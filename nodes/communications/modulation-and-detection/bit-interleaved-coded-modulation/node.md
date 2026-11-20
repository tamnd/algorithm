---
tag: 4FAB4B
kind: technique
slug: bit-interleaved-coded-modulation
name: Bit-interleaved coded modulation
aliases:
- BICM
area: communications/modulation-and-detection
level: advanced
summary: Puts a bit interleaver between a binary code and the mapper and decodes from bit metrics, a robust scheme for fading channels.
prereqs: [soft-demapping, gray-labeling, convolutional-code, channel-capacity]
see_also: [soft-demapping, max-log-demapping, trellis-coded-modulation, multilevel-coding, ldpc-code, turbo-code, bcjr-algorithm, rayleigh-fading-channel]
sources:
  - paper: doi:10.1109/26.141453
    title: Ephraim Zehavi, 8-PSK trellis codes for a Rayleigh channel, IEEE Transactions on Communications 40(5), 873-884, 1992
    locator: the bit interleaver between a convolutional code and 8-PSK, the bit metrics, and the diversity gain on the Rayleigh channel
  - paper: doi:10.1109/18.669123
    title: Giuseppe Caire, Giorgio Taricco and Ezio Biglieri, Bit-interleaved coded modulation, IEEE Transactions on Information Theory 44(3), 927-946, 1998
    locator: the BICM channel model, the BICM capacity, and the error bounds on AWGN and fading channels
---

Bit-interleaved coded modulation (BICM) is the usual way to join a binary error-correcting code with a constellation of more than two points. The coded bits pass through a bit interleaver, groups of $m$ bits select points of a $2^m$-point constellation with a [Gray labeling](/gray-labeling/), and the receiver computes one log-likelihood ratio per bit with a [soft demapper](/soft-demapping/), deinterleaves, and runs an ordinary binary decoder. The code and the constellation can be chosen separately, and one binary code serves every constellation size. Zehavi proposed it in 1992 for the Rayleigh fading channel, where it gives more diversity than [trellis-coded modulation](/trellis-coded-modulation/). Caire, Taricco and Biglieri in 1998 gave its theory. Wi-Fi, LTE, 5G NR and DVB-S2 all use it.

## In plain words

A binary code protects a stream of bits. A modulator with 16 or 64 points packs several bits into each point. BICM does the obvious thing: it shuffles the coded bits, packs them into points, and at the receiver unpacks each point into a "how sure am I" value for each bit. Then it unshuffles and lets the binary decoder do its normal work. The shuffle makes sure that a weak signal or a bad point only hurts bits that are far apart in the code. The decoder does not need to know anything about the constellation. The cost is a small loss against an ideal joint design, and with a good labeling this loss is very small.

## When it applies

- A strong binary code exists for the job: an [LDPC code](/ldpc-code/), a [turbo code](/turbo-code/), a [polar code](/polar-code/) or a [convolutional code](/convolutional-code/) with soft-input decoding.
- The constellation has more than two points, so each symbol carries $m \ge 2$ coded bits, and the receiver can compute bit LLRs.
- The system must change the constellation and the code rate often, as in [link adaptation](/link-adaptation/), with one encoder and one decoder.
- The channel fades from symbol to symbol, or from subcarrier to subcarrier in [OFDM](/orthogonal-frequency-division-multiplexing/), so that diversity across the codeword matters.

## The template

1. **Encode.** A binary code of rate $R_c$ maps the information bits to a codeword $c_1, c_2, \ldots$.
2. **Interleave.** A bit interleaver $\pi$ permutes the codeword, so that bits close together in the code end up in different symbols, and in different label positions.
3. **Map.** Each group of $m$ interleaved bits $(b_0, \ldots, b_{m-1})$ selects the point with that label, usually Gray. The rate is $m R_c$ information bits per symbol.
4. **Demap.** For each received $y$, compute $L_k = \ln\big(\sum_{b_k(a) = 0} p(y \mid a)/\sum_{b_k(a) = 1} p(y \mid a)\big)$ for $k = 0, \ldots, m-1$, exactly or with [max-log](/max-log-demapping/). On a fading channel, $p(y \mid a)$ uses the known gain of that symbol.
5. **Deinterleave and decode.** Apply $\pi^{-1}$ to the LLRs and run the binary decoder as if each LLR came from its own binary channel.
6. **Optionally iterate.** In BICM with iterative decoding (BICM-ID), the decoder returns extrinsic LLRs, the demapper uses them as priors, and the two exchange information for a few rounds.

The decoder treats the $m$ bits of one symbol as if they had come over $m$ independent binary channels. That is the BICM approximation. The largest rate for which this decoder can work is the BICM capacity

$$C_{\mathrm{BICM}} = \sum_{k=0}^{m-1} I(B_k; Y),$$

where $I$ is the mutual information and the points are equally likely. By the chain rule, the coded modulation capacity is $I(X; Y) = \sum_k I(B_k; Y \mid B_0, \ldots, B_{k-1})$, and each term is at least $I(B_k; Y)$ because the bits are independent. So $C_{\mathrm{BICM}} \le I(X; Y)$, with a gap that depends on the labeling.

