---
tag: WSCAQ1
kind: algorithm
slug: k-cfa
name: k-CFA
aliases:
- Shivers k-CFA
- k-limited control flow analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Control flow analysis of higher-order programs that keeps a separate binding of each variable for each string of the last k call sites.
solves: [call-graph-construction]
model: word-ram
complexity:
  vars: {n: the number of nodes of the program, k: the length of the call strings}
  time: {worst: 2^O((k+1) n log n)}
  space: {extra: 2^O((k+1) n log n)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: true}
history:
  year: 1991
  people: [Olin Shivers]
  note: Shivers defined the k-CFA hierarchy in his 1991 thesis, after the 0-CFA and 1-CFA analyses of his PLDI 1988 paper.
prereqs: [zero-cfa, context-sensitivity]
see_also: [k-cfa-exptime-completeness, object-sensitivity, call-graph-construction, cfl-reachability, abstract-interpretation, pushdown-system]
sources:
  - paper: "Olin Shivers, Control-flow analysis of higher-order languages, PhD thesis, Carnegie Mellon University, CMU-CS-91-145, 1991"
    locator: the definition of the k-CFA hierarchy by abstract interpretation of a CPS semantics with contours of the last k call sites
  - paper: doi:10.1145/53990.54007
    title: Olin Shivers, Control flow analysis in Scheme, Proceedings of PLDI '88, 164 to 174, 1988
    locator: the first control flow analyses, 0-CFA and 1-CFA, for Scheme
  - paper: doi:10.1145/1411204.1411243
    title: David Van Horn and Harry G. Mairson, Deciding kCFA is complete for EXPTIME, Proceedings of ICFP 2008, 275 to 282
    locator: the EXPTIME-completeness of k-CFA for every k at least 1
  - paper: doi:10.1145/1806596.1806631
    title: Matthew Might, Yannis Smaragdakis and David Van Horn, Resolving and exploiting the k-CFA paradox, Proceedings of PLDI 2010, 305 to 315
    locator: why k-CFA is polynomial for object-oriented programs, and m-CFA, a polynomial hierarchy for functional programs
  - book: "Flemming Nielson, Hanne Riis Nielson and Chris Hankin, Principles of Program Analysis, Springer, 1999"
    locator: chapter 3, constraint-based analysis, with the section on adding context information (uniform k-CFA)
---

k-CFA is a family of control flow analyses for higher-order programs, one for each $k \ge 0$. Like [0-CFA](/zero-cfa/), it finds the functions that each expression may evaluate to, which gives a [call graph](/call-graph-construction/). Unlike 0-CFA, it binds each variable separately for each *contour*, the string of the last $k$ call sites that led to the binding. A closure records the contour of each of its free variables. For $k = 0$ there is one contour, and k-CFA is 0-CFA. For $k \ge 1$ the answers are more precise, but the number of abstract closures can be exponential, and deciding k-CFA is EXPTIME-complete ([the k-CFA theorem](/k-cfa-exptime-completeness/)).

## In plain words

0-CFA gives each variable one bag of functions for the whole program. If a helper such as `id` is called in two places, both arguments land in the same bag, and both callers get both back. k-CFA gives each variable one bag per context. The context of a binding is the list of the last k call sites on the way to it. With k = 1, the call `id f` at one place and `id g` at another use different bags, so each caller only gets its own function back. A function value also remembers the context of each variable it uses. More contexts mean more precise answers, but the number of these remembered contexts can explode.

## The problem

The input is a closed term of the toy language of the [0-CFA](/zero-cfa/) page and a number $k \ge 0$. A contour $\delta$ is a sequence of at most $k$ application labels. A call at application $t$ in contour $\delta$ runs the body in the contour $\mathrm{next}(\delta, t)$, the last $k$ elements of $\delta$ followed by $t$. A `let` binds in the current contour. An abstract environment $ce$ maps the free variables of a node to contours, and an abstract closure is a pair $(\lambda, ce)$.

The output is the least analysis $(T, C, R)$ where $T$ is a set of tasks $(t, ce, \delta)$ (the ways node $t$ may be evaluated), $C[(t, \delta)]$ is a set of abstract closures for each node and contour, and $R[(b, \delta)]$ is one for each binder and contour, closed under the rules of lines L6 to L15. The call graph forgets the contours: $(t, \lambda)$ is an edge when some closure of $\lambda$ is in $C[(t_1, \delta)]$ for the operator $t_1$ of $t$.

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | tasks, and maps from (node, contour) and (binder, contour) to sets of abstract closures |
| order | inclusion in all parts (bottom is precise) |
| join | union in all parts |
| bottom and top | everything empty, and every task with every set full |
| boundary value | the task of the root, with the empty environment and the empty contour |
| initial value | the root task only |
| transfer | the rules below; monotone, and not distributive, since a call needs both a closure and its task |

