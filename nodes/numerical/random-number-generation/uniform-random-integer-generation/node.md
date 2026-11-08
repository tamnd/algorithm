---
tag: JCPEKE
kind: problem
slug: uniform-random-integer-generation
name: Uniform random integer generation
aliases:
- bounded random integers
- random integer in a range
- dice rolling from random words
area: numerical/random-number-generation
level: intro
summary: Producing an integer uniformly from a range [0, n) given uniform random words.
model: word-ram
prereqs: [uniform-distribution, pseudorandom-number-generator, geometric-distribution]
see_also: [modulo-bias, lemire-bounded-integers, fisher-yates-shuffle, rejection-sampling, unbiased-bits-from-biased-coin, random-variate-generation]
sources:
  - paper: doi:10.1145/3230636
    title: Daniel Lemire, Fast random integer generation in an interval, ACM Transactions on Modeling and Computer Simulation 29(1), article 3, 2019
    locator: Section 2 (the modulo and the rejection methods and their bias), Section 3 (the nearly divisionless algorithm, its proof of exactness and the probability n/2^L that it divides)
  - paper: "Donald E. Knuth and Andrew C. Yao, The complexity of nonuniform random number generation, in Algorithms and Complexity, New Directions and Recent Results, J. F. Traub (editor), Academic Press, 1976, pages 357 to 428"
    locator: the discrete distribution generating trees and the bound H(X) <= E[number of bits] < H(X) + 2 for an optimal tree
  - paper: "Jérémie Lumbroso, Optimal discrete uniform generation from coin flips, and applications, arXiv:1304.1916, 2013"
    locator: the Fast Dice Roller algorithm, its exactness and its expected number of flips at most log2(n) + 2
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.1 (choosing an integer in a range from a uniform number, and the warning about the low bits) and Section 3.4.2 (random sampling and shuffling)
  - url: https://luc.devroye.org/rnbookindex.html
    title: Luc Devroye, Non-Uniform Random Variate Generation, Springer, 1986 (free online edition)
    locator: Chapter XV, The random bit model (the Knuth-Yao trees and the entropy bounds)
---

