---
tag: XHJRTQ
kind: algorithm
slug: chinese-remainder-theorem-fft
name: Good-Thomas prime-factor FFT
aliases:
- prime-factor algorithm
- Good-Thomas algorithm
- PFA
- prime-factor FFT
- Good's mapping
area: algebra/fast-transforms
level: advanced
summary: Factors n into coprime lengths and uses the Chinese remainder theorem to index the data, avoiding twiddle factors.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a product of pairwise coprime factors), s: the sum of the factors}
  time: {worst: O(n s), average: O(n s), best: O(n s)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1958
  people: [I. J. Good, L. H. Thomas]
  note: Good (1958) and, independently, Thomas (1963) turned a DFT of length n_1 n_2 with coprime factors into a two-dimensional DFT by re-indexing with the Chinese remainder theorem.
prereqs: [discrete-fourier-transform, chinese-remainder-theorem, fast-fourier-transform]
see_also: [mixed-radix-fft, rader-fft, winograd-fourier-transform, bluestein-fft, multidimensional-fft, twiddle-factor, kronecker-product, modular-inverse]
sources:
  - paper: doi:10.1111/j.2517-6161.1958.tb00300.x
    title: I. J. Good, The interaction algorithm and practical Fourier analysis, Journal of the Royal Statistical Society Series B 20(2), 1958
    locator: pp. 361 to 372 (the re-indexing of a DFT of length n_1 n_2 with coprime factors as a two-dimensional DFT, with no factors between the stages)
  - paper: "L. H. Thomas, Using a computer to solve problems in physics, in Applications of Digital Computers, Ginn and Company, Boston, 1963"
    locator: the prime-factor re-indexing, found independently of Good
  - paper: doi:10.1109/TASSP.1977.1162973
    title: David P. Kolba and Thomas W. Parks, A prime factor FFT algorithm using high-speed convolution, IEEE Transactions on Acoustics, Speech, and Signal Processing 25(4), 1977
    locator: pp. 281 to 294 (the prime-factor algorithm with short DFT modules computed as convolutions)
  - paper: doi:10.1090/S0025-5718-1978-0468306-4
    title: Shmuel Winograd, On computing the discrete Fourier transform, Mathematics of Computation 32(141), 1978
    locator: pp. 175 to 199 (short DFT modules with few multiplications, nested with the prime-factor index map)
  - paper: doi:10.1109/TASSP.1981.1163645
    title: C. Sidney Burrus and P. W. Eschenbacher, An in-place, in-order prime factor FFT algorithm, IEEE Transactions on Acoustics, Speech, and Signal Processing 29(4), 1981
    locator: pp. 806 to 817 (an index map that makes the prime-factor algorithm in place and in natural order)
  - paper: doi:10.1016/0021-9991(85)90164-0
    title: Clive Temperton, Implementation of a self-sorting in-place prime factor FFT algorithm, Journal of Computational Physics 58(3), 1985
    locator: pp. 283 to 299 (a self-sorting in-place prime-factor FFT)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 4, Section 4.1, Prime factor frameworks (the index permutations, and the DFT matrix as a permuted Kronecker product of smaller DFT matrices)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 3, Section 3.6 (rounding errors of complex arithmetic) and Chapter 24 (the FFT error analysis that the bound on this page follows)
---

The Good-Thomas prime-factor algorithm computes a [DFT](/discrete-fourier-transform/) of length $n = n_1 n_2 \cdots n_r$ with pairwise coprime factors as an $r$-dimensional DFT of shape $n_1 \times \cdots \times n_r$. The input is re-indexed by $j = (N_1 j_1 + \cdots + N_r j_r) \bmod n$, with $N_i = n/n_i$, and the output by the [Chinese remainder theorem](/chinese-remainder-theorem/), $k \equiv k_i \pmod{n_i}$ for each $i$. With these maps $\omega^{jk}$ splits exactly into a product of roots of unity of the lengths $n_i$, so the transform is a sequence of short DFTs along each axis, with none of the [twiddle factors](/twiddle-factor/) that the Cooley-Tukey [mixed-radix FFT](/mixed-radix-fft/) needs between its stages. Its cost is $n \sum_i C(n_i)/n_i$ for short DFTs of cost $C(n_i)$, and it is the frame for the small-length modules of Kolba and Parks and of Winograd. Good found it in 1958 and Thomas, independently, in 1963.

## In plain words

When the length of a Fourier transform is a product of numbers with no common factor, such as $15 = 3 \cdot 5$, the list can be arranged in a table of $3$ rows and $5$ columns in a clever order. With the right order, the whole transform is just a transform of each column followed by a transform of each row, and nothing else.

The right order comes from the Chinese remainder theorem, which says that a number below $15$ is fixed by its remainders after division by $3$ and by $5$. One order is used to read the input into the table and another to read the answer out. The ordinary fast Fourier transform for such lengths needs an extra multiplication between the two steps; this method needs none.

## The problem

**Notation.** $n$ is the transform length; here $n = n_1 \cdots n_r$ with $\gcd(n_a, n_b) = 1$ for $a \ne b$, and no factor needs to be a power of two. Over $\mathbb{C}$, $\omega = \omega_n = e^{-2\pi i/n}$, with the minus sign of signal processing; over a commutative ring, $\omega$ is a principal $n$-th root of unity, for example in $\mathbb{Z}/p\mathbb{Z}$ for a prime $p$ with $n \mid p - 1$. The DFT is $X_k = \sum_j x_j \omega^{jk}$, and the inverse uses $\omega^{-1}$ and the factor $1/n$, as on the [DFT page](/discrete-fourier-transform/). Write $N_i = n/n_i$ and $e_i = N_i^{-1} \bmod n_i$, which exists because $\gcd(N_i, n_i) = 1$.

**Input.** $x \in R^n$, the factors $n_1, \ldots, n_r$, and $\omega$. **Output.** $X = F_n x$.

**Cost model.** Ring multiplications and additions, counted separately, plus integer index arithmetic. In floating point, the error is analysed below.

## The algorithm

```pseudo id=main
GOOD-THOMAS(x, n_1, …, n_r, ω)   ▷ n_i pairwise coprime, n = n_1 ⋯ n_r = |x|
L1  N_i ← n / n_i and e_i ← N_i^(−1) mod n_i for i = 1, …, r
L2  A[j_1, …, j_r] ← x[(N_1 j_1 + ⋯ + N_r j_r) mod n] for all 0 ≤ j_i < n_i
L3  for i ← 1 to r do
L4      replace each line of A along the axis i by its DFT of length n_i with the root ω^(N_i)
L5  X[(N_1 e_1 k_1 + ⋯ + N_r e_r k_r) mod n] ← A[k_1, …, k_r] for all 0 ≤ k_i < n_i
L6  return X
```

Line L2 is Good's input map, and line L5 the CRT output map: the index $k = \sum_i N_i e_i k_i \bmod n$ is the unique $k$ with $k \equiv k_i \pmod{n_i}$, because $N_i e_i \equiv 1 \pmod{n_i}$ and $N_i \equiv 0 \pmod{n_a}$ for $a \ne i$. Line L4 may use any method for the short DFTs: the direct sum (as in the implementation), a radix-2 [FFT](/fast-fourier-transform/) for a power-of-two factor, [Rader's algorithm](/rader-fft/) for a prime factor, or a hand-optimized module. The inverse is the same procedure with $\omega^{-1}$, followed by division by $n$.

