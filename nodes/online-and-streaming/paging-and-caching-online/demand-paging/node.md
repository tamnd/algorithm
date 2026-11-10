---
tag: Q397H4
kind: concept
slug: demand-paging
name: Demand paging
aliases:
- on-demand fetching
- lazy paging
area: online-and-streaming/paging-and-caching-online
level: intro
summary: Bringing a page into the cache only when a request for it causes a fault.
prereqs: [paging-problem, page-fault]
see_also: [belady-optimality, flush-when-full, prefetching, k-server-problem, marking-algorithm, belady-algorithm]
sources:
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 3 (demand paging algorithms and the reduction of any paging algorithm to a demand paging one)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design, Addison-Wesley, 2006
    locator: Section 4.3, Optimal caching (reduced schedules, and the proof that each schedule can be made reduced without more misses)
  - paper: doi:10.1147/sj.52.0078
    title: "L. A. Belady, A study of replacement algorithms for a virtual-storage computer, IBM Systems Journal 5(2) (1966), 78-101"
    locator: the virtual storage model in which pages are loaded on demand
---

Demand paging is the rule that a paging algorithm changes its cache only on a [page fault](/page-fault/): it loads the requested page and nothing else, and it evicts a page only when the cache is full. Each paging algorithm, online or offline, can be turned into a demand paging algorithm that loads no more pages on any request sequence. So in the [paging problem](/paging-problem/) one may assume demand paging with no loss, and the cost is the number of faults.

## In plain words

A paging algorithm could load pages early, before anyone asks for them, or throw pages out before it needs the room. Demand paging forbids both. It waits until a request finds the page missing, then loads that one page, and makes room only if the memory is full.

Waiting never hurts when each load costs the same. The idea of the proof: copy the eager algorithm, but delay each of its loads until the page is actually requested. A delayed load either happens later or never happens. To make room, throw out a page that the eager algorithm has already thrown out. Then each load of the lazy copy can be paid for by a different load of the eager algorithm.

## The idea

**The general model.** A *paging algorithm* $A$ with cache size $k$ keeps a cache $C^A_t$ of at most $k$ pages after request $t$, with $\sigma_t \in C^A_t$. Between requests it may load and evict any pages. Its cost $A(\sigma)$ is the number of loads. The algorithm is *online* if $C^A_t$ depends only on $\sigma_1, \ldots, \sigma_t$.

**Demand paging.** An algorithm $D$ is a *demand paging* algorithm if, at each request $t$: when $\sigma_t \in C^D_{t-1}$, then $C^D_t = C^D_{t-1}$; when $\sigma_t \notin C^D_{t-1}$, then $C^D_t = C^D_{t-1} \cup \{\sigma_t\}$ if $|C^D_{t-1}| < k$, and $C^D_t = C^D_{t-1} \setminus \{q\} \cup \{\sigma_t\}$ for one page $q$ if $|C^D_{t-1}| = k$. Its cost is its number of faults.

**Theorem.** Let $A$ be a paging algorithm with cache size $k$ and initial cache $C_0$. Define $D$ with the same initial cache $C^D_0 = C_0$ as follows. At request $t$, if $\sigma_t \in C^D_{t-1}$, do nothing. Otherwise load $\sigma_t$, and if $|C^D_{t-1}| = k$, evict any page $q \in C^D_{t-1} \setminus C^A_t$. Then $D$ is a demand paging algorithm, $D$ is online if $A$ is online, and $D(\sigma) \le A(\sigma)$ for every sequence $\sigma$.

*Proof.* **The eviction exists.** Let $\sigma_t \notin C^D_{t-1}$ and $|C^D_{t-1}| = k$. If $C^D_{t-1} \subseteq C^A_t$, then $C^A_t$ contains the $k$ pages of $C^D_{t-1}$ and also $\sigma_t$, which is not one of them. So $|C^A_t| \ge k + 1$, which is false. So $C^D_{t-1} \setminus C^A_t$ is not empty.

**Demand paging and online.** By its definition, $D$ changes its cache only on a fault, loads only $\sigma_t$, and evicts one page only when its cache is full. Its choice at request $t$ uses $C^A_t$ and $C^D_{t-1}$, which depend only on $\sigma_1, \ldots, \sigma_t$ when $A$ is online.

