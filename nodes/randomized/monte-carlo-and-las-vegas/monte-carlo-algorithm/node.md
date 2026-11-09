---
tag: 2XRTQG
kind: definition
slug: monte-carlo-algorithm
name: Monte Carlo algorithm
aliases:
- Monte Carlo method
area: randomized/monte-carlo-and-las-vegas
level: intro
summary: A randomized algorithm with a running time bounded on every input and every outcome of its coins, whose answer may be wrong with a probability that is bounded on every input.
prereqs: [randomized-algorithm, probability-space, expected-value]
see_also: [las-vegas-algorithm, las-vegas-to-monte-carlo-conversion, one-sided-error, two-sided-error, error-amplification, freivalds-algorithm, miller-rabin-primality-test, karger-min-cut]
sources:
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 1, Section 1.2 (Las Vegas and Monte Carlo), and Section 1.5 (the complexity classes RP, ZPP, PP and BPP)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 1 (verifying polynomial identities, verifying matrix multiplication, the randomized min-cut algorithm)
  - url: "https://people.cs.uchicago.edu/~laci/lasvegas79.pdf"
    title: Laszlo Babai, Monte-Carlo algorithms in graph isomorphism testing, Universite de Montreal, Technical Report D.M.S. 79-10, 1979
    locator: the section Monte Carlo or Las Vegas? (the two terms and the remark that each Las Vegas computation is a Monte Carlo computation)
  - paper: doi:10.1080/01621459.1949.10483310
    title: Nicholas Metropolis and Stanislaw Ulam, The Monte Carlo method, Journal of the American Statistical Association 44(247), 1949
    locator: pages 335 to 341 (the name Monte Carlo for computation by random sampling)
---

A Monte Carlo algorithm is a [randomized algorithm](/randomized-algorithm/) that stops within a fixed time bound on every input and for every outcome of its random choices, but whose output may be wrong with some probability $\delta$, and this bound on the error holds for every input. It trades certainty of the answer for a guaranteed running time. The opposite trade is a [Las Vegas algorithm](/las-vegas-algorithm/), which is never wrong but whose running time is random. [Freivalds' algorithm](/freivalds-algorithm/), the [Miller-Rabin test](/miller-rabin-primality-test/) and [Karger's minimum cut algorithm](/karger-min-cut/) are standard examples.

## Definition

Notation on this page: $n$ is the input size, $\delta$ is the error (failure) probability, and $\Pr$ and $\mathbb{E}$ are taken over the random choices of the algorithm only, for one fixed input. The algorithm reads uniform random bits; a uniform integer in a range is made from bits, with rejection when the size of the range is not a power of 2.

A problem gives, for each input $x$, a nonempty set $\mathrm{Sol}(x)$ of correct outputs. For a decision problem, $\mathrm{Sol}(x)$ is the single answer "yes" or "no". Let $A(x, r)$ be the output of a randomized algorithm $A$ on input $x$ with random string $r$, and $T_A(x, r)$ its number of steps.

$A$ is a **Monte Carlo algorithm** with time bound $t(n)$ and error $\delta(n)$ if both conditions hold:

1. **Bounded time.** For every input $x$ with $|x| = n$ and for every random string $r$, $T_A(x, r) \le t(n)$.
2. **Bounded error.** For every input $x$ with $|x| = n$, $\Pr_r[A(x, r) \notin \mathrm{Sol}(x)] \le \delta(n)$.

The quantifiers are in this order: for each input, a probability over the coins. A bound on the error averaged over the inputs is not enough.

### The size of the error

- For a decision problem, the usual condition is $\delta \le c$ for a constant $c < 1/2$ when the algorithm can be wrong on both answers ([two-sided error](/two-sided-error/)). When it can be wrong on only one answer ([one-sided error](/one-sided-error/)), any constant $c < 1$ is enough. In both cases, [error amplification](/error-amplification/) makes the error as small as needed by independent repetition, so the constant does not matter.
- For a search or optimization problem, the success probability $1 - \delta$ can be small, for example $2/(n(n - 1))$ for one run of Karger's contraction. Such an algorithm is useful when the outputs of several runs can be compared (keep the smallest cut) or checked.
- $\delta$ may depend on $n$. A bound such as $\delta \le n^{-c}$ for a constant $c > 0$ is a bound *with high probability*.

### Relation to Las Vegas

