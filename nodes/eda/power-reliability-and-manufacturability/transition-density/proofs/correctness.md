---
title: The transition density formula for independent inputs, and exactness of the gate-by-gate pass without reconvergence
proves: [correctness]
status: full
---

**Model.** A logic signal is a random function $x : \mathbb{R} \to \{0, 1\}$ that is right-continuous and has finitely many transitions in every bounded interval. Write $N_x$ for the random set of its transition times and $N_x(A)$ for the number of them in a set $A$. The signal is *stationary* when the law of $(x(t + s))_{t}$ does not depend on $s$; then $P(x(t) = 1) = p_x$ for every $t$ and $E[N_x((a, b])] = D(x)\,(b - a)$ for a constant $D(x)$, the transition density, which we assume finite. Signals are *independent* when they are independent as random functions.

**Lemma 1 (no common transitions).** If $x$ and $z$ are independent stationary signals with finite densities, then with probability 1 they have no transition time in common.

*Proof.* For a fixed instant $t$, $E[N_z(\{t\})] = \lim_{h \to 0} E[N_z((t - h, t])] = \lim_{h \to 0} D(z) h = 0$, so $P(t \in N_z) = 0$. Condition on $x$. Its transition times in $(0, T]$ form a finite set that is independent of $z$, so the expected number of them that are also transitions of $z$ is a finite sum of zeros. Taking expectations and letting $T \to \infty$ over the integers gives the claim. $\square$

**Lemma 2 (sampling at independent instants).** Let $N$ be a random set of instants with $E[N((0, T])] = D T$, and let $Z$ be a stationary 0-1 signal independent of $N$. Then

$$ E\Big[\sum_{t \in N \cap (0, T]} Z(t)\Big] \;=\; D\, T\, P(Z = 1). $$

*Proof.* Condition on $N$. The sum then has finitely many terms $Z(t_1), \ldots, Z(t_m)$ at fixed instants, and since $Z$ is independent of $N$ and stationary, $E[Z(t_k) \mid N] = P(Z = 1)$ for each $k$. So the conditional expectation is $m\,P(Z = 1) = N((0, T])\,P(Z = 1)$, and its expectation is $D T\,P(Z = 1)$. $\square$

**Theorem 1 (one block).** Let $x_1, \ldots, x_n$ be independent stationary signals with finite densities, $f : \{0,1\}^n \to \{0,1\}$, and $y(t) = f(x_1(t - \tau), \ldots, x_n(t - \tau))$ for a fixed delay $\tau \ge 0$. Then $y$ is stationary and

$$ D(y) \;=\; \sum_{i=1}^n P\!\left(\frac{\partial f}{\partial x_i}(X) = 1\right) D(x_i), $$

where $X$ has independent coordinates with $P(X_i = 1) = p_{x_i}$.

*Proof.* The vector signal $(x_1, \ldots, x_n)$ is stationary because its coordinates are independent and stationary, so $y$ is stationary, and a shift by $\tau$ changes neither the law nor the density. So take $\tau = 0$. By Lemma 1, with probability 1 no two inputs switch at the same instant. Then $y$ is constant between the transitions of the inputs, and at a transition time $t$ of $x_i$ only $x_i$ changes. So $y$ changes at $t$ exactly when $f$ takes different values at the two vectors that differ only in coordinate $i$, which is $\frac{\partial f}{\partial x_i}(x(t)) = 1$. The Boolean difference does not depend on $x_i$, so its value is $Z_i(t) = \frac{\partial f}{\partial x_i}(x_{-i}(t))$, a function of the other inputs only. Hence

$$ N_y((0, T]) \;=\; \sum_{i=1}^n \sum_{t \in N_{x_i} \cap (0, T]} Z_i(t). $$

