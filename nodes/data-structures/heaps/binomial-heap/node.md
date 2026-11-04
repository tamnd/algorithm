---
tag: A5XZ80
kind: data-structure
slug: binomial-heap
name: Binomial heap
aliases:
- binomial queue
area: data-structures/heaps
level: core
summary: Forest of binomial trees supporting merge in O(log n) and insert and extract in O(log n).
implements: [priority-queue, meldable-priority-queue]
model: comparison-model
prereqs: [heap, heap-property, binomial-coefficient, binary-counter-increment]
see_also: [binary-heap, fibonacci-heap, leftist-heap, pairing-heap, skew-heap, meldable-priority-queue, accounting-method, k-way-merge]
sources:
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Chapter 19 (Binomial Heaps), Sections 19.1 (binomial trees and binomial heaps) and 19.2 (operations on binomial heaps)
  - paper: "Jean Vuillemin, A data structure for manipulating priority queues, Communications of the ACM 21(4), 1978"
    locator: pages 309 to 315
  - paper: "Mark R. Brown, Implementation and analysis of binomial queue algorithms, SIAM Journal on Computing 7(3), 1978"
    locator: the analysis of insert and of the binomial queue operations
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the part on merging priority queues
---

A binomial heap is a [heap](/heap/) made of a forest of *binomial trees*, at most one of each size $2^k$, so that the trees of a heap of $n$ items match the 1 bits of $n$ written in binary. Two heaps meld like two binary numbers add, with a carry: two trees of the same size link into one tree of twice the size. This gives union, extract-min, decrease-key and delete in $O(\log n)$ worst-case time, and insert in $O(1)$ amortized time. Vuillemin introduced the structure in 1978 as the *binomial queue*. It was the first heap with a fast union and simple code, and it is the base of the [Fibonacci heap](/fibonacci-heap/).

## In plain words

A binomial tree of size 1 is one node. To get the next size, take two trees of the same size and hang one under the root of the other, so the sizes are 1, 2, 4, 8 and so on. Each tree keeps the smaller key on top.

A heap with 13 items, which is 8 plus 4 plus 1, has one tree of each of these sizes. To add an item, add a tree of size 1. If a tree of size 1 is already there, join the two into a tree of size 2, and go on, as when you add 1 to a number in binary. To join two heaps, add them like two binary numbers. To take out the smallest item, look at the tops of the few trees, remove the smallest, and join its subtrees back in.

## The abstract type

A binomial heap implements the [meldable priority queue](/meldable-priority-queue/): MAKE-HEAP, INSERT, MINIMUM, EXTRACT-MIN, UNION, DECREASE-KEY and DELETE, on items with keys from a [total order](/total-order/). DECREASE-KEY and DELETE name the item by a handle that INSERT returns.

## Representation

The *binomial tree* $B_k$ is defined by induction: $B_0$ is one node, and $B_k$ is two copies of $B_{k-1}$, where the root of one copy is made the new child of the root of the other. By induction on $k$, $B_k$ has these properties.

1. It has $2^k$ nodes and height $k$.
2. It has exactly $\binom{k}{i}$ nodes at depth $i$, a [binomial coefficient](/binomial-coefficient/), which gives the name.
3. Its root has degree $k$, larger than the degree of each other node, and the children of the root are roots of $B_{k-1}, B_{k-2}, \ldots, B_0$, from the last linked to the first.

A *binomial heap* $H$ is a list $H.roots$ of binomial trees and a count $H.n$ with

- **(order)** each tree has the min-[heap property](/heap-property/);
- **(shape)** each tree is a $B_k$ for some $k$, and no two trees have the same $k$.

Each node $x$ has the key, the item, a parent pointer $x.p$, its degree $x.degree$, and its children in increasing order of degree. By (shape), $n = \sum 2^{k}$ over the orders $k$ of the trees, so the orders are exactly the positions of the 1 bits of $n$, and there are at most $\lfloor \lg n \rfloor + 1$ trees, each of height at most $\lfloor \lg n \rfloor$.

## Operations

```pseudo id=main
LINK(y, x)                                 ▷ x and y are roots of equal degree, x.key ≤ y.key
L1  y.p ← x
L2  make y the last child of x             ▷ the children stay in increasing order of degree
L3  x.degree ← x.degree + 1

UNION-ROOTS(R1, R2)                        ▷ two lists of roots, each with distinct degrees
L4  T ← an empty table from degrees to trees
L5  for each root x of R1, then each root x of R2, do
L6      d ← x.degree
L7      while T[d] ≠ nil do                ▷ the carry: two trees of degree d
L8          y ← T[d], T[d] ← nil
L9          if y.key < x.key then exchange x and y
L10         LINK(y, x), d ← d + 1
L11     T[d] ← x
L12 R ← the trees of T, in order of degree
L13 return R

INSERT(H, x)                               ▷ x is a new node with its key set
L14 x.p ← nil, x.degree ← 0
L15 while H has a root y with y.degree = x.degree do    ▷ y is the root of least degree
L16     remove y from H.roots
L17     if y.key < x.key then exchange x and y
L18     LINK(y, x)
L19 add x to H.roots as the root of least degree, H.n ← H.n + 1

MINIMUM(H)
L20 if H.roots is empty then error "heap underflow"
L21 return a root of H with the least key

EXTRACT-MIN(H)
L22 x ← MINIMUM(H)
L23 remove x from H.roots
L24 R ← the children of x, each with its parent set to nil
L25 H.roots ← UNION-ROOTS(H.roots, R), H.n ← H.n − 1
L26 return x

DECREASE-KEY(H, x, k)
L27 if k > x.key then error "new key is larger than the current key"
L28 x.key ← k
L29 while x.p ≠ nil and x.key < x.p.key do
L30     exchange the keys and items of x and x.p, and update their handles
L31     x ← x.p

DELETE(H, x)
L32 DECREASE-KEY(H, x, −∞)
L33 EXTRACT-MIN(H)
```

