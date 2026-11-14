---
title: SELECT-SUM returns the k-th smallest cell, and HODGES-LEHMANN the median of the Walsh averages
proves: [correctness]
status: full
---

**Setting.** $a_0 \le \cdots \le a_{m-1}$ and $b_0 \le \cdots \le b_{n-1}$ are sorted, and $L_0 \le L_1 \le \cdots \le L_{m-1}$. The cells are the pairs $(i, j)$ with $L_i \le j \le n - 1$, and the value of a cell is $a_i + b_j$. There are $N$ cells, and $1 \le k \le N$. Let $s_1 \le \cdots \le s_N$ be the sorted cell values (with multiplicity) and $v^* = s_k$. For a value $v$, $c_\le(v)$ and $c_<(v)$ are the numbers of cells with value $\le v$ and $< v$.

**Lemma 0.** A value $v$ equals $s_k$ if and only if
$$c_<(v) < k \le c_\le(v). \tag{1}$$

*Proof.* If $v = s_k$, the cells $< v$ are among $s_1, \ldots, s_{k-1}$, so $c_<(v) \le k - 1$, and $s_1, \ldots, s_k$ are $\le v$, so $c_\le(v) \ge k$. Conversely, if (1) holds, then at least $k$ cells are $\le v$, so $s_k \le v$; and fewer than $k$ cells are $< v$, so $s_k \not< v$. Thus $s_k = v$. $\square$

**Lemma 1 (COUNT).** For each row $i$, line L15 sets $le[i] = p_i$, where $p_i = \max\{j : a_i + b_j \le v\}$ (and $p_i = -1$ if there is no such $j$). Line L16 adds the number of cells $\le v$ in row $i$. So COUNT returns $c_\le(v)$.

*Proof.* If $a_{i+1} + b_j \le v$, then $a_i + b_j \le v$ because $a_i \le a_{i+1}$. So $p_{i+1} \le p_i$. We show by induction that $j \ge p_i$ when row $i$ starts. For $i = 0$, $j = n - 1 \ge p_0$. For row $i + 1$, $j$ starts at the end value of row $i$, which is $p_i \ge p_{i+1}$. In row $i$, line L14 lowers $j$ while $a_i + b_j > v$. Every column $j > p_i$ has $a_i + b_j > v$, because $b$ is sorted, and column $p_i$ has $a_i + b_{p_i} \le v$. So the loop stops at $j = p_i$. The cells $\le v$ of row $i$ are the columns $L_i, \ldots, p_i$, and there are $\max(0, p_i - L_i + 1)$ of them. This is the value that line L16 adds. The strict count is the same proof with $<$ in place of $\le$. $\square$

The index $j$ only moves down, so one COUNT takes $O(m + n)$ steps.

**The parts of a row.** In row $i$, the columns $L_i \le j < lo_i$ are the left part, the columns $lo_i \le j \le hi_i$ are the active part, and the columns $hi_i < j \le n - 1$ are the right part. $W$ is the number of active cells.

**Invariant.** At the start of each round of the loop of line L2:

- (I) every left cell has value $< v^*$, and every right cell has value $> v^*$.

Line L1 makes all left and right parts empty, so (I) holds before the first round.

**Lemma 2.** If (I) holds, then every cell with value $v^*$ is active, and $W \ge 1$.

*Proof.* A cell with value $v^*$ is neither $< v^*$ nor $> v^*$, so by (I) it is not left and not right. There is at least one such cell, $s_k$. $\square$

**Lemma 3 (one round).** Assume (I) at the start of a round with pivot $v$. Then the round returns $v^*$, or (I) holds at the end of the round and $W$ is at least 1 smaller.

*Proof.* By Lemma 2, line L4 can pick an active cell, and $v$ is its value. By Lemma 1, line L5 computes $c_\le(v)$, $c_<(v)$, and the last columns $le[i]$ and $lt[i]$ whose cells are $\le v$ and $< v$.

