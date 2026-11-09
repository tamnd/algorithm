---
title: CDCL(T) is sound and terminates without clause deletion
proves: [correctness, termination]
status: full
---

We prove the claims for the loop of the pseudocode, with a theory solver that meets (T1), (T2) and (T3) of the page. Let $F_0$ be the input clause set over $n$ variables, $F$ the clause set during the run, and $\mathrm{lev}(l)$ the decision level of a literal $l$ of the trail. For a set of literals or clauses $S$, $S \models_T \varphi$ means every $T$-model of $S$ is a model of $\varphi$. A plain Boolean variable is an atom that the theory does not restrict.

## Invariants

At the start of each pass of the loop:

- **(A)** The trail has no repeated variable. Levels do not go down along the trail. For each $k \ge 1$ the first literal of level $k$ is a decision, and only these literals are decisions.
- **(B)** $F_0 \subseteq F$, and $F_0 \models_T C$ for each clause $C$ of $F$.
- **(C)** Each literal $l$ of the trail that is not a decision has a reason $R_l$. The clause $R_l$ contains $l$, its other literals are false and come before $l$ on the trail, and $R_l$ is in $F$ or is $T$-valid.

**Consequence (D).** Each literal $l$ of the trail satisfies $F_0 \cup \Delta_l \models_T l$, where $\Delta_l$ is the set of decisions of levels at most $\mathrm{lev}(l)$. By induction along the trail: a decision is in $\Delta_l$. For another literal, each other literal $\neg l_i$ of $R_l$ comes before $l$, so it has level at most $\mathrm{lev}(l)$, and by induction $F_0 \cup \Delta_l \models_T \neg l_i$. By (B) or by $T$-validity, $F_0 \models_T R_l$. So $F_0 \cup \Delta_l \models_T l$. In particular each literal of level 0 is a $T$-consequence of $F_0$.

**Unit propagation.** It puts the last free literal $l$ of a clause $R$ of $F$ on the trail at the current level, with reason $R$. The other literals of $R$ are false and already on the trail, so (C) holds, and (A) holds because $l$ was free.

**Theory propagation (line L2).** The theory solver puts a free literal $l$ on the trail with reason $l \vee \neg \eta$. By (T3), $\eta$ is a set of literals of the trail and $\eta \models_T l$, so the reason is $T$-valid and its other literals come before $l$. In the implementation, $\eta$ for an equality $s = t$ is the explanation of $s = t$ by the congruence closure of the equalities of the trail. For a disequality $s \ne t$ it is $\{u \ne x\}$ with the explanations of $s = u$ and $t = x$. Both are correct by the explanation theorem of [congruence closure](/congruence-closure/).

**Decisions (line L12).** A decision opens a new level and needs no reason.

## Conflict analysis

Line L4 has a clause $C$ whose literals are all false. If $C$ is in $F$, then $F_0 \models_T C$ by (B). If it comes from the theory solver, it is $\neg \eta$ with $\eta$ $T$-unsatisfiable by (T1), so it is $T$-valid. In both cases $F_0 \models_T C$.

**UNSAT is correct (line L5).** If every literal of $C$ has level 0, then by (D), $F_0 \models_T \neg C$. With $F_0 \models_T C$, $F_0$ has no $T$-model. $\square$

Otherwise let $c \ge 1$ be the highest level of a literal of $C$. Line L6 removes the levels above $c$. The literals of $C$ stay false, and (A), (C) and (D) still hold for the shorter trail.

**The analysis is well defined.** The procedure keeps a clause $E$, first $C$. A literal of $E$ of level 0 is dropped. Let $k$ be the number of literals of $E$ of level $c$. At first $k \ge 1$. While $k > 1$, take the literal $p$ of the trail that is last among the negations of the literals of $E$ of level $c$. It is not the decision of level $c$, because that decision is the first literal of level $c$ and at least one other literal of level $c$ is after it. So $p$ has a reason $R_p$, and $E$ is replaced by the resolvent of $E$ and $R_p$ on $p$. The new literals of level $c$ come from $R_p$, so they are before $p$ on the trail. So the position of the last literal of level $c$ in $E$ moves back each time, and the loop stops with $k = 1$. Let $\neg p$ be the only literal of level $c$ of the final clause $D$.

