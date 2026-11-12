---
tag: M2QAS8
kind: technique
slug: region-based-memory-management
name: Region-based memory management
aliases:
- Tofte-Talpin regions
- region inference
- stack of regions
area: systems/memory-allocation
level: core
summary: "Put each object in a region and free whole regions in LIFO order when their scope ends. A type rule keeps pointers into a region from leaving its scope, so no read dangles."
prereqs: [arena-allocation, stack-allocation]
see_also: [bump-pointer-allocation, tracing-garbage-collection, reference-counting, lambda-calculus, automatic-memory-reclamation, memory-pool, copying-collection, garbage]
sources:
  - paper: doi:10.1006/inco.1996.2613
    title: Mads Tofte and Jean-Pierre Talpin, Region-based memory management, Information and Computation 132(2), 1997, 109-176
    locator: the region calculus with letregion and allocation at a region, the typing rule for letregion with region and effect variables, region inference and the soundness theorem
  - paper: "Mads Tofte and Jean-Pierre Talpin, Implementation of the typed call-by-value lambda-calculus using a stack of regions, POPL 1994"
    locator: the first account of region inference and of the run-time stack of regions
  - paper: doi:10.1002/spe.4380200104
    title: David R. Hanson, Fast allocation and deallocation of memory based on object lifetimes, Software, Practice and Experience 20(1), 1990, 5-12
    locator: arenas as a run-time library, freed by the programmer, which regions make safe
  - paper: "David Gay and Alex Aiken, Memory management with explicit regions, PLDI 1998"
    locator: explicit regions in C with a reference count per region, so that a region is freed only when no pointer to it remains
---

*Region-based memory management* puts every object in a *region* and frees whole regions, never single objects. A region is made when a program enters a scope and freed when it leaves it, so regions form a stack: the region made last is freed first. Inside a region, objects are allocated by [bump-pointer allocation](/bump-pointer-allocation/), as in an [arena](/arena-allocation/). The difference from a plain arena is safety. In the system of Mads Tofte and Jean-Pierre Talpin, the compiler decides which region holds each object, by *region inference*, and a type system proves that no pointer into a region is used after the region is freed. This gives the speed of stack and arena allocation with no garbage collector and no dangling pointers.

## In plain words

Think of a building with rooms. Each task gets its own room, and everything the task makes goes into that room. When the task ends, the room is cleared out at once. Rooms are cleared in the reverse order of opening: a room opened inside another task is cleared before that task ends.

The danger is a note in one room that points to a box in a room that is already cleared. Region systems check the program before it runs, and refuse it if such a note could ever be left behind. Only results that point to rooms that are still open may leave a task.

## When it applies

- Object lifetimes follow the structure of the program: data made in a scope is mostly dead when the scope ends, and the data that survives can go into a region of an outer scope.
- Pauses must be short and predictable, so a tracing collector is not wanted, as in real-time and embedded systems.
- The language has a type system that can carry region names, or the programmer can name regions by hand and accept a checker.
- Freeing in groups is fine: an object may live until its region ends, even if it dies earlier.

## The template

A program has two new forms. `letregion ρ in e` makes a new region, binds it to the region variable $\rho$, runs $e$ and frees the region. `e at ρ` allocates the value of $e$ in the region of $\rho$. The checker gives each pointer a type that names its region, for example $(\text{int} \times \text{int}, \rho)$ for a pair in $\rho$.

```pseudo id=main
CHECK-LETREGION(ρ, e)                         ▷ the type rule, at compile time
L1  τ ← CHECK(e) with ρ added to the regions in scope
L2  if ρ occurs in τ then reject the program, else return τ

RUN-LETREGION(ρ, e)                           ▷ the runtime
L3  k ← a new empty region; push k on the region stack
L4  v ← RUN(e) with ρ bound to k
L5  pop k from the region stack and free all its blocks at once; return v

ALLOC-AT(ρ, n)
L6  bump-allocate n words at the end of the region bound to ρ
```

