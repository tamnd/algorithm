---
title: Functional insertion and deletion keep the red-black invariant
proves: [correctness]
status: full
---

We use the notation of the page. $K(t)$ is the set of keys of $t$. $\text{RB}(t, h)$ means that $t$ meets (R1) search order, (R2) no red node has a red child, and (R3) equal black counts on all paths, with black height $h$. $\text{IR}(t, h)$ means that $t$ meets (R1) and (R3) with black height $h$, and that it meets (R2) except perhaps at its root: either $\text{RB}(t, h)$, or $t$ is red and both its children meet $\text{RB}(\cdot, h)$. Each claim on the keys below is that the keys are in order and that the key set is as stated; the order is kept because each NODE call puts keys in the order they have in its arguments, which we check once per case and then do not repeat.

Since no procedure writes a field of an existing node, a call never changes its arguments, and every old version keeps its tree. So it is enough to prove that each call returns the right tree.

Three facts are used often. (F1) If $\text{RB}(t, h)$ and $t$ is red, its children are black or nil and meet $\text{RB}(\cdot, h)$. (F2) If $\text{RB}(t, h)$ and $t$ is black, its children meet $\text{RB}(\cdot, h - 1)$. (F3) If $\text{IR}(t, h)$ and $t \ne \text{nil}$, then BLACKEN$(t)$ meets $\text{RB}(\cdot, h')$ with a black root, where $h' = h + 1$ if $t$ was red and $h' = h$ if it was black. A nil tree has black height 0, and a tree of black height $h \ge 1$ is not nil.

## BALANCE

**Lemma 1.** Let $\text{IR}(a, h)$ and $\text{IR}(b, h)$, with at least one of $a$, $b$ meeting $\text{RB}(\cdot, h)$, and $K(a) < x < K(b)$. Then $t = $ BALANCE$(a, x, b)$ meets $\text{RB}(t, h + 1)$ with $K(t) = K(a) \cup \{x\} \cup K(b)$, and its root is black, or red with two black children.

*Proof.* Line L10: $a$ and $b$ are red. BLACKEN of an infrared red tree of black height $h$ is a black-rooted $\text{RB}$ tree of black height $h + 1$ (F3). The new red root has two black children of black height $h + 1$, so it meets (R2) and (R3) with black height $h + 1$.

Line L11: $a$ is red with a red left child, and line L10 did not apply, so $b$ is not red. Since $a$ breaks (R2) at its root, $a$ is not $\text{RB}$, so $\text{RB}(b, h)$. As $a$ is infrared, its children $a.left$ and $a.right$ meet $\text{RB}(\cdot, h)$. BLACKEN$(a.left)$ is black with black height $h + 1$ (F3). The node NODE(black, $a.right$, $x$, $b$) has two children of black height $h$ that meet RB, so it meets $\text{RB}(\cdot, h + 1)$. The red root has two black children of black height $h + 1$. The keys are $K(a.left) < a.key < K(a.right) < x < K(b)$, which is the order of the new tree.

Lines L12, L13 and L14 are the same argument for the other three places of the red pair. In line L12, $a.right$ is red and, as a child of the infrared tree $a$, meets $\text{RB}(\cdot, h)$, and its children $a.right.left$ and $a.right.right$ meet $\text{RB}(\cdot, h)$ by (F1); the two new black nodes have children of black height $h$. Lines L13 and L14 are the mirror images of L11 and L12, with $a$ in the role of $b$.

Line L15: no case applied. If $a$ is red, its children are not red (else L11 or L12), so $\text{RB}(a, h)$; the same holds for $b$. A black root over two $\text{RB}$ trees of black height $h$ meets $\text{RB}(\cdot, h + 1)$. $\square$

## Insertion

**Lemma 2.** Let $\text{RB}(t, h)$ and $k \notin K(t)$. Then $K(\text{INS}(t, k)) = K(t) \cup \{k\}$. If $t$ is black, INS$(t, k)$ meets $\text{RB}(\cdot, h)$. If $t$ is red or nil, it meets $\text{IR}(\cdot, h)$.

*Proof.* By induction on the size of $t$. If $t = \text{nil}$, line L3 returns a red leaf, which meets $\text{RB}(\cdot, 0)$ and so $\text{IR}(\cdot, 0)$. Let $k < t.key$ (lines L4 to L6); the case $k > t.key$ is the mirror image.

If $t$ is black, its children meet $\text{RB}(\cdot, h - 1)$ (F2). By induction INS$(t.left, k)$ meets $\text{IR}(\cdot, h - 1)$ (for either color of $t.left$, since RB implies IR), and $t.right$ meets $\text{RB}(\cdot, h - 1)$. Lemma 1 gives $\text{RB}(\cdot, h)$ for line L5.

If $t$ is red, its children are black or nil and meet $\text{RB}(\cdot, h)$ (F1). By induction INS$(t.left, k)$ meets $\text{RB}(\cdot, h)$ when $t.left$ is black; when $t.left$ is nil it is a red leaf, which also meets $\text{RB}(\cdot, 0)$ with $h = 0$. So line L6 makes a red root over two $\text{RB}$ trees of black height $h$, which is $\text{IR}(\cdot, h)$. $\square$

**Theorem 1.** If $t$ is a version (it meets (R1) to (R4)), INSERT$(t, k)$ is a version with keys $K(t) \cup \{k\}$.

*Proof.* If $k \in K(t)$, line L1 returns $t$. Else Lemma 2 gives an infrared tree with the right keys (a black root gives RB, which is infrared), and BLACKEN at line L2 gives (R1) to (R4) by (F3). $\square$

## Deletion

**Lemma 3 (BAL-LEFT).** Let $\text{IR}(l, h - 1)$ and $\text{RB}(r, h)$ with $h \ge 1$, and $K(l) < x < K(r)$. Then $t = $ BAL-LEFT$(l, x, r)$ meets $\text{IR}(t, h)$ with $K(t) = K(l) \cup \{x\} \cup K(r)$. If $r$ is black, $t$ meets $\text{RB}(t, h)$.

*Proof.* Since $h \ge 1$, $r$ is not nil.

Line L25: $l$ is red. BLACKEN$(l)$ meets $\text{RB}(\cdot, h)$ with a black root (F3). The new red root has the black left child BLACKEN$(l)$ and the right child $r$, both of black height $h$. So $t$ meets $\text{IR}(t, h)$, and if $r$ is black, it meets (R2) at the root as well, so $\text{RB}(t, h)$.

Line L26: $l$ is not red, so $l$ is black or nil and meets $\text{RB}(l, h - 1)$. The node $r$ is black, so its children meet $\text{RB}(\cdot, h - 1)$ (F2), and REDDEN$(r)$ is a red node over them, which meets $\text{IR}(\cdot, h - 1)$. Lemma 1 applies, with $l$ as the RB argument, and gives $\text{RB}(t, h)$.

Line L28: $l$ is not red, so $\text{RB}(l, h - 1)$, and $r$ is red. By (F1) the children of $r$ are black or nil with black height $h \ge 1$, so they are black nodes; let $a = r.left$, and note that $r.right$ is black. By (F2) the children of $a$ meet $\text{RB}(\cdot, h - 1)$. The node NODE(black, $l$, $x$, $a.left$) has two RB children of black height $h - 1$, so it meets $\text{RB}(\cdot, h)$. REDDEN$(r.right)$ is a red node over the two children of $r.right$, which meet $\text{RB}(\cdot, h - 1)$ by (F2), so it is $\text{IR}(\cdot, h - 1)$. And $a.right$ meets $\text{RB}(\cdot, h - 1)$. Lemma 1 gives that BALANCE$(a.right, r.key, \text{REDDEN}(r.right))$ meets $\text{RB}(\cdot, h)$. The red root over two RB trees of black height $h$ meets $\text{IR}(t, h)$. The keys are $K(l) < x < K(a.left) < a.key < K(a.right) < r.key < K(r.right)$, which is the order of the new tree. $\square$

**Lemma 3' (BAL-RIGHT).** The mirror image: if $\text{RB}(l, h)$ and $\text{IR}(r, h - 1)$ with $h \ge 1$, then BAL-RIGHT$(l, x, r)$ meets $\text{IR}(\cdot, h)$, and $\text{RB}(\cdot, h)$ if $l$ is black. The proof is Lemma 3 with left and right exchanged, line by line (L29 for L25, L30 for L26, L31 for L27 and L28).

**Lemma 4 (FUSE).** Let $\text{RB}(a, h)$ and $\text{RB}(b, h)$ with $K(a) < K(b)$. Then $t = $ FUSE$(a, b)$ meets $\text{IR}(t, h)$ with $K(t) = K(a) \cup K(b)$. If each of $a$ and $b$ is black or nil, $t$ meets $\text{RB}(t, h)$.

*Proof.* By induction on the total size of $a$ and $b$.

Lines L32 and L33: the result is the other tree, which meets $\text{RB}(\cdot, h)$.

Lines L34 to L37: $a$ and $b$ are red. By (F1), $a.right$ and $b.left$ are black or nil with black height $h$, so by induction $c = $ FUSE$(a.right, b.left)$ meets $\text{RB}(c, h)$. If $c$ is red (line L36), its children are black or nil and meet $\text{RB}(\cdot, h)$ (F1); the two new red nodes each have two black-or-nil RB children of black height $h$ ($a.left$ and $c.left$, and $c.right$ and $b.right$), so they meet $\text{RB}(\cdot, h)$, and the red root over them is $\text{IR}(t, h)$. If $c$ is not red (line L37), the new red node over $c$ and $b.right$ meets $\text{RB}(\cdot, h)$, and the red root over $a.left$ (black or nil) and it is $\text{IR}(t, h)$.

Lines L38 to L41: $a$ and $b$ are black, so $h \ge 1$, and by (F2) $a.right$ and $b.left$ meet $\text{RB}(\cdot, h - 1)$. By induction $c$ meets $\text{IR}(c, h - 1)$. If $c$ is red (line L40), its children meet $\text{RB}(\cdot, h - 1)$ by the definition of IR, so each new black node has two RB children of black height $h - 1$ and meets $\text{RB}(\cdot, h)$, and the red root over two black nodes meets $\text{RB}(t, h)$. If $c$ is not red (line L41), then $\text{RB}(c, h - 1)$, so the node NODE(black, $c$, $b.key$, $b.right$) meets $\text{RB}(\cdot, h)$ and is black. Lemma 3 applies with $l = a.left$, which meets $\text{RB}(\cdot, h - 1)$ and so $\text{IR}(\cdot, h - 1)$, and gives $\text{RB}(t, h)$, because its right argument is black.

Line L42: $b$ is red and, since lines L34 and L38 did not apply, $a$ is black. By (F1), $b.left$ is black or nil with black height $h$, so by induction FUSE$(a, b.left)$ meets $\text{RB}(\cdot, h)$ (both arguments black or nil). The red root over it and $b.right$ (black or nil, RB of black height $h$) meets $\text{IR}(t, h)$. Line L43 is the mirror image, with $a$ red and $b$ black.

In each case, the keys of $t$ are the keys of $a$ followed by the keys of $b$, in order, since each new node puts the keys of $a$ before those of $c$ and those of $c$ before those of $b$. $\square$

**Lemma 5 (DEL).** Let $\text{RB}(t, h)$ and $k \in K(t)$. Then $K(\text{DEL}(t, k)) = K(t) \setminus \{k\}$. If $t$ is black, DEL$(t, k)$ meets $\text{IR}(\cdot, h - 1)$. If $t$ is red, it meets $\text{RB}(\cdot, h)$.

*Proof.* By induction on the size of $t$. Since $k \in K(t)$, $t$ is not nil, and each recursive call is on a child that holds $k$, so it is not nil either.

*Case $k < t.key$, $t.left$ black (line L19).* Let $g = \text{bh}(t.left) \ge 1$, so $\text{RB}(t.right, g)$ as well. By induction DEL$(t.left, k)$ meets $\text{IR}(\cdot, g - 1)$. Lemma 3 gives $\text{IR}(\cdot, g)$, and $\text{RB}(\cdot, g)$ if $t.right$ is black. If $t$ is black, $h = g + 1$, and the result is $\text{IR}(\cdot, h - 1)$. If $t$ is red, $h = g$, and $t.right$ is black by (F1) and not nil (its black height is $g \ge 1$), so the result is $\text{RB}(\cdot, h)$.

*Case $k < t.key$, $t.left$ not black (line L20).* The child $t.left$ holds $k$, so it is not nil, and it is red. Then $t$ is black by (R2), and $h = \text{bh}(t.left) + 1$. By induction DEL$(t.left, k)$ meets $\text{RB}(\cdot, h - 1)$, and $t.right$ meets $\text{RB}(\cdot, h - 1)$ by (F2). A red root over two RB trees of black height $h - 1$ is $\text{IR}(\cdot, h - 1)$, as required for black $t$.

*Case $k > t.key$ (lines L22 and L23).* The mirror image, with Lemma 3'.

*Case $k = t.key$ (line L24).* Let $g = \text{bh}(t.left) = \text{bh}(t.right)$. Lemma 4 gives $\text{IR}(\cdot, g)$ with keys $K(t) \setminus \{k\}$. If $t$ is black, $h = g + 1$, so this is $\text{IR}(\cdot, h - 1)$. If $t$ is red, both children are black or nil (F1), Lemma 4 gives $\text{RB}(\cdot, g)$, and $g = h$. $\square$

**Theorem 2.** If $t$ is a version, DELETE$(t, k)$ is a version with keys $K(t) \setminus \{k\}$.

*Proof.* If $k \notin K(t)$, line L16 returns $t$. Else $t$ is black by (R4), so Lemma 5 gives an infrared tree with the right keys, and BLACKEN at line L17 gives a version by (F3), or nil, which is a version. $\square$

## Persistence

**Corollary.** For any sequence of insertions and deletions in which each update takes any earlier version, every version is a red-black tree with the keys that the updates on its chain from the empty tree give, and CONTAINS answers correctly on it.

*Proof.* By induction on the number of updates, with Theorems 1 and 2, and the fact that no call writes to an existing node, so no update changes an earlier version. CONTAINS is the search of a binary search tree, which is correct by (R1). $\blacksquare$
