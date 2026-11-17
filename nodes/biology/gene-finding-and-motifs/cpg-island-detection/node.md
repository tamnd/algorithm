---
tag: 0S3A9K
kind: algorithm
slug: cpg-island-detection
name: CpG island detection
aliases:
- CpG island HMM
area: biology/gene-finding-and-motifs
level: intro
summary: Find stretches of DNA rich in the dinucleotide CG, with a two-state HMM decoded by the Viterbi algorithm, or with a sliding window test of GC content and observed over expected CpG.
model: real-ram
complexity:
  vars: {n: the length of the sequence, w: the window length of the window rule}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [hidden-markov-model, viterbi-algorithm]
see_also: [markov-chain, forward-backward-algorithm, baum-welch-algorithm, sliding-window, log-sum-exp-trick, gene-prediction, kmer]
sources:
  - book: isbn:9780521629713
    title: Richard Durbin, Sean R. Eddy, Anders Krogh and Graeme Mitchison, Biological Sequence Analysis, Cambridge University Press, 1998
    locator: Chapter 3, the CpG island example (Markov chains for discrimination, and the hidden Markov model for locating islands, decoded with the Viterbi algorithm)
  - paper: doi:10.1016/0022-2836(87)90689-9
    title: M. Gardiner-Garden and M. Frommer, CpG islands in vertebrate genomes, Journal of Molecular Biology 196(2), 1987
    locator: pp. 261 to 282, the criteria for a CpG island (at least 200 bp, G + C above 50 percent, observed over expected CpG above 0.6)
  - paper: doi:10.1073/pnas.052410099
    title: Daiya Takai and Peter A. Jones, Comprehensive analysis of CpG islands in human chromosomes 21 and 22, PNAS 99(6), 2002
    locator: pp. 3740 to 3745, the stricter criteria (more than 500 bp, G + C of 55 percent or more, observed over expected CpG of 0.65)
---

A CpG island is a stretch of DNA, usually a few hundred to a few thousand bases long, where the dinucleotide CG (a C followed by a G on the same strand, written CpG) is much more common than in the rest of the genome. In vertebrate DNA the C of a CG pair is often methylated, and a methylated C mutates to T at a high rate, so CG pairs are rare in most of the genome. Near the promoters of many genes the C is not methylated, and the CG pairs stay. Finding these islands is a common first step in genome annotation, because they mark the 5' ends of many genes. There are two standard methods. The *window rule* of Gardiner-Garden and Frommer (1987) marks every window of 200 bases with a GC content above 50 percent and a ratio of observed to expected CG above 0.6. The *HMM method* of Durbin et al. (1998) models the sequence with a [hidden Markov model](/hidden-markov-model/) with an island state and a background state, and labels each base by the most probable state path, found with the [Viterbi algorithm](/viterbi-algorithm/).

## In plain words

Islands look different from the rest of the DNA: they have more C and G, and the pair CG is not rare in them. The window method slides a window of 200 letters along the sequence, counts C, G and CG in it, and keeps the windows that are rich in C and G and have enough CG. Touching or overlapping windows that pass are joined into one island. The HMM method imagines a machine that is either inside an island or outside one and writes one letter at a time, with different letter odds in the two modes and a small chance to switch modes. For the given sequence it finds the most likely list of modes, letter by letter, and the runs of "inside" are the islands.

## The problem

**Input.** A DNA sequence $x = x_1 \cdots x_n$ over $\{A, C, G, T\}$. For the HMM method, a model with the two states $+$ (island) and $-$ (background): start probabilities $\pi_k$, transition probabilities $a_{jk}$, and emission probabilities $e_k(b)$ for the first base and $e_k(b \mid p)$ for a base $b$ after the base $p$. For the window rule, a window length $w$ and two thresholds $g$ and $r$, by default $w = 200$, $g = 0.5$ and $r = 0.6$.

**Output.** A list of disjoint intervals of $x$, the islands.

For the HMM method, the islands are the maximal runs of $+$ in a state path $q^*$ that maximizes

$$P(x, q) = \pi_{q_1} e_{q_1}(x_1) \prod_{i=2}^{n} a_{q_{i-1} q_i} \, e_{q_i}(x_i \mid x_{i-1}).$$

An emission that depends on the previous base lets each state hold a full first-order [Markov chain](/markov-chain/) of bases, so that the background state can make CG rare while C and G alone are common. This two-state model is the same as the eight-state model of Durbin et al., which has the states $A^+, C^+, G^+, T^+$ and $A^-, C^-, G^-, T^-$, each emitting its own base.

For the window rule, a window of $w$ bases with $C$ cytosines, $G$ guanines and $D$ CG pairs is marked if $(C + G)/w > g$ and $\mathrm{O/E} = D \, w / (C \, G) > r$. The ratio $\mathrm{O/E}$ compares the observed number of CG pairs with the number $C G / w$ expected if the bases were independent. The islands are the maximal unions of marked windows that overlap or touch.

