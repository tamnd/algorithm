---
tag: EF3FV1
kind: problem
slug: undecidability-of-unification-modulo-theories
name: Unification modulo theories
aliases:
- unification modulo equations
area: automata-and-parsing/term-rewriting
level: research
summary: Unification relative to a fixed equational theory such as associativity and commutativity.
prereqs: [equational-theory, most-general-unifier, hilberts-tenth-problem]
see_also: [equational-unification, ac-unification-problem, stickel-ac-unification, narrowing, higher-order-unification-undecidability, word-problem, birkhoff-completeness-theorem, robinson-unification]
sources:
  - paper: doi:10.1016/S0747-7171(89)80012-4
    title: Jörg H. Siekmann, Unification theory, Journal of Symbolic Computation 7(3 and 4) (1989)
    locator: pp. 207 to 274 (survey; complete sets of unifiers, unification types, and results for particular theories such as associativity and commutativity)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 10, Equational unification (10.1 basic definitions and unification types, 10.2 commutative functions, 10.3 associative and commutative functions)
  - paper: doi:10.1070/SM1977v032n02ABEH002376
    title: G. S. Makanin, The problem of solvability of equations in a free semigroup, Mathematics of the USSR-Sbornik 32(2) (1977)
    locator: pp. 129 to 198
  - paper: doi:10.1080/00029890.1973.11993265
    title: Martin Davis, Hilbert's tenth problem is unsolvable, American Mathematical Monthly 80(3) (1973)
    locator: pp. 233 to 269 (every recursively enumerable set is Diophantine, so solvability of Diophantine equations is undecidable)
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1) (1965)
    locator: pp. 23 to 41 (the unification algorithm and the most general unifier for the empty theory)
---

**Unification modulo a theory** $E$ asks, for two terms $s$ and $t$, whether some substitution $\sigma$ makes $s\sigma$ and $t\sigma$ equal in the equational theory of $E$, and if so, for a set of such substitutions from which all others follow. For the empty theory this is syntactic unification, which is decidable and has a most general unifier. For other theories the answer can be finite, infinite, or undecidable: unification modulo associativity has infinitely many independent solutions, and there is one fixed convergent rewrite system, the usual rules for $+$ and $\times$ on unary numbers, modulo which unification is undecidable, because it can express Hilbert's tenth problem.

## In plain words

