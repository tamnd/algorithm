---
tag: 04XM6K
kind: concept
slug: dependent-types
name: Dependent types
aliases:
- dependent type theory
- pi types
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Types that depend on values, such as vectors of length n, so that types can state and check full program specifications.
prereqs: [simply-typed-lambda-calculus, system-f, curry-howard-correspondence]
see_also: [refinement-types, bidirectional-type-checking, church-rosser-theorem, weak-normalization, reducibility-method, halting-problem, unification-problem, verified-compilation]
sources:
  - book: isbn:9788870881059
    title: Per Martin-Löf, Intuitionistic Type Theory (notes by Giovanni Sambin of a series of lectures given in Padua, June 1980), Bibliopolis, Naples, 1984, Studies in Proof Theory 1
    locator: the forms of judgment, including definitional equality, and the rules for the cartesian product of a family of sets and the disjoint union of a family of sets
  - paper: doi:10.1016/0890-5401(88)90005-3
    title: Thierry Coquand and Gérard Huet, The calculus of constructions, Information and Computation 76(2-3), 1988, pages 95 to 120
    locator: the calculus with dependent products over terms and types, and its strong normalization proof
  - book: isbn:9780262162289
    title: Benjamin C. Pierce (ed.), Advanced Topics in Types and Programming Languages, MIT Press, 2005
    locator: Chapter 2 (David Aspinall and Martin Hofmann, Dependent types), the conversion rule, algorithmic typing and the role of normalization in deciding it
  - paper: doi:10.1145/512644.512671
    title: Albert R. Meyer and Mark B. Reinhold, "Type" is not a type, Thirteenth ACM Symposium on Principles of Programming Languages (POPL 1986), pages 287 to 295
    locator: the results on a typed lambda calculus with a type of all types
  - paper: doi:10.1145/292540.292560
    title: Hongwei Xi and Frank Pfenning, Dependent types in practical programming, Twenty-Sixth ACM Symposium on Principles of Programming Languages (POPL 1999), pages 214 to 227
    locator: indexed types over a separate, decidable constraint domain, as opposed to full dependent types
---

A dependent type is a type that contains a term. The type $\mathsf{Vec}\ A\ n$ of lists of length exactly $n$ depends on the number $n$, and the function type $\Pi(x{:}A).\ B$ has a result type $B$ that may mention the argument $x$. With dependent types, a type can state a full specification, and by the [Curry-Howard correspondence](/curry-howard-correspondence/) a term of that type is a proof of it. This page is about full dependent types as in Martin-Löf type theory and the calculus of constructions. It differs from [System F](/system-f/), where types depend on types and not on terms, and from [refinement types](/refinement-types/), which attach predicates from a fixed logic to ordinary types and check them with a decision procedure. Indexed types such as those of Dependent ML lie between the two: the indices come from a separate decidable domain.

## In plain words

In most languages, a type is a fixed label such as "list of integers". A dependent type can mention a value. "A list of exactly 3 integers" is a type, and so is "a list whose length is n", where n is a variable of the program. A function can then promise, in its type, that it takes a list of length n and returns a list of the same length, or that it returns a sorted list. To check such types, the checker must sometimes run part of the program at compile time, for example to see that "2 + 1" and "3" are the same length. That is why the language must make sure that this computation always ends: if it could loop, the checker could loop too.

## The idea

### Syntax

In a dependent type theory, types and terms share one syntax. A minimal system has a universe $\mathcal U$ (the type of small types), dependent functions, and the natural numbers:

$$t, A, B ::= x \mid \mathcal U \mid \Pi(x{:}A).\ B \mid \lambda x{:}A.\ t \mid t\ u \mid \mathsf{Nat} \mid \mathsf{zero} \mid \mathsf{succ}\ t \mid \mathsf{natrec}\ P\ z\ s\ t$$

When $x$ does not occur in $B$, $\Pi(x{:}A).\ B$ is the ordinary function type $A \to B$. The *dependent pair* $\Sigma(x{:}A).\ B$, whose second component has a type that depends on the first, is added in the same way.

### Judgments and rules

There are two judgments: $\Gamma \vdash t : A$ (typing) and $\Gamma \vdash t \equiv u : A$ (*definitional equality*). In the text blocks, `(x : A) -> B` is $\Pi(x{:}A).\ B$ and `B[u/x]` is substitution.

