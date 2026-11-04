---
title: Insertion and deletion keep the AVL invariant
proves: [correctness, rotations.insert]
status: full
---

We write $K(t)$ for the set of keys of the subtree $t$, $h(t)$ for its height ($h(\text{nil}) = 0$), and $(L, x, R)$ for the tree with root key $x$, left subtree $L$ and right subtree $R$. A tree is *AVL* when it satisfies (A1) the search-tree order, (A2) correct stored heights and (A3) $bf \in \{-1, 0, 1\}$ at each node. Rotations keep the in-order sequence of the keys and recompute the heights of the two moved nodes from their children, lower node first (see [tree rotation](/tree-rotation/)).

**Lemma 1 (REBALANCE).** Let $t$ be a node whose subtrees $L = t.left$ and $R = t.right$ are AVL, with each key of $L$ less than $t.key$ and each key of $R$ greater, and with $|h(R) - h(L)| \le 2$. Then REBALANCE$(t)$ returns an AVL tree with the same in-order sequence of keys, and of height $1 + \max(h(L), h(R))$ when $|h(R) - h(L)| \le 1$, and of height $\max(h(L), h(R))$ or $\max(h(L), h(R)) + 1$ when $|h(R) - h(L)| = 2$.

*Proof.* Line L6 sets $t.h$ correctly. If $|bf(t)| \le 1$, line L13 returns $t$, which is AVL with the stated height.

Let $bf(t) = 2$, and write $p = h(L)$, so $h(R) = p + 2 \ge 2$ and $R$ is not nil. Let $a$ and $b$ be the left and right subtrees of $r = R$. Since $R$ is AVL, $\max(h(a), h(b)) = p + 1$ and $|h(a) - h(b)| \le 1$.

*Case $bf(r) \ge 0$.* Then $h(b) = p + 1$ and $h(a) \in \{p, p + 1\}$. Line L8 does nothing and line L9 rotates left at $t$. The result is $((L, t, a), r, b)$. The node $t$ has subtrees of heights $p$ and $h(a)$, so its balance factor is $h(a) - p \in \{0, 1\}$ and its height is $h(a) + 1 \in \{p + 1, p + 2\}$. The node $r$ has subtrees of heights $h(a) + 1$ and $p + 1$, so its balance factor is $p - h(a) \in \{-1, 0\}$ and its height is $h(a) + 2$, which is $p + 2$ or $p + 3$. Here $\max(h(L), h(R)) = p + 2$.

*Case $bf(r) = -1$.* Then $h(a) = p + 1$ and $h(b) = p$. So $a$ is a node, with subtrees $c$ and $d$ such that $\max(h(c), h(d)) = p$ and $h(c), h(d) \in \{p - 1, p\}$. Line L8 rotates right at $r$ and line L9 rotates left at $t$. The result is $((L, t, c), a, (d, r, b))$. The node $t$ has subtrees of heights $p$ and $h(c)$: its balance factor is $h(c) - p \in \{-1, 0\}$, and its height is $p + 1$. The node $r$ has subtrees of heights $h(d)$ and $p$: its balance factor is $p - h(d) \in \{0, 1\}$, and its height is $p + 1$. The root $a$ has two subtrees of height $p + 1$, balance factor 0 and height $p + 2 = \max(h(L), h(R))$.

In both cases the subtrees $L$, $a$, $b$, $c$, $d$ are unchanged AVL trees, the three rebuilt nodes satisfy (A3), and their heights are recomputed from children whose heights are already right, so (A2) holds. Rotations keep the in-order sequence, so (A1) holds and the keys are the same. The case $bf(t) = -2$ is the mirror image, with lines L11 and L12. $\square$

**Lemma 2 (INSERT).** If $t$ is AVL, then INSERT$(t, k)$ returns an AVL tree $t'$ with $K(t') = K(t) \cup \{k\}$ and $h(t') \in \{h(t), h(t) + 1\}$. Moreover, if $t$ is not nil and $h(t') = h(t) + 1$, then the root of $t'$ has a nonzero balance factor, and no rotation was done at the root of $t'$.

*Proof.* By induction on $h(t)$. If $t = \text{nil}$, line L1 returns a single node, which is AVL, with height $1 = h(t) + 1$. If $k = t.key$, line L4 returns $t$ unchanged.

