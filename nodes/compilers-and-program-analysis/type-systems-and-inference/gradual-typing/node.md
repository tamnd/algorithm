---
tag: 8MG0BR
kind: concept
slug: gradual-typing
name: Gradual typing
aliases:
- gradual type system
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Mixes static and dynamic typing in one language with an unknown type, consistency in place of equality, and run-time casts at the borders.
prereqs: [simply-typed-lambda-calculus, type-soundness, subtyping]
see_also: [bidirectional-type-checking, type-checking-problem, design-by-contract, refinement-types, effect-system]
sources:
  - paper: "Jeremy G. Siek and Walid Taha, Gradual typing for functional languages, Scheme and Functional Programming Workshop, September 2006, pages 81 to 92"
    title: Jeremy G. Siek and Walid Taha, Gradual typing for functional languages
    locator: the unknown type, the consistency relation, the gradually typed lambda calculus and its translation to a language with explicit casts
  - paper: doi:10.4230/LIPIcs.SNAPL.2015.274
    title: Jeremy G. Siek, Michael M. Vitousek, Matteo Cimini and John Tang Boyland, Refined criteria for gradual typing, 1st Summit on Advances in Programming Languages (SNAPL 2015), LIPIcs 32, pages 274 to 293
    locator: Figure 3 (the GTLC), Figure 4 (cast insertion and the cast calculus), Figure 6 (type and term precision), Theorems 1 to 4 in Sections 4.1 and 4.2, and Theorem 5 (the gradual guarantee) in Section 4.3
  - paper: doi:10.1007/978-3-642-00590-9_1
    title: Philip Wadler and Robert Bruce Findler, Well-typed programs can't be blamed, European Symposium on Programming (ESOP 2009), Lecture Notes in Computer Science, Springer, pages 1 to 16
    locator: the blame calculus, positive and negative blame, and the blame theorem
  - paper: doi:10.1145/1328438.1328486
    title: Sam Tobin-Hochstadt and Matthias Felleisen, The design and implementation of Typed Scheme, Thirty-Fifth ACM Symposium on Principles of Programming Languages (POPL 2008), pages 395 to 406
    locator: typed and untyped modules in one program, with contracts at the module borders
  - paper: doi:10.1145/2837614.2837630
    title: Asumu Takikawa, Daniel Feltey, Ben Greenman, Max S. New, Jan Vitek and Matthias Felleisen, Is sound gradual typing dead?, Forty-Third ACM Symposium on Principles of Programming Languages (POPL 2016), pages 456 to 468
    locator: the method of measuring all typed and untyped configurations of a program, and the measured cost of the checks in Typed Racket
---

Gradual typing lets one program have parts with static types and parts without them. It adds an *unknown type*, written $?$, and checks programs with a *consistency* relation in place of type equality, so a value of type $?$ can flow where an `int` is expected and the other way round. The meaning of a program comes from a translation that inserts a run-time *cast* at each place where consistency was used, and a failed cast reports *blame* on one place in the source. Siek and Taha (2006) gave the first formal system. Gradual typing is not optional typing: TypeScript and Python's type hints erase the annotations, so a wrong value passes the border without a check. It also differs from [subtyping](/subtyping/): consistency is symmetric, and it is not transitive.

## In plain words

Some programmers want the checker to prove things before the program runs. Others want to try ideas fast without writing types. Gradual typing lets each part of one program choose. A variable with no type gets the type "unknown", and the checker lets an unknown value go anywhere, and lets any value go where an unknown is expected. The checker still rejects a mix that can never work, such as a string where the declared type is a number. At each border between typed and untyped code, the compiler adds a check that runs at run time. If an untyped part gives a typed part a wrong value, the check fails there, and the error message names that border. So the typed parts can trust their types.

## The idea

### Syntax

The gradually typed lambda calculus (GTLC) of Siek et al. (2015, Figure 3) has

