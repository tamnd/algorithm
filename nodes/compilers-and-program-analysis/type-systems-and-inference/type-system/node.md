---
tag: 4GFJEY
kind: concept
slug: type-system
name: Type system
aliases:
- static type system
area: compilers-and-program-analysis/type-systems-and-inference
level: intro
summary: A set of rules that assigns a type to each phrase of a program and rejects the programs whose phrases cannot be typed.
prereqs: [lambda-calculus, abstract-syntax-tree]
see_also: [type-checking-problem, type-inference-problem, simply-typed-lambda-calculus, type-soundness, subtyping, hindley-milner-type-system, gradual-typing, abstract-interpretation]
sources:
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 1, Section 1.1 (the definition of a type system as a tractable syntactic method), and Chapter 8 (typed arithmetic expressions, the rules T-True to T-IsZero, Theorems 8.3.2 and 8.3.3 on progress and preservation)
  - book: isbn:0849329094
    title: Luca Cardelli, Type Systems, in Allen B. Tucker (ed.), The Computer Science and Engineering Handbook, CRC Press, 1997
    locator: Chapter 103, pages 2208 to 2236 (trapped and untrapped errors, safe and typed languages, static and dynamic checking)
  - paper: doi:10.1016/0022-0000(78)90014-4
    title: Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375
    locator: Section 3 (the semantic soundness theorem, stated as "well-typed expressions do not go wrong")
  - paper: doi:10.1006/inco.1994.1093
    title: Andrew K. Wright and Matthias Felleisen, A syntactic approach to type soundness, Information and Computation 115(1), 1994, pages 38 to 94
    locator: the syntactic method, soundness as subject reduction plus progress for a small-step semantics
---

A type system is a set of rules that gives a type, such as $\mathsf{Nat}$ or $\mathsf{Bool} \to \mathsf{Nat}$, to each phrase of a program, using only the program text. A program that has a phrase with no type is rejected before it runs. When the rules are [sound](/type-soundness/), a program that passes cannot reach a state where an operation gets a value of the wrong kind, such as adding a number to a function. The price is that the rules must be conservative: some programs that would run without error are rejected too.

## In plain words

A type says what kind of value a piece of a program can produce: a number, a truth value, or a function from numbers to numbers. A type system is a list of rules. Each rule gives a piece of the program its type from the types of its parts. If some piece gets no type, the program is rejected. The checker reads the text of the program and does not run it. So the checker cannot know which branch a test will take, and it must be careful: it rejects every program that could misuse a value, and as a price it also rejects some programs that would run fine. In return the guarantee holds for every input at once. A program that passes never calls a number as a function and never asks if a function is zero.

## The idea

### Types, contexts and the judgment

A type system has three parts: a grammar of types, a grammar of terms, and a set of inference rules for a *typing judgment*. The judgment $\Gamma \vdash e : \tau$ reads "in context $\Gamma$, the term $e$ has type $\tau$". The context $\Gamma$ is a finite map from variables to types. It records the types of the variables that are free in $e$. A term $e$ is *well typed* if there is a $\tau$ with $\vdash e : \tau$ in the empty context, and a derivation is a finite tree of rule instances that ends in the judgment.

The smallest useful example is the language of typed arithmetic expressions in Chapter 8 of Pierce's book. It has no variables, so the context is empty and is left out.

$$
\tau ::= \mathsf{Bool} \mid \mathsf{Nat} \qquad
e ::= \mathsf{true} \mid \mathsf{false} \mid \mathsf{if}\ e\ \mathsf{then}\ e\ \mathsf{else}\ e \mid 0 \mid \mathsf{succ}\ e \mid \mathsf{pred}\ e \mid \mathsf{iszero}\ e
$$

The values are $\mathsf{true}$, $\mathsf{false}$ and the numeric values $nv ::= 0 \mid \mathsf{succ}\ nv$. The typing rules have the premises above the line and the conclusion below it.

