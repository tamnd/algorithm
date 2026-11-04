---
tag: G97WCH
kind: theorem
slug: azuma-inequality
name: Azuma-Hoeffding inequality
aliases:
- Azuma's inequality
area: foundations/probabilistic-analysis
level: advanced
summary: A martingale whose steps are bounded by c_1, ..., c_n deviates from its start by t or more with probability at most 2 exp(-t^2 / (2 sum c_k^2)).
prereqs: [martingale, hoeffding-inequality, moment-generating-function, markov-inequality, conditional-expectation]
see_also: [concentration-of-measure, chernoff-bound, chebyshev-inequality, balls-into-bins, chromatic-number, erdos-renyi-model, optional-stopping-theorem, high-probability-bounds]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 13, Section 13.4, Tail Inequalities for Martingales, and Section 13.5, Applications of the Azuma-Hoeffding Inequality (13.5.1 general formalization, 13.5.2 pattern matching, 13.5.3 balls and bins, 13.5.4 chromatic number)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 7, Martingales and Tight Concentration (Section 7.2, Large Deviations; Section 7.3, Chromatic Number)
  - book: isbn:9780521884273
    title: Devdatt P. Dubhashi and Alessandro Panconesi, Concentration of Measure for the Analysis of Randomized Algorithms, Cambridge University Press, 2009
    locator: Chapter 5, Martingales and the Method of Bounded Differences (Section 5.2, Martingales and Azuma's Inequality; Section 5.4, The Method of Bounded Differences)
  - paper: doi:10.2748/tmj/1178243286
    title: Kazuoki Azuma, Weighted sums of certain dependent random variables, Tohoku Mathematical Journal 19(3), 1967
    locator: the inequality for sums of bounded martingale differences
  - paper: doi:10.1080/01621459.1963.10500830
    title: Wassily Hoeffding, Probability inequalities for sums of bounded random variables, Journal of the American Statistical Association 58(301), 1963
    locator: the lemma on the moment generating function of a bounded variable, and the remark that the inequalities extend to martingales
  - paper: "Colin McDiarmid, On the method of bounded differences, in Surveys in Combinatorics 1989, London Mathematical Society Lecture Note Series 141, Cambridge University Press, 1989"
    locator: the bounded differences inequality with the constant 2 in the exponent
  - paper: doi:10.1007/BF02579208
    title: Eli Shamir and Joel Spencer, Sharp concentration of the chromatic number on random graphs G(n,p), Combinatorica 7(1), 1987
    locator: the vertex exposure martingale for the chromatic number
---

The Azuma-Hoeffding inequality bounds the probability that a [martingale](/martingale/) moves far from its starting value: if each step changes the value by at most $c_k$, the value after $n$ steps differs from the start by $t$ or more with probability at most $2\exp(-t^2/(2\sum c_k^2))$. It extends [Hoeffding's inequality](/hoeffding-inequality/) from sums of [independent](/independent-random-variables/) terms to sums of dependent steps. Its main corollary, the method of bounded differences of McDiarmid, gives tail bounds for any function of independent random choices that changes little when one choice changes, such as the number of empty bins in [balls into bins](/balls-into-bins/) or the [chromatic number](/chromatic-number/) of a random graph.

## Statement

Let $X_0, X_1, \ldots, X_n$ be a martingale with respect to a filtration $\mathcal F_0 \subseteq \cdots \subseteq \mathcal F_n$, and let $D_k = X_k - X_{k-1}$ for $k = 1, \ldots, n$.

**(a) Azuma's inequality.** If there are constants $c_1, \ldots, c_n \ge 0$, not all 0, with $|D_k| \le c_k$ almost surely, then for each $t > 0$
$$ \Pr(X_n - X_0 \ge t) \le \exp\!\left(-\frac{t^2}{2\sum_{k=1}^n c_k^2}\right), \qquad \Pr(|X_n - X_0| \ge t) \le 2\exp\!\left(-\frac{t^2}{2\sum_{k=1}^n c_k^2}\right). $$
The same bound holds for $\Pr(X_n - X_0 \le -t)$.

**(b) Predictable intervals.** If there are $\mathcal F_{k-1}$-measurable random variables $A_k \le B_k$ and constants $d_k \ge 0$, not all 0, with $A_k \le D_k \le B_k$ and $B_k - A_k \le d_k$ almost surely, then for each $t > 0$
$$ \Pr(X_n - X_0 \ge t) \le \exp\!\left(-\frac{2t^2}{\sum_{k=1}^n d_k^2}\right), $$
and the same bound holds for $\Pr(X_n - X_0 \le -t)$.

**(c) Method of bounded differences (McDiarmid's inequality).** Let $Z_1, \ldots, Z_n$ be independent random variables, $Z_i$ with values in a finite or countable set $S_i$, and let $f : S_1 \times \cdots \times S_n \to \mathbb R$ satisfy the *bounded differences condition*: $|f(z) - f(z')| \le c_i$ whenever $z$ and $z'$ differ only in coordinate $i$, with constants $c_i \ge 0$ not all 0. Then $f(Z) = f(Z_1, \ldots, Z_n)$ is integrable, and for each $t > 0$
$$ \Pr\big(f(Z) - \mathbb E f(Z) \ge t\big) \le \exp\!\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right), \qquad \Pr\big(|f(Z) - \mathbb E f(Z)| \ge t\big) \le 2\exp\!\left(-\frac{2t^2}{\sum_{i=1}^n c_i^2}\right). $$
McDiarmid proved (c) for general product spaces. The countable case below covers the examples on this page, and the proof is the same up to measurability.

Form (a) is the special case $A_k = -c_k$, $B_k = c_k$, $d_k = 2c_k$ of form (b). Applying (a) instead of (b) to the setting of (c) gives the weaker exponent $t^2/(2\sum c_i^2)$, a factor 4 smaller.

## In plain words

A process moves in steps. Each step may depend on all the earlier ones, but given the past, each step is zero on average, and each step has a known largest size. The theorem says that after many steps the process is very unlikely to be far from where it started. The chance of a distance a few times the square root of the sum of the squared step sizes falls off like the bell curve.

The most used form is about a function of many independent random choices. If changing any single choice changes the function only a little, then the function is almost always close to its average. One does not need to know the average. This is why the theorem shows that the number of colors that a random graph needs is almost fixed, although nobody knows that number.

## Proof

The proof is the moment generating function method of the [Chernoff bound](/chernoff-bound/), with one change: the factorization of the expectation of a product of independent factors is replaced by conditioning on the past, one step at a time. We prove (b) first, then derive (a) and (c).

**Step 1 (Hoeffding's lemma, the form used).** For real numbers $a \le 0 \le b$ with $a < b$, and each real $\lambda$,
$$ \frac{b\,e^{\lambda a} - a\,e^{\lambda b}}{b - a} \le \exp\!\left(\frac{\lambda^2 (b - a)^2}{8}\right). $$
This is Hoeffding's lemma, proved on the page of [Hoeffding's inequality](/hoeffding-inequality/): a random variable $Y$ with $\mathbb E Y = 0$ and $a \le Y \le b$ has $\mathbb E[e^{\lambda Y}] \le e^{\lambda^2(b-a)^2/8}$. Apply it to the variable $Y$ that takes the value $a$ with probability $b/(b - a)$ and the value $b$ with probability $-a/(b - a)$. These probabilities are in $[0, 1]$ and sum to 1, $\mathbb E Y = (ab - ab)/(b - a) = 0$, and $\mathbb E[e^{\lambda Y}]$ is the left side.

**Step 2 (the conditional lemma).** Let $\mathcal G$ be a $\sigma$-algebra, let $Y$ be a random variable with $\mathbb E[Y \mid \mathcal G] = 0$, and let $A \le Y \le B$ where $A$ and $B$ are $\mathcal G$-measurable and $B - A \le d$ for a constant $d$. Then for each real $\lambda$, almost surely,
$$ \mathbb E[e^{\lambda Y} \mid \mathcal G] \le e^{\lambda^2 d^2/8}. $$

*Proof.* First, $Y - d \le B - d \le A \le Y$ and $Y \le B \le A + d \le Y + d$, so $A$ and $B$ are integrable because $Y$ is. Next, $A \le 0 \le B$ almost surely: $A = \mathbb E[A \mid \mathcal G] \le \mathbb E[Y \mid \mathcal G] = 0$, and in the same way $B \ge 0$. So $|Y| \le B - A \le d$, and $e^{\lambda Y}$ is bounded. Let $H = \{A < B\}$, an event in $\mathcal G$. On the complement of $H$, $Y = A$, so $Y 1_{H^c} = A 1_{H^c}$ is $\mathcal G$-measurable and equals $\mathbb E[Y 1_{H^c} \mid \mathcal G] = 1_{H^c}\mathbb E[Y \mid \mathcal G] = 0$. So $Y = 0$ on $H^c$, and there $\mathbb E[e^{\lambda Y} \mid \mathcal G] = 1 \le e^{\lambda^2 d^2/8}$. On $H$, the function $y \mapsto e^{\lambda y}$ is convex, so on the interval $[A, B]$ it lies below its chord:
$$ e^{\lambda Y} \le \frac{B - Y}{B - A}\,e^{\lambda A} + \frac{Y - A}{B - A}\,e^{\lambda B}. $$
The coefficients $\frac{1}{B-A}$, $A$, $B$, $e^{\lambda A}$ and $e^{\lambda B}$ are $\mathcal G$-measurable, so they come out of the conditional expectation, and $\mathbb E[Y \mid \mathcal G] = 0$ gives, on $H$,
$$ \mathbb E[e^{\lambda Y} \mid \mathcal G] \le \frac{B\,e^{\lambda A} - A\,e^{\lambda B}}{B - A} \le \exp\!\left(\frac{\lambda^2 (B - A)^2}{8}\right) \le e^{\lambda^2 d^2/8}, $$
by Step 1 with $a = A$, $b = B$, and then by $B - A \le d$. $\square$

**Step 3 (chaining with the tower property).** Let $W_k = X_k - X_0 = D_1 + \cdots + D_k$, and $V = \sum_{k=1}^n d_k^2$. By the first lines of the proof of Step 2, $|D_k| \le d_k$, so $W_k$ is bounded and all expectations below are finite. $W_{k-1}$ is $\mathcal F_{k-1}$-measurable, and the martingale property gives $\mathbb E[D_k \mid \mathcal F_{k-1}] = 0$. So by the tower property and Step 2 with $\mathcal G = \mathcal F_{k-1}$, $Y = D_k$, $A = A_k$, $B = B_k$, $d = d_k$,
$$ \mathbb E[e^{\lambda W_k}] = \mathbb E\big[e^{\lambda W_{k-1}}\,\mathbb E[e^{\lambda D_k} \mid \mathcal F_{k-1}]\big] \le e^{\lambda^2 d_k^2/8}\,\mathbb E[e^{\lambda W_{k-1}}]. $$
With $W_0 = 0$, induction on $k$ gives $\mathbb E[e^{\lambda W_n}] \le e^{\lambda^2 V/8}$ for each real $\lambda$.

**Step 4 (Markov's inequality and the choice of $\lambda$).** For $\lambda > 0$, [Markov's inequality](/markov-inequality/) applied to the positive variable $e^{\lambda W_n}$ gives
$$ \Pr(W_n \ge t) = \Pr(e^{\lambda W_n} \ge e^{\lambda t}) \le e^{-\lambda t}\,\mathbb E[e^{\lambda W_n}] \le \exp\!\left(-\lambda t + \frac{\lambda^2 V}{8}\right). $$
The exponent is smallest at $\lambda = 4t/V > 0$, where it equals $-2t^2/V$. This proves the upper tail of (b). For the lower tail, $-X_0, \ldots, -X_n$ is a martingale with differences in $[-B_k, -A_k]$, an interval of the same width, so $\Pr(X_n - X_0 \le -t) \le e^{-2t^2/V}$ as well.

**Step 5 (form (a)).** If $|D_k| \le c_k$, take $A_k = -c_k$, $B_k = c_k$ and $d_k = 2c_k$ in (b). Then $V = 4\sum c_k^2$ and $2t^2/V = t^2/(2\sum c_k^2)$. The two-sided bound is the [union bound](/union-bound/) over the two tails.

**Step 6 (form (c), through the Doob martingale).** Fix $z^0 \in S_1 \times \cdots \times S_n$. Changing the coordinates of $z$ one at a time into those of $z^0$ gives $|f(z) - f(z^0)| \le \sum_i c_i$, so $f$ is bounded and $f(Z)$ is integrable. Let $\mathcal F_k = \sigma(Z_1, \ldots, Z_k)$ and let $Y_k = \mathbb E[f(Z) \mid \mathcal F_k]$, the Doob martingale, with $Y_0 = \mathbb E f(Z)$ and $Y_n = f(Z)$. Because the $Z_i$ are independent and take countably many values,
$$ Y_k = g_k(Z_1, \ldots, Z_k), \qquad g_k(z_1, \ldots, z_k) = \mathbb E\big[f(z_1, \ldots, z_k, Z_{k+1}, \ldots, Z_n)\big]. $$
Fix a prefix $z_1, \ldots, z_{k-1}$, and let $u(z) = g_k(z_1, \ldots, z_{k-1}, z)$ for $z \in S_k$. Since $Z_k$ is independent of $Z_1, \ldots, Z_{k-1}$, the value of $Y_{k-1}$ on this prefix is $g_{k-1}(z_1, \ldots, z_{k-1}) = \sum_z \Pr(Z_k = z)\,u(z)$, and $D_k = u(Z_k) - Y_{k-1}$. Let $A_k = \inf_z u(z) - Y_{k-1}$ and $B_k = \sup_z u(z) - Y_{k-1}$. Both are functions of $Z_1, \ldots, Z_{k-1}$, so they are $\mathcal F_{k-1}$-measurable, and $A_k \le D_k \le B_k$. For any $z, z' \in S_k$, the bounded differences condition in coordinate $k$ gives
$$ u(z) - u(z') = \mathbb E\big[f(z_1, \ldots, z_{k-1}, z, Z_{k+1}, \ldots, Z_n) - f(z_1, \ldots, z_{k-1}, z', Z_{k+1}, \ldots, Z_n)\big] \le c_k, $$
so $B_k - A_k = \sup u - \inf u \le c_k$. Form (b) with $d_k = c_k$ gives (c), and the union bound gives the two-sided form. $\square$

