---
title: The t interval has coverage exactly 1 - alpha under normal iid data, is dual to the t-test, and has the stated expected width
proves: [correctness, termination]
status: full
---

We prove that the three intervals returned by the code cover the mean with probability exactly $1 - \alpha$ for every $\mu$ and $\sigma$ when the data are iid normal, that the two-sided interval is the set of null values the two-sided t-test does not reject, that without normality the coverage tends to $1 - \alpha$, and we compute the expected width. $X_1, \dots, X_n$ are iid $N(\mu, \sigma^2)$, $n \ge 2$, $S^2$ has the divisor $n - 1$, $\nu = n - 1$, and $q_p = t_{(\nu, p)}$ is the lower $p$ quantile of $t_\nu$.

**Lemma 1 (the pivot).** $Q = (\bar X - \mu)/(S/\sqrt n)$ has the $t_{n-1}$ law for every $\mu$ and every $\sigma > 0$.

*Proof.* This is Lemma 2 of the correctness proof of [Student's t-test](/student-t-test/) with $\mu_0 = \mu$, so $\lambda = 0$: by Helmert's transformation, $\sqrt n(\bar X - \mu)/\sigma \sim N(0, 1)$ is independent of $(n - 1)S^2/\sigma^2 \sim \chi^2_{n-1}$, and their ratio, with $\sigma$ cancelled, is $t_{n-1}$ by definition. $\square$

A pivot is a function of the data and the parameter whose law does not depend on any parameter. Lemma 1 is the whole reason the interval is exact.

**Lemma 2 (exact coverage).** For every $\mu$ and $\sigma > 0$:

1. $P\big(\bar X - q_{1-\alpha/2}S/\sqrt n \le \mu \le \bar X + q_{1-\alpha/2}S/\sqrt n\big) = 1 - \alpha$;
2. $P\big(\mu \ge \bar X - q_{1-\alpha}S/\sqrt n\big) = 1 - \alpha$ (lower bound);
3. $P\big(\mu \le \bar X + q_{1-\alpha}S/\sqrt n\big) = 1 - \alpha$ (upper bound).

*Proof.* $S > 0$ with probability 1, because the $X_i$ are all equal with probability 0 for a continuous law. Dividing by $S/\sqrt n > 0$ keeps the inequalities. Event 1 is $\{-q_{1-\alpha/2} \le Q \le q_{1-\alpha/2}\}$. The $t_\nu$ law is continuous and symmetric, so $q_{\alpha/2} = -q_{1-\alpha/2}$ and the event has probability $(1 - \alpha/2) - \alpha/2 = 1 - \alpha$ by Lemma 1. Event 2 is $\{Q \le q_{1-\alpha}\}$, with probability $1 - \alpha$. Event 3 is $\{Q \ge -q_{1-\alpha}\} = \{Q \ge q_\alpha\}$, with probability $1 - \alpha$ because $P(Q = q_\alpha) = 0$. The probabilities do not depend on $(\mu, \sigma)$, so the infimum over the parameter space, which is the confidence coefficient, is also $1 - \alpha$. $\square$

The probability in Lemma 2 is over the sample. For a fixed computed interval, $\mu$ either lies in it or does not; the statement is about the procedure.

**Lemma 3 (duality with the t-test).** Let $p(\mu_0) = 2\bar F_\nu\big(|\bar x - \mu_0|/(s/\sqrt n)\big)$ be the two-sided t-test p-value for $H_0: \mu = \mu_0$ on data with $s > 0$. Then $p(\mu_0) \ge \alpha$ if and only if $\mu_0$ lies in the closed interval $\bar x \pm q_{1-\alpha/2}s/\sqrt n$, and $p(\mu_0) > \alpha$ if and only if $\mu_0$ lies in its interior. The same holds for the one-sided bounds and one-sided tests.

*Proof.* $\bar F_\nu$ is continuous and strictly decreasing, and $\bar F_\nu(q_{1-\alpha/2}) = \alpha/2$. So $p(\mu_0) \ge \alpha$ iff $|\bar x - \mu_0|/(s/\sqrt n) \le q_{1-\alpha/2}$ iff $|\bar x - \mu_0| \le q_{1-\alpha/2}s/\sqrt n$, and the strict versions match. For the lower bound, the "greater" test of $H_0: \mu \le \mu_0$ has $p = \bar F_\nu\big((\bar x - \mu_0)/(s/\sqrt n)\big)$, and $p \ge \alpha$ iff $\mu_0 \ge \bar x - q_{1-\alpha}s/\sqrt n$; the upper bound is symmetric. $\square$

The test rejects when $p \le \alpha$, so the closed interval contains the set of values it does not reject plus its two end points, where the p-value is exactly $\alpha$. This event of probability 0 is why the closed and the open interval have the same coverage.

**Lemma 4 (one-sided bounds from the two-sided interval).** The $1 - \alpha$ lower bound equals the left end of the two-sided $1 - 2\alpha$ interval, and the $1 - \alpha$ upper bound equals its right end.

*Proof.* Both use the quantile $q_{1-\alpha} = q_{1 - (2\alpha)/2}$ and the same $\bar X$ and $S$. $\square$

**Lemma 5 (expected width).** The two-sided interval has width $2q_{1-\alpha/2}S/\sqrt n$, and $E[S] = c_4(n)\sigma$ with $c_4(n) = \sqrt{2/(n - 1)}\,\Gamma(n/2)/\Gamma((n - 1)/2)$, so the expected width is $2q_{1-\alpha/2}c_4(n)\sigma/\sqrt n$.

*Proof.* $S = \sigma\sqrt{V/(n - 1)}$ with $V \sim \chi^2_k$, $k = n - 1$. With the $\chi^2_k$ density $v^{k/2-1}e^{-v/2}/(2^{k/2}\Gamma(k/2))$,

$$E[\sqrt V] = \frac{1}{2^{k/2}\Gamma(k/2)}\int_0^\infty v^{(k+1)/2-1}e^{-v/2}\,dv = \frac{2^{(k+1)/2}\Gamma((k + 1)/2)}{2^{k/2}\Gamma(k/2)} = \sqrt 2\,\frac{\Gamma((k + 1)/2)}{\Gamma(k/2)} ,$$

so $E[S] = \sigma\sqrt{2/k}\,\Gamma(n/2)/\Gamma((n - 1)/2)$. $\square$

**Lemma 6 (without normality).** Let $X_1, \dots, X_n$ be iid with mean $\mu$ and finite variance $\sigma^2 > 0$. Then the coverage of each of the three intervals tends to $1 - \alpha$ as $n \to \infty$.

*Proof.* By Lemma 7 of the Student proof (the [central limit theorem](/central-limit-theorem/) and Slutsky's theorem), $Q$ converges in distribution to $N(0, 1)$, and $q_{1-\alpha/2} \to z_{1-\alpha/2}$, $q_{1-\alpha} \to z_{1-\alpha}$. The coverage events are $\{|Q| \le q_{1-\alpha/2}\}$, $\{Q \le q_{1-\alpha}\}$ and $\{Q \ge -q_{1-\alpha}\}$, and the limit law is continuous, so their probabilities tend to $1 - \alpha$. $\square$

The convergence is not uniform over the distributions with finite variance, so no fixed $n$ guarantees a coverage close to $1 - \alpha$ for every such distribution.

**Termination.** The code makes two passes over $n$ numbers. The quantile is computed by bisection on the $t_\nu$ upper tail: the bracket is doubled until it contains the quantile, which takes finitely many steps because $\bar F_\nu(x) \to 0$, and then halved at most 400 times or until no double lies strictly between the end points. Each tail evaluation is a continued fraction with an iteration cap. So the procedure stops.

**Theorem.** Under iid normal data, the two-sided t interval and the one-sided t bounds computed by the code have coverage exactly $1 - \alpha$ for every $\mu$, $\sigma$ and $n \ge 2$; the two-sided interval is the closure of the set of $\mu_0$ that the two-sided level $\alpha$ t-test does not reject; and for iid data with finite positive variance the coverage tends to $1 - \alpha$.

*Proof.* Lemmas 1 and 2 for the coverage, Lemma 3 for the duality, and Lemma 6 for the limit. $\blacksquare$
