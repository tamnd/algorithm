---
title: Gomory's algorithm with the lexicographic rule is correct and finite
proves: [correctness, termination]
status: full
---

**Setting.** $A \in \mathbb{Z}^{m \times n}$, $b \in \mathbb{Z}^m$, $c \in \mathbb{Z}^n$, and $P = \{x \ge 0 : Ax \le b\}$ is bounded. Let $S = P \cap \mathbb{Z}^n$. Round $k = 0, 1, \ldots$ works with $P_k = \{x \ge 0 : A^{(k)} x \le b^{(k)}\}$, where $A^{(0)} = A$, $b^{(0)} = b$, and each round appends one row $g^T x \le g_0$ with $g, g_0$ integer. For $x \in \mathbb{R}^n$ let $v(x) = (c^T x, x_1, \ldots, x_n)$, with components numbered $0$ to $n$. We write $\preceq$ for the lexicographic order on $\mathbb{R}^{n+1}$.

**The tableau.** At the end of line L2, the basis gives each component as $v_k = \bar v_k - \sum_{h \in N} d_{kh} t_h$, where $N$ is the set of nonbasic variables, each $t_h$ is an original variable or the slack of a row, and $t_h \ge 0$ on $P_k$. Each point of $P_k$ has unique values of the $t_h$, and $\bar v = v(\bar x)$ is the point with all $t_h = 0$. The stages of line L2 give two facts.

- (S0) $d_{0h} \ge 0$ for all $h \in N$, since stage 0 ends at an optimum of $c^T x$.
- (Sk) For $k \ge 1$: if $d_{0h} = \cdots = d_{k-1,h} = 0$ then $d_{kh} \ge 0$. Such a column may enter in stage $k$, so stage $k$ ends only when its reduced cost $d_{kh}$ is not negative. Pivots of later stages enter only columns with zero reduced cost in stage $k$, and such a pivot does not change $d_{kh}$ for the other columns, nor the value $\bar v_k$. So the fact stays true until the end of line L2.

**Lemma 1 (validity).** Each integer point of $P_k$ satisfies the cut of round $k$. So $P_{k+1} \cap \mathbb{Z}^n = P_k \cap \mathbb{Z}^n = S$.

*Proof.* Let $x \in P_k \cap \mathbb{Z}^n$. Then $v_j(x)$ is an integer, because $c$ is integral. Each $t_h$ is an integer: an original variable is a coordinate of $x$, and a slack $b_r - A_r x$ is an integer since all rows have integer data. From $v_j + \sum_h d_{jh} t_h = \bar v_j$, the number $\sum_h \operatorname{frac}(d_{jh}) t_h - \operatorname{frac}(\bar v_j)$ equals $\bar v_j - v_j - \sum_h \lfloor d_{jh} \rfloor t_h - \operatorname{frac}(\bar v_j) = \lfloor \bar v_j \rfloor - v_j - \sum_h \lfloor d_{jh} \rfloor t_h$, which is an integer. The sum $\sum_h \operatorname{frac}(d_{jh}) t_h$ is at least 0, and $\operatorname{frac}(\bar v_j) < 1$. An integer greater than $-1$ is at least 0, so the cut holds. The same computation shows that the cut is the inequality $v_j + \sum_h \lfloor d_{jh} \rfloor t_h \le \lfloor \bar v_j \rfloor$, and line L8 substitutes $t_h = x_h$ or $t_h = b_r - A_r x$. The result has integer coefficients and right side. $\square$

**Lemma 2 (separation).** $\bar x$ violates the cut of round $k$.

*Proof.* At $\bar x$ all $t_h = 0$, so the left side is 0, and the right side $\operatorname{frac}(\bar v_j)$ is positive because $\bar v_j$ is fractional. $\square$

**Lemma 3 (the key step).** Let $j$ be the source component of round $k$. If $y \in P_{k+1}$ and $v_i(y) = \bar v_i$ for all $i < j$, then $v_j(y) \le \lfloor \bar v_j \rfloor$.