$Z_i$ is a stationary signal that depends only on $x_{-i}$, so it is independent of $N_{x_i}$. Lemma 2 gives $E[N_y((0, T])] = T \sum_i D(x_i)\, P(Z_i = 1)$, and $P(Z_i = 1) = P(\frac{\partial f}{\partial x_i}(X) = 1)$ because the values of $x_1(t), \ldots, x_n(t)$ at one instant are independent with $P(x_i(t) = 1) = p_{x_i}$. Divide by $T$. $\square$

**Lemma 3 (gate rules).** For a gate $y = \mathrm{kind}(z_1, \ldots, z_k)$ with independent 0-1 inputs, $P(z_l = 1) = q_l$, the probability of $\partial y / \partial z_j$ is $\prod_{l \ne j} q_l$ for AND and NAND, $\prod_{l \ne j} (1 - q_l)$ for OR and NOR, and 1 for XOR, XNOR, BUF and NOT, which is line L6.

*Proof.* $\mathrm{AND}|_{z_j = 1} = \prod_{l \ne j} z_l$ and $\mathrm{AND}|_{z_j = 0} = 0$, so the difference is $\prod_{l \ne j} z_l$. For OR the cofactors are 1 and $\bigvee_{l \ne j} z_l$, whose XOR is $\prod_{l \ne j} \bar z_l$. For XOR the cofactors are complements of each other, so the difference is 1, and the same holds for BUF and NOT. Since $\bar f|_{x = 1} \oplus \bar f|_{x = 0} = f|_{x = 1} \oplus f|_{x = 0}$, the complemented gates have the same differences. The probabilities follow from the independence of the $z_l$. $\square$

**Theorem 2 (the pass is exact without reconvergence).** Suppose the primary inputs are independent stationary signals with finite densities, every gate output follows its function with a fixed delay, and for every gate the supports of its input pins are pairwise disjoint (this holds in every fanout-free circuit). Then TRANSITION-DENSITY returns $P[y] = P(y(t) = 1)$ and $D[y] = D(y)$ for every node $y$.

*Proof.* By induction in topological order we show that each node $y$ is a stationary signal that is a function of the primary input signals in its support $S(y)$ (with time shifts), and that $P[y]$ and $D[y]$ are exact. For a primary input this is line L1. For a gate $y = \mathrm{kind}(z_1, \ldots, z_k)$, the signals $z_j$ are functions of the disjoint groups $(x_i)_{i \in S(z_j)}$ of independent signals, so they are independent, and each is stationary with a finite density by the induction hypothesis. The node $y$ is $\mathrm{kind}(z_1, \ldots, z_k)$ with a fixed delay, so it is a function of the inputs in $S(y) = \bigcup_j S(z_j)$, and Theorem 1 applies with $z_1, \ldots, z_k$ as the inputs. With the values at one instant independent, line L3 gives $P(y = 1)$ (the numeric mode of signal probability propagation is exact for independent gate inputs), Lemma 3 shows that line L6 gives $P(\partial y / \partial z_j)$, and lines L4 to L7 then compute the sum of Theorem 1 with the exact $D(z_j)$. $\square$

**Reconvergence.** For $u = \mathrm{AND}(a, b)$, $v = \mathrm{AND}(a, c)$, $y = \mathrm{OR}(u, v)$ with all $p = 1/2$ and $D = 1$, Theorem 1 applied to $y = a(b \lor c)$ as one block gives $D(y) = \frac{3}{4} + \frac{1}{4} + \frac{1}{4} = \frac{5}{4}$, which is the true density. The pass gives $\frac{3}{4} D(u) + \frac{3}{4} D(v) = \frac{3}{2}$. The step that fails is the independence of $u$ and $v$ in Theorem 1 at the gate $y$: both depend on $a$, and they switch together at every transition of $a$ that both pass, so Lemma 1 fails for them as well.

**What is not proved.** For synchronous inputs that all switch at a clock edge, Lemma 1 fails, and the formula is not the zero-delay activity per cycle. For an AND gate with fresh uniform inputs every cycle the formula gives $1/2$ per cycle and the zero-delay output changes in $3/8$ of the cycles. The gap is the expected number of glitches that the formula assumes when the two input transitions are separated in time.
