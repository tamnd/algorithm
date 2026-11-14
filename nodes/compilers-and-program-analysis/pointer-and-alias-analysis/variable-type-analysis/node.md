---
tag: 5D67PN
kind: algorithm
slug: variable-type-analysis
name: Variable type analysis
aliases:
- VTA
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Prune a sound call graph by pushing the classes of new along the assignments of a type propagation graph and keeping the targets that reach each receiver.
solves: [call-graph-construction]
model: word-ram
complexity:
  vars: {n: the size of the program, K: the number of classes, P: the number of edges of the initial call graph}
  time: {worst: O((n + P) K)}
  space: {extra: O((n + P) K)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 2000
  people: [Vijay Sundaresan, Laurie Hendren, Chrislain Razafimahefa, Raja Vallee-Rai, Patrick Lam, Etienne Gagnon, Charles Godin]
  note: Sundaresan and others introduced variable type analysis at OOPSLA 2000 as part of the Soot framework for Java.
prereqs: [rapid-type-analysis, tarjan-scc]
see_also: [class-hierarchy-analysis, points-to-analysis, andersen-analysis, field-sensitivity, devirtualization, call-graph-construction]
sources:
  - paper: doi:10.1145/353171.353189
    title: Vijay Sundaresan, Laurie Hendren, Chrislain Razafimahefa, Raja Vallee-Rai, Patrick Lam, Etienne Gagnon and Charles Godin, Practical virtual method call resolution for Java, Proceedings of OOPSLA 2000, 264 to 280
    locator: the type propagation graph, the collapse of strongly connected components, and the pruning of a conservative initial call graph
  - paper: doi:10.1145/353171.353190
    title: Frank Tip and Jens Palsberg, Scalable propagation-based call graph construction algorithms, Proceedings of OOPSLA 2000, 281 to 293
    locator: the related propagation-based algorithms with one set of classes per method, per field or per class
  - paper: doi:10.1145/506315.506316
    title: David Grove and Craig Chambers, A framework for call graph construction algorithms, ACM Transactions on Programming Languages and Systems 23(6), 685 to 746, 2001
    locator: the lattice of call graph algorithms and the place of flow-insensitive type propagation in it
---

Variable type analysis (VTA) is a solution of [call graph construction](/call-graph-construction/) that tracks, for each variable and each field, the set of classes whose objects may reach it. It starts from a sound call graph, such as the one of [rapid type analysis](/rapid-type-analysis/) or [class hierarchy analysis](/class-hierarchy-analysis/). It builds a graph with an edge for each assignment and for each argument and result passing along the initial call edges. It puts the class of each `new` into its variable, and pushes the classes along the edges after collapsing the cycles. A call `y.m(z)` then keeps only the initial edges that a class reaching `y` explains. The result is sound, and it is inside the initial graph.

## In plain words

Rapid type analysis keeps one list of created classes for the whole program. So if the program creates a `Circle` in one place and a `Square` in another, every variable of type `Shape` may hold both. Variable type analysis keeps one list per variable. When the code says `a = new Circle()`, it writes Circle into the list of `a`. When the code says `b = a`, everything in the list of `a` also goes into the list of `b`. Calls pass lists into parameters and back out of results, along the calls that an earlier, rougher call graph found. When the lists stop growing, a call `a.grow()` keeps only the methods that the classes in the list of `a` really run.

## The problem

The input is a program in the model of [class hierarchy analysis](/class-hierarchy-analysis/), with the dispatch function $\mathrm{LOOKUP}(C, m)$, and a sound initial call graph $(R_0, E_0)$ whose edges start in methods of $R_0$ and end in methods of $R_0$. The type propagation graph $G$ has a node $M.v$ for each variable $v$ of each method $M \in R_0$ and a node $f$ for each field name. Its edges are $M.y \to M.x$ for `x = y`, $f \to M.x$ for `x = y.f`, $M.z \to f$ for `y.f = z`, and for each $(s, T) \in E_0$ with $s$: `x = y.m(z)` in $M$, the edges $M.y \to T.this$, $M.z \to T.p$ and $T.ret \to M.x$. The seed of $M.x$ is the set of classes $C$ with `x = new C()` in $M$.

The types are the least $\tau$ with $\mathrm{seed}(v) \subseteq \tau(v)$ and $\tau(v) \subseteq \tau(w)$ for every edge $v \to w$. The output keeps the edges $(s, T) \in E_0$, $s$: `x = y.m(z)` in $M$, for which some $C \in \tau(M.y)$ has $\mathrm{LOOKUP}(C, m) = T$, and then the part of them reachable from `main`.

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | maps from the nodes of $G$ to sets of classes |
| order | pointwise inclusion (bottom is precise) |
| join | pointwise union |
| bottom and top | every node maps to $\emptyset$, and every node maps to all classes |
| boundary value | the seeds from the `new` statements |
| initial value | the seeds |
| transfer | $\tau(w) \supseteq \tau(v)$ for each edge $v \to w$; distributive, since it copies sets |

## The algorithm

```pseudo id=main
VTA(P, R0, E0)
L1  make a node M.v for each variable v of each method M in R0, and a node f for each field
L2  for each x = y in a method M of R0 do add the edge M.y -> M.x
L3  for each x = y.f do add f -> M.x; for each y.f = z do add M.z -> f
L4  for each (s, T) in E0 with s: x = y.m(z) in M do add M.y -> T.this, M.z -> T.p, T.ret -> M.x
L5  for each x = new C() in a method M of R0 do add C to types(M.x)
L6  find the strongly connected components of the graph with Tarjan's algorithm
L7  for each component c in topological order do
L8      for each edge from c to another component d do types(d) <- types(d) ∪ types(c)
L9  E <- {(s, T) in E0 : s: x = y.m(z) in M, and some C in types(M.y) has LOOKUP(C, m) = T}
L10 R <- the methods reachable from main along E; drop from E the edges of sites outside R
L11 return (R, E)
```

Line L6 uses [Tarjan's algorithm](/tarjan-scc/). All nodes of one component get the same types, the union of their seeds. Line L7 visits the components so that every component comes after all components with an edge into it. So when line L8 pushes the types of a component, they are final, and each edge is used once. Line L10 removes the methods that only pruned edges reached.

## Example

The program of the [call graph construction](/call-graph-construction/) page, with the initial graph of [rapid type analysis](/rapid-type-analysis/):

```
class Shape          { Shape grow() { return this; } }
class Circle : Shape { Shape grow() { return new Square(); } }
class Square : Shape { Shape grow() { return this; } }
class Oval : Circle  { }

main() {
  Shape a = new Circle();
  Shape b = new Square();
  Shape c = a.grow();      // site s1
  Shape d = b.grow();      // site s2
  Shape e = c.grow();      // site s3
}
```

$R_0$ is `main`, `Circle.grow` and `Square.grow`, and $E_0$ links each of s1, s2 and s3 to both `grow` methods. The graph has these edges: from each receiver `a`, `b` and `c` to `Circle.this` and `Square.this`; from `Circle.ret` and `Square.ret` to each result `c`, `d` and `e`; and `Square.this` to `Square.ret` for `return this`. The seeds are $\{Circle\}$ for `a`, $\{Square\}$ for `b` and $\{Square\}$ for `Circle.ret`.

| node | types | why |
|---|---|---|
| `a` | Circle | seed |
| `b` | Square | seed |
| `Circle.ret` | Square | seed |
| `c`, `Square.this`, `Square.ret` | Circle, Square | one component: `c` to `Square.this` to `Square.ret` to `c`; it gets Circle from `a`, and Square from `b` and `Circle.ret` |
| `Circle.this` | Circle, Square | from `a`, `b` and `c` |
| `d`, `e` | Circle, Square | from both results |

Line L9 keeps s1 to `Circle.grow` (the types of `a`), s2 to `Square.grow` (the types of `b`), and s3 to both methods (the types of `c`). That is 4 edges, against 6 for RTA and 9 for CHA. The run makes 3 calls: s1 to `Circle.grow`, and s2 and s3 to `Square.grow`. The edge from s3 to `Circle.grow` is spurious. It comes from the spurious RTA edge from s1 to `Square.grow`: along it, the Circle of `a` flows into `Square.this`, then to `Square.ret` and back into `c`. Starting from the CHA graph gives the same 4 edges here.

## Correctness

**The types.** The least solution maps each node $w$ to the union of the seeds of the nodes that reach $w$. Nodes of one component reach each other, so they share their types. Taking the components in topological order, each component receives the final types of all components with an edge into it, so it ends with the union of the seeds of all nodes that reach it.

**Soundness.** Take a well-typed program without reflection or native code, and a sound initial graph. By induction over the steps of a run, if a variable $v$ of a frame of $M$ holds an object of class $C$, then $C \in \tau(M.v)$, and the same holds for fields. A `new` is a seed. A copy, a load and a store follow an edge of $G$, because all objects share the one node of each field. A call from $s$ to $T$ is an edge of $E_0$, since $E_0$ is sound, so line L4 made the edges that carry the receiver, the argument and the result. So at a call, the class $C$ of the receiver is in $\tau(M.y)$, the target is $\mathrm{LOOKUP}(C, m)$, and line L9 keeps the edge. The caller is in $R$ by induction, so line L10 keeps it too.

**Nesting.** Line L9 keeps a subset of $E_0$, so $\mathrm{VTA} \subseteq \mathrm{RTA} \subseteq \mathrm{CHA}$ when the initial graph is the RTA graph. A larger initial graph gives a larger graph $G$, larger types and a larger result. The full proofs are in the proof file.

## Complexity

**Proved.** The graph has $O(n)$ nodes and at most $n + 3P$ edges, for $P = |E_0|$. Building it and running Tarjan's algorithm take $O(n + P)$. Line L8 takes one union of sets of at most $K$ classes per edge, in $O(K)$ with bit vectors. Line L9 checks at most $K$ classes per edge of $E_0$. So the time is $O((n + P) K)$, and the space for the types is $O(n K)$, plus $O(n + P)$ for the graph.

**Measured, not proved.** On 400 random well-typed programs (seed 2000), the result equals that of a plain iteration of the edges until nothing changes. On 300 random programs with 5 concrete runs each (seed 79), every call that a run makes is in $E$. On 300 random programs (seed 7), $\mathrm{VTA} \subseteq \mathrm{RTA} \subseteq \mathrm{CHA}$, and VTA is strictly smaller than RTA on some of them. On 300 random programs (seed 8), the result from the RTA graph is inside the result from the CHA graph.

## Properties

- **Sound only if the initial graph is sound.** A call edge missing from $E_0$ means a missing parameter edge in line L4, so the types of the callee are too small.
- **Field-based.** One node per field name merges the field $f$ of all objects. This is what makes stores and loads sound without any alias information.
- **Context-insensitive and flow-insensitive.** All calls of a method share its parameter nodes, and the order of statements does not matter.
- **Monotone in the initial graph.** A smaller sound initial graph never gives a larger result. So running VTA again with its own result as the initial graph is sound and may prune more.
- **Classes, not objects.** The sets hold classes, so two objects of the same class are never told apart. A [points-to analysis](/points-to-analysis/) with allocation sites can tell them apart.

## Variants and improvements

- **Declared type analysis.** Sundaresan and others also describe a coarser variant with one node per declared type instead of one per variable. It is cheaper and less precise.
- **On-the-fly pruning.** Pass a class $C$ along $M.y \to T.this$ only if $\mathrm{LOOKUP}(C, m) = T$, and add call edges as types arrive instead of starting from $E_0$. This is a type-based form of [Andersen's analysis](/andersen-analysis/) with an on-the-fly call graph. On the example it removes the spurious edge from s3 and gives the exact 3 edges.
- **Per-method and per-field sets.** Tip and Palsberg propagate classes with one set per method, per field or per class. These lie between RTA and VTA.
- **Field-sensitive versions.** One node per field of each abstract object needs alias information, which leads to [field-sensitive](/field-sensitivity/) points-to analysis.

## When to use it

Use VTA when RTA leaves too many targets and you want a sound graph without a full points-to analysis. It costs one graph build, one pass of Tarjan's algorithm and one propagation pass, and it scales to large Java programs. It is a good input for [devirtualization](/devirtualization/) and for an interprocedural analysis that needs a tighter graph. When the precision of classes per variable is not enough, for example for collections that hold many classes, use a points-to analysis with context.

## Pitfalls

- **A field node per base variable.** Making a node for `x.f` instead of one node `f` in line L3 is unsound. With `x.f = a; y = x; b = y.f`, the class of `a` goes to `x.f` and never reaches `b`. Line L3 must use one node per field name, unless an alias analysis says which bases share objects.
- **Pruning with the declared type.** A version of line L9 that keeps the targets of every class $C \le \mathrm{decl}(y)$ is just CHA. Line L9 must test the classes in $\mathrm{types}(M.y)$.
- **An unsound initial graph.** If $E_0$ comes from a guess, such as the edges seen in a profile, line L4 misses parameter flows, and line L9 may drop real edges. $E_0$ must be sound, for example the result of line L12 of RTA.
- **Forgetting the result edge.** A version of line L4 without $T.ret \to M.x$ leaves `c` in the example with no types, and the real call from s3 to `Square.grow` is lost.
- **Claiming soundness with reflection.** Objects from reflection, deserialization or native code do not come from a `new` of the text, so line L5 has no seed for them.

## Implementations

## History

Sundaresan, Hendren, Razafimahefa, Vallee-Rai, Lam, Gagnon and Godin introduced variable type analysis and declared type analysis in 2000, as part of the Soot framework for Java. They built the type propagation graph on a conservative initial call graph, collapsed its strongly connected components, and used the result to resolve virtual calls. In the same year, Tip and Palsberg described a family of propagation-based algorithms that keep fewer sets. Grove and Chambers (2001) placed such algorithms in a general framework of call graph construction.

## References
