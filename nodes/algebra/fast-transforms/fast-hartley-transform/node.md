---
tag: JPR6KM
kind: algorithm
slug: fast-hartley-transform
name: Fast Hartley transform
aliases:
- FHT
- radix-2 FHT
- Bracewell's algorithm
area: algebra/fast-transforms
level: advanced
summary: Computes the discrete Hartley transform in O(n log n) with only real arithmetic.
solves: [discrete-hartley-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(1)}
  multiplications: {worst: n lg n - 3n + 4}
  additions: {worst: (3/2) n lg n - (3/2) n + 2}
properties: {deterministic: true, recursive: false, in_place: true}
history:
  year: 1984
  people: [Ronald N. Bracewell]
  note: Bracewell published the radix-2 fast Hartley transform in 1984, a year after defining the discrete Hartley transform.
prereqs: [discrete-hartley-transform, fast-fourier-transform, bit-reversal-permutation]
see_also: [real-valued-fft, split-radix-fft, butterfly-operation, convolution-via-fft, fast-dct, fast-walsh-hadamard-transform, discrete-fourier-transform, convolution-theorem]
sources:
  - paper: doi:10.1109/PROC.1984.12968
    title: Ronald N. Bracewell, The fast Hartley transform, Proceedings of the IEEE 72(8), 1984
    locator: pp. 1010 to 1018 (the radix-2 decimation-in-time algorithm, its butterflies that read the entries k and h - k, and its use for real convolution)
  - paper: doi:10.1364/JOSA.73.001832
    title: Ronald N. Bracewell, Discrete Hartley transform, Journal of the Optical Society of America 73(12), 1983
    locator: p. 1832 onward (the definition, the inverse, and the conversion to the DFT)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 25, The Hartley transform (Section 25.2, Radix-2 FHT algorithms; 25.5, Real FFT by FHT and vice versa; 25.7, Convolution via FHT)
  - paper: doi:10.1109/TASSP.1985.1164687
    title: Henrik V. Sorensen, Douglas L. Jones, C. Sidney Burrus and Michael T. Heideman, On computing the discrete Hartley transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 33(5), 1985
    locator: pp. 1231 to 1238 (split-radix FHTs, and the comparison with real-valued FFTs)
  - paper: doi:10.1109/TASSP.1987.1165218
    title: Pierre Duhamel and Martin Vetterli, Improved Fourier and Hartley transform algorithms, application to cyclic convolution of real data, IEEE Transactions on Acoustics, Speech, and Signal Processing 35(6), 1987
    locator: pp. 818 to 824 (the DHT and the real DFT differ by O(n) operations, and real cyclic convolution)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, Section 24.1 (the stage-by-stage error analysis of the FFT, which the proof on this page follows)
---

The fast Hartley transform (FHT) computes the [discrete Hartley transform](/discrete-hartley-transform/) $H_k = \sum_j x_j \, \mathrm{cas}(2\pi jk/n)$, with $\mathrm{cas}\,\theta = \cos\theta + \sin\theta$, of a real vector of length $n = 2^t$ in $\Theta(n \log n)$ real operations, in place, without complex numbers. It has the shape of the iterative [radix-2 FFT](/fast-fourier-transform/): a [bit-reversal permutation](/bit-reversal-permutation/), then $\lg n$ passes that merge two half-length transforms into one. The difference is in the butterfly. Because $\mathrm{cas}$ of a sum is not a product, the odd half enters through the pair $O_k$ and $O_{h-k}$, so each butterfly reads and writes four entries, the indices $k$ and $h - k$ of both halves. Since the DHT is its own inverse up to $1/n$, the same routine computes the inverse. Bracewell published it in 1984.

## In plain words

The Hartley transform is a real cousin of the Fourier transform. The fast method splits the list into its entries at even and odd places, transforms each half, and combines the halves. As with the fast Fourier transform, doing this from the smallest pieces upward gives a method whose work grows only a little faster than the length.

The combining step is slightly different. Each output needs two entries of the odd half, one counted from the front and one from the back, turned by a known angle. So the method updates four places at a time instead of two. Running it twice and dividing by the length gives back the input, so one routine does both directions.

## The problem

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $n$ is the transform length and must be a power of two here; $\omega_n = e^{-2\pi i/n}$, with the minus sign of signal processing; the DFT is $X_k = \sum_j x_j \omega_n^{jk}$, and its inverse has the factor $1/n$. With this sign, $H_k = \mathrm{Re}\,X_k - \mathrm{Im}\,X_k$. Indices of a block of length $h$ are taken modulo $h$.

**Input.** A real vector $x$ of length $n = 2^t$. **Output.** $x$ replaced by its DHT $H$; the inverse replaces $H$ by $x = \frac{1}{n} \mathcal H_n H$.

