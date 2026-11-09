---
tag: T6CQTJ
kind: algorithm
slug: cutset-conditioning
name: Cutset conditioning
aliases:
- cycle cutset method
- loop cutset conditioning
- cycle cutset decomposition
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Fixes a cycle cutset of variables, then solves the remaining tree-structured CSP for each assignment to the cutset.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, e: the number of binary constraints, d: the largest domain size, c: the size of the cycle cutset}
  time: {worst: O(d^c (e d + (n - c) d^2))}
  space: {extra: O(n d)}
properties: {deterministic: true, exact: true, in_place: false, online: false, recursive: false}
history:
  year: 1987
  people: [Rina Dechter, Judea Pearl]
  note: Pearl (1986) used loop cutset conditioning for belief networks. Dechter and Pearl (1987) and Dechter (1990) applied the cycle cutset to constraint networks, with the tree algorithm on the rest.
prereqs: [tree-structured-csp, feedback-vertex-set-problem]
see_also: [bucket-elimination, freuder-theorem, constraint-graph, tree-decomposition, treewidth, graph-coloring, belief-propagation, conflict-directed-backjumping]
sources:
  - paper: "Rina Dechter and Judea Pearl, Network-based heuristics for constraint-satisfaction problems, Artificial Intelligence 34(1), 1987, pages 1 to 38"
    locator: the cycle cutset method, with directional arc consistency on the tree that remains
  - paper: "Rina Dechter, Enhancement schemes for constraint processing, backjumping, learning, and cutset decomposition, Artificial Intelligence 41(3), 1990, pages 273 to 312"
    locator: cutset decomposition inside backtracking search, and its cost exponential in the cutset size
  - paper: "Judea Pearl, Fusion, propagation, and structuring in belief networks, Artificial Intelligence 29(3), 1986, pages 241 to 288"
    locator: conditioning on a loop cutset to reduce a multiply connected belief network to singly connected ones
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 10, Hybrids of search and inference, time-space trade-offs (the cycle cutset scheme and w-cutsets)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Section 6.5 (cutset conditioning on the map of Australia)
---

Cutset conditioning solves a binary [constraint satisfaction problem](/constraint-satisfaction-problem/) by choosing a *cycle cutset*: a set $S$ of variables whose removal leaves a [constraint graph](/constraint-graph/) with no cycle. For each assignment of the variables in $S$ that satisfies the constraints among them, it deletes from the other domains the values that disagree with this assignment and solves the forest that remains with the [tree-structured CSP algorithm](/tree-structured-csp/). With $|S| = c$, it takes $O(d^c (n - c) d^2)$ time for the tree parts, which is exponential in $c$ only. Dechter and Pearl brought it to constraint networks in 1987, after Pearl's loop cutset method for belief networks.

## In plain words

Cycles in the rules are what make a problem hard. A tree of rules is easy: one pass up and one pass down solve it. So pick a few unknowns that touch all the cycles. If you knew their values, you could cross out the values of their neighbours that do not fit, and what is left would be a tree.

You do not know their values, so try all combinations. For each one, solve the tree. If one tree has an answer, you have an answer for the whole problem. If none does, there is no answer. With $c$ chosen unknowns and $d$ values each, this is $d^c$ tree problems, which is fine when $c$ is small.

## The problem

The input is a binary CSP with variables $x_0, \ldots, x_{n-1}$, domains $D_v$ with $|D_v| \le d$, and $e$ binary constraints $R_{uv} \subseteq D_u \times D_v$, with $R_{vu}$ the converse. The constraint graph $G$ has an edge for each constrained pair. The output is a solution or the answer that none exists; the counting form returns the number of solutions.

A *cycle cutset* is a set $S$ of variables such that $G - S$, the graph with $S$ and its edges deleted, is a forest. Finding the smallest one is the [feedback vertex set problem](/feedback-vertex-set-problem/), which is NP-hard, so the algorithm takes any cutset, for example one from a greedy rule.

Notation: $n$ variables, $e$ constraints, $d$ the largest domain size, $c = |S|$ the cutset size. Cost is counted in constraint checks on the word-RAM.

