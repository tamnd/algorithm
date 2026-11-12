---
tag: 0R3JDV
kind: concept
slug: burst-errors
name: Burst errors
aliases:
- Burst error
- burst error model
area: compression-and-coding/error-correcting-codes
level: intro
summary: "Errors that come in clusters of nearby symbols, not one by one. A linear code that corrects all bursts of length b needs at least 2b check symbols (the Reiger bound)."
prereqs: [linear-code, syndrome]
see_also: [interleaving, reed-solomon-code, cyclic-code, crc-error-detection-guarantees, concatenated-codes, binary-symmetric-channel, markov-chain, singleton-bound]
sources:
  - paper: doi:10.1109/TIT.1960.1057558
    title: S. H. Reiger, Codes for the correction of "clustered" errors, IRE Transactions on Information Theory 6(1), 1960, pp. 16 to 21
    locator: The bound that a linear code which corrects all bursts of length b or less has at least 2b check symbols
  - paper: doi:10.1002/j.1538-7305.1960.tb03959.x
    title: E. N. Gilbert, Capacity of a burst-noise channel, Bell System Technical Journal 39(5), 1960
    locator: The two-state Markov model of a burst-noise channel, with no errors in the good state
  - paper: doi:10.1002/j.1538-7305.1963.tb00955.x
    title: E. O. Elliott, Estimates of error rates for codes on burst-noise channels, Bell System Technical Journal 42(5), 1963
    locator: The two-state model with errors in both states, and error rates of block codes on it
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 20 (burst-error-correcting codes, the Reiger bound, Fire codes, interleaved codes and Reed-Solomon codes for bursts)
---

A burst error is a group of errors that fall close together in a block, instead of being spread at random. Many real channels make errors this way: a fade in a radio link, a scratch on a disc or a defect on a magnetic surface damages a run of neighbouring symbols. Codes for bursts measure damage by the length of the window that holds the errors, not by the number of errors, and they can be much more efficient than codes that correct the same number of random errors.

## In plain words

Think of a line of text where a drop of ink covers a few letters next to each other. Many letters are hurt, but all in one place. A random error model would call this a large number of errors and give up. A burst model says it is one burst, and a code can be built to repair any one burst up to a fixed length.

Such codes need fewer extra symbols than codes for scattered errors, because a short run of damage has far fewer possible shapes than the same number of errors anywhere. There is still a limit: to repair every burst of a given length, the check part must be at least twice that long.

When the bursts are longer than one code can repair, the symbols of many codewords are mixed before sending, so that one long burst becomes small damage in many codewords.

## The idea

**Burst length.** Write an error pattern as a word $e$ of length $n$. Its **burst length** is the number of positions from its first nonzero symbol to its last one, both included. The pattern $0010110$ has burst length 4 (positions 3 to 6), although it has only three errors; the positions inside need not all be wrong. For cyclic codes one also uses the **cyclic burst length**, where the window can wrap from the end to the start, so $1000001$ is a cyclic burst of length 2. Over $\mathrm{GF}(2)$ there are $n$ bursts of length 1 and $(n - b + 1)\,2^{b - 2}$ bursts of length exactly $b \ge 2$ in $n$ positions: choose the start, and the $b - 2$ inner positions freely.

**Correction is a coset condition.** For a [linear code](/linear-code/) $C$, a decoder can correct every error pattern in a set $E$ exactly when the patterns of $E$ (and the zero pattern) lie in different cosets of $C$, that is, when they have different [syndromes](/syndrome/). For bursts, the condition is that no nonzero codeword is the sum of two bursts of length at most $b$. A sum of two such bursts can be any burst of length at most $2b$, and more.

**The Reiger bound.** A linear $[n, k]$ code over $\mathrm{GF}(q)$ that corrects all bursts of length $b$ or less has
$$n - k \ge 2b.$$
*Proof.* Take two different words $u$ and $v$ that are zero outside the first $2b$ positions. Their difference is nonzero and fits in the first $2b$ positions, so it is $e_1 + e_2$, where $e_1$ is zero outside positions $1$ to $b$ and $e_2$ is zero outside positions $b + 1$ to $2b$. If it were a codeword, the patterns $e_1$ and $-e_2$, each zero or a burst of length at most $b$, would have the same syndrome, and the decoder could not separate them. So all $q^{2b}$ such words lie in different cosets, and there are only $q^{n - k}$ cosets. The same argument with a window of $b$ positions shows that *detecting* all bursts of length at most $b$ needs $n - k \ge b$; a cyclic code with $n - k$ check symbols, such as a CRC, meets this, as the page [CRC error detection guarantees](/crc-error-detection-guarantees/) shows.

A code that meets the Reiger bound with equality is called optimal for bursts, and the ratio $2b/(n - k)$ is its burst-correcting efficiency. For bursts, the bound plays the role that the [Singleton bound](/singleton-bound/) $n - k \ge d - 1 \ge 2t$ plays for random errors.

**Codes for bursts.**

