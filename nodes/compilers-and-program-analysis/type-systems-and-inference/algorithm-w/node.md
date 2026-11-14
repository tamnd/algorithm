---
tag: BA10YT
kind: algorithm
slug: algorithm-w
name: Algorithm W
aliases:
- Damas-Milner algorithm W
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: Infers the principal type of an ML term bottom-up by unification, generalizing free type variables at each let binding.
solves: [type-inference-problem]
model: word-ram
complexity:
  vars: {n: the number of nodes of the term}
  time: {worst: 2^(2^O(n)), best: Θ(n)}
  space: {extra: 2^(2^O(n))}
properties: {deterministic: true, recursive: true}
prereqs: [hindley-milner-type-system, robinson-unification, most-general-unifier]
see_also: [algorithm-j, principal-type-theorem, constraint-based-type-inference, let-polymorphism, type-inference-problem, occurs-check, ml-typability-dexptime-completeness, value-restriction]
sources:
  - paper: doi:10.1145/582153.582176
    title: Luis Damas and Robin Milner, Principal type-schemes for functional programs, Ninth ACM Symposium on Principles of Programming Languages (POPL 1982), pages 207 to 212
    locator: the definition of algorithm W, Theorem 1 (soundness of W) and Theorem 2 (completeness of W), with the principal type-scheme corollary
  - paper: doi:10.1016/0022-0000(78)90014-4
    title: Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375
    locator: Section 4 (algorithm W, its soundness theorem, and the more efficient algorithm J)
  - paper: doi:10.1145/291891.291892
    title: Oukseh Lee and Kwangkeun Yi, Proofs about a folklore let-polymorphic type inference algorithm, ACM Transactions on Programming Languages and Systems 20(4), 1998, pages 707 to 723
    locator: the soundness and completeness proofs for W and for the top-down algorithm M, and the comparison of where the two algorithms detect a type error
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 22 (constraint typing, unification, principal types, and Section 22.7 on let-polymorphism and its cost)
  - paper: doi:10.1145/321250.321253
    title: J. A. Robinson, A machine-oriented logic based on the resolution principle, Journal of the ACM 12(1), 1965, pages 23 to 41
    locator: the unification algorithm and the most general unifier, which W calls at each application
  - paper: doi:10.1007/3-540-52590-4_50
    title: A. J. Kfoury, J. Tiuryn and P. Urzyczyn, ML typability is dexptime-complete, CAAP 1990, LNCS 431, Springer, pages 206 to 220
    locator: the exponential upper bound for typability with shared types, and the lower bound
  - paper: doi:10.1007/3-540-44881-0_31
    title: David McAllester, A logical algorithm for ML type inference, Rewriting Techniques and Applications (RTA 2003), LNCS 2706, Springer, pages 436 to 451
    locator: the nearly linear time bound for programs whose types have bounded order and arity
---

Algorithm W computes the [principal type](/principal-type-theorem/) of a term of the [Hindley-Milner type system](/hindley-milner-type-system/), or reports that the term has no type. It walks the term from the leaves up. At each variable it makes a fresh copy of the type scheme. At each application it calls [unification](/robinson-unification/) to make the function type and the argument type fit. At each `let` it generalizes the type variables that the context does not mention. Milner (1978) designed it for ML, and Damas and Milner (1982) proved that it is sound and complete. It needs no type annotations at all. Its running time is exponential in the worst case, and doubly exponential if types are stored as trees, but on real programs it is fast.

## In plain words

W reads a program and works out the type of each piece, from the smallest pieces up. When it meets a name it knows nothing about, it writes a placeholder, such as "some type a". When a function is applied to an argument, it compares the two types and fills in placeholders so that they fit. If they cannot fit, for example a number where a function is needed, the program has a type error. When a `let` gives a name to a finished piece, W marks the placeholders that nothing outside depends on as free to vary. Each later use of the name gets new copies of those placeholders, so one helper can work with numbers in one place and with text in another. The answer is the most general type: every other correct type for the program is a special case of it.