## The algorithm

```pseudo id=main
VITERBI-CPG(x, model)
L1  for each state k in {+, -}: V[k] ← ln π_k + ln e_k(x_1)
L2  for i ← 2 to n do
L3      for each state k in {+, -} do
L4          ptr[i][k] ← the state j with the largest V[j] + ln a_jk
L5          V'[k] ← V[j] + ln a_jk + ln e_k(x_i | x_{i-1}) for j = ptr[i][k]
L6      V ← V'
L7  q_n ← the state k with the largest V[k]
L8  for i ← n down to 2: q_{i-1} ← ptr[i][q_i]
L9  return the maximal runs of + in q_1 ... q_n

WINDOW-CPG(x, w, g, r)
L10 for each window x[i, i + w), keeping the counts C, G and D up to date in O(1) per shift do
L11     mark the window if (C + G) / w > g and D · w / (C · G) > r
L12 return the unions of marked windows that overlap or touch
```

The decoder works with logarithms, so a sequence of a million bases does not underflow; see the [log-sum-exp trick](/log-sum-exp-trick/) for the same issue in the [forward-backward algorithm](/forward-backward-algorithm/). When the window moves one base to the right, it loses one base and one possible CG pair on the left and gains one of each on the right, so line L10 updates the three counts with a few additions instead of recounting.

## Example

Take a toy model whose emissions do not depend on the previous base. The island state emits A and T with probability 0.1 each and C and G with 0.4 each. The background state emits A and T with 0.3 each and C and G with 0.2 each. Both start probabilities are 0.5, a state stays with probability 0.8 and switches with 0.2. Decode $x = \mathrm{ATATCGCGCGTATA}$ (14 bases). The table gives $V[+]$ and $V[-]$ after each base, in natural logarithms, rounded to three places. A note "from" gives the pointer of a state when it is the other state.

| $i$ | base | $V[+]$ | $V[-]$ |
|---|---|---|---|
| 1 | A | $-2.996$ | $-1.897$ |
| 2 | T | $-5.521$ | $-3.324$ |
| 3 | A | $-7.236$ (from $-$) | $-4.751$ |
| 4 | T | $-8.663$ (from $-$) | $-6.178$ |
| 5 | C | $-8.704$ (from $-$) | $-8.011$ |
| 6 | G | $-9.844$ | $-9.844$ |
| 7 | C | $-10.983$ | $-11.676$ |
| 8 | G | $-12.123$ | $-13.509$ |
| 9 | C | $-13.262$ | $-15.341$ |
| 10 | G | $-14.401$ | $-16.481$ (from $+$) |
| 11 | T | $-16.927$ | $-17.215$ (from $+$) |
| 12 | A | $-19.453$ | $-18.642$ |
| 13 | T | $-21.979$ | $-20.069$ |
| 14 | A | $-23.981$ (from $-$) | $-21.496$ |

At $i = 14$ the larger value is $V[-] = -21.496$. Following the pointers back from $-$ at base 14 stays in $-$ down to base 11, whose pointer leads to $+$ at base 10, then stays in $+$ down to base 5, whose pointer leads to $-$ at base 4. So the best path is $----++++++----$ and the island is CGCGCG, bases 5 to 10 (the interval $[4, 10)$ from 0). Its log probability $-21.496$ beats $-22.882$ for the path with no island: the six C and G bases gain $6 \ln 2 \approx 4.16$ in the island state, more than the cost $2 \ln 4 \approx 2.77$ of the two switches. A shorter island of four C and G bases would gain only $2.77$ and would tie with the switches.

The window rule, scaled down to $w = 6$ with $g = 0.5$ and $r = 0.6$, on ATATATCGCGCGATATAT marks the windows that start at positions 4 to 8 (from 0). For example, ATCGCG has $C = 2$, $G = 2$ and $D = 2$, so its GC fraction is $4/6$ and its ratio is $2 \cdot 6 / 4 = 3$. The window GCGATA starts at 9 and has only three C and G. The union of the marked windows is $[4, 14)$, which includes two A and T bases on each side of the CG run: the window rule blurs the edges of an island by up to a window length.

## Correctness

For the HMM, let $v_i(k)$ be the largest log probability of the first $i$ bases over the paths that end in state $k$. A best path that ends in $k$ at $i$ extends a best path that ends at $i - 1$ in some state $j$, because the added term $\ln a_{jk} + \ln e_k(x_i \mid x_{i-1})$ depends only on $j$ and $k$. So $v_i(k) = \max_j (v_{i-1}(j) + \ln a_{jk}) + \ln e_k(x_i \mid x_{i-1})$, which is lines L4 and L5, and line L1 is the case $i = 1$. Line L7 takes the best end state, and the pointers of line L8 rebuild a path that reaches $\max_k v_n(k)$, the largest value of $\ln P(x, q)$ over all paths. For the window rule, each shift removes exactly one base and one candidate CG pair and adds one of each, so the counts of line L11 are those of the window, and joining marked windows in order of their start gives the maximal unions. The full proof is in the proofs folder.

