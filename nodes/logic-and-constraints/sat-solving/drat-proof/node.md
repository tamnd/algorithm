---
tag: 9RG6K9
kind: definition
slug: drat-proof
name: DRAT proof format
aliases:
- DRAT
- Deletion Resolution Asymmetric Tautology
- DRAT proof
area: logic-and-constraints/sat-solving
level: advanced
summary: Clausal proof of unsatisfiability as a list of added and deleted clauses; each added clause must be RUP or RAT, so every step keeps a satisfiable formula satisfiable.
prereqs: [unit-propagation, clause-learning, refutation]
see_also: [lrat-proof, cdcl, blocked-clause-elimination, bounded-variable-elimination, unsat-core, clause-database-reduction, cdcl-simulates-resolution]
sources:
  - paper: doi:10.1007/978-3-319-09284-3_31
    title: Nathan Wetzler, Marijn J. H. Heule and Warren A. Hunt Jr., DRAT-trim, Efficient checking and trimming using expressive clausal proofs, SAT 2014, LNCS 8561, 422-429
    locator: the DRAT format with the pivot as the first literal, deletion lines, and backward checking with core-first propagation
  - paper: doi:10.1007/978-3-642-31365-3_28
    title: Matti Järvisalo, Marijn J. H. Heule and Armin Biere, Inprocessing rules, IJCAR 2012, LNCS 7364, 355-370
    locator: asymmetric tautologies and resolution asymmetric tautologies (RAT), and the proof that adding or removing a RAT clause keeps satisfiability
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 15 (Heule, Proofs of Unsatisfiability), the sections on clausal proofs, RUP, RAT, DRAT and proof checking
  - paper: "Evguenii I. Goldberg and Yakov Novikov, Verification of proofs of unsatisfiability for CNF formulas, DATE 2003, pages 886 to 891"
    title: Verification of proofs of unsatisfiability for CNF formulas
    locator: proofs as lists of conflict clauses checked by unit propagation (the RUP idea)
  - paper: doi:10.1007/978-3-319-40970-2_15
    title: Marijn J. H. Heule, Oliver Kullmann and Victor W. Marek, Solving and verifying the Boolean Pythagorean triples problem via cube-and-conquer, SAT 2016, LNCS 9710, 228-245
    locator: the DRAT proof of about 200 terabytes and its checking
  - paper: "Adrián Rebola-Pardo and Armin Biere, Two flavors of DRAT, Pragmatics of SAT 2018"
    title: Two flavors of DRAT
    locator: specified DRAT versus operational DRAT, where checkers ignore deletions of unit clauses
---

A DRAT proof shows that a [CNF](/conjunctive-normal-form/) formula $F$ is unsatisfiable. It is a list of steps. Each step adds a clause or deletes a clause, and the proof ends when the empty clause is added. Each added clause must pass a test that uses only [unit propagation](/unit-propagation/): it is a reverse unit propagation (RUP) clause, or a resolution asymmetric tautology (RAT) on its first literal. Both tests keep a satisfiable formula satisfiable, so a checker that accepts a proof of the empty clause has shown that $F$ has no model. The name stands for Deletion, Resolution Asymmetric Tautology. A [CDCL](/cdcl/) solver writes DRAT almost for free: it prints each [learned clause](/clause-learning/) and each clause it deletes. Preprocessing and inprocessing steps that do not keep equivalence, such as [blocked clause elimination](/blocked-clause-elimination/) and the addition of new variables, are RAT steps. The checker DRAT-trim of Wetzler, Heule and Hunt (2014) checks the format, and the SAT Competition uses DRAT proofs to certify unsatisfiable answers.

## Definition

**Notation.** $F$ is a multiset of clauses with $n$ variables and $m$ clauses, and $|F|$ is its number of literal occurrences. For a clause $C$, $\overline{C}$ is the set of unit clauses $\{(\neg l) : l \in C\}$. We write $F \vdash_1 \bot$ when unit propagation on $F$ reaches a conflict, that is, it makes some clause false.

