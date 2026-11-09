---
tag: W32K9K
kind: problem
slug: nominal-unification-problem
name: Nominal unification problem
aliases:
- nominal unification
- unification of nominal terms
area: logic-and-constraints/unification-and-resolution
level: research
summary: Unification of terms with binders up to α-equivalence, with names, swappings and freshness constraints. It is decidable and unitary, and the best known algorithms take quadratic time.
model: word-ram
complexity:
  vars: {N: the total size of the input terms and freshness problems}
  time: {decide: O(N^2)}
  space: {extra: O(N^2)}
prereqs: [unification-problem, most-general-unifier, lambda-calculus]
see_also: [urban-nominal-unification, pattern-unification-problem, miller-pattern-unification, higher-order-unification-problem, unification-problem, equational-unification]
sources:
  - paper: doi:10.1016/j.tcs.2004.06.016
    title: Christian Urban, Andrew M. Pitts and Murdoch J. Gabbay, Nominal unification, Theoretical Computer Science 323(1-3), 473 to 497 (2004)
    locator: the definitions of nominal terms, freshness and α-equivalence, the definition of the problem, and the theorem that solvable problems have most general solutions
  - paper: doi:10.4230/LIPIcs.RTA.2010.209
    title: Jordi Levy and Mateu Villaret, An efficient nominal unification algorithm, Proceedings of RTA 2010, LIPIcs 6, 209 to 226
    locator: the quadratic-time algorithm
  - paper: "Jordi Levy and Mateu Villaret, Nominal unification from a higher-order perspective, Proceedings of RTA 2008, Lecture Notes in Computer Science 5117, Springer"
    locator: the quadratic reduction of nominal unification to higher-order pattern unification
  - paper: "Christophe Calvès and Maribel Fernández, A polynomial nominal unification algorithm, Theoretical Computer Science 403(2-3), 285 to 306 (2008)"
    locator: the first polynomial bound for the problem
---

The nominal unification problem asks for a substitution that makes two terms with binders equal up to α-equivalence, that is, up to the renaming of bound names. Unlike the [higher-order unification problem](/higher-order-unification-problem/), it keeps the terms first-order: names (atoms) are a kind of constant, a binder is a term constructor $[a]t$, and renaming is done with swappings $(a\ b)$. A variable $X$ stands for a term that may mention names, so a substitution can capture them. Urban, Pitts and Gabbay defined the problem in 2004. They showed that it is decidable and that each solvable problem has a most general solution, made of a substitution and a set of *freshness constraints* $a \# X$. The best known algorithms run in quadratic time.

## In plain words

Programs and formulas have local names, as in "for all x" or a function parameter. Two pieces of code that differ only in the names of their local variables mean the same thing. Nominal unification fills holes in two such pieces so that they become the same up to this renaming. A hole may contain a name that a binder then captures, which is the usual case when you write a rule about programs. The answer is a best way to fill the holes, plus a list of side conditions of the form "this name must not appear free in that hole". A program can always find this answer or show that there is none.

## Definition

Fix a countable set of *atoms* $a, b, c, \ldots$, a set of *variables* $X, Y, \ldots$, and function symbols $f$ with arities. A *permutation* $\pi$ is a finite list of swappings $(a\ b)$. *Nominal terms* are

$$t ::= a \mid \pi \cdot X \mid [a]t \mid f(t_1, \ldots, t_n).$$

The term $\pi \cdot X$ is a *suspension*: the permutation waits until $X$ is replaced. The term $[a]t$ binds $a$ in $t$. A permutation acts on terms by swapping atoms everywhere, also at binders, and by $\pi \cdot (\pi' \cdot X) = (\pi \pi') \cdot X$. A substitution replaces variables, with $\sigma(\pi \cdot X) = \pi \cdot \sigma(X)$. It does not rename binders, so it can capture atoms: $[a]X$ with $X \mapsto a$ gives $[a]a$.

A *freshness context* $\nabla$ is a finite set of constraints $a \# X$, read "$a$ does not occur free in $X$". Two judgments are defined by rules:

- $\nabla \vdash a \# t$: the atom $a$ is not free in $t$. For example $\nabla \vdash a \# [a]t$ always, and $\nabla \vdash a \# \pi \cdot X$ if $\pi^{-1}(a) \# X \in \nabla$.
- $\nabla \vdash t \approx u$: the terms are α-equivalent. The main rules are $[a]t \approx [b]u$ if $a \neq b$, $t \approx (a\ b) \cdot u$ and $a \# u$; and $\pi \cdot X \approx \pi' \cdot X$ if $a \# X \in \nabla$ for each atom $a$ where $\pi$ and $\pi'$ differ.

