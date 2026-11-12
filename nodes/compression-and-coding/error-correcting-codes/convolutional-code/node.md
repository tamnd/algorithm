---
tag: F34YG7
kind: definition
slug: convolutional-code
name: Convolutional code
area: compression-and-coding/error-correcting-codes
level: core
summary: A linear code whose encoder is a shift register over GF(2). Each input bit gives n output bits that depend on it and on the last m inputs. Its strength is the free distance.
history:
  year: 1955
  people: [Peter Elias]
  note: Elias introduced convolutional codes in 1955. Massey and Sain gave the test for catastrophic encoders in 1968, and Forney gave the algebraic theory of encoders in 1970.
prereqs: [linear-code, generator-matrix, gf2-polynomial-arithmetic]
see_also: [trellis, maximum-likelihood-sequence-estimation, bcjr-algorithm, turbo-code, linear-feedback-shift-register, concatenated-codes, reed-solomon-code, viterbi-algorithm]
sources:
  - paper: "P. Elias, Coding for noisy channels, IRE Convention Record, Part 4, 1955, pages 37 to 46"
    title: Coding for noisy channels
    locator: The introduction of convolutional codes, where the check digits are mod 2 sums of a sliding window of message digits
  - paper: "J. L. Massey and M. K. Sain, Inverses of linear sequential circuits, IEEE Transactions on Computers C-17(4), 1968, pages 330 to 337"
    title: Inverses of linear sequential circuits
    locator: The condition for a feedforward inverse of a convolutional encoder, the gcd test for catastrophic encoders
  - paper: "G. D. Forney, Jr., Convolutional codes I: Algebraic structure, IEEE Transactions on Information Theory 16(6), 1970, pages 720 to 738"
    title: "Convolutional codes I: Algebraic structure"
    locator: Generator matrices over polynomials and rational functions, equivalent encoders, minimal and non-catastrophic encoders
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 11 (encoding of convolutional codes, structural properties, distance properties, catastrophic encoders) and Chapter 12 (tables of codes with the largest free distance)
  - url: https://ccsds.org/Pubs/131x0b5.pdf
    title: CCSDS 131.0-B-5, TM Synchronization and Channel Coding, Recommended Standard, September 2023
    locator: Section 3 (convolutional coding), the basic rate 1/2 code with constraint length 7, G1 = 1111001, G2 = 1011011 and the inversion of the G2 output, and the punctured rates
  - paper: "IEEE Std 802.11, Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications"
    title: IEEE Std 802.11, Wireless LAN MAC and PHY Specifications
    locator: Clause 17 (OFDM PHY), the convolutional encoder with g0 = 133 and g1 = 171 octal, constraint length 7, and puncturing to the rates 2/3 and 3/4
---

A convolutional code is a [linear code](/linear-code/) whose encoder is a shift register over GF(2): each input bit enters a register of the last $m$ inputs, and $n$ fixed mod 2 sums of the register give $n$ output bits. Unlike a block code, the input is a stream, and each output bit depends on a window of $m + 1$ input bits. The code is decoded on its [trellis](/trellis/), by the [Viterbi algorithm](/maximum-likelihood-sequence-estimation/) for the most likely sequence or by the [BCJR algorithm](/bcjr-algorithm/) for bit posteriors. Recursive convolutional encoders are the parts of a [turbo code](/turbo-code/).

## Definition

Vectors are rows, arithmetic is in GF(2), and a sequence $x_0, x_1, \ldots$ is written as a power series $x(D) = \sum_t x_t D^t$ in the delay variable $D$. Products of such series are [polynomial products over GF(2)](/gf2-polynomial-arithmetic/).

**Rate $1/n$ feedforward encoder.** Fix $n$ generator polynomials $g^{(1)}(D), \ldots, g^{(n)}(D)$ of degree at most $m$, with at least one of degree exactly $m$. The memory is $m$ and the constraint length is $K = m + 1$. The input $u(D)$ gives the $n$ output streams

$$v^{(j)}(D) = u(D)\, g^{(j)}(D), \qquad j = 1, \ldots, n,$$

that is, $v^{(j)}_t = \sum_{i=0}^{m} g^{(j)}_i u_{t-i}$ with $u_t = 0$ for $t < 0$. The encoder sends $v^{(1)}_t, \ldots, v^{(n)}_t$ at time $t$, so the rate is $R = 1/n$. The state at time $t$ is $(u_{t-1}, \ldots, u_{t-m})$, so there are $2^m$ states.

