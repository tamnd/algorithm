---
tag: 0YHN5A
kind: data-structure
slug: weight-balanced-tree
name: Weight-balanced tree
aliases:
- BB[alpha] tree
- bounded-balance tree
area: data-structures/balanced-trees
level: advanced
summary: A BST that keeps each subtree's size within a fixed ratio of its sibling's, balanced by rotations that use subtree sizes.
implements: [ordered-set]
model: comparison-model
complexity:
  vars: {n: the number of keys in the tree}
  time: {worst: Θ(log n)}
  space: {extra: Θ(n)}
prereqs: [binary-search-tree, tree-rotation, balanced-binary-search-tree]
see_also: [scapegoat-tree, order-statistic-tree, join-based-tree-algorithms, avl-tree, red-black-tree, tree-rebalancing, treap]
sources:
  - paper: doi:10.1137/0202005
    title: Jürg Nievergelt and Edward M. Reingold, Binary search trees of bounded balance, SIAM Journal on Computing 2(1), 1973
    locator: pages 33 to 43, the root balance and the class BB[alpha]
  - paper: doi:10.1016/0304-3975(80)90018-3
    title: Norbert Blum and Kurt Mehlhorn, On the average number of rebalancing operations in weight-balanced trees, Theoretical Computer Science 11(3), 1980
    locator: the range of alpha for which rebalancing works, and the amortized number of rotations
  - paper: doi:10.1017/S0956796800000885
    title: Stephen Adams, Efficient sets, a balancing act, Journal of Functional Programming 3(4), 1993
    locator: the functional version with the parameters delta and gamma
  - paper: doi:10.1017/S0956796811000104
    title: Yoichi Hirai and Kazuhiko Yamamoto, Balancing weight-balanced trees, Journal of Functional Programming 21(3), 2011
    locator: the valid parameter pairs, and the proof that (3, 2) is the only integer pair
---

A weight-balanced tree is a [binary search tree](/binary-search-tree/) that balances by size instead of height. Each node stores the number of keys in its subtree, and the rule says that neither child of a node may be much heavier than the other: with the *weight* of a subtree defined as its size plus one, a child may weigh at most $\Delta$ times its sibling, for a fixed constant such as $\Delta = 3$. After an insertion or deletion, the nodes on the search path that break the rule are repaired with a single or a double [rotation](/tree-rotation/), chosen by a second constant $\Gamma$. The height is at most $\log_{4/3} \frac{n+1}{2} < 2.41 \lg(n + 1)$ for $\Delta = 3$, so all operations take $\Theta(\log n)$ time in the worst case, and the stored sizes give rank and select for free. Jürg Nievergelt and Edward Reingold introduced the trees in 1972 as trees of *bounded balance*, the class BB[$\alpha$].

## In plain words

An AVL tree asks that the two sides of each node have about the same height. A weight-balanced tree asks that they hold about the same number of keys, within a factor. With a factor of 3, a node may have 10 keys on its left and 30 on its right, but not 10 and 40.

Each node keeps a count of the keys below it. When an insertion or deletion makes one side too heavy, a rotation moves part of the heavy side across to the light side. If the heavy side is heavy on its outside, one rotation is enough. If it is heavy on its inside, two rotations are needed. Since every node splits its keys in a fair way, the tree cannot get deep, and the counts also tell you, for example, which key is the hundredth.

## The abstract type

The tree implements an [ordered set](/ordered-set/): CONTAINS$(k)$, INSERT$(k)$ and DELETE$(k)$ on keys from a totally ordered universe, and the keys in increasing order. Because the sizes are stored, it also supports SELECT$(i)$, the key of rank $i$, and RANK$(k)$, the number of keys less than $k$, as an [order-statistic tree](/order-statistic-tree/) does.

## Representation

A node holds a key, two children and $size$, the number of keys in its subtree. Write $w(t) = size(t) + 1$, so $w(\text{nil}) = 1$ and $w(t) = w(t.left) + w(t.right)$. With parameters $\Delta$ and $\Gamma$, the rule is:

1. (B) At each node $t$, $w(t.left) \le \Delta \cdot w(t.right)$ and $w(t.right) \le \Delta \cdot w(t.left)$.

The code here uses $(\Delta, \Gamma) = (3, 2)$. The classic form of Nievergelt and Reingold uses the *root balance* $\rho(t) = w(t.left) / w(t)$ and asks that $\alpha \le \rho(t) \le 1 - \alpha$ at every node; this is the class BB[$\alpha$]. The two forms are the same with $\alpha = 1/(\Delta + 1)$, so $\Delta = 3$ is BB[$1/4$].

The weight uses size plus one, not size, so that an empty side and a side of one key compare sensibly: a node with one child that is a leaf has weights 1 and 2, which is fine, and a node with a child of three keys and no other child has weights 1 and 4, which is not.

## Operations

