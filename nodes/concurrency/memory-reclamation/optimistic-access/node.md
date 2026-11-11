---
tag: HH6AVD
kind: technique
slug: optimistic-access
name: Optimistic access
aliases: [optimistic memory access, optimistic access reclamation]
area: concurrency/memory-reclamation
level: research
summary: Threads read nodes with no protection, then check a warning bit that a reclaimer sets before it frees nodes, and restart if it is set. Hazard pointers guard only the nodes that a CAS uses.
prereqs: [hazard-pointers, type-stable-memory]
see_also: [neutralization-based-reclamation, safe-memory-reclamation, harris-linked-list, treiber-stack, michael-scott-queue, epoch-based-reclamation, debra, use-after-free]
sources:
  - paper: doi:10.1145/2755573.2755579
    title: Nachshon Cohen and Erez Petrank, Efficient memory management for lock-free data structures with optimistic access, SPAA 2015, pages 254-263
    locator: the optimistic access scheme (the warning bits, the hazard pointers for the nodes of a write, the three pools and the recycling phases) and its proof of safety
  - paper: doi:10.1145/2814270.2814298
    title: Nachshon Cohen and Erez Petrank, Automatic memory reclamation for lock-free data structures, OOPSLA 2015, pages 260-279
    locator: the automatic version, which applies optimistic access to a data structure in normalized form without manual changes
  - paper: doi:10.1145/2555243.2555261
    title: Shahar Timnat and Erez Petrank, A practical wait-free simulation for lock-free data structures, PPoPP 2014, pages 357-368
    locator: the normalized form of lock-free data structures (a generator of CAS steps, an executor and a wrap-up), which optimistic access assumes
  - paper: doi:10.1109/TPDS.2004.8
    title: Maged M. Michael, Hazard pointers, safe memory reclamation for lock-free objects, IEEE Transactions on Parallel and Distributed Systems 15(6), 2004, pages 491-504
    locator: the publish and check protocol that optimistic access keeps for the nodes of a CAS
---

**Optimistic access** is a [safe memory reclamation](/safe-memory-reclamation/) technique by Nachshon Cohen and Erez Petrank. A thread reads shared nodes with no protection at all, even nodes that may already be freed. After each read it checks its own **warning bit**. A reclaimer sets the warning bit of every thread before it frees anything, so a thread that may have read freed memory sees the bit and restarts its operation. Only the few nodes that a thread is about to write with a CAS get [hazard pointers](/hazard-pointers/). Reads are almost free, and a stopped thread keeps only the nodes in its hazard pointers. The price is that freed nodes must stay readable, so the memory must be [type-stable](/type-stable-memory/), and that the data structure must be able to restart an operation at any read.

This page implements a simplified version on the [Treiber stack](/treiber-stack/) and the [Michael and Scott queue](/michael-scott-queue/). The paper keeps three shared pools of nodes and a phase number, so that all threads help one another to recycle. Here each thread recycles only its own retired nodes.

## In plain words

Readers walk through a library and read from books on the shelves, with no check at all. Some books may have been taken away and replaced with other books in the same cover.

Before the librarian takes any book away, the librarian puts a red flag on the desk of every reader. After each look at a book, a reader looks at the desk. If a red flag is there, what the reader just saw may be from a replaced book, so the reader removes the flag and starts the search again.

A reader who wants to write in a book first puts a note with its name on that book and looks at the desk once more. The librarian does not take away a book with a note on it.

So reading costs one extra look at the desk, and only writing costs a note.

## When it applies

- **Reads are many and writes are few.** A read costs one extra load of a bit that only the reader and the reclaimers touch, with no fence. A CAS costs a few hazard pointer writes and one check.
- **An operation can restart at any read.** A thread that sees its warning bit drops what it read and starts again. The data structure must allow this: Cohen and Petrank use the normalized form of Timnat and Petrank, in which an operation reads, then makes its CAS steps, and can always start over from the root. The stack, the queue and the [Harris linked list](/harris-linked-list/) fit this form.
- **Freed nodes stay readable.** A read of a freed node must not fault and must return some value of the right type, because the thread finds out only afterward. The nodes come from a pool of the same type, and memory never goes back to the system.
- **A thread can stop.** Unlike [epoch-based reclamation](/epoch-based-reclamation/), a stopped thread does not block reclamation. It holds only the nodes in its hazard pointers.

## The template

$W[t]$ is the warning bit of thread $t$, and $HP[t][1..K]$ are its hazard pointers. Each thread keeps a list of nodes that it has retired.

```pseudo id=main
READ(t, x.f)                             ▷ an optimistic read
L1  v ← x.f                               ▷ x may be freed; the pool is type-stable
L2  if W[t] then
L3      W[t] ← false; restart the operation from the root
    return v
BEFORE-CAS(t, p1, ..., pK)                ▷ hole: the nodes that the CAS uses
L4  HP[t][i] ← pi for i = 1, ..., K
L5  if W[t] then W[t] ← false; restart the operation from the root
RECYCLE(t)                                ▷ when the retired list of t holds R nodes
L6  for each thread q: W[q] ← true
L7  H ← the set of all HP[q][i]
L8  free each retired node of t that is not in H, and keep the others
```

