---
tag: K3EMZX
kind: algorithm
slug: decision-feedback-equalizer
name: Decision feedback equalizer
aliases:
- DFE
area: communications/channel-estimation-and-equalization
level: core
summary: "Cancels the postcursor ISI by subtracting a filtered copy of past decisions and handles the precursor ISI with a linear filter. With ideal feedback the MMSE design is one Wiener solve."
solves: [channel-equalization]
model: real-ram
complexity:
  vars: {N: the number of feedforward taps, L: the number of channel taps, K: the number of symbols}
  time: {worst: O(N^2 (N + L) + K (N + L))}
  space: {extra: O(N (N + L))}
properties: {deterministic: true, linear: false, needs_noise_level: true, biased: true, error_propagation: true}
history:
  year: 1967
  people: [M. E. Austin, J. Salz]
  note: "Austin proposed decision feedback for dispersive channels in 1967. Salz derived the optimum mean-square DFE of infinite length in 1973."
prereqs: [channel-equalization, mmse-linear-equalizer, intersymbol-interference]
see_also: [mmse-dfe-canonical-theorem, tomlinson-harashima-precoding, viterbi-equalizer, reduced-state-sequence-estimation, zero-forcing-equalizer, v-blast, successive-interference-cancellation, adaptive-equalization]
sources:
  - book: isbn:9780072957167
    title: "John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008"
    locator: "Section 9.5 (decision-feedback equalization), with 9.5-1 (coefficient optimization) and 9.5-2 (performance and error propagation)"
  - book: isbn:9780792375487
    title: "John R. Barry, Edward A. Lee and David G. Messerschmitt, Digital Communication, third edition, Kluwer Academic Publishers, 2004"
    locator: "Chapter 8 (equalization)"
  - paper: "M. E. Austin, Decision-feedback equalization for digital communication over dispersive channels, Technical Report 461, MIT Research Laboratory of Electronics, August 1967"
    locator: "the decision feedback structure"
  - paper: "J. Salz, Optimum mean-square decision feedback equalization, Bell System Technical Journal 52(8), 1973, pages 1341 to 1373"
    locator: "the infinite-length MMSE-DFE and its error"
---

The decision feedback equalizer is a linear [equalizer](/channel-equalization/) with a second filter that runs on the decisions. A channel $h$ of $L$ taps adds echoes of each symbol to the later samples (postcursor ISI) and, after a delay, to the earlier ones (precursor ISI). The feedforward filter $c$ works on the received samples and handles the precursors and the noise. The feedback filter $b$ works on the symbols already decided: it rebuilds their echoes and subtracts them before the slicer. These echoes are removed without any noise gain, which the [linear MMSE equalizer](/mmse-linear-equalizer/) and the [zero-forcing equalizer](/zero-forcing-equalizer/) cannot do. The cost is that a wrong decision feeds a wrong echo back, so errors come in bursts. The [MMSE-DFE canonical theorem](/mmse-dfe-canonical-theorem/) shows that the infinite-length MMSE-DFE with correct feedback loses no capacity. [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/) moves the feedback to the transmitter, where there are no wrong decisions. The [Viterbi equalizer](/viterbi-equalizer/) decides the whole sequence and has no error propagation, at a cost exponential in $L$. The same idea on a channel matrix instead of a convolution is [V-BLAST](/v-blast/) and [successive interference cancellation](/successive-interference-cancellation/).

## In plain words

Each received sample contains the wanted symbol, echoes of older symbols and noise. A linear equalizer removes the echoes by filtering, and this also amplifies the noise. A DFE notices that the older symbols were already decided. If those decisions are right, the receiver knows the echoes exactly and can subtract them. Subtraction adds no noise. A short linear filter in front still handles the echoes of the symbols not yet decided. The weak point is a wrong decision: the receiver then subtracts the wrong echo, and the next decision is more likely to be wrong too.

## The problem

