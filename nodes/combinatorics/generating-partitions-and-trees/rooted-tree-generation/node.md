---
tag: YQ0M7Y
kind: problem
slug: rooted-tree-generation
name: Rooted unlabeled tree generation
aliases:
- Generating rooted trees
- Unlabeled rooted tree enumeration
- Listing rooted trees up to isomorphism
area: combinatorics/generating-partitions-and-trees
level: advanced
summary: Enumerate all non-isomorphic rooted trees with n nodes.
model: word-ram
complexity:
  vars: {n: the number of nodes, N: the number of unlabeled rooted trees with n nodes}
  time: {worst: Θ(n + N)}
prereqs: [rooted-tree, level-sequence, tree-isomorphism]
see_also: [beyer-hedetniemi, level-sequence, free-tree-generation, ordered-tree-generation, labeled-tree-generation, tree-isomorphism, constant-amortized-time-generation, orderly-generation]
sources:
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 4.6.2, Rooted Trees, Free Trees (recurrence (4.27), the table of a_n, Algorithm 4.18, Lemma 4.5 and Theorem 4.2 of Kubicka), and Section 2.10.2, Rooted Trees (the asymptotic form of a_n)
  - paper: doi:10.1137/0209055
    title: Terry Beyer and Sandra Mitchell Hedetniemi, Constant time generation of rooted trees, SIAM Journal on Computing 9(4) (1980), 706 to 712
    locator: the whole paper
  - url: https://oeis.org/A000081
    title: OEIS A000081, Number of unlabeled rooted trees with n nodes
    locator: the terms, Otter's recurrence and the asymptotic constants
---

Rooted tree generation is the problem of listing every unlabeled rooted tree with $n$ nodes exactly once, where two trees are the same when a reordering of children turns one into the other. There are $a_n$ of them, $1, 1, 2, 4, 9, 20, 48, \ldots$, and $a_n$ grows like $2.9558^n / n^{3/2}$. The standard solution codes each tree by its canonical [level sequence](/level-sequence/) and steps through these sequences in decreasing lexicographic order with the [Beyer-Hedetniemi algorithm](/beyer-hedetniemi/), in constant amortized time per tree.

## In plain words

A rooted tree has a top node, and every other node hangs below a parent. The children of a node have no order, so two drawings that differ only by swapping branches are the same tree. You want each different tree once.

The trick is to choose one standard drawing for each tree: at every node, put the "largest" branch first. Then write the depth of each node as you walk the drawing from left to right. Each tree gets one list of numbers, and the lists are easy to step through from the largest to the smallest. Each step changes only the end of the list, so the work per tree is small.

## Definition

A *rooted tree* is a tree with one node chosen as the root. Two rooted trees are *isomorphic* if there is a bijection between their nodes that maps root to root and keeps the parent relation. Let $\mathcal{R}_n$ be the set of isomorphism classes of rooted trees with $n$ nodes, and $a_n = |\mathcal{R}_n|$.

**Input:** an integer $n \ge 1$.

**Output:** a sequence that contains one representative of each class in $\mathcal{R}_n$ exactly once, usually as a canonical level sequence or as a parent array.

**Cost model.** The [word RAM](/word-ram/). The trees are visited in place: the generator keeps one sequence and changes it, and the time counts the changes. Copying each tree out costs $\Theta(n)$ per tree, and is not counted.

## Variants

- **Code.** The canonical [level sequence](/level-sequence/), the parent array of the canonical ordering, or a nested bracket word.
- **Order.** Decreasing lexicographic order of the canonical level sequences, which is the order of the Beyer-Hedetniemi algorithm; or orders in which consecutive trees differ by moving one subtree.
- **Rooted forests.** Removing the root of a rooted tree with $n + 1$ nodes gives a rooted forest with $n$ nodes, and every forest arises once. So there are $a_{n+1}$ forests with $n$ nodes, and the same generator lists them.
- **Restricted trees.** Trees with bounded height, with bounded out-degree, or with a given number of leaves. A filter on the output of the general generator solves them, but each restriction needs its own successor rule and analysis to keep the cost per tree constant.
- **Ordered and labeled trees.** If the children are ordered, the problem is [ordered tree generation](/ordered-tree-generation/), with $C_{n-1}$ trees. If the nodes carry labels $1, \ldots, n$, there are $n^{n-1}$ rooted trees; see [labeled tree generation](/labeled-tree-generation/).
- **Counting only.** Computing $a_n$ does not need generation; Otter's recurrence or the partition formula below give it in polynomial time.

