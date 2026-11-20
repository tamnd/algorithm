---
title: The toy scaling algorithm keeps Delta-feasibility, converges to the equilibrium and returns it exactly
proves: [correctness, termination]
status: full
---

This proof is for the toy of the pseudocode: the scaling algorithm with the exact check of line L8. It does not prove the strongly polynomial bound of StrongScaling, which needs the perturbation and the MakeFertile step of Orlin's paper.

Fix buyers $B$ and goods $G$, one unit of each good, $n = |B| + |G| \ge 2$, budgets $e_i > 0$ and utilities $u_{ij} \ge 0$, where every buyer likes some good and every good is liked by some buyer. Write $u_{iG} = \sum_k u_{ik}$, $c_i = e_i - \sum_j x_{ij}$ and $b_j = \sum_i x_{ij} - p_j$. A good is *raised* once its price has gone above $p^0_j$. Line L1 sets $p^0_j = \max_i u_{ij} e_i / (n u_{iG})$, which is positive because some buyer likes good $j$. We say that $(p, x)$ is *$\Delta$-feasible* when

(F1) $c_i \ge 0$ for every buyer; (F2) $b_j \le \Delta$ for every good, and $b_j \ge 0$ for every raised good; (F3) every $x_{ij} > 0$ is on an equality edge at $p$ and is a multiple of $\Delta$; (F4) $x \ge 0$ and $p \ge p^0$.

This is Orlin's definition, with the upper bound of (F2) stated for all goods. All arithmetic is exact.

**Claim 1 (soundness of line L8).** If line L8 returns $(p', x)$, then $(p', x)$ is a Fisher market equilibrium.

*Proof.* The check accepts only positive prices with $\sum_j p'_j = \sum_i e_i$ and a flow of value $\sum_i e_i$ in the network source $\to j$ (capacity $p'_j$) $\to i$ (only on edges of maximum bang per buck of $i$ at $p'$) $\to$ sink (capacity $e_i$). The source arcs and the sink arcs both have total capacity $\sum_i e_i$, so all of them are saturated. The returned $x_{ij}$ is the flow on the arc $j \to i$. So buyer $i$ spends exactly $e_i$, only on goods of maximum bang per buck, which makes her bundle optimal for linear utilities, and good $j$ receives exactly $p'_j$, so it is sold completely. $\square$

**Claim 2 (one price step of line L5).** Let $(p, x)$ be $\Delta$-feasible, let $A$ be the set that line L4 finds from a root $r$, and suppose that every good of $A$ has $b_j > 0$. Then line L5 finds a factor $q > 1$, the new prices keep $\Delta$-feasibility, and the set of line L4 at the new prices contains $A$ and either has a good with $b_j \le 0$ or has a good that $A$ does not have.

*Proof.* The root has an equality edge, so $A$ has a good. For a good $j \in A$ the candidate $\sum_i x_{ij} / p_j$ is greater than $1$ because $b_j > 0$. For a buyer $i \in A$ and a good $j \notin A$ with $u_{ij} > 0$, the edge $(i, j)$ is not an equality edge (otherwise $j$ would be in $A$), so $u_{ij} / p_j < \alpha_i$, where $\alpha_i$ is the maximum bang per buck of $i$, and the candidate $\alpha_i p_j / u_{ij}$ is greater than $1$. So the minimum $q$ exists and $q > 1$.

If $i \in A$ and $x_{ij} > 0$, then $(i, j)$ is an equality edge by (F3), so $j \in A$. If $j \in A$ and $x_{ij} > 0$, then $i \in A$ by the arcs from goods to buyers. So every edge with $x_{ij} > 0$ has both ends in $A$ or both ends outside $A$.

Every buyer $i \in A$ has all her equality goods in $A$. After the step, the bang per buck of $i$ on goods of $A$ is divided by $q$, and on a good $j \notin A$ it is $u_{ij} / p_j \le \alpha_i / q$ by the choice of $q$. So the new maximum of $i$ is $\alpha_i / q$, and all her old equality edges into $A$ stay equality edges. A buyer $i \notin A$ with some $x_{ij} > 0$ has $j \notin A$, so her maximum is attained at a good whose price did not change; her maximum does not change, and her edges with money stay equality edges. So (F3) holds. Prices only rise, so (F4) holds, and $x$ does not change, so (F1) holds. For a good $j \in A$, the new $b_j = \sum_i x_{ij} - q p_j \ge 0$ by the choice of $q$, and it is smaller than the old $b_j \le \Delta$, so (F2) holds.

The equality edges inside $A$ and the money flows do not change, so every node of $A$ is still reachable. If $q$ was attained by a good of $A$, that good now has $b_j = 0$. Otherwise $q$ was attained by a buyer $i \in A$ and a good $j \notin A$, and $(i, j)$ is now an equality edge, so $j$ is reachable. $\square$

By Claim 2, the loop of lines L4 and L5 stops after at most $|G|$ price steps, because the set of reachable goods grows at every step that does not stop it.

**Claim 3 (the augmentation of line L6).** Let $(p, x)$ be $\Delta$-feasible with $c_r \ge \Delta$, and let line L6 send $\Delta$ along the path to a good $j$ with $b_j \le 0$. Then $(p, x)$ stays $\Delta$-feasible, $c_r$ goes down by $\Delta$, and no other $c_i$ changes.

*Proof.* The path comes from a breadth-first search tree, so it is simple. It starts at $r$, alternates between forward arcs (buyer to good, on equality edges) and backward arcs (good to buyer, with $x_{ij} > 0$), and ends at $j$. A forward arc gets $+\Delta$ and stays an equality edge. A backward arc has $x_{ij} > 0$, a multiple of $\Delta$, so $x_{ij} \ge \Delta$, and it gets $-\Delta$ and stays nonnegative. Every flow stays a multiple of $\Delta$, so (F3) and (F4) hold. A good inside the path gets $+\Delta$ from the buyer before it and $-\Delta$ toward the buyer after it, and a buyer inside the path gets $-\Delta$ from the good before it and $+\Delta$ toward the good after it, so their totals do not change. The root spends $\Delta$ more, so $c_r$ goes from at least $\Delta$ to at least $0$. The end good goes from $b_j \le 0$ to $b_j \le \Delta$; if it is raised, then (F2) gave $b_j \ge 0$, so $b_j = 0$ before and $\Delta$ after. $\square$

**Claim 4 (line L9).** If $(p, x)$ is $\Delta$-feasible with every $c_i < \Delta$, then after line L9 it is $\Delta'$-feasible for $\Delta' = \Delta / 2$, and every buyer has $c_i < (2 + k_i) \Delta'$, where $k_i$ is the number of flows of buyer $i$ that line L9 lowered.

*Proof.* Multiples of $\Delta$ are multiples of $\Delta'$, and the prices do not change. A good with $b_j > \Delta'$ has $\sum_i x_{ij} > p_j > 0$, so some $x_{ij} > 0$; it is a positive multiple of $2 \Delta'$, so after subtracting $\Delta'$ it is still a positive multiple of $\Delta'$ on the same equality edge. The good then has $b_j \in (0, \Delta']$, since it had $b_j \le \Delta = 2\Delta'$. The goods that were not repaired have $b_j \le \Delta'$, and the raised ones still have $b_j \ge 0$. Each good is repaired at most once, and each repair raises $c_i$ of one buyer by $\Delta'$, so $c_i < \Delta + k_i \Delta' = (2 + k_i) \Delta'$. $\square$

