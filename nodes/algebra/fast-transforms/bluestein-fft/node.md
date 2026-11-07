---
tag: GDR6AH
kind: algorithm
slug: bluestein-fft
name: Bluestein's algorithm
aliases:
- chirp z-transform
- Bluestein FFT
- chirp-z FFT
- Bluestein's FFT algorithm
area: algebra/fast-transforms
level: advanced
summary: Computes a DFT of arbitrary length n as a convolution with a chirp, using power-of-two FFTs.
solves: [discrete-fourier-transform]
model: real-ram
complexity:
  vars: {n: the transform length (any positive integer), M: the convolution length (the least power of two with M at least 2n - 1)}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
  multiplications: {worst: (3/2) M lg M + 2M + 2n}
  additions: {worst: 3 M lg M}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1970
  people: [Leo I. Bluestein]
  note: Bluestein wrote the DFT as a convolution with a chirp, first at a 1968 meeting and in a journal in 1970; Rabiner, Schafer and Rader built the chirp z-transform on the same identity in 1969.
prereqs: [discrete-fourier-transform, convolution-via-fft, fast-fourier-transform]
see_also: [rader-fft, chinese-remainder-theorem-fft, mixed-radix-fft, number-theoretic-transform, convolution-theorem, roots-of-unity, nonuniform-fft, goertzel-algorithm]
sources:
  - paper: doi:10.1109/TAU.1970.1162132
    title: Leo I. Bluestein, A linear filtering approach to the computation of discrete Fourier transform, IEEE Transactions on Audio and Electroacoustics 18(4), 1970
    locator: pp. 451 to 455 (the identity 2jk = j^2 + k^2 - (k - j)^2 and the DFT as a chirp filter)
  - paper: doi:10.1109/TAU.1969.1162034
    title: Lawrence R. Rabiner, Ronald W. Schafer and Charles M. Rader, The chirp z-transform algorithm, IEEE Transactions on Audio and Electroacoustics 17(2), 1969
    locator: pp. 86 to 92 (the z-transform on a spiral contour computed by one convolution with FFTs)
  - paper: doi:10.1109/PROC.1968.6477
    title: Charles M. Rader, Discrete Fourier transforms when the number of data samples is prime, Proceedings of the IEEE 56(6), 1968
    locator: pp. 1107 to 1108 (the other reduction of a prime-length DFT to a cyclic convolution)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 22, Section 22.6, The z-transform (ZT), and Section 22.7, Prime length FFTs
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 24, Theorem 24.2 (the error bound of the radix-2 FFT, used for the three inner FFTs), and Section 3.6 (complex multiplication)
---

Bluestein's algorithm computes the [discrete Fourier transform](/discrete-fourier-transform/) of any length $n$, prime or not, in $\Theta(n \log n)$ operations. It rests on the identity $2jk = j^2 + k^2 - (k - j)^2$, which turns the DFT sum into a [convolution](/convolution/) with a *chirp*, the sequence $c_m = \zeta^{m^2}$ whose phase grows like $m^2$. That convolution has length about $2n$, so it can be padded to a power of two $M \ge 2n - 1$ and computed with three [radix-2 FFTs](/fast-fourier-transform/) by the [convolution theorem](/convolution-theorem/). The cost is a constant factor more than an FFT of a power-of-two length, and it works for every $n$, which makes it a common fallback for prime lengths and large prime factors. Bluestein published it in 1970. The same identity gives the *chirp z-transform* of Rabiner, Schafer and Rader, which evaluates the z-transform on a spiral of points.

## In plain words

Fast Fourier methods are fastest when the length splits into small factors, and a prime length does not split at all. Bluestein's trick avoids splitting. A little algebra rewrites each output as a sliding weighted sum: multiply the input by a fixed wave whose frequency rises steadily, slide another such wave across it, and multiply by the first wave again.

Sliding sums of this kind are exactly what a fast transform computes well, and the length of the sliding sum may be padded with zeros to any convenient size. So the method pads to a power of two, does three fast transforms of that size, and recovers the answer for the awkward length. The price is several times the work of one fast transform of the original length.

## The problem

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $n$ is the transform length, here any positive integer; $\omega_n = e^{-2\pi i/n}$, with the minus sign of signal processing; the DFT is $X_k = \sum_{j=0}^{n-1} x_j \omega_n^{jk}$, and its inverse is $x_j = \frac{1}{n} \sum_k X_k \omega_n^{-jk}$. Over a commutative ring $R$, $\omega$ is a principal $n$-th root of unity. The algorithm also needs a square root $\zeta$ of $\omega$ with $\zeta^{2n} = 1$: over $\mathbb{C}$, $\zeta = e^{-\pi i/n}$. $M$ is the least power of two with $M \ge 2n - 1$, and the inner FFTs need a principal $M$-th root of unity and $M$ to be a unit in $R$.

