---
tag: CPEY4J
kind: algorithm
slug: mattson-stack-algorithm
name: Mattson's stack algorithm
aliases:
- LRU stack simulation
- one-pass stack simulation
area: systems/caching-policies
level: advanced
summary: "One pass over a trace keeps a stack of items ordered by priority. The depth of each request is its stack distance, and their histogram gives the hits of every cache size."
model: word-ram
complexity:
  vars: {n: the number of requests, m: the number of distinct items}
  time: {worst: O(n m)}
  space: {extra: Θ(m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1970
  people: [R. L. Mattson, J. Gecsei, D. R. Slutz, I. L. Traiger]
  note: Mattson, Gecsei, Slutz and Traiger at IBM defined stack algorithms and showed that one pass over a trace gives the miss ratio of every memory size.
prereqs: [inclusion-property, reuse-distance]
see_also: [stack-algorithms, miss-ratio-curve, miss-ratio-curve-computation, shards, belady-optimal, lru, belady-anomaly, fenwick-tree]
sources:
  - paper: doi:10.1147/sj.92.0078
    title: "R. L. Mattson, J. Gecsei, D. R. Slutz and I. L. Traiger, Evaluation techniques for storage hierarchies, IBM Systems Journal 9(2) (1970), 78-117"
    locator: stack algorithms, the stack update for a priority list, the distance distribution, and the hit ratio of all capacities from one pass, for LRU and for OPT
  - paper: doi:10.1147/rd.194.0353
    title: "B. T. Bennett and V. J. Kruskal, LRU stack processing, IBM Journal of Research and Development 19(4) (1975), 353-357"
    locator: LRU stack distances in O(log n) time per reference with a tree over the positions of last references
  - paper: doi:10.1145/363011.363155
    title: "L. A. Belady, R. A. Nelson and G. S. Shedler, An anomaly in space-time characteristics of certain programs running in a paging machine, Communications of the ACM 12(6) (1969), 349-353"
    locator: the FIFO anomaly, which shows that FIFO cannot be simulated by a stack
---

Mattson's stack algorithm computes the number of hits of a cache of every size $k$ in one pass over a trace. It works for each *stack algorithm*, a replacement policy whose cache of size $k$ is always contained in its cache of size $k + 1$ (the [inclusion property](/inclusion-property/)). For such a policy, the caches of all sizes are the top parts of one list, the *stack*. The algorithm keeps this list as the trace goes by. The depth of the requested item in the list just before the request is its *stack distance* $d$, and the request is a hit exactly in the caches of size $k \ge d$. So the histogram of the distances gives the whole hit curve, and the [miss ratio curve](/miss-ratio-curve/), at the cost of one simulation. For LRU, the stack distance is the [reuse distance](/reuse-distance/) plus 1.

## In plain words

To find out how well a cache of each size would do on a recorded trace, you could run the trace once for each size. That is slow when there are thousands of sizes to try.

For LRU there is a shortcut. Keep one list of all items seen so far, with the most recently used item on top. When an item is requested, note how deep it sits in the list, then move it to the top. An LRU cache that holds $k$ items holds exactly the top $k$ items of this list. So if the item was at depth 5, every cache with room for 5 or more items would have had it, and every smaller cache would have missed. Count how often each depth occurs, and you know the hits for every size at once.

## The problem

The input is a trace $\sigma_1 \cdots \sigma_n$ and a stack algorithm $P$, given by a priority rule. The output is, for each $k \ge 1$, the number $H(k)$ of hits of $P$ with a cache of $k$ items from an empty start. The page uses two priority rules:

- **LRU.** Item $a$ has priority over item $b$ if $a$ was used more recently.
- **OPT.** Item $a$ has priority over item $b$ if the next request for $a$ comes sooner. On a tie, both are never requested again, and the item already in place keeps its place. Mattson and others showed that this rule gives Belady's [MIN](/belady-optimal/) for every size at once.

## The algorithm

The stack $S$ is a list with $S[1]$ on top. $\mathrm{PRI}(a, b)$ is true if $a$ has priority over $b$ under the rule.

```pseudo id=main
STACK-DISTANCES(σ, PRI)                       ▷ σ = σ_1 .. σ_n
L1  S ← an empty list; hist ← an array of zeros
L2  for t ← 1 to n do
L3      y ← σ_t
L4      d ← the position of y in S, or ∞ if y ∉ S
L5      hist[d] ← hist[d] + 1                      ▷ the stack distance of request t
L6      update the priority data of y for time t
L7      if d = 1 then continue
L8      if S is empty then S[1] ← y; continue
L9      c ← S[1]; S[1] ← y                         ▷ y goes on top, the old top is carried down
L10     for i ← 2 to (d − 1 if d < ∞, else |S|) do
L11         if not PRI(S[i], c) then swap S[i] and c   ▷ the item of lower priority goes on down
L12     if d < ∞ then S[d] ← c else append c to S
L13 return H(k) = hist[1] + ... + hist[k] for each k
```

Line L6 records the time of the last use for LRU, or the time of the next use for OPT. Lines L9 to L12 are Mattson's update. At each depth $i$, the item in place and the carried item compete; the item with priority stays at depth $i$, and the other is carried to depth $i + 1$. The carried item ends at the old depth of $y$, or at the bottom if $y$ is new. For LRU the old top always has priority over the items below it, so the update just moves $y$ to the top and shifts the items above its old position down by one.

## Example

Take the trace $a\,b\,c\,a\,d\,b\,a\,c\,d\,a$ and the LRU rule. The stack is listed from the top.

| $t$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| request | $a$ | $b$ | $c$ | $a$ | $d$ | $b$ | $a$ | $c$ | $d$ | $a$ |
| distance | $\infty$ | $\infty$ | $\infty$ | 3 | $\infty$ | 4 | 3 | 4 | 4 | 3 |
| stack after | $a$ | $ba$ | $cba$ | $acb$ | $dacb$ | $bdac$ | $abdc$ | $cabd$ | $dcab$ | $adcb$ |

The histogram has three requests at distance 3 and three at distance 4. So LRU has $H(1) = H(2) = 0$, $H(3) = 3$, and $H(k) = 6$ for $k \ge 4$. One simulation of LRU per size gives the same numbers.

The OPT rule on the same trace gives the distances $\infty, \infty, \infty, 2, \infty, 3, 2, 4, 3, 2$, so MIN has $H(1) = 0$, $H(2) = 3$, $H(3) = 5$ and $H(k) = 6$ for $k \ge 4$. MIN gets 3 hits with 2 items, where LRU gets none.

## Correctness

The proof in [the correctness file](proofs/correctness.md) treats the LRU rule. It shows the invariant that after each request, $S$ lists the distinct items seen so far in order of their last use, most recent first. Lines L9 to L12 keep the invariant: the carried item is always the next item of the old order, so the update moves $y$ to the top and leaves the others in order. Then it shows by induction on $t$ that the LRU cache of size $k$ is exactly the top $\min(k, |S|)$ items of $S$. So request $t$ hits in the cache of size $k$ if and only if $d \le k$, and line L13 counts the hits of each size. For the OPT rule, the correctness of the same update is the theorem of Mattson and others; the tests compare its hit curve with one MIN simulation per size.

## Complexity

- **Time.** Line L4 searches the list, and lines L9 to L12 walk down to depth $d$. Each request costs $O(d) \subseteq O(m)$, so the pass costs $O(n m)$ in the worst case, where $m$ is the number of distinct items. On traces with good locality most distances are small and the pass is fast.
- **Faster LRU.** For LRU only the distance matters, not the list. Bennett and Kruskal (1975) mark the time of the last use of each item in a tree over the times, so that the distance is the number of marks after the previous use of $y$. With a [Fenwick tree](/fenwick-tree/) or a balanced search tree each request takes $O(\log n)$ time, so the pass takes $O(n \log n)$ time and $O(n)$ space, see [reuse distance](/reuse-distance/).
- **Space.** The list holds each distinct item once, so $\Theta(m)$, plus the histogram.
- **Sampling.** For traces of billions of requests over millions of items, [SHARDS](/shards/) runs the same computation on the requests whose key hashes into a small fixed fraction, and scales the result. See [miss ratio curve computation](/miss-ratio-curve-computation/).

## Properties

- **One pass for all sizes.** The cost is about that of one simulation, whatever the number of sizes.
- **Only for stack algorithms.** It needs the inclusion property. LRU, MIN and an LFU that counts all past uses are stack algorithms. FIFO and CLOCK are not, and [Belady's anomaly](/belady-anomaly/) shows that their hit curve need not even be monotone.
- **Online.** The LRU form reads the trace once, from the start, and can run while the trace is produced. The OPT form needs the time of the next use, so it needs a backward pass first.
- **Fully associative.** The method assumes that any item can go anywhere. For a set-associative cache with LRU in each set, run one stack per set; then one pass gives all associativities for a fixed number of sets.

## Variants and improvements

- **Tree-based LRU distances.** Bennett and Kruskal's method above, and later versions with balanced trees keyed by the time of the last use.
- **Approximate distances.** Methods that keep the counts of distances only up to a fixed relative error trade a little precision for much less time and space, for program analysis on long traces.
- **Sampling.** SHARDS samples items by a hash of the key, so that each sampled item keeps its full history; the distances of the sample, scaled by the sampling rate, estimate the distances of the trace.
- **Other policies.** Policies that are not stack algorithms, such as ARC or CLOCK, need one simulation per size or approximate models of their curve.

## When to use it

Use it when a recorded trace must be evaluated for many cache sizes: to size a page cache, a buffer pool or a key-value cache, to choose a processor cache size in a simulator, or to draw a miss ratio curve. Use the LRU form with a tree for long traces, and the list form when $m$ is small or when the stack itself is wanted. Use the OPT form to draw the lower envelope against which other policies are judged. Do not use it for a policy that is not a stack algorithm.

## Pitfalls

- **Depth from 0 or from 1.** Here the top has depth 1, so a request at distance $d$ hits when $k \ge d$. Reuse distance counts the items in between, so it is $d - 1$, and a cache of size $k$ hits when the reuse distance is less than $k$. Mixing the two shifts the curve by one size.
- **The wrong update for OPT.** Putting the new item on top and sorting the rest by next use does not give MIN, because a cache cannot hold an item that it evicted earlier and that has not been requested since. On $a\,b\,c\,a\,b$ with $k = 2$, that order puts $a$ at depth 2 for the second $a$ and $b$ at depth 2 for the second $b$, which claims 2 hits, but MIN has only 1. The update of lines L9 to L12, with the carried item, is needed.
- **Ties in OPT.** Items never requested again tie. A tie rule that depends on the cache size can break inclusion; the rule "the item in place stays" does not.
- **Cold start.** First requests have distance $\infty$ and are misses for every size. Report whether the curve includes them.

## Implementations

## History

Mattson, Gecsei, Slutz and Traiger published the method in 1970, in their study of storage hierarchies at IBM. They defined stack algorithms by the inclusion property, showed that LRU and the optimal algorithm OPT are stack algorithms, and gave the one-pass computation of the distance distribution, from which the miss ratio of each memory size follows. A year before, Belady, Nelson and Shedler had shown that FIFO can have more faults with more memory, which the new theory explained. Bennett and Kruskal reduced the cost per reference for LRU to logarithmic time in 1975. Sampling methods such as SHARDS (2015) made the computation cheap enough to run online in production caches.

## References
