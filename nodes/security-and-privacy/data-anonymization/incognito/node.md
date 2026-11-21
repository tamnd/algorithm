---
tag: KC05HR
kind: algorithm
slug: incognito
name: Incognito
aliases:
- Incognito algorithm
area: security-and-privacy/data-anonymization
level: core
summary: "Finds all k-anonymous full-domain generalizations, and the minimal ones, by a bottom-up search over growing subsets of attributes, as in a priori."
model: word-ram
complexity:
  vars: {n: the number of rows, d: the number of quasi-identifier attributes, g: the number of vectors of the full lattice}
  time: {worst: O(2^d g n d)}
  space: {extra: O(2^d g n)}
history:
  year: 2005
  people: [Kristen LeFevre, David J. DeWitt, Raghu Ramakrishnan]
  note: "LeFevre, DeWitt and Ramakrishnan gave Incognito at SIGMOD 2005, with the subset property and roll-up from data cube computation."
prereqs: [generalization-and-suppression, breadth-first-search]
see_also: [samarati-algorithm, datafly, mondrian-anonymization, k-anonymity, data-cube, priority-queue, l-diversity, join-semilattice]
sources:
  - paper: doi:10.1145/1066157.1066164
    title: "Kristen LeFevre, David J. DeWitt and Raghu Ramakrishnan, Incognito, efficient full-domain k-anonymity, Proceedings of ACM SIGMOD 2005"
    locator: "pp. 49 to 60, the generalization, rollup and subset properties, the basic Incognito algorithm, and the super-roots and cube variants"
  - url: "https://spdp.di.unimi.it/papers/k-Anonymity.pdf"
    title: "Valentina Ciriani, Sabrina De Capitani di Vimercati, Sara Foresti and Pierangela Samarati, k-Anonymity, in Secure Data Management in Decentralized Systems, Springer, Advances in Information Security, 2007"
    locator: "Section 4.3, the algorithm Incognito with a worked example on race, sex and marital status"
  - paper: doi:10.1109/69.971193
    title: "Pierangela Samarati, Protecting respondents' identities in microdata release, IEEE Transactions on Knowledge and Data Engineering 13(6), 2001"
    locator: "pp. 1010 to 1027, the lattice of generalization vectors and minimal generalization"
  - paper: doi:10.1145/1217299.1217302
    title: "Ashwin Machanavajjhala, Daniel Kifer, Johannes Gehrke and Muthuramakrishnan Venkitasubramaniam, l-diversity, privacy beyond k-anonymity, ACM Transactions on Knowledge Discovery from Data 1(1), 2007"
    locator: the use of the Incognito search with the l-diversity test in place of the k-anonymity test
---

Incognito finds every full-domain generalization vector that makes a table [k-anonymous](/k-anonymity/), and marks the minimal ones. It uses two facts. If a table is k-anonymous on a set of attributes, it is k-anonymous on each subset of it. And if a vector is k-anonymous, each vector above it is too. So Incognito first finds the k-anonymous vectors of single attributes, then of pairs, then of triples, and builds the candidates of each size only from the survivors of the size below, as the a priori algorithm does for frequent item sets. Inside each lattice it goes up by height and does not check a node that already has a k-anonymous node below it.

## In plain words

First look at each attribute alone. For race, find the levels of detail at which every race value appears at least $k$ times. Do the same for sex and for marital status. A level that fails alone also fails with other attributes, so drop it.

Then look at pairs of attributes, but only with the levels that survived alone. Then at triples, built only from the pairs that survived. In each step, start with the most detailed choices. If a choice works, each coarser choice works too, so mark them as good without checking. If a choice fails, try the choices one step coarser.

Counting can also be saved: the counts at a coarser level come from adding up the counts at the finer level, without reading the table again.

## The problem

