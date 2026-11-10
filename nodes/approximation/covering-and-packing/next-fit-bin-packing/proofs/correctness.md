---
title: Next fit returns a packing with at most 2 OPT - 1 bins
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a list $s_1, \ldots, s_n$ with $0 < s_i \le 1$, $S = \sum_i s_i$, and the bins are $B_1, \ldots, B_k$ in the order in which line L4 opens them. The load of a bin is the sum of the sizes of its items.

**Lemma 1 (feasibility).** Next fit returns a partition of $\{1, \ldots, n\}$ into bins, and each bin has load at most 1.

*Proof.* We use this invariant at the start of each pass of line L2: the items $1, \ldots, i-1$ are each in exactly one of $B_1, \ldots, B_k$, the variable $load$ is the load of $B_k$, and each of $B_1, \ldots, B_k$ has load at most 1. At the start, $i = 1$ and $k = 0$, so the invariant is true. In a pass, either line L3 sees $load + s_i \le 1$, and line L5 adds $i$ to $B_k$ with new load $load + s_i \le 1$; or line L4 opens $B_{k+1}$ with load 0, and line L5 makes its load $s_i \le 1$. The other bins do not change. So the invariant holds after the pass. When the loop ends, $i = n + 1$, and the invariant is the claim. $\square$

**Lemma 2 (pairs).** For each $j$ with $1 \le j < k$, $\mathrm{load}(B_j) + \mathrm{load}(B_{j+1}) > 1$.

*Proof.* Let $t$ be the item that opened $B_{j+1}$. When $t$ was processed, $B_j$ was the current bin and line L3 found $\mathrm{load}(B_j) + s_t > 1$. After that pass, $B_j$ never gets another item, because each later item goes into $B_{j+1}$ or a later bin. So the final load of $B_j$ is the load at that time. The item $t$ is in $B_{j+1}$, so $\mathrm{load}(B_{j+1}) \ge s_t$, and the sum is more than 1. $\square$

**Theorem.** If $n \ge 1$, then $k \le 2 \lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$.

*Proof.* Pair the bins as $(B_1, B_2), (B_3, B_4), \ldots, (B_{2p-1}, B_{2p})$ with $p = \lfloor k/2 \rfloor$. By Lemma 2, each pair has total load more than 1, and the pairs are disjoint, so $S > p$ when $p \ge 1$. When $p = 0$, $S > 0 = p$ because $n \ge 1$. Since $p$ is an integer and $S > p$, we get $\lceil S \rceil \ge p + 1$, that is, $p \le \lceil S \rceil - 1$. So

$$k \le 2p + 1 \le 2(\lceil S \rceil - 1) + 1 = 2\lceil S \rceil - 1.$$

The [size bound](/bin-packing-lower-bound/) gives $\lceil S \rceil \le \mathrm{OPT}$, which proves the second inequality. $\blacksquare$

**Tightness for each value of OPT.** Fix $k \ge 1$, let $f = \frac{1}{2k}$ and $b = 1 - \frac{1}{4k}$, and take the list $f, b, f, b, \ldots, b, f$ with $k$ copies of $f$ and $k - 1$ copies of $b$. Since $f + b = 1 + \frac{1}{4k} > 1$, line L3 opens a new bin for each item after the first, so next fit uses $2k - 1$ bins. On the other hand, the $k - 1$ items $b$ in separate bins and the $k$ items $f$ in one bin (total $\frac12$) form a packing with $k$ bins, and $S = (k-1)b + kf = k - 1 + \frac{k+1}{4k} > k - 1$ forces $\mathrm{OPT} \ge k$. So $\mathrm{OPT} = k$ and next fit uses $2\,\mathrm{OPT} - 1$ bins.
