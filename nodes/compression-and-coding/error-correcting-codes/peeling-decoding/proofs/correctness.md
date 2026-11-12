---
title: The peeling decoder is correct and stops at the largest stopping set
proves: [correctness]
status: full
---

**Setting.** The variables are the erased symbols, the set $E$, with true values $t[v]$; the input to PEEL is $V = E$. Each check $c$ starts with a set $C_0[c] \subseteq E$ of unknowns and the value $\mathit{val}_0[c] = \bigoplus_{v \in C_0[c]} t[v]$. A *stopping set* is a nonempty $S \subseteq V$ such that each check $c$ with $C_0[c] \cap S \ne \emptyset$ has $|C_0[c] \cap S| \ge 2$. A variable in no check forms the stopping set $\{v\}$ by this definition, since no check meets it.

**Lemma 1.** The union of two stopping sets is a stopping set. So each set $E$ contains a largest stopping set $S^\ast(E)$, the union of all stopping sets inside $E$, or $S^\ast(E) = \emptyset$ if there is none.

*Proof.* If a check meets $S_1 \cup S_2$, it meets $S_1$ or $S_2$, so it has two neighbors in that set, and both are in the union. $\square$

**Invariants.** At each test of line L3:

- (I1) For each check $c$, $C[c] = C_0[c] \setminus R$ and $\mathit{val}[c] = \bigoplus_{v \in C[c]} t[v]$, where $R$ is the set of variables with $x[v] \ne ?$.
- (I2) $x[v] = t[v]$ for each $v \in R$.
- (I3) Each check $c$ with $|C[c]| = 1$ is in $Q$.

*Proof.* At the start $R = \emptyset$, so (I1) and (I2) hold, and line L2 gives (I3). Take one pass of the loop. If line L5 skips $c$, nothing else changes, and $c$ had $|C[c]| \ne 1$, so (I3) still holds. Otherwise $C[c] = \{v\}$ and by (I1) $\mathit{val}[c] = t[v]$, so line L7 sets $x[v] = t[v]$ and (I2) holds for $R \cup \{v\}$. The variable $v$ was not in $R$, because $v \in C[c] = C_0[c] \setminus R$. Lines L8 and L9 remove $v$ from each check that contains it and XOR $t[v]$ into its value, which keeps (I1) for $R \cup \{v\}$. A check whose set changes and becomes of size 1 is added in line L10. A check whose set does not change keeps its size, and was in $Q$ before if the size is 1, unless it is $c$ itself, whose set is now empty. So (I3) holds. $\square$

**Termination and cost.** Each pass that does not skip adds a new variable to $R$, so there are at most $|V|$ such passes. Sets only shrink, so each check enters $Q$ at most once at line L2 and at most once at line L10 (the step at which its size becomes 1). So there are at most $2r$ passes in total, and lines L8 to L10 run once per edge of a resolved variable. $\square$

**Theorem.** PEEL ends, every value it writes is the true value, and the set $U = V \setminus R$ of variables left unknown is exactly $S^\ast(E)$.

*Proof.* Termination and the truth of the values are shown above. Let $U \subseteq E$ be the unknowns at the end.

$U$ is a stopping set or empty: at the end $Q = \emptyset$, so by (I3) no check has $|C[c]| = 1$. By (I1), $C[c] = C_0[c] \cap U$. So every check that meets $U$ meets it in at least two variables.

$U$ contains every stopping set $S \subseteq E$: suppose a variable of $S$ is resolved, and let $v$ be the first one, at the pass that takes check $c$. Then $C[c] = \{v\}$ and $v \in C_0[c] \cap S$, so $c$ meets $S$, and since $S$ is a stopping set, $c$ has another neighbor $v' \in C_0[c] \cap S$, $v' \ne v$. No variable of $S$ was resolved before, so $v' \notin R$, and by (I1) $v' \in C[c]$. This contradicts $C[c] = \{v\}$.

So $U$ is a stopping set (or empty) inside $E$ that contains every stopping set inside $E$, which means $U = S^\ast(E)$. $\square$

**Corollaries.**

1. *Order independence.* $S^\ast(E)$ does not depend on the order in which line L4 takes the checks, so neither does the set of resolved variables. Their values are the true values, so the output is the same for every order.
2. *Success condition.* PEEL resolves all erased variables if and only if $E$ contains no stopping set.
3. *Peeling and Gaussian elimination.* If PEEL resolves all variables, the system determines all of them, so Gaussian elimination (maximum likelihood decoding) succeeds too. The converse is false: a stopping set whose columns in $H$ are linearly independent stops PEEL but not Gaussian elimination. $\blacksquare$
