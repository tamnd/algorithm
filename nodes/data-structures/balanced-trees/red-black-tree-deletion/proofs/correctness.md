---
title: Deletion keeps the left-leaning red-black rules
proves: [correctness]
status: full
---

The rules are (L1) search order, (L2) no red right child, (L3) no red node with a red left child, (L4) the same number of black nodes on every path from the root to nil, and (L5) a black root. For a node $h$, write $bh(h)$ for the number of black nodes on a path from $h$ down to nil, counting $h$ itself, with $bh(\text{nil}) = 0$; it is well defined when (L4) holds in the subtree of $h$. Call a subtree *valid* when (L1) to (L4) hold in it; its root may be red. In a valid subtree, a red node has two black children: the left one by (L3), the right one by (L2).

**Lemma A (the steps).** A rotation of a red link, where the child moves up, takes the color of the old top, and the old top becomes red, keeps (L1), keeps (L4) in the subtree, and keeps $bh$ of the top. A color flip at a node whose two children both have the color opposite to its own keeps (L1), (L4) and $bh$ of the top.

*Proof.* A rotation keeps the in-order sequence of the keys. For ROTATE-LEFT$(h)$ with $x = h.right$ red, let $c$ be the color of $h$ and $\alpha$, $\beta$, $\gamma$ the subtrees $h.left$, $x.left$, $x.right$. Before, a path from the top to $\alpha$, $\beta$ or $\gamma$ meets the node $h$ of color $c$ and, for $\beta$ and $\gamma$, the red $x$. After, it meets the node $x$ of color $c$ and, for $\alpha$ and $\beta$, the red $h$. Red nodes add nothing, so each path has the same count. ROTATE-RIGHT is the mirror image. A flip at a black node with two red children makes the node red and the children black: a path from the top meets one black node before (the top) and one after (a child). The other flip is the reverse. Neither step changes keys. $\square$

A call REMOVE$(h, k)$ has the *precondition* that $k \in K(h)$, that (L1), (L3), (L4) hold in the subtree of $h$ and (L2) holds at every node except possibly at $h$, and that one of these holds:

1. (P1) $h$ is red, with two black children;
2. (P2) $h$ is black, $h.left$ is red and $h.right$ is black;
3. (P3) $h$ is black, $h.left$ is black, $h.right$ is red, and $k \ge h.key$.

In the 2-3 view, (P1) and (P2) say that $h$ is not a 2-node, so a key can leave it. The *postcondition* is that the result $x$ is valid, with keys $K(h) \setminus \{k\}$ and $bh(x) = bh(h)$, and that $x$ is black if $h$ was black when the call began. DELETE-MIN$(h)$ has the same precondition with (P1) or (P2), with $k$ the least key, and the same postcondition.

**Lemma 2 (FIX-UP in deletion).** If both children of $h$ are valid with the same $bh$, and if $h$ is red only when both children are black, then FIX-UP$(h)$ returns a valid subtree with the same keys and $bh$. If $h$ is black and $h.right$ is black, the result is $h$ itself, black.

*Proof.* If $h$ is red, its children are black and no test is true. If $h$ is black: with two black children nothing changes; with a red left child and a black right child, line L23 does not apply, since the left child is valid and red, so its left child is black; with a black left child and a red right child, line L22 rotates left and gives a black top with a red left child $h$ whose two children are black, as in Lemma 1; with two red children, line L24 flips and gives a red top with two black children. $\square$

**Lemma 3 (MOVE-RED-LEFT).** Let $h$ be red with valid black children $l$ and $r$, and let $l.left$ be black. After MOVE-RED-LEFT$(h)$, the subtree has the same keys and $bh$, (L1) and (L4) hold, and either (a) the top is $h$, black, with two red children, each with two black children, or (b) the top is red, its right child is black and valid, and its left child is the old $h$, black, with the red left child $l$ (whose children are black) and a black right child.

*Proof.* Line L5 flips at $h$, a red node with two black children: $h$ is black, and $l$ and $r$ are red. The children of $l$ are black ($l.left$ by assumption, $l.right$ by (L2)), and $r.right$ is black by (L2). If $r.left$ is black, the result is (a). Else let $s = r.left$, red, with two black children. Line L6 rotates right at $r$: $s$ takes the red color of $r$ and $r$ becomes its red right child, whose left child is the old $s.right$, black. Then it rotates left at $h$: $s$ moves up with the black color of $h$, $h$ becomes its red left child, and the right child of $h$ is the old $s.left$, black. Then it flips at $s$, a black node with two red children: $s$ is red, and $h$ and $r$ are black. Now $h$ has the red left child $l$ and a black right child, and $r$ has two black children. Every step is one of Lemma A. $\square$

**Lemma 4 (MOVE-RED-RIGHT).** Let $h$ be red with valid black children $l$ and $r$, and let $r.left$ be black. After MOVE-RED-RIGHT$(h)$, the subtree has the same keys and $bh$, (L1) and (L4) hold, and either (a) the top is $h$, black, with two red children, each with two black children, or (b) the top $t$ is red with two black children; $t.left$ is valid, and $t.right$ is the old $h$, black, with a black left child and the red right child $r$, whose children are black; and $t.key < h.key$.

