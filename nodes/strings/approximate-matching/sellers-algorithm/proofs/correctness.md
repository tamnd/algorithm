---
title: Sellers' algorithm reports exactly the ends of the approximate matches
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m$, $|T| = n$, and $d$ is the Levenshtein distance. For $0 \le i \le m$ and $0 \le j \le n$ let

$$E[i][j] = \min_{0 \le h \le j} d(P[0 \ldots i), T[h \ldots j)).$$

The [Wagner-Fischer](/wagner-fischer-algorithm/) proof shows that $d(u, v)$ is the least cost $A(u, v)$ of an alignment of $u$ and $v$, where a column $(a, b)$ costs $[a \ne b]$ and the gap counts as a symbol. We use alignments below.

**Lemma 1.** $E[0][j] = 0$, $E[i][0] = i$, and for $i, j \ge 1$

$$E[i][j] = \min\bigl(E[i][j-1] + 1,\; E[i-1][j] + 1,\; E[i-1][j-1] + [P[i-1] \ne T[j-1]]\bigr).$$

*Proof.* For $i = 0$, take $h = j$: the empty strings have distance 0. For $j = 0$, the only substring is empty, and $d(P[0 \ldots i), \varepsilon) = i$.

Let $i, j \ge 1$. Each term on the right is the cost of some alignment of $P[0 \ldots i)$ with some $T[h \ldots j)$, $h \le j$. For the first term, take an optimal pair $(h, \alpha)$ for $E[i][j-1]$, with $h \le j - 1$, and add the column $(-, T[j-1])$. This aligns $P[0 \ldots i)$ with $T[h \ldots j)$. For the second, take an optimal pair for $E[i-1][j]$ and add the column $(P[i-1], -)$. For the third, take an optimal pair for $E[i-1][j-1]$, with $h \le j-1$, and add $(P[i-1], T[j-1])$. So $E[i][j]$ is at most each term.

Conversely, let $h \le j$ and let $\alpha$ be an optimal alignment of $P[0 \ldots i)$ and $T[h \ldots j)$. If $h = j$, then $\alpha$ has the $i$ columns $(P[t], -)$ and costs $i$, and $E[i-1][j] + 1 \le (i - 1) + 1 = i$, because $E[i-1][j] \le d(P[0 \ldots i-1), \varepsilon) = i - 1$. If $h < j$, the last column of $\alpha$ is one of $(-, T[j-1])$, $(P[i-1], -)$ and $(P[i-1], T[j-1])$. Without it, $\alpha$ aligns $P[0 \ldots i)$ with $T[h \ldots j-1)$, or $P[0 \ldots i-1)$ with $T[h \ldots j)$, or $P[0 \ldots i-1)$ with $T[h \ldots j-1)$. In each case $h$ is allowed in the minimum of the smaller entry, so the cost of $\alpha$ is at least the matching term on the right. $\square$

**Lemma 2.** At the test of line L9 for the column $j$ (and at line L2 for $j = 0$), the array holds $C[i] = E[i][j]$ for all $0 \le i \le m$.

*Proof.* By induction on $j$. Line L1 sets $C[i] = i = E[i][0]$. Assume $C[i] = E[i][j-1]$ for all $i$ before the step for $j$. Line L4 saves $prev = C[0] = E[0][j-1]$ and sets $C[0] = 0 = E[0][j]$. We claim that at the start of the step for row $i$ (line L5), $C[0 \ldots i-1]$ holds column $j$, $C[i \ldots m]$ still holds column $j - 1$, and $prev = E[i-1][j-1]$. This holds for $i = 1$. In the step, line L7 computes $\min(C[i] + 1, C[i-1] + 1, prev + c) = \min(E[i][j-1] + 1, E[i-1][j] + 1, E[i-1][j-1] + c)$, which is $E[i][j]$ by Lemma 1. Line L8 sets $prev$ to the old $C[i] = E[i][j-1]$ and stores $E[i][j]$ in $C[i]$. So the claim holds for $i + 1$. After row $m$, the array is column $j$. $\square$

**Theorem.** SELLERS$(P, T, k)$ reports $j$ if and only if $d(P, T[h \ldots j)) \le k$ for some $h \le j$, and it reports each such $j$ once, in increasing order.

*Proof.* By Lemma 2, the test at line L2 or L9 for $j$ is $E[m][j] \le k$, which is the condition by the definition of $E$. The loop of line L3 visits each $j$ once, in increasing order. $\blacksquare$
