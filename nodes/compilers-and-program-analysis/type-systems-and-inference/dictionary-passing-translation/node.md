---
tag: ACENP3
kind: technique
slug: dictionary-passing-translation
name: Dictionary-passing translation
aliases:
- dictionary passing
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Compiles type class constraints into extra arguments that are records of the instance methods, chosen at each call site.
prereqs: [type-classes]
see_also: [monomorphization, hindley-milner-type-system, system-f, value-restriction, polymorphic-recursion-undecidability, partial-evaluation, closure-conversion, inline-caching]
sources:
  - paper: doi:10.1145/75277.75283
    title: Philip Wadler and Stephen Blott, How to make ad-hoc polymorphism less ad hoc, Sixteenth ACM Symposium on Principles of Programming Languages (POPL 1989), pages 60 to 76
    locator: the translation of class declarations into dictionary types, of instances into dictionaries, and of overloaded functions into functions of dictionaries, given as inference rules that produce the translated term
  - paper: doi:10.1145/227699.227700
    title: Cordelia V. Hall, Kevin Hammond, Simon L. Peyton Jones and Philip L. Wadler, Type classes in Haskell, ACM Transactions on Programming Languages and Systems 18(2), 1996, pages 109 to 138
    locator: the full translation of Haskell classes, with superclasses and default methods, into a target language with explicit dictionaries
  - book: isbn:9780521472531
    title: Mark P. Jones, Qualified Types, Theory and Practice, Cambridge University Press, 1994
    locator: Chapter 4 (evidence, the translation of predicates into evidence parameters) and Chapter 5 (semantics and coherence of the translation)
  - url: https://www.haskell.org/onlinereport/haskell2010/haskellch4.html
    title: Simon Marlow (ed.), Haskell 2010 Language Report, Chapter 4
    locator: Section 4.5.5 (the monomorphism restriction and its motivation, the loss of sharing)
---

The dictionary-passing translation compiles a program with [type classes](/type-classes/) into a program without them. Each class becomes a record type of its methods, the *dictionary*. Each instance becomes a dictionary value, or a function from dictionaries to a dictionary when the instance has a context. Each predicate in a type scheme becomes one more parameter, and each use of an overloaded name receives the dictionary that the proof of its predicate builds. Wadler and Blott (1989) gave the translation together with the type system. The [type classes](/type-classes/) page is about the typing; [monomorphization](/monomorphization/) is the other way to compile, by one copy of the code per type.

## In plain words

Suppose a sort function must compare items, but it does not know their type. Instead of a hidden lookup, give it one more argument: a small table that holds the comparison for that type. The caller knows the type, so the caller passes the right table. A table for lists of items is built from the table for the items, by a function. The compiler does all of this for you. It adds the extra parameter to each function whose type has a class condition. At each call it builds the table from the instances that the type checker used to accept the call. After this step, no classes are left, and the program is an ordinary program with records and functions.

## When it applies

- The source language has qualified types $\forall \bar\alpha.\ P \Rightarrow \tau$, and the type checker builds a derivation of each entailment $P \Vdash \pi$ (see [type classes](/type-classes/)).
- Code must be compiled once for all types: separate compilation, a polymorphic function in a library, or a function whose set of type instances is not known or not finite. Polymorphic recursion with a declared signature is fine here, though it makes [monomorphization](/monomorphization/) impossible.
- The instances do not overlap, so that the derivation, and hence the translation, is unique in meaning (coherence).
- An extra argument and an indirect call per method are acceptable, or a later pass removes them by specialization.

## The template

### Class and instance declarations

A class with methods $m_1, \dots, m_k$ and superclasses $C'_1, \dots, C'_j$ becomes a record type $D_C\ \alpha$ with one field per method and one field per superclass. Each method becomes a selector function. An instance with context $Q = (\pi_1, \dots, \pi_k)$ becomes a function with one parameter per predicate of $Q$. For the classes of the type classes page:

