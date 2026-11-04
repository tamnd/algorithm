---
tag: 4X7HJN
kind: definition
slug: discrete-probability-distribution
name: Discrete probability distribution
area: foundations/probabilistic-analysis
level: intro
summary: A probability distribution defined on a finite or countable sample space, where each outcome has a probability and events sum these values.
prereqs: [probability-space, probability-distribution]
see_also: [random-variable, uniform-distribution, bernoulli-trials, binomial-distribution, geometric-distribution, poisson-distribution, alias-method, inverse-transform-sampling]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.2, Discrete probability distributions, and Section C.3, Discrete random variables
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 1.2, Axioms of Probability, and Section 2.1, Random Variables and Expectation
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter I, The Sample Space (discrete sample spaces), and Chapter IX, Random Variables; Expectation
---

A discrete probability distribution is a [probability distribution](/probability-distribution/) on a finite or countable sample space, where each outcome has a probability and the probability of an event is the sum of the probabilities of its outcomes. It is given by one function, the probability mass function, which is nonnegative and sums to 1. Almost all randomness in algorithms is discrete: random bits, random pivots, random hash values and random levels in a [skip list](/skip-list/).

## Definition

Let $S$ be a finite or countably infinite set. A **probability mass function** (pmf) on $S$ is a function $p : S \to [0, 1]$ with

$$\sum_{s \in S} p(s) = 1.$$

The **discrete probability distribution** with pmf $p$ is the function on all subsets $A \subseteq S$ given by

$$\Pr(A) = \sum_{s \in A} p(s).$$

The sums are sums of nonnegative terms, so their value does not depend on the order of the terms, and they are always defined (possibly $+\infty$, but here at most 1).

**It is a probability measure.** $\Pr(A) \ge 0$ since each term is at least 0, and $\Pr(S) = 1$ by the condition on $p$. For pairwise disjoint $A_1, A_2, \ldots$, the terms of $\sum_{s \in \bigcup_i A_i} p(s)$ split into the groups $A_1, A_2, \ldots$ with no term in two groups. A series of nonnegative terms can be grouped in any way without a change of its value, so the sum equals $\sum_i \sum_{s \in A_i} p(s) = \sum_i \Pr(A_i)$. So $(S, 2^S, \Pr)$ is a [probability space](/probability-space/).

**Each measure on a countable space is of this form.** Let $\Pr$ be a probability measure on all subsets of a countable $S$, and set $p(s) = \Pr(\{s\})$. Each $A \subseteq S$ is the countable disjoint union of its singletons, so countable additivity gives $\Pr(A) = \sum_{s \in A} p(s)$, and $\sum_{s \in S} p(s) = \Pr(S) = 1$.

**Of a random variable.** A [random variable](/random-variable/) $X$ is **discrete** when it takes values in a countable set $V$ with $\Pr(X \in V) = 1$. Its pmf is $p_X(x) = \Pr(X = x)$, and its distribution is $\Pr(X \in B) = \sum_{x \in B \cap V} p_X(x)$. CLRS calls $p_X$ the probability density function of $X$. This page uses "mass function" to keep it apart from the [density](/probability-density-function/) of a continuous variable. The **support** of $X$ is $\{x : p_X(x) > 0\}$. It is countable, because for each $k \ge 1$ at most $k$ values have $p_X(x) > 1/k$.

**Joint and marginal mass functions.** For two discrete variables, $p_{X,Y}(x, y) = \Pr(X = x, Y = y)$. The marginal is $p_X(x) = \sum_y p_{X,Y}(x, y)$, because the events $\{X = x, Y = y\}$ for the values $y$ of $Y$ are disjoint with union $\{X = x\}$ (up to a null event).

## Examples and non-examples

**Uniform on a finite set.** $p(s) = 1/|S|$. Examples: the bucket of one key under [simple uniform hashing](/simple-uniform-hashing/) ($S = \{0, \ldots, m-1\}$), a [random permutation](/random-permutation/) of $n$ keys ($|S| = n!$), and the pivot index in [randomized quicksort](/randomized-quicksort/). See [uniform distribution](/uniform-distribution/).

