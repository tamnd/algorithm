---
tag: 8720DK
kind: algorithm
slug: weighted-reservoir-sampling
name: Weighted reservoir sampling
aliases:
- A-ExpJ
- A-Res
- Efraimidis-Spirakis algorithm
- Efraimidis-Spirakis sampling
- weighted random sampling with a reservoir
area: randomized/sampling
level: advanced
summary: Keeps the k items with the largest keys u^(1/w) from a weighted stream, which gives weighted sampling without replacement in one pass; A-ExpJ jumps over items that cannot enter.
solves: [weighted-sampling, stream-sampling]
model: word-ram
complexity:
  vars: {n: the number of items in the stream, k: the sample size}
  time: {worst: "O(n log k)"}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2006
  people: [Pavlos S. Efraimidis, Paul G. Spirakis]
  note: Efraimidis and Spirakis published the key rule u^(1/w), Algorithm A-Res and the jump method A-ExpJ in Information Processing Letters in 2006.
prereqs: [reservoir-sampling, weighted-sampling, binary-heap]
see_also: [priority-sampling, algorithm-l, vitter-reservoir-skip, gumbel-max-trick, probability-proportional-to-size-sampling, top-k-selection, stream-sampling]
sources:
  - paper: doi:10.1016/j.ipl.2005.11.003
    title: Pavlos S. Efraimidis and Paul G. Spirakis, Weighted random sampling with a reservoir, Information Processing Letters 97(5), 181 to 185, 2006
    locator: the key rule and its proof, Algorithm A-Res, and Algorithm A-ExpJ with exponential jumps
  - paper: doi:10.1145/3147.3165
    title: Jeffrey S. Vitter, Random sampling with a reservoir, ACM Transactions on Mathematical Software 11(1), 37 to 57, 1985
    locator: the unweighted reservoir and its skip methods, which A-ExpJ follows
---

Weighted reservoir sampling draws $k$ items from a stream of weighted items in one pass, without replacement, so that each draw favors heavy items. In the method of Pavlos Efraimidis and Paul Spirakis (2006), each item with weight $w$ gets the random key $u^{1/w}$, where $u$ is uniform on $(0, 1]$, and the sample is the $k$ items with the largest keys. Algorithm A-Res keeps these $k$ items in a [min-heap](/binary-heap/). Algorithm A-ExpJ draws, like [Algorithm L](/algorithm-l/), how much weight passes before the next item enters, and draws random numbers only for the items that enter. The sample, read by decreasing key, has the law of *successive sampling*: $k$ draws in which each draw picks a remaining item with probability proportional to its weight. With equal weights it is plain [reservoir sampling](/reservoir-sampling/).

## In plain words

Give every item a lottery ticket, a random number, and keep the items with the best tickets. To favor heavy items, a heavy item's ticket is pushed toward the top, in a special way: an item of weight 3 gets the best of three plain tickets, and a weight between whole numbers is handled by the same rule. With this rule the best ticket of all belongs to each item with a chance in proportion to its weight. After the winner is set aside, the same is true of the rest. So the kept items look like a draw from a bag, one by one, where heavy items are more likely to come out first.

Only the best tickets so far need to be kept, so the stream is read once with a small amount of memory.

## The problem

The input is a sample size $k \ge 1$ and a stream of pairs $(x_i, w_i)$ with weights $w_i > 0$, read once, with $n$ and the total weight $W = \sum_i w_i$ unknown in advance. The output is a sequence of $k$ distinct items (all items if $n < k$) with the law of successive sampling:
$$\Pr[\text{output} = (i_1, \ldots, i_k)] = \prod_{j=1}^{k} \frac{w_{i_j}}{W - w_{i_1} - \cdots - w_{i_{j-1}}}.$$
This is the one-pass form of [weighted sampling](/weighted-sampling/) without replacement, and a weighted form of the [stream sampling problem](/stream-sampling/).

The inclusion probability of an item is *not* proportional to its weight. For weights 1, 2, 3 and $k = 2$, the item of weight 3 is in the sample with probability $17/20$, not $2 \cdot 3/6 = 1$. If inclusion must be proportional to size, see [probability proportional to size sampling](/probability-proportional-to-size-sampling/). If the goal is an unbiased estimate of subset sums, see [priority sampling](/priority-sampling/).

