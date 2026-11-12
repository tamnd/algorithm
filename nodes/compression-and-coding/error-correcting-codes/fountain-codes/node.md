---
tag: BM90XJ
kind: definition
slug: fountain-codes
name: Fountain codes
aliases:
- rateless codes
- digital fountain codes
- rateless erasure codes
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "Erasure codes with no fixed rate: the sender makes an endless stream of encoded symbols, and any set slightly larger than the k source symbols lets the receiver rebuild them."
history:
  year: 1998
  people: [John Byers, Michael Luby, Michael Mitzenmacher, Ashutosh Rege]
  note: Byers, Luby, Mitzenmacher and Rege described the digital fountain for reliable bulk data distribution in 1998. Luby (LT codes, 2002) and Shokrollahi (Raptor codes, 2006) gave efficient constructions.
prereqs: [erasure-codes, binary-erasure-channel]
see_also: [lt-codes, raptor-codes, peeling-decoding, erasure-decoding, reed-solomon-code, xor-gaussian-elimination, rank, network-coding]
sources:
  - paper: doi:10.1145/285237.285258
    title: John W. Byers, Michael Luby, Michael Mitzenmacher and Ashutosh Rege, A digital fountain approach to reliable distribution of bulk data, Proceedings of ACM SIGCOMM 1998, pages 56 to 67
    locator: The digital fountain idea (a receiver reconstructs the data from any subset of encoding packets equal in total length to the source), and the comparison of Tornado codes with Reed-Solomon codes and with a data carousel
  - paper: doi:10.1109/TIT.2006.874390
    title: Amin Shokrollahi, Raptor codes, IEEE Transactions on Information Theory 52(6), 2006, pages 2551 to 2567
    locator: Section II (the definition of a fountain code by a distribution on GF(2)^k, the reception overhead and the cost measures)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 50 (the random linear fountain, the failure probability at most 2^(-E) with E extra packets, and LT codes)
  - paper: doi:10.1109/SFCS.2002.1181950
    title: Michael Luby, LT codes, Proceedings of the 43rd Annual IEEE Symposium on Foundations of Computer Science (FOCS), 2002, pages 271 to 280
    locator: The introduction (universal erasure codes that need no knowledge of the loss rate)
---

A fountain code turns $k$ source symbols into a stream of encoded symbols that has no fixed end. A receiver that collects any $k(1 + \varepsilon)$ of them, for a small overhead $\varepsilon$, rebuilds the source with high probability. The name comes from a water fountain: you hold out a cup until it is full, and it does not matter which drops you caught. Byers, Luby, Mitzenmacher and Rege described this *digital fountain* in 1998 for sending one file to many receivers with different loss rates.

## Definition

**Notation.** The message has $k$ *source symbols* $s = (s_0, \ldots, s_{k-1})$, each a packet of the same number of bits, and $\oplus$ is bitwise XOR. For a vector $v \in \mathrm{GF}(2)^k$, $\langle v, s \rangle = \bigoplus_{i : v_i = 1} s_i$. The receiver gets $K$ encoded symbols; the *overhead* is $\varepsilon = K/k - 1$, and $E = K - k$ is the number of extra symbols. The channel is an erasure channel: each symbol arrives intact or not at all, and the receiver knows its index.

**Definition (fountain code).** A binary linear fountain code for $k$ source symbols is a probability distribution $\mathcal{D}$ on $\mathrm{GF}(2)^k$ (Shokrollahi 2006). Encoded symbol $j$, for $j = 0, 1, 2, \ldots$, is $e_j = \langle v_j, s \rangle$, where the vectors $v_j$ are drawn independently from $\mathcal{D}$. Both sides generate $v_j$ from a shared pseudorandom generator seeded with $j$, so a packet carries only $j$ and $e_j$.

A *decoder of overhead $\varepsilon$ and failure probability $\delta$* recovers $s$ from any $k(1 + \varepsilon)$ encoded symbols, chosen independently of the random choices of the code, with probability at least $1 - \delta$. Recovery is possible exactly when the received vectors $v_j$ span $\mathrm{GF}(2)^k$, that is, when the $K \times k$ matrix with rows $v_j$ has [rank](/rank/) $k$.

**The properties that matter.**

- *Rateless.* The sender can make as many symbols as needed, and the code has no fixed length $n$ or rate $k/n$.
- *Universal.* The same stream is near optimal for every receiver, whatever its loss rate. A receiver that loses a fraction $p$ of the packets waits about $k(1 + \varepsilon)/(1 - p)$ packet times. No feedback is needed except a final "done".
- *Efficient.* The cost is the mean number of symbol XORs per encoded symbol and per source symbol for decoding. A fountain code is useful only if both are small.