```text
                               e1 : Bool    e2 : T    e3 : T
-----------  T-True  (also     -----------------------------  T-If
true : Bool   T-False)          if e1 then e2 else e3 : T

                   e : Nat             e : Nat               e : Nat
--------  T-Zero   ----------  T-Succ  ----------  T-Pred    --------------  T-IsZero
 0 : Nat           succ e : Nat        pred e : Nat          iszero e : Bool
```

The small-step semantics $e \to e'$ has the computation rules E-IfTrue ($\mathsf{if\ true\ then}\ e_2\ \mathsf{else}\ e_3 \to e_2$), E-IfFalse, E-PredZero ($\mathsf{pred}\ 0 \to 0$), E-PredSucc ($\mathsf{pred}\ (\mathsf{succ}\ nv) \to nv$), E-IszeroZero ($\mathsf{iszero}\ 0 \to \mathsf{true}$) and E-IszeroSucc ($\mathsf{iszero}\ (\mathsf{succ}\ nv) \to \mathsf{false}$), and one congruence rule per form (E-If, E-Succ, E-Pred, E-IsZero) that steps the first subterm that is not yet a value.

A term is *stuck* if it is not a value and no rule applies to it. The terms $\mathsf{succ\ true}$ and $\mathsf{if}\ 0\ \mathsf{then}\ 0\ \mathsf{else}\ 0$ are stuck. A stuck term is the formal picture of a run-time type error: the machine has an operation and an operand of the wrong kind.

### What the rules buy: safety

The rules are *sound* if a well-typed term never reaches a stuck term. Wright and Felleisen (1994) split this into two lemmas that are each proved by induction on a typing derivation:

- **Progress.** If $\vdash e : \tau$, then $e$ is a value or there is an $e'$ with $e \to e'$.
- **Preservation.** If $\vdash e : \tau$ and $e \to e'$, then $\vdash e' : \tau$.

By induction on the number of steps, every term that a well-typed term reaches is well typed, so it is not stuck. The full statement and proof for the [simply typed lambda calculus](/simply-typed-lambda-calculus/) are on the [type soundness](/type-soundness/) page. Soundness is always relative to one semantics and one definition of "stuck". A division by zero, an array index out of range or a null dereference is usually *not* a stuck state: the semantics defines it to raise an exception, and the type system says nothing about it.

### Why the rules must be conservative

