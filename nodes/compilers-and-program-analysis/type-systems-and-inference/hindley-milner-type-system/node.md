---
tag: 83V6MD
kind: definition
slug: hindley-milner-type-system
name: Hindley-Milner type system
aliases:
- Damas-Milner type system
- HM type system
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: The type system of ML, with type schemes that quantify type variables at let bindings, so that each typable term has a principal type.
prereqs: [let-polymorphism, simply-typed-lambda-calculus]
see_also: [algorithm-w, algorithm-j, principal-type-theorem, value-restriction, ml-typability-dexptime-completeness, polymorphic-recursion-undecidability, constraint-based-type-inference, system-f]
sources:
  - paper: doi:10.1145/582153.582176
    title: Luis Damas and Robin Milner, Principal type-schemes for functional programs, Ninth ACM Symposium on Principles of Programming Languages (POPL 1982), pages 207 to 212
    locator: the type schemes, the generic instance relation, the six inference rules (TAUT, INST, GEN, COMB, ABS, LET), and the statement of soundness and completeness of algorithm W
  - paper: doi:10.1016/0022-0000(78)90014-4
    title: Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375
    locator: Section 3 (the semantic soundness theorem, "well-typed expressions do not go wrong") and Section 4 (algorithm W, with polymorphism at let)
  - paper: doi:10.2307/1995158
    title: J. Roger Hindley, The principal type-scheme of an object in combinatory logic, Transactions of the American Mathematical Society 146, 1969, pages 29 to 60
    locator: the principal type-scheme theorem for combinatory logic, found by unification
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 22 (Section 22.7, let-polymorphism, with the rule that types let by substitution and the discussion of the cost of nested lets)
  - book: isbn:9780262162289
    title: Benjamin C. Pierce (ed.), Advanced Topics in Types and Programming Languages, MIT Press, 2005
    locator: Chapter 10 by Francois Pottier and Didier Remy, The essence of ML type inference (Section 10.1 the ML calculus and the Damas-Milner rules, Section 10.2 constraints)
  - paper: doi:10.1006/inco.1994.1093
    title: Andrew K. Wright and Matthias Felleisen, A syntactic approach to type soundness, Information and Computation 115(1), 1994, pages 38 to 94
    locator: the proof of soundness for a functional core of ML with let-polymorphism by progress and subject reduction, and the type substitution lemma for schemes
---

The Hindley-Milner (HM) type system is the type system of the core of ML, OCaml, F# and Haskell 98. It extends the Curry-style [simply typed lambda calculus](/simply-typed-lambda-calculus/) by one feature: a name bound by `let` can get a *type scheme* such as $\forall \alpha.\, \alpha \to \alpha$, and each use of the name can choose its own instance of the scheme. A name bound by `fun` keeps one type. This is [let-polymorphism](/let-polymorphism/). The system is small enough to have a *principal type* for each typable term, and [algorithm W](/algorithm-w/) finds it with no annotations in the program (Damas and Milner 1982). It sits between the simply typed calculus, which has no polymorphism, and [System F](/system-f/), where full type inference is [undecidable](/system-f-inference-undecidability/).

## Definition

**Terms.** Let $x$ range over term variables and $c$ over constants. The surface syntax is

$$e ::= x \mid c \mid \texttt{fun } x \texttt{ -> } e \mid e_1\ e_2 \mid \texttt{let } x = e_1 \texttt{ in } e_2.$$

The constants are the integers, `true` and `false`. The pages on algorithms also use `if`, the operators `+ - * < ==` and a recursive function form `fix f x -> e`. These need one rule each and change nothing below.

**Types and schemes.** Let $\alpha, \beta$ range over an infinite set of type variables.

$$\tau ::= \alpha \mid \mathsf{int} \mid \mathsf{bool} \mid \tau \to \tau \qquad\qquad \sigma ::= \tau \mid \forall \alpha.\, \sigma$$

A *type* $\tau$ has no quantifier. A *type scheme* $\sigma = \forall \alpha_1 \ldots \alpha_n.\, \tau$ has all its quantifiers at the outside, and $\alpha_1, \ldots, \alpha_n$ are its *bound* variables. So the quantifier never appears inside an arrow, and a function never takes a polymorphic argument. A *context* $\Gamma$ maps finitely many term variables to schemes. We write $\mathrm{ftv}(\sigma)$ for the free type variables of a scheme, and $\mathrm{ftv}(\Gamma)$ for the union over the schemes in $\Gamma$.