```text
class Eq a where (==) : a -> a -> Bool         type EqD a = { eq : a -> a -> Bool }
                                               (==) = fun d -> d.eq
class Eq a => Ord a where (<=) : ...           type OrdD a = { le : a -> a -> Bool, superEq : EqD a }
instance Eq Int where (==) = primEqInt         eqInt = { eq = primEqInt }
instance Eq a => Eq [a] where (==) = ...       eqList = fun d -> { eq = fun xs -> fun ys -> ... d.eq x y ... (eqList d).eq xs' ys' ... }
```

### The translation rules

The translation extends the typing rules of [type classes](/type-classes/). The predicate set now names its evidence: $P$ is a list $d_1 : \pi_1, \dots, d_n : \pi_n$ of distinct *dictionary variables*. Entailment returns a term that builds the evidence:

```text
(d : pi) in P                  instance Q => C tau0 is translated to dfun    P ||- S pi_i ~> e_i  for each pi_i in Q
--------------  E-Hyp          ------------------------------------------------------------------------------  E-Inst
P ||- pi ~> d                  P ||- C (S tau0) ~> dfun e_1 ... e_k

C' is a superclass of C    P ||- C tau ~> e
-------------------------------------------  E-Super
P ||- C' tau ~> e.superC'
```

The term translation $P \mid \Gamma \vdash e \rightsquigarrow e' : \tau$ has one rule per form of term. Write $\lambda Q.\ e$ for `fun d_1 -> ... fun d_k -> e` when $Q = d_1 : \pi_1, \dots, d_k : \pi_k$.

```text
(x : forall as. Q => tau) in Gamma    P ||- [ts/as] pi_i ~> e_i  for each pi_i in Q
------------------------------------------------------------------------------------  D-Var
P | Gamma |- x ~> x e_1 ... e_k : [ts/as] tau

P | Gamma, x : tau1 |- e ~> e' : tau2                           P | Gamma |- e1 ~> e1' : tau1 -> tau2    P | Gamma |- e2 ~> e2' : tau1
------------------------------------------------------  D-Abs    ------------------------------------------------------------------  D-App
P | Gamma |- fun x -> e ~> fun x -> e' : tau1 -> tau2           P | Gamma |- e1 e2 ~> e1' e2' : tau2

Q | Gamma |- e1 ~> e1' : tau1    P | Gamma, x : Gen(Gamma, Q => tau1) |- e2 ~> e2' : tau2
------------------------------------------------------------------------------------------  D-Let
P | Gamma |- let x = e1 in e2 ~> let x = (lambda Q. e1') in e2' : tau2
```

D-Var applies an overloaded name to the dictionaries of its instantiated predicates. D-Let abstracts the bound expression over the dictionaries of the predicates it moved into the scheme. The other rules copy the term.

### The target and its types

Translate predicates and schemes to target types: $|C\ \tau| = D_C\ \tau$ and $|\forall \bar\alpha.\ \pi_1, \dots, \pi_k \Rightarrow \tau| = \forall \bar\alpha.\ |\pi_1| \to \dots \to |\pi_k| \to \tau$. For classes whose methods mention only the class variable, the target is the [Hindley-Milner](/hindley-milner-type-system/) language with records, because the dictionary parameters appear only in let-bound schemes. For classes over type constructors, a method such as `bind : m a -> (a -> m b) -> m b` is polymorphic in `b`, so the dictionary field needs a quantified type, and the target is [System F](/system-f/) or a language with polymorphic record fields.

**Type preservation.** If $P \mid \Gamma \vdash e \rightsquigarrow e' : \tau$, then $|P|, |\Gamma| \vdash e' : \tau$ in the target, where $|P|$ gives each $d_i$ the type $|\pi_i|$.