The code is in the functional style of Adams: NODE$(l, k, r)$ makes a node and sets its size, and BALANCE$(l, k, r)$ builds a node from two subtrees whose weights were in balance before one key was added to or removed from one side. INSERT and DELETE rebuild the search path bottom-up, calling BALANCE at each node.

```pseudo id=main
BALANCE(l, k, r)
L1  if Δ · w(l) < w(r) then return ROTATE-LEFT-CASE(l, k, r)
L2  if Δ · w(r) < w(l) then return ROTATE-RIGHT-CASE(l, k, r)      ▷ the mirror image
L3  return NODE(l, k, r)

ROTATE-LEFT-CASE(l, k, r)                  ▷ r is too heavy
L4  if w(r.left) < Γ · w(r.right) then return NODE(NODE(l, k, r.left), r.key, r.right)      ▷ single
L5  m ← r.left; return NODE(NODE(l, k, m.left), m.key, NODE(m.right, r.key, r.right))     ▷ double

INSERT(t, k)
L6  if t = nil then return NODE(nil, k, nil)
L7  if k < t.key then return BALANCE(INSERT(t.left, k), t.key, t.right)
L8  if k > t.key then return BALANCE(t.left, t.key, INSERT(t.right, k)); else return t

DELETE(t, k)                               ▷ return nil when t = nil
L9  if k < t.key then return BALANCE(DELETE(t.left, k), t.key, t.right); mirror for k > t.key
L10 return GLUE(t.left, t.right)           ▷ k = t.key

GLUE(l, r)
L11 if l = nil then return r; if r = nil then return l
L12 if size(l) > size(r) then (m, l′) ← DELETE-MAX(l); return BALANCE(l′, m, r)
    else (m, r′) ← DELETE-MIN(r); return BALANCE(l, m, r′)
```

DELETE-MIN$(t)$ returns the least key and the tree without it: if $t.left$ is nil, it returns $t.key$ and $t.right$, and otherwise it recurses on the left and calls BALANCE on the way back. DELETE-MAX is the mirror image. SELECT and RANK walk down one path and use the sizes of the left subtrees.

Because NODE makes new nodes and never changes old ones, each update copies only its search path, $O(\log n)$ nodes, and the old version of the tree stays valid. A mutable version does the same rotations in place.

## Example

Insert 1 to 8 in increasing order, with $(\Delta, \Gamma) = (3, 2)$. Trees are written (left, key, right).

| insert | test at the root | tree |
|---|---|---|
| 1, 2, 3 | at 1, weights 1 and 3: allowed | (nil, 1, (nil, 2, 3)) |
| 4 | at 1, weights 1 and 4: $3 \cdot 1 < 4$; inner weight 1 $< 2 \cdot 3$, single rotation | (1, 2, (nil, 3, 4)) |
| 5, 6, 7 | rotations lower down only | (1, 2, (3, 4, (nil, 5, (nil, 6, 7)))) |
| 8 | at 2, weights 2 and 7: $3 \cdot 2 < 7$; inner weight 2 $< 2 \cdot 5$, single rotation | ((1, 2, 3), 4, (5, 6, (nil, 7, 8))) |

A double rotation needs a heavy inner grandchild. Insert 1, 4, 2: the tree is (nil, 1, (2, 4, nil)), with weights 1 and 3 at the root. Insert 3, below 2. At 4, the weights are 3 and 1, which is allowed. At 1, the weights are 1 and 4, too heavy on the right, and the inner subtree (rooted at 2) has weight 3, which is not less than $2 \cdot 1$. So line L5 does a double rotation: 2 becomes the root, with 1 on the left and 4 on the right, and 3 becomes the left child of 4. The tree is (1, 2, (3, 4, nil)).

For deletion, insert 1 to 10 and delete 1. Then delete 2: it has only a right child 3, so GLUE returns the leaf 3, and at the root 4 the weights are 2 and 7. A single rotation makes 6 the root, and the tree is ((3, 4, 5), 6, (7, 8, (nil, 9, 10))).

## Correctness

The key step is a lemma about BALANCE: if $l$ and $r$ satisfy (B) inside, and their weights satisfy $w(l) \le 3w(r) + 3$ and $w(r) \le 3w(l) + 3$, which holds after one key is added to or removed from one side of a balanced pair, then the result satisfies (B). With $a = w(l)$ and $b$, $c$ the weights of the subtrees of $r$, the case of line L1 has $3a < b + c \le 3a + 3$. When $b < 2c$, the single rotation gives the new nodes weights $(a, b)$ and $(a + b, c)$, and each of the four inequalities follows from these bounds. When $b \ge 2c$, the double rotation splits $r.left$, of weight $b = d + e$ with $d, e \ge b/4$, and gives weights $(a, d)$, $(e, c)$ and $(a + d, e + c)$; six short inequalities follow.

With the lemma, INSERT and DELETE are correct by induction on the size of the tree, since each recursive call changes the size of one subtree by at most one. GLUE needs no rotation at all: it takes a key from the larger of two subtrees of a balanced node, which keeps the pair balanced. The full proof is in the proofs folder.

