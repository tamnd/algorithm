---
tag: AWYECR
kind: concept
slug: indicator-random-variable
name: Indicator random variable
aliases:
- indicator variable
area: foundations/probabilistic-analysis
level: intro
summary: A 0/1 variable whose expectation is the probability of an event; combined with linearity to count events.
prereqs: [probability-space, random-variable, expected-value]
see_also: [linearity-of-expectation, hiring-problem, expected-number-of-inversions, quicksort-expected-running-time, birthday-paradox, balls-into-bins, variance, independent-random-variables]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 5.2, Indicator random variables (the lemma E[X_A] = Pr{A} and the analysis of the hiring problem); Section 5.4 (birthday paradox, balls and bins, streaks); Problem 2-4 and the exercises of Section 5.2 (inversions)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.1 (random variables and expectation), Section 2.2 (Bernoulli and binomial random variables), Section 2.5 (the expected run-time of quicksort)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (the analysis of RandQS with indicator variables); Chapter 3, Section 3.1 (occupancy problems)
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter IX, Random Variables; Expectation
---

An indicator random variable $I\{A\}$ is the [random variable](/random-variable/) that is $1$ when the event $A$ occurs and $0$ when it does not. Its [expected value](/expected-value/) is the probability of the event: $\mathrm{E}[I\{A\}] = \Pr[A]$. A count of events is a sum of indicators, so with [linearity of expectation](/linearity-of-expectation/) the expected count is the sum of the probabilities, even when the events depend on each other. This is the standard way to find the expected cost of a randomized algorithm, as in the [hiring problem](/hiring-problem/) and [randomized quicksort](/quicksort-expected-running-time/).

## In plain words

An indicator is a switch that is on when a thing happens and off when it does not. Its average value over many runs is the fraction of runs in which the thing happens, which is the chance of the thing.

Many costs of an algorithm are counts: how many times a line runs, how many pairs it compares, how many items it moves. Split the count into one switch for each place where the thing can happen. The average count is then the sum of the chances of each switch. You do not need to know how the switches affect each other. Each chance is often easy, for example "the third item is the largest of the first three", which happens one time in three.

## The idea

Let $(\Omega, \Pr)$ be a discrete [probability space](/probability-space/) and let $A \subseteq \Omega$ be an event. The indicator random variable of $A$ is

$$ I\{A\}(\omega) = \begin{cases} 1 & \text{if } \omega \in A, \\ 0 & \text{if } \omega \notin A. \end{cases} $$

CLRS writes $X_A$ for $I\{A\}$. Other books write $\mathbf{1}_A$.

**Lemma.** $\mathrm{E}[I\{A\}] = \Pr[A]$.

*Proof.* $I\{A\}$ takes only the values $0$ and $1$, and it is $1$ exactly on $A$. By the definition of expectation, $\mathrm{E}[I\{A\}] = 1 \cdot \Pr[I\{A\} = 1] + 0 \cdot \Pr[I\{A\} = 0] = \Pr[A]$. $\square$

So an indicator is a [Bernoulli](/bernoulli-trials/) random variable with parameter $p = \Pr[A]$, and each Bernoulli variable is the indicator of the event that it equals $1$.

### The algebra of indicators

These identities hold at each outcome $\omega$, so they hold as equalities of random variables. Each one follows from a check of the cases $\omega \in A$ and $\omega \notin A$ (and the same for $B$).