**$D$ is a $T$-consequence of $F_0$.** Each $R_p$ is a $T$-consequence of $F_0$, by (B) or by $T$-validity. A resolvent of two $T$-consequences is one too. A dropped literal $q$ of level 0 is false, so $\neg q$ is on the trail at level 0 and $F_0 \models_T \neg q$ by (D). From $F_0 \models_T D \vee q$ and $F_0 \models_T \neg q$ we get $F_0 \models_T D$. So adding $D$ to $F$ at line L9 keeps (B).

**$D$ is asserting.** Each literal of $D$ is false: the literals of $C$ are false, and the literals of each reason other than its own literal are false. $\neg p$ is the only literal of level $c$. Let $b$ be the highest level of the other literals, or 0 if there is none, so $b < c$. After line L8 removes the levels above $b$, the other literals of $D$ are still false and the variable of $p$ is free. So $\neg p$ is the only free literal of $D$, and line L9 puts it on the trail with reason $D$, which is in $F$. This keeps (A) and (C).

**Restarts (line L10).** Going back to level 0 keeps (A), (B) and (C), since it only removes literals.

## SAT is correct

Line L11 is reached only after a pass in which unit propagation found no false clause and the theory solver found no conflict and no new literal. The trail is total. Each clause of $F \supseteq F_0$ is true or false under a total assignment, and none is false, so all clauses of $F_0$ are true. The theory solver got all theory literals of the total trail and found no conflict, so by (T2) they have a $T$-model $\mathcal{A}$. For EUF, congruence closure is complete for conjunctions of literals: its term model satisfies each equality of the trail, and each disequality of the trail holds in it because the check found its two sides in different classes. Give the plain variables their values from the trail. Then each atom of $F_0$ has its value from the trail in $\mathcal{A}$, and $\mathcal{A}$ satisfies $F_0$. $\square$

## Each learned clause is new

**Lemma.** When line L9 adds $D$, $D$ is not in $F$.

*Proof.* Let $d$ be the decision of level $c$ on the trail after line L6, and let $t_0$ be the moment just before $d$ was made. From $t_0$ until now, $d$ stayed on the trail, so no backtrack went below level $c$ and no restart happened. New literals are put on the trail only at the current level, which is at least $c$ after $t_0$. So the literals of levels below $c$ are the same at $t_0$ and now.

At $t_0$ the loop was at line L12, so unit propagation was at a fixpoint: no clause of $F$ was false or had exactly one free literal. At $t_0$ the literals of $D$ other than $\neg p$ were false, since they have levels below $c$, and the variable of $p$ was free, since $p$ has level $c$. So $D$ had exactly one free literal, and $D$ was not in $F$ at $t_0$.

Suppose $D$ was added to $F$ after $t_0$, at an earlier pass of line L9, with a backjump level $b'$ and an asserted literal $\alpha$. Since $d$ stayed on the trail, $b' \ge c$. At that time $\alpha$ was free, so $\alpha$ is not one of the literals of $D$ of level below $c$, which were already assigned at $t_0$ and stayed so. So $\alpha = \neg p$. The other literals of $D$ then had levels below $c$, so their highest level, $b'$, is below $c$. This contradicts $b' \ge c$. $\square$

## Termination

Nothing is removed from $F$, so by the lemma the learned clauses are pairwise different. Each one has no repeated variable and no two complementary literals, because all its literals are false at the same time. There are $3^n$ such clauses over $n$ variables, so line L9 runs at most $3^n$ times, and there are at most $3^n + 1$ conflicts.

Between two conflicts the trail only grows. Each pass of the loop that does not stop and finds no conflict puts at least one literal on the trail: by unit propagation, by theory propagation at line L3, or by the decision of line L12. Unit propagation itself stops, because each step adds a literal. The trail has at most $n$ literals by (A). So between two conflicts there are at most $n + 1$ passes, and the run has $O(3^n n)$ passes. Each run ends at line L5 or line L11, and both answers are correct. $\blacksquare$

## Remarks

The proof does not use the restart limit of line L10. It is needed when a solver also deletes learned clauses: then the lemma no longer bounds the number of conflicts, and Nieuwenhuis, Oliveras and Tinelli require that the intervals between restarts grow, so that between two restarts the run is finite and in the limit there is a run without restarts. The proof also does not need that the theory solver propagates every entailed literal. If it propagates none, the run is still correct, and theory conflicts at line L2 do all the work.
