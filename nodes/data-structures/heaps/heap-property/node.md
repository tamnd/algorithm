---
tag: 8EXHCW
kind: definition
slug: heap-property
name: Heap property
aliases:
- heap order
- min-heap property
- max-heap property
area: data-structures/heaps
level: intro
summary: Each node's key is no smaller (min-heap) or no larger (max-heap) than its children's keys.
prereqs: [rooted-tree, total-order]
see_also: [heap, binary-heap, priority-queue, binary-search-tree-property, sift-up, sift-down, cartesian-tree, treap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.1 (Heaps), the max-heap property and the min-heap property
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.2.3 (Sorting by selection), the definition of a heap before Algorithm H
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (Priority queues), the definition of a heap-ordered binary tree
---

The heap property is an order condition on the keys of a [rooted tree](/rooted-tree/): in a min-heap, the key of each node is at most the keys of its children, and in a max-heap it is at least those keys. It is a local rule, one comparison for each edge, but it implies a global fact: the root holds a smallest key (or a largest key) of the whole tree. Each [heap](/heap/) and each heap-based [priority queue](/priority-queue/) keeps this property, and the operations [sift-up](/sift-up/) and [sift-down](/sift-down/) restore it after a change.

## Definition

Let $T$ be a finite rooted tree with node set $V$, and let $\mathrm{key} : V \to K$ map each node to an element of a set $K$ with a [total order](/total-order/) $\le$. For a node $v$ other than the root, $p(v)$ is its parent.

**Min-heap property.** $T$ is *min-heap-ordered* if

$$\forall v \in V \setminus \{\mathrm{root}(T)\} : \quad \mathrm{key}(p(v)) \le \mathrm{key}(v).$$

**Max-heap property.** $T$ is *max-heap-ordered* if $\mathrm{key}(p(v)) \ge \mathrm{key}(v)$ for each non-root node $v$.

The two are mirror images: $T$ is max-heap-ordered under $\le$ exactly when it is min-heap-ordered under the reverse order $\ge$. So each fact below is stated for min-heaps only.

**Global form.** For each pair of nodes $u, v$ such that $u$ is an [ancestor](/rooted-tree/) of $v$, $\mathrm{key}(u) \le \mathrm{key}(v)$.

**Equivalence.** The local form (each edge) and the global form (each ancestor and descendant pair) are equivalent.

*Proof.* The global form implies the local form, because a parent is an ancestor. For the other direction, let $u$ be an ancestor of $v$ at distance $d \ge 1$, and let $u = w_0, w_1, \ldots, w_d = v$ be the path from $u$ down to $v$, so $w_{i-1} = p(w_i)$. The local form gives $\mathrm{key}(w_{i-1}) \le \mathrm{key}(w_i)$ for $i = 1, \ldots, d$, and the transitive law of $\le$ gives $\mathrm{key}(u) \le \mathrm{key}(v)$. $\square$

**Consequence: the root is a minimum.** Each node is the root or a descendant of the root, so $\mathrm{key}(\mathrm{root}(T)) \le \mathrm{key}(v)$ for each $v \in V$. More generally, the root of each subtree holds a minimum of that subtree, and each subtree of a heap-ordered tree is heap-ordered.

**Weak form for an array.** For an array $A[1 \ldots n]$ that stores a [complete binary tree](/complete-binary-tree/) in level order, the parent of index $i \ge 2$ is $\lfloor i/2 \rfloor$, and the min-heap property reads

$$\forall i \in \{2, \ldots, n\} : \quad A[\lfloor i/2 \rfloor] \le A[i].$$

This is the form that [binary heaps](/binary-heap/) use. It has exactly $n - 1$ conditions, one for each edge.

**Keys that are equal.** The definition uses $\le$, not $<$, so equal keys may sit on one path. The minimum at the root is then a minimum, not the unique minimum.

**A violation.** An edge $(p(v), v)$ with $\mathrm{key}(p(v)) > \mathrm{key}(v)$ is a *violation*. A tree with violations is not heap-ordered. Several heaps allow a bounded set of violations on purpose and repair them later: the [Brodal queue](/brodal-queue/), and the [relaxed heap](/relaxed-heap/) use this idea.

## Examples and non-examples

- **A min-heap array.** $A = [1, 3, 2, 7, 4, 5]$. The edges are $(1,2), (1,3), (2,4), (2,5), (3,6)$ by index, and the conditions $1 \le 3$, $1 \le 2$, $3 \le 7$, $3 \le 4$, $2 \le 5$ all hold. The root holds the minimum 1.
- **A max-heap array.** $A = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1]$, the array that CLRS builds in Section 6.3. Each of the 9 conditions $A[\lfloor i/2 \rfloor] \ge A[i]$ holds, for example $A[4] = 8 \ge A[8] = 2$ and $A[4] = 8 \ge A[9] = 4$.
- **A sorted array.** Each array in non-decreasing order is a min-heap, because $\lfloor i/2 \rfloor < i$ gives $A[\lfloor i/2 \rfloor] \le A[i]$. The converse is false: $[1, 3, 2]$ is a min-heap but is not sorted.
- **All keys equal.** $[5, 5, 5, 5]$ is both a min-heap and a max-heap.
- **Non-example, one bad edge.** $[1, 3, 2, 7, 0]$ is not a min-heap: the edge from index 2 to index 5 has $3 > 0$. Every other edge is fine, which shows that one edge suffices to break the property. Here the root 1 is not the minimum.
- **Siblings are not ordered.** The rule says nothing about two children of one node. $[1, 3, 2]$ and $[1, 2, 3]$ are both min-heaps. So a heap is far from sorted: of $n$ distinct keys, the heap property fixes only the position of the minimum.
- **Non-example, a binary search tree.** The tree with root 2, left child 1 and right child 3 has the [binary search tree property](/binary-search-tree-property/) but not the heap property, because $2 > 1$ on the left edge.
- **A tree that is not binary.** A root 0 with children 4, 1 and 9, where the node 1 has the children 1 and 6, is min-heap-ordered. The heap property does not need a binary tree or a shape rule.

