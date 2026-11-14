---
tag: 5X8RTE
kind: definition
slug: confidence-sequence
name: Confidence sequence
aliases:
- anytime-valid confidence interval
area: statistics-and-inference/time-series-and-sequential-analysis
level: research
summary: A sequence of confidence sets that contains the true parameter at all times at once with probability 1 - alpha, so it stays valid at any stopping time.
prereqs: [confidence-interval, test-martingale, ville-inequality]
see_also: [mixture-sequential-probability-ratio-test, test-interval-duality, e-variable, group-sequential-design, hoeffding-inequality, central-limit-theorem, multi-armed-bandit, sequential-probability-ratio-test]
sources:
  - paper: doi:10.1073/pnas.58.1.66
    title: D. A. Darling and Herbert Robbins, Confidence sequences for mean, variance, and median, Proceedings of the National Academy of Sciences 58(1) (1967), pages 66 to 68
    locator: the definition of a confidence sequence and the first constructions for the mean, the variance and the median
  - paper: doi:10.1214/20-AOS1991
    title: Steven R. Howard, Aaditya Ramdas, Jon McAuliffe and Jasjeet Sekhon, Time-uniform, nonparametric, nonasymptotic confidence sequences, Annals of Statistics 49(2) (2021), pages 1055 to 1080
    locator: the equivalence of time-uniform coverage and coverage at stopping times, the normal mixture boundary, and stitched boundaries with iterated-logarithm width
  - paper: doi:10.1214/18-PS321
    title: Steven R. Howard, Aaditya Ramdas, Jon McAuliffe and Jasjeet Sekhon, Time-uniform Chernoff bounds via nonnegative supermartingales, Probability Surveys 17 (2020), pages 257 to 317
    locator: the supermartingale constructions behind time-uniform boundaries, with Ville's inequality
  - paper: doi:10.1214/aoms/1177696786
    title: Herbert Robbins, Statistical methods related to the law of the iterated logarithm, Annals of Mathematical Statistics 41(5) (1970), pages 1397 to 1409
    locator: the method of mixtures and the resulting boundary-crossing bounds for sums
  - paper: doi:10.1287/opre.2021.2135
    title: Ramesh Johari, Pete Koomen, Leonid Pekelis and David Walsh, Always valid inference, continuous monitoring of A/B tests, Operations Research 70(3) (2022), pages 1806 to 1821
    locator: always valid confidence intervals obtained by inverting the mixture SPRT
---