$$B ::= \mathsf{int} \mid \mathsf{bool} \qquad T ::= B \mid T \to T \mid\ ? \qquad e ::= k \mid x \mid \lambda x{:}T.\ e \mid (e\ e)^\ell$$

where $k$ is a constant and $\ell$ is a *blame label*, a unique source position. A function without an annotation, $\lambda x.\ e$, is short for $\lambda x{:}?.\ e$.

### Consistency

Two types are consistent, $T_1 \sim T_2$, if they agree on every part where both are known:

```text
--------  C-DynL     --------  C-DynR     --------  C-Base
? ~ T                T ~ ?                B ~ B

T1 ~ T3    T2 ~ T4
------------------------  C-Fun
T1 -> T2 ~ T3 -> T4
```

Consistency is reflexive and symmetric. It is *not transitive*: $\mathsf{int} \sim\ ?$ and $?\ \sim \mathsf{bool}$, but $\mathsf{int} \not\sim \mathsf{bool}$. It must not be: every type is consistent with $?$, so a transitive consistency would relate every pair of types and accept every program.

### Typing rules

The judgment $\Gamma \vdash e : T$ uses the function $\mathrm{fun}(T_1 \to T_2) = T_1 \to T_2$ and $\mathrm{fun}(?) = ?\ \to\ ?$, which treats an unknown value in function position as a function from unknown to unknown.

```text
(x : T) in Gamma
-----------------  T-Var    --------------------  T-Const
Gamma |- x : T              Gamma |- k : ty(k)

Gamma, x : T1 |- e : T2
--------------------------------------  T-Abs
Gamma |- fun (x : T1) -> e : T1 -> T2

Gamma |- e1 : T1    fun(T1) = T11 -> T12    Gamma |- e2 : T2    T2 ~ T11
--------------------------------------------------------------------------  T-App
Gamma |- (e1 e2)^l : T12
```

Only T-App differs from the [simply typed lambda calculus](/simply-typed-lambda-calculus/): it asks for $T_2 \sim T_{11}$ where the STLC asks for $T_2 = T_{11}$. *Checking* is syntax-directed and as easy as checking the STLC: one pass over the term, with a structural test of $\sim$ at each application. *Inference* of the missing annotations is a separate problem. Siek and Vachharajani (2008) and Garcia and Cimini (2015) study it with unification over types that contain $?$.

### Cast insertion

The meaning of the GTLC is given by a translation $\Gamma \vdash e \rightsquigarrow f : T$ into a *cast calculus*, whose terms add casts $f : T_1 \Rightarrow^\ell T_2$ and errors $\mathsf{blame}_T\ \ell$. Each use of $\mathrm{fun}$ or $\sim$ in T-App becomes a cast with the label of the application:

```text
Gamma |- e1 ~> f1 : T1    fun(T1) = T11 -> T12    Gamma |- e2 ~> f2 : T2    T2 ~ T11
--------------------------------------------------------------------------------------  I-App
Gamma |- (e1 e2)^l ~> (f1 : T1 =>l T11 -> T12) (f2 : T2 =>l T11) : T12
```

The other rules copy the term. In the cast calculus a cast is well typed only between consistent types, and $\mathsf{blame}_T\ \ell$ has every type $T$.

### Semantics

The *ground types* are $G ::= B \mid\ ?\ \to\ ?$. The values are constants, abstractions, *injections* $v : G \Rightarrow^\ell\ ?$ and *wrapped functions* $v : T_1 \to T_2 \Rightarrow^\ell T_3 \to T_4$. A chain of two casts $v : T_1 \Rightarrow^{\ell_1} T_2 \Rightarrow^{\ell_2} T_3$ is short for $(v : T_1 \Rightarrow^{\ell_1} T_2) : T_2 \Rightarrow^{\ell_2} T_3$. The reduction rules (Siek et al. 2015, Figure 4) are:

