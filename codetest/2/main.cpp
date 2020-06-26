#include <iostream>
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <complex>
#include <cmath>
#include <vector>
#include <map>
#include <set>
#include <stack> 
#include <bitset>
#include <queue>
#include <assert.h>
#include <unordered_map>
using namespace std;

const int N = 200010;
const int mod = 1000000007;
map<pair<long long, long long>, int > mp;

long long mpow(long long a, long long b) {
	long long ans = 1;
	while (b) {
		if (b & 1) ans = ans * a % mod;
		a = a * a % mod;
		b >>= 1;
	}
	return ans;
}

long long gcd(long long a, long long b) {
	return b ? gcd(b, a % b) : a;
}

int main()
{
	int ans = 0, a = 0, b = 0, o = 0;
	int n;
	scanf("%d", &n);
	for (int i = 1; i <= n; i++) {
		long long x, y;
		scanf("%lld%lld", &x, &y);
		if (x == 0 && y == 0) {
			o++;
			continue;
		}
		if (x == 0) a++;
		else if (y == 0) b++;
		else {
			long long d = gcd(abs(x), abs(y));
			x /= d;
			y /= d;
			if (x < 0) x = -x, y = -y;
			mp[make_pair(x, y)]++;
		}
	}

	long long tot = 1;
	while (!mp.empty()) {
        pair<long long, long long> p = mp.begin()->first;		
		long long x = p.first, y = p.second, c = mp[p];
		long long xx = -y, yy = x;
		if (xx < 0) xx = -xx, yy = -yy;
		// (1, 2) => (2, -1)
		if (mp.count(make_pair(xx, yy))) {
			tot = tot * (mpow(2, c) + mpow(2, mp[make_pair(xx, yy)]) - 1) % mod;
			mp.erase(make_pair(x, y));
			mp.erase(make_pair(xx, yy));
		} else {
			tot = tot * mpow(2, c) % mod;
			mp.erase(make_pair(x, y));
		}
	}
	tot = tot * (mpow(2, a) + mpow(2, b) - 1) % mod;
	tot--;
	if (tot < 0) tot += mod;
	ans = (tot + o) % mod;

	cout << ans << endl;
	return 0;
}
