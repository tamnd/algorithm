---
title: Cutset conditioning is correct
proves: [correctness, termination]
status: full
---

Fix a binary CSP $P$ with variables $V$, domains $D_v$, a relation $R_{uv}$ for each edge $\{u, v\}$ of its constraint graph $G$, and a cycle cutset $S \subseteq V$, so that $G - S$ is a forest $F$. Let $Y = V \setminus S$. Every edge of $G$ is of one of three kinds: both ends in $S$, one end in $S$ and one in $Y$, or both ends in $Y$. The last kind are the edges of $F$.

For an assignment $s$ of $S$ with $s_x \in D_x$, let $P_s$ be the CSP on $Y$ with domains $D'_y$ as in line L4, $D'_y = \{b \in D_y : (s_x, b) \in R_{xy}$ for every neighbour $x \in S$ of $y\}$, and the constraints of $F$. Call $s$ *admissible* if it satisfies every constraint with both ends in $S$, which is the test of line L2.

**Termination.** Line L1 runs over the finite product of the domains of $S$, and each call of TREE-CSP or TREE-COUNT stops. So the algorithm stops.

**Lemma (decomposition).** The map that sends a solution $\sigma$ of $P$ to the pair $(\sigma|_S, \sigma|_Y)$ is a one-to-one correspondence between the solutions of $P$ and the pairs $(s, t)$ with $s$ admissible and $t$ a solution of $P_s$.

*Proof.* Let $\sigma$ be a solution of $P$, $s = \sigma|_S$ and $t = \sigma|_Y$. Then $s$ satisfies the constraints inside $S$, so it is admissible. For $y \in Y$, $t_y = \sigma_y \in D_y$, and for each neighbour $x \in S$ of $y$, $(\sigma_x, \sigma_y) \in R_{xy}$; so $t_y \in D'_y$. And $t$ satisfies the constraints of $F$ because $\sigma$ does. So $t$ is a solution of $P_s$.

Conversely, let $s$ be admissible and $t$ a solution of $P_s$, and let $\sigma = s \cup t$. Each value lies in its domain, since $D'_y \subseteq D_y$. Take an edge $\{u, v\}$ of $G$. If both ends are in $S$, $s$ satisfies it because $s$ is admissible. If $u \in S$ and $v \in Y$, then $t_v \in D'_v$, so $(s_u, t_v) \in R_{uv}$. If both ends are in $Y$, it is an edge of $F$ and $t$ satisfies it. So $\sigma$ is a solution.

The two maps are inverse to each other, because $S$ and $Y$ partition $V$. $\square$

**Theorem.** CUTSET-CONDITIONING returns a solution of $P$ if one exists and NONE otherwise. The counting form returns the number of solutions of $P$.

*Proof.* Line L1 enumerates every assignment $s$ of $S$ with values in the domains, and line L2 skips exactly the ones that are not admissible. For an admissible $s$, lines L3 and L4 build the domains of $P_s$, and $P_s$ is a binary CSP whose constraint graph is the forest $F$. By the correctness of the [tree-structured CSP algorithm](/tree-structured-csp/), line L5 returns a solution $t$ of $P_s$ if one exists, and NONE otherwise.

If line L6 returns $s \cup t$, it is a solution of $P$ by the lemma. If $P$ has a solution $\sigma$, then $\sigma|_S$ is admissible and $P_{\sigma|_S}$ has the solution $\sigma|_Y$, so line L5 returns a solution no later than the iteration for $s = \sigma|_S$, and the algorithm does not reach line L7. So NONE is returned only when $P$ has no solution.

For counting, TREE-COUNT returns the number of solutions of $P_s$ for each admissible $s$. The sets $\{(s, t) : t$ a solution of $P_s\}$ for different $s$ are disjoint, so by the lemma the sum of these numbers over all admissible $s$ is the number of solutions of $P$. $\blacksquare$
