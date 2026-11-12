---
title: The restart and retirement forms of the Gittins index, and the index theorem
proves: [correctness]
status: sketch
---

**Setting.** One arm is a Markov chain on the finite set $S$, with rewards $r(y)$, transitions $P(y, z)$ and discount $\gamma \in (0,1)$. For a state $x$ and a stopping time $\tau \ge 1$ of the chain $X_0 = x, X_1, \ldots$ (with $\tau = \infty$ allowed), let

$$A_\tau = \mathbb{E}_x\Big[\sum_{t=0}^{\tau-1}\gamma^t r(X_t)\Big], \qquad W_\tau = \mathbb{E}_x\Big[\sum_{t=0}^{\tau-1}\gamma^t\Big] = \frac{1 - \mathbb{E}_x[\gamma^\tau]}{1-\gamma},$$

with $\gamma^\infty = 0$. The index is $\nu(x) = \sup_{\tau\ge1} A_\tau/W_\tau$. The two parts below are full proofs. The part on the index theorem is a sketch.

## Part 1: the restart problem

In the restart problem for $x$, in each state $y$ the player either continues (gets $r(y)$, moves by $P(y,\cdot)$) or restarts (gets $r(x)$, moves by $P(x,\cdot)$), and maximizes the expected discounted reward. Its optimal value $V$ is the unique solution of the equation of the page, since the right side is a $\gamma$-contraction in the sup norm, and a stationary deterministic policy that attains the max in each state is optimal ([Bellman optimality](/bellman-optimality-equation/)).

**Claim 1.** $(1-\gamma)V(x) = \nu(x)$.

*Proof.* In state $x$ both actions are the same, so the process from $x$ can be cut into cycles: each cycle starts in $x$, pulls from $x$ in its first round, and ends at the first restart.

($\ge$) Fix a stopping time $\tau \ge 1$. Let the policy follow the chain until $\tau$, then restart, and do the same in each later cycle with a fresh copy of $\tau$. By the Markov property each cycle starts afresh in $x$. Let $C$ be the value of this policy. The first cycle gives $A_\tau$, and the rest is worth $C$, discounted by $\gamma^\tau$ and independent of $\gamma^\tau$ given the restart:

$$C = A_\tau + \mathbb{E}_x[\gamma^\tau]\,C, \qquad\text{so}\qquad C = \frac{A_\tau}{1 - \mathbb{E}_x[\gamma^\tau]} = \frac{A_\tau}{(1-\gamma)W_\tau}.$$

Rewards are bounded, so $C$ is finite and this is valid. Hence $V(x) \ge C$, so $(1-\gamma)V(x) \ge A_\tau/W_\tau$ for each $\tau$, and $(1-\gamma)V(x) \ge \nu(x)$.

($\le$) Take an optimal stationary policy, and let $R \subseteq S$ be the set of states where it restarts. The first cycle ends at $\tau^* = \min\{t \ge 1 : X_t \in R\}$, a stopping time with $\tau^* \ge 1$, and each cycle is the same. The renewal equation above gives $(1-\gamma)V(x) = A_{\tau^*}/W_{\tau^*} \le \nu(x)$. $\blacksquare$

**Consequence.** The supremum in the definition is attained by a hitting time of a set of states, and line L6 returns $\nu(x)$ up to the error of value iteration: if the last change of $V$ is $\delta$, the distance to the fixed point is at most $\gamma\delta/(1-\gamma)$.

## Part 2: the retirement problem

For $M \in \mathbb{R}$, in the retirement problem the player in each state may stop and receive $M$, or pull the arm. Its value from $x$ is $V_M(x) = \sup_{\tau \ge 0}\mathbb{E}_x[\sum_{t<\tau}\gamma^t r(X_t) + \gamma^\tau M]$, with the term $\gamma^\tau M$ equal to 0 when $\tau = \infty$.

**Claim 2.** Going on from $x$ is strictly better than retiring at once if and only if $(1-\gamma)M < \nu(x)$. So $\nu(x) = (1-\gamma)M^*(x)$, where $M^*(x) = \inf\{M : V_M(x) = M\}$.

*Proof.* Going on means using some $\tau \ge 1$, which gives $A_\tau + M\,\mathbb{E}_x[\gamma^\tau] = A_\tau + M - M(1-\gamma)W_\tau$. This is above $M$ exactly when $A_\tau > (1-\gamma)M\,W_\tau$, that is, when $A_\tau/W_\tau > (1-\gamma)M$, since $W_\tau \ge 1 > 0$. Some $\tau \ge 1$ does this if and only if $\nu(x) > (1-\gamma)M$, by the definition of the supremum and the fact that it is attained (Part 1). $\blacksquare$

The bisection of the implementation searches for $M^*(x)$ with the test "is going on better than $M$", which by Claim 2 is a monotone test in $M$.

## Part 3: the index theorem (sketch, after Weber 1992)

**Theorem.** With $K$ independent arms of this kind, the policy that pulls an arm with the largest current index maximizes $\mathbb{E}[\sum_t\gamma^t r_{A_t}(x_{A_t}(t))]$.

*Sketch.* Consider one arm alone, and a player who must pay a fixed charge $\lambda$ for each pull and may stop at any time. The **fair charge** of state $y$ is the largest $\lambda$ at which the player can just break even from $y$; by Claim 2 (with $(1-\gamma)M = \lambda$) it is $\nu(y)$. Now let the charge change over time: whenever the current fair charge falls below the charge in force, lower the charge to the fair charge. The charge in force at time $t$ is the **prevailing charge** $g(t) = \min_{s\le t}\nu(X_s)$, which is nonincreasing along the pulls of the arm.

- *Fact A.* For any rule that pulls the arm at some times and not at others, the expected discounted rewards minus the expected discounted prevailing charges paid is at most 0. Under the prevailing charge, each stretch of play from a time when the charge was reset is a fair game, which can at best break even.
- *Fact B.* The difference is exactly 0 if the arm is never left while its current index is above its prevailing charge. The index policy has this property: it leaves an arm only when the index of that arm falls below the largest index of the others, and at that moment the index of the arm equals its prevailing charge.

Now take any policy for all $K$ arms. By Fact A, applied to each arm, its expected reward is at most the expected discounted sum of the prevailing charges it pays. On each sample path, the prevailing charges of each arm form a nonincreasing sequence, fixed by the path of that arm and not by the policy. Interleaving $K$ nonincreasing sequences so as to maximize $\sum_t\gamma^t(\text{charge at time } t)$ is done by always taking the largest available charge, which is what the index policy does. By Fact B the index policy also has equality in Fact A. So its reward equals the largest possible sum of prevailing charges, which bounds the reward of any policy. The full argument, with the care needed for the independence of the arms and for the exchange of interleavings, is in Weber (1992) and in Lattimore and Szepesvari, Section 35.4. Whittle (1980) gives a different proof, with the retirement value of the whole system written as a product over the arms.
