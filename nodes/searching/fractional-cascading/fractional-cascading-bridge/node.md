---
tag: DVQA5R
kind: concept
slug: fractional-cascading-bridge
name: Fractional cascading bridge
aliases:
- bridge
- bridge pointer
area: searching/fractional-cascading
level: advanced
summary: A sampled element from a neighbouring catalog, stored with a pointer, that lets a search move from one catalog to the next in constant time.
prereqs: [multiple-list-search, catalog-graph, binary-search, lower-bound-query]
see_also: [dynamic-fractional-cascading, layered-range-tree, merge-sort-tree, hive-graph, fractional-cascading-lower-bound, segment-tree]
sources:
  - paper: doi:10.1007/BF01840440
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading I, A data structuring technique, Algorithmica 1 (1986)
    locator: pages 133 to 162 (augmented catalogs, bridges and gaps, the linear-space construction and the query in O(log n + k log d) time)
  - paper: doi:10.1007/BF01840441
    title: Bernard Chazelle and Leonidas J. Guibas, Fractional cascading II, Applications, Algorithmica 1 (1986)
    locator: pages 163 to 191
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Section 5.6 (Fractional Cascading, in the layered range tree)
---

A fractional cascading bridge is a copy of an element of one catalog, placed in the augmented catalog of a neighbouring vertex and linked to the original by a pointer. Bridges are the device of [fractional cascading](/multiple-list-search/), the technique of Chazelle and Guibas for searching one key in many sorted lists. Each augmented catalog keeps a fixed fraction of the elements of its neighbours as bridges, so the total space grows only by a constant factor. Because two consecutive bridges are close in both catalogs, the position of a key in one catalog gives its position in the next one after $O(1)$ extra comparisons on a [catalog graph](/catalog-graph/) of bounded degree.

## In plain words

Suppose you have found where a key fits in one sorted list, and you now want its place in the next list. Without help, you must search the second list from scratch.

A bridge is a shared landmark. Take every second item of the next list and copy it into the current list, and let each copy remember where it came from. Now, after you find your place in the current list, look at the nearest copied item at or after your place. It tells you a spot in the next list, and the right place is that spot or the one just before it. So one more look gives the answer.

The copies of copies get thinner from list to list, because each list passes on only half of what it holds. In total, the extra space is about the size of the original lists, not more.

## The idea

### The path case

Let $C_1, \ldots, C_k$ be sorted lists of total size $n$ over a totally ordered set with a top element $+\infty$, and let $\operatorname{succ}(x, L)$ be the first element of $L$ that is at least $x$.

**Augmented catalogs.** Build lists $M_k, M_{k-1}, \ldots, M_1$ from the last to the first:

- $M_k = C_k$ followed by $+\infty$.
- For $i < k$, let $P_{i+1}$ be the *promoted* elements of $M_{i+1}$: the elements at odd positions $1, 3, 5, \ldots$ (counting from 0), and the last element $+\infty$. Then $M_i$ is the sorted merge of $C_i$ and $P_{i+1}$.

The copies of $P_{i+1}$ inside $M_i$ are the *bridges* of the pair $(i, i+1)$. Since $+\infty$ is promoted at every level, each $M_i$ ends with $+\infty$.

**Pointers.** For each position $j$ of $M_i$, store two numbers:

- $\mathit{own}_i[j]$: the position of $\operatorname{succ}(M_i[j], C_i)$ in $C_i$, with $|C_i|$ for $+\infty$;
- $\mathit{down}_i[j]$ (for $i < k$): the position in $M_{i+1}$ of the first promoted element that is at least $M_i[j]$.

**Query.** Given $x$:

1. Find $p = $ the position of $\operatorname{succ}(x, M_1)$ by a [binary search](/binary-search/) in $M_1$.
2. For $i = 1, \ldots, k$: report $\mathit{own}_i[p]$ as the answer for $C_i$. If $i < k$, set $q = \mathit{down}_i[p]$. If $q \ge 1$ and $M_{i+1}[q-1] \ge x$, set $q = q - 1$. Set $p = q$.

