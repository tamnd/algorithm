---
tag: K3RK0K
kind: concept
slug: expected-value
name: Expected value
aliases:
- expectation
- mean
area: foundations/probabilistic-analysis
level: intro
summary: The probability-weighted average of a random variable.
prereqs: [random-variable, discrete-probability-distribution]
see_also: [linearity-of-expectation, indicator-random-variable, variance, conditional-expectation, markov-inequality, jensens-inequality, quicksort-expected-running-time, hiring-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.3, Discrete random variables (expected value); Section 5.2, Indicator random variables; Section 7.4.2, Expected running time
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.1, Random Variables and Expectation; Section 2.5, Application, The Expected Run-Time of Quicksort
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (randomized quicksort and its expected number of comparisons)
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter IX, Random Variables; Expectation, Section 2
---

The expected value $\mathbb{E}[X]$ of a [random variable](/random-variable/) $X$ is the average of its values, each weighted by its probability: $\sum_x x \Pr(X = x)$ for a discrete variable. It is the main measure of the cost of a [randomized algorithm](/randomized-algorithm/) and of [average-case](/average-case-analysis/) behavior: "randomized quicksort makes $2n \ln n + O(n)$ comparisons in expectation" is a statement about one expected value. Most such results come from [linearity of expectation](/linearity-of-expectation/), which holds with no independence.

## In plain words

Run a random experiment many times, and each time write down the number you care about, such as the running time. The expected value is what the average of these numbers settles to over very many runs. To compute it without running anything, take each possible value, multiply it by its chance, and add up.

The expected value of a sum is the sum of the expected values, even when the parts depend on each other. This is the trick behind most analyses of randomized algorithms: cut the cost into many small yes-or-no events, find the chance of each, and add the chances.

The expected value can mislead. A rare huge value can make it large, it can even be infinite, and the expected value of a ratio is not the ratio of the expected values.

## The idea

**Definition.** Let $X$ be a discrete random variable with values in a countable set $V$. If $\sum_{x \in V} |x| \Pr(X = x) < \infty$, the **expected value** of $X$ is

$$\mathbb{E}[X] = \sum_{x \in V} x \Pr(X = x).$$

The absolute convergence makes the sum independent of the order of the terms. If $X \ge 0$, the sum is always defined, possibly as $+\infty$. If $X$ has a [density](/probability-density-function/) $f$, then $\mathbb{E}[X] = \int x f(x)\,dx$ when $\int |x| f(x)\,dx < \infty$. In general $\mathbb{E}[X]$ is the integral of $X$ with respect to $\Pr$. On a countable space it equals $\sum_{\omega} X(\omega) \Pr(\{\omega\})$: group the outcomes by the value of $X$.

**Basic rules.** Assume the expected values below exist.

1. **Indicators.** For an event $A$, $\mathbb{E}[I_A] = 1 \cdot \Pr(A) + 0 \cdot \Pr(\bar A) = \Pr(A)$. See [indicator random variable](/indicator-random-variable/).
2. **Functions.** For $g : \mathbb{R} \to \mathbb{R}$, $\mathbb{E}[g(X)] = \sum_x g(x) \Pr(X = x)$, if this converges absolutely. Proof: group the values $x$ by $y = g(x)$; then $\Pr(g(X) = y) = \sum_{x : g(x) = y} \Pr(X = x)$.
3. **Linearity.** $\mathbb{E}[aX + bY] = a\mathbb{E}[X] + b\mathbb{E}[Y]$ for constants $a$, $b$ and any $X$, $Y$ on the same space, independent or not. Proof on a countable space: $\sum_\omega (aX(\omega) + bY(\omega)) \Pr(\{\omega\})$ splits into two absolutely convergent sums. By induction, $\mathbb{E}[\sum_{i=1}^n X_i] = \sum_{i=1}^n \mathbb{E}[X_i]$. See [linearity of expectation](/linearity-of-expectation/).
4. **Monotonicity.** If $X \le Y$ at every outcome, then $\mathbb{E}[X] \le \mathbb{E}[Y]$: apply linearity to $Y - X \ge 0$, whose expected value is a sum of nonnegative terms.
5. **Products of independent variables.** If $X$ and $Y$ are discrete and [independent](/independent-random-variables/), then $\mathbb{E}[XY] = \mathbb{E}[X]\mathbb{E}[Y]$. Proof: $\mathbb{E}[XY] = \sum_{x, y} xy \Pr(X = x, Y = y) = \sum_{x,y} xy \Pr(X = x)\Pr(Y = y) = \left(\sum_x x \Pr(X = x)\right)\left(\sum_y y \Pr(Y = y)\right)$, where the double sum converges absolutely because it factors into two absolutely convergent sums. Without independence this can fail: for a fair bit $X$, $\mathbb{E}[X \cdot X] = 1/2 \ne 1/4$.
6. **Tail sums.** If $X$ takes values in $\{0, 1, 2, \ldots\}$, then $\mathbb{E}[X] = \sum_{k \ge 1} \Pr(X \ge k)$. Proof: $X = \sum_{k \ge 1} I_{\{X \ge k\}}$ at each outcome, because exactly the first $X$ indicators are 1. All terms are nonnegative, so the sums can be exchanged: $\sum_{j} j \Pr(X = j) = \sum_j \sum_{k=1}^{j} \Pr(X = j) = \sum_{k \ge 1} \sum_{j \ge k} \Pr(X = j) = \sum_{k \ge 1} \Pr(X \ge k)$.
7. **Total expectation.** If $B_1, B_2, \ldots$ partition $\Omega$ into events of positive probability, then $\mathbb{E}[X] = \sum_i \mathbb{E}[X \mid B_i] \Pr(B_i)$, where $\mathbb{E}[X \mid B] = \sum_x x \Pr(X = x \mid B)$. Proof: substitute the [law of total probability](/conditional-probability/) $\Pr(X = x) = \sum_i \Pr(X = x \mid B_i)\Pr(B_i)$ and exchange the sums, which is allowed by absolute convergence. See [conditional expectation](/conditional-expectation/).
8. **Markov's inequality.** If $X \ge 0$ and $t > 0$, then $\Pr(X \ge t) \le \mathbb{E}[X]/t$, because $X \ge t \cdot I_{\{X \ge t\}}$ and rules 1 and 4 apply. See [Markov's inequality](/markov-inequality/). It turns an expected cost into a bound in probability.

