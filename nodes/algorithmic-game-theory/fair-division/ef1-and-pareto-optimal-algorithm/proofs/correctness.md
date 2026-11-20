---
title: When the exact BKV algorithm returns, its allocation is EF1 and Pareto optimal
proves: [correctness]
status: partial
---

**Setting.** There are $n \ge 1$ agents and $m$ goods with values $v_{ij} > 0$. We refer to the lines L1 to L12 of the page and use its terms: prices $p_j$, spending $p(S)$, MBB ratio $\beta_i = \max_j v_{ij}/p_j$, MBB condition, least spender with spending $p_{\min}$, pEF1, hierarchy $H$ and path violator. This proof shows partial correctness: if the algorithm returns, the allocation is EF1 and Pareto optimal. It does not prove that the exact form ends. For the rounded form, Barman, Krishnamurthy and Vaish prove termination in $\mathrm{poly}(m, n, 1/\varepsilon, \ln v_{\max})$ time (Lemma 4 of their paper).

**Lemma 1 (prices stay positive).** At every step $p_j > 0$ for every good $j$.

*Proof.* Line L1 sets $p_j = v_{kj} > 0$. A swap does not change prices. A rise multiplies some prices by $\alpha$, and Lemma 3 below shows $\alpha > 1$. $\square$

**Lemma 2 (MBB condition).** At every step each agent owns only goods of its MBB set.

