---
tag: A5BRR6
kind: theorem
slug: ml-tree-np-hard
name: Maximum likelihood tree inference is NP-hard
aliases:
- Chor-Tuller theorem
- NP-hardness of maximum likelihood phylogeny
area: biology/phylogenetics
level: advanced
summary: Finding a maximum likelihood tree is NP-hard under the Jukes-Cantor model (Chor and Tuller 2005). Roch proved for the two-state model that even a 1+c approximation is hard.
prereqs: [maximum-likelihood-phylogeny, maximum-parsimony, np-hard, vertex-cover]
see_also: [maximum-parsimony-np-hard, vertex-cover-inapproximability, polynomial-time-reduction, jukes-cantor-model, phylogenetic-likelihood, small-parsimony, long-branch-attraction, ancestral-sequence-reconstruction]
sources:
  - paper: doi:10.1145/1183907.1183909
    title: Benny Chor and Tamir Tuller, Finding a maximum likelihood tree is hard, Journal of the ACM 53(5) (2006)
    locator: pp. 722 to 744 (the NP-hardness of maximum likelihood tree reconstruction; the conference version is Maximum likelihood of evolutionary trees is hard, RECOMB 2005, LNCS 3500, pp. 296 to 310)
  - paper: doi:10.1093/bioinformatics/bti1027
    title: Benny Chor and Tamir Tuller, Maximum likelihood of evolutionary trees, hardness and approximation, Bioinformatics 21(Suppl 1) (2005)
    locator: pp. i97 to i106 (hardness under the Jukes-Cantor model and its generalizations, hardness under a molecular clock, and hardness of approximating the log-likelihood within 1.00175)
  - paper: doi:10.1109/TCBB.2006.4
    title: Sebastien Roch, A short proof that phylogenetic tree reconstruction by maximum likelihood is hard, IEEE/ACM Transactions on Computational Biology and Bioinformatics 3(1) (2006)
    locator: pp. 92 to 94 (Theorem 1 for the CFN model, Claims 1 to 3, Propositions 1 and 2)
  - paper: "Andrea E. F. Clementi and Luca Trevisan, Improved non-approximability results for minimum vertex cover with density constraints, Theoretical Computer Science 225(1-2), 1999, pages 113 to 128"
    locator: no 1.16-approximation for vertex cover on graphs of bounded degree unless P = NP
  - paper: "H. Todd Wareham, On the computational complexity of inferring evolutionary trees, MSc thesis, Memorial University of Newfoundland, 1993"
    locator: the approximation-preserving reduction from bounded-degree vertex cover to maximum parsimony, as used by Roch
  - paper: "Chris Tuffley and Mike Steel, Links between maximum likelihood and maximum parsimony under a simple model of site substitution, Bulletin of Mathematical Biology 59(3), 1997, pages 581 to 607"
    locator: maximum likelihood under no common mechanism equals maximum parsimony
---

Maximum likelihood is the standard criterion for building trees from sequences, and for a fixed tree the likelihood takes linear time. Chor and Tuller proved in 2005 that the search over trees cannot be made efficient: finding a [maximum likelihood tree](/maximum-likelihood-phylogeny/) is NP-hard under the Jukes-Cantor model and its generalizations. In 2006 Roch gave a three-page proof of a stronger form for the two-state Cavender-Farris-Neyman (CFN) model, the binary version of [JC69](/jukes-cantor-model/): even an approximation of the optimum within a factor $1 + c$, for some constant $c > 0$, is NP-hard. Both proofs go through [maximum parsimony](/maximum-parsimony/). This page states both results and gives Roch's proof.

## Statement

**The CFN model.** Characters are binary, $\chi : \{\text{taxa}\} \to \{0, 1\}$. A tree $T$ on the taxa has no internal vertex of degree 2, and each edge $e$ has a flip probability $p_e \in [0, \tfrac12]$; under a branch length $t_e$ it is $p_e = \tfrac12 (1 - e^{-2t_e})$. The root state is uniform, and each edge flips the state with probability $p_e$, independently. For characters $X = (\chi^1, \ldots, \chi^k)$, the problem ML is to minimize

$$\tilde L(X \mid T, p) = -\sum_{i=1}^{k} \ln\bigl(2\, P[\chi^i \mid T, p]\bigr)$$

over all trees $T$ and all $p$. This is the negative log-likelihood plus the constant $-k \ln 2$, which makes every term nonnegative.

**Theorem (Roch 2006).** There is a constant $c > 0$ such that, unless P = NP, no polynomial-time algorithm returns, for every input $X$, a tree $T$ and parameters $p$ with $\tilde L(X \mid T, p) \le (1 + c) \min_{T', p'} \tilde L(X \mid T', p')$. In particular, no polynomial-time algorithm finds a maximum likelihood tree under the CFN model unless P = NP.

**Theorem (Chor and Tuller 2005).** Under the Jukes-Cantor model of substitution and its generalizations, deciding whether some tree with branch lengths has likelihood at least a given value is NP-hard. In the version of the ISMB 2005 paper, maximum likelihood is also NP-hard under a molecular clock, and approximating the maximum log-likelihood within any factor smaller than $1.00175$ is NP-hard.

In both results the model is fixed and is part of the problem; the input is only the alignment. The free parameters are the topology and the branch lengths.

## In plain words

Scoring one family tree by how likely it makes the observed genes is quick. The question is whether finding the best tree can also be quick. These results say no, unless a long list of other hard problems all turn out to be easy too.

The trick is to add a large number of positions where every species has the same letter. Such positions push every branch of a good tree to be very short. On a tree with very short branches, the most likely story for each position is the story with the fewest changes. So the best tree for likelihood is nearly the best tree for the fewest-changes score, and finding that tree is already known to be hard, even roughly.

