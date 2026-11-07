---
tag: R480RJ
kind: algorithm
slug: goertzel-algorithm
name: Goertzel algorithm
aliases:
- Goertzel filter
- Goertzel recurrence
area: algebra/fast-transforms
level: advanced
summary: Computes one DFT bin in O(n) time with a second-order recurrence, cheaper than a full FFT.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the input length (any positive integer)}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
  additions: {worst: 2n + 1}
  multiplications: {worst: n + 1}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1958
  people: [Gerald Goertzel]
  note: Goertzel (1958) gave the recurrence for evaluating a finite trigonometric sum with one multiplication per term. Gentleman (1969) analyzed its rounding errors.
prereqs: [discrete-fourier-transform, horner-rule, roots-of-unity]
see_also: [fast-fourier-transform, chebyshev-polynomials, iir-filter, polynomial-evaluation, linear-recurrences-with-constant-coefficients, bluestein-fft, rounding-error-analysis, twiddle-factor]
sources:
  - paper: doi:10.2307/2310304
    title: Gerald Goertzel, An algorithm for the evaluation of finite trigonometric series, The American Mathematical Monthly 65(1), 1958
    locator: pp. 34 to 35 (the recurrence with the constant 2 cos θ and the final combination)
  - paper: doi:10.1093/comjnl/12.2.160
    title: W. Morven Gentleman, An error analysis of Goertzel's (Watt's) method for computing Fourier coefficients, The Computer Journal 12(2), 1969
    locator: pp. 160 to 164 (the rounding error analysis)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 9, Computation of the Discrete Fourier Transform, Section 9.2 (the Goertzel algorithm as a second-order recursive filter)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 3, Basics (the model of floating-point arithmetic and the constants γ_k) and Section 3.6 (complex arithmetic)
---

The Goertzel algorithm computes one coefficient $X_k = \sum_j x_j \omega_n^{jk}$ of the [discrete Fourier transform](/discrete-fourier-transform/) with a loop of $n$ steps, each doing one multiplication by the real constant $c = 2\cos(2\pi k/n)$ and two additions, followed by one complex multiplication at the end. A direct sum would need $n$ complex multiplications by the powers of $\omega_n$; the Goertzel recurrence replaces them with real ones and needs no table of powers. When only a few of the $n$ coefficients are wanted, say fewer than about $\lg n$, it is cheaper than a full [FFT](/fast-fourier-transform/), and it works for any length $n$, not only powers of two. It is [Horner's rule](/horner-rule/) for evaluating a polynomial at a point $z$ of the unit circle, done with real arithmetic by dividing by the real quadratic $t^2 - c t + 1$ whose roots are $z$ and $\bar z$.

## In plain words

Suppose you only want to know how strongly one frequency is present in a signal, for instance whether a telephone key tone is on the line. Instead of computing the whole spectrum, run the samples through a small machine with two memory cells. Each sample is added to a fixed multiple of the first cell minus the second, and the cells shift by one. After the last sample, a single combination of the two cells gives the answer for that frequency. The fixed multiple depends only on the frequency, so the machine needs no table and does very little work per sample.

## The problem

**Notation.** As on all pages of fast transforms, $n$ is the transform length and $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign). The DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega_n^{jk}$, and the inverse is $x_j = \frac1n \sum_k X_k \omega_n^{-jk}$. Here $n$ can be any positive integer. Over a commutative ring $R$ the same recurrence works for any $\omega \in R$ with $\omega^n = 1$, which is how the tests check it exactly modulo a prime; to have an inverse DFT at all, $\omega$ must be a principal $n$-th [root of unity](/roots-of-unity/) and $n$ a unit.

**Input.** A sequence $x_0, \ldots, x_{n-1}$ of real or complex numbers and an index $k$.

**Output.** The single value $X_k$.

**Cost model.** Additions (with subtractions) and multiplications are counted separately, at unit cost, in the [real RAM](/real-ram/); the counts below are for operations in the ring of the input, with the multiplier $c$ real. For real input every operation of the loop is real. The two constants $z$ and $c$ are computed once, from the exact angle, and not counted.

## The algorithm

Let $z = \omega_n^{-k} = e^{2\pi i k/n}$, so that $z^{-1} = \bar z$ and $z + \bar z = c = 2\cos(2\pi k/n)$. The loop computes the sequence $s_{-2} = s_{-1} = 0$, $s_j = x_j + c\, s_{j-1} - s_{j-2}$, keeping only the last two values, and returns $z\, s_{n-1} - s_{n-2}$.

```pseudo id=main
GOERTZEL(x, k)        ▷ x = (x_0, …, x_(n−1)) with n ≥ 1; returns X_k
L1  z ← ω_n^(−k)                    ▷ = e^(2πik/n)
L2  c ← z + z^(−1)                  ▷ = 2 cos(2πk/n), a real number
L3  s1 ← 0; s2 ← 0                  ▷ s1 holds s_(j−1), s2 holds s_(j−2)
L4  for j ← 0 to n − 1 do
L5      s ← x_j + c · s1 − s2
L6      s2 ← s1; s1 ← s
L7  return z · s1 − s2               ▷ = z s_(n−1) − s_(n−2)
```

