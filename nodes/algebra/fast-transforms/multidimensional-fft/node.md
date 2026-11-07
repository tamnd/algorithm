---
tag: 98S7CV
kind: algorithm
slug: multidimensional-fft
name: Multidimensional FFT
aliases:
- multidimensional DFT
- row-column FFT
- 2D FFT
- row-column algorithm
area: algebra/fast-transforms
level: core
summary: Applies one-dimensional FFTs along each axis of a multidimensional array.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {N: the number of entries n_1 ⋯ n_d (each n_a a power of two), d: the number of axes, m: the largest axis length}
  time: {worst: Θ(N log N), average: Θ(N log N), best: Θ(N log N)}
  space: {extra: Θ(m)}
  additions: {worst: N lg N}
  multiplications: {worst: (N/2) lg N}
properties: {deterministic: true, recursive: false, in_place: true}
history:
  year: 1977
  people: [G. E. Rivard, D. B. Harris, J. H. McClellan, D. S. K. Chan, H. W. Schuessler]
  note: The row-column method follows from the separability of the kernel. In 1977 Rivard, and independently Harris, McClellan, Chan and Schuessler, gave the vector-radix FFT, which splits all axes at once.
prereqs: [fast-fourier-transform, discrete-fourier-transform, kronecker-product]
see_also: [iterative-fft, chinese-remainder-theorem-fft, convolution-theorem, phase-correlation, poisson-equation, real-valued-fft, tensor-product, cache-oblivious-model]
sources:
  - book: isbn:9780136049593
    title: Dan E. Dudgeon and Russell M. Mersereau, Multidimensional Digital Signal Processing, Prentice-Hall, 1984
    locator: the chapter on the discrete Fourier transform of multidimensional arrays (the row-column decomposition and the vector-radix FFT)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 3 (the multidimensional DFT written with Kronecker products, and row and column orderings)
  - paper: doi:10.1109/TASSP.1977.1162951
    title: G. E. Rivard, Direct fast Fourier transform of bivariate functions, IEEE Transactions on Acoustics, Speech, and Signal Processing 25(3), 1977
    locator: pp. 250 to 252 (the two-dimensional radix 2 by 2 decomposition)
  - paper: doi:10.1109/ICASSP.1977.1170349
    title: D. B. Harris, J. H. McClellan, D. S. K. Chan and H. W. Schuessler, Vector radix fast Fourier transform, ICASSP 1977
    locator: pp. 548 to 551
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, The Fast Fourier Transform and Applications, Theorem 24.2 (the normwise error bound of the radix-2 FFT)
---

The multidimensional DFT of a $d$-dimensional array $x$ of shape $n_1 \times \cdots \times n_d$ is

$$X_{k_1, \ldots, k_d} = \sum_{j_1 = 0}^{n_1 - 1} \cdots \sum_{j_d = 0}^{n_d - 1} x_{j_1, \ldots, j_d}\, \omega_1^{j_1 k_1} \cdots \omega_d^{j_d k_d},$$

with a root $\omega_a$ of order $n_a$ for each axis. The kernel is a product of one factor per axis, so the sum can be done one axis at a time: first a one-dimensional [DFT](/discrete-fourier-transform/) along every line in the direction of axis $1$, then along axis $2$, and so on. With the [FFT](/fast-fourier-transform/) for each line, this *row-column* method takes $\Theta(N \log N)$ operations for $N = n_1 \cdots n_d$ entries, the same as one FFT of length $N$. It is how images, volumes and other gridded data are transformed, and it reduces two- and three-dimensional convolution, filtering and spectral solvers to one-dimensional FFTs.

## In plain words

A picture is a grid of numbers. Its two-dimensional Fourier transform describes it as a sum of waves that run across the picture in every direction. Computing that directly would compare every pixel with every wave, which is far too slow for a real image.

The trick is that a wave running across the grid is the product of a wave along the rows and a wave along the columns. So one can transform each row on its own, then transform each column of the result on its own. Every step is an ordinary fast Fourier transform of one line. A cube of data works the same way, with a third pass along the depth. The total work is no more than one fast transform of a list holding all the numbers.

## The problem

