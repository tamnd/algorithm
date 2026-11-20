---
tag: 9MCZDF
kind: technique
slug: hybrid-arq
name: Hybrid ARQ
aliases:
- HARQ
- incremental redundancy
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "Combine forward error correction with retransmission: keep the soft values of a failed block and decode them jointly with the copies or extra parity sent after each NACK."
prereqs: [reliable-data-transfer, channel-coding-theorem]
see_also: [chase-combining, link-adaptation, outer-loop-link-adaptation, effective-snr-mapping, go-back-n, convolutional-code, turbo-code, ldpc-code]
sources:
  - paper: doi:10.1109/TCOM.1982.1095643
    title: "Shu Lin and Philip S. Yu, A hybrid ARQ scheme with parity retransmission for error control of satellite channels, IEEE Transactions on Communications 30(7), 1982"
    locator: "a type II hybrid ARQ scheme that sends parity bits instead of a copy after a failure"
  - paper: doi:10.1109/TCOM.1985.1096314
    title: "David Chase, Code combining: a maximum-likelihood decoding approach for combining an arbitrary number of noisy packets, IEEE Transactions on Communications 33(5), 1985, pages 385 to 393"
    locator: "combining repeated noisy copies of a packet before decoding"
  - paper: doi:10.1109/26.2763
    title: "Joachim Hagenauer, Rate-compatible punctured convolutional codes (RCPC codes) and their applications, IEEE Transactions on Communications 36(4), 1988, pages 389 to 400"
    locator: "a family of punctured codes whose higher-rate members are contained in the lower-rate ones, the code structure used for incremental redundancy"
  - paper: doi:10.1109/18.930931
    title: "Giuseppe Caire and Daniela Tuninetti, The throughput of hybrid-ARQ protocols for the Gaussian collision channel, IEEE Transactions on Information Theory 47(5), 2001, pages 1971 to 1988"
    locator: "information-theoretic throughput of hybrid ARQ with incremental redundancy and with repetition"
  - book: isbn:9780130426727
    title: "Shu Lin and Daniel J. Costello Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004"
    locator: "the chapter on automatic-repeat-request strategies and hybrid ARQ schemes"
---

Hybrid ARQ (HARQ) joins forward error correction with automatic repeat request. A block is sent with a code. If the decoder fails, which a CRC detects, the receiver sends a NACK, and the transmitter sends more. In type I HARQ the receiver drops the failed block and decodes the new copy alone. In the schemes that most systems use, the receiver keeps the soft values of the failed attempts and decodes them together with the new ones: with [Chase combining](/chase-combining/) the new transmission is the same coded block, and the soft values add up, which raises the SNR; with incremental redundancy (type II) it is new parity from a lower-rate mother code, which lowers the code rate. Each round lets the link try a high rate first and pay with extra symbols only when the channel was worse than expected, so HARQ also absorbs the errors of [link adaptation](/link-adaptation/).

## In plain words

When a packet arrives damaged, plain ARQ throws it away and asks for it again. Hybrid ARQ uses an error-correcting code as well, and it keeps the damaged copy.

If the first try fails, the sender sends either the same packet again or some extra check bits for it. The receiver puts the old and the new parts together and tries again. Two weak copies together are often good enough, even when neither was good alone. The sender can therefore start bold, with little protection, and add protection only when it turns out to be needed.

## When it applies

- There is a feedback channel with a short and known delay, so the transmitter learns quickly whether each block was decoded.
- The receiver can detect a decoding failure, usually with a CRC, and can store soft values for blocks in progress.
- The channel quality at the time of sending is uncertain, from fading, interference or delayed reports, so a fixed rate would either waste capacity or fail often.
- The traffic tolerates a few round trips of delay.

## The template

1. **Encode once with a low-rate mother code.** Choose a code of rate $R_0$, for example a turbo or [LDPC](/ldpc-code/) code, and split its output into redundancy versions $v_1, v_2, \ldots, v_M$. For type I and Chase combining, every $v_k$ is the same block.
2. **Send the first version.** Send $v_1$, whose code rate $R_1 > R_0$ is chosen by link adaptation for a first-transmission block error rate, often near 10%.
3. **Decode and check.** Decode all received soft values of this block; check the CRC; send an ACK or a NACK.
4. **On a NACK, send the next version.** Send $v_{k+1}$. Combine at the receiver: add the log-likelihood ratios of repeated bits (Chase combining), and place new parity bits in their positions of the mother code (incremental redundancy). The effective code rate after $k$ rounds is $R_1 / k$ for equal-length versions.
5. **Stop.** Stop after an ACK or after $M$ rounds, then leave the block to a higher layer.
6. **Keep the pipe full.** Run several HARQ processes in parallel, each a stop-and-wait loop on its own block, so the link sends while waiting for feedback.

**Why it gains.** With ideal Gaussian codes, a block of rate $R$ bits per channel use can be decoded after $k$ rounds when the accumulated information $\sum_{i \le k}\log_2(1 + \gamma_i)$ reaches $R$ (incremental redundancy), or when $\log_2(1 + \sum_{i \le k}\gamma_i) \ge R$ (Chase combining). The throughput is $R(1 - P_{\mathrm{fail}})/\mathbb{E}[T]$ by a renewal argument, where $T$ is the number of rounds used and $P_{\mathrm{fail}}$ the chance that all $M$ rounds fail. Caire and Tuninetti analyze this throughput for Gaussian channels. Since $\sum\log_2(1 + \gamma_i) \ge \log_2(1 + \sum\gamma_i)$, incremental redundancy never needs more rounds than Chase combining with the same channel.

