---
tag: C5A1BF
kind: algorithm
slug: list-sphere-decoder
name: List sphere decoder
aliases:
- soft-output sphere decoder
area: communications/mimo-communications
level: advanced
summary: A depth-first sphere search that keeps the L best symbol vectors instead of one and computes the bit log-likelihood ratios for the channel decoder from that list.
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {n: the number of transmitted streams, m: the number of receive antennas, M: the constellation size, L: the list size, b: the number of bits per symbol}
  time: {worst: O(n^2 m + n^3 + M^n (n + log M + L))}
  time_llrs: {worst: O(L n b)}
  space: {extra: O(n m + n M + L n)}
properties: {deterministic: true, exact_list: true, list_size_1_is: "exact ML detection", full_list_gives: "exact bit LLRs", needs_noise_level: "only for the LLRs", cost_depends_on_noise: true}
history:
  year: 2003
  people: [Bertrand M. Hochwald, Stephan ten Brink]
  note: "Hochwald and ten Brink introduced the list sphere decoder to compute soft bit values for iterative detection and decoding over a multiple-antenna channel."
prereqs: [mimo-detection, schnorr-euchner-enumeration, soft-demapping]
see_also: [k-best-detector, fincke-pohst-enumeration, turbo-equalization, ldpc-code, closest-vector-problem, v-blast, mmse-mimo-detector, interleaving]
sources:
  - paper: doi:10.1109/TCOMM.2003.809789
    title: Bertrand M. Hochwald and Stephan ten Brink, Achieving near-capacity on a multiple-antenna channel, IEEE Transactions on Communications 51(3), 389-399, 2003
    locator: the list sphere decoder and the computation of bit LLRs from its candidate list
  - paper: doi:10.1109/MSP.2009.932126
    title: Erik G. Larsson, MIMO detection methods - how they work, IEEE Signal Processing Magazine 26(3), 91-95, 2009
    locator: the tree view of MIMO detection after a QR decomposition and the soft output from a list
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: chapter 8, the MIMO receivers that the list sphere decoder improves on
---

The list sphere decoder solves the soft-output form of the [MIMO detection](/mimo-detection/) problem. A channel decoder, for example of an [LDPC code](/ldpc-code/) or a turbo code, needs a log-likelihood ratio (LLR) for each coded bit, not a hard decision. The exact LLR is a sum over all $M^n$ transmitted vectors, which is too much work for large $n$ or $M$. The list sphere decoder runs a depth-first sphere search, as in [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/), but it keeps the $L$ best vectors that it has found instead of one, and it prunes a subtree only when its partial metric is not below the $L$-th best metric in the list. At the end the list holds $L$ vectors with the smallest metrics of all $M^n$ (a theorem). The LLRs then use only the vectors in the list. With $L = 1$ the search is exact ML detection, and with $L = M^n$ the LLRs are exact (both theorems).

## In plain words

The receiver must tell the decoder, for every bit, how sure it is that the bit is 0 or 1. The best answer compares all possible transmitted signals, but there are too many. Most of them fit the received signal very badly and add almost nothing to the answer. So the receiver searches for a short list of the signals that fit best, and it skips every group of signals that cannot get into the list. Then it computes how sure it is about each bit from the list alone. If a bit has the same value in every signal of the list, the receiver says it is very sure, up to a fixed limit.

## The problem

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$ known, $m \ge n$ and full column rank, $x \in \mathcal{S}^n$ for a constellation $\mathcal{S}$ of size $M = 2^b$ with a bit label for each point, and $w \sim \mathcal{CN}(0, N_0 I)$. For bit $j$ of stream $k$, the LLR with equal priors is

$$\Lambda_{k,j} = \ln \frac{\sum_{x : b_{k,j}(x) = 0} e^{-\|y - H x\|^2 / N_0}}{\sum_{x : b_{k,j}(x) = 1} e^{-\|y - H x\|^2 / N_0}},$$

so a positive LLR favors bit 0. The max-log approximation keeps the largest term of each sum:

$$\Lambda_{k,j} \approx \frac{1}{N_0} \Big( \min_{x : b_{k,j}(x) = 1} \|y - H x\|^2 - \min_{x : b_{k,j}(x) = 0} \|y - H x\|^2 \Big).$$

The list sphere decoder returns a list $\mathcal{L}$ of $L$ vectors with the smallest metrics, and the LLRs computed with the sums or minimums restricted to $\mathcal{L}$. A bit value that no vector of $\mathcal{L}$ has gives the LLR $\pm \Lambda_{\max}$, a fixed clipping level.

## The algorithm

