---
title: Stålmarck's algorithm returns UNSAT only for unsatisfiable formulas, returns a model for satisfiable ones, and stops at a level k of at most n
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a CNF formula over $x_1, \ldots, x_n$ with $m$ clauses, $T$ is its set of AND triplets $x \leftrightarrow (y \wedge z)$, and the nodes are $\top$, the variables and the new nodes $g$ of the clause chains. A literal is a node or its negation, with $\neg\top = \bot$. Let $V \subseteq \{x_1, \ldots, x_n\}$ be the set of variables that occur in $F$; the others do not occur in $T$, and the algorithm sets them to false.

**Valuations.** An assignment $\beta$ of the variables in $V$ extends in one way to all nodes: $\beta(\top) = 1$, and $\beta(x) = \beta(y) \wedge \beta(z)$ for each triplet, in the order in which the triplets were built, since $y$ and $z$ are older nodes. We call this the *extension* of $\beta$. By construction, the last node $g$ of the chain of a clause $C$ has $\beta(g) = 1$ exactly when every literal of $C$ is false, so $\beta$ satisfies $C$ exactly when $\beta(\neg g) = 1$. For a unit clause $(\ell)$ the root literal is $\ell$ itself.

**Relations.** $E$ is an equivalence relation on literals that is closed under negation. A valuation $\beta$ *respects* $E$ when $\beta(a) = \beta(b)$ for each pair $a \equiv b$ in $E$. $E$ is *contradictory* when it contains $\top \equiv \bot$; no valuation respects such an $E$. If $E \subseteq E'$, every valuation that respects $E'$ respects $E$. Let $\mathrm{Mod}(E)$ be the set of assignments of $V$ whose extension respects $E$. Let $E_F$ be the relation built at line L1. By the remark on clause roots, $\mathrm{Mod}(E_F)$ is exactly the set of models of $F$ (restricted to $V$).

The number of classes of a relation is at most $t$, the number of nodes, and a strict refinement in the order $E \subsetneq E'$ lowers the number of classes of nodes or turns a consistent relation into a contradictory one.

## Soundness

**Lemma 1 (simple rules).** If the extension of $\beta$ respects $E$, and $E'$ is $E$ plus the conclusion of one of the rules R1 to R6 whose condition holds in $E$, then the extension of $\beta$ respects $E'$.

*Proof.* Fix a triplet with $\beta(x) = \beta(y) \wedge \beta(z)$, and use that $\beta$ respects the condition.

1. R1. If $\beta(x) = 1$, then $\beta(y) = \beta(z) = 1$.
2. R2. If $\beta(y) = 0$ or $\beta(z) = 0$, then $\beta(x) = 0$.
3. R3. If $\beta(y) = 1$, then $\beta(x) = \beta(z)$; the case $\beta(z) = 1$ is the same with $y$ and $z$ swapped.
4. R4. If $\beta(y) = \beta(z)$, then $\beta(x) = \beta(y) \wedge \beta(y) = \beta(y)$.
5. R5. If $\beta(y) \ne \beta(z)$, one of them is 0, so $\beta(x) = 0$.
6. R6. If $\beta(x) \ne \beta(y)$, then $\beta(x) = 0$ and $\beta(y) = 1$, because $\beta(x) = 1$ forces $\beta(y) = 1$. Then $0 = 1 \wedge \beta(z)$ gives $\beta(z) = 0$. The case $x \equiv \neg z$ is the same with $y$ and $z$ swapped.

The closure of $E'$ under transitivity and negation adds only pairs that every valuation respecting the new pair and $E$ respects too. $\square$

**Lemma 2 (saturation is sound).** For every $k \ge 0$ and every relation $E$, the output $E^*$ of SATURATE$(T, E, k)$ contains $E$ and satisfies $\mathrm{Mod}(E^*) = \mathrm{Mod}(E)$.

*Proof.* By induction on $k$, and inside each $k$ on the steps of the loop L7 to L13. The relation only grows, so $E \subseteq E^*$ and $\mathrm{Mod}(E^*) \subseteq \mathrm{Mod}(E)$. For the other inclusion we show that each step keeps every $\beta \in \mathrm{Mod}(E)$.

