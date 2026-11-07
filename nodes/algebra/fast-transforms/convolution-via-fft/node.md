---
tag: XX6TKR
kind: algorithm
slug: convolution-via-fft
name: Convolution via FFT
aliases:
- FFT-based convolution
- fast convolution
- FFT convolution
area: algebra/fast-transforms
level: core
summary: Computes convolution in O(n log n) by pointwise multiplication in the frequency domain.
solves: [convolution]
model: real-ram
complexity:
  vars: {m: the length of a, l: the length of b, N: the least power of two with N ≥ m + l - 1}
  time: {worst: Θ(N log N), average: Θ(N log N), best: Θ(N log N)}
  space: {extra: Θ(N)}
  multiplications: {worst: (3/2) N lg N + 2N}
  additions: {worst: 3 N lg N}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1966
  people: [Thomas G. Stockham Jr.]
  note: Stockham described convolution and correlation by the FFT in 1966, a year after the paper of Cooley and Tukey.
prereqs: [convolution, convolution-theorem, fast-fourier-transform]
see_also: [fft-polynomial-multiplication, number-theoretic-transform, inverse-fft, circular-convolution, schonhage-strassen-multiplication, chinese-remainder-theorem, bluestein-fft, karatsuba-multiplication]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Sections 30.1 and 30.2 (multiplying polynomials in point-value form at the complex roots of unity of order 2n, and the convolution theorem)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2 (fast convolution and polynomial multiplication by the FFT over a ring with a primitive root of unity)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 4, Section 4.2, Convolution (circulant and Toeplitz products by FFTs)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 22, Section 22.1, Convolution (cyclic and linear convolution by FFT, zero padding, and the error of floating-point convolution)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, Theorem 24.2 (the error bound of the radix-2 FFT used in the error analysis on this page), and Lemma 3.5 (the error of a complex multiplication)
  - paper: "Thomas G. Stockham Jr., High-speed convolution and correlation, AFIPS Spring Joint Computer Conference 28, 1966"
    locator: pp. 229 to 233
  - paper: doi:10.1090/S0025-5718-1971-0301966-0
    title: John M. Pollard, The fast Fourier transform in a finite field, Mathematics of Computation 25(114), 1971
    locator: pp. 365 to 374 (exact convolution by FFTs modulo primes)
---

Convolution via FFT computes the [linear convolution](/convolution/) $c = a * b$ of two sequences, $c_k = \sum_{i + j = k} a_i b_j$, with three [fast Fourier transforms](/fast-fourier-transform/) and one pointwise product. Pad $a$ and $b$ with zeros to a power-of-two length $N \ge m + \ell - 1$, transform both, multiply the transforms entry by entry, and transform back. The [convolution theorem](/convolution-theorem/) says the result is the cyclic convolution of the padded vectors, and the padding makes it equal to the linear one. The cost is $\Theta(N \log N)$ ring operations instead of the $\Theta(m\ell)$ of the direct sum. Over $\mathbb{Z}/p\mathbb{Z}$ with the [number-theoretic transform](/number-theoretic-transform/) the result is exact; over $\mathbb{C}$ it has a small, provable rounding error.

## In plain words

Multiplying two long polynomials term by term is slow, because every term of one meets every term of the other. There is a faster road. A polynomial is also fixed by its values at enough points. So compute the values of both polynomials at the same set of points, multiply the values point by point, which is cheap, and then turn the products back into a polynomial.

The trick is the choice of points: equally spaced points on a circle, where the fast Fourier transform does both the evaluation and the way back quickly. The only care needed is to use enough points, at least as many as the answer has terms. If there are too few, the end of the answer wraps around and spoils its start.

## The problem

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $R$ is a commutative ring, $N$ is the transform length and must be a power of two here, the DFT is $X_k = \sum_j x_j \omega^{jk}$, and the inverse has the factor $1/N$. Over $\mathbb{C}$, $\omega = \omega_N = e^{-2\pi i/N}$ (the statements also hold for $e^{+2\pi i/N}$). Over $\mathbb{Z}/p\mathbb{Z}$, $\omega$ is a principal $N$-th root of unity, which exists exactly when $N \mid p - 1$, and $N$ is a unit since $N < p$.

**Input.** $a = (a_0, \ldots, a_{m-1})$ and $b = (b_0, \ldots, b_{\ell - 1})$ over $R$, with $m, \ell \ge 1$.

**Output.** $c = a * b$ of length $L = m + \ell - 1$, with $c_k = \sum_{i} a_i b_{k-i}$ over $\max(0, k - \ell + 1) \le i \le \min(k, m - 1)$.

**Cost model.** Operations of $R$, with additions and multiplications counted separately. Over $\mathbb{Z}/p\mathbb{Z}$ with $p$ below the word size each is $O(1)$ on the [word RAM](/word-ram/). In floating point the error is analysed below.

## The algorithm

