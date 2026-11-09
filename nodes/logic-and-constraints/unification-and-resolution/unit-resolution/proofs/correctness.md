---
title: Unit resolution is sound, complete for Horn sets, incomplete in general, and stops on ground input
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page and the notation of the proof for [Robinson's resolution principle](/robinson-resolution/): clauses are finite sets of literals, $C$ subsumes $D$ when $|C| \le |D|$ and $C\rho \subseteq D$, and a tautology holds a literal and its negation. A **Horn clause** has at most one positive literal. We call a set $N$ **unit-saturated** when every factor of a clause of $N$, and every binary resolvent of two clauses of $N$ one of which has one literal, is a tautology or is subsumed by a clause of $N$.

**Theorem.** Run the loop on a finite set $S$ of clauses.

1. If it returns UNSAT, then $S$ is unsatisfiable.
2. If $S$ is a set of Horn clauses and it returns SATURATED, then $S$ is satisfiable.
3. If $S$ is an unsatisfiable set of Horn clauses and there is no limit, then it returns UNSAT.
4. Some unsatisfiable sets that are not Horn make it return SATURATED.
5. If $S$ is ground, it stops.

## Part 1

A unit resolvent is a binary resolvent, and a binary resolvent and a factor follow from their parents (Lemma 1 of the proof for Robinson's resolution principle). So every stored clause follows from $S$, and $\square$ is stored only if $S$ is unsatisfiable.

## Ground Horn sets

**Lemma 1.** Let $T$ be a finite unsatisfiable set of ground Horn clauses with no tautology. Then $\square$ has a derivation from $T$ by ground unit resolution in which no clause is a tautology.

*Proof.* Let $U$ be the set of clauses that can be derived from $T$ by ground unit resolution. A unit resolvent of $\{L\}$ and $D$ is $D \setminus \{\neg L\}$, a subset of $D$, so no clause of $U$ is a tautology and every clause of $U$ is a Horn clause. Let $M$ be the set of atoms $A$ with $\{A\} \in U$. Suppose $\square \notin U$. We show that $M$, read as the set of true atoms, satisfies $T$. Take $C \in T$ and write $C = \{\neg A_1, \ldots, \neg A_k\} \cup H$, where $H$ is empty or one positive literal. If some $A_i \notin M$, then $\neg A_i$ is true and $C$ is true. Otherwise every $\{A_i\}$ is in $U$. Resolve $C$ with $\{A_1\}, \ldots, \{A_k\}$ in turn; each step removes one $\neg A_i$, so the result $H$ is in $U$. As $\square \notin U$, $H = \{B\}$ for an atom $B$, so $B \in M$ and $C$ is true. So $T$ is satisfiable, which is a contradiction. Hence $\square \in U$. $\square$

## Lifting

**Lemma 2.** Let $N$ be unit-saturated and let $E$ be a clause in a derivation from ground instances of clauses of $N$ by ground unit resolution, with no tautology in the derivation. Then $C\tau \subseteq E$ for some $C \in N$ and some ground $\tau$.

*Proof.* Lemma 3 of the proof for Robinson's resolution principle uses only factors, so it holds for $N$: if $C\tau$ is not a tautology, then some $C' \in N$ and ground $\tau'$ have $C'\tau' \subseteq C\tau$ and $|C'\tau'| = |C'|$ (no merging). Now induct on the derivation. An input clause is an instance $C\tau$. Let $E$ be the resolvent of $E_1 \ni A$ and $E_2 \ni \neg A$, where $E_1 = \{A\}$ or $E_2 = \{\neg A\}$, and take $C_1\tau \subseteq E_1$ and $C_2\tau \subseteq E_2$ with no merging and with $C_1$, $C_2$ renamed apart. If $A \notin C_1\tau$ or $\neg A \notin C_2\tau$, then $C_1\tau \subseteq E$ or $C_2\tau \subseteq E$. Otherwise, if $E_1 = \{A\}$, then $C_1\tau = \{A\}$, and with no merging $C_1$ has one literal. In the same way, if $E_2 = \{\neg A\}$, then $C_2$ has one literal. Let $L_1 \in C_1$ and $L_2 \in C_2$ be the only literals with $L_1\tau = A$ and $L_2\tau = \neg A$, let $\sigma$ be a most general unifier of their atoms, and write $\tau = \sigma\theta$. The binary resolvent $R$ of $C_1$ and $C_2$ on $L_1$ and $L_2$ is a unit resolvent, and $R\theta = (C_1\tau \setminus \{A\}) \cup (C_2\tau \setminus \{\neg A\}) \subseteq E$. $E$ is not a tautology, so $R$ is not one, and a clause $C_3 \in N$ subsumes $R$. Then $C_3\tau_3 \subseteq E$ for a ground extension $\tau_3$ of the composed substitution. $\square$

**Lemma 3.** A unit-saturated set $N$ of Horn clauses with $\square \notin N$ is satisfiable.

*Proof.* If $N$ is unsatisfiable, [Herbrand's theorem](/herbrand-theorem/) gives a finite unsatisfiable set of ground instances. Instances of Horn clauses are Horn clauses. Delete the tautologies, apply Lemma 1, and apply Lemma 2 to the clause $\square$ at the end. This gives $C \in N$ with $C\tau \subseteq \square$, so $C = \square$, which is a contradiction. $\square$

## Parts 2 and 3

Lines L3, L5, L6 and L10 are the same as lines L3, L5, L6 and L9 of the loop of Robinson's resolution principle. So Lemmas 5 and 6 of that proof hold with the same proofs, and every clause that is in active at some time is subsumed by a clause of the set $A_\infty$ of clauses that enter active and stay there. Suppose that the run never returns UNSAT and that every stored clause is picked at some time. As in Lemma 7 of that proof, every stored clause is a tautology or is subsumed by a clause of $A_\infty$. Take $C, D \in A_\infty$ where one of them has one literal, and let $D$ be the one picked later, or $D = C$. When $D$ was picked, $C$ was in active, so lines L8 and L9 formed every binary resolvent of $D$ and $C$, and line L7 formed every factor of $D$. So $A_\infty$ is unit-saturated, and $\square \notin A_\infty$.

Factors and resolvents of Horn clauses are Horn clauses: a factor or a resolvent does not have more positive literals than its parents together, and in a resolvent of two Horn clauses the positive literal that is resolved away is the only positive literal of its parent. So if $S$ is a Horn set, $A_\infty$ is a Horn set, and Lemma 3 gives a model of $A_\infty$. Each clause of $S$ is a tautology or is subsumed by a clause of $A_\infty$, so the model satisfies $S$.

For part 2, passive is empty at line L12, so every stored clause was picked, and $S$ is satisfiable. For part 3, if the run does not return UNSAT, it returns SATURATED or runs forever. In the second case line L3 is fair, because it takes the oldest untaken clause at every $k$-th pick, so every stored clause is picked. In both cases $S$ is satisfiable, which is a contradiction.

## Part 4

Let $S = \{p \vee q,\ \neg p \vee q,\ p \vee \neg q,\ \neg p \vee \neg q\}$. Each of the four assignments of $p$ and $q$ makes one clause false, so $S$ is unsatisfiable. No clause of $S$ has one literal, and the factors of a ground clause are the clause itself, so line L9 never forms a resolvent and line L7 adds nothing new. After four picks passive is empty, and the loop returns SATURATED.

## Part 5

If $S$ is ground, a unit resolvent of $\{L\}$ and $D$ is $D \setminus \{\neg L\}$. Induction on the run shows that every stored clause is a subset of a clause of $S$. There are finitely many such subsets, line L10 stores each clause at most once, and each pass takes a stored clause that was not taken before. So the loop stops. $\blacksquare$
