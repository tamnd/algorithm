---
tag: 8PYVZ2
kind: technique
slug: lazy-propagation
name: Lazy propagation
aliases:
- lazy segment tree
- deferred updates
area: data-structures/range-query-structures
level: core
summary: Store pending range updates at tree nodes and push them down only when needed.
prereqs: [segment-tree, monoid]
see_also: [range-update-range-query, range-assignment-and-sum-query, range-assignment-query, segment-tree-beats, dynamic-segment-tree, fenwick-tree, chtholly-tree, point-update-range-min-query]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 28, Segment trees revisited, Section 28.1 Lazy propagation (lazy updates, increase and set updates, polynomial updates)
  - url: https://cp-algorithms.com/data_structures/segment_tree.html
    title: cp-algorithms, Segment Tree
    locator: the section Range updates (Lazy Propagation), with addition on segments, assignment on segments, and adding on segments with a maximum query
  - url: https://atcoder.github.io/ac-library/production/document_en/lazysegtree.html
    title: AtCoder Library documentation, Lazy Segment Tree
    locator: the constraints on the monoid S, the set of maps F, mapping, composition and id
---

Lazy propagation is the technique that lets a [segment tree](/segment-tree/) apply an update to a whole range in $O(\log n)$ time. An update stops at the $O(\log n)$ nodes whose ranges tile the update range, changes their stored values at once, and leaves a *tag* that says "this update is still owed to my children". A later operation that must go below a tagged node first pushes the tag down one level. The technique works when the updates form a [monoid](/monoid/) of maps that act on the stored values and distribute over their combination, which covers range add, range assignment, range multiply-and-add and range bit flips with sum, minimum or maximum queries.

## In plain words

A range update on a segment tree would have to touch every leaf in the range, which is slow for a long range. Lazy propagation is a promise. The update goes down the tree only until it reaches nodes that lie fully inside the range. It fixes the total stored at each such node, and it writes a note there: "my children still need this change".

Nothing below a note is fixed yet. That is fine, because nobody has looked there. When a later update or query needs to go below a node with a note, it first hands the note to the two children, fixes their totals, and wipes the note. So each operation does work only along the few paths that it really visits.

## When it applies

- The problem has **range updates** and **range queries** on an array, both online, and a plain segment tree handles the queries.
- The updates can be described by **maps** $f : V \to V$ on the node values, from a set $F$ that contains the identity map and is closed under composition, so that two pending updates can be merged into one tag.
- Each map **distributes** over the combination of values: $f(x \oplus y) = f(x) \oplus f(y)$. The value of a node must hold what the map needs; for "add $c$" with sum queries, the value is the pair (sum, length), and $f_c(s, \ell) = (s + c \ell, \ell)$.
- Signals in a statement: "add to all items from $l$ to $r$", "set all items from $l$ to $r$ to $v$", "flip the bits in a range", followed by "sum, minimum or count of ones over a range".
- If an update depends on each item in a way that does not distribute, such as "replace each item by its square root" or "set each item to $\min(A[i], x)$" with sum queries, plain lazy propagation fails, see [segment tree beats](/segment-tree-beats/).

Formally, $(V, \oplus, e)$ is a monoid of values, $(F, \circ, \mathrm{id})$ is a monoid of maps under composition, $(g \circ f)(x) = g(f(x))$, and $f(x \oplus y) = f(x) \oplus f(y)$ and $f(e) = e$ for each $f \in F$. These are the laws of the AtCoder Library lazy segment tree.

## The template

The holes are COMBINE ($\oplus$), MAP (apply $f$ to a value), COMPOSE ($g \circ f$, for $g$ after $f$) and ID. Node $x$ covers $[lo, hi)$, and its children $2x$ and $2x + 1$ cover the two halves. Each node has a value $val[x]$ and a tag $tag[x]$, which starts as ID.

