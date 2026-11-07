---
tag: 8K6AGB
kind: algorithm
slug: rader-fft
name: Rader's algorithm
aliases:
- Rader's FFT
- Rader FFT
- prime-length FFT
area: algebra/fast-transforms
level: advanced
summary: Computes a prime-length DFT as a cyclic convolution of length p-1 using a primitive root.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a prime), L: the inner FFT length (the least power of two at least 2n − 3)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  additions: {worst: 3 L lg L + 3n − 4}
  multiplications: {worst: (3/2) L lg L + 2L}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1968
  people: [Charles M. Rader]
  note: Rader (1968) reindexed a DFT of prime length by a primitive root, turning it into a cyclic convolution of length n − 1. Winograd (1978) used the same reduction in his short-length DFT algorithms.
prereqs: [discrete-fourier-transform, primitive-root, convolution-via-fft]
see_also: [bluestein-fft, mixed-radix-fft, winograd-fourier-transform, chinese-remainder-theorem-fft, circular-convolution, number-theoretic-transform, multiplicative-group-modulo-n, fermat-prime]
sources:
  - paper: doi:10.1109/PROC.1968.6477
    title: Charles M. Rader, Discrete Fourier transforms when the number of data samples is prime, Proceedings of the IEEE 56(6), 1968
    locator: pp. 1107 to 1108 (the permutation by a primitive root and the cyclic convolution of length n − 1)
  - paper: doi:10.1090/S0025-5718-1978-0468306-4
    title: Shmuel Winograd, On computing the discrete Fourier transform, Mathematics of Computation 32(141), 1978
    locator: pp. 175 to 199 (prime-length DFTs reduced to cyclic convolutions, with few multiplications)
  - paper: doi:10.1109/JPROC.2004.840301
    title: Matteo Frigo and Steven G. Johnson, The design and implementation of FFTW3, Proceedings of the IEEE 93(2), 2005
    locator: pp. 216 to 231 (the use of Rader's algorithm for large prime sizes)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 4, Selected Topics, Section 4.2 (prime factor frameworks and the reduction of prime-length DFTs to convolution)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2, The Discrete Fourier Transform and the Fast Fourier Transform (cyclic convolution by the DFT)
---

Rader's algorithm computes the [discrete Fourier transform](/discrete-fourier-transform/) of a prime length $n$, where the Cooley-Tukey splitting has nothing to split. It uses a [primitive root](/primitive-root/) $g$ modulo $n$ to renumber the nonzero indices as $g^0, g^1, \ldots, g^{n-2}$. In the new order the product $jk$ of two indices becomes a sum of exponents, so the $n - 1$ nonzero outputs become a [cyclic convolution](/circular-convolution/) of length $n - 1$ of the reordered input with a fixed sequence of roots of unity. That convolution is computed with FFTs ([convolution via FFT](/convolution-via-fft/)), of length $n - 1$ itself when it has small factors, or of a power of two at least $2n - 3$ in general. So every prime length costs $\Theta(n \log n)$, and together with the [mixed-radix FFT](/mixed-radix-fft/) this gives an $O(n \log n)$ FFT for every $n$.

## In plain words

When the length is prime, the usual trick of splitting the data into equal piles does not work. Rader's idea is to shuffle the data into a clever order first. Number theory gives an order in which multiplying two positions together becomes adding their places in the order. In that order, the transform turns into a rolling sum of products, a convolution, which an FFT of a convenient length can compute quickly. The first output, the plain sum, is handled separately.

## The problem

**Notation.** As on all pages of fast transforms, $n$ is the transform length, here a prime, and $\omega = \omega_n = e^{-2\pi i/n}$ over $\mathbb{C}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign). Over a commutative ring $R$, $\omega$ is any element of multiplicative order $n$; since $n$ is prime, $\omega \ne 1$ and $\omega^n = 1$ suffice. The DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$, and the inverse is $x_j = \frac1n \sum_k X_k \omega^{-jk}$. Write $N = n - 1$, $g$ for a primitive root modulo $n$, and $g^{-m}$ for the inverse of $g^m$ modulo $n$. The cyclic convolution of $a, b \in R^N$ is $(a * b)_p = \sum_{q=0}^{N-1} a_q b_{(p - q) \bmod N}$.

**Input.** $x \in R^n$ with $n$ prime.

**Output.** $X = (X_0, \ldots, X_{n-1})$.

**Cost model.** Additions (with subtractions) and multiplications in $R$ are counted separately, at unit cost, in the [real RAM](/real-ram/) for $\mathbb{C}$ or the word RAM for $\mathbb{Z}/P\mathbb{Z}$. Index arithmetic modulo $n$, the search for $g$, and the tables of roots of unity are not counted. The inner convolution is done by radix-2 FFTs of length $L$, the least power of two with $L \ge 2N - 1 = 2n - 3$.

## The algorithm

Since $g$ generates the multiplicative group modulo $n$, every $j \ne 0$ is $g^q$ for one $q \in [0, N)$ and every $k \ne 0$ is $g^{-p}$ for one $p \in [0, N)$. Then $jk \equiv g^{q - p}$, and