**Cost model.** Real multiplications and real additions in the real RAM, counted separately; multiplications by $\pm 1$ and the $\cos$ and $\sin$ table are not counted. In floating point, the error is analysed below.

## The algorithm

```pseudo id=main
FHT(x)                  ▷ x[0 .. n − 1] real, n = 2^t; replaces x by its DHT
L1  n ← |x|
L2  for j ← 0 to n − 1 do if j < rev_t(j) then swap x[j] and x[rev_t(j)]
L3  h ← 1
L4  while h < n do
L5      for s ← 0 to n − 1 step 2h do         ▷ merge E = x[s .. s+h−1] and O = x[s+h .. s+2h−1]
L6          (x[s], x[s + h]) ← (x[s] + x[s + h], x[s] − x[s + h])                          ▷ k = 0
L7          if h ≥ 2 then (x[s + h/2], x[s + 3h/2]) ← (x[s + h/2] + x[s + 3h/2], x[s + h/2] − x[s + 3h/2])   ▷ k = h/2
L8          for k ← 1 to h/2 − 1 do
L9              c ← cos(πk/h); σ ← sin(πk/h)
L10             t1 ← c · x[s + h + k] + σ · x[s + 2h − k]; t2 ← σ · x[s + h + k] − c · x[s + 2h − k]
L11             e1 ← x[s + k]; e2 ← x[s + h − k]
L12             x[s + k] ← e1 + t1; x[s + h + k] ← e1 − t1
L13             x[s + h − k] ← e2 + t2; x[s + 2h − k] ← e2 − t2
L14     h ← 2h

INVERSE-FHT(y)
L15 FHT(y)
L16 for j ← 0 to n − 1 do y[j] ← y[j] / n
```

The merge rests on one identity. With $\theta_k = 2\pi k/(2h)$, the DHT of length $2h$ of a block whose even and odd entries have DHTs $E$ and $O$ of length $h$ is

$$H_k = E_k + \cos\theta_k \, O_k + \sin\theta_k \, O_{h-k}, \qquad H_{k+h} = E_k - \cos\theta_k \, O_k - \sin\theta_k \, O_{h-k},$$

because $\mathrm{cas}(a + b) = \cos b \, \mathrm{cas}\,a + \sin b \, \mathrm{cas}(-a)$. For $k = 0$ and $k = h/2$ the angle is $0$ or $\pi/2$, and the butterfly needs no multiplication (lines L6 and L7). For the other $k$, the outputs $k$ and $h - k$ use the same two entries $O_k$ and $O_{h-k}$, and $\theta_{h-k} = \pi - \theta_k$, so lines L10 to L13 compute both at once, with $t_2 = \cos\theta_{h-k} \, O_{h-k} + \sin\theta_{h-k} \, O_k$.

## Example

Transform $x = (1, 2, \ldots, 8)$, so $n = 8$ and $t = 3$.

| step | array |
|---|---|
| L2, bit reversal | 1 5 3 7 2 6 4 8 |
| h = 1, lines L6 | 6 −4 10 −4 8 −4 12 −4 |
| h = 2, lines L6 and L7 | 16 −8 −4 0 20 −8 −4 0 |
| h = 4, lines L6 and L7 | 36 −8 −8 0 −4 −8 0 0 |
| h = 4, k = 1, lines L10 to L13 | 36 −13.657 −8 −5.657 −4 −2.343 0 5.657 |

In the last pass, $c = \sigma = \frac{\sqrt 2}{2}$, the odd entries are $O_1 = x[5] = -8$ and $O_3 = x[7] = 0$, so $t_1 = t_2 = -4\sqrt 2$, and $E_1 = x[1] = -8$, $E_3 = x[3] = 0$, which gives $-8 \mp 4\sqrt 2$ at the places $1$ and $5$ and $\mp 4\sqrt 2$ at the places $3$ and $7$. The result $H \approx (36, -13.6569, -8, -5.6569, -4, -2.3431, 0, 5.6569)$ is the direct DHT. The pass $h = 4$ used $4$ multiplications, the only ones in the whole transform, as the count below predicts: $n \lg n - 3n + 4 = 24 - 24 + 4 = 4$. The trace was checked by script.

## Correctness

After line L2, $x[j] = x_{\mathrm{rev}_t(j)}$. The invariant is the same as for the [FFT](/fast-fourier-transform/): when line L4 tests $h$, each block $x[s \ldots s + h - 1]$ with $h \mid s$ holds the DHT of length $h$ of the subsequence $x_c, x_{c + n/h}, x_{c + 2n/h}, \ldots$ with $c = \mathrm{rev}_{t-q}(s/h)$ and $h = 2^q$. The two blocks merged by one pass of line L5 hold the DHTs of the even and the odd entries of the subsequence for the block of length $2h$, and lines L6 to L13 write, for each $k$, exactly the values of the merge identity, reading only the four cells they write. At $h = n$ the only block is the whole array, which holds the DHT of $x$. The inverse is correct because $\mathcal H_n^2 = n I$. The full proof is below.