```pseudo id=main
APPLY(x, f)                                ▷ f now holds on the range of x
L1  val[x] ← MAP(f, val[x])
L2  tag[x] ← COMPOSE(f, tag[x])            ▷ f after the old tag

PUSH(x)                                    ▷ hand the tag of x to its children
L3  if tag[x] ≠ ID then
L4      APPLY(2x, tag[x]); APPLY(2x + 1, tag[x])
L5      tag[x] ← ID

UPDATE(x, lo, hi, l, r, f)                 ▷ apply f to A[l .. r − 1]
L6  if r ≤ lo or hi ≤ l then return        ▷ no overlap
L7  if l ≤ lo and hi ≤ r then APPLY(x, f); return   ▷ full cover: stop here
L8  PUSH(x); mid ← ⌊(lo + hi)/2⌋
L9  UPDATE(2x, lo, mid, l, r, f); UPDATE(2x + 1, mid, hi, l, r, f)
L10 val[x] ← COMBINE(val[2x], val[2x + 1])

QUERY(x, lo, hi, l, r)                     ▷ the value of A[l .. r − 1]
L11 if r ≤ lo or hi ≤ l then return e
L12 if l ≤ lo and hi ≤ r then return val[x]
L13 PUSH(x); mid ← ⌊(lo + hi)/2⌋
L14 return COMBINE(QUERY(2x, lo, mid, l, r), QUERY(2x + 1, mid, hi, l, r))
```

**The invariant.** For each node $x$, let $f_x$ be the composition of the tags of the strict ancestors of $x$, with the tag of the parent applied first and the tag of the root applied last. Then the true value of the range of $x$ is $f_x(val[x])$. In words: $val[x]$ is right for all updates except the ones still waiting in the tags above it. At the root, $f_x = \mathrm{id}$, so $val[1]$ is always the true value of the array.

**Why each step keeps it.** APPLY at a node that lies inside the update range changes its true value from $v$ to $f(v)$. Line L1 makes $val[x]$ right, and line L2 records that the children still owe $f$, after what they owed before. PUSH moves the tag of $x$ into both children with APPLY; the children's values become right with respect to that tag, and the tag of $x$ becomes ID, so $f_y$ is unchanged for every node $y$ below. Line L10 recomputes $val[x]$ from two children whose values are right: their parent tag is now ID, so their values are their true values, and their combination is the true value of $x$. Distributivity is what makes line L1 correct at an inner node: $f(v_1 \oplus v_2 \oplus \cdots) = f(v_1) \oplus f(v_2) \oplus \cdots$, so changing the total is the same as changing each item. A query reads a node only after all tags above it on its path have been pushed, so the value it reads is true.

**Cost.** At each depth, the ranges of the nodes are disjoint. A node at which UPDATE or QUERY goes on to line L8 or line L13 overlaps $[l, r)$ but is not inside it, so it holds the position $l - 1$ and $l$, or $r - 1$ and $r$. So at most two nodes of each depth recurse, at most four are visited, and an operation costs $O(\log n)$ calls of the holes. If each hole takes $O(1)$ time, both operations take $O(\log n)$ time. The tags add $O(n)$ space.

## Classic examples

### Range add and range sum

Values are (sum, length), MAP$(c, (s, \ell)) = (s + c \ell, \ell)$, COMPOSE$(c, d) = c + d$ and ID $= 0$. Take $A = [1, 2, 3, 4, 5, 6, 7, 8]$ and add 10 to $[2, 6)$.

| node | range | before | action | after |
|---|---|---|---|---|
| 1 | $[0, 8)$ | 36 | recurse | 76 |
| 2 | $[0, 4)$ | 10 | recurse | 30 |
| 4 | $[0, 2)$ | 3 | no overlap | 3 |
| 5 | $[2, 4)$ | 7 | inside: sum $7 + 10 \cdot 2$, tag 10 | 27 |
| 3 | $[4, 8)$ | 26 | recurse | 46 |
| 6 | $[4, 6)$ | 11 | inside: sum $11 + 10 \cdot 2$, tag 10 | 31 |
| 7 | $[6, 8)$ | 15 | no overlap | 15 |

The leaves for positions 2 to 5 still hold 3, 4, 5 and 6. Now QUERY$(3, 8)$ visits node 1, node 2, node 4 (no overlap) and node 5, which is not inside $[3, 8)$. So node 5 pushes its tag: its leaves become 13 and 14, and the query takes 14 from position 3. Node 3 is inside and gives 46. The answer is $14 + 46 = 60$, which is $14 + 15 + 16 + 7 + 8$. Node 6 keeps its tag, because nothing went below it.

### Range assignment and range sum

