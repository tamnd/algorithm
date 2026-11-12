---
tag: 6TKMR6
kind: problem
slug: blind-source-separation
name: Blind source separation
aliases:
- cocktail party problem
- BSS
- blind signal separation
area: machine-learning/dimensionality-reduction
level: core
summary: "Recover source signals s(t) from mixtures x(t) = A s(t) when both the sources and the mixing matrix A are unknown. The answer is defined only up to order and scale."
prereqs: [covariance-matrix, whitening]
see_also: [independent-component-analysis, fastica, nonnegative-matrix-factorization, principal-component-analysis, factor-analysis, projection-pursuit, symmetric-eigenproblem]
sources:
  - paper: doi:10.1121/1.1907229
    title: E. Colin Cherry, Some experiments on the recognition of speech, with one and with two ears, Journal of the Acoustical Society of America 25(5), 1953
    locator: pp. 975 to 979 (the cocktail party problem as a question about human hearing)
  - paper: doi:10.1016/0165-1684(91)90079-X
    title: Christian Jutten and Jeanny Hérault, Blind separation of sources, part I, an adaptive algorithm based on neuromimetic architecture, Signal Processing 24(1), 1991
    locator: pp. 1 to 10 (the problem statement and the first adaptive separation rule)
  - paper: doi:10.1016/0165-1684(94)90029-9
    title: Pierre Comon, Independent component analysis, a new concept?, Signal Processing 36(3), 1994
    locator: pp. 287 to 314 (Theorem 11, identifiability when at most one source is Gaussian)
  - paper: doi:10.1109/31.76486
    title: Lang Tong, Ruey-wen Liu, Victor C. Soon and Yih-Fang Huang, Indeterminacy and identifiability of blind identification, IEEE Transactions on Circuits and Systems 38(5), 1991
    locator: pp. 499 to 509 (AMUSE, separation from one lagged covariance matrix)
  - paper: doi:10.1109/78.554307
    title: Adel Belouchrani, Karim Abed-Meraim, Jean-François Cardoso and Eric Moulines, A blind source separation technique using second-order statistics, IEEE Transactions on Signal Processing 45(2), 1997
    locator: pp. 434 to 444 (SOBI, joint diagonalization of several lagged covariance matrices, and its identifiability condition)
  - book: isbn:9780123747266
    title: Pierre Comon and Christian Jutten (editors), Handbook of Blind Source Separation, Academic Press, 2010
    locator: Chapter 1 (the problem and its history), Chapters 3 and 4 (independence and identifiability), Chapter 7 (second-order methods)
  - book: isbn:9780471405405
    title: Aapo Hyvärinen, Juha Karhunen and Erkki Oja, Independent Component Analysis, Wiley, 2001
    locator: Chapter 7 (the cocktail party example and the ambiguities), Chapter 18 (methods using time structure), Chapter 19 (convolutive mixtures)
---

Blind source separation (BSS) is the problem of recovering $d$ unknown source signals $s_1(t), \ldots, s_d(t)$ from $m$ observed mixtures $x(t) = A s(t)$, where the mixing matrix $A$ is also unknown. The word blind means that neither the sources nor $A$ are observed, so the problem is solvable only with an assumption about the sources: that they are independent and non-Gaussian, or that they have different time structure, or that they are nonnegative or sparse. Even then, the order and the scale of the sources can never be recovered. The best-known example is the cocktail party problem: several microphones in a room record several speakers, and the task is to recover each voice. [Independent component analysis](/independent-component-analysis/) is the main family of methods, and second-order methods such as AMUSE and SOBI use time structure instead.

## In plain words

Several people talk at once in a room, and several microphones record the room. Each recording is a blend of all the voices, with a different blend for each microphone. You know the recordings only. The task is to get back each voice by itself.

Without some extra clue this cannot be done, because many different sets of voices and blends give the same recordings. The usual clues are that the voices are independent of each other and do not sound like random hiss, or that each voice changes over time at its own typical speed. Even with a clue, you cannot tell which voice is first, or how loud each voice really was.

## Definition

**Input.** Observations $x(1), \ldots, x(n) \in \mathbb{R}^m$, from the instantaneous linear model
$$ x(t) = A s(t) , \qquad t = 1, \ldots, n , $$
with $A$ an unknown $m \times d$ matrix of full column rank ($m \ge d$) and $s(t) \in \mathbb{R}^d$ unknown.

