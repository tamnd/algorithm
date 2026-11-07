---
tag: 7Q1636
kind: algorithm
slug: split-radix-fft
name: Split-radix FFT
aliases:
- split-radix algorithm
- split-radix FFT algorithm
- radix-2/4 FFT
area: algebra/fast-transforms
level: advanced
summary: Radix-2/radix-4 hybrid with a low arithmetic count for power-of-two lengths.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  additions: {worst: n lg n}
  multiplications: {worst: (n/2) lg n − n + 1}
properties: {deterministic: true, recursive: true, in_place: false}
history:
  year: 1968
  people: [R. Yavne, Pierre Duhamel, Henk Hollmann]
  note: Yavne (1968) presented the algorithm and its operation count of 4n lg n − 6n + 8 real operations. Duhamel and Hollmann (1984) rediscovered it and named it split radix. Johnson and Frigo (2007) published a modified split-radix FFT with asymptotically about 6 percent fewer operations.
prereqs: [discrete-fourier-transform, fast-fourier-transform, twiddle-factor]
see_also: [iterative-fft, mixed-radix-fft, real-valued-fft, roots-of-unity, butterfly-operation, winograd-fourier-transform, number-theoretic-transform, fast-dct]
sources:
  - paper: doi:10.1145/1476589.1476610
    title: R. Yavne, An economical method for calculating the discrete Fourier transform, Proceedings of the AFIPS Fall Joint Computer Conference 33, 1968
    locator: pp. 115 to 125
  - paper: doi:10.1049/el:19840012
    title: Pierre Duhamel and Henk Hollmann, Split radix FFT algorithm, Electronics Letters 20(1), 1984
    locator: pp. 14 to 16
  - paper: doi:10.1109/TASSP.1986.1164804
    title: Henrik V. Sorensen, Michael T. Heideman and C. Sidney Burrus, On computing the split-radix FFT, IEEE Transactions on Acoustics, Speech, and Signal Processing 34(1), 1986
    locator: pp. 152 to 156 (a program and the separate counts of real additions and multiplications)
  - paper: doi:10.1109/TASSP.1986.1164811
    title: Pierre Duhamel, Implementation of split-radix FFT algorithms for complex, real, and real-symmetric data, IEEE Transactions on Acoustics, Speech, and Signal Processing 34(2), 1986
    locator: pp. 285 to 295
  - paper: doi:10.1109/TSP.2006.882087
    title: Steven G. Johnson and Matteo Frigo, A modified split-radix FFT with fewer arithmetic operations, IEEE Transactions on Signal Processing 55(1), 2007
    locator: pp. 111 to 119 (Section II and equations (4) and (5) for the counts of the standard split radix; equation (1) for the new count)
---

The split-radix FFT computes the [discrete Fourier transform](/discrete-fourier-transform/) of length $n = 2^m$ by splitting the input three ways: one transform of length $n/2$ of the even-indexed samples, and two transforms of length $n/4$ of the samples with index $1$ and $3$ modulo $4$. The even half is combined as in radix 2, which needs no twiddle factors, and the two odd quarters are combined as in radix 4, which needs only two twiddle factors per index. The result is the lowest count of real additions and multiplications for power-of-two lengths known from 1968 until 2004: $4n \lg n - 6n + 8$ real operations, against about $5 n \lg n$ for the radix-2 [FFT](/fast-fourier-transform/). It is a recursive algorithm with the same data flow as radix 2 and radix 4.

## In plain words

An FFT breaks a long transform into shorter ones and glues the results with "twiddle" multiplications. The usual way splits into evens and odds. The odd half carries twiddles, and those multiplications are most of the cost. Split radix keeps the evens as one half-size problem, which needs no twiddles at all, and cuts the odds again into two quarter-size problems. The quarter-size results are glued with twiddles chosen so that half of the glue work is a free quarter turn. Doing this at every level saves about a third of the general multiplications, with no change in the number of additions.

## The problem

**Notation.** As on all pages of fast transforms, $n$ is the transform length, here a power of two, and $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign). The DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega_n^{jk}$ and the inverse is $x_j = \frac1n \sum_k X_k \omega_n^{-jk}$. The algorithm only uses that $\omega^{n/2} = -1$ for the root $\omega$ it is given, so it runs unchanged over any commutative ring with such an element, for example $\mathbb{Z}/p\mathbb{Z}$ with a principal $n$-th root of unity, as in the [number-theoretic transform](/number-theoretic-transform/). Write $J = \omega^{n/4}$; over $\mathbb{C}$, $J = -i$.

