---
tag: 7S6MFP
kind: problem
slug: blind-equalization
name: Blind equalization
aliases:
- self-recovering equalization
area: communications/channel-estimation-and-equalization
level: core
summary: "Equalize a channel from its output alone, with known symbol statistics and no training. Symbol-rate second-order statistics are not enough: use higher orders or oversampling."
prereqs: [channel-equalization]
see_also: [constant-modulus-algorithm, sato-algorithm, tong-xu-kailath-identification, subspace-channel-identification, adaptive-equalization, fractionally-spaced-equalizer, independent-component-analysis, channel-estimation]
sources:
  - paper: "Yoichi Sato, A method of self-recovering equalization for multilevel amplitude-modulation systems, IEEE Transactions on Communications 23(6), 1975, pages 679 to 682"
    locator: "the first statement of the problem and the first blind equalizer"
  - paper: "Albert Benveniste, Maurice Goursat and Gabriel Ruget, Robust identification of a nonminimum phase system: blind adjustment of a linear equalizer in data communications, IEEE Transactions on Automatic Control 25(3), 1980, pages 385 to 399"
    locator: "the identifiability of a nonminimum-phase channel from a non-Gaussian input, and the failure for a Gaussian input"
  - paper: "Ofir Shalvi and Ehud Weinstein, New criteria for blind deconvolution of nonminimum phase systems (channels), IEEE Transactions on Information Theory 36(2), 1990, pages 312 to 321"
    locator: "the necessary and sufficient condition on the variance and the kurtosis of the output"
  - paper: doi:10.1109/18.312157
    title: "Lang Tong, Guanghan Xu and Thomas Kailath, Blind identification and equalization based on second-order statistics: a time domain approach, IEEE Transactions on Information Theory 40(2), 1994, pages 340 to 349"
    locator: "identifiability from second-order statistics of an oversampled output when the subchannels have no common zero"
  - paper: doi:10.1109/26.99137
    title: "Zhi Ding, Rodney A. Kennedy, Brian D. O. Anderson and C. Richard Johnson, Jr., Ill-convergence of Godard blind equalizers in data communication systems, IEEE Transactions on Communications 39(9), 1991, pages 1313 to 1327"
    locator: "local minima of the Godard cost for FIR equalizers"
  - paper: doi:10.1002/j.1538-7305.1985.tb00040.x
    title: "G. J. Foschini, Equalizing without altering or detecting data, AT&T Technical Journal 64(8), 1985, pages 1885 to 1911"
    locator: "convergence of the Godard algorithm for an ideal equalizer of unbounded length"
  - paper: doi:10.1109/5.720246
    title: "C. Richard Johnson, Jr., Philip Schniter, Thomas J. Endres, James D. Behm, Donald R. Brown and Raul A. Casas, Blind equalization using the constant modulus criterion: a review, Proceedings of the IEEE 86(10), 1998, starting at page 1927"
    locator: "a review of the problem, the CM criterion and its use with fractionally spaced equalizers"
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Chapter 10 (adaptive equalization), the section on blind equalization"
---

Blind equalization is the problem of removing [intersymbol interference](/intersymbol-interference/) when the receiver knows neither the channel nor any of the transmitted symbols. It knows only the statistics of the symbols, such as the alphabet and that the symbols are independent. The answer can only be found up to the symmetries of those statistics: an unknown delay, and an unknown phase or sign. This page is the problem. The algorithms that solve it are on their own pages, and they differ in the statistics they use. The [Sato algorithm](/sato-algorithm/) and the [constant modulus algorithm](/constant-modulus-algorithm/) adapt an equalizer online with a nonlinear error, which uses statistics of order higher than two. [Tong-Xu-Kailath identification](/tong-xu-kailath-identification/) and [subspace identification](/subspace-channel-identification/) estimate the channel in one batch from second-order statistics, which only works with an oversampled signal or several antennas. The central fact of the problem is that second-order statistics at one sample per symbol do not determine the channel.

## In plain words

Normally a receiver learns the echoes of a channel from a known training signal. Sometimes there is none: a receiver joins a broadcast late, or a training signal would cost too much time. The receiver must then learn the echoes from the received signal alone. It can use what it knows about the symbols, for example that they come from a small set of values and are independent. This is enough to undo the echoes, but never enough to know the absolute delay or the absolute rotation of the signal. The average power and the correlations of the signal are not enough, because two different channels can give the same ones. Methods look at the shape of the signal values, or they take more than one sample per symbol.

## Definition

