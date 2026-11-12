---
title: Cyclic coordinate descent with soft thresholding converges to a lasso solution and stops
proves: [correctness, termination]
status: full
---

By the argument of the problem section, the intercept reduces to centering, so we work with centered $X \in \mathbb{R}^{n \times d}$ and $y \in \mathbb{R}^n$ and $F(w) = \frac{1}{2n}\|y - Xw\|^2 + \lambda\|w\|_1$ with $\lambda > 0$. Let $A = \{j : a_j > 0\}$ with $a_j = \|x_j\|^2/n$. A column with $a_j = 0$ is zero, so $w_j$ does not change the loss and the penalty makes $w_j = 0$ best. Lines L4 to L7 leave it at 0, so we assume $A = \{1, \dots, d\}$. Arithmetic is exact in this proof.

**Lemma 1 (one update).** Fix all coordinates except $j$ and let $g(t) = F(w + (t - w_j)e_j)$. Then $g(t) = \frac{a_j}{2}t^2 - \rho_j t + \lambda|t| + C$, where $\rho_j$ is the value of line L5 and $C$ does not depend on $t$. Its unique minimizer is $t^\star = S(\rho_j, \lambda)/a_j$, and $g(t) - g(t^\star) \ge \frac{a_j}{2}(t - t^\star)^2$ for all $t$.

*Proof.* Let $r_{(j)} = y - Xw + x_j w_j$. Then $y - X(w + (t - w_j)e_j) = r_{(j)} - t x_j$, and $\frac{1}{2n}\|r_{(j)} - tx_j\|^2 = \frac{a_j}{2}t^2 - \frac{1}{n}x_j^\top r_{(j)}\,t + \frac{1}{2n}\|r_{(j)}\|^2$. With $r = y - Xw$, $\frac1n x_j^\top r_{(j)} = \frac1n x_j^\top r + a_j w_j = \rho_j$, which is line L5. The penalty of the other coordinates is constant. The function $g(t) - \frac{a_j}{2}t^2$ is convex, so $g$ is $a_j$-strongly convex and has one minimizer $t^\star$, with $0 \in a_j t^\star - \rho_j + \lambda\,\partial|t^\star|$. If $t^\star > 0$ this is $t^\star = (\rho_j - \lambda)/a_j$, which needs $\rho_j > \lambda$. If $t^\star < 0$ it is $t^\star = (\rho_j + \lambda)/a_j$ with $\rho_j < -\lambda$. If $t^\star = 0$ it is $|\rho_j| \le \lambda$. In each case $t^\star = S(\rho_j, \lambda)/a_j$. For an $a_j$-strongly convex $g$ with minimizer $t^\star$, $g(t) \ge g(t^\star) + \frac{a_j}{2}(t - t^\star)^2$. $\square$

Line L7 keeps the invariant $r = y - Xw$, because it changes $w_j$ by $\Delta$ and $r$ by $-x_j\Delta$.

**Lemma 2 (sufficient decrease).** Let $w^{(k)}$ be the weights at the start of sweep $k$ and let $\Delta_j^{(k)}$ be the change of $w_j$ in that sweep. Then $F(w^{(k)}) - F(w^{(k+1)}) \ge \sum_j \frac{a_j}{2}(\Delta_j^{(k)})^2$, and $\sum_k \sum_j \frac{a_j}{2}(\Delta_j^{(k)})^2 \le F(0) - \min F < \infty$.

*Proof.* By Lemma 1, the update of coordinate $j$ moves from $t = w_j$ to $t^\star$ and lowers $F$ by at least $\frac{a_j}{2}\Delta_j^2$. Add over the $d$ updates of a sweep, then over the sweeps, starting at $w^{(0)} = 0$. $F \ge 0$, so the sum is finite. $\square$

**Termination.** By Lemma 2, $\max_j \sqrt{a_j}\,|\Delta_j^{(k)}| \to 0$, so for each $\text{tol} > 0$ some sweep has all changes at most $\text{tol}$ in this scale, and line L8 stops. (The implementation also stops after a fixed maximum number of sweeps.)

**Lemma 3 (KKT is optimality).** $w$ minimizes $F$ if and only if, with $r = y - Xw$, $\frac1n x_j^\top r = \lambda\operatorname{sign}(w_j)$ for $w_j \ne 0$ and $|\frac1n x_j^\top r| \le \lambda$ for $w_j = 0$. These hold if and only if $w_j = S(\rho_j(w), \lambda)/a_j$ for each $j$, where $\rho_j(w) = \frac1n x_j^\top r + a_j w_j$.

*Proof.* $F$ is the sum of a differentiable convex function with gradient $-\frac1n X^\top r$ and the separable convex function $\lambda\|w\|_1$, whose subdifferential is the product of the sets $\lambda\,\partial|w_j|$. So $0 \in \partial F(w)$ exactly when $\frac1n x_j^\top r \in \lambda\,\partial|w_j|$ for each $j$, which is the stated condition. For a convex $F$, $0 \in \partial F(w)$ means that $w$ is a global minimizer. The condition for coordinate $j$ is also the optimality condition of Lemma 1 for $g$ at $t = w_j$, since $\rho_j - a_j w_j = \frac1n x_j^\top r$; so it holds exactly when $w_j$ is the minimizer $S(\rho_j, \lambda)/a_j$. $\square$

**Theorem.** Without the stopping test (tol $= 0$), every limit point of $w^{(k)}$ minimizes $F$, a limit point exists, and $F(w^{(k)}) \to \min F$. With tol $> 0$, the output satisfies the KKT conditions of Lemma 3 up to an error that goes to 0 with tol.

*Proof.* The sublevel set $\{w : F(w) \le F(0)\}$ lies in $\{\|w\|_1 \le F(0)/\lambda\}$, which is bounded, and $F(w^{(k)}) \le F(0)$. So a subsequence $w^{(k_m)}$ converges to some $w^\star$. Let $z^{(k, j)}$ be the iterate just before the update of coordinate $j$ in sweep $k$. By Lemma 2, $\|z^{(k, j)} - w^{(k)}\| \to 0$, so $z^{(k_m, j)} \to w^\star$ for each $j$. The update map $u_j(z) = S(\rho_j(z), \lambda)/a_j$ is continuous, since $\rho_j$ is affine and $S$ is continuous. The update sets coordinate $j$ to $u_j(z^{(k, j)})$, and $u_j(z^{(k, j)}) - z^{(k, j)}_j = \Delta_j^{(k)} \to 0$. Taking the limit along $k_m$ gives $u_j(w^\star) = w^\star_j$ for each $j$. By Lemma 3, $w^\star$ minimizes $F$. Since $F(w^{(k)})$ decreases and $F$ is continuous, $F(w^{(k)}) \to F(w^\star) = \min F$.

For tol $> 0$, at the last sweep every $|\Delta_j| \le \text{tol}/\sqrt{a_j}$ (in the units of the test). After the sweep, coordinate $j$ is optimal for the iterate $z^{(j)}$ at its update, and the later updates of the sweep move $w$ by at most $d\,\text{tol}/\min_k\sqrt{a_k}$. Since $\frac1n x_j^\top r$ is a Lipschitz function of $w$, the KKT conditions of Lemma 3 hold at the output up to an error of order $\text{tol}$. $\blacksquare$

**Remark.** The fit $Xw$ of a minimizer is unique, because $F$ is strictly convex as a function of $Xw$ (the squared norm) plus a convex function of $w$. So $Xw^{(k)} \to X\hat w$ for the whole sequence, even when the minimizer itself is not unique.
