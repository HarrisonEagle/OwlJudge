//set many funcs template
//Ver.20190820
#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include<stdbool.h>
#include<time.h>
#include<assert.h>
#define inf 1072114514
#define llinf 4154118101919364364
#define mod 1000000007
#define pi 3.1415926535897932384
#define size 4444

int max(int a,int b){if(a>b){return a;}return b;}
int min(int a,int b){if(a<b){return a;}return b;}
int zt(int a,int b){return max(a,b)-min(a,b);}
int round(int a,int b){if((a%b)*2 >= b){return (a/b)+1;}return a/b;}
int ceil(int a,int b){if(a%b==0){return a/b;}return (a/b)+1;}
int gcd(int a,int b){int c;while(b!=0){c=a%b;a=b;b=c;}return a;}
int lcm(int a,int b){int c=gcd(a,b);a/=c;return a*b;}
int nCr(int a,int b){int i,r=1;for(i=1;i<=b;i++){r*=(a+1-i);r/=i;}return r;}
int nHr(int a,int b){return nCr(a+b-1,b);}
int fact(int a){int i,r=1;for(i=1;i<=a;i++){r*=i;}return r;}
int pow(int a,int b){int i,r=1;for(i=1;i<=b;i++){r*=a;}return r;}
int dsum(int x){int r=0;while(x){r+=(x%10);x/=10;}return r;}
int dsumb(int x,int b){int r=0;while(x){r+=(x%b);x/=b;}return r;}
int sankaku(int x){return ((1+x)*x)/2;}
void swap(int *a,int *b){int c;c=(*a);(*a)=(*b);(*b)=c;}
long long llmax(long long a,long long b){if(a>b){return a;}return b;}
long long llmin(long long a,long long b){if(a<b){return a;}return b;}
long long llzt(long long a,long long b){return llmax(a,b)-llmin(a,b);}
long long llround(long long a,long long b){if((a%b)*2 >= b){return (a/b)+1;}return a/b;}
long long llceil(long long a,long long b){if(a%b==0){return a/b;}return (a/b)+1;}
long long llgcd(long long a,long long b){long long c;while(b!=0){c=a%b;a=b;b=c;}return a;}
long long lllcm(long long a,long long b){long long c=llgcd(a,b);a/=c;return a*b;}
long long llnCr(long long a,long long b){long long i,r=1;for(i=1;i<=b;i++){r*=(a+1-i);r/=i;}return r;}
long long llnHr(long long a,long long b){return llnCr(a+b-1,b);}
long long llfact(long long a){long long i,r=1;for(i=1;i<=a;i++){r*=i;}return r;}
long long llpow(long long a,long long b){long long i,r=1;for(i=1;i<=b;i++){r*=a;}return r;}
long long lldsum(long long x){long long r=0;while(x){r+=(x%10);x/=10;}return r;}
long long lldsumb(long long x,long long b){long long r=0;while(x){r+=(x%b);x/=b;}return r;}
long long llsankaku(long long x){return ((1+x)*x)/2;}
void llswap(long long *a,long long *b){long long c;c=(*a);(*a)=(*b);(*b)=c;}
double dbmax(double a,double b){if(a>b){return a;}return b;}
double dbmin(double a,double b){if(a<b){return a;}return b;}
double dbzt(double a,double b){return dbmax(a,b)-dbmin(a,b);}
void dbswap(double *a,double *b){double c;c=(*a);(*a)=(*b);(*b)=c;}
void chswap(char *a,char *b){char c;c=(*a);(*a)=(*b);(*b)=c;}
int sortfncsj(const void *a,const void *b){if(*(int *)a>*(int *)b){return 1;}if(*(int *)a==*(int *)b){return 0;}return -1;}
int sortfnckj(const void *a,const void *b){if(*(int *)a<*(int *)b){return 1;}if(*(int *)a==*(int *)b){return 0;}return -1;}
int llsortfncsj(const void *a,const void *b){if(*(long long *)a>*(long long *)b){return 1;}if(*(long long *)a==*(long long *)b){return 0;}return -1;}
int llsortfnckj(const void *a,const void *b){if(*(long long *)a<*(long long *)b){return 1;}if(*(long long *)a==*(long long *)b){return 0;}return -1;}
int dbsortfncsj(const void *a,const void *b){if(*(double *)a>*(double *)b){return 1;}if(*(double *)a==*(double *)b){return 0;}return -1;}
int dbsortfnckj(const void *a,const void *b){if(*(double *)a<*(double *)b){return 1;}if(*(double *)a==*(double *)b){return 0;}return -1;}
int strsortfncsj(const void *a,const void *b){return strcmp((char *)a,(char *)b);}
int strsortfnckj(const void *a,const void *b){return strcmp((char *)b,(char *)a);}
int chsortfncsj(const void *a,const void *b){if(*(char *)a>*(char *)b){return 1;}if(*(char *)a==*(char *)b){return 0;}return -1;}
int chsortfnckj(const void *a,const void *b){if(*(char *)a<*(char *)b){return 1;}if(*(char *)a==*(char *)b){return 0;}return -1;}

long long dx4[4]={1,-1,0,0};
long long dy4[4]={0,0,1,-1};

long long search(long long x,long long a[],long long n){
    long long st=0,fi=n-1,te;
    while(st<=fi){
        te=(st+fi)/2;
        if(a[te]<x){st=te+1;}else{fi=te-1;}
    }
    return st;
}

