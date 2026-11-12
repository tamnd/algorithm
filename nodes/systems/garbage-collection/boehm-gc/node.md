---
tag: SF0WFK
kind: algorithm
slug: boehm-gc
name: Boehm-Demers-Weiser collector
aliases:
- Boehm GC
- Boehm-Demers-Weiser garbage collector
- bdwgc
- libgc
area: systems/garbage-collection
level: advanced
summary: "A conservative, non-moving mark-sweep collector for C and C++, with size-class blocks, free lists, blacklisting of false pointers and an incremental mode."
solves: [automatic-memory-reclamation]
model: word-ram
complexity:
  vars: {r: the number of root words, L: the words of the marked objects, H: the words of the blocks in use, N: the number of blocks}
  time: {worst: O(r + L + H), best: O(r + N)}
  space: {extra: O(H)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1988
  people: [Hans-Juergen Boehm, Mark Weiser, Alan Demers]
  note: Boehm and Weiser described a garbage collector for C in an uncooperative environment in 1988; blacklisting (1993) and a mostly parallel, generational mode with Demers and Shenker (1991) followed.
prereqs: [conservative-garbage-collection, mark-and-sweep, segregated-free-lists]
see_also: [mostly-copying-collection, precise-garbage-collection, size-classes, lazy-sweeping, generational-garbage-collection, concurrent-garbage-collection, finalization, thread-local-allocation-buffer]
sources:
  - paper: doi:10.1002/spe.4380180902
    title: Hans-Juergen Boehm and Mark Weiser, Garbage collection in an uncooperative environment, Software Practice and Experience 18(9), 807-820, 1988
    locator: the conservative mark-sweep design for C, the test for a valid object pointer, and the heap of blocks with objects of one size
  - paper: doi:10.1145/155090.155109
    title: Hans-Juergen Boehm, Space efficient conservative garbage collection, PLDI 1993, 197-206
    locator: blacklisting of addresses that look like pointers into the heap, and the measurements of false retention
  - paper: doi:10.1145/113445.113459
    title: Hans-Juergen Boehm, Alan J. Demers and Scott Shenker, Mostly parallel garbage collection, PLDI 1991, 157-164
    locator: virtual memory dirty bits to find pages written during concurrent marking, and the generational use of the same bits
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Chapter 11, Section 11.2 (Finding pointers), on conservative pointer finding, interior pointers and blacklisting
---

The Boehm-Demers-Weiser collector is a garbage collector for C and C++ programs, whose compilers give no help to a collector. It is a [conservative](/conservative-garbage-collection/) [mark-and-sweep](/mark-and-sweep/) collector: it treats every word in the registers, the stacks, the static data and the heap objects as a possible pointer, marks every object that such a word points into, and sweeps the rest onto free lists. It never moves an object, because it cannot tell a pointer from an integer and so must not change either. The heap is a set of blocks; each block holds objects of a single [size class](/size-classes/), and allocation pops an object from a [segregated free list](/segregated-free-lists/). *Blacklisting* stops a number that looks like a pointer from retaining memory: during marking, the collector records the free blocks that such words point into, and the allocator does not use those blocks. The collector is a library: a program replaces `malloc` with `GC_MALLOC` and drops its calls to `free`.

## In plain words

C programs do not say which values are pointers. So this collector plays safe. Every value that could be the address of an object counts as a pointer, and that object stays alive. Objects that no such value reaches are free, and the collector puts their memory on lists for reuse. It never moves anything, because moving an object means changing the values that point to it, and some of those values may be plain numbers.

A number can keep garbage alive by accident. The collector reduces this in a clever way. When it sees a number that points into memory that is still unused, it notes that place, and later it does not put new objects there. So the number cannot hold on to a new object.

## The problem

Collect the heap of a C or C++ program without any help from the compiler. The roots are the registers, the stacks and the static data, and nothing says which of their words are pointers. Heap objects carry no type information, except that the program may say an object holds no pointers at all. Free every object that the program can no longer reach, never free an object that it can reach, never change a word of the program, and keep the memory that numbers falsely retain small.

## The algorithm

The heap is an array of $N$ blocks. A block is either free or holds objects of one size $s$ and one kind: *normal* objects may hold pointers and are scanned; *atomic* objects, from `GC_MALLOC_ATOMIC`, hold no pointers and are not scanned. Each block has a mark bit and an allocated bit for each of its objects. There is a free list for each size and kind, and a blacklist of free blocks.

```pseudo id=main
ALLOCATE(n, kind)
L1  s ← the size class of n; if the free list F[s, kind] is empty then REFILL(s, kind)
L2  pop an object from F[s, kind], set its allocated bit, clear its words, and return it

REFILL(s, kind)
L3  take a free block that is not blacklisted (COLLECT first if there is none); give it size s and kind; put all its objects on F[s, kind]

COLLECT()
L4  newBlacklist ← ∅; clear the mark stack
L5  for each root word w do MARK-IF-POINTER(w)
L6  while the mark stack is not empty do pop o; if o is normal then for each word w of o do MARK-IF-POINTER(w)
L7  blacklist ← newBlacklist
L8  for each block in use: if no object is marked, free the block; else put each unmarked object on its free list, clear its allocated bit, and clear all marks

MARK-IF-POINTER(w)
L9  if w is not an address in the heap then return
L10 if w points into an allocated object o (or to its first word, if interior pointers are off) then mark o and push it, unless o is already marked
L11 else if w points into a free block b then add b to newBlacklist
```

Line L10 is the *valid pointer test*. It finds the block of $w$ by dividing its offset by the block size, reads the block header, and finds the object by dividing the offset in the block by the object size. A word that falls between objects, on an object that is not allocated, or outside the heap, is ignored. This test is what keeps the collector safe: only words that hit an allocated object can mark it, and a wrong mark only keeps an object longer than needed.

Line L11 is blacklisting. A word that points into a free block cannot be a pointer the program will use, since nothing is there. But if the allocator later put an object in that block, the word would point into it and keep it alive forever. So the collector records the block, and line L3 avoids it. The blacklist is rebuilt at each collection, so a block leaves it when the false reference goes away.

Line L8 is the sweep. A block with no marked object goes back to the pool of free blocks, where any size class can reuse it. In other blocks, each unmarked object goes on the free list of the block's size and kind. The library sweeps lazily: it sweeps a block only when the allocator needs objects of that size, as in [lazy sweeping](/lazy-sweeping/). The model sweeps every block at once.

## Example

The heap starts at address 1000 and has 4 blocks of 4 words, so block 2 is $[1008, 1012)$. The size classes are 1, 2 and 4 words. The program holds the integer 1009 in a global variable, which the collector must treat as a root. It allocates three objects of 4 words, $p$, $q$ and $r$, stores $p$ in the first word of $r$, and then drops all three.

| step | with blacklisting | without blacklisting |
|---|---|---|
| early COLLECT | 1009 points into free block 2: blacklist $= \{2\}$ | nothing to do |
| allocate $p$, $q$, $r$ | blocks 0, 1, 3: $p = 1000$, $q = 1004$, $r = 1012$ | blocks 0, 1, 2: $r = 1008$ |
| COLLECT | 1009 still points into free block 2; nothing is marked; all three blocks are freed | 1009 points into $r$, which is marked; scanning $r$ marks $p$; only $q$ is freed |

Without blacklisting, a single number keeps 8 words of garbage, and the chain could be any length. With it, nothing is retained. The early collection matters: it finds false references in static data while their targets are still free. The tests run this example in both modes.

## Correctness

**Claim.** Assume the program keeps every pointer it will use as a word, in a root or in a normal object, that points to the first word of its object (or into it, with interior pointers on). Then: (1) COLLECT never frees an object the program can reach, and never changes a word of a reachable object; (2) the objects it keeps are exactly those reached from the root words by the closure of line L10, and the blacklist is exactly the set of free blocks that the words met during marking point into; (3) ALLOCATE never returns an object that is allocated; (4) REFILL uses a blacklisted block only when every free block is blacklisted.

**Proof sketch.** (1) By induction along a path of pointers from a root: the root word hits its object at line L10, so the object is marked and pushed; when it is popped at line L6, it is normal (it holds a pointer), so its words are tested, and the next object on the path is marked. Line L8 frees only unmarked objects, and the collector writes only mark bits, allocated bits and free lists. (2) The marking loop is a graph search over the words, and line L11 sees exactly the words that hit a free block. (3) Free lists are built only from unmarked objects whose allocated bit L8 clears, or from a fresh block, and line L2 sets the bit when it hands an object out. (4) Line L3 picks from the free blocks that are not blacklisted. The proof file below gives the details. The tests check (1) to (4) on random programs, with random data words that often look like pointers, against a plain search over the object list.

## Complexity

Lines L5 to L7 take $O(r + L)$ time for $r$ root words and $L$ words of marked objects: each object is marked and scanned once, and each valid pointer test takes $O(1)$ time with a block header table. The sweep looks at each object slot of the blocks in use, $O(H)$, and at each block, $O(N)$; with lazy sweeping this cost moves into allocation. If nothing is marked, a block can be freed by checking a count of marked objects, so the best case is $O(r + N)$. Space: one mark bit and one allocated bit per object slot, a block header per block, and the mark stack, which can hold every object, so $O(H)$ in the worst case. The library limits the stack and recovers from overflow by rescanning the heap for marked objects with unmarked children.

## Properties

- **Conservative.** The roots and the heap are both scanned without type information, except that atomic objects are not scanned.
- **Non-moving.** Objects never move, so the program may keep pointers anywhere the collector scans, hash them, and pass them to code that does not know about the collector.
- **Not compacting.** Fragmentation is controlled only by size-segregated blocks and by returning empty blocks.
- **Stop the world by default.** The basic collection stops the program; incremental, generational and parallel modes reduce or share the pause.

## Variants and improvements

- **Incremental and generational mode.** Boehm, Demers and Shenker (1991) mark while the program runs, then stop it briefly and remark from the pages that it wrote. The operating system supplies the written pages, as virtual memory dirty bits, or by write-protecting pages and catching the faults. The same bits give a generational collector without a compiler [write barrier](/write-barrier/): a partial collection keeps the marks of old objects and rescans only the dirty pages, much like [card marking](/card-marking/) with pages as cards. See [concurrent garbage collection](/concurrent-garbage-collection/) and [generational garbage collection](/generational-garbage-collection/).
- **Parallel marking.** Several threads mark at the same time, each with its own mark stack, and steal work from each other.
- **Thread-local free lists.** Each thread takes a batch of free objects per size class and allocates from it without a lock, which plays the role of a [thread-local allocation buffer](/thread-local-allocation-buffer/). Since objects do not move, the collector cannot use [bump-pointer allocation](/bump-pointer-allocation/) over the whole heap.
- **Typed allocation.** The program can give a bitmap of the pointer words of an object, so the collector scans only those words and fewer numbers look like pointers.
- **Leak detection.** In leak detection mode, the program keeps calling `free`, and the collector reports objects that became unreachable without being freed.
- **Finalization.** The library can run a function when an object becomes unreachable; see [finalization](/finalization/).

## When to use it

Use the collector to add garbage collection to C or C++ code, or to a language runtime that compiles to C or calls C code, when the compiler cannot produce stack maps for [precise collection](/precise-garbage-collection/). It needs no change to the compiler and almost none to the program. If the runtime knows the layout of heap objects and wants compaction, [mostly-copying collection](/mostly-copying-collection/) keeps those benefits with ambiguous roots. For a new managed language with full compiler support, a precise moving collector usually has better throughput and less memory overhead.

## Pitfalls

- **Hidden pointers.** A pointer that the program stores in a disguised form, such as XOR linked lists, pointers written to a file, or pointers kept only in memory from the system `malloc`, is not seen, and its object can be freed while in use.
- **False retention.** A number that looks like a pointer keeps its object and all that the object reaches. Large objects and linked structures, such as long lists, make this worse. Blacklisting, atomic allocation and typed allocation reduce it.
- **Compiler optimizations.** An optimizing compiler can keep only a derived value of a pointer, such as an address past the end of an array, after the last use of the base pointer. Interior pointer recognition covers most such cases.
- **Pointer-free data allocated as normal.** Large buffers of numbers or text allocated with `GC_MALLOC` are scanned and add false pointers; allocate them with `GC_MALLOC_ATOMIC`.
- **Blacklisted heap.** If most free blocks are blacklisted, large objects are hard to place and the heap grows. The library grows the heap rather than use a blacklisted block, where possible.

## Implementations

## History

Boehm and Weiser published the collector in 1988 under the title "Garbage collection in an uncooperative environment", with the test for a valid object pointer and the heap of blocks with objects of one size. Alan Demers took part in its development, which gives the collector its full name. Boehm, Demers and Shenker added the mostly parallel and generational mode, based on virtual memory dirty bits, in 1991. Boehm's 1993 paper on space efficient conservative collection introduced blacklisting and measured how little memory false pointers retain when it is used. The library has been maintained for decades and is used by language runtimes such as GNU Guile, the GCC Java front end and early versions of Mono, as well as by many C and C++ programs.

## References
