---
tag: DDXZCS
kind: algorithm
slug: online-cycle-elimination
name: Online cycle elimination
aliases:
- cycle elimination in inclusion constraints
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Detects cycles in an inclusion constraint graph while solving and merges their nodes, since all nodes on a cycle have equal sets.
solves: [points-to-analysis]
model: word-ram
complexity:
  vars: {n: the number of variables (each variable is also a location), m: the number of pointer statements}
  time: {worst: O(n^4 + n^2 m)}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, recursive: false, online: true, flow_sensitive: false, context_sensitive: false}
history:
  year: 1998
  people: [Manuel Fähndrich, Jeffrey S. Foster, Zhendong Su, Alexander Aiken]
  note: Fähndrich, Foster, Su and Aiken added a cheap partial search for cycles to an inclusion constraint solver and made Andersen-style analysis of large C programs practical.
prereqs: [depth-first-search, disjoint-set-forest, andersen-analysis]
see_also: [hybrid-cycle-detection, offline-variable-substitution, steensgaard-analysis, strongly-connected-components, tarjan-scc, transitive-closure, points-to-analysis]
sources:
  - paper: doi:10.1145/277650.277667
    title: Manuel Fähndrich, Jeffrey S. Foster, Zhendong Su and Alexander Aiken, Partial online cycle elimination in inclusion constraint graphs, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '98), 85 to 96, 1998
    locator: whole paper (the inductive form of the constraint graph, the partial search for cycles along chains of variables in index order, and the measurements on C programs)
  - paper: doi:10.1145/1250734.1250767
    title: Ben Hardekopf and Calvin Lin, The ant and the grasshopper, fast and accurate pointer analysis for millions of lines of code, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '07), 290 to 299, 2007
    locator: the section on earlier cycle detection methods and the comparison of online and lazy detection
  - paper: "Lars Ole Andersen, Program Analysis and Specialization for the C Programming Language, PhD thesis, DIKU, University of Copenhagen, 1994 (DIKU report 94/19)"
    locator: the chapter on pointer analysis (the inclusion constraints that the solver works on)
---

