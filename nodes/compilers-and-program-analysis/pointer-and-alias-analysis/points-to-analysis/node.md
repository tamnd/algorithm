---
tag: BT2X7T
kind: problem
slug: points-to-analysis
name: Points-to analysis
aliases:
- pointer analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: core
summary: For each pointer variable, find a set of abstract memory locations, such as allocation sites, that it may point to.
prereqs: [alias-analysis, dataflow-analysis, three-address-code]
see_also: [andersen-analysis, steensgaard-analysis, das-one-level-flow, field-sensitivity, flow-sensitivity, context-sensitivity, cfl-reachability, may-alias-undecidability]
sources:
  - paper: "Lars Ole Andersen, Program Analysis and Specialization for the C Programming Language, PhD thesis, DIKU, University of Copenhagen, 1994 (DIKU report 94/19)"
    locator: the chapter on pointer analysis (inclusion constraints for the assignments of C)
  - paper: doi:10.1145/237721.237727
    title: Bjarne Steensgaard, Points-to analysis in almost linear time, Proceedings of the 23rd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '96), 32 to 41, 1996
    locator: the unification-based analysis and its almost linear bound
  - paper: doi:10.1145/379605.379665
    title: Michael Hind, Pointer analysis, haven't we solved this problem yet?, Proceedings of the ACM SIGPLAN-SIGSOFT Workshop on Program Analysis for Software Tools and Engineering (PASTE '01), 54 to 61, 2001
    locator: the dimensions of precision (flow, context, heap model, aggregates) and the open problems
  - paper: doi:10.1561/2500000014
    title: Yannis Smaragdakis and George Balatsouras, Pointer Analysis, Foundations and Trends in Programming Languages 2(1), 1 to 69, 2015
    locator: the Datalog formulation of the analysis and the survey of context and heap abstractions
  - paper: doi:10.1109/LICS.1997.614960
    title: Nevin Heintze and David McAllester, On the cubic bottleneck in subtyping and flow analysis, Proceedings of the 12th IEEE Symposium on Logic in Computer Science (LICS), 342 to 351, 1997
    locator: whole paper (the cubic bound of inclusion-based flow analysis and 2NPDA reachability)
  - paper: doi:10.1007/978-3-642-03237-0_15
    title: Manu Sridharan and Stephen J. Fink, The complexity of Andersen's analysis in practice, Static Analysis Symposium (SAS 2009), LNCS 5673, 205 to 221
    locator: the quadratic bound for k-sparse programs
  - paper: doi:10.1145/604131.604142
    title: Venkatesan T. Chakaravarthy, New results on the computability and complexity of points-to analysis, Proceedings of the 30th ACM Symposium on Principles of Programming Languages (POPL 2003), 115 to 125
    locator: the undecidability with dynamic memory and the complexity of the flow-insensitive problem
---

Points-to analysis computes, for each pointer in a program, a set of memory locations that the pointer may hold the address of. A location is a variable or an abstract heap cell, usually one per allocation site. The answer must be sound: every address that a pointer holds in some run must be in its set. Smaller sets are more precise. The exact answer is [undecidable](/may-alias-undecidability/) in general, so every algorithm computes an over-approximation, and the design space is the trade between precision and cost: [Andersen's analysis](/andersen-analysis/) in cubic time, [Steensgaard's analysis](/steensgaard-analysis/) in almost linear time, and flow-sensitive and context-sensitive analyses that cost more. The result answers [alias](/alias-analysis/) questions, builds call graphs through function pointers and virtual calls, and feeds almost every optimization that moves or removes loads and stores.

## In plain words

Many program variables hold addresses. A compiler that wants to move a load past a store must know whether the two can touch the same memory. Points-to analysis gives, for each pointer, a list of the places it might point to. The list may contain places the pointer never reaches, but it must never miss one that it does reach. A short list helps the compiler more. Some analyses keep a separate list at each line of the program. Others keep one list per pointer for the whole program, which is cheaper but coarser. Memory made at run time is named by the line that makes it, so all objects made by one line share one name.

## Definition

**Input.** A program in the toy IR with the pointer instructions `p = &x`, `x = *p`, `*p = a` and `p = alloc`, together with copies `x = y` and the other instructions. The *abstract locations* are the variables $V$ and one heap location $h_k$ for each `alloc` site $k$; write $Loc$ for their set and $N = |Loc|$. In a run, the $k$-th site can make many cells, and each of them maps to $h_k$. A variable maps to itself.

