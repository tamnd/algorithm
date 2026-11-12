---
title: The structure of the LIRS stacks
proves: [correctness]
status: full
---

We use the pseudocode of the page with a cache of $L = L_{lirs} + L_{hirs}$ blocks, $L_{lirs} \ge 1$ and $L_{hirs} \ge 1$. Accesses happen at times $1, 2, 3, \ldots$, and $\mathrm{last}(x)$ is the time of the last access to $x$ so far. Let $\mathcal{L}$ be the set of LIR blocks, and let $m = \min_{y \in \mathcal{L}} \mathrm{last}(y)$, with $m = 0$ when $\mathcal{L}$ is empty. Blocks in Q are the resident HIR blocks, and the cache is $\mathcal{L} \cup Q$.

**Claim.** After every access:

- (S1) S holds exactly the blocks of $\mathcal{L}$ and the blocks $x$ with $\mathrm{last}(x) > m$;
- (S2) S is in order of $\mathrm{last}$, the smallest at the bottom;
- (S3) if S is not empty, its bottom block is an LIR block, the one with $\mathrm{last} = m$;
- (C1) $\mathcal{L}$ and Q are disjoint, $|\mathcal{L}| \le L_{lirs}$ and $|Q| \le L_{hirs}$;
- (C2) once $|\mathcal{L}| = L_{lirs}$, it stays so.

*Proof.* By induction on the accesses. At the start all sets are empty. Assume the claim before an access to $x$ at time $t$. Every branch puts $x$ at the top of S and sets $\mathrm{last}(x) = t$, the largest value so far, so (S2) holds for $x$, and all other entries of S keep their order. We first show that (S1) to (S3) hold before pruning with $m$ replaced by the new value $m'$, except that HIR blocks with $\mathrm{last} < m'$ may still sit at the bottom of S. Then pruning removes them.

First note that $m$ never decreases. The set $\mathcal{L}$ changes in three ways. An LIR block is accessed (case 1), which raises its $\mathrm{last}$. A block with $\mathrm{last} = t$ joins $\mathcal{L}$ while the block with the smallest $\mathrm{last}$ leaves it (cases 2a and 3a, by DEMOTE and (S3)). A block with $\mathrm{last} = t$ joins during warm-up. In each case the new minimum is at least the old one. So a block with $\mathrm{last} \le m$ that is not LIR stays out of S under the target (S1) until it is accessed again.

*Case 1, $x \in \mathcal{L}$.* Line L2 moves $x$ to the top. If $x$ was not the bottom, $m' = m$ and the bottom is still the same LIR block, so pruning does nothing. If $x$ was the bottom, then $m' $ is the $\mathrm{last}$ of the next LIR block in S, which by (S1) and (S2) is the lowest LIR entry above $x$. The entries between are HIR blocks with $m < \mathrm{last} < m'$. Pruning on line L3 removes exactly them, so (S1) to (S3) hold with $m'$.

*Case 2a, $x \in Q$ and $x \in S$.* Line L7 makes $x$ LIR at the top of S and removes it from Q. DEMOTE moves the bottom block $y$ of S, which by (S3) is the LIR block with $\mathrm{last} = m$, to Q as a resident HIR block. Now $|\mathcal{L}|$ and $|Q|$ are unchanged, and $m'$ is the smallest $\mathrm{last}$ of the new LIR set. The blocks below the lowest LIR entry are HIR blocks with $\mathrm{last} < m'$, and pruning removes them. Blocks above it have $\mathrm{last} > m'$ and stay.

*Case 2b, $x \in Q$ and $x \notin S$.* By (S1), $\mathrm{last}(x) < m$ before the access. Now $\mathrm{last}(x) = t > m$ and $m$ does not change, so $x$ belongs at the top of S, as line L10 puts it. Q only changes order.

*Warm-up, $x$ is not resident and $|\mathcal{L}| < L_{lirs}$.* By (C2) no HIR block has existed yet, so $x$ is new. Line L13 adds it to $\mathcal{L}$ at the top of S. If $\mathcal{L}$ was empty, $m' = t$ and S is just $x$. Otherwise $m$ does not change. The cache has at most $L_{lirs} < L$ blocks, so no eviction is needed.

*Case 3, $x$ is not resident and $|\mathcal{L}| = L_{lirs}$.* If the cache is full, then $|Q| = L - L_{lirs} = L_{hirs} \ge 1$, so line L15 can evict the bottom of Q. That block is HIR, and staying in S or leaving it does not change $\mathcal{L}$ or $m$, so (S1) still holds for it. Then:

- In case 3a, $x \in S$ means $\mathrm{last}(x) > m$ by (S1). The argument of case 2a applies: $x$ becomes LIR at the top, the oldest LIR block goes to Q, and pruning restores (S1) to (S3). The sizes of $\mathcal{L}$ and Q are unchanged, after the one eviction.
- In case 3b, $x \notin S$, and $x$ goes to the top of S and of Q. $\mathcal{L}$ and $m$ are unchanged. The cache grows by one, after at most one eviction, so it has at most $L$ blocks and $|Q| \le L_{hirs}$.

In all cases (C1) and (C2) hold, because only warm-up adds to $\mathcal{L}$ without removing, and it stops at $L_{lirs}$. $\blacksquare$

**Consequences.**

1. *The bottom of S is always an LIR block.* This is (S3). It is the property that the test file checks after every access on 60 seeded random traces.
2. *LIR blocks always hit.* They are resident by definition, and only the bottom of Q is ever evicted.
3. *The swap rule is the IRR rule.* Suppose an HIR block $x$ is accessed at time $t$ and is found in S. By (S1), $\mathrm{last}(x) > m$. The recency of $x$ just before $t$ is the number of distinct blocks accessed in $(\mathrm{last}(x), t)$, which is the new IRR of $x$. The recency of the oldest LIR block $y$ counts the distinct blocks accessed in $(m, t)$, a longer interval that also contains $x$. So the new IRR of $x$ is less than the recency of $y$, and so less than any IRR that $y$ can have at its next access. Conversely, if $x$ is not in S, then $\mathrm{last}(x) < m$, and its new IRR is at least the recency of $y$. So an HIR block becomes LIR exactly when its new IRR is less than the recency of the oldest LIR block.
4. *Each request costs $O(1)$ amortized time.* Each access pushes at most one entry on S, and pruning only removes entries, so the total number of removals is at most the number of accesses.

**The test file.** It checks (S1) to (S3) and (C1) against a direct computation of $\mathrm{last}$ after every access, compares the hit flags with a second LIRS that keeps no stack S and decides membership by (S1), checks the recency and IRR values of Table 1 of the paper, and checks every state of the worked example.
