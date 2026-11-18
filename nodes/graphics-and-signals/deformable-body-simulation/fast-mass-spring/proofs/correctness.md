---
title: The local and global steps decrease the backward Euler objective, keep momentum, and stop only at a solution
proves: [correctness]
status: full
---

We use the notation of the page.
The free particles are the unknowns; a pinned particle is a constant.
$M$ is the diagonal mass matrix, $h$ the step, $\mathbf y = \mathbf x_n + h \alpha \mathbf v_n$ for the free particles, and a spring $i$ joins $a_i$ and $b_i$ with rest length $r_i$ and stiffness $k_i$.
The objective of one backward Euler step is

$$g(\mathbf x) = \tfrac12 (\mathbf x - \mathbf y)^\top M (\mathbf x - \mathbf y) + h^2 \Big( \sum_i \tfrac12 k_i (|\mathbf x_{a_i} - \mathbf x_{b_i}| - r_i)^2 - \mathbf x^\top \mathbf f_{\text{ext}} \Big).$$

Its gradient is $M(\mathbf x - \mathbf y) - h^2 (\mathbf f(\mathbf x) + \mathbf f_{\text{ext}})$, so $\nabla g(\mathbf x) = 0$ is the backward Euler equation $M(\mathbf x - \mathbf y) = h^2 (\mathbf f(\mathbf x) + \mathbf f_{\text{ext}})$ with $\mathbf v_{n+1} = (\mathbf x - \mathbf x_n)/h$ (Liu et al. 2013, equations (5) to (8), with $\alpha = 1$).

## The spring terms as a minimum

**Lemma 1 (Liu et al. 2013, Section 4).** For $\mathbf p \in \mathbb R^2$ and $r \ge 0$, $(|\mathbf p| - r)^2 = \min_{|\mathbf d| = r} |\mathbf p - \mathbf d|^2$, and for $\mathbf p \ne 0$ the minimum is at $\mathbf d = r \mathbf p / |\mathbf p|$.

*Proof.*
For $|\mathbf d| = r$, the reverse triangle inequality gives $|\mathbf p - \mathbf d| \ge \big||\mathbf p| - |\mathbf d|\big| = \big||\mathbf p| - r\big|$.
For $\mathbf d = r \mathbf p / |\mathbf p|$, $\mathbf p - \mathbf d = (|\mathbf p| - r)\mathbf p / |\mathbf p|$, which has the length $\big||\mathbf p| - r\big|$.
Equality in the reverse triangle inequality for $\mathbf p \ne 0$ and $r > 0$ needs $\mathbf d$ to point along $\mathbf p$, so the minimizer is unique then. $\square$

Define, for spring vectors $\mathbf d = (\mathbf d_1, \dots, \mathbf d_s)$ with $|\mathbf d_i| = r_i$,

$$G(\mathbf x, \mathbf d) = \tfrac12 (\mathbf x - \mathbf y)^\top M (\mathbf x - \mathbf y) + h^2 \Big( \sum_i \tfrac12 k_i |\mathbf x_{a_i} - \mathbf x_{b_i} - \mathbf d_i|^2 - \mathbf x^\top \mathbf f_{\text{ext}} \Big).$$

By Lemma 1, $g(\mathbf x) = \min_{\mathbf d} G(\mathbf x, \mathbf d)$, and the minimum is at the $\mathbf d$ of line L5 (the local step).

## The global step

**Lemma 2.** For a fixed $\mathbf d$, $G(\cdot, \mathbf d)$ has exactly one minimizer, the solution of $A \mathbf x = M \mathbf y + h^2 (J \mathbf d + \mathbf f_{\text{ext}}) + \mathbf c$ in each coordinate, where $A = M + h^2 L$ on the free particles and $\mathbf c$ holds the pinned terms. Lines L6 and L7 compute it.

*Proof.*
Expand the spring sum: $\sum_i \frac12 k_i |\mathbf x_{a_i} - \mathbf x_{b_i}|^2 = \frac12 \mathbf x^\top L \mathbf x$ with the graph Laplacian $L$ weighted by $k_i$ (diagonal entry $\sum k_i$ over the springs at a particle, off-diagonal entry $-k_i$), and $\sum_i k_i (\mathbf x_{a_i} - \mathbf x_{b_i}) \cdot \mathbf d_i = \mathbf x^\top J \mathbf d$, where $J\mathbf d$ has $+k_i \mathbf d_i$ at $a_i$ and $-k_i \mathbf d_i$ at $b_i$.
When a spring has one pinned end $q$, the terms with $\mathbf x_q$ are constants or linear in the free unknowns, and they give $\mathbf c$, which is $+h^2 k_i \mathbf x_q$ at the free end.
So $G$ is a quadratic with the Hessian $A$ in each coordinate.
$L$ is positive semidefinite, because $\mathbf x^\top L \mathbf x = \sum k_i |\mathbf x_{a_i} - \mathbf x_{b_i}|^2 \ge 0$ (with pinned ends set to zero), and $M$ is diagonal with positive masses, so $A$ is symmetric positive definite.
The minimizer is the unique solution of $\nabla_{\mathbf x} G = 0$, which is the stated system.
$A$ does not depend on $\mathbf x$, $\mathbf d$ or $\mathbf y$, so its Cholesky factor from line L1 serves every iteration and every step, as long as $h$, the masses, the stiffnesses, the pins and the springs stay the same. $\square$

