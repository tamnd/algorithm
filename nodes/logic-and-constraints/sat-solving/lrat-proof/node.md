---
tag: XV3Z16
kind: definition
slug: lrat-proof
name: LRAT proof format
aliases:
- LRAT
- linear RAT
- LRAT proof
area: logic-and-constraints/sat-solving
level: advanced
summary: Clausal proof format in which each added clause lists the IDs of the clauses that make it RUP or RAT, so a checker needs no search and runs in time linear in the hinted proof.
prereqs: [drat-proof, unit-propagation]
see_also: [drat-proof, clause-learning, implication-graph, unsat-core, cdcl]
sources:
  - paper: doi:10.1007/978-3-319-63046-5_14
    title: Luís Cruz-Filipe, Marijn J. H. Heule, Warren A. Hunt Jr., Matt Kaufmann and Peter Schneider-Kamp, Efficient certified RAT verification, CADE-26, LNCS 10395, 2017
    locator: the LRAT format, its hint semantics for RUP and RAT steps, the translation from DRAT with DRAT-trim, and the verified checkers
  - paper: doi:10.1007/978-3-319-09284-3_31
    title: Nathan Wetzler, Marijn J. H. Heule and Warren A. Hunt Jr., DRAT-trim, Efficient checking and trimming using expressive clausal proofs, SAT 2014, LNCS 8561, 422-429
    locator: backward checking, which marks the clauses used in each unit propagation and is the source of the hints
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 15 (Heule, Proofs of Unsatisfiability), the sections on proof formats with hints and on verified checking
---

An LRAT proof is a [DRAT proof](/drat-proof/) with hints. Every clause has an integer ID. Each added clause comes with the list of IDs of the clauses that unit propagation needs to show that the new clause is RUP or RAT, in the order in which they become unit. The checker then does no search: it reads each hint clause once, checks that it is unit or false under the current assignment, and moves on. So checking takes time linear in the size of the proof with its hints, and the checker is short enough to prove correct in a proof assistant. Cruz-Filipe, Heule, Hunt, Kaufmann and Schneider-Kamp introduced LRAT in 2017. The usual path is that a [CDCL](/cdcl/) solver writes DRAT, the untrusted tool DRAT-trim finds the hints and writes LRAT, and a small verified checker checks the LRAT file. Some solvers write the hints themselves, because the hints of a learned clause are the reason clauses that [conflict analysis](/clause-learning/) visits.

## Definition

**Notation.** $F$ has $n$ variables and $m$ clauses, $|F|$ is its number of literal occurrences, and the clauses of $F$ have the IDs $1, \ldots, m$. For a clause $C$ and an assignment $\alpha$, a clause $D$ is **unit** under $\alpha$ if all literals of $D$ but one are false and that one is unassigned, and $D$ is **false** under $\alpha$ if all its literals are false.

**Lines.** An addition line has the form
$$i \;\; l_1 \cdots l_k \;\; 0 \;\; h_1 \cdots h_r \;\; 0,$$
where $i$ is the new ID, which must be larger than all earlier IDs, $C = (l_1 \vee \cdots \vee l_k)$ is the clause, and $h_1, \ldots, h_r$ are the hints. A deletion line has the form $i \;\, \mathsf{d} \;\, j_1 \cdots j_s \;\, 0$ and removes the clauses with the IDs $j_1, \ldots, j_s$. The first number $i$ of a deletion line is ignored.

**Applying a hint.** Let $\alpha$ be a partial assignment and $h$ the ID of an active clause $D$. If $D$ is unit under $\alpha$, applying $h$ sets its free literal true. If $D$ is false, applying $h$ ends with a conflict. In every other case, also when $D$ is satisfied, has two free literals or is not active, the step fails.

**A RUP step.** All hints are positive. Start with the assignment $\alpha$ that makes every literal of $C$ false and apply the hints in order. The step is valid if a hint ends with a conflict.

**A RAT step.** The hints have the form
$$p_1 \cdots p_a \;\; {-j_1} \; q^{1}_1 \cdots q^{1}_{b_1} \;\; {-j_2} \; q^{2}_1 \cdots \;\; \ldots \;\; {-j_t} \; q^{t}_1 \cdots q^{t}_{b_t}.$$
Let $l$ be the first literal of $C$. The step is valid if:

