---
title: LSH answers the (c, r)-near neighbor query with constant probability
proves: [correctness]
status: full
---

Let $\mathcal{H}$ be $(r, c r, p_1, p_2)$-sensitive with $0 < p_2 < p_1 \le 1$ and $\rho = \ln(1/p_1)/\ln(1/p_2)$. Let $|P| = n \ge 1$, $k = \lceil \log_{1/p_2} n \rceil$ and $L = \lceil n^\rho / p_1 \rceil$. The functions $h_{j,i}$ of line L2 are independent. Fix a query $q$.

**Claim 1 (no far answer).** If LSH-QUERY returns a point $x$, then $\delta(q, x) \le c r$.

*Proof.* The only line that returns a point is L9, and it does so only when $\delta(q, x) \le c r$. $\square$

So if no point is within $c r$, the query returns none, which is the correct answer. From now on assume that $p^* \in P$ has $\delta(q, p^*) \le r$.

**Claim 2.** Let $E_1$ be the event that $g_j(p^*) = g_j(q)$ for some $j$. Then $\Pr[E_1] \ge 1 - 1/e$.

*Proof.* For one table, $\Pr[g_j(p^*) = g_j(q)] = \prod_{i=1}^{k} \Pr[h_{j,i}(p^*) = h_{j,i}(q)] \ge p_1^k$, by independence and the sensitivity for $\delta \le r$. Since $k < \log_{1/p_2} n + 1$ and $p_1 \le 1$,

$$p_1^k \ge p_1^{\log_{1/p_2} n + 1} = p_1 \cdot n^{\log_{1/p_2} p_1} = p_1 \cdot n^{-\rho}.$$

Here $\log_{1/p_2} p_1 = \ln p_1 / \ln(1/p_2) = -\rho$. So $L p_1^k \ge (n^\rho / p_1) \cdot p_1 n^{-\rho} = 1$. The tables are independent, so $\Pr[\text{not } E_1] \le (1 - p_1^k)^L \le e^{-L p_1^k} \le e^{-1}$, using $1 - x \le e^{-x}$. $\square$

**Claim 3.** Let $F = \{x \in P : \delta(q, x) > c r\}$, and let $Z$ be the number of pairs $(j, x)$ with $x \in F$ and $g_j(x) = g_j(q)$. Let $E_2$ be the event $Z < 3L$. Then $\Pr[E_2] \ge 2/3$.

*Proof.* For $x \in F$, $\delta(q, x) \ge c r$, so each function collides with probability at most $p_2$, and $\Pr[g_j(x) = g_j(q)] \le p_2^k \le p_2^{\log_{1/p_2} n} = 1/n$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[Z] \le L \cdot |F| \cdot (1/n) \le L$. By Markov's inequality, $\Pr[Z \ge 3L] \le \mathbb{E}[Z]/(3L) \le 1/3$. $\square$

**Claim 4.** If $E_1$ and $E_2$ hold, the query returns a point within $c r$.

*Proof.* Each increment of line L8 counts one pair $(j, x)$ with $x$ in the bucket of $q$ in table $j$. Assume the query does not return a point. Then line L9 never succeeded, so each counted pair has $x \in F$, and the count is at most $Z < 3L$. So line L10 never stopped the query, and the loops of lines L6 and L7 ran to the end and counted every pair of every bucket of $q$. By $E_1$ the pair $(j, p^*)$ for some $j$ is among them, and $p^* \notin F$. This contradicts the fact that each counted pair has $x \in F$. So the query returns a point, which is within $c r$ by Claim 1. $\square$

**Theorem.** If some point of $P$ is within $r$ of $q$, LSH-QUERY returns a point within $c r$ of $q$ with probability at least $2/3 - 1/e > 0.29$. If no point is within $c r$, it returns none with probability 1.

*Proof.* The second part is Claim 1. For the first, by Claim 4 and the union bound, the failure probability is at most $\Pr[\text{not } E_1] + \Pr[\text{not } E_2] \le 1/e + 1/3$, and $1 - 1/e - 1/3 = 2/3 - 1/e \approx 0.2988$. $\blacksquare$

**Termination and cost.** The loop of line L6 runs $L$ times, and the inner loop stops after at most $3L$ increments in total by line L10, or at the end of a finite bucket. So the query computes at most $3L$ distances and $Lk$ hash values.
