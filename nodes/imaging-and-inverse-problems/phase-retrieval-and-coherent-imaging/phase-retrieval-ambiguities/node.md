---
tag: KD2SV5
kind: definition
slug: phase-retrieval-ambiguities
name: Trivial ambiguities of phase retrieval
aliases:
- phase retrieval ambiguities
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: core
summary: "The changes that never alter the Fourier magnitude of a signal: a global phase factor, a shift and the conjugate reversal. Any other signal with the same magnitude is a nontrivial ambiguity."
prereqs: [phase-retrieval]
see_also: [bruck-sodin-uniqueness, oversampling-in-phase-retrieval, complement-property, minimum-phase, patterson-function, twin-image-problem, autocorrelation, z-transform]
sources:
  - paper: doi:10.1109/MSP.2014.2352673
    title: Yoav Shechtman, Yonina C. Eldar, Oren Cohen, Henry N. Chapman, Jianwei Miao and Mordechai Segev, Phase retrieval with application to optical imaging, a contemporary overview, IEEE Signal Processing Magazine 32(3), 2015, 87 to 109
    locator: Section III.B (Uniqueness), the list of the three trivial ambiguities, the 1D example of two signals of length 5 with the same autocorrelation, and the uniqueness for d of two or more
  - paper: doi:10.1109/TASSP.1982.1163863
    title: Monson H. Hayes, The reconstruction of a multidimensional sequence from the phase or magnitude of its Fourier transform, IEEE Transactions on Acoustics, Speech, and Signal Processing 30(2), 1982, 140 to 154
    locator: uniqueness from the Fourier magnitude up to the trivial ambiguities for multidimensional sequences (general locator; section not confirmed)
---

The trivial ambiguities of [phase retrieval](/phase-retrieval/) are the three changes of a signal that never alter the magnitude of its Fourier transform: multiplication by a constant of modulus one, a shift, and the conjugate reversal. No data on the magnitude alone can tell a signal from these copies, so a solution of phase retrieval is called unique when it is unique up to them. Every other signal with the same magnitude is a **nontrivial ambiguity**. Nontrivial ambiguities are the rule in 1D and the exception in two or more dimensions.

## Definition

Let $x$ be a complex signal of finite support on $\mathbb{Z}^d$, $d \ge 1$, with Fourier transform $X(\omega) = \sum_t x[t]\, e^{-i t \cdot \omega}$ for $\omega \in [-\pi, \pi]^d$.

**Trivial ambiguities.** For $c \in \mathbb{C}$ with $|c| = 1$ and $t_0 \in \mathbb{Z}^d$:

1. **Global phase.** $y[t] = c\, x[t]$. Then $Y = c X$.
2. **Shift.** $y[t] = x[t - t_0]$. Then $Y(\omega) = e^{-i t_0 \cdot \omega} X(\omega)$.
3. **Conjugate reversal.** $y[t] = \overline{x[-t]}$. Then $Y(\omega) = \sum_t \overline{x[-t]}\, e^{-i t \cdot \omega} = \overline{\sum_s x[s]\, e^{-i s \cdot \omega}} = \overline{X(\omega)}$.

In each case $|Y(\omega)| = |X(\omega)|$ for every $\omega$. The **trivial class** of $x$ is the set of all signals made from $x$ by these operations:

$$\{\, c\, x[t - t_0] \,\} \cup \{\, c\, \overline{x[t_0 - t]} \,\}, \qquad |c| = 1,\ t_0 \in \mathbb{Z}^d.$$

The class is closed under the three operations, so two signals are **trivially equivalent** when one is in the trivial class of the other, and this is an equivalence relation.

**Uniqueness and nontrivial ambiguities.** $x$ is **uniquely determined** by its Fourier magnitude if every finitely supported $y$ with $|Y| = |X|$ is in the trivial class of $x$. A $y$ with $|Y| = |X|$ outside that class is a nontrivial ambiguity. Since $|X|^2$ is the Fourier transform of the [autocorrelation](/autocorrelation/) $r[k] = \sum_t x[t + k]\, \overline{x[t]}$, two signals have the same magnitude exactly when they have the same autocorrelation.

**Real signals.** For a real $x$ the trivial operations that keep it real are $y = \pm x[t - t_0]$ and $y = \pm x[t_0 - t]$: the phase is only a sign, and the conjugate reversal is the plain reversal.

**A known support.** If $x$ is known to lie in the box $\{0, \dots, n_1 - 1\} \times \cdots \times \{0, \dots, n_d - 1\}$ and fills it, with nonzero values on each face, then only two shifts keep the copies inside the box, and the trivial class in the box is $\{c\, x[t]\} \cup \{c\, \overline{x[n - 1 - t]}\}$, with $n - 1 = (n_1 - 1, \dots, n_d - 1)$. This is the form used on the [phase retrieval](/phase-retrieval/) page.

