---
tag: VBTJB9
kind: theorem
slug: belady-optimality
name: Belady's optimality theorem
aliases:
- MIN optimality
- Optimality of Bélády's algorithm
- optimality of MIN
- optimality of LFD
- optimality of furthest in the future
area: online-and-streaming/paging-and-caching-online
level: intro
summary: Evicting the page whose next request is farthest in the future minimizes the number of faults.
prereqs: [belady-algorithm, demand-paging, exchange-argument]
see_also: [paging-problem, belady-optimal, greedy-stays-ahead, stack-algorithms, weighted-paging-problem, online-caching-lower-bound, competitive-ratio]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 4.3, Optimal caching, the proof that the Farthest-in-Future schedule is optimal by an exchange argument
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3, Section 3.4, the optimality of LFD
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the rule MIN, used as the optimum in the simulations
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: the optimal replacement algorithm OPT and its proof of optimality among stack algorithms
---

Belady's optimality theorem says that, for the [paging problem](/paging-problem/) with unit costs, the rule "on a fault with a full cache, evict the page whose next request is furthest in the future" has the fewest faults on every request sequence. The rule is [Belady's algorithm](/belady-algorithm/), also called MIN or LFD. The standard proof is an [exchange argument](/exchange-argument/): an optimal schedule that differs from the rule can be changed, one step at a time, to agree with it without more faults. The theorem makes $\mathrm{OPT}(\sigma)$ easy to compute, and so it is the base of the [competitive analysis](/competitive-ratio/) of paging.

## Statement

A *paging algorithm* with cache size $k$ keeps a cache of at most $k$ pages, holds $\sigma_t$ after request $t$, and pays 1 for each page that it loads, as in the general model of [demand paging](/demand-paging/). For a time $t$ and a page $q$, let $\mathrm{next}_t(q)$ be the smallest $s > t$ with $\sigma_s = q$, or $\infty$ if there is none. The schedule LFD is the demand paging schedule that, on a fault at time $t$ with a full cache $C$, evicts a page $q \in C$ with the largest $\mathrm{next}_t(q)$. Ties are broken by any fixed rule.

**Theorem.** Let $k \ge 1$, let $C_0$ be an initial cache with $|C_0| \le k$, and let $\sigma$ be a request sequence. Then LFD with initial cache $C_0$ loads at most as many pages on $\sigma$ as each paging algorithm with cache size $k$ and initial cache $C_0$. So $\mathrm{LFD}(\sigma) = \mathrm{OPT}(\sigma)$.

The comparison includes offline algorithms, algorithms that load pages early, and algorithms that evict pages early.

## In plain words

Suppose you must throw out a page, and you can see the future. Look at when each page in the cache is needed next, and throw out the one needed last.

Why is this safe? Take any other plan that throws out a different page, one that is needed sooner. Change that plan in one place: throw out the page needed last instead. The changed plan holds one different page. The page it kept comes back first, so the changed plan wins a hit there, and it can then take the other page back at most at the cost the old plan paid. So the change never costs more. Repeat this at each decision and the plan becomes the furthest in the future rule, never getting worse.

## Proof

Two schedules *agree up to $i$* if they make the same choices on requests $1, \ldots, i$, so they have the same cache after request $i$.

**Step.** Let $S$ be a demand paging schedule that agrees with LFD up to $i$, and let $t = i + 1$. Then there is a demand paging schedule $S'$ that agrees with LFD up to $t$, with $S'(\sigma) \le S(\sigma)$.

*Proof of the step.* If $S$ and LFD make the same choice at $t$, take $S' = S$. Otherwise $t$ is a fault with a full cache $C$, and $S$ evicts $u$ while LFD evicts $v \ne u$. By the rule, $\mathrm{next}_t(u) \le \mathrm{next}_t(v)$. Two different pages have different finite next requests, so $\mathrm{next}_t(u) < \mathrm{next}_t(v)$, or neither page is requested again.

Let $A$ be the schedule that evicts $v$ at $t$ and then follows $S$ in this way. Let $X = (C \setminus \{u, v\}) \cup \{\sigma_t\}$. After request $t$, the cache of $S$ is $X \cup \{v\}$ and the cache of $A$ is $X \cup \{u\}$. While the two caches differ in this way, look at a request $s > t$.

1. If $\sigma_s \in X$, both hit.
2. If $\sigma_s \notin X \cup \{u, v\}$, both fault. If $S$ evicts $v$, $A$ evicts $u$, and the caches become equal. If $S$ evicts $w \in X$, $A$ evicts $w$, and the caches still differ only in $u$ and $v$.
3. $\sigma_s = v$ cannot happen while no request for $u$ has come after $t$, because $u$ comes back before $v$, or neither comes back.
4. If $\sigma_s = u$, $S$ faults and $A$ hits. If $S$ evicts $v$, the caches become equal. If $S$ evicts $w \in X$, $A$ loads $v$ and evicts $w$, at a cost of 1, and the caches become equal.

