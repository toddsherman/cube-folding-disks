#!/usr/bin/env python3
"""Complete path/Y certificate via leg products and direct cube-group search."""
from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse,hashlib,json,subprocess,tempfile,time
ROOT=Path(__file__).resolve().parents[1]
SELF='scripts/certify_colored_disk_tree_toggles_independent_v1.py'
CPP='scripts/direct_colored_tree_toggle_search_v1.cpp'
OUT='results/colored-disk-tree-toggle-certificates-independent-v1.json'
NORMALS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
VERTICES=tuple(product((-1,1),repeat=3))
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def cube():
 actions={}
 for axes in permutations(range(3)):
  for signs in product((-1,1),repeat=3):
   def transform(v):return tuple(signs[j]*v[axes[j]] for j in range(3))
   f=tuple(NORMALS.index(transform(n)) for n in NORMALS)
   actions[f]=tuple(VERTICES.index(transform(v)) for v in VERTICES)
 faces=sorted(actions);vertices=[actions[f] for f in faces];assert len(faces)==48
 identity=faces.index(tuple(range(6)))
 multiply=[[faces.index(tuple(a[b[c]] for c in range(6))) for b in faces] for a in faces]
 edge=[[-1]*6 for _ in range(6)]
 for a,b in permutations(range(6),2):
  ends=[i for i,v in enumerate(VERTICES) if sum(x*y for x,y in zip(v,NORMALS[a]))==sum(x*y for x,y in zip(v,NORMALS[b]))==1]
  if len(ends)!=2:continue
  hits=[i for i,f in enumerate(faces) if f[a]==b and all(vertices[i][v]==v for v in ends)]
  assert len(hits)==1;edge[a][b]=hits[0]
 return faces,vertices,identity,multiply,edge
def adjacent(a,b):return sum(x*y for x,y in zip(NORMALS[a],NORMALS[b]))==0
def leaf_orbits(faces):
 out={}
 for size in (2,3):
  tuples=set(permutations(range(6),size));classes=[]
  while tuples:
   rep=min(tuples)
   # Y leg labels may be permuted; all positive ordered lengths are retained.
   orders=list(permutations(range(size))) if size==3 else [tuple(range(size))]
   orbit={tuple(g[rep[j]] for j in order) for g in faces for order in orders}
   assert orbit<=tuples;tuples-=orbit
   witnesses=[]
   for target in sorted(orbit):
    action,order=next((i,p) for i,g in enumerate(faces) for p in orders if tuple(g[rep[j]] for j in p)==target)
    witnesses.append(dict(target=target,action=action,leg_permutation=order))
   classes.append(dict(representative=rep,orbit_size=len(orbit),action_witnesses=witnesses))
  out[str(size)]=classes
 assert [x['representative'] for x in out['2']]==[(0,1),(0,2)]
 assert [x['representative'] for x in out['3']]==[(0,1,2),(0,2,4)]
 return out
def legs(start,end,length,allowed):
 if length==1:
  return [(end,)] if adjacent(start,end) else []
 return [(x,)+tail for x in allowed if adjacent(start,x) for tail in legs(x,end,length-1,allowed)]
def domain(orbits):
 rows=[]
 for arcs in range(5,13):
  for o in orbits['2']:
   a,b=o['representative'];allowed=[x for x in range(6) if x not in (a,b)]
   for word in legs(a,b,arcs,allowed):
    colors=(a,)+word
    if len(set(colors))==6:rows.append(dict(kind='path',arcs=arcs,leg_lengths=None,parents=[-1]+list(range(arcs)),colors=colors))
  for first,second in combinations(range(1,arcs),2):
   lengths=(first,second-first,arcs-second)
   for o in orbits['3']:
    leaves=o['representative'];allowed=[x for x in range(6) if x not in leaves]
    for center in allowed:
     choices=[legs(center,leaf,length,allowed) for leaf,length in zip(leaves,lengths)]
     for three in product(*choices):
      colors=(center,)+sum(three,())
      if len(set(colors))!=6:continue
      parents=[-1]
      for leg in three:
       prev=0
       for _ in leg:parents.append(prev);prev=len(parents)-1
      rows.append(dict(kind='Y',arcs=arcs,leg_lengths=lengths,parents=parents,colors=colors))
 return rows
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default=OUT);args=ap.parse_args();assert not(ROOT/args.output).exists();begin=time.monotonic()
 faces,vertices,identity,multiply,edge=cube();orbits=leaf_orbits(faces);rows=domain(orbits)
 assert len(rows)==87538 and len({(r['kind'],r['arcs'],tuple(r['leg_lengths'] or()),tuple(r['colors'])) for r in rows})==len(rows)
 with tempfile.TemporaryDirectory(prefix='origami-direct-toggles-') as tmp:
  binary=Path(tmp)/'direct';subprocess.run(['c++','-std=c++17','-O3',str(ROOT/CPP),'-o',str(binary)],check=True)
  data=[str(identity)]
  for block in (faces,multiply,edge):data.extend(' '.join(map(str,r)) for r in block)
  data.append(str(len(rows)))
  for r in rows:data.extend((str(len(r['colors'])),' '.join(map(str,r['parents'])),' '.join(map(str,r['colors']))))
  proc=subprocess.run([str(binary)],input='\n'.join(data)+'\n',text=True,capture_output=True,check=True,timeout=120)
 output=proc.stdout.splitlines();assert len(output)==len(rows)
 counts=Counter();histogram=Counter();survivors=[];tested=0
 for i,(r,line) in enumerate(zip(rows,output)):
  j,mask,tried=map(int,line.split());assert i==j and mask>=0
  cost=mask.bit_count();assert cost<=7 and cost<=r['arcs']
  r['active_mask']=mask;r['active_arcs']=cost;r['direct_masks_examined']=tried
  counts[f"{r['kind']}:{r['arcs']}"]+=1;histogram[f"{r['kind']}:{r['arcs']}:minimum={cost}"]+=1;tested+=tried
  if cost==r['arcs']:survivors.append(i)
 out=dict(status='complete_explicit_abstract_path_Y_toggle_certificates',schema='colored_disk_tree_toggle_certificates_independent_v1',
  scope='Explicit six-covering toggle witnesses for every abstract path/Y pattern with exclusive leaf colors and5..12 original active arcs. Direct search is not a folding or physical-domain theorem; source lifting and analytic reductions require separate review.',
  face_normals=NORMALS,cube_vertices=VERTICES,cube_face_actions=faces,cube_vertex_actions=vertices,identity_action=identity,edge_reflection_actions=edge,
  leaf_orbits=orbits,records=rows,counts=dict(counts),minimum_histogram=dict(histogram),minimal_survivor_indices=survivors,
  total_patterns=len(rows),direct_masks_examined=tested,maximum_witness_arcs=max(r['active_arcs'] for r in rows),
  inputs=[dict(path=p,sha256=sha(p)) for p in (SELF,CPP)],seconds=time.monotonic()-begin)
 with(ROOT/args.output).open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps(dict(status=out['status'],patterns=len(rows),direct_masks_examined=tested,survivors=len(survivors),max_arcs=out['maximum_witness_arcs'],seconds=out['seconds'],sha256=sha(args.output))))
if __name__=='__main__':main()
