---
title: Each best response lowers Rosenthal's potential by the mover's gain, so best-response dynamics stops at a pure Nash equilibrium
proves: [correctness]
status: full
---

Let a congestion game have players $1, \ldots, n$, resources $E$, costs $c_e(1), \ldots, c_e(n)$ for each $e \in E$, and finite strategy sets $S_i$ of subsets of $E$. For a profile $s$, $x_e(s)$ is the number of players $i$ with $e \in s_i$, player $i$ pays $c_i(s) = \sum_{e \in s_i} c_e(x_e(s))$, and

$$\Phi(s) = \sum_{e \in E} \sum_{j=1}^{x_e(s)} c_e(j).$$

**Lemma.** If $t = (s_i', s_{-i})$, then $\Phi(t) - \Phi(s) = c_i(t) - c_i(s)$.

Proof. Only the resources in exactly one of $s_i$ and $s_i'$ change load. For $e \in s_i' \setminus s_i$ the load goes from $x_e(s)$ to $x_e(s) + 1$, which adds the term $c_e(x_e(s) + 1) = c_e(x_e(t))$ to $\Phi$; this is what $i$ pays for $e$ in $t$. For $e \in s_i \setminus s_i'$ the load goes from $x_e(s)$ to $x_e(s) - 1$, which removes the term $c_e(x_e(s))$; this is what $i$ paid for $e$ in $s$. For $e \in s_i \cap s_i'$ the load and the price to $i$ do not change. Summing over $e$ gives the claim. $\square$

**The dynamics stops.** Line L3 picks, for the current player $i$, a strategy $b$ that minimizes $c_i(b, s_{-i})$, and line L4 moves to $t = (b, s_{-i})$ only when the gain $g = c_i(s) - c_i(t)$ is positive. By the lemma $\Phi$ falls by exactly $g$, which is what the code records and the tests check. So $\Phi$ strictly falls at each move. The set of profiles is finite, so no profile repeats and the number of moves is less than the number of profiles. With integer costs each move lowers $\Phi$ by at least 1, so the number of moves is also at most $\Phi(s^0) - \min_s \Phi(s) \le \Phi(s^0)$ when costs are nonnegative.

**It stops at an equilibrium.** Line L1 ends after a full round of line L2 in which no player moved. In that round, for each player $i$, the best response $b$ of line L3 had $c_i(b, s_{-i}) \ge c_i(s)$, and since $b$ minimizes over all of $S_i$, no strategy of $i$ costs less than $c_i(s)$. The profile did not change during the round, so this holds for every player at the same profile, which is the definition of a pure Nash equilibrium. $\blacksquare$

**Equilibria are local minima of $\Phi$.** By the lemma, a unilateral deviation lowers the deviator's cost if and only if it lowers $\Phi$. So $s$ is a pure Nash equilibrium if and only if no unilateral deviation lowers $\Phi$. The tests check this set equality by brute force.

**Potential and social cost.** Let $C(s) = \sum_i c_i(s) = \sum_e x_e c_e(x_e)$. If each $c_e$ is nonnegative and nondecreasing, then $\sum_{j \le x} c_e(j) \le x\, c_e(x)$ and $x\, c_e(x) \le x \sum_{j \le x} c_e(j)$, so $\Phi(s) \le C(s) \le (\max_e x_e)\, \Phi(s)$. If $c_e(x) = a_e x + b_e$ with $a_e, b_e \ge 0$, then $\sum_{j \le x} c_e(j) = a_e x (x + 1)/2 + b_e x \ge (a_e x^2 + b_e x)/2$, so $C(s) \le 2 \Phi(s)$.