```text
(fun (x : T) -> f) v               -->  [x := v] f                                        Beta
v : B =>l B                        -->  v                                                 IdBase
v : ? =>l ?                        -->  v                                                 IdStar
v : G =>l1 ? =>l2 G                -->  v                                                 Succeed
v : G1 =>l1 ? =>l2 G2              -->  blame[G2] l2        if G1 /= G2                   Fail
(v1 : T1 -> T2 =>l T3 -> T4) v2    -->  v1 (v2 : T3 =>l T1) : T2 =>l T4                    AppCast
v : T =>l ?                        -->  v : T =>l G =>l ?   if T /= ?, T /= G, T ~ G       Ground
v : ? =>l T                        -->  v : ? =>l G =>l T   if T /= ?, T /= G, T ~ G       Expand
```

Two more rules evaluate inside a frame (Cong) and let blame end the whole program (Blame). AppCast is where higher-order casts are checked: a function cannot be checked when it crosses a border, so it is wrapped, and the argument and result are cast at each call. The argument is cast in the opposite direction, $T_3$ to $T_1$, because a function type is contravariant in its argument.

### Soundness and blame

The cast calculus is a typed language, and it is sound by [progress and preservation](/type-soundness/). *Preservation*: if $\vdash_C f : T$ and $f \longmapsto f'$, then $\vdash_C f' : T$. *Progress*: a closed well-typed $f$ is a value, is $\mathsf{blame}_T\ \ell$, or takes a step. Cast insertion preserves types: if $\Gamma \vdash e \rightsquigarrow f : T$, then $\Gamma \vdash_C f : T$. Together they give type safety of the GTLC (Siek et al. 2015, Theorem 3): if $\vdash e : T$, then $e$ evaluates to a value of type $T$, or to $\mathsf{blame}_T\ \ell$ for some $\ell$, or runs forever. Blame is a checked error at a known place, not undefined behavior.

The *blame-subtyping theorem* (Theorem 4) says which casts can fail. Define $B <: B$, $?\ <:\ ?$, $T <:\ ?$ when $T <: G$ for the ground type $G$ of $T$, and $T_1 \to T_2 <: S_1 \to S_2$ when $S_1 <: T_1$ and $T_2 <: S_2$. If the translation of $e$ contains a cast $f' : T_1 \Rightarrow^\ell T_2$ with $T_1 <: T_2$, and $e$ evaluates to $\mathsf{blame}_T\ \ell'$, then $\ell' \neq \ell$. So a cast up this order never fails, and fully static code is never blamed. The order is not "loses information": $\mathsf{int} \to \mathsf{int} \not<:\ ?$, because $?\ \not<: \mathsf{int}$ in the argument. A typed function cast to $?$ can be blamed when untyped code calls it with a wrong argument. Wadler and Findler (2009) proved the same result for the blame calculus as "well-typed programs can't be blamed".

### The gradual guarantee

*Type precision* $T \sqsubseteq T'$ means that $T$ has at least as much static information as $T'$ (the more precise type is on the left):

$$T \sqsubseteq\ ? \qquad B \sqsubseteq B \qquad \frac{T_1 \sqsubseteq T_3 \quad T_2 \sqsubseteq T_4}{T_1 \to T_2 \sqsubseteq T_3 \to T_4}$$

*Term precision* $e \sqsubseteq e'$ extends it to terms that are the same except for their annotations, with $\lambda x{:}T_1.\ e_1 \sqsubseteq \lambda x{:}T_2.\ e_2$ when $T_1 \sqsubseteq T_2$ and $e_1 \sqsubseteq e_2$.

**Theorem (gradual guarantee; Siek et al. 2015, Theorem 5).** Suppose $e \sqsubseteq e'$ and $\vdash e : T$.