## Examples

For $n = 4$ the four trees are the path, the root with one child that has two children, the root with a child that has one child plus a leaf, and the star. Their canonical level sequences are $0123$, $0122$, $0121$ and $0111$. For $n = 5$ there are nine: $01234$, $01233$, $01232$, $01231$, $01222$, $01221$, $01212$, $01211$, $01111$.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $a_n$ | 1 | 1 | 2 | 4 | 9 | 20 | 48 | 115 | 286 | 719 | 1842 | 4766 | 12486 | 32973 | 87811 |

The numbers satisfy Otter's recurrence $n\, a_{n+1} = \sum_{k=1}^{n} \big(\sum_{d \mid k} d\, a_d\big) a_{n-k+1}$, and also a sum over integer partitions of $n - 1$: if the root has $j_i$ subtrees with $i$ nodes, then
$$a_n = \sum_{j_1 + 2j_2 + \cdots = n - 1}\ \prod_{i \ge 1} \binom{a_i + j_i - 1}{j_i}.$$

## Known algorithms

| method | order | total time | worst step |
|---|---|---|---|
| all $C_{n-1}$ ordered trees, keep the canonical ones ([generate and test](/generate-and-test/)) | any | $\Theta(n C_{n-1})$ | $O(n)$ |
| recursion over the partition formula | by root degree | output-sensitive, but complex | polynomial |
| [Beyer-Hedetniemi](/beyer-hedetniemi/) successor on canonical level sequences | decreasing lexicographic | $\Theta(n + a_n)$ | $O(n)$ |
| [orderly generation](/orderly-generation/) or [canonical augmentation](/canonical-augmentation/) by adding leaves | by construction | polynomial per tree | polynomial |

- **Generate and test.** Listing all ordered trees and keeping those with sorted children is simple, but the ratio $C_{n-1}/a_n$ grows exponentially: it is $6.8$ for $n = 10$ and $30.5$ for $n = 15$.
- **Beyer-Hedetniemi.** Take the last entry of the sequence that is larger than $1$, make that node a sibling of its parent, and fill the rest of the sequence with copies of the parent's subtree. With a parent array, each step costs $O(1)$ plus the number of entries written, and the total over all trees is $O(a_n)$. Ruskey's book gives the proof, and Kubicka showed that the average number of entries rewritten tends to $1/(1 - \rho) \approx 1.511$, where $\rho \approx 0.3383$ is the radius of convergence of $\sum a_n x^n$.
- **Generic isomorph rejection.** Methods for general graphs also work for trees, with a polynomial cost per tree, but the specialized successor is much faster.

## Bounds

- Every method must visit $a_n$ trees, so $\Omega(a_n)$ time is necessary in the in-place model. The Beyer-Hedetniemi algorithm meets this bound, so the problem is solved in constant amortized time.
- $a_n \sim C\, \rho^{-n} n^{-3/2}$ with $\rho^{-1} \approx 2.9558$ and $C \approx 0.4399$, so listing is practical up to about $n = 24$, where $a_n \approx 7.4 \cdot 10^8$.
- In the full output model, writing each tree costs $\Theta(n)$, and the total is $\Theta(n a_n)$.

## Reductions

- **Forests to trees.** Rooted forests with $n$ nodes are rooted trees with $n + 1$ nodes, by adding or removing a root.
- **Free trees to rooted trees.** A free tree has one or two centers. Rooting it at a center, with a rule for two centers, gives one rooted tree per free tree, and the rooted versions are canonical level sequences with extra conditions. This reduction drives [free tree generation](/free-tree-generation/).
- **Isomorphism to canonical forms.** Two rooted trees are isomorphic if and only if their canonical level sequences are equal. The sequence can be computed in $O(n \log n)$ time by sorting the children codes, or in linear time with the [AHU algorithm](/ahu-algorithm/) idea.

## Applications

- Exhaustive tests of tree algorithms, such as dynamic programs on rooted trees, on every shape of a small size.
- Chemistry: rooted trees model acyclic structures with one marked atom, such as alkyl groups.
- Phylogenetics and data structures: shapes of unlabeled hierarchies.
- As a building block for [free tree generation](/free-tree-generation/) and for the generation of other acyclic structures.

## References
