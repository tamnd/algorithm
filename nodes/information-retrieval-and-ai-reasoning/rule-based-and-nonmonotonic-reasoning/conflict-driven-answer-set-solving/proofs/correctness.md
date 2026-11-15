---
title: Conflict-driven nogood learning returns exactly the answer sets
proves: [correctness]
status: full
---

Let $P$ be a finite ground normal program over a set $A$ of atoms, with rules $h \leftarrow B$ and constraints $\leftarrow B$. For a body $B = b_1, \ldots, b_m, \mathit{not}\ c_1, \ldots, \mathit{not}\ c_k$ we write $B^+ = \{b_1, \ldots, b_m\}$ and $B^- = \{c_1, \ldots, c_k\}$. The solver has one variable for each atom and one for each distinct body. A *literal* is $\mathbf{T}v$ or $\mathbf{F}v$. An *assignment* is a consistent set of literals; it is *total* if it assigns every variable. A *nogood* is a set of literals; an assignment *violates* it if it contains all of its literals. A total assignment is a *solution* of a set of nogoods if it violates none of them. A set $X \subseteq A$ *induces* the total assignment $A_X$ that makes an atom true exactly when it is in $X$ and a body true exactly when $X$ satisfies it.

## The nogoods (Gebser, Kaufmann and Schaub 2012)

For each body $\beta$: $\delta(\beta) = \{\mathbf{F}\beta\} \cup \{\mathbf{T}a : a \in \beta^+\} \cup \{\mathbf{F}a : a \in \beta^-\}$, and the nogoods $\{\mathbf{T}\beta, \mathbf{F}a\}$ for $a \in \beta^+$ and $\{\mathbf{T}\beta, \mathbf{T}a\}$ for $a \in \beta^-$. For each atom $p$ with bodies $\beta_1, \ldots, \beta_k$: $\{\mathbf{F}p, \mathbf{T}\beta_i\}$ for each $i$, and $\delta(p) = \{\mathbf{T}p, \mathbf{F}\beta_1, \ldots, \mathbf{F}\beta_k\}$. For each constraint with body $\beta$: $\{\mathbf{T}\beta\}$. These nogoods form $\Delta_P$. Their solutions are exactly the assignments $A_X$ such that $X$ is a model of the Clark completion of $P$ and of the constraints.

For $U \subseteq A$, the *external bodies* $EB(U)$ are the bodies $\beta$ of rules with head in $U$ such that $\beta^+ \cap U = \emptyset$. The *loop nogood* of $p \in U$ is $\lambda(p, U) = \{\mathbf{T}p\} \cup \{\mathbf{F}\beta : \beta \in EB(U)\}$, and $\Lambda_P$ is the set of all loop nogoods for all nonempty $U \subseteq A$.

**Theorem A (Gebser, Kaufmann and Schaub 2012).** $X \subseteq A$ is an answer set of $P$ if and only if $A_X$ is a solution of $\Delta_P \cup \Lambda_P$.

The tests check Theorem A by brute force on random programs. The proof below uses only the "if" direction for one kind of assignment, and proves it directly in Lemma 3.

## Unfounded sets

The solver computes, for the current assignment $\mathcal{A}$, the set $D$ of atoms that can still be derived. $D$ is the least set such that if a body $\beta$ is not false in $\mathcal{A}$ and $\beta^+ \subseteq D$, then each head $p$ of $\beta$ that is not false is in $D$. The set $U$ that it returns is the set of atoms that are not false and not in $D$.

**Lemma 1.** Suppose that unit propagation over a set of nogoods that contains $\Delta_P$ has reached a fixpoint without a violated nogood. Then every body in $EB(U)$ is false in $\mathcal{A}$.

*Proof.* Let $\beta \in EB(U)$ be a body of $p \in U$, and suppose that $\beta$ is not false. If some $a \in \beta^+$ were false, the nogood $\{\mathbf{T}\beta, \mathbf{F}a\}$ would be unit, and unit propagation would have made $\beta$ false. So every atom of $\beta^+$ is not false. Since $\beta^+ \cap U = \emptyset$, every atom of $\beta^+$ is in $D$. Then $p$, which is not false, is in $D$ by the definition of $D$. This contradicts $p \in U$. $\square$

So when $U \neq \emptyset$, every new loop nogood $\lambda(p, U)$ with $p \in U$ is violated, if $p$ is true, or unit, if $p$ is open. In both cases the next round of unit propagation makes progress. Also, at least one of these nogoods is new. If all of them were present already, then each would be violated or unit at the fixpoint, which a fixpoint without conflict excludes. There are finitely many loop nogoods, so the loop in PROPAGATE ends.

**Lemma 2.** If $P$ is tight (its positive dependency graph has no cycle), the solver adds no loop nogood, and every solution of $\Delta_P$ is of the form $A_X$ for an answer set $X$.

*Proof.* The code skips the unfounded set check on tight programs. The second claim is Fages' theorem: for a tight program, the models of the completion are the answer sets. $\square$

**Lemma 3.** Let $\mathcal{A}$ be a total assignment that violates no nogood of $\Delta_P$ and for which $U = \emptyset$. Let $X$ be its set of true atoms. Then $X$ is an answer set of $P$ and satisfies no constraint body.

