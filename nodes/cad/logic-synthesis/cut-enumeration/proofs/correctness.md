---
title: The merge of fanin cuts gives exactly the minimal k-feasible cuts
proves: [correctness]
status: full
---

Let $G$ be a directed acyclic graph whose sources are the primary inputs (PIs). A set $C$ is a cut of $v$ if every path from a PI to $v$ meets $C$, and it is minimal if no proper subset of it is a cut of $v$. Write $\mathcal{M}_k(v)$ for the set of minimal cuts of $v$ with at most $k$ nodes. The cone of $v$ is the set of nodes from which $v$ can be reached.

**Lemma 1 (minimal cuts lie in the cone).** Every minimal cut $C$ of $v$ is a subset of the cone of $v$. If $C \ne \{v\}$, then $v \notin C$.

*Proof.* A node outside the cone is on no path to $v$, so removing it from $C$ leaves a cut. If $v \in C$, then $\{v\}$ is a cut inside $C$, so $C = \{v\}$ by minimality. $\square$

**Lemma 2 (a cut of v cuts each fanin).** Let $u$ be a fanin of $v$ and $C$ a cut of $v$ with $v \notin C$. Then $C$ is a cut of $u$.

*Proof.* A path $P$ from a PI to $u$, followed by the edge $u \to v$, is a path to $v$, so it meets $C$. It does not meet $C$ at $v$, so $P$ meets $C$. $\square$

**Lemma 3 (unions of fanin cuts).** Let $v$ have fanins $u_1, \ldots, u_d$, $d \ge 1$, and let $C_i$ be a cut of $u_i$ for each $i$. Then $C_1 \cup \cdots \cup C_d$ is a cut of $v$.

*Proof.* A path from a PI to $v$ has at least one edge, since $v$ is not a PI, and its last edge is $u_i \to v$ for some $i$. The part before that edge is a path from a PI to $u_i$, which meets $C_i$. $\square$

**Theorem.** For every node $v$, CUTS sets $\Phi(v) = \mathcal{M}_k(v)$.

*Proof.* Induction on the topological order. For a PI $v$, the only path from a PI to $v$ is the path with the one node $v$, so a cut must contain $v$, and $\{v\}$ is the only minimal cut. Line L3 sets $\Phi(v) = \{\{v\}\}$.

Let $v$ be a gate with fanins $u_1, \ldots, u_d$, and assume $\Phi(u_i) = \mathcal{M}_k(u_i)$ for each $i$, which holds since each fanin comes before $v$. Let $A_7$ be the set $A$ after the last run of line L7, and $A_8$ the set after line L8. After the $j$-th run of line L7, $A$ holds exactly the sets $c_1 \cup \cdots \cup c_j$ with $c_i \in \Phi(u_i)$ such that each partial union $c_1 \cup \cdots \cup c_i$, $i \le j$, has at most $k$ nodes. The partial unions grow with $i$, so this is the same as asking that the full union $c_1 \cup \cdots \cup c_j$ has at most $k$ nodes. So
$$A_7 = \{\, c_1 \cup \cdots \cup c_d : c_i \in \mathcal{M}_k(u_i),\ |c_1 \cup \cdots \cup c_d| \le k \,\}.$$

*Every set of $A_7$ is a $k$-feasible cut of $v$ that does not contain $v$.* It is a cut by Lemma 3 and has at most $k$ nodes. Each $c_i$ lies in the cone of $u_i$ by Lemma 1, and $v$ is not in the cone of $u_i$ because $G$ is acyclic.

*$A_8 \subseteq \mathcal{M}_k(v)$.* Let $C \in A_8$ and suppose that a proper subset $C' \subsetneq C$ is a cut of $v$. Then $v \notin C'$, so $C'$ is a cut of each $u_i$ by Lemma 2. Let $c_i \subseteq C'$ be a minimal cut of $u_i$; one exists because $C'$ is finite. Then $|c_i| \le |C'| < |C| \le k$, so $c_i \in \mathcal{M}_k(u_i)$, and $D = c_1 \cup \cdots \cup c_d \subseteq C'$ has at most $k$ nodes, so $D \in A_7$. Now $D \subseteq C' \subsetneq C$, so $C$ contains another set of $A_7$, and line L8 drops it, a contradiction. So $C$ is a minimal cut of $v$.

*$\mathcal{M}_k(v) \setminus \{\{v\}\} \subseteq A_8$.* Let $C$ be a minimal $k$-feasible cut of $v$ other than $\{v\}$. By Lemma 1, $v \notin C$, so $C$ is a cut of each $u_i$ by Lemma 2. Let $c_i \subseteq C$ be a minimal cut of $u_i$. It has at most $|C| \le k$ nodes, so $c_i \in \mathcal{M}_k(u_i) = \Phi(u_i)$. The union $D = c_1 \cup \cdots \cup c_d$ is a subset of $C$, and it is a cut of $v$ by Lemma 3, so $D = C$ by the minimality of $C$. Its size is at most $k$, so $C \in A_7$. If $C$ contained another set $E$ of $A_7$, then $E$ would be a cut of $v$ and a proper subset of $C$, which contradicts minimality. So line L8 keeps $C$.

Line L9 adds $\{v\}$, which is a minimal cut of $v$ with one node, and no set of $A_8$ equals $\{v\}$. Together, $\Phi(v) = A_8 \cup \{\{v\}\} = \mathcal{M}_k(v)$. $\blacksquare$

**Corollary (without pruning).** If line L8 is left out, every set of $\Phi(v)$ is still a $k$-feasible cut of $v$, and $\Phi(v) \supseteq \mathcal{M}_k(v)$.

*Proof.* Induction on the topological order, with the claim that every set of $\Phi(u)$ is a $k$-feasible cut of $u$ inside the cone of $u$, and that $\mathcal{M}_k(u) \subseteq \Phi(u)$. For a PI both hold. For a gate $v$, every set made at line L7 is a union of cuts of the fanins, so it is a cut of $v$ by Lemma 3, it has at most $k$ nodes by the test, and it lies in the cone of $v$. The argument of the last part of the theorem uses only $\mathcal{M}_k(u_i) \subseteq \Phi(u_i)$, so it shows that every minimal $k$-feasible cut of $v$ other than $\{v\}$ is made at line L7. $\square$

**Termination and order.** Each step handles finite sets, so CUTS ends. The set $A_7$ above does not depend on the order of the fanins, so neither does $\Phi$.
