---
tag: YEK621
kind: technique
slug: clause-subsumption
name: Clause subsumption
aliases:
- subsumption
- self-subsuming resolution
- clause strengthening
- backward subsumption
area: logic-and-constraints/sat-solving
level: advanced
summary: Remove each clause that contains another clause, and shorten a clause when a resolvent subsumes it; both steps keep the formula logically equivalent.
prereqs: [clause, conjunctive-normal-form, resolvent]
see_also: [bounded-variable-elimination, blocked-clause-elimination, failed-literal-probing, equivalent-literal-substitution, subsumption, davis-putnam-elimination, cdcl]
sources:
  - paper: doi:10.1007/11499107_5
    title: Niklas Eén and Armin Biere, Effective preprocessing in SAT through variable and clause elimination, SAT 2005, LNCS 3569, 61-75
    locator: the sections on subsumption, self-subsuming resolution, occurrence lists, the queue of touched clauses and clause signatures (SatELite)
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 9 (Biere, Järvisalo and Kiesl, Preprocessing in SAT Solving), the section on subsumption and strengthening
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the discussion of preprocessing (subsumption and strengthening)
---

Clause subsumption is a simplification step for a [CNF](/conjunctive-normal-form/) formula. A clause $C$ **subsumes** a clause $D$ when $C \subseteq D$. Then every assignment that satisfies $C$ also satisfies $D$, so $D$ can be removed. **Self-subsuming resolution**, or strengthening, handles the near miss: if $C = C' \vee l$ and $D \supseteq C' \vee \neg l$, the [resolvent](/resolvent/) of $C$ and $D$ on $l$ is $D \setminus \{\neg l\}$, which subsumes $D$, so the literal $\neg l$ can be deleted from $D$. Both steps keep the formula logically equivalent over the same variables, so no model has to be rebuilt afterwards. Every modern SAT preprocessor and inprocessor uses them, usually together with [bounded variable elimination](/bounded-variable-elimination/), which creates many subsumed clauses.

## In plain words

A clause is a list of options, at least one of which must hold. If one list is part of a longer list, the longer list says nothing new: whenever the short list is met, so is the long one. So you can throw the long list away.

A second rule fixes lists that almost match. Suppose one list says "A or B" and another says "not A or B or C". If A holds, the second list needs B or C. If A fails, the first list gives B. Either way "B or C" holds, so the option "not A" can be dropped from the second list. The formula gets shorter, and it still means exactly the same thing.

## When it applies

Use it on any CNF formula, before the search or between search phases. Signals that it pays off:

- the formula was produced by a translation (for example [Tseitin](/tseitin-transformation/) or a bit-blaster), which often makes duplicate and nested clauses;
- you just added many clauses, such as resolvents from [variable elimination](/bounded-variable-elimination/) or units from [failed-literal probing](/failed-literal-probing/), and old clauses may now be subsumed or shortened;
- a solver keeps learned clauses, which can subsume original clauses or other learned ones.

## The template

Notation: $F$ is a set of clauses, $n$ variables, $m$ clauses, $k$ the longest clause length and $|F|$ the number of literal occurrences. $\mathrm{occ}(l)$ is the set of clauses that contain the literal $l$. The step keeps a queue of clauses to use as subsumers.

```pseudo id=main
SUBSUME(F)
L1  Q ← all clauses of F
L2  while Q is not empty do
L3      C ← take a clause from Q; skip it if it was removed
L4      v ← the variable of C with the fewest occurrences in F (both signs)
L5      for each clause D ≠ C in occ(v) ∪ occ(¬v) with |D| ≥ |C| do
L6          if C ⊆ D then remove D from F
L7          else if C = C' ∨ l with C' ⊆ D and ¬l ∈ D then
L8              D ← D \ {¬l};  put D in Q        ▷ self-subsuming resolution
L9  return F
```

A clause that is a candidate for either step contains $v$ or $\neg v$, so line L5 sees every candidate. Tautologies and repeated literals are removed before line L1. If line L8 makes $D$ empty, $F$ is unsatisfiable.

### Example

Take $F$ with the six clauses
$$(x_1 \vee x_2 \vee x_3),\ (x_1 \vee x_2),\ (\neg x_1 \vee x_2 \vee x_4),\ (x_1 \vee \neg x_2),\ (x_2 \vee \neg x_3 \vee x_4),\ (x_3 \vee \neg x_4).$$

- $(x_1 \vee x_2)$ subsumes $(x_1 \vee x_2 \vee x_3)$, which is removed.
- $(x_1 \vee x_2)$ and $(\neg x_1 \vee x_2 \vee x_4)$: here $C' = x_2$, $l = x_1$, so the second clause becomes $(x_2 \vee x_4)$.
- $(x_2 \vee x_4)$ subsumes $(x_2 \vee \neg x_3 \vee x_4)$.
- $(x_1 \vee x_2)$ and $(x_1 \vee \neg x_2)$: here $C' = x_1$, $l = x_2$, so the second clause becomes the unit $(x_1)$.
- $(x_1)$ subsumes $(x_1 \vee x_2)$.

