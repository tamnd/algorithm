---
tag: 3Z45PV
kind: technique
slug: compressed-sensing
name: Compressed sensing
aliases:
- compressive sensing
area: graphics-and-signals/signal-processing
level: advanced
summary: Take few random linear measurements of a signal that is sparse in a known basis, then recover it by l1 minimization or a greedy sparse solver.
prereqs: [sparse-signal-recovery, restricted-isometry-property, basis-pursuit]
see_also: [orthogonal-matching-pursuit, iterative-shrinkage-thresholding, johnson-lindenstrauss-lemma, sampling-theorem, nyquist-rate, discrete-wavelet-transform, total-variation-denoising, sparse-fourier-transform]
sources:
  - paper: doi:10.1109/TIT.2005.862083
    title: Emmanuel J. Candès, Justin Romberg and Terence Tao, Robust uncertainty principles, exact signal reconstruction from highly incomplete frequency information, IEEE Transactions on Information Theory 52(2), 2006
    locator: pages 489 to 509 (exact recovery of a sparse signal from a random set of its Fourier coefficients by l1 or total variation minimization)
  - paper: doi:10.1109/TIT.2006.871582
    title: David L. Donoho, Compressed sensing, IEEE Transactions on Information Theory 52(4), 2006
    locator: pages 1289 to 1306 (the name, and recovery of compressible signals from a number of measurements of order s log n by l1 minimization)
  - paper: doi:10.1109/TIT.2005.858979
    title: Emmanuel J. Candès and Terence Tao, Decoding by linear programming, IEEE Transactions on Information Theory 51(12), 2005
    locator: pages 4203 to 4215 (the restricted isometry constants as the condition on the measurement matrix)
  - paper: doi:10.1007/s00365-007-9003-x
    title: Richard Baraniuk, Mark Davenport, Ronald DeVore and Michael Wakin, A simple proof of the restricted isometry property for random matrices, Constructive Approximation 28(3), 2008
    locator: pages 253 to 263 (random Gaussian and Bernoulli matrices with order s log(n/s) rows satisfy the restricted isometry property)
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhäuser, 2013
    locator: the chapters on sparse recovery with random matrices and on random sampling in bounded orthonormal systems
---

Compressed sensing is a technique for acquiring a signal of length $n$ that is sparse in a known basis with $m \ll n$ linear measurements, and for recovering it by solving a [sparse signal recovery](/sparse-signal-recovery/) problem. The measurements are random, or incoherent with the sparsity basis, so that the measurement matrix has the [restricted isometry property](/restricted-isometry-property/) with high probability. Then $m$ of order $s\log(n/s)$ measurements are enough for every $s$-sparse signal, and [basis pursuit](/basis-pursuit/) recovers it exactly without noise and stably with noise. It replaces "sample fast, then compress" by "measure only what the compressed form needs".

## In plain words

A camera takes millions of pixel values and then throws most of the information away when it compresses the image. Compressed sensing asks whether the camera could measure only a little in the first place.

The answer is yes when the signal is simple in some known way, for example when a few wavelet patterns describe it well. Each measurement is a weighted sum of all signal values, with weights picked at random. Random weights spread the information of every simple signal over all the measurements, so no simple signal is missed.

A computer then searches for the simplest signal that agrees with the measurements. That search has a fast and reliable form when the measurements are random, and it finds the true signal. The number of measurements grows with how simple the signal is, not with its length.

## When it applies

- **The signal is sparse or compressible in a known basis.** There is an orthonormal basis or frame $\Psi$ with $x = \Psi z$, and $z$ has at most $s$ large entries. Wavelets for images ([discrete wavelet transform](/discrete-wavelet-transform/)), the Fourier basis for signals with few tones, and gradients for piecewise constant images are the usual choices.
- **The measurements are linear and you can design them.** Each measurement is $\langle \phi_i, x\rangle + e_i$, and the vectors $\phi_i$ are yours to choose: random patterns, random rows of a Fourier matrix, or random modulation before a slow sampler.
- **Measurements are expensive and computation is cheap.** Scan time in medical imaging, the number of detectors, the energy of each sample, or the rate of an analog-to-digital converter limits the system, while recovery can run afterwards on a computer.
- **The sensing vectors are incoherent with $\Psi$.** For orthonormal $\Phi$ and $\Psi$, the coherence $\mu(\Phi, \Psi) = \sqrt n \max_{k, j}|\langle \phi_k, \psi_j\rangle|$ lies in $[1, \sqrt n]$. Small values mean that every sensing vector is spread out in the sparsity basis. Spikes and sinusoids give $\mu = 1$, the best case.
- **The noise is bounded or of known size.** The decoder needs a bound $\|e\|_2 \le \varepsilon$ or a penalty tuned to the noise.

## The template

