---
tag: ZXED05
kind: concept
slug: type-classes
name: Type classes
aliases:
- type class
- bounded ad hoc polymorphism
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: Named sets of overloaded operations with instances per type, resolved during inference by constraints on type variables.
prereqs: [hindley-milner-type-system]
see_also: [dictionary-passing-translation, monomorphization, let-polymorphism, algorithm-w, principal-type-theorem, constraint-based-type-inference, polymorphic-recursion-undecidability, subtyping]
sources:
  - paper: doi:10.1145/75277.75283
    title: Philip Wadler and Stephen Blott, How to make ad-hoc polymorphism less ad hoc, Sixteenth ACM Symposium on Principles of Programming Languages (POPL 1989), pages 60 to 76
    locator: the class and instance declarations, the inference rules with predicates, and the translation of overloading into dictionary passing
  - book: isbn:9780521472531
    title: Mark P. Jones, Qualified Types, Theory and Practice, Cambridge University Press, 1994
    locator: Chapter 2 (predicates and entailment), Chapter 3 (type inference for qualified types and principal types), Chapter 5 (semantics and coherence, ambiguity), Chapter 7 (type classes in Haskell)
  - paper: doi:10.1007/3-540-55253-7_17
    title: Mark P. Jones, A theory of qualified types, European Symposium on Programming (ESOP 1992), LNCS 582, pages 287 to 306
    locator: the qualified type system, the syntax-directed rules and the principal type result
  - paper: doi:10.1145/227699.227700
    title: Cordelia V. Hall, Kevin Hammond, Simon L. Peyton Jones and Philip L. Wadler, Type classes in Haskell, ACM Transactions on Programming Languages and Systems 18(2), 1996, pages 109 to 138
    locator: the static semantics of Haskell classes, superclasses, default methods and the translation into a language without classes
  - url: https://www.haskell.org/onlinereport/haskell2010/haskellch4.html
    title: Simon Marlow (ed.), Haskell 2010 Language Report, Chapter 4
    locator: Section 4.3 (overloading and classes) and Section 4.3.4 (ambiguous types and defaults for numeric operations)
---

A type class is a named set of operations, the *methods*, that are declared once for a type variable and defined for each type by an *instance*. A function that uses a method gets a *constraint* such as `Eq a` in its type, and type inference solves the constraints together with the equations of [Hindley-Milner inference](/hindley-milner-type-system/). Wadler and Blott (1989) proposed type classes to give overloading (one name, many types) a typing discipline that fits with [let-polymorphism](/let-polymorphism/), and Haskell adopted them. This page is about the type system. The [dictionary-passing translation](/dictionary-passing-translation/) is the usual way to compile it, and [monomorphization](/monomorphization/) is the other way.

## In plain words

Equality on numbers and equality on strings are different code, but you want to write one name for both. A type class gives that name a contract: "a type that has equality has a function that takes two values and returns true or false". An instance says how one type meets the contract. When you write a function that compares two values, the type checker sees that the values must be of a type with equality, and it records this as a condition in the type of your function. At each call, the checker finds the instance for the real type. If no instance exists, the call is a type error. If two instances could both apply, the meaning is not clear, and a careful language forbids this.

## The idea

### Syntax

The language is the one of the [Hindley-Milner page](/hindley-milner-type-system/), with class and instance declarations at the top level. Types, predicates and type schemes are:

$$\tau ::= \alpha \mid T\ \tau_1 \dots \tau_n \mid \tau_1 \to \tau_2 \qquad \pi ::= C\ \tau \qquad \sigma ::= \forall \bar\alpha.\ P \Rightarrow \tau$$

where $C$ is a class name and $P$ is a finite set of predicates. A type $P \Rightarrow \tau$ is a *qualified type*: it holds for every substitution of the variables that makes all of $P$ true. The declarations are written in Haskell syntax:

```text
class Eq a where (==) : a -> a -> Bool
instance Eq Int where (==) = primEqInt
instance Eq a => Eq [a] where (==) = eqList
class Eq a => Ord a where (<=) : a -> a -> Bool
```

Each method gets a scheme in the initial context: $(==) : \forall \alpha.\ \mathsf{Eq}\ \alpha \Rightarrow \alpha \to \alpha \to \mathsf{Bool}$. The last line makes $\mathsf{Eq}$ a *superclass* of $\mathsf{Ord}$: every instance of $\mathsf{Ord}$ must also be an instance of $\mathsf{Eq}$.

### Entailment

The judgment $P \Vdash \pi$ says that the predicates $P$ entail the predicate $\pi$, given the declared instances and classes. It is the smallest relation closed under these rules (Jones 1994, Chapter 2), where $S$ is a substitution of types for type variables:

