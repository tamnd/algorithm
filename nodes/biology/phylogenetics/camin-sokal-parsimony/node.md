---
tag: B7AFH8
kind: problem
slug: camin-sokal-parsimony
name: Camin-Sokal parsimony
aliases:
- irreversible parsimony
area: biology/phylogenetics
level: advanced
summary: Parsimony on a rooted tree where each character starts in the ancestral state 0 at the root and can only change forward, never back. Small case is easy, tree search is NP-hard.
prereqs: [small-parsimony, rooted-and-unrooted-trees]
see_also: [dollo-parsimony, wagner-parsimony, sankoff-algorithm, maximum-parsimony, maximum-parsimony-np-hard, perfect-phylogeny, character-compatibility]
sources:
  - paper: doi:10.1111/j.1558-5646.1965.tb01722.x
    title: Joseph H. Camin and Robert R. Sokal, A method for deducing branching sequences in phylogeny, Evolution 19(3), 1965, 311-326
    locator: the method of the least number of steps with irreversible characters and a known ancestral state
  - paper: doi:10.1016/0025-5564(86)90161-6
    title: William H. E. Day, David S. Johnson and David Sankoff, The computational complexity of inferring rooted phylogenies by parsimony, Mathematical Biosciences 81(1), 1986, 33-42
    locator: the NP-completeness of the Camin-Sokal and Dollo versions of parsimony
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 7, Variants of parsimony, the section on Camin-Sokal parsimony
---

Camin-Sokal parsimony is [parsimony](/maximum-parsimony/) with irreversible characters on a rooted tree. Each character has an ancestral state 0 at the root, and along each edge from parent to child it may only change forward, to a higher state. A change back is forbidden. The score of a tree is the least number of forward steps that explain the states at the leaves. Joseph Camin and Robert Sokal proposed it in 1965, in one of the first computer methods for building trees. For a fixed tree the score has a simple form: each node takes the least state among the leaves below it. The search over trees is NP-hard, as Day, Johnson and Sankoff showed in 1986.

## In plain words

Some changes in evolution seem to go one way only. Once a lineage has a new trait, it keeps it. Camin-Sokal parsimony assumes this for every character. All characters start at 0 in the common ancestor at the root, and a lineage can only move from 0 to 1, or from a lower state to a higher one, never back.

So on a given tree, if two sister groups both have state 1 and their common ancestor could have it too, the ancestor should get it, and the gain happens once. If some leaves below an ancestor still have state 0, the ancestor must have state 0, since there is no way back. You count the gains. The best tree is the one with the fewest gains.

## Definition

**Characters.** A character has the states $0, 1, \ldots, k - 1$, where 0 is the ancestral state. A change from state $i$ in a parent to state $j$ in its child costs

$$\delta(i, j) = \begin{cases} j - i & \text{if } j \ge i, \\ \infty & \text{if } j < i. \end{cases}$$

**Small Camin-Sokal parsimony.** Given a rooted tree $T$ and a state $x(\ell)$ at each leaf, find states for the internal nodes, together with an extra ancestor of state 0 above the root, that minimize the sum of $\delta$ over the edges, including the edge from the ancestor to the root.

**Large Camin-Sokal parsimony.** Given $m$ characters on $n$ taxa, find a rooted tree with the least total score.

**The solution of the small problem.** A labeling of finite cost is non-decreasing along every path from the root, so a node can have no state higher than any leaf below it. Write $\mu_v$ for the least leaf state below $v$. The labeling $\lambda(v) = \mu_v$ is optimal. To see this, write its cost as a sum over the nodes: an edge $(p, w)$ adds $\lambda(w) - \lambda(p)$, so

$$\operatorname{cost}(\lambda) = \sum_{\ell \text{ leaf}} x(\ell) - \sum_{v \text{ internal}} (d_v - 1)\, \lambda(v),$$

where $d_v$ is the number of children of $v$ and the ancestor above the root has state 0. Each internal node with $d_v \ge 2$ has a negative coefficient, so the cost is least when every $\lambda(v)$ is as high as allowed, which is $\mu_v$. A node with one child has coefficient 0, and $\mu_v$ is as good as any other allowed state for it.

**Binary characters.** For two states, the score is the number of maximal clades whose leaves all have state 1: each such clade gets one gain on the edge above it, and no clade with a leaf of state 0 can have a gain above it, because that leaf would need a change back.

## Variants

