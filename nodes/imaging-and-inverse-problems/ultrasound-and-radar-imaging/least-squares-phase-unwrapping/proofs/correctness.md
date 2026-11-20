---
title: The least squares unwrapped phase solves the discrete Poisson equation with Neumann boundary conditions, the DCT solves that equation exactly, and the result is exact when the wrapped gradient has no residues
proves: [correctness]
status: full
---

Notation. The grid has $m$ rows and $n$ columns. $D$ maps an image $\varphi$ to its forward differences on the $m(n-1)$ horizontal edges and the $(m-1)n$ vertical edges: $(D \varphi)_{e} = \varphi(q) - \varphi(p)$ for the edge $e = (p, q)$ that points right or down. The data are the wrapped differences $g_e = W(\psi(q) - \psi(p))$ (line L1). The method minimizes $J(\varphi) = \|D \varphi - g\|^2$.

**Lemma 1 (the normal equations are a Neumann Poisson equation).** $\varphi$ minimizes $J$ if and only if $\Delta \varphi = \rho$, where $(\Delta \varphi)(p) = \sum_{q \sim p} (\varphi(q) - \varphi(p))$ sums over the neighbours $q$ of $p$ that lie in the grid, and $\rho = $ line L2, $\rho(i, j) = g^x_{i,j} - g^x_{i,j-1} + g^y_{i,j} - g^y_{i-1,j}$ with missing terms equal to zero.

*Proof.* $J$ is a convex quadratic, so $\varphi$ minimizes it if and only if $D^T D \varphi = D^T g$. For one edge $e = (p, q)$, $D^T$ puts $-g_e$ at $p$ and $+g_e$ at $q$. So $(D^T g)(p)$ is the sum of $g_e$ over edges that end at $p$ minus the sum over edges that start at $p$, which is $-\rho(p)$. In the same way $(D^T D \varphi)(p) = \sum_{q \sim p} (\varphi(p) - \varphi(q)) = -(\Delta \varphi)(p)$. A pixel on the border has fewer neighbours; this is the discrete form of the Neumann condition $\partial \varphi / \partial \nu = g \cdot \nu$, here with the boundary flux taken as zero. $\square$

**Lemma 2 (solvability and uniqueness).** The kernel of $\Delta$ is the constant images, $\sum_p \rho(p) = 0$, and the solutions of $\Delta \varphi = \rho$ are one image plus any constant.

*Proof.* $\varphi^T (-\Delta) \varphi = \|D \varphi\|^2$, which is zero if and only if $\varphi$ is equal on the two ends of every edge, that is constant, since the grid graph is connected. $\rho = -D^T g$ is in the range of $D^T$, which is orthogonal to the kernel of $D$, the constants; so $\sum_p \rho(p) = 0$. A symmetric matrix maps onto the orthogonal complement of its kernel, so a solution exists, and two solutions differ by an element of the kernel. $\square$

**Lemma 3 (the DCT diagonalizes the Neumann Laplacian).** Let $c_k(t) = \cos(\pi k (2t + 1)/(2n))$ for $t, k = 0 \ldots n-1$. Then the one-dimensional Neumann Laplacian on $n$ points, $(L f)(t) = \sum_{s \in \{t-1, t+1\} \cap [0, n-1]} (f(s) - f(t))$, satisfies $L c_k = (2 \cos(\pi k / n) - 2)\, c_k$. In two dimensions, $\Delta (c_k \otimes c_l) = (2 \cos(\pi k/m) + 2 \cos(\pi l/n) - 4)\, c_k \otimes c_l$, and the eigenvalue is zero only for $k = l = 0$.

*Proof.* Extend $c_k$ to all integers $t$ by the same formula. The identity $\cos(a - b) + \cos(a + b) = 2 \cos a \cos b$ with $a = \pi k (2t+1)/(2n)$ and $b = \pi k / n$ gives $c_k(t-1) + c_k(t+1) - 2 c_k(t) = (2 \cos(\pi k/n) - 2) c_k(t)$ for every $t$. At $t = 0$ the missing neighbour has $c_k(-1) = \cos(-\pi k/(2n)) = c_k(0)$, so the term $c_k(-1) - c_k(0)$ is zero and dropping it changes nothing. At $t = n - 1$, $c_k(n) = \cos(\pi k + \pi k/(2n)) = (-1)^k \cos(\pi k/(2n)) = \cos(\pi k - \pi k/(2n)) = c_k(n-1)$, so again the missing term is zero. The two-dimensional Laplacian is the sum of the one-dimensional ones along rows and columns, which gives the second formula. $2\cos(\pi k/m) - 2 < 0$ for $0 < k < m$, so the sum is zero only when $k = l = 0$. $\square$

The vectors $c_0, \dots, c_{n-1}$ are orthogonal with $\|c_0\|^2 = n$ and $\|c_k\|^2 = n/2$ for $k \ge 1$ (eigenvectors of a symmetric matrix for distinct eigenvalues, and a direct sum for the norms). So the DCT-II of line L3, $\hat x(k, l) = \sum_{i, j} x(i, j) c_k(i) c_l(j)$, has the inverse of line L6 with the weights $1/(mn)$, $2/(mn)$ and $4/(mn)$, as in the code.

**Theorem 1 (lines L1 to L7 return a least squares solution).** The output $\varphi$ of lines L1 to L7 minimizes $J$, and it is the minimizer with zero mean.

