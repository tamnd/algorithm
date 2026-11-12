---
tag: 8186QR
kind: algorithm
slug: shards
name: SHARDS
aliases:
- Spatially Hashed Approximate Reuse Distance Sampling
- SHARDS sampling
area: systems/caching-policies
level: research
summary: "Approximate the LRU miss ratio curve from the requests to a hash-chosen sample of the items, with reuse distances scaled by one over the sampling rate. A fixed-size form uses constant memory."
solves: [miss-ratio-curve-computation]
model: word-ram
complexity:
  vars: {n: the number of requests, R: the sampling rate, s: the number of sampled items kept}
  time: {average: O(n + R n log s)}
  space: {extra: O(s)}
properties: {online: true, deterministic: true, randomized: false, recursive: false}
history:
  year: 2015
  people: [Carl A. Waldspurger, Nohhyun Park, Alexander Garthwaite, Irfan Ahmad]
  note: Waldspurger, Park, Garthwaite and Ahmad presented SHARDS at FAST 2015, for online miss ratio curves of storage caches.
prereqs: [miss-ratio-curve-computation, reuse-distance, hash-function]
see_also: [miss-ratio-curve, mattson-stack-algorithm, fenwick-tree, splay-tree, reservoir-sampling, universal-hashing, binary-heap, lru]
sources:
  - paper: "Carl A. Waldspurger, Nohhyun Park, Alexander Garthwaite and Irfan Ahmad, Efficient MRC construction with SHARDS, 13th USENIX Conference on File and Storage Technologies (FAST 15), 2015, 95-110"
    title: "Waldspurger, Park, Garthwaite and Ahmad, Efficient MRC construction with SHARDS, FAST 2015"
    locator: "Section 2.1 (sampling with hash(L) mod P < T), Section 2.2 (fixed rate, distances scaled by 1/R), Section 2.3 (fixed size, lowering T, histogram rescaling), Section 3 (P = 2^24, MurmurHash3, a splay tree), Section 4.3 (errors on 124 traces and SHARDS_adj)"
  - paper: "Frank Olken, Efficient methods for calculating the success function of fixed space replacement policies, Lawrence Berkeley Laboratory report LBL-12370, 1981"
    title: "Frank Olken, Efficient methods for calculating the success function of fixed space replacement policies, LBL-12370, 1981"
    locator: the exact tree method for LRU stack distances in O(n log m) time, which SHARDS runs on its sample
---

SHARDS is a sampling method that estimates the [miss ratio curve](/miss-ratio-curve/) of an [LRU](/lru/) cache for all sizes. It samples items, not requests: an item $L$ is in the sample when $\mathrm{hash}(L) \bmod P < T$, so the rate is $R = T/P$ and each request to a sampled item is seen. It computes exact [reuse distances](/reuse-distance/) among the sampled items and divides each by $R$. Waldspurger, Park, Garthwaite and Ahmad (FAST 2015) report a median mean absolute error below $0.02$ at $R = 0.001$, with up to about 10,800 times less memory and 204 times less time than an exact method. A fixed-size form keeps at most $s_{\max}$ items by lowering $T$, so it uses constant memory on any trace.

## In plain words

To learn how a city votes, you do not ask every person. You ask a random sample of people, and you ask each of them about all of their choices.

SHARDS does the same with a trace of requests. It picks a sample of the items, say 1 in 1000, with a hash function, so the choice looks random but the same item is always in or always out. It follows every request to the items in the sample and ignores all other requests. Between two uses of a sampled item, it counts how many different sampled items were used. Since only 1 in 1000 items is in the sample, the true count is about 1000 times larger. From these scaled counts it draws the curve, as an exact method would.

## The problem

The input is a trace of $n$ requests to items, and the output is the miss ratio $m(c)$ of an LRU cache of each size $c$, as in [MRC computation](/miss-ratio-curve-computation/). Exact methods take $O(n \log m)$ time and $O(m)$ space for $m$ distinct items. On a storage system with many disks, $m$ is the number of blocks and can be in the billions, so an exact method does not fit beside the cache it measures. The answer may have a small error.

## The algorithm

Fix $P = 2^{24}$ and a hash function. Let $T_L = \mathrm{hash}(L) \bmod P$. The state is the threshold $T$, the sampled items with the time of their last use, a histogram $H$ of scaled distances, and in the fixed-size form a max-heap of the sampled items by $T_L$.

```pseudo id=main
SHARDS-ACCESS(L)
L1  if T_L ≥ T then return                       ▷ L is not in the sample
L2  d ← the number of distinct sampled items used since the last use of L (∞ if none); mark L
L3  if L is new and the sample has more than s_max items then        ▷ fixed size only
L4      remove each item x with T_x = T_max, the largest T_x in the sample
L5      T ← T_max                                   ▷ rescale old counts by T_new / T_old
        if T_L ≥ T then return
L6  if d = ∞ then add 1 to the cold count
L7  else d' ← d · P / T                              ▷ scale by 1/R
L8      add 1 to the bucket of d' in H
MRC(c)
L9  m(c) ← 1 − (sum of H[d'] over d' < c) / (sampled requests)
```

**Fixed rate.** Without lines L3 to L5, $T = \mathrm{round}(R \cdot P)$ stays the same. Line L2 is an exact method on the sampled requests, such as a [Fenwick tree](/fenwick-tree/) over the times of last use, or the [splay tree](/splay-tree/) of the paper's code. The sample holds about $Rm$ items.

**Fixed size.** The method starts with a high rate, such as $R = 1$ or $R = 0.1$, and lowers $T$ each time the sample would grow past $s_{\max}$. The items removed are those with the largest $T_x$, so they would not have been sampled at the new rate, and they are never sampled again. Each count in $H$ was added at some older threshold $T_{\text{old}}$; it is multiplied by $T/T_{\text{old}}$, so that all counts are on the scale of the current rate. The paper does this lazily, with one threshold stored per bucket.

