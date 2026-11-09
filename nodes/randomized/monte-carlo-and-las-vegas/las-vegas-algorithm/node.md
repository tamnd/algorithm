---
tag: CCAFYB
kind: definition
slug: las-vegas-algorithm
name: Las Vegas algorithm
aliases:
- zero-error randomized algorithm
area: randomized/monte-carlo-and-las-vegas
level: intro
summary: A randomized algorithm that always returns a correct answer, with only the running time being random.
prereqs: [randomized-algorithm, expected-value, geometric-distribution]
see_also: [monte-carlo-algorithm, las-vegas-to-monte-carlo-conversion, randomized-quicksort, expected-running-time, zpp, one-sided-error, yao-minimax-principle, markov-inequality]
sources:
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 1, Section 1.2 (Las Vegas and Monte Carlo) and Section 1.5 (ZPP and its relation to RP and co-RP)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 2 (the expected running time of randomized quicksort, with indicator random variables)
  - url: "https://people.cs.uchicago.edu/~laci/lasvegas79.pdf"
    title: Laszlo Babai, Monte-Carlo algorithms in graph isomorphism testing, Universite de Montreal, Technical Report D.M.S. 79-10, 1979
    locator: the section Monte Carlo or Las Vegas? (the proposal of the term Las Vegas)
  - paper: doi:10.1090/S0025-5718-1990-1023756-8
    title: Eric Bach, Explicit bounds for primality testing and related problems, Mathematics of Computation 55(191), 1990
    locator: pages 355 to 380 (under the extended Riemann hypothesis, a proper subgroup of the units modulo m omits a number below 2 (ln m)^2)
---

A Las Vegas algorithm is a [randomized algorithm](/randomized-algorithm/) that never gives a wrong answer: on every input, each output it gives is correct, and only its running time depends on the random choices. Its cost is stated as an [expected running time](/expected-running-time/), or as a time bound that holds with high probability. [Randomized quicksort](/randomized-quicksort/) is the standard example. A [Monte Carlo algorithm](/monte-carlo-algorithm/) makes the opposite trade: a fixed time bound and a small probability of a wrong answer.

## Definition

Notation on this page: $n$ is the input size, $\delta$ is a failure probability, and $\Pr$ and $\mathbb{E}$ are taken over the random choices of the algorithm only, for one fixed input. The algorithm reads uniform random bits.

A problem gives, for each input $x$, a nonempty set $\mathrm{Sol}(x)$ of correct outputs. Let $A(x, r)$ be the output of a randomized algorithm $A$ on input $x$ with random string $r$, and $T_A(x, r)$ its number of steps.

$A$ is a **Las Vegas algorithm** with expected time $t(n)$ if, for every input $x$ with $|x| = n$:

1. **No error.** For every random string $r$ on which $A$ stops, $A(x, r) \in \mathrm{Sol}(x)$.
2. **Expected time.** $\mathbb{E}_r[T_A(x, r)] \le t(n)$. In particular $A$ stops with probability 1.

The expectation is over the coins for one fixed input, and the bound must hold for the worst input. It is not an average over inputs.

### The second convention: bounded time and "don't know"

Some books use a different but equivalent form. $A$ stops within $t(n)$ steps for every $r$, and outputs either a correct answer or the symbol $\bot$ ("don't know"), with $\Pr_r[A(x, r) = \bot] \le 1/2$ for every $x$. The two forms convert into each other with a constant factor in time:

