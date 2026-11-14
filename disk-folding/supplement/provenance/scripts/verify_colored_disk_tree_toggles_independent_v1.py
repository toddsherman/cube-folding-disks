#!/usr/bin/env python3
"""Regenerate the whole abstract domain and replay explicit cube-vertex actions.

No producer import, compiler, search solver or mask-DP recurrence is used.
"""
from collections import Counter
from itertools import permutations,product
from pathlib import Path
import argparse,copy,hashlib,json,time
ROOT=Path(__file__).resolve().parents[1]
SELF='scripts/verify_colored_disk_tree_toggles_independent_v1.py'
SOURCE='results/colored-disk-tree-toggle-certificates-independent-v1.json'
PRIMARY='results/minimal-colored-disk-region-trees-primary-v1.json'
OUT='results/colored-disk-tree-toggles-independent-verification-v1.json'
NORMALS=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1))
VERTICES=tuple(product((-1,1),repeat=3))
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def cube():
 # Reconstruct all face permutations preserving opposite pairs, not signed
 # axis generation. Derive vertex actions by incident-face intersections.
 faces=[p for p in permutations(range(6)) if all(p[i^1]==(p[i]^1) for i in range(6))]
 assert len(faces)==48
 incidence=[frozenset(i for i,n in enumerate(NORMALS) if sum(a*b for a,b in zip(v,n))==1) for v in VERTICES]
 vertices=[tuple(incidence.index(frozenset(f[i] for i in cell)) for cell in incidence) for f in faces]
 sigma={};edge_vertices={}
 for a,b in permutations(range(6),2):
  ends=tuple(i for i,s in enumerate(incidence) if a in s and b in s)
  if len(ends)!=2:continue
  candidates=[i for i,(f,g) in enumerate(zip(faces,vertices)) if f[a]==b and all(g[v]==v for v in ends)]
  assert len(candidates)==1
  sigma[a,b]=vertices[candidates[0]];edge_vertices[a,b]=ends
 return faces,vertices,sigma,edge_vertices,incidence
def adjacent(a,b):return a!=b and a!=(b^1)
def orbit_check(doc,faces):
 assert doc['face_normals']==list(map(list,NORMALS)) and doc['cube_vertices']==list(map(list,VERTICES))
 assert doc['cube_face_actions']==list(map(list,faces))
 for size in (2,3):
  alltuples=set(permutations(range(6),size));covered=set();reps=[]
  for row in doc['leaf_orbits'][str(size)]:
   rep=tuple(row['representative']);reps.append(rep)
   orders=list(permutations(range(size))) if size==3 else [tuple(range(size))]
   exact={tuple(f[rep[k]] for k in order) for f in faces for order in orders}
   assert not covered&exact;covered|=exact
   assert len(exact)==row['orbit_size']
   listed=set()
   for w in row['action_witnesses']:
    p=tuple(w['leg_permutation']);assert p in orders
    target=tuple(faces[w['action']][rep[k]] for k in p)
    assert target==tuple(w['target']);listed.add(target)
   assert listed==exact
  assert covered==alltuples
  assert reps==([(0,1),(0,2)] if size==2 else [(0,1,2),(0,2,4)])
def templates():
 for arcs in range(5,13):
  for leaves in ((0,1),(0,2)):
   yield 'path',arcs,(),[-1]+[i-1 for i in range(1,arcs+1)],{0:leaves[0],arcs:leaves[1]}
  for a in range(1,arcs):
   for b in range(1,arcs-a):
    c=arcs-a-b;parent=[-1];ends=[]
    for length in (a,b,c):
     first=len(parent)
     parent.extend([0]+list(range(first,first+length-1)));ends.append(len(parent)-1)
    for leaves in ((0,1,2),(0,2,4)):
     yield 'Y',arcs,(a,b,c),parent,dict(zip(ends,leaves))
