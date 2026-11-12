---
tag: QY9E0Z
kind: technique
slug: boundary-tags
name: Boundary tags
aliases:
- boundary tag method
- boundary-tag coalescing
- block header and footer tags
area: systems/memory-allocation
level: core
summary: "Keep the size and the used bit of each block in its first and last word, so free finds both neighbours and merges them in constant time."
prereqs: [coalescing, doubly-linked-list]
see_also: [free-list, first-fit-allocation, deferred-coalescing, internal-fragmentation, dlmalloc, tlsf, buddy-system, allocator]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, Algorithm C (liberation with boundary tags) and the comparison with Algorithm B
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.2 (boundary tags, their cost per block, and the optimization that keeps the footer only in free blocks)
---

*Boundary tags* put the size of a block and a used bit at both of its ends: a *header* in the first word and a *footer* in the last word. When the program frees a block at address $a$, the allocator reads the header at the end of the block to find the block above, and the footer in word $a - 1$ to find the block below. So it can merge the freed block with both free neighbours in constant time, without a search of the heap or of the free list. Knuth describes the method as Algorithm C in *The Art of Computer Programming*, and dates it to his own work of 1962. The cost is one or two words in every block. Many general-purpose allocators that coalesce, such as [dlmalloc](/dlmalloc/), use boundary tags or a variant of them.

## In plain words

Picture a row of boxes of different widths, pushed tight against each other. Each box has a label on its left side and the same label on its right side. The label says how wide the box is and whether it is full.

When you empty a box, you look at the label on the left side of the box to its right, and at the label on the right side of the box to its left. In two looks you know if your neighbours are empty and how wide they are, so you can join the empty boxes into one. Without the right-hand labels, you would have to walk from the start of the row to find out where the box on your left begins.

## When it applies

- An allocator keeps blocks of many sizes in one range of memory and merges free neighbours, by [coalescing](/coalescing/).
- The free list is not in address order, or it is long, so the insertion scan cannot find the neighbours cheaply. Knuth's Algorithm B finds them during a scan of an address-ordered list; boundary tags remove that scan.
- Each block can afford one or two extra words. For very small objects of one size, a [slab allocator](/slab-allocator/) or a pool with no tags is cheaper.
- The free list is a [doubly linked list](/doubly-linked-list/), so a neighbour found by its tag can be removed from the list in $O(1)$.

## The template

The heap model is the one of [first-fit allocation](/first-fit-allocation/). A block at $a$ with $s$ words has the tag $2s + u$ in $mem[a]$ and in $mem[a + s - 1]$, with $u = 1$ when it is used. The block above starts at $a + s$. The block below ends at $a - 1$, so its footer is in $mem[a - 1]$, and its start is $a$ minus the size in that footer.

```pseudo id=main
BOUNDARY-TAG-FREE(h, a)                    ▷ a is the block that the program frees
L1  start ← a; end ← a + SIZE(a)
L2  if end < h.H and the header at end says free then
L3      unlink the block at end; end ← end + SIZE(end)
L4  if start > 0 then t ← mem[start − 1]      ▷ the footer of the block below
L5      if t says free then b ← start − SIZE(t)
L6          unlink b; start ← b
L7  write the tag of (start, end − start, free) in mem[start] and mem[end − 1]
L8  link start
LOWER-BY-SCAN(h, a)                        ▷ the same step without footers
L9  b ← 0
L10 while b + SIZE(b) < a do b ← b + SIZE(b)
L11 return b if b is free, else NIL
```

BOUNDARY-TAG-FREE reads at most three tag words: the header of the freed block, the header above and the footer below. With a doubly linked free list, each unlink is $O(1)$, so the whole free is $O(1)$ apart from the link step, which is $O(1)$ for a LIFO or FIFO list. LOWER-BY-SCAN gives the same block but reads one header for each block below $a$, which is $O(B)$ for $B$ blocks in the heap.

