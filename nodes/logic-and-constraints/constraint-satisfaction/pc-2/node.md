---
tag: JNRB9Z
kind: algorithm
slug: pc-2
name: PC-2 algorithm
aliases:
- path consistency algorithm PC-2
- PC2
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Enforces path consistency with a queue of affected variable triples, in O(n^3 d^5) time.
model: word-ram
complexity:
  vars: {n: the number of variables, d: the largest domain size}
  time: {worst: O(n^3 d^5)}
  space: {extra: O(n^3 + n^2 d^2)}
properties: {deterministic: true, exact: true, in_place: true, online: false, recursive: false}
history:
  year: 1977
  people: [Alan K. Mackworth]
  note: Mackworth gave PC-1 and PC-2 in 1977, after the path consistency of Montanari (1974). Mackworth and Freuder proved the O(n^3 d^5) bound for PC-2 in 1985.
prereqs: [path-consistency, ac-3]
see_also: [ac-4, arc-consistency, k-consistency, constraint-propagation, simple-temporal-problem, singleton-arc-consistency]
sources:
  - paper: doi:10.1016/0004-3702(77)90007-8
    title: Alan K. Mackworth, Consistency in networks of relations, Artificial Intelligence 8(1), 1977
    locator: pages 99 to 118 (path consistency, and the algorithms PC-1 and PC-2)
  - paper: doi:10.1016/0004-3702(85)90041-4
    title: Alan K. Mackworth and Eugene C. Freuder, The complexity of some polynomial network consistency algorithms for constraint satisfaction problems, Artificial Intelligence 25(1), 1985
    locator: pages 65 to 74 (the bounds O(n^3 d^5) for PC-2 and O(n^5 d^5) for PC-1)
  - paper: doi:10.1016/0020-0255(74)90008-5
    title: Ugo Montanari, Networks of constraints, fundamental properties and applications to picture processing, Information Sciences 7, 1974
    locator: pages 95 to 132 (path consistency, and the result that paths of length 2 are enough in a complete network)
  - paper: doi:10.1016/0004-3702(86)90083-4
    title: Roger Mohr and Thomas C. Henderson, Arc and path consistency revisited, Artificial Intelligence 28(2), 1986
    locator: pages 225 to 233 (the counter-based path consistency algorithm PC-3)
  - paper: "Ching-Chih Han and Chia-Hoang Lee, Comments on Mohr and Henderson's path consistency algorithm, Artificial Intelligence 36(1), 1988, pages 125 to 130"
    locator: the flaw in PC-3 and the corrected algorithm PC-4, with O(n^3 d^3) time
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 3, Consistency-enforcing algorithms (path consistency, PC-1, PC-2 and their complexity)
  - paper: "Peter Jeavons, David Cohen and Martin C. Cooper, Constraints, consistency and closure, Artificial Intelligence 101(1-2), 1998, pages 251 to 265"
    locator: the theorem that constraints closed under a near-unanimity operation of arity k+1 are solved by strong (k+1)-consistency; the majority case is strong path consistency
---

PC-2 is an algorithm that enforces [path consistency](/path-consistency/) on a binary [constraint satisfaction problem](/constraint-satisfaction-problem/). It keeps a queue of triples of variables, deletes from the relation of each pair the value pairs that cannot be extended to the third variable, and puts back on the queue only the triples whose test reads a relation that changed. It runs in $O(n^3 d^5)$ time in the worst case and returns the unique path consistency closure. It is to path consistency what [AC-3](/ac-3/) is to arc consistency.

## In plain words

Arc consistency asks that each value of one unknown have a partner in each other unknown. Path consistency asks more: each allowed pair of values for two unknowns must have a partner in every third unknown, a value that the rules allow with both. So path consistency deletes pairs, not single values. It can add a new rule between two unknowns that had none, for example "these two must be equal".

PC-2 keeps a to-do list of "pair, third unknown" tasks. For each task it deletes the pairs that have no partner in the third unknown. A deletion from one pair's list can take away the partner of a pair elsewhere, so the tasks that read the changed list go back on the to-do list. At the end it also deletes single values that no longer appear in any allowed pair.

## The problem

The input is a binary CSP with variables $x_1, \ldots, x_n$, finite domains $D_1, \ldots, D_n$ with $|D_i| \le d$, and binary constraints. PC-2 works on the *complete* network: for each pair $i < j$ it keeps a relation $R_{ij} \subseteq D_i \times D_j$, the intersection of the constraints on $x_i$ and $x_j$, or all of $D_i \times D_j$ if there is none. $R_{ji}$ is the converse of $R_{ij}$.

