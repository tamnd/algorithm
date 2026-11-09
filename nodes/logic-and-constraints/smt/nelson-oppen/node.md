---
tag: P1JJQX
kind: algorithm
slug: nelson-oppen
name: Nelson-Oppen combination method
aliases:
- Nelson-Oppen procedure
- Nelson-Oppen
- Nelson-Oppen theory combination
- equality propagation
area: logic-and-constraints/smt
level: advanced
summary: Combines decision procedures for two theories with disjoint signatures. The solvers exchange equalities between shared variables. It is complete when both theories are stably infinite.
solves: [smt-problem]
model: word-ram
complexity:
  vars: {k: the number of shared variables after purification, t: the time of one call of a theory solver, n: the number of literals after purification}
  time: {worst: O(k^(2k+1) t)}
  space: {extra: O(k (n + k))}
properties: {deterministic: true, recursive: true}
history:
  year: 1979
  people: [Greg Nelson, Derek C. Oppen]
  note: Nelson and Oppen published the method in ACM TOPLAS in 1979. Their completeness proof missed the need for stable infiniteness. Oppen gave the first correct proof, and the role of convexity, in 1980.
prereqs: [smt-problem, congruence-closure, stable-infiniteness, convex-theory]
see_also: [shostak-combination, model-based-theory-combination, dpll-t, ackermannization, euf-satisfiability, linear-integer-arithmetic-satisfiability, decision-procedure, cdcl-t]
sources:
  - paper: doi:10.1145/357073.357079
    title: Greg Nelson and Derek C. Oppen, Simplification by cooperating decision procedures, ACM Transactions on Programming Languages and Systems 1(2), 1979, pages 245 to 257
    locator: the combination method, the propagation of equalities between shared variables, and case splits for non-convex theories
  - paper: doi:10.1016/0304-3975(80)90059-6
    title: Derek C. Oppen, Complexity, convexity and combinations of theories, Theoretical Computer Science 12(3), 1980, pages 291 to 302
    locator: the first correct completeness proof, convex theories, and the complexity of combinations
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.6.1 (purification, arrangements, the combination procedure, Proposition 33.6.2 and the error in the 1979 proof), Section 33.6.2 (the deterministic procedure, convex and non-convex theories), Section 33.6.3 (delayed theory combination, Example 33.6.3)
  - paper: doi:10.1007/978-94-009-0349-4_5
    title: Cesare Tinelli and Mehdi T. Harandi, A new correctness proof of the Nelson-Oppen combination procedure, Frontiers of Combining Systems (FroCoS 1996), Applied Logic Series 3, Kluwer, 1996, pages 103 to 119
    locator: the model-theoretic proof with arrangements of the shared variables
  - paper: doi:10.1007/s10817-005-5204-9
    title: Cesare Tinelli and Calogero G. Zarba, Combining nonstably infinite theories, Journal of Automated Reasoning 34(3), 2005, pages 209 to 238
    locator: the incompleteness of the method without stable infiniteness, and the combination with shiny theories
  - paper: doi:10.1007/11513988_34
    title: Marco Bozzano, Roberto Bruttomesso, Alessandro Cimatti, Tommi Junttila, Peter van Rossum, Silvio Ranise and Roberto Sebastiani, Efficient satisfiability modulo theories via delayed theory combination, CAV 2005, LNCS 3576, pages 335 to 349
    locator: delayed theory combination, the interface equalities decided by the SAT engine
  - paper: doi:10.1007/978-3-540-74113-8_10
    title: Aaron R. Bradley and Zohar Manna, Combining decision procedures, Chapter 10 of The Calculus of Computation, Springer, 2007, pages 269 to 289
    locator: the nondeterministic and deterministic versions, with examples over EUF and integer arithmetic
---