The footer is right for a simple reason. Every write of a tag writes the header and the footer together (L7, and the same rule in malloc when it splits). So between operations each block has equal tags at both ends, and the word just before a block is always the footer of the block below it.

## Classic examples

**One free on a small heap.** In a heap of 64 words, mallocs of 10, 2, 6, 2, 14 and 2 words fill the heap from address 0, and freeing the first, third and fifth block leaves the free blocks $(0, 12), (16, 8), (28, 16), (48, 16)$, written as (start, size). Now free the block at 24 with 4 words. The header at 28 says free, so the block grows to $[24, 44)$. The footer at word 23 says free with size 8, so the block below starts at $24 - 8 = 16$, and the result is one free block $(16, 28)$. That took 3 tag reads. LOWER-BY-SCAN finds the same block at 16 after it reads the headers at 0, 12 and 16, so the free reads 5 tag words.

**A random trace.** On a seeded trace (seed 3) of 3000 steps in a heap of $2^{14}$ words, each step a first-fit malloc of 1 to 64 words, or with chance 0.45 a free of a random live block, there were 1373 frees and the heap held 328 blocks at the end. The two versions built the same heap word for word. With footers, the frees read 4092 tag words in all, at most 3 per free. With the scan, they read 97573, and the cost of each free grew with the number of blocks below it.

**Knuth's Algorithms B and C.** Algorithm B keeps the free list in address order and finds both neighbours while it walks the list to insert the freed block; it needs no footers but its time grows with the list. Algorithm C uses boundary tags and a doubly linked list, so its time does not depend on the list.

## Variations

- **Footer only in free blocks.** A used block does not need a footer, because only a free block below can take part in a merge. Keep a bit in each header that says whether the block *below* is used. The footer is then needed only when the block below is free, and its space can be payload while the block is used. Wilson et al. credit this optimization to Standish; [dlmalloc](/dlmalloc/) uses a form of it.
- **A pointer instead of a size.** Some allocators store a pointer to the physical neighbour in place of the size in the footer. [TLSF](/tlsf/) keeps a pointer to the block below in each block header.
- **Sentinels.** Put a small used block at each end of the heap, so that L2 and L4 do not need the tests $end < H$ and $start > 0$.
- **Tags in a separate table.** A bitmap of the start words of the blocks can give the neighbours with no words inside the blocks, as in a [bitmap allocator](/bitmap-allocator/).
- **No tags for power-of-two blocks.** The [buddy system](/buddy-system/) finds the only block a block may merge with from its address alone, so it needs only a used bit and a size class.

## Pitfalls

- **Writing only one end.** If a split or a merge updates the header but not the footer, the next free reads a stale size below it and corrupts the heap. Write both tags in the same step.
- **Trusting a footer of a used block.** With the footer-only-in-free-blocks variation, the word before a block is payload when the block below is used. Read the used bit first, then the footer.
- **Heap ends.** Without sentinels, a free of the first block must not read $mem[-1]$, and a free of the last block must not read $mem[H]$.
- **Alignment.** The header shifts the payload by one word. If payloads must be aligned to two words, the header size and the block sizes must keep that alignment.
- **Small objects.** Two tag words on a block of two payload words double its size. This is [internal fragmentation](/internal-fragmentation/) of a kind that size classes avoid.

## Exercises

1. Show that, with the template, the word just before any block is the footer of the block below, after any sequence of malloc and free.
2. Change the template so that used blocks have no footer, using a bit in the header that says whether the block below is used. Which writes does malloc need now?
3. Give a sequence of frees on which LOWER-BY-SCAN reads a number of headers that grows with the square of the number of blocks.
4. Why does BOUNDARY-TAG-FREE need a doubly linked free list? What goes wrong with a singly linked list?
5. Add sentinel blocks at both ends of the heap and remove the tests $end < h.H$ and $start > 0$. What is the smallest size of a sentinel?

## References
