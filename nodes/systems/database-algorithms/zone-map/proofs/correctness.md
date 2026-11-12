---
title: A zone map scan returns exactly the qualifying rows, and its bounds stay valid under appends and updates
proves: [correctness]
status: full
---

Notation as on the page. Block $k$ holds the rows $r$ with $\lfloor r / b \rfloor = k$. The invariant (V) says: for every row $r$ in block $k$, $lo_k \le A(r) \le hi_k$.

**Lemma 1 (build).** After `build`, (V) holds with tight bounds.

*Proof.* `build` appends the rows one by one. Induction on the number of rows. With no rows there are no blocks. When row $r$ with value $v$ is appended: if $r$ is a multiple of $b$, a new block $k = r/b$ starts with $lo_k = hi_k = v$, which is the minimum and maximum of its one row. Otherwise row $r$ joins block $k = \lfloor r/b \rfloor$, and $lo_k \leftarrow \min(lo_k, v)$, $hi_k \leftarrow \max(hi_k, v)$. If $lo_k$ was the minimum of the old rows of the block, the new $lo_k$ is the minimum of the old rows and $v$, and the same holds for $hi_k$. Other blocks do not change. $\square$

**Lemma 2 (update).** If (V) holds before UPDATE$(Z, r, x)$, it holds after it.

*Proof.* Line L10 finds the block $k$ of row $r$. Line L11 changes only $A(r)$. For a row $r' \ne r$ of block $k$, $A(r')$ is unchanged, and line L12 can only lower $lo_k$ and raise $hi_k$, so $lo_k \le A(r') \le hi_k$ still holds. For row $r$, the new $lo_k = \min(\text{old } lo_k, x) \le x$ and the new $hi_k \ge x$. Rows of other blocks and their bounds do not change. $\square$

The same argument covers a delete that only marks a row as gone: no bound changes, and the remaining rows still satisfy (V). Recomputing the bounds of a block from all its rows makes them tight, so it also keeps (V).

**Theorem.** If (V) holds, SCAN$(Z, lo, hi)$ returns exactly the rows $r$ with $lo \le A(r) \le hi$, in row order.

*Proof.* Take any row $r$, in block $k$.

- If $lo \le A(r) \le hi$: by (V), $hi_k \ge A(r) \ge lo$ and $lo_k \le A(r) \le hi$. So the test of line L3 is false, block $k$ is read in line L6, row $r$ is visited by line L7, and line L8 adds it.
- If $A(r) < lo$ or $A(r) > hi$: whether the block is read or skipped, line L8 never adds $r$, because line L8 adds only rows that pass the predicate, and row $r$ is visited only through its own block.

Each row is visited at most once, since the blocks are disjoint and each is read at most once. Blocks are visited in increasing order and rows inside a block in increasing order, so the result is in row order. $\blacksquare$

**Corollary (sorted data).** If $A$ is non-decreasing in row order and the bounds are tight, the blocks read by SCAN are the blocks with at least one qualifying row, plus one block only when no row qualifies.

*Proof.* Let block $k$ be read and hold no qualifying row. With tight bounds, $lo_k = A(s)$ and $hi_k = A(t)$ for rows $s, t$ of block $k$. Since block $k$ is read, $hi_k \ge lo$ and $lo_k \le hi$. If $lo_k \ge lo$, then $lo \le A(s) \le hi$ and row $s$ qualifies, a contradiction; so $lo_k < lo$. In the same way $hi_k > hi$. Now let row $u$ qualify. Then $A(s) < lo \le A(u) \le hi < A(t)$. Since $A$ is non-decreasing in row order, $s < u < t$, and rows $s$ and $t$ are in block $k$, so $u$ is in block $k$ as well, a contradiction. So when such a block exists, no row qualifies at all. If two such blocks $k < k'$ existed, the last row of block $k$ would have a value $hi_k > hi \ge lo > lo_{k'}$ that is larger than the first value of block $k'$, which contradicts the order. So there is at most one. $\blacksquare$
