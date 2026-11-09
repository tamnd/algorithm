---
tag: K9NKZA
kind: problem
slug: qbf
name: Quantified Boolean formula
aliases:
- QBF
- Quantified Boolean formula satisfiability
- TQBF
- true quantified Boolean formula
area: logic-and-constraints/sat-solving
level: advanced
summary: Decide whether a Boolean formula with alternating for-all and there-exists quantifiers over its variables is true. PSPACE-complete (Stockmeyer and Meyer 1973); solved by QDPLL, QCDCL and expansion.
prereqs: [sat, conjunctive-normal-form, pspace, dpll]
see_also: [sat, pspace, polynomial-hierarchy, savitch-theorem, alternating-turing-machine, 2-sat, horn-sat, game-tree]
sources:
  - paper: doi:10.1145/800125.804029
    title: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Proceedings of the 5th ACM Symposium on Theory of Computing (STOC 1973), 1 to 9"
    locator: the PSPACE-completeness of the truth of quantified Boolean formulas
  - paper: doi:10.1016/0304-3975(76)90061-X
    title: "Larry J. Stockmeyer, The polynomial-time hierarchy, Theoretical Computer Science 3 (1976), 1 to 22"
    locator: QBF with k alternations is complete for the k-th level
  - paper: doi:10.1016/0020-0190(79)90002-4
    title: "Bengt Aspvall, Michael F. Plass and Robert E. Tarjan, A linear-time algorithm for testing the truth of certain quantified Boolean formulas, Information Processing Letters 8 (1979), 121 to 123"
    locator: quantified 2-CNF in linear time
  - paper: doi:10.1006/inco.1995.1025
    title: "Hans Kleine Büning, Marek Karpinski and Andreas Flögel, Resolution for quantified Boolean formulas, Information and Computation 117 (1995), 12 to 18"
    locator: Q-resolution, universal reduction, and quantified Horn formulas
  - paper: doi:10.1023/A:1015019416843
    title: "Marco Cadoli, Marco Schaerf, Andrea Giovanardi and Massimo Giovanardi, An algorithm to evaluate quantified Boolean formulae and its experimental evaluation, Journal of Automated Reasoning 28 (2002), 101 to 142"
    locator: the QDPLL procedure with unit, pure literal and early termination rules
  - paper: doi:10.1613/jair.1959
    title: "Enrico Giunchiglia, Massimo Narizzano and Armando Tacchella, Clause/term resolution and learning in the evaluation of quantified Boolean formulas, Journal of Artificial Intelligence Research 26 (2006), 371 to 416"
    locator: learning in QDPLL (QCDCL)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapters on QBF theory and on QBF solving
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity (1994)
    locator: Chapter 19, Section 19.1 (QSAT is PSPACE-complete)
---

A quantified Boolean formula (QBF) is a Boolean formula in which each variable is bound by a quantifier, "for all" ($\forall$) or "there exists" ($\exists$). Such a formula has no free variables, so it is simply true or false. The problem TQBF asks which. [SAT](/sat/) is the special case where every quantifier is $\exists$. TQBF is the standard complete problem for [PSPACE](/pspace/) (Stockmeyer and Meyer 1973), and with a bounded number of quantifier alternations it is complete for the levels of the [polynomial hierarchy](/polynomial-hierarchy/). A simple recursive evaluation decides it in polynomial space and exponential time. Practical solvers extend [DPLL](/dpll/) with rules that respect the quantifier order (QDPLL, and QCDCL with learning), or expand quantifiers into SAT calls.

## In plain words

Think of a game between two players. One player, "Exists", wants a formula to come out true. The other, "Forall", wants it false. They take turns setting switches in a fixed order: some switches belong to Exists and some to Forall. When all switches are set, the formula is checked.

The question is whether Exists has a strategy that wins no matter what Forall does. For a plain satisfiability problem, Forall has no switches, and Exists only needs one good setting. With Forall in the game, Exists must have an answer for every move of the opponent, and the answer may depend on the moves made so far. Trying all plays takes exponential time, but only a small amount of memory, and no method that is much faster in all cases is expected.

