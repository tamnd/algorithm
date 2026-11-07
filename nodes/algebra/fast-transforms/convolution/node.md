---
tag: T1ZDPN
kind: problem
slug: convolution
name: Convolution
aliases:
- linear convolution
- cyclic convolution
- circular convolution
- acyclic convolution
area: algebra/fast-transforms
level: core
summary: Given sequences a and b, compute c_k = sum over i + j = k of a_i b_j (linear), or the same sum with indices taken modulo n (cyclic).
model: real-ram
complexity:
  vars: {n: the length of the output}
  time: {worst: O(n log n)}
prereqs: [polynomial-multiplication, discrete-fourier-transform]
see_also: [convolution-theorem, convolution-via-fft, number-theoretic-transform, fft-polynomial-multiplication, circular-convolution, cross-correlation, min-plus-convolution, fast-walsh-hadamard-transform]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.1, Representing polynomials (the convolution of the coefficient vectors), and Section 30.2 (the convolution theorem)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 22, Section 22.1, Convolution (cyclic, linear and negacyclic convolution, and the zero padding), and Section 22.2, Correlation
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 4, Section 4.2, Convolution (circulant and Toeplitz matrices, and convolution by the FFT)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Fast multiplication (Sections 8.1 to 8.3, from Karatsuba to the FFT and the Schönhage-Strassen method over any ring)
  - paper: "Shmuel Winograd, Arithmetic Complexity of Computations, CBMS-NSF Regional Conference Series in Applied Mathematics 33, SIAM, 1980"
    locator: the chapters on the minimal number of multiplications for linear and cyclic convolution
---

Convolution combines two sequences $a$ and $b$ into the sequence $c$ with $c_k = \sum_{i + j = k} a_i b_j$. This *linear* convolution is exactly the coefficient sequence of the product of the polynomials with coefficients $a$ and $b$, and it is the core of [polynomial multiplication](/polynomial-multiplication/), [integer multiplication](/integer-multiplication/) and linear filtering. The *cyclic* convolution of length $n$ takes the indices modulo $n$. The direct method takes $\Theta(mn)$ operations for inputs of lengths $m$ and $n$, and the [convolution theorem](/convolution-theorem/) gives $O(n \log n)$ by the [FFT](/fast-fourier-transform/).

## In plain words

Write one list of numbers on a strip of paper, and the other list backwards on a second strip. Lay the second strip under the first and slide it along, one place at a time. At each position, multiply the numbers that lie above each other and add the products. The sums, one for each position, form the convolution.

The same thing happens when you multiply two polynomials, or two numbers digit by digit before you carry: each digit of the product collects all pairs of digits whose places add up to its place. A blur filter on a sound or an image is also a convolution, with a short list of weights. In the cyclic version, the strip wraps around, as if it were glued into a ring.

## Definition

**Notation.** As on the [DFT page](/discrete-fourier-transform/), $R$ is a commutative ring, and over $\mathbb{C}$ the root is $\omega_n = e^{-2\pi i/n}$. Indices start at $0$. Costs count additions and multiplications in $R$.

**Linear convolution.** Input: $a = (a_0, \ldots, a_{m-1}) \in R^m$ and $b = (b_0, \ldots, b_{\ell-1}) \in R^\ell$ with $m, \ell \ge 1$. Output: $c = a * b \in R^{m + \ell - 1}$ with

$$c_k = \sum_{\substack{0 \le i \le m-1,\ 0 \le j \le \ell-1 \\ i + j = k}} a_i b_j, \qquad 0 \le k \le m + \ell - 2.$$

With $A(t) = \sum a_i t^i$ and $B(t) = \sum b_j t^j$, this says $A(t) B(t) = \sum_k c_k t^k$ in the [polynomial ring](/polynomial-ring/) $R[t]$.

**Cyclic convolution.** Input: $a, b \in R^n$. Output: $c = a \circledast b \in R^n$ with

$$c_k = \sum_{j=0}^{n-1} a_j \, b_{(k - j) \bmod n}, \qquad 0 \le k \le n-1.$$

