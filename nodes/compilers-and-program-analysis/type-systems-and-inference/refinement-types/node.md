---
tag: 1VRD55
kind: concept
slug: refinement-types
name: Refinement types
aliases:
- refinement type system
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Types that carry a logical predicate on their values, such as the integers greater than zero, checked with a decision procedure.
prereqs: [simply-typed-lambda-calculus, subtyping, smt-problem]
see_also: [liquid-types, dependent-types, decision-procedure, presburger-arithmetic, euf-satisfiability, nelson-oppen, verification-condition-generation, hoare-logic]
sources:
  - paper: doi:10.1145/113445.113468
    title: Tim Freeman and Frank Pfenning, Refinement types for ML, ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 1991), pages 268 to 277
    locator: refinements of ML datatypes into subsorts, intersection types for functions, and the inference of refinements by abstract interpretation over a finite lattice
  - paper: doi:10.1145/277650.277732
    title: Hongwei Xi and Frank Pfenning, Eliminating array bound checking through dependent types, ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 1998), pages 249 to 257
    locator: types indexed by integer expressions with linear constraints, checked by a constraint solver, and the removal of array bound checks
  - paper: doi:10.1145/1375581.1375602
    title: Patrick M. Rondon, Ming Kawaguchi and Ranjit Jhala, Liquid types, ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2008), pages 159 to 169
    locator: the refinement type rules with dependent function types, subtyping by implication in a decidable logic, and the path-sensitive environment
  - paper: doi:10.1145/2628136.2628161
    title: Niki Vazou, Eric L. Seidel, Ranjit Jhala, Dimitrios Vytiniotis and Simon Peyton Jones, Refinement types for Haskell, ACM SIGPLAN International Conference on Functional Programming (ICFP 2014), pages 269 to 282
    locator: refinement types under lazy evaluation, and the use of termination to keep subtyping sound
  - paper: doi:10.1561/2500000032
    title: Ranjit Jhala and Niki Vazou, Refinement types, a tutorial, Foundations and Trends in Programming Languages 6(3-4), 2021, pages 159 to 317
    locator: the step-by-step development of a refinement type checker, the verification conditions it generates, and their decidability
---

A refinement type is an ordinary type together with a logical predicate on its values, such as $\{\nu : \mathsf{int} \mid \nu > 0\}$, the integers greater than zero. Subtyping between refinement types is logical implication, and the checker proves each implication with a decision procedure, usually an [SMT solver](/smt-problem/). The predicates come from a fixed logic that the solver decides, and a refined type always erases to an ordinary type. This is the difference from [dependent types](/dependent-types/), where any term can appear in a type and equality is checked by computation. [Liquid types](/liquid-types/) is a method to infer refinement types, and this page is about the type system and its checking. The name also covers an older idea, Freeman and Pfenning's refinements of a datatype into subsorts, such as non-empty lists; this page uses the predicate form, which is the common one today.

## In plain words

A normal type says "this is an integer". A refinement type can say "this is an integer that is not zero" or "this is an index that is smaller than the length of that array". You write such facts on the inputs and outputs of functions. The checker then makes sure that every call passes values that meet them. To do this, it collects what it knows at each point, for example that an `if` test was false, and asks a solver whether those facts imply the one that is needed. If the solver says yes, the call is safe. If it says no, the checker reports an error, often with an example value that breaks the rule. The checker stays automatic only because the facts are written in a logic that the solver can always decide.

## The idea

### Syntax

The base types are $B ::= \mathsf{int} \mid \mathsf{bool}$, and predicates $\varphi$ are formulas of a logic $\mathcal L$ over program variables and the special variable $\nu$, which stands for the value itself. A typical $\mathcal L$ is quantifier-free linear integer arithmetic with uninterpreted functions, such as $\mathsf{len}$. Types are

$$\tau ::= \{\nu : B \mid \varphi\} \mid x{:}\tau_1 \to \tau_2$$

The function type is *dependent*: the result type $\tau_2$ may mention the argument $x$. A plain $\mathsf{int}$ is $\{\nu : \mathsf{int} \mid \mathit{true}\}$. Programs are in A-normal form, so every argument of a call is a variable or a constant. Then substituting an argument into a predicate keeps the predicate in $\mathcal L$.

### Typing and subtyping rules

