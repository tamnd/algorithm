---
tag: YZ4Y3G
kind: problem
slug: phase-retrieval
name: Phase retrieval
aliases:
- magnitude-only reconstruction
area: graphics-and-signals/signal-processing
level: advanced
summary: "Recover a signal from the magnitude of its Fourier transform. In 1D the magnitude fixes only the autocorrelation, so many signals share it; extra constraints or iterations pick one."
model: real-ram
prereqs: [discrete-fourier-transform, autocorrelation]
see_also: [griffin-lim-algorithm, short-time-fourier-transform, minimum-phase, cepstrum, polynomial-root-finding, semidefinite-programming, signal-reconstruction, phase-correlation]
sources:
  - paper: doi:10.1364/AO.21.002758
    title: J. R. Fienup, Phase retrieval algorithms, a comparison, Applied Optics 21(15), 1982, 2758 to 2769
    locator: the error-reduction algorithm, its error that does not increase, and the input-output algorithms (hybrid input-output)
  - paper: "R. W. Gerchberg and W. O. Saxton, A practical algorithm for the determination of phase from image and diffraction plane pictures, Optik 35(2), 1972, pages 237 to 246"
    locator: the iteration between two planes with known magnitudes
  - paper: doi:10.1109/TASSP.1980.1163463
    title: Monson H. Hayes, Jae S. Lim and Alan V. Oppenheim, Signal reconstruction from phase or magnitude, IEEE Transactions on Acoustics, Speech, and Signal Processing 28(6), 1980, 672 to 680
    locator: the conditions under which the Fourier magnitude determines a finite sequence (general locator; section not confirmed)
  - paper: doi:10.1109/MSP.2014.2352673
    title: Yoav Shechtman, Yonina C. Eldar, Oren Cohen, Henry N. Chapman, Jianwei Miao and Mordechai Segev, Phase retrieval with application to optical imaging, a contemporary overview, IEEE Signal Processing Magazine 32(3), 2015, 87 to 109
    locator: the ambiguities in one dimension, uniqueness in higher dimensions, and the survey of algorithms (alternating projections, semidefinite relaxation, gradient methods)
---

Phase retrieval is the problem of recovering a signal $x$ when only the magnitude $|X(e^{i\omega})|$ of its Fourier transform is known. The magnitude is equivalent to the [autocorrelation](/autocorrelation/) of $x$, so the problem asks how much of a signal its autocorrelation determines. In one dimension the answer is: not much. A shift, a conjugate reversal and a constant phase factor never change the magnitude, and a signal of length $n$ can have up to $2^{n-2}$ essentially different signals with the same magnitude. Practical methods add constraints, such as a known support, nonnegativity or overlapping windows, and solve by iterations without a general guarantee.

## In plain words

A Fourier transform turns a signal into a list of waves, each with a strength and an alignment. Many instruments can measure only the strengths. A camera at the far field of an X-ray beam records how bright each spot is, but not how the waves line up. A spectrogram keeps the loudness of each frequency and drops the rest.

Phase retrieval asks for the signal back from the strengths alone. Some losses can never be undone: a delayed copy, a reversed copy, and a copy with all waves turned by the same angle look the same. In one dimension, worse things happen, and genuinely different signals give the same strengths. So the problem needs extra knowledge, for example where the signal is zero, and most methods guess and correct over and over.

## Definition

Let $x[0 \ldots n-1]$ be a complex signal with $x[0] \ne 0$ and $x[n-1] \ne 0$, and $X(e^{i\omega}) = \sum_{t=0}^{n-1} x[t] e^{-i\omega t}$ its [discrete-time Fourier transform](/discrete-time-fourier-transform/), with $\omega$ in radians per sample. The data are the values $|X(e^{i\omega})|$, either for all $\omega \in [-\pi, \pi]$ or at the $M$ points $\omega_k = 2\pi k / M$, which is the magnitude of the [DFT](/discrete-fourier-transform/) of $x$ padded with zeros to length $M$. The task is to find a signal $y$ of length $n$ with $|Y(e^{i\omega_k})| = |X(e^{i\omega_k})|$ for all $k$, and to describe all such $y$.

**The magnitude is the autocorrelation.** Let $r[k] = \sum_t x[t + k]\, \overline{x[t]}$ for $-(n-1) \le k \le n-1$. Then

$$|X(e^{i\omega})|^2 = X(e^{i\omega})\, \overline{X(e^{i\omega})} = \sum_{k=-(n-1)}^{n-1} r[k]\, e^{-i\omega k}.$$