```pseudo id=main
FFT-CONVOLVE(a, b)       ▷ a[0 .. m − 1], b[0 .. l − 1]; returns c = a * b
L1  L ← m + l − 1
L2  N ← the least power of two with N ≥ L
L3  ω ← a principal N-th root of unity           ▷ e^(−2πi/N), or g^((p−1)/N) mod p
L4  A ← a followed by N − m zeros
L5  B ← b followed by N − l zeros
L6  FFT(A, ω), FFT(B, ω)
L7  for k ← 0 to N − 1 do C[k] ← A[k] · B[k]
L8  INVERSE-FFT(C, ω)                             ▷ FFT(C, ω^(−1)), then divide by N
L9  return C[0 .. L − 1]
```

FFT and INVERSE-FFT are the iterative radix-2 procedures of the [FFT page](/fast-fourier-transform/). Over $\mathbb{Z}/p\mathbb{Z}$ with a [primitive root](/primitive-root/) $g$ modulo $p$, line L3 takes $\omega = g^{(p-1)/N}$, which has order exactly $N$. For $p = 998244353 = 119 \cdot 2^{23} + 1$ and $g = 3$, this works for each $N \le 2^{23}$. When the exact result is a vector of integers and the arithmetic is in floating point, round each entry of the output to the nearest integer; the error bound below says when this is safe.

## Example

Over $\mathbb{Z}/17\mathbb{Z}$, convolve $a = (1, 2, 3)$ and $b = (4, 5)$. Then $L = 4$ and $N = 4$. Take $\omega = 4$, a principal $4$-th root of unity, since $4^2 = 16 \equiv -1$. (The choice $g^{(p-1)/N}$ with $g = 3$ gives the other one, $13 = 4^{-1}$.)

| step | vector |
|---|---|
| L4, A | 1 2 3 0 |
| L5, B | 4 5 0 0 |
| L6, F_4 A | 6 6 2 7 |
| L6, F_4 B | 9 7 16 1 |
| L7, C | 3 8 15 7 |
| L8, FFT with ω^(−1) = 13 | 16 1 3 9 |
| L8, times 4^(−1) = 13 | 4 13 5 15 |

The result is $(4, 13, 5, 15)$, which is $(4, 13, 22, 15)$ modulo $17$, the linear convolution computed directly on the [convolution page](/convolution/). For instance $F_4 A$ has $A_1 = 1 + 2 \cdot 4 + 3 \cdot 16 = 57 \equiv 6$. With $N = 2$ instead of $4$, the term $15$ would wrap onto the first entry.

## Correctness

Let $a'$ and $b'$ be $a$ and $b$ padded to length $N$. By the [FFT page](/fast-fourier-transform/), line L6 computes $A = F_N a'$ and $B = F_N b'$, and line L8 computes $F_N^{-1} C$, because $\omega$ is a principal $N$-th root and $N$ is a unit. By the [convolution theorem](/convolution-theorem/), $F_N^{-1}(F_N a' \cdot F_N b') = a' \circledast b'$, the cyclic convolution of length $N$. In polynomial terms, this is $A(t) B(t) \bmod (t^N - 1)$, where $\deg(A B) \le m + \ell - 2 < N$, so the reduction changes nothing: entries $0$ to $L - 1$ of $a' \circledast b'$ are $a * b$, and the others are $0$. The full proof is below.

## Complexity

**Ring operations.** Each FFT of length $N$ uses $\frac{N}{2} \lg N$ multiplications and $N \lg N$ additions. Three of them, the $N$ products of line L7 and the $N$ divisions by $N$ in line L8 (multiplications by $N^{-1}$) give

$$\tfrac{3}{2} N \lg N + 2N \ \text{multiplications} \quad \text{and} \quad 3 N \lg N \ \text{additions},$$

with $N < 2L$. So the cost is $O(L \log L)$, against $m\ell$ multiplications for the direct sum. If one input is fixed, as a filter is, its transform is computed once and the cost per new input is two FFTs. A squaring $a * a$ needs only two FFTs.

**Time and space.** $\Theta(N \log N)$ in each case, since the operations do not depend on the data, and $\Theta(N)$ extra space for $A$, $B$ and the tables. Over $\mathbb{Z}/p\mathbb{Z}$ with word-size $p$ this is $\Theta(N \log N)$ time on the word RAM.

**Lower bound.** The output has $L$ entries, so $\Omega(L)$ operations are needed. No better lower bound is known for general arithmetic circuits; see [convolution](/convolution/) for the exact bilinear complexity found by Winograd.

**Rounding errors (proved to first order).** Over $\mathbb{C}$ in floating point with unit roundoff $u$, let $\delta = \frac{\lg N \cdot \eta}{1 - \lg N \cdot \eta}$ be the relative 2-norm error bound of one FFT from Higham, Theorem 24.2, with $\eta = \mu + \gamma_4(\sqrt 2 + \mu)$, where $\mu$ bounds the error of the twiddle factors. A complex product has relative error at most $\gamma = \sqrt 2 \, \gamma_2$ (Higham, Lemma 3.5). Since $\lVert F_N x \rVert_2 = \sqrt N \lVert x \rVert_2$ and $\lVert F_N x \rVert_\infty \le \lVert x \rVert_1$, the three FFT errors and the product errors add up, to first order in $u$, to

