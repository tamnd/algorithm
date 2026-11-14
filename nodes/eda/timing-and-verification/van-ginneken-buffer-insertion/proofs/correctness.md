---
title: Van Ginneken's algorithm returns the largest slack over all buffer placements, in O(n^2) time for one buffer type
proves: [correctness, list size bound, complexity]
status: full
---

We use the model of the page. The tree has the source $0$ and nodes $1, \ldots, n - 1$. The wire into node $v$ has resistance $R_v \ge 0$ and capacitance $W_v \ge 0$, in the pi model: half of $W_v$ at each end. A sink $s$ is a leaf with load $c_s \ge 0$ and required time $q_s$. A buffer of type $b$ has input capacitance $C_b \ge 0$, resistance $R_b \ge 0$ and intrinsic delay $D_b$. The driver at the source has resistance $R_d \ge 0$ and intrinsic delay $D_d$. A placement $P$ maps some candidate nodes to buffer types. A buffer at $v$ drives the subtree of $v$, and its input is a load at $v$ for the stage above. The arrival time of each node is given by the [Elmore delay](/elmore-delay/) of its stage, and the slack of $P$ is $\min_s (q_s - a_s)$.

**Elmore delay in a stage.** Let a stage have driver resistance $R_0$ at its root $d$, and let $K_d$ be the whole capacitance of the stage. For a wire $e$ of the stage, let $B_e$ be the capacitance of the stage strictly below $e$. The resistor of $e$ sees the half $W_e / 2$ at its lower end and $B_e$ below it, so by the downstream form of the Elmore delay the delay from the driver to a node $u$ of the stage is
$$ R_0 K_d + \sum_{e \text{ on the path from } d \text{ to } u} R_e \Big( \frac{W_e}{2} + B_e \Big). $$

**The pair of a partial solution.** Fix a node $v$ and a placement $P_v$ of the candidate nodes in the subtree $T_v$ of $v$. Cut the tree at $v$ and look into $T_v$ from $v$, without the wire above $v$.

- The *load* $C(P_v)$ is the capacitance that the stage containing the point $v$ sees in $T_v$: $C_b$ if $P_v$ puts a buffer of type $b$ at $v$, else the total capacitance of the stage below $v$ (wire capacitances, sink loads and buffer input capacitances, down to the first buffers).
- The *required time* $q(P_v) = \min_{s \in T_v} (q_s - \delta_s)$, where $\delta_s$ is the arrival time at $s$ minus the arrival time at $v$.

**Lemma 1 ($\delta_s$ depends only on $P_v$).** For each sink $s$ of $T_v$, $\delta_s$ is a function of $P_v$ and of the data inside $T_v$.

*Proof.* If $P_v$ has no buffer at $v$, $v$ lies inside a stage with root $d$ above it. By the formula above, the arrival time at $s$ (if $s$ is in the same stage) minus that at $v$ is $\sum R_e (W_e/2 + B_e)$ over the wires $e$ from $v$ to $s$, and each $B_e$ is a capacitance inside $T_v$. If $s$ lies in a later stage, the path from $v$ to $s$ passes through buffers of $P_v$ in $T_v$, and each stage on the way is inside $T_v$, so its delay is also fixed by $P_v$. If $P_v$ has a buffer at $v$, the same holds with the stage of that buffer, plus its intrinsic delay $D_b$. $\square$

**Lemma 2 (the outside sees only the pair).** Fix a placement $Q$ outside $T_v$. Then the slack of $P_v \cup Q$ is $\min(\phi_Q(C(P_v)),\; q(P_v) - \alpha_Q - \beta_Q C(P_v))$, where $\phi_Q$ is a nonincreasing function and $\alpha_Q$ and $\beta_Q \ge 0$ are numbers, all fixed by $Q$. So the slack is nondecreasing in $q(P_v)$ and nonincreasing in $C(P_v)$.

*Proof.* Let $d$ be the root of the stage that contains the wire above $v$ (or the point $v$). The subtree $T_v$ changes the outside only through the capacitance it adds at $v$, which is $C(P_v)$. In the Elmore formula of that stage, the term $C(P_v)$ appears in $K_d$ and in $B_e$ for each wire $e$ on the path from $d$ to $v$. So the arrival time of each stage node $u$ outside $T_v$ is $a_u^0 + \beta_u C(P_v)$, where $\beta_u \ge 0$ is $R_0$ plus the resistance of the common part of the paths from $d$ to $u$ and to $v$. Stages that are not below $d$ do not depend on $C(P_v)$, and a stage that hangs below a node $u$ of the stage of $d$ shifts by $\beta_u C(P_v)$ as a whole. So every outside sink $s$ has slack $q_s - a_s^0 - \beta_s C(P_v)$ with $\beta_s \ge 0$, and its minimum is a function $\phi(C(P_v))$ that is nonincreasing. The arrival time at $v$ is $\alpha_Q + \beta_Q C(P_v)$ with $\beta_Q = \beta_v$, and by Lemma 1 the sinks of $T_v$ give the term $q(P_v) - \alpha_Q - \beta_Q C(P_v)$. $\square$

**Definition.** A pair $(c, q)$ *dominates* $(c', q')$ when $c \le c'$ and $q \ge q'$. By Lemma 2, if the pair of $P_v$ dominates the pair of $P'_v$, then for every outside $Q$ the slack of $P_v \cup Q$ is at least that of $P'_v \cup Q$.

**Lemma 3 (the three steps).** Let $P_v$ have pair $(c, q)$.

1. Wire. Seen from the top end $u$ of the wire into $v$, the branch has load $c + W_v$ and required time $q - R_v (W_v / 2 + c)$.
2. Buffer. If $P_v$ has no buffer at $v$, adding a buffer of type $b$ at $v$ gives the pair $(C_b, q - D_b - R_b c)$.
3. Join. If the branches of two children of $v$, seen from $v$, have pairs $(c_1, q_1)$ and $(c_2, q_2)$, the union has the pair $(c_1 + c_2, \min(q_1, q_2))$.

