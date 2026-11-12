---
tag: 3PMJC9
kind: problem
slug: wagner-parsimony
name: Wagner parsimony
aliases:
- Wagner's model
area: biology/phylogenetics
level: advanced
summary: Parsimony for ordered characters, whose states are integers and where a change from state i to state j costs the distance between i and j. Changes may go both ways.
prereqs: [small-parsimony, sankoff-algorithm]
see_also: [fitch-algorithm, maximum-parsimony, camin-sokal-parsimony, dollo-parsimony, median, weighted-median, stepwise-addition]
sources:
  - paper: doi:10.2307/2412407
    title: Arnold G. Kluge and James S. Farris, Quantitative phyletics and the evolution of anurans, Systematic Zoology 18(1), 1969, 1-32
    locator: the Wagner method for ordered characters, with the distance between states as the cost of change
  - paper: doi:10.1093/sysbio/19.1.83
    title: James S. Farris, Methods for computing Wagner trees, Systematic Zoology 19(1), 1970, 83-92
    locator: the computation of the states of the internal nodes of a Wagner tree and of its length
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 7, Variants of parsimony, the sections on multiple states and binary coding
---

Wagner parsimony is [parsimony](/maximum-parsimony/) for ordered characters. The states of a character are integers $0, 1, \ldots, k - 1$ in a linear order, such as the number of bones in a fin or a size class, and a change from state $i$ to state $j$ costs $|i - j|$: going from 0 to 2 needs two steps, through state 1. Changes can go up and down, so the cost is symmetric and the root does not matter. Kluge and Farris (1969) introduced the model, and Farris (1970) gave the methods to compute it. The [small parsimony](/small-parsimony/) version has a pass with intervals in place of Fitch's sets that takes $O(n)$ time per character. The search over trees is NP-hard, as for unordered characters.

## In plain words

Some traits come in steps. A leg can be short, medium or long, and to go from short to long it seems natural to pass through medium. Wagner parsimony counts the steps: short to long costs 2, short to medium costs 1.

For a given tree, you guess the ancestors so that the total number of steps is least. The best value for an ancestor is not one number but a range. If the ranges of two children overlap, the ancestor takes a value in the overlap and pays nothing. If they do not, the ancestor takes a value in the gap between them, and the gap is the cost. For the search over trees, the problem is as hard as ordinary parsimony.

## Definition

**Character.** An ordered character has the states $0, 1, \ldots, k - 1$, and the cost of a change from $i$ to $j$ is $\delta(i, j) = |i - j|$. This is a metric. The same definition works for real-valued states.

**Small Wagner parsimony.** Given a tree $T$ and an integer state $x(\ell)$ at each leaf, find integer states for the internal nodes that minimize $\sum_{(u, w) \in E(T)} |\lambda(u) - \lambda(w)|$. The minimum is the Wagner length of the character on $T$.

**Large Wagner parsimony.** Given $m$ ordered characters on $n$ taxa, find an unrooted tree whose total Wagner length is least. Such a tree is a Wagner tree.

**The interval pass.** On a rooted binary tree, give each node $v$ an interval $I_v = [\ell_v, h_v]$ in postorder:

- at a leaf, $I_v = [x(v), x(v)]$;
- at an internal node with children whose intervals are $I_1$ and $I_2$: if they meet, $I_v = I_1 \cap I_2$ and the cost is 0; if not, with $I_1$ to the left of $I_2$, $I_v = [h_1, \ell_2]$, the gap between them, and the cost is its length $\ell_2 - h_1$.

The Wagner length is the sum of the costs. To get the states, give the root any state of $I_{\text{root}}$, and give each child the point of its interval that is closest to the state of its parent.

**Why the pass is right.** Let $c_w(a)$ be the least length of the subtree of $w$ with $w$ in state $a$, and $s_w$ its minimum. The claim is that $c_w(a) \ge s_w + d(a, I_w)$, with equality on $I_w$, where $d(a, I)$ is the distance from $a$ to the interval $I$. Then a parent in state $a$ pays $\min_b (c_w(b) + |a - b|) = s_w + d(a, I_w)$, reached at the point of $I_w$ closest to $a$. At a node with children intervals $I_1$ and $I_2$, this gives $c_v(a) = s_1 + s_2 + d(a, I_1) + d(a, I_2)$. If the intervals meet, the sum of the two distances is 0 exactly on the overlap and grows by at least 1 per unit of distance from it. If not, the sum is at least the gap, by the triangle inequality, with equality exactly on the gap, and it also grows by at least 1 per unit away from the gap. In both cases the claim holds at $v$, with $I_v$ as in the pass.

**Many children.** At a node with $d$ children, $c_v(a) = \text{const} + \sum_j d(a, I_j)$, and $d(a, [\ell, h]) = \tfrac12 (|a - \ell| + |a - h| - (h - \ell))$. So $c_v$ is least at the [medians](/median/) of the $2d$ endpoints $\ell_1, h_1, \ldots, \ell_d, h_d$, and $I_v$ is the interval between the two middle endpoints.

## Variants

- **Unordered characters.** Every change costs 1: [Fitch parsimony](/fitch-algorithm/). For two states, ordered and unordered are the same.
- **Irreversible ordered characters.** Changes only go up from an ancestral state 0: [Camin-Sokal parsimony](/camin-sokal-parsimony/).
- **Single gain.** [Dollo parsimony](/dollo-parsimony/) allows one gain of a derived state and many losses.
- **Real-valued characters.** Measurements, such as a ratio of lengths, with the cost $|a - b|$. The interval pass works without change. With the cost $(a - b)^2$ instead, the problem becomes a least squares fit.
- **Character-state trees.** States in a tree-shaped order, not a line, with the cost the path length in that tree. The [Sankoff algorithm](/sankoff-algorithm/) solves it, and binary coding along the edges of the state tree reduces it to two-state characters.