## Example

Take $n = 6 = 2 \cdot 3$ over $\mathbb{Z}/7\mathbb{Z}$ with $\omega = 3$, which has order $6$, and $x = (1, 2, 3, 4, 5, 6)$. Then $N_1 = 3$, $N_2 = 2$, $e_1 = 3^{-1} \bmod 2 = 1$ and $e_2 = 2^{-1} \bmod 3 = 2$. The input map is $j = 3 j_1 + 2 j_2 \bmod 6$, and the output map is $k = 3 k_1 + 4 k_2 \bmod 6$.

| step | row $j_1 = 0$ | row $j_1 = 1$ |
|---|---|---|
| L2, indices $j$ | 0 2 4 | 3 5 1 |
| L2, values | 1 3 5 | 4 6 2 |
| L4, axis 1, root $\omega^3 = 6 = -1$ | 5 2 0 | 4 4 3 |
| L4, axis 2, root $\omega^2 = 2$ | 0 2 6 | 4 3 5 |
| L5, indices $k$ | 0 4 2 | 3 1 5 |

For instance the first column $(1, 4)$ becomes $(1 + 4, 1 - 4) = (5, 4)$, and the row $(5, 2, 0)$ becomes $(5 + 2 + 0, 5 + 2 \cdot 2 + 0 \cdot 4, 5 + 2 \cdot 4 + 0 \cdot 2) = (0, 2, 6)$ modulo $7$. Placing each entry at its index $k$ gives $X = (0, 3, 6, 4, 2, 5)$, which equals the direct sums $X_k = \sum_j x_j 3^{jk} \bmod 7$. No multiplication happened between the two axes. The example was checked by script.

