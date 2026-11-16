---
tag: K1QASX
kind: algorithm
slug: ifds-framework
name: IFDS framework
aliases:
- IFDS
- Reps-Horwitz-Sagiv algorithm
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: advanced
summary: Solves interprocedural, finite, distributive, subset problems exactly in O(E D^3) time by graph reachability on an exploded supergraph.
solves: [reaching-definitions, live-variable-analysis, available-expressions, very-busy-expressions]
model: word-ram
complexity:
  vars: {E: the number of edges of the supergraph, N: the number of nodes of the supergraph, D: the largest number of facts of one procedure, C: the number of call sites}
  time: {worst: O(E D^3), average: O(E D^3), best: Θ(N + E)}
  space: {extra: O(N D^2 + C D^2)}
properties: {deterministic: true, recursive: false}
prereqs: [interprocedural-dataflow-analysis, distributive-dataflow-framework, graph-reachability]
see_also: [ide-framework, functional-approach-interprocedural, cfl-reachability, context-sensitivity, taint-analysis, system-dependence-graph-slicing, pushdown-reachability, tabulation]
sources:
  - paper: doi:10.1145/199448.199462
    title: "Thomas Reps, Susan Horwitz and Mooly Sagiv, Precise interprocedural dataflow analysis via graph reachability, Proceedings of the 22nd ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '95), 49 to 61, 1995"
    locator: the IFDS problem, the exploded supergraph, the tabulation algorithm with path edges and summary edges, and its O(E D^3) bound
  - paper: doi:10.1016/0304-3975(96)00072-2
    title: "Mooly Sagiv, Thomas Reps and Susan Horwitz, Precise interprocedural dataflow analysis with applications to constant propagation, Theoretical Computer Science 167(1-2), 131 to 170, 1996"
    locator: the IDE generalization, where the edges of the exploded supergraph carry functions on values
  - paper: doi:10.1016/s0950-5849(98)00093-7
    title: "Thomas Reps, Program analysis via graph reachability, Information and Software Technology 40(11-12), 701 to 726, 1998"
    locator: IFDS as an instance of CFL-reachability, and its relation to interprocedural slicing
  - paper: doi:10.1145/77606.77608
    title: "Susan Horwitz, Thomas Reps and David Binkley, Interprocedural slicing using dependence graphs, ACM Transactions on Programming Languages and Systems 12(1), 26 to 60, 1990"
    locator: summary edges at call sites, the earlier form of the same idea for slicing
  - paper: doi:10.1007/978-3-642-11970-5_8
    title: "Nomair A. Naeem, Ondřej Lhoták and Jonathan Rodriguez, Practical extensions to the IFDS algorithm, Compiler Construction (CC 2010), Lecture Notes in Computer Science, 124 to 144, 2010"
    locator: the supergraph built on demand, unbalanced returns, and faster handling of flows into callees
  - paper: doi:10.1145/2259051.2259052
    title: "Eric Bodden, Inter-procedural data-flow analysis with IFDS/IDE and Soot, Proceedings of the ACM SIGPLAN International Workshop on State of the Art in Java Program Analysis (SOAP '12), 3 to 8, 2012"
    locator: the Heros solver, a generic IFDS and IDE solver with multi-threading
  - paper: doi:10.1145/2594291.2594299
    title: "Steven Arzt, Siegfried Rasthofer, Christian Fritz, Eric Bodden, Alexandre Bartel, Jacques Klein, Yves Le Traon, Damien Octeau and Patrick McDaniel, FlowDroid: precise context, flow, field, object-sensitive and lifecycle-aware taint analysis for Android apps, Proceedings of the 35th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '14), 259 to 269, 2014"
    locator: taint analysis as an IFDS problem with access paths as facts
  - paper: "Micha Sharir and Amir Pnueli, Two approaches to interprocedural data flow analysis, in Steven S. Muchnick and Neil D. Jones (eds.), Program Flow Analysis: Theory and Applications, Prentice-Hall, 1981"
    locator: the meet over valid paths and the functional approach that the tabulation algorithm makes concrete
---

The IFDS framework of Reps, Horwitz and Sagiv solves a large class of [interprocedural dataflow](/interprocedural-dataflow-analysis/) problems exactly. The class is in the name: Interprocedural, Finite, Distributive, Subset. The facts form a finite set $D$, an analysis result at a point is a subset of $D$, and every flow function distributes over union. Taint analysis, reaching definitions, possibly uninitialized variables and all gen-kill problems fit. The algorithm turns the problem into reachability in an *exploded supergraph*, which has one node for each pair of a program point and a fact. A fact holds at a point exactly when its node can be reached along a path whose calls and returns match. The tabulation algorithm finds these nodes with a worklist. It records *path edges* inside procedures and *summary edges* across calls, so it never walks through a procedure twice for the same fact. The answer is the meet over all valid paths, the best answer that ignores branch conditions, even with recursion. The time is $O(E D^3)$, where $E$ is the number of edges of the supergraph.

