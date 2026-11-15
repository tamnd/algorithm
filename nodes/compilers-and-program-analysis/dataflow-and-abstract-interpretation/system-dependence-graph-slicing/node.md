---
tag: 6EV9PV
kind: algorithm
slug: system-dependence-graph-slicing
name: System dependence graph slicing
aliases:
- Horwitz-Reps-Binkley slicing
- interprocedural slicing
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Slices across procedures with a system dependence graph and summary edges, in two passes that respect calling context.
solves: [program-slicing]
model: word-ram
complexity:
  vars: {N: the number of nodes of the system dependence graph, E: the number of its edges including summary edges}
  time: {worst: O(N + E)}
  space: {extra: O(N + E)}
properties: {deterministic: true, recursive: false, online: false, context_sensitive: true, executable_result: false}
history:
  year: 1988
  people: [Susan Horwitz, Thomas Reps, David Binkley]
  note: Horwitz, Reps and Binkley joined the dependence graphs of the procedures into one graph and added summary edges, so that a slice no longer mixes the calls of a procedure from different places.
prereqs: [pdg-slicing, program-dependence-graph, call-graph]
see_also: [weiser-slicing, dynamic-slicing, cfl-reachability, dyck-language, ifds-framework, context-sensitivity, functional-approach-interprocedural, attribute-grammar]
sources:
  - paper: doi:10.1145/53990.53994
    title: Susan Horwitz, Thomas Reps and David Binkley, Interprocedural slicing using dependence graphs, Proceedings of the ACM SIGPLAN 1988 Conference on Programming Language Design and Implementation, ACM SIGPLAN Notices 23(7), 1988, pages 35-46
    locator: the system dependence graph, summary edges from a linkage grammar, and the two-pass slice
  - paper: doi:10.1145/77606.77608
    title: Susan Horwitz, Thomas Reps and David Binkley, Interprocedural slicing using dependence graphs, ACM Transactions on Programming Languages and Systems 12(1), 1990, pages 26-60
    locator: the journal version, with the calling-context problem, the graph, the two passes and their precision
  - paper: doi:10.1145/195274.195287
    title: Thomas Reps, Susan Horwitz, Mooly Sagiv and Genevieve Rosay, Speeding up slicing, ACM SIGSOFT Software Engineering Notes 19(5) (FSE '94), 1994, pages 11-20
    locator: the work-list method with path edges that computes the summary edges, used here
  - paper: doi:10.1145/176454.176473
    title: David Binkley, Precise executable interprocedural slices, ACM Letters on Programming Languages and Systems 2(1-4), 1993, pages 31-45
    locator: parameter mismatch, and how to extend the slice so that it runs
  - paper: doi:10.1016/S0950-5849(98)00093-7
    title: Thomas Reps, Program analysis via graph reachability, Information and Software Technology 40(11-12), 1998, pages 701-726
    locator: interprocedural slicing as reachability along paths whose calls and returns match like parentheses
  - paper: doi:10.1109/TSE.1984.5010248
    title: Mark Weiser, Program slicing, IEEE Transactions on Software Engineering SE-10(4), 1984, pages 352-357
    locator: the first interprocedural slices, which do not keep apart the calling contexts of a procedure
---

System dependence graph slicing solves the [program slicing](/program-slicing/) problem for programs with procedures. Horwitz, Reps and Binkley (1988) joined the [program dependence graphs](/program-dependence-graph/) of all procedures into one *system dependence graph* (SDG), with edges for calls, for passing arguments in and for passing results out. A plain backward search in this graph is wrong in a useful way: it enters a procedure from one call site and leaves it through another, so it mixes calling contexts and gives slices that are too large. The fix has two parts. *Summary edges* at each call site record which arguments the result depends on. Then the slice is two searches: the first never descends into a callee and the second never climbs to a caller. The result is exactly the set of nodes that reach the criterion along paths whose calls and returns match.

## In plain words

Each procedure has its own map of which line feeds which line. Join the maps: draw arrows from each call to the procedure it calls, from each argument to the parameter it fills, and from the returned value back to the call. Now walk the arrows backward from the line you care about. The danger is that you go into a procedure through one call and come out through another call, which no run can do. So first find, for every call, which arguments the result needs, and draw a short arrow for that. Then walk in two rounds. In the first round, climb out to callers and use the short arrows, but never go down into a procedure. In the second round, go down into procedures, but never climb out. Nothing you reach comes from a mixed-up path.

## The problem

A *system* is a set of procedures in the toy IR, one of them `main`. A procedure has parameters, uses `x = k`, `x = y`, `x = a op b` and `x = call f(a, b, ...)`, and ends each path with a `ret`. Arguments are passed by value and the only result of a call is the value its callee returns. A criterion is $\langle P, p, V \rangle$: the values of the variables of $V$ just before statement $p$ of procedure $P$, in every activation of $P$. The output is the set of statements of all procedures that can affect those values through data and control dependence along paths that a run could follow, that is, paths in which each return goes back to the call site that made the call.

The SDG has, for each procedure $Q$, the nodes of its program dependence graph and:

- an *entry* node, the ENTRY of the PDG of $Q$;
- one *formal-in* node per parameter, control dependent on entry, which defines that parameter;
- one *formal-out* node for the returned value, with a data edge from each `ret` statement.

Each call statement is a *call node* with one *actual-in* node per argument and one *actual-out* node for the result. These are control dependent on the call node. An actual-in reads its argument, so it has data edges from the definitions that reach the call. The actual-out defines the target of the call, so the later uses have data edges from it. Between procedures:

- a *call edge* from the call node to the entry of the callee;
- a *parameter-in edge* from actual-in $k$ to formal-in $k$ of the callee;
- a *parameter-out edge* from the formal-out of the callee to the actual-out.

A *summary edge* goes from actual-in $k$ to the actual-out of the same call site when, inside the callee, a path with matched calls and returns goes from formal-in $k$ to the formal-out.

## The algorithm

Mark each call or parameter-in edge at site $c$ as an open parenthesis $(_c$ and each parameter-out edge at $c$ as a close $)_c$. A path is *realizable* if no close meets an open of another site and no unmatched close comes after an unmatched open. It is *same-level* if all of its parentheses match. SUMMARY-EDGES is the method of Reps, Horwitz, Sagiv and Rosay (1994). A *path edge* $(v, w)$ records that a same-level path goes from $v$ to the formal-out $w$ of the procedure of $v$.

```pseudo id=main
SDG-SLICE(G, C)
L1  W <- the parents of the criterion C; S <- W
L2  while W is not empty do                          (pass 1: climb to callers)
L3      remove a node n from W
L4      for each edge m -> n of G that is not a parameter-out edge do
L5          if m is not in S then add m to S and to W
L6  W <- S                                           (pass 2: go down into callees)
L7  while W is not empty do
L8      remove a node n from W
L9      for each edge m -> n of G that is not a parameter-in edge or a call edge do
L10         if m is not in S then add m to S and to W
L11 return S

SUMMARY-EDGES(G)
L12 for each formal-out node w do PROPAGATE(w, w)
L13 while the work list is not empty do
L14     remove a path edge (v, w) from the work list
L15     if v is the formal-in node for parameter k of procedure Q then
L16         for each call site c of Q, with actual-in a for parameter k and actual-out o do
L17             if a -> o is not a summary edge then add it, and PROPAGATE(a, x) for each path edge (o, x)
L18     else for each intraprocedural edge or summary edge x -> v do PROPAGATE(x, w)
L19 return the summary edges

PROPAGATE(v, w): if (v, w) is not a path edge then make it one and put it in the work list
```

The parents of the criterion in line L1 are the definitions of $V$ that reach $p$, with the actual-out node standing for a call that defines a variable and a formal-in node for a parameter, and the control parents of $p$. Lines L2 to L5 can climb from a callee to every caller, because the criterion holds in every calling context. They cross calls only by summary edges. Lines L7 to L10 go down from each actual-out to the formal-out of the callee and on into it, and they cross deeper calls again only by summary edges, never climbing back out.

In the implementation, `build_sdg` builds the graph with the per-procedure parts of the [PDG slicing](/pdg-slicing/) page, `summary_edges` is lines L12 to L19, `sdg_slice` is lines L1 to L11, and `reachability_slice` is the naive search, kept for comparison.

## Example

The procedure `add(a, b)` returns $a + b$. `main(n)` uses it twice per loop trip: once to add $i$ to the sum $s$ and once to step $i$.

```
main(n):                         add(a, b):
B1:                              B1:
  s = 0                            r = a + b
  i = 0                            ret r
  jump B2
B2:
  t = i < n
  br t B3 B4
B3:
  s = call add(s, i)
  i = call add(i, 1)
  jump B2
B4:
  ret i
```

**Summary edges.** In `add`, both formal-ins reach the formal-out through `r = a + b` and `ret r`. So each of the two call sites gets two summary edges, from the actual-in of each argument to its actual-out.

**The slice for $\langle main, (B4, 0), \{i\} \rangle$.** The definitions of $i$ that reach B4 are `i = 0` and the actual-out of the second call; B4 runs on every run, so its control parent is the entry of `main`.

| pass | node reached | through |
|---|---|---|
| 1 | actual-in `i` and actual-in `1` of `i = call add(i, 1)` | summary edges into its actual-out |
| 1 | call node `i = call add(i, 1)` | control edge to its actual-in and actual-out |
| 1 | `br t B3 B4`, `t = i < n`, formal-in `n` | control and data edges |
| 2 | formal-out of `add`, `ret r`, `r = a + b`, formal-ins `a` and `b` | parameter-out edge of the second call, then data edges |

Pass 2 stops at the formal-ins of `add`: it does not climb along the parameter-in edges. So the slice is `i = 0`, `t = i < n`, `br t B3 B4` and `i = call add(i, 1)` in `main`, and `r = a + b` and `ret r` in `add`. The statements of $s$ are not in it.

A plain backward search over all edges reaches formal-in `a` of `add` and then follows both parameter-in edges into it. The one from the first call leads to actual-in `s`, then to `s = 0` and to `s = call add(s, i)`. That path enters `add` from the second call and leaves it through the first, which no run does. The naive slice has 8 statements, the SDG slice 6.

## Correctness

The full proof is in the proof file. Its steps:

1. **Path edges are sound.** Each pair that SUMMARY-EDGES adds has a same-level path behind it, by induction on the order of addition.
2. **Path edges are complete.** By induction on the length of a same-level path from $v$ to the formal-out: the first edge is either intraprocedural, or a parameter-in or call edge whose matching return is at the same site. In the second case the callee part gives a summary edge, and the work list adds the pair whichever of the two facts comes first.
3. **Summary edges are exact.** A summary edge exists if and only if a same-level path joins the formal-in to the formal-out of the callee.
4. **Two passes are exact.** Pass 1 reaches the nodes with a path made of opens, summary edges and intraprocedural edges; pass 2 adds the nodes with a path of closes and summary edges to one of them. Replacing summary edges by same-level paths shows each such node has a realizable path. Conversely, cut a realizable path after its last unmatched close and replace each matched pair by a summary edge (or by the control edge from the call node to the actual-out): the tail becomes a pass-1 path and the head a pass-2 path.

So the slice is the set of nodes with a realizable path to the criterion. That is not the same as minimal: a realizable path may still be one that no input follows.

## Complexity

**Proved, for the model here.** Each procedure has one formal-out, so a path edge is determined by its first node and there are at most $N$ of them. Each enters the work list once and costs the number of edges into its first node, or for a formal-in the number of call sites of its procedure. Summary edges are added once. So SUMMARY-EDGES takes $O(N + E)$, and each pass of SDG-SLICE takes $O(N + E)$ like any graph search. With $g$ formal-outs per procedure, for global variables or reference parameters, the same count gives $O(g (N + E))$ for the summary edges.

**Building the graph.** The per-procedure parts cost what the [program dependence graph](/program-dependence-graph/) costs: post-dominators, control dependence and reaching definitions, and the data edges can be quadratic in the size of a procedure. The summary edges are built once and serve every slice.

**Compared.** Horwitz, Reps and Binkley built summary edges from a linkage grammar, an [attribute grammar](/attribute-grammar/) whose productions are the calls. Reps, Horwitz, Sagiv and Rosay (1994) replaced it with the work-list method above, which is asymptotically faster and was also faster on their test programs. Inlining every call and slicing one big graph also respects context, but it grows exponentially with the depth of calls and fails for recursion.

## Properties

- **Context-sensitive.** No path in the slice enters a procedure at one call site and returns to another. This holds with recursion too, because summary edges are a fixed point, not an unrolling.
- **Exact for the graph.** The slice is exactly the set of nodes on realizable paths to the criterion, as the tests check against a graph with one copy of each procedure per calling context, and against the PDG slice of the program with every call inlined.
- **One graph, many slices.** Summary edges depend only on the program, not on the criterion.
- **Not a program.** As with the [PDG slice](/pdg-slicing/), the result is a set of nodes. Across procedures there is one more problem, parameter mismatch: the slice of a procedure can need an argument at one call site that another call site in the slice does not pass.
- **Static.** It holds for every input and every calling context; a [dynamic slice](/dynamic-slicing/) holds for one run.

## Variants and improvements

- **Executable slices.** Binkley (1993) adds to the slice the actual-in nodes, and the statements they depend on, that a callee needs at every kept call site, so that each kept call passes every parameter that the sliced callee reads.
- **Faster summary edges.** The path-edge work list of Reps, Horwitz, Sagiv and Rosay replaced the linkage grammar. The same idea, tabulating same-level paths per procedure, is the core of the [IFDS framework](/ifds-framework/).
- **As CFL-reachability.** Reps (1998) states the problem as [CFL-reachability](/cfl-reachability/) with the matched parentheses of a [Dyck language](/dyck-language/), the form used by many later analyses.
- **Forward slices and chops.** The same graph and summary edges give forward slices by searching along the edges, and precise interprocedural chops between two statements, studied by Reps and Rosay.
- **Specialization slicing.** When one procedure needs different parts at different call sites, a slicer can make one copy of the procedure per needed part instead of taking the union.

## When to use it

Use it for slicing programs with procedures when the slice must not mix calling contexts: debuggers, program understanding tools, change impact analysis and integration of program versions. The context-insensitive search is simpler and enough when procedures are small or called from one place. When the slice must run, add Binkley's step. When one run matters and not all inputs, use [dynamic slicing](/dynamic-slicing/).

## Pitfalls

- **Searching the joined graph in one pass.** It enters a procedure at one call and leaves at another, and the slice grows with statements no run connects to the criterion, like the statements of $s$ in the example.
- **Climbing in pass 2.** If pass 2 follows parameter-in or call edges, it walks out of the callee into every caller and the context sensitivity is lost.
- **Forgetting the call node in pass 2.** The actual-out depends on the call node, so the call statement is in the slice whenever its result is. Without that control edge the call disappears and the callee code in the slice never runs.
- **Slicing an inlined program with loops.** If a call sits in a loop and is inlined, the locals of the callee must be killed at each inlined entry, or the dependence of one activation leaks into the next and the slice grows.
- **Expecting a runnable program.** The slice can call a procedure that needs an argument the slice does not compute at that call site. Binkley's extension fixes this.
- **Reading the slice as minimal.** Realizable paths can still be infeasible, so the slice can contain statements that no run needs.

## Implementations

## History

Weiser's 1984 paper already sliced across procedures, by passing criteria from callers to callees and back, but it did not keep the calling contexts apart, so a procedure called from two places joined their slices. Horwitz, Reps and Binkley presented the system dependence graph and the two-pass slice at PLDI 1988, with summary edges built from a linkage grammar, and gave the full treatment in TOPLAS in 1990. Binkley (1993) showed how to make the slices run. Reps, Horwitz, Sagiv and Rosay (1994) gave the faster work-list method for summary edges, and Reps (1998) placed the method within CFL-reachability, next to interprocedural dataflow analysis and some pointer analyses. The PLDI paper was later chosen among the most influential papers of the first twenty years of the conference.

## References
