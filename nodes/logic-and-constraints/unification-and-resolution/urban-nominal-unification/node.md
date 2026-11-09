---
tag: 5H4NV6
kind: algorithm
slug: urban-nominal-unification
name: Urban-Pitts-Gabbay nominal unification
aliases:
- nominal unification algorithm
- UPG nominal unification
area: logic-and-constraints/unification-and-resolution
level: research
summary: Transformation rules for nominal unification. Equations are simplified first, then freshness problems. The result is a most general solution, a substitution with freshness constraints.
solves: [nominal-unification-problem]
model: word-ram
properties: {deterministic: true}
history:
  year: 2004
  people: [Christian Urban, Andrew M. Pitts, Murdoch J. Gabbay]
  note: Urban, Pitts and Gabbay gave the rules, the correctness proof and the theorem that solvable problems have most general solutions, in a conference paper (CSL 2003) and in Theoretical Computer Science (2004).
prereqs: [nominal-unification-problem, martelli-montanari-unification, most-general-unifier, occurs-check]
see_also: [miller-pattern-unification, pattern-unification-problem, robinson-unification, unification-problem, huet-unification]
sources:
  - paper: doi:10.1016/j.tcs.2004.06.016
    title: Christian Urban, Andrew M. Pitts and Murdoch J. Gabbay, Nominal unification, Theoretical Computer Science 323(1-3), 473 to 497 (2004)
    locator: the rules for freshness and α-equivalence, the transformation rules for equations and freshness problems, and the correctness theorem
  - paper: doi:10.4230/LIPIcs.RTA.2010.209
    title: Jordi Levy and Mateu Villaret, An efficient nominal unification algorithm, Proceedings of RTA 2010, LIPIcs 6, 209 to 226
    locator: the analysis of the exponential cost of the naive rules and the quadratic algorithm
---

The Urban-Pitts-Gabbay algorithm solves the [nominal unification problem](/nominal-unification-problem/): it unifies terms with binders up to α-equivalence, where variables may capture names. It is a set of transformation rules, like the [Martelli-Montanari rules](/martelli-montanari-unification/) for first-order terms, with two new ideas. Two abstractions $[a]t$ and $[b]u$ with different names are compared by swapping $a$ and $b$ in $u$ and asking that $a$ is fresh for $u$. A variable under a permutation, $\pi \cdot X$, is solved by putting the inverse permutation on the other side. The output is a most general solution: a substitution and a set of freshness constraints $a \# X$. Urban, Pitts and Gabbay published it in 2004, with the proof that each solvable problem has a most general solution.

## In plain words

Terms here have local names, and two terms count as equal if they differ only in the names of their local binders. The algorithm takes the equations apart from the top. If both sides bind the same name, compare the bodies. If they bind different names $a$ and $b$, swap $a$ and $b$ in one body, compare again, and note that $a$ must not appear free in that body. When one side is a hole with some swaps waiting on it, fill the hole with the other side, with the swaps undone. When only the "must not appear" notes are left, simplify them to notes about holes, or fail if a name must not appear in itself.

## The problem

The input is a finite set $E$ of equations $t \approx^? u$ between nominal terms and a finite set $F$ of freshness problems $a \#^? t$. Nominal terms are atoms $a$, suspensions $\pi \cdot X$, abstractions $[a]t$ and applications $f(t_1, \ldots, t_n)$, where $\pi$ is a finite list of swappings. The output is a most general solution $(\nabla, \sigma)$, where $\nabla$ is a set of constraints $a \# X$ and $\sigma$ is a substitution, or *fail* if there is no solution. The [problem page](/nominal-unification-problem/) gives the definitions of $\approx$, $\#$ and of a solution.

The *disagreement set* of two permutations is $ds(\pi, \pi') = \{a \mid \pi(a) \neq \pi'(a)\}$. A substitution acts on a suspension by $\sigma(\pi \cdot X) = \pi \cdot \sigma(X)$, so it can capture atoms.

## The algorithm

