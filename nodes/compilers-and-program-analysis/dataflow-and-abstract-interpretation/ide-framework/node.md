---
tag: 60PTYF
kind: algorithm
slug: ide-framework
name: IDE framework
aliases:
- interprocedural distributive environments
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: research
summary: Extends IFDS to environment problems, such as linear constant propagation, by labeling exploded edges with distributive value functions.
solves: [constant-propagation-problem]
model: word-ram
complexity:
  vars: {E: the number of edges of the supergraph, N: the number of nodes of the supergraph, D: the largest number of facts of one procedure, C: the number of call sites}
  time: {worst: O(E D^3), average: O(E D^3), best: Θ(N + E)}
  space: {extra: O(N D^2 + C D^2)}
properties: {deterministic: true, recursive: false}
prereqs: [ifds-framework, constant-propagation-problem]
see_also: [interprocedural-constant-propagation, functional-approach-interprocedural, interprocedural-dataflow-analysis, sparse-conditional-constant-propagation, context-sensitivity, mop-mfp-coincidence-theorem, cfl-reachability, pushdown-reachability]
sources:
  - paper: doi:10.1016/0304-3975(96)00072-2
    title: "Mooly Sagiv, Thomas Reps and Susan Horwitz, Precise interprocedural dataflow analysis with applications to constant propagation, Theoretical Computer Science 167(1-2), 131 to 170, 1996"
    locator: the IDE problem, environment transformers, the exploded supergraph with micro-functions, the two-phase algorithm, linear constant propagation and its O(E D^3) bound
  - paper: doi:10.1007/3-540-59293-8_226
    title: "Mooly Sagiv, Thomas Reps and Susan Horwitz, Precise interprocedural dataflow analysis with applications to constant propagation, TAPSOFT '95: Theory and Practice of Software Development, Lecture Notes in Computer Science, 651 to 665, 1995"
    locator: the conference version of the same work
  - paper: doi:10.1145/199448.199462
    title: "Thomas Reps, Susan Horwitz and Mooly Sagiv, Precise interprocedural dataflow analysis via graph reachability, Proceedings of the 22nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '95), 49 to 61, 1995"
    locator: the IFDS tabulation algorithm that Phase I generalizes
  - paper: doi:10.1145/12276.13327
    title: "David Callahan, Keith D. Cooper, Ken Kennedy and Linda Torczon, Interprocedural constant propagation, Proceedings of the 1986 SIGPLAN Symposium on Compiler Construction, 152 to 161, 1986"
    locator: jump functions and return functions for constants across calls, the earlier practical approach
  - paper: doi:10.1145/2259051.2259052
    title: "Eric Bodden, Inter-procedural data-flow analysis with IFDS/IDE and Soot, Proceedings of the ACM SIGPLAN International Workshop on State of the Art in Java Program Analysis (SOAP '12), 3 to 8, 2012"
    locator: the Heros solver for IFDS and IDE problems
  - paper: doi:10.1007/978-3-030-17465-1_22
    title: "Philipp Dominik Schubert, Ben Hermann and Eric Bodden, PhASAR: an inter-procedural static analysis framework for C/C++, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2019), Lecture Notes in Computer Science, 393 to 410, 2019"
    locator: an IFDS and IDE solver on LLVM IR
  - paper: "Micha Sharir and Amir Pnueli, Two approaches to interprocedural data flow analysis, in Steven S. Muchnick and Neil D. Jones (eds.), Program Flow Analysis: Theory and Applications, Prentice-Hall, 1981"
    locator: the meet over valid paths and the functional approach with procedure summaries
---

The IDE framework of Sagiv, Reps and Horwitz extends [IFDS](/ifds-framework/) from sets of facts to environments. IDE stands for Interprocedural, Distributive, Environment. An environment maps each fact, usually a variable, to a value in a lattice, and every flow function must distribute over the meet of environments. Such a function is fixed by small functions on single values, one for each pair of facts. IDE puts these *micro-functions* on the edges of the exploded supergraph of IFDS. Phase I walks the graph like the tabulation algorithm, but each path edge carries the meet of the micro-functions along its paths. Phase II pushes actual values through these functions. The main example is linear constant propagation, where a variable may be a constant or $a x + b$ of one other variable. The result is the meet over all valid paths, and the time is $O(E D^3)$ when micro-functions are cheap and the value lattice has finite height.

## In plain words

