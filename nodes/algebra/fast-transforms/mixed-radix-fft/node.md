---
tag: FR88CY
kind: algorithm
slug: mixed-radix-fft
name: Mixed-radix FFT
aliases:
- mixed-radix Cooley-Tukey
- radix-4 FFT
- general-radix FFT
- radix-r FFT
area: algebra/fast-transforms
level: advanced
summary: Cooley-Tukey generalization that factors n into arbitrary small radices, not only 2.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (any product of radices r_i at least 2), t: the number of radices, S: the sum r_1 + r_2 + ... + r_t of the radices}
  time: {worst: Θ(n S), average: Θ(n S), best: Θ(n S)}
  space: {extra: Θ(n)}
  additions: {worst: n (S − t)}
  multiplications: {worst: n (S − t)}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  year: 1965
  people: [James W. Cooley, John W. Tukey]
  note: Cooley and Tukey (1965) gave the splitting for a general factorization of n. Gauss had split a transform of length n_1 n_2 about 1805. Singleton (1969) published a widely used mixed-radix program.
prereqs: [fast-fourier-transform, discrete-fourier-transform, twiddle-factor]
see_also: [iterative-fft, split-radix-fft, chinese-remainder-theorem-fft, rader-fft, bluestein-fft, winograd-fourier-transform, multidimensional-fft, butterfly-operation]
sources:
  - paper: doi:10.1090/S0025-5718-1965-0178586-1
    title: James W. Cooley and John W. Tukey, An algorithm for the machine calculation of complex Fourier series, Mathematics of Computation 19(90), 1965
    locator: pp. 297 to 301 (the index splitting for a composite length and the operation count)
  - paper: doi:10.1109/TAU.1969.1162042
    title: Richard C. Singleton, An algorithm for computing the mixed radix fast Fourier transform, IEEE Transactions on Audio and Electroacoustics 17(2), 1969
    locator: pp. 93 to 103 (a mixed-radix program with special butterflies for small factors)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 2, General Radix Frameworks (the radix-p splitting, mixed-radix factorizations and the radix-4 framework)
  - paper: doi:10.1109/MASSP.1984.1162257
    title: Michael T. Heideman, Don H. Johnson and C. Sidney Burrus, Gauss and the history of the fast Fourier transform, IEEE ASSP Magazine 1(4), 1984
    locator: pp. 14 to 21 (Gauss's splitting of a length n_1 n_2 about 1805)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2, The Discrete Fourier Transform and the Fast Fourier Transform (the DFT over a ring and principal roots of unity)
---

The mixed-radix FFT computes the [discrete Fourier transform](/discrete-fourier-transform/) of length $n = r_1 r_2 \cdots r_t$ for any factorization into radices $r_i \ge 2$. It splits the input into $r_1$ interleaved subsequences, transforms each recursively with the remaining radices, multiplies by [twiddle factors](/twiddle-factor/), and combines the results with $n / r_1$ small DFTs of length $r_1$. With all $r_i = 2$ it is the radix-2 [FFT](/fast-fourier-transform/). Its cost is $\Theta(n (r_1 + \cdots + r_t))$, which is $\Theta(n \log n)$ when the radices are bounded, so lengths such as $360 = 2^3 \cdot 3^2 \cdot 5$ or $1000$ are as fast as powers of two. A large prime factor makes it slow; for that case there are [Rader's algorithm](/rader-fft/) and [Bluestein's algorithm](/bluestein-fft/).

## In plain words

To transform a long list whose length factors as, say, three times four, deal the entries out into three piles, like cards. Transform each pile, which is a smaller problem of the same kind, and solve it the same way. Then rotate each pile's results by a known amount and, for each position, combine the three piles with a tiny transform of length three. Each factor of the length adds one round of tiny transforms over the whole list, so the work is the length times the sum of the factors.

## The problem

**Notation.** As on all pages of fast transforms, $n$ is the transform length, here any integer $n \ge 1$ given with a factorization $n = r_1 \cdots r_t$, $r_i \ge 2$ (the empty product for $n = 1$). Over $\mathbb{C}$, $\omega = \omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign). Over a commutative ring $R$, $\omega$ is a principal $n$-th [root of unity](/roots-of-unity/): $\omega^n = 1$ and $\sum_{j} \omega^{jk} = 0$ for $0 < k < n$. The DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$, and the inverse is $x_j = \frac1n \sum_k X_k \omega^{-jk}$, which needs $n$ to be a unit.

