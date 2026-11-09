---
tag: 6TZ7KA
kind: algorithm
slug: miller-pattern-unification
name: Miller pattern unification
aliases:
- pattern unification algorithm
- higher-order pattern unification
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Compute a most general unifier of two higher-order patterns, or report that there is none. Each step is forced, so there is no search, and Qian's version runs in linear time.
solves: [pattern-unification-problem]
model: word-ram
properties: {deterministic: true}
history:
  year: 1991
  people: [Dale Miller]
  note: Miller defined the pattern fragment of the simply typed λ-calculus and showed that unification in it is decidable and has most general unifiers.
prereqs: [pattern-unification-problem, higher-order-unification-problem, lambda-calculus, most-general-unifier]
see_also: [huet-pre-unification, robinson-unification, martelli-montanari-unification, occurs-check, urban-nominal-unification, paterson-wegman-unification]
sources:
  - paper: doi:10.1093/logcom/1.4.497
    title: Dale Miller, A logic programming language with lambda-abstraction, function variables, and simple unification, Journal of Logic and Computation 1(4), 497 to 536 (1991)
    locator: the definition of the pattern fragment and the unification algorithm with its mgu theorem
  - paper: "Tobias Nipkow, Functional unification of higher-order patterns, Proceedings of the 8th IEEE Symposium on Logic in Computer Science (LICS 1993), 64 to 74"
    locator: the rule-based algorithm (flex-flex, flex-rigid with pruning, rigid-rigid) and its functional code
  - paper: "Zhenyu Qian, Linear unification of higher-order patterns, TAPSOFT 1993, Lecture Notes in Computer Science 668, Springer, 391 to 405"
    locator: the linear-time algorithm
---

Miller pattern unification solves the [pattern unification problem](/pattern-unification-problem/): given two simply typed λ-terms in which each free variable is applied only to distinct bound variables, it finds a [most general unifier](/most-general-unifier/) or reports that there is none. Full [higher-order unification](/higher-order-unification-problem/) is undecidable and has no most general unifiers in general. In the pattern fragment both problems go away: each step of the algorithm is forced, there is no search, and the answer is unique up to renaming. The algorithm extends first-order unification in the style of [Martelli and Montanari](/martelli-montanari-unification/) with two new ideas: a flex-flex rule that keeps the common arguments, and *pruning*, which removes arguments that a solution cannot use. Qian showed that a version on shared terms runs in linear time.

## In plain words

An unknown function is applied to some local names, all different. To make it equal to a known expression, the function must rebuild that expression from those names. There is only one way to do this, because each name tells you exactly which input to use. If the known expression mentions a local name that the function does not get, it cannot be built, unless that name sits inside another unknown, which we then forbid to use it. If both sides are unknowns, they can only share the names that both of them get. So each step has one answer, and the algorithm never has to guess or go back. The result is the most general answer: every other answer is a special case of it.

## The problem

Terms are simply typed, in $\beta$-normal $\eta$-long form, and have the form $\lambda x_1 \ldots x_k.\, h(t_1, \ldots, t_m)$. The head $h$ is a constant, a bound variable, or a free variable. A term is a *pattern* when each occurrence of a free variable $F$ has the form $F(y_1, \ldots, y_n)$, where the $y_i$ are distinct bound variables (each in its η-long form). The input is a set of pairs $s \doteq t$ of closed patterns of the same type. The output is a most general unifier, or *fail*.

## The algorithm

The algorithm takes one pair at a time and applies the current substitution $\theta$ to it. The two sides of a pair are put under the same binders $\bar x$ first. PRUNE takes a term and a set $V$ of bound variables, and makes each free variable in the term drop the arguments that are not in $V$.