Line L2 is the core of the method. A value of $e$ whose type does not mention $\rho$ contains no pointer into $\rho$, so after line L5 frees the region, nothing that the program can still reach points into it. In the full calculus of Tofte and Talpin, function types carry *effects*, the sets of regions that a call may read or write, and the rule also requires that $\rho$ does not occur in the types of the free variables. The page's code checks and runs a small first-order language with pairs, `let` and `letregion`, where no functions exist and the rule of line L2 is enough. It does not infer regions; the program names them.

## Classic examples

**A program the checker accepts.** Here $q$ is a temporary pair, and only a copy of its data leaves the inner scope, in the outer region $\rho_1$.

```
letregion ρ1 in
  let p = (letregion ρ2 in
             let q = (1, 2) at ρ2 in
             (fst q, snd q) at ρ1) in
  fst p
```

The inner `letregion` has the type $(\text{int} \times \text{int}, \rho_1)$, which does not mention $\rho_2$, so line L2 accepts it. At run time, $\rho_2$ holds $q$ and is freed when the inner scope ends; $\rho_1$ holds $p$ and is freed at the end. The result is 1, the peak use is 4 words, and both regions are freed.

**A program the checker rejects.**

```
letregion ρ1 in
  let p = (letregion ρ2 in (1, 2) at ρ2) in
  fst p
```

The inner `letregion` has the type $(\text{int} \times \text{int}, \rho_2)$, so line L2 rejects the program. Without the check, `fst p` would read the pair after $\rho_2$ is freed. The page's runtime raises a dangling-access error on exactly this program. The tests also make 4000 random programs and check that no program that the checker accepts ever reads a freed region, and that every region is freed at the end.

**The ML Kit.** Tofte, Talpin and others built region inference into the ML Kit, a compiler for Standard ML. Region inference adds `letregion` and `at` to an ML program by itself, with region-polymorphic functions, so that each function can get the regions of its arguments and results as parameters.

**Explicit regions.** Gay and Aiken (1998) added regions to C, with a count of the pointers into each region, so that freeing a region that is still in use fails safely. Cyclone, a safe dialect of C, combined region types with stack and heap regions. The lifetimes of Rust and the scoped memory areas of the Real-Time Specification for Java follow the same idea.

## Variations

- **Region inference.** Find the regions and their scopes from an unannotated program. Tofte and Talpin infer them from the types and effects of an ML program.
- **Regions plus a collector.** Region inference can keep regions alive too long, for example in a long loop that allocates into an outer region. Later versions of the ML Kit added a garbage collector that runs inside regions.
- **Reference-counted regions.** Count the pointers into each region, as Gay and Aiken did, so that regions need not be freed in LIFO order.
- **Unchecked arenas.** Drop the checker and let the programmer free regions, as with [arenas](/arena-allocation/), APR pools or PostgreSQL memory contexts. This keeps the speed and loses the safety.
- **Regions on a stack.** When every region holds a fixed number of objects of known size, its memory can sit in a stack frame, which is [stack allocation](/stack-allocation/).

## Pitfalls

- **Region leaks.** A region lives until its scope ends, even if its data dies early. A loop that allocates into a region of an outer scope keeps every copy alive until the loop ends.
- **Hidden escapes.** A checker that ignores a path, such as a pointer stored into an object of an outer region or captured by a closure, accepts programs that dangle. The full rule needs effects and the types of free variables.
- **Programs that are hard to infer.** Small changes to a program can change the regions that inference picks, and with them the memory use. Tools that show the inferred regions help.
- **Confusing regions with arenas.** Both free memory in groups. Regions add a static guarantee and a LIFO discipline; arenas are a library with neither.

## Exercises

1. Show that, in the language of the page, a closed program that the checker accepts has the type int.
2. Change the rejected program so that it is accepted and still returns 1, without moving the pair out of $\rho_2$ by hand.
3. Write a program in which the checker forces a value into an outer region, and measure the peak use of words with and without the inner region.
4. Find a program in which a pointer into $\rho_2$ is stored in a pair in $\rho_1$. Why does line L2 still catch it?
5. Explain why freeing regions in LIFO order needs no count of pointers, while freeing them in any order does.

## References
