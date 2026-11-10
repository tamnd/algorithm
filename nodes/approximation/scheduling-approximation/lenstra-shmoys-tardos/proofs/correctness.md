---
title: The Lenstra-Shmoys-Tardos rounding is a 2-approximation
proves: [correctness]
status: full
---

We use the notation of the page: $p_{ij} \in \{1, 2, \ldots\} \cup \{\infty\}$, $S_T = \{(i, j) : p_{ij} \le T\}$, and the program $\mathrm{LP}(T)$ with the job constraints $\sum_i x_{ij} = 1$, the machine constraints $\sum_j p_{ij} x_{ij} \le T$ and $x \ge 0$, over the variables $x_{ij}$ with $(i, j) \in S_T$. A point $x$ of a polytope is a *vertex* if it is not the midpoint of two different points of the polytope. For a point $x$, the *support graph* $G(x)$ is the bipartite graph on jobs and machines with an edge $ij$ for each $x_{ij} > 0$.

**Lemma 1 (monotone, and a lower bound).** If $\mathrm{LP}(T)$ has a solution and $T' \ge T$, then $\mathrm{LP}(T')$ has one. If $T \ge \mathrm{OPT}$, then $\mathrm{LP}(T)$ has a solution. So the least integer $T$ of line L1 satisfies $T \le \mathrm{OPT}$.

*Proof.* $S_T \subseteq S_{T'}$, so a solution of $\mathrm{LP}(T)$, with zeros on the new pairs, solves $\mathrm{LP}(T')$. For the second claim, let $\sigma$ be an optimal schedule and set $x_{ij} = 1$ if $\sigma(j) = i$ and 0 otherwise. Each used pair has $p_{ij} \le \mathrm{OPT} \le T$, so it is in $S_T$; each job has one 1; each machine has load at most $\mathrm{OPT} \le T$. The value $\mathrm{OPT}$ is an integer because the times are integers, so the least integer $T$ with a solution is at most $\mathrm{OPT}$. $\square$

**Lemma 2 (vertices are sparse).** Let $Q$ be a polytope $\{x \ge 0 : Ax = b,\ Cx \le d\}$ in $\mathbb{R}^N$, where $A$ has $r$ rows and $C$ has $s$ rows. Each vertex of $Q$ has at most $r + s$ positive entries.

*Proof.* Let $x$ be a vertex and $P$ the set of its positive entries. Suppose $|P| > r + s$. Let $s'$ be the number of rows of $C$ that hold with equality at $x$. Consider the system of the $r$ rows of $A$ and these $s'$ rows of $C$, restricted to the columns in $P$. It has $r + s' < |P|$ equations, so it has a nonzero solution $y$ with $y_k = 0$ for $k \notin P$. For a small $\delta > 0$, both $x + \delta y$ and $x - \delta y$ keep the positive entries positive, keep $Ax = b$ and the tight rows of $C$, and keep the rows of $C$ that are not tight strictly below $d$. So both are in $Q$, they differ, and $x$ is their midpoint. This contradicts that $x$ is a vertex. $\square$

**Lemma 3 (the support is a pseudoforest).** Let $x$ be a vertex of $\mathrm{LP}(T)$. Each connected component of $G(x)$ has at most as many edges as vertices.

*Proof.* Let $K$ be a component of $G(x)$, with job set $J_K$ and machine set $M_K$. Let $Q_K$ be the polytope of the variables $x_{ij}$ with $(i, j) \in S_T$, $i \in M_K$ and $j \in J_K$, with the job constraints of $J_K$, the machine constraints of $M_K$ (with right side $T$) and $x \ge 0$. Let $x_K$ be the restriction of $x$ to these variables. Every positive $x_{ij}$ with $i \in M_K$ or $j \in J_K$ is an edge of $K$, so it is one of these variables. Hence $x_K$ satisfies the constraints of $Q_K$, and $x_K \in Q_K$.