## Complexity

**Operation count.** A merge of two blocks of length $h \ge 2$ does $h/2 - 1$ four-point butterflies, each with $4$ multiplications and $6$ additions, plus two butterflies with $2$ additions each; for $h = 1$ it does one butterfly with $2$ additions. Summed over the $n/(2h)$ blocks of each pass and over $h = 1, 2, \ldots, n/2$, this is exactly

$$n \lg n - 3n + 4 \text{ multiplications} \quad\text{and}\quad \tfrac{3}{2} n \lg n - \tfrac{3}{2} n + 2 \text{ additions}$$

for $n \ge 2$, about $\frac{5}{2} n \lg n$ real operations in total. The complex radix-2 FFT of the same real data, used naively, costs about $5 n \lg n$; a [real-valued FFT](/real-valued-fft/) costs about the same as the FHT. Using $\cos\frac{\pi}{4} = \sin\frac{\pi}{4}$ saves a little more, and split-radix FHTs lower the count further (Sorensen, Jones, Burrus and Heideman, 1985).

**Time and space.** $\Theta(n \log n)$ in every case, in place, with $\Theta(1)$ extra space besides the optional table of $n/2$ cosines and sines.

**Rounding errors (proved to first order).** Let each computed pair $(\cos\theta, \sin\theta)$ lie within Euclidean distance $\mu$ of the exact pair, and let $u$ be the unit roundoff with $\gamma_2 = 2u/(1 - 2u)$. Then the computed $\hat H$ satisfies

$$\frac{\lVert \hat H - H \rVert_2}{\lVert H \rVert_2} \le \lg n \, \left(u + \sqrt 2 \, (\mu + \gamma_2)\right) + O(u^2),$$

the same form as Higham's bound for the radix-2 FFT. The proof follows Higham's stage-by-stage argument, using that each pass is $\sqrt 2$ times an orthogonal map. Observed errors on random data are much smaller.

## Properties

- **Real arithmetic only.** Real input, real output, real intermediate values.
- **Self-inverse.** The same routine computes the forward and the inverse transform, up to the division by $n$.
- **In place.** The four-point butterfly reads and writes the same four cells.
- **Same access pattern as the FFT**, apart from the index $h - k$, which reads the odd block from both ends.

## Variants and improvements

- **Decimation in frequency.** The transposed algorithm takes natural order in and gives bit-reversed order out.
- **Split radix and higher radix.** Radix-4 and split-radix FHTs have lower operation counts, like their FFT counterparts.
- **FFT by FHT.** The DFT of real data follows from $H$ with $n$ additions, $X_k = \frac{1}{2}(H_k + H_{n-k}) - \frac{i}{2}(H_k - H_{n-k})$, and a complex FFT can be built from two FHTs.
- **Convolution by FHT.** Real cyclic convolution takes three FHTs and the Hartley convolution theorem, $Z_k = \frac{1}{2}\left(A_k(B_k + B_{n-k}) + A_{n-k}(B_k - B_{n-k})\right)$; the implementation includes this.
- **Other transforms.** The DCT and the DST can also be computed through FHTs, with $O(n)$ extra work.

## When to use it

Use the FHT when only real arithmetic is available or wanted, when one routine should serve both directions, or for real convolution with a small code size. When a good real-valued FFT library is available, it is about as fast, so the choice is one of convenience rather than speed.

## Pitfalls

- **The four-point butterfly.** Updating $k$ alone, without $h - k$, overwrites $O_{h-k}$ before it is used. Process the pair together, and treat $k = 0$ and $k = h/2$ separately.
- **The sign convention.** With $\omega_n = e^{+2\pi i/n}$, $H_k = \mathrm{Re}\,X_k + \mathrm{Im}\,X_k$; mixing conventions gives $H_{n-k}$ in place of $H_k$.
- **Speed claims.** The early claim that the FHT is faster than the FFT for real data holds only against a complex FFT used on real input; direct counts showed that real-valued FFTs are as fast.
- **Length.** The radix-2 FHT needs a power of two; pad and use the convolution form, or a mixed-radix FHT, otherwise.

## Implementations

## History

Hartley defined the continuous transform with the kernel $\mathrm{cas}$ in 1942. Bracewell defined the discrete transform in 1983 and gave the radix-2 fast algorithm in 1984, presenting it as a faster alternative to the FFT for real data. Sorensen, Jones, Burrus and Heideman (1985) developed split-radix FHTs and showed that real-valued FFTs reach the same operation counts, and Duhamel and Vetterli (1987) showed that the DHT and the real DFT convert into each other with $O(n)$ operations, so neither is intrinsically faster.

## References
