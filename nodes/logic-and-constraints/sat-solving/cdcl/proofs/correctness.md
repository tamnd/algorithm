---
title: CDCL is sound, its learned clauses follow from F, and it terminates under a growing restart interval or without clause deletion
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is the input formula over $x_1, \ldots, x_n$, a clause is a set of literals, and $\Delta$ is the set of learned clauses in the database. The trail $M$ is a sequence of literals, split into levels $M_0, M_1, \ldots, M_d$, where $d$ is the current decision level. Each $M_i$ with $i \ge 1$ starts with its decision literal. Every other literal $\ell$ on the trail is *implied*: it has a reason clause $R(\ell) \in F \cup \Delta$ with $\ell \in R(\ell)$, and each other literal of $R(\ell)$ is false and earlier on the trail. A learned unit clause is put on level 0, and the unit clause itself is its reason.

A clause is *unit* under $M$ when all its literals but one are false and the last one is free. We use two facts about the parts of the loop.

- **(P) Propagation is complete.** When PROPAGATE (line L4) returns NONE, no clause of $F \cup \Delta$ is false or unit under $M$. When it returns a clause $K$, all literals of $K$ are false. This is the correctness of [two watched literals](/two-watched-literals/), proved on that page.
- **(R) Reasons are never deleted.** REDUCE (line L13) deletes only learned clauses that are not the reason of a literal on the trail, and it never deletes a clause of $F$.

Fact (R) makes $R(\ell)$ available for every implied $\ell$ on the trail at all times.

## Invariants

**Lemma 1.** At each point of the run: (a) every model of $F$ satisfies every clause of $\Delta$; (b) every model of $F$ makes each literal of $M_0$ true; (c) no variable has a literal on the trail twice or both of its literals on the trail.

*Proof.* Part (c) holds because a literal is assigned only when its variable is free. Parts (a) and (b) hold at the start, when $\Delta$ and $M_0$ are empty. Each step keeps them.

- An implied literal $\ell$ at level 0 has a reason $R(\ell) \in F \cup \Delta$ whose other literals are in $M_0$ and false. A model of $F$ satisfies $R(\ell)$ by (a), and it makes each other literal of $R(\ell)$ false by (b), so it makes $\ell$ true.
- A learned clause $C$ is added at line L9. Lemma 2 below shows that every model of $F$ satisfies $C$, using (a) and (b) only for the clauses and literals that are already present. If $C$ is a unit clause, its literal goes to level 0, and (b) holds for it.
- Deletion, decisions, backjumps and restarts add no clause to $\Delta$ and no literal to $M_0$. $\square$

**Lemma 2 (analysis).** Let PROPAGATE return a false clause $K$ at level $d \ge 1$. Then ANALYZE returns a clause $C$ and a level $b < d$ such that: (i) every model of $F$ satisfies $C$, and $C$ has a resolution derivation from $F$; (ii) all literals of $C$ are false under $M$, and exactly one of them, $a$, has level $d$; (iii) $b$ is the largest level of the other literals of $C$, or 0 when $C = \{a\}$; (iv) $C$ is not in $F \cup \Delta$.

*Proof.* Let $t$ be the moment at which PROPAGATE returned NONE just before the decision of level $d$. The decision of line L15 always comes right after such a call. Since $t$, the run has made the decision of level $d$ and propagated at level $d$. It has not backjumped, so $M_0, \ldots, M_{d-1}$ are the same as at $t$, and it has not learned a clause, because the current conflict is the first since $t$.

ANALYZE sets $C_0 = K$. While $C_j$ has two or more literals of level $d$, it takes the literal $\ell$ that is latest on the trail among those with $\neg\ell \in C_j$ and level $d$, and sets $C_{j+1}$ to the resolvent of $C_j$ and $R(\ell)$ on the variable of $\ell$.

*Each $C_j$ is false under $M$ and has a resolution derivation from $F$.* This holds for $C_0 = K$ by (P), since $K \in F \cup \Delta$ and each clause of $\Delta$ was derived from $F$ when it was learned. The resolvent $C_{j+1} = (C_j \setminus \{\neg\ell\}) \cup (R(\ell) \setminus \{\ell\})$ is false, because both parts are false. It is derived from $C_j$ and $R(\ell)$ by one resolution step, and $R(\ell) \in F \cup \Delta$. Resolution is sound, so every model of $F$ satisfies each $C_j$.

*$C_0$ has a literal of level $d$.* If all literals of $K$ had level less than $d$, all of them would have been false at $t$, and $K$ was in $F \cup \Delta$ at $t$, because no clause was added since. That contradicts (P).

*The loop keeps at least one literal of level $d$, and it stops.* A step runs only when $C_j$ has two or more literals of level $d$. Then the chosen $\ell$ is not the decision of level $d$, because the decision is the earliest literal of level $d$ on the trail. So $R(\ell)$ exists. The step removes one literal of level $d$ and adds only literals that are earlier on the trail than $\ell$. So at least one literal of level $d$ remains, and the latest trail position of a level-$d$ literal in $C_j$ strictly decreases. Positions are natural numbers, so the loop stops.

