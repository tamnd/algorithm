---
tag: 37TN4K
kind: algorithm
slug: iterative-fft
name: Iterative FFT
aliases:
- in-place FFT
- decimation-in-frequency FFT
- Gentleman-Sande FFT
- Sande-Tukey FFT
area: algebra/fast-transforms
level: core
summary: Non-recursive fast Fourier transform that combines values in place with butterfly operations, in loops over stages, and moves the bit-reversal permutation to the input or the output or removes it.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  additions: {worst: n lg n}
  multiplications: {worst: (n/2) lg n}
properties: {deterministic: true, recursive: false, in_place: true}
history:
  year: 1966
  people: [W. Morven Gentleman, Gordon Sande]
  note: Cooley and Tukey (1965) gave the decimation-in-time form, which reads its input in bit-reversed order. Gentleman and Sande (1966) gave the decimation-in-frequency form, which reads natural order and writes bit-reversed order.
prereqs: [fast-fourier-transform, butterfly-operation, bit-reversal-permutation, twiddle-factor]
see_also: [inverse-fft, convolution-via-fft, fft-polynomial-multiplication, number-theoretic-transform, split-radix-fft, mixed-radix-fft, parallel-fft-circuit, in-place-algorithm]
sources:
  - paper: doi:10.1090/S0025-5718-1965-0178586-1
    title: James W. Cooley and John W. Tukey, An algorithm for the machine calculation of complex Fourier series, Mathematics of Computation 19(90), 1965
    locator: pp. 297 to 301 (the factorization of the DFT and the digit-reversed order of the result)
  - paper: doi:10.1145/1464291.1464352
    title: W. Morven Gentleman and Gordon Sande, Fast Fourier transforms, for fun and profit, AFIPS Fall Joint Computer Conference, 1966
    locator: from p. 563 (the decimation-in-frequency form)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.3, Efficient FFT implementations (the iterative FFT with bit reversal)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1 (the Cooley-Tukey, Gentleman-Sande and Stockham frameworks, bit reversal, and the order of the loops)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, The Fast Fourier Transform and Applications, Theorem 24.2 (the normwise error bound of the radix-2 FFT)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 21 (radix-2 FFTs by decimation in time and in frequency)
---

The iterative FFT computes the [DFT](/discrete-fourier-transform/) of length $n = 2^t$ with loops instead of recursion. It works on one array, in $t$ stages of $n/2$ [butterflies](/butterfly-operation/) each, and writes every result back into the two cells it read, so it needs no extra array. The price of working in place is a scrambled order: one of the two ends, input or output, is in [bit-reversed order](/bit-reversal-permutation/). The decimation-in-time form of Cooley and Tukey, shown on the [FFT page](/fast-fourier-transform/), permutes the input first. This page gives the other form, *decimation in frequency* (Gentleman and Sande), which reads the input in natural order and leaves the output bit-reversed, and it shows how the two forms fit together so that a [convolution](/convolution-via-fft/) needs no permutation at all.

## In plain words

A recursive fast Fourier transform splits a list in two, transforms each half, and combines. Written as loops, the same work becomes a few passes over one list. Each pass walks the list and, for many pairs of positions, replaces the two numbers by their sum and a turned copy of their difference. The pairs are far apart in the first pass and neighbours in the last.

Because each pair is overwritten in place, no second list is needed. The catch is that the answers come out in a shuffled order, by the rule that reads each position number backwards in binary. A final shuffle fixes that. But when the next step does not care about order, such as multiplying two transforms entry by entry, the shuffle can be skipped, and a matching pass that reads shuffled order undoes it for free.

## The problem

**Notation.** As on all pages of fast transforms: the length is $n = 2^t$, a power of two; over $\mathbb{C}$ the root is $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses $e^{+2\pi i/n}$); over a commutative ring $R$, $\omega$ is a principal $n$-th [root of unity](/roots-of-unity/). The DFT is $X_k = \sum_j x_j \omega^{jk}$, and the inverse carries the factor $1/n$. We write $\mathrm{rev}_t(j)$ for the number whose $t$ binary digits are those of $j$ in reverse order, and $P$ for the permutation that moves the entry at position $\mathrm{rev}_t(i)$ to position $i$.

**Input.** $x \in R^n$ and $\omega$ with $\omega^{n/2} = -1$ when $n \ge 2$. This follows from $\omega$ being principal whenever $\frac{n}{2}$ is not a zero divisor of $R$, so over every field of characteristic other than $2$ and every $\mathbb{Z}/p\mathbb{Z}$ with $p$ odd; the radix-2 split needs it. For the convolution, two vectors $a, b \in R^n$, and $n$ must be a unit of $R$.

