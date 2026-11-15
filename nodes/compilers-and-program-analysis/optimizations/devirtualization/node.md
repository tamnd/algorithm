---
tag: KV05KE
kind: technique
slug: devirtualization
name: Devirtualization
aliases:
- call site specialization
area: compilers-and-program-analysis/optimizations
level: core
summary: Replaces a virtual or indirect call by a direct call when analysis shows one target, often guarded by a type test.
prereqs: [class-hierarchy-analysis, call-graph-construction]
see_also: [rapid-type-analysis, variable-type-analysis, points-to-analysis, type-feedback, inline-caching, polymorphic-inline-cache, deoptimization, function-inlining]
sources:
  - paper: doi:10.1007/3-540-49538-X_5
    title: "Jeffrey Dean, David Grove and Craig Chambers, Optimization of object-oriented programs using static class hierarchy analysis, ECOOP'95, Lecture Notes in Computer Science 952, Springer, 1995, 77-101"
    locator: the whole paper (class hierarchy analysis and its use to replace dynamically dispatched sends by direct calls)
  - paper: doi:10.1145/236337.236371
    title: "David F. Bacon and Peter F. Sweeney, Fast static analysis of C++ virtual function calls, Proceedings of the 11th ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications (OOPSLA 1996), 324-341"
    locator: the whole paper (rapid type analysis, and the fraction of virtual calls in C++ programs that it resolves to one target)
  - paper: doi:10.1145/178243.178478
    title: "Urs Hölzle and David Ungar, Optimizing dynamically-dispatched calls with run-time type feedback, Proceedings of the ACM SIGPLAN 1994 Conference on Programming Language Design and Implementation (PLDI 1994), 326-336"
    locator: the whole paper (receiver types recorded at run time, and guarded inlining of the common targets)
---

Devirtualization turns a virtual method call, or a call through a function pointer, into a direct call to a known function. A virtual call `o.m()` looks up the method in the class of the object at run time, which costs a few loads and an indirect jump, and it hides the target from the compiler. If an analysis proves that only one method can run at this call, the compiler calls that method directly. If the analysis only shows that one target is likely, the compiler adds a cheap type test and calls the likely method directly when the test passes. A direct call can then be inlined, which is where most of the gain comes from.

## In plain words

In an object-oriented program, a call like `shape.area()` does not say which code runs. The program looks at the actual object at run time: a circle runs the circle's code, a square runs the square's code. This lookup is slow, and it hides the code from the compiler.

Often the compiler can see that only one kind of object can ever reach a call. For example, no class in the program changes how `area` works for circles, and the variable always holds a circle. Then it can call the circle's code directly, skip the lookup, and even paste that code into the caller.

When the compiler is not sure, it can still guess. It writes a quick test, "is this a circle?", calls the circle's code directly if yes, and does the normal lookup if no.

## When it applies

Take a virtual call `x = o.m(args)` where the static type of `o` is the class $T$. At run time the target is $\mathrm{lookup}(c, m)$, where $c$ is the class of the object that `o` refers to. Let $S$ be a set of classes that contains $c$ on every run, as given by an analysis. The call can become a direct call to $f$ when $\mathrm{lookup}(c, m) = f$ for every $c \in S$.

Ways to find $S$, from cheap to precise:

- **Final classes and methods.** If $T$ is final, or $m$ is final in $T$, the target is fixed by the declaration.
- **Class hierarchy analysis.** [Class hierarchy analysis](/class-hierarchy-analysis/) takes $S$ to be $T$ and all its subclasses in the whole program. If none of them overrides $m$, the target is unique.
- **Rapid type analysis.** [Rapid type analysis](/rapid-type-analysis/) keeps only the classes of $S$ that the program can create, which removes many classes that are declared but never used.
- **Flow-based analyses.** [Variable type analysis](/variable-type-analysis/) and [points-to analysis](/points-to-analysis/) follow the objects that can reach `o`, so they give a set for this call alone.
- **Local facts.** If `o` was created by `new C` in the same function, after inlining, its class is exactly $C$.

The first four need to know all the classes of the program, a closed world. A program that loads classes at run time, or a library that others can extend, breaks this assumption.

When no analysis gives one target, a profile may show that one target is common: [type feedback](/type-feedback/) records the receiver classes at each call. Then a guarded call applies.

## The template

1. **Collect the virtual and indirect call sites.** Skip sites that are cold, unless their target is free to find.
2. **Compute the possible targets** of each site with the analyses above.
3. **One target $f$.** Replace `x = o.m(args)` by `x = f(o, args)`. If the language throws an error for a null receiver, keep an explicit null check before the call.
4. **A few targets, or one likely target.** Write a guarded call:

   ```
   if (class(o) == C) x = C_m(o, args);   // usually inlined
   else               x = o.m(args);      // the old virtual call
   ```

   The test can compare the class of the object with $C$ (a class test), or compare the method found in the object's dispatch table with `C_m` (a method test). The method test also passes for subclasses of $C$ that do not override `m`.
5. **Inline** the direct calls where the [inlining](/function-inlining/) cost model allows it.

