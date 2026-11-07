---
tag: RQQMCS
kind: theorem
slug: parseval-theorem
name: Parseval's theorem
aliases:
- Parseval-Plancherel identity
- Parseval's identity for the DFT
- Plancherel theorem for the DFT
- energy theorem
area: algebra/fast-transforms
level: intro
summary: The sum of squared magnitudes is preserved by the DFT up to a factor of n.
prereqs: [discrete-fourier-transform, fft-summation-lemma]
see_also: [dft-matrix, inverse-discrete-fourier-transform, convolution-theorem, haar-wavelet-transform, walsh-hadamard-transform, unitary-operator, wiener-khinchin-theorem, periodogram]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 8, The Discrete Fourier Transform (the properties of the DFT, among them Parseval's relation for finite-length sequences)
  - url: https://en.wikipedia.org/wiki/Parseval%27s_theorem
    title: Parseval's theorem, Wikipedia
    locator: the sections Notation used in physics and engineering (the DFT form with the factor 1/N) and History (Parseval's memoir of 1799 and Plancherel's paper of 1910)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 1, Section 1.1 (the DFT matrix and the identity F_n times its conjugate transpose equals n I)
  - paper: "Marc-Antoine Parseval des Chênes, Mémoire sur les séries et sur l'intégration complète d'une équation aux différences partielles linéaires du second ordre, à coefficients constants, presented to the Académie des Sciences on 5 April 1799, Mémoires présentés à l'Institut des Sciences, Lettres et Arts, Sciences mathématiques et physiques, volume 1, 1806"
    locator: pages 638 to 648
  - paper: doi:10.1007/BF03014877
    title: Michel Plancherel, Contribution à l'étude de la représentation d'une fonction arbitraire par des intégrales définies, Rendiconti del Circolo Matematico di Palermo 30, 1910
    locator: pp. 289 to 335 (the identity for Fourier integrals of square-integrable functions)
---

Parseval's theorem for the [discrete Fourier transform](/discrete-fourier-transform/) says that the DFT keeps the energy of a vector up to a factor $n$: $\sum_k |X_k|^2 = n \sum_j |x_j|^2$. More generally it keeps inner products, $\sum_k X_k \overline{Y_k} = n \sum_j x_j \overline{y_j}$, so the scaled matrix $F_n/\sqrt n$ is unitary. The proof is one exchange of sums and the [summation lemma](/fft-summation-lemma/). The theorem lets one measure errors, energy and least-squares fits in either domain, and it has an exact analogue over every ring that has a principal root of unity.

## Statement

**Notation.** The transform length is $n \ge 1$, $\omega_n = e^{-2\pi i/n}$, and $X_k = \sum_{j=0}^{n-1} x_j \omega_n^{jk}$ for $0 \le k < n$. The theorem holds unchanged with $e^{+2\pi i/n}$. Indices of $X$ are taken modulo $n$.

**Theorem (complex form).** Let $x, y \in \mathbb{C}^n$, with DFTs $X$ and $Y$. Then

$$\sum_{k=0}^{n-1} X_k \overline{Y_k} = n \sum_{j=0}^{n-1} x_j \overline{y_j}, \qquad \text{and in particular} \qquad \sum_{k=0}^{n-1} |X_k|^2 = n \sum_{j=0}^{n-1} |x_j|^2.$$

Equivalently $F_n^{*} F_n = nI$, where $F_n = (\omega_n^{jk})$ and $^{*}$ is the conjugate transpose, so $U_n = F_n/\sqrt n$ is unitary and $\lVert U_n x \rVert_2 = \lVert x \rVert_2$.

**Theorem (ring form).** Let $R$ be a commutative ring, and $\omega \in R$ a principal $n$-th root of unity. For $x, y \in R^n$ with $X = \mathrm{DFT}_\omega(x)$ and $Y = \mathrm{DFT}_\omega(y)$,

$$\sum_{k=0}^{n-1} X_k Y_{(-k) \bmod n} = n \sum_{j=0}^{n-1} x_j y_j.$$

Over $\mathbb{C}$ with real $y$, $Y_{-k} = \overline{Y_k}$, so the ring form contains the complex form for real vectors.

**Other normalizations.** With the unitary DFT, $X_k = \frac{1}{\sqrt n} \sum_j x_j \omega_n^{jk}$, the factor $n$ disappears. With the factor $\frac1n$ on the forward transform, as in Fourier series, it becomes $\sum_k |X_k|^2 = \frac1n \sum_j |x_j|^2$.

## In plain words

Think of a list of numbers as a signal, and of the sum of the squares of its sizes as its energy. The Fourier transform describes the same signal as a mix of pure waves. Parseval's theorem says that the energy is the same in both descriptions, up to one fixed factor that depends only on the length of the list. No energy is created or lost; it is only shared out among the waves.

The reason is that the pure waves are at right angles to each other, like the axes of a grid. Measuring a vector along axes that are at right angles, and adding the squares, always gives the same total. So an error that is small in one description is small in the other, and dropping the weakest waves loses exactly their share of the energy.

## Proof

**Ring form.** Put the definitions of $X_k$ and $Y_{-k}$ into the left side, and change the order of the finite sums:

$$\sum_{k} X_k Y_{-k} = \sum_{k} \Bigl(\sum_{j} x_j \omega^{jk}\Bigr)\Bigl(\sum_{l} y_l \omega^{-lk}\Bigr) = \sum_{j} \sum_{l} x_j y_l \sum_{k=0}^{n-1} \omega^{(j - l)k}.$$

Here $Y_{-k} = Y_{(n-k) \bmod n} = \sum_l y_l \omega^{l(n-k)} = \sum_l y_l \omega^{-lk}$, since $\omega^n = 1$ and $\omega$ is a unit with $\omega^{-1} = \omega^{n-1}$. For $j = l$ the inner sum is $n$. For $j \ne l$, let $r = (j - l) \bmod n$; then $1 \le r \le n - 1$, $\omega^{(j-l)k} = \omega^{rk}$, and the inner sum is $\sum_k \omega^{rk} = 0$ by the definition of a principal root (this is the [summation lemma](/fft-summation-lemma/) over $\mathbb{C}$). So only the terms with $j = l$ remain, and the left side equals $n \sum_j x_j y_j$. $\square$

**Complex form.** Over $\mathbb{C}$, $|\omega_n| = 1$, so $\overline{\omega_n^{lk}} = \omega_n^{-lk}$ and $\overline{Y_k} = \sum_l \overline{y_l}\, \omega_n^{-lk}$. The same exchange of sums gives

$$\sum_k X_k \overline{Y_k} = \sum_j \sum_l x_j \overline{y_l} \sum_k \omega_n^{(j-l)k} = n \sum_j x_j \overline{y_j},$$

because $\omega_n$ is a principal $n$-th root of unity: $\omega_n$ has order exactly $n$, so for $1 \le r \le n-1$, $\omega_n^r \ne 1$ and $\sum_k \omega_n^{rk} = (\omega_n^{rn} - 1)/(\omega_n^r - 1) = 0$. Taking $y = x$ gives the identity for $|X_k|^2$. In matrix form the identity for all $x, y$ says $y^{*} F_n^{*} F_n x = n\, y^{*} x$, which is $F_n^{*} F_n = nI$. $\blacksquare$

## Consequences

- **The inverse DFT.** $F_n^{*} F_n = nI$ gives $F_n^{-1} = \frac1n F_n^{*} = \frac1n \overline{F_n}$, which is the formula of the [inverse DFT](/inverse-discrete-fourier-transform/) with $\omega^{-1} = \overline{\omega_n}$.
- **Errors in both domains.** For a computed $\hat X = F_n \hat x$, $\lVert \hat X - X \rVert_2 = \sqrt n \lVert \hat x - x \rVert_2$, so a relative error in the 2-norm is the same in the time and the frequency domain. The error bounds of the [FFT](/fast-fourier-transform/) are stated in this norm for that reason.
- **Best approximation by truncation.** Keep a set $K$ of frequencies and set the others to zero. By the theorem, the squared error in the time domain is $\frac1n \sum_{k \notin K} |X_k|^2$. So keeping the $s$ largest $|X_k|$ gives the best approximation of $x$ by $s$ waves in the least-squares sense. The same holds for each orthonormal basis, for example the orthonormal [Haar transform](/haar-wavelet-transform/).
- **The power spectrum.** The values $|X_k|^2$ share the energy $n \sum_j |x_j|^2$ among the frequencies. Scaled, they form the [periodogram](/periodogram/), and $|X_k|^2$ is the DFT of the cyclic autocorrelation $r_m = \sum_j x_{(j+m) \bmod n} \overline{x_j}$, the finite form of the [Wiener-Khinchin theorem](/wiener-khinchin-theorem/).
- **Other orthogonal transforms.** The orthonormal [DCT](/discrete-cosine-transform/), the [Walsh-Hadamard transform](/walsh-hadamard-transform/) with the factor $1/\sqrt n$, and the orthonormal Haar transform keep the 2-norm exactly. For the Walsh-Hadamard transform $H_n$, $H_n^{T} H_n = nI$, which is the same statement with $\omega = -1$ over the group $(\mathbb{Z}/2\mathbb{Z})^t$.
- **Exact checks.** The ring form gives a cheap test of an [NTT](/number-theoretic-transform/) implementation: one sum on each side, with no rounding.

## Tightness

The theorem is an equality, so it cannot be improved, but each of its hypotheses is needed.

- **The factor $n$.** The impulse $x = (1, 0, \ldots, 0)$ has energy $1$, and its DFT is $(1, 1, \ldots, 1)$, with energy $n$. So the factor is $n$ and not $1$ for the unscaled DFT, for every $n \ge 2$.
- **A worked check.** For $x = (1, 2, 3, 4)$, $X = (10, -2 + 2i, -2, -2 - 2i)$. Then $\sum |X_k|^2 = 100 + 8 + 4 + 8 = 120 = 4 \cdot 30 = n \sum x_j^2$. For the box $x = (1, 1, 1, 1, 0, 0, 0, 0)$, $|X_k|^2$ is $16, 4 + 2\sqrt2, 0, 4 - 2\sqrt2, 0, 4 - 2\sqrt2, 0, 4 + 2\sqrt2$, with sum $32 = 8 \cdot 4$.
- **The ring form.** Over $\mathbb{Z}/17\mathbb{Z}$ with $\omega = 4$, $x = (1, 2, 3, 4)$ has $X = (10, 7, 15, 6)$. Then $X_0^2 + 2X_1X_3 + X_2^2 = 100 + 84 + 225 = 409 \equiv 1$, and $4 \cdot 30 = 120 \equiv 1 \pmod{17}$.
- **A root that is not principal.** In $\mathbb{Z}/15\mathbb{Z}$ the element $4$ has order $2$, but $1 + 4 = 5 \ne 0$, so it is not a principal square root of unity. For $n = 2$ the index $-k$ equals $k$. The vector $x = y = (1, 1)$ has $X = (1 + 1, 1 + 4) = (2, 5)$, and $X_0^2 + X_1^2 = 29 \equiv 14$, while $n \sum x_j^2 = 4$. So the ring form fails without the principal condition.
- **No conjugate.** Over $\mathbb{C}$, $\sum_k X_k^2 = n \sum_j x_j^2$ is false in general: $x = (0, 1, 0, 0)$ has $X = (1, -i, -1, i)$ and $\sum X_k^2 = 1 - 1 + 1 - 1 = 0 \ne 4$. The conjugate, or the index $-k$, is necessary.

## History

Marc-Antoine Parseval stated the identity for series in a memoir that he presented to the Académie des Sciences in Paris on 5 April 1799, published in 1806. It was later applied to Fourier series, where it says that the mean square of a function equals the sum of the squares of its Fourier coefficients. Michel Plancherel proved the corresponding statement for Fourier integrals of square-integrable functions in 1910, and the most general form is often called the Plancherel theorem. The discrete form for the DFT follows from the orthogonality of the roots of unity, and it appears in the standard texts on digital signal processing, for example Oppenheim and Schafer, Chapter 8.

## References
