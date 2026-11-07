---
tag: C9SKTZ
kind: algorithm
slug: real-valued-fft
name: Real-valued FFT
aliases:
- real FFT
- RFFT
- FFT of real data
- packing algorithm
area: algebra/fast-transforms
level: advanced
summary: Computes the DFT of real input using a half-length complex FFT, exploiting conjugate symmetry.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  additions: {worst: (3/2) n lg n + (5/2) n + 8}
  multiplications: {worst: n lg n + 3n + 8}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1970
  people: [James W. Cooley, Peter A. W. Lewis, Peter D. Welch]
  note: Cooley, Lewis and Welch (1970) described computing the transform of real data with a complex FFT of half the length. Sorensen, Jones, Heideman and Burrus (1987) surveyed and compared real-valued FFT algorithms.
prereqs: [discrete-fourier-transform, fast-fourier-transform, twiddle-factor]
see_also: [iterative-fft, inverse-fft, split-radix-fft, discrete-cosine-transform, discrete-hartley-transform, discrete-sine-transform, fft-polynomial-multiplication, parseval-theorem]
sources:
  - paper: doi:10.1016/0022-460X(70)90075-1
    title: James W. Cooley, Peter A. W. Lewis and Peter D. Welch, The fast Fourier transform algorithm, programming considerations in the calculation of sine, cosine and Laplace transforms, Journal of Sound and Vibration 12(3), 1970
    locator: pp. 315 to 337 (the transform of real data by a complex FFT of half the length)
  - paper: doi:10.1109/TASSP.1987.1165220
    title: Henrik V. Sorensen, Douglas L. Jones, Michael T. Heideman and C. Sidney Burrus, Real-valued fast Fourier transform algorithms, IEEE Transactions on Acoustics, Speech, and Signal Processing 35(6), 1987
    locator: pp. 849 to 863 (real-valued FFT algorithms and their operation counts)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 4, Section 4.4, FFTs of Real Data (the half-length complex FFT and the splitting step)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, The Fast Fourier Transform and Applications, Theorem 24.2 (the normwise error bound of the radix-2 FFT)
---

The real-valued FFT computes the [discrete Fourier transform](/discrete-fourier-transform/) of $n$ real numbers with one complex [FFT](/fast-fourier-transform/) of length $n/2$ and $O(n)$ extra work, about half the cost of a complex FFT of length $n$. It packs the even samples into the real parts and the odd samples into the imaginary parts of $n/2$ complex numbers, transforms them, and then separates the two half-length transforms using conjugate symmetry and combines them with one radix-2 step. Since the DFT of real data satisfies $X_{n-k} = \overline{X_k}$, only $X_0, \ldots, X_{n/2}$ are returned, which is the same amount of information as the input. The inverse runs the steps backwards. Most FFT libraries offer this as their "real" or "r2c" transform.

## In plain words

Real data wastes half of a complex transform, because the imaginary parts are all zero. The trick is to fill them: put every second sample into the imaginary slots, so a list of real numbers becomes a list of half as many complex numbers. Transform that shorter list. The answer mixes the transforms of the even samples and the odd samples, but a mirror image of the answer unmixes them, because real data has a mirror-symmetric spectrum. One last combining step, the same as in an ordinary FFT, gives the spectrum of the whole list.

## The problem

**Notation.** As on all pages of fast transforms, $n$ is the transform length, here a power of two, and $\omega_n = e^{-2\pi i/n}$, the sign of signal processing, FFTW and NumPy (CLRS uses the other sign). The DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega_n^{jk}$ and the inverse is $x_j = \frac1n \sum_k X_k \omega_n^{-jk}$. Write $h = n/2$ and $\bar z$ for the complex conjugate. The algorithm needs a conjugation, so it is stated over $\mathbb{C}$; it also runs exactly over the ring $\mathbb{Z}_p[i] = \mathbb{Z}_p[t]/(t^2 + 1)$ for an odd prime $p$, with $\overline{a + bi} = a - bi$, the "real" numbers $\mathbb{Z}_p$, and a root $\omega$ with $\omega^n = 1$, $\omega^{h} = -1$ and $\omega \bar\omega = 1$, which is how the tests check it exactly.

**Input.** Real numbers $x_0, \ldots, x_{n-1}$.

**Output.** $X_0, \ldots, X_{h}$. The rest of the spectrum is $X_{n-k} = \overline{X_k}$, and $X_0$ and $X_h$ are real.

**Cost model.** Real additions (with subtractions) and real multiplications are counted separately, at unit cost, in the [real RAM](/real-ram/). A complex multiplication costs $4$ real multiplications and $2$ real additions, a complex addition $2$ real additions. All operations of the algorithm are counted, including multiplications by twiddle factors equal to $1$; the packing at line L2 only moves data. The table of powers of $\omega_n$ is built once from the exact angles and not counted.

## The algorithm

