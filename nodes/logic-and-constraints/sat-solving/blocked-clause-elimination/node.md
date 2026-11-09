---
tag: GQDPDA
kind: technique
slug: blocked-clause-elimination
name: Blocked clause elimination
aliases:
- BCE
- blocked clause
area: logic-and-constraints/sat-solving
level: research
summary: Remove a clause C that has a literal l such that every resolvent of C on l is a tautology; this keeps satisfiability, and a model is rebuilt by flipping l.
prereqs: [clause, resolvent, conjunctive-normal-form]
see_also: [bounded-variable-elimination, clause-subsumption, plaisted-greenbaum-transformation, pure-literal-elimination, drat-proof, autarky]
sources:
  - paper: "Oliver Kullmann, On a generalization of extended resolution, Discrete Applied Mathematics 96-97, 1999, pages 149 to 176"
    title: On a generalization of extended resolution
    locator: the definition of blocked clauses and the result that adding or removing a blocked clause keeps satisfiability
  - paper: doi:10.1007/978-3-642-12002-2_10
    title: Matti Järvisalo, Armin Biere and Marijn J. H. Heule, Blocked clause elimination, TACAS 2010, LNCS 6015, 129-144
    locator: BCE as a preprocessing step, its confluence, and its effect on Tseitin encodings (it achieves the Plaisted-Greenbaum reduction and cone-of-influence reduction)
  - paper: doi:10.1007/978-3-642-31365-3_28
    title: Matti Järvisalo, Marijn J. H. Heule and Armin Biere, Inprocessing rules, IJCAR 2012, LNCS 7364, 355-370
    locator: the reconstruction stack of removed clauses with witness literals and the flip-based model reconstruction
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 9 (Biere, Järvisalo and Kiesl, Preprocessing in SAT Solving), the sections on blocked clauses and model reconstruction
---

Blocked clause elimination (BCE) removes clauses from a [CNF](/conjunctive-normal-form/) formula without changing whether it is satisfiable. A clause $C$ is **blocked** on a literal $l \in C$ when every [resolvent](/resolvent/) of $C$ on $l$ with a clause that contains $\neg l$ is a tautology. Kullmann introduced blocked clauses in 1999; Järvisalo, Biere and Heule made their elimination a practical preprocessing step in 2010. BCE does not keep the set of models, but a model of the reduced formula becomes a model of the original one by a simple rule: go through the removed clauses in reverse order, and flip the blocking literal of each clause that is false. [Pure literal elimination](/pure-literal-elimination/) is the special case where no clause contains $\neg l$. On [Tseitin encodings](/tseitin-transformation/), BCE removes the clauses that the [Plaisted-Greenbaum transformation](/plaisted-greenbaum-transformation/) leaves out, and more.

## In plain words

Pick a clause and one of its options. Look at every other clause that contains the opposite of that option. If each of those clauses already shares an option with the first clause in an opposite form, then the first clause can never be the only obstacle to a solution. If a solution breaks it, you can switch that one option, and every clause hurt by the switch stays satisfied by the shared opposite option.

So you delete such clauses, one after another, and keep each one in a list with its option. When the solver finds a solution of the smaller formula, you go back through the list from the end and switch the option of each listed clause that is not met.

## When it applies

Use it as a preprocessing or inprocessing step when you need only satisfiability and one model, not all models. Signals:

- the formula comes from a circuit through Tseitin's transformation, so many gate clauses are only needed in one direction;
- variables are defined by other variables, as in $x \leftrightarrow (a \wedge b)$, and the definition is used only in one polarity;
- you will also run [bounded variable elimination](/bounded-variable-elimination/): removing blocked clauses lowers occurrence counts and makes more eliminations cheap.

Do not use it when you count models, enumerate models, or when later clauses or assumptions may mention the removed literals (see Pitfalls).

## The template

Notation: $F$ is a set of clauses with $n$ variables, $m$ clauses and $|F|$ literal occurrences. For $C$ with $l \in C$ and $D$ with $\neg l \in D$, the resolvent is $C \otimes_l D = (C \setminus \{l\}) \cup (D \setminus \{\neg l\})$. It is a tautology if it contains a pair $a, \neg a$.

**Definition.** $C \in F$ is blocked on $l \in C$ with respect to $F$ if for every $D \in F$ with $\neg l \in D$, the resolvent $C \otimes_l D$ is a tautology; that is, there is a literal $a \in C \setminus \{l\}$ with $\neg a \in D$.

