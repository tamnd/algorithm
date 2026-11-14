---
tag: W7DCCA
kind: definition
slug: value-restriction
name: Value restriction
aliases:
- Wright's value restriction
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Generalize the type of a let binding only when its right side is a syntactic value, which keeps polymorphism sound with mutable references.
prereqs: [hindley-milner-type-system, type-soundness]
see_also: [let-polymorphism, algorithm-w, principal-type-theorem, effect-system, type-classes]
sources:
  - paper: doi:10.1007/BF01018828
    title: Andrew K. Wright, Simple imperative polymorphism, LISP and Symbolic Computation 8(4), 1995, pages 343 to 355
    locator: the definition of the value restriction, its soundness proof for ML with references, and the study of how often it rejects existing programs
  - paper: doi:10.1016/0890-5401(90)90018-D
    title: Mads Tofte, Type inference for polymorphic references, Information and Computation 89(1), 1990, pages 1 to 34
    locator: the counterexample with a polymorphic reference cell, and imperative type variables with the non-expansive condition at let
  - paper: doi:10.1007/978-3-540-24754-8_15
    title: Jacques Garrigue, Relaxing the value restriction, Functional and Logic Programming (FLOPS 2004), Lecture Notes in Computer Science 2998, pages 196 to 213
    locator: the relaxed value restriction, which also generalizes type variables that occur only in covariant positions
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 13 (references, the rules T-Ref, T-Deref and T-Assign, and store typings) and Section 22.7 (the unsound polymorphic reference and the value restriction)
---

The value restriction is the rule that makes [let-polymorphism](/let-polymorphism/) sound in a language with mutable references. The plain rule of the [Hindley-Milner type system](/hindley-milner-type-system/) generalizes the type of every `let` definition. With references, this lets one cell hold an integer function and then be read as a boolean function, and the program gets stuck. The value restriction generalizes only when the right side of the `let` is a syntactic value, such as a function or a constant, whose evaluation cannot create a cell. Wright proposed it in 1995. Standard ML adopted it in its 1997 revision, in place of the imperative type variables of Tofte (1990). OCaml uses a relaxed form due to Garrigue (2004).

## Definition

**The language.** Extend the terms of the [Hindley-Milner page](/hindley-milner-type-system/) with references, as in Chapter 13 of Pierce's book:

$$e ::= \ldots \mid \texttt{ref } e \mid\ !e \mid e_1 := e_2 \mid e_1;\ e_2 \mid \texttt{()} \qquad \tau ::= \ldots \mid \tau\ \mathsf{ref} \mid \mathsf{unit}.$$

At run time, `ref v` allocates a new cell $l$ in the store, `!l` reads it, and `l := v` writes it and returns `()`. The typing rules are:

```text
Gamma |- e1 : tau1                 Gamma |- e1 : tau1 ref           Gamma |- e1 : tau1 ref    Gamma |- e2 : tau1
--------------------------  T-Ref  ----------------------  T-Deref  ------------------------------------------  T-Assign
Gamma |- ref e1 : tau1 ref         Gamma |- !e1 : tau1              Gamma |- e1 := e2 : unit

Gamma |- e1 : unit    Gamma |- e2 : tau2
----------------------------------------  T-Seq
Gamma |- e1; e2 : tau2
```

**Syntactic values.** A *syntactic value*, also called a *non-expansive* expression, is a term of the form

$$v ::= x \mid c \mid \texttt{fun } x \texttt{ -> } e \mid \texttt{()} \mid l,$$

where $l$ is a store location, which appears only at run time. Standard ML also counts tuples and constructor applications whose parts are values, except the constructor `ref`. An application, `ref e`, `!e`, `e1 := e2` and a `let` are not values. The test is purely syntactic: `fun x -> ref x` is a value, because its body runs only when it is called.

**The rule.** Replace T-Let' of the syntax-directed system by two rules:

```text
e1 is a value    Gamma |- e1 : tau1    Gamma, x : Gen(Gamma, tau1) |- e2 : tau2
-------------------------------------------------------------------------------  T-LetV
Gamma |- let x = e1 in e2 : tau2

e1 is not a value    Gamma |- e1 : tau1    Gamma, x : tau1 |- e2 : tau2
-----------------------------------------------------------------------  T-LetE
Gamma |- let x = e1 in e2 : tau2
```