**General measurements.** For data $|\langle a_k, x \rangle|$ with general vectors $a_k$, only the global phase is always trivial, because $|\langle a_k, c x \rangle| = |\langle a_k, x \rangle|$ for every $a_k$. Shifts and reversals keep the data only for Fourier vectors. The [complement property](/complement-property/) tells when real data of this kind fix $x$ up to sign.

## Examples and non-examples

**All three for one complex signal.** Take $x = [1, i]$ on $t = 0, 1$. Then $X(\omega) = 1 + i e^{-i\omega}$ and $|X(\omega)|^2 = 2 + 2 \sin\omega$. The global phase copy $\frac{3 + 4i}{5} x$, the shift $[0, 1, i]$ and the conjugate reversal $[-i, 1]$ (in the box) all have this magnitude. For $[-i, 1]$, $|{-i} + e^{-i\omega}|^2 = 2 - 2 \operatorname{Re}(i e^{i\omega}) = 2 + 2 \sin\omega$.

**Non-example: the plain reversal of a complex signal.** The reversal $[i, 1]$ of $x = [1, i]$ has the magnitude $|i + e^{-i\omega}|^2 = 2 - 2\sin\omega$, which is not the magnitude of $x$. The conjugation is needed.

**Non-example: a sign change of one entry.** $[1, 1]$ and $[1, -1]$ have $|X|^2 = 2 + 2\cos\omega$ and $2 - 2\cos\omega$. A local change of sign is not an ambiguity of Fourier data, even though it keeps every $|x[t]|$. In the same way, the modulation $x[t] e^{i \theta t}$ moves the magnitude to $|X(\omega - \theta)|$, which is a different magnitude for $\theta \neq 0$ unless $|X|$ is periodic with period $\theta$.

**A nontrivial ambiguity in 1D.** $x = [1, 5, 6]$ and $y = [2, 7, 3]$ have the same autocorrelation $[6, 35, 62, 35, 6]$, since $X(z) = (1 + 2z^{-1})(1 + 3z^{-1})$ and $y$ comes from the flip of the zero $-2$ to $-1/2$. No sign, shift or reversal maps one to the other. In 1D almost every signal of length $n$ has $2^{n-2}$ trivial classes with its magnitude (see the [phase retrieval](/phase-retrieval/) page).

**A nontrivial ambiguity with the same support.** Shechtman et al. (2015, Section III.B) give $u = [1, 0, -2, 0, -2]$ and $v = [1 - \sqrt3, 0, 1, 0, 1 + \sqrt3]$. Both have the autocorrelation $[-2, 0, 2, 0, 9, 0, 2, 0, -2]$: for $v$, lag $0$ gives $(1 - \sqrt3)^2 + 1 + (1 + \sqrt3)^2 = 9$, lag $2$ gives $(1 - \sqrt3) + (1 + \sqrt3) = 2$, and lag $4$ gives $(1 + \sqrt3)(1 - \sqrt3) = -2$. A known support does not remove the ambiguity.

**2D: only trivial, and not only trivial.** The image $\begin{pmatrix} 1 & 2 \\ 3 & 5 \end{pmatrix}$ has an irreducible z-transform, and among integer $2 \times 2$ images only $\pm$ itself and $\pm \begin{pmatrix} 5 & 3 \\ 2 & 1 \end{pmatrix}$ share its autocorrelation, which is its trivial class in the box. The separable image $\begin{pmatrix} 1 & 2 \\ 3 & 6 \end{pmatrix}$ also shares its magnitude with $\begin{pmatrix} 2 & 1 \\ 6 & 3 \end{pmatrix}$, a reversal along one axis only, which is a nontrivial ambiguity. See the [Bruck-Sodin uniqueness theorem](/bruck-sodin-uniqueness/).

## Related definitions

- **Uniqueness in two or more dimensions.** For almost every image of finite support in two or more dimensions, the trivial class is the whole set of solutions ([Bruck-Sodin uniqueness theorem](/bruck-sodin-uniqueness/); Hayes 1982).
- **Zero flipping.** In 1D, the nontrivial ambiguities come from replacing a zero $a$ of the [z-transform](/z-transform/) by $1/\bar a$. Flipping all zeros gives the conjugate reversal, a trivial ambiguity.
- **Minimum phase.** Among the 1D signals with a given magnitude, the [minimum phase](/minimum-phase/) one has all its zeros inside the unit circle. A causality or minimum phase condition picks one signal from the zero flips.
- **Homometric sets.** In crystallography, structures with the same [Patterson function](/patterson-function/) are called homometric. They are the nontrivial ambiguities of the autocorrelation of a crystal.
- **Twin image.** In in-line holography the conjugate image overlaps the true image (see the [twin image problem](/twin-image-problem/)). In phase retrieval from a support, the image and its conjugate reversal fit the data equally well, so an iterative method can find either one.
- **Oversampling.** Sampling the magnitude at least $2n_k - 1$ times along each axis gives the whole autocorrelation, so the samples allow the same ambiguities as the whole magnitude and no more ([oversampling in phase retrieval](/oversampling-in-phase-retrieval/)).

## References
