---
title: Select and rank are correct, and updates keep the sizes right
proves: [correctness]
status: full
---

Write $|x|$ for the number of nodes in the subtree of $x$, with $|\text{nil}| = 0$, and $S(x)$ for the sorted list of the keys of the subtree of $x$, indexed from 0. The size invariant is (Z) $x.size = |x|$ for every node $x$. The search-tree order gives $S(x) = S(x.left) \cdot [x.key] \cdot S(x.right)$, where the dot joins lists. By (Z), SIZE$(x) = |x|$ for every $x$, nil included (line L13).

**Lemma 1 (UPDATE and rotations keep (Z)).** If (Z) holds at the children of $x$, line L14 makes it hold at $x$. A rotation (lines L15 and L16) changes the children only of the two nodes $h$ and $x$ it moves; it calls UPDATE first on $h$, which is now the child of $x$ and whose children have right sizes, and then on $x$. So (Z) holds at both, and at every other node, whose subtree has the same node set as before.

*Proof.* $|x| = 1 + |x.left| + |x.right|$ for any node. A rotation changes only the links of $h$ and $x$; any other node keeps its children and its subtree, and the subtree of the top keeps the same node set. $\square$

**Lemma 2 (updates keep (Z)).** Insertion and deletion are those of the [left-leaning red-black tree](/left-leaning-red-black-tree/), with rotations as in Lemma 1 and with UPDATE$(h)$ at the end of FIX-UP (line L17). If (Z) holds before an update, it holds after.

*Proof.* The recursive procedures PUT, REMOVE and DELETE-MIN change the tree only by rotations, color flips, by replacing a child pointer of the current node $h$ with the result of a recursive call, by making a new node of size 1, by copying a key, and by returning nil for a removed leaf. Flips and key copies do not change any subtree's node set. Rotations keep (Z) by Lemma 1. By induction on the depth of the recursion, each recursive call returns a subtree in which (Z) holds; at that point, only $h$ may have a wrong size, since its child pointer changed. Each such procedure ends with FIX-UP$(h)$, whose rotations keep (Z) in the subtrees they touch, and whose last step, line L17, recomputes the size of the node it returns from its children. So (Z) holds in the returned subtree. The rotations of MOVE-RED-LEFT and MOVE-RED-RIGHT happen before the recursive call, when (Z) holds everywhere, and keep it by Lemma 1. $\square$

**Lemma 3 (SELECT).** If (Z) holds and $0 \le i < |T.root|$, SELECT$(T, i)$ returns $S(T.root)[i]$.

*Proof.* Invariant at line L3: $x$ is a node, $0 \le i < |x|$, and $S(x)[i]$ is the wanted key. It holds at the start. Let $r = |x.left|$ (line L3). By $S(x) = S(x.left) \cdot [x.key] \cdot S(x.right)$, entry $i$ is $x.key$ if $i = r$ (line L4), entry $i$ of $S(x.left)$ if $i < r$ (line L5), and entry $i - r - 1$ of $S(x.right)$ if $i > r$ (line L6). In the last two cases the new $i$ is at least 0 and less than the size of the new $x$, which is therefore not nil. Each step goes one level down, so the loop stops. $\square$

**Lemma 4 (RANK).** If (Z) holds, RANK$(T, k)$ returns the number of keys of $T$ less than $k$, for any $k$.

*Proof.* Invariant at line L8: the answer is $r$ plus the number of keys less than $k$ in the subtree of $x$ (with 0 for nil). At the start $r = 0$ and $x$ is the root. If $k < x.key$, no key of $x$ or its right subtree is less than $k$, so the answer is $r$ plus the count in $x.left$ (line L9). If $k = x.key$, the keys less than $k$ below $x$ are those of $x.left$, so the answer is $r + |x.left|$ (line L10). If $k > x.key$, all of $x.left$ and $x$ itself are less than $k$, so the answer is $r + |x.left| + 1$ plus the count in $x.right$ (line L11). When $x$ is nil, the answer is $r$ (line L12). Each step goes one level down. $\square$

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions, the tree is a valid left-leaning red-black tree with the right key set and with (Z), and SELECT and RANK return the key of a given rank and the rank of a given key.

*Proof.* The empty tree satisfies (Z) vacuously. The left-leaning red-black tree page proves that the updates keep the red-black rules and the key set; the size field does not affect any of their tests. Lemma 2 keeps (Z), and Lemmas 3 and 4 give the queries. $\blacksquare$
