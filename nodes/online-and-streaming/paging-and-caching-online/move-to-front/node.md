---
tag: XGK3CR
kind: algorithm
slug: move-to-front
name: Move-to-front rule
aliases:
- MTF
- Move-to-front
- move-to-front rule
- MTF rule
area: online-and-streaming/paging-and-caching-online
level: intro
summary: Moves each accessed element to the front of the list; 2-competitive for list update.
solves: [list-update-problem]
model: word-ram
complexity:
  vars: {m: the number of requests, n: the length of the list}
  time: {worst: O(m n)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1985
  people: [Daniel D. Sleator, Robert E. Tarjan]
  note: Sleator and Tarjan proved in 1985 that move-to-front costs at most twice the optimum for list update, with paid and free exchanges. The rule itself is older, and McCabe studied it in 1965.
prereqs: [list-update-problem, competitive-ratio, potential-function, inversion]
see_also: [transposition-rule, frequency-count, move-to-front-heuristic, self-organizing-list, move-to-front-transform, lru]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the theorem that move-to-front costs at most 2 C_A + X_A - F_A - m, and the remarks on transpose and frequency count
  - paper: doi:10.1145/3894.3896
    title: "Jon L. Bentley and Catherine C. McGeoch, Amortized analyses of self-organizing sequential search heuristics, Communications of the ACM 28(4) (1985), 404-411"
    locator: the bound of twice the cost of the optimal static list for move-to-front
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1, the list accessing problem, the analysis of MTF and the lower bound for deterministic algorithms
  - paper: "Sandy Irani, Two results on the list update problem, Information Processing Letters 38(6) (1991), 301-306"
    locator: the lower bound 2n/(n + 1) for deterministic algorithms and the randomized SPLIT algorithm
---

The move-to-front rule (MTF) serves a sequence of accesses to a linked list: after it reaches the requested item, it moves that item to the front. For the [list update problem](/list-update-problem/), Sleator and Tarjan proved in 1985 that MTF costs at most $2 - 1/n$ times the offline optimum on a list of $n$ items, even when the optimum may reorder the list at a price. No deterministic rule can beat $2 - 2/(n+1)$, so MTF is optimal up to a small term. It is one of the first results of [competitive analysis](/competitive-ratio/).

## In plain words

A list of names is kept in a stack of cards. To find a name, you look at the cards from the top, one at a time. A name deep in the stack costs more time to find. Each time you find a name, you take that card out and put it on top.

Names that you use often stay near the top. A name that you have not used for a long time sinks down. This rule is simple, and it adapts quickly when your interests change. Even against a person who knows all your future searches and arranges the cards in the best way, the rule never does much worse than twice as much work.

## The problem

A list holds $n$ distinct items. A request names an item $x$. To serve it, the algorithm scans from the front, and if $x$ is at position $i$ (counting from $1$), the access costs $i$. After the access, $x$ may move to any position nearer the front for free; these are *free exchanges*. Any swap of two adjacent items at another time costs $1$; these are *paid exchanges*. The total cost of a sequence $\sigma$ of $m$ requests is the sum of the access costs and the paid exchanges. The [list update problem](/list-update-problem/) page gives the full model and its variants.

## The algorithm

```pseudo id=main
MOVE-TO-FRONT(L, σ)
L1  cost ← 0
L2  for each request x in σ do
L3      i ← the position of x in L
L4      cost ← cost + i
L5      move x to the front of L, with i − 1 free exchanges
L6  return cost
```

Line L3 is the scan. Line L5 uses only free exchanges, so MTF never pays for a swap. On a linked list, line L5 is a constant number of pointer changes once the scan has found $x$ and its predecessor.

## Example

The list is $a, b, c, d$, and the requests are $c, c, d, a, c, b$.

| request | position | cost | list after the move | total |
|---|---|---|---|---|
| c | 3 | 3 | c, a, b, d | 3 |
| c | 1 | 1 | c, a, b, d | 4 |
| d | 4 | 4 | d, c, a, b | 8 |
| a | 3 | 3 | a, d, c, b | 11 |
| c | 3 | 3 | c, a, d, b | 14 |
| b | 4 | 4 | b, c, a, d | 18 |

MTF pays $18$. A brute-force search over all lists and exchanges gives the offline optimum $14$. The theorem gives $18 \le 2 \cdot 14 - 6 = 22$.

## Correctness

The proof uses the [potential](/potential-function/) $\Phi$ equal to the number of [inversions](/inversion/) between the list of MTF and the list of any offline algorithm $A$: pairs of items that are in a different order in the two lists. If $x$ is at position $j$ in the list of $A$, at most $j - 1$ items are before $x$ in both lists. Moving $x$ to the front creates at most $j - 1$ inversions and removes all the others in front of it. So the cost plus the change of $\Phi$ is at most $2j - 1$. A paid exchange of $A$ adds at most $1$, and a free exchange of $A$ removes $1$. The sum gives $\mathrm{MTF}(\sigma) \le 2\,\mathrm{cost}_A(\sigma) - m$. The full proof, and the lower bound for every deterministic rule, are below.

## Complexity

Each access takes $O(i)$ time for the scan, and $O(1)$ more time on a linked list for the move. So a sequence costs $O(\mathrm{MTF}(\sigma))$ time, which is $O(mn)$ in the worst case. The extra space is $O(1)$. On an array, the move also takes $O(i)$ time to shift the items.

## Properties

- **2-competitive.** $\mathrm{MTF}(\sigma) \le 2 \cdot \mathrm{OPT}(\sigma) - m \le (2 - \frac{1}{n}) \mathrm{OPT}(\sigma)$, with additive constant $0$, when both start from the same list. The second step uses $\mathrm{OPT}(\sigma) \le nm$.
- **Nearly optimal.** For each deterministic online rule there are sequences with a ratio as near to $2n/(n+1) = 2 - 2/(n+1)$ as wanted. Irani (1991) credits this bound to Karp and Raghavan.
- **At most twice the best static list.** If $S$ is the cost of serving $\sigma$ from a fixed list $L^*$, then $\mathrm{MTF}(\sigma) \le 2S + \mathrm{inv}(L_0, L^*) - m$. The best fixed list orders the items by how often they are requested.
- **No paid exchanges.** MTF uses only free exchanges.
- **Like LRU.** The list of MTF is always in the order of the last access, which is the order that [LRU](/lru/) keeps for paging.

## Variants and improvements

- **Transpose and frequency count.** The [transposition rule](/transposition-rule/) moves the item up by one place, and [frequency count](/frequency-count/) keeps the items sorted by their number of accesses. Neither is competitive.
- **Randomized rules.** Against an [oblivious adversary](/oblivious-adversary/), the rule BIT (one random bit per item, move to front when it flips) is $1.75$-competitive (Reingold, Westbrook and Sleator 1994), and COMB, a mix of BIT and TIMESTAMP, is $1.6$-competitive (Albers, von Stengel and Werchner 1995). No randomized rule beats $1.5$ (Teia 1993).
- **TIMESTAMP.** Albers gave a deterministic rule that is also $2$-competitive and that moves an item only in front of the first item that was accessed at most once since its last access.
- **Move-to-front coding.** The [move-to-front transform](/move-to-front-transform/) of Bentley, Sleator, Tarjan and Wei encodes each symbol by its position in an MTF list. It is a step of the bzip2 compressor.
- **Data structure use.** The [move-to-front heuristic](/move-to-front-heuristic/) for [self-organizing lists](/self-organizing-list/) is the same rule as seen from the data structure side.

## When to use it

Use MTF for small lists of symbols or keys that are searched in order, such as the buckets of a hash table with chaining, a symbol table of a compiler or interpreter, or the list of recent items in a cache. It adapts at once to a change of the access pattern. If the accesses are independent and come from a fixed distribution that does not change, the [transposition rule](/transposition-rule/) has a lower expected cost in the long run (Rivest 1976), but it is not competitive.

## Pitfalls

- **Moving on an array.** On an array, the move of line L5 shifts $i - 1$ items. This doubles the work but does not change the bound. Use a linked list when the moves are frequent.
- **The cost model.** Some authors charge $i - 1$ for an access at position $i$ (the *partial cost model*). The constants of the bounds then change, so compare results only in one model.
- **A one-time scan.** A long scan of rare items moves each of them to the front and pushes the useful items back. MTF has no protection against this, as LRU has none in paging.
- **Comparing with a static optimum only.** A static list can be much worse than the dynamic optimum. The theorem of Sleator and Tarjan is stronger: it compares with the best algorithm that may reorder the list at any time.

## Implementations

## History

McCabe studied move-to-front in 1965 for requests drawn independently from a fixed distribution, and Rivest compared it with transpose in 1976. Bentley and McGeoch proved in 1985 that MTF costs at most twice the best static list on every sequence. In the same year, Sleator and Tarjan proved the stronger bound against every dynamic offline algorithm. Their paper also analysed LRU for paging, and it started the field of competitive analysis. Irani and others later gave the lower bound $2n/(n+1)$ and randomized rules that beat $2$.

## References
