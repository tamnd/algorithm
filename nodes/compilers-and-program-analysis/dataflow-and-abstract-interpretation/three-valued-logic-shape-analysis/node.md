---
tag: BGQ8GB
kind: algorithm
slug: three-valued-logic-shape-analysis
name: Three-valued logic shape analysis
aliases:
- Sagiv-Reps-Wilhelm shape analysis
- TVLA
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: research
summary: Represents heaps by logical structures with a third value for unknown and merges nodes by abstraction predicates, for shape properties.
solves: [shape-analysis]
model: word-ram
complexity:
  vars: {E: the number of edges of the program, L: the number of program points, M: the largest number of canonical structures at one point, N: the largest number of nodes in one structure, v: the number of pointer variables}
  time: {worst: O(E M v^2 N^5)}
  space: {extra: O(L M v N^2)}
properties: {deterministic: true, recursive: false, sound: true, terminates: true}
history:
  year: 1999
  people: [Mooly Sagiv, Thomas Reps, Reinhard Wilhelm]
  note: Sagiv, Reps and Wilhelm presented the method at POPL 1999 and in full in TOPLAS 2002; Lev-Ami and Sagiv built the TVLA system around it in 2000.
prereqs: [shape-analysis, abstract-interpretation, galois-connection]
see_also: [bi-abduction, separation-logic, reduced-product, predicate-abstraction, collecting-semantics, points-to-analysis, reverse-linked-list, abstract-domain]
sources:
  - paper: doi:10.1145/292540.292552
    title: Mooly Sagiv, Thomas Reps and Reinhard Wilhelm, Parametric shape analysis via 3-valued logic, Proceedings of the 26th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '99), 1999, pages 105-118
    locator: the first version of the method, with Kleene's logic, summary nodes and the embedding theorem
  - paper: doi:10.1145/514188.514190
    title: Mooly Sagiv, Thomas Reps and Reinhard Wilhelm, Parametric shape analysis via 3-valued logic, ACM Transactions on Programming Languages and Systems 24(3), 2002, pages 217-298
    locator: the embedding theorem, canonical abstraction, instrumentation predicates, and the focus and coerce operations
  - paper: doi:10.1007/978-3-540-45099-3_15
    title: Tal Lev-Ami and Mooly Sagiv, TVLA, A System for Implementing Static Analyses, Static Analysis Symposium (SAS 2000), LNCS 1824, pages 280-301
    locator: the TVLA system, which builds an analysis from predicates and update formulas written by the user
  - paper: doi:10.1145/347324.348031
    title: Tal Lev-Ami, Thomas Reps, Mooly Sagiv and Reinhard Wilhelm, Putting static analysis to work for verification, A case study, Proceedings of the 2000 ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA '00), pages 26-38
    locator: the analysis applied to sorting programs on linked lists, which shows that correct versions produce sorted lists
  - paper: doi:10.1007/978-3-540-27813-9_2
    title: Thomas Reps, Mooly Sagiv and Reinhard Wilhelm, Static program analysis via 3-valued logic, Computer Aided Verification (CAV 2004), pages 15-30
    locator: an invited survey of the method and of later work on it
  - paper: doi:10.1007/978-3-540-73368-3_25
    title: Igor Bogudlov, Tal Lev-Ami, Thomas Reps and Mooly Sagiv, Revamping TVLA, Making parametric shape analysis competitive, Computer Aided Verification (CAV 2007), LNCS 4590, pages 221-225
    locator: the TVLA transformer as focus, update, coerce and blur, and the speedups of the new implementation
  - paper: "Stephen Cole Kleene, Introduction to Metamathematics, North-Holland, 1952"
    locator: the section on the strong three-valued logic, where an unknown value is neither true nor false
---