## Classic examples

**One SNR, two kinds of combining.** At $\gamma = 1$ (0 dB) in every round, a block with $R = 2$ bits per channel use fails at first, because $\log_2(1 + 1) = 1 < 2$.

| rounds | Chase combining $\log_2(1 + k\gamma)$ | incremental redundancy $k\log_2(1 + \gamma)$ |
|---|---|---|
| 1 | 1.000 | 1.000 |
| 2 | 1.585 | 2.000 (decoded) |
| 3 | 2.000 (decoded) | |

Chase combining needs 3 rounds, for a throughput of $2/3$ bits per channel use; incremental redundancy needs 2, for 1 bit per channel use, which is the capacity at 0 dB.

**Rayleigh fading at 10 dB.** Take independent Rayleigh fading in each round with mean SNR 10 dB, ideal codes and at most 4 rounds. A Monte Carlo run with 200000 blocks and a fixed seed gives (computed values):

| scheme | first rate $R$ | throughput (bits per channel use) | fails after 4 rounds |
|---|---|---|---|
| type I, unlimited retries, best $R$ | 3 | 1.49 | none |
| Chase combining | 2 | 1.54 | 0.03% |
| incremental redundancy | 2 | 1.56 | 0.004% |
| Chase combining | 4 | 1.55 | 6.5% |
| incremental redundancy | 4 | 2.03 | 0.15% |
| incremental redundancy | 6 | 2.23 | 1.7% |

The type I value is $R(1 - p)$ with the outage $p = 1 - e^{-(2^R - 1)/10}$. With incremental redundancy, a bold first rate pays off: the throughput climbs toward the ergodic capacity of the channel, about 2.91 bits, without any knowledge of the fading at the transmitter. Chase combining gains SNR but not degrees of freedom, so a high first rate fails often.

**Cellular systems.** HSPA, LTE and 5G NR use HARQ with several parallel processes and soft buffers at the receiver. In LTE and NR the redundancy versions are read from a circular buffer of the turbo or LDPC mother code, so a retransmission can be either a repeat or new parity.

## Variations

- **Type I.** Discard failed blocks. Simple and memoryless, but every attempt must succeed alone.
- **Type II (incremental redundancy).** Send only new parity after a failure. Lin and Yu proposed a scheme of this kind with parity retransmission; [rate-compatible punctured codes](/convolutional-code/), introduced by Hagenauer, give the nested code rates it needs.
- **Type III.** Each retransmission is self-decodable but differs from the earlier ones, so it can be decoded alone or combined with them.
- **Chase combining.** Repeat the same block and add the soft values. See [Chase combining](/chase-combining/).
- **Asynchronous and synchronous.** In synchronous HARQ, retransmissions come at fixed times after the NACK; in asynchronous HARQ, the scheduler chooses the time and the resources.
- **Adaptive retransmission.** The retransmission may use a different modulation or set of resources from the first one.

## Pitfalls

- **Soft buffer size.** Storing soft values for many parallel processes takes memory; when the buffer is too small, the receiver must drop parity bits and the gain falls.
- **Feedback errors.** A NACK read as an ACK loses the block at this layer; an ACK read as a NACK wastes a round. Design the feedback for a much lower error rate than the data.
- **Counting the wrong BLER.** Link adaptation usually aims at the first-transmission BLER; the residual BLER after all rounds is much lower. Mixing them up skews the [outer loop](/outer-loop-link-adaptation/).
- **Delay.** Each round adds a round trip. For delay-sensitive traffic, limit the number of rounds.
- **Correlated fading.** If the channel does not change between rounds, a retransmission sees the same fade; the gain then comes from the extra energy and parity alone.

## Exercises

1. With ideal codes, at $\gamma = 3$ (4.8 dB) in every round and $R = 4$, how many rounds do Chase combining and incremental redundancy need?
   *Answer.* Incremental redundancy: $k\log_2 4 = 2k \ge 4$ gives 2. Chase combining: $\log_2(1 + 3k) \ge 4$ needs $3k \ge 15$, so 5.
2. Show that $\log_2(1 + a) + \log_2(1 + b) \ge \log_2(1 + a + b)$ for $a, b \ge 0$.
   *Answer.* $(1 + a)(1 + b) = 1 + a + b + ab \ge 1 + a + b$.
3. Type I HARQ has a block error rate $p$ per attempt, independent between attempts, and unlimited retries. What is the throughput for a block of rate $R$?
   *Answer.* The number of attempts is geometric with mean $1/(1 - p)$, so the throughput is $R(1 - p)$.
4. Why do systems run several HARQ processes in parallel?
   *Answer.* Each process waits for the feedback of its block before sending more; with $K$ processes, the transmitter can send a new block in every slot while each process waits $K$ slots.
5. Why does incremental redundancy need a rate-compatible code family?
   *Answer.* The receiver decodes the union of all versions received so far, so each union must be a codeword set of one code; the higher-rate codes must be punctured forms of the lower-rate ones.

## References