Once the caches are equal, $A$ makes the same choices as $S$. At each request $A$ pays at most what $S$ pays, so $A(\sigma) \le S(\sigma)$.

In case 4, $A$ loads $v$ with no request for $v$, so $A$ need not be demand paging. Let $S'$ be the demand paging schedule that the conversion of the [demand paging](/demand-paging/) page builds from $A$, with the same initial cache. Then $S'(\sigma) \le A(\sigma)$. Up to $i$, $A$ is a demand paging schedule and $S'$ makes the same choices. At $t$, the conversion evicts a page of $C \setminus C^A_t = \{v\}$, so $S'$ evicts $v$. So $S'$ agrees with LFD up to $t$.

**Induction.** The number of loads is a non-negative integer, so some paging algorithm $S^*$ has the least number of loads, $\mathrm{OPT}(\sigma)$. The conversion gives a demand paging schedule $S_0$ with $S_0(\sigma) \le S^*(\sigma)$, so $S_0$ is also optimal. It agrees with LFD up to $0$. Apply the step $n$ times, for $i = 0, 1, \ldots, n - 1$. Each schedule costs at most the one before, and the last one agrees with LFD on all $n$ requests, so it is LFD. So $\mathrm{LFD}(\sigma) \le S_0(\sigma) = \mathrm{OPT}(\sigma)$, and equality holds because $\mathrm{OPT}$ is the least cost. $\blacksquare$

## Consequences

- **OPT is easy to compute.** [Belady's algorithm](/belady-algorithm/) computes $\mathrm{OPT}(\sigma)$ in $O(n \log n)$ time with a heap. So the offline side of the [competitive ratio](/competitive-ratio/) of paging is concrete, and proofs of upper and lower bounds may use the structure of LFD. The [deterministic lower bound $k$](/online-caching-lower-bound/) uses the fact that LFD faults at most once in each $k$ requests on the adversary sequence.
- **Each tie rule is optimal.** The theorem holds for each fixed tie rule, so the choice among pages that are never requested again does not change the cost.
- **Demand paging is enough.** Together with the conversion of [demand paging](/demand-paging/), the theorem shows that loading pages early never helps with unit costs, even offline.
- **One pass for all cache sizes.** LFD is a [stack algorithm](/stack-algorithms/), so the optimal fault count for every cache size comes from one pass over the trace.
- **The online gap.** No online algorithm can know $\mathrm{next}_t(q)$. Online rules such as [LRU](/lru/) use the time since the last request as a guess of the time to the next request, and the guess can be wrong by a factor of $k$ (see the [Sleator and Tarjan bound](/sleator-tarjan-paging-bound/)).

## Tightness

**LFD is not the only optimal schedule.** Take $k = 2$ and $\sigma = 1\,2\,3\,1\,2$. At request 3 the cache is $\{1, 2\}$, with $\mathrm{next}(1) = 4$ and $\mathrm{next}(2) = 5$, so LFD evicts 2 and has 4 faults. The schedule that evicts 1 instead faults on 1, evicts 3, and hits on 2, so it also has 4 faults. So the theorem gives one optimal schedule, not all of them.

**The rule is not optimal with costs.** Let each page have a load cost, as in [weighted paging](/weighted-paging-problem/). Take $k = 2$, a cost of 10 for page $a$ and 1 for pages $b$ and $c$, and $\sigma = a\,b\,c\,b\,a$. At request $c$, LFD evicts $a$, which comes back last, and later pays 10 again: a total of $10 + 1 + 1 + 10 = 22$. Evicting $b$ instead costs $10 + 1 + 1 + 1 = 13$, with the eviction of $c$ at the second request for $b$. Case 4 of the proof fails here: the late load of $v$ can cost more than the load that $S$ makes. Offline weighted paging is solved by min-cost flow instead. With pages of different sizes, the offline problem is NP-hard.

**Online rules are not optimal.** On the same $\sigma = 1\,2\,3\,4\,1\,2\,5\,1\,2\,3$ with $k = 3$, LFD has 6 faults and LRU has 8. On the cycle of $k + 1$ pages, LRU faults on each request while LFD faults at most once in each $k$ requests, so the factor $k$ between them is reached.

## History

Belady introduced the rule MIN in 1966, in an IBM study that compared replacement algorithms for virtual storage by simulation, and he used MIN as the optimum. Mattson, Gecsei, Slutz and Traiger (1970) gave a proof of the optimality of the rule, which they called OPT, in their work on stack algorithms. The exchange argument above follows the form of Kleinberg and Tardos (2006), who use optimal caching as a main example of the method, and Borodin and El-Yaniv (1998) give a proof of the same kind for LFD.

## References
