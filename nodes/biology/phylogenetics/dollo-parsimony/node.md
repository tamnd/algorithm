---
tag: CQ9087
kind: problem
slug: dollo-parsimony
name: Dollo parsimony
area: biology/phylogenetics
level: advanced
summary: Parsimony for two-state characters on a rooted tree in which the derived state arises only once and may then be lost any number of times. The score counts the gain and the losses.
prereqs: [small-parsimony, camin-sokal-parsimony]
see_also: [wagner-parsimony, maximum-parsimony, sankoff-algorithm, lowest-common-ancestor, maximum-parsimony-np-hard, perfect-phylogeny]
sources:
  - paper: doi:10.2307/2412469
    title: Walter J. Le Quesne, The uniquely evolved character concept and its cladistic application, Systematic Zoology 23(4), 1974, 513-517
    locator: the concept of a character state that evolved only once
  - paper: doi:10.2307/2412867
    title: James S. Farris, Phylogenetic analysis under Dollo's law, Systematic Zoology 26(1), 1977, 77-88
    locator: parsimony with one forward change from 0 to 1 and as many reversions as needed
  - paper: doi:10.1016/0025-5564(86)90161-6
    title: William H. E. Day, David S. Johnson and David Sankoff, The computational complexity of inferring rooted phylogenies by parsimony, Mathematical Biosciences 81(1), 1986, 33-42
    locator: the NP-completeness of the Dollo version of parsimony
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 7, Variants of parsimony, the section on Dollo parsimony
---

Dollo parsimony is [parsimony](/maximum-parsimony/) for two-state characters on a rooted tree under a strict rule: the derived state 1 arises at most once, from the ancestral state 0, and it can then be lost, back to 0, any number of times. A state 1 that was lost can never come back. The score of a tree is the number of changes, one gain and the losses. The rule takes its name from Dollo's law, the idea of the palaeontologist Louis Dollo that a complex structure that evolution has lost is not regained. Le Quesne (1974) and Farris (1977) made it a parsimony method. For a fixed tree, the gain goes on the edge above the [lowest common ancestor](/lowest-common-ancestor/) of the leaves with state 1, and the score follows in linear time. The search over trees is NP-hard (Day, Johnson and Sankoff 1986).

## In plain words

Some traits are hard to build and easy to lose. An eye, a complex enzyme or an intron is unlikely to arise twice in the same form, but a lineage can lose it. Dollo parsimony assumes this for each character: the trait appears once on the tree, and after that it may vanish in any number of branches.

On a given tree, the trait must first appear in the common ancestor of all species that have it, or above it. Putting it exactly there is best. Then every group of species below that ancestor that lacks the trait needs one loss, on the branch above the group. The score is one gain plus the number of these groups. The best tree is the one with the smallest score.

## Definition

**Characters.** A character has the states 0 (ancestral) and 1 (derived). A labeling gives each node of the rooted tree $T$ a state, with an extra ancestor of state 0 above the root, and agrees with the observed states $x$ at the leaves.

**Dollo labelings.** A labeling is a Dollo labeling if at most one edge goes from state 0 to state 1. Its cost is the number of edges whose ends differ: the gain, if there is one, plus the edges from 1 to 0, the losses.

**Small Dollo parsimony.** Given $T$ and $x$, find a Dollo labeling of least cost.

**Large Dollo parsimony.** Given $m$ binary characters on $n$ taxa, find a rooted tree whose total small Dollo score is least.

**The solution of the small problem.** If no leaf has state 1, the score is 0. Otherwise let $z$ be the lowest common ancestor of the leaves with state 1. Call a node below $z$ a zero clade if all leaves below it have state 0 but its parent has a leaf of state 1 below it. Then

$$\operatorname{score} = 1 + (\text{number of zero clades}).$$

*Proof.* In a Dollo labeling, the nodes of state 1 are the nodes below the gain that have no loss on their path from it. Every leaf of state 1 is such a node, so the gain is at or above $z$, and every node on a path from $z$ to a leaf of state 1 has state 1. The parent of a zero clade $c$ is on such a path, so it has state 1. All leaves of $c$ have state 0, so a loss must lie on the edge above $c$ or inside $c$. Different zero clades are disjoint subtrees, so they need different losses. With the gain, this gives at least $1 + $ the number of zero clades changes. The labeling with the gain on the edge above $z$, state 1 on all nodes below $z$ outside the zero clades, and a loss on the edge above each zero clade, reaches this number. $\blacksquare$