1. $\vdash e' : T'$ and $T \sqsubseteq T'$.
2. If $e \Downarrow v$, then $e' \Downarrow v'$ and $v \sqsubseteq v'$. If $e$ diverges, then $e'$ diverges.
3. If $e' \Downarrow v'$, then $e \Downarrow v$ where $v \sqsubseteq v'$, or $e \Downarrow \mathsf{blame}_T\ l$. If $e'$ diverges, then $e$ diverges or $e \Downarrow \mathsf{blame}_T\ l$.

In words: removing annotations never breaks a well-typed program and never changes its result. Adding annotations keeps the result, except that a wrong annotation can turn a run into a blame error. The other criteria of the same paper are equivalence with the STLC on fully annotated terms (Theorem 1) and an exact embedding of the untyped lambda calculus (Theorem 2).

## Examples

**Consistency is not transitive.** For `(fun (y : int) -> y) ((fun (x : ?) -> x) true)`, the inner application has type $?$ because $\mathsf{bool} \sim\ ?$, and the outer one is well typed because $?\ \sim \mathsf{int}$. With $x$ annotated as `bool`, the inner application has type `bool`, and the outer one is a static error because $\mathsf{bool} \not\sim \mathsf{int}$. A checker with a transitive consistency would accept both.

**An error deferred to run time.** Label the inner application $\ell_1$ and the outer $\ell_2$. Cast insertion gives, with the casts from a type to itself left out (they reduce away by AppCast, IdBase and IdStar),

```text
(fun (y : int) -> y) ((fun (x : ?) -> x) (true : bool =>l1 ?) : ? =>l2 int)
-->  (fun (y : int) -> y) (true : bool =>l1 ? =>l2 int)          Beta inside the argument
-->  blame[int] l2                                              Fail, since bool /= int
```

The blame names $\ell_2$, the place where an unknown value entered code that expects `int`. The cast at $\ell_1$ goes from `bool` to $?$, and $\mathsf{bool} <:\ ?$, so the blame-subtyping theorem says it cannot fail.

**The precision lattice.** Siek et al. (2015, Figure 5) take `(fun (y : ?) -> y) ((fun (x : ?) -> x) 42)`. Annotating `x`, `y` or both with `int` keeps the result 42, as part 2 of the guarantee demands. Annotating `y` with `bool` gives a well-typed program that ends in blame, which part 3 allows. Annotating both with `bool` gives a static error, which is allowed because the guarantee speaks only about removing annotations from a well-typed program.

**Gradual against optional.** In TypeScript, `function inc(x: number): number { return x + 1 }` can be called from untyped JavaScript as `inc("1")`. The annotations are erased, so the call returns the string `"11"` and the error shows up later, somewhere else. In a sound gradual language such as Typed Racket, the call crosses a border from untyped to typed code, the cast from $?$ to `number` fails at once, and the blame names the untyped caller.

## Where it is used

- **Typed Racket** (Tobin-Hochstadt and Felleisen 2008) lets typed and untyped modules share one program and turns types at module borders into contracts, the run-time form of casts ([design by contract](/design-by-contract/)).
- **Other run-time semantics.** Reticulated Python uses *transient* checks, which test only the top type constructor of a value at fixed places such as function entry, and need no wrappers. Nominal designs, where each object carries its class, check a cast with one class test. Each choice changes the cost and which errors are caught.
- **Cost.** Takikawa et al. (2016) measured every mix of typed and untyped modules in a set of Typed Racket programs and found large slowdowns in many mixed configurations, from wrappers and repeated checks at each crossing. Wrappers can also pile up: a loop that passes a function across a border at each turn builds a chain of casts, and *coercion* representations that merge such chains keep space bounded.
- **Optional typing.** TypeScript, Python with mypy, Hack and Flow use the unknown type and consistency in their checkers but do not insert casts, by design. Their types help tools and readers, but they give no guarantee at run time.
- **Language features.** C# `dynamic` and Dart's `dynamic` type are unknown types whose uses are checked at run time.

## References