**Input.** $x_0, \ldots, x_{n-1}$ in the ring, and the root $\omega$.

**Output.** $X_0, \ldots, X_{n-1}$.

**Cost model.** Ring additions (with subtractions) and ring multiplications are counted separately, at unit cost, in the [real RAM](/real-ram/) (or the word RAM over $\mathbb{Z}/p\mathbb{Z}$). Every product at lines L8 and L9 is counted, including the products by $J$; the products by $\omega^0 = 1$ at $k = 0$ are skipped, as in the code. Over $\mathbb{C}$ a product by $J = -i$ is a swap and a sign change, so the usual count of real operations treats it as free. Twiddle factors come from a table of the $n$ powers of $\omega$, built once from the exact angles and not counted.

## The algorithm

Split $x$ by index modulo $4$. Let $U$ be the DFT of length $n/2$ of $(x_{2j})$ with root $\omega^2$, and let $Z$ and $Z'$ be the DFTs of length $n/4$ of $(x_{4j+1})$ and $(x_{4j+3})$ with root $\omega^4$. Then for $0 \le k < n/4$,

$$X_k = U_k + (\omega^k Z_k + \omega^{3k} Z'_k), \qquad X_{k + n/2} = U_k - (\omega^k Z_k + \omega^{3k} Z'_k),$$
$$X_{k + n/4} = U_{k + n/4} + J(\omega^k Z_k - \omega^{3k} Z'_k), \qquad X_{k + 3n/4} = U_{k + n/4} - J(\omega^k Z_k - \omega^{3k} Z'_k).$$

The four outputs share the two products $\omega^k Z_k$ and $\omega^{3k} Z'_k$. This "L-shaped" butterfly is the whole algorithm.

```pseudo id=main
SPLIT-RADIX-FFT(x, ω)          ▷ n = length(x) a power of two, ω^(n/2) = −1
L1  if n = 1 then return x
L2  if n = 2 then return (x_0 + x_1, x_0 − x_1)
L3  U ← SPLIT-RADIX-FFT((x_0, x_2, …, x_(n−2)), ω^2)       ▷ length n/2
L4  Z ← SPLIT-RADIX-FFT((x_1, x_5, …, x_(n−3)), ω^4)       ▷ length n/4
L5  Z' ← SPLIT-RADIX-FFT((x_3, x_7, …, x_(n−1)), ω^4)      ▷ length n/4
L6  J ← ω^(n/4)                                            ▷ −i over C
L7  for k ← 0 to n/4 − 1 do
L8      a ← ω^k · Z_k ; b ← ω^(3k) · Z'_k                   ▷ no product at k = 0
L9      s ← a + b ; d ← J · (a − b)
L10     X_k ← U_k + s ; X_(k+n/2) ← U_k − s
L11     X_(k+n/4) ← U_(k+n/4) + d ; X_(k+3n/4) ← U_(k+n/4) − d
L12 return X
```

The **inverse** runs the same procedure with $\omega^{-1}$, which also satisfies $(\omega^{-1})^{n/2} = -1$, and divides by $n$.

## Example

Over $\mathbb{Z}/17\mathbb{Z}$, $n = 8$, $\omega = 2$ (of order $8$, with $2^4 = 16 = -1$), $J = 2^2 = 4$, and $x = (1, 2, 3, 4, 5, 6, 7, 8)$. The recursive calls give $U = \mathrm{DFT}_4(1, 3, 5, 7) = (16, 14, 13, 12)$ with root $4$, $Z = \mathrm{DFT}_2(2, 6) = (8, 13)$ and $Z' = \mathrm{DFT}_2(4, 8) = (12, 13)$ with root $16 = -1$. The loop of lines L7 to L11, modulo $17$:

| k | a = ω^k Z_k | b = ω^(3k) Z'_k | s = a + b | d = J(a − b) | X_k | X_(k+4) | X_(k+2) | X_(k+6) |
|---|---|---|---|---|---|---|---|---|
| 0 | 8 | 12 | 3 | 1 | 2 | 13 | 14 | 12 |
| 1 | 2 · 13 = 9 | 8 · 13 = 2 | 11 | 11 | 8 | 3 | 6 | 1 |

So $X = (2, 8, 14, 6, 13, 3, 12, 1)$, which equals the direct sum $\sum_j x_j 2^{jk} \bmod 17$. Over $\mathbb{C}$, $x = (1, 2, 3, 4)$ gives $U = (4, -2)$, $Z = (2)$, $Z' = (4)$, $s = 6$, $d = -i(2 - 4) = 2i$, and $X = (10, -2 + 2i, -2, -2 - 2i)$. Both examples were checked by script.