Let $e_j = x_{2j}$ and $o_j = x_{2j+1}$ for $0 \le j < h$, and let $E$ and $O$ be their DFTs of length $h$ (with the root $\omega_n^2$). The radix-2 splitting gives $X_k = E_k + \omega_n^k O_k$ for $0 \le k \le h$, with indices of $E, O$ taken modulo $h$. Pack $z_j = e_j + i\, o_j$ and let $Z = \mathrm{DFT}_h(z) = E + iO$. Since $e$ and $o$ are real, $\overline{E_{h-k}} = E_k$ and $\overline{O_{h-k}} = O_k$, so $\overline{Z_{h-k}} = E_k - i O_k$ and

$$E_k = \tfrac12 \left(Z_k + \overline{Z_{h-k}}\right), \qquad O_k = \tfrac{1}{2i} \left(Z_k - \overline{Z_{h-k}}\right).$$

```pseudo id=main
REAL-FFT(x)            ▷ x real, n = length(x) a power of two, n ≥ 2; returns X_0, …, X_(n/2)
L1  h ← n/2
L2  z_j ← x_(2j) + i · x_(2j+1) for j = 0, …, h − 1      ▷ pack
L3  Z ← FFT(z)                                    ▷ complex FFT of length h, root ω_n^2
L4  Z_h ← Z_0                                     ▷ indices modulo h
L5  for k ← 0 to h do
L6      E ← (Z_k + conj(Z_(h−k))) / 2              ▷ DFT of the even samples
L7      O ← (Z_k − conj(Z_(h−k))) / (2i)           ▷ DFT of the odd samples
L8      X_k ← E + ω_n^k · O                         ▷ one radix-2 butterfly
L9  return (X_0, …, X_h)
```

For $n = 1$ the output is $X_0 = x_0$. **Inverse.** Given $X_0, \ldots, X_h$, form $E_k = \frac12 (X_k + \overline{X_{h-k}})$ and $O_k = \frac12 (X_k - \overline{X_{h-k}})\, \omega_n^{-k}$ for $0 \le k < h$ (using $X_{k+h} = \overline{X_{h-k}}$), let $Z_k = E_k + i O_k$, apply the inverse complex FFT of length $h$, and read $x_{2j}$ and $x_{2j+1}$ from the real and imaginary parts.

## Example

For $x = (1, 2, 3, 4)$, $n = 4$, $h = 2$ and $\omega_4 = -i$. Line L2 packs $z = (1 + 2i, 3 + 4i)$, and line L3 gives $Z = (z_0 + z_1, z_0 - z_1) = (4 + 6i, -2 - 2i)$, with $Z_2 = Z_0$.

| k | Z_k | conj(Z_(h−k)) | E | O | ω_4^k | X_k = E + ω_4^k O |
|---|---|---|---|---|---|---|
| 0 | 4 + 6i | 4 − 6i | 4 | 6 | 1 | 10 |
| 1 | −2 − 2i | −2 + 2i | −2 | −2 | −i | −2 + 2i |
| 2 | 4 + 6i | 4 − 6i | 4 | 6 | −1 | −2 |

So $X = (10, -2 + 2i, -2)$, and $X_3 = \overline{X_1} = -2 - 2i$. Directly, $E = \mathrm{DFT}_2(1, 3) = (4, -2)$ and $O = \mathrm{DFT}_2(2, 4) = (6, -2)$, and $X_1 = 1 - 2i - 3 + 4i = -2 + 2i$. The inverse transform returns $(1, 2, 3, 4)$. All values were checked by script.

## Correctness

Line L3 computes $Z = E + iO$ by linearity of the DFT. For $0 \le k \le h$, conjugating $Z_{h-k} = \sum_j (e_j + i o_j) \omega_n^{2j(h-k)}$ and using that $e_j, o_j$ are real and $\overline{\omega_n^{2j(h-k)}} = \omega_n^{2jk}$ gives $\overline{Z_{h-k}} = E_k - i O_k$. Adding and subtracting, lines L6 and L7 recover $E_k$ and $O_k$. Line L8 is the radix-2 identity $X_k = E_k + \omega_n^k O_k$, valid for every $k$ because $E$ and $O$ have period $h$. Over $\mathbb{Z}_p[i]$ the same steps use only $\overline{\omega} = \omega^{-1}$ and that conjugation fixes $\mathbb{Z}_p$. The full proof, with the inverse and the operation counts, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

