---
tag: DTG755
kind: algorithm
slug: algebraic-closure
name: Algebraic closure
aliases:
- a-closure
- path consistency for qualitative calculi
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Refines each label of a qualitative network by the composition through every third node until nothing changes, with a queue of changed pairs, in O(n^3) steps.
model: word-ram
complexity:
  vars: {n: the number of nodes, B: the number of base relations of the calculus}
  time: {worst: O(B n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: true, in_place: false, online: false, recursive: false}
history:
  year: 1983
  people: [James F. Allen, Alan K. Mackworth, Gérard Ligozat, Jochen Renz]
  note: Allen (1983) propagated interval constraints through his transitivity table with a queue, after the path consistency algorithms of Mackworth (1977). Ligozat and Renz (2004) named the general operation algebraic closure.
prereqs: [composition-table, qualitative-constraint-network, path-consistency]
see_also: [pc-2, allen-constraint-propagation, point-algebra-consistency, interval-algebra-np-completeness, ord-horn-subclass, qualitative-constraint-calculus, region-connection-calculus-rcc8, constraint-propagation]
sources:
  - paper: doi:10.1007/978-3-540-28633-2_8
    title: Gérard Ligozat and Jochen Renz, What is a qualitative calculus? A general framework, PRICAI 2004, Lecture Notes in Artificial Intelligence 3157, Springer, 2004
    locator: pages 53 to 64 (calculi as non-associative algebras, weak representations, and algebraically closed networks)
  - paper: doi:10.1007/11564751_40
    title: Jochen Renz and Gérard Ligozat, Weak composition for qualitative spatial and temporal reasoning, CP 2005, Lecture Notes in Computer Science 3709, Springer, 2005
    locator: pages 534 to 548 (weak composition, and the cases where algebraic closure and path consistency differ)
  - paper: doi:10.1145/182.358434
    title: James F. Allen, Maintaining knowledge about temporal intervals, Communications of the ACM 26(11), 1983
    locator: pages 832 to 843 (the transitivity table and the propagation of interval constraints with a queue)
  - paper: doi:10.1016/0004-3702(77)90007-8
    title: Alan K. Mackworth, Consistency in networks of relations, Artificial Intelligence 8(1), 1977
    locator: pages 99 to 118 (path consistency and the queue algorithm PC-2)
  - paper: doi:10.1016/b978-1-4832-1447-4.50034-1
    title: Marc Vilain, Henry Kautz and Peter van Beek, Constraint propagation algorithms for temporal reasoning, a revised report, in Readings in Qualitative Reasoning about Physical Systems, Morgan Kaufmann, 1990
    locator: pages 373 to 381 (the propagation algorithm runs in O(n^3) time because each label changes at most 13 times)
  - paper: doi:10.1613/jair.232
    title: Peter van Beek and Dennis W. Manchak, The design and experimental analysis of algorithms for temporal reasoning, Journal of Artificial Intelligence Research 4, 1996
    locator: pages 1 to 18 (queue orders and other engineering choices for path consistency on interval networks, measured)
  - paper: doi:10.1145/3038927
    title: Frank Dylla, Jae Hee Lee, Till Mossakowski, Thomas Schneider, André van Delden, Jasper van de Ven and Diedrich Wolter, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: survey of calculi, weak and strong composition, and when algebraic closure decides consistency
---

Algebraic closure is the basic propagation step for a [qualitative constraint network](/qualitative-constraint-network/). For every three nodes $i$, $k$, $j$ it intersects the label of $(i, j)$ with the composition of the labels of $(i, k)$ and $(k, j)$, read from the [composition table](/composition-table/) of the calculus, and it repeats this until no label changes. It is the same loop as [PC-2](/pc-2/), but it works on the labels as sets of base relations and never looks at the values of the domain, which is infinite. When the composition of the calculus is strong, as in the [point algebra](/point-algebra/) and in [Allen's interval algebra](/allens-interval-algebra/), the result is the [path consistency](/path-consistency/) closure; when it is only weak, as in RCC8, the two differ. This page gives the generic algorithm for any calculus; [Allen's constraint propagation](/allen-constraint-propagation/) is the incremental form for interval networks.

## In plain words

Each pair of objects carries a list of the relations that are still possible between them, for example "a is before b, or a meets b". Look at three objects at a time. If a is before b and b is before c, then a must be before c, so the other entries on the list for a and c can go. A table of all such two-step facts gives, for each pair of entries, the entries that are possible for the third pair.

The algorithm keeps a to-do list of pairs whose list got shorter. It takes a pair off the to-do list, uses it with every third object to shorten other lists, and puts every list that got shorter back on the to-do list. If a list becomes empty, the facts contradict each other. If the to-do list becomes empty, no three objects can shorten any list.

## The problem

A [qualitative constraint calculus](/qualitative-constraint-calculus/) has a finite set $B$ of base relations, an identity base relation $\mathrm{id}$, a converse $a^{\smile}$ for each $a \in B$, and a composition table that gives a relation $a \diamond b \subseteq B$ for each pair of base relations. A relation is a subset of $B$, and composition extends to relations by union: $r \diamond s = \bigcup_{a \in r, b \in s} a \diamond b$.

The input is a network on the nodes $0, \ldots, n-1$ with a label $R_{ij} \subseteq B$ on each pair. A missing constraint has the label $B$. The network is kept complete and symmetric: $R_{ji} = R_{ij}^{\smile}$ and $R_{ii} = \{\mathrm{id}\}$.

The network is *algebraically closed* if $R_{ij} \subseteq R_{ik} \diamond R_{kj}$ for all nodes $i$, $j$, $k$. The output is the largest algebraically closed network $R^\ast$ with $R^\ast_{ij} \subseteq R_{ij}$ for all pairs, or INCONSISTENT if some label of $R^\ast$ is empty. The largest one exists and is unique, because the union of two closed networks is closed.

Cost is counted in compositions and intersections of labels on a word-RAM. A label is a bit mask of $|B|$ bits. A composition of two labels costs at most $|B|^2$ table reads, or one read in a table of all pairs of labels when $2^{|B|}$ is small.

## The algorithm

```pseudo id=main
A-CLOSURE(R)                         ▷ R[i][j] for all i ≠ j, with R[j][i] = conv R[i][j]
L1  if some R[i][j] = ∅ then return INCONSISTENT
L2  Q ← all pairs {i, j} with i < j
L3  while Q ≠ ∅ do
L4      remove a pair {i, j} from Q
L5      for each node k ∉ {i, j} do
L6          T ← R[i][k] ∩ (R[i][j] ⋄ R[j][k])
L7          if T ≠ R[i][k] then
L8              if T = ∅ then return INCONSISTENT
L9              R[i][k] ← T; R[k][i] ← conv T; add {i, k} to Q
L10         T ← R[k][j] ∩ (R[k][i] ⋄ R[i][j])
L11         if T ≠ R[k][j] then
L12             if T = ∅ then return INCONSISTENT
L13             R[k][j] ← T; R[j][k] ← conv T; add {k, j} to Q
L14 return R
```

A pair $\{i, j\}$ in the queue means "the label of this pair changed, so the triangles that read it may now shorten another label". The label of $\{i, j\}$ is read by two kinds of tests: the test of $\{i, k\}$ through $j$ (line L6) and the test of $\{k, j\}$ through $i$ (line L10). The two other orientations of the same triangle give the converse of the same test, because $(r \diamond s)^{\smile} = s^{\smile} \diamond r^{\smile}$, so they are not needed. A pair already in the queue is not added twice. Line L1 handles an input with an empty label, which the loop would not test when $n = 2$.

## Example

Take four intervals in Allen's interval algebra with these constraints: $0 \mathrel{\{b, m\}} 1$, $1 \mathrel{\{b, m\}} 2$, $2 \mathrel{\{d\}} 3$ and $0 \mathrel{\{o, di, bi\}} 3$. The pairs $\{0, 2\}$ and $\{1, 3\}$ start with all 13 base relations. The queue starts as $\{0,1\}, \{0,2\}, \{0,3\}, \{1,2\}, \{1,3\}, \{2,3\}$.

| step | pair removed | label changed | new label | reason |
|---|---|---|---|---|
| 1 | $\{0, 1\}$ | $R_{02}$ | $\{b\}$ | $\{b, m\} \diamond \{b, m\} = \{b\}$ through node 1 |
| 1 | | $R_{13}$ | $\{d, f, oi, mi, bi\}$ | $R_{10} \diamond R_{03}$ through node 0 |
| 2 | $\{0, 2\}$ | $R_{03}$ | $\{o\}$ | $\{b\} \diamond \{d\} = \{b, m, o, s, d\}$ through node 2 |
| 3 | $\{0, 3\}$ | none | | |
| 4 | $\{1, 2\}$ | $R_{13}$ | $\{d\}$ | $\{b, m\} \diamond \{d\} = \{b, m, o, s, d\}$ through node 2 |
| 5, 6 | $\{1, 3\}$, $\{2, 3\}$ | none | | |

The changed pairs of steps 1, 2 and 4 are already in the queue, so nothing is added. After 6 steps the queue is empty. The result says that interval 0 is before interval 2, overlaps interval 3, and that interval 1 lies during interval 3. Here every base relation that is left occurs in some solution, so the result is the minimal network, but this is not true in general.

## Correctness

The invariant is: every label of $R^\ast$ stays inside the current label, and every triangle condition $R_{ij} \subseteq R_{ik} \diamond R_{kj}$ that fails has a side, $\{i, k\}$ or $\{k, j\}$, in the queue. A revision at line L6 or L10 never removes a base relation of $R^\ast$, because $R^\ast$ satisfies the same condition with smaller labels. Removing $\{i, j\}$ from the queue is safe because lines L6 and L10 make all the conditions with the side $\{i, j\}$ hold, and each write puts the written pair in the queue. So an empty queue means a closed network, which is inside $R^\ast$ and contains it. The algorithm does not use the domain: soundness needs only that the table contains every triple of base relations that occurs, which holds for weak composition. The full proof is in the proof file of this page.

## Complexity

**Steps.** A pair goes into the queue only when its label shrinks and stays non-empty. A label has at most $|B|$ base relations, so each of the $\binom{n}{2}$ pairs enters the queue at most $|B|$ times, counting the start. Each removal does $2(n-2)$ compositions and intersections. The total is at most $\binom{n}{2} |B| \cdot 2(n-2) = O(|B| n^3)$ compositions. For a fixed calculus this is $O(n^3)$, the bound of Vilain, Kautz and van Beek for interval networks, with $|B| = 13$.

**Space.** The complete network has $n^2$ labels and the queue has at most $\binom{n}{2}$ pairs, so the extra space is $O(n^2)$ words, plus the table, which has $|B|^2$ entries.

The algorithm decides only closure, not consistency. The problem of consistency for the whole interval algebra is NP-complete ([NP-completeness of interval algebra satisfiability](/interval-algebra-np-completeness/)), so no polynomial closure can decide it unless P = NP.

## Properties

- **Sound.** No base relation that occurs in a solution is removed, for any calculus whose table is sound.
- **Exact closure.** The result is the unique largest algebraically closed subnetwork. It does not depend on the order of the queue.
- **Decides consistency on some classes.** On point algebra networks, on networks whose labels are all [ORD-Horn](/ord-horn-subclass/) relations, and on atomic interval networks (one base relation per pair), a closed network with no empty label is consistent. On RCC8 networks over the tractable class $\hat{H}_8$ the same holds ([tractable subclasses of RCC8](/rcc8-tractable-subclasses/)).
- **Incomplete in general.** The interval network with $0 \mathrel{\{o, si\}} 1$, $0 \mathrel{\{fi, si\}} 2$, $0 \mathrel{\{o, fi\}} 3$, $1 \mathrel{\{m, mi\}} 2$, $1 \mathrel{\{b, f\}} 3$ and $2 \mathrel{\{b, s\}} 3$ is algebraically closed, but it has no solution.
- **Equal to path consistency only for strong composition.** With strong composition, $r \diamond s$ is the exact relational composition over the domain, so a revision removes exactly the pairs of objects that have no witness. With weak composition the table entry can be larger than the real composition, and a closed network need not be path consistent.

## Variants and improvements

- **Allen's incremental form.** Start from a closed network, add one constraint, and put only that pair in the queue. This is [Allen's constraint propagation](/allen-constraint-propagation/). Over a run of $a$ additions the total cost is $O(n^3 + a n)$ compositions.
- **Triangle queue.** Keep triples $(i, k, j)$ in the queue instead of pairs, as [PC-2](/pc-2/) does. This gives the same result with more queue entries.
- **Queue order.** Van Beek and Manchak (1996) measured that the order in which pairs leave the queue changes the running time on interval networks, and they gave heuristics for it. The result does not change.
- **Partial closure.** Close only the triangles of a chordal graph that contains the constraint graph. This keeps the network sparse. It gives the same answer as full closure for some classes, but not in general.
- **Precomputed composition.** For the point algebra ($2^3$ labels) and for Allen ($2^{13}$ labels) one can store $r \diamond s$ for all pairs of labels, or compose bit masks by the union of rows, so each composition costs a few word operations.

