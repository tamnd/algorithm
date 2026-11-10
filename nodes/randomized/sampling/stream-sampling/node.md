---
tag: DSYY2X
kind: problem
slug: stream-sampling
name: Sampling from a data stream
aliases:
- Stream sampling problem
- sampling from a stream
- stream sampling
- uniform sample of a stream
- one-pass sampling
area: randomized/sampling
level: core
summary: Maintain a uniform sample of fixed size over a one-pass stream of unknown length.
prereqs: [streaming-model, uniform-random-subset, linearity-of-expectation, harmonic-series]
see_also: [reservoir-sampling, algorithm-l, vitter-reservoir-skip, weighted-reservoir-sampling, priority-sampling, bernoulli-sampling, sliding-window-sampling, l0-sampling-problem]
sources:
  - paper: doi:10.1145/3147.3165
    title: Jeffrey S. Vitter, Random sampling with a reservoir, ACM Transactions on Mathematical Software 11(1), 37 to 57, 1985
    locator: the reservoir model, Algorithm R and its analysis, the lower bound on the number of records that enter the reservoir, and Algorithms X, Y and Z
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1997
    locator: Section 3.4.2 (Random Sampling and Shuffling), Algorithm S (selection sampling) and Algorithm R (reservoir sampling)
  - paper: doi:10.1016/j.ipl.2005.11.003
    title: Pavlos S. Efraimidis and Paul G. Spirakis, Weighted random sampling with a reservoir, Information Processing Letters 97(5), 181 to 185, 2006
    locator: Algorithm A-Res and Algorithm A-ExpJ for weighted sampling without replacement in one pass
---

Stream sampling asks for a random sample of the items of a stream that is read once, in order, when the length of the stream is not known in advance and the memory is much smaller than the stream. The basic version keeps a uniform sample of $k$ items: at every moment, the $k$ items kept must be a uniform random $k$-subset of the items seen so far. The answer is [reservoir sampling](/reservoir-sampling/), which replaces a random kept item by item $t$ with probability $k/t$. This page is about the problem, its variants, and the bounds; the algorithms have their own pages.

## In plain words

Items pass by one at a time, for example lines of a log, and you cannot go back. You do not know how many will come. You have room for $k$ of them. At any moment someone may ask you for a fair sample: each group of $k$ items seen so far must be equally likely to be the one you hold.

You cannot simply keep each item with chance $k$ over the total, because you do not know the total. You also cannot keep the first $k$ or the last $k$. The trick is to let the newest item in with a chance that falls as more items arrive.

## Definition

**Input.** A sequence $x_1, x_2, \ldots$ of items, read once in order. The length $n$ is unknown until the stream ends. A source of random numbers, such as uniform integers or uniform reals in $(0, 1)$.

**Memory.** Room for $k$ items plus $O(1)$ words, or $O(k)$ words in some variants.

**Output.** After each prefix $x_1, \ldots, x_t$, a set $S_t$ of $\min(k, t)$ positions such that
$$\Pr[S_t = A] = \binom{t}{k}^{-1} \quad \text{for every } A \subseteq \{1, \ldots, t\},\ |A| = k,$$
when $t \ge k$. The kept items $x_i$, $i \in S_t$, are the sample. Because the stream can end at any time, the condition must hold for every $t$, not only at the end.

**Costs.** The number of random numbers used, the time per item, and the number of items that are ever written to the sample. When a sample lives on disk, as in Vitter's setting, each write is expensive.

## Variants

