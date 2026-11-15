---
title: SLIM splits into one strongly convex problem per column, and cyclic coordinate descent with the nonnegative soft threshold converges to its unique minimizer
proves: [correctness]
status: full
---

The notation is that of the page. $A$ is the $m \times n$ user-item matrix with columns $a_1, \dots, a_n$, $\beta > 0$ and $\lambda \ge 0$. SLIM minimizes

$$F(W) = \tfrac12 \lVert A - A W \rVert_F^2 + \tfrac{\beta}{2} \lVert W \rVert_F^2 + \lambda \lVert W \rVert_1 \quad \text{subject to } W \ge 0, \; \operatorname{diag}(W) = 0.$$

All statements are about exact arithmetic.

**Lemma 1 (columns are independent).** $F(W) = \sum_j f_j(w_j)$, where $w_j$ is column $j$ of $W$ and

$$f_j(w) = \tfrac12 \lVert a_j - A w \rVert^2 + \tfrac{\beta}{2} \lVert w \rVert^2 + \lambda \sum_k |w_k|,$$

and the constraints are $w \ge 0$ and $w_j = 0$ for each column separately. So $W$ is optimal if and only if each column $w_j$ minimizes $f_j$ over $C_j = \{w \in \mathbb{R}^n : w \ge 0, w_j = 0\}$.

*Proof.* Column $j$ of $A - AW$ is $a_j - A w_j$, the squared Frobenius norm is the sum of the squared norms of the columns, and both penalties are sums over the entries. The constraints restrict each column alone. $\square$

Fix $j$ and write $f = f_j$ and $C = C_j$. On $C$ every $|w_k| = w_k$, so on $C$

$$f(w) = h(w) + \lambda \mathbf{1}^\top w, \qquad h(w) = \tfrac12 \lVert a_j - A w \rVert^2 + \tfrac{\beta}{2} \lVert w \rVert^2,$$

a quadratic function. Its Hessian is $A^\top A + \beta I$, which is positive definite since $\beta > 0$, so $f$ is strongly convex on $C$ with modulus at least $\beta$.

**Lemma 2 (unique minimizer and its KKT conditions).** $f$ has a unique minimizer $w^*$ on $C$. A point $w \in C$ is $w^*$ if and only if, with $g_k = -a_k^\top (a_j - A w) + \beta w_k$, for every $k \ne j$

$$g_k + \lambda = 0 \text{ if } w_k > 0, \qquad g_k + \lambda \ge 0 \text{ if } w_k = 0.$$

*Proof.* $C$ is closed and convex and $f$ is continuous and strongly convex, so its sublevel sets in $C$ are bounded, a minimizer exists, and it is unique. $g_k$ is the partial derivative of $h$ in $w_k$, so $\nabla f = g + \lambda \mathbf{1}$ on $C$. The minimizer of a differentiable convex function over $C$ is characterized by $\nabla f(w)^\top (v - w) \ge 0$ for all $v \in C$. Since $C$ is a product of the sets $[0, \infty)$ for $k \ne j$ and $\{0\}$ for $k = j$, this splits into one condition per coordinate: for $k \ne j$, $(g_k + \lambda)(v_k - w_k) \ge 0$ for all $v_k \ge 0$, which is the stated pair of conditions; for $k = j$ there is no condition. These are the KKT conditions that the test file checks. $\square$

**Lemma 3 (the coordinate step is exact).** Fix all coordinates but $w_k$, $k \ne j$, with $\lVert a_k \rVert > 0$, and let $e = a_j - A w$ be the residual at the current point. As a function of $t = w_k \ge 0$, $f$ is

$$\phi(t) = \tfrac12 (\lVert a_k \rVert^2 + \beta) t^2 - \rho\, t + \lambda t + \text{const}, \qquad \rho = a_k^\top e + \lVert a_k \rVert^2 w_k,$$

and its unique minimizer over $t \ge 0$ is $t^* = \max(0, \rho - \lambda) / (\lVert a_k \rVert^2 + \beta)$, which is line L6. Moreover $\phi(w_k) - \phi(t^*) \ge \frac12 (\lVert a_k \rVert^2 + \beta) (w_k - t^*)^2$.

