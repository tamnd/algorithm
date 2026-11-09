---
tag: NAM2FE
kind: problem
slug: pattern-unification-problem
name: Pattern unification problem
aliases:
- Miller pattern unification
- higher-order pattern unification
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Higher-order unification for terms in which each free variable is applied only to distinct bound variables. The problem is decidable, and each solvable instance has a most general unifier.
model: word-ram
complexity:
  vars: {N: the total size of the input terms}
  time: {decide: O(N), mgu on shared terms: O(N)}
  space: {extra: O(N)}
prereqs: [higher-order-unification-problem, unification-problem, most-general-unifier, lambda-calculus]
see_also: [miller-pattern-unification, huet-pre-unification, nominal-unification-problem, second-order-unification-problem, unification-problem]
sources:
  - paper: doi:10.1093/logcom/1.4.497
    title: Dale Miller, A logic programming language with lambda-abstraction, function variables, and simple unification, Journal of Logic and Computation 1(4), 497 to 536 (1991)
    locator: the definition of the fragment and the theorem that unifiable patterns have a most general unifier
  - paper: "Zhenyu Qian, Linear unification of higher-order patterns, TAPSOFT 1993, Lecture Notes in Computer Science 668, Springer, 391 to 405"
    locator: the linear-time bound
  - paper: "Tobias Nipkow, Functional unification of higher-order patterns, Proceedings of the 8th IEEE Symposium on Logic in Computer Science (LICS 1993), 64 to 74"
    locator: the definition of patterns up to η and the rule-based algorithm
---

The pattern unification problem is the part of the [higher-order unification problem](/higher-order-unification-problem/) where each free variable is applied only to distinct bound variables. Miller found this fragment in 1991. Full higher-order unification is undecidable and can have infinitely many independent solutions. Pattern unification has neither problem: it is decidable, and each solvable instance has a [most general unifier](/most-general-unifier/), as in the first-order [unification problem](/unification-problem/), which is the special case without binders. [Miller's algorithm](/miller-pattern-unification/) solves it, and Qian showed it can be solved in linear time.

## In plain words

Some equations have unknowns that are functions. In general such equations are very hard: no program can always tell if they have a solution. But in many practical cases each unknown function is only applied to local names, and never to the same name twice. In these cases the unknown can only copy, reorder or drop those names, so there is never a choice to make. Then the equations are as easy as ordinary equations between trees: a program can always decide them, and when there is a solution there is one best solution that covers all others.

## Definition

Terms are simply typed λ-terms in $\beta$-normal $\eta$-long form, built from constants, bound variables and free variables (the unknowns). A term is a *pattern* if each occurrence of a free variable $F$ has the form

$$F(y_1, \ldots, y_n),$$

where $y_1, \ldots, y_n$ are distinct variables that are bound at that place in the term. The definition is up to η: an argument $\lambda \bar z.\, y(\bar z)$ counts as the variable $y$.

**Input.** A finite set of pairs $s_i \doteq t_i$ of closed patterns, where the two terms of each pair have the same type.

**Output.** A substitution $\sigma$ with $\sigma(s_i) =_{\beta\eta} \sigma(t_i)$ for each $i$ that is most general: each other unifier $\delta$ has the form $\delta' \circ \sigma$ on the variables of the input. If there is no unifier, the answer is *no*. The decision version only asks whether a unifier exists.

The main theorem (Miller 1991) is that a unifiable set of pattern pairs always has a most general unifier. In the words of unification theory, the problem is *unitary*.

## Variants

- **Pattern matching.** One side of each pair has no free variables. The algorithm is the same, and it never needs the flex-flex rules.
- **Richer type theories.** Pfenning extended the fragment and the mgu theorem to dependent and polymorphic λ-calculi. Logical frameworks and the type checkers of dependently typed languages use these versions.
- **Dynamic patterns.** A system can test the pattern condition on each pair when it meets it, solve the pairs that are patterns and postpone the others. This is not a separate problem, but it is how the fragment is used in practice.
- **Nominal unification.** The [nominal unification problem](/nominal-unification-problem/) uses names and swaps in place of λ-binders. It is also decidable and unitary, and it reduces to pattern unification.

## Examples

**A most general unifier.** For $F : \iota \to \iota$ and $G : \iota \to \iota \to \iota$, the pair $\lambda x y.\, F(x) \doteq \lambda x y.\, g(x, G(y, x))$ has the mgu $F \mapsto \lambda u.\, g(u, H(u))$, $G \mapsto \lambda w_1 w_2.\, H(w_2)$. The value of $G$ cannot use its first argument, because $F$ does not see $y$.

**Swapped arguments.** The pair $\lambda x y.\, F(x, y) \doteq \lambda x y.\, F(y, x)$ has the mgu $F \mapsto \lambda u v.\, H$. A value of $F$ that used $u$ or $v$ would give different results on the two sides.

**No unifier, by scope.** The pair $\lambda x.\, F \doteq \lambda x.\, x$, with $F : \iota$, has no unifier. The value of $F$ is fixed before $x$ is bound, so it cannot be $x$. This is the higher-order form of a variable that escapes its scope.

**Not a pattern.** The pair $F(a) \doteq a$ is not a pattern, because $F$ is applied to a constant. It has the two unifiers $\lambda u.\, u$ and $\lambda u.\, a$, and neither is an instance of the other. The pair $\lambda x.\, F(x, x) \doteq \lambda x.\, g(x, x)$ is not a pattern either, because the argument $x$ repeats.

## Known algorithms

| algorithm | year | time | notes |
|---|---|---|---|
| [Miller](/miller-pattern-unification/) | 1991 | exponential on trees | the original algorithm and the mgu theorem |
| Nipkow | 1993 | exponential on trees | the same rules as a short functional program |
| Qian | 1993 | $O(N)$ | shared terms, in the style of [Paterson and Wegman](/paterson-wegman-unification/) |
| [Huet's pre-unification](/huet-pre-unification/) | 1975 | no bound | works on all terms, but it is a search and it does not decide the fragment by itself |

The exponential time of the tree algorithms comes from the size of the mgu as a tree. It already appears for first-order terms.

## Bounds

The problem can be decided in $O(N)$ time (Qian 1993), and a most general unifier can be built in the same time if it is stored as a graph with shared subterms. Each algorithm must read its input, so $\Omega(N)$ is a lower bound. Written as a tree, the mgu can have size exponential in $N$. The first-order example $X_1 \doteq g(X_2, X_2), \ldots, X_{n-1} \doteq g(X_n, X_n)$ already shows this.

## Reductions

- **First-order unification** is the special case where no term has a binder and each free variable has a base type. Every first-order term is a pattern.
- **Nominal unification** reduces to pattern unification in quadratic time (Levy and Villaret 2008). Cheney (2005) related the two problems in the other direction.
- **Full higher-order unification** contains the fragment. Leaving the fragment in either of two ways, by an argument that is not a bound variable or by a repeated argument, brings back problems with no mgu.

## Applications

- **Higher-order logic programming.** λProlog uses higher-order terms to represent programs and formulas with binders. Miller defined the fragment for the language $L_\lambda$, a part of λProlog in which unification needs no search.
- **Logical frameworks.** Twelf and other implementations of the LF type theory use dependent pattern unification to infer implicit arguments and to run logic programs.
- **Proof assistants.** Isabelle uses pattern unification for higher-order rewriting, and the elaborators of dependently typed languages solve the pattern cases of their unification constraints this way.
- **Program transformation.** Rewrite rules over terms with binders, such as rules over programs in higher-order abstract syntax, are often patterns, so a rule can be matched in linear time.

## References