**Output.** A points-to graph $G \subseteq Loc \times Loc$, where $(p, \ell) \in G$ means that $p$ may hold the address of a location that maps to $\ell$. Write $G(p) = \{\ell : (p, \ell) \in G\}$. A *flow-sensitive* analysis gives one graph at each program point. A *flow-insensitive* analysis gives one graph for the whole program.

**The lattice.** The domain at a point is the powerset of $Loc \times Loc$, ordered by $\subseteq$, with union as the join. This is the order of abstract interpretation in the direction of Cousot: bottom is $\emptyset$, the most precise value (no address is held, or the point is not reached), and top is $Loc \times Loc$. The height is $h = N^2$. Turning the order upside down maps this onto the meet convention of Kildall, where union becomes the meet and $\emptyset$ becomes $\top$; this page uses only the join form.

**Transfer functions.** Each instruction maps a graph $G$ to a new graph. "Kill $p$" removes all pairs $(p, \cdot)$.

| instruction | output |
|---|---|
| `p = &a` | kill $p$, add $(p, a)$ |
| `p = alloc` at site $k$ | kill $p$, add $(p, h_k)$ |
| `p = q` | kill $p$, add $(p, \ell)$ for each $\ell \in G(q)$ |
| `p = *q` | kill $p$, add $(p, \ell)$ for each $a \in G(q)$ and $\ell \in G(a)$ |
| `*p = q` with $G(p) = \{a\}$, $a \in V$ | kill $a$, add $(a, \ell)$ for each $\ell \in G(q)$ (a strong update) |
| `*p = q` otherwise, $G(p) \ne \emptyset$ | add $(a, \ell)$ for each $a \in G(p)$ and $\ell \in G(q)$ (a weak update) |
| `*p = q` with $G(p) = \emptyset$ | $\emptyset$: no run gets past a store through a pointer with no target |
| any other instruction that defines $x$ | kill $x$ |

A strong update is allowed only when the target is one concrete location. A heap location $h_k$ stands for many cells, and a store changes only one of them, so a store into it is always weak. Each function is monotone. They are not distributive, because the load and the store combine two facts of $G$.

**Equations.** For each block $B$ with the transfer function $f_B$ (the composition of its instructions):

$$IN[B] = \bigcup_{P \in pred(B)} OUT[P], \qquad OUT[B] = f_B(IN[B]), \qquad IN[entry] = \emptyset.$$

