---
tag: Z8FFSE
kind: problem
slug: sliding-window-sampling
name: Sliding window sampling
aliases:
- sampling from a moving window
- uniform sample of a window
- priority sampling over a window
area: online-and-streaming/sliding-windows
level: advanced
summary: Keep a uniform random sample of the items in the current window of a stream; reservoir sampling fails because samples expire, and chain, priority and bucket methods fix it.
prereqs: [reservoir-sampling, sliding-window-model]
see_also: [chain-sampling, reservoir-sampling, sliding-window-maximum, count-based-window, time-based-window, weighted-reservoir-sampling, forward-decay]
sources:
  - paper: "Brian Babcock, Mayur Datar and Rajeev Motwani, Sampling from a moving window over streaming data, SODA 2002"
    locator: pages 633 to 634, chain sampling for count-based windows and priority sampling for time-based windows, with O(k) and O(k log n) expected memory
  - paper: "Vladimir Braverman, Rafail Ostrovsky and Carlo Zaniolo, Optimal sampling from sliding windows, PODS 2009"
    locator: Section 2, the bucket method for count-based windows with O(k) memory in the worst case; the timestamp-based case with O(k log n) memory, and the matching lower bound
  - paper: doi:10.1145/3147.3165
    title: Jeffrey S. Vitter, Random sampling with a reservoir, ACM Transactions on Mathematical Software 11(1), 1985
    locator: pages 37 to 57, reservoir sampling over a whole stream
---

The sliding window sampling problem asks for a uniform random sample of the items in the current window of a stream: the last $W$ items, or the items of the last $T$ time units. [Reservoir sampling](/reservoir-sampling/) does not solve it, because a sampled item expires and the reservoir has discarded every item that could replace it. Babcock, Datar and Motwani (2002) gave [chain sampling](/chain-sampling/) for count-based windows and priority sampling for time-based windows, with $O(k)$ and $O(k \log n)$ expected memory for $k$ samples, where $n$ is the number of items in the window. Braverman, Ostrovsky and Zaniolo (2009) reached the same bounds in the worst case with a bucket method, and showed that they are optimal.

## In plain words

You want to pick one item at random from the last thousand items of a stream, and keep that pick fair at every moment. The classic trick for a whole stream keeps one item and replaces it by the newest item with a falling probability. In a window this breaks: sooner or later the kept item gets too old, and by then all the other candidates are gone. The fixes keep a few spare candidates. One method gives each item a random ticket and keeps the items whose ticket beats every later ticket; the oldest of them that is still in the window holds the best ticket in the window, and is a fair pick. Another method cuts the stream into blocks of a thousand and keeps one fair pick per block.

## Definition

The input is a stream of items, with timestamps $\tau_1 \le \tau_2 \le \cdots$ in the time-based case, a window, and a sample size $k \ge 1$. At any query, let $V$ be the set of positions in the window, with $n = |V|$.

- **One sample.** Output an item $x_s$ with $\Pr[s = i] = 1/n$ for every $i \in V$.
- **$k$ samples with replacement.** Output $k$ positions that are independent and uniform on $V$; this is $k$ independent copies of the one-sample problem.
- **$k$ samples without replacement.** Output a set $S \subseteq V$ with $|S| = \min(k, n)$, uniform over all such sets.

The probabilities are over the random choices of the algorithm only, for every fixed stream. The cost measures are the memory in items, worst case or expected, and the time per item.

## Variants

- **Count-based windows**, the last $W$ items, where $n = \min(t, W)$ is known.
- **Time-based windows**, where $n$ changes and is unknown, and many items may arrive with the same timestamp.
- **Weighted samples.** Sample in proportion to weights. With weights that grow over time, this gives a decayed sample, see [forward decay](/forward-decay/).
- **Bernoulli samples.** Keep each item with a fixed probability $q$; this needs no repair on expiry, but the sample size is random, about $qn$.
- **Distinct items.** Sample uniformly among the distinct values in the window, which needs other methods.

## Examples

**Why reservoir sampling fails.** Run reservoir sampling with $k = 1$ over the whole stream: item $i$ replaces the sample with probability $1/i$. After $t$ items, the sample is uniform on all $t$ items, so it lies in a window of the last $W$ items only with probability $W/t$, which tends to 0. When the sample expires, the discarded items cannot be brought back. Simple repairs are biased: replacing an expired sample by the newest item puts too much weight on new items, as the [chain sampling](/chain-sampling/) page shows for the closely related wrong order of its steps.

**Priority sampling.** A time-based window of length $T = 3$. The items arrive as (timestamp, item, priority): $(1, a, 0.6)$, $(2, b, 0.9)$, $(2, c, 0.4)$, $(3, d, 0.7)$, $(5, e, 0.2)$.

| step | deque after the step | sample |
|---|---|---|
| insert $a$ | $a\,(0.6)$ | |
| insert $b$ | $b\,(0.9)$ | |
| insert $c$ | $b\,(0.9), c\,(0.4)$ | |
| insert $d$ | $b\,(0.9), d\,(0.7)$ | |
| query $t = 3$ | $b\,(0.9), d\,(0.7)$ | $b$ |
| insert $e$ | $b\,(0.9), d\,(0.7), e\,(0.2)$ | |
| query $t = 5$ | $d\,(0.7), e\,(0.2)$ | $d$ |

