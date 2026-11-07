---
tag: GVPDNK
kind: theorem
slug: fft-cancellation-lemma
name: Cancellation lemma
aliases:
- cancellation lemma for roots of unity
area: algebra/fast-transforms
level: core
summary: For integers n ≥ 1, k ≥ 0 and d ≥ 1, ω_(dn)^(dk) = ω_n^k; in particular ω_n^(n/2) = -1 for even n.
prereqs: [roots-of-unity]
see_also: [fft-halving-lemma, fft-summation-lemma, discrete-fourier-transform, fast-fourier-transform, twiddle-factor, butterfly-operation]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2 (the cancellation lemma and its corollary that the (n/2)-th power of the principal n-th root is -1)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2 (roots of unity in a commutative ring, and the powers ω^2 used by the recursive FFT)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.2, The FFT Idea (the relation between the roots of unity of orders n and n/2)
  - paper: doi:10.1109/MASSP.1984.1162257
    title: Michael T. Heideman, Don H. Johnson and C. Sidney Burrus, Gauss and the history of the fast Fourier transform, IEEE ASSP Magazine 1(4), 1984
    locator: pp. 14 to 21 (Gauss's treatise of about 1805, published in 1866, and its relation to the method of Cooley and Tukey)
---

The cancellation lemma says that a power of a root of unity does not change when the order of the root and the exponent are multiplied by the same factor: $\omega_{dn}^{dk} = \omega_n^k$. Its main case is $d = 2$: the square of a principal $n$-th [root of unity](/roots-of-unity/) is a principal $(n/2)$-th root, and $\omega_n^{n/2} = -1$. These two facts let the [fast Fourier transform](/fast-fourier-transform/) split a [DFT](/discrete-fourier-transform/) of length $n$ into two DFTs of length $n/2$ and combine them with [butterflies](/butterfly-operation/).

## Statement

The notation is that of the [discrete Fourier transform](/discrete-fourier-transform/): $\omega_n = e^{-2\pi i/n}$.

**Lemma (complex form).** For integers $n \ge 1$, $d \ge 1$ and $k$,

$$\omega_{dn}^{dk} = \omega_n^{k}.$$

**Corollary.** For each even $n \ge 2$, $\omega_n^{n/2} = \omega_2 = -1$. So $\omega_n^{k + n/2} = -\omega_n^k$ for each integer $k$.

**Lemma (ring form).** Let $R$ be a commutative ring, let $d, n \ge 1$, and let $\omega \in R$ be a principal $(dn)$-th root of unity. If $d \cdot 1$ is not a zero divisor of $R$ (for example, if $dn$ is a unit, as it is whenever the inverse transform of length $dn$ exists), then $\omega^d$ is a principal $n$-th root of unity. If moreover $n$ is even and $\frac{n}{2} \cdot 1$ is not a zero divisor, then $\omega^{n/2} = -1$ for a principal $n$-th root $\omega$.

## In plain words

Mark points at equal steps around a circle. If you mark twice as many points, each step is half as long, so two small steps land where one big step landed before. The lemma says exactly this, for any factor in place of two.

The second fact is that half of a full turn lands on the point opposite the start, which is minus one. So a point and the point half a turn further on are each other's negatives. The fast Fourier transform uses both facts: it works with half as many points, and it gets the second half of the answer from the first half by a change of sign.

## Proof

**Complex form.** For an integer $m$ and a complex $z$, $(e^{z})^m = e^{mz}$. So

$$\omega_{dn}^{dk} = \left(e^{-2\pi i/(dn)}\right)^{dk} = e^{-2\pi i \, dk/(dn)} = e^{-2\pi i k/n} = \left(e^{-2\pi i/n}\right)^{k} = \omega_n^k.$$

**Corollary.** With $n = 2m$, the lemma with $d = m$ and $k = 1$ gives $\omega_n^{m} = \omega_{m \cdot 2}^{m \cdot 1} = \omega_2 = e^{-\pi i} = -1$. Then $\omega_n^{k + n/2} = \omega_n^k \omega_n^{n/2} = -\omega_n^k$.

**Ring form.** Let $\eta = \omega^d$. First, $\eta^n = \omega^{dn} = 1$. Now let $1 \le k \le n - 1$ and $m = dk$, so $1 \le m \le dn - 1$. Because $\omega$ is a principal $(dn)$-th root,

$$0 = \sum_{j=0}^{dn-1} \omega^{mj}.$$

Write $j = qn + r$ with $0 \le q \le d - 1$ and $0 \le r \le n - 1$. Then $\omega^{mj} = \omega^{mr} \, (\omega^{dn})^{kq} = \omega^{mr}$. Each $r$ occurs for exactly $d$ values of $j$, so

$$0 = d \cdot \sum_{r=0}^{n-1} \omega^{dkr} = d \cdot \sum_{r=0}^{n-1} \eta^{kr}.$$

Since $d \cdot 1$ is not a zero divisor, $\sum_{r=0}^{n-1} \eta^{kr} = 0$. This holds for each $k$ from $1$ to $n - 1$, so $\eta$ is a principal $n$-th root of unity. If $dn$ is a unit, then $d$ divides a unit, so $d \cdot 1$ is a unit and not a zero divisor.

For the last claim, let $n = 2m$ with $m \cdot 1$ not a zero divisor, and apply what we just proved with $d = m$ and order $2$: the element $\omega^{m}$ is a principal square root of unity, so $1 + \omega^{m} = 0$ by the definition with $k = 1$. So $\omega^{n/2} = -1$. $\blacksquare$

### Examples

- $\omega_8^2 = e^{-\pi i/2} = -i = \omega_4$, and $\omega_8^4 = -1 = \omega_2$.
- $\omega_{12}^{9} = \omega_4^{3} = i$ with $d = 3$.
- In $\mathbb{Z}/17\mathbb{Z}$, $\omega = 2$ is a principal $8$-th root of unity. Its square $4$ has powers $1, 4, 16, 13$, so $4$ is a principal $4$-th root, and $2^4 = 16 \equiv -1$.
- For the NTT prime $p = 998244353 = 119 \cdot 2^{23} + 1$, the element $3$ is a [primitive root](/primitive-root/), so $g = 3^{119}$ has order $2^{23}$. By the lemma, $g^{2^{23}/n}$ is a principal $n$-th root for each power of two $n \le 2^{23}$. This is how each [number-theoretic transform](/number-theoretic-transform/) of this prime picks its root.

## Consequences

- **The radix-2 split.** In the [fast Fourier transform](/fast-fourier-transform/), the even-indexed inputs are transformed with $\omega_n^2 = \omega_{n/2}$, which is the DFT of length $n/2$. The corollary gives the second half of the output from the first half, $X_{k + n/2} = E_k - \omega_n^k O_k$. This is the [butterfly operation](/butterfly-operation/).
- **The halving lemma.** The [halving lemma](/fft-halving-lemma/) is the cancellation lemma with $d = 2$, read as a statement on the set of all $n$-th roots.
- **Twiddle factors.** The [twiddle factors](/twiddle-factor/) of the stage of length $m$ are the powers of $\omega_m = \omega_n^{n/m}$, so one table of the powers of $\omega_n$ serves all stages.
- **Choosing roots in a finite field.** A principal $n$-th root for each divisor $n$ of $N$ is a power of one principal $N$-th root, as in the NTT example above.

## Tightness

**The zero-divisor hypothesis in the ring form is needed.** In the field $\mathbb{F}_2$, take $\omega = 1$, $d = 2$ and $n = 3$. Then $\omega^6 = 1$, and for each $k$ the sum $\sum_{j=0}^{5} \omega^{jk} = 6 \cdot 1 = 0$, so $\omega$ meets the definition of a principal $6$-th root. But $\omega^2 = 1$ gives $\sum_{j=0}^{2} 1 = 3 \cdot 1 = 1 \ne 0$, so $\omega^2$ is not a principal cube root. Here $d \cdot 1 = 0$, which is a zero divisor. In such a ring the length $6$ is not a unit and the DFT of length $6$ has no inverse, so the safe hypothesis for FFT work is that the length is a unit.

**The corollary needs the order to be even.** For odd $n$, no power of $\omega_n$ equals $-1$, because $\omega_n^k = -1$ means $2k/n$ is an odd integer, which is impossible when $n$ is odd. This is why the radix-2 butterfly needs even lengths, and why odd lengths use [Rader's](/rader-fft/), [Bluestein's](/bluestein-fft/) or the [mixed-radix](/mixed-radix-fft/) methods.

## History

The identity $\omega_{dn}^{dk} = \omega_n^k$ is the rule of exponents for complex exponentials. The name "cancellation lemma" is the one of CLRS, Section 30.2, where it comes with the corollary $\omega_n^{n/2} = -1$ and the halving and summation lemmas. The idea of splitting a Fourier transform of length $n_1 n_2$ into transforms of lengths $n_1$ and $n_2$, which rests on this identity, goes back to Gauss, about 1805, and was found again by Cooley and Tukey in 1965; see the [fast Fourier transform](/fast-fourier-transform/) for that history and its sources.

## References
