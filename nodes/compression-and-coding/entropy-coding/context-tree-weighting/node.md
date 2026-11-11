---
tag: 4VCC2M
kind: algorithm
slug: context-tree-weighting
name: Context tree weighting
aliases:
- CTW
area: compression-and-coding/entropy-coding
level: research
summary: Mixes the predictions of all context trees up to depth D with a Bayesian weighting that costs O(D) per bit, and stays within a proven redundancy of the best tree source.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of bits, D: the depth of the tree}
  time: {worst: O(n D), average: O(n D), best: Θ(n D)}
  space: {extra: "O(min(n D, 2^D))"}
properties: {deterministic: true, online: true, recursive: false, comparison: false}
history:
  year: 1995
  people: [Frans M. J. Willems, Yuri M. Shtarkov, Tjalling J. Tjalkens]
  note: Willems, Shtarkov and Tjalkens gave the method and its redundancy bound for binary tree sources in 1995.
prereqs: [context-modeling, adaptive-modeling]
see_also: [prediction-by-partial-matching, context-mixing, minimum-description-length, bayesian-inference, regret, multiplicative-weights-update]
sources:
  - paper: doi:10.1109/18.382012
    title: Frans M. J. Willems, Yuri M. Shtarkov and Tjalling J. Tjalkens, The context-tree weighting method, basic properties, IEEE Transactions on Information Theory 41(3), 653-664, 1995
    locator: the weighting recursion, the bound on the KT estimator, and the redundancy theorem for tree sources
  - paper: doi:10.1109/TIT.1981.1056331
    title: Raphail E. Krichevsky and Victor K. Trofimov, The performance of universal encoding, IEEE Transactions on Information Theory 27(2), 199-207, 1981
    locator: the KT estimator with the add-one-half rule
  - paper: doi:10.1109/18.661523
    title: Frans M. J. Willems, The context-tree weighting method, extensions, IEEE Transactions on Information Theory 44(2), 792-798, 1998
    locator: context trees of unbounded depth and the case with no known past
  - paper: doi:10.1109/TIT.1983.1056741
    title: Jorma Rissanen, A universal data compression system, IEEE Transactions on Information Theory 29(5), 656-664, 1983
    locator: the algorithm Context, which selects one context tree, where CTW mixes all of them
  - paper: doi:10.1613/jair.1491
    title: Ron Begleiter, Ran El-Yaniv and Golan Yona, On prediction using variable order Markov models, Journal of Artificial Intelligence Research 22, 385-421, 2004
    locator: the comparison of CTW with PPM and other variable-order predictors on text, music and protein data
---

Context tree weighting (CTW) is a sequential predictor for binary data, used with an [arithmetic coder](/arithmetic-coding/). It does not choose one [context model](/context-modeling/). It takes a Bayesian mixture over all *tree sources* of depth at most $D$, that is, over every way to cut the past into contexts of different lengths, each with its own [adaptive](/adaptive-modeling/) KT estimate. There are at least $2^{2^{D-1}}$ such trees, but one recursion over a single tree of counts computes the mixture exactly in $O(D)$ steps per bit. Willems, Shtarkov and Tjalkens proved that the code length of CTW exceeds that of the best tree source with known parameters by at most the cost to describe the tree plus about $\tfrac12 \lg n$ bits per leaf, for every input, with no probabilities.

## In plain words

Each bit is predicted from the bits before it. A context model must decide how far back to look, and the best answer differs from place to place: after some patterns one past bit is enough, after others three are needed. CTW keeps all answers at once.

It keeps a tree of tallies, one node for each recent pattern up to a fixed length. At each node it asks two questions: how well did a plain tally at this node predict the bits so far, and how well did the two longer patterns below it do? It gives each answer half the vote. Done at every node from the bottom up, this weights every possible choice of contexts at once, and it favors the choices that have predicted well. The coder then turns the result into bits.

## The problem

The input is a binary sequence $x_1 \ldots x_n$, read once, and the $D$ bits before $x_1$ are known to both sides (here they are zeros). The output is a bit string from which the decoder gets the sequence back. The goal is a code length close to that of the best *tree source*: a set $\mathcal S$ of contexts that forms the leaves of a full binary tree of depth at most $D$, with a probability $\theta_s$ of a 1 in each leaf $s$. Neither $\mathcal S$ nor the $\theta_s$ is known.

## The algorithm

A node $s$ is a string of at most $D$ past bits, the most recent first; its children are $s0$ and $s1$, which look one bit further back. Each node keeps the counts $a_s$ and $b_s$ of the zeros and ones that came after its context, the KT estimate $P_e(s)$ of those bits, and the weighted probability

$$P_w(s) = \begin{cases} P_e(s) & \text{if } s \text{ has depth } D, \\ \tfrac12 P_e(s) + \tfrac12 P_w(s0)\, P_w(s1) & \text{otherwise.} \end{cases}$$

