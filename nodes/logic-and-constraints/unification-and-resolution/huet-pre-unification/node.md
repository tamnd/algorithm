---
tag: 29K6EF
kind: algorithm
slug: huet-pre-unification
name: Huet's pre-unification
aliases:
- Huet pre-unification
- Huet's higher-order unification procedure
area: logic-and-constraints/unification-and-resolution
level: research
summary: A semi-decision procedure for higher-order unification. It guesses heads by imitation or projection and stops when only flex-flex pairs are left, so it finds a complete set of pre-unifiers.
solves: [higher-order-unification-problem]
model: word-ram
properties: {deterministic: true}
history:
  year: 1975
  people: [Gérard Huet]
  note: Huet gave the procedure in his 1972 thesis and published it in Theoretical Computer Science in 1975, with the proof that it finds a complete set of pre-unifiers.
prereqs: [higher-order-unification-problem, lambda-calculus, beta-reduction, unifier]
see_also: [miller-pattern-unification, huet-unification, higher-order-unification-undecidability, pattern-unification-problem, robinson-unification, second-order-unification-problem]
sources:
  - paper: doi:10.1016/0304-3975(75)90011-0
    title: Gérard P. Huet, A unification algorithm for typed λ-calculus, Theoretical Computer Science 1(1), 27 to 57 (1975)
    locator: the whole paper (SIMPL, MATCH, the matching tree, and the completeness theorem for pre-unifiers)
  - paper: "Wayne Snyder and Jean H. Gallier, Higher-order unification revisited: complete sets of transformations, Journal of Symbolic Computation 8(1-2), 101 to 140 (1989)"
    locator: the transformation rules for pre-unification and their completeness
  - paper: "Gilles Dowek, Higher-order unification and matching, in Handbook of Automated Reasoning, volume II, Elsevier and MIT Press (2001)"
    locator: the section on Huet's algorithm and pre-unification
---

