---
tag: VX3AMN
kind: problem
slug: frame-synchronization
name: Frame synchronization
aliases:
- frame sync
- frame alignment
area: communications/synchronization
level: core
summary: "Find where each frame or packet begins in the stream of received symbols, usually by searching for a known sync word or preamble, with few false alarms and few misses."
prereqs: [cross-correlation, phase-shift-keying, additive-white-gaussian-noise-channel]
see_also: [preamble-correlation-detection, massey-frame-synchronization, barker-code, schmidl-cox-synchronization, symbol-timing-recovery, maximal-length-sequence, zadoff-chu-sequence, van-de-beek-estimator]
sources:
  - paper: doi:10.1109/TCOM.1972.1091127
    title: "James L. Massey, Optimum frame synchronization, IEEE Transactions on Communications 20(2), 1972, pages 115 to 119"
    locator: "the model of a sync word in random binary data and the maximum likelihood rule"
  - paper: doi:10.1109/TCOM.1980.1094813
    title: "Robert A. Scholtz, Frame synchronization techniques, IEEE Transactions on Communications 28(8), 1980, pages 1204 to 1213"
    locator: "the survey of frame sync methods: sync word search, error probabilities, sync word design and the search and lock strategies"
  - paper: doi:10.1109/TCOM.1987.1096864
    title: "G. L. Lui and H. H. Tan, Frame synchronization for Gaussian channels, IEEE Transactions on Communications 35(8), 1987, pages 818 to 829"
    locator: "optimum and approximate frame sync rules on Gaussian channels and their error probabilities"
  - book: "R. H. Barker, Group synchronizing of binary digital systems, in Communication Theory, W. Jackson (editor), Butterworths, London, 1953, pages 273 to 287"
    title: "R. H. Barker, Group synchronizing of binary digital systems, in Communication Theory, Butterworths, 1953"
    locator: "binary sync groups with small off-peak agreement"
---

