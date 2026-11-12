---
tag: 9J5R6H
kind: algorithm
slug: lock-free-memory-allocator
name: Lock-free memory allocator
aliases:
- Michael's lock-free allocator
area: systems/memory-allocation
level: research
summary: "Maged Michael's malloc with no locks: each superblock has a one-word anchor changed only by CAS, a tag in the anchor stops the ABA problem, and a stopped thread cannot block the others."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {k: the number of successful updates by other threads during the call, s: the number of superblocks}
  time: {worst: O(k + 1), average: O(1)}
  space: {extra: O(s)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2004
  people: [Maged M. Michael]
  note: Written at the IBM Thomas J. Watson Research Center and presented at PLDI 2004; it takes its superblocks and processor heaps from Hoard.
prereqs: [compare-and-swap, aba-problem, treiber-stack, hoard-allocator]
see_also: [lock-freedom, hazard-pointers, epoch-based-reclamation, safe-memory-reclamation, mimalloc, tcmalloc, jemalloc, size-classes]
sources:
  - paper: doi:10.1145/996893.996848
    title: "Maged M. Michael, Scalable lock-free dynamic memory allocation, PLDI 2004, 35-46"
    locator: Section 3.1 (overview), Section 3.2 (Figure 3 structures, Figure 4 malloc, Figure 5 example, Figure 6 free, Figure 7 descriptor allocation, the ABA scenario of Section 3.2.3), Section 4 (results)
---

The lock-free memory allocator of Maged Michael, presented at PLDI 2004, is a malloc and free with no locks at all. It keeps the superblocks and processor heaps of [Hoard](/hoard-allocator/), but every shared field fits in one machine word and changes only by [compare-and-swap](/compare-and-swap/) (CAS). The center is the anchor of each superblock: one word that holds the first free block, the number of free blocks, the state of the superblock and a tag. Because no thread ever holds a lock, a thread that is stopped, killed or interrupted by a signal cannot block the others, so the allocator can be used in signal handlers and real-time code.

## In plain words

Think of a box of tickets with a small display on its lid. The display shows which ticket is on top, how many are left, and a counter. To take a ticket, you read the display, look at the ticket below the top one, and then try to change the display in one move. The change works only if the display still shows exactly what you read. If someone else was faster, you read it again and try again.

Without the counter, a slow person can be fooled: the same top ticket can come back after other people took and returned tickets, and the "next" ticket that the slow person saw may now be in someone's hand. The counter goes up at every take, so the display is never the same twice.

## The problem

This is [online memory allocation](/online-memory-allocation/) for programs with many threads, where malloc and free must be [lock-free](/lock-freedom/): whenever threads take a finite number of steps, some call finishes. Locks in a malloc cause deadlock when a signal handler calls malloc while its thread holds the lock, priority inversion, and a stop of the whole allocator if a thread dies while holding a lock. Earlier allocators that avoided some locks needed help from the operating system. Michael's allocator uses only CAS on one aligned 64-bit word and the usual calls to get memory from the system.

## The algorithm

Memory for small blocks comes in superblocks (for example 16 KiB) of equal blocks, one size class each. Each superblock has a descriptor with an Anchor of four fields that one CAS changes together:

- avail: the index of the first free block; the free blocks form a list through their first words;
- count: the number of free blocks that no thread has reserved;
- state: ACTIVE, FULL, PARTIAL or EMPTY;
- tag: a counter against the [ABA problem](/aba-problem/).

Each processor heap has one size class, an Active field and a Partial slot. Active points to the descriptor of the active superblock and holds a few credits in its low bits: with $c$ credits, $c + 1$ blocks of that superblock are reserved for the heap. Each size class also has a list of partial superblocks. Every block starts with a prefix that points to its descriptor.

```pseudo id=main
MALLOC(t)
L1  heap ← the heap of t's processor; loop: return the first block from ACTIVE(heap), PARTIAL(heap) or NEW-SB(heap)

ACTIVE(heap)
L2  repeat old ← heap.Active; if old = null return null; new ← old with one credit less, or null if it had none
    until CAS(heap.Active, old, new)                          ▷ one block of old.desc is now ours
L3  repeat a ← desc.Anchor; b ← block a.avail; next ← the first word of b
L4      a' ← a with avail = next and tag = a.tag + 1
        if old had no credit: if a.count = 0 then a'.state ← FULL else m ← min(a.count, MAXCREDITS); a'.count ← a.count − m
L5  until CAS(desc.Anchor, a, a')
L6  if m credits were taken then UPDATE-ACTIVE(heap, desc, m); return b

UPDATE-ACTIVE(heap, desc, m)
L7  if CAS(heap.Active, null, (desc, m − 1)) then return
L8  else give the m credits back: CAS desc.Anchor to count + m and state PARTIAL; put desc in heap.Partial

PARTIAL(heap)
L9  desc ← take heap.Partial by CAS, else take one from the partial list of the class; if none return null
L10 repeat a ← desc.Anchor; if a.state = EMPTY then retire desc and go to L9
        m ← min(a.count − 1, MAXCREDITS); a' ← a with count − (m + 1) and state ACTIVE if m > 0, else FULL
    until CAS(desc.Anchor, a, a')
L11 pop one block as in L3 to L5, with tag + 1; if m > 0 then UPDATE-ACTIVE(heap, desc, m); return the block

NEW-SB(heap)
L12 get a superblock, link its blocks 1, 2, ...; c ← min(maxcount − 1, MAXCREDITS) − 1; Anchor ← (1, maxcount − 1 − (c + 1), ACTIVE, 0)
L13 if CAS(heap.Active, null, (desc, c)) then return block 0; else give the superblock back and return null

FREE(b)
L14 desc ← the prefix of b; repeat a ← desc.Anchor; first word of b ← a.avail; a' ← a with avail = b
        if a.state = FULL then a'.state ← PARTIAL
L15     if a.count = maxcount − 1 then a'.state ← EMPTY else a'.count ← a.count + 1
    until CAS(desc.Anchor, a, a')
L16 if a'.state = EMPTY then give the superblock back and remove desc from the partial structures
    else if a.state = FULL then put desc in the Partial slot of its heap
```

**Two steps for a block** (L2 to L5). A malloc first reserves a block by taking a credit from Active with one CAS (L2). After that the block is surely there, and the thread only has to pop the head of the anchor's list (L3 to L5). This is a lock-free stack pop like the [Treiber stack](/treiber-stack/), done on indices inside the anchor word. Only the thread that took the last credit refills Active (L4, L6), so two threads never refill the same heap at once.

**The tag** (L4). Suppose thread X reads avail = A and next = B at L3 and then stops. Others pop A and B and then free blocks until avail is A again and count is the same as before. Without the tag, X's CAS at L5 succeeds and sets avail to B, a block that is in use. The next malloc hands B out a second time. The tag goes up at every pop, so X's CAS fails and X reads the anchor again. The paper gives the tag 42 bits, so a full wrap during one delay is practically impossible.

**States** (L4, L8, L10, L15, L16). A FULL superblock is in no list, so the first free to it makes it PARTIAL and puts it in the heap's Partial slot (L16). The free of the last used block makes it EMPTY, and that thread gives the superblock back to the system. A PARTIAL superblock is taken at L9 and gets its credits at L10.

## Example

The code of this page is a sequential model in Python, not a real allocator: each call is a generator that yields before each access to shared memory, and a scheduler decides which thread takes the next atomic step. This trace is the ABA scenario of the paper, run in the model with one heap, superblocks of 8 blocks and MAXCREDITS = 2. The anchor is written (avail, count, state, tag), with A for ACTIVE.

| Step | Thread | Action | Active credits | Anchor |
|---|---|---|---|---|
| 1 | Y | malloc: new superblock (L12, L13); Y gets block 0 | 1 | (1, 5, A, 0) |
| 2 | X | malloc: takes a credit (L2), reads avail = 1 and next = 2 (L3), stops before L5 | 0 | (1, 5, A, 0) |
| 3 | Y | malloc: takes Active (L2), pops block 1, takes 2 credits (L4), puts them in Active (L7) | 1 | (2, 3, A, 1) |
| 4 | Y | malloc: takes a credit, pops block 2 | 0 | (3, 3, A, 2) |
| 5 | Y | free(0), then free(1) (L14, L15) | 0 | (1, 5, A, 2) |
| 6 | X | CAS at L5 expects (1, 5, A, 0): it fails; X reads again and pops block 1 | 0 | (0, 5, A, 3) |
| 7 | Y | malloc: takes 2 credits and pops block 0 | 1 | (3, 3, A, 4) |

Without the tag, every tag in the table stays 0. At step 6 X's CAS then succeeds and sets avail to 2, though Y still holds block 2. At step 7 Y receives block 2 again. The tests run both versions of this schedule.

## Correctness

Every block of a superblock is either held by the program, or reserved by a credit, or on the anchor's free list and counted in count. Each CAS moves blocks between these sets and changes count and the credits to match, so at a moment when no call is running, the free list has exactly count + (reserved) blocks and no held block is on it. A pop at L5 succeeds only if the anchor, tag included, has not changed since L3, so the next block it installs was free at that moment. The tag is what makes this true. The proof is in [the correctness proof](proofs/correctness.md).

Lock-freedom: every loop in the algorithm retries only when a CAS fails, and a CAS fails only when another thread changed the field, which ends or moves forward that other thread's call. A thread that stops at any point holds no lock; at worst it keeps one reserved block or one superblock away from others.

## Complexity

- **Time.** With no contention, malloc does about two CAS operations and free one. Under contention a call retries once for each change by another thread to the same field, so a call that sees $k$ such changes takes $O(k + 1)$ steps. This is the cost of lock-freedom: no single call has a bound, but the system as a whole always moves forward.
- **Space.** One descriptor per superblock, and an 8-byte prefix per block. The paper states that blowup is a constant factor, as in Hoard, and that descriptors are less than 1% of memory.
- **Speed.** On 16 POWER3 processors under maximum contention, the paper reports a speedup of 331 over the AIX libc malloc, and lower latency than Hoard and Ptmalloc without contention.

## Properties

- **Lock-free.** No call waits for another, so there is no deadlock, the allocator is safe in signal handlers, and a thread that dies in malloc does not stop the others.
- **One-word state.** All fields that CAS changes fit in one aligned 64-bit word, so the allocator needs no double-word CAS.
- **Fine-grained.** Threads on different superblocks never touch the same word, and a free into a superblock of another heap costs no more than a local one.
- **Hoard structure.** Processor heaps and superblocks keep false sharing low and blowup bounded, but the allocator keeps no fullness groups and moves partial superblocks to the class list soon.

## Variants and improvements

- **Contrast with [hazard pointers](/hazard-pointers/).** The tag works for the anchor because the list there is made of small indices that leave room for a tag in the word. Lists of descriptors are linked by full pointers, which leave no room. For those lists the paper uses hazard pointers (DescAlloc in Figure 7) and LL/SC built from CAS. Hazard pointers stop the ABA problem by keeping a node from reuse while a thread may still read it, and they bound the unreclaimed memory even when a thread stops.
- **Contrast with [epoch-based reclamation](/epoch-based-reclamation/).** EBR also stops reuse while a thread may still read, and it costs less per access. But one stopped thread stops all reclamation, so memory can grow without bound. That does not fit an allocator whose aim is to keep working when threads die. The anchor tag needs no reclamation scheme at all: a thread reads a block only after it has reserved one, and a superblock with a reserved block is never EMPTY, so it is never given back during the read.
- **Later allocators.** Allocators such as [mimalloc](/mimalloc/) use CAS only for frees from other threads and keep the common path free of atomic operations; [tcmalloc](/tcmalloc/) and [jemalloc](/jemalloc/) use per-thread or per-CPU caches with locks behind them.

## When to use it

Use a lock-free allocator where locks are not allowed or too risky: in signal handlers, real-time threads, systems that must keep running when a thread is killed, and code with high contention on few processors. When the program has none of these needs, allocators with thread caches have a faster common path, because they need no atomic operation at all on most calls.

## Pitfalls

- **Leaving out the tag** (L4). Without it, the ABA schedule of the example hands out a block that is in use. The count field does not prevent this, because frees can restore it.
- **Popping without a reservation** (L2). The read of the next index at L3 is safe only because the thread has reserved a block, so the superblock cannot become EMPTY and be given back. A pop that skips L2 can read memory that the system has taken back.
- **Losing a FULL superblock** (L16). A FULL superblock is in no list. If the first free to it did not put it in a Partial slot, its free blocks would never be used again.
- **Tags on pointer-sized fields.** Active and the lists of partial superblocks hold full pointers. A tag does not fit there, so these need other ABA protection, such as hazard pointers or LL/SC.
- **Weak memory models.** The model assumes sequential consistency. On real hardware the stores to a new superblock must be visible before the CAS at L13, and the store of the first word at L14 before the CAS at L15; the paper places fences there.

## Implementations

## History

Maged M. Michael presented the allocator at PLDI 2004, while at the IBM Thomas J. Watson Research Center. He had earlier written about hazard pointers and lock-free memory management, which the allocator uses for its descriptor lists. The tag on the anchor is the classic IBM tag method, first given in the IBM System/370 documentation as the reason for the CAS instruction. Lock-free synchronization goes back to work by Lamport, and Herlihy showed that CAS is strong enough for lock-free versions of any object. Earlier allocators avoided some locks with help from the kernel, such as the allocator of Dice and Garthwaite. Michael set out to show that a malloc can be completely lock-free and still compete with the best lock-based allocators, using only hardware and system support that is widely available and without assumptions that make lock-free progress trivial.

## References
