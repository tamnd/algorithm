---
tag: NW600V
kind: problem
slug: mod-ref-analysis
name: Mod-ref analysis
aliases:
- side-effect analysis
- MOD and REF analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: For each call or procedure, find the memory locations it may modify and the ones it may read.
prereqs: [call-graph, alias-analysis, strongly-connected-components]
see_also: [interprocedural-dataflow-analysis, points-to-analysis, call-graph-construction, tarjan-scc, interprocedural-constant-propagation, program-dependence-graph, may-alias-undecidability, escape-analysis]
sources:
  - paper: doi:10.1145/567752.567756
    title: John P. Banning, An efficient way to find the side effects of procedure calls and the aliases of variables, Proceedings of POPL 1979, 29 to 41
    locator: the MOD and USE problems, their split into an alias-free part and the aliases of variables, and the equations over the call graph with binding functions
  - paper: doi:10.1145/960116.53996
    title: Keith D. Cooper and Ken Kennedy, Interprocedural side-effect analysis in linear time, Proceedings of PLDI 1988, SIGPLAN Notices 23(7), 57 to 66
    locator: Banning's alias-free flow-insensitive problem solved with the binding multigraph and depth-first search, in time linear in the size of the call multigraph
---

Mod-ref analysis computes, for each call site and each procedure, the set of variables or memory locations that its execution may modify (MOD) and the set it may read (REF). Optimizers need it at every call: a value kept in a register across a call is still valid only if the call cannot modify it, and two calls can be reordered or run in parallel only if neither modifies what the other reads or modifies. Banning (1979) defined the problem for programs with reference parameters and split it into two parts: the *alias-free* side effects, computed as if no two names referred to the same location, and the aliases, added at the end. Cooper and Kennedy (1988) solved the alias-free part in time linear in the size of the call graph, by splitting it again into a problem on reference formal parameters and a problem on global variables. In languages with pointers, the MOD set of a store depends on [alias analysis](/alias-analysis/), and the problem becomes as hard as alias analysis itself.

## In plain words

When a program calls a function, the compiler wants to know what that call can change and what it can read. If a call cannot change a variable, the compiler can keep the variable's value in a register while the call runs. If two calls do not touch the same data, they can run in either order. The call can change a variable directly, through a parameter that refers to the caller's variable, or through any function it calls in turn. The analysis collects these changes from the leaves of the call graph back to the callers. It follows how each parameter is passed down from function to function, and it adds the global variables that any called function changes.

## Definition

**Input.** A program with a finite set of procedures, a set $Gl$ of global variables, and for each procedure $p$ its local variables and its formal parameters $f_1, \ldots, f_k$, passed by reference. Procedures are not nested. Each procedure has assignments and call sites. For each procedure, $IMOD(p)$ is the set of variables that the statements of $p$ itself, not its calls, may modify, and $IREF(p)$ is the set they may read. A call site $s$ in $p$ calls a procedure $q$ with actual parameters $a_1, \ldots, a_k$. An actual is a variable of $p$, which is then *bound* to the formal $f_i$ of $q$, or an expression, which binds nothing.

**Binding function.** For a call site $s$ from $p$ to $q$, $b_s$ maps a set $X$ of variables of $q$ to the variables of $p$ that they name during the call: each global in $X$ to itself, each formal $f_i \in X$ to its actual $a_i$ if that is a variable, and each local of $q$ to nothing.

**Output.** For each procedure $p$, $GMOD(p)$, the variables of $p$ and the globals that an execution of $p$ may modify, and for each call site $s$ to $q$, $DMOD(s) = b_s(GMOD(q))$. These are the *alias-free* sets: they are the least sets that satisfy Banning's equation

$$GMOD(p) = IMOD(p) \cup \bigcup_{s \text{ in } p \text{, calling } q} b_s(GMOD(q)).$$

