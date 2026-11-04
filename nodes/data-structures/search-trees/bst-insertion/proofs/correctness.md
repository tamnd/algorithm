---
title: BST insertion keeps the BST property and adds exactly the new key
proves: [correctness, termination]
status: full
---

Let $T$ be a binary search tree with the strict [binary search tree property](/binary-search-tree-property/), correct parent pointers, $n$ nodes and key set $S$. Let $k$ be a key and $v$ a value. For a node $u$ write $\mathrm{sub}(u)$ for the nodes of its subtree.

**Claim.** TREE-INSERT$(T, k, v)$ stops after at most $h + 1$ runs of the loop, where $h$ is the height of $T$. Afterwards: (a) if $k \in S$, the tree has the same nodes and links, and the node with key $k$ has value $v$; (b) if $k \notin S$, the tree has the nodes of $T$ plus one new leaf $z$ with key $k$ and value $v$, it has the BST property, its parent pointers are correct, and $T.n = n + 1$. No other value changes.

**Step 1: the loop is the search.** Lines L2 to L6 make the same moves as [BST search](/bst-search/) for $k$: at each node they stop on equality and else go to the left child if $k < x.key$ and to the right child if $k > x.key$. Line L3 only copies $x$ to $y$ before the move. By the correctness of BST search, if $k \in S$ the loop reaches the node with key $k$, and line L6 sets its value and returns; no link changes, which proves (a). The depth of $x$ grows by 1 in each run, so the loop runs at most $h + 1$ times.

**Step 2: the end of the path.** Now let $k \notin S$. Let $u_0, u_1, \ldots, u_m$ be the nodes that $x$ takes in the loop, with $u_0 = T.root$ ($m = -1$ when $T$ is empty). The loop ends when $x = $ NIL, so $y = u_m$, and the move out of $u_m$ was to the left child if $k < u_m.key$ and to the right child else, and that child is NIL. For each $i < m$, $u_{i+1}$ is the left child of $u_i$ if $k < u_i.key$ and the right child if $k > u_i.key$.

**Step 3: the new leaf.** If $T$ is empty, line L8 makes $z$ the root, with no parent, and a tree with one node has the BST property. Else lines L9 and L10 make $z$ the child of $y = u_m$ on the side given by the comparison of $k$ with $u_m.key$, which is the NIL child of Step 2, so no subtree is lost. Line L7 sets $z.p = y$.

**Step 4: the BST property.** Take a node $u$ of the new tree and a node $w$ in its left subtree; we show $w.key < u.key$ (the right side is the mirror image).

- If $u = z$, then $u$ has no subtrees, so there is no $w$.
- If $w \ne z$ and $u \ne z$, then $w$ was in the left subtree of $u$ in $T$, because the insert adds a leaf and changes no other link. So $w.key < u.key$ by the property of $T$.
- If $w = z$, then $u$ is an ancestor of $z$, so $u = u_i$ for some $i \le m$, and $z$ is in the left subtree of $u_i$ exactly when the path went left at $u_i$, that is when $k < u_i.key$. So $w.key = k < u.key$.

**Step 5: links and count.** The only new links are $y \to z$ (or the root field) and $z.p = y$, and they agree. $z$ has no children. Line L11 adds 1 to $T.n$. The keys of the new tree are $S \cup \{k\}$, and each old node keeps its key and value. This proves (b). $\blacksquare$

**Corollary (sequence of inserts).** By induction on the number of inserts, a tree built from the empty tree by TREE-INSERT has the BST property, and its in-order sequence is the sorted list of the distinct keys inserted, each with the value of its last insert.