*Proof.* Let $e_0 = e + a_k w_k$, the residual without coordinate $k$. Then $a_j - A w = e_0 - a_k t$, and $\frac12 \lVert e_0 - a_k t \rVert^2 + \frac{\beta}{2} t^2 + \lambda t$ expands to the stated $\phi$ with $\rho = a_k^\top e_0 = a_k^\top e + \lVert a_k \rVert^2 w_k$. $\phi$ is a parabola with positive leading coefficient $c = \lVert a_k \rVert^2 + \beta$; its unconstrained minimizer is $(\rho - \lambda) / c$, and over $t \ge 0$ the minimizer is that value clipped at 0. For the last claim, $\phi(t) = \phi(t^*) + \phi'(t^*)(t - t^*) + \frac{c}{2} (t - t^*)^2$, and $\phi'(t^*)(t - t^*) \ge 0$ for every $t \ge 0$ by the optimality of $t^*$ on $[0, \infty)$. If $\lVert a_k \rVert = 0$, the code skips $k$ and keeps $w_k = 0$; then $\phi(t) = \frac{\beta}{2} t^2 + \lambda t + \text{const}$ is minimized at 0 anyway. $\square$

Line L7 updates the residual by $-a_k (t^* - w_k)$, so $e = a_j - A w$ holds again after the step, and the next step uses the correct $\rho$.

**Theorem 4 (convergence).** Let $w^{(0)} = 0$ and let $w^{(s)}$ be the point after $s$ single coordinate steps of lines L4 to L7 in cyclic order. Then $f(w^{(s)})$ does not increase, and $w^{(s)} \to w^*$.

*Proof.* Each step stays in $C$, since $t^* \ge 0$ and coordinate $j$ is never changed. By Lemma 3, each step lowers $f$ by at least $\frac{\beta}{2} \lVert w^{(s+1)} - w^{(s)} \rVert^2$. Since $f \ge 0$, summing over the steps gives $\sum_s \lVert w^{(s+1)} - w^{(s)} \rVert^2 \le 2 f(0) / \beta < \infty$, so the step lengths tend to 0. The iterates lie in the bounded sublevel set $\{w \in C : f(w) \le f(0)\}$, so they have limit points. Let $\bar w$ be the limit of a subsequence of points taken at the start of a sweep. Because the steps tend to 0, the points inside the same sweeps converge to $\bar w$ as well. Coordinate $k$ of the point after its step in that sweep is the clipped value of Lemma 3 at the point before the step, and the clipped value is a continuous function of the point, so in the limit $\bar w_k = \max(0, \bar\rho_k - \lambda) / (\lVert a_k \rVert^2 + \beta)$ for each $k \ne j$ with $a_k \ne 0$, with $\bar \rho_k$ computed at $\bar w$. That fixed-point equation says that $\bar w_k$ minimizes $f$ in coordinate $k$ over $[0, \infty)$, which is exactly the coordinate condition of Lemma 2 at $\bar w$; for $a_k = 0$, $\bar w_k = 0$ and $g_k + \lambda = \lambda \ge 0$. So $\bar w$ satisfies the KKT conditions and $\bar w = w^*$. Every limit point equals $w^*$ and the sequence is bounded, so the whole sequence converges to $w^*$. $\square$

The step that turns coordinatewise optimality into global optimality uses that the nonsmooth part, $\lambda \sum_k |w_k|$ plus the constraint $w \in C$, is a sum of functions of one coordinate each. For a nonsmooth term that couples coordinates this step would fail.

**The stopping rule.** The code stops when no coordinate moves by more than a tolerance in a sweep. Theorem 4 says this happens after finitely many sweeps for any positive tolerance; the error in the KKT conditions at that point is what the tests bound.

**Cost.** Lines L5 and L7 cost $O(m)$ with dense columns, or $O(\text{nnz}(a_k))$ with sparse columns, so one sweep over a column costs $O(m n)$ dense or $O(s)$ sparse, where $s$ is the number of nonzero entries of $A$. All $n$ columns cost $O(n s)$ per sweep. $\blacksquare$