**The banded factor.** The code orders the particles row by row, so $A_{ij} = 0$ for $|i - j| > b$, with $b$ the half bandwidth. The Cholesky formulas $R_{ij} = (A_{ij} - \sum_{k<j} R_{ik} R_{jk}) / R_{jj}$ give $R_{ij} = 0$ for $i - j > b$ by induction on $j$: every product $R_{ik} R_{jk}$ with $k < j$ has $i - k > b$, so it is zero. So the code may skip the entries outside the band, and it computes the same factor as a dense Cholesky decomposition.

## Descent and fixed points

**Theorem 3.** Each local step followed by a global step does not increase $g$.

*Proof.*
Let $\mathbf d^j$ be the local step at $\mathbf x^j$ and $\mathbf x^{j+1}$ the global step for $\mathbf d^j$.
Then $g(\mathbf x^{j+1}) = \min_{\mathbf d} G(\mathbf x^{j+1}, \mathbf d) \le G(\mathbf x^{j+1}, \mathbf d^j) \le G(\mathbf x^j, \mathbf d^j) = g(\mathbf x^j)$.
The first inequality is the minimum over $\mathbf d$, the second is Lemma 2, and the last equality is Lemma 1. $\square$

The sequence $g(\mathbf x^j)$ is bounded below, because $g \ge \frac12 (\mathbf x - \mathbf y)^\top M (\mathbf x - \mathbf y) - h^2 \mathbf x^\top \mathbf f_{\text{ext}}$, which is bounded below. So the values converge.

**Theorem 4.** If $\mathbf x$ is a fixed point of the iteration and no spring has length zero at $\mathbf x$, then $\nabla g(\mathbf x) = 0$, so $\mathbf x$ solves the backward Euler step.

*Proof.*
Let $\mathbf d^\star$ be the local step at $\mathbf x$. A fixed point means that $\mathbf x$ minimizes $G(\cdot, \mathbf d^\star)$, so $\nabla_{\mathbf x} G(\mathbf x, \mathbf d^\star) = 0$.
The function $\phi(\mathbf z) = G(\mathbf z, \mathbf d^\star) - g(\mathbf z)$ is at least zero everywhere (Lemma 1) and is zero at $\mathbf z = \mathbf x$.
Both terms are differentiable near $\mathbf x$, since no spring has length zero there, so $\mathbf x$ is a minimum of $\phi$ and $\nabla \phi(\mathbf x) = 0$.
Hence $\nabla g(\mathbf x) = \nabla_{\mathbf x} G(\mathbf x, \mathbf d^\star) = 0$. $\square$

$g$ is not convex in general, so the iteration finds a stationary point of $g$, not always the global minimum. The rate of convergence is linear in the measurements of the page and of Liu et al. (Figure 2); this page proves no rate.

## Momentum

**Theorem 5.** With no pins, after any number of iterations, $\sum_i m_i \mathbf v_{n+1, i} = \alpha \sum_i m_i \mathbf v_{n, i} + h \sum_i \mathbf f_{\text{ext}, i}$. With $\alpha = 1$ the step keeps the linear momentum of the backward Euler step exactly in exact arithmetic.

*Proof.*
Sum the rows of the system of Lemma 2.
Each row of $L$ sums to zero, so $\mathbf 1^\top L = 0$, and $J \mathbf d$ adds $+k_i \mathbf d_i$ and $-k_i \mathbf d_i$ for each spring, so its sum is zero.
So $\sum m_i \mathbf x_i = \sum m_i \mathbf y_i + h^2 \sum \mathbf f_{\text{ext}, i}$ after the global step, whatever $\mathbf d$ was.
Subtract $\sum m_i \mathbf x_{n,i}$ and divide by $h$, using $\mathbf y = \mathbf x_n + h \alpha \mathbf v_n$ and line L8. $\square$

## Stable is not accurate

**Theorem 6.** Let one particle of mass $m$ move on a line, joined to a pinned particle by one spring along the line, with no gravity and $\alpha = 1$. If the spring length stays positive, one iteration gives the exact backward Euler step, and the energy $\frac12 m v^2 + \frac12 k u^2$, with $u$ the stretch, is multiplied by $1/(1 + \omega^2 h^2)$ at each step, $\omega^2 = k/m$.

*Proof.*
The direction of the spring does not change, so the local step at $\mathbf y$ already gives the $\mathbf d$ of the solution, and the global step solves the linear backward Euler equations $u' = u + h v'$, $v' = v - h \omega^2 u'$.
So $u' = (u + h v)/(1 + \omega^2 h^2)$ and $v' = (v - h \omega^2 u)/(1 + \omega^2 h^2)$.
Then $\omega^2 u'^2 + v'^2 = \big(\omega^2 (u + h v)^2 + (v - h \omega^2 u)^2\big)/(1 + \omega^2 h^2)^2$.
The cross terms cancel, and the numerator is $(\omega^2 u^2 + v^2)(1 + \omega^2 h^2)$. $\square$

With $k = 100$ N/m, $m = 1$ kg and $h = 0.1$ s, $\omega h = 1$ and each step halves the energy. The step is stable for every $h$, and the energy loss is a property of backward Euler, not of the spring.
