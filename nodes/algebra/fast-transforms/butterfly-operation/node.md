---
tag: 4W6969
kind: concept
slug: butterfly-operation
name: Butterfly operation
aliases:
- FFT butterfly
- radix-2 butterfly
- Cooley-Tukey butterfly
- Gentleman-Sande butterfly
area: algebra/fast-transforms
level: core
summary: The two-input, two-output combining step (x, y) -> (x + w y, x - w y) repeated in FFT stages.
prereqs: [discrete-fourier-transform, fft-cancellation-lemma]
see_also: [fast-fourier-transform, iterative-fft, twiddle-factor, bit-reversal-permutation, fft-halving-lemma, parallel-fft-circuit, fast-walsh-hadamard-transform, number-theoretic-transform]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.3, Efficient FFT implementations (the butterfly operation, the iterative FFT and the parallel FFT circuit)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.4, Weight and Butterfly Computations, and Section 1.9 (the Gentleman-Sande butterfly of decimation in frequency)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 21, Section 21.2, Radix-2 FFT algorithms (decimation in time and in frequency butterflies)
  - paper: doi:10.1145/1464291.1464352
    title: W. Morven Gentleman and Gordon Sande, Fast Fourier transforms, for fun and profit, AFIPS Fall Joint Computer Conference 29, 1966
    locator: pp. 563 to 578 (decimation in frequency, and the rounding error of the FFT)
---

A butterfly is the basic step of the [fast Fourier transform](/fast-fourier-transform/): it takes two values $x$ and $y$ and a [twiddle factor](/twiddle-factor/) $w$, and returns $x + wy$ and $x - wy$. One multiplication and two additions give two outputs, because the product $wy$ is shared. A radix-2 FFT of length $n = 2^t$ is nothing but $t$ stages of $n/2$ butterflies each, which is where its counts of $\frac{n}{2} \lg n$ multiplications and $n \lg n$ additions come from. The name comes from the shape of the drawing of one butterfly in the data flow graph: two crossing lines between two pairs of points.

## In plain words

Take two numbers. Scale the second one by a fixed factor, then write down two results: the first number plus the scaled one, and the first number minus the scaled one. That is a butterfly. It does one multiplication and gets two useful answers out of it.

The fast Fourier transform is built from many of these little steps. It first pairs up the numbers in a special order and runs a butterfly on each pair. Then it pairs up the results at a wider distance and runs butterflies again, and so on, doubling the distance each round. After as many rounds as there are halvings of the length, the transform is done.

## The idea

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $n$ is the transform length, a power of two for the radix-2 FFT, $\omega_n = e^{-2\pi i/n}$ over $\mathbb{C}$ (the statements also hold for $e^{+2\pi i/n}$), and in a commutative ring $R$, $\omega$ is a principal $n$-th root of unity. The DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$.

**Where it comes from.** Split $x$ into its even and odd entries, with DFTs $E$ and $O$ of length $n/2$, taken with the root $\omega^2$. Then $X_k = E_k + \omega^k O_k$, and since $\omega^{n/2} = -1$ by the [cancellation lemma](/fft-cancellation-lemma/), also $X_{k + n/2} = E_k - \omega^k O_k$, for $0 \le k < n/2$. So the pair $(E_k, O_k)$ gives the pair $(X_k, X_{k+n/2})$ by one butterfly with $w = \omega^k$.

**Decimation in time (Cooley-Tukey).** The butterfly

$$\begin{pmatrix} u \\ v \end{pmatrix} = \begin{pmatrix} 1 & w \\ 1 & -w \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix} \begin{pmatrix} 1 & 0 \\ 0 & w \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}$$

first multiplies $y$ by the twiddle factor, then takes the sum and difference. This is the butterfly of the [iterative FFT](/iterative-fft/), which runs on the input in [bit-reversed order](/bit-reversal-permutation/).

**Decimation in frequency (Gentleman-Sande).** The butterfly $(x, y) \mapsto (x + y, (x - y) w)$ takes the sum and difference first and then multiplies the difference. It is the step of the FFT that splits the *output* into even and odd indices, takes input in natural order, and produces output in bit-reversed order.

