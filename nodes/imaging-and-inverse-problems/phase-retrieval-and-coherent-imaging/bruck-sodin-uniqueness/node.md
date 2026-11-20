---
tag: YJRADG
kind: theorem
slug: bruck-sodin-uniqueness
name: Bruck-Sodin uniqueness theorem
aliases:
- uniqueness of multidimensional phase retrieval
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: "A finite image in two or more dimensions whose z-transform is irreducible is fixed by its Fourier magnitude up to shift, conjugate reversal and a global phase. Almost every image has this property."
prereqs: [phase-retrieval, autocorrelation, z-transform, irreducible-polynomial]
see_also: [phase-retrieval-ambiguities, oversampling-in-phase-retrieval, complement-property, polynomial-ring, gauss-lemma, determinant, coherent-diffraction-imaging, hybrid-input-output]
sources:
  - paper: doi:10.1016/0030-4018(79)90358-4
    title: Yu. M. Bruck and L. G. Sodin, On the ambiguity of the image reconstruction problem, Optics Communications 30(3), 1979, 304 to 308
    locator: the uniqueness of the reconstruction of a two dimensional image from its Fourier magnitude except for a set of measure zero (as summarized by Shechtman et al. 2015, Section III.B; the paper itself was not checked)
  - paper: doi:10.1109/TASSP.1982.1163863
    title: Monson H. Hayes, The reconstruction of a multidimensional sequence from the phase or magnitude of its Fourier transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 30(2), 1982, 140 to 154
    locator: the class of multidimensional sequences that the Fourier magnitude determines, those with irreducible z-transforms (general locator; section not confirmed)
  - paper: doi:10.1109/MSP.2014.2352673
    title: Yoav Shechtman, Yonina C. Eldar, Oren Cohen, Henry N. Chapman, Jianwei Miao and Mordechai Segev, Phase retrieval with application to optical imaging, a contemporary overview, IEEE Signal Processing Magazine 32(3), 2015, 87 to 109
    locator: Section III.B (Uniqueness), the statement for d of two or more, the role of reducible z-transforms, and the oversampled DFT with M of at least 2N - 1 in every dimension
---

The Bruck-Sodin uniqueness theorem says that [phase retrieval](/phase-retrieval/) of images, unlike phase retrieval of 1D signals, almost always has one answer. In 1D a signal of length $n$ can share its Fourier magnitude with up to $2^{n-2}$ essentially different signals. In two or more dimensions the Fourier magnitude of an image of finite support fixes the image up to the [trivial ambiguities](/phase-retrieval-ambiguities/), except for a set of images of measure zero. The reason is algebraic: a polynomial in one variable always splits into factors of degree one, but a polynomial in two or more variables almost never splits at all.

## Statement

Let $x$ be a complex image of finite support on $\mathbb{Z}^d$, not identically $0$, with the [z-transform](/z-transform/)

$$X(z) = \sum_{t} x[t]\, z^{-t}, \qquad z^{-t} = z_1^{-t_1} \cdots z_d^{-t_d},$$

a Laurent polynomial in $z_1, \dots, z_d$. Call $X$ **irreducible** if it is not a product $A B$ of two Laurent polynomials that are both not of the form $c\, z^{a}$.

**Theorem.** If $X$ is irreducible and $y$ is an image of finite support with $|Y(e^{i\omega})| = |X(e^{i\omega})|$ for all $\omega \in [-\pi, \pi]^d$, then for some $t_0 \in \mathbb{Z}^d$ and some $c$ with $|c| = 1$,

$$y[t] = c\, x[t - t_0] \quad \text{for all } t, \qquad \text{or} \qquad y[t] = c\, \overline{x[t_0 - t]} \quad \text{for all } t.$$

**Genericity.** Let $d \ge 2$ and let the support be the box $\{0, \dots, N_1 - 1\} \times \cdots \times \{0, \dots, N_d - 1\}$ with every $N_k \ge 2$. Then the images with a reducible $X$ form a set of Lebesgue measure zero, among the real images and among the complex images. So almost every image is fixed by its Fourier magnitude up to the trivial ambiguities.

The samples of $|X|$ on the grid of an $M_1 \times \cdots \times M_d$ point DFT with $M_k \ge 2 N_k - 1$ give the same information as the whole magnitude (Shechtman et al. 2015, Section III.B).

## In plain words

In one dimension, a signal of finite length is like a product of many small pieces, and each piece can be turned around without a change to the measured pattern. That is why many different signals give the same pattern.

In two or more dimensions, almost every image is a single piece that cannot be broken into smaller pieces. Then the only changes that keep the pattern are the ones that always keep it: move the image, turn it around through its center, or multiply it by a fixed phase. So a measured diffraction pattern of an image almost always has exactly one answer.

The theorem does not tell you how to find that answer, and it does not tell you how much noise the answer can take.

## Proof

**Step 1: the magnitude is the autocorrelation.** Let $r[k] = \sum_t x[t + k]\, \overline{x[t]}$ be the [autocorrelation](/autocorrelation/) of $x$, and write $X^{*}(z) = \sum_t \overline{x[t]}\, z^{t}$. Multiply out:

