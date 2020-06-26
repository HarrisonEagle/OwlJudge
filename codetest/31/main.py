#include<bits/stdc++.h>
using namespace std;
#include<math.h>
#define ll long long
#define ld long double
#define Summon_Tourist ios::sync_with_stdio(false);cin.tie(0);
ll gcd(ll a , ll b) { return b==0?a: gcd( b, a%b); }
ll lcm(ll a , ll b) { return a/gcd(a,b) * b ; }
ll inf = 1e9 + 7;
ll N = 2e5 + 200 ;
ll modexp( ll base ,ll power)
 {
     if( power == 0  ) return 1;
     if( power & 1) return base*modexp( base , power-1 )%inf;
     return modexp(base*base%inf,power/2);
 }
 int main()
{
  Summon_Tourist
  //freopen("input.txt" , "r" , stdin ) ;
  ll t = 1;
  //cin>>t;
  while(t--)
  {
     ll n;
     cin>>n;
     vector<ll> a;
     for( ll i = 0 ; i<N ; i++ )
     {
         a.push_back( modexp(2ll,i) );
     }
     ll k = inf-1 ;
     map<pair<ll,ll>,pair<ll,ll>> mp;
     for( ll i = 0 ; i<n ; i++ ){
        ll x,y;
        cin>>x>>y;
        if( x==0 && y==0 ) { k++; continue ; }
        if( make_pair(x,y) < make_pair(0ll,0ll) ) { x=-x; y=-y;  }
        ll g = gcd( abs(x) , abs(y) );
        x /= g ; y /= g ;
        if(y>0) { mp[{x,y}].first++ ; }
        else { mp[{-y,x}].second++ ; }
     }
     ll r = 1 ;
     for( auto p : mp )
     {
         r = r *( a[p.second.second] + a[p.second.first] - 1)%inf ;
     }
     cout<<(k+r)%inf;
  }
  return 0;

}
