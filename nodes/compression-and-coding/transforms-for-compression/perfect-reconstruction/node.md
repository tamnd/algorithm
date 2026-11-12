---
tag: P3AH4J
kind: definition
slug: perfect-reconstruction
name: Perfect reconstruction
aliases:
- PR property
- perfect reconstruction filter bank
area: compression-and-coding/transforms-for-compression
level: advanced
summary: Property that a filter bank returns exactly its input when no coefficients are altered.
prereqs: [filter-bank]
see_also: [modified-discrete-cosine-transform, orthogonal-transform, lifting-scheme, discrete-wavelet-transform, subband-coding, aliasing, jpeg-2000, haar-wavelet]
sources:
  - paper: "A. Croisier, D. Esteban and C. Galand, Perfect channel splitting by use of interpolation/decimation/tree decomposition techniques, Proceedings of the International Conference on Information Sciences and Systems, Patras, 1976"
    title: A. Croisier, D. Esteban and C. Galand, Perfect channel splitting by use of interpolation/decimation/tree decomposition techniques
    locator: the two-channel quadrature mirror filter bank, H1(z) = H0(-z), which cancels aliasing
  - paper: doi:10.1109/ICASSP.1984.1172486
    title: M. J. T. Smith and T. P. Barnwell, A procedure for designing exact reconstruction filter banks for tree-structured subband coders, Proceedings of ICASSP 1984, vol. 9
    locator: pp. 421 to 424 (conjugate quadrature filters, the first FIR two-channel banks with exact reconstruction)
  - paper: doi:10.1109/TASSP.1986.1164832
    title: M. J. T. Smith and T. P. Barnwell, Exact reconstruction techniques for tree-structured subband coders, IEEE Transactions on Acoustics, Speech, and Signal Processing 34(3), 1986
    locator: pp. 434 to 441 (the design of the halfband product filter and its spectral factorization)
  - paper: doi:10.1109/TASSP.1985.1164587
    title: Fred Mintzer, Filters for distortion-free two-band multirate filter banks, IEEE Transactions on Acoustics, Speech, and Signal Processing 33(3), 1985
    locator: pp. 626 to 630 (the same orthogonal two-channel solution, found independently)
  - paper: doi:10.1016/0165-1684(86)90101-5
    title: Martin Vetterli, Filter banks allowing perfect reconstruction, Signal Processing 10(3), 1986
    locator: pp. 219 to 244 (the polyphase matrix and the conditions for perfect reconstruction in M channels)
  - book: isbn:9780136057185
    title: P. P. Vaidyanathan, Multirate Systems and Filter Banks, Prentice Hall, 1993
    locator: Chapter 5 (alias cancellation, the distortion function, and the polyphase conditions for perfect reconstruction) and Chapter 6 (paraunitary banks)
  - book: isbn:9780130970800
    title: Martin Vetterli and Jelena Kovačević, Wavelets and Subband Coding, Prentice Hall, 1995
    locator: Section 3.2, Two-channel filter banks (orthogonal and biorthogonal perfect reconstruction, the product filter, linear phase)
  - paper: doi:10.1109/ICASSP.1988.196696
    title: D. Le Gall and A. Tabatabai, Sub-band coding of digital images using symmetric short kernel filters and arithmetic coding techniques, Proceedings of ICASSP 1988
    locator: pp. 761 to 764 (the symmetric 5/3 pair with perfect reconstruction)
  - paper: doi:10.1109/ICASSP.1980.1171025
    title: J. D. Johnston, A filter family designed for use in quadrature mirror filter banks, Proceedings of ICASSP 1980, vol. 5
    locator: pp. 291 to 294 (QMF designs with near-perfect reconstruction)
  - paper: doi:10.1002/cpa.3160410705
    title: Ingrid Daubechies, Orthonormal bases of compactly supported wavelets, Communications on Pure and Applied Mathematics 41(7), 1988
    locator: pp. 909 to 996 (orthogonal two-channel FIR filters with a maximal number of vanishing moments, including the 4-tap filter)
---

## Definition

Let a [filter bank](/filter-bank/) have analysis filters $h_0, \dots, h_{M-1}$, downsampling by $M$, upsampling by $M$ and synthesis filters $f_0, \dots, f_{M-1}$, and let $\hat x$ be its output when the subbands pass from the analysis to the synthesis unchanged. The bank has **perfect reconstruction** (PR) if there are a constant $c \ne 0$ and an integer delay $l \ge 0$ such that