$$X(z)\, X^{*}(z) = \sum_{t, s} x[t]\, \overline{x[s]}\, z^{-(t - s)} = \sum_k r[k]\, z^{-k}.$$

On the torus $z = e^{i\omega}$, $X^{*}(e^{i\omega}) = \overline{X(e^{i\omega})}$, so $|X(e^{i\omega})|^2 = \sum_k r[k]\, e^{-i k \cdot \omega}$. A trigonometric polynomial fixes its coefficients, so $|Y| = |X|$ on the torus gives $r_y = r_x$, and then

$$Y(z)\, Y^{*}(z) = X(z)\, X^{*}(z) \tag{1}$$

as Laurent polynomials. If $X$ has support in a box with $N_k$ points per axis, $r$ has support in a box with $2 N_k - 1$ points per axis, so DFT samples on a grid with $M_k \ge 2 N_k - 1$ already give $r$ without [aliasing](/aliasing/).

**Step 2: unique factorization.** The ring $L = \mathbb{C}[z_1^{\pm 1}, \dots, z_d^{\pm 1}]$ of Laurent polynomials is the [polynomial ring](/polynomial-ring/) $\mathbb{C}[z_1, \dots, z_d]$ with the monomials made invertible. The polynomial ring has unique factorization (by [Gauss's lemma](/gauss-lemma/) and induction on $d$), and so does $L$. The units of $L$ are the $c\, z^{a}$ with $c \neq 0$. So "irreducible" in the statement is irreducibility in $L$.

**Step 3: the star map keeps irreducibility.** The map $\sigma(P)(z) = \overline{P}(1/z)$, which conjugates the coefficients and replaces each $z_k$ by $1/z_k$, is a bijection of $L$ to itself with $\sigma(P + Q) = \sigma(P) + \sigma(Q)$ and $\sigma(P Q) = \sigma(P)\, \sigma(Q)$. It sends units to units, so it sends irreducible elements to irreducible elements. Since $X^{*} = \sigma(X)$, the right side of (1) is a product of exactly two irreducible elements, $X$ and $X^{*}$.

**Step 4: compare the factors.** $Y \neq 0$ because $r_y[0] = r_x[0] > 0$. $Y$ is not a unit: if it were, then $Y^{*} = \sigma(Y)$ would be a unit too, and the left side of (1) would be a unit, but the right side is not. In the same way $Y^{*}$ is not a unit. By unique factorization in $L$, the left side of (1) also has exactly two irreducible factors, so $Y$ is irreducible and $Y = u X$ or $Y = u X^{*}$ for a unit $u = c\, z^{-t_0}$.

- $Y = c\, z^{-t_0} X$ means $y[t] = c\, x[t - t_0]$.
- $Y = c\, z^{-t_0} X^{*}$ means $\sum_t y[t] z^{-t} = \sum_s c\, \overline{x[s]}\, z^{s - t_0}$, so $y[t] = c\, \overline{x[t_0 - t]}$.

In both cases $r_y[0] = |c|^2\, r_x[0]$, so $|c| = 1$. This proves the theorem.

**Step 5: genericity, for $d = 2$.** Shift the box so that $X$ is an ordinary polynomial in $w_k = z_k^{-1}$ of degree at most $D = (N_1 - 1, N_2 - 1)$. If all four corner values of $x$ are nonzero, the degree is exactly $D$, every factor in $L$ can be shifted to an ordinary polynomial, and a reducible $X$ is a product $A B$ with degrees $a + b = D$, $a \neq (0, 0)$ and $b \neq (0, 0)$. For each such split, the products $A B$ form the image of a polynomial map from a space of dimension $(a_1 + 1)(a_2 + 1) + (b_1 + 1)(b_2 + 1)$, and the scaling $(A, B) \mapsto (sA, B/s)$ removes one more dimension. The space of all $X$ has dimension $(a_1 + b_1 + 1)(a_2 + b_2 + 1)$, and

$$(a_1 + b_1 + 1)(a_2 + b_2 + 1) - \bigl[(a_1 + 1)(a_2 + 1) + (b_1 + 1)(b_2 + 1) - 1\bigr] = a_1 b_2 + a_2 b_1 .$$

This is positive. If it were $0$, then $a_1 b_2 = 0$ and $a_2 b_1 = 0$. With $a_1 = 0$ we get $b_1 = N_1 - 1 \ge 1$, so $a_2 = 0$ and $a = (0, 0)$. With $b_2 = 0$ we get $a_2 = N_2 - 1 \ge 1$, so $b_1 = 0$ and $b = (0, 0)$. Both are excluded. So the reducible $X$ lie in a finite union of images of polynomial maps from spaces of smaller dimension. Such an image lies in the zero set of a nonzero polynomial in the coefficients, and that zero set has measure zero in $\mathbb{C}^{N_1 N_2}$ and, by the real and imaginary parts of the polynomial, also in $\mathbb{R}^{N_1 N_2}$. The images with a zero corner are a set of measure zero too. The count is the same in more dimensions. $\square$

## Consequences

- **The trivial ambiguities are all of them, generically.** For almost every image, every image with the same Fourier magnitude is a shift, a conjugate reversal through a point, or a phase multiple of it. For a real image the phase is only $\pm 1$ and the conjugate reversal is the plain reversal through a point.
- **Iterative methods have a target.** [Error reduction](/error-reduction-algorithm/), [hybrid input-output](/hybrid-input-output/) and their variants look for an image that fits the magnitude and a support. In two or more dimensions, the theorem says that the answer is generically unique, so a method that finds an image that fits the data has found the image, up to the trivial ambiguities. The theorem says nothing about whether the method finds it.
- **Sampling.** The DFT magnitude on a grid with $M_k \ge 2 N_k - 1$ points per axis is enough. This is about $2^d$ times the number of pixels; [oversampling](/oversampling-in-phase-retrieval/) by a smaller total factor often works in practice, but this theorem does not cover it.
- **Hand example: an irreducible image.** Take the real $2 \times 2$ image $x = \begin{pmatrix} 1 & 2 \\ 3 & 5 \end{pmatrix}$. With $w_1, w_2$ for the inverse variables, $X = 1 + 2 w_2 + 3 w_1 + 5 w_1 w_2$. A polynomial $p + q w_2 + s w_1 + v w_1 w_2$ of degree $(1, 1)$ can only split as $(\alpha + \beta w_1)(\gamma + \delta w_2)$, and that gives $p v = \alpha \gamma \beta \delta = q s$. So it is reducible exactly when the [determinant](/determinant/) $p v - q s$ is $0$. Here $1 \cdot 5 - 2 \cdot 3 = -1 \neq 0$, so $X$ is irreducible. The autocorrelation is the $3 \times 3$ array

$$r = \begin{pmatrix} 5 & 13 & 6 \\ 17 & 39 & 17 \\ 6 & 13 & 5 \end{pmatrix}$$

with lags $k_1 = -1, 0, 1$ in the rows and $k_2 = -1, 0, 1$ in the columns. For example $r[0, 0] = 1 + 4 + 9 + 25 = 39$, $r[1, 0] = 3 \cdot 1 + 5 \cdot 2 = 13$ and $r[1, -1] = 3 \cdot 2 = 6$. A search over all integer $2 \times 2$ images with entries from $-9$ to $9$ finds exactly 4 with this autocorrelation: $\pm x$ and $\pm \begin{pmatrix} 5 & 3 \\ 2 & 1 \end{pmatrix}$, the reversal of $x$ through its center. That is the theorem. For a random image the determinant is not $0$ with probability one, which is the genericity statement for $2 \times 2$ images.

## Tightness

- **One dimension.** Over $\mathbb{C}$, every polynomial in one variable of degree at least $2$ is a product of factors of degree one, by the [fundamental theorem of algebra](/fundamental-theorem-of-algebra/). So the irreducible case is only the case of length $2$, and the theorem says nothing for longer 1D signals. That matches the up to $2^{n-2}$ solutions on the [phase retrieval](/phase-retrieval/) page.
- **Reducible images do have other solutions.** If $X = A B$ with $A$ and $B$ not units, then $Y = A B^{*}$ satisfies $Y Y^{*} = A B^{*} A^{*} B = X X^{*}$, so $y$ has the same Fourier magnitude, and in general it is not a trivial copy of $x$. For the image $\begin{pmatrix} 1 & 2 \\ 3 & 6 \end{pmatrix}$, the determinant is $0$ and $X = (1 + 3 w_1)(1 + 2 w_2)$. Reversing the second factor gives $\begin{pmatrix} 2 & 1 \\ 6 & 3 \end{pmatrix}$, the image reversed along the second axis only. Both have the autocorrelation $\begin{pmatrix} 6 & 15 & 6 \\ 20 & 50 & 20 \\ 6 & 15 & 6 \end{pmatrix}$, and the same integer search finds 8 images with it instead of 4. An image that is a convolution of two smaller images is reducible in the same way.
- **The box must be at least $2$ wide on two axes.** If $N_2 = 1$, the image is a 1D signal and the first point applies. That is why the genericity statement needs $N_k \ge 2$.
- **Generic, not all.** The exceptional set has measure zero but it is not empty, and images near it can be hard to tell from their twins when the data have noise. The theorem is about exact data.

## History

In 1979 Bruck and Sodin, in Optics Communications, studied the ambiguity of the reconstruction of an image from its Fourier magnitude. Hayes (1982) showed that a large class of multidimensional sequences is fixed by the Fourier magnitude, the class with irreducible z-transforms, and also discussed algorithms. Shechtman et al. (2015, Section III.B) list Bruck and Sodin, Hayes, and Bates (1982, in Optik) as the sources of the result that, for $d \ge 2$, all images except a set of measure zero are fixed up to the trivial ambiguities. They add that the DFT magnitude with $M \ge 2N - 1$ in every dimension is enough. In 1D, Hayes, Lim and Oppenheim (1980) had described when the magnitude fixes a sequence, and the [phase retrieval](/phase-retrieval/) page shows the many solutions there.

## References
