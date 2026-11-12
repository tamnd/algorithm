---
tag: ESWX79
kind: algorithm
slug: lirs
name: LIRS
aliases:
- LIRS replacement
- Low Inter-reference Recency Set
- low inter-reference recency set
area: systems/caching-policies
level: advanced
summary: Ranks blocks by inter-reference recency, the reuse distance at their last access, and keeps the low ones. Resists loops and scans.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, L: the cache size in blocks, s: the largest size of stack S}
  time: {worst: O(n), expected: O(n)}
  space: {extra: O(s)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2002
  people: [Song Jiang, Xiaodong Zhang]
  note: Jiang and Zhang presented LIRS at ACM SIGMETRICS 2002 and gave an extended version in IEEE Transactions on Computers in 2005. CLOCK-Pro is its clock form.
prereqs: [lru, reuse-distance, ghost-lists]
see_also: [clock-pro, arc, two-q, lru-k, belady-optimal, mattson-stack-algorithm, s3-fifo]
sources:
  - paper: doi:10.1145/511334.511340
    title: "Song Jiang and Xiaodong Zhang, LIRS: An Efficient Low Inter-reference Recency Set Replacement Policy to Improve Buffer Cache Performance, ACM SIGMETRICS 2002, 31-42"
    locator: the definition of IRR and recency, the LIRS stack S, the stack Q of resident HIR blocks and stack pruning
  - paper: doi:10.1109/TC.2005.130
    title: "Song Jiang and Xiaodong Zhang, Making LRU Friendly to Weak Locality Workloads: A Novel Replacement Algorithm to Improve Buffer Cache Performance, IEEE Transactions on Computers 54(8) (2005), 939-952"
    locator: Section 1.2 (recency and IRR), Section 3.2 and Section 3.3 with Fig. 1, Fig. 2 and Table 1 (the three cases and stack pruning), Section 4.1 (Lhirs is 1 percent of the cache), Section 5.2 (the limit on the size of S)
  - url: https://www.usenix.org/legacy/event/usenix05/tech/general/full_papers/jiang/jiang.pdf
    title: "Song Jiang, Feng Chen and Xiaodong Zhang, CLOCK-Pro: An Effective Improvement of the CLOCK Replacement, USENIX ATC 2005"
    locator: Section 3, which restates the LIRS rule in terms of reuse distance
---

LIRS, the low inter-reference recency set policy, is a [cache replacement policy](/cache-replacement-policy/) that ranks blocks by their inter-reference recency (IRR). The IRR of a block is the number of other distinct blocks accessed between its last two accesses, which is its [reuse distance](/reuse-distance/) at the last access. LIRS keeps the blocks with low IRR, the LIR blocks, always in the cache, and gives a small part of the cache to the other blocks, the HIR blocks. It keeps some evicted HIR blocks as [ghost entries](/ghost-lists/) so that it can see their IRR when they come back. LIRS does well on loops and scans, where [LRU](/lru/) does badly, and each request costs $O(1)$ amortized time.

## In plain words

LRU asks how long ago a block was used. LIRS asks how long the gap was between its last two uses. A block that came back after a short gap is likely to come back soon again, so LIRS protects it. A block that was used once, or came back after a long gap, gets only a small trial area.

Think of a library desk. Most of the desk holds books that you reread often. A small corner holds books you just picked up. If a book in the corner is used again soon, and sooner than the slowest book on the main desk was, the two books swap places. A one-off pile of new books can only pass through the corner, so it never pushes the regular books away.

## The problem

The model is the [paging problem](/paging-problem/) with a cache of $L$ blocks. LIRS aims to fix three weak points of LRU: a scan of blocks used once flushes the cache, a loop over slightly more than $L$ blocks misses on every access, and blocks with different access rates are treated the same.

Two quantities drive the policy. The *recency* of a block is the number of other distinct blocks accessed since its last access. The *IRR* of a block is the number of other distinct blocks accessed between its last two accesses, and it is infinite for a block accessed only once. The cache is split into $L_{lirs}$ blocks for LIR blocks and $L_{hirs}$ blocks for resident HIR blocks, with $L_{lirs} + L_{hirs} = L$. The paper sets $L_{hirs}$ to 1 percent of the cache.

## The algorithm

LIRS keeps two stacks, both with the bottom as the oldest entry.

- **Stack S** holds every LIR block, and every HIR block, resident or not, whose recency is smaller than the largest recency of an LIR block. It is in order of last access. Its bottom is always an LIR block.
- **Stack Q** holds every resident HIR block. Its bottom is the next victim.

A nonresident HIR block in S is a ghost: its data is gone but its entry tells LIRS that it came back after a short gap. *Stack pruning* removes HIR blocks from the bottom of S until an LIR block is at the bottom.

```pseudo id=main
LIRS-ACCESS(x)
L1  if x is an LIR block then                       ▷ case 1: hit
L2      move x to the top of S
L3      PRUNE()                                     ▷ needed if x was at the bottom
L4      return hit
L5  if x is a resident HIR block then               ▷ case 2: hit
L6      if x ∈ S then                               ▷ case 2a
L7          move x to the top of S, make it LIR and remove it from Q
L8          DEMOTE()
L9      else                                        ▷ case 2b
L10         push x on top of S and move x to the top of Q
L11     return hit
L12 if fewer than L_lirs blocks are LIR then        ▷ warm-up: miss
L13     push x on top of S as an LIR block, load it and return miss
L14 if the cache is full then                      ▷ case 3: miss
L15     evict the bottom block of Q; if it is in S, it stays there as nonresident
L16 if x ∈ S then                                   ▷ case 3a: x was a ghost in S
L17     load x, move it to the top of S and make it LIR
L18     DEMOTE()
L19 else                                            ▷ case 3b
L20     load x and push it on top of S and on top of Q as a resident HIR block
L21 return miss

DEMOTE()
L22 move the bottom block of S to the top of Q as a resident HIR block
L23 PRUNE()

PRUNE()
L24 while the bottom block of S is an HIR block, remove it from S
```

The swap in cases 2a and 3a is the heart of LIRS. If an HIR block $x$ is found in S, its new IRR equals its recency just before the access, which is less than the recency of the LIR block at the bottom of S. So $x$ now has a lower IRR than the bottom block will have at best, and the two blocks change status.

S and Q are [doubly linked lists](/doubly-linked-list/), and a [hash table](/hash-table/) maps each block to its entries and status.

## Example

Take $L = 3$, $L_{lirs} = 2$ and $L_{hirs} = 1$, and the trace $A, D, B, C, B, A, D, A, E, D, C$ from a cold cache. Upper case marks an LIR block and lower case an HIR block. A star marks a nonresident HIR block in S. Stacks are written from bottom to top.

| $t$ | access | result | case | evicted | S | Q |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | A | miss | warm-up | | A | |
| 2 | D | miss | warm-up | | A D | |
| 3 | B | miss | 3b | | A D b | b |
| 4 | C | miss | 3b | B | A D b* c | c |
| 5 | B | miss | 3a | C | D c* B | a |
| 6 | A | hit | 2b | | D c* B a | a |
| 7 | D | hit | 1 | | B a D | a |
| 8 | A | hit | 2a | | D A | b |
| 9 | E | miss | 3b | B | D A e | e |
| 10 | D | hit | 1 | | A e D | e |
| 11 | C | miss | 3b | E | A e* D c | c |

At $t = 5$, B is a ghost in S, so it becomes LIR, and A, the LIR block at the bottom of S, becomes a resident HIR block. Pruning then drops nothing, because D is LIR. At $t = 7$, D was at the bottom of S, and pruning after the move removes the ghost of C. At $t = 8$, A is in S, so it swaps status with B. On this trace LIRS has four hits. The first nine accesses are the trace of Table 1 in the paper. The paper assumes a snapshot with LIR set $\{A, B\}$, the two blocks with IRR 1. From a cold cache, warm-up gives LIR status to A and D first, so the state at $t = 9$ differs.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). Let $m$ be the time of the last access of the oldest LIR block. The proof shows that S holds exactly the LIR blocks and the blocks whose last access is after $m$, in order of last access, so the bottom of S is the oldest LIR block. It shows that the cache holds at most $L$ blocks, with at most $L_{lirs}$ LIR blocks and at most $L_{hirs}$ resident HIR blocks. It also shows that an HIR block becomes LIR exactly when its new IRR is less than the recency of the oldest LIR block.