def domain():
 # Whole-tree forward adjacency recursion, separate from producer leg products.
 for kind,arcs,lengths,parents,fixed in templates():
  colors=[-1]*len(parents);allowed=[c for c in range(6) if c not in fixed.values()]
  def visit(v):
   if v==len(parents):
    if set(colors)==set(range(6)):yield tuple(colors)
    return
   for color in ([fixed[v]] if v in fixed else allowed):
    if v and not adjacent(colors[parents[v]],color):continue
    colors[v]=color;yield from visit(v+1)
  for word in visit(0):yield (kind,arcs,lengths,word),parents
def key(row):return row['kind'],row['arcs'],tuple(row['leg_lengths'] or()),tuple(row['colors'])
def replay(row,parents,sigma,edge_vertices,incidence,mask_override=None):
 n=len(parents);assert row['parents']==parents and row['arcs']==n-1
 colors=row['colors'];assert len(colors)==n and set(colors)==set(range(6))
 assert all(adjacent(colors[parents[v]],colors[v]) for v in range(1,n))
 mask=row['active_mask'] if mask_override is None else mask_override
 assert type(mask) is int and 0<=mask<(1<<(n-1))
 if mask_override is None:assert mask.bit_count()==row['active_arcs']<=7
 transforms=[tuple(range(8))];newcolors=[colors[0]]
 for v in range(1,n):
  p=parents[v];old=transforms[p];e=(colors[p],colors[v])
  transform=old if mask>>(v-1)&1 else tuple(old[sigma[e][q]] for q in range(8))
  # Check both full target-edge vertices, not just the incident face labels.
  assert all(transform[q]==old[q] for q in edge_vertices[e])
  original_vertices=[q for q,s in enumerate(incidence) if colors[v] in s]
  assert len(original_vertices)==4
  transformed_vertices={transform[q] for q in original_vertices}
  newface=next(c for c in range(6) if {q for q,s in enumerate(incidence) if c in s}==transformed_vertices)
  assert (newface!=newcolors[p])==bool(mask>>(v-1)&1)
  if newface!=newcolors[p]:assert adjacent(newface,newcolors[p])
  transforms.append(transform);newcolors.append(newface)
 return len(set(newcolors))==6
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',default=SOURCE);ap.add_argument('--output',default=OUT);args=ap.parse_args();assert not(ROOT/args.output).exists();begin=time.monotonic()
 doc=json.loads((ROOT/args.input).read_text());primary=json.loads((ROOT/PRIMARY).read_text())
 for entry in doc['inputs']:assert sha(entry['path'])==entry['sha256']
 for path,value in primary['bindings'].items():assert sha(path)==value
 faces,vertices,sigma,edge_vertices,incidence=cube();orbit_check(doc,faces)
 assert doc['cube_vertex_actions']==list(map(list,vertices))
 assert faces[doc['identity_action']]==tuple(range(6))
 for a in range(6):
  for b in range(6):
   if (a,b) in sigma:assert vertices[doc['edge_reflection_actions'][a][b]]==sigma[a,b]
   else:assert doc['edge_reflection_actions'][a][b]==-1
 records={key(r):r for r in doc['records']};assert len(records)==len(doc['records'])
 counts=Counter();bounds=Counter();survivors=[];seen=set();endpoint_checks=0;minimal_checks=0
 for k,parents in domain():
  assert k not in seen;seen.add(k);assert k in records,k
  row=records[k];assert replay(row,parents,sigma,edge_vertices,incidence)
  counts[f'{k[0]}:{k[1]}']+=1;bounds[str(row['active_arcs'])]+=1;endpoint_checks+=2*(len(parents)-1)
  if row['active_arcs']==row['arcs']:
   # Only80 small survivors: independently test every cheaper toggle here.
   assert row['arcs']<=7
   for mask in range((1<<row['arcs'])-1):
    minimal_checks+=1
    assert not replay(row,parents,sigma,edge_vertices,incidence,mask_override=mask)
   survivors.append(k)
 assert seen==set(records) and len(seen)==87538
 assert dict(counts)==doc['counts']==primary['counts']
 assert len(survivors)==80 and Counter(k[1] for k in survivors)=={5:38,6:38,7:4}
 assert {(r['kind'],r['arcs'],tuple(r['leg_lengths'] or()),tuple(r['colors'])) for r in primary['minimal_survivors']}==set(survivors)
 assert [i for i,r in enumerate(doc['records']) if key(r) in set(survivors)]==doc['minimal_survivor_indices']
 controls=[]
 def reject(name,fn):
  try:fn()
  except (AssertionError,KeyError,ValueError,StopIteration):controls.append(dict(name=name,rejected=True));return
  raise AssertionError('Tamper accepted: '+name)
 sample=next(r for r in doc['records'] if r['arcs']==12);parents=sample['parents']
 bad=copy.deepcopy(sample);bad['active_mask']=0;bad['active_arcs']=0
 reject('all_inactive_forgery',lambda:assert_positive(bad,parents,sigma,edge_vertices,incidence))
 bad=copy.deepcopy(sample);bad['active_arcs']+=1
 reject('wrong_active_count',lambda:assert_positive(bad,parents,sigma,edge_vertices,incidence))
 bad=copy.deepcopy(sample);bad['parents'][1]=1
 reject('wrong_parent_tree',lambda:assert_positive(bad,parents,sigma,edge_vertices,incidence))
 bad=copy.deepcopy(sample);bad['colors'][1]=bad['colors'][0]
 reject('nonadjacent_original_colors',lambda:assert_positive(bad,parents,sigma,edge_vertices,incidence))
 badsigma=dict(sigma)
 inactive=next(v for v in range(1,len(parents)) if not sample['active_mask']>>(v-1)&1)
 e=sample['colors'][parents[inactive]],sample['colors'][inactive];badsigma[e]=tuple(reversed(range(8)))
 reject('wrong_full_vertex_reflection',lambda:assert_positive(sample,parents,badsigma,edge_vertices,incidence))
 bad=copy.deepcopy(doc);bad['leaf_orbits']['3'][0]['action_witnesses'].pop()
 reject('missing_ordered_leaf_orbit_witness',lambda:orbit_check(bad,faces))
 missing=set(records);missing.remove(key(sample))
 reject('missing_high_arc_pattern',lambda:assert_equal(seen,missing))
 extra=set(records);extra.add(('path',13,(),()))
 reject('extra_out_of_domain_pattern',lambda:assert_equal(seen,extra))
 bad=copy.deepcopy(doc);bad['leaf_orbits']['3'][0]['action_witnesses'][0]['leg_permutation']=[0,0,1]
 reject('forged_leg_permutation',lambda:orbit_check(bad,faces))
 out=dict(status='verified_complete_abstract_path_Y_explicit_toggle_certificates',schema='colored_disk_tree_toggles_independent_verification_v1',
  scope='Complete necessary abstract path/Y domain through12 arcs with exclusive leaves. Every saved witness is replayed as full cube-vertex isometries with pointwise original-edge matching; every E>=8 pattern has a six-covering witness with at most7 active arcs. This result does not itself prove the universal physical-disk reductions or local realization.',
  counts=dict(patterns=87538,cube_actions=48,ordered_path_leaf_tuples=30,ordered_Y_leaf_tuples=120,edge_endpoint_matches=endpoint_checks,small_minimal_survivors=80,cheaper_survivor_toggle_checks=minimal_checks,negative_controls=len(controls)),
  domain_counts=dict(counts),witness_active_arc_histogram=dict(bounds),survivor_arc_histogram=dict(Counter(k[1] for k in survivors)),
  negative_controls=controls,inputs=[dict(path=p,sha256=sha(p)) for p in (SELF,args.input,PRIMARY)],seconds=time.monotonic()-begin)
 with(ROOT/args.output).open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps(dict(status=out['status'],counts=out['counts'],seconds=out['seconds'],sha256=sha(args.output))))
def assert_positive(row,parents,sigma,edge_vertices,incidence):assert replay(row,parents,sigma,edge_vertices,incidence)
def assert_equal(a,b):assert a==b
if __name__=='__main__':main()