As on the [K-best page](/k-best-detector/), let $H^H H = R^H R$ with $R$ upper triangular and a positive diagonal, let $\bar y$ solve $R^H \bar y = H^H y$, and let $c = \|y\|^2 - \|\bar y\|^2$. Then $\|y - H x\|^2 = \|\bar y - R x\|^2 + c$, and $\|\bar y - R x\|^2$ is the sum of the level terms $|\bar y_i - \sum_{j > i} R_{ij} x_j - R_{ii} x_i|^2$ for $i = n$ down to 1. The partial metric of $(x_i, \ldots, x_n)$ is the sum of the terms from $i$ to $n$, and it can only grow as the search goes down.

```pseudo id=main
LIST-SPHERE(y, H, S, L)
L1  (R, ȳ, c) ← TRIANGULARIZE(y, H)
L2  list ← empty; radius ← ∞
L3  SEARCH(n, 0)
L4  return the list, with c added to each metric, best first

SEARCH(i, D)                                ▷ x_{i+1}, ..., x_n are fixed
L5  u ← ȳ_i - Σ_{j>i} R_ij x_j
L6  for each s in S, in increasing order of |u - R_ii s|
L7      D' ← D + |u - R_ii s|²
L8      if D' ≥ radius then break            ▷ the other children are farther
L9      x_i ← s; if i = 1 then insert (D', x) into the list, keep the L best, and if the list is full, radius ← its largest metric
L10     else SEARCH(i - 1, D')
```

Line L6 is the Schnorr-Euchner order: the nearest child first. Because the children come in increasing order of their level term, the break of line L8 is safe: when one child fails the test, all later children fail too. The radius stays infinite until the list holds $L$ vectors, and from then on it is the largest metric in the list, so it can only shrink.

The LLRs come from the list in a second step. For each stream $k$ and bit $j$, split the list by the value of bit $j$ of $x_k$. If both parts are nonempty, the max-log LLR is $(D_1 - D_0) / N_0$ with $D_v$ the smallest metric in the part with value $v$, and the full form is the difference of the two log-sum-exp values of $-D / N_0$. If one part is empty, the LLR is $+\Lambda_{\max}$ when all vectors in the list have bit 0 and $-\Lambda_{\max}$ when all have bit 1. The constant $c$ cancels in every difference.

## Example

Take $m = n = 2$, BPSK with bit 0 on $+1$ and bit 1 on $-1$, $H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$, $y = (0.5, 0.6)$, the received vector of the [ZF example](/zero-forcing-mimo-detector/) for $x = (+1, -1)$, and $N_0 = 1$. As on the [K-best page](/k-best-detector/),

$$R = \frac{1}{\sqrt 5} \begin{pmatrix} 5 & 3 \\ 0 & 1 \end{pmatrix}, \qquad \bar y = \frac{1}{\sqrt 5} (1.6, 0.7), \qquad c = 0.$$

Run the search with $L = 2$. Level 2: the term $(0.7 - x_2)^2 / 5$ is 0.018 for $x_2 = +1$ and 0.578 for $x_2 = -1$, so $x_2 = +1$ comes first. Under $x_2 = +1$, the term $(-1.4 - 5 x_1)^2 / 5$ is 2.592 for $x_1 = -1$ and 8.192 for $x_1 = +1$. Both leaves go into the list, with metrics 2.61 and 8.21, and the list is full, so the radius becomes 8.21. Back at level 2, $x_2 = -1$ has partial metric $0.578 < 8.21$. Under it, $x_1 = +1$ adds $(4.6 - 5)^2 / 5 = 0.032$ for a metric of 0.61, which enters the list and pushes out 8.21. The radius becomes 2.61. The next child, $x_1 = -1$, adds 18.432, which fails the test. The search computed 6 partial metrics, and the list is $\{(+1, -1) : 0.61, \ (-1, +1) : 2.61\}$.

The four vectors have the metrics 0.61, 2.61, 8.21 and 19.01, so the list holds the two best. For bit 1 (stream 1), the vector with bit 0 has metric 0.61 and the vector with bit 1 has metric 2.61, so the max-log LLR is $2.61 - 0.61 = 2$. For bit 2 the roles swap and the LLR is $-2$. Both LLRs point to the transmitted $(+1, -1)$. With all four vectors, the exact LLR of bit 1 is $\ln(e^{-0.61} + e^{-8.21}) - \ln(e^{-2.61} + e^{-19.01}) \approx 2.0005$, so the list of two loses almost nothing here (a measurement on this example).

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the metrics in the list are the true metrics $\|y - H x\|^2$ (a theorem, from the triangular form), that the break of line L8 never removes a vector that belongs in the final list (a theorem, from the monotone partial metrics and the shrinking radius), and so that the final list holds $L$ vectors with the smallest metrics of all $M^n$ (a theorem). Two corollaries follow: $L = 1$ gives an ML vector, and $L = M^n$ gives the exact LLRs. The proof also shows that the max-log LLR from the list equals the max-log LLR over all vectors for every bit whose two values both occur in the list (a theorem), because the smallest metric of each value is then in the list.

