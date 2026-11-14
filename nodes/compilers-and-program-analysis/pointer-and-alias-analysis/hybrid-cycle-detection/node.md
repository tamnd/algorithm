---
tag: NC36D7
kind: algorithm
slug: hybrid-cycle-detection
name: Lazy and hybrid cycle detection
aliases:
- Hardekopf-Lin cycle detection
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: research
summary: Looks for constraint cycles only when an edge brings no new points-to facts, plus an offline pass, making Andersen's analysis scale.
solves: [points-to-analysis]
model: word-ram
complexity:
  vars: {n: the number of variables (each variable is also a location), m: the number of pointer statements}
  time: {worst: O(n^4 + n^2 m)}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, recursive: false, online: true, flow_sensitive: false, context_sensitive: false}
history:
  year: 2007
  people: [Ben Hardekopf, Calvin Lin]
  note: Hardekopf and Lin gave lazy cycle detection, which searches only when an edge carries a set equal to its target's, and hybrid cycle detection, which plans merges with an offline pass.
prereqs: [strongly-connected-components, tarjan-scc, online-cycle-elimination]
see_also: [offline-variable-substitution, andersen-analysis, steensgaard-analysis, bdd-points-to-analysis, points-to-analysis, field-sensitivity]
sources:
  - paper: doi:10.1145/1250734.1250767
    title: Ben Hardekopf and Calvin Lin, The ant and the grasshopper, fast and accurate pointer analysis for millions of lines of code, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '07), 290 to 299, 2007
    locator: whole paper (lazy cycle detection, hybrid cycle detection with its offline graph of ref nodes, and the measurements on large C programs)
  - paper: doi:10.1145/277650.277667
    title: Manuel Fähndrich, Jeffrey S. Foster, Zhendong Su and Alexander Aiken, Partial online cycle elimination in inclusion constraint graphs, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '98), 85 to 96, 1998
    locator: whole paper (online cycle elimination, the method that lazy detection makes cheaper)
  - paper: doi:10.1145/349299.349310
    title: Atanas Rountev and Satish Chandra, Off-line variable substitution for scaling points-to analysis, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2000), 47 to 56, 2000
    locator: the offline pass over the copy graph, used before the solver
---

