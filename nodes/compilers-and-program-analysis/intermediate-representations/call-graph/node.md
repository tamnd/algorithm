---
tag: XSNDFV
kind: definition
slug: call-graph
name: Call graph
aliases:
- call multigraph
area: compilers-and-program-analysis/intermediate-representations
level: intro
summary: A directed graph with one node per procedure and an edge from caller to callee for each possible call.
prereqs: [control-flow-graph, directed-graph]
see_also: [call-graph-construction, class-hierarchy-analysis, rapid-type-analysis, strongly-connected-components, interprocedural-dataflow-analysis, function-inlining, cfl-reachability, multigraph]
sources:
  - book: isbn:9780321486813
    title: Alfred V. Aho, Monica S. Lam, Ravi Sethi and Jeffrey D. Ullman, Compilers, Principles, Techniques, and Tools, second edition, Addison-Wesley, 2007
    locator: Section 12.1 (Basic Concepts of interprocedural analysis), with 12.1.1 (call graphs) and 12.1.2 (context sensitivity)
  - paper: doi:10.1109/TSE.1979.234183
    title: Barbara G. Ryder, Constructing the call graph of a program, IEEE Transactions on Software Engineering SE-5(3), 1979, pages 216-226
    locator: the call graph of a program with procedure parameters and an algorithm that builds it
  - paper: doi:10.1145/506315.506316
    title: David Grove and Craig Chambers, A framework for call graph construction algorithms, ACM Transactions on Programming Languages and Systems 23(6), 2001, pages 685-746
    locator: the definition of call graphs with call sites and contexts, and the parameterized family of construction algorithms with their precision and cost
  - book: isbn:9780128154120
    title: Keith D. Cooper and Linda Torczon, Engineering a Compiler, third edition, Morgan Kaufmann, 2022
    locator: Chapter 4 (Intermediate Representations), the part on the call graph; Chapter 9 (interprocedural analysis)
---

A call graph is a directed graph that shows which procedures of a program can call which. It has one node per procedure and an edge from $P$ to $Q$ when some call in $P$ can call $Q$. The *call multigraph* keeps one edge per call site, so two calls from $P$ to $Q$ give two parallel edges. Where the [control flow graph](/control-flow-graph/) shows control inside one procedure, the call graph shows it between procedures. Interprocedural analyses walk it bottom-up or top-down, and inlining, dead procedure removal and whole-program optimizations read it.

## Definition

Let a program have a finite set $\Pi$ of procedures and a finite set $S$ of *call sites*, the call instructions in the bodies of the procedures. Each site $s \in S$ lies in one procedure $\mathrm{caller}(s)$, and the semantics gives the set $\mathrm{callees}(s) \subseteq \Pi$ of procedures that $s$ calls in some run.

- The *call multigraph* has the nodes $\Pi$ and one edge $s : \mathrm{caller}(s) \to Q$, labeled by the site, for each $s \in S$ and each $Q \in \mathrm{callees}(s)$.
- The *call graph* forgets the labels: it has an edge $P \to Q$ if some site $s$ in $P$ has $Q \in \mathrm{callees}(s)$.
- The *root* is the procedure where runs start, such as `main`, or a set of roots for a library or a program with callbacks.

When every call names its callee directly, $\mathrm{callees}(s)$ is that one name, and the call graph is read from the text in one pass, in time linear in the size of the program. With calls through function pointers, virtual methods or closures, $\mathrm{callees}(s)$ is a property of the runs and undecidable in general, so a compiler computes a superset. A static call graph $G$ is *sound* if every call that happens in some run is an edge of $G$. [Call graph construction](/call-graph-construction/) is the analysis that builds such a superset, from cheap and coarse ([class hierarchy analysis](/class-hierarchy-analysis/), [rapid type analysis](/rapid-type-analysis/)) to precise and costly (call graphs built together with a [points-to analysis](/points-to-analysis/)).

A *dynamic call graph* records only the calls of one run or of a set of test runs. It is exact for those runs and, as a basis for optimization, unsound for the others.

### Structure

