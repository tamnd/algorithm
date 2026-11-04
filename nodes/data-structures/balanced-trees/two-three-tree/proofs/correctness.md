---
title: Insertion and deletion keep the 2-3 tree invariant
proves: [correctness]
status: full
---

Write $K(t)$ for the set of keys in the subtree $t$ and $d(t)$ for the number of nodes on a path from $t$ down to a leaf. A subtree is *valid* when it satisfies (T1) each node has one or two keys in increasing order, (T2) an internal node with $j$ keys has $j + 1$ children, and for keys $x_1 < \dots < x_j$ the child $i$ (counted from 0) holds only keys between $x_i$ and $x_{i+1}$, with $x_0 = -\infty$ and $x_{j+1} = +\infty$, and (T3) all paths from the root of the subtree to a leaf have the same number of nodes. In a valid subtree, $d(t)$ is well defined.

## Insertion

**Lemma 1 (INS).** Let $t$ be a valid subtree and $k$ a key. After INS$(t, k)$:

1. if $k \in K(t)$, the result is nil and $t$ is unchanged;
2. else, if the result is nil, $t$ is valid with $K(t) \cup \{k\}$ and the same $d(t)$;
3. else the result is $(m, a, b)$, where $a$ and $b$ are valid with $d(a) = d(b) = d(t)$, each key of $a$ is less than $m$, each key of $b$ is greater than $m$, and $K(a) \cup \{m\} \cup K(b) = K(t) \cup \{k\}$.

*Proof.* By induction on $d(t)$. If $k$ is a key of $t$, line L4 returns nil. Else, if $t$ is a leaf, line L5 puts $k$ into the sorted list of $t$; if $k$ is in a deeper node, then $t$ is internal and the case is handled below.

*Leaf.* After line L5, $t$ has two or three keys in order. With two keys, line L13 returns nil, and $t$ is a valid leaf with $d(t) = 1$. With three keys $x < y < z$, line L12 returns $(y, [x], [z])$, two leaves, which satisfy part 3.

*Internal node.* Line L7 picks the child $c = t.kids[i]$ whose range holds $k$; by (T2), if $k$ is in the tree below $t$, it is in $c$. By the induction hypothesis on $c$, which has $d(c) = d(t) - 1$: if $k \in K(c)$, the result is nil and nothing changed. If line L8 returns nil with $k \notin K(c)$, then $c$ is valid with the new key and the same depth, and $k$ lies in the range of child $i$, so $t$ is valid; line L9 returns nil. Else line L8 returns $(m, a, b)$. Line L10 puts $m$ at position $i$ of $t.keys$ and replaces $c$ by $a$ and $b$. Since $m$ and the keys of $a$ and $b$ come from $K(c) \cup \{k\}$, they lie in the range of $c$, between $x_i$ and $x_{i+1}$; so the keys of $t$ stay in order, and $a$, $b$ lie in the ranges that $m$ cuts out of the old range. The number of children is one more than before, as is the number of keys, and $d(a) = d(b) = d(c)$, so (T2) and (T3) hold. If $t$ now has two keys, line L13 returns nil. If it has three keys $x < y < z$ and four children $c_0, c_1, c_2, c_3$, line L12 returns $y$, the node $[x]$ with $c_0, c_1$, and the node $[z]$ with $c_2, c_3$. By (T2) for the 4-node, the keys of $c_0$ and $c_1$ are less than $y$ and those of $c_2$, $c_3$ are greater, and the two new nodes satisfy (T1) to (T3) with depth $d(t)$. $\square$

**INSERT.** If the tree is empty, line L1 makes a valid leaf. Else, by Lemma 1, either the root is valid with the new key, or line L3 makes a new root $[m]$ with the children $a$ and $b$. This root is valid: $a$ and $b$ have the same depth, and their keys lie on the right sides of $m$. All leaves move one level down together.

## Deletion

An *empty* node is a node with no keys and one child (internal) or none (leaf). A subtree is *nearly valid* when it is valid, or its root is empty and its only child is valid (or it is a single empty leaf). Define $d$ of an empty node as 1 plus $d$ of its child, or 1 for an empty leaf.

