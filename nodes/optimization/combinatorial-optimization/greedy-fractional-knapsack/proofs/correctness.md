---
title: The ratio greedy returns an optimal solution of the fractional knapsack problem
proves: [correctness, termination, optimality]
status: full
---

Let the items be numbered in the order of line L1, so $v_1/w_1 \ge v_2/w_2 \ge \cdots \ge v_n/w_n$, with all $w_i > 0$, all $v_i \ge 0$ and $W \ge 0$. The primal linear program (P) and its dual (D) are

$$ \text{(P)} \quad \max \sum_i v_i x_i \ \text{ s.t. } \ \sum_i w_i x_i \le W, \ 0 \le x_i \le 1, $$

$$ \text{(D)} \quad \min \ W\lambda + \sum_i \mu_i \ \text{ s.t. } \ \lambda w_i + \mu_i \ge v_i \ (\text{all } i), \ \lambda \ge 0, \ \mu \ge 0. $$

**Lemma 1 (weak duality).** If $x$ is feasible for (P) and $(\lambda, \mu)$ is feasible for (D), then $\sum_i v_i x_i \le W\lambda + \sum_i \mu_i$.

*Proof.* Since $x_i \ge 0$ and $v_i \le \lambda w_i + \mu_i$, we get $\sum_i v_i x_i \le \lambda \sum_i w_i x_i + \sum_i \mu_i x_i$. Since $\lambda \ge 0$ and $\sum_i w_i x_i \le W$, the first term is at most $\lambda W$. Since $\mu_i \ge 0$ and $x_i \le 1$, the second term is at most $\sum_i \mu_i$. $\square$

**Lemma 2 (termination and feasibility).** The algorithm stops after at most $n$ iterations, and its output $x$ is feasible for (P), with $\sum_i v_i x_i$ equal to the returned total.

*Proof.* The loop runs over $i = 1, \ldots, n$, so it stops. Before each iteration, $r = W - \sum_{j < i} w_j x_j \ge 0$: this holds at the start by line L2, and line L5 runs only when $w_i \le r$, so it keeps $r \ge 0$. In line L5, $x_i = 1$. Line L7 runs only when $w_i > r \ge 0$, so $x_i = r / w_i \in [0, 1)$, and after it $\sum_{j \le i} w_j x_j = W - r + r = W$. The items not reached keep $x_j = 0$. So $\sum_i w_i x_i \le W$ and $0 \le x_i \le 1$. Every change to $x_i$ adds $v_i x_i$ to the total, so the total is $\sum_i v_i x_i$. $\square$

**Theorem.** The output $x$ is an optimal solution of (P).

*Proof.* There are two cases.

*Case 1: line L9 returns.* Then every item fits, $x = (1, \ldots, 1)$ and the total is $\sum_i v_i$. Every feasible $x'$ has $x'_i \le 1$ and $v_i \ge 0$, so $\sum_i v_i x'_i \le \sum_i v_i$. The output is optimal. (In the dual, $\lambda = 0$ and $\mu_i = v_i$ give the same value.)

*Case 2: line L8 returns at item $k$.* Then $x_i = 1$ for $i < k$, $x_k = r_k / w_k$ where $r_k = W - \sum_{i<k} w_i$, and $x_i = 0$ for $i > k$. Set $\lambda = v_k / w_k \ge 0$ and $\mu_i = v_i - \lambda w_i$ for $i < k$, $\mu_i = 0$ for $i \ge k$.

Dual feasibility. For $i < k$, $v_i / w_i \ge \lambda$ by the order, so $\mu_i \ge 0$, and $\lambda w_i + \mu_i = v_i$. For $i = k$, $\lambda w_k = v_k$. For $i > k$, $v_i / w_i \le \lambda$, so $\lambda w_i \ge v_i$ with $\mu_i = 0$.

Equal values. The dual value is

$$ W\lambda + \sum_{i<k} (v_i - \lambda w_i) = \sum_{i<k} v_i + \lambda \Big( W - \sum_{i<k} w_i \Big) = \sum_{i<k} v_i + \frac{v_k}{w_k} r_k = \sum_{i<k} v_i + v_k x_k, $$

which is the greedy total by Lemma 2. By Lemma 1, no feasible $x'$ has a larger value. So $x$ is optimal. $\square$

**Remark (ties).** The proof uses only that the order of line L1 is non-increasing in the ratio. So any order of the items with equal ratios gives an optimal $x$, and all these $x$ have the same value.

**A second proof, by exchange.** Let $x^*$ be any optimal solution, and suppose that some $i < j$ in the order have $x^*_i < 1$ and $x^*_j > 0$. Move weight $\delta = \min((1 - x^*_i) w_i, x^*_j w_j) > 0$ from item $j$ to item $i$: raise $x^*_i$ by $\delta / w_i$ and lower $x^*_j$ by $\delta / w_j$. The weight does not change, the bounds $0 \le x \le 1$ still hold, and the value changes by $\delta (v_i/w_i - v_j/w_j) \ge 0$. Each move makes $x^*_i = 1$ or $x^*_j = 0$, so the number of pairs $(i, j)$ with $i < j$, $x^*_i < 1$ and $x^*_j > 0$ goes down, and after finitely many moves there are none. Then $x^*$ is a prefix of whole items, one part item and zeros after it. While $\sum_i w_i x^*_i < W$ and some $x^*_i < 1$, raise the first such $x^*_i$ until it is 1 or the capacity is full. This does not lower the value, because $v_i \ge 0$, and it keeps the form. At the end, $x^*$ is optimal, has the form above, and is either all ones or fills the capacity exactly. Only one vector has these properties, and it is the greedy output. $\blacksquare$
