---
tag: 9E8GB1
kind: algorithm
slug: learning-augmented-marking
name: Learning-augmented marking
aliases:
- predictive paging
- learning-augmented caching
- Predictive Marker
area: online-and-streaming/paging-and-caching-online
level: research
summary: Uses predicted next-request times to get near-optimal cost when predictions are good and bounded cost otherwise.
solves: [paging-problem]
model: word-ram
complexity:
  vars: {n: the number of requests, k: the cache size}
  time: {worst: O(n k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 2018
  people: [Thodoris Lykouris, Sergei Vassilvitskii]
  note: Lykouris and Vassilvitskii gave Predictive Marker at ICML 2018, as one of the first online algorithms with predictions that is both near optimal for good predictions and robust for bad ones.
prereqs: [marking-algorithm, marking-phases, paging-problem, learning-augmented-algorithms]
see_also: [randomized-marking, belady-algorithm, harmonic-paging-bound, online-caching-lower-bound, marking-phases, learning-augmented-algorithms]
sources:
  - paper: doi:10.1145/3447579
    title: Thodoris Lykouris and Sergei Vassilvitskii, Competitive caching with machine learned advice, Journal of the ACM 68(4), article 24, 2021
    locator: the Predictive Marker algorithm and its chains, Theorem 3.3 (the ratio 2 min(1 + 2S, 2H_k)) and its corollary for the absolute loss, and Theorem 3.4 (the lower bound for marking rules that use predictions only to break ties); the conference version is ICML 2018, arXiv:1802.05399
  - paper: "Dhruv Rohatgi, Near-optimal bounds for online caching with machine learned advice, Proceedings of the 31st ACM-SIAM Symposium on Discrete Algorithms (SODA), 2020, arXiv:1910.12172"
    locator: the improved ratio O(1 + min((η/OPT)/k, 1) log k) and the lower bound Ω(log min((η/OPT)/(k log k), k))
  - paper: doi:10.1016/0196-6774(91)90041-V
    title: "Amos Fiat, Richard M. Karp, Michael Luby, Lyle A. McGeoch, Daniel D. Sleator and Neal E. Young, Competitive paging algorithms, Journal of Algorithms 12(4) (1991), 685-699"
    locator: the lower bound OPT at least half the number of clean pages, and the randomized marking algorithm
---

Learning-augmented marking is a paging rule that uses a prediction, for each request, of the time when the same page will be requested next. The best known form is Predictive Marker of Lykouris and Vassilvitskii (2018). It is a [marking algorithm](/marking-algorithm/), so it never evicts a page that was requested in the current phase. Among the unmarked pages, it first follows the predictions, and it changes to random evictions when the predictions have caused too many misses in a phase. With perfect predictions its cost is at most $2$ times the optimum, and for each predictor its expected cost is at most $4 H_k$ times the optimum, where $H_k = 1 + 1/2 + \cdots + 1/k$.

## In plain words

The best possible rule for a cache evicts the page that will be needed again last. An online rule does not know the future, but a learned model can guess it. If the cache trusts the guess blindly, a bad model can make it miss on almost every request.

Predictive Marker uses the guesses with care. It works in rounds. In each round, a page that was used in the round is protected, so the cache is never much worse than a safe classical rule. Among the pages that are not protected, it evicts the one that the model says will come back last. If an evicted page comes back soon, the model was wrong. After a few such errors in a row, the rule stops trusting the model for that line of errors and evicts at random.

## The problem

The input is a sequence $\sigma_1, \ldots, \sigma_n$ of page requests and a cache of $k$ pages, as in the [paging problem](/paging-problem/). With each request $\sigma_i$ comes a prediction $h_i$ of the next time $y_i > i$ at which the page $\sigma_i$ is requested again ($y_i = n + 1$ if it never is). The cost is the number of misses. The quality of the predictor is the absolute loss

$$\eta = \sum_{i=1}^{n} |h_i - y_i|,$$

and the predictor is $\epsilon$-accurate if $\eta \le \epsilon \cdot \mathrm{OPT}$, where $\mathrm{OPT}$ is the cost of [Belady's rule](/belady-algorithm/). The aim is a rule whose ratio is close to $1$ when $\epsilon$ is small (consistency), grows slowly with $\epsilon$ (smoothness), and is $O(\log k)$ for every predictor (robustness), like the best rules without predictions.

## The algorithm

The rule works in [$k$-phases](/marking-phases/). A phase ends just before the request to the $(k+1)$-th distinct page since the phase began. At the start of a phase all pages are unmarked, and each requested page becomes marked. In phase $r \ge 2$, a requested page is *clean* if it was not requested in phase $r - 1$, and *stale* if it was. The misses of a phase form *chains*: each clean miss starts a new chain, and each page that is evicted joins the chain of the miss that evicted it. A stale miss belongs to the chain that its page joined when it was evicted. Each page keeps the prediction from its most recent request.

```pseudo id=main
PREDICTIVE-MARKER(σ, h, k)
L1  misses ← 0, cache empty, no page marked, phase ← 1
L2  for i ← 1 to n do x ← σ_i
L3      pred[x] ← h_i
L4      if x is in the cache then mark x; continue (hit)
L5      misses ← misses + 1
L6      if the cache holds k pages and all are marked then phase ← phase + 1, unmark all pages, delete all chains
L7      if the cache holds fewer than k pages then load x, mark x; continue
L8      if x is clean then start a new chain ℓ with length 1
L9      else ℓ ← the chain of x; length(ℓ) ← length(ℓ) + 1
L10     if length(ℓ) ≤ H_k then y ← the unmarked page in the cache with the largest pred
L11     else y ← an unmarked page in the cache, chosen uniformly at random
L12     evict y, put y in chain ℓ, load x, mark x
L13 return misses
```

Line L6 starts a new phase. Lines L8 and L9 decide the chain of the miss. Line L10 is the step that trusts the predictions: it acts like Belady's rule, but only among the unmarked pages. Line L11 is the fallback of [randomized marking](/randomized-marking/). A chain gets long only if the predictions keep pointing at pages that come back in the same phase, so the length of a chain measures the errors of the predictor.

With a full cache and $x$ not in it, some page in the cache is unmarked: if all $k$ were marked, line L6 has just unmarked them. So lines L10 and L11 always find a page.

## Example

Cache size $k = 4$, so $H_4 = 25/12 \approx 2.08$, and chains of length $1$ and $2$ follow the predictions. The requests at times $1$ to $10$ are $a, b, c, d, e, a, b, c, a, b$. The perfect predictions are $6, 7, 8, 11, 11, 9, 10, 11, 11, 11$. In this run the predictor is wrong only at time $4$: it says that $d$ comes back at time $6$, but $d$ never comes back. So $\eta = 5$.

| time | request | prediction | result | phase | eviction |
|---|---|---|---|---|---|
| 1 | a | 6 | miss, load | 1 | - |
| 2 | b | 7 | miss, load | 1 | - |
| 3 | c | 8 | miss, load | 1 | - |
| 4 | d | 6 (true: 11) | miss, load | 1 | - |
| 5 | e | 11 | miss, clean, new chain of length 1 | 2 | c (largest prediction 8 among a, b, c, d) |
| 6 | a | 9 | hit, mark | 2 | - |
| 7 | b | 10 | hit, mark | 2 | - |
| 8 | c | 11 | miss, stale, chain length 2 | 2 | d (the only unmarked page) |
| 9 | a | 11 | hit | 2 | - |
| 10 | b | 11 | hit | 2 | - |

The rule has $6$ misses. With the perfect predictions it evicts $d$ at time $5$ and has $5$ misses, the same as the optimum. The wrong prediction for $d$ cost one extra miss, a stale miss that made the chain longer.

## Correctness

The rule serves each request and never evicts a marked page, so it is a marking algorithm and has at most $k$ misses in each phase. Each miss of phase $r \ge 2$ adds $1$ to the length of exactly one chain, so the cost of the phase is the sum of its chain lengths, and the number of chains is the number $c_r$ of clean pages. With perfect predictions there is no stale miss at all: the page evicted in line L10 is not requested again in the phase. So each chain has length $1$ and the cost is $\sum_r c_r \le 2 \cdot \mathrm{OPT}$. The proof below gives these steps in full and sketches the bounds for imperfect predictions.

## Complexity

Line L4 takes $O(1)$ expected time with a hash table. Lines L10 and L11 scan the unmarked pages in $O(k)$ time; a priority queue keyed by the predictions makes line L10 take $O(\log k)$ time. So $n$ requests take $O(n k)$ time, or $O(n \log k)$ time with the priority queue, and the extra space is $O(k)$ for the cache, the marks and the chains. The cost of the predictor is not counted.

## Properties

- **Consistency.** If $\eta = 0$, the cost is at most $2 \cdot \mathrm{OPT}$, and no random choice is made.
- **Robustness.** For every predictor, the expected cost is at most $4 H_k \cdot \mathrm{OPT}$, within a factor $4$ of the bound $H_k$ of the [lower bound for randomized paging](/online-caching-lower-bound/).
- **Smoothness.** Lykouris and Vassilvitskii prove a ratio of at most $2 \min(1 + 2S, 2H_k)$, where $S$ depends on the loss function and on $\epsilon$. For the absolute loss and an $\epsilon$-accurate predictor this is at most $\min(2 + 2\sqrt{5\epsilon}, 4H_k)$ (Lykouris and Vassilvitskii 2021, Theorem 3.3 and its corollary).
- **A deterministic bound.** The rule is a marking algorithm, so its cost is at most $k \cdot \mathrm{OPT}$ on every sequence, whatever the random choices are.
- **Following the predictions blindly is not robust.** The rule that always evicts the page with the largest prediction, with no marks, is optimal when $\eta = 0$. But with $k = 2$, the sequence $a, b, c$ followed by $a, b$ repeated, and predictions that say $c$ comes back soon and $a$ and $b$ never, it misses on every request while the optimum has $4$ misses. Predictive Marker has $6$ misses on this sequence. The tests check both numbers.

## Variants and improvements

- **Rohatgi (2020).** A modified rule has ratio $O(1 + \min((\eta / \mathrm{OPT}) / k, 1) \log k)$, so the error term is divided by $k$. Rohatgi also proves that every rule has ratio $\Omega(\log \min((\eta / \mathrm{OPT}) / (k \log k), k))$ for some sequences.
- **Lower bound for tie-breaking.** Lykouris and Vassilvitskii show that a deterministic marking rule that uses the predictions only to choose among the unmarked pages has ratio $\Omega(\min(S, k))$ for some $\epsilon$-accurate predictors (Theorem 3.4). So the switch to random evictions in line L11 is needed for robustness.
- **Other predictions.** Later work uses other kinds of advice, such as a predicted eviction for each miss, or combines several predictors. The page on [learning-augmented algorithms](/learning-augmented-algorithms/) gives the general setting.

## When to use it

Use it when a model can predict reuse times, for example from past access patterns of a web cache or a storage system, and the cache must not fail badly when the model is wrong. If the predictions are known to be very good, Belady's rule on the predictions is simpler, but it has no guarantee. If no predictor is available, use randomized marking, which has ratio $2H_k - 1$.

## Pitfalls

- **A deterministic fallback.** Changing line L11 to a fixed rule, such as LRU among the unmarked pages, keeps the bound $k$ but loses the bound $O(\log k)$ for bad predictions.
- **The threshold.** The switch happens when a chain is longer than $H_k$, not when it is longer than $k$. A larger threshold makes the robustness bound worse.
- **Predictions of the next arrival only.** The rule uses $h_i$ as a prediction of the next request of $\sigma_i$, kept until that page is requested again. An error early in the sequence can stay in the cache for a long time and is counted once in $\eta$.
- **The cost of the optimum in the bound.** The error is measured relative to $\mathrm{OPT}$. A predictor with a small total error can still be bad if $\mathrm{OPT}$ is very small.

## Implementations

## History

Lykouris and Vassilvitskii presented Predictive Marker at ICML 2018, with the journal version in the Journal of the ACM in 2021. The paper defined consistency and robustness in the competitive sense and helped start the area of algorithms with predictions. Rohatgi improved the bound and gave a nearly matching lower bound at SODA 2020. The marking framework and the bound $\mathrm{OPT} \ge \frac{1}{2} \sum_r c_r$ go back to Fiat, Karp, Luby, McGeoch, Sleator and Young (1991).

## References
