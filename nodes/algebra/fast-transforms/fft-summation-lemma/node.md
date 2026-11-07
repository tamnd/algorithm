---
tag: 7JDGB4
kind: theorem
slug: fft-summation-lemma
name: Summation lemma
aliases:
- orthogonality of roots of unity
area: algebra/fast-transforms
level: core
summary: For an integer k that n does not divide, the sum of (ω_n^k)^j over j = 0, ..., n-1 is zero; when n divides k the sum is n.
prereqs: [roots-of-unity, geometric-series]
see_also: [fft-cancellation-lemma, fft-halving-lemma, discrete-fourier-transform, inverse-discrete-fourier-transform, dft-matrix, convolution-theorem, parseval-theorem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2 (the summation lemma and its use in the proof of the inverse DFT)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2 (primitive roots of unity in a commutative ring, defined by the condition that ω^(n/t) - 1 is not a zero divisor, and the sums of their powers)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.1 (the identity that the DFT matrix times its conjugate is n times the identity)
---

The summation lemma says that the powers of an $n$-th [root of unity](/roots-of-unity/) other than $1$ add up to zero: $\sum_{j=0}^{n-1} (\omega_n^k)^j = 0$ when $n$ does not divide $k$, and the sum is $n$ when $n$ divides $k$. It is the orthogonality relation of the [DFT matrix](/dft-matrix/), and it is the reason why the [inverse DFT](/inverse-discrete-fourier-transform/) is a DFT with the inverse root and a factor $1/n$. Together with the [cancellation lemma](/fft-cancellation-lemma/) and the [halving lemma](/fft-halving-lemma/), it is one of the three facts on roots of unity behind the [fast Fourier transform](/fast-fourier-transform/).

## Statement

The notation is that of the [discrete Fourier transform](/discrete-fourier-transform/): $\omega_n = e^{-2\pi i/n}$, and each statement also holds for $e^{+2\pi i/n}$.

**Lemma (complex form).** Let $n \ge 1$ and let $k$ be an integer. Then

$$\sum_{j=0}^{n-1} \omega_n^{jk} = \begin{cases} n & \text{if } n \mid k, \\ 0 & \text{if } n \nmid k. \end{cases}$$

**Lemma (ring form).** Let $R$ be a commutative ring, $n \ge 1$, and $\omega \in R$ with $\omega^n = 1$. Let $k$ be an integer. If $n \mid k$, then $\sum_{j=0}^{n-1} \omega^{jk} = n \cdot 1$. If $n \nmid k$ and $\omega^k - 1$ is not a zero divisor of $R$, then $\sum_{j=0}^{n-1} \omega^{jk} = 0$. In particular, if $R$ is a field or an integral domain and $\omega$ has order exactly $n$, the sum is $0$ for each $k$ with $n \nmid k$.

Negative $k$ is allowed: $\omega^{-1} = \omega^{n-1}$ because $\omega^n = 1$.

## In plain words

Put a number of points at equal steps around a circle, starting at the point on the right, with the circle centred at zero. Add all the points as arrows from the centre. The arrows pull in all directions with the same strength, so they cancel, and the sum is zero.

The same is true if you visit the points by jumping a fixed number of steps each time, as long as the jump does not bring you back to the start at once. If the jump is a whole turn, each visit lands on the start, and the sum is the number of points. This fact makes the waves of the Fourier transform independent of each other, so the transform can be undone.

## Proof

Write $z = \omega^k$, where $\omega = \omega_n$ in the complex form. Since $\omega^n = 1$, we have $z^n = (\omega^n)^k = 1$. This also holds for negative $k$, with $\omega^{-1}$ the inverse of $\omega$.

**Case $n \mid k$.** Write $k = qn$. Then $z = (\omega^n)^q = 1$, so each term of the sum is $1$ and the sum is $n \cdot 1$.

**Case $n \nmid k$, ring form.** Let $S = \sum_{j=0}^{n-1} z^j$. The sum telescopes:

$$(z - 1) S = \sum_{j=0}^{n-1} z^{j+1} - \sum_{j=0}^{n-1} z^{j} = z^n - 1 = 0.$$

So $(\omega^k - 1) S = 0$. By hypothesis, $\omega^k - 1$ is not a zero divisor, so $S = 0$.

**Case $n \nmid k$, complex form.** Here $\omega_n^k = e^{-2\pi i k/n}$, and $e^{i\theta} = 1$ holds only when $\theta$ is an integer multiple of $2\pi$. Since $k/n$ is not an integer, $\omega_n^k \ne 1$. In the field $\mathbb{C}$ a nonzero element is not a zero divisor, so the ring form gives $S = 0$.

**Field or integral domain.** If $\omega$ has order exactly $n$ and $n \nmid k$, then $\omega^k \ne 1$, so $\omega^k - 1 \ne 0$, and a nonzero element of an integral domain is not a zero divisor. The ring form applies. $\blacksquare$

### Examples

- For $n = 8$ and $k = 2$, the terms are $\omega_8^{2j} = (-i)^j$: $1, -i, -1, i, 1, -i, -1, i$, with sum $0$.
- In $\mathbb{Z}/17\mathbb{Z}$, $\omega = 2$ has order $8$, because $2^4 = 16 \equiv -1$. For $k = 1$, $\sum_{j=0}^{7} 2^j = 255 = 15 \cdot 17 \equiv 0$. For $k = 3$ and $k = 4$ the sum is also $0$. For $k = 8$ each term is $1$ and the sum is $8$.
- For $n = 1$ each $k$ is a multiple of $n$, and the sum is the single term $1$.

## Consequences

- **The inverse DFT.** The lemma with $k = m - j$ gives $\sum_{k=0}^{n-1} \omega^{(m-j)k} = n$ if $m \equiv j \pmod n$ and $0$ otherwise. So the [DFT matrix](/dft-matrix/) $F_n = (\omega^{jk})$ satisfies $F_n F_n' = nI$ with $F_n' = (\omega^{-jk})$, and $F_n^{-1} = \frac{1}{n}(\omega^{-jk})$ when $n$ is a unit. This is the inversion formula of the [discrete Fourier transform](/discrete-fourier-transform/) and the basis of the [inverse FFT](/inverse-fft/).
- **Principal roots.** The definition of a principal $n$-th root of unity asks for exactly the conclusion of the lemma for $1 \le k \le n-1$. The lemma shows that in a field each element of order $n$ is principal.
- **The convolution theorem.** The proof of the [convolution theorem](/convolution-theorem/) by the inverse transform uses the same orthogonality.
- **Parseval's theorem.** Over $\mathbb{C}$, $\overline{\omega_n^{jk}} = \omega_n^{-jk}$, so the lemma says that the columns of $F_n$ are orthogonal with squared length $n$. This gives [Parseval's theorem](/parseval-theorem/), $\sum_k |X_k|^2 = n \sum_j |x_j|^2$.
- **Filtering a residue class.** The sum $\frac{1}{n}\sum_{j=0}^{n-1} \omega_n^{jk}$ is $1$ when $n \mid k$ and $0$ otherwise. Multiplying a power series by such sums selects the terms whose index is in one residue class modulo $n$ (the roots-of-unity filter).

## Tightness

**The zero-divisor hypothesis is needed.** In $\mathbb{Z}/15\mathbb{Z}$, $\omega = 4$ satisfies $\omega^2 = 16 \equiv 1$ and $\omega \ne 1$. But $1 + 4 = 5 \not\equiv 0$. Here $\omega - 1 = 3$ is a zero divisor, since $3 \cdot 5 \equiv 0$, so the lemma does not apply. Order $n$ alone is not enough in a ring with zero divisors.

**The divisibility condition is needed.** For $n \mid k$ the sum is $n \cdot 1$, which is not zero in $\mathbb{C}$. In a ring where $n \cdot 1 = 0$, such as $\mathbb{F}_2$ with $n = 2$ and $\omega = 1$, the sum is zero for each $k$, and the DFT of length $n$ is not invertible. This is why the inverse transform needs $n$ to be a unit.

## History

The vanishing of the sum of the $n$-th roots of unity is a classical consequence of the formula for a [geometric series](/geometric-series/). The name "summation lemma" is the one used by CLRS in Section 30.2, where it appears next to the cancellation and halving lemmas as the tool for the inverse DFT. The ring form with the condition on zero divisors is the setting of the FFT over rings in von zur Gathen and Gerhard, Section 8.2.

## References