**Notation.** As on all pages of fast transforms: over $\mathbb{C}$, $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign); over a commutative ring, each $\omega_a$ is a principal $n_a$-th [root of unity](/roots-of-unity/). The forward transform has no factor; the inverse uses $\omega_a^{-1}$ on each axis and the factor $1/N$. Here each $n_a$ is a power of two, so that each line can use the radix-2 FFT; other lengths need another one-dimensional FFT per axis.

**Input.** The axis lengths $n_1, \ldots, n_d$, the roots $\omega_1, \ldots, \omega_d$, and the array $x$ stored in row-major order: the entry $x_{j_1, \ldots, j_d}$ sits at position $j_1 \sigma_1 + \cdots + j_d \sigma_d$, with the *strides* $\sigma_a = n_{a+1} \cdots n_d$ (so $\sigma_d = 1$).

**Output.** The array $X$ above, in the same layout.

**Matrix form.** Written as a vector in row-major order, $X = (F_{n_1} \otimes F_{n_2} \otimes \cdots \otimes F_{n_d})\, x$, where $F_n$ is the [DFT matrix](/dft-matrix/) and $\otimes$ the [Kronecker product](/kronecker-product/). The row-column method is the factorization $F_{n_1} \otimes \cdots \otimes F_{n_d} = \prod_{a=1}^{d} (I_{N / (n_a \sigma_a)} \otimes F_{n_a} \otimes I_{\sigma_a})$, whose factors commute.

**Cost model.** Additions (with subtractions) and multiplications in the ring are counted separately, at unit cost, as in the [real RAM](/real-ram/) for $\mathbb{C}$ and the [word RAM](/word-ram/) for $\mathbb{Z}/p\mathbb{Z}$. Index arithmetic and data moves are counted apart.

## The algorithm

```pseudo id=main
MULTIDIM-FFT(x, (n_1, …, n_d), (ω_1, …, ω_d))   ▷ x in row-major order; each n_a a power of two
L1  N ← n_1 · n_2 ⋯ n_d
L2  for a ← 1 to d do
L3      σ ← n_(a+1) ⋯ n_d                         ▷ the stride of axis a
L4      W[k] ← ω_a^k for k = 0, …, n_a/2 − 1        ▷ twiddle factors of axis a
L5      for each start s = q · n_a σ + r with 0 ≤ q < N/(n_a σ) and 0 ≤ r < σ do
L6          ℓ ← (x[s], x[s + σ], …, x[s + (n_a − 1) σ])    ▷ one line along axis a
L7          FFT(ℓ, W)                              ▷ radix-2 FFT of length n_a
L8          x[s + i σ] ← ℓ[i] for i = 0, …, n_a − 1
```

Line L5 lists the $N / n_a$ lines along axis $a$: the starts are the positions whose coordinate $j_a$ is $0$, and the line through a start $s$ visits $s, s + \sigma, \ldots$, changing only $j_a$. Lines L6 and L8 copy the line into a buffer and back, so that the one-dimensional FFT works on contiguous data; it can also work in place with stride $\sigma$. The order of the axes does not matter, since the factors in the matrix form commute. The one-dimensional FFT of line L7 is the radix-2 [iterative FFT](/iterative-fft/), but any one-dimensional DFT algorithm can be used there, a different one for each axis if the lengths differ.

## Example

Over $\mathbb{Z}/17\mathbb{Z}$, transform the $2 \times 4$ array with rows $(1, 2, 3, 4)$ and $(5, 6, 7, 8)$. Take $\omega_1 = -1 \equiv 16$ for the axis of length $2$ and $\omega_2 = 13$ for the axis of length $4$ ($13 = 3^4 \bmod 17$, and $13^2 = 169 \equiv -1$). In row-major order, $x = (1, 2, 3, 4, 5, 6, 7, 8)$, with $\sigma_1 = 4$ and $\sigma_2 = 1$.

| step | row 0 | row 1 |
|---|---|---|
| input | 1 2 3 4 | 5 6 7 8 |
| axis 1: four columns of length 2, sum and difference | 6 8 10 12 | 13 13 13 13 |
| axis 2: two rows of length 4, root 13 | 2 12 13 14 | 1 0 0 0 |

