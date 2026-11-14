---
tag: Z1D969
kind: model
slug: simply-typed-lambda-calculus
name: Simply typed lambda calculus
aliases:
- STLC
- Church's simple theory of types
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: The lambda calculus with base types and function types; each well-typed term has a unique type, evaluation never gets stuck, and every reduction sequence terminates.
prereqs: [lambda-calculus, type-system]
see_also: [type-soundness, curry-howard-correspondence, type-checking-problem, type-inference-problem, system-f, reducibility-method, hindley-milner-type-system, combinatory-logic]
sources:
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 9 (the rules T-Var, T-Abs, T-App, E-App1, E-App2, E-AppAbs; Lemma 9.3.1 inversion, Theorem 9.3.3 uniqueness of types, Lemma 9.3.4 canonical forms, Theorems 9.3.5 and 9.3.9 progress and preservation) and Chapter 12 (normalization)
  - paper: doi:10.2307/2266170
    title: Alonzo Church, A formulation of the simple theory of types, Journal of Symbolic Logic 5(2), 1940, pages 56 to 68
    locator: the whole paper (the simple types built from base types by the function type, with lambda abstraction carrying the type of its variable)
  - paper: doi:10.2307/2271658
    title: William W. Tait, Intensional interpretations of functionals of finite type I, Journal of Symbolic Logic 32(2), 1967, pages 198 to 212
    locator: the convertibility (computability) predicate and the normalization proof for terms of finite type
  - book: isbn:9780521371810
    title: Jean-Yves Girard, Yves Lafont and Paul Taylor, Proofs and Types, Cambridge University Press, 1989
    locator: Chapter 3 (the simply typed calculus), Chapter 4 (weak normalization) and Chapter 6 (strong normalization by reducibility, the conditions CR1 to CR3)
  - paper: doi:10.1016/0304-3975(79)90006-9
    title: Richard Statman, Intuitionistic propositional logic is polynomial-space complete, Theoretical Computer Science 9(1), 1979, pages 67 to 72
    locator: the main theorem and its corollary that inhabitation of simple types is PSPACE-complete
  - paper: doi:10.1016/0304-3975(79)90007-0
    title: Richard Statman, The typed lambda-calculus is not elementary recursive, Theoretical Computer Science 9(1), 1979, pages 73 to 81
    locator: the main theorem (beta-convertibility of closed simply typed terms is not elementary recursive)
  - paper: "Helmut Schwichtenberg, Definierbare Funktionen im Lambda-Kalkul mit Typen, Archiv fur mathematische Logik und Grundlagenforschung 17 (1976), 113 to 114"
    locator: the characterization of the functions definable on Church numerals as the extended polynomials
  - book: isbn:9780521465182
    title: J. Roger Hindley, Basic Simple Type Theory, Cambridge University Press, 1997
    locator: Chapter 2 (Curry-style typing) and Chapter 3 (principal types and the principal type algorithm)
---

The simply typed lambda calculus (STLC) is the [lambda calculus](/lambda-calculus/) in which each bound variable has a type built from base types with the arrow $\to$. Church introduced it in 1940 as a logic that avoids the paradoxes of the untyped system. It is the smallest useful [type system](/type-system/) with functions, and most typed languages start from it. Its type checks run in linear time, its well-typed terms never get stuck, and every reduction of a well-typed term terminates. That last property also means it cannot express every computable function.

## The machine

The STLC is a model of programs, not a machine model. A "run" is a sequence of small steps on a term. The version below has two base types, Booleans and integers, and call-by-value evaluation, as in Chapter 9 of Pierce's book with integers added.

### Syntax

$$
\begin{aligned}
T &::= \mathsf{Bool} \mid \mathsf{Int} \mid T \to T \\
t &::= x \mid \lambda x{:}T.\,t \mid t\ t \mid \mathsf{true} \mid \mathsf{false} \mid \mathsf{if}\ t\ \mathsf{then}\ t\ \mathsf{else}\ t \mid n \mid t + t \\
v &::= \lambda x{:}T.\,t \mid \mathsf{true} \mid \mathsf{false} \mid n
\end{aligned}
$$

Here $n$ ranges over the integer literals. The arrow associates to the right: $\mathsf{Int} \to \mathsf{Int} \to \mathsf{Int}$ is $\mathsf{Int} \to (\mathsf{Int} \to \mathsf{Int})$. Application associates to the left. Terms are equal up to the renaming of bound variables. In the surface syntax of this site, $\lambda x{:}T.\,t$ is written `fun x:T -> t`.

