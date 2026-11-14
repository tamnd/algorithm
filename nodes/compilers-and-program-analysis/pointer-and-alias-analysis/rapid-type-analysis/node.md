---
tag: D3EG6T
kind: algorithm
slug: rapid-type-analysis
name: Rapid type analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: core
summary: Build a call graph like class hierarchy analysis, but let a virtual call reach only the classes that some reachable method creates with new.
solves: [call-graph-construction]
model: word-ram
complexity:
  vars: {n: the size of the program, S: the number of call sites, K: the number of classes, M: the number of method names}
  time: {worst: O(n + S K + K M)}
  space: {extra: O(S K + K M)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 1996
  people: [David F. Bacon, Peter F. Sweeney]
  note: Bacon and Sweeney introduced rapid type analysis at OOPSLA 1996 to resolve C++ virtual calls statically.
prereqs: [class-hierarchy-analysis]
see_also: [variable-type-analysis, call-graph-construction, devirtualization, function-inlining, dead-code-elimination, points-to-analysis]
sources:
  - paper: doi:10.1145/236337.236371
    title: David F. Bacon and Peter F. Sweeney, Fast static analysis of C++ virtual function calls, Proceedings of OOPSLA '96, 324 to 341, 1996
    locator: the definition of rapid type analysis and its measured comparison with class hierarchy analysis on C++ programs
  - paper: doi:10.1145/353171.353190
    title: Frank Tip and Jens Palsberg, Scalable propagation-based call graph construction algorithms, Proceedings of OOPSLA 2000, 281 to 293
    locator: the constraint form of rapid type analysis, and the refinements that keep one set of classes per method, per field or per class
  - paper: doi:10.1145/506315.506316
    title: David Grove and Craig Chambers, A framework for call graph construction algorithms, ACM Transactions on Programming Languages and Systems 23(6), 685 to 746, 2001
    locator: rapid type analysis as a point of the framework between class hierarchy analysis and type propagation
---

Rapid type analysis (RTA) is a solution of [call graph construction](/call-graph-construction/) for object-oriented programs that refines [class hierarchy analysis](/class-hierarchy-analysis/) with one global set: the classes that the program creates. A virtual call `y.m(z)` may reach the method `m` of a class only if that class is at or below the declared class of `y` and some reachable method contains `new` of that class. The graph is built on the fly from `main`, so a class created only in dead code does not count. RTA costs about the same as CHA, it is sound for type-safe programs without reflection, and its graph is always inside the CHA graph.

## In plain words

Class hierarchy analysis assumes that a variable of type `Shape` can hold any kind of shape. But a program that never writes `new Oval()` can never hold an `Oval`. Rapid type analysis keeps a list of the classes that the program creates, and it only follows calls into methods of those classes. It starts at `main` and keeps a to-do list of methods to read. When a method creates a new class, the analysis goes back to the calls it has already seen and adds the new targets. When it sees a new call, it uses all the classes found so far. When the to-do list is empty, the graph is done.

## The problem

The input is a program in the model of [class hierarchy analysis](/class-hierarchy-analysis/): classes with single inheritance and the order $C \le D$, method bodies with `x = new C()`, `x = y`, `x = y.f`, `y.f = z` and virtual calls `x = y.m(z)` at sites $s$, a declared class $\mathrm{decl}(y)$ for each variable, the dispatch function $\mathrm{LOOKUP}(C, m)$ and the root `main`. The program is well typed. The output is the pair $(R, E)$ of the least triple $(R, I, E)$ of methods, classes and edges with these rules:

1. $main \in R$;
2. if a method of $R$ contains `x = new C()`, then $C \in I$;
3. if a method of $R$ contains the site $s$: `x = y.m(z)`, $C \in I$ and $C \le \mathrm{decl}(y)$, then $(s, \mathrm{LOOKUP}(C, m)) \in E$ and $\mathrm{LOOKUP}(C, m) \in R$.

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | triples $(R, I, E)$ of reachable methods, created classes and call edges |
| order | inclusion of all three parts (bottom is precise) |
| join | union of all three parts |
| bottom and top | $(\emptyset, \emptyset, \emptyset)$ and all methods, all classes, all edges |
| boundary value | $main \in R$ |
| initial value | $R = \{main\}$, $I = \emptyset$, $E = \emptyset$ |
| transfer | rules 2 and 3; monotone, not distributive, since rule 3 needs a site of $R$ and a class of $I$ at once |

## The algorithm

```pseudo id=main
RTA(P)
L1  R <- {main}; W <- [main]; E <- {}; I <- {}; S <- {}
L2  while W is not empty do
L3      take a method M from W
L4      for each statement x = new C() in M do
L5          if C is not in I then add C to I
L6              for each site s: x = y.m(z) in S with C <= decl(y) do
L7                  ADD(s, LOOKUP(C, m))
L8      for each call site s: x = y.m(z) in M do
L9          add s to S
L10         for each class C in I with C <= decl(y) do
L11             ADD(s, LOOKUP(C, m))
L12 return (R, E)

ADD(s, T)
L13 add (s, T) to E
L14 if T is not in R then add T to R and to W
```

$I$ holds the classes created so far, and $S$ holds the call sites seen so far. Lines L4 to L7 handle a class that appears late: every site seen before gets the targets for the new class. Lines L8 to L11 handle a site that appears late: it gets the targets for every class created before. So each pair of a site and a class is examined once, by whichever of the two arrives second. LOOKUP and the subclass test use tables built once, as in class hierarchy analysis.

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

| step | method taken | what happens | $W$ after the step |
|---|---|---|---|
| 1 | main | lines L4 to L7: $I = \{Circle, Square\}$, no sites seen yet; lines L8 to L11: s1, s2 and s3 each get edges to `Circle.grow` and `Square.grow` | Circle.grow, Square.grow |
| 2 | Square.grow | no `new`, no sites | Circle.grow |
| 3 | Circle.grow | `new Square()`, but Square is already in $I$ | empty |

The result has 3 reachable methods and 6 edges. Class hierarchy analysis gives 4 methods and 9 edges: RTA drops `Shape.grow`, because no reachable code creates a plain `Shape`, and it drops the 3 edges to it. The run makes 3 of the 6 edges: s1 to `Circle.grow`, and s2 and s3 to `Square.grow`. The edge from s1 to `Square.grow` is spurious, because RTA does not know that `a` holds only a `Circle`. [Variable type analysis](/variable-type-analysis/) removes it.

## Correctness

**Least solution.** Each class enters $I$ once and each site enters $S$ once. The invariant is: for each site in $S$ and each class in $I$ below its declared class, the edge is in $E$. Line L7 keeps it when a class arrives, and line L11 keeps it when a site arrives. When $W$ is empty, $S$ holds all sites of $R$ and $I$ holds all classes created in $R$, so the three rules hold. Every edge that the algorithm adds is forced by the rules, so the result is the least solution.

**Soundness.** Take a well-typed program without reflection, native code or classes loaded at run time. By induction over the steps of a run: every object is created by a `new` in a method that the run entered, which is in $R$, so its class is in $I$. At a call `y.m(z)`, the receiver has a class $C \in I$, and type safety gives $C \le \mathrm{decl}(y)$. So rule 3 puts the call in $E$ and the callee in $R$.

**Inside CHA.** The CHA result with $I$ set to all classes satisfies the three rules. The RTA result is the least triple that satisfies them, so it is inside the CHA result. The full proofs are in the proof file.

## Complexity

**Proved.** Each body is read once, which costs $O(n)$. Each pair of a site and a class is examined once, in line L6 or in line L10, with $O(1)$ work, which costs $O(S K)$. The dispatch table costs $O(K M)$ time and space. So the time is $O(n + S K + K M)$, with direct indexing for $R$, $I$ and $E$ (or hashing, in expectation). The space is $O(S K)$ for the edges and $O(K M)$ for the table. This is the same bound as CHA.

**Measured, not proved.** On 500 random well-typed programs with up to 7 classes (seed 1996), the result equals that of a plain round-robin iteration of the three rules. On 300 random programs with 5 concrete runs each (seed 78), every call that a run makes is in $E$. On 300 random programs (seed 6), the RTA graph is inside the CHA graph, and it is strictly smaller on some of them.

## Properties

- **Sound under type safety and a closed world.** The proof needs every object to come from a `new` of the analysed text.
- **Inside CHA.** For every program, $R_{RTA} \subseteq R_{CHA}$ and $E_{RTA} \subseteq E_{CHA}$.
- **One set for the whole program.** All variables share the same set $I$. A class created anywhere in reachable code is a possible receiver of every call whose declared type is above it.
- **Not distributive.** An edge needs a site and a class, which may come from different paths. So the analysis has a real fixed point, but it is reached in one pass over each method because of lines L6 and L7.

## Variants and improvements

- **Whole-program instantiation.** Count the classes created anywhere in the program text, not only in reachable methods. This needs no on-the-fly graph and gives a graph between RTA and CHA.
- **One set per method or per field.** Tip and Palsberg give each method, each field or each class its own set of classes and propagate classes along the call edges and field accesses. These variants lie between RTA and [variable type analysis](/variable-type-analysis/).
- **Type propagation per variable.** [Variable type analysis](/variable-type-analysis/) keeps a set of classes for each variable and field.
- **Points-to based graphs.** A [points-to analysis](/points-to-analysis/) keeps sets of allocation sites instead of classes and builds the call graph at the same time.
- **Dead code removal.** A method outside $R$ cannot run. A linker or a tree shaker can drop it ([dead code elimination](/dead-code-elimination/)).

## When to use it

Use RTA when you need a sound call graph for a whole program and CHA keeps too many targets, for example when the program uses a large library but creates few of its classes. RTA costs almost the same as CHA and has no per-variable state. It is a good initial graph for [variable type analysis](/variable-type-analysis/) or for a points-to analysis. If you analyse a library without its clients, every class that client code may create must be in $I$ from the start, and then RTA gains little over CHA.

## Pitfalls

- **No back-patching of earlier sites.** A version without lines L6 and L7 handles only the sites seen after a class is created. If `main` calls `a.m()` and only then reaches a method that creates a subclass `B` that overrides `m`, the edge to `B.m` is lost, and the graph is unsound. Lines L6 and L7 must revisit the sites in $S$ for each new class.
- **Objects that no `new` creates.** Reflection (`Class.newInstance`), deserialization, `clone` and native code create objects without a `new` statement in the text. Their classes never enter $I$ in line L5, and the calls on them are missing. Add these classes to $I$ by hand or treat the program as outside the soundness claim.
- **Forgetting the constructor and static calls.** In a real language, `new C()` also calls the constructor of $C$ and its superclasses, and the first use of $C$ may run its static initializer. These are direct calls. Add them to $E$ and their methods to $R$ when line L5 runs, or the methods they call are missed.
- **Testing the class of the declared type only.** Line L10 must test $C \le \mathrm{decl}(y)$ for every created class, not $C = \mathrm{decl}(y)$. A variable declared as `Shape` can hold a `Circle`.

## Implementations

## History

Bacon and Sweeney introduced rapid type analysis in 1996. They compared it with class hierarchy analysis and with name-based resolution on C++ programs, and found that keeping only the created classes resolves many more virtual calls at almost the same cost. Tip and Palsberg (2000) wrote RTA as a set of constraints and refined it with separate sets of classes per method, per field and per class. Grove and Chambers (2001) placed RTA in a framework of call graph algorithms between class hierarchy analysis and full type propagation.

## References