## The problem

Input: a context $\Gamma$ that maps term variables to type schemes, and a term $e$ of the language `x`, `fun x -> e`, `e1 e2`, `let x = e1 in e2`, with constants, `if`, integer operators and `fix f x -> e`.

Output: a substitution $S$ and a type $\tau$ with $S\Gamma \vdash e : \tau$ in the Hindley-Milner rules, such that each other solution is an instance of $(S, \tau)$. If no substitution $R$ and type $\tau'$ give $R\Gamma \vdash e : \tau'$, the output is a failure. For a closed term, $\Gamma$ is empty and $\tau$ is the principal type. This is the [type inference problem](/type-inference-problem/) for ML.

## The algorithm

A *substitution* maps type variables to types. $S_2 S_1$ means "first $S_1$, then $S_2$". A variable is *fresh* if it was never used before. $\mathrm{GEN}(\Gamma, \tau)$ is the scheme $\forall \vec\alpha.\, \tau$, where $\vec\alpha$ are the variables of $\tau$ that are not free in $\Gamma$. MGU is a [most general unifier](/most-general-unifier/) with the [occurs check](/occurs-check/), for example Robinson's algorithm.

```pseudo id=main
W(Γ, e)                                   ▷ returns (S, τ) with SΓ ⊢ e : τ, or fails
L1  if e is a variable x then let ∀α1 ... αk. τ be Γ(x)      ▷ fail if x is not in Γ
L2      return (id, [α1 := β1, ..., αk := βk] τ)              ▷ β1 ... βk fresh
L3  if e is fun x -> e1 then β ← fresh
L4      (S1, τ1) ← W((Γ, x : β), e1)
L5      return (S1, S1 β → τ1)
L6  if e is e1 e2 then (S1, τ1) ← W(Γ, e1)
L7      (S2, τ2) ← W(S1 Γ, e2)
L8      β ← fresh, S3 ← MGU(S2 τ1, τ2 → β)                   ▷ fail if there is no unifier
L9      return (S3 S2 S1, S3 β)
L10 if e is let x = e1 in e2 then (S1, τ1) ← W(Γ, e1)
L11     σ ← GEN(S1 Γ, τ1)                                    ▷ only variables not free in S1 Γ
L12     (S2, τ2) ← W((S1 Γ, x : σ), e2)
L13     return (S2 S1, τ2)
L14 if e is fix f x -> e1 then α, β ← fresh, (S1, τ1) ← W((Γ, f : α → β, x : α), e1)
L15     S2 ← MGU(S1 β, τ1), return (S2 S1, S2 S1 (α → β))
```

Constants return their base type with the identity substitution. `if e1 then e2 else e3` and `e1 op e2` are like L6 to L9: they call W on each part in turn, apply each new substitution to the context, and unify the condition with $\mathsf{bool}$, the operands with $\mathsf{int}$ and the two branches with each other. Note that $f$ and $x$ in line L14 get plain types, not schemes. So a recursive function is monomorphic in its own body.

## Example

Take `let id = fun x -> x in id id`. Write $\beta_0, \beta_1, \ldots$ for the fresh variables in the order W makes them.

| step | call | result |
|---|---|---|
| L10 | W(∅, `fun x -> x`) | L3 makes $\beta_0$. The body `x` gives $(\mathrm{id}, \beta_0)$, so the result is $(\mathrm{id}, \beta_0 \to \beta_0)$ |
| L11 | GEN(∅, $\beta_0 \to \beta_0$) | $\sigma = \forall \beta_0.\, \beta_0 \to \beta_0$, since the context is empty |
| L6 | W(id : σ, `id`) | a fresh copy $\beta_1 \to \beta_1$ |
| L7 | W(id : σ, `id`) | another fresh copy $\beta_2 \to \beta_2$ |
| L8 | MGU($\beta_1 \to \beta_1$, $(\beta_2 \to \beta_2) \to \beta_3$) | $S_3 = [\beta_1 := \beta_2 \to \beta_2,\ \beta_3 := \beta_2 \to \beta_2]$ |
| L9 | | the type $S_3\beta_3 = \beta_2 \to \beta_2$ |