IFDS answers yes or no questions, such as "may this variable hold a secret". Many analyses need a value instead, such as "this variable is always 7". IDE handles these. It keeps the same big graph, with one copy of every program point for each variable. But each edge now carries a small rule that says how a value changes on the way, such as "add 1" or "times 3". First the algorithm builds, for each procedure, rules that go all the way from the entry to every point. It joins rules where paths meet. Then it feeds the real values in at the entry of the program and applies the rules. A procedure that adds 1 to its argument gives a constant at each call with a constant argument, even when the argument differs between callers.

## The problem

An IDE instance is a supergraph $G^*$, a finite set of facts $D_p$ for each procedure $p$, a value lattice $L$ of finite height, and for each edge an environment transformer $t : (D_p \to L) \to (D_q \to L)$ that distributes over the pointwise meet. The output is, for every node $n$ and fact $d$, the meet over all valid paths

$$\mathrm{MVP}(n)(d) = \bigsqcap \{ t_\pi(\rho_0)(d) : \pi \text{ a valid path from } s_{main} \text{ to } n \},$$

where $\rho_0$ is the start environment. This page uses the meet convention of Kildall: the start value is $\top$ and the result is the greatest solution. In the join convention of Cousot the order flips and the same result is the least solution.

A distributive transformer is given by micro-functions. For each pair of facts $d, d'$ there is a function $f_{d,d'} : L \to L$, and

$$t(\rho)(d') = \bigsqcap_{d \in D \cup \{\mathbf{0}\}} f_{d,d'}(\rho(d)),$$

where the extra fact $\mathbf{0}$ always has the value $\bot$. The pair $(\mathbf{0}, d')$ carries the part of $t$ that does not depend on any input, such as `x = 5`. A pair with $f_{d,d'} = \lambda l.\top$ has no edge.

The implementation solves *linear constant propagation* on the toy IR. The values are $\top$, the integers and $\bot$. The micro-functions are:

| form | meaning |
|---|---|
| `top` | $\lambda l.\top$, the function of no path |
| `bot` | $\lambda l.\bot$ |
| `const k` | $\lambda l.k$ |
| `line a b` | $\lambda l.\, a l + b$ with $a \ne 0$, and $\bot \mapsto \bot$ |
| `point l0 v` | $l_0 \mapsto v$, every other value $\mapsto \bot$ |

Every form maps $\top$ to $\top$. The set is closed under meet and composition. The meet of two lines with different slopes agrees with both at one point at most, so it is a point function or `bot`. Each function has exactly one form, so two functions are equal exactly when their tuples are equal. A chain of strict meets from `top` has at most three steps.

| statement | edges and micro-functions |
|---|---|
| `x = k` | $\mathbf{0} \to x$: `const k`; every other $d \to d$: identity |
| `x = a` | $a \to x$: identity, plus the identity for every $d \ne x$ |
| `x = a + k`, `a - k`, `k - a`, `a * k` | $a \to x$: a line. `a * 0` gives $\mathbf{0} \to x$: `const 0` |
| `x = k1 op k2` | $\mathbf{0} \to x$: `const` of the result, or `bot` on a trap |
| any other `x = a op b` | $\mathbf{0} \to x$: `bot` |
| `ret a` | $a \to RET$: identity, or $\mathbf{0} \to RET$: `const a` for a constant |
| call edge of `x = call q(a, b)` | each argument variable to its parameter: identity; a constant argument gives $\mathbf{0} \to$ parameter: `const` |
| call-to-return edge | identity for every fact of the caller except `x` |
| return edge | $RET \to x$: identity, $\mathbf{0} \to \mathbf{0}$: identity |

The parameters of `main` are $\bot$ unless a seed value is given.

## The algorithm

Phase I computes a *jump function* $J(n, d_1, d_2)$ for each pair of a node $n$ in procedure $p$ and facts $d_1, d_2$. It is the meet of the micro-function compositions along all same-level paths from $\langle s_p, d_1 \rangle$ to $\langle n, d_2 \rangle$. It also computes a *summary function* $S(c, d_4, d_5)$ for each call site, which goes from $\langle c, d_4 \rangle$ through the callee to $\langle r, d_5 \rangle$. A key enters the worklist again each time its function goes down. Phase II computes values at start nodes and call nodes with a second worklist, then gets every other value with one application of a jump function.

