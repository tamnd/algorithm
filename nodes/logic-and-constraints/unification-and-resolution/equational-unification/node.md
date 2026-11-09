---
tag: 754QAV
kind: problem
slug: equational-unification
name: Equational unification
aliases:
- E-unification
- E-unification problem
- equational unification
- unification modulo E
area: logic-and-constraints/unification-and-resolution
level: research
summary: Find substitutions that make two terms equal modulo a set of equations, and classify theories by the shape of their solution sets.
prereqs: [unification-problem, most-general-unifier, equational-theory]
see_also: [ac-unification-problem, stickel-ac-unification, undecidability-of-unification-modulo-theories, narrowing, rewriting-modulo-equations, higher-order-unification-problem, anti-unification-problem, ac-matching]
sources:
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 3 (E-unification, complete sets of unifiers, unification types, and the results for commutativity, associativity, AC and related theories)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 10, Equational unification (unification types, the syntactic approach and the semantic approach, commutative and associative-commutative theories)
  - paper: "G. D. Plotkin, Building-in equational theories, in B. Meltzer and D. Michie (editors), Machine Intelligence 7, Edinburgh University Press, 1972, pages 73 to 90"
    locator: building equational theories into resolution, complete sets of unifiers, and the example that associativity has infinitely many independent unifiers
  - paper: "M. E. Stickel, A unification algorithm for associative-commutative functions, Journal of the ACM 28(3), 1981, pages 423 to 434"
    locator: the first complete unification algorithm for AC theories, based on linear Diophantine equations
  - paper: "F. Fages, Associative-commutative unification, Journal of Symbolic Computation 3(3), 1987, pages 257 to 275"
    locator: the termination proof of Stickel's algorithm for terms with several AC symbols and free symbols
  - paper: "F. Baader, Unification in idempotent semigroups is of type zero, Journal of Automated Reasoning 2(3), 1986, pages 283 to 286"
    locator: the proof that the theory of idempotent semigroups has no minimal complete sets of unifiers
---

**Equational unification**, or **E-unification**, asks for substitutions that make two [terms](/term/) equal modulo an [equational theory](/equational-theory/) $E$, such as commutativity or associativity of a symbol. It generalizes the syntactic [unification problem](/unification-problem/), which is the case of the empty theory. The main difference is that a single [most general unifier](/most-general-unifier/) need not exist. Theories are classified by the shape of their solution sets into four **unification types**: unitary, finitary, infinitary and nullary. Whether a problem is solvable depends on the theory: it is decidable for commutativity, associativity and [associativity with commutativity](/ac-unification-problem/), and undecidable for some simple theories.

## In plain words

Ordinary unification fills the blanks of two patterns so that they become the same text. In equational unification, some rules say when two texts count as equal. For example, a rule can say that `x + y` and `y + x` are equal. Now the blanks only need to make the two patterns equal under these rules.

With such rules there can be several best answers, not one. The pattern `x + y` matches `a + b` by putting `a` in `x`, but also by putting `b` in `x`, and neither answer covers the other. For some rules, the best answers are finitely many. For others they are infinitely many, and for some there is no clean list of best answers at all. For some rules, no program can decide whether an answer exists.

## Definition

Notation: $E$ is a set of equations, $=_E$ is the least congruence that contains all instances of $E$, and $\sigma, \theta, \lambda$ are substitutions. $N$ is the size of the input.

**Input:** a set $E$ of equations, fixed in advance, and terms $s, t$ (or a finite set of equations $s_i \doteq_E t_i$).

**Output:** whether an **E-unifier** exists, that is, a substitution $\sigma$ with $s\sigma =_E t\sigma$. In the solving version, the output is a complete set of E-unifiers.

Let $X = \mathrm{Var}(s, t)$. The order modulo $E$ on $X$ is $\sigma \le_E^X \theta$ if there is $\lambda$ with $x\theta =_E x\sigma\lambda$ for each $x \in X$. A set $C$ of E-unifiers is **complete** if every E-unifier $\theta$ has some $\sigma \in C$ with $\sigma \le_E^X \theta$. A complete set is **minimal** if no two of its members are comparable. When minimal complete sets exist, they are unique up to the equivalence of their members.

**Unification types.** A theory $E$ is

- **unitary** if every solvable problem has a minimal complete set with one element, an mgu;
- **finitary** if every solvable problem has a finite minimal complete set, and some problem needs more than one element;
- **infinitary** if every solvable problem has a minimal complete set, and some problem has only infinite ones;
- **nullary**, or of type zero, if some solvable problem has no minimal complete set.

## Variants

- **Elementary, with constants, and general.** In elementary unification, the terms use only the symbols of $E$ and variables. Unification with constants also allows free constants. General unification allows any free function symbols. The type can change between these: for abelian monoids, elementary unification is unitary, but with constants $x + y \doteq a$ has the two incomparable solutions $\{x \mapsto a, y \mapsto 0\}$ and $\{x \mapsto 0, y \mapsto a\}$, so it is finitary.
- **E-matching.** Only $s$ is instantiated: $s\sigma =_E t$. For AC this is [AC matching](/ac-matching/).
- **Disunification and constraints.** Equations are combined with disequations or orderings.
- **Higher-order unification.** Unification of lambda terms modulo $\beta\eta$ conversion is a form of E-unification, and it is undecidable from order two. See [higher-order unification](/higher-order-unification-problem/).
- **Combined theories.** For theories over disjoint signatures, unification algorithms can be combined, by the method of Schmidt-Schauss and of Baader and Schulz.

## Examples

