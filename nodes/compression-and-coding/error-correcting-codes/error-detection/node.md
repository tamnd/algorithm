---
tag: CXD68V
kind: concept
slug: error-detection
name: Error detection
aliases:
- Error detection problem
- error detection
- error-detecting codes
area: compression-and-coding/error-correcting-codes
level: intro
summary: Deciding whether a received word was changed in transit, without finding the errors. A code detects every error that does not turn one codeword into another; a retransmission then fixes it.
prereqs: [minimum-distance]
see_also: [checksum, cyclic-redundancy-check, undetected-error-probability, parity-bit, forward-error-correction, go-back-n, selective-repeat, stop-and-wait]
sources:
  - paper: doi:10.1002/j.1538-7305.1950.tb00463.x
    title: R. W. Hamming, Error detecting and error correcting codes, Bell System Technical Journal 29(2), 1950
    locator: Single error detecting codes (the parity check), and the minimum distance needed to detect a given number of errors
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 3.2 (syndrome and error detection), Section 3.6 (the probability of an undetected error for a linear code over a binary symmetric channel) and Chapter 22 (automatic repeat request strategies, including hybrid ARQ)
  - book: isbn:9780132009164
    title: Dimitri Bertsekas and Robert Gallager, Data Networks, second edition, Prentice Hall, 1992
    locator: Section 2.3 (error detection) and Section 2.4 (ARQ, retransmission strategies, p. 64), with stop-and-wait, go back n and selective repeat
---

Error detection is the task of deciding whether a received block of data is still the block that was sent. The sender adds a few check symbols computed from the data, and the receiver tests whether the block still fits them. Unlike error correction, detection does not try to find where the errors are, so the same number of check bits catches far more error patterns. When an error is found, the block is sent again, or thrown away, or marked as bad.

## In plain words

Before you send a message, you add a short summary of it, made by a fixed rule. The receiver makes the summary again from what it got and compares. If the two do not match, something changed on the way, and the receiver asks for the message again.

Sometimes the noise changes the message and the summary so that they still match. Then the error goes through unseen. A good rule makes this very rare, and it never happens for the kinds of damage the rule was designed for, such as a few wrong bits or a short run of wrong bits.

Detection is cheap and strong. Repair needs much more extra data, so many systems detect errors and send the data again.

## The idea

**Detection by membership.** Let $C$ be a code. The receiver accepts a received word $y$ if $y \in C$ and reports an error otherwise. If the codeword $c$ was sent and the channel changed it into $y \ne c$, the error goes unnoticed exactly when $y$ is another codeword. With [minimum distance](/minimum-distance/) $d$, two codewords differ in at least $d$ positions, so **every pattern of $1$ to $d - 1$ errors is detected**, and some pattern of $d$ errors is not. For a [linear code](/linear-code/), the test $y \in C$ is a check that the syndrome $H y^{\mathsf T}$ is zero, where $H$ is a [parity-check matrix](/parity-check-matrix/).

**Which patterns are missed.** For a linear code, $c + e$ is a codeword exactly when the error pattern $e$ is a codeword. So the missed patterns are the same for every sent word: the $q^k - 1$ nonzero codewords. Of all $q^n - 1$ nonzero error patterns, a fraction of about $q^{-(n-k)}$ is missed. With $r = n - k$ binary check bits, a random pattern slips through with probability about $2^{-r}$, whatever the length.

**Undetected error probability.** On a [binary symmetric channel](/binary-symmetric-channel/) with crossover probability $p$, a pattern of weight $w$ has probability $p^w (1 - p)^{n - w}$, so a binary linear code with $A_w$ codewords of weight $w$ misses an error with probability

$$P_{\mathrm{ud}}(p) = \sum_{w = 1}^{n} A_w \, p^w (1 - p)^{n - w}.$$

At $p = 1/2$ every pattern is equally likely, and $P_{\mathrm{ud}} = (2^k - 1)/2^n < 2^{-(n-k)}$. For small $p$ the first term dominates, $P_{\mathrm{ud}} \approx A_d \, p^d$, so a large $d$ and few codewords of weight $d$ are what count. Not every code has $P_{\mathrm{ud}}(p) \le 2^{-(n-k)}$ for all $p \le 1/2$; the page [undetected error probability](/undetected-error-probability/) treats this, and the [MacWilliams identity](/macwilliams-identity/) computes $A_w$ from the dual code.

**Detection versus correction.** With the same distance $d$, a code detects $d - 1$ errors but corrects only $\lfloor (d - 1)/2 \rfloor$. And detection does not need the costly search for the nearest codeword: the check is one syndrome computation. The price is that detection alone does not deliver the data. It needs a way to get the data again, or a use for which losing a block is acceptable.

