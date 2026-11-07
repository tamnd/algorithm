---
tag: R0R6ZN
kind: theorem
slug: convolution-theorem
name: Convolution theorem
aliases:
- DFT convolution theorem
- cyclic convolution theorem
area: algebra/fast-transforms
level: core
summary: The DFT of a cyclic convolution is the pointwise product of the DFTs, so a cyclic convolution of length n costs three DFTs and n products.
prereqs: [convolution, discrete-fourier-transform, fft-summation-lemma]
see_also: [convolution-via-fft, fast-fourier-transform, number-theoretic-transform, dft-matrix, fft-polynomial-multiplication, evaluation-interpolation-paradigm, parseval-theorem, fast-walsh-hadamard-transform]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Section 30.2 (the convolution theorem, stated for vectors padded to length 2n, and its use for polynomial multiplication)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition
    locator: Chapter 8, Section 8.2 (the DFT as evaluation at the powers of ω, and cyclic convolution as multiplication modulo x^n - 1)
  - book: isbn:9780898712858
    title: Charles Van Loan, Computational Frameworks for the Fast Fourier Transform, SIAM, 1992
    locator: Chapter 4, Section 4.2, Convolution (diagonalization of circulant matrices by the DFT matrix)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer, 2011
    locator: Chapter 22, Section 22.1, Convolution (computing cyclic, linear and negacyclic convolution by the FFT)
  - paper: "Thomas G. Stockham Jr., High-speed convolution and correlation, AFIPS Spring Joint Computer Conference 28, 1966"
    locator: pp. 229 to 233 (convolution and correlation of long sequences by the FFT)
---

The convolution theorem says that the [discrete Fourier transform](/discrete-fourier-transform/) turns [cyclic convolution](/convolution/) into pointwise multiplication: $F_n(a \circledast b) = F_n a \cdot F_n b$, where the product on the right is taken entry by entry. Since the DFT is invertible when $n$ is a unit, a cyclic convolution of length $n$ costs three DFTs and $n$ products. With the [fast Fourier transform](/fast-fourier-transform/) this is $O(n \log n)$ operations, against $\Theta(n^2)$ for the direct sum. This is the basis of [convolution via FFT](/convolution-via-fft/), of fast polynomial and integer multiplication, and of fast digital filtering.

## Statement

**Notation.** As on the [DFT page](/discrete-fourier-transform/): $n \ge 1$ is the length, $R$ is a commutative ring, and $\omega \in R$. Over $\mathbb{C}$, $\omega = \omega_n = e^{-2\pi i/n}$; everything below also holds for $e^{+2\pi i/n}$. The DFT of $x \in R^n$ is $(F_n x)_k = X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$. The cyclic convolution of $a, b \in R^n$ is $(a \circledast b)_k = \sum_{j=0}^{n-1} a_j b_{(k-j) \bmod n}$, and $u \cdot v$ is the entrywise product $(u_k v_k)_k$.

**Theorem (forward form).** Let $\omega \in R$ satisfy $\omega^n = 1$. For all $a, b \in R^n$,

$$F_n(a \circledast b) = F_n a \cdot F_n b, \qquad \text{that is,} \qquad \sum_{m=0}^{n-1} (a \circledast b)_m \, \omega^{mk} = A_k B_k \quad \text{for } 0 \le k \le n-1.$$

**Theorem (inverse form).** If moreover $\omega$ is a principal $n$-th root of unity ($\sum_{j=0}^{n-1} \omega^{jk} = 0$ for $1 \le k \le n-1$) and $n$ is a unit of $R$, then

$$a \circledast b = F_n^{-1}\left(F_n a \cdot F_n b\right), \qquad F_n^{-1} y = \tfrac{1}{n} \left(\textstyle\sum_{k} y_k \omega^{-jk}\right)_j.$$

Over $\mathbb{C}$ with $\omega = \omega_n$, both hypotheses hold for each $n \ge 1$.

## In plain words

