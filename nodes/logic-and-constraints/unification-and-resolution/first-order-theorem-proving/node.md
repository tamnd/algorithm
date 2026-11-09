---
tag: 297GKF
kind: problem
slug: first-order-theorem-proving
name: First-order theorem proving
aliases:
- automated theorem proving
- first-order refutation
- first-order validity problem
- first-order provability
area: logic-and-constraints/unification-and-resolution
level: core
summary: Decide whether a first-order sentence follows from given axioms. It is semi-decidable, by Herbrand's theorem or resolution, and undecidable (Church 1936, Turing 1936).
prereqs: [clausal-normal-form, refutation, herbrand-theorem]
see_also: [robinson-resolution, robinson-completeness-theorem, superposition, herbrand-theorem, church-theorem, entscheidungsproblem, post-correspondence-problem, sat]
sources:
  - paper: doi:10.2307/2269326
    title: Alonzo Church, A note on the Entscheidungsproblem, Journal of Symbolic Logic 1(1), 1936
    locator: the theorem that the decision problem for first-order validity has no recursive solution
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society s2-42, 1936
    locator: the application to the Entscheidungsproblem, a formula that is provable exactly when a given machine prints 0
  - paper: doi:10.1145/321250.321253
    title: John Alan Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965
    locator: the resolution principle as a complete refutation procedure for first-order clauses
  - book: isbn:9780121703509
    title: Chin-Liang Chang and Richard Char-Tung Lee, Symbolic Logic and Mechanical Theorem Proving, Academic Press, 1973
    locator: Chapter 4, Herbrand's theorem (Section 4.6 on implementation, including Gilmore's method), and Chapter 5, The resolution principle
  - paper: "Harry R. Lewis, Complexity results for classes of quantificational formulas, Journal of Computer and System Sciences 21(3), 317 to 353, 1980"
    locator: the satisfiability problem for the Bernays-Schönfinkel class is complete for nondeterministic exponential time
  - book: isbn:9780444508133
    title: Alan Robinson and Andrei Voronkov (eds.), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 2, Leo Bachmair and Harald Ganzinger, Resolution theorem proving, and Chapter 7, Robert Nieuwenhuis and Albert Rubio, Paramodulation-based theorem proving
---

