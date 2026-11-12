---
tag: 3QGTQE
kind: algorithm
slug: reference-counting
name: Reference counting
aliases:
- RC
- refcounting
- reference-counted pointers
- reference count garbage collection
area: systems/garbage-collection
level: intro
summary: "Each object keeps a count of the references to it. A write updates two counts, and an object whose count drops to zero is freed at once. Cycles are never freed."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {k: the number of fields of the objects that one write frees, n: the number of objects in the heap}
  time: {worst: O(1 + k), amortized: O(1)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false, complete: false, moving: false, incremental: true}
history:
  year: 1960
  people: [George E. Collins]
  note: "Collins described a count of references in each list cell, with erasure when the count drops to zero, in Communications of the ACM in December 1960."
prereqs: [garbage, mutator-and-collector]
see_also: [deferred-reference-counting, weighted-reference-counting, cycle-collection, trial-deletion, tracing-garbage-collection, weak-reference, lock-free-reference-counting, write-barrier]
sources:
  - paper: doi:10.1145/367487.367501
    title: "George E. Collins, A method for overlapping and erasure of lists, Communications of the ACM 3(12) (1960), 655-657"
    locator: the whole paper (the reference count of each list cell, its update when lists share cells, and erasure when the count drops to zero)
  - book: isbn:9781032218038
    title: "Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook: The Art of Automatic Memory Management, second edition, CRC Press, 2023"
    locator: Chapter 5 (Section 5.1 on the advantages and disadvantages of reference counting, Section 5.2 on improving efficiency, Section 5.5 on cyclic reference counting)
  - book: isbn:9780471941484
    title: "Richard Jones and Rafael Lins, Garbage Collection: Algorithms for Automatic Dynamic Memory Management, Wiley, 1996"
    locator: Chapter 3 (reference counting)
  - paper: doi:10.1145/1028976.1028982
    title: "David F. Bacon, Perry Cheng and V. T. Rajan, A unified theory of garbage collection, OOPSLA 2004, 50-68"
    locator: reference counting as the greatest fixed point of the reference count equations
---

Reference counting is a garbage collection algorithm that keeps, in each object, a count of the references to it. Each pointer write adds 1 to the count of the new target and subtracts 1 from the count of the old one. When a count drops to zero, no reference to the object is left, so the object is freed at once, and the counts of its children drop in turn. It was described by Collins (1960). It needs no search of the heap and frees most garbage at the moment it appears, but every write pays for two count updates, and a cycle of dead objects keeps its counts above zero and is never freed.

## In plain words

Think of each object as a room, and each reference as a key to the room. Next to the door, a counter shows how many keys exist. When someone copies a key, the counter goes up. When someone throws a key away, the counter goes down. When the counter shows zero, nobody can enter the room again, so the room is cleaned and given to a new user.

Cleaning a room throws away the keys that were inside it. So other counters go down, and other rooms can become free too.

Two rooms that hold each other's keys are a problem. Nobody outside has a key, but each counter shows one. The rooms are never cleaned.

## The problem

Solve [automatic memory reclamation](/automatic-memory-reclamation/) in the heap model of [mutator and collector](/mutator-and-collector/): free each object once no reference to it is left, and never free an object that the mutator can reach. Here a root is treated as a field of a special root object that is never freed, so every reference is a field, and every change of a reference is a WRITE.

## The algorithm

Each object $x$ has a count $\mathrm{rc}(x)$. The mutator calls NEW and WRITE, and the collector work runs inside these two operations.

```pseudo id=main
NEW(n)
L1  x ← allocate an object with n null fields
L2  rc(x) ← 0
L3  return x                               ▷ the caller stores x at once with WRITE

WRITE(p, i, y)                             ▷ p[i] ← y
L4  if y ≠ null then rc(y) ← rc(y) + 1     ▷ increment first
L5  z ← p[i]
L6  p[i] ← y
L7  if z ≠ null then RELEASE(z)

RELEASE(z)
L8  rc(z) ← rc(z) − 1
L9  if rc(z) = 0 then
L10     S ← a stack that holds z
L11     while S is not empty do
L12         x ← pop(S)
L13         for each field x[j] ≠ null do
L14             rc(x[j]) ← rc(x[j]) − 1
L15             if rc(x[j]) = 0 then push x[j] onto S
L16         free(x)
```

Line L4 adds 1 to the new target before line L8 subtracts 1 from the old one. If $y = z$, the count never drops to zero by mistake. The loop of lines L11 to L16 frees a whole dead structure with an explicit stack, so a long dead list does not overflow the call stack.

## Example

Roots $r_0$ and $r_1$ are fields of the root object. NEW makes $A$ with two fields and $B$, $C$ with one field each.

| step | operation | counts after it | freed |
|---|---|---|---|
| 1 | $r_0 \leftarrow A$ | $A = 1$ | |
| 2 | $A[0] \leftarrow B$ | $A = 1$, $B = 1$ | |
| 3 | $B[0] \leftarrow C$ | $A = 1$, $B = 1$, $C = 1$ | |
| 4 | $A[1] \leftarrow C$ | $A = 1$, $B = 1$, $C = 2$ | |
| 5 | $r_1 \leftarrow B$ | $A = 1$, $B = 2$, $C = 2$ | |
| 6 | $r_0 \leftarrow \text{null}$ | $B = 1$, $C = 1$ | $A$ |
| 7 | $C[0] \leftarrow B$ | $B = 2$, $C = 1$ | |
| 8 | $r_1 \leftarrow \text{null}$ | $B = 1$, $C = 1$ | |

