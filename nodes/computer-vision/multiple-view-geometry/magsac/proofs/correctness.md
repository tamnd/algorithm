---
title: The MAGSAC++ loss is the integral of the marginal weight, each sigma-consensus++ step does not increase it, and the loop returns the best model it has seen
proves: [correctness]
status: full
---

We use the notation of the page. The residual of an item is $r \ge 0$, with $\nu = 2$ degrees of freedom, a noise bound $\sigma_{\max} > 0$ and a cut $k > 0$. Write $a = \sqrt{2}\,\sigma_{\max}$ and $c = \operatorname{erfc}(k/\sqrt{2})$. For $0 \le r < k\sigma_{\max}$,

$$w(r) = \frac{1}{\sigma_{\max}} \sqrt{\frac{\pi}{2}} \big(\operatorname{erfc}(r/a) - c\big),$$

and $w(r) = 0$ for $r \ge k\sigma_{\max}$. The loss is $\rho(r) = \int_0^{r} x\, w(x)\, dx$, and the quality of a model is $Q(\theta) = \sum_i \rho(r_i(\theta))$, lower is better. The model of computation is the real RAM, with $\operatorname{erf}$, $\operatorname{erfc}$ and $\exp$ as unit-cost operations.

**Claim.** (a) For $0 < r < k\sigma_{\max}$, $w(r) = \frac{1}{\sigma_{\max}} \int_{r/k}^{\sigma_{\max}} \frac{r}{\sigma^2} e^{-r^2/(2\sigma^2)}\, d\sigma$, the density of the residual of an inlier at $r$, averaged over $\sigma$ uniform on $[0, \sigma_{\max}]$, with the density of each $\sigma$ cut at $k\sigma$. (b) $w$ is non-negative, continuous and non-increasing on $[0, \infty)$, and $\rho$ is non-decreasing, bounded and constant for $r \ge k\sigma_{\max}$. (c) The closed form of $\rho$ in the code is equal to $\int_0^r x\, w(x)\, dx$. (d) If $\theta_1$ minimizes $\sum_i w(r_i(\theta_0))\, r_i(\theta)^2$, then $Q(\theta_1) \le Q(\theta_0)$. (e) The loop of lines L1 to L12 ends after at most $k_{\max}$ rounds, and it returns a model whose quality is the least over all models it has evaluated, and that quality.

**Lemma 1 (weight).** Part (a) holds.

*Proof.* Substitute $u = r/(\sqrt{2}\,\sigma)$, so $\sigma = r/(\sqrt{2}\,u)$ and $d\sigma = -r/(\sqrt{2}\,u^2)\, du$. Then $\frac{r}{\sigma^2} e^{-r^2/(2\sigma^2)}\, d\sigma = -\frac{2u^2}{r} e^{-u^2} \frac{r}{\sqrt{2}\,u^2}\, du = -\sqrt{2}\, e^{-u^2}\, du$. The limit $\sigma = r/k$ goes to $u = k/\sqrt{2}$, and $\sigma = \sigma_{\max}$ goes to $u = r/a$. So the integral is $\sqrt{2} \int_{r/a}^{k/\sqrt{2}} e^{-u^2}\, du = \sqrt{2}\, \frac{\sqrt{\pi}}{2} \big(\operatorname{erfc}(r/a) - c\big)$. Divide by $\sigma_{\max}$ to get $w(r)$. The integrand is the chi density with 2 degrees of freedom of $r$ at scale $\sigma$, and $r < k\sigma$ is the same as $\sigma > r/k$. $\square$

**Lemma 2 (shape).** Part (b) holds.

*Proof.* The function $\operatorname{erfc}$ is continuous and strictly decreasing. For $r < k\sigma_{\max}$, $r/a < k/\sqrt{2}$, so $\operatorname{erfc}(r/a) > c$ and $w(r) > 0$. At $r = k\sigma_{\max}$ the bracket is 0, so $w$ is continuous there, and it is 0 after. So $w$ is non-negative, continuous and non-increasing. Then $x\, w(x) \ge 0$, so $\rho$ is non-decreasing, and $x\, w(x) = 0$ for $x \ge k\sigma_{\max}$, so $\rho$ is constant there. The constant is finite, because it is the integral of a continuous function on a bounded interval. $\square$

**Lemma 3 (closed form).** Part (c) holds.

