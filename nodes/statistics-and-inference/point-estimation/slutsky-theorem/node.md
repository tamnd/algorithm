---
tag: 1WWME7
kind: theorem
slug: slutsky-theorem
name: Slutsky's theorem
aliases:
- Slutsky lemma
area: statistics-and-inference/point-estimation
level: core
summary: If X_n converges in distribution to X and Y_n converges in probability to a constant c, then X_n + Y_n and X_n Y_n converge in distribution to X + c and cX.
prereqs: [consistent-estimator, central-limit-theorem, random-variable]
see_also: [delta-method, asymptotic-normality-of-mle, student-t-test, z-test, wald-test, law-of-large-numbers, standard-error, m-estimator]
sources:
  - paper: "E. Slutsky, Über stochastische Asymptoten und Grenzwerte, Metron 5(3), 1925"
    locator: pages 3 to 89 (convergence in probability, stochastic limits, and limits of sums and products)
  - book: isbn:9780534243128
    title: George Casella and Roger L. Berger, Statistical Inference, second edition, Duxbury, 2002
    locator: Section 5.5.4, Theorem 5.5.17 (Slutsky's theorem) and Example 5.5.18 (the studentized mean)
  - book: isbn:9780521496032
    title: A. W. van der Vaart, Asymptotic Statistics, Cambridge University Press, 1998
    locator: Chapter 2, Section 2.1 (the portmanteau lemma, the continuous mapping theorem and Slutsky's lemma in vector form)
  - book: isbn:9780691005478
    title: Harald Cramér, Mathematical Methods of Statistics, Princeton University Press, 1946
    locator: Chapter 20, Section 20.6 (convergence of functions of random variables that converge in probability to constants)
---

Slutsky's theorem says that a sequence that converges in distribution keeps its limit when you add to it, or multiply it by, a sequence that converges in probability to a constant. It is the step that lets you replace an unknown nuisance quantity, such as $\sigma$, by a [consistent estimator](/consistent-estimator/) of it, such as $S$, without changing the limit law. With the [central limit theorem](/central-limit-theorem/) it gives the asymptotic normal law of the studentized mean, of [Wald statistics](/wald-test/), of the [delta method](/delta-method/) and of the [maximum likelihood estimator](/asymptotic-normality-of-mle/).

## Statement

All random variables are real and defined on one probability space for each $n$. Write $X_n \xrightarrow{d} X$ for convergence in distribution ($P(X_n \le t) \to P(X \le t)$ at each $t$ where the distribution function of $X$ is continuous) and $Y_n \xrightarrow{p} c$ for convergence in probability ($P(|Y_n - c| > \varepsilon) \to 0$ for each $\varepsilon > 0$).

**Theorem (Slutsky).** Assume:

1. $X_n \xrightarrow{d} X$ for some random variable $X$;
2. $Y_n \xrightarrow{p} c$, where $c$ is a constant (not a random variable).

Then, as $n \to \infty$,

- (a) $X_n + Y_n \xrightarrow{d} X + c$;
- (b) $Y_n X_n \xrightarrow{d} cX$;
- (c) if $c \ne 0$, then $X_n / Y_n \xrightarrow{d} X/c$. The ratio is defined in any way on the event $\{Y_n = 0\}$, whose probability tends to 0.

**Vector form.** If $X_n \xrightarrow{d} X$ in $\mathbb R^k$ and $Y_n \xrightarrow{p} c$ in $\mathbb R^m$ with $c$ constant, then the pair $(X_n, Y_n)$ converges in distribution to $(X, c)$ in $\mathbb R^{k+m}$. By the continuous mapping theorem, $g(X_n, Y_n) \xrightarrow{d} g(X, c)$ for each function $g$ that is continuous at every point of a set $C$ with $P((X, c) \in C) = 1$. For example $A_n X_n \xrightarrow{d} A X$ when the random matrices $A_n$ converge in probability to a constant matrix $A$, and $A_n^{-1} X_n \xrightarrow{d} A^{-1} X$ when $A$ is invertible. This form is in van der Vaart, Section 2.1.

## In plain words

Suppose one sequence of random numbers settles down to a fixed bell-shaped spread, and a second sequence settles down to one fixed number. Then their sum settles down to the same spread, moved by that number, and their product settles down to the same spread, stretched by that number.

The rule is used all the time in statistics. The spread of an average depends on a true spread that you do not know. You divide by an estimate of it instead. The estimate settles down to the true value, so the rule says that the answer has the same limit as if you knew the truth.

The second sequence must settle down to one fixed number. If it only settles to a spread of its own, the rule can fail.

## Proof

Let $F$ be the distribution function of $X$ and $F_n$ that of $X_n$. The points where $F$ is not continuous form a countable set, so the continuity points of $F$ are dense in $\mathbb R$.

**Step 1: part (a).** Let $t$ be a point with $t - c$ a continuity point of $F$; these are exactly the continuity points of the distribution function of $X + c$. Take $\varepsilon > 0$ with $t - c - \varepsilon$ and $t - c + \varepsilon$ continuity points of $F$. If $X_n + Y_n \le t$ and $|Y_n - c| \le \varepsilon$, then $X_n \le t - c + \varepsilon$. If $X_n \le t - c - \varepsilon$ and $|Y_n - c| \le \varepsilon$, then $X_n + Y_n \le t$. So

$$F_n(t - c - \varepsilon) - P(|Y_n - c| > \varepsilon) \le P(X_n + Y_n \le t) \le F_n(t - c + \varepsilon) + P(|Y_n - c| > \varepsilon).$$

Let $n \to \infty$. By hypothesis 2 the probability terms tend to 0, and by hypothesis 1 the two values of $F_n$ tend to $F(t - c \mp \varepsilon)$. So every limit point of $P(X_n + Y_n \le t)$ lies in $[F(t - c - \varepsilon), F(t - c + \varepsilon)]$. Let $\varepsilon \downarrow 0$ through continuity points. Since $F$ is continuous at $t - c$, the interval shrinks to the point $F(t - c) = P(X + c \le t)$. This proves (a).

**Step 2: $X_n$ is bounded in probability.** Fix $\eta > 0$. Choose $M > 0$ with $-M$ and $M$ continuity points of $F$ and $F(-M) + 1 - F(M) < \eta$. Then $P(|X_n| > M) \le F_n(-M) + 1 - F_n(M)$, which tends to $F(-M) + 1 - F(M) < \eta$. So $P(|X_n| > M) < \eta$ for all large $n$.

**Step 3: $c X_n \xrightarrow{d} c X$.** If $c = 0$, both sides are the constant 0. If $c > 0$, then $P(c X_n \le t) = F_n(t/c) \to F(t/c) = P(cX \le t)$ at each continuity point. If $c < 0$, let $s = t/c$ be a continuity point of $F$. Then $P(c X_n \le t) = 1 - P(X_n < s)$, and $F_n(s - \delta) \le P(X_n < s) \le F_n(s)$ for each $\delta > 0$. With $s - \delta$ a continuity point, the limit points of $P(X_n < s)$ lie in $[F(s - \delta), F(s)]$, and $\delta \downarrow 0$ gives the limit $F(s) = P(X \le s) = P(X < s)$. So $P(cX_n \le t) \to P(cX \le t)$.

**Step 4: part (b).** Write $Y_n X_n = c X_n + R_n$ with $R_n = (Y_n - c) X_n$. For $\delta > 0$ and $\eta > 0$, take $M$ from Step 2. Then $P(|R_n| > \delta) \le P(|X_n| > M) + P(|Y_n - c| > \delta/M)$, which is less than $2\eta$ for all large $n$. So $R_n \xrightarrow{p} 0$. Step 3 and part (a), applied to $c X_n$ and $R_n$ with the constant 0, give $Y_n X_n \xrightarrow{d} cX$.

**Step 5: part (c).** Let $c \ne 0$. On the event $|Y_n - c| < |c|/2$ we have $|Y_n| > |c|/2$, so $Y_n \ne 0$ and $|1/Y_n - 1/c| = |Y_n - c|/(|Y_n|\,|c|) \le 2|Y_n - c|/c^2$. Hence $P(|1/Y_n - 1/c| > \varepsilon) \le P(|Y_n - c| \ge |c|/2) + P(|Y_n - c| > \varepsilon c^2/2) \to 0$, so $1/Y_n \xrightarrow{p} 1/c$. The value on $\{Y_n = 0\}$ does not matter, because that event lies inside $\{|Y_n - c| \ge |c|/2\}$. Part (b) with $1/Y_n$ in place of $Y_n$ gives $X_n / Y_n \xrightarrow{d} X/c$. $\blacksquare$

For the vector form, the same idea works with bounded Lipschitz test functions $f$ on $\mathbb R^{k+m}$: $|\mathrm E f(X_n, Y_n) - \mathrm E f(X_n, c)| \le \mathrm E \min(L\|Y_n - c\|, 2\sup|f|) \to 0$, and $\mathrm E f(X_n, c) \to \mathrm E f(X, c)$. By the portmanteau lemma this is convergence in distribution of the pair (van der Vaart, Section 2.1).

## Consequences

**The studentized mean.** Let $X_1, \ldots, X_n$ be iid with mean $\mu$ and variance $0 < \sigma^2 < \infty$, with [sample variance](/sample-variance/) $S^2$ (divisor $n - 1$). The [central limit theorem](/central-limit-theorem/) gives $\sqrt n(\bar X - \mu)/\sigma \xrightarrow{d} N(0, 1)$. The [law of large numbers](/law-of-large-numbers/) gives $S^2 \xrightarrow{p} \sigma^2$, so $\sigma/S \xrightarrow{p} 1$ by continuity of $u \mapsto \sigma/\sqrt u$ at $\sigma^2$. Part (b) gives

$$T_n = \frac{\sqrt n(\bar X - \mu)}{S} = \frac{\sqrt n(\bar X - \mu)}{\sigma}\cdot\frac{\sigma}{S} \xrightarrow{d} N(0, 1).$$

So the [t-test](/student-t-test/) and the [t interval](/t-confidence-interval/) have asymptotic level $\alpha$ for any distribution with finite variance. They are exact only for normal data. The theorem says nothing about the error at a fixed $n$. The table gives the size of the two-sided t-test at nominal level $\alpha = 0.05$ for Exp(1) data, measured by simulation with $r = 20000$ samples for each $n$ (Python `random.Random(1)`; the Monte Carlo standard error is about 0.0016). The data are skewed to the right, so $T_n$ is skewed to the left, and most rejections fall in the lower tail.

| $n$ | size | rejections below $-t_{(n-1, 0.975)}$ | rejections above $t_{(n-1, 0.975)}$ |
|---|---|---|---|
| 10 | 0.098 | 0.094 | 0.004 |
| 30 | 0.072 | 0.065 | 0.007 |
| 100 | 0.059 | 0.047 | 0.012 |
| 300 | 0.051 | 0.036 | 0.015 |

The total size approaches 0.05, but even at $n = 300$ the two tails are far from 0.025 each.

**Plug-in standard errors.** If $\sqrt n(\hat\theta_n - \theta) \xrightarrow{d} N(0, v(\theta))$ and $\hat v_n \xrightarrow{p} v(\theta) > 0$, then $(\hat\theta_n - \theta)/\sqrt{\hat v_n/n} \xrightarrow{d} N(0, 1)$. This is the basis of every Wald interval $\hat\theta_n \pm z_{1-\alpha/2}\,\widehat{\mathrm{se}}$, with a [standard error](/standard-error/) estimated from the data, and of the [Wald test](/wald-test/) and [z-test](/z-test/) with an estimated variance.

**Asymptotic arguments.** The proof of the [delta method](/delta-method/) uses part (b) on the remainder of a Taylor expansion. The proof of the [asymptotic normality of the MLE](/asymptotic-normality-of-mle/) and the sandwich formula of [M-estimators](/m-estimator/) use the vector form with $A_n^{-1} X_n$, where $A_n$ is the observed information or the mean Jacobian.

## Tightness

**The limit of $Y_n$ must be a constant.** Let $Z \sim N(0, 1)$ and put $X_n = Z$ and $Y_n = -Z$ for all $n$. Then $X_n \xrightarrow{d} N(0, 1)$ and $Y_n \xrightarrow{d} N(0, 1)$, but $X_n + Y_n = 0$, not $N(0, 2)$. Convergence in distribution of each sequence alone does not fix the joint law, so it says nothing about the sum.

**Convergence in probability to a random limit is not enough either.** Put $X_n = (-1)^n Z$ and $Y_n = Z$. Then $X_n \xrightarrow{d} N(0, 1)$ because $-Z$ has the same law as $Z$, and $Y_n \xrightarrow{p} Z$. But $X_n + Y_n$ is $2Z$ for even $n$ and $0$ for odd $n$, so it has no limit in distribution. The constant limit $c$ in hypothesis 2 is what removes the dependence between the two sequences in the limit.

**Part (c) needs $c \ne 0$.** If $X_n = Z$ and $Y_n = 1/n$, then $Y_n \xrightarrow{p} 0$ and $X_n / Y_n = nZ$ has no limit in distribution.

## History

Eugen Slutsky studied convergence in probability, which he called stochastic convergence, and the limits of functions of such sequences in a long paper in Metron in 1925. Harald Cramér gave the results for sums, products and quotients in his book Mathematical Methods of Statistics (1946), and some texts call the theorem Cramér's theorem for that reason. Casella and Berger state it as Theorem 5.5.17, and van der Vaart gives the vector form and its proof by the portmanteau lemma.

## References