```pseudo id=main
BCE(F)
L1  σ ← empty stack;  Q ← all clauses of F
L2  while Q is not empty do
L3      C ← take a clause from Q; skip it if it was removed
L4      for each literal l ∈ C do
L5          if C is blocked on l with respect to F then
L6              remove C from F;  push (C, l) on σ
L7              put into Q every clause of F that contains ¬a for some a ∈ C;  stop the loop over l
L8  return (F, σ)

RECONSTRUCT(α, σ)                ▷ α: a total model of the reduced F
L9  for each (C, l) in σ, from the last pushed to the first do
L10     if α makes every literal of C false then set α(l) ← true
L11 return α
```

Line L7 is enough because removing $C$ can only make a clause $D$ blocked on a literal $\neg a$ with $a \in C$; for other literals the set of resolution partners of $D$ is the same.

### Example

Let $F$ have the five clauses
$$(\neg x_1 \vee \neg x_3),\ (x_1 \vee \neg x_2),\ (x_2 \vee x_3),\ (\neg x_2 \vee x_4),\ (x_2 \vee \neg x_4).$$

The last two clauses say $x_4 \leftrightarrow x_2$. The clause $(\neg x_2 \vee x_4)$ is blocked on $x_4$: the only clause with $\neg x_4$ is $(x_2 \vee \neg x_4)$, and the resolvent $(\neg x_2 \vee x_2)$ is a tautology. After it is removed, no clause contains $x_4$, so $(x_2 \vee \neg x_4)$ is blocked on $\neg x_4$ (the pure case). The other three clauses are not blocked, and BCE returns them with $\sigma = [(\neg x_2 \vee x_4, x_4),\ (x_2 \vee \neg x_4, \neg x_4)]$.

The reduced formula does not mention $x_4$, so a solver may return $\alpha = (x_1, x_2, x_3, x_4) = (0, 0, 1, 1)$. RECONSTRUCT looks at the last entry first: $(x_2 \vee \neg x_4)$ is false, so it sets $x_4 = 0$. Then $(\neg x_2 \vee x_4)$ is true. The result $(0, 0, 1, 0)$ satisfies all five clauses.

### Why it is correct

**Lemma 1 (one step).** Let $C \in F$ be blocked on $l$ with respect to $F$, and let $\alpha$ be a model of $F \setminus \{C\}$. If $\alpha$ satisfies $C$, it is a model of $F$. Otherwise, $\alpha'$, which is $\alpha$ with $l$ set true, is a model of $F$.

*Proof.* Assume $\alpha$ makes $C$ false. Then $\alpha'$ makes $l$ true, so it satisfies $C$. Let $D \in F \setminus \{C\}$. If $\neg l \notin D$, the flip makes no literal of $D$ false, so $D$ stays true. If $\neg l \in D$, the blocking condition gives $a \in C \setminus \{l\}$ with $\neg a \in D$. As $\alpha$ makes $C$ false, $a$ is false under $\alpha$, so $\neg a$ is true. The variable of $a$ is not the variable of $l$: otherwise $a = \neg l$, so $C$ contains $l$ and $\neg l$, and a tautology is never false. So the flip does not change $\neg a$, which is still true under $\alpha'$, and $D$ is true. $\square$

**Theorem 1 (satisfiability and reconstruction).** Let BCE remove $C_1, \ldots, C_t$ in this order with blocking literals $l_1, \ldots, l_t$, and return $F_t$. Then $F$ is satisfiable if and only if $F_t$ is, and for every model $\alpha$ of $F_t$ that assigns all variables of $F$, RECONSTRUCT$(\alpha, \sigma)$ is a model of $F$.

*Proof.* Let $F_0 = F$ and $F_i = F_{i-1} \setminus \{C_i\}$. $C_i$ is blocked on $l_i$ with respect to $F_{i-1}$. RECONSTRUCT processes $i = t, t-1, \ldots, 1$; by Lemma 1, if the current $\alpha$ is a model of $F_i$, then after step $i$ it is a model of $F_{i-1}$. By induction the result is a model of $F_0$. Conversely $F_t \subseteq F$, so a model of $F$ is a model of $F_t$. $\blacksquare$

**Lemma 2 (monotonicity).** If $C$ is blocked on $l$ with respect to $F$ and $G \subseteq F$ with $C \in G$, then $C$ is blocked on $l$ with respect to $G$.

*Proof.* The condition is a "for every $D$" over the clauses with $\neg l$, and $G$ has fewer such clauses. $\square$

**Theorem 2 (confluence; Järvisalo, Biere and Heule 2010).** Every run of BCE to a fixpoint removes the same set of clauses.

