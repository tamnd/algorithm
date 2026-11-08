---
tag: V53JWN
kind: algorithm
slug: lagged-fibonacci-generator
name: Lagged Fibonacci generator
aliases:
- additive lagged Fibonacci generator
- LFG
- additive generator
area: numerical/random-number-generation
level: advanced
summary: Generates x_n = (x_(n-k) op x_(n-j)) mod 2^w from two earlier outputs, with op addition, subtraction, multiplication or exclusive-or, keeping the last k values in a circular buffer.
model: word-ram
complexity:
  vars: {n: the number of outputs, k: the long lag, w: the word size}
  time: {worst: Θ(n)}
  space: {extra: Θ(k)}
properties: {deterministic: true, recursive: false, cryptographic: false}
history:
  year: 1958
  people: [G. J. Mitchell, D. P. Moore]
  note: Knuth reports an unpublished additive generator x_n = (x_(n-24) + x_(n-55)) mod m by Mitchell and Moore from 1958.
prereqs: [linear-congruential-generator, primitive-polynomial, linear-feedback-shift-register, generator-period]
see_also: [ranlux, well-rng, mersenne-twister, jump-ahead, equidistribution, statistical-tests-for-randomness, multiple-recursive-generator]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.2, Other methods (the additive generator with lags 24 and 55, its period, and the table of primitive trinomials), and Section 3.6, Summary (the subtractive generator ran_array with lags 100 and 37)
  - url: https://www-cs-faculty.stanford.edu/~knuth/programs/rng.c
    title: Donald E. Knuth, rng.c, the routines ran_start and ran_array
    locator: the test program, which prints 995235265 after ran_start(310952) and 2010 calls of ran_array with n = 1009
  - paper: "Richard P. Brent, On the periods of generalized Fibonacci recurrences, Mathematics of Computation 63(207), 1994, pages 389 to 401"
    locator: the theorem that the additive recurrence modulo 2^w has period (2^k - 1) 2^(w-1) when the trinomial is primitive and some initial value is odd
  - paper: "Alan M. Ferrenberg, D. P. Landau and Y. Joanna Wong, Monte Carlo simulations: hidden errors from good random number generators, Physical Review Letters 69(23), 1992, pages 3382 to 3384"
    locator: the systematic errors in cluster-algorithm Ising simulations driven by the shift-register generator R250
  - paper: doi:10.1145/1268776.1268777
    title: Pierre L'Ecuyer and Richard Simard, TestU01, a C library for empirical testing of random number generators, ACM Transactions on Mathematical Software 33(4), 2007
    locator: the results for lagged Fibonacci generators in the tables of tested generators
---

A lagged Fibonacci generator produces each output from two earlier ones, $x_n = (x_{n-k} \star x_{n-j}) \bmod 2^w$ with lags $0 < j < k$ and $\star$ one of $+$, $-$, $\times$ or exclusive-or. It is the Fibonacci recurrence $x_n = x_{n-1} + x_{n-2}$ with the lags pulled apart. With lags chosen so that $x^k + x^j + 1$ is a primitive polynomial modulo 2, the additive version has period $(2^k - 1)\, 2^{w-1}$, enormous for $k$ in the hundreds, at the cost of one addition and a buffer of $k$ words. Its weakness is built in: $x_n - x_{n-j} - x_{n-k} \equiv 0$, so the triples at those three positions are far from independent.

## In plain words

Keep a list of the last few dozen numbers the generator has produced. To make a new number, take two of them that sit at fixed distances back in the list, add them, and keep only the low part that fits in a machine word. Append the new number and forget the oldest.

If the two distances are chosen well, the list of numbers takes an astronomically long time to repeat. The method is fast because each new number costs one addition. Its catch is that every new number is exactly the sum of two old ones, and a test that looks at those three positions together sees it at once.

## The problem

A generator is a tuple $(S, f, g, s_0)$: state space $S$, transition $f$ with $s_{i+1} = f(s_i)$, output $u_i = g(s_i)$ and seed $s_0$. The goal is a long-period stream of $w$-bit words, or values $u_i \in [0, 1)$ close to $U(0, 1)$, at a constant number of word operations per output. Here the state is the window of the last $k$ values,

$$s_n = (x_{n-k}, x_{n-k+1}, \ldots, x_{n-1}) \in \{0, \ldots, 2^w - 1\}^k,$$

the transition appends $x_n = (x_{n-k} \star x_{n-j}) \bmod 2^w$ and drops $x_{n-k}$, and the output is $x_n$, or $u_n = x_n / 2^w$. The parameters are the lags $j < k$, the word size $w$ and the operation $\star$. We write LFG$(j, k, \star)$; Knuth's ran_array is LFG$(37, 100, -)$ with $w = 30$, and the classic additive generator is LFG$(24, 55, +)$.

