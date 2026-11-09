---
tag: EREY3Q
kind: problem
slug: second-order-unification-problem
name: Second-order unification problem
aliases:
- SOU
- second-order unification
area: logic-and-constraints/unification-and-resolution
level: research
summary: Unify first-order terms that contain variables for functions of first-order arguments. The problem is undecidable in general, but some restricted forms are decidable.
prereqs: [higher-order-unification-problem, unification-problem, unifier]
see_also: [second-order-unification-undecidability, higher-order-unification-problem, huet-pre-unification, pattern-unification-problem, term-matching, semi-unification-problem]
sources:
  - paper: doi:10.1016/0304-3975(81)90040-2
    title: Warren D. Goldfarb, The undecidability of the second-order unification problem, Theoretical Computer Science 13(2), 225 to 230 (1981)
    locator: the definition of the problem and the undecidability theorem
  - paper: "Jordi Levy and Margus Veanes, On the undecidability of second-order unification, Information and Computation 159(1-2), 125 to 150 (2000)"
    locator: the introduction (word, linear second-order and context unification) and the chronological list of results in the concluding section
  - paper: "Gilles Dowek, Higher-order unification and matching, in Handbook of Automated Reasoning, volume II, Elsevier and MIT Press (2001)"
    locator: the sections on second-order unification and matching
---

The second-order unification problem is the part of [higher-order unification](/higher-order-unification-problem/) in which the free variables stand for functions of first-order arguments, such as $X : \iota \to \iota \to \iota$, and the constants are first-order. A solution maps each such variable to a first-order term with holes, like $\lambda x y.\, g(y, g(x, a))$. It is the most used case in practice and the simplest case past first-order [unification](/unification-problem/). Goldfarb showed in 1981 that it is [undecidable](/second-order-unification-undecidability/), so the search of [Huet's pre-unification](/huet-pre-unification/) cannot be replaced by a decision procedure. Restricted forms, such as monadic second-order unification and second-order matching, are decidable.

## In plain words

In first-order unification an unknown stands for a whole piece of a tree. In second-order unification an unknown can also stand for a tree with holes in it, and the holes are filled with the arguments that the unknown gets. An unknown can copy an argument to many places, or throw it away. This freedom is enough to encode arithmetic with equations between trees, so no program can solve all such problems. If every symbol in the trees has at most one child, the trees are just words, and the problem becomes the solving of word equations, which is decidable.

## Definition

The signature has first-order constants $f : \iota^k \to \iota$. Free variables have types $\iota^k \to \iota$ for some $k \ge 0$; those with $k = 0$ are first-order variables. Terms of type $\iota$ are built from constants, free variables applied to the right number of terms, and (inside values) bound variables.

**Input.** A finite set of pairs $s_i \doteq t_i$ of terms of type $\iota$. Equations of type $\iota^k \to \iota$ can be written with binders, as in $\lambda u.\, X(g(a, u)) \doteq \lambda u.\, g(a, X(u))$.

**Output.** A substitution that maps each variable $X : \iota^k \to \iota$ to a term $\lambda x_1 \ldots x_k.\, t$, where $t$ is a first-order term over the constants, the $x_i$ and free variables, such that each pair becomes two identical terms after $\beta$-reduction. If none exists, the answer is *no*. The decision version only asks whether a solution exists.

## Variants

- **Monadic.** All constants have at most one argument. Terms are then words, and the problem is closely related to word equations.
- **Second-order matching.** One side of each pair has no free variables.
- **Linear second-order unification.** Each bound variable of a value occurs exactly once in it, so a value is a term with holes that are each filled once.
- **Context unification.** Linear, and all second-order variables have one argument. A variable then stands for a *context*, a term with one hole.
- **Bounded variables.** The number of second-order variables, their arity, or the number of their occurrences is bounded.
- **Simple equations.** The arguments of second-order variables are ground terms.

## Examples

**Several independent solutions.** With $X : \iota \to \iota$, the pair $X(a) \doteq g(a, a)$ has four solutions: $\lambda y.\, g(y, y)$, $\lambda y.\, g(y, a)$, $\lambda y.\, g(a, y)$ and $\lambda y.\, g(a, a)$.

**Numerals.** The pair $\lambda u.\, X(g(a, u)) \doteq \lambda u.\, g(a, X(u))$ has exactly the solutions $X \mapsto \lambda z.\, g(a, g(a, \ldots g(a, z)))$ with any number of copies of $g(a, \cdot)$. Goldfarb's proof uses these terms as numbers.

**Word equations.** In the monadic case, with unary constants $a$ and $b$ and a constant $c$, the word equation $H \cdot a b \cdot G = G \cdot b a \cdot H$ becomes the pair $H(a(b(G(c)))) \doteq G(b(a(H(c))))$ with $G, H : \iota \to \iota$.

**No solution.** The pair $X(a) \doteq g(X(a), a)$ has no solution: the right side would be larger than the left side.

## Known algorithms

| method | inputs | result |
|---|---|---|
| [Huet's pre-unification](/huet-pre-unification/), Pietrzykowski's procedure (1973) | all problems | a complete set of (pre-)unifiers; may not stop |
| Huet and Lang (1978) | second-order matching | a finite complete set of matchers; always stops |
| Farmer (1988), via Makanin's algorithm for word equations | monadic problems | a decision procedure |
| Jeż (2014), recompression | context unification | a decision procedure in polynomial space |
| [Miller pattern unification](/miller-pattern-unification/) | problems where each variable gets distinct bound variables | a most general unifier |

## Bounds

- **Undecidable** in general ([Goldfarb 1981](/second-order-unification-undecidability/)), already over one constant and one binary function symbol.
- **Undecidable** with a single second-order variable that is unary (Levy and Veanes 2000), and when all second-order variables are unary (Farmer 1991).
- **Decidable** in the monadic case (Zhezherun 1979; Farmer 1988).
- **Decidable** for second-order matching (Huet and Lang 1978).
- **Decidable** when the number of occurrences of each bound variable in a solution is bounded (Schmidt-Schauß).
- **Decidable** for context unification, in polynomial space (Jeż 2014).
- **Semi-decidable** in general, since solutions can be listed and checked.

## Reductions

- [Hilbert's tenth problem](/hilberts-tenth-problem/) reduces to second-order unification (Goldfarb). This is the proof of undecidability.
- Word equations and monadic second-order unification reduce to each other (Farmer 1988).
- Second-order unification reduces in polynomial time to simultaneous rigid E-unification (Degtyarev and Voronkov 1996), and Levy and Veanes (2000) gave a reduction in the other direction.
- Second-order unification is a special case of [higher-order unification](/higher-order-unification-problem/), and first-order unification is a special case of it.

## Applications

- **Program transformation.** Huet and Lang (1978) used second-order matching to apply transformation schemes to programs.
- **Automated reasoning.** Proof by induction and the generalization of proofs need terms with holes, and second-order unification finds them.
- **Linguistics.** Second-order unification and context unification are used to compute the meaning of ellipsis and of scope in natural language.
- **Term rewriting.** Context unification describes the overlap of rewrite rules with variables for contexts.

## References
