---
tag: ETPAQ6
kind: algorithm
slug: lrfu
name: LRFU (least recently/frequently used)
aliases:
- LRFU replacement
area: systems/caching-policies
level: advanced
summary: Evicts the block with the least CRF, a sum of (1/2)^(λx) over the ages x of its references. λ = 1 gives LRU, λ = 0 gives LFU, and values in between mix them.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size in blocks}
  time: {expected: O(n log k)}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1999
  people: [Donghee Lee, Jongmoo Choi, Jong-Hun Kim, Sam H. Noh, Sang Lyul Min, Yookun Cho, Chong Sang Kim]
  note: Lee and his coauthors presented the LRFU spectrum at SIGMETRICS 1999, and the full paper appeared in IEEE Transactions on Computers in 2001.
prereqs: [lru, lfu, binary-heap]
see_also: [lru, lfu, lfu-da, lru-k, mq-cache, arc, two-q, cache-replacement-policy]
sources:
  - paper: doi:10.1109/TC.2001.970573
    title: "Donghee Lee, Jongmoo Choi, Jong-Hun Kim, Sam H. Noh, Sang Lyul Min, Yookun Cho and Chong Sang Kim, LRFU, a spectrum of policies that subsumes the least recently used and least frequently used policies, IEEE Transactions on Computers 50(12), 2001, 1352-1361"
    locator: the CRF with F(x) = (1/2)^(λx), the proofs that λ = 0 and λ = 1 give LFU and LRU, the update from the last CRF only, and the heap implementation
  - paper: "Donghee Lee, Jongmoo Choi, Jong-Hun Kim, Sam H. Noh, Sang Lyul Min, Yookun Cho and Chong Sang Kim, On the existence of a spectrum of policies that subsumes the least recently used (LRU) and least frequently used (LFU) policies, Proceedings of ACM SIGMETRICS 1999, 134-143"
    title: On the existence of a spectrum of policies that subsumes the LRU and LFU policies
    locator: the first presentation of the LRFU spectrum
  - paper: "Nimrod Megiddo and Dharmendra S. Modha, ARC, a self-tuning, low overhead replacement cache, Proceedings of the 2nd USENIX Conference on File and Storage Technologies (FAST), 2003, 115-130"
    title: ARC, a self-tuning, low overhead replacement cache
    locator: the discussion of LRFU, its parameter λ and its cost per request, as a policy that ARC is compared with
---

LRFU is a [cache replacement policy](/cache-replacement-policy/) by Lee, Choi, Kim, Noh, Min, Cho and Kim (1999, 2001) that joins [LRU](/lru/) and [LFU](/lfu/) in one family. Each block in the cache gets a **combined recency and frequency** value, its CRF: each past reference adds $F(x) = (1/2)^{\lambda x}$, where $x$ is the age of the reference. The block with the least CRF is evicted. With $\lambda = 0$ each reference counts 1, so the CRF is the reference count, and LRFU is LFU. With $\lambda = 1$ the last reference outweighs all earlier ones, and LRFU is LRU. Between these ends, recent references count more than old ones, and the value of $\lambda$ sets the mix. Since $F(x + y) = F(x) F(y)$, the CRF can be updated from its last value, and since all blocks decay at the same rate, a heap finds the victim in $O(\log k)$ time.

## In plain words

Each item in the cache has a score. Each time someone asks for the item, it gets one point. As time passes, all points shrink, at the same speed for all items. When space runs out, the item with the lowest score leaves.

A dial sets how fast points shrink. If they never shrink, the score is just the number of requests, and the cache keeps the most popular items. If they shrink very fast, only the last request matters, and the cache keeps the most recent items. Between these settings, an item needs both many requests and recent ones to stay.

## The problem

The model is the [paging problem](/paging-problem/): a cache of $k$ blocks of equal size, a request sequence $\sigma$ of length $n$, an empty cache at the start, and the number of misses as the cost. LRFU is online and deterministic. Lee and his coauthors saw that LRU uses only the time of the last reference, and LFU only the number of references, and asked for one policy that uses both and contains each of them as a special case.

## The algorithm

Let the references to block $b$ since it entered the cache be at times $t_1 < \ldots < t_j$. At time $t$, its CRF is

