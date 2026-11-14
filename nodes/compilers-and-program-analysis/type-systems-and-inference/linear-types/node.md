---
tag: M768SQ
kind: concept
slug: linear-types
name: Linear types
aliases:
- substructural types
- affine types
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Types whose values must be used exactly once, or at most once in the affine case, which supports safe in-place update and resources.
prereqs: [simply-typed-lambda-calculus, type-soundness, curry-howard-correspondence]
see_also: [borrow-checking, region-based-memory-management, effect-system, reference-counting, escape-analysis, separation-logic, dependent-types]
sources:
  - paper: doi:10.1016/0304-3975(87)90045-4
    title: Jean-Yves Girard, Linear logic, Theoretical Computer Science 50(1), 1987, pages 1 to 101
    locator: the sequent calculus without weakening and contraction, the linear connectives and the exponential modality
  - paper: "Philip Wadler, Linear types can change the world!, in M. Broy and C. B. Jones (eds.), Programming Concepts and Methods, IFIP TC2 Working Conference, Sea of Galilee, April 1990, North-Holland, 1990"
    title: Philip Wadler, Linear types can change the world!
    locator: the linear and nonlinear types, the array operations with destructive update, and the read-only access construct
  - book: isbn:9780262162289
    title: Benjamin C. Pierce (ed.), Advanced Topics in Types and Programming Languages, MIT Press, 2005
    locator: Chapter 1 (David Walker, Substructural type systems), the structural rules, the linear lambda calculus with qualifiers, and the ordered, affine and relevant variants
  - paper: doi:10.1145/3158093
    title: Jean-Philippe Bernardy, Mathieu Boespflug, Ryan R. Newton, Simon Peyton Jones and Arnaud Spiwack, Linear Haskell, practical linearity in a higher-order polymorphic language, Proceedings of the ACM on Programming Languages 2(POPL), 2018
    locator: linearity on the function arrow, multiplicity polymorphism, and the examples of in-place update and safe resource use
---

A linear type system requires that each variable of linear type be used *exactly once*. It is the type system that the [Curry-Howard correspondence](/curry-howard-correspondence/) gives for Girard's linear logic (1987), the logic in which a hypothesis is a resource that a proof must consume. A program can then rely on two facts: a linear value has no other reference, so it can be updated in place or freed after its use; and it cannot be forgotten, so a file or a channel must be closed. Linear types are one member of the family of *substructural* type systems, which is broader: it also contains affine types (use at most once), relevant types (use at least once) and ordered types (use exactly once, in order). Linear is not affine. Rust's ownership is affine, and the [borrow checking](/borrow-checking/) page covers how Rust adds temporary shared access on top of it.

## In plain words

In most languages you can copy a variable as often as you like, or never use it. A linear type takes away both freedoms. A variable of linear type must be used exactly one time. This turns a value into a resource, like a coin: you can spend it, or give it away, but you cannot spend it twice and you cannot lose it. The checker can then promise useful things. Since no copy of an array exists after you give it to an update function, the update can change the array in place and still behave like a pure function. Since you cannot drop a file handle, you must close it. An affine type is weaker: you may use the value once or not at all, so a forgotten file needs another way to be closed.

## The idea

### Linear logic in brief

Ordinary logic has three *structural rules* that do not mention any connective. *Exchange* lets hypotheses be used in any order. *Weakening* lets a proof ignore a hypothesis. *Contraction* lets a proof use a hypothesis twice. Linear logic drops weakening and contraction, so each hypothesis is used exactly once. Implication becomes *linear implication* $A \multimap B$ ("consume an $A$ to make a $B$"), conjunction splits into a multiplicative $A \otimes B$ (both, from separate resources) and an additive form, and the *exponential* $!A$ marks a hypothesis that may be used any number of times. Read as types, $\multimap$ is the linear function type and $\otimes$ is the linear pair.

### Syntax and typing rules

The terms are those of the [simply typed lambda calculus](/simply-typed-lambda-calculus/) with pairs:

$$T ::= B \mid T \multimap T \mid T \otimes T \qquad e ::= x \mid \lambda x.\ e \mid e_1\ e_2 \mid (e_1, e_2) \mid \mathsf{let}\ (x, y) = e_1\ \mathsf{in}\ e_2$$

A context $\Gamma$ is a finite map from variables to types. In the rules, $\Gamma_1, \Gamma_2$ is defined only when the two domains are disjoint. This *context split* is the heart of the system: the free variables of a term are divided among its parts, and none is given to two parts.

```text
-----------------  T-Var
x : T |- x : T

Gamma, x : T1 |- e : T2
-------------------------------  T-Abs
Gamma |- fun x -> e : T1 -o T2

Gamma1 |- e1 : T1 -o T2    Gamma2 |- e2 : T1
---------------------------------------------  T-App
Gamma1, Gamma2 |- e1 e2 : T2

Gamma1 |- e1 : T1    Gamma2 |- e2 : T2
---------------------------------------  T-Pair
Gamma1, Gamma2 |- (e1, e2) : T1 * T2

Gamma1 |- e1 : T1 * T2    Gamma2, x : T1, y : T2 |- e2 : T
-----------------------------------------------------------  T-LetPair
Gamma1, Gamma2 |- let (x, y) = e1 in e2 : T
```

T-Var has exactly one variable in its context, so an unused variable cannot be carried to a leaf. The three structural rules, stated as typing rules, are:

```text
Gamma1, x : T1, y : T2, Gamma2 |- e : T          Gamma |- e : T
----------------------------------------  X      ----------------------  W
Gamma1, y : T2, x : T1, Gamma2 |- e : T          Gamma, x : T1 |- e : T

Gamma, x : T1, y : T1 |- e : T
-------------------------------  C
Gamma, x : T1 |- [x/y] e : T
```

### Linear, affine, relevant and ordered

Each discipline is the rules above plus a choice of structural rules.

| Discipline | X (exchange) | W (weakening) | C (contraction) | Each variable is used |
| --- | --- | --- | --- | --- |
| Unrestricted (STLC) | yes | yes | yes | any number of times |
| Affine | yes | yes | no | at most once |
| Relevant | yes | no | yes | at least once |
| Linear | yes | no | no | exactly once |
| Ordered | no | no | no | exactly once, in the order of binding |

**Theorem (use counts).** Write $\#_x(e)$ for the number of free occurrences of $x$ in $e$. If $\Gamma \vdash e : T$, then every free variable of $e$ is in $\Gamma$, and for every $x$ in $\Gamma$:

- linear: $\#_x(e) = 1$;
- affine: $\#_x(e) \leq 1$;
- relevant: $\#_x(e) \geq 1$.

Conversely, a term that is typable in the STLC with context $\Gamma$ and meets the count condition for a discipline is typable in that discipline.

*Proof.* The first part is by induction on the derivation. T-Var gives one occurrence of its one variable. T-Abs removes $x$ from the context and binds its occurrences. T-App, T-Pair and T-LetPair give each variable to exactly one premise, so its count in the conclusion is its count in that premise, and zero in the others. X changes nothing. W adds a variable with count 0, which breaks "$= 1$" and "$\geq 1$" and keeps "$\leq 1$". C replaces two variables of counts $a \geq 1$ and $b \geq 1$ (in the relevant system) by one of count $a + b$, which breaks "$\leq 1$" and keeps "$\geq 1$". So linear derivations keep counts at exactly 1, affine ones at most 1, and relevant ones at least 1.

For the converse, follow the STLC derivation. At each rule with two premises, give each variable to the premise in whose subterm it occurs, which is possible because it occurs in at most one of them (linear and affine), or rename its occurrences apart and merge them with C afterwards (relevant). At a leaf, remove the variables that do not occur with W (affine). With all three structural rules, the counts are unrestricted and the system is the STLC. $\square$

So the difference is exact. Weakening is the rule that allows not using a value. Contraction is the rule that allows using it twice. Exchange decides whether order matters. With conditionals, both branches receive the same context, and the count is taken along each path.

### Semantics and soundness