- **Complement.** $I\{\bar A\} = 1 - I\{A\}$, so $\Pr[\bar A] = 1 - \Pr[A]$.
- **Intersection.** $I\{A \cap B\} = I\{A\}\, I\{B\}$. In particular $I\{A\}^2 = I\{A\}$.
- **Union.** $I\{A \cup B\} = I\{A\} + I\{B\} - I\{A\}\,I\{B\}$, and for $n$ events $I\{A_1 \cup \cdots \cup A_n\} = 1 - \prod_{i=1}^{n} (1 - I\{A_i\})$. Taking expectations of the expanded product gives the inclusion-exclusion formula.
- **Union bound.** $I\{A_1 \cup \cdots \cup A_n\} \le \sum_i I\{A_i\}$, because the left side is $1$ only when at least one term on the right is $1$. Taking expectations gives the [union bound](/union-bound/).
- **Markov.** For a random variable $X \ge 0$ and $a > 0$, $I\{X \ge a\} \le X/a$ at each outcome. Taking expectations gives [Markov's inequality](/markov-inequality/) $\Pr[X \ge a] \le \mathrm{E}[X]/a$.
- **Variance.** Since $I\{A\}^2 = I\{A\}$, $\mathrm{E}[I\{A\}^2] = p$ and $\mathrm{Var}[I\{A\}] = p - p^2 = p(1-p)$, where $p = \Pr[A]$. See [variance](/variance/).

### The counting method

Let $X$ be the number of events among $A_1, \ldots, A_n$ that occur. Then $X = \sum_{i=1}^{n} I\{A_i\}$ at each outcome, and by [linearity of expectation](/linearity-of-expectation/)

$$ \mathrm{E}[X] = \sum_{i=1}^{n} \mathrm{E}[I\{A_i\}] = \sum_{i=1}^{n} \Pr[A_i]. $$

The events $A_i$ may be dependent. Linearity needs no [independence](/independent-random-variables/). The method has three steps:

1. Write the cost as a count, and name one event for each unit that the count can add.
2. Find the probability of each event. Symmetry often gives it directly.
3. Add the probabilities, and find a closed form or an asymptotic form of the sum.

## Examples

### The hiring problem

In the [hiring problem](/hiring-problem/), $n$ candidates arrive in a uniformly random order, and we hire a candidate when they are better than each earlier candidate. Assume that the ranks are distinct, so the arrival order is a [uniform](/uniform-distribution/) random permutation of the ranks. Let $A_i$ be the event that candidate $i$ is hired, and $X = \sum_{i=1}^n I\{A_i\}$ the number of hires.

Candidate $i$ is hired exactly when they are the best of the first $i$ candidates. In a uniform random permutation, the relative order of the first $i$ candidates is uniform over the $i!$ orders, so each of the $i$ is the best of them with probability $1/i$. So $\Pr[A_i] = 1/i$ and

$$ \mathrm{E}[X] = \sum_{i=1}^{n} \frac{1}{i} = H_n = \ln n + O(1), $$

where $H_n$ is the $n$th [harmonic number](/harmonic-series/). The expected hiring cost is $c_h H_n = O(c_h \ln n)$, against $c_h n$ in the worst case. For $n = 5$ the expected number of hires is $H_5 = 137/60 \approx 2.283$, which is also the average over all $120$ orders. For $n = 10$, $100$ and $1000$ it is $2.929$, $5.187$ and $7.485$. The events $A_i$ here are in fact mutually independent, which the [variance](/variance/) page uses, but the expectation does not need that.

### Inversions of a random permutation

An [inversion](/inversion/) of an array $A[1..n]$ is a pair $(i, j)$ with $i < j$ and $A[i] > A[j]$. Let the array hold a uniform random permutation of $n$ distinct keys. For each of the $\binom{n}{2}$ pairs $i < j$, let $X_{ij} = I\{A[i] > A[j]\}$. Swapping the keys at positions $i$ and $j$ is a bijection of the permutations that maps the event $A[i] > A[j]$ to its complement, so $\Pr[A[i] > A[j]] = 1/2$. Hence the number of inversions $X = \sum_{i<j} X_{ij}$ has

$$ \mathrm{E}[X] = \binom{n}{2} \cdot \frac12 = \frac{n(n-1)}{4}. $$

For $n = 4$, $5$ and $6$ the averages over all permutations are $3$, $5$ and $7.5$. For $n = 10$ the mean is $22.5$, and for $n = 100$ it is $2475$. The indicators $X_{ij}$ are not independent: for example $X_{12} = 1$ and $X_{23} = 1$ force $X_{13} = 1$. The expectation is right anyway.

[Insertion sort](/insertion-sort/) moves an item one place for each inversion, so on a random input it makes $n(n-1)/4$ moves on average, and its average time is $\Theta(n^2)$. The page on the [expected number of inversions](/expected-number-of-inversions/) has more on this count.

### Shared birthdays

Put $k$ people in a room, each with a birthday chosen uniformly and independently from $m$ days. For each pair $\{i, j\}$, let $X_{ij}$ be the indicator that $i$ and $j$ share a birthday. Then $\Pr[X_{ij} = 1] = 1/m$, and the expected number of pairs that share a birthday is $\binom{k}{2}/m$. With $k = 23$ and $m = 365$ this is $253/365 \approx 0.693$. This is the indicator analysis of the [birthday paradox](/birthday-paradox/) in CLRS Section 5.4.

### Empty bins

Throw $m$ balls into $n$ bins, each ball into a uniform random bin, independently. Let $E_j$ be the event that bin $j$ stays empty. Then $\Pr[E_j] = (1 - 1/n)^m$, and the expected number of empty bins is $n(1 - 1/n)^m$. With $n = m = 10$ this is $10 \cdot 0.9^{10} \approx 3.487$. For $m = n$ large, the fraction of empty bins tends to $1/e \approx 0.368$. See [balls into bins](/balls-into-bins/).

### Pitfalls

- **Expectation is not probability.** In the birthday example the expected number of shared pairs is $0.693$, but the probability of at least one shared pair is $0.507$. An expected count of at least $1$ does not give a probability of at least $1/2$ that the count is positive. To bound that probability, use the [second moment](/chebyshev-inequality/) or compute it directly.
- **Dependent indicators and variance.** Linearity gives the mean of a sum of dependent indicators, but not its variance. $\mathrm{Var}[\sum_i I\{A_i\}] = \sum_i \mathrm{Var}[I\{A_i\}]$ needs the indicators to be pairwise uncorrelated. For inversions the covariances are not zero. See [variance](/variance/).
- **Count each unit once.** In a count of pairs, use one indicator for each unordered pair $i < j$. An indicator for each ordered pair counts each pair twice.
- **Name the event exactly.** In the hiring problem the event is "candidate $i$ is the best of the first $i$", not "candidate $i$ is better than candidate $i-1$". The second event has probability $1/2$ and gives the wrong answer $1 + (n-1)/2$.
- **The random model.** The probabilities come from a model: a random input order (probabilistic analysis) or the random choices of the algorithm (a [randomized algorithm](/randomized-algorithm/)). The hiring result $H_n$ is wrong for an adversarial order unless the algorithm shuffles the input first.

## Where it is used

- **Average-case analysis.** The [hiring problem](/hiring-problem/), [insertion sort](/insertion-sort/) on a random input through [inversions](/expected-number-of-inversions/), and [average-case analysis](/average-case-analysis/) in general.
- **Randomized algorithms.** The expected number of comparisons of [randomized quicksort](/quicksort-expected-running-time/) is a sum of one indicator for each pair of keys, with probability $2/(j - i + 1)$. The derivation is on the page of [linearity of expectation](/linearity-of-expectation/). The same method gives the linear expected time of [quickselect](/quickselect-expected-linear/) and the expected depth of a node in a [random binary search tree](/random-bst-expected-depth/).
- **Hashing.** The expected length of a chain under [simple uniform hashing](/simple-uniform-hashing/) or a [universal hash family](/universal-hash-family/) is a sum of indicators of collisions.
- **Occupancy problems.** [Balls into bins](/balls-into-bins/), the [birthday paradox](/birthday-paradox/), the [coupon collector problem](/coupon-collector-problem/) and [streaks](/streaks/).
- **The probabilistic method.** The expected number of satisfied clauses of a [random assignment](/random-assignment-max-3-sat/) is $7m/8$ for $m$ clauses each with three literals on distinct variables, so some assignment satisfies at least that many.
- **Tail bounds.** A sum of independent indicators is a sum of Bernoulli trials, the setting of the [Chernoff bound](/chernoff-bound/) and of the [binomial distribution](/binomial-distribution/).

## References
