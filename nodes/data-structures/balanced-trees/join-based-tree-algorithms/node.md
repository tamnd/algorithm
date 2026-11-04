---
tag: K1RTAT
kind: technique
slug: join-based-tree-algorithms
name: Join-based tree algorithms
aliases:
- join-based balanced tree framework
- join algorithm for balanced trees
area: data-structures/balanced-trees
level: research
summary: A unified way to implement set operations such as union, intersection and difference on many balanced trees using a single join operation.
prereqs: [balanced-binary-search-tree, avl-tree, treap-split, treap-merge]
see_also: [avl-tree, red-black-tree, weight-balanced-tree, treap, treap-split, treap-merge, ordered-set, fork-join-parallelism]
sources:
  - paper: doi:10.1145/2935764.2935768
    title: Guy E. Blelloch, Daniel Ferizovic and Yihan Sun, Just join for parallel ordered sets, SPAA 2016
    locator: the JOIN algorithms for AVL, red-black, weight-balanced trees and treaps, and the bounds for UNION, INTERSECT and DIFFERENCE
  - paper: doi:10.1145/3512769
    title: Guy E. Blelloch, Daniel Ferizovic and Yihan Sun, Joinable parallel balanced binary trees, ACM Transactions on Parallel Computing 9(2), 2022
    locator: the journal version, with the full proofs of the work and span bounds
  - paper: doi:10.1017/S0956796800000885
    title: Stephen Adams, Efficient sets, a balancing act, Journal of Functional Programming 3(4), 1993
    locator: the concat3 operation and set operations on weight-balanced trees written through it
  - paper: doi:10.1145/322123.322127
    title: Mark R. Brown and Robert E. Tarjan, A fast merging algorithm, Journal of the ACM 26(2), 1979
    locator: the lower bound of log of (n+m choose m) comparisons for merging
  - paper: doi:10.1145/3178487.3178509
    title: Yihan Sun, Daniel Ferizovic and Guy E. Blelloch, PAM, parallel augmented maps, PPoPP 2018
    locator: the library built on join, and augmented maps
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM, 1983
    locator: Chapter 4, Search Trees, joining and splitting red-black trees
---

Join-based tree algorithms write every operation of an ordered set or map on a [balanced binary search tree](/balanced-binary-search-tree/) through one primitive, JOIN$(L, k, R)$. Here every key of $L$ is less than $k$, and every key of $R$ is greater; JOIN returns a balanced tree holding the keys of $L$, then $k$, then the keys of $R$. Only JOIN knows the balance rule. Everything else, including insertion, deletion, SPLIT and the bulk operations UNION, INTERSECT and DIFFERENCE, is written once, the same way for [AVL trees](/avl-tree/), [red-black trees](/red-black-tree/), [weight-balanced trees](/weight-balanced-tree/) and [treaps](/treap/). Guy Blelloch, Daniel Ferizovic and Yihan Sun (2016) showed that with this scheme, on all four trees, the bulk operations on sets of sizes $m \le n$ take $O(m \log(n/m + 1))$ work, which is optimal for comparison-based merging, and $O(\log n \log m)$ span when the two recursive calls run in parallel.

## In plain words

Think of JOIN as glue. You hand it a small-keys tree, one middle key, and a large-keys tree. It puts them together into one balanced tree, doing a little rotating where the two trees meet.

Once you have this glue, the other operations become simple recursions. To split a tree at a key, walk down to the key and glue the pieces back together on the way up. To take the union of two trees, cut the second tree at the root key of the first, take the union of the two left halves and of the two right halves, and glue the results around the root key. The two halves do not touch each other, so two processors can work on them at the same time. Only the glue depends on which kind of balanced tree you use.

## When it applies

