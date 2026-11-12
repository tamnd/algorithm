---
tag: CY94WX
kind: technique
slug: sequential-fit
name: Sequential fit
aliases:
- sequential fit family
- sequential fit policies
area: systems/memory-allocation
level: intro
summary: "Allocate by one scan of a single free list. The start point, the preferred fit and the stop rule give first, next, best and worst fit."
prereqs: [free-list, external-fragmentation]
see_also: [first-fit-allocation, next-fit-allocation, best-fit-allocation, worst-fit, coalescing, segregated-free-lists, buddy-system, knuth-fifty-percent-rule]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, Fundamental Algorithms, third edition
    locator: Section 2.5, Dynamic storage allocation, Algorithm A (first fit), the best-fit method, and the exercises on the roving pointer
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 1.3 (strategy, policy and mechanism), Section 3.4 (sequential fits) and Section 3.5 (list order, splitting and worst fit)
  - paper: doi:10.1145/286860.286864
    title: Mark S. Johnstone and Paul R. Wilson, The memory fragmentation problem, solved?, ISMM 1998, 26-36
    locator: Section 2.1 (sequential fit algorithms with LIFO, FIFO and address-ordered lists) and the fragmentation results for each policy
---

*Sequential fit* is the family of allocation policies that keep all free blocks on one [free list](/free-list/) and serve each request by one scan of that list. The members differ only in three choices: where the scan starts, which fitting block it prefers, and when it may stop. [First fit](/first-fit-allocation/) takes the first fitting block; [next fit](/next-fit-allocation/) does the same from a roving pointer; [best fit](/best-fit-allocation/) takes the smallest fitting block; [worst fit](/worst-fit/) takes the largest. All of them split the chosen block and merge freed blocks with their neighbours in the same way. Wilson, Johnstone, Neely and Boles separate the *policy* (which block to choose) from the *mechanism* (the data structure that finds it), and this page follows that split: the same policies can run on a list, a tree or segregated lists.

## In plain words

You keep a list of all the empty spaces. When a request comes, you walk along the list and look at each space. The rules of the walk make the policy. Do you start at the front or where you stopped last time? Do you take the first space that fits, the tightest one or the widest one? Can you stop early, or must you see every space?

Change one rule and you get a different allocator, with a different speed and a different amount of waste.

## When it applies

- The heap is one range of memory, and the requests have many different sizes, so one block size does not fit all.
- Blocks cannot move after allocation, so the allocator must choose well at the time of the request. This is [online memory allocation](/online-memory-allocation/).
- The free list is short, or the scan can be replaced by an index. A plain scan costs time in proportion to the number of free blocks $F$.
- The allocator can afford a header and a footer per block, for [boundary tags](/boundary-tags/) and immediate [coalescing](/coalescing/).

## The template

The heap model is the one of [first-fit allocation](/first-fit-allocation/). A policy $P$ gives three things: a flag *from_rover*, a test $better(s, t)$ that says when a fitting block of size $s$ is preferred to the current choice of size $t$, and a test $stop(s, need)$ that says when no later block can be better.

```pseudo id=main
SEQUENTIAL-FIT(h, need, P)                 ▷ return a free block, or NIL
L1  start ← h.rover if P.from_rover and h.rover ≠ NIL else h.head
L2  if start = NIL then return NIL
L3  best ← NIL; a ← start
L4  loop: if SIZE(a) ≥ need and (best = NIL or P.better(SIZE(a), SIZE(best))) then
L5          best ← a
L6          if P.stop(SIZE(a), need) then break
L7      a ← NEXT(a)
L8      if a = NIL and P.from_rover then a ← h.head
L9      if a = NIL or a = start then break
L10 if P.from_rover and best ≠ NIL then h.rover ← best
L11 return best
```

The four classic policies:

| policy | from_rover | better(s, t) | stop(s, need) |
|---|---|---|---|
| first fit | no | never | always |
| next fit | yes | never | always |
| best fit | no | $s < t$ | $s = need$ |
| worst fit | no | $s > t$ | never |

