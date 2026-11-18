---
title: MiniCon returns a maximally contained rewriting of a conjunctive query using conjunctive views
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The query is $Q(\bar x) \text{ :- } g_1, \ldots, g_n$ and each view is $V(\bar Y) \text{ :- } v_1, \ldots, v_r$ with $r \le m$. All terms are variables, there are no comparisons, and set semantics holds. A variable of a view is a *head variable* if it is in $\bar Y$ and *existential* otherwise. A rewriting $P$ is a conjunctive query over the view names. Its *expansion* $P^{exp}$ replaces each view atom $V(\bar a)$, the $k$-th atom of $P$, by the body of $V$ under the renaming $ren_k$ that sends the head variable at position $p$ to $a_p$ and each existential $u$ to a new variable $u_k$ used nowhere else. $P$ is *contained* in $Q$ if $P^{exp} \subseteq Q$. By the Chandra-Merlin theorem, $A \subseteq B$ for conjunctive queries if and only if there is a containment mapping from $B$ to $A$: a map on variables that sends the head of $B$ to the head of $A$ and each body atom of $B$ to a body atom of $A$.

An MCD is a tuple $(V, h, \varphi, G)$. Here $G$ is a set of subgoals of $Q$, $h$ maps the head variables of $V$ to head variables of $V$ with $h(h(y)) = h(y)$ (the head homomorphism), and $\varphi$ maps the variables of $G$ to variables of $V$ with values in the range of $h$ or existential, such that each $g \in G$ has a subgoal $v$ of $V$ with $\varphi(g) = h(v)$. Here $h$ is the identity on existentials. Property 1 is the pair of conditions of lines L12 and L13:

- (C1) $\varphi(x)$ is a head variable for each head variable $x$ of $Q$ in $G$;
- (C2) if $\varphi(x)$ is existential, then every subgoal of $Q$ that holds $x$ is in $G$.

**Lemma 1 (unification).** Let $\varphi, h$ be as above and let a subgoal $g$ of $Q$ and a subgoal $v$ of $V$ have the same predicate. Line L15 (and line L3, with $\varphi$ empty and $h$ the identity) returns the least restrictive extension $(\varphi', h')$ with $\varphi'(g) = h'(v)$ that equates no existential with another variable, or fails if none exists. It returns a result if there is a map $\rho$ from the variables of $V$ with $\rho \circ h = \rho$ on head variables, $\rho$ one to one on existentials with values that no head variable takes, and $\rho(\varphi(x)) = \rho(v_p)$ for each position $p$ at which $g$ holds $x$.

*Proof.* The procedure walks the positions of $g$. At position $p$ with variable $x$ and view variable $a = h(v_p)$, it sets $\varphi(x) = a$ if $\varphi(x)$ is not set. If $\varphi(x) = b \ne a$, then $b$ and $a$ must become one variable. This is possible only if both are head variables, and then the procedure merges their classes in $h$ and $\varphi$, keeping the head variable with the lowest position as the class name. Each merge is forced by the equation $\varphi(g) = h(v)$, so the result is the least restrictive one, and the choice of names makes it unique. Under the map $\rho$ of the second claim, $\rho(a) = \rho(v_p) = \rho(b)$. If $a$ or $b$ were existential, the conditions on $\rho$ would give $a = b$. So the procedure never fails, and the merges keep $\rho \circ h' = \rho$ and $\rho \circ \varphi' = \rho \circ \varphi$ on old variables. $\square$

**Lemma 2 (each output tuple is an MCD with Property 1).** Each tuple added at line L5 is an MCD that satisfies C1 and C2.

*Proof.* Lemma 1 keeps $\varphi(g) = h(v)$ for each subgoal added so far, since later merges apply to both sides. Line L12 rejects every state that breaks C1, and the state is only returned by line L13 when no subgoal outside $G$ holds a variable with an existential image, which is C2. $\square$

**Lemma 3 (soundness).** Each rewriting $Q'$ added at line L10 is contained in $Q$.

*Proof.* Line L7 picks MCDs $M_1, \ldots, M_c$, with $M_i = (V_i, h_i, \varphi_i, G_i)$, whose sets $G_i$ partition the subgoals of $Q$. Line L8 gives the classes $EC$, and line L9 gives the atom $V_i(\bar a^i)$ with $a^i_p = EC(\Psi_i(h_i(Y_p)))$, where $\Psi_i(y)$ is a variable $x$ with $\varphi_i(x) = y$ or a fresh variable. Let $ren_i$ be the renaming of the expansion of the $i$-th atom. For a head variable $y$, $ren_i(y) = a^i_p$ for its position $p$, and $ren_i(h_i(y)) = ren_i(y)$, since $h_i$ is idempotent and both give $EC(\Psi_i(h_i(y)))$.