The full answer is $MOD(s) = DMOD(s) \cup \{y : x \in DMOD(s) \text{ and } x, y \text{ may be aliases in } p\}$, where the alias pairs come from a separate alias analysis. REF, also called USE, is the same problem with $IREF$ in place of $IMOD$.

**Soundness and precision.** The problem is flow-insensitive: a procedure modifies a variable if some statement of it, or of a procedure it may call, may modify it, whether or not that statement runs on a real path. The least solution of the equation is the most precise flow-insensitive answer. It is sound for every run that only calls along call graph edges, with the [call graph](/call-graph/) taken as given. Calls through pointers or virtual calls need a sound [call graph construction](/call-graph-construction/) first. In the terms of a data-flow framework:

| item | value |
|---|---|
| direction | backward over the call graph, from callees to callers |
| may or must | may |
| domain | a set of variables for each procedure |
| order | inclusion (bottom is precise) |
| join | union |
| bottom and top | every set empty, and every set holding all variables visible in the procedure |
| boundary value | $IMOD(p)$ for each procedure $p$ |
| initial value | $GMOD(p) = IMOD(p)$ |
| transfer | $b_s$ for each call site $s$, which keeps the globals, maps formals to actuals and drops the callee's locals |

## Variants

- **MOD and REF.** The two problems have the same structure and are solved by the same algorithm with different initial sets. Many tools compute both at once and report for each call whether it modifies, reads, both or neither of a location.
- **Alias-free and with aliases.** Reference parameters create aliases when one variable is passed twice, or when a global is passed as an argument. Banning adds them after the alias-free sets are known, using the alias pairs of each procedure.
- **Flow-sensitive side effects.** "Must modify" sets, which say what a call always overwrites, need the paths inside each procedure, and are harder than the may sets. They are the interprocedural form of the kill sets of [reaching definitions](/reaching-definitions/).
- **Programs with pointers.** In C or Java, a store ${*}p = e$ or $p.f = e$ modifies the locations in the points-to set of $p$. Then $IMOD$ comes from a [points-to analysis](/points-to-analysis/), and the variables of the problem are abstract locations instead of names. Locations that do not [escape](/escape-analysis/) a callee can be dropped from its MOD set, like locals.
- **Nested procedures.** With nested scopes, a callee can modify the locals of the procedures that enclose it, and the transfer must drop only the variables that are local to the callee. Cooper and Kennedy handle this case with a more careful pass over the call graph.
- **Array sections.** For parallelizing compilers, the MOD set of an array is a region of the array, for example one row, instead of the whole array.

## Examples

Take globals $g$ and $h$ and these four procedures:

```
main()      { local x, y;  call p(x, y);   // s1
                           call q(x); }    // s2
p(a, b)     { a = 1;  h = 2;  call q(b); } // s3
q(c)        { g = c;  call r(c); }         // s4
r(d)        { d = 0; }
```

The local sets are $IMOD(main) = \emptyset$, $IMOD(p) = \{a, h\}$, $IMOD(q) = \{g\}$ and $IMOD(r) = \{d\}$. The binding graph has an edge from $b$ to $c$ (site s3) and from $c$ to $d$ (site s4). Since $d$ is modified, $c$ and $b$ are modified through these bindings, so $RMOD(r) = \{d\}$, $RMOD(q) = \{c\}$ and $RMOD(p) = \{a, b\}$. The variables of each procedure that are bound to modified formals of its callees join its local set, and then the globals flow up the call graph:

| procedure | $IMOD^+$ | globals modified below it | $GMOD$ |
|---|---|---|---|
| r | $\{d\}$ | none | $\{d\}$ |
| q | $\{g, c\}$ | none | $\{g, c\}$ |
| p | $\{a, b, h\}$ | $\{g\}$ | $\{a, b, h, g\}$ |
| main | $\{x, y\}$ | $\{g, h\}$ | $\{x, y, g, h\}$ |