**Output.** $X = \mathrm{DFT}_\omega(x)$ in natural order, or the cyclic convolution $c_m = \sum_j a_j b_{(m - j) \bmod n}$.

**Cost model.** Additions (with subtractions) and multiplications in $R$ are counted separately, each at unit cost, as in the [real RAM](/real-ram/) for $R = \mathbb{C}$ and the [word RAM](/word-ram/) for $\mathbb{Z}/p\mathbb{Z}$ with $p$ below the word size. Index arithmetic and data moves are counted apart, as $O(n \log n)$ steps.

## The algorithm

The decimation-in-frequency stage with half length $h$ splits the array into blocks of length $2h$, and in each block replaces the pair $(a, b)$ at offsets $k$ and $k + h$ by $(a + b,\ W_h^k (a - b))$, with $W_h = \omega^{n/(2h)}$. The stages run from $h = n/2$ down to $h = 1$. The decimation-in-time stages without a permutation are the stages of the FFT page, with $h$ from $1$ up to $n/2$.

```pseudo id=main
ITERATIVE-FFT(x, ω)          ▷ x[0 .. n − 1], n = 2^t; ω a principal n-th root of unity
L1  n ← |x|
L2  W[k] ← ω^k for k = 0, …, n/2 − 1              ▷ twiddle factors
L3  h ← n/2                                        ▷ decimation-in-frequency stages
L4  while h ≥ 1 do
L5      for s ← 0 to n − 1 step 2h do
L6          for k ← 0 to h − 1 do
L7              a ← x[s + k], b ← x[s + k + h]
L8              x[s + k] ← a + b
L9              x[s + k + h] ← W[k · n/(2h)] · (a − b)
L10     h ← h/2
L11 for j ← 0 to n − 1 do                          ▷ x now holds X in bit-reversed order
L12     if j < rev_t(j) then swap x[j] and x[rev_t(j)]

CYCLIC-CONVOLUTION(a, b, ω)  ▷ n a unit of R; no permutation anywhere
L13 run lines L3 to L10 on a and on b             ▷ both spectra in bit-reversed order
L14 c[j] ← a[j] · b[j] for j = 0, …, n − 1
L15 V[k] ← ω^(−k) for k = 0, …, n/2 − 1
L16 h ← 1                                          ▷ decimation-in-time stages, root ω^(−1)
L17 while h < n do
L18     for s ← 0 to n − 1 step 2h do
L19         for k ← 0 to h − 1 do
L20             u ← c[s + k], v ← V[k · n/(2h)] · c[s + k + h]
L21             c[s + k] ← u + v, c[s + k + h] ← u − v
L22     h ← 2h
L23 return n^(−1) · c
```

Lines L3 to L10 leave $X_{\mathrm{rev}_t(i)}$ at position $i$, so the swap of lines L11 and L12 restores natural order. Lines L16 to L22 are the decimation-in-time stages, which read their input in bit-reversed order and write their output in natural order. In the convolution, the pointwise product of line L14 does not care about order: the entry at position $i$ of $c$ is $\hat a_{\mathrm{rev}_t(i)} \hat b_{\mathrm{rev}_t(i)}$, which is exactly the bit-reversed order the stages of lines L16 to L22 expect. So the two permutations cancel without being done.

The order of the loops can be changed without changing the result, because the butterflies of one stage touch disjoint pairs. With the loop over $k$ outside the loop over $s$, each twiddle factor is read once per stage instead of once per block; with $s$ outside, the inner loop walks contiguous memory. Libraries choose by the size of the block and the cache.

## Example

Over $\mathbb{Z}/17\mathbb{Z}$ with $n = 8$, $\omega = 2$ (a principal $8$-th root, since $2^4 = 16 \equiv -1$) and $x = (1, 2, 3, 4, 5, 6, 7, 8)$. The table is $W = (1, 2, 4, 8)$, and all values are reduced modulo $17$.

| step | twiddles used | the array |
|---|---|---|
| input | | 1 2 3 4 5 6 7 8 |
| stage $h = 4$ | 1, 2, 4, 8 | 6 8 10 12 13 9 1 2 |
| stage $h = 2$ | 1, 4 | 16 3 13 1 14 11 12 11 |
| stage $h = 1$ | 1 | 2 13 14 12 8 3 6 1 |
| L11 to L12, bit reversal | | 2 8 14 6 13 3 12 1 |

In the first stage, the pair at positions $1$ and $5$ is $(2, 6)$, which becomes $2 + 6 = 8$ and $2 \cdot (2 - 6) = -8 \equiv 9$. The last row is $X = (2, 8, 14, 6, 13, 3, 12, 1)$, the same as on the FFT page; the row before it is $(X_0, X_4, X_2, X_6, X_1, X_5, X_3, X_7)$.