**Named families.** Each of these is a pmf on the given set. The page of each family proves that the values sum to 1.

| name | set | $p(k)$ | typical use |
|---|---|---|---|
| [Bernoulli](/bernoulli-trials/)$(q)$ | $\{0, 1\}$ | $q^k (1-q)^{1-k}$ | one coin flip, one probe |
| [binomial](/binomial-distribution/)$(n, q)$ | $\{0, \ldots, n\}$ | $\binom{n}{k} q^k (1-q)^{n-k}$ | keys in one bucket |
| [geometric](/geometric-distribution/)$(q)$ | $\{1, 2, \ldots\}$ | $(1-q)^{k-1} q$ | attempts until success |
| [Poisson](/poisson-distribution/)$(\lambda)$ | $\{0, 1, \ldots\}$ | $e^{-\lambda} \lambda^k / k!$ | bucket loads for large tables |

**An event in a countable space.** Let $X$ be the number of fair coin flips until the first heads, so $p(k) = 2^{-k}$ for $k \ge 1$. The level of a node in a [skip list](/skip-list/) with promotion probability $1/2$ has this law. The probability that $X$ is even is

$$\sum_{j \ge 1} 2^{-2j} = \frac{1/4}{1 - 1/4} = \frac{1}{3}.$$

**A valid pmf with an infinite mean.** $p(k) = \frac{1}{k(k+1)}$ for $k \ge 1$ sums to 1, because $\frac{1}{k(k+1)} = \frac1k - \frac{1}{k+1}$ and the partial sums telescope to $1 - \frac{1}{n+1}$. But $\sum_k k \, p(k) = \sum_k \frac{1}{k+1}$ diverges. The [expected value](/expected-value/) page shows a waiting time of this kind.

**Non-example: a divergent weight.** $p(k) = 1/k$ on $k \ge 1$ cannot be scaled to a pmf, because $\sum_k 1/k$ diverges (see [harmonic series](/harmonic-series/)). In contrast, $p(k) = 1/k^2$ can be scaled: divide by $\pi^2 / 6$.

**Non-example: a uniform distribution on a countably infinite set.** If $p(s) = c$ for all $s$ in a countably infinite $S$, then the sum is 0 or $\infty$, never 1. See [probability space](/probability-space/).

**Sampling.** To draw from a pmf on $\{1, \ldots, n\}$, store the prefix sums $c_k = p(1) + \cdots + p(k)$, draw $U$ uniform in $[0, 1)$, and return the least $k$ with $U < c_k$. Then $\Pr(k) = c_k - c_{k-1} = p(k)$. With [binary search](/binary-search/) a draw costs $O(\log n)$ time. This is [inverse transform sampling](/inverse-transform-sampling/). The [alias method](/alias-method/) draws in $O(1)$ time after $O(n)$ preprocessing.

### Pitfalls

- **Modulo bias.** If a generator gives an integer $R$ that is uniform on $\{0, \ldots, 7\}$, then $R \bmod 3$ is not uniform on $\{0, 1, 2\}$: the values 0, 1, 2 have probabilities $3/8$, $3/8$, $2/8$. In general $R \bmod m$ is uniform only when $m$ divides the number of values of $R$. The fix is to reject values of $R$ at or above the largest multiple of $m$ and draw again. The number of draws is then [geometric](/geometric-distribution/).
- **Countable support is not the same as a discrete-looking set.** A variable that takes each rational value in $[0, 1]$ with positive probability is discrete, although its values are dense. A variable that is uniform on $[0, 1]$ takes each value with probability 0 and is not discrete.
- **Probability zero outcomes.** A pmf may be 0 at some points of $S$. Then a nonempty event can have probability 0. Bounds of the form "with probability 1" do not say "for every outcome".

## Related definitions

- A [probability distribution](/probability-distribution/) in general need not have a mass function.
- A [probability density function](/probability-density-function/) plays the role of the pmf for continuous variables, with integrals in place of sums.
- The CDF of a discrete variable is the step function $F_X(x) = \sum_{y \le x} p_X(y)$.
- [Expected value](/expected-value/) of a discrete variable is $\sum_x x \, p_X(x)$ when the sum converges absolutely.

## References
