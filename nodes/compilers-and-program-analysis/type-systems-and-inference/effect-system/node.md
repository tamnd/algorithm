---
tag: 77A8AC
kind: concept
slug: effect-system
name: Effect system
aliases:
- type and effect system
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Extends types with effects, such as the regions a function reads or writes, to reason about side effects and to enable optimizations.
prereqs: [simply-typed-lambda-calculus, type-soundness, let-polymorphism]
see_also: [region-based-memory-management, row-polymorphism, value-restriction, subtyping, constraint-based-type-inference, linear-types, alias-analysis, dead-code-elimination]
sources:
  - paper: doi:10.1145/73560.73564
    title: John M. Lucassen and David K. Gifford, Polymorphic effect systems, Fifteenth ACM Symposium on Principles of Programming Languages (POPL 1988), pages 47 to 57
    locator: the kinds of types, regions and effects, the effect rules with effect masking, and the use of non-interfering effects for parallel evaluation
  - paper: doi:10.1017/S0956796800000393
    title: Jean-Pierre Talpin and Pierre Jouvelot, Polymorphic type, region and effect inference, Journal of Functional Programming 2(3), 1992, pages 245 to 271
    locator: the static semantics with regions and effects and its consistency with the dynamic semantics, and the reconstruction algorithm with its correctness proof
  - paper: doi:10.1006/inco.1994.1046
    title: Jean-Pierre Talpin and Pierre Jouvelot, The type and effect discipline, Information and Computation 111(2), 1994, pages 245 to 296
    locator: the static semantics with subeffecting and observable effects, the generalization rule for programs with references, and the proof of consistency with the dynamic semantics
  - paper: doi:10.1006/inco.1996.2613
    title: Mads Tofte and Jean-Pierre Talpin, Region-based memory management, Information and Computation 132(2), 1997, pages 109 to 176
    locator: the region-annotated language with letregion, the effect-based region inference rules, and the proof that deallocation is safe
  - book: isbn:9783540654100
    title: Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999
    locator: Chapter 5 (type and effect systems), pages 283 to 363
  - paper: doi:10.4204/EPTCS.153.8
    title: Daan Leijen, Koka, programming with row polymorphic effect types, Mathematically Structured Functional Programming (MSFP 2014), EPTCS 153, pages 100 to 126
    locator: effect rows with row polymorphism, and the inference of effect types for the Koka language
---

An effect system adds a second component to the typing judgment: next to the type of the value that an expression returns, it gives an *effect*, a set that bounds what evaluation of the expression may do. Typical effects are the regions of memory that it reads, writes or allocates, the exceptions that it may throw, or the operations that it may perform. Function types carry a *latent effect*, the effect of a call. The type system guarantees that each real run does only what the effect lists. This differs from [linear types](/linear-types/), which control how many times a value is used, and from interprocedural side-effect analysis built on [alias analysis](/alias-analysis/), which needs the whole program and does not appear in the types. [Region-based memory management](/region-based-memory-management/) is the main application of region effects.

## In plain words

A type tells you what a piece of code gives back. An effect tells you what the code may do while it runs: read some memory, change some memory, throw an error, print something. The checker computes the effect of each expression from the effects of its parts. A function type remembers the effect of the function body, so a call to the function gets that effect too. The effect is a safe upper limit: the code may do less, but never more. The compiler can use this. Two pieces of code that do not touch the same memory can run in any order or at the same time. A piece of code with no effect at all can be removed if its result is not used, or computed only once.

## The idea

### Syntax

The language is the [simply typed lambda calculus](/simply-typed-lambda-calculus/) with references, where each allocation names a region. Regions $\rho$ are names for disjoint sets of memory locations, so each location belongs to exactly one region. Effect variables $\varsigma$ stand for unknown effects.

$$\varphi ::= \mathsf{alloc}\ \rho \mid \mathsf{read}\ \rho \mid \mathsf{write}\ \rho \qquad \varepsilon ::= \emptyset \mid \{\varphi\} \mid \varsigma \mid \varepsilon \cup \varepsilon$$

$$\tau ::= \mathsf{unit} \mid \mathsf{int} \mid \mathsf{ref}_\rho\ \tau \mid \tau_1 \xrightarrow{\varepsilon} \tau_2 \qquad e ::= x \mid n \mid () \mid \lambda x.\ e \mid e_1\ e_2 \mid \mathsf{ref}_\rho\ e \mid\ !e \mid e_1 := e_2 \mid \ell$$

