---
title: Insertion and deletion keep the treap invariant
proves: [correctness]
status: full
---

A *treap* is a binary tree with (P1) the search order on keys and (P2) the max-heap order on priorities: each node has a priority at least as high as those of its children. Write $K(t)$ for the set of keys of the subtree $t$. A rotation keeps the in-order sequence of the keys, so it keeps (P1) and the key set (see [tree rotation](/tree-rotation/)). For the heap order we track *bad edges*: an edge from a parent $y$ to a child $x$ with $x.pri > y.pri$.

## Insertion

**Lemma 1.** Let $t$ be a treap or nil, with $k \notin K(t)$. Then $r = \text{INSERT}(t, k, p)$ has the keys $K(t) \cup \{k\}$, satisfies (P1), and has no bad edge. Moreover, its root is either the root of $t$ or the new node of key $k$.

*Proof.* By induction on the size of $t$. If $t$ is nil, line L1 returns one node. Else let $k < t.key$ (the case $k > t.key$, with lines L4 and L5, is the mirror image). By induction, line L2 makes $t.left$ a treap $r'$ with the new key, with (P1), no bad edge, and root either the old left child $l$ of $t$ or the new node $x$. Every key of $r'$ is less than $t.key$, so the subtree of $t$ satisfies (P1). The only edge that can be bad is the edge from $t$ to the root of $r'$.

If the root of $r'$ is $l$, its priority is at most $t.pri$ by (P2) for the old $t$, so there is no bad edge, line L3 does nothing, and the root is $t$.

If the root of $r'$ is $x$ and $x.pri \le t.pri$, there is no bad edge and line L3 does nothing. If $x.pri > t.pri$, line L3 rotates right at $t$. Now $x$ is the root, $t$ is its right child, and the old right child $b$ of $x$ becomes the left child of $t$. Check every changed edge. The edge $x \to t$ is good, since $x.pri > t.pri$. The edge $t \to b$ is good: all nodes of $r'$ other than $x$ are nodes of the old $t.left$, so each has priority at most $t.pri$ by (P2) for the old tree, and $b$ is one of them. The edge $t \to t.right$ is unchanged and good, and the edge $x \to a$ to the left child of $x$ is unchanged and good. So there is no bad edge, and the root is the new node. $\square$

So INSERT on a treap gives a treap with the new key. If $k$ is already in the tree, INSERT returns at line L6 with no change at the node of key $k$ and no rotation above it, since each child it returns is the same node as before.

## Deletion

**The heap order with one hole.** Let $x$ be a node of a binary tree. Say that the tree has *(P2) except at $x$* if every edge that does not touch $x$ is good, and, when $x$ has a parent $y$, every child $c$ of $x$ has $c.pri \le y.pri$. In words: if $x$ were removed and its children hung on its parent, the tree would be a heap. Then for any two nodes $u \ne x$ and $v \ne x$ with $v$ below $u$, $v.pri \le u.pri$: the path from $u$ to $v$ uses good edges, except that it may pass through $x$, and the step from the parent of $x$ over $x$ to a child of $x$ does not increase the priority, by the definition. A treap has (P2) except at any of its nodes.

**Lemma 2.** Let $t$ have (P1) and (P2) except at $x$, where $x.key = k$. Then DELETE$(t, k)$ returns a treap with the keys $K(t) \setminus \{k\}$, whose root, if any, is a node of $t$ other than $x$.

*Proof.* By induction on the size of $t$.

*Case $x \ne t$ (lines L8 and L9).* The node $x$ is in the child $c$ on the side of $k$, by (P1). The subtree $c$ has (P2) except at $x$, so by induction DELETE$(c, k)$ returns a treap $c'$ with keys $K(c) \setminus \{k\}$, whose root $v$ is a node of $c$ other than $x$. By the remark above, $v.pri \le t.pri$, so the edge from $t$ to $v$ is good. The other child of $t$ and its edge are unchanged and good, so the subtree of $t$ is a treap. Its keys are $K(t) \setminus \{k\}$, and (P1) holds because the keys of $c'$ come from $c$.

*Case $x = t$ with at most one child (lines L10 and L11).* The result is the other child, or nil. No edge in it touches $x$, so it is a treap, and its keys are $K(t) \setminus \{k\}$.

*Case $x = t$ with two children $a = t.left$ and $b = t.right$.* Say $a.pri > b.pri$, which is line L12; line L13 is the mirror image and also covers ties. Line L12 rotates right at $t$: $a$ is the root, with the left child $a.left$ and the right child $x$, and $x$ has the left child $a.right$ (the old one) and the right child $b$. The edges that do not touch $x$ are $a \to a.left$ and the edges inside the subtrees $a.left$, $a.right$ and $b$; all are unchanged and good. The children of $x$ are $a.right$, with $a.right.pri \le a.pri$ by (P2) for the old edge $a \to a.right$, and $b$, with $b.pri < a.pri$. So the new tree has (P2) except at $x$, and so does the subtree $s$ rooted at $x$, which has fewer nodes than $t$. By induction, DELETE$(s, k)$ returns a treap $s'$ with keys $K(s) \setminus \{k\}$ whose root is a node of $s$ other than $x$, so its priority is at most $a.pri$. The new tree, with root $a$, left subtree $a.left$ and right subtree $s'$, is a treap with (P1), and its keys are $K(t) \setminus \{k\}$. Its root $a$ is a node of $t$ other than $x$. $\square$

If $k$ is not in the tree, DELETE follows the search path to nil at line L7 and changes nothing.

## Conclusion

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions the tree is a treap that holds exactly the keys inserted and not deleted since, and a search returns true exactly for these keys.

*Proof.* The empty tree is a treap. Lemma 1 and Lemma 2 (with $x$ the node of key $k$) show that each operation keeps (P1) and (P2) and changes the key set as stated. A search is correct by (P1). $\blacksquare$