UNION$(H_1, H_2)$ sets $H_1.roots \leftarrow$ UNION-ROOTS$(H_1.roots, H_2.roots)$ and $H_1.n \leftarrow H_1.n + H_2.n$, and empties $H_2$.

**Link** (lines L1 to L3) joins two $B_k$ into one $B_{k+1}$, with the smaller key at the root, in $O(1)$ time.

**Union-roots** (lines L4 to L13) is binary addition. The table $T$ holds at most one tree of each degree. A new tree of degree $d$ that meets a tree of the same degree in $T$ links with it, and the result of degree $d + 1$ is the carry, which goes on to the next degree (lines L7 to L10). At the end, the trees of $T$ have distinct degrees.

**Insert** (lines L14 to L19) adds 1 to the binary number. While a tree of the same degree as the new tree exists, it links them and goes on with the result. Each link takes away the least-degree root, so the loop looks only at the end of the root list.

**Minimum** (lines L20 and L21) looks at the at most $\lfloor \lg n \rfloor + 1$ roots. By the global form of the heap property, a minimum key of the heap is at a root.

**Extract-min** (lines L22 to L26) removes the root $x$ of least key. The children of $x$ are the roots of $B_{k-1}, \ldots, B_0$, so they form a binomial heap by themselves, and UNION-ROOTS melds it with the other trees.

**Decrease-key** (lines L27 to L31) lowers the key and moves it up the tree, as the sift-up of a [binary heap](/binary-heap/) does. The shape of the tree does not change. The items move between nodes, so the handle of an item must be a separate object that knows its node, not the node.

**Delete** (lines L32 and L33) moves the item to the root of its tree and extracts it.

## Example

Insert the keys 12, 7, 25, 15, 28, 33 and 41, in this order, into an empty heap. In the table, $a(b\ c)$ is a tree with the root $a$ and the children $b$ and $c$, with the child of the largest degree first, and the bar separates the trees, from the least degree.

| step | what happens | trees |
|---|---|---|
| insert 12 | $n = 1 = 1_2$ | 12 |
| insert 7 | 7 meets the $B_0$ 12, link | 7(12) |
| insert 25 | $n = 11_2$ | 25 \| 7(12) |
| insert 15 | 15 links with 25 into 15(25), which links with 7(12) | 7(15(25) 12) |
| insert 28, 33 | 33 links with 28 | 28(33) \| 7(15(25) 12) |
| insert 41 | $n = 7 = 111_2$ | 41 \| 28(33) \| 7(15(25) 12) |
| EXTRACT-MIN | returns 7; its children 15(25) and 12 meld with 41 and 28(33): 12 and 41 make 12(41), and 15(25) and 28(33) make 15(28(33) 25) | 12(41) \| 15(28(33) 25) |
| DECREASE-KEY 41 to 3 | 3 < 12, exchange | 3(12) \| 15(28(33) 25) |
| UNION with 9(30) | 9(30) links with 3(12) into a $B_2$, which links with 15(28(33) 25) | 3(15(28(33) 25) 9(30) 12) |
| DELETE 28 | 28 goes up to the root, where it is extracted; the 7 other items form $B_0$, $B_1$ and $B_2$ | 12 \| 9(30) \| 3(15(33) 25) |

After the union, $n = 8 = 1000_2$ and the heap is one $B_3$. After the delete, $n = 7$ and the heap has three trees again.

## Correctness

LINK makes the root with the larger key a child of the other root, so the new edge is ordered and two $B_k$ become a $B_{k+1}$. UNION-ROOTS keeps the invariant that the trees in $T$ are binomial trees with distinct degrees, as in the proof of binary addition, and it keeps each node. INSERT is the same with one new tree of degree 0. EXTRACT-MIN removes a root of least key, which is a minimum by the heap property, and the children of a $B_k$ root are binomial trees of the distinct orders $0, \ldots, k-1$. DECREASE-KEY changes no shape and repairs the order as sift-up does. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

By (shape), a heap of $n$ items has at most $\lfloor \lg n \rfloor + 1$ trees and each tree has height at most $\lfloor \lg n \rfloor$.