A pair $(a, b) \in R_{ij}$ is *path consistent* through $k \notin \{i, j\}$ if some $c \in D_k$ has $(a, c) \in R_{ik}$ and $(c, b) \in R_{kj}$. The network is path consistent if this holds for all pairs, all $i \ne j$ and all $k$. It is *strongly* path consistent if it is also [arc consistent](/arc-consistency/). The output is the strong path consistency closure: the largest strongly path consistent sub-network, which the page [path consistency](/path-consistency/) shows is unique.

Notation: $n$ variables, $d$ the largest domain size, $k$ the third variable of a triple and the consistency level 3. The number of constraints does not enter the bound, because the network is completed to $n(n-1)/2$ relations. The cost is counted in checks, each a test "$(a, c) \in R_{ik}$ and $(c, b) \in R_{kj}$?", on a word-RAM with constant-time membership tests.

## The algorithm

A triple $(i, k, j)$ with $i < j$ and $k \notin \{i, j\}$ stands for "revise $R_{ij}$ through $x_k$".

```pseudo id=main
PC-2(D, R)                                   ▷ R holds R_ij for all i < j
L1  Q ← all triples (i, k, j) with i < j and k ∉ {i, j}
L2  while Q ≠ ∅ do
L3      remove a triple (i, k, j) from Q
L4      if REVISE-PATH(i, k, j) then
L5          if R_ij = ∅ then return false
L6          for each m ∉ {i, j} do
L7              add (min(i, m), j, max(i, m)) and (min(j, m), i, max(j, m)) to Q, unless already there
L8  delete from each D_i every value a that is missing from some R_ij, and the pairs that use it
L9  return true if no D_i is empty, else false

REVISE-PATH(i, k, j)                         ▷ keep the pairs of R_ij that extend to x_k
L10 R' ← {(a, b) ∈ R_ij : some c ∈ D_k has (a, c) ∈ R_ik and (c, b) ∈ R_kj}
L11 if R' = R_ij then return false
L12 R_ij ← R'; return true
```

The test for $R_{ij}$ through $k$ reads $R_{ij}$, $R_{ik}$ and $R_{kj}$. When $R_{ij}$ shrinks, the tests that read it as a side relation are "$R_{im}$ through $j$" and "$R_{jm}$ through $i$", for each other $m$. Line L7 puts exactly these back. Line L8 makes the result arc consistent as well; the correctness proof shows why it does not break path consistency.

## Example

Take the 4-cycle $x_0, x_1, x_2, x_3$ with domain $\{0, 1\}$ and the constraint $\ne$ on the edges $01$, $12$, $23$ and $30$. The pairs $02$ and $13$ have no constraint, so they start with all 4 pairs. Line L1 queues $4 \cdot 3 \cdot 2 / 2 = 12$ triples.

| step | triple | relation revised | pairs deleted | added to the queue |
|---|---|---|---|---|
| 1, 2 | $(0, 2, 1)$, $(0, 3, 1)$ | $R_{01}$ | none | none |
| 3 | $(0, 1, 2)$ | $R_{02}$ through $x_1$ | $(0, 1), (1, 0)$ | $(0, 2, 1)$ |
| 4 to 8 | $(0, 3, 2)$ to $(1, 3, 2)$ | various | none | none |
| 9 | $(1, 0, 3)$ | $R_{13}$ through $x_0$ | $(0, 1), (1, 0)$ | $(0, 3, 1)$, $(0, 1, 3)$, $(1, 3, 2)$ |
| 10 to 16 | the rest | various | none | none |

In step 3, a pair $(a, b)$ with $a \ne b$ for $x_0$ and $x_2$ needs a value of $x_1$ that differs from both, and there is none in $\{0, 1\}$. So PC-2 derives the new constraint $x_0 = x_2$, and in step 9 it derives $x_1 = x_3$. The other triples that line L7 adds, such as $(1, 0, 2)$ after step 3, are still in the queue and are not added twice. The run makes 16 revisions and 56 checks, and line L8 deletes nothing. The graph has the two solutions $0101$ and $1010$, and both agree with the derived equalities.

On the triangle $x_0, x_1, x_2$ with domain $\{0, 1\}$ and $\ne$ on each pair, the first triple $(0, 2, 1)$ empties $R_{01}$, and PC-2 returns false. Arc consistency cannot find this.

## Correctness

PC-2 returns true exactly when the strong path consistency closure has no empty domain, and it then leaves that closure. The argument has the same shape as for AC-3. The union of two path consistent networks is path consistent, so a largest one, $R^\ast$, exists. REVISE-PATH never deletes a pair of $R^\ast$, because such a pair has a witness $c$ inside $R^\ast$. A triple that is not in the queue is satisfied, because line L7 re-queues each triple whose test reads the changed relation. So when the queue is empty the network is path consistent and equals $R^\ast$. Finally, in a path consistent network with at least 3 variables, a value occurs either in every relation of its variable or in none, so line L8 removes exactly the values with no support and gives the strong closure. The full proof is below.

## Complexity