Equivalently, $\sum c_k t^k \equiv A(t) B(t) \pmod{t^n - 1}$, since $t^n \equiv 1$ folds the term $t^{n+k}$ onto $t^k$. In matrix form, $c = Cb$ for the circulant matrix $C$ with entries $a_{(j-k) \bmod n}$. The page [circular convolution](/circular-convolution/) treats the signal-processing view.

**Negacyclic convolution.** The product modulo $t^n + 1$: the wrapped terms change sign, $c_k = \sum_{j \le k} a_j b_{k-j} - \sum_{j > k} a_j b_{n + k - j}$.

**The link between them.** If $N \ge m + \ell - 1$, pad $a$ and $b$ with zeros to length $N$. Then the cyclic convolution of length $N$ of the padded vectors equals $a * b$ followed by $N - (m + \ell - 1)$ zeros. *Proof.* In $A(t)B(t)$ each exponent is at most $m + \ell - 2 < N$, so reduction modulo $t^N - 1$ changes nothing. $\square$ Conversely, a cyclic convolution of length $n$ is the linear convolution of the two vectors, followed by the fold $c_k \leftarrow c_k + c_{k+n}$.

## Variants

- **Correlation.** The [cross-correlation](/cross-correlation/) $r_k = \sum_j a_j b_{j+k}$ is a convolution of $b$ with $a$ reversed.
- **Several dimensions.** $c_{k_1 k_2} = \sum a_{i_1 i_2} b_{k_1 - i_1, k_2 - i_2}$, used for images.
- **Weighted convolutions.** Products modulo $t^n - \zeta$ for a constant $\zeta$, with the negacyclic case $\zeta = -1$. They appear in the [Schönhage-Strassen](/schonhage-strassen-multiplication/) method.
- **Other index groups.** Replacing $i + j$ by $i \oplus j$ (bitwise exclusive or) gives the XOR or dyadic convolution, computed by the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/). Replacing it by $i \lor j$ gives the OR convolution, computed with the [sum over subsets](/sum-over-subsets/) transform.
- **Other semirings.** With $\min$ and $+$ in place of $+$ and $\times$, the problem is [(min, +) convolution](/min-plus-convolution/), for which no $O(n^{2 - \varepsilon})$ algorithm is known.
- **Number-theoretic.** The [Dirichlet convolution](/dirichlet-convolution/) $\sum_{d e = k} f(d) g(e)$ uses products of indices.

## Examples

**Linear.** $(1, 2, 3) * (4, 5) = (4, 13, 22, 15)$, because $(1 + 2t + 3t^2)(4 + 5t) = 4 + 13t + 22t^2 + 15t^3$. For instance $c_1 = a_0 b_1 + a_1 b_0 = 5 + 8$.

**Cyclic.** The cyclic convolution of length $3$ of $(1, 2, 3)$ and $(4, 5, 0)$ is $(19, 13, 22)$: the term $15t^3$ wraps onto $t^0$. With zero padding to length $4 \ge 3 + 2 - 1$, the cyclic convolution of $(1, 2, 3, 0)$ and $(4, 5, 0, 0)$ is $(4, 13, 22, 15)$, the linear result.

**Length 4.** For $a = (1, 2, 3, 4)$ and $b = (5, 6, 7, 8)$: the linear convolution is $(5, 16, 34, 60, 61, 52, 32)$, the cyclic one is $(66, 68, 66, 60)$, and the negacyclic one is $(-56, -36, 2, 60)$. Modulo $17$ the cyclic one is $(15, 0, 15, 9)$.

**Integers.** $123 \cdot 45$: the digit vectors, lowest digit first, are $(3, 2, 1)$ and $(5, 4)$, with convolution $(15, 22, 13, 4)$. Carrying gives $5, 3, 5, 5$ from the lowest digit up, so the product is $5535$.

**Dice.** With $d = (0, 1, 1, 1, 1, 1, 1)$, the number of ways to roll each total with two dice is $d * d = (0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1)$. The distribution of a sum of independent random variables on the integers is the convolution of their distributions.

