---
tag: 4HHBTE
kind: technique
slug: type-feedback
name: Type feedback
aliases:
- profile-based inlining of dynamic calls
area: compilers-and-program-analysis/code-generation-and-jit
level: advanced
summary: Uses the receiver types recorded by inline caches to inline the likely targets of dynamic calls when recompiling hot code.
prereqs: [polymorphic-inline-cache, function-inlining, adaptive-optimization]
see_also: [inline-caching, devirtualization, deoptimization, class-hierarchy-analysis, profile-guided-optimization, hidden-classes, rapid-type-analysis, tracing-jit-compilation]
sources:
  - paper: doi:10.1145/178243.178478
    title: Urs Hölzle and David Ungar, Optimizing dynamically-dispatched calls with run-time type feedback, PLDI 1994, 326-336
    locator: the idea of type feedback, the use of polymorphic inline caches as the source of receiver types, and the inlining of the cached targets behind type tests in SELF-93
  - paper: "Urs Hölzle, Adaptive optimization for SELF: reconciling high performance with exploratory programming, PhD thesis, Stanford University, 1994 (report STAN-CS-TR-94-1520)"
    locator: Chapter 5, Section 5.1 (type feedback, with the example of get_x on CartesianPoint) and Section 5.5 (when the system ignores type feedback for polymorphic sites)
  - paper: doi:10.1007/BFb0057013
    title: Urs Hölzle, Craig Chambers and David Ungar, Optimizing dynamically-typed object-oriented languages with polymorphic inline caches, ECOOP 1991, LNCS 512, 21-38
    locator: the remark that polymorphic inline caches record the receiver types of each send, which a compiler can use for inlining
  - paper: doi:10.1109/JPROC.2004.840305
    title: Matthew Arnold, Stephen J. Fink, David Grove, Michael Hind and Peter F. Sweeney, A survey of adaptive optimization in virtual machines, Proceedings of the IEEE 93(2), 2005, 449-466
    locator: the section on feedback-directed optimization, including receiver type profiles and guarded inlining of virtual calls
---

Type feedback is an optimization for languages with dynamic dispatch. Unoptimized code records, at each call site, the receiver classes that actually occur, usually in its [polymorphic inline caches](/polymorphic-inline-cache/). When [adaptive optimization](/adaptive-optimization/) later recompiles a hot method, the optimizing compiler reads these classes and replaces the dynamic call with a test of the class followed by the [inlined](/function-inlining/) body of the method for that class, with a fallback for any other class. Hölzle and Ungar introduced it in SELF-93 in 1994. It gets the type information from the run itself instead of from a static analysis, so it works in programs where an analysis cannot find the types, and it is the base of the optimizing compilers of Java and JavaScript today.

## In plain words

A call like `p.getX()` in a dynamic language can go to many methods, depending on the kind of `p`. A compiler that knows nothing about `p` must make a slow general call, and it cannot copy the called code into the caller, because it does not know which code that is.

But while the program runs, the call place keeps a short list of the kinds it has seen. Suppose the list says that `p` was always a CartesianPoint. When the busy method is compiled again, the compiler writes: "if `p` is a CartesianPoint, do the body of CartesianPoint's getX right here; otherwise make the general call". The common case is now a quick check followed by the copied code, which the compiler can then improve further. The rare case still works.

## When it applies

- Calls are dispatched on the run-time class of the receiver, and a static analysis cannot narrow the classes enough to [devirtualize](/devirtualization/) the call.
- The program first runs in a form that records receiver classes per call site: an interpreter or unoptimized code with inline caches.
- An optimizing compiler recompiles hot code at run time, as in [adaptive optimization](/adaptive-optimization/), so the profile is available when it compiles.
- Most sites see one or a few classes, so a few tests cover almost all calls.
- The system can invalidate optimized code when a class or a method changes, because the inlined body is right only for the methods as they were at compile time.

## The template

Let a call site send the selector $s$ to a receiver $r$, and let its cache list the classes $K_1, \dots, K_j$, with counts $c_1, \dots, c_j$ if the system counts. The optimizing compiler does the following.

1. **Choose the cases.** Sort the classes by count, most frequent first, and keep those worth inlining: often the classes that cover most calls, up to a small number, and only if the target bodies are small enough.
2. **Find the targets.** For each kept class $K_i$, find $m_i = \mathrm{LOOKUP}(K_i, s)$ now, and record a dependency: the code depends on the result of this lookup.
3. **Emit a type case.** Replace the call by

```
   if class(r) = K1 then  ⟨body of m1 inlined, with r as the receiver⟩
   else if class(r) = K2 then  ⟨body of m2 inlined⟩
   ...
   else  ⟨fallback⟩
```

4. **Choose the fallback.** Either a normal dynamic send, which handles any class, or an *uncommon trap* that leaves the optimized code by [deoptimization](/deoptimization/) and lets the unoptimized code handle the case.
5. **Optimize further.** Inside each branch the class of $r$ is known, so sends to `self` in the inlined body can be inlined in turn, and constant folding and the other optimizations see through the call.

In Hölzle's example (thesis, Section 5.1), the site `p.get_x` has only seen CartesianPoint receivers, whose `get_x` returns a field. The optimized code becomes "if the class of `p` is CartesianPoint, load the field `x` of `p`; else call `get_x` dynamically". A call becomes a compare and a load.

### Why it is correct

The original call means $\mathrm{CALL}(\mathrm{LOOKUP}(\mathit{class}(r), s), r, \mathit{args})$, where $\mathrm{LOOKUP}$ is evaluated at the time of the call.

