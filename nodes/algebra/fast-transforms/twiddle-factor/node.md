---
tag: 2GX23C
kind: concept
slug: twiddle-factor
name: Twiddle factor
aliases:
- twiddle factors
- FFT weights
- trigonometric weights
area: algebra/fast-transforms
level: core
summary: The powers of the root of unity multiplied into odd-half values in each FFT butterfly stage.
prereqs: [roots-of-unity, butterfly-operation, fast-fourier-transform]
see_also: [iterative-fft, mixed-radix-fft, split-radix-fft, chinese-remainder-theorem-fft, number-theoretic-transform, bit-reversal-permutation, real-valued-fft, bluestein-fft]
sources:
  - paper: doi:10.1145/1464291.1464352
    title: W. Morven Gentleman and Gordon Sande, Fast Fourier transforms, for fun and profit, AFIPS Fall Joint Computer Conference, 1966
    locator: from p. 563 (the factorization of the DFT of length n1 n2 with the multipliers between the two passes, which they call twiddle factors)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.3 (the radix-2 Cooley-Tukey factorization with its diagonal matrices of weights), and Section 1.4, Weight and Butterfly Computations (ways to compute the weights and their rounding errors)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, Theorem 24.2 (the error bound of the radix-2 FFT, with the term μ for the errors of the computed weights)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Sections 30.2 and 30.3 (the twiddle factor in the recursive FFT and in the butterfly of the iterative FFT)
  - url: https://en.wikipedia.org/wiki/Twiddle_factor
    title: Twiddle factor, Wikipedia
    locator: the lead (the definition, and the remark that Gentleman and Sande apparently coined the term in 1966)
---

A twiddle factor is a power $\omega^k$ of a [root of unity](/roots-of-unity/) that an FFT multiplies into the output of one sub-transform before it combines it with another. In the radix-2 [FFT](/fast-fourier-transform/), the [butterfly](/butterfly-operation/) $(u, v) \mapsto (u + \omega^k v,\ u - \omega^k v)$ uses the twiddle factor $\omega^k$, and a transform of length $n$ uses the $n/2$ values $\omega^0, \ldots, \omega^{n/2 - 1}$. In general, a split of a length $n = n_1 n_2$ into short transforms needs the twiddle factors $\omega_n^{j_2 k_1}$ between the two passes. How they are computed and stored decides much of the accuracy and of the speed of a floating-point FFT.

## In plain words

A fast Fourier transform cuts a long transform into short ones and then glues the results together. The short transforms do not line up by themselves: each one is measured from a different starting point. Before gluing, the program turns each result by a fixed amount, as one turns a dial. These fixed turns are the twiddle factors.

They are known before the data arrives, because they depend only on the length. So a program computes them once, keeps them in a table, and reads them at each step. Two things matter. They must be accurate, because each small error in a table entry is copied into many outputs. And the table must be read in an order that the memory of the machine handles well.

## The idea

**Notation.** As on all pages of fast transforms: the length is $n$, over $\mathbb{C}$ the root is $\omega_n = e^{-2\pi i/n}$, and over a ring $\omega$ is a principal $n$-th root of unity. The DFT is $X_k = \sum_j x_j \omega^{jk}$.

**In the radix-2 FFT.** Split $x$ into its even and odd entries, with DFTs $E$ and $O$ of length $n/2$. Then

$$X_k = E_k + \omega^k O_k, \qquad X_{k + n/2} = E_k - \omega^k O_k, \qquad 0 \le k < n/2.$$

The factor $\omega^k$ is the twiddle factor. It corrects for the fact that the odd entries start one place later: the entry $x_{2m+1}$ gets the weight $\omega^{(2m+1)k} = \omega^k (\omega^2)^{mk}$, and $O_k$ supplies only $(\omega^2)^{mk}$. In the iterative FFT, the stage that builds blocks of length $2h$ uses $\omega_{2h}^k = \omega^{k \cdot n/(2h)}$ for $0 \le k < h$. So one table $W[k] = \omega^k$, $0 \le k < n/2$, serves all stages, read with the stride $n/(2h)$.

