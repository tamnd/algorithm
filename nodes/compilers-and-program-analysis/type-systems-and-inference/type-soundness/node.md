---
tag: ZB8M1Q
kind: theorem
slug: type-soundness
name: Type soundness
aliases:
- progress and preservation
- well-typed programs do not go wrong
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: A well-typed closed term never reaches a stuck state. For the simply typed lambda calculus it follows from progress (a value or a step) and preservation (a step keeps the type).
prereqs: [simply-typed-lambda-calculus]
see_also: [type-system, simply-typed-lambda-calculus, subtyping, system-f, value-restriction, hindley-milner-type-system, structural-induction, hoare-triple]
sources:
  - paper: doi:10.1006/inco.1994.1093
    title: Andrew K. Wright and Matthias Felleisen, A syntactic approach to type soundness, Information and Computation 115(1), 1994, pages 38 to 94
    locator: the syntactic method (soundness as subject reduction plus a progress lemma for a small-step semantics with stuck states), applied to ML with references, exceptions and continuations
  - paper: doi:10.1016/0022-0000(78)90014-4
    title: Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375
    locator: Section 3 (the semantic soundness theorem for a denotational semantics with the value "wrong")
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Section 8.3 (safety as progress plus preservation, Theorems 8.3.2 and 8.3.3), Section 9.3 (Lemma 9.3.1 inversion, Lemma 9.3.4 canonical forms, Theorem 9.3.5 progress, Lemmas 9.3.6 to 9.3.8 permutation, weakening and substitution, Theorem 9.3.9 preservation), Chapters 13 and 14 (references and exceptions)
  - paper: "Haskell B. Curry and Robert Feys, Combinatory Logic, Volume I, North-Holland, 1958"
    locator: the chapter on functionality (the subject reduction theorem for typed combinatory terms)
  - paper: "Nada Amin and Ross Tate, Java and Scala's type systems are unsound: the existential crisis of null pointers, OOPSLA 2016"
    locator: the counterexamples that combine null with path-dependent or wildcard types
---

Type soundness is the theorem that a well-typed program cannot reach a state that the semantics leaves undefined. Milner (1978) stated it as "well-typed expressions do not go wrong" for a denotational semantics. Wright and Felleisen (1994) gave the syntactic form that most papers now use: it splits soundness into *progress* and *preservation*, two lemmas proved by induction on typing derivations. This page states and proves the theorem for one system, the [simply typed lambda calculus](/simply-typed-lambda-calculus/) with call-by-value small steps. Other systems follow the same plan with more lemmas.

## Statement

The system is the one defined on the [simply typed lambda calculus](/simply-typed-lambda-calculus/) page: base types $\mathsf{Bool}$ and $\mathsf{Int}$, the arrow, conditionals and integer addition, with the typing rules T-Var, T-Abs, T-App, T-True, T-False, T-If, T-Int and T-Add, and the call-by-value small-step rules E-App1, E-App2, E-AppAbs, E-IfTrue, E-IfFalse, E-If, E-Add1, E-Add2 and E-AddInt. The values are the abstractions, $\mathsf{true}$, $\mathsf{false}$ and the integer literals. A closed term is **stuck** if it is not a value and no rule gives it a next step.

**Theorem (type soundness).** Let $t$ be a closed term.

1. **Progress.** If $\vdash t : T$, then $t$ is a value or there is a $t'$ with $t \to t'$.
2. **Preservation.** If $\Gamma \vdash t : T$ and $t \to t'$, then $\Gamma \vdash t' : T$.
3. **Safety.** If $\vdash t : T$ and $t \to^* t'$, then $t'$ is not stuck. If $t'$ is a value, then $\vdash t' : T$.

## In plain words

Think of the program as a machine that rewrites itself one small step at a time. It can fail in only one way: it reaches a point where the next operation gets the wrong kind of value, such as adding a truth value to a number. The theorem says that this never happens to a program that passes the type checker. The proof has two halves. The first says that a typed program is either finished or can make one more step. The second says that a step never changes the type. Put the two together, step by step, and the program stays typed and never gets stuck. Both halves depend on the exact rules for running the program, so the guarantee is only as strong as those rules.

## Proof

The [proof file](proofs/main.md) has the full proof. It uses four lemmas, in the order of Section 9.3 of Pierce's book.

1. **Inversion.** The rules are syntax directed, so the form of a typed term fixes the last rule of its derivation and the types of its parts. For example, if $\Gamma \vdash t_1\,t_2 : R$, then $\Gamma \vdash t_1 : T_{11} \to R$ and $\Gamma \vdash t_2 : T_{11}$ for some $T_{11}$.
2. **Canonical forms.** A closed value of type $\mathsf{Bool}$ is $\mathsf{true}$ or $\mathsf{false}$, a closed value of type $\mathsf{Int}$ is a literal, and a closed value of type $T_1 \to T_2$ is an abstraction $\lambda x{:}T_1.\,t$. This holds because the three kinds of values get three different kinds of types.
3. **Permutation and weakening.** Reordering the context, or adding a fresh variable to it, keeps every typing.
4. **Substitution.** If $\Gamma, x{:}S \vdash t : T$ and $\Gamma \vdash s : S$, then $\Gamma \vdash [x := s]\,t : T$.

**Progress** goes by induction on the derivation of $\vdash t : T$. T-Var cannot occur in the empty context. The value rules give values. For T-App, the induction hypothesis makes the function either step (E-App1) or a value, then the argument either step (E-App2) or a value, and in the last case canonical forms make the function an abstraction, so E-AppAbs applies. T-If and T-Add are the same, with canonical forms for $\mathsf{Bool}$ and $\mathsf{Int}$.