For terms without variables, $\approx$ is ordinary α-equivalence and $\#$ is "not free in".

**Input.** A finite set $P$ of equations $t \approx^? u$ and freshness problems $a \#^? t$.

**Output.** A *solution* is a pair $(\nabla, \sigma)$ with $\nabla \vdash \sigma(t) \approx \sigma(u)$ for each equation and $\nabla \vdash a \# \sigma(t)$ for each freshness problem. A solution $(\nabla, \sigma)$ is *more general* than $(\nabla', \sigma')$ if there is a substitution $\tau$ with $\nabla' \vdash \tau(\nabla)$ and $\nabla' \vdash \tau(\sigma(X)) \approx \sigma'(X)$ for each variable $X$. The task is to find a most general solution, or to answer *no*.

Urban, Pitts and Gabbay proved that each solvable problem has a most general solution, so the problem is *unitary*, like first-order unification.

## Variants

- **Nominal matching.** Only one side has variables. It is easier, and Calvès and Fernández gave faster algorithms for it and for the α-equivalence check.
- **Equivariant unification.** The atoms in the problem may also be renamed by an unknown permutation, so that a rule can be used with any choice of names. Cheney studied this version and showed that it is NP-complete.
- **Nominal unification modulo equations.** As for [equational unification](/equational-unification/), function symbols can satisfy laws such as commutativity. These versions need other algorithms and are not unitary in general.

## Examples

**A freshness constraint.** The problem $[a]X \approx^? [b]Y$ has the most general solution $\nabla = \{a \# Y\}$, $\sigma = \{X \mapsto (a\ b) \cdot Y\}$. The constraint is needed: without it, $Y \mapsto a$ gives $[a]b$ and $[b]a$, which are not α-equivalent.

**Capture.** The problem $[a]a \approx^? [b]X$ has the solution $X \mapsto b$, with no constraints. The term $[b]b$ is α-equivalent to $[a]a$. In higher-order notation this is $\lambda a.\, a = \lambda b.\, X$, but there $X$ could not be $b$, because a higher-order substitution never captures.

**No solution.** The problem $[a]X \approx^? [b]a$ has no solution. The right side has $a$ free, and the left side binds $a$. Formally, the problem becomes $X \approx^? b$ and $a \#^? a$, and the second part fails.

**A suspension.** The problem $(a\ b) \cdot X \approx^? X$ has the solution $\nabla = \{a \# X, b \# X\}$ with the identity substitution. Swapping $a$ and $b$ changes nothing exactly when neither name is free in $X$.

## Known algorithms

| algorithm | year | time | notes |
|---|---|---|---|
| [Urban, Pitts and Gabbay](/urban-nominal-unification/) | 2004 | exponential on trees | rules in the style of [Martelli and Montanari](/martelli-montanari-unification/); first the equations, then the freshness problems |
| Calvès and Fernández | 2008 | polynomial | the first polynomial bound, with shared terms |
| Levy and Villaret | 2008 | $O(N^2)$ | a reduction to [higher-order pattern unification](/pattern-unification-problem/), then Qian's linear algorithm |
| Levy and Villaret | 2010 | $O(N^2)$ | a direct algorithm with lazy permutations |

Calvès, in his thesis (2010), also gave a quadratic algorithm, by a link with first-order unification.

## Bounds

The best known upper bound is $O(N^2)$ time (Levy and Villaret 2008 and 2010). Each algorithm must read its input, so $\Omega(N)$ is a lower bound. No better lower bound is known to us. As in [first-order unification](/unification-problem/), a most general solution written as trees can have size exponential in $N$, so fast algorithms keep terms shared.

## Reductions

- **First-order unification** is the special case with no atoms, no binders and empty permutations. So nominal unification is at least as hard.
- **To pattern unification.** Levy and Villaret (2008) reduced nominal unification to [higher-order pattern unification](/pattern-unification-problem/) in quadratic time. A variable $X$ becomes a higher-order variable applied to the atoms in the problem, and a freshness constraint says which arguments it may use. Cheney (2005) studied the relation between the two problems in both directions.
- **Full higher-order unification** is different: there, substitutions avoid capture and the problem is undecidable. Nominal unification gives up capture avoidance for variables and gains a simple, unitary problem.

## Applications

- **Logic programming with binders.** αProlog (Cheney and Urban 2004) uses nominal unification in place of first-order unification, so that programs about syntax with binders can be written as clauses.
- **Nominal rewriting.** Rewrite rules on nominal terms, as in the work of Fernández and Gabbay, match and unify left sides with nominal algorithms. Critical pairs need unification.
- **Rules about programs.** Typing rules and program transformations often mention a bound name and a context that may capture it. Nominal terms can state such rules directly.

## References
