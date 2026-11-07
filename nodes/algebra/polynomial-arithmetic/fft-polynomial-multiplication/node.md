---
tag: WT2CHV
kind: algorithm
slug: fft-polynomial-multiplication
name: FFT-based polynomial multiplication
aliases:
- convolution by FFT
- FFT multiplication
- NTT multiplication
area: algebra/polynomial-arithmetic
level: core
summary: Multiplies two degree-n polynomials in O(n log n) by evaluating, multiplying pointwise and interpolating.
solves: [polynomial-multiplication]
model: blum-shub-smale-machine
complexity:
  vars: {n: a bound on the number of coefficients of each factor}
  time: {worst: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, in_place: false, recursive: false}
history:
  year: 1965
  people: [James Cooley, John Tukey, John Pollard, Arnold Schonhage, Volker Strassen]
  note: Cooley and Tukey published the FFT in 1965; Pollard gave the exact transform over finite fields in 1971, and Schonhage and Strassen used it for fast integer multiplication in 1971.
prereqs: [point-value-representation, evaluation-interpolation-paradigm, fast-fourier-transform, roots-of-unity, dense-polynomial-representation]
see_also: [number-theoretic-transform, convolution-theorem, convolution, karatsuba-multiplication, schonhage-strassen-multiplication, kronecker-substitution, chinese-remainder-theorem, fast-polynomial-division]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 8.2, The Discrete Fourier Transform and the Fast Fourier Transform (primitive roots of unity, the convolution theorem and FFT multiplication); Section 8.3, Schonhage and Strassen's multiplication algorithm; Section 8.4, Multiplication in Z[x] and R[x, y]
  - book: isbn:9780262046305
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 30, Polynomials and the FFT (Section 30.1, Representing polynomials; Section 30.2, The DFT and FFT, with the convolution theorem)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3.4, Use of the fast Fourier transform (FFT); Section 2.3, The Fourier transform (2.3.1 Theoretical setting, 2.3.2 The fast Fourier transform, 2.3.3 The Schonhage-Strassen algorithm)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 4.3.3, How fast can we multiply? (multiplication by discrete Fourier transforms)
  - paper: doi:10.1090/S0025-5718-1965-0178586-1
    title: James W. Cooley and John W. Tukey, An algorithm for the machine calculation of complex Fourier series, Mathematics of Computation 19(90) (1965), 297 to 301
    locator: the whole paper
  - paper: doi:10.1090/S0025-5718-1971-0301966-0
    title: J. M. Pollard, The fast Fourier transform in a finite field, Mathematics of Computation 25(114) (1971), 365 to 374
    locator: the transform over finite fields and its use for exact convolution
---

FFT multiplication computes the product of two polynomials of degree less than $n$ in $O(n \log n)$ ring operations, against $\Theta(n^2)$ for the schoolbook method. It is the [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/) with the $N$-th roots of unity as points: the [fast Fourier transform](/fast-fourier-transform/) evaluates both factors at all $N$ points, the values are multiplied in pairs, and the inverse transform interpolates. It needs a ring with a suitable root of unity, such as $\mathbb{C}$ with floating point arithmetic or $\mathbb{Z}/p\mathbb{Z}$ for a prime $p = c \cdot 2^k + 1$, where it is called the [number-theoretic transform](/number-theoretic-transform/). It is the base of fast division, fast evaluation and interpolation, and fast gcd algorithms.

## In plain words

Multiplying two polynomials the school way multiplies every coefficient of one by every coefficient of the other, which is slow for long polynomials. There is a faster way. A polynomial is also fixed by its values at enough points, and at each point the value of a product is the product of the values. So we can compute the values of both polynomials at many points, multiply them point by point, and rebuild the product from its values.

In general, computing values at many points is as slow as the school method. But for one special choice of points, the roots of unity, the fast Fourier transform computes all the values with a few steps per point. The same transform, run backwards, rebuilds the product. The whole method takes a little more than a constant number of steps per coefficient.

## The problem

