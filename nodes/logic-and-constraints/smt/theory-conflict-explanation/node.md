---
tag: RE5MKX
kind: concept
slug: theory-conflict-explanation
name: Theory conflict explanation
aliases:
- theory lemma
- conflict clause from theory
- theory conflict set
- T-conflict clause
- explanation
area: logic-and-constraints/smt
level: advanced
summary: A subset of the current theory literals that is already inconsistent in the theory, returned by the theory solver so that its negation can be learned as a clause. Smaller explanations prune more.
prereqs: [dpll-t, smt-problem]
see_also: [cdcl-t, theory-propagation, lazy-smt, congruence-closure, difference-logic-satisfiability, unsat-core, minimal-unsatisfiable-subset, clause-learning]
sources:
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.4.1 (conflict set generation as a feature of theory solvers), Section 33.4.3.5 (T-backjumping and T-learning, theory and mixed conflict sets, Example 33.4.2)
  - paper: doi:10.1145/1217856.1217859
    title: Robert Nieuwenhuis, Albert Oliveras and Cesare Tinelli, Solving SAT and SAT Modulo Theories, from an abstract Davis-Putnam-Logemann-Loveland procedure to DPLL(T), Journal of the ACM 53(6), 2006, pages 937 to 977
    locator: the T-Learn and T-Backjump rules, and explanations of theory propagations
  - paper: doi:10.1007/978-3-540-32033-3_33
    title: Robert Nieuwenhuis and Albert Oliveras, Proof-producing congruence closure, RTA 2005, LNCS 3467, pages 453 to 468
    locator: the proof forest and the Explain operation for EUF
  - paper: doi:10.1007/s10703-017-0283-x
    title: Andreas Fellner, Pascal Fontaine and Bruno Woltzenlogel Paleo, NP-completeness of small conflict set generation for congruence closure, Formal Methods in System Design 51(3), 2017, pages 533 to 544
    locator: a smallest conflict set for congruence closure is NP-hard to find
  - paper: doi:10.1007/11814948_19
    title: Scott Cotton and Oded Maler, Fast and flexible difference constraint propagation for DPLL(T), SAT 2006, LNCS 4121, pages 170 to 183
    locator: negative cycles as explanations in difference logic
  - paper: doi:10.1007/11817963_11
    title: Bruno Dutertre and Leonardo de Moura, A fast linear-arithmetic solver for DPLL(T), CAV 2006, LNCS 4144, pages 81 to 94
    locator: explanations from a simplex row whose bounds cannot be met
---

When a theory solver finds that the theory literals $\mu$ of the current assignment cannot hold together, it returns a *theory conflict set*: a subset $\eta \subseteq \mu$ that is already inconsistent in the theory $T$. The negation $\neg \eta$, a disjunction of the negated literals, is $T$-valid. As a clause over the [Boolean abstraction](/boolean-abstraction/) it is called a *theory lemma* or *T-conflict clause*, and the SAT part learns it and backjumps, as it does for a Boolean conflict. In the same way, a literal that the solver derives by [theory propagation](/theory-propagation/) is explained by a set $\eta$ with $\eta \models_T l$, and the clause $\neg \eta \vee l$ is its reason. In each case the explanation is a certificate that the theory reasoning was correct, and the quality of the solver depends on how small it is.

## In plain words

When the theory expert rejects a list of facts, a plain "no" is not much help. The solver would learn only that this exact list is wrong, and it would try almost the same list next time.

A good expert points at the few facts that clash. "x is less than y, y is less than z, z is less than x: these three cannot all hold." The solver writes down the rule "not all three", and that rule rules out every future list that has these three facts in it, whatever else the list says.

So a short explanation removes many wrong answers at once. The shortest one is not always easy to find, so solvers give a short one that is cheap to find.

## The idea

**Three objects.** Let $\mu$ be the theory literals of the current assignment.

- A *conflict set* is a subset $\eta \subseteq \mu$ that is $T$-unsatisfiable.
- The *theory lemma* is the clause $\neg \eta$. It is $T$-valid, so adding it to the formula does not change its $T$-models.
- The *explanation* of a propagated literal $l$ is a set $\eta \subseteq \mu$ with $\eta \models_T l$. Its clause $\neg \eta \vee l$ is also $T$-valid.

