---
tag: 4S5W6M
kind: data-structure
slug: segment-tree-beats
name: Segment tree beats
aliases:
- Ji's segment tree
area: data-structures/range-query-structures
level: research
summary: Segment tree variant for range chmin, chmax and modulo updates with amortized logarithmic bounds.
implements: [range-query-structure]
prereqs: [segment-tree, lazy-propagation, potential-method]
see_also: [range-update-range-query, range-assignment-query, chtholly-tree, historical-queries, kinetic-heap, segment-tree-maximum-subsegment-sum, square-root-decomposition, range-query-problem]
sources:
  - url: https://codeforces.com/blog/entry/57319
    title: Ji Ruyi (jiry_2), A simple introduction to "Segment tree beats", Codeforces blog
    locator: the task with range chmin, range max and range sum, the break and tag conditions, the O((n + q) log n) bound by tag classes, and the extensions with range add and historic values
  - paper: "Ji Ruyi, Interval maximum operations and historical maximum problems (in Chinese), Chinese national team candidate papers, 2016"
    locator: the original description of the method and its amortized analysis
  - url: https://acm.hdu.edu.cn/showproblem.php?pid=5306
    title: HDU 5306, Gorgeous Sequence
    locator: the problem statement, range chmin with range max and range sum queries
---

Segment tree beats is a [segment tree](/segment-tree/) that supports range updates which do not act on the stored aggregates by a fixed formula, such as "replace each $A[i]$ in $[l, r]$ by $\min(A[i], x)$", together with range sums and maximums. Each node keeps its maximum, its strict second maximum, the count of the maximum and its sum. An update stops at a node when $x$ is at least the maximum, applies a tag when $x$ lies strictly between the second maximum and the maximum, and otherwise recurses further than an ordinary segment tree would. Ji Ruyi showed with a potential argument that the extra recursion is paid for, so the operations cost $O(\log n)$ amortized, and the same scheme with other potentials handles range chmax, range add with chmin, and range modulo.

## In plain words

You keep a list of numbers, and an order says: in this stretch, cut every number that is above $x$ down to $x$. Questions ask for the total or the largest number of a stretch.

A normal segment tree with lazy notes cannot keep the totals right for this order, because the change to a total depends on how many numbers are above $x$ and by how much. The trick is to keep, for each piece, its largest number, how many times it occurs, and the second largest number. If $x$ lies above the second largest, only the copies of the largest change, and the new total is easy. If not, go down into the smaller pieces. Going down costs time, but each such step makes two different numbers equal, which can happen only a limited number of times.

## The abstract type

The structure implements a [range query structure](/range-query-structure/) on an integer array with the update $\mathrm{chmin}(l, r, x)$, which sets $A[i] \leftarrow \min(A[i], x)$ for $l \le i \le r$, and the queries $\mathrm{sum}(l, r)$ and $\mathrm{max}(l, r)$. The update is the map $f_x(v) = \min(v, x)$. These maps compose, $f_y \circ f_x = f_{\min(x, y)}$, but the sum of a range after $f_x$ is not a function of the old sum, $x$ and the length. So the lazy condition of the [range update range query](/range-update-range-query/) page fails, and [lazy propagation](/lazy-propagation/) alone does not apply.

## Representation

The tree is the recursive segment tree with node 1 for $[0, n - 1]$ and the children $2v$ and $2v + 1$, in arrays of $4n$ cells. Each node $v$ stores four fields:

- $\mathit{mx1}[v]$, the largest value of its range;
- $\mathit{mx2}[v]$, the largest value that is strictly less than $\mathit{mx1}[v]$, or $-\infty$ if all values are equal;
- $\mathit{cnt}[v]$, the number of items equal to $\mathit{mx1}[v]$;
- $\mathit{sum}[v]$, the sum of the range.

There is no separate tag field. A pending chmin at $v$ is $\mathit{mx1}[v]$ itself: when $\mathit{mx1}[v]$ is less than the maximum stored in a child, the child has not yet seen the cap.