This is the [polynomial multiplication](/polynomial-multiplication/) problem. Let $R$ be a commutative ring with $1$. Given $f = \sum_{i<m} a_i x^i$ and $g = \sum_{j<n} b_j x^j$ in $R[x]$ as normalized coefficient lists, compute $h = fg$, that is $h_k = \sum_{i+j=k} a_i b_j$ for $0 \le k \le m + n - 2$. This is the linear convolution of the two coefficient sequences.

The algorithm needs the following from $R$. Let $N = 2^k \ge m + n - 1$. An element $\omega \in R$ is a **principal $N$-th root of unity** if $\omega^N = 1$ and $\omega^{N/2} = -1$. The algorithm also needs $N$ to be a unit of $R$, that is $2$ must be invertible. Over a field, a principal $N$-th root of unity is the same as a primitive one. Examples: $\omega = e^{2\pi i/N}$ in $\mathbb{C}$, and $\omega = g^{(p-1)/N}$ in $\mathbb{Z}/p\mathbb{Z}$ for a prime $p$ with $N \mid p - 1$ and a generator $g$ of $(\mathbb{Z}/p\mathbb{Z})^*$. For $p = 998244353 = 119 \cdot 2^{23} + 1$, $g = 3$ and every $N \le 2^{23}$ works.

Costs are ring operations of $R$ in the algebraic complexity model (the [Blum-Shub-Smale machine](/blum-shub-smale-machine/) over $R$), with $M(n)$ for the cost of multiplying two polynomials of degree less than $n$. This algorithm shows $M(n) = O(n \log n)$ for rings with the roots above.

## The algorithm

The discrete Fourier transform of a list $c = [c_0, \ldots, c_{N-1}]$ at $\omega$ is the list of values $\operatorname{DFT}_\omega(c)_i = \sum_{j<N} c_j \omega^{ij} = c(\omega^i)$, the values of the polynomial $c$ at the powers of $\omega$. The multiplication pads both factors to length $N$, transforms, multiplies pointwise, and transforms back with $\omega^{-1}$ and a division by $N$.

```pseudo id=main
FFT-MULTIPLY(a, b)                       ▷ m = |a|, n = |b|; ω principal N-th root, N a unit
L1  if m = 0 or n = 0 then return [ ]
L2  N ← the least power of 2 with N ≥ m + n − 1
L3  pad a and b with zeros to length N
L4  A ← DFT(a, ω); B ← DFT(b, ω)
L5  for i ← 0 to N − 1 do C[i] ← A[i] · B[i]
L6  c ← N⁻¹ · DFT(C, ω⁻¹)
L7  return c[0 .. m + n − 2], normalized
```

The transform is computed by the iterative radix-2 Cooley-Tukey FFT. It first puts the entries in bit-reversed order, then combines blocks of length 1 into blocks of length 2, 4, and so on up to $N$. Each combination step is a butterfly: from the transform $E$ of the even-indexed part and $O$ of the odd-indexed part of a block, it forms $E_j + w O_j$ and $E_j - w O_j$.

```pseudo id=dft
DFT(a, ω)                                ▷ in place; N = |a| = 2^k; ω^N = 1, ω^(N/2) = −1
F1  permute a so that a[i] and a[rev(i)] swap, rev = reversal of the k binary digits
F2  len ← 2
F3  while len ≤ N do
F4      w_len ← ω^(N/len)                ▷ a principal root of order len
F5      for s ← 0 to N − 1 step len do
F6          w ← 1
F7          for j ← 0 to len/2 − 1 do
F8              t ← w · a[s + j + len/2]; x ← a[s + j]
F9              a[s + j] ← x + t; a[s + j + len/2] ← x − t
F10             w ← w · w_len
F11     len ← 2 · len
```

**Why the pointwise product is the product.** The DFT is evaluation at $1, \omega, \ldots, \omega^{N-1}$, and evaluation is a ring homomorphism, so $C_i = f(\omega^i) g(\omega^i) = h(\omega^i)$. The inverse transform turns these values back into coefficients, because $\sum_{i<N} \omega^{i(l - j)}$ is $N$ for $l = j$ and $0$ for $l \ne j$. Since $\deg h < N$, the coefficients are those of $h$. If $N$ were smaller than $m + n - 1$, the result would be the cyclic convolution, $h \bmod (x^N - 1)$.

