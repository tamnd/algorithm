---
tag: B1T4HN
kind: problem
slug: higher-order-unification-problem
name: Higher-order unification problem
aliases:
- HOU
- higher-order unification
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Given two simply typed λ-terms whose free variables may stand for functions, find a substitution that makes them equal up to βη. The problem is undecidable from second order on.
prereqs: [unification-problem, lambda-calculus, beta-reduction, unifier]
see_also: [higher-order-unification-undecidability, huet-pre-unification, pattern-unification-problem, miller-pattern-unification, second-order-unification-problem, nominal-unification-problem, equational-unification]
sources:
  - paper: doi:10.1016/0304-3975(75)90011-0
    title: Gérard P. Huet, A unification algorithm for typed λ-calculus, Theoretical Computer Science 1(1), 27 to 57 (1975)
    locator: the definitions of flex and rigid terms, pre-unifiers, and the examples of problems without most general unifiers
  - paper: doi:10.1016/S0019-9958(73)90301-X
    title: Gérard P. Huet, The undecidability of unification in third order logic, Information and Control 22(3), 257 to 267 (1973)
    locator: the undecidability theorem
  - paper: doi:10.1016/0304-3975(81)90040-2
    title: Warren D. Goldfarb, The undecidability of the second-order unification problem, Theoretical Computer Science 13(2), 225 to 230 (1981)
    locator: the undecidability theorem for second order
  - paper: doi:10.2168/LMCS-5(3:2)2009
    title: Colin Stirling, Decidability of higher-order matching, Logical Methods in Computer Science 5(3:2) (2009)
    locator: the main theorem (matching is decidable at all orders)
  - paper: "Gilles Dowek, Higher-order unification and matching, in Handbook of Automated Reasoning, volume II, Elsevier and MIT Press (2001)"
    locator: the survey of the problem, its fragments and its decidability results
---

