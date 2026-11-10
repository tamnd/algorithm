---
title: The threshold algorithm for online knapsack is (1 + ln(U/L))-competitive for small items, and no online algorithm does better
proves: [correctness]
status: full
---

We use the pseudocode of the page. The capacity is 1. Item $i$ has weight $w_i \in (0, \varepsilon]$ and value $v_i$, and its density $e_i = v_i / w_i$ lies in $[L, U]$ with $0 < L < U$. Let $c = 1/(1 + \ln(U/L))$, so $\ln(Ue/L) = 1/c$, and

$$\Psi(z) = L \text{ for } 0 \le z \le c, \qquad \Psi(z) = \Bigl(\frac{Ue}{L}\Bigr)^{z} \frac{L}{e} \text{ for } c \le z \le 1.$$

At $z = c$ both forms give $(Ue/L)^c (L/e) = e \cdot L/e = L$, and $\Psi(1) = U$. So $\Psi$ is continuous and non-decreasing. We assume $\varepsilon \le 1 - c$; this is the small items assumption. $S$ is the set of items taken, $z_i$ is the used fraction just before item $i$, $Z$ is the final used fraction, $\mathrm{ALG} = \sum_{i \in S} v_i$, and $O$ is an optimal set of items with value $\mathrm{OPT}$. We write $\beta = (Ue/L)^{-\varepsilon}$, a number in $(0, 1]$ that tends to 1 as $\varepsilon \to 0$.

**Claim 1 (feasibility).** The items of $S$ fit: $Z = \sum_{i \in S} w_i \le 1$.

*Proof.* Line L4 takes an item only if $z_i + w_i \le 1$, and $z$ grows by exactly $w_i$. $\square$

**Claim 2 (area identity).** For $c \le Z \le 1$, $\int_0^Z \Psi(z)\,dz = c\,\Psi(Z)$.

*Proof.* With $\lambda = \ln(Ue/L) = 1/c$,

$$\int_0^Z \Psi = Lc + \frac{L}{e} \int_c^Z e^{\lambda z} dz = Lc + \frac{1}{\lambda}\Bigl(\Psi(Z) - \Psi(c)\Bigr) = Lc + c\bigl(\Psi(Z) - L\bigr) = c\,\Psi(Z). \qquad \square$$

The identity is where the shape of $\Psi$ comes from: $\Psi$ is the function for which the value already collected, at least the area under $\Psi$, is a fixed fraction $c$ of the current threshold.

**Claim 3 (the value collected).** $\mathrm{ALG} \ge \sum_{i \in S} \Psi(z_i) w_i \ge \beta \int_0^Z \Psi(z)\,dz$.

*Proof.* Each taken item has $v_i = e_i w_i \ge \Psi(z_i) w_i$ by L4. The taken items fill the intervals $[z_i, z_i + w_i]$, which tile $[0, Z]$. On such an interval, $\Psi(z) / \Psi(z_i) \le (Ue/L)^{z - z_i} \le (Ue/L)^{\varepsilon}$: on the flat part the quotient is 1, on the exponential part it is exactly $(Ue/L)^{z - z_i}$, and across $c$ it is $(Ue/L)^{z - c}$, which is smaller. So $\Psi(z_i) w_i \ge \beta \int_{z_i}^{z_i + w_i} \Psi$, and we sum over $S$. $\square$

**Claim 4 (the items that were refused).** Either every item was taken, or one of these holds.

1. No item was refused for lack of room. Then each $i \in O \setminus S$ has $e_i < \Psi(z_i) \le \Psi(Z)$.
2. Some item was refused for lack of room. Then $Z > 1 - \varepsilon \ge c$, and each $i \in O \setminus S$ has $e_i \le U \le \Psi(Z) / \beta$.

*Proof.* An item is refused by L4 because its density is below the threshold or because it does not fit. In case 1 only the first reason occurs, and $\Psi$ is non-decreasing. In case 2 some item with $w_i \le \varepsilon$ did not fit, so $z_i > 1 - \varepsilon$, and $Z \ge z_i$. Then $\Psi(Z) \ge \Psi(1 - \varepsilon) = U (Ue/L)^{-\varepsilon} = \beta U$, because $1 - \varepsilon \ge c$. $\square$

**Theorem 1 (upper bound).** If every density is in $[L, U]$ and every weight is at most $\varepsilon \le 1 - c$, then

$$\mathrm{OPT} \le \Bigl(1 + \ln \frac{U}{L}\Bigr) \Bigl(\frac{Ue}{L}\Bigr)^{2\varepsilon} \mathrm{ALG},$$