## The algorithm

```pseudo id=main
K-CFA(e, k)
L1  label e; T <- {(root, {}, ())}
L2  repeat
L3      for each task (t, ce, d) in T do RULE(t, ce, d)
L4  until the last pass added no task and no set element
L5  return C and R

RULE(t, ce, d)
L6  if t is a variable x with binder b then add R[(b, ce(x))] to C[(t, d)]
L7  if t is a function then add the closure (t, ce) to C[(t, d)]
L8  if t is let x = t1 in t2 then TASK(t1, ce, d); add C[(t1, d)] to R[(x, d)]; TASK(t2, ce[x -> d], d); add C[(t2, d)] to C[(t, d)]
L9  if t is if or an operator then TASK each subterm with (ce, d); for if, add C[(t2, d)] and C[(t3, d)] to C[(t, d)]
L10 if t is t1 t2 then TASK(t1, ce, d); TASK(t2, ce, d)
L11     for each closure (λ, ce') in C[(t1, d)] do
L12         d' <- the last k labels of d followed by t
L13         add C[(t2, d)] to R[(param(λ), d')]; for fix f x -> body, add (λ, ce') to R[(f, d')]
L14         TASK(body(λ), ce' with the parameters mapped to d', d')
L15         add C[(body(λ), d')] to C[(t, d)]

TASK(t, ce, d)
L16 add (t, ce restricted to the free variables of t, d) to T
```

A task is one way that a node may be evaluated: with which contours for its free variables and in which current contour. Line L16 restricts the environment to the free variables, so two tasks that differ only in variables the node does not use are one task. Line L6 looks up the contour of $x$ in the environment, not the current contour, because $x$ may have been bound by an outer function in an older call. The loop of lines L2 to L4 applies every rule again until nothing changes. A worklist with dependencies, as on the 0-CFA page, gives the same result faster.

## Example

The program of the 0-CFA page:

```
let id = fun x -> x in
let a = id (fun y -> y + 1) in     // call site s1
let b = id (fun z -> z * 2) in     // call site s2
a 3                                // call site s3
```

With $k = 1$, the two calls of `id` run its body in different contours.

| fact | 1-CFA | 0-CFA |
|---|---|---|
| $x$ | in contour $[s_1]$: $\lambda_y$; in contour $[s_2]$: $\lambda_z$ | $\lambda_y, \lambda_z$ |
| body `x` of `id` | in $[s_1]$: $\lambda_y$; in $[s_2]$: $\lambda_z$ | $\lambda_y, \lambda_z$ |
| $a$ | $\lambda_y$ | $\lambda_y, \lambda_z$ |
| $b$ | $\lambda_z$ | $\lambda_y, \lambda_z$ |
| targets of s3 | $\lambda_y$ | $\lambda_y, \lambda_z$ |

1-CFA finds exactly the calls of the run. Now wrap `id` in another function:

```
let id = fun x -> x in
let g = fun w -> id w in           // call site s0 inside g
let a = g (fun y -> y + 1) in      // s1
let b = g (fun z -> z * 2) in      // s2
a 3
```

With $k = 1$, $w$ is split by $[s_1]$ and $[s_2]$, but both calls of `id` happen at $s_0$, so $x$ has the single contour $[s_0]$ and gets both functions back. `a 3` again has two targets. With $k = 2$, the contours of $x$ are $[s_1, s_0]$ and $[s_2, s_0]$, and the spurious target goes away. Every extra layer of wrappers needs one more unit of $k$.

## Correctness

**Least solution.** Every task and every element that a pass adds is the conclusion of one of the rules, applied to facts that are already forced. So by induction the result is inside every closed analysis. The loop stops only after a pass in which every rule held, so the result is closed. Termination holds because there are finitely many contours, abstract closures and tasks.

**Soundness.** Instrument the run with contours: a call at $t$ in contour $\delta$ runs the body in $\mathrm{next}(\delta, t)$, and each binding stores the contour in which it was made. The abstraction of a closure keeps its function and the contours of its free variables. By induction on the evaluation, if node $t$ is evaluated in contour $\delta$ with environment $\rho$, then its task is in $T$, and the abstraction of its value is in $C[(t, \delta)]$. The step for a call uses that the concrete and the abstract contour of the callee are both $\mathrm{next}(\delta, t)$. So every call of the run is in the call graph. The full proofs are in the proof file.

## Complexity

