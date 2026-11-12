---
tag: HJNNKN
kind: definition
slug: polar-code
name: Polar code
aliases:
- Arikan polar code
- Arıkan polar code
area: compression-and-coding/error-correcting-codes
level: research
summary: "Linear code whose codewords are u F^(kron n), with information bits on the most reliable synthetic channels and zeros on the rest. It reaches capacity with SC decoding."
history:
  year: 2009
  people: [Erdal Arıkan]
  note: Arıkan defined polar codes in 2009. Tal and Vardy gave list decoding with a CRC in 2011 (journal 2015). 3GPP chose polar codes for 5G NR control channels in 2016.
prereqs: [channel-polarization-theorem, linear-code]
see_also: [successive-cancellation-decoding, reed-muller-code, list-decoding, cyclic-redundancy-check, binary-erasure-channel, additive-white-gaussian-noise-channel, ldpc-code, systematic-code]
sources:
  - paper: doi:10.1109/TIT.2009.2021379
    title: Erdal Arıkan, Channel polarization, a method for constructing capacity-achieving codes for symmetric binary-input memoryless channels, IEEE Transactions on Information Theory 55(7), 2009, pages 3051 to 3073
    locator: Section V (polar coding, the coset codes G_N(A, u_Ac) and the choice of A by Bhattacharyya parameters), Section VII (the O(N log N) encoder) and Section VIII (the SC decoder)
  - paper: doi:10.1109/TIT.2013.2272694
    title: Ido Tal and Alexander Vardy, How to construct polar codes, IEEE Transactions on Information Theory 59(10), 2013
    locator: The upgrading and degrading merge functions that bound the error probability of each synthetic channel
  - paper: doi:10.1109/TIT.2015.2410251
    title: Ido Tal and Alexander Vardy, List decoding of polar codes, IEEE Transactions on Information Theory 61(5), 2015, pages 2213 to 2226
    locator: The successive cancellation list decoder and its CRC-aided form
  - paper: doi:10.1109/TCOMM.2012.081512.110872
    title: Peter Trifonov, Efficient design and decoding of polar codes, IEEE Transactions on Communications 60(11), 2012
    locator: The Gaussian approximation for the construction of polar codes on the AWGN channel
  - paper: doi:10.1109/TSP.2015.2439211
    title: Alexios Balatsoukas-Stimming, Mani Bastani Parizi and Andreas Burg, LLR-based successive cancellation list decoding of polar codes, IEEE Transactions on Signal Processing 63(19), 2015
    locator: The path metric in the LLR domain
  - url: https://www.3gpp.org/ftp/Specs/archive/38_series/38.212/
    title: 3GPP TS 38.212, NR, Multiplexing and channel coding, V16.9.0 (2022-03)
    locator: Section 5.3.1 (polar coding, x = u G_N with G_N the n-th Kronecker power of F) and Table 5.3.1.2-1 (the polar sequence Q_0^(Nmax - 1) with Nmax = 1024)
---

A polar code is a binary [linear code](/linear-code/) of length $N = 2^n$ whose codewords are $x = u F^{\otimes n}$. The vector $u$ carries the message on $K$ chosen positions and fixed zeros on the other $N - K$ positions. The chosen positions are the synthetic channels that the [channel polarization theorem](/channel-polarization-theorem/) makes nearly noiseless. Erdal Arıkan defined polar codes in 2009 and proved that, with [successive cancellation decoding](/successive-cancellation-decoding/), they reach the symmetric capacity of each binary-input memoryless channel. They have an explicit construction, $O(N \log N)$ encoding and decoding, and a proof that they reach capacity.

## Definition

**Notation.** Vectors are rows over $\mathrm{GF}(2)$, $\oplus$ is addition modulo 2, and indices run from $0$ to $N - 1$. An $[N, K, d]$ code has length $N$, dimension $K$ and [minimum distance](/minimum-distance/) $d$. The rate is $R = K / N$. $W$ is a binary-input memoryless channel, $W_N^{(i)}$ is its $i$-th synthetic channel and $Z(\cdot)$ is the Bhattacharyya parameter, all as on the [channel polarization theorem](/channel-polarization-theorem/) page. $\mathrm{wt}(i)$ is the number of ones in the binary form of the integer $i$.

