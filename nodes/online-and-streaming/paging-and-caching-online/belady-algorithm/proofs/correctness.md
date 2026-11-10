---
title: BELADY evicts the page with the furthest next request, and this gives the optimum
proves: [correctness]
status: full
---

We use the pseudocode of the page. Positions run from 1 to $n$, and $\infty$ is larger than each position. For a time $t$ and a page $q$, $\mathrm{next}_t(q)$ is the smallest $s > t$ with $\sigma_s = q$, or $\infty$. Line L1 sets $next[t] = \mathrm{next}_t(\sigma_t)$. The rule LFD is: on a fault with a full cache at time $t$, evict a page $q \in C$ with the largest $\mathrm{next}_t(q)$.

**Claim 1.** BELADY is a demand paging algorithm that follows the rule LFD.

*Proof.* Demand paging is clear from lines L5 to L10: the cache changes only on a fault, it gains only $\sigma_t$, and it loses one page only when it is full. For the rule, we prove this invariant $I(t)$, which holds after line L11 of iteration $t$, and for $t = 0$ after line L2.

- (a) For each $q \in C$, $key[q] = \mathrm{next}_t(q)$, and the pair $(key[q], q)$ is in $H$. Call it the current pair of $q$.
- (b) Each other pair in $H$ has a key of at most $t$.

$I(0)$ holds because $C$ and $H$ are empty. Assume $I(t)$ and look at request $t + 1$ with $p = \sigma_{t+1}$.

*The eviction.* Let $p \notin C$ and $|C| = k$. For each $q \in C$ we have $q \ne p$, so $\mathrm{next}_t(q) \ne t + 1$ and $\mathrm{next}_t(q) \ge t + 2$. Also $\mathrm{next}_{t+1}(q) = \mathrm{next}_t(q)$. By (a) and (b), each current pair has a key greater than $t + 1$ and each other pair has a key of at most $t$. Since $k \ge 1$, $C$ is not empty, so the first pair that line L8 pops is the current pair of a page $q \in C$ with the largest $\mathrm{next}_{t+1}(q)$. The test of line L8 accepts it, and line L9 evicts $q$. This is the rule LFD. After the pop, $q$ has no pair with a key greater than $t$: each earlier pair of $q$ was pushed at an earlier request $s$ of $q$, with the key $\mathrm{next}_s(q)$, which is at most the last request of $q$, so at most $t$.

*The update.* Line L11 sets $key[p] = \mathrm{next}_{t+1}(p)$ and pushes the new current pair of $p$. If $p$ was in $C$ before, its old current pair has the key $\mathrm{next}_t(p) = t + 1$, so it now satisfies (b). Each other page $q$ in $C$ keeps its pair, with $\mathrm{next}_{t+1}(q) = \mathrm{next}_t(q)$. Each other pair had a key of at most $t$. So $I(t + 1)$ holds.

By induction, each eviction of BELADY follows the rule LFD. $\square$

**Claim 2.** Each demand paging schedule that follows the rule LFD has $\mathrm{OPT}(\sigma)$ faults.

*Proof.* We show the exchange step of [Belady's optimality theorem](/belady-optimality/). Two schedules *agree up to $i$* if they make the same choices on requests $1, \ldots, i$, so they have the same cache after request $i$.

*Step.* Let $S$ be a demand paging schedule that agrees with LFD up to $i$. We build a demand paging schedule $S'$ that agrees with LFD up to $i + 1$, with $S'(\sigma) \le S(\sigma)$. Let $t = i + 1$. If $S$ and LFD make the same choice at $t$, take $S' = S$. Otherwise $t$ is a fault with a full cache $C$, $S$ evicts $u$ and LFD evicts $v \ne u$. By the rule, $\mathrm{next}_t(u) \le \mathrm{next}_t(v)$, and since two pages have different finite next requests, $\mathrm{next}_t(u) < \mathrm{next}_t(v)$ or both are $\infty$.

Let $A$ be the schedule that evicts $v$ at $t$ and then copies $S$ as follows. After request $t$, the caches are $X \cup \{v\}$ for $S$ and $X \cup \{u\}$ for $A$, with $X = (C \setminus \{u, v\}) \cup \{\sigma_t\}$. While the caches differ in this way, at a request $s > t$:

- if $\sigma_s \in X$, both hit;
- if $\sigma_s \notin X \cup \{u, v\}$, both fault; if $S$ evicts $v$, then $A$ evicts $u$ and the caches become equal; if $S$ evicts $w \in X$, then $A$ evicts $w$ and the caches still differ in the same way;
- $\sigma_s = v$ cannot happen before the first request of $u$ after $t$, because $\mathrm{next}_t(u) < \mathrm{next}_t(v)$ or neither page comes again;
- if $\sigma_s = u$, then $S$ faults and $A$ hits; if $S$ evicts $v$, the caches become equal; if $S$ evicts $w \in X$, then $A$ loads $v$ and evicts $w$, at a cost of 1, and the caches become equal.

When the caches are equal, $A$ makes the same choices as $S$. At each request, $A$ pays at most what $S$ pays, so $A(\sigma) \le S(\sigma)$. The schedule $A$ may load $v$ without a request, so it may not be demand paging. Apply the conversion of the [demand paging](/demand-paging/) page to $A$ and call the result $S'$. Then $S'(\sigma) \le A(\sigma)$. Up to $i$, $A$ is demand paging and $S'$ makes the same choices. At $t$, $S'$ must evict a page of $C \setminus C^A_t = \{v\}$, so $S'$ evicts $v$. So $S'$ agrees with LFD up to $i + 1$.

*Induction.* By the demand paging conversion, there is an optimal schedule $S_0$ that is demand paging, with $S_0(\sigma) = \mathrm{OPT}(\sigma)$. It agrees with LFD up to $0$. Apply the step $n$ times. The result agrees with LFD up to $n$, so it is the LFD schedule, and its cost is at most $\mathrm{OPT}(\sigma)$. So the LFD schedule is optimal. $\square$

By Claims 1 and 2, BELADY returns $\mathrm{OPT}(\sigma)$. $\blacksquare$
