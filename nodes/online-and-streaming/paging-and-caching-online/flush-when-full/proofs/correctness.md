---
title: FWF faults once per distinct page of each phase, so it is k-competitive and the worst marking algorithm
proves: [correctness]
status: full
---

We use the pseudocode of the page, with an empty initial cache. The [phases](/marking-phases/) of $\sigma$ for the size $k$ are defined greedily: phase 1 starts at request 1, and a new phase starts at the first request that would make the current phase contain $k + 1$ distinct pages. Let $N$ be the number of phases and $d_i$ the number of distinct pages of phase $i$, so $d_i = k$ for $i < N$ and $1 \le d_N \le k$.

**Claim 1.** After each request $t$, $C$ is the set $P_t$ of distinct pages requested from the start of the current phase up to $t$. Line L7 runs exactly at the first request of each phase after the first.

*Proof.* By induction on $t$. Before request 1, $C = \emptyset$. Assume $C = P_{t-1}$ after request $t - 1$, and let $p = \sigma_t$.

- If request $t$ starts a new phase, then $|P_{t-1}| = k$ and $p \notin P_{t-1}$. So $p \notin C$ and $|C| = k$, line L7 runs, and line L8 gives $C = \{p\} = P_t$.
- Otherwise $p \in P_{t-1}$, or $|P_{t-1}| < k$. In the first case $p \in C$ and nothing changes, and $P_t = P_{t-1}$. In the second case $|C| < k$, so line L7 does not run, and line L8 gives $C = P_{t-1} \cup \{p\} = P_t$. $\square$

So $|C| \le k$ always, and $\sigma_t \in C$ after request $t$. The schedule is valid.

**Claim 2.** $\mathrm{FWF}(\sigma) = \sum_{i=1}^{N} d_i \le kN$.

*Proof.* By Claim 1, request $t$ is a fault exactly when $\sigma_t \notin P_{t-1}$ inside the current phase, or when $t$ starts a phase. In both cases $\sigma_t$ is requested for the first time in its phase. So the faults are exactly the first requests of each page in each phase, and there are $d_i$ of them in phase $i$. $\square$

**Claim 3.** Each paging algorithm with an empty initial cache loads at least $N$ pages on $\sigma$.

*Proof.* Let phase $i$ start at request $a_i$, with $p_i = \sigma_{a_i}$. For $1 \le i < N$, the window $W_i$ of requests $a_i + 1, \ldots, a_{i+1}$ requests the $k - 1$ pages of phase $i$ other than $p_i$, and the page $\sigma_{a_{i+1}}$, which is not in phase $i$. These are $k$ distinct pages other than $p_i$. After request $a_i$ the cache holds $p_i$, so at most $k - 1$ of them are cached, and the algorithm must load one of them during $W_i$. The windows are disjoint, and request 1 needs one more load. $\square$

**Claim 4.** Each marking algorithm $\mathrm{ALG}$ has $\mathrm{ALG}(\sigma) \le \mathrm{FWF}(\sigma)$.

*Proof.* A marking algorithm never evicts a page that was requested earlier in the current phase, so it faults at most once for each distinct page of each phase, at most $d_i$ times in phase $i$. By Claim 2, FWF faults exactly $d_i$ times. $\square$

**Theorem.** $\mathrm{FWF}(\sigma) \le k \cdot \mathrm{OPT}(\sigma)$ for every $\sigma$.

*Proof.* By Claims 2 and 3, $\mathrm{FWF}(\sigma) \le kN \le k \cdot \mathrm{OPT}(\sigma)$. $\blacksquare$