Suppose $x_K = \frac12 (y + z)$ with $y \ne z$ in $Q_K$. Let $y'$ be $x$ with the entries of $x_K$ replaced by $y$, and $z'$ the same with $z$. For a job in $J_K$, all its positive entries in $x$ lie in $K$, and $y$ satisfies its constraint. For a machine in $M_K$, its load in $y'$ is its load in $y$, because its other entries are 0 in $x$. Jobs and machines outside $K$ see only entries of $x$, because no edge of $K$ touches them, and every variable of $Q_K$ that is positive in $y$ or $z$ joins $J_K$ to $M_K$. So $y', z' \in \mathrm{LP}(T)$, $y' \ne z'$, and $x = \frac12(y' + z')$, which contradicts that $x$ is a vertex. So $x_K$ is a vertex of $Q_K$.

$Q_K$ has $|J_K|$ equality rows and $|M_K|$ inequality rows, so by Lemma 2, $x_K$ has at most $|J_K| + |M_K|$ positive entries. These are the edges of $K$. $\square$

A connected graph with at most as many edges as vertices is a tree or a tree with one more edge, so it has at most one cycle. Each subgraph of such a graph also has components with at most one cycle, and so with at most as many edges as vertices. Since the graph is bipartite, every cycle has even length.

**Lemma 4 (the matching step).** Let $H$ be the graph of line L4. Lines L5 to L9 give every job of $H$ a machine $\sigma(j)$ with $x_{\sigma(j) j} > 0$, and no machine gets two jobs from these lines.

*Proof.* A job $j$ of $H$ has no entry equal to 1, and its entries sum to 1, so it has at least two positive entries: its degree in $H$ is at least 2. By Lemma 3, every component of $H$ has at most as many edges as vertices.

We call a component of the current graph *of type A* if every job in it has degree at least 2, and *of type B* if it is a path whose two ends are a job and a machine. Every component of $H$ at line L4 is of type A. We show that each pass of the loop keeps all components of type A or B, with at most as many edges as vertices.

- *Line L7, in a type A component.* The machine $i$ has degree 1, so its only neighbour is $j$. Deleting $i$ and $j$ removes edges only at $j$ and at $i$. A job $j' \ne j$ loses an edge only if a deleted machine was next to it, and $i$ was next only to $j$. So every remaining job keeps its degree, and the new components are of type A.
- *Line L7, in a type B component.* The only machine of degree 1 on a path from a job to a machine is the machine end. Deleting it and the job next to it leaves a shorter path from the same job end to a machine, or nothing.
- *Line L8.* Here no machine has degree 1. A type B component has a machine of degree 1, so all components are of type A. Take a type A component $K$ with a job. Its jobs have degree at least 2, and its machines have degree at least 2, because the component is connected, has a job, and has no machine of degree 1. So the sum of the degrees is at least $2 |V(K)|$, which is twice the number of edges. With at most as many edges as vertices, every degree is exactly 2, and $K$ is a cycle. Deleting a job $j$ of the cycle and a neighbour $i$ leaves a path. One end is the other neighbour of $i$, a job, and the other end is the other neighbour of $j$, a machine. This is a component of type B.

In every pass, the job that line L7 or L9 assigns is next to the machine in the current graph, which is a subgraph of $H$, so $x_{\sigma(j) j} > 0$. Both are deleted at once, so no machine is used twice. Each pass deletes one job, and line L6 or line L8 always applies while a job is left, so the loop ends with every job of $H$ assigned. $\square$

**Theorem.** The schedule $\sigma$ of the algorithm has makespan at most $T + \max\{p_{ij} : 0 < x_{ij} < 1\} \le 2T \le 2\,\mathrm{OPT}$.

*Proof.* Each job gets one machine: in line L3 if one entry is 1, else in the loop by Lemma 4. Every assignment uses a pair with $x_{ij} > 0$, so a pair in $S_T$, and $p_{ij} \le T < \infty$. Fix a machine $i$. The jobs of line L3 on $i$ have total time

$$\sum_{j : x_{ij} = 1} p_{ij} \le \sum_j p_{ij} x_{ij} \le T,$$

by the machine constraint of $\mathrm{LP}(T)$. By Lemma 4 the loop adds at most one job $j$ to $i$, with $0 < x_{ij} < 1$, so of time at most $\max\{p_{ij} : 0 < x_{ij} < 1\} \le T$. Hence the load of $i$ is at most $2T$, and $T \le \mathrm{OPT}$ by Lemma 1. $\blacksquare$
