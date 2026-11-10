---
tag: T7XGDD
kind: algorithm
slug: transposition-rule
name: Transposition rule
aliases:
- Transpose heuristic
- transpose heuristic
- transposition heuristic
- transpose
- TRANS
area: online-and-streaming/paging-and-caching-online
level: core
summary: Swaps each accessed element with its predecessor; it is not competitive.
solves: [list-update-problem]
model: word-ram
complexity:
  vars: {m: the number of requests, n: the length of the list}
  time: {worst: O(m n)}
  space: {extra: O(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1976
  people: [Ronald L. Rivest]
  note: Rivest proved in 1976 that, under independent requests from a fixed distribution, transpose has an expected cost at most that of move-to-front. Sleator and Tarjan noted in 1985 that it is not competitive.
prereqs: [list-update-problem, competitive-ratio]
see_also: [move-to-front, frequency-count, self-organizing-list, move-to-front-heuristic, list-access-problem]
sources:
  - paper: doi:10.1145/359997.360000
    title: "Ronald L. Rivest, On self-organizing sequential search heuristics, Communications of the ACM 19(2) (1976), 63-67"
    locator: the transposition rule and the proof that its expected cost under independent requests is at most that of move-to-front
  - paper: doi:10.1145/2786.2793
    title: "Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2) (1985), 202-208"
    locator: the remark that transpose and frequency count are not competitive, next to the analysis of move-to-front
  - book: isbn:9780521563925
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press, 1998
    locator: Chapter 1, the list accessing problem, the sections on TRANS and FC
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1, sequential searching, the self-organizing file and the transposition method
---

The transposition rule (transpose, TRANS) serves a sequence of accesses to a list: after it reaches the requested item, it swaps that item with the one just before it. It moves an item toward the front by only one place for each access, so a list changes slowly. For the [list update problem](/list-update-problem/) it is not competitive: on a list of $n$ items, a simple sequence makes it pay about $2n/3$ times the optimum. Under independent requests from a fixed distribution, it has a lower expected cost than [move-to-front](/move-to-front/) in the long run.

## In plain words

You keep a stack of cards with names, and you search from the top. Each time you find a name, you swap its card with the card just above it. A name that you use often climbs slowly to the top, one place at a time, and it stays there.

This is careful and stable. One rare search does not disturb the order much. But an opponent can use the slowness. If the opponent always asks for the bottom card, the two bottom cards swap again and again, and each search goes through the whole stack. A smarter plan moves those two cards to the top once and then pays almost nothing.

## The problem

A list holds $n$ distinct items. An access to the item at position $i$ costs $i$. After the access, the item can move nearer the front by free exchanges, and other swaps of adjacent items cost $1$ each. The total cost of a sequence of $m$ requests is the sum of these costs. The [list update problem](/list-update-problem/) page defines the model.

## The algorithm

```pseudo id=main
TRANSPOSE(L, σ)
L1  cost ← 0
L2  for each request x in σ do
L3      i ← the position of x in L
L4      cost ← cost + i
L5      if i > 1 then
L6          swap x with the item at position i − 1        ▷ one free exchange
L7  return cost
```

Line L6 is one free exchange. The rule never uses paid exchanges. On an array, line L6 is a swap of two cells, so transpose is easy to build without pointers.

## Example

The list is $a, b, c, d$, and the requests are $c, c, d, a, c, b$, the same as on the [move-to-front](/move-to-front/) page.

| request | position | cost | list after the swap | total |
|---|---|---|---|---|
| c | 3 | 3 | a, c, b, d | 3 |
| c | 2 | 2 | c, a, b, d | 5 |
| d | 4 | 4 | c, a, d, b | 9 |
| a | 2 | 2 | a, c, d, b | 11 |
| c | 2 | 2 | c, a, d, b | 13 |
| b | 4 | 4 | c, a, b, d | 17 |

Transpose pays $17$ here, move-to-front pays $18$, and the offline optimum is $14$. On this short sequence transpose is not bad. The next section shows a sequence where it is.

**The bad sequence.** Start from the list $1, 2, \ldots, n$ and request $n, n-1, n, n-1, \ldots$, which is always the item that is last at that moment. The request for $n$ costs $n$ and swaps $n$ and $n - 1$. Then $n - 1$ is last, costs $n$, and swaps them back. So transpose pays $n$ for each of the $m$ requests. The optimum moves $n$ and $n - 1$ to the front at the first two requests, for a cost of $2n$, and then pays $2$ and $1$ in turn, so

$$\mathrm{OPT}(\sigma) \le 2n + \tfrac{3}{2}(m - 2) + 1, \qquad \frac{\mathrm{TRANS}(\sigma)}{\mathrm{OPT}(\sigma)} \to \frac{2n}{3} \quad (m \to \infty).$$

For $n = 5$ and $m = 12$, transpose pays $60$ and an exact search gives $\mathrm{OPT} = 24$.

## Correctness

Transpose serves each request, because line L3 finds the item and line L6 only swaps two items. The page claim is that it is not competitive. For each $n$, the bad sequence above gives $\mathrm{TRANS}(\sigma) = nm$, while $\mathrm{OPT}(\sigma) \le 2n + \frac{3}{2}(m-2) + 1$. So no bound $\mathrm{TRANS}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ can hold with $c < 2n/3$, and no constant $c$ works for all $n$. The full proof is below.

## Complexity

An access to position $i$ takes $O(i)$ time for the scan and $O(1)$ time for the swap. The total time is $O(\mathrm{TRANS}(\sigma))$, which is $O(mn)$, and the extra space is $O(1)$.

## Properties

- **Not competitive.** The ratio is at least about $2n/3$ on a list of $n$ items. Every rule on such a list has ratio at most $n$, since each access costs at least $1$ and at most $n$, so the ratio of transpose is $\Theta(n)$.
- **Good on a fixed distribution.** If the requests are independent and each item $x$ is requested with a fixed probability $p_x$, the expected cost per access in the stationary state of transpose is at most that of move-to-front (Rivest 1976).
- **Slow to adapt.** An item needs up to $n - 1$ accesses to reach the front. After a change of the distribution, transpose needs a long time to reach its new stationary order.
- **Free exchanges only.** Transpose uses one free exchange per access and never pays for a swap.

## Variants and improvements

- **Move-to-front.** The [move-to-front rule](/move-to-front/) moves the item all the way, and it is $2$-competitive.
- **Frequency count.** [Frequency count](/frequency-count/) keeps the items in decreasing order of their number of accesses. It is also not competitive, but it tends to the best static order on a fixed distribution.
- **Move-ahead-k.** Move the item $k$ places forward. This is between transpose ($k = 1$) and move-to-front ($k = n$). For each fixed $k$, the bad sequence of the last $k + 1$ items shows that it is not competitive either.
- **Counter and batched rules.** Move an item to the front only on every $c$-th access to it. These rules mix the stability of transpose with the speed of move-to-front.

## When to use it

Use transpose only when the requests are close to independent draws from a stable distribution and the list is short, such as a fixed table of keywords. It is also useful as a teaching example: it is the classic case where an average-case analysis and a worst-case [competitive analysis](/competitive-ratio/) give opposite advice. When the access pattern can change, or when an adversary can choose it, use [move-to-front](/move-to-front/).

## Pitfalls

- **Trusting the average case.** Rivest's result is about the expected cost under a fixed distribution. It says nothing about a sequence chosen by an opponent, where transpose is very bad.
- **Slow convergence.** Even under a fixed distribution, the time to reach the stationary order can be long, and in that time transpose can cost more than move-to-front.
- **The first item.** An access to the first item must not swap. Line L5 checks this. A program that swaps with index $i - 2$ without the check reads outside the list.

## Implementations

## History

Transpose appears with move-to-front in the early work on self-organizing files in the 1960s and 1970s. Rivest proved in 1976 that, under independent requests, transpose is at least as good as move-to-front in the stationary state, and he conjectured that it is the best of a wide family of rules. Anderson, Nash and Weber found a counterexample to this conjecture in 1982. Knuth discussed both rules in Volume 3. Sleator and Tarjan pointed out in 1985 that transpose and frequency count are not competitive, while move-to-front is, which made the list update problem a standard example of the gap between average-case and worst-case analysis.

## References