**Output.** A $d \times m$ matrix $B$ such that $y(t) = B x(t)$ recovers the sources. Since $A s = (A \Pi^{\top} D^{-1})(D \Pi s)$ for every permutation $\Pi$ and invertible diagonal $D$, the success criterion is
$$ B A = \Pi D . $$
The usual convention fixes the scale with $\operatorname{Var}(s_i) = 1$, which leaves only the order and the signs free.

**Assumptions.** The model alone is not enough. Each standard assumption gives a different version of the problem.

- **Independent, non-Gaussian, i.i.d. sources.** The samples $s(t)$ are independent copies of a vector with independent components. Then $B A = \Pi D$ is reachable if and only if at most one source is Gaussian (Comon 1994, Theorem 11). This is the ICA version.
- **Uncorrelated sources with different spectra.** Each $s_i$ is a stationary time series, the sources are mutually uncorrelated at all lags, and the autocorrelation functions $r_i(\tau) = E[s_i(t) s_i(t + \tau)]$ differ. Then second-order statistics are enough, and the sources may be Gaussian.
- **Nonstationary sources.** The variances of the sources change over time in different ways. Joint diagonalization of covariance matrices from several time windows separates them.
- **Nonnegative or sparse sources.** Nonnegative sources and mixing (spectra, images) or sparse sources lead to [nonnegative matrix factorization](/nonnegative-matrix-factorization/) and sparse component analysis, which are not limited to $m \ge d$.

## Variants

- **Noisy BSS.** $x(t) = A s(t) + \varepsilon(t)$. Noise can be partly removed by a PCA step that keeps $d$ components, but separation is then biased.
- **Underdetermined BSS.** Fewer sensors than sources ($m < d$). Linear unmixing is impossible because $A$ has a null space; methods use sparsity, for example by assigning each time-frequency point to one source.
- **Convolutive BSS.** $x(t) = \sum_{\tau} A_{\tau} s(t - \tau)$, the model of a real room with echoes. In the frequency domain it becomes one instantaneous complex problem per frequency, with a different permutation at each frequency that must be aligned.
- **Single-channel separation.** $m = 1$, for example one microphone. This needs strong models of the sources, such as spectral dictionaries or trained neural networks.
- **Nonlinear BSS.** $x = f(s)$ for an unknown nonlinear $f$. Without restrictions on $f$ or extra information, it is not identifiable: Hyvärinen and Pajunen showed in 1999 that nonlinear ICA has infinitely many solutions.
- **Semi-blind separation.** Some sources or part of $A$ are known, for example a reference signal for a known artifact.

## Examples

**Two Gaussian time series.** Let $s_1$ and $s_2$ be autoregressive series with unit variance, $s_i(t) = \phi_i s_i(t - 1) + \sqrt{1 - \phi_i^2}\, e_i(t)$ with Gaussian $e_i$ and $\phi = (0.9, -0.5)$. Mix 5000 samples with $A = \begin{pmatrix} 1 & 0.6 \\ 0.4 & 1 \end{pmatrix}$. Each source is Gaussian at each time, so ICA has nothing to work with: [FastICA](/fastica/) on these data gives $B A \approx \begin{pmatrix} -0.49 & -0.86 \\ -0.89 & 0.48 \end{pmatrix}$, an arbitrary rotation. AMUSE whitens the data to $z = V x$, forms the symmetric lag-1 covariance $\frac12 (E[z(t) z(t+1)^{\top}] + E[z(t+1) z(t)^{\top}])$, and rotates by its eigenvectors. The eigenvalues are 0.896 and −0.498, close to the lag-1 autocorrelations 0.9 and −0.5 of the sources, and
$$ B A \approx \begin{pmatrix} -1.016 & -0.002 \\ -0.008 & 0.983 \end{pmatrix} , $$
a signed identity up to estimation error.

**Why AMUSE works.** After whitening, $z(t) = Q s(t)$ with $Q$ orthogonal, and for uncorrelated sources $E[z(t) z(t+\tau)^{\top}] = Q \operatorname{diag}(r_1(\tau), \ldots, r_d(\tau)) Q^{\top}$. This is an eigendecomposition. If the $r_i(\tau)$ are distinct, the eigenvectors are unique up to sign, so they are the columns of $Q$.