## Correctness

Split the sum for $X_k$ by the index modulo $4$, joining the classes $0$ and $2$: the even part is $\sum_j x_{2j} (\omega^2)^{jk} = U_{k \bmod n/2}$, and the classes $1$ and $3$ give $\omega^k \sum_j x_{4j+1} (\omega^4)^{jk} = \omega^k Z_{k \bmod n/4}$ and $\omega^{3k} Z'_{k \bmod n/4}$. So $X_k = U_k + \omega^k Z_k + \omega^{3k} Z'_k$ for every $k$, with indices of $U, Z, Z'$ taken modulo their lengths. Replacing $k$ by $k + n/4$ multiplies $\omega^k$ by $J$ and $\omega^{3k}$ by $J^3 = -J$ (since $J^2 = \omega^{n/2} = -1$), and replacing $k$ by $k + n/2$ multiplies both by $-1$. This gives the four formulas of lines L10 and L11. The recursive calls are correct by induction, since $(\omega^2)^{n/4} = -1$ and $(\omega^4)^{n/8} = -1$. The full proof, with the exact operation counts, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Ring operations.** Let $n = 2^m$. The proof shows, for every $m \ge 0$:

- $A(n) = n \lg n$ additions and subtractions, the same as radix 2;
- $\frac13 n \lg n - \frac89 n + 1 - \frac19 (-1)^{m}$ multiplications by twiddle factors $\omega^k, \omega^{3k}$ with $k \ge 1$ (line L8);
- $\frac16 n \lg n - \frac19 n + \frac19 (-1)^{m}$ multiplications by $J$ (line L9);
- in total $\frac{n}{2} \lg n - n + 1$ multiplications.

The total equals that of the radix-2 FFT with the products by $1$ skipped. The gain is in their kind: over $\mathbb{C}$ the products by $J = -i$ are free, so split radix does about $\frac13 n \lg n$ general complex multiplications, against $\frac12 n \lg n - \frac32 n + 2$ for radix 2 with the products by $\pm 1$ and $\pm i$ skipped. The time is $\Theta(n \log n)$ for every input, and the recursion depth is $\lg n$. The test file checks the addition and multiplication counts exactly for $n \le 4096$.

**Real operations.** With complex multiplications done by $4$ real multiplications and $2$ real additions, and the twiddle factor $\omega^{n/8} = (1 - i)/\sqrt2$ done with $2$ real multiplications, Sorensen, Heideman and Burrus (1986) give $\frac83 n \lg n - \frac{16}{9} n - \frac29 (-1)^{\lg n} + 2$ real additions and $\frac43 n \lg n - \frac{38}{9} n + \frac29 (-1)^{\lg n} + 6$ real multiplications, $4 n \lg n - 6n + 8$ in all for $n > 1$; these are the counts quoted by Johnson and Frigo (2007, equations (4) and (5)). Our code does not take the shortcut at $k = n/8$, so it does a few more real multiplications than this.

**Space.** The recursion holds the partial results of one root-to-leaf path, of total length at most $2n$, plus the table of $n$ powers, so the extra space is $\Theta(n)$. Iterative in-place forms exist (see Variants).

**Rounding errors.** Over $\mathbb{C}$ in floating point, every output is a sum of $O(\log n)$ rounded butterfly terms, as in radix 2, and the same kind of normwise bound, of order $u \lg n$, can be expected; *not proved here*: we know of no published proof for split radix that we have checked, and we do not state one. *Observed:* for random complex data with entries uniform in the unit square, the relative $2$-norm error of a forward and inverse round trip was $7u$ at $n = 2^{10}$, $10u$ at $n = 2^{14}$ and $12u$ at $n = 2^{16}$, where $u = 2^{-53}$. Johnson and Frigo state that their modified algorithm does not sacrifice accuracy. The tests use the tolerance $64(\lg n + 2) u \sqrt n \max(\lVert x \rVert_2, 1)$.

## Properties

- **Exact over rings.** The code uses only $+$, $-$ and $\times$, so over $\mathbb{Z}/p\mathbb{Z}$ the output is exact.
- **Same additions as radix 2.** The saving is only in multiplications.
- **Fewer twiddle factors.** Each level needs only $\omega^k$ and $\omega^{3k}$ for $k < n/4$.
- **Irregular recursion.** The two branches have lengths $n/2$ and $n/4$, so the call tree is unbalanced; an iterative form needs a more complex schedule than radix 2.
- **Deterministic.** The operation count does not depend on the data.

## Variants and improvements