**Claim 1 (correctness).** At the start of step 2 for index $i$, $p$ is the position of $y_i = \operatorname{succ}(x, M_i)$, and $\mathit{own}_i[p]$ is the position of $\operatorname{succ}(x, C_i)$.

*Proof.* For $i = 1$ this is step 1. Assume it for $i < k$. First, $\operatorname{succ}(x, C_i) = \operatorname{succ}(y_i, C_i)$: since $C_i \subseteq M_i$, no element of $C_i$ lies in $[x, y_i)$, because such an element would be an element of $M_i$ that is at least $x$ and less than $y_i$. So $\mathit{own}_i[p]$ is right.

Let $q = \mathit{down}_i[p]$ and $z = M_{i+1}[q]$, the first promoted element that is at least $y_i$. It exists because $+\infty$ is promoted. Since $z \ge y_i \ge x$, the successor of $x$ in $M_{i+1}$ is at position $q$ or before it. Let $z'$ be the promoted element just before $z$ in $M_{i+1}$, if there is one. Then $z' < y_i$, because $z$ is the first promoted element at least $y_i$. Also $z' \in P_{i+1} \subseteq M_i$, and $y_i$ is the first element of $M_i$ that is at least $x$, so $z' < x$. The promoted positions are $1, 3, 5, \ldots$ and the last one, so two consecutive promoted positions differ by at most 2, and the first one is at most 1. Hence every element of $M_{i+1}$ that is at least $x$ and before $z$ is at position $q - 1$. The test in step 2 checks exactly this one position, so the new $p$ is the position of $\operatorname{succ}(x, M_{i+1})$. $\square$

**Claim 2 (space).** $\sum_{i=1}^{k} |M_i| \le 2n + k + 1$.

*Proof.* A list of length $L$ has $\lfloor L/2 \rfloor$ odd positions, and its last position is odd or it adds one more, so $|P_{i+1}| = \lceil |M_{i+1}|/2 \rceil \le (|M_{i+1}| + 1)/2$. So $|M_k| = |C_k| + 1$ and $|M_i| \le |C_i| + (|M_{i+1}| + 1)/2$ for $i < k$. Summing, with $S = \sum_i |M_i|$,
$$S \le n + 1 + \frac{1}{2} \sum_{i=2}^{k} |M_i| + \frac{k-1}{2} \le n + 1 + \frac{S}{2} + \frac{k - 1}{2},$$
so $S \le 2n + k + 1$. $\square$

**Cost.** Step 1 costs $\lceil \lg (|M_1| + 1) \rceil = O(\log n)$ comparisons, since $|M_1| \le 2n + k + 1$. Each later step costs one comparison and $O(1)$ pointer steps. So a query costs $O(\log n + k)$ time. The build merges each $C_i$ with $P_{i+1}$ and fills the pointers by one scan, in $O(n + k)$ time.

### Bridges on a graph

On a [catalog graph](/catalog-graph/) of degree $d$, each vertex $v$ gets an augmented catalog $A_v \supseteq C_v$. Along each edge $uv$, a fraction of the elements of $A_u$ is copied into $A_v$ and a fraction of $A_v$ into $A_u$. A copy that is present in both lists, with pointers between its two places, is a *bridge* of the edge. The elements of $A_u$ between two consecutive bridges of the same edge form a *gap*.

**The invariant.** For the move from $u$ to $v$, what matters is the list that sent the copies. Each gap of $A_v$ between two consecutive bridges of the edge $uv$ has at most $c\,d$ elements, for a constant $c$. Then a search that knows its position in $A_u$ goes to the next bridge of the edge $uv$, crosses to $A_v$, and searches back in a gap of $O(d)$ elements: $O(d)$ steps by a scan, or $O(\log d)$ comparisons by a binary search in the gap. The proof is the one of Claim 1, with the gap of size $c\,d$ in place of the gap of size 2. This gives the query time $O(\log n + k \log d)$ of Chazelle and Guibas.

