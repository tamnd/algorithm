---
title: Iteratively reweighted least squares is Fisher scoring for a GLM, Newton's method for a canonical link, and a descent method for M-estimation
proves: [correctness, termination]
status: full
---

The arithmetic is exact. $X$ is a fixed real $n \times p$ matrix with rows $x_i^\top$, and line L5 is always applied to a weighted design of rank $p$ (the code raises an error otherwise). By the proof on the [weighted least squares](/weighted-least-squares/) page, line L5 then returns the unique minimizer

$$b^+ = (X^\top WX)^{-1}X^\top Wz, \qquad W = \operatorname{diag}(w_1, \dots, w_n),$$

of $\sum_i w_i(z_i - x_i^\top\beta)^2$. The three lemmas below say what this step is for each kind of working rule.

**Lemma 1 (a GLM step is a Fisher scoring step).** Let $y_i$ have an exponential family law with mean $\mu_i$, variance $\phi V(\mu_i)$ and link $g(\mu_i) = \eta_i = x_i^\top\beta$, with $g$ smooth and strictly monotone. With $z_i = \eta_i + (y_i - \mu_i)g'(\mu_i)$ and $w_i = 1/(V(\mu_i)g'(\mu_i)^2)$, all at the current $b$, the step of line L5 is

$$b^+ = b + \mathcal I(b)^{-1}U(b),$$

where $U$ is the score and $\mathcal I$ the expected information.

*Proof.* The log-likelihood of observation $i$ is $(y_i\theta_i - \kappa(\theta_i))/\phi$ plus a term free of $\beta$, with $\kappa'(\theta) = \mu$ and $\kappa''(\theta) = V(\mu)$. By the chain rule, $\partial\theta_i/\partial\eta_i = (d\mu_i/d\eta_i)/V(\mu_i) = 1/(V(\mu_i)g'(\mu_i))$, so

$$U(\beta) = \frac1\phi\sum_i \frac{y_i - \mu_i}{V(\mu_i)g'(\mu_i)}x_i = \frac1\phi X^\top W\,\bigl((y_i - \mu_i)g'(\mu_i)\bigr)_i.$$

The expected information is $\mathcal I = \operatorname{Cov}U = \frac1{\phi^2}\sum_i \frac{\phi V(\mu_i)}{V(\mu_i)^2g'(\mu_i)^2}x_ix_i^\top = \frac1\phi X^\top WX$. So $b + \mathcal I^{-1}U = (X^\top WX)^{-1}\bigl(X^\top WXb + X^\top W((y_i - \mu_i)g'(\mu_i))_i\bigr) = (X^\top WX)^{-1}X^\top Wz$, since $Xb = \eta$. $\square$

The dispersion $\phi$ cancels, so the iteration does not need it.

**Lemma 2 (for the logistic model the step is the Newton step).** For $y_i \in \{0, 1\}$, $\mu_i = 1/(1 + e^{-\eta_i})$ and the log-likelihood $\ell(\beta) = \sum_i (y_i\eta_i - \log(1 + e^{\eta_i}))$, the Newton step $b - (\nabla^2\ell)^{-1}\nabla\ell$ equals the step of line L5 with $w_i = \mu_i(1 - \mu_i)$ and $z_i = \eta_i + (y_i - \mu_i)/w_i$.

*Proof.* $d\mu/d\eta = \mu(1 - \mu)$, so $\nabla\ell = \sum_i(y_i - \mu_i)x_i = X^\top(y - \mu)$ and $\nabla^2\ell = -\sum_i\mu_i(1 - \mu_i)x_ix_i^\top = -X^\top WX$, which does not depend on $y$. The Newton step is

$$b + (X^\top WX)^{-1}X^\top(y - \mu) = (X^\top WX)^{-1}X^\top W\bigl(Xb + W^{-1}(y - \mu)\bigr) = (X^\top WX)^{-1}X^\top Wz. \qquad\square$$

The same argument works for every canonical link, where $g'(\mu) = 1/V(\mu)$ and the observed information $-\nabla^2\ell$ has no term in $y - \mu$, so it equals $\mathcal I$. For a link that is not canonical, such as the probit link, the observed information has an extra term with factor $y_i - \mu_i$, and the step is Fisher scoring, not Newton. At $b = 0$ in the logistic model every $\mu_i = 1/2$, so $w_i = 1/4$ and $z_i = 4y_i - 2$ are rational, and the first step can be checked in exact arithmetic.

