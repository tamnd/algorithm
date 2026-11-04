---
title: Top-down insertion and deletion keep the 2-3-4 tree valid
proves: [correctness]
status: full
---

A tree is *valid* when (B1) each node has 1, 2 or 3 sorted keys, (B2) an internal node with $j$ keys has $j + 1$ children, (B3) the keys are in search-tree order, so all keys of child $c_i$ lie strictly between the keys $x_{i-1}$ and $x_i$ of the node (with $x_{-1} = -\infty$ and the last bound $+\infty$), and (B4) all leaves are at the same depth. During a deletion we allow two exceptions for a moment: the root may hold no key and have one child (after a merge at the root), and a key may have two copies, as explained in Lemma 5. We write $K(t)$ for the set of keys of the subtree $t$.

**Lemma 1 (SPLIT-CHILD).** Let $t$ be a node with at most 2 keys whose child $c = c_i$ has the 3 keys $a < b < d$. Lines L10 and L11 give a valid tree with the same keys, the same depth of every leaf, and $t$ with one key more.

*Proof.* The new left node gets $a$ and the two left children of $c$, the new right node gets $d$ and the two right children; each is a 2-node (or a leaf with one key), so (B1) and (B2) hold for them. The key $b$ goes into $t$ at position $i$, and the two new nodes become children $i$ and $i + 1$. Then $t$ has at most 3 keys and one more child than before, so (B1) and (B2) hold. All keys of the left node are less than $b$ and greater than $x_{i-1}$, and all keys of the right node are greater than $b$ and less than $x_i$, so (B3) holds. Both new nodes are at the depth of $c$, and the children of $c$ keep their depths, so (B4) holds. $\square$

**Lemma 2 (MERGE).** Let $t$ have at least 2 keys, or be the root, and let $c_i$ and $c_{i+1}$ be 2-nodes. Line L26 gives a valid tree with the same keys and leaf depths, in which $c_i$ is a 4-node and $t$ has one key less. If $t$ was the root with one key, it now has no key and the single child $c_i$.

*Proof.* The node $c_i$ gets the keys $a$, $x_i$, $d$ with $a < x_i < d$ by (B3), and the four children of the two nodes in order. (B1) to (B3) hold for it, and the leaf depths do not change. The node $t$ loses one key and one child. $\square$

**Lemma 3 (FILL).** Let $t$ have at least 2 keys, or be the root, and let $c_i$ be a 2-node. Lines L23 to L25 give a valid tree with the same keys and leaf depths, in which the child that holds the old key of $c_i$ and covers the same key range has at least 2 keys, and the returned index points to it.

*Proof.* At line L23 the left sibling $s = c_{i-1}$ has at least 2 keys. Its last key $y$ goes up into position $i - 1$ of $t$, the old $x_{i-1}$ goes down to the front of $c_i$, and the last child of $s$ becomes the first child of $c_i$. The keys of that child lie between $y$ and $x_{i-1}$, which are now the bounds of the first child slot of $c_i$, so (B3) holds; the child keeps its depth. $s$ keeps at least 1 key and $c_i$ now has 2. Line L24 is the mirror image. At line L25 both siblings that exist are 2-nodes, and Lemma 2 merges $c_i$ with one of them into a 4-node, whose index is returned. In each case the keys that $c_i$ covered are covered by the returned child. $\square$

**Lemma 4 (INSERT).** If the tree is valid and $k \notin K$, INSERT gives a valid tree with keys $K \cup \{k\}$. If $k \in K$, it gives a valid tree with keys $K$.

*Proof.* If the root is nil, line L1 makes a leaf with one key. If the root is a 4-node, line L2 puts an empty root above it and splits it by Lemma 1; all leaves move down by one level together, so (B4) holds and the new root has one key.

*Invariant.* At each test of line L5, the tree is valid, its keys are $K$, $t$ is not a 4-node, and if $k$ is in the tree or is to be placed, its place is in the subtree of $t$: all keys of $t$'s subtree range contain $k$ by (B3).

