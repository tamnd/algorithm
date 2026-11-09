---
tag: RJ452K
kind: technique
slug: ackermannization
name: Ackermannization
aliases:
- Ackermann reduction
- Ackermann's reduction
- Ackermann's expansion
- functional consistency constraints
area: logic-and-constraints/smt
level: advanced
summary: Replace each application of a free function by a fresh constant, and add a constraint that equal arguments give equal results. The result is equisatisfiable and at most quadratic.
prereqs: [smt-problem, euf-satisfiability]
see_also: [eager-smt-encoding, congruence-closure, nelson-oppen, model-based-theory-combination, bit-blasting, lazy-smt]
sources:
  - paper: doi:10.1016/s0049-237x(08)x7070-3
    title: Wilhelm Ackermann, Solvable Cases of the Decision Problem, Studies in Logic and the Foundations of Mathematics, North-Holland, 1954
    locator: the reduction of free function symbols to equality, cited as [Ack54] in the Handbook
  - book: isbn:9781643681603
    title: Clark Barrett, Roberto Sebastiani, Sanjit A. Seshia and Cesare Tinelli, Satisfiability Modulo Theories, Chapter 33 of the Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Section 33.3.1.3 (Ackermann's method and the Bryant-German-Velev method), Section 33.3.1.4 (the quadratic bound), Section 33.6.4 (Ackermann's expansion in theory combination, Example 33.6.4)
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 4, Equalities and Uninterpreted Functions (Ackermann's reduction and Bryant's reduction)
  - paper: doi:10.1145/371282.371364
    title: Randal E. Bryant, Steven German and Miroslav N. Velev, Processor verification using efficient reductions of the logic of uninterpreted functions to propositional logic, ACM Transactions on Computational Logic 2(1), 2001, pages 93 to 134
    locator: the ite form of function elimination and positive equality
  - paper: doi:10.1007/11916277_38
    title: Roberto Bruttomesso, Alessandro Cimatti, Anders Franzén, Alberto Griggio, Alessandro Santuari and Roberto Sebastiani, To Ackermann-ize or not to Ackermann-ize? On efficiently handling uninterpreted function symbols in SMT(EUF ∪ T), LPAR 2006, LNCS 4246, pages 557 to 571
    locator: an experimental comparison of Ackermann's expansion and delayed theory combination
---

Ackermannization removes the uninterpreted function symbols from a quantifier-free formula. Each application $f(t_i)$ is replaced by a fresh constant $F_i$, and for each pair of applications of the same symbol the formula gets the *functional consistency constraint* $t_i = t_j \rightarrow F_i = F_j$. The new formula has no function symbols of positive arity, it is satisfiable exactly when the old one is, and it is at most quadratic in the size of the old one. The method is from Ackermann's 1954 book on decidable cases of the decision problem. In SMT it is the first step of the [eager approach](/eager-smt-encoding/) for EUF, and an alternative to [theory combination](/nelson-oppen/) with EUF when the other theory has a solver of its own.

## In plain words

An unknown function is a box: put a value in, get a value out. The only rule that we know about the box is that the same input always gives the same output.

So we can forget the box. Give each use of it, such as f(a) or f(b), a new name of its own, as if the outputs were free unknowns. Then write down the one rule that matters for each pair of uses: if a equals b, then the name for f(a) must equal the name for f(b).

Nothing is lost. Any answer to the new problem can be turned back into a box, because the rule makes sure that equal inputs never ask for two different outputs. The cost is one rule for each pair of uses of the same function.

## When it applies

- The formula is ground (quantifier-free), and the function symbols that you remove are *uninterpreted*: no theory axiom mentions them.
- The theory that remains can decide equalities between the new constants. Equality logic, difference logic, linear arithmetic and bit-vectors all can.
- The number of applications of each symbol is small, because the constraints grow with the square of that number.
- You want one solver for one theory, and not a combination of two solvers: for example, an [eager encoding](/eager-smt-encoding/) to SAT, a bit-vector solver that does [bit-blasting](/bit-blasting/), or an arithmetic solver without an EUF part.

## The template

The holes are the set of symbols to remove and the form of the constraints.