Three-valued logic shape analysis is an [abstract interpretation](/abstract-interpretation/) for [shape analysis](/shape-analysis/). It describes a heap as a logical structure: its cells are the individuals, and its pointers are predicates. To get a finite description of heaps of any size, it merges cells that the chosen *abstraction predicates* cannot tell apart into one *summary node*. A fact that is not the same for all the merged cells gets a third truth value, $\tfrac12$, for "unknown". The *embedding theorem* gives soundness: a formula that is true or false on the abstract structure has that value in every heap that the structure describes. Sagiv, Reps and Wilhelm (1999, 2002) gave the method, and the TVLA system (2000) made the predicates a parameter that the user sets.

## In plain words

Draw the heap as boxes and arrows. Keep a few yes or no facts about each box: which variable points to it, which variables can reach it, and whether it is on a loop. Boxes that agree on all those facts are merged into one fuzzy box that may stand for many boxes. Some facts are then no longer yes or no. An arrow from a fuzzy box may be there for some of its boxes and missing for others, so its value is "maybe". A program step first splits a fuzzy box when it needs to know one box exactly, then updates the facts, then throws away pictures that no heap can match, and then merges again. Since there are only so many ways to label boxes, the pictures at each point stop changing, and every real heap at that point matches one of them.

## The problem

Programs work on cells with one pointer field `n`. They have pointer variables, and statements `x = null`, `x = new`, `x = y`, `x = y.n`, `x.n = null`, `x.n = y`, and tests whether a variable is null or whether two variables are equal. The question is the shape problem: find a sound description of all heaps that reach each point, precise enough to show that no null pointer is dereferenced and that lists stay acyclic.

**Three-valued logic.** The values are $0$ (false), $1$ (true) and $\tfrac12$ (unknown). Kleene's strong connectives are $a \wedge b = \min(a, b)$, $a \vee b = \max(a, b)$ and $\neg a = 1 - a$. So $\tfrac12 \wedge 0 = 0$ and $\tfrac12 \vee 1 = 1$, and an unknown input makes the result unknown only when the result depends on it. The *information order* is $a \sqsubseteq b$ if $a = b$ or $b = \tfrac12$: the value $\tfrac12$ is weaker than both $0$ and $1$. The connectives are monotone in this order. If you replace an input by a weaker one, the result can only get weaker.

**Structures.** A structure has nodes and a value for each predicate on them. The core predicates are $x(v)$ for each variable $x$ ("$x$ points to $v$") and $n(v, w)$ ("the field of $v$ is $w$"). There is also a summary flag $sm(v)$, which is $\tfrac12$ when $v$ may stand for several cells. A heap is a structure with only the values $0$ and $1$. This version also stores *instrumentation predicates*, whose values are fixed by the core ones in every heap: $r_x(v)$ ("$v$ is reachable from $x$") and $c(v)$ ("$v$ is on a cycle"). They cost space, but they keep facts that a summary node would otherwise blur.

A map $f$ from the nodes of $S$ onto the nodes of $S'$ *embeds* $S$ into $S'$ if every value of $S$ is $\sqsubseteq$ the value of its image, and two nodes go to the same image only if that image is a summary node. A structure stands for all heaps that embed into it.

## The algorithm

Every unary predicate is an abstraction predicate. **Blur** (canonical abstraction) merges all nodes that agree on every unary predicate. It keeps their unary values, joins the binary values, and marks a merged node as a summary. So a canonical structure has at most one node per vector of unary values, and there are finitely many canonical structures. A statement is done in four steps, as in TVLA:

- **Focus.** Before `x = y.n`, the successor of the node of $y$ must be definite. Focus replaces a structure of $N$ nodes by up to $2N + 1$ structures: one with no successor, one per candidate node that is the successor as a whole, and, for a summary candidate, one in which a single cell is split off as the successor.
- **Update.** Each predicate gets its new value from a Kleene formula over the old values. For example, after `x.n = y` with $x$ at $a$, $r_z'(v) = r_z(v) \vee (r_z(a) \wedge r_y(v))$.
- **Coerce.** Facts that hold in every heap make values sharper, or show that no heap fits: a variable points to at most one cell, a cell has one successor, the successor of a cell reachable from $x$ is reachable from $x$, and an edge back into a cell that is not on a cycle cannot exist. A structure that no heap fits is dropped.
- **Blur** again, so the result is canonical.

