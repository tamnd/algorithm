---
title: Conflict-based search returns a solution of least sum of costs on every solvable instance
proves: [correctness, termination]
status: full
---

We use the pseudocode and the model of the page. There are $k$ agents on a graph with $n$ vertices (the free cells, with their grid neighbours). A *path* of agent $a$ gives its vertex $\pi(t)$ at each time $t = 0, 1, 2, \dots$, with $\pi(0) = s_a$; each step is a move along an edge or a wait, and from some time on the agent stays at $g_a$. Its *cost* $T$ is the least time with $\pi(t) = g_a$ for all $t \ge T$. A *solution* is one path for each agent with no vertex conflict ($\pi_i(t) = \pi_j(t)$) and no edge conflict ($\pi_i(t-1) = \pi_j(t)$ and $\pi_j(t-1) = \pi_i(t)$ with $\pi_i(t) \ne \pi_i(t - 1)$). Its cost is the sum of the costs of the paths, and $C^*$ is the least cost of a solution.

A *constraint* of agent $a$ is $(a, v, t)$, which forbids $\pi_a(t) = v$, or $(a, u, v, t)$ with $u \ne v$, which forbids the move $\pi_a(t - 1) = u$, $\pi_a(t) = v$. A path *satisfies* a set of constraints if it breaks none of them, also at the times after it reached its goal. A node $N$ of the constraint tree holds a set $C_a(N)$ of constraints for each agent, one path $\pi_a(N)$ for each agent, and the cost $\mathrm{cost}(N)$, the sum of the costs of its paths.

**Lemma 1 (the low level).** LOW-LEVEL$(a, C)$ stops. It returns a path of agent $a$ of least cost among the paths that satisfy $C$, or none if no path satisfies $C$.

*Proof.* Consider the space-time graph with the states $(v, t)$ and an arc from $(v, t)$ to $(w, t + 1)$ when $w = v$ or $w$ is a neighbour of $v$, and $C$ does not contain $(a, w, t + 1)$ or $(a, v, w, t + 1)$. Let $G$ be the largest $t$ with $(a, g_a, t) \in C$, or $-1$. A path of cost $T$ that satisfies $C$ is a walk from $(s_a, 0)$ to $(g_a, T)$ with $T > G$: the walk gives the first $T$ steps, and after $T$ the agent waits at $g_a$, which no constraint forbids because no vertex constraint at $g_a$ has a time after $G$ and edge constraints never forbid a wait. Conversely, such a walk followed by waits at $g_a$ is a path that satisfies $C$, with cost at most $T$. So the least cost is the least $T$ of a *target* state $(g_a, T)$ with $T > G$ that can be reached, which is what line L15 tests.

