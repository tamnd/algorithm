---
tag: MGQX2W
kind: algorithm
slug: demand-driven-points-to
name: Demand-driven points-to analysis
aliases:
- refinement-based points-to analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: research
summary: Answers points-to queries for chosen variables only, by searching backward in the constraint graph, often as CFL reachability.
solves: [points-to-analysis]
model: word-ram
complexity:
  vars: {m: the number of variables and queries, s: the number of statements}
  time: {worst: O(m^3 + m s)}
  space: {extra: O(m^2 + s)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 2001
  people: [Nevin Heintze, Olivier Tardieu]
  note: Heintze and Tardieu answered Andersen-style queries for large C programs by computing only the constraints that each query needs.
prereqs: [andersen-analysis, magic-sets]
see_also: [points-to-analysis, cfl-reachability, alias-analysis, datalog-program-analysis, sparse-flow-sensitive-pointer-analysis, object-sensitivity, call-graph-construction]
sources:
  - paper: doi:10.1145/378795.378802
    title: Nevin Heintze and Olivier Tardieu, Demand-driven pointer analysis, Proceedings of PLDI 2001
    locator: the demand-driven form of Andersen's analysis for C, with points-to and pointed-by queries and caching between queries
  - paper: doi:10.1145/1133981.1134027
    title: Manu Sridharan and Rastislav Bodík, Refinement-based context-sensitive points-to analysis for Java, Proceedings of PLDI 2006
    locator: points-to queries as CFL reachability with balanced fields and calls, refined on demand within a budget
---

A demand-driven points-to analysis answers a question such as "what may $p$ point to?" for a few chosen variables, without solving the whole program. It gives the same answer as the exhaustive [Andersen analysis](/andersen-analysis/) for each queried variable, but it only builds the part of the constraint graph that the query depends on. The algorithm on this page starts from the queried variables and works backward: a variable is *demanded* when the set of a demanded variable depends on its set, and only demanded variables get sets, edges and work. In the language of Datalog it is the [magic-sets](/magic-sets/) form of Andersen's rules. Heintze and Tardieu (2001) made the approach fast in practice for C, and Sridharan and Bodík (2006) recast it as [CFL reachability](/cfl-reachability/) for Java, with contexts and fields refined on demand.

## In plain words

A full pointer analysis works out where every pointer may point, even when a tool only needs to know about one of them. A demand-driven analysis starts from the one pointer it is asked about. To know what it points to, it must know the pointers it was copied from, and the pointers it was loaded through. So it asks about those next, and so on. Pointers that the answer does not depend on are never looked at. For a debugger, an editor or a check on one line of code, this is often a small part of the program. The answer is exactly the one the full analysis would give for that pointer.

## The problem

The input is a list of statements of the four forms of the [Andersen page](/andersen-analysis/): $v = \&a$, $v = y$, $v = {*}y$ and ${*}p = q$, and a set $Q$ of query variables. The output is $A(q)$ for each $q \in Q$, where $A$ is the least solution of Andersen's inclusion constraints. A variable is *taken* if some statement takes its address.

| item | value |
|---|---|
| direction | none: flow-insensitive, one answer for the whole program |
| may or must | may |
| domain | maps from the demanded variables to sets of variables, a set of demanded variables and a set of edges |
| order | inclusion in all parts (bottom is precise) |
| join | union |
| bottom and top | everything empty, and every variable demanded with the set of all variables |
| boundary value | the queries are demanded |
| initial value | only the queries are demanded, with empty sets |
| transfer | Andersen's four rules, each applied only for a demanded left side |

## The algorithm

```pseudo id=main
DEMAND-POINTS-TO(S, Q)
L1  for each q in Q do DEMAND(q)
L2  while some variable waits to start or the worklist is not empty do
L3      if a variable v waits to start then START(v)
L4      else take n from the worklist, with its new part d
L5          for each a in d and each load x = *n with x demanded do EDGE(a, x)
L6          for each a in d that is demanded and each store *n = q do EDGE(q, a)
L7          for each edge n -> w do ADD(d, w)
L8  return pts(q) for each q in Q

START(v)
L9  ADD({a : v = &a is in S}, v)
L10 for each v = y in S do EDGE(y, v)
L11 for each v = *y in S do DEMAND(y); for each b in pts(y) do EDGE(b, v)
L12 if v is taken then for each *p = q in S do DEMAND(p); if v is in pts(p) then EDGE(q, v)

EDGE(u, v)
L13 DEMAND(u); if u -> v is new then add it and ADD(pts(u), v)

DEMAND(v)
L14 if v is not demanded then demand it with an empty set and let it wait to start

ADD(s, v)
L15 if s has elements not in pts(v) then add them to pts(v) and to its new part, and put v on the worklist
```

The four rules of Andersen's analysis are read backward. Line L10 says that the set of $v$ needs the set of $y$ for a copy. Line L11 says that a load $v = {*}y$ needs the set of $y$, and then the set of every $b$ that $y$ may point to. Line L12 is the hard case: a store ${*}p = q$ writes to $v$ when $p$ may point to $v$, so for a taken $v$ the run must know the sets of all store pointers $p$. Lines L5 and L6 handle the same two cases when a set grows after the variable has started. The edges and the worklist with new parts are those of Andersen's solver, with difference propagation.

## Example

```
p = &a
q = &b
r = &p
s = q
*r = s
t = *r
u = &c
v = u
w = *v
```

The query is $t$. Line L11 demands $r$ for the load $t = {*}r$. Then $pts(r) = \{p\}$, so $p$ is demanded with the edge $p \to t$. The variable $p$ is taken, so line L12 demands the store pointer $r$ (already demanded) and, since $p \in pts(r)$, adds the edge $s \to p$ for the store ${*}r = s$. Then $s$ demands $q$ through the copy $s = q$.

| variable | demanded because | set |
|---|---|---|
| $t$ | it is the query | $\{a, b\}$ |
| $r$ | $t = {*}r$ | $\{p\}$ |
| $p$ | $r$ points to $p$ | $\{a, b\}$ |
| $s$ | ${*}r = s$ with $p \in pts(r)$ | $\{b\}$ |
| $q$ | $s = q$ | $\{b\}$ |

The run never looks at $a$, $b$, $u$, $v$, $w$ or $c$, and $pts(t) = \{a, b\}$ is the Andersen answer. A query for $q$ demands only $q$. A query for $w$ demands $w$, $v$, $u$ and $c$, and, since $c$ is taken, the store pointer $r$. It finds $c \notin pts(r)$ and stops with $pts(w) = \emptyset$.

## Correctness

**Soundness.** Every edge $u \to v$ is created only when Andersen's least solution $A$ has $A(u) \subseteq A(v)$: for a copy, for a load through a pointer that may point to $u$, or for a store through a pointer that may point to $v$. So by induction every set stays inside $A$.

**Completeness for demanded variables.** When the run stops, the demanded part is closed. Every demanded variable has its own facts from line L9, an edge from each copy source, the edges of each load, and, if it is taken, the edges of every store whose pointer may point to it, with the store pointers demanded. Edges carry every element, by the worklist argument of Andersen's solver. Now take a fact $(v, a)$ of $A$ with $v$ demanded and do induction on the height of its derivation by Andersen's rules. Each rule has premises about variables that the closure forces to be demanded, so by induction they hold, and the edge carries $a$ into $pts(v)$. So $pts(v) = A(v)$ for every demanded $v$, and in particular for every query. The full proofs are in the proof file.

## Complexity

**Proved.** With $m$ variables and queries and $s$ statements, the run takes $O(m^3 + m s)$ time and $O(m^2 + s)$ space, the same worst case as Andersen's solver. Only demanded variables get starts, edges and propagation, so the actual work is that of Andersen's solver on the demanded part, plus a scan of all stores for each demanded taken variable.

**Stated in the literature.** Heintze and Tardieu report that demand-driven queries on large C programs are answered much faster than the exhaustive analysis, with caching of the results of earlier queries. Sridharan and Bodík report that refinement-based queries for Java answer most client questions within a small budget.

**Measured, not proved.** On 400 random programs (seed 2001), each answer equals the exhaustive Andersen set, also computed by plain iteration. On 200 programs (seed 2006), answering all variables at once gives the full Andersen solution, and the union of the demanded sets of single queries equals the demanded set of all of them. On 200 random programs with 60 statements over 60 variables (seed 2005), one query demanded 23% of the variables on average, and 98 of the 200 queries demanded at most 5 variables. On 300 programs (seed 1990), every fact of a concrete run is in the answer.

## Properties

- **Exact with respect to the exhaustive analysis.** It is not an approximation of Andersen's analysis: each answer is the same set.
- **Monotone in the queries.** More queries demand more variables, never fewer, and the answers do not change.
- **Stores are the expensive part.** A taken variable needs the sets of all store pointers, because any of them may point to it. In C code with many stores through pointers, the demanded part can grow to most of the program.
- **Reusable.** The demanded sets are final, so a later query can reuse them.

## Variants and improvements

- **Pointed-by queries.** Heintze and Tardieu avoid demanding every store pointer: for a taken $v$ they ask a second kind of query, "which pointers may point to $v$?", and only follow the stores whose pointers are in its answer. They also cache answers between queries.
- **CFL reachability.** For Java, where pointers come from fields and not from address-of, a points-to query is a search for paths in a graph of assignments whose field stores and loads match, like balanced parentheses. Sridharan and Bodík add matching calls and returns for context sensitivity, and a refinement loop that starts with cheap, imprecise matching and refines only the parts that affect the client's question, within a budget.
- **Magic sets.** Writing Andersen's rules in [Datalog](/datalog-program-analysis/) and applying the [magic-sets](/magic-sets/) rewriting to the query gives this algorithm automatically.
- **Incremental and demand-driven alias queries.** The same backward search answers alias questions for two pointers, and can stop as soon as a common target is found.

## When to use it

Use it when a client needs points-to facts for a small part of a large program: an IDE that shows the targets of a call, a bug checker that asks about a few dereferences, or a just-in-time compiler with a time limit. When the client needs facts for most variables, for example a whole-program optimizer, the exhaustive [Andersen analysis](/andersen-analysis/) with cycle elimination is faster, because it shares work between all variables.

## Pitfalls

- **Forgetting stores into a taken variable.** A version of START without line L12 only follows copies and loads. It misses every value written through a pointer, so in the example it returns $pts(t) = \{a\}$ instead of $\{a, b\}$. Line L12 must demand every store pointer for a taken variable and add the store edge when that pointer may point to it.
- **Handling only the sets present at the start.** A version of START that adds the load and store edges only for the elements present when the variable starts is incomplete. Lines L5 and L6 must also add the edges for elements that arrive later.
- **Answering before the worklist is empty.** A query answer is final only when no variable waits to start and the worklist is empty, as in line L2. Partial answers are under-approximations.
- **Calling it sound with reflection or native code.** Like the exhaustive analysis, it only covers the statements it sees. Code that is loaded, generated or called through native interfaces needs a model.

## Implementations

## History

Andersen's inclusion-based analysis dates from 1994, and exhaustive solvers for it were made fast in the following years. Heintze and Tardieu (2001) showed that a demand-driven version could answer queries on very large C programs quickly. Sridharan, Gopan, Shan and Bodík (2005) formulated demand-driven points-to analysis for Java as CFL reachability, and Sridharan and Bodík (2006) added refinement and context sensitivity. The link to Datalog and magic sets made the idea a standard part of declarative program analysis.

## References