The input is the channel $h = (h_0, \ldots, h_{L-1})$, the noise power $N_0$, the symbol energy $E_s$, the alphabet, the filter lengths $N_f$ and $N_b$, the delay $\Delta$, and the received samples $y[n] = \sum_l h_l\, x[n-l] + w[n]$ at one sample per symbol, with independent symbols of mean zero and $w[n] \sim \mathcal{CN}(0, N_0)$. The slicer input for the symbol $x[n-\Delta]$ is
$$q[n] = \sum_{i=0}^{N_f-1} c_i\, y[n-i] - \sum_{j=1}^{N_b} b_j\, \hat x[n-\Delta-j].$$
The design problem is to choose $c$ and $b$ to minimize $J = E|q[n] - x[n-\Delta]|^2$, under the assumption that the past decisions $\hat x$ are correct. The run then produces the decisions $\hat x[0], \hat x[1], \ldots$ one at a time.

## The algorithm

Stack the samples in $u = Hs + v$ as for the linear equalizer, where $H$ is the $N_f \times (N_f + L - 1)$ convolution matrix with $H_{ij} = h_{j-i}$. With correct feedback, the symbols in the positions $\Delta + 1, \ldots, \Delta + N_b$ are known, so the feedforward filter does not need to fight them. The design removes their columns from $H$ and solves the Wiener problem against the rest. The feedback taps are then the postcursors of the combined response $g = c * h$.

```pseudo id=main
MMSE-DFE(h, Nf, Nb, Δ, N0, Es, y, K)
L1  H[i][j] ← h[j - i]  for 0 ≤ i < Nf, 0 ≤ j < Nf + L - 1
L2  K ← the columns j of H with j ≤ Δ or j > Δ + Nb          ▷ remove the fed-back symbols
L3  R ← Es H_K H_Kᴴ + N0 I
L4  r ← Es H e_Δ
L5  f ← R⁻¹ r;  c ← conj(f)                                  ▷ the feedforward taps
L6  J ← Es - rᴴ f                                            ▷ the error with correct feedback
L7  g ← c * h                                                ▷ the combined response
L8  b[j] ← g[Δ + j]  for j = 1 .. Nb                          ▷ the feedback taps
L9  for k ← 0 to K - 1
L10     z ← Σ_i c[i] y[k + Δ - i]
L11     q ← z - Σ_j b[j] x̂[k - j]                           ▷ subtract the known echoes
L12     x̂[k] ← the alphabet point nearest to q / (1 - J/Es)
L13 return x̂
```

Lines L1 to L8 run once per channel. Line L5 is one Hermitian positive definite solve. Line L8 makes the feedback cancel exactly the postcursors $g_{\Delta+1}, \ldots, g_{\Delta+N_b}$ that the feedforward filter leaves. Lines L9 to L12 run once per symbol. Line L12 divides by the bias $1 - J/E_s$: the MMSE output is a shrunk copy of the symbol, which matters for QAM and PAM but not for BPSK or PSK. The ZF-DFE is the limit $N_0 \to 0$. For $h_0 \ne 0$ it can take $N_f = 1$, $c_0 = 1/h_0$ and $b_j = h_j/h_0$.

## Example

Take $h = (1, 0.5)$, $E_s = 1$ and $N_0 = 0.1$ (10 dB). With $N_f = 5$ and $N_b = 1$, the error for each delay is:

| $\Delta$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $J$ | 0.090909 | 0.089069 | 0.088705 | 0.088634 | 0.088620 | 0.778511 |

At $\Delta = 5$ the only postcursor is outside the filter span, so the feedback has nothing to cancel. The best delay is 4, with the feedforward taps $c = (-0.00353, 0.00952, -0.02218, 0.05036, 0.88620)$ and the feedback tap $b_1 = 0.44310$. The cursor of $g = c * h$ is $g_4 = 0.91138 = 1 - J$. The unbiased SNR is $1/J - 1 = 10.28$, or 10.12 dB. For comparison, at the same SNR on the same channel:

| receiver | SNR at the slicer |
|---|---|
| infinite-length linear MMSE | 9.07 dB |
| ZF-DFE, $c_0 = 1$, $b_1 = 0.5$ | 10.00 dB |
| MMSE-DFE, $N_f = 5$, $N_b = 1$ | 10.12 dB |
| infinite-length MMSE-DFE | 10.12 dB |
| matched filter bound, $\|h\|^2 E_s / N_0$ | 10.97 dB |