## Correctness

Let $j = \sum_a N_a j_a \bmod n$ and $k = \sum_i N_i e_i k_i \bmod n$. Modulo $n$, $jk \equiv \sum_{a, i} N_a N_i e_i j_a k_i$. For $a \ne i$, $n \mid N_a N_i$, so these terms vanish, and $\omega^{jk} = \prod_i \omega^{N_i^2 e_i j_i k_i} = \prod_i (\omega^{N_i})^{j_i k_i}$, because $N_i e_i \equiv 1 \pmod{n_i}$ and $\omega^{N_i}$ has order dividing $n_i$. Both maps are bijections by the Chinese remainder theorem. So $X_k = \sum_{j_1, \ldots, j_r} A[j_1, \ldots, j_r] \prod_i (\omega^{N_i})^{j_i k_i}$, which is the $r$-dimensional DFT of $A$; line L4 computes it one axis at a time. The full proof, including that $\omega^{N_i}$ is a principal $n_i$-th root, is below.

## Complexity

**Operations.** If a short DFT of length $m$ costs $M(m)$ multiplications and $S(m)$ additions, line L4 for the axis $i$ does $N_i$ of them, so the total is $n \sum_i M(n_i)/n_i$ multiplications and $n \sum_i S(n_i)/n_i$ additions, with no other ring operations. With direct short DFTs ($M(m) \le (m - 1)^2$ nontrivial multiplications) this is at most $n \sum_i (n_i - 1)$ of each, which is $O(n \log n)$ when the factors are bounded. The Cooley-Tukey mixed-radix FFT with the same factors needs, in addition, up to $n$ twiddle multiplications between consecutive stages.

**Index arithmetic.** Lines L2 and L5 cost $O(n r)$ integer operations, or $O(n)$ with incremental updates. These permutations, not arithmetic, often dominate in practice; Burrus and Eschenbacher (1981) and Temperton (1985) gave in-place, self-sorting versions that hide them.

**Space.** $\Theta(n)$ extra for $A$ and $X$ in the form above, $\Theta(1)$ beyond the input for the in-place variants.

**Limits.** The factors must be coprime, so a length such as $2^k$ or $p^2$ cannot be split this way; the prime-power factors are done by another method, such as a radix-2 FFT or the mixed-radix FFT, inside line L4.

**Rounding errors (proved to first order).** Over $\mathbb{C}$ with direct short DFTs, let the computed roots have absolute error at most $\mu$, and let $u$ be the unit roundoff and $\gamma_m = mu/(1 - mu)$. Then

