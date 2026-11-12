---
title: The semi-global DP returns an optimal semi-global alignment
proves: [correctness]
status: full
---

Write $x[a..b]$ for $x_a \cdots x_b$, empty if $b < a$, and assume $d \ge 0$. In an alignment, a gap column $(x_k, -)$ is *leading* if it comes before every column that holds a letter of $y$, and *trailing* if it comes after every such column; the same holds for a gap column $(-, y_l)$ and the letters of $x$. If the alignment holds no letter of $y$, every gap column $(x_k, -)$ is both leading and trailing.

The semi-global score $S_F(A)$ of an alignment $A$ of $x$ and $y$ counts $s(a, b)$ for each pair column and $-d$ for each charged gap column. A gap column $(x_k, -)$ is free if it is leading and $P_x$ holds, or trailing and $S_x$ holds; a gap column $(-, y_l)$ is free if it is leading and $P_y$ holds, or trailing and $S_y$ holds.

For an alignment $B$ of $x[1..i]$ and $y[1..j]$, the *prefix score* $S_P(B)$ counts $s(a, b)$ for each pair column and $-d$ for each gap column, except that a column $(x_k, -)$ that is leading in $B$ is free if $P_x$ holds, and a column $(-, y_l)$ that is leading in $B$ is free if $P_y$ holds. Let $\operatorname{OPT}_P(i, j)$ be the largest prefix score of an alignment of $x[1..i]$ and $y[1..j]$.

**Lemma 1 (the table).** After lines L1 to L6, $F[i, j] = \operatorname{OPT}_P(i, j)$ for all cells.

*Proof.* By induction in the order in which the cells are filled.

*Border.* The only alignment of $x[1..i]$ with the empty string has $i$ columns $(x_k, -)$, all leading, so its prefix score is 0 if $P_x$ holds and $-id$ otherwise. This is line L2 (and line L1 for $i = 0$). Line L3 is right in the same way.

*Inner cell.* Let $i, j \ge 1$, and let $B$ align $x[1..i]$ and $y[1..j]$, with last column $c$ and the rest $B'$. The column $c$ is $(x_i, y_j)$, $(x_i, -)$ or $(-, y_j)$, because it holds the last letter of $x[1..i]$ or of $y[1..j]$. If $c = (x_i, -)$, it is not leading, because $y_j$ stands in an earlier column; so $c$ is charged. In the same way, $c = (-, y_j)$ is charged.

Removing $c$ does not change which columns of $B'$ are leading. Take a column $(x_k, -)$ of $B'$. If $c$ holds no letter of $y$, the first column with a letter of $y$ is the same in $B$ and in $B'$. If $c$ holds $y_j$ with $j \ge 2$, the first column with a letter of $y$ holds $y_1$ and lies in $B'$. If $c$ holds $y_1$, every column of $B'$ comes before it, so $(x_k, -)$ is leading in $B$; it is also leading in $B'$, which holds no letter of $y$. The same holds for the columns $(-, y_l)$ with the roles of $x$ and $y$ exchanged.

So $S_P(B) = S_P(B') + w(c)$, where $w(c)$ is $s(x_i, y_j)$ for a pair and $-d$ for a gap. Each term of line L6 is the prefix score of an optimal alignment of smaller prefixes plus one column, so $F[i, j] \le \operatorname{OPT}_P(i, j)$. For an optimal $B$, $\operatorname{OPT}_P(i, j) = S_P(B') + w(c)$ is at most the term of line L6 for the kind of $c$, by the induction hypothesis, so $\operatorname{OPT}_P(i, j) \le F[i, j]$. $\square$

**Lemma 2 (the end set).** Let $E$ be the set of line L7. Then $\max_A S_F(A) = \max_{(i, j) \in E} F[i, j]$, where $A$ runs over the alignments of $x$ and $y$. Moreover, for $(i, j) \in E$ and any alignment $B$ of $x[1..i]$ and $y[1..j]$, the alignment $A = BT$, with $T$ the tail columns of line L8, satisfies $S_F(A) \ge S_P(B)$.

*Proof.* *The tail.* Let $(i, j) \in E$ and let $T$ be the columns $(x_{i+1}, -), \ldots, (x_m, -)$ followed by $(-, y_{j+1}), \ldots, (-, y_n)$. Since $(i, j) \in E$, $i = m$ or $j = n$, so one of the two lists is empty. If $j = n$ and $i < m$, the cell came from the part of line L7 for $S_x$, so $S_x$ holds; the columns of $T$ come after all letters of $y$, so they are trailing and free. The case $i = m$, $j < n$ is the same with $S_y$. So $T$ is free in $S_F$.