Effects are equal up to the laws of sets: $\cup$ is associative, commutative and idempotent, with unit $\emptyset$. The location $\ell$ appears only at run time.

### Typing rules

The judgment $\Gamma; \Sigma \vdash e : \tau \mathbin{!} \varepsilon$ says that $e$ has type $\tau$ and that its evaluation has effects included in $\varepsilon$. The store typing $\Sigma$ gives the type $\mathsf{ref}_\rho\ \tau$ of each location. In the text blocks, `tau1 -[eps]-> tau2` is the arrow with latent effect `eps`, `{}` is the empty effect and `u` is union. The store typing is left out of the rules except in T-Loc.

```text
(x : tau) in Gamma                  Sigma(l) = ref[rho] tau
---------------------  T-Var        -------------------------------  T-Loc
Gamma |- x : tau ! {}               Gamma |- l : ref[rho] tau ! {}

Gamma, x : tau1 |- e : tau2 ! eps
-------------------------------------------  T-Abs
Gamma |- fun x -> e : tau1 -[eps]-> tau2 ! {}

Gamma |- e1 : tau1 -[eps]-> tau2 ! eps1    Gamma |- e2 : tau1 ! eps2
--------------------------------------------------------------------  T-App
Gamma |- e1 e2 : tau2 ! eps1 u eps2 u eps

Gamma |- e : tau ! eps
------------------------------------------------------  T-Ref
Gamma |- ref[rho] e : ref[rho] tau ! eps u {alloc rho}

Gamma |- e : ref[rho] tau ! eps
-------------------------------------  T-Deref
Gamma |- !e : tau ! eps u {read rho}

Gamma |- e1 : ref[rho] tau ! eps1    Gamma |- e2 : tau ! eps2
--------------------------------------------------------------  T-Assign
Gamma |- e1 := e2 : unit ! eps1 u eps2 u {write rho}

Gamma |- e : tau ! eps    eps included in eps'
----------------------------------------------  T-Sub
Gamma |- e : tau ! eps'

Gamma |- e : tau ! eps    rho not free in Gamma or tau
------------------------------------------------------  T-Mask
Gamma |- e : tau ! eps minus every effect on rho
```

T-Abs is the key rule: a function value has no effect when it is built, and the effect of its body moves into its type, to be paid at T-App. T-Sub (*subeffecting*) lets two branches of a conditional, or two functions passed to the same place, agree on one effect. T-Mask (*effect masking*, Lucassen and Gifford 1988) hides the effects on a region that nothing outside can see. A function that allocates a local reference, uses it and returns an integer is then pure from the outside.

### Semantics

A configuration is a pair $e \mid \mu$ of a term and a store. Each step has a label: an action $\mathsf{alloc}\ \rho$, $\mathsf{read}\ \rho$ or $\mathsf{write}\ \rho$, or $\mathsf{none}$. The values are $n$, $()$, $\lambda x.\ e$ and $\ell$, and each location remembers the region it was allocated in.

```text
(fun x -> e) v | mu     --none-->       [v/x] e | mu                            E-App
ref[rho] v | mu         --alloc rho-->  l | mu[l := v]   (l fresh, region(l) = rho)   E-Ref
!l | mu                 --read rho-->   mu(l) | mu       (region(l) = rho)       E-Deref
l := v | mu             --write rho-->  () | mu[l := v]  (region(l) = rho)       E-Assign

e | mu --a--> e' | mu'
-----------------------------  E-Ctx
E[e] | mu --a--> E[e'] | mu'
```

The evaluation contexts are $E ::= [\,] \mid E\ e \mid v\ E \mid \mathsf{ref}_\rho\ E \mid\ !E \mid E := e \mid v := E$, which fixes left-to-right call-by-value order. Steps of integer primitives have the label $\mathsf{none}$, and $e_1; e_2$ is short for $(\lambda x.\ e_2)\ e_1$ with $x$ not free in $e_2$.

### Soundness

Type soundness is [progress and preservation](/type-soundness/) as for references without effects. Effect soundness is the extra statement that the effect is an upper bound on every action of every run. It is proved here for the rules without T-Mask.