A confidence sequence is a sequence of [confidence sets](/confidence-interval/) $C_1, C_2, \ldots$, one after each new observation, such that with probability at least $1 - \alpha$ the true parameter lies in every one of them at the same time. A fixed-sample confidence interval covers the parameter at one planned sample size; a confidence sequence covers it at all sample sizes together, so the analyst can watch the interval shrink, stop at any time for any reason, and still report a set with coverage $1 - \alpha$. The usual construction inverts a family of [test martingales](/test-martingale/) with [Ville's inequality](/ville-inequality/). Darling and Robbins introduced the idea in 1967.

## Definition

Let $X_1, X_2, \ldots$ be observations with a distribution $P$ from a model $\mathcal P$, let $\theta(P)$ be a parameter with values in a set $\Theta$, and let $\mathcal F_t = \sigma(X_1, \ldots, X_t)$.

**Definition.** A $(1 - \alpha)$ confidence sequence for $\theta$ is a sequence of sets $C_t \subseteq \Theta$, $t \ge 1$, where each $C_t$ is a function of $X_1, \ldots, X_t$, such that
$$P\bigl(\theta(P) \in C_t \text{ for all } t \ge 1\bigr) \ge 1 - \alpha \quad \text{for every } P \in \mathcal P.$$

**Equivalent form.** The sets $(C_t)$ form a $(1 - \alpha)$ confidence sequence if and only if $P(\theta(P) \in C_\tau) \ge 1 - \alpha$ for every $P \in \mathcal P$ and every stopping time $\tau$ with respect to $(\mathcal F_t)$, where $\tau$ may take the value $\infty$ and the event $\{\theta \in C_\infty\}$ is read as "true" (Howard, Ramdas, McAuliffe and Sekhon 2021). Proof. If the uniform statement holds, then $\{\theta \notin C_\tau\} \subseteq \{\exists t: \theta \notin C_t\}$, which has probability at most $\alpha$; this direction holds even for random times that are not stopping times. Conversely, fix $P$, write $\theta = \theta(P)$, and let $\tau = \inf\{t : \theta \notin C_t\}$. It is a stopping time. For each $N$, $\tau \wedge N$ is a stopping time and $\{\theta \notin C_{\tau \wedge N}\} = \{\tau \le N\}$, so $P(\tau \le N) \le \alpha$. Letting $N \to \infty$ gives $P(\exists t: \theta \notin C_t) = P(\tau < \infty) \le \alpha$. $\square$

**Construction from test martingales.** Suppose that for each $\theta \in \Theta$ there is a process $M_t(\theta)$, computable from $X_1, \ldots, X_t$, which is a test supermartingale under every $P$ with $\theta(P) = \theta$. Let
$$C_t = \{\theta \in \Theta : M_t(\theta) < 1/\alpha\}.$$
Then $(C_t)$ is a $(1 - \alpha)$ confidence sequence: for the true $\theta$, the event that some $C_t$ misses it is the event that $M_t(\theta) \ge 1/\alpha$ for some $t$, which has probability at most $\alpha$ by Ville's inequality. The running intersection $C'_t = C_1 \cap \cdots \cap C_t$ misses $\theta$ only if some $C_s$ does, so it is also a confidence sequence, and it never grows. This is the sequential form of [test-interval duality](/test-interval-duality/).

## Examples and non-examples

**The normal mixture confidence sequence.** Let $X_i$ be i.i.d. $N(\mu, 1)$, $S_t = X_1 + \cdots + X_t$ and $\bar X_t = S_t/t$. For each $\mu$, mixing the exponential martingale $\exp(\lambda(S_t - t\mu) - \lambda^2 t/2)$ over $\lambda \sim N(0, \rho^2)$ gives the test martingale
$$M_t(\mu) = \frac{1}{\sqrt{1 + t\rho^2}}\exp\left(\frac{\rho^2 (S_t - t\mu)^2}{2(1 + t\rho^2)}\right).$$
Solving $M_t(\mu) < 1/\alpha$ for $\mu$ gives the interval $\bar X_t \pm w_t$ with
$$w_t = \frac1t\sqrt{\frac{1 + t\rho^2}{\rho^2}\left(2\log\frac1\alpha + \log(1 + t\rho^2)\right)}.$$
The free parameter $\rho > 0$ chooses the sample sizes where the interval is tightest. With $\rho = 1$ and $\alpha = 0.05$, against the fixed-sample half-width $1.96/\sqrt t$:

| $t$ | 10 | 100 | 1000 | 10 000 |
|---|---|---|---|---|
| confidence sequence $w_t$ | 0.9606 | 0.3273 | 0.1136 | 0.0390 |
| fixed-sample $1.96/\sqrt t$ | 0.6198 | 0.1960 | 0.0620 | 0.0196 |
| ratio | 1.55 | 1.67 | 1.83 | 1.99 |

The ratio grows like $\sqrt{\log t}$, since $w_t \sim \sqrt{\log t / t}$.

**Non-example: the fixed-sample interval at every step.** The interval $\bar X_t \pm 1.96/\sqrt t$ covers $\mu$ with probability 0.95 at each fixed $t$, but not at all $t$ together. In 1000 simulated paths of $N(0, 1)$ data, it missed the true mean at some $t \le 100$ in 38.6% of the paths, at some $t \le 1000$ in 52.4%, and at some $t \le 10\,000$ in 64.0%; the normal mixture sequence above with $\rho = 1$ missed at some $t \le 10\,000$ in 3.1%. By the law of the iterated logarithm, $\limsup_t |S_t - t\mu| / \sqrt{2t \log\log t} = 1$ almost surely, so the fixed-sample interval misses the mean infinitely often with probability 1.

**A union bound example.** Choose $\alpha_t = \alpha/(t(t+1))$, which add up to $\alpha$, and take the fixed-sample interval at level $1 - \alpha_t$ at each $t$. By the union bound this is a confidence sequence. It is valid but wide: for the normal model with $\alpha = 0.05$ its half-width $z_{1 - \alpha_t/2}/\sqrt t$ is 1.1088, 0.4567, 0.1724 and 0.0622 at $t = 10$, 100, 1000 and 10 000, which is 1.15 to 1.59 times the mixture width $w_t$ of the table. The squared quantile grows like $4\log t$ against $\log t$ for the mixture, so the ratio tends to 2, slowly.

**Bounded data.** For $X_i \in [0, 1]$ with conditional mean $\mu$, the betting products $\prod_{i \le t}(1 + \lambda_i(X_i - \mu))$ of the [test martingale](/test-martingale/) page give a confidence sequence for $\mu$ with no other assumption. The [Hoeffding](/hoeffding-inequality/) supermartingale gives a simpler one with a closed form.

**Non-example: stop when the interval looks good.** An analyst computes the fixed-sample interval after each observation, stops at the first $t$ where it excludes 0, and reports that interval. The report is $C_\tau$ for a stopping time $\tau$, so by the equivalence above its coverage is at least $1 - \alpha$ under every such rule only when the whole sequence is a confidence sequence. With true mean 0 and at most 1000 observations, the simulation above shows that this rule ends with an interval that misses 0 in 52.4% of the paths.

## Related definitions

- **Confidence interval.** The fixed-sample notion, with $P(\theta \in C_n) \ge 1 - \alpha$ for one $n$ fixed in advance. A confidence sequence restricted to one $t$ is a confidence interval; the converse fails, as shown above.
- **Width.** No confidence sequence for a mean with finite variance can have width $c\sqrt{2\log\log t / t}$ with $c < 1$ for all large $t$, by the law of the iterated logarithm, since such intervals miss the mean infinitely often almost surely. Howard et al. (2021) construct stitched boundaries with width of order $\sqrt{\log\log t / t}$; the normal mixture has the larger order $\sqrt{\log t / t}$ but smaller constants over a planned range of $t$.
- **Always valid confidence interval.** Inverting the [mixture SPRT](/mixture-sequential-probability-ratio-test/) gives the normal mixture confidence sequence above; Johari, Koomen, Pekelis and Walsh (2022) call its running intersection an always valid confidence interval and use it in online experiments.
- **Repeated confidence intervals.** In a [group sequential design](/group-sequential-design/), intervals computed at a few planned analyses with the group sequential critical values cover the parameter at all analyses together. They are confidence sequences for a finite set of times.
- **Sequential tests.** A confidence sequence gives an anytime-valid test of $\theta = \theta_0$: reject at the first $t$ with $\theta_0 \notin C_t$. Its type I error is at most $\alpha$ by the definition.

## References