**Input.** A vector $x$ of length $n \ge 1$. **Output.** Its DFT $X$; the inverse returns $x$ from $X$.

**Cost model.** Operations of $R$, with additions and multiplications counted separately, as on the [FFT page](/fast-fourier-transform/): over $\mathbb{C}$ in the real RAM each complex operation is a fixed number of real ones, and over $\mathbb{Z}/p\mathbb{Z}$ each is $O(1)$ on the word RAM. The chirp values and the twiddle factors are counted apart, like a table, and copies are free. In floating point, the error is analysed below.

## The algorithm

Writing $\omega^{jk} = \zeta^{2jk} = \zeta^{j^2} \zeta^{k^2} \zeta^{-(k-j)^2}$ and $c_m = \zeta^{m^2}$,

$$X_k = c_k \sum_{j=0}^{n-1} (x_j c_j) \, c_{k-j}^{-1}, \qquad 0 \le k < n,$$

a convolution of $a_j = x_j c_j$ with $b_m = c_m^{-1}$, $-n < m < n$, multiplied by the chirp once more. Since $c_{-m} = c_m$, storing $b_m$ at position $m \bmod M$ gives a cyclic vector of length $M$.

```pseudo id=main
BLUESTEIN(x, ζ)            ▷ x[0 .. n − 1] over R; ζ² = ω_n and ζ^(2n) = 1; over ℂ, ζ = e^(−πi/n)
L1  n ← |x|; M ← the least power of two with M ≥ 2n − 1
L2  for m ← 0 to n − 1 do c[m] ← ζ^(m² mod 2n)                         ▷ the chirp
L3  a[0 .. M − 1] ← 0; for j ← 0 to n − 1 do a[j] ← x[j] · c[j]
L4  b[0 .. M − 1] ← 0; for m ← 0 to n − 1 do b[m] ← c[m]⁻¹; b[(M − m) mod M] ← c[m]⁻¹
L5  A ← FFT_M(a); B ← FFT_M(b)
L6  for r ← 0 to M − 1 do A[r] ← A[r] · B[r]
L7  z ← INVERSE-FFT_M(A)                                               ▷ z = a ⊛ b, cyclic of length M
L8  for k ← 0 to n − 1 do X[k] ← c[k] · z[k]
L9  return X

INVERSE-BLUESTEIN(X, ζ)
L10 y ← BLUESTEIN(X, ζ⁻¹)
L11 return y / n
```

Over $\mathbb{C}$, $c[m]^{-1}$ is the complex conjugate of $c[m]$, which is exact. Line L2 reduces $m^2$ modulo $2n$ before forming the power, which is exact since $\zeta^{2n} = 1$ and keeps the angle small in floating point. The vector $B$ depends only on $n$, so it can be computed once for many transforms of the same length.

## Example

Take $n = 3$ over $\mathbb{Z}/97\mathbb{Z}$ with the primitive root $5$, and $x = (1, 2, 3)$. Then $\zeta = 5^{96/6} = 36$, which has order $6$, and $\omega = \zeta^2 = 35$, which has order $3$. Since $2n - 1 = 5$, $M = 8$, and the inner FFTs use the root $5^{96/8} = 64$ of order $8$.

| step | values |
|---|---|
| L2, chirp $c_m = \zeta^{m^2 \bmod 6}$ | $c = (1, 36, 61)$, and $c^{-1} = (1, 62, 35)$ |
| L3, $a_j = x_j c_j$ | $a = (1, 72, 86, 0, 0, 0, 0, 0)$ |
| L4, chirp inverse at $\pm m$ | $b = (1, 62, 35, 0, 0, 0, 35, 62)$ |
| L5 to L7, $z = a \circledast b$ | $z = (6, 34, 26, 92, 3, 0, 35, 60)$ |
| L8, $X_k = c_k z_k$ for $k < 3$ | $X = (6, 60, 34)$ |

For instance $z_1 = a_0 b_1 + a_1 b_0 + a_2 b_7 = 62 + 72 + 86 \cdot 62 \equiv 62 + 72 + 94 \equiv 34$, and $X_1 = 36 \cdot 34 \equiv 60$. The direct sums agree: $X_0 = 6$, $X_1 = 1 + 2 \cdot 35 + 3 \cdot 35^2 \equiv 60$, $X_2 = 1 + 2 \cdot 35^2 + 3 \cdot 35^4 \equiv 34$. Only $z_0, z_1, z_2$ are used; the other entries of $z$ are by-products of the padding. Over $\mathbb{C}$ the same steps with $\zeta = e^{-\pi i/3}$ give $X = (6, -1.5 + 0.866i, -1.5 - 0.866i)$. Both were checked by script.

