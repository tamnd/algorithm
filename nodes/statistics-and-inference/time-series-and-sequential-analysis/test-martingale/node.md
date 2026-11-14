---
tag: 8V449R
kind: definition
slug: test-martingale
name: Test martingale
aliases:
- nonnegative supermartingale test
area: statistics-and-inference/time-series-and-sequential-analysis
level: research
summary: A nonnegative process that starts at 1 and is a martingale (or supermartingale) under the null. It is the wealth of a bettor against the null and can be checked at any time.
prereqs: [martingale, e-variable]
see_also: [ville-inequality, confidence-sequence, mixture-sequential-probability-ratio-test, sequential-probability-ratio-test, optional-stopping-theorem, bayes-factor, p-value, kullback-leibler-divergence]
sources:
  - paper: doi:10.1214/10-STS347
    title: Glenn Shafer, Alexander Shen, Nikolai Vereshchagin and Vladimir Vovk, Test martingales, Bayes factors and p-values, Statistical Science 26(1) (2011), pages 84 to 101
    locator: the definition of a test martingale, its relation to Bayes factors and p-values, and the history of the idea from Ville
  - paper: doi:10.1214/23-STS894
    title: Aaditya Ramdas, Peter Grünwald, Vladimir Vovk and Glenn Shafer, Game-theoretic statistics and safe anytime-valid inference, Statistical Science 38(4) (2023), pages 576 to 601
    locator: test martingales, test supermartingales and e-processes for composite nulls, and testing by betting
  - paper: doi:10.1016/j.ijar.2021.06.017
    title: Aaditya Ramdas, Johannes Ruf, Martin Larsson and Wouter M. Koolen, Testing exchangeability, fork-convexity, supermartingales and e-processes, International Journal of Approximate Reasoning 141 (2022), pages 83 to 109
    locator: e-processes that are not supermartingales, and the test of exchangeability where they are needed
  - paper: doi:10.1214/18-PS321
    title: Steven R. Howard, Aaditya Ramdas, Jon McAuliffe and Jasjeet Sekhon, Time-uniform Chernoff bounds via nonnegative supermartingales, Probability Surveys 17 (2020), pages 257 to 317
    locator: nonnegative supermartingales built from exponential and mixture constructions, with Ville's inequality
---

