---
tag: EPV4TJ
kind: algorithm
slug: spectral-subtraction
name: Spectral subtraction
aliases:
- Boll spectral subtraction
area: graphics-and-signals/signal-processing
level: core
summary: "Remove additive noise frame by frame: subtract an estimate of the noise power from each short-time spectrum, keep a floor, reuse the noisy phase and overlap-add."
solves: [signal-denoising]
model: real-ram
complexity:
  vars: {N: the number of samples, L: the frame length (a power of two)}
  time: {worst: O(N log L)}
  space: {extra: O(L)}
properties: {deterministic: true, online: true, recursive: false, exact: false}
history:
  year: 1979
  people: [Steven F. Boll, Michael Berouti, Richard Schwartz, John Makhoul]
  note: "Boll published magnitude subtraction for speech in acoustic noise in 1979, and in the same year Berouti, Schwartz and Makhoul added oversubtraction and a spectral floor against the musical noise."
prereqs: [short-time-fourier-transform, signal-denoising]
see_also: [wiener-filter, overlap-add-method, window-functions, periodogram, welch-method, power-spectral-density, signal-detection, image-denoising]
sources:
  - paper: doi:10.1109/TASSP.1979.1163209
    title: "S. F. Boll, Suppression of acoustic noise in speech using spectral subtraction, IEEE Transactions on Acoustics, Speech, and Signal Processing 27(2), 1979, pages 113 to 120"
    locator: "the magnitude subtraction rule with half-wave rectification, the noise estimate from frames without speech, and the residual noise reduction"
  - paper: doi:10.1109/ICASSP.1979.1170788
    title: "M. Berouti, R. Schwartz and J. Makhoul, Enhancement of speech corrupted by acoustic noise, Proceedings of ICASSP 1979"
    locator: "the oversubtraction factor alpha and the spectral floor beta, chosen to reduce the musical noise"
  - book: isbn:9781466504219
    title: "Philipos C. Loizou, Speech Enhancement, Theory and Practice, 2nd edition, CRC Press, 2013"
    locator: "Chapter 5, Spectral-Subtractive Algorithms (the basic rule, the musical noise, oversubtraction and the floor, and the nonlinear and multiband variants)"
  - paper: doi:10.1109/TASSP.1984.1164453
    title: "Y. Ephraim and D. Malah, Speech enhancement using a minimum mean-square error short-time spectral amplitude estimator, IEEE Transactions on Acoustics, Speech, and Signal Processing 32(6), 1984, pages 1109 to 1121"
    locator: "the MMSE amplitude gain and the decision-directed estimate of the a priori SNR, which removes most of the musical noise"
---

Spectral subtraction removes additive noise from a signal $y = x + v$ in the short-time Fourier domain. It cuts $y$ into overlapping windowed frames, takes the DFT of each, and in each frequency bin subtracts an estimate $\hat N$ of the noise power, measured beforehand on a part of the recording that holds only noise. Negative results are clipped to a small floor. The method keeps the noisy phase, takes the inverse DFT, and puts the frames back together by overlap-add. Steven Boll proposed it for speech in 1979. It is cheap, needs only a noise estimate and no model of the signal, and leaves a typical artifact: isolated spectral peaks that come and go from frame to frame and sound like random tones, the "musical noise".

## In plain words

A steady noise, such as a fan or an engine, sounds the same all the time. Record a short part where only the noise is present and measure how much energy it has at each pitch. Then cut the noisy recording into short overlapping pieces. In each piece, look at the energy at each pitch, take away the energy you measured for the noise, and keep what is left. Where nothing is left, keep a small amount, so that the background does not drop to total silence. Then turn the pieces back into sound and join them. The method cannot know the noise in each piece exactly, only its average, so a few random pieces of noise stay behind.

## The problem

The input is a real signal $y[0], \ldots, y[N-1]$ with $y = x + v$, where $x$ is the wanted signal and $v$ is additive noise that is stationary, or changes slowly, and is uncorrelated with $x$. A noise-only signal of the same kind is also given, or a part of $y$ known to hold no signal. The output is an estimate $\hat x$ of $x$ of the same length. The parameters are an even frame length $L$, the oversubtraction factor $\alpha \ge 0$, the spectral floor $\beta \ge 0$ and the exponent $\gamma > 0$: $\gamma = 1$ subtracts magnitudes and $\gamma = 2$ subtracts powers. There is no stated error that the method minimizes. This is one method for the 1D [signal denoising](/signal-denoising/) problem; [image denoising](/image-denoising/) is the problem for images.

## The algorithm

The frames use the hop $H = L/2$ and the periodic Hann window $w[n] = \frac12 - \frac12 \cos(2\pi n/L)$, whose two shifted copies add up to one.

