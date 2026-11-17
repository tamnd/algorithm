---
title: Wraparound dynamic programming and the sum of heads law are computed exactly
proves: [correctness]
status: full
---

The finder has two parts. The detection part (lines L1 to L6 of the main pseudocode) is a filter that chooses candidates by a statistical test; it has no guarantee to find every repeat, and the page treats it as a heuristic. This file proves the two exact parts that the finder relies on: the wraparound dynamic program (WDP, lines W1 to W7) gives the best local alignment of a text with any number of tandem copies of a pattern, and the threshold of line L6 is the stated quantile of the exact law of the sum of heads.

## Wraparound dynamic programming

Let $P = p_1 \ldots p_d$ be the pattern and $T = t_1 \ldots t_n$ the text. Let $P^\infty$ be the infinite string $p_1 \ldots p_d p_1 \ldots p_d \ldots$, and write the position $q$ of $P^\infty$ as having *phase* $((q - 1) \bmod d) + 1$. A *wraparound alignment* is a global alignment of a substring $T[a+1 \ldots b]$ with a substring of $P^\infty$. Its score adds $+\mu$ for a column with two equal letters, $-\sigma$ for a column with two different letters and $-\delta$ for a column with a gap, where $\mu, \sigma, \delta > 0$. The empty alignment has score 0.

For $0 \le x \le n$ and $1 \le j \le d$, let $V^*(x, j)$ be the largest score of a wraparound alignment that is empty, or that ends with text position $x$ (the last text letter used is $t_x$, or no text letter is used and $x$ is the point before $t_{x+1}$) and with a pattern letter of phase $j$ (the last pattern letter used has phase $j$). Every non-empty alignment ends with a text letter or a pattern letter or both, so this is well defined if we also allow alignments with no text letter, which only have gap columns and negative scores. Write $j^- = j - 1$ for $j > 1$ and $1^- = d$, and $s(t, p) = \mu$ if $t = p$ and $-\sigma$ otherwise.

**Lemma 1 (recurrence).** $V^*(0, j) = 0$, and for $x \ge 1$,
$$V^*(x, j) = \max\big(0,\; V^*(x - 1, j^-) + s(t_x, p_j),\; V^*(x - 1, j) - \delta,\; V^*(x, j^-) - \delta\big).$$

*Proof.* Look at the last column of a best non-empty alignment counted in $V^*(x, j)$. If it pairs $t_x$ with a letter of phase $j$, the rest is an alignment that ends at $x - 1$ and phase $j^-$, or is empty. If it pairs $t_x$ with a gap, the rest ends at $x - 1$ with the same last pattern phase $j$. If it pairs a letter of phase $j$ with a gap, the rest ends at $x$ and phase $j^-$. In each case the rest is counted by the term named, and the converse holds by appending the column. The empty alignment gives 0, and so does the case where the rest is empty. With $x = 0$ only gap columns of the pattern are possible, which score below 0. $\square$

The term $V^*(x, j^-)$ is in the same row, and for $j = 1$ it is $V^*(x, d)$, so row $x$ is a cyclic system. Fix $x \ge 1$, and let $A_j = \max(0, V^*(x - 1, j^-) + s(t_x, p_j), V^*(x - 1, j) - \delta)$, the part that uses row $x - 1$ only. Indices of $A$ are taken modulo $d$ in $\{1, \ldots, d\}$.

**Lemma 2 (solution of a row).** $V^*(x, j) = \max_{0 \le r < d} (A_{j - r} - r\delta)$.

*Proof.* By Lemma 1, $V^*(x, j) = \max(A_j, V^*(x, j^-) - \delta)$. Unrolling this $r$ times gives $V^*(x, j) \ge A_{j - r} - r\delta$ for every $r \ge 0$. For the other direction, follow from $(x, j)$ the term that reaches the maximum: either it is $A_j$, or we step to $j^-$ and pay $\delta$. The walk cannot go round the row: after $d$ steps it would be back at $j$ with $V^*(x, j) = V^*(x, j) - d\delta$, which is false because $\delta > 0$. So it stops after some $r < d$ steps at an index where $A$ reaches the maximum, and $V^*(x, j) = A_{j - r} - r\delta$. $\square$

**Lemma 3 (two passes).** Lines W3 to W5 set row $x$ to $V^*(x, \cdot)$.

*Proof.* Line W3 computes $F_j = \max(A_j, F_{j-1} - \delta)$ for $j = 1, \ldots, d$, where $F_0$ is the value 0 that the new row holds in column 0 at that time. Since $A_1 \ge 0 > 0 - \delta$, $F_1 = A_1$, and by induction $F_j = \max_{0 \le r < j} (A_{j - r} - r\delta)$, the chains that do not cross column 1 going left. Line W4 sets column 0 to $F_d$. Line W5 computes $S_j = \max(F_j, S_{j-1} - \delta)$ with $S_0 = F_d$. Unrolling, $S_j = \max(F_j, F_{j-1} - \delta, \ldots, F_1 - (j - 1)\delta, F_d - j\delta)$. Each $F_{j - i} - i\delta$ is at most $F_j$ by the definition of $F$, so $S_j = \max(F_j, F_d - j\delta)$. The term $F_j$ covers the chains with $r < j$, and $F_d - j\delta = \max_{0 \le r < d} (A_{d - r} - (r + j)\delta)$ covers the chains of length $r + j$ that start at index $d - r \equiv j - (r + j)$, that is all lengths from $j$ to $d + j - 1$. Together they cover all lengths below $d$, and the longer ones are at most the value of a shorter chain with the same start, as in Lemma 2. So $S_j = V^*(x, j)$ by Lemma 2.

