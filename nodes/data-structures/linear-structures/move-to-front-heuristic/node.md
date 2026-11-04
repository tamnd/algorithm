---
tag: ADRSG4
kind: algorithm
slug: move-to-front-heuristic
name: Move-to-front heuristic
aliases:
- MTF
- move-to-front list update
- move-to-front rule
area: data-structures/linear-structures
level: advanced
summary: Moves each accessed element to the front of the list; 2-competitive against optimal static order.
solves: [list-update-problem]
model: word-ram
complexity:
  vars: {n: the number of items in the list}
  time: {worst: Θ(n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, online: true, deterministic: true, recursive: false}
prereqs: [singly-linked-list, competitive-ratio, potential-method]
see_also: [list-access-problem, self-organizing-list, frequency-count, move-to-front-transform, lru-cache, paging-problem, splay-tree, sequential-search-symbol-table]
sources:
  - paper: doi:10.1145/2786.2793
    title: Daniel D. Sleator and Robert E. Tarjan, Amortized efficiency of list update and paging rules, Communications of the ACM 28(2), 1985
    locator: pp. 202 to 208, Theorem 1 and its proof by the number of inversions
  - book: isbn:9780521619462
    title: Allan Borodin and Ran El-Yaniv, Online Computation and Competitive Analysis, Cambridge University Press (1998)
    locator: Chapter 1, Sections 1.2 to 1.5 (the list accessing problem, the Sleator and Tarjan result, the potential function method, lower bounds)
  - paper: doi:10.1145/359997.360000
    title: Ronald L. Rivest, On self-organizing sequential search heuristics, Communications of the ACM 19(2), 1976
    locator: pp. 63 to 67
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.1 (Sequential searching), the part on self-organizing files
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3, Exercise 1.3.40 (Move-to-front)
---

The move-to-front heuristic (MTF) keeps a set of items in a [linked list](/singly-linked-list/), searches for each requested item from the front, and then moves that item to the front of the list. It is an [online algorithm](/online-algorithm/) for the [list update problem](/list-update-problem/): one access costs $\Theta(n)$ time in the worst case on a list of $n$ items, but over any request sequence its total cost is less than twice the cost of the best algorithm that knows the whole sequence in advance. This bound, by Sleator and Tarjan in 1985, is the first result stated with a [competitive ratio](/competitive-ratio/), and it is the standard example of a proof by the [potential method](/potential-method/).

## In plain words

You keep your tools in one row on a shelf. To find a tool, you look along the row from the left until you see it. Each tool that you look at costs you one unit of time. After you use a tool, you put it back at the left end of the row.

Tools that you use often then stay near the left end, so you find them fast. A tool that you have not used for a long time drifts to the right. You do not need to count how often you use each tool, and you do not need to know the future. Even so, a person who knows in advance every tool that you will ask for, and who rearranges the row in the best possible way, can save you less than half of your work.

## The problem

The input is a list $L$ of $n$ distinct items and a sequence of requests $\sigma = x_1, x_2, \ldots, x_m$, each an item of $L$. The requests come one at a time, and each must be served before the next one is seen. This is the [list update problem](/list-update-problem/) in the standard model of Sleator and Tarjan:

- To access the item at position $i$ (the first item is at position 1) costs $i$.
- Right after an access, the algorithm may move the accessed item to any position closer to the front at no cost. Each swap of two neighbours done this way is a *free exchange*.
- At any time, the algorithm may swap two neighbours at a cost of 1. This is a *paid exchange*.

The cost of an algorithm on $\sigma$ is the sum of these costs. Insertions and deletions are a variant, treated below.

## The algorithm

The list is a singly linked list with a head pointer. The call MTF-ACCESS$(L, x)$ serves one request and returns its cost, the position of $x$.

```pseudo id=main
MTF-ACCESS(L, x)                           ▷ precondition: x is in L
L1  prev ← nil, cur ← L.head, i ← 1
L2  while cur.key ≠ x do
L3      prev ← cur, cur ← cur.next, i ← i + 1
L4  if prev ≠ nil then                     ▷ x is not already first
L5      prev.next ← cur.next               ▷ unlink x
L6      cur.next ← L.head                  ▷ relink x at the front
L7      L.head ← cur
L8  return i
```

Lines L1 to L3 are a [linear search](/linear-search/) that also keeps a pointer to the node before the current one. The loop stops at the node of $x$, which exists by the precondition, and $i$ is then its position. Lines L5 to L7 unlink that node and put it in front of the old head. They change three pointers and do not depend on $n$. When $x$ is already first, $prev$ is nil and the list does not change. In the cost model, the move uses $i - 1$ free exchanges, so the cost of the request is $i$, the value of line L8.

## Example

Start with the list $a, b, c, d, e$ and serve the requests $d, b, d, e, a, d, b$.

| request | position (cost) | list after the move | total cost |
|---|---|---|---|
| $d$ | 4 | $d, a, b, c, e$ | 4 |
| $b$ | 3 | $b, d, a, c, e$ | 7 |
| $d$ | 2 | $d, b, a, c, e$ | 9 |
| $e$ | 5 | $e, d, b, a, c$ | 14 |
| $a$ | 4 | $a, e, d, b, c$ | 18 |
| $d$ | 3 | $d, a, e, b, c$ | 21 |
| $b$ | 4 | $b, d, a, e, c$ | 25 |

The list that never changes costs $4 + 2 + 4 + 5 + 1 + 4 + 2 = 22$ on the same requests. The best fixed order for this sequence is $d, b, a, e, c$, which costs 14. To reach it from $a, b, c, d, e$ takes 5 paid exchanges (the number of pairs in a different order), so this offline plan costs 19. The bound of the Complexity section, with $C_A = 14$, $X_A = 5$, $F_A = 0$ and $m = 7$, gives $C_{\mathrm{MTF}} \le 2 \cdot 14 + 5 - 0 - 7 = 26$, and MTF pays 25.

On requests with locality MTF wins by far. Ten requests for $e$ cost $5 + 9 \cdot 1 = 14$ with MTF and $10 \cdot 5 = 50$ with the fixed list.

## Correctness

MTF-ACCESS$(L, x)$ returns the position $i$ of $x$ in $L$, and after the call $L$ holds $x$ followed by the other items in their old order. The proof uses the [loop invariant](/loop-invariant/) of line L2: $cur$ is the node at position $i$, the keys at positions 1 to $i - 1$ are not $x$, and $prev$ is the node at position $i - 1$ (nil when $i = 1$). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time of one request.** The loop of lines L2 and L3 runs $i - 1$ times, and every other line runs at most once in $\Theta(1)$ time. So one request takes $\Theta(i)$ time on the [word RAM](/word-ram/), where $i$ is the position of the item. This is $\Theta(n)$ in the worst case (the last item) and $\Theta(1)$ in the best case (the first item). The extra space is $\Theta(1)$: three variables.

**The competitive bound.** Let $A$ be any algorithm, online or offline, that starts from the same list and serves the same sequence $\sigma$ of $m$ requests. Let $C_A(\sigma)$ be the sum of the access costs of $A$, $X_A(\sigma)$ the number of its paid exchanges, and $F_A(\sigma)$ the number of its free exchanges. Then

$$C_{\mathrm{MTF}}(\sigma) \le 2\, C_A(\sigma) + X_A(\sigma) - F_A(\sigma) - m.$$

The proof uses the potential $\Phi$, the number of [inversions](/inversion/) of the list of MTF with respect to the list of $A$: pairs of items that are in a different order in the two lists. If $x$ is at position $k$ for MTF and $i$ for $A$, and $v$ items are before $x$ for MTF but after $x$ for $A$, the move to the front creates $k - 1 - v$ inversions and removes $v$, so the amortized cost of the access is $k + (k - 1 - v) - v = 2(k - 1 - v) + 1 \le 2i - 1$. A free exchange of $A$ removes one inversion and a paid exchange adds at most one. The details are in [the complexity proof](proofs/complexity.md).

Since the total cost of $A$ is $C_A + X_A$, the bound gives $C_{\mathrm{MTF}}(\sigma) \le 2\,(C_A(\sigma) + X_A(\sigma)) - m$. So MTF is 2-competitive, with no additive constant, against every algorithm, including the offline optimum.

**A lower bound for every online algorithm.** No deterministic online algorithm is $\alpha$-competitive with $\alpha < 2n/(n + 1) = 2 - 2/(n + 1)$. The adversary always requests the last item of the list of the online algorithm, which then pays $n$ per request, while some fixed order pays at most $(n+1)/2$ per request on average. The proof is in the same file. So the factor 2 of MTF cannot be improved by much for long lists.

**Independent requests.** Assume that each request is item $j$ with probability $p_j$, independently of the others, and that each $p_j > 0$. In the long run, MTF has expected access cost

$$E_{\mathrm{MTF}} = 1 + 2 \sum_{j < k} \frac{p_j\, p_k}{p_j + p_k} \le 2\, E_{\mathrm{OPT}} - 1,$$

where $E_{\mathrm{OPT}} = \sum_j j\, p_j$, with the $p_j$ sorted in non-increasing order, is the cost of the best fixed order. The derivation is also in [the complexity proof](proofs/complexity.md). For example, with $p = (1/2, 1/4, 1/8, 1/8)$, $E_{\mathrm{OPT}} = 15/8 = 1.875$ and $E_{\mathrm{MTF}} = 1 + 2 \cdot (1/6 + 1/10 + 1/10 + 1/12 + 1/12 + 1/16) = 263/120 \approx 2.19$, below the bound $2 \cdot 15/8 - 1 = 2.75$.

| measure | cost |
|---|---|
| time of one request, worst case | $\Theta(n)$ |
| time of one request, best case | $\Theta(1)$ |
| extra space | $\Theta(1)$ |
| total cost against any algorithm $A$ | $\le 2\,(C_A + X_A) - m$ |
| lower bound on the ratio of any deterministic online algorithm | $2 - 2/(n + 1)$ |
| expected cost under independent requests | $\le 2\, E_{\mathrm{OPT}} - 1$ |

## Properties

- **Online.** Each move uses only the current request.
- **Memoryless.** MTF keeps no counters and no history beyond the order of the list. Compare [frequency count](/frequency-count/), which keeps one counter per item.
- **In place.** The move changes three pointers in the list itself.
- **Deterministic.** The same requests give the same list and the same cost.
- **Adapts to locality.** An item that is requested again soon is near the front. When $x$ is requested again, the items before it are exactly the distinct items requested since the previous request for $x$.

## Variants and improvements

- **Transpose.** Swap the accessed item with the one just before it. Rivest proved that under independent requests its stationary cost is at most that of MTF, but it is not competitive: requests that alternate between the last two items cost $n$ each forever. See [self-organizing list](/self-organizing-list/).
- **Frequency count.** Keep the list sorted by the number of accesses. It converges to the best fixed order under independent requests, and it is not competitive either.
- **Insert and delete.** In the full model of Sleator and Tarjan, inserting an item costs $n + 1$ (a scan to the end) and deleting the item at position $i$ costs $i$. MTF inserts a new item at the front. The same potential argument gives the same bound with these operations.
- **Randomized algorithms.** Against an oblivious adversary, randomized rules do better than 2. The algorithm BIT keeps one random bit per item and moves an item to the front on every second access; it is $1.75$-competitive (Reingold, Westbrook and Sleator). See Chapter 2 of Borodin and El-Yaniv.
- **Move-to-front transform.** The [move-to-front transform](/move-to-front-transform/) outputs the position of each symbol before the move. It turns the output of the [Burrows and Wheeler transform](/burrows-wheeler-transform/) into many small numbers.
- **The array form.** Sedgewick and Wayne apply the rule to an array symbol table: shift the items before the found one right by one, then write it at index 0. The cost is again $\Theta(i)$.

## When to use it

Use MTF when you keep a small set in a list and the requests have locality, for example a short cache, the buckets of a hash table with [separate chaining](/separate-chaining/), or a symbol table of recent identifiers. It needs no extra memory and no tuning, and its cost is never worse than twice the best possible. If the requests are independent and their probabilities are stable, transpose or frequency count may have a lower expected cost. If the list is large, a [hash table](/hash-table/) or a balanced search tree gives each access in $O(1)$ expected or $O(\log n)$ time, and a [splay tree](/splay-tree/) gives a similar adaptive behaviour in a tree.

## Pitfalls

- **Losing the predecessor.** A search that keeps only $cur$ cannot unlink the found node in a singly linked list. Line L3 must update $prev$ before $cur$: `prev ← cur, cur ← cur.next`.
- **Moving the first item.** Without the test of line L4, the call on the first item runs line L6 with $cur = L.head$ and makes $cur.next = cur$, a cycle of one node. Skip the move when $prev = nil$.
- **The wrong order of the pointer changes.** Running line L7 before line L6 sets $cur.next \leftarrow cur$ and loses the rest of the list. Change $cur.next$ while $L.head$ still points to the old first node.
- **Counting from 0.** The cost model counts positions from 1. A 0-based count makes the total smaller by $m$, and then the inequality $C_{\mathrm{MTF}} \le 2C_A + X_A - F_A - m$ seems to fail.
- **Comparing with the wrong offline cost.** The bound compares MTF with $A$ from the same start list. A fixed order that differs from the start must pay for its exchanges, as in the example.

## Implementations

## History

The rule appears in the study of self-organizing files in the 1960s. McCabe analyzed move-to-front under independent requests in 1965, and Rivest in 1976 compared it with transpose and showed that both are within a constant factor of the best fixed order (Knuth, Section 6.1, describes these results). Sleator and Tarjan in 1985 gave the amortized bound against every algorithm on every sequence. With the same paper they introduced what is now called competitive analysis, and they applied it also to paging, where the analogous rule is LRU.

## References