```pseudo id=main
COMPRESSED-SENSING(x, Ψ, s, ε)
L1  m ← C · s · log(n / s)                       ▷ C is a moderate constant
L2  draw Φ ∈ ℝ^{m×n} at random                  ▷ Gaussian or ±1 entries over √m, or m random rows of a Fourier matrix
L3  measure y ← Φ x + e                          ▷ the hardware forms the m sums; x itself is never stored
L4  A ← Φ Ψ                                      ▷ measurements of the sparse coefficients z, with x = Ψ z
L5  ẑ ← argmin ‖z‖₁ subject to ‖A z − y‖₂ ≤ ε    ▷ or OMP, iterative thresholding, CoSaMP
L6  return x̂ ← Ψ ẑ
```

Lines L1 to L3 are the acquisition, and lines L4 to L6 are the decoding. Only line L3 touches the signal.

**Why random matrices work.** For line L5 to succeed for every $s$-sparse $z$, $A$ needs a small restricted isometry constant $\delta_{2s}$. A Gaussian matrix with $m \ge C s\log(n/s)$ rows has $\delta_{2s} \le \delta$ with probability at least $1 - 2e^{-cm}$, where $C$ and $c$ depend on $\delta$ (Baraniuk and others 2008). If $\Psi$ is orthonormal and $\Phi$ is Gaussian, then $\Phi\Psi$ is Gaussian too, because the Gaussian distribution is invariant under rotations. So one random design works for every sparsity basis, and the designer does not need to know $\Psi$ when building the hardware. The proof is a [concentration inequality](/concentration-of-measure/) for one vector, as in the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/), with a union bound over a net of each $s$-dimensional coordinate subspace.

**What the decoder guarantees.** Under a small $\delta_{2s}$, the solution of line L5 obeys $\|\hat z - z\|_2 \le C_0\,\sigma_s(z)_1/\sqrt s + C_1\varepsilon$, where $\sigma_s(z)_1$ is the $\ell_1$ error of the best $s$-term approximation. The constants and the proof are on the [basis pursuit](/basis-pursuit/) page. So the error is zero for exactly sparse $z$ and no noise, it degrades gracefully for compressible $z$, and it is proportional to the noise level.

**How many measurements.** The count $s\log(n/s)$ is optimal up to the constant: any stable decoder needs $m \ge c\,s\log(en/s)$, as the bounds on the [sparse signal recovery](/sparse-signal-recovery/) page show. Compared with the $n$ samples that the [sampling theorem](/sampling-theorem/) asks for, the gain is large when $s \ll n$. For $m$ random rows of an orthonormal $\Phi$, the count grows to order $\mu(\Phi, \Psi)^2\, s \log n$, up to powers of the logarithm, so incoherence is what makes the structured case work.

**Example.** Let $n = 10$, $m = 5$, and let $\Psi$ be the identity, so $x$ itself is sparse. Take the $\pm 1$ matrix

$$A = \begin{pmatrix}
1 & -1 & -1 & -1 & -1 & 1 & -1 & 1 & 1 & 1 \\
1 & -1 & -1 & 1 & 1 & 1 & 1 & 1 & -1 & -1 \\
-1 & 1 & -1 & -1 & 1 & -1 & 1 & 1 & 1 & 1 \\
1 & -1 & 1 & -1 & -1 & -1 & 1 & 1 & 1 & -1 \\
1 & 1 & 1 & 1 & 1 & 1 & -1 & -1 & 1 & -1
\end{pmatrix},$$

which Python's `random.Random(21)` draws row by row. Its columns have norm $\sqrt5$, and the largest $|\langle a_i, a_j\rangle|$ is $3$, so the coherence is $\tfrac35$. Let $x_0 = 3e_3 - 2e_8$. Then $y = Ax_0 = (-5, -5, -5, 1, 5)$.

- **The minimum energy answer is wrong.** The solution of $Ax = y$ with the least $\ell_2$ norm, $A^{\mathsf T}(AA^{\mathsf T})^{-1}y$, has all $10$ entries nonzero, $\ell_1$ norm $\tfrac{1055}{138} \approx 7.64$ and squared norm $\tfrac{2651}{276} \approx 9.61$, less than $\|x_0\|_2^2 = 13$.
- **The $\ell_1$ answer is right.** The minimizer of $\|x\|_1$ subject to $Ax = y$ is unique and equals $x_0$, with $\ell_1$ norm $5$. Among the other solutions whose nonzero columns are independent, the smallest $\ell_1$ norm is $7$.

The coherence bound $\mu < 1/(2s - 1) = \tfrac13$ fails here, so no theorem promises this instance. The guarantee for random matrices is statistical, and at this tiny size it holds only for some draws.

## Classic examples