## Classic examples

**16-QAM on the AWGN channel.** With equally likely points and the SNR $E_s/N_0$ per complex symbol, numerical integration gives (in bits per symbol):

| $E_s/N_0$ | coded modulation $I(X; Y)$ | BICM, Gray | BICM, natural binary per axis | $\log_2(1 + E_s/N_0)$ |
|---|---|---|---|---|
| 5 dB | 1.973 | 1.932 | 1.654 | 2.057 |
| 10 dB | 3.164 | 3.164 | 2.904 | 3.459 |
| 15 dB | 3.929 | 3.929 | 3.905 | 5.028 |

With Gray labeling the BICM loss is $0.04$ bits at $5$ dB and almost zero above $10$ dB. With natural binary labels it is a quarter of a bit at $10$ dB. This is why BICM uses Gray labels.

**Zehavi's 8-PSK code.** A rate-$2/3$ convolutional code, bit interleaving, and 8-PSK at $2$ bits per symbol. On the Rayleigh channel with ideal interleaving, the diversity order of the code is the minimum [Hamming distance](/hamming-distance/) of the binary code, because each differing bit lands in a different, independently faded symbol. For Ungerboeck's TCM, it is the smallest number of differing symbols on an error path, which is smaller for codes of the same complexity.

**IEEE 802.11a/g Wi-Fi.** A rate-$1/2$ convolutional code with $7$-bit constraint length, punctured to $2/3$ or $3/4$, a block interleaver over the bits of one OFDM symbol, Gray BPSK, QPSK, 16-QAM or 64-QAM, and a Viterbi decoder with soft bit metrics. The highest rate, $54$ Mbit/s, is 64-QAM with rate $3/4$.

**LDPC and turbo codes.** DVB-S2 uses LDPC codes with a bit interleaver and QPSK, 8-PSK, 16-APSK or 32-APSK; LTE uses turbo codes, and 5G NR uses LDPC codes, both with Gray QAM up to 256-QAM and beyond. In each, the decoder is the binary decoder and the only constellation-specific block is the demapper.

## Variations

- **BICM with iterative decoding (BICM-ID).** The demapper uses the decoder's extrinsic LLRs as priors. A labeling other than Gray, for example set partitioning, has a poor BICM capacity but gains a lot from the priors, and BICM-ID with such labels can beat Gray BICM.
- **Max-log demapping.** Replace the exact LLR by the max form, which costs little at high SNR and allows a [min-sum](/min-sum-decoding/) decoder without the noise level.
- **Interleaver design.** The interleaver also spreads the bits over the label positions. In 16-QAM, the in-phase sign bit is more reliable than the bit that separates the inner from the outer levels, and a good design gives each code bit a fair mix.
- **Shaping.** With [probabilistic constellation shaping](/probabilistic-constellation-shaping/), the amplitude bits come from a distribution matcher and the sign bits from the parity of a systematic code, and the demapper uses the nonuniform priors.
- **MIMO BICM.** The demapper computes the LLRs of the bits of a whole vector of symbols, exactly or with a [list sphere decoder](/list-sphere-decoder/).

## Pitfalls

- **Labeling.** Without iterations, BICM needs Gray labeling. Natural or set-partitioning labels lose a lot of capacity (see the table), and a decoder that is fine with Gray fails with them.
- **A short interleaver on a slow fading channel.** The diversity argument assumes that the bits of each error event see independent fades. If the interleaver is shorter than the fade, the code sees bursts of weak bits and the gain disappears.
- **Wrong channel state.** The LLRs need the gain of each symbol and $N_0$. Using one average gain on a fading channel removes most of the benefit; with max-log the scale can be dropped, but the gain per symbol cannot.
- **The bits of one symbol are not independent.** The decoder treats them as independent. This is the source of the gap to $I(X; Y)$, and it also makes the error bounds of a binary code on a binary channel only approximate.
- **Bit order.** The demapper, the interleaver and the mapper must agree on the bit order of the label (here most significant bit first) and on the LLR sign.

## Exercises

1. Show that $\sum_k I(B_k; Y) \le I(X; Y)$ for independent uniform label bits, and give the condition for equality.
2. For Gray QPSK on the AWGN channel, show that $C_{\mathrm{BICM}} = I(X; Y)$ exactly.
3. For Gray 16-QAM, explain why the in-phase bits depend only on the real part of $y/h$, and compute the two LLRs of one axis at $\sqrt{10}\,\mathrm{Re}(y/h) = 1.58$ and $N_0 = 0.1$ with max-log.
4. A binary code has free distance $d$. On a fully interleaved Rayleigh channel with BICM, show that the pairwise error probability of two codewords at Hamming distance $d$ decays as $\bar\gamma^{-d}$, where $\bar\gamma$ is the average SNR.
5. Show that a rate-$1/2$ code with 64-QAM and a rate-$3/4$ code with 16-QAM both carry $3$ information bits per symbol. Using a table of BICM capacities, explain how a system would choose between them.

## References
