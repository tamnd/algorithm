---
tag: TNBREA
kind: concept
slug: structural-sharing
name: Structural sharing
aliases:
- sharing of unchanged parts
area: data-structures/persistent-structures
level: intro
summary: New versions reuse the unchanged parts of old versions instead of copying them.
prereqs: [persistent-data-structure, linked-list, binary-tree]
see_also: [path-copying, persistent-stack, persistent-binary-search-tree, persistent-vector, hash-consing, purely-functional-data-structure, reference-counting, tracing-garbage-collection]
sources:
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 2, Persistence (Section 2.1 on sharing in lists, and Section 2.2 on copying the search path of a binary search tree)
  - paper: doi:10.1016/0022-0000(89)90034-2
    title: James R. Driscoll, Neil Sarnak, Daniel D. Sleator and Robert E. Tarjan, Making data structures persistent, Journal of Computer and System Sciences 38(1), 1989
    locator: the discussion of path copying, and of the fat node and node-copying methods that copy fewer nodes
  - url: https://ocw.mit.edu/courses/6-851-advanced-data-structures-spring-2012/
    title: Erik Demaine, MIT 6.851 Advanced Data Structures, Spring 2012
    locator: Lecture 1, Persistent data structures (path copying and the pointer-machine model)
---

Structural sharing is the method by which a new version of a data structure reuses the unchanged parts of an old version by pointing to them, instead of copying them. The new version gets new nodes only for the parts that the update changes, and these new nodes point into the old structure. It is what makes a [persistent data structure](/persistent-data-structure/) cheap: with [path copying](/path-copying/) in a balanced tree, an update makes $O(\log n)$ new nodes, not $n$. The method is safe only when the shared parts are never changed in place.

## In plain words

Suppose you keep a family tree on cards, and you want a second copy with one name changed. You could copy every card. But almost every card would be the same, so you copy only the card with the change, and each card that pointed to it. The new top card then leads to the new cards, and through them to all the old cards that did not change.

Now the old top card and the new top card both lead to most of the same cards. Each copy is complete when you read it, and the second copy cost only a few new cards.

This only works if nobody ever writes on a shared card. If someone did, both copies would change at once.

## The idea

Model a version as a pointer to a root node of a linked structure: a list, a tree, or any graph of nodes with fields. The value of a version is everything reachable from its root.

**The rule.** To change node $x$ in version $v$, do not write to $x$. Make a new node $x'$ with the new fields. Each node that points to $x$ in $v$ must now point to $x'$ in the new version, so it is copied too, and so on up to the root. Every node that is not on these paths is reused: the new nodes point to it. In a tree each node has one parent, so the copied nodes form exactly the path from the root to $x$.

**Cost.** Let $c$ be the number of nodes that an update copies or makes. Then the update takes time and space proportional to $c$, and after $m$ updates on a structure that started with $n$ nodes the total space is $n + c_1 + \cdots + c_m$, where $c_i$ is the count of update $i$. Without sharing, keeping $m + 1$ versions of size about $n$ costs about $(m + 1) n$ space. For a tree of depth $d$, $c = d + 1$ for an update at the deepest level.

**Safety.** Sharing is correct if no shared node changes after another version can reach it. The simplest way to ensure this is to never change any node after it is made: then the structure is a [purely functional data structure](/purely-functional-data-structure/). The [fat node](/fat-node/) and [node copying](/node-copying/) methods relax the rule: they do write to old nodes, but each write is stamped with a version number, so an old version never sees it.

**Two uses of shared pointers.** If two versions hold the same pointer for a subtree, the subtrees are equal, so a comparison of the two versions can skip that subtree. And if many versions share one part, the part is freed only when no version reaches it, which needs [reference counting](/reference-counting/) or a [tracing garbage collector](/tracing-garbage-collection/).

**Maximal sharing.** Structural sharing reuses parts that a version got from its own history. [Hash-consing](/hash-consing/) goes further: it keeps a table of all nodes, and before it makes a node it looks for an equal node and returns that one. Then equal values are always the same object, even if they were built separately.

## Examples

**Lists.** Let $xs = [3, 2, 1]$, as a linked list with 3 nodes. Then $ys = 4 :: xs$ and $zs = 5 :: xs$ each make one node that points to the first node of $xs$. The three lists hold $3 + 4 + 4 = 11$ items in total, but they use only 5 nodes. This is the [persistent stack](/persistent-stack/).

**A list update that cannot share.** To change the last item of $xs$ to 9, every node of $xs$ must be copied: the new last node is new, so the node before it must point to it and is new, and so on. The update makes 3 nodes and shares nothing. In a list, an update at depth $d$ copies $d + 1$ nodes, so sharing helps most when the changes are near the front.

**A balanced tree.** A [persistent binary search tree](/persistent-binary-search-tree/) with $2^{20} - 1 = 1{,}048{,}575$ keys, kept perfectly balanced, has 20 levels. A change of one key copies at most 20 nodes. A program that keeps 1000 versions, each made from the one before by one change, adds at most $20{,}000$ nodes. Full copies would need $1000 \times 1{,}048{,}575 = 1{,}048{,}575{,}000$ nodes.

**A wide tree.** A [persistent vector](/persistent-vector/) of $10^6$ items with 32 children per node has 4 levels, because $32^4 = 1{,}048{,}576 \ge 10^6$. An update copies 4 nodes of 32 slots each, which is 128 slots, out of about a million.

**Comparison by pointer.** Two versions of a search tree that differ in one key share all nodes off the copied path. A recursive comparison that returns "equal" at once when both pointers are the same node visits only the copied path and the nodes next to it, which is $O(\log n)$ nodes in a balanced tree.

**Unsafe sharing.** Let $ys = 4 :: xs$, and then let a program set the item of the first node of $xs$ to 7 in place. Now $xs = [7, 2, 1]$, and also $ys = [4, 7, 2, 1]$, though no operation on $ys$ was done. This is the error that the safety rule prevents.

## Where it is used

- Every persistent structure built by [path copying](/path-copying/): the [persistent stack](/persistent-stack/), the [persistent binary search tree](/persistent-binary-search-tree/), the [persistent red-black tree](/persistent-red-black-tree/), the [persistent treap](/persistent-treap/), the [persistent segment tree](/persistent-segment-tree/) and the [persistent trie](/persistent-trie/).
- The collections of functional languages and libraries, such as the [persistent vector](/persistent-vector/) of Clojure and the maps and sets of Haskell, OCaml and Scala, which are balanced trees with shared subtrees.
- Version control systems that store a directory tree as a tree of objects: a new commit makes new objects only for the changed files and the directories on their paths, and points to the old objects for the rest.
- [Multiversion concurrency control](/multiversion-concurrency-control/) in databases, where readers see an old version while a writer builds a new one.
- Copy-on-write in operating systems, where a forked process shares the pages of its parent until one of them writes to a page. This is sharing at the level of pages, with the write as the signal to copy.
- The [zipper](/zipper/), which keeps the path to a cursor and shares the rest of the tree.

## References
