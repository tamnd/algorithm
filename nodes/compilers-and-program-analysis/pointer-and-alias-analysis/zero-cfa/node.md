---
tag: JG6AT6
kind: algorithm
slug: zero-cfa
name: 0-CFA
aliases:
- zeroth-order control flow analysis
- monovariant control flow analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: core
summary: Find the functions that each expression of a higher-order program may evaluate to, with one abstract binding per variable, in cubic time.
solves: [call-graph-construction]
model: word-ram
complexity:
  vars: {n: the number of nodes of the program}
  time: {worst: O(n^3)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 1988
  people: [Olin Shivers]
  note: Shivers named control flow analysis and described 0-CFA for Scheme at PLDI 1988, and developed it in his 1991 thesis.
prereqs: [lambda-calculus, call-graph-construction]
see_also: [k-cfa, k-cfa-exptime-completeness, andersen-analysis, closure-conversion, defunctionalization, cfl-reachability, abstract-interpretation]
sources:
  - paper: doi:10.1145/53990.54007
    title: Olin Shivers, Control flow analysis in Scheme, Proceedings of PLDI '88, 164 to 174, 1988
    locator: the first statement of control flow analysis for higher-order programs
  - paper: "Olin Shivers, Control-flow analysis of higher-order languages, PhD thesis, Carnegie Mellon University, CMU-CS-91-145, 1991"
    locator: the definition of 0-CFA and 1-CFA by abstract interpretation of a CPS semantics
  - paper: doi:10.1145/200994.201001
    title: Jens Palsberg, Closure analysis in constraint form, ACM Transactions on Programming Languages and Systems 17(1), 47 to 62, 1995
    locator: the constraint form of 0-CFA and its equivalence with the abstract interpretation form
  - paper: doi:10.1109/LICS.1997.614960
    title: Nevin Heintze and David McAllester, On the cubic bottleneck in subtyping and flow analysis, Proceedings of LICS 1997, 342 to 351
    locator: the reduction from 2NPDA recognition to flow analysis, which explains why no sub-cubic algorithm is known
  - paper: doi:10.1007/978-3-540-69166-2_17
    title: David Van Horn and Harry G. Mairson, Flow analysis, linearity, and PTIME, Static Analysis Symposium 2008, LNCS 5079, 255 to 269
    locator: the proof that 0-CFA is complete for PTIME
---

0-CFA is the simplest control flow analysis for higher-order programs. In a language where functions are values, the function that a call `f x` runs depends on the value of `f`, so [call graph construction](/call-graph-construction/) needs to know which functions can flow into which expressions. 0-CFA answers this with one set of functions for each expression and one for each variable, the same for all calls of the enclosing function. It writes the flow as inclusions between sets and solves them with a worklist in $O(n^3)$ time. The answer is sound for every run, it is the base of closure optimizations, and it is the $k = 0$ case of [k-CFA](/k-cfa/).

## In plain words

In a functional program, `f x` may call any function that ends up in `f`. To find out which, 0-CFA gives every expression and every variable a set of functions. A function written in the code goes into the set of its own expression. A variable gets everything that was bound to it. When a call may call a function, the argument flows into the parameter of that function, and the result of its body flows back into the call. The analysis only looks inside a function once some call can call it. It repeats this until nothing new appears. Every variable has one set for the whole program, so two calls of the same function mix their arguments. That is what the 0 in the name means.

## The problem

The input is a closed term of a call-by-value language with variables, `fun x -> e`, `fix f x -> e` (a recursive function), application `e1 e2`, `let x = e1 in e2`, `if e1 then e2 else e3`, operators on integers and constants. Each node has a label $t$, and each variable occurrence knows its binder $b$. $\Lambda$ is the set of function nodes. The output is the least triple of a set $Re$ of reachable labels, a cache $C[t] \subseteq \Lambda$ for each label and an environment $R[b] \subseteq \Lambda$ for each binder, such that for every $t \in Re$:

1. a function $t$ has $t \in C[t]$;
2. a variable with binder $b$ has $R[b] \subseteq C[t]$;
3. `let x = t1 in t2` has $C[t_1] \subseteq R[x]$ and $C[t_2] \subseteq C[t]$;
4. `if t1 then t2 else t3` has $C[t_2] \cup C[t_3] \subseteq C[t]$;
5. `t1 t2` has, for each $\lambda \in C[t_1]$: $\mathrm{body}(\lambda) \in Re$, $C[t_2] \subseteq R[\mathrm{param}(\lambda)]$, $C[\mathrm{body}(\lambda)] \subseteq C[t]$, and for `fix f x -> e` also $\lambda \in R[f]$;

and the root and the direct subterms of every reachable node other than a function are in $Re$. The call graph is the set of pairs $(t, \lambda)$ with $t$ = `t1 t2` in $Re$ and $\lambda \in C[t_1]$.

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | triples $(Re, C, R)$ of reachable labels and sets of functions |
| order | inclusion in all parts (bottom is precise) |
| join | union in all parts |
| bottom and top | everything empty, and all labels reachable with all sets equal to $\Lambda$ |
| boundary value | the root is reachable |
| initial value | everything empty |
| transfer | the inclusions above; monotone, and not distributive, since rule 5 needs both $t$ reachable and $\lambda \in C[t_1]$ |

## The algorithm

```pseudo id=main
ZERO-CFA(e)
L1  label the nodes of e and link each variable to its binder
L2  for each set node n (C[t] for a label, R[b] for a binder): V[n] <- {}; D[n] <- {}; succ[n] <- {}
L3  W <- []; REACH(root)
L4  while W is not empty do
L5      take n from W; d <- D[n]; D[n] <- {}
L6      for each application t that watches n and each λ in d do CALL(t, λ)
L7      for each m in succ[n] do PROPAGATE(m, d)
L8  return the sets V

REACH(t)
L9  if t is marked then return; mark t
L10 if t is a function then PROPAGATE(C[t], {t}); stop here, the body waits for a call
L11 if t is a variable with binder b then ADD-EDGE(R[b], C[t])
L12 if t is let x = t1 in t2 then ADD-EDGE(C[t1], R[x]); ADD-EDGE(C[t2], C[t])
L13 if t is if t1 then t2 else t3 then ADD-EDGE(C[t2], C[t]); ADD-EDGE(C[t3], C[t])
L14 if t is t1 t2 then make t watch C[t1] and CALL(t, λ) for each λ in V[C[t1]]
    then REACH each direct subterm of t

CALL(t, λ)                          -- t is t1 t2
L15 if λ is fix f x -> body then PROPAGATE(R[f], {λ})
L16 ADD-EDGE(C[t2], R[param(λ)])
L17 ADD-EDGE(C[body(λ)], C[t])
L18 REACH(body(λ))

ADD-EDGE(a, b)
L19 if b is not in succ[a] then add b to succ[a]; PROPAGATE(b, V[a])

PROPAGATE(n, d)
L20 d <- d \ V[n]; if d is empty then return
L21 V[n] <- V[n] ∪ d; D[n] <- D[n] ∪ d; if n is not in W then add n to W
```

The sets $V[n]$ form a graph with an edge $a \to b$ for each inclusion $V[a] \subseteq V[b]$. Most edges are known from the text (lines L11 to L13). The edges of a call (lines L16 and L17) appear only when a function reaches the operator, which is why each application watches the cache of its operator. $D[n]$ holds the elements that $n$ has not yet sent on, so each element crosses each edge once. REACH skips the bodies of functions, and line L18 visits a body only when a call may run it.

## Example

```
let id = fun x -> x in
let a = id (fun y -> y + 1) in
let b = id (fun z -> z * 2) in
a 3
```

The program evaluates to 4. Write $\lambda_x$, $\lambda_y$ and $\lambda_z$ for the three functions.

| step | what the algorithm finds |
|---|---|
| 1 | REACH from the root: $\lambda_x \in C[\texttt{fun x}]$, and the edge to $R[id]$ gives $R[id] = \{\lambda_x\}$ |
| 2 | the operator `id` of both calls gets $\lambda_x$; each call runs CALL with $\lambda_x$ |
| 3 | the first call: $\lambda_y$ flows into $R[x]$; the second call: $\lambda_z$ flows into $R[x]$; so $R[x] = \{\lambda_y, \lambda_z\}$ |
| 4 | the body `x` of $\lambda_x$ gets $\{\lambda_y, \lambda_z\}$ and sends it back to both calls; so $R[a] = R[b] = \{\lambda_y, \lambda_z\}$ |
| 5 | the call `a 3` gets $\lambda_y$ and $\lambda_z$ in its operator, CALL reaches both bodies, and the integer 3 adds no function to $R[y]$ or $R[z]$ |

The call graph has 4 edges: both calls of `id` go to $\lambda_x$, and `a 3` goes to $\lambda_y$ and $\lambda_z$. The run only calls $\lambda_y$ at `a 3`. The edge to $\lambda_z$ is spurious, because both calls of `id` share the one set $R[x]$. [1-CFA](/k-cfa/) keeps one set of `x` per call site of `id`, and removes it.

## Correctness

**Least solution.** Every edge and every element that the algorithm adds is required by one of the rules, for labels that the rules make reachable. So, by induction over the steps, the sets stay inside every solution. When $W$ is empty, every element of every set has crossed every edge and reached every watcher, so all rules hold. So the result is the least solution.

**Soundness.** Use an environment semantics with closures $(\lambda, \rho)$. Call an environment good if the closure of each variable has its function in $R$ of the variable's binder, and its own environment good. By induction on the evaluation, a reachable node evaluated in a good environment gives a value whose function is in $C[t]$. At a call, the operator gives $\lambda \in C[t_1]$, rule 5 puts the argument into $R[\mathrm{param}(\lambda)]$ and makes the body reachable, so the body runs in a good environment and its result is in $C[t]$. This covers runs that stop, get stuck or loop, since every finished part of a run is a finished evaluation. The full proofs are in the proof file.

## Complexity

**Proved.** There are $O(n)$ set nodes and each set has at most $n$ functions. The edges are $O(n)$ from the text and two per pair of an application and a function, so $O(n^2)$ in all. Each element crosses each edge at most once, which costs $O(n^3)$. CALL runs at most twice per pair of an application and a function, and each run may send a set of size $O(n)$, which is $O(n^3)$ again. So the time is $O(n^3)$ and the space is $O(n^2)$ for the sets and the edges.

**Stated in the literature.** Heintze and McAllester (1997) reduce the recognition problem of two-way nondeterministic pushdown automata (2NPDA) to flow analysis. No sub-cubic algorithm for that problem is known, so this is the "cubic bottleneck". Van Horn and Mairson (2008) prove that 0-CFA is complete for PTIME, so it is unlikely to have a fast parallel algorithm.

**Measured, not proved.** On 500 random closed terms (seed 1991), the result equals a plain round-robin iteration of the rules. On 2000 random terms (seed 1988), every closure, binding and call of a concrete run is in the result. The test interpreter agrees with the substitution semantics of the toy language on 500 random terms.

## Properties

- **Monovariant.** Each variable has one set for all calls of its function. This is the source of the spurious edge in the example.
- **Reachability-aware.** A function body that no reachable call can run adds nothing. Plain constraint versions that scan all the code give a larger, still sound, result.
- **Flow-insensitive within a body.** The branches of `if` both flow into the result, whatever the test.
- **Exact on linear programs.** Van Horn and Mairson show that 0-CFA and evaluation agree when each bound variable is used at most once. This is the root of the PTIME hardness.
- **Equivalent to inclusion-based points-to analysis.** Functions play the role of allocation sites, and application plays the role of a call through a pointer. The constraint graph is the one of [Andersen's analysis](/andersen-analysis/).

## Variants and improvements

- **k-CFA.** Keep the last $k$ call sites as a context for each binding ([k-CFA](/k-cfa/)). It is more precise and EXPTIME-complete for $k \ge 1$ ([the k-CFA theorem](/k-cfa-exptime-completeness/)).
- **Abstract values for constants.** Track integers and booleans by sign or by constant to prune `if` branches. This mixes control flow analysis with constant propagation.
- **Equality-based flow.** Unify the sets of both sides instead of including one in the other, as in [Steensgaard's analysis](/steensgaard-analysis/). It runs in almost linear time and loses precision.
- **Sub-transitive flow.** Heintze and McAllester (PLDI 1997) answer some queries in linear time for typed programs of bounded type size by not building the transitive closure.
- **CFL reachability.** The flow can also be written as reachability with matched parentheses ([CFL reachability](/cfl-reachability/)).

## When to use it

Use 0-CFA when a compiler for a functional language needs to know which functions a call may run, for example to turn calls into direct calls, to choose a closure layout in [closure conversion](/closure-conversion/), or to do [defunctionalization](/defunctionalization/) with one case per function that reaches a call. It is cubic in the worst case and usually much faster. When two uses of a helper such as `map` or `compose` mix their arguments and that costs too much precision, use 1-CFA or a polynomial context-sensitive variant.

## Pitfalls

- **Analysing every body at once.** A version of line L10 that also calls REACH on the body of every function gives a sound result with more edges, because dead functions add flows. Keep line L10 as it is and let line L18 reach a body only on a call.
- **Forgetting the self binding of fix.** Without line L15, the recursive call `f (x - 1)` inside `fix f x -> ...` finds no function in $R[f]$, and the recursive edge is missing. Line L15 must put the fix itself into $R[f]$.
- **Sending only the new elements on a new edge.** If line L19 sent only the current delta, the elements that $a$ received before the edge existed would never cross it. Line L19 must send all of $V[a]$.
- **Calling 0-CFA context-sensitive.** The name 0-CFA means zero call sites of context. Call strings of length $k$ give k-CFA only in this functional setting; in object-oriented programs, call-site contexts and k-CFA in the sense of Shivers differ.

## Implementations

## History

Jones (1981) gave an early flow analysis for lambda expressions. Shivers named control flow analysis in 1988 and defined 0-CFA and 1-CFA for Scheme by abstract interpretation of a continuation-passing semantics, in a PLDI paper and in his 1991 thesis. Palsberg (1995) wrote 0-CFA as a system of set constraints and showed that it agrees with the abstract interpretation form. Heintze and McAllester (1997) explained why it has resisted sub-cubic algorithms, and Van Horn and Mairson (2008) proved it complete for PTIME.

## References