**Invariant (B).** For an item $i$ in the range of $v$, let $s_v(i)$ be the leaf value of $i$ capped by $\mathit{mx1}$ of every node on the path from the leaf up to $v$: $s_{\mathrm{leaf}}(i) = \mathit{mx1}[\mathrm{leaf}]$ and $s_v(i) = \min(s_{\mathrm{child}}(i), \mathit{mx1}[v])$. Then for every node, the four fields of $v$ are the maximum, the strict second maximum, the count of the maximum and the sum of the values $s_v(i)$ over its range, and $A[i] = s_1(i)$ for every $i$.

So the fields of a node describe the true values of its range exactly when no ancestor holds a smaller $\mathit{mx1}$, which holds for every node that an operation reaches, since the operation pushes the caps down on its way.

## Operations

```pseudo id=main
BUILD(v, lo, hi)                                             ▷ call BUILD(1, 0, n − 1)
L1  if lo = hi then (mx1, mx2, cnt, sum)[v] ← (A[lo], −∞, 1, A[lo]); return
L2  mid ← ⌊(lo + hi)/2⌋; BUILD(2v, lo, mid); BUILD(2v + 1, mid + 1, hi)
L3  PULL(v)

PULL(v)                                                      ▷ combine the two children
L4  a ← 2v; b ← 2v + 1
L5  sum[v] ← sum[a] + sum[b]
L6  if mx1[a] = mx1[b] then mx1[v] ← mx1[a]; cnt[v] ← cnt[a] + cnt[b]; mx2[v] ← max(mx2[a], mx2[b])
L7  else if mx1[a] > mx1[b] then mx1[v] ← mx1[a]; cnt[v] ← cnt[a]; mx2[v] ← max(mx2[a], mx1[b])
L8  else mx1[v] ← mx1[b]; cnt[v] ← cnt[b]; mx2[v] ← max(mx1[a], mx2[b])

APPLY(v, x)                                                  ▷ used only when mx2[v] < x
L9  if x < mx1[v] then sum[v] ← sum[v] − cnt[v] · (mx1[v] − x); mx1[v] ← x

PUSH(v)                                                      ▷ hand the cap of v to its children
L10 APPLY(2v, mx1[v]); APPLY(2v + 1, mx1[v])

CHMIN(v, lo, hi, l, r, x)                                    ▷ call CHMIN(1, 0, n − 1, l, r, x)
L11 if r < lo or hi < l or mx1[v] ≤ x then return            ▷ break condition
L12 if l ≤ lo and hi ≤ r and mx2[v] < x then APPLY(v, x); return    ▷ tag condition
L13 PUSH(v); mid ← ⌊(lo + hi)/2⌋
L14 CHMIN(2v, lo, mid, l, r, x); CHMIN(2v + 1, mid + 1, hi, l, r, x)
L15 PULL(v)

QUERY-SUM(v, lo, hi, l, r)                                   ▷ QUERY-MAX is the same with max and −∞
L16 if r < lo or hi < l then return 0
L17 if l ≤ lo and hi ≤ r then return sum[v]
L18 PUSH(v); mid ← ⌊(lo + hi)/2⌋; return QUERY-SUM(2v, lo, mid, l, r) + QUERY-SUM(2v + 1, mid + 1, hi, l, r)
```

**Pull** (lines L4 to L8) merges two children. The new maximum is the larger of the two maximums. If they are equal, the counts add and the second maximum is the larger of the two second maximums; if not, the smaller maximum competes with the second maximum of the larger side.

**Apply** (line L9) caps a node at $x$ when $\mathit{mx2}[v] < x$. Then the items above $x$ are exactly the $\mathit{cnt}[v]$ copies of the maximum, each drops by $\mathit{mx1}[v] - x$, and the new maximum is $x$, still above $\mathit{mx2}[v]$, with the same count.

**Push** (line L10) applies the cap $\mathit{mx1}[v]$ to both children. A child whose maximum is at most the cap is unchanged by line L9. A child whose maximum is above the cap had the old maximum of $v$, and its second maximum is at most the second maximum of $v$, which is below the cap, so the precondition of APPLY holds.

**Chmin** (lines L11 to L15) is a range update with two stopping rules. The *break condition* of line L11 stops when the node is outside the range or no item is above $x$. The *tag condition* of line L12 stops when the node is inside the range and only its maximum is above $x$. Otherwise the call pushes, recurses into both children, and pulls.