1. applying $p_1, \ldots, p_a$ from the negation of $C$ ends without failure, giving an assignment $\alpha$;
2. $j_1, \ldots, j_t$ are exactly the active clauses $D$ with $\neg l \in D$;
3. for each $s$, either the resolvent $C \cup (D_{j_s} \setminus \{\neg l\})$ is a tautology, or extending $\alpha$ by the negation of $D_{j_s} \setminus \{\neg l\}$ and applying $q^s_1, \ldots, q^s_{b_s}$ ends with a conflict.

An LRAT refutation of $F$ is a list of lines in which every addition is valid and the empty clause is added. The empty clause can only be a RUP step.

**Lemma 1.** A valid RUP step adds a clause that is RUP for the active clauses. A valid RAT step adds a clause that is RAT on its first literal for the active clauses.

*Proof.* Applying a hint is one step of [unit propagation](/unit-propagation/): it sets a literal that a unit clause forces. If some sequence of such steps from the negation of $C$ makes a clause false, then unit propagation to its fixpoint either stops earlier with a conflict or sets all the same literals and makes the same clause false, because the set of forced literals only grows. So a valid RUP step adds a RUP clause. In a RAT step, the assignment of item 3 is the negation of the resolvent, extended by unit steps, so each non-tautological resolvent is RUP. Tautological resolvents are RUP by definition. By item 2 every clause with $\neg l$ was tested. $\square$

So an LRAT refutation, with the hints removed, is a DRAT refutation, and $F$ is unsatisfiable by the soundness theorem of DRAT. A wrong hint can only make the checker reject a step. It can never make it accept a clause that is not RUP or RAT.

### Checking

```pseudo id=main
CHECK-LRAT(F, P)
L1  for each line s of P in order do
L2      if s deletes IDs j_1, …, j_s then remove those clauses and go to the next line
L3      (i, C, H) ← the ID, clause and hints of s; reject if i is not larger than all earlier IDs
L4      α ← the assignment that makes every literal of C false
L5      apply the positive hints of H before the first negative one; reject on failure; if one is false, the step is valid
L6      if C is empty then reject
L7      reject unless the negative hints name every active clause that contains ¬C[1]
L8      for each negative hint −j of H with the positive hints H_j after it do
L9          unless the resolvent with D_j is a tautology: extend α by the negation of D_j ∖ {¬C[1]}, apply H_j, reject without a conflict, then undo the extension
L10     store C under the ID i; if C is empty then accept
L11 reject                                                                       ▷ no empty clause
```

**Theorem (linear-time checking).** Keep the clauses in an array indexed by ID, the assignment in an array indexed by variable, and for each literal a count of the active clauses that contain it. Then a RUP line with clause $C$ and hints $H$ is checked in time $O\bigl(|C| + \sum_{h \in H} |D_h|\bigr)$, a deletion line in time $O(\sum_j |D_j|)$, and a RAT line in the same time as a RUP line plus $O(t)$ for the $t$ candidates. So the whole proof is checked in time $O\bigl(|F| + \sum_{\text{lines}} (|C| + \sum_{h \in H} |D_h|)\bigr)$, which is linear in the size of the proof when each hint is counted with the length of the clause it names.

*Proof.* Line L4 sets $|C|$ entries. Each hint is looked up in $O(1)$ and its clause is scanned once, so line L5 and each run of line L9 cost the total length of their hint clauses. Every assignment entry that a line sets is set by line L4, by a hint or by line L9, and it is cleared once, so clearing costs no more than setting. For line L7, the checker counts the distinct negative hints that name active clauses containing $\neg C[1]$ and compares the number with the stored count for $\neg C[1]$, in time $O(t)$. Additions and deletions update the counts in time proportional to the clause length. No step searches the clause set, and no step looks at a clause that is not named. $\blacksquare$

The bound compares with the DRAT case, where each RUP test runs full unit propagation over the active clauses and costs up to $O(|F_i|)$ per lemma. The implementation here scans the active clauses for line L7 instead of keeping counts, which is simpler but not linear.

