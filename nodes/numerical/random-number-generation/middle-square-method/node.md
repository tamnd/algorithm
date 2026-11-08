---
tag: 0TYC2R
kind: algorithm
slug: middle-square-method
name: Middle-square method
aliases:
- von Neumann middle-square
- middle-square generator
area: numerical/random-number-generation
level: intro
summary: Historical generator that squares an n-digit number and keeps the middle n digits; it falls into zero or short cycles and is not used today.
model: word-ram
complexity:
  vars: {n: the number of digits of the state, t: the number of outputs}
  time: {worst: Θ(t)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, cryptographic: false}
history:
  year: 1949
  people: [John von Neumann]
  note: Von Neumann described the method at a symposium on Monte Carlo methods in 1949, published in 1951; Knuth dates his first suggestion to about 1946.
prereqs: [generator-period]
see_also: [linear-congruential-generator, pseudorandom-number-generator, floyd-cycle-detection, statistical-tests-for-randomness, seed, splitmix64]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.1, Introduction (the middle-square method, the example 5772156649, Metropolis's experiments, and the exercises on its cycles)
  - paper: "John von Neumann, Various techniques used in connection with random digits, in Monte Carlo Method, National Bureau of Standards Applied Mathematics Series 12, 1951, pages 36 to 38"
    locator: the proposal to square a number and take its middle digits, and the remarks on its short cycles
  - url: https://arxiv.org/abs/1704.00358
    title: Bernard Widynski, Middle square Weyl sequence RNG, arXiv 1704.00358, 2017
    locator: the generator that adds a Weyl sequence to the square to avoid the short cycles
---

The middle-square method is the first arithmetic [pseudorandom number generator](/pseudorandom-number-generator/) used on a computer: square the current $n$-digit number and keep its middle $n$ digits as the next number. John von Neumann proposed it in the 1940s for the first Monte Carlo computations. It is fast and simple, but nothing controls its [period](/generator-period/): its sequences fall into 0 or into short cycles, often after a few dozen steps. It is studied today as a lesson in what a generator must not do.

## In plain words

Start with a four-digit number, say 5772. Multiply it by itself to get an eight-digit number, adding zeros in front if it is shorter. Throw away the first two and the last two digits. The four digits in the middle are the next number. Repeat.

The digits look jumbled, so the numbers seem random at first. But the method has no plan. If a number with leading zeros comes up, the next number is smaller, and the numbers shrink to zero and stay there. Other starting numbers fall into a loop of four numbers that repeats forever. Every four-digit start ends in one of a few traps, after at most about a hundred steps.

## The problem

In the notation of the random-number-generation pages, the generator is $(S, f, g, s_0)$ with state space $S = \{0, \ldots, b^n - 1\}$ for a base $b$ and an even number of digits $n$, transition

$$f(x) = \left\lfloor \frac{x^2}{b^{n/2}} \right\rfloor \bmod b^n,$$

and output $g(x) = x / b^n$ in $[0, 1)$. The cost model counts word operations per output; when $b^{2n}$ fits in a word, a step is one multiplication, one division and one remainder (shifts and a mask when $b = 2$).

## The algorithm

```pseudo id=main
MIDDLE-SQUARE-STEP(x)              ▷ n even, 0 ≤ x < b^n
L1  q ← x · x                       ▷ a number of at most 2n digits
L2  return ⌊q / b^(n/2)⌋ mod b^n     ▷ drop n/2 low digits, keep the next n

MIDDLE-SQUARE-NEXT()
L3  x ← MIDDLE-SQUARE-STEP(x)
L4  return x
```

## Example

**Knuth's example.** With $n = 10$ decimal digits and $x = 5772156649$, the square is $33317792380594909201$, so the next number is $7923805949$.

**A run into zero.** With $n = 4$ and seed $5772$:

| $i$ | $x_i$ | $x_i^2$ (8 digits) | $x_{i+1}$ |
|---|---|---|---|
| 0 | 5772 | 33315984 | 3159 |
| 1 | 3159 | 09979281 | 9792 |
| 2 | 9792 | 95883264 | 8832 |
| 3 | 8832 | 78004224 | 0042 |
| 4 | 42 | 00001764 | 0017 |
| 5 | 17 | 00000289 | 0002 |
| 6 | 2 | 00000004 | 0000 |

From step 4 on, the value is below 100, and each step makes it smaller until it reaches 0, a fixed point. So $\mu = 7$ and $\rho = 1$.

**A short cycle.** From $2916$: $2916^2 = 08503056$ gives $5030$, then $3009$, then $0540$, then $2916$ again, a cycle of length 4.

**All four-digit seeds.** An exhaustive run over the 10000 seeds finds exactly eight cycles: the fixed points 0, 100, 2500, 3792 and 7600, and three cycles of length 4, namely $(540, 2916, 5030, 3009)$, $(1600, 5600, 3600, 9600)$ and $(2100, 4100, 8100, 6100)$. The longest $\mu + \rho$ is 111 (seed 6239), and the mean over all seeds is about 43.7.

**Twenty binary digits.** With $b = 2$ and $n = 20$, the step keeps bits 10 to 29 of the 40-bit square. The map has 13 cycles on its $2^{20}$ states, and the longest has period 142. Knuth reports this result of Metropolis.

## Correctness

The step returns the middle digits: dividing $x^2 < b^{2n}$ by $b^{n/2}$ removes the $n/2$ low digits, and the reduction modulo $b^n$ removes the $n/2$ high digits. What can be proved about the dynamics is negative. If $1 \le x < b^{n/2}$, then $x^2 < x \, b^{n/2}$, so $f(x) < x$: once the high half of the state is zero, the sequence decreases strictly to the fixed point 0. The number $b^{n/2}$ is also a fixed point. No theorem gives a lower bound on the period from any seed; the cycles for a given $b$ and $n$ are found by exhaustive search. The full proofs are below.

## Complexity

- **Time.** One step costs $\Theta(1)$ word operations when the square fits in a word, so $t$ outputs cost $\Theta(t)$. For larger $n$ the square costs one multiplication of $n$-digit numbers.
- **Space.** One number of $n$ digits.
- **Finding the cycle.** For one seed, [Floyd's cycle detection](/floyd-cycle-detection/) finds $\mu$ and $\rho$ in $O(\mu + \rho)$ steps and $O(1)$ space. For all seeds, one pass over the functional graph takes $O(b^n)$ steps.

## Properties

- **Not a bijection.** Different states can have the same successor (for example $f(0) = f(1) = 0$), so states with no predecessor exist and tails appear. A generator with a bijective $f$ has no tails.
- **Short periods (computed, not proved).** For $n = 4$ in base 10, every seed ends in a cycle of length 1 or 4. Metropolis's larger experiments, as reported by Knuth, found long runs for some seeds of 38 bits, but also many short cycles; there is no general guarantee.
- **Absorbing state.** Lemma 2 of the proof makes 0 absorbing for every seed that ever reaches a value below $b^{n/2}$.
- **Not cryptographic.** The state is the output.

## Variants and improvements

- **Middle square with a Weyl sequence.** Widynski (2017) adds a Weyl sequence $w \leftarrow w + s \bmod 2^{64}$, with an odd constant $s$, to the square at each step and swaps the two halves of the 64-bit result. The Weyl sequence has period $2^{64}$, so the combined state cannot get stuck in a short cycle. Its statistical quality is an empirical claim of the author, based on test batteries.
- **Middle product.** Multiply two successive values instead of squaring one. This also lacks a period guarantee.
- **Replacement.** Generators with a proved period and a bijective transition, such as the [linear congruential generator](/linear-congruential-generator/) or [SplitMix64](/splitmix64/), replaced the method in the 1950s and later.

## When to use it

Do not use it for any real purpose. Use it to teach the eventual periodicity of a finite-state generator, the danger of a non-bijective transition, and cycle detection.

## Pitfalls

- **Missing leading zeros.** The square must be read as exactly $2n$ digits, with leading zeros. Code that takes "the middle of the decimal string" of $x^2$ without padding computes a different map.
- **Odd $n$.** The middle of $2n$ digits is not defined for odd $n$ without an arbitrary choice.
- **Trusting a few outputs.** The first outputs look random; the collapse comes later. A generator must be judged by its period and its structure, not by a short sample.

## Implementations

## History

Knuth (Section 3.1) dates von Neumann's first suggestion of the method to about 1946. Von Neumann presented it at a symposium on the Monte Carlo method held in 1949 and published in 1951; in that paper he also wrote that anyone who considers arithmetical methods of producing random digits is in a state of sin. N. Metropolis studied the method on binary numbers in the 1950s; Knuth reports his results.

## References
