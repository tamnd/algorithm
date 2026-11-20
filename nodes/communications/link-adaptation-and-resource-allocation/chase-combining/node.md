---
tag: B11JYG
kind: technique
slug: chase-combining
name: Chase combining
aliases:
- soft packet combining
area: communications/link-adaptation-and-resource-allocation
level: core
summary: "Retransmit the same coded block after a failure and add the soft values (log-likelihood ratios) of all copies before decoding, which is maximal ratio combining over time."
prereqs: [hybrid-arq, maximal-ratio-combining]
see_also: [hybrid-arq, maximal-ratio-combining, rayleigh-fading-channel, effective-snr-mapping, outer-loop-link-adaptation, gaussian-q-function, turbo-decoding, link-adaptation]
sources:
  - paper: doi:10.1109/TCOM.1985.1096314
    title: "David Chase, Code combining: a maximum-likelihood decoding approach for combining an arbitrary number of noisy packets, IEEE Transactions on Communications 33(5), 1985, pages 385 to 393"
    locator: "maximum-likelihood decoding of several noisy copies of a packet, by combining them into one codeword of a lower-rate code"
  - paper: doi:10.1109/18.930931
    title: "Giuseppe Caire and Daniela Tuninetti, The throughput of hybrid-ARQ protocols for the Gaussian collision channel, IEEE Transactions on Information Theory 47(5), 2001, pages 1971 to 1988"
    locator: "the throughput of repetition (Chase-type) hybrid ARQ compared with incremental redundancy"
  - book: isbn:9780521845274
    title: "David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005"
    locator: "the chapter on diversity (time diversity and maximal ratio combining of repeated symbols over fading)"
---

Chase combining is the simplest form of [hybrid ARQ](/hybrid-arq/) with memory. When a coded block fails, the transmitter sends the same coded block again, and the receiver adds the log-likelihood ratios (LLRs) of each coded bit over all copies received so far, then decodes the sum. For copies with independent noise, adding LLRs is exactly [maximal ratio combining](/maximal-ratio-combining/) over time: each copy is weighted by its channel gain over its noise power, and the SNRs of the copies add. So after $k$ copies with SNRs $\gamma_1, \ldots, \gamma_k$, the decoder sees one block at the SNR $\gamma_1 + \cdots + \gamma_k$, and if the copies see different fades, it also gains diversity. David Chase described the general idea, maximum-likelihood decoding of several noisy copies of a packet, in 1985. Chase combining gains SNR but not code rate; [incremental redundancy](/hybrid-arq/) sends new parity instead and gains more when the first rate is high.

## In plain words

If a message arrives damaged, the sender sends the same message again. Instead of throwing away the first copy, the receiver keeps it and puts the two copies together.

Each copy carries, for each bit, a measure of how sure the receiver is. The receiver adds these measures from all the copies. A bit that looked unclear in one copy but clear in the other ends up clear. Two copies of equal quality together are about as good as one copy sent with twice the power. If the copies were hit by different fades, a bad moment in one is often covered by a good moment in the other.

## When it applies

- The link uses HARQ with a soft buffer, and the retransmission can be the same coded block.
- The noise of the copies is independent, as it is for thermal noise.
- The first rate is moderate, so extra SNR is what a failed block needs. At high first rates, new parity helps more.
- The receiver must stay simple: the soft buffer stores one value per coded bit, and combining is an addition.

## The template

1. **Store the LLRs of the first copy.** For BPSK with $y_1 = h_1 x + n_1$, $x \in \{+1, -1\}$ and complex noise of variance $N_0$, the LLR is $L_1 = 4\,\mathrm{Re}(h_1^* y_1)/N_0$. For higher orders, use the bit LLRs from the demapper.
2. **On a NACK, receive the same block again.** The transmitter repeats the same coded bits, possibly with a different mapping to symbols.
3. **Add.** For each coded bit, $L = L_1 + L_2 + \cdots + L_k$.
4. **Decode the sum and check.** Decode once with the summed LLRs and check the CRC. Stop on success or after the last round.

**Why adding is optimal.** Given the bit $x$, the copies are independent, so the likelihood of all copies is the product of the likelihoods of each, and the LLR of the product is the sum of the LLRs. For BPSK the sum is $4\,\mathrm{Re}\left(\sum_k h_k^* y_k\right)/N_0$, the output of maximal ratio combining, whose SNR is $\sum_k \gamma_k$ with $\gamma_k = |h_k|^2 E_s/N_0$. This holds bit by bit, for any code and any decoder that takes LLRs.