**Input.** $x \in R^n$, the radices, and $\omega$.

**Output.** $X = (X_0, \ldots, X_{n-1})$.

**Cost model.** Additions (with subtractions) and multiplications in $R$ are counted separately, at unit cost, in the [real RAM](/real-ram/) for $\mathbb{C}$ and the word RAM for $\mathbb{Z}/p\mathbb{Z}$. Twiddle factors come from a table of the $n$ powers of $\omega$, built once and not counted. Index arithmetic is not counted.

## The algorithm

Write $r = r_1$ and $m = n / r$. Split the index $j = r q + l$ with $0 \le l < r$ and $0 \le q < m$, and the output index $k + m s$ with $0 \le k < m$ and $0 \le s < r$. Let $Y^{(l)}$ be the DFT of length $m$, with root $\omega^r$, of the subsequence $(x_l, x_{l+r}, \ldots, x_{l + (m-1) r})$. Then, since $\omega^{r q m s} = 1$,

$$X_{k + m s} = \sum_{l=0}^{r-1} \omega^{l(k + ms)} \sum_{q=0}^{m-1} x_{rq+l}\, \omega^{rqk} = \sum_{l=0}^{r-1} \left(\omega^{lk}\, Y^{(l)}_k\right) \omega_r^{l s}, \qquad \omega_r = \omega^m.$$

So for each $k$ the $r$ outputs $X_k, X_{k+m}, \ldots, X_{k + (r-1)m}$ are a DFT of length $r$, with the root $\omega^m$ of order $r$, applied to the twiddled values $\omega^{lk} Y^{(l)}_k$. This length-$r$ DFT is the radix-$r$ [butterfly](/butterfly-operation/).

```pseudo id=main
MIXED-RADIX-FFT(x, ω, (r_1, …, r_t))   ▷ length(x) = r_1 ⋯ r_t and ω^length(x) = 1
L1  n ← length(x)
L2  if n = 1 then return x
L3  r ← r_1; m ← n / r
L4  for l ← 0 to r − 1 do                 ▷ r interleaved subsequences
L5      Y^(l) ← MIXED-RADIX-FFT((x_l, x_(l+r), …, x_(l+(m−1)r)), ω^r, (r_2, …, r_t))
L6  for k ← 0 to m − 1 do
L7      t_l ← ω^(lk) · Y^(l)_k for l = 0, …, r − 1      ▷ twiddle factors (t_0 = Y^(0)_k)
L8      for s ← 0 to r − 1 do                          ▷ a DFT of length r with root ω^m
L9          X_(k+ms) ← t_0 + Σ_(l=1)^(r−1) ω^(mls) · t_l
L10 return X
```

The recursion depth is $t \le \lg n$. Lines L6 to L9 form one *stage*; the subproblems of one recursion level together form a stage of the whole computation. The inverse transform runs the same program with $\omega^{-1}$ and divides by $n$; any order of the radices may be used, and different orders give the same result.

## Example

Modulo $97$, with $n = 6$ and $\omega = 5^{16} \bmod 97 = 36$ (so $\omega^3 = 96 = -1$ and $\omega^2 = 35$), transform $x = (1, 2, 3, 4, 5, 6)$ with the radices $(2, 3)$.

Lines L4 and L5 split by parity and transform each half with the root $\omega^2 = 35$ of order $3$: the even entries $(1, 3, 5)$ give $E = (9, 23, 68)$, and the odd entries $(2, 4, 6)$ give $O = (12, 23, 68)$. Since $r = 2$, the length-$2$ DFT in lines L8 and L9 is $(t_0 + t_1, t_0 - t_1)$, with $\omega^3 = -1$.

| k | t_0 = E_k | t_1 = ω^k O_k | X_k = t_0 + t_1 | X_(k+3) = t_0 − t_1 |
|---|---|---|---|---|
| 0 | 9 | 12 | 21 | 94 |
| 1 | 23 | 36 · 23 ≡ 52 | 75 | 68 |
| 2 | 68 | 35 · 68 ≡ 52 | 23 | 16 |