**Input.** Received samples $y[0], \ldots, y[K-1]$ with
$$y[k] = \sum_{l=0}^{L-1} h_l\, a[k-l] + w[k], \qquad w[k] \sim \mathcal{CN}(0, N_0) \text{ independent},$$
and the statistics of the symbols: they are independent and identically distributed, with zero mean, known variance and known higher moments, for example a uniform choice from a known constellation. The channel $h$ and the symbols are unknown.

**Output.** Either an equalizer $c$ of $N$ taps, with output $z[k] = \sum_i c_i\, y[k-i]$, or an estimate $\hat h$ of the channel. The goal for the equalizer is a combined response $g = c * h$ close to $\alpha\, e_d$, where $e_d$ is a unit vector at some delay $d$ and $\alpha$ is in the symmetry group of the alphabet. For a circular alphabet such as QAM or PSK the phase is unknown; for square QAM, the per-axis methods find the phase up to a multiple of 90 degrees; for real PAM, the sign is unknown. The goal for an identifier is $\hat h = \beta h$ for an unknown scalar $\beta$. The quality is measured by the residual ISI $(\sum_k |g_k|^2 - \max_k |g_k|^2) / \max_k |g_k|^2$ or by the symbol error rate after the delay and phase are resolved.

**Why the ambiguity cannot be removed.** If $a$ is a valid symbol sequence, so is $\alpha\, a[k - d]$ for any $\alpha$ in the symmetry group and any $d$, with the same statistics. The channel $h$ and the channel $\alpha^{-1} h$ shifted by $d$ produce the same output from these two inputs. So no method can tell them apart.

## Variants

- **Online or batch.** Adaptive methods such as Sato and CMA update an equalizer at every sample and track slow changes. Batch methods estimate the channel from a block of statistics.
- **Equalization or identification.** Some methods return the equalizer taps directly. Others return $\hat h$, and a nonblind equalizer is then designed for it.
- **Symbol rate or oversampled.** At one sample per symbol, the received signal is stationary, and its second-order statistics determine only $|H(e^{j\omega})|$. Sampling $P \ge 2$ times per symbol, or using $P$ antennas, gives $P$ subchannels and a cyclostationary signal, whose second-order statistics are enough.
- **Real or complex.** PAM has a sign ambiguity; QAM and PSK have a phase ambiguity that a later [carrier recovery](/carrier-recovery/) stage, or a per-axis error, must resolve.
- **Semi-blind.** A few known pilots fix the ambiguity and help the convergence, while the unknown data supplies most of the statistics.
- **Blind sequence estimation.** Estimate the channel and the symbol sequence together by maximum likelihood, for example by [expectation maximization](/expectation-maximization/) or [per-survivor processing](/per-survivor-processing/).

## Examples

**Second-order statistics at symbol rate are not enough.** Take BPSK symbols $a \in \{\pm 1\}$, no noise, and the channels $h = (1, 0.5)$ and $h' = (0.5, 1)$. Both outputs have the autocorrelation $r(0) = 1.25$ and $r(\pm 1) = 0.5$, and $r(m) = 0$ for $|m| \ge 2$. So their power spectra are equal, and no method that uses only correlations can tell them apart. The first channel is minimum phase (zero at $-0.5$), the second is maximum phase (zero at $-2$), and their inverses are very different.

**Fourth-order statistics separate them.** The fourth cumulant of BPSK is $\kappa_4 = E a^4 - 3 (E a^2)^2 = -2$. For a real channel, $\mathrm{cum}(y[k], y[k], y[k], y[k+1]) = \kappa_4 \sum_l h_l^3 h_{l+1}$. This is $-2 \times 0.5 = -1$ for $h$ and $-2 \times 0.125 = -0.25$ for $h'$. So a method that uses fourth-order statistics, such as CMA, can tell the two channels apart.

**Oversampling also separates them.** Sample twice per symbol and suppose the two subchannels are $h^{(1)} = (1, 0.5)$ and $h^{(2)} = (0.5, 1)$. Their zeros, $-0.5$ and $-2$, differ, so the subchannels have no common zero and the Tong-Xu-Kailath theorem says that the correlations at lags 0 and 1 determine the pair up to one scalar. If instead $h^{(2)} = (2, 1)$, both subchannels have the zero $-0.5$, and flipping that zero to $-2$ in both changes the channel but not the correlations.

**A local minimum.** For $h = (1, 0.5)$ and a CMA equalizer of two taps, the [CMA page](/constant-modulus-algorithm/) finds a local minimum of the cost with residual ISI 0.236, worse than the global minimum. A blind method that descends a cost can stop there.

