---
tag: 26G2FC
kind: technique
slug: deferred-coalescing
name: Deferred coalescing
aliases:
- lazy coalescing
- delayed coalescing
- quick lists
area: systems/memory-allocation
level: advanced
summary: "Keep freed small blocks unmerged on quick lists for reuse, and merge them with their neighbours only later, for example when a request fails."
prereqs: [coalescing]
see_also: [dlmalloc, boundary-tags, segregated-free-lists, size-classes, lazy-buddy-system, external-fragmentation, deferred-reclamation, epoch-based-reclamation]
sources:
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 2.5 (splitting and coalescing, and deferred coalescing) and Section 3.11 (quick lists and the policies for when to coalesce)
  - paper: "Charles B. Weinstock and William A. Wulf, Quick Fit: an efficient algorithm for heap storage allocation, ACM SIGPLAN Notices 23(10), 1988"
    title: Quick Fit, an efficient algorithm for heap storage allocation
    locator: the quick lists for small exact sizes in front of a general allocator
---

*Deferred coalescing* postpones the merge of freed blocks. A freed block of a common small size goes onto a *quick list* for its exact size and keeps its used tag, so no merge touches it. The next request of that size takes it back from the list in constant time, with no search, no split and no merge. Only later, when a request cannot be met or at some other chosen moment, does the allocator merge all the waiting blocks with their free neighbours in one pass. Programs often free and allocate the same few sizes again and again; immediate [coalescing](/coalescing/) would merge such a block on each free and split it again on the next malloc, and deferred coalescing skips that work. The quick lists of Weinstock and Wulf's Quick Fit and the fastbins of [dlmalloc](/dlmalloc/) work this way.

## In plain words

A restaurant clears tables after each guest leaves. If it always pushes the tables back into one long table, it must pull them apart again when the next pair of guests comes. Most guests come in pairs, so the staff leave the small tables as they are and seat the next pair at once.

Only when a large group comes and no long table is free do the staff push all the free small tables together. They do the joining work once, when it is needed, and not after every guest.

## When it applies

- The program frees and allocates blocks of a few sizes many times, so a freed block is likely to be reused at the same size soon.
- The allocator merges free neighbours, by [boundary tags](/boundary-tags/) or another way, so there is a merge to postpone.
- A quick search matters more than the lowest possible fragmentation at every moment. Blocks on the quick lists are free space that the general search cannot see.
- The allocator has a point where a full merge is cheap or necessary: a failed request, a large request, a timer or a quick list that has grown too long.

## The template

The heap model is the one of [first-fit allocation](/first-fit-allocation/), with immediate coalescing for blocks larger than a limit $Q$. For each block size $s \le Q$ there is a quick list $QUICK[s]$, a stack linked through the first payload word of each block. A block on a quick list keeps its used tag, so to every merge it looks like a live block.

```pseudo id=main
DEFERRED-FREE(h, a)
L1  if SIZE(a) ≤ Q then push a on QUICK[SIZE(a)]; return     ▷ the tag stays used
L2  COALESCE-ON-FREE(h, a)
DEFERRED-MALLOC(h, n)
L3  need ← max(MIN, n + 2)
L4  if need ≤ Q and QUICK[need] is not empty then return pop(QUICK[need]) + 1
L5  a ← FIT(h, need)
L6  if a = NIL and some quick list is not empty then
L7      CONSOLIDATE(h); a ← FIT(h, need)
L8  if a = NIL then return NIL
L9  split a or use it whole; return a + 1
CONSOLIDATE(h)
L10 for s ← MIN to Q do
L11     while QUICK[s] is not empty do COALESCE-ON-FREE(h, pop(QUICK[s]))
```

A quick hit (L4) costs $O(1)$. A free of a small block (L1) costs $O(1)$. CONSOLIDATE frees each waiting block with immediate coalescing, so its cost is the sum of those frees, and it runs only when the search has failed. Two invariants hold between operations: no two blocks with a free tag are adjacent, because only blocks larger than $Q$ and consolidated blocks get a free tag, and both go through COALESCE-ON-FREE; and every block with a used tag is either live or on exactly one quick list. After CONSOLIDATE the quick lists are empty, so no two free blocks of the heap are adjacent, the same state as under immediate coalescing. A request that fails after L7 would also fail under immediate coalescing with the same block layout, since the merge is then complete.

## Classic examples

