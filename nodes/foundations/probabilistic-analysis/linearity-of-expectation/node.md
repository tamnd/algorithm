---
tag: XCKF51
kind: theorem
slug: linearity-of-expectation
name: Linearity of expectation
aliases:
- additivity of expectation
area: foundations/probabilistic-analysis
level: intro
summary: The expectation of a sum equals the sum of expectations, with no independence assumption needed.
prereqs: [probability-space, random-variable, expected-value]
see_also: [indicator-random-variable, quicksort-expected-running-time, randomized-quicksort, variance, walds-equation, jensens-inequality, independent-random-variables, maximum-cut]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.3, Discrete random variables (linearity of expectation); Section 5.2 (indicator random variables); Section 7.4.2, Expected running time (randomized quicksort)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.1.1, Linearity of Expectations; Section 2.5, Application, The Expected Run-Time of Quicksort; Section 6.2.1, Application, Finding a Large Cut
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (the expected number of comparisons of RandQS)
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter IX, Random Variables; Expectation (the expectation of a sum)
---

Linearity of expectation says that the [expected value](/expected-value/) of a sum of [random variables](/random-variable/) is the sum of their expected values: $\mathrm{E}[X + Y] = \mathrm{E}[X] + \mathrm{E}[Y]$, and $\mathrm{E}[aX + b] = a\,\mathrm{E}[X] + b$. It holds for any random variables with finite expectations, whether they are [independent](/independent-random-variables/) or not. With [indicator random variables](/indicator-random-variable/) it turns the expected value of a count into a sum of probabilities. It is the main tool of the expected-time analysis of randomized algorithms, for example the bound $2(n+1)H_n - 4n$ on the expected comparisons of [randomized quicksort](/randomized-quicksort/).

## Statement

Let $(\Omega, \Pr)$ be a discrete [probability space](/probability-space/), that is, $\Omega$ is finite or countable. For a random variable $X : \Omega \to \mathbb{R}$, write $p(\omega) = \Pr[\{\omega\}]$. The expectation $\mathrm{E}[X] = \sum_{\omega \in \Omega} X(\omega)\, p(\omega)$ is *finite* when $\sum_{\omega} |X(\omega)|\, p(\omega) < \infty$.

**Theorem (finite sums).** Let $X_1, \ldots, X_n$ be random variables on $\Omega$ with finite expectations, and let $a_1, \ldots, a_n, b$ be real numbers. Then $\sum_i a_i X_i + b$ has a finite expectation, and

$$ \mathrm{E}\Big[\sum_{i=1}^{n} a_i X_i + b\Big] = \sum_{i=1}^{n} a_i\, \mathrm{E}[X_i] + b. $$

No hypothesis on the joint distribution of the $X_i$ is needed.

**Theorem (countable sums).** Let $X_1, X_2, \ldots$ be random variables on $\Omega$.

1. If each $X_i \ge 0$, then $\mathrm{E}\big[\sum_{i \ge 1} X_i\big] = \sum_{i \ge 1} \mathrm{E}[X_i]$, where both sides may be $+\infty$.
2. If $\sum_{i \ge 1} \mathrm{E}\big[|X_i|\big] < \infty$, then the series $\sum_i X_i(\omega)$ converges absolutely for each $\omega$ with $p(\omega) > 0$, its sum has a finite expectation, and $\mathrm{E}\big[\sum_{i \ge 1} X_i\big] = \sum_{i \ge 1} \mathrm{E}[X_i]$.

The same statements hold on a general probability space, where the expectation is the Lebesgue integral. There they are the linearity of the integral and the monotone and dominated convergence theorems. This page proves the discrete case, which covers the analysis of algorithms with finitely many random choices.

## In plain words

Run a random process many times and add up a total cost in each run. The average total is the sum of the averages of the parts. This is true even when the parts depend on each other, for example when one part is large exactly when another part is small.

This matters because the parts of an algorithm almost always depend on each other. Which pairs of items quicksort compares depends on all its earlier random choices. You cannot easily describe the whole cost at once. But you can ask, for each pair of items, how likely it is that the pair is ever compared. The average number of comparisons is then the sum of these chances. Each chance needs only a small argument about one pair.

## Proof

**Finite sums.** We prove the case $\mathrm{E}[X + Y] = \mathrm{E}[X] + \mathrm{E}[Y]$ and the case $\mathrm{E}[aX + b] = a\,\mathrm{E}[X] + b$. The general statement then follows by induction on $n$.