The input is a table $T$ of $n$ rows with $d$ quasi-identifier attributes, a tree hierarchy for each attribute $a$ with levels $0, \ldots, h_a$, and an integer $k \ge 1$. A *node* is a set $A$ of attributes with a level for each of them. It is k-anonymous if the projection of $T$ on $A$, generalized to these levels, has no tuple that occurs fewer than $k$ times. The output is the set of all k-anonymous vectors over the $d$ attributes, and the subset of them that have no k-anonymous vector strictly below. The full lattice has $g = \prod_a (h_a + 1)$ vectors. The value of $k$ is a policy choice.

## The algorithm

```pseudo id=main
INCOGNITO(T, H, k)
L1  C ← all nodes of one attribute, with each level of its hierarchy
L2  for i ← 1 to d do
L3      S ← C
L4      put the roots of C (nodes with no direct specialization in C) in a queue Q ordered by height
L5      while Q is not empty do
L6          node ← the node of least height in Q, removed from Q
L7          if node is marked then continue at L5
L8          F ← the frequency set of node: counted from T if node is a root, else rolled up from its parent's set
L9          if each count in F is at least k then
L10             mark each direct generalization of node
L11         else remove node from S
L12             put each direct generalization of node in C into Q, with node as its parent, unless it is in Q already
L13     if i < d then C ← the nodes of i + 1 attributes made by joining two nodes of S that agree on all but their last attribute, kept only if each of their subsets of i attributes is in S
L14 all ← S
L15 minimal ← the vectors of all with no direct specialization in all
L16 return (all, minimal)
```

A direct generalization raises one level by one, and a direct specialization lowers one level by one. The frequency set of a node is the count of each tuple of the generalized projection. Line L8 rolls up the set of the parent by mapping each value of one attribute to its parent value in the hierarchy and adding the counts, which is correct because the hierarchy is a tree. The priority queue of line L4 is a [priority queue](/priority-queue/) on the height, so the search inside one lattice goes up level by level, like a [breadth-first search](/breadth-first-search/) from the roots.

## Example

Take the 9 rows of Ciriani et al. (2007) with race (R0 value, R1 person), sex (S0 value, S1 \*) and marital status (M0 value, M1 been married or never married, M2 \*): asian F divorced twice, asian F married, asian M married twice, black F single twice, white F single, and white F widow. Let $k = 2$. Incognito does 11 checks.

| round | node checked | from | smallest count | result |
|---|---|---|---|---|
| 1 | R0 | table | 2 | anonymous, mark R1 |
| 1 | S0 | table | 2 | anonymous, mark S1 |
| 1 | M0 | table | 1 (widow) | remove, queue M1 |
| 1 | M1 | roll-up of M0 | 3 | anonymous, mark M2 |
| 2 | (R0, S0) | table | 2 | anonymous |
| 2 | (R0, M1) | table | 1 (white, been married) | remove, queue (R1, M1) and (R0, M2) |
| 2 | (S0, M1) | table | 2 | anonymous |
| 2 | (R0, M2) | roll-up | 2 | anonymous |
| 2 | (R1, M1) | roll-up | 3 | anonymous |
| 3 | (R0, S0, M2) | table | 2 | anonymous |
| 3 | (R1, S0, M1) | table | 2 | anonymous |

Round 1 drops only M0, so the pairs of round 2 use M1 and M2. In round 2, (R0, M1) is a root of the race and marital lattice, because its specialization (R0, M0) was pruned. Round 3 gets 6 candidates from the join of line L13. The two roots are k-anonymous, and they mark the other 4, which are never checked. The answer is the 6 vectors (0, 0, 2), (0, 1, 2), (1, 0, 1), (1, 0, 2), (1, 1, 1) and (1, 1, 2), and the minimal ones are (0, 0, 2) and (1, 0, 1).

## Correctness

