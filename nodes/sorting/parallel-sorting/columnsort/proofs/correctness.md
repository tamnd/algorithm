---
title: Columnsort sorts when r ≥ 2s² and s divides r
proves: [correctness]
status: full
---

This proof shows the sufficient condition $r \ge 2s^2$ with $s \mid r$. Leighton's paper proves the sharper condition $r \ge 2(s-1)^2$ by a finer count of the mixed stretch in Lemma 3.

Index the matrix as $M[i][k]$ with row $i \in [0, r)$ and column $k \in [0, s)$. The *column-major index* of $M[i][k]$ is $kr + i$ and its *row-major index* is $is + k$.

## Reduction to zeros and ones

A column sort is a sequence of compare-exchanges, and lines L2, L4, L6 and L8 move keys by fixed permutations, with fixed $\pm\infty$ keys added on line L6 and removed on line L8. A compare-exchange commutes with every non-decreasing map $f$ on keys, and so does a fixed permutation, and $f$ can be extended to $\pm\infty$ by $f(\pm\infty) = \pm\infty$. So columnsort commutes with $f$. By the argument of the [zero-one principle](/zero-one-principle/), if columnsort sorts every 0-1 matrix, it sorts every matrix. From now on the keys are zeros and ones, with $-\infty$ treated as $0$ and $+\infty$ as $1$.

## Lemma 1. After line L2, column zero counts are monotone and close

Let $z_j$ be the number of zeros in column $j$ after line L1, and let $Z_k$ be the number of zeros in column $k$ after line L2. Then $Z_0 \ge Z_1 \ge \cdots \ge Z_{s-1} \ge Z_0 - s$.

*Proof.* After line L1, column $j$ is $z_j$ zeros and then ones. Line L2 sends the key with column-major index $t$ to the cell with row-major index $t$, that is, to column $t \bmod s$. The keys of column $j$ have column-major indices $jr, \ldots, jr + r - 1$, and since $s \mid r$, the key at offset $u$ in column $j$ goes to column $u \bmod s$. Its zeros are at offsets $u = 0, \ldots, z_j - 1$, so column $k$ gets $\lfloor z_j / s \rfloor + [k < z_j \bmod s]$ zeros from column $j$. Summing over $j$,

$$Z_k = \sum_j \lfloor z_j / s \rfloor + \#\{\, j : k < z_j \bmod s \,\}.$$

The second term does not increase with $k$, and it is between $0$ and $s$. $\square$

## Lemma 2. After line L3, at most s rows are mixed

*Proof.* After line L3, column $k$ has zeros in rows $0, \ldots, Z_k - 1$ and ones below. By Lemma 1, row $i$ is all zeros when $i < Z_{s-1}$, all ones when $i \ge Z_0$, and mixed only when $Z_{s-1} \le i < Z_0$. There are $Z_0 - Z_{s-1} \le s$ such rows. $\square$

## Lemma 3. After line L5, the mixed stretch has at most s² keys and spans two columns

*Proof.* By Lemma 2, in row-major order after line L3, all keys before row-major index $Z_{s-1} s$ are zeros and all keys from index $Z_0 s$ on are ones. Call the indices between them the mixed stretch. It has at most $s^2$ indices. Line L4 sends the key with row-major index $t$ to the cell with column-major index $t$, so after line L4, in column-major order, the matrix is zeros, then a stretch $I$ of at most $s^2$ indices, then ones.

Since $s^2 \le r/2 < r$, the stretch $I$ meets at most two columns, say columns $a$ and $a + 1$. Line L5 sorts each column. Columns before $a$ and after $a + 1$ are clean, and clean columns stay clean. If $I$ lies in one column, that column is now sorted, and the whole matrix is sorted in column-major order. Otherwise, column $a$ becomes zeros followed by $e$ ones, and column $a + 1$ becomes $b$ zeros followed by ones, where $e$ and $b$ are at most the sizes of the parts of $I$ in these columns. So $e \le s^2$ and $b \le s^2$, and in column-major order the matrix is

$$0 \cdots 0 \; \underbrace{1 \cdots 1}_{e} \; \underbrace{0 \cdots 0}_{b} \; 1 \cdots 1,$$

with the boundary between the two runs at column-major index $(a+1) r$. $\square$

## Lemma 4. Lines L6 to L8 sort the column-major order

*Proof.* In column-major order, the shifted matrix is $\lfloor r/2 \rfloor$ keys $-\infty$, then $M$ in column-major order, then $\lceil r/2 \rceil$ keys $+\infty$. So column $k'$ of the shifted matrix holds the keys of $M$ with column-major indices in $[k' r - \lfloor r/2 \rfloor, (k'+1) r - \lfloor r/2 \rfloor)$, together with padding at the two ends. Line L7 sorts each such window, and line L8 puts the keys back at their column-major indices.

If $M$ is already sorted in column-major order, each window is sorted, and nothing changes. Otherwise $M$ has the form of Lemma 3. The window with $k' = a + 1$ is $[(a+1)r - \lfloor r/2 \rfloor, (a+2)r - \lfloor r/2 \rfloor)$. It contains the $e$ ones before index $(a+1)r$ because $e \le s^2 \le \lfloor r/2 \rfloor$, and the $b$ zeros from index $(a+1)r$ on because $b \le s^2 \le \lceil r/2 \rceil$. All keys of $M$ before this window are zeros and all keys after it are ones. Sorting the window makes the column-major order zeros followed by ones. The other windows are sorted already, as are the padding keys, since all $-\infty$ keys come first and all $+\infty$ keys last. $\square$

## Theorem

If $s \mid r$ and $r \ge 2s^2$, columnsort sorts every $r \times s$ matrix into column-major order.

*Proof.* The condition gives $s^2 \le \lfloor r/2 \rfloor$, which Lemmas 3 and 4 use. By Lemmas 1 to 4, columnsort sorts every 0-1 matrix, and by the reduction it sorts every matrix. $\square$
