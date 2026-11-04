---
tag: PYNHQH
kind: problem
slug: offline-subarray-painting
name: Painting subarrays offline
area: data-structures/disjoint-sets
level: core
summary: Offline problem of painting segments of an array in reverse order with union-find so each cell is painted once, in near-linear time.
prereqs: [disjoint-set-forest, path-compression, offline-algorithm]
see_also: [path-compression, static-tree-set-union, offline-minimum, lazy-propagation, segment-tree, offline-query-processing, arpa-offline-rmq]
sources:
  - url: https://cp-algorithms.com/data_structures/disjoint_set_union.html
    title: cp-algorithms, Disjoint Set Union
    locator: the section Compress jumps along a segment / Painting subarrays offline
  - paper: doi:10.1016/0022-0000(85)90014-5
    title: "Harold N. Gabow and Robert E. Tarjan, A linear-time algorithm for a special case of disjoint set union, Journal of Computer and System Sciences 30(2) (1985), 209-221"
    locator: the interval union-find case, in which each union joins a set with the next one on a line
---

Painting subarrays offline is the problem of finding the final colors of an array of $n$ cells after $m$ operations, each of which paints a contiguous range of cells with a color. A later operation paints over an earlier one. Because only the final colors are asked for, the operations can be read backwards: then each cell takes the color of the first operation that covers it and is never painted again. A [disjoint-set forest](/disjoint-set-forest/) in which each painted cell points to the next cell to its right lets each operation skip the painted cells, so the whole problem takes $O((n + m)\,\alpha(n))$ time, or $O(n + m)$ with the [Gabow-Tarjan](/gabow-tarjan-union-find/) structure. It is the standard example of union-find used to *jump over* used positions.

## In plain words

You have a row of boxes and a list of jobs, each of the form "paint the boxes from here to there in this color". A later job paints over an earlier one. You want to know the colors at the end.

Do the jobs from the last to the first. Then the first job that reaches a box gives its final color, and no later job may change it. So each box needs to be painted only once.

The hard part is to skip quickly over the boxes that are already done. Let each done box point to the box on its right. To find the next box that is not done, follow the pointers, and shorten them on the way. Each box is then painted once, and the skipping costs almost nothing.

## Definition

**Input.** A number $n$ of cells, numbered $0$ to $n - 1$, and a sequence of $m$ operations $(l_j, r_j, c_j)$ for $j = 1, \ldots, m$, with $0 \le l_j \le r_j \le n - 1$ and a color $c_j$.

**Output.** The array $\mathrm{color}[0..n-1]$ with
$$\mathrm{color}[i] = c_{j(i)}, \qquad j(i) = \max\{j : l_j \le i \le r_j\},$$
and $\mathrm{color}[i] = \bot$ (unpainted) when no operation covers $i$.

The problem is *offline*: all operations are known before the output is needed, and only the final state is asked for.

**The union-find method.** Keep a forest on the elements $0$ to $n$, where $n$ is a sentinel. A cell is a root while it is unpainted. Let $\mathrm{next}(i)$ be the root of $i$, the least unpainted cell $\ge i$, or $n$ if there is none.

```pseudo
PAINT-OFFLINE(n, ops)
    for i ← 0 to n do p[i] ← i; color[i] ← ⊥
    for j ← m down to 1 do
        i ← FIND(l_j)
        while i ≤ r_j do
            color[i] ← c_j
            p[i] ← i + 1                  ▷ i is painted; link it to the right
            i ← FIND(i + 1)
    return color[0..n−1]
```

Each cell is painted once and then linked once, so there are $n$ links in all. Each operation does one FIND to start and one FIND per cell that it paints.

## Variants

- **Online painting.** If the colors must be known between operations, the reverse order is not possible. A [segment tree](/segment-tree/) with [lazy propagation](/lazy-propagation/) supports range assignment and point queries in $O(\log n)$ time each.
- **First cover instead of last.** If the earliest operation should win, process the operations in their given order with the same method.
- **Only the count.** Count the cells painted by each operation, or the number of cells that stay unpainted. The same pass gives both.
- **Jumping over used positions.** The same forest solves other "next free slot" problems: assign each job the latest free day before its deadline, or give each request the next free seat at or after its position. The link then goes left or right.
- **A circle.** For a circular array, link $n - 1$ to $0$ and stop when the walk has gone once round.