```pseudo id=main
PATTERN-UNIFY(E)                       ▷ E: pairs of patterns of the same type
L1  θ ← the identity substitution
L2  while E is not empty do
L3      take λx̄. s ≐ λx̄. t from E, and let s ← θ(s), t ← θ(t)
L4      if s = F(ȳ) and t = F(z̄) then                        ▷ flex-flex, same head
L5          if ȳ ≠ z̄ then θ ← {F ↦ λw̄. H(w_i : y_i = z_i)} ∘ θ    ▷ H is new
L6      else if s = F(ȳ) and t = G(z̄) then                    ▷ flex-flex, F ≠ G
L7          θ ← {F ↦ λȳ. H(v̄), G ↦ λz̄. H(v̄)} ∘ θ   ▷ v̄: the variables in both ȳ and z̄
L8      else if one side is F(ȳ) and the other side t is rigid then    ▷ flex-rigid
L9          if F occurs in t then return fail
L10         t ← PRUNE(t, ȳ)
L11         θ ← {F ↦ λȳ. t} ∘ θ
L12     else if the heads of s and t differ then return fail    ▷ rigid-rigid
L13     else add λx̄. s_i ≐ λx̄. t_i to E, for each argument i
L14 return θ

PRUNE(λz̄. h(t̄), V)                    ▷ bound variables in V or z̄ may stay
L15 if h is a free variable G, with arguments w̄, then
L16     ū ← the w_i that are in V or in z̄
L17     if ū ≠ w̄ then θ ← {G ↦ λw̄. H(ū)} ∘ θ, and return λz̄. H(ū)    ▷ H is new
L18     return λz̄. G(w̄)
L19 if h is a bound variable that is not in V or z̄ then return fail
L20 return λz̄. h(PRUNE(t_1, V ∪ z̄), ..., PRUNE(t_m, V ∪ z̄))
```

In line L11 the term $\lambda \bar y.\, t$ abstracts the names $\bar y$ in their order. Because $F(\bar y)$ applied to these names gives back $t$ by $\beta$-reduction, the binding solves the pair. In line L5, $\lambda \bar w.\, H(w_i : y_i = z_i)$ keeps the argument places where the two sides agree. The notation $\{\ldots\} \circ \theta$ means: apply $\theta$ first, then the new binding. When PRUNE meets a variable that $\theta$ already binds, it applies $\theta$ first.

All bindings map a pattern to a pattern. A free variable stays applied to distinct bound variables, because a binding only renames bound variables or drops some of them. So the algorithm never leaves the fragment.

## Example

Take $F : \iota \to \iota$, $G : \iota \to \iota \to \iota$, a constant $g : \iota \to \iota \to \iota$, and the two pairs

$$\lambda x y.\, F(x) \doteq \lambda x y.\, g(x, G(y, x)), \qquad \lambda x y.\, G(x, y) \doteq \lambda x y.\, G(y, x).$$

| step | pair | rule | new binding |
|---|---|---|---|
| 1 | $F(x) \doteq g(x, G(y, x))$ | flex-rigid, PRUNE with $V = \{x\}$ | $G \mapsto \lambda w_1 w_2.\, H(w_2)$ |
| 1 | the same pair, now $F(x) \doteq g(x, H(x))$ | flex-rigid | $F \mapsto \lambda u.\, g(u, H(u))$ |
| 2 | $H(y) \doteq H(x)$, after $\theta$ | flex-flex, same head | $H \mapsto \lambda w.\, K$ |

In step 1 the argument $y$ of $G$ is not available to $F$, so PRUNE makes $G$ drop its first argument. In step 2 the second pair has become $H(y) \doteq H(x)$; the two argument lists differ in the only place, so $H$ keeps no argument. The result is

$$\theta = \{F \mapsto \lambda u.\, g(u, K),\ G \mapsto \lambda w_1 w_2.\, K,\ H \mapsto \lambda w.\, K\}.$$

Each unifier of the two pairs is an instance of $\theta$: it fixes a value for $K$.

The problem $F(a) \doteq a$ is not a pattern, because $a$ is a constant. It has the two unifiers $\lambda u.\, u$ and $\lambda u.\, a$, and neither is an instance of the other. So the restriction to patterns is what makes most general unifiers possible.

## Correctness

The full proof is in the [correctness proof](proofs/correctness.md). It shows three things.

- **Each step is most general.** If a step makes the binding $\rho$, then $\rho$ solves the pair, and each unifier $\delta$ of the pair has the form $\delta' \circ \rho$. The key fact is that applying a term to *distinct* bound variables only renames them. So if $\delta(F)(\bar y) = \delta(F)(\bar z)$, the value of $F$ cannot use an argument place where $\bar y$ and $\bar z$ differ. The same fact proves the pruning step and the flex-rigid binding: $\delta(F)$ must be $\lambda \bar y.\, \delta(t)$.
- **Failure is correct.** A clash of rigid heads, a bound variable that the flex side cannot reach (line L19), and an occurs check failure (line L9) each mean that the pair has no unifier. For the occurs check, the occurrence of $F$ in $t$ is under rigid heads only, because in a pattern a free variable has only bound variables as arguments. So the instance of $t$ would be strictly larger than the instance of $F(\bar y)$.
- **Termination.** Each step lowers the pair (number of unsolved variables in $E$, size of $E$) in the lexicographic order.

