---
title: Identifiability of the dueling aggregation
proves: [correctness]
status: full
---

Fix one state and drop $s$ from the notation. There are $M \ge 1$ actions. The heads output a number $V$ and a vector $A \in \mathbb{R}^M$, and lines L4 and L5 output $Q \in \mathbb{R}^M$. We prove the four facts on the page. "Identifiable" means: the output $Q$ fixes $V$, and it fixes $A$ up to an added constant vector $c \mathbf{1}$, which does not change $Q$.

**Claim 1 (mean aggregation).** Let $Q(a) = V + A(a) - \bar A$ with $\bar A = \frac{1}{M} \sum_b A(b)$. Then $V = \bar Q := \frac{1}{M} \sum_a Q(a)$ and $A = Q - \bar Q \mathbf{1} + \bar A \mathbf{1}$. Conversely, $A + c\mathbf{1}$ with the same $V$ gives the same $Q$ for every $c$.

*Proof.* Average the equation over $a$: $\bar Q = V + \bar A - \bar A = V$. Substitute back: $A(a) = Q(a) - V + \bar A = Q(a) - \bar Q + \bar A$. So $V$ is fixed by $Q$, and $A$ is fixed by $Q$ up to the constant $\bar A$. For the converse, replacing $A$ by $A + c\mathbf{1}$ adds $c$ to each $A(a)$ and $c$ to $\bar A$, so each $Q(a)$ is unchanged. $\square$

**Claim 2 (max aggregation).** Let $Q(a) = V + A(a) - \max_b A(b)$. Then $V = \max_a Q(a)$ and $A = Q - V\mathbf{1} + (\max_b A(b)) \mathbf{1}$. Conversely, $A + c \mathbf{1}$ gives the same $Q$.

*Proof.* For every $a$, $A(a) - \max_b A(b) \le 0$, with equality at a maximizer $a^*$ of $A$. Hence $Q(a) \le V$ for all $a$ and $Q(a^*) = V$, so $V = \max_a Q(a)$. Substitute back as in Claim 1. Adding $c$ to every entry of $A$ adds $c$ to $\max_b A(b)$ too, so $Q$ is unchanged. $\square$

**Claim 3 (naive sum).** Let $Q(a) = V + A(a)$. For every $Q$ and every number $V$, the vector $A = Q - V\mathbf{1}$ gives the output $Q$. So $V$ is not fixed by $Q$.

*Proof.* Substitute: $V + (Q(a) - V) = Q(a)$. $\square$

**Claim 4 (same class).** For each of the three aggregations, every $Q \in \mathbb{R}^M$ is the output of some $(V, A)$. If the heads are linear in shared features $z \in \mathbb{R}^H$, that is $V = \beta^\top z + \beta_0$ and $A(a) = \alpha_a^\top z + \alpha_{a,0}$, then the set of functions $z \mapsto Q$ that the dueling heads compute is the set of affine maps $z \mapsto W z + b$ with $W \in \mathbb{R}^{M \times H}$, $b \in \mathbb{R}^M$, the same set as a plain linear output layer, for the mean and the sum.

*Proof.* For the first part, take $V = \bar Q$ and $A = Q - \bar Q\mathbf{1}$ for the mean; $V = \max Q$ and $A = Q - V\mathbf{1}$ for the max; any $V$ and $A = Q - V\mathbf{1}$ for the sum. Claims 1 to 3 show these give $Q$.

For the second part, with the mean, $Q = V\mathbf{1} + (I - \frac{1}{M}\mathbf{1}\mathbf{1}^\top) A$, which is affine in $z$ because $V$ and $A$ are. Conversely, given $W$ and $b$, set $\beta$ to the mean of the rows of $W$, $\beta_0$ to the mean of $b$, and $\alpha_a = W_a$, $\alpha_{a,0} = b_a$. Then $\bar A = \beta^\top z + \beta_0 = V$, so $Q(a) = V + A(a) - \bar A = W_a z + b_a$. The sum is the same with $\beta = 0$, $\beta_0 = 0$. With the max, $Q$ is piecewise affine in $z$, since the maximizer of $A$ changes with $z$, so the dueling heads compute a different set; they still reach every value of $Q$ at a single $z$, by the first part. $\square$

**What this does and does not show.** Claims 1 and 2 show that the split computed by the network is unique given its output, so the value head has a fixed meaning: the mean of the Q-values, or their maximum. They do not show that training converges, or that it is faster than with a plain head. The paper's evidence for speed is experimental. The implementation tests Claims 1 to 3 with exact rational arithmetic, and tests the hand-written gradient through line L5 against finite differences for both aggregations. $\blacksquare$