**Instances.** A type $\tau'$ is an *instance* of $\sigma = \forall \alpha_1 \ldots \alpha_n.\, \tau$, written $\sigma \sqsubseteq \tau'$, if $\tau' = [\alpha_1 := \tau_1, \ldots, \alpha_n := \tau_n]\,\tau$ for some types $\tau_1, \ldots, \tau_n$. Only bound variables are replaced. For example $\forall \alpha.\, \alpha \to \beta \sqsubseteq \mathsf{int} \to \beta$, but $\forall \alpha.\, \alpha \to \beta \not\sqsubseteq \mathsf{int} \to \mathsf{bool}$, because $\beta$ is free. A scheme $\sigma'$ is a *generic instance* of $\sigma$, written $\sigma \sqsubseteq \sigma'$, if each instance of $\sigma'$ is an instance of $\sigma$.

**Generalization.** $\mathrm{Gen}(\Gamma, \tau) = \forall \vec\alpha.\, \tau$, where $\vec\alpha$ lists the variables of $\mathrm{ftv}(\tau) \setminus \mathrm{ftv}(\Gamma)$. It quantifies exactly the variables that the context does not mention.

**Rules.** The judgment $\Gamma \vdash e : \sigma$ is the smallest relation closed under these rules. They are the rules of Damas and Milner (1982), with the names of Pierce's book. T-Gen and T-Inst can end a derivation of any term, so this form is not syntax directed.

```text
x : sigma in Gamma            Gamma, x : tau1 |- e : tau2               Gamma |- e1 : tau1 -> tau2    Gamma |- e2 : tau1
------------------  T-Var     ----------------------------------  T-Abs  ----------------------------------------------  T-App
Gamma |- x : sigma            Gamma |- fun x -> e : tau1 -> tau2        Gamma |- e1 e2 : tau2

Gamma |- e1 : sigma    Gamma, x : sigma |- e2 : tau
---------------------------------------------------  T-Let
Gamma |- let x = e1 in e2 : tau

Gamma |- e : sigma    alpha not in ftv(Gamma)            Gamma |- e : sigma    sigma below sigma'
---------------------------------------------  T-Gen    ----------------------------------------  T-Inst
Gamma |- e : forall alpha. sigma                         Gamma |- e : sigma'
```

In T-Inst, "sigma below sigma'" is $\sigma \sqsubseteq \sigma'$. T-Abs puts a type, not a scheme, into the context. This one restriction is what keeps inference decidable.

**The syntax-directed form.** Move each T-Inst to the variables and each T-Gen to the `let` that needs it. This gives an equivalent system with one rule per form of term:

```text
x : sigma in Gamma    sigma below tau              Gamma |- e1 : tau1    Gamma, x : Gen(Gamma, tau1) |- e2 : tau2
-------------------------------------  T-Var'      ----------------------------------------------------------  T-Let'
Gamma |- x : tau                                   Gamma |- let x = e1 in e2 : tau2
```

with T-Abs and T-App as before. A judgment $\Gamma \vdash e : \tau$ holds in the first system exactly when it holds in the second, and $\Gamma \vdash e : \sigma$ holds in the first exactly when $\Gamma \vdash e : \tau$ holds in the second for a $\tau$ with $\mathrm{Gen}(\Gamma, \tau) \sqsubseteq \sigma$. The proof is an induction on derivations: a T-Gen step can always move down to the next `let` or to the end, and a T-Inst step can always move up to a variable. Algorithms work on the syntax-directed form.

**Recursion.** The rule for `fix f x -> e` types the body with $f : \tau_1 \to \tau_2$ and $x : \tau_1$, both as plain types. So a recursive function is monomorphic inside its own body. Mycroft's extension, which gives $f$ a scheme there, makes inference [undecidable](/polymorphic-recursion-undecidability/).

**Soundness.** With the call-by-value semantics of the [simply typed lambda calculus](/simply-typed-lambda-calculus/) and the step $\texttt{let } x = v \texttt{ in } e \to [x := v]\,e$, a closed well-typed term never gets stuck. The proof is [progress and preservation](/type-soundness/) (Wright and Felleisen 1994). Preservation needs two substitution lemmas. The *term substitution* lemma: if $\Gamma, x : \sigma \vdash e : \tau$ and $\Gamma \vdash v : \sigma$, then $\Gamma \vdash [x := v]\,e : \tau$. The *type substitution* lemma: if $\Gamma \vdash e : \tau$, then $S\Gamma \vdash e : S\tau$ for each substitution $S$ of types for type variables. The side condition of T-Gen is what makes the type substitution lemma true. Milner (1978) proved the first form of the theorem, for a denotational semantics.

## Examples and non-examples

