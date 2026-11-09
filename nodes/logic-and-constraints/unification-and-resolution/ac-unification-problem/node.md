---
tag: GGM2XV
kind: problem
slug: ac-unification-problem
name: Associative-commutative unification problem
aliases:
- AC-unification
- AC unification problem
area: logic-and-constraints/unification-and-resolution
level: research
summary: E-unification for theories with associative and commutative operators; finitary and decidable, NP-complete to decide, with complete sets that can be doubly exponential.
prereqs: [equational-unification, unification-problem, linear-diophantine-equation]
see_also: [stickel-ac-unification, ac-matching, linear-diophantine-system, rewriting-modulo-equations, knuth-bendix-completion, equational-theory, np-complete]
sources:
  - paper: "M. E. Stickel, A unification algorithm for associative-commutative functions, Journal of the ACM 28(3), 1981, pages 423 to 434"
    locator: the reduction of AC unification to homogeneous linear Diophantine equations, and the first complete algorithm
  - paper: "F. Fages, Associative-commutative unification, Journal of Symbolic Computation 3(3), 1987, pages 257 to 275"
    locator: the termination of the complete algorithm in the general case, which shows that AC is finitary
  - paper: "D. Kapur and P. Narendran, Complexity of unification problems with associative-commutative operators, Journal of Automated Reasoning 9, 1992"
    locator: the proof that deciding AC unifiability is in NP, and so NP-complete
  - paper: "D. Kapur and P. Narendran, Double-exponential complexity of computing a complete set of AC-unifiers, Proceedings of the Seventh IEEE Symposium on Logic in Computer Science, 1992, pages 11 to 21"
    locator: the doubly exponential bounds on the size of minimal complete sets of AC unifiers
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 3 (unification in commutative theories, the AC case, its unification type and its complexity)
---