### Typing

A context $\Gamma$ is a list $x_1{:}T_1, \dots, x_k{:}T_k$ of distinct variables with types. The judgment $\Gamma \vdash t : T$ is the smallest relation closed under these rules.

```text
x:T in Gamma               Gamma, x:T1 |- t2 : T2               Gamma |- t1 : T11 -> T12    Gamma |- t2 : T11
-------------  T-Var       ---------------------------  T-Abs   ---------------------------------------------  T-App
Gamma |- x : T             Gamma |- \x:T1. t2 : T1 -> T2         Gamma |- t1 t2 : T12

---------------------  T-True      ----------------------  T-False      -----------------  T-Int
Gamma |- true : Bool               Gamma |- false : Bool                Gamma |- n : Int

Gamma |- t1 : Bool    Gamma |- t2 : T    Gamma |- t3 : T          Gamma |- t1 : Int    Gamma |- t2 : Int
------------------------------------------------------  T-If     ---------------------------------------  T-Add
Gamma |- if t1 then t2 else t3 : T                                Gamma |- t1 + t2 : Int
```

The rules are syntax directed: for each form of term, exactly one rule can end a derivation. This gives the inversion lemma (Pierce, Lemma 9.3.1): if $\Gamma \vdash t_1\,t_2 : R$, then $\Gamma \vdash t_1 : T_{11} \to R$ and $\Gamma \vdash t_2 : T_{11}$ for some $T_{11}$, and the same for each other form.

### Evaluation

The call-by-value small-step relation $t \to t'$ has these rules.

```text
t1 --> t1'                     t2 --> t2'
-----------------  E-App1      -----------------  E-App2      ---------------------------------  E-AppAbs
t1 t2 --> t1' t2               v1 t2 --> v1 t2'               (\x:T. t) v2 --> [x := v2] t

-----------------------------------  E-IfTrue     ------------------------------------  E-IfFalse
if true then t2 else t3 --> t2                    if false then t2 else t3 --> t3

t1 --> t1'
-----------------------------------------------------  E-If
if t1 then t2 else t3 --> if t1' then t2 else t3

t1 --> t1'                     t2 --> t2'                     n = n1 + n2
-------------------  E-Add1    -------------------  E-Add2    --------------  E-AddInt
t1 + t2 --> t1' + t2           v1 + t2 --> v1 + t2'           n1 + n2 --> n
```

$[x := v]t$ is capture-avoiding substitution. The relation is deterministic: each term has at most one next step. A closed term $t$ is *stuck* if it is not a value and has no next step, for example $\mathsf{true} + 1$ or $3\ 4$. Evaluation does not go under $\lambda$, so a $\lambda$ is a value even if its body has a redex.

### Church style and Curry style

The calculus above is *Church style*: each $\lambda$ carries the type of its variable. In the *Curry-style* version, terms are untyped ($\lambda x.\,t$), and T-Abs may choose any $T_1$. A Curry-style term then has many types: $\lambda x.\,x$ has $\mathsf{Int} \to \mathsf{Int}$, $\mathsf{Bool} \to \mathsf{Bool}$ and every $T \to T$. Hindley (1969) showed that each typable Curry-style term has a *principal type* with type variables, here $\alpha \to \alpha$, of which every other type is an instance. The two styles have the same typable terms after erasure of the annotations, and they behave the same under evaluation.

### A worked derivation and run

Let $\mathit{twice} = \lambda f{:}\mathsf{Int}{\to}\mathsf{Int}.\ \lambda x{:}\mathsf{Int}.\ f\ (f\ x)$ and $\mathit{inc} = \lambda y{:}\mathsf{Int}.\ y + 1$. Write $\Gamma = f{:}\mathsf{Int}{\to}\mathsf{Int}, x{:}\mathsf{Int}$. The derivation of the type of $\mathit{twice}$ is:

```text
                         Gamma |- f : Int->Int (T-Var)   Gamma |- x : Int (T-Var)
                         --------------------------------------------------- T-App
Gamma |- f : Int->Int    Gamma |- f x : Int
------------------------------------------- T-App
Gamma |- f (f x) : Int
------------------------------------------- T-Abs
f:Int->Int |- \x:Int. f (f x) : Int -> Int
------------------------------------------- T-Abs
|- twice : (Int -> Int) -> Int -> Int
```

