---
tag: 4J8PSN
kind: theorem
slug: fft-halving-lemma
name: Halving lemma
aliases:
- halving lemma for roots of unity
area: algebra/fast-transforms
level: core
summary: For even n, squaring the n complex n-th roots of unity gives the n/2 complex (n/2)-th roots of unity, each exactly twice.
prereqs: [fft-cancellation-lemma, roots-of-unity]
see_also: [fft-summation-lemma, fast-fourier-transform, discrete-fourier-transform, butterfly-operation, iterative-fft]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2 (the halving lemma and its use in the recursive FFT)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2 (the FFT as evaluation at the powers of ω, split into evaluations at the powers of ω^2)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.2, The FFT Idea, and Section 1.3, The Cooley-Tukey Factorization
  - paper: doi:10.1109/MASSP.1984.1162257
    title: Michael T. Heideman, Don H. Johnson and C. Sidney Burrus, Gauss and the history of the fast Fourier transform, IEEE ASSP Magazine 1(4), 1984
    locator: pp. 14 to 21 (Gauss's treatise of about 1805 and the work of Cooley and Tukey)
---

The halving lemma says that for even $n$, the squares of the $n$ complex $n$-th [roots of unity](/roots-of-unity/) are exactly the $n/2$ complex $(n/2)$-th roots of unity, and each of them is the square of exactly two $n$-th roots. So evaluating a polynomial in $t^2$ at all $n$-th roots needs only $n/2$ points. This is the step that makes the [fast Fourier transform](/fast-fourier-transform/) run in $O(n \log n)$: each level of the recursion halves the number of points, not only the degree.

## Statement

The notation is that of the [discrete Fourier transform](/discrete-fourier-transform/): $\omega_n = e^{-2\pi i/n}$, and $U_n = \{\omega_n^k : 0 \le k \le n-1\}$ is the set of the complex $n$-th roots of unity.

**Lemma (complex form).** Let $n \ge 2$ be even. The map $s(z) = z^2$ sends $U_n$ onto $U_{n/2}$, and each element of $U_{n/2}$ has exactly two preimages in $U_n$. In terms of indices, for $0 \le k \le n-1$,

$$\left(\omega_n^{k}\right)^2 = \omega_{n/2}^{\,k \bmod (n/2)}, \qquad \omega_n^{k + n/2} = -\omega_n^{k}.$$

**Lemma (ring form).** Let $R$ be a commutative ring in which $n$ is a unit, let $n$ be even, and let $\omega$ be a principal $n$-th root of unity. Then $\omega^2$ is a principal $(n/2)$-th root of unity, the elements $1, \omega, \ldots, \omega^{n-1}$ are distinct, and $(\omega^{k})^2 = (\omega^{k + n/2})^2$ with $\omega^{k + n/2} = -\omega^k$ for each $k$.

## In plain words

Mark an even number of points at equal steps around a circle, and replace each point by its square. Squaring doubles the angle of a point. So the points fall onto a circle of half as many points, and two marks go to each new point: a mark and the mark exactly opposite to it.

Why does this matter? The fast Fourier transform must find the value of a polynomial at all the marked points. It splits the polynomial into a part with even powers and a part with odd powers. Each part only needs the squares of the points, and there are only half as many squares. So each part is the same kind of problem at half the size.

## Proof

**Complex form.** Let $n = 2m$.

1. *The squares lie in $U_m$.* By the [cancellation lemma](/fft-cancellation-lemma/) with $d = 2$, $(\omega_n^k)^2 = \omega_{2m}^{2k} = \omega_m^k$. Since $\omega_m^m = 1$, $\omega_m^k = \omega_m^{k \bmod m}$. This proves the index formula, and $s(U_n) \subseteq U_m$.
2. *The two preimages.* By the corollary of the cancellation lemma, $\omega_n^{m} = -1$, so $\omega_n^{k+m} = -\omega_n^k$ and $(\omega_n^{k+m})^2 = (\omega_n^k)^2$. For $0 \le k \le m-1$, the indices $k$ and $k + m$ both lie in $\{0, \ldots, n-1\}$, and both map to $\omega_m^k$.
3. *Onto, with exactly two preimages.* The $n$ indices $0, \ldots, n-1$ split into the $m$ pairs $\{k, k + m\}$ with $0 \le k \le m-1$. The pair $\{k, k+m\}$ maps to $\omega_m^k$. The values $\omega_m^0, \ldots, \omega_m^{m-1}$ are distinct, because $\omega_m^a = \omega_m^b$ with $0 \le a < b \le m-1$ gives $e^{-2\pi i (b-a)/m} = 1$ with $0 < b - a < m$, which is false. The elements $\omega_n^0, \ldots, \omega_n^{n-1}$ are distinct for the same reason. So each element of $U_m$ is the image of exactly the two elements of one pair, and $s$ maps $U_n$ onto $U_m$.

**Ring form.** Since $n$ is a unit, $2 \cdot 1$ and $m \cdot 1$ are units, so by the ring form of the [cancellation lemma](/fft-cancellation-lemma/), $\omega^2$ is a principal $m$-th root of unity and $\omega^{m} = -1$. So $\omega^{k+m} = -\omega^k$ and the squares agree. For distinctness, suppose $\omega^a = \omega^b$ with $0 \le a < b \le n - 1$, and let $r = b - a$. Then $\omega^{r} = 1$, so $\sum_{j=0}^{n-1} \omega^{rj} = n \cdot 1$. Since $1 \le r \le n - 1$, the definition of a principal root makes this sum $0$. So $n \cdot 1 = 0$, which is false because $n$ is a unit (and $R \ne 0$). $\blacksquare$

### Examples

- For $n = 8$: the roots are $\omega_8^k$, $k = 0, \ldots, 7$, and their squares are $1, -i, -1, i, 1, -i, -1, i$. These are the four $4$-th roots of unity, each twice, with $\omega_8^k$ and $\omega_8^{k+4}$ in each pair.
- In $\mathbb{Z}/17\mathbb{Z}$ with $\omega = 2$ of order $8$: the powers $1, 2, 4, 8, 16, 15, 13, 9$ square to $1, 4, 16, 13, 1, 4, 16, 13$. The pairs are $\{2^k, 2^{k+4}\} = \{2^k, -2^k\}$, for example $\{2, 15\}$ and $\{8, 9\}$.
- For $n = 2$, $U_2 = \{1, -1\}$ and both square to $1$, the only element of $U_1$.

## Consequences

- **The recursion of the FFT.** Write $A(t) = A_{\mathrm{even}}(t^2) + t \, A_{\mathrm{odd}}(t^2)$, where $A_{\mathrm{even}}$ and $A_{\mathrm{odd}}$ have the even and odd coefficients of $A$. To evaluate $A$ at the $n$ points of $U_n$, it is enough to evaluate $A_{\mathrm{even}}$ and $A_{\mathrm{odd}}$ at the $n/2$ points of $U_{n/2}$: these are two DFTs of length $n/2$. The cost recurrence $T(n) = 2T(n/2) + \Theta(n)$ gives $T(n) = \Theta(n \log n)$ by the [master theorem](/master-theorem/). See the [fast Fourier transform](/fast-fourier-transform/).
- **The butterfly.** The two preimages $\omega_n^k$ and $-\omega_n^k$ of one square give the two outputs $X_k = E_k + \omega_n^k O_k$ and $X_{k+n/2} = E_k - \omega_n^k O_k$ of one [butterfly](/butterfly-operation/).
- **Number-theoretic transforms.** The ring form gives the same recursion over $\mathbb{Z}/p\mathbb{Z}$, for the [number-theoretic transform](/number-theoretic-transform/).

## Tightness

**The lemma needs $n$ to be even.** For odd $n$, the map $z \mapsto z^2$ is a bijection of $U_n$ onto itself: $\omega_n^{2a} = \omega_n^{2b}$ implies $n \mid 2(a - b)$, so $n \mid a - b$ because $n$ is odd. So squaring does not reduce the number of points, and the radix-2 split gives nothing. Odd lengths use other factors of $n$ ([mixed radix](/mixed-radix-fft/)) or other methods ([Rader](/rader-fft/), [Bluestein](/bluestein-fft/)).

**In a ring, the unit hypothesis is needed for distinctness.** In $\mathbb{F}_2$, $\omega = 1$ is a principal $2$-nd root by the definition, since $1 + 1 = 0$. Its two powers $1, 1$ are equal, so the "two preimages" are the same element. Here $n = 2$ is not a unit.

## History

The name "halving lemma" is the one of CLRS, Section 30.2, where the lemma is the key step of the recursive FFT. The fact itself is the core of the radix-2 case of the method of Cooley and Tukey (1965). The general idea of splitting a transform of length $n_1 n_2$ into transforms of lengths $n_1$ and $n_2$ goes back to Gauss, about 1805; see the [fast Fourier transform](/fast-fourier-transform/) for that history and its sources.

## References