For the first row of the last step, $X_{0,1} = 6 + 8 \cdot 13 + 10 \cdot 13^2 + 12 \cdot 13^3 \equiv 6 - 10 + 13 \cdot (8 - 12) = -56 \equiv 12$, using $13^2 \equiv -1$. The second row is the transform of the constant $-4 \equiv 13$, which is $(4 \cdot 13, 0, 0, 0) \equiv (1, 0, 0, 0)$. The result agrees with the direct $O(N^2)$ sum, checked by script.

## Correctness

Write $X^{(a)}$ for the array after the passes for axes $1, \ldots, a$. The claim is

$$X^{(a)}_{k_1, \ldots, k_a, j_{a+1}, \ldots, j_d} = \sum_{j_1, \ldots, j_a} x_{j_1, \ldots, j_d}\, \omega_1^{j_1 k_1} \cdots \omega_a^{j_a k_a}.$$

For $a = 0$ it is the input. The pass for axis $a$ applies a one-dimensional DFT with root $\omega_a$ to each line along axis $a$, which replaces the index $j_a$ by $k_a$ and multiplies by $\omega_a^{j_a k_a}$ summed over $j_a$; the other indices are fixed along the line. Inserting the claim for $a - 1$ and moving the sum over $j_a$ inside gives the claim for $a$. For $a = d$ it is the definition of $X$. The lines along one axis are disjoint and cover the array, so every entry is transformed exactly once per pass. The details are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Ring operations.** The pass for axis $a$ transforms $N / n_a$ lines of length $n_a$, each with $n_a \lg n_a$ additions and $\frac{n_a}{2} \lg n_a$ multiplications, so it costs $N \lg n_a$ additions and $\frac{N}{2} \lg n_a$ multiplications. Summed over the axes, since $\sum_a \lg n_a = \lg N$, this is exactly $N \lg N$ additions and $\frac{N}{2} \lg N$ multiplications, the same as one radix-2 FFT of length $N$. The tables cost at most $\sum_a n_a / 2$ more multiplications.

**Time and space.** The time is $\Theta(N \log N)$ in every case, plus $\Theta(N d)$ for copying lines, which is $O(N \log N)$ because each axis with $n_a \ge 2$ adds at least $1$ to $\lg N$ (axes of length $1$ can be skipped). The array is transformed in place; the line buffer and the table take $\Theta(m)$ extra space, where $m$ is the largest $n_a$.

**Memory access.** The lines along the last axis are contiguous, but the lines along axis $a$ have stride $\sigma_a$, which for a large array means one cache miss per entry. Practical codes transpose the array between passes, or process many lines at once so that each cache line is used fully; in the [external-memory model](/external-memory-model/) and the [cache-oblivious model](/cache-oblivious-model/) these choices decide the cost.

**Rounding errors.** Over $\mathbb{C}$ in floating point with unit roundoff $u$, the whole computation is a sequence of $\lg N$ radix-2 stages, each of which is $\sqrt 2$ times a unitary matrix computed with one rounded multiplication and addition per entry. Higham's Theorem 24.2 proves the bound $\lVert \hat X - X \rVert_2 / \lVert X \rVert_2 \le \lg n \cdot \eta / (1 - \lg n \cdot \eta)$, $\eta = \mu + \gamma_4(\sqrt 2 + \mu)$, for one radix-2 FFT of length $n$, and its proof uses only this stage structure; applied to the $\lg N$ stages here it gives the same bound with $\lg N$ in place of $\lg n$. We state this as a consequence of that argument, not as a quoted theorem. *Observed:* the tests pass with the tolerance $64 (\lg N + 1) u \lVert X \rVert_2$ on random data.

## Properties

- **Separable.** The transform of an outer product $x_{j_1, j_2} = u_{j_1} v_{j_2}$ is the outer product of the transforms, $X_{k_1, k_2} = \hat u_{k_1} \hat v_{k_2}$; the tests check this.
- **Axis order free.** The passes commute, so the axes can be processed in any order, which lets an implementation choose the order with the best memory access.
- **Exact over rings.** Over $\mathbb{Z}/p\mathbb{Z}$ every value is exact.
- **Same count as one dimension.** $N \lg N$ additions and $\frac{N}{2} \lg N$ multiplications for every shape with power-of-two sides, but the multiplications by trivial twiddle factors are more frequent, since short axes have few nontrivial ones.
- **Convolution theorem.** The multidimensional DFT turns the cyclic convolution on the grid $\mathbb{Z}_{n_1} \times \cdots \times \mathbb{Z}_{n_d}$ into the entrywise product, just as in one dimension.

