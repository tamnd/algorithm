---
tag: 4RD0AS
kind: problem
slug: call-graph-construction
name: Call graph construction
aliases:
- call graph analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: core
summary: Find a sound superset of the targets of each call site of a program with virtual or indirect calls, from type or pointer facts.
prereqs: [call-graph, subtyping]
see_also: [class-hierarchy-analysis, rapid-type-analysis, variable-type-analysis, points-to-analysis, zero-cfa, k-cfa, object-sensitivity, devirtualization]
sources:
  - paper: doi:10.1145/506315.506316
    title: David Grove and Craig Chambers, A framework for call graph construction algorithms, ACM Transactions on Programming Languages and Systems 23(6), 685 to 746, 2001
    locator: the lattice of call graphs, the parameterized family of algorithms (CHA, RTA, 0-CFA, k-CFA and others) and their measured precision and cost
  - paper: doi:10.1145/263698.264352
    title: David Grove, Greg DeFouw, Jeffrey Dean and Craig Chambers, Call graph construction in object-oriented languages, Proceedings of OOPSLA '97, SIGPLAN Notices 32(10), 108 to 124, 1997
    locator: the first form of the framework and the measurements on Cecil and Java programs
  - paper: doi:10.1007/3-540-49538-X_5
    title: Jeffrey Dean, David Grove and Craig Chambers, Optimization of object-oriented programs using static class hierarchy analysis, ECOOP '95, LNCS 952, 77 to 101, 1995
    locator: class hierarchy analysis and its use to bind message sends statically
  - paper: doi:10.1145/236337.236371
    title: David F. Bacon and Peter F. Sweeney, Fast static analysis of C++ virtual function calls, Proceedings of OOPSLA '96, 324 to 341, 1996
    locator: rapid type analysis and its comparison with class hierarchy analysis on C++ programs
  - paper: doi:10.1145/353171.353189
    title: Vijay Sundaresan, Laurie Hendren, Chrislain Razafimahefa, Raja Vallee-Rai, Patrick Lam, Etienne Gagnon and Charles Godin, Practical virtual method call resolution for Java, Proceedings of OOPSLA 2000, 264 to 280
    locator: variable type analysis and declared type analysis, built on a conservative call graph
  - paper: doi:10.1145/2644805
    title: Benjamin Livshits, Manu Sridharan, Yannis Smaragdakis, Ondrej Lhotak, J. Nelson Amaral, Bor-Yuh Evan Chang, Samuel Z. Guyer, Uday P. Khedker, Anders Moller and Dimitrios Vardoulakis, In defense of soundiness, a manifesto, Communications of the ACM 58(2), 44 to 46, 2015
    locator: whole paper (no practical whole-program analysis is sound for reflection, native code and dynamic loading)
  - paper: doi:10.1109/TSE.1979.234183
    title: Barbara G. Ryder, Constructing the call graph of a program, IEEE Transactions on Software Engineering SE-5(3), 216 to 226, 1979
    locator: call graphs of programs with procedure parameters
  - paper: "Olin Shivers, Control-Flow Analysis of Higher-Order Languages, or Taming Lambda, PhD thesis, Carnegie Mellon University, 1991, technical report CMU-CS-91-145"
    locator: the call graph problem for higher-order languages, and 0CFA and 1CFA as its solutions
  - paper: doi:10.1145/1291151.1291166
    title: David Van Horn and Harry G. Mairson, Relating complexity and precision in control flow analysis, Proceedings of ICFP 2007, 85 to 96
    locator: Theorem 2, the PTIME-completeness of 0-CFA
---

Call graph construction is the analysis that computes, for a program with virtual calls, function pointers or closures, a set of edges from call sites to procedures that contains every call that a run can make. The [call graph](/call-graph/) page defines the graph itself and its structure; this page is about the problem of computing a sound and precise superset of it when the text of a call does not name its callee. The exact answer is undecidable, so every algorithm over-approximates, and the algorithms form a ladder of precision and cost: [class hierarchy analysis](/class-hierarchy-analysis/) looks only at declared types, [rapid type analysis](/rapid-type-analysis/) also looks at which classes the program creates, [variable type analysis](/variable-type-analysis/) tracks the types that reach each variable, and analyses built on [points-to analysis](/points-to-analysis/) or control flow analysis ([0-CFA](/zero-cfa/), [k-CFA](/k-cfa/)) track values. Almost every interprocedural analysis needs a call graph first, and most of them get a better answer from a better graph.

## In plain words

In a program written with objects, the line `shape.area()` does not say which code runs. It depends on the class of the object that `shape` holds at run time. The same is true for a call through a function pointer or for a call of a function that was passed as an argument. A compiler wants to know, for each such call, the list of functions it can reach. The list may contain extra functions, but it must not miss one that a run calls. A cheap method looks only at the class tree and lists every class that could be below the declared type. Better methods also look at which objects the program creates and at how they move between variables. Shorter lists help the compiler more, and cost more time to find.

