---
tag: EGE7J5
kind: algorithm
slug: closure-conversion
name: Closure conversion
aliases:
- closure representation
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Turns each function with free variables into closed code plus an environment record, so that functions can be compiled as plain code.
model: word-ram
complexity:
  vars: {n: the number of nodes of the source term}
  time: {worst: O(n^2), best: Θ(n)}
  space: {output: O(n^2), extra: O(n)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [lambda-calculus, substitution]
see_also: [lambda-lifting, defunctionalization, cps-conversion, a-normal-form, escape-analysis, zero-cfa, tracing-garbage-collection, function-inlining]
sources:
  - paper: doi:10.1093/comjnl/6.4.308
    title: Peter J. Landin, The mechanical evaluation of expressions, The Computer Journal 6(4), 1964, pages 308-320
    locator: the SECD machine, in which the value of a lambda expression is a closure made of the expression and its environment
  - paper: doi:10.1145/800055.802037
    title: Luca Cardelli, Compiling a functional language, Proceedings of the 1984 ACM Symposium on LISP and Functional Programming, pages 208-217
    locator: the abstract machine of the ML compiler, whose closures hold the code and copies of the values of the free variables
  - book: isbn:0521416957
    title: Andrew W. Appel, Compiling with Continuations, Cambridge University Press, 1992
    locator: the chapter on closure conversion, with flat and linked closures and the closure-passing calling convention
  - paper: doi:10.1145/182409.156783
    title: Zhong Shao and Andrew W. Appel, Space-efficient closure representations, Proceedings of the 1994 ACM Conference on LISP and Functional Programming, pages 150-161
    locator: closure sharing, the safe-for-space rule and the comparison of flat and linked closures
  - paper: doi:10.1145/345099.345125
    title: Zhong Shao and Andrew W. Appel, Efficient and safe-for-space closure conversion, ACM Transactions on Programming Languages and Systems 22(1), 2000, pages 129-161
    locator: the full closure conversion algorithm of SML/NJ and its measurements
  - paper: doi:10.1145/237721.237791
    title: Yasuhiko Minamide, Greg Morrisett and Robert Harper, Typed closure conversion, Proceedings of the 23rd ACM Symposium on Principles of Programming Languages (POPL 1996), pages 271-283
    locator: closure conversion as a type-preserving translation, with environments hidden by existential types, and its correctness proof by a logical relation
  - book: isbn:0521582741
    title: Andrew W. Appel, Modern Compiler Implementation in ML, Cambridge University Press, 1998
    locator: the chapter on functional programming languages, the section on closures
---

Closure conversion makes every function of a program closed. A function `fun x -> b` whose body reads variables from outside becomes a *closure*: a record that holds a closed piece of code and the values of those free variables. The code takes the record as an extra parameter, usually called `self` or `env`, and reads each free variable from it. A call `f a` becomes "fetch the code from the record `f`, and call it with `f` and `a`". After the conversion no function body refers to a variable of an enclosing function, so each function can be compiled to machine code on its own and placed anywhere in memory, and the records live in the heap. Landin (1964) introduced closures in the SECD machine. The flat form below, where each record holds copies of the values, is the one of Cardelli's ML compiler (1984) and of most compilers for functional languages since.

## In plain words

A function written inside another function often uses names from the outside, like a helper that adds a fixed amount chosen by its caller. Machine code cannot reach into another function's local names. So the compiler packs the function together with the values it needs into a small box, and changes the code to take its values out of the box. Calling the function now means: open the box, take out the code, and run it with the box and the argument. Every function becomes a plain piece of code that needs nothing from outside, and the boxes carry what is left.

## The problem

The input is a closed term of the call-by-value toy language: constants, `fun x -> e`, calls, `let`, `if`, operators and recursive functions `fix f x -> e`. The output is a term of the same language plus records: `[e0, e1, ..., em]` builds a record and `e.i` reads part $i$, counted from 0. The output must have the same outcome as the input, with a closure record in place of each function value, and every `fun` in it must be closed. The free variables of a term are those it reads but does not bind; for `fun x -> x + a + b` they are `a` and `b`.

## The algorithm

CONVERT carries a map $\rho$ that says how to read each variable that is free in the current term: as itself when it is local to the current function, or as a part `self.i` of the current record.

```pseudo id=main
CLOSURE-CONVERT(e)                         ▷ e is closed
L1  return CONVERT(e, empty map)

CONVERT(e, ρ)                              ▷ ρ maps each free variable of e to the target term that reads it
L2  if e is a variable x then return ρ(x)
L3  if e is fun x -> b, or fix f x -> b, then                                   ▷ self new
L4      y1, ..., ym ← the free variables of e, sorted
L5      ρ' ← {y1 ↦ self.1, ..., ym ↦ self.m, x ↦ x}, and f ↦ self for a fix
L6      code ← fun self -> fun x -> CONVERT(b, ρ')
L7      return [code, ρ(y1), ..., ρ(ym)]
L8  if e is e1 e2 then return let c = CONVERT(e1, ρ) in let a = CONVERT(e2, ρ) in (c.0 c) a     ▷ c, a new
L9  if e is let x = e1 in e2 then return let x = CONVERT(e1, ρ) in CONVERT(e2, ρ[x ↦ x])
L10 otherwise apply CONVERT with ρ to each part of e (constants, if, operators)
```

Line L7 builds the record in the scope where the function is defined, so it reads each free variable through the outer map $\rho$. Line L6 converts the body with the inner map $\rho'$, in which only `self` and the parameter are variables, so the code is closed. Line L8 evaluates the function before the argument, as the source does, and then passes the record itself as the first argument of its code. A recursive function needs no special record: line L5 maps its own name to `self`, the record through which it was called. So the output has no `fix` at all.

## Example

Take `let a = 1 in let b = 2 in let f = fun x -> x + a + b in f 10`. The function has the free variables `a` and `b`, so line L7 builds the record `[code, a, b]`, and the body reads `self1.1` and `self1.2`:

```
let a = 1 in let b = 2 in
let f = [fun self1 -> fun x -> x + self1.1 + self1.2, a, b] in
let c2 = f in let a3 = 10 in (c2.0 c2) a3
```

| step | term being run |
|---|---|
| 1 | the three `let`s give `f = [code, 1, 2]` |
| 2 | `(c2.0 c2) a3` with `c2 = [code, 1, 2]` and `a3 = 10` |
| 3 | `code [code, 1, 2] 10` |
| 4 | `10 + [code, 1, 2].1 + [code, 1, 2].2`, which is `10 + 1 + 2 = 13` |

For the recursive `let m = 1 in (fix f n -> if n < 1 then m else n * f (n - 1)) 5`, the free variable is `m`, and `f` becomes `self`. The record is `[code, m]`, and the recursive call inside the code is `let c4 = self3 in let a5 = n - 1 in (c4.0 c4) a5`. The result is 120 in both programs.

## Correctness

Relate a source value $v$ and a target value $w$ by $v \sim w$: equal integers, equal booleans, or a source function and a record $[\mathit{code}, w_1, \dots, w_m]$ whose code is CONVERT of that function's body and whose parts are related to the values of its free variables. The main lemma says: if every free variable $y$ of $e$ has a source value $\sigma(y)$, and $\rho(y)$ evaluates in the target to a value related to $\sigma(y)$, then $e$ with $\sigma$ substituted and CONVERT$(e, \rho)$ have related outcomes. A value result maps to a related value, stuck maps to stuck, and a run without end maps to a run without end. The proof is an induction on the evaluation, with one case per line. The call case of line L8 is the heart of it: the code receives the record as `self`, and $\rho'$ of line L5 then reads each free variable from the right part of the record. A second induction shows that the free variables of CONVERT$(e, \rho)$ are among those of the terms $\rho(y)$, so the code of line L6, with only `self` and $x$ in $\rho'$, is closed. The [proof file](proofs/correctness.md) gives both proofs.

## Complexity

The model is the word RAM, with names as small integers, and the unit step is the creation of one output node or one operation on one element of a set. Line L4 needs the free variables of each function. With one bottom-up pass that stores them, or with a fresh walk of each function, this costs $O(n)$ per function and $O(n^2)$ in all. The output is the source plus $O(1)$ nodes per call and one record part for each pair of a function and one of its free variables. That sum can reach $\Theta(n^2)$: in `fun x1 -> fun x2 -> ... fun xk -> x1 + ... + xk`, with $n = 3k - 1$ nodes, the function of $x_i$ captures $i - 1$ variables, and the records have $k(k-1)/2$ parts in all. If every function has a bounded number of free variables, time and output are $O(n)$. The recursion depth and the map $\rho$ take $O(n)$ extra space.

## Properties

- **Closed code.** Every `fun` in the output is closed, and only `self` and the parameter are free in a function body.
- **Calls are uniform.** Every call has the same shape, whatever function is called, because the record carries the code.
- **Safe for space.** A flat record holds only the free variables of its function, so the garbage collector never keeps a value alive just because some enclosing scope had it.
- **Copies.** A record holds copies of values. A variable that the program can change after the record is made must be put in a box first.

## Variants and improvements

- **Linked closures.** A record holds the free variables of its own function and a pointer to the record of the enclosing function, as in Landin's environments. Records are made faster and share data, but reading a variable follows a chain, and the chain can keep dead values alive.
- **Shared and safe-for-space closures.** Shao and Appel (1994, 2000) choose for each function between flat and shared parts, so that records are small and access is fast without keeping dead values alive.
- **Typed closure conversion.** Minamide, Morrisett and Harper (1996) give each record an existential type that hides the type of its environment, so that a typed compiler can keep types through the conversion.
- **Known functions.** A function whose every call site is known needs no record. [Lambda lifting](/lambda-lifting/) passes its free variables as extra arguments instead, and [escape analysis](/escape-analysis/) or [0-CFA](/zero-cfa/) finds the functions that can be treated this way.
- **[Defunctionalization](/defunctionalization/).** Replaces the code part of the record by a tag and every call by a case analysis on the tag, which turns the whole program into a first-order one.
- **Closure conversion after CPS.** In a compiler that first applies [CPS conversion](/cps-conversion/), continuations become closures too, and the stack frames of a normal compiler appear as continuation records.

## When to use it

Use closure conversion in a compiler for any language with first-class nested functions: ML, Haskell, Scheme, JavaScript, Rust and Java lambdas. It is the step that turns nested functions into code that a machine can run. Use it together with a cheaper path for known functions, as in most real compilers. For an interpreter that keeps environments at run time, closures appear without this transformation, as in the SECD machine.

## Pitfalls

- **Recursion.** Treating the name of a recursive function as a free variable needs a record that contains itself, which the record cannot hold when it is built. Map the name to `self`, as line L5 does.
- **Assigned variables.** Flat records copy values. If the source can assign to a captured variable, every closure and the outer function must share one box, or they see different values.
- **Order of the parts.** Lines L5 and L7 must use the same order of free variables. A different order at the two places reads the wrong value without any error.
- **Shadowing.** A `let x` or a parameter inside a function must hide an outer `x` of the same name in $\rho$, as line L9 and line L5 do.
- **Quadratic size.** Deeply nested functions copy the same variables into many records. Linked or shared records avoid this, at a cost in access time.
- **Calls through the record.** A call to a known function through its record costs a memory read and an indirect jump. Compilers call known functions directly.

## Implementations

## History

Landin (1964) defined the closure in his SECD machine: the value of a lambda expression is the pair of the expression and the environment in which it was evaluated. Cardelli (1984) described the ML compiler with flat closures that hold the code and the values of the free variables. Appel's book of 1992 presents closure conversion of the Standard ML of New Jersey compiler on a CPS intermediate language. Shao and Appel (1994) studied closure sharing and the safe-for-space rule, and gave the full algorithm in 2000. Minamide, Morrisett and Harper (1996) made the conversion type-preserving, with a proof of correctness by a logical relation.

## References