The **AC unification problem** is [equational unification](/equational-unification/) modulo the theory AC of one or more binary symbols that are associative and commutative, such as $+$ with $(x + y) + z = x + (y + z)$ and $x + y = y + x$. Modulo AC, a sum is a multiset of its arguments, so the problem is about counting. Elementary AC equations reduce to homogeneous [linear Diophantine equations](/linear-diophantine-equation/) over the natural numbers. AC is **finitary**: every solvable problem has a finite minimal complete set of unifiers, but not one most general unifier. The problem is decidable, [Stickel's algorithm](/stickel-ac-unification/) solves it, and Fages proved that the general algorithm terminates. Deciding solvability is NP-complete, and minimal complete sets can be doubly exponential in the size of the problem.

## In plain words

Some operations do not care about order or grouping. Adding numbers and joining bags are examples: $a + b$ is $b + a$, and it does not matter which pair is added first. A sum is then just a bag of parts.

AC unification asks how to fill the blanks of two such sums so that the two bags become equal. Since only the bags matter, the question is about counting: each kind of part must appear as often on the left as on the right. Often there are several different best ways to fill the blanks, but never infinitely many. The number of best ways can grow very fast with the size of the problem.

## Definition

Notation: AC is the set of equations $(x + y) + z = x + (y + z)$ and $x + y = y + x$ for each AC symbol $+$. $=_{AC}$ is equality modulo these equations, $\sigma, \theta, \lambda$ are substitutions, and $X = \mathrm{Var}(s, t)$. A term whose top symbol is not $+$ is an **atom** of a sum.

**Input:** terms $s$ and $t$ (or a finite set of equations) over AC symbols, free function symbols, free constants and variables.

**Output:** whether there is an **AC-unifier** $\sigma$, with $s\sigma =_{AC} t\sigma$. In the solving version, the output is a complete set of AC-unifiers: a set $U$ such that each AC-unifier $\theta$ has some $\sigma \in U$ and some $\lambda$ with $x\theta =_{AC} x\sigma\lambda$ for each $x \in X$.

**Flattening.** By associativity, nested sums can be flattened, and by commutativity, the order of the arguments does not matter. So $s =_{AC} t$ exactly when the flattened forms have the same top symbol and the same multiset of arguments, compared recursively modulo AC. In pure AC there is no unit element, so a variable is never mapped to an empty sum.

**Facts.**

- AC is finitary. Every solvable AC problem has a finite minimal complete set of unifiers (Stickel 1975 and 1981, Fages 1987).
- AC unifiability is decidable, and it is NP-complete (Kapur and Narendran 1992). It is NP-hard already for AC matching, where one side has no variables (Benanav, Kapur and Narendran 1987).
- Minimal complete sets of AC unifiers can be doubly exponential in the size of the problem, and there is a doubly exponential upper bound (Kapur and Narendran 1992).

## Variants

- **Elementary AC unification.** Only one AC symbol and variables. After the common variables are cancelled, two nonempty sums are always unifiable: give the left variables the value $(\sum_j b_j) \cdot z$ and the right variables $(\sum_i a_i) \cdot z$, where $a_i$ and $b_j$ are the multiplicities. So the decision is trivial, and the work is in computing the complete set.
- **With constants.** Free constants are allowed. Each constant must be produced by exactly one basis piece, which adds a combinatorial condition. For example, $x + x \doteq a + b$ has no unifier.
- **General AC unification.** Several AC symbols and free function symbols. The arguments of sums are then arbitrary terms, and algorithms combine elementary AC unification with syntactic unification.
- **AC matching.** Only one side is instantiated. See [AC matching](/ac-matching/).
- **ACU, ACI, ACUI.** Adding a unit element (abelian monoids), idempotence, or both changes the arithmetic. Elementary ACU unification is unitary, because variables may be empty and all basis pieces can be used at once.
- **Commutativity alone.** Without associativity, the problem is C-unification, which is finitary and NP-complete, with a different algorithm.

## Examples

| problem | complete set | note |
|---|---|---|
| $x + y \doteq a + b$ | $\{x \mapsto a, y \mapsto b\}$, $\{x \mapsto b, y \mapsto a\}$ | two incomparable unifiers; $x \mapsto a + b$ is impossible, since $y$ cannot be empty |
| $x + x \doteq a + b$ | none | each constant appears once, but $x$ appears twice |
| $x + a \doteq y + b$ | $\{x \mapsto b, y \mapsto a\}$, $\{x \mapsto b + z, y \mapsto a + z\}$ | the second covers the bigger instances |
| $x + x \doteq y + z$ | 5 unifiers | the basis of $2x' = y' + z'$ has 3 vectors |
| $x + x + x \doteq y + y$ | $\{x \mapsto z + z, y \mapsto z + z + z\}$ | one mgu; the only minimal solution of $3x' = 2y'$ is $(2, 3)$ |
| $x_1 + x_2 \doteq y_1 + y_2$ | 7 unifiers | the edge covers of $K_{2,2}$ |

**Why counting works.** Take $x + x \doteq y + z$ and a unifier $\theta$. Pick any atom $u$ and count how often it occurs in $x\theta$, $y\theta$ and $z\theta$: say $n_x$, $n_y$ and $n_z$. Both sides of the equation contain $u$ the same number of times, so $2n_x = n_y + n_z$. So every atom follows a solution of this linear Diophantine equation, and every solution is a sum of the minimal solutions $(1, 0, 2)$, $(1, 1, 1)$ and $(1, 2, 0)$.

## Known algorithms

- **[Stickel's algorithm](/stickel-ac-unification/)** (1975, 1981). Flatten, cancel common arguments, compute the minimal solutions of the Diophantine equation, give each a new variable, and build one unifier for each admissible subset. In the general case, non-variable arguments are first replaced by new variables, and the resulting equations are solved recursively. Fages (1987) proved termination.
- **Diophantine basis algorithms.** The minimal solutions can be found by Huet's bounded search (1978), and for systems of equations by the algorithm of Contejean and Devie.
- **Solving all equations together.** Later algorithms solve a whole system of AC equations at once, as one system of linear Diophantine equations, which avoids much repeated work.
- **Decision only.** Kapur and Narendran show membership in NP: a solvable problem has a solution with a certificate of polynomial size, which can be guessed and checked in polynomial time. This avoids building the complete set.

## Bounds

- **Decision.** NP-complete for general AC unification, and NP-hard already for AC matching.
- **Output size.** Minimal complete sets can be doubly exponential (Kapur and Narendran 1992). For the simple family $x_1 + \cdots + x_n \doteq y_1 + \cdots + y_n$, Stickel's set has 1, 7, 265 and 41503 elements for $n = 1, 2, 3, 4$, one for each edge cover of $K_{n,n}$, so it grows like $2^{n^2}$.
- **Exact counts.** Domenjoud (1992) gave the exact number of minimal unifiers for equations of the form $\alpha x_1 + \cdots + \alpha x_p \doteq \beta y_1 + \cdots + \beta y_q$.

## Reductions

- **Elementary AC to linear Diophantine equations.** An equation $\sum_i a_i x_i \doteq \sum_j b_j y_j$, with multiplicities $a_i$ and $b_j$, becomes $\sum_i a_i x_i' = \sum_j b_j y_j'$ over $\mathbb{N}$. Its minimal solutions form a finite Hilbert basis, and the unifiers are built from subsets of the basis. Systems of AC equations become [systems of linear Diophantine equations](/linear-diophantine-system/).
- **General AC to elementary AC and syntactic unification.** Replacing alien subterms by variables splits a general problem into an elementary AC part and a free part, which are solved and recombined.
- **AC matching to AC unification.** Matching is the special case with a ground side, so the NP-hardness of matching carries over.

## Applications

- **Rewriting and completion modulo AC.** Critical pairs in [completion](/knuth-bendix-completion/) modulo AC and [rewriting modulo equations](/rewriting-modulo-equations/) are computed with AC unification. This is how equations such as $x + y = y + x$, which cannot be oriented, are handled.
- **Theorem provers.** Equational provers build AC into unification for operators such as $+$, $\cdot$, union and intersection.
- **Rewriting languages.** Languages based on rewriting logic offer matching and unification modulo AC for multisets and sets.
- **Protocol analysis.** Theories of exclusive or and of abelian groups extend AC, and their unification algorithms build on the same counting.

## References