## The algorithm

```pseudo id=main
LFG-NEXT()                            ▷ B[0..k−1] is a circular buffer; B[p] holds x_(n−k)
L1  q ← p + k − j; if q ≥ k then q ← q − k   ▷ B[q] holds x_(n−j)
L2  x ← (B[p] ⋆ B[q]) mod 2^w
L3  B[p] ← x                           ▷ x_n replaces x_(n−k), which is no longer needed
L4  p ← p + 1; if p = k then p ← 0
L5  return x

LFG-SEED(x_0, ..., x_(k−1))
L6  B ← (x_0, ..., x_(k−1)); p ← 0
L7  require: some x_i odd if ⋆ is + or −; all x_i odd if ⋆ is ×; some x_i ≠ 0 if ⋆ is ⊕
```

The buffer positions rotate instead of the data: after $L4$, $B[p]$ again holds the oldest value. Implementations often generate a whole array at once, as ran_array does, which removes the index arithmetic from the inner loop. The $k$ initial values are filled from another generator, such as an [LCG](/linear-congruential-generator/) or [SplitMix64](/splitmix64/); Knuth's ran_start uses a special procedure that makes the initial values from different seeds far apart.

## Example

Take LFG$(1, 3, +)$ with $w = 3$, so $x_n = (x_{n-3} + x_{n-1}) \bmod 8$, and seed $(x_0, x_1, x_2) = (1, 0, 0)$. The trinomial $x^3 + x + 1$ is primitive modulo 2.

| $n$ | buffer $B$ before | $p$ | $x_{n-3}$ | $x_{n-1}$ | $x_n$ |
|---|---|---|---|---|---|
| 3 | $(1, 0, 0)$ | 0 | 1 | 0 | 1 |
| 4 | $(1, 0, 0)$ | 1 | 0 | 1 | 1 |
| 5 | $(1, 1, 0)$ | 2 | 0 | 1 | 1 |
| 6 | $(1, 1, 1)$ | 0 | 1 | 1 | 2 |
| 7 | $(2, 1, 1)$ | 1 | 1 | 2 | 3 |
| 8 | $(2, 3, 1)$ | 2 | 1 | 3 | 4 |
| 9 | $(2, 3, 4)$ | 0 | 2 | 4 | 6 |
| 10 | $(6, 3, 4)$ | 1 | 3 | 6 | 1 |

The sequence continues $1, 0, 0, 1, 1, 1, 2, 3, 4, 6, 1, 5, 3, 4, 1, 4, 0, 1, 5, 5, 6, 3, 0, 6, 1, 1, 7, 0, 1, 0, 0, \ldots$ and returns to $(1, 0, 0)$ at $n = 28 = (2^3 - 1) \cdot 2^2$, the maximal period. The low bits $1, 0, 0, 1, 1, 1, 0, 1, 0, 0, \ldots$ repeat with period 7: they are the bit sequence of an [LFSR](/linear-feedback-shift-register/) with feedback polynomial $x^3 + x + 1$.

**Reference value.** Knuth's rng.c, after ran_start(310952) and 2010 calls of ran_array with $n = 1009$, has first array element 995235265; the same value appears after 1010 calls with $n = 2009$. A port of ran_start and ran_array reproduces it.

## Correctness

The buffer invariant is: before each call, $B[(p + i) \bmod k] = x_{n-k+i}$ for $0 \le i < k$. Line L1 then finds $x_{n-j}$ at offset $i = k - j$, line L3 overwrites the only entry no longer needed, and line L4 restores the invariant for $n + 1$. So the outputs are exactly the recurrence. The proof page gives the details, with the facts about the low bit.

**Period (additive and subtractive).** If $x^k + x^j + 1$ is primitive over $\mathbb{F}_2$ and at least one of $x_0, \ldots, x_{k-1}$ is odd, then the sequence modulo $2^w$ is purely periodic with period exactly $(2^k - 1)\, 2^{w-1}$ (Brent 1994; Knuth Section 3.2.2 for the case $(24, 55)$). Modulo 2 the recurrence is an LFSR with a primitive characteristic polynomial, which gives the factor $2^k - 1$; each extra bit of the word at most doubles the period, and Brent shows it does double. Exhaustive search confirms the formula for all seeds with an odd value, for the primitive trinomials of degree at most 5 and $w \le 3$.

**Other operations.** With $\star = \oplus$ each bit position is a separate LFSR, so the period is $2^k - 1$ and the generator is a generalized feedback shift register. With $\star = \times$ and all initial values odd, the maximal period is $(2^k - 1)\, 2^{w-3}$ for $w \ge 3$; it is reached for suitable seeds but not for all (all ones is a fixed point).

## Complexity

