---
title: Each zero-force move minimizes the spring energy along one coordinate, so the energy never increases in a round, and without spreading the sweeps converge to the quadratic placement
proves: [correctness, termination, running time]
status: full
---

Fix a round of the algorithm, so the extra forces $e_i$ are fixed, and write $\Phi$ for the energy of the page with these forces. The $x$ part and the $y$ part of $\Phi$ do not share a variable, so it is enough to treat $x$. Write $d_i = \sum_j w_{ij} > 0$ for each cell; the algorithm stops with an error if a cell has no spring.

**Lemma 1 (one move is the minimum along a coordinate).** Fix all coordinates except $x_i$. Then $\Phi$ as a function of $x_i$ is $\frac{d_i}{2} x_i^2 - \bigl( \sum_j w_{ij} x_j + e^x_i \bigr) x_i + c$ for a constant $c$. Its minimum over the interval $[W_i / 2, X - W_i / 2]$ is at the clamped value of $t = (\sum_j w_{ij} x_j + e^x_i) / d_i$, which line L6 sets.

*Proof.* The terms of $\Phi$ that contain $x_i$ are $\frac12 w_{ij} (x_i - x_j)^2$ for the springs at $i$ and $-e^x_i x_i$. Expanding gives the stated quadratic, whose second derivative is $d_i > 0$. A convex quadratic of one variable with its unconstrained minimum at $t$ is decreasing to the left of $t$ and increasing to the right. So on an interval its minimum is at $t$ if $t$ is inside, and otherwise at the end of the interval nearest to $t$; that is the clamped value. $\square$

**Theorem 1 (the energy does not increase in a round).** Let $\Phi_0, \Phi_1, \ldots$ be the values of $\Phi$ after each execution of line L6 in a round. Then $\Phi_0 \ge \Phi_1 \ge \cdots$.

*Proof.* Before the move, $x_i$ is a point of the interval, because the start point is in the region and every earlier move clamps. By Lemma 1, the new $x_i$ minimizes $\Phi$ over the interval with the other coordinates fixed, so its value is at most the value at the old $x_i$. The same holds for $y_i$. $\blacksquare$

**Lemma 2 (positive definite).** Let $A$ be the $n \times n$ matrix with $A_{ii} = d_i$ and $A_{ij} = -w_{ij}$ for two cells $i \ne j$. If every cell has a path of springs to a pad, then $A$ is symmetric and positive definite.

*Proof.* The weights are symmetric. For a vector $v$, $v^\top A v = \sum_{\{i, j\} \text{ cells}} w_{ij} (v_i - v_j)^2 + \sum_{i} \omega_i v_i^2$, where $\omega_i$ is the total stiffness of the springs from cell $i$ to pads. Both sums are at least 0. If $v^\top A v = 0$, then $v$ is constant along every spring between cells and $v_i = 0$ at every cell with a spring to a pad. A path of springs from any cell to a pad then gives $v = 0$ at that cell. $\square$

**Theorem 2 (convergence without spreading).** Let $\kappa = 0$ and suppose the clamp of line L6 never changes a value, for example when the region contains the convex hull of the pads. If every cell has a path of springs to a pad, then the positions after $T$ sweeps converge, as $T \to \infty$, to the unique minimum of $\Phi$, the solution of $A x = b$ with $b_i = \sum_{q \text{ pad}} w_{iq} x_q$.

*Proof.* With $e = 0$, $\Phi(x) = \frac12 x^\top A x - b^\top x + c$, so its gradient is $A x - b$, and by Lemma 2 its unique minimum is $A^{-1} b$. Line L6 without the clamp sets $x_i = (b_i - \sum_{j \ne i} A_{ij} x_j) / A_{ii}$ with the newest values of the other cells, which is exactly the update of the [Gauss-Seidel method](/gauss-seidel-method/) for $A x = b$. For a symmetric positive definite matrix, the Gauss-Seidel method converges to the solution from every start point (the Ostrowski-Reich theorem). $\blacksquare$

If the convex hull of the pads is inside the region, the clamp never acts on the limit, because the solution of $A x = b$ is a weighted mean of the neighbors at every cell and so lies in the hull. The theorem above assumes the clamp does not act during the sweeps either, which the start point inside the hull ensures, since each unclamped move takes a weighted mean of points of the hull.

**Theorem 3 (termination and running time).** The algorithm stops after $R T n$ moves and $R$ density steps, in $O(P + E + R (T (n + E) + G))$ time, where no cell is larger than a bin.

*Proof.* The loops of lines L3, L4 and L5 have fixed bounds $R$, $T$ and $n$. Line L1 visits each pair of pins of each net once, $O(P + E)$. Line L6 reads the $\deg(i)$ springs of cell $i$, and $\sum_i \deg(i) = 2 E_{\mathrm{cells}} + E_{\mathrm{pads}} \le 2 E$, so a sweep costs $O(n + E)$. A cell no larger than a bin overlaps at most 2 bins in each direction, so line L7 does $O(1)$ work per cell after $O(G)$ work to clear the bins, and lines L8 and L9 do $O(1)$ work per cell. $\blacksquare$
