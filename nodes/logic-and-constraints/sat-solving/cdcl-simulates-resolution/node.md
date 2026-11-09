---
tag: NAVAK9
kind: theorem
slug: cdcl-simulates-resolution
name: CDCL simulates resolution
aliases:
- CDCL polynomially simulates general resolution
- clause learning p-simulates resolution
- Pipatsrisawat-Darwiche theorem
area: logic-and-constraints/sat-solving
level: research
summary: CDCL with restarts, no clause deletion and good decisions refutes every formula in a number of conflicts polynomial in its shortest resolution refutation.
prereqs: [cdcl, clause-learning, refutation, unit-propagation, restarts]
see_also: [haken-resolution-lower-bound, drat-proof, first-uip, implication-graph, dpll, clause-database-reduction]
sources:
  - paper: doi:10.1016/j.artint.2010.10.002
    title: Knot Pipatsrisawat and Adnan Darwiche, On the power of clause-learning SAT solvers as resolution engines, Artificial Intelligence 175(2), 2011, 512-525
    locator: 1-empowering clauses and the proof that CDCL with any asserting learning scheme, restarts and an ideal decision strategy p-simulates general resolution
  - paper: doi:10.1613/jair.3152
    title: Albert Atserias, Johannes Klaus Fichte and Marc Thurley, Clause-learning algorithms with many restarts and bounded-width resolution, Journal of Artificial Intelligence Research 40, 2011, 353-373
    locator: Section 2 (the solver model), Lemmas 1, 2, 5, 10, 14 and 15 (rounds, absorption, beneficial rounds), Theorems 13 and 17 and Corollary 18 (bounds with random decisions)
  - paper: "Paul Beame, Henry Kautz and Ashish Sabharwal, Towards understanding and harnessing the potential of clause learning, Journal of Artificial Intelligence Research 22, 2004, 319-351"
    title: Towards understanding and harnessing the potential of clause learning
    locator: the translation of CDCL runs into resolution proofs, and the first simulation results for modified formulas
  - paper: "Michael Alekhnovich and Alexander Razborov, Resolution is not automatizable unless W[P] is tractable, SIAM Journal on Computing 38(4), 2008"
    title: Resolution is not automatizable unless W[P] is tractable
    locator: the main theorem on the automatizability of resolution
  - paper: "Albert Atserias and Moritz Müller, Automating resolution is NP-hard, Journal of the ACM 67(5), 2020"
    title: Automating resolution is NP-hard
    locator: the main theorem, that finding resolution refutations of size polynomial in the shortest one is NP-hard
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 7 (Buss and Nordström, Proof Complexity and SAT Solving), the sections on CDCL as a proof system and on the role of restarts
---

[CDCL](/cdcl/) solvers look for a model, but when the formula is unsatisfiable their learned clauses form a resolution [refutation](/refutation/). So a CDCL run can never be shorter than the shortest resolution refutation, up to a polynomial factor. This theorem gives the converse: if the decisions are well chosen, the solver restarts after each conflict and never deletes a learned clause, then CDCL with any asserting learning scheme, such as [first UIP](/first-uip/), finds a refutation with a number of conflicts polynomial in the size of the shortest resolution refutation. Pipatsrisawat and Darwiche proved it in 2009, with the journal version in 2011. Atserias, Fichte and Thurley proved it independently in the same years for refutations of bounded width, with random decisions in place of good ones. Together with the old direction, the theorem makes CDCL in this model and resolution equally strong as proof systems.

## Statement

**Notation.** $F$ is a [CNF](/conjunctive-normal-form/) formula with $n$ variables, $m$ clauses and $|F|$ literal occurrences. A resolution refutation $\pi = C_1, \ldots, C_s$ of $F$ is a list of clauses that ends with the empty clause, where each $C_i$ is a clause of $F$ or the resolvent of two earlier clauses. We may assume that no $C_i$ is a tautology. Its length is $s$ and its width $w$ is the largest number of literals in a clause of $\pi$.

**The solver model.** This is the model of Atserias, Fichte and Thurley (Section 2). The solver keeps a clause set $D$, at first $D = F$, and a list $S$ of assignments, each marked as a decision or as implied.

1. If $S$ makes a clause of $D$ false, there is a conflict. The solver learns a clause by an *asserting* learning scheme and adds it to $D$. If it is the empty clause, the answer is UNSAT. Otherwise the solver *restarts*: it clears $S$.
2. Otherwise, if a clause of $D$ is unit under $S$, the solver sets its free literal (unit propagation).
3. Otherwise, if all variables are set, the answer is SAT. If not, the solver adds a *decision* $x = a$ for some free $x$.