*Sum.* Assume that $X$ and $Y$ have finite expectations. By the triangle inequality, $|X(\omega) + Y(\omega)| \le |X(\omega)| + |Y(\omega)|$ for each $\omega$, so
$$ \sum_\omega |X(\omega) + Y(\omega)|\, p(\omega) \le \sum_\omega |X(\omega)|\, p(\omega) + \sum_\omega |Y(\omega)|\, p(\omega) < \infty, $$
and $X + Y$ has a finite expectation. The two series $\sum_\omega X(\omega)p(\omega)$ and $\sum_\omega Y(\omega)p(\omega)$ converge absolutely, so we may add them term by term:
$$ \mathrm{E}[X + Y] = \sum_\omega \big(X(\omega) + Y(\omega)\big)\, p(\omega) = \sum_\omega X(\omega)\, p(\omega) + \sum_\omega Y(\omega)\, p(\omega) = \mathrm{E}[X] + \mathrm{E}[Y]. $$

*Scaling and shift.* $\sum_\omega |aX(\omega) + b|\, p(\omega) \le |a| \sum_\omega |X(\omega)|\, p(\omega) + |b| < \infty$, and
$$ \mathrm{E}[aX + b] = \sum_\omega \big(aX(\omega) + b\big)\, p(\omega) = a \sum_\omega X(\omega)\, p(\omega) + b \sum_\omega p(\omega) = a\,\mathrm{E}[X] + b, $$
because $\sum_\omega p(\omega) = 1$.

*Induction.* For $n = 1$ the claim is the scaling case. For $n \ge 2$, write $\sum_{i=1}^n a_i X_i + b = \big(\sum_{i=1}^{n-1} a_i X_i + b\big) + a_n X_n$. By the induction hypothesis the first part has a finite expectation, equal to $\sum_{i<n} a_i \mathrm{E}[X_i] + b$. By the scaling case, $a_n X_n$ has expectation $a_n \mathrm{E}[X_n]$. The sum case adds the two. $\square$

*Where independence would enter, and why it does not.* The same proof can be written with the joint distribution of $X$ and $Y$, as in CLRS Appendix C.3. With $q(x, y) = \Pr[X = x \text{ and } Y = y]$,
$$ \mathrm{E}[X + Y] = \sum_{x, y} (x + y)\, q(x, y) = \sum_x x \sum_y q(x, y) + \sum_y y \sum_x q(x, y) = \sum_x x \Pr[X = x] + \sum_y y \Pr[Y = y]. $$
The inner sums are marginal probabilities: $\sum_y q(x, y) = \Pr[X = x]$ for any joint distribution $q$. The proof never writes $q(x, y)$ as a product, so it never uses independence.

**Countable sums.** *Part 1.* Let $X_i \ge 0$. Then
$$ \mathrm{E}\Big[\sum_i X_i\Big] = \sum_\omega \sum_i X_i(\omega)\, p(\omega) = \sum_i \sum_\omega X_i(\omega)\, p(\omega) = \sum_i \mathrm{E}[X_i]. $$
The middle step exchanges the order of a double series with non-negative terms. This is valid for any such series, with the value $+\infty$ allowed: both orders equal the supremum of the sums over finite sets of index pairs $(i, \omega)$.

*Part 2.* Apply part 1 to the variables $|X_i|$: $\sum_\omega \sum_i |X_i(\omega)|\, p(\omega) = \sum_i \mathrm{E}[|X_i|] < \infty$. So for each $\omega$ with $p(\omega) > 0$ the series $\sum_i |X_i(\omega)|$ is finite, the double series $\sum_{i, \omega} X_i(\omega) p(\omega)$ converges absolutely, and an absolutely convergent double series has the same sum in both orders. This gives $\mathrm{E}[\sum_i X_i] = \sum_i \mathrm{E}[X_i]$, and the bound $|\sum_i X_i| \le \sum_i |X_i|$ shows that the expectation on the left is finite. $\blacksquare$

## Consequences

### Expected comparisons of randomized quicksort

[Randomized quicksort](/randomized-quicksort/) (CLRS Section 7.3) sorts $n$ distinct keys. Each call picks its pivot uniformly at random from its subarray, and the partition compares the pivot with each other key of the subarray once. Let $z_1 < z_2 < \cdots < z_n$ be the keys in sorted order and $Z_{ij} = \{z_i, z_{i+1}, \ldots, z_j\}$.