**Theorem (effect soundness).** If $\emptyset; \Sigma \vdash e : \tau \mathbin{!} \varepsilon$, the store $\mu$ is well typed under $\Sigma$, and $e \mid \mu$ takes the steps $a_1, a_2, \dots$, then every action $a_i \neq \mathsf{none}$ is in $\varepsilon$.

*Proof sketch.* Four lemmas.

1. *Values are pure.* If $\Gamma; \Sigma \vdash v : \tau \mathbin{!} \varepsilon$ for a value $v$, then $\Gamma; \Sigma \vdash v : \tau \mathbin{!} \emptyset$. The rules for values (T-Var, T-Loc, T-Abs and constants) give $\emptyset$, and T-Sub only makes the effect larger.
2. *Inversion.* Because T-Sub is not syntax-directed, each rule is inverted up to inclusion. For example, from $\Gamma \vdash\ !e : \tau \mathbin{!} \varepsilon$ follows $\Gamma \vdash e : \mathsf{ref}_\rho\ \tau \mathbin{!} \varepsilon_0$ with $\varepsilon_0 \cup \{\mathsf{read}\ \rho\} \subseteq \varepsilon$.
3. *Substitution.* If $\Gamma, x : \tau_1; \Sigma \vdash e : \tau \mathbin{!} \varepsilon$ and $\Gamma; \Sigma \vdash v : \tau_1 \mathbin{!} \emptyset$, then $\Gamma; \Sigma \vdash [v/x]e : \tau \mathbin{!} \varepsilon$. Because $v$ has no effect, putting it in the place of $x$ adds none.
4. *Effect preservation.* If $\emptyset; \Sigma \vdash e : \tau \mathbin{!} \varepsilon$, $\mu$ is well typed under $\Sigma$ and $e \mid \mu \xrightarrow{a} e' \mid \mu'$, then $a = \mathsf{none}$ or $a \in \varepsilon$, and there is a $\Sigma' \supseteq \Sigma$ such that $\mu'$ is well typed under $\Sigma'$ and $\emptyset; \Sigma' \vdash e' : \tau \mathbin{!} \varepsilon$.

The proof of Lemma 4 is by induction on the step. For E-Deref, inversion gives $\mathsf{read}\ \rho \in \varepsilon$ with $\rho$ the region of $\ell$ in $\Sigma$, and the action is $\mathsf{read}\ \rho$. E-Ref and E-Assign are the same, and E-Ref extends $\Sigma$ with the new location. For E-App, inversion of T-App gives the function type $\tau_1 \xrightarrow{\varepsilon_l} \tau_2$ with $\varepsilon_l \subseteq \varepsilon$, inversion of T-Abs gives the body the effect $\varepsilon_l$, and Lemmas 1 and 3 give $[v/x]e : \tau_2 \mathbin{!} \varepsilon_l$, which T-Sub lifts to $\varepsilon$. For E-Ctx, the subterm in the hole has an effect included in $\varepsilon$ by inversion, so the induction hypothesis applies to it, and the context is retyped around the new subterm. The theorem follows by induction on the number of steps, since the effect $\varepsilon$ stays the same at each step. $\square$

With T-Mask the statement holds for the actions on regions that are free in $\Gamma$ or $\tau$. The proof is harder, because a masked region appears in $\Sigma$ once its reference is allocated. Talpin and Jouvelot (1994) and Tofte and Talpin (1997) give such proofs.

