---
title: FISTA reaches F(x_k) - F* ≤ 2 L ||x_0 - x*||^2 / (k+1)^2
proves: [correctness, convergence-rate]
status: full
---

**Assumptions.** $F = f + h$ on $\mathbb{R}^n$. The function $f$ is convex and differentiable, with an $L_f$-Lipschitz gradient. The function $h$ is proper, closed and convex. $F$ has a minimizer $x^*$, and $F^* = F(x^*)$. The step is $1/L$ with $L \ge L_f$. The method is lines L1 to L6 of the page: $y_1 = x_0$, $t_1 = 1$, and for $k \ge 1$,

$$x_k = T(y_k), \qquad t_{k+1} = \frac{1 + \sqrt{1 + 4t_k^2}}{2}, \qquad y_{k+1} = x_k + \frac{t_k - 1}{t_{k+1}}(x_k - x_{k-1}),$$

where $T(y) = \operatorname{prox}_{h/L}(y - \frac{1}{L}\nabla f(y))$ is one proximal gradient step.

**Lemma 1 (one prox-grad step).** For all $y, z \in \mathbb{R}^n$,

$$F(z) - F(T(y)) \ge \frac{L}{2}\lVert T(y) - y\rVert^2 + L\langle T(y) - y, y - z\rangle.$$

*Proof.* The one-step lemma of the [proximal gradient method](/proximal-gradient-method/) (with $\mu = 0$ and $t = 1/L \le 1/L_f$) says $F(T(y)) \le F(z) + \frac{L}{2}(\lVert y - z\rVert^2 - \lVert T(y) - z\rVert^2)$. Expand $\lVert T(y) - z\rVert^2 = \lVert T(y) - y\rVert^2 + 2\langle T(y) - y, y - z\rangle + \lVert y - z\rVert^2$. Then $\lVert y - z\rVert^2 - \lVert T(y) - z\rVert^2 = -\lVert T(y) - y\rVert^2 - 2\langle T(y) - y, y - z\rangle$, which gives the claim. $\square$

**Lemma 2 (the momentum sequence).** For each $k \ge 1$: $t_k \ge 1$, $t_{k+1}^2 - t_{k+1} = t_k^2$, and $t_k \ge (k+1)/2$.

*Proof.* $t_{k+1}$ is the positive root of $s^2 - s - t_k^2 = 0$, which is the second claim. From $\sqrt{1 + 4t_k^2} \ge 2t_k$ we get $t_{k+1} \ge t_k + \frac{1}{2}$. With $t_1 = 1$, induction gives $t_k \ge 1 + \frac{k-1}{2} = \frac{k+1}{2} \ge 1$. $\square$

**Theorem.** For each $k \ge 1$,

$$F(x_k) - F^* \le \frac{2L\lVert x_0 - x^*\rVert^2}{(k+1)^2}.$$

*Proof.* Write $v_k = F(x_k) - F^*$, and define

$$u_k = t_k x_k - (t_k - 1)x_{k-1} - x^*, \qquad E_k = t_k^2 v_k + \frac{L}{2}\lVert u_k\rVert^2 \qquad (k \ge 1).$$

*Step 1: $E_{k+1} \le E_k$ for $k \ge 1$.* Let $d = x_{k+1} - y_{k+1}$. Lemma 1 with $y = y_{k+1}$, so that $T(y) = x_{k+1}$, gives two inequalities, one with $z = x_k$ and one with $z = x^*$:

$$v_k - v_{k+1} \ge \frac{L}{2}\lVert d\rVert^2 + L\langle d, y_{k+1} - x_k\rangle, \qquad -v_{k+1} \ge \frac{L}{2}\lVert d\rVert^2 + L\langle d, y_{k+1} - x^*\rangle.$$

Multiply the first one by $t_{k+1} - 1 \ge 0$ (Lemma 2) and add the second one:

$$(t_{k+1} - 1)v_k - t_{k+1}v_{k+1} \ge \frac{L}{2}t_{k+1}\lVert d\rVert^2 + L\langle d, t_{k+1}y_{k+1} - (t_{k+1} - 1)x_k - x^*\rangle.$$

Multiply by $t_{k+1} > 0$, and use $t_{k+1}^2 - t_{k+1} = t_k^2$ on the left:

$$t_k^2 v_k - t_{k+1}^2 v_{k+1} \ge \frac{L}{2}\Big(\lVert a\rVert^2 + 2\langle a, b\rangle\Big), \qquad a = t_{k+1}d, \quad b = t_{k+1}y_{k+1} - (t_{k+1} - 1)x_k - x^*.$$

By the update of $y_{k+1}$, $t_{k+1}y_{k+1} = t_{k+1}x_k + (t_k - 1)(x_k - x_{k-1})$, so $b = t_k x_k - (t_k - 1)x_{k-1} - x^* = u_k$. Also $a + b = t_{k+1}x_{k+1} - (t_{k+1} - 1)x_k - x^* = u_{k+1}$. Since $\lVert a\rVert^2 + 2\langle a, b\rangle = \lVert a + b\rVert^2 - \lVert b\rVert^2$,

$$t_k^2 v_k - t_{k+1}^2 v_{k+1} \ge \frac{L}{2}\big(\lVert u_{k+1}\rVert^2 - \lVert u_k\rVert^2\big),$$

which is $E_{k+1} \le E_k$.

*Step 2: $E_1 \le \frac{L}{2}\lVert x_0 - x^*\rVert^2$.* Here $t_1 = 1$, so $u_1 = x_1 - x^*$. The one-step lemma of the proximal gradient method with $y = y_1 = x_0$ and $z = x^*$ gives $v_1 \le \frac{L}{2}(\lVert x_0 - x^*\rVert^2 - \lVert x_1 - x^*\rVert^2)$. So $E_1 = v_1 + \frac{L}{2}\lVert x_1 - x^*\rVert^2 \le \frac{L}{2}\lVert x_0 - x^*\rVert^2$.

*Step 3.* By Steps 1 and 2, $t_k^2 v_k \le E_k \le E_1 \le \frac{L}{2}\lVert x_0 - x^*\rVert^2$. By Lemma 2, $t_k^2 \ge (k+1)^2/4$. So $v_k \le 2L\lVert x_0 - x^*\rVert^2/(k+1)^2$. $\blacksquare$

**What the proof does not give.** The energy $E_k$ decreases, but $v_k$ alone need not decrease: the term $\frac{L}{2}\lVert u_k\rVert^2$ can fall while $v_k$ rises. The page shows a lasso run where $F(x_4) > F(x_3)$. The proof also gives no convergence of the iterates $x_k$ themselves; that needs the modified sequence $t_k = (k + a - 1)/a$ with $a > 2$ (Chambolle and Dossal 2015).