which tends to $(1 + \ln(U/L))\,\mathrm{ALG}$ as $\varepsilon \to 0$.

*Proof.* If every item was taken, $\mathrm{ALG} \ge \mathrm{OPT}$. If no item was refused for lack of room and $Z < c$, then at each arrival $z_i \le Z < c$, so $\Psi(z_i) = L \le e_i$, and every item was taken. So we may assume $Z \ge c$ and one of the cases of Claim 4, and we set $T = \Psi(Z)$ in case 1 and $T = \Psi(Z)/\beta$ in case 2. Then each $i \in O \setminus S$ has $e_i \le T$.

Split $O$ into $O \cap S$, with value $A$ and weight $W$, and $O \setminus S$, with weight at most $1 - W$. Then $\mathrm{OPT} \le A + T(1 - W)$. Write $\mathrm{ALG} = A + B$, where $B$ is the value of $S \setminus O$. If $T(1 - W) \le B$, then $\mathrm{OPT} \le \mathrm{ALG}$. Otherwise the fraction $(A + T(1-W))/(A + B)$ decreases as $A$ grows, so it does not get smaller when $A$ is replaced by the smaller number $A' = \sum_{i \in O \cap S} \Psi(z_i) w_i$. Now $A' \le \Psi(Z) W \le T W$, so the new numerator is at most $T$. The new denominator is $A' + B \ge \sum_{i \in S} \Psi(z_i) w_i \ge \beta\, c\, \Psi(Z)$ by Claims 3 and 2. So

$$\frac{\mathrm{OPT}}{\mathrm{ALG}} \le \frac{T}{\beta c \Psi(Z)} \le \frac{1}{\beta^2 c} = \Bigl(1 + \ln\frac{U}{L}\Bigr)\Bigl(\frac{Ue}{L}\Bigr)^{2\varepsilon}. \qquad \square$$

The fractional knapsack optimum is at least $\mathrm{OPT}$, and the same proof bounds it, because the bound $\mathrm{OPT} \le A + T(1 - W)$ holds for fractional solutions too. The tests check the bound against the fractional optimum.

**Theorem 2 (lower bound, all online algorithms).** Fix $L < U$ and an integer $N \ge 1$, and let $p_k = L (U/L)^{k/N}$ for $k = 0, \ldots, N$. Each online algorithm, deterministic, or randomized against an oblivious adversary, has ratio at least $1 + N\bigl(1 - (L/U)^{1/N}\bigr)$, and this tends to $1 + \ln(U/L)$ as $N \to \infty$. The bound holds for items of any small size.

*Proof.* Fix $m \ge 1$. Batch $k$ is $m$ items of weight $1/m$ and density $p_k$. The input $\sigma_k$ is batches $0, 1, \ldots, k$. The batches have rising density and each one fills the knapsack, so $\mathrm{OPT}(\sigma_k) = p_k$. All inputs $\sigma_k$ share their prefixes, so the algorithm behaves the same on batches $0, \ldots, k$ in all inputs $\sigma_j$ with $j \ge k$. Let $f_k$ be the expected used fraction after batch $k$ and $a_k$ the expected value after batch $k$, with $f_{-1} = a_{-1} = 0$. All items of batch $k$ have density $p_k$, so in each run the value gained in batch $k$ is $p_k$ times the weight gained, and so $a_k - a_{k-1} = p_k (f_k - f_{k-1})$. Let $\alpha$ be the ratio, so $a_k \ge p_k / \alpha$ for each $k$. By summation by parts,

$$1 \ge f_N = \sum_{k=0}^{N} \frac{a_k - a_{k-1}}{p_k} = \frac{a_N}{p_N} + \sum_{k=0}^{N-1} a_k \Bigl(\frac{1}{p_k} - \frac{1}{p_{k+1}}\Bigr) \ge \frac{1}{\alpha} + \frac{1}{\alpha} \sum_{k=0}^{N-1} \Bigl(1 - \frac{p_k}{p_{k+1}}\Bigr).$$

Each term of the last sum is $1 - (L/U)^{1/N}$. So $\alpha \ge 1 + N (1 - (L/U)^{1/N})$. As $N \to \infty$, $N(1 - e^{-\ln(U/L)/N}) \to \ln(U/L)$. $\square$

For $U/L = 10$ and $N = 10$ the bound is $3.0567$, and the limit is $1 + \ln 10 = 3.3026$. Theorem 2 shows that the threshold algorithm is optimal among all online algorithms, also randomized ones, up to the factor $(Ue/L)^{2\varepsilon}$ that disappears for small items. $\blacksquare$