An ideal fountain would have $\varepsilon = 0$, like an MDS code that recovers from any $k$ symbols. Binary codes cannot do this for large $k$, so the design goals are a small $\varepsilon$, a small $\delta$ and linear time.

**Constructions.**

- *The random linear fountain.* $\mathcal{D}$ is uniform on $\mathrm{GF}(2)^k$. Decoding is [Gaussian elimination](/xor-gaussian-elimination/). It has the best overhead possible for a binary code up to a small constant, but encoding costs about $k/2$ XORs per symbol and decoding order $k^3$ bit operations.
- *[LT codes](/lt-codes/)* (Luby 2002). $\mathcal{D}$ chooses a weight $d$ from the robust soliton distribution and then a uniform vector of weight $d$. The [peeling decoder](/peeling-decoding/) needs $k + O(\sqrt{k} \ln^2(k/\delta))$ symbols and $O(k \ln(k/\delta))$ XORs.
- *[Raptor codes](/raptor-codes/)* (Shokrollahi 2006). First extend $s$ with a high-rate precode, then apply an LT code with constant mean degree. This gives linear-time encoding and decoding with a constant overhead. RaptorQ (RFC 6330) is the standard form.

## Examples and non-examples

**Failure of the random linear fountain.** The probability that $K = k + E$ uniform random vectors span $\mathrm{GF}(2)^k$ is

$$\prod_{i=0}^{k-1} \bigl(1 - 2^{\,i - K}\bigr), \qquad \text{so} \qquad \Pr[\text{failure}] \le \sum_{i=0}^{k-1} 2^{\,i-K} < 2^{-E}.$$

For $k = 1000$ the exact failure probabilities are

| extra symbols $E$ | 0 | 1 | 2 | 5 | 10 |
|---|---|---|---|---|---|
| $\Pr[\text{failure}]$ | 0.711 | 0.422 | 0.230 | 0.031 | 0.00098 |

The expected number of symbols until the rank reaches $k$ is $\sum_{j=1}^{k} 2^j/(2^j - 1) = k + \sum_{j=1}^{k} 1/(2^j - 1)$, which is $k + 1.6067$ for large $k$. So the random linear fountain needs on average fewer than two extra symbols, whatever $k$ is. The tests check the formula against brute force for small matrices, and against 1500 simulated receptions for $k = 16$.

**An LT code.** With $k = 500$ and the robust soliton ($c = 0.1$, $\delta = 0.5$), peeling decoded 16 of 20 trials at 25 percent overhead and all 20 at 50 percent (see [LT codes](/lt-codes/)). The overhead is larger than that of the random linear fountain, and the decoding cost is far lower.

**Non-example: a data carousel.** The sender repeats the $k$ source packets in a fixed cycle. Each receiver must catch every one of the $k$ packets, so a receiver that misses a packet waits for the next cycle. With independent losses at rate $p$, the number of cycles grows like $\log_{1/p} k$, and the waste grows with $k$. Byers et al. used the carousel as the baseline that the digital fountain beats.

**Non-example: a fixed Reed-Solomon code.** A [Reed-Solomon code](/reed-solomon-code/) $[n, k]_q$ recovers from any $k$ of its $n$ symbols, which is the ideal reception. But it is not rateless: $n \le q$ is fixed in advance, and a receiver that loses more than $n - k$ symbols cannot be served by sending more from the same code. Its decoding also costs order $k^2$ or $k \log^2 k$ field operations per block, more than peeling.

**Non-example: retransmission with feedback.** A protocol that sends each lost packet again on request (like TCP) also delivers everything, but each receiver needs a feedback channel and its own retransmissions. A fountain serves many receivers with one stream.

## Related definitions

- [LT codes](/lt-codes/) and [Raptor codes](/raptor-codes/): the main practical fountain codes.
- [Erasure codes](/erasure-codes/): the fixed-rate setting. A fountain code is an erasure code whose length is chosen by the receivers.
- [Erasure decoding](/erasure-decoding/): the decoding problem of each fountain code, a linear system over $\mathrm{GF}(2)$.
- [Network coding](/network-coding/): random linear network coding sends random combinations of packets through a network; it is a random linear fountain in which inner nodes also mix packets.
- Online codes (Maymounkov 2002) are another construction of the precode plus sparse fountain kind, found at the same time as Raptor codes.

## References

- John W. Byers, Michael Luby, Michael Mitzenmacher and Ashutosh Rege, "A digital fountain approach to reliable distribution of bulk data", SIGCOMM 1998.
- Michael Luby, "LT codes", FOCS 2002.
- Amin Shokrollahi, "Raptor codes", IEEE Transactions on Information Theory 52(6), 2006.
- David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003, Chapter 50.