```text
pi in P                    instance Q => C tau0 is declared    P ||- S pi' for each pi' in Q
--------  E-Hyp            ------------------------------------------------------------  E-Inst
P ||- pi                   P ||- C (S tau0)

class C' a => C a is declared    P ||- C tau
---------------------------------------------  E-Super
P ||- C' tau
```

For example, $\emptyset \Vdash \mathsf{Eq}\ [\mathsf{Int}]$ by E-Inst with the list instance and $S = [a := \mathsf{Int}]$, whose premise $\emptyset \Vdash \mathsf{Eq}\ \mathsf{Int}$ holds by E-Inst with the instance for $\mathsf{Int}$.

### Typing rules

The judgment $P \mid \Gamma \vdash e : \tau$ says that $e$ has type $\tau$ in context $\Gamma$ when the predicates $P$ hold. The syntax-directed rules (Jones 1992 and 1994, Chapter 3) are:

```text
(x : forall as. Q => tau) in Gamma    P ||- [ts/as] Q
------------------------------------------------------  T-Var
P | Gamma |- x : [ts/as] tau

P | Gamma, x : tau1 |- e : tau2                       P | Gamma |- e1 : tau1 -> tau2    P | Gamma |- e2 : tau1
------------------------------------  T-Abs           ---------------------------------------------------------  T-App
P | Gamma |- fun x -> e : tau1 -> tau2                P | Gamma |- e1 e2 : tau2

Q | Gamma |- e1 : tau1    P | Gamma, x : Gen(Gamma, Q => tau1) |- e2 : tau2
--------------------------------------------------------------------------  T-Let
P | Gamma |- let x = e1 in e2 : tau2
```

Here $\mathrm{Gen}(\Gamma, Q \Rightarrow \tau) = \forall \bar\alpha.\ Q \Rightarrow \tau$ with $\bar\alpha = \mathrm{ftv}(Q \Rightarrow \tau) \setminus \mathrm{ftv}(\Gamma)$. T-Var is where predicates are *used*: each use of an overloaded name must show that its instantiated predicates hold. T-Let is where they are *abstracted*: the predicates of the bound expression move into its scheme. With $P = \emptyset$ everywhere and no classes, these are exactly the HM rules.

### Inference

Inference is algorithm W with one more output. Each instantiation at T-Var adds the instantiated predicates to a set, and unification refines them with the same substitution as the types. At a `let`, the set is first *simplified* by context reduction: each predicate $C\ (T\ \bar\tau)$ whose head is a type constructor is replaced by the premises of the matching instance (E-Inst read backward), until each predicate is on a type variable or no instance matches. A predicate on a constructor that no instance matches, such as $\mathsf{Eq}\ (\mathsf{Int} \to \mathsf{Int})$, is a type error. Then the predicates on generalized variables go into the scheme. Jones (1992, 1994) proved the analogue of the [principal type theorem](/principal-type-theorem/): every typable term has a principal qualified type scheme, and the extended W finds it. Plain ML is the special case with no classes, so inference is at least as hard as ML typability, which is [DEXPTIME-complete](/ml-typability-dexptime-completeness/). Context reduction terminates under the Haskell 98 rules, where the context of an instance constrains only type variables of its head, because each step replaces a predicate by predicates on smaller types.

### Ambiguity and coherence

A scheme $\forall \bar\alpha.\ P \Rightarrow \tau$ is *ambiguous* if a variable of $\bar\alpha$ occurs in $P$ but not in $\tau$. Then no use of the term can fix that variable, and the meaning would depend on an instance that nothing in the program selects. Haskell rejects ambiguous types, except for a defaulting rule for numeric classes (Haskell 2010, Section 4.3.4).

The semantics of a program with classes is given by translation: each derivation of $P \mid \Gamma \vdash e : \tau$ gives a program in a language without classes, where each predicate becomes an argument that carries the methods. One term can have several derivations. The system is *coherent* if all of them give programs with the same meaning. Jones (1994, Chapter 5) proved coherence for unambiguous types, under the condition that each entailed predicate has one evidence value. Instance declarations that do not overlap give this condition: then each derivation of $P \Vdash \pi$ selects the same instances, and the translations are equal. Both conditions are needed. The examples below show a failure for each.

### Soundness

The classes add no new run-time steps: a program runs as its translation runs. So soundness is soundness of the translation target ([progress and preservation](/type-soundness/) for a lambda calculus with records), plus the fact that the translation of a well-typed term is well typed. The [dictionary-passing translation](/dictionary-passing-translation/) page states this and sketches the proof.

## Examples

**Inference with a constraint.** Infer the type of `let f = fun x -> fun y -> x == [y] in f [1] 2`.

