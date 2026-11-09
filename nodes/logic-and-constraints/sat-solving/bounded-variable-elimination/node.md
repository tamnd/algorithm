---
tag: CFQP37
kind: technique
slug: bounded-variable-elimination
name: Bounded variable elimination
aliases:
- SatELite preprocessing
- BVE
- variable elimination by clause distribution
- NiVER
area: logic-and-constraints/sat-solving
level: advanced
summary: Eliminate a variable by replacing its clauses with all their non-tautological resolvents, but only when this does not make the formula larger; a model is rebuilt from the saved clauses.
prereqs: [davis-putnam-elimination, resolvent, conjunctive-normal-form]
see_also: [clause-subsumption, blocked-clause-elimination, equivalent-literal-substitution, failed-literal-probing, cdcl, tseitin-transformation]
sources:
  - paper: doi:10.1007/11499107_5
    title: Niklas Eén and Armin Biere, Effective preprocessing in SAT through variable and clause elimination, SAT 2005, LNCS 3569, 61-75
    locator: variable elimination by clause distribution with the bound "no more clauses than before", elimination by substitution of gate definitions, and the combination with subsumption (SatELite)
  - paper: doi:10.1145/321033.321034
    title: Martin Davis and Hilary Putnam, A computing procedure for quantification theory, Journal of the ACM 7(3), 1960, 201-215
    locator: the rule for eliminating atomic formulas, which replaces the clauses of a variable by their resolvents
  - paper: "Sathiamoorthy Subbarayan and Dhiraj K. Pradhan, NiVER: Non-increasing variable elimination resolution for preprocessing SAT instances, SAT 2004, LNCS 3542, 2005, pages 276 to 291"
    title: NiVER
    locator: elimination only when the number of literals does not grow
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 9 (Biere, Järvisalo and Kiesl, Preprocessing in SAT Solving), the sections on bounded variable elimination and model reconstruction
---

Bounded variable elimination (BVE) removes a variable $x$ from a [CNF](/conjunctive-normal-form/) formula by the [Davis-Putnam rule](/davis-putnam-elimination/): replace all clauses that contain $x$ or $\neg x$ by all their non-tautological [resolvents](/resolvent/) on $x$. The result is satisfiable exactly when the input is. Done for every variable, this rule can blow up the formula, so BVE applies it only when the number of clauses does not grow (Eén and Biere's SatELite, 2005), or when the number of literals does not grow (Subbarayan and Pradhan's NiVER). A model of the smaller formula is turned into a model of the original by going back through the removed clauses and flipping $x$ where a clause is false. BVE is the most effective single step of modern SAT preprocessing, and it is run again between search phases in current solvers.

## In plain words

Choose a variable. Collect the clauses where it appears plain and the clauses where it appears negated. Combine each clause of the first kind with each clause of the second kind by dropping the variable from both and joining what is left. The combined clauses say everything that the old clauses said about the other variables. So you can delete the old clauses and keep the combined ones, and the variable is gone.

There is a catch: ten plus ten clauses can give a hundred combinations. So you only do this when the new set is not bigger than the old one. You keep the deleted clauses on the side. When the solver finds a solution, you go back through them and set the removed variable so that each one is met.

## When it applies

Use it before the search and between search phases when you need satisfiability and one model. Signals:

- many variables occur in few clauses, for example the gate variables of a [Tseitin encoding](/tseitin-transformation/), whose clause pairs often resolve into fewer clauses;
- the formula has variables defined by others ($x \leftrightarrow (a \wedge b)$, $x \leftrightarrow (a \oplus b)$), so substitution removes them cheaply;
- you can afford a model reconstruction step at the end.

## The template

Notation: $F$ is a set of clauses over $n$ variables, with $m$ clauses and $|F|$ literal occurrences. For a variable $x$, $P_x$ is the set of clauses with $x$, $N_x$ the set with $\neg x$, and
$$R_x = \{\, C \otimes_x D : C \in P_x,\ D \in N_x,\ C \otimes_x D \text{ not a tautology} \,\},$$
where $C \otimes_x D = (C \setminus \{x\}) \cup (D \setminus \{\neg x\})$. The step "eliminate $x$" replaces $F$ by $(F \setminus (P_x \cup N_x)) \cup R_x$.

