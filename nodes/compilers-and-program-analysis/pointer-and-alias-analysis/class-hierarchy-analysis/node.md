---
tag: M6WV8Z
kind: algorithm
slug: class-hierarchy-analysis
name: Class hierarchy analysis
aliases:
- CHA
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: core
summary: Build a call graph from declared types. A virtual call y.m() may reach the method m of every class at or below the declared class of y.
solves: [call-graph-construction]
model: word-ram
complexity:
  vars: {n: the size of the program, S: the number of call sites, K: the number of classes, M: the number of method names}
  time: {worst: O(n + S K + K M)}
  space: {extra: O(S K + K M)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 1995
  people: [Jeffrey Dean, David Grove, Craig Chambers]
  note: Dean, Grove and Chambers described class hierarchy analysis at ECOOP 1995 and used it to bind message sends statically.
prereqs: [call-graph-construction, subtyping]
see_also: [rapid-type-analysis, variable-type-analysis, devirtualization, function-inlining, call-graph, polymorphic-inline-cache]
sources:
  - paper: doi:10.1007/3-540-49538-X_5
    title: Jeffrey Dean, David Grove and Craig Chambers, Optimization of object-oriented programs using static class hierarchy analysis, ECOOP '95, LNCS 952, 77 to 101, 1995
    locator: the definition of class hierarchy analysis and its use to bind message sends statically
  - paper: doi:10.1145/236337.236371
    title: David F. Bacon and Peter F. Sweeney, Fast static analysis of C++ virtual function calls, Proceedings of OOPSLA '96, 324 to 341, 1996
    locator: class hierarchy analysis for C++ and its measured comparison with rapid type analysis
  - paper: doi:10.1145/506315.506316
    title: David Grove and Craig Chambers, A framework for call graph construction algorithms, ACM Transactions on Programming Languages and Systems 23(6), 685 to 746, 2001
    locator: class hierarchy analysis as the cheapest point of the framework, and its measured precision
  - paper: doi:10.1145/353171.353189
    title: Vijay Sundaresan, Laurie Hendren, Chrislain Razafimahefa, Raja Vallee-Rai, Patrick Lam, Etienne Gagnon and Charles Godin, Practical virtual method call resolution for Java, Proceedings of OOPSLA 2000, 264 to 280
    locator: class hierarchy analysis as the conservative initial call graph of the Soot framework
---

Class hierarchy analysis (CHA) solves [call graph construction](/call-graph-construction/) for object-oriented programs from the class tree and the declared types alone. At a virtual call `y.m(z)`, the object in `y` has a class at or below the declared class of `y`, so the call may reach the method that `m` dispatches to on any of those classes. The analysis starts at `main`, adds these targets as edges, and scans each newly reached method once. It runs in time close to linear in the size of the program, it is sound for any type-safe program without reflection, and it is the base that [rapid type analysis](/rapid-type-analysis/) and [variable type analysis](/variable-type-analysis/) refine.

## In plain words

When a program calls `shape.area()`, the variable `shape` is declared as a `Shape`. The language promises that the object in it is a `Shape` or an object of a class below `Shape` in the class tree. So the call can only run one of the `area` methods that those classes use. Class hierarchy analysis lists exactly those methods. It does this for each call in each method that `main` can reach, and it adds each new method it finds to a to-do list. When the list is empty, the result is a call graph. It never misses a real call, as long as the program does not use tricks such as reflection. It may list calls that never happen, because it does not ask which objects the program creates.

## The problem

The input is a program in the model of the [call graph construction](/call-graph-construction/) page: a set of classes with single inheritance, where $C \le D$ means that $C$ is $D$ or a class below it; for each method name $m$ the class $\mathrm{decl}(m)$ that introduces it; method bodies with the statements `x = new C()`, `x = y`, `x = y.f`, `y.f = z` and the virtual call `x = y.m(z)` at a site $s$; a declared class $\mathrm{decl}(y)$ for each variable; and the root `main`. The program is *well typed*: an assignment puts a value of class $C$ into a variable or field of declared class $D$ only if $C \le D$, and a call `y.m(z)` has $\mathrm{decl}(y) \le \mathrm{decl}(m)$.

$\mathrm{LOOKUP}(C, m)$ is the method that runs when $m$ is called on an object of class $C$: the definition of $m$ in $C$ or in the nearest class above $C$ that defines it. The CHA targets of a site $s$: `x = y.m(z)` are

$$T_{CHA}(s) = \{\mathrm{LOOKUP}(C, m) : C \le \mathrm{decl}(y)\}.$$

The output is the least pair $(R, E)$ such that $main \in R$, and for each site $s$ in a method of $R$ and each $T \in T_{CHA}(s)$, $(s, T) \in E$ and $T \in R$.

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | pairs $(R, E)$ of reachable methods and call edges |
| order | inclusion of both parts (bottom is precise) |
| join | union of both parts |
| bottom and top | $(\emptyset, \emptyset)$ and all methods with all edges |
| boundary value | $main \in R$ |
| initial value | $R = \{main\}$, $E = \emptyset$ |
| transfer | the closure rule above; monotone, and distributive since $T_{CHA}$ does not depend on $(R, E)$ |

## The algorithm

```pseudo id=main
CHA(P)
L1  R <- {main}; W <- [main]; E <- {}
L2  while W is not empty do
L3      take a method M from W
L4      for each call site s: x = y.m(z) in M do
L5          for each class C with C <= decl(y) do
L6              T <- LOOKUP(C, m)
L7              add (s, T) to E
L8              if T is not in R then add T to R and to W
L9  return (R, E)

LOOKUP(C, m)
L10 while C does not define m do C <- parent(C)
L11 return the method m of C
```

Each method enters $W$ once, when it first enters $R$ (line L8), so each body is scanned once. Line L5 needs the set of classes below each class. The implementation builds it once, together with a table of $\mathrm{LOOKUP}(C, m)$ for every class $C$ below $\mathrm{decl}(m)$, so lines L5 and L6 cost $O(1)$ per class. The loop of line L10 always stops, because $C \le \mathrm{decl}(y) \le \mathrm{decl}(m)$ and $\mathrm{decl}(m)$ defines $m$.

## Example

The program of the [call graph construction](/call-graph-construction/) page:

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

The classes at or below `Shape` are `Shape`, `Circle`, `Square` and `Oval`. $\mathrm{LOOKUP}(Oval, grow)$ walks up to `Circle.grow`. So $T_{CHA}(s) = \{Shape.grow, Circle.grow, Square.grow\}$ for all three sites, since all three receivers are declared as `Shape`.

| step | method taken | what happens | $W$ after the step |
|---|---|---|---|
| 1 | main | s1, s2 and s3 each get the 3 edges; the 3 `grow` methods enter $R$ | Shape.grow, Circle.grow, Square.grow |
| 2 | Square.grow | no call sites | Shape.grow, Circle.grow |
| 3 | Circle.grow | no call sites | Shape.grow |
| 4 | Shape.grow | no call sites | empty |

The result has 4 reachable methods and 9 edges. The only run makes 3 calls: s1 to `Circle.grow`, and s2 and s3 to `Square.grow`. `Shape.grow` is in $R$ although no code creates a `Shape`. [Rapid type analysis](/rapid-type-analysis/) removes it.

## Correctness

**Soundness.** In a well-typed program without reflection, native callbacks or classes loaded at run time, every method that a run enters is in $R$, and every call that a run makes is in $E$. The key fact is *type safety*: at every moment of a run, each variable and field of declared class $D$ holds null or an object of a class $C \le D$. So when site $s$: `x = y.m(z)` runs in a method of $R$, the receiver has a class $C \le \mathrm{decl}(y)$, and the method that runs is $\mathrm{LOOKUP}(C, m) \in T_{CHA}(s)$. By induction over the calls of the run, the caller is in $R$, so the edge is in $E$ and the callee is in $R$.

**Least solution.** The algorithm adds only edges that the closure rule forces, and when $W$ is empty, every method of $R$ has been scanned, so the rule holds. So the result is the least closed pair. The full proof is in the proof file.

## Complexity

**Proved.** Let $h$ be the height of the class tree. The table of LOOKUP has at most $K M$ entries. Filled top-down, each entry copies the entry of the parent or takes the class's own method, so it takes $O(K M)$ time; the implementation calls LOOKUP for each entry, which takes $O(K M h)$. Each method is scanned once, which costs $O(n)$ over the program. Each call site loops over at most $K$ classes with $O(1)$ work each, which costs $O(S K)$. So the time is $O(n + S K + K M)$, with hash sets for $R$ and $E$ (in expectation) or arrays indexed by method and site (worst case). The space is $O(K M)$ for the table and $O(S K)$ for the edges.

**Measured, not proved.** On 500 random well-typed programs with up to 7 classes, the result equals that of a plain round-robin iteration of the closure rule. On 300 random programs with 5 concrete runs each (seed 77), every call that a run makes is in $E$.

## Properties

- **Sound under type safety.** The proof uses only the declared types. A language with unchecked casts, such as C++ with `static_cast` on a wrong type, breaks it.
- **Independent of the values.** $T_{CHA}(s)$ depends on the text of the site, not on what the program creates or assigns. So the transfer is distributive, and the answer for a site does not change when other code changes, as long as the class tree is the same.
- **Least precise of the classic three.** For every program, the call graph of [rapid type analysis](/rapid-type-analysis/) and that of [variable type analysis](/variable-type-analysis/) are subsets of the CHA graph. The proofs are on their pages.
- **Single target.** If $T_{CHA}(s)$ has one method, the call can become a direct call ([devirtualization](/devirtualization/)) with no run-time test.

## Variants and improvements

- **Name-based resolution.** Keep every method called $m$, whatever the class. This needs no class tree and is weaker than CHA.
- **Rapid type analysis.** Keep only the classes that some reachable method creates ([rapid type analysis](/rapid-type-analysis/)).
- **Type propagation.** Track the classes that reach each variable ([variable type analysis](/variable-type-analysis/)), or the abstract objects of a [points-to analysis](/points-to-analysis/).
- **Interfaces and multiple inheritance.** For a Java interface, the classes below it are the classes that implement it and their subclasses. For C++ with multiple inheritance, LOOKUP must search several paths and report an ambiguity.
- **Specialization.** A compiler can make a copy of a method for a group of receiver classes. Inside the copy, `this` has a smaller set of classes below it, so more calls on `this` have one CHA target.
- **Guarded inlining in a JIT.** A just-in-time compiler can use CHA on the classes loaded so far, inline the single target, and record a dependency. When a new subclass is loaded, it throws the code away. See [inline caching](/inline-caching/) for the run-time alternative.

## When to use it

Use CHA when you need a sound call graph fast, for example as the first step of a whole-program optimizer, as the initial graph of variable type analysis, or in a tool that must answer at once. It needs no fixed point over values and scales to any program size. When the program creates few of the classes in its hierarchy, as with large libraries, use rapid type analysis, which costs almost the same. When the call graph feeds a precise analysis, such as an alias analysis, use a points-to based graph.

## Pitfalls

- **Missing inherited methods.** A version that, in line L5, loops only over the classes that *define* `m` misses calls of a method inherited from above $\mathrm{decl}(y)$. With `Oval o` and a call `o.grow()`, no class at or below `Oval` defines `grow`, but the call runs `Circle.grow`. Line L5 must loop over all classes below $\mathrm{decl}(y)$, and line L6 must walk up.
- **Scanning unreachable code.** Taking every method of the program as a root, instead of `main` in line L1, makes a sound graph with more edges. That is right for a library, whose public methods are all roots, and wrong for a whole program.
- **Claiming soundness with reflection.** A call through `Method.invoke` or a class loaded by name is not a call site of the text. The result of line L9 does not cover it. Treat such programs as unsound for CHA, or add the reflective targets by hand.
- **An open hierarchy.** If code that the analysis did not see can add subclasses, the set in line L5 is not complete. A compiler that devirtualizes on CHA must then guard the call or recompile when a class is loaded.

## Implementations

## History

Dean, Grove and Chambers described class hierarchy analysis in 1995, in their work on optimizing compilers for object-oriented languages, and used it to replace message sends with direct calls. Bacon and Sweeney (1996) measured it on C++ programs and showed that rapid type analysis removes many more virtual calls at almost the same cost. Grove, DeFouw, Dean and Chambers (1997), and Grove and Chambers (2001), placed CHA at the bottom of a lattice of call graph algorithms and measured the whole family on Cecil and Java programs. Sundaresan and others (2000) used CHA as the conservative initial call graph of the Soot framework for Java, on which variable type analysis builds.

## References
