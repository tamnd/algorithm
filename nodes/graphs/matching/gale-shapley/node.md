---
tag: 9YR7J5
kind: algorithm
slug: gale-shapley
name: Gale-Shapley algorithm
aliases:
- deferred acceptance
- stable marriage algorithm
area: graphs/matching
level: core
summary: 'Deferred acceptance: proposers propose in turn until all are matched, producing a stable matching in O(n²) time.'
solves: [stable-matching]
model: word-ram
complexity:
  vars: {n: the number of agents on both sides, m: the total length of the preference lists}
  time: {worst: O(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1962
  people: [David Gale, Lloyd Shapley]
  note: Gale and Shapley proved that stable matchings always exist by this algorithm in 1962; the American medical residency match had used an equivalent procedure since the early 1950s.
prereqs: [stable-matching]
see_also: [hospitals-residents-problem, stable-matching-rotations, stable-matching-with-ties, stable-roommates-problem, irving-stable-roommates, bipartite-matching, hungarian-algorithm]
sources:
  - paper: doi:10.2307/2312726
    title: David Gale and Lloyd S. Shapley, College admissions and the stability of marriage, The American Mathematical Monthly 69(1), 9 to 15 (1962)
    locator: the whole paper (the existence theorem, the deferred acceptance procedure and the optimality theorem)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 1.1, A First Problem, Stable Matching, and Section 2.3, Implementing the Stable Matching Algorithm Using Lists and Arrays
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 25.2, The stable-marriage problem
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: Chapter 1 (the fundamental algorithm, man-optimality and its consequences)
---

The Gale-Shapley algorithm, also called deferred acceptance, finds a [stable matching](/stable-matching/) between two sides of agents who rank each other. Agents on one side, the proposers, propose to the other side in their order of preference; each receiver keeps the best proposal so far and rejects the rest, and a receiver's acceptance is only provisional. It runs in time linear in the total length of the preference lists, $O(n^2)$ when everyone ranks everyone on the other side, and it returns the stable matching that is best for every proposer at once. The underlying graph of acceptable pairs is bipartite, and the preferences are rankings, not weights; with one side only, the [stable roommates problem](/stable-roommates-problem/) needs [Irving's algorithm](/irving-stable-roommates/).

## In plain words

Picture a dance. Each person on one side asks their favourite partner on the other side. Each person who is asked keeps the best offer so far, says "maybe" to it, and turns down the others. Anyone turned down asks the next person on their list. A person who said "maybe" can drop that partner later, when a better offer comes. When nobody has anyone left to ask, the dance pairs are fixed.

The result is stable: no two people who are not paired with each other would both rather be together. The askers come off well: each gets the best partner they could get in any stable pairing. The people who are asked get the worst partner they could get in any stable pairing.

## The problem

The input is a set $P$ of proposers and a set $R$ of receivers, with $n = |P| + |R|$, and for each agent a strict preference list, best first, of the agents on the other side that it finds acceptable. A pair $pr$ is acceptable if each lists the other; these pairs are the edges of a [bipartite graph](/bipartite-graph/), and $m$ is the total length of the lists. A matching $M$ uses only acceptable pairs. A pair $pr \notin M$ that is acceptable *blocks* $M$ if $p$ is single or prefers $r$ to its partner, and $r$ is single or prefers $p$ to its partner. The output is a matching with no blocking pair, a stable matching.

**Assumptions.** Lists are strict, without ties, and without repeated entries; ties are handled in [stable matching with ties](/stable-matching-with-ties/). The two sides may have different sizes, and lists may be incomplete, so the stable matching need not be perfect. An agent listed by someone it does not list itself is treated as unacceptable to both. The classical stable marriage problem is the case $|P| = |R|$ with complete lists, where every stable matching is perfect and $m = |P|^2$.

## The algorithm

```pseudo id=main
GALE-SHAPLEY(lists of P, lists of R)
L1  for each r ∈ R and each p on the list of r do rank_r(p) ← the position of p on the list of r
L2  for each p ∈ P do next[p] ← 1;  for each r ∈ R do holder[r] ← NIL
L3  F ← a stack holding all of P
L4  while F is not empty do
L5      p ← POP(F)
L6      if p has proposed to every receiver on its list then continue   ▷ p stays single
L7      r ← the receiver at position next[p] on the list of p;  next[p] ← next[p] + 1
L8      if p is not on the list of r then PUSH(F, p)
L9      else if holder[r] = NIL then holder[r] ← p
L10     else if rank_r(p) < rank_r(holder[r]) then PUSH(F, holder[r]);  holder[r] ← p
L11     else PUSH(F, p)
L12 return the pairs (holder[r], r) with holder[r] ≠ NIL
```

Line L7 is a proposal. Lines L9 and L10 are provisional acceptances: a receiver holds at most one proposer, and in line L10 it trades up, sending the old holder back to $F$. Lines L8 and L11 are rejections. The order in which free proposers are taken from $F$ does not matter: every order gives the same matching. Line L1 needs $\text{rank}_r(p)$ in constant time. With complete lists an $|R| \times |P|$ array does it; with incomplete lists, the implementation stores, at each entry $r$ of the list of $p$, the position of $p$ on the list of $r$, computed in $O(n + m)$ time by grouping the entries by receiver.

## Example

The proposers are $A$, $B$, $C$ and the receivers $x$, $y$, $z$, with the lists

| agent | list | agent | list |
|---|---|---|---|
| $A$ | $x, y, z$ | $x$ | $C, B, A$ |
| $B$ | $y, x, z$ | $y$ | $A, B, C$ |
| $C$ | $x, y, z$ | $z$ | $A, B, C$ |

The stack gives the proposers in the order $A$, $B$, $C$, and a proposer pushed back is the next one popped.

| step | proposal | outcome | held after the step |
|---|---|---|---|
| 1 | $A \to x$ | $x$ was free, holds $A$ | $xA$ |
| 2 | $B \to y$ | $y$ was free, holds $B$ | $xA$, $yB$ |
| 3 | $C \to x$ | $x$ prefers $C$ to $A$; $A$ is free again | $xC$, $yB$ |
| 4 | $A \to y$ | $y$ prefers $A$ to $B$; $B$ is free again | $xC$, $yA$ |
| 5 | $B \to x$ | $x$ prefers $C$ to $B$; rejected | $xC$, $yA$ |
| 6 | $B \to z$ | $z$ was free, holds $B$ | $xC$, $yA$, $zB$ |

The result is $\{Ay, Bz, Cx\}$. It is stable: $A$ prefers only $x$, which holds its first choice $C$; $B$ prefers $y$ and $x$, which both hold someone they rank above $B$; $C$ has its first choice. Here it is the only stable matching.

**Two stable matchings.** Change the list of $x$ to $B, A, C$. Then the proposals go $A \to x$, $B \to y$, $C \to x$ (rejected), $C \to y$ (rejected), $C \to z$, giving $\{Ax, By, Cz\}$, where $A$ and $B$ have their first choices. With the roles swapped, the receivers proposing, the result is $\{Ay, Bx, Cz\}$, where $x$ and $y$ have their first choices. Both are stable, and each side prefers the one where it proposed.

**No perfect matching.** If $A$ and $B$ both list only $x$, and $x$ lists $B, A$, then $A$ proposes and is held, $B$ proposes and replaces $A$, and $A$ has nobody left: the result is $\{Bx\}$ with $A$ single.

**Edge cases.** With no agents the result is empty. A proposer with an empty list stays single at once in line L6. A receiver that no one proposes to stays single.

## Correctness

The invariant has two parts. Each receiver only trades up: once it holds a proposer, it holds one for the rest of the run, and each new holder is ranked higher than the one before. And if $p$ has proposed to $r$ in an acceptable pair, then $r$ holds $p$ or a proposer it prefers to $p$. At the end every proposer is held or has exhausted its list. A pair $pr$ in which $p$ prefers $r$ to its final partner, or $p$ is single, is a pair where $p$ has proposed to $r$; by the invariant $r$ holds someone better, so $pr$ does not block. No proposer is ever rejected by a receiver that is its partner in some stable matching; this gives proposer-optimality and the independence of the order. The full proof is in the proof files below.

## Complexity

The model is the [word RAM](/word-ram/); agents are indices, and reading or comparing a rank costs $O(1)$.

- **Proposals.** Each proposer proposes to each receiver on its list at most once, because $\text{next}[p]$ only grows, so there are at most $m$ proposals. With complete lists and $|P| = |R| = k$, there are at most $k^2 - k + 1$: once some receiver has been proposed to, it holds someone forever, and the run ends when every receiver holds someone, so at most one proposer reaches the last entry of its list.
- **Iterations.** Each pass of the loop either makes a proposal or, in line L6, removes a proposer for good. A proposer enters $F$ again only after a proposal or after being displaced by one, so there are at most $|P| + m$ pushes and as many passes.
- **Total.** $O(n + m)$ time, which is $O(n^2)$ for complete lists, and $\Theta(n + m)$ space for the lists, the ranks and the arrays $\text{next}$ and $\text{holder}$. This is linear in the size of the input.

The full argument is in the complexity proof below.

## Properties

- **Proposer-optimal.** Each proposer gets the best partner it has in any stable matching, or stays single if it is single in every stable matching. This holds for all proposers at the same time.
- **Receiver-pessimal.** Each receiver gets the worst partner it has in any stable matching.
- **Order-independent.** The matching does not depend on the order in which free proposers are chosen, which makes the result well defined.
- **Same agents matched.** The set of matched agents is the same in every stable matching, the rural hospitals theorem; the algorithm finds this set.
- **Strategy-proof for proposers.** No proposer can get a better partner by misreporting its list (Dubins and Freedman, 1981; Roth, 1982). Receivers can sometimes gain by misreporting.
- **Average case.** With complete lists drawn uniformly at random, the expected number of proposals is about $k \ln k$ for $k$ agents per side.

## Variants and improvements

- **Receivers propose.** Swapping the roles gives the receiver-optimal stable matching, the other end of the lattice of stable matchings. The [rotations](/stable-matching-rotations/) between the two describe every stable matching.
- **Many-to-one.** Each receiver has a capacity and holds up to that many proposers: the [hospitals-residents problem](/hospitals-residents-problem/), solved by the same method in $O(n + m)$ time.
- **Ties.** With ties broken arbitrarily the algorithm gives a weakly stable matching; maximizing its size is NP-hard. See [stable matching with ties](/stable-matching-with-ties/).
- **One side only.** In the [stable roommates problem](/stable-roommates-problem/) a stable matching may not exist, and [Irving's algorithm](/irving-stable-roommates/) decides it in $O(n^2)$ time.
- **McVitie and Wilson.** A recursive formulation that adds one proposer at a time and resolves the chain of displacements it causes; it makes the same proposals.

## When to use it

Use it whenever a stable matching between two sides with strict preferences is needed: school choice, residency matching, the assignment of students to courses or projects. Choose the side whose interests should come first as the proposers. If the goal is a largest matching or a cheapest assignment, stability is the wrong objective: use [bipartite matching](/bipartite-matching/) or the [Hungarian algorithm](/hungarian-algorithm/).

## Pitfalls

- **Searching the receiver's list.** Finding $\text{rank}_r(p)$ by scanning the list of $r$ costs $O(k)$ per proposal and $O(k^3)$ in all. Precompute the ranks, as in line L1.
- **Proposing twice to the same receiver.** The pointer $\text{next}[p]$ must survive rejections and displacements. A displaced proposer continues after the receiver that displaced it; it does not start its list again.
- **One-sided acceptability.** With incomplete lists, a receiver must reject a proposer it does not list. Otherwise the output can contain a pair that one side finds unacceptable.
- **Expecting a perfect matching.** With incomplete lists or sides of different sizes, some agents stay single in every stable matching, so a missing partner is not an error.
- **Expecting fairness.** The result favours the proposers as much as stability allows. Exchanging the sides can change many pairs.

## Implementations

The Python version takes the two lists of preference lists as lists of indices, best first, and returns the partner of each proposer, the partner of each receiver, with $-1$ for a single agent, and the number of proposals. The free proposers are kept on a stack, and an optional callback reports each proposal and its outcome.

## History

David Gale and Lloyd Shapley published the algorithm in 1962 in "College admissions and the stability of marriage", where they proved that a stable matching always exists and that the proposing side gets its optimal stable matching. Alvin Roth showed in 1984 that the procedure used by the American medical residency match since the early 1950s is equivalent to deferred acceptance with the hospitals proposing. Donald Knuth's 1976 lectures "Mariages stables" studied the algorithm's analysis and the structure of stable matchings. In 2012 Roth and Shapley received the Nobel Memorial Prize in Economic Sciences for the theory of stable allocations and its use in market design.

## References
