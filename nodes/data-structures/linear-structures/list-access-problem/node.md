---
tag: T5ZQ6T
kind: problem
slug: list-access-problem
name: List access problem
aliases:
- self-organizing list problem
area: data-structures/linear-structures
level: advanced
summary: Serve a sequence of accesses on a list while reordering it to minimise total cost.
prereqs: [linked-list, online-algorithm, competitive-ratio]
see_also: [list-update-problem, move-to-front-heuristic, self-organizing-list, move-to-front-transform, paging-problem, offline-algorithm, splay-tree, static-optimality-theorem]
sources:
  - paper: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985)"
    locator: the cost model with free and paid exchanges, the theorem that move-to-front costs at most twice the optimum, and the examples that transpose and frequency count are not competitive
  - paper: "Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press (1998)"
    locator: Chapter 1 (the list accessing problem), and Chapter 2 on randomized list accessing algorithms
  - paper: "Nick Reingold, Jeffery Westbrook and Daniel D. Sleator, Randomized competitive algorithms for the list update problem, Algorithmica 11(1) (1994)"
    locator: the algorithm BIT and its competitive ratio 1.75
  - paper: "Susanne Albers, Bernhard von Stengel and Ralph Werchner, A combined BIT and TIMESTAMP algorithm for the list update problem, Information Processing Letters 56(3) (1995)"
    locator: the algorithm COMB and its competitive ratio 1.6
  - paper: "Boris Teia, A lower bound for randomized list update algorithms, Information Processing Letters 47(1) (1993)"
    locator: the lower bound 1.5 for randomized algorithms against an oblivious adversary
  - paper: "Christoph Ambühl, Offline list update is NP-hard, European Symposium on Algorithms (ESA 2000), Lecture Notes in Computer Science 1879 (2000)"
    locator: the reduction that shows that computing the offline optimum is NP-hard
  - paper: "Ronald Rivest, On self-organizing sequential search heuristics, Communications of the ACM 19(2) (1976)"
    locator: the probabilistic model with independent requests, and the comparison of move-to-front and transpose
---

The list access problem asks how to keep the items of a [linked list](/linked-list/) in an order that makes a sequence of accesses cheap. Reaching the item at position $i$ costs $i$, and after each access the list may be reordered: the accessed item can move forward for free, and every other swap of two neighbours costs 1. An [online algorithm](/online-algorithm/) sees each request only when it arrives and must reorder without knowing the future. Sleator and Tarjan proved in 1985 that the [move-to-front](/move-to-front-heuristic/) rule costs at most twice the optimal offline cost on every sequence, so its [competitive ratio](/competitive-ratio/) is 2. No deterministic rule does better than $2 - 2/(n + 1)$ on a list of $n$ items, randomized rules reach 1.6, and computing the offline optimum is NP-hard.

## In plain words

You keep a stack of files and look for one file at a time from the top. A file near the top is found fast, a file near the bottom is slow. After you find a file, you may put it back higher in the stack at no cost. Other changes to the order cost you work.

You do not know which file you will need next. A simple rule is to always put the file you just used on top. Files that you use often then stay near the top. The question is how much more this rule, or any other rule, costs than a person who knows all the future requests and arranges the files in the best way.

## Definition

**Input.** A list $L$ of $n$ distinct items in an initial order, and a request sequence $\sigma = \sigma_1 \sigma_2 \cdots \sigma_m$ of items of $L$.

**Cost model.** This is the full cost model of Sleator and Tarjan.

- Serving request $\sigma_t$ when it is at position $i$ (positions start at 1) costs $i$.
- Right after the access, $\sigma_t$ may move to any position closer to the front at no cost. These are the *free exchanges*.
- At any time, two adjacent items may be swapped at a cost of 1. These are the *paid exchanges*.

**Offline version.** Given $L$ and the whole $\sigma$, find a schedule of exchanges with the least total cost $\text{OPT}(\sigma)$.

**Online version.** Serve $\sigma_1, \sigma_2, \ldots$ in order and decide the exchanges after $\sigma_t$ without seeing $\sigma_{t+1}, \ldots$. A deterministic online algorithm $A$ is *$c$-competitive* if there is a constant $b$ with $A(\sigma) \le c \cdot \text{OPT}(\sigma) + b$ for every $\sigma$. A randomized algorithm is $c$-competitive when the same holds for its expected cost, against an oblivious adversary that fixes $\sigma$ in advance.

## Variants

- **Partial cost model.** An access at position $i$ costs $i - 1$, the number of items passed. Lower bounds are often proved in this model; the ratios differ from the full model by terms that vanish as costs grow.
- **[List update problem](/list-update-problem/).** The requests also include insertion of a new item, which costs $n + 1$ in a list of $n$ items, and deletion, which costs as an access. All the competitive results below hold for it as well.
- **Static optimum.** Compare with the best fixed order, chosen with knowledge of $\sigma$ and never changed. Bentley and McGeoch showed that move-to-front costs at most twice the best fixed order.
- **Independent requests.** Each request is item $j$ with a fixed probability $p_j$, independently. The best fixed order sorts by decreasing $p_j$. Move-to-front has expected cost at most $\pi/2$ times this optimum, a result of Chung, Hajela and Seymour; transpose has a lower expected cost than move-to-front in this model (Rivest 1976), but it is not competitive.
- **Paid exchanges only, or free exchanges only.** Some analyses restrict the offline algorithm to one kind. Free exchanges alone are enough for move-to-front, but the offline optimum can need paid exchanges.

## Examples

**A small instance.** The list is $\langle a, b, c \rangle$ and $\sigma = c\,b\,c\,b\,c\,b\,a\,a\,a$, with $m = 9$ requests.