The right side is a trigonometric polynomial with $2n - 1$ coefficients, so its values at $M \ge 2n - 1$ equally spaced points determine $r$ by an inverse DFT. Two signals of length $n$ have the same Fourier magnitude exactly when they have the same autocorrelation. With $M < 2n - 1$ points, the samples alias $r$ and the data carry less information.

**Trivial ambiguities.** For every $x$, these signals have the same magnitude: the shift $x[t - t_0]$, the conjugate reversal $\overline{x[n - 1 - t]}$, and the product $c\, x[t]$ with $|c| = 1$. For a real $x$, the last one is only $\pm x$, and the conjugate reversal is the plain reversal. A solution is called unique when it is unique up to these three operations.

**Nontrivial ambiguities.** Write the z-transform as $X(z) = x[0] \prod_{j=1}^{n-1} (1 - a_j z^{-1})$ with zeros $a_j$. On the unit circle $|1 - a e^{-i\omega}| = |e^{-i\omega} - \bar a|$, so replacing a factor $1 - a_j z^{-1}$ by $z^{-1} - \bar{a}_j$ moves the zero from $a_j$ to $1/\bar{a}_j$ and keeps the magnitude. Each of the $n - 1$ zeros can be flipped or not. Flipping all of them gives the conjugate reversal, so there are up to $2^{n-2}$ different solutions up to the trivial ambiguities. A zero on the unit circle gives nothing new when flipped, and in 1D almost every signal has $2^{n-2}$ different solutions.

## Variants

- **Oversampled 1D Fourier magnitude.** The definition above with $M \ge 2n - 1$. Solving it is the same as factoring a nonnegative trigonometric polynomial, and the solutions are listed by the zero flips.
- **Minimum phase.** If $x$ is known to be [minimum phase](/minimum-phase/), with every zero inside the unit circle, then the magnitude determines $x$ up to a constant phase. The log magnitude and the phase are then a [Hilbert transform](/hilbert-transform/) pair, and the [cepstrum](/cepstrum/) computes the phase.
- **Two and more dimensions.** For images, the polynomial in two variables is irreducible for almost every signal, so the magnitude generically determines the image up to the trivial ambiguities (Hayes 1982). Uniqueness does not make the computation easy; the iterations below are the standard tools.
- **Support and sign constraints.** A known support, a real or nonnegative signal, or a known part of the signal reduce the set of solutions.
- **STFT magnitude.** The data are the magnitudes $|X_m[k]|$ of a [short-time Fourier transform](/short-time-fourier-transform/) with overlapping windows. The overlap ties the frames together, and for suitable windows the signal is determined up to a global sign or phase. The [Griffin-Lim algorithm](/griffin-lim-algorithm/) is the classical method.
- **Generalized phase retrieval.** The data are $|\langle a_i, x \rangle|$ for chosen or random vectors $a_i$, for example several masked Fourier transforms. Random measurements in a number proportional to $n$ make the problem well posed and allow methods with guarantees.

## Examples

**Two real signals with the same magnitude.** Take $x = [1, 5, 6]$, so $X(z) = (1 + 2z^{-1})(1 + 3z^{-1})$ with zeros $-2$ and $-3$. Flip the zero $-2$: the factor $1 + 2z^{-1}$ becomes $z^{-1} + 2$, and $(2 + z^{-1})(1 + 3z^{-1}) = 2 + 7z^{-1} + 3z^{-2}$. So $y = [2, 7, 3]$. Both have the autocorrelation

$$r = [6, 35, 62, 35, 6] \quad (k = -2, \ldots, 2),$$

for example $1^2 + 5^2 + 6^2 = 62 = 2^2 + 7^2 + 3^2$ and $1 \cdot 5 + 5 \cdot 6 = 35 = 2 \cdot 7 + 7 \cdot 3$. At $\omega = 0$ both magnitudes are $12$, and at $\omega = \pi$ both are $2$. No shift, reversal or sign maps $x$ to $y$. A search over all integer signals of length 3 with entries in $-7 \ldots 7$ and nonzero ends finds exactly 8 with this autocorrelation: $\pm[1, 5, 6]$, $\pm[6, 5, 1]$, $\pm[2, 7, 3]$ and $\pm[3, 7, 2]$. These are the $2^{n-2} = 2$ classes times the trivial sign and reversal.

**Reversal alone is not trivial for complex signals.** For $x = [1, i]$ the autocorrelation at lag 1 is $x[1]\, \overline{x[0]} = i$. The plain reversal $[i, 1]$ has $1 \cdot \bar{i} = -i$, a different magnitude: $|X(e^{i\omega})|^2 = 2 + 2\sin\omega$ against $2 - 2\sin\omega$. The conjugate reversal $[-i, 1]$ has $1 \cdot \overline{-i} = i$ and the same magnitude as $x$.

