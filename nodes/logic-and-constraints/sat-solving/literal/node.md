---
tag: VKZ8D5
kind: definition
slug: literal
name: Literal
aliases:
- propositional literal
- signed variable
area: logic-and-constraints/sat-solving
level: intro
summary: A Boolean variable x or its negation ¬x. Literals are the atoms of clauses, CNF formulas and SAT solvers.
prereqs: [boolean-function]
see_also: [clause, conjunctive-normal-form, dimacs-cnf-format, unit-clause, pure-literal-elimination, phase-saving, sat]
sources:
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the opening definitions of literals, clauses and the internal coding of literals as 2k and 2k + 1
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, 2016
    locator: Chapter 1, Section 1.3 (normal forms; literals, negation normal form and CNF)
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 2, CNF Encodings, by Steven Prestwich (literals, clauses and CNF)
  - paper: doi:10.1145/321033.321034
    title: Martin Davis and Hilary Putnam, A computing procedure for quantification theory, Journal of the ACM 7(3), 1960
    locator: pages 201 to 215 (formulas in conjunctive normal form over literals, and the rules for one-literal clauses and pure literals)
---

A literal is a Boolean variable $x$ or its negation $\neg x$. The first is a positive literal and the second a negative one, and the two are complements of each other. Literals are the atoms from which [clauses](/clause/) and [CNF formulas](/conjunctive-normal-form/) are built, so every SAT solver works on them: it assigns them, watches them, and counts them. Solvers code a literal as a signed integer in the [DIMACS format](/dimacs-cnf-format/) and as a small non-negative integer inside their arrays.

## Definition

Let $V = \{x_1, \ldots, x_n\}$ be a set of Boolean variables.

**Literal.** A literal over $V$ is $x_i$ or $\neg x_i$ for some $i$. There are $2n$ literals. The variable of a literal is $\mathrm{var}(x_i) = \mathrm{var}(\neg x_i) = x_i$.

**Complement.** The complement of a literal $\ell$ is $\bar\ell$, with $\overline{x_i} = \neg x_i$ and $\overline{\neg x_i} = x_i$. So $\bar{\bar\ell} = \ell$, and $\ell$ and $\bar\ell$ are the two literals of one variable. Many texts write $\neg\ell$ for $\bar\ell$ and treat $\neg\neg x$ as $x$.

**Value.** A total assignment $\alpha : V \to \{0, 1\}$ gives each literal a value: $\alpha(x_i)$ as given, and $\alpha(\neg x_i) = 1 - \alpha(x_i)$. So exactly one of $\ell$ and $\bar\ell$ is true.

**Partial assignment.** A partial assignment is a set $\tau$ of literals that holds no literal together with its complement. Under $\tau$, a literal $\ell$ is *true* if $\ell \in \tau$, *false* if $\bar\ell \in \tau$, and *unassigned* otherwise. A total assignment is a partial assignment with $n$ literals. This is the form a solver's trail has: the list of true literals in the order of assignment.

**Polarity.** The polarity, sign or phase of a literal is positive for $x_i$ and negative for $\neg x_i$. A literal $\ell$ is *pure* in a formula $F$ when $\ell$ occurs in $F$ and $\bar\ell$ does not.

**Coding.** In the DIMACS format, $x_i$ is the integer $i$ and $\neg x_i$ is $-i$. Inside a solver, $x_i$ is often $2i$ and $\neg x_i$ is $2i + 1$, as in Knuth's programs; MiniSat does the same with variables counted from 0. Then the complement is one exclusive or with 1, the variable is a shift by one bit, and the codes $2, \ldots, 2n + 1$ index arrays such as the watch lists directly.

## Examples and non-examples

| object | literal? | why |
|---|---|---|
| $x_3$ | yes | a positive literal |
| $\neg x_7$ | yes | a negative literal; its complement is $x_7$ |
| $\neg\neg x_2$ | yes, as $x_2$ | double negation is removed |
| $x_1 \wedge x_2$ | no | a conjunction of two literals |
| $x_1 \vee \neg x_2$ | no | a [clause](/clause/) of two literals |
| the constant true | no | constants are not variables; a formula with constants is simplified first |
| $x \oplus y$ | no | an exclusive or of two variables, the atom of [XOR-SAT](/xor-sat/) |

The codes of some literals:

| literal | DIMACS | internal code $2i$ or $2i + 1$ | complement code |
|---|---|---|---|
| $x_1$ | 1 | 2 | 3 |
| $\neg x_1$ | $-1$ | 3 | 2 |
| $x_5$ | 5 | 10 | 11 |
| $\neg x_5$ | $-5$ | 11 | 10 |

Under the partial assignment $\tau = \{x_1, \neg x_3\}$ over $\{x_1, x_2, x_3\}$, the literals $x_1$ and $\neg x_3$ are true, $\neg x_1$ and $x_3$ are false, and $x_2$ and $\neg x_2$ are unassigned. The set $\{x_1, \neg x_1\}$ is not a partial assignment. In the formula $\{x_1, x_2\}, \{\neg x_2, x_3\}, \{x_1, \neg x_3\}$, the literal $x_1$ is pure, and no literal of $x_2$ or $x_3$ is.

In first-order logic, a literal is an atomic formula $P(t_1, \ldots, t_k)$ or its negation, as in the [clausal normal form](/clausal-normal-form/) of [resolution](/robinson-resolution/) provers. This page is about the propositional case.

## Related definitions

- **[Clause](/clause/).** A finite set of literals, read as their disjunction. A clause that holds $\ell$ and $\bar\ell$ is a tautology.
- **[Conjunctive normal form](/conjunctive-normal-form/).** A conjunction of clauses, the input form of SAT solvers.
- **[Unit clause](/unit-clause/).** A clause with one literal left that is not false, which forces that literal.
- **Pure literal.** A literal whose complement does not occur. [Pure literal elimination](/pure-literal-elimination/) makes it true.
- **Saved phase.** The last polarity a variable had on the trail, which [phase saving](/phase-saving/) reuses at the next decision.
- **[Horn clause](/horn-clause/).** A clause with at most one positive literal.

## References