**Integers, other moduli and rationals.** Over $\mathbb{Z}$, the coefficients of $h$ satisfy $|h_k| \le \min(m, n) \max|a_i| \max|b_j| = B$. Compute $h$ modulo several primes $p_1, \ldots, p_r$ of the form $c \cdot 2^k + 1$ with $\prod p_i > 2B$, and rebuild each coefficient by the [Chinese remainder theorem](/chinese-remainder-theorem/) in the symmetric range. A product over $\mathbb{Z}/m\mathbb{Z}$ for any $m$, for example $m = 2, 3, 7$, which have no roots of unity of large order, is computed over $\mathbb{Z}$ from the representatives in $[0, m)$ and then reduced. Over $\mathbb{Q}$, multiply by the common denominators first. The implementation does all three.

## Example

Multiply $f = 1 + 2x$ by $g = 3 - x$ over $\mathbb{Z}/17\mathbb{Z}$. The product has 3 coefficients, so $N = 4$. Since $4^2 = 16 = -1$, $\omega = 4$ is a principal 4th root of unity, and $\omega^{-1} = 13$, $N^{-1} = 4^{-1} = 13$. The points are $1, 4, 16, 13$.

**Forward transform of $a = [1, 2, 0, 0]$.** Line F1 swaps positions 1 and 2, giving $[1, 0, 2, 0]$. With len $= 2$, $w_{\text{len}} = \omega^2 = 16 = -1$, but only $w = 1$ is used: the block $[1, 0]$ becomes $[1 + 0, 1 - 0] = [1, 1]$, and $[2, 0]$ becomes $[2, 2]$. With len $= 4$ and $w_{\text{len}} = 4$:

| $j$ | $w$ | $x = a[j]$ | $t = w \cdot a[j + 2]$ | $a[j] = x + t$ | $a[j + 2] = x - t$ |
|---|---|---|---|---|---|
| 0 | 1 | 1 | 2 | 3 | $-1 = 16$ |
| 1 | 4 | 1 | 8 | 9 | $-7 = 10$ |

So $A = [3, 9, 16, 10]$, and indeed $f(1) = 3$, $f(4) = 9$, $f(16) = 33 = 16$, $f(13) = 27 = 10$.

**The rest.** In the same way $B = \operatorname{DFT}([3, 16, 0, 0]) = [2, 16, 4, 7]$, the values of $3 - x$. Line L5 gives $C = [6, 144, 64, 70] = [6, 8, 13, 2]$ modulo 17. The inverse transform with $\omega^{-1} = 13$ and the factor $13$ gives $[3, 5, 15, 0]$, that is $3 + 5x - 2x^2$ since $15 = -2$. This is $(1 + 2x)(3 - x) = 3 + 5x - 2x^2$. Over $\mathbb{Z}$ the bound is $B = 1 \cdot 2 \cdot 3 = 6$, and $17 > 2B$, so the result modulo 17 already determines the integer product.

## Correctness

The proof has three parts. First, the iterative DFT computes $\sum_{j} a_j \omega^{ij}$: after the stage with block length $L$, each block holds the length-$L$ transform, at $\omega^{N/L}$, of a subsequence of the input with stride $N/L$, and the butterfly of lines F8 and F9 is the even-odd split $c(z) = c_{\text{even}}(z^2) + z\, c_{\text{odd}}(z^2)$, together with $(\omega^{N/2L})^{L} = \omega^{N/2} = -1$. Second, for a principal root, $\sum_{i<N} \omega^{ij} = 0$ for $0 < j < N$, so the inverse DFT, with $\omega^{-1}$ and $N^{-1}$, inverts the DFT. Third, the pointwise product of the values is the list of values of $fg$, and $\deg fg < N$. The full proof is in the proof file.

## Complexity

All bounds in this section are proved, in ring operations of $R$, unless they are marked as observed.