## When to use it

Use algebraic closure as the first step on any qualitative network: it finds many contradictions in cubic time and makes the labels smaller. It decides consistency when every label is in a tractable subclass, so a solver can split the labels until they are in such a class and run the closure at each node of the search; for intervals the [Nebel-Bürckert theorem](/nebel-burckert-theorem/) says which class to split into. For a point algebra network alone, the [point algebra consistency algorithm](/point-algebra-consistency/) is faster, $O(n^2)$, and returns a solution. For constraints with metric distances, use the [simple temporal problem](/simple-temporal-problem/) methods instead.

## Pitfalls

- **Revising one direction only.** Line L9 and line L13 must also write the converse label. If $R[k][i]$ keeps its old value, line L10 reads a wrong label and the result is too large.
- **Testing only the target pair.** After $\{i, j\}$ changes, the tests to repeat are those that read $\{i, j\}$ as a side, that is lines L6 and L10 with the third node $k$. Revising $R[i][j]$ again through $k$ does not use the change.
- **Not starting from the complete network.** Line L2 must queue all pairs, including the pairs with the universal label. Otherwise the labels of unconstrained pairs, such as $R_{02}$ in the example, are never derived.
- **Forgetting the empty test.** Without line L8 and line L12 the loop runs on with an empty label and returns a network that looks closed but has no solution.
- **Calling a closed network consistent.** Line L14 returns a closed network, not a proof of consistency. The 4-node network above is closed and has no solution.
- **Using the wrong table for weak calculi.** For RCC8 and other calculi with weak composition, the table must contain every triple that occurs. A table copied from a paper with a typing error makes line L6 unsound. Generate the table from a model where you can, as the implementation here does for points and intervals.

## Implementations

## History

Montanari (1974) and Mackworth (1977) introduced path consistency for networks of binary constraints over finite domains. Allen (1983) applied the same idea to intervals: he replaced the relations over values by unions of his 13 base relations and their composition by a transitivity table, and he propagated each new constraint with a queue. Vilain and Kautz (1986) and the revised report with van Beek (1990) proved the $O(n^3)$ bound, showed that for the point algebra without $\ne$ the propagation finds every consequence, and showed that consistency of interval networks is NP-complete. Ligozat and Renz (2004) gave a general definition of a qualitative calculus and used the name algebraic closure for this operation. Renz and Ligozat (2005) made the difference between weak and strong composition explicit and showed when algebraic closure and path consistency differ.

## References