A learning scheme takes the false clause and resolves it, from the end of $S$ backward, with the reason clauses of implied literals, as in the [implication graph](/implication-graph/). It is asserting if the clause it learns has exactly one literal of the highest decision level. First UIP is asserting. The Decision scheme, which resolves until only negations of decision literals remain, is also asserting. Learned clauses are never deleted. A conflict at decision level 0 gives the empty clause.

**Theorem (Pipatsrisawat and Darwiche 2011; Atserias, Fichte and Thurley 2011).** Let $F$ have a resolution refutation of length $s$ and width $w$. Then the solver model has a run on $F$, with suitable decisions, that learns the empty clause after at most $s$ conflicts when it uses the Decision scheme, and after at most $s \cdot w \cdot n + 1 \le s n^2 + 1$ conflicts with any asserting scheme. A restart follows each conflict, and between two conflicts the solver makes at most $n$ assignments. So the whole run takes time polynomial in $s$, $n$ and $|F|$.

**Theorem (random decisions; Atserias, Fichte and Thurley 2011, Theorem 17 and Corollary 18).** Suppose every decision picks a free variable and a value uniformly at random. If $F$ has a resolution refutation of width $w$ and length $s$, then with probability at least $1/2$ the solver with any asserting scheme learns the empty clause within $4ws \ln(4wns)\, n^{w+1}$ conflicts and restarts. Since the length can be taken at most $4n^w$, this is at most $16w(w+1)\ln(16wn)\, n^{2w+1}$. With the Decision scheme the bound is $4s\ln(4s)\, n^{w}$ (their Theorem 13).

## In plain words

When a solver finds a conflict, it learns a new clause and starts again. A resolution proof is a list of clauses where each one follows from two earlier ones. The idea of the proof is to make the solver "know" the clauses of the resolution proof one after the other. Knowing a clause here does not mean that it is stored. It means that whenever the solver has made all literals of the clause false but one, propagation makes the last one true.

If the solver knows the two parents of a step but not the result, there is a way to make decisions that walks into a conflict which teaches it the result. Repeat this for every step of the proof. At the end the solver knows a variable and its negation, so propagation alone gives a conflict and the empty clause.

## Proof

We prove the first theorem in full, following Atserias, Fichte and Thurley. The second theorem uses the same lemmas and a probability bound, and we only state it.

**Rounds.** Fix a clause set $D$. A *round* started with $D$ is a run of steps 2 and 3 from the empty assignment, until a clause is false (the round is *conclusive*) or no clause is unit (the round is *inconclusive*). So an inconclusive round leaves no unit clause: if it makes all literals of a clause of $D$ false but one, it makes that one true. A round $R'$ *subsumes* $R$ if every assignment of $R$ is also made in $R'$. A round *branches in* $C$ if all its decision variables are variables of $C$. Two rounds *agree on* $C$ if they give the same value, or no value, to each variable of $C$.

**Lemma 1.** Let $D \subseteq D'$, let $R'$ be an inconclusive round started with $D'$, and let $R$ be a round started with $D$ that branches in $C$ and agrees with $R'$ on $C$. Then $R'$ subsumes $R$.

*Proof.* By induction over the assignments of $R$. A decision of $R$ is on a variable of $C$, so $R'$ makes it, because they agree on $C$. An implied assignment of $R$ comes from a clause of $D \subseteq D'$ that is unit under earlier assignments, which $R'$ also makes by induction. As $R'$ is inconclusive, it leaves no unit clause, so it makes this assignment too. $\square$

**Lemma 2.** Let $D \subseteq D'$ and let $R'$ be an inconclusive round started with $D'$. For every clause $C$ there is an inconclusive round $R$ started with $D$ that branches in $C$, agrees with $R'$ on $C$, and is subsumed by $R'$.

*Proof.* Run from the empty assignment with $D$: propagate while a clause is unit, and otherwise decide, in a fixed order, the next variable of $C$ that $R'$ sets and is still free, with the value of $R'$. Stop when no such variable is left. Each decision is an assignment of $R'$ on $C$, so by Lemma 1, applied to each prefix, $R'$ subsumes the run. So the run makes no clause of $D$ false, because $R'$ makes no clause of $D'$ false. It is an inconclusive round that sets every variable of $C$ that $R'$ sets, and it sets no other variable of $C$, because $R'$ subsumes it. $\square$