| theory | equations | type | example |
|---|---|---|---|
| empty | none | unitary | the syntactic mgu |
| C | $f(x, y) = f(y, x)$ | finitary | $f(x, y) \doteq f(a, b)$ has $\{x \mapsto a, y \mapsto b\}$ and $\{x \mapsto b, y \mapsto a\}$ |
| AC | A and C for $+$ | finitary | $x + x \doteq y + z$: Stickel's algorithm returns 5 unifiers |
| abelian groups | AC, unit, inverse | unitary | solved by integer linear algebra |
| A | $(x \cdot y) \cdot z = x \cdot (y \cdot z)$ | infinitary | $x \cdot a \doteq a \cdot x$ |
| idempotent semigroups | A and $x \cdot x = x$ | nullary | Baader 1986, Schmidt-Schauss 1986 |

**Associativity is infinitary (Plotkin 1972).** The equation $x \cdot a \doteq a \cdot x$ has the solutions $\sigma_n = \{x \mapsto a^n\}$ for $n \ge 1$, where $a^n$ is $a \cdot a \cdots a$. These are ground substitutions, so no two of them are comparable, and every solution is one of them, because a word $w$ with $wa = aw$ is a power of $a$. So the only complete set is the infinite set of all $\sigma_n$.

**Commutativity can need exponentially many unifiers.** The problem $f(x_1, y_1) \doteq f(a, b), \ldots, f(x_n, y_n) \doteq f(a, b)$ has $2^n$ ground solutions, one for each choice of order in each equation, and no two of them are comparable.

**AC.** For $x + x \doteq y + z$, the algorithm of [Stickel](/stickel-ac-unification/) builds a complete set from the minimal solutions of the linear Diophantine equation $2x' = y' + z'$, which are $(1, 0, 2)$, $(1, 1, 1)$ and $(1, 2, 0)$. One of the unifiers is $\{x \mapsto z_2, y \mapsto z_2, z \mapsto z_2\}$, and another is $\{x \mapsto z_1 + z_3, y \mapsto z_3 + z_3, z \mapsto z_1 + z_1\}$.

## Known algorithms

- **Syntactic theories.** For the empty theory, the algorithms of [Robinson](/robinson-unification/), [Martelli and Montanari](/martelli-montanari-unification/) and [Paterson and Wegman](/paterson-wegman-unification/).
- **Commutativity.** Decompose $f(s_1, s_2) \doteq f(t_1, t_2)$ in both orders and unify recursively. The result is a finite complete set.
- **AC.** [Stickel's algorithm](/stickel-ac-unification/) reduces each AC equation to a homogeneous [linear Diophantine equation](/linear-diophantine-equation/) over the natural numbers, combines its minimal solutions, and recurses. Fages (1987) proved that it terminates with several AC symbols and free symbols.
- **Associativity.** Plotkin's procedure enumerates an infinite complete set. Deciding solvability is the problem of word equations, solved by Makanin's algorithm (1977).
- **Abelian groups.** Solve a system of linear equations over the integers, for example with the [Hermite normal form](/hermite-normal-form/) or the [Smith normal form](/smith-normal-form/).
- **Convergent theories.** If $E$ is given by a convergent rewrite system, [narrowing](/narrowing/) enumerates a complete set of E-unifiers. It may not terminate.
- **Combination.** For disjoint theories with unification algorithms of the right kind, the Baader-Schulz method combines them.

## Bounds

- **Undecidability.** E-unification is undecidable for some finite theories. For the theory of commutative rings with free constants, solvability encodes [Hilbert's tenth problem](/hilberts-tenth-problem/), so it is undecidable. See [undecidability of unification modulo theories](/undecidability-of-unification-modulo-theories/).
- **C and AC.** Deciding solvability is NP-complete for commutativity and for AC (Kapur and Narendran 1992 for AC). Minimal complete sets of AC unifiers can be doubly exponential in the size of the problem.
- **A.** Solvability of word equations is decidable, and it is in PSPACE (Plandowski).
- **Semi-decidability.** If $=_E$ is recursively enumerable, so is the set of solvable problems: enumerate substitutions and equational proofs. Narrowing gives a better complete enumeration for convergent systems.

## Reductions

- **AC to linear Diophantine equations.** Elementary AC unification of $\sum a_i x_i \doteq \sum b_j y_j$ reduces to the equation $\sum a_i x_i' = \sum b_j y_j'$ over the natural numbers, by counting the occurrences of each new variable. See the [AC unification problem](/ac-unification-problem/).
- **Abelian groups to integer linear algebra.** The same counting gives linear equations over the integers.
- **A to word equations.** A term over an associative symbol is a word, so A-unification is the solving of word equations.
- **Hilbert's tenth problem to ring unification.** A polynomial equation with integer coefficients becomes a unification problem modulo commutative rings.
- **Syntactic unification as a special case.** With $E = \emptyset$, every problem is unitary and the mgu of the [unification theorem](/mgu-existence-theorem/) is the minimal complete set.

## Applications

- **Theorem proving with built-in theories.** Plotkin (1972) proposed building theories such as AC into resolution, so that the axioms do not have to be used as clauses. Provers based on [superposition](/superposition/) and [paramodulation](/paramodulation/) use AC unification for this.
- **Rewriting and completion modulo theories.** [Rewriting modulo equations](/rewriting-modulo-equations/) and [completion](/knuth-bendix-completion/) modulo AC compute critical pairs with AC unification.
- **Rewriting languages.** Languages based on rewriting logic, such as Maude, support matching and unification modulo theories built from associativity, commutativity and unit elements.
- **Protocol analysis.** Tools for cryptographic protocols use unification modulo theories of exclusive or, of Diffie-Hellman exponentiation, and of abelian groups.
- **Type systems.** Unification modulo the theory of records or of dimensions appears in type inference for record types and for units of measure.

## References