## Definition

**Input.** A program with a finite set $\Pi$ of procedures (methods or functions), a root $main \in \Pi$, and a finite set $S$ of call sites. Each site $s$ lies in one procedure $\mathrm{caller}(s)$. A site is *direct* if its text names its one callee, and *indirect* if the callee depends on a value: a virtual call `x = y.m(z)`, a call through a function pointer, or the application of a closure. For an object-oriented program the input also has a finite set of classes with a single-inheritance order $\le$ (where $C \le D$ means that $C$ is $D$ or a subclass of it), a declared type $\mathrm{decl}(y)$ for each variable, and a dispatch function $\mathrm{lookup}(C, m)$, the method that runs when $m$ is called on an object of class $C$.

**Output.** A pair $(R, E)$ with $R \subseteq \Pi$, the *reachable* procedures, and $E \subseteq S \times \Pi$, the call edges. The edge $(s, Q)$ says that site $s$ may call $Q$.

**Soundness.** For each run of the program, every procedure that the run enters is in $R$, and every pair $(s, Q)$ such that the run executes site $s$ and enters $Q$ there is in $E$. The *exact* call graph is the union of these facts over all runs. A sound output contains the exact graph.

**Precision.** Order outputs by inclusion of both parts. Of two sound outputs, the smaller one is more precise.

**Assumptions.** Soundness is with respect to a closed world: the analysis sees the whole program, and calls happen only through the call sites of the program text. Reflection, which looks up a method by a string at run time, native code that calls back, and classes loaded at run time all break this. No practical tool is sound for them, and Livshits and others (2015) name the usual compromise *soundiness*: a tool is sound except for a listed set of such features. Every soundness claim on the pages of this group holds under these assumptions and no other.

**As a fixed point.** Most algorithms compute the least $(R, E)$ that is closed under two rules: $main \in R$, and for each site $s$ with $\mathrm{caller}(s) \in R$ and each $Q \in T(s)$, $(s, Q) \in E$ and $Q \in R$. Here $T(s)$ is the algorithm's approximation of the targets of $s$, and it may itself depend on $R$ and $E$. The analysis in the terms of a data-flow framework:

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | pairs $(R, E)$ with $R \subseteq \Pi$ and $E \subseteq S \times \Pi$ |
| order | inclusion of both parts (bottom is precise) |
| join | union of both parts |
| bottom and top | $(\emptyset, \emptyset)$ and $(\Pi, S \times \Pi)$ |
| boundary value | $main \in R$ |
| initial value | $R = \{main\}$, $E = \emptyset$ |
| transfer | the two closure rules; monotone when $T(s)$ grows with $(R, E)$ |

## Variants