| step | what happens | types and predicates |
|---|---|---|
| 1 | T-Abs twice | $x : \alpha$, $y : \gamma$ |
| 2 | T-Var on `==` | `==` $: \beta \to \beta \to \mathsf{Bool}$, predicate $\mathsf{Eq}\ \beta$ |
| 3 | `[y]` | type $[\gamma]$ |
| 4 | T-App twice, unify | $\alpha = \beta$, $\beta = [\gamma]$ |
| 5 | predicates after the substitution | $\mathsf{Eq}\ [\gamma]$ |
| 6 | context reduction by `instance Eq a => Eq [a]` | $\mathsf{Eq}\ \gamma$ |
| 7 | T-Let, generalize $\gamma$ | $f : \forall \gamma.\ \mathsf{Eq}\ \gamma \Rightarrow [\gamma] \to \gamma \to \mathsf{Bool}$ |
| 8 | T-Var on `f`, $\gamma := \mathsf{Int}$ | needs $\emptyset \Vdash \mathsf{Eq}\ \mathsf{Int}$, true by E-Inst |

The whole term has type $\mathsf{Bool}$, and its value is $[1] = [2]$, which is false. Step 6 matters for the output: without context reduction, the scheme would be $\forall \gamma.\ \mathsf{Eq}\ [\gamma] \Rightarrow \dots$, which is equivalent but larger.

**A missing instance.** In `f [fun z -> z] (fun z -> z)`, step 8 instantiates $\gamma$ to the type $\delta \to \delta$ of the identity function and needs $\mathsf{Eq}\ (\delta \to \delta)$. No instance has a head that matches a function type, so E-Inst does not apply, and the program is rejected. The error is a type error, found before the program runs.

**An ambiguous type.** In Haskell, `fun s -> show (read s)` gets the scheme $\forall \alpha.\ (\mathsf{Show}\ \alpha, \mathsf{Read}\ \alpha) \Rightarrow \mathsf{String} \to \mathsf{String}$. The variable $\alpha$ is not in $\mathsf{String} \to \mathsf{String}$. With $\alpha := \mathsf{Int}$ the function maps `"7"` to `"7"`; with $\alpha := \mathsf{Bool}$ it fails on `"7"`. Nothing selects one, so the term is rejected. Neither class is numeric, so defaulting does not apply. An annotation `read s : Int` removes the ambiguity.

**Overlapping instances break coherence.** Take one class and two instances whose heads unify:

```text
class C a where m : a -> Int
instance C a   where m = fun z -> 0
instance C Int where m = fun z -> 1
```

The term `m 3` with `3 : Int` needs $\emptyset \Vdash C\ \mathsf{Int}$. E-Inst gives two derivations: one with the second instance, and one with the first instance and $S = [a := \mathsf{Int}]$. Their translations evaluate to 1 and to 0. So the meaning of the program depends on the derivation, and the system is not coherent. A rule "choose the most specific instance" fixes `m 3` to 1, but it breaks a different law. Let `h = fun x -> m x` have the declared signature $\forall \alpha.\ \alpha \to \mathsf{Int}$, with no predicate. To check `h`, the checker must show $\emptyset \Vdash C\ \alpha$ for an unknown $\alpha$, and only the first instance matches. So `h 3` gives 0 while `m 3` gives 1, and replacing `h 3` by the body of `h` changes the result. Haskell 98 forbids overlapping instance heads. GHC allows overlap only with pragmas, and by default it refuses to solve $C\ \alpha$ with the general instance while a more specific one could still match later.

**Classes against subtyping.** A class constraint is not a [subtype](/subtyping/) bound. The type $\forall \alpha.\ \mathsf{Eq}\ \alpha \Rightarrow \alpha \to \alpha \to \mathsf{Bool}$ forces both arguments to have the same type. A function on an interface type $\mathsf{Eq} \to \mathsf{Eq} \to \mathsf{Bool}$ would accept an integer and a string together.

## Where it is used

- **Haskell** has single-parameter classes in the standard, with superclasses and default methods. GHC adds multi-parameter classes, functional dependencies, classes over type constructors (`Functor`, `Monad`) and associated types. GHC compiles classes by [dictionary passing](/dictionary-passing-translation/) and then specializes hot overloaded functions to known types.
- **Rust traits** are type classes with a coherence rule: at most one implementation of a trait for a type may exist in the whole program, and the orphan rule says where it may be written. Generic functions with trait bounds are compiled by [monomorphization](/monomorphization/); trait objects (`dyn Trait`) carry a table of methods, which is a dictionary packed with the value.
- **Other languages.** Scala implicits and `given` instances, Swift protocols, PureScript, Coq and Lean 4 type classes, and C++20 concepts (which constrain templates but do not change how they compile) follow the same idea of a constraint resolved from declared instances.
- **Inference engines.** HM(X) and [constraint-based type inference](/constraint-based-type-inference/) treat class predicates as one more kind of constraint next to equations.

## References
