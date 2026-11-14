---
tag: 4JA4HE
kind: model
slug: system-f
name: System F
aliases:
- polymorphic lambda calculus
- second-order lambda calculus
- Girard-Reynolds calculus
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: The simply typed lambda calculus with abstraction over types, so one term works at every type. It is strongly normalizing, and Church-style checking is decidable but Curry-style typing is not.
prereqs: [simply-typed-lambda-calculus]
see_also: [system-f-inference-undecidability, hindley-milner-type-system, curry-howard-correspondence, reducibility-method, subtyping, type-soundness, dictionary-passing-translation, monomorphization]
sources:
  - paper: "Jean-Yves Girard, Interpretation fonctionnelle et elimination des coupures de l'arithmetique d'ordre superieur, these de doctorat d'Etat, Universite Paris VII, 1972"
    locator: the system F, its strong normalization by reducibility candidates, and the representation of the functions provably total in second-order arithmetic
  - paper: "John C. Reynolds, Towards a theory of type structure, in B. Robinet (ed.), Programming Symposium, Paris 1974, LNCS 19, Springer, 1974"
    locator: the polymorphic lambda calculus with type abstraction and type application, found independently of Girard
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 23 (the rules T-TAbs, T-TApp, E-TApp, E-TappTabs; Section 23.4 Church encodings; Section 23.5 basic properties; Section 23.6 erasure, typability and type reconstruction; Section 23.7 erasure and evaluation order)
  - book: isbn:9780521371810
    title: Jean-Yves Girard, Yves Lafont and Paul Taylor, Proofs and Types, Cambridge University Press, 1989
    locator: Chapter 11 (System F and its representation of data types), Chapter 14 (strong normalization by reducibility candidates), Chapter 15 (the representation theorem)
  - paper: "John C. Reynolds, Types, abstraction and parametric polymorphism, Information Processing 83 (IFIP Congress), North-Holland, 1983"
    locator: the abstraction theorem (relational parametricity)
  - paper: "John C. Reynolds, Polymorphism is not set-theoretic, in Semantics of Data Types, LNCS 173, Springer, 1984"
    locator: the main theorem (no set-theoretic model interprets the polymorphic types)
  - paper: doi:10.1016/S0168-0072(98)00047-5
    title: Joe B. Wells, Typability and type checking in System F are equivalent and undecidable, Annals of Pure and Applied Logic 98(1-3), 1999, pages 111 to 156
    locator: Theorem 4.1 and Section 6 (Curry-style type checking and typability are undecidable)
  - paper: "Philip Wadler, Theorems for free!, Functional Programming Languages and Computer Architecture (FPCA), 1989"
    locator: the free theorems derived from parametricity for polymorphic types
---

System F extends the [simply typed lambda calculus](/simply-typed-lambda-calculus/) with functions over types. The term $\Lambda\alpha.\,\lambda x{:}\alpha.\,x$ takes a type and returns the identity function at that type, and it has the type $\forall\alpha.\,\alpha \to \alpha$. Girard (1972) found the system as the proof terms of second-order logic, and Reynolds (1974) found it independently as a model of polymorphic programs. Every well-typed term terminates, and yet the calculus can define every function that second-order arithmetic proves total. Church-style checking is easy, but [inference is undecidable](/system-f-inference-undecidability/).

## The machine

System F is a model of programs, not a machine model. A run is a sequence of small steps on a term, as for the STLC.

### Syntax

$$
\begin{aligned}
T &::= \alpha \mid T \to T \mid \forall\alpha.\,T \\
t &::= x \mid \lambda x{:}T.\,t \mid t\ t \mid \Lambda\alpha.\,t \mid t\,[T] \\
v &::= \lambda x{:}T.\,t \mid \Lambda\alpha.\,t
\end{aligned}
$$

$\Lambda\alpha.t$ is a *type abstraction* and $t\,[T]$ a *type application*. The quantifier binds $\alpha$; types are equal up to renaming of bound type variables. A context $\Gamma$ holds term variables with types and type variables. Base types such as $\mathsf{Int}$ are not needed: they can be encoded, as shown below.

### Typing

The rules are those of the STLC (T-Var, T-Abs, T-App) plus two more (Pierce, Chapter 23).

```text
Gamma, a |- t : T                            Gamma |- t : forall a. T1
------------------------------  T-TAbs        -----------------------------  T-TApp
Gamma |- /\a. t : forall a. T                Gamma |- t [T2] : [a := T2] T1
```

In T-TAbs, the variable $\alpha$ must be fresh for $\Gamma$, which the context extension expresses. Without that side condition, $\lambda x{:}\alpha.\,\Lambda\alpha.\,x$ would get the wrong type $\alpha \to \forall\alpha.\alpha$.