```text
(x : A) in Gamma                Gamma |- A : U    Gamma, x : A |- B : U
-----------------  T-Var        ----------------------------------------  T-Pi
Gamma |- x : A                  Gamma |- (x : A) -> B : U

Gamma, x : A |- t : B
------------------------------------------  T-Abs
Gamma |- fun (x : A) -> t : (x : A) -> B

Gamma |- t : (x : A) -> B    Gamma |- u : A
--------------------------------------------  T-App
Gamma |- t u : B[u/x]

Gamma |- t : A    Gamma |- A == B : U
--------------------------------------  T-Conv
Gamma |- t : B
```

The rules for $\mathsf{Nat}$ give $\mathsf{Nat} : \mathcal U$, $\mathsf{zero} : \mathsf{Nat}$, $\mathsf{succ} : \mathsf{Nat} \to \mathsf{Nat}$, and the eliminator, which is both recursion and induction:

```text
Gamma, n : Nat |- P : U    Gamma |- z : P[zero/n]
Gamma |- s : (k : Nat) -> P[k/n] -> P[succ k/n]    Gamma |- m : Nat
--------------------------------------------------------------------  T-NatRec
Gamma |- natrec P z s m : P[m/n]
```

Definitional equality is the least congruence (closed under all term formers, and an equivalence) that contains the computation rules

$$(\lambda x{:}A.\ t)\ u \equiv t[u/x] \quad (\beta) \qquad \mathsf{natrec}\ P\ z\ s\ \mathsf{zero} \equiv z \qquad \mathsf{natrec}\ P\ z\ s\ (\mathsf{succ}\ m) \equiv s\ m\ (\mathsf{natrec}\ P\ z\ s\ m)$$

and often the $\eta$ rule for functions. T-App is where dependency enters: the type of the result is $B$ with the actual argument put in. T-Conv is where computation enters: a term of type $A$ also has every type that is definitionally equal to $A$.

The *calculus of constructions* (Coquand and Huet 1988) uses the same rules with a second sort, so that $\Pi$ can range over types as well as terms. It contains System F and simple dependent types as fragments.

### Semantics and soundness

The operational semantics is [beta reduction](/beta-reduction/) and the $\mathsf{natrec}$ rules, read from left to right as steps $t \longrightarrow t'$. Soundness is [progress and preservation](/type-soundness/). *Preservation* (often called subject reduction here): if $\Gamma \vdash t : A$ and $t \longrightarrow t'$, then $\Gamma \vdash t' : A$. Its proof needs the substitution lemma and *injectivity of* $\Pi$: if $\Pi(x{:}A).\ B \equiv \Pi(x{:}A').\ B'$, then $A \equiv A'$ and $B \equiv B'$. Injectivity follows from confluence of reduction ([Church-Rosser](/church-rosser-theorem/)), because two terms are definitionally equal exactly when they reduce to a common term, and a $\Pi$ only reduces to a $\Pi$. *Progress*: a closed well-typed term is a value (a $\lambda$, $\mathsf{zero}$, $\mathsf{succ}$ of a term, or a type former) or takes a step, by canonical forms.

For a type theory used as a logic, a stronger property matters: *normalization*. Every well-typed term reduces to a normal form. Coquand and Huet proved strong normalization for the calculus of constructions with the [reducibility method](/reducibility-method/). Normalization gives *consistency*: the empty type has no closed normal term, so no closed term at all.

### Type checking needs definitional equality

The rules above are not syntax-directed, because T-Conv applies to any term. The usual algorithm is [bidirectional](/bidirectional-type-checking/): it infers a type for variables and applications, checks abstractions against a given $\Pi$ type, and uses T-Conv only where an inferred type meets an expected one. So type checking reduces to one question, asked many times: is $A \equiv B$?

**Theorem.** If reduction is confluent and every well-typed term has a normal form that can be computed, then $A \equiv B$ is decidable for well-typed $A$ and $B$, and so type checking of annotated terms is decidable.

*Proof sketch.* By confluence, $A \equiv B$ holds if and only if $A$ and $B$ have a common reduct, and so if and only if their normal forms are the same up to renaming of bound variables. Normal forms can be computed: with strong normalization, any reduction order reaches the normal form; with [weak normalization](/weak-normalization/) of $\beta$, leftmost-outermost order does. So the checker normalizes both sides and compares them. The rest of the algorithm recurses on the structure of the term, and each recursive call is on a smaller term. Its completeness for the declarative rules uses subject reduction and injectivity of $\Pi$. $\square$