*Proof.* Let $e(r) = e^{-r^2/a^2}$ and let $R(r) = \frac{1}{2} r^2 \operatorname{erfc}(r/a) + \frac{1}{4} a^2 \operatorname{erf}(r/a) - \frac{a r\, e(r)}{2\sqrt{\pi}} - \frac{1}{2} r^2 c$, so the code computes $\rho(r) = \frac{1}{\sigma_{\max}}\sqrt{\frac{\pi}{2}}\, R(\min(r, k\sigma_{\max}))$. Use $\frac{d}{dr}\operatorname{erfc}(r/a) = -\frac{2}{a\sqrt{\pi}} e(r)$ and $e'(r) = -\frac{2r}{a^2} e(r)$. The four terms of $R$ have the derivatives $r \operatorname{erfc}(r/a) - \frac{r^2 e}{a\sqrt{\pi}}$, $\frac{a e}{2\sqrt{\pi}}$, $-\frac{a e}{2\sqrt{\pi}} + \frac{r^2 e}{a\sqrt{\pi}}$ and $-r c$. Their sum is $r\big(\operatorname{erfc}(r/a) - c\big)$. So $\frac{d}{dr}\rho(r) = r\, w(r)$ for $r < k\sigma_{\max}$. Also $R(0) = 0$. By the fundamental theorem of calculus, the code gives $\int_0^r x\, w(x)\, dx$ for $r \le k\sigma_{\max}$. For larger $r$ the code uses $R(k\sigma_{\max})$, which is correct by Lemma 2. $\square$

**Lemma 4 (one reweighting step does not increase the loss).** Part (d) holds.

*Proof.* Let $\varphi(v) = \rho(\sqrt{v})$ for $v \ge 0$. For $v > 0$, $\varphi'(v) = \rho'(\sqrt{v}) / (2\sqrt{v}) = w(\sqrt{v})/2$ by Lemma 3. By Lemma 2 this derivative is non-increasing in $v$, and $\varphi$ is continuous at 0, so $\varphi$ is concave on $[0, \infty)$, with right derivative $w(0)/2$ at 0. A concave function lies below its tangent: $\varphi(v) \le \varphi(v_0) + \frac{1}{2} w(\sqrt{v_0})(v - v_0)$ for all $v, v_0 \ge 0$. Put $v = r_i(\theta)^2$, $v_0 = r_i(\theta_0)^2$ and $w_i = w(r_i(\theta_0))$, and add over $i$:

$$Q(\theta) \le Q(\theta_0) + \frac{1}{2}\Big(\sum_i w_i\, r_i(\theta)^2 - \sum_i w_i\, r_i(\theta_0)^2\Big).$$

The right side is equal to $Q(\theta_0)$ at $\theta = \theta_0$. Since $\theta_1$ minimizes $\sum_i w_i\, r_i(\theta)^2$, the bracket is at most 0 at $\theta = \theta_1$, so $Q(\theta_1) \le Q(\theta_0)$. $\square$

Lemma 4 is the step of a majorize-minimize method: the weighted squares give an upper bound of $Q$ that touches it at the current model. For the affine map, $r_i(\theta)^2$ is a quadratic in the 6 parameters, and line L15 solves the weighted normal equations exactly when their matrix is regular. So every pass of lines L13 to L15 that returns a model does not increase $Q$. The code keeps the old model when the matrix is singular.

**Lemma 5 (loop).** Part (e) holds.

*Proof.* Each round raises $t$ by 1 at line L3, and line L11 never sets the bound above $k_{\max}$, so the loop of line L2 ends after at most $k_{\max}$ rounds. For the invariant, we show that at each test of line L2, $Q^*$ is the least quality over all models evaluated so far (the minimal models of line L6 and the polished models of line L9), and $\theta^*$ has the quality $Q^*$. At the start no model has been evaluated and $Q^* = \infty$. In a round, line L6 evaluates $\theta$. If $Q(\theta) \ge Q^*$, nothing else is evaluated and the invariant holds. Otherwise line L8 makes a polished model $\theta'$, line L9 evaluates it and keeps the better of $\theta$ and $\theta'$, and line L10 stores it. Its quality is less than the old $Q^*$, and it is the least of the two new values, so the invariant holds again. At the end, line L12 returns $\theta^*$ and $Q^*$. $\square$

**Remark (what is not proved).** As in [RANSAC](/ransac/), the loop finds a model of least quality only if one of the samples it draws leads to it. The stopping rule of line L11 is a heuristic: it uses the inlier ratio of the best model at a set of noise scales. The papers report the accuracy of MAGSAC and MAGSAC++ in experiments, and these results are not theorems.
