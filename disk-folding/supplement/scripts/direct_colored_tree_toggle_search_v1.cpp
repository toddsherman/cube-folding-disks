#include <algorithm>
#include <array>
#include <iostream>
#include <vector>
// Direct group-action enumeration only. No mask dynamic programming.
int main(){
  int identity; std::cin>>identity;
  int face[48][6],multiply[48][48],edge[6][6];
  for(auto &row:face)for(int &x:row)std::cin>>x;
  for(auto &row:multiply)for(int &x:row)std::cin>>x;
  for(auto &row:edge)for(int &x:row)std::cin>>x;
  int count;std::cin>>count;
  for(int index=0;index<count;index++){
    int n;std::cin>>n;std::vector<int> parent(n),color(n),state(n);
    for(int &x:parent)std::cin>>x;
    for(int &x:color)std::cin>>x;
    const int arcs=n-1;
    int answer=-1;unsigned long long tested=0;
    for(int cost=0;cost<=std::min(arcs,7)&&answer<0;cost++){
      for(int mask=0;mask<(1<<arcs);mask++){
        if(__builtin_popcount((unsigned)mask)!=cost)continue;
        tested++;state[0]=identity;int covered=1<<color[0];
        for(int v=1;v<n;v++){
          int p=parent[v];
          state[v]=(mask&(1<<(v-1)))?state[p]:multiply[state[p]][edge[color[p]][color[v]]];
          covered|=1<<face[state[v]][color[v]];
        }
        if(covered==63){answer=mask;break;}
      }
    }
    std::cout<<index<<' '<<answer<<' '<<tested<<'\n';
  }
}