*Proof sketch.* First show, by induction on the entailment derivation, that $P \Vdash \pi \rightsquigarrow e$ implies $|P| \vdash e : |\pi|$. E-Hyp: $d : |\pi|$ is in $|P|$. E-Inst: `dfun` has type $\forall \bar\alpha.\ |Q| \to D_C\ \tau_0$; instantiate with $S$, then apply it to the $e_i$, which have the types $|S\pi_i|$ by induction. E-Super: the field `superC'` of a value of type $D_C\ \tau$ has type $D_{C'}\ \tau$. Then show the main claim by induction on the term derivation. D-Var instantiates the scheme of $x$, which has the type $\forall \bar\alpha.\ |Q| \to \tau$, and applies it to evidence of the right types. D-Abs and D-App are the target rules. D-Let: by induction $|Q|, |\Gamma| \vdash e_1' : \tau_1$, so $|\Gamma| \vdash \lambda Q.\ e_1' : |Q| \to \tau_1$. The variables $\bar\alpha$ of $\mathrm{Gen}$ are not free in $|\Gamma|$, because the dictionary variables of $Q$ are now bound by the lambdas. So the target may generalize them, and $x$ gets the scheme $|\mathrm{Gen}(\Gamma, Q \Rightarrow \tau_1)|$.

With [type soundness](/type-soundness/) of the target, a translated program never gets stuck: no method is ever looked up in a dictionary that lacks it.

**Meaning.** Erase the dictionaries: delete the dictionary lambdas and applications, and replace each selector applied to evidence by the method code of the instance that the evidence names. The result is the source program with each method call resolved to one instance. The translated program computes the same value as this resolved program, because a dictionary application only selects code and does no other work. Two derivations of the same typing judgment can build different evidence terms. If the instances do not overlap and the type is not ambiguous, all evidence terms for one predicate name the same instances, so all translations have the same meaning. This is the coherence theorem of Jones (1994, Chapter 5). Without it, the translation is well typed but the meaning of the source is not defined.

### Cost

The translation is linear in the size of the typing derivation: each rule adds a constant number of target nodes, except D-Var, which adds one evidence term per predicate of the scheme, of size at most the size of its entailment derivation. At run time each method call is a field load and an indirect call, and an instance with a context builds a new record at each use unless the compiler shares it.

## Classic examples

**A function with a list instance.** The type classes page infers $f : \forall \gamma.\ \mathsf{Eq}\ \gamma \Rightarrow [\gamma] \to \gamma \to \mathsf{Bool}$ for `f = fun x -> fun y -> x == [y]`. In the body, with $Q = d : \mathsf{Eq}\ \gamma$, the use of `==` needs $Q \Vdash \mathsf{Eq}\ [\gamma]$, and E-Inst with E-Hyp gives the evidence `eqList d`. So:

```text
source:      let f = fun x -> fun y -> x == [y] in f [1] 2
translated:  let f = fun d -> fun x -> fun y -> (eqList d).eq x [y] in f eqInt [1] 2
```

The call `f [1] 2` instantiates $\gamma := \mathsf{Int}$ and needs $\emptyset \Vdash \mathsf{Eq}\ \mathsf{Int}$, with evidence `eqInt`. Evaluation: `f eqInt [1] 2` steps to `(eqList eqInt).eq [1] [2]`. The list equality compares the heads with `eqInt.eq 1 2`, which is false, so the result is false, as in the source.

**A superclass.** For `g = fun x -> fun y -> x <= y || x == y`, inference collects $\mathsf{Ord}\ \alpha$ and $\mathsf{Eq}\ \alpha$. Context reduction drops $\mathsf{Eq}\ \alpha$, because E-Super derives it from $\mathsf{Ord}\ \alpha$, so $g : \forall \alpha.\ \mathsf{Ord}\ \alpha \Rightarrow \alpha \to \alpha \to \mathsf{Bool}$. The translation is `g = fun d -> fun x -> fun y -> d.le x y || d.superEq.eq x y`. One dictionary parameter carries both classes.

**Polymorphic recursion.** Take the nested type `data Nest a = Flat a | Deep (Nest [a])` and a function `display : forall a. Show a => Nest a -> String` with a declared signature, whose `Deep` case calls `display` at type `Nest [a]`. The translated call is `display (showList d) t`. A value with $k$ `Deep` layers makes the program build the dictionaries `d`, `showList d`, `showList (showList d)` and so on, $k + 1$ of them, at run time. One compiled copy of `display` serves all of them. Monomorphization would need one copy per type $[a], [[a]], \dots$, an infinite set (see [monomorphization](/monomorphization/)). The signature is required, because [inference with polymorphic recursion is undecidable](/polymorphic-recursion-undecidability/).

**Loss of sharing.** In `let n = expensive 10 in n + n`, suppose `expensive` is overloaded on a numeric class and nothing fixes the type of `n`. Then `n` gets the scheme $\forall \alpha.\ \mathsf{Num}\ \alpha \Rightarrow \alpha$ and is translated to `fun d -> expensive d (fromInteger d 10)`. Each use of `n` is now a call, so the work runs twice. This is why Haskell has the monomorphism restriction (Haskell 2010, Section 4.5.5): a binding without arguments and without a signature does not generalize its constrained variables.

## Variations

- **Specialization.** If a call site passes a dictionary that is known at compile time, such as `f eqInt`, a compiler can make a copy of `f` with the dictionary inlined, so that `(eqList eqInt).eq` becomes a direct call. This is [partial evaluation](/partial-evaluation/) on the dictionary argument. GHC does it on request and for hot functions, and keeps the dictionary version for the rest. Specializing every call is [monomorphization](/monomorphization/).
- **Dictionaries inside values.** An existential type such as `exists a. Show a => a`, a Rust trait object `dyn Trait`, or an object of a class in an object-oriented language stores the dictionary with the value. A method table in C++ or Java is a dictionary packed into each object. The call site then needs no evidence term, but every value carries one more pointer.
- **Type passing.** Pass a representation of the type instead of a dictionary, and select the method by a case on it at run time. This needs a closed set of types or a global table.
- **Programmer-written dictionaries.** Scala implicit parameters, OCaml modules passed as arguments, and Agda instance arguments make the dictionary an ordinary parameter that the compiler fills in at the call.

## Pitfalls

- **Effects under a dictionary lambda.** D-Let turns `let x = e1` into `let x = fun d -> e1'`. In a call-by-value language with effects, the effects of `e1` then run at each use of `x`, not once. A strict language must generalize predicates only over syntactic values, in the same way as the [value restriction](/value-restriction/) does for references.
- **Repeated dictionary construction.** In `eqList` above, the recursive call builds `eqList d` again for each element. Bind the record once with a `let` or a recursive definition, or let the optimizer float it out.
- **Overlap.** With overlapping instances, two evidence terms for one predicate can name different code. The translation is still well typed, so no check catches it; the language must forbid the overlap or fix a rule for it (see [type classes](/type-classes/)).
- **Ambiguity.** An ambiguous predicate has no evidence term that the program determines. The type checker must reject it before translation, or apply a default.
- **Order of dictionary parameters.** Separately compiled modules must agree on the order of the predicates in each scheme, since the order fixes the order of the dictionary parameters. Compilers fix a canonical order.

## Exercises

1. Translate `let h = fun x -> fun y -> x == y in h [[1]] [[1]]`. *Answer.* `let h = fun d -> fun x -> fun y -> d.eq x y in h (eqList (eqList eqInt)) [[1]] [[1]]`. The evidence for $\mathsf{Eq}\ [[\mathsf{Int}]]$ uses E-Inst twice and the instance for $\mathsf{Int}$ once. The result is true.
2. Give the target type of `eqList`. *Answer.* $\forall \alpha.\ \mathsf{EqD}\ \alpha \to \mathsf{EqD}\ [\alpha]$, the translation of the instance `Eq a => Eq [a]` read as a function.
3. A program applies `display` from the polymorphic recursion example to a value with 3 `Deep` layers. How many dictionaries does it build at run time, and how many copies of `display` does it compile? *Answer.* It builds 4 dictionaries (for $a$, $[a]$, $[[a]]$ and $[[[a]]]$) and compiles 1 copy.
4. Why does D-Let place $\lambda Q$ around `e1'` and not around the whole `let`? *Answer.* The dictionaries belong to the scheme of `x`. Each use of `x` in `e2` may instantiate the scheme at a different type, and then passes different dictionaries. Abstracting the whole `let` would fix one dictionary for all uses.

## References