```pseudo id=main
BVE(F, slack)
L1  repeat until no variable is eliminated in a full pass
L2      for each variable x, by increasing |P_x| · |N_x| do
L3          P ← clauses of F with x;  N ← clauses of F with ¬x
L4          R ← all non-tautological resolvents C ⊗_x D for C ∈ P, D ∈ N
L5          if |R| ≤ |P| + |N| + slack then
L6              remove P and N from F
L7              add R to F                       ▷ x no longer occurs
L8              push (C, x) for C ∈ P, then (D, ¬x) for D ∈ N, on the stack σ
L9  RECONSTRUCT(α, σ): for each (C, l) in σ, from the last pushed to the first
L10     if α makes C false then set α(l) ← true
L11 return α
```

With $\text{slack} = 0$ the number of clauses never grows. Real solvers also limit the length of a resolvent and the size of $P$ and $N$, and run [subsumption](/clause-subsumption/) on the new resolvents.

### Example

Let $F = (x \vee a) \wedge (x \vee b) \wedge (\neg x \vee c) \wedge (\neg x \vee \neg a \vee d)$. Then $P_x$ and $N_x$ have 2 clauses each, and the four resolvents are
$$(a \vee c),\quad (a \vee \neg a \vee d)\ \text{(tautology)},\quad (b \vee c),\quad (b \vee \neg a \vee d).$$
So $R_x$ has 3 clauses, which is at most $2 + 2$, and $x$ is eliminated: $F$ becomes $(a \vee c) \wedge (b \vee c) \wedge (\neg a \vee b \vee d)$.

Take the model $a = 0$, $b = 1$, $c = 1$, $d = 0$ of the new formula, and $x = 0$ for the removed variable. RECONSTRUCT checks $(\neg x \vee \neg a \vee d)$ and $(\neg x \vee c)$, which are true, and then $(x \vee b)$, true, and $(x \vee a)$, false, so it sets $x = 1$. Now all four original clauses are true.

### Why it is correct

**Lemma 1 (Davis and Putnam).** Let $G = F \setminus (P_x \cup N_x)$. A total assignment $\alpha$ of the other variables satisfies $G \cup R_x$ if and only if some value of $x$ extends $\alpha$ to a model of $F$.

*Proof.* If $\alpha$ with some $x$ satisfies $F$, it satisfies $G$ and every resolvent, because resolution is sound and $x$ does not occur in a resolvent. Conversely, let $\alpha$ satisfy $G \cup R_x$. Let $P_0$ be the set of $C \in P_x$ with $C \setminus \{x\}$ false under $\alpha$, and $N_0$ the same for $N_x$. If $C \in P_0$ and $D \in N_0$, the resolvent $C \otimes_x D$ is false under $\alpha$. It is not a tautology, since a tautology is never false, so it is in $R_x$, against the choice of $\alpha$. So $P_0$ or $N_0$ is empty. If $P_0$ is empty, set $x = 0$: each clause of $P_x$ is true by its other literals, and each clause of $N_x$ is true by $\neg x$. If $N_0$ is empty, set $x = 1$. $\square$

**Theorem (satisfiability and reconstruction).** After any number of eliminations, the reduced formula is satisfiable if and only if $F$ is, and for every total model $\alpha$ of the reduced formula, RECONSTRUCT$(\alpha, \sigma)$ is a model of $F$.

