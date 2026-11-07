---
tag: 14CJHC
kind: algorithm
slug: fast-fourier-transform
name: Fast Fourier transform
aliases:
- FFT
- radix-2 Cooley-Tukey FFT
- Cooley-Tukey algorithm
- radix-2 FFT
area: algebra/fast-transforms
level: core
summary: Divide-and-conquer DFT in O(n log n) when n is a power of two (recursive or iterative).
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (a power of two)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  multiplications: {worst: (n/2) lg n}
  additions: {worst: n lg n}
properties: {deterministic: true, recursive: false, in_place: true}
history:
  year: 1965
  people: [James W. Cooley, John W. Tukey]
  note: Cooley and Tukey published the method in 1965. Gauss had used the same splitting about 1805, in work published in 1866.
prereqs: [discrete-fourier-transform, butterfly-operation, bit-reversal-permutation, fft-halving-lemma, divide-and-conquer-paradigm]
see_also: [inverse-fft, iterative-fft, split-radix-fft, mixed-radix-fft, number-theoretic-transform, convolution-via-fft, bluestein-fft, fft-polynomial-multiplication]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2, The DFT and FFT (the recursive FFT), and Section 30.3, Efficient FFT implementations (the iterative FFT with bit reversal)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2, The Discrete Fourier Transform and the Fast Fourier Transform (the FFT over a commutative ring with a primitive root of unity, and its operation count)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Sections 1.2 to 1.5 and 1.9 (the FFT idea, the Cooley-Tukey factorization, butterflies, bit reversal, and decimation in frequency)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, The Fast Fourier Transform and Applications, Theorem 24.2 (the normwise error bound of the radix-2 FFT)
  - paper: doi:10.1090/S0025-5718-1965-0178586-1
    title: James W. Cooley and John W. Tukey, An algorithm for the machine calculation of complex Fourier series, Mathematics of Computation 19(90), 1965
    locator: pp. 297 to 301
  - paper: doi:10.1109/MASSP.1984.1162257
    title: Michael T. Heideman, Don H. Johnson and C. Sidney Burrus, Gauss and the history of the fast Fourier transform, IEEE ASSP Magazine 1(4), 1984
    locator: pp. 14 to 21 (Gauss's treatise of about 1805, published in 1866, and the later rediscoveries)
  - paper: doi:10.1145/321752.321761
    title: Jacques Morgenstern, Note on a lower bound on the linear complexity of the fast Fourier transform, Journal of the ACM 20(2), 1973
    locator: pp. 305 to 306
  - paper: doi:10.1109/TSP.2006.882087
    title: Steven G. Johnson and Matteo Frigo, A modified split-radix FFT with fewer arithmetic operations, IEEE Transactions on Signal Processing 55(1), 2007
    locator: pp. 111 to 119
---

The fast Fourier transform (FFT) computes the [discrete Fourier transform](/discrete-fourier-transform/) of length $n$ in $\Theta(n \log n)$ operations instead of the $\Theta(n^2)$ of the direct sum. This page gives the radix-2 method of Cooley and Tukey, for $n$ a power of two. It splits the input into its even and odd entries, transforms each half, and combines the two halves with $n/2$ [butterflies](/butterfly-operation/), using exactly $\frac{n}{2} \lg n$ multiplications and $n \lg n$ additions. The version below is the iterative, in-place form: it puts the input in [bit-reversed order](/bit-reversal-permutation/) and then runs $\lg n$ stages of butterflies, with no recursion. It works over $\mathbb{C}$ and over each commutative ring with a principal $n$-th root of unity, where it is the [number-theoretic transform](/number-theoretic-transform/).

## In plain words

The Fourier transform of a list of numbers measures how much of each regular wave the list contains. Done directly, every output looks at every input, which is slow.

The fast method notices that the work for a long list is mostly the same work as for two lists of half the length: one made of the entries at even places and one made of the entries at odd places. It solves the two half problems and then joins them with a cheap step that adds and subtracts pairs of numbers. Each half is split again, down to lists of one number. There are only as many levels of splitting as the number of times the length can be halved, and each level costs about one step per entry. In practice the program first reorders the list and then joins pairs, then fours, then eights, in one array.

## The problem

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $n$ is the transform length, and here it must be a power of two, $n = 2^t$. Over $\mathbb{C}$, $\omega = \omega_n = e^{-2\pi i/n}$, the sign convention of signal processing, FFTW and NumPy; CLRS uses $e^{+2\pi i/n}$, and everything on this page holds for both. In a commutative ring $R$, $\omega$ is a principal $n$-th root of unity: $\omega^n = 1$ and $\sum_{j=0}^{n-1} \omega^{jk} = 0$ for $1 \le k \le n-1$.

**Input.** $x = (x_0, \ldots, x_{n-1}) \in R^n$ with $n = 2^t$, and $\omega$ as above.

**Output.** $X = F_n x$ with $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$ for $0 \le k \le n-1$. The inverse is $x_j = \frac{1}{n} \sum_{k} X_k \omega^{-jk}$, which needs $n$ to be a unit of $R$. The forward algorithm itself uses only $\omega^{n/2} = -1$ (for $n \ge 2$). A principal $n$-th root has this property when $n$ is a unit, by the [cancellation lemma](/fft-cancellation-lemma/), and so does $\omega_n$ over $\mathbb{C}$.

**Cost model.** Costs are counted as operations of $R$: additions (including subtractions) and multiplications, counted separately, as is usual in the FFT literature. Over $\mathbb{C}$ in the real RAM, each complex operation is a fixed number of real operations. Over $\mathbb{Z}/p\mathbb{Z}$ with $p$ below the word size, each ring operation is $O(1)$ time on the [word RAM](/word-ram/). Index computations, such as the bit reversal, are not ring operations and are counted apart.

## The algorithm

**The idea.** Split the sum by the parity of $j$. With $E = F_{n/2}(x_0, x_2, \ldots, x_{n-2})$ and $O = F_{n/2}(x_1, x_3, \ldots, x_{n-1})$, both taken with the root $\omega^2$, which is a principal $(n/2)$-th root by the [cancellation lemma](/fft-cancellation-lemma/),

$$X_k = E_k + \omega^k O_k, \qquad X_{k + n/2} = E_k - \omega^k O_k, \qquad 0 \le k < n/2,$$

since $\omega^{n/2} = -1$. The [halving lemma](/fft-halving-lemma/) is the statement behind this: the $n$ points $\omega^k$ square to only $n/2$ points. The recursive FFT applies this split until the length is $1$, where $F_1 x = x$. Unrolling the recursion, the leaf in position $p$ holds $x_{\mathrm{rev}_t(p)}$, so the iterative form permutes once and then combines blocks of length $2, 4, \ldots, n$ from the bottom up.

```pseudo id=main
FFT(x, ω)               ▷ x[0 .. n − 1] with n = 2^t; ω a principal n-th root of unity
L1  n ← |x|, t ← lg n
L2  W[k] ← ω^k for k = 0, …, n/2 − 1             ▷ the twiddle factors
L3  for j ← 0 to n − 1 do                          ▷ bit-reversal permutation
L4      if j < rev_t(j) then swap x[j] and x[rev_t(j)]
L5  h ← 1                                          ▷ half the block length
L6  while h < n do
L7      for s ← 0 to n − 1 step 2h do              ▷ the block x[s .. s + 2h − 1]
L8          for k ← 0 to h − 1 do
L9              u ← x[s + k]
L10             v ← W[k · n/(2h)] · x[s + k + h]   ▷ W[k · n/(2h)] = (ω^(n/(2h)))^k
L11             x[s + k] ← u + v
L12             x[s + k + h] ← u − v
L13     h ← 2h

INVERSE-FFT(X, ω)       ▷ n must be a unit of R
L14 FFT(X, ω^(−1))
L15 for j ← 0 to n − 1 do X[j] ← X[j] / n
```

The stage with half length $h$ treats each block of length $2h$ as the output of two transforms of length $h$, side by side, and combines them with $h$ butterflies. Its root is $\omega^{n/(2h)}$, a principal $(2h)$-th root of unity, and its twiddle factors are read from the one table $W$ with stride $n/(2h)$. Lines L9 to L12 are one butterfly. The value $u$ is saved before line L11 overwrites $x[s + k]$, and both outputs go back into the two cells that were read, so the transform runs in place. INVERSE-FFT is the same algorithm with $\omega^{-1}$, which is also a principal $n$-th root, followed by the scaling.

## Example

Over $\mathbb{Z}/17\mathbb{Z}$ with $n = 8$ and $\omega = 2$ (order $8$, since $2^4 = 16 \equiv -1$), transform $x = (1, 2, 3, 4, 5, 6, 7, 8)$. The table is $W = (1, 2, 4, 8)$, and $\mathrm{rev}_3 = (0, 4, 2, 6, 1, 5, 3, 7)$. All values are reduced modulo $17$.

| step | twiddles used | the array |
|---|---|---|
| input | | 1 2 3 4 5 6 7 8 |
| L3 to L4, bit reversal | | 1 5 3 7 2 6 4 8 |
| stage h = 1 | 1 | 6 13 10 13 8 13 12 13 |
| stage h = 2 | 1, 4 | 16 14 13 12 3 14 13 12 |
| stage h = 4 | 1, 2, 4, 8 | 2 8 14 6 13 3 12 1 |

In stage $h = 1$, the pair $(1, 5)$ becomes $(1 + 5, 1 - 5) = (6, -4) = (6, 13)$. In stage $h = 4$, the first butterfly gives $X_0 = 16 + 1 \cdot 3 = 19 \equiv 2$, which is $1 + 2 + \cdots + 8 = 36 \equiv 2$, as it must be. The output equals the direct sum $X_k = \sum_j x_j 2^{jk} \bmod 17$ for each $k$, and INVERSE-FFT with $\omega^{-1} = 9$ and $8^{-1} = 15$ gives back $x$. Over $\mathbb{C}$, the same steps with $n = 4$ give $F_4 (1, 2, 3, 4) = (10, -2+2i, -2, -2-2i)$; the trace is on the [butterfly](/butterfly-operation/) page.

## Correctness

Write $x$ for the input and $h = 2^q$. The invariant of the loop of line L6 is: when line L6 tests $h$, each block $x[s \ldots s + h - 1]$ with $h \mid s$ holds the DFT of length $h$, with the root $\omega^{n/h}$, of the subsequence $(x_{c}, x_{c + n/h}, x_{c + 2n/h}, \ldots)$ of $h$ entries, where $c = \mathrm{rev}_{t-q}(s/h)$. For $h = 1$ this says $x[s] = x_{\mathrm{rev}_t(s)}$, which is what lines L3 and L4 do. Two neighbouring blocks of length $h$ hold the DFTs of the even-indexed and the odd-indexed entries of one subsequence of length $2h$, and lines L9 to L12 apply the split formula for length $2h$ with the root $\omega^{n/(2h)}$, whose $h$-th power is $\omega^{n/2} = -1$. So the invariant holds for $2h$. When $h = n$, $c = 0$ and the array is $F_n x$. The [inverse](/inverse-discrete-fourier-transform/) is correct because $\omega^{-1}$ is also a principal $n$-th root and $F_n(\omega^{-1}) F_n(\omega) = nI$ by the [summation lemma](/fft-summation-lemma/). The full proof is below.

## Complexity

**Ring operations.** Stage $h$ has $n/(2h)$ blocks with $h$ butterflies each, so $n/2$ butterflies, and there are $t = \lg n$ stages. Each butterfly does one multiplication and two additions. So FFT uses

$$\tfrac{n}{2} \lg n \ \text{multiplications} \quad \text{and} \quad n \lg n \ \text{additions in } R,$$

plus at most $n/2 - 2$ multiplications to fill the table $W$ (none if it is precomputed). This is exact, with no lower-order terms, when every twiddle factor is counted as a multiplication. The butterflies with $W[0] = 1$ need no multiplication, and there are $n - 1$ of them, so a careful count is $\frac{n}{2} \lg n - n + 1$ nontrivial multiplications. INVERSE-FFT adds $n$ multiplications by $n^{-1}$. The same counts follow from the recurrence $T(n) = 2T(n/2) + \frac{n}{2}$ multiplications and $n$ additions, $T(1) = 0$, of the recursive form.

**Real operations.** Over $\mathbb{C}$, a complex multiplication costs $4$ real multiplications and $2$ real additions, and a complex addition costs $2$ real additions. So the radix-2 FFT costs about $5 n \lg n$ real operations, $2 n \lg n$ multiplications and $3 n \lg n$ additions. Removing the trivial twiddles $1$ and $-i$ and using larger radices lowers this. The [split-radix FFT](/split-radix-fft/) uses $4 n \lg n - 6n + 8$ real operations for $n \ge 2$, and the modified split radix of Johnson and Frigo uses $\frac{34}{9} n \lg n + O(n)$, the lowest count known for power-of-two $n$.

**Time and space.** The bit reversal takes $O(n)$ index operations with the recurrence of the [bit-reversal page](/bit-reversal-permutation/). The time is $\Theta(n \log n)$ in each case, since the operation sequence does not depend on the data. The array is transformed in place; the twiddle table and the table of reversed indices take $\Theta(n)$ extra space, and both can be removed at some cost in time.

**Lower bounds.** Morgenstern (1973) proved that each linear algorithm for $F_n$ over $\mathbb{C}$ whose constants have modulus at most $1$ needs $\Omega(n \log n)$ linear steps. The proof uses $|\det F_n| = n^{n/2}$ and the fact that one such step, which adds two earlier values with bounded coefficients, can at most double the absolute value of a suitable determinant, so at least $\frac{n}{2} \lg n$ steps are needed. Without the bound on the constants, no lower bound better than $\Omega(n)$ is known for arithmetic circuits. So the FFT is optimal up to a constant factor in Morgenstern's model, and the exact constant is open.

**Rounding errors (proved).** Let the FFT run in floating point with unit roundoff $u$, and let the computed twiddle factors have relative errors at most $\mu$. Higham, Theorem 24.2, proves that the computed $\hat X$ satisfies

$$\frac{\lVert \hat X - X \rVert_2}{\lVert X \rVert_2} \le \frac{\lg n \cdot \eta}{1 - \lg n \cdot \eta}, \qquad \eta = \mu + \gamma_4 (\sqrt 2 + \mu), \quad \gamma_4 = \frac{4u}{1 - 4u}.$$

With accurate twiddle factors, $\mu = O(u)$ and the bound is $O(u \log n)$, far better than the error bounds for evaluating the direct sum, which grow like a power of $n$. *Observed in practice:* for random inputs the root-mean-square relative error grows like $u \sqrt{\lg n}$, as statistical models predict; this is an observation, not a worst-case bound.

## Properties

- **Exact over rings.** Over $\mathbb{Z}/p\mathbb{Z}$ and other rings the algorithm uses only ring operations, so the result is exact.
- **In place.** The butterflies overwrite their inputs; only $O(1)$ ring elements are needed besides the array and the tables.
- **Oblivious.** The sequence of operations depends only on $n$, not on the data, so the FFT is also an arithmetic circuit of depth $O(\log n)$: the [parallel FFT circuit](/parallel-fft-circuit/).
- **Linear.** $F_n(\alpha x + \beta y) = \alpha F_n x + \beta F_n y$, and the computed result over a ring obeys the same law.
- **Stable in floating point.** The proved error bound grows with $\lg n$, not with $n$.
- **Needs a power-of-two length.** Other lengths need padding, which changes the transform, or another method (below).

## Variants and improvements

- **The recursive form.** Split into even and odd entries, recurse, combine. It is the form in which the method is usually first explained (CLRS, Section 30.2), and it is cache-oblivious, but it uses $\Theta(n)$ extra space for copies and a recursion of depth $\lg n$.
- **Decimation in frequency (Gentleman and Sande).** Split the *outputs* into even and odd $k$ instead. It reads natural order and writes bit-reversed order, with the butterfly $(x, y) \mapsto (x + y, (x - y) w)$.
- **The Stockham form.** Uses a second array and avoids the bit reversal; good on vector machines.
- **Radix 4, split radix, modified split radix.** Fewer real operations by combining stages: split radix (Yavne 1968, Duhamel and Hollmann 1984) and its modification by Johnson and Frigo (2007). See the [split-radix FFT](/split-radix-fft/).
- **Other lengths.** The [mixed-radix FFT](/mixed-radix-fft/) handles each composite $n = n_1 n_2$, as in the paper of Cooley and Tukey. The prime factor algorithm of Good (1958) and Thomas (1963), the [Chinese remainder theorem FFT](/chinese-remainder-theorem-fft/), needs no twiddle factors when $\gcd(n_1, n_2) = 1$. [Rader's algorithm](/rader-fft/) (1968) and [Bluestein's algorithm](/bluestein-fft/) (1970) handle prime lengths in $O(n \log n)$.
- **Real input.** A [real-valued FFT](/real-valued-fft/) of length $n$ costs about half of a complex one.
- **Exact arithmetic.** The [number-theoretic transform](/number-theoretic-transform/) is this algorithm over $\mathbb{Z}/p\mathbb{Z}$, for example with $p = 998244353 = 119 \cdot 2^{23} + 1$ and $\omega = 3^{(p-1)/n}$.
- **Libraries.** FFTW chooses among many of these variants at run time by measuring them on the machine.

## When to use it

Use the FFT for each DFT of length more than a few dozen, and for the operations that reduce to it: [convolution](/convolution-via-fft/), [polynomial multiplication](/fft-polynomial-multiplication/), large [integer multiplication](/integer-multiplication/), correlation, spectral analysis and filtering. Use it over $\mathbb{Z}/p\mathbb{Z}$ when the result must be exact. For a few output frequencies, the [Goertzel algorithm](/goertzel-algorithm/) or direct sums cost $O(n)$ each and are cheaper. For very short lengths, a direct or hand-written small DFT is faster. For lengths that are not powers of two, pad only if the application allows it (convolution does, a spectrum at given frequencies does not); otherwise use a mixed-radix or Bluestein FFT.

## Pitfalls

- **Twiddle factors by repeated multiplication.** Computing $\omega^k$ as $\omega \cdot \omega \cdots$ in floating point gives errors that grow with $k$, and $\mu$ in the error bound grows to $O(u n)$ in the worst case. Compute each twiddle factor directly as $\cos$ and $\sin$ of $2\pi k/n$, or by a stable recurrence. Over $\mathbb{Z}/p\mathbb{Z}$, repeated multiplication is exact and fine.
- **The sign convention.** NumPy and FFTW use $e^{-2\pi i/n}$ in the forward transform, and CLRS uses $e^{+2\pi i/n}$. Mixing them conjugates and reverses the output: $X_k$ becomes $X_{n-k}$ for real input.
- **The scaling.** The factor $1/n$ belongs to the inverse in this convention, but some texts put $1/\sqrt n$ on both directions. A round trip that returns $n x$ is missing it.
- **A root that is not principal.** Over $\mathbb{Z}/p\mathbb{Z}$ the root must have order exactly $n$, so $n$ must divide $p - 1$. For example $3$ is a primitive root modulo $998244353$ and modulo $17$, but not modulo $97$, where $3^{48} \equiv 1$; there $5$ is a primitive root. A wrong root gives wrong output with no error.
- **Overflow modulo p.** The product in line L10 needs twice the width of $p$; reduce after every operation.
- **The wrong stride.** The twiddle factor of stage $h$ is $W[k \cdot n/(2h)]$, not $W[k]$; using $W[k]$ is correct only in the last stage.

## Implementations

## History

Gauss found the method about 1805, while interpolating the orbits of asteroids from observations, and split a transform of length $n_1 n_2$ into transforms of lengths $n_1$ and $n_2$. His treatise was published only in 1866, in Latin, in his collected works, and it remained little known; Heideman, Johnson and Burrus traced the history in 1984. Variants were found again several times, for example by Runge (1903 and 1905) and by Danielson and Lanczos (1942). Cooley and Tukey published the general method for composite $n$ in 1965, with the case $n = 2^t$ in the form used today, and their paper started its wide use in computing. Good (1958) had already given the prime factor algorithm, and Thomas (1963) found it independently. Rader (1968) and Bluestein (1970) gave methods for prime lengths. Yavne (1968) and Duhamel and Hollmann (1984) gave the split-radix algorithm, and Johnson and Frigo (2007) lowered its operation count to $\frac{34}{9} n \lg n + O(n)$. Morgenstern (1973) proved the $\Omega(n \log n)$ lower bound for algorithms with bounded constants.

## References
