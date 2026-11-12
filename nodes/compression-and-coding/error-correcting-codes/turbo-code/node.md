---
tag: NXDXWC
kind: definition
slug: turbo-code
name: Turbo code
aliases:
- parallel concatenated convolutional code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Two recursive systematic convolutional encoders, the second fed through an interleaver, send the message bits and both parity streams. Iterative decoding comes close to capacity.
history:
  year: 1993
  people: [Claude Berrou, Alain Glavieux, Punya Thitimajshima]
  note: Berrou, Glavieux and Thitimajshima presented turbo codes in 1993. Benedetto and Montorsi explained the interleaver gain in 1996, and Benedetto, Divsalar, Montorsi and Pollara gave the serial form in 1998.
prereqs: [convolutional-code, interleaving]
see_also: [turbo-decoding, bcjr-algorithm, concatenated-codes, systematic-code, ldpc-code, channel-coding-theorem, polar-code, additive-white-gaussian-noise-channel]
sources:
  - paper: doi:10.1109/ICC.1993.397441
    title: C. Berrou, A. Glavieux and P. Thitimajshima, Near Shannon limit error-correcting coding and decoding, turbo-codes, Proceedings of the IEEE International Conference on Communications (ICC), 1993, pages 1064 to 1070
    locator: The parallel concatenation of two recursive systematic codes through an interleaver, and the simulated bit error rate of the rate 1/2 code with an interleaver of 65536 bits
  - paper: "S. Benedetto and G. Montorsi, Unveiling turbo codes: some results on parallel concatenated coding schemes, IEEE Transactions on Information Theory 42(2), 1996, pages 409 to 428"
    title: "Unveiling turbo codes: some results on parallel concatenated coding schemes"
    locator: The uniform interleaver, the interleaver gain, and why the constituent encoders must be recursive
  - paper: "S. Benedetto, D. Divsalar, G. Montorsi and F. Pollara, Serial concatenation of interleaved codes: performance analysis, design, and iterative decoding, IEEE Transactions on Information Theory 44(3), 1998, pages 909 to 926"
    title: "Serial concatenation of interleaved codes: performance analysis, design, and iterative decoding"
    locator: Serially concatenated convolutional codes with an outer code, an interleaver and a recursive inner code, and their interleaver gain
  - url: https://www.3gpp.org/DynaReport/36212.htm
    title: 3GPP TS 36.212, Evolved Universal Terrestrial Radio Access (E-UTRA), Multiplexing and channel coding
    locator: Section 5.1.3.2 (the turbo encoder, its 8-state constituent code with g0 = 1 + D^2 + D^3 and g1 = 1 + D + D^3, the trellis termination, and the QPP interleaver with the parameters of Table 5.1.3-3)
  - url: https://ccsds.org/Pubs/131x0b5.pdf
    title: CCSDS 131.0-B-5, TM Synchronization and Channel Coding, Blue Book
    locator: Section 6 (the turbo code, its 16-state constituent encoders with G0 = 10011 and G1 = 11011, the permutation with k1 = 8, and the information block lengths of Table 6-1)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 16 (turbo coding, the weight distribution of parallel concatenated codes and the error floor)
---

A turbo code is a parallel concatenation of two recursive systematic [convolutional codes](/convolutional-code/). The first encoder reads the message bits in their order. The second reads the same bits in the order of a fixed permutation, the [interleaver](/interleaving/). The codeword is the message bits followed by the two parity streams, so the basic rate is 1/3, and puncturing the parity gives higher rates. The code is a long linear block code with no small trellis, so it is not decoded by maximum likelihood. [Turbo decoding](/turbo-decoding/) instead runs a [BCJR](/bcjr-algorithm/) decoder on each constituent trellis and lets the two exchange soft information. In 1993 this reached a bit error rate of $10^{-5}$ well within 1 dB of capacity on the [AWGN channel](/additive-white-gaussian-noise-channel/).

## Definition

**Constituent encoder.** A recursive systematic convolutional (RSC) encoder of memory $m$ with feedback polynomial $g_0(D)$ and feedforward polynomial $g_1(D)$, both of degree at most $m$ with $g_0(0) = 1$, maps an input $u(D)$ to the systematic stream $u(D)$ and the parity stream

