---
tag: 8PQV2E
kind: concept
slug: forward-error-correction
name: Forward error correction
aliases:
- FEC
area: compression-and-coding/error-correcting-codes
level: intro
summary: "Adding redundancy before transmission so that the receiver can correct errors by itself, with no request to send again. Its benefit is measured as coding gain in dB at a target error rate."
prereqs: [minimum-distance, error-detection]
see_also: [channel-coding-theorem, channel-capacity, additive-white-gaussian-noise-channel, hamming-code, reed-solomon-code, ldpc-code, convolutional-code, interleaving]
sources:
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: C. E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part II (the discrete channel with noise), Section 13 (the fundamental theorem, reliable transmission at any rate below capacity with suitable coding)
  - paper: doi:10.1002/j.1538-7305.1950.tb00463.x
    title: R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2), 1950
    locator: The single error correcting codes and the geometric model with the distance between code points
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 1 (forward error correction and automatic repeat request, block and convolutional codes, hard and soft decisions, the coding gain at a given error rate)
---

Forward error correction (FEC) is the practice of adding redundant symbols to data before it is sent or stored, so that the receiver can find and correct errors by itself. Nothing goes back to the sender: the receiver decodes what it has. FEC is the only choice where there is no return path or the round trip is too long, as in broadcasting, storage and deep-space links, and it is part of almost every modern link. Its benefit is usually given as a coding gain: the saving in signal energy per information bit at a target error rate.

## In plain words

When you spell a name on a bad phone line, you say "B as in Bravo". The extra word lets the listener get the letter right even if part of it is lost, without asking you to say it again.

FEC does the same with data. The sender adds extra symbols made from the data by a fixed rule. Noise changes some symbols. The receiver looks for the valid message that is closest to what arrived and takes it as the answer.

The extra symbols cost time, bandwidth or space. In return, the link works with a weaker signal, or with more noise, or at a larger distance. A good code gets much more benefit from the same amount of extra data than a simple one, such as sending everything three times.

## The idea

**Encoding and decoding.** A code maps each block of $k$ data symbols to a codeword of $n > k$ symbols, so its rate is $R = k/n$ and a fraction $1 - R$ of the channel symbols is redundancy. The decoder maps each received word back to a message, usually the one whose codeword is most likely, as in [maximum likelihood decoding](/maximum-likelihood-decoding/). With [minimum distance](/minimum-distance/) $d$, a code corrects every pattern of up to $t = \lfloor (d - 1)/2 \rfloor$ symbol errors, or $d - 1$ erasures; good codes also correct most patterns of more errors.

**FEC against retransmission.** [Error detection](/error-detection/) with automatic repeat request needs few check bits and is very reliable, but it needs a return channel, and its delay and throughput get worse as the channel gets worse. FEC has a fixed delay and a fixed rate whatever the noise, works on one-way links and for many receivers at once, but must carry enough redundancy for the worst noise it is designed for. Hybrid ARQ puts the two together: FEC corrects the common errors and a retransmission handles the rest.

**Hard and soft decisions.** On a channel with continuous output, such as the [additive white Gaussian noise channel](/additive-white-gaussian-noise-channel/), the receiver can first decide each bit (a hard decision, which turns the channel into a [binary symmetric channel](/binary-symmetric-channel/)) and then decode, or it can give the decoder the real-valued channel outputs (soft decisions). Soft decisions are worth about 2 dB on the Gaussian channel.

**Coding gain.** Compare systems by the energy per information bit $E_b$ over the noise density $N_0$. A coded system with rate $R$ sends each code bit with energy $R E_b$, so the rate penalty is counted. Fix a target bit error rate $P^\ast$. The **coding gain** at $P^\ast$ is
$$G(P^\ast) = \Bigl(\tfrac{E_b}{N_0}\Bigr)_{\text{uncoded}} - \Bigl(\tfrac{E_b}{N_0}\Bigr)_{\text{coded}} \quad \text{in dB},$$
where each term is the least $E_b/N_0$ at which that system reaches $P^\ast$. The gain depends on the target, and it can be negative at high error rates, where the rate penalty is larger than what the code corrects. As $P^\ast \to 0$, it tends to the **asymptotic coding gain**, $10 \log_{10}(R d)$ dB for a binary code with soft-decision maximum likelihood decoding and $10 \log_{10}(R(t + 1))$ dB with hard decisions.

**The limit.** The [channel coding theorem](/channel-coding-theorem/) says that for every rate below the [channel capacity](/channel-capacity/) there are codes with error probability as small as wanted, and none above it. On the Gaussian channel with binary inputs and rate $1/2$, this needs $E_b/N_0 \ge 0.187$ dB, while uncoded BPSK needs $9.59$ dB for a bit error rate of $10^{-5}$. So about 9.4 dB of gain is available at that target for rate $1/2$, and much of the work on coding since 1948 has gone into codes and decoders that get close to this limit at a practical cost.

