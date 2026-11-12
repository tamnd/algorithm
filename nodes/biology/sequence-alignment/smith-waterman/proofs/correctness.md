---
title: Smith-Waterman returns an optimal local alignment
proves: [correctness]
status: full
---

Write $x[a..b]$ for $x_a \cdots x_b$, empty if $b < a$. The score of an alignment is $\sum s(a, b)$ over its pair columns minus $d$ for each gap column, with $d \ge 0$. The score is a sum over the columns. For $0 \le i \le m$ and $0 \le j \le n$, let $\mathcal{L}(i, j)$ be the set of alignments of $x[i' + 1..i]$ with $y[j' + 1..j]$ for some $0 \le i' \le i$ and $0 \le j' \le j$: the alignments of a suffix of $x[1..i]$ with a suffix of $y[1..j]$. The empty alignment is in every $\mathcal{L}(i, j)$. Let $L(i, j)$ be the largest score in $\mathcal{L}(i, j)$.

**Lemma 1 (the table).** After lines L1 to L7, $H[i, j] = L(i, j)$ for all cells.

*Proof.* By induction in the order in which the cells are filled.

*Border.* An alignment in $\mathcal{L}(i, 0)$ aligns a suffix of $x[1..i]$ of some length $k$ with the empty string, so it has $k$ gap columns and the score $-kd \le 0$. The empty suffix gives 0, so $L(i, 0) = 0$, the value of line L1. Line L2 is right for $L(0, j)$ in the same way.

*Inner cell, $\le$.* Let $i, j \ge 1$. By the induction hypothesis the three cells that line L6 reads hold $L$. Each term of line L6 is the score of an alignment in $\mathcal{L}(i, j)$. The term 0 is the empty alignment. For the second term, take an alignment of $x[i' + 1..i - 1]$ and $y[j' + 1..j - 1]$ with score $L(i - 1, j - 1)$ and add the column $(x_i, y_j)$; the result aligns $x[i' + 1..i]$ and $y[j' + 1..j]$, so it is in $\mathcal{L}(i, j)$. The third and fourth terms add $(x_i, -)$ to an alignment in $\mathcal{L}(i - 1, j)$ and $(-, y_j)$ to one in $\mathcal{L}(i, j - 1)$ in the same way. So $H[i, j] \le L(i, j)$.

*Inner cell, $\ge$.* Let $A \in \mathcal{L}(i, j)$ have the score $L(i, j)$, and let it align $u = x[i' + 1..i]$ and $v = y[j' + 1..j]$. If $A$ is empty, $S(A) = 0 \le H[i, j]$. Otherwise its last column holds the last letter of $u$ or the last letter of $v$, and these are $x_i$ and $y_j$. So the last column is $(x_i, y_j)$, $(x_i, -)$ or $(-, y_j)$. Remove it, and let $A'$ be the rest.

- For $(x_i, y_j)$: $A'$ aligns $x[i' + 1..i - 1]$ and $y[j' + 1..j - 1]$, so $A' \in \mathcal{L}(i - 1, j - 1)$ and $S(A) = S(A') + s(x_i, y_j) \le H[i - 1, j - 1] + s(x_i, y_j)$.
- For $(x_i, -)$: $A' \in \mathcal{L}(i - 1, j)$ and $S(A) \le H[i - 1, j] - d$.
- For $(-, y_j)$: $A' \in \mathcal{L}(i, j - 1)$ and $S(A) \le H[i, j - 1] - d$.

So $L(i, j) = S(A) \le H[i, j]$. $\square$

**Lemma 2 (the best cell).** After line L7, $best = \max_{i, j} H[i, j] = \operatorname{OPT}_{\mathrm{loc}}(x, y)$, and $H[b_i, b_j] = best$.

*Proof.* Line L3 starts with $best = 0 = H[0, 0]$, and line L7 runs once for each inner cell and keeps the largest value and its position. The border cells are 0. So $best$ is the maximum over all cells, and $H[b_i, b_j] = best$.

A local alignment aligns $x[i' + 1..i]$ with $y[j' + 1..j]$ for some $i' \le i$ and $j' \le j$, so it lies in $\mathcal{L}(i, j)$, and its score is at most $L(i, j) = H[i, j] \le best$. In the other direction, each $\mathcal{L}(i, j)$ is a set of local alignments, so $best = \max L(i, j) \le \operatorname{OPT}_{\mathrm{loc}}$. $\square$

**Lemma 3 (the traceback).** Each time line L9 tests its condition, these statements hold:

> **(T)** $0 \le i \le b_i$, $0 \le j \le b_j$; the list $A$ is an alignment of $x[i + 1..b_i]$ and $y[j + 1..b_j]$; and $H[i, j] + S(A) = best$.

*Proof.* Line L8 makes (T) true with $A$ empty, by Lemma 2.

Assume (T) and $H[i, j] > 0$. Then $i \ge 1$ and $j \ge 1$, because the border cells are 0. By line L6, $H[i, j]$ equals one of the four terms, and not the term 0, so it equals one of the other three. If the test of line L10 holds, the column $(x_i, y_j)$ in front of $A$ aligns $x[i..b_i]$ and $y[j..b_j]$, and $H[i - 1, j - 1] + S(A) + s(x_i, y_j) = H[i, j] + S(A) = best$, so (T) holds for the new values. The same holds for line L11 with $(x_i, -)$ and $-d$. If lines L10 and L11 fail, $H[i, j] = H[i, j - 1] - d$, and line L12 keeps (T) with $(-, y_j)$. $\square$

**Theorem.** SMITH-WATERMAN stops and returns $\operatorname{OPT}_{\mathrm{loc}}(x, y)$, substrings $x[i + 1..b_i]$ and $y[j + 1..b_j]$, and an alignment $A$ of these substrings with the score $\operatorname{OPT}_{\mathrm{loc}}(x, y)$.

*Proof.* Each pass of the loop of line L9 lowers $i + j$, and the loop stops at the latest at a border cell, which is 0. When it stops, $H[i, j] = 0$ (the cells are never negative, because of the term 0 of line L6). By (T), $A$ aligns $x[i + 1..b_i]$ and $y[j + 1..b_j]$, and $S(A) = best - 0 = best$, which is $\operatorname{OPT}_{\mathrm{loc}}(x, y)$ by Lemma 2. $\blacksquare$
