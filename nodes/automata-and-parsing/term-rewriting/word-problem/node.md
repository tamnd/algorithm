---
tag: 02199F
kind: problem
slug: word-problem
name: Word problem (equational)
aliases:
- identity problem
- equational word problem
- uniform word problem
area: automata-and-parsing/term-rewriting
level: advanced
summary: Decide whether two terms are equal in a given equational theory or rewriting system.
prereqs: [equational-theory, term-rewriting-system]
see_also: [undecidability-of-word-problem, word-problem-for-groups, knuth-bendix-completion, congruence-closure, birkhoff-completeness-theorem, string-rewriting-system, rewriting-modulo-equations, unfailing-completion]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.1, Deciding ≈E; Section 4.3, Congruence closure; Section 5.1.1, Undecidability in the general case; Chapter 7, Completion
  - paper: doi:10.1145/322217.322228
    title: Peter J. Downey, Ravi Sethi and Robert E. Tarjan, Variations on the common subexpression problem, Journal of the ACM 27(4) (1980)
    locator: pp. 758 to 771 (congruence closure in O(n log n) time, which decides the word problem for ground equations)
  - paper: doi:10.1016/0001-8708(82)90048-2
    title: Ernst W. Mayr and Albert R. Meyer, The complexity of the word problems for commutative semigroups and polynomial ideals, Advances in Mathematics 46(3) (1982)
    locator: pp. 305 to 329 (the uniform word problem for commutative semigroups is EXPSPACE-complete)
  - book: isbn:9780387979656
    title: Ronald V. Book and Friedrich Otto, String-Rewriting Systems, Springer, 1993
    locator: the chapters String-rewriting systems and Decision problems (word problems of Thue systems)
---

The **word problem** for a set of equations $E$ asks whether two given terms are equal in every algebra that satisfies $E$, that is, whether $s \approx_E t$. It is the basic question of equational reasoning, and many questions reduce to it: equality in a group given by generators and relations, equivalence of two programs under algebraic laws, or validity of an identity. It is semi-decidable, since proofs can be enumerated, but undecidable in general, already for a fixed finite $E$. It is decidable when $E$ has a finite [convergent](/confluence/) rewrite system, which [Knuth-Bendix completion](/knuth-bendix-completion/) tries to build, and for ground equations, by [congruence closure](/congruence-closure/) in $O(n \log n)$ time.

## In plain words

You are given some laws, such as "x times one equals x", and two expressions. The question is whether the laws force the two expressions to be equal: can you turn one into the other by replacing parts with equal parts, a law at a time?

If the answer is yes, a proof exists and a patient search will find it. If the answer is no, the search may never end, and in general no program can tell the two cases apart. For many useful sets of laws, though, the laws can be turned into one-way simplification rules that always end in a unique simplest form. Then you simplify both expressions and compare the results.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure. $\approx_E$ is the [equational theory](/equational-theory/) of $E$: the smallest congruence on $T(\Sigma, V)$ that contains every instance $l\sigma \approx r\sigma$ of an equation in $E$. Equivalently, $\approx_E = \leftrightarrow_E^*$, where $\leftrightarrow_E$ replaces an instance of one side of an equation by the same instance of the other side, anywhere in a term.

**Input.** A finite set $E$ of equations over $\Sigma$, and two terms $s, t \in T(\Sigma, V)$.

**Question.** Is $s \approx_E t$?

By the [Birkhoff completeness theorem](/birkhoff-completeness-theorem/), $s \approx_E t$ iff the equation $s \approx t$ holds in every $\Sigma$-algebra that satisfies $E$, for all values of the variables. So the syntactic question (is there a chain of replacements) and the semantic question (is it a law of all models) have the same answer. The variables of $s$ and $t$ behave as constants: $s \approx_E t$ iff $\hat s \approx_E \hat t$, where each variable is replaced by a new constant.

## Variants

- **Fixed theory.** $E$ is fixed and only $s, t$ are input: the word problem *for* $E$. The theory of groups, rings, lattices or a specific finitely presented group each give one problem.
- **Uniform word problem.** $E$ is part of the input, as in the definition above, often restricted to a class: ground equations, string equations, or equations together with a fixed theory such as commutative semigroups.
- **Ground word problem.** $E$ and $s, t$ are ground. This is the problem solved by [congruence closure](/congruence-closure/).
- **Word problem for monoids and groups.** With unary symbols only, terms are strings and $E$ is a Thue system; see [string rewriting system](/string-rewriting-system/) and [word problem for groups](/word-problem-for-groups/). The name "word problem" comes from this case.
- **Modulo a built-in theory.** Decide $\approx_{R \cup E}$ with rules $R$ and a theory $E$ such as associativity and commutativity, as in [rewriting modulo equations](/rewriting-modulo-equations/).
- **Inductive validity.** Decide whether $s \approx t$ holds for all ground instances, a different and harder question; see [inductive theorem proving](/inductive-theorem-proving/).

## Examples

All results below were checked by programs.