## Known algorithms

| algorithm | statistics | cost | notes |
|---|---|---|---|
| [Sato algorithm](/sato-algorithm/) (1975) | higher order, through a sign | $O(N)$ per sample | PAM, or square QAM per axis; finds the phase up to 90 degrees |
| [Constant modulus algorithm](/constant-modulus-algorithm/) (Godard 1980) | fourth order | $O(N)$ per sample | the most used; ignores the phase; local minima |
| Shalvi-Weinstein kurtosis criteria (1990) | second and fourth order | $O(N)$ per sample, or batch | maximize the output kurtosis at fixed power |
| [Tong-Xu-Kailath identification](/tong-xu-kailath-identification/) (1991) | second order, oversampled | one eigenvalue problem per block | needs no common zero of the subchannels |
| [Subspace identification](/subspace-channel-identification/) (Moulines and others 1995) | second order, oversampled | one eigenvalue problem per block | uses the noise subspace of the stacked covariance |
| blind maximum-likelihood sequence estimation | the full likelihood | exponential in the channel memory | joint estimate of $h$ and the symbols |

After a blind method opens the eye, receivers usually switch to decision-directed [adaptive equalization](/adaptive-equalization/), which has a smaller steady-state error.

## Bounds

**Gaussian inputs cannot be equalized blindly.** If the symbols are Gaussian, all their statistics follow from the second-order ones, so the output statistics depend only on $|H(e^{j\omega})|$, and a nonminimum-phase channel cannot be identified. Benveniste, Goursat and Ruget (1980) showed that a non-Gaussian independent input is enough: if the output of $g$ has the same distribution as the input, then $g$ is a scaled delay. This is a theorem.

**How many channels share a spectrum.** A channel of length $L$ has $L - 1$ zeros. Replacing a zero $z_i$ by $1/\bar z_i$ and rescaling keeps $|H(e^{j\omega})|$, so up to $2^{L-1}$ channels of length $L$ have the same symbol-rate second-order statistics. This is a closed form fact.

**The Shalvi-Weinstein condition.** For an independent input with nonzero kurtosis, if the output has the same variance as the input and the same absolute kurtosis, then $g = \alpha e_d$ with $|\alpha| = 1$. This is a theorem, and it is the basis of the kurtosis methods.

**Oversampled identifiability.** With $P \ge 2$ subchannels and a white input, the channel is determined by the output correlations up to one scalar if and only if the subchannels have no common zero (and the window is long enough). This is the theorem of Tong, Xu and Kailath; the subspace method has the same condition.

**Convergence.** No general global convergence theorem exists for finite equalizers of the Sato or CMA type. Ding, Kennedy, Anderson and Johnson (1991) showed that the Godard cost of an FIR equalizer can have local minima with large residual ISI. For an equalizer of unbounded length the picture is better: Foschini (1985) showed that the Godard algorithm then converges to a perfect equalizer.

## Reductions

- **Blind identification then nonblind equalization.** An estimate $\hat h = \beta h$ reduces the problem to [channel equalization](/channel-equalization/) with a known channel, apart from the scalar $\beta$, which a few pilots or a carrier recovery stage fix.
- **Blind deconvolution and source separation.** Stacking the samples gives $y = H a + w$ with a Toeplitz matrix $H$ and independent entries of $a$, so blind equalization is a structured case of [independent component analysis](/independent-component-analysis/), and kurtosis criteria are shared by both.
- **Oversampled identification and common zeros.** Two subchannels with no common zero means that their polynomials have a [greatest common divisor](/polynomial-gcd/) of degree 0, which is the same as a nonzero [resultant](/resultant/), the determinant of their [Sylvester matrix](/sylvester-matrix/).
- **Fractionally spaced equalizers.** A [fractionally spaced equalizer](/fractionally-spaced-equalizer/) sees $P$ subchannels, so a blind method run on it inherits the oversampled identifiability. For CMA, this removes the local minima under conditions given in the review by Johnson and others (1998).

## Applications

Godard designed blind equalization for multipoint data networks, where a terminal must start receiving without asking the sender for a training sequence. The same need arises in broadcast systems, where a receiver can tune in at any time, and in links where a training sequence would cost too much of the frame. Passive receivers that monitor a signal not meant for them have no training at all. In most receivers a blind stage, usually CMA, opens the eye, and decision-directed adaptation then takes over.

## References
