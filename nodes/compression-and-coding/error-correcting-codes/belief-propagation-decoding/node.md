---
tag: RMPGHV
kind: algorithm
slug: belief-propagation-decoding
name: Belief propagation decoding
aliases:
area: compression-and-coding/error-correcting-codes
level: advanced
summary: Decode a code on its Tanner graph by passing LLR messages between bits and checks, with the tanh rule at each check. It is exact on trees and near optimal for long LDPC codes.
model: word-ram
complexity:
  vars: {E: the number of edges of the Tanner graph, d: the largest check degree, I: the number of iterations}
  time: {worst: Θ(I E d)}
  space: {extra: Θ(E)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1962
  people: [Robert G. Gallager, Judea Pearl, David J. C. MacKay, Radford M. Neal]
  note: Gallager gave the probabilistic decoder for LDPC codes in 1962. Pearl gave belief propagation for graphical models in the 1980s, and MacKay and Neal showed in 1996 that it decodes LDPC codes close to capacity.
prereqs: [ldpc-code, tanner-graph, belief-propagation]
see_also: [min-sum-decoding, bit-flipping-decoding, symbol-by-symbol-map-decoding, loopy-belief-propagation, turbo-decoding, bcjr-algorithm, peeling-decoding, binary-erasure-channel]
sources:
  - paper: doi:10.1109/TIT.1962.1057683
    title: R. G. Gallager, Low-density parity-check codes, IRE Transactions on Information Theory 8(1), 1962, pages 21 to 28
    locator: The probabilistic decoding procedure, which passes to each digit the probabilities from the other digits of each of its checks
  - paper: "D. J. C. MacKay, Good error-correcting codes based on very sparse matrices, IEEE Transactions on Information Theory 45(2), 1999, pages 399 to 431"
    title: Good error-correcting codes based on very sparse matrices
    locator: The sum-product decoder of LDPC codes and its simulated performance close to capacity
  - paper: "F. R. Kschischang, B. J. Frey and H.-A. Loeliger, Factor graphs and the sum-product algorithm, IEEE Transactions on Information Theory 47(2), 2001, pages 498 to 519"
    title: Factor graphs and the sum-product algorithm
    locator: The sum-product algorithm on factor graphs, its exactness on trees, and the decoding of LDPC codes as a special case
  - book: isbn:9780521852296
    title: Tom Richardson and Rüdiger Urbanke, Modern Coding Theory, Cambridge University Press, 2008
    locator: Chapter 2 (factor graphs and the message passing rules) and Chapter 4 (belief propagation on binary memoryless symmetric channels, in the LLR domain)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 47 (low-density parity-check codes and their decoding by belief propagation)
---

Belief propagation decoding is the iterative decoder of an [LDPC code](/ldpc-code/), and of any binary linear code given by a parity-check matrix. It works on the [Tanner graph](/tanner-graph/) of the matrix, with the channel LLRs as input. Each variable node sends to each of its checks its belief about its bit, without the part that came from that check. Each check node sends to each of its variables what the other variables of the check imply about that bit, by the tanh rule. After each round the decoder adds up the messages at each bit and stops when the hard decisions form a codeword. When the graph is a tree the result is the exact [symbol-by-symbol MAP](/symbol-by-symbol-map-decoding/) posterior. With cycles it is an approximation, and for long sparse codes a very good one. It is the code form of [belief propagation](/belief-propagation/) and [loopy belief propagation](/loopy-belief-propagation/) of the machine learning area, with parity checks as the factors.

## In plain words

Each bit of the received word has a first opinion from the channel: "I am probably 0, and I am this sure." Each parity check knows that its bits must add up to an even number. In each round, every check tells every one of its bits: "given what the others in my group say, you should be this." A bit adds these hints to its own opinion.

When a bit answers a check, it leaves out the hint that came from that check, so that the check does not hear its own words back. After a few rounds, wrong bits are pulled toward the right value by the checks they break. The decoder stops when all checks are satisfied.

## The problem

A codeword $c$ of the code $C = \{c : H c^T = 0\}$, with $H$ an $m \times n$ binary matrix, is sent over a memoryless channel, and the receiver has the channel LLRs $L_j = \ln P(y_j \mid c_j = 0) / P(y_j \mid c_j = 1)$. On BPSK over AWGN with noise variance $\sigma^2$, $L_j = 2 y_j / \sigma^2$; on the BSC with crossover $p$, $L_j = \pm \ln \frac{1 - p}{p}$. The goal is the bitwise posteriors $L(c_j)$ and decisions with a low error rate. Exact computation costs time exponential in $\min(k, n - k)$ for a general code, so the decoder uses the sparse graph instead.

## The algorithm

$N(i)$ is the set of variables of check $i$, and $M(j)$ the set of checks of variable $j$. The schedule is *flooding*: all checks, then all variables, in each iteration.

```pseudo id=main
BP-DECODE(H, L, I)
L1  for each edge (i, j): q_{j→i} ← L_j                     ▷ variable to check
L2  for it ← 1 to I do
L3      for each edge (i, j): r_{i→j} ← 2 artanh( Π_{k ∈ N(i), k ≠ j} tanh(q_{k→i} / 2) )
L4      for each j: Λ_j ← L_j + Σ_{i ∈ M(j)} r_{i→j}             ▷ posterior LLR
L5      for each j: ĉ_j ← 0 if Λ_j ≥ 0, else 1
L6      if H ĉ^T = 0 then return (ĉ, Λ, success)
L7      for each edge (i, j): q_{j→i} ← Λ_j − r_{i→j}             ▷ leave out what came from i
L8  return (ĉ, Λ, failure)
```

Line L3 is the tanh rule: if the other bits of check $i$ were independent with LLRs $q_{k \to i}$, the LLR of their XOR, which the check forces $c_j$ to equal, is exactly this value. Line L7 subtracts the message from $i$, so the message to $i$ is extrinsic.

## Example

**The Hamming code with one weak wrong bit.** Take the [Hamming code](/hamming-code/) with checks $\{0, 2, 3, 4\}$, $\{0, 1, 2, 5\}$ and $\{1, 2, 3, 6\}$, the codeword 0000000, and the channel LLRs

$$L = (2.0,\ 1.5,\ -0.8,\ 2.2,\ 1.8,\ 2.5,\ 1.2).$$

Bit 2 has the wrong sign. In iteration 1 the three checks send to bit 2:

| check | other bits | message $r_{i \to 2}$ |
|---|---|---|
| 0 | 0, 3, 4 | $2 \operatorname{artanh}(\tanh 1.0 \cdot \tanh 1.1 \cdot \tanh 0.9) = 0.936$ |
| 1 | 0, 1, 5 | $0.872$ |
| 2 | 1, 3, 6 | $0.560$ |

So $\Lambda_2 = -0.8 + 0.936 + 0.872 + 0.560 = 1.569$, and bit 2 becomes 0. All posteriors after iteration 1 are $(1.142, 0.669, 1.569, 1.519, 1.328, 2.128, 0.809)$, all positive, so line L6 returns 0000000 after one iteration. The other bits lost some confidence, because each is in a check with the doubtful bit 2. The exact bitwise MAP LLRs are larger, $(2.348, 2.289, 1.489, 3.137, 2.378, 3.335, 2.158)$: one iteration does not give exact posteriors, but here it gives the right decisions.

**Exact on a tree.** The checks $\{0, 1, 2\}$, $\{2, 3, 4\}$, $\{4, 5\}$ and $\{1, 6, 7\}$ give a Tanner graph with 12 nodes and 11 edges that is connected, so it is a tree. The longest path, $v_5, c_2, v_4, c_1, v_2, c_0, v_1, c_3, v_6$, has 4 checks. With the LLRs $(-1.3, 2.2, 1.8, -0.7, 0.5, 0.2, 1.3, 1.9)$ and no early stop, the posteriors of bits 5 and 6 are still changing after iterations 1, 2 and 3, and after iteration 4 all eight equal the brute-force posteriors $(0.086, 2.3135, 0.4132, -0.4909, 0.4909, 0.4909, 2.2686, 2.6252)$. The test checks this to $10^{-9}$ for 200 random LLR vectors.

**Not exact with cycles.** On the Hamming code with $L = (0.9, -0.4, 1.1, 0.3, -0.7, 1.4, 0.2)$, belief propagation without early stop settles at $(0.741, -0.154, 0.968, 0.176, -0.650, 1.324, 0.193)$, while the exact posteriors are $(0.761, -0.215, 0.913, 0.268, -0.627, 1.315, 0.096)$. The signs agree, but the values do not, because the graph has 4-cycles.

**Against the simpler decoders.** On a $(3, 6)$-regular Gallager code with $n = 96$, BPSK on AWGN at $E_b/N_0 = 2$ dB and 60 frames, the bit errors were 83 for belief propagation, 125 for [min-sum](/min-sum-decoding/) and 725 for hard-decision [bit flipping](/bit-flipping-decoding/), against 552 in the raw hard decisions. Bit flipping at this noise level makes things worse; the soft decoders do not.

## Correctness

Three facts make the algorithm right where it is exact.

- **The tanh rule.** For independent bits, $P(\oplus = 0) - P(\oplus = 1) = \prod_k (P_k(0) - P_k(1))$, and $P(0) - P(1) = \tanh(L/2)$ for a bit with LLR $L$. So line L3 is the exact LLR of the XOR of the other bits of the check.
- **Trees.** If the Tanner graph is a tree, cutting the edge $(i, j)$ splits it into two parts, and the exact message $r_{i \to j}$ is the evidence that the part on the side of $i$ gives about $c_j$. The parts below a node are disjoint, so their evidence multiplies, which gives the update rules. By induction on the depth of the part, the message on each edge is exact after as many iterations as the part has levels of checks, and then line L4 gives the exact posterior.
- **The output.** Line L6 returns only words that satisfy all checks.

The [correctness proof](proofs/correctness.md) gives the induction. With cycles the incoming messages of a node are not independent, and the result is an approximation. Its behavior on long random codes is described by density evolution, which treats the graph as a tree to the depth of the iterations.

## Complexity

Line L3 as written takes $\Theta(d_i^2)$ for a check of degree $d_i$, so an iteration takes $\Theta(\sum_i d_i^2) = O(E d)$ time. Computing the product of all $d_i$ values once and the products that leave out one value by prefix and suffix products gives $\Theta(d_i)$ per check and $\Theta(E)$ per iteration. The memory is $\Theta(E)$ for the messages. For an LDPC code with bounded degrees, $E = \Theta(n)$, so the decoder is linear in $n$ per iteration. Usual iteration limits are 20 to 100, and most frames stop much earlier.

## Properties

- Exact on a tree after at most as many iterations as there are checks on the longest path; approximate on graphs with cycles.
- Soft input and soft output: the posteriors $\Lambda_j$ can feed a later stage.
- The decision on the stop is always a codeword, but on a graph with cycles it need not be the ML codeword or the bitwise MAP decisions.
- Invariant under the symmetry of the code: for a symmetric channel, the error probability does not depend on the codeword sent, so it can be simulated with the all-zero codeword. The simulations in the tests do this.
- Each node update uses only its neighbors, so the work is parallel across nodes.

## Variants and improvements

- **Min-sum.** Replace the tanh rule by the sign product and the least magnitude. It needs no knowledge of $\sigma^2$ and no transcendental functions. See [min-sum decoding](/min-sum-decoding/).
- **Layered (serial) schedule.** Update one check or group of checks at a time and use the new messages at once. It often converges in about half as many iterations, and it is the usual schedule in hardware decoders.
- **Probability and log domain forms.** Gallager's form works with probabilities and differences $P(0) - P(1)$. The LLR form avoids underflow. The check update can also use $\phi(x) = -\ln \tanh(x/2)$, which is its own inverse, so $|r| = \phi(\sum \phi(|q|))$ with a sign product.
- **The erasure channel.** With LLRs $0$ and $\pm \infty$ only, belief propagation becomes [peeling decoding](/peeling-decoding/), and it fails exactly on stopping sets.
- **Nonbinary codes.** Over $\mathrm{GF}(q)$ the messages are distributions on $q$ values, and the check update is a convolution, done fast with the Fourier transform over the group.

## When to use it

- Use it for LDPC codes on soft-output channels when the best error rate matters and the decoder can compute $\tanh$ and $\operatorname{artanh}$ or a table of $\phi$.
- Use min-sum in hardware, or when $\sigma^2$ is unknown, and bit flipping when only hard decisions are available and the error rate is low.
- For short dense codes, such as a Hamming or BCH code, the graph has many short cycles. A trellis decoder or an algebraic decoder is better there.

## Pitfalls

- **Overflow of artanh.** When the product in line L3 is close to $\pm 1$, artanh is infinite. Clip the product, as the implementation does at $1 - 10^{-15}$, or clip the LLRs.
- **Passing the full posterior back.** Line L7 must subtract $r_{i \to j}$; without it the check hears its own message, and the decoder becomes too confident and stops improving.
- **Wrong LLR scale.** The tanh rule needs LLRs with the right scale. With the wrong $\sigma^2$ the decoder still runs but loses performance.
- **Short cycles and trapping sets.** On a graph with 4-cycles the messages echo after two iterations. On good graphs the remaining failures at high signal to noise ratio come from small trapping sets, which give an error floor.
- **Treating a failed stop as success.** If the iteration limit is reached, the output is not a codeword. The flag of line L8 says so, and a system can ask for a retransmission.

## Implementations

## History

Gallager described the probabilistic decoder for his LDPC codes in 1962, in the form of probabilities passed between digits and checks, and showed that it worked well on long codes; the computers of the time made it hard to use. Tanner put codes and their decoders on bipartite graphs in 1981. Pearl gave belief propagation on Bayesian networks in the 1980s, as an exact method on trees. After turbo codes, MacKay and Neal in 1996 found LDPC codes again and showed that belief propagation decodes them close to capacity. McEliece, MacKay and Cheng, and Kschischang and Frey, showed in 1998 that turbo decoding is the same algorithm, and Kschischang, Frey and Loeliger described the sum-product algorithm on factor graphs in 2001. Richardson and Urbanke's density evolution of 2001 gave thresholds that guide the design of the codes.

## References