The analysis keeps a set $A[p]$ of canonical structures at each point and iterates to a fixed point with a worklist. It does not join structures. The union of the sets is the join.

```pseudo id=main
TVLA-SHAPE-ANALYSIS(P, entry)
L1  for each structure S in entry do add blur(coerce(S)) to A[start] and push it on W
L2  while W is not empty do
L3      take a point p and a structure S from W
L4      for each edge from p to q, with statement st, of P do
L5          R <- post(S, st): focus if st reads a field, then update, then coerce
L6          if st dereferences a variable that has no node in S then report p
L7          for each structure T in R do
L8              K <- blur(T)
L9              if K is not in A[q] then add K to A[q] and push (q, K) on W
L10 return A and the reported points
```

## Example

In-place reversal of the list at `x` into `y`. The loop head is point 1.

```
0: y = null
1: while x != null:
2:     t = x.n
3:     x.n = y
4:     y = x
5:     x = t
6: exit
```

The input is a list of any length. Canonical abstraction gives 4 entry structures: the empty list, one cell, two cells, and a head cell that points into a summary node. All lists of three or more cells map to that last one. Write $X_0$ for the cell of `x`, $X$ for the summary node of the other cells reachable from `x`, and $Y_0$, $Y$ for the same on the `y` side. The most general structure at point 2 is:

| node | variables | $r_x$ | $r_y$ | $c$ | $sm$ | edges out |
|---|---|---|---|---|---|---|
| $Y_0$ | `y` | 0 | 1 | 0 | 0 | to $Y$: $\tfrac12$ |
| $Y$ | none | 0 | 1 | 0 | $\tfrac12$ | to $Y$: $\tfrac12$ |
| $X_0$ | `x`, `t` | 1 | 0 | 0 | 0 | to $X$: $\tfrac12$ |
| $X$ | none | 1 | 0 | 0 | $\tfrac12$ | to $X$: $\tfrac12$ |

No node has both $r_x = 1$ and $r_y = 1$, so the two lists are disjoint. $c = 0$ everywhere, so both are acyclic.

`t = x.n` needs the successor of $X_0$, and focus gives three structures. In the first, $X_0$ has no successor. The update then sets $r_t$ to $1$ on $X$ while `t` is null, and coerce drops the structure. In the second, $X$ is one cell and is the successor. In the third, one cell $X_1$ is split off $X$ as the successor, and $X$ keeps the rest. `x.n = y` points $X_0$ at $Y_0$, so $X_0$ now reaches the old `y` list. `y = x` and `x = t` move the variables, and blur merges the old $Y_0$ into $Y$. The result is again one of the structures at point 1. The worklist stops with 13 structures at point 1, and at most 13 at any point.

At the exit, `x` is null and there are 4 structures: no cell, `y` alone, `y` with one successor, and `y` with a summary of the rest. On all four, $\forall v.\ r_y(v)$ is $1$ and $\exists v.\ c(v)$ is $0$. By the embedding theorem, in every run on every input list, `y` is an acyclic list that holds every cell, so no cell is lost. No point is reported, so the loop never dereferences null.

## Correctness