**In a general factorization.** Let $n = n_1 n_2$, and write $j = n_2 j_1 + j_2$ and $k = k_1 + n_1 k_2$ with $0 \le j_1, k_1 < n_1$ and $0 \le j_2, k_2 < n_2$. Then $jk = n_2 j_1 k_1 + n j_1 k_2 + j_2 k_1 + n_1 j_2 k_2$, and $\omega_n^{n} = 1$, $\omega_n^{n_2} = \omega_{n_1}$, $\omega_n^{n_1} = \omega_{n_2}$, so

$$X_{k_1 + n_1 k_2} = \sum_{j_2 = 0}^{n_2 - 1} \omega_{n_2}^{j_2 k_2} \Bigl[\ \omega_n^{j_2 k_1} \sum_{j_1 = 0}^{n_1 - 1} x_{n_2 j_1 + j_2}\, \omega_{n_1}^{j_1 k_1} \Bigr].$$

The inner sums are $n_2$ DFTs of length $n_1$, the outer sums are $n_1$ DFTs of length $n_2$, and the $n$ numbers $\omega_n^{j_2 k_1}$ in between are the twiddle factors. This is the [mixed-radix FFT](/mixed-radix-fft/). When $\gcd(n_1, n_2) = 1$, another index map makes all twiddle factors equal to $1$; that is the [prime factor algorithm](/chinese-remainder-theorem-fft/). In matrix terms, the twiddle factors form the diagonal matrix between the two Kronecker factors of the Cooley-Tukey factorization of $F_n$.

**Trivial twiddle factors.** $\omega^0 = 1$ needs no multiplication. Over $\mathbb{C}$, $\omega_n^{n/4} = -i$ only swaps the real and the imaginary part and changes a sign, and $\omega_n^{n/8} = (1 - i)/\sqrt 2$ needs $2$ real multiplications instead of $4$. The radix-2 FFT has $n - 1$ butterflies with the factor $1$, and the [split-radix FFT](/split-radix-fft/) gets its lower count by arranging more butterflies to have trivial factors.

**Computing the table.** These are the common ways, with their accuracy in floating point with unit roundoff $u$.

- *Direct.* $W[k] = \cos(2\pi k/n) - i \sin(2\pi k/n)$ for each $k$. The error of each entry is that of the library functions. Good libraries are accurate to about one unit in the last place; this is a property of the library, not a guarantee of IEEE arithmetic.
- *Symmetry.* Compute only $0 \le k \le n/8$ directly, and get the others exactly: $\omega^{n/4 - k} = -i\,\overline{\omega^k}$, and $\omega^{n/4 + k} = -i\, \omega^k$. This reduces the calls by a factor of $4$ with no loss.
- *Repeated multiplication.* $W[k] = W[k-1] \cdot \hat\omega$. Each step adds a relative error of about $u$, and the error of $\hat\omega$ itself is multiplied by $k$. So the error of $W[k]$ grows linearly in $k$, up to about $nu$. The table below shows the size.
- *Recursions with restarts.* Van Loan (Section 1.4) analyses subvector scaling and logarithmic recursions, which compute $W[k]$ from a few accurate values with errors that grow like $u \log n$ instead of $u n$.

Higham's Theorem 24.2 bounds the relative error of the radix-2 FFT by about $\lg n \cdot (\mu + \gamma_4(\sqrt 2 + \mu))$, where $\mu$ bounds the relative errors of the computed twiddle factors. With $\mu = O(u)$ the bound is $O(u \log n)$. With repeated multiplication, $\mu$ can be as large as $O(nu)$, and the proved bound becomes $O(n u \log n)$. Over $\mathbb{Z}/p\mathbb{Z}$ every method is exact, and repeated multiplication is the usual one.