## Examples

**The hiring problem.** Candidates arrive in a uniformly random order, and we hire each candidate who is better than all before. Candidate $i$ is the best of the first $i$ with probability $1/i$, so by rules 1 and 3 the expected number of hires is $\sum_{i=1}^n 1/i = H_n$. For $n = 100$ this is about $5.187$. CLRS, Section 5.2, gives this analysis; see the [hiring problem](/hiring-problem/).

**Comparisons of randomized quicksort.** Let $z_1 < \cdots < z_n$ be the keys in sorted order. [Randomized quicksort](/randomized-quicksort/) compares $z_i$ and $z_j$ at most once, and it does so with probability $2/(j - i + 1)$ (proved on the [conditional probability](/conditional-probability/) page). With $d = j - i$, linearity gives

$$\mathbb{E}[C] = \sum_{i < j} \frac{2}{j - i + 1} = \sum_{d=1}^{n-1} \frac{2(n - d)}{d + 1} = \sum_{k=2}^{n} \frac{2(n + 1 - k)}{k} = 2(n+1)(H_n - 1) - 2(n - 1) = 2(n+1)H_n - 4n.$$

For $n = 4$ this is $29/6$, the mean of the distribution on the [probability distribution](/probability-distribution/) page. For $n = 10$ it is $30791/1260 \approx 24.44$, for $n = 100$ about $647.85$, and for $n = 1000$ about $10985.9$. Since $H_n = \ln n + O(1)$, this is $2n \ln n + O(n) \approx 1.39\, n \log_2 n$. The comparisons are far from independent, but linearity does not need independence. CLRS, Section 7.4.2, Mitzenmacher and Upfal, Section 2.5, and Motwani and Raghavan, Chapter 1, give this argument. See [quicksort expected running time](/quicksort-expected-running-time/).