**Size.** The set $\mu$ itself is always a conflict set when $\mu$ is inconsistent. It is the trivial explanation, and it excludes only the one assignment. A conflict set is *minimal* when no proper subset is a conflict set. A *smallest* conflict set has the least number of literals. Every smallest conflict set is minimal, but a minimal one need not be smallest. For EUF, finding a smallest conflict set is NP-hard (Fellner, Fontaine and Woltzenlogel Paleo, 2017), so solvers aim for small sets, not for the smallest.

**Where they come from.** Each solver keeps enough history to name the input literals behind each derived fact. For EUF, [congruence closure](/congruence-closure/) keeps a *proof forest*: each edge is an input equality or a congruence step, and the explanation of $s = t$ collects the input labels on the path from $s$ to $t$, opening each congruence step into the explanations of its arguments. For [difference logic](/difference-logic-satisfiability/), the explanation is a negative cycle of the constraint graph. For linear real arithmetic with [simplex](/simplex-for-smt/), it is the bounds that appear in a row whose basic variable cannot be fixed. The multipliers of that row are a Farkas certificate.

**How the SAT part uses them.** The lemma $\neg \eta$ is false under the current assignment, so it is a conflict clause. Conflict analysis can learn it as it is, or resolve it with the reasons in the [implication graph](/implication-graph/) until it reaches the [first UIP](/first-uip/). The result is then a *mixed* Boolean and theory conflict clause, which is not $T$-valid alone but is a $T$-consequence of the formula (Handbook, Section 33.4.3.5). See [CDCL(T)](/cdcl-t/).

**Not the same as an unsat core.** A conflict set is a set of *literals* found inside one theory check. An [unsat core](/unsat-core/) is a set of input *assertions* whose conjunction is unsatisfiable. The solver builds cores from the clauses, including theory lemmas, that the final refutation uses.

## Examples

All the claims in this section were checked by a script: each explanation is unsatisfiable by brute force, and where it is called minimal, the removal of any one literal makes it satisfiable.

**EUF, minimal.** For $\mu = \{a = b,\ b = c,\ c = d,\ d = e,\ f(a) \ne f(c)\}$, congruence closure finds $f(a) = f(c)$ and returns $\eta = \{a = b,\ b = c,\ f(a) \ne f(c)\}$. It is a conflict, and it is minimal. The lemma is $a \ne b \vee b \ne c \vee f(a) = f(c)$, and it ignores $c = d$ and $d = e$.

**EUF, not minimal.** Take the equalities $f(a) = b$ and $b = a$, asserted in this order, and the disequality $f(f(a)) \ne f(f(b))$. The proof forest explanation contains both equalities. But $b = a$ alone already gives $f(a) = f(b)$ and then $f(f(a)) = f(f(b))$, so $\{b = a,\ f(f(a)) \ne f(f(b))\}$ is a smaller conflict set. With the two equalities in the other order, the same code returns the minimal set. On 1242 conflicts from random EUF problems, 91 of the proof forest explanations were not minimal.

**Difference logic, minimal.** For $\{x - y \le 2,\ y - z \le 3,\ z - x \le -6,\ w - x \le 0\}$, the constraint graph has the cycle $x, y, z$ with weight $2 + 3 - 6 = -1 < 0$, and the conflict set is these three constraints. A simple negative cycle is always a minimal conflict, because the removal of any one edge leaves no cycle among the rest, and a set of difference constraints is unsatisfiable exactly when its graph has a negative cycle. The script confirmed this on 152 random cycles.

**Linear real arithmetic.** For $\{x + y \le 1,\ x \ge 1,\ y \ge 1\}$, the sum with multipliers $1, 1, 1$ gives $0 \le -1$. The three bounds are the conflict set, and the multipliers are its Farkas certificate.

## Where it is used

- **[DPLL(T)](/dpll-t/) and [CDCL(T)](/cdcl-t/).** Theory lemmas drive T-learning and T-backjumping, and explanations are the reasons of theory-propagated literals.
- **The [lazy approach](/lazy-smt/).** In the offline loop, the lemma is the blocking clause, and a small one cuts the number of SAT calls from exponential to a few.
- **[Unsat cores](/unsat-core/) and proofs.** The lemmas are the theory steps of the refutation, and a proof checker checks each one in the theory.
- **Interpolation.** Interpolating solvers need the explanation to be split by the two parts of the input, and they compute partial interpolants for each theory lemma.
- **Constraint programming.** Lazy clause generation uses the same idea for propagators over finite domains.

## References
