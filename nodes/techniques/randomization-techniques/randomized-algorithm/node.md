---
tag: ZA8KYZ
kind: definition
slug: randomized-algorithm
name: Randomized algorithm
aliases:
- probabilistic algorithm
- randomized computation
area: techniques/randomization-techniques
level: intro
summary: An algorithm that draws random bits and whose running time or output varies with those draws.
prereqs: [probability-space, random-variable, expected-value]
see_also: [las-vegas-algorithm, monte-carlo-algorithm, expected-running-time, error-amplification, rp, zpp, bpp, yao-minimax-principle]
sources:
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 1, Introduction (randomized quicksort, Las Vegas and Monte Carlo algorithms, and the model of computation and complexity classes)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 1, Events and Probability (verifying polynomial identities, verifying matrix multiplication, and the randomized min-cut algorithm)
  - paper: doi:10.1137/0206049
    title: John Gill, Computational complexity of probabilistic Turing machines, SIAM Journal on Computing 6(4) (1977)
    locator: pp. 675 to 695 (the probabilistic Turing machine and the classes of zero, one-sided and bounded two-sided error)
---

A randomized algorithm is an algorithm that, in addition to its input, reads a sequence of independent random bits and may use them to choose its next step. For a fixed input, its running time and its output are then random variables, and its guarantees are statements about their distribution over the random bits, not over the inputs. The two main kinds are *Las Vegas* algorithms, whose answer is always correct and whose running time is random, and *Monte Carlo* algorithms, whose running time is bounded and whose answer is wrong with a small probability.

## Definition

A randomized algorithm $A$ is a deterministic algorithm with two inputs: the input $x$ and a string $r = r_1 r_2 \cdots$ of bits, where the $r_i$ are independent and each is 0 or 1 with probability $1/2$. The algorithm reads the bits of $r$ one at a time, as coin flips, when it needs them. In the [word RAM](/word-ram/) or the [random-access machine](/random-access-machine/), a step can also draw a uniform integer in a range; in the [probabilistic Turing machine](/probabilistic-turing-machine/) of Gill, the machine has two transitions in some states and picks one with a fair coin.

For a fixed input $x$, let $A(x)$ be the output and $T_A(x)$ the number of steps. Both are [random variables](/random-variable/) on the [probability space](/probability-space/) of the coin flips. Each probability and each expectation below is over $r$ only, for one fixed $x$, and the bound must hold for every $x$.

- The **expected running time** of $A$ on inputs of size $n$ is $\max_{|x| = n} \mathbb{E}[T_A(x)]$. This is the worst case over the inputs of an average over the coins. See [expected running time](/expected-running-time/).
- $A$ is a **[Las Vegas algorithm](/las-vegas-algorithm/)** for a problem if, for every input $x$, each output it gives is correct, and it stops with probability 1. Its cost is stated as an expected running time or as a bound that holds with high probability. A second, equivalent convention lets it stop in a bounded time and output "don't know" with probability at most $1/2$.
- $A$ is a **[Monte Carlo algorithm](/monte-carlo-algorithm/)** with error $\delta$ if, for every input $x$, it stops within a bound $t(|x|)$ for every $r$, and $\Pr[A(x) \text{ is wrong}] \le \delta$.
- For a decision problem, a Monte Carlo algorithm has **[one-sided error](/one-sided-error/)** if it can err only on the "yes" inputs, and it is always correct on the "no" inputs, or the reverse. It has **[two-sided error](/two-sided-error/)** if it can err on both, with $\delta < 1/2$ on each input.

Polynomial-time bounds give the classes of Gill (1977): [ZPP](/zpp/) for Las Vegas algorithms with expected polynomial time, [RP](/rp/) and [co-RP](/co-rp/) for one-sided error at most $1/2$, and [BPP](/bpp/) for two-sided error at most $1/3$. The constants $1/2$ and $1/3$ do not matter, because of the two facts below.

**Fact 1 (Las Vegas to Monte Carlo).** Let $A$ be a Las Vegas algorithm with expected running time at most $t(n)$. Run $A$ for $2t(n)$ steps and output "don't know" if it has not stopped. The result is correct whenever it answers, stops within $2t(n)$ steps, and says "don't know" with probability at most $1/2$.