**RUP, also called asymmetric tautology (AT).** A clause $C$ is RUP with respect to $F$ if $F \wedge \overline{C} \vdash_1 \bot$. The empty clause is RUP with respect to $F$ exactly when unit propagation on $F$ alone reaches a conflict. A tautology is always RUP, because $\overline{C}$ then has two opposite units.

**RAT.** A clause $C$ is RAT on a literal $l \in C$ with respect to $F$ if for every clause $D \in F$ with $\neg l \in D$ the resolvent $C \cup (D \setminus \{\neg l\})$ is RUP with respect to $F$. The literal $l$ is the pivot. If no clause of $F$ contains $\neg l$, the condition is empty and $C$ is RAT on $l$. A non-empty RUP clause is RAT on each of its literals, because every resolvent contains $C$ and a superset of a RUP clause is RUP.

**DRAT proof.** A DRAT proof for $F$ is a list of steps $s_1, \ldots, s_t$. Put $F_0 = F$.

- An addition step $s_i = (\mathsf{a}, C_i)$ gives $F_i = F_{i-1} \cup \{C_i\}$. It is valid if $C_i$ is RUP with respect to $F_{i-1}$, or $C_i$ is non-empty and RAT on its first literal with respect to $F_{i-1}$.
- A deletion step $s_i = (\mathsf{d}, C_i)$ gives $F_i = F_{i-1} \setminus \{C_i\}$, which removes one copy of $C_i$.

The proof is a DRAT refutation of $F$ if all addition steps are valid and some addition step adds the empty clause. A DRUP proof is a DRAT proof in which every addition is RUP.

**File format.** The text format reuses the clause lines of the [DIMACS CNF format](/dimacs-cnf-format/). Each line is a clause ending in `0`, and a deletion line starts with `d`. The pivot of a RAT clause must be written first, because checkers test RAT only on the first literal.

**Lemma 1 (RUP clauses are implied).** If $C$ is RUP with respect to $F$, then every model of $F$ satisfies $C$.

*Proof.* Let $\alpha$ be a model of $F$ that makes $C$ false. Then $\alpha$ satisfies every unit of $\overline{C}$, so $\alpha$ is a model of $F \wedge \overline{C}$. Unit propagation only sets a literal when one clause forces it, so every literal it sets is true in every model of the clauses, in particular in $\alpha$. Thus no clause becomes false, and unit propagation cannot reach a conflict, which contradicts $F \wedge \overline{C} \vdash_1 \bot$. $\square$

**Lemma 2 (RAT clauses keep satisfiability).** If $C$ is RAT on $l$ with respect to $F$ and $\alpha$ is a model of $F$, then $\alpha$, or $\alpha$ with the value of $l$ flipped, is a model of $F \wedge C$. In particular, $F$ is satisfiable if and only if $F \wedge C$ is.

*Proof.* If $\alpha$ satisfies $C$ we are done. Otherwise $\alpha$ makes every literal of $C$ false, also $l$. Let $\alpha'$ be $\alpha$ with $l$ set true. Then $\alpha'$ satisfies $C$. Take a clause $D \in F$.

- If $\neg l \notin D$: $\alpha$ satisfies $D$ by a literal $k$. The literal $k$ is not $\neg l$, and it is not $l$ because $\alpha$ makes $l$ false. So $k$ is on another variable, and $\alpha'$ still makes $k$ true.
- If $\neg l \in D$: the resolvent $R = C \cup (D \setminus \{\neg l\})$ is RUP with respect to $F$, so $\alpha$ satisfies $R$ by Lemma 1. All literals of $C$ are false under $\alpha$, so $\alpha$ makes some $k \in D \setminus \{\neg l\}$ true. If $k = l$, then $\alpha'$ makes it true. Otherwise $k$ is on another variable and stays true.

So $\alpha'$ satisfies $F \wedge C$. The other direction holds because $F \subseteq F \wedge C$. $\square$

**Theorem (soundness).** If $F$ has a DRAT refutation, then $F$ is unsatisfiable.

*Proof.* Suppose $F$ has a model. We show by induction that every $F_i$ is satisfiable. A deletion removes a clause, and a subset of a satisfiable set is satisfiable. A valid addition keeps satisfiability by Lemma 1 for RUP and by Lemma 2 for RAT. But some $F_i$ contains the empty clause, which no assignment satisfies. $\blacksquare$

