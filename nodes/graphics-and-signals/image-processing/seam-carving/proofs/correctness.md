---
title: The seam dynamic program returns a connected vertical seam of least energy, and repeated removal is greedy
proves: [correctness]
status: full
---

Fix an energy table $e$ with $W \ge 1$ columns and $H \ge 1$ rows and real entries. A partial seam to $(x, y)$ is a sequence $(s_0, \ldots, s_y)$ of columns in $\{0, \ldots, W-1\}$ with $s_y = x$ and $|s_i - s_{i-1}| \le 1$ for $1 \le i \le y$. Its energy is $\sum_{i=0}^{y} e(s_i, i)$. Let $\mathrm{OPT}(x, y)$ be the least energy of a partial seam to $(x, y)$. A seam is a partial seam to some pixel of row $H - 1$. For a column $x$, let $A(x) = \{x - 1, x, x + 1\} \cap \{0, \ldots, W-1\}$, which is not empty because it contains $x$.

**Claim 1 (the table).** After lines L6 to L10, for each $y$ and $x$, $M[y][x] = \mathrm{OPT}(x, y)$, $P[y][x] \in A(x)$ for $y \ge 1$, and $M[y][x] = e(x, y) + M[y-1][P[y][x]]$.

*Proof.* Induction on $y$. For $y = 0$ the only partial seam to $(x, 0)$ is $(x)$, with energy $e(x, 0)$, which is the value of line L6.

Let $y \ge 1$ and assume the claim for row $y - 1$. Line L9 chooses $b \in A(x)$ with $M[y-1][b] = \min_{x' \in A(x)} M[y-1][x']$, and line L10 sets $M[y][x] = e(x, y) + M[y-1][b]$ and $P[y][x] = b$, which gives the last two parts of the claim.

Lower bound. Take any partial seam $(s_0, \ldots, s_y)$ to $(x, y)$. Then $s_{y-1} \in A(x)$, and $(s_0, \ldots, s_{y-1})$ is a partial seam to $(s_{y-1}, y-1)$, so its energy is at least $\mathrm{OPT}(s_{y-1}, y-1) = M[y-1][s_{y-1}] \ge M[y-1][b]$. Adding $e(x, y)$ shows that the seam has energy at least $M[y][x]$.

Upper bound. By the hypothesis there is a partial seam to $(b, y-1)$ with energy $M[y-1][b]$. Since $|b - x| \le 1$, appending $x$ gives a partial seam to $(x, y)$ with energy $e(x, y) + M[y-1][b] = M[y][x]$.

So $M[y][x] = \mathrm{OPT}(x, y)$. $\square$

**Claim 2 (the seam).** Lines L11 and L12 return a seam $s$ with $E(s) = \min_x M[H-1][x]$, and this is the least energy of any seam.

*Proof.* Every seam ends at some $(x, H-1)$, so the least seam energy is $\min_x \mathrm{OPT}(x, H-1) = \min_x M[H-1][x]$ by Claim 1. Line L11 sets $s_{H-1}$ to a column $x^\ast$ where this minimum is reached.

We show by downward induction on $y$ that after line L12 has set $s_y$, the sequence $(s_y, \ldots, s_{H-1})$ satisfies $|s_i - s_{i-1}| \le 1$ for $y < i \le H-1$ and

$$\sum_{i=y+1}^{H-1} e(s_i, i) + M[y][s_y] = M[H-1][x^\ast].$$

For $y = H - 1$ the sum is empty and the equation holds. Going from $y$ to $y - 1$, line L12 sets $s_{y-1} = P[y][s_y] \in A(s_y)$, so $|s_y - s_{y-1}| \le 1$, and Claim 1 gives $M[y][s_y] = e(s_y, y) + M[y-1][s_{y-1}]$, which keeps the equation. At $y = 0$, $M[0][s_0] = e(s_0, 0)$, so $E(s) = M[H-1][x^\ast]$, and $s$ is connected. $\square$

The tie rule at lines L9 and L11 affects only which optimal seam is returned, not its energy, because Claims 1 and 2 use only that $b$ and $x^\ast$ reach the minimum.

**Claim 3 (removal).** Line L4 returns a $(W-1) \times H$ image whose row $y$ is row $y$ of $I$ without the entry at column $s_y$, in the same order.

*Proof.* $0 \le s_y \le W - 1$ by Claim 2, so exactly one entry is deleted from each row. $\square$

**Claim 4 (termination and size).** For $0 \le k < W$, SEAM-CARVE returns a $(W-k) \times H$ image, and each output row is a subsequence of the input row.

*Proof.* Before step $i$ of the loop of line L1 (counting from 0), the width is $W - i \ge W - k + 1 \ge 2$, so the image is not empty and Claims 1 to 3 apply. Each step removes one entry per row and keeps the order of the others, and a subsequence of a subsequence is a subsequence. $\square$

**Claim 5 (greedy over several seams).** The loop of line L1 does not in general minimize the total energy of the $k$ removed seams, even when the energy is not recomputed.

*Proof.* Keep the energy fixed on the pixels, so that after a removal each remaining pixel keeps its energy and the second seam is chosen in the reduced table. Take $W = 4$, $H = 3$ and the rows $(0, 3, 3, 4)$, $(5, 1, 4, 1)$, $(2, 4, 1, 5)$. The least first seam is $(0, 1, 2)$ with energy $0 + 1 + 1 = 2$, and it is unique. The reduced rows are $(3, 3, 4)$, $(5, 4, 1)$, $(2, 4, 5)$, whose least seam is $(1, 2, 1)$ with energy $3 + 1 + 4 = 8$, for a total of 10. Instead remove $(0, 1, 0)$ first, with energy $0 + 1 + 2 = 3$. The reduced rows are $(3, 3, 4)$, $(5, 4, 1)$, $(4, 1, 5)$, and the seam $(1, 2, 1)$ has energy $3 + 1 + 1 = 5$, for a total of 8. $\square$

So each seam is optimal for the image it is cut from, and the whole procedure is a greedy heuristic for the $k$-seam problem.

**Cost.** Line L9 looks at $|A(x)| \le 3$ entries, so lines L6 to L10 do $O(1)$ work per entry, $\Theta(WH)$ in total; lines L11 and L12 take $\Theta(W + H)$. With $\Theta(WH)$ for lines L2 and L4, one step costs $\Theta(WH)$, and $k$ steps cost $\sum_{i=0}^{k-1}\Theta((W-i)H)$. Since $\sum_{i=0}^{k-1}(W - i) = kW - k(k-1)/2$ and $k - 1 < W$, this sum lies between $kW/2$ and $kW$, so the total is $\Theta(kWH)$.
