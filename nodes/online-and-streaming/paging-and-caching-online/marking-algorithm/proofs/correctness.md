---
title: Each marking algorithm is a valid demand paging rule and is k-competitive
proves: [correctness]
status: full
---

We use the pseudocode of the page, with an empty initial cache. The [phases](/marking-phases/) of $\sigma$ for the size $k$ are defined greedily: phase 1 starts at request 1, and a new phase starts at the first request that would make the current phase contain $k + 1$ distinct pages. Let $N$ be the number of phases.

**Claim 1.** The pseudocode is well defined: at line L8 the set $C \setminus M$ is not empty. Also $|C| \le k$ always holds.

*Proof.* First, $M \subseteq C$ holds after each line. It holds at line L1. Line L11 adds $p$ to $M$, and $p \in C$ there, because $p$ was in $C$ or line L10 just added it. Line L9 removes from $C$ a page $q \notin M$. Line L7 only makes $M$ smaller. Now at line L8, $|C| = k \ge 1$. If $M \ne C$ before line L7, then $M \subsetneq C$, so $C \setminus M \ne \emptyset$. If $M = C$, line L7 sets $M = \emptyset$ and $C \setminus M = C \ne \emptyset$. For the size: line L10 adds one page, and when $|C| = k$ line L9 has removed one page first. $\square$

**Claim 2.** After each request $t$, $M$ is the set of distinct pages requested from the start of the current phase up to $t$. Line L7 empties $M$ exactly at the first request of each phase after the first.

*Proof.* By induction on $t$. Before request 1, $M = \emptyset$, and phase 1 starts at request 1. Assume the claim after request $t - 1$, and let $p = \sigma_t$. Let $P$ be the set of distinct pages of the current phase up to $t - 1$, so $M = P$.

- If request $t$ starts a new phase, then $|P| = k$ and $p \notin P$. By Claim 1, $M \subseteq C$ and $|C| \le k$, so $|M| = k$ gives $M = C$, and $p \notin C$. So request $t$ is a fault with $|C| = k$ and $M = C$. Line L7 empties $M$, and line L11 sets $M = \{p\}$, the set of pages of the new phase so far.
- If request $t$ does not start a new phase, then $p \in P$ or $|P| < k$. If line L7 empties $M$, then $M = C$ and $p \notin C$, and $|C| = k$, so $|P| = k$ and $p \notin P$, which is false. So line L7 does not change $M$, and line L11 sets $M = P \cup \{p\}$, the set of pages of the current phase up to $t$. $\square$

**Claim 3.** In each phase, the algorithm has at most $k$ faults. So $\mathrm{ALG}(\sigma) \le kN$.

*Proof.* Let $p$ be a page requested in a phase, and let $s$ be its first request in the phase. After request $s$, the page $p$ is in $M$ by Claim 2, and it stays in $M$ until the end of the phase, because line L7 runs only at the start of a phase. Line L9 never evicts a page of $M$. So $p$ stays in $C$ until the end of the phase, and each later request for $p$ in the phase is a hit. So each distinct page of the phase faults at most once in the phase, and the phase has at most $k$ distinct pages. $\square$

**Claim 4.** Each paging algorithm, online or offline, with an empty initial cache, loads at least $N$ pages on $\sigma$. So $\mathrm{OPT}(\sigma) \ge N$.

*Proof.* Let phase $i$ start at request $a_i$, and let $p_i = \sigma_{a_i}$. For $1 \le i < N$, let $W_i$ be the requests $a_i + 1, \ldots, a_{i+1}$. After request $a_i$, the cache holds $p_i$ and at most $k - 1$ other pages. The requests of $W_i$ before $a_{i+1}$ contain the $k - 1$ pages of phase $i$ other than $p_i$, and $\sigma_{a_{i+1}}$ is a page outside phase $i$. So $W_i$ requests $k$ distinct pages other than $p_i$, and one of them, say $r$, is not in the cache after request $a_i$. The algorithm must hold $r$ at its first request in $W_i$, so it loads $r$ at a time after request $a_i$ and not after that request. So it has a load inside $W_i$. The windows $W_1, \ldots, W_{N-1}$ are disjoint, since $W_i$ ends at $a_{i+1}$ and $W_{i+1}$ starts at $a_{i+1} + 1$. Request 1 needs one more load, before any window. So there are at least $N$ loads. $\square$

**Theorem.** For each rule CHOOSE and each $\sigma$, $\mathrm{MARKING}(\sigma) \le k \cdot \mathrm{OPT}(\sigma)$.

*Proof.* By Claims 3 and 4, $\mathrm{MARKING}(\sigma) \le kN \le k \cdot \mathrm{OPT}(\sigma)$. With a common initial cache instead of an empty one, Claim 4 gives $N - 1$ loads, so $\mathrm{MARKING}(\sigma) \le k \cdot \mathrm{OPT}(\sigma) + k$. $\blacksquare$
