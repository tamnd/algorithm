---
tag: MBB0JP
kind: algorithm
slug: andersen-analysis
name: Andersen's analysis
aliases:
- inclusion-based points-to analysis
- subset-based pointer analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: core
summary: Flow-insensitive points-to analysis that turns each assignment into a subset constraint and solves the constraint graph in cubic time.
solves: [points-to-analysis]
model: word-ram
complexity:
  vars: {n: the number of variables (each variable is also a location), m: the number of pointer statements}
  time: {worst: O(n^3 + m)}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 1994
  people: [Lars Ole Andersen]
  note: Andersen gave the inclusion-based analysis of C pointers in his PhD thesis at DIKU, University of Copenhagen.
prereqs: [points-to-analysis, transitive-closure, worklist-dataflow-algorithm]
see_also: [steensgaard-analysis, das-one-level-flow, online-cycle-elimination, hybrid-cycle-detection, offline-variable-substitution, alias-analysis, field-sensitivity, cfl-reachability]
sources:
  - paper: "Lars Ole Andersen, Program Analysis and Specialization for the C Programming Language, PhD thesis, DIKU, University of Copenhagen, 1994 (DIKU report 94/19)"
    locator: the chapter on pointer analysis, with the inclusion constraints for the assignments of C and their solution
  - paper: doi:10.1109/LICS.1997.614960
    title: Nevin Heintze and David McAllester, On the cubic bottleneck in subtyping and flow analysis, Proceedings of the 12th IEEE Symposium on Logic in Computer Science (LICS), 342 to 351, 1997
    locator: whole paper (the cubic bound of inclusion-based flow analysis and its relation to 2NPDA reachability)
  - paper: doi:10.1007/978-3-642-03237-0_15
    title: Manu Sridharan and Stephen J. Fink, The complexity of Andersen's analysis in practice, Static Analysis Symposium (SAS 2009), LNCS 5673, 205 to 221
    locator: whole paper (a quadratic bound for k-sparse programs, which explains why the analysis is fast on real code)
  - paper: doi:10.1145/379605.379665
    title: Michael Hind, Pointer analysis, haven't we solved this problem yet?, Proceedings of the ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering (PASTE '01), 54 to 61, 2001
    locator: the survey of flow-insensitive analyses and their scalability
  - paper: doi:10.1561/2500000014
    title: Yannis Smaragdakis and George Balatsouras, Pointer Analysis, Foundations and Trends in Programming Languages 2(1), 1 to 69, 2015
    locator: the inclusion-based model of the analysis, written as rules over input relations
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 12.4 (a simple pointer-analysis algorithm, flow-insensitive, written in Datalog)
---

Andersen's analysis solves the [points-to analysis](/points-to-analysis/) problem for a whole program, without regard to the order of its statements. Each pointer assignment becomes one subset constraint between points-to sets: after `p = q`, the set of `p` must contain the set of `q`. The analysis finds the least sets that meet all the constraints. It keeps a constraint graph with an edge for each subset constraint and moves new facts along the edges with a worklist. Loads and stores add new edges while it runs, because the target of `*p` is known only when the set of `p` is known. On $n$ variables it runs in $O(n^3)$ time in the worst case, and much faster on real programs.

## In plain words

Each pointer in a program holds the address of some memory cell. We want to know, for each pointer, all the cells it could ever hold, for any run of the program. Andersen's analysis reads each assignment as a rule. If one pointer is copied into another, then everything the first could hold, the second could hold too. Copies through a pointer give rules that depend on what that pointer holds, so new rules appear as the answer grows. The analysis draws an arrow from each source to each target and pushes facts along the arrows until nothing new arrives. The result is the smallest answer that obeys every rule. It never misses a cell that a real run can use. It can list a cell that no real run uses, because it ignores the order of the statements.

## The problem