Define $\tau(x) = ren_i(\varphi_i(x))$ for $x$ a variable of a subgoal of $G_i$. This does not depend on $i$. If $x$ occurs in $G_i$ and in $G_j$ with $i \ne j$, then $\varphi_i(x)$ is a head variable by C2, so $\tau(x) = EC(\Psi_i(\varphi_i(x))) = EC(x)$, because $\Psi_i(\varphi_i(x))$ is a variable with the same $\varphi_i$ image as $x$ and so in the class of $x$. The same holds for $j$.

For $g \in G_i$, there is $v$ with $\varphi_i(g) = h_i(v)$, so $\tau(g) = ren_i(h_i(v)) = ren_i(v)$, an atom of $Q'^{exp}$. For a head variable $x$ of $Q$, C1 gives $\tau(x) = EC(x)$, the head of $Q'$ at that position. So $\tau$ is a containment mapping from $Q$ to $Q'^{exp}$, and $Q' \subseteq Q$. $\square$

**Lemma 4 (completeness).** Let $P$ be a conjunctive rewriting with $P \subseteq Q$. Then some rewriting $Q'$ added at line L10 has $P \subseteq Q'$.

*Proof.* Take a containment mapping $\tau$ from $Q$ to $P^{exp}$. Each $\tau(g)$ is an atom of the expansion of some atom $k(g)$ of $P$, so $\tau(g) = ren_{k(g)}(v_g)$ for a subgoal $v_g$ of that view. Fix such choices. Let $G_k$ be the subgoals with $k(g) = k$, and write $\rho = ren_k$.

A variable of $P^{exp}$ of the form $u_k$ is existential in the $k$-th expansion and occurs only there. So if $\tau(x) = u_k$, every subgoal that holds $x$ is in $G_k$. Call two subgoals of $G_k$ *linked* if they share a variable $x$ with $\tau(x)$ of the form $u_k$.

Start the procedure at line L2 with a subgoal $g \in G_k$, the view of the $k$-th atom and the subgoal $v_g$. At line L14, take the branch $v_{g'}$ for the subgoal $g'$ that line L13 picks. By Lemma 1, applied with $\rho$, each unification succeeds and keeps $\rho(\varphi(x)) = \tau(x)$. So $\varphi(x)$ is existential exactly when $\tau(x)$ is of the form $u_k$, because $\rho$ sends head variables to variables of $P$ and existentials to variables $u_k$. Line L12 never fails, since a head variable $x$ of $Q$ has $\tau(x)$ in the head of $P$. Line L13 picks only subgoals linked to the current set. So this branch returns an MCD whose set is the linked component of $g$ in $G_k$. These components partition each $G_k$, and the sets $G_k$ partition the subgoals of $Q$. Line L7 enumerates this partition, since it tries every disjoint cover. Let $Q'$ be its rewriting.

Map each variable of $Q'$ to a variable of $P$. A class $EC(x)$ goes to $\tau(x)$. This is well defined, because $\varphi_i(x) = \varphi_i(y)$ gives $\tau(x) = \rho_i(\varphi_i(x)) = \tau(y)$. A fresh variable made at line L9 for the class of a head variable $y$ of $V_i$ goes to $\rho_i(y)$. Then the $p$-th argument of the $i$-th atom of $Q'$ goes to $\rho_i(h_i(Y_p)) = \rho_i(Y_p)$, the $p$-th argument of atom $k$ of $P$. The head $EC(\bar x)$ goes to $\tau(\bar x)$, the head of $P$. This is a containment mapping from $Q'$ to $P$, so $P \subseteq Q'$. $\square$

**Theorem.** MINICON stops, and the union $R$ of its output is a maximally contained rewriting of $Q$ using the views among unions of conjunctive queries: $R \subseteq Q$, and $P \subseteq R$ for each union of conjunctive queries $P$ over the views with $P \subseteq Q$.

*Proof.* Termination: each recursion of CLOSE adds a subgoal to $G$, so its depth is at most $n$, and each loop is over a finite set. Lemma 3 gives $R \subseteq Q$. A union $P \subseteq Q$ has each disjunct contained in $Q$, and Lemma 4 puts each disjunct inside one member of $R$. $\blacksquare$

**Running time.** Let $k$ be the number of views and $a$ the largest arity. An MCD is fixed by its view and by the view subgoal chosen for each subgoal in $G$, because Lemma 1 makes the unifier unique. So there are at most $d \le k (m + 1)^n$ MCDs, and the search of lines L2 to L5 has at most $n k m \cdot m^n$ leaves, each reached in $O(n^2 a)$ steps. A set of MCDs that partitions the subgoals is fixed by the partition, at most $n^n$ choices, and by the view and view subgoal of each subgoal, at most $(k m)^n$ choices, so line L7 yields at most $(n k m)^n$ sets. This is the bound of Pottinger and Halevy. The enumeration visits at most $(n k m + 1)^n$ partial covers and scans the $d$ MCDs at each one. The total time is $O(a\, n\, k\, (m + 1)^n (n k m + 1)^n)$ in combined complexity.