**Groups.** With $E$ the three group axioms $e \cdot x \approx x$, $x^{-1} \cdot x \approx e$, $(x \cdot y) \cdot z \approx x \cdot (y \cdot z)$, completion gives the classic convergent system of 10 rules: the three axioms oriented left to right, plus $x^{-1} \cdot (x \cdot z) \to z$, $e^{-1} \to e$, $x \cdot e \to x$, $(x^{-1})^{-1} \to x$, $x \cdot x^{-1} \to e$, $x \cdot (x^{-1} \cdot z) \to z$ and $(x \cdot y)^{-1} \to y^{-1} \cdot x^{-1}$. All 55 critical pairs of these rules are joinable. To decide $(x^{-1} \cdot (y \cdot x))^{-1} \approx x^{-1} \cdot (y^{-1} \cdot x)$, normalize both sides: both become $x^{-1} \cdot (y^{-1} \cdot x)$, so the identity holds in all groups. The terms $x \cdot y$ and $y \cdot x$ are distinct normal forms, so commutativity is not a law of groups.

**Ground equations.** $E = \{f^3(a) \approx a,\ f^5(a) \approx a\}$. Congruence closure over the 6 subterms $a, f(a), \ldots, f^5(a)$ merges classes until $f(a) \approx_E a$: from $f^3(a) \approx a$ follows $f^5(a) \approx f^2(a)$, so $f^2(a) \approx a$, and then $f^3(a) \approx f(a)$, so $f(a) \approx a$.

**Not every decidable theory has a convergent system.** Commutativity $x \cdot y \approx y \cdot x$ has a decidable word problem (sort the arguments and compare), but no terminating rewrite system for it, since any rule from it can be reversed. The monoid $\langle a, b \mid aba = bab \rangle$ has a decidable word problem but no finite convergent string rewriting system over $\{a, b\}$; see [string rewriting system](/string-rewriting-system/).

## Known algorithms

- **Proof search.** Enumerate all chains $s = u_0 \leftrightarrow_E u_1 \leftrightarrow_E \cdots$ breadth-first. This halts with "yes" iff $s \approx_E t$, and may run forever otherwise. It shows that the problem is recursively enumerable.
- **Normal forms of a convergent system.** If $R$ is finite and convergent and $\approx_R = \approx_E$, then $s \approx_E t$ iff the [normal forms](/normal-form/) of $s$ and $t$ are equal. The cost is the cost of normalizing, which depends on $R$ and can be large.
- **Completion.** [Knuth-Bendix completion](/knuth-bendix-completion/) tries to turn $E$ into such an $R$. It can fail on an equation that the order cannot orient, or run forever. [Unfailing completion](/unfailing-completion/) never fails for lack of orientation, and gives a semi-decision procedure that is a decision procedure when it terminates.
- **Congruence closure.** For ground $E$, $s$ and $t$: build the [term DAG](/term-dag/) of all subterms, merge the two sides of each equation, and merge two nodes $f(u_1, \ldots, u_n)$, $f(v_1, \ldots, v_n)$ whenever all their arguments are merged. With union-find and a signature table this takes $O(n \log n)$ time (Downey, Sethi and Tarjan, 1980).
- **Theory-specific procedures.** Commutative semigroups and polynomial ideals: Gröbner bases. Free groups: free reduction of words. Abelian groups and AC theories: normal forms modulo AC.

## Bounds

- **General case.** The problem is complete for the recursively enumerable sets: the proof search places it there, and reductions from the [halting problem](/halting-problem/) show hardness. There is a fixed finite $E$ whose word problem is undecidable, already for semigroups (Post and Markov, 1947); see [undecidability of the word problem](/undecidability-of-word-problem/).
- **Ground equations.** $O(n \log n)$ time, where $n$ is the total size of $E$, $s$ and $t$.
- **Commutative semigroups.** The uniform word problem for finitely presented commutative semigroups is EXPSPACE-complete (Mayr and Meyer, 1982); it is the reachability problem of reversible [Petri nets](/petri-net/).
- **Convergent systems.** Decidable, but with no general bound on time: with a convergent system that computes the [Ackermann function](/ackermann-function/), normalizing can take longer than any primitive recursive function of the input size.

## Reductions

- **Halting problem to word problem.** A Turing machine is encoded as a string rewriting system whose Thue congruence relates an initial configuration to a halting one iff the machine halts; see [undecidability of the word problem](/undecidability-of-word-problem/).
- **Word problem to matching and unification modulo $E$.** For ground $s$, $s$ matches $t$ modulo $E$ iff $s \approx_E t$. So $E$-matching and [unification modulo $E$](/undecidability-of-unification-modulo-theories/) are at least as hard as the word problem.
- **Group word problem.** A group presentation $\langle X \mid R \rangle$ gives $E$ = group axioms plus the relators, and the [word problem for groups](/word-problem-for-groups/) is this word problem for ground terms.

## Applications

- Automated reasoning: equational theorem provers and [superposition](/superposition/) provers decide or semi-decide instances of the word problem.
- SMT solvers: congruence closure decides equality with uninterpreted functions, a core theory of every SMT solver.
- Algebraic specification: two expressions of an abstract data type denote the same value iff they are equal in the theory of its equations.
- Computational group theory: Knuth-Bendix completion for monoid and group presentations, and automatic groups.
- Compilers: common subexpression elimination and value numbering decide ground equalities between expressions.

## References