**Two uses at two types.** In `let id = fun x -> x in if id true then id 1 else 0`, the name `id` gets the scheme $\forall \alpha.\, \alpha \to \alpha$. The first use takes $\alpha := \mathsf{bool}$, the second $\alpha := \mathsf{int}$, and the term has type $\mathsf{int}$. The syntax-directed derivation, with $\Gamma = \texttt{id} : \forall \alpha.\, \alpha \to \alpha$, is:

```text
x : a |- x : a                         Gamma |- id : bool -> bool  Gamma |- true : bool     Gamma |- id 1 : int    Gamma |- 0 : int
------------------------------ T-Abs   ------------------------------------------------ T-App
|- fun x -> x : a -> a                 Gamma |- id true : bool
                                       ----------------------------------------------------------------------------------- T-If
                                       Gamma |- if id true then id 1 else 0 : int
-------------------------------------------------------------------------------------------------------------------------- T-Let'
|- let id = fun x -> x in if id true then id 1 else 0 : int
```

The empty context has no free variables, so $\mathrm{Gen}(\emptyset, \alpha \to \alpha) = \forall \alpha.\, \alpha \to \alpha$.

**The same body with a `fun`.** The term `fun f -> if f true then f 1 else 0` has no type. The variable `f` gets one type $\tau$ from T-Abs. The two uses need $\tau = \mathsf{bool} \to \beta$ and $\tau = \mathsf{int} \to \gamma$, and $\mathsf{bool} \ne \mathsf{int}$. System F types this term with $f : \forall \alpha.\, \alpha \to \alpha$, a rank-2 type that HM cannot write.

**A `let` that does not generalize.** In `fun x -> let y = x in y`, the variable `x` has type $\alpha$ in the context when `let` is typed. So $\mathrm{Gen}(x : \alpha, \alpha) = \alpha$ with no quantifier, and the term has type $\alpha \to \alpha$. The term `fun x -> let y = x in if y true then y 1 else 0` has no type for the same reason. If $\alpha$ were quantified, `y` would get $\forall \alpha.\, \alpha$, the term would get the type $\beta \to \mathsf{int}$, and the application of it to `5` would get stuck at `5 true`. This is why T-Gen asks that $\alpha$ is not free in $\Gamma$.

**Self-application.** `fun x -> x x` has no type. T-App would need $\alpha = \alpha \to \beta$, which fails the [occurs check](/occurs-check/). With [recursive types](/recursive-types/) the equation has a solution.

**Not an HM type.** $(\forall \alpha.\, \alpha \to \alpha) \to \mathsf{int}$ is a type of System F, but not an HM type or scheme, because a quantifier sits to the left of an arrow.

**Principal types.** `fun f -> fun g -> fun x -> f (g x)` has the principal type $(\alpha \to \beta) \to (\gamma \to \alpha) \to \gamma \to \beta$. Each other type of the term, such as $(\mathsf{int} \to \mathsf{bool}) \to (\mathsf{int} \to \mathsf{int}) \to \mathsf{int} \to \mathsf{bool}$, is an instance of it. The [principal type theorem](/principal-type-theorem/) says that such a type exists for each typable term.

## Related definitions

- **[Simply typed lambda calculus](/simply-typed-lambda-calculus/).** HM without schemes. A term `let x = e1 in e2` has an HM type exactly when $e_1$ has a type and the copy $[x := e_1]\,e_2$ has an HM type. So repeated substitution turns HM typing into simple typing, at the cost of an exponential growth of the term.
- **[System F](/system-f/).** HM is the fragment of System F in which quantifiers appear only at the outside of the types of `let`-bound names. Inference for HM is decidable, and for System F it is not.
- **[Algorithm W](/algorithm-w/) and [algorithm J](/algorithm-j/).** The two classic algorithms that compute principal types. [Constraint-based inference](/constraint-based-type-inference/) splits the same work into constraint generation and solving.
- **[Principal type theorem](/principal-type-theorem/).** Every typable term has a principal type scheme, and W computes it.
- **[DEXPTIME-completeness of ML typability](/ml-typability-dexptime-completeness/).** Deciding whether a term has an HM type is complete for [EXPTIME](/exptime/), because nested lets make types exponentially large.
- **[Value restriction](/value-restriction/).** With mutable references, T-Let' is unsound. ML generalizes only when $e_1$ is a syntactic value.
- **[Polymorphic recursion](/polymorphic-recursion-undecidability/).** HM with schemes for recursive functions inside their own bodies. Typability for it is equivalent to [semi-unification](/semi-unification-problem/), so it is undecidable.
- **Extensions.** [Type classes](/type-classes/) add constraints such as `Eq a` to schemes. [Row polymorphism](/row-polymorphism/) adds row variables for records. [Subtyping](/subtyping/) is hard to combine with principal types.

## References