**The transform.** Each of the $k = \log_2 N$ stages does $N/2$ butterflies, each with one multiplication and two additions, plus $N/2$ multiplications to update $w$ at line F10. So one DFT costs $N \log_2 N$ multiplications and $N \log_2 N$ additions with this code, and $\tfrac12 N \log_2 N$ multiplications if the powers of $\omega$ are precomputed. The bit-reversal permutation moves data but does no ring operation.

**The product.** Three transforms, $N$ pointwise products and $N$ scalings by $N^{-1}$ give $O(N \log N)$. Since $N < 2(m + n - 1)$, the total is $O(n \log n)$ for factors with at most $n$ coefficients, and $\Theta(n \log n)$ in each case, because the transforms run in full whatever the coefficients are. The extra space is $\Theta(N)$ for the padded arrays. So $M(n) = O(n \log n)$ in rings with principal roots of unity of all power-of-two orders.

**Unbalanced factors.** If $m \gg n$, cut $f$ into $\lceil m/n \rceil$ blocks of $n$ coefficients, multiply each by $g$ with a transform of length $O(n)$, and add the overlapping results. The cost is $O(m \log n)$ instead of $O(m \log m)$.

**Over $\mathbb{Z}$ and on a real machine.** For $\mathbb{Z}/p\mathbb{Z}$ with $p$ below the word size, each ring operation is $O(1)$ time on the [word RAM](/word-ram/), so the time is $O(n \log n)$. Over $\mathbb{Z}$ with coefficients of absolute value at most $2^\ell$, the number of primes of about 30 binary digits is $r = O(1 + (\ell + \log n)/30)$, and the time is $O(r\, n \log n + n r^2)$ word operations, the last term for the CRT. Von zur Gathen and Gerhard, Section 8.4, and Brent and Zimmermann, Section 2.3, analyze this and the alternative of packing the coefficients into one integer by [Kronecker substitution](/kronecker-substitution/).

**Rings without roots of unity.** Schonhage and Strassen's method adjoins virtual roots of unity by working in $R[y]/(y^{2^t} + 1)$, where $y$ is a principal root. It multiplies over any commutative ring in which 2 is a unit in $O(n \log n \log\log n)$ ring operations, and Cantor and Kaltofen extended this to every commutative ring and to divisions by 3 instead of 2 (von zur Gathen and Gerhard, Section 8.3). This is the best general bound for $M(n)$ in the algebraic model.

**Crossover (observed).** For small $n$ the schoolbook method and then Karatsuba are faster, because the transform has a large constant factor. The crossover depends on the ring and the machine. Exact NTT libraries over word-size primes typically switch to the transform at degrees between a few dozen and a few hundred; floating point FFT codes switch at similar sizes. These are measurements, not theorems.

## Properties

- **Exact over finite fields, approximate over $\mathbb{C}$.** The NTT is exact. A floating point FFT returns approximate coefficients, which are rounded to integers. The rounding is correct while the error is below $\tfrac12$; with 53-bit doubles this holds in practice when $N \cdot \max|a_i| \cdot \max|b_j|$ stays well below about $2^{50}$, but the rigorous bounds are smaller and depend on the implementation.
- **Not in place.** The factors are padded to length $N$, so it needs $\Theta(N)$ extra space. The transform itself is in place.
- **Oblivious.** The sequence of ring operations does not depend on the coefficients, only on $m$ and $n$. This makes it suitable for hardware and for constant-time code.
- **Squaring is cheaper.** For $f^2$, one forward transform suffices: two transforms instead of three.
- **Powers of two.** The radix-2 form needs $N = 2^k$, which can almost double the work when $m + n - 1$ is just above a power of two.

## Variants and improvements

