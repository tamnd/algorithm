---
tag: 3ZQXDE
kind: algorithm
slug: k-best-detector
name: K-best detector
aliases:
- K-best sphere decoder
- M-algorithm detection
area: communications/mimo-communications
level: advanced
summary: A breadth-first search of the detection tree that keeps the K best partial symbol vectors at each level. Its cost is fixed and it is not exact ML unless K is at least M^(n-1).
solves: [mimo-detection]
model: real-ram
complexity:
  vars: {n: the number of transmitted streams, m: the number of receive antennas, M: the constellation size, K: the number of survivors per level}
  time: {worst: O(n^2 m + n^3 + n^2 K + n K M log(K M))}
  space: {extra: O(n m + n K M)}
properties: {deterministic: true, exact_ml: false, exact_ml_if_K_at_least: "M^(n-1)", fixed_complexity: true, k_equal_1_is: "ZF successive cancellation in a fixed order", needs_noise_level: false}
history:
  year: 2002
  people: [Kwan-wai Wong, Chi-ying Tsui, Roger S.-K. Cheng, Wai-ho Mow]
  note: "Wong, Tsui, Cheng and Mow proposed the K-best lattice decoder for MIMO with a VLSI architecture. The idea is the M-algorithm of sequential decoding, surveyed by Anderson and Mohan in 1984."
prereqs: [mimo-detection, cholesky-decomposition, breadth-first-search]
see_also: [schnorr-euchner-enumeration, fincke-pohst-enumeration, list-sphere-decoder, v-blast, beam-search, babai-nearest-plane, closest-vector-problem, partial-sorting]
sources:
  - paper: "Kwan-wai Wong, Chi-ying Tsui, Roger S.-K. Cheng and Wai-ho Mow, A VLSI architecture of a K-best lattice decoding algorithm for MIMO channels, Proc. IEEE International Symposium on Circuits and Systems (ISCAS) 2002, vol. 3, pages III-273 to III-276"
    locator: the breadth-first search with K survivors per level and its hardware architecture
  - paper: doi:10.1109/JSAC.2005.862402
    title: Zhan Guo and Peter Nilsson, Algorithm and implementation of the K-best sphere decoding for MIMO detection, IEEE Journal on Selected Areas in Communications 24(3), 491-503, 2006
    locator: the K-best Schnorr-Euchner variant, which expands the children of each survivor in order of distance, and its VLSI implementation
  - paper: doi:10.1109/TCOM.1984.1096023
    title: John B. Anderson and Seshadri Mohan, Sequential coding algorithms - a survey and cost analysis, IEEE Transactions on Communications 32(2), 169-176, 1984
    locator: the M-algorithm, a breadth-first tree search that keeps the M best paths at each depth
  - paper: doi:10.1109/MSP.2009.932126
    title: Erik G. Larsson, MIMO detection methods - how they work, IEEE Signal Processing Magazine 26(3), 91-95, 2009
    locator: the tree view of MIMO detection after a QR decomposition and the K-best search
---

The K-best detector solves the [MIMO detection](/mimo-detection/) problem approximately by a breadth-first search over the tree of partial symbol vectors. After a triangular factorization of the channel, the ML metric $\|y - H x\|^2$ splits into $n$ nonnegative terms, one per tree level, and each level adds one symbol. The detector goes down the tree level by level, extends each surviving partial vector by all $M$ symbols, and keeps only the $K$ extensions with the smallest partial metrics. So it visits exactly $K M$ nodes per level, whatever the noise. This fixed cost is the difference from the depth-first sphere searches, [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/) and [Fincke-Pohst enumeration](/fincke-pohst-enumeration/), which are exact ML but have a cost that depends on the noise and the channel. The price is that K-best is not exact: the ML vector is lost if one of its partial vectors falls out of the $K$ best at some level. With $K = 1$ it is the ZF successive cancellation of [V-BLAST](/v-blast/) in a fixed order, and with $K \ge M^{n-1}$ it is exact ML (both theorems). In tree search terms it is a [beam search](/beam-search/) with beam width $K$.

## In plain words

The receiver must guess several symbols at once. It can guess them one at a time, starting with the symbol that the others do not affect after a change of coordinates. For each guess it keeps a score, the part of the total error that the symbols guessed so far already cause. The score only grows as more symbols are added. A greedy receiver keeps only its single best guess at each step, and one bad early guess ruins the rest. The K-best receiver keeps its K best partial guesses at each step instead of one. A larger K costs more work but makes a fatal early mistake less likely. The work is the same for every received signal, which is useful in hardware.

## The problem