**Lemma 2 (FIX).** Let $t$ be a node whose children are valid, except that $c = t.kids[i]$ is nearly valid with an empty root, and all children have the same $d$. Let the keys of $t$ and its children satisfy (T2). After FIX$(t, i)$, all children of $t$ are valid with the same $d$ as before, the keys in the subtree of $t$ are the same, the keys of $t$ and its children satisfy (T2), and $t$ has one key less than before or the same number.

*Proof.* Assume the sibling $s$ is $t.kids[i + 1]$ and $x = t.keys[i]$ is the key between them; the case $s = t.kids[i - 1]$ is the mirror image. Every key in $c$ is less than $x$ and every key in $s$ is greater.

*Borrow (lines L22 and L23).* Let $s$ have keys $y < z$ and, if it is internal, children $s_0, s_1, s_2$. Then $c$ gets the key $x$ and, after its own child $c_0$, the child $s_0$; $t.keys[i]$ becomes $y$; and $s$ keeps $z$ with $s_1, s_2$. The keys of $c_0$ are less than $x$ (they were in $c$), and the keys of $s_0$ are between $x$ and $y$ (they were in $s$, below $y$). So $c$ is a valid 2-node, and it lies below the new separator $y$. The node $s$ is a valid 2-node above $y$. Since $c_0$ and $s_0$ had the same depth, $d(c) = d(s)$ is as before. $t$ has the same number of keys.

*Merge (lines L24 and L25).* Let $s$ have one key $y$ and, if internal, children $s_0, s_1$. The merged node has keys $x < y$ and children $c_0, s_0, s_1$, with the keys of $c_0$ below $x$, those of $s_0$ between $x$ and $y$, and those of $s_1$ above $y$. It is a valid 3-node with the old depth. The key $x$ and the child $c$ leave $t$, which keeps one child fewer and one key fewer, so the key ranges of $t$ are still right. $\square$

**Lemma 3 (DEL).** Let $t$ be valid. After DEL$(t, k)$, the subtree of $t$ is nearly valid, holds $K(t) \setminus \{k\}$, and has the same $d$ as before.

*Proof.* By induction on $d(t)$. *Leaf (line L17).* Removing $k$ leaves zero or one key, or two when $k$ was absent; the result is a leaf, so it is nearly valid with $d = 1$.

*Internal node.* If $k$ is a key $x_j$ of $t$, line L19 finds the least key $s$ of the child $j + 1$ by going to the first child until a leaf. By (T2), $x_j < s$ and every other key of that subtree is greater than $s$. So after $t.keys[j] \leftarrow s$, the order (T2) holds at $t$ for the tree in which the child $j + 1$ still holds $s$, and it is enough to delete $s$ from it, which line L20 does with $i = j + 1$. If $k$ is not a key of $t$, line L18 picks the child $i$ whose range holds $k$, and $k$ can only be there. By the induction hypothesis, after line L20 the child $i$ is nearly valid with the right keys and the same depth. If it is not empty, $t$ is valid. If it is empty, line L21 calls FIX, and by Lemma 2 all children of $t$ are valid with the old depth. Then $t$ has at least zero keys and at most its old number, and its children satisfy (T2) and (T3), so the subtree of $t$ is nearly valid: either $t$ is valid, or $t$ lost its only key in a merge and has one child, which is valid. $\square$

**DELETE.** By Lemma 3, after line L15 the root is valid or empty. If it is empty, line L16 replaces it by its only child, which is valid, or by nil. All leaves move one level up together, so (T3) holds.

## Conclusion

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions the tree is a valid 2-3 tree that holds exactly the keys inserted and not deleted since, and a search returns true exactly for these keys.

*Proof.* The empty tree is valid. INSERT and DELETE keep the tree valid and change the key set as stated, by Lemma 1 and Lemma 3. A search at a node either finds $k$ among its keys, or goes to the child whose range holds $k$; by (T2), $k$ can be in the subtree only there. It reaches a leaf after $d(\text{root})$ steps. $\blacksquare$
