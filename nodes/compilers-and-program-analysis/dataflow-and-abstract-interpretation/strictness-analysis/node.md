---
tag: GYNYB7
kind: algorithm
slug: strictness-analysis
name: Strictness analysis
aliases:
- Mycroft strictness analysis
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Finds functions of a lazy language that surely evaluate an argument, by abstract interpretation over a two-point domain, so it can be passed by value.
model: word-ram
complexity:
  vars: {n: the size of the function body, k: the number of parameters}
  time: {worst: O(4^k n), average: O(4^k n), best: Θ(2^k n)}
  space: {extra: Θ(2^k + n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1980
  people: [Alan Mycroft]
  note: Mycroft mapped every defined value to 1 and the undefined value to 0, computed recursive functions over this two-point domain by fixed-point iteration, and used the result to pass arguments of a lazy language by value.
prereqs: [abstract-domain, galois-connection, kleene-fixed-point-theorem]
see_also: [abstract-interpretation, collecting-semantics, graph-reduction, deforestation, binding-time-analysis, function-inlining, simply-typed-lambda-calculus, widening-operator]
sources:
  - paper: doi:10.1007/3-540-09981-6_19
    title: "Alan Mycroft, The theory and practice of transforming call-by-need into call-by-value, International Symposium on Programming 1980, LNCS 83, pages 269 to 281"
    locator: the two-point abstraction of a flat domain, the abstract functions of first-order recursive programs, their computation as least fixed points, and the use of the result to evaluate arguments before the call
  - paper: doi:10.1016/0167-6423(86)90010-9
    title: "Geoffrey Burn, Chris Hankin and Samson Abramsky, Strictness analysis for higher-order functions, Science of Computer Programming 7(3), 1986, pages 249 to 278"
    locator: the extension of the two-point analysis to typed higher-order functions, with abstract domains of monotone functions, and its proof of soundness
  - paper: doi:10.1007/3-540-15975-4_28
    title: "Chris Clack and Simon Peyton Jones, Strictness analysis, a practical approach, FPCA 1985, LNCS 201, pages 35 to 49"
    locator: the cost of computing the fixed point by full tables, and the frontiers method that stores a monotone table by the border between its points with value 0 and its points with value 1
---

Strictness analysis finds, at compile time, the arguments that a function of a lazy language always evaluates. If $f$ is *strict* in its argument $x_i$, then a call $f\ e_1 \ldots e_k$ is undefined whenever $e_i$ is undefined. The compiler can then compute $e_i$ before the call and pass it by value, with no thunk for it. Mycroft's analysis (1980) maps every defined value to $1$ and the undefined value $\bot$ to $0$. It evaluates the body of $f$ over $\{0, 1\}$, with $\wedge$ for the operators and $x \wedge (y \vee z)$ for a conditional. For a recursive function it computes the least fixed point of the abstract function $f^\sharp : \{0,1\}^k \to \{0,1\}$ by Kleene iteration on its table of $2^k$ entries. Then $f$ is strict in $x_i$ when $f^\sharp(1, \ldots, 1, 0, 1, \ldots, 1) = 0$, with the $0$ in place $i$. This is [abstract interpretation](/abstract-interpretation/) of a denotational semantics, with a two-point [abstract domain](/abstract-domain/).

## In plain words

A lazy language such as Haskell does not compute an argument when a function is called. It makes a *thunk*, a small record that knows how to compute the argument later, and computes it on the first use. An argument that is never used is never computed. But this is slow. A thunk takes memory, and a function that adds to an accumulator in a loop can build a long chain of thunks.

If a function surely uses an argument, there is no point in delaying it. Computing it early changes nothing: if the argument loops, the call loops anyway. Strictness analysis finds such arguments. It runs the function on two abstract values only: $0$ for "this loops for sure" and $1$ for "this may give a value". If putting $0$ in one argument and $1$ in all others still gives $0$, the function needs that argument.

## The problem

The input is one function in a first-order language with lazy parameters:

$$ f\ x_1 \ldots x_k = \mathit{body}. $$

The body is built from the parameters, integer and boolean constants, the operators $+$, $-$, $\times$, $<$ and $=$, conditionals $\mathbf{if}\ e_1\ \mathbf{then}\ e_2\ \mathbf{else}\ e_3$, lazy bindings $\mathbf{let}\ x = e_1\ \mathbf{in}\ e_2$, and calls $f\ e_1 \ldots e_k$ of $f$ itself with all $k$ arguments. The meaning of $f$ is a function $\varphi : D^k \to D$, where $D = \mathbb{Z} \cup \{\mathit{true}, \mathit{false}\} \cup \{\bot\}$ and $\bot$ stands for a computation that loops or fails. An argument is passed unevaluated, so $\varphi$ may give a value even when an argument is $\bot$.

The function is *strict in $x_i$* if $\varphi(d_1, \ldots, d_k) = \bot$ whenever $d_i = \bot$, for all values of the other arguments. This is undecidable in general, since $f$ might loop for all inputs. So the analysis gives a safe answer: it may miss a strict argument, but it never calls an argument strict when it is not.

The abstract domain is $\mathbf{2} = \{0, 1\}$ with $0 \sqsubseteq 1$. The meaning of $0$ is $\{\bot\}$ and the meaning of $1$ is all of $D$. The abstraction of a value is $\mathit{abs}(\bot) = 0$ and $\mathit{abs}(d) = 1$ for every other $d$. This is a [Galois connection](/galois-connection/) between sets of values and $\mathbf{2}$, in the Cousot order: the lower element says more.

## The algorithm

The table $T$ holds the current approximation of $f^\sharp$, one bit for each point of $\{0,1\}^k$. ABS computes the abstract value of an expression from the abstract values of the names in scope, with the table for the recursive calls.

```pseudo id=main
STRICTNESS(f, x1 … xk, body)
L1  for each v in {0,1}^k do T[v] ← 0
L2  repeat
L3      for each v in {0,1}^k do T′[v] ← ABS(body, {xi ↦ vi}, T)
L4      stable ← (T′ = T)
L5      T ← T′
L6  until stable
L7  for i ← 1 to k do strict[i] ← (T[1 … 1, 0 at place i, 1 … 1] = 0)
L8  return T, strict

ABS(e, ρ, T)
L9  if e is a constant then return 1
L10 if e is a name x then return ρ(x)
L11 if e = e1 op e2 then return ABS(e1, ρ, T) ∧ ABS(e2, ρ, T)
L12 if e = if e1 then e2 else e3 then return ABS(e1, ρ, T) ∧ (ABS(e2, ρ, T) ∨ ABS(e3, ρ, T))
L13 if e = let x = e1 in e2 then return ABS(e2, ρ[x ↦ ABS(e1, ρ, T)], T)
L14 if e = f e1 … ek then return T[ABS(e1, ρ, T), …, ABS(ek, ρ, T)]
```

Line L11 holds because every operator needs both operands: if one of them is $\bot$, so is the result. Line L12 says that the condition is always computed, and that the result is defined only if the branch that is taken is defined. Since the analysis does not know which branch is taken, it uses the join $\vee$ of the two. Line L13 binds $x$ without computing $e_1$: a lazy `let` is defined even if $e_1$ is not, as long as $e_2$ does not use $x$. Line L14 reads the current guess for the recursive call.

Lines L1 to L6 are the Kleene iteration $T_0 = \lambda v.\,0$, $T_{j+1} = F(T_j)$ with $F(T)(v) = \mathrm{ABS}(\mathit{body}, \{x_i \mapsto v_i\}, T)$. Each $T_j$ is a monotone table, the tables only go up, and there are $2^k$ entries that can go from $0$ to $1$. So the iteration stops, and it stops at the least fixed point of $F$, as the [Kleene fixed-point theorem](/kleene-fixed-point-theorem/) gives. No widening is needed, since the domain is finite.

A runtime type error, such as `1 + true`, is counted as $\bot$ too. The analysis treats it the same way as a loop.

## Example

Take this function, which swaps its second and third arguments on every call:

```
f x y z = if x == 0 then y else f (x - 1) z y
```

The abstract body is $F(T)(x, y, z) = x \wedge \bigl(y \vee T(x, z, y)\bigr)$. The condition `x == 0` gives $x \wedge 1 = x$, the branch `y` gives $y$, and the call gives $T(x \wedge 1, z, y)$. The iteration runs over the 8 points.

| $(x, y, z)$ | $T_0$ | $T_1$ | $T_2$ | $T_3$ |
|---|---|---|---|---|
| $(0, 0, 0)$ | 0 | 0 | 0 | 0 |
| $(0, 0, 1)$ | 0 | 0 | 0 | 0 |
| $(0, 1, 0)$ | 0 | 0 | 0 | 0 |
| $(0, 1, 1)$ | 0 | 0 | 0 | 0 |
| $(1, 0, 0)$ | 0 | 0 | 0 | 0 |
| $(1, 0, 1)$ | 0 | 0 | 1 | 1 |
| $(1, 1, 0)$ | 0 | 1 | 1 | 1 |
| $(1, 1, 1)$ | 0 | 1 | 1 | 1 |

In closed form, $T_1 = x \wedge y$ and $T_2 = x \wedge (y \vee z)$. Then $T_3 = x \wedge (y \vee (x \wedge (z \vee y))) = T_2$, so line L4 finds the table stable after three rounds. Line L7 reads three entries:

- $T(0, 1, 1) = 0$, so $f$ is strict in $x$.
- $T(1, 0, 1) = 1$, so $f$ is not known to be strict in $y$.
- $T(1, 1, 0) = 1$, so $f$ is not known to be strict in $z$.

The entry $T(1, 0, 0) = 0$ says more: if both $y$ and $z$ are undefined, so is the result. The lazy runs agree. With $\Omega$ a term that loops:

| call | the calls that follow | result |
|---|---|---|
| `f 3 Ω 5` | `f 2 5 Ω`, `f 1 Ω 5`, `f 0 5 Ω` | 5 |
| `f 2 Ω 5` | `f 1 5 Ω`, `f 0 Ω 5` | loops |
| `f Ω 1 5` | the test `Ω == 0` | loops |

So $f$ is really not strict in $y$, and $T_1$ is not a safe answer: it would call $f$ strict in $y$. Only the fixed point is safe.

A second function shows the common use:

```
sum n acc = if n == 0 then acc else sum (n - 1) (acc + n)
```

Here $F(T)(n, a) = n \wedge (a \vee T(n, a \wedge n))$, and the iteration gives $T_1 = T_2 = n \wedge a$. So `sum` is strict in both arguments. The compiler can compute `acc + n` before each call, and the chain of thunks `((0 + 4) + 3) + …` never forms.

## Correctness

Two facts are needed: the iteration computes the least fixed point of $F$, and the least fixed point is safe.

The first is Kleene's theorem on the finite lattice of tables. $F$ is monotone, because $\wedge$, $\vee$ and a lookup in a monotone table are monotone. So $T_0 \sqsubseteq T_1 \sqsubseteq \ldots$, and every $T_j$ is below every fixed point. The chain stops after at most $2^k$ strict steps.

For the second, let $\varphi$ be the meaning of $f$. It is the limit of $\varphi_0 = \lambda d.\,\bot$ and $\varphi_{j+1} = \Phi(\varphi_j)$, where $\Phi$ is the concrete counterpart of $F$. Say that a table $T$ *covers* a function $\psi$ if $\mathit{abs}(\psi(d)) \le T(a)$ whenever $\mathit{abs}(d_i) \le a_i$ for all $i$. One induction on expressions shows that ABS covers the concrete evaluation of the body, case by case for lines L9 to L14. A second induction on $j$ shows that the least fixed point $T^*$ covers every $\varphi_j$. In a flat domain $\varphi(d) = \varphi_j(d)$ for some $j$, so $T^*$ covers $\varphi$. If $T^*(1, \ldots, 0, \ldots, 1) = 0$, then $\varphi(d) = \bot$ for every $d$ with $d_i = \bot$. This is the proof by fixed-point induction. The full proof is in [the correctness proof](proofs/correctness.md).

The denotation $\varphi$ agrees with the running program: a lazy call stops with a value exactly when its denotation is not $\bot$. This is the adequacy of the denotational semantics of recursion equations under call by name, which Winskel proves in *The Formal Semantics of Programming Languages* (1993), in the chapter on recursion equations.

## Complexity

The table has $2^k$ entries, and each entry can change only from $0$ to $1$. Every round but the last changes at least one entry, so there are at most $2^k + 1$ rounds. A round evaluates the body at $2^k$ points, in $O(n)$ time each. The total is $O((2^k + 1) \cdot 2^k \cdot n) = O(4^k n)$ time in the worst case. At least two rounds are always needed, one to compute and one to see that nothing changed, so the best case is $\Theta(2^k n)$, reached by every function with no recursion. The space is $\Theta(2^k)$ for the two tables and $O(n)$ for the code of the body and the stack of ABS.

The cost is exponential in the number of parameters, not in the size of the program. For the small arities of real functions this is fine. For functions with many parameters, or for higher-order functions, where the abstract domains of functions grow much faster, the table is too large. The frontiers method of Clack and Peyton Jones (1985) stores a monotone table by the border between its $0$ points and its $1$ points, which is often much smaller.

## Properties

- **Sound.** If the analysis says that $f$ is strict in $x_i$, then it is.
- **Not complete.** The analysis may miss strictness. For `g x y = if x == x then y else 0`, it says that $g$ is not strict in $y$, but the `else` branch is never taken, so $g$ is strict in $y$.
- **Least fixed point.** The result is the most precise table that is a fixed point of $F$. Any other fixed point is also safe, but it gives fewer strict arguments.
- **Monotone tables.** Every table $T_j$ is monotone, and so is the result.
- **Deterministic.** The order of the points in line L3 does not matter, because every $T'[v]$ reads only $T$.

## Variants and improvements

- **Systems of functions.** For functions that call each other, keep one table for each function and update all tables in each round. The bound on the number of rounds becomes the total number of entries plus one.
- **In-place updates.** Writing $T[v]$ at once in line L3, instead of into $T'$, often needs fewer rounds. It reaches the same least fixed point, by the theory of chaotic iterations.
- **Higher-order functions.** Burn, Hankin and Abramsky (1986) extended the analysis to typed higher-order functions. The abstract value of a function is a monotone function between abstract domains, so the tables grow very fast with the order of the types.
- **Frontiers.** Clack and Peyton Jones (1985) store each monotone table by its frontier, the border between the points with value $0$ and the points with value $1$, which can be much smaller than $2^k$ entries.
- **Data structures.** A two-point domain cannot say "this function evaluates the whole list". Wadler (1987) used a four-point domain for lists, and Wadler and Hughes (1987) used projections to describe how much of a structure a function needs.
- **Demand analysis.** Modern compilers for lazy languages, such as GHC, run a backward analysis that records how each argument is used, which descends from this line of work.

## When to use it

Use it in a compiler for a lazy language, where it is one of the most useful optimizations: strict arguments can be computed early, kept unboxed and passed in registers, and accumulators no longer build chains of thunks. It also tells a parallel implementation which arguments can be computed at the same time as the call, which was the aim of Clack and Peyton Jones. A language that passes all arguments by value has no use for it, since every function is already strict in all its arguments in that semantics. For more than a handful of parameters, use frontiers or a type-based analysis instead of full tables.

## Pitfalls

- **Starting from the top.** Writing line L1 as $T[v] \leftarrow 1$ makes the iteration go down to the greatest fixed point. That table is safe but weak. For `sum` it gives $T = n$, so it misses that `sum` is strict in `acc`. Line L1 must start from $0$.
- **Stopping early.** Writing line L6 as a fixed number of rounds, such as one, returns a table below the least fixed point, and that is not safe. In the example, $T_1 = x \wedge y$ calls $f$ strict in $y$, but `f 3 Ω 5` gives 5. Line L6 must wait for a stable table.
- **A conditional as an operator.** Writing line L12 as $\mathrm{ABS}(e_1) \wedge \mathrm{ABS}(e_2) \wedge \mathrm{ABS}(e_3)$ claims that both branches are computed. Then `h x y = if x == 0 then y else 1` looks strict in $y$, but `h 1 Ω` gives 1. Line L12 must join the two branches with $\vee$.
- **A strict let.** Writing line L13 as $\mathrm{ABS}(e_1) \wedge \mathrm{ABS}(e_2, \rho[x \mapsto 1])$ treats a lazy `let` as strict. Then `k x = let y = x in 5` looks strict in $x$, but `k Ω` gives 5. Line L13 must bind $x$ to the abstract value of $e_1$ and not compute it.
- **The wrong probe.** Writing line L7 with $0$ in all the other places, $T[0, \ldots, 0] = 0$, tests something else. For `p x y = y` that entry is $0$, so $p$ would look strict in $x$, but `p Ω 1` gives 1. Line L7 must put $1$ in every place but $i$.

## Implementations

## History

Mycroft introduced the analysis in 1980, at the International Symposium on Programming in Paris, and developed it in his Edinburgh thesis of 1981. He framed it as an abstract interpretation in the sense of Cousot and Cousot (1977), applied to the denotational semantics of recursion equations, and used it to change call by need into call by value where it is safe. Clack and Peyton Jones (1985) looked at the cost of the fixed point and introduced frontiers. Burn, Hankin and Abramsky (1986) gave the higher-order version and its proof of soundness. Wadler and Hughes (1987) handled data structures with projections. Strictness analysis became a standard part of compilers for lazy languages.

## References