**The transform.** Let $F = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$ and let $F^{\otimes n}$ be its $n$-th [Kronecker power](/kronecker-product/). Row $i$ of $F^{\otimes n}$ has weight $2^{\mathrm{wt}(i)}$.

**Definition (polar code).** Fix $N = 2^n$, a channel $W$ and $1 \le K \le N$. Let $\mathcal{A} \subseteq \{0, \ldots, N - 1\}$ be a set of $K$ indices with the smallest values of $Z(W_N^{(i)})$ (ties broken by any fixed rule). The *information set* is $\mathcal{A}$ and the *frozen set* is its complement $\mathcal{A}^c$. The polar code $\mathcal{P}(N, K, W)$ is

$$\mathcal{P}(N, K, W) = \bigl\{\, u F^{\otimes n} : u \in \mathrm{GF}(2)^N,\ u_i = 0 \text{ for each } i \in \mathcal{A}^c \,\bigr\}.$$

Its [generator matrix](/generator-matrix/) is the $K \times N$ submatrix of $F^{\otimes n}$ with the rows in $\mathcal{A}$. Arıkan allows any fixed values on the frozen positions (a coset code). On a symmetric channel the value does not change the error probability, so zeros are the usual choice.

**Bit order.** Arıkan writes $G_N = B_N F^{\otimes n}$, where $B_N$ is the [bit-reversal permutation](/bit-reversal-permutation/). $B_N$ only permutes the code bits, so it does not change $\mathcal{A}$ or the error probability. 3GPP TS 38.212 and this page use $x = u F^{\otimes n}$ with no bit reversal.

**Encoding.** Compute $x = u F^{\otimes n}$ with $n$ stages of butterflies. At stage $h = 1, 2, 4, \ldots, N/2$, for each block of $2h$ positions starting at $s$ and each $j \in [s, s + h)$, replace $x_j$ by $x_j \oplus x_{j+h}$. That is $(N/2) \log_2 N$ XOR operations, so encoding takes $O(N \log N)$ time, like the [fast Walsh-Hadamard transform](/fast-walsh-hadamard-transform/).

**Choice of the information set.** The definition needs the order of the $Z(W_N^{(i)})$:

- On BEC($\varepsilon$) the order is exact and cheap. Write $i$ in binary with $n$ digits, start from $z = \varepsilon$, and read the digits from the most significant one: replace $z$ by $2z - z^2$ for a $0$ and by $z^2$ for a $1$. All $N$ values take $O(N)$ operations.
- On the [AWGN channel](/additive-white-gaussian-noise-channel/) the usual tool is the Gaussian approximation of density evolution (Trifonov 2012). It tracks one mean LLR per synthetic channel.
- On a general channel Tal and Vardy (2013) replace each synthetic channel by an upgraded and a degraded channel with a bounded output alphabet. This gives upper and lower bounds on each error probability in $O(N \mu^2 \log \mu)$ time for alphabet size $\mu$.
- 5G NR fixes one order for all lengths. Table 5.3.1.2-1 of TS 38.212 lists the indices $0$ to $1023$ from the least reliable to the most reliable. For length $N$, keep the entries below $N$ in the same order and take the last $K$ of them. The table begins $0, 1, 2, 4, 8, 16, 32, 3, 5, 64, 9, 6, 17, 10, 18, 128, 12, 33, 65, 20, \ldots$ The real 5G encoder also places CRC bits, parity-check bits and rate matching on top of this. The implementation copies the first 80 entries by hand and uses them only for $N \le 16$.

**Minimum distance.** Let $\mathcal{C}(\mathcal{A})$ be the code spanned by the rows of $F^{\otimes n}$ in a nonempty set $\mathcal{A}$. Then

$$d\bigl(\mathcal{C}(\mathcal{A})\bigr) = \min_{i \in \mathcal{A}} 2^{\mathrm{wt}(i)}.$$

