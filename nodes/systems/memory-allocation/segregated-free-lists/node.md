---
tag: 2CE79K
kind: data-structure
slug: segregated-free-lists
name: Segregated free lists
aliases:
- segregated storage
- segregated fits
- segregated free list allocator
area: systems/memory-allocation
level: core
summary: "One free list per size class. A request searches the list of its own class, then takes a block from a larger class and splits it, and a free merges with free neighbours."
implements: [allocator]
model: word-ram
complexity:
  vars: {h: the heap size in words, k: "the number of size classes, about lg h", l: the length of the list of the request's class}
  time: {malloc: O(l + k), free: O(1)}
  space: {extra: Θ(k)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [free-list, size-classes]
see_also: [sequential-fit, tlsf, buddy-system, slab-allocator, memory-pool, coalescing, boundary-tags, dlmalloc]
sources:
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: "Section 3.6, Segregated free lists: simple segregated storage, and segregated fits with exact lists, strict size classes with rounding, and size classes with range lists; Section 4.1 for Comfort (1964) and Purdom, Stigler and Cheam (1971)"
  - paper: "W. T. Comfort, Multiword list items, Communications of the ACM 7(6), 1964"
    locator: the multiple free lists, one for each block size, cited by Wilson et al. as the first segregated storage scheme
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, CRC Press, 2011
    locator: Chapter 7, Allocation (segregated fits and size classes)
---

*Segregated free lists* keep one [free list](/free-list/) for each [size class](/size-classes/) instead of one list for the whole heap. A request of $n$ words looks only at the list of its class, and if that list has no block large enough, it takes a block from the least larger class that is not empty. Because every block in a larger class is large enough, that step needs no search. Wilson et al. call allocators of this kind *segregated fits* when they split and merge blocks, and *simple segregated storage* when every block keeps its class for ever. This page gives segregated fits with classes $[2^i, 2^{i+1})$ in full, and simple segregated storage as a variant.

## In plain words

A store room keeps boxes of all sizes on one long shelf. To find a box of a given size, you walk the whole shelf. A better store room has one shelf per size range: one for small boxes, one for medium boxes, one for large boxes, and so on.

To find a box, go to the shelf of its size range and look there. If that shelf has nothing big enough, go to the next shelf that is not empty: every box on it is big enough. If the box is too big, cut off the extra part and put that part on the shelf of its own size.

When a box comes back, check its two neighbours in memory. If a neighbour is empty, join them into one bigger box, and put the result on the shelf of its new size.

## The abstract type

The data structure implements the [allocator](/allocator/) interface on a heap of $h$ words with addresses $0$ to $h - 1$:

- `malloc(n)` returns the address of $n$ free words, which become allocated, or FAIL.
- `free(p)` gives back the block that a call `malloc(n)` returned at $p$.

Blocks never move. The aim is to make the search of `malloc` short, and to keep the heap free of two free blocks side by side.

## Representation

- **Blocks.** The heap is a sequence of blocks that tile it. Each block has a size and a free bit. In a real allocator these sit in a header and, for free blocks, a footer, the [boundary tags](/boundary-tags/), so that `free` finds both neighbours in $O(1)$ time. The page's code keeps the same facts in two maps: start to size, and end to start.
- **Classes.** A free block of $s$ words belongs to class $\lfloor \lg s \rfloor$, so class $i$ holds the sizes from $2^i$ to $2^{i+1} - 1$. There are $k = \lfloor \lg h \rfloor + 1$ classes.
- **Lists.** LIST$[i]$ is a doubly linked list of the free blocks of class $i$, with the links inside the free blocks. A new free block goes to the front, so the lists are last in, first out.

## Operations

```pseudo id=main
SEG-MALLOC(n)
L1  i ← ⌊lg n⌋
L2  b ← the first block in LIST[i] with size(b) ≥ n, if any
L3  if there is none then j ← the least j > i with LIST[j] not empty; FAIL if none
L4      b ← the first block of LIST[j]                 ▷ size(b) ≥ 2^j > n
L5  remove b from its list
L6  if size(b) > n then the rest [b + n, b + size(b)) becomes a free block in its class
L7  mark b allocated with size n; return b

SEG-FREE(p)
L8  mark p free
L9  if the block after p is free then remove it from its list and merge it into p
L10 if the block before p is free then remove it from its list and merge p into it
L11 add the merged block to LIST[⌊lg size⌋]
```

Line L2 is first fit inside one class. A block of class $i$ can be smaller than $n$, because the class holds a range of sizes, so the scan must check the size. Line L3 skips the rest of class $i$ and needs no size check: a block of class $j > i$ has at least $2^j \ge 2^{i+1} > n$ words. Lines L9 and L10 are immediate [coalescing](/coalescing/), as in Knuth's boundary tag method.

## Example

The heap has 64 words. The program calls malloc(10), malloc(20), malloc(5), frees the 20-word block, calls malloc(17), and then frees all blocks. The table shows the free blocks as size at address.

| step | call | result | what happens | free blocks |
|---|---|---|---|---|
| 0 | start | | | 64 at 0 (class 6) |
| 1 | A = malloc(10) | 0 | class 3 is empty; class 6 holds 64: split, the rest 54 goes to class 5 | 54 at 10 |
| 2 | B = malloc(20) | 10 | class 4 is empty; take 54 from class 5: the rest 34 goes to class 5 | 34 at 30 |
| 3 | C = malloc(5) | 30 | class 2 is empty; take 34 from class 5: the rest 29 goes to class 4 | 29 at 35 |
| 4 | free(B) | | the neighbours A and C are allocated; 20 goes to class 4 | 20 at 10, 29 at 35 |
| 5 | D = malloc(17) | 10 | class 4 holds 20 (newest) and 29; first fit takes 20; the rest 3 goes to class 1 | 3 at 27, 29 at 35 |
| 6 | free(C) | | merge with 29 at 35 on the right and with 3 at 27 on the left | 37 at 27 (class 5) |
| 7 | free(A) | | the right neighbour D is allocated | 10 at 0, 37 at 27 |
| 8 | free(D) | | merge with both neighbours | 64 at 0 |

At step 5 both blocks of class 4 are large enough, and the LIFO order picks the newest. An address-ordered list would also pick 20 at 10. At step 1 the request of 10 words takes the whole heap and splits it, because classes 3, 4 and 5 are empty.

## Correctness

A state is legal when (T) the blocks tile the heap, (C) no two free blocks are neighbours, and (L) the lists hold exactly the free blocks, each in the list of class $\lfloor \lg \text{size} \rfloor$. The key fact is that a free block of size at least $n$ has a class $c \ge \lfloor \lg n \rfloor$. If $c = i$, line L2 finds some fitting block in class $i$. If not, every block of the least non-empty class above $i$ fits. So `malloc(n)` fails only when no free block has $n$ words, and the block it returns comes from the least class that holds a fitting block. Splits and merges keep (T), (C) and (L), and when all blocks are freed, (C) leaves one free block, the whole heap. The full proof is in the [correctness proof](proofs/correctness.md).

## Complexity

In the [word RAM](/word-ram/), with doubly linked lists and boundary tags:

| operation | time | why |
|---|---|---|
| malloc | $O(l + k)$ | line L2 scans the $l$ blocks of class $i$, and line L3 checks at most $k$ list heads |
| malloc with a class bitmap | $O(l)$ | one word with a bit per non-empty class gives $j$ by a [trailing zero count](/trailing-zero-count/) |
| free | $O(1)$ | two neighbour checks, at most two list removals and one insertion |

Here $k = \lfloor \lg h \rfloor + 1$, so $k \le 64$ on a 64-bit machine, and the list heads take $\Theta(k)$ words. The scan of line L2 is the only part that depends on the number of free blocks, and it covers only one class. [TLSF](/tlsf/) removes it: it uses finer classes and rounds the request up to the next class, so that any block of the found class fits.

**Fit quality.** With power-of-two range classes, a block found at line L3 has at least twice the request, but the split gives the rest back, so the allocated block has exactly $n$ words. The cost of the coarse classes is in the search, not in [internal fragmentation](/internal-fragmentation/). Wilson et al. note that with closely spaced classes, a class often holds only one or two popular sizes, so segregated fits can approximate best fit very closely.

## Variants

- **Simple segregated storage.** The heap is cut into pages, and each page is cut into slots of one class only. A request takes a slot of its class, with no split and no merge, and a freed slot goes back to the list of its class. All calls take $O(1)$ time, but a request is rounded up to its class, and free slots of one class never serve another. The page's code includes this scheme. The [slab allocator](/slab-allocator/) and [memory pools](/memory-pool/) are refinements of it.
- **Exact lists.** One list per exact size for small sizes, and range lists only for large sizes. Many general-purpose allocators, such as [dlmalloc](/dlmalloc/), use exact lists for small blocks.
- **Strict size classes with rounding.** Round each request up to its class, so that all blocks in a list have the same size and the scan of line L2 takes one step. This trades internal fragmentation for speed.
- **Finer classes.** Split each power-of-two range into several classes, as in [TLSF](/tlsf/), to shorten the scan.
- **Deferred coalescing.** Keep freed blocks of popular sizes on quick lists without merging, as in [deferred coalescing](/deferred-coalescing/).

## When to use it

Use segregated fits for a general-purpose allocator that must serve many sizes with low fragmentation and short searches. It is the basis of most production allocators. Use simple segregated storage when the program allocates many objects of a few sizes and speed matters more than memory. When the time of each call must have a fixed bound, as in real-time systems, use [TLSF](/tlsf/) or a [buddy system](/buddy-system/), because the scan of line L2 has no constant bound.

## Pitfalls

- **Taking any block of the request's own class.** A block in class $\lfloor \lg n \rfloor$ can be smaller than $n$, so line L2 must check the size. Only the blocks of larger classes fit without a check.
- **Forgetting to move a merged block.** After a merge, the size changes and so can the class. The merged block must go to the list of its new class (line L11), and both old blocks must leave their lists first.
- **Losing the rest of a split.** If the rest at line L6 is too small to hold the header and the links of a free block, a real allocator must allocate the whole block instead. The page's code works in words with no headers, so it splits down to 1 word.
- **Mixing up the two schemes.** Simple segregated storage never merges, so it cannot give the memory of one class to another. Programs whose sizes change phase can then run out of memory while many free slots exist in other classes.

## Implementations

## History

Wilson et al. trace segregated storage back to Comfort (1964), who kept several free lists, one for each block size. The binary buddy system of Knowlton (1965) is a segregated scheme with a strict rule for splits and merges. According to Wilson et al., an efficient segregated fits scheme with general coalescing by boundary tags was described in 1971 by Purdom, Stigler and Cheam, but it did not become well known. Wilson, Johnstone, Neely and Boles (1995) gave the names *simple segregated storage* and *segregated fits*, and sorted segregated fits into exact lists, strict size classes with rounding, and size classes with range lists. Most modern allocators, from dlmalloc to [TLSF](/tlsf/) and the allocators with thread caches, use some form of segregated lists.

## References
