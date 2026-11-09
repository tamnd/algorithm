---
tag: G0H16E
kind: algorithm
slug: tree-structured-csp
name: Tree-structured CSP algorithm
aliases:
- Dechter-Pearl tree algorithm
- tree CSP solver
- directional arc consistency on trees
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Solves a CSP whose constraint graph is a tree in polynomial time by directional arc consistency and backtrack-free assignment.
model: word-ram
complexity:
  vars: {n: the number of variables, d: the largest domain size}
  time: {worst: O(n d^2)}
  space: {extra: O(n d)}
properties: {deterministic: true, exact: true, in_place: false, online: false, recursive: false}
history:
  year: 1987
  people: [Rina Dechter, Judea Pearl]
  note: Freuder (1982) proved that an arc consistent tree is backtrack-free along a parent-first order. Dechter and Pearl (1987) showed that arc consistency in one direction, from the leaves to the root, is enough, which gives O(n d^2) time.
prereqs: [arc-consistency, freuder-theorem, tree]
see_also: [cutset-conditioning, bucket-elimination, ac-3, constraint-graph, k-consistency, tree-decomposition, belief-propagation, breadth-first-search]
sources:
  - paper: doi:10.1145/322290.322292
    title: Eugene C. Freuder, A sufficient condition for backtrack-free search, Journal of the ACM 29(1), 1982
    locator: pages 24 to 32 (an arc consistent CSP whose constraint graph is a tree has a backtrack-free order)
  - paper: "Rina Dechter and Judea Pearl, Network-based heuristics for constraint-satisfaction problems, Artificial Intelligence 34(1), 1987, pages 1 to 38"
    locator: directional arc consistency, and its use to solve tree-structured networks in O(n d^2) time
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 4, Directional consistency (directional arc consistency and trees)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, 2020
    locator: Chapter 6, Section 6.5 (the structure of problems, and the TREE-CSP-SOLVER algorithm)
---