## Variants and improvements

- **Vector radix.** Split all axes at once: for a $2^t \times 2^t$ array, one radix-$(2 \times 2)$ butterfly combines four entries with three nontrivial twiddle factors, and there are $N/4$ butterflies in each of $t = \frac12 \lg N$ stages, so $\frac{3N}{4} \cdot \frac{\lg N}{2} = \frac{3}{8} N \lg N$ multiplications, three quarters of the $\frac12 N \lg N$ of the row-column method. Rivard (1977) and Harris, McClellan, Chan and Schuessler (1977) introduced this form.
- **Transposition.** Transform the contiguous lines, transpose the array, and repeat; the transpose turns strided access into contiguous access. The four-step form of a one-dimensional FFT of length $n_1 n_2$ is the same idea applied to a reshaped vector, with [twiddle factors](/twiddle-factor/) between the steps.
- **Real data.** A real array has the symmetry $X_{-k} = \overline{X_k}$ in all coordinates at once, so about half the output suffices; transform the last axis with a [real-valued FFT](/real-valued-fft/) and the others as complex.
- **Prime factor map.** Conversely, a one-dimensional DFT of length $n_1 n_2$ with $\gcd(n_1, n_2) = 1$ is a two-dimensional DFT of shape $n_1 \times n_2$ after reindexing, with no twiddle factors: the [prime factor algorithm](/chinese-remainder-theorem-fft/).
- **Parallel and distributed.** For large three-dimensional transforms, each processor holds a slab or a pencil of lines, transforms its lines, and the processors exchange data in an all-to-all transpose between passes.
- **Other lengths.** Use a [mixed-radix FFT](/mixed-radix-fft/), [Rader's algorithm](/rader-fft/) or [Bluestein's algorithm](/bluestein-fft/) along each axis.

## When to use it

Use it for every transform of gridded data in two or more dimensions: images, volumes, video, and the grids of spectral methods for partial differential equations, such as fast solvers for the [Poisson equation](/poisson-equation/). Use it for two- and three-dimensional convolution and correlation with large kernels, for [phase correlation](/phase-correlation/) in image registration, and for multivariate polynomial multiplication. For small kernels, direct convolution is cheaper.

## Pitfalls

- **Wrong root per axis.** Each axis needs a root of its own order $n_a$; using one root for all axes is correct only when all $n_a$ are equal.
- **Layout.** Row-major and column-major storage give the same result only if the strides match the layout; transforming with the wrong strides transforms a transposed array, or a scrambled one.
- **Wrap-around.** Like the one-dimensional DFT, the multidimensional DFT computes cyclic convolutions: pad each axis to at least the sum of the two kernel extents minus one to get linear convolution.
- **Normalization.** The inverse divides by $N$, the total number of entries, not by any single $n_a$.
- **Cache behaviour.** A naive pass along the first axis of a large array is much slower than a pass along the last, though the operation counts are the same.

## Implementations

The Python file `impl/python/multidimensional_fft.py` takes a flat row-major list, a shape and one root per axis, over $\mathbb{C}$ or modulo a prime $p$, and follows the pseudocode with `# @line` markers. The tests compare it with the direct $O(N^2)$ multidimensional DFT for shapes from $1$ to $2 \times 2 \times 2 \times 2$, modulo $17$, $97$ and $998244353$ with exact equality and in floating point with a tolerance proportional to $\lg N$, and check the inverse, zeros, constants, impulses, separability on a $16 \times 32$ array, the rejection of bad shapes, and the example above.

## History

The row-column method needs no new idea beyond separability, and every FFT library provides it. Rivard (1977) published a direct radix-$(2 \times 2)$ decomposition for two-dimensional arrays, and Harris, McClellan, Chan and Schuessler presented the vector-radix FFT at ICASSP in the same year. Dudgeon and Mersereau (1984) give a textbook account of both methods for multidimensional signal processing.

## References