## In plain words

Many questions about a program are yes or no questions about a fixed list of facts, such as "this variable may hold a secret". IFDS answers them across procedure calls without mixing up the callers. It draws a big graph with one copy of every program point for each fact. An edge says that a fact at one point causes a fact at the next point. Then "does this fact hold here" becomes "can we walk to this node". The walk must leave each procedure back to the call it came in by. To avoid walking through a procedure again and again, the algorithm remembers, for each fact at the entry of a procedure, which facts come out at its exit. These shortcuts are the summary edges. The cost grows with the size of the program times the cube of the number of facts.

## The problem

An IFDS instance is a supergraph $G^*$ with a finite set of facts $D_p$ for each procedure $p$, a seed set $S \subseteq D_{main}$, and a flow function $f_e : 2^{D_p} \to 2^{D_q}$ for each edge $e$ with $f_e(X \cup Y) = f_e(X) \cup f_e(Y)$. The supergraph has the call edge, the return edge and the call-to-return edge of each call site, as on the [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/) page. The output is, for every node $n$,

$$\mathrm{MVP}(n) = \bigcup \{ f_\pi(S) : \pi \text{ a valid path from } s_{main} \text{ to } n \},$$

where a path is valid when every return goes back to the call that its procedure was entered from. Sets of facts are ordered by $\supseteq$, so union is the meet and $\emptyset$ is $\top$: this is the meet convention of Kildall, and the result is the greatest solution. In the join convention of Cousot the order flips, union is the join, and the same set is the least solution. A problem whose meet is intersection, such as available expressions, fits after a change to the complement facts, since the complement of a distributive intersection problem is a distributive union problem.

The implementation solves a taint problem on the toy IR. The question is which variables may depend on the first parameter of `main`. It follows data flow only, not branches.

| item | choice |
|---|---|
| facts of $p$ | the variables of $p$, and `RET` for its return value |
| seed | the first parameter of `main` |
| `x = k` | kills `x` |
| `x = a` | `a` gives `a` and `x`; `x` itself dies unless it is `a` |
| `x = a op b` | each operand gives itself and `x`; `x` itself dies unless it is an operand |
| `ret a` | every fact stays; `a` also gives `RET` |
| call edge of `x = call q(a, b)` | an argument gives the parameters it is passed to |
| call-to-return edge | every fact of the caller stays, except `x` |
| return edge | `RET` gives `x`; nothing else crosses |
| `jump`, `br` | every fact stays |

## The algorithm

**The exploded supergraph.** A distributive function on subsets is fixed by what it does to each single fact and to the empty set. So draw it as a bipartite graph on $D \cup \{\mathbf{0}\}$. The extra fact $\mathbf{0}$ always holds. There is an edge $\mathbf{0} \to \mathbf{0}$, an edge $\mathbf{0} \to d'$ for every $d'$ that $f$ makes from nothing, and an edge $d \to d'$ for every $d' \in f(\{d\})$. The facts reachable from $X \cup \{\mathbf{0}\}$ are then $f(X) \cup \{\mathbf{0}\}$, and composing two functions is joining their graphs end to end. The exploded supergraph $G^\#$ puts these small graphs on every edge of $G^*$. Its nodes are the pairs $\langle n, d \rangle$.

| flow function | edges out of $\langle n, d \rangle$ |
|---|---|
| identity | $d \to d$ for every $d$ |
| kill `x` | $d \to d$ for $d \ne x$; no edge out of `x` |
| gen `x` | $\mathbf{0} \to x$, plus the identity |
| copy `x = a` | `a` $\to$ `a`, `a` $\to$ `x`, $d \to d$ for $d \ne x$ |

**Tabulation.** The algorithm does not build $G^\#$. It finds the reachable part with a worklist. A *path edge* $(n, d_1, d_2)$ says that $\langle n, d_2 \rangle$ can be reached from $\langle s_p, d_1 \rangle$, the start of its own procedure, by a same-level path, which is a path whose calls all return inside it. A *summary edge* $(c, d_4, d_5)$ says that a call at $c$ with the fact $d_4$ can come back at the return site with the fact $d_5$. Summary edges are found once per call site and used by every caller context that reaches the call with the same fact.

