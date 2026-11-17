---
tag: 7JJWSE
kind: algorithm
slug: elston-stewart-algorithm
name: Elston-Stewart algorithm
aliases:
- peeling algorithm for pedigrees
- pedigree peeling
area: biology/population-genetics
level: advanced
summary: "Computes the likelihood of the phenotypes of a pedigree by peeling one nuclear family at a time. The cost is linear in the pedigree size and cubic in the number of genotypes."
model: word-ram
complexity:
  vars: {n: the number of individuals, G: the number of joint genotypes of one individual, c: the largest number of children in a nuclear family}
  time: {worst: Θ(n G^3), average: Θ(n G^3), best: Θ(n G)}
  space: {extra: O(n G + c G^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1971
  people: [Robert C. Elston, John Stewart]
  note: "Elston and Stewart gave the recursive computation of the likelihood of a simple pedigree in 1971. Lange and Elston (1975) and Cannings, Thompson and Skolnick (1978) extended peeling to general pedigrees."
prereqs: [hardy-weinberg-principle, tree-dynamic-programming]
see_also: [lander-green-algorithm, felsenstein-pruning, variable-elimination, belief-propagation, junction-tree-algorithm, kinship-coefficient, likelihood-ratio-test, treewidth]
sources:
  - paper: doi:10.1159/000152448
    title: Robert C. Elston and John Stewart, A general model for the genetic analysis of pedigree data, Human Heredity 21(6), 1971
    locator: pp. 523-542 (the model of genotype, transmission and penetrance, and the recursive sum over the genotypes of a simple pedigree)
  - paper: doi:10.2307/1426718
    title: Chris Cannings, Elizabeth A. Thompson and Mark H. Skolnick, Probability functions on complex pedigrees, Advances in Applied Probability 10(1), 1978
    locator: pp. 26-61 (probability functions and peeling on pedigrees of arbitrary complexity)
  - book: isbn:9780387953892
    title: Kenneth Lange, Mathematical and Statistical Methods for Genetic Analysis, 2nd edition, Springer, 2002
    locator: Chapter 7, Computation of Mendelian Likelihoods (the Elston-Stewart algorithm and genotype elimination)
---

The Elston-Stewart algorithm computes the likelihood of the phenotypes observed in a family tree (a pedigree) under a genetic model of genotype frequencies, Mendelian transmission and penetrance. The direct sum runs over all joint genotypes of the $n$ individuals, which is $G^n$ terms. Peeling sums out one nuclear family at a time and passes a vector of $G$ numbers to the next family, so a pedigree without loops costs $\Theta(n G^3)$. It is the pedigree form of [dynamic programming on a tree](/tree-dynamic-programming/), and the engine of classical parametric linkage analysis with few loci.

## In plain words

A family tree records who is the child of whom, and for some people we know a trait, such as whether they have a disease. Each person carries a hidden genotype, and the model says how likely each genotype is in a founder, how parents pass genes to a child, and how likely the trait is for each genotype. We want the chance of all the known traits together. Trying every combination of genotypes is too slow for a large family. Peeling starts at the edges of the tree. For a family whose members are already summarized, it adds up over their genotypes and keeps only a small table for the one person who connects the family to the rest of the tree. Then it moves inward, family by family, until one person is left. The cost grows with the size of the tree, not with the number of combinations.

## The problem

**Input.** A pedigree on a set $I$ of $n$ individuals, where each person is a founder or has both parents in $I$, and a genetic model:

- a prior $\pi(g)$ of genotype $g \in \{1, \ldots, G\}$ in a founder, for one autosomal locus usually the [Hardy-Weinberg](/hardy-weinberg-principle/) proportions $p_a^2$ and $2 p_a p_b$;
- a transmission table $T(g \mid a, b)$, the probability that parents with genotypes $a$ and $b$ have a child with genotype $g$ (for one locus, Mendel's laws);
- a penetrance $\text{pen}_i(g)$, the probability of the phenotype of person $i$ given genotype $g$, equal to 1 for a person with no data.

**Output.** The likelihood

$$L = \sum_{\gamma \in [G]^I} \prod_{i \text{ founder}} \pi(\gamma_i) \prod_{i \text{ non-founder}} T(\gamma_i \mid \gamma_{f_i}, \gamma_{m_i}) \prod_{i \in I} \text{pen}_i(\gamma_i).$$

The individuals with the same two parents form a *nuclear family*. The algorithm needs the pedigree to have no loop: the graph $H$ that joins each family to its parents and children must be a forest. A marriage between relatives, or two families joined at two places, makes a loop.

## The algorithm

Root each component of $H$ at a person. Each node then sends one vector of length $G$ to its parent in $H$:

- a person $i$ sends $w_i(g)$, the probability of the data in its part of the tree given $\gamma_i = g$, including its own penetrance and prior;
- a family $F$ sends $M_F(g)$ to the member $p$ that joins it to the rest of the tree, the probability of the data in its part given $\gamma_p = g$.

```pseudo id=main
PEEL(pedigree, π, T, pen)
L1  build the graph H of individuals and nuclear families; fail if H has a cycle
L2  root each component of H at a person and list its nodes in preorder
L3  for each node v in reverse preorder do
L4      if v is a person i then w_i(g) ← pen_i(g) · π(g) if i is a founder, else pen_i(g)
L5          w_i(g) ← w_i(g) · product of M_F(g) over the families F below i in H
L6      else v is a family F with father f, mother m and parent p in H
L7          S_c(a, b) ← sum over g of T(g | a, b) · w_c(g), for each child c of F other than p
L8          if p = f then M_F(g) ← sum over b of w_m(b) · product over c of S_c(g, b), and the same with roles swapped if p = m
L9          if p is a child then M_F(g) ← sum over a, b of w_f(a) · w_m(b) · T(g | a, b) · product over c of S_c(a, b)
L10 return product over the roots r of (sum over g of w_r(g))
```

Line L8 peels a family onto a parent, which is the step of the original paper for a family that hangs below a person. Line L9 peels a family onto a child, which is needed when the tree reaches a family from below, for example from a person who married in. Line L7 is shared by both. The reverse preorder of line L3 makes every message ready before it is used.

## Example

Take a recessive disease with alleles $D$ (frequency 0.9) and $d$ (frequency 0.1). A person is affected exactly when the genotype is $dd$. The genotypes in the order $DD, Dd, dd$ have the prior $(0.81, 0.18, 0.01)$. Two unaffected parents have two children: child 1 is affected and child 2 is not. The penetrance vectors are $(1, 1, 0)$ for an unaffected person and $(0, 0, 1)$ for an affected one.

Root the tree at the father. The family node is his only neighbour. Lines L4 and L5 give

| person | $w$ |
|---|---|
| mother | $(0.81, 0.18, 0)$ |
| child 1 | $(0, 0, 1)$ |
| child 2 | $(1, 1, 0)$ |

Line L7 gives $S_1(a, b) = T(dd \mid a, b)$, which is $1/4$ for $Dd \times Dd$, $1/2$ for $dd \times Dd$ and 0 when a parent is $DD$, and $S_2(a, b) = 1 - T(dd \mid a, b)$. The mother cannot be $dd$, so line L8 gives

$$M_F(Dd) = 0.18 \cdot \tfrac14 \cdot \tfrac34 = 0.03375, \qquad M_F(dd) = 0.18 \cdot \tfrac12 \cdot \tfrac12 = 0.045, \qquad M_F(DD) = 0.$$

At the root, $w_{\text{father}} = (0.81, 0.18, 0) \cdot M_F = (0, 0.006075, 0)$, so line L10 returns $L = 0.006075 = 243/40000$. This is $0.18^2 \cdot \tfrac14 \cdot \tfrac34$: both parents must be carriers, the first child must be $dd$, and the second must not. Peeling again with child 2 fixed to each genotype gives the posterior $(1/3, 2/3, 0)$, so the unaffected sib is a carrier with probability $2/3$. The implementation returns these values in exact fractions.

## Correctness

Each factor of the product in the definition of $L$ belongs to one node of $H$: a person owns its prior and penetrance, and a family owns the transmission factors of its children. A factor owned by a node of a subtree involves only the people of the subtree and the parent of the subtree's root. By induction in reverse preorder, $w_i$ is the sum of the factors of the subtree of $i$ over all genotypes in it with $\gamma_i = g$, and $M_F$ is the same for a family with the genotype of its parent fixed. The induction step is the distributive law: the subtrees below a node are disjoint, so the sum of the product splits into a product of sums. Line L1 is right because a graph with $N$ nodes, $E$ edges and $K$ components is a forest exactly when $E = N - K$. The full proof is below.

## Complexity

- **Time.** Each non-founder is a child in exactly one family, and line L7 costs $G^3$ for each child, so all of line L7 costs at most $n G^3$. Lines L8 and L9 cost $O(G^2 (c + G))$ for a family with $c$ children, and there are fewer families than people. The total is $\Theta(n G^3)$ against $G^n$ for the direct sum. A pedigree of founders only, with no families, costs $\Theta(n G)$.
- **Space.** One vector per node, $O(n G)$, plus the tables $S_c$ of one family, $O(c G^2)$.
- **Many loci.** For $\ell$ linked loci a joint genotype must record the phase, so $G$ grows like $(k(k+1)/2)^\ell$ or more for $k$ alleles per locus. The cost is exponential in the number of loci, which is why the [Lander-Green algorithm](/lander-green-algorithm/) is used for many markers.
- **Genotype elimination.** Many entries of $w$ and $M$ are zero, because data rule out genotypes. Removing impossible genotypes before peeling (Lange, Chapter 7) cuts $G$ to a few values for most typed people.

## Properties

- **Exact.** No approximation: the result equals the sum of $G^n$ terms. The code uses only $+$ and $\times$, so it runs on exact fractions as well as floats.
- **Any genotype space.** The same code serves one locus with many alleles, several loci with phased genotypes, or a major gene with a polygenic class, as long as the model has the form prior, transmission and penetrance.
- **Same answer from every root.** The likelihood does not depend on the root or on the order of peeling. The order only changes the cost when the family structure is uneven.
- **Posterior genotypes.** Fixing one person's genotype and peeling again gives the posterior of that genotype. A second, outward pass, as in [belief propagation](/belief-propagation/), gives the posteriors of all people at about twice the cost of one pass.

## Variants and improvements

- **Peeling on general pedigrees.** Lange and Elston (1975) and Cannings, Thompson and Skolnick (1978) peel onto sets of people (cutsets) instead of one person, which handles any pedigree. A pedigree with loops is peeled by conditioning on the genotypes of a few people that break the loops, at a factor $G$ per broken loop, or by a [junction tree](/junction-tree-algorithm/). The cost then depends on the [treewidth](/treewidth/) of the graph.
- **As variable elimination.** Peeling is [variable elimination](/variable-elimination/) on the [Bayesian network](/bayesian-network/) of the pedigree, with an elimination order given by the family structure. [Felsenstein pruning](/felsenstein-pruning/) is the same idea on a phylogeny, where each node has one parent.
- **Faster linkage programs.** Genotype elimination and good peeling orders made linkage on large pedigrees practical in programs such as LINKAGE and VITESSE.
- **Many markers.** The [Lander-Green algorithm](/lander-green-algorithm/) swaps the roles: it is linear in the number of markers and exponential in the number of meioses.

## When to use it

- Parametric linkage analysis on large pedigrees with one or a few loci, where the LOD score compares the likelihood at a recombination fraction $\theta$ with the likelihood at $\theta = 1/2$, as in a [likelihood ratio test](/likelihood-ratio-test/).
- Segregation analysis: fitting the model of a major gene (dominant, recessive, penetrances) to the trait in families.
- Genetic counselling: the probability that a relative is a carrier, as in the example.
- When the pedigree is too large for the $2^{2n}$ states of the Lander-Green algorithm.

## Pitfalls

- **Loops.** A pedigree with a loop has no tree of families, and simple peeling is wrong or impossible. The implementation rejects it. Use loop breaking or a junction tree instead.
- **Underflow.** On a large pedigree the likelihood is tiny. Scale each vector and keep the log of the scale factors, as in the [log-sum-exp trick](/log-sum-exp-trick/).
- **Phase with many loci.** For linked loci, an unordered genotype is not enough to write the transmission table. The genotype must record which alleles are on the same chromosome.
- **Wrong model.** Allele frequencies and penetrances are inputs. A wrong allele frequency changes the founder prior and can inflate or deflate a LOD score, most when founders are untyped.
- **Inconsistent data.** A Mendelian error in the data makes $L = 0$. Check the data for Mendel errors before the analysis.

## Implementations

## History

Robert Elston and John Stewart (1971) wrote the genetic model of a pedigree as a prior, a transmission probability and a penetrance, and they showed how to compute the likelihood of a simple pedigree by summing out one generation at a time. Lange and Elston (1975) and Cannings, Thompson and Skolnick (1978) extended peeling to pedigrees of arbitrary size and complexity. The algorithm became the core of linkage programs in the 1980s and 1990s. Later work saw it as one case of variable elimination in graphical models.

## References