Lazy and hybrid cycle detection are two ways to find the cycles of the constraint graph of [Andersen's analysis](/andersen-analysis/) at a low cost, so that the nodes of each cycle can be merged. All nodes on a cycle must end with the same points-to set, and merging them saves the solver from moving each fact around the cycle. [Online cycle elimination](/online-cycle-elimination/) searches for a cycle at each new edge, which costs much. *Lazy cycle detection* (LCD) searches only when an edge would carry a set that is already equal to the set at its target, since that is what a cycle looks like once the facts have gone around it. *Hybrid cycle detection* (HCD) looks at the statements before solving and finds cycles that go through loads and stores. It records which merges to do once the targets of the pointers are known, and then does them with no search. Hardekopf and Lin (2007) gave both and used them to analyse C programs of over a million lines.

## In plain words

Andersen's analysis passes lists of addresses along arrows from pointer to pointer. When arrows go around a circle, every pointer on it ends with the same list, so the circle can become one pointer. Looking for circles after every new arrow is slow. The lazy method waits for a sign: an arrow whose two ends already have the same list. Only then does it look for a circle through that arrow, and it looks only once per arrow. The hybrid method reads the program first. A circle that passes through a read or write via a pointer only appears once that pointer gets a target. The method notes in advance which merges such targets will cause, and it does them as soon as the targets appear. The final lists are those of Andersen's analysis.

## The problem

The input is a set of statements in the four basic forms `p = &a`, `p = q`, `p = *q` and `*p = q` over $n$ variables, and the output is the least solution $L$ of the subset constraints of Andersen's analysis, as on the page of the [points-to analysis](/points-to-analysis/) problem. The order is the subset order on each set, with the empty sets at the bottom, in the direction of Cousot. The analysis is flow-insensitive: it ignores the order of the statements, not the statements that the control flow gives.

If the solver's graph has a path from $u$ to $v$, then $L(u) \subseteq L(v)$, so $L$ is the same on a cycle. Many cycles only appear while the solver runs: a load `p = *q` gives the edge $a \to p$ only when $a$ enters the set of $q$. The *offline graph* shows them in advance. It has a node $v$ and a *ref node* $*v$ for each variable, which stands for every target of $v$, and the edges

| statement | offline edge |
|---|---|
| `p = q` | $q \to p$ |
| `p = *q` | $*q \to p$ |
| `*p = q` | $q \to *p$ |

A cycle of the offline graph through $*a$ and a variable $b$ becomes a real cycle through $x$ and $b$ for each target $x$ of $a$, once the other ref nodes on the cycle have targets too.

## The algorithm

The offline part is lines L1 to L4. The solver is the worklist solver of Andersen's analysis over the roots of a union-find forest, with the hybrid merges in lines L8 and L9 and the lazy check in lines L12 to L14.

```pseudo id=main
HYBRID(S)
L1  G <- the offline graph of S; find its strongly connected components
L2  merge the variables of each strongly connected component of the copy edges alone
L3  for each component C of G with a ref node and a variable node b do
L4      for each *a in C do add (b, the pointers of the other ref nodes of C) to H[a]
L5  set up the sets, edges, loads and stores as in Andersen's analysis; W <- the roots with a non-empty set
L6  while W is not empty do
L7      take n from W; if FIND(n) is not n then go to the next n
L8      for each (b, R) in H[n] such that pts[FIND(c)] is not empty for every c in R do
L9          for each x in pts[n] do MERGE(x, b)
L10     for each x in pts[n] do add the edges of the loads and stores of n for x
L11     for each w in succ[n] do
L12         if pts[w] = pts[n] and the edge n -> w was never checked then
L13             mark it checked; C <- the roots on some path from w to n
L14             if C is not empty then MERGE all of C; go to the next w
L15         copy pts[n] into pts[w]; if it grew, add w to W
L16 return pts[FIND(v)] for each variable v
```

MERGE joins the classes in the union-find forest, takes the union of their sets, edges, loads, stores and table entries, and puts the new root on the worklist. Line L2 merges only cycles of copies; the variable nodes of a component with ref nodes are not merged offline, since their cycle may need a pointer that never gets a target. The lazy check runs at most once per edge, so a cycle that it misses at one time is not searched for again on that edge.

## Example

The program, in the toy IR:

```
entry:
  a = &x
  a = &y
  b = *a
  c = b
  *a = c
  y = &z
  ret 0
```

The offline graph has the edges $*a \to b$ (from the load), $b \to c$ (from the copy) and $c \to *a$ (from the store). They form the component $\{*a, b, c\}$, so line L4 records $H[a] = \{(b, \emptyset)\}$: every target of $a$ will be on a cycle with $b$. There is no cycle of copies alone.

| step | lines | what happens |
|---|---|---|
| 1 | L5 | $pts(a) = \{x, y\}$, $pts(y) = \{z\}$, the copy edge $b \to c$; the worklist is $a, y$ |
| 2 | L8, L9 | take $a$: the entry $(b, \emptyset)$ applies, so $x$ and then $y$ merge into $b$; $pts(b) = \{z\}$, from $y$ |
| 3 | L10 | the load adds $x \to b$ and $y \to b$, which are now inside one node; the store `*a = c` adds $c \to b$ |
| 4 | L7 | take $y$: not a root, so skip it |
| 5 | L15 | take $b$: along $b \to c$, $pts(c) = \{z\}$ |
| 6 | L12 to L14 | take $c$: the edge $c \to b$ carries $\{z\}$ and $pts(b) = \{z\}$ already, so search from $b$ for $c$; the path $b \to c$ closes a cycle, and $c$ merges into $b$ |
| 7 | L11 | take $b$: no edges are left |

The result is $pts(a) = \{x, y\}$ and $pts(b) = pts(c) = pts(x) = pts(y) = \{z\}$, which is Andersen's least solution. The run made two hybrid merges, one lazy merge, and one search. The hybrid merges put $x$ and $y$ into one node before any fact went around the cycle.

## Correctness

The full proof is in the proof file. Its steps:

1. **An offline path gives inclusions.** Replace each ref node $*c$ on a path of the offline graph by a location in $L(c)$. Then each edge becomes a true inclusion of least sets: a copy, a load from that location, or a store into it.
2. **Every merge joins nodes with one least set.** Copy cycles share their set. A hybrid merge of $x \in pts(a)$ with $b$ happens only when every other ref node of the component has a target; then the two paths between $b$ and $*a$ in the component, with $x$ for $*a$, give $L(b) \subseteq L(x) \subseteq L(b)$. A lazy merge joins nodes on a cycle of the solver's edges, which are true inclusions.
3. **What is done stays done.** A root that is not on the worklist has all the edges for its loads and stores, and its set is inside the set of each successor.
4. **At the end, the sets are $L$.** They form a solution, so they contain $L$, and every set stays inside $L$ by step 2.

The proof never needs a merge to happen. So the lazy check can miss cycles, and the result is still exact.

## Complexity

**Proved.** The offline part takes $O(n + m)$ time, with [Tarjan's algorithm](/tarjan-scc/) on a graph of $2n$ nodes and $m$ edges. The solver takes $O(n^4 + n^2 m)$ time in the worst case, with each find counted as one step: each root goes back on the worklist $O(n)$ times, there are at most $n^2$ lazy searches of $O(n^2)$ time each, and the table costs $O(n^2)$ per visit of a root. The space is $O(n^2 + m)$. The method does not lower the worst case of Andersen's analysis, which is $O(n^3)$ with difference propagation.

**Stated in the paper, not proved here.** Hardekopf and Lin report that LCD and HCD together, with offline variable substitution and difference propagation, analyse C programs of over a million lines, and that they are faster than the earlier cycle detection methods that they compare with, including online cycle elimination and the methods of Heintze and Tardieu and of Pearce, Kelly and Hankin. They also report that HCD costs little and can be added to other solvers, including solvers based on BDDs.

**Measured, not proved.** On the 300 seeded random programs of the test file, of up to 12 variables and 30 statements, with 1809 variables in all, the solver made 158 offline merges, 101 hybrid merges and 320 lazy merges, with 292 searches. The result equals Andersen's least solution in each of the four modes, with or without the lazy and the offline parts. With the condition of line L8 dropped, 2 of 1000 random programs got sets larger than Andersen's.

## Properties

- **Same result as Andersen's analysis.** Every merge joins nodes with equal least sets.
- **Few searches.** A search runs only on an edge that carries no new facts, and at most once per edge.
- **Merges with no search.** The hybrid merges need only the table lookup of line L8.
- **Incomplete.** Neither part finds every cycle. The proof does not need them to.
- **Works with other methods.** It adds to [offline variable substitution](/offline-variable-substitution/), to difference propagation, and to [BDD-based solvers](/bdd-points-to-analysis/).

## Variants and improvements

- **Online cycle elimination.** [Online cycle elimination](/online-cycle-elimination/) searches at every new edge; it finds more cycles earlier, at a much higher cost per edge.
- **Hash-based value numbering.** Hardekopf and Lin (SAS 2007) extended offline substitution so that it also finds pointers that are equal through loads, which shrinks the graph before LCD and HCD run.
- **Wave and deep propagation.** Later solvers by Pereira and Berlin (2009) propagate in topological order of the collapsed graph and run cycle detection between waves.
- **Field-sensitive analysis.** With [field sensitivity](/field-sensitivity/), a load or store may add a field offset to each target. A cycle whose edges add offsets does not make the sets equal, so such edges must be left out of the cycle search or handled apart.

## When to use it

Use it in an inclusion-based points-to solver that must handle large programs, together with offline variable substitution and difference propagation. For a small program, or a one-off analysis, plain Andersen's analysis is simpler and fast enough. When near-linear time matters more than precision, use [Steensgaard's analysis](/steensgaard-analysis/).

## Pitfalls

- **Merging too early.** A component of the offline graph can pass through several ref nodes. The cycle through $*a$ and $b$ exists only when the other pointers have targets too. In the statements `a = &x`, `b = &w`, `b = *a`, `*c = b`, `q = *c`, `*a = q`, with no target for $c$, the least set of $x$ is empty and that of $b$ is $\{w\}$. Merging $x$ with $b$ at once is sound but less precise than Andersen's analysis.
- **Merging the variable nodes of a mixed component offline.** A cycle that passes through a ref node needs a target for that pointer. Merge offline only the cycles of plain copies.
- **Equal sets are only a hint.** Two nodes can have equal sets without a cycle. The lazy check must still search, and must not merge on the hint alone.
- **Checking an edge again and again.** Without the mark of line L13, an edge between two nodes with equal sets and no cycle starts a search on every visit.
- **Merging locations.** Only the pointer sets are joined. The addresses in the sets stay the original locations.

## Implementations

## History

Fähndrich, Foster, Su and Aiken (1998) merged cycles online with a partial search, and Rountev and Chandra (2000) merged equal variables before solving. Heintze and Tardieu (2001) and Pearce, Kelly and Hankin (2003) gave other online methods. Hardekopf and Lin (2007) observed that most searches of the online methods find nothing, and proposed to search only when an edge brings no new facts, which is lazy cycle detection, and to plan merges through loads and stores in an offline pass, which is hybrid cycle detection. Together with offline substitution, the methods made the inclusion-based analysis of C programs of millions of lines practical.

## References