```pseudo id=main
TABULATE(G*, F, S)    F gives the flow of each edge one fact at a time; S is the seed set
L1  PathEdge ← ∅; WorkList ← []; Summary ← ∅; Through ← ∅
L2  for each d in S ∪ {0} do PROPAGATE(s_main, d, d)
L3  while WorkList is not empty do
L4      (n, d1, d2) ← remove the first item of WorkList          (n is in procedure p)
L5      if n is a call node c, with callee q and return site r then
L6          for each d3 in F_call(c)(d2) do PROPAGATE(s_q, d3, d3)
L7          for each d3 in F_c2r(c)(d2) ∪ Summary[c, d2] do PROPAGATE(r, d1, d3)
L8      else if n is the exit node e_p then
L9          for each call node c of p, with return site r, and each d5 in F_ret(c)(d2) do
L10             if (c, d1, d5) is in Through then skip it, else add it to Through
L11             for each d4 with d1 in F_call(c)(d4) do
L12                 if d5 is not in Summary[c, d4] then add it
L13                     for each d3 with (c, d3, d4) in PathEdge do PROPAGATE(r, d3, d5)
L14     else for each successor m of n and each d3 in F_(n,m)(d2) do PROPAGATE(m, d1, d3)
L15 return X, with X[n] = {d ≠ 0 : (n, d1, d) is in PathEdge for some d1}

PROPAGATE(n, d1, d2)
L16 if (n, d1, d2) is not in PathEdge then add it to PathEdge and append it to WorkList
```

Line L6 starts the callee with a self loop, so the callee is analysed once per entry fact, not once per caller. Line L7 does two things. It carries the caller's facts around the call, and it reuses every summary that is already known. When a fact reaches the exit (L8 to L13), the algorithm turns it into summary edges at every call site of the procedure. It then extends every path edge that already reaches that call with the matching fact.

The set $Through$ of line L10 is not in the pseudocode of the paper. Without it, a direct count of the exit case gives $D^4$ steps per call site. Line L13 needs, for each pair $(c, d_4)$, the set of $d_3$ with a path edge to $\langle c, d_4 \rangle$. The implementation keeps this index next to $PathEdge$.

## Example

This is the program of the [interprocedural dataflow analysis](/interprocedural-dataflow-analysis/) page, in the toy IR. The seed is `secret`.

```text
id(a):          B0: ret a
main(secret):   B0: x = call id(secret)      c1
                    y = call id(0)           c2, also the return site of c1
                    ret y                    the return site of c2
```

The worklist is a queue. The steps, with $\mathbf{0}$ written as 0:

| step | item taken | new path edges and summary edges |
|---|---|---|
| L2 | | $(c_1, secret, secret)$, $(c_1, 0, 0)$ |
| 1 | $(c_1, secret, secret)$ | L6: $(s_{id}, a, a)$. L7: $(c_2, secret, secret)$ |
| 2 | $(c_1, 0, 0)$ | L6: $(s_{id}, 0, 0)$. L7: $(c_2, 0, 0)$ |
| 3 | $(s_{id}, a, a)$ | L14 through `ret a`: $(e_{id}, a, a)$, $(e_{id}, a, RET)$ |
| 4 | $(c_2, secret, secret)$ | L6: none, the argument is a constant. L7: $(r_2, secret, secret)$ |
| 5, 6 | $(s_{id}, 0, 0)$, $(c_2, 0, 0)$ | $(e_{id}, 0, 0)$, $(r_2, 0, 0)$ |
| 7 | $(e_{id}, a, a)$ | none: the return edge passes only $RET$ |
| 8 | $(e_{id}, a, RET)$ | at $c_1$: $RET$ gives `x`, and $a$ came from `secret`. Summary $(c_1, secret, x)$, path edge $(c_2, secret, x)$. At $c_2$: no fact of `main` gives $a$, so no summary |
| 9, 10 | $(r_2, secret, secret)$, $(e_{id}, 0, 0)$ | $(e_{main}, secret, secret)$; summaries $(c_1, 0, 0)$ and $(c_2, 0, 0)$ |
| 11 to 16 | the rest | $(r_2, secret, x)$ from L7 at $c_2$, then the exit of `main` |

In total there are 16 path edges, 3 summary edges and 24 flow steps.