```pseudo id=main
NOMINAL-UNIFY(E, F)          ▷ E: equations t ≈? u, F: freshness problems a #? t
L1  σ ← the identity substitution
L2  while E is not empty do
L3      take an equation t ≈? u out of E
L4      if t and u are atoms then
L5          if t ≠ u then return fail
L6      else if t = f(t_1..t_n) and u = f(u_1..u_n) then add t_i ≈? u_i to E for each i
L7      else if t = [a]t' and u = [a]u' then add t' ≈? u' to E
L8      else if t = [a]t' and u = [b]u' with a ≠ b then add t' ≈? (a b)·u' to E and a #? u' to F
L9      else if t = π·X and u = π'·X then add a #? X to F for each a in ds(π, π')
L10     else if one side is π·X and X does not occur in the other side s then ρ ← [X := π⁻¹·s], apply ρ to E, F and σ, σ ← ρ ∘ σ
L11     else return fail                       ▷ a clash, or X occurs in s
L12 ∇ ← ∅
L13 while F is not empty do take a problem a #? t out of F
L14     if t is an atom b then: if a = b then return fail
L15     if t = [a]t' then drop the problem
L16     if t = [b]t' with b ≠ a then add a #? t' to F
L17     if t = f(t_1..t_n) then add a #? t_i to F for each i
L18     if t = π·X then add π⁻¹(a) # X to ∇
L19 return (∇, σ)
```

The first phase (lines L2 to L11) removes all equations. It moves the work about names into $F$ and builds $\sigma$. The second phase (lines L13 to L18) turns the freshness problems into constraints on variables. Line L10 is the only place where a variable is bound, and the [occurs check](/occurs-check/) is part of its test. A permutation never changes the size or the shape of a term, so $\pi \cdot X \approx^? s$ with $X$ inside $s$ has no solution.

## Example

Solve $[a]f(X, b) \approx^? [b]f(Y, a)$, with function symbol $f$ of arity 2.

