---
tag: 4S8GH7
kind: algorithm
slug: lazy-abstraction
name: Lazy abstraction with interpolants
aliases:
- Lazy abstraction
- Abstract reachability tree refinement
area: logic-and-constraints/model-checking
level: research
summary: Unwind a program into an abstract reachability tree, and on a spurious error path add interpolant predicates only at its locations and rebuild only the affected subtree.
solves: [invariant-checking]
model: word-ram
complexity:
  vars: {L: the number of program locations, E: the number of control-flow edges, V: the number of data valuations}
  time: {total: 2^O(V) · (L E)^O(1)}
  space: {total: 2^O(V) · (L E)^O(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 2002
  people: [Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, Grégoire Sutre, Kenneth L. McMillan]
  note: Henzinger, Jhala, Majumdar and Sutre introduced lazy abstraction in the BLAST model checker at POPL 2002. Interpolants for local predicates followed at POPL 2004, and McMillan's interpolant-only version at CAV 2006.
prereqs: [cegar, predicate-abstraction, inductive-invariant, invariant-checking]
see_also: [interpolation-based-model-checking, cegar, predicate-abstraction, weakest-precondition, hoare-logic, abstract-interpretation, depth-first-search, counterexample-generation]
sources:
  - paper: doi:10.1145/503272.503279
    title: Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar and Grégoire Sutre, Lazy abstraction, POPL 2002
    locator: pages 58 to 70 (the abstract reachability tree, on-the-fly refinement from the pivot node, location-local predicates, covering, and BLAST)
  - paper: doi:10.1145/964001.964021
    title: Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar and Kenneth L. McMillan, Abstractions from proofs, POPL 2004
    locator: pages 232 to 244 (Craig interpolants along a spurious path as new predicates, each added only at its own location)
  - paper: doi:10.1007/11817963_14
    title: Kenneth L. McMillan, Lazy abstraction with interpolants, CAV 2006, LNCS 4144
    locator: pages 123 to 136 (the unwinding with interpolant labels, covering, and the proof that a complete well-labelled unwinding is a safety proof)
---

Lazy abstraction checks that an error location of a program is unreachable. It is a form of [CEGAR](/cegar/) that refines only where it must. It unwinds the control-flow graph into an *abstract reachability tree*: each node is a program location with an abstract region of data values, computed with [predicate abstraction](/predicate-abstraction/) from the region of its parent. A node is *covered* when an expanded node at the same location already has a larger region; covered nodes are not expanded. When the tree reaches the error location, the path to it is checked on the concrete program. If the path is feasible, it is a real bug. If it is spurious, a sequence of *interpolants* along the path proves it infeasible. Each interpolant is added as a predicate only at its own location, and only the subtree below the first node that the new predicates cut, the *pivot*, is rebuilt. The rest of the tree, and the predicates at other locations, stay as they were. Henzinger, Jhala, Majumdar and Sutre introduced lazy abstraction in BLAST in 2002; interpolants for finding predicates came in 2004, and McMillan's version that uses interpolants directly as node labels in 2006.

## In plain words

We want to show that a program never reaches a crash point. We explore the program as a tree of program points, and at each point we keep a rough description of the data, such as "x is not 3". Rough descriptions keep the tree small.

When the tree reaches the crash point, we replay the path on real data. If the replay works, we have a real bug. If not, we learn a fact for each point on the path, such as "here x is not 3", that explains why the replay fails. We add each fact only at its own point, and redo only the part of the tree below the first point that the facts change.

When every open branch is closed or repeats a branch already seen, the descriptions in the tree prove that the crash point is unreachable.

## The problem

A program is a control-flow automaton: a finite set of locations, a start location $l_0$ with a set of initial data valuations, an error location $l_E$, and edges $(l, \rho, l')$ where $\rho$ is a relation on data valuations. The task is [invariant checking](/invariant-checking/) for the property "the location $l_E$ is unreachable". A safety proof is an [inductive invariant](/inductive-invariant/) given per location, a region $\psi_l$ of valuations for each location $l$, with the initial valuations in $\psi_{l_0}$, $\mathrm{post}_\rho(\psi_l) \subseteq \psi_{l'}$ for each edge, and $\psi_{l_E}$ empty. This is the form of a [Hoare logic](/hoare-logic/) annotation of the program.

Each location $l$ has a list of predicates $\Pi_l$. The abstraction $\alpha_l(X)$ of a set $X$ of valuations is the union of the cells of $\Pi_l$ that meet $X$, where a cell is a set of valuations that agree on all predicates of $\Pi_l$. So $X \subseteq \alpha_l(X)$.

## The algorithm

```pseudo id=main
LAZY-ABSTRACTION(program)
L1  root ← a node at l_0 with region α_l0(Init); W ← {root}
L2  while W is not empty do
L3      n ← remove a node from W                                 ▷ depth-first here
L4      if n is dead, expanded, covered, or has an empty region then continue
L5      if loc(n) = l_E then
L6          if the path root ... n is feasible concretely then return UNSAFE, with the trace
L7          compute interpolants φ_0, ..., φ_k along the path; add φ_i to Π at the location of the i-th node
L8          pivot ← the first node on the path whose region meets ¬φ_i; delete its subtree, recompute its region, put it in W
L9      else if an expanded live node m at loc(n) has region(n) ⊆ region(m) then mark n covered by m
L10     else expand n: for each edge (loc(n), ρ, l') add a child at l' with region α_l'(post_ρ(region(n))) to W
L11 return SAFE, with ψ_l = the union of the regions of the live nodes at l
```

Line L8 also uncovers every node that was covered by a deleted node and puts it back in W.

For a spurious path $l_0 \xrightarrow{\rho_1} l_1 \cdots \xrightarrow{\rho_k} l_E$, an *interpolant sequence* is a list of formulas $\varphi_0, \ldots, \varphi_k$ with $\mathit{Init} \subseteq \varphi_0$, $\mathrm{post}_{\rho_{i+1}}(\varphi_i) \subseteq \varphi_{i+1}$, and $\varphi_k$ empty. SMT solvers compute such sequences from a refutation of the path formula. The implementation here works on a small finite data domain, so it can use the weakest sequence exactly: $\neg\varphi_i$ is the set of valuations from which the rest of the path can still run to $l_E$, computed by pre-images from the end.

## Example

The program has one variable $x \in \{0, 1, 2, 3\}$, with any initial value.

```text
L0: x := 0
L1: while x < 2: x := x + 1
L2: if x == 3: goto L3      (L3 is the error location)
```

There are no predicates at first, so every region is the full set $\{0, 1, 2, 3\}$.

1. The root $n_0$ at L0 has a child $n_1$ at L1. $n_1$ has two children: $n_2$ at L1 for the loop body, and $n_3$ at L2 for the loop exit. Depth-first search expands $n_3$, and its child $n_4$ at L3 is an error node.
2. The path $L0 \to L1 \to L2 \to L3$ is infeasible: after $x := 0$ the exit test $x \ge 2$ fails. The pre-images from the end give the valuations that can still reach the error: all of them at L3, $\{3\}$ at L2, $\{3\}$ at L1, and none at L0. So the predicate $x = 3$ is added at L1 and at L2 only.
3. The first node whose region meets one of these sets is $n_1$, whose region contains 3. It becomes the pivot. Its subtree is deleted, and its region becomes $\alpha_{L1}(\{0\}) = \{0, 1, 2\}$, the cell where $x \ne 3$.
4. $n_1$ is expanded again. The loop child has the region $\alpha_{L1}(\{1, 2\}) = \{0, 1, 2\}$. The exit child at L2 has the region $\{0, 1, 2\}$, and its child at L3 has the empty region, since no $x \ne 3$ passes the test $x = 3$. The loop child is covered by $n_1$.

The work list is empty after one refinement. The invariant is $\psi_{L0} = \{0, 1, 2, 3\}$, $\psi_{L1} = \psi_{L2} = \{x \ne 3\}$, and $\psi_{L3} = \emptyset$. The predicate $x = 3$ is never needed at L0, and the node at L0 is never rebuilt. If the loop test is changed to $x < 3$, the method returns the real trace $x = 0, 1, 2, 3$ that ends at L3.

## Correctness

**UNSAFE is sound.** The trace comes from a concrete execution of the path.

**SAFE is sound.** When the work list is empty, each live node with a nonempty region that is not at $l_E$ is either expanded, with a live child for each edge whose region contains the post of its own region, or covered by a live expanded node with a larger region. Live nodes at $l_E$ have empty regions, since a nonempty one would have caused a refinement. So the union of the regions per location contains the initial valuations, is closed under every edge, and is empty at $l_E$: it is an inductive invariant.

**Progress and termination.** The pivot's new region is disjoint from the set of valuations that can still reach the error along the path, while its old region met that set. So the same spurious path cannot come back below the pivot. For finite data domains, there are finitely many predicates per location, and between refinements the live expanded nodes have pairwise different pairs of location and region, so the tree stays finite. The full proof is below. For programs over integers, the method is sound but need not terminate.

## Complexity

All bounds here are worst-case bounds for the finite form above, with $V$ data valuations. A location has at most $2^V$ predicates and at most $2^V$ regions, so at most $L \cdot 2^V$ live expanded nodes, at most $E \cdot L \cdot 2^V + 1$ live nodes, and the number of refinements is bounded by the same kind of quantity. Each step is polynomial in these numbers, so the time and space are $2^{O(V)} \cdot (L E)^{O(1)}$. In real programs $V$ is itself exponential in the number of bits of the data, and each abstract post is a set of SMT or SAT queries. The practical cost depends on how few predicates the interpolants give, which is a measured property of the tool, not a bound.

## Properties

- **Lazy in two ways.** Predicates are added only where a spurious path needs them, and only the subtree below the pivot is rebuilt.
- **Location-local predicates.** Different locations have different predicate sets, which keeps each abstract post small. A global predicate set, as in classical predicate abstraction, grows with every refinement.
- **Sound both ways.** SAFE comes with a per-location inductive invariant; UNSAFE with a concrete trace.
- **Depends on the interpolants.** Strong or weak interpolants give different predicates and different trees. The weakest sequence used here always works on finite domains, but it can be large.

## Variants and improvements

- **BLAST.** Henzinger, Jhala, Majumdar and Sutre (2002) found new predicates by an analysis of the spurious path with a theorem prover, in their model checker BLAST. Henzinger, Jhala, Majumdar and McMillan (2004) used Craig interpolants of the path formula, one per location, as in the implementation here.
- **Interpolants as labels (IMPACT).** McMillan (2006) drops predicate abstraction. Each node is labelled with a formula; a spurious path strengthens the labels along it by conjunction with interpolants. Covering must then be undone when a label of a covering node gets stronger. This avoids the cost of the abstract post.
- **Large-block encoding and adjustable precision.** Later tools, such as CPAchecker by Beyer and others, merge loop-free blocks into single edges and combine lazy abstraction with other analyses.
- **Compared with eager CEGAR.** [CEGAR](/cegar/) with a global abstraction rebuilds the whole abstract model after each refinement. Lazy abstraction rebuilds only a subtree.

## When to use it

Use lazy abstraction for safety properties of sequential programs, such as assertion checks in C code, where the proof needs a few facts at a few program points. It works less well for properties that need many relations between variables at every location, or for deep loops that need loop invariants that interpolants do not find; there [abstract interpretation](/abstract-interpretation/) with widening, or [IC3](/ic3-pdr/) on the control-flow graph, can do better.

## Pitfalls

- **Rebuilding from the wrong node.** The pivot is the first node whose region meets the new interpolant's complement. Rebuilding from a later node leaves an earlier region too coarse, and the same spurious path comes back.
- **Stale covers.** When a covering node is deleted or its region shrinks, the nodes it covered must be uncovered and checked again. If not, SAFE is unsound.
- **Global predicates by accident.** Adding each interpolant at every location loses the main benefit, and the abstract post becomes as costly as in eager predicate abstraction.
- **Infinite unwinding.** With infinite data domains the tree may keep growing, because each refinement can produce new predicates, for example $x = 1$, $x = 2$, and so on, for a loop counter.

## Implementations

## History

Henzinger, Jhala, Majumdar and Sutre (POPL 2002) introduced lazy abstraction and the model checker BLAST, which checked device drivers. Henzinger, Jhala, Majumdar and McMillan (POPL 2004) used Craig interpolants of the spurious path formula to find location-local predicates. McMillan (CAV 2006) gave the interpolant-labelled unwinding, implemented in the tool IMPACT. The ideas carried over to later software model checkers, including CPAchecker.

## References