The quantifier is *impredicative*: $\forall\alpha.T$ ranges over all types, including itself. So $\mathit{id}\,[\forall\alpha.\alpha \to \alpha]\ \mathit{id}$ is well typed, and the polymorphic identity is applied to itself.

### Evaluation

Call-by-value small steps: E-App1, E-App2 and E-AppAbs as in the STLC, plus

```text
t1 --> t1'
---------------------  E-TApp        -----------------------------  E-TappTabs
t1 [T2] --> t1' [T2]                 (/\a. t) [T2] --> [a := T2] t
```

Type soundness holds by the same [progress and preservation](/type-soundness/) proof, with one new lemma: substitution of a type for a type variable keeps typing ($\Gamma, \alpha, \Delta \vdash t : T$ implies $\Gamma, [\alpha := S]\Delta \vdash [\alpha := S]\,t : [\alpha := S]\,T$).

### Church encodings

Data types are definable from $\to$ and $\forall$ alone (Pierce, Section 23.4; Girard, Lafont and Taylor, Chapter 11).

- Booleans: $\mathsf{CBool} = \forall\alpha.\,\alpha \to \alpha \to \alpha$, with $\mathit{tru} = \Lambda\alpha.\lambda t{:}\alpha.\lambda f{:}\alpha.\,t$ and $\mathit{fls} = \Lambda\alpha.\lambda t{:}\alpha.\lambda f{:}\alpha.\,f$.
- Natural numbers: $\mathsf{CNat} = \forall\alpha.\,(\alpha \to \alpha) \to \alpha \to \alpha$, with $\underline{n} = \Lambda\alpha.\lambda f{:}\alpha{\to}\alpha.\lambda x{:}\alpha.\,f^n\,x$.
- Pairs: $A \times B = \forall\alpha.\,(A \to B \to \alpha) \to \alpha$. Sums: $A + B = \forall\alpha.\,(A \to \alpha) \to (B \to \alpha) \to \alpha$.
- Lists: $\mathsf{List}\,A = \forall\alpha.\,(A \to \alpha \to \alpha) \to \alpha \to \alpha$, the type of `fold_right`.
- Existential types: $\exists\alpha.T = \forall\beta.\,(\forall\alpha.\,T \to \beta) \to \beta$. These are abstract data types.

A script with a Church-style checker for System F gives these types, and runs the erased terms on numerals:

| term | type | value on numerals |
|---|---|---|
| $\mathit{id} = \Lambda\alpha.\lambda x{:}\alpha.\,x$ | $\forall\alpha.\,\alpha \to \alpha$ | |
| $\lambda x{:}\forall\alpha.\alpha{\to}\alpha.\ x\,[\forall\alpha.\alpha{\to}\alpha]\ x$ | $(\forall\alpha.\alpha \to \alpha) \to \forall\alpha.\alpha \to \alpha$ | |
| $\mathit{exp} = \lambda m{:}\mathsf{CNat}.\lambda n{:}\mathsf{CNat}.\ \Lambda\alpha.\ n\,[\alpha \to \alpha]\,(m\,[\alpha])$ | $\mathsf{CNat} \to \mathsf{CNat} \to \mathsf{CNat}$ | $\mathit{exp}\ \underline{2}\ \underline{3} = \underline{8}$ |
| $\mathit{ack} = \lambda m{:}\mathsf{CNat}.\ m\,[\mathsf{CNat} \to \mathsf{CNat}]\ \mathit{step}\ \mathit{succ}$ | $\mathsf{CNat} \to \mathsf{CNat} \to \mathsf{CNat}$ | $\mathit{ack}\ \underline{3}\ \underline{3} = \underline{61}$ |

Here $\mathit{step} = \lambda g{:}\mathsf{CNat}{\to}\mathsf{CNat}.\ \lambda n{:}\mathsf{CNat}.\ n\,[\mathsf{CNat}]\ g\ (g\ \underline{1})$, and $\mathit{ack}$ is the Ackermann function: on all $m, n \le 3$, the script matches the recursive definition $A(0, n) = n + 1$, $A(m+1, 0) = A(m, 1)$, $A(m+1, n+1) = A(m, A(m+1, n))$. The second row is self-application, which has no type in the STLC. The fourth row uses a numeral at the type $\mathsf{CNat} \to \mathsf{CNat}$, which is possible only because $\mathsf{CNat}$ can be instantiated at a type that contains $\mathsf{CNat}$.

## What it counts

The cost measure is again the number of reduction steps and the size of terms. Type abstraction and type application cost a step each in the semantics above, but they do no work at run time. The *erasure* $\mathit{erase}(t)$ removes all types, all $\Lambda\alpha$ and all $[T]$. In the pure calculus, $t$ reduces to a value exactly when $\mathit{erase}(t)$ does, with the same number of term-level beta steps, so compilers drop the types. With side effects, this needs care: $\Lambda\alpha.\,t$ is a value, so its body is not evaluated, but its erasure $t$ is. Pierce (Section 23.7) gives an erasure that keeps a dummy abstraction, and ML's [value restriction](/value-restriction/) solves the same problem.

