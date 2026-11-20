---
title: Split Bregman is ADMM, has a nonincreasing Lyapunov function, and converges to a minimizer and a dual solution for every penalty
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $A \in \mathbb{R}^{m \times n}$, $y \in \mathbb{R}^m$, $\Phi \in \mathbb{R}^{q \times n}$, $\lambda > 0$, $\mu > 0$. $N$ is the $\ell_1$ norm on $\mathbb{R}^q$ or a sum of Euclidean norms of disjoint groups of entries. Let $f(x) = \tfrac12\|Ax - y\|^2$, $g(d) = \lambda N(d)$ and $F(x) = f(x) + g(\Phi x)$. We assume $\ker A \cap \ker\Phi = \{0\}$. Then $M = A^\top A + \mu\Phi^\top\Phi$ is positive definite, because $x^\top Mx = \|Ax\|^2 + \mu\|\Phi x\|^2 > 0$ for $x \ne 0$.

The method starts with $d^0 = b^0 = 0$ and, for $k \ge 0$, does

$$x^{k+1} = \operatorname*{argmin}_x f(x) + \tfrac\mu2\|\Phi x - d^k + b^k\|^2,\qquad d^{k+1} = \operatorname*{argmin}_d g(d) + \tfrac\mu2\|d - \Phi x^{k+1} - b^k\|^2,$$

$$b^{k+1} = b^k + \Phi x^{k+1} - d^{k+1}.$$

The first problem is strictly convex with the normal equation $Mx = A^\top y + \mu\Phi^\top(d^k - b^k)$, which is line L3. The second is the proximal map of $(\lambda/\mu)N$ at $\Phi x^{k+1} + b^k$, which is the shrinkage of line L4 (for the $\ell_1$ norm entry by entry, for groups group by group). Both minimizers exist and are unique. Write $v^k = \mu b^k$, $r^{k+1} = \Phi x^{k+1} - d^{k+1}$ and $\Delta^k = d^{k+1} - d^k$, so $v^{k+1} = v^k + \mu r^{k+1}$.

**Remark (ADMM).** For $\min f(x) + g(d)$ subject to $\Phi x - d = 0$, scaled ADMM with penalty $\rho$ and scaled multiplier $u$ is $x^{k+1} = \operatorname{argmin} f(x) + \tfrac\rho2\|\Phi x - d^k + u^k\|^2$, $d^{k+1} = \operatorname{argmin} g(d) + \tfrac\rho2\|\Phi x^{k+1} - d + u^k\|^2$, $u^{k+1} = u^k + \Phi x^{k+1} - d^{k+1}$. With $\rho = \mu$ and $u = b$ these are the three steps above. The proof below is the ADMM argument written out for this case.

**Lemma 1 (optimality of the steps).** For $k \ge 0$,

$$A^\top(Ax^{k+1} - y) + \Phi^\top(v^{k+1} + \mu\Delta^k) = 0, \qquad v^{k+1} \in \partial g(d^{k+1}).$$

*Proof.* The $x$-step gives $A^\top(Ax^{k+1} - y) + \mu\Phi^\top(\Phi x^{k+1} - d^k + b^k) = 0$, and $\Phi x^{k+1} - d^k + b^k = r^{k+1} + b^k + \Delta^k = b^{k+1} + \Delta^k$. The $d$-step gives $0 \in \partial g(d^{k+1}) + \mu(d^{k+1} - \Phi x^{k+1} - b^k)$, and $\mu(\Phi x^{k+1} + b^k - d^{k+1}) = \mu b^{k+1} = v^{k+1}$. $\square$

**Lemma 2 (optimality conditions).** Call $(x^*, d^*, v^*)$ a KKT point if

$$A^\top(Ax^* - y) + \Phi^\top v^* = 0, \qquad v^* \in \partial g(d^*), \qquad d^* = \Phi x^*.$$

(a) If $(x^*, d^*, v^*)$ is a KKT point, then $x^*$ minimizes $F$. (b) A KKT point exists.

*Proof.* (a) For any $x$, convexity of $f$ and the subgradient inequality for $g$ at $d^* = \Phi x^*$ give