typedef struct{
long long val;
long long node;
}sd;

int sdsortfnc(const void *a,const void *b){
if(((sd*)a)->val < ((sd*)b)->val){return -1;}
if(((sd*)a)->val > ((sd*)b)->val){return 1;}
return 0;
}

void coordinate_comp(long long a[],long long n){
  long long i,c=0;
  sd dat[524288];
  for(i=0;i<n;i++){
    dat[i].val=a[i];
    dat[i].node=i;
  }
  qsort(dat,n,sizeof(dat[0]),sdsortfnc);
  a[dat[0].node]=c;
  for(i=1;i<n;i++){
    if(dat[i-1].val!=dat[i].val){c++;}
    a[dat[i].node]=c;
  }
}

long long **fl,**s;
long long xcnt=0,ycnt=0;
long long qfl=0;
long long wq[16777216],wsp=0;

void rep(){
  long long a,b,i;
  wsp--;
  a=wq[wsp]/size;
  b=wq[wsp]%size;
  if(qfl){return;}
  if(a<0 || xcnt<=a){return;}
  if(b<0 || ycnt<=b){return;}
  //if(fl[a][b]!=0){return;}
  fl[a][b]=1;
  if(s[a][b]==-1){qfl=1;return;}
  for(i=0;i<4;i++){
    if(fl[a+dx4[i]][b+dy4[i]]!=0){continue;}
    fl[a+dx4[i]][b+dy4[i]]=1;
    wq[wsp]=(a+dx4[i])*size+b+dy4[i];
    wsp++;
  }
}

int main(void){
  long long i,j,n,m,r=0;
  long long a[size],b[size],c[size];
  long long d[size],e[size],f[size];
  long long x[size],cx[size];
  long long y[size],cy[size];
  s=malloc(sizeof(long long*)*size);
  fl=malloc(sizeof(long long*)*size);
  for(i=0;i<size;i++){
    s[i]=malloc(sizeof(long long)*size);
    fl[i]=malloc(sizeof(long long)*size);
    for(j=0;j<size;j++){s[i][j]=0;fl[i][j]=0;}
  }
  long long sp,fp,vq;
  scanf("%lld%lld",&n,&m);
  
  x[xcnt]=-inf;xcnt++;
  x[xcnt]=inf;xcnt++;
  y[ycnt]=-inf;ycnt++;
  y[ycnt]=inf;ycnt++;
  for(i=0;i<n;i++){
    scanf("%lld%lld%lld",&a[i],&b[i],&c[i]);
    x[xcnt]=a[i];xcnt++;
    x[xcnt]=b[i];xcnt++;
    y[ycnt]=c[i];ycnt++;
    y[ycnt]=c[i];ycnt++;
  }
  for(i=0;i<m;i++){
    scanf("%lld%lld%lld",&f[i],&d[i],&e[i]);
    y[ycnt]=d[i];ycnt++;
    y[ycnt]=e[i];ycnt++;
    x[xcnt]=f[i];xcnt++;
    x[xcnt]=f[i];xcnt++;
  }

  qsort(x,xcnt,sizeof(long long),llsortfncsj);
  for(i=0;i<xcnt;i++){cx[i]=x[i];}
  coordinate_comp(cx,xcnt);
  
  qsort(y,ycnt,sizeof(long long),llsortfncsj);
  for(i=0;i<ycnt;i++){cy[i]=y[i];}
  coordinate_comp(cy,ycnt); 

  for(i=0;i<xcnt;i++){
    for(j=0;j<ycnt;j++){
      if(i==0 || i==xcnt-1 || j==0 || j==ycnt-1){s[i][j]=-1;}
      else{s[i][j]=(x[i+1]-x[i])*(y[j+1]-y[j]);}
    }
  }

  for(i=0;i<n;i++){
    sp=search(a[i],x,xcnt);
    fp=search(b[i],x,xcnt);
    while(x[fp+1]==b[i]){fp++;}
    vq=search(c[i],y,ycnt);
    //printf("[%lld %lld)\n",sp,fp);
    for(j=sp;j<fp;j++){fl[j][vq]=-1;}
  }
  
  for(i=0;i<m;i++){
    sp=search(d[i],y,ycnt);
    fp=search(e[i],y,ycnt);
    while(y[fp+1]==e[i]){fp++;}
    vq=search(f[i],x,xcnt);
    //printf("[%lld %lld)\n",sp,fp);
    for(j=sp;j<fp;j++){fl[vq][j]=-1;}
  }
  
  sp=search(0,x,xcnt);while(x[sp]>0){sp--;}
  fp=search(0,y,ycnt);while(y[fp]>0){fp--;}
  
  //for(i=0;i<xcnt;i++){
  //  for(j=0;j<ycnt;j++){
  //    printf("%lld",-1*fl[i][j]);
  //  }printf("\n");
  //}
  
  wq[wsp]=sp*size+fp;
  wsp++;
  while(wsp>0){rep();}

  for(i=0;i<xcnt;i++){
    for(j=0;j<ycnt;j++){
      if(fl[i][j]==1){
        if(s[i][j]==-1){puts("INF");return 0;}
        r+=s[i][j];
      }
    }
  }
  
  printf("%lld\n",r);
  return 0;
}
