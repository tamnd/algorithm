---
tag: KTT4P1
kind: definition
slug: gc-roots
name: Root set
aliases:
- GC roots
- garbage collection roots
area: systems/garbage-collection
level: intro
summary: "The references that the mutator can use without loading them from the heap: registers, stack slots and global variables. Tracing starts from them."
prereqs: [mutator-and-collector]
see_also: [heap-reachability, precise-garbage-collection, conservative-garbage-collection, mostly-copying-collection, remembered-set, deferred-reference-counting, tracing-garbage-collection, boehm-gc]
sources:
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Section 1.6 (the mutator roots), Section 11.2 (finding pointers, conservative and accurate pointer finding, pointers in stacks and registers, derived pointers) and Section 11.6 (GC safe-points and mutator suspension)
  - paper: doi:10.1002/spe.4380180902
    title: "Hans-Juergen Boehm and Mark Weiser, Garbage collection in an uncooperative environment, Software: Practice and Experience 18(9) (1988), 807-820"
    locator: the treatment of each word of the stacks, registers and static data as a possible pointer, and the test of a candidate word against the heap
  - book: isbn:9780471941484
    title: "Richard Jones and Rafael Lins, Garbage Collection: Algorithms for Automatic Dynamic Memory Management, Wiley, 1996"
    locator: Chapter 9 (garbage collection for C, conservative root scanning and its false retention)
---

The *root set* of a program that runs with a garbage collector is the set of locations that hold references which the [mutator](/mutator-and-collector/) can use directly, without first loading them from a heap object. The usual roots are the processor registers, the slots of each thread's stack and the global variables. Every live object is reached from the roots by a chain of [pointers](/pointer/), so a [tracing collector](/tracing-garbage-collection/) starts its search there. A collector must find every root, or it frees a live object; how it finds them splits collectors into *precise* and *conservative* ones.

## Definition

Use the heap model of [mutator and collector](/mutator-and-collector/): a heap $H$ of objects with fields, and a mutator that changes the heap with $\mathrm{New}$, $\mathrm{Read}$ and $\mathrm{Write}$.

**Definition.** A *root* is a storage location $\ell$ outside $H$ whose content the mutator can use as a reference without a $\mathrm{Read}$ of a heap object. The *root set* $R$ is the set of all roots at a given moment. The *root objects* are

$$\mathrm{Roots} = \{\, x \in H : \text{some } \ell \in R \text{ holds a reference to } x \,\}.$$

The root set changes all the time: each call pushes stack slots, and each return pops them. A collector reads it at a *safe point*, a place in the code where the mutator can stop and where the collector knows where the references are.

**Where the roots are.**

- **Registers** of each mutator thread, at the moment it stops.
- **Stack slots** of each thread: local variables, arguments, return values and temporaries that the compiler spilled.
- **Global and static variables** of the program and of loaded classes or modules.
- **Runtime references:** handles that native code holds (in Java, through JNI), references in the runtime's own tables, interned strings, and constants that compiled code embeds.

**Precise and conservative root scanning.** A *precise* (or exact, or accurate) collector knows for each root location whether it holds a reference. The compiler emits a *stack map* for each safe point, which lists the slots and registers that hold references there. A *conservative* collector does not know this. It treats each word of the stacks, registers and static data as a reference if its value is the address of a heap object (or, with interior pointers, an address inside one). Boehm and Weiser (1988) showed that this is enough to collect C programs. The price is *false retention*: an integer that happens to look like an address keeps an object alive. A conservative collector also cannot move an object that an ambiguous root refers to, because it cannot change a word that may be an integer. See [precise garbage collection](/precise-garbage-collection/) and [conservative garbage collection](/conservative-garbage-collection/).

**Liveness of roots.** A slot can hold a reference that the program will never use again. A stack map that lists only the slots whose variables are still live at the safe point makes the root set smaller. Then the collector can free more, and [reachability](/heap-reachability/) comes closer to true liveness.

## Examples and non-examples

**A stack frame.** A heap holds objects of 32 bytes: $A$ at address 0x1000, $B$ at 0x1020, $C$ at 0x1040 and $D$ at 0x1060. A thread stops at a safe point. Its frame holds four words:

| slot | value | meaning in the program |
|---|---|---|
| $s_0$ | 0x1020 | a reference to $B$, used later |
| $s_1$ | 7 | an integer |
| $s_2$ | 4164 | an integer loop counter; 4164 is 0x1044 |
| $s_3$ | 0x1060 | a reference to $D$, never used again |

The three kinds of scan give three different sets of root objects:

| scan | root objects |
|---|---|
| precise, with a liveness map | $\{B\}$ |
| precise, with a type map only | $\{B, D\}$ |
| conservative, with interior pointers | $\{B, C, D\}$ |

The conservative scan keeps $C$ alive because 0x1044 points into $C$. This is false retention. It is not an error of safety, because an extra live object never causes a wrong free.

**A remembered set as roots.** When a [generational collector](/generational-garbage-collection/) collects only the young generation, the references from old objects to young objects act as extra roots. The collector keeps them in a [remembered set](/remembered-set/). These are roots of a partial collection, not of the program.

**Deferred counting.** [Deferred reference counting](/deferred-reference-counting/) does not count references from the roots. It scans the roots at each collection instead, to protect objects whose count is zero but which a root still refers to.

**Non-example: a hidden pointer.** A program that stores $p \oplus q$ instead of $p$ and $q$, as an [XOR linked list](/xor-linked-list/) does, hides both references from the collector. Neither a precise nor a conservative scan finds them, so the objects can be freed while the program still needs them. A safe collected language gives no way to do this, and a conservative collector requires that the program does not hide its pointers.

**Non-example: a field of a heap object.** A field of an object in $H$ is not a root, even if a root refers to the object. The collector reaches it by tracing.

## Related definitions

- **Reachability.** An object is live when a path of references leads to it from a root object: [reachability in the heap](/heap-reachability/). Multi-source search from all root objects at once, as in [multi-source BFS](/multi-source-bfs/), finds the live set.
- **Derived pointers.** An optimizing compiler can keep a pointer into the middle of an object, or a base plus an offset, in a register. A precise collector needs the stack map to tell it the base object, and a moving collector must update the derived pointer when it moves the base.
- **Precise and conservative collection.** [Precise garbage collection](/precise-garbage-collection/), [conservative garbage collection](/conservative-garbage-collection/), the [Boehm collector](/boehm-gc/) and [mostly-copying collection](/mostly-copying-collection/), which moves only the objects that no ambiguous root refers to.
- **Mutator and collector.** The two parts that share the roots: [mutator and collector](/mutator-and-collector/).

## References