*Proof.* Let two runs remove the sets $R$ and $R'$, and let $C_1, \ldots, C_t$ be the order of the first run. Suppose some $C_i \notin R'$, with $i$ least. Then $C_1, \ldots, C_{i-1} \in R'$, so $F \setminus R' \subseteq F \setminus \{C_1, \ldots, C_{i-1}\}$, and $C_i \in F \setminus R'$. By Lemma 2, $C_i$ is blocked in $F \setminus R'$, against the fixpoint of the second run. So $R \subseteq R'$, and by symmetry $R = R'$. $\blacksquare$

### Cost

One test "$C$ blocked on $l$" costs $O(\sum_{D \ni \neg l} (|C| + |D|))$ with a marked array for $C$, which is $O(|C| \cdot |\mathrm{occ}(\neg l)| + |F|)$ in the worst case. Each removal puts at most $\sum_{a \in C} |\mathrm{occ}(\neg a)|$ clauses back in the queue. There are at most $m$ removals and each one puts back at most $|F|$ clauses, so a full run makes $O(m \cdot |F|)$ clause tests and is polynomial in $|F|$. Practical tools bound the number of resolution partners they check per literal.

## Classic examples

- **Pure literals.** If no clause contains $\neg l$, every clause with $l$ is blocked on $l$. This is [pure literal elimination](/pure-literal-elimination/).
- **Tseitin encodings.** For a gate $y \leftrightarrow (a \wedge b)$ where $y$ appears only positively elsewhere, the clause $(y \vee \neg a \vee \neg b)$ is blocked on $y$. BCE to a fixpoint thus removes the clauses that the [Plaisted-Greenbaum transformation](/plaisted-greenbaum-transformation/) omits, and it also removes gates outside the cone of influence of the output (Järvisalo, Biere and Heule 2010).
- **Equivalences used once.** A definition $x \leftrightarrow y$ of a variable $x$ that occurs nowhere else disappears, as in the example.
- **Extended resolution.** The definition clauses of a fresh variable, $(\neg x \vee a), (\neg x \vee b), (x \vee \neg a \vee \neg b)$, are blocked on $x$ and $\neg x$. Kullmann's result that adding blocked clauses keeps satisfiability generalizes the extension rule of extended resolution.

## Variations

- **Blocked clause addition.** Adding a clause that is blocked with respect to $F$ also keeps satisfiability, by the same lemma read in the other direction. The [DRAT](/drat-proof/) proof format allows a generalization of it, the RAT step.
- **Covered clause elimination.** Extend $C$ with literals that occur in every non-tautological resolution partner (covered literals) and test the extended clause for being blocked. It removes strictly more clauses.
- **Resolution asymmetric tautologies.** Replace "every resolvent is a tautology" by "every resolvent is implied by [unit propagation](/unit-propagation/)". This is the RAT property; removing a RAT clause also keeps satisfiability, with the same flip reconstruction.
- **Inprocessing.** Järvisalo, Heule and Biere show how to run BCE, variable elimination and other steps between search phases, with one reconstruction stack for all of them.

## Pitfalls

- **Models change.** The reduced formula can have models that the original does not have, and the original can have more models. Model counting and all-solutions enumeration need equivalence-preserving steps.
- **Frozen variables.** If clauses or assumptions that mention $l$ may be added later (as in [incremental SAT](/incremental-sat/)), a clause blocked on $l$ now may not be blocked then. Do not use such variables as blocking literals, or re-add the removed clauses before the new ones.
- **Learned clauses.** Check the blocking condition against every clause the solver keeps, including learned clauses, or delete the learned clauses that contain $\neg l$.
- **Order of reconstruction.** The stack must be processed from the last removed clause to the first. Processing it in the other order can give an assignment that falsifies a removed clause.
- **Variables not in the reduced formula.** RECONSTRUCT needs a value for every variable of the original formula, including those that vanished; give them any value first.

## Exercises

1. Show that a clause can be blocked in $F$ and not blocked in $F \cup \{D\}$ for one more clause $D$, and use this to explain the "Frozen variables" pitfall.
2. Prove that BCE on the Tseitin encoding of a circuit whose output is asserted true removes the clause $(y \vee \neg a \vee \neg b)$ of each AND gate $y$ that occurs only in positive polarity. Use the polarity definition of the Plaisted-Greenbaum transformation.
3. Give a formula where BCE removes a clause and the reduced formula has more models than the original, and one where it has fewer.

## References