So $DMOD(s_1) = \{x, y, g, h\}$, $DMOD(s_2) = \{x, g\}$, $DMOD(s_3) = \{b, g\}$ and $DMOD(s_4) = \{c\}$. If `main` called `p(x, x)` instead, $a$ and $b$ would be aliases inside `p`, and the alias step would add $b$ to every MOD set of `p` that holds $a$, and the other way round.

## Known algorithms

| algorithm | what it solves | time |
|---|---|---|
| iteration of Banning's equation | the alias-free sets on the call graph | $O(N \cdot V)$ rounds of $O(E)$ set operations in the worst case, for $V$ variables |
| Banning (1979) | the alias-free sets and the aliases, by iteration over the call graph | polynomial |
| Cooper and Kennedy (1988) | the alias-free sets, split into formals and globals | $O(N_\beta + E_\beta)$ plus $O(N + E)$ set operations |
| points-to based MOD and REF | side effects of stores and loads through pointers | the cost of the points-to analysis plus one pass over the call graph |

Here $N$ and $E$ are the procedures and call sites, and $N_\beta$ and $E_\beta$ are the formals and the bindings of formals to formals. A set operation is a union of bit vectors of $|Gl|$ bits.

**The linear-time algorithm.** Cooper and Kennedy solve the alias-free problem in three steps.

1. **Formals, on the binding multigraph.** The binding graph $\beta$ has one node per formal parameter, and an edge $f \to f'$ for each call site where the formal $f$ of the caller is passed as the actual for the formal $f'$ of the callee. A formal $f$ of $q$ is in $RMOD(q)$ if a path in $\beta$ leads from $f$ to a formal $f''$ of some procedure $r$ with $f'' \in IMOD(r)$. This is one backward graph search from all locally modified formals, in $O(N_\beta + E_\beta)$ time.
2. **The extended local sets.** $IMOD^+(p) = IMOD(p) \cup \bigcup_{s \text{ in } p \text{, calling } q} b_s(RMOD(q))$. This adds the variables of $p$ that it passes to a modified formal.
3. **Globals, on the call graph.** Find the [strongly connected components](/strongly-connected-components/) of the call graph with [Tarjan's algorithm](/tarjan-scc/), and visit them in reverse topological order. For a component $C$, $GG(C)$ is the union of $IMOD^+(p) \cap Gl$ over $p \in C$ and of $GG(C')$ over the components $C'$ that $C$ calls. Then $GMOD(p) = IMOD^+(p) \cup GG(C(p))$ for each $p$ in its component $C(p)$.

Finally $DMOD(s) = b_s(GMOD(q))$ for each call site $s$ to $q$.

## Bounds

**Theorem (Cooper and Kennedy).** The three steps compute the least solution of Banning's equation, and they take $O(N_\beta + E_\beta + \sum_p |IMOD(p)|)$ time plus $O(N + E)$ unions of sets of globals.

*Proof.* Let $L$ be the least solution. Every $b_s$ distributes over union and maps a single variable to at most one variable, so by Kleene iteration, $v \in L(p_0)$ if and only if there is a chain of call sites $p_0 \xrightarrow{s_1} p_1 \xrightarrow{s_2} \cdots \xrightarrow{s_k} p_k$ with $k \ge 0$ and a variable $w \in IMOD(p_k)$ such that $v = b_{s_1}(b_{s_2}(\cdots b_{s_k}(w)))$. Call $y_k = w$ and $y_{i-1} = b_{s_i}(y_i)$ the variables along the chain, so $v = y_0$.

*Formals.* Let $v$ be a formal of $p_0$. A binding maps a global to a global and never to a formal, so every $y_i$ is a formal, and $y_{i-1} \to y_i$ is an edge of $\beta$. So $v \in L(p_0)$ if and only if $\beta$ has a path from $v$ to a formal in the $IMOD$ set of its procedure, which is $v \in RMOD(p_0)$. $\square$