## The algorithm

```pseudo id=main
CUTSET-CONDITIONING(D, R, S)         ▷ S is a cycle cutset: G − S is a forest
    F ← the forest G − S, with a breadth-first order and parents
L1  for each assignment s of S with s_x ∈ D_x for each x ∈ S do
L2      if s violates a constraint between two variables of S then go to the next s
L3      for each variable y not in S do
L4          D'_y ← {b ∈ D_y : (s_x, b) ∈ R_xy for every neighbour x ∈ S of y}
L5      t ← TREE-CSP(D', R restricted to F)            ▷ or TREE-COUNT, and add the count
L6      if t ≠ NONE then return s ∪ t
L7  return NONE                                         ▷ the counting form returns the sum
```

Line L4 *conditions* on $s$: once the values of $S$ are fixed, a constraint between $x \in S$ and $y \notin S$ becomes the unary constraint "$x_y$ fits $s_x$", which filters $D_y$. What remains is a binary CSP on the forest $F$, which line L5 solves in $O((n - c) d^2)$ time.

A greedy cutset, as in the implementation: delete vertices of degree at most 1 as long as there are any, since they lie on no cycle. If vertices remain, every one lies on a cycle; move one of largest degree into $S$ and repeat. The result is a cycle cutset, though not always the smallest.

## Example

Colour the map of Australia with three colours, so that neighbouring regions differ. The variables are WA, NT, SA, Q, NSW, V and T, and there are 9 constraints $\ne$: WA-NT, WA-SA, NT-SA, NT-Q, SA-Q, SA-NSW, SA-V, Q-NSW and NSW-V. T has no neighbour.

**The cutset.** The greedy rule first deletes T (degree 0). Every other region then has degree at least 2, and SA has the largest degree, 5. Deleting SA leaves the path WA-NT-Q-NSW-V, which the rule removes from its ends. So $S = \{\text{SA}\}$ and $c = 1$.

**Conditioning.** Take SA = red. Line L4 deletes red from the five neighbours of SA, so WA, NT, Q, NSW and V have the domains $\{\text{green}, \text{blue}\}$, and T keeps all three colours. The forest is the path WA-NT-Q-NSW-V and the single vertex T. On the path, two colours must alternate, so the path has 2 solutions, and T has 3. TREE-CSP returns WA = green, NT = blue, Q = green, NSW = blue, V = green, T = red, and with SA = red this is a solution of the whole map, found after one assignment of the cutset.

**Counting.** The colours are symmetric, so each of the 3 values of SA gives $2 \cdot 3 = 6$ solutions of the forest, and the map has $3 \cdot 6 = 18$ colourings. Brute force over all $3^7 = 2187$ assignments gives the same number. Conditioning did 3 tree computations on 6 variables instead.

## Correctness

Each solution of the CSP restricts to an assignment $s$ of $S$ that satisfies the constraints inside $S$, and to an assignment $t$ of the other variables. The pair passes line L2, and $t$ is a solution of the forest CSP of line L5: each $t_y$ lies in $D'_y$ because the solution satisfies the constraints between $y$ and $S$, and $t$ satisfies the constraints of $F$. In the other direction, any such $s$ and any solution $t$ of the forest CSP combine into a solution, because every constraint of the CSP lies inside $S$ (line L2), between $S$ and the rest (line L4), or inside $F$ (line L5). So the solutions are in one-to-one correspondence with the pairs $(s, t)$, and the algorithm finds one when one exists, and counts them in the counting form. The full proof is below.

## Complexity

**Assignments.** Line L1 runs over at most $d^c$ assignments.

**Per assignment.** Line L2 checks at most the constraints inside $S$. Line L4 makes at most $d$ checks per constraint between $S$ and the rest. Line L5 costs $O((n - c) d^2)$ by the [tree-structured CSP algorithm](/tree-structured-csp/). So one assignment costs $O(e d + (n - c) d^2)$.