The result is $\{secret, x\}$ after each call, and `y` is never tainted. A context-insensitive analysis of the same supergraph lets `RET` flow from the exit of `id` to both return sites, so it reports `y` as tainted. The tabulation avoids this. A summary edge exists only at a call site whose own arguments reach the fact at the entry of `id`.

## Correctness

The full proof is in the proof file. Its steps:

1. **One path, many facts.** Following a path $\pi$ of the supergraph through the exploded graph from $X \cup \{\mathbf{0}\}$ reaches exactly $f_\pi(X) \cup \{\mathbf{0}\}$. The proof is an induction on the length of $\pi$.
2. **MVP is reachability.** Valid paths of $G^\#$ are the valid paths of $G^*$ with a fact at each node. So $d \in \mathrm{MVP}(n)$ exactly when a valid path reaches $\langle n, d \rangle$ from a seed or from $\langle s_{main}, \mathbf{0} \rangle$.
3. **Path edges and summary edges are sound.** Each insertion extends a path that already exists by one edge or by a summary edge, and each summary edge is a call edge, a same-level path in the callee and the return edge of the same call site. The proof is an induction on the order of insertion.
4. **Path edges are complete.** Every valid path to $\langle n, d_2 \rangle$ ends with a same-level part that starts at some $\langle s_p, d_1 \rangle$, and $(n, d_1, d_2)$ is found. The proof is an induction on the length of the path. The hard case ends with a return edge. Then the summary edge is found at the exit, and it meets the path edge at the call either at L7 or at L13, whichever runs later.
5. **The result.** Steps 3 and 4 show that the targets of the path edges are exactly the reachable nodes of $G^\#$. With step 2 this gives $X = \mathrm{MVP}$.
6. **Termination and cost.** Each path edge enters the worklist once, and there are at most $(D+1)^2$ per node. The cost bound counts the work of each kind of node.

## Complexity

- **Ordinary nodes.** A node has at most $(D+1)^2$ path edges. Each is taken once and gives at most $D + 1$ new items per outgoing edge. Over all nodes this is $O(E D^3)$.
- **Call nodes.** Each path edge gives at most $3(D+1)$ items at L6 and L7, so $O(D^3)$ per call site.
- **Exit nodes.** Each path edge gives at most $D + 1$ tests at L10 per call site. Each new triple of $Through$ runs over at most $D + 1$ facts at L11, and each new summary edge over at most $D + 1$ sources at L13. Each of these costs $O(D^3)$ per call site.
- **Total.** $O(E D^3)$ time with hash sets. Space is $O(N D^2)$ for the path edges and $O(C D^2)$ for the summary edges, where $C$ is the number of call sites.
- **Special cases.** Reps, Horwitz and Sagiv also give smaller bounds for special classes. For a gen-kill problem every fact flows only to itself, so a node has $O(D)$ path edges, and the time is $O(E D)$. A flow function where each fact reaches only a few facts also costs less than $D^3$ per edge.
- **Best case.** Building the supergraph reads the whole program, $\Theta(N + E)$, even when only the fact $\mathbf{0}$ is ever reached.

The tables below are *measured*, not proved. The first has random modules of the toy IR with loops and recursion. `f0` calls `f1`, each `fi` calls `f(i+1)` and one random procedure, and the seeds are both parameters of `f0`.

| procedures | variables | $N$ | $E$ | $D$ | path edges | summary edges | flow steps | $E (D+1)^3$ | ms |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 4 | 133 | 155 | 15 | 413 | 8 | 466 | 634880 | 0.6 |
| 16 | 4 | 517 | 605 | 15 | 1785 | 46 | 2047 | 2478080 | 3.2 |
| 64 | 4 | 2036 | 2401 | 15 | 6155 | 161 | 7153 | 9834496 | 8.2 |
| 64 | 8 | 2321 | 2696 | 19 | 2546 | 128 | 3195 | 21568000 | 3.7 |
| 64 | 16 | 2752 | 3111 | 27 | 2917 | 128 | 3543 | 68292672 | 4.5 |

The taint dies quickly in these programs, because constants and loop counters overwrite it. So the work grows with the program and stays far below the bound. The second table is a worst case for the number of path edges. A procedure `g` with $k$ parameters mixes all of them in a loop, so every entry fact reaches every variable. `main` calls `g` twice.

| $k$ | $N$ | $E$ | $D$ | path edges | $N (D+1)^2$ | flow steps | $E (D+1)^3$ | ms |
|---|---|---|---|---|---|---|---|---|
| 4 | 12 | 15 | 5 | 167 | 432 | 217 | 3240 | 0.3 |
| 8 | 16 | 19 | 9 | 811 | 1600 | 937 | 19000 | 1.0 |
| 16 | 24 | 27 | 17 | 5075 | 7776 | 5449 | 157464 | 5.4 |
| 32 | 40 | 43 | 33 | 36259 | 46240 | 37513 | 1690072 | 39.1 |

