---
tag: 101AXP
kind: concept
slug: random-variable
name: Random variable
aliases:
- discrete random variable
area: foundations/probabilistic-analysis
level: intro
summary: A function from the sample space to the reals, used to model quantities such as running time or cost.
prereqs: [probability-space, probability-distribution]
see_also: [discrete-probability-distribution, probability-density-function, indicator-random-variable, expected-value, independent-random-variables, variance, linearity-of-expectation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.3, Discrete random variables; Section 5.2, Indicator random variables
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.1, Random Variables and Expectation
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction, and Appendix C, Basic Probability Theory
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter IX, Random Variables; Expectation, Section 1
---

A random variable is a function from the sample space of a [probability space](/probability-space/) to the real numbers. It is how probabilistic analysis names a quantity that depends on chance: the running time of a [randomized algorithm](/randomized-algorithm/), the length of a chain in a [hash table](/hash-table/), the height of a [skip list](/skip-list/), or the number of retries before a request succeeds. Once a quantity is a random variable, we can ask for its [distribution](/probability-distribution/), its [expected value](/expected-value/) and its tails.

## In plain words

A random experiment has many possible results. A random variable is a rule that reads one number off each result. If the experiment is "flip three coins", one rule is "count the heads". If the experiment is "run randomized quicksort, with all its random pivot choices", one rule is "count the comparisons".

The rule itself is fixed and has nothing random in it. The chance is in which result occurs. So the number it gives is uncertain before the run, and we describe it by the chance of each value it can take. Many rules can read different numbers off the same experiment, and we can add them, compare them or take the largest. This is how an analysis turns "the algorithm flips coins" into exact statements about its cost.

## The idea

**Definition.** Let $(\Omega, \mathcal{F}, \Pr)$ be a [probability space](/probability-space/). A **random variable** is a function $X : \Omega \to \mathbb{R}$ such that $\{\omega : X(\omega) \le x\} \in \mathcal{F}$ for each real $x$. The condition says that "$X \le x$" is an event, so it has a probability. When $\Omega$ is countable and every subset is an event, the condition always holds, and each function $\Omega \to \mathbb{R}$ is a random variable. CLRS and Feller define a random variable in this discrete setting.

**Notation.** We write $\{X = x\}$ for the event $\{\omega : X(\omega) = x\}$, and $\Pr(X = x)$ for its probability. In the same way, $\{X \le x\}$, $\{X \in B\}$ and $\{X \ne Y\}$ are events. The function $x \mapsto \Pr(X = x)$ is the mass function of a [discrete](/discrete-probability-distribution/) $X$. A continuous $X$ may have a [density](/probability-density-function/) instead.

**Operations.** If $X$ and $Y$ are random variables on the same space, then so are $X + Y$, $XY$, $cX$, $\max(X, Y)$ and $g(X)$ for each continuous $g : \mathbb{R} \to \mathbb{R}$. In a discrete space this is immediate, since every function is a random variable. In general, for the sum: $\{X + Y > z\} = \bigcup_{r \in \mathbb{Q}} (\{X > r\} \cap \{Y > z - r\})$, a countable union of events, because between $z - Y(\omega)$ and $X(\omega)$ there is a rational number when $X(\omega) + Y(\omega) > z$. For the maximum: $\{\max(X, Y) \le x\} = \{X \le x\} \cap \{Y \le x\}$.

**Indicator random variables.** For an event $A$, the [indicator random variable](/indicator-random-variable/) $I_A$ is 1 on $A$ and 0 off $A$. Then $\mathbb{E}[I_A] = \Pr(A)$. CLRS, Section 5.2, uses sums of indicators to count events such as "candidate $i$ is hired" or "keys $i$ and $j$ collide", and then applies [linearity of expectation](/linearity-of-expectation/).

**Joint behavior.** Several random variables on one space have a joint distribution: $\Pr(X = x, Y = y)$ for discrete variables. They are [independent](/independent-random-variables/) when $\Pr(X = x, Y = y) = \Pr(X = x) \Pr(Y = y)$ for all $x, y$ (for discrete variables), or $\Pr(X \le x, Y \le y) = \Pr(X \le x) \Pr(Y \le y)$ in general.

**What we compute about a random variable.** Its distribution, its [expected value](/expected-value/) $\mathbb{E}[X]$, its [variance](/variance/), and tail bounds of the form $\Pr(X \ge t) \le \delta$ from the [Markov](/markov-inequality/), [Chebyshev](/chebyshev-inequality/) and [Chernoff](/chernoff-bound/) inequalities.

## Examples

**Heads in three flips.** $\Omega = \{H, T\}^3$ has 8 equally likely outcomes. Let $X$ be the number of heads. Then $X(TTT) = 0$; $X$ is 1 on $HTT$, $THT$, $TTH$; it is 2 on $HHT$, $HTH$, $THH$; and $X(HHH) = 3$. So $\Pr(X = 0, 1, 2, 3) = 1/8, 3/8, 3/8, 1/8$. This is the [binomial distribution](/binomial-distribution/) with $n = 3$ and $p = 1/2$.

**Collisions in a hash table.** Put $n$ keys into $m$ buckets with [simple uniform hashing](/simple-uniform-hashing/). For $i < j$ let $I_{ij}$ be the indicator that keys $i$ and $j$ land in the same bucket, and let $X = \sum_{i < j} I_{ij}$ be the number of colliding pairs. Then $\mathbb{E}[X] = \binom{n}{2} / m$. For $n = 100$ and $m = 10^6$ this is $0.00495$.

**Comparisons of randomized quicksort.** For a fixed input of 5 distinct keys, the number $C$ of comparisons that [randomized quicksort](/randomized-quicksort/) makes is a function of its random pivot choices. Its distribution is

| $c$ | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|
| $\Pr(C = c)$ | $1/3$ | $4/15$ | $1/5$ | $1/15$ | $2/15$ |

and $\mathbb{E}[C] = 37/5 = 7.4$. The input is not random here. The randomness is only in the pivots.

**The height of a skip list.** In a [skip list](/skip-list/) with promotion probability $1/2$, each key $i$ gets a level $L_i \ge 1$, with $\Pr(L_i \ge k) = 2^{-(k-1)}$, and the levels are independent. The height is the random variable $H = \max_i L_i$. By independence, $\Pr(H \ge k) = 1 - (1 - 2^{-(k-1)})^n$. By the [union bound](/union-bound/), $\Pr(H \ge k) \le n \, 2^{-(k-1)}$. For $n = 1000$ and $k = 21$, the exact value is about $0.000953$ and the bound is about $0.000954$. The tail sum formula gives $\mathbb{E}[H] = \sum_{k \ge 1} \Pr(H \ge k) \approx 11.30$, close to $\log_2 1000 \approx 9.97$ plus a small constant.

**Retries.** A client retries a request until it succeeds, and each attempt succeeds with probability $0.9$, independently. The number of attempts $N$ is a random variable with the [geometric distribution](/geometric-distribution/): $\Pr(N = k) = 0.1^{k-1} \cdot 0.9$. The total delay with [exponential backoff](/exponential-backoff/) is another random variable on the same space, a function of $N$.

### Pitfalls

- **The expected value of a maximum is not the maximum of the expected values.** In the skip list above, each $\mathbb{E}[L_i] = 2$, but $\mathbb{E}[\max_i L_i] \approx 11.30$ for $n = 1000$. In general $\mathbb{E}[\max_i X_i] \ge \max_i \mathbb{E}[X_i]$, and the gap can grow with $n$.
- **Equal laws do not make equal variables.** Two variables with the same distribution can differ at every outcome, see [probability distribution](/probability-distribution/). A proof that uses $X = Y$ needs equality as functions, not only equal laws.
- **Name the space.** For a deterministic algorithm on a random input, the running time is a random variable on the space of inputs. For a randomized algorithm on a fixed input, it is a random variable on the space of coin flips. A bound for one is not a bound for the other.

## Where it is used

- **Randomized algorithms.** The running time of a [Las Vegas algorithm](/las-vegas-algorithm/) and the correctness of a [Monte Carlo algorithm](/monte-carlo-algorithm/) are random variables over the coin flips of the algorithm, for each fixed input.
- **Average-case analysis.** In [average-case analysis](/average-case-analysis/), the cost is a random variable over a distribution of inputs, for example the uniform distribution over the $n!$ orders.
- **Hashing.** Chain lengths, probe counts and the number of collisions are random variables over the random choice of the hash function, see [chaining analysis](/chaining-analysis/) and [universal hashing](/universal-hashing/).
- **Data structures.** The depth of a node in a [treap](/treap/) or a [random binary search tree](/random-binary-search-tree/), and the height of a [skip list](/skip-list/), are random variables.
- **The probabilistic method.** To show that an object exists, one shows that a random variable over random objects has positive probability of a good value, see [probabilistic method](/probabilistic-method/).

## References
