---
tag: 7P7E2R
kind: algorithm
slug: allen-constraint-propagation
name: Allen's constraint propagation
aliases:
- Allen's propagation algorithm
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Allen's incremental method for interval networks. Each new constraint is intersected into its label and pushed through the 13 by 13 table until no label changes.
model: word-ram
complexity:
  vars: {n: the number of intervals, a: the number of added constraints}
  time: {worst: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, exact: false, in_place: true, online: true, recursive: false}
history:
  year: 1983
  people: [James F. Allen]
  note: Allen introduced the interval algebra together with this propagation procedure, which keeps a network of interval relations path consistent as new facts arrive.
prereqs: [allens-interval-algebra, algebraic-closure]
see_also: [composition-table, path-consistency, pc-2, ord-horn-subclass, nebel-burckert-theorem, interval-algebra-np-completeness, point-algebra-consistency]
sources:
  - paper: doi:10.1145/182.358434
    title: James F. Allen, Maintaining knowledge about temporal intervals, Communications of the ACM 26(11), 1983
    locator: pages 832 to 843 (the 13 relations, the transitivity table and the propagation procedure with its queue of changed pairs)
  - paper: "Marc Vilain and Henry Kautz, Constraint propagation algorithms for temporal reasoning, Proceedings of AAAI-86, 1986, pages 377 to 382"
    locator: the propagation is polynomial and incomplete; consistency of interval networks is NP-hard
  - paper: doi:10.1145/200836.200848
    title: Bernhard Nebel and Hans-Jürgen Bürckert, Reasoning about temporal relations, a maximal tractable subclass of Allen's interval algebra, Journal of the ACM 42(1), 1995
    locator: pages 43 to 66 (path consistency decides consistency of ORD-Horn networks)
  - paper: doi:10.1613/jair.232
    title: Peter van Beek and Dennis W. Manchak, The design and experimental analysis of algorithms for temporal reasoning, Journal of Artificial Intelligence Research 4, 1996
    locator: pages 1 to 18 (efficient path consistency for interval networks and backtracking search on top of it)
  - paper: doi:10.1145/3038927
    title: Frank Dylla and others, A survey of qualitative spatial and temporal calculi, algebraic and computational properties, ACM Computing Surveys 50(1), 2017
    locator: pages 1 to 39 (algebraic closure and its role in qualitative calculi)
---

Allen's constraint propagation keeps a network of interval relations up to date while new facts arrive. Each pair of intervals carries a label, a set of the 13 relations of [Allen's interval algebra](/allens-interval-algebra/). When a new constraint arrives, the algorithm intersects it into the label, and every label that gets smaller is pushed through the [composition table](/composition-table/) to the other intervals, until no label changes. The method is the incremental, interval-specific form of [algebraic closure](/algebraic-closure/): algebraic closure takes a whole network of any qualitative calculus at once, while this page handles one constraint at a time on a network that is already closed, which gives a total cost of $O(n^3 + a)$ for $a$ additions. Like [path consistency](/path-consistency/) in general CSPs, it is fast but incomplete: it finds every contradiction that shows up in three intervals, not every contradiction.

## In plain words

Think of a calendar where you only know how events relate: the talk is during the conference, the dinner is after the talk. Each pair of events has a list of the orders that are still possible. When you learn a new fact, you cross out the orders on that pair's list that it rules out. Then you look at every third event: what you now know about the first pair, plus what you know about the second, may cross out more of the third pair's list. Each list that got shorter is checked again in the same way. If a list loses all its entries, the facts contradict each other.

## The problem

The input is a stream of constraints $i \mathrel{S} j$ on $n$ intervals, where $S$ is a set of base relations. The algorithm keeps a matrix of labels $R_{ij}$, with $R_{ii} = \{\mathrm{eq}\}$ and $R_{ji}$ the converse of $R_{ij}$, and keeps it *closed*: $R_{ik} \subseteq R_{ij} \circ R_{jk}$ for all distinct $i, j, k$, where $\circ$ is the composition of the [composition table](/composition-table/). After each addition it reports a contradiction or a closed network that has the same solutions as all the constraints so far. The cost is counted in label operations on a word-RAM; a label is a 13-bit mask, and one composition is a constant number of table look-ups.

## The algorithm

```pseudo id=main
ADD(R, i, j, S)                       ▷ R is closed before the call
L1  T ← R[i][j] ∩ S
L2  if T = ∅ then return CONTRADICTION
L3  if T = R[i][j] then return OK     ▷ nothing new
L4  R[i][j] ← T; R[j][i] ← conv T; Q ← a queue that holds {i, j}
L5  while Q is not empty do
L6      {p, q} ← pop the front of Q
L7      for each interval k ∉ {p, q} do
L8          T ← R[p][k] ∩ (R[p][q] ∘ R[q][k])
L9          if T = ∅ then return CONTRADICTION
L10         if T ≠ R[p][k] then R[p][k] ← T; R[k][p] ← conv T; push {p, k} on Q unless it is there
L11         T ← R[k][q] ∩ (R[k][p] ∘ R[p][q])
L12         if T = ∅ then return CONTRADICTION
L13         if T ≠ R[k][q] then R[k][q] ← T; R[q][k] ← conv T; push {k, q} on Q unless it is there
L14 return OK
```

The network starts with the universal label on every pair, which is closed. Line L8 uses the popped pair as the first step of a two-step path from $p$ to $k$, and line L11 uses it as the second step of a path from $k$ to $q$. The two other triples that contain the popped pair follow from these by the converse rule of the table, so two revisions per third interval are enough.