So $X = (21, 75, 23, 94, 68, 16)$, which is the direct DFT. The radices in the order $(3, 2)$ give the same vector, and the inverse transform with the radices $(3, 2)$ returns $(1, 2, 3, 4, 5, 6)$. All numbers were checked by script.

## Correctness

The proof is by induction on $t$, and it uses only $\omega^n = 1$; that $\omega$ is principal matters for the inverse, not for the forward transform. For $t = 0$, $n = 1$ and $X_0 = x_0$. For $t \ge 1$, $(\omega^r)^m = 1$, so by induction line L5 computes the DFTs $Y^{(l)}$ of length $m$ with root $\omega^r$. The identity displayed above shows that lines L7 and L9 compute $X_{k+ms}$, and as $k$ ranges over $[0, m)$ and $s$ over $[0, r)$, $k + ms$ ranges over $[0, n)$ exactly once. The full proof, with the operation counts, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Operations.** Let $n_i = r_i r_{i+1} \cdots r_t$ be the size of the subproblems at recursion level $i$; there are $n / n_i$ of them. A subproblem at level $i$ does, for each of its $n_i / r_i$ values of $k$, $r_i - 1$ twiddle multiplications at line L7 and, at line L9, $r_i (r_i - 1)$ additions and at most $(r_i - 1)^2$ multiplications (the products with $ls \equiv 0 \pmod{r_i}$ are skipped). So level $i$ costs exactly $n (r_i - 1)$ additions and at most $n (r_i - 1)$ multiplications, and in total

$$A(n) = n \sum_{i=1}^{t} (r_i - 1), \qquad M(n) \le n \sum_{i=1}^{t} (r_i - 1),$$

with equality for $M$ when every $r_i$ is prime. The time is $\Theta(n \sum_i r_i)$ for every input. With the radices bounded by a constant, $t \le \lg n$ gives $\Theta(n \log n)$. With $n$ prime, $t = 1$ and the cost is $\Theta(n^2)$, the direct DFT.

**Special butterflies.** The count above treats the length-$r$ DFT as a plain matrix-vector product. Hand-written butterflies for small $r$ do much better, because $\omega_2 = -1$ and $\omega_4 = -i$ need no multiplication. Radix $2$ then costs $\frac{n}{2}$ twiddle multiplications and $n$ additions per stage, $\frac{n}{2} \lg n$ and $n \lg n$ in total. A radix-$4$ stage costs $\frac{3n}{4}$ twiddle multiplications ($l = 1, 2, 3$ for each of the $\frac{n}{4}$ values of $k$) and $2n$ additions (a radix-$4$ butterfly is $8$ additions and subtractions and a free multiplication by $-i$), and there are $\frac12 \lg n$ stages, so a radix-$4$ FFT of length $4^q$ uses at most $\frac38 n \lg n$ complex multiplications, including the trivial ones at $k = 0$, and $n \lg n$ complex additions: a quarter fewer multiplications than radix $2$ and the same additions. The [split-radix FFT](/split-radix-fft/) does better still.

**Space.** The recursive form uses $\Theta(n)$ extra space for the subresults and the table of powers. Iterative versions work in place with a digit-reversal permutation, the mixed-radix analogue of the [bit-reversal permutation](/bit-reversal-permutation/).

**Rounding errors.** Over $\mathbb{C}$ in floating point, each stage is a matrix that is $\sqrt{r_i}$ times a unitary one, computed with sums of $r_i$ rounded products. *Not proved here:* by the argument of Higham's Theorem 24.2 for radix $2$, one expects a normwise relative error of order $u \sum_i r_i$, with twiddles computed accurately; we do not state a theorem. *Observed:* the round trip, forward and inverse, on Gaussian random data had relative $2$-norm error $16u$ at $n = 360$, $10u$ at $n = 1000$, $32u$ at $n = 3^7 = 2187$ and $23u$ at $n = 8640$. The tests use the tolerance $64 (r_1 + \cdots + r_t + 1)\, u \lVert X \rVert_2$.

## Properties