| item | flow-sensitive | flow-insensitive |
|---|---|---|
| direction | forward | none: one answer for the whole program |
| may or must | may | may |
| domain | subsets of $Loc \times Loc$ at each point | subsets of $Loc \times Loc$ |
| order | $\subseteq$ (bottom is precise) | $\subseteq$ |
| join | union | union |
| bottom and top | $\emptyset$ and $Loc \times Loc$ | $\emptyset$ and $Loc \times Loc$ |
| boundary value | $IN[entry] = \emptyset$ | none |
| initial value | $\emptyset$ everywhere | $\emptyset$ |
| transfer | the table above; monotone, not distributive | the inclusion constraints of [Andersen's analysis](/andersen-analysis/); monotone, not distributive |

**The ideal answer** at a point $x$ is the join over all paths, $MOP(x) = \bigcup_{\pi} f_\pi(\emptyset)$, where $\pi$ ranges over the paths from the entry to $x$, and $f_\pi$ composes the transfer functions along $\pi$.

**The computed answer** is the least fixed point of the equations, found by a worklist that starts from $\emptyset$ everywhere and applies the transfer functions until nothing changes ([worklist algorithm](/worklist-dataflow-algorithm/)). The functions are monotone, so the least fixed point exists by the [Knaster-Tarski theorem](/knaster-tarski-theorem/), and $MOP(x) \subseteq LFP(x)$ at every point.

**Soundness.** The concrete semantics is the set of states that reach each point along the executable paths. Map a state $\sigma$ to the graph $\alpha(\sigma)$ of pairs $(p, \ell)$ such that the variable or cell $p$ holds the address of a location that maps to $\ell$. For every instruction, $\alpha$ of the state after it is in the transfer function applied to $\alpha$ of the state before it. A strong update is safe because it replaces the only location that the store can write. By induction along a path, $\alpha(\sigma) \subseteq f_\pi(\emptyset) \subseteq MOP(x) \subseteq LFP(x)$ for every state $\sigma$ that reaches $x$ along $\pi$. Every real path is a path of the graph, so the answer is sound.

**Flow-insensitive soundness.** The flow-insensitive answer $S$ is the least graph that is closed under the inclusion constraints of all instructions: $(p, a) \in S$ for `p = &a`, $S(q) \subseteq S(p)$ for `p = q`, and so on. For every instruction, the transfer function maps any $G \subseteq S$ into $S$, since it only adds pairs that the constraints already require. So $IN[B]$ and $OUT[B]$ stay inside $S$ for every block, and $S$ covers every point. It ignores the order of the statements, not the program: it covers every run that executes the statements in any order, any number of times.

**Precision.** The join loses information when two paths each carry half of a fact. In this program, `p` gets `z` on every path, but the computed answer adds `x` and `y`:

```
entry:
  a = &z
  b = &z
  br c left right
left:
  q = &a
  b = &y
  jump join
right:
  q = &b
  a = &x
  jump join
join:
  p = *q
  ret 0
```

On the path through `left`, `q` points to `a` and `a` to `z`; on the path through `right`, `q` points to `b` and `b` to `z`. So $MOP$ gives $G(p) = \{z\}$ at `ret`. The fixed point joins first: at `join`, $G(q) = \{a, b\}$, $G(a) = \{z, x\}$ and $G(b) = \{z, y\}$, so $G(p) = \{x, y, z\}$.

**Cost.** Let $n$ be the number of instructions and $m$ the number of edges of the control flow graph. Each $OUT[B]$ only grows, at most $h = N^2$ times, so the worklist applies $O((n + m) N^2)$ transfer functions and joins in the worst case. Each application handles sets of $O(N^2)$ pairs, which a bit-vector does in $O(N^2 / w)$ word operations. The flow-insensitive answer takes $O(N^3)$ time by Andersen's analysis.

## Variants

- **Flow sensitivity.** One graph per point, as above, or one per program ([flow sensitivity](/flow-sensitivity/)). Flow-insensitive analysis cannot kill facts, so it cannot do strong updates. Sparse flow-sensitive analyses ([sparse flow-sensitive pointer analysis](/sparse-flow-sensitive-pointer-analysis/)) propagate facts along def-use chains instead of the control flow graph.
- **Context sensitivity.** A procedure analyzed once for all its callers merges their facts. [Context sensitivity](/context-sensitivity/) keeps them apart, by call strings, by the receiver objects ([object sensitivity](/object-sensitivity/)), or by summaries. For higher-order programs the same question is control flow analysis ([0-CFA](/zero-cfa/), [k-CFA](/k-cfa/)).
- **Heap abstraction.** One location per allocation site is the common choice. Adding the calling context to the site (heap cloning) separates objects made by one factory method for different callers.
- **Aggregates.** A structure can be one location or one location per field ([field sensitivity](/field-sensitivity/)). Arrays are usually one location for all elements.
- **Subset or unification.** Inclusion constraints, as in Andersen's analysis, or equality constraints, as in Steensgaard's. [Das's one-level flow](/das-one-level-flow/) uses inclusion at the top level and equality below it.
- **May or must.** A must points-to fact says that $p$ points to one concrete location on every path. Must facts are what allow strong updates.
- **Demand-driven.** Answer the set of one pointer only, by a backward search ([demand-driven points-to analysis](/demand-driven-points-to/)).

## Examples

This program stores one heap pointer over another through `r`:

```
entry:
  p = alloc
  q = alloc
  r = &p
  *r = q
  s = p
  ret 0
```

Call the two sites `h1` and `h2`. In every run, `s` ends up holding the cell from `h2`. Three analyses give these sets at `ret`:

| pointer | flow-sensitive | Andersen | Steensgaard |
|---|---|---|---|
| `p` | {h2} | {h1, h2} | {h1, h2} |
| `q` | {h2} | {h2} | {h1, h2} |
| `r` | {p} | {p} | {p} |
| `s` | {h2} | {h1, h2} | {h1, h2} |

The flow-sensitive analysis sees that `r` points only to the variable `p` when the store runs, so it replaces the set of `p` (a strong update). Andersen's analysis has one set per variable for the whole program, so `p` keeps `h1` from its first statement. Steensgaard's analysis makes the targets of `p` and `q` one class at the store `*r = q`, so `q` also gets `h1`, which Andersen's analysis avoids.

## Known algorithms

| algorithm | kind | worst-case time |
|---|---|---|
| [Andersen's analysis](/andersen-analysis/) | flow-insensitive, inclusion | $O(n^3)$ |
| [Steensgaard's analysis](/steensgaard-analysis/) | flow-insensitive, unification | $O(n\,\alpha(n))$ |
| [Das's one-level flow](/das-one-level-flow/) | inclusion at the top level, unification below | $O(n^2)$ |
| [online cycle elimination](/online-cycle-elimination/), [offline variable substitution](/offline-variable-substitution/), [hybrid cycle detection](/hybrid-cycle-detection/) | faster solvers for Andersen's constraints, same answer | cubic or worse, much faster in practice |
| [BDD-based analysis](/bdd-points-to-analysis/) | Andersen-style sets stored as binary decision diagrams | depends on the size of the diagrams |
| [demand-driven points-to analysis](/demand-driven-points-to/) | one query at a time, often context-sensitive | depends on the query budget |
| [sparse flow-sensitive analysis](/sparse-flow-sensitive-pointer-analysis/) | flow-sensitive, along def-use chains | polynomial |
| [object sensitivity](/object-sensitivity/) | context-sensitive for object-oriented programs | polynomial for a fixed depth $k$, growing exponentially with $k$ |

Here $n$ is the size of the program. [Type-based alias analysis](/type-based-alias-analysis/) answers alias questions from types alone, without points-to sets.

## Bounds

- **Undecidable in general.** With dynamic allocation, the precise flow-sensitive question is undecidable, even when every path is executable ([undecidability of may-alias analysis](/may-alias-undecidability/)). Chakaravarthy (2003) showed that this holds with scalar variables only.
- **NP-hard without the order.** Without dynamic memory, the precise flow-insensitive question is NP-hard when statements may dereference many times ([NP-hardness of precise flow-insensitive alias analysis](/flow-insensitive-alias-np-hardness/)).
- **Cubic for inclusion.** Andersen's analysis takes $O(n^3)$ time. Heintze and McAllester (1997) relate this cubic bound to the reachability problem of two-way nondeterministic pushdown automata, for which no subcubic algorithm is known. Sridharan and Fink (2009) show a quadratic bound for *k-sparse* programs, where, roughly, each variable and each location gets its values from at most a constant number of statements.
- **Output size.** The answer of Andersen's analysis can have $\Theta(n^2)$ pairs, so no algorithm that lists all sets is faster than quadratic in the worst case.

## Reductions

**Points-to gives alias, and alias gives points-to.** `*p` and `*q` may alias when $G(p) \cap G(q) \ne \emptyset$, and $p$ may point to $a$ when `*p` and `a` may alias. So the two questions have the same difficulty, and an [alias analysis](/alias-analysis/) is usually built on a points-to analysis.

**Transitive closure reduces to Andersen's analysis.** Take a directed graph, a variable for each node, the statement `u = &a_u` with a new location $a_u$ for each node $u$, and the copy `v = u` for each edge $(u, v)$. Then $a_u \in pts(v)$ exactly when $v$ is reachable from $u$. So all points-to sets give the [transitive closure](/transitive-closure/) of the graph.

**Andersen's analysis is a Datalog program.** With the input relations `addr`, `copy`, `load` and `store`, the four rules

```
pts(p, a) :- addr(p, a).
pts(p, a) :- copy(p, q), pts(q, a).
pts(p, a) :- load(p, q), pts(q, b), pts(b, a).
pts(b, a) :- store(p, q), pts(p, b), pts(q, a).
```

compute the least solution. Tools such as Doop write context-sensitive analyses for Java this way and evaluate them by [semi-naive evaluation](/semi-naive-evaluation/) ([Datalog](/datalog/)).

**CFL-reachability.** Field-sensitive and context-sensitive points-to questions can be phrased as [CFL-reachability](/cfl-reachability/) on a graph with an edge for each statement, where a store and a load of the same field, or a call and its return, act as matched parentheses.

## Applications

- **Alias analysis for optimization.** Loads and stores that cannot alias may be reordered by [instruction scheduling](/instruction-scheduling-problem/), moved by [loop-invariant code motion](/loop-invariant-code-motion/), or removed by [common subexpression elimination](/common-subexpression-elimination/) and [partial redundancy elimination](/partial-redundancy-elimination/). Fields whose address never escapes can be kept in registers ([scalar replacement of aggregates](/scalar-replacement-of-aggregates/)).
- **Call graphs.** The targets of a call through a function pointer or a virtual method are the points-to set of the pointer or the receiver ([call graph construction](/call-graph-construction/)).
- **Side effects.** [Mod-ref analysis](/mod-ref-analysis/) finds the locations that a call may read or write, and [escape analysis](/escape-analysis/) finds objects that do not outlive their method or thread.
- **Bug finding and security.** Null dereferences, use after free, and the flow of tainted data through the heap all need points-to sets.

## References
