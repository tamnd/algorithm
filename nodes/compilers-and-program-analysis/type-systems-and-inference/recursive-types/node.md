---
tag: W2ZTM2
kind: concept
slug: recursive-types
name: Recursive types
aliases:
- equi-recursive types
- iso-recursive types
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Types of the form mu a. T that refer to themselves, for lists, trees and objects; equi-recursive types equal their unfolding, while iso-recursive types need explicit fold and unfold.
prereqs: [subtyping, simply-typed-lambda-calculus]
see_also: [subtyping, type-soundness, hopcroft-karp-equivalence, bisimulation, knaster-tarski-theorem, occurs-check, hindley-milner-type-system, dfa-minimization]
sources:
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Chapter 20 (examples of recursive types, the iso-recursive rules T-Fld and T-Unfld with E-UnfldFld, and the equi-recursive view) and Chapter 21 (metatheory of recursive types, coinduction, regular trees, and the subtyping algorithm with its termination and complexity)
  - paper: doi:10.1145/155183.155231
    title: Roberto M. Amadio and Luca Cardelli, Subtyping recursive types, ACM Transactions on Programming Languages and Systems 15(4), 1993, pages 575 to 631
    locator: the subtyping rules for recursive types, their soundness and completeness for the order on infinite trees, and the decision algorithm (POPL 1991 version)
  - paper: doi:10.1017/S0960129500000657
    title: Dexter Kozen, Jens Palsberg and Michael I. Schwartzbach, Efficient recursive subtyping, Mathematical Structures in Computer Science 5(1), 1995, pages 113 to 125
    locator: the term automaton for a recursive type and the O(n^2) subtyping algorithm by product automaton reachability (POPL 1993 version)
  - book: isbn:9780262162289
    title: Benjamin C. Pierce (ed.), Advanced Topics in Types and Programming Languages, MIT Press, 2005
    locator: Chapter 10 by Francois Pottier and Didier Remy, The essence of ML type inference (inference with recursive types by unification without the occurs check)
---

A recursive type is a type that mentions itself, written $\mu\alpha.T$, where $\alpha$ may occur in $T$. Lists of integers are $\mu\alpha.\,\mathsf{Unit} + \mathsf{Int} \times \alpha$: a list is either empty or an integer paired with another list. There are two ways to give such a type meaning. In the *equi-recursive* view, $\mu\alpha.T$ is *equal* to its unfolding $[\alpha := \mu\alpha.T]\,T$, and types are infinite regular trees. In the *iso-recursive* view, the two are only isomorphic, and the program moves between them with explicit `fold` and `unfold`. Both views keep [type soundness](/type-soundness/), but both lose termination: with recursive types, a typed program can loop.

## In plain words

Some data has a shape that contains itself. A list is either empty or an item followed by a smaller list. A tree node holds two smaller trees. To give such data a type, the type must refer to itself. There are two ways to do it. In the first, the checker treats the type and its one-step expansion as the very same type, as if the type were an endless tree written out in full. Then the programmer writes nothing extra, but the checker must compare endless trees, which it does by finding that both repeat the same finite pattern. In the second, the type and its expansion are different, and the programmer converts between them with two small operations. Most languages use the second way, and they hide the operations inside data constructors and pattern matching.

## The idea

### Syntax and the unfolding

Add type variables $\alpha$ and types $\mu\alpha.T$ to the [simply typed lambda calculus](/simply-typed-lambda-calculus/), with sums, products and records. The *unfolding* of $\mu\alpha.T$ is $[\alpha := \mu\alpha.T]\,T$. Some standard types (Pierce, Section 20.1):

- $\mathsf{IntList} = \mu\alpha.\,\mathsf{Unit} + \mathsf{Int} \times \alpha$.
- $\mathsf{Stream} = \mu\alpha.\,\mathsf{Unit} \to \mathsf{Int} \times \alpha$, a lazy infinite sequence.
- $\mathsf{Counter} = \mu\alpha.\,\{\mathit{get}{:}\mathsf{Int}, \mathit{inc}{:}\mathsf{Unit} \to \alpha\}$, an object whose methods return an object of the same type.
- $\mathsf{D} = \mu\alpha.\,\alpha \to \alpha$, the type of untyped lambda terms seen as data.