*Proof.* After line L1, the owner $k$ of good $j$ has $v_{kj}/p_j = 1$, and every agent $i$ has $v_{ij'}/p_{j'} = v_{ij'}/v_{k'j'} \le 1$ for every good $j'$ with owner $k'$, because $k'$ values $j'$ most. So $\beta_k = 1$ and $j$ is an MBB good of $k$.

A swap of line L6 gives $j$ to an agent $g$ for which $j$ is an MBB good, and changes no prices, so all MBB sets stay the same.

A rise of line L10 multiplies by $\alpha$ the prices of the goods owned in $H$. By the construction of the hierarchy, every MBB good of an agent of $H$ is owned by an agent of $H$. For $h \in H$, the ratios of the goods owned in $H$ drop by the factor $\alpha$, so the ratio of its own goods becomes $\beta_h/\alpha$. A good $j$ owned outside $H$ keeps its price, and $\alpha \le \alpha_1 \le \beta_h p_j / v_{hj}$ gives $v_{hj}/p_j \le \beta_h/\alpha$. So the goods of $h$ are still MBB goods of $h$. For $k \notin H$, the goods of $k$ keep their prices and the other prices do not drop, so the goods of $k$ are still MBB goods of $k$. $\square$

**Lemma 3 (a rise has $\alpha > 1$).** When line L7 is reached, $\alpha_1 > 1$, $\alpha_3 > 1$ and $\alpha_2 > 1$, wherever they are defined, and at least one is defined.

*Proof.* Line L7 is reached only if the allocation is not pEF1 and no path violator exists. All least spenders are at level 0 of $H$, so every $k \notin H$ has $p(x_k) > p_{\min}$, which gives $\alpha_3 > 1$. A good $j$ owned outside $H$ is not an MBB good of any $h \in H$, since otherwise its owner would be in $H$; so $v_{hj}/p_j < \beta_h$ and $\alpha_1 > 1$.

Every agent $h \in H$ has $p(x_h) - \max_{j \in x_h} p_j \le p_{\min}$. At level 0 this holds because $p(x_h) = p_{\min}$. At a level $\ell \ge 1$, agent $h$ owns a good $j$ that is an MBB good of an agent at level $\ell - 1$, and since $h$ is not a path violator, $p(x_h) - \max_{j' \in x_h} p_{j'} \le p(x_h \setminus \{j\}) \le p_{\min}$. Since the allocation is not pEF1, some agent $k$ has $p(x_k) - \max_{j \in x_k} p_j > p_{\min}$, and so $k \notin H$. If $p_{\min} > 0$, then $\alpha_2$ and $\alpha_3$ are defined, and $\alpha_2 \ge (p(x_k) - \max_{j \in x_k} p_j)/p_{\min} > 1$. If $p_{\min} = 0$, the least spenders own no goods, $\alpha_2$ and $\alpha_3$ are not defined, and $\alpha_1$ is defined because the violator $k \notin H$ owns goods outside $H$. $\square$

**Lemma 4 (the output is pEF1).** When the loop exits, the allocation is pEF1 for the current prices.

*Proof.* If it exits in line L3, this is the test of that line. Otherwise it exits in line L11 after a rise with $\alpha = \alpha_2$. Write $q$ for the prices before the rise, $p$ for the prices after it, and $q_{\min}$ for the least spending before it. Every agent of $H$ had spending at least $q_{\min}$ and now has $\alpha$ times its old spending, so at least $\alpha q_{\min}$. Every agent $k \notin H$ keeps its spending, which is at least $\alpha_3 q_{\min} \ge \alpha q_{\min}$. So the new least spending is $p_{\min} = \alpha q_{\min}$, reached by the old least spenders.

Now check every agent $k$. If $k \notin H$, its spending minus its most expensive good is unchanged and at most $\alpha_2 q_{\min} = p_{\min}$ by the definition of $\alpha_2$. If $k \in H$, the proof of Lemma 3 gave $q(x_k) - \max_{j \in x_k} q_j \le q_{\min}$, and all prices of $x_k$ were multiplied by $\alpha$, so $p(x_k) - \max_{j \in x_k} p_j \le \alpha q_{\min} = p_{\min}$. Hence the allocation is pEF1. $\square$

**Lemma 5 (pEF1 with the MBB condition gives EF1; Lemma 2 of the paper with $\varepsilon = 0$).** If $x$ satisfies the MBB condition and is pEF1 for prices $p > 0$, then $x$ is EF1.

*Proof.* Fix agents $i \ne k$ with $x_k \ne \emptyset$, and let $j$ be a most expensive good of $x_k$. For any set $S$, $v_i(S) = \sum_{j' \in S} v_{ij'} \le \beta_i\, p(S)$, and by the MBB condition $v_i(x_i) = \beta_i\, p(x_i)$. pEF1 gives $p(x_i) \ge p_{\min} \ge p(x_k \setminus \{j\})$. So $v_i(x_i) = \beta_i p(x_i) \ge \beta_i p(x_k \setminus \{j\}) \ge v_i(x_k \setminus \{j\})$. $\square$

**Lemma 6 (MBB condition gives Pareto optimality; the first welfare theorem).** If $x$ satisfies the MBB condition for prices $p > 0$, then no fractional allocation $y$ has $v_i(y_i) \ge v_i(x_i)$ for every agent with strict inequality for some agent.

*Proof.* Suppose $y$ is such an allocation, where $y_{ij} \ge 0$ is the share of good $j$ given to $i$ and $\sum_i y_{ij} = 1$. For each agent, $v_i(y_i) = \sum_j v_{ij} y_{ij} \le \beta_i \sum_j p_j y_{ij}$, and $v_i(x_i) = \beta_i p(x_i)$ with $\beta_i > 0$. So $\sum_j p_j y_{ij} \ge p(x_i)$ for every agent, with strict inequality for the agent that is strictly better off. Summing over the agents gives $\sum_j p_j > \sum_j p_j$, a contradiction. $\square$

**Theorem.** If the algorithm returns an allocation, the allocation contains every good once, is EF1, and is Pareto optimal, even against fractional allocations.

*Proof.* Line L1 gives every good to one agent, and swaps move goods between agents, so every good stays in exactly one bundle. By Lemma 1 the prices are positive, by Lemma 2 the MBB condition holds, and by Lemma 4 the output is pEF1. Lemma 5 gives EF1 and Lemma 6 gives Pareto optimality, since an integral allocation is a special fractional one. $\blacksquare$

Termination of the exact form is not proved here. Barman, Krishnamurthy and Vaish prove that the rounded form ends in $\mathrm{poly}(m, n, 1/\varepsilon, \ln v_{\max})$ time and that, for their choice of $\varepsilon$, its output is EF1 and PO for the original values (Lemmas 3 to 5 and Theorem 1 of their paper).