**Why the space stays linear.** Suppose that each vertex passes one element out of every $2d$ elements of its augmented catalog to each of its at most $d$ neighbours, so that the gaps of the invariant have about $2d$ elements. Let $S = \sum_v |A_v|$. The copies received in total are at most $\sum_u d \cdot \lceil |A_u| / (2d) \rceil \le S/2 + d\,|V|$. So $S \le n + S/2 + d\,|V|$, which gives $S \le 2n + 2d\,|V|$. In a graph with cycles the lists depend on each other, since a copy can be copied again, and Chazelle and Guibas give a construction in linear time that reaches such a state and keeps the gap invariant (Part I). The path case above is the case where copies move in one direction only, and passing half of the elements is enough.

**The fraction is the name.** Copying all of $M_{i+1}$ into $M_i$ would also work, but $M_1$ would then hold all $n$ items and the total space would be $\Theta(nk)$ in the worst case. Copying a fraction is the trade between this and separate searches: the space stays $O(n)$, and the gaps stay $O(1)$.

## Examples

**The path of three catalogs.** Let
$$C_1 = (2, 7, 13, 24, 35), \quad C_2 = (5, 9, 16, 21, 30, 42), \quad C_3 = (1, 6, 10, 19, 23, 28, 40).$$
The build gives

| list | elements (positions 0, 1, 2, ...) | promoted to the list above |
|---|---|---|
| $M_3$ | 1, 6, 10, 19, 23, 28, 40, $\infty$ | 6, 19, 28, $\infty$ |
| $M_2$ | 5, **6**, 9, 16, **19**, 21, **28**, 30, 42, $\infty$ | 6, 16, 21, 30, $\infty$ |
| $M_1$ | 2, **6**, 7, 13, **16**, **21**, 24, **30**, 35, $\infty$ | none |

The bold elements, and the final $\infty$ of $M_1$ and $M_2$, are bridges from the list below. The total size is $8 + 10 + 10 = 28$, within the bound $2 \cdot 18 + 3 + 1 = 40$. The pointer arrays are $\mathit{down}_1 = (1, 1, 3, 3, 3, 5, 7, 7, 9, 9)$ and $\mathit{down}_2 = (1, 1, 3, 3, 3, 5, 5, 7, 7, 7)$.

**The query $x = 20$.**

| step | position $p$ in $M_i$ | $M_i[p]$ | answer in $C_i$ | move to the next list |
|---|---|---|---|---|
| $i = 1$ | 5 (binary search) | 21 | 24 | $q = \mathit{down}_1[5] = 5$; $M_2[4] = 19 < 20$, so $q$ stays 5 |
| $i = 2$ | 5 | 21 | 21 | $q = \mathit{down}_2[5] = 5$; $M_3[4] = 23 \ge 20$, so $q = 4$ |
| $i = 3$ | 4 | 23 | 23 | done |

The answers 24, 21 and 23 are the successors of 20 in the three catalogs. After the binary search in $M_1$, the query made one comparison per list. The step from $M_2$ to $M_3$ shows why the test is needed: the bridge 28 is past the answer 23, which sits just before it.

## Where it is used

- [Multiple list search](/multiple-list-search/), the problem that bridges solve.
- [Layered range trees](/layered-range-tree/): the lists of the secondary structures are linked by bridges, so a 2-dimensional orthogonal range query costs $O(\log n + t)$ instead of $O(\log^2 n + t)$.
- [Merge sort trees](/merge-sort-tree/) and [segment trees](/segment-tree/) with sorted lists at the nodes, where one key is ranked at each node on a root-to-leaf path.
- The [hive graph](/hive-graph/) of Chazelle, whose combing step copies every other vertical edge down to the next segment, the same sampling idea in a planar map.
- [Dynamic fractional cascading](/dynamic-fractional-cascading/), which keeps the gaps small while items are inserted and deleted.
- The [Chazelle-Liu lower bound](/fractional-cascading-lower-bound/), which shows that bridges have no general analogue for planar maps.

## References