Each call does one operation $\star$, one comparison and two index updates, so $n$ outputs cost $\Theta(n)$ word operations. Space is the buffer of $k$ words. Seeding costs $\Theta(k)$ plus the cost of the seeding generator; ran_start costs more, about 100 rounds of $O(k)$ operations plus ten calls of ran_array, to decorrelate seeds. Batch generation into an array of length $N \ge k$ costs one operation per element with no modular indexing.

## Properties

- **Long period, cheap step.** LFG$(24, 55, +)$ with $w = 32$ has period $(2^{55} - 1)\, 2^{31} \approx 7.7 \cdot 10^{25}$; LFG$(37, 100, -)$ with $w = 30$ has $(2^{100} - 1)\, 2^{29}$.
- **Exact three-point relation.** For $\star = +$, $u_n - u_{n-j} - u_{n-k} \in \{0, -1\}$ exactly, so the triple $(u_{n-k}, u_{n-j}, u_n)$ lies on two planes. A test that conditions on $u_{n-k} + u_{n-j} < \tfrac12$ finds $u_n < \tfrac12$ every time, against probability $\tfrac12$ for independent values.
- **Weak low bits.** Bit $b$ (counting from 0 at the low end) of $x_n$ depends only on bits $0, \ldots, b$ of the earlier values; the lowest bit is an LFSR sequence with all its linear structure.
- **Many disjoint cycles.** For $w > 1$ the state space splits into many cycles of the maximal length, so different seeds usually give different, non-overlapping cycles rather than offsets in one cycle.
- **Not cryptographic.** Given $k$ consecutive outputs, the state is known and every later output follows.

## Variants and improvements

- **Subtractive and subtract-with-borrow.** $x_n = (x_{n-k} - x_{n-j}) \bmod 2^w$ behaves like the additive one. Subtract-with-borrow and add-with-carry generators (Marsaglia and Zaman) add a carry bit and reach much longer periods; [RANLUX](/ranlux/) is subtract-with-borrow with discarded outputs.
- **Discarding outputs.** Knuth recommends generating ran_array in blocks of 1009 and using only the first 100 values, which hides the three-point relation from tests that look at nearby outputs; Lüscher's RANLUX does the same with a theory for how many to skip.
- **More taps.** Generators with four taps, $x_n = x_{n-a} \oplus x_{n-b} \oplus x_{n-c} \oplus x_{n-d}$ (Ziff), remove the strongest three-point correlations of two-tap $\oplus$ generators.
- **Multiplicative LFG.** $\star = \times$ on odd words gives better statistics than $+$ at a higher cost per step and a period shorter by a factor 4.
- **Combination.** Adding the output of a different kind of generator, such as an LCG, breaks the linear relation; this is how several long-period generators of the 1990s were built.

## When to use it

Use it where a very long period and a very cheap step matter and outputs are consumed in ways that do not combine lags $j$ and $k$, for example with Knuth's ran_array and its discarding rule. For new code, a well-tested generator with a better structure, such as [xoshiro](/xoshiro-xoroshiro/), [PCG](/pcg-random/) or [MRG32k3a](/mrg32k3a/), is usually a better default, and [cryptographic generators](/cryptographically-secure-prng/) are needed whenever outputs must not be predictable.

## Pitfalls

- **Small lags fail tests.** With $k$ below a few hundred, additive LFGs fail empirical tests such as the birthday spacings test and some TestU01 batteries; use $k$ of 100 or more and discard outputs, or pick another generator.
- **Simulations that hit the lag structure.** Ferrenberg, Landau and Wong (1992) found wrong results in Ising model simulations with the Wolff cluster algorithm driven by R250, a two-tap $\oplus$ generator with lags 103 and 250, although it passed the standard tests of the time.
- **Bad seeding.** An additive LFG seeded with all even values never produces an odd value; one seeded with mostly zeros produces mostly small numbers for a long time. Fill the buffer from a good generator and discard the first several $k$ outputs.
- **Non-primitive trinomials.** If $x^k + x^j + 1$ is not primitive, the period is much shorter; for $x^4 + x^2 + 1$ and $w = 3$, every seed with an odd value has period 24 instead of 60.
- **Low bits.** Do not use $x_n \bmod 2$ or $x_n \bmod 2^b$ for small $b$ as random bits; take the high bits.

## Implementations

## History

Knuth (Section 3.2.2) credits the additive generator with lags 24 and 55 to an unpublished 1958 proposal by G. J. Mitchell and D. P. Moore, and tabulates lags for which $x^k + x^j + 1$ is primitive. Marsaglia studied lagged Fibonacci generators with several operations in the 1980s and showed their failures on the birthday spacings test for small lags. Brent (1994) proved the period of the additive generator modulo $2^w$ in general. Knuth's third edition (1997) recommends the subtractive ran_array with lags 100 and 37, used in blocks with discarding, and the 2002 revision of its seeding routine is the version in common use.

## References