Tags are "set to $v$" or ID, MAP$(\text{set } v, (s, \ell)) = (v \ell, \ell)$, and COMPOSE$(\text{set } v, \cdot) = \text{set } v$: a later assignment wins. This solves [range assignment and sum query](/range-assignment-and-sum-query/). The tag ID must be a separate value, not "set to 0".

### Range add and range minimum

Values are minima, MAP$(c, m) = m + c$, and COMPOSE adds. No length is needed, because $\min(x + c, y + c) = \min(x, y) + c$. This is the classic tree of [range update range query](/range-update-range-query/) for minima.

### Affine updates modulo a prime

Tags are maps $x \mapsto a x + b$, which cover "multiply the range by $a$" and "add $b$ to the range" at once. MAP$((a, b), (s, \ell)) = (a s + b \ell, \ell)$ and COMPOSE$((a_2, b_2), (a_1, b_1)) = (a_2 a_1, a_2 b_1 + b_2)$. Here the order of COMPOSE matters, because affine maps do not commute.

### Range flip of bits

On a 0/1 array, values are (ones, length), the tag is a bit, MAP$(1, (c, \ell)) = (\ell - c, \ell)$, and COMPOSE is xor. A query counts the ones in a range.

## Variations

- **Tags not yet applied to the node itself.** Some code keeps $val[x]$ without its own tag and applies the tag when it reads the node. Both conventions work, but one program must use only one of them.
- **Permanent tags.** When the maps commute and a query can apply a map to a partial answer, as with add and sum, the tags never move. A query sums the tags on its path, each multiplied by the length of the overlap of its node with the query. This avoids PUSH and works for [persistent](/persistent-segment-tree/) trees, where copying children on each push is expensive.
- **Iterative lazy tree.** A bottom-up tree of size $2^k$ pushes the tags on the two root-to-leaf paths of $l$ and $r - 1$ first, then works on the loop from the leaves up, then pulls the values back up. The AtCoder Library uses this form.
- **[Dynamic segment tree](/dynamic-segment-tree/).** PUSH creates the children of a node when they do not exist yet, so range updates work on index ranges of size $10^9$ or more.
- **Two kinds of updates.** Assignment and addition together use the tag (set or none, add), with the rule that an assignment clears the pending add. This is the affine case with $a \in \{0, 1\}$.
- **Beyond distributive maps.** [Segment tree beats](/segment-tree-beats/) keeps extra values (the maximum and the second maximum) so that "chmin" updates can stop early: range chmin with sum queries takes $O(\log n)$ amortized time, and mixes with range add take $O(\log^2 n)$. The [Chtholly tree](/chtholly-tree/) handles assignments by keeping runs of equal values.

## Pitfalls

- **No PUSH before going down.** If line L8 or line L13 skips PUSH, the children are read or changed with an old tag still above them. The tag is pushed later and is applied after an update that came after it, and with assignment this gives wrong values.
- **The wrong order in COMPOSE.** Line L2 must put the new map after the old tag. For add, the order does not matter, but for assignment followed by add, or for affine maps, the swapped order is wrong: "set to 5, then add 2" is 7, but "add 2, then set to 5" is 5.
- **No length in the value.** MAP for add with sum queries must add $c$ times the length of the node. Code that adds only $c$ gives the right answer for single items and wrong answers for longer ranges.
- **A real value used as "no tag".** For assignment, "set to 0" is a real update. Use a separate flag or a value outside the input range for ID, or line L3 skips needed pushes.
- **No pull after the recursion.** Line L10 must recompute the value of $x$ from its children after UPDATE. Without it, the node keeps an old total.
- **Too small arrays.** A recursive tree on $n$ leaves with the root at index 1 uses indices up to less than $4n$. An array of size $2n$ is too small when $n$ is not a power of two.

## Exercises

1. Write MAP and COMPOSE for updates "add $c$ to the range" and queries "sum of squares of the range". What must a node value hold?
2. Show that the cost bound of four visited nodes per depth is tight: give $n$ and a range on which some depth has four visited nodes.
3. Support "add $c \cdot (i - l + 1)$ to each $A[i]$ for $l \le i < r$" (an arithmetic progression on a range) and range sums with lazy propagation. What is the tag?
4. On a 0/1 array, support range flip and the query "longest run of ones in a range". Which values must a node keep?

## References
