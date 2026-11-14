---
tag: ZHK5BH
kind: algorithm
slug: lambda-lifting
name: Lambda lifting
aliases:
- Johnsson lambda lifting
area: compilers-and-program-analysis/intermediate-representations
level: core
summary: Moves local functions to the top level and passes their free variables as extra parameters at each call.
model: word-ram
complexity:
  vars: {n: the number of nodes of the source term}
  time: {worst: O(n^3), best: Θ(n)}
  space: {output: O(n^2), extra: O(n^2)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [lambda-calculus, substitution, transitive-closure]
see_also: [closure-conversion, defunctionalization, cps-conversion, graph-reduction, combinatory-logic, function-inlining, partial-evaluation, strongly-connected-components]
sources:
  - paper: doi:10.1007/3-540-15975-4_37
    title: Thomas Johnsson, Lambda lifting, transforming programs to recursive equations, Functional Programming Languages and Computer Architecture (FPCA 1985), LNCS, pages 190-203
    locator: the algorithm, with the extra parameters of mutually recursive functions found as the least solution of a set of equations
  - paper: doi:10.1145/800068.802129
    title: R. J. M. Hughes, Super-combinators, a new implementation method for applicative languages, Proceedings of the 1982 ACM Symposium on LISP and Functional Programming, pages 1-10
    locator: the translation of a program into supercombinators, closed functions that are applied to their free variables
  - paper: doi:10.7146/brics.v11i12.21837
    title: Olivier Danvy and Ulrik P. Schultz, Lambda-lifting in quadratic time, BRICS Report Series RS-04-12, 2004
    locator: the analysis of the cubic cost of the equations, and an algorithm that solves them in quadratic time with strongly connected components of the call graph
  - paper: "Olivier Danvy and Ulrik P. Schultz, Lambda-lifting in quadratic time, Journal of Functional and Logic Programming, 2004"
    title: Olivier Danvy and Ulrik P. Schultz, Lambda-lifting in quadratic time, Journal of Functional and Logic Programming, 2004
    locator: the journal version of the quadratic-time algorithm
  - paper: "Olivier Danvy and Ulrik P. Schultz, Lambda-lifting in quadratic time, Functional and Logic Programming (FLOPS 2002), LNCS"
    title: Olivier Danvy and Ulrik P. Schultz, Lambda-lifting in quadratic time, Sixth International Symposium on Functional and Logic Programming (FLOPS 2002), LNCS
    locator: the conference version, whose algorithm takes O(n^2 log n) time
---

Lambda lifting turns a program with nested functions into a set of global functions that are all closed. A local function that reads variables of an enclosing scope gets those variables as extra parameters, and every place that names the function passes them. After the transformation no function is nested in another, so the program is a set of recursive equations, one per function. Hughes (1982) used this idea to compile functional programs to supercombinators. Johnsson (1985) gave the algorithm with its main difficulty solved: a function must also receive the free variables of every function that it calls, and with mutual recursion these sets depend on each other.

## In plain words

A helper function written inside another function often uses names of the outer function. The compiler moves the helper out to the top level and adds those names to its list of parameters. Each call of the helper now hands over the values it needs. If the helper calls a second helper that needs more values, the first helper must take those values too, so that it can pass them on. When helpers call each other in a circle, the compiler repeats this until no helper needs anything new. At the end every function stands alone and reads only its own parameters.

## The problem

The input is a closed term of the call-by-value toy language: constants, `fun x -> e`, calls, `let`, `if`, operators, recursive functions `fix f x -> e`, and groups of mutually recursive functions `letrec f1 x1 = e1 and ... and fk xk = ek in e`. The output is a set of global definitions `F p1 ... pk x = body` and a main term. No body and no main term may contain a `fun`, a `fix` or a `letrec`. Every variable in a body must be one of its parameters, and the main term must be closed. The program must have the same outcome as the input. A global applied to fewer arguments than it has parameters is a value, a partial application, and it takes the place of a function value of the source.

## The algorithm

For a function $f$, let $D(f)$ be its free variables that are not names of functions, and $R(f)$ the functions whose names are free in $f$. The extra parameters $E(f)$ must satisfy $E(f) \supseteq D(f) \cup \bigcup_{g \in R(f)} E(g)$, because $f$ calls each $g$ and must pass $E(g)$. The least solution is the union of $D(g)$ over all $g$ that $f$ reaches along $R$, which line L4 computes.

```pseudo id=main
LAMBDA-LIFT(e)                                 ▷ e is closed
L1  rename every bound variable of e apart, and give each function f a new global name F
L2  for each function f: D(f) ← free variables of f that name no function; R(f) ← functions named free in f
L3  for each function f
L4      E(f) ← the union of D(g) over every g reachable from f along R, f included
L5      params(f) ← E(f), sorted
L6  for each function f = fun x -> b, or fix f x -> b, or a member f x = b of a letrec
L7      define F params(f) x = LIFT(b)
L8  return the definitions and LIFT(e)

LIFT(e)
L9  if e is a variable that names a function g, return G params(g); otherwise return e
L10 if e is a function f, return F params(f)
L11 otherwise apply LIFT to each part of e; a letrec becomes LIFT of its body
```

Line L1 makes every binder unique, so that adding a parameter never captures a name. Line L9 replaces each use of a function name by the global applied to the extra parameters, which is a value. Line L10 does the same for an anonymous function at the place where it is defined. The extra parameters at those places are in scope, because each variable in $E(f)$ is bound around the definition of $f$ or around a function that $f$ reaches, and those binders enclose the use.

## Example

Take `let a = 1 in (fix f x -> if x < 1 then a else (fun y -> f y + x) (x - 1)) 3`, whose value is 7. Line L1 names the outer function `F2` and the inner `fun y` `F5`, and renames `a`, `x` and `y` to `a1`, `x4` and `y6`.

| function | $D$ | $R$ | $E$ |
|---|---|---|---|
| `F2` (`fix f x`) | `a1` | none | `a1` |
| `F5` (`fun y`) | `x4` | `F2` | `x4`, `a1` |

The inner function does not read `a`, but it calls `f`, which needs `a`, so line L4 adds `a1` to it. The output is:

```
F2 a1 x4    = if x4 < 1 then a1 else F5 a1 x4 (x4 - 1)
F5 a1 x4 y6 = F2 a1 y6 + x4
main        = let a1 = 1 in F2 a1 3
```

Its value is also 7. With mutual recursion the need for line L4 is plainer. In `let d = 1 in letrec f n = if n < 1 then 0 else g n and g n = h n and h n = 1 + f (n - d) in f 3`, only `h` reads `d`, but `g` calls `h` and `f` calls `g`. Line L4 gives all three the parameter `d`. With only $D$, `g` would have to pass `d` to `h` without having it, and the program would get stuck.

## Correctness

Two facts carry the proof. The first is that the output is well scoped. If $g \in R(f)$, every function that $g$ reaches is also reached by $f$, so $E(g) \subseteq E(f)$, and the call of line L9 inside the body of $f$ passes only parameters of $f$. For a function $\psi$ defined inside the body of $f$, each variable of $E(\psi)$ is a parameter of $f$ or is bound by a `let` around $\psi$ inside that body. The second fact is a simulation. Relate a source function value made from function $f$ to the partial application $F\ w_1 \dots w_k$ when each $w_i$ is related to the value of the $i$-th extra parameter, and relate equal constants. An induction on the evaluation, with one case per form, shows that a source term with related values put in for its free variables, and its LIFT, have related outcomes: equal constants, related functions, stuck in both, or no end in both. The call case uses the first fact: the full application $F\ w_1 \dots w_k\ a$ steps to the body with exactly the values that the source closure held. The [proof file](proofs/correctness.md) gives both proofs.

## Complexity

The model is the word RAM, with names as small integers, and the unit step is the creation of one output node or one operation on one element of a set. Let $m \le n$ be the number of functions. Line L2 walks each function once, $O(n)$ each and $O(n^2)$ in all. For each function, line L4 walks the graph $R$, which has at most $m^2$ edges, and unites at most $m$ sets of at most $n$ variables, so $O(n^2)$ per function and $O(n^3)$ in all. The output adds at most $n$ arguments at each of at most $n$ places, $O(n^2)$, and that is reached: in `fun x1 -> fun x2 -> ... fun xk -> x1 + ... + xk` the function of $x_i$ gets $i - 1$ extra parameters. A term without functions takes $\Theta(n)$. The sets $E$ take $O(n^2)$ extra space. Danvy and Schultz solve the equations of line L4 in $O(n^2)$ time with the strongly connected components of $R$.

## Properties

- **First order in form.** Every function is global and closed, so a compiler can give each one a fixed address and no environment.
- **Function values remain.** A local function that escapes becomes a partial application, which the target still has to represent at run time, for example as a record of the global and its arguments.
- **No change to the order of evaluation.** Extra arguments are variables, so passing them does no work and cannot diverge.
- **Same number of calls.** Every source call is one target call with more arguments.

## Variants and improvements

- **Quadratic time.** Danvy and Schultz group the functions of $R$ into strongly connected components, give all members of a component the same set, and process the components in topological order. Their conference version of 2002 takes $O(n^2 \log n)$ time; the 2004 versions take $O(n^2)$.
- **Lambda dropping.** The inverse transformation moves global functions back into the scope of their callers and removes the parameters that are the same at every call. Danvy and Schultz study it together with lifting.
- **Selective lifting.** Compilers such as GHC lift only functions whose extra parameters are few, and keep the others as closures, because many extra arguments cost registers at every call.
- **Supercombinators.** Hughes also lifts maximal free subexpressions, not only variables, so that work inside a function body can be shared between calls.

## When to use it

Use lambda lifting when the target has global functions but no nested ones: the code generators of graph reduction machines, C as a target, and the equations of a partial evaluator. Use it for local functions whose every call site is known, where it avoids allocating a closure. For functions that escape and have many free variables, [closure conversion](/closure-conversion/) is usually cheaper, because it builds the record once and does not pass every variable at every call.

## Pitfalls

- **Mutual recursion.** The extra parameters of mutually recursive functions depend on each other. Taking only the variables that each function reads leaves calls that must pass values the caller does not have. Compute the least fixed point, as line L4 does by reachability.
- **Calls through names.** A function must also get the free variables of every function it calls, not only of functions it defines inside it, as `F5` in the example shows.
- **Name capture.** Adding a parameter named `a` to a function whose body has its own `a` changes the meaning. Rename all binders apart first, as line L1 does.
- **Order of extra parameters.** The definition and every call must list them in the same order. Line L5 fixes one order per function.
- **Assigned variables.** Passing a variable as an argument copies its value. A variable that the source can assign to must be put in a box before lifting.
- **Cost of many parameters.** Deep nesting gives $\Theta(n^2)$ output, and functions with many free variables make every call slow.

## Implementations

## History

Hughes (1982) introduced supercombinators: closed functions, applied to their free variables, into which a functional program can be translated for graph reduction. Johnsson (1985) defined lambda lifting as the translation of block-structured programs into recursive equations, and set up the equations for the extra parameters of mutually recursive functions. Danvy and Schultz showed that the usual way to solve these equations is cubic, and gave an algorithm in $O(n^2 \log n)$ time at FLOPS 2002 and in $O(n^2)$ time in the 2004 versions of the paper.

## References
