---
tag: JJK6YC
kind: problem
slug: link-adaptation
name: Link adaptation
aliases:
- adaptive modulation and coding
- AMC
area: communications/link-adaptation-and-resource-allocation
level: intro
summary: "Choose the modulation, code rate and power of each transmission from the reported channel quality, so that the throughput is high and the block error rate stays near a target."
model: real-ram
complexity:
  vars: {J: the number of modulation and coding schemes}
  time: {worst: O(log J)}
prereqs: [spectral-efficiency, bit-error-rate]
see_also: [adaptive-modulation, outer-loop-link-adaptation, effective-snr-mapping, hybrid-arq, truncated-channel-inversion, water-filling-power-allocation, bit-loading, channel-capacity]
sources:
  - paper: doi:10.1109/26.634685
    title: "Andrea J. Goldsmith and Soon-Ghee Chua, Variable-rate variable-power MQAM for fading channels, IEEE Transactions on Communications 45(10), 1997, pages 1218 to 1230"
    locator: "adaptive rate and power for a target bit error rate on a fading channel, with continuous and discrete rate sets"
  - paper: doi:10.1109/18.641562
    title: "Andrea J. Goldsmith and Pravin P. Varaiya, Capacity of fading channels with channel side information, IEEE Transactions on Information Theory 43(6), 1997, pages 1986 to 1992"
    locator: "the capacity with side information at both ends, an upper bound on the average rate of any adaptive scheme"
  - book: isbn:9780521837163
    title: "Andrea Goldsmith, Wireless Communications, Cambridge University Press, 2005"
    locator: "Chapter 9 (adaptive modulation and coding)"
  - paper: doi:10.1109/VETECF.2007.378
    title: "Klaus I. Pedersen, Guillaume Monghal, Istvan Z. Kovacs, Troels E. Kolding, Akhilesh Pokhariyal, Frank Frederiksen and Preben Mogensen, Frequency domain scheduling for OFDMA with limited and noisy channel feedback, IEEE Vehicular Technology Conference (VTC 2007-Fall), pages 1792 to 1796"
    locator: "link adaptation from channel quality reports with an outer loop that corrects the reported SINR from acknowledgments"
---

Link adaptation is the problem of choosing, for each transmission, a modulation and coding scheme (MCS) from a fixed list, and sometimes a power, from a report of the channel quality, so that the data rate is as high as possible while the block error rate (BLER) stays near a target. The transmitter does not see the channel; it sees a quantized and delayed SNR or SINR estimate that the receiver sends back. Each scheme $j$ has a rate $R_j$ and a BLER curve $\mathrm{BLER}_j(\gamma)$ that falls with the SNR $\gamma$, and a faster scheme needs a higher SNR for the same BLER. The choice trades rate against errors: the throughput of scheme $j$ is $R_j(1 - \mathrm{BLER}_j(\gamma))$. In cellular systems the problem is split into an inner loop, which maps the reported quality to a scheme with a table, and an [outer loop](/outer-loop-link-adaptation/), which corrects the table from acknowledgments. [Adaptive modulation](/adaptive-modulation/) in the sense of Goldsmith and Chua is the special case of uncoded QAM with a bit error rate target.

## In plain words

A radio link can send data slowly and safely or fast and with risk. When the signal is strong, the fast way works; when it is weak, the fast way loses most packets.

The receiver measures how strong the signal is and reports it. Before each packet, the sender looks at the last report and picks one setting from a short list, from slow and safe to fast and fragile. It wants the fastest setting that still gets most packets through, often so that about one packet in ten fails. Lost packets are sent again. Because the report can be old or wrong, the sender also watches which packets fail and adjusts its choices.

## Definition

**Input.**

- A list of schemes $j = 1, \ldots, J$, ordered by rate $R_1 < R_2 < \cdots < R_J$ (information bits per channel use), each with a BLER function $\mathrm{BLER}_j(\gamma)$ that does not increase with $\gamma$.
- A quality report $\hat\gamma$, which is related to the true SNR $\gamma$ of the next transmission through an error model, for example $\gamma = \hat\gamma + e$ in dB with a random error $e$.
- A target block error rate $\beta_T$, often $0.1$ in cellular data, or no target.

**Output.** A rule $j(\hat\gamma)$, and in the variants also a power $P(\hat\gamma)$ with an average limit.

**Goal.** One of two forms.

- *Throughput form*: maximize $\mathbb{E}[R_{j}(1 - \mathrm{BLER}_{j}(\gamma)) \mid \hat\gamma]$ over $j$.
- *Target form*: choose the largest $j$ with $\mathbb{E}[\mathrm{BLER}_j(\gamma) \mid \hat\gamma] \le \beta_T$, or the scheme $j = 1$ if none qualifies.

In the target form with an exact report, the rule is a threshold table. Let $\theta_j$ be the SNR at which $\mathrm{BLER}_j(\theta_j) = \beta_T$. If the thresholds increase with $j$, choose the largest $j$ with $\theta_j \le \hat\gamma$. Building the table takes $O(J)$ work once, and each decision is a binary search of $O(\log J)$ comparisons.

## Variants