*Lower bound.* Let $(i, j) \in E$, let $B$ align $x[1..i]$ and $y[1..j]$, and let $A = BT$. A column of $B$ that is leading in $B$ is leading in $A$, because $T$ comes after it. So every column that $S_P$ frees in $B$ is also free in $S_F$, and $T$ is free, so $S_F(A) \ge S_P(B)$. With $B$ optimal, Lemma 1 gives $S_F(A) \ge F[i, j]$.

*Upper bound.* Let $A$ be any alignment of $x$ and $y$. Let $T$ be the longest run of columns at the end of $A$ that are trailing gap columns freed by $S_x$ or $S_y$, and let $B$ be the rest of $A$. A trailing $(x_k, -)$ and a trailing $(-, y_l)$ cannot both occur, since each would have to come after the other; so $T$ holds columns of one kind. If $T$ is empty, $B = A$ ends at $(m, n) \in E$. If $T$ holds columns $(x_k, -)$, they come after all letters of $y$, so $B$ aligns $x[1..i]$ with all of $y$ for some $i$, and $S_x$ holds, so $(i, n) \in E$. The other kind is the same with $S_y$. So $B$ aligns the prefixes of a cell $(i, j) \in E$.

Compare the columns of $B$ under $S_F$ and under $S_P$. Pair columns score the same. Suppose $S_F$ frees a gap column $c$ of $B$. If $c$ is leading in $A$, it is leading in $B$, because $B$ holds fewer letters, and $S_P$ frees it by the same flag. If $c$ is trailing in $A$ and freed by $S_x$ (say $c = (x_k, -)$), then no column after $c$ holds a letter of $y$, so every column after $c$ is a trailing $(x_{k'}, -)$, freed by $S_x$. Then $c$ and all columns after it form a run of freed trailing columns at the end of $A$ that is longer than $T$, which contradicts the choice of $T$. So $S_P$ frees every column of $B$ that $S_F$ frees, and $S_F(A) \le S_P(B) \le F[i, j]$ by Lemma 1.

The two bounds give $\max_A S_F(A) = \max_{E} F$. $\square$

**Lemma 3 (the traceback).** Let $(e_i, e_j)$ be the cell of line L8. Each time line L9 tests its condition, the columns that the loop has put in front of $T$ form an alignment $C$ of $x[i + 1..e_i]$ and $y[j + 1..e_j]$, and $F[i, j] + W(C) = F[e_i, e_j]$, where $W(C)$ is the sum of $s(a, b)$ over the pair columns of $C$ minus $d$ for each gap column of $C$.

*Proof.* At the start $C$ is empty and $(i, j) = (e_i, e_j)$. While $i, j \ge 1$, line L6 set $F[i, j]$ to one of its three terms. Line L10 or L11 takes a step whose term holds; if both fail, the third term holds, and line L12 takes it. The step adds its column to $C$ and keeps the equation, as in the proof for Needleman-Wunsch. $\square$

**Theorem.** SEMI-GLOBAL-DP returns $\max_A S_F(A)$ and an alignment of $x$ and $y$ with this semi-global score.

*Proof.* The loop of line L9 lowers $i + j$ in each pass and stops when $i = 0$ or $j = 0$. Line L13 puts the head $H$ in front: $x[1..i]$ against gaps, or gaps against $y[1..j]$; at most one is not empty. The columns of $H$ are leading in $HC$, so by line L2 or L3, $S_P(H) = F[i, j]$ also inside $HC$.

No gap column of $C$ is leading in $HC$. The first column of $C$ came from a cell $(i', j')$ with $i', j' \ge 1$. If it is $(x_{i'}, -)$, the loop stopped at $(i' - 1, j')$ with $i' = 1$, so $H$ holds $y[1..j']$ with $j' \ge 1$, and these letters come before it. If it is $(-, y_{j'})$, then $j' = 1$ and $H$ holds $x[1..i']$ with $i' \ge 1$. A later gap column of $C$ has letters of both sequences before it. So $S_P(HC) = S_P(H) + W(C) = F[i, j] + W(C) = F[e_i, e_j]$ by Lemma 3.

The returned alignment is $A = HCT$, and $B = HC$ aligns $x[1..e_i]$ and $y[1..e_j]$. By the lower bound of Lemma 2, $S_F(A) \ge S_P(B) = F[e_i, e_j]$. Line L8 chose $(e_i, e_j)$ with the largest $F$ in $E$, so by Lemma 2, $F[e_i, e_j] = \max_{A'} S_F(A') \ge S_F(A)$. Hence $S_F(A) = F[e_i, e_j] = \max_{A'} S_F(A')$, the value that line L14 returns. $\blacksquare$
