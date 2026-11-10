---
tag: MV8B8B
kind: algorithm
slug: chain-sampling
name: Chain sampling
aliases:
- chain-sample
- chain sample
area: online-and-streaming/sliding-windows
level: advanced
summary: Keeps a uniform random sample of the last W items of a stream by choosing, for the sampled item, a successor uniform among the items that arrive before it expires, and chaining these successors.
solves: [sliding-window-sampling]
model: sliding-window-model
complexity:
  vars: {W: the window size in items}
  time: {worst: O(1)}
  space: {expected: O(1), worst: O(W)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2002
  people: [Brian Babcock, Mayur Datar, Rajeev Motwani]
  note: Chain-sample is the first of the two methods in the SODA 2002 paper that introduced sampling from a moving window. Braverman, Ostrovsky and Zaniolo (PODS 2009) later gave a method with a deterministic O(k) memory bound.
prereqs: [reservoir-sampling, count-based-window, linearity-of-expectation]
see_also: [sliding-window-sampling, reservoir-sampling, sliding-window-model, count-based-window, time-based-window, random-sampling, priority-sampling, geometric-distribution]
sources:
  - paper: "Brian Babcock, Mayur Datar and Rajeev Motwani, Sampling from a moving window over streaming data, SODA 2002"
    locator: pages 633 to 634, Section 2, Sequence-Based Windows (the chain-sample rule, the recurrence for the expected chain length with T[n] < e, and the O(log n) high-probability bound)
  - paper: "Vladimir Braverman, Rafail Ostrovsky and Carlo Zaniolo, Optimal sampling from sliding windows, PODS 2009"
    locator: the introduction (the randomized memory bounds of chain-sample, and O(k) deterministic memory for sequence-based windows)
  - paper: doi:10.1145/3147.3165
    title: Jeffrey S. Vitter, Random sampling with a reservoir, ACM Transactions on Mathematical Software 11(1), 1985
    locator: pages 37 to 57, Algorithm R, the reservoir rule that chain-sample extends
---

Chain sampling keeps one uniform random item from the last $W$ items of a stream, a [count-based window](/count-based-window/), in $O(1)$ expected memory. When item $i$ becomes the sample, the algorithm also picks the index of its replacement, uniform among $i + 1, \ldots, i + W$, the items that are in the window when item $i$ expires; the replacement picks its own replacement when it arrives, and so on, which builds a chain. Babcock, Datar and Motwani gave it in 2002 as the fix for [reservoir sampling](/reservoir-sampling/), which cannot drop an expired sample. The expected chain length is $(1 + 1/W)^W - 1 < e - 1$ words in the sliding window model, and $k$ independent chains give a sample of size $k$ with replacement.

## In plain words

You watch a long line of items go by, and at any moment you want one item picked fairly from the most recent ones, say the last thousand. A plain lottery over the whole past fails, because the item you hold gets too old and must be dropped, and the items that could replace it are gone. Chain sampling plans ahead. When an item wins, you also choose, at random, which future item will take its place when it gets too old. When that future item arrives, you keep it and choose its own heir. So you hold a short chain of heirs. When the current winner gets too old, the next in the chain takes over. On average the chain holds fewer than two items.

## The problem

The stream is $\sigma_1, \sigma_2, \ldots$, read one item per step. At step $t$ the window is the last $\min(t, W)$ items, $\sigma_{t-W+1}, \ldots, \sigma_t$ for $t \ge W$. The task is to output, after every step, an item $\sigma_{S_t}$ whose index $S_t$ is uniform on the window: $\Pr[S_t = s] = 1/\min(t, W)$ for each index $s$ in the window. The bound holds for every fixed stream; the only randomness is the algorithm's. This is the single-item case of [sliding-window sampling](/sliding-window-sampling/).

## The algorithm

The state is a chain $C$ of pairs (index, item), with $C[0]$ the sample, and the index $\mathit{want}$ of the next item to append. RANDOM$(1..m)$ returns a uniform integer in $1, \ldots, m$, independent of all other calls.

```pseudo id=main
STEP(x)                                    ▷ the next item of the stream
L1  t ← t + 1
L2  if t = want then                       ▷ the chosen successor arrives
L3      append (t, x) to C; want ← t + RANDOM(1..W)
L4  if C is not empty and C[0].index = t − W then
L5      remove C[0]                        ▷ the sample expires; its successor takes over
L6  else if RANDOM(1..min(t, W)) = 1 then  ▷ the new item wins
L7      C ← [(t, x)]; want ← t + RANDOM(1..W)
SAMPLE()
L8  return C[0].item
```

Lines L2 and L3 extend the chain when the chosen successor of its last element arrives. Line L5 replaces an expired sample by its successor, which has arrived by then because its index is at most $(t - W) + W = t$. Lines L6 and L7 are the reservoir rule: the new item becomes the sample with probability $1/\min(t, W)$, and the old chain is dropped, since none of its items can be used again. The coin of line L6 is tossed only in a step where the sample did not expire. At $t = 1$ the coin always wins.

## Example

$W = 3$ and the stream a, b, c, ..., j. One run with seeded choices gives this table. The column $C$ lists the items of the chain after the step, the sample first.

| $t$ | item | $C$ | want | what happened |
|---|---|---|---|---|
| 1 | a | a | 2 | a wins; its successor is item 2 |
| 2 | b | a, b | 3 | b is appended; its successor is item 3 |
| 3 | c | a, b, c | 4 | c is appended; the coin fails |
| 4 | d | b, c, d | 7 | d is appended; a expires and b takes over |
| 5 | e | c, d | 7 | b expires and c takes over |
| 6 | f | d | 7 | c expires and d takes over |
| 7 | g | g | 9 | g is appended; d expires and g takes over |
| 8 | h | g | 9 | the coin fails |
| 9 | i | i | 12 | the coin wins: i is the sample, the chain restarts |
| 10 | j | j | 13 | the coin wins again |

The chain reached three items here because the successors 2, 3 and 4 were the nearest possible. The expected length for $W = 3$ is $(4/3)^3 - 1 = 37/27 \approx 1.37$.

## Correctness

The sample index $S_t$ changes in only two ways. If the sample expires, $S_t = S_{t-1} + D$, where $D$ is the offset drawn when that item joined the chain. Otherwise the new item wins with probability $1/\min(t, W)$. The run up to step $t - 1$ never reads an offset of an item that is still in the window at step $t - 1$, so the offset $D$ of the expiring sample is independent of the event that it is the sample. By induction on $t$, with $\Pr[S_{t-1} = t - W] = 1/W$:

$$\Pr[S_t = u] = \frac{1}{W} \cdot \frac{1}{W} + \frac{1}{W}\Bigl(1 - \frac{1}{W}\Bigr) = \frac{1}{W} \quad (t - W < u < t), \qquad \Pr[S_t = t] = \frac{1}{W} \cdot \frac{1}{W} + \Bigl(1 - \frac{1}{W}\Bigr)\frac{1}{W} = \frac{1}{W}.$$

For $t \le W$ nothing expires and the rule is the reservoir rule, which gives $1/t$. The algorithm never looks at the items, so the sample is a uniform item of the window for every stream. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each step does a constant number of operations on the chain, a [deque](/deque/), so the time is $O(1)$ per item in the worst case; dropping the old chain in line L7 is $O(1)$ amortized if the memory must be freed item by item, since each item is freed once.

The memory is the chain. Given the sample's index $s$ with $m = t - s$ newer items in the window, the chain has the $k + 1$ elements $s, s + D_1, \ldots$ with $D_1 + \cdots + D_k \le m$, and the offsets are independent and uniform on $1, \ldots, W$. So

$$\Pr[|C| > k \mid m] = \binom{m}{k} W^{-k} < \frac{1}{k!}, \qquad \mathbb{E}\bigl[|C| \mid m\bigr] = \Bigl(1 + \frac{1}{W}\Bigr)^m.$$

Averaging over the uniform $m \in \{0, \ldots, W - 1\}$ gives, for $t \ge W$,

$$\mathbb{E}|C| = \Bigl(1 + \frac{1}{W}\Bigr)^W - 1 < e - 1 \approx 1.718,$$

and $\frac{W}{t}\bigl((1 + 1/W)^t - 1\bigr)$, which is smaller, for $t < W$. The tail $1/k!$ means that the chain has $O(\log W / \log \log W)$ elements with probability $1 - W^{-c}$, for any constant $c$. The worst case is $W$ elements, when every offset is 1. The proofs are in [the complexity proof](proofs/complexity.md). Babcock, Datar and Motwani state the bounds as $T[n] < e$ for the oldest position and $O(\log n)$ with high probability.

| measure | bound | kind |
|---|---|---|
| time per item | $O(1)$ | worst case |
| memory | $(1 + 1/W)^W - 1 < e - 1$ items | expected, proved here |
| memory | $O(\log W / \log \log W)$ items | with probability $1 - W^{-c}$, proved here |
| memory | $W$ items | worst case |
| $k$ samples | $k$ chains, $O(k)$ expected | with replacement |

## Properties

- **Online and one pass.** Each item is read once; the window size $W$ must be known in advance.
- **Uniform at every step, not independent across steps.** The samples at steps $t$ and $t + 1$ are the same item with high probability, as with reservoir sampling.
- **Value-oblivious.** The choices do not depend on the items, so an adversary that picks the stream in advance cannot bias the sample.
- **Count-based only.** The offsets are drawn from a range of exactly $W$ indices, so the method needs to know which items will be in the window when the sample expires. A [time-based window](/time-based-window/) does not tell this in advance.

## Variants and improvements

- **Coin at every step.** Toss the coin of line L6 in every step, also after an expiry, but draw each successor uniform on $i + 1, \ldots, i + W - 1$ (for $W \ge 2$). After an expiry the promoted item is uniform on $W - 1$ indices, and the coin then gives the new item $1/W$ and each of the others $\frac{1}{W - 1}(1 - \frac{1}{W}) = \frac{1}{W}$. Both versions give a uniform sample.
- **Sample of size $k$.** Run $k$ independent chains for a sample with replacement. Babcock, Datar and Motwani get a sample without replacement by over-sampling: keep enough extra chains that, with high probability, $k$ distinct items appear.
- **Priority sampling for time windows.** For a time-based window, the same paper gives each item a random priority and keeps the items that no later item beats in priority; the sample is the active item of highest priority. The kept items form the right spine of a [treap](/treap/), with expected size $H_n$ for $n$ active items. See [sliding-window sampling](/sliding-window-sampling/).
- **Deterministic memory.** Braverman, Ostrovsky and Zaniolo (PODS 2009) split the stream into blocks of $W$ items and keep a reservoir sample of the last full block and of the current block, which gives $O(k)$ memory in the worst case for sequence-based windows. See [sliding-window sampling](/sliding-window-sampling/).

## When to use it

Use chain sampling for one uniform item, or a few with replacement, from the last $W$ items of a stream, when expected memory of two items per sample is enough. If a hard memory bound is needed, the block method of Braverman, Ostrovsky and Zaniolo is as simple and has a worst-case bound. If the window is defined by time, use priority sampling. If the whole window fits in memory, store it in a [circular buffer](/circular-buffer/) and draw a random index.

## Pitfalls

- **Tossing the coin at an expiry step with successors over $W$ indices.** The short paper does not fix the order of the events in a step where the sample expires. If the new item gets its $1/W$ chance after the expired sample has already been replaced by a successor drawn from $i + 1, \ldots, i + W$, the newest item is chosen too often: for $W = 2$, at step 3 the sample is item 3 with probability $5/8$ and item 2 with probability $3/8$. Use one of the two orders above.
- **Successor range off by one.** The successor of item $i$ must be uniform over the indices that are in the window at step $i + W$, which are $i + 1, \ldots, i + W$. A range that starts at $i$ or ends at $i + W - 1$ (with the coin rule of line L6) breaks uniformity.
- **Keeping the old chain after a win.** When the new item wins in line L7, every item of the old chain is older than the new sample and can never be used again. Keeping them only wastes memory, and the memory bound above no longer holds.
- **Correlated chains.** For $k$ samples, each chain needs its own random choices. Chains that reuse the same choices hold the same item, and the sample of size $k$ is one item repeated.

## Implementations

## History

Babcock, Datar and Motwani introduced the problem of sampling from a moving window in a two-page paper at SODA 2002, with chain-sample for sequence-based windows and priority-sample for timestamp-based windows. They extended Vitter's reservoir sampling. Braverman, Ostrovsky and Zaniolo pointed out in 2009 that the memory bounds of chain-sample hold only in expectation or with high probability, and gave methods with deterministic bounds.

## References