*Proof.* Since $\mathcal{A}$ is total and violates no body nogood, a body is true exactly when $X$ satisfies it. Let $L$ be the least model of the reduct $P^X$. A rule of $P^X$ is $h \leftarrow \beta^+$ for a rule $h \leftarrow \beta$ with $\beta^- \cap X = \emptyset$. If $\beta^+ \subseteq X$, then $\beta$ is true, and the nogood $\{\mathbf{F}h, \mathbf{T}\beta\}$ gives $h \in X$. So $X$ is a model of $P^X$ and $L \subseteq X$. Under a total assignment, $D$ is the least set closed under the rules $h \leftarrow \beta^+$ with $\beta$ true and $h$ true. Each of these is a rule of $P^X$, so $D \subseteq L$. $U = \emptyset$ means $X \subseteq D$. So $X \subseteq D \subseteq L \subseteq X$, and $X = L$. The nogood $\{\mathbf{T}\beta\}$ of each constraint is not violated, so $\beta$ is false. $\square$

For a tight program, Lemma 2 covers the same case: a total solution of $\Delta_P$ gives an answer set.

## Learned nogoods

A nogood $\delta$ is *implied* by a set $\Gamma$ of nogoods if every solution of $\Gamma$ is a solution of $\Gamma \cup \{\delta\}$.

**Lemma 4.** Let $\Gamma = \Delta_P \cup \Lambda_P \cup \Theta$, where $\Theta$ is the set of blocking nogoods of the run. Each nogood in the solver's database is in $\Gamma$ or implied by $\Gamma$.

*Proof.* The nogoods of $\Delta_P$, the loop nogoods and the blocking nogoods are in $\Gamma$. A learned nogood is built by ANALYZE. It starts from a violated nogood of the database and repeatedly replaces a literal $\sigma$ by the other literals of the nogood $\varepsilon$ that implied $\sigma$ in unit propagation. That nogood holds the complement $\bar\sigma$. The new set is the resolvent $(\delta \setminus \{\sigma\}) \cup (\varepsilon \setminus \{\bar\sigma\})$. Let $\mathcal{B}$ be a solution of $\Gamma$ that contains the resolvent. $\mathcal{B}$ is total, so it contains $\sigma$ or $\bar\sigma$. In the first case it contains $\delta$, and in the second case it contains $\varepsilon$. Both are implied by $\Gamma$ by induction, so this is impossible. $\square$

**Lemma 5 (analysis ends with an asserting nogood).** Let the conflict have its largest decision level $k \geq 1$. ANALYZE ends, and its result has exactly one literal of level $k$ and its other literals at levels at most $j < k$, where $j$ is the level returned.

*Proof.* While the set holds two or more literals of level $k$, the one assigned last is not the decision literal of level $k$, because that literal is the first one at level $k$ on the trail. So it has a reason, and the step replaces it by literals assigned earlier. The positions on the trail of the literals at level $k$ decrease, so the loop ends. It ends exactly when one literal of level $k$ is left. $j$ is the largest level among the others, so $j < k$. $\square$

After the backjump to level $j$, the learned nogood has all literals but one true, so unit propagation assigns the complement of its literal of level $k$.

## The theorem

**Theorem.** `solve` returns an answer set of $P$ that is not blocked, if there is one, and None otherwise. `answer_sets` returns every answer set exactly once.

*Proof.* *Termination.* Between two decisions, PROPAGATE ends by Lemma 1 and the finite number of loop nogoods. By Lemma 5 each conflict at level $k \geq 1$ is followed by a backjump and the assignment of an asserted literal at a level below $k$. This is the conflict-driven clause learning scheme, and the standard argument for its termination applies: the vector of the numbers of literals at the levels $0, 1, \ldots$ grows in the lexicographic order after each conflict, and it is bounded.

*Soundness.* The search returns only when the assignment is total and PROPAGATE found no violated nogood and, for a program that is not tight, $U = \emptyset$. By Lemma 3, or by Lemma 2 for a tight program, the set of true atoms is an answer set. It violates no blocking nogood, so it is not one of the answer sets found before.

*Completeness.* Let $X$ be an answer set that is not blocked. By Theorem A, $A_X$ is a solution of $\Delta_P \cup \Lambda_P$, and it is a solution of $\Theta$. By Lemma 4, it violates no nogood of the database. The search returns None only after a conflict at level $0$. All literals at level $0$ follow from the database by unit propagation, so every solution of the database contains them. The conflict nogood would then be violated by $A_X$, which is impossible. So the search does not return None, and by termination it returns an answer set.

*Enumeration.* Each call of `solve` in `answer_sets` adds a blocking nogood for each answer set found before. By soundness and completeness, each call returns a new answer set until none is left. $\square$

## Running time

Let $n$ be the number of atoms and $s$ the size of the program, the number of rules plus the number of body literals. There are at most $n + s$ variables and $O(s)$ nogoods in $\Delta_P$. The unfounded set computation takes $O(n \cdot s)$ time with repeated scans, or $O(s)$ with counters. The number of conflicts is not bounded by a polynomial, since the problem is NP-complete. The code finds unit nogoods by scanning all nogoods, which costs $O(g)$ per pass for $g$ the total size of the database; solvers such as clasp use watched literals instead.

## What the tests check

On 300 random programs with at most 6 atoms, and on 150 random programs with constraints, `answer_sets` gives exactly the answer sets found by brute force with the reduct. For 60 programs the tests build $\Lambda_P$ for every nonempty $U$ from the definition, independent of the solver code, and check Theorem A: the solutions of $\Delta_P \cup \Lambda_P$ are the answer sets. On 300 larger random programs, every answer set that a run does not block violates none of the learned nogoods and none of the loop nogoods of that run, so these nogoods are consistent with Lemma 4. The run learns more than 100 nogoods in total. A last test checks that each loop nogood has one true atom literal and false body literals.