*Proof.* $T_A(x) \ge 0$, so [Markov's inequality](/markov-inequality/) gives $\Pr[T_A(x) \ge 2t(n)] \le \mathbb{E}[T_A(x)] / (2t(n)) \le 1/2$. $\square$

Conversely, a Monte Carlo algorithm becomes a Las Vegas one if each answer can be checked: repeat until the check accepts. With success probability $p$ in each run, the number of runs is geometric with mean $1/p$.

**Fact 2 ([error amplification](/error-amplification/), one-sided).** If $A$ has one-sided error at most $\delta$, then $k$ independent runs, with the answer "yes" when some run says "yes", have one-sided error at most $\delta^k$.

*Proof.* On a "no" input, every run says "no", so the combined answer is correct. On a "yes" input, the combined answer is wrong only if all $k$ runs are wrong. The runs use independent bits, so this has probability at most $\delta^k$. $\square$

For two-sided error at most $1/2 - \gamma$, the majority of $k$ runs is wrong with probability at most $e^{-2\gamma^2 k}$, by a [Chernoff bound](/chernoff-bound/) on the number of correct runs.

## Examples and non-examples

- **Randomized quicksort, Las Vegas.** [Randomized quicksort](/randomized-quicksort/) picks each pivot uniformly at random. Its output is always the sorted array. On $n$ distinct keys, the expected number of comparisons is $2(n + 1)H_n - 4n$, for every input order, see [quicksort expected running time](/quicksort-expected-running-time/). For $n = 10$ this is about 24.44. The worst case of 45 comparisons still occurs, when each pivot is the smallest or the largest key of its subarray, but only with probability $\prod_{m=2}^{10} 2/m = 2/14175$, about $1.41 \times 10^{-4}$.
- **Freivalds' algorithm, Monte Carlo with one-sided error.** To test whether $AB = C$ for $n \times n$ matrices, [Freivalds' algorithm](/freivalds-algorithm/) draws $r \in \{0, 1\}^n$ uniformly and checks $A(Br) = Cr$ with $O(n^2)$ operations. If $AB = C$, it always says yes. If $AB \neq C$, let $D = AB - C$ and $d_{ij} \neq 0$. Then $(Dr)_i = d_{ij} r_j + y$, where $y$ does not depend on $r_j$, and for each value of $y$ at most one of the two values of $r_j$ makes it 0. So it wrongly says yes with probability at most $1/2$. The bound is tight: with $A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, $B = \begin{pmatrix} 5 & 6 \\ 7 & 8 \end{pmatrix}$ and $C = \begin{pmatrix} 19 & 22 \\ 43 & 51 \end{pmatrix}$, the product is $\begin{pmatrix} 19 & 22 \\ 43 & 50 \end{pmatrix}$, and the error is found only by the two vectors with $r_2 = 1$. With 20 independent vectors, the error is at most $2^{-20}$ by Fact 2.
- **Miller-Rabin, Monte Carlo with one-sided error.** The [Miller-Rabin test](/miller-rabin-primality-test/) never calls a prime composite, and it calls an odd composite prime with probability at most $1/4$ for each random base. With 20 bases, the error is at most $4^{-20} \approx 9.09 \times 10^{-13}$.
- **Karger's min cut, Monte Carlo with a small success probability.** [Karger's algorithm](/karger-min-cut/) contracts random edges until two vertices are left, and returns a given minimum cut with probability at least $2/(n(n - 1))$. For $n = 10$, this is $1/45$. Since the answers can be compared, keep the smallest cut over $t$ runs: it fails with probability at most $(1 - 1/45)^t$, which is below $10^{-3}$ for $t = 311$.
- **Non-example: a deterministic algorithm on random inputs.** Deterministic quicksort with the first element as pivot does $2(n + 1)H_n - 4n$ comparisons on average over a uniformly random input order. This is [average-case analysis](/average-case-analysis/), not randomization: the algorithm draws no bits, and an adversary that knows it can choose a sorted input and force $n(n - 1)/2$ comparisons each time.
- **Non-example: a fixed seed.** A program that calls a [pseudorandom generator](/pseudorandom-generator/) with a seed fixed in the code is deterministic. It has one fixed run on each input, so its worst case is the worst case over the inputs, and the probability bounds above do not apply. They apply in practice only if the seed is unknown to whoever chooses the input.
- **Non-example: a heuristic that fails on some input every time.** An algorithm whose error on a bad input is close to 1 is not Monte Carlo with error $\delta < 1/2$, even if it is wrong only on a small fraction of the inputs. The bound $\delta$ must hold for each input.

## Related definitions

- **Deterministic algorithm.** The special case that reads no random bits. Its output and time are fixed for each input.
- **[Expected running time](/expected-running-time/)** and **bounds with high probability.** Two ways to state the cost of a Las Vegas algorithm: a bound on $\mathbb{E}[T]$, or a bound $\Pr[T > c\, t(n)] \le n^{-\alpha}$. Tail bounds such as [Markov](/markov-inequality/) and [Chernoff](/chernoff-bound/) connect them.
- **[Yao's minimax principle](/yao-minimax-principle/).** The expected cost of the best Las Vegas algorithm on its worst input is at least the average cost of the best deterministic algorithm on any fixed distribution of inputs. It is the standard tool for lower bounds on randomized algorithms.
- **[Las Vegas to Monte Carlo conversion](/las-vegas-to-monte-carlo-conversion/).** Fact 1 and its converse with a checker.
- **Randomized techniques.** [Linearity of expectation](/linearity-of-expectation/) with [indicator random variables](/indicator-random-variable/) is the main tool of the analysis. [Randomized incremental construction](/randomized-incremental-construction/), [backwards analysis](/backwards-analysis/), random sampling and [universal hashing](/universal-hashing/) are common designs, and the [probabilistic method](/probabilistic-method/) uses the same reasoning to prove that objects exist.

## References