As a filter, lines L4 to L6 run the input through the recursive filter with transfer function $1/(1 - c t + t^2)$, whose poles are $z$ and $\bar z$ on the unit circle, and line L7 is one step of the nonrecursive part $z - t$. Only line L7 involves a complex number.

## Example

Modulo $p = 17$ with $n = 8$ and $\omega = 2$ (so $2^4 = 16 = -1$, and $2$ has order $8$), compute $X_1$ for $x = (1, 2, 3, 4, 5, 6, 7, 8)$. Here $z = 2^{-1} = 9$ and $c = 9 + 2 = 11$.

| j | x_j | s_j = x_j + 11 s_(j−1) − s_(j−2) mod 17 |
|---|---|---|
| 0 | 1 | 1 |
| 1 | 2 | 2 + 11 = 13 |
| 2 | 3 | 3 + 143 − 1 = 145 ≡ 9 |
| 3 | 4 | 4 + 99 − 13 = 90 ≡ 5 |
| 4 | 5 | 5 + 55 − 9 = 51 ≡ 0 |
| 5 | 6 | 6 + 0 − 5 = 1 |
| 6 | 7 | 7 + 11 − 0 = 18 ≡ 1 |
| 7 | 8 | 8 + 11 − 1 = 18 ≡ 1 |

Line L7 gives $X_1 = 9 \cdot 1 - 1 = 8$. Directly, $\sum_j x_j 2^j = 1 + 4 + 12 + 32 + 80 + 192 + 448 + 1024 = 1793 = 105 \cdot 17 + 8$. Running the algorithm for every $k$ gives the whole transform $(2, 8, 14, 6, 13, 3, 12, 1)$, which matches the direct DFT.

Over $\mathbb{C}$, for $x = (1, 2, 3, 4)$ and $k = 1$: $z = i$ and $c = 0$, so $s = (1, 2, 2, 2)$ and $X_1 = 2i - 2$, which is $1 - 2i - 3 + 4i$. Both examples were checked by script.

## Correctness

Write $y_j = \sum_{i \le j} x_i z^{j-i}$, the value of Horner's rule after $j + 1$ steps at the point $z$. We claim $y_j = s_j - \bar z\, s_{j-1}$ for every $j \ge 0$. For $j = 0$ both sides are $x_0$. If it holds for $j$, then $y_{j+1} = z y_j + x_{j+1} = z s_j - s_{j-1} + x_{j+1}$, because $z \bar z = 1$; and $s_{j+1} - \bar z s_j = x_{j+1} + (c - \bar z) s_j - s_{j-1} = x_{j+1} + z s_j - s_{j-1}$, because $c = z + \bar z$. So the claim holds for $j + 1$.

Now $X_k = \sum_j x_j z^{-j}$, and since $z^n = 1$, $z^{-j} = z \cdot z^{n-1-j}$, so $X_k = z\, y_{n-1} = z s_{n-1} - s_{n-2}$, which is line L7. The argument uses only $z^n = 1$ and $c = z + z^{-1}$, so it holds over any commutative ring. The full proof, with the rounding error bound below, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Operations.** The loop does $n$ multiplications $c \cdot s_1$ and $2n$ additions and subtractions; line L7 does one multiplication and one subtraction. So one coefficient costs exactly $n + 1$ multiplications and $2n + 1$ additions, in $\Theta(n)$ time and $\Theta(1)$ extra space, for every input. For real input the loop is real arithmetic, so the cost is $n$ real multiplications and $2n$ real additions plus one real-by-complex product ($2$ real multiplications) and one real subtraction: $n + 2$ and $2n + 1$. For complex input the loop runs on the two components separately: $2n + 4$ real multiplications and $4n + 4$ real additions, counting line L7 as a general complex product.

**Against the direct sum and the FFT.** The direct sum for one coefficient needs $n$ complex multiplications by table entries ($4n$ real multiplications and about $4n$ real additions for complex input). Computing $M$ coefficients by Goertzel costs about $M n$ multiplications against about $\frac{n}{2} \lg n$ complex multiplications for one radix-2 FFT of all $n$, so it is cheaper when $M$ is below a small multiple of $\lg n$. It also allows any $n$, and the samples can be processed as they arrive, without storing them.

**Rounding errors.** In floating point with unit roundoff $u$, let $\eta = |\hat c - c|$ and $\mu = |\hat z - z|$ be the errors of the two constants, and $M = \min(n, 1/|\sin(2\pi k/n)|)$. To first order in $u$, the computed value satisfies

$$|\hat X_k - X_k| \le (13u + \eta + \mu)(n + 2)\, M \sum_j |x_j|.$$

