---
tag: CFKXHW
kind: technique
slug: object-sensitivity
name: Object sensitivity
aliases:
- object-sensitive pointer analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Context-sensitive pointer analysis for object-oriented code that tells calls apart by the allocation sites of their receiver objects.
prereqs: [andersen-analysis, context-sensitivity]
see_also: [k-cfa, k-cfa-exptime-completeness, points-to-analysis, call-graph-construction, devirtualization, escape-analysis, datalog-program-analysis]
sources:
  - paper: doi:10.1145/1044834.1044835
    title: Ana Milanova, Atanas Rountev and Barbara G. Ryder, Parameterized object sensitivity for points-to analysis for Java, ACM Transactions on Software Engineering and Methodology 14(1), 2005, 1 to 41
    locator: the definition of k-object-sensitive Andersen-style analysis for Java, its rules and its comparison with call-site sensitivity
  - paper: doi:10.1145/1926385.1926390
    title: Yannis Smaragdakis, Martin Bravenboer and Ondřej Lhoták, Pick your contexts well, understanding object-sensitivity, Proceedings of POPL 2011, 17 to 30
    locator: the framework with the two context functions Record and Merge, full object sensitivity, heap contexts, and type sensitivity
  - paper: doi:10.1145/1806596.1806631
    title: Matthew Might, Yannis Smaragdakis and David Van Horn, Resolving and exploiting the k-CFA paradox, Proceedings of PLDI 2010, 305 to 315
    locator: why context-sensitive analyses of object-oriented programs are polynomial for fixed context depth
---

Object sensitivity is a way to choose the contexts of a context-sensitive [points-to analysis](/points-to-analysis/) for object-oriented programs. A call-site sensitive analysis, like [k-CFA](/k-cfa/), analyses a method once for each string of the last $k$ call sites. An object-sensitive analysis analyses a method once for each *receiver object*, named by its allocation site, together with the allocation sites of the objects that created it. Milanova, Rountev and Ryder introduced it in 2002. It became the default for Java analysis because the methods of one object usually work on that object's data, so splitting by receiver keeps the data of different objects apart where it matters. For a fixed depth $k$, the analysis takes polynomial time, unlike functional k-CFA.

## In plain words

A simple pointer analysis looks at each method once. If two different lists call the same `add` method, their elements get mixed, and every list seems to hold every element. A context-sensitive analysis looks at a method several times, once for each context. With call sites as contexts, the context is where the call came from. With object sensitivity, the context is which object the method runs on. We do not know the real objects, so each object is named by the `new` statement that created it. Two lists made at two different `new` statements then get two copies of `add`, and their elements stay apart. To also separate objects made inside other objects, a name can include the creator's name as well.

## When it applies