## Examples

**Four operations on eight cells.** Let $n = 8$ and the operations be $(0, 4, a)$, $(2, 6, b)$, $(5, 7, c)$, $(3, 3, d)$. In reverse order:

| operation | cells painted | colors of 0 to 7 after it |
|---|---|---|
| $(3, 3, d)$ | 3 | ⊥ ⊥ ⊥ d ⊥ ⊥ ⊥ ⊥ |
| $(5, 7, c)$ | 5, 6, 7 | ⊥ ⊥ ⊥ d ⊥ c c c |
| $(2, 6, b)$ | 2, 4 | ⊥ ⊥ b d b c c c |
| $(0, 4, a)$ | 0, 1 | a a b d b c c c |

The operation $(2, 6, b)$ starts with FIND$(2) = 2$, paints 2, then FIND$(3)$ follows $3 \to 4$ and returns 4, paints 4, then FIND$(5)$ follows $5 \to 6 \to 7 \to 8$ and returns the sentinel 8, which is past $r = 6$. The answer is $a\,a\,b\,d\,b\,c\,c\,c$, the same as painting in the given order.

**A worst case for the naive method.** With $m$ operations that each paint the whole array, the direct method costs $\Theta(nm)$. The reverse method paints all cells in the last operation, and each of the other $m - 1$ operations makes one FIND from cell 0 that returns $n$. The first of these walks the chain of $n$ links and compresses it, and each later one takes one step.

## Known algorithms

| method | time | notes |
|---|---|---|
| direct painting in the given order | $O(n + \sum_j (r_j - l_j + 1)) = O(nm)$ | no data structure |
| reverse order with [path compression](/path-compression/) alone | $O((n + m) \log n)$ | links always go to $i + 1$, so no linking rule; cp-algorithms |
| reverse order with union by rank and a right end at each root | $O((n + m)\,\alpha(n))$ | the root stores the largest cell of its set |
| reverse order with the [Gabow-Tarjan](/gabow-tarjan-union-find/) structure | $O(n + m)$ | the unions form a fixed path, a case of [static tree set union](/static-tree-set-union/) |
| sweep over the cells with a heap of the open operations | $O((n + m) \log m)$ | no union-find |
| [segment tree](/segment-tree/) with [lazy propagation](/lazy-propagation/) | $O(n + m \log n)$ | also online |

With path compression alone, the bound is the one for compression with any linking rule, which is $O(\log n)$ amortized per find when there are at least $n$ finds. To use union by rank, the representative of a set is no longer its rightmost cell, so each root keeps the largest cell of its set, and FIND returns that value instead of the root.

## Bounds

- **Upper bound.** $O(n + m)$ on a RAM with words of $\Theta(\log n)$ bits, by the [Gabow-Tarjan](/gabow-tarjan-union-find/) algorithm, because the unions are known in advance: each cell $i$ is united with $i + 1$.
- **Lower bound.** $\Omega(n + m)$, to read the input and write the output.
- **The amortized union-find bound does not apply.** The [union-find lower bound](/union-find-lower-bound/) of $\Omega(m\,\alpha(m, n))$ is for arbitrary unions. Here the shape of the unions is fixed in advance, which is why linear time is possible.

## Reductions

- **To interval union-find.** The method is a sequence of at most $n$ unions of a set with the set to its right and $n + m$ finds. This is the interval case of [static tree set union](/static-tree-set-union/), with the path $0, 1, \ldots, n$ as the fixed tree.
- **From offline minimum.** [Offline minimum](/offline-minimum/) uses the same kind of forest on the positions of a sequence, where each used position is united with the next one.
- **Offline processing.** The reverse order is an instance of [offline query processing](/offline-query-processing/): choose an order of the operations in which each answer is fixed once.

## Applications

- Final colors after range assignments, in problems where only the final state is needed.
- Scheduling with deadlines: give each job, in order of value, the latest free slot at or before its deadline, with links to the left.
- Allocation of the next free position at or after a given index, for example seats or hash slots, when positions are never freed.
- Removing elements from an array while scanning, so that a scan skips the removed ones.

## References