The loop of line W5 stops at the first $j$ with $S_{j-1} - \delta \le F_j$. Then $S_j = F_j$, and for every later $j'$, $S_{j'-1} - \delta = F_{j'-1} - \delta \le F_{j'}$ by the definition of $F$, so $S_{j'} = F_{j'}$, which is the value already stored. $\square$

By induction on $x$, the whole table is $V^*$, and the best score of line W6 is $\max_{x, j} V^*(x, j)$, the best wraparound alignment.

**Theorem 1 (equivalence with copies).** For $M \ge 2n/d + 3$, the best wraparound alignment score of $T$ and $P$ equals the best local alignment score (Smith-Waterman with the same scores and linear gaps) of $T$ and the finite string $P^M$.

*Proof.* A local alignment of $T$ and $P^M$ aligns a substring of $T$ with a substring of $P^M$, which is a substring of $P^\infty$, so it is a wraparound alignment with the same score. Conversely, take a best wraparound alignment, with score $V \ge 0$. If it is empty, both sides are 0. Otherwise it uses $u \le n$ text letters, $e$ deletions and at most $u$ other pattern letters. All columns score at most $\mu$, so its score is at most $u\mu - e\delta$, and a best alignment has a non-negative score, so $e \le u\mu/\delta$. With $\mu = 2$ and $\delta = 7$, as in the code and the test, $e \le 2u/7$. It uses at most $u + e < 2n$ letters of $P^\infty$, which fit inside $P^M$ from any starting phase when $Md \ge 2n + d$. So it is a local alignment of $T$ and $P^M$. $\square$

**Lemma 4 (traceback).** Line W7 returns an alignment whose score is the best score.

*Proof.* From a cell with value $v > 0$, at least one of the three moves of Lemma 1 has a predecessor whose value plus the column score is $v$, because $v$ is the maximum of those terms or of 0, and it is not 0. Each move appends the matching column, so the sum of the column scores from the stop cell to the start cell is $v$ minus the value of the stop cell, which is 0. The walk stops: the diagonal and up moves lower $x$, and a run of left moves in one row cannot go round the row, by the argument of Lemma 2. $\square$

## The sum of heads law

Let $h_1, \ldots, h_w$ be independent with $P(h_i = 1) = p$. A position $i$ with $h_i = 1$ is a *head*. The statistic $C$ counts the heads that lie in a maximal run of at least $k$ consecutive heads. In a window of $w$ positions of a tandem repeat with period $d$, $h_i = 1$ means that the base at position $i$ equals the base $d$ positions before it. A $k$-tuple match at distance $d$ is a run of $k$ heads, so the union of the matched tuples that lie in the window covers exactly the heads counted by $C$. The model assumes that the heads are independent with probability $p_M$, which is Benson's model of an alignment of two copies.

**Lemma 5.** The function `heads_distribution(w, k, p)` returns the law of $C$.

*Proof.* Scan the positions from left to right, and keep the state $(r, c)$, where $r$ is the length of the current run of heads, capped at $k$, and $c$ is the number of heads counted so far. A tail sets $r = 0$. A head with $r + 1 < k$ sets $r \leftarrow r + 1$ and counts nothing yet. A head with $r + 1 = k$ completes a run of $k$, so all $k$ heads of the run are counted: $c \leftarrow c + k$ and $r = k$. A head with $r = k$ extends a counted run: $c \leftarrow c + 1$. A run that ends with fewer than $k$ heads is never counted. So after the last position $c = C$. The states form a Markov chain with the transition probabilities $p$ and $1 - p$, and the code applies them $w$ times to the start state $(0, 0)$ and sums over $r$. $\square$

**Corollary.** `sum_of_heads_threshold(w, k, p, alpha)` returns the largest $c \le w$ with $P(C < c) \le \alpha$. So a window of a true repeat whose heads follow the model passes the test $C \ge c$ of line L6 with probability at least $1 - \alpha$. This is a statement about one window under the model; it does not say that the finder reports every repeat, and real repeats with indels or with mutations that cluster do not follow the model.

## What the finder returns

Each report comes from line L10 after the WDP of a final pattern $P'$ of length $d$ in a window $s[\mathit{lo}, \mathit{hi})$. By Theorem 1, its score is the best local alignment score of the window with copies of $P'$, its interval is the text part of that alignment, and its number of copies is the number of pattern letters used divided by $d$. Line L9 reports it only if it uses at least $2d$ pattern letters and its score is at least the minimum score. These facts hold for every report. Which regions are reported, and with which period, depends on the detection filter, the window growth and the consensus rounds, which are heuristics.