$$F(x) \ge f(x^*) + \langle A^\top(Ax^* - y), x - x^*\rangle + g(d^*) + \langle v^*, \Phi x - \Phi x^*\rangle = F(x^*) + \langle A^\top(Ax^* - y) + \Phi^\top v^*, x - x^*\rangle = F(x^*).$$

(b) Existence of a minimizer: the map $x \mapsto (Ax, \Phi x)$ is injective, so there is $c > 0$ with $\|Ax\| + \|\Phi x\| \ge c\|x\|$ for all $x$. Since $N(d) \ge \|d\|$, we have $F(x) \ge \tfrac12\|Ax - y\|^2 + \lambda\|\Phi x\|$. If $\|x\| \to \infty$ then $\|Ax\| \ge c\|x\|/2$ or $\|\Phi x\| \ge c\|x\|/2$, and in both cases this lower bound tends to $\infty$. So $F$ is continuous and coercive and has a minimizer $x^*$. Since $f$ is differentiable and $g$ is convex and finite everywhere, $\partial F(x) = \nabla f(x) + \Phi^\top\partial g(\Phi x)$ (Rockafellar, Convex Analysis, Theorems 23.8 and 23.9). So $0 \in \partial F(x^*)$ gives $v^* \in \partial g(\Phi x^*)$ with $\nabla f(x^*) + \Phi^\top v^* = 0$. Put $d^* = \Phi x^*$. $\square$

**Lemma 3 (Lyapunov function).** Let $(x^*, d^*, v^*)$ be a KKT point and $V_k = \tfrac1\mu\|v^k - v^*\|^2 + \mu\|d^k - d^*\|^2$. Then for $k \ge 0$

$$V_{k+1} \le V_k - \mu\|r^{k+1} + \Delta^k\|^2,$$

and for $k \ge 1$

$$V_{k+1} \le V_k - \mu\|r^{k+1}\|^2 - \mu\|\Delta^k\|^2.$$

*Proof.* The gradient of the convex function $f$ is monotone. With Lemma 1 and the KKT condition, $\nabla f(x^{k+1}) = -\Phi^\top(v^{k+1} + \mu\Delta^k)$ and $\nabla f(x^*) = -\Phi^\top v^*$, so

$$0 \le \langle \nabla f(x^{k+1}) - \nabla f(x^*), x^{k+1} - x^*\rangle = \langle v^* - v^{k+1} - \mu\Delta^k, \Phi x^{k+1} - d^*\rangle.$$

The subdifferential of $g$ is monotone, so $0 \le \langle v^{k+1} - v^*, d^{k+1} - d^*\rangle$. Add the two and use $\Phi x^{k+1} - d^* = r^{k+1} + (d^{k+1} - d^*)$:

$$0 \le \langle v^* - v^{k+1}, r^{k+1}\rangle - \mu\langle \Delta^k, r^{k+1}\rangle - \mu\langle \Delta^k, d^{k+1} - d^*\rangle.$$

Now $r^{k+1} = (v^{k+1} - v^k)/\mu$. The identity $2\langle a - b, b - c\rangle = \|a - c\|^2 - \|a - b\|^2 - \|b - c\|^2$ gives

$$2\langle v^* - v^{k+1}, v^{k+1} - v^k\rangle = \|v^k - v^*\|^2 - \|v^{k+1} - v^*\|^2 - \|v^{k+1} - v^k\|^2,$$

$$2\langle d^{k+1} - d^k, d^{k+1} - d^*\rangle = \|d^{k+1} - d^*\|^2 + \|\Delta^k\|^2 - \|d^k - d^*\|^2.$$

Multiply the inequality by 2 and insert these. With $\|v^{k+1} - v^k\|^2/\mu = \mu\|r^{k+1}\|^2$:

$$0 \le V_k - V_{k+1} - \mu\|r^{k+1}\|^2 - 2\mu\langle\Delta^k, r^{k+1}\rangle - \mu\|\Delta^k\|^2 = V_k - V_{k+1} - \mu\|r^{k+1} + \Delta^k\|^2.$$