## The algorithm

```pseudo id=main
A-RES(stream, k)                           ▷ items x with weights w > 0
L1  H ← an empty min-heap of (key, item)
L2  for each item x with weight w
L3      r ← random()^(1/w)                   ▷ random() is uniform on (0, 1]
L4      if |H| < k then insert (r, x) into H
L5      else if r > the least key in H then replace the least of H by (r, x)
L6  return the items of H by decreasing key

A-EXPJ(stream, k)
L7  put the first k items into H as in lines L2 to L4
L8  T ← the least key in H; X ← ln(random()) / ln(T)     ▷ the weight to pass
L9  for each later item x with weight w
L10     X ← X − w
L11     if X ≤ 0                             ▷ this item enters
L12         r ← (T^w + (1 − T^w) · random())^(1/w)        ▷ a key above T
L13         replace the least of H by (r, x)
L14         T ← the least key in H; X ← ln(random()) / ln(T)
L15 return the items of H by decreasing key
```

A-RES is [top-k selection](/top-k-selection/) on random keys. A-EXPJ uses the fact that, while the least key in $H$ is $T$, an item of weight $w$ enters with probability $1 - T^w$, independently of the others. So the total weight that passes before the next entry has $\Pr[X > s] = T^s$, which line L8 draws by [inversion](/inverse-transform-sampling/). The entering item has a key conditioned to be above $T$, which line L12 draws directly.

## Example

Take $k = 2$ and the stream $a, b, c, d$ with weights $1, 2, 3, 4$.

**A-RES.** Say the uniform reals are $0.5, 0.3, 0.8, 0.2$.

| item | $w$ | $u$ | key $u^{1/w}$ | heap after (key, item) |
|---|---|---|---|---|
| $a$ | 1 | 0.5 | 0.5000 | (0.5000, $a$) |
| $b$ | 2 | 0.3 | 0.5477 | (0.5000, $a$), (0.5477, $b$) |
| $c$ | 3 | 0.8 | 0.9283 | (0.5477, $b$), (0.9283, $c$) |
| $d$ | 4 | 0.2 | 0.6687 | (0.6687, $d$), (0.9283, $c$) |

The output is $(c, d)$. Its probability under successive sampling is $\frac{3}{10} \cdot \frac{4}{7} = \frac{6}{35}$.

**A-EXPJ.** Keep the keys $0.5$ and $0.5477$ of $a$ and $b$. Then $T = 0.5$, and with $V = 0.2$ line L8 gives $X = \ln 0.2 / \ln 0.5 \approx 2.32$. Item $c$ brings $X$ to $2.32 - 3 \le 0$, so it enters. With $T^3 = 0.125$ and $V' = 0.6$, line L12 gives the key $(0.125 + 0.875 \cdot 0.6)^{1/3} \approx 0.8662$, and $a$ leaves. Now $T = 0.5477$, and $V = 0.7$ gives $X \approx 0.592$. Item $d$ enters, with $T^4 = 0.09$ and $V' = 0.1$: its key is $0.181^{1/4} \approx 0.6523$, and $b$ leaves. The output is again $(c, d)$. On a stream this short A-EXPJ draws more random numbers (7) than A-RES (4). The gain comes on long streams, where entries are rare.

## Correctness

**Theorem (Efraimidis and Spirakis 2006).** In exact arithmetic, A-RES returns a successive sample of size $\min(k, n)$, and A-EXPJ returns a sample with the same law.

Put $D_i = -\ln(u_i)/w_i$. Then $D_i$ is exponential with rate $w_i$, and the key is $e^{-D_i}$, so the largest keys are the smallest $D_i$. In a race of independent exponential clocks, clock $j$ rings first with probability $w_j / \sum w$, and the remaining times after the first ring are again independent exponentials with the same rates. Applying this $k$ times gives the successive sampling product. For A-EXPJ, the time to the next entry and the key of the entering item have the same law as in A-RES, given the current least key $T$. The full proof is below.

