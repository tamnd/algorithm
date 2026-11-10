---
title: Randomized marking is a marking algorithm and is 2H_k-competitive against an oblivious adversary
proves: [correctness]
status: full
---

We use the pseudocode of the page, with an empty initial cache, and a fixed sequence $\sigma$ (the adversary is oblivious). The [phases](/marking-phases/) of $\sigma$ are defined greedily: a new phase starts at the first request that would make the current phase contain $k + 1$ distinct pages. Let $N$ be the number of phases and let $D_i$ be the set of distinct pages of phase $i$. A page of $D_i$ is *new* if $i = 1$ or the page is not in $D_{i-1}$, and *stale* otherwise. Let $m_i$ be the number of new pages of phase $i$.

**Claim 1.** On every run, $U$ is the set of cached pages not yet requested in the current phase, line L7 runs exactly at the first request of each phase after the first, and the algorithm never evicts a page requested earlier in the current phase.

*Proof.* Write $M = C \setminus U$. Line L10 adds $p$ to $C$ but not to $U$, line L11 removes $p$ from $U$, and line L9 removes $q$ from both, so $U \subseteq C$ and $p \in M$ after each request. Line L7 sets $U = C$, so $M = \emptyset$ before line L10. These are the steps of the marking pseudocode of the [marking algorithm](/marking-algorithm/) page, with CHOOSE a uniform random choice: "$M = C$" there is "$U = \emptyset$" here. The proof of Claim 2 of that page applies to every run, so $M$ is the set of distinct pages requested so far in the current phase, and line L7 runs exactly at the phase starts. Line L8 picks from $U$, so it never evicts a page of $M$. $\square$

So each run is a valid demand paging schedule, with at most $k$ faults per phase.

**Claim 2.** At the start of phase $i \ge 2$, just before line L7 runs, the cache is $D_{i-1}$, and all its pages become unmarked.

*Proof.* Phase $i - 1$ is complete, so $|D_{i-1}| = k$. By Claim 1, just before the first request of phase $i$, $M = D_{i-1}$, and $M \subseteq C$ with $|C| \le k$, so $C = D_{i-1}$. Line L7 then sets $U = C$. $\square$

**Claim 3.** For each phase $i$, the expected number of faults in phase $i$ is at most $m_i (1 + H_k - H_{m_i}) \le m_i H_k$.

*Proof.* For $i = 1$, the cache starts empty, all $m_1 = |D_1| \le k$ pages are new, and by Claim 1 each faults exactly once in the phase, so the phase has $m_1 \le m_1 H_k$ faults. Let $i \ge 2$. By Claim 1, a fault in phase $i$ can happen only at the first request in the phase for a page, and later requests in the phase are hits.

*New pages.* A new page $p$ is not in $D_{i-1}$, so by Claim 2 it is not in the cache at the start of the phase. Only requested pages are loaded during the phase. So $p$ faults at its first request in the phase, once.

*Stale pages.* Let $T$ be the set of stale pages not yet requested in the phase, and let $R = T \cap C$ be those of them that are cached. By Claim 1, $U = R$ at each moment of the phase after line L7: the unmarked cached pages are exactly the cached pages of $D_{i-1}$ not yet requested. We show by induction over the events of the phase: given the number $r = |R|$, the set $R$ is a uniform random subset of $T$ of size $r$, and $r$ is a fixed number, since $\sigma$ is fixed.

- At the start, after line L7, $R = T = D_{i-1}$, which is the only subset of size $k$.
- A first request for a new page faults and evicts a uniform random element of $U = R$. A uniform random subset of size $r$, minus a uniform random element of it, is a uniform random subset of size $r - 1$.
- A first request for a stale page $s \in T$: if $s \in R$, it is a hit and $s$ leaves $R$ and $T$; if $s \notin R$, it is a fault, a uniform random element of $R$ is evicted, and $s$ leaves $T$. In both cases the new $R$ is a uniform random subset of $T \setminus \{s\}$ of size $r - 1$. Indeed, given $s \in R$, the set $R \setminus \{s\}$ is uniform among the subsets of $T \setminus \{s\}$ of size $r - 1$; given $s \notin R$, the set $R$ is uniform among the subsets of $T \setminus \{s\}$ of size $r$, and removing a uniform random element gives a uniform subset of size $r - 1$. A mixture of two copies of the same uniform distribution is that distribution.
- Other requests change nothing.

Each new page decreases $r$ by 1 and does not change $T$. Each stale first request decreases both $|T|$ and $r$ by 1. So at the first request of the $j$-th distinct stale page, after $\ell$ new pages, $|T| = k - j + 1$ and $r = k - (j - 1) - \ell$. The page $s \in T$ is fixed and $R$ is a uniform $r$-subset of $T$, so

$$\Pr[s \notin R] = 1 - \frac{r}{|T|} = \frac{\ell}{k - j + 1} \le \frac{m_i}{k - j + 1}.$$

Phase $i$ has at most $k - m_i$ stale pages. By [linearity of expectation](/linearity-of-expectation/), the expected faults in phase $i$ are at most

$$m_i + \sum_{j=1}^{k - m_i} \frac{m_i}{k - j + 1} = m_i + m_i \left(H_k - H_{m_i}\right).$$

Since a phase $i \ge 2$ starts with a page outside $D_{i-1}$, $m_i \ge 1$, so $H_{m_i} \ge 1$ and the bound is at most $m_i H_k$. $\square$

**Claim 4.** $\mathrm{OPT}(\sigma) \ge \frac{1}{2} \sum_{i=1}^{N} m_i$.

*Proof.* Let $\mathrm{OPT}_i$ be the faults of an optimal schedule in phase $i$. Phase 1 has $m_1$ distinct pages and the cache starts empty, so $\mathrm{OPT}_1 \ge m_1$. For $i \ge 2$, phases $i - 1$ and $i$ together request the $k$ pages of $D_{i-1}$ and the $m_i$ new pages of phase $i$, so $k + m_i$ distinct pages. Before phase $i - 1$, the optimal cache holds at most $k$ pages, so at least $m_i$ of these pages are missing at their first request in the two phases, and $\mathrm{OPT}_{i-1} + \mathrm{OPT}_i \ge m_i$. Adding these $N$ inequalities counts each $\mathrm{OPT}_i$ at most twice, so $\sum_i m_i \le 2\,\mathrm{OPT}(\sigma)$. $\square$

**Theorem.** For every fixed $\sigma$, $\mathbb{E}[\mathrm{MARK}(\sigma)] \le 2H_k \cdot \mathrm{OPT}(\sigma)$.

*Proof.* By Claim 3 and linearity of expectation, $\mathbb{E}[\mathrm{MARK}(\sigma)] \le H_k \sum_i m_i$, and by Claim 4 this is at most $2H_k \cdot \mathrm{OPT}(\sigma)$. $\blacksquare$
