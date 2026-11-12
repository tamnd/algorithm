---
title: The Sankoff recursion computes the best joint alignment and structure
proves: [correctness]
status: full
---

We use the names and line numbers of the pseudocode on the page. Indices are 0-based and intervals are half-open.

**Solutions.** For $0 \le i \le j \le m$ and $0 \le k \le l \le n$, a solution for $(i, j, k, l)$ is a sequence of columns and a set $P$ of pairs of columns such that:

1. each column is $(x_p, y_r)$, a match column, or $(x_p, -)$, or $(-, y_r)$;
2. reading the columns from left to right, the $x$ entries spell $x[i:j)$ and the $y$ entries spell $y[k:l)$;
3. each pair in $P$ joins two match columns $(x_p, y_r)$ and $(x_{p'}, y_{r'})$ that come in this order, with $x_p x_{p'}$ and $y_r y_{r'}$ allowed pairs, $p' - p - 1 \ge h_{\min}$ and $r' - r - 1 \ge h_{\min}$;
4. each column is in at most one pair, and pairs are nested: for two pairs on columns $a < b$ and $a' < b'$, it is not the case that $a < a' < b < b'$.

Its score is the sum of $\sigma$ over match columns, minus $d$ for each other column, plus $\beta$ for each pair. Let $\mathrm{OPT}(i, j, k, l)$ be the largest score of a solution. There are finitely many solutions and at least one (all bases against gaps), so the maximum exists.

**Lemma 1 (order).** When line L12 sets $D[i, j, k, l]$, every cell that lines L6 to L11 read has already been set.

*Proof.* The cells read are $D[i+1, j, k, l]$, $D[i+1, j, k+1, l]$, $D[i+1, h, k+1, q]$ and $D[h+1, j, q+1, l]$, whose $x$ interval is shorter than $s = j - i$, and $D[i, j, k+1, l]$, whose $x$ interval has length $s$ and whose $y$ interval is shorter than $t = l - k$. Line L1 runs $s$ upwards and line L2 runs $t$ upwards inside it, so all of these cells belong to earlier iterations. $\square$

**Lemma 2 (decomposition).** Let $i < j$ and $k < l$. Every solution for $(i, j, k, l)$ has a first column of exactly one of these kinds, and its score is as stated:

- (a) $(x_i, -)$: the rest is a solution for $(i+1, j, k, l)$, and the score is the score of the rest minus $d$;
- (b) $(-, y_k)$: the rest is a solution for $(i, j, k+1, l)$, and the score is the score of the rest minus $d$;
- (c) $(x_i, y_k)$ in no pair: the rest is a solution for $(i+1, j, k+1, l)$, and the score is the score of the rest plus $\sigma(x_i, y_k)$;
- (d) $(x_i, y_k)$ paired with a later column $(x_h, y_q)$: then $x_i x_h$ and $y_k y_q$ are allowed pairs, $h \ge i + h_{\min} + 1$, $q \ge k + h_{\min} + 1$, $h < j$ and $q < l$; the columns strictly between the two paired columns form a solution $S_1$ for $(i+1, h, k+1, q)$, the columns after the second one form a solution $S_2$ for $(h+1, j, q+1, l)$, and the score is $\sigma(x_i, y_k) + \sigma(x_h, y_q) + \beta + \mathrm{score}(S_1) + \mathrm{score}(S_2)$.

Conversely, each of these constructions from solutions of the smaller subproblems, with the side conditions of (d), is a solution for $(i, j, k, l)$ with the stated score.

*Proof.* By condition 2 the first column contains $x_i$, or $y_k$, or both, which gives the four kinds; (c) and (d) differ by whether the column is in a pair, and it can be only the left column of a pair because it is the first column. In cases (a) to (c), removing the first column leaves columns that spell the shorter intervals, and every pair of $P$ is among the remaining columns, so conditions 1 to 4 still hold.

In case (d), let the first column be column $a$ and its partner column $b$. By condition 3, $b$ is a match column $(x_h, y_q)$ with the allowed pairs and the hairpin conditions stated, and $h < j$, $q < l$ because the columns spell $x[i:j)$ and $y[k:l)$. The columns strictly between $a$ and $b$ spell $x[i+1:h)$ and $y[k+1:q)$, and the columns after $b$ spell $x[h+1:j)$ and $y[q+1:l)$. Take any other pair of $P$ on columns $a' < b'$. Neither of them is $a$ or $b$ by condition 4. If one of them were between $a$ and $b$ and the other after $b$, we would have $a < a' < b < b'$, which nesting forbids. So every other pair lies wholly between $a$ and $b$ or wholly after $b$. Hence the two parts with the pairs inside them satisfy conditions 1 to 4 for their subproblems; the hairpin rule of each pair refers only to its own bases, so it carries over. The score adds over columns and pairs, which gives the formula.

For the converse, put the stated columns in the stated order. They spell the right intervals. The pairs of $S_1$ and $S_2$ are nested inside their parts, and the new pair encloses all pairs of $S_1$ and is disjoint from those of $S_2$, so nesting holds; the new pair meets condition 3 by the side conditions. The score is again the sum. $\square$

**Theorem.** For all $(i, j, k, l)$, after the loops, $D[i, j, k, l] = \mathrm{OPT}(i, j, k, l)$. In particular SANKOFF returns $\mathrm{OPT}(0, m, 0, n)$.

*Proof.* By induction on the order of the loops, which by Lemma 1 sets each cell after the cells it reads.

*Base.* If $i = j$ or $k = l$, a solution has no match column, because one side has no bases, so it has no pairs, and its columns are the $s + t$ bases of the other side against gaps. Its score is $-d(s + t)$, which line L5 stores.

*Step.* Let $i < j$ and $k < l$, and assume the claim for every cell read by lines L6 to L11. Lines L6 to L8 compute the best scores of cases (a), (b) and (c) of Lemma 2: by the converse part each value is reached by a solution, and by the first part no solution of that case is better, because its rest is a solution of the smaller subproblem with score at most its $D$ value. Lines L9 to L11 run over exactly the pairs $(h, q)$ allowed by the side conditions of case (d), and for each one add the best scores of the two parts; the score of case (d) is a sum of two independent terms, so it is largest when each part is optimal, and the two optimal parts combine into a solution by the converse part. So after line L11, $\mathit{best}$ is the largest score over all four cases, which by Lemma 2 cover every solution. Line L12 stores it. $\blacksquare$

**Traceback.** Start from $(0, m, 0, n)$. For a cell, find a case of lines L6 to L11 whose value equals $D[i, j, k, l]$; one exists because the cell is the maximum of these values. Output its column or columns and continue in the order of Lemma 2 with the subproblems it names. By the converse part of Lemma 2, the output is a solution, and its score is $D[0, m, 0, n]$ by the same sums.

**Cost.** Each cell does $O(1)$ work in lines L5 to L8 and L12, and at most $(j - i)(l - k)$ evaluations of line L11. Summed over all $\binom{m+2}{2}\binom{n+2}{2}$ cells this is $O(m^3 n^3)$ time, and the table is the $\Theta(m^2 n^2)$ space.