$$\frac{\lVert \hat X - X \rVert_2}{\lVert X \rVert_2} \le \sum_{i=1}^{r} \sqrt{n_i} \left(\gamma_{n_i - 1} + \sqrt 2 \gamma_2 + \mu\right) + O(u^2),$$

which is $O(u \sum_i n_i^{3/2})$. With fast short modules the factor $\sqrt{n_i}(\gamma_{n_i - 1} + \ldots)$ is replaced by the relative error of that module. Over $\mathbb{Z}/p\mathbb{Z}$ the result is exact.

## Properties

- **No twiddle factors.** The axes are fully independent; this is the defining advantage over the Cooley-Tukey mixed-radix FFT.
- **Exact over finite rings.** With $\omega$ a principal root modulo $p$, the output is exactly the DFT, as in the tests with $p = 97$ and $p = 998244353$.
- **Two different index maps.** The input map and the output map differ (Good's map and the CRT map), and the algorithm is not in natural order without extra work.
- **Non-recursive.** The axes are processed in a loop.

## Variants and improvements

- **Winograd Fourier transform algorithm.** Winograd (1978) nested the short modules so that all multiplications are done in one middle stage, reaching the fewest multiplications known for many lengths, at the price of more additions; see the [Winograd Fourier transform](/winograd-fourier-transform/).
- **Short modules by convolution.** Kolba and Parks (1977) computed the prime-length modules by Rader's reduction to cyclic convolution.
- **In-place, in-order.** Burrus and Eschenbacher (1981) and Temperton (1985) chose index maps that make the algorithm in place and self-sorting.
- **Combined with Cooley-Tukey.** For a general $n$, split it into prime powers with the PFA and handle each prime power with a mixed-radix FFT, the approach of many FFT libraries for lengths such as $720 = 16 \cdot 9 \cdot 5$.
- **Arbitrary lengths.** For a prime length with no useful factor, use [Rader's algorithm](/rader-fft/) or [Bluestein's algorithm](/bluestein-fft/).

## When to use it

Use the prime-factor algorithm for lengths with several small coprime factors, such as $60$, $240$ or $1008$, when twiddle multiplications are costly, in fixed-point hardware, and in number-theoretic transforms over $\mathbb{Z}/p\mathbb{Z}$ whose $p - 1$ has small odd factors. For powers of two use the radix-2 or split-radix FFT, for which this method has nothing to offer.

## Pitfalls

- **Non-coprime factors.** With $\gcd(n_1, n_2) > 1$, the maps are not bijections and the result is wrong; check the factorization.
- **The root of each axis must match the maps.** With Good's map in and the CRT map out, the axis $i$ uses $\omega^{N_i}$, which is a primitive $n_i$-th root but in general not $e^{-2\pi i/n_i}$. The swapped pair (CRT in, Good out) uses the same roots. With the CRT map on both sides the axis root must be $\omega^{N_i e_i}$, and with Good's map on both sides $\omega^{N_i^2}$; pairing a map with the wrong root gives a permuted, wrong result.
- **Modular inverse.** $e_i = N_i^{-1} \bmod n_i$ needs the [extended Euclidean algorithm](/extended-euclidean-algorithm/) or Python's `pow(N, -1, m)`; for $n_i = 1$ the axis can be skipped.

## Implementations

## History

Good (1958) described the re-indexing for coprime factors in a paper on the interaction algorithm and Fourier analysis, and Thomas (1963) found it independently. Cooley and Tukey (1965) acknowledged Good's paper; their algorithm works for any factorization, at the cost of twiddle factors. Kolba and Parks (1977) combined the prime-factor map with short DFT modules computed by convolution, and Winograd (1978) gave modules with minimal multiplications and the nested form. Burrus and Eschenbacher (1981) and Temperton (1985) made the algorithm in place and in order.

## References
