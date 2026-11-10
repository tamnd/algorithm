---
title: A uniform random assignment satisfies 7m/8 clauses of an exact 3-CNF formula in expectation, and its derandomization satisfies at least 7m/8
proves: [correctness]
status: full
---

**Statement.** Let $\varphi$ be a CNF formula on $x_1, \ldots, x_n$ with clauses $C_1, \ldots, C_m$, each with exactly three literals on three different variables. Let $a$ be the output of lines L1 and L2 of RANDOM-ASSIGNMENT, and $s$ the count of line L3. Then:

1. $\mathbb{E}[s] = 7m/8$, so $\mathbb{E}[s] \ge \tfrac78 \text{OPT}$;
2. the derandomized algorithm, which fixes $x_1, \ldots, x_n$ in turn to the value with the larger conditional expectation, returns an assignment that satisfies at least $7m/8$ clauses, so at least $\tfrac78 \text{OPT}$;
3. one run of RANDOM-ASSIGNMENT satisfies at least $7m/8$ clauses with probability at least $1/(m + 1)$.

**Step 1: one clause.** Fix $C_j = \ell_1 \lor \ell_2 \lor \ell_3$, with $\ell_i$ a literal on the variable $x_{v_i}$ and $v_1, v_2, v_3$ different. Line L2 makes $a_{v_1}, a_{v_2}, a_{v_3}$ independent fair bits, so the values of $\ell_1, \ell_2, \ell_3$ (each a bit or its negation) are also independent fair bits. The clause is false exactly when all three literals are false, so $\Pr[C_j \text{ false}] = (1/2)^3 = 1/8$.

**Step 2: the expectation.** Let $Y_j$ be 1 if $C_j$ is satisfied and 0 otherwise, so $s = \sum_j Y_j$ and $\mathbb{E}[Y_j] = 7/8$ by step 1. By linearity of expectation, which needs no independence between clauses, $\mathbb{E}[s] = 7m/8$. Each assignment satisfies at most $m$ clauses, so $\text{OPT} \le m$ and $\mathbb{E}[s] = \tfrac78 m \ge \tfrac78 \text{OPT}$. This proves item 1.

**Step 3: the derandomization.** For a partial assignment $b_1, \ldots, b_i$ of the first $i$ variables, let $E(b_1, \ldots, b_i) = \mathbb{E}[s \mid a_1 = b_1, \ldots, a_i = b_i]$, with the other variables fair and independent. Since $a_{i+1}$ is a fair bit independent of the first $i$,

$$E(b_1, \ldots, b_i) = \tfrac12 E(b_1, \ldots, b_i, 1) + \tfrac12 E(b_1, \ldots, b_i, 0),$$

so the larger of the two values on the right is at least $E(b_1, \ldots, b_i)$. The derandomized algorithm picks that value at each step, so by induction on $i$, $E(b_1, \ldots, b_i) \ge E() = 7m/8$ for each $i$. At $i = n$, all variables are fixed and $E(b_1, \ldots, b_n) = s(b)$, so $s(b) \ge 7m/8 \ge \tfrac78 \text{OPT}$. Each value $E(b_1, \ldots, b_i)$ can be computed exactly: a clause with a true fixed literal, or with a variable in both signs, contributes 1, and otherwise a clause with $k$ free distinct literals contributes $1 - 2^{-k}$. This proves item 2.

**Step 4: the probability of one run.** Let $p = \Pr[s \ge 7m/8]$ and let $k$ be the largest integer below $7m/8$. Then $s \le k$ when $s < 7m/8$, and $s \le m$ always, so

$$\frac{7m}{8} = \mathbb{E}[s] \le (1 - p) k + p m, \qquad \text{so} \qquad p \ge \frac{7m/8 - k}{m - k}.$$

As $7m/8$ is a multiple of $1/8$, $k \le 7m/8 - 1/8$. The right side $\frac{7m/8 - k}{m - k}$ decreases as $k$ grows, because $7m/8 < m$. So $p \ge \frac{1/8}{m/8 + 1/8} = \frac{1}{m + 1}$. This proves item 3.

**Termination.** The loop of line L1 runs $n$ times, line L3 reads each clause once, and the derandomized algorithm makes $2n$ evaluations of $E$, each in $O(m)$ time. $\blacksquare$
