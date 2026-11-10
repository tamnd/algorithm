---
tag: RV0AAH
kind: algorithm
slug: priority-sampling
name: Priority sampling
aliases:
- Duffield-Lund-Thorup priority sampling
- priority-sample
- DLT priority sampling
area: randomized/sampling
level: research
summary: Gives each weighted item the priority w/u, keeps the k largest, and estimates each sampled weight as max(w, tau), with tau the next priority; any subset sum is then estimated without bias.
solves: [weighted-sampling]
model: word-ram
complexity:
  vars: {n: the number of items in the stream, k: the sample size}
  time: {worst: "O(n log k)"}
  space: {extra: Θ(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2007
  people: [Nick Duffield, Carsten Lund, Mikkel Thorup]
  note: Duffield, Lund and Thorup published priority sampling for the estimation of arbitrary subset sums in the Journal of the ACM in 2007; Szegedy proved their conjecture on its near optimal variance at STOC 2006.
prereqs: [weighted-reservoir-sampling, linearity-of-expectation, variance]
see_also: [weighted-reservoir-sampling, probability-proportional-to-size-sampling, importance-sampling, reservoir-sampling, kmv-sketch, stream-sampling]
sources:
  - paper: doi:10.1145/1314690.1314696
    title: Nick Duffield, Carsten Lund and Mikkel Thorup, Priority sampling for estimation of arbitrary subset sums, Journal of the ACM 54(6), article 32, 2007
    locator: the definition of priority sampling, the unbiasedness of the estimates, the zero covariance, and the variance estimator
  - paper: doi:10.1016/j.ipl.2005.11.003
    title: Pavlos S. Efraimidis and Paul G. Spirakis, Weighted random sampling with a reservoir, Information Processing Letters 97(5), 181 to 185, 2006
    locator: the related key rule u^(1/w), for comparison
---

Priority sampling, by Nick Duffield, Carsten Lund and Mikkel Thorup, keeps $k$ items from a stream of weighted items so that the total weight of *any* subset can be estimated later without bias, even for a subset chosen after the sample is taken. Each item of weight $w$ gets the priority $q = w/u$, where $u$ is uniform on $(0, 1]$. The sample is the $k$ items of largest priority, and $\tau$ is the $(k+1)$-th largest priority. A sampled item gets the estimate $\hat w = \max(w, \tau)$, and every other item gets 0. Each $\hat w_i$ has mean $w_i$, the estimates of different items have zero covariance when $k \ge 2$, and $\tau \max(0, \tau - w)$ is an unbiased estimate of the variance. Szegedy (2006) proved that priority sampling with $k + 1$ samples has a total variance no larger than the best unbiased method with $k$ samples.

## In plain words

Each item draws a random number, and its priority is its weight divided by that number. Heavy items tend to get high priorities, but a light item can win with a lucky draw. Keep the items with the highest priorities, and also remember the best priority that did not make it. That value is the bar.

To estimate the total of any group of items, add up an estimate for each kept item in the group. A heavy item counts as its own weight. A light item that got in by luck counts as the bar, which is larger than its weight, because it also stands for the light items that did not get in. On average these guesses are exactly right, for every group at once.

## The problem

The input is a sample size $k \ge 1$ and a stream of pairs $(x_i, w_i)$ with weights $w_i > 0$, read once, with $n$ unknown in advance. After the pass, a query names a set $I$ of items, for example all network flows from one source, and asks for $\sum_{i \in I} w_i$. The sample must answer every such query with an estimate whose mean is the true sum, and with variance as small as possible for its size. Typical items are packets or flows with byte counts, or sales with amounts. This is a form of [weighted sampling](/weighted-sampling/) aimed at estimation, not at the law of the sample itself.

## The algorithm

```pseudo id=main
PRIORITY-SAMPLE(stream, k)                 ▷ items x with weights w > 0
L1  H ← an empty min-heap of (priority, item, weight)
L2  for each item x with weight w
L3      q ← w / random()                     ▷ random() is uniform on (0, 1]
L4      insert (q, x, w) into H
L5      if |H| > k + 1 then remove the least of H
L6  if |H| ≤ k then return H with each estimate ŵ = w, and τ = 0
L7  τ ← the least priority in H; remove it from H
L8  return H with each estimate ŵ = max(w, τ), and τ

SUBSET-SUM(sample, I)                      ▷ any set of items, chosen after sampling
L9  return the sum of ŵ over the sampled items in I
```

Lines L1 to L5 keep the $k + 1$ largest priorities. Line L7 takes out the smallest of them as the threshold $\tau$. The estimate in line L8 is a Horvitz-Thompson estimate, the weight divided by the chance of being sampled, but with a chance taken *given the priorities of the other items*: item $i$ is sampled exactly when $q_i$ is above the $k$-th largest priority $\tau'$ of the others, which has probability $\min(1, w_i/\tau')$, and when it is sampled $\tau = \tau'$. So $\hat w_i = w_i / \min(1, w_i/\tau) = \max(w_i, \tau)$.

## Example

Take $k = 3$ and six items.

| item | $w$ | $u$ | priority $w/u$ |
|---|---|---|---|
| $a$ | 6 | 0.75 | 8 |
| $b$ | 1 | 0.25 | 4 |
| $c$ | 3 | 0.6 | 5 |
| $d$ | 0.5 | 0.05 | 10 |
| $e$ | 2 | 0.8 | 2.5 |
| $f$ | 4 | 0.45 | 8.89 |

The three largest priorities are those of $d$, $f$ and $a$, and the fourth is $\tau = 5$, from $c$. The estimates are $\hat w_d = \max(0.5, 5) = 5$, $\hat w_f = \max(4, 5) = 5$ and $\hat w_a = \max(6, 5) = 6$. The estimate of the total is $16$, and the true total is $16.5$. The light item $d$ got in by luck and stands for weight 5. The heavy item $a$ is above $\tau$, so it counts as itself with no error: its variance estimate is $5 \cdot \max(0, 5 - 6) = 0$. The variance estimates of $d$ and $f$ are $5 \cdot 4.5 = 22.5$ and $5 \cdot 1 = 5$.

## Correctness

**Theorem (Duffield, Lund and Thorup 2007).** Let $n > k$. Then $E[\hat w_i] = w_i$ for every item $i$, so $\sum_{i \in I} \hat w_i$ is unbiased for every set $I$. If $k \ge 2$, then $E[\hat w_i \hat w_j] = w_i w_j$ for $i \ne j$, so the variance of a subset sum is the sum of the variances of its terms. And $E[\tau \max(0, \tau - w_i)\,[i \text{ sampled}]] = \operatorname{Var}[\hat w_i]$.

The proof conditions on the priorities of all items but $i$. Let $\tau'$ be the $k$-th largest of them. Then $i$ is sampled if and only if $q_i > \tau'$, which has probability $\min(1, w_i/\tau')$, and then $\tau = \tau'$. So the conditional mean of $\hat w_i$ is $\min(1, w_i/\tau') \max(w_i, \tau') = w_i$, whatever $\tau'$ is. For a pair $i, j$, the same idea works with the $(k-1)$-th largest priority of the others. The full proof is below.

## Complexity

- **Time.** One random number and one heap step per item: $O(n \log k)$ in the worst case. Each query takes $O(k)$ time.
- **Space.** The heap holds $k + 1$ entries: $\Theta(k)$.
- **Variance.** Each item has $\operatorname{Var}[\hat w_i] = E[\,w_i \max(0, \tau' - w_i)\,]$, which is 0 for an item heavier than every possible threshold. So heavy items cost no error and the error comes only from items with weight below $\tau$.

## Properties

- **Unbiased for every subset.** The subset may be chosen after the sample is taken, which is what makes the method fit for traffic and sales logs, where queries are not known in advance.
- **Zero covariance.** For $k \ge 2$, the estimates of distinct items are uncorrelated, so the variance of a subset sum is easy to estimate from the sample. For $k = 1$ two items are never sampled together, and $E[\hat w_i \hat w_j] = 0$.
- **Near optimal.** Duffield, Lund and Thorup conjectured, and Szegedy (STOC 2006, "The DLT priority sampling is essentially optimal") proved, that the total variance $\sum_i \operatorname{Var}[\hat w_i]$ with $k + 1$ samples is at most that of any unbiased method with $k$ samples.
- **Mergeable.** Two samples with their priorities merge by keeping the $k + 1$ largest priorities of the union.
- **Online.** After each item the heap is a priority sample of the items so far.

## Variants and improvements

- **Successive sampling keys.** The key $u^{1/w}$ of [weighted reservoir sampling](/weighted-reservoir-sampling/) gives samples with the law of draws without replacement, but the inclusion probabilities have no simple form, so subset-sum estimation is harder.
- **Bottom-k sketches.** Keeping the $k$ smallest hash values, as in the [KMV sketch](/kmv-sketch/), is an unweighted relative: there too, a threshold value at the edge of the kept set sets the scale of the estimate.
- **Hashing instead of random numbers.** If $u$ is a hash of the item's key, the same item gets the same priority at every site, which allows samples of different streams to be coordinated.
- **Inclusion proportional to size.** When a design with fixed inclusion probabilities is required, see [probability proportional to size sampling](/probability-proportional-to-size-sampling/).

## When to use it

Use priority sampling when weighted records arrive in a stream, the space is fixed, and later queries will ask for totals over subsets that are not known in advance, as in network measurement or sales logs. It suits heavy-tailed weights well, because heavy items are kept with no error. If the goal is a sample with the law of draws without replacement, use [weighted reservoir sampling](/weighted-reservoir-sampling/) instead. If every subset is known in advance, a separate counter per subset is exact.

## Pitfalls

- **The wrong threshold.** The threshold is the $(k+1)$-th largest priority, outside the sample. Using the $k$-th largest, the smallest inside the sample, makes the estimates too large on average, because that value is never below $\tau$ and the estimate $\max(w, \tau)$ grows with the threshold.
- **u = 0.** A generator in $[0, 1)$ can return 0, and $w/0$ fails. Use $1 - \text{random}()$.
- **Covariance for k = 1.** With $k = 1$ the estimates of two items are negatively correlated, so the variance of a sum is not the sum of the variances.
- **Fewer than k + 1 items.** Then there is no threshold. Every item is in the sample and its estimate is its own weight.

## Implementations

## History

Nick Duffield, Carsten Lund and Mikkel Thorup developed priority sampling at AT&T for the measurement of network traffic, where each flow record has a byte count and queries ask for the bytes of arbitrary sets of flows. The journal version appeared in the Journal of the ACM in 2007. Mario Szegedy proved their conjecture on the near optimal variance in a STOC 2006 paper titled "The DLT priority sampling is essentially optimal".

## References
