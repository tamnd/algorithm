---
tag: QVH7RA
kind: problem
slug: rewrite-system-completion
name: Rewrite system completion
aliases:
- completion problem
- finite convergent presentation
area: automata-and-parsing/term-rewriting
level: advanced
summary: Given equations, find a confluent and terminating rewrite system with the same equational theory.
prereqs: [knuth-bendix-completion, word-problem]
see_also: [unfailing-completion, critical-pair-lemma, well-founded-reduction-ordering, lexicographic-path-ordering, rewriting-modulo-equations, congruence-closure, string-rewriting-system, undecidability-of-word-problem]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 7, Completion
  - paper: doi:10.1016/0022-0000(81)90002-7
    title: Gérard Huet, A complete proof of correctness of the Knuth-Bendix completion algorithm, Journal of Computer and System Sciences 23(1) (1981)
    locator: pp. 11 to 21
  - paper: doi:10.1016/0020-0190(83)90009-1
    title: Yves Métivier, About the rewriting systems produced by the Knuth-Bendix completion algorithm, Information Processing Letters 16(1) (1983)
    locator: pp. 31 to 34 (reduced convergent systems contained in one reduction order are unique up to renaming)
  - paper: doi:10.1145/138027.138032
    title: Jean Gallier, Paliath Narendran, David Plaisted, Stan Raatz and Wayne Snyder, An algorithm for finding canonical sets of ground rewrite rules in polynomial time, Journal of the ACM 40(1) (1993)
    locator: pp. 1 to 16
  - paper: doi:10.1007/3-540-51081-8_123
    title: Wayne Snyder, Efficient ground completion, Rewriting Techniques and Applications (RTA 1989), Lecture Notes in Computer Science 355
    locator: pp. 419 to 433 (ground completion in O(n log n) time)
---

The **completion problem** asks, for a finite set of equations $E$, for a finite [convergent](/confluence/) rewrite system $R$ that has the same equational theory: $\approx_R = \approx_E$. Such an $R$ decides the [word problem](/word-problem/) for $E$, because two terms are equal iff they have the same normal form. [Knuth-Bendix completion](/knuth-bendix-completion/) is the standard procedure for it, but the problem has no total algorithmic solution: some theories have no finite convergent system, some have one that completion with a given order cannot reach, and the theories with an undecidable word problem have none at all. For ground equations the problem is always solvable, in $O(n \log n)$ time.

## In plain words

You have a list of laws, and you want a set of one-way simplification rules that does the same job: two expressions are equal by the laws exactly when they simplify to the same final form. Each rule must make expressions smaller in some sense, so simplification always ends, and different orders of simplifying must never lead to different final forms.

Sometimes such rules exist and a program can find them by adding rules until all conflicts are resolved. Sometimes no finite set of rules works, and sometimes the program never stops adding rules. A law such as "x plus y equals y plus x" cannot be made one-way at all.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure. $\approx_E$ is the [equational theory](/equational-theory/) of $E$.

**Input.** A finite set $E$ of equations over $\Sigma$, and in the usual form of the problem a [reduction order](/well-founded-reduction-ordering/) $>$ on $T(\Sigma, V)$, given for example as a precedence for the [lexicographic path ordering](/lexicographic-path-ordering/).

**Output.** A finite rewrite system $R$ over $\Sigma$ such that

1. $\approx_R = \approx_E$ (same theory),
2. $l > r$ for each rule $l \to r$ of $R$ (so $R$ terminates),
3. $R$ is confluent.

The system is **reduced** if no right side is reducible and no left side is reducible by the other rules. For a fixed reduction order, a reduced convergent $R$ with properties 1 to 3 is unique up to renaming of variables (Métivier, 1983). So with the order fixed, the problem has at most one reduced answer, and the question is whether it is finite and how to compute it.

## Variants

- **Fixed order or any order.** With $>$ given, the answer is unique if it exists. Without it, the problem asks whether *some* reduction order admits a finite convergent system, a much less constrained search.
- **Ground completion.** $E$ consists of ground equations. A finite convergent ground system always exists, for a total order on ground terms.
- **String completion.** All symbols are unary, so $E$ is a Thue system and $R$ a [string rewriting system](/string-rewriting-system/); a finite convergent $R$ is a finite complete presentation of the monoid.
- **Completion modulo a theory.** Find $R$ convergent modulo a built-in theory such as associativity and commutativity; see [rewriting modulo equations](/rewriting-modulo-equations/).
- **Ordered completion.** Accept an $R$ together with unorientable equations used by ordered rewriting, as in [unfailing completion](/unfailing-completion/), which is convergent on ground terms.
- **Infinite but regular answers.** Accept an infinite $R$ described by a finite schema, which still decides the word problem when membership in $R$ is decidable.