The principal type is $a \to a$. The two uses of `id` got different instances, $(\beta_2 \to \beta_2) \to \beta_2 \to \beta_2$ and $\beta_2 \to \beta_2$, which is possible only because line L11 quantified $\beta_0$.

Now take `fun x -> let y = x in if y true then y 1 else 0`. Line L3 gives `x` the type $\beta_0$. At line L11 the context is $x : \beta_0$, so $\beta_0$ is free in it and GEN returns $\beta_0$ with no quantifier. Then `y true` unifies $\beta_0$ with $\mathsf{bool} \to \beta_1$, and `y 1` must unify $\mathsf{bool} \to \beta_1$ with $\mathsf{int} \to \beta_2$, which fails. The term has no type, which is right: applied to `5`, it would get stuck at `5 true`.

## Correctness

Two theorems say that W is correct. *Soundness:* if $W(\Gamma, e) = (S, \tau)$, then $S\Gamma \vdash e : \tau$. *Completeness:* if $R\Gamma \vdash e : \tau'$ for some substitution $R$, then W succeeds with $(S, \tau)$, and $\tau' = R'\tau$ and $R\Gamma = R'S\Gamma$ for some $R'$. Both are proved by induction on $e$. Soundness needs the type substitution lemma: if $\Gamma \vdash e : \tau$, then $S\Gamma \vdash e : S\tau$. That lemma holds only because GEN skips the variables that are free in the context. Completeness needs the fact that $R_3 = R_4 S_3$ for any unifier $R_3$ at line L8, which is the most general unifier property, and a lemma that a more general scheme in the context keeps each judgment true. For a closed term, the two theorems together say that W returns the principal type. The [proof file](proofs/correctness.md) proves both theorems in full for the syntax-directed rules. It cites Damas (1985) for the equivalence with the rules that have explicit generalization and instantiation steps.

## Complexity

Let $n$ be the number of nodes of the term. W makes one call per node, but the cost of a call depends on the size of the types.

- **Without `let`.** The term is a simply typed term, and the types are those of Hindley's algorithm. Robinson's unification on trees can build types of exponential size. With shared types, a [union-find](/disjoint-set-forest/) structure and one test for cycles at the end in place of an occurs check at each step, the time is $O(n\,\alpha(n))$.
- **Exponential types.** Let $y_0 = $ `fun x -> x` and $y_i = $ `fun z -> z` $y_{i-1}\ y_{i-1}$, nested by `let`, and return $y_k$. The term has $7k + 4$ nodes. The principal type has $8 \cdot 2^k - 5$ nodes and $2^{k+1} - 1$ type variables. Since the output alone is that large, W needs time $2^{\Omega(n)}$, even with sharing.
- **Doubly exponential trees.** Let $f_0 = $ `fun x -> fun z -> z x x` and $f_i = $ `fun y -> ` $f_{i-1}\ (f_{i-1}\ y)$, nested by `let`. The term has $7k + 9$ nodes. As a tree, the principal type of $f_k$ has $6 \cdot 2^{2^k} - 3$ nodes, for example 393,213 nodes at $k = 4$. As a DAG with shared subtypes it has only $2^{k+2} + 2$ nodes. So W with types stored as trees takes time $2^{2^{\Omega(n)}}$, and with shared types the cost stays $2^{O(n)}$.
- **Upper bound.** With shared types, W runs in $2^{O(n)}$ time (Kfoury, Tiuryn and Urzyczyn 1990). The [typability problem is complete for EXPTIME](/ml-typability-dexptime-completeness/), and EXPTIME contains problems that are not in polynomial time. So no algorithm for ML typability runs in polynomial time.
- **Bounded nesting.** If the nesting depth of `let` is bounded by a constant, the time is polynomial. McAllester (2003) gives a nearly linear bound when the types have bounded order and arity, which explains why compilers are fast in practice.