- **Discrete rate with power.** Adapt the power together with the scheme under an average power limit; for uncoded QAM this is [adaptive modulation](/adaptive-modulation/).
- **Multicarrier.** In OFDM, one scheme covers many subcarriers with different SNRs. An [effective SNR mapping](/effective-snr-mapping/) compresses them into one number for the table. If each subcarrier may use its own constellation, the problem becomes [bit loading](/bit-loading/).
- **With retransmissions.** With [hybrid ARQ](/hybrid-arq/), a failed block is not lost but combined with later copies. The best first-transmission BLER is then higher than with plain ARQ, and the throughput form must count the rounds.
- **Closed-loop correction.** When the error model is unknown or biased, an [outer loop](/outer-loop-link-adaptation/) shifts the report by an offset learned from acknowledgments, so the long-run BLER meets the target.
- **Multiple antennas.** The scheme includes the number of layers and the precoder, and the report includes a rank and a precoder index.
- **Fixed rate.** With one scheme only, the power must do all the work; [truncated channel inversion](/truncated-channel-inversion/) is the policy that keeps the received SNR constant.

## Examples

Take five schemes with rates $R = (0.5, 1, 2, 3, 4.5)$ bits per symbol and a model BLER curve $\mathrm{BLER}_j(\gamma) = 1/(1 + e^{1.5(\gamma - t_j)})$ with $\gamma$ in dB and the 50% points $t = (-2, 1, 6, 10, 15)$ dB. The curve is a modelling choice for this example; real curves come from link simulations. The 10% thresholds are $\theta_j = t_j + \ln 9/1.5 = t_j + 1.46$ dB, that is $-0.54, 2.46, 7.46, 11.46, 16.46$ dB.

| true SNR | scheme from the 10% table | its BLER | its throughput | best throughput |
|---|---|---|---|---|
| 7 dB | 2 (rate 1) | 0.0001 | 1.000 | 1.635 (scheme 3, BLER 0.18) |
| 9 dB | 3 (rate 2) | 0.011 | 1.978 | 1.978 (scheme 3) |
| 11 dB | 3 (rate 2) | 0.0006 | 1.999 | 2.453 (scheme 4, BLER 0.18) |

Three points follow. First, the throughput-best choice can run at a BLER well above 10%, because the next scheme up is much faster. Second, the table is coarse: at 9 dB the AWGN capacity is $\log_2(1 + 10^{0.9}) = 3.16$ bits, and the chosen scheme gives 1.98. Third, errors in the report are costly: if the true SNR is 9 dB but the report says 12 dB, the table picks scheme 4, whose BLER at 9 dB is 0.82, and the throughput falls to 0.55. This is why systems add an outer loop.

## Known algorithms

| method | what it does | cost per decision |
|---|---|---|
| threshold table (inner loop) | largest scheme whose threshold is at most the report | $O(\log J)$ |
| throughput maximization | evaluate $R_j(1 - \mathrm{BLER}_j)$ for each scheme | $O(J)$ |
| [outer loop link adaptation](/outer-loop-link-adaptation/) | add an offset to the report that moves up on each error and down on each success | $O(1)$ per acknowledgment |
| [adaptive modulation](/adaptive-modulation/) | closed-form thresholds and powers from a BER fit | $O(\log J)$ |
| [effective SNR mapping](/effective-snr-mapping/) | maps the SNRs of $N$ subcarriers to one value | $O(N)$ per scheme |

## Bounds

- **Per state.** With an exact report and a Gaussian channel, no scheme can carry more than $\log_2(1 + \gamma)$ bits per channel use with a vanishing error rate, by the [channel coding theorem](/channel-coding-theorem/). With a finite block length, the bound is lower.
- **On average.** With power adaptation and exact knowledge at both ends, the average rate is at most the capacity of Goldsmith and Varaiya, $\int \log_2(\gamma/\gamma_0)\, p(\gamma)\, d\gamma$ over $\gamma \ge \gamma_0$, with the cutoff $\gamma_0$ of [water-filling](/water-filling-power-allocation/) over time.
- **Discrete schemes.** A list of schemes whose rates step by $\Delta R$ loses up to $\Delta R$ bits against a continuous choice at each SNR, unless the power is used to fill the gaps.

## Reductions

- With an exact report and a BLER target, the target form reduces to a search in a sorted list of thresholds.
- With the SNR gap model and uncoded QAM, it reduces to [adaptive modulation](/adaptive-modulation/), whose continuous form is water-filling with a scaled power.
- For multicarrier links with one scheme per block, an effective SNR mapping reduces it to the flat case.
- For many users, link adaptation gives each user's rate for each resource, and a scheduler then chooses the users; the two problems are often solved in turn.

## Applications

- Cellular data: HSDPA, LTE and 5G NR choose a modulation and coding scheme for each transmission from channel quality reports, with HARQ and an outer loop.
- Wireless LAN: IEEE 802.11 stations choose among rate sets, often from loss statistics instead of SNR reports.
- Digital subscriber lines and power-line modems, which adapt per subcarrier by bit loading.
- Satellite links with adaptive coding and modulation that follow rain fades.

## References