- **Decimation in frequency.** The transposed algorithm splits the outputs into even indices and indices $1$ and $3$ modulo $4$, with the twiddle factors applied after the butterflies; it has the same counts.
- **Iterative and in-place forms.** Sorensen, Heideman and Burrus (1986) give a program that runs the L-shaped butterflies in place, level by level.
- **Real and symmetric data.** Duhamel (1986) adapts split radix to real input and to real-symmetric data, which also gives fast [discrete cosine transforms](/fast-dct/); see also the [real-valued FFT](/real-valued-fft/).
- **Conjugate-pair split radix.** Using $x_{4j-1}$ and $\omega^{-k}$ in place of $x_{4j+3}$ and $\omega^{3k}$ makes the two twiddle factors conjugate. It was proposed to save operations, and its count was later proved identical to that of ordinary split radix (Johnson and Frigo 2007, Section II, with references); its advantage is fewer twiddle loads, and it is the starting point of the modified algorithm below.
- **Modified split radix.** Johnson and Frigo (2007) rescale the subtransforms so that some twiddle factors become cheaper, reaching $\frac{34}{9} n \lg n + O(n)$ real operations; they credit the first improvement over Yavne's count to a 2004 Usenet post by James Van Buskirk for $n = 64$.
- **Other lengths.** Splitting into one transform of length $n/p$ and several of length $n/p^2$ works for other radices $p$; for lengths that are not powers of two, see the [mixed-radix FFT](/mixed-radix-fft/) and the [Winograd Fourier transform](/winograd-fourier-transform/).

## When to use it

Use it for complex transforms of power-of-two length when the count of floating-point operations matters: fixed-length kernels, hardware pipelines, and generated code. For large $n$ on modern machines, memory traffic matters more than the exact count, and a radix-4 or radix-8 iterative FFT runs at a similar speed. Over $\mathbb{Z}/p\mathbb{Z}$, multiplications by $J$ are not free, so the advantage over radix 2 disappears unless products by $J$ are cheaper than others.

## Pitfalls

- **The sign of $J$.** With $\omega_n = e^{-2\pi i/n}$, $J = -i$; with the other sign convention, $J = +i$. Using the wrong one swaps $X_{k+n/4}$ and $X_{k+3n/4}$.
- **$\omega^{3k}$, not $\omega^{-k}$, in this form.** The two are different unless the indexing of $Z'$ is shifted, as in the conjugate-pair variant.
- **Base cases.** Both $n = 1$ and $n = 2$ are needed: a call of length $2$ would create quarter-length calls of length $1/2$.
- **Twiddle accuracy.** Computing $\omega^{3k}$ by repeated multiplication accumulates error; read it from a table built from exact angles.
- **Counting claims.** The famous $4n\lg n - 6n + 8$ assumes products by $\pm 1$, $\pm i$ are free and the special case $k = n/8$; a plain implementation does more real multiplications.

## Implementations

The Python implementation in [impl/python/split_radix_fft.py](impl/python/split_radix_fft.py) follows the main block, with the recursion working on strided views of the input and twiddles read from a table of the $n$ powers of $\omega$ built from the exact angles. The core uses only ring operations, so the same function runs over $\mathbb{C}$, over $\mathbb{Z}/p\mathbb{Z}$ through a small residue class, and over a counting class. The tests compare it exactly with the direct $O(n^2)$ DFT modulo $17$, $97$ and $998244353$ (primitive roots $3$, $5$ and $3$) for every power of two the prime allows up to $256$; compare it in floating point with the direct DFT up to $n = 256$; check round trips up to $n = 2^{14}$, zeros, an impulse, a constant, $n = 1$ and $2$, and rejection of other lengths; and check the exact counts of additions and multiplications for $n \le 4096$.

## History

Yavne (1968) presented the algorithm at the AFIPS Fall Joint Computer Conference, and his count of $4n \lg n - 6n + 8$ real operations stood as the lowest known for power-of-two lengths until 2004 (Johnson and Frigo 2007). The paper was little noticed; in 1984 Duhamel and Hollmann rediscovered the algorithm and gave it the name split radix, and Vetterli and Nussbaumer, and Martens, published algorithms in the same year that Johnson and Frigo cite as forms of the split-radix algorithm. Sorensen, Heideman and Burrus (1986) gave an in-place program and the separate counts of additions and multiplications, and Duhamel (1986) the versions for real and symmetric data. In 2004 James Van Buskirk lowered the count for $n = 64$, and Johnson and Frigo (2007) turned the idea into a modified split-radix algorithm with $\frac{34}{9} n \lg n - \frac{124}{27} n + O(\log n)$ real operations.

## References