## Classic examples

**Two copies at 0 dB.** For uncoded BPSK at $\gamma = 1$, the bit error rate is $Q(\sqrt{2}) = 0.0787$. Two copies combine to $\gamma = 2$, and the rate is $Q(2) = 0.0228$, a gain of 3 dB. Selecting the better copy would give nothing here, since both are equal.

**Rayleigh fading at 10 dB.** For uncoded BPSK on [Rayleigh fading](/rayleigh-fading-channel/) with mean SNR 10 dB per copy (computed values):

| receiver | bit error rate |
|---|---|
| one copy | $2.33 \times 10^{-2}$ |
| two copies, same fade, combined | $1.20 \times 10^{-2}$ |
| two copies, independent fades, keep the better | $2.97 \times 10^{-3}$ |
| two copies, independent fades, combined | $1.60 \times 10^{-3}$ |

With the same fade, combining gives 3 dB and no diversity. With independent fades it gives diversity order 2, from the formula $p^2(1 + 2(1 - p))$ with $p = \frac12\left(1 - \sqrt{\gamma/(1 + \gamma)}\right)$. Keeping the better copy also gives diversity 2 but loses the energy of the other one.

**Coded block, ideal codes.** With ideal Gaussian codes, a block of rate $R$ is decoded after $k$ copies when $\log_2(1 + \sum_{i \le k}\gamma_i) \ge R$. At $\gamma = 1$ and $R = 2$, this takes 3 copies; incremental redundancy would need 2. See [hybrid ARQ](/hybrid-arq/) for the throughput on fading channels.

## Variations

- **Constellation rearrangement.** For 16-QAM and higher, the bits in a symbol have unequal reliability. Changing the bit-to-symbol mapping between copies averages this out, which helps more than plain repetition.
- **Code combining.** Chase's 1985 view: the $k$ copies form one codeword of a code with rate $R/k$, and a maximum-likelihood decoder for that code uses all of them. With LLR decoders, this is the same as adding LLRs.
- **Packet combining without a code.** Uncoded systems can combine copies symbol by symbol, by MRC or by majority vote of hard bits; majority voting loses the reliability information.
- **Partial Chase combining.** Send only part of the block again, the bits that the receiver reports as weak, and combine those.
- **Effective SNR.** For multicarrier links, add the SNRs per subcarrier before an [effective SNR mapping](/effective-snr-mapping/) to predict the BLER after combining.

## Pitfalls

- **Wrong scaling of LLRs.** The sum is optimal only if each LLR is scaled by its own noise variance and channel. Adding raw matched filter outputs from copies with different noise levels gives the wrong weights.
- **Saturation.** Fixed-point soft buffers clip large LLRs; after several copies, clipped values add up to wrong reliabilities.
- **Correlated noise or interference.** If the interference is the same in each copy, the copies are not independent, and the sum overstates the reliability.
- **Expecting diversity from a static channel.** In slow fading, every copy sees the same fade; the gain is then only the 3 dB per doubling of the copies.
- **High first rates.** When the first rate is far above what the channel supports, repeating it gains little. Each doubling of the copies adds only one bit per channel use at high SNR.

## Exercises

1. Show that the LLR of $k$ independent copies is the sum of the LLRs of each copy.
   *Answer.* $\ln\frac{\prod_k p(y_k \mid +1)}{\prod_k p(y_k \mid -1)} = \sum_k \ln\frac{p(y_k \mid +1)}{p(y_k \mid -1)}$.
2. Three copies of BPSK each arrive at 0 dB. What is the bit error rate after combining?
   *Answer.* The SNR is 3, and the rate is $Q(\sqrt{6}) = 7.2 \times 10^{-3}$.
3. Two copies arrive at SNRs 4 and 1. What is the SNR after combining, and what weight does MRC give each copy?
   *Answer.* The SNR is $4 + 1 = 5$. With equal noise, MRC weights each copy by $h_k^*/N_0$, so the weights are in the ratio of the amplitudes, $\sqrt{4} : \sqrt{1} = 2 : 1$.
4. With ideal codes and $\gamma = 3$ per copy, how many copies does a block of rate 4 need?
   *Answer.* $\log_2(1 + 3k) \ge 4$ needs $k \ge 5$.
5. Why does Chase combining in slow fading give a gain of only 3 dB per doubling of the copies?
   *Answer.* All copies have the same SNR $\gamma$, so $k$ copies give $k\gamma$; doubling $k$ doubles the SNR, which is 3 dB, and there is no diversity.

## References