**Absorption.** $D$ *absorbs* a non-empty clause $A$ at a literal $l \in A$ if every inconclusive round started with $D$ that makes $A \setminus \{l\}$ false sets $l$ true. $D$ absorbs $A$ if it absorbs $A$ at each of its literals. Pipatsrisawat and Darwiche use the dual notion: an implied clause is *1-empowering* via $l$ exactly when it is not absorbed at $l$ (Atserias, Fichte and Thurley, Lemma 7).

**Lemma 3 (monotonicity).** (a) Every clause of $D$ is absorbed by $D$. (b) If $D$ absorbs $A$ and $A \subseteq B$, then $D$ absorbs $B$. (c) If $D$ absorbs $A$ and $D \subseteq E$, then $E$ absorbs $A$.

*Proof.* (a) An inconclusive round leaves no unit clause. (b) Let $R$ be inconclusive, started with $D$, and let it make $B \setminus \{l\}$ false. If $l \notin A$, then $R$ makes all of $A$ false, but absorption of $A$ at any of its literals forbids that, so there is no such $R$. If $l \in A$, then $R$ makes $A \setminus \{l\}$ false and so sets $l$ true. (c) Let $R'$ be inconclusive, started with $E$, and let it make $A \setminus \{l\}$ false. Lemma 2 with $C = A \setminus \{l\}$ gives an inconclusive round $R$ started with $D$ that also makes $A \setminus \{l\}$ false. So $R$ sets $l$ true, and $R'$, which subsumes $R$, does too. $\square$

**Lemma 4 (a beneficial round).** Let $D$ absorb $A$ and $B$, and let $C = \mathrm{Res}(A, B)$ on the variable $y$ be non-empty and not absorbed by $D$. Then there are a literal $l \in C$ and an inconclusive round $R$ started with $D$ such that $R$ branches in $C \setminus \{l\}$, makes $C \setminus \{l\}$ false, leaves the variable of $l$ free, and adding the decision $\neg l$ to $R$ and propagating gives a conflict.

*Proof.* As $C$ is not absorbed, there are $l \in C$ and an inconclusive round $R'$ started with $D$ that makes $C \setminus \{l\}$ false and does not set $l$ true. $R'$ does not set $l$ false either. Otherwise it makes all of $C = (A \setminus \{y\}) \cup (B \setminus \{\neg y\})$ false, and absorption of $A$ at $y$ and of $B$ at $\neg y$ makes it set $y$ true and false. Let $R$ be the round of Lemma 2 for $C \setminus \{l\}$ with $D' = D$. It makes $C \setminus \{l\}$ false, branches in it, and leaves $l$ free because $R'$ does. Now add the decision $\neg l$ and propagate. If this ended inconclusive, the new round would make $A \setminus \{y\}$ and $B \setminus \{\neg y\}$ false and, by absorption, set $y$ both true and false. So it ends with a conflict. $\square$

**Proof of the theorem for the Decision scheme.** Let $\pi = C_1, \ldots, C_s$ with $C_s$ empty, and let the last step resolve $(y)$ and $(\neg y)$. We go through $C_1, \ldots, C_{s-1}$ and keep the invariant that the current $D$ absorbs every clause handled so far. A clause of $F$ is absorbed by Lemma 3(a) and (c). Let $C_i$ be the resolvent of earlier $A$ and $B$, which are absorbed. If $C_i$ is absorbed, do nothing. Otherwise make the solver follow the round $R$ of Lemma 4: its decisions are the negations of literals of $C_i \setminus \{l\}$ and then $\neg l$, and the round ends with a conflict. The Decision scheme learns a clause whose literals are negations of decision literals, so it learns some $C' \subseteq C_i$. Then the solver restarts. Now $C' \in D$, so $D$ absorbs $C_i$ by Lemma 3(a) and (b), and it still absorbs all earlier clauses by Lemma 3(c). This costs one conflict per resolvent.

At the end $D$ absorbs $(y)$ and $(\neg y)$. Then every inconclusive round sets $y$ both true and false, which is impossible, so no inconclusive round exists. In particular, the round with no decisions, which is pure unit propagation on $D$, ends with a conflict at level 0, and the solver learns the empty clause. In all, at most $s - 1$ conflicts for the resolvents and one more at the end. $\blacksquare$