- **Magnetic resonance imaging.** The scanner measures Fourier coefficients of the image, one line or point of the frequency plane at a time, and scan time grows with their number. Images are compressible in wavelets and have sparse gradients. Sampling the frequency plane at random, more densely near the center, and decoding with $\ell_1$ on the wavelet coefficients or [total variation](/total-variation-denoising/), gives images from a fraction of the usual samples. Candès, Romberg and Tao (2006) proved exact recovery from random Fourier samples for this kind of model.
- **The single-pixel camera.** An array of tiny mirrors shows a random binary pattern, and one light sensor measures the inner product of the scene with that pattern. Repeating with $m$ patterns gives $y = \Phi x$. This makes cameras practical at wavelengths where large sensor arrays are expensive.
- **Signals with few tones.** A signal with $s$ frequencies in a band of width $W$ has a sparse spectrum. Random time samples, or a random sign modulation followed by a slow sampler, give enough information to recover it at an average rate far below the [Nyquist rate](/nyquist-rate/) $2W$. The [sparse Fourier transform](/sparse-fourier-transform/) is a related idea, where the samples are chosen by the algorithm itself.
- **Sensor networks and channel estimation.** Each node sends a few random combinations of the readings, and a center decodes them. A wireless channel with few strong paths is a sparse vector of delays, estimated from a short known pilot signal.

## Variations

- **Decoders.** Basis pursuit denoising (line L5), the [lasso](/lasso-regression/) solved by [iterative shrinkage-thresholding](/iterative-shrinkage-thresholding/), [orthogonal matching pursuit](/orthogonal-matching-pursuit/), CoSaMP and iterative hard thresholding all fit line L5. Greedy and thresholding decoders are faster, and $\ell_1$ decoders recover from fewer measurements in practice.
- **Analysis sparsity.** Minimize $\|\Omega x\|_1$ subject to $\|\Phi x - y\| \le \varepsilon$, where $\Omega$ is a redundant transform or a finite difference operator. Total variation is the main case for images.
- **Structured sparsity.** Wavelet coefficients of natural images lie on trees, and some signals have blocks of nonzeros. Decoders that use the structure need fewer measurements, about $s$ instead of $s\log(n/s)$ in some models.
- **Structured random matrices.** Random rows of a Fourier or Hadamard matrix, random convolutions, and sparse random matrices allow fast products in the decoder, at the cost of extra logarithmic factors in $m$.
- **Low-rank matrices.** Replace "sparse vector" by "low-rank matrix" and the $\ell_1$ norm by the nuclear norm, the sum of the singular values. The same template recovers a matrix from few random linear measurements, or from a random subset of its entries.
- **One-bit measurements.** Keep only the sign of each measurement. The direction of $x$ can still be recovered, but its scale is lost.

## Pitfalls

- **Coherent sensing.** Point samples of a signal that is sparse in the standard basis miss every spike that is not sampled. With $m$ of $n$ positions sampled at random, a given spike is missed with probability $1 - m/n$. The sensing vectors must be spread out in the sparsity basis.
- **Model mismatch.** A tone between two frequencies of the discrete Fourier grid is not sparse in the Fourier basis, because of [spectral leakage](/spectral-leakage/). The decoder then returns many small wrong entries. Use a finer dictionary, or a decoder for frequencies off the grid.
- **Few rows of signs.** A $\pm1$ matrix with $m$ rows has at most $2^{m-1}$ different columns up to sign. With more columns than that, two columns $a_i$ and $a_j$ are parallel, $e_i \mp e_j$ is in the null space, and two different $1$-sparse vectors have the same measurements. Random draws at small $m$ already show this.
- **Noise before the measurement.** Noise added to the signal itself, not to the measurements, passes through $\Phi$ with the signal, and subsampling raises its effect on the recovery by a factor of about $n/m$. Compressed sensing saves measurements, not signal-to-noise ratio.
- **No certificate.** Checking the restricted isometry property of a given matrix is NP-hard, so a random design comes with a probability, not a proof for the drawn matrix. Coherence can be checked, but it gives only $m$ of order $s^2$.
- **Scaling and quantization.** Gaussian or $\pm1$ entries must be divided by $\sqrt m$ for the restricted isometry constants to be near $0$. Coarse quantization of $y$ adds an error that must be included in $\varepsilon$.

## Exercises

1. Let $\Phi$ have independent $N(0, 1/m)$ entries and let $\Psi$ be orthonormal. Show that $\Phi\Psi$ has the same distribution as $\Phi$.
2. For the example matrix $A$, check that $y = (-5, -5, -5, 1, 5)$, and show that the minimum $\ell_2$ norm solution $A^{\mathsf T}(AA^{\mathsf T})^{-1}y$ has no zero entries.
3. Show that the coherence of the identity and the unitary discrete Fourier basis in $\mathbb C^n$ is $1$, and that $\mu(\Phi, \Psi) \ge 1$ for any two orthonormal bases.
4. Show that a $\pm1$ matrix with $m$ rows and more than $2^{m-1}$ columns cannot recover every $1$-sparse vector by any decoder.
5. Suppose each measurement costs one unit of time and $n = 10^6$, $s = 10^3$. Compare $n$ with $s\log(n/s)$, and explain why the constant $C$ in line L1 matters for the real saving.
6. Show that if $x$ is $s$-sparse in $\Psi$ and $y = \Phi x$ exactly, then any decoder that returns the sparsest solution of $\Phi\Psi z = y$ recovers $x$ when every $2s$ columns of $\Phi\Psi$ are independent.

## References
