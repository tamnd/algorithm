---
tag: RTRVA7
kind: algorithm
slug: two-q
name: 2Q buffer replacement
aliases:
- two queues
area: systems/caching-policies
level: advanced
summary: A FIFO queue A1in for pages seen once, a ghost queue A1out of their ids, and an LRU queue Am for pages seen again. Scan resistant like LRU-2, at O(1) per request.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the buffer size in pages}
  time: {expected: O(n)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1994
  people: [Theodore Johnson, Dennis Shasha]
  note: Johnson and Shasha presented 2Q at VLDB 1994 as a buffer policy with the hit ratio of LRU-2 and the cost of LRU.
prereqs: [lru, fifo-replacement]
see_also: [two-q-replacement, lru-k, slru, arc, ghost-lists, s3-fifo, lirs, lru]
sources:
  - paper: "Theodore Johnson and Dennis Shasha, 2Q, a low overhead high performance buffer management replacement algorithm, Proceedings of the 20th International Conference on Very Large Data Bases (VLDB), 1994, 439-450"
    title: 2Q, a low overhead high performance buffer management replacement algorithm
    locator: the simplified 2Q, the full 2Q with A1in, A1out and Am, and the tuning Kin near 25% and Kout near 50% of the buffer
  - paper: doi:10.1145/170035.170081
    title: "Elizabeth J. O'Neil, Patrick E. O'Neil and Gerhard Weikum, The LRU-K page replacement algorithm for database disk buffering, Proceedings of ACM SIGMOD 1993, 297-306"
    locator: LRU-2, the policy whose hit ratio 2Q aims at
---

2Q is a [cache replacement policy](/cache-replacement-policy/) for database buffers by Johnson and Shasha (1994). It aims at the hit ratio of [LRU-2](/lru-k/) with the constant cost per request of [LRU](/lru/). A page seen for the first time goes into a FIFO queue $A1_{in}$. If it is requested again while there, nothing changes: such requests are taken as correlated. When it leaves $A1_{in}$, its identifier goes into a ghost queue $A1_{out}$. Only a page that is requested again while its identifier is in $A1_{out}$ enters the main LRU queue $A_m$. So pages read once by a scan pass through $A1_{in}$ and never touch $A_m$. The paper also gives a simplified 2Q with two queues of resident pages. The [2Q page in the online algorithms area](/two-q-replacement/) proves that 2Q is not competitive; this page covers the policy as a systems tool.

## In plain words

A new page first waits in a short line at the door. If it is used again while it waits, that does not count: many programs touch a page a few times in a row and then never again. When the page reaches the end of the line, it leaves, but the cache writes its name on a short list.

If the page comes back while its name is still on that list, it has shown a real second use, after a while. Then it goes into the main room, which works like LRU. Pages that are read once, as in a big scan, go through the line and out, and never push the useful pages out of the main room.

## The problem

The model is the [paging problem](/paging-problem/) for a buffer pool: a buffer of $k$ pages, a request sequence $\sigma$ of length $n$, an empty buffer at the start, and the number of misses as the cost. 2Q is online and deterministic. Johnson and Shasha wanted a policy that resists scans and uses frequency, as LRU-2 does, without its priority queue and with no lock on a shared structure longer than LRU needs.

## The algorithm

The **full 2Q** has two parameters: $K_{in} < k$, the normal size of $A1_{in}$, and $K_{out}$, the size of $A1_{out}$. The resident pages are the pages of $A1_{in}$ and $A_m$, at most $k$ in total. $A1_{out}$ holds identifiers only.

```pseudo id=main
2Q-ACCESS(p)                     ▷ A1in FIFO, A1out FIFO of ids, Am LRU
L1  if p ∈ Am then
L2      move p to the head of Am; return hit
L3  if p ∈ A1in then
L4      return hit                          ▷ correlated: no change
L5  if p ∈ A1out then
L6      remove p from A1out; RECLAIM()
L7      add p to the head of Am; return miss
L8  RECLAIM()
L9  add p to the head of A1in; return miss

RECLAIM()
L10 if |A1in| + |Am| < k then return       ▷ a free slot
L11 if |A1in| > Kin then
L12     page out the tail of A1in
L13     add its id to the head of A1out
L14     if |A1out| > Kout then drop the tail of A1out
L15 else page out the tail of Am
```

A page paged out of $A_m$ at line L15 is not put in $A1_{out}$: it was not used for a long time, and it has to show reuse again. Johnson and Shasha suggest $K_{in}$ near $25\%$ of the buffer and $K_{out}$ near $50\%$ of the buffer. Since $A1_{out}$ holds only identifiers, its memory cost is small.

The **simplified 2Q** has two queues of resident pages: a FIFO queue $A1$ and an LRU queue $A_m$. A hit in $A1$ moves the page to the head of $A_m$ at once. A miss adds the page to $A1$, and frees the tail of $A1$ if $A1$ holds more than a threshold, and the tail of $A_m$ otherwise. It is close to [SLRU](/slru/). It promotes a page on a correlated second request, which is why the paper goes on to the full version.

## Example

Run full 2Q with $k = 4$, $K_{in} = 1$, $K_{out} = 2$ on $a, a, b, c, d, e, a, f, g, h, i, a$. Each queue is written from its head to its tail.

| $t$ | request | result | paged out | $A1_{in}$ | $A1_{out}$ | $A_m$ |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | a | miss | | a | | |
| 2 | a | hit, in $A1_{in}$ | | a | | |
| 3 to 5 | b, c, d | 3 misses | | d c b a | | |
| 6 | e | miss | a | e d c b | a | |
| 7 | a | miss, in $A1_{out}$ | b | e d c | b | a |
| 8 | f | miss | c | f e d | c b | a |
| 9 | g | miss | d | g f e | d c | a |
| 10, 11 | h, i | 2 misses | e, f | i h g | f e | a |
| 12 | a | hit, in $A_m$ | | i h g | f e | a |

The hit at $t = 2$ does not promote $a$. At $t = 7$, $a$ comes back while its identifier is in $A1_{out}$, so it enters $A_m$. From then on the stream $f, g, h, i$ evicts from $A1_{in}$ only, because $|A1_{in}| > K_{in}$, and $a$ survives. Full 2Q has 10 misses. LRU loses $a$ to the stream twice and has 11. The simplified 2Q has 9 here, because it promotes $a$ at $t = 2$; it would make the same move for a page read twice in one transaction and never again, which would hold a slot of $A_m$ for nothing.

## Correctness

The invariants are: the three queues are disjoint, at most $k$ pages are resident, $A1_{out}$ has at most $K_{out}$ identifiers, all of pages that are not resident, and the requested page is resident after each request. RECLAIM always frees a slot when the buffer is full: if $|A1_{in}| \le K_{in} < k$, then $|A_m| \ge k - K_{in} \ge 1$. With $K_{out} = 0$, no page enters $A_m$, and 2Q is [FIFO](/fifo-replacement/). The proof is below.

## Complexity

- **Time.** With a hash map from page identifiers to queue nodes and a doubly linked list per queue, each line is $O(1)$ expected, so $O(n)$ expected in total. LRU-2 needs a priority queue and $O(\log k)$ per request; this was the main argument of the paper.
- **Space.** $\Theta(k)$ for $k$ resident pages and $K_{out} = O(k)$ identifiers.
- **Hit ratio.** On the database and file traces of the paper, 2Q gave hit ratios close to LRU-2 and above LRU, with the suggested values of $K_{in}$ and $K_{out}$.
- **Worst case.** 2Q with the usual parameters is not competitive: stale pages in $A_m$ are never paged out while new pages keep $A1_{in}$ above $K_{in}$. The proof is on the [2Q page in the online algorithms area](/two-q-replacement/).

## Properties

- **Scan resistant.** Once $A1_{in}$ holds more than $K_{in}$ pages, a scan of new pages evicts only from $A1_{in}$, whatever its length.
- **Correlated references filtered.** A second request while a page is in $A1_{in}$ does nothing, which plays the role of the correlated reference period of LRU-K.
- **Ghost entries.** $A1_{out}$ is a [ghost list](/ghost-lists/): it remembers pages that are gone, so that the policy can see a reuse distance a little longer than $A1_{in}$.
- **Fixed split.** The sizes are set by hand. A workload that changes its mix needs other values.

## Variants and improvements

- **Simplified 2Q.** Described above: two resident queues and promotion on any second request in $A1$.
- **SLRU.** [SLRU](/slru/) has a probationary and a protected segment, both LRU, and demotes from the protected segment to the probationary one.
- **ARC.** [ARC](/arc/) keeps two resident lists and two ghost lists, and moves the split between recency and frequency by itself, with no parameter like $K_{in}$.
- **S3-FIFO.** [S3-FIFO](/s3-fifo/) keeps the 2Q structure, a small FIFO queue, a main queue and a ghost queue, but uses FIFO queues only, with a bit or a small counter in place of the LRU moves.
- **LIRS.** [LIRS](/lirs/) uses the reuse distance in place of a fixed queue size to decide which pages are hot.

## When to use it

Use 2Q for buffer pools and page caches where scans of cold data mix with a hot set, and where the cost per request must stay constant. PostgreSQL used 2Q for a short time in 2005, in place of ARC, before it moved to a clock sweep. Prefer ARC or LIRS when the mix of the workload changes a lot. Prefer LRU or FIFO when a worst-case bound matters.

## Pitfalls

- **Leaving the identifier in $A1_{out}$.** When a page from $A1_{out}$ enters $A_m$ at line L6, its identifier must leave $A1_{out}$. Otherwise a page can be in two queues, and a later trim of $A1_{out}$ can act on a resident page.
- **Promoting on a hit in $A1_{in}$.** That gives the simplified 2Q. Correlated requests then fill $A_m$ with pages that are not hot.
- **$K_{in} \ge k$.** Then $A_m$ can be empty when RECLAIM needs to free a slot from it. Keep $K_{in} < k$.
- **Too short $A1_{out}$.** A page with real reuse leaves $A1_{out}$ before its second request and never enters $A_m$. The paper found $K_{out}$ near half of the buffer to work well.

## Implementations

## History

Johnson and Shasha presented 2Q at VLDB 1994. Their aim was the hit ratio of LRU-2 of O'Neil, O'Neil and Weikum (1993) without its priority queue. The structure of a small queue for new pages, a ghost queue of identifiers and a main queue came back in later policies: ARC in 2003, CAR in 2004 and S3-FIFO in 2023. PostgreSQL replaced ARC by 2Q in release 8.0.2 in 2005 because of a patent on ARC, and moved to a clock sweep soon after.

## References
