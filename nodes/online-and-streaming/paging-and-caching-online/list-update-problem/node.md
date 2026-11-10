---
tag: M801WK
kind: problem
slug: list-update-problem
name: List update problem
aliases:
- Online list update
- list update problem
- self-organizing list problem
- self-organizing lists
- list accessing problem
area: online-and-streaming/paging-and-caching-online
level: advanced
summary: Maintain a list under accesses, reordering it online so that access costs stay low.
prereqs: [competitive-ratio, online-algorithm, offline-optimum]
see_also: [move-to-front, transposition-rule, frequency-count, self-organizing-list, move-to-front-heuristic, independent-reference-model, paging-problem, splay-tree]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the cost model with free and paid exchanges, and the theorem that move-to-front costs at most twice the optimum
  - paper: doi:10.1145/3894.3896
    title: "Jon L. Bentley and Catherine C. McGeoch, Amortized analyses of self-organizing sequential search heuristics, Communications of the ACM 28(4) (1985), 404-411"
    locator: the comparison with the optimal static list, the bound of twice its cost for move-to-front, and the bad cases for transpose
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1 (the list accessing problem, the static optimum, move-to-front, the deterministic lower bound) and Chapter 2 (randomized list accessing, BIT and the lower bounds)
  - paper: doi:10.1145/359997.360000
    title: "Ronald L. Rivest, On self-organizing sequential search heuristics, Communications of the ACM 19(2) (1976), 63-67"
    locator: move-to-front and transpose under independent random accesses
  - paper: "Sandy Irani, Two results on the list update problem, Information Processing Letters 38(6) (1991), 301-306"
    locator: the lower bound 2n/(n + 1) for deterministic algorithms and the randomized SPLIT algorithm
  - paper: "Christoph Ambühl, Offline list update is NP-hard, Proceedings of ESA 2000, Lecture Notes in Computer Science 1879, Springer, 42-51"
    locator: the NP-hardness of the offline problem
  - paper: doi:10.1007/978-3-642-40273-9_17
    title: "Shahin Kamali and Alejandro López-Ortiz, A survey of algorithms and models for list update, in: Space-Efficient Data Structures, Streams, and Algorithms, Lecture Notes in Computer Science 8066, Springer, 2013"
    locator: the overview of the cost models, the deterministic and randomized bounds, and the offline problem
---

The list update problem asks how to keep a linked list of $n$ items in a good order while requests for items arrive one at a time. A request for the item at position $i$ costs $i$, the number of items scanned, and after each request the item may move toward the front for free. Other changes of the order cost $1$ for each swap of two neighbours. Sleator and Tarjan (1985) made it a central example of competitive analysis: [move-to-front](/move-to-front/) costs at most twice the offline optimum, and no deterministic rule does much better. If the list may not change at all, the best fixed order is by decreasing frequency of access.

## In plain words

You keep a pile of papers on your desk. Each time you need a paper, you search from the top, and a paper deep in the pile takes longer to find. After you use a paper, you can put it back anywhere above its old place at no cost. Moving other papers around takes extra work.

The question is how to arrange the pile when you do not know which papers you will need next. One simple habit is to put each paper on top after you use it. This habit is never worse than twice the best plan made with full knowledge of the future. If you knew how often you need each paper but had to fix the order once, the best choice is the most used paper on top, then the next most used, and so on.

## Definition

**Input.** A list $L_0$ of $n$ distinct items and a request sequence $\sigma = \sigma_1, \ldots, \sigma_m$ of items of the list.

**Cost model (the standard or full cost model of Sleator and Tarjan).**

- *Access.* A request for the item at position $i$ (the front is position $1$) costs $i$.
- *Free exchanges.* Right after an access, the accessed item may move to any position closer to the front, at no cost.
- *Paid exchanges.* At any time, two neighbouring items may be swapped, for a cost of $1$.