Then T-App twice gives $\vdash \mathit{twice}\ \mathit{inc}\ 3 : \mathsf{Int}$. The run takes six steps, and a script with a checker and a stepper for this calculus gives the same type and the same trace.

| step | term | rule |
|---|---|---|
| 0 | $\mathit{twice}\ \mathit{inc}\ 3$ | |
| 1 | $(\lambda x{:}\mathsf{Int}.\ \mathit{inc}\ (\mathit{inc}\ x))\ 3$ | E-App1 with E-AppAbs |
| 2 | $\mathit{inc}\ (\mathit{inc}\ 3)$ | E-AppAbs |
| 3 | $\mathit{inc}\ (3 + 1)$ | E-App2 with E-AppAbs |
| 4 | $\mathit{inc}\ 4$ | E-App2 with E-AddInt |
| 5 | $4 + 1$ | E-AppAbs |
| 6 | $5$ | E-AddInt |

Each term in the trace has type $\mathsf{Int}$, which is what preservation says.

## What it counts

The cost measures are the ones of the untyped [lambda calculus](/lambda-calculus/): the number of reduction steps under a chosen strategy, and the size of terms, counted as nodes of the syntax tree. Two facts make the typed setting different.

- **Every run ends.** The number of steps is finite for every strategy (strong normalization, below). So the STLC computes only total functions, and it is not Turing complete.
- **Runs can still be very long.** Let $\underline{2} = \lambda f.\lambda x.\,f\,(f\,x)$ in Curry style, and let $E_k = \underline{2}\ \underline{2} \cdots \underline{2}$ with $k$ copies, applied to the left. Each copy is typed with its own instance of $(\alpha \to \alpha) \to \alpha \to \alpha$, and $E_k$ itself has the principal type $(\alpha \to \alpha) \to \alpha \to \alpha$ for $k = 1$ to $5$ (checked by a script with unification). Since $\underline{m}\ \underline{n} = \underline{n^m}$, $E_k$ normalizes to the numeral for the tower $2^{2^{\cdot^{\cdot^{2}}}}$ of height $k$: the script gives 2, 4, 16 and 65536 for $k = 1$ to $4$. $E_4$ has 31 nodes, and its normal form has $2 \cdot 65536 + 3 = 131075$ nodes. The growth in $k$ is faster than any fixed tower of exponentials, which is the root of Statman's lower bound below.

For the type checker, the measure is the size $n$ of the term with its annotations, and the cost model is a word RAM.

## Relation to other models

- **Untyped lambda calculus.** Erasing the annotations maps each STLC term to an untyped term with the same reductions. The image is a proper subset: $\lambda x.\,x\,x$ and the fixed-point combinators have no simple type.
- **Combinatory logic.** The typed combinators $K : A \to B \to A$ and $S : (A \to B \to C) \to (A \to B) \to A \to C$ generate exactly the simply typed terms up to translation ([combinatory logic](/combinatory-logic/)). Their types are the axioms of the Hilbert system for implication.
- **Logic.** By the [Curry-Howard correspondence](/curry-howard-correspondence/), simple types are formulas of intuitionistic implicational logic, terms are natural deduction proofs, and normalization is the removal of detours in proofs.
- **Extensions.** Adding a fixed-point operator $\mathsf{fix}$ gives PCF, which is Turing complete and loses termination. Adding natural numbers with primitive recursion at all types gives Gödel's System T. Adding $\forall$ over types gives [System F](/system-f/). Adding polymorphism only at `let` gives [Hindley-Milner](/hindley-milner-type-system/). Adding [subtyping](/subtyping/) or [recursive types](/recursive-types/) gives the systems on those pages.
- **Categories.** Lambek showed that the STLC with products is the internal language of cartesian closed categories.

## Known results in the model

**Uniqueness of types.** In Church style, if $\Gamma \vdash t : T$ and $\Gamma \vdash t : T'$, then $T = T'$ (Pierce, Theorem 9.3.3). *Proof.* Induction on $t$. A variable has the one type that $\Gamma$ gives it. For $\lambda x{:}T_1.\,t_2$, inversion gives $T = T_1 \to T_2$ and $T' = T_1 \to T_2'$ with both $T_2$ and $T_2'$ types of $t_2$ under $\Gamma, x{:}T_1$, so $T_2 = T_2'$ by induction. For $t_1\,t_2$, inversion gives $t_1 : T_{11} \to T$ and $t_1 : T_{11}' \to T'$, so by induction the two arrow types are equal and $T = T'$. The other forms are similar.

