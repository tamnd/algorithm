---
tag: QEJV4W
kind: concept
slug: occurs-check
name: Occurs check
aliases:
- occur check
area: logic-and-constraints/unification-and-resolution
level: core
summary: Test that a variable does not occur inside the term it would be bound to, preventing cyclic bindings.
prereqs: [unifier, unification-problem]
see_also: [robinson-unification, martelli-montanari-unification, paterson-wegman-unification, term-dag, cycle-detection, sld-resolution, warren-abstract-machine, binary-resolution]
sources:
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965, pages 23 to 41
    locator: the unification algorithm (the step that fails when the variable of the disagreement pair occurs in the other term)
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (the occurs-check rule of syntactic unification and unification without it)
  - paper: "Krzysztof R. Apt and Alessandro Pellegrini, On the occur-check-free Prolog programs, ACM Transactions on Programming Languages and Systems 16(3), 1994"
    locator: the introduction (why Prolog systems omit the occur check and the resulting unsoundness) and the sufficient conditions for programs that never need it
  - paper: "Alain Colmerauer, Prolog and infinite trees, in K. L. Clark and S.-A. Tärnlund (editors), Logic Programming, Academic Press, 1982"
    locator: the treatment of equations such as x = f(x) as equations over infinite rational trees
---

The **occurs check** is the test, inside a unification algorithm, that a variable $x$ does not occur in the term $t$ before the algorithm binds $x$ to $t$. If $x$ occurs in $t$ and $t \ne x$, the equation $x \doteq t$ has no solution in finite terms, and the algorithm must fail. Without the test, it would build a cyclic binding such as $x \mapsto f(x)$, and a resolution prover or a Prolog program could then derive false conclusions. The check is part of [Robinson's algorithm](/robinson-unification/) and of the [Martelli-Montanari rules](/martelli-montanari-unification/). Most Prolog systems leave it out by default for speed.

## In plain words

Unification fills blanks so that two patterns become equal. Suppose one blank must equal a pattern that contains the same blank, such as a box that must equal a bigger box with itself inside. No finite filling works: whatever you put in, the right side is larger than the left side. The occurs check looks for this case and says "no solution".

The check costs time, because it must look through the whole pattern. Many Prolog systems skip it. Then the system accepts the impossible filling and builds a pattern that loops back into itself. This is fast, and it is fine for most programs. But a program can then prove things that are false, and a printer or a comparison can run forever on the looped pattern.

## The idea

Notation, as in the rest of this area: $n$ is the number of variables, $\sigma, \theta$ are substitutions, $t\sigma$ is the application of $\sigma$ to $t$, and $\mathrm{Var}(t)$ is the set of variables of $t$.

**The rule.** In the transformation form of unification, the elimination step takes an equation $x \doteq t$ and applies $\{x \mapsto t\}$ to the rest. The occurs check is its side condition:

$$\{x \doteq t\} \cup E \;\Rightarrow\; \text{FAIL} \qquad \text{if } x \in \mathrm{Var}(t) \text{ and } t \ne x.$$

**Why failure is correct.** If $x \in \mathrm{Var}(t)$ and $t \ne x$, then $t$ is not a variable, and $x$ is a proper subterm of $t$. For every $\theta$, $x\theta$ is a proper subterm of $t\theta$, so $|t\theta| > |x\theta|$ and $x\theta \ne t\theta$. So no unifier exists.

**Indirect cycles.** The check must be done on the current terms, after earlier bindings are applied. In $\{x \doteq f(y),\ y \doteq g(x)\}$, neither equation fails the test by itself. After $x \mapsto f(y)$, the second equation becomes $y \doteq g(f(y))$, which fails. In graph terms, the bindings $x \to f(y)$ and $y \to g(x)$ form a cycle through the variables.

**Cost.** A direct test walks $t$, so it costs $O(|t|)$ per binding. Repeated tests on growing terms make naive unification quadratic or worse. Linear and almost linear algorithms do not test each binding. They unify first, as if over infinite trees, and then check that the graph of equivalence classes on the [term DAG](/term-dag/) is acyclic. This is one [cycle detection](/cycle-detection/) or [topological sort](/topological-sort/) pass, in linear time. The [Paterson-Wegman algorithm](/paterson-wegman-unification/) detects the cycle during its search, and the [Martelli-Montanari algorithm](/martelli-montanari-unification/) finds it when no multiequation has a free left side.

**Without the check.** Leaving out the test gives unification over **rational trees**: infinite trees with finitely many distinct subtrees, which are exactly the trees that a finite cyclic graph unfolds to. In that domain $x \doteq f(x)$ has the solution $x = f(f(f(\cdots)))$. Colmerauer's Prolog II made this the intended semantics. For a system that claims to reason about finite terms, it is unsound.

## Examples

**The unsound refutation.** Consider the two clauses

$$C_1 = \{P(x, f(x))\}, \qquad C_2 = \{\neg P(y, y)\}.$$

They are satisfiable together. Take the domain $\mathbb{N}$, let $f$ be the successor function and $P$ the relation $<$. Then $x < x + 1$ holds for all $x$, and $y < y$ holds for no $y$.

Resolution needs a unifier of $P(x, f(x))$ and $P(y, y)$. Decomposition gives $x \doteq y$ and $f(x) \doteq y$. After $x \mapsto y$, the second becomes $f(y) \doteq y$.

- With the occurs check, unification fails, no resolvent exists, and the prover does not derive the empty clause. This is correct.
- Without the occurs check, the algorithm binds $y \mapsto f(y)$, resolves, and derives the empty clause. It "proves" that a satisfiable set is unsatisfiable.

The same example as a Prolog program is the fact `less(X, s(X)).` with the query `?- less(Y, Y).` A system without the occurs check answers yes and binds `Y` to the cyclic term `s(s(s(...)))`. A system with the check answers no.

**Cases that pass or fail.**

| equation set | with the check | without the check |
|---|---|---|
| $x \doteq x$ | succeeds (delete) | succeeds |
| $x \doteq f(y)$ | succeeds, $\{x \mapsto f(y)\}$ | succeeds |
| $x \doteq f(x)$ | fails | binds $x$ to a cyclic term |
| $f(x, y) \doteq f(g(y), g(x))$ | fails, $x = g(g(x))$ | cyclic binding |
| $x \doteq f(x),\ y \doteq f(y),\ x \doteq y$ | fails | succeeds: both are $f(f(\cdots))$ |

**Type inference.** For the expression $\lambda x.\, x\, x$, type inference gives the equation $\alpha \doteq \alpha \to \beta$. The occurs check rejects it, and the expression has no simple type. Compilers of ML-family languages and Haskell report this as an occurs-check error or an infinite-type error.

## Where it is used

- **Resolution theorem provers** must perform the check, since a single unsound step can produce a false proof. [Binary resolution](/binary-resolution/), [factoring](/factoring/) and [superposition](/superposition/) all use unification with the check.
- **Prolog systems.** The ISO Prolog standard has the predicate `unify_with_occurs_check/2` next to the default `=/2`, whose result is undefined by the standard when the check would fail. SWI-Prolog has an `occurs_check` flag with the values `false` (the default), `true` and `error`, and by default it builds cyclic terms. The [Warren abstract machine](/warren-abstract-machine/) binds a variable in constant time because it does not check.
- **Occur-check-free programs.** Apt and Pellegrini give syntactic conditions, based on modes of arguments, under which a Prolog program never reaches a case where the check would fail. For such programs, omitting the check is safe.
- **Type checkers.** Hindley-Milner inference keeps the check, because a cyclic type means a type error. Some languages allow equirecursive types and then unify over rational trees on purpose.
- **Linear-time unification.** The [Paterson-Wegman](/paterson-wegman-unification/) and union-find algorithms move the check to one acyclicity test on a [term DAG](/term-dag/), which keeps the total cost linear or almost linear.

## References