**Detection plus retransmission (ARQ).** In *automatic repeat request*, the receiver sends a positive acknowledgment for each block that passes the check, and the sender sends again each block that is not acknowledged in time. Let blocks have $n$ bits with $k$ information bits, and let $P$ be the probability that a block is detected in error. Each block is then sent $1/(1 - P)$ times on average. The three classic schemes differ in what they do while they wait:

- **[Stop-and-wait](/stop-and-wait/).** Send one block and wait for its answer. If the round trip adds $s$ idle bit times to each transmission, the throughput is $(1 - P)\,k/(n + s)$ information bits per bit time.
- **[Go-back-N](/go-back-n/).** Send blocks without waiting, up to a window of $N$ blocks. When block $i$ fails, send again from block $i$, so each failure wastes $N$ block times. The expected time per delivered block $T$ satisfies $T = (1 - P) \cdot 1 + P\,(N + T)$, so the throughput is $\frac{1 - P}{1 - P + NP} \cdot \frac{k}{n}$.
- **[Selective repeat](/selective-repeat/).** Send again only the failed blocks, which needs a buffer at the receiver to put blocks back in order. Each failure wastes one block time, and the throughput is $(1 - P)\,k/n$, the best of the three.

A missed error delivers a wrong block to the user, so in ARQ the undetected error probability, not the detected one, sets the reliability, while $P$ sets the throughput.

**Hybrid ARQ.** Combine the two strategies: use a code that corrects the most likely error patterns and detects the rest, and ask for a retransmission only when correction fails ([forward error correction](/forward-error-correction/) inside ARQ). In *type I* hybrid ARQ each transmission carries the data with both kinds of check bits. In *type II*, or *incremental redundancy*, the first transmission carries a high-rate code, and each retransmission sends extra parity bits instead of a copy, so the receiver decodes a stronger code each time.

## Examples

- **[Parity bit](/parity-bit/).** One bit makes the number of ones even. The code is $[n, n - 1, 2]$, it detects every pattern with an odd number of errors, and it misses every pattern with an even number. For $n = 8$ and $p = 0.01$, $P_{\mathrm{ud}} = \sum_{w \text{ even}} \binom{8}{w} p^w (1 - p)^{8 - w} \approx 2.6 \times 10^{-3}$.
- **The Hamming code $[7, 4, 3]$ used only for detection.** Its weights are $A_3 = A_4 = 7$ and $A_7 = 1$, so at $p = 0.01$, $P_{\mathrm{ud}} = 7p^3(1 - p)^4 + 7p^4(1 - p)^3 + p^7 \approx 6.79 \times 10^{-6}$. It detects all patterns of 1 or 2 errors, and misses 15 of the 127 nonzero patterns.
- **A [cyclic redundancy check](/cyclic-redundancy-check/).** A CRC with $r$ check bits is a shortened cyclic code. It detects every burst of length at most $r$ and, with a well chosen [generator polynomial](/crc-generator-polynomial/), all patterns of a few errors in blocks up to a design length. The page [CRC error detection guarantees](/crc-error-detection-guarantees/) has the proofs.
- **Arithmetic checksums.** The [Internet checksum](/internet-checksum/) and other [checksums](/checksum/) add up the data words. They are cheaper in software but weaker than a CRC of the same size; for example, the Internet checksum misses any reordering of 16-bit words.
- **ARQ numbers.** Take blocks of $n = 1000$ bits with a 32-bit CRC, so $k = 968$, on a channel with bit error probability $10^{-4}$. Then $P = 1 - (1 - 10^{-4})^{1000} \approx 0.095$. Selective repeat gives a throughput of about $0.876$. Go-back-N with $N = 8$ gives about $0.526$. Stop-and-wait with a round trip of $s = 7000$ idle bit times (seven blocks) gives about $0.109$.

## Where it is used

- **Link layers.** Ethernet, Wi-Fi and many other link protocols put a CRC on each frame and drop the frames that fail, leaving the recovery to retransmission at the link or at a higher layer.
- **Transport protocols.** TCP and UDP carry the Internet checksum, and TCP retransmits lost or damaged segments with a [sliding window](/sliding-window-protocol/), as part of [reliable data transfer](/reliable-data-transfer/).
- **Storage and files.** Disks, file systems and archive formats store CRCs or cryptographic hashes to detect corruption, and fall back to a redundant copy or report the error.
- **Inside error correction.** A decoder for a strong code can make a wrong decision; an outer CRC tells the receiver whether the decoded block is right. Mobile networks use a CRC on each transport block to trigger hybrid ARQ, and CRC-aided list decoding of [polar codes](/polar-code/) uses it to choose among candidates.
- **Memory.** A parity bit per byte or word detects single-bit faults in memory. Error-correcting memory goes further and corrects one error and detects two per word, with a code of minimum distance 4 such as the extended Hamming code.

## References
