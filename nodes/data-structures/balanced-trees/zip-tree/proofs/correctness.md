---
title: Zip and unzip keep the zip-tree order
proves: [correctness]
status: full
---

Say that a node $u$ *beats* a node $v$ when $u.rank > v.rank$, or $u.rank = v.rank$ and $u.key < v.key$. Keys are distinct, so this is a strict total order on the nodes. A tree is a *zip tree* when:

1. (Z1) it is a binary search tree on its keys;
2. (Z2) every node beats its children.

For a left child $c$ of $u$, $c.key < u.key$, so (Z2) asks $c.rank < u.rank$; for a right child, $c.rank \le u.rank$. This is the rank rule checked in the code. By (Z2) and transitivity, every node beats all of its proper descendants. So a zip tree is a treap whose priority is the pair $(rank, -key)$, and for a given set of keys and ranks there is exactly one zip tree: the root must be the node that beats all others, and the two subtrees are the zip trees of the smaller and of the larger keys.

**Lemma 1 (UNZIP).** Let $t$ be a zip tree and $k$ a key not in $t$. UNZIP$(t, k)$ returns zip trees $P$ and $Q$ whose nodes are those of $t$, with the keys less than $k$ in $P$ and the greater keys in $Q$.

*Proof.* Let $t_1, t_2, \ldots, t_m$ be the nodes visited by the loop of line L6; they form the search path of $k$ in $t$, from the root down. A node $t_j$ with $t_j.key < k$ goes to $P$, and all of its left subtree has keys less than $t_j.key < k$, so the whole left subtree goes along unchanged. A node with $t_j.key > k$ goes to $Q$ with its right subtree. Every node of $t$ is on the path or in such a subtree, because the path leaves each visited node through the other side. So the keys are divided as claimed.

Consider the nodes $p_1, p_2, \ldots$ of the path that go to $P$, in the order visited. The loop makes $p_{j+1}$ the right child of $p_j$ (line L6), and line L7 ends the spine with nil. In $t$, after visiting $p_j$ the path goes right, so $p_{j+1}$ lies in the right subtree of $p_j$: its key is larger, and $p_j$ beats it. So the new link keeps (Z1) and (Z2). All of the right subtree of $p_j$ in $P$ consists of nodes from its old right subtree with keys less than $k$, so (Z1) holds at $p_j$. The left subtrees are unchanged. So $P$ is a zip tree with root $p_1$, and $Q$ is a zip tree by the mirror argument. $\square$

**Lemma 2 (ZIP).** Let $a$ and $b$ be zip trees with every key of $a$ less than every key of $b$. ZIP$(a, b)$ returns a zip tree on the nodes of $a$ and $b$.

*Proof.* Lines L9 and L10 are the loop form of the recursion

$$\text{ZIP}(a, b) = \begin{cases} b & \text{if } a = \text{nil},\\ a & \text{if } b = \text{nil},\\ a \text{ with } a.right \leftarrow \text{ZIP}(a.right, b) & \text{if } a.rank \ge b.rank,\\ b \text{ with } b.left \leftarrow \text{ZIP}(a, b.left) & \text{otherwise}: \end{cases}$$

each pass of the loop hangs the root of one call at the place where the previous call puts its result. Since $a.key < b.key$, the test $a.rank \ge b.rank$ says exactly that $a$ beats $b$. We prove the recursion by induction on the number of nodes. In the third case, the root $a$ keeps its left subtree. By induction, $\text{ZIP}(a.right, b)$ is a zip tree on the nodes of $a.right$ and $b$, all with keys greater than $a.key$, so (Z1) holds at $a$. Its root is $a.right$ or $b$; $a$ beats $a.right$ by (Z2), and $a$ beats $b$, so (Z2) holds at $a$. The fourth case is the mirror image, with $b$ beating $a$. $\square$

**Insertion.** Line L1 returns if $k$ is present; otherwise $x$ is a new node with key $k$. Line L2 walks down the search path of $k$ while the current node beats $x$; let $cur$ be the node where it stops (possibly nil) and $parent$ the node before it. Every node above $cur$ on the path beats $x$. If $cur$ is a node, it does not beat $x$, so $x$ beats $cur$, and by transitivity $x$ beats every node of the subtree of $cur$. By Lemma 1, line L3 makes the left subtree of $x$ a zip tree on the keys of that subtree less than $k$, and the right subtree a zip tree on the greater keys; so (Z1) and (Z2) hold at $x$. Line L4 puts $x$ in the place of $cur$. The subtree of $cur$ held exactly the keys of the tree in the interval of that place, and $k$ is in this interval, since the search path of $k$ passes there; so (Z1) holds at $parent$ and above. $parent$ beats $x$, so (Z2) holds there. Nothing else changes.

**Deletion.** Line L8 finds the node $x$ with key $k$, or returns. By Lemma 2, ZIP of its two subtrees is a zip tree on all the nodes below $x$, with the same set of keys apart from $k$. It takes the place of $x$; its keys lie in the interval of that place, and the parent of $x$ beats all of them, because they were descendants. So (Z1) and (Z2) hold.

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions the tree is a zip tree on exactly the keys inserted and not deleted, and a search returns true exactly for these keys. Its shape depends only on the keys and their ranks, not on the order of the operations.

*Proof.* The empty tree is a zip tree. The two cases above keep (Z1) and (Z2) and change the key set as stated. The search is correct by (Z1). The shape is the unique zip tree for the keys and ranks, as shown at the start. $\blacksquare$
