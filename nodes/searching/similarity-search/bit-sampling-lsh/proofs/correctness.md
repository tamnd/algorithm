---
title: Bit sampling answers the (c, r)-near neighbor query with constant probability
proves: [correctness]
status: full
---

Let $P \subseteq \{0,1\}^d$ with $|P| = n \ge 1$, let $c > 1$ and $0 < cr < d$, and let $H$ be the Hamming distance. Put $p_1 = 1 - r/d$, $p_2 = 1 - cr/d$, $\rho = \ln(1/p_1)/\ln(1/p_2)$, $k = \lceil \ln n / \ln(1/p_2) \rceil$ and $L = \lceil n^\rho / p_1 \rceil$. The positions of line L2 are independent and uniform. Fix a query $q$. Write $g_j(x)$ for the key of $x$ in table $j$.

**Claim 1.** If the query returns $x$, then $H(q, x) \le cr$.

*Proof.* The only line that returns a string is L6, after the test $H(q, x) \le cr$. $\square$

So if no string is within $cr$, the answer none is correct. From now on let $p^* \in P$ have $H(q, p^*) \le r$.

**Claim 2.** For one uniform position $i$, $\Pr[x[i] = y[i]] = 1 - H(x, y)/d$.

*Proof.* The bits of $x$ and $y$ differ at exactly $H(x, y)$ of the $d$ positions, and $i$ is uniform over the $d$ positions. $\square$

**Claim 3.** $\Pr[g_j(p^*) = g_j(q)] \ge p_1^k$, and $\Pr[g_j(x) = g_j(q)] \le p_2^k \le 1/n$ for each $x$ with $H(q, x) > cr$.

*Proof.* The $k$ positions of table $j$ are independent, so the key probability is the product of $k$ equal factors $1 - H/d$ from Claim 2. For $p^*$, each factor is at least $1 - r/d = p_1$. For $x$ with $H(q,x) > cr$, each factor is less than $1 - cr/d = p_2$. Finally $k \ge \ln n / \ln(1/p_2)$ gives $p_2^k \le e^{-\ln n} = 1/n$. $\square$

**Claim 4.** Let $E_1$ be the event that $g_j(p^*) = g_j(q)$ for some $j$. Then $\Pr[E_1] \ge 1 - 1/e$.

*Proof.* Since $k < \ln n / \ln(1/p_2) + 1$ and $p_1 \le 1$,
$$p_1^k \ge p_1 \cdot p_1^{\ln n / \ln(1/p_2)} = p_1 \cdot e^{-\ln n \cdot \ln(1/p_1)/\ln(1/p_2)} = p_1 n^{-\rho}.$$
So $L p_1^k \ge 1$. The tables are independent, so $\Pr[\text{not } E_1] \le (1 - p_1^k)^L \le e^{-L p_1^k} \le 1/e$. $\square$

**Claim 5.** Let $Z$ be the number of pairs $(j, x)$ with $H(q, x) > cr$ and $g_j(x) = g_j(q)$, and let $E_2$ be the event $Z < 3L$. Then $\Pr[E_2] \ge 2/3$.

*Proof.* By Claim 3 and linearity of expectation, $\mathbb{E}[Z] \le L \cdot n \cdot (1/n) = L$. By Markov's inequality, $\Pr[Z \ge 3L] \le 1/3$. $\square$

**Claim 6.** If $E_1$ and $E_2$ hold, the query returns a string within $cr$.

*Proof.* Assume the query returns none. Then the test of line L6 failed for every counted pair, so every counted pair $(j, x)$ has $H(q, x) > cr$ and is counted in $Z$. So the count stays below $3L$, line L7 never stops the loop, and line L5 visits every pair of every bucket of $q$. By $E_1$ one of them is $(j, p^*)$ with $H(q, p^*) \le r \le cr$, and line L6 returns it. This is a contradiction. So the query returns a string, which is within $cr$ by Claim 1. $\square$

**Conclusion.** By the union bound, $\Pr[E_1 \text{ and } E_2] \ge 1 - 1/e - 1/3 = 2/3 - 1/e > 0.29$. By Claim 6 the query then returns a string within $cr$. Together with Claim 1 this proves the theorem.

**The exponent.** Let $x = r/d$, so $0 < cx < 1$. Bernoulli's inequality gives $(1 - x)^c \ge 1 - cx$ for real $c \ge 1$ and $0 \le x \le 1$. Taking logarithms, $c \ln(1 - x) \ge \ln(1 - cx)$, and dividing by the negative number $c \ln(1 - cx)$ gives $\rho = \ln(1 - x)/\ln(1 - cx) \le 1/c$. So $L = O(n^{1/c}/p_1)$. $\blacksquare$