**Chains in a hash table.** With $n$ keys in $m$ buckets under [simple uniform hashing](/simple-uniform-hashing/), the chain of a fixed bucket has expected length $n/m = \alpha$, the sum of $n$ indicators of probability $1/m$. A search for a key that is absent costs $1 + \alpha$ steps in expectation, counting the hash. See [chaining expected search time](/chaining-expected-search-time/).

**Skip list size.** In a [skip list](/skip-list/) with promotion probability $1/2$, a key has a [geometric](/geometric-distribution/) level with mean 2, so the expected total number of nodes is $2n$, by linearity over the keys.

**Retries.** If each attempt succeeds with probability $p$ independently, the expected number of attempts is $1/p$, by the tail sum rule 6 with $\Pr(N \ge k) = (1-p)^{k-1}$.

### Pitfalls

- **The expected value of a ratio is not the ratio of the expected values.** A randomized routine takes time $T = 1$ or $T = 100$, each with probability $1/2$. Its expected time is $50.5$, but its expected rate is $\mathbb{E}[1/T] = 0.5 \cdot 1 + 0.5 \cdot 0.01 = 0.505$ jobs per unit of time, while $1/\mathbb{E}[T] \approx 0.0198$. The two differ by a factor of about 25. In the same way, the mean of a per-run ratio such as "successes per attempt" is not total successes over total attempts. For convex $g$, [Jensen's inequality](/jensens-inequality/) gives $\mathbb{E}[g(X)] \ge g(\mathbb{E}[X])$, and $1/x$ is convex on $x > 0$.
- **A finite variable can have an infinite mean.** Let $X_0, X_1, X_2, \ldots$ be independent with the same continuous law, and let $N$ be the first $n \ge 1$ with $X_n > X_0$: the wait for a candidate better than the first one. $N > n$ exactly when $X_0$ is the largest of $X_0, \ldots, X_n$, which has probability $1/(n+1)$ by symmetry. So $N$ is finite with probability 1, but by rule 6, $\mathbb{E}[N] = \sum_{n \ge 0} \frac{1}{n+1} = \infty$. Here $\Pr(N = n) = \frac{1}{n(n+1)}$.
- **Expected time is not a bound on each run.** Randomized quicksort runs in expected $O(n \log n)$ time on each input, but some pivot sequences take $\Theta(n^2)$ time. Rule 8 bounds how often a run is much slower than the mean. Sharper statements use [high-probability bounds](/high-probability-bounds/).
- **Name the space.** The expected time of a randomized algorithm on its worst input and the expected time of a deterministic algorithm on a random input are different quantities. See [average-case analysis](/average-case-analysis/).
- **The expected value need not be a possible value.** The expected number of comparisons for $n = 4$ is $29/6$, which no run makes.

## Where it is used

- **Analysis of randomized algorithms.** Expected running times of [Las Vegas algorithms](/las-vegas-algorithm/) such as [randomized quicksort](/randomized-quicksort/) and [randomized quickselect](/randomized-quickselect/), and the expected number of repetitions of a test.
- **Hashing and data structures.** Expected chain lengths, probe counts and depths in [hash tables](/hash-table/), [treaps](/treap/), [skip lists](/skip-list/) and [random binary search trees](/random-bst-expected-depth/).
- **Average-case analysis.** Expected costs over a distribution of inputs, see [average-case analysis](/average-case-analysis/).
- **Tail bounds.** [Markov's inequality](/markov-inequality/), [Chebyshev's inequality](/chebyshev-inequality/) and the [Chernoff bound](/chernoff-bound/) all start from expected values of $X$, of $(X - \mathbb{E}[X])^2$, or of $e^{tX}$.
- **The probabilistic method.** If a random object has expected value $\mu$ for some score, then some object has score at least $\mu$, and some has score at most $\mu$. See [probabilistic method](/probabilistic-method/).

## References