The input is a set of statements in the four basic forms over a set $V$ of $n$ variables, and the output is a points-to set $pts(v) \subseteq V$ for each variable. Every variable is also a memory location, so it can be a target. In the toy IR, `p = alloc` at site $k$ is treated as `p = &h_k`, with one location $h_k$ per site. Each statement gives one constraint:

| statement | constraint |
|---|---|
| `p = &a` | $a \in pts(p)$ |
| `p = q` | $pts(q) \subseteq pts(p)$ |
| `p = *q` | $pts(a) \subseteq pts(p)$ for every $a \in pts(q)$ |
| `*p = q` | $pts(q) \subseteq pts(a)$ for every $a \in pts(p)$ |

The result is the least solution of these constraints, in the order of $\subseteq$ on each set, with union as the join. This is the order of abstract interpretation in the direction of Cousot: bottom is the most precise answer, where every set is empty, and larger answers are less precise. The least solution exists because the solutions are closed under intersection. The analysis in the terms of a data-flow framework:

| item | value |
|---|---|
| direction | none: the analysis is flow-insensitive and has one answer for the whole program |
| may or must | may |
| domain | maps from $V$ to subsets of $V$ |
| order | $\subseteq$ on each set (bottom is precise) |
| join | union on each set |
| bottom and top | all sets empty, and all sets equal to $V$ |
| boundary value | none, there is no entry or exit point |
| initial value | all sets empty |
| transfer | monotone, not distributive: the load and store rules combine two facts, $a \in pts(q)$ and $b \in pts(a)$ |

Flow-insensitive means that the order of the statements is ignored: the answer covers every run that executes the statements in any order, any number of times. It does not mean that control flow is ignored entirely. Every real path is one of those orders, so the answer is sound for the program, and statements that the program never reaches can still be dropped first. Two expressions `*p` and `*q` may alias if $pts(p) \cap pts(q) \neq \emptyset$, which gives an [alias analysis](/alias-analysis/).

## The algorithm

The constraint graph has a node for each variable and an edge $u \to v$ for each known constraint $pts(u) \subseteq pts(v)$. Copies give edges at the start. A load `p = *q` gives the edge $a \to p$ for each $a$ that enters $pts(q)$, and a store `*q = r` gives $r \to a$. Each node keeps $delta$, the part of its set that it has not yet sent on. This is difference propagation: each fact moves along each edge once.

```pseudo id=main
ANDERSEN(S)
L1  for each variable v do pts[v] <- {}; succ[v] <- {}; delta[v] <- {}
L2  W <- an empty worklist
L3  for each p = &a in S do add a to pts[p] and to delta[p]; add p to W
L4  for each p = q in S do ADD-EDGE(q, p)
L5  while W is not empty do
L6      take n from W; d <- delta[n]; delta[n] <- {}
L7      for each a in d do
L8          for each p = *n in S do ADD-EDGE(a, p)
L9          for each *n = r in S do ADD-EDGE(r, a)
L10     for each w in succ[n] do PROPAGATE(d, w)
L11 return pts

ADD-EDGE(u, v)
L12 if v is not in succ[u] then
L13     add v to succ[u]; PROPAGATE(pts[u], v)

PROPAGATE(s, v)
L14 new <- s minus pts[v]
L15 if new is not empty then
L16     add new to pts[v] and to delta[v]; add v to W if it is not there
```

A new edge must carry the whole set of its source at once (line L13), since the facts that the source already sent on did not go along this edge. After that, only the differences move (line L10). The implementation keeps the loads and stores of each node in tables, so lines L8 and L9 look only at the statements of $n$, and it uses a first-in first-out worklist. The order of the worklist changes the running time, not the result.

## Example

The program, in the toy IR:

```
entry:
  p = &a
  q = &b
  r = &p
  s = q
  *r = s
  t = *r
  ret 0
```

Lines L3 and L4 give $pts(p) = \{a\}$, $pts(q) = \{b\}$, $pts(r) = \{p\}$, the edge $q \to s$ and $pts(s) = \{b\}$. The worklist is $p, q, r, s$.

