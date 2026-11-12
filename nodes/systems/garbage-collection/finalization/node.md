---
tag: T8X57S
kind: concept
slug: finalization
name: Finalization
aliases:
- finalizers
- object finalization
area: systems/garbage-collection
level: advanced
summary: "Running code of the program after the collector finds an object unreachable. The finalizer can make the object live again, runs in no fixed order, and may run late or never."
prereqs: [garbage, weak-reference]
see_also: [weak-reference, ephemeron, garbage, reference-counting, cycle-collection, heap-reachability, tracing-garbage-collection, generational-garbage-collection]
sources:
  - paper: doi:10.1145/604131.604153
    title: "Hans-J. Boehm, Destructors, finalizers, and synchronization, POPL 2003, 262-272"
    locator: the whole paper (finalizers must run in their own thread, need locks like concurrent code, and can run while a method of the object still runs; the comparison with destructors)
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Section 12.1 (finalisation, when finalizers run, which thread runs them, ordering, resurrection, and finalisation in reference counting and tracing collectors)
  - url: https://openjdk.org/jeps/421
    title: "JEP 421: Deprecate Finalization for Removal"
    locator: the motivation section (the flaws of finalization) and the alternatives (try-with-resources and cleaners)
  - url: https://peps.python.org/pep-0442/
    title: "PEP 442: Safe object finalization"
    locator: the sections on the finalization of reference cycles, resurrection, and running each finalizer at most once
  - url: https://github.com/python/cpython/blob/main/InternalDocs/garbage_collector.md
    title: CPython developer documentation, Garbage collector design
    locator: the sections on destroying unreachable objects (finalizers, resurrection, weak reference callbacks and legacy finalizers)
---

*Finalization* is the running of program code, a *finalizer*, for an object after the garbage collector has found that the object is unreachable and before its memory is reused. Programs use it to release resources that the collector does not manage, such as file handles, sockets or memory of a native library. Finalization is the one place where the collector calls back into the program, and this makes it hard to use well. The finalizer can make the object reachable again, finalizers of related objects run in an order that the program does not control, and nothing says when, or whether, a finalizer runs. Modern guidance prefers explicit release, and Java has deprecated its finalizers for removal.

## In plain words

When an object is no longer used, the collector takes its memory back. But some objects also hold things outside memory, such as an open file. Finalization lets such an object say: "before you throw me away, run this code", for example to close the file.

The collector does not throw the object away at once. It keeps the object, and everything that the object refers to, and asks a separate thread to run the code. Only later, at the next collection, is the memory reused.

The problems are simple to see. The code can store the object somewhere, so it is in use again. Two dying objects may need each other in their code. And because the collector runs when it wants, the file may stay open for a long time.

## The idea

**Finding finalizable objects.** The runtime keeps a list of the objects that have a finalizer. At the end of the marking phase of a [tracing collector](/tracing-garbage-collection/), each object on the list that is not marked is *finalizable*. The collector does not free it. It marks it, and everything that it reaches, so that the finalizer can use these objects, and it puts it on a queue. A finalizer thread takes objects from the queue and runs their finalizers. A later collection frees an object whose finalizer has run if it is still unreachable. So each finalizable object, and the data below it, survives at least one more collection, which in a [generational collector](/generational-garbage-collection/) can promote it to an older generation.

**Resurrection.** A finalizer runs ordinary code, so it can store a reference to its object, or to anything that the object reaches, in a global variable. The object is then reachable again: it is *resurrected*. This breaks the rule that [garbage](/garbage/) stays garbage, so the runtime must check reachability again before it frees anything that a finalizer could reach. To avoid an object that is finalized on each collection, Java runs each finalizer at most once, and CPython since PEP 442 does the same for its finalizers.

**Order.** Let $A$ refer to $B$, and let both have finalizers and become unreachable at the same time. The finalizer of $A$ may still use $B$. There are two policies:

- *Topological order.* Finalize $A$ first, and $B$ only at a later collection, after $A$ is gone. Then each finalizer sees the objects that it refers to in a state that their own finalizers have not changed. But if finalizable objects form a cycle, no order exists, and such a cycle is never finalized.
- *No order.* Finalize all finalizable objects of a collection, in any order, and keep all of them until their finalizers have run. Java works in this way. A finalizer may then see an object whose finalizer has already run, so each finalizer must cope with that.

**Which thread.** Boehm (2003) argued that finalizers must run in a thread of their own, not inside the allocation that started the collection. A finalizer that ran in the allocating thread could need a lock that this thread already holds. In its own thread, a finalizer is concurrent with the rest of the program, so it needs the same locking as any concurrent code. Boehm also showed that an object can become unreachable, and be finalized, while one of its own methods still runs, after the method's last use of the object's fields.

**No promptness.** A finalizer runs only after a collection finds its object unreachable, and a collection runs when the heap needs space, not when a file handle is short. A program can run out of file handles while gigabytes of memory are free. Most runtimes also do not promise to run finalizers when the program exits.

**With reference counting.** In a [reference counting](/reference-counting/) system, the finalizer of an acyclic object can run at the moment its count drops to zero, which is prompt and in a natural order. For objects in garbage cycles, the [cycle collector](/cycle-collection/) must choose an order. Before PEP 442, CPython did not collect cycles that held objects with finalizers and left them in a list for the programmer; since PEP 442 it runs the finalizers of the cycle once, checks again that the cycle is still unreachable, and then frees it.

**Weak references and finalization.** A [weak reference](/weak-reference/) is cleared when its target is no longer strongly reachable. Runtimes define whether this happens before or after finalization, and so whether a finalizer can resurrect an object that a weak reference has already given up. Java's phantom references are enqueued only after an object has been finalized and cannot be resurrected; this is the basis of the cleaners that replace finalizers. [Ephemerons](/ephemeron/) give another way to learn that an object has died, without code that runs on the object itself.

## Examples

**A file wrapper.** An object $F$ holds a file handle and a buffer object $G$. The program drops its last reference to $F$.

1. Collection 1 finds $F$ unmarked. $F$ has a finalizer, so the collector marks $F$ and $G$ and queues $F$.
2. The finalizer thread runs the finalizer of $F$, which writes out $G$ and closes the file.
3. Collection 2 finds $F$ and $G$ unmarked. The finalizer has already run, so both are freed.

The memory of $F$ and $G$ came back one collection later than without a finalizer, and the file stayed open from the moment $F$ died until step 2.

**Resurrection.** The finalizer of $F$ instead stores $F$ in a global list. At collection 2, $F$ is reachable, so it stays. When the program later removes $F$ from the list, $F$ becomes garbage again, and since its finalizer has already run, Java frees it without running it again.

**An order problem.** A connection object $A$ refers to a socket object $B$, and the finalizer of $A$ sends a last message over $B$. Both die together. Under topological order, the finalizer of $A$ runs first, then the one of $B$ at a later collection, and the message is sent. With no order, the finalizer of $B$ can run first and close the socket, and the finalizer of $A$ then fails.

**A cycle with finalizers.** A tree node $P$ and its child $C$ refer to each other, and both have finalizers. Under topological order, neither can be finalized first, so a collector that keeps this order never frees them. Such a collector can at best report the cycle to the programmer, who must break it.

## Where it is used

Java has had finalizers from its first version; JEP 421 deprecated them for removal in Java 18 and points programs to try-with-resources and to cleaners built on phantom references. C# has finalizers, with a pattern that lets code release resources explicitly and then tell the runtime that the finalizer is no longer needed. Python runs `__del__` methods, and CPython runs them at once for acyclic objects, through reference counting, and through its cycle detector for cycles. The [Boehm collector](/boehm-gc/) for C and C++ offers finalization in topological order. In each of these systems, the advice is to release important resources explicitly, with `close`, `using`, `with` or try-with-resources, and to use finalizers or cleaners only as a safety net.

## References