```pseudo id=main
ACKERMANN(φ)
L1  for each function symbol f to remove      ▷ hole: all free symbols, or only some of them
L2      list the applications f(s_1), ..., f(s_r) of f in φ, inner terms before outer ones
L3      give each f(s_i) a fresh constant F_i of the result sort of f
L4  φ* ← φ with each application replaced by its constant, inner terms first
L5  FC ← true
L6  for each removed f and each pair i < j of its applications
L7      FC ← FC ∧ (s_i* = s_j* → F_i = F_j)    ▷ s* is s after L4; for k arguments, a conjunction of k equalities
L8  return φ* ∧ FC                              ▷ hole: Ackermann constraints, or the ite form of Bryant, German and Velev
```

A predicate symbol $p$ is removed in the same way, with fresh Boolean constants $P_i$ and the constraints $s_i^* = s_j^* \rightarrow (P_i \leftrightarrow P_j)$.

**Theorem (equisatisfiability).** Let $T$ be a theory whose signature does not contain the removed symbols. Then $\varphi$ is satisfiable in $T$ combined with the free symbols if and only if $\varphi^* \wedge FC$ is $T$-satisfiable.

*Proof.* Write $t^*$ for the term $t$ after line L4. A term with no removed symbol is its own image.

($\Rightarrow$) Let $M$ satisfy $\varphi$. Extend $M$ by $F_i := M(f(s_i))$. By induction on terms, $M(t^*) = M(t)$ for every subterm $t$ of $\varphi$, because $f(s_i)^* = F_i$ gets the value of $f(s_i)$ and the other symbols are not changed. So $\varphi^*$ has the truth value of $\varphi$, which is true. If $M(s_i^*) = M(s_j^*)$, then $M(s_i) = M(s_j)$, so $M(f(s_i)) = M(f(s_j))$ because $f^M$ is a function, so $F_i = F_j$. Thus $FC$ holds. The new constants are not in the signature of $T$, so the model is still a $T$-model.