For the convolution, take $n = 4$, $\omega = 4$ (a principal $4$-th root modulo $17$), $a = (1, 2, 0, 0)$ and $b = (3, 4, 0, 0)$. Lines L3 to L10 give $\hat a = (3, 16, 9, 10)$ and $\hat b = (7, 16, 2, 4)$, the spectra in the order $(X_0, X_2, X_1, X_3)$. Their product is $c = (4, 1, 1, 6)$. Lines L16 to L22 with $\omega^{-1} = 13$ give $(12, 6, 15, 0)$, and times $4^{-1} = 13$ this is $(3, 10, 8, 0)$, the product $(1 + 2t)(3 + 4t) = 3 + 10t + 8t^2$. Each value was checked by script.

## Correctness

**Decimation in frequency.** Let $D_t$ be the map of lines L3 to L10 on an array of length $2^t$ with root $\omega$. The claim is $D_t(x) = P\,\mathrm{DFT}_\omega(x)$, that is, position $i$ ends with $X_{\mathrm{rev}_t(i)}$. Proof by induction on $t$; $t = 0$ is trivial. The first stage ($h = n/2$, one block) makes $u_j = x_j + x_{j + n/2}$ and $v_j = \omega^j (x_j - x_{j + n/2})$ for $j < n/2$. Splitting the sum for $X_k$ at $n/2$ and using $\omega^{n/2} = -1$,

$$X_{2m} = \sum_{j < n/2} u_j (\omega^2)^{jm}, \qquad X_{2m+1} = \sum_{j < n/2} v_j (\omega^2)^{jm}.$$

The later stages never mix the two halves, and on each half they are exactly $D_{t-1}$ with the root $\omega^2$, since $W[k \cdot n/(2h)] = (\omega^2)^{k \cdot (n/2)/(2h)}$. By induction, position $q < n/2$ ends with $X_{2\,\mathrm{rev}_{t-1}(q)}$ and position $n/2 + q$ with $X_{2\,\mathrm{rev}_{t-1}(q) + 1}$, and these indices are $\mathrm{rev}_t(q)$ and $\mathrm{rev}_t(n/2 + q)$. Lines L11 and L12 apply $P^{-1} = P$, so ITERATIVE-FFT returns $X$.

**Decimation in time.** In the same way, the stages $h = 1, \ldots, n/2$ of lines L16 to L22 with root $\omega$ map $P z$ to $\mathrm{DFT}_\omega(z)$: the first $t - 1$ stages act on each half alone, and the halves of $Pz$ are the bit-reversed even and odd parts of $z$, so by induction they become their DFTs $E$ and $O$ with root $\omega^2$; the last stage makes $E_k + \omega^k O_k = X_k$ and $E_k - \omega^k O_k = X_{k + n/2}$.

**Convolution.** After line L14, $c = P(\hat a \odot \hat b)$, where $\odot$ is the entrywise product, since $P$ commutes with it. Lines L16 to L22 with root $\omega^{-1}$ then give $\mathrm{DFT}_{\omega^{-1}}(\hat a \odot \hat b)$, which by the [convolution theorem](/convolution-theorem/) and the inverse formula is $n \cdot (a \ast b)$; line L23 removes the $n$. The details are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Ring operations.** Each stage has $n/2$ butterflies with one addition, one subtraction and one multiplication, and there are $t = \lg n$ stages. So ITERATIVE-FFT does exactly $n \lg n$ additions and subtractions and $\frac{n}{2}\lg n$ multiplications, plus at most $n/2$ multiplications for the table, once per length. Of the multiplications, the $n - 1$ by $W[0] = 1$ can be skipped. The convolution does three transforms, $n$ pointwise products and $n$ scalings: $3 n \lg n$ additions and $\frac{3}{2} n \lg n + 2n$ multiplications.

**Time and space.** The operation sequence depends only on $n$, so the time is $\Theta(n \log n)$ in every case. The array is transformed in place; the twiddle table and the table of reversed indices take $\Theta(n)$ extra space. The bit reversal is $O(n)$ swaps, but each swap touches two distant cells, and on large arrays it can cost a noticeable part of the run time; the convolution form avoids it.

**Rounding errors (proved).** Over $\mathbb{C}$ in floating point with unit roundoff $u$, Higham, Theorem 24.2, proves for the radix-2 FFT that $\lVert \hat X - X \rVert_2 \le \frac{\lg n \cdot \eta}{1 - \lg n \cdot \eta} \lVert X \rVert_2$ with $\eta = \mu + \gamma_4(\sqrt 2 + \mu)$, where $\mu$ bounds the relative errors of the twiddle factors. Each decimation-in-frequency stage is again $\sqrt 2$ times a unitary matrix, computed by one rounded addition and one rounded multiplication per entry, and Higham's argument uses only this; so the same bound holds for both forms. The permutation is exact. *Observed:* the tests pass with the tolerance $64 (\lg n + 1) u \lVert X \rVert_2$ on random data.

