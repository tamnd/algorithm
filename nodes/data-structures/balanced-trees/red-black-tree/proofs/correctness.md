---
title: Insertion and deletion keep the red-black properties
proves: [correctness, rotations.insert, rotations.delete]
status: full
---

The properties are (R0) the search-tree order, (R1) the root is black, (R2) every leaf $T.nil$ is black, (R3) a red node has two black children, and (R4) for each node $v$, all paths from $v$ down to a leaf have the same number of black nodes. A *path weight* is the number of black nodes on a path. Rotations keep the in-order sequence of the keys (see [tree rotation](/tree-rotation/)), so they keep (R0). Each recoloring and rotation below changes only nodes in a subtree $S$ whose root is at a fixed place; we check (R4) by comparing, for each leaf of $S$, the weight of the path from the top of $S$ to that leaf before and after. If all these weights stay equal, then (R4) holds for each node above $S$, because the paths from such a node agree outside $S$.

## Insertion

**Initialization.** Lines L1 to L7 are the insertion of a binary search tree, so (R0) holds and the key set gains $k$ (or line L4 returns and nothing changes, when $k$ is present). The new node $z$ is red, with two black children $T.nil$. It replaces a leaf: each path that ended at that leaf now goes on through the red $z$ to a black leaf, so its weight is unchanged, and (R4) and (R2) hold. The only possible failures are (R1), when the tree was empty and $z$ is the root, and (R3), when the parent of $z$ is red.

**Invariant.** At each test of line L9:

1. (I1) $z$ is red.
2. (I2) (R0), (R2) and (R4) hold.
3. (I3) (R1) holds unless $z$ is the root.
4. (I4) (R3) holds, except that $z$ and its parent may both be red.

This holds at the first test, by the initialization.

**The grandparent.** If the loop body runs, $z.p$ is red. By (I3), the root is black unless $z$ is the root, and the parent of the root is the black $T.nil$, so $z.p$ is not the root, and $g = z.p.p$ is a node. By (I4), the only red-red pair is $z$ and $z.p$, so $g$ is black. Let $p = z.p$, and assume that $p$ is the left child of $g$ (line L10); the other case is the mirror image (line L18). Let $u$ be the right child of $g$, the uncle.

**Case 1: $u$ is red (line L13).** Here $S$ is the subtree of $g$. Before, each path from $g$ to a leaf passes $g$ (black) and then exactly one of $p$, $u$ (red). After the recoloring, it passes $g$ (red) and one of $p$, $u$ (black). Nothing else changes, so each path weight from the top of $S$ is the same, and (R4) holds. Now $p$ and $u$ are black, and $g$ is red with two black children. The only possible red-red pair is $g$ and its parent. The new $z$ is $g$, which is red, so (I1) and (I4) hold. The root changed color only if $g$ is the root, which is then $z$, so (I3) holds.

**Case 2: $u$ is black and $z$ is the right child of $p$ (line L15).** Let $\alpha$ be the left subtree of $p$, and $\beta$, $\gamma$ the subtrees of $z$. Since $p$ and $z$ are red, (R4) at $p$ says that all paths into $\alpha$, $\beta$ and $\gamma$ have the same weight from their roots. The left rotation at $p$ makes $z$ the left child of $g$, with left child $p$; $p$ has subtrees $\alpha$ and $\beta$, and $z$ has right subtree $\gamma$. Both rotated nodes are red, so each path from $g$'s left child has the same weight as before. The new $z$ is the old $p$: it is red, it is the left child of its red parent (the old $z$), and this is the only red-red pair, because $\alpha$, $\beta$ and $\gamma$ have black roots (they were children of red nodes, other than the pair $p$, $z$). So the state is that of case 3.

**Case 3: $u$ is black and $z$ is the left child of $p$ (lines L16 and L17).** Let $\gamma$ be the right subtree of $p$. The roots of $\gamma$ and of the subtrees of $z$ are black by (I4), and $u$ is black. By (R4) at $g$, with $p$ and $z$ red, the paths into the subtrees of $z$, into $\gamma$, and into the subtree of $u$ (counting $u$) all have the same weight $b$. Lines L16 and L17 paint $p$ black and $g$ red and rotate right at $g$. Now $p$ is the root of $S$, with children $z$ (red) and $g$ (red), and $g$ has children $\gamma$ and $u$. Each path from $p$ has weight $1 + b$: the black $p$, then a red node, then a path of weight $b$. Before, each path from $g$ had weight $1 + b$ too: the black $g$, then a red node or the path through $u$. So (R4) holds. The red nodes $z$ and $g$ have black children, and $p$ is black, so (R3) holds everywhere. If $g$ was the root, then $p$ is the new root and it is black.

