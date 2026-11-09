---
title: Threshold accepting returns the best solution it saw, moves only along the edges of a threshold graph, and ends as a descent
proves: [correctness]
status: full
---

We use the pseudocode of the page. $S$ is a finite set, $f : S \to \mathbb{R}$, $R(i, \cdot)$ is a probability distribution on the neighbors $N(i)$ of $i$, and $\tau_1 \ge \tau_2 \ge \dots \ge \tau_J > 0$. We number the steps $t = 1, 2, \dots, JL$ in the order in which line L4 runs them, write $x_t$ for the value of $x$ after step $t$, $x_0$ for the start, and $\tau(t)$ for the threshold used at step $t$. For $\tau > 0$ let $G_\tau$ be the directed graph on $S$ with an edge $i \to j$ when $j \in N(i)$ and $f(j) - f(i) < \tau$.

**Claim 1 (the returned solution).** After step $t$, $best \in \{x_0, \dots, x_t\}$ and $f(best) = \min\{f(x_0), \dots, f(x_t)\}$.

*Proof.* By induction on $t$. Line L1 gives $best = x_0$, which is the claim for $t = 0$. Assume it after step $t - 1$. If line L5 rejects, $x_t = x_{t-1}$, so neither the minimum nor $best$ changes. If line L5 accepts, $x_t = y$, and line L7 sets $best = x_t$ exactly when $f(x_t) < f(best) = \min\{f(x_0), \dots, f(x_{t-1})\}$. In both branches $f(best) = \min(\min\{f(x_0), \dots, f(x_{t-1})\}, f(x_t))$ and $best$ is a visited solution. Line L8 returns $best$ after the last step. $\square$

**Claim 2 (each move is an edge of the threshold graph).** If $x_t \ne x_{t-1}$, then $x_{t-1} \to x_t$ is an edge of $G_{\tau(t)}$, and so an edge of $G_{\tau_1}$. Hence every $x_t$ is reachable from $x_0$ in $G_{\tau_1}$.

*Proof.* If $x_t \ne x_{t-1}$, line L5 accepted the proposal $y = x_t$ of line L4, so $x_t \in N(x_{t-1})$ and $f(x_t) - f(x_{t-1}) < \tau(t)$. That is an edge of $G_{\tau(t)}$. Since $\tau(t) \le \tau_1$, the condition $f(x_t) - f(x_{t-1}) < \tau(t)$ implies $f(x_t) - f(x_{t-1}) < \tau_1$, so the edge is also in $G_{\tau_1}$. By induction on $t$, $x_t$ is joined to $x_0$ by a directed path of such edges. $\square$

**Claim 3 (the end is a descent).** Let $\delta = \min\{f(j) - f(i) : i \in S, j \in N(i), f(j) > f(i)\}$, with $\delta = \infty$ if there is no such pair. If $\tau(t) \le \delta$, then $f(x_t) \le f(x_{t-1})$. Hence, from the first stage $j_0$ with $\tau_{j_0} \le \delta$, the values $f(x_t)$ do not increase.

*Proof.* If $x_t = x_{t-1}$ there is nothing to prove. Otherwise, by Claim 2, $x_t \in N(x_{t-1})$ and $f(x_t) - f(x_{t-1}) < \tau(t) \le \delta$. If $f(x_t) > f(x_{t-1})$, the pair $(x_{t-1}, x_t)$ would be a rise smaller than $\delta$, which contradicts the definition of $\delta$. So $f(x_t) \le f(x_{t-1})$. Since the thresholds do not increase, every later step also has $\tau(t) \le \delta$, which gives the second statement. $\square$

**Claim 4 (the trap condition).** Let $A \subseteq S$ contain $x_s$, and assume that every edge $i \to j$ with $i \in A$, $j \in N(i)$ and $j \notin A$ has $f(j) - f(i) \ge \tau(s+1)$. Then $x_t \in A$ for all $t \ge s$.

*Proof.* By induction on $t$. If $x_{t-1} \in A$ and $x_t \notin A$, then $x_t \in N(x_{t-1})$ and, by Claim 2, $f(x_t) - f(x_{t-1}) < \tau(t) \le \tau(s+1)$, which contradicts the assumption on the edges that leave $A$. $\square$

On the 8-state cycle of the page, with $f = (3, 1, 4, 2, 5, 0, 3, 6)$, the set $A = \{0, 1\}$ has the two leaving edges $0 \to 7$ and $1 \to 2$, with the rises 3 and 3. So by Claim 4, once the walk is in $A$ at a threshold of 3 or below, it stays in $A$. The test `test_trap_that_needs_a_larger_threshold` checks this, and that a threshold of 3.5 lets the walk leave $A$.

**What is not proved.** None of these claims says that the walk reaches a global minimum. Claim 2 shows that it cannot when no global minimum is reachable from $x_0$ in $G_{\tau_1}$, and Claim 4 shows that it cannot after it enters a set like $A$ at a low threshold. Whether it reaches a global minimum otherwise depends on the random proposals and on the number $L$ of steps at each threshold.