The heuristic is the grid distance $h(v)$ from $v$ to $g_a$. Each arc changes it by at most 1 and costs 1, and $h(g_a) = 0$, so it is consistent and admissible for the target states. Let $L$ be the largest time in $C$, or 0. From a state $(v, t)$ with $t \ge L + 1$ no arc is forbidden and every state $(g_a, t')$ with $t' \ge t$ is a target, so the part of the graph after $(v, t)$ is the part after $(v, t')$ moved by $t' - t$ in time. For $L + 1 \le t \le t'$, a walk from $(v, t')$ to a target thus gives a walk from $(v, t)$ to a target that is cheaper by $t' - t$. A* with a consistent heuristic takes states in an order of nondecreasing $t + h(v)$, so for one vertex $v$ it takes the smallest $t$ first, and the search loses nothing when it treats all $(v, t)$ with $t \ge L + 1$ as one state. With this rule there are at most $n (L + 2)$ states, so the search stops, and by the optimality of [A*](/a-star-search/) with a consistent heuristic the first target it takes has the least $T$. If it takes none, no target can be reached and no path satisfies $C$. $\square$

**Lemma 2 (each child adds a new constraint).** When line L10 makes a child of $N$ for agent $a$ with the constraint $c$, the path $\pi_a(N)$ breaks $c$. So $C_a(\mathrm{child}) = C_a(N) \cup \{c\}$ is strictly larger than $C_a(N)$.

*Proof.* For a vertex conflict $(i, j, v, t)$ of the paths of $N$, $\pi_i(t) = \pi_j(t) = v$, so $\pi_i$ breaks $(i, v, t)$ and $\pi_j$ breaks $(j, v, t)$. For an edge conflict where $\pi_i$ moves from $u$ to $v$ and $\pi_j$ from $v$ to $u$, both arriving at time $t$, $\pi_i$ breaks $(i, u, v, t)$ and $\pi_j$ breaks $(j, v, u, t)$. The path $\pi_a(N)$ satisfies $C_a(N)$, by Lemma 1 for the call that made it, so $c \notin C_a(N)$. $\square$

**Lemma 3 (paths are optimal for their node).** For each node $N$ and each agent $a$, $\pi_a(N)$ is a path of least cost among the paths of $a$ that satisfy $C_a(N)$.

*Proof.* At the root each path comes from LOW-LEVEL with the empty set (line L1). A child changes only the constraints of agent $a$ and gets its path from LOW-LEVEL with the new set (line L10). The other agents keep both their constraints and their paths. Lemma 1 gives the claim. $\square$

Call a node $N$ *compatible* with a solution $\pi^\star$ if $\pi^\star_a$ satisfies $C_a(N)$ for every agent $a$.

**Lemma 4 (a compatible child exists).** If $N$ is compatible with a solution $\pi^\star$ and line L9 splits $N$, then at least one child of $N$ is compatible with $\pi^\star$, and line L11 puts it in the open list.

*Proof.* For a vertex conflict $(i, j, v, t)$, the solution $\pi^\star$ cannot have both $\pi^\star_i(t) = v$ and $\pi^\star_j(t) = v$, because that is a vertex conflict. So it satisfies $(i, v, t)$ or $(j, v, t)$. For an edge conflict, it cannot both move agent $i$ from $u$ to $v$ and agent $j$ from $v$ to $u$ at time $t$, because that is an edge conflict. So it satisfies $(i, u, v, t)$ or $(j, v, u, t)$. The child with that constraint is compatible. Its agent $a$ has the path $\pi^\star_a$ that satisfies the new set, so LOW-LEVEL returns a path by Lemma 1, and line L11 adds the child. $\square$

**Lemma 5 (compatible nodes are cheap).** If $N$ is compatible with a solution $\pi^\star$, then $\mathrm{cost}(N) \le \mathrm{cost}(\pi^\star)$.

*Proof.* By Lemma 3, $\pi_a(N)$ has the least cost among the paths that satisfy $C_a(N)$, and $\pi^\star_a$ is one of them. Add over the agents. $\square$

**Theorem 6 (correctness and termination).** If the instance has a solution, CBS stops and returns a solution of cost $C^*$.

*Proof.* Fix a solution $\pi^\star$ of cost $C^*$. Each agent has a path to its goal, so line L1 does not stop. *Invariant:* until CBS returns, the open list holds a node compatible with $\pi^\star$. The root has no constraints, so it is compatible. When line L4 takes a compatible node, either line L6 returns, or the node is split and Lemma 4 adds a compatible child. So the open list is never empty before a return, and line L12 is never reached.

Each node that line L4 takes has the least cost in the open list, so by the invariant and Lemma 5 its cost is at most $C^*$. If it has no conflict, its paths start at the starts, end at the goals and have no conflicts, so they form a solution, of cost at least $C^*$. So line L6 returns a solution of cost exactly $C^*$.

It remains to show that line L4 runs only finitely often. Take a node $N$ that line L4 takes. Its paths have costs at most $\mathrm{cost}(N) \le C^*$. After the largest of these costs all agents wait at their goals, which are distinct, so no conflict happens later, and every conflict of $N$ has a time $t \le C^*$. The constraints of a node come from the conflicts of its ancestors, which were all taken by line L4. So every node that line L4 takes has only constraints with times at most $C^*$. There are at most $M = k \cdot 5 n \cdot (C^* + 1)$ such constraints (an agent, a vertex or one of at most $4n$ directed edges, and a time). By Lemma 2 the constraint sets grow strictly from a node to its child, so such a node has depth at most $M$ in the binary constraint tree, and there are fewer than $2^{M+1}$ of them. Each run of line L4 takes a different node, so the loop runs fewer than $2^{M+1}$ times. Each call of LOW-LEVEL stops by Lemma 1. $\square$

**Remarks.** If some agent cannot reach its goal at all, line L1 returns no solution, which is correct. If each agent can reach its goal but there is no solution, as when two agents must swap in a corridor, CBS can run forever: each node is split again, with ever later constraints, and the open list never becomes empty. The implementation therefore takes an optional limit on the number of nodes. The proof does not depend on which conflict line L5 picks, nor on how ties in line L4 are broken.