The higher-order unification problem asks for a substitution that makes two simply typed λ-terms equal up to $\beta\eta$, where the free variables may stand for functions. It extends first-order [unification](/unification-problem/) in two ways at once: a variable can be applied to arguments, and terms can bind variables. Both make the problem much harder. It is undecidable from third order on ([Huet 1973, Lucchesi 1972](/higher-order-unification-undecidability/)) and even at second order ([Goldfarb 1981](/second-order-unification-undecidability/)), and a solvable instance need not have a most general unifier. The standard procedure is [Huet's pre-unification](/huet-pre-unification/), a semi-decision procedure. The [pattern](/pattern-unification-problem/) fragment and the matching problem are decidable.

## In plain words

In ordinary unification, the unknowns stand for pieces of a tree, and we fill them in so that two trees become the same. In higher-order unification, the unknowns can stand for functions. Then an unknown applied to an argument can copy the argument, drop it, or use it many times. Because of this, one equation can have many different solutions with nothing in common, or an infinite list of them. In the worst case no program can even tell whether a solution exists. Still, many equations that come up in practice are easy, and a search finds their solutions.

## Definition

Types are built from base types, such as $\iota$, and arrows $\sigma \to \tau$. Terms are simply typed λ-terms over typed constants and typed free variables (the unknowns), taken in $\beta$-normal $\eta$-long form. Such a term has the form $\lambda x_1 \ldots x_k.\, h(t_1, \ldots, t_m)$. It is *rigid* when the head $h$ is a constant or one of the bound variables, and *flex* when $h$ is a free variable.

**Input.** A finite set of pairs $s_i \doteq t_i$, where $s_i$ and $t_i$ are closed except for free variables and have the same type.

**Output.** A substitution $\sigma$, mapping free variables to terms of the same type, with $\sigma(s_i) =_{\beta\eta} \sigma(t_i)$ for each $i$, or the answer that no such $\sigma$ exists. The decision version only asks whether $\sigma$ exists.

The *order* of a type is $\operatorname{ord}(\iota) = 1$ and $\operatorname{ord}(\sigma \to \tau) = \max(\operatorname{ord}(\sigma) + 1, \operatorname{ord}(\tau))$. The problem has order $k$ if all its free variables have types of order at most $k$. First-order unification is order 1 without binders.

Because the problem has no most general unifiers in general, a solution method aims at a *complete set of unifiers*: a set $U$ of unifiers such that each unifier is an instance of some member of $U$, on the variables of the input. Huet also uses *pre-unifiers*, substitutions that leave only flex-flex pairs. Each flex-flex pair has a solution, so a pre-unifier shows that the problem is solvable.

## Variants

- **By order.** [Second-order unification](/second-order-unification-problem/) allows only free variables of type $\iota^k \to \iota$, which take first-order arguments. Third order and higher allow free variables that take functions.
- **Matching.** One side of each pair has no free variables. The problem is decidable at all orders (Stirling 2009).
- **Patterns.** Each free variable is applied only to distinct bound variables. The [pattern unification problem](/pattern-unification-problem/) is decidable and unitary.
- **Monadic, linear and context unification.** These restrict the constants or the solutions of second-order unification. Some of these restrictions are decidable; the page on [second-order unification](/second-order-unification-problem/) lists them.
- **Richer type systems.** The same question arises for dependent and polymorphic λ-calculi. It is undecidable there too, as these contain the simply typed case.

## Examples

**No most general unifier.** With constants $a : \iota$ and $g : \iota \to \iota \to \iota$ and $F : \iota \to \iota$, the pair $F(a) \doteq g(a, a)$ has exactly four unifiers: $F$ maps to $\lambda y.\, g(y, y)$, $\lambda y.\, g(y, a)$, $\lambda y.\, g(a, y)$ or $\lambda y.\, g(a, a)$. None of them is an instance of another.

**Infinitely many unifiers.** For $G : (\iota \to \iota) \to \iota$, the pair $G(\lambda u.\, u) \doteq a$ has the unifiers $G \mapsto \lambda y.\, y^k(a)$ for each $k \ge 0$, and no unifier is more general than all of them.

**Flex-flex.** The pair $F(a) \doteq F(b)$ has the most general unifier $F \mapsto \lambda y.\, H$. In general a flex-flex pair, such as $F(G(a)) \doteq G(F(a))$, has infinitely many independent solutions, but it always has some solution.

**Patterns.** The pair $\lambda x y.\, F(x, y) \doteq \lambda x y.\, F(y, x)$ is a pattern problem. Its most general unifier is $F \mapsto \lambda u v.\, H$.

## Known algorithms

| method | year | inputs | result |
|---|---|---|---|
| [Huet's pre-unification](/huet-pre-unification/) | 1975 | all problems | a complete set of pre-unifiers; may not stop |
| Jensen and Pietrzykowski | 1976 | all problems | a complete set of unifiers, including flex-flex solutions; may not stop |
| [Miller pattern unification](/miller-pattern-unification/) | 1991 | patterns | a most general unifier or failure; always stops |
| Huet and Lang | 1978 | second-order matching | a finite complete set of matchers |
| Stirling | 2009 | matching at all orders | a decision procedure |

Snyder and Gallier (1989) wrote Huet's procedure as a set of transformation rules, which is the form most later work uses.

## Bounds

- **Undecidable.** At order 3, even with one equation and one free variable, by reduction from Post's correspondence problem ([Huet 1973, Lucchesi 1972](/higher-order-unification-undecidability/)). At order 2, by reduction from Hilbert's tenth problem ([Goldfarb 1981](/second-order-unification-undecidability/)).
- **Semi-decidable.** The set of solvable problems is recursively enumerable: list all substitutions and check each by normalization. So the problem is complete for the recursively enumerable sets.
- **Decidable cases.** First-order unification (linear time), patterns (linear time, Qian 1993), matching at all orders (Stirling 2009), and monadic second-order unification (Zhezherun 1979, Farmer 1988).

## Reductions

- [Post's correspondence problem](/post-correspondence-problem/) reduces to third-order unification.
- [Hilbert's tenth problem](/hilberts-tenth-problem/) reduces to second-order unification.
- First-order unification and [pattern unification](/pattern-unification-problem/) are special cases.
- [Nominal unification](/nominal-unification-problem/) reduces to pattern unification in quadratic time (Levy and Villaret 2008).
- Many questions of [unification modulo an equational theory](/equational-unification/) can be posed as higher-order unification problems, and some undecidability proofs for [those problems](/undecidability-of-unification-modulo-theories/) use the same ideas.

## Applications

- **Higher-order theorem proving.** Provers for higher-order logic need to unify terms with function variables. Huet built pre-unification for constrained resolution, and later provers still use variants of his procedure.
- **Higher-order logic programming.** λProlog runs programs over terms with binders and uses higher-order unification to match goals with clauses.
- **Proof assistants.** Isabelle uses higher-order unification to apply rules, and the elaborators of dependently typed systems use it to fill in implicit arguments.
- **Program transformation.** Huet and Lang (1978) used second-order matching to apply program transformation schemes.
- **Linguistics.** Higher-order unification has been used to compute the meaning of ellipsis in natural language sentences.

## References