**Claim.** The expected number of comparisons is exactly $2(n+1)H_n - 4n$, where $H_n = \sum_{k=1}^n 1/k$.

*Proof.* Two keys are compared only when one of them is the pivot of the current call. After that call the pivot is in no subarray, so each pair is compared at most once. Let $X_{ij} = I\{z_i \text{ is compared with } z_j\}$ for $i < j$. The number of comparisons is $X = \sum_{i<j} X_{ij}$, so by linearity and the lemma $\mathrm{E}[I\{A\}] = \Pr[A]$ of [indicator random variables](/indicator-random-variable/),
$$ \mathrm{E}[X] = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \Pr[z_i \text{ is compared with } z_j]. $$

Fix $i < j$. As long as no key of $Z_{ij}$ has been a pivot, all of $Z_{ij}$ lies in one subarray: a pivot outside $Z_{ij}$ is smaller than all of $Z_{ij}$ or larger than all of it, so the partition keeps $Z_{ij}$ on one side. Consider the first call whose pivot is in $Z_{ij}$. Its subarray contains all of $Z_{ij}$, and its pivot is uniform over the subarray, so given that the pivot is in $Z_{ij}$, each of the $j - i + 1$ keys of $Z_{ij}$ is this pivot with the same probability. If the pivot is $z_i$ or $z_j$, the two keys are compared in this call. If the pivot is a key strictly between them, $z_i$ and $z_j$ go to different subarrays and are never compared. So $\Pr[z_i \text{ is compared with } z_j] = 2/(j - i + 1)$.

Set $k = j - i + 1$. For each $k$ from $2$ to $n$ there are $n + 1 - k$ pairs with $j - i + 1 = k$. Hence
$$ \mathrm{E}[X] = \sum_{k=2}^{n} \frac{2(n + 1 - k)}{k} = 2(n+1)\sum_{k=2}^{n}\frac1k - 2(n-1) = 2(n+1)(H_n - 1) - 2(n - 1) = 2(n+1)H_n - 4n. \qquad \square $$

Since $H_n = \ln n + O(1)$, this is $2n\ln n + O(n) \approx 1.386\, n \lg n$. The exact values for $n = 3$, $10$, $100$ and $1000$ are $8/3$, $30791/1260 \approx 24.44$, $647.85$ and $10985.91$. They agree with the recurrence $C(n) = n - 1 + \frac{2}{n}\sum_{k=0}^{n-1} C(k)$ that the [conditional expectation](/conditional-expectation/) of the pivot rank gives. The indicators $X_{ij}$ are far from independent, and the proof does not need them to be. The full running-time analysis is on [expected running time of quicksort](/quicksort-expected-running-time/).

### Fixed points of a random permutation

Let $\pi$ be a uniform random permutation of $\{1, \ldots, n\}$, with $n \ge 1$. Let $F = \sum_{i=1}^n I\{\pi(i) = i\}$ be its number of fixed points. Each $\pi(i)$ is uniform over the $n$ values, so $\Pr[\pi(i) = i] = 1/n$ and $\mathrm{E}[F] = n \cdot 1/n = 1$ for each $n$. For $n = 5$ the $120$ permutations have $120$ fixed points in total. The events depend on each other (if $n - 1$ points are fixed, the last one is too), and the answer is still exact.

### Existence by expectation: a large cut

Put each vertex of a graph with $m$ edges on one side of a cut by a fair coin flip. An edge crosses the cut when its two ends get different sides, which has probability $1/2$. By linearity the expected number of crossing edges is $m/2$. A random variable takes some value at least its mean, so each graph has a cut with at least $m/2$ edges. This is the start of the approximation algorithms for [maximum cut](/maximum-cut/) (Mitzenmacher and Upfal, Section 6.2.1). The same argument shows that a [random assignment](/random-assignment-max-3-sat/) satisfies $7m/8$ clauses of a 3-CNF formula in expectation, when each clause has three literals on distinct variables.

### Other uses