## Complexity

- **Time.** The decoder does $|Q|^2 = 4$ steps for each base, so $\Theta(n)$. With $K$ states it would be $\Theta(n K^2)$. The window rule spends $\Theta(w)$ on the first window and $O(1)$ on each shift, so $\Theta(n)$.
- **Space.** The decoder keeps two pointers per base for the traceback, $\Theta(n)$. The window rule needs $O(1)$ beyond the output. If memory is short, the decoder can keep pointers only at checkpoints and recompute the rest, for $O(\sqrt{n})$ space and about twice the time.

## Properties

- **Exact for its model.** The decoder returns a path of largest probability. The quality of the islands depends on the model, not on the decoder.
- **Global decisions.** The transition probabilities set how long islands and gaps tend to be. A state that stays with probability $a$ has runs of mean length $1/(1 - a)$, so $a_{++} = 0.999$ gives islands of about 1000 bases.
- **The window rule is local.** It looks only inside one window, so its result does not depend on what is far away. Its islands start and end at window edges and include up to $w - 1$ bases of flanking DNA.
- **Both methods use the same signal.** The GC content and the O/E ratio of CG are what the island state of the HMM models, through its emission probabilities.

## Variants and improvements

- **Posterior decoding.** The [forward-backward algorithm](/forward-backward-algorithm/) gives, for each base, the probability that it is in an island. This gives a confidence for each base, and the bases with posterior above 0.5 can differ from the Viterbi path.
- **Training the model.** With labeled islands, the emission and transition probabilities are frequencies of the labeled data, the [maximum likelihood estimates](/maximum-likelihood-estimation/). Without labels, [Baum-Welch](/baum-welch-algorithm/) fits them to the sequence itself.
- **Stricter criteria.** Takai and Jones (2002) asked for more than 500 bases, a GC content of 55 percent or more and an O/E ratio of 0.65. On human chromosomes 21 and 22 this removed most of the hits in Alu repeats and left a number of islands closer to the number of genes.
- **Discrimination of known regions.** To decide whether a given short sequence is an island, compare its log probability under the island Markov chain with that under the background chain. This log-odds score is the first method of Durbin et al., chapter 3, before the HMM.
- **Masking repeats first.** Repeats such as Alu elements are GC rich and pass the window rule. Many pipelines run [repeat masking](/repeat-masking/) before the search.

## When to use it

Use CpG island detection to annotate vertebrate genomes, to find candidate promoters, and to choose regions for studies of DNA methylation. Use the window rule when you want results that match a published definition, such as the criteria of Gardiner-Garden and Frommer or of Takai and Jones. Use the HMM when you want islands with sharp edges, posterior probabilities per base, or a model that you can train on your own genome. The method relies on the depletion of CG in the rest of the genome. Takai and Jones (2002) found strong depletion in the human genome but only slight depletion in *Drosophila melanogaster* and *Saccharomyces cerevisiae*, so in such genomes islands stand out much less.

## Pitfalls

- **Expected CpG.** The ratio O/E uses $C G / w$ as the expected count of CG pairs. Other formulas for the expected count are also in use, and they give other values when C and G are unbalanced. Say which formula is used.
- **Strict and non-strict thresholds.** "Above 50 percent" and "at least 50 percent" give different islands at the edges. Check the definition you need to match.
- **Probabilities without logarithms.** A product of $n$ probabilities underflows for $n$ in the thousands. Work with logarithms throughout.
- **Zero probabilities.** A model trained by counting can have $e_k(b \mid p) = 0$, which forbids a state at some bases forever. Add pseudocounts before taking logarithms.
- **Self-transition probabilities set the island length.** With $a_{++}$ too small, the decoder breaks islands into pieces; with $a_{--}$ too close to 1, it misses short islands. Fit them, or check the length distribution of the result.
- **Lower case and N.** Soft-masked genomes use lower case for repeats; upper-case first, or decide to skip them. A run of N must be cut out or given its own state.

## Implementations

## History

Gardiner-Garden and Frommer (1987) surveyed vertebrate sequences and gave the criteria of at least 200 bases, a GC content above 50 percent and an O/E ratio of CG above 0.6, which many tools still use. Durbin, Eddy, Krogh and Mitchison (1998) used CpG islands as the running example of chapter 3 of their textbook: first a pair of Markov chains to tell island sequences from others, then a hidden Markov model with eight states to find islands in a long sequence, decoded by the Viterbi algorithm. Takai and Jones (2002) proposed stricter criteria after a study of human chromosomes 21 and 22.

## References