**Claim.** If the code is thrown away as soon as any lookup it recorded in step 2 changes its result, and the fallback is either a dynamic send or an exit that rebuilds the interpreter state at the call, then each run of the type case has the same outcome as the original call.

*Proof.* Take a run of the type case in which the code is still valid, and let $K = \mathit{class}(r)$. If $K = K_i$ for some kept class, the first such test succeeds, because the classes are distinct, and the branch runs the inlined body of $m_i$. Since the code is valid, $\mathrm{LOOKUP}(K_i, s)$ still returns $m_i$, so the original call would also run $m_i$ on $r$. Inlining a body, with the parameters bound to the arguments and the names renamed apart, has the same outcome as calling it, by the correctness of [function inlining](/function-inlining/). If $K$ is none of the kept classes, all tests fail and the fallback runs. A dynamic send is the original call. An exit happens before any effect of the call, so if it rebuilds the interpreter state at the call exactly, the interpreter makes the original call. In each case the outcome is the same. $\square$

The tests are what make the inlining safe: a profile can only say what happened before, so it is never trusted without a check. The profile decides which cases are fast, never which results are right.

### A worked example

A site has the cache counts Circle 900, Square 80 and Triangle 20 over 1000 calls, and the system inlines Circle and Square with a dynamic send as fallback. Suppose the next 1000 calls have the same mix.

| order of tests | tests for Circle | tests for Square | tests for Triangle | total tests | dynamic sends |
|---|---|---|---|---|---|
| Circle, Square | 900 × 1 | 80 × 2 | 20 × 2 | 1100 | 20 |
| Square, Circle | 900 × 2 | 80 × 1 | 20 × 2 | 1920 | 20 |
| no inlining | none | none | none | 0 | 1000 |

So ordering by count saves 820 of 1920 tests, and inlining turns 980 of the 1000 dynamic sends into inline code. These are counts of operations in this model, not times.

## Classic examples

- **SELF-93.** Unoptimized code has counters and polymorphic inline caches. When a method is recompiled, the compiler reads the caches of the sends it inlines through and builds type cases from them. The thesis also gives rules for when the system ignores the feedback of a polymorphic site, because a cache in a method with many callers mixes the types of all of them (Section 5.5).
- **Java virtual machines.** The interpreter and the first-tier compiler record a receiver type profile at virtual and interface calls. The optimizing compiler inlines the one or two most frequent receivers behind class tests, and falls back to a virtual call or to deoptimization. The survey of Arnold and others describes this guarded inlining.
- **JavaScript engines.** The lower tiers record types for calls, property reads and arithmetic operations, and the optimizing compiler turns them into guards with [deoptimization](/deoptimization/) as the fallback. For property reads the "type" is a [hidden class](/hidden-classes/).
- **Ahead-of-time compilers.** A [profile-guided](/profile-guided-optimization/) compiler can promote an indirect call to a test plus a direct call, from a profile of a training run. This is the same transformation with an offline profile.

## Variations

- **Fallback by send or by trap.** A dynamic send keeps all classes possible after the call, so the code after the type case must handle any result. An uncommon trap lets the compiler assume that $r$ was one of the kept classes in the rest of the method, which gives better code, at the cost of a deoptimization if the assumption fails.
- **Class tests or method tests.** Instead of testing the class, the code can test that the lookup gives $m_i$, for example by comparing the method found in the class's dispatch table. Then all subclasses that inherit $m_i$ share one case.
- **Types of values, not only receivers.** The same idea applies to the operand types of `+`, the hidden class of an object at a property read, or whether an array holds only small integers.
- **Static analysis together with feedback.** [Class hierarchy analysis](/class-hierarchy-analysis/) or [rapid type analysis](/rapid-type-analysis/) can remove a case that cannot occur, and feedback picks among the rest.
- **Profiles per call path.** A callee that is inlined into many callers has one cache for all of them. A system can keep the profile per caller, or per inlined copy, to avoid mixing types.

## Pitfalls

- **No fallback.** Inlining the seen cases without a fallback is wrong as soon as a new class appears. The profile describes the past only.
- **No dependency on the lookup.** If a method of $K_i$ is redefined, or a new method in a class between $K_i$ and the class that defines $m_i$ overrides it, the inlined body is stale. The code must be invalidated, and frames that run it must be [deoptimized](/deoptimization/).
- **Polluted profiles.** The cache of a send inside a widely used method holds the classes of all its callers. Inlining all of them in one caller makes large code with cases that never occur there.
- **Code growth.** Every inlined case copies a body. Limit the number of cases and the size of the bodies.
- **A trap that fires often.** If an uncommon trap fires many times, the code deoptimizes again and again. Count the traps and recompile with a send in that place, as SELF did with its uncommon traps.

## Exercises

1. Write the type case for a site with the cache Circle 600, Square 300, Triangle 100, inlining all three with an uncommon trap as fallback. How many tests run per 1000 calls in the best order?
2. Give a program where a class test on $K_i$ is correct but a test "is $r$ an instance of $K_i$ or a subclass" is wrong, and one where the method test of the variations is correct but the class test misses.
3. Explain why the claim needs the dependency in step 2 even if the system never removes a method, but can load new classes.
4. A method `max(a, b)` is called from 50 places, and its inner send `a < b` sees integers, floats and strings. Discuss whether to use the feedback of this send when `max` is inlined into a caller that only passes integers.
5. Compare the code after a type case with a send fallback and with a trap fallback, for `x = p.get_x(); y = x + 1`, where `get_x` returns a small integer for the inlined class.

## References