The embedding theorem is proved by induction on formulas. Atomic values are $\sqsubseteq$ by the definition of embedding. The connectives are monotone. A quantifier is a maximum or minimum over all nodes, and the map is onto, so both sides range over the same values. Each step then keeps every heap of the input inside the output. Blur is itself an embedding. Coerce changes a value only to the one that every embedded heap has. Focus splits a structure into cases that together cover its heaps. The update formulas, read by the theorem, give values $\sqsubseteq$-above the new concrete values. Where the new value cannot be computed from the predicates, as for reachability after a cycle is cut, the formula uses the constant $\tfrac12$. By induction on runs, every reached heap embeds into a structure at its point: $\mathrm{lfp}\, F \subseteq \gamma(\mathrm{lfp}\, F^\#)$, with $\bot$ the empty set of states. The proof file has the details.

## Complexity

A canonical structure has at most $N \le 2^v 3^{v+1}$ nodes, since the variable predicates are always $0$ or $1$. The number $M$ of canonical structures is finite but can be doubly exponential in $v$. One `coerce` costs $O(v N^4 + v^2 N^3)$. A transfer focuses into $O(N)$ structures, so the whole run takes $O(E M v^2 N^5)$ time and $O(L M v N^2)$ space. These bounds are far above what real runs see. In practice the cost depends on how many distinct structures reach each point.

## Properties

- **Sound.** Every reached heap embeds into a structure at its point, and every possible null dereference is reported.
- **Terminating without widening.** The set of canonical structures is finite, so no widening is needed.
- **Parametric.** The precision is set by the choice of predicates. Adding an instrumentation predicate, such as reachability or "is shared", splits nodes that it tells apart and keeps the facts it records exact.
- **Disjunctive.** A set of structures per point keeps cases apart. Joining the structures into one would lose, for example, the case split between a list of one cell and a longer list.

## Variants and improvements

- **TVLA.** Lev-Ami and Sagiv (2000) made predicates, update formulas and integrity rules user input, so one engine runs many analyses. Bogudlov, Lev-Ami, Reps and Sagiv (2007) made the engine up to 50 times faster.
- **Single structure per point.** An analysis can join all structures at a point into one. It is faster but less precise.
- **Verification by stronger predicates.** With predicates for sortedness and order, Lev-Ami, Reps, Sagiv and Wilhelm (2000) showed that correct versions of bubble sort and insertion sort on lists return sorted lists.
- **Separation logic.** The [separation logic](/separation-logic/) analyses and [bi-abduction](/bi-abduction/) describe heaps with list segment formulas instead of logical structures. Bi-abduction computes a summary for each procedure on its own, and this makes the analysis compositional.

## When to use it

Use it when the property is about the shape of linked data, such as acyclicity, sharing, reachability or disjointness, and when it needs a precise case split, as in destructive updates of lists and trees. It fits small and mid-sized code and research tools that need to state new properties as predicates. For whole programs, use a compositional method such as bi-abduction.

## Pitfalls

- **Too few predicates.** With only the core predicates, a summary node loses which cells are reachable from which variable, and the analysis can report null dereferences that cannot happen. The instrumentation predicates keep this information.
- **Wrong update formulas.** An update formula that is not sound for some heap breaks the theorem, and nothing in the method detects it. Test each formula against real heaps.
- **No focus before a field read.** Without focus, `x = y.n` on a summary successor gives `x` the value $\tfrac12$ on several nodes, and the next steps can tell almost nothing.
- **Too many structures.** Each unary predicate can multiply the bound on the number of nodes by 3, and the number of structures at a point can grow very fast. Use few abstraction predicates.

## Implementations

## History

Jones and Muchnick (1979) and later analyses described the heap with graphs of a bounded size. Sagiv, Reps and Wilhelm (TOPLAS 1998) analyzed destructive updates with shape graphs. They then recast shape analysis in Kleene's three-valued logic (1952), with summary nodes, abstraction by predicates and the embedding theorem, at POPL 1999 and in TOPLAS 2002. Lev-Ami and Sagiv built TVLA (SAS 2000), and Lev-Ami, Reps, Sagiv and Wilhelm used it to verify sorting programs (ISSTA 2000). Reps, Sagiv and Wilhelm surveyed the line of work at CAV 2004. Bogudlov and others revamped TVLA in 2007.

## References