- **Union.** UNION-ROOTS gets at most $\lfloor \lg n_1 \rfloor + \lfloor \lg n_2 \rfloor + 2$ roots. Each link lowers the number of trees by 1, and each root costs $O(1)$ besides its links, so the time is $O(\log n)$, with $n = n_1 + n_2$. The table needs $\lfloor \lg n \rfloor + 1$ cells.
- **Minimum.** $O(\log n)$ to look at the roots. A pointer to the minimum root, updated after each operation, makes it $O(1)$.
- **Extract-min.** $O(\log n)$ for MINIMUM and $O(\log n)$ for the union with at most $\lfloor \lg n \rfloor$ children.
- **Decrease-key and delete.** The loop of line L29 goes up at most the height, $\lfloor \lg n \rfloor$ steps, so $O(\log n)$.
- **Insert.** One insert makes $L$ links, where $L$ is the number of trailing 1 bits of $n$, so it costs $\Theta(\log n)$ when $n = 2^k - 1$. With the [potential](/potential-method/) $\Phi(H) = $ the number of trees, an insert that makes $L$ links has actual cost $L + 1$ and changes $\Phi$ by $1 - L$, so its amortized cost is 2. The other operations raise $\Phi$ by at most $\lfloor \lg n \rfloor + 1$, so they stay $O(\log n)$ amortized. This is the analysis of the [binary counter](/binary-counter-increment/). $n$ inserts into an empty heap take $O(n)$ time.

| operation | worst case | amortized |
|---|---|---|
| make-heap | $O(1)$ | $O(1)$ |
| insert | $O(\log n)$ | $O(1)$ |
| minimum | $O(\log n)$, $O(1)$ with a min pointer | |
| extract-min | $O(\log n)$ | $O(\log n)$ |
| union | $O(\log n)$ | $O(\log n)$ |
| decrease-key | $O(\log n)$ | $O(\log n)$ |
| delete | $O(\log n)$ | $O(\log n)$ |
| space | $O(n)$ | |

In the comparison model, insert plus extract-min costs $\Omega(\log n)$ (see the [heap](/heap/) page), so the bounds of insert and extract-min cannot both be lowered.

## Variants

- **Min pointer.** Keep a pointer to the minimum root. MINIMUM becomes $O(1)$, and each operation that changes the roots updates the pointer in $O(\log n)$.
- **Lazy binomial heap.** Insert and union only put the trees in the root list, and extract-min links trees of equal degree, as CONSOLIDATE of the [Fibonacci heap](/fibonacci-heap/) does. Insert and union become $O(1)$ worst case, and extract-min becomes $O(\log n)$ amortized.
- **[Fibonacci heap](/fibonacci-heap/).** The lazy version plus cuts for $O(1)$ amortized decrease-key.
- **Skew binomial heap.** Brodal and Okasaki (1996) used skew binary numbers, in which an increment makes at most one link, to get $O(1)$ worst-case insert in a purely functional setting.
- **Max-heap.** Reverse each comparison.

## When to use it

Use a binomial heap when heaps must meld fast and the worst-case bound matters, for example in a [k-way merge](/k-way-merge/) that also melds queues, in scheduling with queues that join, or in a functional language, where its trees share well. When melds are rare, a [binary heap](/binary-heap/) is simpler and faster. When melds are common and amortized bounds are enough, a [pairing heap](/pairing-heap/) or a [skew heap](/skew-heap/) has less code. When decrease-key dominates, use a [Fibonacci heap](/fibonacci-heap/).

## Pitfalls

- **Linking trees of different degrees.** LINK must join two roots of the same degree; else the result is not a binomial tree, and the bound on the number of trees fails.
- **Three trees of one degree.** During a union, each degree can see a tree from each heap and a carry. A two-pointer merge that looks only at the next tree can leave two trees of the same degree. The table of lines L4 to L11 handles this case, and so do the four cases of the merge in CLRS.
- **Handles that move.** DECREASE-KEY exchanges the items of a node and its parent. If the handle of an item is its node, the handle points to the wrong item after the exchange. Keep a separate handle object and update it at line L30.
- **The wrong order of children.** The children of a root must be given to UNION-ROOTS as a heap with distinct degrees. When the children are kept from the largest degree, as in CLRS, they must be reversed first if the code expects increasing degrees.
- **A forgotten parent reset.** The children of an extracted root become roots, so their parent pointers must be set to nil (line L24); else a later DECREASE-KEY climbs into a removed node.

## Implementations

The Python class `BinomialHeap` follows the main block. It keeps `roots` in decreasing order of degree, so the root of least degree is the last element of the list and INSERT works at the end. The table of UNION-ROOTS is a dictionary. `insert` returns an `Entry`, the handle for `decrease_key` and `delete`, and each node points to its entry and each entry to its node, so line L30 updates both. `delete` moves the item to the root without key comparisons, which is the decrease to $-\infty$ of line L32, so the keys need only the operation "<".

## History

Jean Vuillemin introduced the binomial queue in 1978 in the Communications of the ACM, and Mark Brown analysed and implemented it in the same year in the SIAM Journal on Computing. Fredman and Tarjan built the [Fibonacci heap](/fibonacci-heap/) on it in 1984. The second edition of CLRS has a chapter on binomial heaps, Chapter 19; the third edition moved them to a problem and gave the chapter to Fibonacci heaps.

## References
