---
title: Successor and insert are correct in a threaded binary search tree
proves: [correctness]
status: full
---

We use the invariant of the page: (H1) the child links form a binary search tree with distinct keys, and (H2) each left thread points to the in-order predecessor and each right thread to the in-order successor (NIL at the two ends). Let $x_1, \ldots, x_n$ be the in-order sequence of the tree of child links, so $x_1.key < \cdots < x_n.key$ by (H1).

**Lemma 1.** A node has a left child exactly when its left tag is false, and a right child exactly when its right tag is false. This is the meaning of the tags.

**Lemma 2 (successor in a binary tree).** In a binary tree, if $x$ has a right child, the in-order successor of $x$ is the leftmost node of the right subtree of $x$. If $x$ has no right child, the successor is the lowest ancestor of $x$ whose left subtree contains $x$, or nothing.

*Proof.* In-order visits the left subtree of a node, then the node, then its right subtree. If $x$ has a right subtree $R$, the next node visited after $x$ is the first node of $R$ in in-order, which is the leftmost node of $R$. If not, the subtree of $x$ is finished when $x$ is visited, and in-order returns up the ancestors; it visits next the first ancestor $u$ reached from its left subtree. $\square$

**Claim 1.** SUCCESSOR$(x)$ returns $x_{i+1}$ for $x = x_i$, or NIL for $i = n$.

*Proof.* If $x.rthread$ is true, then $x$ has no right child (Lemma 1), and by (H2) $x.right$ is $x_{i+1}$ or NIL for $i = n$; line L1 returns it. Else $x$ has a right child $y$ (line L2). The loop of line L3 moves from $y$ to its left child while the left tag is false, that is while a left child exists (Lemma 1), so it stops at the leftmost node of the subtree of $y$, after at most $h$ steps because the depth grows by 1 in each step. By Lemma 2 this node is $x_{i+1}$. $\square$

**Corollary (walk).** Starting at $x_1$ and applying SUCCESSOR until NIL visits $x_1, \ldots, x_n$ in order. Each left child link $(u, u.left)$ lies on exactly one maximal chain of left links; let $t$ be the top node of that chain. The chain is walked down once: by the first walk to the minimum if $t$ is the root, and else by line L3 in the call for the node whose right child is $t$. Each right child link is followed once by line L2, in the call for its upper end, and each right thread once by line L1. So the walk takes $O(n)$ steps.

**Claim 2.** If the tree satisfies (H1) and (H2) and $k$ is not a key, then after INSERT$(T, k)$ the tree satisfies (H1) and (H2) and its keys are the old keys and $k$. If $k$ is a key, nothing changes.

*Proof.* If the tree is empty, line L5 makes a single node with two NIL threads, which satisfies both conditions. Else lines L6 to L12 follow the search path for $k$ in the tree of child links, because by Lemma 1 a move is made exactly when the child exists. If $k$ is found, line L8 returns without a change. Else the walk ends at a node $x$ whose field on the side of $k$ is a thread, which by Lemma 1 is an empty child position, the same position where [BST insertion](/bst-insertion/) puts $k$. The new node $z$ becomes the child of $x$ there, as a leaf, so (H1) holds by the correctness of BST insertion.

For (H2), assume $k < x.key$, so line L11 runs (the other case is the mirror image). Let $x = x_j$. Because $x$ had no left child, by Lemma 2 applied to predecessors its predecessor $x_{j-1}$ is the old target of $x.left$ (by (H2)), or none for $j = 1$. In the new tree, $z$ is a leaf and is the whole left subtree of $x$, so in-order visits $z$ right before $x$. The nodes visited before $z$ are the nodes visited before $x$ in the old tree, in the same order, because no other subtree changed. The new sequence is $x_1, \ldots, x_{j-1}, z, x_j, \ldots, x_n$.

Now check each thread. $z$ has both tags true, with $z.left$ equal to the old $x.left$, which is $x_{j-1}$ or NIL, its new predecessor, and $z.right = x = x_j$, its new successor. The node $x$ loses its left thread and gets the child $z$, with its tag set to false. Each other node keeps its fields. Its in-order neighbours did not change, except for $x_{j-1}$, whose successor is now $z$; but $x_{j-1}$ has a right child or a right thread to $x_j$. In the second case $x_{j-1}$ would have no right child, so its successor would be the lowest ancestor with $x_{j-1}$ in its left subtree, which is $x_j$, and then $x_j$ would have a left child in the old tree, which is false because the left field of $x_j$ was a thread. So $x_{j-1}$ has a right child, and its right field is not a thread. Hence every thread is correct, and (H2) holds. $\blacksquare$
