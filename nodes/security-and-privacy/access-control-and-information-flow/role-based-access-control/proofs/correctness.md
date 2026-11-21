---
title: The access check of RBAC computes the flattened relation, and the constraints stay true
proves: [correctness, invariant, termination]
status: full
---

Write $J$ for the set of immediate hierarchy edges: $(x, y) \in J$ when $y$ is a junior that was added to $x$ directly. The order $x \ge y$ is the reflexive and transitive closure $J^*$: there is a path of edges of $J$ from $x$ to $y$, possibly of length 0. For a set $X$ of roles write $\mathrm{below}(X) = \{y : x \ge y \text{ for some } x \in X\}$. A user $u$ is authorized for $\mathrm{auth}(u) = \mathrm{below}(\{x : (u, x) \in UA\})$.

The invariant (R) of a state is:

- (R1) $J$ has no cycle, so $\ge$ is a partial order.
- (R2) For each user $u$ and each static pair $(rs, n)$: $|\mathrm{auth}(u) \cap rs| < n$.
- (R3) For each session with user $u$ and active roles $X$: $X \subseteq \mathrm{auth}(u)$, and $|X \cap rs| < n$ for each dynamic pair $(rs, n)$.

**Lemma 1 (CHECK-ACCESS).** CHECK-ACCESS$(\mathit{sess}, p)$ returns true exactly when there is a role $y \in \mathrm{below}(X)$ with $(p, y) \in PA$, where $X$ is the set of active roles of the session. It ends after at most $|\mathrm{below}(X)|$ rounds that pass line L5.

*Proof.* Every role pushed is in $\mathrm{below}(X)$: line L1 pushes the roles of $X$, and line L7 pushes juniors of a popped role, and $\mathrm{below}(X)$ is closed under taking juniors. Line L5 adds each role to *seen* once, and line L4 skips a role that is already in *seen*, so lines L6 and L7 run at most once for each role of $\mathrm{below}(X)$. The pushes are at most the number of edges out of these roles plus $|X|$, so the loop ends.

If the loop returns true at line L6, the popped role $x$ is in $\mathrm{below}(X)$ and has $p$. Conversely, suppose some $y \in \mathrm{below}(X)$ has $(p, y) \in PA$, and assume the loop returns false. Take a path $x_0 \in X, x_1, \ldots, x_k = y$ of edges of $J$. Then $x_0$ is pushed at line L1, and if $x_i$ is popped and added to *seen*, line L6 does not return for it (the loop returns false at the end), and line L7 pushes $x_{i+1}$. A pushed role is popped before the stack is empty, and either it is added to *seen* then, or it was added earlier. By induction every $x_i$ is added to *seen*, including $y$, and at that time line L6 returns true, which is a contradiction. $\square$

**Lemma 2 (ADD-ACTIVE-ROLE keeps (R3)).** Line L9 refuses a role that is not in $\mathrm{auth}(u)$, and line L10 refuses a role that would break a dynamic pair. Line L11 adds the role only when both tests pass, so after it $X \cup \{x\} \subseteq \mathrm{auth}(u)$ and every dynamic pair holds. Dropping an active role makes $X$ smaller, which keeps (R3). $\square$

**Lemma 3 (administrative changes keep (R)).**

- ADD-INHERITANCE$(x, y)$ refuses the edge when $x \in \mathrm{below}(\{y\})$, which is exactly the case where the edge would close a cycle, so (R1) holds. It then adds the edge, computes $\mathrm{auth}(u)$ for every user, and removes the edge again if a static pair fails, so (R2) holds after it. A new edge only makes $\mathrm{auth}$ larger, so the active roles of a session stay authorized and (R3) holds.
- ASSIGN-USER$(u, x)$ computes the new $\mathrm{auth}(u)$ and refuses if a static pair fails. Other users are not changed, so (R2) holds; $\mathrm{auth}(u)$ grows, so (R3) holds.
- DEASSIGN-USER$(u, x)$ makes $\mathrm{auth}(u)$ smaller, which keeps (R2), and then intersects the active roles of each session of $u$ with the new $\mathrm{auth}(u)$, which keeps (R3).
- ADD-SSD and ADD-DSD refuse a pair that some user or some session already breaks, and a pair with $n < 2$ or $n > |rs|$.
- Changes of $PA$ do not appear in (R). $\square$

**Theorem.** In every state reached from the empty state, (R) holds. For a session of $u$ with active roles $X$, CHECK-ACCESS$(\mathit{sess}, p)$ is true exactly when $p \in \bigcup_{y \in \mathrm{below}(X)} PA^{-1}(y)$. If $X = \mathrm{auth}(u)$, this set is the row of $u$ in the flattened relation $UA \circ RH^* \circ PA$: the permissions $p$ with $(u, x) \in UA$, $x \ge y$ and $(p, y) \in PA$ for some roles $x$ and $y$.

*Proof.* The empty state holds (R). By Lemmas 2 and 3 each operation keeps it. The first claim about CHECK-ACCESS is Lemma 1. For $X = \mathrm{auth}(u)$ we have $\mathrm{below}(X) = \mathrm{auth}(u)$, because $\mathrm{auth}(u)$ is already closed under taking juniors, and $y \in \mathrm{auth}(u)$ means $x \ge y$ for some $x$ with $(u, x) \in UA$, which is the definition of the composed relation. Such an $X$ can be activated role by role only if no dynamic pair forbids it; the tests of this page activate every authorized role in states with no dynamic pairs. $\blacksquare$
