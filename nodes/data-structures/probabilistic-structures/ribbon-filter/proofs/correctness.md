---
title: A ribbon filter accepts every key of its set
proves: [correctness, invariant, termination]
status: full
---

All arithmetic is over $\mathrm{GF}(2)$, on rows of length $m$ with an $r$-bit right side. For a key $x$ let $E(x)$ be its equation: the row with ones at the columns $s(x) + j$ for the bits $j$ of $c(x)$, and right side $\mathrm{fp}(x)$. A stored row $(C[i], B[i])$ with $C[i] \ne 0$ stands for the row with ones at the columns $i + j$ for the bits $j$ of $C[i]$, and right side $B[i]$. Let $R$ be the set of stored rows.

**Lemma 1 (shape).** At all times during the build, each nonzero $C[i]$ has bit 0 set and fewer than $w$ bits, and all its columns are in $\{0, \ldots, m - 1\}$. The current row $(s, c)$ of INSERT-ROW has the same properties.

*Proof.* At the start of INSERT-ROW, $c = c(x)$ has bit 0 set and $w$ bits, and $s + w - 1 \le m - 1$. Line L4 stores a row with these properties. At line L5, both $c$ and $C[s]$ are rows relative to $s$ with fewer than $w$ bits, so their xor has fewer than $w$ bits, and it has bit 0 cleared. If it is not 0, line L7 shifts it to its lowest bit, which keeps the absolute columns and sets bit 0. The absolute columns of the xor are among those of the two rows, so they stay in $\{0, \ldots, m - 1\}$. $\square$

**Lemma 2 (equivalence).** After INSERT-ROW has succeeded for the keys $x_1, \ldots, x_t$, the systems $\{E(x_1), \ldots, E(x_t)\}$ and $R$ have the same set of solutions $Z$.

*Proof.* By induction on $t$, with both systems empty for $t = 0$. Consider INSERT-ROW for $x = x_{t+1}$. Let $e$ be the current row with its right side, as an equation. Line L5 replaces $e$ by $e \oplus \rho$ for a row $\rho \in R$; line L7 does not change $e$ as an equation, it only renames its columns relative to the new $s$. So at all times $e = E(x) \oplus \sum_{\rho \in P} \rho$ for a set $P \subseteq R$.

If line L4 stores $e$, the new system $R' = R \cup \{e\}$ satisfies: a solution of $R'$ satisfies $E(x) = e \oplus \sum_P \rho$, and a solution of $R$ and $E(x)$ satisfies $e$. So $R'$ and $R \cup \{E(x)\}$ have the same solutions, and by the induction hypothesis these are the solutions of $E(x_1), \ldots, E(x_{t+1})$. If line L6 succeeds, then $e$ is the zero row with right side 0, so $E(x) = \sum_P \rho$ holds for every solution of $R$, and $R$ is unchanged. $\square$

**Lemma 3 (failure means no solution).** If line L6 fails, the equations of the keys inserted so far, with $x$, have no common solution.

*Proof.* Then $e$ is the zero row with right side $b \ne 0$, which no $Z$ satisfies, and $e = E(x) \oplus \sum_P \rho$; a common solution of $R$ and $E(x)$ would satisfy $e$. By Lemma 2 the system of the keys is equivalent to $R$. $\square$

**Theorem 1 (invariant (R)).** If every INSERT-ROW succeeds, then after BACK-SUBSTITUTE, $Z$ satisfies $E(x)$ for each $x \in S$, so QUERY returns true on $S$.

*Proof.* By Lemma 2 it suffices that $Z$ satisfies every stored row. Stored row $i$ has leading column $i$ (bit 0) and its other columns $i + j$ with $j \ge 1$, by Lemma 1. Line L9 runs for $i = m - 1$ down to 0 and sets $Z[i] = B[i] \oplus \bigoplus_{j \ge 1,\, C_j[i] = 1} Z[i + j]$, using only values $Z[i + j]$ that are already final, since $i + j > i$. So row $i$ holds, and it keeps holding, because later steps only write $Z[i']$ with $i' < i$, which row $i$ does not use. $\square$

**Theorem 2 (termination).** Each INSERT-ROW ends after at most $w$ rounds. If the hash functions of each try are independent and ideal, and a try succeeds with probability $p > 0$, then BUILD ends with probability 1 after a geometric number of tries. In particular $p > 0$ whenever $m - w + 1 \ge n$.

*Proof.* In each round that does not return, line L7 shifts $c$ right by $j \ge 1$, and $c$ has fewer than $w$ bits by Lemma 1, so after fewer than $w$ shifts it would be 0, and line L6 returns. For $p > 0$: if $m - w + 1 \ge n$, the keys can have distinct starts, and then each row finds its leading column free at line L4; this choice of starts has positive probability. $\blacksquare$