## Consequences

**Hoeffding's inequality.** If $X_n = \sum_{i \le n} (Y_i - \mathbb E Y_i)$ for independent $Y_i \in [a_i, b_i]$, then $X_n$ is a martingale with differences in intervals of width $b_i - a_i$, and (b) is [Hoeffding's inequality](/hoeffding-inequality/). So Azuma's inequality loses nothing against Hoeffding's inequality in the independent case, and it keeps the same bound when the steps depend on each other.

**The simple random walk, bound against exact.** Let $S_n$ be the sum of $n$ independent signs $\pm 1$, each with probability $\frac12$. It is a martingale with $|D_k| \le 1$, so (a) gives $\Pr(S_n \ge t) \le e^{-t^2/(2n)}$. The exact tail is $\Pr(S_n \ge t) = 2^{-n}\sum_{j \ge (n+t)/2}\binom nj$.

| $n$ | $t$ | exact $\Pr(S_n \ge t)$ | Azuma $e^{-t^2/(2n)}$ | bound / exact |
| --- | --- | --- | --- | --- |
| 100 | 10 | 0.1841 | 0.6065 | 3.3 |
| 100 | 20 | 0.02844 | 0.1353 | 4.8 |
| 100 | 30 | 0.001759 | 0.01111 | 6.3 |
| 100 | 40 | $3.925 \times 10^{-5}$ | $3.355 \times 10^{-4}$ | 8.5 |
| 1000 | 100 | $8.653 \times 10^{-4}$ | 0.006738 | 7.8 |
| 1000 | 150 | $1.178 \times 10^{-6}$ | $1.301 \times 10^{-5}$ | 11.0 |
| 1000 | 200 | $1.364 \times 10^{-10}$ | $2.061 \times 10^{-9}$ | 15.1 |