**Preservation** goes by induction on the derivation of $\Gamma \vdash t : T$, with a case for each step rule. The congruence rules (E-App1, E-App2, E-If, E-Add1, E-Add2) use the induction hypothesis on the part that steps. E-IfTrue, E-IfFalse and E-AddInt are direct. The one real case is E-AppAbs: inversion gives $\Gamma, x{:}T_{11} \vdash t_{12} : T$ and $\Gamma \vdash v_2 : T_{11}$, and the substitution lemma gives $\Gamma \vdash [x := v_2]\,t_{12} : T$.

**Safety** follows by induction on the number of steps: preservation keeps the type along $t \to^* t'$, and progress applied to $t'$ says it is a value or steps.

**Example of the E-AppAbs case.** The term $(\lambda x{:}\mathsf{Int}.\ x + 1)\ 4$ steps to $4 + 1$. Inversion on the typing of the redex gives $x{:}\mathsf{Int} \vdash x + 1 : \mathsf{Int}$, and $\vdash 4 : \mathsf{Int}$. The substitution lemma gives $\vdash 4 + 1 : \mathsf{Int}$. The trace of $\mathit{twice}\ \mathit{inc}\ 3$ on the [STLC page](/simply-typed-lambda-calculus/) has six steps, and each of the seven terms in it has type $\mathsf{Int}$.

## Consequences

- **Erasure of run-time checks.** A compiler for a sound language need not test the kind of a value before an operation. Canonical forms says the test would always pass.
- **Termination is separate.** Soundness says nothing about termination. In the STLC every run ends, by strong normalization (see the [STLC page](/simply-typed-lambda-calculus/)), so a closed term of type $T$ ends in a value of type $T$. With a fixed-point operator, a well-typed term may run forever, and soundness still holds, because an infinite run never gets stuck.
- **Other systems.** The same plan proves soundness for many richer systems, each with extra lemmas.
  - [Subtyping](/subtyping/): preservation may lower the type to a subtype, and canonical forms needs inversion lemmas for the subtype relation (Pierce, Chapter 15).
  - [System F](/system-f/) and [Hindley-Milner](/hindley-milner-type-system/): a lemma on type substitution, $[\alpha := S]$, handles type application and instantiation.
  - References: the typing judgment gets a store typing $\Sigma$, and preservation says the new store typing extends the old one (Pierce, Chapter 13). With let-polymorphism, references break preservation unless generalization is restricted, which is the [value restriction](/value-restriction/).
  - Exceptions: progress allows a third outcome, an uncaught exception (Pierce, Chapter 14).
  - [Recursive types](/recursive-types/): canonical forms for $\mu$ types needs fold and unfold, or a coinductive type equality.
- **Mechanized proofs.** Because the proof is a set of inductions on derivations, it is a standard benchmark for proof assistants, and full languages have mechanized soundness proofs, for example the definition of Standard ML in Twelf and the WebAssembly specification.
- **A link to program logic.** Soundness says that the type of a term is an invariant of its run. Program logics such as the [Hoare triple](/hoare-triple/) prove invariants that the programmer chooses. A type system proves one fixed, weak invariant for all programs, and it does so without help.

## Tightness

**Soundness depends on the semantics and on the meaning of "stuck".** Add integer division $t_1 / t_2$ with a rule T-Div that gives $\mathsf{Int}$, and a step rule E-DivInt for $n_1 / n_2$ only when $n_2 \neq 0$. Then $1 / 0$ has type $\mathsf{Int}$, it is not a value, and no rule steps it. A script with a stepper for this extension confirms that $1/0$ is stuck. So progress fails. There are two standard repairs. One adds a rule $n / 0 \to \mathsf{error}$ and lets progress allow the outcome $\mathsf{error}$, as with exceptions. The other leaves the term stuck and accepts that the theorem no longer covers it. Most real languages take the first repair, so a sound language can still fail at run time, with a defined error. The theorem rules out only the failures that the chosen semantics calls stuck.

**Progress needs closed terms.** The term $x$ has type $\mathsf{Int}$ in the context $x{:}\mathsf{Int}$, but it is not a value and does not step.

**A sound system rejects safe programs.** The term $\mathsf{if\ true\ then}\ 1\ \mathsf{else\ false}$ steps to the value $1$ in one step and never gets stuck. But it has no type, because T-If needs both branches to have the same type. No sound and decidable type system for a Turing-complete language can accept exactly the safe programs (see [type system](/type-system/)). The same example shows that the converse of preservation, *subject expansion*, fails: $1$ has type $\mathsf{Int}$, but the term that stepped to it has no type.

**Each rule matters.** If T-If did not require $t_1 : \mathsf{Bool}$, the stuck term $\mathsf{if}\ 0\ \mathsf{then}\ 1\ \mathsf{else}\ 2$ would be typed, and progress would fail. If let-bound references were generalized without the value restriction, preservation would fail. Real languages have had soundness bugs of this kind. Amin and Tate (2016) gave Java and Scala programs that pass the type checker and then fail with a cast error where none was written, by combining `null` with wildcard or path-dependent types.

## History

Curry and Feys (1958) proved the *subject reduction* theorem for typed combinatory logic: reduction keeps the type. Milner (1978) proved the first soundness theorem for a programming language with polymorphism. He gave a denotational semantics in which ill-typed operations produce a special value *wrong*, and he proved that the meaning of a well-typed expression is never *wrong*. That style needs a domain-theoretic model, and it is hard to extend to references and control. Wright and Felleisen (1994) replaced it with the syntactic method: a small-step semantics where errors are stuck terms, subject reduction for each step, and a separate lemma that typed terms are not stuck. They applied it to ML with references, exceptions and continuations. Pierce's book named the two lemmas progress and preservation and made this the standard form.

## References