**Query** (lines L16 to L18) is the ordinary segment tree query with a push before each descent.

## Example

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$. The root has $\mathit{mx1} = 9$, $\mathit{mx2} = 8$, $\mathit{cnt} = 1$ and $\mathit{sum} = 39$.

1. **chmin$(0, 7, 6)$.** At the root, $9 > 6$ and $\mathit{mx2} = 8 \ge 6$, so neither condition holds and the call recurses. Node 2, for $[0, 3]$ with the values $5, 2, 8, 1$, has $\mathit{mx2} = 5 < 6$: line L12 applies the tag, and its sum drops from 16 to $16 - 1 \cdot (8 - 6) = 14$. Node 3, for $[4, 7]$ with $9, 3, 7, 4$, has $\mathit{mx2} = 7 \ge 6$ and recurses. Its children, node 6 for $9, 3$ and node 7 for $7, 4$, both take the tag, with the sums $12 \to 9$ and $11 \to 10$. The call enters 5 nodes. The root now has $\mathit{mx1} = 6$, $\mathit{mx2} = 5$, $\mathit{cnt} = 3$ and $\mathit{sum} = 33$, for the array $[5, 2, 6, 1, 6, 3, 6, 4]$.
2. **The pending cap.** Node 5, for $[2, 3]$, still stores $\mathit{mx1} = 8$, while its parent, node 2, stores 6. By (B), the item 2 is $\min(8, 6) = 6$. The query sum$(2, 5)$ pushes the cap of node 2 into node 5, which then stores 6, and returns $6 + 1 + 6 + 3 = 16$.
3. **chmin$(1, 6, 3)$.** This call enters 13 nodes: several nodes of the range have second maximums at least 3, so it goes down to the leaves at the items 2, 4 and 6. The array becomes $[5, 2, 3, 1, 3, 3, 3, 4]$, with sum$(0, 7) = 24$ and max$(1, 6) = 3$.

The second update is more expensive than the first, but it makes many items equal: after it, the range $[1, 6]$ holds only the values 1, 2 and 3.

## Correctness

BUILD gives (B), since at that point no node caps a child, and PULL computes the four fields of a union from those of its two parts. APPLY under its precondition gives the fields of the capped values, as shown above, and PUSH meets that precondition, so PUSH changes no value $s_v(i)$ and only moves a cap down. CHMIN changes exactly the items of $[l, r]$ above $x$: a node stopped by line L11 has no such item in the range, a node stopped by line L12 is capped correctly by APPLY, and a node that recurses is made correct again by PULL from correct children. The queries return correct values because every node they read has been reached by pushes from the root. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

A query visits $O(\log n)$ nodes, as in an ordinary segment tree, with $O(1)$ work for each push.

**The amortized bound for chmin.** Call a node visited by CHMIN *partial* if its range meets $[l, r]$ but is not inside it, and *extra* if its range is inside $[l, r]$ and both conditions fail, so that $\mathit{mx1}[v] > x$ and $\mathit{mx2}[v] \ge x$. Every visited node except the root is a child of a partial or an extra node. As in the [segment tree](/segment-tree/) page, there are at most 2 partial nodes per level, so a call enters at most $1 + 2(2 \lceil \lg n \rceil + E)$ nodes, where $E$ is its number of extra nodes.

Let the potential $\Phi$ be the sum, over all nodes $v$, of the number of distinct values of $A$ in the range of $v$. Then $0 \le \Phi \le n(\lceil \lg n \rceil + 1)$, since each item lies in at most $\lceil \lg n \rceil + 1$ ranges. Consider one chmin with the cap $x$:

- A node whose range is inside $[l, r]$ does not gain distinct values, because $v \mapsto \min(v, x)$ maps the set of its values onto a set of at most the same size.
- A partial node gains at most one distinct value, the value $x$. There are at most $2 \lceil \lg n \rceil + 1$ of them.
- An extra node loses at least one distinct value: its two largest values, $\mathit{mx1}[v] > \mathit{mx2}[v] \ge x$, both become $x$.