*Proof.* Induction on $n$. For $n = 0$ the code is $\{0, 1\}$ and $d = 1 = 2^0$. For the step, $F^{\otimes (n+1)} = \begin{pmatrix} G & 0 \\ G & G \end{pmatrix}$ with $G = F^{\otimes n}$. Split $u = (a, b)$ into halves. Then $x = (aG \oplus bG,\ bG)$. Let $\mathcal{A}_0 = \mathcal{A} \cap [0, N)$ and $\mathcal{A}_1 = \{ i - N : i \in \mathcal{A},\ i \ge N \}$, and let $v = aG \in \mathcal{C}(\mathcal{A}_0)$, $w = bG \in \mathcal{C}(\mathcal{A}_1)$. A nonzero codeword is $(v \oplus w, w)$. If $v = 0$, its weight is $2\,\mathrm{wt}(w) \ge 2\, d(\mathcal{C}(\mathcal{A}_1))$. If $v \ne 0$, its weight is $\mathrm{wt}(v \oplus w) + \mathrm{wt}(w) \ge \mathrm{wt}(v) \ge d(\mathcal{C}(\mathcal{A}_0))$. Both bounds are reached: take $v = 0$ and $w$ of least weight, or $w = 0$ and $v$ of least weight. So $d = \min\bigl(2\, d(\mathcal{C}(\mathcal{A}_1)),\ d(\mathcal{C}(\mathcal{A}_0))\bigr)$, with $d$ of an empty set read as $\infty$. An index $i \in \mathcal{A}_1$ is the index $i + N \in \mathcal{A}$, which has one more binary one, so $2 \cdot 2^{\mathrm{wt}(i)} = 2^{\mathrm{wt}(i+N)}$. The induction hypothesis on both halves gives the formula. $\blacksquare$

This is the Plotkin $(u \mid u + v)$ construction applied $n$ times. The tests check the formula against brute force on random sets $\mathcal{A}$ for $N = 8$ and $16$.

**Decoding.** The decoder knows $\mathcal{A}$ and the frozen values.

- [Successive cancellation (SC)](/successive-cancellation-decoding/) decides $u_0, u_1, \ldots, u_{N-1}$ in order. It uses the earlier decisions and sets each frozen bit to its known value. It runs in $O(N \log N)$ time. Arıkan's union bound gives block error probability at most $\sum_{i \in \mathcal{A}} Z(W_N^{(i)})$.
- SC list (SCL) decoding keeps up to $L$ paths. At each information bit it extends each path with both values and keeps the $L$ paths with the best metric. It takes $O(L N \log N)$ time (Tal and Vardy 2015). With $L = 2^K$ no path is ever dropped, so SCL is [maximum likelihood decoding](/maximum-likelihood-decoding/).
- CRC-aided SCL (CA-SCL) puts a [cyclic redundancy check](/cyclic-redundancy-check/) of $r$ bits on the last $r$ information positions. At the end it returns the best path that passes the check. In the simulations of Tal and Vardy, this made short polar codes better than LDPC codes of similar length. 5G NR uses this form.

**Capacity.** For each $\beta < 1/2$ and each rate $R < I(W)$, polar codes with $K = \lceil NR \rceil$ and SC decoding have block error probability $O(2^{-N^{\beta}})$ (Arıkan 2009 for the capacity part, Arıkan and Telatar 2009 for the exponent).

## Examples and non-examples

**Length 8 on BEC(1/2).** The recursion gives $Z(W_8^{(i)})$ for $i = 0, \ldots, 7$ as

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $\mathrm{wt}(i)$ | 0 | 1 | 1 | 2 | 1 | 2 | 2 | 3 |
| $256\, Z$ | 255 | 225 | 207 | 81 | 175 | 49 | 31 | 1 |

For $K = 4$ the information set is $\mathcal{A} = \{3, 5, 6, 7\}$. The least weight of these indices is 2, so $d = 2^2 = 4$ and the code is $[8, 4, 4]$. It is the first-order [Reed-Muller code](/reed-muller-code/) RM(1, 3). The 5G sequence restricted to $N = 8$ is $0, 1, 2, 4, 3, 5, 6, 7$, and its last four entries give the same set.

**Encoding a message.** Put the message $(1, 1, 1, 0)$ on $\mathcal{A} = \{3, 5, 6, 7\}$, so $u = (0, 0, 0, 1, 0, 1, 1, 0)$. The three butterfly stages give

| after stage | vector |
|---|---|
| start | 0 0 0 1 0 1 1 0 |
| $h = 1$ | 0 0 1 1 1 1 1 0 |
| $h = 2$ | 1 1 1 1 0 1 1 0 |
| $h = 4$ | 1 0 0 1 0 1 1 0 |

So $x = (1, 0, 0, 1, 0, 1, 1, 0)$, a codeword of weight 4. The [successive cancellation decoding](/successive-cancellation-decoding/) page decodes this word after one channel error.