The cost of type checking is measured in the size $n$ of the annotated term, on a word RAM.

## Relation to other models

- **STLC.** The fragment without $\forall$. System F types more terms, for example self-application above and every function in the table.
- **Hindley-Milner.** [ML's type system](/hindley-milner-type-system/) is the *predicative, prenex* fragment: $\forall$ only at the top of a type, only at `let`, and instantiated only with types that have no $\forall$. That restriction makes inference decidable. Full System F inference is undecidable.
- **Rank-$k$ fragments.** A type has rank $k$ if no $\forall$ is to the left of $k$ or more arrows, counting nesting. Rank 1 is the ML fragment. Inference is decidable at rank 2 and undecidable at every rank of 3 or more (Kfoury and Wells 1994).
- **Logic.** By the [Curry-Howard correspondence](/curry-howard-correspondence/), System F types are the formulas of second-order intuitionistic propositional logic, and the encodings above are its definitions of $\wedge$, $\vee$ and $\exists$ from $\to$ and $\forall$.
- **Extensions.** $F_\omega$ adds functions from types to types. $F_{<:}$ adds [bounded quantification](/subtyping/). The Calculus of Constructions adds [dependent types](/dependent-types/). GHC compiles Haskell to System FC, a Church-style System F with type equality coercions.
- **Implementation.** Compilers realize polymorphism either by passing type information at run time ([dictionary passing](/dictionary-passing-translation/) for type classes), by a uniform boxed representation, or by [monomorphization](/monomorphization/), which copies each polymorphic function at each type it is used.

## Known results in the model

**Strong normalization (Girard 1972).** Every well-typed term is strongly normalizing. The Tait method of the [reducibility method](/reducibility-method/) page does not work directly: $\mathrm{RED}_{\forall\alpha.T}$ would be defined from $\mathrm{RED}_{[\alpha := S]T}$ for all $S$, including $\forall\alpha.T$ itself, which is circular. Girard's fix is *reducibility candidates*: sets of terms that satisfy CR1, CR2 and CR3. Interpret a type relative to an assignment of candidates to its free type variables, and let $\forall\alpha.T$ denote the intersection of the interpretations of $T$ over all candidates for $\alpha$. This intersection is again a candidate. Then every typed term is in the interpretation of its type, and CR1 gives strong normalization (Girard, Lafont and Taylor, Chapter 14). The proof quantifies over all sets of terms, which is the impredicativity of System F reflected in the proof.

**Representable functions.** The functions $\mathbb{N} \to \mathbb{N}$ definable by closed terms of type $\mathsf{CNat} \to \mathsf{CNat}$ are exactly the functions that second-order Peano arithmetic proves total (Girard 1972; Girard, Lafont and Taylor, Chapter 15). This includes the Ackermann function and much more. It excludes the evaluator for System F itself: by a diagonal argument, no total language can define its own interpreter.

**Consistency strength.** Strong normalization of System F implies the consistency of second-order arithmetic. So by Gödel's second incompleteness theorem, it cannot be proved in second-order arithmetic.

**Parametricity (Reynolds 1983).** A polymorphic function must act the same way at every type, because it cannot inspect its type argument. Reynolds' abstraction theorem makes this precise with relations: every closed term of type $T$ preserves every relation built from the structure of $T$. Consequences, called free theorems by Wadler (1989): every closed term of type $\forall\alpha.\,\alpha \to \alpha$ behaves as the identity; every closed term of type $\forall\alpha.\,\alpha \to \alpha \to \alpha$ returns its first or its second argument; and a function of type $\forall\alpha.\,\mathsf{List}\,\alpha \to \mathsf{List}\,\alpha$ commutes with `map f` for every $f$.

**No set-theoretic model (Reynolds 1984).** There is no model of System F that interprets types as sets and $\to$ as the full set of functions. Models exist with other notions of function, for example PER models and Girard's coherence spaces.

**Type checking and inference.** For Church-style terms, type checking is decidable by one bottom-up pass, with types compared up to renaming of bound variables. For Curry-style terms, where types, $\Lambda$ and $[T]$ are erased, typability and type checking are both undecidable (Wells 1999), by a reduction from [semi-unification](/semi-unification-problem/). See [Wells' theorem](/system-f-inference-undecidability/).

**Inhabitation.** Under Curry-Howard, inhabitation of System F types is provability in second-order intuitionistic propositional logic, which is undecidable (Löb 1976). For the STLC the same problem is PSPACE-complete.

## References