The parameters matter. Hirai and Yamamoto checked all pairs $(\Delta, \Gamma)$ and showed that for this algorithm, $(3, 2)$ is the only pair of integers for which both insertion and deletion keep the rule. With other pairs, some sequences of operations break (B).

## Complexity

**Height.** If $w(t.left) \le 3\,w(t.right)$, then $w(t.left) \le \frac34 w(t)$, and the same on the right. So the weight drops by a factor of at least $\frac43$ per level, and a tree with $n$ keys has height at most $\log_{4/3} \frac{n+1}{2}$, about $2.41 \lg n$. For BB[$\alpha$] in general, the height is at most $\log_{1/(1-\alpha)} (n + 1)$.

**Time.** Search, insertion, deletion, rank and select follow one path and do $O(1)$ work per node, so they take $\Theta(\log n)$ time in the worst case. An insertion or deletion can rotate at every node of the path, $O(\log n)$ rotations in the worst case. Blum and Mehlhorn showed that, for suitable $\alpha$, the amortized number of rotations per update is $O(1)$, and that rotations near the root, which move many keys, are rare: a node of weight $w$ is rotated only once per $\Omega(w)$ updates in its subtree. This matters when each rotation costs time proportional to the subtree, as in trees with secondary structures.

**Space.** One size field per node, $O(\log n)$ bits, and $\Theta(n)$ space in all. The functional version uses $O(\log n)$ new nodes per update.

## Variants

- **BB[$\alpha$] with bottom-up repair.** The original trees keep $\alpha \le \rho(t) \le 1 - \alpha$ and repair with single or double rotations. Nievergelt and Reingold proved rebalancing correct for $\alpha \le 1 - 1/\sqrt{2} \approx 0.293$; Blum and Mehlhorn found a gap in that proof and gave a correct one for $\frac{2}{11} < \alpha \le 1 - 1/\sqrt2$.
- **Top-down repair.** Lai and Wood gave a top-down version that rebalances on the way down, in one pass.
- **Functional sets.** Adams's trees, with $(\Delta, \Gamma)$, are the basis of the set and map libraries of Haskell, MIT Scheme and SML/NJ. Their union, intersection and difference use split and join, as in [join-based tree algorithms](/join-based-tree-algorithms/).
- **Partial rebuilding.** A [scapegoat tree](/scapegoat-tree/) uses the same weight criterion but stores no sizes; it lets nodes become unbalanced and rebuilds a whole subtree when a path gets too long.
- **Sizes for free.** Since the sizes are stored anyway, the tree is a natural [order-statistic tree](/order-statistic-tree/), and it supports splitting by rank and indexing into a sequence.

## When to use it

Use a weight-balanced tree when you need sizes in the nodes anyway, for rank, select or positional access; when you want functional, persistent sets and maps with fast union and intersection; or when rotations near the root are expensive, since the amortized cost of rebalancing a large subtree is low. For a plain ordered set in a mutable program, a [red-black tree](/red-black-tree/) is about as fast, stores one bit instead of a size, and has a lower height bound.

## Pitfalls

- **Weight is size plus one.** With weight equal to size, a node with an empty child could never get a second key on the other side, since $0 \cdot \Delta = 0$. Keep $w(\text{nil}) = 1$.
- **Wrong parameters.** Not every pair $(\Delta, \Gamma)$ works. Some pairs used in practice were later found to break the rule on deletion, and the analysis of Hirai and Yamamoto led libraries to $(3, 2)$. Use $(3, 2)$, or a pair proved valid.
- **Single or double rotation by the wrong test.** The double rotation is needed when the inner grandchild is heavy: $w(r.left) \ge \Gamma \cdot w(r.right)$ for a heavy right child. Testing the outer grandchild instead, or using $\le$ where $<$ is meant, breaks the rule on some inputs.
- **Stale sizes.** Each rotation must recompute the sizes of the moved nodes from their children, lower node first. A functional NODE constructor makes this automatic.
- **Joining arbitrary trees with BALANCE.** BALANCE only repairs a pair that was nearly balanced. To join two trees of very different sizes, use a join that walks down the larger tree, as in the join-based algorithms.

## Implementations

## History

Jürg Nievergelt and Edward Reingold introduced binary search trees of bounded balance at STOC 1972, with the journal version in 1973. Norbert Blum and Kurt Mehlhorn (1980) corrected the range of $\alpha$ and proved the amortized bounds on rebalancing. Stephen Adams (1992, 1993) gave the functional version with the parameters $\Delta$ and $\Gamma$, and his trees became the set and map libraries of several functional languages. Yoichi Hirai and Kazuhiko Yamamoto (2011) proved, with the Coq proof assistant, which parameters are valid, and showed that $(3, 2)$ is the only integer pair. Blelloch, Ferizovic and Sun (2016) used weight-balanced trees as one of the four trees for which their join-based parallel set operations are work-efficient.

## References