**The charging.** Each fault of $D$ at time $t$ loads the page $p = \sigma_t$. Charge it to the last load of $p$ by $A$ at a time $s \le t$. Such a load exists. At time $t$ the page $p$ is in $C^A_t$. If $p \notin C_0$, then $A$ loaded $p$ at some time at most $t$. If $p \in C_0$, then $D$ also started with $p$, and because $p \notin C^D_{t-1}$, $D$ evicted $p$ at some time $r < t$. At time $r$ the rule of $D$ gives $p \notin C^A_r$, while $p \in C^A_t$, so $A$ loaded $p$ at a time in $(r, t]$.

**The charging is one to one.** Two faults of $D$ that load different pages are charged to loads of different pages. Let $D$ load the same page $p$ at times $t_1 < t_2$. Between them $D$ evicted $p$, at a time $r$ with $t_1 < r < t_2$. As above, $p \notin C^A_r$ and $p \in C^A_{t_2}$, so $A$ loaded $p$ at a time in $(r, t_2]$. So the last load of $p$ by $A$ at or before $t_2$ is after $r > t_1$, and it is not the last load of $p$ at or before $t_1$. So distinct faults of $D$ are charged to distinct loads of $A$, and $D(\sigma) \le A(\sigma)$. $\blacksquare$

**Remarks.**

- The proof works for each fixed $\sigma$, so it also holds for offline algorithms. For a randomized algorithm, apply it to each fixed value of the random bits.
- The choice of $q$ inside $C^D_{t-1} \setminus C^A_t$ is free. The bound holds for each choice.
- If $A$ is already a demand paging algorithm with $C^A$ equal to $C^D$ up to time $t - 1$, the set $C^D_{t-1} \setminus C^A_t$ is exactly the page that $A$ evicts at time $t$. So the construction does not change a demand paging algorithm. The [proof of Belady's theorem](/belady-optimality/) uses this fact.
- For [weighted paging](/weighted-paging-problem/) and for the [$k$-server problem](/k-server-problem/), the same idea gives *lazy* algorithms: move a server only to serve a request. The triangle inequality replaces the count of loads.

## Examples

**Flush when full is not demand paging.** [Flush when full](/flush-when-full/) (FWF) evicts all $k$ pages on a fault with a full cache. Take $k = 3$ and $\sigma = 1\,2\,3\,4\,1\,2$. FWF loads 1, 2, 3, then on request 4 it empties the cache and loads 4, then it loads 1 and 2 again. It has 6 faults.

Now build $D$ from FWF. On request 4, $C^D_3 = \{1, 2, 3\}$ and $C^{\mathrm{FWF}}_4 = \{4\}$, so $D$ may evict any of 1, 2 or 3.

| rule for $q$ | evicted at $t = 4$ | then | faults of $D$ |
|---|---|---|---|
| the smallest page in $C^D \setminus C^A$ | 1 | on request 1, $C^D \setminus C^A = \{2, 3\}$, evict 2; on request 2, evict 3 | 6 |
| the largest page in $C^D \setminus C^A$ | 3 | requests 1 and 2 are hits | 4 |

Both satisfy $D \le 6$, as the theorem says. The second one equals the optimum, which is 4 here.

**Prefetching.** An algorithm that loads page $b$ at the same time as page $a$, because it guesses that $b$ comes next, pays for two loads. Its demand version loads $b$ only when $b$ is requested. If $b$ is never requested, the demand version saves one load. If $b$ is requested, the demand version pays for $b$ then, and the two counts are equal. In real systems [prefetching](/prefetching/) still helps, because it hides latency or reads many pages in one disk access, and the unit cost model does not count either effect.

## Where it is used

- **Optimal offline paging.** The [proof of Belady's theorem](/belady-optimality/) changes an optimal schedule step by step, and it uses this conversion to keep each new schedule a demand paging one.
- **Competitive analysis.** Lower bounds such as the [deterministic bound $k$](/online-caching-lower-bound/) and the [harmonic bound](/harmonic-paging-bound/) may assume that the online algorithm is a demand paging algorithm, because the conversion keeps it online and does not raise its cost.
- **Marking algorithms.** [Flush when full](/flush-when-full/) is a [marking algorithm](/marking-algorithm/) that is not demand paging. Its demand version is again a marking algorithm with at most the same number of faults.
- **The $k$-server problem.** Lazy algorithms for the [$k$-server problem](/k-server-problem/) and for [weighted paging](/weighted-paging-problem/) come from the same argument.
- **Operating systems.** Demand paging is the standard policy of virtual memory: a page is read from disk on a page fault. Many systems add read-ahead, which the remark on prefetching explains.

## References