$$\hat x[n] = c\, x[n - l] \qquad \text{for every input } x \text{ and every } n,$$

that is, $\hat X(z) = c\, z^{-l} X(z)$. Many authors scale the filters so that $c = 1$. A bank whose output is only close to $c\,x[n-l]$ has **near-perfect reconstruction**.

**The two-channel conditions.** For $M = 2$ the output is

$$\hat X(z) = T(z)\, X(z) + A(z)\, X(-z),$$
$$T(z) = \tfrac12\big[F_0(z)H_0(z) + F_1(z)H_1(z)\big], \qquad A(z) = \tfrac12\big[F_0(z)H_0(-z) + F_1(z)H_1(-z)\big].$$

PR holds exactly when both conditions hold:

1. **Alias cancellation:** $A(z) = 0$.
2. **No distortion:** $T(z) = c\, z^{-l}$. This rules out amplitude distortion (a $|T|$ that varies with frequency) and phase distortion (a phase that is not linear).

The alias-cancelling choice $F_0(z) = H_1(-z)$ and $F_1(z) = -H_0(-z)$ meets condition 1 for every analysis pair. With it, let $P(z) = F_0(z) H_0(z) = H_1(-z) H_0(z)$, the **product filter**. Then $F_1(z) H_1(z) = -P(-z)$, and condition 2 becomes

$$P(z) - P(-z) = 2c\, z^{-l}.$$

$P(z) - P(-z)$ keeps only the odd powers of $z^{-1}$, doubled. So $l$ is odd, and $P$ is a **halfband** filter: all its coefficients at odd indices are zero except the one at index $l$, which is $c$. Designing a two-channel PR bank is the same as designing a halfband $P$ and factoring it into $H_0$ and $H_1(-z)$.

**The M-channel condition.** With the polyphase matrices $\mathbf E(z)$ of the analysis and $\mathbf R(z)$ of the synthesis, the condition $\mathbf R(z)\mathbf E(z) = c\, z^{-l_0} I$ is sufficient for PR. The necessary and sufficient condition allows $\mathbf R(z)\mathbf E(z)$ to be $c\, z^{-l_0}$ times a block matrix $\begin{pmatrix} 0 & I_{M-r} \\ z^{-1} I_r & 0 \end{pmatrix}$ for some $0 \le r < M$ (Vaidyanathan 1993, Chapter 5).

## Examples and non-examples

**Haar (orthogonal, PR).** $h_0 = (1, 1)/\sqrt2$ and $h_1 = (1, -1)/\sqrt2$ give $H_1(-z) = H_0(z)$ and

$$P(z) = H_0(z)^2 = \tfrac12\big(1 + 2z^{-1} + z^{-2}\big).$$

The only odd coefficient is $1$ at index 1, so $T(z) = z^{-1}$: PR with $c = 1$ and $l = 1$.

**LeGall 5/3 (biorthogonal, PR).** $h_0 = (-1, 2, 6, 2, -1)/8$ and $h_1 = (-\frac12, 1, -\frac12)$. Then $H_1(-z)$ has the coefficients $(-\frac12, -1, -\frac12)$ and

$$P(z) = -\tfrac{1}{16}\big(-1 + 9z^{-2} + 16z^{-3} + 9z^{-4} - z^{-6}\big).$$

The odd coefficients are $0, -1, 0$ at indices 1, 3, 5, so $T(z) = -z^{-3}$: PR with $c = -1$ and $l = 3$; changing the sign of both synthesis filters gives $c = 1$. The filters are symmetric, so the bank has linear phase. $(-1, 0, 9, 16, 9, 0, -1)/16$ is the classic halfband filter, and the 5/3 pair is one of its factorizations.

**Daubechies 4-tap (orthogonal, PR).** Let $h_0 = (1 + \sqrt3, 3 + \sqrt3, 3 - \sqrt3, 1 - \sqrt3)/(4\sqrt2)$ and let $h_1$ be its conjugate quadrature filter, $h_1[n] = (-1)^n h_0[3 - n]$. Then $H_1(-z) = z^{-3} H_0(z^{-1})$, so $P(z)$ is the autocorrelation of $h_0$ shifted by 3. The coefficients at odd indices of $P$ are the autocorrelation values at the even lags $-2, 0, 2$, which are $0, 1, 0$ because $h_0$ is orthonormal to its shifts by 2. So $T(z) = z^{-3}$.