**Producing the hints.** A forward pass over a DRAT proof finds hints for each lemma: run unit propagation from the negation of the lemma and record, for each forced literal, the clause that forced it. When a clause becomes false, walk back from it through the recorded reasons, as in conflict analysis in the [implication graph](/implication-graph/), and list the reasons that were used in the order in which they fired, followed by the false clause. For a RAT lemma, do this for each resolvent. DRAT-trim does the same during its backward check and so prints LRAT for only the lemmas that are needed.

## Examples and non-examples

**A refutation with a RAT step.** Number the 8 clauses with three literals over $x_1, x_2, x_3$ as follows: $1{:}\,(x_1 \vee x_2 \vee x_3)$, $2{:}\,(x_1 \vee x_2 \vee \neg x_3)$, $3{:}\,(x_1 \vee \neg x_2 \vee x_3)$, $4{:}\,(x_1 \vee \neg x_2 \vee \neg x_3)$, and $5$ to $8$ the same with $\neg x_1$ for $x_1$. This LRAT proof refutes them:

```
9 1 0 -5 1 -6 2 -7 3 -8 4 0
10 2 0 9 5 6 0
10 d 1 2 3 4 0
11 0 9 10 7 8 0
```

- Line 1 adds $(x_1)$ as clause 9. It is not RUP, so it has no positive hints before the first negative one. The clauses with $\neg x_1$ are 5, 6, 7 and 8, and all four are named. For $-5$, the resolvent is $(x_1 \vee x_2 \vee x_3)$; from its negation, clause 1 is false, so the hint list is just `1`. The other three are the same with clauses 2, 3 and 4.
- Line 2 adds $(x_2)$ as clause 10. From $\neg x_2$, clause 9 forces $x_1$, clause 5 $(\neg x_1 \vee x_2 \vee x_3)$ forces $x_3$, and clause 6 $(\neg x_1 \vee x_2 \vee \neg x_3)$ is false.
- Line 3 deletes clauses 1 to 4, which are no longer needed.
- Line 4 adds the empty clause. Clause 9 forces $x_1$, clause 10 forces $x_2$, clause 7 forces $x_3$, and clause 8 is false.

The hint generator in the implementation gives exactly the hints of lines 1, 2 and 4 from the DRAT proof `1 0`, `2 0`, `0`. The LRAT checker scans only the clauses that the hints name, once per mention. A DRAT check of the same proof runs unit propagation over all active clauses for each of the 4 resolvents and for the two later lemmas.

**Non-example: the conflict clause is missing.** If line 2 has the hints `9 5`, then after them $x_1$ and $x_3$ are set and no clause is false. The line is not a RUP step. It is also not a RAT step, because clauses 3, 4, 7 and 8 contain $\neg x_2$ and none of them is named, so the checker rejects it.

**Non-example: a candidate is missing.** If line 1 omits `-8 4`, then clause 8 contains $\neg x_1$ and is not named, and line L7 rejects the step, even though the resolvent with clause 8 is RUP.

**Non-example: wrong order.** If line 4 has the hints `7 9 10 8`, the first hint, clause 7 $(\neg x_1 \vee \neg x_2 \vee x_3)$, has three free literals when nothing is assigned. The checker rejects the line at once. It does not try other orders, and this is what makes it fast. The same holds for a hint that names a deleted clause, such as `9 10 7 1` after line 3.

## Related definitions

- [DRAT proof](/drat-proof/): the same proof without hints. LRAT is to DRAT what a resolution proof with named premises is to a list of resolvents.
- [Clause learning](/clause-learning/) and the [implication graph](/implication-graph/): the reason clauses that conflict analysis visits for a learned clause are its RUP hints.
- [Unsatisfiable core](/unsat-core/): the original clauses that appear as hints in a refutation form an unsatisfiable core.
- [Refutation](/refutation/): a resolution step with premises $D_1, D_2$ is an LRAT line with hints $D_1, D_2$, so resolution refutations translate into LRAT line by line.
- Verified checkers: the checker for LRAT is small enough to be proved correct in a proof assistant. The paper that introduced the format describes verified checkers, and later verified checkers, for example in ACL2 and in CakeML, follow the same plan.

## References