$$C_t(b) = \sum_{i=1}^{j} F(t - t_i), \qquad F(x) = \left(\tfrac{1}{2}\right)^{\lambda x}, \quad 0 \le \lambda \le 1.$$

LRFU keeps for each resident block only $C[b]$, its CRF at the time $last[b]$ of its last reference. Since $F(x + y) = F(x) F(y)$, the CRF at time $t$ is $C[b] \cdot F(t - last[b])$, and a new reference at time $t$ gives $C[b] \leftarrow F(0) + F(t - last[b]) \cdot C[b]$, with $F(0) = 1$.

```pseudo id=main
LRFU-ACCESS(x)                ▷ C[b], last[b] for each resident block b
L1  t ← t + 1
L2  if x is resident then
L3      C[x] ← 1 + 2^(−λ (t − last[x])) · C[x]; last[x] ← t
L4      restore the heap order at x; return hit
L5  if k blocks are resident then
L6      v ← the root of the heap, the block with the least C[v] · 2^(−λ (t − last[v]))
L7      remove v from the heap and from the cache
L8  C[x] ← 1; last[x] ← t
L9  insert x into the heap; return miss
```

The heap compares blocks at the current time. Since $C[b] \cdot 2^{-\lambda (t - last[b])}$ has the factor $2^{-\lambda t}$ for all blocks, the order is that of $\log_2 C[b] + \lambda \cdot last[b]$, which does not change while $b$ is not referenced. So only the block of line L3 changes its place in the heap. Ties go to the block with the older last reference. A block that leaves the cache loses its CRF, and it starts again at 1 if it comes back.

## Example

Run LRFU with $k = 3$ and $\lambda = 1/2$ on $c, c, b, b, a, d, e, b, d$. Then $F(1) = 2^{-1/2} \approx 0.707$. After the second $c$, $C[c] = 1 + 0.707 = 1.707$, and the same holds for $b$ after time 4. The table shows the CRF of the resident blocks at time $t$, before the request.

| $t$ | request | result | CRF before the request | evicted |
| --- | --- | --- | --- | --- |
| 1 to 5 | c, c, b, b, a | 3 misses, 2 hits | | |
| 6 | d | miss | c 0.427, b 0.854, a 0.707 | c |
| 7 | e | miss | b 0.604, a 0.500, d 0.707 | a |
| 8 | b | hit | b 0.427, d 0.500, e 0.707 | |
| 9 | d | hit | b 1.009, d 0.354, e 0.500 | |

At $t = 6$, $c$ has two references but they are old, so its CRF is below that of $a$, which has one recent reference. At $t = 7$, the two references of $b$ outweigh the single and older reference of $a$. LRFU has 5 misses. LRU ($\lambda = 1$) evicts $c$, $b$ and $a$, and misses $b$ at $t = 8$: 6 misses. LFU ($\lambda = 0$) keeps $c$ and $b$ with count 2, evicts $a$, $d$ and $e$, and misses $d$ at $t = 9$: 6 misses.

## Correctness

At each eviction, the heap root is the resident block with the least CRF at the current time, with ties to the older last reference, because the heap key differs from $\log_2$ of the CRF by the same amount $\lambda t$ for all blocks. With $\lambda = 0$, $C[b]$ is the number of references since $b$ entered, so LRFU is LFU with ties to the least recently used block. With $\lambda = 1$, every $C[b]$ is in $[1, 2)$, so a block with an older last reference always has a smaller CRF, and LRFU is LRU. The proofs are below.

## Complexity

- **Time.** A hash map gives $C[b]$, $last[b]$ and the heap position of $b$ in $O(1)$ expected time. Lines L4, L6, L7 and L9 are heap steps of $O(\log k)$ time on a [binary heap](/binary-heap/) of the $k$ resident blocks, so $n$ requests take $O(n \log k)$ expected time. LRU and LFU need only $O(1)$ per request, and this extra cost was one of the reasons that ARC was proposed later.
- **Space.** $\Theta(k)$: one CRF, one time and one heap entry per resident block.
- **Hit ratio.** On the file system and database traces of the paper, the best $\lambda$ for each trace gave a higher hit ratio than LRU, LFU, [LRU-2](/lru-k/) and [2Q](/two-q/).
- **Worst case.** At $\lambda = 0$, LRFU is LFU, which is not competitive: a block with a high count stays for ever. At $\lambda = 1$ it is LRU, which is $k$-competitive. For $0 < \lambda < 1$ the CRF is bounded, so an unused block loses its place after a bounded time, but the time grows as $\lambda$ goes to 0.