Here the path edges come close to $N (D+1)^2$. The flow steps stay near the number of path edges, because a taint flow sends each fact to at most two facts. A problem whose flow functions send one fact to many facts pays the full factor $D$ on top.

## Properties

- **Exact.** For a distributive problem the result is the meet over all valid paths, with and without recursion. Context-insensitive analysis can only be less precise.
- **Order free.** The set of path edges at the end does not depend on the order of the worklist.
- **Per fact.** Facts are tracked one at a time. The seeds $S \cup T$ give the union of the results for $S$ and for $T$.
- **Reuse.** A procedure is analysed once per entry fact, and its summary edges serve every caller that reaches the call with that fact.
- **Only what is reached.** Procedures and facts that no valid path reaches cost nothing beyond building the supergraph.

## Variants and improvements

- **IDE.** The [IDE framework](/ide-framework/) puts a function on values on each exploded edge. It solves environment problems such as linear constant propagation in the same time bound.
- **Practical extensions.** Naeem, Lhoták and Rodriguez build the supergraph on demand, return from the start procedure to all callers when a seed is not in `main`, and avoid repeated work for facts that pass into a callee.
- **Solvers.** Heros (Bodden 2012) is a generic multi-threaded solver for IFDS and IDE on Soot. FlowDroid (Arzt et al. 2014) runs taint analysis of Android apps as an IFDS problem, with access paths such as `x.f.g` as facts, and adds an alias search on demand.
- **Demand queries.** A query for one node and one fact can run the reachability backwards from that node, so only the part of the graph that can matter is explored.
- **Other forms.** The same problems are CFL-reachability problems over the language of matched calls and returns, see [CFL-reachability](/cfl-reachability/). They are also reachability in a [pushdown system](/pushdown-reachability/), and Datalog programs can express the tabulation directly.

## When to use it

Use IFDS when the facts are a finite set that you can list per procedure, every flow function is a union of effects of single facts, and you need precision across calls. Taint and information flow, uninitialized variables, interprocedural reaching definitions, and typestate with a small set of states are typical. If you need values, such as constants, use IDE. If the flow functions are not distributive, a [functional approach](/functional-approach-interprocedural/) with general summaries or [context sensitivity](/context-sensitivity/) with call strings is the choice.

## Pitfalls

- **Large fact sets.** The bound has $D^3$, and $D$ can be large. With access paths as facts, the number of facts grows quickly, so tools cut access paths at a fixed length.
- **No $\mathbf{0}$.** Without the fact $\mathbf{0}$, a fact that a statement makes from nothing never appears. Every edge must also map $\mathbf{0}$ to $\mathbf{0}$, or whole regions of the graph go missing.
- **Locals through the callee.** The caller's locals belong on the call-to-return edge. If the call edge passes them into the callee, every callee must carry every caller local back, which costs more and can lose precision.
- **Facts that need two inputs.** A distributive function treats each fact alone. "x is constant if a and b are constant" needs two facts at once, and IFDS cannot express it. IDE cannot either, since `x = a + b` is not distributive over its value lattice and IDE sends `x` to $\bot$. Use a non-distributive method.
- **Seeds outside main.** If the analysis starts inside a procedure, the facts at its exit must return to every caller, with no matching call. Forgetting this loses results.
- **Data flow only.** The taint instance here does not follow branches. A secret that only decides which constant is stored does not taint the result.

## Implementations

## History

Sharir and Pnueli (1981) defined the meet over valid paths and the functional approach, which computes the effect of each procedure as a function. Knoop and Steffen (1992) proved the interprocedural coincidence theorem for distributive problems. Horwitz, Reps and Binkley (1990) had already used summary edges at call sites for interprocedural slicing. Reps, Horwitz and Sagiv (POPL 1995) combined these ideas. They noted that a distributive function on a finite set of facts is a small graph, so the functional approach becomes reachability in an exploded supergraph, and they gave the tabulation algorithm with its $O(E D^3)$ bound. Sagiv, Reps and Horwitz (1996) extended it to IDE. Reps (1998) presented both as CFL-reachability. Naeem, Lhoták and Rodriguez (2010) made the algorithm practical for large programs. The Heros solver (2012) and FlowDroid (2014) brought it into wide use for Java and Android.

## References
