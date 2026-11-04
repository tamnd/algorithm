---
title: The Balas additive algorithm returns an optimal 0-1 vector
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The problem is to minimize $c^\top x$ over $X = \{x \in \{0, 1\}^n : A x \le b\}$, with $c \ge 0$. Let $z^* = \min_{x \in X} c^\top x$, or $\infty$ if $X = \emptyset$. For a node $N = (O, v, s, F)$, let $X(N)$ be the set of $x \in \{0, 1\}^n$ with $x_j = 1$ for $j \in O$ and $x_j = 0$ for $j \notin O \cup F$. For such $x$, write $U = \{j \in F : x_j = 1\}$; then $c^\top x = v + \sum_{j \in U} c_j$ and $b - A x = s - \sum_{j \in U} A_j$.

**Claim 1 (node data).** For every node on the stack, $v = \sum_{j \in O} c_j$, $s = b - \sum_{j \in O} A_j$, and $O$ and $F$ are disjoint. *Proof.* True for the root. Line L11 adds $j \in F$ to $O$, adds $c_j$ to $v$, subtracts $A_j$ from $s$, and removes $j$ from $F$; line L10 removes $j$ from $F$ only. $\square$

**Claim 2 (children cover the parent).** If $N$ is split on $j$ at lines L10 and L11 into $N_0$ and $N_1$, then $X(N) = X(N_0) \cup X(N_1)$. *Proof.* A vector in $X(N)$ has $x_j = 0$, and lies in $X(N_0)$, or $x_j = 1$, and lies in $X(N_1)$. $\square$

**Claim 3 (a node that is not split loses nothing).** Let $N$ be popped at line L3 with the current value $z$. If the loop continues at line L6, then after line L5, every $x \in X(N) \cap X$ has $c^\top x \ge z$. If the loop continues at line L8, then every $x \in X(N) \cap X$ has $c^\top x \ge z$.

*Proof.* Line L6: $s \ge 0$, so the vector with $U = \emptyset$ is in $X$ and costs $v$. Line L5 makes $z \le v$, and every $x \in X(N)$ has $c^\top x = v + \sum_{j \in U} c_j \ge v \ge z$ since $c \ge 0$.

Line L8: suppose that $x \in X(N) \cap X$ has $c^\top x < z$. Every $j \in U$ has $v + c_j \le c^\top x < z$. Let $I^- = \{i : s_i < 0\}$, which is not empty because line L4 failed. For $i \in I^-$, feasibility gives $s_i - \sum_{j \in U} a_{ij} \ge 0$, so $s_i - \sum_{j \in U, a_{ij} < 0} a_{ij} \ge s_i - \sum_{j \in U} a_{ij} \ge 0$. Every $j \in U$ with $a_{ij} < 0$ for some $i \in I^-$ is in $T$. As $s_i < 0$, some $j \in U$ has $a_{ij} < 0$, so $T \ne \emptyset$; and $\sum_{j \in T} \min(0, a_{ij}) \le \sum_{j \in U, a_{ij} < 0} a_{ij}$, so $s_i - \sum_{j \in T} \min(0, a_{ij}) \ge 0$ for every $i \in I^-$. Then the test of line L8 fails, a contradiction. $\square$

**Claim 4 (invariant).** At the start of each iteration of line L2, every $x \in X$ with $c^\top x < z$ lies in $X(N)$ for some node $N$ on the stack, and $z = \infty$ with $best = \text{NIL}$, or $best$ gives a vector in $X$ of cost $z$.

*Proof.* At the start, the root has $X(\text{root}) = \{0, 1\}^n$. Suppose the claim holds at the start of an iteration that pops $N$, and let $x \in X$ have $c^\top x < z$ after the iteration. Since $z$ never increases, $c^\top x$ was below $z$ at the start too, so $x$ was in $X(N')$ for some $N'$ on the stack. If $N' \ne N$, then $N'$ is still there. If $N' = N$, Claim 3 rules out lines L6 and L8, so $N$ was split, and by Claim 2, $x$ is in a child, which is pushed. For the second part, line L5 sets $best = O$, whose vector, by Claim 1 and $s \ge 0$, is in $X$ with cost $v = z$. $\square$

**Claim 5 (termination).** Each child has $|F|$ one less than its parent, so every path of the search tree has at most $n$ splits, and the tree has at most $2^{n+1} - 1$ nodes. Each node is pushed once and popped once, so the loop ends. $\square$

**Theorem.** BALAS$(c, A, b)$ returns $z^*$ and an optimal vector if $X \ne \emptyset$, and $(\infty, \text{NIL})$ otherwise.

*Proof.* By Claim 5 the loop ends with an empty stack. By Claim 4, no $x \in X$ then has $c^\top x < z$, so $z \le z^*$; and $z$ is $\infty$ or the cost of a vector in $X$, so $z \ge z^*$. Hence $z = z^*$, and if $z < \infty$, $best$ gives an optimal vector. If $X = \emptyset$, line L5 never runs, since $s \ge 0$ at line L4 means that the zero completion is in $X$; so $best = \text{NIL}$. $\blacksquare$