| step | node | $d$ | what happens |
|---|---|---|---|
| 1 | $p$ | $\{a\}$ | $p$ has no edges, loads or stores yet |
| 2 | $q$ | $\{b\}$ | $b$ is already in $pts(s)$ |
| 3 | $r$ | $\{p\}$ | load `t = *r`: edge $p \to t$, $pts(t) = \{a\}$; store `*r = s`: edge $s \to p$, $pts(p) = \{a, b\}$ |
| 4 | $s$ | $\{b\}$ | $b$ is already in $pts(p)$ |
| 5 | $t$ | $\{a\}$ | no edges |
| 6 | $p$ | $\{b\}$ | along $p \to t$: $pts(t) = \{a, b\}$ |
| 7 | $t$ | $\{b\}$ | no edges; the worklist is empty |

The result is $pts(p) = \{a, b\}$, $pts(q) = \{b\}$, $pts(r) = \{p\}$, $pts(s) = \{b\}$, $pts(t) = \{a, b\}$, and $pts(a) = pts(b) = \emptyset$. The fact $b \in pts(p)$ comes from the store `*r = s`, which writes into $p$ because $r$ points to $p$. The set of $q$ stays $\{b\}$: the edge $q \to s$ goes one way only. The [Steensgaard analysis](/steensgaard-analysis/) of the same program unifies the targets of $q$ and $s$ with those of $p$ and gives $pts(q) = \{a, b\}$.

## Correctness

The full proof is in the proof file. Its steps:

1. **The least solution exists.** The intersection of solutions is a solution, and the assignment where every set is $V$ is one. So the intersection $L$ of all solutions is the least one. It is also the least fixed point of a monotone map, by the [Knaster-Tarski theorem](/knaster-tarski-theorem/).
2. **Every fact is forced.** By induction over the steps, $pts(v) \subseteq L(v)$, and every edge $u \to v$ has $L(u) \subseteq L(v)$: each new edge comes from a statement and from a fact that is already in $L$.
3. **What is sent stays sent.** With $done(v) = pts(v)$ minus $delta(v)$, every edge $u \to v$ has $done(u) \subseteq pts(v)$, and the edges for loads and stores exist for every element of $done$. A node with a non-empty $delta$ is on the worklist.
4. **At the end, the sets are a solution.** When the worklist is empty, $done = pts$, so all four constraints hold. With step 2, $pts = L$.
5. **Soundness for the program.** In any run that executes the statements in any order, the cell that $v$ points to is always in $L(v)$. Each statement keeps this true because $L$ meets its constraint.

## Complexity

**Proved.** Each of the at most $n^2$ edges is added once, and its first PROPAGATE costs $O(n)$. Each element enters each set once, so it is in some $d$ once per node; for that pair, lines L8 and L9 touch the loads and stores of the node, and line L10 touches at most $n$ edges. After the statements are read and their repeats dropped in $O(m)$ time, there are at most $n^2$ loads and $n^2$ stores, and the total is $O(n^3 + m)$ time with $O(n^2 + m)$ space. With hash sets the bound is in expectation; with an $n \times n$ bit matrix for the edges and bit vectors for the sets it is a worst-case bound.

**Stated in the literature, not proved here.** Heintze and McAllester (1997) relate the cubic time of inclusion-based flow analysis to the reachability problem of two-way nondeterministic pushdown automata (2NPDA), for which no subcubic algorithm is known; this is the "cubic bottleneck". Sridharan and Fink (2009) show that the worklist algorithm runs in $O(n^2)$ time on *k-sparse* programs, where, roughly, each variable and each location gets its values from at most a constant number of statements, and they argue that real programs are close to this case.

**Measured, not proved.** On random programs of 30 statements, the result of the implementation equals that of a plain round-robin iteration of the four rules in all 400 seeded trials of its test file.

## Properties

