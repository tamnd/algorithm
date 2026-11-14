---
title: The MM computation finds the M-scale, keeps the least scale, and never increases the M-objective
proves: [correctness]
status: full
---

This proof covers the computation only. The breakdown point and the efficiency of the MM-estimator are theorems of Yohai (1987) and are not proved here.

**Notation.** $\rho_c(u) = 1 - (1 - u^2/c^2)^3$ for $|u| \le c$ and $1$ beyond, with $0 < c_0 < c_1$ and $b = 1/2$. For residuals $r_1, \ldots, r_n$ put $h(s) = \frac1n\sum_i \rho_{c_0}(r_i/s)$ for $s > 0$, and let $z$ be the number of nonzero $r_i$.

**Lemma 1 (the M-scale).** If $z > nb$, the equation $h(s) = b$ has exactly one solution $s^* > 0$, and the bisection of lines L13 and L14 keeps $s^*$ in $[lo, hi]$.

*Proof.* $\rho_{c_0}$ is continuous, even, and nondecreasing in $|u|$, and strictly increasing in $|u|$ on $[0, c_0]$. So $h$ is continuous and nonincreasing in $s$. At $s = lo = \min_{r_i \ne 0}|r_i|/c_0$, every nonzero term is $\rho_{c_0}(u)$ with $|u| \ge c_0$, which is 1, so $h(lo) = z/n > b$. Since $1 - (1 - v)^3 \le 3v$ for $0 \le v \le 1$, $\rho_{c_0}(u) \le 3u^2/c_0^2$ for all $u$, so $h(s) \le 3\,\overline{r^2}/(c_0^2 s^2)$, and $h(hi) \le b$ for the $hi$ of line L13. By continuity a root lies in $(lo, hi]$. Let $s^*$ be a root. Since $b < z/n$, some nonzero term has $\rho_{c_0}(r_i/s^*) < 1$, that is $|r_i|/s^* < c_0$. This term is strictly decreasing in $s$ near $s^*$ and the others are nonincreasing, so $h$ is strictly decreasing on a neighbourhood of $s^*$. A nonincreasing function that is strictly decreasing near each of its roots has at most one root: two roots $s_1 < s_2$ would make $h$ constant on $[s_1, s_2]$. So the root is unique. Each bisection step keeps $h(lo) > b \ge h(hi)$, so $s^* \in (lo, hi]$. $\square$

If $z \le nb$, line L12 returns 0. This is the limit of the scale equation, because the residuals that are 0 already make up at least half of the sample.

**Lemma 2 (the S-stage).** Lines L1 to L4 return a pair $(\beta_0, s_0)$ such that $s_0$ is the least M-scale over the nonsingular subsets drawn, and $\beta_0$ is the fit of one subset that attains it.

*Proof.* Line L4 keeps a running minimum of the values of line L3. $\square$

**Lemma 3 (majorization).** Put $g(v) = 1 - (1 - v/c_1^2)^3$ for $0 \le v \le c_1^2$ and $g(v) = 1$ beyond. Then $\rho_{c_1}(u) = g(u^2)$, $g$ is concave, nondecreasing and differentiable, and $g'(u^2) = \frac{3}{c_1^2}w(u)$ with $w(u) = (1 - u^2/c_1^2)^2$ for $|u| < c_1$ and 0 beyond.

*Proof.* $g'(v) = \frac{3}{c_1^2}(1 - v/c_1^2)^2$ for $v < c_1^2$ and 0 for $v > c_1^2$, and both one-sided derivatives at $c_1^2$ are 0. This derivative is nonnegative and nonincreasing. $\square$

**Lemma 4 (descent).** Fix $\hat s > 0$ and put $F(\beta) = \sum_i \rho_{c_1}(r_i(\beta)/\hat s)$. Let $w_i$ be the weights of line L8 at $\beta$, and suppose the matrix $A = \sum_i w_i x_i x_i^{\mathsf T}$ is nonsingular. Then the fit $\beta'$ of line L9 satisfies $F(\beta') \le F(\beta)$, with equality only if $\beta' = \beta$.