*Proof.* 1: the stage that contains the wire sees the wire capacitance and all of $c$ below the top end. The arrival time at $v$ minus that at $u$ is $R_v (W_v / 2 + B)$ with $B = c$, the capacitance strictly below the wire. So every $\delta_s$ grows by $R_v (W_v/2 + c)$. 2: the buffer input is a load $C_b$ at $v$. The buffer adds $D_b + R_b c$ between its input and the point $v$ of its own stage, since its stage has capacitance $c$. 3: loads in parallel add, and $q$ is a minimum over the sinks of both branches. $\square$

**Lemma 4 (pruning).** The procedure PRUNE, on a list sorted by load, returns a list with strictly increasing loads and strictly increasing required times, in which every input pair is dominated by an output pair.

*Proof.* An input pair is skipped only when its $q$ is at most that of the last kept pair, whose load is no larger, so it is dominated. A kept pair with the same load as the last kept one replaces it and has a larger $q$, so it dominates it. By induction the kept list has strictly increasing loads, and each kept pair has a larger $q$ than the one before it. $\square$

**Lemma 5 (the join keeps a dominating pair).** Let $A$ and $B$ be lists with strictly increasing loads and required times. For every $i$ and $j$, the two pointer join outputs a pair that dominates $(A_i.c + B_j.c, \min(A_i.q, B_j.q))$.

*Proof.* Let $m = \min(A_i.q, B_j.q)$. Let $i_0$ be the first index with $A_{i_0}.q \ge m$ and $j_0$ the first with $B_{j_0}.q \ge m$. Then $i_0 \le i$ and $j_0 \le j$, so $A_{i_0}.c + B_{j_0}.c \le A_i.c + B_j.c$. We show that the pointers $(x, y)$ reach a pair with $x \le i_0$, $y \le j_0$ and $\min(A_x.q, B_y.q) \ge m$. At the start $(x, y) = (0, 0)$. Suppose $x \le i_0$, $y \le j_0$ and $\min(A_x.q, B_y.q) < m$. If $A_x.q < B_y.q$, then $A_x.q < m$, so $x < i_0$, and the step moves to $(x + 1, y)$, which stays in the bounds. The case $B_y.q < A_x.q$ is the mirror. If $A_x.q = B_y.q < m$, then $x < i_0$ and $y < j_0$, and the step moves both. Each step increases $x + y$ by at least 1 and stays inside the lists, so after at most $i_0 + j_0$ steps the pointers hold a pair whose minimum is at least $m$ and whose load is at most $A_{i_0}.c + B_{j_0}.c$. That pair is output, and PRUNE keeps a pair that dominates it by Lemma 4. $\square$

**Theorem 1 (correctness).** For every node $v$, every pair in the list $L(v)$ is the pair of some placement of $T_v$, stored in its record, and for every placement $P_v$ of $T_v$ some pair in $L(v)$ dominates the pair of $P_v$. So the value returned is the largest slack over all placements, and the returned placement reaches it.

*Proof.* By induction from the leaves up. A sink has only the empty placement, with pair $(c_s, q_s)$. Let $v$ be internal and take a placement $P_v$. Its restriction to each child subtree $T_u$ has a pair dominated by some pair $p_u$ of $L(u)$, by induction. The wire map of Lemma 3 is monotone: if $(c, q)$ dominates $(c', q')$ then $(c + W, q - R(W/2 + c))$ dominates $(c' + W, q' - R(W/2 + c'))$, since $R \ge 0$. So after the wire, some pair of the moved list dominates the branch of $P_v$, and PRUNE keeps a dominating pair (Lemma 4). The join map is monotone in both arguments in the same sense, so by Lemma 5 the joined list holds a pair that dominates the pair of $P_v$ without its buffer at $v$. If $P_v$ has a buffer of type $b$ at $v$, its pair is $(C_b, q' - D_b - R_b c')$ for the unbuffered pair $(c', q')$, and the candidate for $b$ uses the best value of $q - D_b - R_b c$ over the list, which is at least $q' - D_b - R_b c'$ for a pair that dominates $(c', q')$. Each record holds the placement whose pair it is, by Lemma 3. At the source the slack is $q - D_d - R_d c$ by Lemma 2 with an empty outside, which is nonincreasing in $c$ and increasing in $q$, so the best pair of $L(0)$ gives the best slack. $\square$

**Lemma 6 (list size).** With one buffer type, $|L(v)| \le s_v + p_v$, where $s_v$ is the number of sinks in $T_v$ and $p_v$ the number of candidate nodes in $T_v$. With $k$ types, $|L(v)| \le s_v + k p_v$.

*Proof.* A sink has one pair. The wire map and PRUNE do not make a list longer. The join of lists of lengths $a$ and $b$ makes at most $a + b - 1$ steps, since each step moves at least one pointer and the loop stops when a pointer leaves its list, so it outputs at most $a + b - 1$ pairs. A buffer step adds $k$ pairs. Summing over the children gives the bound. $\square$

**Theorem 2 (time).** With one buffer type the algorithm takes $O(n^2)$ time and $O(n^2)$ space for the records in the worst case.

*Proof.* At node $v$, the wire map, PRUNE, the buffer step (one pass for the best value and one merge) and the join each take time linear in the lengths of the lists they read, which are at most $s_v + p_v \le n$ by Lemma 6. Each node does a constant number of these steps per child, so the total is $\sum_v O(n) = O(n^2)$. Each step makes $O(1)$ new records per pair, which bounds the record space by the same sum. $\square$
