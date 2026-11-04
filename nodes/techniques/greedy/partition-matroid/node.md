---
tag: 82BWVQ
kind: concept
slug: partition-matroid
name: Partition matroid
aliases:
- generalized partition matroid
- block-capacity matroid
area: techniques/greedy
level: advanced
summary: A matroid on a ground set split into blocks, where a set is independent if it holds at most a given number of elements from each block.
prereqs: [matroid, uniform-matroid]
see_also: [matroid, uniform-matroid, matroid-intersection, bipartite-matching, matroid-greedy-algorithm, assignment-problem, graphic-matroid, linear-matroid]
sources:
  - book: isbn:9780199603398
    title: James Oxley, Matroid Theory, second edition
    locator: Chapter 1, Basic definitions and examples, and Chapter 4 (direct sums)
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 13, Matroids (matroid intersection, bipartite matching as an example)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Part IV, Matroids and Submodular Functions
---

A partition matroid has a ground set $E$ split into disjoint blocks $E_1, \ldots, E_m$, each with a capacity $k_i$, and a set is independent when it contains at most $k_i$ elements of each block $E_i$. It is the direct sum of the [uniform matroids](/uniform-matroid/) $U_{k_i, |E_i|}$ on the blocks. Its greedy algorithm takes the $k_i$ heaviest elements of each block. Partition matroids are simple on their own, but the common independent sets of two of them are the matchings of a bipartite graph, which makes them a main tool in [matroid intersection](/matroid-intersection/).

## In plain words

The items come in groups, and each group has its own limit. A pick is allowed when no group goes over its limit. For example: choose players for a team with at most one goalkeeper, at most four defenders and at most two from each club. The first two limits together are one partition matroid, by position. The club limit is a second partition matroid, by club.

With one partition matroid, the best pick is easy: in each group, take the most valuable items up to the limit. With two of them at the same time, the problem becomes harder. Matching people to jobs, with each person and each job used at most once, is exactly the case of two partition matroids at the same time.

## The idea

**Definition.** Let $E = E_1 \cup \cdots \cup E_m$ be a partition of a finite set into disjoint blocks, and let $k_1, \ldots, k_m \ge 0$ be integers. The partition matroid has independent sets
$$ \mathcal{I} = \{X \subseteq E : |X \cap E_i| \le k_i \text{ for } i = 1, \ldots, m\}. $$
Some authors reserve the name for the case $k_i = 1$ and call the general case a generalized partition matroid.

**It is a matroid.** (I1) and (I2) hold because the counts $|X \cap E_i|$ only go down for subsets. (I3) Let $X, Y \in \mathcal{I}$ with $|X| < |Y|$. Since $|X| = \sum_i |X \cap E_i|$ and the same for $Y$, some block has $|X \cap E_i| < |Y \cap E_i|$. Pick $y \in (Y \cap E_i) \setminus X$, which exists because $Y \cap E_i$ is larger than $X \cap E_i$. Adding $y$ raises only the count of block $i$, to $|X \cap E_i| + 1 \le |Y \cap E_i| \le k_i$. $\square$

**Rank and bases.** $r(X) = \sum_i \min(|X \cap E_i|, k_i)$. When $k_i \le |E_i|$ for all $i$, the bases take exactly $k_i$ elements from each block, and the rank is $\sum_i k_i$.

**Greedy.** Sorting all elements by weight and adding each one whose block is not full gives a maximum-weight basis, as for any matroid. Here it decomposes: the result is the $k_i$ heaviest elements of each block, which can be found block by block with [selection](/selection-problem/) in $O(|E|)$ time in total.

**Two partition matroids.** Let $G$ be a bipartite graph with sides $L$ and $R$ and edge set $E$. Partition $E$ by the left endpoint, with capacity 1 for each block, and also by the right endpoint, with capacity 1. A set of edges is independent in both matroids exactly when no two of its edges share a vertex, that is, when it is a matching. So [bipartite matching](/bipartite-matching/) and the [assignment problem](/assignment-problem/) are [matroid intersection](/matroid-intersection/) problems. The common independent sets do not form a matroid, and the plain greedy algorithm does not solve them.

## Examples

**A team.** Players in three blocks: goalkeepers $\{a, b, c\}$ with values $9, 7, 4$ and capacity 1, defenders $\{d, e, f\}$ with values $8, 6, 5$ and capacity 2, forwards $\{g, h\}$ with values $3, 2$ and capacity 1. Greedy by value takes $a$ (9), $d$ (8), skips $b$ (7, goalkeeper block full), takes $e$ (6), skips $f$ (5, defender block full), skips $c$ (4), takes $g$ (3), and skips $h$. The team $\{a, d, e, g\}$ has value 26, the best possible.

**Exchange.** With the same blocks, $X = \{a, d\}$ and $Y = \{b, e, f, g\}$ are independent and $|X| < |Y|$. The defender block has $|X \cap E_2| = 1 < 2 = |Y \cap E_2|$, so $X$ can take $e$ or $f$. The goalkeeper $b$ cannot be added, because that block is full in $X$.

**Matchings as an intersection.** Take the path $u_1 - v_1 - u_2 - v_2$ as a bipartite graph with left side $\{u_1, u_2\}$ and right side $\{v_1, v_2\}$, and edge weights $w(u_1 v_1) = 2$, $w(u_2 v_1) = 3$, $w(u_2 v_2) = 2$. Each of the two matroids alone limits only one side: the left matroid allows $\{u_1 v_1, u_2 v_1\}$, and the right matroid allows $\{u_2 v_1, u_2 v_2\}$. Greedy for the intersection would take $u_2 v_1$ (3) and then be blocked, with weight 3, while the matching $\{u_1 v_1, u_2 v_2\}$ has weight 4. The intersection needs the [matroid intersection algorithm](/matroid-intersection-algorithm/).

**Uniform as a special case.** With one block, $m = 1$, the partition matroid is $U_{k_1, |E|}$.

## Where it is used

- **Constraints of the form "at most $k_i$ per group".** Budgets per category, per region or per time slot. A single such constraint keeps greedy exact.
- **Matching and assignment.** As the intersection of two partition matroids, see above. Many scheduling and assignment problems combine a partition matroid with a [graphic](/graphic-matroid/) or [linear matroid](/linear-matroid/) to stay within matroid intersection.
- **Submodular maximization with group constraints.** Allocating items to agents, where each item goes to at most one agent, is a partition matroid constraint on the pairs (item, agent).

## References