## Examples

All results below were checked by a small completion program with the lexicographic path ordering.

**Groups.** $E = \{e \cdot x \approx x,\ x^{-1} \cdot x \approx e,\ (x \cdot y) \cdot z \approx x \cdot (y \cdot z)\}$ with precedence ${}^{-1} > \cdot > e$ completes to the 10 rules listed on the [word problem](/word-problem/) page, and every critical pair of those rules is joinable.

**Completion that does not stop.** $E = \{f(g(f(x))) \approx f(g(x))\}$ with precedence $f > g$ gives the rule $f(g(f(x))) \to f(g(x))$. Its overlap with itself at the inner $f$ gives the peak
$$f(g(g(f(x)))) \leftarrow f(g(f(g(f(x))))) \to f(g(f(g(x)))) \to f(g(g(x))),$$
and the new rule $f(g(g(f(x)))) \to f(g(g(x)))$. Continuing gives $f(g^n(f(x))) \to f(g^n(x))$ for every $n \ge 1$, one new rule per round. The limit is an infinite convergent system, and since its rules form a simple family, it still decides the word problem.

**Completion that fails.** For $E = \{x \cdot y \approx y \cdot x\}$, no reduction order can orient the equation in either direction, since one direction is a renaming of the other and a reduction order is closed under substitution. Completion fails at once, and no rewrite system for commutativity terminates.

**No finite answer, whatever the order.** The monoid $\langle a, b \mid aba = bab \rangle$ has no finite convergent string rewriting system over $\{a, b\}$; see [string rewriting system](/string-rewriting-system/). A finite one exists over a larger alphabet, so the answer can depend on the signature as well as the order.

**Ground equations.** $E = \{f(f(a)) \approx a,\ f(f(f(a))) \approx a\}$, with $f(a) > a$ in the order, completes to $\{f(a) \to a\}$.

## Known algorithms

- **Knuth-Bendix completion** (Knuth and Bendix, 1970; correctness proved by Huet, 1981). Orient equations with $>$, compute [critical pairs](/critical-pair-lemma/), add their normalized forms as new equations, and simplify. A fair run that does not fail produces in the limit a convergent system for $E$, and if the run terminates, that system is finite. See [Knuth-Bendix completion](/knuth-bendix-completion/).
- **Unfailing (ordered) completion.** Keeps unorientable equations and uses them only in the decreasing direction. It never fails, and its limit decides ground equations; see [unfailing completion](/unfailing-completion/).
- **Ground completion.** Congruence closure computes the classes of all subterms, and a convergent rule set is read off by mapping each term to the least term of its class. This is polynomial (Gallier and others, 1993), and Snyder (1989) gave an $O(n \log n)$ algorithm.
- **Completion modulo AC.** Uses AC-unification for critical pairs and adds extended rules; see [rewriting modulo equations](/rewriting-modulo-equations/).
- **Search over orders.** Tools run completion with many precedences, or with several orders at once, and stop when one run succeeds.

## Bounds

- **No total algorithm.** If every finite $E$ had a computable finite convergent $R$, the word problem would be decidable for every finite $E$, which is false by the [undecidability of the word problem](/undecidability-of-word-problem/). So completion must fail or run forever on some inputs, whatever procedure is used.
- **Ground case.** Always solvable, in $O(n \log n)$ time for input size $n$ (Snyder, 1989).
- **Cost when it succeeds.** Completion can produce systems far larger than $E$, and each round costs a critical pair computation over all pairs of rules, so even successful runs have no useful bound in terms of $|E|$.

## Reductions

- **Completion to word problem.** A finite convergent $R$ decides the word problem by normal forms, so completion is a method for the [word problem](/word-problem/), and undecidable word problems show completion cannot always succeed.
- **Ground completion and congruence closure.** Each solves the other: a convergent ground system gives the classes of the congruence, and the classes give a convergent ground system.
- **Confluence check as the inner step.** For a terminating $R$, confluence is decidable by joining critical pairs, by the [critical pair lemma](/critical-pair-lemma/) and Newman's lemma; completion repeats this check and repairs the failures.

## Applications

- Decision procedures for equational theories: groups, rings, Boolean rings modulo AC, and many algebraic specifications of data types.
- Computational group theory: Knuth-Bendix completion for monoid and group presentations, which yields normal forms of elements and, in good cases, automatic structures.
- Equational theorem proving: unfailing completion is the core of equational provers and of the superposition calculus.
- Program verification and compilers: completing simplification rules makes a simplifier confluent, so that its result does not depend on the order in which rules fire.

## References