- **Mixed radix and truncated transforms.** Transforms of length $3 \cdot 2^k$ or other smooth lengths, and the truncated Fourier transform of van der Hoeven, avoid the jump in cost at powers of two.
- **Transform reuse.** When one factor is fixed, as in [fast division](/fast-polynomial-division/) by Newton iteration or in [multipoint evaluation](/fast-multipoint-evaluation/), keep its transform and save one third of the work. The middle product, which computes only the middle coefficients of a product, saves more (Brent and Zimmermann, Section 3.3.2).
- **Three primes and Garner.** For coefficients below about $2^{60}$ and lengths up to $2^{23}$, three NTT primes near $2^{30}$ suffice, and Garner's algorithm rebuilds the result. This is the usual method for multiplication modulo an arbitrary 30-bit prime, such as $10^9 + 7$.
- **Splitting the coefficients.** Over $\mathbb{C}$, write each coefficient as $a_i = a_i' + 2^{s} a_i''$ with small parts, and do several smaller-precision products. This keeps the rounding error under control for large coefficients.
- **Schonhage-Strassen.** Use the ring $\mathbb{Z}/(2^K + 1)\mathbb{Z}$, where $2$ is a root of unity and multiplication by its powers is a shift. See [Schonhage-Strassen multiplication](/schonhage-strassen-multiplication/) for integers and the polynomial version above for rings without roots.
- **Multivariate polynomials.** Use a multidimensional transform, or reduce to one variable by Kronecker substitution.

## When to use it

Use FFT multiplication for dense polynomials of large degree, above a crossover that is found by measurement, over rings with suitable roots of unity: $\mathbb{Z}/p\mathbb{Z}$ for NTT primes, and $\mathbb{C}$ or $\mathbb{R}$ when floating point error is acceptable. Over $\mathbb{Z}$ and over $\mathbb{Z}/m\mathbb{Z}$ for general $m$, use several NTT primes and the CRT, or Kronecker substitution with a fast integer multiplication. For small degrees use the schoolbook method, and for medium degrees [Karatsuba](/karatsuba-multiplication/). For sparse polynomials use a sparse method: the transform length depends on the degree, not on the number of terms.

## Pitfalls

- **Transform too short.** With $N < m + n - 1$, the result is the cyclic convolution, and the top coefficients wrap around onto the bottom ones. For $f = g = 1 + x$ and $N = 2$, the result is $2 + 2x$, which is $(1 + x)^2 \bmod (x^2 - 1)$, instead of $1 + 2x + x^2$.
- **No root of unity of the needed order.** Over $\mathbb{Z}/p\mathbb{Z}$, a root of order $N$ exists only if $N \mid p - 1$. For $p = 10^9 + 7$, $p - 1 = 2 \cdot 500000003$, so only $N \le 2$ works. Use NTT primes and the CRT, as the implementation does.
- **Forgetting the scaling.** The inverse transform needs the factor $N^{-1}$. Without it, every coefficient is $N$ times too large.
- **Wrong root for the inverse.** The inverse uses $\omega^{-1}$, not $\omega$. With $\omega$ in both directions the result is reversed: $c_{N - j}$ appears at position $j$.
- **Too few primes.** The product of the CRT primes must exceed $2B$ for the bound $B$ on the coefficients, with the factor 2 for the sign. With a smaller product, large coefficients come out reduced, and nothing signals the error.
- **Rounding over $\mathbb{C}$.** With large coefficients or long inputs, the floating point error exceeds $\tfrac12$ and rounding gives a wrong integer. Bound the error, or use the exact transform.
- **Overflow in fixed width.** Modulo a 30-bit prime, products of two residues need 60 binary digits. In a language with 64-bit integers, reduce after each product; for primes near $2^{62}$ use 128-bit products or Montgomery multiplication.

## Implementations

## History

Gauss had found a fast Fourier transform method in 1805 for interpolating orbits of asteroids, but it was not published in his lifetime. Cooley and Tukey published the FFT in 1965, and its use for fast convolution and for polynomial and integer multiplication followed quickly. Pollard described the transform over finite fields in 1971, which makes the product exact. Schonhage and Strassen published their $O(n \log n \log\log n)$ integer multiplication in 1971, and Schonhage (1977) and Cantor and Kaltofen (1991) gave the versions for polynomials over arbitrary rings. Harvey and van der Hoeven reached $O(n \log n)$ for integer multiplication in 2021; see [Harvey-van der Hoeven multiplication](/harvey-van-der-hoeven-multiplication/).

## References