## Complexity

Each access moves a constant number of entries, plus the entries removed by pruning. Every entry that pruning removes was pushed by an earlier access, so pruning costs $O(n)$ in total over $n$ accesses, and the total time is $O(n)$. The cache holds $L$ blocks. Stack S also holds ghost entries, and with no limit it can grow with the number of distinct blocks seen since the oldest LIR block was last accessed. The paper's later version caps S at a small multiple of $L$ and drops HIR entries near the bottom when it is full.

## Properties

- **Online and deterministic.**
- **LIR blocks never miss.** An LIR block is always resident. Only HIR blocks can be evicted.
- **Scan resistance.** A scan of new blocks enters as HIR blocks in case 3b and leaves through Q. It never changes the LIR set, because its blocks are never found in S again before they are pruned.
- **Loop resistance.** On a loop over more than $L$ blocks, the LIR blocks stay in the cache and hit on every turn. The test file runs a loop of 12 blocks with $L = 10$ and $L_{hirs} = 1$, and LIRS hits on 9 blocks in each turn after warm-up. LRU gets no hit on that loop.
- **No worst-case guarantee beyond the general bound.** Like every deterministic online policy, its [competitive ratio](/competitive-ratio/) is at least $L$. No better bound is known for LIRS. A small $L_{hirs}$ makes it miss often on workloads where most blocks are new.

