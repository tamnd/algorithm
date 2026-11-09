---
tag: SQ3VKJ
kind: problem
slug: semi-unification-problem
name: Semi-unification problem
aliases:
- semi-unification
- SUP
area: logic-and-constraints/unification-and-resolution
level: research
summary: Find one substitution that makes each left term, after a further instantiation of its own, equal to the right term; undecidable in general.
prereqs: [unification-problem, substitution, term-matching]
see_also: [semi-unification-undecidability, unification-problem, term-matching, occurs-check, undecidability, turing-machine, rewrite-rule, lambda-calculus]
sources:
  - paper: doi:10.1006/inco.1993.1003
    title: A. J. Kfoury, J. Tiuryn and P. Urzyczyn, The undecidability of the semi-unification problem, Information and Computation 102(1), 1993, pages 83 to 101
    locator: the definition of semi-unification as systems of inequalities, and the proof that it is undecidable
  - paper: "A. J. Kfoury, J. Tiuryn and P. Urzyczyn, Type reconstruction in the presence of polymorphic recursion, ACM Transactions on Programming Languages and Systems 15(2), 1993"
    locator: the equivalence between typability with polymorphic recursion and semi-unification
  - paper: "F. Henglein, Type inference with polymorphic recursion, ACM Transactions on Programming Languages and Systems 15(2), 1993"
    locator: the reduction of type inference in the Milner-Mycroft calculus to semi-unification and back
  - paper: "A. Dudenhefner, Undecidability of semi-unification on a napkin, 5th International Conference on Formal Structures for Computation and Deduction (FSCD 2020), LIPIcs volume 167, 2020"
    locator: a short reduction from Turing machine boundedness to semi-unification, mechanized in the Coq proof assistant
---

The **semi-unification problem** asks, for a finite set of pairs of first-order [terms](/term/) $s_i \le t_i$, whether one [substitution](/substitution/) $\sigma$ exists such that each $t_i\sigma$ is an instance of $s_i\sigma$. It combines the [unification problem](/unification-problem/), where $\sigma$ is applied to both sides, and [matching](/term-matching/), where an extra substitution is applied to one side. Each inequality may use its own extra substitution. Semi-unification is the core of type inference with polymorphic recursion, and it also appears in tests for loops in term rewriting. [Kfoury, Tiuryn and Urzyczyn proved](/semi-unification-undecidability/) in 1990 (journal version 1993) that it is undecidable, which settled a question open for several years.

## In plain words

In ordinary unification you fill the blanks of two patterns so that they become the same. In matching, one side is fixed, and you fill only the blanks of the other side.

Semi-unification mixes the two. You have several pairs, each with a left pattern and a right pattern. You must choose one filling for all blanks, used everywhere. After that filling, each left pattern must still match its right pattern, and each pair may use its own extra filling of the left side for that.

This looks like a small change, but it makes the problem much harder. The shared filling must work for all pairs at once, while each pair copies the left side in its own way. Because of this, no program can decide every case.

## Definition

Notation: $\sigma, \rho, \theta$ are substitutions, $t\sigma$ is the application of $\sigma$ to $t$, and $s \le t$ is an **inequality** between terms.

**Input:** a finite set $\Gamma = \{s_1 \le t_1, \ldots, s_n \le t_n\}$ of inequalities between first-order terms.

**Output:** whether $\Gamma$ has a **semi-unifier**: a substitution $\sigma$ such that for each $i$ there is a substitution $\rho_i$ with

$$s_i\sigma\rho_i = t_i\sigma.$$

In words, $t_i\sigma$ is an instance of $s_i\sigma$ for each $i$. The substitution $\sigma$ is shared by all inequalities, and the residual substitutions $\rho_i$ are separate.

**Facts.**

- **Undecidable** in general ([Kfoury, Tiuryn and Urzyczyn](/semi-unification-undecidability/)).
- **Semi-decidable.** An algorithm can enumerate all candidate tuples $\sigma, \rho_1, \ldots, \rho_n$ of finite substitutions and check each one, so it halts exactly on the semi-unifiable inputs.
- **Principal semi-unifiers.** If $\Gamma$ is semi-unifiable, it has a most general semi-unifier, unique up to renaming, in the same sense as a [most general unifier](/most-general-unifier/).

## Variants

- **Uniform semi-unification.** One residual substitution $\rho$ for all inequalities. It is the same as a single inequality, by tupling: $\{s_i \le t_i\}$ with one $\rho$ is $f(s_1, \ldots, s_n) \le f(t_1, \ldots, t_n)$.
- **One inequality.** Semi-unification with one inequality is decidable (Kapur, Musser, Narendran and Stillman 1991).
- **Restricted classes.** Some syntactic restrictions on how the variables occur in the inequalities give decidable classes.
- **Rational trees.** If $\sigma$ may map variables to infinite rational trees, as in unification without the [occurs check](/occurs-check/), the problem changes and is studied separately.
- **Equations and inequalities.** Systems that also contain equations $s \doteq t$ are no more general, because an equation can be written as an inequality (see Reductions).