A type is *contractive* if each bound $\alpha$ occurs under at least one type constructor ($\to$, $\times$, $+$, a record) inside its $\mu$. The type $\mu\alpha.\alpha$ is not contractive: unfolding it never produces a constructor. Systems either forbid such types or treat them as a special case.

### Iso-recursive types

The type $\mu\alpha.T$ and its unfolding are different types, connected by two term forms.

```text
U = mu a. T1     Gamma |- t : [a := U] T1                  U = mu a. T1     Gamma |- t : U
-----------------------------------------  T-Fld           -----------------------------------------  T-Unfld
Gamma |- fold [U] t : U                                    Gamma |- unfold [U] t : [a := U] T1

-----------------------------------  E-UnfldFld
unfold [U] (fold [U] v) --> v
```

with congruence rules for `fold` and `unfold`, and `fold [U] v` as a new form of value. Canonical forms for $\mu$ types says that a closed value of type $U$ is a `fold`, so progress still holds. In ML and Haskell, each `datatype` or `data` declaration is an iso-recursive type: the constructor `Cons` is `fold` after an injection, and a pattern match on `Cons` is `unfold` followed by a case. The programmer never writes `fold` or `unfold`, and the type checker stays simple, because it compares types by name.

### Equi-recursive types

The type $\mu\alpha.T$ *is* its unfolding. No term forms are added. The typing rules are those of the STLC, but the equality of types used in T-App and elsewhere is equality of the infinite trees that the types unfold to. For example $\mu\alpha.\,\mathsf{Int} \to \alpha$ and $\mu\beta.\,\mathsf{Int} \to \mathsf{Int} \to \beta$ are equal: both unfold to the infinite tree $\mathsf{Int} \to \mathsf{Int} \to \mathsf{Int} \to \cdots$.

The infinite tree of a contractive type is *regular*: it has finitely many distinct subtrees, at most the number of subterms of the type. So a type is a finite automaton, with one state per subterm, a label per state (the constructor), and one transition per child position. Two types are equal if and only if their automata accept the same tree, which is a [bisimulation](/bisimulation/) between the states. Equality is the greatest fixed point of the one-step matching relation, so it is proved by coinduction ([Knaster-Tarski](/knaster-tarski-theorem/)). It can be decided with the union-find method of [Hopcroft and Karp](/hopcroft-karp-equivalence/) in $O(n\,\alpha(n))$ time, or by [minimizing](/dfa-minimization/) the automaton to a canonical form.

### Subtyping

With [subtyping](/subtyping/), the order on infinite trees is again a greatest fixed point. Amadio and Cardelli (1993) gave rules and a decision procedure. The algorithm keeps a set $A$ of pairs it is already trying to prove. To check $S <: T$: if $(S, T) \in A$, succeed; if either side is a $\mu$, add $(S, T)$ to $A$ and check the unfoldings; otherwise compare the constructors as in the ordinary rules, contravariant in function arguments. The set $A$ stops the unfolding loop, and it is sound because the relation is coinductive: a pair met again on a cycle may be assumed. Kozen, Palsberg and Schwartzbach (1995) build the product of the two term automata and reduce subtyping to the reachability of a "bad" pair of states, which gives an $O(n^2)$ algorithm.

For the iso-recursive view, the classic rule is the *Amber rule*: if $\alpha <: \beta$ implies $S <: T$, then $\mu\alpha.S <: \mu\beta.T$. It is sound, but its metatheory is subtle: a direct proof that the Amber rules are transitive is hard, and later work gives simpler equivalent rules.

### Type inference

For inference with equi-recursive types, drop the [occurs check](/occurs-check/) from unification. The equation $\alpha = \alpha \to \beta$ then has the solution $\alpha = \mu\gamma.\gamma \to \beta$. Unification of regular trees with union-find runs in near-linear time, so inference stays as cheap as for simple types. OCaml has this as the `-rectypes` option. It is off by default, because it makes many wrong programs typable, with strange types, instead of rejecting them.

### What is lost: termination

