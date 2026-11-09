---
title: The given-clause resolution prover is sound, refutation complete, and stops on ground input
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. A clause is a finite set of literals, and its variables are read as universally quantified. Two clauses that differ only by a renaming of variables are variants, and line L9 stores at most one clause of each variant class. A clause $C$ subsumes $D$ when $|C| \le |D|$ and $C\rho \subseteq D$ for some substitution $\rho$. Subsumption is transitive: from $C\rho \subseteq D$ and $D\rho' \subseteq E$ we get $C\rho\rho' \subseteq E$. A tautology is a clause that holds a literal and its negation. We use [Herbrand's theorem](/herbrand-theorem/) in this form: a set $N$ of clauses is unsatisfiable if and only if some finite set of ground instances of clauses of $N$, with terms from the Herbrand universe of $N$, is unsatisfiable when each ground atom is read as a propositional variable.

We say that a set $N$ of clauses is **saturated** when every factor of a clause of $N$, and every binary resolvent of two clauses of $N$ renamed apart, is a tautology or is subsumed by a clause of $N$.

## Soundness of the rules

**Lemma 1.** Every factor and every binary resolvent is a logical consequence of its parents.

*Proof.* A clause implies each of its instances, and a factor $C\sigma$ is an instance of $C$. For a resolvent, let $\sigma$ be a unifier of the atoms $L$ and $L'$, with parents $C \vee L$ and $D \vee \neg L'$. In a model $M$ of both parents, take any assignment of the variables. The instances $(C \vee L)\sigma$ and $(D \vee \neg L')\sigma$ are true. The atom $L\sigma = L'\sigma$ is true or false. If it is true, $D\sigma$ is true. If it is false, $C\sigma$ is true. So $(C \vee D)\sigma$ is true. $\square$

So every stored clause follows from $S$, and if line L4 returns UNSAT, then $\square$ follows from $S$, and $S$ is unsatisfiable.

## Ground completeness

**Lemma 2.** Let $T$ be a finite unsatisfiable set of ground clauses, none of them a tautology. Then $\square$ has a derivation from $T$ by ground resolution in which no clause is a tautology.

*Proof.* Induction on the number $k$ of atoms in $T$. If $k = 0$, then $T \subseteq \{\square\}$, and $T$ is unsatisfiable, so $\square \in T$. If $k > 0$ and $\square \notin T$, pick an atom $A$ of $T$. Let $T_A$ be the set of clauses $C \setminus \{\neg A\}$ for $C \in T$ with $A \notin C$. If an assignment $\beta$ of the other atoms satisfies $T_A$, then $\beta$ with $A$ true satisfies $T$. So $T_A$ is unsatisfiable, it has fewer atoms, and it has no tautology. By the induction hypothesis, $T_A$ has a derivation of $\square$ with no tautology. Replace each input clause of this derivation by the clause of $T$ that it came from, and repeat the same resolution steps. No step resolves on $A$, so each derived clause becomes the old one, or the old one plus $\neg A$. No clause holds $A$, so no clause becomes a tautology. The last clause is $\square$ or $\{\neg A\}$. In the same way, from $T_{\neg A}$ we derive $\square$ or $\{A\}$. If neither derivation ends in $\square$, resolve $\{A\}$ with $\{\neg A\}$. $\square$

## Saturated sets

**Lemma 3 (no merging).** Let $N$ be saturated. Let $C \in N$ and let $\tau$ be a ground substitution such that $C\tau$ is not a tautology. Then there are $C' \in N$ and a ground $\tau'$ such that $C'\tau' \subseteq C\tau$ and $|C'\tau'| = |C'|$.

*Proof.* Induction on $|C|$. If $|C\tau| = |C|$, take $C' = C$. Otherwise two literals $L_1 \ne L_2$ of $C$ have $L_1\tau = L_2\tau$, so they have the same sign and $\tau$ unifies their atoms. Let $\sigma$ be a most general unifier of these atoms. Then $\tau = \sigma\theta$ on the variables of $C$ for some ground $\theta$, by the definition of a most general unifier ([mgu existence theorem](/mgu-existence-theorem/)). The factor $F = C\sigma$ has $F\theta = C\tau$ and $|F| < |C|$. $F$ is not a tautology, because $F\theta$ is not one. As $N$ is saturated, some $C'' \in N$ has $C''\rho \subseteq F$ and $|C''| \le |F| < |C|$. Extend $\rho\theta$ to a ground substitution $\theta''$ on the variables of $C''$. Then $C''\theta'' \subseteq F\theta = C\tau$, and it is not a tautology. The induction hypothesis for $C''$ gives $C'$ and $\tau'$ with $C'\tau' \subseteq C''\theta'' \subseteq C\tau$. $\square$

**Lemma 4.** Let $N$ be saturated and let $E$ be a clause in a derivation from ground instances of clauses of $N$ by ground resolution, with no tautology in the derivation. Then $C\tau \subseteq E$ for some $C \in N$ and some ground $\tau$.

*Proof.* Induction on the derivation. An input clause is an instance $C\tau$, so it holds. Let $E = (E_1 \setminus \{A\}) \cup (E_2 \setminus \{\neg A\})$, and by the induction hypothesis and Lemma 3 (the clauses $E_1, E_2$ are not tautologies), let $C_1\tau_1 \subseteq E_1$ and $C_2\tau_2 \subseteq E_2$ with $C_1, C_2 \in N$ and no merging. If $A \notin C_1\tau_1$, then $C_1\tau_1 \subseteq E$, and we are done. The same holds if $\neg A \notin C_2\tau_2$. Otherwise, rename $C_2$ apart from $C_1$ and let $\tau$ be $\tau_1$ on $C_1$ and $\tau_2$ on $C_2$. With no merging, exactly one literal $L_1 \in C_1$ has $L_1\tau = A$, and exactly one literal $L_2 \in C_2$ has $L_2\tau = \neg A$. The substitution $\tau$ unifies the atoms of $L_1$ and $L_2$. Let $\sigma$ be their most general unifier, with $\tau = \sigma\theta$. The binary resolvent $R = ((C_1 \setminus \{L_1\}) \cup (C_2 \setminus \{L_2\}))\sigma$ has

$$R\theta = (C_1\tau \setminus \{A\}) \cup (C_2\tau \setminus \{\neg A\}) \subseteq E,$$

where the equality uses that there is no merging. $E$ is not a tautology, so $R$ is not one. As $N$ is saturated, some $C_3 \in N$ has $C_3\rho \subseteq R$. Extend $\rho\theta$ to a ground $\tau_3$. Then $C_3\tau_3 \subseteq R\theta \subseteq E$. $\square$

**Theorem A.** A saturated set $N$ with $\square \notin N$ is satisfiable.

*Proof.* Suppose $N$ is unsatisfiable. By Herbrand's theorem, a finite set of ground instances of clauses of $N$ is unsatisfiable. Delete its tautologies; they are true under each assignment, so the rest $T$ is still unsatisfiable. Lemma 2 gives a derivation of $\square$ from $T$ with no tautology, and Lemma 4 gives $C \in N$ and $\tau$ with $C\tau \subseteq \square$. Then $C = \square$, which is a contradiction. $\square$

## The loop

**Lemma 5.** At most finitely many clauses that are not variants of each other subsume a given clause $D$.

*Proof.* If $C$ subsumes $D$, then $|C| \le |D|$, and the term $\mathrm{t}(C)$ that lists the literals of $C$ in some order generalizes a term that lists at most $|D|$ literals of $D$, with repeats. There are finitely many such lists. A term $t$ has finitely many generalizations up to a renaming of variables, because a generalization is fixed by the set of positions of $t$ at which it has a variable and by which of these positions carry the same variable. $\square$

**Lemma 6.** Consider any run of the loop. Every clause that is in active at some time is subsumed by a clause that stays in active for the rest of the run.

*Proof.* Let $D_0$ be in active. If line L6 removes it, the given clause $D_1$ that removes it subsumes $D_0$ and enters active. If $D_1$ is removed later, the clause $D_2$ that removes it subsumes $D_1$, and so on. By transitivity each $D_i$ subsumes $D_0$. The $D_i$ entered active at different picks, so they are stored clauses with different numbers, and line L9 never stores two variants. By Lemma 5 the chain is finite, and its last clause stays in active. $\square$

Let $A_\infty$ be the set of clauses that enter active and stay there for the rest of the run.

**Lemma 7.** Suppose the run never returns UNSAT, and every stored clause is picked at some time. Then $A_\infty$ is saturated, every stored clause is a tautology or is subsumed by a clause of $A_\infty$, and $\square \notin A_\infty$.

*Proof.* A picked clause $G$ is deleted at line L5 as a tautology, or because a clause of active subsumes it, or it enters active. In the last two cases, Lemma 6 and transitivity give a clause of $A_\infty$ that subsumes $G$. A clause that line L9 does not store is a variant of a stored clause, and a variant is subsumed by it. Now let $C, D \in A_\infty$, and let $D$ be picked after $C$, or $D = C$. When $D$ was picked, $C$ was in active, because a clause of $A_\infty$ is never removed and line L9 never stores it again. So line L8 formed every factor of $D$ and every binary resolvent of $D$ and $C$, and line L9 stored each of them or a variant. By the first part, each is a tautology or subsumed by a clause of $A_\infty$. The factors of $C$ were formed when $C$ was picked. Finally, if $\square$ were in $A_\infty$, line L4 would have returned UNSAT when it was picked. $\square$

**Theorem B (correctness).** Run the loop on a set $S$ of clauses.

1. If it returns UNSAT, then $S$ is unsatisfiable.
2. If it returns SATURATED, then $S$ is satisfiable.
3. If $S$ is unsatisfiable and there is no limit, then it returns UNSAT.

*Proof.* Part 1 is Lemma 1. For part 2, passive is empty at line L11, so every stored clause was picked and $A_\infty$ is the final active set. By Lemma 7 and Theorem A, $A_\infty$ has a model $M$. Each clause of $S$ was stored at line L1. It is a tautology, which is true in $M$, or $C\rho \subseteq D$ for some $C \in A_\infty$, and then $D$ follows from $C$, so $D$ is true in $M$. So $M$ is a model of $S$.

For part 3, suppose that the run does not return UNSAT. With no limit, line L10 never returns, so the run returns SATURATED or runs forever. If it returns SATURATED, then $S$ is satisfiable by part 2. If it runs forever, every stored clause is picked at some time: line L3 takes the oldest untaken clause at every $k$-th pick, and only finitely many clauses are older than a given one. Lemma 7 and Theorem A make $A_\infty$ satisfiable, and its model satisfies $S$ as in part 2. In both cases $S$ is satisfiable. $\square$

## Termination on ground input

**Theorem C.** If every clause of $S$ is ground and $n$ atoms occur in $S$, the loop stops. It stores at most $4^n$ clauses, and at most $3^n$ passes reach line L8.

*Proof.* A factor of a ground clause is the clause itself, and a resolvent of ground clauses is a ground clause whose atoms occur in its parents. So every stored clause is a set of literals over the $n$ atoms of $S$. In such a set each atom is absent, positive, negative, or both, so there are at most $4^n$ of them. A clause in which some atom is both positive and negative is a tautology, so at most $3^n$ of them are not tautologies. Line L9 stores each clause at most once, so at most $4^n$ clauses are stored. Each pass of the loop takes one stored clause that was not taken before, so there are at most $4^n$ passes and the loop stops. Line L5 deletes a tautology before line L8, so only the passes on clauses that are not tautologies reach line L8, and there are at most $3^n$ of them. $\blacksquare$