- **From $\bot$ to expected time.** Repeat $A$ with fresh random bits until it gives an answer. The runs are independent, each gives an answer with probability $p \ge 1/2$, so the number of runs has the [geometric distribution](/geometric-distribution/) with mean $1/p \le 2$. The expected time is at most $2t(n)$, and the answer is always correct.
- **From expected time to $\bot$.** Stop $A$ after $2t(n)$ steps and output $\bot$ if it has not stopped. By [Markov's inequality](/markov-inequality/), $\Pr[T_A \ge 2t(n)] \le 1/2$. The proof and the general cut-off are on the page [Las Vegas to Monte Carlo conversion](/las-vegas-to-monte-carlo-conversion/).

### Expected time and tail bounds

An expected time bound alone allows long runs. Markov's inequality gives only $\Pr[T_A > c\,t(n)] \le 1/c$. Many Las Vegas algorithms have much stronger tails. For an algorithm that repeats an independent trial with success probability $p$ until success, $\Pr[\text{more than } k \text{ trials}] = (1 - p)^k$. Randomized quicksort makes $O(n \log n)$ comparisons with probability at least $1 - n^{-c}$ for each constant $c$, with the constant of the $O$ depending on $c$. A bound of this kind is stated with its probability, as a bound *with high probability*.

## Examples and non-examples

- **Randomized quicksort.** [Randomized quicksort](/randomized-quicksort/) picks each pivot uniformly at random, and its output is always sorted. On $n$ distinct keys it makes $2(n + 1)H_n - 4n$ comparisons in expectation, for every input order, see [quicksort expected running time](/quicksort-expected-running-time/). For $n = 10$ this is about $24.44$. The worst case, 45 comparisons, happens only when each pivot is the smallest or the largest key of its part, with probability $\prod_{m=2}^{10} 2/m = 2/14175$.
- **A quadratic non-residue modulo a prime.** For an odd prime $p$, draw $a$ uniformly from $\{1, \ldots, p - 1\}$ and test $a^{(p-1)/2} \equiv -1 \pmod p$ by [Euler's criterion](/euler-criterion/). Exactly $(p - 1)/2$ of the candidates are non-residues, so each trial succeeds with probability exactly $1/2$, the expected number of trials is 2, and more than $k$ trials happen with probability $2^{-k}$. The answer is checked before it is returned, so it is never wrong. For $p = 41$, the non-residues are 20 of the 40 candidates, and the least one is 3. No deterministic polynomial-time method is known without an unproved hypothesis; under the extended Riemann hypothesis, the least non-residue is below $2(\ln p)^2$ (Bach 1990).
- **Search in a half-full array.** An array of $n$ bits has at least $n/2$ ones. Probe uniform random positions until a 1 appears. The expected number of probes is at most 2 on every array, while a deterministic method needs $n/2 + 1$ probes in the worst case.
- **[Randomized quickselect](/randomized-quickselect/).** It finds the $k$-th smallest of $n$ keys in expected $O(n)$ time on every input, and its answer is always correct.
- **Non-example: Miller-Rabin.** The [Miller-Rabin test](/miller-rabin-primality-test/) can call a composite number prime. It is a Monte Carlo algorithm with one-sided error.
- **Non-example: Karger's contraction.** One run of [Karger's algorithm](/karger-min-cut/) can return a cut that is not minimum. The algorithm has no fast way to tell, so it is not Las Vegas.
- **Non-example: deterministic quicksort on a random input.** It draws no random bits. Its average of $2(n + 1)H_n - 4n$ comparisons is over a distribution of inputs, and a sorted input makes it use $n(n - 1)/2$ comparisons each time.

## Related definitions

- **[Monte Carlo algorithm](/monte-carlo-algorithm/).** Fixed time, bounded error. A Las Vegas algorithm with a worst-case time bound is a Monte Carlo algorithm with zero error.
- **[Las Vegas to Monte Carlo conversion](/las-vegas-to-monte-carlo-conversion/).** Stopping at a cut-off turns Las Vegas into Monte Carlo; the reverse needs a verifier for the answers.
- **[ZPP](/zpp/).** The decision problems with a Las Vegas algorithm in expected polynomial time. ZPP equals [RP](/rp/) $\cap$ [co-RP](/co-rp/): an algorithm with [one-sided error](/one-sided-error/) for each side gives a Las Vegas algorithm.
- **[Expected running time](/expected-running-time/).** The cost measure of a Las Vegas algorithm, a worst case over the inputs of an expectation over the coins.
- **[Yao's minimax principle](/yao-minimax-principle/).** The expected cost of the best Las Vegas algorithm on its worst input is at least the average cost of the best deterministic algorithm on any fixed input distribution. It gives lower bounds for Las Vegas algorithms.
- **Name.** Babai (1979) proposed the term *Las Vegas* for randomized algorithms whose answers are always correct, as a stronger kind of Monte Carlo algorithm.

## References