- The tree is a binary search tree with a balance rule for which a fast JOIN exists: AVL, red-black, weight-balanced, treaps, and also [WAVL trees](/wavl-tree/), [zip trees](/zip-tree/) and B-trees in a similar form.
- The operations are on whole sets or maps: union, intersection, difference, filter, building from a sorted list, range extraction, and bulk insertion or deletion.
- Parallel or functional code. The algorithms are divide and conquer with independent halves, and with path copying they never change an input tree, which gives [persistent](/persistent-data-structure/) sets for free.
- A tree with *augmented* data, such as sizes or sums, as in an [order-statistic tree](/order-statistic-tree/). Only JOIN creates nodes, so it is the one place where the augmented value is computed.

It is a poor fit when the only operations are single insertions and searches on one mutable tree; there the classic bottom-up rebalancing with parent pointers does fewer allocations.

## The template

Fix a balanced tree scheme, and write NODE$(L, k, R)$ for a new node with those children and its balance data computed from them. The scheme must give:

1. **JOIN$(L, k, R)$.** Keys of $L$ < $k$ < keys of $R$. If $L$ and $R$ are already "close" in balance (heights within one for AVL, the same black height for red-black, weights within the ratio for weight-balanced trees, $k$ of larger priority than both roots for treaps), return NODE$(L, k, R)$. Otherwise, say $L$ is the larger one: walk down the right spine of $L$ to the first node $c$ that is close to $R$, replace $c$ by NODE$(c, k, R)$, and rebalance on the way back up, as after an insertion. For AVL trees this costs $O(|h(L) - h(R)| + 1)$.

On top of JOIN, the following is generic.

```pseudo id=main
SPLIT(T, k)                          ▷ returns (L, found, R)
L1  if T = nil then return (nil, false, nil)
L2  (l, m, r) ← (T.left, T.key, T.right)
L3  if k = m then return (l, true, r)
L4  if k < m then (L', b, R') ← SPLIT(l, k); return (L', b, JOIN(R', m, r))
L5  (L', b, R') ← SPLIT(r, k); return (JOIN(l, m, L'), b, R')

JOIN2(L, R)                          ▷ join without a middle key
L6  if L = nil then return R
L7  (L', k) ← SPLIT-LAST(L); return JOIN(L', k, R)

UNION(A, B)
L8  if A = nil then return B;  if B = nil then return A
L9  (L, b, R) ← SPLIT(B, A.key)
L10 in parallel: TL ← UNION(A.left, L);  TR ← UNION(A.right, R)
L11 return JOIN(TL, A.key, TR)

INTERSECT(A, B)
L12 if A = nil or B = nil then return nil
L13 (L, b, R) ← SPLIT(B, A.key)
L14 in parallel: TL ← INTERSECT(A.left, L);  TR ← INTERSECT(A.right, R)
L15 if b then return JOIN(TL, A.key, TR) else return JOIN2(TL, TR)

DIFFERENCE(A, B)                     ▷ keys of A not in B
L16 if A = nil or B = nil then return A
L17 (L, b, R) ← SPLIT(A, B.key)
L18 in parallel: TL ← DIFFERENCE(L, B.left);  TR ← DIFFERENCE(R, B.right)
L19 return JOIN2(TL, TR)
```

SPLIT-LAST$(L)$ removes the largest key of a nonempty tree: if $L$ has no right child it returns $(L.left, L.key)$, else it recurses on $L.right$ to get $(L', k)$ and returns $(\text{JOIN}(L.left, L.key, L'), k)$. INSERT$(T, k)$ is $(L, b, R) \leftarrow$ SPLIT$(T, k)$ followed by JOIN$(L, k, R)$, and DELETE$(T, k)$ is SPLIT followed by JOIN2.

