---
title: Linear resolution is sound and refutation complete, and the bounded search finds every refutation within its bound
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. Clauses are finite sets of literals. A linear derivation from $S$ with top clause $C_0$ is a sequence of centers $C_0, \ldots, C_r$ in which each $C_{i+1}$ is a factor of $C_i$, or a binary resolvent of $C_i$ with a side clause: a clause of the list $\mathrm{sides}$ of line L1, or an earlier center $C_j$, $j < i$. For ground clauses, a resolvent on the literal $L$ of $X \ni L$ and $Y \ni \neg L$ is $(X \setminus \{L\}) \cup (Y \setminus \{\neg L\})$. The **excess** of a finite set $T$ of nonempty ground clauses is $e(T) = \sum_{X \in T} (|X| - 1) \ge 0$.

**Theorem.**

1. If the search returns UNSAT, then $S$ is unsatisfiable.
2. The search stops, and it returns UNSAT if and only if some clause $T \in S$ is the top clause of a linear refutation of at most $D$ steps.
3. If $S$ is unsatisfiable and $C \in S$ is a clause such that $S \setminus \{C\}$ is satisfiable, then there is a linear refutation of $S$ with top clause $C$.
4. If $S$ is unsatisfiable, the search returns UNSAT for every large enough $D$.

## Parts 1 and 2