Let $k < t.key$ (the case $k > t.key$ is the mirror image). Write $p = h(L)$ and $q = h(R)$ for the old subtrees, so $|p - q| \le 1$ and $h(t) = 1 + \max(p, q)$. By the induction hypothesis, line L2 makes $t.left = L'$, an AVL tree with keys $K(L) \cup \{k\}$, all less than $t.key$, and $h(L') \in \{p, p + 1\}$. So $|h(L') - q| \le 2$, and Lemma 1 applies to line L5. The keys are $K(t) \cup \{k\}$.

*No rotation at $t$.* Then $|h(L') - q| \le 1$, and $h(t') = 1 + \max(h(L'), q)$, which is $h(t)$ or $h(t) + 1$. It is $h(t) + 1$ only if $h(L') = p + 1$ and $p \ge q$. Then $bf(t') = q - (p + 1) \le -1$, which is nonzero.

*A rotation at $t$.* Then $h(L') = q + 2$. Since $p \le q + 1$, this forces $h(L') = p + 1$ and $p = q + 1$, so $h(t) = p + 1$. The tree $L$ is not nil, because $p = q + 1 \ge 1$, and $L'$ grew, so by the induction hypothesis $bf(L') \ne 0$. In the proof of Lemma 1 (mirrored), the only case with height $\max(h(L'), q) + 1$ is the one with $bf(L') = 0$. So $h(t') = \max(h(L'), q) = p + 1 = h(t)$: the height did not grow. $\square$

**Corollary (one rebalancing per insertion).** An insertion does rotations at one node at most, one single rotation or one double rotation. *Proof.* Let $t$ be the lowest node of the path where REBALANCE rotates. By Lemma 2, the subtree of $t$ has the same height after the insertion as before. So each ancestor of $t$ has children of the same heights as before, its balance factor is the old one, which is in $\{-1, 0, 1\}$, and REBALANCE does not rotate there. $\square$

**Lemma 3 (DELETE).** If $t$ is AVL, then DELETE$(t, k)$ returns an AVL tree $t'$ with $K(t') = K(t) \setminus \{k\}$ and $h(t') \in \{h(t) - 1, h(t)\}$ (with $h(t') = 0$ when $t$ is nil).

*Proof.* By induction on $h(t)$. If $t = \text{nil}$, line L14 returns nil. Write $L$, $R$, $p = h(L)$, $q = h(R)$ as before.

*Case $k < t.key$* (the case $k > t.key$ is the mirror image). By the induction hypothesis, line L15 makes $t.left = L'$, AVL, with keys $K(L) \setminus \{k\}$ and $h(L') \in \{p - 1, p\}$. So $|h(L') - q| \le 2$ and Lemma 1 applies at line L22. The keys are $K(t) \setminus \{k\}$. By Lemma 1, $h(t') \le \max(h(L'), q) + 1 \le h(t)$. If REBALANCE does not rotate, $h(t') = 1 + \max(h(L'), q) \ge 1 + \max(p - 1, q) \ge \max(p, q) = h(t) - 1$. If it rotates, then $q = h(L') + 2$, so $q \ge p + 1$, hence $q = p + 1$ and $h(t) = q + 1$; and $h(t') \ge \max(h(L'), q) = q = h(t) - 1$.

*Case $k = t.key$ and $t.left = \text{nil}$.* Line L18 returns $R$, an AVL tree. Since $bf(t) \in \{0, 1\}$ and $p = 0$, $h(R) = q = h(t) - 1$. Its keys are $K(t) \setminus \{k\}$, since the keys are distinct. The case $t.right = \text{nil}$ (line L19) is the mirror image.

*Case $k = t.key$ with two children.* Line L20 finds the node $m$ of least key in $R$. Line L21 sets $t.key = m.key$ and, by the induction hypothesis applied to $R$, makes $t.right = R'$, AVL, with keys $K(R) \setminus \{m.key\}$ and $h(R') \in \{q - 1, q\}$. Each key of $L$ is less than $k$, which is less than $m.key$, and each key of $R'$ is greater than $m.key$, because $m.key$ was the least key of $R$ and the keys are distinct. So the hypotheses of Lemma 1 hold, and the height bound follows as in the first case. The keys are $K(L) \cup \{m.key\} \cup (K(R) \setminus \{m.key\}) = K(t) \setminus \{k\}$. $\square$

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions the tree is AVL and holds exactly the keys inserted and not deleted since. CONTAINS$(k)$ returns true exactly when $k$ is in the tree. Each insertion does at most one single or one double rotation.

*Proof.* The empty tree is AVL. Lemmas 2 and 3, applied to the root, keep the tree AVL and give the stated key sets. CONTAINS is the search of a binary search tree, which is correct by (A1): at each node, a key less than the node's key can only be in the left subtree and a greater key only in the right subtree. Each recursive call works on a child, whose height is one less, so each operation stops after at most $h(t) + 1$ calls. The bound on rotations is the corollary. $\blacksquare$