A Las Vegas algorithm that also has a worst-case time bound is a Monte Carlo algorithm with $\delta = 0$. A Las Vegas algorithm with only an expected time bound $t(n)$ becomes a Monte Carlo algorithm when it is stopped after $2t(n)$ steps: by [Markov's inequality](/markov-inequality/) it has not stopped with probability at most $1/2$. The reverse direction needs a way to check an answer. Both directions are on the page [Las Vegas to Monte Carlo conversion](/las-vegas-to-monte-carlo-conversion/).

### The name

Metropolis and Ulam (1949) used the name *Monte Carlo method* for computation by random sampling, after the casino. Babai (1979) proposed the term *Las Vegas* for randomized algorithms whose answers are always correct, and kept *Monte Carlo* for algorithms such as the Solovay-Strassen test, which may be wrong. In numerical work, "Monte Carlo method" still means estimation by random sampling, as in [Monte Carlo integration](/monte-carlo-integration/). Such an estimator is a Monte Carlo algorithm in the sense of this page when "wrong" means "farther than $\varepsilon$ from the true value".

## Examples and non-examples

- **Freivalds' algorithm.** To test $AB = C$ for $n \times n$ matrices, [Freivalds' algorithm](/freivalds-algorithm/) draws $r \in \{0, 1\}^n$ and compares $A(Br)$ with $Cr$, in $O(n^2)$ time for every $r$. If $AB = C$ it always says "equal". If $AB \ne C$ it says "equal" with probability at most $1/2$. With 20 independent vectors, the error is at most $2^{-20} \approx 9.54 \times 10^{-7}$.
- **Miller-Rabin.** One round of the [Miller-Rabin test](/miller-rabin-primality-test/) uses $O(\log n)$ multiplications modulo the input number $N$ (here $n$ is the number of digits), for every base. A prime always passes. An odd composite passes with probability at most $1/4$. On the [Carmichael number](/carmichael-number/) $561$, a base drawn from $\{2, \ldots, 559\}$ is a strong liar with probability $8/558 \approx 0.0143$.
- **Karger's contraction.** One run of [Karger's algorithm](/karger-min-cut/) on a graph with $10$ vertices returns a minimum cut with probability at least $2/(10 \cdot 9) = 1/45$. Its error is at most $44/45$, which is close to 1, but the smallest cut of $311$ independent runs is wrong with probability at most $(44/45)^{311} < 10^{-3}$.
- **Polynomial identity testing.** To test whether a polynomial of total degree $d$ is identically zero, evaluate it at a point drawn from $S^m$ for a finite set $S$ of field elements. By the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), a nonzero polynomial gives 0 with probability at most $d/|S|$. See [polynomial identity testing](/polynomial-identity-testing/).
- **Monte Carlo estimation.** To estimate the mean $\mu$ of a random variable with values in $[0, 1]$ to within $\varepsilon$, average $s$ samples. By [Hoeffding's inequality](/hoeffding-inequality/), the estimate is farther than $\varepsilon$ from $\mu$ with probability at most $2e^{-2s\varepsilon^2}$. For $\varepsilon = 0.01$ and $\delta = 0.05$, $s = \lceil \ln(2/\delta)/(2\varepsilon^2) \rceil = 18445$ samples are enough.
- **Non-example: randomized quicksort as a "Monte Carlo" sort.** [Randomized quicksort](/randomized-quicksort/) is never wrong. It is a Las Vegas algorithm. Its worst case of $n(n-1)/2$ comparisons holds for every random string, so it is also a Monte Carlo algorithm with $\delta = 0$, but this name says nothing useful about it.
- **Non-example: the Fermat test.** The [Fermat test](/fermat-primality-test/) with a random base has no error bound $\delta < 1$ that holds on every input. On a Carmichael number $N$, each base coprime to $N$ passes. For $N = 561$, $1105$, $1729$ and $8911$, a base drawn from $\{2, \ldots, N - 2\}$ passes with probability $0.570$, $0.695$, $0.750$ and $0.800$, and the probability is $\varphi(N)/N$ up to a small term, which comes close to 1 for Carmichael numbers whose prime factors are all large.
- **Non-example: a deterministic algorithm that is wrong on rare inputs.** Its error on a bad input is 1, not a small probability. The bound must hold for each input, not for most inputs.
- **Non-example: a fixed seed.** A program that seeds its [pseudorandom generator](/pseudorandom-generator/) with a constant is deterministic. Each input then has one fixed run, so an input that makes it fail makes it fail each time.

## Related definitions

- **[Las Vegas algorithm](/las-vegas-algorithm/).** Never wrong; the running time is a random variable. Every Las Vegas algorithm with a worst-case time bound is a Monte Carlo algorithm with zero error.
- **[One-sided error](/one-sided-error/)** and **[two-sided error](/two-sided-error/).** The two kinds of error of a Monte Carlo algorithm for a decision problem. They define the classes [RP](/rp/) and [co-RP](/co-rp/), and [BPP](/bpp/), in polynomial time. Las Vegas algorithms in expected polynomial time define [ZPP](/zpp/).
- **[Error amplification](/error-amplification/).** Repetition with an OR of the answers for one-sided error, or with a majority vote for two-sided error.
- **[Las Vegas to Monte Carlo conversion](/las-vegas-to-monte-carlo-conversion/).** A time cut-off and Markov's inequality in one direction, a verifier and repetition in the other.
- **[Probabilistic Turing machine](/probabilistic-turing-machine/).** The machine model of the classes RP, BPP and ZPP.
- **[Monte Carlo integration](/monte-carlo-integration/).** The numerical method that gave the name, with an error in value instead of an error in a yes or no answer.

## References