In step 6, the count of $A$ drops to 0. RELEASE frees $A$ and subtracts 1 from $B$ and from $C$, which stay alive because $r_1$ still reaches them. After step 8, no root reaches $B$ or $C$, but they refer to each other, so both counts stay at 1. This cycle is a leak: plain reference counting never frees it.

## Correctness

The invariant is that each count is exact: $\mathrm{rc}(x)$ equals the number of fields of unfreed objects (the root object included) that refer to $x$. From it, an object is freed only when no field refers to it, so it is unreachable: the algorithm is safe. A stronger statement says which garbage it keeps. After each WRITE, the unfreed objects are exactly the reachable objects together with the garbage objects that a cycle of garbage reaches. This is the greatest fixed point of the reachability equations, as shown on the page [automatic memory reclamation](/automatic-memory-reclamation/). The proofs are below.

## Complexity

- **Per write.** Lines L4 to L9 take $O(1)$ time. If the count drops to zero, the loop of line L11 takes $O(1 + k)$ time, where $k$ is the total number of fields of the objects that it frees. One write can free a structure of any size, so there is no constant bound on the pause.
- **Amortized.** Each object is freed at most once, and each of its fields is visited once then. Charge this work to the NEW that made the object: the amortized cost of each NEW and each WRITE is $O(1)$, for objects with $O(1)$ fields.
- **Space.** One count per object. A count of $w$ bits is exact while fewer than $2^w$ references exist; implementations with small count fields make a count sticky at its largest value.
- **Cost to the mutator.** Each pointer write does two count updates, each a memory write to a third object, which a tracing collector does not do. In a multithreaded program the updates must be atomic, which costs more.

## Properties

- **Incremental by nature.** The collector work is spread over the mutator's writes, and no step looks at the live heap.
- **Prompt.** An acyclic object is freed at the write that removes its last reference. This is why reference counting suits resources with a clear end, such as files.
- **Not complete.** Garbage that a dead cycle reaches is never freed.
- **Local.** The work of a write depends only on the objects that it touches and frees, not on the size of the live heap.
- **Non-moving.** Objects stay where they are, so the allocator must handle fragmentation.

## Variants and improvements

- **Lazy freeing.** RELEASE puts an object whose count is zero on a list and does not touch its fields. Each NEW frees one object from the list first, and releases its fields then. This bounds the work per operation by the number of fields of one object, at the cost of a slower return of memory. Weizenbaum proposed this in the early 1960s.
- **Deferred reference counting.** Do not count references from the roots, and find the objects with count zero that a root still holds by a scan of the roots from time to time: [deferred reference counting](/deferred-reference-counting/).
- **Coalesced and buffered counting.** Log the first change of each field between two collections, and apply only the net count changes. Many writes to the same field then cost one pair of updates.
- **Limited-field counts.** Use one or a few bits per count, make the count sticky when it overflows, and restore the counts with a tracing collection.
- **Cycle collection.** Add [trial deletion](/trial-deletion/) or a backup tracing collector to free dead cycles: see [cycle collection](/cycle-collection/).
- **Weighted reference counting.** For a distributed heap, put a weight in each reference so that a copy needs no message to the owner: [weighted reference counting](/weighted-reference-counting/).
- **Weak references.** A reference that does not add to the count can break a cycle that the program knows about, for example the parent pointer of a tree: [weak reference](/weak-reference/).

## When to use it

Use reference counting when memory or other resources must be returned at once, when the heap is large but the live set changes in small steps, or when no runtime can stop the program to trace. It is common in scripting languages (CPython), in compiled languages without a tracing runtime (Swift, Objective-C, and the `shared_ptr`, `Rc` and `Arc` types of C++ and Rust), and in file systems that count the links to a file. Add a way to free cycles, or design the data so that it has no cycles of strong references. If throughput matters most and pauses are acceptable, a [tracing collector](/tracing-garbage-collection/) is usually faster.

## Pitfalls

- **Decrement before increment.** If WRITE subtracts from the old target before it adds to the new one, then $p[i] \leftarrow p[i]$ with a count of 1 frees the object that it is about to store.
- **Cycles.** A doubly linked list, a tree with parent pointers, or an object that refers to itself is never freed after its last outside reference goes. Use weak references for back pointers, or add cycle collection.
- **Recursive freeing.** A recursive RELEASE on a long dead list overflows the call stack. Use an explicit stack, as in lines L10 to L16, or lazy freeing.
- **Long pauses.** Dropping the last reference to a large structure frees all of it in one write.
- **Race conditions.** Two threads that update one count without atomic operations can lose an update. Even with atomic counts, a thread that loads a pointer and then increments its count can lose a race with a thread that frees the object between the two steps. The page [lock-free reference counting](/lock-free-reference-counting/) treats this case; there, the counts serve manual memory reclamation in lock-free data structures, not a runtime collector.

## Implementations

## History

Collins (1960) introduced reference counts to let lists share cells in a list-processing system: each cell holds the number of references to it, and a cell is erased when its count drops to zero. In the same year, McCarthy described the other approach, tracing from the registers and reclaiming what is not marked, for Lisp. The two approaches have been compared ever since. Deutsch and Bobrow (1976) cut the cost of counting with [deferred reference counting](/deferred-reference-counting/). Bacon, Cheng and Rajan (2004) showed that tracing and reference counting compute the least and the greatest fixed point of the same equations.

## References
