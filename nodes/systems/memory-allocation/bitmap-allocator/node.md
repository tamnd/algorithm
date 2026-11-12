---
tag: GDECRB
kind: data-structure
slug: bitmap-allocator
name: Bitmap allocator
aliases:
- bitmap allocation
- free-space bitmap
- bitmapped fits
area: systems/memory-allocation
level: intro
summary: "Track each unit of memory with one bit, 1 for used. First fit scans the bitmap a word at a time, with bit tricks to find n free units in a row."
implements: [allocator]
model: word-ram
complexity:
  vars: {h: the number of units, w: the word size, n: the request in units}
  time: {malloc: O((h/w) lg w), free: O(n/w + 1)}
  space: {extra: Θ(h/w)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [bit-set, first-fit-allocation]
see_also: [bit-vector, trailing-zero-count, leading-zero-count, segregated-free-lists, memory-pool, buddy-system, tlsf, internal-fragmentation]
sources:
  - paper: doi:10.1007/3-540-60368-9_19
    title: Paul R. Wilson, Mark S. Johnstone, Michael Neely and David Boles, Dynamic storage allocation, a survey and critical review, IWMM 1995, LNCS 986, 1-116
    locator: Section 3.9, Bitmapped fits (one bit per word of the heap, two bitmaps for boundaries and use, and byte scans with a 256-way table)
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley, 2013
    locator: Chapter 6, Searching words (find the first string of 1 bits of a given length)
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition, Wiley, 2018
    locator: Chapter 14, File-system implementation, free-space management with a bit vector
---

A bitmap allocator divides memory into $h$ units of equal size and keeps one bit per unit: 1 when the unit is in use, 0 when it is free. To allocate $n$ units, it looks for $n$ zero bits in a row and sets them. To free a block, it clears its bits. A second bitmap marks the first unit of each block, so a block needs no header. The scan reads whole words of $w$ bits, so a search over $h$ units takes about $h/w$ word steps instead of $h$. Bitmaps manage disk blocks in file systems, physical pages in kernels, and small objects in some garbage-collected heaps.

## In plain words

Picture a row of parking spaces with a light above each one: on when the space is taken, off when it is free. To park a bus that needs five spaces, look along the row for five dark lights in a row, and turn them on.

A computer can look at 64 lights at once, because a machine word holds 64 bits. So the search skips a whole group of busy spaces in one step. Inside a group, a few bit steps find a free run without looking at each space. A run can also start at the end of one group and go on into the next, so the search remembers how many free spaces it saw at the end of the last group.

To free the bus, turn its lights off. A second row of lights marks where each vehicle starts, so you know where the bus ends.

## The abstract type

The bitmap allocator implements the [allocator](/allocator/) interface on $h$ units with addresses $0$ to $h - 1$:

- `malloc(n)` returns the address of $n$ free units in a row, which become used, or FAIL;
- `free(p)` frees the block that a `malloc` returned at $p$.

The allocator on this page uses the [first fit](/first-fit-allocation/) policy: it returns the lowest address where $n$ free units start. The unit is a fixed size, for example 16 bytes in a heap, a 4 KB page in a kernel or a disk block in a file system, so a request in bytes is rounded up to whole units.

## Representation

- **USED** is a [bit vector](/bit-vector/) of $h$ bits in $\lceil h/w \rceil$ words. Bit $x$ is 1 when unit $x$ is in use. Bits past $h$ in the last word are set to 1, so that no search returns them.
- **START** is a second bit vector of $h$ bits. Bit $x$ is 1 when unit $x$ is the first unit of an allocated block. This is the boundary bitmap of the *bitmapped fits* that Wilson et al. describe. It lets `free(p)` find the end of the block: the block ends at the first unit after $p$ that is free or starts another block.

Both maps together take $2h$ bits. With units of 16 bytes, that is $2/128$ of the memory, about 1.6 percent.

## Operations

$f$ is the *free mask* of a word, the complement of its USED word, so its 1 bits are free units. TZ and LZ are the [trailing zero count](/trailing-zero-count/) and the [leading zero count](/leading-zero-count/) of a $w$-bit word, with TZ$(0) = $ LZ$(0) = w$.

```pseudo id=main
BITMAP-MALLOC(n)
L1  run ← 0                                 ▷ free units at the top of the words seen so far
L2  for i ← 0 to ⌈h/w⌉ − 1 do
L3      f ← NOT USED[i]
L4      if run > 0 and run + TZ(NOT f) ≥ n then return MARK(w·i − run, n)
L5      if n ≤ w then r ← RUN-OF-ONES(f, n)
L6          if r ≠ 0 then return MARK(w·i + TZ(r), n)
L7      if f = all ones then run ← run + w else run ← LZ(NOT f)
L8  return FAIL

BITMAP-FREE(p)
L9  clear START[p]; q ← the first unit after p with START = 1 or USED = 0
L10 clear the USED bits p to q − 1, a word at a time

RUN-OF-ONES(f, n)                            ▷ bit j of the result: bits j to j+n−1 of f are all 1
    r ← f; m ← n − 1; s ← 1
    while m > 0 do t ← min(s, m); r ← r AND (r >> t); m ← m − t; s ← 2s
    return r
```

MARK$(a, n)$ sets the USED bits $a$ to $a + n - 1$ a word at a time, sets START$[a]$, and returns $a$.

**Why RUN-OF-ONES works.** After shifts that add up to $k$, bit $j$ of $r$ is the AND of the bits $j$ to $j + k$ of $f$. The step $r \leftarrow r \text{ AND } (r \gg t)$ with $t \le k + 1$ joins the windows $[j, j+k]$ and $[j+t, j+t+k]$, which touch or overlap, into $[j, j + t + k]$. The shifts $1, 2, 4, \ldots$ keep $t \le k + 1$, so after $\lceil \lg n \rceil$ steps the windows have length $n$. Zeros shift in from the top, so a window that would pass the end of the word gives 0. Warren's *Hacker's Delight* gives this method for finding the first string of 1 bits of a given length.

**Order of the checks.** A run that crosses into word $i$ from the words before it starts earlier than any run that starts inside word $i$, so line L4 comes before line L5. Inside the word, TZ$(r)$ is the lowest start. So the scan returns the lowest possible address, which is first fit.

## Example

$h = 200$ units in four words of 64 bits; the 56 units from 200 to 255 are padding and count as used.

| step | call | result | what the scan does |
|---|---|---|---|
| 1 | malloc(60) | 0 | word 0 is all free: RUN-OF-ONES finds bit 0 |
| 2 | malloc(10) | 60 | word 0 has free units 60 to 63 only: no run of 10 inside, run = 4; word 1 is all free: $4 + 64 \ge 10$, so the block starts at $64 - 4 = 60$ |
| 3 | malloc(100) | 70 | word 0 is full, run = 0; word 1 has units 70 to 127 free: $n > w$, run = 58; word 2 is all free: $58 + 64 \ge 100$, start $128 - 58 = 70$ |
| 4 | free(60) | | the block ends at unit 70, where START is 1: clear 60 to 69 |
| 5 | malloc(5) | 60 | first fit takes the lowest hole, 60 to 69 |
| 6 | malloc(40) | FAIL | the free runs are 65 to 69 (5 units) and 170 to 199 (30 units) |
| 7 | malloc(30) | 170 | the run from 170 stops at the padding, but it has 30 units |

Step 6 is [external fragmentation](/external-fragmentation/): 35 units are free, but no 40 of them lie in a row. After freeing all four blocks, malloc(200) returns 0. The page's code checks every call of a seeded random sequence against a plain scan of one boolean per unit.

## Correctness

The proof shows that after each call the USED bits are exactly the units of the allocated blocks, plus the padding, and that the START bits are exactly their first units. Then BITMAP-MALLOC returns the lowest $a$ such that units $a$ to $a + n - 1$ are free: the variable *run* is always the number of free units just below word $i$, so line L4 finds every run that crosses into word $i$, and line L6 finds every run inside word $i$. BITMAP-FREE finds the end of the block, because the block's units are used and the unit after it is free, padding or the start of another block. The full proof is in the [correctness proof](proofs/correctness.md).

## Complexity

In the [word RAM](/word-ram/) with words of $w$ bits, TZ and LZ take $O(1)$ time, either as machine instructions or with a [de Bruijn table](/de-bruijn-bit-scan/).

| operation | time | why |
|---|---|---|
| malloc | $O((h/w) \lg w)$ | $\lceil h/w \rceil$ words, each with $O(1)$ steps plus RUN-OF-ONES in at most $\lceil \lg \min(n, w) \rceil$ steps, and MARK in $O(n/w + 1)$ |
| free | $O(n/w + 1)$ | the scan for the end and the clear go a word at a time |
| space | $\Theta(h/w)$ words | two bits per unit |

A unit-by-unit scan would take $\Theta(h)$ steps. With $w = 64$, the word scan is up to 64 times faster when most words are full or empty. The search is still linear in $h$, so large heaps add a summary level: one bit per word that is wholly used, or a count of free units per group, which lets the scan skip groups.

## Variants

- **Single-unit bitmaps.** When every request is one unit, as for physical pages or disk blocks, `malloc` is a search for the first word that is not all ones and a TZ of its complement. No START bitmap is needed.
- **Hierarchical bitmaps.** A second level holds one bit per word of the first level, set when that word has a free unit. Then a one-unit search takes $O(\log_w h)$ word steps.
- **Next fit.** Start each scan where the last one stopped, to spread blocks and to avoid scanning the full prefix again.
- **Bitmaps in garbage collectors.** Mark bits and allocation bits of a heap are bitmaps too. A sweep can turn the mark bitmap into free runs; see [mark and sweep](/mark-and-sweep/).

## When to use it

Use a bitmap when the units are small and fixed and the metadata must be tiny and kept apart from the memory it describes, for example because the memory is on disk, or on a device, or must not be touched until it is used. File systems such as ext2 and its successors keep block and inode bitmaps. Kernels use bitmaps for page frames and for ID numbers. Bitmaps are also easy to save, to check and to compare. For a heap with many different sizes, [segregated free lists](/segregated-free-lists/) or [TLSF](/tlsf/) give faster searches.

## Pitfalls

- **Forgetting the padding.** The bits past $h$ in the last word must be set to 1. Otherwise the scan can return a block that runs past the end of the memory.
- **Missing a run that crosses a word.** Checking each word alone misses free runs that span two or more words. Keep the count of free units at the top of the words before.
- **Shifting too far in RUN-OF-ONES.** If a step shifts by more than the window length plus 1, the AND can join two windows with a gap, and report a run that has a used unit in it.
- **Finding the end without START.** With only USED, two adjacent blocks look like one, and `free` clears both. Keep the START bitmap, or store the size somewhere else.
- **Units that are too large.** Rounding requests up to whole units is [internal fragmentation](/internal-fragmentation/). Units that are too small make the bitmaps large and the scans long.

## Implementations

## History

Bitmaps for free space are an old idea in file systems and in kernels, where a disk or the physical memory is cut into blocks of one size. Wilson et al. (1995) call bitmap allocators for heaps *bitmapped fits*. They wrote that, to their knowledge, bitmaps had never been used in a conventional heap allocator, though they were common in file systems and in mark-sweep collectors such as the conservative collector of Boehm and others. They suspected the reason was that bitmaps were thought too slow, proposed fast scans with a 256-way lookup table per byte, and noted that the obvious scheme needs two bitmaps, one for block boundaries and one for use. Word-level search with trailing and leading zero counts, and the shift-and-AND search for runs of 1 bits, are standard techniques of bit manipulation, collected in Warren's *Hacker's Delight*.

## References