The tree-structured CSP algorithm solves a binary [constraint satisfaction problem](/constraint-satisfaction-problem/) whose [constraint graph](/constraint-graph/) is a [tree](/tree/), or a forest, in $O(n d^2)$ time. It roots each tree, makes each arc from a parent to a child consistent in one pass from the leaves up, and then assigns the variables from the root down, each time picking a value that agrees with the parent. By [Freuder's theorem](/freuder-theorem/) the second pass never gets stuck. A small change counts the solutions in the same time. Dechter and Pearl gave the directional form in 1987, and it is the base of [cutset conditioning](/cutset-conditioning/) and the simplest case of [bucket elimination](/bucket-elimination/).

## In plain words

Draw the rules as a tree: each unknown is a node, and each rule joins two nodes. Pick a root. Now go from the leaves towards the root. At each node, look at its parent and cross out each value of the parent that has no fitting value in the node. When you reach the root, every value that is left in a parent has a fitting value in each of its children.

Then go back down. Give the root any value that is left. For each child, the parent's value has a fitting partner, so pick one. Continue to the leaves. You never get stuck, so you never undo a choice. If a list of values becomes empty on the way up, there is no answer.

## The problem

The input is a binary CSP: variables $x_0, \ldots, x_{n-1}$, finite domains $D_v$ with $|D_v| \le d$, and binary constraints. A constraint on $x_u$ and $x_v$ is a relation $R_{uv} \subseteq D_u \times D_v$, and $R_{vu}$ is its converse. Constraints on the same pair are intersected first, and unary constraints are folded into the domains ([node consistency](/node-consistency/)). The constraint graph has an edge for each constrained pair, and here it must be a forest, so it has at most $n - 1$ edges.

The output is a solution, an assignment that satisfies every constraint, or the answer that none exists. The counting form returns the number of solutions.

Notation: $n$ variables, $d$ the largest domain size, $e \le n - 1$ edges. Cost is counted in constraint checks, the tests "is $(a, b) \in R_{uv}$?", in the word-RAM with a constant-time membership test.

## The algorithm

```pseudo id=main
TREE-CSP(D, R)                           ▷ the constraint graph is a forest
L1  if some D_v = ∅ then return NONE
L2  (order, parent) ← breadth-first order from a root in each tree
L3  for v in order, from last to first do               ▷ directional arc consistency
L4      if v has a parent p then
L5          D_p ← {a ∈ D_p : some b ∈ D_v has (a, b) ∈ R_pv}
L6          if D_p = ∅ then return NONE
L7  for v in order, from first to last do               ▷ backtrack-free assignment
L8      if v is a root then x_v ← any value of D_v
L9      else x_v ← any b ∈ D_v with (x_p, b) ∈ R_pv, where p = parent(v)
L10 return x

TREE-COUNT(D, R)                         ▷ number of solutions; same order and parent
L11 for v in order, from last to first, and each a ∈ D_v do
        W_v(a) ← ∏ over children c of v of Σ { W_c(b) : b ∈ D_c, (a, b) ∈ R_vc }
L12 return ∏ over roots r of Σ { W_r(a) : a ∈ D_r }
```

Line L2 lists each parent before its children. Line L3 visits the children before the parent, so when the arc $(p, v)$ is revised at line L5, all children of $v$ have been handled and $D_v$ does not change again. Only the arcs from a parent to a child are revised, never from a child to its parent; this is *directional* arc consistency. At line L9 the parent's value $x_p$ is in the final $D_p$, so it has a support in $D_v$, and line L9 always finds a value.

$W_v(a)$ is the number of assignments of the subtree of $v$ with $x_v = a$ that satisfy the constraints inside the subtree. A leaf has $W_v(a) = 1$, an empty product.

## Example

Take five variables $A, B, C, D, E$ with domains $\{1, 2, 3\}$ and the constraints $A < B$, $A \ne C$, $D < B$ and $E < C$. The graph is the tree with edges $\{A, B\}$, $\{A, C\}$, $\{B, D\}$ and $\{C, E\}$. With root $A$, the breadth-first order is $A, B, C, D, E$, and the parents are $B, C \to A$, $D \to B$, $E \to C$.

Upward pass (line L5), testing values in increasing order and stopping at the first support:

| step | arc revised | $D_p$ after | checks |
|---|---|---|---|
| 1 | $(C, E)$, needs $e < c$ | $D_C = \{2, 3\}$ | 5 |
| 2 | $(B, D)$, needs $d < b$ | $D_B = \{2, 3\}$ | 5 |
| 3 | $(A, C)$, needs $a \ne c$ | $D_A = \{1, 2, 3\}$ | 4 |
| 4 | $(A, B)$, needs $a < b$ | $D_A = \{1, 2\}$ | 5 |

Downward pass (lines L8 and L9), taking the smallest fitting value: $A = 1$; $B = 2$ since $1 < 2$; $C = 2$ since $2 \ne 1$; $D = 1$ since $1 < 2$; $E = 1$ since $1 < 2$. The solution is $(A, B, C, D, E) = (1, 2, 2, 1, 1)$, found with no backtracking.

Counting (lines L11 and L12) on the original domains: the leaves $D$ and $E$ have $W = 1$ for each value. $W_B(b)$ is the number of $d < b$, so $W_B = (0, 1, 2)$ for $b = 1, 2, 3$, and in the same way $W_C = (0, 1, 2)$. Then

- $W_A(1) = (W_B(2) + W_B(3)) \cdot (W_C(2) + W_C(3)) = 3 \cdot 3 = 9$,
- $W_A(2) = W_B(3) \cdot (W_C(1) + W_C(3)) = 2 \cdot 2 = 4$,
- $W_A(3) = 0$, as no $b > 3$ exists.

The CSP has $9 + 4 = 13$ solutions, which the tests confirm by brute force.

## Correctness

The upward pass deletes only values that occur in no solution: when $a$ is deleted from $D_p$, no value left in $D_v$ supports it, and every value already deleted from $D_v$ occurs in no solution by induction. So if line L6 returns NONE, there is no solution. Otherwise, after the pass, each value of each parent has a support in the final domain of each child. The downward pass then extends each partial assignment by one variable, and the only constraint between the new variable and the earlier ones is the one with its parent, because the graph is a forest. So the result satisfies every constraint. This is the case $k = 2$, width 1 of [Freuder's theorem](/freuder-theorem/), with one difference: the algorithm needs consistency of the arcs from parents to children only, not of all arcs.

For counting, a solution of the subtree of $v$ with $x_v = a$ is a choice, for each child $c$, of a value $b$ with $(a, b) \in R_{vc}$ and a solution of the subtree of $c$ with $x_c = b$. The subtrees of different children share no variable and no constraint, so the numbers multiply. The full proof is below.

## Complexity

**Time.** Line L1 and the breadth-first search take $O(n + e) = O(n)$ steps besides the domains. Line L5 runs once for each of the at most $n - 1$ edges and makes at most $|D_p| \cdot |D_v| \le d^2$ checks. Line L9 makes at most $d$ checks per variable. So TREE-CSP makes at most $(n - 1) d^2 + n d = O(n d^2)$ checks, and with constant-time checks this is its running time.

**Counting.** Line L11 does, for each edge $(v, c)$ and each pair $(a, b) \in D_v \times D_c$, one check and at most one addition, and one multiplication per edge and value. So it makes $O(n d^2)$ arithmetic operations. The counts can reach $d^n$, which needs $n \log_2 d$ bits, so on the word-RAM with $O(\log n)$-bit words each operation on these big numbers costs more; counting modulo a word-size number, or with floating point, stays at $O(n d^2)$.

**Space.** The order, the parents and the copies of the domains take $O(n d)$ space, and the counting tables $W_v$ take $O(n d)$ too, besides the input relations.

**Lower bound.** Deciding whether a single constraint on two variables allows any pair can need all $d^2$ checks: an adversary can answer "no" to each test until the last untested pair, so an algorithm that stops earlier cannot know the answer. The same argument as in the [AC-4](/ac-4/) optimality proof shows that the factor $d^2$ per edge cannot be avoided in the worst case.

## Properties

- **Exact and complete.** On a forest it finds a solution exactly when one exists.
- **Backtrack-free.** The second pass makes no choice that it undoes.
- **Not in place.** It works on copies of the domains; the input is not changed.
- **Order of the root.** Any root gives a correct answer. The solution found can depend on the root and on the value choice at lines L8 and L9.
- **All solutions.** After the upward pass, every value left at the root is part of a solution, but values left lower in the tree need not be, since a child's value may fit no value left in its parent. Full arc consistency (both directions) leaves exactly the values that occur in some solution.

## Variants and improvements

- **Full arc consistency.** Running [AC-3](/ac-3/) on a tree also gives a backtrack-free search along any parent-first order, but costs $O(n d^3)$. A second, downward pass of directional arc consistency, from the root to the leaves, gives full arc consistency in $O(n d^2)$; then each value left is in some solution.
- **Counting and optimization.** Replacing "some support exists" by a sum gives the number of solutions (TREE-COUNT), and replacing it by a minimum of costs solves weighted problems on trees. These are the sum-product and min-sum forms of [belief propagation](/belief-propagation/) on a tree.
- **Nearly trees.** [Cutset conditioning](/cutset-conditioning/) fixes a set of variables whose removal leaves a forest and calls this algorithm for each of their assignments. [Tree decompositions](/tree-decomposition/) group variables into bags that form a tree, and run the same two passes on the bags. [Bucket elimination](/bucket-elimination/) along an order of induced width 1 is this algorithm.
- **Non-binary constraints.** If the dual graph or a join tree of the hypergraph is a tree (an acyclic hypergraph), the same two passes on the constraints solve the CSP in time polynomial in the size of the relations.

## When to use it

Use it when the constraint graph is a forest, or after conditioning or decomposition has made it one. Many problems from configuration, scheduling with chain-like dependencies, and labelling along sequences have tree structure. For a general graph, test first whether it is a forest: a breadth-first search does that in $O(n + e)$ time. If it is not, use [cutset conditioning](/cutset-conditioning/) for a small cycle cutset, [bucket elimination](/bucket-elimination/) for small induced width, or search with [maintaining arc consistency](/maintaining-arc-consistency/).

## Pitfalls

- **Revising in the wrong direction.** The upward pass must delete values of the parent that have no support in the child. Deleting values of the child that have no support in the parent leaves parents with values that cannot be extended.
- **Wrong order.** A child's arc must be revised after all arcs below the child. Revising in breadth-first order instead of its reverse can leave a parent value whose only support is deleted later.
- **A graph with a cycle.** The algorithm is wrong on a cycle: the downward pass ignores constraints that close a cycle. The implementation checks that the number of edges is at most $n - 1$ and that the search finds no cycle.
- **Two constraints on one pair.** They form a cycle of length 2 in a multigraph view. Intersect them into one relation first.
- **Disconnected graphs.** Each tree of a forest needs its own root. A count must multiply the counts of the trees.
- **Big counts.** The number of solutions grows like $d^n$. Use big integers, or count modulo a prime when an exact count is not needed.

## Implementations

## History

Freuder (1982) defined the width of a constraint graph and showed that an arc consistent CSP whose graph is a tree can be solved without backtracking. Dechter and Pearl (1987) noted that arc consistency in one direction is enough, which gives the $O(n d^2)$ algorithm, and built on it adaptive consistency and the cycle cutset method. The same two-pass scheme on trees appears in Pearl's belief propagation for probabilistic networks, and in dynamic programming on trees in general.

## References