- **By the model of the receiver.** Name-based resolution keeps every method called $m$. [Class hierarchy analysis](/class-hierarchy-analysis/) keeps the methods that $m$ dispatches to on classes below $\mathrm{decl}(y)$. [Rapid type analysis](/rapid-type-analysis/) keeps only classes that a reachable method creates. [Variable type analysis](/variable-type-analysis/) keeps the classes that reach $y$ along assignments. Points-to based construction keeps the classes of the abstract objects in the points-to set of $y$, as in [Andersen's analysis](/andersen-analysis/) run together with the call graph.
- **Context-sensitive.** The call graph of a context-sensitive analysis has nodes $(Q, c)$ for a procedure and a context $c$. Call strings give the [k-CFA](/k-cfa/) family; receiver objects give [object sensitivity](/object-sensitivity/). See [context sensitivity](/context-sensitivity/).
- **Higher-order functions.** In a functional language the callee is a closure. The problem becomes control flow analysis: which lambda terms can reach each application. [0-CFA](/zero-cfa/) is the base analysis.
- **Ahead of time or on the fly.** An algorithm can build a call graph first and then a points-to analysis over it, or it can build both together. On the fly is more precise, because an edge that the values never support is never added.
- **Whole program or library.** For a library the roots are all public methods, and the classes that client code may create are unknown. This changes the answer of every algorithm above.
- **Dynamic call graphs.** Recording the calls of test runs gives a subset of the exact graph. It is useful for profiling and unsound for optimization.

## Examples

In this Java-like program, `Oval` inherits `grow` from `Circle`, and no code creates a `Shape` or an `Oval`:

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

Every variable has the declared type `Shape`. The only run calls `Circle.grow` at s1 and `Square.grow` at s2 and s3.

| algorithm | s1 | s2 | s3 | edges | reachable methods |
|---|---|---|---|---|---|
| exact | Circle | Square | Square | 3 | main, Circle.grow, Square.grow |
| class hierarchy analysis | Shape, Circle, Square | Shape, Circle, Square | Shape, Circle, Square | 9 | main and all three `grow` |
| rapid type analysis | Circle, Square | Circle, Square | Circle, Square | 6 | main, Circle.grow, Square.grow |
| variable type analysis on the RTA graph | Circle | Square | Circle, Square | 4 | main, Circle.grow, Square.grow |

The class hierarchy analysis keeps `Shape.grow` because a `Shape` could exist. Rapid type analysis drops it because no reachable code creates a `Shape`. Variable type analysis sees that only a `Circle` reaches `a` and only a `Square` reaches `b`. It keeps the extra target at s3 because the spurious RTA edge from s1 to `Square.grow` carries a `Circle` into that method's `this` and back out of its return into `c`.

## Known algorithms

| algorithm | what it tracks | worst-case time |
|---|---|---|
| [class hierarchy analysis](/class-hierarchy-analysis/) | declared types and the class tree | $O(|S| \cdot |K|)$ for $|K|$ classes, after a dispatch table is built |
| [rapid type analysis](/rapid-type-analysis/) | also the set of created classes | $O(|S| \cdot |K| + n)$ |
| [variable type analysis](/variable-type-analysis/) | the classes that reach each variable and field | $O((n + |E_0|) \cdot |K|)$ after an initial call graph with $|E_0|$ edges |
| [Andersen's analysis](/andersen-analysis/), on the fly | abstract objects per variable and field | $O(n^3)$ |
| [0-CFA](/zero-cfa/) | the lambda terms that reach each expression | $O(n^3)$ |
| [k-CFA](/k-cfa/) for $k \ge 1$ | closures with the last $k$ call sites | exponential in $n$; EXPTIME-complete |
| [object sensitivity](/object-sensitivity/) | abstract objects with their allocation context | polynomial for a fixed depth |

Here $n$ is the size of the program. The first three are the classic algorithms for object-oriented programs, and the bounds are those proved on their pages.

## Bounds

- **The exact call graph is undecidable.** Take any program $P$ and build `main() { P(); t(); }` with a direct call to a new procedure `t`. The edge from `main` to `t` is in the exact graph if and only if $P$ halts, so the [halting problem](/halting-problem/) reduces to the question. This holds even with no indirect calls: exact means over all runs, and that is a semantic property ([Rice's theorem](/rice-theorem/)). So all algorithms are sound over-approximations, and precision is measured, not proved optimal.
- **Linear time for declared types.** Class hierarchy analysis needs only the text and the class tree. It is linear in the size of the program times the number of classes, and close to linear in practice.
- **Cubic time for value flow.** With closures, the [0-CFA](/zero-cfa/) form of the problem takes $O(n^3)$ time, and Van Horn and Mairson (2007) proved that it is complete for polynomial time. So it is unlikely to be solvable in polylogarithmic parallel time.
- **Exponential time with call strings.** [k-CFA](/k-cfa/) for any fixed $k \ge 1$ is complete for EXPTIME ([the k-CFA EXPTIME-completeness theorem](/k-cfa-exptime-completeness/)). The object-oriented form of $k$-CFA is polynomial, because an object stores its fields in one context.

## Reductions

- **Points-to analysis gives a call graph.** The targets of `y.m()` are $\{\mathrm{lookup}(C, m)\}$ for the classes $C$ of the abstract objects in the points-to set of $y$. The targets of a call through a function pointer are the functions in its points-to set.
- **A call graph is needed for points-to analysis.** Parameters receive values only along call edges. So the two analyses depend on each other, and the precise solution computes both as one least fixed point.
- **Graph reachability reduces to it.** For a directed graph, make one procedure per vertex, with a direct call from $u$ to $v$ for each edge. The reachable procedures are the vertices reachable from the root. So any algorithm must take at least linear time.
- **Control flow analysis is call graph construction for closures.** The application $(e_1\ e_2)$ is a call site, and the lambda terms that reach $e_1$ are its targets.

## Applications

- **Devirtualization and inlining.** A site with one target can become a direct call ([devirtualization](/devirtualization/)) and then be inlined ([function inlining](/function-inlining/)).
- **Dead method removal.** Methods outside $R$ are never called, so a whole-program compiler can remove them ([dead code elimination](/dead-code-elimination/)).
- **Interprocedural analysis.** [Interprocedural data-flow analysis](/interprocedural-dataflow-analysis/), the [IFDS framework](/ifds-framework/), [mod-ref analysis](/mod-ref-analysis/) and [escape analysis](/escape-analysis/) all walk the call graph.
- **Tools.** Security and bug-finding tools, refactoring tools and IDE "find callers" features start from a call graph.

## References