*Proof.* Write $\rho = \sum_{k, l} \frac{w_k w_l}{mn} \hat\rho(k, l)\, c_k \otimes c_l$ by the inverse DCT. By Lemma 2, $\hat \rho(0, 0) = \sum_p \rho(p) = 0$. Line L4 sets $\hat\varphi(k, l) = \hat\rho(k, l)/\lambda_{kl}$ with $\lambda_{kl}$ from Lemma 3, and line L5 sets $\hat\varphi(0, 0) = 0$. By Lemma 3 and linearity, $\Delta \varphi = \sum_{(k, l) \ne (0, 0)} \frac{w_k w_l}{mn} \hat\rho(k, l)\, c_k \otimes c_l = \rho$, using $\hat\rho(0,0) = 0$. By Lemma 1, $\varphi$ minimizes $J$. The mean of $\varphi$ is $\hat\varphi(0, 0)/(mn) = 0$. $\square$

**Theorem 2 (exact without residues).** Suppose that every $2 \times 2$ loop of $g$ sums to zero (no residues). Then $\min J = 0$, the output satisfies $\varphi(q) - \varphi(p) = g_e$ on every edge, and $\varphi$ is congruent to $\psi$ up to a constant: $\varphi - \psi + C \in 2 \pi \mathbb{Z}$ for one real $C$. If in addition the true phase $\varphi^*$ satisfies $|\varphi^*(q) - \varphi^*(p)| < \pi$ on every edge (the Itoh condition), then $\varphi = \varphi^* - \text{mean}(\varphi^*)$.

*Proof.* Define $\varphi_0(p)$ as the sum of $g$ along any path of grid edges from the pixel $(0, 0)$ to $p$ (with a minus sign for edges walked backwards). Any two such paths differ by a closed walk, and every closed walk on the grid graph is a sum of boundaries of $2 \times 2$ squares, so the sum of $g$ along it is a sum of loop sums, which are zero. So $\varphi_0$ is well defined, $D \varphi_0 = g$ and $J(\varphi_0) = 0$. By Lemma 2 every minimizer, and the output by Theorem 1, is $\varphi_0$ plus a constant. Each $g_e$ differs from $\psi(q) - \psi(p)$ by a multiple of $2\pi$, so $\varphi_0 - \psi + \psi(0, 0)$ is a multiple of $2\pi$ at every pixel. Under the Itoh condition, $W(\psi(q) - \psi(p)) = W(\varphi^*(q) - \varphi^*(p)) = \varphi^*(q) - \varphi^*(p)$, so $D \varphi^* = g$ and $\varphi^*$ is also a minimizer with $J = 0$; Lemma 2 gives equality up to a constant. $\square$

**Theorem 3 (with residues the error spreads).** Let $r = g - D\varphi$ be the misfit of the output. Then $D^T r = 0$, and for every closed loop $\gamma$ the sum of $r$ along $\gamma$ equals the sum of $g$ along $\gamma$, which is $2\pi$ times the total residue charge enclosed. In particular, if some residue is nonzero, then $r \ne 0$ and $\min J > 0$: no image reproduces all the wrapped differences.

*Proof.* $D^T r = D^T g - D^T D \varphi = 0$ by the normal equations. The sum of $D\varphi$ along any closed loop is zero (it telescopes), so the loop sums of $r$ and $g$ agree. The boundary of a square with charge $q \ne 0$ has the loop sum $2 \pi q \ne 0$, so some edge on it has $r_e \ne 0$. $\square$

For the grid of one $2 \times 2$ square with charge $+1$, $D^T r = 0$ at each corner says that the misfit entering the corner equals the misfit leaving it, so $r$ has the same value on the four edges in the loop direction, and the loop sum gives $r_e = \pi/2$: the error of $2\pi$ is shared equally. Then $\varphi(q) - \varphi(p) = g_e - \pi/2$ on each edge, which is not congruent to $\psi(q) - \psi(p)$ modulo $2\pi$. This is the worked example of the main page. In general $r = g - D\varphi$ is the orthogonal projection of $g$ onto the kernel of $D^T$ (the cycle space of the grid graph), because $D\varphi$ is the projection onto the range of $D$. By Theorem 3, every closed loop that encloses a nonzero total charge has a nonzero loop sum of $r$, so $r$ is nonzero on at least one edge of each such loop, however far it is from the residues. The misfit forced by a residue cannot stay on the four edges around it. This is why least squares unwrapping spreads local errors over a wide area.

**Lemma 4 (invariance).** If $\psi'(p) = \psi(p) + 2 \pi k(p)$ for integers $k(p)$, the output is unchanged.

*Proof.* $W(\psi'(q) - \psi'(p)) = W(\psi(q) - \psi(p) + 2\pi(k(q) - k(p))) = W(\psi(q) - \psi(p))$, so $g$ and everything after line L1 are unchanged. $\square$

**Theorem 4 (cost).** With a fast DCT, lines L1 to L7 cost $O(m n \log(m n))$ operations and $O(m n)$ space. The direct sums of the reference code cost $O(m n (m + n))$.

*Proof.* Lines L1, L2, L4, L5 and L7 cost $O(1)$ per pixel. A two-dimensional DCT is $m$ transforms of length $n$ and $n$ transforms of length $m$; a fast DCT of length $n$ costs $O(n \log n)$, and a direct one $O(n^2)$. Every array has $m n$ entries. $\square$
