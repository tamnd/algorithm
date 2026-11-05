---
title: The LCS table holds the prefix LCS lengths and the traceback returns an LCS
proves: [correctness]
status: full
---

We use the pseudocode of the page, with $X = \langle x_1, \ldots, x_m \rangle$ and $Y = \langle y_1, \ldots, y_n \rangle$. Write $X_i$ for the prefix of length $i$ and $L(i, j) = \mathrm{lcs}(X_i, Y_j)$.

**Lemma 1 (the fill).** When LCS-LENGTH returns, $c[i, j] = L(i, j)$ for all $0 \le i \le m$ and $0 \le j \le n$.

*Proof.* Order the cells by the time at which they get their final value: first the cells of lines L1 and L2, then the cells $(i, j)$ with $i, j \ge 1$ in row-major order. No cell is written again after this time. We prove by induction along this order that each cell gets the value $L(i, j)$.

If $i = 0$ or $j = 0$, the only common subsequence of $X_i$ and $Y_j$ is the empty one, so $L(i, j) = 0$, which lines L1 and L2 write.

Let $i, j \ge 1$. The cells $(i-1, j-1)$ and $(i-1, j)$ are in row $i - 1$ (or in row 0 or column 0), and $(i, j-1)$ is earlier in row $i$ (or in column 0). So all three come before $(i, j)$ in the order, and by the induction hypothesis they hold $L(i-1, j-1)$, $L(i-1, j)$ and $L(i, j-1)$. If $x_i = y_j$, line L5 writes $L(i-1, j-1) + 1$. If $x_i \ne y_j$, lines L6 and L7 write $\max(L(i-1, j), L(i, j-1))$: line L6 writes $c[i-1, j]$ when it is at least $c[i, j-1]$, and line L7 writes $c[i, j-1]$ otherwise. By the corollary of the [optimal substructure theorem](/lcs-optimal-substructure/), the written value is $L(i, j)$ in both cases. $\square$

**Lemma 2 (the traceback).** LCS-TRACEBACK$(c, X, Y)$ stops, and returns a common subsequence of $X$ and $Y$ of length $L(m, n)$.

*Proof.* Write $X[a..]$ for the suffix $x_{a} \cdots x_m$ (empty if $a > m$), and the same for $Y$. We show this invariant of the loop of line L10:

> **(T)** $0 \le i \le m$, $0 \le j \le n$, $Z$ is a common subsequence of $X[i+1..]$ and $Y[j+1..]$, and $|Z| + c[i, j] = c[m, n]$.

*Initialization.* Line L9 sets $i = m$, $j = n$ and $Z$ empty. The suffixes are empty, the empty sequence is a common subsequence of them, and $|Z| + c[m, n] = c[m, n]$.

*Maintenance.* Assume (T) and $i, j \ge 1$.

- If $x_i = y_j$ (line L11), by Lemma 1 and the recurrence, $c[i, j] = c[i-1, j-1] + 1$. The new $Z' = x_i Z$ is a common subsequence of $X[i..]$ and $Y[j..]$: embed $x_i$ at index $i$ of $X$ and at index $j$ of $Y$, followed by the embeddings of $Z$, which use indices larger than $i$ and $j$. And $|Z'| + c[i-1, j-1] = |Z| + 1 + c[i, j] - 1 = c[m, n]$.
- If $x_i \ne y_j$, by Lemma 1, $c[i, j] = \max(c[i-1, j], c[i, j-1])$. Line L12 moves to $(i-1, j)$ when $c[i-1, j] \ge c[i, j-1]$, that is, when $c[i-1, j] = c[i, j]$. Line L13 moves to $(i, j-1)$ otherwise, and then $c[i, j-1] > c[i-1, j]$, so $c[i, j-1] = c[i, j]$. In both cases the value of $c$ at the new cell is $c[i, j]$, so the equation stays true. $Z$ does not change, and a common subsequence of $X[i+1..]$ and $Y[j+1..]$ is also a common subsequence of the longer suffixes $X[i..]$ and $Y[j+1..]$, or $X[i+1..]$ and $Y[j..]$.

*Termination.* Each iteration lowers $i + j$ by at least 1, and the loop runs only while $i + j \ge 2$, so it stops after at most $m + n$ iterations.

*At the end.* The loop stops with $i = 0$ or $j = 0$. Then $c[i, j] = L(i, j) = 0$ by Lemma 1, so $|Z| = c[m, n] = L(m, n)$. By (T), $Z$ is a common subsequence of $X[i+1..]$ and $Y[j+1..]$, which are suffixes of $X$ and $Y$, so it is a common subsequence of $X$ and $Y$. $\square$

**Theorem.** LCS-TRACEBACK(LCS-LENGTH$(X, Y)$, $X$, $Y$) returns a longest common subsequence of $X$ and $Y$.

*Proof.* By Lemma 2 the output is a common subsequence of length $L(m, n) = \mathrm{lcs}(X, Y)$, which is the maximum length. $\blacksquare$