1. Line L8 adds conclusions of simple rules, and Lemma 1 keeps $\beta$.
2. Lines L11 and L12, with $k \ge 1$. Let $\beta \in \mathrm{Mod}(E)$, where $E$ is the current relation. If $\beta(v) = 1$, then $\beta \in \mathrm{Mod}(E \cup \{v \equiv \top\})$, and by induction on $k$ the extension of $\beta$ respects $E_1$. If $\beta(v) = 0$, it respects $E_0$ in the same way. So it respects $E_1$ or $E_0$, and in both cases it respects every pair that lies in both, that is, $E_1 \cap E_0$. If $E_1$ is contradictory, then no $\beta$ has $\beta(v) = 1$, every $\beta$ respects $E_0$, and the rule sets $E \leftarrow E_0$, which is $E_1 \cap E_0$ when a contradictory relation is read as the set of all pairs. The case of a contradictory $E_0$ is the same.

Every step keeps $\mathrm{Mod}$, so $\mathrm{Mod}(E^*) = \mathrm{Mod}(E)$. $\square$

**Corollary 3.** If line L4 returns UNSAT, then $F$ is unsatisfiable.

*Proof.* Each value of $E$ in the loop of line L2 is a saturation of the previous one, so by Lemma 2, $\mathrm{Mod}(E) = \mathrm{Mod}(E_F)$, the set of models of $F$. If $E$ is contradictory, $\mathrm{Mod}(E) = \emptyset$. $\square$

## Models

**Lemma 4 (fixed relations).** Let $E$ be consistent and closed under the simple rules, and let $E$ fix every variable of $V$. Let $\beta$ be the assignment that $E$ fixes. Then the extension of $\beta$ respects $E$, and $\beta$ is a model of $F$ if $E \supseteq E_F$.

*Proof.* First, every node is fixed to its value under $\beta$. This holds for $\top$ and for the variables. For a triplet $x \leftrightarrow (y \wedge z)$ with $y$ and $z$ fixed to their values: if one of them is fixed to $\bot$, R2 adds $x \equiv \bot$; otherwise both are fixed to $\top$, and R3 adds $x \equiv z \equiv \top$. Since $E$ is closed, these pairs are in $E$, and by induction over the order of the triplets every node $u$ has $u \equiv \top$ or $u \equiv \bot$ in $E$ according to $\beta(u)$. Now let $a \equiv b$ be in $E$. Both $a$ and $b$ are fixed, $a$ to $\beta(a)$ and $b$ to $\beta(b)$. If $\beta(a) \ne \beta(b)$, then $\top \equiv a \equiv b \equiv \bot$ or the reverse lies in $E$, and $E$ is contradictory, which it is not. So $\beta$ respects $E$. If $E \supseteq E_F$, then $\beta \in \mathrm{Mod}(E_F)$, so $\beta$ is a model of $F$. $\square$

Call a relation *$k$-saturated* when it is a consistent output of SATURATE at level $k$. A 0-saturated relation is closed under the simple rules (line L9). For $k \ge 1$, a $k$-saturated relation $E$ was returned at line L13, so it is closed under the simple rules (line L8 ran at the start of the last pass), and in the last pass, for each class of unfixed variables, line L11 ran on one variable $v$ of the class, at least one of $E_1, E_0$ was consistent, and $E_1 \cap E_0 = E$. Let $\mathrm{free}(E)$ be the number of classes of $E$ that contain an unfixed variable of $V$.

**Lemma 5 (completeness).** If $E$ is $k$-saturated and $\mathrm{free}(E) \le k$, then $\mathrm{Mod}(E) \ne \emptyset$.

*Proof.* By induction on $k$.