## Complexity

- **A-RES.** One random number and $O(1)$ work per item, plus $O(\log k)$ heap work for each item that enters. The worst case is $O(n \log k)$ time and $\Theta(k)$ space.
- **A-EXPJ.** One subtraction per item, and two random numbers and $O(\log k)$ heap work per entry. The items must still be read, so the time is $O(n)$ plus $O(\log k)$ per entry.
- **Number of entries.** Item $i > k$ enters with probability $\Pr[\text{its key is among the } k \text{ largest of the first } i]$. With equal weights this is $k/i$, so there are $k(H_n - H_k) \le k \ln(n/k)$ entries in expectation. The same holds when the weights are in random order, because then the rank of item $i$ among the first $i$ keys is uniform. When the weights grow along the stream, almost every item can enter: with weights $1.02^i$, $n = 1000$ and $k = 10$, a simulation measured about 198 entries per run, against $k(H_n - H_k) \approx 45.6$ for equal weights.
- **Random numbers.** A-RES uses $n$. A-EXPJ uses $k + 1$ plus 2 per entry, so with equal weights $k + 1 + 2k(H_n - H_k)$ in expectation.

## Properties

- **Online.** After each item, the reservoir is a successive sample of the items so far.
- **Mergeable.** Each of the $k$ largest keys of a union is among the $k$ largest keys of its own part, so samples of parts merge by keeping the $k$ largest of their stored keys.
- **Reduces to the unweighted case.** With equal weights, the key order is a uniform order, and A-RES returns a uniform $k$-subset.
- **Exact only in exact arithmetic.** The keys use real powers and logarithms.

## Variants and improvements

- **Log keys.** The key $\ln(u)/w$ is a monotone function of $u^{1/w}$, so it gives the same sample and does not underflow. Its negative, $-\ln(u)/w$, is an exponential clock, and taking $\ln w$ minus the log of an exponential gives the [Gumbel-max trick](/gumbel-max-trick/), whose top $k$ is the same successive sample.
- **Inclusion proportional to weight.** Methods whose inclusion probabilities are proportional to weight need a different rule. See [probability proportional to size sampling](/probability-proportional-to-size-sampling/).
- **Priority sampling.** The key $w/u$ instead of $u^{1/w}$ gives a sample with a simple unbiased estimator of subset sums. See [priority sampling](/priority-sampling/).
- **Unweighted jumps.** A-EXPJ is the weighted form of the skip idea of [Vitter's Algorithm Z](/vitter-reservoir-skip/) and [Algorithm L](/algorithm-l/).

## When to use it

Use A-RES when you need $k$ items without replacement from a stream or a large table, with heavy items more likely, and the total weight is unknown or changes. It is a few lines over a heap, and samples of parts can be merged. Use A-EXPJ when random numbers are costly and the weights are not growing along the stream. If one item is needed at a time, with replacement, from a fixed list, the [alias method](/alias-method/) is faster.

## Pitfalls

- **Underflow.** For small $w$, $u^{1/w}$ rounds to 0, and many keys become equal. Compare $\ln(u)/w$ instead, or guard the threshold $T = 0$ in A-EXPJ.
- **Key $u \cdot w$.** The intuitive key $u \cdot w$ does not give successive sampling. For weights 1, 2, 3, 4 and $k = 2$, a chi-squared test over the 12 ordered pairs rejects it at once.
- **Reading the output as proportional to weight.** The inclusion probabilities of successive sampling are not $k w_i / W$. Estimators that assume they are will be biased.
- **ln(0).** Use $1 - \text{random}()$, in $(0, 1]$, before taking the logarithm.
- **Zero weights.** An item of weight 0 must be dropped before the key is computed, since $1/w$ is undefined.

## Implementations

## History

Pavlos Efraimidis and Paul Spirakis published "Weighted random sampling with a reservoir" in Information Processing Letters in 2006. It gives the key rule $u^{1/w}$ with a proof that the order of keys is successive sampling, the heap method A-Res, and the jump method A-ExpJ, which carries the skip idea of Vitter's 1985 reservoir methods to weighted streams.

## References
