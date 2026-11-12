---
title: Needleman-Wunsch returns an optimal global alignment
proves: [correctness]
status: full
---

Write $x[1..i]$ for $x_1 \cdots x_i$, and $\operatorname{OPT}(i, j)$ for the largest score of an alignment of $x[1..i]$ and $y[1..j]$. The score of an alignment is $\sum s(a, b)$ over its pair columns minus $d$ for each gap column. So the score is a sum over the columns, and the score of a concatenation of two alignments is the sum of their scores.

**Lemma 1 (the table).** After lines L1 to L6, $F[i, j] = \operatorname{OPT}(i, j)$ for all $0 \le i \le m$ and $0 \le j \le n$.

*Proof.* By induction over the cells in the order in which they are filled: the border by lines L1 to L3, then the rows $i = 1, \ldots, m$, each from $j = 1$ to $n$.

*Border.* The empty string and $y[1..j]$ have exactly one alignment, $j$ columns $(-, y_k)$, with score $-jd$. This is the value of line L3, and line L1 for $j = 0$. In the same way, line L2 is right for $F[i, 0]$.

*Inner cell.* Let $i, j \ge 1$. When line L6 fills $F[i, j]$, the cells $F[i - 1, j - 1]$, $F[i - 1, j]$ and $F[i, j - 1]$ are already filled, and by the induction hypothesis they hold $\operatorname{OPT}$.

($\le$) Each term of line L6 is the score of an alignment of $x[1..i]$ and $y[1..j]$. For the first term, take an optimal alignment of $x[1..i - 1]$ and $y[1..j - 1]$ and add the column $(x_i, y_j)$; its score is $\operatorname{OPT}(i - 1, j - 1) + s(x_i, y_j)$. The other two terms add $(x_i, -)$ or $(-, y_j)$ in the same way. So $F[i, j] \le \operatorname{OPT}(i, j)$.

($\ge$) Let $A$ be an optimal alignment of $x[1..i]$ and $y[1..j]$. Its last column holds $x_i$ or $y_j$ or both, because the last letter of the top row is $x_i$ and that of the bottom row is $y_j$ when the gap symbols are removed, and no column is $(-, -)$. So the last column is $(x_i, y_j)$, $(x_i, -)$ or $(-, y_j)$. Remove it, and let $A'$ be the rest.

- If it is $(x_i, y_j)$, then $A'$ aligns $x[1..i - 1]$ and $y[1..j - 1]$, so $S(A) = S(A') + s(x_i, y_j) \le F[i - 1, j - 1] + s(x_i, y_j)$.
- If it is $(x_i, -)$, then $A'$ aligns $x[1..i - 1]$ and $y[1..j]$, so $S(A) = S(A') - d \le F[i - 1, j] - d$.
- If it is $(-, y_j)$, then $S(A) \le F[i, j - 1] - d$ in the same way.

In each case $S(A)$ is at most one term of line L6, so $\operatorname{OPT}(i, j) = S(A) \le F[i, j]$. $\square$

**Lemma 2 (the traceback).** Let $A$ be the list of columns built so far. Each time line L8 tests its condition, these statements hold:

> **(T)** $0 \le i \le m$ and $0 \le j \le n$; $A$ is an alignment of $x[i + 1..m]$ and $y[j + 1..n]$; and $F[i, j] + S(A) = F[m, n]$.

*Proof.* Line L7 makes (T) true with $A$ empty and $(i, j) = (m, n)$.

Assume (T) and $i > 0$ or $j > 0$. If line L9 runs, $F[i, j] = F[i - 1, j - 1] + s(x_i, y_j)$; the new list is $(x_i, y_j)$ in front of $A$, which aligns $x[i..m]$ and $y[j..n]$, and its score is $S(A) + s(x_i, y_j)$. So $F[i - 1, j - 1] + S(A) + s(x_i, y_j) = F[i, j] + S(A) = F[m, n]$, and (T) holds for the new values. Line L10 is the same with the column $(x_i, -)$ and the term $-d$.

If line L11 runs, the tests of lines L9 and L10 failed. If $i = 0$, then $j > 0$ and $F[0, j] = F[0, j - 1] - d$ by line L3. If $i > 0$ and $j = 0$, then $F[i, 0] = F[i - 1, 0] - d$ by line L2, so line L10 would have run; this case does not occur. If $i > 0$ and $j > 0$, line L6 set $F[i, j]$ to one of its three terms, and the first two do not hold, so $F[i, j] = F[i, j - 1] - d$. In each case $j > 0$ and $F[i, j] = F[i, j - 1] - d$, so the column $(-, y_j)$ keeps (T) as before. $\square$

**Theorem.** NEEDLEMAN-WUNSCH stops, and it returns $\operatorname{OPT}(m, n)$ and an alignment of $x$ and $y$ with this score.

*Proof.* Each pass of the loop of line L8 lowers $i + j$ by 1 or 2, and $i, j \ge 0$ by (T), so the loop stops after at most $m + n$ passes. It stops when $i = j = 0$. Then (T) says that $A$ aligns $x[1..m]$ and $y[1..n]$ and that $S(A) = F[m, n] - F[0, 0] = F[m, n]$. By Lemma 1, $F[m, n] = \operatorname{OPT}(m, n)$, so $A$ is optimal. $\blacksquare$
