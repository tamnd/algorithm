---
tag: KFMA92
kind: definition
slug: circular-convolution
name: Circular convolution
aliases:
- cyclic convolution
area: graphics-and-signals/signal-processing
level: core
summary: The convolution of two blocks of length L with indices taken modulo L. The DFT turns it into a product, and it equals linear convolution when L is at least N + M - 1.
prereqs: [discrete-convolution, discrete-fourier-transform]
see_also: [convolution, convolution-theorem, convolution-via-fft, overlap-add-method, overlap-save-method, dft-matrix, bluestein-fft]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 8.6 (circular convolution as a property of the DFT) and Section 8.7.2, Circular Convolution as Linear Convolution with Aliasing
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Section 7.2.2, Multiplication of Two DFTs and Circular Convolution
---

Circular convolution combines two blocks of $L$ samples as if each block were one period of a periodic signal: the index of the second block wraps around modulo $L$. It is the product that the [discrete Fourier transform](/discrete-fourier-transform/) turns into a pointwise product, so an FFT computes it in $O(L \log L)$ time. It equals the time-aliased [discrete convolution](/discrete-convolution/): the linear output folded onto $L$ samples. So it equals the linear convolution of lengths $N$ and $M$ exactly when $L \ge N + M - 1$, which is why FFT filtering pads with zeros. The algebraic form of the same operation, over any ring, is on the [convolution](/convolution/) page.

## Definition

**Blocks.** A block of length $L$ is a vector $x[0], \ldots, x[L-1]$. A shorter signal is a block of length $L$ after padding with zeros at the end.

**Definition.** The circular convolution of length $L$ of two blocks $x$ and $h$ of length $L$ is the block

$$(x \circledast_L h)[n] = \sum_{k=0}^{L-1} x[k]\, h[(n - k) \bmod L], \qquad 0 \le n \le L - 1.$$

It is the convolution over one period of the $L$-periodic extensions of $x$ and $h$. It costs $L^2$ multiplications by the definition.

**Matrix form.** $x \circledast_L h = C_h x$, where $C_h$ is the circulant matrix with entries $(C_h)_{n,k} = h[(n-k) \bmod L]$. Each column is the one before it, shifted down by one place with wrap-around.

**Convolution theorem.** Let $X[k] = \sum_{n=0}^{L-1} x[n] e^{-2\pi i k n / L}$ be the DFT of length $L$. Then

$$\mathrm{DFT}_L(x \circledast_L h)[k] = X[k]\, H[k], \qquad 0 \le k \le L - 1,$$

because $e^{-2\pi i k n / L}$ depends only on $n \bmod L$; see the [convolution theorem](/convolution-theorem/). The DFT matrix diagonalizes every circulant matrix, see the [DFT matrix](/dft-matrix/).

**Time aliasing.** Let $x$ have length $N$ and $h$ have length $M$, both at most $L$, and let $y = x * h$ be the linear convolution, of length $N + M - 1$. Then

$$(x \circledast_L h)[n] = \sum_{r \ge 0} y[n + rL], \qquad 0 \le n \le L - 1.$$

To see it, each term $x[k] h[j]$ of the linear sum lands at $k + j$, and in the circular sum at $(k + j) \bmod L$. So the circular output is the linear output with its samples at $n, n + L, n + 2L, \ldots$ added together.

**When the two agree.** If $L \ge N + M - 1$, then $y[n + rL] = 0$ for all $r \ge 1$ and $0 \le n \le L - 1$, so the circular convolution equals the linear convolution padded with zeros. If $N, M \ge 2$ and $L = N + M - 2$, then $(x \circledast_L h)[0] = y[0] + y[L] = x[0] h[0] + x[N-1] h[M-1]$, which differs from $y[0]$ whenever the last samples of both inputs are nonzero. So the bound $N + M - 1$ is tight.

## Examples and non-examples

- $[1, 2, 3, 4] \circledast_4 [1, 1, 0, 0] = [5, 3, 5, 7]$. The linear convolution is $[1, 3, 5, 7, 4]$, and its last sample $4$ wraps onto index $0$: $1 + 4 = 5$.
- $[1, 2, 3] \circledast_3 [4, 5] = [19, 13, 22]$. The linear convolution is $[4, 13, 22, 15]$ of length $4$, and $4 + 15 = 19$. With $L = 4 = N + M - 1$, the circular result is $[4, 13, 22, 15]$, the same as the linear one.
- **Circular shift.** $x \circledast_L \delta[n - n_0]$ is the circular shift $x[(n - n_0) \bmod L]$: samples that leave at the end come back at the start.
- **Identity.** $x \circledast_L \delta = x$, and the operation is commutative and associative, because it is the product in the ring of polynomials modulo $t^L - 1$.
- **Non-example.** A filter longer than the block, $M > L$, does not fit the definition; it must first be folded to length $L$ by adding $h[j]$ into $h[j \bmod L]$. The result is then the circular convolution with the folded filter, which is not the filtering of $x$ by $h$.
- **Non-example.** A pointwise product of two DFTs of length $L$, with no padding, does not give the linear convolution of two blocks of length $L$; it gives the circular one, with the last $L - 1$ samples of the linear output wrapped onto the first ones.

## Related definitions

- [Discrete convolution](/discrete-convolution/): the linear operation that circular convolution matches after zero padding.
- [Convolution](/convolution/): the algebraic problem, with the cyclic and negacyclic forms over a ring.
- [Convolution via FFT](/convolution-via-fft/): linear convolution by one circular convolution of a padded length.
- [Overlap-add method](/overlap-add-method/) and [overlap-save method](/overlap-save-method/): long linear convolutions by many circular convolutions of a short length. Overlap-add pads each block so nothing wraps; overlap-save lets the first $M - 1$ outputs wrap and discards them.
- [Bluestein FFT](/bluestein-fft/): a DFT of any length written as a convolution, which is then computed as a circular convolution of a power-of-two length.
- [Number-theoretic transform](/number-theoretic-transform/): circular convolution computed exactly modulo a prime.

## References