## Complexity

The triangular form costs $O(n^2 m + n^3)$. Each visit of SEARCH computes $u$ in $O(n)$ and sorts $M$ level terms in $O(M \log M)$, and each accepted leaf updates the list in $O(L)$. In the worst case no subtree is pruned, so there are fewer than $2 M^{n-1}$ visits and $M^n$ leaves, and the total is $O(n^2 m + n^3 + M^n (n + \log M + L))$ in the [real RAM](/real-ram/) (a closed form). The LLR step costs $O(L n b)$. The memory holds $R$, the list and the recursion stack.

The worst case is exponential, and so is the expected cost over random channels for fixed SNR (Jaldén and Ottersten, cited on the [MIMO detection](/mimo-detection/) page). The cost in practice depends on the noise: at high SNR the first leaf is near the right answer and the radius shrinks fast. A larger list keeps the radius large longer, so the search visits more nodes. The test with seed 1704 runs 100 vectors of 4-QAM over a $4 \times 4$ Rayleigh channel at $E_s / N_0 = 15$ dB, where the full tree has 340 nodes. The search computed 8.2 partial metrics per vector on average for $L = 1$ and 102.4 for $L = 16$ (a measurement).

## Properties

- **Exact list.** The list holds $L$ vectors with the smallest metrics of all $M^n$ (theorem). This differs from the [K-best detector](/k-best-detector/), whose final $K$ survivors need not be the $K$ best.
- **Two limits.** $L = 1$ is exact ML detection, and $L = M^n$ gives the exact LLRs (theorem).
- **Max-log from a list.** For each bit whose two values both occur in the list, the max-log LLR from the list equals the max-log LLR from all $M^n$ vectors (theorem). Only the bits with one value in the list need clipping.
- **Variable cost.** The number of visited nodes depends on $H$, $y$ and $L$, not only on $n$ and $M$.
- **Noise level.** The search does not need $N_0$; the LLR step does.

## Variants and improvements

- **Fixed initial radius.** Start with a finite radius from the noise level, for example a radius that holds the transmitted vector with high probability, and collect every vector inside the sphere up to the list size. This can prune more at the start, but the sphere can be empty, and then the search must restart with a larger radius.
- **Single tree search.** Instead of one list for all bits, keep for each bit the smallest metric found with the bit value opposite to the ML vector, and prune with a radius per bit. This gives the max-log LLRs over all $M^n$ vectors without a list. Studer, Burg and Bölcskei described this form in 2008, with LLR clipping built into the pruning.
- **K-best list.** Use the final survivors of the [K-best detector](/k-best-detector/) as the list. The cost is fixed, but the list is not guaranteed to hold the best vectors.
- **Prior information.** In iterative detection and decoding, as in [turbo equalization](/turbo-equalization/), the decoder returns prior LLRs for the bits. They add a term per bit to each metric, and the search can include it in the partial metrics.
- **Real-valued decomposition.** Write the complex model as a real model of size $2n$ with $\sqrt M$-PAM symbols, so each level has $\sqrt M$ children.

## When to use it

Use the list sphere decoder when a coded MIMO system needs soft bit values close to the exact ones, $n$ and $M$ are moderate, and the receiver can accept a cost that varies with the channel. With a fixed hardware budget, use the [K-best detector](/k-best-detector/) with a list output instead. For a hard decision only, use $L = 1$, which is [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/). For large $n$, where the tree search is too slow, use [MMSE detection](/mmse-mimo-detector/) with per-stream [soft demapping](/soft-demapping/), or [expectation propagation](/expectation-propagation-detection/).

## Pitfalls

- **A list that is too short.** If the list has only one value of a bit, the LLR is clipped to $\pm \Lambda_{\max}$, which can be confidently wrong. A large clipping level makes such errors costly for the decoder.
- **No clipping.** Without a clipping level, a bit with one value in the list gets an infinite LLR, which breaks the arithmetic of most decoders.
- **The break with an unsorted child order.** The break of line L8 is correct only when the children come in increasing order of their level term. With another order, use continue instead of break.
- **A wrong sign convention.** On this site a positive LLR favors bit 0. A decoder that expects the other sign gets every bit inverted.
- **Bit labels.** The LLRs depend on the labeling of the constellation. The detector and the decoder must use the same labels, here those of the shared constellation helper, most significant bit first.

## Implementations

## History

Hochwald and ten Brink introduced the list sphere decoder in 2003, in a paper that combined it with an iterative receiver and turbo codes to work close to the capacity of a multiple-antenna channel. The search itself comes from the sphere decoders of lattice theory: the enumeration of Fincke and Pohst and the nearest-child order of Schnorr and Euchner. Later work, such as the single tree search of Studer, Burg and Bölcskei in 2008, reduced the cost of soft output and brought it to chips.

## References