## Example

Take four intervals: a talk 0, a conference 1, a dinner 2 and a party 3. All labels start universal.

| call | what changes | pops |
|---|---|---|
| ADD(0, 1, {d}) | $R_{01} = \{\mathrm{d}\}$; no third interval has a label to combine with | 1 |
| ADD(1, 2, {b}) | $R_{12} = \{\mathrm{b}\}$; popping $\{1, 2\}$ with $k = 0$ gives $R_{02} = \mathrm{d} \circ \mathrm{b} = \{\mathrm{b}\}$, so $\{0, 2\}$ is pushed and popped with no further change | 2 |
| ADD(2, 3, {o, s}) | popping $\{2, 3\}$ gives $R_{13} = \mathrm{b} \circ \{\mathrm{o}, \mathrm{s}\} = \{\mathrm{b}\}$ and $R_{03} = \{\mathrm{b}\}$ | 3 |
| ADD(0, 3, {bi}) | line L1 gives $\{\mathrm{b}\} \cap \{\mathrm{bi}\} = \emptyset$; CONTRADICTION at line L2 | 0 |

The talk must be before the party, because it is during the conference, the conference is before the dinner and the dinner starts no later than the party starts. The algorithm finds this from three-interval steps only, and the last fact is rejected without any search.

## Correctness

Each revision at lines L8 and L11 removes only base relations that no solution can use, because the table is sound: if $x \mathrel{r} y$ and $y \mathrel{s} z$ then $x \mathrel{(r \circ s)} z$. So no solution is lost, and an empty label proves a contradiction. The queue holds every pair whose label shrank and whose triples have not been revised since. When the queue is empty, no triple can shrink a label, so the network is closed. A closed network can still have no solution: the tests of this page contain a closed network on 4 intervals with no solution. For networks whose labels are in the [ORD-Horn subclass](/ord-horn-subclass/), a closed network with no empty label always has a solution, by the [Nebel-Bürckert theorem](/nebel-burckert-theorem/). The full proof is in the proof file of this page.

## Complexity

**Time.** A label is a set of at most 13 base relations and every change removes at least one, so each of the $\binom{n}{2}$ labels shrinks at most 12 times over the whole life of the network. A pair enters the queue only after it shrinks, so the total number of pops is at most $12 \binom{n}{2}$, and each pop costs $O(n)$ revisions. Over $a$ calls the total is $O(n^3 + a)$. A single call can do all of this work, so the worst case of one call is $O(n^3)$.

**Space.** The matrix takes $O(n^2)$ labels, and the queue holds at most $\binom{n}{2}$ pairs.

Deciding consistency of a general interval network is NP-complete ([NP-completeness of the interval algebra](/interval-algebra-np-completeness/)), so no polynomial propagation can be complete for all networks unless P = NP.

## Properties

- **Sound.** It removes only base relations that no solution uses, and it reports a contradiction only when there is none.
- **Incomplete.** It decides consistency for some subclasses, such as ORD-Horn and the pointisable relations, but not for all networks.
- **Online.** It accepts constraints one at a time, and the total cost over all additions is the cost of one batch closure.
- **Order does not matter.** The final network is the largest closed network inside the constraints, whatever the order of the additions and of the queue.
- **No undo.** After a contradiction the labels are not meaningful. A search that adds and retracts constraints must save and restore the matrix.

## Variants and improvements

- **Batch closure.** [Algebraic closure](/algebraic-closure/) starts with all pairs in the queue and works for any calculus with a composition table; [PC-2](/pc-2/) is the same queue idea for general binary CSPs.
- **Search.** Backtracking over the base relations of each label, with this propagation at each node, decides consistency. Nebel (1997) makes this faster by splitting labels into ORD-Horn pieces instead of single base relations, because propagation is complete on the pieces.
- **Queue order.** Van Beek and Manchak (1996) compare orders of the queue and other changes to the propagation loop, and report large gains in practice.
- **Points instead of intervals.** If every label is pointisable, translate to endpoints and use the [point algebra consistency algorithm](/point-algebra-consistency/), which is exact and faster.

## When to use it

Use it to maintain a set of qualitative facts about intervals while they arrive, for example in planning, scheduling with unknown durations, or story understanding, where each new fact should give its consequences at once. It is the standard filter inside a search for interval networks. Do not use it alone as a consistency test for arbitrary labels: it can accept a network with no solution.

## Pitfalls

- **Writing one direction.** Lines L4, L10 and L13 must write the converse into the opposite cell. Otherwise a later revision reads an old label and the network is not closed.
- **Revising only one side.** Line L11 is needed as well as line L8. With only line L8, triples where the popped pair is the second step are never revised.
- **Pushing without a change.** Lines L10 and L13 push a pair only when its label got smaller. Pushing on every revision makes the loop run forever on a closed network.
- **Skipping the early exit.** Line L3 makes a repeated or weaker constraint cost $O(1)$. Without it, every call costs at least one pop of $O(n)$.
- **Trusting OK.** Line L14 means "closed", not "consistent". Treat OK as a proof of consistency only for tractable subclasses.

## Implementations

## History

Allen (1983) introduced the 13 interval relations, their transitivity table and this propagation procedure. Vilain and Kautz (1986) showed that consistency of interval networks is NP-hard, so the procedure must be incomplete unless P = NP. Ladkin and Maddux (1994) placed it in the theory of relation algebras, where it is the computation of the algebraic closure. Nebel and Bürckert (1995) proved that it decides consistency for the ORD-Horn subclass, and van Beek and Manchak (1996) studied fast versions of it inside search.

## References