## Properties

- **In place.** Each butterfly overwrites its two inputs, so only $O(1)$ ring elements of scratch are needed besides the array and the tables.
- **Oblivious.** Which cells are combined depends only on $n$, so the algorithm is a circuit of depth $\lg n$ stages, the [parallel FFT circuit](/parallel-fft-circuit/).
- **Exact over rings.** Over $\mathbb{Z}/p\mathbb{Z}$ the result is exact.
- **Dual forms.** The decimation-in-frequency stages are the decimation-in-time stages run backwards with each butterfly transposed: the matrix of one form, transposed, is the other with the stages in reverse order, since $F_n$ is symmetric.
- **Twiddle access.** The stage with half length $h$ reads the table with stride $n/(2h)$, so the early stages of decimation in frequency read all of it and the late ones read only $W[0]$.

## Variants and improvements

- **Decimation in time.** Bit reversal first, then the stages $h = 1, \ldots, n/2$; see the [FFT page](/fast-fourier-transform/).
- **No permutation at all.** Decimation in frequency for the forward transforms and decimation in time for the inverse, as in CYCLIC-CONVOLUTION. This is the standard design of [NTT](/number-theoretic-transform/) based [polynomial multiplication](/fft-polynomial-multiplication/).
- **Stockham autosort.** Use a second array and write each stage into it in an order that leaves the output sorted, trading the in-place property for a permutation-free, unit-stride form (Van Loan, Chapter 1).
- **Higher radix.** Combine two or three stages into one radix-4 or radix-8 pass, which touches memory fewer times and has more trivial twiddles; with mixed factors this is the [mixed-radix FFT](/mixed-radix-fft/), and the [split-radix FFT](/split-radix-fft/) lowers the count of real operations.
- **Real input.** Pack a real vector of length $2n$ into a complex vector of length $n$ and post-process; see the [real-valued FFT](/real-valued-fft/).
- **Inverse.** The [inverse FFT](/inverse-fft/) uses the same loops with $\omega^{-1}$ and a factor $1/n$.

## When to use it

Use an iterative form whenever an FFT is written by hand: it has no recursion overhead and no extra array, and every loop bound is known in advance. Use decimation in frequency when the input arrives in natural order and the output is consumed in any order, and pair it with decimation in time when transforming back, as in convolution and multiplication. Use a library FFT for large complex transforms, where cache-aware orderings and radix choices matter more than the operation count.

## Pitfalls

- **Wrong end permuted.** Decimation in frequency must not be preceded by a bit reversal, and decimation in time must be. Mixing them up gives a wrong answer that still has the right sum $X_0$.
- **Stride of the twiddles.** The stage with half length $h$ uses $\omega^{k n/(2h)}$, not $\omega^k$.
- **Overwriting before reading.** Both inputs of a butterfly must be read before either output is written.
- **Pointwise product order.** In the permutation-free convolution, both spectra must be in the same order, which holds when both come from the same decimation-in-frequency routine.
- **Twiddle accuracy.** Building $W$ by repeated multiplication makes the error of $W[k]$ grow with $k$; take entries from cosines and sines (see [twiddle factor](/twiddle-factor/)).

## Implementations

The Python file `impl/python/iterative_fft.py` has `iterative_fft`, the stage routines `dif_stages` and `dit_stages`, `bit_reverse`, and `cyclic_convolution`, with `# @line` markers for the pseudocode. It works over $\mathbb{C}$ and modulo a prime $p$, and over $\mathbb{C}$ it takes the twiddle factors from the exact angles. The tests compare with the direct $O(n^2)$ DFT and convolution modulo $17$, $97$ and $998244353$ with exact equality and in floating point with a tolerance proportional to $\lg n$; they check the bit-reversed orders of both stage routines, edge cases ($n = 1$ and $2$, zeros, impulses, constants, a delta in the convolution), the rejection of other lengths, polynomial products with zero padding, and the examples above.

## History

Cooley and Tukey (1965) published the algorithm in the form that splits the input by its index, now called decimation in time, and noted that the result comes out in digit-reversed order. Gentleman and Sande (1966) gave the form that splits the output index, now called decimation in frequency or the Sande-Tukey form, together with the general factorization with twiddle factors. CLRS, Section 30.3, presents the iterative decimation-in-time form with a separate bit-reversal copy.

## References