$$X_{g^{-p}} = x_0 + \sum_{q=0}^{N-1} x_{g^q}\, \omega^{g^{q-p}} = x_0 + (a * b)_p, \qquad a_q = x_{g^q}, \quad b_m = \omega^{g^{-m}},$$

since $b_{(p - q) \bmod N} = \omega^{g^{q - p}}$ (exponents of $g$ are taken modulo $N$ by Fermat's little theorem). The output $X_0 = \sum_j x_j$ is separate.

```pseudo id=main
RADER-FFT(x, ω)          ▷ n = length(x) prime; ω of order n
L1  g ← a primitive root modulo n; N ← n − 1
L2  a_q ← x_(g^q mod n) for q = 0, …, N − 1             ▷ the input in the order of powers of g
L3  b_m ← ω^(g^(−m) mod n) for m = 0, …, N − 1          ▷ fixed: depends only on n and ω
L4  c ← CYCLIC-CONVOLUTION(a, b)                       ▷ length N, by FFTs of length L ≥ 2N − 1
L5  X_0 ← x_0 + x_1 + ⋯ + x_(n−1)
L6  for p ← 0 to N − 1 do
L7      X_(g^(−p) mod n) ← x_0 + c_p
L8  return X
```

Line L4 pads $a$ and $b$ with zeros to length $L$, computes $A = \mathrm{FFT}_L(a)$ and $B = \mathrm{FFT}_L(b)$, multiplies pointwise, applies the inverse FFT of length $L$ to get the linear convolution $\ell$ of length $2N - 1$, and folds it: $c_p = \ell_p + \ell_{p+N}$, where $\ell_{p+N} = 0$ for $p = N - 1$. The inverse DFT is the same program with $\omega^{-1}$ and a final division by $n$.

## Example

Take $n = 5$ modulo the prime $P = 41$, where $40 = 8 \cdot 5$ allows both a root of order $5$ and an inner length $L = 8 \ge 2n - 3 = 7$. The least primitive root of $41$ is $6$, so $\omega = 6^8 \bmod 41 = 10$, with powers $1, 10, 18, 16, 37$. The least primitive root of $5$ is $g = 2$, with powers $2^q = 1, 2, 4, 3$ and inverses $2^{-m} = 1, 3, 4, 2$. Transform $x = (1, 2, 3, 4, 5)$.

| q or m | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| g^q mod 5 | 1 | 2 | 4 | 3 |
| a_q = x_(g^q) | 2 | 3 | 5 | 4 |
| g^(−m) mod 5 | 1 | 3 | 4 | 2 |
| b_m = ω^(g^(−m)) | 10 | 16 | 37 | 18 |
| c_p = (a * b)_p mod 41 | 36 | 13 | 39 | 21 |
| X_(g^(−p)) = 1 + c_p | X_1 = 37 | X_3 = 14 | X_4 = 40 | X_2 = 22 |

For instance $c_0 = a_0 b_0 + a_1 b_3 + a_2 b_2 + a_3 b_1 = 20 + 54 + 185 + 64 = 323 = 7 \cdot 41 + 36$. With $X_0 = 15$, the result is $X = (15, 37, 22, 14, 40)$, which equals the direct DFT; for example $X_1 = 1 + 20 + 54 + 64 + 185 = 324 \equiv 37$. Running the program with $\omega^{-1}$ and dividing by $5$ returns $x$. All numbers were checked by script.

## Correctness

The map $q \mapsto g^q \bmod n$ is a bijection from $[0, N)$ to the nonzero residues, because $g$ has order $N$; the same holds for $p \mapsto g^{-p}$. So line L2 is a permutation of $x_1, \ldots, x_{n-1}$, and line L7 writes each $X_k$, $k \ne 0$, exactly once. For $k = g^{-p}$ and $j = g^q$, $jk \equiv g^{q-p} \pmod n$, and $\omega^{jk}$ depends only on $jk \bmod n$ because $\omega^n = 1$. Hence $X_k = x_0 + \sum_q a_q \omega^{g^{q-p}} = x_0 + \sum_q a_q b_{(p-q) \bmod N}$, which is $x_0 + c_p$. Line L5 handles $k = 0$. The full proof, including the convolution by FFTs and the operation counts, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Operations.** With radix-2 FFTs of length $L$, each of the three transforms in line L4 costs $\frac{L}{2} \lg L$ multiplications and $L \lg L$ additions; the pointwise product and the scaling by $1/L$ cost $2L$ multiplications; the folding costs $N - 1$ additions. Lines L5 and L7 cost $n - 1$ and $N$ additions. In total

$$\tfrac32 L \lg L + 2L \text{ multiplications}, \qquad 3 L \lg L + 3n - 4 \text{ additions},$$

and since $2n - 3 \le L < 4n - 6$, this is $\Theta(n \log n)$, for every input. The transform $B$ of the fixed sequence $b$ depends only on $n$ and $\omega$; precomputing it, as libraries do for repeated transforms of the same size, saves $\frac{L}{2} \lg L$ multiplications and $L \lg L$ additions, and the scaling can be folded into $B$, saving $L$ more multiplications.

**Shorter convolutions.** If $N = n - 1$ has only small factors, the cyclic convolution can be computed by FFTs of length exactly $N$, with the [mixed-radix FFT](/mixed-radix-fft/), and no padding. For a Fermat prime such as $n = 17$ or $257$, $N$ is a power of two. Winograd's short DFTs compute the convolution for small $n$ with very few multiplications instead.

**Space.** $\Theta(L) = \Theta(n)$ for the padded arrays.

**Rounding errors.** Over $\mathbb{C}$ in floating point, the result is the composition of three FFTs of length $L$, each covered by Higham's bound of order $u \lg L$ (Theorem 24.2), and a pointwise product with the fixed transform $B$. *Not proved here:* we do not state a combined bound. *Observed:* on Gaussian random data the relative $2$-norm error of a forward and inverse round trip was $27u$ at $n = 257$, $37u$ at $n = 1009$, $49u$ at $n = 8191$ and $57u$ at $n = 65537$. The tests use the tolerance $64 (\lg n + 3)\, u \lVert X \rVert_2$.

## Properties

- **Prime lengths only.** For composite $n$, the nonzero residues do not form a cyclic group under multiplication that covers all indices; use the mixed-radix or prime-factor algorithm.
- **Exact over rings.** Modulo a prime $P$ with $n \mid P - 1$ and $L \mid P - 1$, the result is exact.
- **A fixed permutation.** The input and output permutations depend only on $n$ and $g$.
- **Deterministic.** The operation count does not depend on the data.

## Variants and improvements

- **Convolution of length exactly $n - 1$.** When $n - 1$ is smooth, recurse with the mixed-radix FFT of length $n - 1$ (FFTW does this), avoiding the padding.
- **Winograd's short DFTs.** For small primes, the cyclic convolution is computed by a minimal-multiplication algorithm based on the factorization of $t^{N} - 1$, which is the heart of the [Winograd Fourier transform algorithm](/winograd-fourier-transform/).
- **Prime powers.** Rader's reindexing extends to $n = q^e$ using the cyclic group of units modulo $q^e$ for odd $q$, with separate handling of the non-units.
- **Bluestein's algorithm.** The [chirp z-transform](/bluestein-fft/) turns a DFT of any length into a convolution, using $jk = \frac12 (j^2 + k^2 - (k - j)^2)$; it needs no primitive root but needs $\omega^{1/2}$.
- **Multidimensional and prime-factor use.** In the [Good-Thomas algorithm](/chinese-remainder-theorem-fft/) each prime factor of $n$ becomes an axis, and Rader handles the prime axes.

## When to use it

Use it inside a general-length FFT for prime factors that are too large for a direct butterfly, as FFTW does, and for prime-length transforms in exact arithmetic modulo a prime, where Bluestein's square root of $\omega$ may not exist. For a one-off prime-length transform in floating point, Bluestein's algorithm is often simpler and comparable in speed.

## Pitfalls

- **The direction of the permutation.** The input is reordered by $g^q$ and the output by $g^{-p}$; using $g^p$ for both gives a correlation, not a convolution, and permuted outputs.
- **Forgetting $x_0$.** Every nonzero output gets $x_0$ added, and $X_0$ is the full sum; neither is part of the convolution.
- **Cyclic, not linear.** Padding to $L \ge 2N - 1$ and then forgetting to fold $\ell_{p+N}$ back gives a wrong result.
- **Exponents modulo $N$.** Powers of $g$ are periodic with period $N = n - 1$, not $n$; indices of $b$ are taken modulo $N$.
- **Roots modulo $P$.** Over $\mathbb{Z}/P\mathbb{Z}$, $P - 1$ must be divisible by $n$ (for $\omega$) and by $L$ (for the inner FFT).

## Implementations

The Python implementation in [impl/python/rader_fft.py](impl/python/rader_fft.py) follows the main block, with the inner cyclic convolution by radix-2 FFTs of length $L$ over $\mathbb{C}$ (twiddles from the exact angles) or modulo a prime $P$, and an inverse flag. The tests compare it with the direct $O(n^2)$ DFT: exactly modulo $17$, $97$ and $998244353$ for the prime lengths they allow ($2$, $3$, $7$ and $17$), and modulo a searched prime $P \equiv 1$ modulo $n$ and $L$ for every prime $n < 140$; and over $\mathbb{C}$ for every prime below $200$, with round trips for every prime below $400$ and at $n = 8191$, within the tolerance above; plus zeros, an impulse, a constant and $n = 2$.

## History

Rader (1968) published the reduction: for a prime number of samples, a permutation by a primitive root turns the DFT into a cyclic convolution of length $n - 1$, which can be computed by FFTs. Winograd (1978) combined this reduction with minimal-multiplication algorithms for cyclic convolution to obtain his short DFT algorithms. FFTW uses Rader's algorithm for large prime factors (Frigo and Johnson, 2005).

## References
