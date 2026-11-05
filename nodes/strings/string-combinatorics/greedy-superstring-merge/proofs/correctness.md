---
title: GREEDY-SUPERSTRING returns a superstring and equals greedy merging
proves: [correctness, termination]
status: full
---

**Notation.** Strings are over an alphabet with equality of letters only; indices are 0-based. For strings $x, y$, $\mathrm{ov}(x, y)$ is the length of the longest suffix of $x$ that is a prefix of $y$. After line L1 the list $s_0, \ldots, s_{m-1}$ has no repeats and no string inside another (substring-free), and $w(i, j) = \mathrm{ov}(s_i, s_j)$ for $i \ne j$.

**Lemma 1.** If $x \ne y$ are in a substring-free list, then $\mathrm{ov}(x, y) < \min(|x|, |y|)$.

*Proof.* An overlap of length $|y|$ makes $y$ a suffix of $x$, and one of length $|x|$ makes $x$ a prefix of $y$; both are excluded. $\square$

**Lemma 2 (removed strings are covered).** Each input string occurs in some $s_i$.

*Proof.* A repeat of a string is covered by the copy that L1 keeps or by what covers that copy, so consider a removed string $x$. It occurs inside a different string $y$ of the list, and then $|y| > |x|$, since a different string of the same length cannot contain $x$. If $y$ is removed too, repeat the argument with $y$. The lengths grow strictly, so this stops at a kept string, and occurrence is transitive. $\square$

**Invariant of the scan.** Before and after each step of line L4: the accepted edges form vertex-disjoint paths (chains) covering all $m$ vertices; $\mathit{next}[i] = \mathrm{nil}$ exactly for the tails, $\mathit{prev}[j] = \mathrm{nil}$ exactly for the heads; $\mathit{head}[t]$ is the head of the chain with tail $t$, and $\mathit{tail}[h]$ the tail of the chain with head $h$.

*Initially* each vertex is a chain alone, and $\mathit{head}[t] = t$, $\mathit{tail}[h] = h$. *An accepted edge* $(i, j)$ has $i$ a tail, $j$ a head, and $\mathit{head}[i] \ne j$, so the chain $C_1$ ending at $i$ and the chain $C_2$ starting at $j$ differ; the edge joins them into one path with head $\mathit{head}[i]$ and tail $\mathit{tail}[j]$, and line L6 records these two values. The other chains do not change. A rejected edge changes nothing.

**Lemma 3 (one chain at the end).** After the scan there is exactly one chain.

*Proof.* Suppose there are two chains $A \ne B$ at the end; let $t$ be the tail of $A$ and $h$ the head of $B$. The pair $(t, h)$ was scanned, and $t \ne h$. Chains only merge, and $\mathit{next}$, $\mathit{prev}$ are never reset, so at that time $t$ was a tail, $h$ a head, and they were in different chains (otherwise they would be in the same chain at the end). So $\mathit{head}[t] \ne h$, and line L5 accepted $(t, h)$, which makes $\mathit{next}[t] \ne \mathrm{nil}$ at the end, a contradiction. $\square$

**Termination.** Line L4 scans the finite list of $m(m - 1)$ pairs. By Lemma 3 the accepted edges form one path $h_0 \to h_1 \to \cdots \to h_{m-1}$; line L7 finds its unique head $h_0$, and line L8 runs $m - 1$ times.

**Lemma 4 (the spelling).** After the step of line L8 that reaches $h_r$, $R$ ends with $s_{h_r}$ and contains $s_{h_0}, \ldots, s_{h_r}$, and $|R| = \sum_{q \le r} |s_{h_q}| - \sum_{q < r} w(h_q, h_{q+1})$.

*Proof.* True for $r = 0$. The step appends $s_{h_{r+1}}$ without its prefix of length $k = w(h_r, h_{r+1})$. That prefix is a suffix of $s_{h_r}$, hence of $R$, so the new $R$ ends with $s_{h_{r+1}}$, and its length grows by $|s_{h_{r+1}}| - k$. $\square$

With Lemma 2, the output contains every input string. For $m = 0$ the list is empty; we return the empty string, which is correct.

**Lemma 5 (inherited overlaps).** Let $L$ be a substring-free list, let $x, y \in L$ with $\mathrm{ov}(x, y) = k$ maximal over all pairs of distinct strings of $L$, and let $z = x \cdot y[k..]$. Then for each $u \in L \setminus \{x, y\}$: $u$ does not occur in $z$, $z$ does not occur in $u$, $\mathrm{ov}(z, u) = \mathrm{ov}(y, u)$ and $\mathrm{ov}(u, z) = \mathrm{ov}(u, x)$.

*Proof.* $z$ is longer than $x$, which is not inside $u$, so $z$ is not inside $u$. If $u$ occurs in $z$ at index $p$, it is not inside $x$, so it ends after $|x| - 1$; it is not inside $y$, which occupies the indices from $|x| - k$ on, so $p < |x| - k$. Then the suffix of $x$ from $p$, of length $|x| - p > k$, is a prefix of $u$, and $\mathrm{ov}(x, u) > k$, against the choice of $k$. For the overlaps: a suffix of $z$ that is a prefix of $u$ has length less than $|y|$, otherwise $y$, a suffix of $z$, would be inside $u$ (as a suffix of that prefix). So it is a suffix of $y$, and $\mathrm{ov}(z, u) = \mathrm{ov}(y, u)$. Symmetrically, a prefix of $z$ that is a suffix of $u$ has length less than $|x|$, so it is a prefix of $x$, and $\mathrm{ov}(u, z) = \mathrm{ov}(u, x)$. $\square$

**Equivalence with greedy merging.** Consider the string form: keep the list of chains, each spelled as a string, and at each step merge the pair of chains $(A, B)$ with the largest overlap of their strings, ties broken by the smaller tail of $A$, then the smaller head of $B$. By Lemma 5 and induction on the number of merges, the list of chain strings stays substring-free, and the overlap of the string of $A$ with the string of $B$ equals $w(\mathrm{tail}(A), \mathrm{head}(B))$. So the string form chooses, at each step, the valid edge (from a tail to the head of another chain) that is first in the order of line L3. The scan does the same: an edge rejected at line L5 stays invalid forever, since tails stop being tails, heads stop being heads, and chains only merge; so the next accepted edge is the first valid edge in the order. Both forms accept the same edges in the same order and spell the same string. $\blacksquare$