## Examples

**The interval pass.** Take the tree $((t_1, t_2), (t_3, (t_4, t_5)))$ with the states 0, 2, 3, 1, 3. Let $u = (t_1, t_2)$, $w = (t_4, t_5)$, $v = (t_3, w)$ and $r = (u, v)$.

| node | children's intervals | case | interval | cost |
|---|---|---|---|---|
| $u$ | $[0, 0]$, $[2, 2]$ | gap | $[0, 2]$ | 2 |
| $w$ | $[1, 1]$, $[3, 3]$ | gap | $[1, 3]$ | 2 |
| $v$ | $[3, 3]$, $[1, 3]$ | overlap | $[3, 3]$ | 0 |
| $r$ | $[0, 2]$, $[3, 3]$ | gap | $[2, 3]$ | 1 |

The Wagner length is $2 + 2 + 0 + 1 = 5$. One optimal labeling gives state 2 to $r$, $u$, $v$ and $w$. Its steps are $|2 - 0| = 2$ to $t_1$, $|2 - 3| = 1$ to $t_3$, $|2 - 1| = 1$ to $t_4$ and $|2 - 3| = 1$ to $t_5$, in total 5. A check of all labelings shows that the optimal states are $\{2\}$ at $u$ and $\{2, 3\}$ at $v$, $w$ and $r$. So, as with Fitch's sets, the intervals of the first pass are not the sets of optimal states: $I_v = [3, 3]$ misses 2, and $I_u = [0, 2]$ holds 0 and 1, which are not optimal.

**Ordered and unordered.** With unit costs, the same character costs 3 on this tree. Treating the states as ordered adds the cost of the steps between distant states.

**Binary coding.** The ordered character with states 0 to $k - 1$ is the sum of $k - 1$ binary characters $y_t = [x \ge t]$ for $t = 1, \ldots, k - 1$, since $|i - j| = \sum_t \bigl|[i \ge t] - [j \ge t]\bigr|$. In the example, the three binary characters are 01111, 01101 and 00101 over $t_1, \ldots, t_5$. Their Fitch scores on the tree are 1, 2 and 2, and their sum is the Wagner length 5.

## Known algorithms

| method | tree | time per character |
|---|---|---|
| interval pass (Farris 1970) | rooted binary | $O(n)$ |
| median of endpoints | rooted, any degree | $O(n \log n)$, or $O(n)$ with linear-time selection |
| [Sankoff algorithm](/sankoff-algorithm/) with $\delta(i, j) = \lvert i - j \rvert$ | rooted, any degree | $O(nk^2)$, or $O(nk)$ with two sweeps per edge |
| binary coding with [Fitch's algorithm](/fitch-algorithm/) | rooted binary | $O(nk)$ |

For the search over trees, the methods of [maximum parsimony](/maximum-parsimony/) apply. Farris (1970) built Wagner trees by adding the taxa one at a time at the place of least added length, an early form of [stepwise addition](/stepwise-addition/).

## Bounds

- **Lower bound per character.** On any tree, the path between a leaf of the least state and a leaf of the largest state must cover the range, so the Wagner length is at least $\max_\ell x(\ell) - \min_\ell x(\ell)$.
- **Upper bound per character.** A star with a [median](/median/) of the leaf states at the center costs $\sum_\ell |x(\ell) - \operatorname{med}|$, and every tree costs at most this.
- **Binary coding is exact.** The Wagner length of an ordered character is the sum of the Fitch scores of its $k - 1$ threshold characters. One direction is the sum of the threshold costs of an optimal labeling. For the other, take an optimal labeling $\mu_t$ for each threshold character and let $\lambda(v) = \sum_t \mu_t(v)$. It agrees with $x$ at the leaves, and $|\lambda(u) - \lambda(w)| \le \sum_t |\mu_t(u) - \mu_t(w)|$ on each edge, so its length is at most the sum of the Fitch scores.
- **NP-hard.** Large Wagner parsimony contains the two-state case, which is ordinary parsimony on binary characters, and that is [NP-hard](/maximum-parsimony-np-hard/).

## Reductions

- **To weighted parsimony.** Wagner parsimony is the [Sankoff algorithm](/sankoff-algorithm/) with the table $\delta(i, j) = |i - j|$.
- **To binary parsimony.** By the binary coding above, an ordered character with $k$ states is the same as $k - 1$ two-state characters, so large Wagner parsimony reduces to ordinary parsimony on binary data in polynomial time, and the other way round for $k = 2$.
- **To a Steiner problem.** Large Wagner parsimony is the [Steiner tree problem](/steiner-tree-problem/) for the rows in $\mathbb{Z}^m$ with the $\ell_1$ distance.

## Applications

- **Morphology.** Characters with a natural order of states, such as counts of parts or grades of a structure, are often treated as ordered in cladistic analyses.
- **Measurements.** Real-valued characters, such as ratios of lengths, can be coded as ordered states or analyzed with the interval pass directly.
- **Tree building.** The Wagner tree method of Farris, which adds the taxa one at a time, was one of the first practical algorithms for parsimony trees on many taxa.

## References
