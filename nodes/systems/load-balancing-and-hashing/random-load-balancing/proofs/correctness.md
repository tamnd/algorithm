---
title: Random dispatch picks each server with probability 1/n, the weighted pick picks server i with probability w_i / W, and the loads follow the one-choice law
proves: [correctness]
status: full
---

We use the pseudocode of the page. There are $n \ge 1$ servers. RANDOM$(0, n-1)$ returns an index that is uniform on $\{0, \ldots, n-1\}$ and independent of all other calls. RANDOM-REAL returns a real number that is uniform on $[0, 1)$ and independent of all other calls.

## Lemma 1 (uniform dispatch)

**Claim.** One call of RANDOM-DISPATCH adds 1 to the load of exactly one server, and this server is $j$ with probability $1/n$ for each $j$. After $m$ calls the load vector has the multinomial law with $m$ trials and $n$ equal cells. In particular each load has mean $m/n$ and variance $m(1/n)(1 - 1/n)$.

*Proof.* Line L1 draws $s$, and line L2 changes $load[s]$ only, by 1. So $\Pr[s = j] = 1/n$. The $m$ calls use independent draws, so the counts of the $m$ draws in the $n$ cells have the multinomial law. The load of server $j$ is the number of the $m$ independent draws that equal $j$, which is binomial with $m$ trials and success probability $1/n$. Its mean is $m/n$ and its variance is $m(1/n)(1 - 1/n)$. $\square$

## Lemma 2 (weighted pick)

**Claim.** Let $w_0, \ldots, w_{n-1} \ge 0$ with $W = \sum_i w_i > 0$, and let $prefix[i] = w_0 + \cdots + w_i$. WEIGHTED-PICK returns $i$ with probability exactly $w_i/W$. A server with $w_i = 0$ is never returned.

*Proof.* Set $prefix[-1] = 0$. The array $prefix$ is nondecreasing and $prefix[n-1] = W$. Line L3 draws $u$ uniform on $[0, W)$. Line L4 returns the least $i$ with $prefix[i] > u$. Such an $i$ exists because $prefix[n-1] = W > u$. The least such $i$ satisfies $prefix[i-1] \le u < prefix[i]$: the right inequality holds by the choice of $i$, and the left one holds because $i - 1$ does not qualify (or $i = 0$ and $prefix[-1] = 0 \le u$). Conversely, if $prefix[i-1] \le u < prefix[i]$, then every $k < i$ has $prefix[k] \le prefix[i-1] \le u$, so $i$ is the least index that qualifies. So line L4 returns $i$ exactly when $u \in [prefix[i-1], prefix[i])$. This interval has length $w_i$, so the probability is $w_i/W$. If $w_i = 0$ the interval is empty. $\square$

*The binary search.* Because $prefix$ is sorted, the least $i$ with $prefix[i] > u$ is found by [binary search](/binary-search/) in $O(\log n)$ comparisons. In Python, `bisect_right(prefix, u)` returns the number of entries $\le u$, and in a sorted array this number is the least index of an entry $> u$. Floating point can round $u$ up to $W$; the code then returns the last server, which changes the law by at most one unit of rounding.

## Lemma 3 (the maximum load)

**Claim.** After $n$ calls of RANDOM-DISPATCH on $n$ servers, the maximum load is $(1 + o(1))\ln n/\ln\ln n$ with high probability. After $m \ge n\ln n$ calls it is $m/n + \Theta(\sqrt{m\ln n/n})$ with high probability.

*Proof.* By Lemma 1 the process is exactly the throw of $m$ balls into $n$ bins, one uniform bin per ball, independently. The two statements are the theorem on the [maximum load of balls into bins](/balls-into-bins-max-load/), proved in full in its proof file. $\square$

## Lemma 4 (round robin is exact)

**Claim.** If request $t = 0, 1, \ldots, m-1$ goes to server $t \bmod n$, then each server gets $\lfloor m/n \rfloor$ or $\lceil m/n \rceil$ requests.

*Proof.* Write $m = qn + r$ with $0 \le r < n$. The requests $0, \ldots, qn - 1$ give exactly $q$ to each server. The last $r$ requests go to servers $0, \ldots, r - 1$, one each. So servers $0, \ldots, r-1$ get $q + 1$ and the others get $q$. $\square$

## Lemma 5 (queues)

**Claim.** Let requests arrive as a Poisson stream of rate $\lambda n$ with $0 < \lambda < 1$, and let each server work in order of arrival with exponential service times of rate 1. Under random dispatch, each server is an M/M/1 queue with arrival rate $\lambda$, and its mean number of requests in equilibrium is $\lambda/(1-\lambda)$.

*Proof.* Each arrival goes to server $j$ with probability $1/n$, independently of the stream and of the other arrivals (Lemma 1). By the splitting property of the Poisson process, the arrivals at server $j$ form a Poisson stream of rate $\lambda$, independent of the streams of the other servers. With exponential service of rate 1, server $j$ is an M/M/1 queue of load $\lambda < 1$. Its equilibrium law is geometric, $\Pr[Q = k] = (1 - \lambda)\lambda^k$, with mean $\lambda/(1-\lambda)$. $\blacksquare$

The fraction of servers with at least $i$ requests is therefore $\lambda^i$ in equilibrium. With two choices it is $\lambda^{2^i - 1}$, which is the gain shown on the page of the [power of two choices](/power-of-two-choices/).