At $t = 5$ the window $(2, 5]$ holds $d$ and $e$, and $b$ has expired. The sample $d$ has the highest priority among them, and $c$, which was removed by $d$, could never have won: it was older and had a lower priority.

## Known algorithms

**Priority sampling (Babcock, Datar and Motwani).** Give each item an independent priority, uniform on $[0, 1)$. The sample is the item of highest priority in the window. A deque $D$ keeps the items whose priority is higher than the priority of every later item; it is the [sliding window maximum](/sliding-window-maximum/) structure applied to the priorities.

```pseudo id=main
INSERT(τ, x)
L1  p ← a uniform random number in [0, 1)
L2  while D is not empty and priority(back(D)) < p do pop the back of D
L3  push (τ, x, p) at the back of D
SAMPLE(t)
L4  while D is not empty and time(front(D)) ≤ t − T do pop the front of D
L5  if D is empty then return none
L6  return the item of front(D)
```

*Correctness.* By the invariant of the sliding window maximum, the front of $D$ after line L4 is the item of highest priority among the items in the window. The priorities are independent, identically distributed and continuous, so ties have probability 0, and by symmetry each of the $n$ items in the window has the highest priority with probability $1/n$. The priorities do not depend on the items or the timestamps, so the sample is uniform for every stream.

*Memory.* The item $j$ places from the end of the window is in $D$ exactly when its priority is the highest of the last $j$ items, which has probability $1/j$. So $D$ holds on average $H_n = 1 + \frac12 + \cdots + \frac1n \le 1 + \ln n$ items of the window. Before the expiry at line L4, $D$ may also hold expired items, which form a prefix; the same bound applies to the items since the last query. In the worst case $D$ holds all $n$ items, when the priorities decrease. For $k$ samples without replacement, the sample is the $k$ items of highest priority, and the structure keeps each item that has fewer than $k$ later items of higher priority; its expected size is $O(k \log n)$.

*Time.* Each item is pushed and popped once, so the time is $O(1)$ amortized per item.

**Chain sampling.** For count-based windows, [chain sampling](/chain-sampling/) keeps, for the current sample, a chain of successors chosen in advance. Its chain has on average fewer than $e - 1 \approx 1.72$ items for one sample, and more than $O(\log W / \log \log W)$ items only with a probability that is polynomially small in $W$; the proofs are on its page.

**Buckets (Braverman, Ostrovsky and Zaniolo).** For a count-based window of size $W$, cut the stream into buckets of $W$ consecutive items. Keep $R_{\text{prev}}$, a uniform sample of the last complete bucket, and $R_{\text{cur}}$, a [reservoir sample](/reservoir-sampling/) of the $j$ items of the current, partial bucket. If $j = 0$, the window is the last complete bucket, and $R_{\text{prev}}$ is the answer. Otherwise the window is the last $W - j$ items of the previous bucket and the $j$ items of the current one. Output $R_{\text{prev}}$ if it is still in the window, and $R_{\text{cur}}$ otherwise.

*Proof of uniformity.* The two samples are independent. A position $i$ of the previous bucket that is still in the window is the output exactly when $R_{\text{prev}} = i$, with probability $1/W$. A position $i$ of the current bucket is the output exactly when $R_{\text{prev}}$ has expired, with probability $j/W$, and $R_{\text{cur}} = i$, with probability $1/j$; the product is $1/W$. $\square$

The memory is two items and a few counters in the worst case, and $k$ independent copies give $k$ samples with replacement in $O(k)$ memory. Braverman, Ostrovsky and Zaniolo extend the method to samples without replacement with $O(k)$ memory, and to time-based windows with $O(k \log n)$ memory in the worst case, which matches their lower bound.

| method | window | memory for $k$ samples | bound type |
|---|---|---|---|
| store the window | both | $n$ items | worst case |
| chain sampling | count-based | $O(k)$ | expected, $O(k \log W / \log \log W)$ with high probability |
| priority sampling | time-based | $O(k \log n)$ | expected and with high probability |
| buckets | count-based | $O(k)$ | worst case |
| buckets with a smooth-histogram structure | time-based | $O(k \log n)$ | worst case, optimal |

The priority-sampling and bucket bounds for one sample and $k$ samples with replacement are proved on this page and on the chain sampling page; the bounds for samples without replacement and for time-based buckets are cited from the two papers.

## Bounds

For time-based windows, Braverman, Ostrovsky and Zaniolo prove that $\Omega(k \log n)$ memory is necessary, so priority sampling is optimal in expectation and their method is optimal in the worst case. For count-based windows, $k$ samples need $\Omega(k)$ memory to store them, and the bucket method meets this bound.

## Reductions

- **To the sliding window maximum.** Priority sampling is the sliding window maximum of random priorities; any structure for that problem gives a sampler with the same memory.
- **Many samples with replacement.** Run $k$ independent one-sample structures.
- **Window estimates from samples.** A uniform sample of the window gives unbiased estimates of window means and of the fraction of items with a property, which is how samples serve approximate query answering.

## Applications

Approximate answers to aggregate queries over recent data, load shedding in stream systems that cannot process every item, recent-data monitoring in networks where only sampled packets are inspected, and training sets for models that must follow a drifting distribution.

## References