## Properties

- **A spectrum.** One parameter covers LRU, LFU and the policies between them. Small $\lambda$ is close to LFU and large $\lambda$ is close to LRU.
- **Bounded CRF.** For $\lambda > 0$, $C[b] < 1 / (1 - 2^{-\lambda})$, the sum of the geometric series. So the frequency part of the key is bounded. If the last reference of a block is at least $\log_2(1/(1 - 2^{-\lambda})) / \lambda$ time steps older than the last reference of another block, the first block has the smaller CRF, whatever its count.
- **Order that does not change.** Two blocks that are not referenced keep their order, since both CRFs shrink by the same factor. This is what makes a heap work.
- **Aging built in.** Unlike LFU, an old popular block loses its CRF over time when $\lambda > 0$, with no separate aging step.

## Variants and improvements

- **Heap and list.** The bounded CRF means that, for $\lambda > 0$, only the blocks with recent references can be out of LRU order. The paper uses this to keep only a part of the blocks in a heap and the rest in an LRU list, so the cost per request goes from $O(\log k)$ toward $O(1)$ as $\lambda$ grows toward 1.
- **Other weighing functions.** Any $F$ with $F(x + y) = F(x) F(y)$ allows the update from the last value. Other $F$ need the full history of each block.
- **History of evicted blocks.** The CRF of a block that leaves can be kept for a while, as the counts in [MQ](/mq-cache/) are kept in $Q_{out}$, so that a block that comes back keeps its weight.
- **Self-tuning.** The best $\lambda$ depends on the workload. Later work changes $\lambda$ while the cache runs. [ARC](/arc/) solves the same problem with a split between a recency list and a frequency list that moves by itself.
- **LFU-DA and GDSF.** [LFU-DA](/lfu-da/) ages LFU by an inflation value in place of a decay of each reference.

## When to use it

Use LRFU when the workload has both recency and frequency, when the value of $\lambda$ can be tuned on traces, and when $O(\log k)$ per request is acceptable. Buffer caches of file systems and databases were the target of the paper. Prefer ARC or [W-TinyLFU](/w-tinylfu/) when there is no good way to tune $\lambda$, and LRU or a [clock](/clock/) policy when the cost per request must be as low as possible.

## Pitfalls

- **Decaying all blocks at each step.** It is not needed. Store the CRF at the last reference and its time, and decay only when the block is touched or compared.
- **Comparing the stored CRFs.** $C[b]$ values belong to different times. Compare $C[b] \cdot 2^{-\lambda(t - last[b])}$, or $\log_2 C[b] + \lambda \cdot last[b]$, never $C[b]$ alone, except at $\lambda = 0$.
- **Overflow of $2^{\lambda \cdot last}$.** Comparing $C[b] \cdot 2^{\lambda \cdot last[b]}$ overflows after about a thousand steps for $\lambda = 1$ in double precision. Use the logarithm of the key.
- **Rounding at $\lambda = 1$.** After many references in a row, $C[b]$ rounds to 2.0, and its key can equal the key of a block referenced one step later. The tie must go to the older last reference, or the policy is no longer LRU.
- **Keeping the CRF after eviction by mistake.** The basic LRFU starts a block again at 1 when it comes back. Keeping old CRFs is a different policy, and its memory is not bounded by $k$.

## Implementations

## History

Lee, Choi, Kim, Noh, Min, Cho and Kim presented the LRFU spectrum at SIGMETRICS 1999, and the full paper appeared in IEEE Transactions on Computers in 2001. It came after LRU-K (1993) and 2Q (1994), which also tried to use more than the last reference. Megiddo and Modha compared ARC with LRFU in 2003, and they pointed to the cost per request of LRFU and to the need to tune $\lambda$ as reasons for a policy that tunes itself.

## References