**Revisions.** Line L1 queues $n(n-1)(n-2)/2$ triples. Each of the $n(n-1)/2$ relations loses pairs at most $d^2$ times, and each time line L7 adds at most $2(n-2)$ triples. So there are at most

$$\frac{n(n-1)(n-2)}{2} + n(n-1)(n-2) d^2 = O(n^3 d^2)$$

revisions.

**Checks.** REVISE-PATH tests at most $d$ values $c$ for each of at most $d^2$ pairs of $R_{ij}$, so it makes at most $d^3$ checks. The total is $O(n^3 d^2) \cdot d^3 = O(n^3 d^5)$ in the worst case, the bound of Mackworth and Freuder (1985). Line L8 takes $O(n^2 d^2)$ time.

**Space.** The complete network has $n(n-1)/2$ relations of at most $d^2$ pairs, and the queue has at most $n(n-1)(n-2)/2$ triples. The extra space is $O(n^3 + n^2 d^2)$.

For comparison, PC-1 revises all triples in passes until nothing changes and costs $O(n^5 d^5)$, and PC-4 (Han and Lee 1988) uses support counters, as [AC-4](/ac-4/) does, and runs in $O(n^3 d^3)$ time.

## Properties

- **Exact.** It computes the strong path consistency closure; the result does not depend on the order of the queue.
- **Changes the graph.** It adds relations between pairs that had no constraint, so the [constraint graph](/constraint-graph/) becomes complete in general. Structure-based methods cannot use the original sparse graph after PC-2.
- **Sound.** No pair of values that occurs in a solution is deleted.
- **Complete for some classes.** On binary Boolean CSPs (2-SAT), on the [simple temporal problem](/simple-temporal-problem/), and on any binary constraints closed under a majority operation, a strongly path consistent network with no empty domain has a solution (Jeavons, Cohen and Cooper 1998 for the majority case). See [path consistency](/path-consistency/).

## Variants and improvements

- **PC-1.** Revise every triple in each pass until a pass changes nothing; $O(n^5 d^5)$.
- **PC-3 and PC-4.** Counter-based, in the style of AC-4. Mohr and Henderson (1986) gave PC-3, and Han and Lee (1988) showed that PC-3 can delete pairs it should keep and gave the corrected PC-4, with $O(n^3 d^3)$ time and space.
- **Directional path consistency.** Revise only along an order of the variables, from the last to the first, through earlier variables. Along an order of induced width at most 2 this, with directional arc consistency, gives backtrack-free search, by the argument of [Freuder's theorem](/freuder-theorem/).
- **Partial path consistency.** Revise only the triangles of a chordal completion of the constraint graph, so no new edges appear outside it. This is the standard method for large temporal networks.
- **Floyd-Warshall.** For the simple temporal problem the relations are intervals of differences, and composing and intersecting them is addition and minimum. Path consistency is then the Floyd-Warshall algorithm, in $O(n^3)$ time.

## When to use it

Use PC-2 when arc consistency is too weak and $n$ is small, for example on dense networks of a few dozen variables, on temporal networks, and on binary Boolean or other majority-closed constraints, where it decides the problem. For large networks the $n^3$ term and the loss of sparsity are too costly; use [singleton arc consistency](/singleton-arc-consistency/) or a search with [maintaining arc consistency](/maintaining-arc-consistency/) instead. When memory allows, PC-4 or a counter-based method avoids the $d^5$ factor.

## Pitfalls

- **Forgetting the missing constraints.** Path consistency runs on the complete network. A pair with no constraint must start with the full relation $D_i \times D_j$, or the algorithm misses derived constraints such as $x_0 = x_2$ above.
- **Re-queuing the wrong triples.** When $R_{ij}$ changes, the triples to revise again are those that read $R_{ij}$ as a side relation, not those whose target is $R_{ij}$.
- **Keeping only one direction.** $R_{ij}$ and $R_{ji}$ are the same constraint. Store one of them and derive the other, or keep both equal after each change.
- **Path consistency without arc consistency.** Some definitions of path consistency do not include arc consistency. Line L8 is needed for the strong form.
- **Expecting a solver.** Path consistency is not complete in general. For example, 4 variables with domain $\{0, 1, 2\}$ and $\ne$ on all pairs (3-colouring $K_4$) are path consistent and have no solution.

## Implementations

## History

Montanari (1974) introduced path consistency for networks of binary constraints and showed that in a complete network it is enough to test paths of length 2. Mackworth (1977) gave the algorithms PC-1 and PC-2 in the same paper as AC-3. Mackworth and Freuder (1985) proved the bounds $O(n^5 d^5)$ for PC-1 and $O(n^3 d^5)$ for PC-2. Mohr and Henderson (1986) gave the counter-based PC-3, which Han and Lee (1988) corrected as PC-4, with $O(n^3 d^3)$ time.

## References
