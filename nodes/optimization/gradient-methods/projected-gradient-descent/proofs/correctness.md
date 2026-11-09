---
title: Projected gradient descent converges at the rate O(1/k), linearly under strong convexity, and at O(1/√K) for subgradients
proves: [correctness, convergence-rate]
status: full
---

**Setting.** $C \subseteq \mathbb{R}^n$ is nonempty, closed and convex, and $P_C$ is the Euclidean projection onto $C$. The method is $x_0 \in C$ and $x_{k+1} = P_C(x_k - t_k g_k)$, where $g_k = \nabla f(x_k)$ in Parts 1 and 2 and $g_k \in \partial f(x_k)$ in Part 3. A minimizer $x^*$ of $f$ over $C$ exists, $f^* = f(x^*)$, and $R = \lVert x_0 - x^*\rVert$.

**Lemma 1 (projection).** For each $v \in \mathbb{R}^n$, the point $p = P_C(v)$ exists, is unique, and satisfies $\langle v - p, z - p\rangle \le 0$ for all $z \in C$. Also $\lVert P_C(v) - P_C(w)\rVert \le \lVert v - w\rVert$.

*Proof.* The function $z \mapsto \frac{1}{2}\lVert z - v\rVert^2$ is continuous and $1$-strongly convex, and $C$ is closed and convex, so it has exactly one minimizer $p$ over $C$. For $z \in C$ and $s \in (0, 1]$, the point $p + s(z - p)$ lies in $C$, so $\lVert p + s(z - p) - v\rVert^2 \ge \lVert p - v\rVert^2$. Expand, divide by $s$ and let $s \to 0$: $2\langle p - v, z - p\rangle \ge 0$, which is the first claim. For the second, let $p = P_C(v)$ and $q = P_C(w)$. The first claim with $z = q$ and with $z = p$ gives $\langle v - p, q - p\rangle \le 0$ and $\langle w - q, p - q\rangle \le 0$. Add them: $\lVert p - q\rVert^2 \le \langle v - w, p - q\rangle \le \lVert v - w\rVert\,\lVert p - q\rVert$. $\square$

Projected gradient descent is the [proximal gradient method](/proximal-gradient-method/) with $h = \iota_C$, the indicator of $C$, since $\operatorname{prox}_{t\iota_C} = P_C$. Parts 1 and 2 give the proofs directly, without that page.

**Lemma 2 (one step).** Let $f$ be convex and differentiable on an open set that contains $C$, with $\mu$-strongly convex $f$ for some $\mu \ge 0$ and an $L_f$-Lipschitz gradient. Let $0 < t \le 1/L_f$, $x \in C$ and $x^+ = P_C(x - t\nabla f(x))$. Then for all $z \in C$,

$$f(x^+) \le f(z) + \frac{1}{2t}\Big((1 - \mu t)\lVert x - z\rVert^2 - \lVert x^+ - z\rVert^2\Big).$$

*Proof.* By the descent lemma for an $L_f$-smooth function and $t \le 1/L_f$,

$$f(x^+) \le f(x) + \langle \nabla f(x), x^+ - x\rangle + \frac{1}{2t}\lVert x^+ - x\rVert^2.$$

By strong convexity, $f(x) \le f(z) - \langle \nabla f(x), z - x\rangle - \frac{\mu}{2}\lVert z - x\rVert^2$. Add the two lines:

$$f(x^+) \le f(z) + \langle \nabla f(x), x^+ - z\rangle + \frac{1}{2t}\lVert x^+ - x\rVert^2 - \frac{\mu}{2}\lVert x - z\rVert^2.$$

Lemma 1 with $v = x - t\nabla f(x)$ and $p = x^+$ gives $\langle x - t\nabla f(x) - x^+, z - x^+\rangle \le 0$, so $\langle \nabla f(x), x^+ - z\rangle \le \frac{1}{t}\langle x - x^+, x^+ - z\rangle$. The identity $2\langle x - x^+, x^+ - z\rangle = \lVert x - z\rVert^2 - \lVert x - x^+\rVert^2 - \lVert x^+ - z\rVert^2$ then gives

