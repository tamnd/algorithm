---
tag: E8G97Z
kind: algorithm
slug: frequency-count
name: Frequency count
aliases:
- sorted by frequency
- FC
- count heuristic
- frequency count rule
area: online-and-streaming/competitive-analysis
level: core
summary: Keeps the list sorted by access count; it is close to the best fixed list, but it is not competitive against the best dynamic list.
solves: [list-update-problem]
model: word-ram
complexity:
  vars: {m: the number of requests, n: the length of the list}
  time: {worst: O(m n)}
  space: {extra: O(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1985
  people: [Daniel D. Sleator, Robert E. Tarjan, Jon L. Bentley, Catherine C. McGeoch]
  note: The rule is older and was studied for independent requests in the 1960s and 1970s. In 1985 Bentley and McGeoch compared it with the best fixed list, and Sleator and Tarjan pointed out that it is not competitive against the best dynamic list.
prereqs: [list-update-problem, competitive-ratio]
see_also: [move-to-front, transposition-rule, self-organizing-list, list-access-problem, independent-reference-model, lfu, move-to-front-heuristic, adversary-argument]
sources:
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the cost model with free and paid exchanges, and the remark that frequency count and transpose are not competitive
  - paper: doi:10.1145/3894.3896
    title: "Jon L. Bentley and Catherine C. McGeoch, Amortized analyses of self-organizing sequential search heuristics, Communications of the ACM 28(4) (1985), 404-411"
    locator: the comparison of move-to-front, transpose and frequency count with the best fixed list
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1, the list accessing problem, and the examples that show that frequency count and transpose are not competitive
  - paper: "Ronald L. Rivest, On self-organizing sequential search heuristics, Communications of the ACM 19(2) (1976)"
    title: "Rivest, On self-organizing sequential search heuristics (1976)"
    locator: the analysis of self-organizing rules when requests are independent with fixed probabilities
---

Frequency count is a rule for the [list update problem](/list-update-problem/). It keeps a counter for each item of a list. After an access, it increments the counter of the accessed item and moves the item forward past every item with a smaller count, so the list stays sorted by decreasing count. The rule is the online version of the best fixed list, which sorts the items by how often they are requested. Its cost is never much more than twice the cost of that fixed list. But it is not competitive in the sense of Sleator and Tarjan: an adversary can make it pay about $n/6$ times the cost of the best dynamic algorithm on a list of $n$ items, and this factor grows without bound. The reason is that old counts never fade, so the rule cannot follow a change of the requests. [Move-to-front](/move-to-front/) has no counters and is $2$-competitive.

## In plain words

A librarian keeps one shelf of books, and readers ask for the books one at a time. To give a book, the librarian walks along the shelf from the left until the book is found, and longer walks take more time.

The librarian keeps a tally for each book. After each request, the tally of the book goes up, and the book moves to the left past every book with a smaller tally. So the most popular books are always at the left.

This is a good plan when the readers always like the same books. It is a bad plan when their taste changes. A book that was popular last year keeps a high tally, so a book that is popular now must wait a long time before it passes it. A librarian who always puts the last book at the left end adapts at once.

## The problem

**Notation.** The list holds $n$ distinct items. The request sequence $\sigma$ has $m$ requests, each to an item of the list. An access to the item at position $i$ costs $i$. After an access, the accessed item may move forward at no cost (a free exchange); any other swap of two adjacent items costs $1$ (a paid exchange). $f_x$ is the number of requests to $x$. $\mathrm{SOPT}(\sigma)$ is the cost of the best fixed list for $\sigma$, and $\mathrm{OPT}(\sigma)$ is the cost of the best offline algorithm that starts from the same list.

An online algorithm sees one request at a time and must reorder the list before it sees the next one. It is $c$-competitive if $\mathrm{ALG}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for a constant $b$ and all $\sigma$; see [competitive ratio](/competitive-ratio/). The [list update problem](/list-update-problem/) page gives the full model with insertions and deletions.

## The algorithm

```pseudo id=main
FREQUENCY-COUNT(L, σ)
L1  cost ← 0
L2  count[x] ← 0 for every item x of L
L3  for each request x of σ do
L4      i ← the position of x in L
L5      cost ← cost + i
L6      count[x] ← count[x] + 1
L7      while i > 1 and count[L[i − 1]] < count[x] do
L8          swap L[i − 1] and L[i]; i ← i − 1
L9  return cost, L
```

The move in lines L7 and L8 uses only free exchanges. Since the list is sorted by count before the access, the loop moves $x$ past the block of items whose count is equal to the old count of $x$, and it stops behind the items whose count is at least the new count. Among items with equal counts, the item that reached the count first is ahead.

## Example

The list is $a, b, c, d$ and the requests are $c, c, d, a, c, b$.

| request | position | cost | counts after $(a, b, c, d)$ | list after |
|---|---|---|---|---|
| $c$ | $3$ | $3$ | $0, 0, 1, 0$ | $c, a, b, d$ |
| $c$ | $1$ | $1$ | $0, 0, 2, 0$ | $c, a, b, d$ |
| $d$ | $4$ | $4$ | $0, 0, 2, 1$ | $c, d, a, b$ |
| $a$ | $3$ | $3$ | $1, 0, 2, 1$ | $c, d, a, b$ |
| $c$ | $1$ | $1$ | $1, 0, 3, 1$ | $c, d, a, b$ |
| $b$ | $4$ | $4$ | $1, 1, 3, 1$ | $c, d, a, b$ |

Frequency count pays $16$. Move-to-front pays $18$ on the same input, the best offline algorithm pays $14$, and the best fixed list $c, d, a, b$ pays $12$ if it is set up for free.

**The bad sequence.** On the list $x_1, \ldots, x_n$, request $x_1$ exactly $n$ times, then $x_2$ exactly $n - 1$ times, and so on, down to one request to $x_n$. Frequency count never moves an item, because each item has a smaller count than the item just ahead of it. It pays $\sum_i i (n - i + 1) = n(n + 1)(n + 2)/6$. Move-to-front pays $n$ for each item, $n^2$ in total. For $n = 3$ and $n = 4$, an exact search over all lists gives $\mathrm{OPT} = n^2$, so the costs are $10$ against $9$ and $20$ against $16$. The ratio grows like $n/6$.

## Correctness

Every request is served, and the list is always a permutation of the items, so the output is valid. The proof shows by induction that the list is always sorted by decreasing count, with ties broken by the time each item reached its count. So the order of two items depends only on the requests to those two items. The cost then splits into one term for each pair of items, and for each pair frequency count pays at most $2 \min(f_x, f_y) + 1$ for the accesses that find the requested item behind the other, while the best fixed list pays $\min(f_x, f_y)$. Summing over the pairs,

$$\mathrm{FC}(\sigma) \le 2\, \mathrm{SOPT}(\sigma) - m + \binom{n}{2}.$$

For the dynamic optimum, the bad sequence above followed by a second part that requests $x_i$ exactly $i$ times brings all counts back to equal values with the list unchanged. Repeating this phase $k$ times makes frequency count pay $k\, n(n + 1)^2 / 2$, while move-to-front plus $n(n - 1)/2$ paid exchanges per phase pays $k(3n^2 - n)$. The ratio $(n + 1)^2 / (6n - 2)$ exceeds every constant for large $n$, and the repetition defeats every additive constant. The correctness proof gives all steps.

## Complexity

Each access scans the list to find $x$ and moves $x$ forward, so it takes $O(n)$ time, and $m$ requests take $O(m n)$ time in the worst case. The rule stores one counter per item, which is $O(n)$ extra space, and the counters grow up to $m$. In the cost model of the problem, the work of the rule is the access cost itself, which is also $O(n)$ per request.

## Properties

- **Not competitive.** On lists of $n$ items, the competitive ratio is at least $(n + 1)^2 / (6n - 2)$, by the repeated bad phase, and at most $n$, because each access costs at most $n$ and every algorithm pays at least $1$ per request.
- **Close to the best fixed list.** The cost is at most $2\,\mathrm{SOPT} - m + n(n - 1)/2$. The factor $2$ is tight: on the list $y, x$, the requests $x, y, y, x, x, y, y, \ldots$ always find the requested item in second place.
- **Optimal for independent requests, in the limit.** If each request is to item $x$ with a fixed probability $p_x$, independently, the counts sort the items by $p_x$ after enough requests, with probability $1$ when the $p_x$ are distinct. Then the expected cost per request tends to that of the best fixed list.
- **Uses only free exchanges.** The rule moves only the accessed item, and only forward.
- **Pairwise independent.** The relative order of two items depends only on the requests to those two items. This is the same property that the standard analysis of move-to-front uses.
- **Deterministic.** So the lower bound of about $2$ for deterministic list update algorithms applies to it too.

## Variants and improvements

- **Move-to-front.** Move the accessed item to the front. It is $2$-competitive, the best possible ratio for deterministic rules up to a lower order term, and it needs no counters; see [move-to-front](/move-to-front/).
- **Transpose.** Swap the accessed item with the one just ahead of it. It also uses no counters, and it is also not competitive; see [transposition rule](/transposition-rule/).
- **Aging counters.** Halve all counts from time to time, or count only the last requests in a window. This lets the rule follow a change of the requests, at the cost of more state.
- **Ties.** Moving past items with equal count, and not only strictly smaller count, gives a slightly different rule. Both versions keep the list sorted by count.
- **Caching.** The same idea for a cache is the [least frequently used](/lfu/) policy, which evicts the item with the smallest count.

## When to use it

Use frequency count when the requests come from a fixed distribution that does not change, and the list is short enough that a counter per item is cheap. Typical uses are small symbol tables, the chains of a hash table, and lists of options that are offered in order of popularity. If the requests have locality, or their distribution changes over time, use [move-to-front](/move-to-front/), which adapts at once and has a guarantee for every sequence.

## Pitfalls

- **No worst-case guarantee.** The bad phase above costs about $n/6$ times the optimum. Do not use the rule when an adversary, or a shift of the workload, can choose the requests.
- **Old counts never fade.** An item that was popular long ago stays near the front. Aging fixes this, but then the static bound above no longer holds in the same form.
- **Strict comparison.** The rule in line L7 moves past strictly smaller counts. If an implementation uses a different tie rule, the costs in the examples change.
- **Counter growth.** The counts grow without bound. In a long run, a fixed width counter can overflow and break the order.
- **Fixed list cost versus offline cost.** The best fixed list is set up for free in $\mathrm{SOPT}$, while $\mathrm{OPT}$ starts from the given list. The two measures are not comparable in general, as the example shows: $\mathrm{SOPT} = 12$ but $\mathrm{OPT} = 14$.

## Implementations

## History

Self-organizing lists were studied in the 1960s and 1970s under the model of independent requests, where frequency count is the natural online version of the best fixed order. Rivest (1976) compared move-to-front and transpose in this model. In 1985 Bentley and McGeoch compared self-organizing rules with the best fixed list for every sequence, and Sleator and Tarjan introduced the comparison with the best dynamic algorithm. In that model move-to-front is $2$-competitive, but frequency count and transpose are not. Borodin and El-Yaniv give the examples in their 1998 book.

## References