*Proof.* Write $y$ with the nonbasic values $t_h \ge 0$ of the round $k$ tableau; this is possible because $y \in P_{k+1} \subseteq P_k$. We show by induction on $i < j$ that $t_h = 0$ for each $h$ with $d_{ih} > 0$. Assume it for all $i' < i$. Then $t_h > 0$ implies $d_{i'h} \le 0$ for all $i' < i$, and with (S0) and (Sk) one gets $d_{0h} = \cdots = d_{i-1,h} = 0$ and $d_{ih} \ge 0$. Now $0 = \bar v_i - v_i(y) = \sum_h d_{ih} t_h$ is a sum of terms that are all at least 0, so each term is 0, and $t_h = 0$ when $d_{ih} > 0$. The same argument for $i = j$ shows that $d_{jh} \ge 0$ for each $h$ with $t_h > 0$. For $q \ge 0$ we have $q \ge \operatorname{frac}(q)$. So

$$v_j(y) = \bar v_j - \sum_h d_{jh} t_h \le \bar v_j - \sum_h \operatorname{frac}(d_{jh}) t_h \le \bar v_j - \operatorname{frac}(\bar v_j) = \lfloor \bar v_j \rfloor,$$

where the last inequality is the cut, which $y$ satisfies. $\square$

**Theorem.** The algorithm stops after finitely many rounds. If it returns $\bar x$, then $\bar x$ is an optimal solution of $\max\{c^T x : x \in S\}$. If it returns INFEASIBLE, then $S = \emptyset$.

*Proof of the answers.* By Lemma 1, $S \subseteq P_k \subseteq P$ for each $k$. If $P_k = \emptyset$, then $S = \emptyset$. If line L5 returns $\bar x$, then $\bar x \in P$ is integral, so $\bar x \in S$, and $c^T \bar x = \max_{P_k} c^T x \ge \max_S c^T x$.

*Proof of termination.* Assume that the algorithm runs forever, and let $\bar v^{(k)}$ be the vector $\bar v$ of round $k$. Since $P_{k+1} \subseteq P_k$, the lexicographic maximum cannot increase: $\bar v^{(k+1)} \preceq \bar v^{(k)}$. Each component is bounded below on $P$: component 0 by $\min_P c^T x$, which is finite because $P$ is bounded and not empty, and component $i \ge 1$ by 0.

We show by induction on $j = 0, 1, \ldots, n$ that there is a round $K_j$ after which components $0$ to $j$ of $\bar v^{(k)}$ are constant integers. Assume this for $j - 1$, with $K_{-1} = 0$. For $k \ge K_{j-1}$, components $0$ to $j-1$ are constant, so the lexicographic order gives that $\bar v^{(k)}_j$ does not increase. Let $k \ge K_{j-1}$ be a round with $\bar v^{(k)}_j$ fractional. Components $0$ to $j-1$ are integral, so $j$ is the source component of round $k$, and $\bar v^{(k+1)}$ agrees with $\bar v^{(k)}$ in components $0$ to $j-1$. Lemma 3 gives $\bar v^{(k')}_j \le \lfloor \bar v^{(k)}_j \rfloor$ for all $k' > k$. If $k' > k$ is the next such round, then $\bar v^{(k')}_j$ is fractional and at most the integer $\lfloor \bar v^{(k)}_j \rfloor$, so $\lfloor \bar v^{(k')}_j \rfloor \le \lfloor \bar v^{(k)}_j \rfloor - 1$. The floors of the fractional values form a strictly decreasing sequence of integers, which is bounded below, so there are only finitely many such rounds. After the last one, $\bar v_j$ is an integer that does not increase and is bounded below, so it is constant from some round $K_j$ on.

For $j = n$, all components of $\bar v^{(k)}$ are integers for $k \ge K_n$, and line L5 stops at round $K_n$. This contradicts the assumption. $\blacksquare$
