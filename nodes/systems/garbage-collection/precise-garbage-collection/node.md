---
tag: KYZMZH
kind: concept
slug: precise-garbage-collection
name: Precise garbage collection
aliases:
- exact garbage collection
- accurate garbage collection
- type-accurate garbage collection
area: systems/garbage-collection
level: intro
summary: "A collector that knows exactly which words are pointers, from object layouts and from stack maps at safepoints, so it can move objects and ignore dead slots."
prereqs: [gc-roots, tracing-garbage-collection]
see_also: [conservative-garbage-collection, mostly-copying-collection, copying-collection, heap-compaction, stop-the-world-collection, boehm-gc]
sources:
  - paper: doi:10.1145/143095.143140
    title: Amer Diwan, J. Eliot B. Moss and Richard L. Hudson, Compiler support for garbage collection in a statically typed language, PLDI 1992, 273-282
    locator: the tables that the compiler emits for each gc-point, giving the live pointer slots and registers, the treatment of derived pointers by their base pointers, and the compression of the tables
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Section 11.2 (Finding pointers, including accurate pointer finding in objects, stacks and registers, and interior and derived pointers) and Section 11.6 (GC safe-points and mutator suspension)
  - paper: doi:10.1002/spe.4380180902
    title: Hans-Juergen Boehm and Mark Weiser, Garbage collection in an uncooperative environment, Software Practice and Experience 18(9), 807-820, 1988
    locator: the conservative alternative, for a compiler that gives the collector no information about pointers
---

## In plain words

To clean memory, a collector must follow pointers from the program's variables to the objects they use. A precise collector knows exactly which values are pointers. The compiler tells it: for each kind of object, which fields hold pointers, and for each point where the program can stop for a collection, which variables on the stack hold pointers that the program will still use.

With this knowledge the collector keeps only what is really in use. It can also move objects to new places, because it can fix every pointer to them. A number that happens to look like an address is never mistaken for a pointer.

## The idea

A tracing collector needs the set of *roots*, the pointers held outside the heap, and for each object the positions of its pointer fields. A collector is *precise* (also *exact* or *accurate*) if it knows both exactly. Otherwise it must guess, as a [conservative collector](/conservative-garbage-collection/) does. Precise information comes from three places.

**Object layouts.** Each heap object has a header that leads to its type, and each type records which words are pointers: a bitmap, a list of offsets, or a convention such as "pointer fields first", which the implementation here uses. Some systems tag every word instead: the low bits of a word say whether it is a pointer or a small integer, as in many Lisp, Smalltalk and OCaml implementations.

**Stack maps.** The stack and the registers are harder, because their layout changes at each instruction. The compiler emits a *stack map* for some code positions: which frame slots and which registers hold live pointers there. Diwan, Moss and Hudson describe such tables, one per *gc-point*, for Modula-3. A slot that holds a pointer the function will not use again is left out, so dead variables keep nothing alive. The collector walks the frames, finds the code position of each frame (the return address of the call it is making), looks up the map, and visits the slots that it lists.

**Safepoints.** Maps for every instruction would be too large, so a collection may only start when every thread is at a *safepoint*, a position with a map. Call sites are safepoints, because a frame that is not the top of the stack is always stopped at a call. Allocation sites and the back edges of loops are safepoints too, so that a thread in a long loop can be stopped. A thread that is asked to stop for a collection runs on to its next safepoint, where it checks a flag or touches a protected page.

**Derived pointers.** An optimizing compiler can keep pointers that are not the start of an object: $p + 8$ for a field, a pointer into an array during a loop, or $p - k$ from strength reduction. The map lists each such *derived* pointer with its *base* pointer. The collector records the difference, moves the base object, and sets the derived pointer to the new base plus the difference. Diwan, Moss and Hudson also allow derived values that depend on several bases.

**What precision buys.**

- **Moving objects.** The collector can update every pointer, so it can use [copying](/copying-collection/) or [compacting](/heap-compaction/) collection and fast [bump-pointer allocation](/bump-pointer-allocation/). A conservative collector must pin any object that an ambiguous word might point to.
- **No false retention.** Only live pointers are followed. Numbers, stale pointers in dead slots, and floating-point data never keep garbage alive.
- **Generations and barriers.** A [generational collector](/generational-garbage-collection/) moves young objects out of the nursery, which needs precise pointers at least for the young objects.

**What it costs.** The compiler must track pointer types through all its optimizations, and it must keep the maps correct for each safepoint. The maps take space, often reduced by compression or by computing them lazily. Safepoint polls cost a little time in loops. Code that the compiler does not control, such as C libraries, must register its pointers with the runtime by hand, or be treated as a conservative region.

## Examples

**A frame at two safepoints.** A function $f$ has four slots: $p$, a pointer to object $A$; $n$, an integer; $q$, a pointer to $B$ that $f$ uses for the last time between the two calls; and $d = p + 2$, a pointer into $A$. The heap has $A$ at 1000 with words $[1005, 10, 20]$, where the first word points to $D$ at 1005, and $B$ at 1003 and $C$ at 1004.

| safepoint | stack map | the slots are $p, n, q, d$ |
|---|---|---|
| call at pc 8 | pointers: $p$, $q$ | 1000, 1004, 1003, 1002 |
| call at pc 12 | pointers: $p$; derived: $d$ from base $p$ | 1000, 1004, 1003, 1002 |

At pc 12 the integer $n$ happens to equal the address of $C$, and $q$ still holds the address of $B$, but neither is in the map. A copying collection to new addresses from 2000 copies $A$ to 2000 and $D$ to 2003, sets $p = 2000$ and $d = 2000 + 2 = 2002$, and leaves $n$ and $q$ alone. $B$ and $C$ are freed. At pc 8, $q$ is live, and $B$ is copied too. A conservative scan of the same frame would keep $A$, $B$, $C$ and $D$, and could move none of them. The implementation runs this example and checks random stacks against the true reachable graph: exactly the reachable objects are copied, the copy has the same shape, derived pointers keep their offset, and slots that are not pointers do not change.

**Tagged integers.** In OCaml a word with its low bit set is an integer and a word with the low bit clear is a pointer. The collector needs no maps for the heap, but integers have one bit less, and arithmetic must adjust the tags.

**Non-example.** A C compiler gives no maps, and C code can turn pointers into integers and back. A collector for C must be conservative, at least for the stack.

## Where it is used

- **Java and .NET virtual machines.** HotSpot, OpenJ9 and the .NET runtime compile stack maps for safepoints and use moving collectors, from generational copying to concurrent compaction.
- **Functional languages.** OCaml, GHC Haskell and many Lisps and Schemes use tags or layout information and copying collectors.
- **Modula-3 and Oberon.** Statically typed languages for which compiler support for collection was first studied; Diwan, Moss and Hudson used Modula-3.
- **Mixed systems.** Runtimes that call C code, or that are written in C, often scan the stack conservatively and the heap precisely, as in [mostly-copying collection](/mostly-copying-collection/). The [Boehm-Demers-Weiser collector](/boehm-gc/) can be told the layout of heap objects and be precise in the heap only.
- **Native interfaces.** The Java Native Interface gives native code handles to objects, not raw pointers. The collector knows every handle, so it stays precise and can still move the objects.

## References