The theorem uses only one direction. A deletion can turn an unsatisfiable formula into a satisfiable one, and a RAT clause is in general not implied by $F$, so the formulas $F_i$ are not equivalent to $F$. They are only satisfiable when $F$ is. For this reason a deletion step can change which later clauses are RAT: RAT is not monotone, and a clause that is RAT with respect to $F_i$ can fail to be RAT with respect to a larger set.

### Checking a proof

A forward checker replays the steps in order.

```pseudo id=main
CHECK-DRAT(F, P)
L1  for each step s of P in order do
L2      if s deletes C then remove one copy of C from F and go to the next step
L3      C ← the clause added by s
L4      if unit propagation on F ∧ ¬C reaches no conflict then          ▷ C is not RUP
L5          if C is empty then return REJECT
L6          if some D ∈ F with ¬C[1] ∈ D has a resolvent C ∪ (D ∖ {¬C[1]}) that is not RUP then
L7              return REJECT                                               ▷ C is not RAT on its first literal
L8      add C to F; if C is empty then return ACCEPT
L9  return REJECT                                                           ▷ no empty clause was added
```

By the theorem, ACCEPT is correct. A RUP test is one run of unit propagation, which costs $O(|F_i|)$ with occurrence lists or [two watched literals](/two-watched-literals/). A RAT test runs one RUP test for each clause that contains $\neg l$. So the forward check costs $O\bigl(\sum_i (1 + \mathrm{occ}_i(\neg l_i)) \cdot |F_i|\bigr)$, which is polynomial in the sizes of $F$ and the proof, but can be very large in practice. DRAT-trim checks backward instead. It first replays the proof to the empty clause, then walks back and checks only the lemmas that some later check used. During each RUP test it prefers clauses already marked as used (core-first propagation). As a result it also prints an [unsatisfiable core](/unsat-core/) of $F$ and a smaller proof, for example in the [LRAT format](/lrat-proof/), which has hints for checking in linear time.

### Pitfalls

- **Unit deletions.** Solvers delete satisfied clauses at level zero, also the reason clauses of units. DRAT-trim by default ignores the deletion of unit clauses. Rebola-Pardo and Biere call this "operational" DRAT and show that it differs from the definition above, which they call "specified" DRAT. A checker for one flavor can reject a proof made for the other.
- **The pivot comes first.** A clause that is RAT only on its second literal fails in every standard checker.
- **RAT clauses are not consequences.** A model of $F_{i-1}$ can falsify a RAT lemma. Model reconstruction after a RAT step needs the flip of Lemma 2, as in [blocked clause elimination](/blocked-clause-elimination/).
- **Tautological resolvents.** A resolvent that contains a literal and its negation is RUP, and a checker must accept it without running propagation.

## Examples and non-examples

**A short refutation.** Let $F$ be the 8 clauses with three literals over $x_1, x_2, x_3$, one for each sign pattern. No assignment satisfies all of them. This proof has 5 lines:

```
1 2 0
1 0
d 1 2 0
2 0
0
```

- $(x_1 \vee x_2)$ is RUP: from $\neg x_1, \neg x_2$, the clause $(x_1 \vee x_2 \vee x_3)$ forces $x_3$, and then $(x_1 \vee x_2 \vee \neg x_3)$ is false.
- $(x_1)$ is RUP: from $\neg x_1$, the lemma $(x_1 \vee x_2)$ forces $x_2$, then $(x_1 \vee \neg x_2 \vee x_3)$ forces $x_3$, and $(x_1 \vee \neg x_2 \vee \neg x_3)$ is false.
- The deletion removes $(x_1 \vee x_2)$, which is now subsumed by $(x_1)$.
- $(x_2)$ is RUP: the unit $(x_1)$ and $\neg x_2$ make $(\neg x_1 \vee x_2 \vee x_3)$ force $x_3$, and then $(\neg x_1 \vee x_2 \vee \neg x_3)$ is false.
- The empty clause is RUP: the units $x_1, x_2$ make $(\neg x_1 \vee \neg x_2 \vee x_3)$ force $x_3$, and $(\neg x_1 \vee \neg x_2 \vee \neg x_3)$ is false.

