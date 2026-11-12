---
tag: 1YD9K5
kind: definition
slug: lt-codes
name: LT codes
aliases:
- Luby transform codes
- Luby transform code
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "Rateless erasure codes: each encoded symbol is the XOR of d random source symbols, d drawn from a soliton distribution. Peeling decodes k symbols from slightly more than k."
history:
  year: 2002
  people: [Michael Luby]
  note: Luby published LT codes, the ideal and robust soliton distributions and their analysis at FOCS 2002.
prereqs: [fountain-codes, peeling-decoding]
see_also: [raptor-codes, erasure-codes, binary-erasure-channel, coupon-collector-problem, balls-into-bins, ldpc-code, tanner-graph, erasure-decoding]
sources:
  - paper: doi:10.1109/SFCS.2002.1181950
    title: Michael Luby, LT codes, Proceedings of the 43rd Annual IEEE Symposium on Foundations of Computer Science (FOCS), 2002, pages 271 to 280
    locator: The LT encoding and decoding processes, the ideal soliton distribution, the robust soliton distribution with R = c ln(k/δ) sqrt(k), and the theorem that kβ encoding symbols suffice with probability at least 1 - δ
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 50 (digital fountain codes, the LT decoder, and the robust soliton example with K = 10000, c = 0.2, δ = 0.05)
  - paper: doi:10.1109/TIT.2006.874390
    title: Amin Shokrollahi, Raptor codes, IEEE Transactions on Information Theory 52(6), 2006, pages 2551 to 2567
    locator: Section on LT codes (the lower bound of order ln(k) on the average degree of an LT code that recovers all symbols)
---

LT codes, for *Luby transform*, are sparse [fountain codes](/fountain-codes/) with a fast decoder. The encoder makes as many encoded symbols as needed, each the XOR of a random set of source symbols whose size comes from a carefully chosen distribution. The receiver collects any slightly more than $k$ of them, in any order, and recovers the $k$ source symbols with the [peeling decoder](/peeling-decoding/). Michael Luby introduced them in 2002.

## Definition

**Notation.** The message has $k$ *source symbols* $s_0, \ldots, s_{k-1}$, each a string of bits of the same length (a packet), and $\oplus$ is bitwise XOR. The encoder produces *encoded symbols* $e_0, e_1, \ldots$ without limit. The receiver gets $K$ of them; the *overhead* is $\varepsilon = K/k - 1$. A degree distribution is a probability distribution $\mu$ on $\{1, \ldots, k\}$.

**Definition (LT code).** Given $k$ and a degree distribution $\mu$, encoded symbol $e_j$ is made as follows:

1. draw a degree $d$ with $\Pr[d] = \mu(d)$;
2. choose $d$ distinct source indices $N_j \subseteq \{0, \ldots, k-1\}$ uniformly at random;
3. set $e_j = \bigoplus_{i \in N_j} s_i$.

Each draw is independent. In practice both sides compute $d$ and $N_j$ from a pseudorandom generator seeded by the index $j$, so a packet carries only $j$ and $e_j$. The code is linear over $\mathrm{GF}(2)$, acting the same way on each bit position of the packets, and it has no fixed length: it is *rateless*.

**Decoding.** The decoder is the [peeling decoder](/peeling-decoding/) on the bipartite graph between the received encoded symbols and the source symbols. An encoded symbol with one unknown neighbor gives that source symbol; its value is then XORed out of every other encoded symbol that contains it. Luby calls the set of source symbols that are found but not yet removed from the graph the *ripple*. Decoding fails if the ripple becomes empty before all $k$ symbols are found.

**Ideal soliton distribution.**

$$\rho(1) = \frac{1}{k}, \qquad \rho(d) = \frac{1}{d(d-1)} \quad (d = 2, \ldots, k).$$

The sum telescopes to $1/k + (1 - 1/k) = 1$, and the mean degree is $1/k + H_{k-1} \approx \ln k$, where $H_m$ is the $m$-th harmonic number. Luby showed that with $k$ encoded symbols, in expectation exactly one encoded symbol reaches degree one at each step of the decoder. So the expected ripple stays at size one, and any random fluctuation empties it. The ideal soliton works in expectation and badly in practice.

**Robust soliton distribution.** Fix $c > 0$ and a failure bound $\delta \in (0, 1)$, and let

$$R = c \ln(k/\delta) \sqrt{k}.$$

Define

$$\tau(d) = \begin{cases} \dfrac{R}{d k} & d = 1, \ldots, k/R - 1, \\[2mm] \dfrac{R \ln(R/\delta)}{k} & d = k/R, \\[2mm] 0 & d > k/R, \end{cases} \qquad \beta = \sum_{d=1}^{k} \bigl(\rho(d) + \tau(d)\bigr), \qquad \mu(d) = \frac{\rho(d) + \tau(d)}{\beta}.$$

Luby assumes that $k/R$ is an integer. When it is not, implementations put the spike at a nearby integer; the implementation here uses $\lfloor k/R \rfloor$. The extra mass $\tau$ keeps the expected ripple at about $R$, which is about $c \ln(k/\delta)$ standard deviations of a random walk of $k$ steps, since one standard deviation is about $\sqrt{k}$, and the spike at $k/R$ makes sure that every source symbol is covered.