The bound is safe but not exact. `if 0 = 1 then r := 1 else ()` has the effect $\{\mathsf{write}\ \rho\}$, although no run writes. An exact effect cannot be computed for all programs, by [Rice's theorem](/rice-theorem/).

### Checking and inference

*Checking* takes a program whose functions are annotated with types and latent effects. It computes the effect of each expression bottom-up by the rules, with T-Sub used only at the annotations, and checks the inclusions. Lucassen and Gifford's FX language worked this way.

*Inference* gives each arrow a fresh effect variable and generates two kinds of constraints: type equations, solved by unification as in [Hindley-Milner](/hindley-milner-type-system/), and effect inclusions $\varepsilon \subseteq \varsigma$. An inclusion constraint set of this form always has a least solution: start with every $\varsigma = \emptyset$ and add atoms until no constraint is violated. This ends because the atoms come from a finite set. Talpin and Jouvelot (1992) proved their reconstruction algorithm correct with respect to the static rules. At a `let`, the type, region and effect variables that occur neither in $\Gamma$ nor in the effect of the bound expression are generalized. This gives *effect polymorphism*:

$$\mathit{map} : \forall \alpha\, \beta\, \varsigma.\ (\alpha \xrightarrow{\varsigma} \beta) \xrightarrow{\emptyset} \mathsf{list}\ \alpha \xrightarrow{\varsigma} \mathsf{list}\ \beta$$

Each call of `map` has the effect of the function that it is given.

## Examples

**A counter.** Type `fun r -> r := !r + 1` with $r : \mathsf{ref}_\rho\ \mathsf{int}$.

| Subterm | Type | Effect | Rule |
| --- | --- | --- | --- |
| `r` | $\mathsf{ref}_\rho\ \mathsf{int}$ | $\emptyset$ | T-Var |
| `!r` | $\mathsf{int}$ | $\{\mathsf{read}\ \rho\}$ | T-Deref |
| `!r + 1` | $\mathsf{int}$ | $\{\mathsf{read}\ \rho\}$ | primitive |
| `r := !r + 1` | $\mathsf{unit}$ | $\{\mathsf{read}\ \rho, \mathsf{write}\ \rho\}$ | T-Assign |
| the function | $\mathsf{ref}_\rho\ \mathsf{int} \xrightarrow{\{\mathsf{read}\ \rho, \mathsf{write}\ \rho\}} \mathsf{unit}$ | $\emptyset$ | T-Abs |

**Masking local state.** In `(fun r -> (r := !r + 1; !r)) (ref[rho] 41)`, the effect is $\{\mathsf{alloc}\ \rho, \mathsf{read}\ \rho, \mathsf{write}\ \rho\}$ and the type is $\mathsf{int}$. The region $\rho$ is not free in the empty context or in $\mathsf{int}$, so T-Mask gives the effect $\emptyset$. The term returns 42, and no code outside can see the reference. Haskell's `runST` reaches the same result with a rank-2 type in place of a masking rule.

**Disjoint effects commute.** If $e_1$ has effect $\{\mathsf{read}\ \rho_1, \mathsf{write}\ \rho_1\}$ and $e_2$ has effect $\{\mathsf{read}\ \rho_2\}$, and $\rho_1 \neq \rho_2$, then neither writes a region that the other reads or writes. So `(e1, e2)` and the pair computed in the other order give the same result, and the two can run in parallel. This is the use that Lucassen and Gifford had in mind.

**Effects and generalization.** Talpin and Jouvelot record the type of the content in the allocation effect, written $\mathsf{init}(\rho, \tau)$. For `let r = ref [] in ...`, the type $\mathsf{ref}_\rho\ (\mathsf{list}\ \alpha)$ has $\alpha$ in the effect of the bound expression, so $\alpha$ is not generalized and the unsound use of `r` at two types is rejected. A pure `let` is generalized fully. This is a finer test than the syntactic [value restriction](/value-restriction/) that Standard ML adopted.

**Checked exceptions.** Java's `throws` clauses form an effect system with exception classes as atoms. A method body's effect is the set of checked exceptions it may throw, a call adds the callee's `throws` clause (the latent effect), and `try ... catch (E e)` removes `E` and its subclasses, as T-Mask removes a region. The compiler rejects a method whose effect is not included in its declared `throws` clause.

## Where it is used

- **Region inference.** The ML Kit compiler infers region and effect annotations with the rules of Tofte and Talpin (1997), and frees a whole region at the end of a `letregion` when the effect shows that no live value uses it. See [region-based memory management](/region-based-memory-management/).
- **Effect rows.** Koka gives each function a row of effect labels such as `<exn, div, console>` and uses [row polymorphism](/row-polymorphism/) for effect variables (Leijen 2014). Handlers of algebraic effects remove labels, as `catch` removes exceptions.
- **Exceptions and asynchrony.** Java checked exceptions, C++ `noexcept`, and Swift `throws` and `async` mark effects in function types, with simple inclusion checks.
- **Optimization.** A compiler that knows that an expression is pure may remove it when its value is not used ([dead code elimination](/dead-code-elimination/)), share it between two uses, or move it. Region effects give the same facts as an alias analysis, read from the types.
- **Program analysis.** Nielson, Nielson and Hankin (1999, Chapter 5) present type and effect systems as one of the main styles of static analysis, next to data flow analysis and abstract interpretation, with control flow and side-effect analyses as examples.

## References
