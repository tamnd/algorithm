---
title: The great deluge algorithm returns the best solution it saw and makes a bounded number of moves
proves: [correctness]
status: full
---

We use the pseudocode of the page. $S$ is a finite set, $f : S \to \mathbb{R}$ with minimum $f^*$, $B_0$ is the start level and $\rho > 0$. We number the steps $t = 1, \dots, K$, and write $x_t$ and $B_t$ for the values of $x$ and $B$ after step $t$, with $x_0$ and $B_0$ the start values. Step $t$ uses the level $B_{t-1}$ in line L4.

**Claim 1 (the returned solution).** After step $t$, $best \in \{x_0, \dots, x_t\}$ and $f(best) = \min\{f(x_0), \dots, f(x_t)\}$.

*Proof.* By induction on $t$, as for simulated annealing. Line L1 gives the claim for $t = 0$. If line L4 rejects at step $t$, then $x_t = x_{t-1}$ and nothing changes. If it accepts, line L7 sets $best = x_t$ exactly when $f(x_t)$ is below the minimum so far. In both cases $f(best)$ is the new minimum and $best$ is a visited solution. $\square$

**Claim 2 (accepted values are below the level).** If step $t$ accepts, then $f(x_t) < B_{t-1}$. The levels satisfy $B_t = B_0 - \rho m_t$, where $m_t$ is the number of moves accepted in steps $1, \dots, t$. So $B_t$ does not increase, and every state accepted at a step $t' > t$ has $f < B_t$.

*Proof.* Line L4 accepts $y$ only when $f(y) < B_{t-1}$, and line L5 sets $x_t = y$. Line L6 is the only line that changes $B$, and it subtracts $\rho$ once per accepted move, which gives $B_t = B_0 - \rho m_t$. Since $m_t$ does not decrease, neither does $B$ increase, and a state accepted at step $t' > t$ has $f < B_{t'-1} \le B_t$. $\square$

**Claim 3 (the number of moves is bounded).** The total number $m$ of accepted moves satisfies $m \le \lceil (B_0 - f^*)/\rho \rceil$, for any $K$.

*Proof.* If $m = 0$ there is nothing to prove. Otherwise, consider the step $t$ of the $m$-th accepted move. Before it, $m - 1$ moves were accepted, so $B_{t-1} = B_0 - (m-1)\rho$ by Claim 2. The accepted state has $f^* \le f(x_t) < B_0 - (m - 1)\rho$, so $m - 1 < (B_0 - f^*)/\rho$. For a real number $r$, the integers $m$ with $m - 1 < r$ are exactly those with $m \le \lceil r \rceil$, since $m - 1 < r$ means $m < r + 1$, and the largest integer below $r + 1$ is $\lceil r \rceil$. $\square$

**Claim 4 (the current value is close to the level).** If at least one move was accepted in steps $1, \dots, t$, then $f(x_t) < B_t + \rho$.

*Proof.* Let $s \le t$ be the step of the last accepted move. Then $x_t = x_s$, and $B_t = B_s = B_{s-1} - \rho$, since no move was accepted after step $s$. By Claim 2, $f(x_s) < B_{s-1} = B_t + \rho$. $\square$

**Claim 5 (islands are traps).** Let $A \subseteq S$ with $x_s \in A$, and assume that $f(j) \ge B_s$ for every $j \notin A$ that is a neighbor of a state in $A$. Then $x_t \in A$ for all $t \ge s$.

*Proof.* By induction on $t$. If $x_{t-1} \in A$ and $x_t \notin A$, the move was accepted at step $t > s$, so $x_t \in N(x_{t-1})$ and $f(x_t) < B_{t-1} \le B_s$ by Claim 2. This contradicts the assumption on the neighbors of $A$. $\square$

On the 8-state cycle of the page, with $f = (3, 1, 4, 2, 5, 0, 3, 6)$, the set $A = \{0, 1\}$ has the outside neighbors 7 and 2, with $f = 6$ and $f = 4$. So by Claim 5, a walk that is in $A$ when the level is 4 or below never leaves $A$, and it never sees the global minimum 5. The test `test_level_set_trap` checks this, and `test_number_of_acceptances_is_bounded` checks Claims 3 and 4 on 120 runs.

**What is not proved.** No claim says that the returned solution is a global minimum, or a [local minimum](/local-optimum/). Claim 5 shows how the method can fail, and a run can also end because its budget $K$ ends before the level is low.
