---
title: Cyclic coordinate descent converges to the unique elastic net solution and stops
proves: [correctness, termination]
status: full
---

By the same argument as for ridge and the lasso, the unpenalized intercept reduces to centering, so we work with centered $X \in \mathbb{R}^{n \times d}$ and $y$, and $F(w) = \frac{1}{2n}\|y - Xw\|^2 + \lambda_1\|w\|_1 + \frac{\lambda_2}{2}\|w\|^2$ with $\lambda_1 \ge 0$ and $\lambda_2 > 0$. Let $a_j = \|x_j\|^2/n$ and $c_j = a_j + \lambda_2 > 0$, so line L4 visits every $j$. Arithmetic is exact in this proof.

**Lemma 1 (one update).** Fix all coordinates except $j$ and let $g(t) = F(w + (t - w_j)e_j)$. Then $g(t) = \frac{c_j}{2}t^2 - \rho_j t + \lambda_1|t| + C$, with $\rho_j$ the value of line L5 and $C$ independent of $t$. Its unique minimizer is $t^\star = S(\rho_j, \lambda_1)/c_j$, the value of line L6, and $g(t) - g(t^\star) \ge \frac{c_j}{2}(t - t^\star)^2$.

*Proof.* With $r_{(j)} = y - Xw + x_j w_j$, the loss term is $\frac{1}{2n}\|r_{(j)} - t x_j\|^2 = \frac{a_j}{2}t^2 - \frac1n x_j^\top r_{(j)}\,t + \text{const}$, and $\frac1n x_j^\top r_{(j)} = \frac1n x_j^\top r + a_j w_j = \rho_j$. The L2 term adds $\frac{\lambda_2}{2}t^2$, and the penalties of the other coordinates are constant. So $g$ is $c_j$-strongly convex. Its optimality condition $0 \in c_j t - \rho_j + \lambda_1\partial|t|$ gives $t^\star = (\rho_j - \lambda_1)/c_j$ if $\rho_j > \lambda_1$, $t^\star = (\rho_j + \lambda_1)/c_j$ if $\rho_j < -\lambda_1$, and $t^\star = 0$ if $|\rho_j| \le \lambda_1$, which is $S(\rho_j, \lambda_1)/c_j$. The last inequality holds for each $c_j$-strongly convex function at its minimizer. $\square$

Line L7 keeps the invariant $r = y - Xw$.

**Lemma 2 (decrease).** Each sweep lowers $F$ by at least $\sum_j \frac{c_j}{2}\Delta_j^2$, where $\Delta_j$ is the change of $w_j$ in the sweep. Over all sweeps, $\sum \frac{c_j}{2}\Delta_j^2 \le F(0) - \min F$.

*Proof.* Apply Lemma 1 to each update and add, starting from $w = 0$, with $F \ge 0$. $\square$

**Termination.** By Lemma 2 the changes $\sqrt{c_j}|\Delta_j|$ tend to 0, so for each tol $> 0$ some sweep moves no weight by more than tol, and line L8 stops.

**Lemma 3 (optimality).** $F$ is $\lambda_2$-strongly convex, so it has exactly one minimizer $\hat w$. A point $w$ is $\hat w$ if and only if $w_j = S(\rho_j(w), \lambda_1)/c_j$ for each $j$, where $\rho_j(w) = \frac1n x_j^\top(y - Xw) + a_j w_j$.

*Proof.* $F$ is a strictly convex quadratic plus a convex function, so it is strongly convex, and its sublevel sets are bounded, which gives one minimizer. Since the nonsmooth part $\lambda_1\|w\|_1$ is separable, $0 \in \partial F(w)$ exactly when, for each $j$, $0 \in -\frac1n x_j^\top r + \lambda_2 w_j + \lambda_1\partial|w_j|$. By the proof of Lemma 1 this is the condition that $w_j$ minimizes $g$, that is $w_j = S(\rho_j(w), \lambda_1)/c_j$. For a convex $F$, $0 \in \partial F(w)$ means that $w$ is the minimizer. $\square$

**Theorem.** Without the stopping test, the iterates $w^{(k)}$ at the start of each sweep converge to $\hat w$. With tol $> 0$, the output satisfies the optimality conditions up to an error of order tol, and line L10 returns $\hat b = \bar y - \bar x^\top w$.

*Proof.* $F(w^{(k)}) \le F(0)$ keeps the iterates in a bounded set. Take a convergent subsequence $w^{(k_m)} \to w^\star$. By Lemma 2 the iterates within a sweep also converge to $w^\star$ along this subsequence. The update map $u_j(z) = S(\rho_j(z), \lambda_1)/c_j$ is continuous and $u_j(z) - z_j = \Delta_j \to 0$ at the point where coordinate $j$ is updated, so $u_j(w^\star) = w^\star_j$ for each $j$. By Lemma 3, $w^\star = \hat w$. Every convergent subsequence has the same limit $\hat w$, and the sequence is bounded, so the whole sequence converges to $\hat w$. With tol $> 0$, the last sweep moves each coordinate by $O(\text{tol})$, and the conditions of Lemma 3 are Lipschitz in $w$, so they hold up to $O(\text{tol})$.

Line L9 multiplies the naive solution by $1 + \lambda_2$, which is the rescaled estimate by definition, and line L10 restores the intercept as for ridge. $\blacksquare$
