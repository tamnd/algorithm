---
tag: WDQ3S8
kind: theorem
slug: ville-inequality
name: Ville's inequality
aliases:
- maximal inequality for nonnegative supermartingales
area: statistics-and-inference/time-series-and-sequential-analysis
level: research
summary: A nonnegative supermartingale that starts at 1 ever reaches 1 / alpha with probability at most alpha. It makes sequential tests valid under optional stopping.
prereqs: [martingale, markov-inequality, optional-stopping-theorem]
see_also: [test-martingale, e-variable, confidence-sequence, mixture-sequential-probability-ratio-test, sequential-probability-ratio-test, azuma-inequality, hoeffding-inequality]
sources:
  - book: isbn:9781108473682
    title: Rick Durrett, Probability, Theory and Examples, fifth edition, Cambridge University Press, 2019
    locator: Section 4.4 (Doob's inequality, convergence in L^p)
  - paper: doi:10.1214/10-STS347
    title: Glenn Shafer, Alexander Shen, Nikolai Vereshchagin and Vladimir Vovk, Test martingales, Bayes factors and p-values, Statistical Science 26(1) (2011), pages 84 to 101
    locator: Ville's inequality for test martingales and its history in Ville's 1939 thesis
  - paper: doi:10.1214/18-PS321
    title: Steven R. Howard, Aaditya Ramdas, Jon McAuliffe and Jasjeet Sekhon, Time-uniform Chernoff bounds via nonnegative supermartingales, Probability Surveys 17 (2020), pages 257 to 317
    locator: Ville's maximal inequality as the tool that turns nonnegative supermartingales into time-uniform bounds
  - paper: doi:10.1214/23-STS894
    title: Aaditya Ramdas, Peter Grünwald, Vladimir Vovk and Glenn Shafer, Game-theoretic statistics and safe anytime-valid inference, Statistical Science 38(4) (2023), pages 576 to 601
    locator: Ville's inequality as the basis of anytime-valid tests, p-values and confidence sequences
---

Ville's inequality bounds the probability that a nonnegative [supermartingale](/martingale/) ever climbs high: the chance that it ever reaches a level $a$ is at most its starting mean divided by $a$. It is [Markov's inequality](/markov-inequality/) for the whole path at once, not for one fixed time. For a [test martingale](/test-martingale/), which starts at 1, it says that the wealth of a bettor against a true null ever reaches $1/\alpha$ with probability at most $\alpha$. This is what makes sequential tests and [confidence sequences](/confidence-sequence/) valid when the analyst checks the data after every observation and stops at will.

## Statement