```pseudo id=main
NOISE-ESTIMATE(v, L, γ)
L1  for each frame j of v: V_j ← DFT(w · v[jH .. jH + L − 1])
L2  N̂[m] ← the mean over j of |V_j[m]|^γ, for m = 0 .. L − 1

SPECTRAL-SUBTRACTION(y, N̂, L, α, β, γ)
L3  x̂ ← 0, the length of y padded with H zeros at both ends
L4  for each frame j of the padded y do
L5      Y ← DFT(w · y[jH .. jH + L − 1])
L6      for m ← 0 to L − 1 do
L7          P ← max(|Y[m]|^γ − α N̂[m], β N̂[m])   ▷ subtract, then floor
L8          X̂[m] ← P^(1/γ) · Y[m] / |Y[m]|, or 0 if Y[m] = 0   ▷ the noisy phase
L9      x̂[jH .. jH + L − 1] ← x̂[jH .. jH + L − 1] + Re IDFT(X̂)   ▷ overlap-add
L10 return x̂ without the padding
```

Lines L1 and L2 compute the average noise spectrum, which is a [Welch](/welch-method/) estimate of the noise [power spectral density](/power-spectral-density/) for $\gamma = 2$. Lines L3 and L5 compute the [short-time Fourier transform](/short-time-fourier-transform/) of the padded signal. Line L7 is the subtraction rule. With $\alpha = 1$ and $\beta = 0$ it is Boll's rule with half-wave rectification; with $\alpha > 1$ it removes more than the average noise, so that fewer noise peaks survive, and $\beta > 0$ leaves a weak, smooth background noise in place of silence. Line L8 keeps the phase of the noisy bin, because the ear is not sensitive to it and no better estimate is available. The rule is a real gain $G = (P / |Y|^\gamma)^{1/\gamma}$ between $0$ and $1$ applied to $Y[m]$. It depends only on $|Y[m]|$ and $\hat N[m]$, which are the same for the bins $m$ and $L - m$ of a real signal, so these bins get the same gain, $\hat X$ keeps the Hermitian symmetry of $Y$, and the inverse DFT in line L9 is real. Line L9 adds the frames back by [overlap-add](/overlap-add-method/). The windows sum to one, so a frame left unchanged reconstructs the input exactly.

## Example

Take one frame with the noise estimate $\hat N[m] = 1$ in six bins, $\gamma = 2$, $\alpha = 2$ and $\beta = 1/25$. The column $G$ is the amplitude gain $|\hat X| / |Y|$.

| $\lvert Y \rvert^2$ | $\lvert Y \rvert^2 - 2 \hat N$ | $P$ (L7) | $G$ |
|---|---|---|---|
| $10$ | $8$ | $8$ | $0.894$ |
| $1$ | $-1$ | $1/25$ | $0.200$ |
| $3$ | $1$ | $1$ | $0.577$ |
| $1/2$ | $-3/2$ | $1/25$ | $0.283$ |
| $25$ | $23$ | $23$ | $0.959$ |
| $2$ | $0$ | $1/25$ | $0.141$ |

The strong bins, which hold the signal, lose little. The weak bins drop to the floor $\beta \hat N = 1/25$, which is $14$ dB below the noise level. The bin with power $3$ is a typical noise peak: three times the average noise, which happens with probability $e^{-3} \approx 5\%$ for Gaussian noise, so it survives with power $1$. This is musical noise. For white Gaussian noise alone and $\gamma = 2$, $|Y|^2 / \hat N$ has an exponential distribution with mean one, a bin survives above the floor with probability $e^{-(\alpha + \beta)}$, and the mean output power is $\hat N (\beta + e^{-(\alpha + \beta)})$. With $\alpha = 2$ and $\beta = 1/25$ this is $13.0\%$ of the bins and $17.0\%$ of the noise power, a reduction of $7.7$ dB. With $\alpha = 1$ and $\beta = 0$, $37\%$ of the noise bins survive.

## Correctness

**Claim.** If lines L7 and L8 leave the bins unchanged, as for $\alpha = \beta = 0$, the output equals $y$ exactly. For $\gamma = 2$, $\alpha = 1$ and an exact noise estimate, $|Y|^2 - \hat N$ is an unbiased estimate of the signal power in the bin. On white Gaussian noise alone, a bin survives above the floor with probability $e^{-(\alpha + \beta)}$, and the expected output power is $\hat N(\beta + e^{-(\alpha + \beta)})$.

**Key invariant.** After frame $j$ is added in line L9, every sample of $\hat x$ before $(j + 1) H$ holds its final value, which is the sum of the outputs of its two frames, weighted by two window values that add up to one.

The first claim follows from the invariant. The second holds because the cross term of signal and noise has mean zero. The third follows from the exponential law of $|Y|^2$ for a circular complex Gaussian bin, which gives the survival probability and an integral in closed form. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The padded signal has about $N + L$ samples and so about $2N / L + 2$ frames. For a power of two $L$, the forward and inverse FFT of a frame cost $O(L \log L)$ each, and lines L6 to L8 cost $O(L)$. The total is $O((N / L) \cdot L \log L) = O(N \log L)$ in the [real RAM](/real-ram/). The noise estimate costs $O(N_v \log L)$ for a noise signal of $N_v$ samples. The extra space is $O(L)$ for one frame and its spectrum, besides the input and the output. The latency is one frame, so the method runs online with a delay of $L$ samples.

## Properties