($\Leftarrow$) Let $M'$ be a $T$-model of $\varphi^* \wedge FC$. Define $f^M$ on the domain of $M'$: if $v = M'(s_i^*)$ for some $i$, let $f^M(v) = M'(F_i)$ for the smallest such $i$; for any other $v$, let $f^M(v)$ be any element of the right sort. Let $M$ be $M'$ with $f^M$ added. Now $f^M(M'(s_i^*)) = M'(F_i)$ for every $i$, not only for the smallest one: if $j$ is the smallest index with $M'(s_j^*) = M'(s_i^*)$, then the constraint for the pair $j, i$ gives $M'(F_j) = M'(F_i)$. By induction on terms, inner terms first, $M(t) = M'(t^*)$: for $t = f(s_i)$, $M(t) = f^M(M(s_i)) = f^M(M'(s_i^*)) = M'(F_i) = M'(t^*)$. So $\varphi$ gets the truth value of $\varphi^*$ in $M'$, which is true. The theory $T$ does not mention $f$, so $M$ is still a $T$-model. $\square$

**Theorem (size).** If $f$ has $r_f$ applications of arity $k_f$, line L7 adds $r_f (r_f - 1)/2$ constraints, each with $k_f + 1$ equalities between constants or terms of $\varphi^*$. Write $n$ for the number of nodes of $\varphi$ as a DAG, so that $\sum_f r_f k_f \le n$ and $\sum_f r_f \le n$. Then the output has $O(n^2)$ nodes, and the bound is reached.

*Proof.* Line L4 does not increase the number of nodes: each application node is replaced by one constant. The constraints for $f$ have $O(r_f^2 (k_f + 1))$ nodes, if each $s_i^*$ is shared as a DAG node. The sum over $f$ is at most $(\max_f r_f) \sum_f r_f (k_f + 1) \le n \cdot 2n$. For the lower bound, $\bigwedge_{i=1}^{r} f(x_i) = y$ has $O(r)$ nodes and gets $r (r - 1)/2$ constraints. $\square$

The Handbook (Section 33.3.1.4) states the same bound for the step from the lambda-free formula to the arithmetic formula: the worst-case growth is quadratic.

### A worked example

*Nested applications.* Take $\varphi = f(f(x)) \ne f(x) \wedge f(x) = x$. It is unsatisfiable: from $f(x) = x$, congruence gives $f(f(x)) = f(x)$. Line L2 lists $f(x)$ before $f(f(x))$. Line L3 gives $F_1$ for $f(x)$ and $F_2$ for $f(f(x))$. After line L4 the argument of the outer application is $F_1$, so line L7 gives one constraint:

$$\varphi^* \wedge FC = F_2 \ne F_1 \wedge F_1 = x \wedge (x = F_1 \rightarrow F_1 = F_2).$$

The second conjunct makes the premise of the constraint true, so $F_1 = F_2$, which contradicts the first conjunct. A script checked this with all assignments over 5 values, and it checked the theorem on 300 random formulas with up to 4 clauses over $a, b, c$ and nested applications of $f$, against brute force over all functions on a small domain. All 300 answers were the same, 277 satisfiable and 23 unsatisfiable.

*With arithmetic.* Take $x \le y \wedge y \le x \wedge f(x) \ne f(y)$ over the integers with a free $f$. Ackermannization gives the pure linear arithmetic formula

$$x \le y \wedge y \le x \wedge F_1 \ne F_2 \wedge (x = y \rightarrow F_1 = F_2),$$

and an arithmetic solver alone sees that $x = y$, so $F_1 = F_2$, a contradiction. If $y \le x$ is dropped, the solver can return $x = 0, y = 1, F_1 = 0, F_2 = 1$, and the second half of the proof reads off $f(0) = 0$, $f(1) = 1$ and any value elsewhere.

## Classic examples

- **Eager EUF solving.** [Eager SMT encoding](/eager-smt-encoding/) first ackermannizes, then encodes equality logic in SAT by a small domain or by transitivity constraints.
- **Bit-vectors with free functions.** A bit-vector solver can ackermannize the free functions of a QF_UFBV formula and then [bit-blast](/bit-blasting/) the result, see [bit-vector satisfiability](/bit-vector-satisfiability/).
- **Theory combination without combination.** For EUF with arithmetic, the Handbook (Section 33.6.4) gives Ackermann's expansion as the alternative to [Nelson-Oppen](/nelson-oppen/) and [model-based theory combination](/model-based-theory-combination/): one arithmetic solver, no exchange of equalities. Bruttomesso and others compared it with delayed theory combination.
- **Processor verification.** Burch and Dill, and Bryant, German and Velev, abstracted ALUs and memories as free functions and removed them before the SAT call.

## Variations

- **The Bryant-German-Velev ite form.** Replace $f(s_j)$ by $\mathrm{ite}(s_j = s_1, F_1, \mathrm{ite}(s_j = s_2, F_2, \ldots, F_j))$. No separate constraints are added, the size is also quadratic, and the form keeps the polarity of equalities, which allows *positive equality*: applications that occur only under positive equalities can take distinct values.
- **Partial Ackermannization.** Remove only the symbols with few applications, and leave the others to a [congruence closure](/congruence-closure/) solver.
- **Lazy Ackermannization.** Add a constraint $s_i = s_j \rightarrow F_i = F_j$ only when a candidate model sets $s_i = s_j$ and $F_i \ne F_j$, as in the [lazy approach](/lazy-smt/). This is how lemmas on demand handle free functions and array reads.
- **Predicates.** Fresh Boolean constants and $\leftrightarrow$ in place of $=$, as described above.

## Pitfalls

- **Interpreted symbols.** Only uninterpreted symbols can be removed. If $+$ or $\mathrm{select}$ is replaced by fresh constants, the theory facts about it are lost, and an unsatisfiable formula can become satisfiable.
- **Order of replacement.** Inner applications must be replaced first, so that the arguments in the constraints are terms of $\varphi^*$. If $f(f(x))$ gets a constant but the constraint still mentions $f(x)$, the result is not free of $f$.
- **Quantifiers.** The reduction is for ground formulas. Under a quantifier, the set of applications is not finite, so no finite set of constraints is enough.
- **Many applications.** A symbol with thousands of applications gives millions of constraints, almost all of which have false premises. Congruence closure handles such formulas in $O(n \log n)$ time.
- **Lost structure.** The constraints hide the term structure from the solver. For EUF alone, a [congruence closure](/congruence-closure/) solver is better, and the comparison by Bruttomesso and others shows that the best choice depends on the benchmark.

## Exercises

1. Prove that the Bryant-German-Velev ite form gives a formula that is equisatisfiable with $\varphi$.
2. A binary symbol $g$ has $r$ applications. How many constraints does line L7 add, and how many equalities do they contain in all?
3. Give a formula with an interpreted symbol, for example $x + y \ne y + x$ over the integers, that is unsatisfiable, but becomes satisfiable when $+$ is removed as if it were free.

## References
