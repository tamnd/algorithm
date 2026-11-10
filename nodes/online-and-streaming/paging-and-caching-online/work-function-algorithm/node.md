---
tag: CQEK7R
kind: algorithm
slug: work-function-algorithm
name: Work function algorithm
aliases:
- WFA
- work function
- work-function algorithm
area: online-and-streaming/paging-and-caching-online
level: research
summary: Moves servers according to minimum offline cost to reach configurations; gives a (2k-1)-competitive k-server algorithm.
solves: [k-server-problem]
model: word-ram
complexity:
  vars: {m: the number of requests, n: the number of points, k: the number of servers}
  time: {worst: O(m k n^k)}
  space: {extra: O(n^k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1995
  people: [Elias Koutsoupias, Christos H. Papadimitriou]
  note: Koutsoupias and Papadimitriou proved in 1994 that the work function algorithm is (2k-1)-competitive on every metric space. The journal version appeared in 1995.
prereqs: [k-server-problem, work-function, competitive-ratio, offline-optimum]
see_also: [double-coverage, k-server-conjecture, metrical-task-systems, metrical-service-systems, balance-algorithm]
sources:
  - paper: doi:10.1145/210118.210128
    title: "Elias Koutsoupias and Christos H. Papadimitriou, On the k-server conjecture, Journal of the ACM 42(5) (1995), 971-983"
    locator: the work function algorithm, quasiconvexity of work functions, and the proof of the bound 2k - 1
  - paper: doi:10.1016/j.cosrev.2009.04.002
    title: "Elias Koutsoupias, The k-server problem, Computer Science Review 3(2) (2009), 105-118"
    locator: Section 3.3, the work function algorithm (Definition 1, Lemma 1 on duality, Lemma 2 on the extended cost, Theorem 3)
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 10, the k-server problem, the sections on work functions and the work function algorithm
  - paper: "Yair Bartal and Elias Koutsoupias, On the competitive ratio of the work function algorithm for the k-server problem, Theoretical Computer Science 324(2-3) (2004), 337-345"
    locator: the proofs that the work function algorithm is k-competitive on the line, on weighted stars and on metrics with k + 2 points
  - paper: "Christian Coester, Elias Koutsoupias and Marek Zbysinski, The k-server conjecture is true, arXiv:2609.15979, 2026"
    locator: the claim that the work function algorithm is k-competitive on every metric space (a preprint, not yet refereed)
---

The work function algorithm (WFA) is a deterministic online algorithm for the [k-server problem](/k-server-problem/). It keeps the [work function](/work-function/), the cheapest offline cost to serve the requests so far and end in each configuration, and it moves the server that makes the sum of this cost and the move cost smallest. Koutsoupias and Papadimitriou proved in 1995 that it is $(2k-1)$-competitive on every metric space, which is the best bound known for general metrics. It is $k$-competitive on several special metrics, and it is the main candidate for the deterministic [k-server conjecture](/k-server-conjecture/).

## In plain words

Two simple ideas both fail. The first idea is to move the nearest server, which is cheap now but can be tricked into many small moves. The second idea is to copy what the best offline plan would have done so far, but that plan can change its mind again and again, and copying each change costs a lot.

The work function algorithm mixes the two ideas. For each way to place the servers, it knows the cheapest cost of an offline plan that has served all requests so far and ends there. When a new request comes, it picks the server to move by adding two numbers: the cost of the move now, and the best past cost of the place where it ends. It takes the smallest sum.

## The problem

A metric space $(M, d)$ has $k$ servers on its points. A configuration is a multiset $X$ of $k$ points. The cost to move between configurations $X$ and $Y$ is $D(X, Y)$, the cost of a minimum matching between them. Requests $r_1, r_2, \ldots$ arrive online, and after request $r_t$ some server must be at $r_t$. The cost is the total distance moved.

The **work function** after $t$ requests is $w_t(X)$, the minimum cost of a schedule that starts in $C_0$, serves $r_1, \ldots, r_t$ in order, and ends in $X$. It satisfies

$$w_0(X) = D(C_0, X), \qquad w_t(X) = \min_{x \in X} \bigl( w_{t-1}(X - x + r_t) + d(x, r_t) \bigr),$$

and $w_t(X) = w_{t-1}(X)$ when $r_t \in X$. The [offline optimum](/offline-optimum/) is $\mathrm{OPT} = \min_X w_m(X)$. The [work function](/work-function/) page treats this object and its properties. This page is about the algorithm that uses it.

## The algorithm

```pseudo id=main
WORK-FUNCTION-ALGORITHM(d, C_0, σ)
L1  C ← C_0, cost ← 0
L2  w(X) ← D(C_0, X) for each configuration X
L3  for each request r in σ do
L4      w(X) ← min over x in X of w_old(X − x + r) + d(x, r), for each X
L5      if r ∉ C then
L6          s ← the server x in C with the least w(C − x + r) + d(x, r)
L7          cost ← cost + d(s, r)
L8          C ← C − s + r
L9  return cost
```

Line L4 updates the work function by its recurrence, with the old values on the right side. Line L6 is the rule: the new configuration $C - s + r$ must contain $r$, and among these the algorithm minimizes $w_t(C - s + r) + d(s, r)$. The term $d(s, r)$ alone would give the greedy rule. The term $w_t(C - s + r)$ alone would give the rule that jumps to an offline optimal configuration. In this form WFA is lazy: it moves one server, and only when no server is at $r$.

A useful identity follows from the choice of line L6. With $C$ the old and $C'$ the new configuration,

$$w_t(C) = w_t(C') + d(s, r),$$

because $w_t(C)$ is the minimum over $x \in C$ of $w_{t-1}(C - x + r) + d(x, r)$, and $w_{t-1}$ and $w_t$ agree on configurations that contain $r$.

## Example

Take the points $0$, $10$ and $11$ of the line, two servers at $0$ and $10$, and the requests $11, 10, 11, 10, \ldots$. There are three configurations. The table shows the work function after $t$ requests.

| $t$ | request | $w(\{0,10\})$ | $w(\{0,11\})$ | $w(\{10,11\})$ | WFA after the move | WFA total |
|---|---|---|---|---|---|---|
| 0 | | 0 | 1 | 11 | 0, 10 | 0 |
| 1 | 11 | 2 | 1 | 11 | 0, 11 | 1 |
| 2 | 10 | 2 | 3 | 11 | 0, 10 | 2 |
| 3 | 11 | 4 | 3 | 11 | 0, 11 | 3 |
| 19 | 11 | 20 | 19 | 11 | 0, 11 | 19 |
| 20 | 10 | 20 | 21 | 11 | 10, 11 | 29 |
| 26 | 10 | 22 | 21 | 11 | 10, 11 | 29 |

For the first 19 requests, WFA moves the server between $10$ and $11$, like the greedy rule. At the request $t = 20$ for the point $10$, from $\{0, 11\}$, the two choices cost $w(\{0, 10\}) + 1 = 21$ and $w(\{10, 11\}) + 10 = 21$. The tie goes to the server at $0$ in this program, so WFA moves it to $10$ for a cost of $10$. After that, no server moves again. The optimum is $11$, so the ratio here is $29/11 \approx 2.6$, below $2k - 1 = 3$. Greedy would pay $1$ for each request for ever.

## Correctness

WFA serves each request, because the new configuration of line L8 contains $r$. The bounds come from the work function. The identity above gives $\mathrm{WFA}(\sigma) + \mathrm{OPT}(\sigma) \le \sum_t \max_X (w_t(X) - w_{t-1}(X))$, the *extended cost* bound. On a metric with $k + 1$ points, the sum telescopes, and this gives $\mathrm{WFA} \le k \cdot \mathrm{OPT} + k \cdot \mathrm{diam}$. On a general metric, Koutsoupias and Papadimitriou bound the sum of the extended costs by $2k \cdot \mathrm{OPT}$ plus a constant, with a potential and the *quasiconvexity* of work functions. The full proof of the first two results and a sketch of the third are below.

## Complexity

On a finite metric with $n$ points, there are $\binom{n}{k}$ configurations of distinct points; a lazy schedule never needs two servers at one point. The update of line L4 takes $O(k)$ time for each configuration, so one request costs $O(k \binom{n}{k})$ time and the table needs $O(\binom{n}{k})$ space. This is exponential in $k$.

Without a finite table, the value $w_t(X)$ for one configuration is the cost of an offline k-server schedule, which is a minimum cost flow problem. So line L6 can be done with $k$ flow computations on a graph with $O(t)$ nodes. The time for each request then grows with $t$, and WFA is mostly a tool of the theory, not of practice.

## Properties

- **$(2k-1)$-competitive** on every metric space: $\mathrm{WFA}(\sigma) \le (2k-1) \cdot \mathrm{OPT}(\sigma) + b$, where $b$ depends on the metric and the start (Koutsoupias and Papadimitriou 1995).
- **$k$-competitive** on metrics with $k+1$ points (Koutsoupias and Papadimitriou), on metrics with $k+2$ points, on the line and on weighted stars (Bartal and Koutsoupias 2004), and for $k = 2$ (Chrobak and Larmore). By the lower bound $k$ of Manasse, McGeoch and Sleator, it is optimal there.
- **Not memoryless.** It needs the whole work function, which depends on all past requests.
- **Lazy.** In the form above, it moves only one server, and only on a request that no server covers.

## Variants and improvements

- **Metrical task systems.** The same rule, with $D$ replaced by the metric of the states, is the work function algorithm for [metrical task systems](/metrical-task-systems/). There it is $(2n-1)$-competitive on $n$ states, which is optimal for deterministic algorithms.
- **Metrical service systems.** WFA also applies to [metrical service systems](/metrical-service-systems/), where each request is a set of allowed points.
- **Double coverage.** On the line and on trees, the simpler [double coverage](/double-coverage/) rule is $k$-competitive and needs only $O(k)$ space.
## When to use it

Use WFA as the reference algorithm for k-server on a general metric, in proofs, in teaching, and in experiments on small metrics. For a line or a tree, use [double coverage](/double-coverage/), which is simpler and has the optimal ratio. For [paging](/paging-problem/), use [LRU](/lru/) or a [marking algorithm](/marking-algorithm/). For large metrics, the cost of the work function is too high for practice.

## Pitfalls

- **Using only the work function.** The rule that always moves to the configuration of least $w_t$ is not competitive: it can switch between two configurations far apart at each request.
- **Updating in place.** Line L4 must use the old values of $w$ on the right side. An update in place mixes $w_{t-1}$ and $w_t$.
- **The configuration space.** The table has $\binom{n}{k}$ entries. With $n = 50$ points and $k = 10$ servers, this is already about $10^{10}$.
- **Ties.** The bounds hold for each tie rule, but the cost on a given sequence can depend on it, as in the example.
- **Claims about $k$.** The bound $k$ for every metric is the deterministic k-server conjecture. A 2026 preprint by Coester, Koutsoupias and Zbysinski claims a proof that WFA is $k$-competitive on every metric. It is not yet refereed, so the bound $2k - 1$ is the one to cite as established.

## Implementations

## History

Work functions appear in the work of Chrobak and Larmore on the server problem around 1991 and 1992, and they proved that WFA is $2$-competitive for $k = 2$. Koutsoupias and Papadimitriou proved the bound $2k - 1$ for all metrics at STOC 1994, with the journal version in 1995. Before that, the best bound for general metrics grew exponentially in $k$ (Fiat, Rabani and Ravid 1990). Bartal and Koutsoupias added the line, the weighted star and $k + 2$ points (STACS 2000, journal 2004). In September 2026, Coester, Koutsoupias and Zbysinski posted a preprint that claims WFA is $k$-competitive on every metric space.

## References