The Nelson-Oppen method decides satisfiability in a combination of two theories, such as equality with uninterpreted functions together with integer arithmetic, from decision procedures for each theory alone. It first *purifies* the formula: each subterm that belongs to the other theory gets a fresh variable, so that every literal belongs to one theory. The two parts then share only variables. The solvers exchange equalities between these shared variables until one of them finds a contradiction or there is nothing left to exchange. The method needs the two signatures to be disjoint, and it is complete only when both theories are [stably infinite](/stable-infiniteness/). For [convex](/convex-theory/) theories, the exchange of single equalities is enough. For non-convex theories, such as integer arithmetic, a solver can entail a disjunction of equalities without entailing any one of them, and the method must split cases. Greg Nelson and Derek Oppen published it in 1979. It is the base of theory combination in every SMT solver, mostly in the forms of [delayed theory combination](#variants-and-improvements) and [model-based theory combination](/model-based-theory-combination/).

## In plain words

Two experts look at the same puzzle. One knows only about functions, the other only about numbers. Each gets the clues of their own field.

The clues share some names. The method lets the experts talk only about these names, and only in one way: "I am sure that these two names are the same thing."

The number expert says "x and y must be equal". The function expert writes it down, and now sees that f(x) and f(y) must also be equal. The number expert hears this, and learns something new again. They go back and forth.

If one expert finds that the clues cannot all hold, there is no solution. If nobody has anything new to say, there is a solution. The second part is true only when no expert's field forces a small, finite world.

## The problem

Let $T_1$ be a $\Sigma_1$-theory and $T_2$ a $\Sigma_2$-theory, where the signatures $\Sigma_1$ and $\Sigma_2$ share no symbol except equality. Each $T_i$ has a decision procedure for conjunctions of ground literals. The input is a conjunction $\varphi$ of ground literals over $\Sigma_1 \cup \Sigma_2$ and free constants. The question is whether $\varphi$ is satisfiable in the combined theory $T_1 \oplus T_2$, whose models are the structures that are models of $T_1$ and of $T_2$ at the same time. Arbitrary Boolean structure is handled by a SAT engine on top, as in [DPLL(T)](/dpll-t/), so it is enough to treat conjunctions.

**Purification.** Replace each *alien* subterm, a term of one theory that occurs as an argument in the other, with a fresh constant $v$, and add the equation $v = t$. Then split the literals into $\varphi_1$, over $\Sigma_1$, and $\varphi_2$, over $\Sigma_2$. For example, $f(x) \le z$ becomes $v_0 \le z$ in the arithmetic part and $v_0 = f(x)$ in the EUF part. The result is equisatisfiable with $\varphi$ and has linear size (Handbook, Section 33.6.1). The *shared* constants are those that occur in both parts. An equality between two constants may go to either part, or to both.

**Arrangements.** An *arrangement* of the shared constants is an equivalence relation $R$ on them, written as the formula $\mathrm{ar}_R$ with $c = d$ for each pair in $R$ and $c \ne d$ for each pair not in $R$.

## The algorithm

**The nondeterministic form.** Guess an arrangement $R$ of the shared constants, and answer SAT if both $\varphi_1 \wedge \mathrm{ar}_R$ and $\varphi_2 \wedge \mathrm{ar}_R$ are satisfiable in their theories; answer UNSAT if no arrangement works. This is the form in which the theorem is stated and proved (Handbook, Proposition 33.6.2).

**The deterministic form.** The pseudocode below computes the same answer without guessing. Each solver reports the equalities between shared constants that its part entails, and the other part receives them (lines L4 and L5). When nothing is left to send, the two parts entail the same equivalence relation $R$. For convex theories this is the end: the answer is SAT. For non-convex theories, one part may still entail a disjunction of equalities that $R$ does not contain, and the procedure splits on its disjuncts (lines L8 to L10).

```pseudo id=main
NELSON-OPPEN(φ1, φ2)               ▷ φi: a conjunction of pure Ti-literals
L1  S ← the constants that occur in both φ1 and φ2
L2  loop
L3      if φ1 is T1-unsatisfiable or φ2 is T2-unsatisfiable: return UNSAT
L4      if for some i and some c, d ∈ S: φi ⊨Ti c = d, but not φj ⊨Tj c = d (j ≠ i):
L5          add c = d to φj; continue the loop
L6      R ← the equivalence relation {(c, d) : φ1 ⊨T1 c = d} on S, with one member chosen per class
L7      D ← the equalities between the chosen members of two different classes of R
L8      if D is not empty and φi ∧ ar_R is Ti-unsatisfiable for some i:       ▷ never for convex theories
L9          for each equality e in D: if NELSON-OPPEN(φ1 ∧ e, φ2 ∧ e) = SAT: return SAT
L10         return UNSAT
L11     return SAT
```

The implementation decides an entailment $\varphi_i \models_{T_i} c = d$ by one call of the solver on $\varphi_i \wedge c \ne d$. Real solvers get the entailed equalities more cheaply: congruence closure reads them from its classes, and the simplex method from the equal values of its bounds. The test at line L8 asks whether $\varphi_i$ entails the disjunction of $D$, because the equalities of $\mathrm{ar}_R$ are already entailed.

## Example

**Convex theories: EUF and the order of the rationals.** Take
$$x \le y \ \wedge\ y \le x \ \wedge\ f(x) \le z \ \wedge\ z \le f(y) \ \wedge\ g(z) \ne g(f(x)).$$
Purification names $f(x)$ as $v_0$ and $f(y)$ as $v_1$. The EUF part is $v_0 = f(x),\ v_1 = f(y),\ g(z) \ne g(f(x))$, and the order part is $x \le y,\ y \le x,\ v_0 \le z,\ z \le v_1$. The shared constants are $v_0, v_1, x, y, z$.

| pass | sender | equality sent | reason |
|---|---|---|---|
| 1 | order | $x = y$ | $x \le y$ and $y \le x$ |
| 2 | EUF | $v_0 = v_1$ | congruence: $f(x) = f(y)$ |
| 3 | order | $v_0 = z$ | $v_0 \le z \le v_1 = v_0$ |
| 4 | EUF | none | $g(z) = g(v_0) = g(f(x))$ contradicts the disequality: UNSAT at line L3 |

Neither solver could find the contradiction alone, and three equalities were enough. The answer is the same over the integers. The implementation gives this run, with three sent equalities and no split.

**A non-convex theory: EUF and the order of the integers.** Take
$$1 \le x \ \wedge\ x \le 2 \ \wedge\ f(x) \ne f(1) \ \wedge\ f(x) \ne f(2).$$
Purification names $1$ as $v_0$ and $2$ as $v_1$ in the EUF part. The EUF part is $f(x) \ne f(v_0),\ f(x) \ne f(v_1)$, the integer part is $1 \le x,\ x \le 2,\ v_0 = 1,\ v_1 = 2$, and the shared constants are $v_0, v_1, x$.

- No single equality is entailed. The integer part entails $x = v_0 \vee x = v_1$, but neither disjunct. The EUF part entails nothing.
- At line L6, $R$ has the three classes $\{v_0\}$, $\{v_1\}$, $\{x\}$. The integer part with $v_0 \ne v_1,\ v_0 \ne x,\ v_1 \ne x$ is unsatisfiable, because $x$ would have to be an integer in $[1, 2]$ other than 1 and 2. So line L8 splits.
- The branch $v_0 = v_1$ fails in the integer part ($1 = 2$). The branches $v_0 = x$ and $v_1 = x$ fail in the EUF part, by congruence.

The answer is UNSAT. Without lines L8 to L10, the procedure would answer SAT, which is wrong; this is why convexity matters. Over the rationals the same formula is satisfiable with $x = 3/2$, and all versions answer SAT.

**Without stable infiniteness.** Let $T_2$ be the theory with the axiom $\forall x\, y\, z.\ x = y \vee x = z \vee y = z$, whose models have at most two elements. The EUF formula $f(a) \ne f(b) \wedge f(a) \ne f(c) \wedge f(b) \ne f(c)$ shares no constant with the empty $T_2$ part. Both parts are satisfiable, so the method answers SAT. But no model has two elements and three distinct values, so the formula is unsatisfiable in the combination. $T_2$ is not stably infinite.

## Correctness

The core is the theorem of Nelson and Oppen in its corrected form (Oppen, 1980; Handbook, Proposition 33.6.2): *if $T_1$ and $T_2$ have disjoint signatures and are stably infinite, then $\varphi_1 \wedge \varphi_2$ is satisfiable in $T_1 \oplus T_2$ exactly when some arrangement $R$ makes both $\varphi_1 \wedge \mathrm{ar}_R$ and $\varphi_2 \wedge \mathrm{ar}_R$ satisfiable.* For the hard direction, take a model of each part. By stable infiniteness and the Löwenheim-Skolem theorem, both can be taken countably infinite. Both satisfy the same arrangement, so a bijection between the two universes can map the value of each shared constant in one to its value in the other. Moving the first model along this bijection gives one structure that is a model of both theories and of both parts. The signatures are disjoint, so the two interpretations do not clash.

The proof page also proves three more facts.

- **The counterexample.** The example with at most two elements above shows that the theorem fails without stable infiniteness. The 1979 paper stated completeness for any two signature-disjoint theories; the Handbook notes that its proof assumed, without saying so, that only infinite models matter.
- **The deterministic form for convex theories.** If no single equality is left to send, both parts entail the same relation $R$. If $\varphi_i \wedge \mathrm{ar}_R$ were unsatisfiable, $\varphi_i$ would entail the disjunction of the equalities outside $R$, and by convexity one of them, which contradicts the definition of $R$. So the answer SAT is correct. Each sent equality joins two classes on the receiving side, so at most $2(k - 1)$ equalities are sent.
- **The form with splits.** Every model of the input satisfies one equality of $D$ when line L8 finds an unsatisfiable side, so the split is exact. Each branch joins two classes of $R$, so the recursion has depth at most $k - 1$.

The full proofs are in the [proof page](proofs/correctness.md).

**Tests.** The implementation combines EUF, by congruence closure, with the order of the integers or of the rationals, with integer constants. It was compared with brute force on 400 random integer formulas and 250 random rational formulas. Brute force looks for values of the variables and of the function applications, with equal arguments giving equal values. A bounded domain suffices: a strictly increasing map that fixes the constants $0, \ldots, K$ and closes up the gaps between the other values keeps every literal true and keeps functions consistent, so a formula with $m$ free subterms has a model with values in $[-m, K + m]$; over the rationals without constants, the ranks $0, \ldots, m - 1$ do the same. The procedure with splits and the nondeterministic one agreed with brute force on all formulas. Over the rationals no split was ever needed, as convexity predicts. Over the integers the procedure split on 4 formulas, and the version without splits answered SAT on one unsatisfiable formula. The tests also check the counterexample with at most two elements against brute force over two values.

## Complexity

Let $k$ be the number of shared constants and $t$ the time of one solver call.

- **Convex theories.** At most $2k - 1$ passes of the loop, each with $O(k^2)$ entailment checks, so $O(k^3)$ solver calls and $O(k^3 t)$ time. If both theories have polynomial-time solvers, so does the combination. Real solvers find the entailed equalities as a side effect of the satisfiability check, which removes most of these calls; for EUF they come from the classes of [congruence closure](/congruence-closure/).
- **Non-convex theories.** Each split has fewer than $k^2$ branches, and the recursion depth is at most $k - 1$, so there are at most $O(k^{2k - 2})$ calls of the procedure, each with $O(k^3)$ solver calls: $O(k^{2k+1} t)$ in the worst case. The nondeterministic form tries at most the Bell number $B_k \le k^k$ of arrangements, with two solver calls each.
- The exponential factor is not an artifact. For the difference logic fragment of integer arithmetic, conjunctions are decidable in polynomial time, but deciding whether a conjunction entails a disjunction of equalities is NP-complete (Handbook, Section 33.6.2, citing Lahiri and Musuvathi).

The space is that of the recursion: at most $k$ levels, each with a copy of the two parts, $O(k (n + k))$, where $n$ is the number of literals after purification.

## Properties

- **Modular.** Each theory solver is used as a black box. Only satisfiability checks of conjunctions, or entailed equalities, are needed.
- **Exchanges only equalities.** Nothing but equalities and disequalities between shared constants passes between the solvers. This is what the theorem shows to be enough for stably infinite theories.
- **Deterministic for convex theories.** No case split is ever needed when both theories are convex.
- **Restricted.** The signatures must be disjoint: two theories that both interpret $+$ cannot be combined this way. And both theories must be stably infinite.

## Variants and improvements

- **No purification.** Solvers can treat alien subterms as free constants, and exchange equalities between these terms instead of between fresh names. The Handbook notes that this was known to the early implementers, and Barrett, Dill and Stump describe the method in this form.
- **Delayed theory combination.** Bozzano and others (2005) let the SAT engine of a [lazy](/lazy-smt/) solver decide the *interface equalities* $c = d$ between shared constants, as extra Boolean atoms. The theory solvers do not need to deduce equalities at all; better solvers save Boolean search. Splits become ordinary decisions, and conflicts on interface equalities are learned as clauses.
- **[Model-based theory combination](/model-based-theory-combination/).** De Moura and Bjørner let each solver build a candidate model and propose the equalities that hold in it, and the SAT engine checks them. This avoids the computation of entailed disjunctions, and it is the method of Z3.
- **[Shostak's method](/shostak-combination/).** For theories with a canonizer and a solver, such as linear arithmetic, one data structure handles the equalities of all the theories. Its correct form, by Rueß and Shankar, uses Nelson-Oppen to add other theories.
- **Non-stably infinite theories.** Tinelli and Zarba combine any theory with a *shiny* one, exchanging cardinality constraints as well. Ranise, Ringeissen and Zarba do the same for *polite* theories in many-sorted logic, the setting of SMT-LIB, where the condition is needed only for the shared sorts.
- **More than two theories.** The method extends to $n$ theories by pairs, or by exchanging equalities among all solvers at once.
- **[Ackermannization](/ackermannization/).** For EUF together with one other theory, the function symbols can be removed before solving, and no combination is needed. Bruttomesso and others compared this with delayed theory combination.

## When to use it

Use Nelson-Oppen, in one of its modern forms, when a formula mixes theories whose solvers exist separately: uninterpreted functions with arithmetic (QF_UFLIA, QF_UFLRA), arrays with bit-vectors (QF_ABV), and so on. Check that the theories are stably infinite, or use a polite or shiny combination for the others, such as bit-vectors. For two convex theories, the deterministic form is simple and polynomial in the number of shared variables. For non-convex theories inside a CDCL(T) solver, prefer delayed or model-based combination, which hand the case splits to the SAT engine. Use [Ackermannization](/ackermannization/) instead when the formula has few function applications.

## Pitfalls

- **Missing stable infiniteness.** Fixed-width bit-vectors and other finite domains are not stably infinite. Combined naively with EUF over the same sort, the method can answer SAT on an unsatisfiable formula, as in the example above.
- **Missing case splits.** Integer arithmetic, arrays and bit-vectors are not convex. A solver that only sends single equalities is incomplete for them, and answers SAT wrongly on the formula $1 \le x \le 2 \wedge f(x) \ne f(1) \wedge f(x) \ne f(2)$.
- **Shared symbols.** If both theories use the same function symbol, such as $+$ in two arithmetic theories, the method does not apply, and the answers can be wrong in both directions.
- **Forgetting to purify a constant.** A number such as $1$ inside $f(1)$ is an arithmetic term. It must become a shared constant, or the EUF solver will treat $f(1)$ and $f(x)$ as unrelated even when $x = 1$.
- **Too few interface equalities.** It is enough to consider equalities between shared constants, but all of them must be considered. A solver that sends only some of the entailed equalities makes the method incomplete.

## Implementations

## History

Greg Nelson and Derek Oppen published "Simplification by cooperating decision procedures" in ACM TOPLAS in 1979. It gave the method of propagating equalities between decision procedures for disjoint theories, with case splits for non-convex theories. Their completeness result imposed no condition on the theories, and the Handbook notes that it is incorrect as stated: the proof assumed that it is enough to consider infinite models. Oppen's paper "Complexity, convexity and combinations of theories" of 1980 gave the first correct proof, under the condition now called stable infiniteness, and introduced convex theories. Tinelli and Harandi gave a model-theoretic proof with arrangements in 1996, and Tinelli and Zarba showed in 2005 that the method is really incomplete without the condition. Nelson's prover Simplify used the method. From 2005, delayed and model-based combination moved the case splits into the SAT engine of lazy SMT solvers.

## References