## Examples

| system | semi-unifiable? | witness or reason |
|---|---|---|
| $x \le f(x)$ | yes | $\sigma = \mathrm{id}$, $\rho = \{x \mapsto f(x)\}$ |
| $f(x, y) \le f(y, g(x))$ | yes | $\sigma = \mathrm{id}$, $\rho = \{x \mapsto y, y \mapsto g(x)\}$ |
| $\{x \le f(y),\ y \le f(x)\}$ | yes | $\sigma = \mathrm{id}$, $\rho_1 = \{x \mapsto f(y)\}$, $\rho_2 = \{y \mapsto f(x)\}$ |
| $f(x, x) \le f(y, z)$ | yes | $\sigma = \{z \mapsto y\}$, $\rho = \{x \mapsto y\}$ |
| $f(x, x) \le f(y, g(y))$ | no | it would need $x\sigma\rho = y\sigma$ and $x\sigma\rho = g(y\sigma)$, so $y\sigma = g(y\sigma)$ |
| $f(x, x) \le f(a, b)$ | no | it would need $x\sigma\rho = a$ and $x\sigma\rho = b$ |

The first row shows the difference from unification: $x \doteq f(x)$ fails the occurs check, but $x \le f(x)$ holds with the identity, because the residual substitution may map $x$ to $f(x)$. The third row is a system whose equations $x \doteq f(y)$, $y \doteq f(x)$ have no unifier. The fourth row needs a nontrivial $\sigma$: with $\sigma = \mathrm{id}$, $\rho$ would have to map $x$ to both $y$ and $z$.

## Known algorithms

- **Semi-decision.** Enumerate all candidate tuples $(\sigma, \rho_1, \ldots, \rho_n)$ and check $s_i\sigma\rho_i = t_i\sigma$. This halts exactly on semi-unifiable inputs, and no procedure can also halt on all the others.
- **Closure on a term graph.** Procedures for the decidable classes work on a graph of term nodes and add the equations that the inequalities force, in the style of [unification by union-find](/martelli-montanari-unification/).
- **One inequality.** A decision procedure exists, by the work of Kapur, Musser, Narendran and Stillman.

## Bounds

- **Undecidable** for finite systems of inequalities, by a reduction from the boundedness problem for [Turing machines](/turing-machine/). See the [undecidability theorem](/semi-unification-undecidability/).
- **Recursively enumerable.** The set of semi-unifiable systems is recursively enumerable, so its complement is not.
- **At least as hard as unification.** Unification reduces to semi-unification in linear time, so semi-unification is P-hard even on the decidable classes that contain unification.

## Reductions

- **Unification to semi-unification.** For a fresh variable $z$, the equation $s \doteq t$ has a unifier if and only if $g(z, z) \le g(s, t)$ has a semi-unifier. If $s\theta = t\theta$, take $\sigma = \theta$ restricted away from $z$ and $\rho = \{z \mapsto s\theta\}$. Conversely, $g(z\sigma, z\sigma)\rho = g(s\sigma, t\sigma)$ gives $s\sigma = z\sigma\rho = t\sigma$.
- **Matching to semi-unification.** If $t$ is ground, $s \le t$ is semi-unifiable exactly when $s$ matches $t$.
- **Polymorphic recursion to semi-unification and back.** Typability in the Milner-Mycroft calculus, which is ML with polymorphic recursion, is equivalent to semi-unification under log-space reductions (Kfoury, Tiuryn and Urzyczyn 1993, Henglein 1993). Each recursive use of a function at a new type gives one inequality between the type of the definition and the type of the use. So type inference with polymorphic recursion is undecidable.
- **Turing machine boundedness to semi-unification.** This is the reduction behind undecidability.

## Applications

- **Type inference.** In ML, a recursive function is monomorphic inside its own definition, so type inference needs only unification. With polymorphic recursion, as in the Milner-Mycroft calculus, the uses inside the definition may instantiate its type, and inference becomes semi-unification. This is why Haskell accepts polymorphic recursion only with an explicit type signature, and why OCaml needs an explicit polymorphic annotation for it.
- **Loop detection in rewriting.** If a [rewrite rule](/rewrite-rule/) $l \to r$ has a subterm $r'$ of $r$ with $l\sigma\rho = r'\sigma$, then $l\sigma$ rewrites to a term that contains an instance of $l\sigma$, and the rewriting can go on forever. So a semi-unifier of $l \le r'$ shows that the system does not terminate.

## References