The context $\Gamma$ holds variable bindings and *guards*, the conditions of the `if` tests on the path to the current point. Its meaning $[\![\Gamma]\!]$ is the conjunction of $\varphi[x/\nu]$ for each binding $x : \{\nu : B \mid \varphi\}$ and of each guard.

```text
                                           Gamma(x) = {v : B | p}
--------------------------------  T-Const  -----------------------------------  T-Var
Gamma |- n : {v : int | v = n}             Gamma |- x : {v : B | p and v = x}

Gamma, x : t1 |- e : t2                          Gamma |- e : (x : t1 -> t2)    Gamma |- y : t1
---------------------------------  T-Abs         -------------------------------------------------  T-App
Gamma |- fun x -> e : x : t1 -> t2               Gamma |- e y : t2[y/x]

Gamma |- y : bool    Gamma, y |- e1 : t    Gamma, not y |- e2 : t
-----------------------------------------------------------------  T-If
Gamma |- if y then e1 else e2 : t

Gamma |- e : t1    Gamma |- t1 <: t2    t2 is well formed in Gamma
-----------------------------------------------------------------  T-Sub
Gamma |- e : t2

[[Gamma]] and p1 implies p2 is valid in L
------------------------------------------  S-Base
Gamma |- {v : B | p1} <: {v : B | p2}

Gamma |- s1 <: t1    Gamma, x : s1 |- t2 <: s2
-----------------------------------------------  S-Fun
Gamma |- (x : t1 -> t2) <: (x : s1 -> s2)
```

T-Var gives a variable the most precise type, "equal to $x$". T-If adds the test to the context of each branch, which makes the checker path-sensitive. S-Base is the only rule that consults the logic. S-Fun is the usual rule of [subtyping](/subtyping/), contravariant in the argument.

### Semantics and soundness

The semantics is the call-by-value semantics of the underlying language, with primitives that get stuck on bad input: $\mathit{div}\ n\ 0$ and an array read out of bounds have no step. The primitives get types that rule this out:

$$\mathit{div} : x{:}\mathsf{int} \to y{:}\{\nu : \mathsf{int} \mid \nu \neq 0\} \to \{\nu : \mathsf{int} \mid \mathit{true}\}$$

A refinement type denotes a set of values, $[\![\{\nu : B \mid \varphi\}]\!] = \{c \in B \mid \varphi[c/\nu] \text{ holds}\}$. Soundness is [progress and preservation](/type-soundness/). Preservation uses a substitution lemma for dependent function types: if $\Gamma, x : \tau_1 \vdash e : \tau_2$ and $\vdash v : \tau_1$, then $\Gamma[v/x] \vdash e[v/x] : \tau_2[v/x]$. Progress uses that the logic is sound for its model: if S-Base proved $\nu \neq 0$ for the second argument of $\mathit{div}$, then the value is not 0, so the call steps. A program that passes the checker never gets stuck on a primitive, so it never divides by zero and never reads outside an array.

### Checking and its decidability

With every function annotated, checking is syntax-directed when T-Sub is used only at fixed places (call arguments, function bodies against their annotation, and the two branches of an `if` against a common type). Each use of S-Base produces one *verification condition* $[\![\Gamma]\!] \wedge \varphi_1 \Rightarrow \varphi_2$, whose free variables are read as universally quantified. A formula is valid when its negation is unsatisfiable, so each condition is one query to an SMT solver. This is [verification condition generation](/verification-condition-generation/) driven by types.

**Theorem.** Checking annotated programs is decidable if and only if validity of quantifier-free formulas of $\mathcal L$ is decidable.

*Proof.* If validity is decidable, the checker makes one pass over the program and produces finitely many conditions. A-normal form keeps each of them in $\mathcal L$. It decides each one. Conversely, let $\varphi(x_1, \dots, x_k)$ be any quantifier-free formula of $\mathcal L$ over integer variables. The program `fun x1 -> ... -> fun xk -> true` checks against $x_1{:}\mathsf{int} \to \dots \to x_k{:}\mathsf{int} \to \{\nu : \mathsf{bool} \mid \varphi\}$ if and only if $\varphi$ is valid, since the only condition is $\nu = \mathit{true} \Rightarrow \varphi$ with $x_1, \dots, x_k$ unconstrained in the context, and $\nu$ does not occur in $\varphi$. So a checker for every program would decide validity in $\mathcal L$. $\square$