- The program is object-oriented, with virtual calls on receivers, and most state lives in fields of objects.
- A context-insensitive analysis such as [Andersen's](/andersen-analysis/) merges the contents of containers, builders or wrapper objects that are created at different sites.
- The same objects are reached through several layers of helper calls, so call-site contexts would need a large $k$ to see past the helpers.
- The analysis can afford a constant factor more work. Object sensitivity with depth 2 often costs several times the context-insensitive analysis, and sometimes much more.

## The template

Notation: $C$ is the set of contexts, a context $c$ is a short sequence of allocation sites or call sites. An abstract object is a pair $(i, \hat h)$ of an allocation site $i$ and a heap context $\hat h$. $pts(x, c)$ is the points-to set of local $x$ in context $c$, and $pts(o.f)$ that of field $f$ of abstract object $o$. The two holes are RECORD, which picks the heap context of a new object, and MERGE, which picks the context of a callee.

```pseudo id=main
CONTEXT-SENSITIVE-POINTS-TO(P)
L1  mark (main, ()) reachable
L2  repeat
L3      for each reachable (m, c) and each statement of m do
L4          x = new T at site i:   add (i, RECORD(i, c)) to pts(x, c)
L5          x = y:                 add pts(y, c) to pts(x, c)
L6          x = y.f:               for each o in pts(y, c) do add pts(o.f) to pts(x, c)
L7          x.f = y:               for each o in pts(x, c) do add pts(y, c) to pts(o.f)
L8          r = x.g(a) at site s:  for each o = (i, h) in pts(x, c) do
L9              t <- the method g that the class of site i selects
L10             c' <- MERGE(o, s, c)
L11             add o to pts(this_t, c'); add pts(a, c) to pts(param_t, c'); add pts(ret_t, c') to pts(r, c)
L12             mark (t, c') reachable; add the edge (s, c) -> (t, c')
L13 until nothing changes
L14 return pts and the call edges
```

The template is an [Andersen-style](/andersen-analysis/) inclusion analysis that also builds the [call graph](/call-graph-construction/) on the fly, as at line L9. Each method is analysed once per reachable context, and each object is split by its heap context. The holes decide the precision.

| analysis | MERGE((i, h), s, c) | RECORD(i, c) |
|---|---|---|
| context-insensitive | () | () |
| k-call-site sensitive | the last k elements of c followed by s | the last h elements of c |
| k-object sensitive (full) | the last k elements of (i followed by h) | the last k - 1 elements of c |
| k-type sensitive | the last k elements of (the class that contains site i, followed by h) | the last k - 1 elements of c |

For a static call, there is no receiver. Object-sensitive analyses usually let the callee inherit the caller's context $c$ at line L10.

All instances are sound for programs without reflection, native code and dynamic class loading, by the same argument as Andersen's analysis: each rule over-approximates the matching step of a run, for every choice of contexts, because a context only splits facts and never drops one. With $H$ allocation sites, $S$ call sites and fixed $k$, there are at most $(H + S)^k$ contexts and $H^{k}$ heap contexts, so the number of facts and the running time are polynomial. This is the reason, explained by Might, Smaragdakis and Van Horn, that these analyses avoid the [EXPTIME-hardness](/k-cfa-exptime-completeness/) of functional k-CFA: an abstract object has one heap context for all its fields, so environments are flat.

## Classic examples

**A box behind a helper.** In this Java code, `put` calls `set`.

```
class Box {
  Object v;
  void set(Object x) { this.v = x; }
  void put(Object x) { this.set(x); }    // site s0
  Object get() { return this.v; }
}
Box b1 = new Box();      // o1
Box b2 = new Box();      // o2
b1.put(new A());         // oA, site s1
b2.put(new B());         // oB, site s2
Object a = b1.get();     // site s3
```

A context-insensitive analysis gives $pts(o1.v) = pts(o2.v) = \{oA, oB\}$, so $a$ may point to $oB$. With 1-call-site sensitivity, `put` is split by $s_1$ and $s_2$, but `set` is called only from $s_0$, so its parameter $x$ again holds $\{oA, oB\}$ and the fields are mixed. With 1-object sensitivity, `put` and `set` run in context $[o1]$ when the receiver is `b1` and in $[o2]$ for `b2`. So $pts(o1.v) = \{oA\}$, $pts(o2.v) = \{oB\}$ and $pts(a) = \{oA\}$, which is exact.

**Context-insensitive analysis.** With both holes returning the empty context, the template is [Andersen's analysis](/andersen-analysis/) with an on-the-fly call graph. It is the baseline that every context-sensitive choice refines.

**Call strings.** With MERGE adding the call site, the template is the k-call-site analysis of Java tools. In a functional language with closures, the same idea is [k-CFA](/k-cfa/), which is EXPTIME-complete for $k \ge 1$. In Java it is polynomial, because objects copy their fields and have one heap context.

**Clients.** Precise points-to sets give a precise call graph, which drives [devirtualization](/devirtualization/) and [escape analysis](/escape-analysis/). Declarative engines such as Doop write the template as [Datalog rules](/datalog-program-analysis/), and the holes are two small Datalog functions.

## Variations

- **Heap contexts.** With RECORD returning the empty context, all objects made at one site in a factory or a container are one abstract object. "2-object sensitive with a 1-object heap context" (2obj+1H), which keeps the creator of each object, is a common sweet spot in the Smaragdakis, Bravenboer and Lhoták study.
- **Full and plain object sensitivity.** Full object sensitivity uses the allocation site of the receiver and of the receiver's creator, as in the table. Other variants mix in the allocation site of the caller's receiver. Smaragdakis, Bravenboer and Lhoták show that these choices differ in precision and cost, and they recommend the full form.
- **Type sensitivity.** Replace each allocation site in a context by the class that contains it. Contexts become coarser and fewer, which costs a little precision and saves much time.
- **Selective and hybrid contexts.** Use object sensitivity for virtual calls and call-site sensitivity for static calls, or apply context sensitivity only to the methods where a pre-analysis predicts it helps.
- **Field sensitivity and parameterization.** Milanova and colleagues allow different depths for different parts of the program. Object sensitivity is usually combined with [field sensitivity](/field-sensitivity/).

## Pitfalls

- **Forgetting the heap context.** With RECORD empty, two lists that each allocate their internal node array at the same site share one node array, and their elements mix, whatever the method context is.
- **Wrong context for static calls.** A static call has no receiver. Giving the callee an empty context merges all callers. Inheriting the caller's context keeps the precision.
- **Comparing by depth only.** 1-object and 1-call-site sensitivity are incomparable: each is more precise on some programs. A larger $k$ is not always more precise either, when the contexts are truncated in different places.
- **Expecting low cost from small $k$.** The number of contexts can grow as $H^k$, and 2-object or 3-object sensitivity can run out of time or memory on large programs. Measure, and consider type sensitivity.
- **Claiming soundness with reflection.** All forms are sound only for code without reflection, native methods and dynamic class loading. Real tools model these parts by hand or not at all.

## Exercises

1. In the box example, add a method `Box copy() { Box n = new Box(); n.v = this.v; return n; }` at allocation site $o3$, and call it as `b1.copy()` and `b2.copy()`. Show that 1-object sensitivity with an empty heap context makes `copy().get()` return both $oA$ and $oB$, and that a heap context of depth 1 fixes it.
2. Write a program where 1-call-site sensitivity is more precise than 1-object sensitivity. Hint: call one method on the same receiver from two sites with different arguments.
3. Fix $k$. Show that with $H$ allocation sites and $S$ call sites, the template derives at most a polynomial number of facts in $H + S$ and the number of variables and fields. Which part of the closure argument of k-CFA fails here?
4. Show that every instance of the template is sound for programs without reflection, by mapping each concrete object to the abstract object with its allocation site and the heap context that RECORD would give along the concrete call path.

## References
