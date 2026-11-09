---
title: Bucket elimination is correct
proves: [correctness, termination]
status: full
---

Fix a CSP with variables $x_1, \ldots, x_n$ in the order of the algorithm, domains $D_i$, and a set $C$ of constraints. An assignment of $x_1, \ldots, x_i$ is *admissible* if each value lies in its domain. For a set $K$ of constraints whose scopes lie inside $\{x_1, \ldots, x_i\}$, let $\mathrm{Sol}_i(K)$ be the set of admissible assignments of $x_1, \ldots, x_i$ that satisfy every constraint of $K$.

Each constraint goes into the bucket of the latest variable of its scope (line L1), and a new constraint $R_U$ made in the bucket of $x_i$ goes into the bucket of the latest variable of $U \subseteq \{x_1, \ldots, x_{i-1}\}$ (line L6). So a constraint in the bucket of $x_j$ has its scope inside $\{x_1, \ldots, x_j\}$ and contains $x_j$, and constraints are only ever added to buckets of variables earlier than the one being processed. In particular, the bucket of $x_i$ does not change after line L2 reaches $x_i$. Write $B_i$ for its final content.

**Termination.** Each loop runs over a finite list, and line L4 runs over a finite product. So the algorithm stops.

**Invariant.** For $0 \le i \le n$, let $C_i$ be the union of the buckets of $x_1, \ldots, x_i$ right after the iteration of line L2 for $x_{i+1}$ (for $i = n$, right after line L1). Then $C_n = C$.

**Lemma 1 (projection).** Let $1 \le i \le n$, and suppose the iteration for $x_i$ does not return at line L5. Then an admissible assignment $\tau$ of $x_1, \ldots, x_{i-1}$ lies in $\mathrm{Sol}_{i-1}(C_{i-1})$ exactly when some $a \in D_{x_i}$ gives $(\tau, x_i = a) \in \mathrm{Sol}_i(C_i)$. If the iteration returns at line L5, then $\mathrm{Sol}_i(C_i) = \emptyset$.

*Proof.* $C_i$ is the disjoint union of $B_i$ and the set $K$ of constraints in the buckets of $x_1, \ldots, x_{i-1}$ at that time. The constraints of $K$ do not mention $x_i$. The iteration for $x_i$ computes $R_U$ from $B_i$, and $C_{i-1} = K \cup \{R_U\}$ if $U \ne \emptyset$, and $C_{i-1} = K$ if $U = \emptyset$.

By line L4, for an admissible $\tau$, $\tau|_U \in R_U$ holds exactly when some $a \in D_{x_i}$ makes $(\tau, x_i = a)$ satisfy every constraint of $B_i$, since the scopes in $B_i$ lie inside $U \cup \{x_i\}$. So, when $U \ne \emptyset$: $(\tau, x_i = a)$ satisfies $C_i$ for some $a$ exactly when $\tau$ satisfies $K$ and $\tau|_U \in R_U$, that is, $\tau \in \mathrm{Sol}_{i-1}(C_{i-1})$. When $U = \emptyset$ and $R_U$ is not empty, some $a$ satisfies $B_i$ whatever $\tau$ is, and the same equivalence holds with $C_{i-1} = K$.

If line L5 returns, then $R_U = \emptyset$, so no admissible $(\tau, x_i = a)$ satisfies $B_i \subseteq C_i$, and $\mathrm{Sol}_i(C_i) = \emptyset$. $\square$

**Theorem.** BUCKET-ELIMINATION returns NONE if the CSP has no solution, and otherwise returns a solution.

*Proof.* Suppose line L5 returns during the iteration for $x_i$. Then $\mathrm{Sol}_i(C_i) = \emptyset$ by Lemma 1. Applying the first part of Lemma 1 for $i + 1, \ldots, n$, whose iterations did not return, an element of $\mathrm{Sol}_n(C_n)$ would restrict to an element of $\mathrm{Sol}_i(C_i)$, so $\mathrm{Sol}_n(C) = \emptyset$, and the CSP has no solution.

Suppose line L5 never returns. We show by induction on $i$ that after line L8 handles $x_i$, the assignment $x_1, \ldots, x_i$ is admissible and satisfies every constraint of $B_1, \ldots, B_i$.

Line L8 handles $x_i$ after $x_1, \ldots, x_{i-1}$, whose assignment $\tau$ satisfies $B_1, \ldots, B_{i-1}$ by the hypothesis (for $i = 1$, $\tau$ is empty). In the iteration for $x_i$, line L4 made $R_U$ from $B_i$. If $U \ne \emptyset$, line L6 put $R_U$ into the bucket of some $x_j$ with $j < i$, so $R_U \in B_j$ and $\tau|_U \in R_U$. If $U = \emptyset$, $R_U$ is not empty because line L5 did not return, so it contains the empty tuple, which is $\tau|_U$. In both cases line L4 gives some $a \in D_{x_i}$ such that $(\tau, x_i = a)$ satisfies every constraint of $B_i$, and line L8 picks the first such $a$. The constraints of $B_1, \ldots, B_{i-1}$ do not mention $x_i$, so they stay satisfied.

After $x_n$, the assignment is admissible and satisfies every constraint in every bucket. Every input constraint was put in some bucket at line L1 and stays there, so the assignment is a solution. $\blacksquare$

**Remark (counting).** In the counting form, each table of the bucket of $x_i$ is replaced by a function to the integers, and line L4 computes $f_U(t) = \sum_{a \in D_{x_i}} \prod_{g \in B_i} g(t, a)$. The same decomposition as in Lemma 1, with the sum over $a$ in place of "some $a$" and the distributive law to move the factors of $K$, which do not depend on $x_i$, out of the sum, shows that $\sum_{\tau} \prod_{g \in C_{i-1}} g(\tau) = \sum_{\sigma} \prod_{g \in C_i} g(\sigma)$, where $\tau$ and $\sigma$ range over admissible assignments of $x_1, \ldots, x_{i-1}$ and of $x_1, \ldots, x_i$, and the product for an input constraint is 1 on allowed tuples and 0 on others. At $i = n$ the right side is the number of solutions, and at $i = 0$ the left side is the product of the tables with empty scope, which the implementation returns.