- **Any composite length.** Works for every $n$, but is fast only when $n$ has small prime factors.
- **Order of the radices.** Any order gives the same DFT; the order changes the memory access pattern and the rounding, not the result in exact arithmetic.
- **Exact over rings.** Over $\mathbb{Z}/p\mathbb{Z}$, any $n$ dividing $p - 1$ works, with exact results.
- **Recursive and not in place.** As written; iterative in-place forms exist.
- **Decimation in time.** This form splits the input; splitting the output instead (decimation in frequency) gives the same cost.

## Variants and improvements

- **Decimation in frequency.** Apply the length-$r$ DFTs first, then the twiddles, then recurse on contiguous blocks; the output comes out in digit-reversed order.
- **Higher radices.** Radix $4$ and radix $8$ butterflies reduce multiplications and memory passes; FFT libraries generate optimized butterflies ("codelets") for many small radices.
- **Prime-factor algorithm.** When the factors are coprime, the [Good-Thomas mapping](/chinese-remainder-theorem-fft/) based on the Chinese remainder theorem removes the twiddle factors entirely.
- **Large prime factors.** A prime radix $r$ can be computed by [Rader's algorithm](/rader-fft/) as a cyclic convolution of length $r - 1$, or by [Bluestein's algorithm](/bluestein-fft/), keeping the total cost $O(n \log n)$ for every $n$.
- **Minimal multiplications.** The [Winograd Fourier transform algorithm](/winograd-fourier-transform/) nests short DFTs with few multiplications.
- **Split radix.** For powers of two, mixing radix $2$ and radix $4$ in one step gives the [split-radix FFT](/split-radix-fft/).

## When to use it

Use it whenever the length is not a power of two but has only small prime factors, for example lengths fixed by the data, such as $360$ angular samples or $1000$ time steps, where padding to a power of two would change the problem (a cyclic transform of a padded length is a different transform). Use radix $4$ or $8$ butterflies even for powers of two, to save multiplications and memory passes. For lengths with a large prime factor, combine it with Rader or Bluestein.

## Pitfalls

- **The root of the subproblems.** The subsequences use $\omega^r$, of order $m$; the small DFTs use $\omega^m$, of order $r$. Mixing them up gives wrong values that still pass the tests with an impulse or a constant input.
- **Index maps.** The input split is $j = rq + l$ and the output index is $k + ms$; writing the outputs at $rk + s$ instead gives a permuted transform.
- **Twiddles from repeated multiplication.** Over $\mathbb{C}$, take the twiddle table from the exact angles; powers built by repeated multiplication accumulate error proportional to the exponent.
- **Roots over a ring.** Modulo $p$, $\omega$ must have order exactly $n$. With an element of smaller order the program still returns $\sum_j x_j \omega^{jk}$, but that transform is not invertible and does not give cyclic convolution. Checking $\omega^{n/q} \ne 1$ for each prime $q \mid n$ is enough.
- **Prime lengths.** A large prime factor gives quadratic cost silently.

## Implementations

The Python implementation in [impl/python/mixed_radix_fft.py](impl/python/mixed_radix_fft.py) follows the main block, with recursion depth $t$, a table of the $n$ powers of $\omega$ taken from the exact angles over $\mathbb{C}$, an exact branch modulo a prime, and an inverse flag. The tests compare it with the direct $O(n^2)$ DFT: exactly modulo $17$, $97$ and $998244353$ for every length below $130$ that divides $p - 1$ (including $3, 6, 7, 12, 14, 17, 24, 48, 96, 119$), with several orders of the radices and the inverse; and over $\mathbb{C}$ for every length from $1$ to $64$ and for $96$, $100$, $210$, $243$ and $360$, within the tolerance above, plus a round trip and Parseval's identity at $n = 8640$.

## History

Gauss split a transform of length $n_1 n_2$ into transforms of lengths $n_1$ and $n_2$ about 1805, in work published in 1866 (Heideman, Johnson and Burrus, 1984). Cooley and Tukey (1965) published the splitting for a general composite $n = r_1 r_2 \cdots$ with its operation count. Singleton (1969) published a mixed-radix program with special butterflies for the factors $2$, $3$, $4$ and $5$, which was widely used. Van Loan (1992) presents the radix-$r$ and mixed-radix forms as factorizations of the DFT matrix.

## References
