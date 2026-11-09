---
tag: 69AYK4
kind: technique
slug: model-based-theory-combination
name: Model-based theory combination
aliases:
- MBTC
- model-based combination
- model-based equality propagation
area: logic-and-constraints/smt
level: research
summary: Each theory solver keeps a candidate model. Equalities between shared terms that hold in a model are tried as decisions, and the formula is satisfiable when all models agree.
prereqs: [nelson-oppen, cdcl-t]
see_also: [shostak-combination, stable-infiniteness, convex-theory, euf-satisfiability, linear-integer-arithmetic-satisfiability, quantifier-instantiation, theory-propagation, lazy-smt]
sources:
  - paper: doi:10.1016/j.entcs.2008.04.079
    title: Leonardo de Moura and Nikolaj Bjørner, Model-based theory combination, Electronic Notes in Theoretical Computer Science 198(2), 2008, pages 37 to 49 (SMT workshop 2007)
    locator: the combination that incrementally reconciles the models maintained by each theory, and its evaluation in Z3
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.6.1 (arrangements and Proposition 33.6.2), Section 33.6.2 (entailed disjunctions of equalities, NP-complete for difference logic), Section 33.6.3 (delayed theory combination and the model-driven search on interface equalities)
  - paper: doi:10.1007/11513988_34
    title: Marco Bozzano, Roberto Bruttomesso, Alessandro Cimatti, Tommi Junttila, Peter van Rossum, Silvio Ranise and Roberto Sebastiani, Efficient satisfiability modulo theories via delayed theory combination, CAV 2005, LNCS 3576, pages 335 to 349
    locator: the interface equalities as Boolean atoms decided by the SAT engine
  - paper: doi:10.1007/978-3-540-78800-3_24
    title: Leonardo de Moura and Nikolaj Bjørner, Z3, an efficient SMT solver, TACAS 2008, LNCS 4963, pages 337 to 340
    locator: the architecture of Z3, in which theory solvers are combined
  - paper: doi:10.1007/978-3-642-02658-4_25
    title: Yeting Ge and Leonardo de Moura, Complete instantiation for quantified formulas in satisfiability modulo theories, CAV 2009, LNCS 5643, pages 306 to 320
    locator: model-based quantifier instantiation, which checks quantified formulas against a candidate model
  - paper: doi:10.1145/357073.357079
    title: Greg Nelson and Derek C. Oppen, Simplification by cooperating decision procedures, ACM Transactions on Programming Languages and Systems 1(2), 1979, pages 245 to 257
    locator: the exchange of equalities between shared variables, which model-based combination replaces
---

Model-based theory combination is a way to combine the solvers of two theories inside a [CDCL(T)](/cdcl-t/) solver. As in [Nelson-Oppen](/nelson-oppen/), the theories share only some terms, and the combination must make the solvers agree on which shared terms are equal. Nelson-Oppen asks each solver for all the equalities, or disjunctions of equalities, that its literals *entail*. For non-convex theories such as integer arithmetic this is expensive. Model-based combination asks for less. Each solver keeps a *candidate model* of its literals, which it usually has anyway. If two shared terms are equal in one model but the equality is not yet assigned, the combination adds the equality as a new atom and lets the SAT engine *decide* it, with the value true taken from the model. If the guess is wrong, conflict analysis learns a clause and the search goes on. When all models agree on the equalities between the shared terms, the formula is satisfiable. Leonardo de Moura and Nikolaj Bjørner introduced the method in the Z3 solver in 2007. It needs the same conditions as Nelson-Oppen: disjoint signatures and [stably infinite](/stable-infiniteness/) theories.

## In plain words

Two experts each hold part of the clues, and some names appear in both parts. Each expert has already found one way to make their own clues true, a candidate answer.

Compare the two answers on the shared names only. If they agree on which names stand for the same thing, the two answers can be glued together, and the puzzle is solved.

If one expert's answer makes two names equal, but nobody has said that they must be equal, take a guess: "assume these two are equal". Tell both experts. If the other expert now finds a contradiction, the guess was wrong. Write down "these two are not equal" and try again.

The experts never have to work out everything that their clues force. They only show one answer each, and the guesses fix the differences.

## When it applies