This takes one pass to find $z$ and one pass to count the zero clades, $O(n)$ time per character.

## Variants

- **Camin-Sokal parsimony.** The opposite rule: gains may happen many times, but losses never ([Camin-Sokal parsimony](/camin-sokal-parsimony/)).
- **Unrooted Dollo.** If the ancestral state is not known, the root and the choice of state 0 matter, so the tree must be rooted. Some programs choose the root and the polarity to fit the data.
- **Relaxed Dollo.** Instead of a strict rule, give a gain a much higher cost than a loss, which is [Sankoff parsimony](/sankoff-algorithm/) with an asymmetric table. With a gain cost $W$ larger than the number of edges, the best labeling has exactly one gain, so it is a Dollo labeling, and its cost is $W$ plus the Dollo losses.
- **Multistate Dollo.** Characters with an ordered chain of derived states, each arising once, can be split into binary characters.
- **Stochastic Dollo models.** Likelihood versions of the same idea, with one origin of the trait and a rate of loss, are used for gene families and morphology.

## Examples

**Six taxa.** Take the rooted tree $(((L_1, L_2), L_3), ((L_4, L_5), L_6))$ and these three characters. The other columns are the same characters under [Fitch](/fitch-algorithm/) parsimony with a free root, and under [Camin-Sokal](/camin-sokal-parsimony/) parsimony.

| character on $L_1, \ldots, L_6$ | lowest common ancestor of the 1s | zero clades | Dollo | Fitch | Camin-Sokal |
|---|---|---|---|---|---|
| 1 1 0 1 0 0 | root | $L_3$, $L_5$, $L_6$ | 4 | 2 | 2 |
| 0 0 1 1 1 1 | root | $(L_1, L_2)$ | 2 | 1 | 2 |
| 0 1 1 0 1 1 | root | $L_1$, $L_4$ | 3 | 2 | 4 |

For the first character, the leaves with state 1 are spread over both halves of the tree, so the single gain must be at the root. Then $L_3$, $L_5$ and $L_6$ each need a loss: four changes, while Camin-Sokal explains the same character with two separate gains. The two models give opposite rankings on the first and the third character, so they can choose different trees for the same data.

**When Dollo is cheap.** A character that is 1 in exactly one clade of the tree costs 1 under Dollo, the same as under Fitch: one gain, no losses.

## Known algorithms

- **Small problem.** The rule above: find the [lowest common ancestor](/lowest-common-ancestor/) of the leaves with state 1 in a [postorder](/postorder-traversal/) pass that counts, for each node, the leaves of state 1 below it, then count the zero clades. $O(n)$ time per character.
- **Sankoff form.** The [Sankoff algorithm](/sankoff-algorithm/) with the gain cost $W$ of the relaxed variant gives the same labeling in $O(n)$ time per character, as $k = 2$.
- **Large problem.** Branch and bound or the heuristics of [maximum parsimony](/maximum-parsimony/), with the Dollo score of each character.

## Bounds

- **NP-hard.** Large Dollo parsimony is NP-complete (Day, Johnson and Sankoff 1986). The simple reduction on [the NP-hardness page](/maximum-parsimony-np-hard/) is for unordered and Camin-Sokal parsimony; the Dollo case needs a different construction, which is in that paper.
- **Per character.** A character with at least one leaf of state 1 costs at least 1, and exactly 1 on a tree in which its leaves of state 1 form a clade.
- **Compared with Fitch.** A Dollo labeling is a labeling, so the Dollo score of a character is at least its Fitch score with the root fixed to 0.

## Reductions

- **To weighted parsimony.** As in the relaxed variant, small Dollo parsimony is Sankoff parsimony with $\delta(0, 1) = W$, $\delta(1, 0) = 1$, an ancestor of state 0 above the root, and $W$ larger than the number of edges. If some leaf has state 1, the Dollo score is the Sankoff score minus $W$.
- **To perfect phylogeny.** If every character can be explained by its gain alone, with no loss, the characters are a rooted [perfect phylogeny](/perfect-phylogeny/), and that tree is optimal for Dollo, Camin-Sokal and Fitch parsimony at the same time.

## Applications

- **Gene content.** The presence or absence of gene families across genomes is often analyzed with Dollo parsimony: a gene family arises once and is lost in many lineages.
- **Introns and restriction sites.** The gain of an intron at a given place, or of a restriction site, is rare compared with its loss, which fits the Dollo rule.
- **Complex morphological traits.** Structures that need many genes, such as eyes or wings, are the classic case for Dollo's law.

## References