*Proof.* Equisatisfiability follows from Lemma 1, one elimination at a time. For reconstruction, consider the last elimination, of $x$, with $F' = G \cup R_x$ before the later steps. By induction on the later eliminations, when RECONSTRUCT reaches the entries of $x$, the current $\alpha$ is a model of $F'$. These entries are the clauses of $N_x$ (processed first) and of $P_x$. Use $P_0$ and $N_0$ from the proof of Lemma 1; at most one is non-empty. If $N_0$ is not empty, a clause of $N_0$ is false only when $x = 1$, so line L10 sets $x = 0$; then every clause of $N_x$ is true, and every clause of $P_x$ is true by its other literals, so no further flip happens. If $N_0$ is empty, the clauses of $N_x$ are true for both values of $x$, and line L10 sets $x = 1$ exactly when a clause of $P_0$ is false. In both cases $\alpha$ satisfies $P_x \cup N_x$ and, since $x$ does not occur in $G$, also $G$. So $\alpha$ is a model of the formula before the elimination. $\blacksquare$

**Termination and size.** Each elimination removes one variable for good, so there are at most $n$ eliminations. With $\text{slack} = 0$ each one keeps $m$ or lowers it. Computing $R_x$ costs $O(|P_x| \cdot |N_x| \cdot k)$, with $k$ the longest clause length.

## Classic examples

- **SatELite and MiniSat.** Eén and Biere's preprocessor eliminates variables in the order of $|P_x| \cdot |N_x|$ and checks each resolvent for [subsumption](/clause-subsumption/). Its results made BVE a standard step, and MiniSat 2 and later solvers include it.
- **Tseitin gates.** For an AND gate $x \leftrightarrow (a \wedge b)$ with $x$ used in $k$ clauses, eliminating $x$ gives at most $3k$ resolvents and often fewer; on circuits from hardware verification many gate variables are removed.
- **Davis-Putnam 1960.** The original procedure eliminates every variable in turn without a bound. It decides satisfiability but can need exponential space. See [Davis-Putnam elimination](/davis-putnam-elimination/).
- **Inprocessing in CaDiCaL and Kissat.** These solvers run BVE in rounds, raise the bound of allowed growth slowly over the rounds, and keep one reconstruction stack for BVE and [blocked clause elimination](/blocked-clause-elimination/).

## Variations

- **Elimination by substitution.** If the clauses $G_x \subseteq P_x \cup N_x$ define $x$ as a gate of other variables, only the resolvents between $G_x$ and the rest are needed; the resolvents inside $G_x$ are tautologies and those outside $G_x$ follow from the others. This often makes $|R_x|$ much smaller.
- **Literal bound.** NiVER compares the number of literals, not clauses. Other bounds allow a growth of a few clauses (the slack), raised in later rounds.
- **Bounded variable addition.** The inverse step adds a new variable to replace a product of clause sets, which can make the formula smaller.
- **Relation to BCE.** Once $R_x$ is added, each resolvent of a clause $C \in P_x$ on $x$ is a tautology or a member of $R_x$. So the clauses of $P_x$ can be removed one by one as RAT clauses on $x$, and then $\neg x$ is pure and the clauses of $N_x$ are blocked. This is why the flip-based reconstruction of [blocked clause elimination](/blocked-clause-elimination/) serves both steps.

## Pitfalls

- **Frozen variables.** Do not eliminate a variable that appears in assumptions or in clauses that will be added later, as in [incremental SAT](/incremental-sat/). Keep a set of frozen variables.
- **Models.** BVE keeps satisfiability, not the set of models over the eliminated variables. Model counting needs a different method.
- **Learned clauses.** Learned clauses that contain an eliminated variable must be deleted; they cannot simply be kept.
- **Reconstruction order.** The stack must be processed from the end. The clauses of one variable can be processed in any order among themselves, but the variables must go in the reverse order of elimination.
- **Duplicate and subsumed resolvents.** Count each distinct resolvent once; otherwise the bound rejects eliminations that would make the formula smaller.

## Exercises

1. For the XOR gate $x \leftrightarrow (a \oplus b)$, with $x$ used in $k$ other clauses, count the resolvents with and without elimination by substitution.
2. Show that eliminating every variable in turn with the Davis-Putnam rule can produce $2^{\Omega(n)}$ clauses for some formulas with $O(n)$ clauses.
3. Prove that BVE with $\text{slack} = 0$ applied to a formula with $m$ clauses and every variable in at most two clauses ends with at most $m$ clauses and no variable that occurs in exactly one positive and one negative clause.

## References
