---
tag: BD793D
kind: definition
slug: conjunctive-normal-form
name: Conjunctive normal form
aliases:
- CNF
- clause form
- product of sums
area: logic-and-constraints/sat-solving
level: intro
summary: A formula that is a conjunction of clauses, each a disjunction of literals. Every Boolean function has one, and it is the input form of SAT solvers.
prereqs: [clause, boolean-function]
see_also: [sat, tseitin-transformation, dimacs-cnf-format, k-sat, horn-sat, clausal-normal-form, circuit-sat, cook-levin-theorem]
sources:
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 1, Section 1.3 (normal forms, CNF and the Tseitin encoding)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 2, CNF Encodings, by Steven Prestwich (CNF, the cost of conversion and the Tseitin encoding)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability (formulas as sets of clauses)
  - paper: "G. S. Tseitin, On the complexity of derivation in propositional calculus, in A. O. Slisenko (ed.), Studies in Constructive Mathematics and Mathematical Logic, Part 2, 1968"
    locator: pages 115 to 125 (the definitional transformation into CNF with new variables)
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the Third Annual ACM Symposium on Theory of Computing (STOC), 1971
    locator: pages 151 to 158 (satisfiability of formulas in conjunctive normal form is NP-complete)
---

A formula is in conjunctive normal form (CNF) when it is a conjunction of [clauses](/clause/), and each clause is a disjunction of [literals](/literal/), for example $(x_1 \vee \neg x_2) \wedge (x_2 \vee x_3)$. Every [Boolean function](/boolean-function/) has a CNF, but some need exponentially many clauses unless new variables are added; the [Tseitin transformation](/tseitin-transformation/) adds them and gives an equisatisfiable CNF of linear size. CNF is the input form of SAT solvers and of the [Boolean satisfiability problem](/sat/), which [Cook](/cook-levin-theorem/) proved NP-complete for CNF formulas.

## Definition

Fix the variables $x_1, \ldots, x_n$.

**CNF formula.** A CNF formula $F$ is a finite set of clauses $\{C_1, \ldots, C_m\}$, read as $\bigwedge_{j=1}^{m} \bigvee_{\ell \in C_j} \ell$. Its size is $|F| = \sum_j |C_j|$, the number of literal occurrences. The empty formula, with $m = 0$, is true. A formula that contains the empty clause is false.

**Models.** An assignment $\alpha$ is a model of $F$, written $\alpha \models F$, when it satisfies every clause. $F$ is *satisfiable* if it has a model. Two formulas are *equivalent* when they have the same models over the same variables, and *equisatisfiable* when both are satisfiable or both are not.

**k-CNF.** $F$ is in $k$-CNF when every clause has at most $k$ literals (some texts say exactly $k$). The satisfiability problem for $k$-CNF is [k-SAT](/k-sat/).

**Existence.** Every Boolean function $f$ of $x_1, \ldots, x_n$ has a CNF: for each assignment $\beta$ with $f(\beta) = 0$, take the clause of the $n$ literals that are false under $\beta$. That clause is false exactly at $\beta$, so the conjunction of these clauses is false exactly where $f$ is false. These clauses are the *maxterms* of $f$, and the formula is its canonical CNF.

**Size can be exponential.** Let $f = x_1 \oplus \cdots \oplus x_n$, the parity function. *Every CNF of $f$ over $x_1, \ldots, x_n$ has at least $2^{n-1}$ clauses.* Proof: let $C$ be a clause of such a CNF that is not a tautology, and suppose $C$ does not mention $x_i$. Take an assignment $\beta$ that falsifies $C$. Then $f(\beta) = 0$. Flipping $x_i$ in $\beta$ keeps $C$ false but makes $f$ equal to 1, a contradiction. So $C$ mentions all $n$ variables and is false at exactly one assignment. The function is false at $2^{n-1}$ assignments, and each needs its own clause. $\blacksquare$

**Equisatisfiable CNF in linear size.** With new variables, every formula $\varphi$ built from $\neg$, $\wedge$ and $\vee$ has an equisatisfiable CNF with $O(|\varphi|)$ clauses of width at most 3: give each subformula a new variable and add the clauses that define it, as the [Tseitin transformation](/tseitin-transformation/) does. Each model of $\varphi$ extends in one way to a model of the CNF, and each model of the CNF restricts to a model of $\varphi$.

## Examples and non-examples

| formula | CNF? | note |
|---|---|---|
| $(x_1 \vee \neg x_2) \wedge (x_2 \vee x_3 \vee x_4) \wedge \neg x_1$ | yes | 3 clauses, $\lvert F \rvert = 6$ |
| $x_1 \vee x_2 \vee \neg x_3$ | yes | one clause |
| $x_1 \wedge \neg x_2$ | yes | two unit clauses |
| the empty conjunction | yes | true |
| $(x_1 \wedge x_2) \vee x_3$ | no | a disjunction of a conjunction |
| $\neg(x_1 \vee x_2)$ | no | negation of a clause; its CNF is $\{\neg x_1\}, \{\neg x_2\}$ |
| $(x_1 \wedge x_2) \vee (\neg x_1 \wedge x_3)$ | no | disjunctive normal form (DNF) |

Some CNFs of familiar functions:

- Majority of three: $\{x_1, x_2\}, \{x_1, x_3\}, \{x_2, x_3\}$. At least two variables are true exactly when every pair has a true member.
- Parity of three, $x_1 \oplus x_2 \oplus x_3$: the four clauses $\{x_1, x_2, x_3\}$, $\{x_1, \neg x_2, \neg x_3\}$, $\{\neg x_1, x_2, \neg x_3\}$, $\{\neg x_1, \neg x_2, x_3\}$, one for each of the four assignments with an even number of ones. By the bound above, no CNF over these variables has fewer.
- Distribution blows up: $(x_1 \wedge y_1) \vee (x_2 \wedge y_2)$ becomes $\{x_1, x_2\}, \{x_1, y_2\}, \{y_1, x_2\}, \{y_1, y_2\}$, and with $k$ terms $(x_1 \wedge y_1) \vee \cdots \vee (x_k \wedge y_k)$ it gives $2^k$ clauses of width $k$, none of which can be dropped. The Tseitin form of the same formula uses $k$ new variables $t_i \leftrightarrow (x_i \wedge y_i)$ and $3k + 1$ clauses.

The dual form, DNF, is a disjunction of conjunctions. Satisfiability of a DNF is easy, since one consistent term is enough, but deciding whether a DNF is a tautology is coNP-complete, which is the same problem as unsatisfiability of a CNF. Conversely, a CNF is a tautology exactly when each of its clauses is.

## Related definitions

- **[Clause](/clause/) and [literal](/literal/).** The parts of a CNF.
- **[Boolean satisfiability problem](/sat/).** Decide whether a CNF has a model.
- **[DIMACS CNF format](/dimacs-cnf-format/).** The standard text file for a CNF.
- **[Tseitin transformation](/tseitin-transformation/).** The linear-size equisatisfiable conversion from formulas and [Boolean circuits](/boolean-circuit/), the link between [Circuit-SAT](/circuit-sat/) and SAT.
- **Horn and 2-CNF.** CNFs with at most one positive literal per clause, or at most two literals per clause. Their satisfiability is in linear time, see [Horn-SAT](/horn-sat/) and [2-SAT](/2-sat/).
- **[Clausal normal form](/clausal-normal-form/).** The first-order counterpart, after Skolemization.

## References