**Type soundness.** If $\vdash t : T$, then $t$ never reaches a stuck term: each closed well-typed term is a value or steps (progress), and a step keeps the type (preservation). The full proof, with the lemmas for inversion, canonical forms and substitution, is on the [type soundness](/type-soundness/) page.

**Strong normalization (Tait 1967).** If $\Gamma \vdash t : T$, then there is no infinite sequence of full beta reductions $t \to_\beta t_1 \to_\beta t_2 \to_\beta \cdots$, where a step may contract any redex, also under $\lambda$. This is a strong form of termination: every strategy ends, not only call by value. We give a sketch here. The full proof is on the [reducibility method](/reducibility-method/) page and in Chapter 6 of Girard, Lafont and Taylor. *Sketch.* Define a set $\mathrm{RED}_T$ of terms for each type: $\mathrm{RED}_B$ is the set of strongly normalizing terms of base type $B$, and $t \in \mathrm{RED}_{A \to B}$ if $t\,u \in \mathrm{RED}_B$ for every $u \in \mathrm{RED}_A$. Prove by induction on $T$ the three conditions CR1 (every term in $\mathrm{RED}_T$ is strongly normalizing), CR2 (the set is closed under reduction), and CR3 (a neutral term, that is a term not of the form $\lambda x.t$, whose one-step reducts are all in $\mathrm{RED}_T$ is in $\mathrm{RED}_T$; so variables are in it). Then prove by induction on the typing derivation that if $x_1{:}A_1, \dots, x_k{:}A_k \vdash t : T$ and $u_i \in \mathrm{RED}_{A_i}$, then $t[x_1 := u_1, \dots, x_k := u_k] \in \mathrm{RED}_T$. Taking $u_i = x_i$ and CR1 gives the theorem. The induction on types is what fails for the untyped calculus: there is no type to induct on. Weak normalization, that one strategy always ends, has a simpler proof by a measure on the redexes ([weak normalization](/weak-normalization/)).

**Confluence.** Typed beta reduction is confluent, as a restriction of the untyped calculus ([Church-Rosser theorem](/church-rosser-theorem/)). With strong normalization, each term has exactly one normal form, and beta equality is decidable: normalize both terms and compare.

**Type checking is linear.** Church-style checking of $\Gamma \vdash t : T$ runs in $O(n)$ time on a word RAM, by a reduction to [Paterson-Wegman unification](/paterson-wegman-unification/) or, in expected time, by one bottom-up pass with [hash-consed](/hash-consing/) types. Naive tree comparison of types gives $\Theta(n^2)$ in the worst case. Details are on the [type checking problem](/type-checking-problem/) page.

**Typability is linear.** For Curry-style terms, typability and the principal type come from constraint generation and [first-order unification](/unification-problem/), in $O(n)$ time with a DAG representation. Written out as a tree, the principal type can be exponentially larger than the term. See the [type inference problem](/type-inference-problem/).

**Inhabitation is PSPACE-complete (Statman 1979).** The question "is there a closed term of type $T$?" is PSPACE-complete in the size of $T$. Under Curry-Howard it is provability in intuitionistic implicational logic. For example, $(\alpha \to \beta) \to (\beta \to \gamma) \to \alpha \to \gamma$ is inhabited, but Peirce's law $((\alpha \to \beta) \to \alpha) \to \alpha$ is not (see the [Curry-Howard correspondence](/curry-howard-correspondence/)).

**Beta equality is not elementary (Statman 1979).** Deciding whether two closed terms have the same normal form is decidable, but no algorithm runs in time bounded by a fixed tower of exponentials $2^{2^{\cdot^{\cdot^{n}}}}$. The term family $E_k$ above shows why normalization alone cannot be faster.

**Expressive power (Schwichtenberg 1976).** The functions $\mathbb{N}^k \to \mathbb{N}$ that closed terms of type $\mathsf{N}_\alpha \to \dots \to \mathsf{N}_\alpha$ compute on Church numerals, with $\mathsf{N}_\alpha = (\alpha \to \alpha) \to \alpha \to \alpha$, are exactly the *extended polynomials*: the functions built from constants, projections, addition, multiplication and the test "if $x = 0$ then $y$ else $z$". So even subtraction by one is not definable at this fixed type. More functions become definable if the input type may differ from the output type.

## References