For $k \ge 1$, Lemma 1 at steps $k - 1$ and $k$ gives $v^k \in \partial g(d^k)$ and $v^{k+1} \in \partial g(d^{k+1})$, and monotonicity gives $\langle v^{k+1} - v^k, d^{k+1} - d^k\rangle \ge 0$, that is, $\mu\langle r^{k+1}, \Delta^k\rangle \ge 0$. So $\|r^{k+1} + \Delta^k\|^2 \ge \|r^{k+1}\|^2 + \|\Delta^k\|^2$. $\square$

**Theorem 1 (residual rate).** $V_k$ is nonincreasing, $\sum_{k \ge 1}\big(\|r^{k+1}\|^2 + \|\Delta^k\|^2\big) \le V_1/\mu \le V_0/\mu$, and

$$\min_{1 \le k \le K}\big(\|r^{k+1}\|^2 + \|\Delta^k\|^2\big) \le \frac{V_0}{\mu K}, \qquad V_0 = \tfrac1\mu\|v^*\|^2 + \mu\|d^*\|^2.$$

In particular $r^k \to 0$ and $d^{k+1} - d^k \to 0$.

*Proof.* Lemma 3 with a KKT point from Lemma 2(b). Sum the second inequality for $k = 1, \dots, K$; the smallest term is at most the mean. $V_0$ has this form because $d^0 = 0$ and $v^0 = 0$. $\square$

**Theorem 2 (convergence).** For every $\mu > 0$, $x^k \to \bar x$, $d^k \to \Phi\bar x$ and $\mu b^k \to \bar v$, where $\bar x$ minimizes $F$ and $(\bar x, \Phi\bar x, \bar v)$ is a KKT point. In particular $|\bar v_i| \le \lambda$ for all $i$ and $\bar v_i = \lambda\operatorname{sign}((\Phi\bar x)_i)$ where $(\Phi\bar x)_i \ne 0$ (for the $\ell_1$ norm).

*Proof.* By Theorem 1, the sequences $v^k$ and $d^k$ are bounded. The $x$-step is $x^{k+1} = M^{-1}\big(A^\top y + \Phi^\top(\mu d^k - v^k)\big)$, a fixed affine map of $(d^k, v^k)$, so $x^k$ is bounded too. Choose a subsequence $k_j$ with $(x^{k_j}, d^{k_j}, v^{k_j}) \to (\bar x, \bar d, \bar v)$. By Theorem 1, $\Delta^{k_j - 1} \to 0$ and $r^{k_j} = \Phi x^{k_j} - d^{k_j} \to 0$, so $\bar d = \Phi\bar x$. Lemma 1 at step $k_j - 1$ gives, in the limit, $A^\top(A\bar x - y) + \Phi^\top\bar v = 0$. The graph of $\partial g$ is closed, because $g$ is convex and continuous, so $v^{k_j} \in \partial g(d^{k_j})$ gives $\bar v \in \partial g(\bar d)$. So $(\bar x, \bar d, \bar v)$ is a KKT point, and $\bar x$ minimizes $F$ by Lemma 2(a).

Now apply Lemma 3 with this KKT point. The sequence $\bar V_k = \tfrac1\mu\|v^k - \bar v\|^2 + \mu\|d^k - \bar d\|^2$ is nonincreasing and $\bar V_{k_j} \to 0$, so $\bar V_k \to 0$: $v^k \to \bar v$ and $d^k \to \bar d$. Then $x^{k+1} \to M^{-1}\big(A^\top y + \Phi^\top(\mu\bar d - \bar v)\big)$. This vector is $\bar x$: from the KKT conditions $M\bar x = A^\top A\bar x + \mu\Phi^\top\bar d = A^\top y - \Phi^\top\bar v + \mu\Phi^\top\bar d$, and $M$ is invertible. The last claim is $\bar v \in \partial g(\Phi\bar x)$ written out for $g = \lambda\|\cdot\|_1$. $\blacksquare$

**Remarks.** The minimizer of $F$ need not be unique, for example when $A$ has a null space; the method then converges to one of them. The proof uses exact solves in lines L3 and L4. The ergodic $O(1/K)$ bound for the objective and the constraint residual follows from the general ADMM argument on the [ADMM](/admm/) page with $B = -I$ and $c = 0$.