**Operations.** The complex FFT of length $h = n/2$ by the radix-2 method does $\frac{h}{2} \lg h$ complex multiplications and $h \lg h$ complex additions, that is $n(\lg n - 1)$ real multiplications and $\frac32 n (\lg n - 1)$ real additions. Each of the $h + 1$ iterations of lines L5 to L8 does $8$ real additions (two complex sums at L6 and L7, the complex product's $2$, and the final sum) and $8$ real multiplications (two scalings by $\frac12$ and $\frac{1}{2i}$, $2$ each, and the complex product, $4$). In total

$$n \lg n + 3n + 8 \text{ real multiplications}, \qquad \tfrac32 n \lg n + \tfrac52 n + 8 \text{ real additions},$$

against $2 n \lg n$ and $3 n \lg n$ for a complex radix-2 FFT of length $n$ applied to the real data. The time is $\Theta(n \log n)$ for every input. Folding the factors $\frac12$ into the table, skipping the trivial twiddles, and using a better complex FFT lower these counts; the [split-radix FFT](/split-radix-fft/) adapted to real data needs fewer operations still.

**Space.** The packed array and the output take $\Theta(n)$ space; the transform can be done in place in the packed array, with $X_0$ and $X_h$ (both real) sharing one complex slot.

**Rounding errors.** Over $\mathbb{C}$ in floating point, line L3 is a radix-2 FFT of length $n/2$, for which Higham's Theorem 24.2 proves a normwise relative error bound of order $u \lg n$. Lines L6 to L8 are a linear map applied entrywise with $O(1)$ rounding errors each. *Not proved here:* we do not state a combined bound. *Observed:* on Gaussian random data, the relative $2$-norm error of a forward and inverse round trip was $9u$ at $n = 1024$, $14u$ at $n = 2^{14}$ and $16u$ at $n = 2^{16}$. The tests use the tolerance $64 (\lg n + 2)\, u \lVert X \rVert_2$.

## Properties

- **Half the work.** About half the operations and half the memory of a complex FFT of the same length.
- **Half the output.** The output has $h + 1$ complex numbers, two of them real: $n$ real numbers in all, the same as the input.
- **Not in place as written.** The output has one more complex entry than the packed array; in-place codes pack $X_h$ into the imaginary part of $X_0$.
- **Exact over $\mathbb{Z}_p[i]$.** With a root of norm $1$ the computation is exact.
- **Deterministic.** The operation count does not depend on the data.

## Variants and improvements

- **Two real transforms at once.** For two real sequences $a$ and $b$ of length $n$, one complex FFT of $a + ib$ gives both: $A_k = \frac12 (Z_k + \overline{Z_{n-k}})$ and $B_k = \frac{1}{2i} (Z_k - \overline{Z_{n-k}})$. This is lines L6 and L7 without line L8, and it is common in [FFT polynomial multiplication](/fft-polynomial-multiplication/).
- **Real-input FFTs built from scratch.** Instead of packing, a radix-2 or split-radix FFT can be specialized to real input by keeping only half of each conjugate-symmetric intermediate result; Sorensen, Jones, Heideman and Burrus (1987) compare such algorithms.
- **The Hartley transform.** The [discrete Hartley transform](/discrete-hartley-transform/) is a real-to-real transform with the same information, and has its own fast algorithms.
- **Cosine and sine transforms.** The [discrete cosine transform](/discrete-cosine-transform/) and [discrete sine transform](/discrete-sine-transform/) of real data are computed by real FFTs of related lengths after symmetric extension.
- **Mixed radix.** Any even $n$ works if the complex FFT of length $n/2$ handles that length.

## When to use it

Use it for any transform of real data: audio, images, sensor signals, and polynomial multiplication with real or integer coefficients. It is the default in libraries for real input. It does not apply to complex data, and over $\mathbb{Z}/p\mathbb{Z}$ (the [number-theoretic transform](/number-theoretic-transform/)) there is no conjugation, so this packing does not apply directly.

## Pitfalls

- **The index $h - k$ at $k = 0$.** It refers to $Z_h$, which is $Z_0$ by periodicity; forgetting line L4 reads past the array.
- **Conjugating the wrong term.** The formula uses $\overline{Z_{h-k}}$, not $\overline{Z_k}$ or $Z_{h-k}$.
- **The sign of the twiddle.** With $\omega_n = e^{-2\pi i/n}$, line L8 multiplies by $e^{-2\pi i k/n}$, and the inverse by $e^{+2\pi i k/n}$.
- **The output length.** There are $n/2 + 1$ outputs, not $n/2$: $X_h$ is needed, and is lost if the loop stops at $h - 1$.
- **Inverse input.** The inverse assumes conjugate symmetry; if $X_0$ or $X_h$ has a nonzero imaginary part (for example after filtering), the program still returns a real sequence, but its transform is not the given input, and no error is raised.

## Implementations

The Python implementation in [impl/python/real_valued_fft.py](impl/python/real_valued_fft.py) follows the main block over $\mathbb{C}$, with twiddles from the exact angles, and runs unchanged over $\mathbb{Z}_p[i]$ through a small class of Gaussian residues. The tests compare it exactly with the direct $O(n^2)$ DFT over $\mathbb{Z}_p[i]$ for $p = 17$, $97$ and $998244353$ (all $1 \bmod 4$, with roots built from the primitive roots $3$, $5$ and $3$) and for $p = 127$ (where $\mathbb{Z}_p[i]$ is a field), for every power of two up to $64$ or $128$; over $\mathbb{C}$ for every power of two up to $1024$ within the tolerance above; and check the inverse, zeros, an impulse, a constant, $n = 1$ and $2$, and a round trip with Parseval's identity at $n = 2^{14}$.

## History

Cooley, Lewis and Welch (1970) discussed the computation of sine, cosine and real transforms with the FFT, including the transform of real data through a complex FFT of half the length. Sorensen, Jones, Heideman and Burrus (1987) surveyed real-valued FFT algorithms, including specialized forms of the radix-2 and split-radix FFTs, and compared their operation counts. Van Loan (1992) presents the packing method in matrix form.

## References