| rule | total cost |
|---|---|
| move-to-front | 19 |
| transpose (swap the item with the one before it) | 21 |
| frequency count (keep the items in order of access count) | 21 |
| best fixed order, $\langle b, c, a \rangle$ | 18 |
| offline optimum | 16 |

Move-to-front pays $3, 3, 2, 2, 2, 2, 3, 1, 1$: the first request for $c$ finds it last, and the first $a$ finds it last after six requests for $b$ and $c$. One optimal schedule pays 1 to swap $a$ and $b$ before the first request, giving $\langle b, a, c \rangle$, and pays 3 to reach $c$, moving it one place forward for free to get $\langle b, c, a \rangle$. The next four requests cost $1 + 2 + 1 + 2 = 6$ for $b, c, b, c$; then it pays 1 to swap $c$ and $a$ and 1 to reach $b$; then it pays 1 to swap $b$ and $a$, giving $\langle a, b, c \rangle$, and the three requests for $a$ cost 1 each. The total is $1 + 3 + 6 + 1 + 1 + 1 + 3 = 16$. The values were computed by a search over all orders after each request.

**The adversary for move-to-front.** Always request the item that is last in the move-to-front list. From $\langle a, b, c \rangle$ this gives $\sigma = (c\,b\,a)^3$. Move-to-front pays $n = 3$ for every request, 27 in total, while the offline optimum is 18. The ratio $27/18 = 3/2 = 2n/(n+1)$ is the deterministic lower bound for $n = 3$.

## Known algorithms

| algorithm | type | competitive ratio | notes |
|---|---|---|---|
| [move-to-front](/move-to-front-heuristic/) | deterministic | 2 | Sleator and Tarjan (1985); best possible up to the term $2/(n+1)$ |
| TIMESTAMP | deterministic | 2 | Albers (1998): move $x$ in front of the first item before it that was requested at most once since the last request for $x$ |
| transpose | deterministic | not competitive | ratio grows with $n$ |
| frequency count | deterministic | not competitive | ratio grows with $n$ |
| BIT | randomized | 1.75 | Reingold, Westbrook and Sleator (1994): one random bit per item, flipped at each access; move to front when it becomes 1 |
| COMB | randomized | 1.6 | Albers, von Stengel and Werchner (1995): BIT with probability 4/5, TIMESTAMP with probability 1/5 |
| offline dynamic program | exact | 1 | over all $n!$ orders after each request, so time exponential in $n$ and linear in $m$ |

**Why move-to-front is 2-competitive.** Let $\Phi$ be the number of *inversions* between the move-to-front list and the list of the optimal algorithm, the pairs of items that the two lists put in different orders. When move-to-front accesses $x$ at position $k$ and the other list has $x$ at position $i$, at most $i - 1$ of the $k - 1$ items in front of $x$ are also in front of it in the other list. Moving $x$ to the front creates at most $i - 1$ inversions and removes at least $k - i$. So the amortized cost of the access is at most $k + (i - 1) - (k - i) = 2i - 1$. A free exchange of the other algorithm removes an inversion, and a paid exchange creates at most one. Summing over the sequence, $\text{MTF}(\sigma) \le 2\,\text{OPT}(\sigma) - m$ when both lists start equal. The details are on the [move-to-front](/move-to-front-heuristic/) page.

## Bounds

- **Deterministic lower bound.** For every deterministic online algorithm and every $n$, there are sequences with $A(\sigma) \ge (2 - \frac{2}{n + 1}) \cdot \text{OPT}(\sigma) - b$. The adversary always requests the last item of $A$'s list, so $A$ pays $n$ per request, while the average cost of all $n!$ fixed orders, and hence the optimum, is at most $(n + 1)/2$ per request plus a constant.
- **Randomized lower bound.** Teia (1993) proved that no randomized algorithm is better than 1.5-competitive against an oblivious adversary, as $n$ grows. The gap between 1.5 and 1.6 is open.
- **Offline hardness.** Ambühl (2000) proved that computing $\text{OPT}(\sigma)$ is NP-hard. The dynamic program over all orders is exponential in $n$.
- **Upper bound from move-to-front.** $\text{OPT}(\sigma) \le \text{MTF}(\sigma) \le 2\,\text{OPT}(\sigma)$, so move-to-front gives a 2-approximation of the offline optimum in $O(mn)$ time.

## Reductions

- **Paging.** The [paging problem](/paging-problem/) is the closest relative: a cache of $k$ slots is a list in which only membership in the first $k$ positions matters. Sleator and Tarjan analysed both problems in the same paper, and the rule "least recently used" for paging is move-to-front applied to the cache. Its deterministic ratio is $k$.
- **Compression.** The [move-to-front transform](/move-to-front-transform/) outputs, for each symbol, its position in a move-to-front list. The cost of the access sequence is the sum of the output values, so a good list rule gives small numbers that an entropy coder compresses well. This is the second stage of [Burrows-Wheeler](/burrows-wheeler-transform/) compression.
- **Search trees.** A [splay tree](/splay-tree/) is the tree analogue of move-to-front: it moves the accessed key to the root. Its [static optimality](/static-optimality-theorem/) is the analogue of the bound against the best fixed order.

## Applications

- **[Self-organizing lists](/self-organizing-list/).** Symbol tables in interpreters and compilers, the chains of a hash table, and caches of recently used objects keep a short list in move-to-front order.
- **Data compression.** Move-to-front coding after the Burrows-Wheeler transform, as in bzip2.
- **Collision resolution in hashing.** Move-to-front on each chain shortens searches for keys that are used often.
- **A model problem for online algorithms.** The list access problem is, with paging, the standard first example of competitive analysis in textbooks such as Borodin and El-Yaniv.

## References