**Claim 5 (each phase ends).** Line L1 gives a $\Delta$-feasible start, every call of PriceAndAugment ends, and every phase ends with a $\Delta$-feasible $(p, x)$ with all $c_i < \Delta$. From the second phase on, a phase makes at most $n$ calls, and during a phase, line L9 at its start included, every $x_{ij}$ changes by at most $(n + 1) \Delta$ in total.

*Proof.* With $x = 0$ and $p = p^0$, (F1), (F3) and (F4) hold, no good is raised, and $b_j = -p^0_j < 0$. By Claims 2 and 3, every call ends and keeps $\Delta$-feasibility, and each call lowers $\sum_i c_i \ge 0$ by $\Delta$, so line L3 stops after finitely many calls with all $c_i < \Delta$. By Claim 4, the next phase starts $\Delta'$-feasible.

In a later phase with step $\Delta'$, the money $c_i$ of buyer $i$ changes only in calls with root $i$, each time by $-\Delta'$, so by Claim 4 the number of these calls is at most $\lfloor c_i / \Delta' \rfloor \le 1 + k_i$. The total is at most $|B| + \sum_i k_i \le |B| + |G| = n$, because each good is repaired at most once. Each call changes each $x_{ij}$ by at most $\Delta'$ (the path is simple), and line L9 changes each $x_{ij}$ by at most $\Delta'$. $\square$

**Claim 6 (convergence).** Let $p^k$ and $x^k$ be the values at the end of the phase $k$, with step $\Delta_k$. Then $p^k \to \bar{p}$ and $x^k \to \bar{x}$, and $(\bar{p}, \bar{x})$ is a Fisher market equilibrium. So $\bar{p} = p^*$, the unique equilibrium prices.