Together these give the main theorem: the pattern unification problem is decidable and *unitary*. If two patterns have a unifier, they have a most general one, and the algorithm returns it.

## Complexity

With terms stored as trees and with eager substitution, as in the pseudocode, the run time can be exponential. This already happens for first-order terms, which are patterns with no λ-binders, as for [Robinson's algorithm](/robinson-unification/). The cause is the size of the unifier as a tree. Qian (1993) gave a version that works on shared terms and runs in linear time in the size of the input, in the same way as [Paterson and Wegman](/paterson-wegman-unification/) for first-order terms. The Python implementation uses trees for clarity.

## Properties

- **Decidable and unitary.** One answer, the most general unifier, or fail.
- **No search.** Each rule is deterministic. The order in which pairs are taken does not change the result, up to the renaming of new variables.
- **Closed fragment.** Bindings map patterns to patterns.
- **First-order case.** With no binders and only variables of base type, lines L4 to L11 reduce to the variable elimination rules of Martelli and Montanari, and PRUNE does nothing.
- **η matters.** The definition of a pattern is up to η: an argument $\lambda z.\, y(z)$ is the bound variable $y$.

## Variants and improvements

- **Linear time.** Qian (1993) on shared terms.
- **Functional code.** Nipkow (1993) gave the rules as a short functional program, which this page follows.
- **Dependent types.** Pfenning extended the pattern fragment to dependent and polymorphic type theories, and logical frameworks such as Twelf use it.
- **Dynamic patterns.** Many systems test each pair at run time. They solve the pairs that are patterns at that moment and delay the others, in the hope that later bindings turn them into patterns. When this fails, they fall back to [Huet's pre-unification](/huet-pre-unification/) or report an unsolved constraint.
- **Nominal unification.** [Nominal unification](/urban-nominal-unification/) solves a related problem with names in place of bound variables. Levy and Villaret gave a reduction from it to pattern unification.

## When to use it

Use it when unknowns stand for terms with holes for bound variables, as in programs and proofs that use higher-order abstract syntax, rule schemes in logical frameworks, and type checkers with implicit arguments. It is the standard unifier of λProlog implementations, of Twelf, and of the higher-order rewriting in Isabelle. If the terms are first-order, use a first-order algorithm. If some unknown is applied to a constant or to the same variable twice, the problem is outside the fragment.

## Pitfalls

- **Missing the prune.** Without PRUNE, the algorithm would fail on $\lambda x y.\, F(x) \doteq \lambda x y.\, g(x, G(y))$, but $G \mapsto \lambda w.\, a$ and $F \mapsto \lambda u.\, g(u, a)$ solve it.
- **Wrong argument list in the flex-flex rule.** For $F(\bar y) \doteq G(\bar z)$, the new variable takes the variables that occur in both lists, not the positions where the lists agree. The positions rule applies only when $F = G$.
- **Argument order.** In line L7, $\bar v$ must be listed in one fixed order for both bindings, or the two sides are not equal.
- **Testing the pattern condition too late.** Check the pattern condition on the input. A non-pattern pair can make a rule produce a binding that is not most general.
- **Occurs check under a flex head.** In patterns a free variable never occurs in the argument of another free variable, so the occurs check is exact. Outside the fragment the same test is wrong, as the page on [Huet's pre-unification](/huet-pre-unification/) shows.

## Implementations

## History

Miller introduced the pattern fragment, which he called $L_\lambda$, in work on higher-order logic programming in 1989, and published it in the Journal of Logic and Computation in 1991. He proved that unification of patterns is decidable and that a unifiable pair has a most general unifier. Nipkow restated the algorithm as a small set of rules with a functional program in 1993. In the same year Qian gave a linear-time version on shared terms. Pfenning extended the fragment to richer type theories, and the fragment became the core of the unifiers of λProlog, Twelf and many proof assistants.

## References