The KT estimate gives the next bit the probability $(a_s + \tfrac12)/(a_s + b_s + 1)$ for a 0 and $(b_s + \tfrac12)/(a_s + b_s + 1)$ for a 1. The root $\lambda$ holds the probability $P_w(\lambda)$ of the whole sequence so far.

```pseudo id=main
CTW-ENCODE(x_1 … x_n, D)
L1  every node s starts with a_s = b_s = 0 and P_e(s) = P_w(s) = 1; the D bits before x_1 are zeros
L2  for t ← 1 to n do
L3      for each x ∈ {0, 1}: q_x ← the value of P_w(λ) after lines L6 to L10 run for the bit x
L4      p ← q_1 / (q_0 + q_1)
L5      code x_t with the arithmetic coder, with Pr[1] = p
L6      for d ← D down to 0, with s the context x_{t−1} … x_{t−d} do
L7          P_e(s) ← P_e(s) · (the count of x_t in s + ½) / (a_s + b_s + 1)
L8          add 1 to a_s if x_t = 0, else to b_s
L9          if d = D then P_w(s) ← P_e(s)
L10         else P_w(s) ← ½ P_e(s) + ½ P_w(s0) · P_w(s1)
L11 finish the arithmetic coder

CTW-DECODE(code, n, D)
L12 for t ← 1 to n do
L13     compute p as in L3 and L4
L14     decode x_t with Pr[1] = p, and output it
L15     update the tree with x_t as in L6 to L10
```

Only the $D + 1$ nodes on the path of the current context change, and in line L10 the child off the path keeps its old value. The probabilities get small fast, so the implementation stores $\lg P_e$ and $\lg P_w$. Willems, Shtarkov and Tjalkens store the ratio $P_e(s) / (P_w(s0) P_w(s1))$ in place of the two values, which also avoids the underflow.

## Example

Take $D = 1$, the zero past bit, and $x = 0110100$. The root sees all seven bits, 4 zeros and 3 ones. The node 0 sees the bits that follow a 0, which are $0, 1, 1, 0$, and the node 1 sees the bits that follow a 1, which are $1, 0, 0$.

| node | bits | $a$, $b$ | $P_e$ | $\lg(1/P_e)$ |
|---|---|---|---|---|
| root | 0110100 | 4, 3 | $\tfrac{(1/2)(3/2)(5/2)(7/2) \cdot (1/2)(3/2)(5/2)}{7!} = \tfrac{5}{2048}$ | 8.68 |
| 0 | 0110 | 2, 2 | $\tfrac{3}{128}$ | 5.42 |
| 1 | 100 | 2, 1 | $\tfrac{1}{16}$ | 4.00 |

The leaves have depth $D$, so $P_w = P_e$ there, and at the root

$$P_w(\lambda) = \tfrac12 \cdot \tfrac{5}{2048} + \tfrac12 \cdot \tfrac{3}{128} \cdot \tfrac{1}{16} = \tfrac{5}{4096} + \tfrac{3}{4096} = \tfrac{1}{512}.$$

So CTW codes the seven bits in 9 bits. The memoryless model alone would need 8.68 bits and the model with one bit of context 9.42 bits; the mixture is within 1 bit of the better of the two, which is the cost of the half weights. Step by step, the coder gives the bits the probabilities $\tfrac12, \tfrac14, \tfrac12, \tfrac{5}{16}, \tfrac12, \tfrac{9}{20}, \tfrac49$, and their product is $\tfrac{1}{512}$.

## Correctness

The update touches only the path of the current context, and it applies the product formula of the KT estimate and the weighting recursion from the leaf up, so after each bit every node holds the values of the definition. The KT estimate satisfies $P_e(a + 1, b) + P_e(a, b + 1) = P_e(a, b)$, and so, by induction up the path, the two possible next values of $P_w(\lambda)$ sum to the present one; the prediction $p$ is a true conditional probability, and the product of the predictions is $P_w(\lambda)$. The decoder builds the same tree from the same bits, so the arithmetic decoder gets the same probabilities and returns each bit. For the length, $P_w(s) \ge \tfrac12 P_e(s)$ and $P_w(s) \ge \tfrac12 P_w(s0) P_w(s1)$ give $P_w(\lambda) \ge 2^{-\Gamma_D(\mathcal S)} \prod_{s \in \mathcal S} P_e(s)$ for every tree $\mathcal S$, and the KT bound finishes the argument. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/), with floating-point or fixed-point numbers for the probabilities.

- **Time.** Each bit visits the $D + 1$ nodes of its path a constant number of times, so CTW takes $O(n D)$ time. For bytes coded as 8 binary decisions, this is $O(8 n D)$ for $n$ bytes.
- **Space.** A node exists only after a context reaches it, so there are at most $\min(n(D + 1), 2^{D+1} - 1)$ nodes. For text at a useful depth, this is large, and practical coders limit the number of nodes.
- **Redundancy.** For every tree source with leaves $\mathcal S$ and parameters $\theta$, and every input,