$$p(D) = u(D)\, \frac{g_1(D)}{g_0(D)}.$$

In the shift register, the bit that enters the register at time $t$ is $a_t = u_t + \sum_{i=1}^{m} g_{0,i}\, a_{t-i}$, and the parity is $p_t = \sum_{i=0}^{m} g_{1,i}\, a_{t-i}$, over GF(2).

**Interleaver.** A permutation $\pi$ of $\{0, \ldots, N - 1\}$. The interleaved message is $u'_i = u_{\pi(i)}$.

**Turbo code.** For a message $u = (u_0, \ldots, u_{N-1})$, the rate 1/3 turbo encoder sends

$$x^{s} = u, \qquad x^{p1} = \text{parity of RSC}_1(u), \qquad x^{p2} = \text{parity of RSC}_2(u').$$

Each encoder is driven back to state 0 by $m$ tail steps. In a tail step the input is the feedback sum, so the bit that enters the register is 0. The tail inputs and tail parities are sent, which adds $4m$ bits for two encoders. The turbo code is the set of all such codewords; it is a linear block code of dimension $N$, since the map from $u$ to the codeword is linear over GF(2).

**Puncturing.** Deleting parity bits by a fixed pattern raises the rate. Sending $p1$ at even times and $p2$ at odd times gives rate 1/2 (not counting the tail). The decoder puts an LLR of 0 at each deleted position.

**Why the encoders are recursive.** For a feedforward encoder, an input of weight 1 gives a codeword of low weight, and no interleaver can change that, since an interleaved weight 1 input is still of weight 1. For a recursive encoder, $1/g_0(D)$ is an infinite series, so an input of weight 1 gives a parity stream that never ends. The low weight parity streams come from inputs that $g_0(D)$ divides, and the lightest of these have weight 2: $1 + D^{L}$, where $L$ is the period of $g_0$. The interleaver should map most such inputs to inputs that the second encoder does not divide. Benedetto and Montorsi showed that with recursive encoders the bit error rate of the average code over all interleavers falls in proportion to $1/N$ at a fixed signal to noise ratio. This is the *interleaver gain*.

**Error floor.** The minimum distance of a turbo code grows only slowly with $N$, and a few low weight codewords always remain. At low signal to noise ratio the iterative decoder improves fast; at high signal to noise ratio the bit error rate curve flattens and follows the few lightest codewords. This flat part is the error floor. A good interleaver design lowers it; serial concatenation lowers it more.

## Examples and non-examples

**A small worked example.** Take both constituent encoders equal to the RSC encoder $(1, 5/7)$, that is $g_0 = 1 + D + D^2$ and $g_1 = 1 + D^2$ with $m = 2$, the message $u = 10110010$, and the interleaver $\pi = (3, 6, 1, 4, 7, 2, 5, 0)$. Then $u' = 11000101$, and

| stream | bits |
|---|---|
| $x^{s}$ | 1 0 1 1 0 0 1 0 |
| $x^{p1}$ | 1 1 0 0 1 0 0 0 |
| $x^{p2}$ | 1 0 0 1 1 1 0 1 |
| tail 1 (input, parity) | (1, 0) (1, 1) |
| tail 2 (input, parity) | (1, 0) (1, 1) |

The rate 1/3 codeword has $24 + 8 = 32$ bits for 8 message bits. With alternate puncturing it has $16 + 8 = 24$ bits.

**Weight 1 and weight 2 inputs.** For the encoder $(1, 5/7)$, the input $1$ gives the parity 1 1 1 0 1 1 0 1 1 0 ..., which never ends. The input $1 + D^3$ is a multiple of $1 + D + D^2$, and it gives the parity $1 + D + D^2 + D^3$, the stream 1 1 1 1, after which the encoder is back in state 0.

**The interleaver matters.** With the identity interleaver both encoders see the same input, so each input $1 + D^{3}$ inside the block gives a codeword of weight $2 + 4 + 4 = 10$ wherever it sits. A brute-force search over all $\binom{40}{2}$ inputs of weight 2 for $N = 40$ gives the least weight 8 for the identity interleaver and 9 for the LTE QPP interleaver with $f_1 = 3$ and $f_2 = 10$. In both cases the lightest word comes from the input with ones in the last two positions: there the termination tail closes the first encoder at once. For the QPP interleaver the two ones go to the positions 26 and 23, three apart, which is again the pattern $1 + D^3$ for the second encoder. Small blocks keep such light words; the uniform interleaver analysis shows that they get rarer as $N$ grows.

**The turbo code of BGT 1993.** Berrou, Glavieux and Thitimajshima used two 16-state RSC encoders with the generators 37 (feedback) and 21 octal, an interleaver of $256 \times 256 = 65536$ bits, and puncturing to rate 1/2. With 18 decoding iterations they reported a bit error rate of $10^{-5}$ at $E_b/N_0 = 0.7$ dB on the AWGN channel with BPSK. The capacity limit of a rate 1/2 code on this channel is about 0.2 dB with BPSK input, and 0 dB with unconstrained input.

**LTE.** 3GPP TS 36.212, Section 5.1.3.2, uses two equal 8-state RSC encoders with $g_0(D) = 1 + D^2 + D^3$ and $g_1(D) = 1 + D + D^3$, rate 1/3, and 12 tail bits. The interleaver is the quadratic permutation polynomial (QPP)

$$\Pi(i) = (f_1 i + f_2 i^2) \bmod K,$$

with $u'_i = u_{\Pi(i)}$, where Table 5.1.3-3 lists $f_1$ and $f_2$ for each allowed block size $K$ from 40 to 6144. For example $(K, f_1, f_2) = (40, 3, 10)$, $(64, 7, 16)$ and $(1216, 39, 76)$. For $K = 40$, $\Pi(0), \ldots, \Pi(3) = 0, 13, 6, 19$. A QPP is a permutation only for suitable $f_1$ and $f_2$; the implementation checks that each of the eight rows that it copies gives one.

**CCSDS.** CCSDS 131.0-B-5, Section 6, defines a turbo code for space links with two 16-state encoders, backward (feedback) connection vector $G_0 = 10011$ and forward vector $G_1 = 11011$, information block lengths 1784, 3568, 7136 and 8920 bits, and rates 1/2, 1/3, 1/4 and 1/6. Its interleaver is a permutation built from $k_1 = 8$ and $k_2 = N/8$ and eight primes.

**Serial concatenation (Benedetto, Divsalar, Montorsi and Pollara 1998).** An outer convolutional code, an interleaver, and an inner recursive convolutional code in series. It is also decoded iteratively. Its interleaver gain is larger when the outer code has free distance at least 3, so its error floor is lower, but it usually converges at a higher signal to noise ratio than the parallel code.

**Non-example: feedforward constituent codes.** With two feedforward systematic encoders $(1, 1 + D^2)$, an input of weight 1 gives the parity $1 + D^2$ in each encoder, at any position and for any interleaver. That is a codeword of weight $1 + 2 + 2 = 5$, and there are $N$ of them. The number of light words grows with $N$, and there is no interleaver gain.

**Non-example: a product code.** A [product code](/product-codes/) also uses two codes and a permutation, but it encodes the parity of the first code again, in series. A turbo code encodes only the message twice, in parallel.

## Related definitions

- [Convolutional code](/convolutional-code/): the constituent codes, here in recursive systematic form.
- [Interleaving](/interleaving/): the permutation between the two encoders.
- [Concatenated codes](/concatenated-codes/): the general idea of building a long code from shorter ones; a turbo code is the parallel form.
- [Systematic code](/systematic-code/): the message bits appear in the codeword.
- [LDPC codes](/ldpc-code/): the other family of iteratively decoded codes that come close to capacity. A turbo code also has a sparse parity-check description, but it is not the usual one for decoding.
- [Polar codes](/polar-code/): the capacity achieving family that 5G NR chose for its control channels, while it chose LDPC codes for data.
- [Channel coding theorem](/channel-coding-theorem/): the limit that turbo codes first came close to in practice.

## References