1. If $\mathrm{free}(E) = 0$, $E$ fixes every variable of $V$ and is closed under the simple rules, so Lemma 4 gives an assignment in $\mathrm{Mod}(E)$. This covers $k = 0$.
2. Let $k \ge 1$ and $\mathrm{free}(E) \ge 1$. Take a free class and the variable $v$ of it that line L11 used in the last pass. One of $E_1, E_0$ is consistent; say $E_1$, the other case being the same. $E_1$ is a consistent output of SATURATE at level $k - 1$, so it is $(k-1)$-saturated.
3. $E_1 \supseteq E \cup \{v \equiv \top\}$. Each free class of $E_1$ is a union of classes of $E$, and it holds an unfixed variable, which was unfixed in $E$ too. The class of $v$ is fixed in $E_1$. So $\mathrm{free}(E_1) \le \mathrm{free}(E) - 1 \le k - 1$.
4. By induction, $\mathrm{Mod}(E_1) \ne \emptyset$, and $\mathrm{Mod}(E_1) \subseteq \mathrm{Mod}(E)$ because $E \subseteq E_1$. $\square$

**Lemma 6 (EXTEND).** Let $E \supseteq E_F$ be $k$-saturated. If EXTEND$(T, E, k)$ returns an assignment, it is a model of $F$. If $\mathrm{free}(E) \le k$, it returns an assignment.

*Proof.* Each step of EXTEND replaces $E$ by a consistent output $E'$ of SATURATE at level $k$, so $E'$ is $k$-saturated and contains $E$. A variable fixed in $E$ stays fixed, and the variable $v$ of the step becomes fixed, so the loop ends after at most $|V|$ steps. If it reaches line 6, the final relation is consistent, closed under the simple rules, fixes every variable and contains $E_F$, and Lemma 4 shows that the returned assignment is a model of $F$.

Now let $\mathrm{free}(E) \le k$. We show that the invariant "$E$ is $k$-saturated and $\mathrm{free}(E) \le k$" holds before each step, and that line 4 never returns FAIL. By Lemma 5, $\mathrm{Mod}(E) \ne \emptyset$. If SATURATE$(T, E \cup \{v \equiv \top\}, k)$ is consistent, it is the new $E$. Otherwise, by Lemma 2, $\mathrm{Mod}(E \cup \{v \equiv \top\}) = \emptyset$, so every $\beta \in \mathrm{Mod}(E)$ has $\beta(v) = 0$, and $\mathrm{Mod}(E \cup \{v \equiv \bot\}) = \mathrm{Mod}(E) \ne \emptyset$. By Lemma 2 again, SATURATE$(T, E \cup \{v \equiv \bot\}, k)$ is consistent, so line 4 does not return. The new relation is $k$-saturated, and its free count is at most the old one, so the invariant holds. $\square$

## Correctness and termination

**Theorem.** STALMARCK$(F)$ stops. It returns UNSAT if and only if $F$ is unsatisfiable, and otherwise it returns a model of $F$. The final level $k$ is at most $|V| \le n$.

*Proof.*

1. **Each call of SATURATE stops.** By induction on $k$. For $k = 0$, line L8 stops because each pass of the rules that changes $E$ lowers the number of classes or makes $E$ contradictory, which stops at line L9. For $k \ge 1$, each recursive call stops by induction, and each pass of L10 to L12 that adds something to $E$ lowers the number of classes or makes $E$ contradictory. So there are at most $t + 1$ passes before line L13 or line L9 returns.
2. **EXTEND stops**, by the proof of Lemma 6.
3. **The loop of line L2 stops by $k = |V|$.** At level $k$ the relation after line L3 contains $E_F$. If it is contradictory, line L4 returns. Otherwise it is $k$-saturated, and $\mathrm{free}(E) \le |V|$. At $k = |V|$ this gives $\mathrm{free}(E) \le k$, and Lemma 6 shows that line L5 returns a model.
4. **The answers are right.** By Corollary 3, UNSAT is returned only for an unsatisfiable $F$. By Lemma 6, a returned assignment is a model of $F$ on $V$, and the variables outside $V$ do not occur in $F$, so any values for them keep it a model. Since the loop always returns one of the two answers, a satisfiable $F$ gets a model, and an unsatisfiable $F$, which has no model, gets UNSAT. $\blacksquare$

The bound $k \le |V|$ is crude. The level at which line L4 fires for an unsatisfiable $F$ is the hardness of $F$ for this version of the method, and line L5 often succeeds at a much lower level than $|V|$, as in the example of the page, which is decided at $k = 0$.
