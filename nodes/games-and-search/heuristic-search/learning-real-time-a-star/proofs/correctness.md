---
title: LRTA* keeps lower bounds, reaches the goal in each trial, and its repeated trials end with an optimal trial
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The graph is finite and directed, every arc cost is positive and finite, and the goal $g$ can be reached from every state. Let $h^*(x)$ be the distance from $x$ to $g$, and let $c_{min} > 0$ be the least arc cost. The heuristic $h_0$ is admissible, $0 \le h_0(x) \le h^*(x)$, so $h_0(g) = 0$.

Write $H(x)$ for the value of $x$: the stored value if there is one, else $h_0(x)$. Line L5 sets $H(x) \leftarrow \min_y (c(x, y) + H(y))$, and line L6 moves to a successor $y$ that gives this least value. So after the move, $H(x) = c(x, y) + H(y)$ exactly. The goal is never updated, because the loop of line L2 stops there, so $H(g) = 0$ at all times. Let $P = \sum_x H(x)$, the sum over all states, and $\Phi_0 = \sum_x (h^*(x) - h_0(x))$.

**Lemma 1 (lower bounds).** At all times, $0 \le H(x) \le h^*(x)$ for every state $x$.

*Proof.* This holds at the start. Assume that it holds before an update of $x \ne g$, and let $y^*$ be the next state on a shortest path from $x$. The new value is at most $c(x, y^*) + H(y^*) \le c(x, y^*) + h^*(y^*) = h^*(x)$, and it is at least $0$ because all costs and values are at least $0$. $\square$

**Lemma 2 (cost identity).** Let a trial start with the table $H_0$ and the sum $P_0$, and let it make $t$ moves along $x_0, \dots, x_t$, after which the table is $H_t$ and the sum is $P_t$. Then
$$ \sum_{j < t} c(x_j, x_{j+1}) = H_0(x_0) - H_t(x_t) + P_t - P_0 . $$

*Proof.* Let $H_j$ be the table after $j$ moves. Move $j$ changes only the value of $x_j$, to $H_{j+1}(x_j) = c(x_j, x_{j+1}) + H_j(x_{j+1})$. Also $H_{j+1}(x_{j+1}) = H_j(x_{j+1})$, because $x_{j+1} \ne x_j$. So
$$ c(x_j, x_{j+1}) = H_{j+1}(x_j) - H_j(x_j) + H_j(x_j) - H_{j+1}(x_{j+1}) = (P_{j+1} - P_j) + H_j(x_j) - H_{j+1}(x_{j+1}) . $$
The sum over $j < t$ telescopes to the claim. $\square$

**Theorem 3 (each trial reaches the goal).** Each call of TRIAL stops after finitely many moves, and it returns a walk from the start to $g$ along arcs of the graph. If the trial starts with the table $H_0$, its cost is at most $H_0(s) + \sum_x (h^*(x) - H_0(x))$. For the first trial, $H_0 = h_0$, and the bound is $h_0(s) + \Phi_0$.

*Proof.* The walk starts at $s$ (line L1), each move goes to a successor (line L6), and the loop stops only at $g$. After $t$ moves, Lemma 2 and Lemma 1 give that the cost so far is at most $H_0(s) + P_t - P_0 \le H_0(s) + \sum_x (h^*(x) - H_0(x))$, because $H_t(x_t) \ge 0$ and $P_t \le \sum_x h^*(x)$. Each move costs at least $c_{min}$, so the number of moves is bounded and the trial stops, at $g$. The bound on the cost is the same inequality for the full trial. $\square$

**Corollary 4 (total excess).** Let trials $1, 2, \dots$ start from the same state $s$, with costs $C_1, C_2, \dots$. Then $\sum_k (C_k - h^*(s)) \le \Phi_0$, and each term is at least $0$.

*Proof.* Let $H_k$ and $P_k$ be the table and the sum at the start of trial $k$. Lemma 2 for the full trial, with $H(g) = 0$, gives $C_k = H_k(s) + P_{k+1} - P_k$. So $C_k - h^*(s) \le C_k - H_k(s) = P_{k+1} - P_k$ by Lemma 1. Summing over $k$ gives at most $P_{last} - P_1 \le \sum_x h^*(x) - \sum_x h_0(x) = \Phi_0$. Each walk from $s$ to $g$ costs at least $h^*(s)$. $\square$