The model is $y = H x + w$ with $H \in \mathbb{C}^{m \times n}$ known, $m \ge n$ and full column rank, $x \in \mathcal{S}^n$ for a constellation $\mathcal{S}$ of size $M$, and $w \sim \mathcal{CN}(0, N_0 I)$. The ML decision minimizes $\|y - H x\|^2$ over the $M^n$ vectors of $\mathcal{S}^n$. The K-best detector returns a vector of $\mathcal{S}^n$ with a small metric, and the list of its $K$ final survivors with their metrics, which a soft-output receiver can use.

## The algorithm

Let $H^H H = R^H R$ with $R$ upper triangular and a real positive diagonal, from a [Cholesky decomposition](/cholesky-decomposition/) of $H^H H$ or a [QR decomposition](/qr-decomposition/) of $H$. Let $\bar y$ solve $R^H \bar y = H^H y$. Then $\|y - H x\|^2 = \|\bar y - R x\|^2 + c$ with $c = \|y\|^2 - \|\bar y\|^2$, which does not depend on $x$. Row $i$ of $R$ involves only $x_i, \ldots, x_n$, so

$$\|\bar y - R x\|^2 = \sum_{i = 1}^{n} \Big|\bar y_i - \sum_{j > i} R_{ij} x_j - R_{ii} x_i\Big|^2,$$

and the partial metric of $(x_i, \ldots, x_n)$ is the sum of the terms from $i$ to $n$.

```pseudo id=main
K-BEST(y, H, S, K)
L1  (R, ȳ, c) ← TRIANGULARIZE(y, H)
L2  survivors ← {(0, empty vector)}
L3  for i ← n down to 1                      ▷ one tree level per symbol
L4      for each (d, (x_{i+1}, ..., x_n)) in survivors
L5          for each s in S: add (d + |ȳ_i - Σ_{j>i} R_ij x_j - R_ii s|², (s, x_{i+1}, ..., x_n)) to the candidates
L6      survivors ← the K candidates with the smallest metrics
L7  return the survivors, with c added to each metric, best first
```

Line L5 computes the interference term $u = \bar y_i - \sum_{j > i} R_{ij} x_j$ once per survivor and then one squared distance per symbol. Line L6 needs only the $K$ smallest of $K M$ values, so a [partial sort](/partial-sorting/) or a selection by [quickselect](/quickselect/) is enough; the implementation sorts, which is simpler. Hardware versions avoid the full sort: the Schnorr-Euchner variant of Guo and Nilsson (2006) generates the children of each survivor in order of distance, so only the next best child of each survivor competes for a slot.

## Example

Take $m = n = 2$, BPSK, $H = \begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$, and $y = (0.5, 0.6)$, the received vector of the example on the [ZF page](/zero-forcing-mimo-detector/) for $x = (+1, -1)$. Then $H^T H = \begin{pmatrix} 5 & 3 \\ 3 & 2 \end{pmatrix}$, and

$$R = \frac{1}{\sqrt 5} \begin{pmatrix} 5 & 3 \\ 0 & 1 \end{pmatrix}, \qquad \bar y = \frac{1}{\sqrt 5} (1.6, 0.7), \qquad c = 0.$$

Level 2 (the symbol $x_2$): the term is $(0.7 - x_2)^2 / 5$, which is 0.018 for $x_2 = +1$ and 0.578 for $x_2 = -1$.

With $K = 1$, only $x_2 = +1$ survives. Level 1 then has $u = (1.6 - 3) / \sqrt 5 = -1.4 / \sqrt 5$, and the term $(-1.4 - 5 x_1)^2 / 5$ is 8.192 for $x_1 = +1$ and 2.592 for $x_1 = -1$. The detector returns $(-1, +1)$ with metric $0.018 + 2.592 = 2.61$. Both symbols are wrong. This is the ZF successive cancellation decision that starts with $x_2$.

With $K = 2 = M^{n-1}$, both level 2 nodes survive. For $x_2 = -1$, $u = (1.6 + 3) / \sqrt 5$, and $x_1 = +1$ adds $(4.6 - 5)^2 / 5 = 0.032$, for a total of $0.578 + 0.032 = 0.61$. The best final survivor is $(+1, -1)$ with metric 0.61, the ML vector. The partial metric of the ML path was the larger one at level 2 (0.578 against 0.018), so a search with $K = 1$ pruned it.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows four things. First, the triangular form gives $\|y - H x\|^2 = \|\bar y - R x\|^2 + c$, so the returned metrics are the true ML metrics (a theorem). Second, partial metrics never decrease down the tree (a theorem), which is why pruning by partial metric is reasonable but also why it can fail: a path can start badly and end well, as in the example. Third, with $K \ge M^{n-1}$ no node is pruned before the last level, so the survivors are the $K$ best vectors of $\mathcal{S}^n$ and the first one is the ML vector (a theorem). Fourth, with $K = 1$ the detector is ZF successive cancellation in the order $x_n, \ldots, x_1$ (a theorem).

## Complexity

