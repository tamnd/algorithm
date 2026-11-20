---
title: The best of the n LPs is the leader's optimal commitment, and it is at least every Nash equilibrium payoff
proves: [correctness, termination]
status: full
---

Let $(A, B)$ be an $m \times n$ bimatrix game with the leader as the row player. For $x \in \Delta_m$ let $\mathrm{BR}(x) = \arg\max_k (B^{\mathsf T} x)_k$, the set of the follower's pure best responses, and let the leader's commitment payoff be $V(x) = \max_{k \in \mathrm{BR}(x)} (A^{\mathsf T} x)_k$ (ties broken for the leader). The goal is $V^* = \sup_{x \in \Delta_m} V(x)$ and an $x$ that attains it. For each $j$, let $R_j = \{x \in \Delta_m : j \in \mathrm{BR}(x)\}$, which is the feasible set of LP_j, and let $v_j = \max_{x \in R_j} (A^{\mathsf T} x)_j$ when $R_j \ne \emptyset$.

**Lemma 1 (the LPs are well defined).** Each $R_j$ is a polytope, possibly empty, and the sets $R_1, \ldots, R_n$ cover $\Delta_m$. Each LP_j with $R_j \ne \emptyset$ has an optimum.

*Proof.* $R_j$ is the simplex cut by the $n - 1$ linear inequalities $(B^{\mathsf T} x)_k \le (B^{\mathsf T} x)_j$, so it is a bounded polyhedron. For every $x$, the set $\mathrm{BR}(x)$ is nonempty because it is the set of maximizers of a finite list, so $x$ lies in some $R_j$. A linear function on a nonempty polytope attains its maximum. $\square$

**Theorem.** Let $j^*$ be a column with the largest $v_j$ and $x^*$ an optimal solution of LP_$j^*$, as returned by lines L1 to L5. Then $V(x^*) = v_{j^*} = V^*$, and the follower's tie-broken best response to $x^*$ gives the leader exactly $v_{j^*}$.

*Proof.* Upper bound: for any $x$, let $k \in \mathrm{BR}(x)$ be the follower's choice. Then $x \in R_k$, so $(A^{\mathsf T} x)_k \le v_k \le v_{j^*}$. Hence $V(x) \le v_{j^*}$ for all $x$. Attainment: $x^* \in R_{j^*}$, so $j^* \in \mathrm{BR}(x^*)$ and $V(x^*) \ge (A^{\mathsf T} x^*)_{j^*} = v_{j^*}$. With the upper bound, $V(x^*) = v_{j^*}$, so $V^* = v_{j^*}$ is attained at $x^*$. If the tie rule picks some $k \in \mathrm{BR}(x^*)$, the leader gets $V(x^*) = v_{j^*}$ by the definition of $V$. $\square$

**Termination.** The loop runs $n$ times, and each LP is solved by the simplex method with Bland's rule, which ends on every input.

**Proposition (pure follower responses suffice).** If the follower may also play a mixed best response $y$, the leader's best payoff for a fixed $x$ is still $V(x)$.

*Proof.* A mixed best response $y$ puts weight only on $\mathrm{BR}(x)$, by the best response condition, so $x^{\mathsf T} A y = \sum_k y_k (A^{\mathsf T} x)_k \le \max_{k \in \mathrm{BR}(x)} (A^{\mathsf T} x)_k = V(x)$. $\square$

**Proposition (commitment beats Nash).** For every Nash equilibrium $(\hat x, \hat y)$ of $(A, B)$, $V^* \ge \hat x^{\mathsf T} A \hat y$.

*Proof.* In the equilibrium $\hat y$ is a best response to $\hat x$, so by the previous proposition $\hat x^{\mathsf T} A \hat y \le V(\hat x) \le V^*$. $\square$

The same argument with $\hat x$ pure shows that $V^*$ is at least the value of every pure commitment.

**Proposition (zero-sum games).** If $B = -A$, then $V^*$ equals the value $v$ of the matrix game $A$.

*Proof.* For $B = -A$, the follower's best responses to $x$ minimize $(A^{\mathsf T} x)_k$, so $V(x) = \min_k (A^{\mathsf T} x)_k$ and $V^* = \max_x \min_k (A^{\mathsf T} x)_k$, which is the maximin value. By the minimax theorem it equals $v$. $\square$
