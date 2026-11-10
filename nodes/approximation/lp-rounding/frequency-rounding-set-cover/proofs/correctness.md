---
title: Rounding the set cover LP at 1/f gives a cover of cost at most f times the LP value
proves: [correctness]
status: full
---

**Statement.** Let $U$ be a finite universe, $S_1, \ldots, S_m \subseteq U$ sets whose union is $U$, and $c_1, \ldots, c_m \ge 0$ costs. Let $f_e = |\{j : e \in S_j\}|$ and $f = \max_{e \in U} f_e$. Let $x$ be feasible for the set cover LP: $\sum_{j : e \in S_j} x_j \ge 1$ for each $e \in U$ and $x \ge 0$. Let $I = \{j : x_j \ge 1/f\}$. Then:

1. $\bigcup_{j \in I} S_j = U$;
2. $c(I) \le f \sum_{j=1}^m c_j x_j$;
3. if $x$ is optimal, $c(I) \le f \cdot \text{LP}^* \le f \cdot \text{OPT}$.

If $U$ is empty, the algorithm returns $I = \emptyset$, which is a cover of cost 0, so we assume $U \ne \emptyset$ and so $f \ge 1$.

**Setup.** Line L1 of FREQ-ROUND-SC computes $f$. Line L2 computes $x$. The loop of lines L4 and L5 visits each $j$ once and adds $j$ to $I$ exactly when $x_j \ge 1/f$. So line L6 returns the set $I$ of the statement.

**Step 1: $I$ is a cover.** Take $e \in U$ and let $J_e = \{j : e \in S_j\}$, so $|J_e| = f_e$ and $1 \le f_e \le f$. Assume, for a contradiction, that $x_j < 1/f$ for each $j \in J_e$. Then

$$\sum_{j \in J_e} x_j < \frac{f_e}{f} \le 1,$$

which contradicts the constraint of $e$. So some $j \in J_e$ has $x_j \ge 1/f$. This $j$ is in $I$, and $e \in S_j$. So each element is covered.

**Step 2: the cost bound.** For $j \in I$, $x_j \ge 1/f$, so $f x_j \ge 1$, and since $c_j \ge 0$, $c_j \le f c_j x_j$. Summing over $I$ and then adding the nonnegative terms $f c_j x_j$ for $j \notin I$:

$$c(I) = \sum_{j \in I} c_j \le f \sum_{j \in I} c_j x_j \le f \sum_{j=1}^m c_j x_j.$$

**Step 3: comparison with OPT.** For an optimal $x$, step 2 gives $c(I) \le f \cdot \text{LP}^*$. Let $I^*$ be an optimal cover. Its indicator vector is nonnegative, and for each $e$ the sum $\sum_{j \in J_e} [j \in I^*]$ is at least 1, because some set of $I^*$ contains $e$. So it is feasible, and $\text{LP}^* \le c(I^*) = \text{OPT}$. Hence $c(I) \le f \cdot \text{LP}^* \le f \cdot \text{OPT}$.

**Termination.** Line L1 reads each set once, line L2 calls an LP solver that halts, and the loop of line L4 runs $m$ times. $\blacksquare$