**A unit phase with rational parts.** Multiplying $x$ by $c = \frac{3}{5} + \frac{4}{5} i$ gives a signal with the same autocorrelation, because $|c|^2 = \frac{9 + 16}{25} = 1$ and $r$ is multiplied by $c \bar{c}$.

## Known algorithms

| Method | Data | What it gives |
|---|---|---|
| Spectral factorization | 1D magnitude, $M \ge 2n - 1$ | all solutions: compute $r$, find the $2n - 2$ roots of $z^{n-1} \sum_k r[k] z^{-k}$, which come in pairs $a, 1/\bar a$, and pick one root of each pair; cost of one [polynomial root finding](/polynomial-root-finding/) of degree $2n - 2$, then $2^{n-2}$ choices |
| Gerchberg-Saxton (1972) | magnitudes in two planes | alternating projections; no global guarantee |
| Fienup error reduction (1982) | magnitude and a support or sign constraint | the Gerchberg-Saxton iteration for one magnitude; the error does not increase, and it often stalls |
| Fienup hybrid input-output (1982) | magnitude and support | a feedback step outside the support that escapes many stalls; no proof of convergence |
| [Griffin-Lim](/griffin-lim-algorithm/) (1984) | STFT magnitude | alternating projections with a least squares overlap-add; the distance does not increase |
| PhaseLift (Candès, Strohmer and Voroninski) | generalized measurements | lifts $x x^*$ to a matrix and solves a [semidefinite program](/semidefinite-programming/); exact recovery with high probability for random measurements |
| Wirtinger flow (Candès, Li and Soltanolkotabi) | generalized measurements | a spectral start and [gradient descent](/gradient-descent/) on a nonconvex loss; exact recovery with high probability for random measurements |

## Bounds

- **Information.** $M \ge 2n - 1$ magnitude samples carry the whole autocorrelation, and nothing more is in the data: no method can tell apart signals with the same $r$. In 1D that leaves up to $2^{n-2}$ classes of solutions, and almost every signal reaches that number.
- **Uniqueness in higher dimensions.** In two or more dimensions the magnitude determines almost every signal of finite support up to the trivial ambiguities. This is a statement about the solutions, not about the cost of finding them.
- **Iterations.** Error reduction and Griffin-Lim have errors that never increase, which is a worst case statement about each step. Neither has a bound on the number of iterations or a guarantee of reaching a solution. The behaviour of hybrid input-output is observed, not proved.
- **Random measurements.** For generalized measurements, PhaseLift and Wirtinger flow recover $x$ up to a global phase with high probability from a number of random measurements of order $n$ or $n \log n$. These are expected case bounds over the random measurements.

## Reductions

- **1D Fourier phase retrieval to root finding.** With $M \ge 2n - 1$, the inverse DFT of $|X|^2$ gives $r$, and the solutions are the polynomials whose zeros take one element of each pair $\{a, 1/\bar a\}$ of roots of $z^{n-1} R(z)$. This is spectral factorization, and the minimum-phase choice is the one used for filter design.
- **Minimum phase to the Hilbert transform.** For a minimum-phase signal, $\log|X|$ and the phase of $X$ are related by the Hilbert transform, so the phase follows from the magnitude by a linear map; the [cepstrum](/cepstrum/) computes it.
- **STFT phase retrieval to alternating projections.** The [Griffin-Lim algorithm](/griffin-lim-algorithm/) projects between the set of consistent STFTs, a linear subspace, and the set of arrays with the given magnitudes.
- **Phase retrieval as a quadratic system.** Each measurement $|\langle a_i, x \rangle|^2 = b_i$ is a quadratic equation in $x$; lifting to $X = x x^*$ makes it linear in $X$ with the constraint that $X$ has rank one, and dropping the rank constraint gives the semidefinite relaxation.

## Applications

- **X-ray crystallography and coherent diffraction imaging.** The detector records the intensity of the diffracted wave, which is the squared Fourier magnitude of the electron density. Oversampling, a known support and positivity make the image recoverable.
- **Electron microscopy and optics.** Gerchberg and Saxton used two intensity images in different planes; wavefront sensing in optics uses the same idea.
- **Astronomy.** Speckle interferometry and the alignment of telescope mirrors use Fourier magnitudes.
- **Audio.** Sound from a magnitude spectrogram, after modification or prediction by a model, by the [Griffin-Lim algorithm](/griffin-lim-algorithm/).
- **Filter design.** The minimum-phase filter with a given magnitude response is the spectral factor with all zeros inside the unit circle.

## References