- **Recursion.** A procedure is recursive if it lies on a cycle of the call graph. The [strongly connected components](/strongly-connected-components/) are the groups of mutually recursive procedures.
- **Bottom-up order.** Collapsing each component to one node gives a directed acyclic graph. A reverse topological order of it, callees before callers, is the order in which a bottom-up analysis computes procedure summaries, iterating to a fixed point inside each component.
- **Reachable procedures.** Procedures that the roots cannot reach in a sound call graph are never called, and a whole-program compiler can delete them.
- **Context.** A context-sensitive analysis distinguishes the calls of $Q$ by the chain of call sites that led to it. This is a path in the call multigraph, which is why the multigraph keeps the sites. The set of valid paths, where each return goes back to its call, is the language of a context-free grammar over the sites, see [CFL reachability](/cfl-reachability/).

## Examples and non-examples

### A small program

In the toy IR, with the call form `x = call f(a, b)`:

```
main:
  a = call even(n)
  b = call sq(n)
  c = call sq(a)
  r = a + b
  r = r + c
  ret r
```

```
even:
  z = k == 0
  br z yes no
yes:
  ret 1
no:
  k1 = k - 1
  r = call odd(k1)
  ret r
```

`odd` is the same as `even` with `ret 0` in `yes` and `call even(k1)` in `no`, and `sq` is one block:

```
sq:
  y = x * x
  ret y
```

`main` has the parameter `n`, `even` and `odd` have `k`, and `sq` has `x`. The call sites are $s_1$ = `call even(n)`, $s_2$ = `call sq(n)`, $s_3$ = `call sq(a)` in `main`, $s_4$ in `even` and $s_5$ in `odd`.

- Call multigraph: $s_1 : main \to even$, $s_2 : main \to sq$, $s_3 : main \to sq$, $s_4 : even \to odd$, $s_5 : odd \to even$. Five edges.
- Call graph: $main \to even$, $main \to sq$, $even \to odd$, $odd \to even$. Four edges; $s_2$ and $s_3$ merge.
- Strongly connected components: $\{main\}$, $\{even, odd\}$ and $\{sq\}$. The pair is mutually recursive.
- Bottom-up order: $sq$, then $\{even, odd\}$ (iterated together), then $main$. The order $\{even, odd\}$, $sq$, $main$ is also valid.

The run of `main` on $n = 4$ returns $1 + 16 + 1 = 18$, on $n = 3$ it returns $0 + 9 + 0 = 9$, and on $n = 0$ it returns $1 + 0 + 1 = 2$. On $n = -1$ the recursion never reaches 0, and the toy interpreter stops with "out of fuel". The call graph is the same for all inputs: it shows which calls are possible, not how often they happen.

### An indirect call

In C, `int (*op)(int) = flag ? inc : dec; y = op(x);` has one call site whose callee depends on `flag`. A sound call graph has both edges, to `inc` and to `dec`, because each is possible in some run. A points-to analysis finds that `op` points to one of these two, so the call graph does not get an edge to every function whose address is taken; a cruder construction would add all of them.

### Non-examples

- The [control flow graph](/control-flow-graph/) of `main` has one node, not three, because a call does not end a basic block in this site's convention. The calls appear in the call graph, not as CFG edges.
- A *call tree* (one node per activation, as in a profiler) is not a call graph: it can be infinite for a recursive program, while the call graph is always finite.
- A dependence graph between modules (which file imports which) is not a call graph; an import does not mean a call.

### Pitfalls

- **Treating the call graph as exact.** Edges for indirect calls are possible calls. An optimization such as inlining a virtual call needs a guard or a proof that the target is unique.
- **Forgetting entry points.** Callbacks, reflection, signal handlers and exported functions are called from outside the program text. If they are not roots, the call graph wrongly marks them as dead.
- **Merging sites too early.** The plain call graph loses which site made a call, and with it the context that interprocedural analyses need to match calls and returns.

## Related definitions

- [Control flow graph](/control-flow-graph/): the graph inside one procedure. Joining the CFGs of all procedures with call and return edges gives the interprocedural CFG.
- [Call graph construction](/call-graph-construction/): how to build a sound call graph in the presence of indirect calls, with [class hierarchy analysis](/class-hierarchy-analysis/) and [rapid type analysis](/rapid-type-analysis/) as cheap members of the family.
- [Strongly connected components](/strongly-connected-components/): the groups of mutually recursive procedures.
- [Interprocedural dataflow analysis](/interprocedural-dataflow-analysis/): analyses that walk the call graph, with summaries or with contexts.
- [Function inlining](/function-inlining/): the transformation that replaces a call edge by a copy of the callee.

## References