- **No model of the signal.** The method needs only the noise spectrum. It does not know what the signal looks like, and so it cannot tell a signal bin from a strong noise bin.
- **Musical noise.** The noise power in a bin is random around its mean. Bins where it is above $\alpha \hat N$ survive, at random places in every frame, as short tones. A larger $\alpha$ removes more of them and distorts more of the signal.
- **A gain between 0 and 1.** Every bin is scaled by a real gain. The method never adds energy and keeps the noisy phase, so it cannot remove the noise that falls on the signal bins.
- **Real output.** The gain depends only on $|Y[m]|$ and $\hat N[m]$, so it keeps the Hermitian symmetry, and the inverse DFT is real.
- **Relation to the Wiener filter.** For $\gamma = 2$, $\alpha = 1$ and $\beta = 0$, the amplitude gain is $\sqrt{1 - \hat N / |Y|^2}$. The [Wiener filter](/wiener-filter/) with the same power estimate $|Y|^2 - \hat N$ of the signal has the gain $1 - \hat N / |Y|^2$, which is the square of this one and attenuates more.
- **Stationary noise.** The noise estimate is fixed. If the noise changes, it must be updated, for example in the pauses that a [signal detection](/signal-detection/) step finds.

## Variants and improvements

- **Magnitude averaging.** Boll averages $|Y|$ over a few adjacent frames before the subtraction, which reduces the variance of the noise in each bin and so the musical noise, at the cost of smearing fast changes.
- **Residual noise reduction.** Boll also replaces an isolated surviving bin by the minimum of its values in the adjacent frames, which removes many short noise peaks.
- **Oversubtraction and floor.** Berouti, Schwartz and Makhoul use $\gamma = 2$, an $\alpha$ that depends on the SNR of the frame, about $4$ at $0$ dB and falling to $1$ at $20$ dB, and a floor $\beta$ of about $0.005$ to $0.1$. This is line L7 as written.
- **Generalized exponent.** Lim and Oppenheim treat $\gamma$ as a free parameter; $\gamma = 1$ and $\gamma = 2$ are the common choices.
- **Multiband subtraction.** A different $\alpha$ in each frequency band follows noise that is not white.
- **Noise tracking.** Minimum statistics and similar methods track the noise spectrum during speech, without a pause.
- **Statistical estimators.** The Ephraim-Malah MMSE amplitude estimator, with its decision-directed estimate of the SNR, gives a smoother gain and almost no musical noise. It replaced spectral subtraction in many products.

## When to use it

Use spectral subtraction to reduce stationary or slowly changing noise in speech and audio when a noise-only part is available and the computation must be cheap: hands-free telephones, hearing aids, the front end of speech recognition, and the cleanup of recordings. It is a good first method and a reference for comparison. For better quality, use a Wiener gain or the Ephraim-Malah estimator. For noise that changes fast, or noise that is another voice, use a model of the signal or a learned method. For images, see [image denoising](/image-denoising/).

## Pitfalls

- **No floor.** Line L7 written as $P \leftarrow |Y|^\gamma - \alpha \hat N$ gives negative powers, and their root is not real. Write $P \leftarrow \max(|Y|^\gamma - \alpha \hat N, \beta \hat N)$, with $\beta = 0$ for plain half-wave rectification.
- **A zero floor with oversubtraction.** With a large $\alpha$ and $\beta = 0$ in line L7, the background is silent between the surviving noise peaks, and the musical noise is easier to hear. Use $\beta > 0$ so that a weak smooth noise masks the peaks.
- **Mixed units.** Line L7 must subtract $\hat N$ in the same units as $|Y|^\gamma$. Line L2 must average $|V_j|^\gamma$, not $|V_j|$, and the noise frames must use the same window and frame length as line L5. A power estimate subtracted from magnitudes removes far too much or too little.
- **Windows that do not add up to one.** Line L9 with a window whose shifts do not sum to a constant at hop $H$, such as a symmetric Hann window of length $L$, modulates the output even when nothing is subtracted. Use the periodic Hann window with $H = L/2$, or divide by the sum of the windows.
- **No padding at the ends.** Line L3 without the $H$ zeros at each end covers the first and last $H$ samples by one frame only, so they come out scaled by the window. Pad, or divide by the window sum there.
- **Taking the real part of a rule that breaks symmetry.** A rule in line L8 that gives the bins $m$ and $L - m$ different gains makes the inverse DFT complex, and taking its real part in line L9 hides the error. Use a gain that depends only on $|Y[m]|$ and $\hat N[m]$.

## Implementations

## History

Steven Boll published spectral subtraction in 1979 in the IEEE Transactions on Acoustics, Speech, and Signal Processing, with magnitude subtraction, half-wave rectification, magnitude averaging and a step that removes isolated residual peaks. In the same year Berouti, Schwartz and Makhoul, at BBN, proposed the power form with oversubtraction and a spectral floor, and Lim and Oppenheim surveyed the enhancement of noisy speech and the family of subtraction rules. The residual tones were soon named musical noise. In 1984 Ephraim and Malah derived the MMSE estimator of the short-time spectral amplitude, whose smooth gain removes most of it. Spectral subtraction remains the standard simple method and the reference in comparisons, as in the book of Loizou.

## References
