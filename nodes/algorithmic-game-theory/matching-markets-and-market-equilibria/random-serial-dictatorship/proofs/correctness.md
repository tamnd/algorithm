---
title: Random serial dictatorship is ex post efficient, strategyproof and treats equals equally
proves: [correctness, termination]
status: full
---

Fix agents $1, \dots, n$, objects $O$, and a strict list of acceptable objects for each agent. For an order $\pi$ of the agents, let $SD(\pi)$ be the output of lines L2 to L8 with that order. Write $\succ_i$ for the preference of agent $i$, where every listed object is better than nothing and nothing is better than an unlisted object. Let $P_{io}$ be the probability that agent $i$ gets object $o$.

**Termination.** Line L1 makes $n - 1$ swaps. Lines L2 to L8 are serial dictatorship, which makes $n$ passes over finite lists. So the algorithm stops.

**Claim 1 (the order is uniform).** Line L1 returns each of the $n!$ orders with probability $1/n!$. *Proof.* The Fisher-Yates shuffle picks the entry of the last position uniformly from all $n$ agents, then the entry of the position before it uniformly from the $n - 1$ agents left, and so on. Each order comes from exactly one sequence of choices, and each sequence has probability $1/(n(n-1)\cdots 2) = 1/n!$. $\square$

So the output is $SD(\pi)$ for a uniform random order $\pi$, and $P_{io} = |\{\pi : SD(\pi)(i) = o\}| / n!$.

**Claim 2 (ex post efficiency).** The set of matchings that the algorithm outputs with positive probability is the set of Pareto optimal matchings. *Proof.* By Claim 1, the matchings with positive probability are the matchings $SD(\pi)$ over all orders $\pi$. The proof file of serial dictatorship shows that each $SD(\pi)$ is Pareto optimal and that each Pareto optimal matching equals $SD(\pi)$ for some $\pi$. $\square$

**Claim 3 (strategyproofness for each order).** Fix an order $\pi$ and an agent $i$. Let $SD(\pi)$ use the true list of $i$, and let $\widehat{SD}(\pi)$ use any other list of $i$, with the lists of the others unchanged. Then $SD(\pi)(i) \succeq_i \widehat{SD}(\pi)(i)$. *Proof.* Let $i = \pi(k)$. Passes $1, \dots, k - 1$ read only the lists of the agents before $i$, so the set $T$ of taken objects at the turn of $i$ is the same in both runs. With its true list, $i$ gets its best acceptable object outside $T$, or nothing if there is none. With the other list it gets an object outside $T$ or nothing. If that object is acceptable to $i$, it is at most as good as the best acceptable object outside $T$. If it is not acceptable, or nothing, then the true outcome, which is an acceptable object or nothing, is at least as good. $\square$

**Strategyproofness in the sense of stochastic dominance.** Let $o_1 \succ_i o_2 \succ_i \cdots \succ_i o_r$ be the true list of $i$, let $P$ be the matrix under the true list and $\hat P$ the matrix under another list. For each $k \le r$, Claim 3 shows that for every order $\pi$, if $\widehat{SD}(\pi)(i) \in \{o_1, \dots, o_k\}$ then $SD(\pi)(i) \in \{o_1, \dots, o_k\}$. Counting orders and dividing by $n!$ gives
$$\sum_{l \le k} P_{i o_l} \ge \sum_{l \le k} \hat P_{i o_l} \quad \text{for } k = 1, \dots, r.$$
So the true row stochastically dominates every false row. For any utility $u_i$ with $u_i(o_1) > \cdots > u_i(o_r) > u_i(\emptyset) = 0$ and $u_i$ of an unlisted object at most 0, the expected utility is a positive combination of these partial sums (summation by parts), so truth-telling also maximizes the expected utility.

**Claim 4 (equal treatment of equals).** If agents $i$ and $j$ have the same list, then $P_{io} = P_{jo}$ for every object $o$. *Proof.* Let $\tau$ swap $i$ and $j$, and for an order $\pi$ let $\pi' = \tau \circ \pi$, the order with $i$ and $j$ exchanged. The map $\pi \mapsto \pi'$ is a bijection of the orders. In the run on $\pi'$, at each step the agent that picks has the same list as the agent that picks at the same step of the run on $\pi$, so the same objects are taken in the same steps. Hence $SD(\pi')(j) = SD(\pi)(i)$. Counting the orders gives $P_{jo} = P_{io}$. $\square$

**Claim 5 (bistochastic for complete lists with $n = m$).** If $n = m$ and every list contains every object, then each row and each column of $P$ sums to 1. *Proof.* In each run, when agent $\pi(k)$ picks, $k - 1 < m$ objects are taken, so a free object is on its list. Hence every agent gets an object, and since $n = m$ every object is given. So $\sum_o P_{io} = 1$ and $\sum_i P_{io} = 1$. $\blacksquare$

**Cost of one draw.** Line L1 costs $O(n)$. The proof file of serial dictatorship bounds lines L2 to L8 by $O(m + n^2)$: the $k$-th agent reads at most $k$ entries of its list.