**Proved.** With $n$ nodes there are at most $N \le (n+1)^k$ contours. An abstract closure maps up to $n$ free variables to contours, so there are at most $n N^n$ of them, and as many tasks times $N$. Each pass of the loop adds at least one fact, and each pass costs a polynomial in these numbers. So the time is $2^{O((k+1) n \log n)}$, which is $2^{O(n \log n)}$ for fixed $k \ge 1$. For $k = 0$ every closure has the one empty contour, and the time is polynomial.

**Stated in the literature.** Van Horn and Mairson (2008) prove that deciding whether a closure flows to an expression under k-CFA is EXPTIME-complete for every $k \ge 1$. Since P is not EXPTIME, by the time hierarchy theorem, no polynomial algorithm exists. Might, Smaragdakis and Van Horn (2010) show that the same idea is polynomial for object-oriented programs, where a closure (an object) copies its free values into fields instead of capturing an environment, and they define m-CFA, a polynomial analysis for functional programs with flat environments.

**Measured, not proved.** On 400 random closed terms (seed 1991), $k = 0$ gives exactly the result of a plain 0-CFA. On 300 random terms (seed 2007), forgetting the contours, 2-CFA is inside 1-CFA and 1-CFA is inside 0-CFA. On 1500 random terms (seed 1988), every closure, binding and call of a concrete run with contours is in the result for $k = 1$ and $k = 2$.

## Properties

- **Polyvariant.** One variable has many abstract bindings, one per contour.
- **The environment problem.** A closure keeps one contour per free variable, and these can differ. This is the source of the exponential number of abstract closures, and of the EXPTIME hardness.
- **Not distributive.** A call rule fires only for closures that reach the operator in the same contour.
- **More precise as $k$ grows, in practice.** In the tests, larger $k$ never gave a larger projected result. With the "last $k$" truncation, the contours of $k + 1$ map onto those of $k$ by dropping the oldest site, which is why this holds.
- **Call strings are functional k-CFA only here.** In a first-order or object-oriented setting, a call-string analysis of length $k$ has no environment problem and is polynomial. Calling that "k-CFA" hides the difference.

## Variants and improvements

- **Uniform k-CFA.** Nielson, Nielson and Hankin index both the cache and the environment by the same contour of the current call. It is the form used on this page.
- **m-CFA.** Might, Smaragdakis and Van Horn keep only the top $m$ stack frames and use flat environments, where all free variables of a closure share one contour. It is polynomial for fixed $m$.
- **Object sensitivity.** In object-oriented analysis, contexts made of receiver allocation sites often work better than call sites ([object sensitivity](/object-sensitivity/)).
- **Pushdown analyses.** CFA2 and related analyses match calls with returns, like a [pushdown system](/pushdown-system/), so a return never goes to the wrong caller, even with $k = 0$.
- **Abstract machines.** Van Horn and Might derive k-CFA by bounding the store of an abstract machine, which gives the same analysis for richer languages.

## When to use it

Use 1-CFA, or 2-CFA at most, when 0-CFA mixes the uses of small higher-order helpers and the extra precision pays off, for example to inline or specialize closures in a compiler for a functional language. Large $k$ rarely pays. For big programs, prefer a polynomial analysis: m-CFA, a pushdown analysis, or, in object-oriented code, call-site or [object-sensitive](/object-sensitivity/) points-to analysis, which are polynomial for fixed $k$.

## Pitfalls

- **Looking up a variable in the current contour.** A version of line L6 that reads $R[(b, d)]$ instead of $R[(b, ce(x))]$ is unsound. In `let f = fun x -> fun y -> x in (f 1) 2`, the inner body runs in the contour of the call `(f 1) 2`, but $x$ was bound in the contour of `f 1`. Line L6 must use the contour that the closure environment records.
- **Dropping the environment of closures.** If line L7 stores only the function $t$, line L14 has no contours for the free variables of the body. Keep the restricted environment $ce$ in the closure.
- **Keeping the first $k$ call sites.** A version of line L12 that keeps the oldest $k$ labels makes all deep calls share one contour. Line L12 must keep the most recent $k$ labels.
- **Expecting polynomial time for fixed $k$.** For $k \ge 1$ the problem is EXPTIME-complete, and real programs can show the blow-up. Bound the time, or use m-CFA.

## Implementations

## History

Shivers introduced control flow analysis for Scheme in 1988, with 0-CFA and 1-CFA, and defined the k-CFA hierarchy in his 1991 thesis by abstract interpretation of a continuation-passing semantics. Nielson, Nielson and Hankin (1999) gave a constraint-based uniform form in their textbook. For years it was believed that k-CFA was polynomial for fixed $k$. Van Horn and Mairson (2008) proved that it is EXPTIME-complete for every $k \ge 1$, by encoding a Turing machine with exponential time in the closures of a program. Might, Smaragdakis and Van Horn (2010) explained why the same idea is polynomial for object-oriented programs and used it to define m-CFA.

## References