Every clause of $\mathrm{sides}$ and every center is a factor or a resolvent of clauses that follow from $S$, so it follows from $S$ (Lemma 1 of the proof for [Robinson's resolution principle](/robinson-resolution/)). So $\square$ appears only if $S$ is unsatisfiable.

Line L1 stops, because a factor has fewer literals than its parent, so the chains of factors are finite, and each clause has finitely many factors. A call $\mathrm{SEARCH}(\mathrm{chain}, d)$ makes at most finitely many calls with $d - 1$, so by induction on $d$ it stops, and it returns true exactly when some extension of the chain by at most $d$ moves ends in $\square$. Line L8 lists every move that the definition allows. The cut at line L7 for ground input loses nothing: a ground factor is the clause itself, and a ground resolvent has at least $|C_i| - 1$ literals, so a center with more than $d$ literals is not $\square$ after $d$ steps. Lines L2 to L4 try every top clause and every bound up to $D$.

## The ground completeness lemma

**Lemma 1.** Let $T$ be a finite unsatisfiable set of ground clauses and $C \in T$ a clause such that $T \setminus \{C\}$ is satisfiable. Then there is a linear refutation of $T$ with top clause $C$, in which every side clause is a clause of $T$ or an earlier center.

*Proof.* If $C = \square$, the chain $C$ alone is a refutation. Otherwise $\square \notin T$, because $T \setminus \{C\}$ is satisfiable. We use induction on $e(T)$.

*Replay.* We use this fact twice. Let $X_0, \ldots, X_r$ be a linear derivation from a set $T'$ in which no step resolves on the atom of a literal $K$. For each side clause $Y \in T'$ choose a clause $Y^+$ with $Y \subseteq Y^+ \subseteq Y \cup \{K\}$, and choose $X_0^+$ the same way. Repeat each step with the clauses $^+$ in place of the old ones, and with the new centers in place of the old ones. Each step is still a resolution on the same literal, and by induction $X_i \subseteq X_i^+ \subseteq X_i \cup \{K\}$, because the literal resolved upon is not $K$ or $\neg K$, and its complement is in the side clause. So the last center is $\square$ or $\{K\}$.

*Case 1: $C = \{L\}$.* Let $T' = \{X \setminus \{\neg L\} : X \in T \setminus \{C\},\ L \notin X\}$, and for each clause of $T'$ fix one clause $X$ of $T$ that gives it. If an assignment $\beta$ of the other atoms satisfies $T'$, then $\beta$ with $L$ true satisfies $T$. So $T'$ is unsatisfiable. Let $T''$ be a minimal unsatisfiable subset of $T'$. If every clause of $T''$ were a clause of $T \setminus \{C\}$ without change, then $T \setminus \{C\}$ would be unsatisfiable. So $T''$ has a clause $Y' = Y \setminus \{\neg L\}$ with $\neg L \in Y \in T$. If $Y' = \square$, the chain $\{L\}, \square$, with side clause $Y = \{\neg L\}$, is a refutation. Otherwise $\square \notin T''$, because $T''$ is minimal and $Y' \ne \square$, and $e(T'') \le e(T \setminus \{C\}) - 1 = e(T) - 1$, since the clauses of $T''$ have distinct chosen clauses of $T \setminus \{C\}$ and $Y'$ has one literal less than $Y$. By minimality $T'' \setminus \{Y'\}$ is satisfiable, so by induction $T''$ has a linear refutation with top clause $Y'$. Start the new chain with $\{L\}$, resolve it with the side clause $Y$ to get $Y'$, and then replay the refutation of $T''$ with $K = \neg L$, using the chosen clause of $T$ for each side clause of $T''$. No clause of $T''$ contains $L$ or $\neg L$, so no step resolves on this atom. The replay ends in $\square$ or $\{\neg L\}$. In the second case, resolve with the top clause $\{L\}$, an earlier center.

*Case 2: $|C| \ge 2$.* Pick $L \in C$ and let $C' = C \setminus \{L\} \ne \square$. Every model of $T \setminus \{C\}$ falsifies $C$, so it falsifies $C'$ and $L$. Hence $T_1 = (T \setminus \{C\}) \cup \{C'\}$ and $T_2 = (T \setminus \{C\}) \cup \{\{L\}\}$ are unsatisfiable, and $C', \{L\} \notin T \setminus \{C\}$. Also $T_1 \setminus \{C'\}$ and $T_2 \setminus \{\{L\}\}$ are $T \setminus \{C\}$, which is satisfiable, and $e(T_1) = e(T) - 1$ and $e(T_2) = e(T) - (|C| - 1)$ are smaller than $e(T)$. By induction, $T_1$ has a linear refutation with top clause $C'$. Replay it with $K = L$, top clause $C$, and $C$ in place of $C'$ where $C'$ is a side clause. The literal $L$ may be resolved upon in this refutation, so we check the replay fact in this case too. If a step resolves on $L$ in the center, then $X^+ \setminus \{L\} = X \setminus \{L\}$, and if it resolves on $\neg L$ in the center, then $L$ is removed from the side clause, so in both cases $X_{i+1} \subseteq X_{i+1}^+ \subseteq X_{i+1} \cup \{L\}$ still holds. The replay ends in $\square$, and we are done, or in $\{L\}$. By induction, $T_2$ has a linear refutation with top clause $\{L\}$. Append its steps to the chain, which ends with the center $\{L\}$. Its side clauses are clauses of $T \setminus \{C\} \subseteq T$, or the clause $\{L\}$, which is now an earlier center, or its own earlier centers, which are now earlier centers of the joined chain. $\square$

## Lifting

**Lemma 2.** Let $T$ be a set of ground instances of clauses of $S$, and let $G_0, \ldots, G_r$ be a linear refutation of $T$ whose side clauses are clauses of $T$ or earlier centers, with $G_0 = C\tau_0$ for a clause $C \in S$. Then there is a linear refutation of $S$ with top clause $C$, with side clauses from $\mathrm{sides}$ and earlier centers.

*Proof.* We say that a clause $X$ and a ground substitution $\theta$ **match** $G$ when $X\theta = G$ and $|X| = |G|$, so that no two literals of $X$ merge. If $X\theta = G$ but two literals merge, they have the same sign, $\theta$ unifies their atoms, and with a most general unifier $\sigma$ we get $\theta = \sigma\theta'$ on the variables of $X$ and a factor $X\sigma$ with $X\sigma\theta' = G$ and fewer literals. Repeating this gives a chain of factors that ends in a clause that matches $G$. We use this for the centers, which may be factored as moves, and for the clauses of $S$, whose iterated factors are in $\mathrm{sides}$.

We build centers $C_0, C_1, \ldots$ with $C_0 = C$, and for each $i$ a center $C_{k(i)}$ and a ground $\theta_i$ that match $G_i$. For $i = 0$, factor $C$ as above. Suppose that $C_{k(i)}$ and $\theta_i$ match $G_i$, and $G_{i+1}$ is the resolvent of $G_i$ and a side clause $H$ on a literal $A \in G_i$ with $\neg A \in H$. If $H \in T$, then $H = E\rho$ for some $E \in S$, and an iterated factor $F \in \mathrm{sides}$ of $E$ and a ground $\rho'$ match $H$. If $H = G_j$ with $j < i$, take $F = C_{k(j)}$ and $\rho' = \theta_j$. Rename $F$ apart from $C_{k(i)}$, and let $\tau$ be $\theta_i$ on $C_{k(i)}$ and $\rho'$ on $F$. As nothing merges, exactly one literal $L_1$ of $C_{k(i)}$ has $L_1\tau = A$ and exactly one literal $L_2$ of $F$ has $L_2\tau = \neg A$. Then $\tau$ unifies their atoms. With a most general unifier $\sigma$, $\tau = \sigma\theta$ for a ground $\theta$, and the binary resolvent $R = ((C_{k(i)} \setminus \{L_1\}) \cup (F \setminus \{L_2\}))\sigma$ has

$$R\theta = (G_i \setminus \{A\}) \cup (H \setminus \{\neg A\}) = G_{i+1},$$

where the first equality uses that nothing merges in $C_{k(i)}$ and $F$. Add $R$ as the next center, then factor it as above until it matches $G_{i+1}$, and let $C_{k(i+1)}$ be the last of these centers. All of these are moves of a linear derivation. At the end, $C_{k(r)}\theta_r = G_r = \square$, so $C_{k(r)} = \square$. $\square$

## Parts 3 and 4

Let $S$ be unsatisfiable and let $S \setminus \{C\}$ be satisfiable. By [Herbrand's theorem](/herbrand-theorem/), a finite set $T_0$ of ground instances of clauses of $S$ is unsatisfiable. Let $T$ be a minimal unsatisfiable subset of $T_0$. A model of $S \setminus \{C\}$, extended to all function symbols of $S$, gives a truth value to each ground atom, and it makes every ground instance of a clause of $S \setminus \{C\}$ true. So $T$ contains an instance $G_0 = C\tau_0$ of $C$, and $T \setminus \{G_0\}$ is satisfiable by minimality. Lemma 1 gives a linear refutation of $T$ with top clause $G_0$, and Lemma 2 gives a linear refutation of $S$ with top clause $C$. This proves part 3.

For part 4, $S$ is finite, so it has a minimal unsatisfiable subset $S_0$, and for any $C \in S_0$ the set $S_0 \setminus \{C\}$ is satisfiable. Part 3 gives a linear refutation of $S_0$ with top clause $C$. Its side clauses are in the list $\mathrm{sides}$ for $S$ or are earlier centers, so it is a linear refutation of $S$. Let $r$ be its length. For every $D \ge r$, part 2 shows that the search returns UNSAT. $\blacksquare$
