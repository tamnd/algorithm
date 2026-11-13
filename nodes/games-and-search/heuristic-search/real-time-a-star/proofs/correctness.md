---
title: RTA* reaches the goal in a finite graph in which the goal can be reached from every state
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The graph is finite and directed, every arc cost is positive and finite, the goal $g$ can be reached from every state, and the heuristic $h_0$ is finite. It need not be admissible. Let $c_{min} > 0$ be the least arc cost.

Write $x_t$ for the state of the agent after $t$ moves, and $V_t(y)$ for the value that line L4 uses for $y$ at that time: the stored value $H(y)$ if there is one, and $h_0(y)$ if not. Line L4 sets $f(y) = c(x_t, y) + V_t(y)$ for each successor $y$ of $x_t$.

**Fact 1 (values are finite).** Every value $V_t(y)$ is finite.

*Proof.* $h_0$ is finite, and lines L6 and L7 store one of the values $f(y)$, which is a finite cost plus a finite value. $\square$

**Fact 2 (the update rule).** At each move, $V_{t+1}(x_t) \ge c(x_t, x_{t+1}) + V_t(x_{t+1})$, and $V_{t+1}(y) = V_t(y)$ for every $y \ne x_t$.

*Proof.* Line L5 picks $x_{t+1}$ with the least $f$, and lines L6 and L7 store the second least $f$ or the least $f$, which is at least $f(x_{t+1}) = c(x_t, x_{t+1}) + V_t(x_{t+1})$. Only $H(x_t)$ changes. $\square$

**Theorem 3 (termination and correctness).** The loop of line L3 stops after finitely many moves, and the walk that line L9 returns starts at the start state, follows arcs of the graph, and ends at $g$.

*Proof.* The walk starts at the start state (line L2), each move goes to a successor (line L8), and the loop stops only at $g$. So we must show that it stops.

Assume that it does not. The graph is finite, so the set $S$ of states that the agent visits infinitely often is not empty, and there is a time $T_0$ after which the agent visits only states of $S$. The goal is not in $S$, because the loop stops there. States outside $S$ are not visited after $T_0$, so their values do not change after $T_0$.

Let $m_t = \min_{x \in S} V_t(x)$ for $t \ge T_0$. By Fact 2, a move at time $t \ge T_0$ changes only $V(x_t)$, and the new value is at least $c_{min} + V_t(x_{t+1}) \ge c_{min} + m_t$, because $x_{t+1} \in S$. So $m_{t+1} \ge m_t$. Take any $t \ge T_0$ and a later time $t'$ such that every state of $S$ is left at least once between $t$ and $t'$. Every value in $S$ was then set after time $t$, to at least $c_{min} + m_t$, so $m_{t'} \ge m_t + c_{min}$. Each state of $S$ is left infinitely often, so such times exist again and again, and $m_t \to \infty$.

The goal can be reached from a state of $S$, so some arc $z \to y$ has $z \in S$ and $y \notin S$. The value $V(y)$ is fixed after $T_0$ and finite by Fact 1. Choose a time $t \ge T_0$ with $m_t \ge c(z, y) + V(y)$ and $x_t = z$, which exists because $z$ is visited infinitely often. At that time, each successor $w \in S$ of $z$ has
$$ f(w) = c(z, w) + V_t(w) \ge c_{min} + m_t > c(z, y) + V(y) = f(y) , $$
so line L5 picks a successor with $f \le f(y)$, and that successor is not in $S$. This is a move out of $S$ after $T_0$, which is false. $\square$

**Remark (the stored values are not lower bounds).** Line L6 stores the second least $f$, not the least. So a stored value can be larger than the distance to the goal even when $h_0$ is admissible. The example of the page shows this: the cell $(2, 1)$ stores 7, and its distance to the goal is 5. Theorem 3 does not need lower bounds, but the values cannot be kept for a second trial as lower bounds, which is why LRTA* stores the least $f$.