*Proof.* Prices only rise. A raised good has $b_j \ge 0$, so $p_j \le \sum_i x_{ij} \le \sum_i e_i$, and a good that is not raised has $p_j = p^0_j$. So the prices are bounded and $p^k \to \bar{p} \ge p^0 > 0$. By Claim 5, $|x^{l}_{ij} - x^{l-1}_{ij}| \le (n + 1) \Delta_l$ for $l \ge 2$, and $\Delta_l = \Delta_k / 2^{l - k}$, so $|x^l_{ij} - x^k_{ij}| \le (n + 1) \Delta_k$ for all $l > k \ge 1$. So $x^k$ is a Cauchy sequence, $x^k \to \bar{x}$, and
$$
|x^k_{ij} - \bar{x}_{ij}| \le (n + 1) \Delta_k \quad \text{for } k \ge 1 .
$$

Buyers: $0 \le c_i < \Delta_k \to 0$, so every buyer spends $\sum_j \bar{x}_{ij} = e_i$. If $\bar{x}_{ij} > 0$, then $x^k_{ij} > 0$ for all large $k$, so $(i, j)$ is an equality edge at $p^k$, that is $u_{ij} / p^k_j \ge u_{il} / p^k_l$ for all $l$ with $u_{il} > 0$. These inequalities pass to the limit, so $(i, j)$ is an equality edge at $\bar{p}$. Goods: $b_j \le \Delta_k \to 0$, so $\sum_i \bar{x}_{ij} \le \bar{p}_j$ for every good, and for a raised good also $b_j \ge 0$, so $\sum_i \bar{x}_{ij} = \bar{p}_j$.

It remains to show that every good is raised at some time. Suppose good $j$ is never raised, so $\bar{p}_j = p^0_j$. Let $i$ be the buyer with $p^0_j = u_{ij} e_i / (n u_{iG})$. At $\bar{p}$, buyer $i$ has maximum bang per buck $\alpha_i \ge u_{ij} / p^0_j = n u_{iG} / e_i$, and she spends $e_i$ only on goods with bang per buck $\alpha_i$, so she gets utility $\alpha_i e_i \ge n u_{iG}$. But she gets the amount $\bar{x}_{ik} / \bar{p}_k \le 1$ of each good $k$, so her utility is at most $\sum_k u_{ik} = u_{iG} < n u_{iG}$. This is a contradiction. This argument plays the role of Lemma 3.3 of Orlin.

So every good is sold completely at $\bar{p}$, every buyer spends her budget on goods of maximum bang per buck, and $(\bar{p}, \bar{x})$ is an equilibrium with the money flows $\bar{x}$. The equilibrium prices of a linear Fisher market are unique (Eisenberg and Gale), so $\bar{p} = p^*$. $\square$

**Claim 7 (line L8 returns).** The algorithm returns after finitely many phases.

*Proof.* Let $S^* = \{(i, j) : \bar{x}_{ij} > 0\}$ and $\beta$ its smallest entry. Take $k$ so large that $(5n + 1) \Delta_k \le \beta$. By Claim 6, an edge outside $S^*$ has $x^k_{ij} \le (n + 1) \Delta_k < 4n \Delta_k$, and an edge in $S^*$ has $x^k_{ij} \ge \beta - (n + 1) \Delta_k \ge 4n \Delta_k$. So line L7 finds $S = S^*$.

Every buyer spends $e_i > 0$ and every good receives $p^*_j > 0$ in $\bar{x}$, so $S^*$ touches every node. Every edge of $S^*$ is an equality edge at $p^*$, so $u_{ij} / p^*_j = \alpha_i$. In one connected part of $S^*$, `basic_prices` gives the first good the value $1$, a buyer reached from a good with value $t$ the value $u_{ij} / t$, and a good reached from a buyer with value $s$ the value $u_{ij} / s$. By induction along the search, if a good has value $\lambda p^*_j$ then the next buyer has value $\alpha_i / \lambda$ and the next good has value $\lambda p^*_{j'}$, with the same $\lambda$ in the whole part. So the values are consistent and the function does not return None. In $\bar{x}$, the buyers of a part spend all their money on goods of the same part, and those goods get money only from buyers of that part, so the prices $p^*_j$ of a part add up to the budgets of its buyers. The scaling of `basic_prices` therefore gives exactly $p^*$. The prices $p^*$ are positive, add up to $\sum_i e_i$, and the flow given by $\bar{x}$ has value $\sum_i e_i$, which is the largest possible, so the check accepts. Hence line L8 returns at the latest at phase $k$, and by Claim 1 its answer is an equilibrium. $\blacksquare$

Orlin's paper perturbs the utilities so that the equilibrium allocation is unique and its support is a forest, and then shows that the prices of the support are the answer. The toy does not perturb, so the support that it guesses can give wrong prices at an early phase, as at $\Delta = 1/32$ in the example of the page; the exact check of line L8 rejects them, and Claim 7 shows that the right support appears.