A plain implementation also applies each substitution to the whole context at lines L7 and L12. This costs $O(|\Gamma|)$ per step and $O(n^2)$ over the run even for small types. Algorithm J removes this cost.

## Properties

- **Principal results.** For a closed term, the result type is principal, and it is unique up to renaming of type variables.
- **Deterministic.** The result depends only on the input, up to the names of the fresh variables.
- **Error location.** W finds an error at the first unification that fails, in a left to right walk. This is often far from the real mistake. Algorithm M finds some errors earlier.
- **Purely functional.** W returns substitutions and never changes a shared structure. This makes it easy to prove correct and costly to run.
- **Compositional in one direction.** The type of a subterm does not depend on the terms to its right, but it can change when later substitutions are applied.

## Variants and improvements

- **[Algorithm J](/algorithm-j/).** One global substitution in a union-find structure, changed in place. It returns the same types, without the cost of composing and applying substitutions.
- **Levels.** Each type variable stores the `let` depth at which it was made. GEN then quantifies the variables with a deeper level, without a scan of the context. This is Rémy's method, used by OCaml.
- **Algorithm M.** Lee and Yi (1998) proved the folklore top-down algorithm correct. It passes the expected type down into the term, and it stops at the first subterm that cannot have the expected type.
- **[Constraint-based inference](/constraint-based-type-inference/).** First generate the equations, then solve them. HM(X) extends this to other constraint domains, such as [subtyping](/subtyping/) or [type classes](/type-classes/).
- **[Value restriction](/value-restriction/).** In a language with mutable references, line L11 quantifies only if $e_1$ is a syntactic value.
- **[Bidirectional type checking](/bidirectional-type-checking/).** Uses written annotations to check richer types, and falls back on W-style inference for the rest.

## When to use it

Use W to learn Hindley-Milner inference, to prove facts about it, or in a small interpreter where speed does not matter. Its cases follow the typing rules one by one, so each line has a direct proof. For a compiler, use algorithm J with levels, or constraint-based inference, which compute the same types faster and give better error messages. For languages with first-class polymorphism or subtyping, W alone is not enough.

## Pitfalls

- **Generalizing too much.** Line L11 must skip the variables that are free in $S_1\Gamma$. If it quantifies them, `fun x -> let y = x in if y true then y 1 else 0` gets a type, and the application of it to `5` gets stuck.
- **Using the old context.** Line L7 and line L12 must use $S_1\Gamma$, not $\Gamma$. The scheme in line L11 must also be computed against $S_1\Gamma$: in the old context, a variable that $S_1$ has removed would look free.
- **Leaving out the occurs check.** Without it, `fun x -> x x` gets the cyclic type $\alpha = \alpha \to \beta$, and the program may loop when it prints or applies the substitution.
- **Order of composition.** The result substitution is $S_3 S_2 S_1$, with $S_1$ applied first. Any other order gives wrong types.
- **Believing that W is polynomial.** It is not cubic or polynomial. Nested `let` makes the types exponential, and trees without sharing make them doubly exponential.
- **Polymorphic recursion.** Giving $f$ a scheme in line L14 does not make W infer polymorphic recursion. That problem is [undecidable](/polymorphic-recursion-undecidability/), and languages ask for a type signature instead.

## Implementations

## History

Hindley (1969) proved that each typable object of combinatory logic has a principal type scheme, and found it with Robinson's unification of 1965. Milner, without knowing Hindley's work, designed the type discipline of ML for the LCF theorem prover. His 1978 paper adds polymorphism at `let`, defines algorithm W, proves it sound, and gives the faster algorithm J. Damas and Milner (1982) proved that W is complete, so that each typable term has a principal type scheme. The full proofs are in Damas's thesis of 1985. In 1990, Mairson and Kfoury, Tiuryn and Urzyczyn showed that ML typability is complete for exponential time, which ended the belief that W runs in polynomial time. Lee and Yi (1998) proved the folklore top-down algorithm M correct and compared it with W.

## References
