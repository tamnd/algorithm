---
tag: ADSKYW
kind: algorithm
slug: das-one-level-flow
name: One-level flow analysis
aliases:
- Das one level flow
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Points-to analysis with subset constraints at the top pointer level and unification below. Das measured it nearly as precise as Andersen and nearly as fast as Steensgaard.
solves: [points-to-analysis]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of pointer statements, α: the inverse Ackermann function}
  time: {worst: O(n (n + m)), unification-phase: O((n + m) α(n + m))}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 2000
  people: [Manuvir Das]
  note: Das presented one-level flow at PLDI 2000, after he observed that in C programs most pointer copies happen at the top level.
prereqs: [points-to-analysis, andersen-analysis, steensgaard-analysis]
see_also: [andersen-analysis, steensgaard-analysis, disjoint-set-forest, graph-reachability, alias-analysis, field-sensitivity, context-sensitivity, cfl-reachability]
sources:
  - paper: doi:10.1145/349299.349309
    title: Manuvir Das, Unification-based pointer analysis with directional assignments, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2000), 35 to 46
    locator: whole paper (the observation about top-level copies in C, the flow edges between the outer types, the unification below them, and the comparison with Steensgaard's and Andersen's analyses)
  - paper: doi:10.1145/237721.237727
    title: Bjarne Steensgaard, Points-to analysis in almost linear time, Proceedings of the 23rd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '96), 32 to 41, 1996
    locator: the unification-based analysis with union-find that one-level flow keeps below the top level
  - paper: "Lars Ole Andersen, Program Analysis and Specialization for the C Programming Language, PhD thesis, DIKU, University of Copenhagen, 1994 (DIKU report 94/19)"
    locator: the chapter on pointer analysis, with the inclusion constraints that one-level flow keeps at the top level
  - paper: doi:10.1145/379605.379665
    title: Michael Hind, Pointer analysis, haven't we solved this problem yet?, Proceedings of the ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering (PASTE '01), 54 to 61, 2001
    locator: the place of one-level flow between the unification-based and the inclusion-based analyses
---

One-level flow is a [points-to analysis](/points-to-analysis/) that sits between [Steensgaard's analysis](/steensgaard-analysis/) and [Andersen's analysis](/andersen-analysis/). It reads each assignment as a subset constraint on the values that the assignment moves, as Andersen does, but only at that one level. The things those values point to are unified, as Steensgaard does. Das proposed it in 2000 after he saw that in C programs, most of the precision that Andersen's analysis gains over Steensgaard's comes from copies of top-level pointers. The unification phase runs in almost linear time; the final sets come from one reachability pass over the flow edges.

## In plain words

Steensgaard's method is fast but merges too much: after `p = q`, the two pointers share all their targets, in both directions. Andersen's method keeps the direction, so only `p` gains the targets of `q`, but it is slow. One-level flow keeps the direction for the value that the assignment copies, and merges everything under it. So after `p = q`, the pointer `p` gets the targets of `q`, and not the other way around. The cells that those targets point to are merged into one group, as Steensgaard would do. In C, most copies are of plain pointers, so this keeps most of the precision of the slow method. The merges are cheap, and one walk along the arrows at the end gives the sets.

## The problem