**Two i.i.d. non-Gaussian sources.** A uniform source and a Laplace source mixed by a rotation have no time structure, so AMUSE fails, but the kurtosis contrast of ICA finds them; see the example on the [ICA page](/independent-component-analysis/).

## Known algorithms

| method | assumption used | idea |
|---|---|---|
| Jacobi ICA (Comon 1994) | independence, non-Gaussianity | whiten, then rotate pairs to maximize the sum of squared kurtoses |
| [FastICA](/fastica/) (1997) | independence, non-Gaussianity | fixed-point iteration on a negentropy approximation |
| Infomax (Bell and Sejnowski 1995) | independence, a source density model | gradient ascent on the likelihood, natural gradient form |
| JADE (Cardoso and Souloumiac 1993) | independence, fourth-order cumulants | joint diagonalization of cumulant matrices |
| AMUSE (Tong et al. 1991) | different autocorrelation at one lag | eigendecomposition of one lagged covariance after whitening |
| SOBI (Belouchrani et al. 1997) | different autocorrelation functions | joint diagonalization of several lagged covariances |
| [NMF](/nonnegative-matrix-factorization/) | nonnegative sources and mixing | factor the data matrix into nonnegative parts |

AMUSE needs one [symmetric eigendecomposition](/symmetric-eigenproblem/) after whitening, and costs $O(n d^2 + d^3)$. SOBI replaces it with approximate joint diagonalization by Jacobi rotations over $K$ lags, $O(n d^2 K + S K d^3)$ for $S$ sweeps. The ICA methods cost about the same per iteration.

## Bounds

These are limits of identifiability, not of computation.

- **Order and scale.** No method can recover them: the distribution of $x$ is the same for $(A, s)$ and $(A \Pi^{\top} D^{-1}, D \Pi s)$.
- **Two Gaussian i.i.d. sources.** If $s_i$ and $s_j$ are independent standard Gaussians, then for every rotation $R$ in their plane, $R (s_i, s_j)$ is again a pair of independent standard Gaussians. So $(A, s)$ and $(A R^{\top}, R s)$ give the same data distribution, and the two sources cannot be told apart from a rotation of them.
- **Equal spectra.** If two sources have the same autocorrelation at every lag in use, the same rotation argument makes them inseparable by second-order methods. SOBI separates $s_i$ and $s_j$ if and only if $r_i(\tau) \ne r_j(\tau)$ for at least one lag $\tau$ in its set.
- **Fewer sensors than sources.** With $m < d$, no linear $B$ can recover $d$ sources, because $B A$ has rank at most $m$.
- **Statistical accuracy.** For the ICA version, the estimation error of $B A$ around $\Pi D$ shrinks as $O(n^{-1/2})$ and depends on the source densities; Gaussian-like sources give large errors.

## Reductions

- **To ICA.** For i.i.d. sources, BSS is exactly the ICA estimation problem. After whitening, both reduce to a search over orthogonal matrices.
- **To joint diagonalization.** For time-structured sources, whitening reduces BSS to finding one orthogonal $Q$ that diagonalizes a set of symmetric matrices $C_{\tau} = Q \Lambda_{\tau} Q^{\top}$. With one matrix this is the symmetric eigenproblem.
- **Convolutive to instantaneous.** A short-time Fourier transform turns a convolutive mixture into one complex instantaneous mixture per frequency bin.
- **Single-direction search.** Finding one source at a time is [projection pursuit](/projection-pursuit/) with a non-Gaussianity index.

## Applications

- **Biomedical signals.** Removal of eye blink, muscle and heartbeat artifacts from EEG and MEG, and extraction of a fetal ECG from electrodes on the mother.
- **Audio.** Separation of instruments or voices from several microphones, usually in the convolutive version.
- **Telecommunications.** Blind beamforming in antenna arrays, and the separation of users who share a channel.
- **Imaging.** Spatial ICA of fMRI, and spectral unmixing of hyperspectral images with nonnegative methods.
- **Finance and science.** Factors in returns, and the separation of foregrounds in sky maps of the cosmic microwave background.

## References
