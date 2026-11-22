---
title: The backward step, the fixed points and the linear convergence of forward-backward splitting for the poison objective with linear features
proves: [correctness]
status: full
---

**Setting.** $F(x) = h(x) + g(x)$ over $\mathbb{R}^d$, with the feature term $h(x) = \lVert f(x) - f(t) \rVert^2$ and $g(x) = \beta \lVert x - b \rVert^2 + \iota(x)$, where $\iota$ is $0$ on the box $B = [0, 1]^d$ and $+\infty$ outside, $\beta > 0$ and $b \in B$. One iteration of lines L3 and L4 is $T(x) = P(x - \lambda \nabla h(x))$ with $P(u) = \operatorname{clip}_B\big((u + c\, b)/(1 + c)\big)$ and $c = 2\lambda\beta$.

**Claim 1 (the backward step).** For every $u$, $P(u)$ is the unique minimizer over $B$ of $q_u(x) = \beta \lVert x - b \rVert^2 + \frac{1}{2\lambda}\lVert x - u \rVert^2$.

*Proof.* $q_u$ is a sum over coordinates of $\beta (x_j - b_j)^2 + \frac{1}{2\lambda}(x_j - u_j)^2$, and $B$ is a product of intervals, so the problem splits into $d$ problems in one variable. Each is a strictly convex quadratic with derivative $2\beta(x_j - b_j) + (x_j - u_j)/\lambda$, which is zero at $m_j = (u_j + 2\lambda\beta\, b_j)/(1 + 2\lambda\beta)$. A strictly convex function of one variable decreases up to $m_j$ and increases after it, so its minimizer on $[0, 1]$ is $m_j$ clipped to $[0, 1]$. $\square$

**Claim 2 (fixed points are minimizers).** Let $h$ be convex and differentiable. Then $x = T(x)$ if and only if $x$ minimizes $F$ over $B$.

*Proof.* By Claim 1, $x = T(x)$ means that $x$ minimizes the convex function $g(z) + \frac{1}{2\lambda}\lVert z - (x - \lambda \nabla h(x)) \rVert^2$, that is, $0 \in \partial g(x) + \frac{1}{\lambda}\big(x - x + \lambda \nabla h(x)\big) = \partial g(x) + \nabla h(x)$. Since $h$ is differentiable, $\partial F(x) = \nabla h(x) + \partial g(x)$, so this says $0 \in \partial F(x)$, which for the convex $F$ means that $x$ is a minimizer. $\square$

**Claim 3 (linear convergence for linear features).** Let $f(x) = A x$ and $0 < \lambda \le 1/(2\lVert A \rVert_2^2)$. Then $F$ has a unique minimizer $x^*$ over $B$, and the iterates $x_0 = b$, $x_{p+1} = T(x_p)$ satisfy

$$\lVert x_p - x^* \rVert \le (1 + 2\lambda\beta)^{-p}\, \lVert b - x^* \rVert .$$

*Proof.* Here $h(x) = \lVert A(x - t) \rVert^2$ is convex with $\nabla h(x) = 2A^\top A (x - t)$. The forward map $G(x) = x - \lambda\nabla h(x)$ has $G(x) - G(y) = (I - 2\lambda A^\top A)(x - y)$. The symmetric matrix $I - 2\lambda A^\top A$ has the eigenvalues $1 - 2\lambda\sigma_i^2$, where the $\sigma_i^2 \le \lVert A \rVert_2^2$ are the eigenvalues of $A^\top A$, so they lie in $[0, 1]$ and $\lVert G(x) - G(y) \rVert \le \lVert x - y \rVert$. The map $\operatorname{clip}_B$ is the Euclidean projection onto a convex set and is $1$-Lipschitz, so $\lVert P(u) - P(v) \rVert \le \lVert u - v \rVert / (1 + c)$. Hence $T = P \circ G$ is a contraction with factor $r = 1/(1 + 2\lambda\beta) < 1$ on the closed set $B$, which $T$ maps into itself. By the Banach fixed point theorem it has exactly one fixed point $x^*$, which by Claim 2 is a minimizer, and every minimizer is a fixed point, so the minimizer is unique. Finally $\lVert x_{p+1} - x^* \rVert = \lVert T(x_p) - T(x^*) \rVert \le r \lVert x_p - x^* \rVert$, and induction gives the bound. $\square$

**Claim 4 (the conditions that the tests check).** With $f(x) = A x$, $\nabla F(x) = 2A^\top A(x - t) + 2\beta(x - b)$ on $B$. A point $x \in B$ is the minimizer if and only if, for each $j$, $\partial_j F(x) \ge 0$ when $x_j = 0$, $\partial_j F(x) \le 0$ when $x_j = 1$, and $\partial_j F(x) = 0$ when $0 < x_j < 1$. If the solution $x^\circ$ of $(A^\top A + \beta I)x = A^\top A t + \beta b$ lies in $B$, then $x^* = x^\circ$.

*Proof.* $F$ is convex and differentiable on a neighborhood of $B$ (where $\iota = 0$), so $x$ minimizes it over $B$ if and only if $\langle \nabla F(x), y - x \rangle \ge 0$ for every $y \in B$. Taking $y$ equal to $x$ except in coordinate $j$ shows that the condition implies the three cases; conversely the three cases make every term $\partial_j F(x)(y_j - x_j)$ of the inner product nonnegative. The matrix $A^\top A + \beta I$ is positive definite, so $x^\circ$ is the unique zero of $\nabla F$, and it minimizes $F$ over $\mathbb{R}^d$; if it is in $B$ it minimizes $F$ over $B$, and by uniqueness it is $x^*$. $\square$

**Claim 5 (the gradient of the ReLU features).** Let $f(x) = \operatorname{relu}(W x + c_1)$ and let $x$ have no pre-activation equal to $0$. Then near $x$, $f(x) = D(Wx + c_1)$ with the fixed diagonal $0/1$ matrix $D$ of the active units, $h$ is a convex quadratic there, and $\nabla h(x) = 2W^\top D (f(x) - f(t))$, which is what relu_collision_grad returns.

*Proof.* Each pre-activation is continuous, so its sign is constant near $x$, and so is $D$. Then $f$ is affine near $x$, $h(x) = \lVert D(Wx + c_1) - f(t) \rVert^2$ is a convex quadratic, and the chain rule gives $\nabla h(x) = 2 W^\top D^\top (D(Wx + c_1) - f(t)) = 2W^\top D(f(x) - f(t))$, since $D^\top = D$ and $D(Wx + c_1) = f(x)$ near $x$. The code sums $2(\text{pre}_i - f_i(t)) W_i$ over the active units $i$, which is the same vector, because $\text{pre}_i = f_i(x)$ for an active unit. $\square$

**The algorithm.** Line L1 starts at $b \in B$; lines L3 and L4 are $T$; by Claim 3 the iterates converge linearly to the unique minimizer for linear features and a step in the allowed range, and the tests check Claim 4 on the result. For ReLU features $h$ is not convex, Claim 2 does not apply, and nothing is claimed beyond Claim 5 and Claim 1; that the target flips after training is a measurement. $\blacksquare$
