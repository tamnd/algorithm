---
title: Some pair of k-uniform strategies is an epsilon-Nash equilibrium, so the search succeeds
proves: [correctness]
status: full
---

Let $(A, B)$ be an $m \times n$ bimatrix game with all entries in $[0, 1]$, where $m$ and $n$ are the numbers of pure strategies of the row player and of the column player. A mixed strategy is **$k$-uniform** if it is the uniform distribution on a multiset of $k$ pure strategies, so that each probability is a multiple of $1/k$. A pair $(x, y)$ is an $\varepsilon$-Nash equilibrium if $\max_r (Ay)_r - x^{\mathsf T} A y \le \varepsilon$ and $\max_c (x^{\mathsf T} B)_c - x^{\mathsf T} B y \le \varepsilon$. Pure deviations are enough here, because the payoff of a mixed deviation is an average of payoffs of pure deviations.

**Lemma 1 (Hoeffding).** Let $X_1, \dots, X_k$ be independent random variables with values in $[0, 1]$ and the same mean $\mu$, and let $\bar X = \frac1k \sum_t X_t$. For every $t > 0$, $\Pr[|\bar X - \mu| \ge t] \le 2 e^{-2 k t^2}$.

This is the [Hoeffding inequality](/hoeffding-inequality/), used here without proof.

**Lemma 2 (best response fact).** If $(x^*, y^*)$ is a Nash equilibrium, then $(A y^*)_r = \max_{r'} (A y^*)_{r'}$ for every $r$ with $x^*_r > 0$, and $(x^{*\mathsf T} B)_c = \max_{c'} (x^{*\mathsf T} B)_{c'}$ for every $c$ with $y^*_c > 0$.

*Proof.* $x^{*\mathsf T} A y^*$ is the average of the numbers $(A y^*)_r$ with weights $x^*_r$. If a row of the support earned less than the maximum, moving its weight to a best row would raise the average, so $x^*$ would not be a best response. The same holds for the column player. $\square$

**Theorem 1 (existence of a k-uniform approximate equilibrium).** Let $(x^*, y^*)$ be any Nash equilibrium, with payoffs $v_A = x^{*\mathsf T} A y^*$ and $v_B = x^{*\mathsf T} B y^*$. If $k > 2 \ln(2(m + n)) / \varepsilon^2$, there is a pair $(x', y')$ of $k$-uniform strategies with supports inside the supports of $x^*$ and $y^*$ such that $(x', y')$ is an $\varepsilon$-Nash equilibrium, and moreover $|x'^{\mathsf T} A y' - v_A| \le \varepsilon/2$ and $|x'^{\mathsf T} B y' - v_B| \le \varepsilon/2$.

*Proof.* A Nash equilibrium exists by [Nash's theorem](/nash-existence-theorem/). Draw rows $r_1, \dots, r_k$ independently from $x^*$, and columns $c_1, \dots, c_k$ independently from $y^*$. Let $x'$ be uniform on the multiset $\{r_1, \dots, r_k\}$ and $y'$ uniform on $\{c_1, \dots, c_k\}$. Every $r_t$ is in the support of $x^*$ and every $c_s$ in the support of $y^*$.

Fix a row $r$. Then $(A y')_r = \frac1k \sum_s A_{r c_s}$ is the mean of $k$ independent values in $[0, 1]$, each with mean $\sum_c y^*_c A_{rc} = (A y^*)_r$. By Lemma 1 with $t = \varepsilon/2$, $|(A y')_r - (A y^*)_r| \ge \varepsilon/2$ has probability at most $2 e^{-k \varepsilon^2 / 2}$. In the same way, for a fixed column $c$, $|(x'^{\mathsf T} B)_c - (x^{*\mathsf T} B)_c| \ge \varepsilon/2$ has probability at most $2 e^{-k \varepsilon^2/2}$. By the [union bound](/union-bound/) over the $m$ rows and the $n$ columns, the probability that at least one of these $m + n$ events happens is at most $2(m + n) e^{-k \varepsilon^2 / 2}$, which is less than 1 because $k \varepsilon^2 / 2 > \ln(2(m + n))$. So with positive probability, and therefore for at least one outcome of the draws, the event $E$ holds:

$$|(A y')_r - (A y^*)_r| < \varepsilon/2 \text{ for all rows } r, \qquad |(x'^{\mathsf T} B)_c - (x^{*\mathsf T} B)_c| < \varepsilon/2 \text{ for all columns } c.$$

Fix such an outcome. *Row player.* By $E$ and Lemma 2, $\max_r (A y')_r < \max_r (A y^*)_r + \varepsilon/2 = v_A + \varepsilon/2$. Also

$$x'^{\mathsf T} A y' = \frac1k \sum_t (A y')_{r_t} > \frac1k \sum_t \big((A y^*)_{r_t} - \varepsilon/2\big) = v_A - \varepsilon/2,$$

because each $r_t$ is in the support of $x^*$, so $(A y^*)_{r_t} = v_A$ by Lemma 2. So the row gain is less than $\varepsilon$. *Column player.* In the same way, $\max_c (x'^{\mathsf T} B)_c < v_B + \varepsilon/2$, and $x'^{\mathsf T} B y' = \frac1k \sum_s (x'^{\mathsf T} B)_{c_s} > v_B - \varepsilon/2$, because each $c_s$ is in the support of $y^*$. So the column gain is less than $\varepsilon$.

*Payoffs.* We showed $x'^{\mathsf T} A y' > v_A - \varepsilon/2$, and $x'^{\mathsf T} A y' \le \max_r (A y')_r < v_A + \varepsilon/2$. The same holds for $B$. $\square$

**Theorem 2 (correctness of the search).** Let $k$ be the value of line L1, the least integer with $k > 2 \ln(2(m + n)) / \varepsilon^2$. Then the algorithm returns a pair, and every pair it returns is a $k$-uniform $\varepsilon$-Nash equilibrium.

*Proof.* Lines L2 and L4 go through all multisets of $k$ rows and all multisets of $k$ columns, so lines L3 and L5 produce every pair of $k$-uniform strategies. Line L6 compares $\max_r (Ay)_r - x^{\mathsf T} A y$ and $\max_c (x^{\mathsf T} B)_c - x^{\mathsf T} B y$ with $\varepsilon$, which is the definition of an $\varepsilon$-Nash equilibrium (pure deviations are enough). So a returned pair is an $\varepsilon$-Nash equilibrium. By Theorem 1 at least one pair passes line L6, so the loops do not end without a return. $\square$

**Running time.** There are $\binom{m + k - 1}{k}$ multisets of $k$ rows and $\binom{n + k - 1}{k}$ multisets of $k$ columns. For each column multiset the code computes $k \cdot A y$ and its maximum in $O(km)$ time, and for each row multiset it computes $k \cdot x^{\mathsf T} B$ and its maximum in $O(kn)$ time. Then one pair costs $O(k)$: the payoff $k^2 \, x^{\mathsf T} A y$ is the sum of $k$ entries of $k \cdot A y$, and in the same way for $B$. The total is
$$O\Big(\tbinom{m+k-1}{k}\tbinom{n+k-1}{k}\, k + \big(\tbinom{m+k-1}{k} + \tbinom{n+k-1}{k}\big)\, k (m + n)\Big).$$
Since $\binom{n + k - 1}{k} \le (n + k)^k$ and $k = O(\log(m + n)/\varepsilon^2)$, this is $(m + n)^{O(\log(m + n)/\varepsilon^2)}$, which is quasi-polynomial for every fixed $\varepsilon$.