**Any asserting scheme.** An asserting clause need not lie inside $C_i$, so one beneficial round is not enough. For $l \in C$ let $u_l$ be the number of variables that an inconclusive round started with $D$, of the kind in Lemma 4 for $l$, leaves free, or 0 if there is no such round. By Lemma 1 all such rounds make the same assignments, so $u_l$ is well defined. Put $u_C(D) = \sum_l u_l \le w n$. Atserias, Fichte and Thurley show that $u_C$ never grows when $D$ grows (their Lemma 14), and that it drops by at least one when the solver runs into a conflict after such a round. The asserting clause is unit at the end of the round, so after it is added the same decisions force one more variable (their Lemma 15). When $u_C(D) = 0$ there is no round as in Lemma 4, so $C$ is absorbed. Hence $w n$ conflicts per resolvent suffice, and the total is at most $(s - 1) w n + 1$.

**The random case.** A random round follows a fixed beneficial round with probability at least $\frac{(w-1)!}{2^w n^w} \ge \frac{1}{4 n^w}$, since it must pick the $w - 1$ literals of $C \setminus \{l\}$ in some order and then $\neg l$, each with the right value. A union bound over the $s$ steps of the refutation gives the stated bounds.

## Consequences

- **CDCL and resolution are p-equivalent.** Each learned clause has a trivial resolution derivation from the clauses in $D$, with at most $n$ steps. So a CDCL run with $c$ conflicts gives a resolution refutation of length at most $c \cdot n$ plus $m$ (Beame, Kautz and Sabharwal). With the theorem, the two systems have the same shortest proofs up to a polynomial.
- **Lower bounds carry over.** Every resolution lower bound is a lower bound on the number of conflicts in this model, whatever the decisions. By [Haken's theorem](/haken-resolution-lower-bound/), every run on the pigeonhole formula with $n + 1$ pigeons and $n$ holes has $2^{\Omega(n)}$ conflicts.
- **Bounded width is easy with random decisions.** Unsatisfiable 2-CNF formulas have refutations of width 2, so the random solver refutes them with polynomially many conflicts. Atserias, Fichte and Thurley note that formulas of treewidth at most $k$ have refutations of width at most $k + 1$, which gives a running time of $O(k^2 \log(kn)\, n^{2k+3})$ for them.
- **Proof logging is complete.** A [DRAT proof](/drat-proof/) from such a run has polynomial length whenever a short resolution refutation exists.

## Tightness

- **The decisions must be good.** The theorem says that a short run exists, not that a deterministic heuristic finds it. Alekhnovich and Razborov showed that resolution is not automatizable unless W[P] is tractable, and Atserias and Müller showed that finding a resolution refutation of size polynomial in the shortest one is NP-hard. So unless P = NP, no polynomial-time decision strategy realizes the simulation for all formulas.
- **Restarts.** The proof uses a restart after every conflict. Whether CDCL without restarts also p-simulates resolution is open. Without restarts, CDCL corresponds to restricted systems, such as pool resolution, which the Handbook chapter of Buss and Nordström discusses.
- **No deletion.** The proof needs all learned clauses. Practical solvers delete most of them ([clause database reduction](/clause-database-reduction/)). Atserias, Fichte and Thurley point to Nordström's space lower bounds as a sign that some assumption of this kind is needed.
- **Width of learned clauses.** The learned clauses can be wider than the clauses of $\pi$. Ben-Sasson and Johannsen (2010) showed that a solver that learns only short clauses is weaker, as quoted by Atserias, Fichte and Thurley.
- **The random bound is exponential in $w$.** The factor $n^{w}$ comes from the small chance that random decisions follow one beneficial round. So the second theorem gives polynomial bounds only for refutations of constant width, while the first one needs no bound on the width.

## History

Beame, Kautz and Sabharwal (2004) showed that CDCL runs are resolution proofs, and that a CDCL solver with restarts p-simulates resolution on formulas changed by a preprocessing step that depends on the proof. Hertel, Bacchus, Pitassi and Van Gelder (2008) gave an effective simulation, also with a change of the formula. Pipatsrisawat and Darwiche (CP 2009; Artificial Intelligence 2011) removed the change: CDCL with any asserting scheme, restarts and an ideal decision strategy p-simulates general resolution on the original formula. Their key notion is the 1-empowering clause. Atserias, Fichte and Thurley (SAT 2009; JAIR 2011) found the dual notion of absorption and showed that random decisions suffice for refutations of bounded width. Their journal version notes that the first proof of Pipatsrisawat and Darwiche had an error that was corrected later.

## References