Normalization is not a detail. If definitional equality may unfold unrestricted recursion, type checking is undecidable. Take a function `f : Unit -> Nat` with general recursion that searches for a halting step of a Turing machine $M$ and returns 0 when it finds one. The term `refl : Id Nat (f ()) 0` is well typed if and only if `f ()` reduces to `0`, that is, if and only if $M$ halts, so a type checker would solve the [halting problem](/halting-problem/). The same happens with the rule $\mathcal U : \mathcal U$: Girard's paradox gives a well-typed term with no normal form, and Meyer and Reinhold (1986) showed that type checking with $\mathcal U : \mathcal U$ is undecidable. Practical languages that allow general recursion keep checking decidable by not unfolding such definitions during conversion: Lean treats a `partial def` as opaque, and F* does not reduce code in its divergence effect. The part of the language that the checker computes with must be normalizing.

*Inference* is harder than checking. Filling in a missing argument or annotation means solving equations between terms that contain unknown functions, which is higher-order unification and is undecidable in general. Proof assistants solve the decidable cases, such as Miller's pattern fragment, and ask the user for the rest (see the [unification problem](/unification-problem/) for the first-order case).

## Examples

**Vectors.** Let $\mathsf{Vec} : \mathcal U \to \mathsf{Nat} \to \mathcal U$ with

$$\mathsf{nil} : \Pi(A{:}\mathcal U).\ \mathsf{Vec}\ A\ \mathsf{zero} \qquad \mathsf{cons} : \Pi(A{:}\mathcal U).\ \Pi(n{:}\mathsf{Nat}).\ A \to \mathsf{Vec}\ A\ n \to \mathsf{Vec}\ A\ (\mathsf{succ}\ n)$$

Then $\mathsf{head} : \Pi(A{:}\mathcal U).\ \Pi(n{:}\mathsf{Nat}).\ \mathsf{Vec}\ A\ (\mathsf{succ}\ n) \to A$ needs no case for the empty vector: $\mathsf{nil}$ has type $\mathsf{Vec}\ A\ \mathsf{zero}$, and $\mathsf{zero} \not\equiv \mathsf{succ}\ n$. The run-time error of `head []` becomes a type error.

**Conversion at work.** Define $+$ by recursion on its first argument, so $\mathsf{zero} + n \equiv n$ and $\mathsf{succ}\ m + n \equiv \mathsf{succ}\ (m + n)$. A term $v : \mathsf{Vec}\ \mathsf{Nat}\ 3$ can be passed to a function that expects $\mathsf{Vec}\ \mathsf{Nat}\ (2 + 1)$: the checker reduces $2 + 1$ to $3$ and T-Conv applies. For `append : Vec A m -> Vec A n -> Vec A (m + n)`, the clause `append nil ys = ys` checks because $\mathsf{zero} + n \equiv n$.

**Definitional against propositional equality.** The type $\mathsf{Vec}\ A\ (m + \mathsf{zero})$ is *not* definitionally equal to $\mathsf{Vec}\ A\ m$ when $m$ is a variable: $+$ recurses on its first argument, which is stuck. The equation $m + \mathsf{zero} = m$ is true for every $m$, but only *propositionally*: it has a proof by induction, a term $p : \Pi(m{:}\mathsf{Nat}).\ \mathsf{Id}\ \mathsf{Nat}\ (m + \mathsf{zero})\ m$ built with $\mathsf{natrec}$. To use a vector of length $m + \mathsf{zero}$ as one of length $m$, the program must *transport* it along $p\ m$. Definitional equality is what the checker decides by itself. Propositional equality is what the programmer proves.

**Specifications as types.** The type $\Pi(\ell{:}\mathsf{List}\ \mathsf{Nat}).\ \Sigma(\ell'{:}\mathsf{List}\ \mathsf{Nat}).\ \mathsf{Sorted}\ \ell' \times \mathsf{Perm}\ \ell\ \ell'$ is the type of correct sorting functions. A term of this type is a sorting function together with a proof that its output is a sorted permutation of its input.

## Where it is used

- **Proof assistants.** Coq (now Rocq) is based on the calculus of inductive constructions, Agda and Idris on Martin-Löf type theory, and Lean on a variant of the calculus of constructions. They are used for mathematics and for [verified compilers](/verified-compilation/), such as CompCert, written and proved in Coq.
- **Programming.** Idris and Agda are used as programming languages with dependent types. F* combines dependent types with an SMT solver that discharges many proof obligations, close to [refinement types](/refinement-types/).
- **Restricted forms.** Dependent ML (Xi and Pfenning 1999) and ATS index types by integer expressions and check the constraints with a decision procedure, so type checking never runs program code. Haskell's GADTs and type families give a similar effect with type-level data.
- **Quantities.** Idris 2 adds use counts to dependent types, so that a variable used only in types is erased at run time, and others can be [linear](/linear-types/).

## References