```pseudo id=main
IDE(G*, F, seeds)    F gives the labelled exploded edges; seeds gives values to the parameters of main
L1  Jump, Through, Summary ← λl.⊤ everywhere; WorkList ← []
L2  for each d in {0} ∪ params(main) do PROPAGATE(s_main, d, d, id)
L3  while WorkList is not empty do
L4      (n, d1, d2) ← remove the first item; f ← Jump(n, d1, d2)          (n is in procedure p)
L5      if n is a call node c, with callee q and return site r then
L6          for each call edge <c,d2> → <s_q,d3> do PROPAGATE(s_q, d3, d3, id)
L7          for each edge <c,d2> → <r,d3> with label g, call-to-return or Summary(c, d2, d3), do PROPAGATE(r, d1, d3, g ∘ f)
L8      else if n is the exit node e_p then
L9          for each call node c of p, with return site r, and each return edge <e_p,d2> → <r,d5> with label g do
L10             t ← Through(c, d1, d5) ⊓ (g ∘ f); if t = Through(c, d1, d5) then skip it, else Through(c, d1, d5) ← t
L11             for each call edge <c,d4> → <s_p,d1> with label h do
L12                 s ← Summary(c, d4, d5) ⊓ (t ∘ h); if s ≠ Summary(c, d4, d5) then Summary(c, d4, d5) ← s
L13                     for each d3 with Jump(c, d3, d4) ≠ λl.⊤ do PROPAGATE(r, d3, d5, s ∘ Jump(c, d3, d4))
L14     else for each successor m of n and each edge <n,d2> → <m,d3> with label g do PROPAGATE(m, d1, d3, g ∘ f)
L15 val ← ⊤ everywhere; LOWER(s_main, 0, ⊥); for each parameter x of main do LOWER(s_main, x, seed of x, or ⊥)
L16 while WorkList2 is not empty do
L17     (n, d) ← remove the first item; v ← val(n, d)          (n is in procedure p)
L18     if n = s_p then for each m in {s_p} ∪ calls(p) and each d2 with Jump(m, d, d2) ≠ λl.⊤ do LOWER(m, d2, Jump(m, d, d2)(v))
L19     if n is a call node with callee q then for each call edge <n,d> → <s_q,d3> with label h do LOWER(s_q, d3, h(v))
L20 for each other node n of p and each d2 do val(n, d2) ← ⊓ over d1 of Jump(n, d1, d2)(val(s_p, d1))
L21 return val without the fact 0

PROPAGATE(n, d1, d2, f)
L22 j ← Jump(n, d1, d2) ⊓ f; if j ≠ Jump(n, d1, d2) then Jump(n, d1, d2) ← j and append (n, d1, d2) to WorkList unless it is there

LOWER(n, d, v)
L23 w ← val(n, d) ⊓ v; if w ≠ val(n, d) then val(n, d) ← w and append (n, d) to WorkList2 unless it is there
```

Phase I has the shape of the IFDS tabulation. The differences are in L22 and in the exit case. A key is not done when it is first found. It goes back on the worklist each time its function goes down, and the finite height of the function space bounds how often this happens. At the exit (L9 to L13), $Through(c, d_1, d_5)$ collects the effect of the callee from the entry fact $d_1$ to the return fact $d_5$ at the site $c$. Each call edge into $d_1$ then turns it into a summary function, and every path edge that already reaches the call is extended.

In Phase II, line L18 handles the start node of $p$ and the call nodes of $p$ only. These are the nodes where values must cross into other procedures, so they need the worklist. Every other node gets its value in L20, in one pass, from the values at the start of its procedure.

The implementation keeps, next to $Jump$, an index of sources for L13 and an index of targets for L18. It also builds, for each call site, the inverse of its call edges for L11.

## Example

```text
add(a, b):    t = a * 3
              u = t + 1
              ret u
main(n):      x = 2
              y = call add(x, n)        c1
              z = call add(n, x)        c2
              v = 4
              w = call add(v, y)        c3
              ret w
```

The parameter `n` of `main` is $\bot$. Phase I finds these jump functions in `add`: $a \to t$ is `line 3 0`, $a \to u$ is `line 3 1`, and at the exit $a \to RET$ is `line 3 1`. The fact $b$ only reaches itself. At the exit, L10 to L12 give one summary function per call site from the argument variable to the target: $x \to y$ at $c_1$, $n \to z$ at $c_2$ and $v \to w$ at $c_3$, all `line 3 1`. Each site also gets $\mathbf{0} \to \mathbf{0}$, so there are six summary functions.

Back in `main`, L13 composes each summary function with the jump function at the call:

