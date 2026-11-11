---
tag: P0ZJPF
kind: definition
slug: use-after-free
name: Use-after-free
aliases: [dangling pointer dereference, UAF]
area: concurrency/memory-reclamation
level: intro
summary: A read or write through a pointer to a block of memory after the block was freed. The block may already hold a new object, so the access can see or damage data of another owner.
prereqs: []
see_also: [safe-memory-reclamation, aba-problem, type-stable-memory, hazard-pointers, epoch-based-reclamation, free-list, treiber-stack, race-condition]
sources:
  - paper: "ISO/IEC 9899:2011, Information technology, Programming languages, C"
    locator: Section 6.2.4, Storage durations of objects (an object referred to outside its lifetime gives undefined behavior, and a pointer to it becomes indeterminate), and Section 7.22.3, Memory management functions (the lifetime of an allocated object)
  - url: https://cwe.mitre.org/data/definitions/416.html
    title: MITRE, CWE-416, Use After Free, Common Weakness Enumeration
    locator: the description, the consequences and the code examples
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: the statement of the memory reclamation problem for lock-free objects, in which a thread may access a node that another thread removed
---

A **use-after-free** is a read or a write through a pointer to a block of memory after the block was freed. The pointer still holds the old address, but the block no longer belongs to the object that the pointer was made for. The allocator may have given the block to a new object, so a read can return data of another owner, and a write can damage it. In C and C++ the behavior is undefined. In concurrent code, a use-after-free happens when one thread frees a node that another thread has already loaded a pointer to; preventing this is the [safe memory reclamation](/safe-memory-reclamation/) problem.

## Definition

Take one run of a program. Each allocation returns a block $b$, a set of addresses, and starts an **allocation instance** $(b, i)$, the $i$-th allocation of $b$. The instance is **live** from its allocation at time $a_i$ until the free of $b$ at time $f_i$, so in the interval $[a_i, f_i)$, with $f_i = \infty$ if $b$ is never freed again. Instances of the same block do not overlap: $a_{i+1} \ge f_i$.

Each pointer value comes from one instance: the one that the allocator returned, or that the address was read from while that instance was live. An access is a pair of a time $\tau$ and a pointer $p$ to an address in $b$, with $p$ made from instance $(b, i)$.

The access is a **use-after-free** if $\tau \ge f_i$, that is, if the instance that $p$ was made for is no longer live at the time of the access. The block may be free at $\tau$ ($f_i \le \tau < a_{i+1}$), or it may hold a newer instance ($\tau \ge a_{i+1}$); both are use-after-free.

A **double free** is a free of $b$ through a pointer made from instance $i$ at a time $\tau \ge f_i$. It is a use-after-free of the allocator's own data in the block.

## Examples and non-examples

- **Example: the Treiber stack with immediate free.** Thread $p$ reads $top = A$ and is about to read $A.next$. Thread $q$ pops $A$ and frees it at once. Then $p$ reads $A.next$ at a time $\tau \ge f$: a use-after-free. If $q$ then pushes a new node and the allocator returns the same block, $p$ reads the $next$ of the new node, a value from another instance. The test files of the reclamation pages find this run with a simulator that marks each freed block.
- **Example: the [ABA problem](/aba-problem/) after reuse.** In the run above, $p$'s CAS on $top$ from $A$ to the old $A.next$ can succeed if $top$ again holds the address $A$, now of a new instance. The CAS does not access the block, so by the definition it is not a use-after-free. But it uses a pointer of a dead instance as if it were live, and it has the same cause and the same cures.
- **Example: a pointer kept after a read-side section.** In [read-copy-update](/read-copy-update/), a reader that saves a pointer and uses it after its section ended may use a version that was freed after the grace period.
- **Non-example: a protected read.** With [hazard pointers](/hazard-pointers/), a thread publishes the address and checks that it is still reachable before the read. No reclaimer frees the instance while the hazard pointer names it, so every access has $\tau < f_i$.
- **Non-example: a fresh pointer to a reused block.** A thread that reads $top$ after the block of $A$ was reallocated gets a pointer made from the new instance. Its accesses are to a live instance, even though the address is the same as before.
- **Borderline: a read in type-stable memory.** In a [type-stable](/type-stable-memory/) pool, a freed node stays a node, so a stale read returns a well-formed but possibly wrong value and does not fault. By the definition it is still a use-after-free. Schemes such as [optimistic access](/optimistic-access/) allow such reads on purpose, and then check that the value is not used.

## Related definitions

- **Dangling pointer.** A pointer whose instance is no longer live. A use-after-free is an access through a dangling pointer.
- **Double free.** Defined above. Most reclamation schemes must also prevent two threads from freeing the same node.
- **Memory leak.** The opposite failure: an instance that is no longer reachable and is never freed. A reclamation scheme must avoid use-after-free without leaking.
- **[Safe memory reclamation](/safe-memory-reclamation/).** The problem of freeing removed nodes of a concurrent structure with no use-after-free by any thread.
- **[ABA problem](/aba-problem/).** A CAS that succeeds because an address came back, often by reuse of a freed block.
- **[Race condition](/race-condition/).** A use-after-free in concurrent code is a race between the free in one thread and the access in another.

## References