*All variables.* If a $y_i$ is global, so are $y_{i-1}, \ldots, y_0$. Let $t$ be the largest index with $y_0, \ldots, y_t$ all global, or $t = -1$ if $v$ is not global. If $t = k$, then $v = w$ is a global in $IMOD(p_k) \subseteq IMOD^+(p_k)$. If $t < k$, then $y_{t+1}$ is a formal of $p_{t+1}$ when $t + 1 \ge 1$, and it is in $L(p_{t+1})$ by the rest of the chain, so it is in $RMOD(p_{t+1})$, and $y_t = b_{s_{t+1}}(y_{t+1}) \in IMOD^+(p_t)$. The case $t = -1$, $k \ge 1$ is the same with $t + 1 = 1$, and gives $v \in IMOD^+(p_0)$. The case $t = -1$, $k = 0$ gives $v \in IMOD(p_0)$. So $v \in IMOD^+(p_0)$, or $v$ is a global in $IMOD^+(p_t)$ for a procedure $p_t$ that $p_0$ reaches in the call graph. Both are in $IMOD^+(p_0) \cup GG(C(p_0))$, since $GG(C)$ collects the globals of $IMOD^+$ over every procedure that $C$ reaches, including $C$ itself. Conversely, $b_s(RMOD(q)) \subseteq b_s(L(q)) \subseteq L(p)$ by the formal part and the equation, so $IMOD^+(p) \subseteq L(p)$. A global in $IMOD^+(q)$ for $q$ reachable from $p$ is in $L(q)$, and each $b_s$ keeps it, so it is in $L(p)$. $\square$

*Time.* Step 1 is one search of $\beta$. Step 2 visits each actual parameter once. Step 3 is Tarjan's algorithm, $O(N + E)$, and one union per procedure and per call graph edge between components. Computing all $DMOD$ sets visits each call site once. $\blacksquare$

**Lower bounds.** Every algorithm must read the call graph and the local sets, so the time is at least linear. With bit vectors of $w$-bit words, a union of sets of globals costs $O(|Gl| / w + 1)$, which gives $O((N + E)(|Gl| / w + 1))$ for step 3.

**With pointers.** When stores go through pointers, $IMOD$ itself depends on which locations a pointer may point to. A precise MOD set for a call would decide whether a pointer in the callee may point to a given variable, so precise mod-ref inherits the hardness of alias analysis, which is undecidable in general ([may-alias undecidability](/may-alias-undecidability/)). Tools use a sound points-to analysis and accept larger sets.

## Reductions

- **Graph reachability reduces to it.** Give each procedure one global that it modifies and calls that follow the edges of a directed graph. Then $GMOD(p)$ holds the global of $q$ if and only if $q$ is reachable from $p$. So the global part is exactly a reachability problem, which is why step 3 needs the component graph.
- **Alias-free MOD and aliases are independent.** The alias pairs of each procedure can be computed with a separate pass over the call graph, and MOD is the alias-free set closed under these pairs, as in Banning's split.
- **Mod-ref reduces to points-to analysis for pointer programs.** Each store gives $IMOD$ entries for the targets of its pointer, and each load gives $IREF$ entries, after which the problem is the one above on abstract locations.
- **It is a special case of interprocedural data-flow analysis.** The equation is a flow-insensitive [interprocedural data-flow problem](/interprocedural-dataflow-analysis/) over the call graph, with the binding functions as transfer functions.

## Applications

- **Register allocation and code motion across calls.** A value of a variable that is not in $MOD(s)$ survives the call $s$, so the compiler can keep it in a register or move a load of it past the call.
- **Interprocedural constant propagation.** A constant in a global stays valid across a call that does not modify it ([interprocedural constant propagation](/interprocedural-constant-propagation/)).
- **Dependence and parallelization.** Two calls are independent if neither one's MOD set meets the other's MOD or REF set. Parallelizing compilers for Fortran used this, with array sections, to run calls in a loop in parallel. The same sets give the edges of calls in a [program dependence graph](/program-dependence-graph/).
- **Compiler alias interfaces.** Modern compilers ask their alias analysis, for each call and each memory access, whether the call may modify or read that location, and use the answer for redundancy elimination and scheduling.

## References