**Why it is correct.** Each line keeps the order condition of JOIN: in line L4 the keys of $R'$ lie between $k$ and $m$ and those of $r$ above $m$; in line L11 the keys of TL are less than A.key and those of TR are greater, since $L$ and $R$ are the parts of $B$ below and above A.key. Each JOIN returns a balanced tree, so every result is balanced, whatever the scheme. The key sets follow by induction: for example the keys of UNION are $(K(A.\text{left}) \cup K(L)) \cup \{A.\text{key}\} \cup (K(A.\text{right}) \cup K(R))$, which is $K(A) \cup K(B)$.

**Why it is fast.** SPLIT does one JOIN per level. For AVL trees the costs of these joins telescope, because the heights of the pieces grow along the path, so SPLIT takes $O(\log n)$ time; the same holds for the other three schemes. For UNION with $|A| = m \le n = |B|$, the recursion follows the shape of $A$. Blelloch, Ferizovic and Sun bound the total work of the splits and joins by $O(m \log(n/m + 1))$, and this matches the lower bound $\log_2 \binom{n+m}{m}$ of Brown and Tarjan for merging two sorted lists by comparisons. With the two calls of line L10 run in parallel, the span is $O(\log n \log m)$: the recursion depth is $O(\log m)$, and each level does one SPLIT and one JOIN of $O(\log n)$ cost.

## Classic examples

### JOIN for four balance schemes

- **AVL trees.** If $h(L) > h(R) + 1$, walk down the right spine of $L$ to the first node $c$ with $h(c) \le h(R) + 1$, put NODE$(c, k, R)$ in its place, and go back up doing at most one single or double rotation at each level, as in AVL insertion.
- **Red-black trees.** If the black height of $L$ is larger, walk down the right spine of $L$ to a black node $c$ with the black height of $R$, put a red node with key $k$ and children $c$ and $R$ there, and fix a red-red pair as in red-black insertion. Tarjan (1983) gave this join.
- **Weight-balanced trees.** If $L$ is too heavy for $R$, walk down the right spine of $L$ to the first node that is balanced with $R$, and rebalance with single and double rotations on the way up. Adams (1993) called this operation concat3 and wrote his set operations through it.
- **Treaps.** If $k$ has a larger priority than both roots, return NODE$(L, k, R)$. Otherwise, if the root of $L$ has the larger priority, return NODE$(L.\text{left}, L.\text{key}, \text{JOIN}(L.\text{right}, k, R))$, and symmetrically for $R$. With $k$ removed, this is [treap merge](/treap-merge/), and SPLIT is [treap split](/treap-split/).

### A union by hand

Take AVL trees $A$ with keys 1, 3, 5, 7, 9, shaped $(1, 3, (5, 7, 9))$ with root 3, and $B$ with keys 2, 3, 4, 8, shaped $(2, 3, (4, 8, \text{nil}))$. UNION$(A, B)$ splits $B$ at 3 and gets $L = (2)$, found, $R = (4, 8, \text{nil})$. The left call UNION$((1), (2))$ splits $(2)$ at 1 and returns JOIN$(\text{nil}, 1, (2)) = (\text{nil}, 1, 2)$. The right call UNION$((5, 7, 9), (4, 8, \text{nil}))$ splits at 7 into $(4)$ and $(8)$, recurses to $(4, 5, \text{nil})$ and $(8, 9, \text{nil})$, and joins them around 7. The final JOIN around 3 gives

$((\text{nil}, 1, 2), 3, ((4, 5, \text{nil}), 7, (8, 9, \text{nil})))$,

an AVL tree with keys 1 to 5 and 7 to 9. INTERSECT$(A, B)$ gives the single node 3, and DIFFERENCE$(A, B)$ gives $((\text{nil}, 1, 5), 7, 9)$. A Python version of the AVL join and of lines L1 to L19 agrees with Python sets on 600 random pairs of sets drawn with seed 2016, and every result passes the AVL check.

### JOIN of trees of very different heights

