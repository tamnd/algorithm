---
tag: FBS75S
kind: technique
slug: effective-snr-mapping
name: Effective SNR mapping
aliases:
- EESM
- MIESM
area: communications/link-adaptation-and-resource-allocation
level: advanced
summary: "Compress the SNRs of the many subcarriers that carry one coded block into one effective SNR, so that the block error rate can be read from an AWGN curve."
prereqs: [link-adaptation, orthogonal-frequency-division-multiplexing]
see_also: [link-adaptation, outer-loop-link-adaptation, adaptive-modulation, bit-loading, jensens-inequality, channel-capacity, hybrid-arq, chase-combining]
sources:
  - paper: doi:10.1109/PIMRC.2005.1651855
    title: "Karsten Brueninghaus, David Astély, Thomas Sälzer, Samuli Visuri, Angeliki Alexiou, Stephan Karger and Gholam-Ali Seraji, Link performance models for system level simulations of broadband radio access systems, IEEE International Symposium on Personal, Indoor and Mobile Radio Communications (PIMRC) 2005, volume 4, pages 2306 to 2311"
    locator: "link performance models that map the SINRs of an OFDM block to one effective SINR for system level simulation"
---

An effective SNR mapping (ESM) predicts the block error rate (BLER) of a coded block whose symbols see different SNRs $\gamma_1, \ldots, \gamma_N$, as on the subcarriers of an [OFDM](/orthogonal-frequency-division-multiplexing/) system in frequency-selective fading. It maps the SNRs to one number $\gamma_{\mathrm{eff}}$ and reads the BLER from the curve that the same modulation and code have on an AWGN channel at the SNR $\gamma_{\mathrm{eff}}$. Most mappings have the form $\gamma_{\mathrm{eff}} = \beta\, I^{-1}\!\left(\frac{1}{N}\sum_k I(\gamma_k/\beta)\right)$ for an increasing function $I$ and a parameter $\beta$ fitted for each modulation and coding scheme. The exponential mapping (EESM) uses $I(x) = 1 - e^{-x}$, which gives $\gamma_{\mathrm{eff}} = -\beta\ln\left(\frac{1}{N}\sum_k e^{-\gamma_k/\beta}\right)$. The mutual information mapping (MIESM) uses the mutual information per symbol of the modulation for $I$. Effective SNRs feed the threshold tables of [link adaptation](/link-adaptation/) and the link-to-system interfaces of network simulators.

## In plain words

In a wideband radio link, one block of data is spread over many tones, and some tones are strong while others are faded. The decoder can still succeed, because the code uses the strong tones to fill in the weak ones. But how likely is it to succeed?

An effective SNR mapping answers with one number: the SNR of a plain, unfaded link on which the same block would fail just as often. It is found by a fixed formula with one tuning knob per coding setting. With that number, the sender can use the same simple tables it uses for an unfaded link. A plain average would be too hopeful, because a few bad tones can ruin a block; the formula gives the bad tones more weight.

## When it applies

- One coded block is spread over symbols with different SNRs, and the code is long enough to mix them, as with turbo or LDPC codes interleaved over many subcarriers.
- AWGN curves of BLER against SNR are known for each scheme, from simulation or measurement.
- The question is a quick prediction, for example the choice of a scheme for the next block or the result of each block in a system simulation where full decoding is too slow.
- The SNRs are known or estimated per subcarrier or per group of subcarriers.

## The template

1. **Collect the SNRs.** Get $\gamma_1, \ldots, \gamma_N$ (linear, not dB) for the symbols of the block, one per subcarrier or per resource block.
2. **Choose the mapping.** EESM: $\gamma_{\mathrm{eff}} = -\beta\ln\left(\frac{1}{N}\sum_k e^{-\gamma_k/\beta}\right)$. MIESM: $\gamma_{\mathrm{eff}} = I_M^{-1}\left(\frac{1}{N}\sum_k I_M(\gamma_k)\right)$, where $I_M(\gamma)$ is the mutual information per symbol of the constellation on an AWGN channel at the SNR $\gamma$, often with a scale $\beta$ as in the general form.
3. **Fit $\beta$ per scheme.** For each modulation and coding scheme, simulate many channel draws, record the SNRs and whether the block failed, and choose $\beta$ to minimize the error between the predicted and the measured BLER, for example in the log domain.
4. **Look up the BLER.** Read $\mathrm{BLER}_{\mathrm{AWGN}}(\gamma_{\mathrm{eff}})$ from the scheme's curve. For link adaptation, compare $\gamma_{\mathrm{eff}}$ for each candidate scheme with its threshold.

**Why EESM has this form.** For BPSK at SNR $\gamma$, the Chernoff bound gives $Q(\sqrt{2\gamma}) \le e^{-\gamma}$. The pairwise error probability of two codewords that differ in $d$ positions is then at most $\prod e^{-\gamma_k}$ over those positions. If the positions are spread at random over the subcarriers by an interleaver, its average is $\left(\frac{1}{N}\sum_k e^{-\gamma_k}\right)^d$, which is the AWGN bound $e^{-d\gamma_{\mathrm{eff}}}$ with $\beta = 1$. For square $M$-QAM with unit average energy, the minimum squared distance is $6/(M-1)$, and the same steps give $\beta = (M - 1)/1.5$: 2 for QPSK, 10 for 16-QAM, 42 for 64-QAM. Fitted values differ from these, because the bound is loose and the code matters, which is why $\beta$ is fitted for each scheme.

