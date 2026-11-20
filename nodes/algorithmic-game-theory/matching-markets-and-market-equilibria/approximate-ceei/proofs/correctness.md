---
title: The toy grid search returns demands at the best grid prices, and equal budgets can fail to clear
proves: [correctness, termination]
status: full
---

This proof is for the toy grid search of the pseudocode. It does not prove Budish's existence theorem, which is non-constructive and relies on the Kakutani fixed point theorem.

Fix $n$ agents, $m$ goods with $q_j \ge 1$ seats, budgets $b_i > 0$, and for each agent a list of accepted bundles in strict order, best first. The empty bundle is accepted by every agent and ranked below every listed bundle. All numbers are exact rationals. For prices $p \ge 0$, the demand $x_i(p)$ is the highest ranked accepted bundle $B$ with $\sum_{j \in B} p_j \le b_i$, and the clearing error is $\alpha(p) = \|z(p)\|_2$, where $z_j(p) = d_j - q_j$ if $p_j > 0$ and $z_j(p) = \max(d_j - q_j, 0)$ if $p_j = 0$, with $d_j = \#\{i : j \in x_i(p)\}$. The grid is $P = \{0, s, 2s, \ldots, Ks\}^m$ with $K = \lfloor c / s \rfloor$.

**Claim 1 (termination).** The search ends after $(K + 1)^m$ iterations of lines L3 to L5.

*Proof.* Line L2 enumerates the finite set $P$ once, and lines L3 to L5 do finite work: each agent's list is finite. $\square$

**Claim 2 (lines L3 and L4).** For each $p \in P$, line L3 computes $x_i(p)$ for every agent, and line L4 computes $z(p)$.

*Proof.* The function `demand` walks the list of agent $i$ from the best bundle down and returns the first bundle whose cost is at most $b_i$. Every bundle above it on the list costs more than $b_i$, so it is the highest ranked affordable bundle. If no listed bundle is affordable, it returns the empty bundle, which costs $0 \le b_i$ and is the only affordable accepted bundle left. The comparisons are exact. Line L4 counts the agents whose bundle contains $j$, subtracts $q_j$, and raises a negative value to $0$ when $p_j = 0$, which is the definition of $z_j(p)$. $\square$

**Claim 3 (output).** Line L6 returns $(\alpha(p^\circ), p^\circ, x(p^\circ))$, where $p^\circ$ is the first vector of $P$ in lexicographic order with $\alpha(p^\circ) = \min_{p \in P} \alpha(p)$. So every returned bundle is the demand of its agent at the returned prices, no grid vector has a smaller clearing error, and if all budgets lie in $[1, 1 + \beta]$, the output is an $(\alpha(p^\circ), \beta)$-CEEI.

*Proof.* By induction over the iterations of line L2, after each iteration `best` holds the squared error, the prices and the bundles of the first vector seen so far with the smallest squared error: the first vector is stored because `best` is empty (line L1), and a later vector replaces it only when its squared error is strictly smaller (line L5), so ties keep the earlier vector. By Claim 2 the stored bundles are the demands at the stored prices. The square root is increasing, so the smallest squared error gives the smallest $\alpha$. The definition of an $(\alpha, \beta)$-CEEI asks for budgets in $[1, 1 + \beta]$, every agent at her demand, and clearing error at most $\alpha$, which the output satisfies. $\square$

**Claim 4 (perturbed budgets).** The budgets $1 + \beta i / n$ for $i = 0, \ldots, n - 1$ are distinct and lie in $[1, 1 + \beta)$ for $\beta > 0$.

*Proof.* They increase strictly with $i$, the first is $1$, and the last is $1 + \beta (n - 1)/n < 1 + \beta$. $\square$

**Claim 5 (equal budgets can fail).** If all agents have the same budget and the same list, then at every price vector $p \ge 0$, not only on the grid, they all demand the same bundle. In the example with one seat and two agents who both accept only $\{1\}$, every price has $\alpha(p) = 1$. In the example with three students, one seat of course 1, three of course 2, and the list $\{1, 2\}, \{1\}, \{2\}$ for everyone, every price has $\alpha(p) \ge 1$.

*Proof.* The demand depends only on the list, the budget and $p$, so it is the same for all agents. With one seat, if $p_1 \le 1$ both agents demand $\{1\}$ and $z_1 = 2 - 1 = 1$; if $p_1 > 1$ neither does, the price is positive, and $z_1 = 0 - 1 = -1$. In both cases $\alpha = 1$.

With three students, let $B$ be the common demand. If $1 \in B$, then $d_1 = 3$ and $z_1 = 2$. If $1 \notin B$, then $\{1\}$ is not affordable, because it is ranked above $\{2\}$ and the empty bundle; so $p_1 > 1 \ge 0$, $d_1 = 0$ and $z_1 = -1$. In both cases $\alpha(p) \ge |z_1| \ge 1$. $\square$

**Claim 6 (distinct budgets can clear).** In the example with one seat and budgets $b_1 < b_2$, every price $p_1 \in (b_1, b_2]$ has $\alpha = 0$; with budgets $(1, 11/10)$ and step $1/20$, the search returns $\alpha = 0$ and $p_1 = 21/20$. In the example with three students and budgets $(1, 11/10, 6/5)$, the prices $(9/8, 0)$ have $\alpha = 0$, and the search with step $1/40$ returns them.

*Proof.* With one seat and $b_1 < p_1 \le b_2$, only agent 2 can pay for $\{1\}$, so $d_1 = 1$ and $z_1 = 0$. The grid values in $(1, 11/10]$ are $21/20$ and $22/20$; every smaller grid value has $\alpha = 1$ by the case analysis of Claim 5 (both agents demand the seat), so by Claim 3 the first vector with error $0$ is $21/20$.

With three students and $p = (9/8, 0)$: students 1 and 2 have budgets below $9/8$, so they cannot pay for $\{1, 2\}$ or $\{1\}$, and they demand $\{2\}$, which costs $0$. Student 3 has $6/5 \ge 9/8$ and demands $\{1, 2\}$. So $d = (1, 3)$ and $z = (0, 0)$. To see that it is the first vector of the grid with error $0$, note that error $0$ needs exactly one student to demand a bundle with course 1. If $p_1 \le 11/10$, then students 2 and 3 can pay for $\{1\}$ and both demand a bundle with course 1, so $d_1 \ge 2$. Hence $p_1 > 11/10$, and the smallest grid value above $11/10$ with step $1/40$ is $45/40 = 9/8$; with $p_2 = 0$ the error is $0$, and $(9/8, 0)$ comes first in lexicographic order among the vectors with $p_1 = 9/8$. By Claim 3, the search returns it. $\blacksquare$

The bound $\sqrt{\sigma m} / 2$ that the implementation computes is the bound of Budish's theorem; the toy does not reach it in general, because a coarse grid can miss the prices that the theorem promises.