$$f(x^+) \le f(z) + \frac{1}{2t}\big(\lVert x - z\rVert^2 - \lVert x^+ - z\rVert^2\big) - \frac{\mu}{2}\lVert x - z\rVert^2,$$

which is the claim. $\square$

**Theorem 1 (smooth convex, constant step).** Under Lemma 2 with $\mu = 0$ and the constant step $t \le 1/L_f$: $f(x_{k+1}) \le f(x_k)$, $\lVert x_{k+1} - x^*\rVert \le \lVert x_k - x^*\rVert$, and for each $k \ge 1$

$$f(x_k) - f^* \le \frac{R^2}{2tk}.$$

*Proof.* Lemma 2 with $z = x_k$ gives $f(x_{k+1}) \le f(x_k) - \frac{1}{2t}\lVert x_{k+1} - x_k\rVert^2 \le f(x_k)$. Lemma 2 with $z = x^*$ gives $0 \le f(x_{j+1}) - f^* \le \frac{1}{2t}(\lVert x_j - x^*\rVert^2 - \lVert x_{j+1} - x^*\rVert^2)$, so the distance to $x^*$ does not increase. Sum this over $j = 0, \dots, k-1$; the right side telescopes to at most $R^2/(2t)$. Since $f(x_j)$ does not increase, the left side is at least $k(f(x_k) - f^*)$. $\blacksquare$

With $t = 1/L_f$ the bound is $L_f R^2/(2k)$.

**Theorem 2 (strongly convex).** Under Lemma 2 with $\mu > 0$ and the constant step $t \le 1/L_f$, the minimizer $x^*$ is unique and $\lVert x_k - x^*\rVert^2 \le (1 - \mu t)^k R^2$ for each $k \ge 0$.

*Proof.* Lemma 2 with $z = x^*$, and $f(x_{k+1}) \ge f^*$, give $0 \le (1 - \mu t)\lVert x_k - x^*\rVert^2 - \lVert x_{k+1} - x^*\rVert^2$. Apply this $k$ times. A strongly convex function has at most one minimizer over a convex set. $\blacksquare$

With $t = 1/L_f$ the factor is $1 - 1/\kappa$, where $\kappa = L_f/\mu$.

**Theorem 3 (projected subgradient method).** Let $f$ be convex on an open set that contains $C$, let $g_k \in \partial f(x_k)$ with $\lVert g_k\rVert \le G$, and let $t_k > 0$. Then for each $K \ge 1$,

$$\min_{0 \le k < K} f(x_k) - f^* \le \frac{R^2 + G^2\sum_{k<K} t_k^2}{2\sum_{k<K} t_k}.$$

With the constant step $t_k = R/(G\sqrt{K})$ the right side is $RG/\sqrt{K}$.

*Proof.* Since $x^* \in C$, $x^* = P_C(x^*)$, and Lemma 1 (nonexpansive) gives

$$\lVert x_{k+1} - x^*\rVert^2 \le \lVert x_k - t_k g_k - x^*\rVert^2 = \lVert x_k - x^*\rVert^2 - 2t_k\langle g_k, x_k - x^*\rangle + t_k^2\lVert g_k\rVert^2.$$

By the subgradient inequality, $\langle g_k, x_k - x^*\rangle \ge f(x_k) - f^*$. So $2t_k(f(x_k) - f^*) \le \lVert x_k - x^*\rVert^2 - \lVert x_{k+1} - x^*\rVert^2 + t_k^2G^2$. Sum over $k < K$, drop $\lVert x_K - x^*\rVert^2 \ge 0$, and bound each $f(x_k) - f^*$ below by the minimum. For the constant step, the numerator is $2R^2$ and the denominator is $2R\sqrt{K}/G$. $\blacksquare$

**Remarks.** The test file checks Theorem 1 at every iterate on random box-constrained quadratics with a known minimizer, Theorem 2 on separable quadratics over a ball, and Theorem 3 on $\lVert x - p\rVert_1$ over a box. When $x_0 \notin C$, line L1 projects it first; since $P_C$ is nonexpansive and $x^* \in C$, this does not increase $R$.