T-LetE binds $x$ to the plain type $\tau_1$, as T-Abs would. So `let x = e1 in e2` with a non-value $e_1$ types like `(fun x -> e2) e1`. In [algorithm W](/algorithm-w/), the change is one test at the `let` line: if $e_1$ is not a value, store $\tau_1$ with no quantifier. The type variables of $\tau_1$ stay free in the context, and later uses of $x$ may fix them. Type checkers often call them *weak* type variables.

**Soundness.** With the value restriction, a closed well-typed program never gets stuck. The proof is [progress and preservation](/type-soundness/) (Wright 1995). Preservation is shown for a term together with a store typing $\Sigma$, which gives the type of each allocated cell, and Gen must also skip the type variables that are free in $\Sigma$. Source programs contain no locations, so this changes nothing for them. Two steps of the proof use the restriction.

- *The `let` step.* `let x = v in e2` steps to $[x := v]\,e_2$. Each copy of $v$ needs its own instance of the scheme, and the type substitution lemma gives it, because the generalized variables are free neither in $\Gamma$ nor in $\Sigma$. The step does nothing else, so the copying model of let-polymorphism is exact.
- *The allocation step.* `let x = ref v in e2` was typed with T-LetE, so $x$ has the plain type $\tau_1\ \mathsf{ref}$. After the step `ref v` becomes a new location $l$ with $\Sigma(l) = \tau_1$, and T-LetV for `let x = l in e2` generalizes nothing, since all variables of $\tau_1$ are now free in $\Sigma$. So the same typing of $e_2$ still works.

A non-value can allocate a cell while it runs, and then its type mentions the type of the new cell. That is the case that the restriction refuses to generalize.

## Examples and non-examples

**The unsound program.** Take the term

```text
let r = ref (fun x -> x) in
r := (fun x -> x + 1);
(!r) true
```

Without the restriction, it has the type $\mathsf{bool}$. The derivation, step by step, with the plain rule T-Let':

1. $x : \alpha \vdash x : \alpha$ by T-Var', so $\vdash \texttt{fun x -> x} : \alpha \to \alpha$ by T-Abs.
2. $\vdash \texttt{ref (fun x -> x)} : (\alpha \to \alpha)\ \mathsf{ref}$ by T-Ref.
3. The context is empty, so T-Let' binds $r$ to $\mathrm{Gen}(\emptyset, (\alpha \to \alpha)\ \mathsf{ref}) = \forall \alpha.\, (\alpha \to \alpha)\ \mathsf{ref}$. Let $\Gamma = r : \forall \alpha.\, (\alpha \to \alpha)\ \mathsf{ref}$.
4. $\Gamma \vdash r : (\mathsf{int} \to \mathsf{int})\ \mathsf{ref}$ by T-Var', with the instance $\alpha := \mathsf{int}$.
5. $\Gamma \vdash \texttt{fun x -> x + 1} : \mathsf{int} \to \mathsf{int}$ by T-Abs.
6. $\Gamma \vdash \texttt{r := (fun x -> x + 1)} : \mathsf{unit}$ by T-Assign, from steps 4 and 5.
7. $\Gamma \vdash r : (\mathsf{bool} \to \mathsf{bool})\ \mathsf{ref}$ by T-Var', with the instance $\alpha := \mathsf{bool}$.
8. $\Gamma \vdash \texttt{!r} : \mathsf{bool} \to \mathsf{bool}$ by T-Deref.
9. $\Gamma \vdash \texttt{(!r) true} : \mathsf{bool}$ by T-App.
10. $\Gamma \vdash \texttt{r := (fun x -> x + 1); (!r) true} : \mathsf{bool}$ by T-Seq, from steps 6 and 9.
11. $\vdash$ the whole term $: \mathsf{bool}$ by T-Let', from steps 2 and 10.

Each step follows the rules. The error is at step 3: the two uses of `r` in steps 4 and 7 choose two instances, but they name the same cell. Evaluation, with the store on the right:

```text
let r = ref (fun x -> x) in r := (fun x -> x + 1); (!r) true     | empty
-> let r = l in r := (fun x -> x + 1); (!r) true                  | l = fun x -> x
-> l := (fun x -> x + 1); (!l) true                               | l = fun x -> x
-> (); (!l) true                                                  | l = fun x -> x + 1
-> (!l) true                                                      | l = fun x -> x + 1
-> (fun x -> x + 1) true                                          | l = fun x -> x + 1
-> true + 1                                                       | l = fun x -> x + 1
```

The last term is not a value, and no rule applies to it. The program is stuck, so this type system is unsound. The copying model fails here: the copy `(ref (fun x -> x)) := ...; (!(ref (fun x -> x))) true` creates two cells and runs with no error, but the real program creates one cell.

**The same program with the restriction.** `ref (fun x -> x)` is not a value, so T-LetE binds `r` to $(\alpha \to \alpha)\ \mathsf{ref}$ with no quantifier. Step 4 now forces $\alpha = \mathsf{int}$, and step 7 needs $\alpha = \mathsf{bool}$. W fails at the unification of $\mathsf{int}$ with $\mathsf{bool}$, and the program is rejected. The program `let r = ref (fun x -> x) in r := (fun x -> x + 1); (!r) 2` uses the cell at one type and has the type $\mathsf{int}$.

**Values are still generalized.** In `let id = fun x -> x in ...`, `let n = 5 in ...` and `let k = fun x -> fun y -> x in ...`, the right sides are values, and the schemes are as in plain HM. A variable is a value too, so in `let g = id in if g true then g 1 else 0`, the name `g` gets $\forall \alpha.\, \alpha \to \alpha$.

**A safe program that the restriction rejects.** In

```text
let id = fun x -> x in
let f = id id in
if f true then f 1 else 0
```

the right side `id id` is an application, so `f` gets $\beta \to \beta$ with $\beta$ not quantified. The two uses need $\beta = \mathsf{bool}$ and $\beta = \mathsf{int}$, and the program is rejected, although plain HM gives it the type $\mathsf{int}$ and it runs without error. The usual repair is eta-expansion: `let f = fun y -> id id y` is a value and gets $\forall \beta.\, \beta \to \beta$. The same problem hits partial applications in real code, such as `let ids = List.map (fun x -> x)` in OCaml.

**Weak type variables in OCaml.** At the OCaml top level, `let r = ref []` gets the type `'_weak1 list ref`. The variable `'_weak1` is not quantified. After `r := [1]`, the type of `r` becomes `int list ref`, and `r := [true]` is then a type error.

**The relaxed restriction.** OCaml generalizes a type variable of a non-value when the variable occurs only in covariant positions of $\tau_1$, that is, never to the left of an arrow and never under `ref` or another mutable type (Garrigue 2004). So `let l = List.rev []` gets `'a list`, while `let r = ref []` still gets a weak variable.

## Related definitions

- **[Let-polymorphism](/let-polymorphism/).** The value restriction limits which `let` definitions get schemes. For pure programs, the copying model shows why every `let` is safe.
- **[Hindley-Milner type system](/hindley-milner-type-system/).** The value restriction only changes T-Let', so each typable term still has a principal type and W still finds it. See the [principal type theorem](/principal-type-theorem/).
- **Imperative type variables (Tofte 1990).** The approach of Standard ML in 1990. The type of `ref` uses imperative type variables, and a `let` may generalize them only when the right side is non-expansive. Other type variables are always generalized. The value restriction is simpler and replaced it in 1997.
- **[Effect systems](/effect-system/).** An effect system can record in the type which regions a computation allocates or writes, and then generalize all variables that no effect mentions. This accepts more programs, at the cost of more complex types.
- **The Haskell view.** Haskell needs no value restriction for references, because allocation is an `IO` action: in `do r <- newIORef []`, the name `r` is bound by a function argument and is monomorphic. Code that uses `unsafePerformIO` to allocate a top-level cell can break soundness in the same way as the program above. The monomorphism restriction of Haskell is a different rule, about [type classes](/type-classes/).
- **[Type soundness](/type-soundness/).** The theorem that the value restriction protects.

## References