The tiny CDCL solver in the implementation, which decides each variable false first, prints the same proof without the deletion and with the first lemma written as `2 1 0`. Its first conflict comes after the decisions $\neg x_1$ and $\neg x_2$, and the first-UIP clause is $(x_2 \vee x_1)$.

**A RAT step that is not RUP.** For the same $F$, the unit $(x_1)$ as the first step is not RUP: setting $x_1$ false leaves four binary clauses over $x_2, x_3$ and no unit. It is RAT on $x_1$: the clauses with $\neg x_1$ are $(\neg x_1 \vee \pm x_2 \vee \pm x_3)$, and each resolvent $(x_1 \vee \pm x_2 \vee \pm x_3)$ is a clause of $F$, so it is RUP. The proof `1 0`, `0` still fails at its second line, because after adding $(x_1)$ unit propagation finds no conflict.

**New variables.** Extended resolution introduces a fresh variable $x_4$ with $x_4 \leftrightarrow (x_1 \wedge x_2)$. In DRAT this is three RAT steps: `-4 1 0` and `-4 2 0` are RAT on $\neg x_4$ because no clause contains $x_4$, and `4 -1 -2 0` is RAT on $x_4$ because both resolvents, with $(\neg x_4 \vee x_1)$ and $(\neg x_4 \vee x_2)$, are tautologies. None of the three clauses follows from $F$, but adding them keeps satisfiability. So DRAT can simulate extended resolution, which is much stronger than [resolution](/refutation/); Kiesl, Rebola-Pardo and Heule (IJCAR 2018) showed the converse simulation.

**Non-example: a broken step.** Delete $(\neg x_1 \vee \neg x_2 \vee x_3)$ from $F$. The remaining 7 clauses have exactly one model, $x_1 = x_2 = 1, x_3 = 0$. The lemma $(\neg x_1 \vee \neg x_2)$ is false in that model, so by Lemmas 1 and 2 it can be neither RUP nor RAT, and the checker rejects the proof `1 2 0`, `-1 -2 0`, `0` at line 2. In the same way, if one clause is removed from an unsatisfiable formula and the result is satisfiable, every proof for the old formula must fail on the new one. The tests check this on random formulas.

**Non-example: no empty clause.** A proof whose lines are all valid but which never adds the empty clause proves nothing. The three extension steps above, alone, are such a proof.

## Related definitions

- [Refutation](/refutation/) and [resolvent](/resolvent/): a resolution refutation is a special DRUP proof, because each resolvent of two clauses is RUP with respect to them. DRUP proofs can be much shorter, because one RUP step can stand for many resolution steps.
- [LRAT proof](/lrat-proof/): DRAT with the clause IDs of the propagation steps written into the proof, so that a checker needs no search. DRAT-trim can translate DRAT to LRAT.
- [Clause learning](/clause-learning/) and [first UIP](/first-uip/): every clause learned by conflict analysis is RUP with respect to the current clause database, which is why CDCL solvers can print DRUP proofs. [Clause minimization](/clause-minimization/) keeps this property.
- [Clause database reduction](/clause-database-reduction/): the deletions of the solver become `d` lines, and they keep the checker fast.
- [Blocked clause elimination](/blocked-clause-elimination/) and [bounded variable elimination](/bounded-variable-elimination/): a blocked clause is RAT on its blocking literal, because all its resolvents are tautologies; so removing it, or adding it back, is a RAT step. Variable elimination adds resolvents, which are RUP, and then deletes the old clauses.
- [Unsatisfiable core](/unsat-core/): backward checking marks the clauses of $F$ that the proof used, and these form an unsatisfiable core.
- [CDCL simulates resolution](/cdcl-simulates-resolution/): the theorem that CDCL with restarts finds proofs as short as resolution, up to a polynomial.
- Propagation redundancy (PR), by Heule, Kiesl and Biere (2017), is a further generalization of RAT. It allows short proofs of the pigeonhole formulas without new variables.

## References
