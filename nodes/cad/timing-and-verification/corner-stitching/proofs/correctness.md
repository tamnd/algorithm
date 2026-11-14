---
title: Corner stitching keeps a canonical tiling with correct stitches, and its walks find what they claim
proves: [correctness, termination, space bound, complexity]
status: full
---

We use the model and the pseudocode of the page. The world is $W = [X_0, X_1) \times [Y_0, Y_1)$ with integer corners. A *tile* is a half-open rectangle $[x_0, x_1) \times [y_0, y_1)$ with integer corners and $x_0 < x_1$, $y_0 < y_1$, marked *solid* or *space*. Because all corners are integers, a point $(x, y - \varepsilon)$ for a small $\varepsilon > 0$ lies in the same tile as the point $(x, y - \tfrac12)$, and we use the second form. The structure keeps four invariants.

- **(T)** The tiles partition $W$: each point of $W$ lies in exactly one tile.
- **(S)** For each tile $t$: $bl(t)$ is the tile that contains $(x_0, y_0 - \tfrac12)$, $lb(t)$ the tile that contains $(x_0 - \tfrac12, y_0)$, $tr(t)$ the tile that contains $(x_1 - \tfrac12, y_1)$, and $rt(t)$ the tile that contains $(x_1, y_1 - \tfrac12)$. A stitch whose point is outside $W$ is nil.
- **(H)** No two space tiles share a piece of a vertical edge.
- **(V)** No two space tiles with the same $x$-span share a piece of a horizontal edge.

Two tiles are *left and right neighbours* if the right edge of one lies on the left edge of the other and their $y$-spans overlap in an interval of positive length. Top and bottom neighbours are defined in the same way.

## The canonical form

For a height $y$ and a free point $(x, y)$ (a point of $W$ in no solid tile), let $\sigma_y(x) = [a, b)$ be the maximal half-open interval that contains $x$ and is free at height $y$.

**Lemma 1 (uniqueness).** Under (T), (H) and (V), the space tile that contains a free point $p = (x, y)$ is $[a, b) \times [c, d)$, where $[a, b) = \sigma_y(x)$ and $[c, d)$ is the maximal interval of heights that contains $y$ such that $[a, b)$ is a maximal free interval at every height of $[c, d)$. So the space tiles are fixed by the solid tiles.