*Proof.* Line L7 flips at $h$: $h$ is black, and $l$ and $r$ are red. The children of $r$ are black ($r.left$ by assumption, $r.right$ by (L2)), and $l.right$ is black by (L2). If $l.left$ is black, the result is (a). Else $l.left$ is red, with black children. Line L8 rotates right at $h$: $l$ moves up with the black color of $h$, $h$ becomes its red right child, and the left child of $h$ is the old $l.right$, black. Then it flips at $l$, a black node with two red children: $l$ is red, $l.left$ is black, and $h$ is black. The node $h$ keeps the red right child $r$. Since $l$ was the left child of $h$, $l.key < h.key$. $\square$

**Lemma 5 (REMOVE and DELETE-MIN).** Under the precondition, REMOVE$(h, k)$ and DELETE-MIN$(h)$ meet the postcondition.

*Proof.* By induction on the size. In every case below, the recursive call meets the precondition, so by induction it returns a valid subtree with the same $bh$ as the child it replaces; then Lemma 2 applies to the last line, and we check its two conditions and the color of the result.

*Case $k < h.key$ (lines L9 to L11).* Since (P3) needs $k \ge h.key$, this case has (P1) or (P2). The key is in $h.left$, which is not nil.

- (P2): $h.left$ is red with black children, so line L10 does nothing and the call on $h.left$ has (P1). Line L11 replaces $h.left$; the right child of $h$ is black and unchanged. By Lemma 2, the result is $h$, black.
- (P1) and $h.left.left$ red: line L10 does nothing. The call on the black $h.left$ has (P2) and returns a black node. At FIX-UP, $h$ is red with two black children, so Lemma 2 applies.
- (P1) and $h.left.left$ black: $h.right$ is not nil, since $bh(h.right) = bh(h.left) \ge 1$. Line L10 calls MOVE-RED-LEFT. In Lemma 3 (a), the call on the red left child has (P1), and at FIX-UP the top is black. In Lemma 3 (b), $k$ is less than the key of the old $h$, which is the left child of the new top, so the recursion goes there, with (P2), and returns a black node; at FIX-UP the top is red with two black children.

*Case $k \ge h.key$ (lines L12 to L16).*

- (P2): line L12 rotates right at $h$. The new top $t$ is the old $h.left$, black, with the black left child $h.left.left$ (by (L3)) and the red right child $h$, whose children are black. Now $k > t.key$, line L13 does not apply ($t.right \ne$ nil), line L14 does nothing ($t.right$ is red), and line L16 calls REMOVE on the red $h$, which has (P1). At FIX-UP, $t$ is black with a black left child, so Lemma 2 gives a black result.
- (P3): line L12 does nothing, line L13 does not apply ($h.right \ne$ nil), and line L14 does nothing ($h.right$ is red). The red right child has two black children, by (L3) and (L2) below $h$. If $k = h.key$, line L15 calls DELETE-MIN on it, and else line L16 calls REMOVE on it; both calls have (P1). At FIX-UP, $h$ is black with a black left child, and the result is black.
- (P1): line L12 does nothing. If $k = h.key$ and $h.right$ is nil, then $bh(h.left) = 0$ and $h.left$ is black, so $h.left$ is nil: $h$ is a red leaf, and line L13 returns nil, with $bh = 0 = bh(h)$. Else $h.right$ is not nil, and neither is $h.left$, by (L4). If $h.right.left$ is red, line L14 does nothing, and the call at line L15 or L16 on the black $h.right$ has (P2) and returns a black node; at FIX-UP, $h$ is red with two black children. If $h.right.left$ is black, line L14 calls MOVE-RED-RIGHT. In Lemma 4 (a), the call on the red right child has (P1), and the top is black at FIX-UP. In Lemma 4 (b), the new top $t$ has $t.key < h.key \le k$, so line L15 does not apply, and line L16 calls REMOVE on the old $h$, which is black, with a black left child and a red right child, and $k \ge h.key$: (P3). It returns a black node, so at the FIX-UP of $t$, $t$ is red with two black children.

When line L15 runs, $h.key$ becomes the least key $m$ of $h.right$. Every key of $h.left$ is less than $k < m$, and every other key of $h.right$ is greater than $m$, so after DELETE-MIN removes $m$ from $h.right$, (L1) holds and the key $k$ is gone.

*DELETE-MIN.* If $h.left$ is nil (line L18), then (P2) is impossible, so $h$ is red, and as above $h$ is a red leaf and the result is nil. Else lines L19 to L21 run the case $k < h.key$ above, with DELETE-MIN in place of REMOVE.

In every case the keys are $K(h) \setminus \{k\}$, and $bh$ is kept, by Lemma A, by induction and by Lemma 2. A result that comes from a call with $h$ black is black, as shown in each case. $\square$

**DELETE.** Line L1 makes sure that $k$ is in the tree. Before line L2 the tree is valid with a black root. If both children of the root are black, line L2 paints the root red, which subtracts one from every path and so keeps (L4); now (P1) holds. Else the root has a red child, which is the left one by (L2), and (P2) holds. By Lemma 5, REMOVE returns a valid tree without $k$. Line L4 paints the root black, which keeps (L4) and gives (L5).

## Conclusion

**Theorem.** If $T$ is a left-leaning red-black tree, then after DELETE$(T, k)$ it is a left-leaning red-black tree whose keys are the old keys without $k$.

*Proof.* If $k$ is not in $T$, line L1 returns with no change. Else this is the paragraph on DELETE above, with Lemma 5. Each call of REMOVE or DELETE-MIN moves one level down, so the procedure stops after at most $h + 1$ calls, where $h$ is the height. $\blacksquare$
