---
tag: 8QPQ8N
kind: problem
slug: self-organizing-list-search
name: Search in a self-organizing list
aliases:
- self-adjusting list search
area: searching/sequential-and-binary-search
level: advanced
summary: Minimise total search cost when the list is reordered by access, using heuristics such as move-to-front or transpose.
model: comparison-model
complexity:
  vars: {n: the number of items in the list, m: the number of requests}
  time: {worst: Θ(m n)}
prereqs: [linear-search, self-organizing-list]
see_also: [self-organizing-list, move-to-front-heuristic, transposition-rule, frequency-count, list-update-problem, competitive-ratio, splay-tree, linear-search]
sources:
  - paper: doi:10.1145/359997.360000
    title: Ronald L. Rivest, On self-organizing sequential search heuristics, Communications of the ACM 19(2) (1976)
    locator: pp. 63 to 67 (the stationary cost of move-to-front and of transpose under independent requests)
  - paper: doi:10.1145/2786.2793
    title: Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985)
    locator: pp. 202 to 208 (move-to-front is within a factor 2 of every algorithm; transpose and frequency count are not)
  - paper: doi:10.1145/5505.5507
    title: J. H. Hester and D. S. Hirschberg, Self-organizing linear search, ACM Computing Surveys 17(3) (1985)
    locator: survey of the heuristics and of their average-case results
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1, Sequential searching (self-organizing files, the move-to-front rule and Zipf's law)
---

Search in a self-organizing list asks how to keep an unsorted list of $n$ items in a good order while a sequence of $m$ requests is served, when each request is answered by a [linear search](/linear-search/) from the front and costs the position of the item. If the request frequencies were known, the best fixed order would sort the items by decreasing frequency. They are not known, so a self-organizing list changes its order after each access by a simple rule: [move to front](/move-to-front-heuristic/), [transpose](/transposition-rule/) with the item before it, or keep the items sorted by [access count](/frequency-count/). Under independent requests, move to front costs at most $2C_{\text{opt}} - 1$, where $C_{\text{opt}}$ is the cost of the best fixed order. For any request sequence at all, Sleator and Tarjan proved that move to front costs at most twice as much as any algorithm, even one that knows the future, while transpose and frequency count can be worse by a factor that grows with $n$ or with $m$. This is the [list update problem](/list-update-problem/), a founding example of [competitive analysis](/competitive-ratio/).

## In plain words

You keep your tools in one long drawer and always search from the front. Some tools you use every day, others once a year. The best order puts the most used tools first, but you do not know in advance which ones those are, and it changes over time.

So you use a habit. Each time you use a tool, you put it back at the front of the drawer. Tools you use often then stay near the front without any counting. A gentler habit moves a tool only one place forward. Another keeps a tally for each tool and orders the drawer by the tallies.

The first habit never does too badly: in the long run it costs at most about twice as much as the best order. The gentle habit can get stuck badly when two tools at the back take turns.

## Definition

**Input.** A list of $n$ distinct items in some first order, and a sequence $\sigma = \sigma_1, \ldots, \sigma_m$ of requests, each one an item of the list.

**Serving a request.** The request for $x$ scans the list from the front and costs $i$ when $x$ is at position $i$ (positions start at 1). After the access the algorithm may move $x$ forward to any position at no cost (a *free exchange*), and it may swap any two adjacent items at cost 1 each (a *paid exchange*). This is the standard model of Sleator and Tarjan.

**Goal.** Minimize the total cost $\sum_t \text{cost}(\sigma_t)$ plus the cost of paid exchanges. The algorithm is *online*: it must act on $\sigma_t$ before it sees $\sigma_{t+1}$.

Two settings are studied:

- **Probabilistic.** The requests are independent, and item $i$ is requested with a fixed unknown probability $p_i$. The measure is the expected cost of a request in the long run, compared with $C_{\text{opt}} = \sum_i i\, p_{(i)}$, the cost of the best fixed order, where $p_{(1)} \ge p_{(2)} \ge \cdots$.
- **Adversarial.** The sequence is arbitrary. The measure is the competitive ratio: the least $c$ such that the cost of the algorithm is at most $c$ times the cost of the best offline algorithm on the same sequence, plus a constant.

## Variants

- **Insertions and deletions.** The dictionary version, where an insertion scans to the end and adds the item, and a deletion scans to it. The same results hold for the main rules.
- **Paid exchanges only.** Some models make every move cost; [move to front](/move-to-front/) is then still within a constant factor.
- **Unequal item sizes or costs.** Each item has its own access cost; the best fixed order sorts by the ratio of probability to cost.
- **Trees.** The same question for a binary search tree gives [splay trees](/splay-tree/) and the [dynamic optimality conjecture](/dynamic-optimality-conjecture/).
- **Compression.** The [move-to-front transform](/move-to-front-transform/) encodes each symbol by its position in a move-to-front list, which turns local repetition into small numbers.

## Examples

**A short sequence.** The list starts as $a, b, c, d, e$. For the requests $e, e, e, e, d, e, d, e$ the costs are:

| rule | costs per request | total | final order |
|---|---|---|---|
| no change | 5, 5, 5, 5, 4, 5, 4, 5 | 38 | $a, b, c, d, e$ |
| move to front | 5, 1, 1, 1, 5, 2, 2, 2 | 19 | $e, d, a, b, c$ |
| transpose | 5, 4, 3, 2, 5, 1, 4, 1 | 25 | $e, a, d, b, c$ |

For the requests $e, d, e, d, e, d, e, d$, transpose swaps $d$ and $e$ back and forth at the end of the list and pays 5 for every request, 40 in all, more than the 36 of no change. Move to front pays 22. Repeating the pair longer makes the gap grow without limit, which is why transpose is not competitive.

**Independent requests, Zipf's law.** With $p_i$ proportional to $1/i$, computed exactly by the formula below:

| $n$ | best fixed order $C_{\text{opt}}$ | move to front | ratio |
|---|---|---|---|
| 10 | 3.414 | 4.295 | 1.258 |
| 100 | 19.278 | 26.261 | 1.362 |
| 1000 | 133.592 | 184.724 | 1.383 |

The ratio approaches $2 \ln 2 \approx 1.386$ for Zipf's law. A simulation with $n = 10$ and 300000 requests gave averages of 4.296 for move to front, 3.703 for transpose and 3.415 for frequency count. For the uniform distribution all orders cost $(n+1)/2$, and so do all rules.

## Known algorithms

- **Move to front (MTF).** Move the requested item to the front with free exchanges. No memory beyond the list, $O(1)$ extra work on a linked list, and it adapts fast to changes in the request pattern.
- **Transpose.** Swap the requested item with the item before it. It moves slowly, so it is stable under independent requests: Rivest proved that its long-run cost is never more than that of MTF in that setting. But it adapts slowly and can fail badly on adversarial sequences.
- **Frequency count.** Keep a counter per item and keep the list in decreasing order of the counters. Under independent requests it tends to the best fixed order, but it needs a counter per item, and it is not competitive: a sequence that requests items in long runs, in the reverse of the counter order, makes it pay $\Theta(n)$ per request where MTF pays $O(1)$.
- **Randomized rules.** BIT keeps one random bit per item and moves an item to the front when its bit flips to a given value; COMB mixes BIT with a timestamp rule. These are known to reach ratios below 2 against an oblivious adversary.
- **Offline optimum.** With the whole sequence known, the best way to serve it can be found by dynamic programming over the $n!$ orders, which is feasible only for very small $n$; the general offline problem is NP-hard.

## Bounds

**Best fixed order.** For independent requests, the fixed order of least expected cost lists the items by decreasing $p_i$. If two adjacent items have $p_a < p_b$ with $a$ first, swapping them changes the cost by $p_a - p_b < 0$, so every best order is sorted.

**Move to front under independent requests.** In the long run, the expected cost of a request under MTF is
$$ C_{\text{MTF}} = 1 + 2 \sum_{i < j} \frac{p_i p_j}{p_i + p_j} \;\le\; 2 C_{\text{opt}} - 1. $$

*Proof.* After many requests, item $j$ is before item $i$ exactly when the last request for either of them was for $j$. The requests are independent, so this has probability $p_j/(p_i + p_j)$, in the limit where both items have been requested. A request for $i$ costs 1 plus the number of items before it, so its expected cost is $1 + \sum_{j \ne i} p_j/(p_i + p_j)$. Averaging over $i$ with weights $p_i$ gives $1 + \sum_{i \ne j} p_i p_j/(p_i + p_j)$, which is the formula. For the inequality, number the items so that $p_1 \ge \cdots \ge p_n$. For $i < j$, $p_i p_j / (p_i + p_j) \le p_j$, since $p_i \le p_i + p_j$. So $C_{\text{MTF}} \le 1 + 2 \sum_j (j - 1) p_j = 2 \sum_j j p_j - 1 = 2C_{\text{opt}} - 1$. $\blacksquare$

The sharp constant is smaller: Chung, Hajela and Seymour proved that $C_{\text{MTF}} \le (\pi/2)\, C_{\text{opt}}$ for every distribution, and that $\pi/2$ cannot be lowered.

**Move to front against every algorithm.** Sleator and Tarjan proved that, for every request sequence and every algorithm $A$, including offline ones, MTF pays at most twice the cost of $A$, up to terms for the paid exchanges of $A$ and the number of requests. The proof uses the [potential method](/potential-method/) with the number of inversions between the two lists.

**No deterministic rule does better than 2.** For every deterministic online rule, the ratio is at least $2 - 2/(n+1)$.

*Proof.* The adversary always requests the item that is last in the rule's current list, so the rule pays $n$ per request, $mn$ for $m$ requests. For the same sequence, consider the $n!$ fixed orders, each set up once at the start with at most $\binom{n}{2}$ paid exchanges. In a random fixed order a request costs $(n+1)/2$ on average, so some fixed order pays at most $m(n+1)/2 + \binom{n}{2}$ in all. The ratio is at least $mn / (m(n+1)/2 + \binom{n}{2})$, which tends to $2n/(n+1) = 2 - 2/(n+1)$ as $m$ grows. $\blacksquare$

**Randomized rules.** Against an oblivious adversary, BIT is $1.75$-competitive and COMB is $1.6$-competitive, and no randomized rule beats $1.5$.

## Reductions

- **[Linear search](/linear-search/) is the access step.** Each request is a search in an [unordered array](/search-in-unordered-array/) or list, with cost equal to the position found.
- **It is the [list update problem](/list-update-problem/)** of online algorithms, with search as the access cost.
- **Paging is a related problem.** The proof idea of Sleator and Tarjan also bounds the LRU rule for paging, which is move to front on the pages in memory: see the [LRU cache](/lru-cache/).
- **Search trees.** Replacing the list by a binary search tree and "move to front" by "rotate to the root" gives [splay trees](/splay-tree/).

## Applications

- Symbol tables in small compilers and interpreters, where a [sequential search symbol table](/sequential-search-symbol-table/) with move to front keeps recent names near the front.
- Chains of a hash table with separate chaining: moving a found key to the front of its chain helps when keys are requested in bursts.
- The [move-to-front transform](/move-to-front-transform/) in data compression, after the Burrows-Wheeler transform.
- Caches of recent items in network and file system code, where the access pattern changes over time.

## References