$$\lVert \hat c - c \rVert_\infty \le (3\delta + \gamma) \, K, \qquad K = \max\left(\lVert a \rVert_1 \lVert b \rVert_2, \ \lVert a \rVert_2 \lVert b \rVert_1\right).$$

The derivation is in the proof below. For integer inputs, rounding gives the exact result whenever this bound, with the higher-order terms, is less than $\frac{1}{2}$. In double precision ($u = 2^{-53}$, $\mu = u$), for $m = \ell = 2^{15}$ digits below $2^{10}$, so $N = 2^{16}$, the bound is about $0.22$, and exactness is guaranteed. For $m = \ell = 2^{20}$ digits below $2^8$, the bound is about $3.3$, so it guarantees nothing. *Observed in practice:* the actual errors are many orders of magnitude below this worst case, because rounding errors behave like random variables and partly cancel, so practical codes use larger sizes than the bound allows. Codes that must be certain use the NTT or check the result.

## Properties

- **Exact over $\mathbb{Z}/p\mathbb{Z}$.** The result is $a * b$ modulo $p$. The true integer coefficients, of size up to $\min(m, \ell) \cdot \max|a_i| \cdot \max|b_j|$, are recovered exactly if this is below $p/2$ (taking residues in $(-p/2, p/2)$), or from two or three primes by the [Chinese remainder theorem](/chinese-remainder-theorem/).
- **Not in place.** It needs the two padded arrays of length $N$, which is up to about $2L$.
- **Oblivious.** The sequence of operations depends only on $m$ and $\ell$.
- **Bilinear.** The result is linear in $a$ and in $b$, like the convolution itself.

## Variants and improvements

- **Cyclic convolution.** If the cyclic convolution of length $n$ is wanted and $n$ is a power of two, skip the padding: $a \circledast b = F_n^{-1}(F_n a \cdot F_n b)$. For other $n$, use a [Bluestein](/bluestein-fft/) or mixed-radix FFT of length $n$, or a linear convolution followed by folding.
- **Negacyclic convolution.** Products modulo $t^n + 1$ use the weights $\psi^j$ with $\psi^n = -1$, as in the [convolution theorem](/convolution-theorem/) page. This avoids the padding in [Schönhage-Strassen multiplication](/schonhage-strassen-multiplication/).
- **Real data.** Two real sequences fit into one complex FFT as real and imaginary parts, and the two spectra are separated by symmetry, which halves the work; see the [real-valued FFT](/real-valued-fft/).
- **Long signals and short filters.** Overlap-add and overlap-save cut the long input into blocks of length about the filter length and convolve each block by FFT, for $O(m \log \ell)$ total cost with $m \gg \ell$.
- **Large integer coefficients.** Split each coefficient into small digits, or use the NTT modulo several primes and the Chinese remainder theorem. Over an arbitrary ring with no roots of unity, Schönhage and Strassen adjoin them, for $O(n \log n \log \log n)$ operations.
- **Small inputs.** Below a threshold of a few dozen terms, the direct sum or [Karatsuba](/karatsuba-multiplication/) is faster.

## When to use it

Use it to multiply polynomials or large integers of more than a few hundred terms, to apply a long FIR filter, to compute all correlations of two long signals, and to count the pairs with each sum in two sets of small integers. Use the NTT form when the result must be exact and fits the modulus, and the complex form when the data are real numbers or when an error bound like the one above is acceptable. For short filters on long signals, use overlap-add or the direct sum.

## Pitfalls

- **Too little padding.** With $N < m + \ell - 1$ the result is a cyclic convolution, and the high terms wrap onto the low ones. The length must be at least $m + \ell - 1$, not $\max(m, \ell)$.
- **Modulus too small.** Over $\mathbb{Z}/p\mathbb{Z}$ the output is reduced modulo $p$; if the true coefficients can reach $p$, the result is wrong with no warning.
- **Wrong root.** $N$ must divide $p - 1$, and $\omega$ must have order exactly $N$. The pair $p = 97$, $g = 3$ fails because $3$ is not a primitive root modulo $97$; use $g = 5$.
- **Rounding to integers too early.** Round only the final output, and only when the error bound, or a check, shows that the error is below $\frac{1}{2}$.
- **Forgetting the factor $1/N$.** The inverse FFT without the scaling returns $N$ times the convolution.
- **Mixed sign conventions.** The inverse must use $\omega^{-1}$ for the same $\omega$ as the forward transforms.

## Implementations

## History

The convolution theorem is old, but it became a fast algorithm only with the FFT of Cooley and Tukey (1965). Stockham (1966) described fast convolution and correlation by the FFT, including the sectioning of long inputs. Pollard (1971) gave the FFT over finite fields, which makes the convolution exact, and Schönhage and Strassen (1971) used FFT convolution over rings for fast integer multiplication. CLRS presents the method as polynomial multiplication in point-value form.

## References