**A quick hit.** In a heap of 64 words with $Q = 8$, malloc(2) gets the block $(0, 4)$ and malloc(10) gets $(4, 12)$. A free of the first block puts it on $QUICK[4]$; its tag stays used and the free list still holds only $(16, 48)$. The next malloc(2) pops it at once and returns the same address. A free of the second block, of 12 words, is above $Q$, so it merges at once with $(16, 48)$ into $(4, 60)$.

**Consolidation.** In a heap of 32 words, eight malloc(2) calls fill the heap with eight blocks of 4 words, and all eight are freed onto $QUICK[4]$. The free list is empty. A malloc(20) needs 22 words, so the fit search fails, CONSOLIDATE frees the eight blocks with merging into one block of 32 words, and the second search splits it.

**A random trace.** A seeded trace (seed 3) of 3000 steps, each a free of a random live block or, with equal chance, a malloc of 2, 2, 4, 6, 6 or 14 words (nine times in ten) or of 32 to 400 words (one time in ten), ran with first fit. The table compares immediate coalescing with quick lists for blocks up to $Q = 16$ words.

| heap | coalescing | failed requests | probes | merges | quick hits | consolidations |
|---|---|---|---|---|---|---|
| $2^{12}$ words | immediate | 0 | 2818 | 991 | 0 | 0 |
| $2^{12}$ words | deferred | 0 | 376 | 126 | 1317 | 0 |
| $2^{10}$ words | immediate | 31 | 3135 | 950 | 0 | 0 |
| $2^{10}$ words | deferred | 32 | 1485 | 240 | 1126 | 27 |

In the large heap, most small requests were quick hits, and the search and the merge work fell by a factor of about 7. In the small heap, the deferred version consolidated 27 times, and it failed one request more than the immediate version: the quick hits had given out blocks at other places, so the heap had a different layout when the large requests came.

## Variations

- **When to coalesce.** Wilson et al. list several policies: merge all waiting blocks when memory runs out or a request fails, merge at fixed times, or limit the length of each quick list and merge what does not fit. Their survey describes Lea's allocator of that time as merging only when a request cannot be met otherwise.
- **Fastbins in dlmalloc.** Later versions of [dlmalloc](/dlmalloc/) keep small freed chunks in *fastbins*, singly linked LIFO lists by exact size whose chunks still look in use to their neighbours. A step called consolidation frees them with merging, before a large request is served or when the allocator runs short of space.
- **Quick lists in front of segregated lists.** Quick Fit puts quick lists for small sizes in front of a general allocator. [Segregated free lists](/segregated-free-lists/) and [size classes](/size-classes/) carry the idea further and never merge blocks of different classes.
- **Lazy buddies.** The [lazy buddy system](/lazy-buddy-system/) delays the merge of buddies in the same way.
- **Thread caches.** Per-thread caches of free objects in [tcmalloc](/tcmalloc/) and [jemalloc](/jemalloc/) also delay the return of blocks to the shared heap. The main gain there is less locking, not less merging.

## Pitfalls

- **Hidden free memory.** A block on a quick list is free, but the fit search does not see it. If the allocator never consolidates, the quick lists can hold much of the heap while large requests fail. Consolidate before reporting a failure.
- **Forgetting the used tag.** If a quick block had a free tag, a neighbour's free would merge it while it is still on a quick list, and a later quick hit would hand out part of a larger free block.
- **Double free.** A second free of the same block pushes it twice on a quick list, and two later requests get the same memory. A check of the list head, as some allocators do, catches only the simplest case.
- **Worse fragmentation.** Small blocks that stay in place can split large free areas. Measure fragmentation, not only speed.
- **Not deferred reclamation.** Deferred coalescing delays the merge of memory that is already free. [Deferred reclamation](/deferred-reclamation/) in concurrent data structures, such as [epoch-based reclamation](/epoch-based-reclamation/) and [hazard pointers](/hazard-pointers/), delays the free itself until no thread can still read the block.

## Exercises

1. Show that after CONSOLIDATE the free blocks are exactly the maximal runs of words that no live block covers, which is also the state that immediate coalescing gives for the same live blocks.
2. Find a short trace on which deferred coalescing fails a request that immediate coalescing serves. Which placement choice made the two heaps differ?
3. Limit each quick list to $k$ blocks and send the rest to COALESCE-ON-FREE. How do the probes and the merges change with $k$ on a random trace?
4. Why does a quick list need only one link per block, while the main free list needs two?
5. Add a consolidation before every request larger than some size $L$. On the trace of the table, how does the number of failed requests change?

## References