- The formula mixes theories with disjoint signatures, such as uninterpreted functions with integer or real arithmetic, and the theories are stably infinite.
- The solver is a [lazy](/lazy-smt/) CDCL(T) solver, which can add new atoms during the search and decide them.
- Each theory solver can give a model of its literals cheaply when they are consistent. [Congruence closure](/congruence-closure/) gives one value per class. The simplex method gives its current assignment.
- Computing entailed equalities is costly, or the theory is not [convex](/convex-theory/). For the difference logic fragment of integer arithmetic, deciding whether a conjunction entails a disjunction of equalities is NP-complete, even though conjunctions are decided in polynomial time (Handbook, Section 33.6.2).

## The template

The step runs as the *final check* of a CDCL(T) solver: every atom of the formula has a value, and each theory solver has found its own literals consistent. The shared terms are the terms that occur in literals of both theories, or the shared variables after purification.

```pseudo id=main
FINAL-CHECK(μ)                    ▷ μ: a full assignment, consistent in each theory alone
L1  for each theory i: Mi ← a model of the Ti-literals of μ         ▷ hole: how the solver builds and adjusts its model
L2  for each pair of shared terms x, y                              ▷ hole: which pairs first, for example by grouping equal values
L3      if the atom x = y has no value in μ and Mi(x) = Mi(y) for some i:
L4          add x = y as a new atom, given to both theory solvers
L5          decide x = y with the value true                        ▷ hole: the phase, true from the model, or false
L6          return CONTINUE                                         ▷ the CDCL(T) search goes on
L7  return SAT                                                      ▷ all models induce the same arrangement
```

When an assigned equality $x = y$ makes a theory inconsistent, the theory solver reports a conflict that contains it. The SAT engine learns a clause, backjumps, and usually propagates $x \ne y$. Then each solver must find a new model that respects the disequality.

**Why SAT is correct.** At line L7, consider any pair of shared terms $x, y$. If $x = y$ is true in $\mu$, both theories received it, so it holds in every model. If it is false in $\mu$, it is false in every model. If it has no value, line L3 shows that $x$ and $y$ are different in every model. So all the models induce the same equivalence relation $R$ on the shared terms, and each model satisfies its own literals together with $\mathrm{ar}_R$, the equalities and disequalities of $R$. By the Nelson-Oppen theorem for stably infinite theories with disjoint signatures (Handbook, Proposition 33.6.2), the literals of $\mu$ are satisfiable in the combined theory.

**Why it terminates.** Each call adds at most one atom, and there are only finitely many pairs of shared terms, so at most $k(k-1)/2$ atoms are added for $k$ shared terms. The CDCL(T) search over a finite set of atoms terminates.

### A worked example

Take the formula from the [Nelson-Oppen page](/nelson-oppen/), over the integers:
$$1 \le x \ \wedge\ x \le 2 \ \wedge\ f(x) \ne f(1) \ \wedge\ f(x) \ne f(2).$$
Purification names $1$ as $v_0$ and $2$ as $v_1$ in the EUF part. The shared terms are $x, v_0, v_1$. The EUF solver has the literals $f(x) \ne f(v_0)$ and $f(x) \ne f(v_1)$, and the arithmetic solver has $1 \le x,\ x \le 2,\ v_0 = 1,\ v_1 = 2$.

1. Both parts are consistent. Assume that the arithmetic model puts $x$ at its lower bound: $x = 1$, $v_0 = 1$, $v_1 = 2$. The EUF model puts $x$, $v_0$ and $v_1$ in three different classes.
2. The pair $x, v_0$ is equal in the arithmetic model, and $x = v_0$ has no value. The final check adds the atom and decides it true.
3. The EUF solver now derives $f(x) = f(v_0)$ by congruence, which contradicts $f(x) \ne f(v_0)$. The conflict is $\{x = v_0,\ f(x) \ne f(v_0)\}$. The SAT engine learns $x \ne v_0 \vee f(x) = f(v_0)$, backjumps, and propagates $x \ne v_0$.
4. The arithmetic solver must now respect $x \ne v_0$. Its new model is $x = 2$. The pair $x, v_1$ is equal in it, so the final check decides $x = v_1$ true. The same conflict pattern gives the learned clause $x \ne v_1 \vee f(x) = f(v_1)$, and $x \ne v_1$ is propagated.
5. The arithmetic literals are now $1 \le x \le 2,\ x \ne 1,\ x \ne 2$, which have no integer solution. The arithmetic solver reports a conflict at decision level 0, and the answer is UNSAT.

