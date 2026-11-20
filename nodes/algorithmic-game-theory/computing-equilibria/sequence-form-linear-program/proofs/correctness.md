---
title: The sequence-form LP gives the value of a zero-sum game with perfect recall and optimal strategies for both players
proves: [correctness]
status: full
---

Let $T$ be a finite two-player zero-sum game tree with chance moves and perfect recall, with payoffs $u(\ell)$ to player 1. Let $S_1, S_2$, $E, e$, $F, f$ and $A$ be as built in lines L1 to L3, so that $X = \{x : E x = e, x \ge 0\}$ and $Y = \{y : F y = f, y \ge 0\}$. Write (P) for the LP of lines L4 and L5: maximize $q_\emptyset = f^{\mathsf T} q$ subject to $F^{\mathsf T} q - A^{\mathsf T} x \le 0$, $E x = e$, $x \ge 0$, $q$ free.

**Lemma 1 (realization plans).** For every behavior strategy $\beta$ of player 1, the vector $x_\beta(\sigma) = \prod_{(h, a) \in \sigma} \beta(h, a)$ is in $X$. Conversely, for every $x \in X$ there is a behavior strategy $\beta$ with $x_\beta = x$.

*Proof.* $x_\beta(\emptyset) = 1$ is the empty product. For $h \in H_1$, $\sum_a x_\beta(\sigma_h a) = x_\beta(\sigma_h) \sum_a \beta(h, a) = x_\beta(\sigma_h)$, and all entries are nonnegative. Conversely, given $x \in X$, let $\beta(h, a) = x(\sigma_h a) / x(\sigma_h)$ if $x(\sigma_h) > 0$, and the uniform distribution otherwise. By the constraint of row $h$, this is a distribution on $A(h)$. We show $x_\beta(\sigma) = x(\sigma)$ by induction on the length of $\sigma$. It holds for $\emptyset$. Let $\sigma = \sigma_h a$, with $x_\beta(\sigma_h) = x(\sigma_h)$ by induction; here perfect recall is used, because $\sigma_h$ is one sequence and the last pair of $\sigma$ is $(h, a)$. If $x(\sigma_h) > 0$, then $x_\beta(\sigma) = x(\sigma_h) \beta(h, a) = x(\sigma)$. If $x(\sigma_h) = 0$, then $x(\sigma) = 0$ because $0 \le x(\sigma_h a) \le \sum_{a'} x(\sigma_h a') = 0$, and $x_\beta(\sigma) = 0 \cdot \beta(h, a) = 0$. $\square$

The same holds for player 2 and $Y$.

**Lemma 2 (payoff).** If player 1 plays a behavior strategy $\beta_1$ and player 2 plays $\beta_2$, the expected payoff to player 1 is $x_{\beta_1}^{\mathsf T} A\, y_{\beta_2}$.

*Proof.* The probability of reaching a leaf $\ell$ is the product of the probabilities of the moves on its path. The chance moves give $c(\ell)$, the moves of player 1 give $\prod_{(h, a) \in \sigma_1(\ell)} \beta_1(h, a) = x_{\beta_1}(\sigma_1(\ell))$, and those of player 2 give $y_{\beta_2}(\sigma_2(\ell))$. Here $\sigma_i(\ell)$ is the sequence of player $i$ on the path, and the moves of player $i$ on the path are exactly the pairs of $\sigma_i(\ell)$. So the expected payoff is $\sum_\ell c(\ell)\, u(\ell)\, x(\sigma_1(\ell))\, y(\sigma_2(\ell))$, and grouping the leaves by the pair $(\sigma_1(\ell), \sigma_2(\ell))$ gives $\sum_{\sigma_1, \sigma_2} x(\sigma_1) A(\sigma_1, \sigma_2) y(\sigma_2)$, by the definition of $A$ in line L2. $\square$

By Lemmas 1 and 2, every pair $(x, y) \in X \times Y$ is the pair of realization plans of a pair of behavior strategies with expected payoff $x^{\mathsf T} A y$. By Kuhn's theorem, in a game with perfect recall every mixed strategy has a behavior strategy with the same payoff against every strategy of the other player, so it suffices to consider behavior strategies. Hence $x \in X$ guarantees player 1 at least $\min_{y \in Y} x^{\mathsf T} A y$ against every strategy of player 2, and the same for player 2.

**Lemma 3 (inner problem).** For each $x \in X$, the largest $q_\emptyset$ over the $q$ with $F^{\mathsf T} q \le A^{\mathsf T} x$ is $\min_{y \in Y} x^{\mathsf T} A y$.

*Proof.* The LP $\min \{(A^{\mathsf T} x)^{\mathsf T} y : F y = f, y \ge 0\}$ is feasible, because $Y$ contains the plan of any pure strategy, and bounded, because $Y$ is bounded: every entry of $y$ is at most 1, by induction along the sequences, since $y(\sigma_h a) \le y(\sigma_h)$. So it has an optimum. Its dual is $\max \{f^{\mathsf T} q : F^{\mathsf T} q \le A^{\mathsf T} x\}$ with $q$ free, and by strong duality the two optimal values are equal. $\square$

**Theorem.** (P) has an optimal solution $(q^*, x^*)$. Its value $v = q^*_\emptyset$ is the value of the game, $x^*$ is an optimal realization plan of player 1, and the vector $y^*$ of dual prices of the inequality rows of (P) is an optimal realization plan of player 2.

*Proof.* By Lemma 3, (P) is $\max_{x \in X} \min_{y \in Y} x^{\mathsf T} A y$, the maximum of a continuous function on a nonempty compact set, so it has an optimum, and $x^*$ attains the maximin. The dual of (P) has a nonnegative variable $y_\tau$ for each inequality row and a free variable $p_k$ for each row of $E$. The columns of $q$, which are free, give the equations $F y = f$. The columns of $x$, which are nonnegative, give $E^{\mathsf T} p - A y \ge 0$. The objective is $e^{\mathsf T} p = p_\emptyset$. So the dual is: minimize $p_\emptyset$ subject to $E^{\mathsf T} p \ge A y$, $y \in Y$, $p$ free. For a fixed $y$, this is the dual of $\max \{(A y)^{\mathsf T} x : x \in X\}$, so by the argument of Lemma 3 with the players exchanged, the dual of (P) computes $\min_{y \in Y} \max_{x \in X} x^{\mathsf T} A y$, and its optimal $y^*$ attains this minimax. By strong duality for (P), both values equal $v$. So $\min_y x^{*\mathsf T} A y = v = \max_x x^{\mathsf T} A y^*$: $x^*$ guarantees $v$ and $y^*$ holds player 1 to $v$, which is the definition of the value and of optimal strategies. The dual prices returned by the solver satisfy the dual constraints and have value $v$ (the shared LP code returns duals with $\sum_i b_i \cdot \text{dual}_i$ equal to the value and $A^{\mathsf T} \text{dual} \ge c$), so they are an optimal solution of the dual. $\square$

**Perfect recall check.** Line L1 rejects a tree in which two nodes of one information set have different own sequences. Lemma 1 uses exactly this property, so the theorem holds for every tree that the code accepts.