**How many heaps.** For $n$ distinct keys and a fixed tree shape, the number of ways to place the keys so that the tree is heap-ordered is

$$\frac{n!}{\prod_{v \in V} s(v)},$$

where $s(v)$ is the number of nodes of the subtree of $v$. *Proof* by induction on $n$. For $n = 1$ there is one placement. For $n > 1$, the root must get the smallest key. Let the root have the subtrees $T_1, \ldots, T_k$ with $n_1, \ldots, n_k$ nodes, so $n_1 + \cdots + n_k = n - 1$. A placement is heap-ordered exactly when the root gets the smallest key and each $T_j$ is heap-ordered. There are $(n-1)!/(n_1! \cdots n_k!)$ ways to split the other $n - 1$ keys into sets of sizes $n_1, \ldots, n_k$, and by the induction hypothesis $T_j$ has $n_j!/\prod_{v \in T_j} s(v)$ heap-ordered placements of its set. The product is $(n-1)!/\prod_{v \ne \mathrm{root}} s(v) = n!/\prod_{v} s(v)$, because $s(\mathrm{root}) = n$. $\square$

For the binary heap shape with $n = 10$, the subtree sizes are $10, 6, 3, 3, 2, 1, 1, 1, 1, 1$, so there are $10!/1080 = 3360$ min-heaps on the keys $1$ to $10$, out of $3628800$ arrays.

## Related definitions

- A [heap](/heap/) is a data structure: a heap-ordered tree or forest, together with a shape rule and the operations of a [priority queue](/priority-queue/).
- A [binary heap](/binary-heap/) is a [complete binary tree](/complete-binary-tree/) in an array with the heap property.
- The [binary search tree property](/binary-search-tree-property/) orders the left subtree, the node and the right subtree. It sorts the keys in in-order. The heap property sorts each root-to-leaf path.
- A [Cartesian tree](/cartesian-tree/) and a [treap](/treap/) have both properties at the same time: the search tree property on one key and the heap property on a second key.
- A [min-max heap](/min-max-heap/) alternates the min rule and the max rule level by level, to give both the minimum and the maximum.
- A [tournament tree](/tournament-tree/) holds the keys at the leaves, and each internal node holds the smaller key of its two children. It satisfies the min-heap property with copies of keys.

## References