Every term of the pure untyped lambda calculus becomes typable with the equi-recursive type $\mathsf{D} = \mu\alpha.\alpha \to \alpha$. So strong normalization fails, and so does the logical reading of the [Curry-Howard correspondence](/curry-howard-correspondence/): a looping term has every type. The negative occurrence of $\alpha$ in $\alpha \to \alpha$ is the cause. Proof assistants allow only *strictly positive* recursive types, where the type being defined never occurs to the left of an arrow. Then termination and consistency come back.

## Examples

A script with the coinductive algorithm above checks the claims in this section.

**Equal types with different text.** $\mu\alpha.\,\mathsf{Int} \to \alpha$ and $\mu\beta.\,\mathsf{Int} \to \mathsf{Int} \to \beta$ are equal: the algorithm proves both subtype directions. $\mu\alpha.\,\mathsf{Int} \to \alpha$ and $\mu\gamma.\,\mathsf{Bool} \to \gamma$ are not: the first arguments differ.

**Self-application.** With $\mathsf{D} = \mu\alpha.\alpha \to \alpha$, the script confirms $\mathsf{D} = \mathsf{D} \to \mathsf{D}$ in the equi-recursive view. So $\lambda x{:}\mathsf{D}.\ x\ x$ has type $\mathsf{D} \to \mathsf{D}$, which is $\mathsf{D}$: in T-App, $x$ is used at type $\mathsf{D} \to \mathsf{D}$ and its argument has type $\mathsf{D}$. Then $\Omega = (\lambda x{:}\mathsf{D}.\,x\,x)\,(\lambda x{:}\mathsf{D}.\,x\,x)$ has type $\mathsf{D}$, and it steps to itself forever. In the iso-recursive view, the same term is $\lambda x{:}\mathsf{D}.\ (\mathsf{unfold}\ [\mathsf{D}]\ x)\ x$, and its argument must be wrapped in `fold`.

**A fixed-point combinator.** For each type $T$, the call-by-value fixed-point combinator $\mathit{fix}_T = \lambda f{:}T{\to}T.\ (\lambda x{:}A.\ f\,(\lambda y{:}T_1.\ x\,x\,y))\,(\lambda x{:}A.\ f\,(\lambda y{:}T_1.\ x\,x\,y))$, with $T = T_1 \to T_2$ and $A = \mu\alpha.\,\alpha \to T$, has type $(T \to T) \to T$ in the equi-recursive view. Pierce (Section 20.1) gives the version without the inner $\lambda y$, which is for call by name. Under call by value, the inner $\lambda y$ delays the evaluation of $x\,x$, which would otherwise loop before $f$ is ever called. So general recursion needs no built-in `fix` once recursive types exist.

**Subtyping of recursive records.** Let $L_2 = \mu\alpha.\{x{:}\mathsf{Int}, y{:}\mathsf{Int}, \mathit{next}{:}\alpha\}$ and $L_1 = \mu\beta.\{x{:}\mathsf{Int}, \mathit{next}{:}\beta\}$. The algorithm proves $L_2 <: L_1$: after one unfolding of each side, width subtyping handles $y$, and the pair $(L_2, L_1)$ meets itself again at $\mathit{next}$, where the assumption set closes the cycle. It rejects $L_1 <: L_2$, because $L_1$ has no field $y$.

**ML lists.** In OCaml, `type intlist = Nil | Cons of int * intlist` is iso-recursive. The expression `Cons (1, Nil)` is `fold` applied to the second injection of the pair, and `match l with Cons (h, t) -> ...` unfolds `l` and does a case on the sum.

## Where it is used

- **Algebraic data types** in ML, Haskell, Rust, Swift and Scala are iso-recursive types with names. Type equality is by name, so the checker never compares infinite trees.
- **Structural object types** in OCaml, and recursive type aliases in TypeScript, are equi-recursive. Their checkers compare regular trees.
- **Typed assembly and intermediate languages**, where objects and closures have recursive types, often use the iso-recursive view because `fold` and `unfold` are free at run time and keep the checker simple.
- **Session types** for communication protocols, and types for XML schemas, are recursive types whose equality and subtyping are decided on regular trees.
- **Program analysis.** Unification without the occurs check is the basis of some points-to analyses, where the type of a pointer may point to itself.

## References
