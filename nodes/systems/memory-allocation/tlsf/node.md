---
tag: P3XK4D
kind: algorithm
slug: tlsf
name: Two-level segregated fit (TLSF)
aliases:
- TLSF
- two-level segregated fit
- TLSF allocator
area: systems/memory-allocation
level: advanced
summary: "A real-time allocator with O(1) malloc and free. Free blocks sit in a two-level grid of size classes, and two levels of bitmaps find a nonempty class with find-first-set."
solves: [online-memory-allocation]
model: word-ram
complexity:
  vars: {h: the heap size in words, j: "the second-level index, so each power-of-two range has 2^j classes"}
  time: {worst: O(1), best: O(1)}
  space: {extra: Θ(2^j lg h)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2004
  people: [Miguel Masmano, Ismael Ripoll, Alfons Crespo, Jorge Real]
  note: Masmano, Ripoll, Crespo and Real presented TLSF at the Euromicro Conference on Real-Time Systems in 2004, as an allocator with constant time bounds for real-time systems.
prereqs: [segregated-free-lists, size-classes, trailing-zero-count, boundary-tags]
see_also: [floor-log2, bitmap-allocator, buddy-system, coalescing, dlmalloc, external-fragmentation, internal-fragmentation, slab-allocator]
sources:
  - paper: "Miguel Masmano, Ismael Ripoll, Alfons Crespo and Jorge Real, TLSF, a new dynamic memory allocator for real-time systems, Proceedings of the 16th Euromicro Conference on Real-Time Systems (ECRTS 2004), Catania, Italy, 79-86"
    locator: the two-level index of free lists with its bitmaps, and the functions mapping_insert, mapping_search and find_suitable_block
  - paper: doi:10.1007/s11241-008-9052-7
    title: Miguel Masmano, Ismael Ripoll, Patricia Balbastre and Alfons Crespo, A constant-time dynamic storage allocator for real-time systems, Real-Time Systems 40(2), 2008
    locator: the worst-case analysis of the time and of the fragmentation of TLSF
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.6, Segregated free lists (segregated fits with size classes)
---

TLSF, two-level segregated fit, is a general [allocator](/allocator/) whose `malloc` and `free` take $O(1)$ time in the worst case, not only on average. It keeps free blocks in [segregated free lists](/segregated-free-lists/) indexed in two levels. The first level splits sizes by powers of two. The second level splits each power-of-two range into $2^J$ equal parts. A bitmap for each level records which lists are nonempty, so one *find-first-set* on each level finds a list whose blocks all fit. Freed blocks merge at once with free neighbors. TLSF was designed for real-time systems, where the time bound of each call matters more than the average.

## In plain words

Think of a warehouse with shelves of empty boxes. Each shelf holds boxes of one size band: one shelf for sizes 16 to 19, one for 20 to 23, and so on. Bands are narrow for small boxes and wider for large ones. On each shelf there is a lamp that is on when the shelf has a box.

To get a box for an item, go to the band just above the item's size, so that every box there is big enough. If its lamp is off, look along the lamps for the next one that is on. A row of lamps can be checked in one step, so finding a shelf never takes long. Cut the box down to size and put the spare part on its shelf. When a box comes back, join it with empty boxes next to it before you shelve it.

## The problem

The allocator solves [online memory allocation](/online-memory-allocation/) on a heap of $h$ words: `malloc(n)` returns a block of at least $n$ free words, and `free(b)` gives back a block. A real-time system needs a fixed bound on the time of each call, so that its schedule can be checked. [Sequential fits](/sequential-fit/) search a list whose length grows with the number of free blocks. A [buddy system](/buddy-system/) has a bound of $O(\lg h)$, but it rounds every request up to a power of two. TLSF aims at an $O(1)$ bound that does not depend on $h$ or on the number of blocks, with small rounding waste.

## The algorithm

**Size classes.** Fix $J \ge 0$. A size $r \ge 2^J$ has first-level index $fl = \lfloor \lg r \rfloor$, the [floor of its log](/floor-log2/). Its second-level index $sl$ is the next $J$ bits of $r$ below the highest set bit. So class $(fl, sl)$ holds the sizes from $2^{fl} + sl \cdot 2^{fl - J}$ up to, but not including, $2^{fl} + (sl + 1) \cdot 2^{fl - J}$. Every block has at least $2^J$ words, so that $fl \ge J$.

**State.** LIST$[fl][sl]$ is a doubly linked list of the free blocks in class $(fl, sl)$. Bit $sl$ of the word SL$[fl]$ is 1 when LIST$[fl][sl]$ is not empty, and bit $fl$ of the word FL is 1 when SL$[fl] \ne 0$. Each block has a header with its size, a free flag and the address of the block just before it in memory, as with [boundary tags](/boundary-tags/), so `free` finds both physical neighbors in $O(1)$ time. FLS is the index of the highest 1 bit and FFS the index of the lowest 1 bit, the [trailing zero count](/trailing-zero-count/).

```pseudo id=main
MAPPING-INSERT(r)                                ▷ the class that holds size r
L1  fl ← FLS(r); sl ← (r >> (fl − J)) − 2^J; return (fl, sl)

MAPPING-SEARCH(r)                                ▷ the first class whose sizes are all ≥ r
L2  r ← r + 2^(FLS(r) − J) − 1; return MAPPING-INSERT(r)

FIND-SUITABLE-BLOCK(fl, sl)
L3  m ← SL[fl] AND (ALL ONES << sl)              ▷ classes of row fl from sl on
L4  if m ≠ 0 then sl ← FFS(m)
L5  else m ← FL AND (ALL ONES << (fl + 1)); if m = 0 then return FAIL
L6      fl ← FFS(m); sl ← FFS(SL[fl])
L7  return the head of LIST[fl][sl]

TLSF-MALLOC(n)
L8  n ← max(n, 2^J); (fl, sl) ← MAPPING-SEARCH(n); n ← the lowest size of class (fl, sl)
    b ← FIND-SUITABLE-BLOCK(fl, sl)
L9  remove b from its list; clear the SL and FL bits if the list becomes empty
L10 if size(b) − n ≥ 2^J then split off the rest after n words and INSERT it
L11 mark b used; return b

TLSF-FREE(b)
L12 mark b free; if the block before b is free, remove it from its list and merge
L13 if the block after b is free, remove it from its list and merge
L14 INSERT(b)                                    ▷ MAPPING-INSERT, push on the list, set the bits
```

**Why round up.** Line L2 adds $2^{fl - J} - 1$, one less than the width of the classes in the row of $r$, and line L1 then cuts off the low bits. So MAPPING-SEARCH rounds $r$ up to the next class boundary. Every block in that class or in a higher class has at least $r$ words, so line L7 can take the head of the list with no search inside it. Line L8 then rounds the request up to the start of that class, as the original code does.

**Good fit, not best fit.** A free block whose size lies between $r$ and the next class boundary sits in a lower class, and the search does not look there. So `malloc` can fail while a block of size at least $r$ is free. The paper calls this policy a *good fit*. With $J = 4$ or $5$, the classes are narrow, and the loss is small.

## Example

$h = 100$ words and $J = 2$, so each row has 4 classes and the smallest block has 4 words. At the start, the whole heap is one free block of 100 words in class $(6, 2)$, which holds sizes 96 to 111.

| step | call | search class | result | free lists after the call |
|---|---|---|---|---|
| 1 | malloc(13) | (3, 3): 14 to 15 | 0, 14 words | $(6,1)$: 14 (86 words) |
| 2 | malloc(20) | (4, 1): 20 to 23 | 14 | $(6,0)$: 34 (66) |
| 3 | malloc(10) | (3, 1): 10 to 11 | 34 | $(5,3)$: 44 (56) |
| 4 | free(14) | | | $(4,1)$: 14 (20); $(5,3)$: 44 (56) |
| 5 | malloc(11) | (3, 2): 12 to 13 | 14, 12 words | $(3,0)$: 26 (8); $(5,3)$: 44 (56) |
| 6 | malloc(40) | (5, 1): 40 to 47 | 44 | $(3,0)$: 26 (8); $(4,0)$: 84 (16) |
| 7 | free(0), free(34) | | | $(3,3)$: 0 (14); $(4,0)$: 26 (18), 84 (16) |
| 8 | malloc(17) | (4, 1): 20 to 23 | FAIL | unchanged |
| 9 | malloc(16) | (4, 0): 16 to 19 | 26, 18 words | $(3,3)$: 0 (14); $(4,0)$: 84 (16) |

In step 5, SL$[3]$ has no bit at 2 or above, so line L5 looks at FL above row 3, finds row 4, and takes the block of 20 words at 14 from class $(4, 1)$. In step 7, the block at 34 merges with the free block at 26 into one block of 18 words. Step 8 shows the good fit: a block of 18 words is free, but class $(4, 0)$ is below the search class, so `malloc(17)` fails. In step 9, the rest of 2 words is less than the smallest block, so the whole block of 18 words is used.

## Correctness

The proof keeps four facts after each call: the blocks tile the heap, no two free blocks are next to each other, each free block is in the list of its class, and the bits of SL and FL are 1 exactly for the nonempty lists and rows. MAPPING-SEARCH returns the lowest class whose smallest size is at least $n$. The classes are in the order of their sizes, so FIND-SUITABLE-BLOCK returns the head of the first nonempty list at or above that class. So the block is big enough, and `malloc` fails only when no free block reaches the search class. The full proof is in the [correctness proof](proofs/correctness.md). The page's tests check all of these facts after every call of a seeded random sequence, and check the two mapping functions for every size up to 3000.

## Complexity

In the [word RAM](/word-ram/), FLS and FFS take $O(1)$ time, either as machine instructions or with a [de Bruijn table](/de-bruijn-bit-scan/). A row has $2^J$ classes, so SL$[fl]$ fits in one word when $2^J \le w$, and FL fits in one word when $\lg h < w$.

| operation | time | why |
|---|---|---|
| malloc | $O(1)$ | two mappings, at most three FFS steps, one list removal and one split |
| free | $O(1)$ | two neighbor checks, at most two removals and one insert |
| space | $\Theta(2^J \lg h)$ words | one list head per class, plus one SL word per row |

No step loops over blocks, classes or rows, so the bound does not depend on $h$ or on the number of free blocks. This is the point of TLSF. A [binary heap](/binary-heap/) or a balanced tree of free blocks gives $O(\lg n)$ only.

## Properties

- **Constant time.** Both calls have a bound that does not depend on the state, which is what schedule analysis in a real-time system needs.
- **Bounded rounding.** The rounding of line L2 adds less than $2^{fl - J} \le r / 2^J$ words, so the [internal fragmentation](/internal-fragmentation/) of a request is less than a share $2^{-J}$ of its size, plus a rest of fewer than $2^J$ words that is not split off.
- **Immediate coalescing.** No two free blocks are next to each other, which limits [external fragmentation](/external-fragmentation/).
- **Good fit.** The block that `malloc` returns is from the first nonempty class at or above the search class, close to best fit, but not always the best.

## Variants and improvements

- **Small sizes.** Real implementations treat sizes below some limit, for example 128 bytes, as one first-level row with linear classes, so that tiny blocks do not need tiny classes.
- **Choice of $J$.** A larger $J$ makes classes narrower, which lowers the rounding waste and the good-fit loss, at the cost of more list heads.
- **Several pools.** Implementations let a program add more memory areas to the same index. The 2008 paper gives a worst-case analysis of both time and fragmentation.
- **Half-fit.** An earlier allocator with constant time that keeps one level of power-of-two classes and one bitmap. It rounds more coarsely than TLSF.

## When to use it

Use TLSF in a real-time or embedded system that must allocate memory while it runs and needs a fixed bound on every call. It also suits systems without virtual memory, where external fragmentation must stay low over long runs. On a desktop or server, where the average speed and the use of many threads matter more, allocators with thread caches such as [jemalloc](/jemalloc/) are faster. For objects of a few fixed sizes, a [memory pool](/memory-pool/) or a [slab allocator](/slab-allocator/) is simpler.

## Pitfalls

- **Searching with MAPPING-INSERT.** Using the class of $n$ itself, without the rounding of line L2, can return the head of a list whose block is smaller than $n$.
- **Shifting by a negative amount.** MAPPING-INSERT needs $fl \ge J$, so sizes below $2^J$ must be rounded up, or mapped by a separate small-size rule.
- **Stale bitmaps.** Each removal that empties a list must clear its SL bit, and the FL bit when the row becomes empty. A stale bit sends the search to an empty list.
- **Expecting best fit.** TLSF can fail when a block of the right size is free in a lower class. Tests that compare it with a best-fit allocator must allow for this.

## Implementations

## History

Real-time programmers long avoided dynamic memory, because the common allocators had no useful bound on the time of a call. Segregated free lists with bitmaps were known before, and T. Ogasawara's Half-fit allocator of 1995 already gave constant time with one level of power-of-two classes. Miguel Masmano, Ismael Ripoll, Alfons Crespo and Jorge Real presented TLSF at the 16th Euromicro Conference on Real-Time Systems in 2004. Its second level of classes cut the rounding waste of Half-fit, and its tests showed low fragmentation and fast calls on real workloads. In 2008 Masmano, Ripoll, Balbastre and Crespo published a longer analysis in the journal Real-Time Systems. TLSF has since been ported to many real-time and embedded systems.

## References
