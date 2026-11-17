---
title: The MAC grid operators give a symmetric pressure system, an exact divergence-free projection and no checkerboard null space
proves: [correctness]
status: full
---

We use the layout and the line numbers of the page. All statements are about exact arithmetic. A cell outside the grid is SOLID. For a FLUID cell $c$ let $N(c)$ be its four neighbors. A face is **open** if no side is SOLID and at least one side is FLUID; lines L5 to L7 change exactly the open inner faces. A face with a SOLID side is a **solid face**.

For a cell field $q$ with $q = 0$ on AIR cells, define the face field $G q$ by $(G q)_f = (q_{\text{high}} - q_{\text{low}}) / \Delta x$ on an open face $f$, where high and low are the cells on the side of larger and smaller index, and $(G q)_f = 0$ on every other face. Define $(D w)_c$ as line L4 computes it. Then line L6 and line L7 do $w \leftarrow w - \frac{\Delta t}{\rho} G p$.

**Lemma 1 (SAMPLE).** If $q[a][b] = \alpha (a + o_x)\Delta x + \beta (b + o_y) \Delta x + \gamma$ for all $a, b$, then SAMPLE returns $\alpha x + \beta y + \gamma$ at every point $(x, y)$ inside the box of the sample points. At any point, the result lies between the least and the largest of the four values used.

*Proof.* Inside the box, the clamps of line L1 do nothing, so $x = (f_x + o_x)\Delta x$ and $y = (f_y + o_y)\Delta x$. Line L2 picks $a \le f_x \le a + 1$ and $b \le f_y \le b + 1$, so $s, t \in [0, 1]$. The four weights of line L3 are $(1-s)(1-t)$, $(1-s)t$, $s(1-t)$ and $st$. They are nonnegative and sum to $1$, which proves the second claim at any point. The weighted sum of the $a$ indices is $(1-s)a + s(a+1) = a + s = f_x$, and in the same way the weighted sum of the $b$ indices is $f_y$. An affine function of the indices commutes with a weighted sum whose weights sum to 1, so the result is $\alpha (f_x + o_x)\Delta x + \beta (f_y + o_y)\Delta x + \gamma = \alpha x + \beta y + \gamma$. $\square$

**Lemma 2 (the pressure matrix).** For each FLUID cell $c$ and each cell field $p$ with $p = 0$ on AIR cells, $-\Delta x^2 (D G p)_c = (A p)_c$, where $A$ is the matrix of lines L8 and L9.

*Proof.* Each face of $c$ is either a solid face or an open face, because $c$ is FLUID. On a solid face $(G p)_f = 0$. On an open face toward the neighbor $n$, the outward flux of $G p$ is $(p_n - p_c)/\Delta x$: if $n$ has the larger index this is $(G p)_f$ with the sign $+$, and if $n$ has the smaller index it is $-(G p)_f = -(p_c - p_n)/\Delta x$. So

$$(D G p)_c = \frac{1}{\Delta x^2} \sum_{n \in N(c),\ n \text{ not SOLID}} (p_n - p_c).$$

An AIR neighbor has $p_n = 0$ and adds $-p_c$. A FLUID neighbor adds $p_n - p_c$. Lines L8 and L9 put $1$ on the diagonal for each non-SOLID neighbor and $-1$ in the column of each FLUID neighbor, so $(A p)_c = \sum_{n \text{ not SOLID}} p_c - \sum_{n \text{ FLUID}} p_n$, which is $-\Delta x^2 (D G p)_c$. $\square$

**Theorem 1 (zero divergence).** If $A p = b$ with $b$ from line L10, then after GRADIENT-UPDATE every FLUID cell has zero divergence.

*Proof.* Line L10 is $b_c = -\frac{\rho\,\Delta x^2}{\Delta t} (D w)_c$ for the old field $w$. GRADIENT-UPDATE gives $w' = w - \frac{\Delta t}{\rho} G p$, and $D$ is linear, so by Lemma 2

