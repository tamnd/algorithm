---
tag: PG6CCH
kind: concept
slug: parsimony-informative-site
name: Parsimony-informative site
aliases:
- informative site
area: biology/phylogenetics
level: core
summary: A site where at least two states each occur in at least two taxa. Only these sites can change which tree is most parsimonious under unit costs.
prereqs: [maximum-parsimony, small-parsimony]
see_also: [fitch-algorithm, quartet, four-gamete-condition, character-compatibility, long-branch-attraction, wagner-parsimony]
sources:
  - paper: doi:10.1086/283157
    title: Walter M. Fitch, On the problem of discovering the most parsimonious tree, The American Naturalist 111(978), 1977, 223-257
    locator: the lower bound on the number of substitutions that a set of sites requires on any tree
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 1, Parsimony methods, and Chapter 2, Counting evolutionary changes
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Section 10.11, Large Parsimony Problem
---

A site of an alignment is parsimony-informative if at least two of its states each occur in at least two taxa. For example, the column AACCG on five taxa is informative, because A and C each occur twice, and the column AACGT is not, because only A occurs twice. Under unit costs, a site that is not informative needs the same number of changes on every tree, namely the number of its distinct states minus one. An informative site needs fewer changes on some trees than on others. So only the informative sites can choose between trees in [maximum parsimony](/maximum-parsimony/), and a search can drop the other sites and add back their constant cost.

## In plain words

Look at one column of the alignment. If every letter in it but one appears only once, the column cannot tell trees apart. Any tree explains it in the same way: the ancestors all have the common letter, and each rare letter appears on the branch to its own species. That costs one change per rare letter, whatever the tree.

A column helps only when two different letters each appear at least twice. Then some trees put the two species with letter A together and the two species with letter C together, and they need fewer changes. Other trees mix them up, and they need more. Such a column is informative.

A column with the same letter everywhere is the extreme case: it costs nothing on any tree.

## The idea

Fix a site with $n$ taxa, and let $r$ be the number of distinct states in it. Write $\operatorname{PS}(T)$ for its [small parsimony](/small-parsimony/) score on an unrooted tree $T$ under unit costs. Call the site informative if at least two states each occur in at least two taxa.

**Theorem.** For $n \ge 4$, the following hold.

1. $\operatorname{PS}(T) \ge r - 1$ for every tree $T$.
2. If the site is not informative, then $\operatorname{PS}(T) = r - 1$ for every tree $T$.
3. If the site is informative, then some tree has $\operatorname{PS}(T) = r - 1$ and some tree has $\operatorname{PS}(T) \ge r$.

So the score of a site is the same on all trees if and only if the site is not informative. For $n \le 3$ there is only one unrooted tree, and the question does not arise.

**Proof of 1.** Take a labeling of $T$ with $c$ changes. Remove the $c$ edges whose ends have different states. This leaves $c + 1$ connected parts, and all nodes in one part have the same state. Each of the $r$ states occurs at some leaf, so it needs at least one part. So $c + 1 \ge r$.

**Proof of 2.** If the site is not informative, at most one state occurs two or more times. Let $a$ be that state, or any state of the site if there is none. Give $a$ to every internal node of $T$. Then the only changes are on the edges to the leaves whose state is not $a$. Each state other than $a$ occurs exactly once, so there are $r - 1$ such leaves and $r - 1$ changes. With part 1, $\operatorname{PS}(T) = r - 1$.

**Proof of 3.** Let $a$ and $b$ be two states with leaves $a_1, a_2$ in state $a$ and $b_1, b_2$ in state $b$.

*A tree with score $r - 1$.* For each state $s$, make a subtree whose leaves are the taxa in state $s$, and give $s$ to its internal nodes. Join the roots of these $r$ subtrees by any tree whose internal nodes all have state $a$, and resolve the nodes of high degree into binary nodes with the same state. The only changes are on the $r - 1$ edges into the subtrees of the states other than $a$.

*A tree with score at least $r$.* Take any tree $T$ that has an edge $e$ with $a_1, b_1$ on one side and $a_2, b_2$ on the other, so that it displays the [quartet](/quartet/) $a_1 b_1 \mid a_2 b_2$. Such a tree exists for $n \ge 4$. Suppose a labeling of $T$ has only $r - 1$ changes. By the proof of part 1, the $r$ parts are then one part for each state. So the part of state $a$ is connected and holds the path from $a_1$ to $a_2$, and the part of state $b$ holds the path from $b_1$ to $b_2$. Both paths use the edge $e$, so its end nodes would have both state $a$ and state $b$, which is impossible. So every labeling of $T$ has at least $r$ changes. $\blacksquare$

**An upper bound.** No tree costs more than $n - f$, where $f$ is the count of the most frequent state: give that state to all internal nodes. For a site that is not informative, $n - f = r - 1$, so the lower and the upper bound meet, which is another way to see part 2.

**Only for unit costs.** The theorem is about the unit cost of [Fitch's algorithm](/fitch-algorithm/). Under other costs a site that is not informative in this sense can still prefer some trees. For example, take the ordered states 0, 1, 2, 3 of [Wagner parsimony](/wagner-parsimony/) on four taxa with one state each. The tree $01 \mid 23$ costs 3, and the tree $02 \mid 13$ costs 4.

## Examples

**Four taxa.** On taxa $A, B, C, D$ in this order, the three trees are $AB \mid CD$, $AC \mid BD$ and $AD \mid BC$.

| site | informative | score on $AB \mid CD$ | on $AC \mid BD$ | on $AD \mid BC$ |
|---|---|---|---|---|
| AAAA | no | 0 | 0 | 0 |
| AAAC | no | 1 | 1 | 1 |
| AACG | no | 2 | 2 | 2 |
| ACGT | no | 3 | 3 | 3 |
| AACC | yes | 1 | 2 | 2 |
| ACAC | yes | 2 | 1 | 2 |

On four taxa, the informative sites are exactly those of the form $xxyy$, each of which supports one of the three trees.

**Five taxa.** In the example of [maximum parsimony](/maximum-parsimony/), the columns of the 8 sites are AAAGG, AAGGG, GGGAA, TCCCC, TTTTA, CCTTT, GGGGA and AACCC. The sites 1, 2, 3, 6 and 8 are informative. The sites 4, 5 and 7 each have one taxon that differs from the other four, so they cost 1 on all 15 trees. The scores of the 15 trees on all sites are 8, 10, 10, 11, 11 and ten times 13. On the informative sites alone they are 5, 7, 7, 8, 8 and ten times 10: the same order, each lower by 3.

**Variable but not informative.** The site AACGT on five taxa has four states and is variable, but only A repeats. Every tree needs exactly 3 changes for it, one on the branch to each of C, G and T.

## Where it is used

- **Faster parsimony search.** Programs for [maximum parsimony](/maximum-parsimony/) count the sites that are not informative once, add their constant cost, and search with the informative sites only. In large alignments this often removes most of the sites.
- **Reporting.** Papers often give the number of parsimony-informative sites of an alignment as a rough measure of how much signal it has for the tree.
- **Indices of fit.** Measures such as the consistency index compare the score of a tree to the lower bound $\sum (r_i - 1)$. Sites that are not informative always fit, so they raise such an index, and some versions leave them out.
- **Not for likelihood.** For [maximum likelihood](/maximum-likelihood-phylogeny/), constant sites and singleton sites still carry information about the branch lengths and the rates. They must not be removed from such an analysis.
- **Four-taxon signal.** On four taxa, parsimony picks the split of most informative sites, which is the start of the analysis of [long-branch attraction](/long-branch-attraction/).

## References