**Rate $k/n$ and recursive encoders.** In general a $k \times n$ generator matrix $G(D)$ with entries that are polynomials, or rational functions $a(D)/b(D)$ with $b_0 = 1$, maps $k$ input streams to $n$ output streams by $v(D) = u(D) G(D)$. An entry with a denominator is a feedback shift register, which is an [LFSR](/linear-feedback-shift-register/). The encoder $(1, g^{(2)}/g^{(1)})$ is *recursive systematic* (RSC): its first output is the input.

**The code.** The convolutional code is the set of all output sequences $\{u(D) G(D)\}$. Two encoders are *equivalent* when they give the same set. For example $(g^{(1)}, g^{(2)})$ and $(1, g^{(2)}/g^{(1)})$ are equivalent: the input $u' = u g^{(1)}$ to the second gives the output of $u$ in the first. Equivalent encoders have the same distances but map inputs to outputs differently.

**Free distance.** The free distance is the least [Hamming weight](/hamming-weight/) of a nonzero code sequence:

$$d_{\text{free}} = \min \{\, \mathrm{wt}(u(D) G(D)) : u(D) \ne 0 \,\}.$$

The code is linear, so this is also the least [Hamming distance](/hamming-distance/) between two distinct code sequences. On the trellis it is the least weight of a path that leaves the zero state and comes back to it. Each path of a terminated code (below) leaves state 0 and comes back to it, so the terminated code has minimum distance at least $d_{\text{free}}$, and a maximum likelihood decoder with hard decisions on the [BSC](/binary-symmetric-channel/) corrects every pattern of at most $\lfloor (d_{\text{free}} - 1)/2 \rfloor$ errors. The weight spectrum lists $A_d$, the number of such paths of output weight $d$, and $B_d$, the total input weight of these paths. The [union bound](/union-bound/) on the bit error rate of [MLSE](/maximum-likelihood-sequence-estimation/) uses $B_d$.

**Catastrophic encoders.** An encoder is catastrophic when some input of infinite weight gives an output of finite weight. Then a finite number of channel errors can cause an infinite number of decoded bit errors.

*Theorem (Massey and Sain, 1968).* A rate $1/n$ feedforward encoder is catastrophic if and only if $\gcd(g^{(1)}, \ldots, g^{(n)})$ is not a power of $D$.

*Proof.* Let $g = \gcd(g^{(1)}, \ldots, g^{(n)})$. If $g$ is not a power of $D$, take the input $u = 1/g$ as a power series (it exists because we can divide out the power of $D$ and then $g_0 = 1$). It has infinite weight: if $1/g$ were a polynomial $p$, then $g p = 1$, so $g$ would be a unit of GF(2)[$D$], that is $g = 1$. The outputs $u g^{(j)} = g^{(j)}/g$ are polynomials, so the output weight is finite. Conversely, if $g = D^l$, Bezout's identity for polynomials gives $a_1, \ldots, a_n$ with $\sum_j a_j g^{(j)} = D^l$. Then $u = D^{-l} \sum_j a_j v^{(j)}$, so an output of finite weight comes from an input of finite weight. $\square$

**Termination, truncation and tail-biting.** A block of $L$ input bits followed by $m$ zero bits drives the register back to state 0. This is a *terminated* code, a block code of rate $L / (n(L + m))$. A *tail-biting* code instead starts the register in the state of the last $m$ input bits, so it starts and ends in the same state with no rate loss. A *truncated* code just stops, and its last bits are less protected.

**Puncturing.** A puncturing pattern is an $n \times P$ matrix of 0 and 1. Over each period of $P$ input bits, the encoder sends output $j$ at time $t$ only if entry $(j, t \bmod P)$ is 1. With the rate 1/2 mother code and the pattern with rows $11$ and $10$, the encoder sends 3 bits for every 2 input bits, so the rate is 2/3. One decoder serves all rates: it puts an LLR of 0 at the deleted positions.

## Examples and non-examples