**Total.** The time is $O(d^c (e d + (n - c) d^2))$. The term $e d$ is dominated by $(n - c) d^2$ when $e \le (n - c) d$, which is the usual case, and then the bound is the familiar $O(d^c (n - c) d^2) = O((n - c) d^{c+2})$. The counting form has the same number of operations, on numbers up to $d^n$.

**Space.** One assignment of $S$, the filtered domains $D'$ and the tree tables take $O(n d)$ space, besides the input. Unlike [bucket elimination](/bucket-elimination/), the space stays linear in the size of the problem whatever the cutset size.

**Cutset size and treewidth.** If $S$ is a cycle cutset of size $c$, then $G$ has [treewidth](/treewidth/) at most $c + 1$: add $S$ to every bag of a tree decomposition of the forest. So bucket elimination along a good order takes time $O(n d^{c+2})$ or less, often far less, since the treewidth can be much smaller than the cutset size, as in a long grid of width 2. Cutset conditioning pays more time to use less space.

## Properties

- **Exact and complete.** It finds a solution when one exists, and the counting form gives the exact count.
- **Exponential in $c$ only.** For a fixed cutset size the time is linear in $n$.
- **Linear space.** It keeps one assignment of the cutset at a time.
- **Depends on the cutset.** The cost depends on the cutset found. A minimum cycle cutset is a minimum [feedback vertex set](/feedback-vertex-set-problem/), which is NP-hard to find, though the problem is fixed-parameter tractable in $c$.
- **Easy to combine with search.** The loop of line L1 is a search over $S$, and [backjumping](/conflict-directed-backjumping/) or propagation can prune it.

## Variants and improvements

- **Inside backtracking.** Dechter (1990) runs a backtracking search and calls the tree algorithm as soon as the variables not yet assigned form a forest, so the cutset is found during the search and can change between branches.
- **w-cutset.** Condition on a set whose removal leaves a graph of induced width at most $w$, not 1, and solve the rest by [bucket elimination](/bucket-elimination/). The time is $O(n d^{c_w + w + 1})$ for a $w$-cutset of size $c_w$, and the space is $O(n d^w)$. This trades space for time between the two methods.
- **Loop cutset conditioning.** In belief networks, Pearl (1986) conditioned on a loop cutset and ran belief propagation on each singly connected network, then summed the results with weights. The CSP form above is the same idea with "exists" or "count" instead of probabilities.
- **Graph colouring.** For [graph colouring](/graph-coloring/) with $k$ colours, conditioning on a feedback vertex set of size $c$ gives an $O(k^c \cdot n k^2)$ algorithm.

## When to use it

Use cutset conditioning when the constraint graph is close to a tree, with a few variables that close all the cycles, and when memory is limited. It is a natural choice when the cutset variables are also good branching variables, as in search. If the graph has small treewidth but a large cycle cutset, such as a long ladder or a grid of width 2, use [bucket elimination](/bucket-elimination/) or a [tree decomposition](/tree-decomposition/) instead, if their memory fits.

## Pitfalls

- **Forgetting the constraints inside the cutset.** Line L2 must check them; the forest does not contain them.
- **Constraints that close a cycle in the rest.** If $G - S$ still has a cycle, the tree algorithm gives wrong answers. Check that the cutset really leaves a forest.
- **Stopping on the first assignment when counting.** The counting form must add the counts of all assignments of $S$.
- **Hoping for a minimum cutset.** The greedy rule can return a cutset far larger than the minimum. Better heuristics or a fixed-parameter algorithm for feedback vertex set can pay off when $d^c$ is large.
- **Comparing with treewidth.** A small treewidth does not imply a small cutset. The time $d^c$ can be much larger than the $d^{w^\ast + 1}$ of bucket elimination.

## Implementations

## History

Pearl (1986) introduced conditioning on a loop cutset to make belief propagation exact on networks with loops. Dechter and Pearl (1987) applied the cycle cutset to constraint networks, solving the remaining tree with directional arc consistency, and Dechter (1990) combined it with backjumping and learning inside backtracking search. Later work by Dechter and others on $w$-cutsets placed it at one end of a range of time and space trade-offs, with bucket elimination at the other end.

## References