The result is $(x_1) \wedge (x_2 \vee x_4) \wedge (x_3 \vee \neg x_4)$: 3 clauses with 5 literals instead of 6 clauses with 15 literals, and the same 4 models over $x_1, \ldots, x_4$.

### Why it is correct

**Lemma 1.** If $C \subseteq D$ and $C \in F$, then $F$ and $F \setminus \{D\}$ have the same models.

*Proof.* Removing a clause can only add models. Let $\alpha$ satisfy $F \setminus \{D\}$. It satisfies $C$, so some literal of $C$ is true, and that literal is in $D$. $\square$

**Lemma 2.** If $C = C' \vee l \in F$ and $D = D' \vee \neg l \in F$ with $C' \subseteq D'$, then $F$ and $(F \setminus \{D\}) \cup \{D'\}$ have the same models.

*Proof.* The resolvent of $C$ and $D$ on $l$ is $C' \vee D' = D'$. Every model of $F$ satisfies the resolvent, so it satisfies $D'$. Conversely, $D' \subseteq D$, so every model of $D'$ satisfies $D$. $\square$

**Theorem.** SUBSUME stops after at most $|F|$ steps of lines L6 and L8, and returns a formula with the same models as $F$ in which no clause subsumes another and no pair allows the step of line L8.

*Proof.* Equivalence follows from Lemmas 1 and 2 by induction on the steps. Each step of line L6 removes a clause and each step of line L8 removes a literal, so the number of literal occurrences falls each time. For the fixpoint: a clause is processed after its last change, because line L8 puts the changed clause back in $Q$. When $C$ is processed, it removes or shortens every candidate. Later steps only shrink or remove clauses, and if $C \not\subseteq D$ then $C \not\subseteq D''$ for every $D'' \subseteq D$; the same holds for the condition of line L7. So a pair that is not reducible when $C$ is processed stays so, unless $C$ itself changes, and then $C$ is processed again. $\blacksquare$

### Cost

One test "$C \subseteq D$" costs $O(|C| + |D|)$ with a marked array. With $\mathrm{occ}$ lists, processing $C$ costs $O(k \cdot (|\mathrm{occ}(v)| + |\mathrm{occ}(\neg v)|))$. In the worst case all $m$ clauses share a variable and the total is $O(m^2 k)$. In practice the choice of the rarest variable in line L4 and the signatures below keep the candidate lists short.

## Classic examples

- **SatELite.** Eén and Biere combine subsumption, self-subsuming resolution and [bounded variable elimination](/bounded-variable-elimination/) in a loop; each elimination adds resolvents that are checked for subsumption at once.
- **Learned-clause minimization.** In [CDCL](/cdcl/), the learned clause is shortened by self-subsuming resolution with the reason clauses of its literals.
- **On-the-fly subsumption.** During [conflict analysis](/clause-learning/), if an intermediate resolvent is a strict subset of the antecedent clause just used, the antecedent can be replaced by the resolvent.
- **Inprocessing.** Solvers such as CaDiCaL and Kissat run subsumption at intervals on the learned and the original clauses.

## Variations

- **Forward subsumption.** For each new clause $D$, check whether some existing clause subsumes it, by looking at $\mathrm{occ}(l)$ for the literals $l \in D$. This suits a stream of new clauses.
- **Signatures.** Give each clause a 64-bit word with bit $h(\mathrm{var}(l)) \bmod 64$ set for each literal. If $\mathrm{sig}(C) \wedge \neg\mathrm{sig}(D) \ne 0$, then $C$ cannot subsume or strengthen $D$, and the full test is skipped.
- **Asymmetric subsumption and vivification.** A clause $D$ is redundant if [unit propagation](/unit-propagation/) on $F \setminus \{D\}$ with all literals of $D$ false gives a conflict. Vivification shortens $D$ in the same way. These are stronger and cost more.

## Pitfalls

- **Learned and original clauses.** If a learned clause subsumes an original one, the solver must keep the learned clause as irredundant. If the learned clause is later deleted, the original information is lost.
- **Proof output.** In a [DRAT](/drat-proof/) proof, write the strengthened clause $D'$ as an addition before you delete $D$. $D'$ is a resolvent, so it passes the RUP check.
- **Variable elimination interaction.** Clauses on the reconstruction stack of an eliminated variable are no longer in $F$. Do not use them as subsumers of clauses that are in $F$ unless the elimination is undone.
- **Repeated literals and tautologies.** Normalize clauses first, or the test $|D| \ge |C|$ and the subset test can give wrong answers.

## Exercises

1. Show that the order of steps matters for the final formula: give two clauses where strengthening in one order gives a different result from strengthening in the other order, and check that both results are equivalent.
2. Prove that if $C$ strengthens $D$ on $l$ and the result $D'$ is a subset of $C$, then $D'$ subsumes $C$ as well, and that the pair $C$, $D$ is then replaced by $D'$ alone. When does this happen?
3. Design forward subsumption with $\mathrm{occ}$ lists for a clause $D$ of length $k$, and give its cost in terms of the list lengths.

## References
