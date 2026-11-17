---
tag: 13J1K1
kind: algorithm
slug: lander-green-algorithm
name: Lander-Green algorithm
aliases:
- Lander-Green HMM
- multipoint linkage HMM
area: biology/population-genetics
level: advanced
summary: "Computes multipoint pedigree likelihoods with a hidden Markov model over inheritance vectors along the chromosome. Linear in the markers, exponential in the meioses."
model: word-ram
complexity:
  vars: {M: the number of markers, b: the number of meioses (twice the number of non-founders), n: the number of people}
  time: {worst: Θ(M 2^b (b + n)), average: Θ(M 2^b (b + n)), best: Θ(M 2^b (b + n))}
  space: {extra: Θ(M 2^b)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1987
  people: [Eric S. Lander, Philip Green]
  note: "Lander and Green described the hidden Markov model over inheritance patterns for multilocus linkage maps in 1987. Kruglyak, Daly, Reeve-Daly and Lander (1996) built GENEHUNTER on it."
prereqs: [hidden-markov-model, forward-backward-algorithm, identity-by-descent]
see_also: [elston-stewart-algorithm, kinship-coefficient, viterbi-algorithm, hamming-distance, kronecker-product, walsh-hadamard-transform, log-sum-exp-trick, likelihood-ratio-test]
sources:
  - paper: doi:10.1073/pnas.84.8.2363
    title: Eric S. Lander and Philip Green, Construction of multilocus genetic linkage maps in humans, Proceedings of the National Academy of Sciences USA 84(8), 1987
    locator: pp. 2363-2367 (the inheritance vectors as hidden states along the chromosome, and the computation linear in the number of loci)
  - paper: "Leonid Kruglyak, Mark J. Daly, Mary Pat Reeve-Daly and Eric S. Lander, Parametric and nonparametric linkage analysis, a unified multipoint approach, American Journal of Human Genetics 58(6), 1996"
    title: Kruglyak, Daly, Reeve-Daly and Lander 1996
    locator: pp. 1347-1363 (the inheritance vector, founder symmetry with 2n - f bits of entropy, and IBD sharing at every point of the map)
  - book: isbn:9780387953892
    title: Kenneth Lange, Mathematical and Statistical Methods for Genetic Analysis, 2nd edition, Springer, 2002
    locator: Chapter 9, Descent Graph Methods
---

The Lander-Green algorithm computes the likelihood of marker data on a pedigree for many linked markers at once. Its hidden state at each marker is the *inheritance vector*, one bit per meiosis saying whether the parent passed on its paternal or its maternal gene. Along the chromosome these vectors form a Markov chain, so the [forward-backward algorithm](/forward-backward-algorithm/) gives the likelihood and the posterior of every vector. The cost is linear in the number of markers and exponential in the number of meioses, the opposite trade from the [Elston-Stewart algorithm](/elston-stewart-algorithm/).

## In plain words

In a family tree, each child got one of two genes from the father and one of two from the mother. Writing down these choices for every child gives a short string of bits. If we knew the bits, we would know which genes are copies of the same gene from a grandparent, and the chance of the marker data would be easy to work out. We do not know them, but along the chromosome they change only where a crossover happened, and crossovers are rare between close markers. So the bits behave like the hidden states of a hidden Markov model: they change from marker to marker with a known small chance, and each marker gives evidence about them. A forward sweep along the chromosome adds up over all bit strings at all markers, and a backward sweep tells how likely each string is at each point.

## The problem

**Input.** A pedigree with $f$ founders and $k$ non-founders, so $b = 2k$ meioses. For each of $M$ ordered markers on one chromosome: the allele frequencies $q_j$ and the unordered genotypes $D_j$ of the typed people. For each pair of adjacent markers: the recombination fraction $\theta_j$, for example $\theta = \tfrac12 (1 - e^{-2d})$ for a map distance of $d$ Morgans under the Haldane map function.

**Model.** The inheritance vector $V_j \in \{0, 1\}^b$ at marker $j$ is uniform at the first marker. Between markers $j$ and $j + 1$, each bit flips with probability $\theta_j$, independently (no interference). Given $V_j$, each person carries two known founder genes, and the founder genes get independent alleles with frequencies $q_j$.

**Output.** The likelihood $L = \Pr(D_1, \ldots, D_M)$ and the posterior $\Pr(V_j = v \mid D_1, \ldots, D_M)$ for every marker $j$ and vector $v$. From the posterior follow the [identity by descent](/identity-by-descent/) probabilities of any pair of relatives at every marker.

## The algorithm

The emission $e_j(v) = \Pr(D_j \mid V_j = v)$ is computed on a small graph: its nodes are the founder genes, and each typed person is an edge between the two founder genes that it carries under $v$. In a connected part of this graph, the allele of one gene fixes the alleles of all others, so there are at most two fitting assignments. The transition matrix $A(u, v) = \theta^{h(u, v)} (1 - \theta)^{b - h(u, v)}$, with $h$ the [Hamming distance](/hamming-distance/), is a [Kronecker product](/kronecker-product/) of $b$ matrices of size $2 \times 2$. So it acts on a vector one bit at a time.

```pseudo id=main
LANDER-GREEN(pedigree, D, q, θ)
L1  e_j(v) ← P(D_j | V_j = v) for each marker j and vector v, by the founder gene graph
L2  α(v) ← 2^-b · e_1(v) for each v
L3  for j ← 1 to M do
L4      if j > 1 then α ← A(θ_{j-1}) α, applied one bit at a time
L5          α(v) ← α(v) · e_j(v) for each v
L6      c_j ← sum of α; if c_j = 0 then fail (Mendel error); α_j ← α / c_j
L7  log L ← sum over j of log c_j
L8  β_M ← 1; for j ← M - 1 down to 1 do β_j ← A(θ_j) (e_{j+1} · β_{j+1}) / c_{j+1}
L9      post_j(v) ← α_j(v) · β_j(v), and post_M ← α_M
```

The scaling by $c_j$ in line L6 keeps the numbers in range on long chromosomes and gives the log-likelihood directly.

## Example

Take a father with genotype 1/2, a mother with 3/4, and two children who are both 1/3, at a marker with four alleles of frequency $1/4$. The vector has 4 bits: the paternal and maternal choices of child A and of child B, so 16 vectors.

- Both children got allele 1 from the father and allele 3 from the mother. So under a fitting vector the paternal bits of A and B are equal, and so are the maternal bits. Four of the 16 vectors fit, one for each choice of which gene of each parent carries the allele 1 or 3.
- Under each of them the four founder genes have fixed alleles, so $e_1(v) = (1/4)^4 = 1/256$, and $L = 4 \cdot 2^{-4} \cdot (1/256) = 1/1024$.
- Under every fitting vector the sibs share both founder genes, so they are IBD 2 at this marker with probability 1.

Add an untyped marker at $\theta = 0.1$ from the first. The sibs still share the paternal gene when both or neither of their paternal meioses recombine, with probability $0.9^2 + 0.1^2 = 0.82$, and the same holds for the maternal gene. So at the second marker the sibs are IBD 2 with probability $0.82^2 = 0.6724$, IBD 1 with probability $2 \cdot 0.82 \cdot 0.18 = 0.2952$ and IBD 0 with probability $0.18^2 = 0.0324$. The implementation returns these numbers.

## Correctness

The vectors form a Markov chain, and the data at a marker depend only on the vector there, so the model is a hidden Markov model. The emission is right because a founder gene graph with one fixed allele has at most one fitting assignment per connected part, which the search finds and checks. The transition is right because $A$ is the Kronecker product of the $2 \times 2$ flip matrices, so applying them bit by bit is the full product. By induction, $\alpha_j$ is the posterior of $V_j$ given the data up to marker $j$ and $c_j$ is the probability of $D_j$ given the earlier data, so $\prod_j c_j = L$ by the chain rule. The backward pass gives the rest, and the product $\alpha_j \beta_j$ is the full posterior because the past and the future data are independent given $V_j$. The full proof is below.

## Complexity

- **Time.** Line L1 builds the gene flow for each of the $2^b$ vectors in $O(n)$ and checks each marker in $O(n)$, so $\Theta(M 2^b n)$. The bitwise transition of lines L4 and L8 costs $\Theta(b 2^b)$ per marker against $4^b$ for a dense matrix product. The total is $\Theta(M 2^b (b + n))$.
- **Space.** $\Theta(M 2^b)$ for the emissions, the forward vectors and the posteriors. A two-pass version that recomputes the emissions needs less.
- **The limit.** With $b = 2k$, the state space doubles with every meiosis. At $b = 30$ one vector of probabilities already has about $10^9$ entries, so the method fits small and medium pedigrees.
- **Founder symmetry.** Swapping the two genes of a founder does not change the probability of the data, so the choices of one child of each founder can be fixed. Kruglyak and coworkers (1996) give $2k - f$ bits of real information, and the state space shrinks by $2^f$.

## Properties

- **Exact.** The likelihood is the exact sum over all $2^{bM}$ paths of vectors.
- **Multipoint.** All markers contribute at once, so missing genotypes and markers with few alleles are filled in by their neighbours.
- **IBD at every point.** The posterior gives the IBD distribution of any pair of relatives at any marker, which is the input of nonparametric linkage.
- **Unlinked markers factor.** With $\theta_j = 1/2$, the flip matrix makes the vector uniform, and the likelihood is the product of single-marker likelihoods.
- **Model assumptions.** No interference, linkage equilibrium between markers in founders, and a known map. All three are assumed in the emission or the transition.

## Variants and improvements

- **Trait locus.** For parametric linkage, a trait locus with penetrances is placed between markers, and the likelihood ratio against $\theta = 1/2$ gives the LOD score, a [likelihood ratio test](/likelihood-ratio-test/) on a $\log_{10}$ scale.
- **GENEHUNTER.** Kruglyak, Daly, Reeve-Daly and Lander (1996) used the vector HMM for both parametric and nonparametric linkage, with founder symmetry and a fast transition.
- **Sparse gene flow trees.** Merlin (Abecasis and coworkers) stores the emissions and posteriors as trees that merge vectors with the same value, which saves time and memory on dense maps.
- **Most likely vectors.** The [Viterbi algorithm](/viterbi-algorithm/) on the same chain gives the most likely inheritance path, which shows the crossovers and helps find genotyping errors.
- **Sampling.** For large pedigrees, Markov chain Monte Carlo over descent graphs replaces the exact sum (Lange, Chapter 9).

## When to use it

- Multipoint linkage analysis in small and medium pedigrees with dense marker maps.
- Estimating IBD sharing of relatives along the chromosome, for example sib pairs in affected sib pair studies or relatives in a [kinship coefficient](/kinship-coefficient/) study.
- Finding crossovers and Mendel errors in family genotype data.
- When the pedigree is too large, use the Elston-Stewart algorithm for few loci, or sampling methods.

## Pitfalls

- **Exponential in pedigree size.** Each extra non-founder multiplies the state space by 4. Check $2^b$ before a run.
- **Linkage disequilibrium.** Dense SNP maps break the assumption of independent markers in founders. Untyped founders then make the shared haplotypes look like extra IBD, which inflates linkage evidence. Thin the markers or model the haplotypes.
- **Underflow.** Without the scaling of line L6, the forward vector underflows after a few hundred markers.
- **Map errors.** Wrong genetic distances distort the transitions. Too short a distance hides real crossovers and can make good data look like errors.
- **Genotyping errors.** A single error can make $c_j = 0$ and stop the computation. Programs add a small error rate to the emission.

## Implementations

## History

Eric Lander and Philip Green (1987) saw that the inheritance pattern of a pedigree along the chromosome is a Markov chain, and they used this to build multilocus linkage maps with dozens of markers in three-generation families, in time linear in the number of loci. The Elston-Stewart method was exponential in the number of loci, so this changed what multipoint linkage could do. Kruglyak and coworkers (1996) put the method into GENEHUNTER, and later programs such as Merlin made it faster on dense maps.

## References
