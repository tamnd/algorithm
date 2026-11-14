---
title: The SDM model is the second-order Taylor model of the squared distance, its weight lies between the tangent and the point distance, each step is a convex least-squares problem, the energy never increases, and exact data give a fixed point
proves: [correctness, termination]
status: full
---

**Setup.** $C : [a, b] \to \mathbb{R}^2$ is a $C^2$ curve with $C'(t) \ne 0$. At a parameter $t$ let $T = C'/\lvert C' \rvert$, let $N$ be $T$ turned left by $90$ degrees, and let $\kappa$ be the signed curvature, so that
$$ C'' = \bigl( \lvert C' \rvert \bigr)' \, T + \kappa \lvert C' \rvert^2 N . \tag{1} $$
For a point $X$, $F(X) = \min_{s \in [a, b]} \lvert X - C(s) \rvert^2$ is the squared distance to the curve. A foot point of $X$ is a parameter $t_0$ where the minimum is attained; write $K = C(t_0)$ and $d = (X - K) \cdot N$. The SDM weight is $w = \kappa d / (\kappa d - 1)$; when $\kappa \ne 0$ and $\rho = 1/\kappa$, this is $d / (d - \rho)$.

**Lemma 1 (foot point conditions).** If $t_0$ is a foot point of $X$ inside $(a, b)$, then $X - K = d N$ and $\kappa d \le 1$.

*Proof.* Let $g(t) = \lvert X - C(t) \rvert^2$. Since $t_0$ is an interior minimum, $g'(t_0) = -2 (X - K) \cdot C'(t_0) = 0$, so $X - K$ is normal to the curve and equals $d N$. Also $g''(t_0) \ge 0$. Now $g'' = 2 \lvert C' \rvert^2 - 2 (X - C) \cdot C''$, and by (1), $(X - K) \cdot C'' = d N \cdot C'' = \kappa d \lvert C' \rvert^2$. So $g''(t_0) = 2 \lvert C' \rvert^2 (1 - \kappa d) \ge 0$, and $\kappa d \le 1$. $\square$

**Theorem 1 (the second-order model).** Let $t_0$ be the only foot point of $X$, inside $(a, b)$, with $\kappa d < 1$. Then $F$ is $C^2$ near $X$, and for small $v$
$$ F(X + v) = w (v \cdot T)^2 + (d + v \cdot N)^2 + o(\lvert v \rvert^2) . \tag{2} $$

*Proof.* Let $G(t, Y) = (C(t) - Y) \cdot C'(t)$. Then $G(t_0, X) = 0$ and, by the computation of Lemma 1, $\partial G / \partial t = \lvert C' \rvert^2 + (C - Y) \cdot C'' = \lvert C' \rvert^2 (1 - \kappa d) > 0$ at $(t_0, X)$. By the implicit function theorem there is a $C^1$ function $t(Y)$ near $X$ with $t(X) = t_0$ and $G(t(Y), Y) = 0$, and it is the only zero of $G(\cdot, Y)$ near $t_0$.

It is also the foot point of $Y$. Take $Y_j \to X$ and foot points $s_j$ of $Y_j$. Every limit point $s$ of $(s_j)$ satisfies $\lvert X - C(s) \rvert^2 = \lim F(Y_j) = F(X)$, because $F$ is continuous (it is a minimum of functions that are $1$-Lipschitz in the distance). So $s$ is a foot point of $X$, and $s = t_0$. Hence $s_j \to t_0$, so $s_j$ is an interior minimum of $\lvert Y_j - C(s) \rvert^2$, a zero of $G(\cdot, Y_j)$ near $t_0$, and equal to $t(Y_j)$ for large $j$. So $F(Y) = \lvert Y - C(t(Y)) \rvert^2$ near $X$.

Differentiate: $\nabla F(Y) = 2 (Y - C(t)) - 2 \bigl( (Y - C(t)) \cdot C'(t) \bigr) \nabla t = 2 (Y - C(t(Y)))$, since the factor in parentheses is $-G = 0$. This is $C^1$, so $F$ is $C^2$, with $\nabla^2 F = 2 (I - C' \, \nabla t^{\mathsf T})$. Differentiating $G(t(Y), Y) = 0$ gives $\frac{\partial G}{\partial t} \nabla t - C' = 0$, so at $X$
$$ \nabla t = \frac{C'}{\lvert C' \rvert^2 (1 - \kappa d)}, \qquad \nabla^2 F(X) = 2 \Bigl( I - \frac{T T^{\mathsf T}}{1 - \kappa d} \Bigr) = 2 \Bigl( w \, T T^{\mathsf T} + N N^{\mathsf T} \Bigr), $$
using $I = T T^{\mathsf T} + N N^{\mathsf T}$ and $1 - \frac{1}{1 - \kappa d} = \frac{\kappa d}{\kappa d - 1} = w$. Taylor's theorem with $F(X) = d^2$ and $\nabla F(X) = 2 d N$ gives
$$ F(X + v) = d^2 + 2 d \, (v \cdot N) + w (v \cdot T)^2 + (v \cdot N)^2 + o(\lvert v \rvert^2), $$
which is (2). With $y = X + v$, $(y - K) \cdot T = v \cdot T$ and $(y - K) \cdot N = d + v \cdot N$, so (2) is the model $w ((y - K) \cdot T)^2 + ((y - K) \cdot N)^2$ of the page. $\square$

**Theorem 2 (the weight and its limits).** Let $x = \kappa d$.

1. If $x < 0$, then $0 < w < 1$. If $0 < x < 1$, then $w < 0$. If $x = 0$, then $w = 0$.
2. $w \to 0$ as $x \to 0$, that is, as $d \to 0$ or $\kappa \to 0$, and then the model tends to $((y - K) \cdot N)^2$, the squared distance to the tangent line (TDM).
3. $w \to 1$ as $x \to -\infty$, that is, as the point moves far away on the outer side, and then the model tends to $\lvert y - K \rvert^2$, the squared distance to the foot point (PDM).
4. With the clamp of line L4 ($w = 0$ when $0 \le x < 1$), every interior foot point gets a weight in $[0, 1)$, and the end feet get $w = 1$.

*Proof.* For $x < 0$, $w = \lvert x \rvert / (\lvert x \rvert + 1) \in (0, 1)$. For $0 < x < 1$, the numerator is positive and the denominator negative. The limits follow from the continuity of $x / (x - 1)$ at $0$ and from $x / (x - 1) = 1 / (1 - 1/x) \to 1$. The two limit models follow by putting $w = 0$ or $w = 1$ in the model, with $\lvert y - K \rvert^2 = ((y - K) \cdot T)^2 + ((y - K) \cdot N)^2$. By Lemma 1, $x \le 1$ at an interior foot point; $x = 1$ makes the formula undefined and $x \in [0, 1)$ is clamped to $0$, so the weight lies in $[0, 1)$. $\square$

Item 1 shows why line L4 clamps: for $0 < \kappa d < 1$, the true squared distance is not convex in the direction $T$, and an unclamped model would have no minimum.

**Theorem 3 (the step).** Fix the foot parameters $t_k$, the frames and the weights $w_k \in [0, 1]$ of lines L3 and L4. The function
$$ M(Q) = \sum_k \Bigl[ w_k \bigl( (C_Q(t_k) - X_k) \cdot T_k \bigr)^2 + \bigl( (C_Q(t_k) - X_k) \cdot N_k \bigr)^2 \Bigr] + \mu R(Q) + \nu \lvert Q - P \rvert^2 $$
with $\mu, \nu \ge 0$ is a convex quadratic function of the control points $Q$. Its minimizers are the solutions of a linear system $A Q = r$ with $A$ symmetric positive semidefinite, and for $\nu > 0$ the minimizer is unique.

*Proof.* $C_Q(t_k) = \sum_i N_{i,p}(t_k) Q_i$ is linear in $Q$, so each term in brackets, each second difference in $R(Q)$, and each coordinate of $Q - P$ is an affine function $\ell(Q) = c \cdot Q - e$. So $M = \sum_j \omega_j \ell_j(Q)^2$ with weights $\omega_j \ge 0$. Then $M(Q) = Q^{\mathsf T} A Q - 2 r^{\mathsf T} Q + \text{const}$ with $A = \sum_j \omega_j c_j c_j^{\mathsf T}$ positive semidefinite, so $M$ is convex, and $\nabla M = 2 (A Q - r) = 0$ characterizes its minimizers. For $\nu > 0$ the coordinates of $Q - P$ add $\nu I$ to $A$, so $A$ is positive definite and the solution is unique. $\square$

When $\nu = 0$ and all $w_k = 0$, a move of each $C_Q(t_k)$ along $T_k$ costs nothing in the data terms; on straight data this move can be a slide of the whole curve along the line, which $R$ does not see either, so $A$ is singular. This is why the code adds a small $\nu$.

**Theorem 4 (monotone energy and termination).** Let $f$ be the energy that the code computes, the sum over the data points of the squared distance to the computed foot point plus $\mu R$. The accepted energies $f_0, f_1, \dots$ satisfy $f_{j+1} \le f_j$, and the algorithm stops.

*Proof.* Line L6 tries $\alpha = 1, \frac12, \frac14, \dots$ and accepts a trial only when its energy is at most the current $f_j$; the code stops the halving when $\alpha$ falls below a fixed minimum step, and if no trial was accepted the algorithm returns the current $P$ without a change. So every accepted energy is at most the one before it. Each iteration does at most $\lceil \log_2 (1 / \alpha_{\min}) \rceil + 2$ energy evaluations, each with a fixed amount of work, and the outer loop runs at most the iteration limit. $\square$

When the computed foot points are global nearest points, $f$ is the true $\sum_k F(X_k) + \mu R$, and the theorem holds for the true energy.

**Theorem 5 (exact data give a fixed point).** Let $\mu = 0$, let every data point lie on the regular curve $C_P$, and let the foot points be computed exactly. Then $Q = P$ minimizes $M$, it is the only minimizer when $\nu > 0$ or when $A$ is nonsingular, and SDM returns $P$ unchanged with energy $0$.

*Proof.* Each $X_k$ has distance $0$, so its foot point is a parameter with $C_P(t_k) = X_k$. At $Q = P$ every data term vanishes, and so does $\nu \lvert Q - P \rvert^2$, so $M(P) = 0 \le M(Q)$ for every $Q$. When the minimizer is unique (Theorem 3), it is $P$, the step $Q - P$ is $0$, and the energy stays $0$. $\square$

**What is not proved.** Nothing here shows that the iterates converge, how fast, or to which local minimum. Wang, Pottmann and Liu relate SDM to a quasi-Newton method and TDM to the Gauss-Newton method; the fast convergence on the page is measured, not proved. $\blacksquare$