So one chmin raises $\Phi$ by at most $2 \lceil \lg n \rceil + 1$ and lowers it by at least $E$. Over $q$ operations, the total number of extra nodes is at most $n(\lceil \lg n \rceil + 1) + q(2 \lceil \lg n \rceil + 1)$, and the total number of visited nodes is $O((n + q) \log n)$.

| operation | time |
|---|---|
| build | $\Theta(n)$ |
| chmin | $O(\log n)$ amortized, $O(n)$ worst case for one call |
| sum or max query | $O(\log n)$ worst case |
| space | $4n$ cells of four fields |

The tests of the implementation check the bound on the number of visited nodes for random operations. This is the potential method; see the [potential method](/potential-method/) page for the general scheme.

## Variants

- **Range chmax.** Mirror the fields with the minimum, the strict second minimum and its count.
- **Chmin and chmax together, with range add.** Keep both sets of fields and an add tag. Ji's analysis by tag classes gives $O(\log^2 n)$ amortized per operation for these mixes, and $O(\log n)$ when range add is absent.
- **Range modulo.** The update $A[i] \leftarrow A[i] \bmod x$ on $[l, r]$, with point assignment and range sums. Stop at a node whose maximum is less than $x$; otherwise recurse to the leaves. An item $v \ge x$ becomes $v \bmod x < v/2$, so each item changes $O(\log C)$ times between assignments for values up to $C$, and the total cost is $O((n + q) \log n \log C)$.
- **Range division and square roots.** The same scheme as for modulo works for $\lfloor A[i] / d \rfloor$ with $d \ge 2$ and for $\lfloor \sqrt{A[i]} \rfloor$, with a break when the range has a single repeated value and the update leaves it unchanged, or when all its items are at most 1.
- **Historic values.** Ji also keeps, with similar tags, the historic maximum or the historic sum of each item, the largest value it ever had; see [historical queries](/historical-queries/).

## When to use it

Use it when range updates are capping operations such as chmin or chmax, or contracting ones such as modulo, and the queries are sums or extremes. For range add or assignment alone, an ordinary lazy segment tree is simpler and has worst-case bounds. For random assignments with arbitrary queries, the [Chtholly tree](/chtholly-tree/) is shorter. When a worst-case bound per operation is required, segment tree beats is not suitable: one chmin can visit $\Theta(n)$ nodes.

## Pitfalls

- **A second maximum that is not strict.** If $\mathit{mx2}$ may equal $\mathit{mx1}$, the tag condition fails on ranges of equal values, and the merges of line L6 count the maximum twice. Keep $\mathit{mx2}$ strictly below $\mathit{mx1}$, with $-\infty$ for a range of one value.
- **The wrong comparison in the tag condition.** The condition is $\mathit{mx2}[v] < x$, strict. With $\mathit{mx2}[v] \le x$, the items equal to $\mathit{mx2}$ stay correct, but the new maximum $x$ then equals $\mathit{mx2}$, and $\mathit{cnt}$ and $\mathit{mx2}$ are wrong after the tag.
- **Pushing a cap to a child with a smaller maximum.** Line L9 must do nothing when $x \ge \mathit{mx1}[v]$. Without the test, the sum of a child below the cap grows.
- **Forgetting to push before a query.** A query that reads a child without the push of line L18 reads values above the caps of its ancestors.
- **Mixing with range add naively.** An add tag and the implicit chmin cap must be ordered: apply the add first to all fields, then the cap. Getting this order wrong breaks (B) silently.

## Implementations

The Python class `SegmentTreeBeats` follows the main block, with range chmin, range sum and range max on integers. It keeps a counter of the nodes entered by chmin, which the tests compare with the amortized bound, and a `check_invariant` method that recomputes the capped values $s_v(i)$ of every node and compares the four fields.

## History

Ji Ruyi introduced the method in his 2016 paper for the Chinese national team selection, on interval maximum operations and historic maximum problems, and described it in English in a Codeforces blog post under the name "segment tree beats". The task with range chmin and range sum and maximum queries appears as the problem Gorgeous Sequence on the HDU online judge.

## References
