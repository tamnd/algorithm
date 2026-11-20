---
title: The DMP pair is a 1/2-Nash equilibrium, and the bound 1/2 is tight
proves: [correctness]
status: full
---

Let $(A, B)$ be an $m \times n$ bimatrix game with all entries in $[0, 1]$. Here $m$ and $n$ are the numbers of pure strategies of the row player and of the column player. For mixed strategies $x$ and $y$, the row player gets $x^{\mathsf T} A y$ and the column player gets $x^{\mathsf T} B y$. The pair $(x, y)$ is an $\varepsilon$-Nash equilibrium if $\max_r (Ay)_r - x^{\mathsf T} A y \le \varepsilon$ and $\max_c (x^{\mathsf T} B)_c - x^{\mathsf T} B y \le \varepsilon$.

**Lemma 1 (pure deviations are enough).** For every mixed strategy $x'$ of the row player, $x'^{\mathsf T} A y \le \max_r (Ay)_r$, and the same holds for the column player.

*Proof.* $x'^{\mathsf T} A y = \sum_r x'_r (Ay)_r$ is an average of the numbers $(Ay)_r$, so it is at most their maximum. $\square$

So the gain of a player from any deviation is the gain from its best pure deviation, and the two inequalities above are the full definition.

The algorithm takes any row $i$, then lets $j$ be a column with $B_{ij} = \max_c B_{ic}$ (line L1), and $k$ a row with $A_{kj} = \max_r A_{rj}$ (line L2). It outputs $x = \tfrac12 e_i + \tfrac12 e_k$ and $y = e_j$ (lines L3 to L5). If $k = i$, then $x = e_i$.

**Theorem 1.** $(x, y)$ is a $1/2$-Nash equilibrium. More exactly, the gain of the row player is $(A_{kj} - A_{ij})/2$, and the gain of the column player is at most $\max_c (B_{kc} - B_{kj})/2$.

*Proof.* First, $x$ and $y$ are mixed strategies: the weights are $\tfrac12$ and $\tfrac12$ on rows $i$ and $k$ (or 1 on row $i$ if $k = i$), and 1 on column $j$.

*Row player.* Since $y = e_j$, $(Ay)_r = A_{rj}$, and $\max_r (Ay)_r = A_{kj}$ by the choice of $k$. The row player gets $x^{\mathsf T} A y = \tfrac12 A_{ij} + \tfrac12 A_{kj}$. So the gain is
$$A_{kj} - \tfrac12 A_{ij} - \tfrac12 A_{kj} = \tfrac12 (A_{kj} - A_{ij}) \le \tfrac12 A_{kj} \le \tfrac12,$$
because $A_{ij} \ge 0$ and $A_{kj} \le 1$.

*Column player.* The column player gets $x^{\mathsf T} B y = \tfrac12 B_{ij} + \tfrac12 B_{kj}$. A pure deviation to column $c$ gives $\tfrac12 B_{ic} + \tfrac12 B_{kc}$. By the choice of $j$, $B_{ic} \le B_{ij}$. So the gain from column $c$ is
$$\tfrac12 B_{ic} + \tfrac12 B_{kc} - \tfrac12 B_{ij} - \tfrac12 B_{kj} \le \tfrac12 (B_{kc} - B_{kj}) \le \tfrac12 B_{kc} \le \tfrac12,$$
because $B_{kj} \ge 0$ and $B_{kc} \le 1$. By Lemma 1 the largest gain over all strategies is the largest of these numbers, so it is at most $\tfrac12$. $\square$

**Corollary 1 (pure equilibrium).** If $k = i$, then $(e_i, e_j)$ is a pure Nash equilibrium.

*Proof.* With $k = i$ the row gain is $(A_{ij} - A_{ij})/2 = 0$. For the column player, $x = e_i$ and $j$ is a best column against row $i$, so the gain is 0 too. $\square$

**Corollary 2 (other payoff ranges).** If every entry of $A$ and of $B$ is in $[a, b]$, the output is a $(b - a)/2$-Nash equilibrium.

*Proof.* The algorithm only compares entries of the same matrix, so it gives the same output on $(A', B')$ with $A'_{rc} = (A_{rc} - a)/(b - a)$ and $B'_{rc} = (B_{rc} - a)/(b - a)$, whose entries are in $[0, 1]$. All gains scale by the factor $b - a$. If $a = b$, every gain is 0. $\square$

**Theorem 2 (the bound is tight).** For every $a, b \in [0, 1]$, the game
$$A = \begin{pmatrix} 0 & a \\ 1 & b \end{pmatrix}, \qquad B = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$$
with start row $i = 0$ and ties broken to the smallest index gives an output where both gains are exactly $\tfrac12$.

*Proof.* Row 0 of $B$ is $(1, 1)$, so the tie goes to $j = 0$. Column 0 of $A$ is $(0, 1)$, so $k = 1$. The output is $x = (\tfrac12, \tfrac12)$ and $y = e_0$. The row player gets $\tfrac12(0 + 1) = \tfrac12$ and row 1 gives 1, a gain of $\tfrac12$. The column player gets $\tfrac12 (1 + 0) = \tfrac12$, and column 1 gives $\tfrac12(1 + 1) = 1$, a gain of $\tfrac12$. $\square$

**Running time.** Line L1 reads the $n$ entries $B_{i0}, \dots, B_{i,n-1}$ and line L2 reads the $m$ entries $A_{0j}, \dots, A_{m-1,j}$. The other lines write $m + n$ numbers. So the time is $O(m + n)$, which is sublinear in the size $2mn$ of the input when the matrices can be read at random positions.