A Fourier transform describes a list of numbers as a mix of waves of different speeds. Convolution, which slides one list along another and adds products, is hard to compute directly. The theorem says that in the wave description it becomes easy: each wave of the result is just the product of the matching waves of the two inputs.

So there is a detour that is shorter than the direct road. Transform both lists, multiply the matching entries, and transform back. With the fast Fourier transform each transform is cheap, and the whole detour is much faster than sliding and adding, once the lists are long.

## Proof

**Forward form, by the sum.** Fix $k$. Using $\omega^n = 1$, the power $\omega^{mk}$ depends only on $m \bmod n$, so $\omega^{mk} = \omega^{jk} \omega^{((m - j) \bmod n) k}$ for all $j, m$. Then

$$\sum_{m=0}^{n-1} (a \circledast b)_m \, \omega^{mk} = \sum_{j=0}^{n-1} a_j \omega^{jk} \sum_{m=0}^{n-1} b_{(m-j) \bmod n} \, \omega^{((m-j) \bmod n) k}.$$

For fixed $j$, the map $m \mapsto (m - j) \bmod n$ is a bijection of $\{0, \ldots, n-1\}$, so the inner sum is $\sum_{l=0}^{n-1} b_l \omega^{lk} = B_k$. The outer sum is then $A_k B_k$.

**Forward form, by polynomials.** Let $A(t) = \sum a_j t^j$, $B(t) = \sum b_j t^j$ and $C(t) = \sum_m (a \circledast b)_m t^m$. Then $C(t) \equiv A(t) B(t) \pmod{t^n - 1}$, so $A(t)B(t) = C(t) + Q(t)(t^n - 1)$ for some $Q \in R[t]$. Put $t = \omega^k$: since $(\omega^k)^n = 1$, the second term vanishes, and $C(\omega^k) = A(\omega^k) B(\omega^k)$. Since $X_k = X(\omega^k)$ for each vector, this is the claim.

**Inverse form.** If $\omega$ is principal and $n$ is a unit, then by the [summation lemma](/fft-summation-lemma/) the DFT matrix has the inverse $F_n^{-1} = \frac{1}{n}(\omega^{-jk})_{j,k}$, as shown on the [DFT page](/discrete-fourier-transform/). Apply $F_n^{-1}$ to both sides of the forward form. $\blacksquare$

### Examples

- Over $\mathbb{C}$ with $n = 4$: $a = (1, 2, 3, 4)$ and $b = (5, 6, 7, 8)$ have $F_4 a = (10, -2+2i, -2, -2-2i)$ and $F_4 b = (26, -2+2i, -2, -2-2i)$. The products are $(260, -8i, 4, 8i)$. The cyclic convolution is $a \circledast b = (66, 68, 66, 60)$, and its DFT is $(260, -8i, 4, 8i)$, as the theorem says. For instance $66 - 68 + 66 - 60 = 4$.
- Over $\mathbb{Z}/17\mathbb{Z}$ with $\omega = 4$, a principal $4$-th root: $F_4 a = (10, 7, 15, 6)$ and $F_4 b = (9, 7, 15, 6)$, with products $(5, 15, 4, 2)$. Transforming back with $\omega^{-1} = 13$ and $4^{-1} = 13$ gives $(15, 0, 15, 9)$, which is $(66, 68, 66, 60)$ reduced modulo $17$.
- With $n = 1$, the theorem says $a_0 b_0 = a_0 b_0$. With the impulse $b = (1, 0, \ldots, 0)$, $F_n b = (1, \ldots, 1)$ and $a \circledast b = a$.

## Consequences