- Expected counts with [indicator random variables](/indicator-random-variable/): $H_n$ hires in the [hiring problem](/hiring-problem/), $n(n-1)/4$ [inversions](/expected-number-of-inversions/) in a random permutation, the shared pairs of the [birthday paradox](/birthday-paradox/).
- The [coupon collector problem](/coupon-collector-problem/): the waiting time is a sum of $n$ [geometric](/geometric-distribution/) waiting times with means $n/(n - i + 1)$, so its mean is $nH_n$.
- The mean $np$ of the [binomial distribution](/binomial-distribution/), as a sum of $n$ indicators with mean $p$.
- The formula $\mathrm{Var}[X] = \mathrm{E}[X^2] - \mathrm{E}[X]^2$ and the variance of a sum, on the page of [variance](/variance/).
- The expected linear time of [quickselect](/quickselect-expected-linear/) and of [bucket sort](/bucket-sort-expected-linear/) on uniform input.

## Tightness

The statement is an equality, so the question is which hypotheses can be dropped. None of the following can.

- **Products need independence.** Let $X = Y$ be the indicator of heads in one fair coin flip. Then $\mathrm{E}[XY] = \mathrm{E}[X] = 1/2$, but $\mathrm{E}[X]\,\mathrm{E}[Y] = 1/4$. The rule $\mathrm{E}[XY] = \mathrm{E}[X]\,\mathrm{E}[Y]$ holds for [independent random variables](/independent-random-variables/), and it is not part of linearity.
- **Countable sums need a condition.** Let $N$ take the value $k \ge 1$ with probability $2^{-k}$, and let $X_k = 2^k\, I\{N = k\} - 2^{k+1}\, I\{N = k+1\}$. Then $\mathrm{E}[X_k] = 1 - 1 = 0$ for each $k$, so $\sum_k \mathrm{E}[X_k] = 0$. But for each outcome only $X_N$ and $X_{N-1}$ are not zero, and they cancel when $N \ge 2$. So $\sum_k X_k = 2\, I\{N = 1\}$, whose expectation is $1$. Here $\mathrm{E}[|X_k|] = 2$ for each $k$, so $\sum_k \mathrm{E}[|X_k|] = \infty$, and part 2 of the theorem does not apply.
- **Infinite expectations.** If $\mathrm{E}[X] = +\infty$ and $Y = -X$, then $X + Y = 0$ has expectation $0$, but $\mathrm{E}[X] + \mathrm{E}[Y]$ is the undefined form $\infty - \infty$.
- **A random number of terms.** Let $X_1, X_2$ be independent fair bits, and let $N = 1$ when $X_2 = 0$ and $N = 2$ when $X_2 = 1$. Then $\mathrm{E}[\sum_{i=1}^N X_i] = \frac12 \cdot \frac12 + \frac12 \cdot \frac32 = 1$, but $\mathrm{E}[N]\,\mathrm{E}[X_1] = \frac32 \cdot \frac12 = \frac34$. The rule $\mathrm{E}[\sum_{i \le N} X_i] = \mathrm{E}[N]\,\mathrm{E}[X_1]$ needs the hypotheses of [Wald's equation](/walds-equation/), and here $N$ looks ahead at $X_2$.
- **Only linear maps.** In general $\mathrm{E}[f(X)] \ne f(\mathrm{E}[X])$ for a function $f$ that is not affine. For convex $f$ the direction of the error is given by [Jensen's inequality](/jensens-inequality/). For the maximum, $\mathrm{E}[\max(X, Y)] \ge \max(\mathrm{E}[X], \mathrm{E}[Y])$, with strict inequality for two independent fair bits ($3/4$ against $1/2$).

### Pitfalls

- **Expectation does not bound the spread.** Linearity gives the mean of quicksort's comparison count, not the probability of a slow run. For that you need the [variance](/variance/) of the count or a [tail bound](/high-probability-bounds/).
- **Asymptotic form against exact value.** $2n\ln n$ is the leading term only. At $n = 1000$ it is $13815.5$, while the exact mean is $10985.9$. The term $-4n$ and the constant of $H_n$ matter at practical sizes.
- **The random model.** The quicksort result is over the random pivot choices, for each fixed input with distinct keys. With a fixed pivot rule, such as the last key, the same sum is the average over random inputs, and an adversary can force $\binom{n}{2}$ comparisons. With many equal keys the two-way partition behaves differently, and the claim needs distinct keys.

## History

The additivity of expectation is part of the basic theory of expected values, as in Feller, Chapter IX. Its use with one indicator for each pair of keys to analyse randomized quicksort is the standard first example of the textbooks on randomized algorithms: Motwani and Raghavan, Chapter 1, Mitzenmacher and Upfal, Section 2.5, and CLRS, Section 7.4.2.

## References
