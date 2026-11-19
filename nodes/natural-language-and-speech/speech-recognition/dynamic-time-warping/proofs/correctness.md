---
title: DTW returns a warping path of least weighted cost
proves: [correctness]
status: full
---

We use the notation of the page. The sequences are $x_1, \ldots, x_n$ and $y_1, \ldots, y_m$ with $n, m \ge 1$, and $c(i, j) = d(x_i, y_j) \ge 0$. A step pattern gives three weights $w_D$, $w_V$ and $w_H$ for the steps $(1, 1)$, $(1, 0)$ and $(0, 1)$; on the page they are $(1, 1, 1)$, $(2, 1, 1)$ and $(1, 1, 0)$.

A *path to $(i, j)$* is a sequence of cells $p_0 = (0, 0), p_1 = (1, 1), p_2, \ldots, p_L = (i, j)$ in which each $p_\ell - p_{\ell-1}$ is $(1, 1)$, $(1, 0)$ or $(0, 1)$, and every cell after $p_0$ has both coordinates at least 1. The first step from the sentinel $(0, 0)$ to $(1, 1)$ is a diagonal step. Write $w(p_\ell - p_{\ell-1})$ for the weight of a step. The cost of the path is

$$\mathrm{cost}(p) = \sum_{\ell=1}^{L} w(p_\ell - p_{\ell-1})\, c(p_\ell).$$

The warping paths of the page are exactly the paths to $(n, m)$ without the sentinel cell, and the cost above is the weighted cost of the page. Let $V(i, j)$ be the least cost of a path to $(i, j)$, for $i, j \ge 1$. Such a path always exists, so $V(i, j)$ is finite. Set $V(0, 0) = 0$ and $V(i, 0) = V(0, j) = \infty$ for $i, j \ge 1$; these cells are not reachable, except the sentinel itself.

**Lemma (recurrence).** For $i, j \ge 1$,

$$V(i, j) = \min\big( V(i-1, j-1) + w_D\, c(i, j),\ V(i-1, j) + w_V\, c(i, j),\ V(i, j-1) + w_H\, c(i, j) \big).$$

*Proof.* The last step of a path to $(i, j)$ enters $(i, j)$ from one of the three cells $(i-1, j-1)$, $(i-1, j)$ or $(i, j-1)$, and the part of the path before it is a path to that cell (or the sentinel alone, when $(i, j) = (1, 1)$ and the step is diagonal). The cost is the cost of that part plus the weight of the last step times $c(i, j)$. So the least cost over paths whose last step comes from a given cell is $V$ of that cell plus the weighted local cost, and $V(i, j)$ is the least of the three. A predecessor with $V = \infty$ contributes no path. For $(i, j) = (1, 1)$ the right side is $\min(0 + w_D c(1, 1), \infty, \infty) = w_D\, c(1, 1)$, which is the cost of the only path. $\square$

**Theorem.** DTW returns $D[n][m] = V(n, m)$, the least weighted cost of a warping path, and a warping path with that cost.

*Proof.* Line L1 sets the sentinel row and column to the values above. The loops of lines L2 and L3 visit the cells in row-major order, so when cell $(i, j)$ is filled, the cells $(i-1, j-1)$, $(i-1, j)$ and $(i, j-1)$ are already final. By induction on this order and by the lemma, lines L4 to L6 set $D[i][j] = V(i, j)$ and store in the back pointer a predecessor that attains the minimum. The traceback of lines L7 and L8 starts at $(n, m)$ and follows the back pointers. Each pointer goes to a cell with a finite value and a smaller sum $i + j$, and the only cell with $i, j \ge 1$ whose pointer is the sentinel is $(1, 1)$, so the loop stops at $(1, 1)$ after at most $n + m - 2$ steps. Along the way, $D$ of each cell equals $D$ of its predecessor plus the weighted cost of the step, so the sum of the step costs of the path is $D[n][m] - D[0][0] = V(n, m)$. $\square$

**Corollary (normalizers).** For the pattern $(2, 1, 1)$ the weight of a step is $\Delta i + \Delta j$, so the weights of every path to $(n, m)$ sum to $n + m$. For the pattern $(1, 1, 0)$ the weight is $\Delta i$, and the weights sum to $n$. In both cases the normalizer is the same for all paths, so dividing $V(n, m)$ by it does not change which path is best.

**Cost.** Lines L4 to L6 run once per cell, with one call of $d$ and a constant number of other operations, so the time is $\Theta(n m)$ in the word-RAM, counting a call of $d$ as one operation. The table and the back pointers take $\Theta(n m)$ words. If only $V(n, m)$ is needed, two rows of the table are enough, and the space is $\Theta(\min(n, m))$ after swapping the sequences when needed.

**The paths counted.** The number of warping paths from $(1, 1)$ to $(n, m)$ is the Delannoy number $D(n-1, m-1)$, because a path is a lattice path from $(0, 0)$ to $(n-1, m-1)$ with the steps east, north and northeast. For $n = m = 1, \ldots, 6$ this is $1, 3, 13, 63, 321, 1683$. The table has $n m$ cells, so the dynamic program replaces an exponential search by a quadratic one.