- **Fixed size, without replacement.** The definition above. Solved by [reservoir sampling](/reservoir-sampling/).
- **With replacement.** The sample is $k$ independent uniform items of the stream. Run $k$ independent reservoirs of size 1, or draw how many of the $k$ slots item $t$ takes from a binomial distribution with parameters $k$ and $1/t$.
- **Bernoulli sampling.** Keep each item independently with a fixed probability $p$. It needs no knowledge of $n$, but the sample size is random, binomial with mean $pn$. See [Bernoulli sampling](/bernoulli-sampling/).
- **Known length.** If $n$ is known in advance, the sample can be chosen in order as the stream passes, keeping item $t$ with probability (still needed)/(still to come). This is [selection sampling](/selection-sampling/), and the problem is then [uniform random subset](/uniform-random-subset/) with sorted output.
- **Weighted items.** Item $t$ has a weight $w_t$, and the sample should favor heavy items. One version is weighted sampling without replacement, solved by [weighted reservoir sampling](/weighted-reservoir-sampling/). Another asks for unbiased estimates of subset sums with few samples, solved by [priority sampling](/priority-sampling/). See also [probability proportional to size sampling](/probability-proportional-to-size-sampling/).
- **Sliding windows.** The sample must be uniform over the last $w$ items, or over the items of the last $T$ seconds. Old items expire, so a plain reservoir fails. See [sliding window sampling](/sliding-window-sampling/) and [chain sampling](/chain-sampling/).
- **Deletions.** In a turnstile stream items can be inserted and deleted, and the sample must be uniform over the items present at the end. This needs linear sketches instead of stored items. See the [l0 sampling problem](/l0-sampling-problem/) and the [l0 sampler](/l0-sampler/).
- **Distinct values.** The sample should be uniform over the distinct values in the stream, not over the occurrences. A hash function chosen in advance can decide: keep the values with the $k$ least hash values, as the [KMV sketch](/kmv-sketch/) does, which needs a [min-wise independent](/min-wise-independent-hashing/) family in the analysis.
- **Distributed streams.** Several machines each sample their own stream, and the samples must be merged into a uniform sample of the union.

## Examples

**Algorithm R, exact.** For $k = 2$ and $n = 5$, reservoir sampling uses three random integers, uniform on $\{0, 1, 2\}$, $\{0, 1, 2, 3\}$ and $\{0, 1, 2, 3, 4\}$, so it has $3 \cdot 4 \cdot 5 = 60$ equally likely runs. Counting the runs gives each of the $\binom{5}{2} = 10$ pairs in exactly 6 of them, so each pair has probability $1/10$.

**A wrong rule.** For $k = 1$, the rule "replace the kept item by the new one with probability $1/2$" is not uniform. For $n = 4$ it keeps items 1, 2, 3, 4 with probabilities $1/8, 1/8, 1/4, 1/2$. The right rule replaces with probability $1/t$ at item $t$, so every item ends with probability $1/4$.

**Bernoulli sampling has a random size.** With $n = 5$ and $p = 2/5$, Bernoulli sampling returns exactly 2 items with probability only $216/625 \approx 0.35$. It returns no items with probability $243/3125 \approx 0.08$.

**Writes.** In reservoir sampling with $k = 10$, item $t > k$ enters the reservoir with probability $10/t$. Over a stream of $n = 10^6$ items, the expected number of replacements is $10 (H_{10^6} - H_{10}) \approx 114.6$. A seeded run of 200 streams of $10^5$ items (Python `random.Random(5)`) averaged $91.1$ replacements, against the exact mean $91.6$.

**Merging two samples.** One machine has a uniform sample of 3 items from a stream of 6 items, and another has a uniform sample of 3 from a stream of 4. A uniform sample of 3 from all 10 takes $j$ items from the first stream with the hypergeometric probability $\binom{6}{j}\binom{4}{3-j}/\binom{10}{3}$, which is $1/30, 3/10, 1/2, 1/6$ for $j = 0, 1, 2, 3$. Draw $j$ this way, then a uniform $j$-subset of the first sample and a uniform $(3-j)$-subset of the second. The result is uniform on the union, because a uniform subset of a uniform subset is uniform.

## Known algorithms