After the search, the caller splits the block if the remainder has at least $MIN$ words and links the remainder in the place of the block. On free, it merges the block with its free neighbours and links the result.

The template is correct for any policy: the loop visits each list block at most once, in list order from the start (as a circle when it uses the rover), and $best$ is always a fitting block or NIL. The first fitting block that the loop meets sets $best$, so NIL comes back only when no block on the list fits.

## Classic examples

On the heap with free blocks $(0, 12), (16, 8), (28, 16), (48, 16)$, written as (start, size), one malloc(6) needs 8 words. First fit splits $(0, 12)$ after 1 probe. Next fit, with the rover at 28, splits $(28, 16)$ after 1 probe. Best fit uses all of $(16, 8)$, an exact fit, after 2 probes. Worst fit splits $(28, 16)$, the first of the two largest blocks, after 4 probes.

On a seeded random trace (a heap of $2^{14}$ words, seed 3, 1501 requests of 1 to 64 words, frees of random live blocks), the four policies gave these numbers:

| policy | free blocks on average | probes | largest free block at the end |
|---|---|---|---|
| first fit | 9.2 | 7527 | 13246 |
| next fit | 11.9 | 1642 | 7095 |
| best fit | 7.3 | 10345 | 13313 |
| worst fit | 12.0 | 17974 | 3151 |

The total free space at the end was about 14140 words for each policy. The order of these numbers agrees with the trace studies that Wilson et al. and Johnstone and Wilson report: best fit and address-ordered first fit fragment least, next fit more, and worst fit most. Random traces are a weak model of real programs, so read the table as an example, not as a measurement of real allocators.

## Variations

- **The order of the list.** Address order, LIFO order (push freed blocks at the head) and FIFO order (append them at the tail) are three different policies for the same rule. Wilson et al. report that address-ordered first fit can fragment much less than LIFO-ordered first fit, and that FIFO order may work about as well as address order.
- **The splitting threshold.** Do not split if the remainder would be smaller than a threshold. Knuth's step A4' does this.
- **Indexed fits.** Replace the scan by a structure that finds the same block faster: a size-ordered [balanced search tree](/balanced-binary-search-tree/) for best fit, or a [Cartesian tree](/cartesian-tree/) for address-ordered first fit.
- **Segregated fits.** Keep one list per size range and scan only the lists that can fit, as in [segregated free lists](/segregated-free-lists/). This approximates best fit.
- **Other families.** The [buddy system](/buddy-system/) and [size classes](/size-classes/) restrict the block sizes, so the search becomes a table lookup at the cost of more [internal fragmentation](/internal-fragmentation/).

## Pitfalls

- **Treating the list order as a detail.** The order changes which block a policy picks. State it with the policy.
- **Comparing policies on random traces only.** Random sizes and random lifetimes miss the phases and size patterns of real programs, and can rank policies wrongly.
- **Ignoring the search cost.** A linear scan grows with the number of free blocks. Measure probes, not only fragmentation.
- **Forgetting the rover rules.** A next-fit rover must stay on the list when its block is split, used whole or merged.
- **Mixing policy and mechanism.** A segregated-list allocator can be a best-fit policy, and a tree can be a first-fit policy. Name both.

## Exercises

1. Write $better$ and $stop$ for "best fit, but stop at the first block that wastes at most 2 words". Is the result still best fit?
2. Show that first fit on a LIFO-ordered list can pick a block of higher address than first fit on an address-ordered list, with a heap of three free blocks.
3. Find a short trace on which first fit fails and best fit succeeds, and another on which best fit fails and first fit succeeds.
4. Explain why worst fit can never stop its scan early, and why best fit can stop at an exact fit.
5. Run the template on the trace of the table with a LIFO list for each policy, and compare the free blocks on average with the address-ordered list.

## References