| target | composition | jump function from the start of `main` |
|---|---|---|
| `y` | `line 3 1` after $\mathbf{0} \to x$: `const 2` | $\mathbf{0} \to y$: `const 7` |
| `z` | `line 3 1` after $n \to n$: identity | $n \to z$: `line 3 1` |
| `w` | `line 3 1` after $\mathbf{0} \to v$: `const 4` | $\mathbf{0} \to w$: `const 13` |

Phase II starts with $\mathbf{0} = \bot$ and $n = \bot$ at the start of `main`. So `y` is 7, `w` is 13, and `z` is $\bot$. At the start of `add`, `a` gets 2, $\bot$ and 4 from the three calls, so it is $\bot$. The same is true of `b`. A context-insensitive analysis of the same supergraph sees only $a = \bot$ at the entry of `add`, so it reports `u` as $\bot$ and gets $\bot$ for `y` and `w` too. IDE gets the constants because the summary keeps the relation $RET = 3a + 1$, not the value of `a`.

The run finds 53 keys, with 53 changes of jump functions, 6 summary functions and 20 changes of values in Phase II.

## Correctness

The full proof is in the proof file. Its steps:

1. **The micro-functions.** The forms are closed under meet and composition, every form is distributive and maps $\top$ to $\top$, each function has one form, and a strictly falling chain has at most four elements.
2. **One path, many facts.** For a path $\pi$ of the supergraph, $t_\pi(\rho)(d')$ is the meet of the compositions of micro-functions along the exploded paths that follow $\pi$ and end at $d'$, applied to the start values. So MVP is the meet over valid paths of the exploded graph.
3. **Phase I is sound.** Every stored jump, through and summary function is a finite meet of the functions of real same-level paths. The proof is an induction on time, with distributivity to move compositions inside meets.
4. **Phase I is complete.** Each key is taken off the worklist after its last change. This gives five local constraints at the end. The one at summary functions holds because L7 or L13 runs after both functions take their final values. An induction on the length of the path then shows that the jump function is at most the function of every same-level path.
5. **Phase II.** The values at start nodes and call nodes are meets of real path values, and at the end they satisfy three local constraints. An induction on the number of calls that are still open gives the other direction. L20 then gives the right value at every other node.
6. **Termination and cost.** Each function changes at most three times and each value at most twice. The cost counts the work at each kind of node, as for IFDS.

## Complexity

- **Phase I.** A node has at most $(D+1)^2$ keys, and each is taken off the worklist at most three times, once per change. So the counts of IFDS grow by a constant factor: $O(E D^3)$ for ordinary nodes and $O(D^3)$ per call site for call nodes and exit nodes.
- **Phase II.** Each value at a start node or a call node changes at most twice. Each time a start value changes, L18 looks at the keys of that entry fact at the start node and at each call node of the procedure. L20 is one pass over the keys. This is $O((N + C) D^2)$.
- **Total.** $O(E D^3)$ time and $O(N D^2 + C D^2)$ space, with hash tables and micro-functions of constant size. Each meet, composition and application is $O(1)$ here when integers fit in a word.
- **Best case.** Building the supergraph reads the program, $\Theta(N + E)$.
- **Few targets per fact.** In linear constant propagation a statement sends a variable to itself and to at most one other variable. So the flow steps stay near the number of keys, far below the $D^3$ factor per edge.

The tables below are *measured*, not proved. The first has random modules of the toy IR with loops and recursion. `f0` calls `f1`, each `fi` calls `f(i+1)` and one random procedure, and some arguments are constants.

| procedures | variables | $N$ | $E$ | $D$ | keys | jump changes | summary changes | value changes | $E (D+1)^3$ | ms |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 133 | 155 | 15 | 1509 | 1688 | 16 | 122 | 634880 | 5.2 |
| 16 | 4 | 527 | 615 | 15 | 5756 | 6371 | 65 | 459 | 2519040 | 20.9 |
| 16 | 16 | 711 | 801 | 27 | 13567 | 14490 | 68 | 869 | 17583552 | 75.6 |
| 64 | 4 | 2061 | 2430 | 15 | 21926 | 24562 | 297 | 1773 | 9953280 | 248.4 |
| 64 | 16 | 2762 | 3127 | 27 | 50878 | 54734 | 304 | 3313 | 68643904 | 626.1 |

Most keys get one function and keep it. At most about one key in eight goes down after it is found. The second table is a worst case for the number of keys. A procedure `g` with $k$ parameters moves them around in a loop with linear steps, so every entry fact reaches every variable, and at the loop head the lines meet into points and then into `bot`. `main` calls `g` twice.

| $k$ | $N$ | $E$ | $D$ | keys | jump changes | summary changes | value changes | $E (D+1)^3$ | ms |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 14 | 17 | 7 | 246 | 458 | 18 | 19 | 8704 | 1.7 |
| 8 | 18 | 21 | 11 | 1058 | 2054 | 34 | 35 | 36288 | 6.9 |
| 16 | 26 | 29 | 19 | 5946 | 11774 | 66 | 67 | 232000 | 85.6 |
| 32 | 42 | 45 | 35 | 39530 | 78830 | 130 | 131 | 2099520 | 435.8 |

Here the keys come close to $N (D+1)^2$, and almost every key changes twice. The times were taken on a busy machine, so only the counts are reliable.

## Properties

- **Exact.** For a distributive problem whose micro-functions are closed under meet and composition, the result is the meet over all valid paths, with and without recursion.
- **Relations, not values.** A summary function keeps how the result depends on the argument. One summary serves callers with different constant arguments.
- **IFDS as a special case.** With the two-point lattice and the identity on every edge, Phase I finds exactly the path edges of IFDS, and a fact holds where its value is not $\top$.
- **Order free.** The final jump functions and values do not depend on the order of the worklists.
- **Only what is reached.** Keys exist only for entry facts that some valid path reaches.

## Variants and improvements

- **Copy constant propagation.** Without lines and points, only `const`, identity and `bot` remain. This is cheaper and finds constants that are only copied across calls.
- **Affine relations.** Linear constant propagation follows one variable at a time. Relations between several variables, such as $x + y = 10$, need weighted pushdown systems or other summary-based methods, which cost more.
- **Solvers.** Heros (Bodden 2012) runs IDE problems on Soot for Java. PhASAR (Schubert, Hermann and Bodden 2019) runs them on LLVM IR. Both build the supergraph on demand.
- **Typestate.** IDE is also used for typestate, with an object as the fact and the set of its possible states as the value.
- **Other forms.** Like IFDS, IDE can be read as a [functional approach](/functional-approach-interprocedural/) where each procedure summary is stored one pair of facts at a time. It is also a weighted form of [CFL-reachability](/cfl-reachability/) and of [pushdown reachability](/pushdown-reachability/).

## When to use it

Use IDE when the result at a point is a value per variable, the transformers are distributive, and you want precision across calls. Linear constant propagation, copy constants and typestate fit. If the facts have no values, IFDS is simpler. If one result depends on two variables at once, as in `x = a + b` with both unknown, the transformer is not distributive in this sense, and IDE gives `bot`. Then use an intraprocedural method such as [sparse conditional constant propagation](/sparse-conditional-constant-propagation/) inside procedures, or a non-distributive functional approach.

## Pitfalls

- **Forms must be unique.** L22 stops when the new function equals the old one. If one function has two forms, the test can fail forever or miss a change. Keep every micro-function in one normal form, or compare the functions themselves.
- **Integer overflow.** The meet of two lines solves $a_1 l + b_1 = a_2 l + b_2$. With machine integers that wrap around, this equation can have several solutions, and the point form is wrong. Use exact integers, or treat a possible overflow as `bot`.
- **Infinite height.** Full linear functions over the integers are fine here because each chain has at most three steps. A richer function space without a height bound may not stop.
- **Functions on $\top$.** Every micro-function must map $\top$ to $\top$, or a fact that no path reaches can give a value. This holds for `const k` too, although it ignores every other input.
- **Branches are ignored.** The result is the meet over valid paths of the graph, so a branch that is never taken still counts. A recursive procedure is analysed at every depth, even when a test stops the recursion early.
- **Values at other nodes.** Running the Phase II worklist over every node is correct but costs more. Only start nodes and call nodes need it.

## Implementations

## History

Callahan, Cooper, Kennedy and Torczon (1986) introduced jump functions and return functions to carry constants across calls in a practical compiler. Sharir and Pnueli (1981) had defined the meet over valid paths and the functional approach, in which each procedure is summarized as a function. Reps, Horwitz and Sagiv (POPL 1995) turned the functional approach for finite distributive subset problems into reachability on the exploded supergraph. Sagiv, Reps and Horwitz then generalized it to environments. They presented IDE at TAPSOFT 1995, and the journal version appeared in Theoretical Computer Science in 1996. It gave the two phases, linear constant propagation as the main example, and the $O(E D^3)$ bound. Later tools such as Heros (2012) and PhASAR (2019) made IDE available for Java and for C and C++.

## References