**Inverse.** If $w$ and $2$ are units, the decimation-in-time butterfly has the inverse $x = \frac{1}{2}(u + v)$, $y = \frac{1}{2} w^{-1} (u - v)$: a decimation-in-frequency butterfly with $w^{-1}$, followed by halving. This is why running the stages in reverse order with inverse twiddles gives the [inverse FFT](/inverse-fft/), with the factors $\frac{1}{2}$ of the $\lg n$ stages combining to $\frac{1}{n}$.

**Cost.** In the ring $R$, one butterfly costs one multiplication and two additions (counting a subtraction as an addition). A radix-2 FFT of length $n$ has $\lg n$ stages of $n/2$ butterflies, so it uses $\frac{n}{2} \lg n$ multiplications and $n \lg n$ additions. Over $\mathbb{C}$ with real arithmetic, a complex product costs $4$ real multiplications and $2$ real additions, and each complex addition costs $2$ real additions, so a butterfly costs $10$ real operations and the FFT about $5 n \lg n$. Butterflies with $w = 1$ or $w = -i$ need no multiplication. Removing them, and grouping stages into larger butterflies, is what radix-4 and [split-radix](/split-radix-fft/) FFTs do.

**In place.** A butterfly reads two memory cells and writes its two outputs back into the same cells. A whole FFT can therefore run in the input array, with $O(1)$ extra space besides the twiddle factors.

**Rounding.** When $|w| = 1$, the matrix $\frac{1}{\sqrt 2}\left(\begin{smallmatrix} 1 & w \\ 1 & -w \end{smallmatrix}\right)$ is unitary, so a stage of butterflies multiplies every vector, and every earlier error, by exactly $\sqrt 2$ in the 2-norm. Errors are therefore not magnified relative to the data, and the rounding errors of the $\lg n$ stages add up instead of compounding. This is why the relative error of the FFT grows like $\lg n$ times the unit roundoff; the proved bound is on the [FFT page](/fast-fourier-transform/).

## Examples

- Over $\mathbb{C}$, with $x = 1$, $y = 2$ and $w = -i$: $wy = -2i$, so the outputs are $1 - 2i$ and $1 + 2i$.
- Over $\mathbb{Z}/17\mathbb{Z}$, with $x = 3$, $y = 5$ and $w = 4$: $wy = 20 \equiv 3$, so the outputs are $6$ and $0$.
- The DFT of length $2$ is a single butterfly with $w = 1$: $(x_0, x_1) \mapsto (x_0 + x_1, x_0 - x_1)$.
- **A full FFT of length $4$.** For $x = (1, 2, 3, 4)$, the bit-reversed order is $(1, 3, 2, 4)$. Stage 1, with $w = 1$ on the pairs at distance $1$: $(1, 3) \mapsto (4, -2)$ and $(2, 4) \mapsto (6, -2)$, giving $(4, -2, 6, -2)$. Stage 2, on the pairs at distance $2$: $w = 1$ on $(4, 6)$ gives $(10, -2)$, and $w = \omega_4 = -i$ on $(-2, -2)$ gives $-2 + 2i$ and $-2 - 2i$. The output, in natural order, is $(10, -2+2i, -2, -2-2i)$, the DFT of $x$. It took $4$ butterflies, of which only one needed a nontrivial multiplication.

## Where it is used

- **Radix-2 FFTs.** Every stage of the recursive, the iterative and the decimation-in-frequency [FFT](/fast-fourier-transform/) is a layer of butterflies. Higher radices use a small DFT, such as the length-$4$ DFT, as a larger butterfly.
- **Number-theoretic transforms.** The same butterfly with arithmetic modulo $p$, often with [Montgomery](/montgomery-multiplication/) or [Barrett](/barrett-reduction/) reduction, is the step of the [number-theoretic transform](/number-theoretic-transform/).
- **The Walsh-Hadamard transform.** With $w = 1$ everywhere, the stages compute the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/).
- **Hardware and parallel computing.** The pattern of connections between the stages is the butterfly network, the graph of the [parallel FFT circuit](/parallel-fft-circuit/), with depth $\lg n$ and $\frac{n}{2}$ butterflies per level. The same network is used for routing in parallel machines.
- **Fast wavelet and Hartley transforms.** The [fast Hartley transform](/fast-hartley-transform/) uses a butterfly with three inputs, because the Hartley kernel mixes the indices $k$ and $n - k$. The Haar step of the [fast wavelet transform](/fast-wavelet-transform/) is a butterfly with $w = 1$, scaled by $\frac{1}{\sqrt 2}$.

## References