It holds at the first test, since the root is not a 4-node after line L2. If $k$ is a key of $t$, line L6 returns. If $t$ is a leaf, it has at most 2 keys, and line L7 inserts $k$ at the position that keeps it sorted; $t$ gets at most 3 keys, and (B3) holds because $k$ lies in the range of $t$. Else let $c_i$ be the child whose range contains $k$. If it is a 4-node, line L8 splits it by Lemma 1, which is allowed because $t$ is not a 4-node; the middle key goes into $t$ at position $i$. If it equals $k$, the line returns; else $k$ lies in the range of one of the two new children, and $i$ points to it. That child is a 2-node. If $c_i$ was not a 4-node, it is not one now. Line L9 steps down, and the invariant holds at the next test. Each step goes one level down, so the loop stops at a leaf. $\square$

**Lemma 5 (DELETE).** If the tree is valid, DELETE gives a valid tree with keys $K \setminus \{k\}$ for the key $k$ given.

*Proof.* Write $k_0$ for the key given. During the loop, $k$ is either $k_0$ or a replacement key, as explained below.

*Invariant.* At each test of line L14: (D1) the tree satisfies (B1) to (B4), except that the root may have no key and one child, and that in (B3) the two copies of $k$ of (D3) count as equal bounds; (D2) $t$ is the root or has at least 2 keys; (D3) either $k = k_0$ and the keys of the tree are $K$, or $k \ne k_0$, an ancestor of $t$ holds $k$ in the place of $k_0$, and a second copy of $k$ is the largest (or the smallest) key of the subtree of $t$, in a leaf of it, so the keys are $(K \setminus \{k_0\})$ with $k$ counted twice; (D4) the range of $t$ contains $k$.

It holds at the first test with $t$ the root. If $t$ is a leaf, line L15 removes $k$ if it is there. By (D2), $t$ keeps at least 1 key unless it is the root, which may become empty only when it held the last key of the tree. In the first case of (D3) the keys are now $K \setminus \{k_0\}$, or $K$ when $k_0$ was absent. In the second case the duplicate copy of $k$ is gone, and the keys are $K \setminus \{k_0\}$.

If $t$ is internal and holds $k$ at position $i$ (line L16), there are three cases. At line L17, $c_i$ has at least 2 keys. The largest key $p$ of its subtree is the predecessor of $k$; writing $p$ over $k$ keeps (B3) in the sense of (D1), because $p$ is greater than all other keys of $c_i$'s subtree and less than the keys to the right. Now $k \leftarrow p$ and $t \leftarrow c_i$, which has at least 2 keys and whose range contains $p$, so (D2) to (D4) hold. From here on, $p$ is the largest key of the subtree of $t$, so it is not a key of an internal node on the path, and the path follows the last child at each level. There, line L20 can only borrow from the left sibling, which moves a key of that sibling up, or merge with the left sibling, which moves a key of $t$ down; neither moves $p$. So $p$ stays in the last leaf, line L16 does not find it again, and (D3) holds at each step. Line L18 is the mirror image, with the successor, the smallest key, and the first child at each level. At line L19 both children are 2-nodes, and $t$ has at least 2 keys or is the root, so Lemma 2 applies: $k$ moves down into the merged 4-node, and $t$ becomes that node.

If $t$ is internal and does not hold $k$, the child $c_i$ whose range contains $k$ is reached. If it is a 2-node, line L20 makes the child that covers $k$ hold at least 2 keys, by Lemma 3, which applies by (D2). Line L21 steps down, and (D2) and (D4) hold.

Each step goes one level down, so the loop reaches a leaf. Line L22 removes an empty root and makes its only child the root; all leaves move up by one level together, so (B4) holds and (D1) gives a valid tree. If the tree held only $k_0$, the root was a leaf and becomes nil. $\square$

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions the tree is a valid 2-3-4 tree that holds exactly the keys inserted and not deleted since. CONTAINS returns true exactly for these keys.

*Proof.* The empty tree is valid. Lemmas 4 and 5 keep it valid and give the stated key sets. CONTAINS follows (B3): at each node, the key can lie only in the child whose range contains it, and it stops at a leaf after at most $h$ steps. $\blacksquare$
