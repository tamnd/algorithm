---
tag: JVVDBX
kind: algorithm
slug: escape-analysis
name: Escape analysis
aliases:
- escape analysis for objects
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Finds objects that do not outlive their method or thread, so they can be put on the stack and their locks removed.
model: word-ram
complexity:
  vars: {n: the number of nodes of the constraint graph, h: the number of allocation sites, s: the total size of the statements}
  time: {worst: O(n^2 h + s h)}
  space: {extra: O(n^2 + n h + s)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 1999
  people: [Jong-Deok Choi, Manish Gupta, Mauricio Serrano, Vugranam C. Sreedhar, Samuel Midkiff, Bruno Blanchet, John Whaley, Martin Rinard]
  note: Three papers at OOPSLA 1999 gave escape analyses for Java that allocate objects on the stack and remove locks on objects seen by one thread.
prereqs: [andersen-analysis, stack-allocation]
see_also: [scalar-replacement-of-aggregates, function-inlining, region-based-memory-management, gc-roots, just-in-time-compilation, object-sensitivity, alias-analysis, interprocedural-dataflow-analysis]
sources:
  - paper: doi:10.1145/320384.320386
    title: Jong-Deok Choi, Manish Gupta, Mauricio Serrano, Vugranam C. Sreedhar and Samuel Midkiff, Escape analysis for Java, Proceedings of OOPSLA 1999, 1 to 19
    locator: the connection graph, the three escape states NoEscape, ArgEscape and GlobalEscape, objects reachable from threads as escaping, stack allocation and lock removal
  - paper: doi:10.1145/320384.320387
    title: Bruno Blanchet, Escape analysis for object-oriented languages, application to Java, Proceedings of OOPSLA 1999, 20 to 34
    locator: escape analysis as an abstract interpretation over types, with stack allocation and synchronization elimination
  - paper: doi:10.1145/320384.320400
    title: John Whaley and Martin Rinard, Compositional pointer and escape analysis for Java programs, Proceedings of OOPSLA 1999, 187 to 206
    locator: points-to escape graphs with inside and outside edges, method summaries, and objects captured by a method or a thread
  - paper: doi:10.1145/2581122.2544157
    title: Lukas Stadler, Thomas Würthinger and Hanspeter Mössenböck, Partial escape analysis and scalar replacement for Java, Proceedings of CGO 2014
    locator: escape decided per control flow branch in a just-in-time compiler, with objects created only on the branches where they escape
---

Escape analysis finds the objects that cannot outlive the method that creates them, and the objects that only one thread can ever see. An object *escapes its method* when some path of references from outside the method's activation can reach it: through a global, a parameter object of the caller, or the return value. An object *escapes its thread* when another thread can reach it, through a global or through the arguments of a thread start. The first fact lets a compiler put the object in the method's stack frame, or break it into local variables with [scalar replacement](/scalar-replacement-of-aggregates/). The second lets it remove the locks on the object. The algorithm on this page follows Choi and colleagues (1999): it gives each allocation site one of three states, NONE, ARG or GLOBAL, from a points-to graph of the whole program. Here the graph comes from a field-sensitive [Andersen analysis](/andersen-analysis/).

## In plain words

Many objects in object-oriented code live only for a moment: an iterator in a loop, a small result object, a temporary string builder. If no one outside the method can ever get a reference to such an object, the method can keep it in its own stack frame, and the garbage collector never sees it. Escape analysis checks this. It follows every way a reference can leave a method: it can be stored in a global, written into an object that the caller gave, returned, or handed to a new thread. If none of these ways can reach the object, it stays inside. If only the thread start and global ways are closed, the object stays in one thread, so locking it is not needed. The check is safe: when it says an object stays inside, that is true for every run.

## The problem

The input is a program of methods with the statements $x = $ `new` at site $s$, $x = y$, $x = y.f$, $x.f = y$, $x = g$ and $g = y$ for a global $g$, $x = m(a_1, \ldots)$, start $m(a_1, \ldots)$ in a new thread, and `ret y`. The output is a state for each allocation site $s$ in method $m$: GLOBAL if an object of $s$ may be reachable from a global or from a thread other than the one that made it, ARG if not, but it may be reachable from a parameter or the return value of $m$, and NONE otherwise.

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may: GLOBAL and ARG mean "may escape" |
| domain | points-to sets of the locals, globals, return values and fields of sites, then one state for each site |
| order | inclusion of sets, and NONE below ARG below GLOBAL (bottom is precise) |
| join | union of sets, and maximum of states |
| bottom and top | empty sets and every site NONE, and every set full and every site GLOBAL |
| boundary value | the objects of globals and of thread start arguments are GLOBAL, and those of parameters and return values of $m$ are at least ARG for the sites of $m$ |
| initial value | every set empty |
| transfer | Andersen's inclusion rules for each statement, then reachability through the field sets |

## The algorithm

```pseudo id=main
ESCAPE(P)
L1  pts = ANDERSEN(P), with fields, globals, calls, returns and thread starts as copies
L2  roots = the sites in pts(g) for every global g, and in pts(a) for every argument a of every start
L3  shared = all sites reachable from roots through the field sets pts(s.f)
L4  for each method m do
L5      out = the sites in pts(p) for every parameter p of m, and in the return value of m
L6      out = all sites reachable from out through the field sets
L7      for each allocation site s in m do
L8          if s is in shared then state(s) = GLOBAL
L9          else if s is in out then state(s) = ARG
L10         else state(s) = NONE
L11 return state
```

Line L1 builds one points-to graph for the whole program. A call adds the copies $p_i \supseteq a_i$ from each argument to the callee's parameter and $x \supseteq ret$ from the callee's return value. A start adds the parameter copies only. A field $f$ of the objects of site $s$ is one node $s.f$, so a store $x.f = y$ adds $y$ to $s.f$ for every $s$ in $pts(x)$, and a load reads it.

Lines L2 and L3 find what other threads may see. Every object that a global may hold, or that is passed to a new thread, is shared, and so is everything reachable from it. Lines L5 and L6 do the same for one method: its parameter objects belong to its callers, and its return value goes to its caller. A site of $m$ in neither set is NONE. Its objects are reachable only from the activation that made them and from the methods that activation calls, and they are garbage when it returns.

## Example

```
main():                    make():                  worker(p):
  a = new      // s1         d = new    // s4         q = new    // s7
  b = new      // s2         e = new    // s5         p.f = q
  a.f = b                    d.f = e                  r = new    // s8
  c = make()                 w = new    // s6         G = r
  t = new      // s3         w.f = d
  start worker(t)            ret d
```

| site | state | why |
|---|---|---|
| $s_1$, $s_2$ | NONE | only locals of `main` reach them |
| $s_3$ | GLOBAL | it is the argument of a thread start |
| $s_4$ | ARG | `make` returns it |
| $s_5$ | ARG | it is reachable from the return value through $s_4.f$ |
| $s_6$ | NONE | it points to $s_4$, but nothing points to it |
| $s_7$ | GLOBAL | it is stored into $s_3.f$, and $s_3$ is shared |
| $s_8$ | GLOBAL | it is stored in the global $G$ |

So $s_1$, $s_2$ and $s_6$ can live in the stack frame of their method. The objects of $s_4$ and $s_5$ outlive `make`, but no other thread sees them, so their locks can go. If the compiler [inlines](/function-inlining/) `make` into `main`, they become NONE in `main` too. The other three need the heap and their locks. Note that $s_7$ is made by `worker` and never stored in a global, but the thread that started `worker` can reach it through $t$.

## Correctness

The proof file shows three facts. First, the points-to stage is sound for every run, including every interleaving of threads: each value that a local, a field, a global or a return slot holds has its site in the matching set. Second, a frontier lemma: split the frames into inside and outside. If every object that both sides reach has its site in a set $B$ that is closed under the field sets, and every way across the frontier, a global or a start argument, only carries sites of $B$, then this stays true, and an object made inside with its site outside $B$ never becomes reachable from outside. Third, two uses of the lemma. With the frames of one thread inside and $B$ = shared, objects of non-GLOBAL sites are never seen by another thread. With one activation of $m$ and its callees inside and $B$ = shared plus out of $m$, objects of NONE sites are never reachable from the caller, and when the activation returns, its return value does not reach them, so no root does.

## Complexity

**Proved.** Let $n$ be the number of nodes of the constraint graph (locals, return values, globals and pairs of a site and a field), $h$ the number of sites and $s$ the total size of the statements. The Andersen stage with difference propagation takes $O(n^2 h + s h)$ time. Each closure of lines L3 and L6 takes $O(n h)$, once for the shared set and once per method, and there are at most $n$ methods. So the whole analysis takes $O(n^2 h + s h)$ time and $O(n^2 + n h + s)$ space.

**Stated in the literature.** Choi and colleagues report, for a set of Java benchmarks in a static compiler, that a large share of the objects could be allocated on the stack in some programs and that many lock operations could be removed, with a measurable speedup. Stadler, Würthinger and Mössenböck report that a partial escape analysis in a just-in-time compiler removes more allocations and locks than an analysis that decides once per method.

**Measured, not proved.** On 250 random programs with up to 4 methods, threads, globals, recursion and two fields (seed 2024), the 2608 sites got 1608 NONE, 431 ARG and 569 GLOBAL states. Three random interleaved runs of each program, with each statement skipped with probability 0.2 to model branches, checked the claims of both theorems after every step, 575103 checks in all, with no failure. Dropping the globals, the start arguments, the return values or the parameters from lines L2 and L5 made the same check fail in 138, 33, 99 and 17 of the 750 runs.

## Properties

- **Sound, not exact.** A NONE object never escapes in any run, but an object marked ARG or GLOBAL may never escape in a real run.
- **Context-insensitive.** All activations of a method share one set per variable, so a method that sometimes receives an escaping object makes its parameter objects escape for all callers. Object sensitivity or method summaries reduce this.
- **Flow-insensitive.** An object that escapes only on one branch, or only at the end of a method, escapes everywhere.
- **Thread-aware.** Thread starts are roots of escape, like globals. An analysis that ignores them would remove locks from objects that two threads share.
- **Whole program.** The answer for one method depends on its callers and callees, so loading a new class can change it. A just-in-time compiler that uses the result must be able to undo it.

## Variants and improvements

- **Connection graphs.** Choi and colleagues build a summary graph for each method that records which parameter fields may reach which objects, and combine summaries at call sites, without a whole-program points-to analysis. This gives some context sensitivity, since each call site maps the summary to its own arguments.
- **Escape by types.** Blanchet's analysis abstracts each value by an integer that says how much of its type may escape, and computes it by abstract interpretation. It is fast and handles recursion over lists and trees.
- **Points-to escape graphs.** Whaley and Rinard separate inside edges, made by the method, from outside edges, which stand for unknown objects of the caller. A method's summary can then be reused, and objects captured by a method or a thread are found compositionally.
- **Partial escape analysis.** In a [just-in-time compiler](/just-in-time-compilation/), Stadler, Würthinger and Mössenböck decide escape per control flow branch. An object that escapes only on a rare path is created only on that path, and is replaced by local values on the others.
- **Regions.** [Region-based memory management](/region-based-memory-management/) generalizes stack allocation: an object goes into the region of the outermost activation that it cannot escape.

## When to use it

Use it in a compiler for a language where every object is on the heap and every object can be locked, such as Java. The common clients are [stack allocation](/stack-allocation/), scalar replacement after inlining, and removing locks from thread-local objects. A just-in-time compiler runs it per compiled method after inlining, where most temporary objects become NONE. For languages that already let the programmer choose stack allocation, the same analysis checks that a pointer to a stack object does not outlive the frame.

## Pitfalls

- **Forgetting threads.** A version of line L2 that uses only the globals as roots treats $s_3$ and $s_7$ in the example as thread-local and removes locks that two threads need. The right line L2 also adds every argument of every thread start.
- **Forgetting the return value.** A version of line L5 with only the parameters marks $s_4$ and $s_5$ as NONE, and stack allocation would leave `main` with a pointer into a dead frame. The right line L5 adds the return value.
- **Forgetting the parameters.** A version of line L5 without the parameters misses an object stored into a field of a parameter object, which the caller can then reach. The right line L5 adds the sites of every parameter.
- **Stopping at direct references.** A version of lines L3 and L6 that takes only the sets themselves, without the closure, marks $s_7$ as NONE, although it is reachable from the shared $s_3$ through a field. The right lines close over the field sets.
- **Allocation in a loop.** A NONE site in a loop makes one object per iteration. One fixed slot in the frame is enough only if the object of the last iteration is dead when the next one is made. Otherwise the frame needs space per iteration, or the object stays on the heap.
- **Claiming soundness with reflection or native code.** Reflection, native methods and serialization can store a reference where the analysis does not see it. Such calls must be treated as making their arguments GLOBAL.

## Implementations

## History

Escape analysis began in functional languages. Park and Goldberg (1992) found lists that do not escape a function, so that they could be allocated on the stack. For Java, three papers at OOPSLA 1999 appeared together: Choi, Gupta, Serrano, Sreedhar and Midkiff with connection graphs and the three escape states, Blanchet with an analysis by abstract interpretation over types, and Whaley and Rinard with compositional points-to escape graphs. All three used the result to allocate on the stack and to remove locks. Escape analysis then moved into just-in-time compilers for Java, where it drives scalar replacement and lock removal after inlining, and Stadler, Würthinger and Mössenböck (2014) made it partial, per control flow branch.

## References