## Examples

**Length 8 over $\mathbb{C}$.** $W = (\omega_8^0, \omega_8^1, \omega_8^2, \omega_8^3) = \bigl(1,\ \tfrac{1 - i}{\sqrt 2},\ -i,\ \tfrac{-1 - i}{\sqrt 2}\bigr)$. The three stages of the iterative FFT read them as follows.

| stage | block length $2h$ | stride $n/(2h)$ | twiddle factors used |
|---|---|---|---|
| 1 | 2 | 4 | $W[0] = 1$ |
| 2 | 4 | 2 | $W[0] = 1$, $W[2] = -i$ |
| 3 | 8 | 1 | $W[0], W[1], W[2], W[3]$ |

Of the $12$ butterflies, $7 = n - 1$ use the factor $1$, $3$ use $-i$, and only $2$ need a full complex multiplication, by $W[1]$ and $W[3]$, which by the symmetry rule are related by $W[3] = -i\, W[1]$.

**Length 8 over $\mathbb{Z}/17\mathbb{Z}$.** With $\omega = 2$, a principal $8$-th root since $2^4 = 16 \equiv -1$, the table is $W = (1, 2, 4, 8)$. Here $W[2] = 4$ plays the role of $-i$: $4^2 = 16 \equiv -1$.

**Length 6 with $n_1 = 2$, $n_2 = 3$.** The twiddle factors are $\omega_6^{j_2 k_1}$ for $j_2 \in \{0, 1, 2\}$ and $k_1 \in \{0, 1\}$: the values $1, 1, 1$ for $k_1 = 0$, and $1, \omega_6, \omega_6^2$ for $k_1 = 1$, with $\omega_6 = \tfrac12 - \tfrac{\sqrt 3}{2} i$. So only $2$ of the $6$ are nontrivial.

**Error of repeated multiplication.** Computing $W[k]$ for $0 \le k < n/2$ in IEEE double precision by $W[k] = W[k-1] \cdot \hat\omega_n$ gives these largest errors $\max_k |W[k] - \omega_n^k|$, measured against the direct values:

| $n$ | largest error | in units of $u = 2^{-53}$ |
|---|---|---|
| $2^{10}$ | $1.8 \times 10^{-14}$ | about 164 |
| $2^{16}$ | $6.8 \times 10^{-13}$ | about 6100 |
| $2^{20}$ | $2.3 \times 10^{-11}$ | about 210000 |

These are measurements of one run, not bounds. They grow roughly in proportion to $n$, as the analysis above predicts, while the direct method stays at a few $u$ for every $n$.

## Where it is used

- **Every Cooley-Tukey FFT.** The [radix-2 FFT](/fast-fourier-transform/), the [iterative FFT](/iterative-fft/), the [mixed-radix FFT](/mixed-radix-fft/) and the [split-radix FFT](/split-radix-fft/) all multiply by twiddle factors between their passes. The [inverse FFT](/inverse-fft/) uses the conjugates, or the inverse powers over a ring.
- **Exact transforms.** The [number-theoretic transform](/number-theoretic-transform/) stores the powers of its root modulo $p$, and the [Schönhage-Strassen algorithm](/schonhage-strassen-multiplication/) uses powers of $2$, which are shifts.
- **Real-input transforms.** The [real-valued FFT](/real-valued-fft/) uses one more set of twiddle factors to split a half-length complex transform into the spectrum of a real input.
- **Bluestein's algorithm.** The chirp $\omega^{k^2/2}$ of [Bluestein's algorithm](/bluestein-fft/) is a twiddle factor of another kind, and its accuracy has the same issues.
- **Algorithms without them.** The [prime factor algorithm](/chinese-remainder-theorem-fft/) and the [Walsh-Hadamard transform](/fast-walsh-hadamard-transform/) need no nontrivial twiddle factors.

## References