Two properties of k-anonymity carry the proof. Generalization: a node above a k-anonymous node is k-anonymous, because its classes are unions of classes. Subset: a k-anonymous node gives k-anonymous nodes on each subset of its attributes, for the same reason. Inside one round, a node leaves $S$ only after a check that fails, so no anonymous node is lost. By induction on the height, each node of $C$ that is not anonymous is checked: either it is a root and line L4 queues it, or each of its direct specializations in $C$ fails, and line L12 queues it. It is never marked, because no node below it is anonymous. So after the round $S$ is exactly the anonymous nodes of $C$. By the subset property, the join of line L13 keeps every anonymous node of the next size. After round $d$, $S$ is the set of all k-anonymous vectors, and a vector is minimal exactly when no direct specialization is in $S$. The full proof is in proofs/correctness.md.

## Complexity

Let $n$ be the number of rows, $d$ the number of attributes and $g$ the number of vectors of the full lattice. The model is the [word RAM](/word-ram/) with hashing.

- A node is a subset of the attributes with a vector of levels on it. There are at most $2^d g$ nodes, because each subset lattice has at most $g$ vectors.
- Each check costs $O(n d)$ expected time, from the table or by a roll-up of a frequency set of at most $n$ entries.
- In total $O(2^d g n d)$ expected time in the worst case, and $O(2^d g n)$ space for the stored frequency sets.

The worst case is far from typical. The pruning of line L13 and the marks of line L10 skip most nodes in practice, and LeFevre et al. (2005) measured Incognito as much faster than the binary search of Samarati on their data sets. That is a measurement on those data sets, not a bound. Any exact search for all k-anonymous vectors must output them, and there can be about $g$ of them.

## Properties

- **Complete.** It returns every k-anonymous vector, so a user can choose one by any measure of loss afterwards.
- **No suppression in the basic form.** A limit on suppressed rows can be added to the test of line L9 as in Samarati's algorithm. Both properties still hold, because the rows in classes of fewer than $k$ rows can only become fewer on a subset of the attributes or at higher levels.
- **Any monotone test.** The search is correct for each test that has the generalization and subset properties, such as the forms of l-diversity that Machanavajjhala et al. (2007) show to be monotone.
- **Deterministic.** The output does not depend on the order of the queue.

## Variants and improvements

- **Super-roots Incognito.** Compute the frequency set of one node below all roots of a lattice once, and roll up from it, so the table is read fewer times.
- **Cube Incognito.** Compute the frequency sets of the projections on all attribute subsets first, as in a [data cube](/data-cube/), and roll up from them.
- **Samarati's algorithm.** [Samarati's algorithm](/samarati-algorithm/) finds only one vector of least height, by binary search, and needs no per-subset lattices.
- **Greedy and multidimensional.** [Datafly](/datafly/) is faster and not minimal. [Mondrian](/mondrian-anonymization/) leaves full-domain generalization for boxes of values.

## When to use it

Use Incognito when the hierarchies are small, all minimal full-domain generalizations are wanted, and the loss measure is decided later or by a person. It is also the natural search for other monotone tests, such as l-diversity. With many attributes the $2^d$ subsets and the lattice sizes make it slow, and a greedy or multidimensional method is the practical choice.

## Pitfalls

- **Roots of height 0 only in line L4.** A root is a node with no direct specialization in $C$, and after pruning it can have any height. In the example, (R0, M1) is a root. If line L4 queues only nodes of height 0, (R0, M1) is never checked and stays in $S$, so a node that is not anonymous is returned.
- **A roll-up in line L8 with a hierarchy that is not a tree.** If a value has two parents, adding the counts by parent value counts some rows twice or puts them in the wrong class.
- **Treating a marked node as removed in line L7.** A marked node is anonymous and stays in $S$. Removing it loses answers and breaks the join of line L13 for the next round.
- **A join without the subset test in line L13.** The answer stays correct, because each candidate is checked, but the number of candidates grows, and the saving of the a priori idea is lost.

## Implementations

## History

LeFevre, DeWitt and Ramakrishnan presented Incognito at SIGMOD 2005. They took the a priori idea from frequent item set mining and the roll-up and cube ideas from data cube computation, and they showed that full-domain k-anonymity has the generalization, roll-up and subset properties. In the same year Machanavajjhala et al. used the same search for l-diversity. The authors then moved to multidimensional recoding with Mondrian in 2006.

## References
