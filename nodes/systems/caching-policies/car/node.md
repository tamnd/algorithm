---
tag: BEKWFB
kind: algorithm
slug: car
name: CAR (clock with adaptive replacement)
aliases:
- CAR
area: systems/caching-policies
level: advanced
summary: ARC with its two LRU lists replaced by two clocks, so a hit only sets a bit. The same ghost lists and the same adaptive target p.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, c: the cache size in pages}
  time: {worst: O(n), expected: O(n)}
  space: {extra: Θ(c)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2004
  people: [Sorav Bansal, Dharmendra S. Modha]
  note: Bansal and Modha presented CAR and its variant CART at USENIX FAST 2004, as a clock form of ARC that needs no lock on a hit.
prereqs: [arc, clock]
see_also: [clock-pro, ghost-lists, lru, sieve, s3-fifo, competitive-ratio]
sources:
  - url: https://www.usenix.org/legacy/events/fast04/tech/full_papers/bansal/bansal.pdf
    title: "Sorav Bansal and Dharmendra S. Modha, CAR: Clock with Adaptive Replacement, USENIX FAST 2004, 187-200"
    locator: Section III.B with Fig. 1 and Fig. 2 (the CAR algorithm and the invariants I1 to I7), Section IV with Fig. 3 (CART)
  - url: https://www.usenix.org/legacy/events/fast03/tech/full_papers/megiddo/megiddo.pdf
    title: "Nimrod Megiddo and Dharmendra S. Modha, ARC: A Self-Tuning, Low Overhead Replacement Cache, USENIX FAST 2003, 115-130"
    locator: Section IV and Fig. 4, the rule for the target p that CAR reuses
  - url: https://arxiv.org/abs/1503.07624
    title: "Mario E. Consuegra, Wendy A. Martinez, Giri Narasimhan, Raju Rangaswami, Leo Shao and Giuseppe Vietri, Analyzing Adaptive Cache Replacement Strategies, arXiv 1503.07624 (2015)"
    locator: the abstract, the claimed competitive ratio of CAR
---

CAR, clock with adaptive replacement, is a [cache replacement policy](/cache-replacement-policy/) that keeps the structure of [ARC](/arc/) but replaces its two LRU lists of cached pages with two [clocks](/clock/). Clock $T_1$ holds pages seen once recently and clock $T_2$ holds pages seen at least twice. A hit only sets the reference bit of the page, so hits need no lock and no list update. The [ghost lists](/ghost-lists/) $B_1$ and $B_2$ and the adaptive target $p$ for the size of $T_1$ work as in ARC.

## In plain words

ARC moves a page to the front of a list on every hit. That is a write to a shared list, and in a busy system many threads wait for it. CLOCK avoids this: a hit only raises a flag on the page, and the flags are read later when the system needs a free slot.

CAR puts these two ideas together. It keeps two clocks instead of two lists, and the same notes about recently evicted pages that ARC keeps. When a note shows that a clock was too small, CAR gives that clock more room. A page in the first clock whose flag is up moves to the second clock, because it was used more than once.

## The problem

The model is the [paging problem](/paging-problem/) with a cache of $c$ pages. CAR aims at the hit ratio of ARC, with the low cost per hit of CLOCK. This matters in virtual memory, where the hardware sets a reference bit and the operating system cannot afford to update a list on each access, and in caches shared by many threads.

## The algorithm

$T_1$ and $T_2$ are circular lists. The head of a clock is the page under its hand, and the tail is the page just behind the hand, so "move to the tail" means that the hand moves past the page. $B_1$ and $B_2$ are LRU lists of keys only. The target $p$ starts at $0$. The pseudocode follows Fig. 2 of the paper.

```pseudo id=main
CAR-ACCESS(x)                           ▷ clocks T1, T2, ghost lists B1, B2, target p
L1  if x ∈ T1 ∪ T2 then
L2      set the reference bit of x to 1 and return hit
L3  if |T1| + |T2| = c then             ▷ the cache is full
L4      REPLACE()
L5      if x ∉ B1 ∪ B2 and |T1| + |B1| = c then
L6          delete the LRU key of B1
L7      else if x ∉ B1 ∪ B2 and |T1| + |T2| + |B1| + |B2| = 2c then
L8          delete the LRU key of B2
L9  if x ∉ B1 ∪ B2 then
L10     put x at the tail of T1 with bit 0 and return miss
L11 else if x ∈ B1 then
L12     p ← min(p + max(1, |B2| / |B1|), c)
L13     move x from B1 to the tail of T2 with bit 0 and return miss
L14 else
L15     p ← max(p − max(1, |B1| / |B2|), 0)
L16     move x from B2 to the tail of T2 with bit 0 and return miss

REPLACE()
L17 repeat
L18     if |T1| ≥ max(1, p) then
L19         if the head page of T1 has bit 0 then
L20             evict it, put its key at the MRU end of B1, and stop
L21         else clear its bit and move it to the tail of T2
L22     else
L23         if the head page of T2 has bit 0 then
L24             evict it, put its key at the MRU end of B2, and stop
L25         else clear its bit and move it to the tail of T2
```

Line L21 is where CAR learns frequency: a page of $T_1$ with its bit set has been requested at least twice, so it moves to $T_2$. Line L25 is plain CLOCK on $T_2$. The two tests on lines L5 and L7 keep the directory at $2c$ keys at most, and they skip the delete when $x$ is a ghost, because then $x$ leaves its ghost list on line L13 or L16.

Three details differ from ARC. A hit does not move the page (line L2). REPLACE runs before $p$ is updated, not after. The test on line L18 is $|T_1| \ge \max(1, p)$, so a tie goes to $T_1$, with no special case for $x \in B_2$.

## Example

Take $c = 3$ and the same trace as on the ARC page, $1, 2, 1, 3, 4, 2, 5, 4, 1, 6, 1, 2$. Clocks are written from head to tail, a star marks a set bit, and ghost lists are written LRU first.

| $t$ | request | result | evicted | $T_1$ | $T_2$ | $B_1$ | $B_2$ | $p$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | miss | | 1 | | | | 0 |
| 2 | 2 | miss | | 1 2 | | | | 0 |
| 3 | 1 | hit | | 1* 2 | | | | 0 |
| 4 | 3 | miss | | 1* 2 3 | | | | 0 |
| 5 | 4 | miss | 2 | 3 4 | 1 | 2 | | 0 |
| 6 | 2 | miss | 3 | 4 | 1 2 | 3 | | 1 |
| 7 | 5 | miss | 4 | 5 | 1 2 | 3 4 | | 1 |
| 8 | 4 | miss | 5 | | 1 2 4 | 3 5 | | 2 |
| 9 | 1 | hit | | | 1* 2 4 | 3 5 | | 2 |
| 10 | 6 | miss | 2 | 6 | 4 1 | 3 5 | 2 | 2 |
| 11 | 1 | hit | | 6 | 4 1* | 3 5 | 2 | 2 |
| 12 | 2 | miss | 4 | 6 | 1* 2 | 3 5 | 4 | 1 |

At $t = 5$ the hand of $T_1$ finds page 1 with its bit set, clears it and moves it to $T_2$ (line L21), then evicts page 2. At $t = 7$ the two policies part. ARC has $|T_1| = 1 = p$ and evicts from $T_2$, but CAR has $|T_1| \ge \max(1, p) = 1$ and evicts page 4 from $T_1$. So at $t = 8$ ARC has a hit and CAR a ghost hit. At $t = 10$ the hand of $T_2$ passes page 1, whose bit is set, and evicts page 2. CAR has three hits here, as ARC does, at different times. The test file checks every row.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that REPLACE always stops after at most $c + 1$ steps of the hand, and that CAR keeps the invariants I1 to I7 of the paper: $|T_1| + |T_2| \le c$, $|T_1| + |B_1| \le c$, $|T_2| + |B_2| \le 2c$, at most $2c$ keys in the directory, empty ghost lists while the cache is not full, a full cache once the directory has $c$ keys, and a cache that stays full once it is full.

## Complexity

A hit takes $O(1)$ time and writes only one bit. A miss takes $O(1)$ time plus the steps of the hand in REPLACE. Each step that does not evict clears a bit that a hit had set, and a bit is set at most once for each hit, so all hand steps over a trace of $n$ requests number at most $2n$. The total time is $O(n)$ with a [hash table](/hash-table/) for the directory, and the extra space is $\Theta(c)$ keys for the clocks and ghost lists.

## Properties

- **Online and deterministic.**
- **No tuning parameter.** The target $p$ is learned, as in ARC.
- **Low cost per hit.** A hit sets a bit and does not reorder anything. This is the main reason for CAR.
- **No worst-case guarantee beyond the general bound.** As with every deterministic online policy, the [competitive ratio](/competitive-ratio/) is at least $c$. No ratio close to $c$ is proven for CAR. A 2015 preprint by Consuegra and others claims a bound of $18c$, and it has not been through peer review.
- **Not the same as ARC.** The example shows that the two policies can evict different pages on the same trace.

## Variants and improvements

- **CART.** In the same paper, Bansal and Modha add a filter bit to each page that marks it as short-term or long-term use. A page that is referenced twice in quick succession does not count as frequent. CART changes the invariants to $|T_2| + |B_2| \le c$ and $|T_1| + |B_1| \le 2c$.
- **CLOCK-Pro.** [CLOCK-Pro](/clock-pro/) is the clock form of [LIRS](/lirs/). It also keeps ghost keys, but in the same circular list as the cached pages.
- **SIEVE and S3-FIFO.** [SIEVE](/sieve/) and [S3-FIFO](/s3-fifo/) also aim at a low cost per hit, with FIFO order instead of clock order.

## When to use it

Use CAR where you would use ARC but the cost of a list update on each hit is too high: in a kernel page cache with hardware reference bits, or in a cache that many threads read at once. On sequential workloads with one thread, ARC and CAR give similar hit ratios in the paper's tests, and ARC is simpler to reason about.

A small seeded run made for this page uses Python `random.Random(1)`, $c = 100$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| ARC | 45.6% | 76.7% | 0.0% | 28.0% |
| CAR | 46.2% | 76.7% | 0.0% | 28.2% |
| CLOCK-Pro | 46.8% | 76.6% | 80.7% | 28.6% |

CAR stays close to ARC on all four traces. These numbers come from small synthetic traces and say nothing about real workloads.

## Pitfalls

- **Copying ARC's order of steps.** In CAR, REPLACE runs first and $p$ changes after it, on lines L12 and L15. In ARC, $p$ changes first.
- **Moving a page from $T_1$ to the head of $T_2$.** It goes to the tail of $T_2$, behind the hand, so that it gets a full turn of the hand.
- **Keeping the bit when a page moves.** The bit is cleared on line L21. A page that moves from $T_1$ to $T_2$ with its bit set would get a second free pass.
- **Deleting a ghost when $x$ is itself a ghost.** The tests on lines L5 and L7 skip this, and then $x$ leaves its ghost list. Deleting another ghost as well would lose history for no reason.
- **The patent.** CAR builds on ARC, which IBM held a patent on. Check the legal state before you ship it.

## Implementations

## History

Sorav Bansal and Dharmendra S. Modha presented CAR at the USENIX FAST conference in 2004. They built it on [ARC](/arc/), which Megiddo and Modha had published a year before, and on [CLOCK](/clock/), which goes back to the Multics system of the late 1960s. In the same paper they gave CART, which adds a test for temporal filtering. The paper reports hit ratios close to ARC and better than CLOCK on its traces.

## References