**The tests.** The implementation on the page [filter bank](/filter-bank/) checks these three banks on 500 random inputs (seed 21): each output is $c\, x[n - l]$ with $(c, l) = (1, 1)$, $(-1, 3)$ and $(1, 3)$.

**The CEG quadrature mirror filter bank (no PR beyond two taps).** Croisier, Esteban and Galand (1976) set $H_1(z) = H_0(-z)$, $F_0 = H_0$ and $F_1 = -H_1$. Then $A(z) = \frac12[H_0(z)H_0(-z) - H_0(-z)H_0(z)] = 0$ for every $H_0$: aliasing always cancels. Write $H_0(z) = E_0(z^2) + z^{-1}E_1(z^2)$ in polyphase form. Then

$$T(z) = \tfrac12\big[H_0(z)^2 - H_0(-z)^2\big] = 2z^{-1} E_0(z^2)\, E_1(z^2).$$

For FIR filters this is a single power of $z$ only if $E_0$ and $E_1$ are both single powers, that is, if $h_0$ has at most two nonzero taps, as in Haar. So no nontrivial FIR filter gives PR in this structure. For example, $h_0 = (1, 2, 1)\sqrt2/4$ gives $T(z) = \frac12 z^{-1} + \frac12 z^{-3}$: the output is the mean of two delayed copies of the input, not one. Johnston (1980) designed longer QMFs that make $|T|$ nearly flat, which is near-perfect reconstruction.

**A misaligned bank (no PR).** Delay the 5/3 highpass by one sample, $h_1 = (0, -\frac12, 1, -\frac12)$, and use the alias-cancelling synthesis. Aliasing still cancels, but now $P(z) = H_1(-z)H_0(z)$ has $-1$ times the old product times $z^{-1}$, so its odd coefficients become the even coefficients of the old product, and $T(z)$ has several terms. The output is no longer a delayed copy of the input. The tests check this case.

**The MDCT (PR).** With a symmetric window that meets $w[n]^2 + w[n+N]^2 = 1$, the [MDCT](/modified-discrete-cosine-transform/) with overlap-add is an $N$-channel PR bank: the time domain aliasing of each frame cancels against that of the next.

**Quantized subbands (not part of the definition).** PR is a property of the bank with unchanged subbands. Once the subbands are quantized, the output differs from the input. For an orthogonal bank the squared error of the output equals the squared error of the subbands; for a biorthogonal bank it does not, and the synthesis filters can amplify it.

## Related definitions

- **Alias cancellation** is condition 1 alone. A bank with alias cancellation but no PR is a linear time-invariant filter $T(z)$, as in the QMF example.
- **Orthogonal (paraunitary) bank.** A PR bank whose polyphase matrix satisfies $\mathbf E^{\mathsf T}(z^{-1})\mathbf E(z) = I$. Its synthesis filters are the time-reversed analysis filters, and the whole bank is an [orthogonal transform](/orthogonal-transform/) of the signal. In two channels these are the conjugate quadrature filters of Smith and Barnwell (1984, 1986) and Mintzer (1985).
- **Biorthogonal bank.** A PR bank that is not orthogonal: the synthesis filters are a dual basis of the analysis filters. This allows symmetric FIR filters such as the 5/3 and 9/7 filters of [JPEG 2000](/jpeg-2000/). An orthogonal two-channel FIR bank with real symmetric filters must be the Haar bank.
- **Lifting.** A two-channel bank written as a sequence of [lifting steps](/lifting-scheme/) has PR by construction, because each step is undone by subtracting what it added; this holds even with rounding, which gives integer-to-integer transforms.
- **Time domain aliasing cancellation (TDAC).** The form of PR used by the MDCT, in which aliasing is cancelled in the time domain between overlapping frames.
- **Near-perfect reconstruction.** $A(z)$ and $T(z) - c z^{-l}$ are small but not zero, as in the pseudo-QMF bank of MPEG-1 audio.
- **Oversampled PR.** When the channels keep more samples than the input, PR means that the analysis is a frame and the synthesis a dual frame. There are then many synthesis banks for one analysis bank.

## References
