---
tag: BWBTC5
kind: algorithm
slug: inverse-fft
name: Inverse FFT
aliases:
- IFFT
- inverse fast Fourier transform
area: algebra/fast-transforms
level: core
summary: Recovers polynomial coefficients from values at the roots of unity by running the FFT with the inverse root and dividing by n.
solves: [inverse-discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  additions: {worst: n lg n}
  multiplications: {worst: (n/2) lg n + n}
properties: {deterministic: true, recursive: false, in_place: true}
history:
  year: 1966
  people: [W. Morven Gentleman, Gordon Sande]
  note: The butterfly that undoes a stage, sum and difference first and the twiddle factor after, is the decimation-in-frequency butterfly of Gentleman and Sande (1966). The inverse formula with the factor 1/n is classical.
prereqs: [inverse-discrete-fourier-transform, fast-fourier-transform, butterfly-operation, bit-reversal-permutation]
see_also: [iterative-fft, twiddle-factor, number-theoretic-transform, fft-polynomial-multiplication, convolution-via-fft, discrete-fourier-transform, parseval-theorem, roots-of-unity]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2, The DFT and FFT (interpolation at the complex roots of unity by the FFT with the inverse root, followed by division by n)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.4, Weight and Butterfly Computations, and Section 1.9 (the Gentleman-Sande butterfly and the inverse transform)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, The Fast Fourier Transform and Applications, Theorem 24.2 (the normwise error bound of the radix-2 FFT)
  - paper: doi:10.1145/1464291.1464352
    title: W. Morven Gentleman and Gordon Sande, Fast Fourier transforms, for fun and profit, AFIPS Fall Joint Computer Conference, 1966
    locator: from p. 563 (the decimation-in-frequency form of the FFT)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2, The Discrete Fourier Transform and the Fast Fourier Transform (the inverse DFT over a ring, and its use in fast convolution)
---

The inverse FFT computes the [inverse DFT](/inverse-discrete-fourier-transform/) $x_j = \frac{1}{n} \sum_k X_k \omega^{-jk}$ in $\Theta(n \log n)$ ring operations when $n$ is a power of two. The simplest way is to call the forward [FFT](/fast-fourier-transform/) with the root $\omega^{-1}$ and divide by $n$. This page gives a second way that shows *why* the inverse is so cheap: it undoes the forward FFT one stage at a time, in reverse order. Each forward [butterfly](/butterfly-operation/) $(u, v) \mapsto (u + w v,\ u - w v)$ is undone, up to a factor $2$, by the butterfly $(a, b) \mapsto (a + b,\ w^{-1}(a - b))$, and the [bit-reversal permutation](/bit-reversal-permutation/) is undone by itself. The two programs together are the core of fast convolution, where one transforms, multiplies pointwise, and transforms back.

## In plain words

The fast Fourier transform works in rounds. In each round it takes pairs of numbers and replaces each pair by their sum and their difference, after turning one of them by a fixed amount. To undo a round, take the sum and the difference of the two new numbers again. This gives back twice the old numbers, with the second one still turned, so turn it back by the same amount in the other direction.

So the inverse does the rounds of the forward transform backwards, each one undone this way, and then puts the numbers back in their first order. Every round doubled everything, so at the end it divides by two once for each round, which is a division by the length. The work is the same as for the forward transform.

## The problem

**Notation.** As on all pages of fast transforms: $n$ is the transform length, here a power of two, $n = 2^t$. Over $\mathbb{C}$, $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy; CLRS uses $e^{+2\pi i/n}$, which swaps the roles of the two directions. Over a commutative ring $R$, $\omega$ is a principal $n$-th [root of unity](/roots-of-unity/). The forward transform is $X_k = \sum_j x_j \omega^{jk}$ with no factor.

**Input.** A commutative ring $R$ in which $n$ is a unit, a principal $n$-th root of unity $\omega$, and $X \in R^n$.

**Output.** The $x \in R^n$ with $\mathrm{DFT}_\omega(x) = X$, that is $x_j = \frac{1}{n}\sum_k X_k \omega^{-jk}$. It exists and is unique exactly because $n$ is a unit, as shown on the [problem page](/inverse-discrete-fourier-transform/).

**Cost model.** Ring additions (with subtractions) and ring multiplications are counted separately, at unit cost, as in the [real RAM](/real-ram/) for $R = \mathbb{C}$ and in the [word RAM](/word-ram/) for $\mathbb{Z}/p\mathbb{Z}$ with $p$ below the word size. Index arithmetic and the bit reversal are counted as $O(n)$ extra steps.

## The algorithm

Write $W_h = \omega^{n/(2h)}$, the root of the stage that builds blocks of length $2h$ in the forward [iterative FFT](/iterative-fft/). The forward stage replaces $(x[s + k], x[s + k + h])$ by $(u + W_h^k v,\ u - W_h^k v)$ for each block start $s$ and each $0 \le k < h$, and the forward FFT is the bit reversal followed by the stages $h = 1, 2, \ldots, n/2$. INVERSE-FFT runs the inverse stages for $h = n/2, \ldots, 2, 1$, then the bit reversal, then the scaling.

```pseudo id=main
INVERSE-FFT(X, ω)       ▷ X[0 .. n − 1] with n = 2^t; ω a principal n-th root; n a unit of R
L1  n ← |X|
L2  V[k] ← ω^(−k) for k = 0, …, n/2 − 1             ▷ inverse twiddle factors
L3  h ← n/2
L4  while h ≥ 1 do
L5      for s ← 0 to n − 1 step 2h do              ▷ the block X[s .. s + 2h − 1]
L6          for k ← 0 to h − 1 do
L7              a ← X[s + k], b ← X[s + k + h]
L8              X[s + k] ← a + b
L9              X[s + k + h] ← V[k · n/(2h)] · (a − b)   ▷ V[k · n/(2h)] = W_h^(−k)
L10     h ← h/2
L11 for j ← 0 to n − 1 do                          ▷ undo the bit-reversal permutation
L12     if j < rev_t(j) then swap X[j] and X[rev_t(j)]
L13 for j ← 0 to n − 1 do X[j] ← n^(−1) · X[j]
```

Line L2 builds one table of inverse twiddle factors, read with stride $n/(2h)$ as in the forward transform. Over $\mathbb{C}$, $\omega_n^{-k} = \overline{\omega_n^k}$, and the implementation takes each entry from the exact angle $2\pi k/n$ rather than by repeated multiplication, whose error grows with $k$ (see [twiddle factor](/twiddle-factor/)). Lines L7 to L9 are one inverse butterfly. If the forward stage turned $(u, v)$ into $(a, b) = (u + W v, u - W v)$, then $a + b = 2u$ and $W^{-1}(a - b) = 2v$: the pair is restored, doubled. The loop runs the stages from the last one back to the first, because the inverse of a composition is the composition of the inverses in reverse order. Lines L11 and L12 apply the bit reversal, which is its own inverse. After the $t$ stages every entry has been doubled $t$ times, so line L13 divides by $2^t = n$. If line L13 is left out, the result is $n x$, which is often wanted in convolution, where the factor can be folded into another step.

## Example

Over $\mathbb{Z}/17\mathbb{Z}$ with $n = 8$ and $\omega = 2$, a principal $8$-th root since $2^4 = 16 \equiv -1$, invert $X = (2, 8, 14, 6, 13, 3, 12, 1)$, which is the forward transform of $(1, 2, 3, 4, 5, 6, 7, 8)$ on the [FFT page](/fast-fourier-transform/). Here $\omega^{-1} = 9$, since $2 \cdot 9 = 18 \equiv 1$, and the table is $V = (1, 9, 13, 15)$. All values are reduced modulo $17$.

| step | twiddles used | the array |
|---|---|---|
| input | | 2 8 14 6 13 3 12 1 |
| undo stage $h = 4$ | 1, 9, 13, 15 | 15 11 9 7 6 11 9 7 |
| undo stage $h = 2$ | 1, 13 | 7 1 6 1 15 1 14 1 |
| undo stage $h = 1$ | 1 | 8 6 7 5 16 14 15 13 |
| L11 to L12, bit reversal | | 8 16 7 15 6 14 5 13 |
| L13, times $8^{-1} = 15$ | | 1 2 3 4 5 6 7 8 |

The row after the last stage is $8 \cdot (1, 5, 3, 7, 2, 6, 4, 8)$, eight times the bit-reversed input that the forward FFT started from. For instance, in the first stage the pair at positions $0$ and $4$ is $(2, 13)$: $2 + 13 = 15$ and $1 \cdot (2 - 13) = -11 \equiv 6$. Each row was checked by script.

## Correctness

Write $P$ for the bit-reversal permutation and $S_h$ for the forward stage with half length $h$, so that the forward FFT computes $S_{n/2} \circ \cdots \circ S_2 \circ S_1 \circ P = F_n$, the [DFT matrix](/dft-matrix/), as proved on the [FFT page](/fast-fourier-transform/). Let $I_h$ be the map of lines L5 to L9 for one value of $h$. The butterfly identity above gives $I_h \circ S_h = 2 \cdot \mathrm{id}$, and $P \circ P = \mathrm{id}$. All maps are $R$-linear, so the scalars move to the front, and lines L3 to L12 compute $G = P \circ I_1 \circ \cdots \circ I_{n/2}$ with

$$G \circ F_n = P \circ I_1 \circ \cdots \circ I_{n/2} \circ S_{n/2} \circ \cdots \circ S_1 \circ P = 2^t \cdot \mathrm{id} = n \cdot \mathrm{id}.$$

Since $n$ is a unit, $F_n$ is invertible, so $G = n F_n^{-1}$, and line L13 leaves $F_n^{-1} X = x$. The full proof is in [proofs/correctness.md](proofs/correctness.md). Note that the argument needs no division by $2$, only that $n$ is a unit, so it holds over $\mathbb{Z}/p\mathbb{Z}$ for each odd prime $p$ with $n \mid p - 1$; with line L13 removed it gives the unnormalized inverse $n x$.

## Complexity

**Ring operations.** Each of the $t = \lg n$ stages has $n/2$ inverse butterflies, each with one addition, one subtraction and one multiplication. So lines L4 to L10 do exactly $n \lg n$ additions and $\frac{n}{2} \lg n$ multiplications, the same as the forward FFT, and line L13 adds $n$ multiplications. Line L2 costs at most $n/2$ more multiplications, once per length. As in the forward transform, the factors $V[0] = 1$ in the $n - 1$ butterflies with $k = 0$ can be skipped.

**Time and space.** The operation sequence depends only on $n$, so the time is $\Theta(n \log n)$ in the best and in the worst case. The array is changed in place. The table $V$ and the reversed indices take $\Theta(n)$ extra space.

**Rounding errors.** Over $\mathbb{C}$ in floating point with unit roundoff $u$, Higham's Theorem 24.2 proves for the forward radix-2 FFT the bound $\lVert \hat X - X \rVert_2 / \lVert X \rVert_2 \le \lg n \cdot \eta / (1 - \lg n \cdot \eta)$, with $\eta = \mu + \gamma_4(\sqrt 2 + \mu)$ and $\mu$ the relative error of the twiddle factors. Calling the forward FFT with $\omega^{-1}$ therefore has this proved bound, and the scaling by $1/n$ is exact when $n$ is a power of two, unless it underflows. The stage-by-stage form of this page has stages $I_h = 2 S_h^{-1}$ that are again $\sqrt 2$ times a unitary matrix with one rounded multiplication and addition per entry, which is all that Higham's proof uses; we state the same bound for it on that basis, as an argument and not as a quoted theorem. *Observed:* the tests check the 2-norm error against $64 (\lg n + 1) u \lVert x \rVert_2$ on random inputs and pass with a wide margin.

## Properties

- **Exact over rings.** Only additions, subtractions and multiplications by fixed ring elements are used, with one final multiplication by $n^{-1}$.
- **In place.** Each butterfly writes back into the two cells it read.
- **Oblivious.** The operations depend only on $n$, so the algorithm is a circuit of depth $O(\log n)$, like the [parallel FFT circuit](/parallel-fft-circuit/).
- **Linear.** $G(\alpha X + \beta Y) = \alpha G(X) + \beta G(Y)$.
- **Order of data.** In this form the input is in natural order and the bit reversal comes last. Leaving out the bit reversal gives the inverse in bit-reversed order, which is enough when the next step reads the data in that order.

## Variants and improvements

- **Forward FFT with $\omega^{-1}$.** Call the forward FFT with the inverse root, then scale. This is how most libraries do it.
- **Index reversal.** Call the forward FFT with $\omega$ itself, then reverse the entries $1, \ldots, n-1$ and scale. The same twiddle table serves both directions.
- **Conjugation and swap.** Over $\mathbb{C}$, $x = \frac{1}{n}\overline{F_n \overline{X}}$, and also $x = \frac{1}{n} s(F_n s(X))$ with $s(a + bi) = b + ai$. Both reuse a forward routine with no change.
- **Halving per stage.** Multiply by $\frac12$ in each inverse butterfly instead of by $\frac1n$ at the end. In binary floating point the halving is exact, and the values stay the size of the data in every stage.
- **Without bit reversal.** Lines L3 to L10 alone compute $P F_{\omega^{-1}}$: natural order in, bit-reversed order out. Run with $\omega$ in place of $\omega^{-1}$, they are the decimation-in-frequency forward FFT. The forward decimation-in-time stages with the root $\omega^{-1}$ and no bit reversal do the opposite, bit-reversed order in and natural order out. Fast convolution pairs the two, with a pointwise product in between, and so needs no permutation at all; see the [iterative FFT](/iterative-fft/).
- **Exact transforms.** Over $\mathbb{Z}/p\mathbb{Z}$ this is the inverse [number-theoretic transform](/number-theoretic-transform/), with $n^{-1}$ computed once by a [modular inverse](/modular-inverse/).
- **Other lengths.** The [mixed-radix FFT](/mixed-radix-fft/) and [Bluestein's algorithm](/bluestein-fft/) invert in the same way, by the inverse root and a factor $1/n$.

## When to use it

Use it as the last step of every FFT convolution: [polynomial multiplication](/fft-polynomial-multiplication/), [convolution via FFT](/convolution-via-fft/), integer multiplication, correlation, and fast filtering. Use it to synthesize a signal or an interpolating trigonometric polynomial from its spectrum. When a library is available, use its inverse transform and check its normalization; write the stage-by-stage form when the forward transform is written by hand and the inverse should reuse its structure, or when an unnormalized or bit-reversed result is wanted.

## Pitfalls

- **Normalization.** Libraries differ on where the factor $1/n$ goes: on the inverse (FFTW leaves it out of both, so one must divide by hand; NumPy puts it on the inverse by default), on the forward, or $1/\sqrt n$ on both. A missing or doubled factor gives results off by $n$.
- **Wrong root.** The inverse must use the inverse of the root that the forward transform used. With the other sign convention, the "inverse" computes a reversed forward transform.
- **Order of stages.** Running the inverse butterflies with $h = 1, 2, \ldots$ instead of $h = n/2, \ldots, 1$ does not undo the transform.
- **$n$ not a unit.** Over $\mathbb{Z}/m\mathbb{Z}$ with even $m$, or over $\mathbb{Z}/p\mathbb{Z}$ with $p \mid n$, there is no $n^{-1}$; the unnormalized result $n x$ then loses information.
- **Twiddle accuracy.** Computing $V$ by repeated multiplication with $\omega^{-1}$ makes the error of $V[k]$ grow with $k$ and weakens the bound; take the entries from cosines and sines or by the symmetries.

## Implementations

The Python file `impl/python/inverse_fft.py` follows the pseudocode line for line, with `# @line` markers, and works over $\mathbb{C}$ or modulo a prime $p$. The flag `scale=False` leaves out line L13. It also contains the forward iterative FFT whose stages it undoes. The tests compare it with the direct $O(n^2)$ inverse modulo $17$, $97$ and $998244353$ with exact equality, and in floating point with a tolerance proportional to $\lg n$. They check that forward and inverse undo each other, cover $n = 1$ and $2$, zero, spike, constant and wave inputs, check that other lengths are rejected, and check the example above.

## History

The DFT inverse with the factor $1/n$ is classical, and CLRS derives it from the inverse of the Vandermonde matrix at the roots of unity. The butterfly $(a, b) \mapsto (a + b, (a - b) w)$ that this page uses to undo a stage is the decimation-in-frequency butterfly of Gentleman and Sande (1966), who also gave the general factorization with twiddle factors. That the stages of the decimation-in-time FFT are undone by decimation-in-frequency stages with inverse twiddles, up to a factor $2$, is a direct check, made on the [butterfly page](/butterfly-operation/).

## References
