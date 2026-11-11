---
tag: RAFW61
kind: concept
slug: type-stable-memory
name: Type-stable memory
aliases: [type-preserving memory, type-safe memory, type-stable memory management, TSM]
area: concurrency/memory-reclamation
level: advanced
summary: Memory that may be freed and reused, but only for objects of the same type, so that a stale pointer still reads a well-formed object. It makes stale reads safe, not correct.
prereqs: [use-after-free, free-list]
see_also: [tagged-pointers, aba-problem, optimistic-access, read-copy-update, safe-memory-reclamation, treiber-stack, michael-scott-queue, hazard-pointers]
sources:
  - url: https://www.usenix.org/legacy/publications/library/proceedings/osdi96/greenwald.html
    title: Michael Greenwald and David Cheriton, The synergy between non-blocking synchronization and operating system structure, OSDI 1996
    locator: the section on type-stable memory management (TSM), which names the idea and uses it to make non-blocking code in the Cache Kernel simple
  - url: https://www.usenix.org/legacy/publications/library/proceedings/bos94/bonwick.html
    title: Jeff Bonwick, The slab allocator, an object-caching kernel memory allocator, USENIX Summer 1994 Technical Conference
    locator: the object caches, which keep freed objects of one type in a constructed state for reuse
  - url: https://www.kernel.org/doc/html/latest/RCU/rculist_nulls.html
    title: The Linux Kernel documentation, Using RCU hlist_nulls to protect list and objects
    locator: the lookups in a slab cache made with SLAB_TYPESAFE_BY_RCU, which must check the key again after the reference is taken, because the object may have been freed and reused for another key
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996, pages 267-275
    locator: the non-blocking queue, whose dequeued nodes go to a free list and are reused only as queue nodes, together with counted pointers
  - paper: doi:10.1145/2755573.2755579
    title: Nachshon Cohen and Erez Petrank, Efficient memory management for lock-free data structures with optimistic access, SPAA 2015, pages 254-263
    locator: the assumption that a read of a reclaimed node does not fault, which the optimistic reads rely on
---

**Type-stable memory** is memory that may be freed and allocated again, but only for objects of the same type, and that is never given back to the system while a pointer to it may exist. A pointer to a freed object therefore still points to an object of the right type: a read through it does not fault and returns a well-formed value, though maybe a value of a newer object. Greenwald and Cheriton named the idea type-stable memory management in their non-blocking kernel. It turns the danger of a [use-after-free](/use-after-free/) into the milder danger of a stale read, which lock-free code can detect with a check after the read, such as a [tagged pointer](/tagged-pointers/) in a CAS or a key compared again. It does not prevent the [ABA problem](/aba-problem/), and it does not let the memory shrink.

## In plain words

A hotel gives out rooms. When a guest leaves, the room is cleaned and given to the next guest, but it always stays a hotel room. It never becomes a storeroom or is torn down.

A visitor who has an old room number can still walk in and find a bed, a desk and a name on the door. The visitor will not fall into a hole. But the name on the door may be of a new guest, so the visitor must check the name before believing anything in the room.

## The idea

**The rule.** A pool holds the memory for one type $T$. A freed object of type $T$ goes back to the pool, and the pool reuses it only for a new object of type $T$. The pool never returns its memory to the system, or returns it only when no thread can hold a pointer to it, for example after a [grace period](/grace-period/). The fields of $T$ that lock-free code reads must stay valid values of their types at all times, even while the object is free: a pointer field holds nil or a pointer to another object of the pool, never random bits.

**What it gives.** Take a thread that loaded a pointer $p$ to an object, and the object is then freed and maybe reused. Under type-stable memory:

- a read through $p$ does not fault, and returns a value of the right type;
- a CAS through $p$ acts on an object of the right type, so it cannot damage an object of another type.

So a lock-free algorithm needs no protection for its reads, as long as it checks, after each read, that the object it read is still the one it meant. The common checks are:

- a CAS on a word that holds a pointer and a tag, as in the [Treiber stack](/treiber-stack/) with [tagged pointers](/tagged-pointers/), which fails if the object was removed after the read;
- a key or a version number in the object, read again after the use, as in the Linux kernel;
- a warning bit set by the reclaimer, as in [optimistic access](/optimistic-access/).

**What it does not give.**

- *Correct values.* A stale read is safe, not right. The algorithm must not use a value from a stale read without the check.
- *No ABA.* The address of a freed object comes back for a new object of the same type, so a plain CAS on the pointer can succeed by mistake. Type-stable memory makes ABA more likely, not less, and is used with tags or other checks.
- *Shrinking memory.* The pool keeps the most memory it ever used for type $T$. If the peak was large, the memory stays reserved.
- *Safety against writes.* A write through a stale pointer damages the new object. Only CAS steps that are checked, and that fail on a stale object, are safe.

**Compared with safe memory reclamation.** A [safe memory reclamation](/safe-memory-reclamation/) scheme, such as [hazard pointers](/hazard-pointers/), never frees an object while a thread may read it, so it gives back memory and needs no checks after reads. Type-stable memory lets objects be reused at once, with no tracking of readers, and asks the algorithm to check its reads instead. Some schemes combine the two: they reuse objects inside a type-stable pool at once, and give memory back to the system only after a grace period.

## Examples

- **A free list for a lock-free stack.** A popped node of the [Treiber stack](/treiber-stack/) goes to a free list of nodes and comes back as a new node. A pop that read $top = A$ and then $A.next$ while $A$ was reused gets a wrong $next$, but not a fault; the tag in $top$ makes its CAS fail. The tests of the [tagged pointers](/tagged-pointers/) page run every interleaving of small runs with such a pool, and find no lost value with a wide enough tag.
- **The Michael and Scott queue.** The 1996 [queue](/michael-scott-queue/) puts dequeued nodes on a free list that holds only queue nodes, and uses counted pointers. A dequeue may read the value of a node that is already reused, and its CAS on $head$ then fails.
- **Optimistic access.** In [optimistic access](/optimistic-access/), threads read nodes with no protection and check a warning bit after each read. The scheme is safe only because freed nodes stay in a type-stable pool; the tests of that page run on such a pool, and with normal memory the same reads would be a use-after-free.
- **SLAB_TYPESAFE_BY_RCU in Linux.** A slab cache made with this flag may reuse a freed object at once for an object of the same type, but returns its pages to the system only after an RCU grace period. A lookup under [read-copy-update](/read-copy-update/) may find an object that was freed and reused for another key, so it takes a reference and then checks the key again.
- **Non-example: a general allocator.** A call to malloc can return a freed block for an object of any type, and free can give the pages back to the system. A stale read can then fault, or read a pointer field that now holds an integer.

## Where it is used

- Operating system kernels: the Cache Kernel of Greenwald and Cheriton, the slab allocator of Bonwick in SunOS and its successors, and SLAB_TYPESAFE_BY_RCU in Linux.
- Lock-free data structures with free lists and tags, from the IBM System/370 free-pool example to the Michael and Scott queue.
- Reclamation schemes that allow unprotected reads, such as optimistic access, and some uses of [read-copy-update](/read-copy-update/) in which objects are reused inside a grace period.
- Object pools in managed and unmanaged languages, which keep objects of one type for reuse and so have the same benefit and the same stale-read risk.

## References