$$(D w')_c = (D w)_c - \frac{\Delta t}{\rho} (D G p)_c = (D w)_c + \frac{\Delta t}{\rho \Delta x^2} (A p)_c = (D w)_c + \frac{\Delta t}{\rho\,\Delta x^2} b_c = 0. \qquad \square$$

**Theorem 2 (the matrix).** $A$ is symmetric and positive semidefinite. Its null space is spanned by the indicator vectors of the connected components of FLUID cells (under 4-neighbor adjacency) that have no AIR neighbor. $A p = b$ has a solution if and only if, for each such closed component $K$, $\sum_{c \in K} b_c = 0$. For a closed component this sum is $-\frac{\rho\,\Delta x}{\Delta t}$ times the net outflow through the solid faces of $K$, so with fixed walls the condition always holds.

*Proof.* The entry $A_{cn} = -1$ for two FLUID neighbors is the same in row $c$ and in row $n$, so $A$ is symmetric. For a vector $x$ on the FLUID cells,

$$x^T A x = \sum_{\{c, n\} \text{ FLUID neighbors}} (x_c - x_n)^2 + \sum_{c \text{ FLUID},\ n \in N(c) \text{ AIR}} x_c^2 \ \ge\ 0,$$

which follows by collecting, for each pair of FLUID neighbors, the terms $x_c^2 - x_c x_n$ from row $c$ and $x_n^2 - x_n x_c$ from row $n$, and for each AIR neighbor the term $x_c^2$. So $x^T A x = 0$ if and only if $x$ is constant on each component and zero on each component with an AIR neighbor. For a positive semidefinite matrix, $A x = 0$ if and only if $x^T A x = 0$, which gives the null space. A symmetric system is solvable if and only if $b$ is orthogonal to the null space, that is, the sum of $b$ over each closed component is zero.

For the last claim, sum $\Delta x (D w)_c$ over $c \in K$. A face between two cells of $K$ appears twice with opposite signs. A face between a cell of $K$ and a cell outside $K$ is not toward a FLUID cell (else that cell would be in $K$) and not toward AIR (since $K$ is closed), so it is a solid face. What remains is the net outflow through the solid faces of $K$. With fixed walls, rule (S) makes every solid face zero. $\square$

The helper removes the mean of $b$ on each closed component before the solve. This makes the system consistent when rounding or a moving solid gives a small nonzero sum, and it then removes the mean of $p$ on the component, which picks one solution.

**Lemma 3 (summation by parts).** Let $w$ be a face field that is zero on every solid face. For every cell field $q$ with $q = 0$ on AIR cells,

$$\sum_{\text{faces } f} (G q)_f\, w_f = -\sum_{c \text{ FLUID}} q_c\, (D w)_c .$$

*Proof.* Only open faces have $(G q)_f \ne 0$. Write $(G q)_f w_f = (q_{\text{high}} w_f - q_{\text{low}} w_f)/\Delta x$ and give each term to its cell. Cell $c$ receives $-q_c w_f/\Delta x$ times the outward sign for each of its open faces: $-1$ for its right and top faces (it is the low cell) and $+1$ for its left and bottom faces. AIR cells have $q = 0$, and a SOLID cell has no open face. For a FLUID cell, the faces that are not open are solid faces, where $w = 0$, so the sum of the outward fluxes of its open faces is $\Delta x (D w)_c$. Hence the total is $-\sum_{c \text{ FLUID}} q_c (D w)_c$. $\square$

**Theorem 3 (energy).** With fixed walls (zero velocity on solid faces), let $w' = w - \frac{\Delta t}{\rho} G p$ with $A p = b$. Then $\sum_f w_f^2 = \sum_f w_f'^2 + \sum_f \left(\frac{\Delta t}{\rho} G p\right)_f^2$. So the projection does not increase the kinetic energy $\frac12 \rho \Delta x^2 \sum_f w_f^2$, and $w'$ is the closest field to $w$ in this norm among the fields with zero divergence on the FLUID cells, the same values on the faces that are not open, and zero on the solid faces.

*Proof.* $w'$ is zero on solid faces, because $G p$ is. By Theorem 1, $D w' = 0$ on FLUID cells, so Lemma 3 with $q = \frac{\Delta t}{\rho} p$ gives $\sum_f (G q)_f w'_f = 0$. Expand $\sum_f w_f^2 = \sum_f (w'_f + (G q)_f)^2$; the cross term is zero. For the second claim, let $z$ be any field with these properties. Then $z - w'$ is zero on all faces that are not open and has zero divergence on FLUID cells, so Lemma 3 gives $\sum_f (G q)_f (z_f - w'_f) = 0$, and $\sum_f (z_f - w_f)^2 = \sum_f (z_f - w'_f)^2 + \sum_f (G q)_f^2 \ge \sum_f (w'_f - w_f)^2$. $\square$

With a moving solid, the solid faces carry the solid velocity, Lemma 3 gets a boundary term, and the kinetic energy of the fluid can grow: the solid does work on it.

**Theorem 4 (no checkerboard on the MAC grid).** On a periodic $n$ by $n$ grid with $\Delta x = 1$, let $L_{\text{MAC}} = D G$ with the face differences of the MAC grid, and let $L_{\text{col}} = D_c G_c$ with $G_c p_i = (p_{i+1} - p_{i-1})/2$ and $D_c w_i = (w_{i+1} - w_{i-1})/2$ in each axis on a collocated grid. Then the null space of $L_{\text{MAC}}$ is the constants, and for even $n$ the null space of $L_{\text{col}}$ has dimension 4 and contains the checkerboard $(-1)^{i+j}$.

*Proof.* On the MAC grid, $(D G p)_{ij} = p_{i+1,j} + p_{i-1,j} + p_{i,j+1} + p_{i,j-1} - 4 p_{ij}$. On the collocated grid, $(D_c G_c p)_i = \frac12 \left( \frac{p_{i+2} - p_i}{2} - \frac{p_i - p_{i-2}}{2} \right) = \frac{p_{i+2} - 2 p_i + p_{i-2}}{4}$ in each axis: the two central differences skip the direct neighbors. Both operators are circulant in each axis, so the $n^2$ Fourier modes $e_{kl}(i, j) = \exp(2\pi\iota (k i + l j)/n)$, $0 \le k, l < n$, which form a basis, are eigenvectors. The eigenvalues are

$$\lambda_{\text{MAC}}(k, l) = -4 \sin^2\frac{\pi k}{n} - 4 \sin^2 \frac{\pi l}{n}, \qquad \lambda_{\text{col}}(k, l) = -\sin^2 \frac{2\pi k}{n} - \sin^2\frac{2 \pi l}{n}.$$

$\lambda_{\text{MAC}} = 0$ only for $k = l = 0$, the constant mode. $\lambda_{\text{col}} = 0$ when $2k/n$ and $2l/n$ are both integers, that is $k, l \in \{0, n/2\}$ for even $n$: four modes, which are real ($\pm 1$ patterns), and $k = l = n/2$ is the checkerboard. The real null space has the same dimension as the complex one, because the operators are real. For the checkerboard on the MAC grid, $\lambda_{\text{MAC}}(n/2, n/2) = -8$. $\square$

The test file checks Lemma 1 and Lemma 2 exactly with `fractions.Fraction` on a grid with SOLID and AIR cells, the symmetry of $A$, the nullities 1 and 4 for $n = 4$ and $n = 6$ by exact elimination, and Theorems 1 to 3 in floating point through the helper.
