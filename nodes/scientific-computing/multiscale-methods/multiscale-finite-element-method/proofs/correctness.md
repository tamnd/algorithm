---
title: In 1D the multiscale finite element method is exact at the coarse nodes and has an energy error of order H
proves: [correctness]
status: full
---

We prove two facts about the 1D method of the page, in exact arithmetic. The problem is $-(a u')' = f$ on $(0, 1)$ with $u(0) = u(1) = 0$ and $a \ge \alpha > 0$ piecewise constant on the fine mesh. Let $V_h$ be the fine P1 space with zero boundary values and $a(v, w) = \int_0^1 a v' w'$. The fine solution $u_h \in V_h$ solves $a(u_h, v) = (f_h, v)$ for all $v \in V_h$, where $f_h$ is the P1 interpolant of $f$. This is what `fine_solve_1d` computes.

**The multiscale space.** On a coarse element $K = [x_e, x_{e+1}]$, line L2 computes $\phi_K \in P1$ on the fine cells of $K$ with $\phi_K(x_e) = 0$, $\phi_K(x_{e+1}) = 1$ and

$$\int_K a\, \phi_K' v' = 0 \quad \text{for every fine P1 function } v \text{ on } K \text{ with } v(x_e) = v(x_{e+1}) = 0. \tag{1}$$

The system of line L2 is tridiagonal with a positive diagonal that dominates the row sums of the absolute values of the off-diagonal entries, with strict dominance in the first and last rows, so it has one solution and the Thomas algorithm needs no pivoting. The basis function $\psi_i$ of coarse node $x_i$ is $\phi_K$ on the element to the left of $x_i$, $1 - \phi_K$ on the element to the right, and 0 elsewhere. Let $V_{ms}$ be the span of $\psi_1, \ldots, \psi_{M-1}$. Lines L3 to L5 compute the Galerkin solution $u_{ms} \in V_{ms}$:

$$a(u_{ms}, \psi) = (f_h, \psi) \quad \text{for every } \psi \in V_{ms}. \tag{2}$$

Lines L3 compute $a(\psi_j, \psi_i)$ and $(f_h, \psi_i)$ element by element without error: on a fine cell, $\psi_i'$ is constant and $f_h \psi_i$ is a product of two linear functions, whose integral is the formula of `_fine_cell_load`. Line L4 adds the element values, and line L6 writes $u_{ms}$ on the fine mesh.

**Lemma 1 (the splitting).** Let $B = \{ v \in V_h : v(x_i) = 0 \text{ at every coarse node} \}$. Then $V_h = V_{ms} \oplus B$, and $a(\psi, b) = 0$ for all $\psi \in V_{ms}$ and $b \in B$.

*Proof.* A function in $V_{ms}$ is fixed by its values at the coarse nodes, since $\psi_i(x_j) = \delta_{ij}$. For $v \in V_h$, let $\Pi v = \sum_i v(x_i) \psi_i$. Then $v - \Pi v$ vanishes at every coarse node, so $v - \Pi v \in B$, and the sum is direct because a function of $V_{ms}$ that vanishes at all coarse nodes is zero. For the orthogonality, $b \in B$ restricted to $K$ is a fine P1 function with zero values at the ends of $K$, and on $K$ the function $\psi$ is a constant plus a multiple of $\phi_K$. A constant has zero derivative, and (1) gives $\int_K a\, \phi_K' b' = 0$. Summing over $K$ gives $a(\psi, b) = 0$. $\square$

**Theorem 1 (nodal exactness).** $u_{ms}(x_i) = u_h(x_i)$ at every coarse node, and $u_{ms} = \Pi u_h$.

*Proof.* Write $u_h = \Pi u_h + b$ with $b \in B$ by Lemma 1. For $\psi \in V_{ms}$,

$$a(\Pi u_h, \psi) = a(u_h, \psi) - a(b, \psi) = (f_h, \psi) - 0,$$

because $\psi \in V_h$ and by Lemma 1. So $\Pi u_h$ solves (2). The matrix of (2) is the Gram matrix of the linearly independent functions $\psi_i$ in the inner product $a$, so (2) has one solution, and $u_{ms} = \Pi u_h$. At a coarse node, $\Pi u_h(x_i) = u_h(x_i)$. $\square$

**Theorem 2 (energy error).** With $\|v\|_a = a(v, v)^{1/2}$ and $H$ the largest coarse element,

$$\|u_h - u_{ms}\|_a \le \frac{H}{\pi \sqrt \alpha}\, \|f_h\|_{L^2}.$$

*Proof.* By Theorem 1, $e = u_h - u_{ms} = b \in B$. For $v \in B$, Lemma 1 gives $a(u_{ms}, v) = 0$, so $a(e, v) = a(u_h, v) = (f_h, v)$. Take $v = e$ and restrict to one element $K$ of length $H_K$; the function $e$ vanishes at both ends of $K$, and $e|_K$ extended by zero lies in $B$, so

$$\|e\|_{a, K}^2 = (f_h, e)_K \le \|f_h\|_{L^2(K)} \|e\|_{L^2(K)} \le \|f_h\|_{L^2(K)} \frac{H_K}{\pi} \|e'\|_{L^2(K)} \le \|f_h\|_{L^2(K)} \frac{H_K}{\pi \sqrt \alpha} \|e\|_{a, K}.$$

The second step is the Poincare inequality $\|w\|_{L^2(0, L)} \le (L/\pi) \|w'\|_{L^2(0, L)}$ for $w \in H^1_0(0, L)$, whose best constant is the inverse square root of the first Dirichlet eigenvalue $(\pi/L)^2$. The third uses $a \ge \alpha$. Divide by $\|e\|_{a, K}$, square, and add over $K$. $\square$

The bound does not depend on the fine structure of $a$, only on its lower bound. This is the point of the method: the coarse space carries the oscillations of $u_h$, and what it misses is a sum of local bubbles driven by $f$. In 2D and 3D, Lemma 1 fails: a fine function that vanishes at the coarse nodes need not vanish on the coarse edges, so it is not $a$-orthogonal to $V_{ms}$, and the boundary data of the local problems add an extra resonance error. The proof above is for 1D only.