**Theorem (Luby 2002).** With the robust soliton distribution, the decoder recovers all $k$ source symbols from any $K = k\beta$ encoded symbols with probability at least $1 - \delta$. Here $k\beta = k + O(\sqrt{k} \ln^2(k/\delta))$, and the mean degree is $O(\ln(k/\delta))$. So encoding costs $O(\ln(k/\delta))$ symbol operations per encoded symbol and decoding costs $O(k \ln(k/\delta))$.

**Lower bound on the degree.** Every source symbol must be a neighbor of some received symbol, or nothing can recover it. With $K \approx k$ received symbols of mean degree $a$, a fixed source symbol is missed with probability about $e^{-a}$, as in the [coupon collector problem](/coupon-collector-problem/). Making the expected number of missed symbols at most $\delta$ needs $a \ge \ln(k/\delta)$ roughly. So any LT code that recovers all symbols with small failure probability has mean degree $\Omega(\ln k)$, and the robust soliton is optimal up to a constant (Luby 2002; Shokrollahi 2006). [Raptor codes](/raptor-codes/) avoid this bound by letting the LT stage miss a few symbols.

## Examples and non-examples

**A small decoding.** Take $k = 4$ source symbols of 4 bits, $s = (0101, 0011, 0110, 0001)$, and five received symbols:

| $j$ | $N_j$ | $e_j$ |
|---|---|---|
| 0 | $\{2\}$ | 0110 |
| 1 | $\{0, 2\}$ | 0011 |
| 2 | $\{1, 2, 3\}$ | 0100 |
| 3 | $\{0, 1\}$ | 0110 |
| 4 | $\{1, 3\}$ | 0010 |

The decoder runs as follows.

| step | degree-one symbol | source found | effect on the others |
|---|---|---|---|
| 1 | $e_0$ | $s_2 = 0110$ | $e_1 \to \{0\}$, value 0101; $e_2 \to \{1, 3\}$, value 0010 |
| 2 | $e_1$ | $s_0 = 0101$ | $e_3 \to \{1\}$, value 0011 |
| 3 | $e_3$ | $s_1 = 0011$ | $e_2 \to \{3\}$, value 0001; $e_4 \to \{3\}$, value 0001 |
| 4 | $e_2$ | $s_3 = 0001$ | $e_4$ becomes empty with value 0000 |

Five symbols decoded four, an overhead of 25 percent. The last symbol was redundant.

**The robust soliton for $k = 10000$.** With $c = 0.2$ and $\delta = 0.05$: $R \approx 244$, $k/R \approx 41$, $\beta \approx 1.31$ and the mean degree is about 14.5. These are the values of MacKay's example. The theorem needs $k\beta \approx 13100$ symbols for the guarantee, but in experiments far fewer are enough: the guarantee is a worst-case bound, and $c$ and $\delta$ act as tuning knobs.

**Success against overhead.** With $k = 500$, $c = 0.1$, $\delta = 0.5$ and fixed seeds, 20 trials at each overhead gave:

| overhead | 5% | 25% | 50% |
|---|---|---|---|
| robust soliton | 0/20 | 16/20 | 20/20 |
| ideal soliton | 0/20 | 4/20 | 12/20 |

With $k = 1000$ and 40 trials, the robust soliton decoded 7 of 40 at 15 percent overhead, 33 of 40 at 20 percent and 40 of 40 at 30 percent. Short LT codes need a noticeable overhead; the relative overhead falls as $k$ grows.

**Non-example: a random linear fountain.** Each encoded symbol is the XOR of a uniformly random subset of the source symbols, so the mean degree is $k/2$. The receiver decodes by Gaussian elimination from $k + E$ symbols with failure probability at most $2^{-E}$. This is a fountain code, but not an LT code: its degrees are not drawn from a sparse distribution. Encoding costs about $k/2$ packet XORs per symbol, and decoding needs a $k \times k$ elimination of order $k^3$ bit operations plus order $k^2$ packet XORs, in place of $O(k \ln k)$ packet XORs.

**Non-example: an LDPC code for the erasure channel.** An [LDPC code](/ldpc-code/) is also decoded by peeling on a sparse graph, but it has a fixed length $n$ and rate $k/n$. If more than $n - k$ symbols are lost, it cannot recover even if the sender is willing to send more.

**Non-example: LT with constant mean degree.** A degree distribution with mean degree bounded by a constant is still an LT code, but it cannot recover all $k$ symbols with small failure probability, by the lower bound above. It recovers all but a small constant fraction, which is what the LT stage of a Raptor code does.

## Related definitions

- [Fountain codes](/fountain-codes/): the general class of rateless codes. LT codes are its basic sparse member.
- [Raptor codes](/raptor-codes/): an LT code with constant mean degree after a high-rate precode. They give linear time encoding and decoding.
- [Peeling decoder](/peeling-decoding/): the decoder of LT codes; the ripple is its queue of degree-one checks.
- [Erasure codes](/erasure-codes/): LT codes are erasure codes that trade a small reception overhead for speed, against MDS codes that need exactly $k$ symbols.
- [Balls into bins](/balls-into-bins/) and the [coupon collector problem](/coupon-collector-problem/): the probability tools behind the analysis of the ripple and of the cover of all source symbols.

## References

- Michael Luby, "LT codes", FOCS 2002, pages 271 to 280.
- David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003, Chapter 50.
- Amin Shokrollahi, "Raptor codes", IEEE Transactions on Information Theory 52(6), 2006.
