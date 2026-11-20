---
title: Why the product of flux and crossing probabilities gives the rate
proves: [correctness]
status: full
---

We prove two things for a Markov chain $(X_t)$ with an order parameter $\lambda$, a state $A$ with $\lambda < \lambda_0$ on $A$, interfaces $\lambda_0 < \lambda_1 < \cdots < \lambda_n$, and the state $B = \{\lambda \ge \lambda_n\}$. First, the rate is the flux times the probability to reach $B$ from the first crossing of $\lambda_0$. Second, the staged estimator of that probability is unbiased.

**Definitions.** A trajectory is in the *region of A* at time $t$ if it visited $A$ more recently than $B$. A *first crossing* of $\lambda_0$ is a time at which the trajectory, in the region of $A$, reaches $\lambda \ge \lambda_0$ for the first time since its last visit to $A$. For a point $y$, let $u_i(y)$ be the probability that the chain from $y$ reaches $\lambda \ge \lambda_n$ before it enters $A$, and let $\tau_{i+1}(y)$ be the first time at which it reaches $\lambda \ge \lambda_{i+1}$ or enters $A$. The rate $k_{AB}$ is the long run number of transitions from the region of $A$ to $B$ per unit of time spent in the region of $A$.

**Lemma 1 (the rate).** Let $y_1, y_2, \ldots$ be the points of the successive first crossings of $\lambda_0$ in a long stationary run, and $T_A(t)$ the time spent in the region of $A$ up to $t$. If the chain is ergodic, then
$$k_{AB} = \lim_{t \to \infty} \frac{1}{T_A(t)} \sum_{j : \text{crossing } j \text{ before } t} u(y_j),$$
where $u = u_0$. Writing $\Phi_{A,0}$ for the limit of the number of crossings over $T_A(t)$, and $P(\lambda_n | \lambda_0)$ for the average of $u$ over the crossing points, $k_{AB} = \Phi_{A,0} P(\lambda_n | \lambda_0)$.

*Proof.* Every transition to $B$ starts in the region of $A$ and must reach $\lambda \ge \lambda_0$ on the way, because $\lambda < \lambda_0$ on $A$ and $\lambda \ge \lambda_n > \lambda_0$ on $B$. So each transition belongs to exactly one first crossing, the last one before it, and the excursion after crossing $j$ ends in $B$ (a transition) or in $A$ (no transition). The indicator $I_j$ that excursion $j$ ends in $B$ has the conditional mean $u(y_j)$ given the past up to crossing $j$, by the strong Markov property. So $\sum_j (I_j - u(y_j))$ is a martingale with bounded increments, and divided by the number of crossings it tends to 0. Dividing by $T_A(t)$ instead changes nothing, because the number of crossings grows like $T_A(t)$. The number of transitions is $\sum_j I_j$, which proves the first formula; the second is a rewriting. $\square$

**Lemma 2 (the stages).** Fix the set $S_0$ of first crossing points. In stage $i$, the estimator draws $M$ points $y$ uniformly with replacement from $S_i$, runs each until $\tau_{i+1}(y)$, and collects the end points that have $\lambda \ge \lambda_{i+1}$ into $S_{i+1}$; $\hat P_i = |S_{i+1}| / M$. Then
$$E\left[\hat P_0 \hat P_1 \cdots \hat P_{n-1} \,\middle|\, S_0\right] = \frac{1}{|S_0|} \sum_{y \in S_0} u(y).$$

*Proof.* Let $u_i(y)$ be the probability to reach $\lambda \ge \lambda_n$ before $A$ from $y$, as above; it does not depend on $i$, but we use it at stage $i$. We show by downward induction on $i$ that $E[\hat P_i \cdots \hat P_{n-1} | S_i] = \frac{1}{|S_i|} \sum_{y \in S_i} u(y)$ for nonempty $S_i$. For $i = n$ the product is empty, equal to 1, and $u = 1$ on $S_n$ because its points have $\lambda \ge \lambda_n$. For the step, condition on $S_{i+1}$ and use the induction hypothesis (if $S_{i+1}$ is empty, the product is 0, and so is the sum below):
$$E[\hat P_i \cdots \hat P_{n-1} | S_i] = E\left[\frac{|S_{i+1}|}{M} \cdot \frac{1}{|S_{i+1}|} \sum_{z \in S_{i+1}} u(z) \,\middle|\, S_i\right] = \frac{1}{M} E\left[\sum_{z \in S_{i+1}} u(z) \,\middle|\, S_i\right].$$
Each of the $M$ trials picks $y$ uniformly in $S_i$ and adds $u(X_{\tau_{i+1}})$ if the run reaches $\lambda_{i+1}$ first. By the strong Markov property at $\tau_{i+1}$, the expectation of this term given $y$ is the probability to reach $\lambda_n$ before $A$ from $y$, which is $u(y)$, because a run that reaches $\lambda_n$ must first reach $\lambda_{i+1}$. So the right side is $\frac{1}{|S_i|} \sum_{y \in S_i} u(y)$. $\square$

**Theorem.** The estimate $\hat k = \hat \Phi_{A,0} \prod_i \hat P_i$ of the implementation, with $\hat \Phi_{A,0}$ the number of first crossings over the time in the region of $A$ in the first run, satisfies $E[\hat k | \text{first run}] = \frac{1}{T_A} \sum_j u(y_j)$, and this tends to $k_{AB}$ as the first run grows. So $\hat k$ is unbiased given the first run, and consistent.

*Proof.* $\hat \Phi_{A,0} = |S_0| / T_A$ is fixed by the first run. Lemma 2 gives $E[\hat k | \text{first run}] = \frac{|S_0|}{T_A} \cdot \frac{1}{|S_0|} \sum_{y \in S_0} u(y)$, and Lemma 1 gives the limit. $\blacksquare$

**For the nearest neighbour walk of the tests.** With $A = \{0\}$, $B = \{L\}$ and the interfaces $1, 2, \ldots, L$, every point on interface $i$ is the state $i$, so $\hat P_i$ is a binomial proportion with the mean $P(i+1 | i) = q(i) / q(i+1)$, where $q$ is the committor ($q(0) = 0$, $q(L) = 1$). The product telescopes to $q(1)$. The flux is the rate of steps from 0 to 1 per unit of time in the region of $A$, $\pi(0) p(0, 1) / \sum_x \pi(x) (1 - q(x))$, because for a reversible chain the probability that $x$ is in the region of $A$ is $1 - q(x)$. Together, $k_{AB} = \pi(0) p(0, 1) q(1) / \sum_x \pi(x) (1 - q(x))$, the exact value of the tests.

**What is not proved.** The theorem gives no variance. The variance of $\hat k$ depends on the placement of the interfaces and on $M$; on the page it is measured.