Linear integer arithmetic ([Presburger arithmetic](/presburger-arithmetic/)), equality with [uninterpreted functions](/euf-satisfiability/), the theory of arrays and their combination by [Nelson-Oppen](/nelson-oppen/) are decidable, which is why refinement languages use them. Integer arithmetic with multiplication of variables is not: validity of such formulas includes Hilbert's tenth problem, which is undecidable. A refinement checker that allows nonlinear predicates is therefore incomplete: the solver may answer "unknown" or time out, and the checker then rejects the program. Quantified predicates have the same problem.

*Inference* is a separate problem. Refinements for local variables can be read off by T-Var and T-If, but the refinement of a recursive function or a loop is an invariant, and finding one is as hard as [loop invariant synthesis](/loop-invariant-synthesis/). Liquid types restricts the search to conjunctions of given qualifiers, which makes inference decidable.

## Examples

**Safe division.** Check `fun a -> if a = 0 then 0 else div 100 a`. In the `else` branch, the guard $\neg(a = 0)$ is in $\Gamma$. T-Var gives `a` the type $\{\nu : \mathsf{int} \mid \nu = a\}$, and S-Base must show it is a subtype of $\{\nu \mid \nu \neq 0\}$:

$$\neg(a = 0) \wedge \nu = a \Rightarrow \nu \neq 0$$

This is valid. Without the test, the condition is $\nu = a \Rightarrow \nu \neq 0$, and the solver gives the counterexample $a = 0$.

**Absolute value.** Check `fun x -> if x < 0 then 0 - x else x` against $x{:}\mathsf{int} \to \{\nu : \mathsf{int} \mid \nu \geq 0 \wedge \nu \geq x\}$. The two branches give the conditions

$$x < 0 \wedge \nu = 0 - x \Rightarrow \nu \geq 0 \wedge \nu \geq x \qquad \neg(x < 0) \wedge \nu = x \Rightarrow \nu \geq 0 \wedge \nu \geq x$$

Both are valid in linear integer arithmetic.

**Array bounds.** Let $\mathit{get} : a{:}\mathsf{arr} \to i{:}\{\nu : \mathsf{int} \mid 0 \leq \nu \wedge \nu < \mathsf{len}\ a\} \to \mathsf{int}$, with $\mathsf{len}$ uninterpreted. In

```text
let rec sum (a : arr) (i : {v : int | 0 <= v}) (acc : int) : int =
  if i >= len a then acc else sum a (i + 1) (acc + get a i)
```

the call of `get` needs $0 \leq i \wedge \neg(i \geq \mathsf{len}\ a) \wedge \nu = i \Rightarrow 0 \leq \nu \wedge \nu < \mathsf{len}\ a$, and the recursive call needs $0 \leq i \wedge \nu = i + 1 \Rightarrow 0 \leq \nu$. Both are valid, so the bound check in `get` can be removed. This is the use that Xi and Pfenning (1998) measured.

**Where the logic stops.** The predicate $\nu = x \cdot y$ with both $x$ and $y$ variables is outside linear arithmetic. A checker over linear arithmetic either rejects it or treats $x \cdot y$ as an uninterpreted function, which loses facts such as $x \cdot y = y \cdot x$ unless they are added as axioms.

## Where it is used

- **Liquid Haskell** checks refinement types for Haskell with an SMT solver (Vazou et al. 2014). Under lazy evaluation, a binding may never be evaluated, so a false refinement on a diverging binding could prove anything. Liquid Haskell checks termination to keep subtyping sound.
- **F\*** combines dependent types with refinements and sends its conditions to Z3. **Flux** adds refinement types to Rust, using the ownership information that [borrow checking](/borrow-checking/) gives.
- **Dependent ML and ATS** use integer indices with linear constraints (Xi and Pfenning 1998, 1999), the same idea in the language of indexed types.
- **Datasort refinements** (Freeman and Pfenning 1991) refine a datatype into subsorts with a finite lattice, so their inference is a finite fixed point.
- **Run-time contracts.** Ada range subtypes and contract systems state the same predicates but check them when the program runs ([design by contract](/design-by-contract/)). A refinement checker proves them before.

## References