**A map of the sub-area.**

- **Channels and limits.** The [binary symmetric](/binary-symmetric-channel/), [binary erasure](/binary-erasure-channel/) and [Gaussian](/additive-white-gaussian-noise-channel/) channels; [channel capacity](/channel-capacity/) and the [channel coding theorem](/channel-coding-theorem/).
- **Distance and bounds.** [Hamming distance](/hamming-distance/), [Hamming weight](/hamming-weight/), [minimum distance](/minimum-distance/), and the bounds of [Singleton](/singleton-bound/), [Hamming](/hamming-bound/) and [Gilbert and Varshamov](/gilbert-varshamov-bound/).
- **Linear block codes.** [Linear codes](/linear-code/) with their [generator](/generator-matrix/) and [parity-check](/parity-check-matrix/) matrices and [syndrome decoding](/syndrome-decoding/); the [repetition](/repetition-code/), [Hamming](/hamming-code/), [Golay](/golay-code/) and [Reed-Muller](/reed-muller-code/) codes.
- **Algebraic codes.** [Cyclic codes](/cyclic-code/), [BCH codes](/bch-code/) and [Reed-Solomon codes](/reed-solomon-code/), with bounded-distance and [list decoding](/list-decoding/).
- **Codes with memory and iterative decoding.** [Convolutional codes](/convolutional-code/) and the [BCJR algorithm](/bcjr-algorithm/); [turbo codes](/turbo-code/), [LDPC codes](/ldpc-code/) with [belief propagation](/belief-propagation-decoding/), and [polar codes](/polar-code/).
- **Building larger codes.** [Product codes](/product-codes/), [concatenated codes](/concatenated-codes/) and [interleaving](/interleaving/) against [burst errors](/burst-errors/).
- **Erasures and packets.** [Erasure decoding](/erasure-decoding/), [peeling decoding](/peeling-decoding/) and [fountain codes](/fountain-codes/).

## Examples

- **Repetition.** The [repetition code](/repetition-code/) $[3, 1, 3]$ corrects one error in three, but with hard decisions it needs about 1.44 dB *more* $E_b/N_0$ than no coding at a bit error rate of $10^{-5}$, and with soft decisions its gain is exactly 0 dB. Redundancy alone does not give a gain.
- **The Hamming code $[7, 4, 3]$ with hard decisions.** At $E_b/N_0 = 9.17$ dB, each code bit is wrong with probability about $1.06 \times 10^{-3}$, and syndrome decoding gives a bit error rate of $10^{-5}$. Uncoded BPSK needs $9.59$ dB, so the coding gain at $10^{-5}$ is about $0.41$ dB. At $10^{-9}$ it is about $0.56$ dB, close to the asymptotic hard-decision gain $10 \log_{10}(\frac{4}{7} \cdot 2) \approx 0.58$ dB. Below $E_b/N_0 \approx 5.85$ dB (bit error rates above about $2.8 \times 10^{-3}$) the code is worse than no code. With soft decisions its asymptotic gain is $10 \log_{10}(\frac{4}{7} \cdot 3) \approx 2.34$ dB.
- **Erasures.** A [Reed-Solomon code](/reed-solomon-code/) with $n - k$ check symbols fills any $n - k$ lost symbols. Packet networks use such codes, and [fountain codes](/fountain-codes/), to recover lost packets without a retransmission.
- **Error correction plus detection.** Memory with error correction uses a code of distance 4 per word, which corrects any one bit error and detects any two.

## Where it is used

- **Storage.** Hard disks, flash memory, optical discs, tapes and RAID arrays all use FEC; when the stored data itself is damaged, reading it again does not help. QR codes carry Reed-Solomon check symbols, so a damaged code can still be read.
- **Broadcasting and space.** Digital television and radio, satellite links and deep-space probes have no useful return channel. They use [concatenated codes](/concatenated-codes/) of a [convolutional code](/convolutional-code/) and a Reed-Solomon code with [interleaving](/interleaving/), or [turbo](/turbo-code/) and [LDPC](/ldpc-code/) codes.
- **Mobile and wireless networks.** 5G NR uses LDPC codes for data channels and [polar codes](/polar-code/) for control channels, with hybrid ARQ on top. Wi-Fi uses convolutional and LDPC codes.
- **Wired and optical links.** High-speed Ethernet and long-haul optical links use FEC to run at a raw error rate that would be too high without it.
- **Computer memory.** Error-correcting memory corrects single-bit faults on the fly.

## References