*Proof.* Let $s = [a', b') \times [c', d')$ be the space tile that contains $p$. Every point of $s$ is free. At each height $y'$ of $[c', d')$, the point $(a' - \tfrac12, y')$, if it is in $W$, lies in a left neighbour of $s$, which is solid by (H). So $a'$ is the left end of a maximal free interval at height $y'$, and in the same way $b'$ is the right end. Hence $[a', b') = \sigma_{y'}(x)$ for all $y' \in [c', d')$, and $[c', d') \subseteq [c, d)$ with $[a', b') = [a, b)$. Suppose $d' < d$. Then the free interval at height $d'$ is $[a, b)$, and the tiles that contain the points $(x'', d')$ with $a \le x'' < b$ are space tiles. Take the one, $s'$, that contains $(a, d')$. By the argument above applied to $s'$, its $x$-span is the maximal free interval $[a, b)$ at height $d'$, so $s'$ and $s$ have the same $x$-span and share the edge at height $d'$, which (V) forbids. So $d' = d$, and in the same way $c' = c$. $\square$

**Lemma 2 (space bound).** If there are $n$ solid tiles, there are at most $3n + 1$ space tiles.

*Proof.* Sweep a horizontal line from $Y_0$ upward. At each height the free part of the line is a set of maximal free intervals. By Lemma 1, a space tile is a maximal run of heights over which one interval $[a, b)$ stays a maximal free interval, so the number of space tiles is the number of times an interval *appears*: it is a maximal free interval at height $y$ and either $y = Y_0$ or it is not a maximal free interval at height $y - \tfrac12$. Let $n_0$ be the number of solid tiles with $y_0 = Y_0$. At $Y_0$ these tiles cut the line into at most $n_0 + 1$ free intervals. We charge each appearance of $[a, b)$ at a height $y > Y_0$ to one solid tile, by these rules.

1. If $a > X_0$, the point $(a - \tfrac12, y)$ is not free, so it lies in a solid tile $U$, and $U.x_1 = a$ because $(a, y)$ is free. If $U.y_0 = y$, charge $U$ (a *right side* charge: an interval that starts at the right edge of $U$, at the height of the bottom of $U$).
2. Else ($a = X_0$, or $U.y_0 < y$), the point $(a - \tfrac12, y - \tfrac12)$ is outside $W$ or in $U$, so it is not free. If the point $(a, y - \tfrac12)$ lies in a solid tile $T$, then $T.y_1 = y$ (as $(a, y)$ is free) and $T.x_0 = a$ (as $T \ne U$, because $U.x_1 = a$). Charge $T$ (a *top-left* charge: the top-left corner $(T.x_0, T.y_1)$ of $T$ lies in $[a, b)$ at height $T.y_1$).
3. Else the point $(a, y - \tfrac12)$ is free, and the maximal free interval at height $y - \tfrac12$ that contains it is $[a, e)$, since its left neighbour point is not free. It is not $[a, b)$, because $[a, b)$ appears at $y$. If $e > b$, the point $(b, y)$ is not free and $(b, y - \tfrac12)$ is free, so $(b, y)$ lies in a solid tile $V$ with $V.x_0 = b$ and $V.y_0 = y$. Charge $V$ (a *left side* charge: an interval that ends at the left edge of $V$, at the height of the bottom of $V$). If $e < b$, the point $(e, y - \tfrac12)$ lies in a solid tile $T$ with $T.x_0 = e$ and $T.y_1 = y$, since $(e - \tfrac12, y - \tfrac12)$ and $(e, y)$ are free. Charge $T$ as a top-left charge.

A solid tile gets at most one charge of each type. For a top-left charge, the corner $(T.x_0, T.y_1)$ lies in at most one maximal free interval at height $T.y_1$. For a right side charge, exactly one interval starts at $U.x_1$ at height $U.y_0$, and for a left side charge, exactly one interval ends at $V.x_0$ at height $V.y_0$. Side charges happen only at heights $y > Y_0$ with $y$ the bottom of the tile, so the $n_0$ tiles at the bottom of the world get none. So the number of space tiles is at most $(n_0 + 1) + n + 2(n - n_0) \le 3n + 1$. $\square$

## The walks

**Lemma 3 (neighbour lists).** Under (T) and (S), the four loops of the page list exactly the top, right, bottom and left neighbours of $t$, in the stated orders.

*Proof.* We do the top side; the others follow by symmetry. $tr(t)$ contains $(x_1 - \tfrac12, y_1)$, so it is the top neighbour at the right end, and its bottom edge is at $y_1$ (a tile that contains $(x_1 - \tfrac12, y_1)$ and reached below $y_1$ would meet $t$). Let $u$ be a top neighbour with $u.x_0 > t.x_0$. Then $lb(u)$ contains $(u.x_0 - \tfrac12, u.y_0) = (u.x_0 - \tfrac12, t.y_1)$, which is above the top edge of $t$, so $lb(u)$ is the next top neighbour to the left, and its right edge is $u.x_0 > t.x_0$. If $u.x_0 \le t.x_0$, then $lb(u)$ has right edge $u.x_0 \le t.x_0$ and is not a top neighbour, and the loop stops. Each step moves strictly left along the line $y = t.y_1$, so the loop visits each top neighbour once. $\square$

**Lemma 4 (point find).** Under (T) and (S), POINT-FIND returns the tile that contains $p = (p_x, p_y)$, from any start tile.

*Proof.* Line L2 moves to $bl(t)$, whose top edge is $t.y_0$, so the bottom edge strictly decreases and the loop stops with $p_y \ge t.y_0$. It never leaves $W$, since $p_y \ge Y_0$ and $t.y_0 > p_y$ give $t.y_0 > Y_0$. Line L3 moves to $tr(t)$, whose bottom edge is $t.y_1$, and stops with $p_y < t.y_1$; it does not undo L2, since every tile it reaches has $y_0 \le p_y$. So after L2 and L3, $t.y_0 \le p_y < t.y_1$.

Suppose $p_x < t.x_0$, so line L4 moves to $u = lb(t)$, which contains $(t.x_0 - \tfrac12, t.y_0)$ and has right edge $t.x_0$. Then $u.y_0 \le t.y_0 \le p_y$, so L2 does nothing. If $p_y \ge u.y_1$, line L3 moves to $tr(u)$, which contains $(t.x_0 - \tfrac12, u.y_1)$. As $u.y_1 \le p_y < t.y_1$, this point is beside the left edge of $t$, so $tr(u)$ is again a left neighbour of $t$. By induction L3 stops at the tile $t'$ that contains $(t.x_0 - \tfrac12, p_y)$. The case $p_x \ge t.x_1$ is the mirror: L5 and then L2 stop at the tile that contains $(t.x_1, p_y)$.

So after the first time that L2 and L3 finish, each pass of the outer loop moves from the tile that contains a point $(x, p_y)$ to the next tile on the line $y = p_y$, to the left if $p_x$ is left of the current tile and to the right otherwise. A tile reached by a left step has right edge greater than $p_x$, so the next step, if any, is again a left step; the same holds to the right. The tiles on the line $y = p_y$ are finitely many and the walk never returns to one, so it stops, and it stops only at line L6, when $t$ contains $p$. $\square$

**Lemma 5 (area search).** Under all four invariants, AREA-SEARCH returns a solid tile that meets $A = [a_{x0}, a_{x1}) \times [a_{y0}, a_{y1})$ if there is one, and nil otherwise.

*Proof.* The loop visits, from the top down, the tiles that contain the points $(a_{x0}, y)$ for $a_{y0} \le y < a_{y1}$: line A1 finds the top one, and line A5 finds the tile just below the current one on the line $x = a_{x0}$, by Lemma 4. Each visited tile meets $A$. If a visited tile is solid, line A2 returns it. If a visited space tile $t$ has $t.x_1 < a_{x1}$, the point $(t.x_1, \min(t.y_1, a_{y1}) - 1)$ is in $A$ and in a right neighbour of $t$, which is solid by (H), and line A3 returns that tile. If no line returns a tile, every visited tile is space with $t.x_1 \ge a_{x1}$, so for every height $y$ of $A$ the whole row $[a_{x0}, a_{x1}) \times \{y\}$ lies in one space tile, and $A$ is free. $\square$

**Lemma 6 (enumeration).** Under all four invariants, ENUMERATE reports every tile that meets $A$ exactly once.

*Proof.* For a tile $r$ that meets $A$ with $r.x_0 > a_{x0}$, define its *owner* as the tile that contains $(r.x_0 - \tfrac12, \max(r.y_0, a_{y0}))$. That point lies in $A$ (its $x$ is at least $a_{x0}$ because $r.x_0 > a_{x0}$ and the corners are integers, and $\max(r.y_0, a_{y0}) < a_{y1}$ because $r$ meets $A$), so the owner meets $A$, and it is the left neighbour of $r$ whose $y$-span contains $\max(r.y_0, a_{y0})$. So a right neighbour $w$ of a tile $u$ that meets $A$ has owner $u$ exactly when $\max(w.y_0, a_{y0}) \ge u.y_0$, which is the test of line E9 together with $w.y_0 < a_{y1}$ and $w.y_1 > \max(u.y_0, a_{y0})$, the conditions for $w$ to meet $A$.

The tiles with $r.x_0 \le a_{x0}$ that meet $A$ are exactly the tiles on the left edge of $A$, and the outer loop reports each of them once, as in Lemma 5. The other tiles are reported from their owner. By induction on $r.x_0$: the owner has a smaller $x_0$, so it is reported exactly once, and when it is processed, line E9 pushes $r$ once. No tile is pushed by a tile that is not its owner, and a tile on the left edge has $x_0 \le a_{x0}$ and is never pushed. $\square$

## Split and merge keep (T) and (S)

**Lemma 7.** Each of the four primitives SPLIT-H, SPLIT-V, MERGE-V and MERGE-H keeps (T) and (S).

*Proof.* (T) holds because a split replaces a tile by two tiles with the same union and a merge replaces two tiles by their union, which is a rectangle by the precondition (the same span on the shared side).

For (S), a stitch of a tile $w$ is defined by one point $q_w$. The stitch can change only if the tile that contains $q_w$ changes, that is, if $q_w$ is in the changed tiles, or if $w$ itself is a changed tile. We give the case SPLIT-H($t$, $y$), where $t = [x_0, x_1) \times [y_0, y_1)$ becomes $t = [x_0, x_1) \times [y_0, y)$ and $u = [x_0, x_1) \times [y, y_1)$.

- The new tile $u$: $tr(u)$ and $rt(u)$ have the same points as the old $tr(t)$ and $rt(t)$; $bl(u)$ contains $(x_0, y - \tfrac12)$, which is in $t$; $lb(u)$ contains $(x_0 - \tfrac12, y)$, the left neighbour of the old $t$ found by walking up from $lb(t)$ while the top edge is at most $y$ (Lemma 3).
- The tile $t$: $tr(t)$ becomes $u$, since $(x_1 - \tfrac12, y)$ is in $u$. $rt(t)$ becomes the tile that contains $(x_1, y - \tfrac12)$, the right neighbour found by walking down from the old $rt(t)$ while the bottom edge is at least $y$. $bl(t)$ and $lb(t)$ keep their points.
- Other tiles: only stitches whose point lies in the old $t$ can change. A top neighbour $w$ of the old $t$ has $q_w$ for $bl(w)$ at $(w.x_0, y_1 - \tfrac12)$, which is now in $u$ when it was in $t$; the code tests $bl(w) = t$. A right neighbour $w$ has $lb(w)$ at $(x_1 - \tfrac12, w.y_0)$, which lies in $u$ exactly when $w.y_0 \ge y$; those are the right neighbours that the walk down from $rt(t)$ passes. A left neighbour $w$ has $rt(w)$ at $(x_0, w.y_1 - \tfrac12)$, which is in $u$ exactly when $y < w.y_1 \le y_1$; the walk over the left neighbours of $u$ tests $rt(w) = t$. A bottom neighbour $w$ has $tr(w)$ at $(w.x_1 - \tfrac12, y_0)$, which stays in $t$. No other stitch has its point in the old $t$.

SPLIT-V is the same argument with the axes exchanged. For MERGE-V($lo$, $hi$), the stitches whose point is in $hi$ are $bl$ of the top neighbours of $hi$, $lb$ of its right neighbours, $rt$ of its left neighbours and $tr(lo)$; after the merge these points are in $lo$, and the code redirects exactly the stitches equal to $hi$. The new $tr(lo)$ and $rt(lo)$ have the points of the old $tr(hi)$ and $rt(hi)$. MERGE-H is the mirror. $\square$

## Insertion and deletion keep (H) and (V)

**Claim 8 (settling).** During a sequence of SETTLE calls, every tile that has finished its call and is still alive has no space tile with the same $x$-span directly above or below it.

*Proof.* A call ends only when its tile has no such neighbour. A merge during a later call joins two tiles $x$ and $y$ with the same span into $m$. The top neighbours of $m$ are those of the upper tile and its bottom neighbours are those of the lower tile. If a finished tile $z$ had the span of $m$ and touched $m$, it touched $x$ or $y$, which have that span, which the claim excluded for $z$ already. $\square$

**Theorem 9 (insertion).** If the four invariants hold and the area $R = [a, b) \times [c, d)$ is free, then after INSERT they hold again, and $R$ is one solid tile.

*Proof.* (T) and (S) hold by Lemma 7. Since $R$ is free, at every height of $[c, d)$ the interval $[a, b)$ lies in one maximal free interval, so by Lemma 1 the tiles that meet $R$ are space tiles that span $[a, b)$ entirely, stacked on the line $x = a$. After the two cuts of lines I2 and I3, they lie inside the heights $[c, d)$. Line I5 cuts each of them at $a$ and $b$ into a left piece, a middle and a right piece, and line I6 joins the middles, which have the span $[a, b)$, into one solid tile equal to $R$.

(H): a left piece keeps the left neighbours of its column tile, which are solid by (H) before, and its right neighbour is $R$. A right piece is the mirror. The parts cut off at $c$ and $d$ keep the left and right neighbours of their old tiles. No other space tile changes its left or right neighbours.

(V): a pair of space tiles with the same span that touch vertically after the insertion must contain a tile that changed. The upper part $u$ cut off at $d$ has the span of its old tile, its top neighbours are those of the old tile, and its bottom neighbours are $R$ and the pieces, which are strictly narrower than $u$; the part cut off at $c$ is the mirror. Every remaining changed space tile is a piece or a product of a merge in line I7, and by Claim 8 it has no space tile with the same span above or below. $\square$

**Theorem 10 (deletion).** If the four invariants hold and $D = [a, b) \times [c, d)$ is a solid tile, then after DELETE they hold again for the solid tiles without $D$.

*Proof.* (T) and (S) hold by Lemma 7. After line D2, every space left or right neighbour of $D$ lies inside the heights $[c, d)$. Line D4 cuts $D$ at every top and bottom edge of these neighbours that is strictly inside $(c, d)$, and line D5 cuts the neighbours at the same heights. Then for each piece $p$ of $D$, the tiles beside its left edge are either all solid, or exactly one space tile with the same $y$-span as $p$: the $y$-span of a space neighbour is a union of piece spans, and after D5 it is one piece span. That space tile, if it exists, contains $(p.x_0 - \tfrac12, p.y_0)$ and so it is $lb(p)$. The right side is the same with $rt(p)$.

(H): line D6 joins each piece with its space neighbours on both sides. A space neighbour of $D$ is a part of a space tile of the old structure, so its other neighbours on the far side are solid by (H) before. So each row tile runs from a solid tile or the world edge on the left to one on the right. The parts cut off at $c$ and $d$ keep the far side neighbours of their old tile and, on the near side, the old solid neighbours below $c$ or above $d$.

(V): as in Theorem 9. A part $\ell$ cut off above $d$ has the span of its old tile and that tile's top neighbours. Below it lies the top row tile, which contains $\ell$'s span and also $[a, b)$, so it is wider. The part below $c$ is the mirror. All other changed space tiles go through SETTLE in line D7, and Claim 8 applies. $\square$

## Cost

Let $\deg(t)$ be the number of neighbours of $t$.

- A neighbour list of $t$ costs $O(1)$ for each listed tile (Lemma 3).
- POINT-FIND visits no tile twice in its first vertical phase, since the heights of the visited tiles change in one direction. After that, by Lemma 4, the right edge of each visited tile (on a walk to the left) is at most the left edge of the tile of the step before, so no tile repeats there either. So it visits at most $2N$ tiles and costs $O(N)$ for $N$ tiles in the worst case. The bound is tight: for $n$ solid unit squares in one row with one unit of space between them, a walk from the left end to the right end of the row crosses all $2n + 1$ tiles of the row.
- ENUMERATE, after its first point find and the walk down the left edge, examines each pair (reported tile, right neighbour) once, so it costs $O(k + e)$, where $k$ is the number of reported tiles and $e$ the number of such pairs.
- A split or a merge of tiles $t$ and $u$ costs $O(\deg(t) + \deg(u))$. INSERT and DELETE cost the point finds plus $O(1 + \sum \deg)$ over the tiles they split or merge.