## Proof

The full proof is in [the proof page](proofs/main.md). Here is its plan.

**Step 1: parsimony is hard to approximate.** Wareham (1993) reduces [vertex cover](/vertex-cover/) on graphs of degree at most $B$ to maximum parsimony, so that a $(1 + c')$-approximation for parsimony gives a $(1 + 2Bc')$-approximation for vertex cover. Clementi and Trevisan (1999) showed that bounded-degree vertex cover has no $1.16$-approximation unless P = NP ([vertex cover inapproximability](/vertex-cover-inapproximability/)). So there is $c_0 > 0$ for which parsimony has no $(1 + c_0)$-approximation. The proof uses this step as a black box.

**Step 2: add constant characters.** Given a parsimony instance $X$ with $n$ taxa and $k$ characters, none of them constant, let $M = \max\{2n, k\}$, fix a small $\varepsilon > 0$, and append $N_c = \lceil M^{1/\varepsilon} \rceil$ all-zero characters. For fixed $\varepsilon$ this is a polynomial-time map. It does not change any parsimony score. Let $K = k + N_c$.

**Step 3: likelihood is close to $\ln K$ times parsimony.** Three estimates hold for every tree $T$:

- *Upper bound.* With every $p_e = l(X, T) / (EK)$, where $E$ is the number of edges, the score is at most $(1 + 2\varepsilon)\, l(X, T) \ln K$. The most parsimonious labeling alone already has this probability.
- *Short edges.* If the score is at most $\beta$, then every $p_e \le \beta / N_c$: a longer edge would make the many all-zero characters too unlikely, because the two leaves on a path through that edge would differ with probability at least $p_e$.
- *Lower bound.* If all $p_e$ are that small, the probability of a character with parsimony score $l$ is at most $(E \bar p)^l$, since labelings with $j$ changes number at most $E^j$. This gives a score of at least $(1 - 5\varepsilon)\, l(X, T) \ln K$.

**Step 4: combine.** A $(1 + c)$-approximate ML solution $(T, p)$ for the padded instance has score at most $(1 + c)(1 + 2\varepsilon)\, l^* \ln K$, where $l^*$ is the optimal parsimony score. By the short-edge and lower-bound estimates, its tree has $l(X, T) \le \frac{(1 + c)(1 + 2\varepsilon)}{1 - 5\varepsilon} l^*$. For small $c$ and $\varepsilon$, the factor is below $1 + c_0$, which contradicts Step 1 unless P = NP. $\blacksquare$

**About the proof of Chor and Tuller.** Their proof also starts from the hardness of approximating vertex cover and uses the link of Tuffley and Steel between likelihood and parsimony, but it needs a longer chain of constructions, and it covers the four-state Jukes-Cantor model. Roch's paper calls these constructions "rather involved" and gives the shorter route above for the binary model.

## Consequences

- **No exact polynomial algorithm.** Unless P = NP, no algorithm finds a maximum likelihood tree in polynomial time, so the hill-climbing programs (PhyML, RAxML, IQ-TREE) on the [maximum likelihood phylogeny](/maximum-likelihood-phylogeny/) page cannot come with a guarantee of optimality.
- **No approximation scheme.** For the CFN model, there is no polynomial-time approximation scheme for the negative log-likelihood, unless P = NP.
- **Likelihood and parsimony agree on short trees.** The proof shows a quantitative form of a known fact: when all branches are short, maximum likelihood and [maximum parsimony](/maximum-parsimony/) pick nearly the same trees. Far from that regime, as in the [long branch attraction](/long-branch-attraction/) zone, they differ.
- **Related problems.** Ancestral maximum likelihood, which maximizes over the internal states as well, is NP-hard by a separate proof of Addario-Berry, Chor, Hallett, Lagergren, Panconesi and Wareham (2004). Maximum likelihood under a molecular clock is NP-hard by the ISMB 2005 paper.

## Tightness

- **The model.** Roch's statement is for the binary CFN model; it is not a statement about all substitution models. Chor and Tuller's covers the Jukes-Cantor model and its generalizations. A result for one model does not transfer to another by itself, because the likelihood landscape changes with the model.
- **The constant.** The constants are very small: $c$ in Roch's proof comes from $0.16 / (2B)$ for a large degree bound $B$, and Chor and Tuller's factor is $1.00175$. The results say nothing about larger approximation factors.
- **The instances.** The hard instances have a huge share of constant sites, of order $M^{1/\varepsilon}$, and only short branches. Real alignments also have many constant sites, but the proof does not show that typical data are hard.
- **Fixed number of taxa.** For a fixed number of taxa, the number of topologies is a constant, so the hardness needs $n$ to grow. Even then, the inner problem of fitting branch lengths to one tree is a non-concave optimization with no known polynomial global method in general.

## History

[Maximum parsimony](/maximum-parsimony/) was shown NP-hard by Foulds and Graham in 1982 ([NP-hardness of parsimony](/maximum-parsimony-np-hard/)), while the complexity of maximum likelihood stayed open for more than twenty years after Felsenstein's 1981 paper. Tuffley and Steel linked the two criteria in 1997 through the no-common-mechanism model. Addario-Berry and coauthors proved ancestral maximum likelihood NP-hard in 2004. Chor and Tuller then proved maximum likelihood itself NP-hard at RECOMB 2005, with the hardness of approximation and the molecular clock case at ISMB 2005 and the full version in the Journal of the ACM in 2006. The same year Roch published the short proof for the two-state model in IEEE/ACM TCBB.

## References
