---
tag: 1SHFPZ
kind: algorithm
slug: plru-replacement
name: Tree pseudo-LRU (PLRU)
aliases:
- pseudo-LRU
- tree-PLRU
- tree PLRU
- PLRU
area: online-and-streaming/paging-and-caching-online
level: intro
summary: Approximates LRU with a binary tree of bits, used in set-associative hardware caches.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of accesses, k: the number of ways in the set}
  time: {worst: O(n k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1989
  people: []
  note: Tree pseudo-LRU is a hardware rule from the late 1980s, used for the 4-way caches of processors such as the Intel 486. Reineke and others analysed its predictability and competitiveness from 2007 on.
prereqs: [lru, set-associative-cache, paging-problem]
see_also: [lru, clock, random-replacement, cache-replacement-policy, lru-competitiveness, sleator-tarjan-paging-bound, fifo-replacement]
sources:
  - paper: "Jan Reineke, Caches in WCET Analysis: Predictability, Competitiveness, Sensitivity, PhD dissertation, Saarland University, 2008"
    locator: Section 2.2.6 (the tree PLRU rule and its example), Theorem 5.19 (the log2 k + 1 most recently used blocks stay), Theorems 6.21 and 6.30 (competitiveness relative to LRU and to OPT with a smaller cache)
  - paper: "Jan Reineke, Daniel Grund, Christoph Berg and Reinhard Wilhelm, Timing predictability of cache replacement policies, Real-Time Systems 37(2) (2007), 99-122"
    locator: the definition of tree PLRU and the metrics evict and fill for LRU, FIFO, MRU and PLRU
  - paper: "Jan Reineke and Daniel Grund, Relative competitive analysis of cache replacement policies, Proceedings of LCTES 2008"
    locator: the competitive ratios of PLRU relative to LRU, and the result that PLRU with 4 or 8 ways is not competitive relative to LRU of the same size
  - book: isbn:9780128119051
    title: John L. Hennessy and David A. Patterson, Computer Architecture, A Quantitative Approach, sixth edition, Morgan Kaufmann, 2017
    locator: Appendix B, Section B.1, block replacement in set-associative caches
---

Tree pseudo-LRU (PLRU) is a replacement rule for one set of a [set-associative cache](/set-associative-cache/) with $k$ ways, where $k$ is a power of two. It keeps $k - 1$ one-bit pointers in a binary tree over the ways. Each access sets the pointers on its path to point away from it, and a miss follows the pointers from the root to find the way to evict. This costs much less hardware than exact [LRU](/lru/), and its miss rate is usually close. But it is not exact: with $4$ ways, a block that is never used again can stay for ever, and PLRU is then not competitive in the sense of the [paging problem](/paging-problem/).

## In plain words

A cache set has a few slots, say four. Exact LRU must remember the full order of use of all four slots, which needs a lot of logic. PLRU remembers less. It splits the slots into two halves, and one switch tells which half was used less recently. Inside each half, another switch tells which slot was used less recently.

When a slot is used, the switches on its way point to the other side. When a new block must come in, the hardware follows the switches from the top and replaces the slot it reaches. The slot it finds was not used recently, but it is not always the slot that was used least recently.

## The problem

The input is a sequence of block addresses that map to one cache set with $k$ ways. A block in the set is a hit. Otherwise it is a miss: the block is loaded, and if all ways are full, one block is evicted. The aim is few misses, with a rule that is cheap to build in hardware and fast enough for each access. The [cache replacement policy](/cache-replacement-policy/) page lists the other rules.

## The algorithm

Number the internal nodes of a complete binary tree in heap order, with the root $1$ and the children of node $v$ at $2v$ and $2v + 1$. The leaves are the ways $0, \ldots, k-1$. Each internal node $v$ has a bit $b[v]$: $0$ points to the left child, $1$ to the right child.

```pseudo id=main
TREE-PLRU(σ, k)
L1  misses ← 0, all ways empty, all bits 0
L2  for each access x in σ do
L3      if x is in some way w then (hit)
L4      else if some way is empty then w ← the lowest empty way, misses ← misses + 1
L5      else start at the root and follow the bits to a leaf; w ← that way, misses ← misses + 1
L6      put x in way w
L7      for each node v on the path from the root to w: set b[v] to point to the child that is not on the path
L8  return misses
```

Line L5 finds the victim with $\log_2 k$ steps. Line L7 updates the same number of bits, on a hit and on a miss. In hardware, both lines are a few gates for each level, and the tag compare of line L3 is done for all ways at once. The rule for empty ways in line L4 varies between processors; filling them from the left is common.

## Example

Four ways, $k = 4$, so three bits: the root $b[1]$, the left node $b[2]$ (ways 0 and 1) and the right node $b[3]$ (ways 2 and 3). The accesses are $a, b, c, d, e$ and then $a, b, c, a, b, d$.

| access | result | ways 0 to 3 after | bits $b[1], b[2], b[3]$ | next victim |
|---|---|---|---|---|
| a | miss, fill | a, -, -, - | 1, 1, 0 | way 2 |
| b | miss, fill | a, b, -, - | 1, 0, 0 | way 2 |
| c | miss, fill | a, b, c, - | 0, 0, 1 | way 0 |
| d | miss, fill | a, b, c, d | 0, 0, 0 | way 0 |
| e | miss, evict a | e, b, c, d | 1, 1, 0 | way 2 |
| a | miss, evict c | e, b, a, d | 0, 1, 1 | way 1 |
| b | hit | e, b, a, d | 1, 0, 1 | way 3 |
| c | miss, evict d | e, b, a, c | 0, 0, 0 | way 0 |
| a | hit | e, b, a, c | 0, 0, 1 | way 0 |
| b | hit | e, b, a, c | 1, 0, 1 | way 3 |
| d | miss, evict c | e, b, a, d | 0, 0, 0 | way 0 |

From here, each repeat of $a, b, c, a, b, d$ gives two misses, and the pointers always move away from way 0 just before a miss. So $e$, which is never used again, stays for ever. LRU with four ways holds $a, b, c, d$ after a few misses and then never misses again.

## Correctness

PLRU serves each access: line L3 or line L6 puts $x$ in the set. Two facts describe its behaviour. First, after each access, the bit at each node points away from the subtree with the most recent access below that node. So the victim is found by going, at each level, to the half that was used less recently. Second, the victim has at least $\log_2 k$ distinct blocks above it in the order of use, one in each subtree that the path leaves. So the $\log_2 k + 1$ most recently used blocks are always in the set, and PLRU never misses more than LRU with $\log_2 k + 1$ ways. The full proofs, and the proof that PLRU with $4$ ways is not competitive, are below.

## Complexity

Each access takes $O(\log k)$ steps for the bits, and the search of line L3 takes $O(k)$ time in software or one parallel compare in hardware. The state is $k - 1$ bits per set. Exact LRU needs at least $\lceil \log_2 k! \rceil$ bits per set, which is $5$ for $k = 4$ and $16$ for $k = 8$, and more logic for each update.

## Properties

- **Equal to LRU for two ways.** With $k = 2$ there is one bit, and it always points to the way used less recently.
- **The recent blocks stay.** The $\log_2 k + 1$ most recently used blocks are always in the set (Reineke 2008, Theorem 5.19). So PLRU with $k$ ways never misses more often than LRU with $\log_2 k + 1$ ways on the same sequence.
- **Competitive against a much smaller cache.** With the bound of Sleator and Tarjan for LRU, this gives $\mathrm{PLRU}_k(\sigma) \le \frac{\log_2 k + 1}{\log_2 k - h + 2} \mathrm{OPT}_h(\sigma) + b$ for each $h \le \log_2 k + 1$. This matches Theorem 6.30 of Reineke.
- **Not competitive for 4 ways.** The example above gives an unbounded number of misses, while LRU with $4$ ways misses only $9$ times and the offline optimum with $4$ ways only $6$ times. So no bound $\mathrm{PLRU}_4(\sigma) \le c \cdot \mathrm{OPT}_4(\sigma) + b$ holds. Reineke and Grund show the same for $8$ ways.
- **Close to LRU in practice.** On common benchmarks the miss rate of PLRU is near that of LRU.

## Variants and improvements

- **Bit-PLRU (MRU bits).** Keep one bit per way, set it on each access, and clear all other bits when all are set. Evict a way with a clear bit. This is another cheap approximation of LRU.
- **CLOCK.** In software caches, the [CLOCK](/clock/) rule plays a similar role: one bit per page approximates LRU.
- **Random replacement.** [Random replacement](/random-replacement/) needs no state at all and is $k$-competitive in expectation against an adaptive online adversary, but it is hard to predict for timing analysis.

## When to use it

Use tree PLRU in hardware caches with $4$ to $16$ ways, where exact LRU costs too much logic and power. It is the standard choice for L1 and L2 caches of many processors. In software, where the order of use is cheap to keep in a list, use exact LRU or CLOCK. For hard real-time systems, where the worst case of each access matters, prefer LRU: analyses of PLRU must assume that fewer blocks are safe in the set.

## Pitfalls

- **Assuming that PLRU is LRU.** A block can stay for ever without use, and the victim is often not the least recently used block. Timing and security analyses that assume exact LRU can be wrong.
- **The bit direction.** Some documents let a bit point to the next victim, others to the side used last. Mixing the two conventions inverts the rule. This page uses pointers toward the victim.
- **Ways that are not a power of two.** The tree needs $k = 2^d$. A 12-way cache must use another scheme, such as a tree with unequal parts.
- **Empty ways.** The fill rule of line L4 is not part of the tree. Different processors fill empty ways in different orders, which changes the later behaviour.

## Implementations

## History

Tree pseudo-LRU appeared in hardware in the late 1980s, when four-way set-associative caches became common in microprocessors. The Intel 486 used three bits per set for its four ways, and many PowerPC and other designs used the same scheme. Reineke, Grund, Berg and Wilhelm studied its predictability in 2007, and Reineke's dissertation of 2008 gave the bounds on this page, including the result that PLRU with $4$ or $8$ ways is not competitive relative to LRU of the same size.

## References