- **Least solution.** The result does not depend on the worklist order or on the order of the statements.
- **Directional.** An edge $u \to v$ moves facts only from $u$ to $v$. This is the source of its precision over unification.
- **Not distributive.** The load and store rules join two facts, so the analysis is not a bit-vector problem, and the solver must add edges while it runs.
- **Whole program.** The answer for one variable can depend on any statement. Demand-driven methods answer one query with less work.
- **One location per name.** Every variable and allocation site is one location. A loop that allocates many objects at one site gives one location for all of them.

## Variants and improvements

- **Cycle elimination.** All nodes on a cycle of edges have the same final set, so they can be merged into one. [Online cycle elimination](/online-cycle-elimination/) looks for a cycle when an edge is added; [lazy and hybrid cycle detection](/hybrid-cycle-detection/) look less often or plan the merges offline.
- **Offline variable substitution.** [Offline variable substitution](/offline-variable-substitution/) finds, before solving, variables that must have equal sets and solves for one of each group.
- **Unification.** [Steensgaard's analysis](/steensgaard-analysis/) replaces each subset constraint by an equality and runs in almost linear time, with larger sets. [One-level flow](/das-one-level-flow/) keeps subsets only at the top level.
- **Fields and contexts.** [Field sensitivity](/field-sensitivity/) gives each field of a structure its own location. [Context sensitivity](/context-sensitivity/) analyses each call of a function apart, and [object sensitivity](/object-sensitivity/) uses the receiver object as the context.
- **Datalog and BDDs.** The four rules are a [Datalog](/datalog/) program; [semi-naive evaluation](/semi-naive-evaluation/) is the same difference propagation. Large analyses store the relations as [binary decision diagrams](/bdd-points-to-analysis/).
- **Demand-driven.** [Demand-driven points-to analysis](/demand-driven-points-to/) answers one query by a search in the constraint graph, with matched load and store edges, a form of [CFL-reachability](/cfl-reachability/).

## When to use it

Use it when a flow-insensitive answer is enough and the program is up to a few million lines, as in most whole-program analyses of C and Java. It is the usual base for call graph construction, for [mod-ref analysis](/mod-ref-analysis/) and for alias queries in an optimizer. With cycle elimination and difference propagation, it handles programs of millions of lines. When time must be near linear and precision can drop, use Steensgaard's analysis. When the order of the statements matters, such as for strong updates of a pointer that is assigned twice, use a flow-sensitive analysis.

## Pitfalls

- **New edges need the full set.** If ADD-EDGE sends only the current $delta$ of the source, the facts the source sent earlier never reach the new target, and the result misses facts.
- **Stores write into the target, not the pointer.** The store `*p = q` adds edges $q \to a$ for $a \in pts(p)$. Adding $q \to p$ instead is a common mistake that gives wrong sets for both $p$ and its targets.
- **The order of statements.** Flow-insensitive answers include facts that no single order makes true together. The answer is not "what $p$ points to at this line".
- **Precision of the abstraction.** All objects from one allocation site are one location, so a store into one of them is a store into all. Do not use the result to prove that two objects from one site are different.
- **Self-loops and repeats.** Edges $u \to u$ and repeated statements are harmless, but without a test for repeated edges, ADD-EDGE can run PROPAGATE over the full set many times.

## Implementations

## History

Lars Ole Andersen defined the inclusion-based analysis in his 1994 PhD thesis at DIKU, as part of a partial evaluator for C. Steensgaard's 1996 unification analysis was a faster and less precise answer to its cubic cost. Heintze and McAllester (1997) placed the cubic time among the problems equivalent to 2NPDA reachability. Fähndrich, Foster, Su and Aiken (1998) made the solver much faster by merging cycles online, Rountev and Chandra (2000) by finding equal variables offline, and Hardekopf and Lin (2007) by lazy and hybrid cycle detection, which made Andersen's analysis of millions of lines of C practical. Hind (2001) surveyed the field and its open questions. Sridharan and Fink (2009) explained its speed on real code with the k-sparse bound. Many current tools write the analysis as Datalog rules; Smaragdakis and Balatsouras (2015) survey this style.

## References