JOIN$(T_7, 8, (9))$, where $T_7$ is the perfect AVL tree on 1 to 7 and $(9)$ a single node, walks down the right spine of $T_7$ to the node 6, of height 2, which is within one of $h((9)) = 1$. It makes NODE$((5, 6, 7), 8, (9))$ of height 3 there, and then the root 4 has subtrees of heights 2 and 3, which is balanced. The result is $((1, 2, 3), 4, ((5, 6, 7), 8, 9))$. The work is proportional to the height difference, two levels, not to the size.

### Libraries

The PAM library of Sun, Ferizovic and Blelloch (2018) implements parallel ordered maps and augmented maps in C++ on top of join, with a choice of the four balance schemes. The `Data.Set` and `Data.Map` modules of Haskell's containers package are weight-balanced trees in the style of Adams, with a `link` function in the role of JOIN.

## Variations

- **Augmented maps.** If each node stores a value computed from its subtree, such as a sum or a maximum, NODE computes it, and every operation above keeps it correct. Range sums, interval trees and range trees can then be written with the same template.
- **Bulk updates.** Build a tree from a sorted batch, then UNION or DIFFERENCE it with the main tree, which inserts or deletes $m$ keys in $O(m \log(n/m + 1))$ work.
- **Filter, map-reduce and range.** FILTER$(T, p)$ recurses on both children in parallel and calls JOIN or JOIN2 depending on $p(T.\text{key})$. RANGE$(T, a, b)$ is two splits.
- **Persistence.** With NODE always making a new node and no pointer ever written twice, every operation leaves its inputs unchanged and shares unchanged subtrees, at $O(\log n)$ extra nodes per split or join.
- **Other trees.** The same framework works for B-trees, with JOIN defined on nodes of different heights, and for any scheme whose JOIN costs $O(|r(L) - r(R)| + 1)$ in some rank $r$ that is $\Theta(\log n)$.

## Pitfalls

- **JOIN must accept any two balanced trees.** A JOIN that only handles trees of equal height, like the root case of NODE, breaks SPLIT, whose pieces can differ in height a lot. The spine walk is the part that matters.
- **JOIN2 where JOIN would do.** JOIN2 first removes the last key of $L$, which costs $O(\log n)$ more than a JOIN. Use it only where no middle key is available, as in lines L15 and L19; UNION always has the key A.key and should call JOIN.
- **Duplicate keys.** The algorithms assume distinct keys; for maps, UNION must decide which value wins when a key is in both trees, at line L11.
- **Rebalancing data out of date.** In a mutable implementation that reuses nodes, every node changed by a rotation must have its height, color or size recomputed, or later joins take wrong branches.
- **Parallel grain.** Spawning a task for each tiny subtree costs more than it saves; switch to sequential code below a cutoff size.

## Exercises

1. Write JOIN for treaps using [treap merge](/treap-merge/), and show that SPLIT and UNION of the template then give the usual treap algorithms.
2. For AVL trees, show that the heights of the trees joined during SPLIT along a search path telescope, so that SPLIT takes $O(\log n)$ time.
   <details><summary>Hint</summary>On the side where pieces are joined, each join adds a node whose subtree contains the previous result; bound the cost of each join by the height difference and sum.</details>
3. Show that $\log_2 \binom{n+m}{m} = \Theta(m \log(n/m + 1))$ for $1 \le m \le n$, and conclude that UNION is optimal up to a constant factor among comparison-based algorithms.
4. Write FILTER$(T, p)$ with JOIN and JOIN2, and give its work and span for an AVL tree of $n$ keys.
5. Trace UNION$(A, B)$ for $A$ the perfect tree on 2, 4, 6 and $B$ the perfect tree on 1, 3, 5, 7, using the AVL JOIN. Draw the tree after each JOIN.
6. Show how to write INSERT and DELETE of an ordered map with SPLIT, JOIN and JOIN2, and compare the number of rotations with AVL insertion.
7. Add a size field to each node, computed in NODE, and use it to write SELECT$(T, i)$ and a SPLIT by position. Which lines of the template change?

## References
