---
title: Tetris legalization returns a legal placement, takes the cheapest place that the frontiers allow, and runs in O(n log n + nK) time
proves: [correctness, termination, running time]
status: full
---

Write $F_r$ for the frontier of row $r$, $n$ for the number of cells and $K$ for the number of rows. All frontiers start at 0. Let $N(v) = -\lfloor -v + \frac12 \rfloor$, the integer nearest to $v$ with a tie to the left, and let $\mathrm{cl}(p, L, U) = \min(\max(p, L), U)$ for $L \le U$.

**Lemma 1 (frontier invariant).** Before and after each step, every cell placed in row $r$ occupies an interval $[x_j, x_j + W_j)$ with $0 \le x_j$ and $x_j + W_j \le F_r \le S$, and the intervals of row $r$ are pairwise disjoint.

*Proof.* At the start no cell is placed and $F_r = 0$. Suppose it holds before cell $i$ goes into row $r$ at $p = \max(F_r, \text{want})$. Then $p \ge F_r \ge 0$, and $p + W_i \le S$ by line L6. Every earlier cell of row $r$ ends at most at $F_r \le p$, so the new interval $[p, p + W_i)$ meets none of them. Line L10 sets $F_r = p + W_i \le S$, and every cell of row $r$, the new one included, ends at most at the new $F_r$. Other rows do not change. $\square$

**Theorem 1 (legal output).** If Tetris does not stop with failure, it returns a legal placement: each cell is on an integer site of a row, inside the row, and no two cells of a row overlap.

*Proof.* Line L4 gives an integer, and line L5 takes the maximum of two integers, so every $x_i$ is an integer. The rest is Lemma 1 after the last step. $\blacksquare$

**Lemma 2 (the best place in a row).** Let $0 \le L \le U$ be integers. Over the integers $p \in [L, U]$, $|p - v|$ is least at $p^\ast = \mathrm{cl}(N(v), L, U)$. If $F_r \le S - W_i$, line L5 gives $p^\ast$ for $L = F_r$ and $U = S - W_i$; if $F_r > S - W_i$, no position in row $r$ starts at or after $F_r$ and ends at most at $S$, and line L6 skips the row.

*Proof.* The function $g(p) = |p - v|$ is convex in $p$ and, over all integers, least at $N(v)$. A convex function on the integers decreases up to its minimum and increases after it. If $N(v) < L$, the least value on $[L, U]$ is at $L$; if $N(v) > U$, at $U$; otherwise at $N(v)$. This is $\mathrm{cl}(N(v), L, U)$. Line L4 computes $\text{want} = \mathrm{cl}(N(v), 0, U)$ with $v = x'_i$, and line L5 takes $\max(L, \text{want})$. If $N(v) \le L$, then $\text{want} \le L$ (because $L \le U$), and the result is $L$. If $L < N(v) \le U$, the result is $N(v)$. If $N(v) > U$, then $\text{want} = U \ge L$ and the result is $U$. In each case it is $p^\ast$. If $F_r > S - W_i$, every $p \ge F_r$ has $p + W_i > S$, and $p = \max(F_r, \cdot) \ge F_r$ fails line L6. $\square$

**Theorem 2 (greedy choice).** At each step Tetris puts cell $i$ at the place of least Manhattan movement among all positions $(p, y_r)$ with $p$ an integer, $p \ge F_r$ and $p + W_i \le S$, over all rows $r$; on a tie it takes the row of smallest index. It stops with failure exactly when no such position exists.

*Proof.* For a fixed row the term $|y_r - y'_i|$ is a constant, so by Lemma 2 the cheapest allowed position in row $r$ is $\text{pos}(r)$, and rows with none are skipped. Line L9 takes the least $\text{cost}(r)$, the first on a tie. If every row is skipped, no allowed position exists, and line L8 stops; otherwise some row is left and the step succeeds. $\blacksquare$

The theorem is about the positions that the frontiers allow. A free gap to the left of $F_r$ is not allowed, which is why Tetris can fail while a legal placement exists.

**Theorem 3 (running time).** Tetris runs in $O(n \log n + n K)$ time and $O(n + K)$ extra space.

*Proof.* Line L1 is one sort of $n$ keys, $O(n \log n)$. The loop of line L2 runs $n$ times. In each run, lines L3 to L7 do $O(1)$ arithmetic per row, $O(K)$ in total, and lines L8 to L10 cost $O(1)$ (the least cost is kept during the loop over rows). The frontiers take $O(K)$ space and the positions $O(n)$. The loop ends after the $n$ cells, or earlier at line L8. $\blacksquare$