Online cycle elimination speeds up [Andersen's analysis](/andersen-analysis/) without a change to its result. Andersen's analysis keeps a graph with an edge $u \to v$ for each subset constraint $pts(u) \subseteq pts(v)$. If the edges form a cycle, every node on it must end with the same set, so the solver can merge the nodes into one and keep one set for all of them. The online method checks for a new cycle each time it adds an edge, while the solver runs, and merges the nodes at once with a [disjoint-set forest](/disjoint-set-forest/). Fähndrich, Foster, Su and Aiken (1998) showed that a cheap, partial search for these cycles makes the analysis of large C programs much faster. This page gives a version with a full search, which finds every cycle.

## In plain words

Andersen's analysis draws arrows between pointers. An arrow from one pointer to another says that the second can hold every address that the first can hold. If arrows go around a circle, each pointer on the circle can hold the addresses of all the others, so all of them end with the same list. Then there is no need to keep a separate list for each one and to send each new address around the circle again and again. The method looks for a circle each time it draws a new arrow. When it finds one, it joins all the pointers on the circle into one group with one shared list. The final lists are the same as those of Andersen's analysis. Only the work to find them is less.

## The problem

The input is a set of statements in the four basic forms `p = &a`, `p = q`, `p = *q` and `*p = q` over $n$ variables, and the output is the least solution $L$ of the subset constraints of Andersen's analysis, as on the page of the [points-to analysis](/points-to-analysis/) problem. The analysis uses the subset order on each set, with the empty sets as bottom, in the direction of Cousot: smaller is more precise. It is flow-insensitive: it ignores the order of the statements, but the statements themselves come from the control flow of the program.

The fact that makes the method work: if the constraint graph has a path $u \to^* v$, then $L(u) \subseteq L(v)$, because inclusion is transitive. So on a cycle, $L$ is the same at every node. Merging the nodes of a cycle into one node, with one set, gives a smaller system with the same least solution. The *nodes* are merged; the *locations* stay distinct. If `q` and `r` are merged, a pointer that holds the address of `q` does not also hold the address of `r`.

## The algorithm

The solver is Andersen's worklist solver over the roots of a union-find forest. FIND gives the root of the class of a variable. ADD-EDGE adds the edge, then searches for the roots on a path back from the new target to the new source.

```pseudo id=main
OCE(S)
L1  for each variable v do parent[v] <- v; pts[v] <- {}; succ[v] <- {}
L2  for each p = &a in S do add a to pts[p]; add p to W
L3  for each p = q in S do ADD-EDGE(q, p)
L4  while W is not empty do
L5      take n from W; if FIND(n) is not n then go to the next n
L6      for each a in pts[n] do
L7          for each p = *y in S with FIND(y) = n do ADD-EDGE(a, p)
L8          for each *y = q in S with FIND(y) = n do ADD-EDGE(q, a)
L9      for each w in succ[n] do copy pts[n] into pts[FIND(w)]; if it grew, add FIND(w) to W
L10 return pts[FIND(v)] for each variable v

ADD-EDGE(u, v)
L11 u <- FIND(u); v <- FIND(v); if u = v or v is in succ[u] then return
L12 add v to succ[u]
L13 C <- the roots on some path from v to u
L14 if C is not empty then COLLAPSE(C, u); return
L15 copy pts[u] into pts[v]; if it grew, add v to W

COLLAPSE(C, r)
L16 for each x in C other than r do
L17     parent[x] <- r; add pts[x], succ[x] and the loads and stores of x to those of r
L18 succ[r] <- {FIND(w) : w in succ[r]} without r; add r to W
```

Line L13 is two [depth-first searches](/depth-first-search/): one forward from $v$, and one backward from $u$ inside the part that the first reached. The roots on some path from $v$ to $u$ are the roots that both searches visit. The merged root is pushed on the worklist in line L18, so its loads and stores are processed for the union of the sets. The implementation keeps the loads and stores of each root in tables, so lines L7 and L8 look only at the statements of the class $n$.

## Example

The program, in the toy IR:

```
entry:
  p = &a
  a = &x
  q = *p
  r = q
  a = r
  s = &b
  r = s
  ret 0
```

The copies give the edges $q \to r$, $r \to a$ and $s \to r$. The load `q = *p` gives the edge $a \to q$ once $a$ is in the set of $p$, and that edge closes the cycle $a \to q \to r \to a$.

| step | line | what happens |
|---|---|---|
| 1 | L2 | $pts(p) = \{a\}$, $pts(a) = \{x\}$, $pts(s) = \{b\}$; the worklist is $p, a, s$ |
| 2 | L3 | `r = q`: edge $q \to r$; no path from $r$ to $q$ |
| 3 | L3 | `a = r`: edge $r \to a$; no path from $a$ to $r$ |
| 4 | L3 | `r = s`: edge $s \to r$; no path back; $pts(r) = \{b\}$; $r$ joins the worklist |
| 5 | L7 | take $p$: $a \in pts(p)$ and `q = *p` give ADD-EDGE$(a, q)$; the search from $q$ finds $q \to r \to a$, so $C = \{a, q, r\}$ |
| 6 | L16 to L18 | $q$ and $r$ merge into $a$: $pts(a) = \{x\} \cup \{b\} = \{x, b\}$; the edges inside $C$ disappear |
| 7 | L9 | take $a$: no loads, stores or edges |
| 8 | L9 | take $s$: the edge $s \to r$ is now $s \to a$, and $b$ is already in the set |
| 9 | L5 | take $r$: not a root, so skip it |

The result is $pts(a) = pts(q) = pts(r) = \{x, b\}$, $pts(p) = \{a\}$, $pts(s) = \{b\}$, and empty sets for $x$ and $b$. This is the result of Andersen's analysis. There were two merges. The set of $p$ is $\{a\}$ and not $\{a, q, r\}$: the three variables share one set as pointers, but they are still three locations.

## Correctness

The full proof is in the proof file. Its steps:

1. **Every step is forced.** Every edge $u \to v$ that the solver adds has $L(u) \subseteq L(v)$, and every set stays inside $L$. A merged set $C$ lies on the cycle $u \to v \to^* x \to^* u$, and $L$ cannot shrink along an edge, so $L$ is the same at every node of $C$, and the union of their sets is still inside it.
2. **The graph stays acyclic.** If the graph has no cycle before an edge $u \to v$ is added, every new cycle goes through the path from $v$ to $u$, and all its nodes are merged. A cycle through the merged node would need a node outside $C$ on a path from $v$ to $u$, which cannot be.
3. **What is done stays done.** A root that is not on the worklist has the edges for the loads and stores of all its elements, and its set is inside the set of each successor. A merge or a growing set puts the root back on the worklist.
4. **At the end, the sets are $L$.** With the worklist empty, the sets meet every constraint, so they contain $L$, and with step 1 they equal $L$.

The proof uses only the fact that the merged nodes lie on a cycle. So a partial search, which can miss some cycles, gives the same result.

## Complexity

**Proved.** With a full search for each new edge, the time is $O(n^4 + n^2 m)$ and the space is $O(n^2 + m)$, with each find counted as one step. There are at most $n^2$ edges, and each new one starts a search of $O(n^2)$ time. Each root goes back on the worklist $O(n)$ times, and each visit makes $O(n)$ calls of ADD-EDGE per load or store of its class and copies its set along $O(n)$ edges. The bound is worse than the $O(n^3)$ bound of Andersen's analysis with difference propagation, because this version moves full sets and searches the whole graph. Cycle elimination does not lower the worst case; its gain is on the graphs of real programs.

**Stated in the paper, not proved here.** Fähndrich, Foster, Su and Aiken keep the constraint graph in an *inductive form*: the variables have a fixed order, and each edge is stored at only one of its ends. Their search follows only chains of edges in that order, so it costs little, and it finds only some of the cycles. They report that this partial search finds most of the variables that are on cycles, and that it makes their solver much faster on C programs, by large factors on the larger ones. Hardekopf and Lin (2007) report that full online searches cost too much on large programs, which led them to lazy and hybrid detection.

**Measured, not proved.** On the 400 seeded random programs of the test file, of up to 12 variables and 30 statements, the result equals Andersen's least solution in every case, and 817 of the 2519 variables are merged into another. On 200 random programs of 40 variables and 120 statements, 6262 of 7980 variables are merged.

## Properties

- **Same result as Andersen's analysis.** The merges change the work, not the answer.
- **Online.** The search happens while the solver runs, so it also finds the cycles that the edges from loads and stores close, which no analysis before the solver can see.
- **Acyclic graph.** With a full search, the graph of classes never has a cycle.
- **Not every equal pair.** Two variables with equal sets but no cycle between them stay apart. [Offline variable substitution](/offline-variable-substitution/) finds some of those before solving.
- **Nodes, not locations.** Merging joins the sets of pointers. The addresses in the sets stay the original locations.

## Variants and improvements

- **Partial search.** The original method of Fähndrich, Foster, Su and Aiken searches only a chain of edges in a fixed order of the variables. It misses some cycles and costs much less per edge.
- **Lazy and hybrid detection.** [Lazy cycle detection](/hybrid-cycle-detection/) searches only when an edge carries a set that is already equal to the set at its target, which is a hint of a cycle. Hybrid cycle detection plans some merges with an offline pass over the statements and does them while the solver runs, with no search.
- **Dynamic topological order.** Pearce, Kelly and Hankin keep a topological order of the graph and update it when an edge is added; an edge that goes against the order shows a possible cycle.
- **Offline merges.** [Offline variable substitution](/offline-variable-substitution/) merges variables before the solver starts, with the [strongly connected components](/strongly-connected-components/) of the copy graph and more.
- **Unification.** [Steensgaard's analysis](/steensgaard-analysis/) merges every pair of nodes joined by an edge, not only nodes on a cycle, and loses precision.

## When to use it

Use cycle elimination in any inclusion-based points-to solver for large programs. Real C programs give constraint graphs with large cycles, many of them closed only by the edges from loads and stores, and without merges the solver moves the same facts around them many times. For the fastest solvers, use the cheaper lazy or hybrid detection, or the partial search, instead of a full search for every edge.

## Pitfalls

- **Merging the locations too.** Only the sets are shared. If the merge renames the addresses in the sets, the pointers to a merged variable seem to point to all of its class, and the result is wrong.
- **Merging only the two ends.** All the nodes on every path from $v$ back to $u$ must be merged; merging only $u$ and $v$ leaves a cycle in the graph.
- **Forgetting the tables.** The loads and stores of a merged node move to the root, and the root goes back on the worklist; without this, the new elements of the merged set never add their edges.
- **Stale names.** After merges, an edge can name a variable that is no longer a root. Every use of a node must go through FIND.
- **A full search for every edge.** It is correct, but it can cost more than it saves. Bound the search, or search only when there is a hint of a cycle.

## Implementations

## History

The cubic cost of Andersen's analysis (1994) was the main obstacle to its use on large programs, and the constraint graphs of real programs have many cycles. Fähndrich, Foster, Su and Aiken (1998) showed that a partial online search for cycles in an inductive form of the graph removes most of the repeated work. Rountev and Chandra (2000) found many equal variables before solving. Heintze and Tardieu (2001) and Pearce, Kelly and Hankin (2003) gave other ways to detect cycles while solving. Hardekopf and Lin (2007) compared these methods and gave lazy and hybrid cycle detection, which analyse millions of lines of C.

## References