**The (7, 5) code.** The generators in octal are 7 and 5, that is $g^{(1)} = 1 + D + D^2$ and $g^{(2)} = 1 + D^2$, with $m = 2$ and 4 states. In this page the leftmost of the $K$ binary digits of an octal number is the tap of $D^0$. The input 1011 with two tail zeros gives

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $u_t$ | 1 | 0 | 1 | 1 | 0 | 0 |
| $v^{(1)}_t v^{(2)}_t$ | 11 | 10 | 00 | 01 | 01 | 11 |

The free distance is 5: the input 1 gives the path 11 10 11. The spectrum is $A_d = 2^{d-5}$ and $B_d = (d - 4)\, 2^{d-5}$ for $d \ge 5$, so $(A_5, A_6, A_7) = (1, 2, 4)$ and $(B_5, B_6, B_7) = (1, 4, 12)$.

**The constraint length 7 standard code.** CCSDS 131.0-B-5 Section 3 defines the rate 1/2 code with $G1 = 1111001$ (171 octal) and $G2 = 1011011$ (133 octal). It sends the G1 symbol first and inverts the G2 symbol. IEEE 802.11 Clause 17 uses the same two generators but names them $g_0 = 133$ and $g_1 = 171$, sends the 133 output first, and does not invert. So the two standards use the same code with a different order of the two outputs and a different sign. Its free distance is 10, with $A_{10} = 11$, $A_{12} = 38$, $A_{14} = 193$ and $B_{10} = 36$, $B_{12} = 211$, $B_{14} = 1404$. The odd weights are absent. Over GF(2) the weight of a polynomial $p$ has the parity of $p(1)$, and both generators have 5 taps, so $g^{(1)}(1) = g^{(2)}(1) = 1$. Then $\mathrm{wt}(u g^{(1)}) + \mathrm{wt}(u g^{(2)}) \equiv 2 u(1) \equiv 0 \pmod 2$.

**The largest free distance for rate 1/2.** For the constraint lengths 3 to 7, the codes (7, 5), (15, 17), (23, 35), (53, 75) and (171, 133) have the free distances 5, 6, 7, 8 and 10. These are the values of the tables of codes with the largest free distance in Lin and Costello, Chapter 12.

**A recursive systematic encoder.** The RSC encoder $(1, 5/7)$, that is $(1, (1 + D^2)/(1 + D + D^2))$, gives the same code as (7, 5). An input of weight 1 never brings it back to state 0, because $1 + D + D^2$ does not divide 1. The input $1 + D^3$ is a multiple of $1 + D + D^2$, so it gives the finite parity $1 + D + D^2 + D^3$, the stream 1111. The turbo code uses this property.

**Non-example: a catastrophic encoder.** The generators 6 and 5 octal are $1 + D$ and $1 + D^2 = (1 + D)^2$, with the common factor $1 + D$. The all-ones input $u = 1/(1 + D)$ has infinite weight, but the outputs are $1$ and $1 + D$, of total weight 3. So 3 channel errors can make the decoder output the all-ones stream in place of the all-zeros stream. This encoder generates a code, but no practical system uses it. The equivalent encoder $(1, 1 + D)$ is not catastrophic.

**Non-example: a block code.** A block code with no memory between blocks is the case $m = 0$, with $G(D) = G$ constant. The free distance is then the [minimum distance](/minimum-distance/) of the block code, and the trellis has a single state at each step between blocks. The name convolutional code is used for $m \ge 1$.

## Related definitions

- [Trellis](/trellis/): the graph of the states of the encoder over time. Each code sequence is a path.
- [Maximum-likelihood sequence estimation](/maximum-likelihood-sequence-estimation/): the decoding problem that the Viterbi algorithm solves on the trellis. The general [Viterbi algorithm](/viterbi-algorithm/) of hidden Markov models is the same recursion on a model with learned probabilities.
- [BCJR algorithm](/bcjr-algorithm/): the posterior of each bit on the same trellis.
- [Turbo code](/turbo-code/): two recursive systematic convolutional encoders with an [interleaver](/interleaving/) between them.
- [Concatenated codes](/concatenated-codes/): CCSDS uses the K = 7 code as the inner code with a [Reed-Solomon code](/reed-solomon-code/) as the outer code.
- [Generator matrix](/generator-matrix/): the block code analogue of $G(D)$.
- [Linear feedback shift register](/linear-feedback-shift-register/): the circuit of a recursive encoder. A [cyclic redundancy check](/cyclic-redundancy-check/) also divides by a polynomial, but over a finite block, for detection only.

## References