The semantics is ordinary call-by-value reduction: $(\lambda x.\ e)\ v \longrightarrow [v/x]e$ (E-App) and $\mathsf{let}\ (x, y) = (v_1, v_2)\ \mathsf{in}\ e \longrightarrow [v_1/x][v_2/y]e$ (E-LetPair), with the usual evaluation contexts. Linearity changes the types, not the steps.

Soundness is [progress and preservation](/type-soundness/). Progress uses canonical forms as in the STLC. Preservation needs the *linear substitution lemma*: if $\Gamma_1, x : T_1 \vdash e : T$ and $\Gamma_2 \vdash v : T_1$, then $\Gamma_1, \Gamma_2 \vdash [v/x]e : T$. The resources of $v$ move to the one place where $x$ occurs. The ordinary lemma, where $v$ is typed in the same context as $e$, would be false here, because it would give the resources of $v$ to two places.

Real systems mix linear and unrestricted data. Walker (2005) puts a qualifier, `lin` or `un`, on each type, and adds the rule that an unrestricted pair or closure cannot contain a linear value; otherwise a copy of the container would copy the linear value inside it. Linear logic uses $!T$ for the same purpose, and Linear Haskell puts the multiplicity on the arrow. With these rules, a closed well-typed program holds at most one reference to each linear value at each step, which is the property that allows in-place update and freeing on use.

## Examples

**The structural rules decide.** Four terms, with $x : A$, $y : B$:

| Term | Linear | Affine | Relevant | Ordered | Why |
| --- | --- | --- | --- | --- | --- |
| `fun x -> fun y -> (x, y)` | yes | yes | yes | yes | each used once, in order |
| `fun x -> fun y -> (y, x)` | yes | yes | yes | no | needs X |
| `fun x -> fun y -> x` | no | yes | no | no | needs W for `y` |
| `fun x -> (x, x)` | no | no | yes | no | needs C for `x` |

**A file protocol.** With the operations

```text
open  : string -> file
read  : file -o (char * file)
close : file -o unit
```

where `string` and `char` are unrestricted and `file` is linear, the program `let f = open "a" in let (c, f2) = read f in close f2` is well typed. `let (c, f2) = read f in c` is not, because `f2` is never used, and `let u = close f in read f` is not, because `f` is used twice. In an affine system the first bad program is accepted. So an affine language needs another way to release the file. Rust runs the destructor (`Drop`) when an owned value goes out of scope.

**In-place update.** Following Wadler (1990), give arrays the operations `update : (arr * int * int) -o arr` and `lookup : (arr * int) -o (int * arr)`, where only the array is linear. In `let a1 = update (a0, 3, 7) in lookup (a1, 3)`, the old array `a0` cannot be used after `update`, so the implementation may write into `a0` and return it as `a1`. The program still means what the pure version means. The term `let a1 = update (a0, 3, 7) in lookup (a0, 3)` is rejected, since it uses `a0` twice. That second use is exactly the case in which an in-place write would be visible.

## Where it is used

- **Rust** is affine: a non-`Copy` value is moved on use, and the compiler rejects a use after a move. `Copy` types such as integers have contraction. Borrowing adds temporary access without a move.
- **Linear Haskell** (Bernardy et al. 2018) adds the linear arrow `a %1 -> b` to GHC, with multiplicity polymorphism so that one function can serve linear and unrestricted callers.
- **Clean** has *uniqueness types*, a close relative: a unique value has no other reference now, which is a promise about the past. A linear variable will be used once, which is a promise about the future. Clean uses uniqueness for in-place update and for I/O.
- **Session types** treat a channel endpoint as a linear value whose type changes after each message, so that a protocol is followed to the end.
- **Quantitative type theory** in Idris 2 counts uses with 0, 1 or many, combining linear and [dependent types](/dependent-types/).
- **Memory management.** A linear value can be freed when it is consumed, with no [reference counting](/reference-counting/) or tracing collector. [Region-based memory management](/region-based-memory-management/) and [separation logic](/separation-logic/) use related resource reasoning.

## References