**Theorem (Ville's inequality).** Let $(M_t)_{t \ge 0}$ be a supermartingale with respect to a filtration $(\mathcal F_t)_{t \ge 0}$ under a probability $P$, with $M_t \ge 0$ for all $t$. Then for every $a > 0$,
$$P\Bigl(\sup_{t \ge 0} M_t \ge a\Bigr) \le \frac{E[M_0]}{a}.$$
In particular, if $M_0 = 1$ and $0 < \alpha \le 1$, then $P(\exists t \ge 0: M_t \ge 1/\alpha) \le \alpha$.

Here $t$ runs over $\{0, 1, 2, \ldots\}$. The supermartingale property means that each $M_t$ is $\mathcal F_t$-measurable and integrable and $E[M_t \mid \mathcal F_{t-1}] \le M_{t-1}$ almost surely for $t \ge 1$.

## In plain words

A gambler starts with one unit of money and makes a sequence of bets that are fair or worse for the gambler, and can never owe money. The rule says that the chance that the gambler is ever twenty times richer than at the start is at most one in twenty. It does not matter how the gambler picks the bets, when the gambler looks at the balance, or whether the game ever ends. A test of a hypothesis can use the same idea. The tester bets against the hypothesis. If the hypothesis is true, the bets are fair, so a big win is rare. The tester can look after every new data point and stop at the first big win, and the false alarm rate stays below the chosen level.

## Proof

Fix $a > 0$. Let $\tau = \inf\{t \ge 0 : M_t \ge a\}$, with $\inf \emptyset = \infty$. The event $\{\tau \le t\}$ depends only on $M_0, \ldots, M_t$, so $\tau$ is a stopping time and $\{\tau \ge t\} = \{\tau \le t - 1\}^c \in \mathcal F_{t-1}$ for $t \ge 1$.

*Step 1: the stopped mean does not grow.* Fix an integer $N \ge 0$. For every outcome,
$$M_{\tau \wedge N} = M_0 + \sum_{t=1}^{N} \mathbf 1\{\tau \ge t\}\,(M_t - M_{t-1}),$$
because the sum telescopes up to $\tau \wedge N$ and its later terms are 0. Each term is integrable. Since $\mathbf 1\{\tau \ge t\}$ is $\mathcal F_{t-1}$-measurable and bounded,
$$E\bigl[\mathbf 1\{\tau \ge t\}(M_t - M_{t-1})\bigr] = E\bigl[\mathbf 1\{\tau \ge t\}\bigl(E[M_t \mid \mathcal F_{t-1}] - M_{t-1}\bigr)\bigr] \le 0.$$
So $E[M_{\tau \wedge N}] \le E[M_0]$.

*Step 2: Markov's step.* On $\{\tau \le N\}$ we have $M_{\tau \wedge N} = M_\tau \ge a$, and everywhere $M_{\tau \wedge N} \ge 0$. Hence
$$a\,P(\tau \le N) \le E\bigl[M_{\tau \wedge N}\,\mathbf 1\{\tau \le N\}\bigr] \le E[M_{\tau \wedge N}] \le E[M_0].$$

*Step 3: let $N \to \infty$.* The events $\{\tau \le N\}$ increase with $N$ to $\{\tau < \infty\} = \{\exists t: M_t \ge a\}$. By continuity of $P$ from below, $P(\exists t: M_t \ge a) \le E[M_0]/a$.

*Step 4: from "some $M_t \ge a$" to "$\sup_t M_t \ge a$".* The supremum can equal $a$ without being attained. For every $a'$ with $0 < a' < a$, the event $\{\sup_t M_t \ge a\}$ is contained in $\{\exists t: M_t \ge a'\}$, so by Step 3 its probability is at most $E[M_0]/a'$. Letting $a' \uparrow a$ gives the bound $E[M_0]/a$. $\blacksquare$

Step 1 is the [optional stopping theorem](/optional-stopping-theorem/) for the bounded stopping time $\tau \wedge N$, written out. The proof never uses the distribution of the increments, only their conditional means and the sign of $M$.

## Consequences

- **Anytime-valid tests.** If $M$ is a test supermartingale for every distribution in a null $\mathcal H_0$, the rule "reject at the first $t$ with $M_t \ge 1/\alpha$" has type I error at most $\alpha$ under every $P \in \mathcal H_0$, for every stopping rule the analyst uses, including never stopping. The [mixture SPRT](/mixture-sequential-probability-ratio-test/) is this rule with a mixture likelihood ratio.
- **Anytime-valid p-values.** $p_t = \min(1, 1/\max_{s \le t} M_s)$ satisfies $P(\exists t: p_t \le \alpha) \le \alpha$, because $\{\exists t: p_t \le \alpha\} = \{\exists t: M_t \ge 1/\alpha\}$ for $\alpha \in (0, 1]$.
- **Confidence sequences.** If $M_t(\theta)$ is a test martingale when $\theta$ is the true parameter, the sets $C_t = \{\theta : M_t(\theta) < 1/\alpha\}$ contain the true $\theta$ at all times at once with probability at least $1 - \alpha$. See [confidence sequence](/confidence-sequence/).
- **Wald's bound for the SPRT.** In the [SPRT](/sequential-probability-ratio-test/) the likelihood ratio $L_n = \prod_{i \le n} f_1(X_i)/f_0(X_i)$ is a test martingale under $H_0$. Rejecting when $L_n \ge A$ therefore has type I error at most $1/A$, with no approximation.
- **Line-crossing bounds.** Let $S_t$ be a sum of i.i.d. $N(0, 1)$ variables. For $\lambda > 0$, $\exp(\lambda S_t - \lambda^2 t/2)$ is a test martingale. On the event that $S_t \ge a + bt$ for some $t$, with $a, b > 0$ and $\lambda = 2b$, the martingale is at least $\exp(2ab + 2b^2 t - 2b^2 t) = e^{2ab}$. So $P(\exists t: S_t \ge a + bt) \le e^{-2ab}$. The same argument with a sub-Gaussian or bounded increment gives the time-uniform versions of the [Hoeffding](/hoeffding-inequality/) and [Azuma](/azuma-inequality/) inequalities surveyed by Howard, Ramdas, McAuliffe and Sekhon (2020).
- **E-processes.** Fatou's lemma applied to Step 1 shows $E[M_\tau] \le E[M_0]$ for every stopping time $\tau$, so a test supermartingale is an e-process; see [test martingale](/test-martingale/).
- **Continuous time.** If $(M_t)_{t \ge 0}$, with real $t$, is a nonnegative supermartingale with right-continuous paths, apply the theorem to the times $\{k 2^{-j} : k \ge 0\}$ and let $j \to \infty$. Right continuity makes the supremum over these times equal to the supremum over all $t$, so the same bound holds.

## Tightness

The constant cannot be improved.

- **A two-point martingale.** Let $a \ge 1$, $M_0 = 1$, and let $M_t = a$ for all $t \ge 1$ with probability $1/a$ and $M_t = 0$ for all $t \ge 1$ otherwise. This is a nonnegative martingale and $P(\sup_t M_t \ge a) = 1/a = E[M_0]/a$.
- **Geometric Brownian motion.** Let $B$ be standard Brownian motion and $M_t = \exp(B_t - t/2)$, a continuous nonnegative martingale with $M_0 = 1$. For $a > 1$ let $\tau$ be the first time $M_t = a$. Up to $\tau$ the process stays in $[0, a]$, so optional stopping at $\tau \wedge T$ gives $E[M_{\tau \wedge T}] = 1$. As $T \to \infty$, $M_T \to 0$ on $\{\tau = \infty\}$ because $B_T - T/2 \to -\infty$, and dominated convergence gives $a\,P(\tau < \infty) = 1$. So equality holds with no overshoot. For Gaussian sums in discrete time the martingale jumps over the level, and the inequality is strict.
- **Nonnegativity is needed.** Let $M_t = 1 + S_t$ with $S_t$ a simple symmetric random walk. It is a martingale with $M_0 = 1$, but it takes negative values, and by recurrence it reaches every level $a$ with probability 1, far above $1/a$.
- **The supermartingale property is needed.** $M_t = \exp(\lambda S_t)$ for a Gaussian walk is nonnegative and starts at 1, but it is a submartingale, and it also reaches every level with probability 1 when $\lambda \ne 0$.
- **Fixed time against all times.** Markov's inequality at one fixed $t$ gives the same number $E[M_0]/a$ for $P(M_t \ge a)$. Ville's inequality says that the bound for all times at once costs nothing more. The price of uniformity is paid in power. At a planned sample size $n$, the rule "reject if $M_t \ge 1/\alpha$ for some $t \le n$" is a level-$\alpha$ test, so by the [Neyman-Pearson lemma](/neyman-pearson-lemma/) its power against a simple alternative is at most that of the most powerful fixed-sample test with $n$ observations.

## History

Jean Ville proved the inequality for nonnegative martingales in his 1939 thesis, Étude critique de la notion de collectif, where he used martingales, a word he brought into probability, to criticize von Mises's definition of randomness; Shafer, Shen, Vereshchagin and Vovk (2011) tell this history and name the inequality after him. The statement is the special case for nonnegative supermartingales of Doob's maximal inequality, in the form found in textbooks such as Durrett, Section 4.4. Its use as the basis of anytime-valid inference, test martingales and time-uniform concentration bounds is surveyed by Howard, Ramdas, McAuliffe and Sekhon (2020) and Ramdas, Grünwald, Vovk and Shafer (2023).

## References