A test martingale for a null hypothesis is a [martingale](/martingale/) $(M_t)_{t \ge 0}$ that starts at $M_0 = 1$ and never takes a negative value under every distribution of the null. Its value is the wealth of a bettor who starts with one unit and makes fair bets against the null, so a large value is evidence against the null. By [Ville's inequality](/ville-inequality/) the process ever reaches $1/\alpha$ with null probability at most $\alpha$, so a test that rejects at that level is valid no matter when the analyst looks or stops. The value at any stopping time is an [e-variable](/e-variable/).

## Definition

Let $X_1, X_2, \ldots$ be observations, let $\mathcal F_t = \sigma(X_1, \ldots, X_t)$ with $\mathcal F_0$ trivial, and let $\mathcal H_0$ be a set of distributions of the sequence, the null hypothesis.

**Test supermartingale.** A process $(M_t)_{t \ge 0}$ is a test supermartingale for $\mathcal H_0$ when, for every $P \in \mathcal H_0$:

1. $M_t$ is $\mathcal F_t$-measurable with values in $[0, \infty)$ for every $t \ge 0$;
2. $M_0 = 1$;
3. $E_P[M_t \mid \mathcal F_{t-1}] \le M_{t-1}$ for every $t \ge 1$, $P$-almost surely.

**Test martingale.** It is a test martingale when the inequality in 3 is an equality for every $P \in \mathcal H_0$. For a simple null $\mathcal H_0 = \{P\}$ this is the definition of Shafer, Shen, Vereshchagin and Vovk (2011): a nonnegative $P$-martingale with initial value 1.

**Limit and stopped value.** A nonnegative supermartingale converges almost surely, so $M_\infty = \lim_{t \to \infty} M_t$ exists $P$-almost surely. For a stopping time $\tau$, possibly infinite, $M_\tau$ means $M_\infty$ on $\{\tau = \infty\}$.

**Every test supermartingale is an e-process.** A process $(E_t)$ is an e-process for $\mathcal H_0$ when $E_P[E_\tau] \le 1$ for every $P \in \mathcal H_0$ and every stopping time $\tau$. A test supermartingale has this property. Fix $P \in \mathcal H_0$ and a stopping time $\tau$. For each $n$, $\tau \wedge n$ is a bounded stopping time, so the [optional stopping theorem](/optional-stopping-theorem/) for supermartingales gives $E_P[M_{\tau \wedge n}] \le E_P[M_0] = 1$. As $n \to \infty$, $M_{\tau \wedge n} \to M_\tau$ almost surely, and Fatou's lemma, which needs $M \ge 0$, gives $E_P[M_\tau] \le \liminf_n E_P[M_{\tau \wedge n}] \le 1$. So $M_\tau$ is an e-variable for every stopping time $\tau$.

The converse is false. If for each $P \in \mathcal H_0$ the process $M^P$ is a test martingale for $\{P\}$, then $E_t = \inf_{P \in \mathcal H_0} M^P_t$ satisfies $E_P[E_\tau] \le E_P[M^P_\tau] \le 1$, so it is an e-process, but in general it is not a supermartingale under any $P$. Ramdas, Ruf, Larsson and Koolen (2022) use such processes to test exchangeability, a composite null for which test supermartingales are weak. So "e-process" is the wider class, not a second name for this one.

**Anytime-valid p-value.** The process $p_t = \min\bigl(1, 1/\max_{s \le t} M_s\bigr)$ is nonincreasing, and by Ville's inequality $P(\exists t: p_t \le \alpha) \le \alpha$ for every $P \in \mathcal H_0$ and every $\alpha \in (0, 1]$.

**Construction by betting.** Most test martingales are running products. Let $q_t$ be a density that depends only on $X_1, \ldots, X_{t-1}$ (a predictable bet), and let $\mathcal H_0 = \{P\}$ with conditional density $p_t(\cdot \mid \mathcal F_{t-1})$ positive where $q_t$ is. Then
$$M_t = \prod_{i=1}^t \frac{q_i(X_i)}{p_i(X_i)}$$
is a test martingale, because $E_P[q_t(X_t)/p_t(X_t) \mid \mathcal F_{t-1}] = \int q_t = 1$. For observations in $[0, 1]$ with null mean $\mu_0$, the product $\prod_{i \le t}(1 + \lambda_i (X_i - \mu_0))$ with predictable $\lambda_i \in [-1/(1 - \mu_0), 1/\mu_0]$ is a test martingale for the whole composite null "the conditional mean is $\mu_0$": each factor is nonnegative and has conditional mean 1. A mixture $\int M^{(\lambda)}_t\,\pi(d\lambda)$ of test martingales with a prior $\pi$ fixed in advance is again a test martingale, by Fubini's theorem.

## Examples and non-examples

**A likelihood ratio on a coin.** Test the fair coin, $P$: the flips are i.i.d. with heads probability $1/2$, against the bet $q$: heads with probability $0.7$. A head multiplies the wealth by $0.7/0.5 = 1.4$ and a tail by $0.3/0.5 = 0.6$. The conditional mean of a factor under $P$ is $\tfrac12(1.4) + \tfrac12(0.6) = 1$. On the flips HHTHHHTH:

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| flip | H | H | T | H | H | H | T | H |
| $M_t$ | 1.4 | 1.96 | 1.176 | 1.6464 | 2.3050 | 3.2269 | 1.9362 | 2.7106 |

So $M_8 = 1.4^6 \cdot 0.6^2 = 1058841/390625 \approx 2.7106$. The largest value is $M_6 \approx 3.2269$, so the anytime-valid p-value after eight flips is $1/3.2269 \approx 0.31$. Rejecting the fair coin at $\alpha = 0.05$ needs $M_t \ge 20$.

**The Gaussian exponential martingale.** For i.i.d. $N(0, 1)$ data with sum $S_t$ and a fixed $\lambda$, the process $M_t = \exp(\lambda S_t - \lambda^2 t/2)$ is a test martingale for $\mathcal H_0 = \{N(0,1)^\infty\}$, since $E[e^{\lambda X - \lambda^2/2}] = 1$. Mixing over $\lambda \sim N(0, \rho^2)$ gives the normal mixture $(1 + t\rho^2)^{-1/2}\exp\bigl(\rho^2 S_t^2 / (2(1 + t\rho^2))\bigr)$, which is the statistic of the [mixture SPRT](/mixture-sequential-probability-ratio-test/) and of a normal [confidence sequence](/confidence-sequence/).

**A Bayes factor.** For a simple null $P_0$ and a prior $\pi$ on alternatives $P_\theta$ fixed before the data, the [Bayes factor](/bayes-factor/) $\int \prod_{i \le t} p_\theta(X_i)\,\pi(d\theta) / \prod_{i \le t} p_0(X_i)$ is a test martingale for $P_0$. Shafer et al. (2011) discuss this link.

**Non-example: the missing drift term.** $M_t = \exp(\lambda S_t)$ with $\lambda \ne 0$ is nonnegative and starts at 1, but $E[M_t] = e^{\lambda^2 t/2} > 1$ for $t \ge 1$. It is a submartingale, and a rule that rejects when it exceeds $1/\alpha$ has no level-$\alpha$ guarantee.

**Non-example: a bet placed after the outcome.** On the coin, let the bettor pick the side after seeing the flip: the factor is 1.4 whatever happens, so $M_t = 1.4^t$. Here $q_t$ depends on $X_t$, so it is not predictable, and $E_P[M_t] = 1.4^t$.

**Non-example: the wrong start.** A nonnegative martingale with $M_0 = 2$ satisfies only $P(\sup_t M_t \ge 1/\alpha) \le 2\alpha$. Dividing by 2 gives a test martingale.

**Non-example: the running maximum.** $\max_{s \le t} M_s$ is nonnegative and starts at 1, but it is a submartingale, not a supermartingale. On the coin it is 3.2269 at $t = 8$ while $M_8 = 2.7106$. Its reciprocal is still the anytime-valid p-value above, because the guarantee comes from Ville's inequality on $M$.

## Related definitions

- **E-variable.** An [e-variable](/e-variable/) is one nonnegative statistic with null mean at most 1. A test supermartingale gives one at every stopping time, as shown above.
- **E-process.** The wider class of processes with $E_P[E_\tau] \le 1$ for all stopping times and all null $P$. Every test supermartingale is an e-process; the infimum construction above gives e-processes that are not supermartingales (Ramdas et al. 2022, 2023).
- **Martingale.** A test martingale is a [martingale](/martingale/) under each null distribution, with the two extra conditions $M_0 = 1$ and $M_t \ge 0$.
- **Ville's inequality.** [Ville's inequality](/ville-inequality/) is the time-uniform bound $P(\sup_t M_t \ge 1/\alpha) \le \alpha$ that turns a test supermartingale into a sequential test.
- **Sequential tests.** The log of the [SPRT](/sequential-probability-ratio-test/) statistic is the log of a likelihood-ratio test martingale; the [mixture SPRT](/mixture-sequential-probability-ratio-test/) uses a mixture; a [confidence sequence](/confidence-sequence/) collects the parameter values whose test martingale stays below $1/\alpha$.
- **Growth rate.** Let the data be i.i.d. from $Q$ and let the bet be a fixed density $q$. By the [law of large numbers](/law-of-large-numbers/), $\frac1t \log M_t \to E_Q[\log(q/p)] = D(Q \,\|\, P) - D(Q \,\|\, q)$ almost surely, with $D$ the [Kullback-Leibler divergence](/kullback-leibler-divergence/). The rate is largest, equal to $D(Q \,\|\, P)$, when the bet is $q = Q$. This is the reason to bet with a good guess of the alternative.

## References