When it stops, $C_j$ has exactly one literal $a$ of level $d$. ANALYZE then removes the literals of level 0 and, if minimization is on, the redundant literals. Removing a level-0 literal $q$ is a resolution step with the unit clause $\{\neg q\}$, and $\{\neg q\}$ has a derivation from $F$: resolve $R(\neg q)$ with the unit clauses of the earlier level-0 literals, by induction on the trail position. Minimization removes a literal only when resolution steps with reason clauses remove it, which is proved on the [clause minimization](/clause-minimization/) page, and it never removes $a$. So (i) and (ii) hold for the final $C$. Part (iii) is the definition of $b$, and $b < d$ because the other literals have levels below $d$.

For (iv), look at the moment $t$. Each literal of $C$ other than $a$ has level at most $b \le d - 1$, so it was false at $t$. The literal $a$ has level $d$, so it was free at $t$. So $C$ was unit at $t$, and by (P) it was not in $F \cup \Delta$ at $t$. No clause was added since $t$, so $C$ is not in $F \cup \Delta$ now. $\square$

## Soundness

**Theorem 1.** If CDCL returns SAT with the trail $M$, then $M$ is a model of $F$. If it returns UNSAT, then $F$ has no model.

*Proof.* SAT is returned at line L11, after PROPAGATE returned NONE and every variable has a value. By (P) no clause of $F$ is false. All variables have a value, so every clause of $F$ is true, and by Lemma 1(c) the trail is a consistent assignment. Deletion removes only learned clauses, so all of $F$ is checked.

UNSAT is returned at line L1 or line L6. At line L1, $F$ has the empty clause, or two opposite unit clauses, and has no model. At line L6, PROPAGATE returned a clause $K \in F \cup \Delta$ at level 0, so the negation of every literal of $K$ is in $M_0$. If $F$ had a model $\alpha$, then $\alpha$ would satisfy $K$ by Lemma 1(a), but it would make every literal of $K$ false by Lemma 1(b). So $F$ has no model. $\blacksquare$

After the backjump to $b$, the learned clause is unit with the free literal $a$. By (ii) and (iii), its other literals have levels at most $b$ and stay false, and $a$ has level $d > b$, so the backjump removes it. So line L9 assigns a literal that is free, as the pseudocode needs.

## Termination

For a trail with levels $M_0, \ldots, M_d$, let $v(M)$ be the vector $(|M_0|, |M_1|, \ldots, |M_d|)$, padded to length $n + 1$ with the value $-1$. Compare vectors in lexicographic order. Since $d \le n$ and each entry is between $-1$ and $n$, the set of possible vectors is finite. Let $N$ be its size.

**Lemma 3.** Each of these steps strictly increases $v(M)$: the assignment of one implied literal by PROPAGATE, a decision (line L15), and a backjump to level $b$ followed by the assignment of the asserting literal (lines L8 and L9).

*Proof.* An implied literal at level $d$ increases $|M_d|$ by one and changes no earlier entry. A decision changes entry $d + 1$ from $-1$ to $1$ and changes no earlier entry. A backjump to $b < d$ keeps $M_0, \ldots, M_b$, and line L9 adds $a$ to $M_b$, so entries $0$ to $b - 1$ do not change and entry $b$ grows by one. Later entries do not matter in a lexicographic comparison. $\square$

Only restarts (line L12) can decrease $v(M)$. Reduction (line L13) does not change the trail.

**Theorem 2.** CDCL terminates under each of these hypotheses.

- (a) The restart intervals are unbounded: for each bound $B$ there is a later restart interval of more than $B$ conflicts. The Luby policy with any unit has this property. Any reduction policy that keeps reason clauses is allowed.
- (b) Learned clauses are never deleted, and two restarts have at least one conflict between them. The restart policy is otherwise arbitrary.

*Proof.* Each iteration of the loop returns, or does at least one step of Lemma 3, or restarts. Between two restarts, $v(M)$ strictly increases at each step of Lemma 3, so there are fewer than $N$ such steps. Each conflict that does not return ends with the step of lines L8 and L9, so there are fewer than $N$ conflicts between two restarts.

(a) Take a restart interval of more than $N$ conflicts. The next restart needs more than $N$ conflicts after the one before it, and the run can make fewer than $N$. So it returns before that restart.

(b) By Lemma 2(iv), each learned clause is not in the database when it is learned, and with no deletion it stays there. So the learned clauses are pairwise distinct. Each is false under a consistent assignment, so it has no complementary pair of literals, and there are at most $3^n$ such clauses. So at most $3^n$ conflicts do not return. Between two of them there are fewer than $N$ steps and at most one restart. So the run is finite. $\blacksquare$

Neither hypothesis covers a run that deletes learned clauses and also uses a restart policy with bounded intervals, such as the glucose-style dynamic policy. Termination of such a run is not proved here.
