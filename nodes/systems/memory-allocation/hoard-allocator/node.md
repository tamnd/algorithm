---
tag: HAC5RQ
kind: algorithm
slug: hoard-allocator
name: Hoard allocator
aliases:
- Hoard
area: systems/memory-allocation
level: research
summary: "A multithreaded malloc with one heap per processor and a global heap. Superblocks move to the global heap when a heap gets too empty, which bounds memory use and avoids false sharing."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {c: the number of size classes, g: the number of fullness groups, p: the number of processors}
  time: {worst: O(c + g)}
  space: {extra: O(p)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2000
  people: [Emery D. Berger, Kathryn S. McKinley, Robert D. Blumofe, Paul R. Wilson]
  note: Presented at ASPLOS 2000. It was the first allocator with a proof that its memory use stays within a constant factor of a serial allocator while it scales with the number of processors.
prereqs: [segregated-free-lists, size-classes, allocator]
see_also: [tcmalloc, jemalloc, mimalloc, lock-free-memory-allocator, dlmalloc, slab-allocator, internal-fragmentation, online-memory-allocation]
sources:
  - paper: doi:10.1145/378993.379232
    title: "Emery D. Berger, Kathryn S. McKinley, Robert D. Blumofe and Paul R. Wilson, Hoard: a scalable memory allocator for multithreaded applications, ASPLOS IX, 2000, 117-128"
    locator: Section 2 (false sharing and blowup), Section 3.1 (the emptiness threshold and the invariant), Section 3.3, Figure 2 (malloc and free), Section 4.1 (Lemma 1 and Theorem 1)
  - paper: doi:10.1007/3-540-60368-9_19
    title: "Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation: a survey and critical review, IWMM 1995, LNCS 986, 1-116"
    locator: Section 3.6 (segregated storage by size class, the basis of superblocks)
---

Hoard is a memory [allocator](/allocator/) for multithreaded programs, published by Berger, McKinley, Blumofe and Wilson in 2000. It keeps one heap per processor and one global heap. Each heap owns superblocks: blocks of $S$ bytes cut into objects of one [size class](/size-classes/). A thread allocates only from the heap of its processor, so threads rarely contend for a lock and never get pieces of one superblock at the same time. When a heap becomes too empty, it gives a mostly empty superblock to the global heap, where another heap can reuse it. This rule keeps the memory that Hoard holds within a constant factor of the memory in use, which allocators with private heaps and no such rule do not do.

## In plain words

A company has one storeroom per team and one shared storeroom. Supplies come in boxes, and each box holds items of one size. A worker takes items only from the storeroom of their own team, so teams do not wait for each other. Two teams never take items from the same box at the same time, so they do not get in each other's way at the desk where the box sits.

Items can be handed back anywhere, but each item goes back to its own box. If a team's storeroom has many empty places, it sends its emptiest box to the shared storeroom. A team that runs out first looks there before it orders a new box. So no storeroom can sit on a large pile of unused boxes while another team orders more.

## The problem

This is [online memory allocation](/online-memory-allocation/) with $P$ processors that call malloc and free at the same time. A good parallel allocator must be fast, must scale with $P$, must not cause false sharing, and must not waste memory.

- **False sharing.** Two processors write different objects that lie in one cache line, and the line moves between their caches on every write. An allocator causes it actively if it gives parts of one cache line to two threads, and passively if a thread frees an object that another thread allocated and the allocator then gives that memory to a third thread.
- **Blowup.** The paper defines blowup as the most memory an allocator holds divided by the most memory that an ideal serial allocator would need. With one heap per thread and no exchange, a producer thread that allocates objects freed by a consumer thread makes the consumer's heap grow without bound, because the producer never sees the freed memory. Simple designs with $P$ heaps have blowup up to a factor of $P$ or without limit.

## The algorithm

Heap 0 is the global heap. Heaps $1, \ldots, P$ belong to processors, and a thread maps to a heap by a hash of its id. Heap $i$ keeps $u_i$, the bytes in use in its superblocks, and $a_i$, the bytes of the superblocks it holds. A superblock $s$ keeps $s.u$, its bytes in use, its owner, and a free list of its blocks in LIFO order. The two parameters are the empty fraction $f$ and a slack $K$ of whole superblocks. Heap $i$ crosses the emptiness threshold when

$$u_i < a_i - K S \quad\text{and}\quad u_i < (1 - f)\,a_i .$$

```pseudo id=main
MALLOC(sz) by a thread t
L1  if sz > S/2 then return a separate mapping from the system
L2  i ← heap of t; c ← size class of sz
L3  s ← the fullest superblock of class c in heap i that has a free block
L4  if there is none then
L5      if heap 0 has a superblock of class c with a free block, or an empty one, move it to heap i:
            u_0 ← u_0 − s.u; a_0 ← a_0 − S; u_i ← u_i + s.u; a_i ← a_i + S
L6      else s ← a new superblock of S bytes from the system, owned by heap i; a_i ← a_i + S
L7  take the first block of the free list of s; s.u ← s.u + c; u_i ← u_i + c
L8  return the block

FREE(p)
L9  if p is a large object then return its mapping to the system; return
L10 s ← the superblock of p; i ← the owner of s
L11 put p at the front of the free list of s; s.u ← s.u − c; u_i ← u_i − c
L12 if i = 0 then return
L13 while u_i < a_i − K·S and u_i < (1 − f)·a_i do
L14     move the emptiest superblock of heap i to heap 0, with the same updates of u and a
```

Every step of MALLOC and FREE on heap $i$ runs under the lock of heap $i$; FREE also locks the superblock first, because its owner can change. The global heap has its own lock, taken only at L5, L13 and L14 and for frees into its superblocks.

**Allocation** (L1 to L8). Objects larger than half a superblock go to the system. Otherwise the thread uses its own heap and the fullest superblock of the right class with room. Allocating from nearly full superblocks lets mostly empty ones drain, so that they can be given away. If the heap has no room, the global heap is tried before the system.

**Free** (L9 to L14). A block always goes back to the free list of its own superblock, whichever thread frees it. This is how Hoard avoids passive false sharing: the freed piece returns to the heap that owns its superblock, not to the heap of the thread that freed it. Then, if heap $i$ is too empty, superblocks move to heap 0. The paper finds a superblock that is at least $f$ empty in constant time with fullness groups: each heap keeps, per size class, a few lists of superblocks by how full they are, and moves a superblock to the front of its list when one of its blocks is freed.

**The invariant.** Section 3.1 states that the rule keeps, for every processor heap,

$$\bigl(u_i \ge a_i - K S\bigr) \;\lor\; \bigl(u_i \ge (1 - f)\,a_i\bigr).$$

Figure 2 of the paper moves one superblock per free. The model moves superblocks while the threshold is crossed, so the invariant holds after every free; see the pitfalls for why one move is not always enough.

## Example

The code of this page is a small model of Hoard in Python, not the real allocator: it runs in one thread, counts superblocks and blocks, and only computes addresses. This trace comes from the model. Two processors, so heaps 1 and 2; thread 0 uses heap 1 and thread 1 uses heap 2. $S = 64$, every object has 16 bytes, so a superblock holds 4 blocks. $f = 1/4$ and $K = 0$, so heap $i$ crosses the threshold when $u_i < a_i$ and $u_i < \tfrac34 a_i$.

| Step | Call | Action | $u_1, a_1$ | $u_2, a_2$ | $u_0, a_0$ |
|---|---|---|---|---|---|
| 1 | thread 0: malloc(16) five times | superblock A at 0 gets 0, 16, 32, 48; new superblock B at 64 gets 64 (L6) | 80, 128 | 0, 0 | 0, 0 |
| 2 | thread 1: malloc(16) | new superblock C at 128 for heap 2; returns 128 | 80, 128 | 16, 64 | 0, 0 |
| 3 | thread 1: free(16) | the block goes back to A, owned by heap 1 (L11); $64 < 96$: move B, the emptiest, to heap 0 (L14) | 48, 64 | 16, 64 | 16, 64 |
| 4 | thread 1: free(64) | the block is in B, owned by heap 0, so only heap 0 changes (L12) | 48, 64 | 16, 64 | 0, 64 |
| 5 | thread 1: malloc(16) four times | 144, 160, 176 from C; C is full, so heap 2 takes the empty B from heap 0 (L5) and gets 64 | 48, 64 | 80, 128 | 0, 0 |
| 6 | thread 0: malloc(16) | A has a free block; LIFO gives 16 back | 64, 64 | 80, 128 | 0, 0 |

At step 3 a block of heap 1 is freed by thread 1, but the block returns to heap 1, so thread 1 never reuses a piece of a superblock that thread 0 writes. At step 5 heap 2 reuses the superblock that heap 1 gave away, so the system gave out only three superblocks, 192 bytes, for at most 128 bytes in use.

## Correctness

Each block of a superblock is either on its free list or handed out, never both, because L7 takes it off the list and L11 puts it back. A block is handed out only by the heap that owns its superblock, and a superblock has one owner at a time, so no block is given to two threads. The counters $u_i$ and $a_i$ change only with the moves and the block operations they count, so they stay equal to the sums over the superblocks of heap $i$. The loop at L13 stops: each move lowers $a_i$ by $S$, and at $a_i = 0$ the first condition fails. When the loop runs, an emptiest superblock exists and has $s.u \le (1-f) S$, because the average fullness is below $1 - f$. After the loop the invariant holds for heap $i$. The full argument, with the memory bound below, is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time.** A malloc finds a superblock of the right class with room in $O(1)$ through the fullness groups, or scans the $g$ groups of its class; L5 looks in the global heap the same way. A free finds its superblock from the address or the block header in $O(1)$ and moves superblocks in $O(1)$ each. With a constant number of size classes and groups, both calls take $O(1)$ time plus lock waits. The model scans lists instead.
- **Memory (Theorem 1).** Let $A(t)$ be the most memory held and $U(t)$ the most memory in use up to step $t$. The paper proves $A(t) = O(U(t) + P)$, so blowup is $O(1)$ when $P$ is small next to $U(t)$. From the invariant, each heap holds $a_i \le u_i/(1-f) + KS$ after a free. The test of the model checks, for one size class, $a_i \le u_i/(1-f) + (K+1)S$ at all times and total system memory at most $U/(1-f) + P(K+1)S$; the extra $S$ per heap is the superblock that a malloc may have just added.
- **Contention.** In a growing phase a thread takes the global lock at most once per $fS/s$ allocations of size $s$, because each superblock from the global heap has at least that many free blocks. The paper notes a bad case in a shrinking phase, where each free can cross the threshold, but it needs a contrived sequence of frees.

## Properties

- **No active false sharing.** Only the owner heap allocates from a superblock, so two threads on different processors never get blocks of one superblock at the same time.
- **Little passive false sharing.** Freed blocks go back to their superblock. A superblock that moves to another heap is at least $f$ empty, and in practice often empty.
- **Bounded blowup.** The emptiness rule bounds memory to $O(U + P)$. Producer and consumer threads do not make memory grow without limit.
- **Locks.** One lock per heap and one for the global heap; Hoard is not lock-free.
- **Locality.** LIFO free lists and move-to-front in the fullness groups reuse memory that is likely still in the cache.

## Variants and improvements

- **Heaps per thread instead of per processor.** Where threads cannot be mapped to processors, the hash at L2 maps thread ids to heaps; collisions only add lock contention, not blowup, because the bound depends on the number of heaps.
- **[tcmalloc](/tcmalloc/) and [jemalloc](/jemalloc/).** Both give each thread or CPU a cache and several arenas, with size-class runs or spans much like superblocks, but they bound memory by trimming caches instead of by Hoard's invariant.
- **[mimalloc](/mimalloc/).** Pages per size class owned by one thread, as in Hoard, with separate free lists for local and remote frees, so a remote free needs no lock.
- **[Lock-free allocators](/lock-free-memory-allocator/).** Michael's allocator keeps Hoard's superblocks and replaces the locks with compare-and-swap.

## When to use it

Use a Hoard-style allocator for C and C++ programs with many threads, especially when threads free objects that other threads allocated, as in producer and consumer pipelines, and when memory use must stay bounded. For a single thread, a serial allocator such as [dlmalloc](/dlmalloc/) is simpler and at least as fast. For the highest speed on modern systems, allocators with per-thread or per-CPU caches and no lock on the fast path, such as [tcmalloc](/tcmalloc/) and [mimalloc](/mimalloc/), are the common choice.

## Pitfalls

- **One move is not always enough.** Figure 2 moves one superblock at L14, and Section 3.1 argues that one move restores the invariant. That argument assumes the invariant held before the free. But malloc does not check the threshold: L5 and L6 add $S$ to $a_i$ while adding only one block to $u_i$. With several size classes, one heap can hold several nearly empty superblocks; the model's test has a trace where one free needs three moves. Use a loop at L13, or check after L6 too.
- **Returning a block to the freeing thread's heap.** If L11 put the block in heap of the calling thread instead of in its own superblock, Hoard would induce passive false sharing and lose its memory bound for producer and consumer threads.
- **Allocating from emptier superblocks first.** If L3 took the emptiest superblock, superblocks would never drain, and the heap would not cross the threshold to give them away.
- **Reading the invariant as "and".** The invariant is the "or" of two conditions; the threshold at L13 is its negation, the "and" of the two strict inequalities. Using "or" at L13 would move superblocks whenever one condition fails, for example on every free with $K = 0$.
- **Lock order.** FREE locks the superblock and then its owner heap. Locking the heap first is a race: the superblock can move to another heap between the read of the owner and the lock.

## Implementations

## History

Emery Berger, Kathryn McKinley, Robert Blumofe and Paul Wilson presented Hoard at ASPLOS in 2000. Earlier parallel allocators used one heap with one lock, which does not scale, or private heaps per thread, which can have unbounded blowup, as in the allocators of the Cilk and STL systems that the paper discusses, or blowup linear in $P$, as in ptmalloc and LKmalloc. Hoard was the first to combine per-processor heaps with a rule that provably bounds blowup and that avoids active false sharing. On 14 processors the paper reports Hoard up to 60 times faster than the standard Solaris allocator, and up to 18 times faster than the next best allocator it tested. Its superblock and ownership design shaped later allocators, including Michael's lock-free allocator.

## References