- **Fast cyclic convolution.** $a \circledast b$ costs two forward DFTs, $n$ multiplications, and one inverse DFT. With the [FFT](/fast-fourier-transform/) for $n$ a power of two, this is $\frac{3}{2} n \lg n + 2n$ multiplications and $3 n \lg n$ additions in $R$, counting the scaling by $1/n$. The algorithm is [convolution via FFT](/convolution-via-fft/).
- **Fast linear convolution and polynomial multiplication.** Pad to a length $N \ge m + \ell - 1$, as on the [convolution page](/convolution/). Then the cyclic convolution of length $N$ is the linear one. This is the [FFT polynomial multiplication](/fft-polynomial-multiplication/) and an instance of the [evaluation-interpolation paradigm](/evaluation-interpolation-paradigm/): evaluate both factors at the $N$-th roots of unity, multiply the values, and interpolate.
- **Circulant matrices.** The circulant matrix $C$ with first column $c$ acts by $Cb = c \circledast b$. The theorem says $F_n C = \mathrm{diag}(F_n c) F_n$, that is $C = F_n^{-1} \mathrm{diag}(F_n c) F_n$: the DFT diagonalizes every circulant, and the eigenvalues of $C$ are the entries of $F_n c$. See the [DFT matrix](/dft-matrix/).
- **The dual form.** Over $\mathbb{C}$, $F_n(a \cdot b) = \frac{1}{n} F_n a \circledast F_n b$: a product in time is a convolution in frequency, scaled by $1/n$. The proof is the same computation with $F_n^{-1}$ in place of $F_n$.
- **Correlation.** For real $a$, the DFT of the [cross-correlation](/cross-correlation/) $r_k = \sum_j a_j b_{(j + k) \bmod n}$ is $\overline{F_n a} \cdot F_n b$. With $b = a$ this gives the power spectrum $|A_k|^2$, whose inverse DFT is the [autocorrelation](/autocorrelation/).
- **Negacyclic convolution.** If $\psi$ satisfies $\psi^2 = \omega$ and $\psi^n = -1$, then the negacyclic convolution of $a$ and $b$ is $\psi^{-j}$ times the cyclic convolution of $(\psi^j a_j)$ and $(\psi^j b_j)$. This weighted form is used in the [Schönhage-Strassen](/schonhage-strassen-multiplication/) method.
- **Other groups.** The same theorem holds for each finite abelian group with its characters. For the group $(\mathbb{Z}/2\mathbb{Z})^k$ the transform is the [Walsh-Hadamard transform](/fast-walsh-hadamard-transform/), and convolution becomes XOR convolution.

## Tightness

**The forward form needs only $\omega^n = 1$.** The proof above uses no other property, so the forward form holds for each $n$-th root of unity, principal or not, and in each commutative ring.

**The inverse form needs a principal root and a unit length.** Over $\mathbb{F}_7$ with $n = 6$ and $\omega = 2$, $\omega^6 = 1$ but $\omega$ has order $3$, so it is not principal. The nonzero vector $x = (1, 0, 0, 6, 0, 0)$ has $X_k = 1 + 6 \cdot 2^{3k} = 7 \equiv 0$ for each $k$. So $F_6 x = 0$, and the products $F_6 a \cdot F_6 b$ do not determine $a \circledast b$: for example $x \circledast (1, 0, \ldots, 0) = x \ne 0$, but the pointwise product is $0$. In a ring where $n \cdot 1 = 0$, the inverse fails for the same reason, as on the [summation lemma](/fft-summation-lemma/) page.

**The theorem is about cyclic convolution.** The DFT of a linear convolution of two vectors of length $n$ is not the product of their DFTs of length $n$: the high terms wrap around. For $(1, 2, 3, 4)$ and $(5, 6, 7, 8)$, the linear convolution $(5, 16, 34, 60, 61, 52, 32)$ has length $7$, and the length-$4$ product gives $(66, 68, 66, 60)$, which is that vector folded modulo $4$. Zero padding to length at least $7$ removes the wrap.

## History

The convolution theorem for Fourier series and Fourier integrals is classical. Its discrete form became an algorithm when the FFT made the transforms cheap: Stockham (1966) described the computation of convolutions and correlations by the FFT, with long inputs cut into sections. Over finite fields, the same theorem with a principal root of unity in $\mathbb{Z}/p\mathbb{Z}$ gives exact convolution, which is the basis of the [number-theoretic transform](/number-theoretic-transform/). CLRS, Section 30.2, states the theorem for vectors padded to length $2n$, in the form used for polynomial multiplication.

## References