- **Wagner parsimony.** The same ordered costs without the ban on changes back: [Wagner parsimony](/wagner-parsimony/). Its tree may be unrooted.
- **Dollo parsimony.** The opposite kind of asymmetry: a derived state arises only once, and it can be lost many times. See [Dollo parsimony](/dollo-parsimony/).
- **Unknown ancestral state.** If the ancestral state of a character is not known, it can be treated as a free state of the root, which turns the cost into a choice of the best direction for each character.
- **Character-state trees.** States can be in a tree-shaped order with 0 at its root, and a change goes only away from 0. The [Sankoff algorithm](/sankoff-algorithm/) handles this with $\delta = \infty$ for the forbidden changes.
- **Weighted characters.** Each character can have a weight, which multiplies its score.

## Examples

**Six taxa, three binary characters.** Take the rooted tree $(((L_1, L_2), L_3), ((L_4, L_5), L_6))$, with an ancestor of state 0 above the root. The table compares the score of three characters under three models. Fitch is the unit cost with a free root state, and Dollo allows one gain only.

| character on $L_1, \ldots, L_6$ | Fitch | Fitch, root 0 | Camin-Sokal | [Dollo](/dollo-parsimony/) |
|---|---|---|---|---|
| 1 1 0 1 0 0 | 2 | 2 | 2 | 4 |
| 0 0 1 1 1 1 | 1 | 2 | 2 | 2 |
| 0 1 1 0 1 1 | 2 | 3 | 4 | 3 |

For the first character, the maximal clades with only state 1 are $(L_1, L_2)$ and $L_4$, so Camin-Sokal needs two gains. For the third character, no clade of two or more leaves has only state 1, so each of $L_2$, $L_3$, $L_5$ and $L_6$ needs its own gain: 4. Fitch parsimony explains the same character with 2 changes: the root and all internal nodes have state 1, and state 0 arises on the edges to $L_1$ and $L_4$. Here the ban on changes back costs 2 extra steps.

**An ordered character.** On the tree $((t_1, t_2), (t_3, (t_4, t_5)))$ with the states 0, 2, 3, 1, 3, the least leaf states below the internal nodes are 0 for $(t_1, t_2)$, 1 for $(t_4, t_5)$, 1 for $(t_3, (t_4, t_5))$ and 0 at the root. The formula gives $(0 + 2 + 3 + 1 + 3) - (0 + 1 + 1 + 0) = 7$ steps. The same character costs 5 under [Wagner parsimony](/wagner-parsimony/), where changes back are allowed.

## Known algorithms

- **Small problem.** The rule $\lambda(v) = \mu_v$ takes one [postorder](/postorder-traversal/) pass, $O(n)$ time per character. The [Sankoff algorithm](/sankoff-algorithm/) with the table $\delta$ above and the root fixed to follow state 0 gives the same result in $O(nk^2)$ time.
- **Large problem.** Exact search by branch and bound over rooted trees, or the heuristics of [maximum parsimony](/maximum-parsimony/), with the score above.
- **Compatible characters.** If every binary character can be explained by one gain on a common rooted tree, the characters form a rooted [perfect phylogeny](/perfect-phylogeny/), which is found in polynomial time and is then the best Camin-Sokal tree.

## Bounds

- **NP-hard.** Large Camin-Sokal parsimony is NP-complete, also for binary characters (Day, Johnson and Sankoff 1986). The vertex cover instance of [the NP-hardness of maximum parsimony](/maximum-parsimony-np-hard/) also works here: the tree built in its proof is monotone from the zero row, and the Camin-Sokal score of a tree is never below its Fitch score.
- **Lower bound per character.** A character whose largest leaf state is $h$ needs at least $h$ steps, along the path from the root to a leaf of state $h$.
- **Compared with Fitch.** A Camin-Sokal labeling is also a labeling for Fitch parsimony, so the Camin-Sokal score of a binary character is at least its Fitch score with the root fixed to 0, and that is at least its Fitch score with a free root.

## Reductions

- **To weighted parsimony.** The small problem is the [Sankoff algorithm](/sankoff-algorithm/) with an asymmetric table and an infinite cost for changes back.
- **From vertex cover.** As in the bounds above, by the instance of the [maximum parsimony NP-hardness proof](/maximum-parsimony-np-hard/), rooted at the zero row.
- **To compatibility.** For binary characters, a tree has a score equal to the number of characters that are not all 0 exactly when each such character is one clade of the tree, which is the rooted form of [character compatibility](/character-compatibility/).

## Applications

- **Early numerical phylogenetics.** Camin and Sokal used the method on morphological data, where the direction of change can often be argued from an outgroup or from fossils.
- **Irreversible markers.** Some genomic events are rare and hard to undo, such as the insertion of a transposable element at a site. They are close to the Camin-Sokal model.
- **Cell lineages.** In some lineage-tracing experiments with CRISPR, edits accumulate in cells and are not reversed, so they also fit an irreversible model.

## References