*Case $c_<(v) \ge k$ (line L6).* If $v \le v^*$, then $c_<(v^*) \ge c_<(v) \ge k$, which is false by Lemma 0. So $v^* < v$. Line L6 sets $hi_i \leftarrow \min(hi_i, lt_i)$, and the left parts do not change. A cell that joins the right part of row $i$ has a column $> lt_i$, so its value is $\ge v > v^*$. So (I) holds. The pivot has value $v$, which is not $< v$, so its column is $> lt_i$, and it leaves the active part.

*Case $c_<(v) < k \le c_\le(v)$ (line L7).* By Lemma 0, $v = v^*$, and the round returns $v^*$.

*Case $c_\le(v) < k$ (line L8).* If $v \ge v^*$, then $c_\le(v) \ge c_\le(v^*) \ge k$, which is false by Lemma 0. So $v^* > v$. Line L8 sets $lo_i \leftarrow \max(lo_i, le_i + 1)$, and the right parts do not change. A cell that joins the left part of row $i$ has a column $\le le_i$, so its value is $\le v < v^*$. So (I) holds. The pivot has value $v \le v$, so its column is $\le le_i$, and it leaves the active part.

In the first and third cases the active parts only shrink, and the pivot leaves them, so $W$ drops by at least 1. $\square$

**Theorem 1.** SELECT-SUM$(a, b, L, k)$ returns $s_k$, the $k$-th smallest cell value.

*Proof.* By Lemma 3 and induction, (I) holds at the start of every round. $W \le N$ at the start, every round that does not return lowers $W$ by at least 1, and $W \ge 1$ at every start by Lemma 2. So the loop returns after at most $N$ rounds. It returns only at line L7, and there the value is $v^*$ by Lemma 3. $\square$

**Theorem 2.** HODGES-LEHMANN$(x)$ returns the median of the Walsh averages $(x_i + x_j)/2$, $i \le j$.

*Proof.* After line L9, $x$ is sorted. Take $a = b = x$ and $L_i = i$. The cells are the pairs $i \le j$ of sorted positions, and each Walsh average is half the value of exactly one cell. So the median of the Walsh averages is half the median of the cell values. Line L9 sets $k = \lceil N/2 \rceil$, and by Theorem 1 line L10 gives $s_1 = s_k$.

If $N$ is odd, the median of the cell values is $s_k$, line L11 sets $s_2 = s_k$, and line L12 returns $(s_k + s_k)/4 = s_k/2$.

If $N$ is even, the median of the cell values is $(s_k + s_{k+1})/2$. If $c_\le(s_k) \ge k + 1$, then $s_{k+1} \le s_k$, so $s_{k+1} = s_k$. Else $c_\le(s_k) = k$ by Lemma 0, so $s_{k+1}$ is the least cell value greater than $s_k$. In row $i$ the cells greater than $s_k$ are the columns from $\max(le_i + 1, L_i)$ to $n - 1$, and the least of them is the first one, because $b$ is sorted. The minimum of these first cells over all rows is $s_{k+1}$, which line L11 takes. In both cases line L12 returns $(s_k + s_{k+1})/4$, which is half the median of the cell values. $\square$

The two-sample estimator uses the same proof with $a$ the sorted values $-x_i$, $b$ the sorted $y$, and $L_i = 0$. Then the cells are all the pairs, with the values $y_j - x_i$.

**Expected number of rounds.** Put the active cells in order by value, with ties broken by position. The pivot is uniform among the $W$ active cells. Let $r$ be its rank. In the case of line L6, every active cell with value $\ge v$ leaves, and there are at least $W - r + 1$ of them. In the case of line L8, every active cell with value $\le v$ leaves, and there are at least $r$ of them. If $W/4 \le r \le 3W/4 + 1$, at least $W/4$ cells leave in both cases. This occurs with probability at least $1/2$. So in expectation at most 2 rounds make $W$ drop by the factor $3/4$, and the expected number of rounds is at most $2 \log_{4/3} N + O(1)$. With $N \le n^2$, this is $O(\log n)$ rounds of cost $O(m + n)$ each.