**First-order theorem proving** is the problem of deciding whether a first-order sentence $\varphi$ is a logical consequence of a set of axioms $\Gamma$, and of producing a proof when it is. It is equivalent to showing that $\Gamma \cup \{\lnot \varphi\}$ is unsatisfiable, so provers put this set into [clausal normal form](/clausal-normal-form/) and search for a [refutation](/refutation/). The problem is semi-decidable: a complete method such as [Robinson's resolution](/robinson-resolution/) finds a proof of every true consequence. It is not decidable, by the theorems of Church and Turing of 1936, so on a non-consequence the search may run forever.

## In plain words

You give the computer some basic facts and rules, and a claim. The computer must find out whether the claim follows from the facts in every possible world where the facts hold, and show a proof if it does.

The usual way is to add the denial of the claim and look for a contradiction. A careful search always finds one when the claim does follow, because every contradiction already shows up in finitely many concrete cases.

When the claim does not follow, there is no contradiction to find, and the search may never stop. This is not a weakness of one method: no program can give the right yes or no answer for every claim. Provers therefore stop after a time limit, or look for a world that shows the claim is false.

## Definition

**Input.** A finite set $\Gamma$ of first-order sentences and a sentence $\varphi$, over a signature of function, constant and predicate symbols.

**Question.** Is $\Gamma \models \varphi$, that is, does every structure that satisfies $\Gamma$ satisfy $\varphi$?

**Output.** YES with a proof, if $\Gamma \models \varphi$. A procedure is a **semi-decision procedure** if it halts with YES exactly on the instances where the answer is yes; it may run forever on the others.

By Gödel's completeness theorem, $\Gamma \models \varphi$ if and only if $\varphi$ has a formal proof from $\Gamma$, so consequence and provability are the same problem. Since $\Gamma \models \varphi$ if and only if $\Gamma \cup \{\lnot\varphi\}$ is unsatisfiable, and a [clausal normal form](/clausal-normal-form/) preserves satisfiability, the problem is the same as **unsatisfiability of a finite set of clauses**. The special case $\Gamma = \emptyset$ is the **validity problem**.

## Variants

- **Validity of one sentence.** $\Gamma = \emptyset$. The general case reduces to it: $\Gamma \models \varphi$ iff $\bigwedge \Gamma \to \varphi$ is valid.
- **With equality.** The symbol $=$ is always read as identity. It can be axiomatized, but provers use [paramodulation](/paramodulation/) or [superposition](/superposition/).
- **Modulo a theory.** Arithmetic, arrays and other theories are built in, as in SMT solving. Many of these are undecidable as well, or decidable only for quantifier-free input.
- **Decidable fragments.** Propositional logic ([SAT](/sat/) is the dual); the monadic fragment, with only unary predicates and no function symbols; the Bernays-Schönfinkel class $\exists^* \forall^*$ with no function symbols, whose Skolem form has only constants; and ground Horn clauses.
- **Finite satisfiability.** Does $\Gamma \cup \{\lnot\varphi\}$ have a finite model? This is the question of model finders, which search for a counterexample of each size.
- **Answer extraction.** For a goal $\exists \vec x \, \psi$, return terms for $\vec x$; see [answer substitution](/answer-substitution/).

## Examples

**A theorem.** "Every man is mortal; Socrates is a man; so Socrates is mortal." The clauses $\lnot \mathit{Man}(x) \vee \mathit{Mortal}(x)$, $\mathit{Man}(s)$ and $\lnot \mathit{Mortal}(s)$ have a refutation with two resolution steps.

**A theorem that needs two instances.** The drinker sentence $\exists x \, (D(x) \to \forall y \, D(y))$ is valid. Its negation in clausal form is $\{D(x), \lnot D(g(x))\}$, with a Skolem function $g$. Over the [Herbrand universe](/herbrand-universe/) $\{a, g(a), g(g(a)), \ldots\}$, the 2 instances at depth 0, $D(a)$ and $\lnot D(g(a))$, are satisfiable. At depth 1 there are 4 instances, and $D(g(a))$ with $\lnot D(g(a))$ is a contradiction. Resolution finds it in one step, with the unifier $x \mapsto g(x')$.

**Three instances deep.** For $\{P(a), \lnot P(x) \vee P(f(x)), \lnot P(f(f(a)))\}$, the ground instances over the terms of depth 0 are 3 satisfiable clauses, and those over depth 1 are 4 clauses that are unsatisfiable: $P(a)$, $\lnot P(a) \vee P(f(a))$, $\lnot P(f(a)) \vee P(f(f(a)))$ and $\lnot P(f(f(a)))$.

**A non-theorem.** $\forall x \exists y \, R(x, y) \to \exists y \forall x \, R(x, y)$ is not valid: in the domain $\{0, 1\}$ with $R$ the identity relation, every element is related to itself, but no element is related to both. The negation has the clauses $R(x, f(x))$ and $\lnot R(g(y), y)$. Unifying the atoms needs $x = g(y)$ and $y = f(x)$, so $y = f(g(y))$, which fails the [occurs check](/occurs-check/). No resolvent exists, the clause set is saturated without $\square$, and resolution answers "satisfiable".

**A non-theorem with no answer.** $\{P(a), \lnot P(x) \vee P(f(x))\}$ is satisfiable, but resolution derives $P(f(a))$, $P(f(f(a)))$, and so on forever. A prover stops on a limit, or a model finder reports the model with $P$ true everywhere.

## Known algorithms

- **Herbrand instance enumeration (Gilmore 1960).** Generate the ground instances over the Herbrand universe level by level, and test each finite set by a propositional method. Complete by [Herbrand's theorem](/herbrand-theorem/), and practical only for tiny problems.
- **Davis-Putnam (1960).** The same enumeration with a better propositional test, which is the origin of [Davis-Putnam elimination](/davis-putnam-elimination/) and DPLL.
- **Resolution (Robinson 1965).** [Binary resolution](/binary-resolution/) and [factoring](/factoring/) on clauses with variables, with [most general unifiers](/most-general-unifier/), as in [Robinson's resolution](/robinson-resolution/). Complete by the [Robinson completeness theorem](/robinson-completeness-theorem/).
- **Refinements of resolution.** [Set of support](/set-of-support/), [hyperresolution](/hyperresolution/), [linear resolution](/linear-resolution/), [unit resolution](/unit-resolution/) (complete for Horn clauses) and [ordered resolution](/ordered-resolution/), with deletion of tautologies and [subsumed clauses](/subsumption/).
- **Equality.** [Paramodulation](/paramodulation/), [demodulation](/demodulation/) and [superposition](/superposition/). The provers E, SPASS and Vampire are built on superposition.
- **Logic programming.** For Horn clauses, [SLD resolution](/sld-resolution/) is complete and serves as an execution model.

## Bounds

**Theorem 1 (semi-decidability).** The set of unsatisfiable finite clause sets, and so the set of pairs $(\Gamma, \varphi)$ with $\Gamma \models \varphi$, is recursively enumerable.

*Proof.* Let $S$ be a finite clause set. Let $H_0$ be the constants of $S$, or one new constant if there is none, and let $H_{d+1}$ add to $H_d$ all terms $f(t_1, \ldots, t_n)$ with $f$ in $S$ and $t_i \in H_d$. Each $H_d$ is finite, so the set $G_d$ of instances of clauses of $S$ with variables replaced by terms of $H_d$ is finite, and its propositional satisfiability can be decided by a truth table. Test $d = 0, 1, 2, \ldots$ and halt when $G_d$ is unsatisfiable. If $S$ is unsatisfiable, Herbrand's theorem gives a finite unsatisfiable set of ground instances, which lies in some $G_d$, and every superset of an unsatisfiable set is unsatisfiable, so the procedure halts. If it halts, $G_d$ is unsatisfiable, and since each clause implies its instances, $S$ is unsatisfiable. For $(\Gamma, \varphi)$, first compute a clausal form of $\Gamma \cup \{\lnot\varphi\}$. $\square$

**Theorem 2 (undecidability; Church 1936, Turing 1936).** No algorithm decides, for every sentence $\varphi$, whether $\varphi$ is valid.

*Proof.* We reduce the [Post correspondence problem](/post-correspondence-problem/), which is undecidable: given pairs $(u_1, v_1), \ldots, (u_k, v_k)$ of nonempty words over $\{0, 1\}$, is there a nonempty sequence $i_1, \ldots, i_m$ with $u_{i_1} \cdots u_{i_m} = v_{i_1} \cdots v_{i_m}$? Church and Turing used other reductions; this one is shorter.

Use a constant $a$, unary function symbols $f_0, f_1$ and a binary predicate $P$. For a word $w$ write $f_w(t)$ for $t$ with the symbols of $w$ applied in order: $f_\varepsilon(t) = t$ and $f_{wb}(t) = f_b(f_w(t))$. Then $f_w(f_v(t)) = f_{vw}(t)$. Let

$$\varphi = \Big( \bigwedge_{i=1}^{k} P(f_{u_i}(a), f_{v_i}(a)) \;\wedge\; \forall x \forall y \big( P(x, y) \to \bigwedge_{i=1}^{k} P(f_{u_i}(x), f_{v_i}(y)) \big) \Big) \to \exists z \, P(z, z).$$

The map from the instance to $\varphi$ is computable. We show that $\varphi$ is valid if and only if the instance has a solution.

If $i_1, \ldots, i_m$ is a solution, let $M$ be a structure that satisfies the antecedent; for other structures $\varphi$ is true at once. Write $U_j = u_{i_1} \cdots u_{i_j}$ and $V_j = v_{i_1} \cdots v_{i_j}$. By induction on $j$, $M$ satisfies $P(f_{U_j}(a), f_{V_j}(a))$: for $j = 1$ by the first conjunct, and from $j$ to $j + 1$ by the second conjunct with $x = f_{U_j}(a)$ and $y = f_{V_j}(a)$, since $f_{u_{i_{j+1}}}(f_{U_j}(a)) = f_{U_{j+1}}(a)$. For $j = m$, $U_m = V_m$, so the two arguments are the same term, and its value is a witness for $\exists z \, P(z, z)$.

If there is no solution, take the domain of all words over $\{0, 1\}$, let $a$ be the empty word, let $f_b$ append the letter $b$, so that $f_w(t)$ is $t w$, and let $P$ hold for exactly the pairs $(U_j, V_j)$ of all nonempty index sequences. The first conjunct holds with $m = 1$, and the second holds because extending a sequence by $i$ appends $u_i$ and $v_i$. No pair $(w, w)$ is in $P$, because that would be a solution. So the antecedent is true and the conclusion is false, and $\varphi$ is not valid. $\square$

**Corollaries.** Satisfiability of first-order sentences is not recursively enumerable: if it were, then validity and its complement would both be enumerable, and validity would be decidable. There is no computable bound $b(n)$ on the length of the shortest resolution refutation of an unsatisfiable clause set of size $n$: with such a bound, trying all derivations up to length $b(n)$ would decide unsatisfiability.

**Fragments.** Propositional unsatisfiability is coNP-complete, the complement of [SAT](/sat/). Satisfiability of the Bernays-Schönfinkel class is NEXPTIME-complete (Lewis 1980). Resolution length is exponential in the worst case even for propositional clauses, by the [Haken lower bound](/haken-resolution-lower-bound/).

## Reductions

- **From the Post correspondence problem**, as in Theorem 2, and from the [halting problem](/halting-problem/), as in Turing's paper: a machine halts if and only if a sentence that describes its run implies a sentence that says it halts.
- **To clause unsatisfiability**, by negation and [clausal normal form](/clausal-normal-form/), which preserves satisfiability with new Skolem and definition symbols.
- **To propositional satisfiability**, one level at a time, by [Herbrand's theorem](/herbrand-theorem/). Each level is a [SAT](/sat/) instance, but the number of levels needed has no computable bound.
- **Equality to pure logic**, by adding the axioms of reflexivity, symmetry, transitivity and congruence for each symbol. Provers prefer built-in rules, because these axioms produce many useless resolvents.

## Applications

- **Mathematics.** McCune's prover EQP found a proof of the Robbins conjecture in 1996, which shows that every Robbins algebra is a Boolean algebra.
- **Interactive proof assistants.** Tools called hammers translate a goal and relevant lemmas into first-order clauses, call a superposition prover, and rebuild the proof found inside the assistant.
- **Program verification.** Verification conditions with quantifiers are passed to first-order provers or to SMT solvers with [quantifier instantiation](/quantifier-instantiation/).
- **Logic programming and databases.** [Logic programming](/logic-programming/) runs Horn clauses by [SLD resolution](/sld-resolution/), and deductive databases answer queries by resolution over rules and facts.

## References