The bound has the right exponent and loses a factor that grows slowly with $t/\sqrt n$. The Tightness section explains the factor.

**Empty bins.** Throw $m$ balls independently and uniformly into $n$ bins, and let $f$ be the number of empty bins. Let $Z_i$ be the bin of ball $i$. Moving one ball empties at most one bin and fills at most one, so $f$ has bounded differences with $c_i = 1$, and (c) gives $\Pr(|f - \mathbb E f| \ge t) \le 2e^{-2t^2/m}$, with $\mathbb E f = n(1 - 1/n)^m$. For $n = m = 100$, $\mathbb E f = 36.60$ and $\operatorname{Var} f = 9.740$. The exact tail comes from the exact distribution $\Pr(f = j) = \binom nj\,\mathrm{Surj}(m, n - j)/n^m$, where $\mathrm{Surj}(m, k)$ counts the maps from $m$ balls onto $k$ bins.

| $t$ | exact $\Pr(\lvert f - \mathbb E f\rvert \ge t)$ | McDiarmid $2e^{-2t^2/m}$ | Azuma form (a), $2e^{-t^2/(2m)}$ | [Chebyshev](/chebyshev-inequality/) $\operatorname{Var} f/t^2$ |
| --- | --- | --- | --- | --- |
| 5 | 0.1079 | 1.213 | 1.765 | 0.3896 |
| 8 | 0.009974 | 0.5561 | 1.452 | 0.1522 |
| 10 | 0.001258 | 0.2707 | 1.213 | 0.09740 |
| 15 | $1.175 \times 10^{-6}$ | 0.02222 | 0.6493 | 0.04329 |
| 20 | $7.426 \times 10^{-11}$ | $6.709 \times 10^{-4}$ | 0.2707 | 0.02435 |