- **Fire codes** (Fire, 1959) are binary [cyclic codes](/cyclic-code/) with generator $g(x) = (x^{2b - 1} + 1)\,p(x)$, where $p(x)$ is irreducible of degree $m \ge b$ and its period $e$ (the least $e$ with $p(x) \mid x^e + 1$) does not divide $2b - 1$. The length is $n = \operatorname{lcm}(2b - 1, e)$, and the code corrects every burst of length $b$ or less with $n - k = 2b - 1 + m$ check bits. A decoder can find the burst by error trapping in a shift register.
- **Reed-Solomon codes** over $\mathrm{GF}(q)$ correct any $t$ symbol errors with $n - k = 2t$, so for bursts counted in symbols they meet the Reiger bound with equality. Over $\mathrm{GF}(2^m)$, each symbol is $m$ bits, and a bit burst of length $m(t - 1) + 1$ or less touches at most $t$ symbols. So a [Reed-Solomon code](/reed-solomon-code/) correcting $t$ symbol errors corrects every bit burst of that length, and also many patterns that are not bursts.
- **Interleaved codes.** [Interleaving](/interleaving/) $I$ codewords of a code that corrects bursts of length $b$ gives a code that corrects bursts of length $I b$, with the same rate.

**Models of bursty channels.** The Gilbert model (Gilbert, 1960) is a two-state [Markov chain](/markov-chain/) with a good state G and a bad state B. In G no errors occur; in B each bit is in error with some probability. Elliott (1963) allowed errors in both states, with bit error probabilities $\epsilon_G < \epsilon_B$; the result is called the Gilbert-Elliott channel. If the chain goes from G to B with probability $p_{GB}$ and back with probability $p_{BG}$ after each bit, the [stationary distribution](/stationary-distribution/) gives $\pi_B = p_{GB}/(p_{GB} + p_{BG})$, the average bit error rate is $\pi_G \epsilon_G + \pi_B \epsilon_B$, and a stay in B lasts $1/p_{BG}$ bits on average. The noise has memory: an error makes the next error more likely. A decoder that uses this memory can do better than on a memoryless [binary symmetric channel](/binary-symmetric-channel/) with the same average error rate, since the entropy rate of the noise is less than the entropy of one noise bit. A decoder that ignores it, and decodes each codeword as if the errors were independent, can do much worse, which is why codes for random errors are used with interleaving.

## Examples

- **A single-error-correcting code fails on short bursts.** The $[7, 4, 3]$ Hamming code corrects any one error, but no pattern of two errors, not even two adjacent ones. Two adjacent errors make the syndrome of a third position, and the decoder changes a third bit.
- **The bound is tight for small $b$.** The repetition codes $[3, 1]$ and $[5, 1]$ correct all bursts of length 1 and 2 with $n - k = 2$ and $n - k = 4$. A search over all $3277$ binary linear codes with $2 \le n \le 6$ and $1 \le k < n$ finds none that breaks $n - k \ge 2b$, or $n - k \ge b$ for detection, and finds codes with $n - k = 2b$ for $b = 1$ and $b = 2$.
- **A Fire code.** With $b = 2$ and $p(x) = x^3 + x + 1$, whose period is 7, the generator is $g(x) = (x^3 + 1)(x^3 + x + 1)$ and $n = \operatorname{lcm}(3, 7) = 21$, so the code is $[21, 15]$. All its bursts of length at most 2, cyclic ones included, have different syndromes, and some bursts of length 3 share a syndrome. It uses 6 check bits where the Reiger bound asks for 4, an efficiency of $2/3$. As a cyclic code with 6 check bits, it also detects every burst of length 6 or less.
- **A Reed-Solomon code on bits.** The $[7, 3, 5]$ Reed-Solomon code over $\mathrm{GF}(8)$ corrects $t = 2$ symbol errors. Its binary image is a $[21, 9]$ binary code that corrects every bit burst of length $3(2 - 1) + 1 = 4$ or less, since such a burst covers at most two 3-bit symbols. A burst of length 5 can cover three symbols.
- **A Gilbert-Elliott channel.** Take $p_{GB} = 0.01$, $p_{BG} = 0.1$, $\epsilon_G = 0.001$ and $\epsilon_B = 0.3$. The chain spends $1/11$ of the time in B, bad periods last 10 bits on average, and the average bit error rate is $\frac{10}{11}(0.001) + \frac{1}{11}(0.3) \approx 0.028$. But almost all errors come from B, so after an error the next bit is wrong with probability about $0.26$, more than nine times the average.

## Where it is used

- **Optical discs and storage.** A scratch or a dust particle on a compact disc wipes out a run of bits. The cross-interleaved Reed-Solomon code of the CD uses two Reed-Solomon codes with [interleaving](/interleaving/) between them to repair long bursts. Disk drives and tape used Fire codes and later Reed-Solomon codes for the same reason.
- **Wireless and satellite links.** Fading makes the error rate change with time, so radio systems use interleavers in front of their codes. In [concatenated codes](/concatenated-codes/), the inner decoder (often a Viterbi decoder) makes its mistakes in bursts, and an outer Reed-Solomon code with an interleaver corrects them.
- **Error detection.** A CRC with $r$ check bits detects every burst of length $r$ or less, so it is a good check on links where errors come in bursts.
- **Channel modelling.** The Gilbert-Elliott model and other hidden Markov models of the noise are used to test codes and protocols on links with memory, and to fit measured error traces.

## References
