---
title: The Wagner-Fischer table holds the Levenshtein distances of all prefix pairs
proves: [correctness]
status: full
---

Indices are 0-based. Let $x$ have length $m$ and $y$ length $n$. The distance $d(u, v)$ is the least number of unit-cost insertions, deletions and substitutions that turn $u$ into $v$. Let $-$ be a gap symbol that is not in $\Sigma$, and let $\delta(a, b) = [a \ne b]$ for $a, b \in \Sigma \cup \{-\}$. This $\delta$ is the discrete metric, so $\delta(a, b) \le \delta(a, c) + \delta(c, b)$ for all three symbols.

An *alignment* of $u$ and $v$ is a sequence of columns $(a_1, b_1), \ldots, (a_L, b_L)$ over $\Sigma \cup \{-\}$, with no column $(-, -)$, such that $a_1 \cdots a_L$ with the gaps removed is $u$ and $b_1 \cdots b_L$ with the gaps removed is $v$. Its cost is $\sum_t \delta(a_t, b_t)$. Let $A(u, v)$ be the least cost of an alignment of $u$ and $v$.

**Lemma 1.** After lines L1 to L6, $D[i][j] = A(x[0 \ldots i), y[0 \ldots j))$ for all $0 \le i \le m$ and $0 \le j \le n$.

*Proof.* By induction on $i + j$, in the order of the loops, which compute $D[i-1][j]$, $D[i][j-1]$ and $D[i-1][j-1]$ before $D[i][j]$. The only alignment of $x[0 \ldots i)$ with the empty string has $i$ columns $(a, -)$, so $A = i$, which line L1 stores. Line L2 is the same for $j$. Let $i, j \ge 1$, and consider an alignment of $x[0 \ldots i)$ and $y[0 \ldots j)$. Its last column is one of three kinds: $(x[i-1], y[j-1])$, $(x[i-1], -)$ or $(-, y[j-1])$. If we remove the last column, we get an alignment of $x[0 \ldots i-1)$ and $y[0 \ldots j-1)$, or of $x[0 \ldots i-1)$ and $y[0 \ldots j)$, or of $x[0 \ldots i)$ and $y[0 \ldots j-1)$, and each alignment of these pairs extends by the matching column. So $A$ of the pair is the least of $A(\text{shorter pair}) + \delta(\text{last column})$ over the three kinds. The three costs of the last columns are $[x[i-1] \ne y[j-1]]$, 1 and 1. By the induction hypothesis, this is the minimum of line L6, with $c$ from line L5. $\square$

**Lemma 2.** $d(u, v) \le A(u, v)$.

*Proof.* Take an alignment of cost $A(u, v)$. Process its columns from the last one to the first one. A column $(a, b)$ with $a = b$ needs no operation. A column $(a, b)$ with $a, b \in \Sigma$ and $a \ne b$ is a substitution of the character of $u$ in this column by $b$. A column $(a, -)$ is a deletion of that character, and a column $(-, b)$ is an insertion of $b$ at this place. The columns to the left are not changed by an operation on a later column, so their characters keep their positions. At the end the string reads $v$. The script has one operation for each column with $\delta = 1$, so its length is the cost of the alignment. $\square$

**Lemma 3.** $A(u, w) \le A(u, v) + A(v, w)$ for all strings $u$, $v$, $w$.

*Proof.* Let $\alpha$ be an optimal alignment of $u$ and $v$ and $\beta$ an optimal alignment of $v$ and $w$. Each character of $v$ is in one column of $\alpha$ and in one column of $\beta$. We build a sequence of triples $(a, c, b)$. For the $t$-th character $c$ of $v$, take the triple $(a, c, b)$, where $(a, c)$ is its column in $\alpha$ and $(c, b)$ is its column in $\beta$. A column $(a, -)$ of $\alpha$ gives the triple $(a, -, -)$, and a column $(-, b)$ of $\beta$ gives the triple $(-, -, b)$. Order the triples by the order of $v$: before the triple of the $t$-th character of $v$, and after the triple of the $(t-1)$-th one, put the triples of the columns of $\alpha$ that lie between these two characters, in their order in $\alpha$, then those of $\beta$, in their order in $\beta$. Then the first entries, read in order, spell $u$ with gaps, and the last entries spell $w$ with gaps. Remove the triples whose first and last entries are both $-$. The pairs (first entry, last entry) of the other triples form an alignment $\gamma$ of $u$ and $w$. For each triple, $\delta(a, b) \le \delta(a, c) + \delta(c, b)$. The term $\delta(a, c)$ is the cost of the column of $\alpha$ in the triple, or 0 for a triple $(-, -, b)$, and the same holds for $\beta$. Each column of $\alpha$ and of $\beta$ is in exactly one triple. So the cost of $\gamma$ is at most the cost of $\alpha$ plus the cost of $\beta$. $\square$

**Lemma 4.** $A(u, v) \le d(u, v)$.

*Proof.* Let $u = s_0, s_1, \ldots, s_L = v$ be a script of length $L = d(u, v)$, where each $s_t$ comes from $s_{t-1}$ by one operation. For one operation, $A(s_{t-1}, s_t) \le 1$: align the unchanged characters with themselves, and add one column $(a, b)$, $(a, -)$ or $(-, b)$ for the changed character. By Lemma 3, applied $L - 1$ times, $A(u, v) \le \sum_{t=1}^{L} A(s_{t-1}, s_t) \le L$. For $L = 0$, $u = v$ and the alignment of each character with itself costs 0. $\square$

**Theorem.** WAGNER-FISCHER$(x, y)$ returns $d(x, y)$, and TRACEBACK returns an alignment of cost $d(x, y)$.

*Proof.* By Lemmas 2 and 4, $A = d$. By Lemma 1, line L7 returns $D[m][n] = A(x, y) = d(x, y)$.

For TRACEBACK, we use this invariant at line L9: the columns in $S$ form an alignment of $x[i \ldots m)$ and $y[j \ldots n)$ of cost $D[m][n] - D[i][j]$. It holds at line L8, where $S$ is empty and $(i, j) = (m, n)$. In a step, if line L10 applies, the column $(x[i-1], y[j-1])$ costs $D[i][j] - D[i-1][j-1]$. If line L11 applies, the column $(x[i-1], -)$ costs $1 = D[i][j] - D[i-1][j]$. If neither applies, then $j > 0$ and $D[i][j] = D[i][j-1] + 1$: when $i = 0$, this is $D[0][j] = j$; when $j = 0$, line L11 applies, because $D[i][0] = D[i-1][0] + 1$; when $i, j \ge 1$, line L6 makes $D[i][j]$ equal to one of its three terms, and the first two are excluded. So line L12 adds a column $(-, y[j-1])$ of cost $1 = D[i][j] - D[i][j-1]$. In each case the invariant holds again, and $i + j$ drops by 1 or 2. So the loop stops after at most $m + n$ steps, with $i = j = 0$, and $S$ is an alignment of $x$ and $y$ of cost $D[m][n] - D[0][0] = d(x, y)$. $\blacksquare$