An algorithm $A$ pays $A(\sigma) = \sum (\text{access costs}) + (\text{number of paid exchanges})$. An online algorithm decides its exchanges after each request with no knowledge of later requests. The offline optimum $\mathrm{OPT}(\sigma)$ is the least cost of any sequence of exchanges. An algorithm is $c$-competitive if $A(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all $\sigma$, for a constant $b$ that may depend on $n$.

**The static problem.** The list may be put in any order once, before the first request, at no cost, and it may not change after that. The static cost of an order $\pi$ is $\sum_t \mathrm{pos}_\pi(\sigma_t)$, and the static optimum is the least static cost over all $n!$ orders.

## Variants

- **Partial cost model.** An access to position $i$ costs $i - 1$, the number of comparisons with other items. Ratios in this model are a little different for small $n$, but the main results are the same.
- **Dynamic lists.** Requests may also insert an item, for a cost of $n + 1$, at the end of the list, or delete an item, for the cost of an access. The bound for move-to-front still holds.
- **Paid exchanges with a different cost.** In the $P^d$ model of Reingold, Westbrook and Sleator, a paid exchange costs $d$ instead of $1$.
- **Free exchanges only.** Many simple rules, such as move-to-front, transpose and frequency count, use only free exchanges. Sleator and Tarjan prove their bound against an optimum that may also use paid exchanges.
- **Independent requests.** In the probabilistic model of McCabe and Rivest, each request is item $j$ with a fixed probability $p_j$, independent of the others ([independent reference model](/independent-reference-model/)). Then the expected cost per request of a fixed order is $\sum_j p_j \, \mathrm{pos}(j)$, and the rules are compared by their long-run expected cost.

## Examples

**One sequence, several rules.** The list is $a, b, c, d$ and the requests are $c, c, d, a, c, b$. The costs, computed by scripts:

| rule | cost |
|---|---|
| never move (the order $a, b, c, d$) | 16 |
| [move-to-front](/move-to-front/) | 18 |
| [frequency count](/frequency-count/) | 16 |
| [transpose](/transposition-rule/) | 17 |
| offline optimum, from $a, b, c, d$ | 14 |
| static optimum, order $c, a, b, d$ | 12 |

The optimum first moves $c$ to the front with $2$ paid exchanges, and then serves all requests in the order $c, a, b, d$ for $3 + 2 + 3 + 4 = 12$, so it pays $14$. The static optimum gets the same order for free, so it pays $12$. Here MTF pays $18 \le 2 \cdot 14$, inside the bound of Sleator and Tarjan.

**Why transpose fails.** With the list $x_1, \ldots, x_n$, request $x_n, x_{n-1}, x_n, x_{n-1}, \ldots$ for $m$ requests. Transpose swaps the two last items each time, so each request costs $n$. Move-to-front pays $n$ twice and then $2$ each time. So transpose pays about $n m$ and the optimum at most $2 m + O(n^2)$, a ratio of about $n/2$. The [transposition rule](/transposition-rule/) page gives a sharper bad case.

## Known algorithms

- **[Move-to-front](/move-to-front/).** After each access, move the item to the front. It is $2$-competitive: $\mathrm{MTF}(\sigma) \le 2 \cdot \mathrm{OPT}(\sigma) - m$ when both start from the same list (Sleator and Tarjan 1985). It is also within a factor $2$ of the static optimum (Bentley and McGeoch 1985).
- **TIMESTAMP (Albers 1998).** After an access to $x$, move $x$ just in front of the first item that precedes $x$ in the list and was accessed at most once since the last access to $x$. If there is no such item, or if this is the first access to $x$, do nothing. It is also $2$-competitive and deterministic.
- **[Transpose](/transposition-rule/) and [frequency count](/frequency-count/).** Transpose swaps the item with the one before it. Frequency count keeps the list sorted by the number of accesses so far. Neither is competitive: both have ratio $\Omega(n)$ on some sequences.
- **Randomized rules.** Against an [oblivious adversary](/oblivious-adversary/), BIT keeps one random bit for each item, flips it at each access and moves the item to the front when the bit becomes $1$. It is $1.75$-competitive (Reingold, Westbrook and Sleator 1994). COMB, a random mix of BIT and TIMESTAMP, is $1.6$-competitive (Albers, von Stengel and Werchner 1995). Irani's SPLIT was the first randomized rule below $2$.
- **Offline algorithms.** The optimum can be found by dynamic programming over the $n!$ orders of the list, in time that is exponential in $n$ but linear in $m$. Reingold and Westbrook (1996) showed that an optimal schedule can use paid exchanges only.

## Bounds

**Theorem 1 (static optimality).** For a fixed request sequence, let $f_x$ be the number of requests for item $x$. An order is a static optimum if and only if it lists the items by decreasing frequency, with ties in any order. Its cost is $\sum_{i=1}^{n} i \cdot f_{(i)}$, where $f_{(1)} \ge f_{(2)} \ge \cdots \ge f_{(n)}$ are the sorted frequencies.

*Proof.* The static cost of an order $\pi$ is $\sum_t \mathrm{pos}_\pi(\sigma_t) = \sum_x f_x \, \mathrm{pos}_\pi(x)$, since each request for $x$ costs $\mathrm{pos}_\pi(x)$. Suppose that $x$ is at position $i$ and $y$ at position $j > i$ with $f_x < f_y$. Swap $x$ and $y$. Only their two terms change, from $f_x i + f_y j$ to $f_x j + f_y i$, a change of $(j - i)(f_x - f_y) < 0$. So an order with such a pair is not optimal, and each optimal order is sorted by decreasing frequency. All sorted orders have the same cost $\sum_i i \cdot f_{(i)}$, because they differ only in the order of equal frequencies. Some order is optimal, since there are finitely many, so each sorted order is optimal. $\blacksquare$

The same exchange argument, applied to probabilities, shows that under independent requests the best fixed order is by decreasing probability $p_j$ (McCabe 1965).

**Deterministic bounds.** Move-to-front and TIMESTAMP are $2$-competitive. No deterministic online algorithm is better than $2n/(n+1)$-competitive: an adversary that always requests the last item of the list forces a cost of $n$ for each request, while the average cost of all $n!$ static orders is $(n + 1)/2$ for each request (Karp and Raghavan, in Irani 1991). So the best deterministic ratio lies between $2n/(n+1)$ and $2$.

**Randomized bounds.** The best known ratio is $1.6$ (COMB), and the best lower bound is $1.5$ (Teia 1993), for lists of many items. The gap between $1.5$ and $1.6$ is open.

**The offline problem.** Computing $\mathrm{OPT}(\sigma)$ is NP-hard (Ambühl 2000). The static optimum is easy by Theorem 1: count the requests and sort, in $O(m + n \log n)$ time.

**Independent requests.** If requests are independent with fixed probabilities, transpose has a long-run expected cost at most that of move-to-front (Rivest 1976), and move-to-front costs at most $\pi/2$ times the best fixed order (Chung, Hajela and Seymour 1988). In this model, frequency count tends to the optimal static order. These results show that the probabilistic and the competitive views can rank the rules in opposite ways.

## Reductions

- **Relation to paging.** Paging is like list update on a list where only the first $k$ positions are cheap. Sleator and Tarjan treated both in the same paper, and the analysis of LRU uses the same idea as the analysis of move-to-front: compare the order of last use.
- **Pairwise independence.** For many rules, such as move-to-front, BIT and TIMESTAMP, the relative order of two items $x$ and $y$ depends only on the requests to $x$ and $y$. The cost then splits into a sum over pairs, and it is enough to analyse lists of two items. This is the main method for the randomized bounds.
- **Splay trees.** A [splay tree](/splay-tree/) is the analogue of move-to-front for binary search trees, and the static optimality theorem of splay trees is the analogue of Theorem 1.

## Applications

- **Self-organizing lists.** Small symbol tables and caches in linked lists use move-to-front so that frequent keys stay near the front; see [self-organizing list](/self-organizing-list/) and the [move-to-front heuristic](/move-to-front-heuristic/).
- **Data compression.** The [move-to-front transform](/move-to-front-transform/) codes each symbol by its position in a list under move-to-front. After a Burrows-Wheeler transform, frequent symbols get small numbers.
- **Collision chains in hash tables.** Chains can be kept as self-organizing lists.

## References