The triangularization costs $O(n^2 m + n^3)$. Each of the $n$ levels computes $K$ interference terms of $O(n)$ each, $K M$ squared distances, and a selection of $K$ out of $K M$ values, which is $O(K M)$ with quickselect or $O(K M \log(K M))$ with a sort. So the search costs $O(n^2 K + n K M \log(K M))$ with sorting, and the total is $O(n^2 m + n^3 + n^2 K + n K M \log(K M))$ in the [real RAM](/real-ram/). The memory holds $K M$ candidates of up to $n$ symbols. The cost does not depend on the noise or on $H$, unlike the depth-first sphere searches, whose expected cost is exponential in $n$ (Jaldén and Ottersten, 2005, cited on the [MIMO detection](/mimo-detection/) page).

## Properties

- **Fixed cost.** Exactly $n$ levels with $K M$ candidates each, for every $y$ and $H$.
- **Exact metrics.** The metric of each survivor is $\|y - H x\|^2$ (theorem).
- **Exact for large K.** With $K \ge M^{n-1}$ the result is the ML vector (theorem). This is the cost of exhaustive search, $M^n$ final candidates.
- **Greedy for K = 1.** With $K = 1$ it is ZF successive cancellation in a fixed order (theorem).
- **No guarantee in between.** For $1 < K < M^{n-1}$ the result can differ from ML, and a larger $K$ is not guaranteed to give a better metric for every $y$.
- **Measured agreement with ML.** For 4-QAM, $m = n = 4$, i.i.d. Rayleigh entries and $E_s / N_0 = 15$ dB, the test with seed 1605 runs 150 vectors. $K = 1$ agreed with ML on 145 and $K = 4$ on all 150 (measurement). Here $M^{n-1} = 64$, so $K = 4$ is far below the exact bound.
- **List output.** The $K$ final survivors give a list for soft output, as in the [list sphere decoder](/list-sphere-decoder/), but the list is not guaranteed to hold the $K$ best vectors.

## Variants and improvements

- **Sorted QR.** Order the columns of $H$ before the factorization so that the first levels, where pruning is most harmful, have the largest $R_{ii}$. This is the order question of [V-BLAST](/v-blast/) in tree form.
- **Schnorr-Euchner expansion.** Generate the children of each survivor in order of distance from $u / R_{ii}$, as in [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/), and merge the sorted child lists. This is the method of Guo and Nilsson (2006).
- **Real-valued decomposition.** Write the complex model as a real model of size $2n$ with $\sqrt M$-PAM symbols. The tree then has $2n$ levels with $\sqrt M$ children each, which reduces the sorting cost.
- **Adaptive K.** Use a larger $K$ at the first levels and a smaller one later, or a radius test that drops survivors whose metric is far from the best.
- **Soft output.** Compute bit LLRs from the final list, with clipping for bits that take only one value in the list, as in the [list sphere decoder](/list-sphere-decoder/).

## When to use it

Use the K-best detector in hardware receivers that need a fixed throughput, with $n$ up to about 8 and moderate constellations, where a sphere search would need a worst-case budget. For a software receiver that needs the exact ML decision, use [Schnorr-Euchner enumeration](/schnorr-euchner-enumeration/). For large $n$ and $M$, where $K M$ candidates per level are too many, use [lattice reduction aided detection](/lattice-reduction-aided-detection/) or [MMSE detection](/mmse-mimo-detector/).

## Pitfalls

- **Expecting ML.** For $K < M^{n-1}$ the detector can miss the ML vector even at moderate noise, as the example shows with $K = 1$.
- **Ignoring the order of the columns.** Without sorting, the first levels can have small $R_{ii}$, where the partial metrics say little and pruning is most often wrong.
- **Forgetting the constant.** $\|\bar y - R x\|^2$ differs from $\|y - H x\|^2$ by $c = \|y\|^2 - \|\bar y\|^2$ when $m > n$. LLRs computed from differences of metrics do not need $c$, but a comparison with a threshold does.
- **Ties.** The selection of line L6 needs a fixed tie rule if the result must be reproducible; the implementation keeps the earlier candidate.
- **Wide channels.** With $n > m$, $H^H H$ is singular and the triangular form above does not exist. Use a regularized form such as $H^H H + (N_0 / E_s) I$, which changes the metric.

## Implementations

## History

The M-algorithm, a breadth-first search that keeps the best $M$ paths of a code tree at each depth, comes from the decoding of tree and trellis codes and from source coding. Anderson and Mohan surveyed it and its cost in 1984. Wong, Tsui, Cheng and Mow applied it to the tree of lattice decoding for MIMO in 2002, under the name K-best, together with a VLSI architecture. Guo and Nilsson (2006) combined it with the Schnorr-Euchner order to reduce the sorting cost, and many chip designs followed.

## References
