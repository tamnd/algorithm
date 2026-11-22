---
title: The C&W attack returns a valid adversarial input, never closer than the true minimum
proves: [correctness]
status: full
---

We write $f(v) = \arg\max_k z_k(v)$ for the label, $y = f(x)$ for the label of the input $x \in [0,1]^d$, and $d^\star(x) = \inf\{\lVert v - x \rVert_2 : v \in [0,1]^d,\ f(v) \ne y\}$ for the true minimum adversarial distance. The attack works on a variable $w \in \mathbb{R}^d$ and the point $x' = \tfrac12(\tanh w + 1)$, taken coordinate by coordinate (line L5).

**Lemma 1 (the box constraint disappears).** For every $w \in \mathbb{R}^d$, $x' \in (0,1)^d$. Every point of $(0,1)^d$ is $x'$ for exactly one $w$.

*Proof.* The function $\tanh$ is a strictly increasing bijection from $\mathbb{R}$ onto $(-1, 1)$, so $t \mapsto \tfrac12(\tanh t + 1)$ is a strictly increasing bijection from $\mathbb{R}$ onto $(0,1)$. Apply it to each coordinate. $\square$

In floating point, $\tanh$ can round to $\pm 1$, so a coordinate can be exactly $0$ or $1$. It is still in $[0,1]$. The function `from_box` keeps $2x_i - 1$ inside $[-1 + 10^{-9}, 1 - 10^{-9}]$, so the start of line L3 is finite even when $x_i$ is $0$ or $1$.

**Lemma 2 (the gradient of line L7).** Let $F(w) = \lVert x' - x \rVert_2^2 + c\, \ell(x')$ with $\ell(v) = \max(z_y(v) - \max_{i \ne y} z_i(v), -\kappa)$. At a point where the best other class $j$ is unique and $\ell(x') > -\kappa$, $\partial F / \partial w_i = \big(2(x'_i - x_i) + c\,(\partial_i z_y - \partial_i z_j)(x')\big) \cdot \tfrac12 (1 - \tanh^2 w_i)$. Where $\ell(x') < -\kappa$, the same formula holds without the term in $c$.

*Proof.* Near such a point, $\ell(v) = z_y(v) - z_j(v)$ in the first case and $\ell(v) = -\kappa$ in the second, so $\nabla_v \ell$ is $\nabla z_y - \nabla z_j$ or $0$. The gradient of $\lVert v - x \rVert_2^2$ is $2(v - x)$. Since $x'_i$ depends only on $w_i$, with $dx'_i / dw_i = \tfrac12 (1 - \tanh^2 w_i)$, the chain rule gives the formula. This is what `objective_gradient` computes. $\square$

**Theorem 1 (a valid output).** If the attack returns a point $x^\star$ (not `None`), then $x^\star \in [0,1]^d$, $f(x^\star) \ne y$, $\max_{i \ne y} z_i(x^\star) - z_y(x^\star) \ge \kappa$, and $\lVert x^\star - x \rVert_2 \ge d^\star(x)$.

*Proof.* The variable `best` is set only in line L6, and only to a point $x'$ of line L5 whose label differs from $y$ and whose best other logit is at least $\kappa$ above $z_y(x')$. By Lemma 1 and the remark after it, $x' \in [0,1]^d$. So $x^\star$ is in the set over which $d^\star(x)$ is the infimum, and its distance is at least the infimum. $\square$

So the attack gives an upper bound $\lVert x^\star - x \rVert_2$ on the distance from $x$ to the nearest adversarial input, and never a value below the truth. If it returns `None`, it proves nothing: the point $x$ may still have adversarial inputs close by.

**Theorem 2 (the best point is the closest one seen).** The returned point is, among all points $x'$ of line L5 in all rounds that have a label other than $y$, one with the smallest distance to $x$.

*Proof.* Line L6 replaces `best` only by a point with a strictly smaller distance, and every adversarial $x'$ of every round passes through line L6. $\square$

**Lemma 3 (the search on $c$).** Let $c_0 > 0$. Before the first round that succeeds, line L9 multiplies $c$ by $10$ and $hi = \infty$. After it, $0 \le lo < c < hi < \infty$ holds after each line L9, and $hi - lo$ is halved by each round.

*Proof.* While every round fails, line L8 sets $lo = c$ and line L9 sets $c$ to $10c$, so $lo < c$. At the first success, $hi = c > lo$, and line L9 sets $c = (lo + hi)/2$, strictly between $lo$ and $hi$. In each later round, line L8 replaces either $hi$ or $lo$ by the current $c$, which lies strictly between them, and so it halves the gap and keeps $lo < hi$. Line L9 then puts $c$ at the midpoint again. $\blacksquare$

**What is not claimed.** The function $F$ is not convex for a nonlinear model, and success of a round need not be monotone in $c$. So Lemma 3 is a statement about the search, not a proof that it finds the best $c$, and Adam is not proved to reach a global minimum of $F$. Theorems 1 and 2 hold for every model, and they are the properties an attack must have.