**Edge cases.** If $m = \ell = 1$, the output is the single product $a_0 b_0$. The impulse $b = (1)$ is the identity: $a * (1) = a$. Shifting $b$ by one place, $b = (0, 1)$, shifts the output.

## Known algorithms

- **Direct sum.** $m\ell$ multiplications and $m\ell - (m + \ell - 1)$ additions for linear convolution; $n^2$ multiplications and $n(n-1)$ additions for cyclic convolution.
- **[Karatsuba](/karatsuba-multiplication/) and [Toom-Cook](/toom-cook-multiplication/).** $O(n^{\lg 3})$ and $O(n^{1 + \varepsilon})$ ring operations over any ring, by evaluation and interpolation at few points.
- **[Convolution via FFT](/convolution-via-fft/).** Three FFTs of length $N \ge m + \ell - 1$, a power of two, and $N$ pointwise products: $O(N \log N)$ operations over $\mathbb{C}$, or over $\mathbb{Z}/p\mathbb{Z}$ with the [number-theoretic transform](/number-theoretic-transform/) when $N \mid p - 1$.
- **[FFT polynomial multiplication](/fft-polynomial-multiplication/).** The same method, stated for polynomials.
- **Schönhage-Strassen over any ring.** $O(n \log n \log \log n)$ ring operations over each commutative ring, by adjoining virtual roots of unity (von zur Gathen and Gerhard, Section 8.3).
- **Short filters.** For a long input and a short filter of length $\ell$, the direct method costs $O(m\ell)$, and block methods (overlap-add, overlap-save) cut the FFT cost to $O(m \log \ell)$.

## Bounds

**Upper bounds.** Over $\mathbb{C}$, and over each ring with principal roots of unity of the needed power-of-two orders, $O(n \log n)$ ring operations. Over an arbitrary commutative ring, $O(n \log n \log \log n)$. In floating point, the FFT method has a proved normwise error bound that grows like $\log n$ times the unit roundoff; see [convolution via FFT](/convolution-via-fft/).

**Lower bounds.** The output has $2n - 1$ entries, each depending on the inputs, so $\Omega(n)$ operations are needed. No superlinear lower bound is known for general arithmetic circuits. For the *bilinear* model, where one counts only the multiplications of a linear form in $a$ by a linear form in $b$, Winograd determined the exact minimum over an infinite field: $m + \ell - 1$ multiplications for linear convolution, and $2n - d(n)$ for cyclic convolution of length $n$ over the rationals, where $d(n)$ is the number of divisors of $n$. These minimal algorithms use many additions, so they are practical only for small lengths.

## Reductions

- **Polynomial multiplication is linear convolution**, with no extra cost.
- **Integer multiplication** is linear convolution of the digit vectors followed by carry propagation in $O(n)$ digit operations.
- **Linear to cyclic.** Zero padding to length $N \ge m + \ell - 1$, as shown in Definition.
- **Cyclic to DFT.** By the [convolution theorem](/convolution-theorem/), $a \circledast b = F_n^{-1}(F_n a \cdot F_n b)$: three DFTs and $n$ products.
- **DFT to convolution.** [Bluestein's algorithm](/bluestein-fft/) writes a DFT of any length $n$ as a linear convolution of lengths $n$ and $2n - 1$. [Rader's algorithm](/rader-fft/) writes a DFT of prime length $p$ as a cyclic convolution of length $p - 1$.

## Applications

- **Arithmetic.** Fast [polynomial multiplication](/polynomial-multiplication/) and integer multiplication, and through them [fast polynomial division](/fast-polynomial-division/) and [multipoint evaluation](/fast-multipoint-evaluation/).
- **Filtering.** An [FIR filter](/fir-filter/) is a convolution with its impulse response; [digital filtering](/digital-filtering/) of long signals uses FFT convolution.
- **Probability and counting.** Distributions of sums, and counting the pairs $(i, j)$ with $x_i + y_j = s$ for all $s$ at once, for sets of small integers.
- **Strings.** Matching with wildcards and computing all Hamming distances of a pattern against a text reduce to a few convolutions.
- **Images.** Blurring, sharpening and template matching by [cross-correlation](/cross-correlation/).

## References
