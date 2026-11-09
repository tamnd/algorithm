---
tag: D70D3M
kind: algorithm
slug: paterson-wegman-unification
name: Paterson-Wegman linear unification
aliases:
- linear-time unification
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Linear-time unification of terms represented as shared DAGs.
solves: [unification-problem]
model: word-ram
complexity:
  vars: {N: the number of nodes plus the number of edges of the term DAG}
  time: {worst: O(N)}
  space: {extra: O(N)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1978
  people: [Michael S. Paterson, Mark N. Wegman]
  note: Paterson and Wegman published "Linear unification" in the Journal of Computer and System Sciences in 1978, the first unification algorithm with a linear worst-case bound.
prereqs: [unification-problem, term-dag, most-general-unifier, depth-first-search]
see_also: [martelli-montanari-unification, robinson-unification, occurs-check, mgu-existence-theorem, topological-sort, cycle-detection, congruence-closure]
sources:
  - paper: "M. S. Paterson and M. N. Wegman, Linear unification, Journal of Computer and System Sciences 16(2), 1978, pages 158 to 167"
    locator: the algorithm with the procedure FINISH, its pointers and complete marks, and the proof of the linear bound
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.8, Unification of term graphs
  - paper: "Kevin Knight, Unification: a multidisciplinary survey, ACM Computing Surveys 21(1), 1989, doi:10.1145/62029.62030"
    locator: the section on the Paterson-Wegman linear algorithm and its comparison with the union-find algorithms
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (efficient syntactic unification on term DAGs and its complexity)
---

The Paterson-Wegman algorithm solves the [unification problem](/unification-problem/) in time linear in the size of the input, stored as a [term DAG](/term-dag/). It finds the classes of nodes that a unifier must make equal, and it finishes each class only after the classes above it are finished. This order makes the [occurs check](/occurs-check/) free: a cycle shows up as a class that is reached again while it is still open. The result is a [most general unifier](/most-general-unifier/) in triangular form, of linear size. Michael Paterson and Mark Wegman published it in 1978. It is optimal in theory, but the almost linear [union-find algorithm](/martelli-montanari-unification/) is simpler and often as fast.

## In plain words

Store both patterns in one shared drawing, where each blank appears once and equal parts are drawn once. Draw a line between the two tops: they must become equal. Two parts that must be equal and start with the same symbol make their pieces equal too, so draw lines between the pieces.

Now collect groups of parts joined by lines. Before you close a group, close every group that sits above it in the drawing, because those groups can still add lines to this one. If a group you need is already open further up the chain, the pattern would have to contain itself, so stop. If a group has two different symbols, stop. Each part is handled once and each line is read twice, so the work grows only in step with the size of the drawing.

## The problem

The input is a term DAG $G$ with two nodes $u$ and $v$. Each variable is a single node, and each function node $f(c_1, \ldots, c_k)$ has ordered children and a list of parents. Notation: $N$ is the number of nodes plus the number of edges of $G$, $n$ the number of variable nodes, $\sigma, \theta$ are substitutions and $t\sigma$ is the application of $\sigma$ to $t$. The output is a most general unifier of the terms of $u$ and $v$, given as bindings from variable nodes to nodes, or FAIL. Two tree terms are turned into such a DAG by [hash-consing](/hash-consing/) in linear expected time.

## The algorithm

Each node has an undirected list of **equality edges**, a pointer $\mathrm{ptr}$ to the root of its class (unset at first) and a mark **complete**. FINISH$(r)$ collects the class of $r$ by a search over equality edges. Before it reads the edges of a member, it finishes every parent of that member.

```pseudo id=main
UNIFY(G, u, v)
L1  add the equality edge {u, v}
L2  for each function node r: if r is not complete then FINISH(r)
L3  for each variable node r: if r is not complete then FINISH(r)
L4  return the bindings                      ▷ triangular mgu on G

FINISH(r)
L5  if ptr(r) is set then FAIL                ▷ r is open further up: a cycle
L6  ptr(r) ← r; push r on a stack S; M ← [r]
L7  while S is not empty do
L8      s ← pop S
L9      if s and r are function nodes with different symbols or arities then FAIL   ▷ clash
L10     for each parent p of s: if p is not complete then FINISH(p)
L11     for each equality edge {s, t} do
L12         if ptr(t) is unset then ptr(t) ← r; push t on S; append t to M
L13         else if ptr(t) ≠ r then FAIL      ▷ a cycle through two open classes
L14     if s is a variable and s ≠ r then bind s ↦ r
L15     else if s ≠ r then add the equality edges {childᵢ(r), childᵢ(s)} for each i
L16 mark every node of M complete
```

Line L2 runs before L3, so a class that contains a function node is always started from a function node, and its root $r$ is a function node. Line L15 is decomposition: two function nodes of one class must agree on their children. Line L14 binds the variables of a class to its root. The implementation below replaces the recursion of L10 with an explicit stack of generators.

## Example

Unify $s = f(x_1, h(x_1), x_2)$ and $t = f(g(x_3), x_4, x_3)$. The DAG has the nodes

| node | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| term | $x_1$ | $h(0)$ | $x_2$ | $f(0, 1, 2)$ | $x_3$ | $g(4)$ | $x_4$ | $f(5, 6, 4)$ |

and L1 adds the edge $\{3, 7\}$. The trace:

1. L2 takes node 1. FINISH(1) pops 1, and L10 finds the parent 3, which is not complete, so it calls FINISH(3).
2. FINISH(3) pops 3, follows the edge to 7, and pops 7. Both are $f$ nodes, so L15 adds the edges $\{0, 5\}$, $\{1, 6\}$ and $\{2, 4\}$. The class $\{3, 7\}$ is complete.
3. Back in FINISH(1), L11 follows the new edge to 6. Node 6 is $x_4$, so L14 binds $x_4 \mapsto 1$. The class $\{1, 6\}$ is complete.
4. L2 takes node 5. FINISH(5) follows the edge to 0 and binds $x_1 \mapsto 5$. The class $\{5, 0\}$ is complete.
5. L3 takes node 2. FINISH(2) follows the edge to 4 and binds $x_3 \mapsto 2$. The class $\{2, 4\}$ is complete.

The bindings $\{x_4 \mapsto h(x_1),\ x_1 \mapsto g(x_3),\ x_3 \mapsto x_2\}$ are in triangular form. Expanded, they give the idempotent mgu $\{x_1 \mapsto g(x_2),\ x_3 \mapsto x_2,\ x_4 \mapsto h(g(x_2))\}$. [Robinson's algorithm](/robinson-unification/) gives $\{x_1 \mapsto g(x_3),\ x_2 \mapsto x_3,\ x_4 \mapsto h(g(x_3))\}$ on the same input, which is the same mgu up to the renaming that swaps $x_2$ and $x_3$.

**A cycle.** For $f(x, y) \doteq f(g(y), g(x))$, the nodes are $x$, $y$, $f(x, y)$, $g(y)$, $g(x)$ and $f(g(y), g(x))$. Finishing the class of the two $f$ nodes adds the edges $\{x, g(y)\}$ and $\{y, g(x)\}$. FINISH on $g(y)$ first finishes its parents, which are complete, then reaches $x$ through the new edge. Before it reads the edges of $x$, L10 calls FINISH on the parent $g(x)$ of $x$. That call reaches $y$, and L10 calls FINISH on the parent $g(y)$ of $y$, which already has a pointer and is not complete. Line L5 returns FAIL.

**The exponential example.** For $f(x_1, \ldots, x_n) \doteq f(g(x_0, x_0), \ldots, g(x_{n-1}, x_{n-1}))$, the DAG has $2n + 3$ nodes, and the algorithm returns $n$ bindings $x_i \mapsto g(x_{i-1}, x_{i-1})$. It runs in linear time, while the expanded mgu has $2^{n+2} - n - 4$ symbols.

## Correctness

A unifier $\theta$ must make equal every pair of nodes in the least equivalence $\equiv$ that contains $(u, v)$ and is closed under decomposition. So $u$ and $v$ are unifiable exactly when no class of $\equiv$ has two different function symbols and the graph of classes (a class points to the classes of the children of its function nodes) has no cycle. In that case, binding each variable to its class, read as a term, is an idempotent mgu, by a size argument for the cycles and an induction along the class graph for generality. The algorithm computes the classes of $\equiv$ exactly: every equality edge joins two equivalent nodes, and the order of L10 makes sure that no edge reaches a class after it is complete. The classes complete in a topological order of the class graph, so a cycle forces a call of FINISH on an open class, which L5 or L13 reports. The full proof is below.

## Complexity

- **Time $O(N)$.** Each node gets a pointer once, so it is pushed and popped once. L10 reads each parent list once, which costs one step per DAG edge. L15 adds at most $k$ equality edges for each function node of arity $k$, so there are at most one more equality edge than DAG edges, and L11 reads each twice.
- **Space $O(N)$.** The pointers, marks, equality edges and the stack.
- **Input conversion.** If the input is two trees of total size $N$, building the DAG with a hash table costs $O(N)$ expected time, or $O(N \log N)$ with a balanced search tree. Sharing of function nodes is not needed: two trees whose variables are numbered $1, \ldots, n$ become a valid DAG in linear time with no hash table, by making each variable one node.
- **Output.** The bindings have size $O(n)$, and the mgu in triangular form has size $O(N)$. Expanding it into explicit trees can take exponential space; this is a property of the output, not of the algorithm.

## Properties

- **Linear time in the worst case.** It is the first unification algorithm with this bound, and the bound is optimal, since the input must be read.
- **Built-in occurs check.** No separate test is needed: the order of completion is a [topological sort](/topological-sort/) of the class graph, and a cycle is found when it closes.
- **Triangular output.** Variables are bound to nodes, not to copied terms.
- **Recursive.** FINISH calls itself on parents. The depth of recursion can be linear, so an explicit stack is safer.

## Variants and improvements

- **Union-find unification.** Huet's algorithm (1976), the efficient form of the [Martelli-Montanari algorithm](/martelli-montanari-unification/), merges classes with a disjoint-set forest and checks for cycles once at the end. It takes $O(N\,\alpha(N))$ time and has smaller constants.
- **Rational trees.** Remove the failure of L5 and L13, and finish classes in any order. The result is unification without the occurs check, in linear time.
- **Matching.** For [term matching](/term-matching/), one side has no variables, and a simpler linear algorithm suffices.
- **Congruence closure.** [Congruence closure](/congruence-closure/) is the upward dual: it merges parents when their children are merged. Its linear-time methods use similar ideas of classes and pending edges.

## When to use it

Use it when a worst-case linear bound matters, for example in a complexity proof that calls unification as a subroutine, or for very large shared terms. In most provers and Prolog systems, terms are small and bindings are kept in place, so a recursive algorithm in the style of [Robinson](/robinson-unification/) or a union-find algorithm is usually preferred: the extra parent lists, edge lists and marks of the linear algorithm cost more than they save on small terms.

## Pitfalls

- **Variables must be shared.** Each variable must be a single node. Two separate nodes for $x$ break the algorithm, because the class structure then does not see that both copies must be equal.
- **Order of the two passes.** L2 must finish all function nodes before L3 starts on variable nodes. Otherwise a class can get a variable as root, and its function nodes are not checked against each other.
- **Parents first.** The calls of L10 must run before the edges of $s$ are read at L11. This is what lets the algorithm detect cycles without a separate test.
- **Deep recursion.** A long chain of parents gives deep recursion; use an explicit stack.

## Implementations

## History

Michael S. Paterson and Mark N. Wegman published "Linear unification" in the Journal of Computer and System Sciences in 1978. Their algorithm was the first to unify in linear time in the worst case, after Robinson's exponential algorithm of 1965 and Huet's almost linear union-find algorithm of 1976. Martelli and Montanari (1982) gave another efficient algorithm, and in 1984 Dwork, Kanellakis and Mitchell showed that unification is complete for P, so a linear sequential bound is unlikely to have a fast parallel counterpart.

## References
