---
title: Weak division returns the unique largest algebraic quotient
proves: [correctness]
status: full
---

Cubes are sets of literals with at most one literal of each variable, and an SOP is a set of cubes. For a cube or SOP $G$, $\mathrm{sup}(G)$ is the set of its variables. Fix SOPs $F$ and $D = \{d_1, \ldots, d_k\}$ with $k \ge 1$. Call a cube $q$ *allowed* if $\mathrm{sup}(q) \cap \mathrm{sup}(D) = \emptyset$ and $q \cup d_i \in F$ for $i = 1, \ldots, k$, and let $\mathcal{Q}$ be the set of allowed cubes. A quotient in the sense of the page is a set $Q$ of allowed cubes that contains every allowed cube, so $\mathcal{Q}$ is the only quotient, and the remainder is then fixed as $F \setminus \mathcal{Q} D$.

**Lemma 1.** If $q$ is allowed, then $q \in V_i$ for every $i$.

*Proof.* The cube $c = q \cup d_i$ is in $F$ and contains $d_i$. Since $q$ has no variable of $d_i$, $q \cap d_i = \emptyset$, so $c \setminus d_i = q$, and line L2 puts $q$ in $V_i$. $\square$

**Lemma 2.** If $q \in V_i$ for every $i$, then $q$ is allowed.

*Proof.* For each $i$ there is a cube $c_i \in F$ with $d_i \subseteq c_i$ and $q = c_i \setminus d_i$. Then $q \cup d_i = c_i \in F$. Let $x$ be a variable of $D$, and pick $i$ with a literal $\lambda$ of $x$ in $d_i$. The cube $c_i$ contains $\lambda$ and, being a cube, no other literal of $x$. So $c_i \setminus d_i$ has no literal of $x$, and $x \notin \mathrm{sup}(q)$. $\square$

**Lemma 3.** After the loop of lines L1 to L3, $Q = \bigcap_i V_i$. The early stop does not change this.

*Proof.* Line L3 sets $Q$ to $V_1$ and then intersects it with each later $V_i$. If $Q$ becomes empty, every later intersection is empty too, so stopping returns the same set. $\square$

**Theorem.** WEAK-DIVIDE returns $Q = \mathcal{Q}$ and $R = F \setminus \mathcal{Q} D$. These satisfy $F = Q D \cup R$, $Q D \cap R = \emptyset$ and $\mathrm{sup}(Q) \cap \mathrm{sup}(D) = \emptyset$, and they are the unique quotient and remainder.

*Proof.* By Lemmas 1 to 3, $Q = \bigcap_i V_i = \mathcal{Q}$. Every cube of $Q$ is allowed, so $\mathrm{sup}(Q) \cap \mathrm{sup}(D) = \emptyset$ and every product $q \cup d$ of line L4 lies in $F$. So $P = Q D \subseteq F$, and line L5 gives $R = F \setminus P$, which is disjoint from $P$ and satisfies $P \cup R = F$. A quotient must contain every allowed cube and may contain no other cube, so it equals $\mathcal{Q}$, and then $R$ is fixed. $\blacksquare$