Uniform random integer generation is the problem of producing an integer $X$ with $\Pr[X = k] = 1/n$ for each $k \in \{0, \ldots, n-1\}$, given a source of independent uniform random words or bits. The easy answer, the remainder of a random word modulo $n$, is biased when $n$ does not divide $2^w$ (see [modulo bias](/modulo-bias/)). An exact method must reject some inputs, so its number of input words has no fixed upper bound unless $n$ is a power of two. Rejection with one multiplication ([Lemire's method](/lemire-bounded-integers/)) is the standard fast exact solution.

## In plain words

You want to roll a fair die with six faces, but all you have is a source of random numbers from 0 to 255. Taking the remainder after division by six does not work: 256 is not a multiple of six, so four faces come up a little more often than the other two.

The fix is to throw away some numbers. Use only the numbers from 0 to 251, which split into six groups of the same size, and ask again when you get 252 or more. This is fair, and you almost never need a second try.

There is no fair method that always stops after a fixed number of tries when the number of faces is not a power of two. The thrown-away cases are the price of fairness.

## Definition

**Input.** An integer $n$ with $1 \le n \le 2^w$, and access to a source that returns independent words $x_1, x_2, \ldots$, each uniform on $\{0, 1, \ldots, 2^w - 1\}$. In the bit version, $w = 1$ and the source is a fair coin.

**Output.** An integer $X \in \{0, \ldots, n - 1\}$ with

$$\Pr[X = k] = \frac{1}{n} \qquad \text{for each } k \in \{0, \ldots, n - 1\}.$$

The algorithm must stop with probability 1.

**Cost.** The number $N$ of source words (or bits) that it reads, a random variable, and the number of word operations, with divisions counted apart because they are much slower than multiplications on current processors. We measure $\mathbb{E}[N]$ and the expected number of divisions.

In practice the source is a [pseudorandom number generator](/pseudorandom-number-generator/), and "uniform" means that the method is exact for a truly uniform source. A method that is exact for a uniform source adds no defect of its own.

## Variants

- **A range $[a, b]$.** Solve the problem for $n = b - a + 1$ and add $a$. The full range $n = 2^w$ needs no work: return the word.
- **Bits instead of words.** The source is a fair coin, and the cost is the expected number of flips. This is the setting of Knuth and Yao (1976).
- **Large $n$.** For $n > 2^w$, build a word of $kw$ bits from $k$ source words and apply the same method.
- **Many draws for one $n$.** When $n$ is fixed for many draws, the threshold $2^w \bmod n$ can be computed once.
- **Approximate versions.** Some uses accept a bias below a stated bound, for example $\lfloor x n / 2^w \rfloor$ with a 64-bit word and $n < 2^{32}$, whose bias is at most $n / 2^{64}$ for each value.
- **Floating-point methods.** $\lfloor n U \rfloor$ for a float $U$ in $[0, 1)$ is exact only if $U$ is a uniform multiple of $2^{-k}$ with $n \mid 2^k$; in floating point it can also round up to $n$. It is a source of bias in old code.

## Examples

**A die from a byte, $n = 6$, $w = 8$.** $256 = 6 \cdot 42 + 4$.

- *Modulo:* $x \bmod 6$ gives 0, 1, 2 and 3 with probability $43/256$ each, and 4 and 5 with probability $42/256$ each.
- *Rejection by threshold:* accept $x < 252$ and return $x \bmod 6$. Each value has probability $42/252 = 1/6$. A word is rejected with probability $4/256$, so $\mathbb{E}[N] = 256/252 \approx 1.016$.
- *Lemire's method:* compute $p = 6x$ as a 16-bit product, with high part $\lfloor p / 256 \rfloor$ and low part $\ell = p \bmod 256$. Reject when $\ell < t = (256 - 6) \bmod 6 = 4$. For $x = 200$, $p = 1200$, the high part is 4 and $\ell = 176 \ge 4$, so the output is 4. Over all 256 words, 252 are accepted, and each output value comes from exactly 42 of them. A division to compute $t$ is needed only when $\ell < 6$, which happens for 6 of the 256 words.

**Other ranges with $w = 8$.**

| $n$ | $256 \bmod n$ | words accepted | $\mathbb{E}[N]$ | modulo counts |
|---|---|---|---|---|
| 1 | 0 | 256 | 1 | 256 |
| 6 | 4 | 252 | $256/252$ | 42 or 43 |
| 100 | 56 | 200 | $1.28$ | 2 or 3 |
| 128 | 0 | 256 | 1 | 2 |
| 255 | 1 | 255 | $256/255$ | 1 or 2 |

For $n = 100$, the modulo method gives the values 0 to 55 with probability $3/256$ and the others with probability $2/256$, a 50 percent excess.

**Coin flips, $n = 6$.** Lumbroso's Fast Dice Roller uses $11/3 \approx 3.67$ flips on average. Plain rejection with three flips, rejecting 6 and 7, uses $3 \cdot 8/6 = 4$ flips on average. The entropy bound is $\log_2 6 \approx 2.585$. For $n = 3$ both methods use $8/3$ flips on average.

## Known algorithms

- **[Modulo reduction](/modulo-bias/).** Return $x \bmod n$. One division, one word. Exact only when $n$ divides $2^w$; otherwise the values below $2^w \bmod n$ have probability $\lceil 2^w / n \rceil / 2^w$ instead of $1/n$.
- **Rejection by threshold.** Let $r = 2^w \bmod n$. Draw $x$ until $x < 2^w - r$, then return $x \bmod n$. Exact. $\mathbb{E}[N] = 2^w / (2^w - r) < 2$, and two divisions per call: one for $r$ and one for the result. OpenBSD's `arc4random_uniform` uses the same idea but rejects the $r$ smallest words instead of the $r$ largest.
- **Rejection with a bit mask.** Let $k = \lceil \log_2 n \rceil$. Draw $x$, keep its low $k$ bits, and retry while the result is at least $n$. Exact, no division, $\mathbb{E}[N] = 2^k / n < 2$.
- **[Lemire's nearly divisionless method](/lemire-bounded-integers/).** Compute the $2w$-bit product $x n$; its high word is the candidate and its low word decides rejection. Exact. $\mathbb{E}[N] = 2^w / (2^w - r)$, the same as the threshold method, and the probability of a division is $n / 2^w$ for each call.
- **Multiply and shift without rejection.** Return $\lfloor x n / 2^w \rfloor$. One multiplication, not exact, with the same bias as modulo but on different values.
- **Fast Dice Roller (Lumbroso 2013).** Uses single bits and keeps the unused part of a rejected draw. Exact, with expected flips at most $\log_2 n + 2$.
- **Knuth-Yao trees.** For any discrete distribution given by binary expansions, a tree that reads bits until it reaches a leaf. Optimal in expected bits among all exact algorithms.

## Bounds

**No bounded exact method.** Let $n$ not be a power of 2, and let an algorithm always stop after at most $k$ words. Then $X$ is a function of $k$ uniform words, so each probability $\Pr[X = j]$ is $c_j / 2^{kw}$ for an integer $c_j$. If $\Pr[X = j] = 1/n$, then $n c_j = 2^{kw}$, so $n$ divides a power of 2, a contradiction. So every exact algorithm has inputs on which it reads more than $k$ words, for every $k$: rejection is necessary, not a defect of a particular method.

**Words.** For one $w$-bit word source and $n \le 2^w$, the threshold and Lemire methods read a [geometric](/geometric-distribution/) number of words with success probability $(2^w - r)/2^w > 1/2$. Since $r < n$, $\mathbb{E}[N] = 2^w / (2^w - r) \le 1 / (1 - n/2^w)$, which is close to 1 when $n$ is much smaller than $2^w$.

**Bits.** By Knuth and Yao (1976), every exact algorithm that uses fair coin flips has $\mathbb{E}[\text{flips}] \ge H(X) = \log_2 n$, the entropy of the output, and the optimal algorithm has $\mathbb{E}[\text{flips}] < \log_2 n + 2$. Lumbroso's Fast Dice Roller meets the upper bound with $O(1)$ words of memory.

**Divisions.** Lemire's method performs a division with probability exactly $n / 2^w$ per call (the probability that the low word is below $n$), so for small $n$ it almost never divides. The threshold method divides at least once on every call.

## Reductions

- **Shuffling reduces to it.** The [Fisher-Yates shuffle](/fisher-yates-shuffle/) of $n$ items makes $n - 1$ calls with ranges $2, 3, \ldots, n$, and it gives each of the $n!$ orders with probability $1/n!$ exactly when each call is exact.
- **Uniform sampling of a $k$-subset** ([Floyd's method](/floyd-sampling/), [reservoir sampling](/reservoir-sampling/)) reduces to $k$ calls.
- **Discrete distributions with rational weights** reduce to it: the [alias method](/alias-method/) needs one uniform index and one biased coin per sample.
- **Uniform bits reduce to it trivially** for $n = 2^k$, and the converse holds through the Fast Dice Roller.

## Applications

Dice and card games, the [Fisher-Yates shuffle](/fisher-yates-shuffle/), [random sampling](/random-sampling/), randomized algorithms such as quicksort with a random pivot, hashing with random coefficients ([universal hashing](/universal-hashing/)), and the choice of random keys in cryptographic protocols, where a biased integer can leak part of a secret. In the last case the source must be a [cryptographically secure generator](/cryptographically-secure-prng/) and the method must be exact.

## References