At this size Chebyshev's inequality, which uses the true variance, wins up to $t = 15$. The bounded differences bound behaves as if the standard deviation were $\sqrt m/2 = 5$, while the true one is $3.12$. Its advantage is the exponential decay for large $t$, and that it needs no variance computation.

**Pattern matching.** Let $Z_1, \ldots, Z_n$ be independent letters, uniform over an alphabet of $s$ letters, and let $f$ count the positions where a fixed pattern of length $k$ occurs ([string matching](/string-matching/)). Then $\mathbb E f = (n - k + 1)s^{-k}$. A letter lies in at most $k$ windows, so $c_i = k$, and (c) gives $\Pr(|f - \mathbb E f| \ge t) \le 2e^{-2t^2/(nk^2)}$. For a DNA string with $n = 10^6$, $s = 4$ and a pattern of length $k = 2$ such as AC, $\mathbb E f = 62499.94$, and $f$ is within $3255$ of the mean with probability at least $0.99$ (the value of $t$ where the bound equals $0.01$ is $k\sqrt{n\ln 200/2}$). The true standard deviation is $225.3$. For $k = 8$ the mean is $15.26$ and the bound allows a deviation of $13021$, which says nothing. The bounded differences condition charges each letter the worst case $k$, although a change of one letter almost never changes the count.