No static type system for a Turing-complete language can accept exactly the programs that never get stuck. Suppose a checker $C$ did. For any program $p$, build the term $(\mathsf{fun}\ \_ \to \mathsf{succ\ true})\ (p\ ())$. Under call-by-value, this term gets stuck if and only if $p$ halts. So $C$ would decide the [halting problem](/halting-problem/). This is a case of [Rice's theorem](/rice-theorem/). A real checker therefore errs on one side. A sound checker rejects some safe programs; an unsound checker accepts some programs that go wrong. Designers choose soundness for the core of the language and add run-time checks for the rest.

### Two questions about the same rules

The rules define a relation. Two algorithmic questions come from it, and they have very different difficulty.

- [Type checking](/type-checking-problem/): given $\Gamma$, $e$ and $\tau$, decide whether $\Gamma \vdash e : \tau$.
- [Type inference](/type-inference-problem/): given $e$, find a $\Gamma$ and a $\tau$ that make the judgment hold, or report that none exist.

When the programmer writes the type of every bound variable (Church style, or explicit typing), checking is easy for the simple systems. When the types are left out (Curry style, or implicit typing), the checker must infer them. For the [simply typed lambda calculus](/simply-typed-lambda-calculus/) inference is [first-order unification](/unification-problem/). For [System F](/system-f/) it is undecidable ([Wells' theorem](/system-f-inference-undecidability/)).

### Static and dynamic checking

A *statically typed* language checks the rules before the program runs. A *dynamically typed* language keeps a tag with each value and checks the tag at each operation. Both are safe in Cardelli's sense: every error is *trapped*, which means the run stops with a defined error instead of reading memory as the wrong kind of data. C is typed but not safe, because a cast or an out-of-range write gives an untrapped error. The static check gives a guarantee for all inputs before the first run. The dynamic check rejects only runs that really fail. [Gradual typing](/gradual-typing/) mixes the two in one language.

### Other axes

- *Structural* type equality compares the shape of two types. *Nominal* equality compares their declared names. Java classes are nominal; OCaml object types are structural.
- [Subtyping](/subtyping/) lets a value of one type be used where another type is expected.
- *Polymorphism* lets one term have many types: parametric polymorphism ([System F](/system-f/), [Hindley-Milner](/hindley-milner-type-system/)), subtype polymorphism, and ad hoc polymorphism ([type classes](/type-classes/)).
- Richer systems track more than the shape of values: [effect systems](/effect-system/) track side effects, [linear types](/linear-types/) track how often a value is used, and [dependent types](/dependent-types/) let types mention values.

## Examples

**A typed term.** The term $\mathsf{if\ iszero}\ (\mathsf{succ}\ 0)\ \mathsf{then}\ 0\ \mathsf{else\ succ}\ 0$ has type $\mathsf{Nat}$. The derivation uses T-Zero, then T-Succ for $\mathsf{succ}\ 0 : \mathsf{Nat}$, then T-IsZero for the test, which has type $\mathsf{Bool}$. Both branches have type $\mathsf{Nat}$, so T-If gives $\mathsf{Nat}$. The term takes two steps: E-IsZero with E-IszeroSucc gives $\mathsf{if\ false\ then}\ 0\ \mathsf{else\ succ}\ 0$, and E-IfFalse gives the value $\mathsf{succ}\ 0$, which has type $\mathsf{Nat}$, as preservation says.

**A stuck term is rejected.** The term $\mathsf{succ\ true}$ is stuck: it is not a value, and no rule steps it. T-Succ needs $\mathsf{true} : \mathsf{Nat}$, and the only rule for $\mathsf{true}$ gives $\mathsf{Bool}$, so the term has no type.

**A safe term is rejected.** The term $\mathsf{if\ true\ then}\ 0\ \mathsf{else\ false}$ steps in one step to the value $0$, so it never gets stuck. But T-If needs both branches to have the same type, and $\mathsf{Nat} \neq \mathsf{Bool}$. The checker does not know which branch runs, so it rejects the term. This is the price of a static check.

**A safe function with no simple type.** In the [simply typed lambda calculus](/simply-typed-lambda-calculus/), the term $\mathsf{fun}\ x \to x\ x$ has no type. If $x : \tau$, then T-App needs $\tau = \tau \to \tau'$, and no finite type satisfies this equation. Unification fails on it with the [occurs check](/occurs-check/). A system with [recursive types](/recursive-types/) gives it the type $\mu\alpha.\alpha \to \alpha$.

**A dynamic check.** In Python, `1 + "a"` raises a `TypeError` at run time. The same expression in OCaml, `1 + "a"`, is rejected by the compiler before the program runs. Both errors are trapped. Only the time of the report differs.

## Where it is used

- **Compilers.** Every statically typed language (ML, Haskell, Java, C#, Rust, Go, TypeScript) runs a type checker after parsing, on the [abstract syntax tree](/abstract-syntax-tree/). The types then guide code generation: they fix the size and layout of values, select the right machine operation for `+` on integers or floats, and drive [monomorphization](/monomorphization/) and [dictionary passing](/dictionary-passing-translation/).
- **Optimization.** A sound type system lets the compiler drop run-time tag checks and unbox values, because the types prove the checks always succeed.
- **Security.** The Java bytecode verifier is a type checker for the bytecode. It lets a virtual machine run code it does not trust without a check at each instruction.
- **Proofs.** By the [Curry-Howard correspondence](/curry-howard-correspondence/), a type checker for a rich enough system is a proof checker. Coq, Agda and Lean work on this basis.
- **Static analysis.** Many program analyses are phrased as type systems (effect systems, [borrow checking](/borrow-checking/) in Rust, [refinement types](/refinement-types/)). Others are phrased as [abstract interpretation](/abstract-interpretation/). The two views often describe the same analysis.

## References