The infinite-length value is $J_\infty = N_0 / G$, where $G = (1.35 + \sqrt{1.35^2 - 1})/2 = 1.12846$ is the geometric mean of $|H(e^{j\omega})|^2 + N_0/E_s = 1.35 + \cos\omega$. This gives $J_\infty = 0.088616$. The DFE gains 1 dB over the linear equalizer here. On the channel B of Proakis, $h = (0.407, 0.815, 0.407)$ at 20 dB, an MMSE-DFE with $N_f = 11$ and $N_b = 2$ reaches $J = 0.02968$, an unbiased SNR of 15.14 dB, against 6.60 dB for a 31-tap linear MMSE equalizer. That channel has a spectral null, which hurts every linear equalizer.

**Error propagation.** Run the ZF-DFE on $h = (1, 0.5)$ with BPSK and the noise $w = (0, -1.6, 0.1, 0.2, 0)$:

| $k$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $x[k]$ | 1 | 1 | -1 | -1 | 1 |
| $y[k]$ | 1.0 | -0.1 | -0.4 | -1.3 | 0.5 |
| $q = y[k] - 0.5\, \hat x[k-1]$ | 1.0 | -0.6 | 0.1 | -1.8 | 1.0 |
| $\hat x[k]$ | 1 | -1 | 1 | -1 | 1 |

The large noise sample at $k = 1$ causes the first error. The wrong feedback at $k = 2$ adds $-0.5 \times (-1 - 1) = 1$ to $q$, which turns a correct decision into a second error. With correct feedback, $q$ at $k = 2$ would be $-0.9$. At $k = 3$ the error happens to push $q$ the right way, and the burst ends. In a simulation of 40000 symbols at $N_0 = 0.3$ (seed 7206), this receiver made 201 errors with ideal feedback, close to $40000\, Q(\sqrt{2/N_0}) = 196.5$, and 257 errors with its own decisions. On $h = (1, 0.9)$ the ratio grows to about 1.9 (195 against 375, seed 7207).

## Correctness

**Claim.** If the past decisions are correct, lines L5 and L8 give the unique taps that minimize $J$, the minimum is line L6, and the cursor is $g_\Delta = 1 - J/E_s$. With $N_b = 0$ the design is the linear MMSE equalizer, and more feedback taps never increase $J$.

**Key step.** With correct feedback, the error is $E_s \sum_{j \notin B} |g_j - [j = \Delta]|^2 + E_s \sum_t |g_{\Delta+t} - b_t|^2 + N_0 \|c\|^2$, where $B$ holds the feedback positions. The feedback taps appear only in the middle sum, which is zero for $b_t = g_{\Delta+t}$. What remains is a Wiener problem for $f$ against the regressor with the columns $B$ removed, which completing the square solves. Without noise and with a small residual ISI, an induction on $k$ shows that every decision is correct, so the assumption holds. With noise, a burst of errors ends after $N_b$ correct decisions in a row. The proofs folder has the details.

## Complexity

The design costs $O(N_f^2 (N_f + L))$ for $R$ and $O(N_f^3)$ for the solve. $R$ is a Toeplitz matrix minus a matrix of rank $N_b$, so fast solvers exist, but the direct solve is cheap for the usual lengths. The run costs $N_f + N_b$ complex multiplications per symbol. With $N_b \le L - 1$, $K$ symbols cost $O(N^2 (N + L) + K (N + L))$ in the [real RAM](/real-ram/) with $N = N_f$, and the extra space is $O(N (N + L))$ for $H$ and $R$.

## Properties