## Variants and improvements

- **CLOCK-Pro.** [CLOCK-Pro](/clock-pro/) puts hot and cold pages and ghost entries in one clock and makes the size of the cold area adaptive, so that a hit only sets a bit.
- **Bounded stack.** The extended paper caps the size of S, for example at 1.5 to 3 times $L$, and reports little loss.
- **ARC.** [ARC](/arc/) also keeps ghost keys, but splits the cache by recency and frequency, not by IRR. It does not handle loops.

## When to use it

Use LIRS for a buffer cache or block cache with loops, scans and blocks of very different access rates, such as database and file system caches. It suits workloads where the reuse distance of a block is stable. If the hot set changes quickly, the small HIR area makes it slow to admit new hot blocks; a larger $L_{hirs}$ or [ARC](/arc/) may adapt faster. If a lock on each hit is too costly, use [CLOCK-Pro](/clock-pro/).

A small seeded run made for this page uses Python `random.Random(1)`, $c = 100$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| ARC | 45.6% | 76.7% | 0.0% | 28.0% |
| LIRS | 44.9% | 76.7% | 82.2% | 25.6% |
| CLOCK-Pro | 46.8% | 76.6% | 80.7% | 28.6% |

On the loop of 120 keys, LIRS comes within 1 point of MIN, where LRU and ARC get nothing. These numbers come from small synthetic traces and say nothing about real workloads.

## Pitfalls

- **Forgetting to push a case 2b block onto S.** A resident HIR block that is not in S must still go to the top of S, so that its next access can find it there.
- **Pruning only on misses.** Case 1 must prune when the accessed block was at the bottom. Otherwise the bottom of S can be an HIR block and DEMOTE would demote the wrong block.
- **An unbounded stack S.** A long run of new blocks with no access to the oldest LIR block makes S grow. Cap its size in production.
- **Taking Table 1 as a cold-start result.** The paper's Table 1 is a snapshot set by IRR. A run from an empty cache gives a different LIR set, as the example shows.
- **Treating ghosts as hits.** A nonresident HIR block in S is a miss. Its entry only decides its new status.

## Implementations

## History

Song Jiang and Xiaodong Zhang presented LIRS at ACM SIGMETRICS 2002. They used IRR, which Mattson and others' stack distance makes easy to read from an LRU stack, as the basis for replacement. In 2005 they gave an extended version in IEEE Transactions on Computers with a size limit for S and more experiments, and with Feng Chen they gave the clock form [CLOCK-Pro](/clock-pro/) at USENIX ATC 2005.

## References