**Chromatic number.** Let $G$ be a random graph $G(n, p)$ ([Erdős-Rényi model](/erdos-renyi-model/)). For $i = 2, \ldots, n$, let $Z_i$ be the set of edges from vertex $i$ to the vertices $1, \ldots, i - 1$. The $Z_i$ are independent and determine $G$. If two graphs $G$ and $G'$ differ only in the edges at vertex $i$, then $\chi(G) \le \chi(G - i) + 1 \le \chi(G') + 1$: color $G - i$ as in an optimal coloring of $G'$ and give $i$ a new color. So $c_i = 1$ for $n - 1$ coordinates, and (c) gives
$$ \Pr\big(|\chi(G) - \mathbb E\chi(G)| \ge t\big) \le 2e^{-2t^2/(n-1)}. $$
For $n = 1000$, $\chi(G)$ is within $51.4$ of its mean with probability at least $0.99$, for each $p$, although the bound says nothing about the mean itself. Form (a) gives the window $102.9$. This is the vertex exposure argument of Shamir and Spencer, see also [martingale](/martingale/).

### Pitfalls

- **The bound on a step must hold always.** The constants $c_k$ bound every step on every path, not the typical step. For the number of triangles in $G(n, p)$, one vertex can be in $\binom{n-1}{2}$ triangles, and the bound becomes weak. Refinements that use averaged differences are in Dubhashi and Panconesi, Chapter 7.
- **The order of exposure matters.** For the chromatic number, the edge exposure martingale also has steps at most 1, but it has $\binom n2$ steps instead of $n - 1$. For $n = 1000$ this gives the window $1150.3$ instead of $51.4$, which is useless.
- **Half-width or full width.** With $|D_k| \le c_k$ the exponent is $t^2/(2\sum c_k^2)$. With $D_k$ in an interval of width $c_k$ it is $2t^2/\sum c_k^2$. Mixing the two forms gives a bound that is wrong by a factor 4 in the exponent.
- **The variance is ignored.** The bound depends only on the ranges. When the true variance is much smaller than $\sum c_k^2$, as for empty bins at moderate $t$, or for a sum of rare events where the [Chernoff bound](/chernoff-bound/) uses the small mean, other bounds win.
- **The center is the mean, or $X_0$.** The bound is about the deviation from $X_0 = \mathbb E f$. It does not say that $f$ is close to an estimate of the mean, unless the estimate is itself proved.
- **A martingale is needed for both tails.** For a supermartingale the upper tail keeps the bound: write $D_k = D'_k + m_k$ with $m_k = \mathbb E[D_k \mid \mathcal F_{k-1}] \le 0$. For $\lambda > 0$, $e^{\lambda D_k} \le e^{\lambda D'_k}$, and $D'_k$ has conditional mean 0 and lies in an interval of the same width, so Steps 2 to 4 go through. The lower tail fails: the process $X_k = -k$ is a supermartingale with $|D_k| \le 1$, and $\Pr(X_n - X_0 \le -n) = 1$.