Frame synchronization is the problem of finding where each frame, packet or burst begins in a stream of received symbols. After [symbol timing recovery](/symbol-timing-recovery/) the receiver has one value per symbol, but it does not know which value is the first symbol of a frame, so it cannot split the stream into headers, payloads and code words. The usual solution is to insert a known pattern, a sync word inside a continuous stream or a preamble before a burst, and to search for it. The [preamble correlation detector](/preamble-correlation-detection/) correlates with the pattern and compares with a threshold. [Massey's rule](/massey-frame-synchronization/) is the optimum search for a sync word in random binary data. For OFDM, the [Schmidl and Cox](/schmidl-cox-synchronization/) method uses a preamble with two equal halves. The pattern itself is chosen for a sharp autocorrelation, as the [Barker codes](/barker-code/) are.

## In plain words

Data arrive as a long row of symbols with no marks between the messages. To read a message, the receiver must know where it starts. So the sender puts a known short pattern at the start of each message. The receiver looks for the pattern in what it receives. Noise can hide the pattern, and random data can look like it by chance. A good method finds the pattern where it is, and seldom finds it where it is not. A good pattern looks very different from any shifted copy of itself.

## Definition

**Input.** A sequence of received values $y_0, y_1, \ldots$, one per symbol after the matched filter and symbol timing, and a known sync word $s_0, \ldots, s_{L-1}$. In the model of Massey, a window of $N$ values holds the sync word at an unknown start $\mu$, equally likely in $\{0, \ldots, N-1\}$, and the other values are independent random data. Each value is $y_i = h\,d_i + n_i$, with $d_i$ the sync or data symbol, $h$ a gain and $n_i$ noise, as on the [AWGN channel](/additive-white-gaussian-noise-channel/).

**Output.** The start $\hat\mu$. In the threshold form, the output is a decision at each start, frame or no frame.

**Measures.** The probability of a wrong start $P(\hat\mu \ne \mu)$ in the window form. In the threshold form, the false alarm probability per start on noise or data and the miss probability. In continuous links, the mean time to acquire and the mean time to lose a correct lock.

## Variants

- **Embedded sync word or preamble.** A sync word between frames of a continuous stream is surrounded by data on both sides. A preamble starts a burst after silence or noise.
- **Window or threshold.** If exactly one sync word is known to lie in a window, the receiver picks the best position. If not, it compares each position with a threshold.
- **Soft or hard decisions.** The search uses the real received values or only their signs.
- **Coherent or noncoherent.** With an unknown carrier phase the search uses the magnitude of a complex correlation. With a frequency offset it may use differential products.
- **Periodic sync.** When the sync word repeats every $F$ symbols, the receiver can combine several frames and confirm a lock over several periods.

## Examples

**A threshold set for a false alarm rate (theorem).** For a preamble of length $L = 13$ on white circular Gaussian noise, the normalized correlation $\rho$ at one start passes $\lambda$ with probability $(1 - \lambda)^{12}$, whatever the noise level. A false alarm rate of $10^{-3}$ per start needs $\lambda = 0.4377$, and $10^{-6}$ needs $\lambda = 0.6838$.

**Data that look like the sync word (theorem for one group, estimate for a frame).** With hard decisions and random equiprobable binary data, a fixed group of $L$ data symbols equals the sync word with probability $2^{-L}$. For $L = 13$ this is $1.22 \times 10^{-4}$. In a frame of 1000 symbols there are about 1000 such groups, so the chance of at least one exact match in the data is about $0.11$. This is why a receiver confirms a lock over several frames.

**The pattern matters (theorem).** The aperiodic autocorrelation of a word of $L$ ones at shift $k$ is $L - k$, so a shifted copy that partly overlaps itself gives almost the full peak. For the Barker word of length 13 every shift gives 0 or 1.

**Optimum against correlation (measurement).** For Barker 13 in a window of 64 random BPSK symbols at $E_s/N_0 = 0$ dB, Massey's rule chose the wrong start in $3.6\%$ of 2000 trials, and plain correlation in $15.9\%$.

## Known algorithms

| Algorithm | Setting | Note |
|---|---|---|
| [Preamble correlation detection](/preamble-correlation-detection/) | preamble or sync word, threshold | normalized correlation; constant false alarm rate on noise |
| [Massey optimum frame synchronization](/massey-frame-synchronization/) | sync word in random data, window | maximum likelihood with a $\ln\cosh$ correction; needs the SNR |
| Hard-decision sync word search | sync word, threshold | accepts up to $e$ disagreements in sign; picking the fewest disagreements in a window is the optimum hard-decision rule |
| [Schmidl and Cox](/schmidl-cox-synchronization/) | OFDM preamble with two equal halves | autocorrelation of the received signal; tolerates a frequency offset |
| [Van de Beek estimator](/van-de-beek-estimator/) | OFDM cyclic prefix | finds the symbol start from the repeated prefix, without a preamble |

Continuous receivers wrap the search in a state machine: a search state, a check state that waits for the sync word one frame later, and a lock state that leaves only after several missed sync words.

## Bounds

- **Optimum rule (theorem).** In Massey's model, the maximum likelihood rule minimizes $P(\hat\mu \ne \mu)$ among all rules, so its error probability is a lower bound for every method in that model.
- **False alarms on noise (theorem).** For the normalized correlation, the false alarm probability per start is $(1 - \lambda)^{L-1}$ on white circular Gaussian noise. Over $K$ starts, the union bound gives at most $K(1 - \lambda)^{L-1}$.
- **False sync in data (theorem).** With hard decisions, a tolerance of $e$ disagreements and random data, a group of data symbols is accepted with probability $2^{-L}\sum_{i=0}^{e}\binom{L}{i}$.
- **Length of the sync word (heuristic).** For a fixed false alarm rate and SNR, the miss probability falls with $L$, at the cost of $L$ symbols of overhead per frame.

## Reductions

- **To multiple hypothesis testing.** Each start is a hypothesis. With equally likely starts, the minimum error rule is the maximum likelihood rule, which gives Massey's rule for binary data on the AWGN channel.
- **To matched filtering.** For a preamble after noise, the likelihood ratio of the preamble against noise at one start is a function of the correlation, so the search is a [cross-correlation](/cross-correlation/) with the pattern followed by a threshold.
- **From symbol timing.** Frame synchronization assumes symbol timing is known. Run at several samples per symbol, a preamble correlation also gives the symbol timing, which joins the two problems.

## Applications

- **Space telemetry.** CCSDS links mark each transfer frame with an attached sync marker, the 32-bit word 1ACFFC1D in hexadecimal.
- **Wi-Fi and other packet radios.** IEEE 802.11 bursts start with short and long training fields, which the receiver uses to detect the packet and find its start.
- **Cellular systems.** GSM bursts carry a training sequence in the middle, and LTE cells send primary synchronization signals built from Zadoff-Chu sequences.
- **Wired links.** An Ethernet frame starts with a preamble of alternating bits and a start frame delimiter.
- **Framing of coded data.** Decoders of block codes and interleavers need the frame start to align code words.

## References
