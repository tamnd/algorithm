---
tag: Q2A2ZX
kind: algorithm
slug: irving-stable-roommates
name: Irving's stable roommates algorithm
aliases:
- Irving algorithm
area: graphs/matching
level: advanced
summary: Finds a stable matching in a general graph with preference lists, or reports that none exists, in O(n²) time for complete lists.
solves: [stable-roommates-problem]
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of mutually acceptable pairs}
  time: {worst: O(n + n m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1985
  people: [Robert W. Irving]
  note: Irving gave the first polynomial algorithm for the stable roommates problem, after Knuth had asked for one in 1976.
prereqs: [stable-roommates-problem, gale-shapley]
see_also: [stable-matching, stable-matching-rotations, stable-matching-with-ties, gale-shapley, hospitals-residents-problem, maximum-matching, edmonds-blossom, np-complete]
sources:
  - paper: doi:10.1016/0196-6774(85)90033-1
    title: Robert W. Irving, An efficient algorithm for the stable roommates problem, Journal of Algorithms 6(4), 577 to 595 (1985)
    locator: the whole paper (phase 1, rotations, phase 2, the proofs and the O(n^2) bound for complete lists)
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: Chapter 4, The Stable Roommates Problem (the algorithm, the stable tables, the rotation lemmas and incomplete lists)
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 4, The Stable Roommates Problem (Irving's algorithm for incomplete lists and its O(m) bound)
  - paper: doi:10.2307/2312726
    title: David Gale and Lloyd S. Shapley, College admissions and the stability of marriage, The American Mathematical Monthly 69(1), 9 to 15 (1962)
    locator: the section on the roommates problem (an instance with no stable matching)
---

Irving's algorithm solves the [stable roommates problem](/stable-roommates-problem/): $n$ agents rank each other, and we want a [stable matching](/stable-matching/), or a proof that none exists. The graph of acceptable pairs is general, not bipartite, and it has no weights; the ranks are preferences, not weights. Phase 1 is a round of proposals as in the [Gale-Shapley algorithm](/gale-shapley/), and it cuts each list to a "stable table". Phase 2 then removes cyclic structures called rotations one at a time, until every list has one entry, which is a stable matching, or some list becomes empty, which proves that no stable matching exists. The version below runs in $O(n + nm)$ time on $n$ agents and $m$ acceptable pairs. With more careful bookkeeping Irving's original version runs in $O(n^2)$ time for complete lists.

## In plain words

Some students must share rooms in pairs, and each student ranks the others. A pairing is stable if no two students both prefer each other to the roommates they got. Unlike the marriage case with two sides, such a pairing may not exist at all.

In the first phase, each student asks the best student who has not yet refused. A student who is asked keeps the best offer, refuses the rest, and also crosses off everyone worse than that offer, since they can never pair. When this settles, each student holds one offer and has one offer held.

In the second phase, the algorithm finds a cycle of students who must all give up their first choice together. It crosses off those choices and repeats. If every list shrinks to one name, those names form a stable pairing. If some list runs out, no stable pairing exists.

## The problem

The input has $n$ agents $0, \ldots, n - 1$, and a list for each agent: the agents it finds acceptable, best first. Lists may be incomplete. A pair $\{a, b\}$ is *acceptable* if each lists the other; let $m$ be the number of acceptable pairs. These pairs form a general [undirected graph](/undirected-graph/) with no weights. A *matching* is a set of acceptable pairs with no common agent. A pair $\{a, b\}$ that is acceptable and not in the matching *blocks* it if $a$ is single or prefers $b$ to its partner, and $b$ is single or prefers $a$ to its partner. A matching is *stable* if no pair blocks it.

The output is a stable matching, given as the partner of each agent (nil for a single agent), or "no stable matching". The empty instance has the empty stable matching. If the graph is bipartite with men on one side and women on the other, a stable matching always exists and [Gale-Shapley](/gale-shapley/) finds one; Irving's algorithm also works there.

## The algorithm

The algorithm keeps a *table*: a sublist of each agent's list. Every deletion is symmetric: deleting $\{a, b\}$ removes $b$ from the list of $a$ and $a$ from the list of $b$. Write $\text{first}(x)$, $\text{second}(x)$ and $\text{last}(x)$ for the first, second and last entries of the current list of $x$. The phrase "delete all $z$ after $x$ on the list of $y$" means: delete $\{y, z\}$ for each $z$ that is ranked by $y$ below $x$ and still present.

```pseudo id=main
IRVING(lists)
L1  make the lists symmetric: keep b on the list of a only if a is on the list of b
L2  F ← all agents;  holder[y] ← nil for each y          ▷ phase 1: proposals
L3  while F is not empty do
L4      x ← POP(F);  if the list of x is empty then continue
L5      y ← first(x)                                       ▷ x proposes to y
L6      delete all z after x on the list of y               ▷ a deleted holder of y goes back to F
L7      holder[y] ← x
L8  A ← the agents with nonempty lists;  S ← empty stack    ▷ phase 2: rotations
L9  loop
L10     cut S at its first agent whose list has fewer than 2 entries, or whose next agent is not last(second(·)) of it
L11     if S is empty then exit the loop if no list has 2 or more entries, else push such an agent
L12     repeat p ← last(second(top(S))); push p if it is not in S, until p is already in S
L13     ρ ← the agents of S from p to the top;  pop them
L14     for each x ∈ ρ, with y = second(x) computed before any deletion, delete all z after x on the list of y
L15     if the list of some agent of A is empty then return "no stable matching"
L16 return the pairs {x, first(x)} for x ∈ A;  the agents outside A are single
```

**Phase 1** (lines L2 to L7) is the proposal round of Gale-Shapley, with one change: when $y$ receives a proposal from $x$, $y$ deletes not only the worse proposer it held but every agent it ranks below $x$. These agents can never be the partner of $y$ in a stable matching. If $y$ held a proposal from such an agent, that agent becomes free again and proposes to the next agent on its list. At the end, for agents with nonempty lists, $\text{first}(x) = y$ if and only if $\text{last}(y) = x$.

**Rotations.** In such a table, a *rotation* is a sequence of distinct agents $x_0, x_1, \ldots, x_{r-1}$ with $x_{i+1} = \text{last}(\text{second}(x_i))$, indices modulo $r$. Write $y_i = \text{first}(x_i)$; then $y_{i+1} = \text{second}(x_i)$. *Eliminating* the rotation (line L14) makes each $y_{i+1}$ delete everyone it ranks below $x_i$. So $x_{i+1}$ loses $y_{i+1}$, and its new first entry is $y_{i+2}$: every $x_i$ moves one step down its list together.

**Phase 2** (lines L8 to L15) finds rotations by a walk. From an agent with at least two entries, it follows $p \mapsto \text{last}(\text{second}(p))$ until an agent repeats; the cycle at the end of the walk is a rotation. The stack $S$ keeps the part of the walk before the cycle for the next search, and line L10 cuts it back to the part that is still valid after the elimination.

## Example

Let the lists be $A: B, D, C$; $B: C, D, A$; $C: A, D, B$; $D: C, B, A$. All pairs are acceptable.

**Phase 1**, with $F$ popped in the order $A, B, C, D$:

| step | proposal | deletions | holders after the step |
|---|---|---|---|
| 1 | $A \to B$ | none, $A$ is last for $B$ | $B$ holds $A$ |
| 2 | $B \to C$ | none, $B$ is last for $C$ | $C$ holds $B$ |
| 3 | $C \to A$ | none, $C$ is last for $A$ | $A$ holds $C$ |
| 4 | $D \to C$ | $\{C, B\}$; $B$ is free again | $C$ holds $D$ |
| 5 | $B \to D$ (its new first) | $\{D, A\}$ | $D$ holds $B$ |

The table is now $A: B, C$; $B: D, A$; $C: A, D$; $D: C, B$. Each first entry matches a last entry: $\text{first}(A) = B$ and $\text{last}(B) = A$, and so on.

**Phase 2.** Start the walk at $A$: $\text{second}(A) = C$ and $\text{last}(C) = D$; then $\text{second}(D) = B$ and $\text{last}(B) = A$, which repeats. The rotation is $(A, D)$, with $y_0 = B$, $y_1 = C$. Eliminate it: $C$ deletes everyone below $A$, that is $D$, and $B$ deletes everyone below $D$, that is $A$. The table becomes $A: C$; $B: D$; $C: A$; $D: B$. Every list has one entry, so the output is $\{AC, BD\}$. It is stable: $A$ prefers $B$, but $B$ prefers $D$ to $A$; $C$ prefers $A$ already; $B$ prefers $C$, but $C$ prefers $A$; $D$ prefers $C$, but $C$ prefers $A$.

This instance has a second stable matching, $\{AB, CD\}$. The algorithm returns one stable matching, which depends on the choice of rotations.

**No stable matching.** Let $A: B, C, D$; $B: C, A, D$; $C: A, B, D$; $D: A, B, C$. In phase 1, $A$, $B$ and $C$ propose to $B$, $C$ and $A$, and each of them deletes $D$. So $D$ ends with an empty list and is not in $A$. The table is $A: B, C$; $B: C, A$; $C: A, B$. The walk from $A$ gives $A, B, C$ and back to $A$. Eliminating this rotation deletes $\{C, B\}$, $\{A, C\}$ and $\{B, A\}$, so all three lists are empty and the algorithm reports that no stable matching exists. This is the odd preference cycle of Gale and Shapley.

## Correctness

The main steps are these; the full proof is below.

1. **Phase 1 removes only useless pairs.** No pair deleted at line L6 is in any stable matching: the first such pair would be blocked by the proposer $x$ and $y$.
2. **The table after phase 1 is stable in form.** At its end, $\text{first}$ is a bijection of $A$ onto itself, and $\text{last}(\text{first}(x)) = x$. With this, every stable matching matches all agents of $A$ and no others.
3. **Phase 2 keeps a stable matching if there is one.** If the table contains a stable matching $M$, then after a rotation is eliminated it still contains one: either $M$ itself, or $M$ with each $x_i$ moved from $y_i$ to $y_{i+1}$.
4. **The walk is well defined.** If $x$ has at least two entries, so does $\text{last}(\text{second}(x))$; so the walk never gets stuck.
5. **The output is stable.** Each deleted pair was deleted by one of its agents, which then had an entry it prefers; at the end that agent's single entry is at least as good. So no deleted pair blocks the final matching.

If some list of $A$ becomes empty, step 3 shows that the table before the elimination held no stable matching, and by steps 1 and 3 by induction, no stable matching exists.

## Complexity

The model is the [word RAM](/word-ram/). Each list is an array with a flag per entry and pointers to its first live entry, its last live entry, and a pointer for $\text{second}$ that only moves right. The rank of each agent in each list is stored, so deletion of a pair takes $O(1)$ time plus pointer moves.

- **Line L1** takes $O(n + m)$ time with hashing or one array per agent.
- **Phase 1.** Each pair is deleted at most once, and each pointer moves at most the length of its list, so all deletions cost $O(n + m)$. An agent goes back to $F$ only when a pair is deleted, so there are at most $n + m$ pops.
- **Phase 2.** Each elimination deletes at least the $r \ge 2$ pairs $\{x_i, y_i\}$, so there are at most $m/2$ rotations. Line L10 and line L15 take $O(n)$ time per rotation. Each push of the walk costs $O(1)$ amortized, and the pushes are at most the pops plus $n$. So phase 2 takes $O(n + nm)$ time.
- **Space.** $O(n + m)$ for the lists, the flags and the ranks.

So the total is $O(n + nm)$ in the worst case. With complete lists, $m = \Theta(n^2)$, which gives $O(n^3)$. Irving's paper reuses the walk across rotations without the scan of line L10 and reaches $O(n^2)$ time for complete lists, and the same idea gives $O(n + m)$ for incomplete lists; see Gusfield and Irving, Chapter 4.

## Properties

- **Graphs.** General graphs, with no weights. A bipartite instance always has a stable matching, so on such inputs the answer is never "no stable matching".
- **Same agents matched.** Every stable matching of an instance matches the same set of agents, which is the set $A$ of agents with nonempty lists after phase 1.
- **Order of rotations.** The output depends on which rotation is eliminated first. Gusfield and Irving show that every stable matching of the instance is reached by some order of eliminations, and that phase 1 gives the same table for every order of $F$.
- **Deterministic and iterative.** The walk uses an explicit stack, so there is no deep recursion.

## Variants and improvements

- **Linear time.** Reusing the valid part of the walk without a full scan, as Irving does, gives $O(n + m)$ time.
- **Stable partitions.** Tan's algorithm finds a *stable partition*, a structure that always exists. It gives a stable matching when one exists, and otherwise odd cycles of preferences that show why none exists.
- **Ties.** With ties in the lists, deciding whether a weakly stable matching exists is [NP-complete](/np-complete/), by Ronn for complete lists; see [stable matching with ties](/stable-matching-with-ties/). Super-stable matchings with ties can still be found in polynomial time by an extension of this algorithm.
- **All stable matchings.** The rotations of an instance form a structure like the [rotation poset of stable marriage](/stable-matching-rotations/), and it describes all stable matchings.

## When to use it

Use it for any pairing problem with preferences in which every agent may pair with any other: roommates, pairs of players, kidney exchange with pairs only, peer-to-peer partner choice. If the instance is bipartite, [Gale-Shapley](/gale-shapley/) is simpler. If the goal is a largest pairing without preferences, use a [maximum matching](/maximum-matching/) algorithm such as [Edmonds' blossom algorithm](/edmonds-blossom/) instead.

## Pitfalls

- **Assuming a solution exists.** Unlike stable marriage, the answer can be "none", as in the example with $A$, $B$, $C$ and $D$. Code must handle it.
- **Not making the lists symmetric.** If $a$ lists $b$ but $b$ does not list $a$, the pair is not acceptable. Leaving $b$ on the list of $a$ breaks the first-last property of phase 1.
- **Freeing the old holder too late.** At line L6, the deletions can remove the agent that $y$ held. That agent must go back to $F$. If $\text{holder}[y]$ is set before the deletions, the old holder is lost and the loop can stop with a free agent that has not proposed.
- **Computing second() during the elimination.** All pairs $(x_i, \text{second}(x_i))$ must be computed before line L14 deletes anything, because a deletion can change $\text{second}$ of a later $x_j$.
- **Reusing a stale walk.** After an elimination, an agent left on the stack can have only one entry, or its next agent can have changed. Line L10 cuts the stack at the first such agent; without it the next rotation found may not be a rotation of the current table.
- **Deleting by presence instead of by rank.** "Delete all $z$ after $x$ on the list of $y$" must use the rank of $x$, because $x$ itself may already be gone from that list in the same elimination.

## Implementations

The Python version takes the lists as a list of lists of agent numbers, best first, and returns the partner of each agent, or None when no stable matching exists. Each list is a fixed array with live flags, a head pointer, a tail pointer and a pointer for $\text{second}$. The tests compare it with a brute force that tries every matching on random instances with up to 8 agents.

## History

Gale and Shapley stated the roommates problem in 1962 and showed by a small example that, unlike the marriage problem, it may have no stable matching. Knuth asked in 1976 for an efficient algorithm to decide whether one exists. Robert W. Irving gave the two-phase algorithm in 1985, with an $O(n^2)$ bound for complete lists. Gusfield and Irving's 1989 book presented its theory of stable tables and rotations, and Tan's work of 1991 on stable partitions explained exactly when no stable matching exists.

## References