## Tightness

**The constant in the exponent is best possible.** Take the simple random walk, with $c_k = 1$. By the [central limit theorem](/central-limit-theorem/), $\Pr(S_n \ge x\sqrt n) \to 1 - \Phi(x)$ for each fixed $x > 0$, and $1 - \Phi(x) \ge \frac{x}{1 + x^2}\cdot\frac{e^{-x^2/2}}{\sqrt{2\pi}}$. If a bound $\Pr(X_n - X_0 \ge t) \le \exp(-\gamma t^2/\sum c_k^2)$ held for all martingales with some $\gamma > \frac12$, then $1 - \Phi(x) \le e^{-\gamma x^2}$ for every $x > 0$, which fails for large $x$ because $\frac{x}{1+x^2}e^{-x^2/2}$ decreases more slowly than $e^{-\gamma x^2}$. In the same way, the number of heads in $n$ fair coin tosses has $c_i = 1$ and variance $n/4$, so its normal approximation has the tail exponent $2t^2/n$, and the constant 2 of form (c) is also best possible.

**The lost factor.** For $t = x\sqrt n$ the bound $e^{-x^2/2}$ exceeds the normal tail by a factor of about $x\sqrt{2\pi}$, a factor that is not exponential. For $n = 1000$ and $t = 200$, $x = 6.32$ and $x\sqrt{2\pi} = 15.9$, close to the ratio $15.1$ in the table.

**Where the bound is weak.** The examples of empty bins and pattern matching show that the bound can be far from the truth when the variance is much smaller than $\sum c_k^2$. Martingale inequalities of Bernstein type, which use the conditional variances of the steps, and the averaged and variance methods of Dubhashi and Panconesi, Chapters 7 and 8, give sharper results there.

## History

Hoeffding proved his inequality for sums of independent bounded variables in 1963, and in the same paper he remarked that the inequalities stay true for martingale differences. Azuma stated and proved the martingale form in 1967, which is why the result has both names. Shamir and Spencer used the vertex exposure martingale in 1987 to prove that the chromatic number of $G(n, p)$ is concentrated in a window of width $O(\sqrt n)$. McDiarmid's survey of 1989, On the method of bounded differences, developed the method with the constant 2 of form (c). Alon and Spencer, Chapter 7, and Mitzenmacher and Upfal, Sections 13.4 and 13.5, present the inequality with the applications on this page.

## References