**Lemma 3 (M-estimation: the loss never increases).** Let $\rho(r) = f(r^2)$ with $f$ differentiable, nondecreasing and concave on $[0, \infty)$, and $F(\beta) = \sum_i\rho(y_i - x_i^\top\beta)$. With $z = y$ and $w_i = f'(r_i^2)$ for the current residuals $r_i = y_i - x_i^\top b$, the step satisfies $F(b^+) \le F(b)$. Multiplying all $w_i$ by one positive constant does not change $b^+$.

*Proof.* Concavity gives $f(t) \le f(t_0) + f'(t_0)(t - t_0)$ for all $t, t_0 \ge 0$. With $t = (y_i - x_i^\top\beta)^2$ and $t_0 = r_i^2$, summing over $i$,

$$F(\beta) \le G(\beta) = F(b) + \sum_i w_i\bigl((y_i - x_i^\top\beta)^2 - r_i^2\bigr),$$

with equality at $\beta = b$. Line L5 minimizes $\sum_iw_i(y_i - x_i^\top\beta)^2$, which is $G$ up to a constant, so $F(b^+) \le G(b^+) \le G(b) = F(b)$. The scale statement holds because a constant factor in all weights does not change the minimizer. $\square$

The rules of the implementation fit Lemma 3, with $u = r/s$ for a fixed scale $s$:

- Huber: $f(t) = t/2$ for $t \le c^2$ and $c\sqrt t - c^2/2$ beyond. Then $f'(t) = \min(1/2, c/(2\sqrt t))$ is continuous and nonincreasing, so $f$ is concave, and $2f'(u^2) = \min(1, c/|u|)$.
- Tukey biweight: $f(t) = (c^2/6)(1 - (1 - t/c^2)^3)$ for $t \le c^2$ and $c^2/6$ beyond. Then $f'(t) = \frac12(1 - t/c^2)^2$ for $t \le c^2$ and $0$ beyond, which is nonincreasing, and $2f'(u^2) = (1 - u^2/c^2)^2$. The loss $\rho$ is not convex in $r$, so the iteration can stop at a local minimum.
- L1 with a floor $\delta > 0$: $f(t) = t/(2\delta)$ for $t \le \delta^2$ and $\sqrt t - \delta/2$ beyond, so $\rho_\delta(r) = r^2/(2\delta)$ for $|r| \le \delta$ and $|r| - \delta/2$ beyond, and $2f'(r^2) = 1/\max(|r|, \delta)$.

**Lemma 4 (the L1 rule is within $n\delta/2$ of least absolute deviations).** Let $b^*$ be a fixed point of the L1 rule, that is $b^+ = b^*$ when $b = b^*$, and let $m = \min_\beta\sum_i|y_i - x_i^\top\beta|$. Then $m \le \sum_i|y_i - x_i^\top b^*| \le m + n\delta/2$.

*Proof.* The left inequality is the definition of $m$. Let $F_\delta(\beta) = \sum_i\rho_\delta(y_i - x_i^\top\beta)$; $F_\delta$ is convex and differentiable, because $\rho_\delta$ is convex with a continuous derivative. The majorizer $G$ of Lemma 3 at $b^*$ touches $F_\delta$ at $b^*$ and lies above it, so the two have the same gradient there: $\nabla G(b^*) = -2\sum_iw_ir_ix_i = -\sum_i\rho_\delta'(r_i)x_i = \nabla F_\delta(b^*)$, using $2f'(r^2)r = \rho_\delta'(r)$. Since $b^*$ minimizes $G$, $\nabla F_\delta(b^*) = 0$, and $b^*$ minimizes the convex $F_\delta$. From $|r| - \delta/2 \le \rho_\delta(r) \le |r|$,

$$\sum_i|y_i - x_i^\top b^*| \le F_\delta(b^*) + \frac{n\delta}2 \le F_\delta(\beta_{\mathrm{LAD}}) + \frac{n\delta}2 \le m + \frac{n\delta}2,$$

where $\beta_{\mathrm{LAD}}$ attains $m$. $\square$

**What is not proved.** Lemma 3 gives a nonincreasing loss sequence, which therefore converges, but it does not prove that the coefficients converge, and with the biweight they can converge to a local minimum. For a GLM, Lemmas 1 and 2 describe one step only. Newton's method converges quadratically near a maximizer where the information is nonsingular, but from a poor start the full step can increase the deviance, and when the maximum likelihood estimate does not exist (separation in a binary model) the iterates go to infinity. The implementation reports these cases through `converged` and `separation_suspected`; it does not halve steps.

**Termination.** Each pass of lines L3 to L7 is a finite computation: $O(np)$ for $\eta$, $O(n)$ for the rule and $\Theta(np^2)$ for the weighted QR. The loop of line L2 runs at most `maxit` times, so the algorithm stops after $O(\text{maxit}\cdot np^2)$ operations, with `converged` true exactly when line L6 stopped it.