## Correctness

For $0 \le j, k < n$ the difference $d = k - j$ lies in $(-n, n)$. Line L4 stores $c_{|d|}^{-1}$ at $d \bmod M$: at $d$ itself when $d \ge 0$ and at $M - |d|$ when $d < 0$. These $2n - 1$ positions are distinct because $M - (n - 1) \ge n$, and every other position is $0$. So the cyclic convolution of line L7, restricted to $k < n$, is $z_k = \sum_{j<n} x_j c_j c_{k-j}^{-1}$, with no wrap-around terms, since $a_j = 0$ for $j \ge n$. Then $c_k z_k = \sum_j x_j \zeta^{k^2 + j^2 - (k-j)^2} = \sum_j x_j \zeta^{2jk} = \sum_j x_j \omega^{jk} = X_k$. Lines L5 to L7 compute the cyclic convolution exactly by the convolution theorem, given a principal $M$-th root and $M$ a unit. For the inverse, $\zeta^{-1}$ meets the same conditions with $\omega^{-1}$ in place of $\omega$, so line L10 computes $\sum_k X_k \omega^{-jk} = n x_j$. The full proof is below.

## Complexity

**Operation count.** Lines L3 and L8 do $n$ multiplications each, and line L6 does $M$. Each FFT of length $M$ does $\frac{M}{2} \lg M$ multiplications and $M \lg M$ additions, and the inverse FFT does $M$ more multiplications by $M^{-1}$. In total, BLUESTEIN uses

$$\tfrac{3}{2} M \lg M + 2M + 2n \text{ multiplications} \quad\text{and}\quad 3 M \lg M \text{ additions}.$$

If $B$ is precomputed and the factor $M^{-1}$ is folded into it, this drops to $M \lg M + M + 2n$ multiplications and $2 M \lg M$ additions. Since $2n - 1 \le M < 4n - 2$ for $n \ge 2$, the cost is $\Theta(n \log n)$, roughly $6$ to $12$ times the count of a radix-2 FFT of length $n$, if $n$ were a power of two, or $4$ to $8$ times with the precomputed kernel. Over $\mathbb{C}$, with $4$ real multiplications and $2$ real additions per complex multiplication, this is about $15 M \lg M$ real operations without precomputation.

**Time and space.** $\Theta(n \log n)$ in every case, since the operations do not depend on the data. The arrays $a$, $b$ and the chirp take $\Theta(M) = \Theta(n)$ extra space.

**Rounding errors (proved to first order).** Over $\mathbb{C}$ in floating point with unit roundoff $u$, let each computed chirp value have absolute error at most $\mu$, let $\gamma_2 = 2u/(1 - 2u)$, and let each FFT of length $M$ have the relative error $\varepsilon_M = \lg M \cdot \eta + O(u^2)$ of Higham's Theorem 24.2, with $\eta$ as on the [FFT page](/fast-fourier-transform/). Then

$$\lVert \hat X - X \rVert_2 \le (2n - 1)\left(2\mu + 2\sqrt 2 \, \gamma_2 + (2 + \sqrt 2) \, \varepsilon_M\right) \lVert x \rVert_2 + (\mu + \sqrt 2 \, \gamma_2) \lVert X \rVert_2 + O(u^2).$$

Since $\lVert X \rVert_2 = \sqrt n \lVert x \rVert_2$, the relative error is at most $2\sqrt n \, (2\mu + 2\sqrt 2 \gamma_2 + (2 + \sqrt 2)\varepsilon_M) + \mu + \sqrt 2 \gamma_2$, which is $O(\sqrt n \log n \cdot u)$. The factor $\sqrt n$ comes from the crude bound $\lVert B \rVert_\infty \le 2n - 1$. The largest $|B_r|$ observed was about $2.1 \sqrt n$ for $n$ up to $4093$, which would reduce the bound to $O(\log n \cdot u)$, and the observed relative errors on random data were about $10^{-15}$ for $n$ up to $1000$; these two statements are observed, not proved.

## Properties

- **Any length.** Works for every $n \ge 1$, including primes, with only power-of-two FFTs inside.
- **Exact in a ring.** Over $\mathbb{Z}/p\mathbb{Z}$ it is exact when $2n \mid p - 1$ and $M \mid p - 1$, so that $\zeta$ and the $M$-th root exist.
- **Linear.** The map from $x$ to the computed $X$ is linear, as each step is.
- **Not in place.** It needs arrays of length $M$, about $2n$ to $4n$.