## Definition

A QBF in prenex form is $\Phi = Q_1 x_1\, Q_2 x_2 \cdots Q_n x_n\, \varphi$, where each $Q_i \in \{\forall, \exists\}$ and $\varphi$, the *matrix*, is a propositional formula over $x_1, \ldots, x_n$, usually in [CNF](/conjunctive-normal-form/). Truth is defined by induction: $\exists x\, \Psi$ is true if $\Psi[x := 0]$ or $\Psi[x := 1]$ is true, and $\forall x\, \Psi$ is true if both are. A block of equal quantifiers can be read in any order, so the prefix is a sequence of blocks with alternating quantifiers.

TQBF is the set of true closed QBFs. $\Sigma_k$-QBF is the restriction to prefixes with $k$ blocks starting with $\exists$, and $\Pi_k$-QBF starts with $\forall$.

A *strategy* for the existential player gives, for each existential variable, a Boolean function of the universal variables before it (a Skolem function). $\Phi$ is true exactly when some strategy makes $\varphi$ true for every assignment of the universal variables.

## Variants

- **2QBF.** Formulas $\exists X \forall Y\, \varphi$ or $\forall X \exists Y\, \varphi$, used in synthesis and in checking that a candidate solution is robust.
- **Non-prenex QBF.** Quantifiers inside the formula; these can be moved to the front without changing the truth, though the choice of order affects solvers.
- **Dependency QBF (DQBF).** Each existential variable depends on a given set of universal variables, not necessarily a prefix. DQBF is NEXPTIME-complete.
- **Quantified 2-CNF and quantified Horn formulas.** Polynomial cases, see below.
- **QBF with certificates.** Solvers that return Skolem functions for true formulas and Herbrand functions for false ones.

## Examples

**The order of quantifiers matters.** The matrix $(x \vee y) \wedge (\neg x \vee \neg y)$ says that $y = \neg x$.

- $\forall x\, \exists y\, (x \vee y)(\neg x \vee \neg y)$ is true: for each $x$, choose $y = \neg x$. The Skolem function is $y = \neg x$.
- $\exists y\, \forall x\, (x \vee y)(\neg x \vee \neg y)$ is false: whichever $y$ is chosen, $x = y$ makes a clause false.

**The QDPLL rules on a small formula.** $\Phi = \exists x_1\, \forall u\, \exists x_2.\ (x_1 \vee u \vee x_2) \wedge (x_1 \vee \neg u \vee \neg x_2) \wedge (\neg x_1 \vee u)$.

1. *Universal reduction.* In the clause $(\neg x_1 \vee u)$, the universal literal $u$ is quantified after every existential variable of the clause. The universal player can always make $u$ false there, so $u$ can be deleted, leaving $(\neg x_1)$.
2. *Unit rule.* $(\neg x_1)$ is a unit clause with an existential literal, so $x_1 = 0$.
3. What remains is $\forall u\, \exists x_2.\ (u \vee x_2) \wedge (\neg u \vee \neg x_2)$. No literal is pure and no clause is unit, so branch on the outermost variable, $u$. For $u = 0$, $x_2 = 1$ works; for $u = 1$, $x_2 = 0$ works. Both branches are true, so $\Phi$ is true.

A script that applies these rules, together with the pure literal rule, agreed with the recursive evaluation on 3000 random QBFs with up to 7 variables.

## Known algorithms

**Recursive evaluation.** Evaluate the outermost quantifier: for $\exists x$, return true if one of the two restrictions is true; for $\forall x$, if both are. When no quantifier is left, evaluate the matrix. Correctness is the definition of truth. The recursion has depth $n$ and keeps only the current partial assignment and the position in each level, so it needs $O(n + |\varphi|)$ space, and it takes $O(2^n |\varphi|)$ time. This puts TQBF in PSPACE. An existential branch may stop at the first true child and a universal one at the first false child, as in [game tree](/game-tree/) search.

**QDPLL.** DPLL adapted to the prefix (Cadoli and others 1998; Giunchiglia, Narizzano and Tacchella). Its rules, for a CNF matrix:

- *Branching order.* Branch only on a variable of the outermost block that still has free variables. An existential branch succeeds if one value succeeds, a universal branch if both do.
- *Universal reduction.* Delete a universal literal $u$ from a clause if no existential variable of the clause is quantified after $u$.
- *Empty clause.* If a clause has no literal left after reduction, the current branch is false.
- *Unit rule.* If, after universal reduction, a clause has a single literal, it is existential; set it true.
- *Pure literal rule.* If a literal $\ell$ occurs and $\neg \ell$ does not, set $\ell$ true when its variable is existential, and false when it is universal.
- *All clauses satisfied.* The current branch is true.

QCDCL adds learning of clauses, by Q-resolution, from conflicts, and of *cubes*, sets of literals that make the matrix true, from solutions, with backjumping. DepQBF is a well-known solver of this kind.

**Expansion.** Replace $\forall u\, \Psi$ by $\Psi[u := 0] \wedge \Psi[u := 1]$, with copies of the existential variables inside. Full expansion is exponential, but counterexample-guided methods such as RAReQS expand only on the universal assignments that matter, using SAT solvers, and they are strong on formulas with few alternations.

**Polynomial cases.** Quantified 2-CNF formulas are decided in linear time by the strongly connected components of the implication graph (Aspvall, Plass and Tarjan 1979), extending the [2-SAT algorithm](/two-sat-algorithm/). Quantified [Horn](/horn-sat/) formulas are decided in polynomial time (Kleine Büning, Karpinski and Flögel 1995).

## Bounds

- **PSPACE-complete** (Stockmeyer and Meyer 1973). Membership is the recursive evaluation. For hardness, take a machine $M$ that uses polynomial space $p$, so that a configuration is a string of $s = O(p)$ bits. Let $R_i(c, d)$ say that $d$ is reachable from $c$ in at most $2^i$ steps. Then $R_0$ is a polynomial formula, and

$$R_{i+1}(c, d) = \exists m\, \forall a\, \forall b\, \big[\big((a = c \wedge b = m) \vee (a = m \wedge b = d)\big) \rightarrow R_i(a, b)\big],$$

which uses one copy of $R_i$, so the size grows by $O(s)$ per level, and $R_s(c_{\mathrm{start}}, c_{\mathrm{accept}})$ has size $O(s^2)$. A [Tseitin transformation](/tseitin-transformation/) with innermost existential variables gives a CNF matrix. The same idea, with an existential middle point, proves [Savitch's theorem](/savitch-theorem/).
- **Bounded alternation.** $\Sigma_k$-QBF is $\Sigma_k^p$-complete when the matrix is in CNF for odd $k$ and in DNF for even $k$ (Stockmeyer 1976; Wrathall 1976). The form of the matrix matters: $\exists X \forall Y\, \varphi$ with $\varphi$ in CNF is only NP-complete, because universal reduction removes all of $Y$.
- **Proof complexity.** Q-resolution is sound and complete for false QBFs with CNF matrix, and some families of false formulas need exponentially long Q-resolution refutations; such lower bounds also bound the running time of QCDCL.
- **Under the strong exponential time hypothesis**, TQBF on $n$ variables needs about $2^n$ time, since SAT does.

## Reductions

- **SAT** is $\exists$-QBF, and unsatisfiability is $\forall$-QBF of the negated matrix.
- **Two-player games** of polynomial length, such as generalized geography, and positions of board games with polynomially bounded play, reduce to TQBF and from it.
- **Planning and model checking.** Conformant planning, the bounded model checking of a system for a path of length $2^k$ by the squaring trick above, and the checking of properties with alternation are encoded as QBF.
- **Synthesis.** Find a function or a circuit that meets a specification for all inputs: $\exists$ design $\forall$ input. Skolem functions of the true QBF give the design.

## Applications

QBF solvers are used for the synthesis of circuits and of reactive controllers, for planning under uncertainty, for the verification of hardware with parameters, for computing the diameter of state spaces, and for the analysis of games. Because QBF is much harder than SAT, practical use is mostly on formulas with few alternations, often 2QBF.

## References
