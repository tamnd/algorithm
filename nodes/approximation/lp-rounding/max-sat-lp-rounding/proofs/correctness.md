---
title: LP rounding for MAX-SAT gives 1 − 1/e, and the better of LP rounding and a fair random assignment gives 3/4 of the LP value
proves: [correctness]
status: full
---

**Statement.** Let $C_1, \ldots, C_m$ be clauses on $x_1, \ldots, x_n$ with weights $w_j \ge 0$, where each clause has $k_j \ge 1$ literals on different variables, $P_j$ the variables that appear positive and $N_j$ those that appear negated. Let $(y, z)$ be an optimal solution of the LP of the page, with value $\text{LP}^* = \sum_j w_j z_j$. Let $a$ set each $x_i$ true with probability $y_i$, and $b$ with probability $1/2$, all independently, and let $\beta_k = 1 - (1 - 1/k)^k$. Then:

1. $\mathbb{E}[W(a)] \ge \sum_j \beta_{k_j} w_j z_j \ge (1 - 1/e) \cdot \text{LP}^*$;
2. $\mathbb{E}[W(b)] = \sum_j (1 - 2^{-k_j}) w_j \ge \sum_j (1 - 2^{-k_j}) w_j z_j$;
3. $\mathbb{E}[\max(W(a), W(b))] \ge \tfrac12 (\mathbb{E}[W(a)] + \mathbb{E}[W(b)]) \ge \tfrac34 \cdot \text{LP}^* \ge \tfrac34 \cdot \text{OPT}$.

**Step 0: OPT is at most LP*.** For an assignment $c$, set $y_i = c_i$ and $z_j = 1$ if $c$ satisfies $C_j$ and $z_j = 0$ otherwise. A satisfied clause has a true literal, so the left side of its constraint is at least 1. So the point is feasible, with value $W(c)$. Hence $\text{OPT} \le \text{LP}^*$.

**Step 1: one clause under LP rounding.** Fix $C_j$ with $k = k_j$ and $z = z_j$. The clause is false when each positive variable is false and each negated variable is true. The variables are different and independent, so

$$\Pr[C_j \text{ false}] = \prod_{i \in P_j} (1 - y_i) \prod_{i \in N_j} y_i.$$

The $k$ factors are in $[0, 1]$. By the inequality of arithmetic and geometric means, the product is at most the $k$-th power of their mean, and by the LP constraint that mean is at most $1 - z/k$:

$$\Pr[C_j \text{ false}] \le \Big( \frac{1}{k} \Big( \sum_{i \in P_j} (1 - y_i) + \sum_{i \in N_j} y_i \Big) \Big)^k = \Big( 1 - \frac{1}{k} \Big( \sum_{i \in P_j} y_i + \sum_{i \in N_j} (1 - y_i) \Big) \Big)^k \le \Big( 1 - \frac{z}{k} \Big)^k.$$

The last step uses that $t \mapsto t^k$ is increasing on $[0, 1]$ and that $0 \le 1 - z/k$.

**Step 2: concavity.** Let $g(z) = 1 - (1 - z/k)^k$ on $[0, 1]$. Its second derivative is $-\frac{k - 1}{k} (1 - z/k)^{k-2} \le 0$, so $g$ is concave. A concave function on $[0, 1]$ lies above the chord between its end points, and $g(0) = 0$, $g(1) = \beta_k$, so $g(z) \ge \beta_k z$. With step 1, $\Pr[C_j \text{ satisfied}] \ge g(z_j) \ge \beta_{k_j} z_j$.

**Step 3: the bound $1 - 1/e$.** For $k \ge 1$, $(1 - 1/k)^k \le e^{-1}$, because $1 - t \le e^{-t}$. So $\beta_k \ge 1 - 1/e$. By linearity of expectation and step 2,

$$\mathbb{E}[W(a)] = \sum_j w_j \Pr[C_j \text{ satisfied}] \ge \sum_j \beta_{k_j} w_j z_j \ge (1 - 1/e) \sum_j w_j z_j.$$

This proves item 1.

**Step 4: the fair assignment.** Under $b$, each of the $k_j$ literals of $C_j$ is false with probability $1/2$, independently, so $C_j$ is satisfied with probability $1 - 2^{-k_j}$. Since $z_j \le 1$ and $w_j \ge 0$, linearity of expectation gives item 2.

**Step 5: the average.** For a clause of length $k$, let $\gamma_k = \tfrac12 (\beta_k + 1 - 2^{-k})$. By steps 2 and 4, the average of the two probabilities of satisfying $C_j$ is at least $\gamma_{k_j} z_j$. We show $\gamma_k \ge 3/4$ for all $k \ge 1$:

- $k = 1$: $\beta_1 = 1$ and $1 - 2^{-1} = 1/2$, so $\gamma_1 = 3/4$.
- $k = 2$: $\beta_2 = 1 - 1/4 = 3/4$ and $1 - 2^{-2} = 3/4$, so $\gamma_2 = 3/4$.
- $k \ge 3$: $\beta_k \ge 1 - 1/e > 0.632$ and $1 - 2^{-k} \ge 7/8 = 0.875$, so $\gamma_k > \tfrac12 (0.632 + 0.875) > 0.75$.

So $\tfrac12 (\mathbb{E}[W(a)] + \mathbb{E}[W(b)]) \ge \sum_j \gamma_{k_j} w_j z_j \ge \tfrac34 \text{LP}^*$.

**Step 6: the better of two.** For each outcome, $\max(W(a), W(b)) \ge \tfrac12 (W(a) + W(b))$. Taking expectations and using step 5 and step 0,

$$\mathbb{E}[\max(W(a), W(b))] \ge \tfrac12 (\mathbb{E}[W(a)] + \mathbb{E}[W(b)]) \ge \tfrac34 \text{LP}^* \ge \tfrac34 \text{OPT}.$$

This proves item 3. The deterministic form fixes the variables of each rounding by conditional expectations, which gives assignments $a'$ and $b'$ with $W(a') \ge \mathbb{E}[W(a)]$ and $W(b') \ge \mathbb{E}[W(b)]$, and the better of them has $\max(W(a'), W(b')) \ge \tfrac12 (W(a') + W(b')) \ge \tfrac34 \text{LP}^*$. $\blacksquare$