**Length 16, rate 1/2.** On BEC(1/2) the information set is $\{7, 9, 10, 11, 12, 13, 14, 15\}$. The 5G sequence gives $\{6, 7, 10, 11, 12, 13, 14, 15\}$. The two sets differ in one index: $Z(W_{16}^{(6)}) \approx 0.533$ and $Z(W_{16}^{(9)}) \approx 0.467$ on BEC(1/2), so the BEC order prefers 9. The 5G order is a single order for many channels and lengths. For every other $K$ from 1 to 16 the two orders give the same set at $N = 16$.

**CRC-aided list decoding.** Take $N = 64$, $K = 32$ with the BEC(1/2) information set, 26 data bits and a 6-bit CRC with generator $x^6 + x + 1$ on the last 6 information positions. Send BPSK over the AWGN channel with noise standard deviation $\sigma = 0.8$, which is $E_b/N_0 = 1/(2 R \sigma^2) \approx 2.84$ dB with $R = 26/64$. Here $E_b$ is the energy per data bit and $N_0/2 = \sigma^2$ is the noise variance per real dimension. In one run of 1000 frames with a fixed seed, SC decoding had 123 frame errors, SCL with $L = 8$ and no CRC had 86, and CA-SCL with $L = 8$ had 11. The test runs a shorter version of this experiment.

**Non-example: a Reed-Muller code is not a polar code in general.** RM($r$, $n$) takes all rows of $F^{\otimes n}$ with $\mathrm{wt}(i) \ge n - r$, which maximizes the minimum distance. A polar code takes the rows with the best synthetic channels. For $N = 32$, $K = 16$ on BEC(1/2), the polar information set contains $24 = (11000)_2$ in place of $7 = (00111)_2$. So the polar code has $d = 2^2 = 4$, while RM(2, 5) is a $[32, 16, 8]$ code. The polar code has the smaller distance and the better SC error probability.

**Non-example: picking $K$ rows at random.** A random set of $K$ rows of $F^{\otimes n}$ is a valid linear code with the same encoder and decoder. It is not a polar code, because the set is not chosen by the reliabilities of the synthetic channels. With SC decoding such a code has no capacity guarantee: one unreliable information index already makes the block error probability large.

**Non-example: the rate-one case.** $K = N$ gives the whole space $\mathrm{GF}(2)^N$. It fits the formula, but there are no frozen bits and $d = 1$, so it gives no protection. It is a valid building block in fast SC decoders, not a useful polar code by itself.

## Related definitions

- [Channel polarization theorem](/channel-polarization-theorem/): the fact that makes the information set work.
- [Successive cancellation decoding](/successive-cancellation-decoding/): the decoder for which polar codes are designed, and the base of SCL and CA-SCL.
- [Reed-Muller code](/reed-muller-code/): uses the same rows $F^{\otimes n}$, chosen by weight in place of reliability.
- [Systematic code](/systematic-code/): Arıkan (2011) gave a systematic polar encoder in which the message bits appear in the codeword, with the same code and a better bit error rate.
- [List decoding](/list-decoding/): SCL is a list decoder in a different sense, it keeps a list of candidate paths and outputs one word.
- [LDPC code](/ldpc-code/) and [turbo code](/turbo-code/): the other capacity-approaching families. 5G NR uses LDPC codes for data channels and polar codes for control channels.

## References

- Erdal Arıkan, "Channel polarization, a method for constructing capacity-achieving codes for symmetric binary-input memoryless channels", IEEE Transactions on Information Theory 55(7), 2009, pages 3051 to 3073.
- Ido Tal and Alexander Vardy, "How to construct polar codes", IEEE Transactions on Information Theory 59(10), 2013.
- Ido Tal and Alexander Vardy, "List decoding of polar codes", IEEE Transactions on Information Theory 61(5), 2015, pages 2213 to 2226.
- Peter Trifonov, "Efficient design and decoding of polar codes", IEEE Transactions on Communications 60(11), 2012.
- Alexios Balatsoukas-Stimming, Mani Bastani Parizi and Andreas Burg, "LLR-based successive cancellation list decoding of polar codes", IEEE Transactions on Signal Processing 63(19), 2015.
- 3GPP TS 38.212, "NR, Multiplexing and channel coding", V16.9.0, 2022, Section 5.3.1 and Table 5.3.1.2-1.