**Why the behavior stays the same.** For an unguarded rewrite, the analysis is sound: on every run, the class $c$ of the receiver at this call is in $S$, so the old call runs $\mathrm{lookup}(c, m) = f$ with the same receiver and arguments as the new call. With the null check kept, a null receiver gives the same error. For a guarded rewrite, no analysis is needed. If the class test passes, $c = C$ and the old call would also run $\mathrm{lookup}(C, m) = $ `C_m`. If the method test passes, the method in the table is `C_m`, which is exactly what the old call would run. If the test fails, the old virtual call runs unchanged.

**Profit.** The direct call saves the dispatch loads and the indirect jump, and the processor predicts direct calls better. The main gain is that the target can be inlined and optimized with the caller. A guard costs a load and a compare, so it pays only when the guessed target is common.

## Classic examples

**Class hierarchy analysis.**

```
class Shape  { virtual double area(); };
class Circle : public Shape { double area() override; };
class Square : public Shape { double area() override; };

double f(Circle *c) { return c->area(); }
```

The program has no subclass of `Circle`, so the call in `f` can only run `Circle::area`. The compiler calls it directly and inlines it. A call `s->area()` with `Shape *s` has two targets and stays virtual, unless other facts help.

**Exact type after allocation.** `Shape *s = new Square(2); return s->area();` After the allocation, the compiler knows the class of `s` exactly, even though its declared type is `Shape`.

**Guarded inlining from a profile.** A call `s->area()` with `Shape *s` sees a `Circle` in 95 percent of the runs. The compiler emits a class test for `Circle`, inlines `Circle::area` on that branch, and keeps the virtual call on the other branch.

**A function pointer.** A sort routine takes a comparison function `cmp` and calls `cmp(a, b)`. After the sort routine is inlined into a caller that passes `compare_ints`, constant propagation makes the pointer a constant, and the indirect call becomes a direct call to `compare_ints`, which can then be inlined into the loop.

**A JIT with class loading.** A Java virtual machine compiles a method with class hierarchy analysis and finds one target. It records the assumption. If the program later loads a class that overrides the method, the virtual machine discards the compiled code, moving any running activations to the interpreter by [deoptimization](/deoptimization/), and compiles again.

## Variations

- **Whole-program devirtualization.** At link time, with all classes visible, a compiler can apply class hierarchy analysis to a C++ program. Classes that are visible outside the program must be treated as open.
- **Inline caches.** Dynamic language runtimes do the guarded form at run time without a compiler: an [inline cache](/inline-caching/) at the call site remembers the last receiver class and its target, and a [polymorphic inline cache](/polymorphic-inline-cache/) remembers several. Type feedback in optimizing JIT compilers reads these caches.
- **Customization.** Compile a separate copy of a method for each receiver class. Inside each copy, calls on `this` have a known class and become direct.
- **Speculation without a guard.** A JIT can skip the guard and rely on deoptimization when its assumption about the class hierarchy stops holding, as in the class loading example.

## Pitfalls

- **The closed world.** Class hierarchy analysis is wrong if a class can be added later: a shared library, a plugin, or a class loaded at run time can override the method. An ahead-of-time compiler must treat such classes as open. A JIT must register dependencies and deoptimize when a new class breaks one.
- **Null receivers.** A virtual call on null fails in a defined way in many languages. The direct call needs an explicit null check to keep that behavior.
- **Megamorphic calls.** A call with many common targets gains nothing from a chain of guards. Too many guards cost more than the dispatch and grow the code.
- **Profile drift.** A guard that was right during training can be wrong in production. The fallback keeps the program correct, but the guard then only costs time.
- **Reflection and dynamic proxies.** Objects created by reflection, serialization or proxies may belong to classes that a static analysis never saw.
- **Method test versus class test.** A class test fails for subclasses that inherit the same method, so it misses cases that are safe. A method test catches them, but it needs one more load.

## Exercises

1. In the shape example, add `class SmallCircle : public Circle` that does not override `area`. Can `c->area()` in `f` still be devirtualized? *Answer.* Yes. The possible classes are `Circle` and `SmallCircle`, and both look up `Circle::area`, so the target is still unique.
2. Now `SmallCircle` overrides `area`. What can the compiler do with `c->area()`? *Answer.* There are two targets, so an unguarded direct call is not sound. It can emit a guarded call for the more common class, or leave the call virtual.
3. Why is the guarded form correct even when the analysis is wrong? *Answer.* The test checks at run time exactly the fact that makes the direct call right. If it fails, the old virtual call runs, so no analysis result is needed for correctness.
4. Why do JIT compilers devirtualize more aggressively than ahead-of-time compilers for Java? *Answer.* The JIT sees the classes that are actually loaded and can undo its work by deoptimization when a new class arrives. An ahead-of-time compiler must be correct for every class that could ever be loaded.
5. A call `p(x)` goes through a function pointer that can hold `f` or `g`. Write the guarded form for the case where `f` is common. *Answer.* `if (p == f) y = f(x); else y = p(x);`. The direct call to `f` can then be inlined.

## References