Huet's pre-unification is a search procedure for the [higher-order unification problem](/higher-order-unification-problem/): find a substitution for the free variables of two simply typed λ-terms that makes the terms equal up to $\beta\eta$. The problem is undecidable from third order on ([Huet 1973](/higher-order-unification-undecidability/)), so no procedure can always stop. Huet's procedure is the best possible kind: it lists a complete set of *pre-unifiers*, and it stops on each branch that has a solution. It leaves out the *flex-flex* pairs, where both sides start with a variable, because these pairs always have a solution and solving them in full would make the search branch without end. This page is about the higher-order procedure of 1975. The page [Huet's almost-linear unification](/huet-unification/) is about a different algorithm by the same author, for first-order terms.

## In plain words

We have two expressions with unknown functions in them, and we want to fill in the unknowns so that both expressions compute the same thing. Look at a place where one side starts with an unknown function and the other side starts with a known symbol. The answer for the unknown must start with something, and there are only a few choices. It can copy the known symbol, or it can return one of its own inputs. The procedure tries each choice, puts new unknowns for the parts it does not know yet, and goes on. When both sides of each equation start with an unknown, it stops: such equations can always be solved by a constant answer. Some problems have infinitely many different answers, so the search can go on forever.

## The problem

Terms are simply typed λ-terms in $\beta$-normal $\eta$-long form. Each term has the form $\lambda x_1 \ldots x_k.\, h(t_1, \ldots, t_m)$, where the head $h$ is a constant, a bound variable $x_i$, or a free variable. The term is *rigid* when $h$ is a constant or a bound variable, and *flex* when $h$ is a free variable. The input is a finite set $E$ of pairs $s \doteq t$ of closed terms of the same type, where only the free variables (the unknowns) are open.

A [unifier](/unifier/) of $E$ is a substitution $\delta$ with $\delta(s) =_{\beta\eta} \delta(t)$ for each pair. A *pre-unifier* is a substitution $\theta$ such that each pair of $\theta(E)$, after the rigid-rigid pairs are taken apart, gives only flex-flex pairs and no clash. A set $P$ of pre-unifiers is *complete* when for each unifier $\delta$ of $E$ there are $\theta \in P$ and a substitution $\rho$ with $\delta = \rho \circ \theta$ on the variables of $E$. The output of the procedure is a complete set of pre-unifiers, listed one by one, possibly without end.

## The algorithm

The procedure works on a search tree. A node holds a set of pairs and the substitution made so far. SIMPL takes rigid-rigid pairs apart. MATCH gives the possible first steps for a flex-rigid pair.

```pseudo id=main
PRE-UNIFY(E)
L1  Q ← a queue with the node (E, identity)
L2  while Q is not empty do
L3      (E, θ) ← take a node from Q
L4      E ← SIMPL(E)
L5      if E = fail then continue                         ▷ a clash: no unifier below this node
L6      if E has no flex-rigid pair then
L7          output (θ, E)                                 ▷ θ is a pre-unifier; E holds flex-flex pairs
L8          continue
L9      pick a flex-rigid pair λx̄. F(s̄) ≐ λx̄. a(t̄) in E
L10     for each binding ρ in MATCH(F, a) do
L11         put the node (ρ(E), ρ ∘ θ) in Q              ▷ ρ(E) is put in β-normal η-long form

SIMPL(E)
L12 while E has a pair λx̄. a(s̄) ≐ λx̄. b(t̄) with rigid heads a and b do
L13     if a ≠ b then return fail
L14     replace the pair by the pairs λx̄. s_i ≐ λx̄. t_i, for i = 1, ..., m
L15 turn each flex-rigid pair so that the flex side is on the left
L16 return E

MATCH(F, a)                                ▷ F has type τ1 → ... → τn → β, with β a base type
L17 R ← ∅
L18 if a is a constant of type σ1 → ... → σm → β then
L19     add to R the imitation  F ↦ λy1 ... yn. a(H1(ȳ), ..., Hm(ȳ))
L20 for each j with τj = ρ1 → ... → ρk → β do
L21     add to R the projection  F ↦ λy1 ... yn. yj(H1(ȳ), ..., Hk(ȳ))
L22 return R
```

In lines L19 and L21 each $H_i$ is a new free variable. When the argument place has a function type $\sigma_i = \gamma_1 \to \ldots \to \gamma_r \to \beta'$, the argument is the $\eta$-long term $\lambda z_1 \ldots z_r.\, H_i(\bar y, \bar z)$, so $H_i$ has type $\tau_1 \to \ldots \to \tau_n \to \sigma_i$. These bindings are the *general bindings*. They fix the head of the solution for $F$ and nothing more.

If the rigid head $a$ is a bound variable of the pair, then line L19 does not apply: the value of $F$ is a closed term, so it cannot name $a$. Only the projections remain, and these can bring $a$ in through the arguments $\bar s$.

The choice of the pair in line L9 is free, and the proof below works for each choice. The choice of the binding in line L10 is not free: the procedure must try all of them. The queue must be fair, for example first in first out, or a depth-first search with a depth bound that grows. A plain depth-first search can go down an infinite branch and never reach a solution on another branch. The Python implementation uses a stack with a depth bound, and the caller runs it with the bounds 1, 2, 3 and so on.

## Example

Take $F : \iota \to \iota$, constants $a : \iota$ and $g : \iota \to \iota \to \iota$, and the single pair $F(a) \doteq g(a, a)$. It is flex-rigid. MATCH gives two bindings.

| binding | new pairs after SIMPL | result |
|---|---|---|
| projection $F \mapsto \lambda y.\, y$ | $a \doteq g(a, a)$ | clash |
| imitation $F \mapsto \lambda y.\, g(H_1(y), H_2(y))$ | $H_1(a) \doteq a$, $H_2(a) \doteq a$ | go on |

Each new pair $H_i(a) \doteq a$ has two solutions: the projection $\lambda y.\, y$ and the imitation $\lambda y.\, a$. So the tree has four leaves with no pairs left. They give the four unifiers $\lambda y.\, g(y, y)$, $\lambda y.\, g(y, a)$, $\lambda y.\, g(a, y)$ and $\lambda y.\, g(a, a)$. No one of them is an instance of another, so this problem has no most general unifier.

The tree can be infinite. Take $G : (\iota \to \iota) \to \iota$ and the pair $G(\lambda u.\, u) \doteq a$. The imitation $G \mapsto \lambda y.\, a$ solves it. The projection $G \mapsto \lambda y.\, y(H(y))$ gives $H(\lambda u.\, u) \doteq a$, which is the same problem again. So the solutions are $\lambda y.\, y^k(a)$ for each $k \ge 0$, and the search lists them one by one. At depth $d$ the tree holds exactly $d$ of them.

A flex-flex pair stops the search at once. For $F(a) \doteq F(b)$ the procedure outputs the identity substitution with this pair left. The pair has the solution $F \mapsto \lambda y.\, H$ for a new variable $H$.

## Correctness

Three facts make the procedure correct. The full proofs are in the [correctness proof](proofs/correctness.md).

1. **SIMPL keeps the unifiers.** A substitution does not change a rigid head, because the values of the free variables are closed terms. So $\delta$ unifies $\lambda \bar x.\, a(\bar s) \doteq \lambda \bar x.\, a(\bar t)$ if and only if it unifies each pair of arguments, and no $\delta$ unifies a pair with two different rigid heads.
2. **Soundness.** Each output $\theta$ is a pre-unifier, by the test in line L6. Each flex-flex pair has a unifier: map each flex head $F : \tau_1 \to \ldots \to \tau_n \to \beta$ to $\lambda y_1 \ldots y_n.\, H_\beta$, with one new variable $H_\beta$ for each base type $\beta$. Then both sides of each pair become $H_\beta$. This is *Huet's lemma*. So each output gives a unifier of $E$.
3. **Completeness.** Let $\delta$ be a unifier of $E$. Follow the branch that $\delta$ selects: at a flex-rigid pair, the normal form of $\delta(F)$ starts with a constant or with one of its bound variables, and MATCH has exactly one binding with that head. A measure, the total size of the values of $\delta$ on the variables that are still open, goes down by one at each step. So the branch ends after a finite number of steps, at an output node $\theta$ with $\theta \le \delta$.

## Complexity

No bound on the run time is possible, because the problem is undecidable. A node has at most $n + 1$ children, where $n$ is the number of arguments of the flex head. A unifier $\delta$ is found at a depth of at most the total number of head symbols in the values of $\delta$, by the measure in the completeness proof. So a breadth-first search finds each unifier after a finite number of steps. The work at a node is the $\beta$-normalization of the new pairs, and this can make terms larger. The tree can be infinite even when the problem has a solution, as the example with $G$ shows.

## Properties

- **Semi-decision procedure.** If $E$ has a unifier, a fair search outputs a pre-unifier after a finite time. If $E$ has no unifier, the search can run forever.
- **Not unitary.** A problem can have many independent unifiers, and even an infinite set of them with no most general one.
- **Don't care and don't know.** The choice of the pair is a don't-care choice. The choice of the binding is a don't-know choice.
- **Exact for first order.** On first-order terms, MATCH has only the imitation, and the procedure becomes a form of [Robinson unification](/robinson-unification/) without an [occurs check](/occurs-check/). A first-order failure of the occurs check shows up as an infinite branch.

## Variants and improvements

- **Full unification.** Jensen and Pietrzykowski (1976) gave a procedure that also enumerates the solutions of flex-flex pairs. It must guess heads for both sides, so it branches much more.
- **Transformation rules.** Snyder and Gallier (1989) wrote the procedure as a set of rules on pairs, in the style of [Martelli and Montanari](/martelli-montanari-unification/), and proved the rules complete.
- **Patterns.** When each free variable is applied to distinct bound variables, the problem is decidable and has a most general unifier. [Miller's pattern unification](/miller-pattern-unification/) solves it with no search. Many systems use it first and fall back to Huet's procedure, or delay the pairs that are not patterns.
- **Matching.** When one side has no free variables, the problem is [higher-order matching](/higher-order-unification-problem/). It is decidable (Stirling 2009), but Huet's procedure alone does not decide it.

## When to use it

Use it when the terms are higher-order and not patterns, and when an incomplete or slow search is acceptable. Huet built it for resolution in higher-order logic, where flex-flex pairs stay as constraints on the clause. Higher-order logic programming in λProlog and the elaborators of proof assistants use it, often with delays and depth limits. For first-order terms, use [Robinson](/robinson-unification/) or [Martelli and Montanari](/martelli-montanari-unification/) unification. For patterns, use [Miller's algorithm](/miller-pattern-unification/).

## Pitfalls

- **Plain depth-first search.** The pair $G(\lambda u.\, u) \doteq a$ has an infinite branch of projections. A depth-first search that explores projections first never outputs the imitation. Use iterative deepening or a queue.
- **No occurs check.** The pair $F(a) \doteq f(F(a))$ has no unifier, but the imitation branch repeats the same problem forever. The occurs check of first-order unification is not valid in general: $F \doteq f(G(F))$, with $F : \iota$ and $G : \iota \to \iota$, has the unifier $F \mapsto f(a)$, $G \mapsto \lambda u.\, a$, because the value of $G$ can drop its argument.
- **Projections of the wrong type.** A projection on $y_j$ is only possible when the result type of $\tau_j$ is the base type $\beta$ of the pair.
- **Missing η-expansion.** The arguments $H_i(\bar y)$ of a general binding must be in η-long form. Without it, SIMPL can compare terms that are equal up to η and report a clash.
- **Pre-unifier is not unifier.** An output $\theta$ alone does not unify $E$. Apply Huet's lemma to the flex-flex pairs that are left to get a unifier.

## Implementations

## History

Huet described the procedure in his 1972 thesis at Case Western Reserve University, as the unification step of *constrained resolution* for higher-order logic. In that method the flex-flex pairs stay on the clauses as constraints, so the prover never has to solve them. He published the procedure and its completeness proof in Theoretical Computer Science in 1975. In 1973 he had shown that third-order unification is undecidable, so a semi-decision procedure was the best result possible. Jensen and Pietrzykowski gave a full unification procedure in 1976, and Snyder and Gallier recast Huet's procedure as transformation rules in 1989.

## References