## Variants and improvements

- **Precomputed kernel.** For many transforms of one length, store $B / M$; each transform then costs two FFTs of length $M$ and $O(n)$ further work.
- **Chirp z-transform.** The same identity evaluates $\sum_j x_j A^{-j} W^{jk}$ at $K$ points $z_k = A W^{-k}$ of a spiral, for any complex $A$ and $W$, in $O((n + K) \log (n + K))$ time (Rabiner, Schafer and Rader, 1969). This gives zoomed spectra and DFTs at arbitrary frequency spacing.
- **A slightly shorter convolution.** Because the chirp is even, $c_{-m} = c_m$, the length $M = 2n - 2$ already works: the only two positions that then coincide, $\pm(n - 1)$, receive the same value. Shorter lengths fail in general. This saves a factor of $2$ in $M$ when $2n - 2$ is a power of two, for example $n = 17$ with $M = 32$ instead of $64$. Checked by script for $n \le 13$.
- **Any fast length for $M$.** $M$ need not be a power of two; any length $\ge 2n - 1$ with a fast FFT, such as a product of small primes, will do.
- **Odd $n$ without a $2n$-th root.** For odd $n$, $\zeta = \omega^{(n+1)/2}$ satisfies $\zeta^2 = \omega$ and $\zeta^{2n} = 1$, so over $\mathbb{Z}/p\mathbb{Z}$ only $n \mid p - 1$ is needed for the chirp. Alternatively, $jk = \binom{j+k}{2} - \binom{j}{2} - \binom{k}{2}$ writes the DFT as a correlation with $\omega^{\binom{m}{2}}$, which needs no square root at all. Both checked by script.
- **[Rader's algorithm](/rader-fft/).** For prime $n$, a cyclic convolution of length $n - 1$ indexed by a primitive root modulo $n$; it is often faster when $n - 1$ is smooth, and Bluestein can compute its convolution when it is not.

## When to use it

Use Bluestein's algorithm for lengths with a large prime factor, as the fallback in a [mixed-radix FFT](/mixed-radix-fft/), for the chirp z-transform and zoomed spectra, and over finite fields whose roots of unity have order not a power of two. For lengths that are products of small factors, a mixed-radix or [prime-factor FFT](/chinese-remainder-theorem-fft/) is faster by the constant factor. When only a few outputs are needed, the [Goertzel algorithm](/goertzel-algorithm/) or the direct sum is simpler.

## Pitfalls

- **Convolution too short.** With $M < 2n - 2$ the positions of $c_d^{-1}$ and $c_{d'}^{-1}$ collide for $d - d' = M$, and the result is wrong in general. Use $M \ge 2n - 1$ (or exactly $2n - 2$, see above), not $M \ge n$.
- **Large chirp angles.** Computing $e^{-\pi i m^2 / n}$ with $m^2$ unreduced loses accuracy once $m^2$ is large, because the angle is huge. Reduce $m^2$ modulo $2n$ first, which is exact in integers.
- **Twiddles by repeated powers.** Generating the chirp or the FFT twiddles as powers of one computed root accumulates error. A first version of the implementation here that did so had relative error about $2 \times 10^{-13}$ at $n = 1000$; computing each value directly brought it to about $8 \times 10^{-16}$ (observed).
- **The sign of $\zeta$.** With the convention $\omega_n = e^{+2\pi i/n}$, use $\zeta = e^{+\pi i/n}$; mixing signs gives $X_{n-k}$ in place of $X_k$.
- **Modular roots.** Over $\mathbb{Z}/p\mathbb{Z}$ the chirp needs $\zeta$ and the convolution needs a principal $M$-th root; with $p = 998244353$ any $M \le 2^{23}$ is fine, but $n$ must divide $p - 1$, and $2n$ must too unless $n$ is odd.

## Implementations

## History

Bluestein presented the reduction of the DFT to a linear filter with a chirp impulse response at the Northeast Electronics Research and Engineering Meeting in 1968 and published it in 1970. In 1969, Rabiner, Schafer and Rader generalised it to the chirp z-transform, which evaluates the z-transform on a spiral contour with one convolution done by FFTs. In 1968 Rader gave a different reduction of a prime-length DFT to a cyclic convolution, of length $n - 1$, through a primitive root modulo $n$. The two methods are the usual ways to handle prime lengths, alongside the prime-factor re-indexing of Good (1958) and Thomas (1963) for coprime factors, in the framework of Cooley and Tukey (1965).

## References