**Properties of EESM.** By [Jensen's inequality](/jensens-inequality/) for the convex function $e^{-x/\beta}$, $\gamma_{\mathrm{eff}} \le \frac{1}{N}\sum_k \gamma_k$, and since every term is at most $e^{-\min\gamma_k/\beta}$, $\gamma_{\mathrm{eff}} \ge \min_k \gamma_k$. As $\beta \to 0$ it tends to the minimum, and as $\beta \to \infty$ to the mean; in between it increases with $\beta$. If all $\gamma_k$ are equal, $\gamma_{\mathrm{eff}}$ equals them, so the mapping is exact on AWGN.

## Classic examples

**Four subcarriers.** Take SNRs of 0, 5, 10 and 15 dB. The mean of the linear values is 10.59 dB and the minimum is 0 dB. EESM gives (computed values):

| $\beta$ | 1 | 2 | 5 | 10 | 30 |
|---|---|---|---|---|---|
| $\gamma_{\mathrm{eff}}$ | 3.57 dB | 5.01 dB | 6.94 dB | 8.27 dB | 9.69 dB |

A robust scheme (small $\beta$) is judged mostly by its weak subcarriers; a dense one is closer to the mean. The Gaussian-input mapping with $I(\gamma) = \log_2(1 + \gamma)$ gives the mean rate 2.886 bits and $\gamma_{\mathrm{eff}} = 2^{2.886} - 1 = 6.39$, or 8.06 dB.

**Scheme choice in OFDM.** A scheduler that must pick one scheme for a block of 12 resource blocks computes $\gamma_{\mathrm{eff}}$ for each candidate with that candidate's $\beta$, and picks the fastest one whose $\gamma_{\mathrm{eff}}$ meets its threshold. Because $\beta$ differs per scheme, the effective SNR is not one number per channel but one per channel and scheme.

**System simulation.** A network simulator with thousands of links cannot decode every block. It computes $\gamma_{\mathrm{eff}}$ from the simulated SINRs, reads the BLER from a table, and draws the block result from it. This is the link-to-system interface. EESM was proposed for this use by Ericsson in the 3GPP RAN1 contribution R1-031303, "System-level evaluation of OFDM - further considerations" (meeting 35, Lisbon, November 2003).

## Variations

- **MIESM with BICM.** For bit-interleaved coded modulation, use the mutual information per coded bit of the labelled constellation; this follows the decoder more closely for higher orders and needs less fitting.
- **Capacity mapping.** $I(\gamma) = \log_2(1 + \gamma)$, the Gaussian-input mapping, needs no table but is less accurate for a fixed constellation at high SNR.
- **Two parameters.** Some fits use $\gamma_{\mathrm{eff}} = \alpha_1 I^{-1}\left(\frac1N\sum I(\gamma_k/\alpha_2)\right)$, with a second scale to correct an offset.
- **HARQ.** With [Chase combining](/chase-combining/), add the SNRs of each symbol over the transmissions before the mapping; with [incremental redundancy](/hybrid-arq/), average the mutual information over all received bits, which favors MIESM.
- **Multiple antennas.** Use the post-detection SINR of each layer and subcarrier as the inputs.
- **Reporting.** The receiver can send $\gamma_{\mathrm{eff}}$ itself, or the index of the scheme it would choose, as the channel quality report.

## Pitfalls

- **Averaging dB values.** The mapping works on linear SNRs. The mean of the dB values is the geometric mean, 7.5 dB in the example, which is neither EESM nor MIESM.
- **One $\beta$ for all schemes.** $\beta$ depends strongly on the modulation and somewhat on the code rate. A single value gives large errors for some schemes.
- **Short blocks and little diversity.** The mapping assumes the code spreads its bits over many SNRs. For short codes or few subcarriers, the BLER also depends on which bits are faded.
- **Channel estimation error.** The mapping is fitted with known SNRs. With estimated ones, the prediction is biased, and an [outer loop](/outer-loop-link-adaptation/) is needed to correct it.
- **Extrapolating the fit.** A $\beta$ fitted on one channel model may not fit another with very different selectivity.

## Exercises

1. Show that EESM gives $\gamma_{\mathrm{eff}} = \gamma$ when all $\gamma_k = \gamma$.
   *Answer.* $\frac1N\sum e^{-\gamma/\beta} = e^{-\gamma/\beta}$, and $-\beta\ln e^{-\gamma/\beta} = \gamma$.
2. Show that $\gamma_{\mathrm{eff}} \ge \min_k\gamma_k$ for EESM.
   *Answer.* Each $e^{-\gamma_k/\beta} \le e^{-\gamma_{\min}/\beta}$, so the mean is at most $e^{-\gamma_{\min}/\beta}$, and $-\beta\ln$ is decreasing.
3. Two subcarriers have SNRs 0 and 20 (linear). Compute EESM with $\beta = 1$.
   *Answer.* $-\ln\left(\frac{1 + e^{-20}}{2}\right) \approx \ln 2 = 0.693$, or $-1.59$ dB: the faded subcarrier at 0 dominates.
4. Use the Chernoff bound to derive $\beta$ for 16-QAM with unit average energy.
   *Answer.* $d_{\min}^2 = 6/15 = 0.4$, and $Q(\sqrt{d_{\min}^2\gamma/2}) \le e^{-d_{\min}^2\gamma/4} = e^{-\gamma/10}$, so $\beta = 10$.
5. Why does a simple mean of the linear SNRs overestimate the quality of a frequency-selective channel?
   *Answer.* The mean is the limit $\beta \to \infty$ of EESM, which ignores how strongly the error rate grows on the weak subcarriers. Any finite $\beta$ gives a lower value, by Jensen's inequality.

## References