| step | line | action | E and F after the step | σ |
|---|---|---|---|---|
| 1 | L8 | different binders $a$, $b$: swap in the right body | $E = \{f(X, b) \approx^? f((a\ b) \cdot Y, b)\}$, $F = \{a \#^? f(Y, a)\}$ | $\emptyset$ |
| 2 | L6 | same symbol $f$ | $E = \{X \approx^? (a\ b) \cdot Y,\ b \approx^? b\}$ | $\emptyset$ |
| 3 | L4 | $b = b$ | $E = \{X \approx^? (a\ b) \cdot Y\}$ | $\emptyset$ |
| 4 | L10 | bind $X$ | $E = \emptyset$ | $X \mapsto (a\ b) \cdot Y$ |
| 5 | L17 | split $a \#^? f(Y, a)$ | $F = \{a \#^? Y,\ a \#^? a\}$ | |
| 6 | L14 | $a \#^? a$ | fail | |

There is no solution: the right term $[b]f(Y, a)$ has $a$ free, and the left term binds $a$. If the right term is $[b]f(Y, c)$, step 2 gives $b \approx^? (a\ b) \cdot c = c$, which fails in line L5. If it is $[b]f(Y, b)$, then $(a\ b) \cdot b = a$ and step 2 gives $b \approx^? a$, which also fails. For $[a]f(X, a) \approx^? [b]f(Y, b)$ the run succeeds with $\nabla = \{a \# Y\}$ and $\sigma = \{X \mapsto (a\ b) \cdot Y\}$.

## Correctness

The full proof is in the [correctness proof](proofs/correctness.md). It rests on facts about nominal terms that Urban, Pitts and Gabbay prove first: $\approx$ is an equivalence relation under each $\nabla$, permutations preserve $\approx$ and $\#$, and $\nabla \vdash \pi \cdot t \approx \pi' \cdot t$ holds exactly when $\nabla \vdash a \# t$ for each $a \in ds(\pi, \pi')$.

1. **Each step keeps the solutions.** For each rule, a pair $(\nabla', \theta)$ solves the problem before the step if and only if it solves the problem after it. For line L10, a solution satisfies $\theta(X) \approx \pi^{-1} \cdot \theta(s)$, so it agrees with $\theta \circ \rho$ up to $\approx$.
2. **Failure is correct.** A clash of atoms, of symbols or of term shapes, a variable that occurs inside its own value, and a problem $a \#^? a$ have no solution.
3. **The result is most general.** The pair $(\nabla, \sigma)$ is a solution, and each solution $(\nabla', \theta)$ satisfies $\nabla' \vdash \theta(\nabla)$ and $\nabla' \vdash \theta(\sigma(X)) \approx \theta(X)$. So $\theta$ itself is the $\tau$ of the definition.
4. **Termination.** Each step of the first phase lowers the number of variables in $E$ (line L10) or keeps it and lowers the total size of $E$. Each step of the second phase lowers the size of $F$.

## Complexity

With terms stored as trees, the run can take time exponential in $N$, the size of the input. The reason is the same as for [Robinson's algorithm](/robinson-unification/): the equations $X_1 \approx^? f(X_0, X_0), \ldots, X_n \approx^? f(X_{n-1}, X_{n-1})$ make the value of $X_n$ a tree of size about $2^n$. The permutations can also grow, since line L8 adds a swapping to a body each time. With shared terms and lazy permutations, Levy and Villaret (2010) and Calvès and Fernández made the problem solvable in $O(N^2)$ time. The rules stay the same in spirit, so this page describes the rule system, and the [problem page](/nominal-unification-problem/) lists the faster algorithms.

## Properties

- **Unitary.** Each solvable problem has one most general solution, a pair of a substitution and freshness constraints.
- **Terminating and complete.** The algorithm always stops, and it fails only if there is no solution.
- **First-order at heart.** Without atoms and binders it is the Martelli-Montanari algorithm.
- **Constraints only on variables.** The final $\nabla$ only says which atoms may not be free in which variables.

## Variants and improvements

- **Quadratic algorithms.** Levy and Villaret (2010) gave a direct quadratic algorithm, and they also reduced the problem to [pattern unification](/pattern-unification-problem/) in quadratic time (2008). Calvès and Fernández gave polynomial and quadratic versions.
- **Matching.** If one side has no variables, the same rules solve nominal matching, which is faster.
- **Equivariant unification.** If the atoms of a rule may be renamed, the problem becomes NP-complete (Cheney), and this algorithm is used with a search over permutations.

## When to use it

Use it when terms have binders and when a rule must mention a name that a context can capture, as in a typing rule or a program transformation. It is the unification step of αProlog and of nominal rewriting. If capture is never needed, and the terms are [Miller patterns](/miller-pattern-unification/), a higher-order pattern unifier works too. For large inputs, use a quadratic algorithm with shared terms.

## Pitfalls

- **Treating substitution as capture avoiding.** In nominal terms $[a]X$ with $X \mapsto a$ is $[a]a$. Renaming the binder first would give a different and wrong answer.
- **Dropping the freshness side condition.** In line L8 the problem $a \#^? u'$ is needed. Without it, $[a]X \approx^? [b]Y$ would allow $Y \mapsto a$.
- **The direction of the permutation.** Line L10 binds $X$ to $\pi^{-1} \cdot s$, not to $\pi \cdot s$. The two differ when $\pi$ is not its own inverse.
- **Applying the substitution to F.** The freshness problems mention variables too, so line L10 must apply $\rho$ to $F$ as well as to $E$.

## Implementations

## History

Christian Urban, Andrew Pitts and Murdoch Gabbay presented nominal unification at CSL 2003, and the journal version appeared in Theoretical Computer Science in 2004. It builds on the nominal approach to syntax with binders of Gabbay and Pitts (1999 and 2002), where swappings and freshness replace capture-avoiding substitution. Cheney and Urban used it in αProlog (2004). Calvès and Fernández (2008) gave the first polynomial algorithm, and Levy and Villaret (2008 and 2010) gave quadratic ones.

## References