Only two interface atoms were created, both suggested by a model. The solvers never computed the disjunction $x = v_0 \vee x = v_1$ that the integer part entails. Over the rationals, step 5 is different: the arithmetic solver finds the model $x = 3/2$, no pair of shared terms is equal in any model, and line L7 answers SAT.

## Classic examples

- **EUF with integer arithmetic.** This is the setting in Z3 for which de Moura and Bjørner designed the method. EUF is convex, so congruence closure cheaply reports its entailed equalities; the arithmetic side is not convex, and its equalities come from the model. See [EUF satisfiability](/euf-satisfiability/) and [linear integer arithmetic satisfiability](/linear-integer-arithmetic-satisfiability/).
- **EUF with real arithmetic.** The [simplex method for SMT](/simplex-for-smt/) keeps an assignment that satisfies the current bounds, so it has a model at all times. Real arithmetic is convex, but finding all entailed equalities still costs extra simplex work. The model gives candidates for free. See [linear real arithmetic satisfiability](/linear-real-arithmetic-satisfiability/).
- **The same pattern for quantifiers.** Model-based [quantifier instantiation](/quantifier-instantiation/) (Ge and de Moura, 2009) builds a candidate model of the ground part, checks the quantified formulas against it, and adds an instance only where the model fails. Like model-based combination, it uses a candidate model to choose the next piece of work, and it learns from each failure.
- **The general guess, check and refine loop.** The method is an instance of the loop of [CEGAR](/cegar/) and [CEGIS](/cegis/): propose a candidate, check it, and learn from a counterexample. Here the candidate is an arrangement of the shared terms.

## Variations

- **Delayed theory combination.** Bozzano and others (2005) let the SAT engine assign *every* interface equality, whether a model suggests it or not. The theory solvers need no deduction at all, but the search can branch on up to $k(k-1)/2$ new atoms. Model-based combination creates only the atoms that some model suggests.
- **Interface equalities on demand.** The Handbook credits Dutertre and de Moura (Yices, 2006) with creating interface equalities only when they are needed, and de Moura and Bjørner (2007) with letting a model under construction drive the Boolean search on them (Section 33.6.3).
- **Mixed propagation.** A solver that can find entailed equalities cheaply, such as congruence closure, can still propagate them as in deterministic Nelson-Oppen. The model is used only for the theories where entailment is costly.
- **The phase of the decision.** Deciding $x = y$ true follows the model and tends to keep the current models valid. Deciding it false avoids the merge, but then the solver whose model had $x = y$ must change its model.
- **Many-sorted and non-stably infinite theories.** For theories with finite sorts, such as bit-vectors, agreement on equalities is not enough. The models must also agree on the sizes of the shared sorts, as in the combinations of Tinelli and Zarba.

## Pitfalls

- **Accidental equalities.** The simplex method keeps many variables at their bounds, so many shared terms get equal values by chance. Each one becomes a decision, and often a conflict. A solver can reduce this by moving variables to distinct values when the bounds allow it.
- **Missing a pair at the final check.** Line L7 is correct only if no unassigned pair of shared terms is equal in any model. A check that looks only at some pairs can answer SAT on an unsatisfiable formula. Grouping the shared terms by value, with a hash table per model, finds all equal pairs in time linear in $k$ plus the number of pairs found.
- **Models that ignore disequalities.** After $x \ne y$ is learned, each solver must give a model with different values for $x$ and $y$. For integer arithmetic this needs case splits, such as $x < y \vee x > y$, inside the solver or by splitting on demand.
- **The conditions of Nelson-Oppen.** The method relies on the Nelson-Oppen theorem, so it is incomplete for theories that are not stably infinite, and it does not apply when the signatures share function symbols.
- **Many new atoms.** In the worst case every pair of shared terms gets an atom, as in delayed theory combination. Solvers that keep these atoms forever can grow large on formulas with many shared terms.

## Exercises

1. In the worked example, the arithmetic model first puts $x$ at its upper bound, $x = 2$. Give the run, and show that it again creates two interface atoms.
2. Give a formula over EUF and real arithmetic in which the simplex model has an accidental equality between two shared terms, the decision on it leads to a conflict, and a model with distinct values would have avoided the conflict.
3. Combine EUF with a theory whose models have at most two elements (see [stable infiniteness](/stable-infiniteness/)). Give a formula on which the final check returns SAT although the formula is unsatisfiable in the combination.
4. Show that the correctness argument still holds if line L5 decides $x = y$ false instead of true. What changes in the run of the worked example?

## References
