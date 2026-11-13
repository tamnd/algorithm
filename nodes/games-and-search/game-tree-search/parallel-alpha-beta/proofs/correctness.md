---
title: Parallel alpha-beta with the Young Brothers Wait rule returns the alpha-beta value, whatever the order in which the results arrive
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode PARALLEL-AB of the page and the simulated machine of the tests. Values are negamax values for the side to move. Let $V(n)$ be the negamax value of $n$ in the tree cut at depth $d$, with EVALUATE at the cut and at terminal nodes. A value $r$ is a *fail-soft answer* for $V(n)$ with the window $(\alpha, \beta)$, $\alpha < \beta$, when
$$ V(n) \le r \le \alpha \ \text{ if } V(n) \le \alpha, \qquad r = V(n) \ \text{ if } \alpha < V(n) < \beta, \qquad \beta \le r \le V(n) \ \text{ if } V(n) \ge \beta. $$
Sequential fail-soft [alpha-beta](/alpha-beta-pruning/) returns a fail-soft answer, and with the window $(-\infty, +\infty)$ it returns $V(n)$.

For a child $c$ of $n$, write $u(c) = -V(c)$ for its value seen from $n$. If the call on $c$ uses the window $(-\beta, -a)$ and returns a fail-soft answer $r$, then $t = -r$ satisfies three facts, as in the proof for [quiescence search](/quiescence-search/):

- if $t \ge \beta$, then $\beta \le t \le u(c)$;
- if $a < t < \beta$, then $t = u(c)$;
- if $t \le a$, then $u(c) \le t$.

**Theorem 1 (correctness).** Every call PARALLEL-AB$(n, d, \alpha, \beta)$ that is not cancelled returns a fail-soft answer for $V(n)$, for every number of processors and every order in which the results of the young brothers arrive.

*Proof.* By induction on $d$. Line L1 is the base case. Let $c_1$ be the eldest child, and let the other children be $c_2, \ldots, c_k$. By induction, line L4 gives $m = t_1$ with the three facts for $a_1 = \alpha$. If $m \ge \beta$, line L5 returns $m$, and $\beta \le m \le u(c_1) \le V(n)$.

Otherwise the young brothers run. A young brother $c_i$ reads $a_i = \max(m, \alpha)$ at line L7 when it starts, where $m$ is the value at that time. The value $m$ never decreases, so $a_i$ is at most the value of $\max(m, \alpha)$ at any later time. By induction, $c_i$ returns with the three facts for $a_i$. Line L9 takes the maximum in the order of arrival.

*Case of a cutoff at line L10 on the result $t_j$.* Then $t_j = m \ge \beta$, because $m$ was below $\beta$ before. By the first fact, $\beta \le t_j \le u(c_j) \le V(n)$, and the returned $m = t_j$ is a fail-soft answer. The cancelled brothers do not matter, because the answer needs only $V(n) \ge \beta$.

*Case of no cutoff.* All results $t_1, \ldots, t_k$ are below $\beta$, and line L11 returns $M = \max_i t_i$. By the second and third facts, $u(c_i) \le t_i$ for all $i$, so $V(n) = \max_i u(c_i) \le M$. If $M \le \alpha$, this is a fail-soft answer. If $M > \alpha$, let $t_j$ be the result whose arrival first made $m$ equal to $M$. Just before that arrival, $m < M$. The brother $c_j$ started before its result arrived, so $a_j = \max(m_{\text{start}}, \alpha)$ with $m_{\text{start}} < M$ and $\alpha < M$, hence $a_j < t_j = M < \beta$. (For $j = 1$, $a_1 = \alpha < M$ directly.) The second fact gives $t_j = u(c_j)$, so $M \le V(n)$, and $M = V(n)$. $\square$

**Corollary 2.** At the root, called with $(-\infty, +\infty)$, the parallel search returns $V(\text{root})$, the value of sequential alpha-beta. The tests check this on 500 random trees with $P = 1, 2, 4, 8$, with and without the wait for the eldest brother.

**Theorem 3 (termination of the simulation).** On a finite tree with $P \ge 1$ processors, the simulated machine finishes, and the number of time steps is at most the number of node visits.

*Proof.* A task waits only for its own children. Take an unfinished task that is not cancelled and has no unfinished, uncancelled child; one exists while the root is unfinished, because the tree of tasks is finite. This task is not blocked, so it is running or on the ready stack, and an idle processor takes it. So in each time step before the end, at least one processor visits a node. Each task visits at most the nodes of its subtree, and the tasks of a node are made once, so the number of visits is finite. A time step is counted only when a node is visited, so the steps are at most the visits. $\square$

**Theorem 4 (one processor).** With $P = 1$, the simulated search visits exactly the nodes of sequential alpha-beta, in the same order.

*Proof.* The ready stack has the eldest young brother on top. With one processor, the task that runs is always the newest one that is ready, so the young brothers of a node run one at a time, in order, and each runs to its end before the next starts: its own spawned tasks lie above it on the stack. When $c_i$ starts, $m$ is the maximum of the results of $c_1, \ldots, c_{i-1}$, which is the value that sequential alpha-beta has before $c_i$. So each call has the same window as in the sequential search, and by induction it visits the same nodes and returns the same value. The tests check the node counts on 200 trees. $\square$

**Theorem 5 (cost).** Let $N_P$ be the number of node visits with $P$ processors and $T_P$ the number of time steps. Then $T_P \ge N_P / P$, so the speedup $N_1 / T_P$ is at most $P \cdot N_1 / N_P$. The ratio $N_P / N_1$ is the *search overhead*: the nodes that a parallel search visits because it starts young brothers before their windows are as good as in the sequential search.

*Proof.* In each time step, each of the $P$ processors visits at most one node. $\blacksquare$
