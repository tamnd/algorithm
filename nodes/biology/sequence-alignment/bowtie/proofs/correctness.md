---
title: Backtracking and double indexing find every hit within the allowed mismatches
proves: [correctness]
status: full
---

Let $R$ have length $n$, let $P$ have length $m$, and let $I$ be an FM-index of $R$ with suffix array $SA$. For a string $u$, write $\mathrm{rows}(u)$ for the interval of suffix array rows whose suffixes start with $u$. We use the backward-search lemma of the [FM-index](/fm-index/): if $[sp, ep) = \mathrm{rows}(u)$, then $\mathrm{rows}(bu) = [C[b] + \mathrm{Occ}(b, sp),\ C[b] + \mathrm{Occ}(b, ep))$, and $\mathrm{rows}(\varepsilon) = [0, n+1)$.

Call a string $v$ of length $m$ *admissible* for $(P, k, lo, hi)$ when $v$ differs from $P$ in at most $k$ positions, all in $[lo, hi)$. The limit of backtracks is assumed to be off.

**Lemma 1 (BACKTRACK).** BACKTRACK$(I, P, k, lo, hi)$ reports, for each admissible $v$ that occurs in $R$, the rows $\mathrm{rows}(v)$ with $z$ equal to the number of positions where $v$ differs from $P$, and it reports no other row.

*Proof.* Every stack entry $(i, [sp, ep), z)$ satisfies: there is a string $u$ of length $m - i$ with $[sp, ep) = \mathrm{rows}(u)$, $u$ occurs in $R$, $u$ differs from $P[i \ldots m-1]$ in exactly $z \le k$ positions, and all of them are in $[lo, hi)$. The first entry has $u = \varepsilon$. Line L7 forms $\mathrm{rows}(bu)$ by the backward-search lemma; line L5 makes sure that a new difference is allowed and within budget; line L8 pushes the entry only if $bu$ occurs. So the invariant holds, and every report at line L3 is $\mathrm{rows}(v)$ for an admissible $v$ that occurs.

Conversely, let $v$ be admissible and occur in $R$. For each $i$ from $m$ down to 0, the suffix $v[i \ldots m-1]$ occurs (it is a substring of an occurrence of $v$) and differs from $P[i \ldots m-1]$ in an allowed way. By induction on $m - i$, an entry for $v[i \ldots m-1]$ is pushed: the entry for $v[i+1 \ldots]$ is popped at some time, line L4 tries the letter $b = v[i]$, line L5 does not skip it because $v$ is admissible, and its interval is not empty. At $i = 0$ the entry for $v$ is reported. Different strings give different leaves of the search tree, so each is reported once. $\square$

So with $lo = 0$ and $hi = m$, BACKTRACK solves the k-mismatch problem on $I$: the positions $SA[r]$ of the reported rows are exactly the starts of the substrings of $R$ at Hamming distance at most $k$ from $P$.

**Lemma 2 (mirror positions).** Let $\overleftarrow{R}$ be $R$ reversed. Then $R[s \ldots s+m-1] = v$ if and only if $\overleftarrow{R}[n-s-m \ldots n-s-1] = \overleftarrow{v}$.

*Proof.* $\overleftarrow{R}[j] = R[n-1-j]$. For $0 \le t < m$, $\overleftarrow{R}[n-s-m+t] = R[s+m-1-t] $, which is the letter $t$ of $\overleftarrow{v}$ exactly when $R[s+m-1-t] = v[m-1-t]$. $\square$

**Theorem (double indexing).** Let $h = \lfloor m/2 \rfloor$. BOWTIE-ONE-MISMATCH$(P)$ returns exactly the set of positions $s$ with $\mathrm{Ham}(R[s \ldots s+m-1], P) \le 1$.

*Proof.* Soundness: phase 1 reports only substrings that differ from $P$ in at most one position, by Lemma 1. Phase 2 reports rows of $\overleftarrow{v}$ in $\overleftarrow{R}$ where $\overleftarrow{v}$ differs from $\overleftarrow{P}$ in at most one position; by Lemma 2 the position $s = n - SA_{\text{mirror}}[r] - m$ has $R[s \ldots s+m-1] = v$, and $v$ differs from $P$ in at most one position.

Completeness: let $v = R[s \ldots s+m-1]$ with at most one mismatch. If $v = P$ or the mismatch is at a position $j < h$, then $v$ is admissible for $(P, 1, 0, h)$, and phase 1 reports $s$. If the mismatch is at $j \ge h$, then $\overleftarrow{v}$ differs from $\overleftarrow{P}$ only at position $m - 1 - j \le m - 1 - h < m - h$, so $\overleftarrow{v}$ is admissible for $(\overleftarrow{P}, 1, 0, m - h)$. It occurs in $\overleftarrow{R}$ at $n - s - m$ by Lemma 2, so phase 2 reports this row, and line L11 maps it to $s$. $\square$

**Why it saves work.** In phase 1 the substitutions are allowed only at positions below $h$, and the search reaches them after $m - h$ exact steps, so every branch starts from $\mathrm{rows}(P_R)$, which in a random genome holds about $n/4^{m-h}$ rows. In phase 2 every branch starts from $\mathrm{rows}(\overleftarrow{P_L})$ in the mirror index. Plain backtracking with substitutions allowed everywhere also branches at the first positions it reads, at the right end of $P$, where the interval is still large; this is the excess that double indexing removes. This is an argument about the typical cost, not a worst-case bound.