The input and the output are those of [Andersen's analysis](/andersen-analysis/): statements `p = &a`, `p = q`, `p = *q` and `*p = q` over $n$ variables, each also a location, with `p = alloc` at site $k$ read as `p = &h_k`; the output is a set $S(v)$ for each variable that meets all the subset constraints. One-level flow gives a set between the two others in precision on most programs, at a cost much lower than Andersen's. The analysis in the terms of a data-flow framework:

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | a partition of value nodes, each class with a base set of locations, at most one deref class and flow edges |
| order | coarser partitions, larger base sets and more edges (bottom is precise) |
| join | merging classes; union of base sets and edges |
| bottom and top | each node alone, empty base sets, no edges; one class holding everything |
| boundary value | none |
| initial value | one value node per location, alone, with an empty base set |
| transfer | monotone, not distributive |

## The algorithm

Each location $a$ has a value node $V(a)$, which stands for the values stored in $a$. The value nodes are in a union-find forest. A class has a base set (the addresses stored in it directly), at most one deref node (the value node of the locations that its values point to) and flow edges to other classes. An assignment adds a flow edge from the value node of its right side to the value node of its left side, and unifies the deref nodes of the two ends. Unifying two classes also unifies their deref nodes. This page writes the method with explicit nodes and edges; Das writes it as a type system in the style of Steensgaard, with flow edges between the outermost types.

```pseudo id=main
ONE-LEVEL-FLOW(S)
L1  make a value node V(a) for each variable a, alone, with an empty base set
L2  for each statement of S, in any order do
L3      x = &a: add a to base(V(x)); UNIFY(V(a), DEREF(V(x)))
L4      x = y:  FLOW(V(y), V(x))
L5      x = *y: FLOW(DEREF(V(y)), V(x))
L6      *x = y: FLOW(V(y), DEREF(V(x)))
    return CLOSURE()

FLOW(u, v)
L7  add the flow edge u -> v
L8  UNIFY(DEREF(u), DEREF(v))

DEREF(u)
L9  if the class of u has no deref node then give it a new one
    return the class of its deref node

UNIFY(x, y)
L10 while a pair (x, y) of classes waits to be unified do
L11     merge x and y into one class c
L12     base(c) <- base(x) + base(y); the edges of c are those of x and y
L13     if both had deref nodes then queue the pair of the two deref nodes; else c keeps the one it has

CLOSURE()
L14 for each location a do
L15     add a to the set of every class that a class with a in its base set reaches along flow edges
L16 return S(v) = the set of the class of V(v), for each v
```

Lines L1 to L13 are phase 1, and CLOSURE is phase 2. Each statement adds at most one flow edge, and each edge is directional, so the top level keeps Andersen's precision. Everything that DEREF reaches is unified. Phase 2 is a [graph reachability](/graph-reachability/) pass, one search per location. Unlike Andersen's analysis, phase 1 never adds an edge because a set grew: the deref node of a class stands for all its targets at once, so loads and stores need one edge each.

## Example

```
entry:
  a = &x
  b = &y
  p = &a
  q = &b
  p = q
  ret 0
```

Phase 1:

| statement | what happens |
|---|---|
| `a = &x` | $x$ goes into $base(V(a))$; $V(x)$ is unified with the deref node of $V(a)$ |
| `b = &y` | $y$ goes into $base(V(b))$; $V(y)$ is unified with the deref node of $V(b)$ |
| `p = &a` | $a$ goes into $base(V(p))$; $V(a)$ is unified with the deref node of $V(p)$ |
| `q = &b` | $b$ goes into $base(V(q))$; $V(b)$ is unified with the deref node of $V(q)$ |
| `p = q` | flow edge $V(q) \to V(p)$; the deref nodes of $V(q)$ and $V(p)$, which are $V(b)$ and $V(a)$, are unified, so $V(a)$ and $V(b)$ form one class with base set $\{x, y\}$, and their deref nodes $V(x)$ and $V(y)$ are unified too |

Phase 2 sends $b$ along the edge $V(q) \to V(p)$. The three analyses give:

| variable | Andersen | one-level flow | Steensgaard |
|---|---|---|---|
| $p$ | $\{a, b\}$ | $\{a, b\}$ | $\{a, b\}$ |
| $q$ | $\{b\}$ | $\{b\}$ | $\{a, b\}$ |
| $a$ | $\{x\}$ | $\{x, y\}$ | $\{x, y\}$ |
| $b$ | $\{y\}$ | $\{x, y\}$ | $\{x, y\}$ |

At the top level, one-level flow keeps the direction of `p = q`, so $q$ does not get $a$. One level down, it merges what $a$ and $b$ hold, as Steensgaard does.

## Correctness

The full proof is in the proof file. Its steps:

1. **Merges keep derefs together.** When two classes merge, their deref nodes are unified in the same call, so the deref class of a node at any moment stays the deref class of its class at the end.
2. **Two invariants.** At the end, if $a$ is in the base set of a class $r$, then $V(a)$ is in the deref class of $r$; and the two ends of each flow edge have the same deref class.
3. **Sets share one deref class.** Following a path of flow edges, every location in the set of a class $r$ has its value node in the deref class of $r$.
4. **The result is a solution.** For `x = *y` and $a$ in $S(y)$, step 3 puts $V(a)$ in the deref class of $V(y)$, which has the edge to $V(x)$ that line L5 added, so $S(a) \subseteq S(x)$. The store is the same, and the other forms are direct.
5. **It contains Andersen's result.** Andersen's sets are the least solution.

When the program has only address and copy statements and no target of an address is ever assigned, the result is exactly Andersen's: the proof file shows this, and a test checks it on random programs.

## Complexity

**Proved.** Phase 1 makes at most $n + 3m$ nodes and $O(n + m)$ union-find operations, so it takes $O((n + m)\,\alpha(n + m))$ time if base sets join in $O(1)$, with $\alpha$ the [inverse Ackermann function](/inverse-ackermann-function/). Phase 2 runs one search per location over at most $n + 3m$ nodes and $m$ edges, so $O(n (n + m))$ time, and the sets take $O(n^2)$ space. A client that asks only some queries can run phase 2 for them alone.

**Stated in the paper, not proved here.** Das reports that on his C benchmarks the analysis was nearly as precise as Andersen's and its running time was close to Steensgaard's.

**Measured, not proved.** In the seeded tests, on 400 random programs of up to 30 statements, every set contained Andersen's. In a separate seeded run of 5,000 random programs, the result equalled Andersen's on 3,686 of them.

## Properties

- **Between the two classic analyses, mostly.** The sets always contain Andersen's. They usually lie inside Steensgaard's, but not always: in the seeded run above, 48 of the 5,000 programs had some set that was not inside Steensgaard's. The smallest such program found is `v1 = *v1`, `v0 = *v1`, `v0 = &v0`. This formulation unifies the deref nodes at once, even for a pointer that never gets a target, while Steensgaard's analysis waits with its pending lists.
- **Directional at one level.** A copy `p = q` moves addresses from $q$ to $p$ only. A load or a store moves values directionally between a pointer and the class of its targets.
- **Two phases.** The unification phase is online and cheap; the closure phase is the only part that can be quadratic.
- **Order independent.** The tests found no case where the order of the statements changed the result.

## Variants and improvements

- **More levels.** Keeping the direction for $k$ levels gives analyses between one-level flow and Andersen's. Das's measurements suggest that one level already gives most of the gain on C programs.
- **Conditional unification.** Unifying deref nodes only once both sides can hold an address, as Steensgaard's pending lists do, would avoid the extra merges in the small example of the Properties section.
- **Context sensitivity.** The flow edges can be labelled with the calls and returns they cross, and a path then counts only if its calls and returns match like brackets. This gives [context sensitivity](/context-sensitivity/) as a form of [CFL-reachability](/cfl-reachability/).
- **Fields.** As with the other analyses, structures can be split into fields; see [field sensitivity](/field-sensitivity/).

## When to use it

Use it for C programs of millions of lines when Steensgaard's sets are too coarse and Andersen's analysis is too slow. It is a good fit for clients that care about top-level pointers, such as call graphs through function pointers held in variables. For programs where most pointer traffic goes through the heap, such as Java programs with many objects that point to objects, the unified levels lose more, and an optimized Andersen's analysis is the better choice.

## Pitfalls

- **Forgetting to unify the derefs of a flow edge.** If FLOW adds the edge but does not unify the deref nodes of its ends, a load through a pointer that got its targets by a copy misses facts. Step 2 of the proof needs this unification.
- **Unifying the two ends of a copy.** Merging $V(p)$ and $V(q)$ for `p = q` gives Steensgaard's analysis, not one-level flow. Only the deref nodes are unified.
- **Reading the classes as sets.** Two variables whose value nodes are in one class have equal sets, but the sets of the others come from the closure in phase 2, not from the classes.
- **Treating the closure as cheap.** Phase 2 is a reachability pass and can be quadratic. Compute it once and store it, or compute it per query.

## Implementations

## History

Manuvir Das presented one-level flow at PLDI 2000 under the title "Unification-based pointer analysis with directional assignments". His starting point was a measurement: on C programs, the extra precision of Andersen's analysis over Steensgaard's came mostly from assignments of top-level pointers. The method showed that the choice between unification and inclusion need not be made for the whole program, and later analyses mix the two in other ways.

## References
