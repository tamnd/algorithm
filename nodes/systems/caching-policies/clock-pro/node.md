---
tag: P3XQXT
kind: algorithm
slug: clock-pro
name: CLOCK-Pro
aliases:
- CLOCK-Pro replacement
area: systems/caching-policies
level: advanced
summary: The clock form of LIRS. One circular list holds hot pages, cold pages and ghosts of cold pages, swept by three hands, with an adaptive cold area.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, m: the memory size in pages}
  time: {worst: O(n m), expected: O(n m)}
  space: {extra: Θ(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2005
  people: [Song Jiang, Feng Chen, Xiaodong Zhang]
  note: Jiang, Chen and Zhang presented CLOCK-Pro at USENIX ATC 2005, to bring the reuse distance rule of LIRS to virtual memory, where a hit can only set a reference bit.
prereqs: [lirs, clock]
see_also: [car, arc, ghost-lists, reuse-distance, sieve, s3-fifo]
sources:
  - url: https://www.usenix.org/legacy/event/usenix05/tech/general/full_papers/jiang/jiang.pdf
    title: "Song Jiang, Feng Chen and Xiaodong Zhang, CLOCK-Pro: An Effective Improvement of the CLOCK Replacement, USENIX Annual Technical Conference 2005"
    locator: Section 4.1 and Section 4.2 (hot and cold pages, test periods, the one clock), Section 4.3 (HAND_cold, HAND_hot and HAND_test), Section 4.4 (the adaptive cold allocation)
  - paper: doi:10.1109/TC.2005.130
    title: "Song Jiang and Xiaodong Zhang, Making LRU Friendly to Weak Locality Workloads: A Novel Replacement Algorithm to Improve Buffer Cache Performance, IEEE Transactions on Computers 54(8) (2005), 939-952"
    locator: Section 3, the LIRS rule that CLOCK-Pro approximates
---

CLOCK-Pro is a [cache replacement policy](/cache-replacement-policy/) for virtual memory that brings the rule of [LIRS](/lirs/) to the cost model of [CLOCK](/clock/). A page with a small reuse distance is *hot* and a page with a large reuse distance is *cold*. All pages, and the [ghost entries](/ghost-lists/) of recently evicted cold pages, sit in one circular list. Three hands sweep the list: HAND_cold looks for a cold page to evict, HAND_hot turns a hot page cold when there are too many hot pages, and HAND_test ends the test periods of cold pages. A hit only sets a reference bit. The share of memory for cold pages adapts to the workload.

## In plain words

LIRS keeps the pages that came back after a short gap. To measure gaps it moves pages in a stack on every access, which an operating system cannot afford, because the hardware only sets a bit when a page is used.

CLOCK-Pro measures gaps with the clock instead. A newly loaded page is cold and gets a trial period, which lasts until a hand has gone once around the clock. If the page is used again during its trial, its gap was short, and it becomes hot. Even if a cold page is evicted during its trial, CLOCK-Pro keeps a note with its name until the trial ends. If the page comes back while the note is still there, it returns as a hot page.

## The problem

The model is the [paging problem](/paging-problem/) with a memory of $m$ pages, with one extra limit: the policy cannot do any work on a hit except set the reference bit of the page. This is the setting of page replacement in an operating system, and of caches where the cost of a lock on each hit is too high. The aim is a policy that resists scans and loops, as LIRS does, with the cost of CLOCK.

## The algorithm

Memory is split between hot pages and resident cold pages, with a target $m_c$ for cold pages and $m - m_c$ for hot pages, $1 \le m_c \le m - 1$. Each entry in the clock is a hot page, a resident cold page or a non-resident cold page. Each resident page has a reference bit, and each cold page may be in its *test period*. At most $m$ non-resident cold pages are kept. The *head* of the list is the place just behind HAND_hot, so a page put at the head is the last one that HAND_hot reaches. Removing an entry under a hand moves the hand to the next entry.

```pseudo id=main
CLOCK-PRO-ACCESS(x)
L1  if x is resident then
L2      set the reference bit of x and return hit
L3  if m pages are resident then
L4      RUN-HAND-COLD()                         ▷ frees one page
L5  if x is in the clock then                    ▷ a non-resident cold page in its test period
L6      m_c ← min(m_c + 1, m − 1)
L7      make x a resident hot page with bit 0 and move it to the head
L8      BALANCE()
L9  else
L10     put x at the head as a resident cold page with bit 0, in its test period
L11 return miss

RUN-HAND-COLD()
L12 repeat
L13     let e be the entry under HAND_cold
L14     if e is not a resident cold page then advance HAND_cold
L15     else if the bit of e is 0 then
L16         evict e; keep it as non-resident if it is in its test period, else remove it
L17         advance HAND_cold
L18         while more than m pages are non-resident do RUN-HAND-TEST()
L19         stop
L20     else if e is in its test period then
L21         clear the bit, make e hot, m_c ← min(m_c + 1, m − 1), move e to the head
L22         BALANCE()
L23     else
L24         clear the bit, start a new test period for e, move e to the head

BALANCE()
L25 while more than m − m_c pages are hot do RUN-HAND-HOT()

RUN-HAND-HOT()                                  ▷ turns one hot page cold
L26 repeat
L27     let e be the entry under HAND_hot
L28     if e is cold then
L29         if e is in its test period, end it and set m_c ← max(m_c − 1, 1)
L30         if e is non-resident then remove it, else advance HAND_hot
L31     else if the bit of e is 1 then clear it and advance HAND_hot
L32     else make e cold, advance HAND_hot and stop

RUN-HAND-TEST()                                 ▷ one step
L33 let e be the entry under HAND_test
L34 if e is cold then do lines L29 and L30 with HAND_test
L35 else advance HAND_test
```

A cold page that is used during its test period has a reuse distance smaller than the recency of the oldest hot page, which is at HAND_hot. So it should be hot, as in LIRS (lines L5 and L20). A test period that ends with no use is evidence that the cold area is too big, so $m_c$ shrinks (line L29). A use during a test period is evidence that more cold pages should stay, so $m_c$ grows (lines L6 and L21). The paper fixes the rules for the hands but leaves two details open. Here a cold page found with its bit set after its test period starts a new one (line L24), and hot pages are held at $m - m_c$ by BALANCE.

## Example

Take $m = 4$ with a fixed $m_c = 1$, so at most three hot pages, and the trace $A, B, A, C, D, B, E, A, F, B, C, G, D$. The clock is listed from HAND_hot around the circle. "AH" is a hot page, "Ac" a resident cold page and "An" a non-resident cold page. A star marks a set bit and a "t" a test period.

| $t$ | request | result | evicted | clock from HAND_hot |
| --- | --- | --- | --- | --- |
| 1 to 6 | A B A C D B | 4 misses, 2 hits | | Ac\*t Bc\*t Cct Dct |
| 7 | E | miss | C | Cnt Dct AH BH Ect |
| 8 | A | hit | | Cnt Dct AH\* BH Ect |
| 9 | F | miss | D | Cnt Dnt AH\* BH Ect Fct |
| 10 | B | hit | | Cnt Dnt AH\* BH\* Ect Fct |
| 11 | C | miss | E | Dnt AH\* BH\* Ent Fct CH |
| 12 | G | miss | F | Dnt AH\* BH\* Ent Fnt CH Gct |
| 13 | D | miss | G | Gnt DH AH BH Cc |

At $t = 7$ memory is full. HAND_cold finds A and B with their bits set during their test periods, so both become hot and move to the head. It then evicts C, which stays as a ghost because it is in its test period. At $t = 11$, C is found in the clock, so it returns as a hot page: its gap of five other pages was short enough. At $t = 13$, D returns as the fourth hot page, one more than $m - m_c = 3$. HAND_hot clears the bits of A and B, removes the ghosts of E and F as their test periods end, and turns C cold. The test file checks these rows.

## Correctness

The proof is in [the correctness proof](proofs/correctness.md). It shows that every hand run stops, and that after every request at most $m$ pages are resident, at most $m$ are non-resident, at most $m - m_c$ are hot, $1 \le m_c \le m - 1$, every hot page is resident and has no test period, and every non-resident page is cold and in its test period. So the ghosts never use memory for data, and a ghost can only exist while its page could still turn hot.

## Complexity

A hit takes $O(1)$ time. On a miss, each step of a hand either clears a bit set by an earlier hit, evicts or removes an entry, ends a test period, or skips over an entry. Between two steps of the first kinds a hand skips at most the $2m$ entries of the clock. So the total work over $n$ requests is $O(n m)$ in the worst case. It is much less in practice, because a hand usually finds what it needs within a few entries. The clock holds at most $2m$ entries, so the extra space is $\Theta(m)$.

## Properties

- **Online and deterministic.**
- **Hits are cheap.** A hit sets one bit, as in CLOCK.
- **Scan resistance.** A scan of new pages enters as cold pages and leaves through HAND_cold. It turns no page hot, and it does not raise $m_c$. The test file checks that six hot pages survive a scan of 1000 new pages with $m = 10$ and a fixed $m_c = 2$.
- **Loops up to a limit.** With $m = 10$ and the default $m_c$, the implementation here gets about eight hits per turn on loops of 11, 12 and 15 pages, where LRU gets none. On a loop of 20 pages it gets no hits, because a ghost lives only until $m$ other ghosts are kept, and the gap of 19 pages is too long. LIRS with an unbounded stack still hits on that loop.
- **No worst-case guarantee beyond the general bound.** Like every deterministic online policy, its [competitive ratio](/competitive-ratio/) is at least $m$, and no better bound is known for it.

## Variants and improvements

- **Fixed cold area.** With the adaptation off, $m_c$ is a parameter, which gives a clock version of LIRS with $L_{hirs} = m_c$.
- **CAR.** [CAR](/car/) is the clock form of [ARC](/arc/). It keeps two clocks and two separate ghost lists, and splits pages by recency and frequency, not by reuse distance.
- **Operating systems.** NetBSD has a CLOCK-Pro page replacement option, and approximations were proposed for Linux.

## When to use it

Use CLOCK-Pro for page replacement in a kernel, or in any cache where a hit can only set a bit, when the workload has loops or scans that defeat CLOCK. For a user-space cache where a hit can update a list, [LIRS](/lirs/) is simpler and does at least as well on loops. For very simple code with good results on web traces, consider [SIEVE](/sieve/) or [S3-FIFO](/s3-fifo/).

A small seeded run made for this page uses Python `random.Random(1)`, $c = 100$ and 30000 requests per trace. Zipf has 1000 keys with exponent 0.8. Scan repeats 1000 uniform requests to 80 hot keys followed by 300 new keys. Loop cycles through 120 keys. Mix takes 60% Zipf, 20% the next key of a 120-key loop and 20% new keys.

| policy | Zipf | scan | loop | mix |
| --- | --- | --- | --- | --- |
| MIN | 62.4% | 76.7% | 82.9% | 39.3% |
| LRU | 37.5% | 70.7% | 0.0% | 16.7% |
| CAR | 46.2% | 76.7% | 0.0% | 28.2% |
| LIRS | 44.9% | 76.7% | 82.2% | 25.6% |
| CLOCK-Pro | 46.8% | 76.6% | 80.7% | 28.6% |

These numbers come from small synthetic traces and say nothing about real workloads.

## Pitfalls

- **Losing track of the head.** All pages, from three hands, go to one head, just behind HAND_hot. Putting them behind HAND_cold instead changes the test periods.
- **Moving a hand past a removed entry.** When a hand removes the entry it points to, the hand must move to the next entry first. Otherwise the hands point at dead entries.
- **No cap on ghosts.** Without HAND_test and the limit of $m$ non-resident pages, the clock grows without bound on a scan.
- **Running BALANCE with no hot pages.** RUN-HAND-HOT must only run when there are more than $m - m_c \ge 1$ hot pages, or it loops forever.
- **Reading the paper's two open details as fixed.** The handling of a cold page with its bit set after its test period, and the exact time at which HAND_hot runs, vary between implementations.

## Implementations

## History

Song Jiang, Feng Chen and Xiaodong Zhang presented CLOCK-Pro at the USENIX Annual Technical Conference in 2005. It followed LIRS, which Jiang and Zhang had published in 2002, and it answered the main obstacle to LIRS in an operating system: a hit cannot move a page in a stack. The paper also added the adaptive split of memory between hot and cold pages, and it reported an implementation in Linux kernel 2.4.21 (Section 5.2).

## References
