---
tag: Q5H7VX
kind: data-structure
slug: set-associative-cache
name: Set-associative cache
aliases:
- n-way set-associative cache
- W-way set-associative cache
- set associative mapping
area: systems/caching-policies
level: intro
summary: "A cache split into S sets of W ways: the address bits pick one set, the tag names the block, and replacement acts inside the set. W = 1 is direct mapped, S = 1 is fully associative."
implements: [cache]
model: word-ram
complexity:
  vars: {S: the number of sets, W: the number of ways in a set}
  time: {worst: O(W)}
  space: {extra: Θ(S W)}
prereqs: [cache, lru, bit-manipulation]
see_also: [three-cs-model, plru-replacement, random-replacement, fifo-replacement, hash-table, multilevel-caching, cache-hit-ratio, memory-hierarchy]
sources:
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: "Appendix B, Section B.1 (block placement: direct mapped, set associative, fully associative; block identification by tag, index and offset; replacement by random, LRU and FIFO)"
  - paper: doi:10.1145/356887.356892
    title: "Alan Jay Smith, Cache memories, ACM Computing Surveys 14(3) (1982), 473-530"
    locator: the sections on placement (set associative mapping and the effect of set size) and on the replacement algorithm
  - paper: doi:10.1109/12.40842
    title: "Mark D. Hill and Alan Jay Smith, Evaluating associativity in CPU caches, IEEE Transactions on Computers 38(12) (1989), 1612-1630"
    locator: the miss ratio as a function of associativity, and conflict misses measured against a fully associative cache of the same size
---

A set-associative cache is a [cache](/cache/) of $S \cdot W$ blocks arranged as $S$ sets of $W$ ways. A few bits of the address, the index, choose one set, and the block may go in any of the $W$ ways of that set; the rest of the address, the tag, is stored with the block to name it. A lookup compares the tag with only $W$ stored tags, and a miss evicts a block of the same set by [LRU](/lru/), a pseudo-LRU tree or a random choice. With $W = 1$ it is a direct-mapped cache, and with $S = 1$ it is a fully associative cache.

## In plain words

Think of a coat check with 64 hooks. If any coat can go on any hook, you must look at all 64 hooks to find a coat. If the hook is fixed by the last digit of the ticket, you look at one hook, but two guests with the same last digit push each other's coats out, even when other hooks are free.

A set-associative cache is the middle way. The hooks are in small groups, say 16 groups of 4. The ticket picks the group, and the coat may hang on any of the 4 hooks there. You look at 4 hooks, not 64, and two coats with the same group number can both stay. Only when a fifth coat comes to a full group does one of the 4 have to go, usually the one used least recently.

## The abstract type

The type is a [cache](/cache/) of blocks. A block is $B$ bytes of memory that start at a multiple of $B$, and the cache holds copies of at most $S \cdot W$ blocks. One operation, ACCESS$(a)$, reads the byte at address $a$: it reports a hit if the block of $a$ is in the cache, and otherwise it loads the block, which may evict another block. The cache is part of a [memory hierarchy](/memory-hierarchy/), so the rest of the system sees only speed, not a change of the data. The set-associative design limits where each block can be stored, and so it limits which block a miss can evict.

## Representation

Let $B = 2^b$ and $S = 2^s$. An address of $t$ bits is read as three fields:

| field | bits | meaning |
|---|---|---|
| tag | the top $t - s - b$ bits | which block of those that share the set |
| index | the next $s$ bits | the set |
| offset | the low $b$ bits | the byte in the block |

So the block number is $\beta = \lfloor a / B \rfloor$, the set is $\beta \bmod S$, and the tag is $\lfloor \beta / S \rfloor$. With [bit operations](/bit-manipulation/) these are a mask and two shifts. Each of the $S \cdot W$ ways holds a valid bit, a tag and the $B$ bytes of data. Each set also holds the state of its replacement policy: an age order for LRU, $W - 1$ bits for tree pseudo-LRU, or nothing for random.

The two ends of the range are the classic designs. A *direct-mapped* cache ($W = 1$) needs one comparator and no replacement state, but blocks whose numbers agree mod $S$ always evict each other. A *fully associative* cache ($S = 1$) has no index bits; any block can go anywhere, at the cost of $S \cdot W$ comparators and a policy over the whole cache.

## Operations

```pseudo id=main
ACCESS(a)                                   ▷ returns hit or miss
L1  offset ← a mod B; s ← ⌊a / B⌋ mod S; tag ← ⌊a / (B·S)⌋
L2  line ← the W ways of set s
L3  for w ← 0 to W − 1 do                   ▷ in hardware, W comparisons at once
L4      if line[w] is valid and holds tag then
L5          UPDATE(s, w)                     ▷ record the use for the policy
L6          return hit
L7  w ← VICTIM(s)                           ▷ an empty way if there is one, else by the policy
L8  line[w] ← tag; load the block from the next level
L9  UPDATE(s, w)
L10 return miss
```

UPDATE and VICTIM depend on the policy of the set:

- **LRU.** UPDATE stamps way $w$ with the time; VICTIM takes the way with the oldest stamp. Hardware keeps an order of the $W$ ways, which costs $\lceil \log_2 W! \rceil$ bits a set, so it is common only for small $W$.
- **Tree pseudo-LRU.** The $W - 1$ bits form a binary tree over the ways. UPDATE sets each bit on the path to $w$ to point away from $w$; VICTIM follows the bits from the root. The [PLRU page](/plru-replacement/) covers its behaviour.
- **Random.** VICTIM draws a way at random and UPDATE does nothing, as on the [random replacement](/random-replacement/) page. It needs no state at all.
- **FIFO**, or round robin, keeps one pointer a set, as in [FIFO replacement](/fifo-replacement/).

A write goes to the same set by the same lookup; the [write-back](/write-back/) or write-through rule then decides when memory is updated.

## Example

Take $S = 4$ sets, $W = 2$ ways and $B = 16$ bytes, a cache of 128 bytes. The address $420$ is $1\,1010\,0100$ in binary. The low 4 bits $0100$ give offset 4, the next 2 bits $10$ give set 2, and the rest, $110$, gives tag 6. Indeed $\lfloor 420/16 \rfloor = 26$, $26 \bmod 4 = 2$ and $\lfloor 26/4 \rfloor = 6$.

Now alternate the addresses 0 and 128, ten times each, in three caches of the same 128 bytes:

| cache | sets × ways | block of 0 | block of 128 | hits in 20 accesses |
|---|---|---|---|---|
| direct mapped | 8 × 1 | 0, in set 0 | 8, in set 0 | 0 |
| two-way | 4 × 2 | 0, in set 0 | 8, in set 0 | 18 |
| fully associative | 1 × 8 | 0 | 8 | 18 |

In the direct-mapped cache both blocks have index 0, so each access evicts the other block, while 7 of the 8 lines stay empty. These 18 extra misses are *conflict misses*: misses that a fully associative cache of the same size would not have. The two-way cache keeps both blocks in set 0 and misses only on the first use of each.

## Correctness

The proof below shows four facts. The split of line L1 is one to one: a block number gives exactly one (tag, index) pair, and back. Each set holds at most $W$ different tags, and a block is in the cache if and only if its tag is in its set. Each set acts as a separate fully associative cache of $W$ blocks on the requests that map to it. So with $S = 1$ and LRU the cache gives the same hits and misses as fully associative LRU, and with $W = 2$ tree PLRU is the same as LRU.

## Complexity

A lookup does the split in $O(1)$ and compares $W$ tags: $O(W)$ time in software, and one step in hardware with $W$ comparators, followed by a multiplexer that picks the matching way. LRU victim choice is $O(W)$ in this form, and tree PLRU walks $\log_2 W$ bits. The space is $S \cdot W$ blocks, plus a tag and a valid bit for each way and the policy state for each set. For a fixed size, a larger $W$ means fewer index bits and longer tags.

## Variants

- **Way prediction.** The cache guesses the way and reads only that one first, which saves energy and time in a set-associative L1.
- **Victim cache.** Jouppi (ISCA 1990) put a few fully associative lines beside a direct-mapped cache to hold recent victims, which removes many conflict misses.
- **Skewed associativity.** Seznec (ISCA 1993) gave each way its own index hash, so blocks that collide in one way rarely collide in the others.
- **Hashed index.** The set is a hash of more address bits, not just the low bits of the block number, which spreads power-of-two strides over the sets.
- **Sectored lines.** One tag covers a large sector of several smaller blocks, each with its own valid bit.

## When to use it

Nearly all hardware caches are set associative: L1 caches with 4 to 12 ways, and larger L2 and L3 caches with 8 to 20 or more. The design trades a little miss rate for a much cheaper and faster lookup than full associativity. Hennessy and Patterson give a rule of thumb from measurements: a direct-mapped cache of size $N$ has about the same miss rate as a two-way cache of size $N/2$, and eight ways are close to fully associative for typical programs. In software, the same layout fits a fixed-size lookup table that must be fast and simple, such as a transposition table or a translation cache: it is a [hash table](/hash-table/) with $W$ slots a bucket and eviction in the bucket.

## Pitfalls

- **Power-of-two strides.** Arrays with a row length that is a multiple of $S \cdot B$, or several arrays that start at such multiples, map to the same set, and a loop over them gets conflict misses. Padding the rows by one block fixes it.
- **Counting the size.** The cache size is $S \cdot W \cdot B$ bytes of data; the tags and state are extra. A change of $W$ at fixed size changes $S$.
- **Index from a virtual address.** If the L1 is indexed with virtual address bits but tagged with physical ones, the index and offset bits must lie inside the page offset, so the size is at most the page size times $W$. This is why many L1 caches are 32 or 48 KB with 8 or 12 ways over 4 KB pages.
- **Global LRU is not per-set LRU.** Per-set LRU evicts the oldest block of one set, which may be much newer than the oldest block in the cache.
- **Random needs a source.** A hardware random choice is usually a cheap counter or shift register; in a model, pass the generator in so that runs repeat.

## Implementations

## History

The first commercial cache, on the IBM System/360 Model 85 in 1968, used a sector design in which any sector could hold any area of memory. Set-associative mapping became the common choice in the following years because it needs only a few comparators. Alan Jay Smith's 1982 survey measured the miss ratio against the set size and found that a few ways remove most of the gap to full associativity. Mark Hill and Smith, in 1989, gave the three Cs model and fast ways to simulate many associativities in one pass, and showed that the conflict misses fall quickly from one way to two and to four. Later work added victim caches, skewed caches and pseudo-LRU trees to get more of the benefit of full associativity at low cost.

## References
