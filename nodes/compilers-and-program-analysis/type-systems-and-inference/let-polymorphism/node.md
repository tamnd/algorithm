---
tag: E10QMV
kind: concept
slug: let-polymorphism
name: Let-polymorphism
aliases:
- ML-style polymorphism
- prenex polymorphism
area: compilers-and-program-analysis/type-systems-and-inference
level: core
summary: Polymorphism where only let-bound names get type schemes, and lambda-bound names stay monomorphic, which keeps inference decidable.
prereqs: [simply-typed-lambda-calculus, type-system]
see_also: [hindley-milner-type-system, algorithm-w, value-restriction, system-f, ml-typability-dexptime-completeness, polymorphic-recursion-undecidability, monomorphization, type-classes]
sources:
  - paper: doi:10.1016/0022-0000(78)90014-4
    title: Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375
    locator: Section 1 (the motivation for polymorphism at let, with the map function as the example) and Section 4 (algorithm W)
  - paper: doi:10.1145/582153.582176
    title: Luis Damas and Robin Milner, Principal type-schemes for functional programs, Ninth ACM Symposium on Principles of Programming Languages (POPL 1982), pages 207 to 212
    locator: the rules GEN and LET, and the type schemes with the quantifiers at the outside
  - book: isbn:9780262162098
    title: Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002
    locator: Section 22.7 (let-polymorphism, typing let by substitution, the generalization step and its side condition, and the exponential cost of nested lets)
  - paper: doi:10.1007/BF01018828
    title: Andrew K. Wright, Simple imperative polymorphism, LISP and Symbolic Computation 8(4), 1995, pages 343 to 355
    locator: the value restriction, which limits generalization at let to syntactic values
---

Let-polymorphism is the form of polymorphism in ML and its relatives. A name bound by `let` gets a *type scheme* such as $\forall \alpha.\, \alpha \to \alpha$, and each use of the name may pick a different instance of it. A name bound by `fun` gets one plain type, the same at all its uses. The quantifiers of a scheme sit only at the outside, so the style is also called *prenex* or *rank-1* polymorphism. Milner (1978) chose this design because it gives reusable generic functions and still lets the compiler infer all types, with no annotations. The formal system is the [Hindley-Milner type system](/hindley-milner-type-system/).

## In plain words

When you write a helper function and give it a name with `let`, the compiler looks at its definition first. If the definition works for any kind of value, the compiler remembers it as a template. Each later use of the name can then fill the template in its own way: once with numbers, once with truth values.

A parameter of a function is different. When the compiler checks the body of the function, it cannot see what the caller will pass. So it gives the parameter one fixed type, which all uses inside the body must share.

There is one more rule. A template may only leave open the parts that do not depend on the surrounding parameters. If a part comes from an outer parameter, that part is fixed for the whole body, and the template must keep it fixed too.

## The idea

**Why `let` and not `fun`.** In `let x = e1 in e2`, the definition $e_1$ is right there. The type checker can find the most general type $\tau_1$ of $e_1$ first and then decide which of its type variables are free to vary. In `fun x -> e`, the argument is unknown when the body is checked. To let each use of `x` have its own type, the type of the function would have to be something like $(\forall \alpha.\, \alpha \to \alpha) \to \mathsf{int}$, with a quantifier inside an arrow. That is [System F](/system-f/), where inference is [undecidable](/system-f-inference-undecidability/). So the line between `let` and `fun` is the line between decidable and undecidable inference.

**Typing by copying.** A good model of the rule: `let x = e1 in e2` has a type exactly when $e_1$ has a type and the term $[x := e_1]\,e_2$, with a fresh copy of $e_1$ at each use of $x$, has a simple type (Pierce, Section 22.7). Each copy can be typed on its own, so each use gets its own type. A type scheme is a compact summary of all the types that the copies could get. Algorithms such as [algorithm W](/algorithm-w/) never make the copies. They type $e_1$ once and store the scheme.

**Generalization and the context.** After $e_1$ has the type $\tau_1$, the scheme quantifies only the type variables of $\tau_1$ that are not free in the context. A variable that is free in the context belongs to an enclosing `fun` parameter. Its value is fixed by the caller, and all uses must agree on it. Generalizing it anyway is unsound: it would type `fun x -> let y = x in y 1` with any argument type, so `(fun x -> let y = x in y 1) true` would type check, and evaluation would get stuck at `true 1`.

**Effects.** If $e_1$ can allocate a mutable reference, the copying model is wrong: the copies would create different cells, but the program creates one cell. Polymorphism on that cell is unsound. ML therefore generalizes only when $e_1$ is a syntactic value. This is the [value restriction](/value-restriction/).

**Recursion.** A recursive function is monomorphic inside its own body: the recursive calls must all use the type that is being inferred. Lifting this limit gives [polymorphic recursion](/polymorphic-recursion-undecidability/), where inference is undecidable. Haskell allows it only for functions with a written signature.

**Cost.** Copying can double the size of a type at each level of `let`. So inference for let-polymorphism is [complete for exponential time](/ml-typability-dexptime-completeness/), although programs in practice do not nest this way and inference is fast.

## Examples

**One function, two types.** In

```text
let id = fun x -> x in if id true then id 1 else 0
```

`id` gets $\forall \alpha.\, \alpha \to \alpha$, the first use is at $\mathsf{bool} \to \mathsf{bool}$, and the second at $\mathsf{int} \to \mathsf{int}$. The same body with `fun id -> ...` in place of the `let` has no type.

**A context variable stays fixed.** In `fun x -> let y = x in y`, the type of `x` is $\alpha$ and $\alpha$ is free in the context, so `y` gets $\alpha$ and not $\forall \alpha.\, \alpha$. The term has type $\alpha \to \alpha$.

**Partly generic.** In `fun x -> let k = fun y -> x in k`, the definition has type $\beta \to \alpha$, where $\alpha$ is the type of `x`. The scheme is $\forall \beta.\, \beta \to \alpha$: the argument type of `k` is free, and the result type is fixed.

**Types that double.** Let

```text
let y0 = fun x -> x in
let y1 = fun z -> z y0 y0 in
let y2 = fun z -> z y1 y1 in
...
let yk = fun z -> z y(k-1) y(k-1) in yk
```

Each use of $y_{i-1}$ is a fresh instance, so the type of $y_i$ holds two renamed copies of the type of $y_{i-1}$. The type of $y_1$ is $((a \to a) \to (b \to b) \to c) \to c$. The term has $7k + 4$ nodes, and the principal type has $8 \cdot 2^k - 5$ nodes as a tree and $2^{k+1} - 1$ type variables. So [algorithm W](/algorithm-w/) and every other inference algorithm need exponential time on this family, just to write the answer.

## Where it is used

- **Standard ML, OCaml and F#** use let-polymorphism with the value restriction. OCaml uses a relaxed form, which also generalizes type variables that occur only in covariant positions.
- **Haskell** uses it with [type classes](/type-classes/) in the schemes. The monomorphism restriction stops generalization of some class-constrained bindings without arguments. The `MonoLocalBinds` option of GHC stops generalization of local `let` bindings that mention variables of the enclosing scope.
- **Elm and PureScript** use it for top-level and local definitions. PureScript adds [row polymorphism](/row-polymorphism/).
- **Compilers** turn polymorphic functions into code by [monomorphization](/monomorphization/), as in MLton, by one uniform boxed representation, as in OCaml, or by [dictionary passing](/dictionary-passing-translation/) for type classes.

## References