$$\lg \frac{1}{P_w(\lambda)} - \lg \frac{1}{P_a(x)} \le \Gamma_D(\mathcal S) + |\mathcal S|\, \gamma\!\left(\frac{n}{|\mathcal S|}\right),$$

where $\Gamma_D(\mathcal S) = 2|\mathcal S| - 1 - |\{s \in \mathcal S : |s| = D\}|$ is the length of a natural code for the tree, $\gamma(z) = \tfrac12 \lg z + 1$ for $z \ge 1$ and $\gamma(z) = z$ below 1. The arithmetic coder adds at most 2 bits. The last term, about $\tfrac12 \lg n$ bits for each leaf, is the price of learning $|\mathcal S|$ parameters, the same rate as in [minimum description length](/minimum-description-length/).

**Measured.** On 5000 bits from the tree source whose leaves are "last bit 1" ($\theta = 0.1$), "last bits 0 then 0" ($\theta = 0.8$) and "last bits 0 then 1" ($\theta = 0.4$), the true source gives the data 3609.4 bits. CTW gives 4829.2 bits at $D = 0$, 3969.2 at $D = 1$, 3628.4 at $D = 2$ and 3630.3 to 3630.5 for every depth from 3 to 16. The redundancy at $D \ge 3$ is 21.0 bits, below the bound of 24.05. A depth larger than needed costs almost nothing; a depth too small costs a lot.

## Properties

- **Exact Bayesian mixture.** $P_w(\lambda) = \sum_{\mathcal S} 2^{-\Gamma_D(\mathcal S)} \prod_{s \in \mathcal S} P_e(s)$, a mixture over all trees with prior $2^{-\Gamma_D(\mathcal S)}$, and each $P_e$ is itself a mixture over $\theta$ with the Beta(½, ½) prior.
- **Bound for each sequence.** The redundancy bound holds for every input, not only on average.
- **Binary.** CTW in its basic form predicts bits. Larger alphabets are coded through a binary decomposition, for example the 8 bits of a byte with the earlier bits of the byte as part of the context.
- **Symmetric.** The decoder does the same work as the encoder.

## Variants and improvements

- **Unbounded depth.** Willems (1998) removes the bound $D$, keeping the tree finite by storing only the contexts that occurred, and handles the case where the past before $x_1$ is not known.
- **Other weights.** The weight $\tfrac12$ at each node can change with the depth or be learned; other estimators can replace KT, such as ones that give more weight to deterministic contexts, which helps on text.
- **Decomposed CTW for text.** Coders for bytes split each symbol into binary decisions and run a CTW for each decision, with the earlier decisions of the symbol as part of the context.
- **Use beyond compression.** CTW serves as a sequence predictor in other fields, for example in the MC-AIXI agent of Veness and others (2011) and in the comparison of variable-order predictors by Begleiter, El-Yaniv and Yona (2004).

## When to use it

Use CTW when a provable guarantee matters, when the data are binary or have a natural binary form, and when the source is plausibly a variable-order Markov source, such as in research on universal coding and in sequence prediction. For general byte data, [PPM](/prediction-by-partial-matching/) and [context mixing](/context-mixing/) are more common in practice: PPM is faster, and context mixing can add models of other kinds.

## Pitfalls

- **Underflow.** $P_e$ and $P_w$ fall below the range of double-precision numbers once the code length passes about 1074 bits. Store logarithms or the ratio $P_e(s) / (P_w(s0) P_w(s1))$.
- **The child off the path.** Line L10 must use the stored value of the other child. A child that no context has reached has $P_w = 1$, not 0.
- **The first $D$ bits.** Both sides must agree on the past before $x_1$; the simplest choice is $D$ zeros.
- **Determinism.** With floating-point numbers, the encoder and the decoder must run the same operations in the same order, or their predictions can differ in the last bit and the decoder fails.
- **Extreme probabilities.** The rounding of $p$ for the coder must keep both outcomes possible; here $p$ is rounded to 16 bits and kept in $[2^{-16}, 1 - 2^{-16}]$.

## Implementations

## History

Rissanen's algorithm Context (1983) chose one tree of contexts as it went. Krichevsky and Trofimov (1981) gave the add-one-half estimator for memoryless sources, with a redundancy of about $\tfrac12 \lg n$ bits. Willems, Shtarkov and Tjalkens combined the two ideas in the context-tree weighting method, published in 1995. It mixes all trees at a cost linear in the depth, and its redundancy bound holds for each sequence. Willems extended the method to unbounded depth in 1998. Later work applied it to text, to prediction of sequences in machine learning, and to the approximation of general agents.

## References
