---
title: Merge insertion returns the input in sorted order, with at most F(n) comparisons
proves: [correctness, termination]
status: full
---

Write $m = \lfloor n/2 \rfloor$ and $h = \lceil n/2 \rceil$, so the losers are $b_1, \ldots, b_h$, and $b_h$ has no partner when $n$ is odd. Let $t_1 = 1$ and $t_k = (2^{k+1} + (-1)^k)/3$ for $k \ge 2$, so $t_2 = 3$, $t_3 = 5$, $t_4 = 11$. A short check gives $t_k + t_{k-1} = (2^{k+1} + 2^k)/3 = 2^k$ for $k \ge 2$, because the terms $(-1)^k$ and $(-1)^{k-1}$ cancel.

**Termination.** By induction on $n$. For $n \le 1$, line L1 returns. For $n \ge 2$, the call of line L5 is on $m < n$ items, so it ends by induction, and the loops of lines L7 to L10 are finite: the values $t_k$ grow, so line L7 stops after the first $k$ with $t_k \ge h$, and each binary search ends.

**Lemma 1 (the groups cover each loser once).** The ranges $t_{k-1} + 1, \ldots, \min(t_k, h)$ of line L8, for $k = 2, 3, \ldots$ while $t_{k-1} < h$, are disjoint and cover $2, \ldots, h$.

*Proof.* The $t_k$ are strictly increasing, so the ranges are disjoint and follow each other without gaps from $t_1 + 1 = 2$. The loop stops at the first $k$ with $t_k \ge h$, and the last range ends at $\min(t_k, h) = h$. $\square$

**Lemma 2 (the chain stays sorted).** After line L6, and after each insertion of line L10, $S$ is in non-decreasing order, and for each $j$ not yet inserted with $j \le m$, $a_j$ is in $S$.

*Proof.* After line L5 the pairs are in the order $a_1 \le \cdots \le a_m$, and each pair still has $b_i \le a_i$ from line L3, because the recursive call moves pairs as units. So $(b_1, a_1, \ldots, a_m)$ is sorted. The winners are never removed from $S$, so each $a_j$ stays in $S$.

Now let $S$ be sorted, and insert $b_j$. If $j \le m$, let $u$ be the position of $a_j$. Each item $S[i]$ with $i \ge u$ is at least $S[u] = a_j \ge b_j$. So there is a place for $b_j$ in $S[0 \ldots u]$, at or before $u$, that keeps $S$ sorted: right after the last item of $S[0 \ldots u-1]$ that is not greater than $b_j$, or at 0 if there is none. The binary search of line L10 over $S[0 \ldots u-1]$ returns this place: it keeps the range of places $[lo, hi]$ such that each item before $lo$ is at most $b_j$ and each item from $hi$ to $u-1$ is greater than $b_j$, and the range shrinks to one place. Inserting $b_j$ there keeps $S$ sorted. If $j > m$, the same argument with $u = |S|$ applies. $\square$

**Correctness.** By induction on $n$, MERGE-INSERTION returns the items of $X$ in sorted order. For $n \le 1$ this is clear. For $n \ge 2$: by line L6 and Lemma 1, each $a_i$ and each $b_i$ enters $S$ exactly once, and nothing else does, so at line L11 $S$ holds exactly the items of $X$. By Lemma 2, $S$ is sorted. The recursive call of line L5 is correct by induction, because it sorts the pairs by the order of their winners, which is a total preorder, and the claim for the call needs only that the order is total. Equal winners may come out in any order, which does not affect the argument.

**Lemma 3 (the comparison bound).** When $b_j$ with $t_{k-1} < j \le t_k$ is inserted, the binary search makes at most $k$ comparisons.

*Proof.* Let $j \le m$ first. The part $S[0 \ldots u-1]$ to the left of $a_j$ can only hold items less than or equal to $a_j$ in the sorted chain, and these are among: the winners $a_1, \ldots, a_{j-1}$; the losers $b_1, \ldots, b_{t_{k-1}}$ inserted at line L6 or in earlier groups; and the losers $b_{j+1}, \ldots, b_{\min(t_k, h)}$ of the current group, which line L8 inserts before $b_j$. The losers $b_{j'}$ with $j' > t_k$ are not yet in $S$. So $u \le (j - 1) + t_{k-1} + (t_k - j) = 2^k - 1$. If $j = h > m$, then $j$ is the first index of its group to be inserted, and $S$ holds $a_1, \ldots, a_m$ and $b_1, \ldots, b_{t_{k-1}}$, so $|S| = (j - 1) + t_{k-1} \le 2^k - 1$. A binary search over $u \le 2^k - 1$ items halves a range of at most $2^k$ places at each comparison, so it ends after at most $k$ comparisons. $\square$

Adding $m$ comparisons for line L3, the comparisons of the recursive call, and Lemma 3 for each loser gives a worst case that satisfies the recurrence of Knuth, Section 5.3.1, whose solution is $F(n) = \sum_{k=1}^{n} \lceil \lg (3k/4) \rceil$. $\blacksquare$
