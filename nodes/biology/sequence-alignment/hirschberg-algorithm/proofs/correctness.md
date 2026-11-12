---
title: Hirschberg's algorithm returns an optimal global alignment
proves: [correctness]
status: full
---

Write $x(i_0, i_1]$ for $x_{i_0 + 1} \cdots x_{i_1}$, and $\operatorname{OPT}(u, v)$ for the largest score of a global alignment of the strings $u$ and $v$, with the score $s$ for a pair column and $-d$ for a gap column, $d \ge 0$. Write $u^R$ for the reverse of $u$.

**Lemma 1 (forward row).** LAST-ROW$(x(i_0, i_1], y(j_0, j_1], \text{forward})$ returns $r$ with $r[k] = \operatorname{OPT}(x(i_0, i_1], y(j_0, j_0 + k])$ for $0 \le k \le w$.

*Proof.* Let $F$ be the Needleman-Wunsch table of $x(i_0, i_1]$ against $y(j_0, j_1]$. We show by induction on $t$ that after pass $t$ of line L2 (and after line L1 for $t = 0$), $r[k] = F[t, k]$ for all $k$. Line L1 sets row 0, $F[0, k] = -kd$. In pass $t$, line L3 saves $F[t - 1, 0]$ in $diag$ and sets $r[0] = -td = F[t, 0]$. Before line L5 runs for column $k$, the cells $r[0..k - 1]$ hold row $t$, the cells $r[k..w]$ hold row $t - 1$, and $diag = F[t - 1, k - 1]$. So line L5 computes $\max(F[t - 1, k - 1] + s(a, b), F[t - 1, k] - d, F[t, k - 1] - d) = F[t, k]$, stores it in $r[k]$, and sets $diag$ to $F[t - 1, k]$, which keeps the invariant. After the last pass, $r[k] = F[i_1 - i_0, k]$, and the Needleman-Wunsch recurrence gives $F[i_1 - i_0, k] = \operatorname{OPT}(x(i_0, i_1], y(j_0, j_0 + k])$. $\square$

**Lemma 2 (reversal).** $\operatorname{OPT}(u, v) = \operatorname{OPT}(u^R, v^R)$.

*Proof.* Reversing the order of the columns of an alignment of $u$ and $v$ gives an alignment of $u^R$ and $v^R$ with the same columns, so with the same score. The map is its own inverse, so it is a bijection between the two sets of alignments, and the two maxima are equal. $\square$

**Lemma 3 (backward row).** LAST-ROW$(x(i_0, i_1], y(j_0, j_1], \text{backward})$ returns $r$ with $r[k] = \operatorname{OPT}(x(i_0, i_1], y(j_1 - k, j_1])$.

*Proof.* In the backward mode, pass $t$ reads $x_{i_1 - t + 1}$ and column $k$ reads $y_{j_1 - k + 1}$, so the procedure is the forward procedure on $x(i_0, i_1]^R$ and $y(j_0, j_1]^R$. By Lemma 1, $r[k]$ is the optimal score of $x(i_0, i_1]^R$ against the first $k$ letters of $y(j_0, j_1]^R$, which are $y(j_1 - k, j_1]^R$. By Lemma 2 this equals $\operatorname{OPT}(x(i_0, i_1], y(j_1 - k, j_1])$. $\square$

**Lemma 4 (split).** Let $i_0 \le mid \le i_1$ and $w = j_1 - j_0$. Then

$$\operatorname{OPT}(x(i_0, i_1], y(j_0, j_1]) = \max_{0 \le k \le w} \bigl(\operatorname{OPT}(x(i_0, mid], y(j_0, j_0 + k]) + \operatorname{OPT}(x(mid, i_1], y(j_0 + k, j_1])\bigr),$$

and for every $k$, an optimal alignment of the first pair followed by an optimal alignment of the second pair is an alignment of $x(i_0, i_1]$ and $y(j_0, j_1]$ with the score of the term for $k$.