**SHARDS_adj.** The number of sampled requests $N_s$ should be about $nR$, but a popular item that happens to be in the sample, or out of it, moves it a lot. SHARDS_adj adds $nR - N_s$ to the first bucket of the histogram, which removes most of this error.

## Example

Take a trace with 20,000 items and 100,000 requests, each request drawn with probability proportional to $1/i^{0.9}$ for the item of rank $i$. Measure the mean absolute error over the sizes $0, 100, \ldots, 20{,}000$, averaged over four hash salts.

| method | sample | mean absolute error |
|---|---|---|
| fixed rate, $R = 0.1$ | about 2,000 items | about 0.050 |
| fixed rate, $R = 0.1$, SHARDS_adj | about 2,000 items | about 0.008 |
| fixed size, $s_{\max} = 4000$, starting at $R = 1$ | at most 4,000 items | about 0.016 |

The plain fixed rate does poorly here because the 20 most popular items carry a large share of the requests, so the number of sampled requests depends much on which of them the hash picks. The adjustment fixes most of it. At $R = 1$ the result is the exact curve, and with $s_{\max}$ at least the number of items the fixed-size form never lowers $T$, so it is also exact.

In the paper's experiments on 124 real storage traces, fixed-rate SHARDS at $R = 0.001$ had a median mean absolute error below $0.02$. The fixed-size form with $s_{\max} = 8\mathrm{K}$ had a median of $0.0072$ and a worst case of $0.078$, and SHARDS_adj had a median of $0.0027$ and a worst case of $0.017$.

## Correctness

SHARDS is an estimator, so its correctness has two parts: the code computes the stated quantity, and that quantity estimates the right one.

- **Exact on the sample.** The hash decides for each item, not for each request, so the requests seen are the whole trace restricted to the sampled items. The distance that line L2 finds is the number of sampled items among the $D$ distinct items between two uses.
- **Unbiased distances.** If the hash acts as a random function, each of the $D$ items is sampled with probability $R$, independently of the item requested. So the expected sampled distance is $RD$, and dividing by $R$ gives $D$ on average.
- **Exact at rate 1.** With $T = P$ every item is sampled and the curve is the exact LRU curve.
- **Fixed size.** $T$ only falls, so an item still in the sample was in it from its first request, and the sample is always exactly what fixed-rate SHARDS at the current rate would hold.

The full proof is below.

## Complexity

Each request costs one hash and one comparison. Only a fraction $R$ of the requests reaches line L2, which costs $O(\log s)$ in a balanced tree over $s$ sampled items. So the time is $O(n + Rn \log s)$ on average, and the space is $O(s)$ for the sample, plus the histogram. For a fixed rate $s \approx Rm$; for a fixed size $s \le s_{\max}$, a constant. The paper's fixed-size code with $s_{\max} = 8\mathrm{K}$ used about 320 KB for the sample and less than 1 MB in total.

## Properties

- **Online.** One pass, in the order of the trace, so a cache can run it on its live stream.
- **Deterministic for a given hash.** The same trace and salt give the same curve. Changing the salt gives another sample.
- **Spatial sampling.** All requests to an item are kept or all are dropped. Sampling requests at random would break each reuse distance.
- **Subset property.** Lowering $T$ only removes items, so the fixed-size form never needs data it has dropped.
- **LRU only.** The distances describe LRU. For other policies, the same sample can feed a small simulation of each cache size.

## Variants and improvements

- **Fixed rate and fixed size**, as above. The fixed size bounds the memory; the fixed rate is simpler and is unbiased when $R$ is constant.
- **SHARDS_adj**, the correction of the first bucket.
- **Miniature simulations.** The same hash sample, run through a small simulation of any policy with the cache size scaled by $R$, gives curves for policies without the stack property. Waldspurger and others extended SHARDS this way in later work.
- **Other estimators.** Counter Stacks estimates the distances with probabilistic counters, and the AET model uses only reuse times; see [MRC computation](/miss-ratio-curve-computation/).

## When to use it

Use SHARDS when an LRU curve is needed online, for a cache of many items, with a memory budget far below the number of items: storage arrays, hypervisor caches and key-value caches that resize or partition their memory from time to time. For a short trace offline, an exact tree method is simple and fast enough. For policies other than LRU, use the sample to drive small simulations.

## Pitfalls

- **Too small a sample.** With few items, a few popular ones decide the result. Use SHARDS_adj, a higher rate, or a larger $s_{\max}$.
- **A poor hash.** If the hash is correlated with the access pattern, for example the identity on block numbers, the sample is not random. Use a good hash such as MurmurHash3, as the paper does, with a salt.
- **Forgetting to rescale.** In the fixed-size form, counts from different rates must be put on one scale, or the curve is biased toward the early part of the trace.
- **Byte sizes.** With objects of different sizes, scale the sum of the sizes, not the count of items, and use a cache size in bytes.
- **Short traces.** The cold misses of the sample are a noisy estimate of the cold misses of the trace.

## Implementations

## History

Mattson and others gave one-pass stack processing in 1970, and Bennett and Kruskal and then Olken made LRU stack distances fast with trees. These methods are exact but need memory in proportion to the number of distinct items, which kept them out of production storage systems. Waldspurger, Park, Garthwaite and Ahmad, at the storage startup CloudPhysics, presented SHARDS at FAST 2015. Their key choice was to sample by a hash of the location, which keeps every reuse among sampled items. They gave the fixed-rate and fixed-size forms, showed that $R = 0.001$ is accurate on 124 real traces, and built it on the PARDA code with a splay tree.

## References