*Proof.* Put $v_i(\gamma) = r_i(\gamma)^2/\hat s^2$. By Lemma 3 and the tangent inequality for concave functions,
$$F(\gamma) \le \sum_i \Bigl[g(v_i(\beta)) + \tfrac{3}{c_1^2}w_i\bigl(v_i(\gamma) - v_i(\beta)\bigr)\Bigr] =: M(\gamma),$$
with equality at $\gamma = \beta$. $M$ is a quadratic in $\gamma$ whose quadratic part is $\frac{3}{c_1^2\hat s^2}\gamma^{\mathsf T}A\gamma$, which is positive definite because $A$ is nonsingular and $w_i \ge 0$. So $M$ has a unique minimizer, the weighted least squares fit $\beta' = A^{-1}\sum_i w_i x_i y_i$. Then $F(\beta') \le M(\beta') \le M(\beta) = F(\beta)$, and the second inequality is strict when $\beta' \ne \beta$. $\square$

**Lemma 5 (the weighted design stays nonsingular).** Assume $\hat s > 0$, every $p$ rows of $X$ are linearly independent, and $n \ge 2p$. Then at every step of lines L6 to L11, at least $n/2$ points have a positive weight, and $A$ is nonsingular.

*Proof.* For fixed $u$, $\rho_c(u)$ is nonincreasing in $c$, because $u^2/c^2$ decreases. Since $c_1 > c_0$, at the start
$$F(\beta_0) = \sum_i \rho_{c_1}(r_i(\beta_0)/\hat s) \le \sum_i \rho_{c_0}(r_i(\beta_0)/\hat s) = nb = n/2,$$
where the last equality is the scale equation (Lemma 1). A point with weight 0 has $|r_i| \ge c_1\hat s$ and adds exactly 1 to $F$. So the number of points with weight 0 is at most $F$. Assume that $A$ was nonsingular at all earlier steps. By Lemma 4, $F$ at the current $\beta$ is at most $F(\beta_0) \le n/2$, so at most $n/2$ points have weight 0, and at least $n/2 \ge p$ points have a positive weight. Any $p$ of them have independent rows $x_i$, so for $\gamma \ne 0$ some of them has $x_i^{\mathsf T}\gamma \ne 0$, and $\gamma^{\mathsf T}A\gamma \ge w_i(x_i^{\mathsf T}\gamma)^2 > 0$. So $A$ is nonsingular. Induction on the steps completes the proof. $\square$

**Theorem.** Under the assumptions of Lemma 5, the M-stage is well defined, $F(\beta_t)$ is nonincreasing, and every limit point $\beta^*$ of the iterates satisfies $\sum_i \psi_{c_1}(r_i(\beta^*)/\hat s)\,x_i = 0$, where $\psi_{c_1}(u) = u\,w(u)$.

*Proof.* Lemmas 4 and 5 give the first two claims. Let $K = \{\beta : F(\beta) \le n/2\}$. $K$ is closed, because $F$ is continuous. For $\beta \in K$, as in Lemma 5, there is a set $J$ of $p$ rows with $|r_i(\beta)| < c_1\hat s$ for $i \in J$. Then $\beta = X_J^{-1}(y_J - r_J(\beta))$ with $\|r_J(\beta)\|_\infty < c_1\hat s$, so $\beta$ lies in a bounded set that depends only on $J$. There are finitely many sets $J$, so $K$ is bounded, and the iterates, which lie in $K$, have limit points in $K$. The weights are continuous functions of $\beta$, and $A$ is nonsingular at every point of $K$ by the count of Lemma 5, so the map $\beta \mapsto \beta'$ is continuous on $K$. As in the proof on the [Tukey biweight](/tukey-biweight/) page, $F(\beta_t)$ converges to some $F^*$, and a limit point $\beta^*$ with its image $\beta^{*\prime}$ both have $F = F^*$, so Lemma 4 gives $\beta^{*\prime} = \beta^*$. A fixed point of the weighted least squares map satisfies $\sum_i w_i x_i (y_i - x_i^{\mathsf T}\beta^*) = 0$, which is the stated equation. $\square$
