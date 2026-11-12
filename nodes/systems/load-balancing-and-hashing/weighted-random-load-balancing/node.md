---
tag: BWGAF8
kind: algorithm
slug: weighted-random-load-balancing
name: Weighted random load balancing
aliases:
- weighted random selection
- weighted random balancing
area: systems/load-balancing-and-hashing
level: intro
summary: "Send each request to backend i with probability w_i / W. Prefix sums and binary search cost O(log n) per pick; Walker's alias method costs O(1). No shared state is needed."
solves: [load-balancing-problem]
model: word-ram
complexity:
  vars: {n: the number of backends}
  time: {worst: Θ(log n), build: Θ(n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: false, recursive: false}
prereqs: [random-load-balancing, prefix-sums, binary-search]
see_also: [weighted-round-robin, alias-method, weighted-sampling, lottery-scheduling, inverse-transform-sampling, power-of-two-choices, binomial-distribution, fenwick-tree]
sources:
  - paper: doi:10.1145/355744.355749
    title: Alastair J. Walker, An efficient method for generating discrete random variables with general distributions, ACM Transactions on Mathematical Software 3(3), 1977
    locator: pages 253 to 256 (the alias table and the O(1) draw)
  - paper: doi:10.1109/32.92917
    title: Michael D. Vose, A linear algorithm for generating random numbers with a given distribution, IEEE Transactions on Software Engineering 17(9), 1991
    locator: pages 972 to 975 (the O(n) construction with the small and large lists)
  - book: isbn:9780387963051
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986
    locator: Chapter III, Section 2 (the inversion method for discrete distributions, search in a table) and Section 4 (the alias method)
  - paper: "Carl A. Waldspurger and William E. Weihl, Lottery Scheduling: Flexible Proportional-Share Resource Management, Proceedings of the First USENIX Symposium on Operating Systems Design and Implementation (OSDI), 1994"
    locator: the sections on the lottery (a random ticket draw over a list or a tree of partial sums)
  - url: https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/upstream/load_balancing/load_balancers
    title: Envoy documentation, Supported load balancers
    locator: the random load balancer and the use of host weights
---

Weighted random load balancing is a [load balancer](/load-balancer/) policy that sends each request to backend $i$ with probability $w_i / W$, where $w_i \ge 0$ is the weight of backend $i$ and $W = \sum_j w_j$. It is the weighted form of [random load balancing](/random-load-balancing/), and a direct use of [weighted sampling](/weighted-sampling/). With [prefix sums](/prefix-sums/) of the weights and a [binary search](/binary-search/), a pick costs $O(\log n)$; with Walker's [alias method](/alias-method/) it costs $O(1)$ after $O(n)$ setup. Unlike [weighted round robin](/weighted-round-robin/), it needs no counter that the picks share, so many independent balancers can use it without coordination, but each backend gets its share only on average.

## In plain words

Put marks on a ruler, one segment for each server, and make each segment as long as that server's weight. A server with weight five gets a segment five times as long as a server with weight one. For each request, throw a dart at a random point on the ruler, and send the request to the server whose segment it hits.

To find the segment fast, keep the running totals of the lengths and search them by halving, as in a phone book. Over many requests each server gets its share. Over a few requests luck matters: a small server can get two requests in a row, and a large server can get none for a while.

## The problem

The model has $n$ backends with integer weights $w_0, \ldots, w_{n-1} \ge 0$ and $W > 0$, and a stream of requests in any order. For each request the balancer must return backend $i$ with probability $w_i / W$, independently of the earlier requests. The guarantee is in expectation: after $m$ requests, the count of backend $i$ is binomial with mean $m w_i / W$. The balancer reads no load information.

## The algorithm

WR-BUILD runs once, and again when the weights change. WR-PICK runs per request.

```pseudo id=main
WR-BUILD(w)                       ▷ integer weights w[0..n−1] ≥ 0 with a positive sum
L1  P[0] ← 0
L2  for i ← 0 to n − 1 do P[i + 1] ← P[i] + w[i]

WR-PICK(P, rng)                   ▷ P[0..n] from WR-BUILD
L3  r ← a uniform random integer in [0, P[n])
L4  lo ← 0; hi ← n − 1
L5  while lo < hi do
L6      mid ← ⌊(lo + hi) / 2⌋
L7      if P[mid + 1] > r then hi ← mid else lo ← mid + 1
L8  return lo
```

Backend $i$ owns the integers $P[i], \ldots, P[i+1] - 1$: there are exactly $w_i$ of them, and a backend of weight 0 owns none. Line L3 draws one of the $W$ integers, and lines L4 to L8 find the smallest $i$ with $P[i+1] > r$, which is the owner of $r$. This is the inversion method for a discrete distribution ([inverse transform sampling](/inverse-transform-sampling/)), with a binary search over the cumulative sums.

**The alias method.** Walker's method (1977) builds a table of $n$ columns. Column $i$ has a threshold $q_i \in [0, 1]$ and an alias $a_i$. A pick draws a column $i$ uniformly and a real $u \in [0, 1)$, and returns $i$ if $u < q_i$, else $a_i$. Vose (1991) gave an $O(n)$ construction that is also stable in floating point. The [alias method](/alias-method/) page has the construction and its proof; a balancer uses it unchanged, with the backends as the outcomes.

## Example

Four backends $a, b, c, d$ with weights 5, 1, 3, 1, so $W = 10$ and $P = [0, 5, 6, 9, 10]$.

| r | 0 to 4 | 5 | 6 to 8 | 9 |
|---|---|---|---|---|
| backend | a | b | c | d |

The search for $r = 6$: $lo = 0$, $hi = 3$. First $mid = 1$, and $P[2] = 6 > 6$ is false, so $lo = 2$. Then $mid = 2$, and $P[3] = 9 > 6$ is true, so $hi = 2$. Now $lo = hi = 2$, and the answer is $c$.

Vose's construction on the same weights scales them to $n w_i / W = 2, 0.4, 1.2, 0.4$ and gives the thresholds $q = (1, 2/5, 3/5, 2/5)$ and the aliases $(a, a, a, c)$. Then $a$ gets $\frac{1}{4}(1 + 3/5 + 2/5 + 2/5) = 1/2$, $b$ gets $\frac{1}{4} \cdot \frac{2}{5} = 1/10$, $c$ gets $\frac{1}{4}(3/5 + 3/5) = 3/10$ and $d$ gets $\frac{1}{4} \cdot \frac{2}{5} = 1/10$, which is $w_i / W$ in each case.

**A fit test.** With weights 5, 1, 3, 1, 10 and 100000 picks from `random.Random(seed)` for seeds 1, 2 and 3, Pearson's chi-square statistic against the expected counts was 4.25, 5.32 and 2.32 for the prefix-sum method and 10.18, 2.32 and 3.25 for the alias method. With 4 degrees of freedom, the 0.1 percent critical value is 18.47, so none of the six runs rejects the weights.

## Correctness

Lines L1 and L2 make $P[i] = \sum_{k<i} w_k$, so the integers $r$ with $P[i] \le r < P[i+1]$ number exactly $w_i$, and each $r \in [0, W)$ lies in exactly one such range. The loop of line L5 keeps the invariant $lo \le i^* \le hi$, where $i^*$ is the smallest index with $P[i^*+1] > r$: line L7 moves $hi$ down to $mid$ only when $P[mid+1] > r$, and moves $lo$ up past $mid$ only when $P[mid+1] \le r$. So the pick returns $i$ with probability $w_i / W$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Build.** Lines L1 and L2 take $\Theta(n)$ time and $\Theta(n)$ space.
- **Pick.** One random integer and at most $\lceil \lg n \rceil$ passes of the loop, so $\Theta(\log n)$ in the worst case. A linear scan of the running sums costs $O(n)$ and is faster for a few backends.
- **Alias method.** $\Theta(n)$ build and $\Theta(1)$ per pick, with two random numbers per pick.
- **Weight changes.** Both tables are rebuilt in $\Theta(n)$. If weights change often, a [Fenwick tree](/fenwick-tree/) over the weights gives $O(\log n)$ updates and $O(\log n)$ picks.
- **Coordination.** None: each balancer instance needs only its own random generator and a copy of the weights.

## Properties

- **Exact in distribution, not in counts.** The count of backend $i$ after $m$ requests is binomial with standard deviation $\sqrt{m p_i (1 - p_i)}$, $p_i = w_i / W$. With $m = 10000$ and $p_i = 0.1$ this is 30 requests, so a deviation of 1 percent of $m$ is normal. [Weighted round robin](/weighted-round-robin/) has deviation below one request at every moment.
- **Independent picks.** A backend can get several requests in a row, and runs of length $k$ appear with probability $p_i^k$. This is the price of having no shared state.
- **Zero weight.** A backend of weight 0 is never picked, which gives a simple way to drain a backend.
- **Same maximum load as one random choice.** With equal weights it is [random load balancing](/random-load-balancing/), so with $n$ requests on $n$ backends the busiest one has about $\ln n / \ln \ln n$ requests (see [balls into bins](/balls-into-bins-max-load/)).

## Variants and improvements

- **Float weights.** Draw $r$ uniform in $[0, W)$ as a real and search the same way. Rounding can make a backend of tiny weight unreachable or give it a slightly wrong share.
- **Weighted [power of two choices](/power-of-two-choices/).** Draw two backends by weight and send the request to the one with less load. This keeps most of the low maximum load of two choices.
- **Lottery scheduling.** [Lottery scheduling](/lottery-scheduling/) makes the same draw, with tickets as weights, to give CPU quanta to processes. Weighted random load balancing is the request-routing analogue: the prize is one request for one server instead of one time slice of one CPU, and there is no preemption. In the same way, [weighted round robin](/weighted-round-robin/) is the analogue of [stride scheduling](/stride-scheduling/), the deterministic counterpart of lottery scheduling.
- **Weighted hashing.** A balancer that must send the same key to the same backend uses a hash of the key in place of $r$, or a weighted form of [rendezvous hashing](/rendezvous-hashing/).

## When to use it

Use weighted random choice when many independent clients or proxies spread requests over the same backends, each without shared state, for example a client library in each of thousands of processes. Over the many requests of all clients the shares are close to the weights. Use [weighted round robin](/weighted-round-robin/) when one balancer handles the traffic and an exact share over short windows matters. Use a load-aware policy such as [weighted least connections](/weighted-least-connections/) or [power of two choices](/power-of-two-choices/) when request costs vary.

## Pitfalls

- **Comparing with ≥ in line L7.** The test $P[mid+1] \ge r$ finds the first $i$ with $P[i+1] \ge r$, which gives $r = P[i+1]$ to backend $i$ instead of the next backend of positive weight. With weights 0, 1 the backend of weight 0 then gets $r = 0$, and in general the shares are off by one value of $r$ each. Line L7 must use $>$.
- **A draw in $[0, W]$.** If line L3 can return $W$, no backend owns it, and the search returns the last backend, which then gets one extra value. Draw from the half-open range $[0, W)$.
- **Modulo bias.** Taking a 32-bit random number modulo $W$ makes small values of $r$ slightly more likely when $W$ does not divide $2^{32}$. Use an unbiased bounded draw, such as Python's `randrange`.
- **One shared generator.** Many balancer instances that seed their generators with the same value make the same picks. Seed each instance differently.
- **A table that is not rebuilt.** After a weight change or a [health check](/health-checking/) failure, both $P$ and the alias table are stale until rebuilt. A backend that is down but still in the table keeps its share of requests.

## Implementations

## History

The alias method is due to Walker (1974 and 1977), and the stable linear-time construction to Vose (1991). Devroye's book of 1986 treats both the table search and the alias method for discrete distributions. Waldspurger and Weihl used the same weighted draw for CPU time in lottery scheduling (1994).

## References
