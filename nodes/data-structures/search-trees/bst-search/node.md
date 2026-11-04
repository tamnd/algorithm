---
tag: EJR7Z3
kind: algorithm
slug: bst-search
name: Binary search tree search
aliases:
- BST lookup
- tree search
area: data-structures/search-trees
level: intro
summary: Descend from the root, going left or right by key comparison; O(h) time.
model: comparison-model
complexity:
  vars: {n: the number of keys, h: the height of the tree}
  time: {worst: Θ(h), average: Θ(log n), best: Θ(1)}
  space: {extra: Θ(1)}
properties: {deterministic: true, comparison: true, recursive: false, in_place: true}
prereqs: [binary-search-tree, binary-search-tree-property]
see_also: [binary-search, bst-insertion, bst-floor-and-ceiling, random-binary-search-tree, expected-search-cost-bst, sorted-search-lower-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 12.2 (Querying a binary search tree), TREE-SEARCH and ITERATIVE-TREE-SEARCH
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2 (Binary tree searching), Algorithm T and the analysis of the average number of comparisons
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 3.2 (Binary search trees), search, and Proposition C on the cost in a BST built from random keys
---

BST search finds the node with a given key in a [binary search tree](/binary-search-tree/): it starts at the root, compares the key with the key of the current node, and goes left if the key is smaller and right if it is larger, until it finds the key or reaches an empty subtree. By the [binary search tree property](/binary-search-tree-property/), the key cannot be in the subtree that the search skips. It takes $O(h)$ time, where $h$ is the height of the tree, and $O(1)$ extra space. On a tree of height $\Theta(\log n)$ it is the tree form of [binary search](/binary-search/).

## In plain words

Picture a road with a sign at each fork. Each sign shows a number. If the number you want is smaller, take the left road. If it is larger, take the right road. If it is the same, you have arrived.

A binary search tree is built so that this rule is always safe: everything smaller than a sign is down its left road, and everything larger is down its right road. So you never need to come back and try the other road. If a road ends before you find your number, the number is not in the tree.

The number of forks you pass is at most the length of the longest road. In a bushy tree that is small, even for a very large number of keys.

## The problem

The input is a binary search tree with root $x$ and a key $k$. The output is the node of the tree whose key equals $k$, or NIL if no node has key $k$. The tree is not changed. The keys come from a total order, and the algorithm only compares keys.

## The algorithm

```pseudo id=main
TREE-SEARCH(x, k)                     ▷ x is the root of a BST
L1  while x ≠ NIL do
L2      if k = x.key then return x
L3      if k < x.key then x ← x.left
L4      else x ← x.right                 ▷ here k > x.key
L5  return NIL
```

The loop keeps one pointer $x$. Line L2 stops at a match. Otherwise lines L3 and L4 move $x$ to the one child whose subtree can still hold $k$. When $x$ becomes NIL, the search has fallen out of the tree at the place where $k$ would be inserted, and line L5 reports a miss.

Each step does one three-way comparison of $k$ with $x.key$. A language with only $<$ can do it with two tests, $k < x.key$ and $x.key < k$, as the Python code does.

## Example

Search the tree built by inserting 15, 6, 18, 3, 7, 17, 20, 2, 4, 13 and 9 in this order.

```
            15
          /    \
         6      18
        / \    /  \
       3   7  17   20
      / \   \
     2   4   13
             /
            9
```

**Search for 13.**

| step | $x$ | compare | action |
|---|---|---|---|
| 1 | 15 | $13 < 15$ | go left |
| 2 | 6 | $13 > 6$ | go right |
| 3 | 7 | $13 > 7$ | go right |
| 4 | 13 | $13 = 13$ | return the node |

**Search for 8.**

| step | $x$ | compare | action |
|---|---|---|---|
| 1 | 15 | $8 < 15$ | go left |
| 2 | 6 | $8 > 6$ | go right |
| 3 | 7 | $8 > 7$ | go right |
| 4 | 13 | $8 < 13$ | go left |
| 5 | 9 | $8 < 9$ | go left |
| 6 | NIL | | return NIL |

The miss ends at the empty left child of 9. That is the place where [BST insertion](/bst-insertion/) would put 8. A search for 15 stops after one comparison, at the root.

## Correctness

The loop of line L1 keeps this invariant: *if some node of the tree has key $k$, it is in the subtree rooted at $x$.* At the start $x$ is the root. If $k < x.key$, then by the BST property each node of the right subtree has a key larger than $x.key > k$, so the node with key $k$, if any, is in the left subtree, and line L3 keeps the invariant. Line L4 is the mirror case. The depth of $x$ grows by 1 in each step, so the loop stops after at most $h + 1$ steps. At a return in line L2 the answer is right. At line L5, $x$ is NIL, the subtree is empty, and by the invariant no node has key $k$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Let $d$ be the depth of the node where the search stops: the depth of the found node, or the depth of the last node visited for a miss. The loop runs $d + 1$ times and each run takes $O(1)$ time, so the time is $\Theta(d + 1)$.

- **Worst case.** $d \le h$, so the time is $O(h)$. For each tree there is a key whose search reaches depth $h$, so the bound $\Theta(h)$ is tight. The height ranges from $\lfloor \lg n \rfloor$ to $n - 1$, so the worst case is $\Theta(n)$ on a chain.
- **Best case.** The key is at the root: one comparison, $\Theta(1)$.
- **Average case.** In a BST built by inserting $n$ distinct keys in a uniformly random order, the expected number of nodes visited by a successful search for a uniformly random key of the tree is $C_n = 2(1 + 1/n) H_n - 3$, and by an unsuccessful search for a uniformly random one of the $n + 1$ gaps it is $C'_n = 2 H_{n+1} - 2$ (Knuth, Section 6.2.2), where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). Both are $2 \ln n + O(1) \approx 1.39 \lg n$. For $n = 6$: $C_6 = 163/60 \approx 2.72$ and $C'_6 = 223/70 \approx 3.19$. See [randomly built BSTs](/random-binary-search-tree/).
- **Space.** The iterative version uses $O(1)$ extra space. The recursive version uses a stack of depth $d + 1$.
- **Lower bound.** In the [comparison model](/comparison-model/), each search algorithm on $n$ keys needs $\lceil \lg(n + 1) \rceil$ comparisons in the worst case ([sorted search lower bound](/sorted-search-lower-bound/)). A tree of minimum height meets this bound with three-way comparisons.

## Properties

- **Read only.** The search does not change the tree, so many searches can run at the same time on a tree that no one changes.
- **One path.** It visits the nodes of one root-to-node path, in order, which is what makes it the base of insertion, deletion, floor and ceiling.
- **Comparison based.** It uses only comparisons of keys, so it works for any total order: numbers, strings, tuples.
- **No parent pointers needed.** The search goes only down.

## Variants and improvements

- **Recursive form.** CLRS gives TREE-SEARCH as a recursive procedure: return $x$ if $x = $ NIL or $k = x.key$, else recurse on the left or right child. It is the same algorithm, with $\Theta(d)$ stack space. The iterative form is faster in most languages.
- **Two-way comparisons.** Test only $k < x.key$ on the way down, remember the last node where the test failed, and test equality once at the end. This uses one comparison per level instead of up to two, at the cost of always going to a leaf. Andersson proposed this for search trees in 1991.
- **Floor, ceiling, rank.** The same descent, with a record of the best candidate so far, answers [floor and ceiling](/bst-floor-and-ceiling/) queries. With subtree sizes it computes [rank and select](/order-statistic-tree/).
- **Search with a sentinel.** If each empty child points to one sentinel node, and the search first stores $k$ in the sentinel, the test $x \ne$ NIL can go: the search always stops at a key equal to $k$.
- **Splaying.** A [splay tree](/splay-tree/) runs the same search, then moves the found node to the root with [splaying](/splaying/), so that a later search for a nearby or recent key is fast.

## When to use it

Use it for each lookup in a binary search tree. The search is only as fast as the tree is short, so pair it with a balanced tree ([red-black tree](/red-black-tree/), [AVL tree](/avl-tree/), [treap](/treap/)) when the input order is not random. If the set does not change, [binary search](/binary-search/) on a sorted array does the same comparisons with better cache behaviour and no pointers. If no ordered query is needed, a [hash table](/hash-table/) lookup is faster on average.

## Pitfalls

- **Comparing with the wrong side.** Writing "if $k > x.key$ then go left" in line L3 breaks the search on each tree with more than one level. The side must match the BST property: smaller keys are on the left.
- **Testing only $<$.** With only "if $k < x.key$ then left else right" and no equality test, as in line L4 alone, the search never stops at a match and always runs to NIL. Line L2, or the final test of the two-way variant, is required.
- **Floating-point keys.** With NaN keys, $k < x.key$ and $k > x.key$ can both be false while $k \ne x.key$, so the three cases of lines L2 to L4 do not cover all inputs. Keep NaN out of the tree.
- **Recursion depth.** On a chain of $10^5$ nodes, the recursive form overflows the default stack of Python and of many threads in other languages. Use the loop of lines L1 to L4.
- **Using a miss as an insert point after a change.** The NIL place where a miss ends is the right place to insert only if the tree has not changed since the search.

## Implementations

The Python function takes the root node and needs only `<` on the keys. The file also has a small insert helper, used by the tests to build trees.

## History

Knuth, in the history at the end of Section 6.2.2, reports that tree search was found independently by several people in the 1950s and was first published around 1960. The algorithm has not changed since: TREE-SEARCH in CLRS and Algorithm T in Knuth do the same comparisons.

## References