| Algorithm | Problem | Time | Random numbers | Notes |
| --- | --- | --- | --- | --- |
| [Reservoir sampling](/reservoir-sampling/) (Algorithm R) | fixed size $k$ | $O(n)$ | $n - k$ | the basic method |
| [Vitter's skips](/vitter-reservoir-skip/) (Algorithms X and Z) | fixed size $k$ | $O(k(1 + \log(n/k)))$ expected | $O(k(1 + \log(n/k)))$ | draws the number of items to skip |
| [Algorithm L](/algorithm-l/) | fixed size $k$ | $O(k(1 + \log(n/k)))$ expected | about $3k \ln(n/k)$ | geometric skips, simple code |
| [Bernoulli sampling](/bernoulli-sampling/) | each item with probability $p$ | $O(n)$, or $O(1 + pn)$ with geometric skips | as many as items or as kept items | random size |
| [Selection sampling](/selection-sampling/) | fixed size, known $n$ | $O(n)$ | up to $n$ | sample in stream order |
| [Weighted reservoir sampling](/weighted-reservoir-sampling/) (A-Res, A-ExpJ) | weighted, without replacement | $O(n \log k)$, fewer random numbers with jumps | $n$, or $O(k \log(n/k))$ with jumps | keys $u^{1/w}$ |
| [Priority sampling](/priority-sampling/) | subset sums of weights | $O(n \log k)$ | $n$ | unbiased estimates |
| [Chain sampling](/chain-sampling/) | sliding window of $w$ items | $O(k)$ expected per item | $O(k)$ per item | with replacement, expected $O(k)$ memory |
| [l0 sampler](/l0-sampler/) | turnstile stream | polylog per update | hash functions | approximately uniform |

## Bounds

**Memory.** A sample of $k$ items needs room for $k$ items, so $k$ items of memory is optimal. Reservoir sampling uses exactly that plus a counter.

**The sample must change with probability k/t.** Since the stream may end after any item, the sample after item $t$ must contain item $t$ with probability exactly $k/t$ for $t \ge k$. Item $t$ can be stored only when it arrives. So any one-pass algorithm stores item $t$ with probability at least $\min(1, k/t)$, and by [linearity of expectation](/linearity-of-expectation/) the expected number of items that are ever stored is at least
$$k + \sum_{t=k+1}^{n} \frac{k}{t} = k\,(1 + H_n - H_k) \approx k\left(1 + \ln\frac{n}{k}\right),$$
with $H_n$ the [harmonic number](/harmonic-series/). Algorithm R meets this bound with equality, since it stores item $t$ with probability exactly $k/t$. Vitter (1985) states this lower bound for reservoir algorithms.

**Time.** Reading every item costs $\Theta(n)$. If the stream can skip items without reading them, for example a file with fixed-length records, the cost of the lower bound above is all that is needed: Algorithm Z and Algorithm L run in $O(k(1 + \log(n/k)))$ expected time, which matches the number of writes up to a constant.

**Randomness.** Algorithm R uses one random number per item after the first $k$. Methods with skips use $O(k \log(n/k))$ random numbers, which is again of the order of the number of writes.

**Exact uniformity.** For fixed size samples, the algorithms above are exactly uniform when the random numbers are exactly uniform. With hashing, as in the l0 sampler or distinct value sampling, the sample is uniform only up to the quality of the hash family, unless the hash functions are fully random.

## Reductions

- **To uniform random subset.** If $n$ is known in advance, choose a [uniform random subset](/uniform-random-subset/) of $k$ positions first, sort them, and keep those items as they pass. Selection sampling does this in one pass with no sorting.
- **From random sort keys.** Give each item an independent uniform key in $(0, 1)$ and keep the $k$ items with the least keys. The $k$ least keys of $t$ items fall on a uniform $k$-subset by symmetry, so this solves the problem for every prefix. It is the form behind Algorithm L, weighted reservoir sampling (with keys $u^{1/w}$), priority sampling (with priorities $w/u$), and the merge of distributed samples: the $k$ least keys of a union are the $k$ least keys among the two samples.
- **To shuffling.** Reservoir sampling with $k = n$ stores everything. The inside-out form of the [Fisher-Yates shuffle](/fisher-yates-shuffle/) is the stream analog for a full [random permutation](/random-permutation/): it puts item $t$ at a random position among the first $t$.

## Applications

- **Databases.** Vitter's motivation: draw a random sample of a file on tape or of the result of a query, in one pass, without knowing the number of records.
- **Logs and monitoring.** Keep a fixed number of random log lines, requests or network packets per hour for later inspection, at constant memory. Priority sampling of network flows gives unbiased estimates of the traffic of any subset of flows.
- **Approximate query answers.** Answer aggregate queries over a large table or stream from a uniform sample, with error bars from the sample size.
- **Machine learning.** Draw training batches from a stream of examples, or keep a fixed replay buffer that is a uniform sample of past experience.
- **Testing and auditing.** Pick random records for manual review from a stream of events, where every event must have the same chance.

## References