- **No noise gain for the postcursors.** The feedback removes the echoes of past symbols by subtraction, so on a minimum-phase channel the ZF-DFE needs only one feedforward tap and has the noise gain $1/|h_0|^2$. On $h = (1, 0.5)$ this is 1, against 1.333 for the linear ZF equalizer.
- **Nonlinear.** The slicer is inside the loop, so the DFE is not a linear filter, and its BER is not a function of $J$ alone.
- **Error propagation.** A wrong decision makes the next $N_b$ slicer inputs worse. This is a measurement for each channel; no simple closed form gives the BER.
- **Biased.** With correct feedback, $q[n] = (1 - J/E_s)\, x[n-\Delta]$ plus an uncorrelated error. The unbiased SNR is $E_s/J - 1$.
- **Optimal with ideal feedback in the limit.** The infinite-length MMSE-DFE has $J_\infty = N_0 / \exp\big(\frac{1}{2\pi}\int \ln(|H(e^{j\omega})|^2 + N_0/E_s)\, d\omega\big)$, and its unbiased SNR gives the mutual information of the channel with Gaussian inputs; see the [MMSE-DFE canonical theorem](/mmse-dfe-canonical-theorem/).
- **Causality.** The feedback can only use decided symbols, so the precursor ISI must be handled by the feedforward filter. A channel with strong precursors needs a long feedforward filter and a large delay.

## Variants and improvements

- **ZF-DFE.** The limit $N_0 \to 0$. It is simpler and needs no noise estimate, but it enhances noise from the precursors.
- **Adaptive DFE.** Both filters adapt with the [LMS algorithm](/lms-algorithm/) or the [RLS algorithm](/rls-algorithm/), with the decisions as the reference; see [adaptive equalization](/adaptive-equalization/).
- **Fractionally spaced feedforward filter.** A [fractionally spaced](/fractionally-spaced-equalizer/) feedforward filter makes the DFE insensitive to the sampling phase.
- **Precoding.** [Tomlinson-Harashima precoding](/tomlinson-harashima-precoding/) runs the feedback filter at the transmitter with a modulo operation, so there is no error propagation and coding works as on an ISI-free channel.
- **Sequence estimation with feedback.** [Reduced-state sequence estimation](/reduced-state-sequence-estimation/) keeps a short trellis for the first taps and uses feedback per survivor for the rest; it lies between the DFE and the Viterbi equalizer.
- **Soft feedback.** In [turbo equalization](/turbo-equalization/), the [soft interference cancellation equalizer](/soft-interference-cancellation-equalizer/) subtracts the mean of each symbol from a decoder instead of a hard decision.

## When to use it

Use a DFE when the channel has strong postcursors or spectral nulls and a linear equalizer loses too much SNR, but the Viterbi equalizer is too expensive because $L$ or the alphabet is large. It was the standard receiver of voiceband modems and is common in high-speed serial links. When the code needs reliable symbols before decoding, or when error propagation is too costly, move the feedback to the transmitter with precoding, or iterate with the decoder.

## Pitfalls

- **Designing with real decisions in mind.** The MMSE formulas assume correct feedback. Measure the BER of the real loop, and compare it with a run that feeds back the true symbols to separate error propagation from the noise.
- **The wrong delay.** On $h = (1, 0.5)$ with $N_f = 5$ and $N_b = 1$, the error is 0.0886 at $\Delta = 4$ and 0.7785 at $\Delta = 5$, where the feedback is outside the span. Keep $\Delta \le N_f - 1$ and search over the delays.
- **Feedback indexing.** $b_1$ multiplies the decision just before the current one. An off-by-one shift subtracts the wrong echo on every symbol, and the loop can still look stable at high SNR.
- **The bias with multilevel alphabets.** For 16-QAM or 4-PAM, slice $q / (1 - J/E_s)$. Without the scaling, the outer points fall short.
- **Startup.** Before the first decision, the feedback has no history. Start with a known preamble, or treat the symbols before the block as known zeros, as the implementation does.
- **Coding.** A decoder needs soft values for all symbols of a block, but the DFE needs hard decisions now. Tentative decisions from the slicer are less reliable than the decoded symbols, which is a reason for precoding.

## Implementations

## History

Austin proposed decision feedback for digital communication over dispersive channels in a 1967 MIT report. In 1973, Salz derived the optimum mean-square DFE of infinite length and its minimum error, the geometric mean form above. The DFE became a common receiver for voiceband modems. Tomlinson in 1971 and Harashima and Miyakawa in 1972 moved the feedback to the transmitter. In 1995, Cioffi, Dudevoir, Eyuboglu and Forney showed that the unbiased MMSE-DFE is canonical: with ideal feedback and Gaussian codes, it reaches the capacity of the ISI channel.

## References
