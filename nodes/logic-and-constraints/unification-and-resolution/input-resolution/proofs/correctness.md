---
title: Input resolution is sound, complete for Horn sets, incomplete in general, and stops on ground input
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page and the notation of the proof for [Robinson's resolution principle](/robinson-resolution/): clauses are finite sets of literals, $C$ subsumes $D$ when $|C| \le |D|$ and $C\rho \subseteq D$, and a tautology holds a literal and its negation. A **Horn clause** has at most one positive literal, and a **definite clause** has exactly one. A marked clause is an **input clause**.

**Theorem.** Run the loop on a finite set $S$ of clauses.

1. If it returns UNSAT, then $S$ is unsatisfiable.
2. If $S$ is a Horn set and it returns SATURATED, then $S$ is satisfiable.
3. If $S$ is an unsatisfiable Horn set and there is no limit, then it returns UNSAT.
4. A set with no input clause of one literal, and no factor of an input clause with one literal, has no input refutation. Some such sets are unsatisfiable.
5. If $S$ is ground, it stops.

Part 1 holds because factors and binary resolvents follow from their parents (Lemma 1 of the proof for Robinson's resolution principle).

## Ground Horn sets

**Lemma 1.** Let $T$ be a finite unsatisfiable set of ground Horn clauses with no tautology. Then $\square$ has a derivation from $T$ in which every step resolves the clause made by the step before, or a clause of $T$ at the first step, with a clause of $T$, and no clause is a tautology.

*Proof.* Let $D$ be the set of definite clauses of $T$. Define $M_0 = \emptyset$ and let $M_{i+1}$ be $M_i$ plus the heads $B$ of the clauses $B \vee \neg A_1 \vee \cdots \vee \neg A_k$ of $D$ with all $A_j \in M_i$. The union $M$ of the $M_i$ satisfies $D$, because a clause of $D$ whose body atoms are all in $M$ has them all in some $M_i$, and then its head is in $M_{i+1}$. For $A \in M$ let $\mathrm{st}(A)$ be the least $i$ with $A \in M_i$. As $T$ is unsatisfiable, $M$ does not satisfy $T$, so some negative clause $G_0 \in T$ is false in $M$: all its atoms are in $M$. Given a negative clause $G$ whose atoms are all in $M$, with $G \ne \square$, pick an atom $A$ of $G$. Some clause $B \vee \neg A_1 \vee \cdots \vee \neg A_k$ of $D$ with $B = A$ has all $A_j$ in $M_{\mathrm{st}(A) - 1}$. Resolve $G$ with it on $A$. The resolvent is negative, its atoms are in $M$, and its multiset of stages is the old one with one $\mathrm{st}(A)$ replaced by $k$ smaller numbers. The multiset order on natural numbers is well founded, so after finitely many steps the clause is $\square$. Negative clauses are not tautologies. $\square$

## Lifting

Let $N$ be a set of clauses and $I \subseteq N$. We call the pair **input-saturated** when every factor of a clause of $I$ is a tautology or is subsumed by a clause of $I$, every factor of a clause of $N$ is a tautology or is subsumed by a clause of $N$, and every binary resolvent of a clause of $I$ with a clause of $N$, renamed apart, is a tautology or is subsumed by a clause of $N$.

**Lemma 2.** Let $(N, I)$ be input-saturated, and let $E$ be a clause in a derivation as in Lemma 1 from a set $T$ of ground instances of clauses of $I$. Then $C\tau \subseteq E$ for some $C \in N$ and some ground $\tau$.

*Proof.* Lemma 3 of the proof for Robinson's resolution principle (no merging) uses only factors and subsumption inside one set. So for $C \in N$ and ground $\tau$ with $C\tau$ not a tautology, some $C' \in N$ and ground $\tau'$ have $C'\tau' \subseteq C\tau$ with no merging, and if $C \in I$, the same holds with $C' \in I$. Now induct on the derivation. The first clause is in $T$, so it is an instance of a clause of $I \subseteq N$. A later clause is $E = (E_1 \setminus \{A\}) \cup (E_2 \setminus \{\neg A\})$, or the same with the signs swapped, where $E_2 \in T$. By induction and no merging, $C_1\tau \subseteq E_1$ with $C_1 \in N$, and $C_2\tau \subseteq E_2$ with $C_2 \in I$, both with no merging, renamed apart. If the literal resolved upon is missing from $C_1\tau$ or from $C_2\tau$, then $C_1\tau \subseteq E$ or $C_2\tau \subseteq E$. Otherwise exactly one literal of each clause maps to it, and as in Lemma 4 of that proof the binary resolvent $R$ of $C_1$ and $C_2$ on these two literals has $R\theta \subseteq E$ for a ground $\theta$. Its parent $C_2$ is in $I$, so $R$ is a tautology or is subsumed by a clause $C_3 \in N$. $E$ is not a tautology, so $C_3\tau_3 \subseteq E$ for a ground $\tau_3$. $\square$

## The loop

The deletion chains of Lemma 6 of the proof for Robinson's resolution principle are finite here too, because line L10 stores each pair of a clause and a mark at most once, so at most two clauses of each variant class are stored. Let $A_\infty$ be the set of clauses that enter active and stay there, and $I_\infty$ its marked clauses.

**Lemma 3.** Suppose that the run never returns UNSAT and every stored clause is picked at some time. Then every stored clause is a tautology or is subsumed by a clause of $A_\infty$, every marked stored clause is a tautology or is subsumed by a clause of $I_\infty$, the pair $(A_\infty, I_\infty)$ is input-saturated, and $\square \notin A_\infty$.

*Proof.* By lines L5 and L6, a marked clause is deleted only because a marked clause of active subsumes it. So the chain of deletions that starts at a marked clause has only marked clauses, and it ends in $I_\infty$. An unmarked clause has a chain that ends in $A_\infty$. Now let $C, D \in A_\infty$ with $C$ or $D$ marked, and let $D$ be picked later, or $D = C$. When $D$ was picked, $C$ was in active, so line L9 formed every binary resolvent of $D$ and $C$, and line L8 formed every factor of $D$, marked if $D$ is marked. Each was stored, or the same clause with the same mark was stored before, so each is covered by the first two claims. Finally, $\square$ would have stopped the run at line L4. $\square$

**Parts 2 and 3.** Suppose that the run returns SATURATED, or runs forever with no limit. In both cases every stored clause is picked: in the first case passive is empty, and in the second case line L3 takes the oldest untaken clause at every $k$-th pick. Suppose $S$ is a Horn set. Factors and resolvents of Horn clauses are Horn clauses, so $I_\infty$ is a Horn set. Each clause of $S$ was stored marked, so by Lemma 3 it is a tautology or is subsumed by a clause of $I_\infty$, and therefore $S$ is satisfiable if $I_\infty$ is. Suppose $I_\infty$ is unsatisfiable. By [Herbrand's theorem](/herbrand-theorem/), a finite set of its ground instances is unsatisfiable. Delete the tautologies and call the rest $T$. Lemma 1 gives a derivation of $\square$ from $T$, and Lemma 2 for the input-saturated pair $(A_\infty, I_\infty)$ gives $C \in A_\infty$ with $C\tau \subseteq \square$, so $\square \in A_\infty$, against Lemma 3. So $I_\infty$ and $S$ are satisfiable. This proves part 2, and it proves part 3, because an unsatisfiable Horn set can then neither give SATURATED nor make the run go on forever.

## Part 4

In an input refutation the last step makes $\square$ from two clauses $E_1$ and $E_2$, resolved on $L_1 \in E_1$ and $L_2 \in E_2$ with a unifier $\sigma$. The resolvent is $((E_1 \setminus \{L_1\}) \cup (E_2 \setminus \{L_2\}))\sigma$, and an instance of a nonempty clause is nonempty. So $\square$ needs $E_1 = \{L_1\}$ and $E_2 = \{L_2\}$. One of $E_1$ and $E_2$ is an input clause or a factor of one, so that clause has one literal. The set $\{p \vee q,\ \neg p \vee q,\ p \vee \neg q,\ \neg p \vee \neg q\}$ has no such clause, because its clauses are ground with two literals each, and a ground clause is its only factor. Each of the four assignments of $p$ and $q$ makes one of its clauses false, so it is unsatisfiable.

## Part 5

If $S$ is ground, every stored clause is a set of literals over the atoms of $S$. There are finitely many such sets, line L10 stores each with each mark at most once, and each pass takes a stored clause that was not taken before. So the loop stops. $\blacksquare$