*Proof.* ($\ge$) The concatenation of an alignment of $x(i_0, mid]$ with $y(j_0, j_0 + k]$ and an alignment of $x(mid, i_1]$ with $y(j_0 + k, j_1]$ is an alignment of the whole pieces, and its score is the sum of the two scores, because the score is a sum over columns. This also proves the second claim.

($\le$) Let $A$ be an optimal alignment of the whole pieces. Cut $A$ after the column that holds $x_{mid}$; if $mid = i_0$, cut before the first column that holds a letter of $x$, or at the end if there is none. The first part holds exactly the letters $x(i_0, mid]$ of $x$, and it holds a prefix $y(j_0, j_0 + k]$ of the $y$ piece for some $k$, because the columns keep the order of $y$. The second part holds $x(mid, i_1]$ and $y(j_0 + k, j_1]$. Each part is an alignment of its pair, so the score of $A$ is at most the term for this $k$. $\square$

**Lemma 5 (one letter).** Let $a$ be one letter and $v = v_1 \cdots v_w$ with $w \ge 1$. The best alignment of $a$ and $v$ is $a$ under a letter $v_j$ with the largest $s(a, v_j)$ and gaps against the other letters, if $s(a, v_j) > -2d$, and otherwise $(a, -)$ followed by gaps against all of $v$.

*Proof.* The letter $a$ is in one column. If that column is $(a, v_j)$, the other $w - 1$ letters of $v$ stand against gaps, and the score is $s(a, v_j) - (w - 1)d$, largest for the $v_j$ with the largest $s(a, v_j)$. If the column is $(a, -)$, all $w$ letters of $v$ stand against gaps, and the score is $-(w + 1)d$. All alignments of each kind have the same score, so the order of the columns does not matter. The first kind is better exactly when $s(a, v_j) - (w - 1)d > -(w + 1)d$, that is, $s(a, v_j) > -2d$; on a tie both are optimal. $\square$

**Theorem.** HIRSCHBERG$(i_0, i_1, j_0, j_1)$ returns an alignment of $x(i_0, i_1]$ and $y(j_0, j_1]$ with the score $\operatorname{OPT}(x(i_0, i_1], y(j_0, j_1])$. In particular, HIRSCHBERG$(0, m, 0, n)$ returns an optimal global alignment of $x$ and $y$.

*Proof.* By induction on $i_1 - i_0$.

*Line L7.* If one piece is empty, the only alignment puts the other piece against gaps, so it is optimal.

*Line L8.* If $i_1 - i_0 = 1$ and $w \ge 1$, the call returns the alignment of Lemma 5, which is optimal.

*Lines L9 to L13.* Now $i_1 - i_0 \ge 2$, so $i_0 < mid < i_1$, and both calls of line L13 have fewer rows than the current call. By Lemma 1, $f[k] = \operatorname{OPT}(x(i_0, mid], y(j_0, j_0 + k])$. By Lemma 3 with $w - k$, $b[w - k] = \operatorname{OPT}(x(mid, i_1], y(j_0 + k, j_1])$. So $f[k] + b[w - k]$ is the term for $k$ in Lemma 4, and line L12 picks a $k$ with the largest term, which by Lemma 4 equals $\operatorname{OPT}(x(i_0, i_1], y(j_0, j_1])$. By the induction hypothesis, the two calls of line L13 return optimal alignments of the two pairs for this $k$, and by the second claim of Lemma 4, their concatenation is an alignment of the whole pieces with this optimal score.

The implementation keeps the pending pairs on a stack and pops the left pair first, so it emits the columns of the two parts in the same order as line L13; the argument does not change. If the inputs were exchanged so that $x$ is the longer sequence, exchanging the two rows of every column back gives an alignment of the original pair with the same score, because the scores use $s(b, a)$ for the exchanged pair. $\blacksquare$