Ordinary unification fills in the unknowns in two expressions so that they become the same text. Unification modulo a theory makes them the same up to some laws, such as "the order of the two inputs of an addition does not matter". The laws make more pairs match, but they make the problem harder. With the order law, one problem can have two different best answers instead of one. With the grouping law, one problem can have infinitely many. With the laws of arithmetic, asking whether two expressions can be made equal is the same as asking whether an equation in whole numbers has a solution, and no program can answer that question in general.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, rules $l \to r$, $\to^*$ for the reflexive transitive closure, positions as sequences of positive integers, and substitutions $\sigma$. For a set $E$ of equations, $s =_E t$ means that $s$ and $t$ are equal in the [equational theory](/equational-theory/) of $E$; by [Birkhoff's theorem](/birkhoff-completeness-theorem/) this is the same as $s \leftrightarrow_E^* t$.

**Problem.** Given a set $E$ of equations over $\Sigma$, an **$E$-unification problem** is a finite set of pairs $s_1 \doteq_E t_1, \dots, s_n \doteq_E t_n$. A substitution $\sigma$ is an **$E$-unifier** if $s_i\sigma =_E t_i\sigma$ for every $i$. The **decision problem** asks whether an $E$-unifier exists. For a fixed $E$, the input is the problem; in the **uniform** version, $E$ is part of the input.

**Generality.** For a finite set $W$ of variables, $\sigma \leq_E^W \theta$ ($\sigma$ is more general than $\theta$ on $W$) if there is a $\rho$ with $x\theta =_E x\sigma\rho$ for every $x \in W$. A **complete set of $E$-unifiers** of a problem with variables $W$ is a set $C$ of $E$-unifiers such that every $E$-unifier $\theta$ has some $\sigma \in C$ with $\sigma \leq_E^W \theta$. It is **minimal** if no two different members are comparable by $\leq_E^W$.

**Unification type.** A theory $E$ is

- **unitary** if every solvable problem has a minimal complete set with one element, a most general $E$-unifier;
- **finitary** if every solvable problem has a finite minimal complete set, and some has more than one element;
- **infinitary** if every solvable problem has a minimal complete set, and some has only infinite ones;
- **of type zero** if some solvable problem has no minimal complete set.

Baader and Nipkow (Section 10.1) and Siekmann (1989) define these types and give examples of each.

## Variants

- **Elementary, with constants, and general.** In **elementary** unification the terms use only the symbols of $E$. **Unification with constants** adds free constants, symbols that occur in no equation. **General** unification adds free function symbols of any arity. A theory can be easier in one variant than in another, so a result must say which one it is about.
- **Matching.** Only the variables of $s$ may be instantiated, and $t$ is fixed: find $\sigma$ with $s\sigma =_E t$. This is the problem solved at each step of [rewriting modulo equations](/rewriting-modulo-equations/); for associativity and commutativity see [AC matching](/ac-matching/).
- **Ground terms.** If $s$ and $t$ have no variables, the problem is the [word problem](/word-problem/) for $E$.
- **Theory given by a convergent system.** $E$ is presented by a [confluent](/confluence/) and [terminating](/termination/) rewrite system, possibly modulo axioms such as commutativity.
- **Higher order.** The terms are simply typed λ-terms and $E$ is β-η equality; this is [higher-order unification](/higher-order-unification-undecidability/), undecidable already at second order.

## Examples

**The empty theory.** With $E = \emptyset$, $f(x, g(y)) \doteq g(z)$ has no unifier because the root symbols differ, and $f(x, g(y)) \doteq f(g(z), x)$ has the [most general unifier](/most-general-unifier/) $\{x \mapsto g(y), z \mapsto y\}$. Robinson (1965) showed that every solvable problem has a most general unifier, so the empty theory is unitary.

**Commutativity: two answers.** Let $C = \{f(x, y) = f(y, x)\}$ and let $a$ and $b$ be free constants. The problem $f(x, y) \doteq_C f(a, b)$ has the two unifiers $\{x \mapsto a, y \mapsto b\}$ and $\{x \mapsto b, y \mapsto a\}$. Every unifier is one of them on $\{x, y\}$: the class of $f(a, b)$ modulo $C$ is $\{f(a, b), f(b, a)\}$, so $x\sigma$ and $y\sigma$ are $a$ and $b$ in some order. The two are ground and different, so neither is more general than the other, and there is no most general unifier. Commutativity is finitary (Baader and Nipkow, Section 10.2).

**Associativity: infinitely many answers.** Let $A = \{(x \cdot y) \cdot z = x \cdot (y \cdot z)\}$, so terms built from $\cdot$ and constants are words, and let $a$ and $b$ be free constants. The problem $x \cdot a \doteq_A a \cdot x$ has the unifiers $x \mapsto a^n$ for every $n \geq 1$, and only those among the ground ones: if $w a = a w$ for a word $w$, then $w$ starts with $a$, and removing that $a$ from both sides gives $w' a = a w'$ for the rest $w'$, so by induction $w$ is a power of $a$. A script that checks every word over $\{a, b\}$ up to length 8 finds exactly $a, aa, \dots, a^8$. Now suppose $\theta$ is a unifier more general than $x \mapsto a^n$. If $x\theta$ contained a variable, then $\theta$ followed by the substitution of $b$ for every variable would be a ground unifier whose value contains $b$, which is impossible. So $x\theta$ is ground, and $x\theta =_A a^n$. Hence every complete set contains, for each $n$, a unifier equal to $x \mapsto a^n$, and it is infinite. The set $\{x \mapsto a^n : n \geq 1\}$ is a minimal complete set, so this problem shows that associativity is not finitary; Siekmann (1989) reports that associativity is infinitary.

**Arithmetic: a solvable and an unsolvable problem.** Let $N$ be the convergent system on numerals $0, s(0), s(s(0)), \dots$:

$$x + 0 \to x \qquad x + s(y) \to s(x + y) \qquad x \times 0 \to 0 \qquad x \times s(y) \to (x \times y) + x.$$

Write $\underline{n}$ for the numeral $s^n(0)$. The problem $x \times x \doteq_N (\underline{2} \times (y \times y)) + \underline{1}$ asks for a solution of $x^2 = 2y^2 + 1$. A script that normalizes both sides with the four rules finds the unifiers $\{x \mapsto \underline{1}, y \mapsto \underline{0}\}$ and $\{x \mapsto \underline{3}, y \mapsto \underline{2}\}$ among $x, y < 8$, and confirms $\{x \mapsto \underline{17}, y \mapsto \underline{12}\}$, where both sides normalize to $\underline{289}$. The problem $x \times x \doteq_N \underline{2} \times (y \times y)$ has only $\{x \mapsto \underline{0}, y \mapsto \underline{0}\}$ among ground unifiers, since $\sqrt 2$ is irrational. In general, no algorithm can tell which problems over $N$ are solvable; the proof is in the section on reductions.

**Commutative rings: a decidable word problem but undecidable unification.** Let $E$ be the axioms of commutative rings with $1$, over $+$, $\times$, $-$, $0$ and $1$. Then $s =_E t$ exactly when $s$ and $t$ are the same polynomial with integer coefficients, which can be checked by expanding both sides. The problem $x \times x + y \times y \doteq_E 1 + 1 + 1 + 1 + 1$ has the unifier $\{x \mapsto 1 + 1, y \mapsto 1\}$, while $x \times x + y \times y \doteq_E 1 + 1 + 1$ has none, because $3$ is not a sum of two integer squares.

## Known algorithms

- **The empty theory.** [Robinson's algorithm](/robinson-unification/) computes a most general unifier or reports failure. The [Martelli-Montanari](/martelli-montanari-unification/) rules give the same result as a set of transformations, and the [Paterson-Wegman](/paterson-wegman-unification/) algorithm runs in linear time.
- **Commutativity.** The decomposition step of syntactic unification is replaced by a choice: $f(s_1, s_2) \doteq_C f(t_1, t_2)$ becomes either $s_1 \doteq t_1, s_2 \doteq t_2$ or $s_1 \doteq t_2, s_2 \doteq t_1$. Collecting the solved forms over all choices gives a finite complete set (Baader and Nipkow, Section 10.2).
- **Associativity and commutativity.** [Stickel's algorithm](/stickel-ac-unification/) flattens the AC symbols, reduces the problem to a system of linear Diophantine equations over the natural numbers, and builds the unifiers from a basis of its solutions. See the [AC unification problem](/ac-unification-problem/) and Baader and Nipkow, Section 10.3.
- **Associativity.** Unification with constants modulo $A$ is the solvability of word equations, which Makanin (1977) proved decidable. Since the type is infinitary, an algorithm that lists a complete set of unifiers cannot always stop; it can only enumerate.
- **A convergent system.** If $E$ is presented by a convergent rewrite system, [narrowing](/narrowing/) enumerates a complete set of $E$-unifiers. It is a semi-decision procedure: it finds a unifier when one exists, and need not stop when none exists.
- **Any finite $E$.** Enumerate all pairs of a substitution $\sigma$ and a proof by equational replacement of $s\sigma = t\sigma$ from $E$. By Birkhoff's theorem this finds a unifier whenever one exists, so the set of solvable problems is recursively enumerable for every finite $E$.

## Bounds

**Undecidable in general.** There is a fixed convergent system $N$, given above, such that the set of solvable $N$-unification problems is undecidable. The same holds for the theory of commutative rings with $1$, elementary unification, although its word problem is decidable. These follow from the reductions below and the undecidability of Hilbert's tenth problem.

**Exactly the recursively enumerable degree.** For a finite $E$ the solvable problems form a recursively enumerable set, by the last algorithm above. By the theorem of Matiyasevich, Robinson, Davis and Putnam (Davis 1973), every recursively enumerable set is Diophantine, so the solvable Diophantine equations form a set to which every recursively enumerable set reduces. The reductions below carry this over, so unification modulo $N$ is complete for the recursively enumerable sets.

**Decidable cases.** For the empty theory, unifiability is decidable in linear time. For commutativity and for associativity with commutativity the theory is finitary and the complete sets can be computed, so unifiability is decidable; for AC it is NP-hard (see the [AC unification problem](/ac-unification-problem/)). For associativity it is decidable by Makanin's algorithm, although no finite complete set exists in general.

**Type is not decidability.** The type and the decidability are independent: associativity is infinitary and decidable, while $N$ is a convergent system whose unification problem is undecidable. A theory with a decidable [word problem](/word-problem/), such as commutative rings, can still have an undecidable unification problem.

## Reductions

**From Hilbert's tenth problem to unification modulo $N$.** [Hilbert's tenth problem](/hilberts-tenth-problem/) over the natural numbers asks whether a polynomial equation $P(x_1, \dots, x_k) = 0$ with integer coefficients has a solution in natural numbers. It is undecidable (Davis 1973). Move the monomials with negative coefficients to the other side, so the equation becomes $p = q$ where $p$ and $q$ have natural coefficients, and write $p$ and $q$ as terms $\hat p$ and $\hat q$ over $0$, $s$, $+$ and $\times$. Then $P = 0$ has a solution in the natural numbers iff $\hat p \doteq_N \hat q$ has an $N$-unifier.

*Proof.* The system $N$ terminates, and its rules are left-linear and do not overlap, so it is confluent, and every ground term rewrites to a numeral $\underline{n}$, since a ground term with $+$ or $\times$ at an innermost position has numeral arguments and is a redex. Each rule preserves the value of a ground term in the natural numbers, so a ground term $u$ normalizes to $\underline{v(u)}$, where $v(u)$ is its value. If $(n_1, \dots, n_k)$ is a solution, then $\sigma = \{x_i \mapsto \underline{n_i}\}$ gives $v(\hat p\sigma) = p(\vec n) = q(\vec n) = v(\hat q\sigma)$, so both sides normalize to the same numeral and $\sigma$ is an $N$-unifier. Conversely, let $\sigma$ be an $N$-unifier, and let $\tau$ map every variable to $0$. The relation $=_N$ is closed under substitutions, so $\hat p\sigma\tau =_N \hat q\sigma\tau$, and these are ground terms. Let $n_i = v(x_i\sigma\tau)$. Then $p(\vec n) = v(\hat p\sigma\tau) = v(\hat q\sigma\tau) = q(\vec n)$, because ground terms equal modulo $N$ have the same normal form and so the same value. $\square$

**From Hilbert's tenth problem to commutative rings.** The same argument works over the integers: an elementary unifier for $p \doteq_E q$ modulo the theory of commutative rings with $1$, followed by the substitution of $0$ for all variables, gives ground terms, which are integers modulo $E$; and an integer solution gives a unifier that maps $x_i$ to $1 + \dots + 1$ or its negative. Hilbert's tenth problem over the integers is also undecidable, since $n$ ranges over the natural numbers iff it is a sum of four integer squares.

**From the word problem.** A problem $s \doteq_E t$ with ground $s$ and $t$ is solvable iff $s =_E t$. So a theory with an undecidable [word problem](/word-problem/) has undecidable unification, already for ground problems; see the [undecidability of the word problem](/undecidability-of-word-problem/). The converse fails, as commutative rings show.

**From matching.** Matching $s\sigma =_E t$ reduces to unification by replacing each variable of $t$ by a new free constant, so that it cannot be instantiated.

## Applications

- **Theorem proving with built-in theories.** Resolution and [paramodulation](/paramodulation/) use unification to find clashing literals. Replacing syntactic unification by $E$-unification lets a prover treat the axioms of $E$, such as commutativity, without using them as clauses, which would cause many redundant inferences. The complete set of unifiers then replaces the most general unifier, and it must be finite for each inference to have finitely many conclusions.
- **Completion modulo theories.** [Rewriting modulo equations](/rewriting-modulo-equations/) and completion modulo AC compute critical pairs with AC-unifiers instead of most general unifiers.
- **Symbolic execution of rewrite theories.** [Narrowing](/narrowing/) modulo axioms in [rewriting logic](/rewriting-logic/) computes the states reachable from a term with variables. Each narrowing step solves a unification problem modulo the axioms.

## References