The holes are the nodes that a CAS uses, given at L4, and the data structure code between the reads. Every read of a shared node goes through L1 to L3, and every CAS goes after L4 and L5. When the operation ends, the thread clears its hazard pointers.

**Walk-through.** L1 reads with no protection. If the node was freed before the read, then the reclaimer set $W[t]$ at L6 before it freed the node at L8, so the check at L2 sees the bit and the value is never used. A thread that restarts clears its bit at L3, and then it reads again from the root, which cannot lead it to a node that was removed before the bit was set. Before a CAS, L4 publishes the nodes of the CAS and L5 checks the bit again. Either the reclaimer set the bit before L5, and the thread restarts, or it set the bit after L5, and then its L7 comes after L4 and finds the hazard pointers, so it keeps those nodes. So the nodes of a CAS are never freed and reused while the CAS can still succeed, and there is no [ABA problem](/aba-problem/) on them.

**Garbage bound.** A recycle keeps at most $n K$ nodes, the ones in hazard pointers, so with $R > n K$ each list holds at most $R$ nodes and at most $n R$ retired nodes are unfreed at any time, whatever the threads do. A stopped thread keeps at most $K$ nodes from being freed.

**Cost.** One extra read per shared read, $K$ writes and one read before a CAS, and for a recycle, $n$ writes and $n K$ reads, done once every $R$ retires. A recycle makes each other thread restart at most once, so there are at most $n$ restarts for every $R$ retires.

**Example.** A stack $A \to B \to C$ and $R = 1$. Thread $p$ pops, and thread $q$ pops and recycles at once.

| step | thread | line | action | state after |
|---|---|---|---|---|
| 1 | $p$ | L1, L2 | reads $top = A$; $W[p]$ is false | |
| 2 | $p$ | L1, L2 | reads $A.next = B$; $W[p]$ is false | |
| 3 | $q$ | pop | CAS $top$ from $A$ to $B$, retires $A$ | $top = B$ |
| 4 | $q$ | L6 | sets $W[p]$ and $W[q]$ | |
| 5 | $q$ | L7, L8 | no hazard pointer names $A$, so frees $A$ | $A$ in the pool |
| 6 | $p$ | L1 | reads $A.val$: stale, but readable | |
| 7 | $p$ | L2, L3 | $W[p]$ is true: clears it and restarts | |
| 8 | $p$ | L1, L2 | reads $top = B$; $W[p]$ is false | |

If $p$ had passed L4 and L5 with $HP[p] = \{A, B\}$ before step 4, then at step 5 $q$ would find $A$ in $H$ and keep it, and $p$'s CAS from $A$ would simply fail. Without the checks at L2 and L5, $p$ could use stale values in a CAS that succeeds because the address $A$ was reused. The test file finds such a run.

## Classic examples

- [Treiber stack](/treiber-stack/): reads of $top$, $next$ and $val$ go through L1 to L3, and the pop CAS protects $top$ and $next$ at L4. The implementation on this page runs it.
- [Michael and Scott queue](/michael-scott-queue/): the CAS on $tail.next$ writes into a node, so $tail$ must be in a hazard pointer; the dequeue protects $head$ and $head.next$. The implementation runs it too.
- [Harris linked list](/harris-linked-list/): a search walks many nodes. With hazard pointers, each step costs a write and a fence; with optimistic access, each step costs one extra read, and only the two or three nodes of a CAS are protected. This is the kind of structure the paper targets.

## Variations

- **The original recycling with three pools.** In the paper, retired nodes go to a shared pool, and recycling runs in phases that any thread can help with. Nodes move from a retired pool to a processing pool and then to a ready pool for allocation, and a phase number keeps the threads in step. This makes recycling lock-free and spreads its cost.
- **Automatic optimistic access.** The second paper by Cohen and Petrank applies the scheme to a data structure in normalized form without manual changes: the restart points and the nodes of each CAS come from the form itself.
- **[Neutralization-based reclamation](/neutralization-based-reclamation/).** Also restarts a reader, but the reclaimer sends a signal instead of setting a bit, so the reader needs no check after each read.
- **[DEBRA](/debra/) with neutralizing.** The same restart idea built on top of epochs.
- **[Hazard pointers](/hazard-pointers/).** The case in which every read is protected: no restarts and no type-stable memory, but a write and a fence per node read.

## Pitfalls

- **Using a value before the check.** The wrong code reads $x.next$ at L1 and follows it at once, before L2. If $x$ was freed, the pointer is garbage. The right code checks $W[t]$ at L2 after every read and before any use of the value.
- **A CAS without the second check.** The wrong code writes the hazard pointers at L4 and makes the CAS without L5. A reclaimer that set the bit just before L4 may have read the hazard pointers before L4 and freed the node. The right code checks $W[t]$ again at L5, after the hazard pointer writes.
- **Freeing to the system.** Optimistic reads touch freed nodes. If the allocator gives memory back to the operating system, a read faults. Use a type-stable pool.
- **A restart that does not go back far enough.** After a warning, every value read in the attempt may be stale, including pointers kept in local variables. The operation must start again from the root, not from the last node it read.
- **Clearing the bit at the wrong time.** A thread clears its own bit only when it restarts. If it clears the bit and then goes on with values read before, a stale value can slip through.

## References
