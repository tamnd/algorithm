---
title: The Wu-Manber vectors hold the active rows of the Sellers table
proves: [correctness]
status: full
---

Indices are 0-based, $|P| = m$, $|T| = n$, $k \ge 0$. Let $C[i][j]$ be the Sellers table, so $C[0][j] = 0$, $C[i][0] = i$, and for $i, j \ge 1$

$$C[i][j] = \min\bigl(C[i][j-1] + 1,\; C[i-1][j] + 1,\; C[i-1][j-1] + \delta_{ij}\bigr), \qquad \delta_{ij} = [P[i-1] \ne T[j-1]], \tag{R}$$

by the correctness proof of [Sellers' algorithm](/sellers-algorithm/). For $0 \le e \le k$ and $0 \le j \le n$ let

$$S_e(j) = \{\, i : 1 \le i \le m,\ C[i][j] \le e \,\}, \qquad V_e(j) = \sum_{i \in S_e(j)} 2^{i-1}.$$

For a vector $X$ that represents a set $S \subseteq \{1, \ldots, m\}$ by bit $i - 1$ for $i$, the vector $(X \ll 1) \,|\, 1$, cut to $m$ bits, represents $\{\, i : 1 \le i \le m,\ i - 1 \in S \cup \{0\} \,\}$.

**Lemma 1.** For $1 \le i \le m$, $1 \le j \le n$ and $0 \le e \le k$, $C[i][j] \le e$ holds exactly when at least one of these holds:

1. $\delta_{ij} = 0$ and $C[i-1][j-1] \le e$;
2. $e \ge 1$ and $C[i-1][j-1] \le e - 1$;
3. $e \ge 1$ and $C[i][j-1] \le e - 1$;
4. $e \ge 1$ and $C[i-1][j] \le e - 1$.

*Proof.* By (R), $C[i][j] \le e$ exactly when one of its three terms is at most $e$. The term $C[i][j-1] + 1 \le e$ is condition 3, and $C[i-1][j] + 1 \le e$ is condition 4; both need $e \ge 1$ since the values are not negative. The term $C[i-1][j-1] + \delta_{ij} \le e$ holds exactly when $\delta_{ij} = 0$ and $C[i-1][j-1] \le e$ (condition 1), or $\delta_{ij} = 1$ and $C[i-1][j-1] \le e - 1$. The latter implies condition 2, and condition 2 implies $C[i-1][j-1] + \delta_{ij} \le e$ for both values of $\delta_{ij}$. $\square$

**Lemma 2.** After line L2, $R[e] = V_e(0)$ for all $e$. After the pass of the loop of line L4 for column $j$, $R[e] = V_e(j)$ for all $e$.

*Proof.* Column 0: $C[i][0] = i \le e$ exactly for $1 \le i \le \min(e, m)$, which are the bits 0 to $\min(e, m) - 1$ set by line L2.

Column $j \ge 1$: assume $R[e] = V_e(j-1)$ for all $e$ before the pass. Let $b = B[T[j-1]]$, which has bit $i - 1$ set exactly when $\delta_{ij} = 0$. We show by induction on $e$ that after the update of $R[e]$, $R[e] = V_e(j)$, and that at that moment $old = V_e(j-1)$.

For $e = 0$, line L5 saves $old = V_0(j-1)$ and sets $R[0]$ to $((V_0(j-1) \ll 1) \,|\, 1) \,\&\, b$. Bit $i - 1$ of it is set exactly when $i - 1 \in S_0(j-1) \cup \{0\}$, that is $C[i-1][j-1] \le 0$ (row 0 has the value 0), and $\delta_{ij} = 0$. By Lemma 1 with $e = 0$, only condition 1 can hold, so this is $C[i][j] \le 0$.

For $e \ge 1$, line L7 sets $prev = V_{e-1}(j-1)$ (the value of $old$ from step $e - 1$) and $old = V_e(j-1)$, and $R[e-1] = V_{e-1}(j)$ by the induction. The new value is the OR, cut to $m$ bits, of four vectors. Bit $i - 1$ of each is set exactly when:

- $((old \ll 1) \,|\, 1) \,\&\, b$: $C[i-1][j-1] \le e$ and $\delta_{ij} = 0$, which is condition 1;
- $(prev \ll 1) \,|\, 1$: $C[i-1][j-1] \le e - 1$, which is condition 2 (for $i = 1$, $C[0][j-1] = 0 \le e - 1$);
- $prev$: $C[i][j-1] \le e - 1$, which is condition 3;
- $R[e-1] \ll 1$, together with the 1 of the second vector: $C[i-1][j] \le e - 1$, which is condition 4 (for $i = 1$, $C[0][j] = 0 \le e - 1$, and the 1 covers it).

By Lemma 1 the OR has bit $i - 1$ set exactly when $C[i][j] \le e$. So $R[e] = V_e(j)$. $\square$

**Theorem.** WU-MANBER$(P, T, k)$ reports, in increasing order, exactly the positions $j \in \{0, \ldots, n\}$ such that $d(P, T[h \ldots j)) \le k$ for some $h \le j$.

*Proof.* By the definition of the Sellers table, $j$ is such a position exactly when $C[m][j] \le k$. For $m = 0$ this holds for every $j$, and lines L3 and L8 report every $j$. For $m \ge 1$, $C[m][j] \le k$ holds exactly when $m \in S_k(j)$, that is when bit $m - 1$ of $V_k(j)$ is set. By Lemma 2 this is the test of line L3 for $j = 0$ and of line L8 for $j \ge 1$. The columns are handled in increasing order. $\blacksquare$