*Proved* in [proofs/correctness.md](proofs/correctness.md), in the standard model of Higham's Chapter 3. The key fact is that a local error in $s_j$ reaches the output with factor of modulus exactly $1$, while the values $s_j$ themselves can grow like $M \sum |x_j|$. So the bound is $O(n u \lVert x \rVert_1)$ for frequencies away from $0$ and $\pi$, but grows to $O(n^2 u \lVert x \rVert_1)$ as $k/n$ approaches $0$ or $\frac12$, where the two poles $z, \bar z$ merge. This is worse than the FFT, whose error per coefficient grows like $\lg n$. *Observed* on random real data in $[-1, 1]$ with the coefficients $k = 1$ and $k = n/2 - 1$: the error relative to $u \lVert x \rVert_1$ was about $14$ at $n = 64$, $1075$ at $n = 1024$ and $89000$ at $n = 16384$, well below the bound but clearly growing faster than $n$, while for $k = n/4$ (where $c = 0$ exactly) it stayed below $1$. The tests use the bound above with $\eta + \mu \le 7u$.

## Properties

- **Any length.** $n$ need not be a power of two, or even composite.
- **Streaming.** Each sample is used once, in order, and then discarded; the state is two numbers.
- **No table.** Only the two constants $c$ and $z$ depend on $k$; there are no twiddle factors.
- **Exact over rings.** Over $\mathbb{Z}/p\mathbb{Z}$ with any $\omega$ of order dividing $n$ it computes $X_k$ exactly.
- **Real arithmetic.** For real input the loop is entirely real; only line L7 produces a complex number, and the magnitude $|X_k|^2 = s_{n-1}^2 + s_{n-2}^2 - c\, s_{n-1} s_{n-2}$ needs no complex arithmetic at all.

## Variants and improvements

- **Power only.** Detectors that need $|X_k|^2$ use the real formula above instead of line L7, which saves the complex product.
- **Arbitrary frequency.** With $z = e^{i\theta}$ and $c = 2\cos\theta$ for any real $\theta$, the same proof shows that line L7 returns $z^n \sum_j x_j e^{-i\theta j}$. Multiplying by $e^{-i\theta n}$ gives the discrete-time Fourier transform of the block at $\theta$; for $\theta = 2\pi k/n$ the factor is $1$.
- **Many bins.** Running the loop for $M$ values of $k$ at once is $M$ independent recurrences over the same samples.
- **Clenshaw recurrence.** The same idea evaluates any sum $\sum_j a_j \phi_j$ where the $\phi_j$ satisfy a three-term recurrence, such as the [Chebyshev polynomials](/chebyshev-polynomials/); Goertzel's recurrence is the case $\phi_j = $ cosines and sines.

## When to use it

Use it when only a few DFT coefficients of a block are needed, and especially when the samples arrive one at a time: tone detection, such as the dual-tone keys of a telephone keypad, and monitoring a fixed set of frequencies. For the whole spectrum, or for more than a handful of bins of a long block, use an [FFT](/fast-fourier-transform/), which is also more accurate. For frequencies very close to $0$ or $\pi$ in long blocks, prefer the direct sum with an accurate table, or an FFT, if accuracy matters.

## Pitfalls

- **The sign of $z$.** With the convention $\omega_n = e^{-2\pi i/n}$, line L7 multiplies by $z = e^{+2\pi i k/n}$. Using $e^{-2\pi i k/n}$ there returns the coefficient of the other sign convention, which is the complex conjugate for real input.
- **The final step.** Forgetting line L7 and reporting $s_{n-1}$ gives a wrong phase and magnitude; the power formula needs both $s_{n-1}$ and $s_{n-2}$.
- **Accuracy near $0$ and $\pi$.** The constant $c$ is close to $\pm 2$ there and the state grows like $n$, so errors grow like $n^2 u$; do not use the basic form for very long blocks at such frequencies.
- **Constants from a large angle.** Take $c = 2\cos(2\pi k/n)$ from the exact angle, with $k$ reduced modulo $n$; computing $\cos$ of a large unreduced argument loses accuracy.
- **Not a full transform.** For all $n$ coefficients Goertzel costs $\Theta(n^2)$, like the direct sum.

## Implementations

The Python implementation in [impl/python/goertzel_algorithm.py](impl/python/goertzel_algorithm.py) follows the main block line by line over $\mathbb{C}$, taking $z$ from the exact angle, and has an exact branch modulo a prime $p$ for any $\omega$ with $\omega^n = 1$. The tests compare it with the direct $O(n^2)$ DFT: exactly modulo $17$, $97$ and $998244353$ for every length $n < 50$ dividing $p - 1$ (including lengths that are not powers of two) and every $k$, and over $\mathbb{C}$ for lengths $1$ to $39$ and up to $331$ against the proved error bound; they cover zeros, an impulse, a constant, $n = 1$ and $2$, and recover the input by computing every bin and then inverting with $\omega^{-1}$ and $1/n$.

## History

Goertzel (1958) published the recurrence as a way to evaluate finite trigonometric series $\sum_j x_j \cos j\theta$ and $\sum_j x_j \sin j\theta$ with one multiplication per term, before the Cooley-Tukey FFT of 1965. Gentleman (1969) gave a rounding error analysis of the method, which his title also attributes to Watt. The recursive-filter view, with poles at $e^{\pm 2\pi i k/n}$, is the standard presentation in signal processing texts such as Oppenheim and Schafer.

## References
