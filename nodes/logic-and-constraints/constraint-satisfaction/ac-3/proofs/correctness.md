---
title: AC-3 computes the arc consistency closure
proves: [correctness, termination]
status: full
---

Fix a binary CSP with domains $D^0_1, \ldots, D^0_n$, one relation $R_{ij}$ for each arc, and $R_{ji}$ the converse of $R_{ij}$. For domains $D$ and $D'$ we write $D' \subseteq D$ when $D'_i \subseteq D_i$ for each $i$, and $D' \cup D''$ for the domains $D'_i \cup D''_i$. An arc $(i, j)$ is *consistent* in $D$ if every $a \in D_i$ has some $b \in D_j$ with $(a, b) \in R_{ij}$. The domains $D$ are arc consistent if all arcs are consistent in $D$.

**Lemma 1 (the closure).** If $D'$ and $D''$ are arc consistent, then so is $D' \cup D''$. So there is a largest arc consistent $D^\ast \subseteq D^0$: the union of all arc consistent domains inside $D^0$.

*Proof.* Let $a \in D'_i \cup D''_i$ and let $(i, j)$ be an arc. If $a \in D'_i$, some $b \in D'_j$ has $(a, b) \in R_{ij}$, and $b \in D'_j \cup D''_j$. The case $a \in D''_i$ is the same. There are finitely many $D \subseteq D^0$, and the domains that are all empty are arc consistent, so the union of all arc consistent $D \subseteq D^0$ exists and is arc consistent by the first part. It contains each arc consistent $D \subseteq D^0$, so it is the largest. $\square$

**Lemma 2 (REVISE keeps the closure).** If $D^\ast \subseteq D$ before REVISE$(i, j)$, then $D^\ast \subseteq D$ after it.

*Proof.* REVISE changes only $D_i$, and deletes $a$ only if no $b \in D_j$ has $(a, b) \in R_{ij}$. If $a \in D^\ast_i$, the arc $(i, j)$ is consistent in $D^\ast$, so some $b \in D^\ast_j \subseteq D_j$ has $(a, b) \in R_{ij}$. So $a$ is not deleted. $\square$

**Lemma 3 (the queue).** Each time line L3 tests the queue, every arc that is not in $Q$ is consistent in $D$.

*Proof.* At the first test, line L2 has put all arcs in $Q$. Assume the claim before an iteration that removes $(i, j)$ at line L4. After REVISE$(i, j)$, the arc $(i, j)$ is consistent, because each value of $D_i$ without a support in $D_j$ has been deleted and $D_j$ has not changed. If REVISE deletes nothing, no domain changes and the other arcs keep their state. If it deletes a set $G \ne \emptyset$ from $D_i$, consider the arcs that are not in $Q$ after line L8.

- An arc $(i, k)$ leaves $i$. Its values are now a subset of the old $D_i$, and $D_k$ is the same, so it stays consistent.
- An arc $(k, i)$ with $k \ne j$ is in $Q$ after line L8, so the claim says nothing about it.
- The arc $(j, i)$. Let $c \in D_j$. If $(j, i)$ was consistent, $c$ had a support $a$ in the old $D_i$, with $(c, a) \in R_{ji}$, so $(a, c) \in R_{ij}$. Then $a$ has the support $c \in D_j$ on $(i, j)$, so $a \notin G$, and $a$ is still in $D_i$. So $(j, i)$ stays consistent. If $(j, i)$ was in $Q$ before, it is still in $Q$.
- An arc that does not touch $i$ has the same domains as before.

So the claim holds at the next test. If line L6 returns, there is no next test. $\square$

**Termination.** Let $S = \sum_i |D_i|$. Each iteration either deletes at least one value, so $S$ drops by at least 1, or deletes nothing and makes $|Q|$ drop by exactly 1. $S$ starts at most $nd$ and never grows. Between two deletions, $|Q| \le 2e$ and it drops by 1 at each iteration, so there are at most $2e$ iterations between two deletions. So the loop runs at most $(nd + 1)(2e + 1)$ times. (The complexity section on the main page gives the sharper bound $2e(d+1)$.)

**Theorem.** AC-3 stops. It returns true if and only if no domain of $D^\ast$ is empty, and then the domains it leaves are $D^\ast$.

*Proof.* By Lemma 2 and induction over the revisions, $D^\ast \subseteq D$ holds at all times. Suppose AC-3 returns true at line L9. Then $Q = \emptyset$, so by Lemma 3 every arc is consistent and $D$ is arc consistent. $D \subseteq D^0$, so $D \subseteq D^\ast$ by Lemma 1. With $D^\ast \subseteq D$, this gives $D = D^\ast$. Line L1 and line L6 make sure that no domain is empty when line L9 runs, because a domain changes only at line L14 and line L6 tests it at once. So no domain of $D^\ast$ is empty.

Suppose AC-3 returns false, at line L1 or line L6. Then some $D_i$ is empty, and $D^\ast_i \subseteq D_i$ is empty too. So AC-3 returns false exactly when $D^\ast$ has an empty domain. $\blacksquare$

**Corollary (no solution is lost).** Let $s$ be a solution with $s_i \in D^0_i$. The domains $\{s_1\}, \ldots, \{s_n\}$ are arc consistent, because $(s_i, s_j) \in R_{ij}$ for each arc. So $s_i \in D^\ast_i$ for each $i$. In particular, if AC-3 returns false, the CSP has no solution.