So when costs and $h_0$ are integers, at most $\Phi_0$ trials are not optimal.

**Lemma 5 (finitely many tables).** Over all trials, the table takes finitely many values.

*Proof.* By induction on the updates, each value $H(x)$ is $h_0(z)$ plus the cost of some walk from $x$ to some state $z$: this holds for $h_0(x)$ with the empty walk, and an update stores $c(x, y) + H(y)$, which adds the arc $x \to y$ in front of the walk of $y$. By Lemma 1 and $h_0 \ge 0$, the walk costs at most $h^*(x)$, so it has at most $h^*(x) / c_{min}$ arcs. A finite graph has finitely many such walks, so each state has finitely many possible values, and there are finitely many tables. $\square$

**Theorem 6 (the repeated trials end with an optimal trial).** TRIALS stops: some trial changes no value. That trial is optimal, and the values on its walk are the true distances.

*Proof.* The sums $P_k$ do not go down (Corollary 4 gives $P_{k+1} - P_k \ge C_k - h^*(s) \ge 0$), and they take finitely many values (Lemma 5). So there is a $K$ with $P_{k+1} = P_k$ for all $k \ge K$. For such $k$, $C_k = H_k(s) \le h^*(s) \le C_k$, so trial $k$ costs $h^*(s)$ and $H_k(s) = h^*(s)$. A walk of cost $h^*(s)$ with positive costs is a shortest path, so it visits no state twice, and $h^*(x_j) = c(x_j, x_{j+1}) + h^*(x_{j+1})$ along it.

Let $\delta(x) = h^*(x) - H(x) \ge 0$ be the deficit of $x$. In trial $k \ge K$, the walk $x_0, \dots, x_t$ visits each state once, so when the agent leaves $x_j$, the value of $x_{j+1}$ is still its value at the start of the trial. The new deficit of $x_j$ is
$$ h^*(x_j) - c(x_j, x_{j+1}) - H_k(x_{j+1}) = \delta_k(x_{j+1}) . $$
So the trial moves each deficit on the walk one step back toward $s$, and the deficit of $x_0 = s$, which is $0$, goes away. Let $W = \sum_x \delta(x)\, h^*(x)$. Trial $k$ changes $W$ by
$$ \sum_{j < t} \delta_k(x_{j+1}) \bigl(h^*(x_j) - h^*(x_{j+1})\bigr) - \delta_k(x_0)\, h^*(x_0) = \sum_{j < t} \delta_k(x_{j+1})\, c(x_j, x_{j+1}) \ge 0 . $$
If the trial changes a value, then some new deficit $\delta_k(x_{j+1})$ differs from the old $\delta_k(x_j)$, so not all deficits on the walk are $0$, and since $\delta_k(x_0) = 0$, some $\delta_k(x_{j+1})$ with $j < t$ is positive. Then $W$ goes up strictly. By Lemma 5, $W$ takes finitely many values, so it cannot go up strictly in every trial after $K$. So some trial changes no value, and line L10 stops the loop.

A trial that changes no value has $P_{k+1} = P_k$, so it costs $H_k(s) \le h^*(s)$ and is optimal. In it, all deficits on the walk are $0$, as shown above, so the values on the walk are the true distances. The next trial would start from the same table and repeat this walk. $\square$

**Lemma 7 (consistent heuristics).** If $h_0$ is consistent, $h_0(u) \le c(u, v) + h_0(v)$ for every arc, then the table stays consistent and no value goes down.

*Proof.* Assume that $H$ is consistent before the update of $x$. The new value $H'(x) = \min_y (c(x, y) + H(y))$ is at least $H(x)$ by consistency at $x$. For an arc $u \to x$, $H(u) \le c(u, x) + H(x) \le c(u, x) + H'(x)$. For an arc $x \to v$, $H'(x) \le c(x, v) + H(v)$ by the minimum. Other arcs do not change. $\square$

With a consistent $h_0$, each trial that changes a value raises $P$ strictly, so with integer costs and $h_0$ there are at most $\Phi_0 + 1$ trials. With an inconsistent $h_0$, values can go down, which is why Theorem 6 needs the potential $W$.

The four statements that the tests check are Lemma 1 (values at most the distances, after every move), Lemma 7 (values do not go down for a consistent $h_0$), Corollary 4 (the total excess) and Theorem 6 (the last trial costs $h^*(s)$).