**Termination.** Case 1 moves $z$ up two levels, so it runs at most $h/2$ times in a row. After case 3, the parent of $z$ is the black $p$, so the test of line L9 fails. At exit, $z.p$ is black, so by (I4) (R3) holds, and by (I3) (R1) can fail only at the root. Line L19 paints the root black. This adds one to the weight of every path from the root, so (R4) still holds, and it cannot create a red-red pair. So the tree satisfies (R0) to (R4). Cases 2 and 3 happen at most once, so an insertion does at most two rotations. $\square$

## Deletion

**Weights with an extra black.** During DELETE-FIXUP, the node $x$ carries an *extra black*: in path weights, $x$ counts one more than its color says. Write (R4$'$) for (R4) with this count.

**Lemma 1 (RB-DELETE).** Let $y$ be the node that leaves its place (line L23 or L27), $c$ its original color, and $x$ the node that takes its place. After lines L23 to L31, the tree holds the old keys without the key of $z$, and (R0) and (R2) hold. If $c$ is red, (R1), (R3) and (R4) hold. If $c$ is black, (R4$'$) holds, and (R3) holds except for a red-red pair that contains $x$, and (R1) holds except that $x$ may be a red root.

*Proof.* Lines L23 to L31 are the deletion of a binary search tree: if $z$ has at most one child, that child replaces $z$; else the successor $y$, which has no left child, is replaced by its right child $x$, and then $y$ replaces $z$. So (R0) holds and the key of $z$ is gone. Line L31 gives $y$ the color of $z$, so at the old place of $z$ the colors are as before. The only change of colors on paths is that the node $y$ of color $c$ no longer lies above $x$.

If $c$ is red, the path weights do not change, so (R4) holds. A red $y$ is not the root, so (R1) holds. Its parent was black and its children were black, so putting $x$ under the parent of $y$ makes no red-red pair. In the two-child case, $y$ gets the color of $z$; if that color is red, the children of $y$ are $z.left$, and $z.right$ or $x$, all of which were children of a red node, so they are black. So (R3) holds.

If $c$ is black, each path through the old place of $y$ lost one black node, and these are exactly the paths through $x$. With the extra black at $x$, each weight is as before, so (R4$'$) holds. A red-red pair can appear only between $x$ and its new parent, and the root changes only if $x$ becomes the root. $\square$

**Invariant.** At each test of line L33:

1. (J1) (R0), (R2) and (R4$'$) hold.
2. (J2) (R3) holds, except for red-red pairs that contain $x$.
3. (J3) (R1) holds, except that $x$ may be a red root.

By Lemma 1 this holds at the first test. When the loop body runs, $x$ is black and is not the root. So by (J2) there is no red-red pair at all, and by (J3) the root is black.

Assume $x$ is the left child of $p = x.p$ (line L34); the right case is the mirror image (line L45). Let $w$ be the right child of $p$ (line L35). The paths from $x$ have weight at least 2 (the black $x$ and its extra), so by (R4$'$) at $p$ the paths from $w$ have weight at least 2, and $w$ is not $T.nil$.

**Case 1: $w$ is red (line L37).** Then $p$ and the children $a$, $b$ of $w$ are black. Let $W$ be the weight of each path from $x$ (with the extra), which by (R4$'$) at $p$ is also the weight of each path from $w$, and so of each path from $a$ and from $b$ (the red $w$ adds nothing). Line L37 paints $w$ black and $p$ red and rotates left at $p$. Now $w$ is the top, with children $p$ and $b$, and $p$ has children $x$ and $a$. Each path from the top has weight $1 + W$: through $w$ (black), then $p$ (red) and a path from $x$ or $a$, or a path from $b$. Before, each path from $p$ had weight $1 + W$ too. So (R4$'$) holds. The red $p$ has the black children $x$ and $a$, so (J2) holds, and if $p$ was the root, the black $w$ is the new root. The new sibling of $x$ is $a$, which is black, and $x.p$ is red. One of cases 2 to 4 follows.

**Case 2: $w$ is black and both children of $w$ are black (line L39).** Line L39 paints $w$ red and moves the extra black from $x$ to $p$. Each path from $p$ through $w$ loses one, and each path through $x$ loses the extra; the extra at $p$ adds one to all paths through $p$. So the weights from the top of the subtree of $p$ are unchanged, and (R4$'$) holds with the new $x = p$. The red $w$ has black children. If $p$ is red, then $p$ and $w$ form a red-red pair, which contains the new $x$, as (J2) allows. If $p$ is the root, it is the new $x$, as (J3) allows.

**Case 3: $w$ is black, its left child $a$ is red and its right child $b$ is black (line L42).** Let $a_1$ and $a_2$ be the children of $a$; they are black. By (R4) at $w$, the paths from $a_1$, from $a_2$ and from $b$ have the same weight $d$. Line L42 swaps the colors of $w$ and $a$ and rotates right at $w$. Now $a$ (black) has children $a_1$ and $w$ (red), and $w$ has children $a_2$ and $b$. Each path from $a$ has weight $1 + d$; before, each path from $w$ had weight $1 + d$. So (R4$'$) holds. The red $w$ has black children $a_2$ and $b$. The new sibling of $x$ is $a$, black, and its right child $w$ is red. This is case 4.

**Case 4: $w$ is black and its right child $b$ is red (lines L43 and L44).** Let $a$ be the left child of $w$, of any color, and let $c_p$ be the color of $p$ (1 if black, 0 if red). Let $W$ be the weight of each path from $x$ with the extra. By (R4$'$) at $p$ and (R4) at $w$, each path from $a$ and each path from $b$ has weight $W - 1$, and $b$ is red, so each path from a child of $b$ has weight $W - 1$. Before, each path from $p$ has weight $c_p + W$. Lines L43 and L44 give $w$ the color $c_p$, paint $p$ and $b$ black, rotate left at $p$, and drop the extra black of $x$. Now $w$ is the top, with children $p$ and $b$, and $p$ has children $x$ and $a$. A path from the top through $p$ and $x$ has weight $c_p + 1 + (W - 1)$. A path through $p$ and $a$ has weight $c_p + 1 + (W - 1)$. A path through $b$ has weight $c_p + 1 + (W - 1)$. All equal $c_p + W$, so (R4) holds with no extra black anywhere. The nodes $p$ and $b$ are black. If $w$ is red, then $c_p$ was red, so the parent of the top is black, since there was no red-red pair. So (R3) holds everywhere. If $p$ was the root, $w$ is the root with the color of $p$, which was black by (J3). Line L44 sets $x$ to the root, so the loop ends.

**Termination.** Case 2 moves $x$ up one level. After case 1, the parent of $x$ is red, so case 2 ends the loop, and cases 3 and 4 end it in at most two more steps. Case 3 leads to case 4, which ends the loop. So the loop runs at most $h + 2$ times. It does at most three rotations: one in case 1, one in case 3 and one in case 4, and each of these cases happens at most once.

**Exit.** At exit, $x$ is red or $x$ is the root. Line L46 paints $x$ black and drops its extra black. If $x$ was red, the paths through $x$ gain one from the color and lose the extra, so (R4) holds, and the red-red pairs that contained $x$ are gone. If $x$ is a black root, dropping the extra subtracts one from every path from the root, which keeps (R4). In both cases (R1) to (R4) hold. If $c$ was red, DELETE-FIXUP is not called and Lemma 1 already gives the properties. $\square$

## Conclusion

**Theorem.** Starting from the empty tree, after any sequence of RB-INSERT and RB-DELETE calls the tree satisfies (R0) to (R4) and holds exactly the keys inserted and not deleted. A search returns true exactly for these keys. Each insertion does at most two rotations, and each deletion at most three.

*Proof.* The empty tree, the sentinel alone, satisfies (R0) to (R4). The insertion and deletion parts above show that each operation keeps the properties and changes the key set as stated. A search is correct by (R0). $\blacksquare$
