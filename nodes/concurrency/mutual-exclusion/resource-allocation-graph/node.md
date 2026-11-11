---
tag: SGGS8W
kind: data-structure
slug: resource-allocation-graph
name: Resource allocation graph
aliases:
- RAG
- general resource graph
- Holt graph
area: concurrency/mutual-exclusion
level: core
summary: A bipartite directed graph of processes and resource types, with request edges and assignment edges counted in units. It shows who holds and who waits for what.
history:
  year: 1972
  people: [Richard C. Holt]
  note: Holt defined general resource graphs, graph reduction, and the cycle and knot conditions for deadlock in his 1972 survey.
prereqs: [deadlock, bipartite-graph]
see_also: [wait-for-graph, deadlock-detection, coffman-conditions, banker-algorithm, cycle-detection, directed-graph, deadlock-prevention]
sources:
  - paper: doi:10.1145/356603.356607
    title: Richard C. Holt, Some deadlock properties of computer systems, ACM Computing Surveys 4(3), 1972, pages 179 to 196
    locator: the general resource graph, request and assignment edges, graph reduction, and the cycle and knot theorems
  - paper: doi:10.1145/356586.356588
    title: E. G. Coffman, M. J. Elphick and A. Shoshani, System deadlocks, ACM Computing Surveys 3(2), 1971, pages 67 to 78
    locator: the four conditions and the graph form of circular wait
  - book: isbn:9781119320913
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, tenth edition (2018)
    locator: Chapter 8, Deadlocks, the sections on the resource-allocation graph and on the resource-allocation-graph algorithm with claim edges
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition (2015)
    locator: Chapter 6, Deadlocks, the resource graphs and deadlock detection with one resource of each type
---

A resource allocation graph is a [bipartite](/bipartite-graph/) [directed graph](/directed-graph/) with one vertex for each process and one vertex for each resource type. An edge from a process to a resource is a *request* edge, and an edge from a resource to a process is an *assignment* edge; a type with several units can have several edges. Holt (1972) used it to state exactly when a state is a [deadlock](/deadlock/): when every type has one unit, a cycle is a deadlock, and in general a deadlock is a part of the graph that no *reduction* can remove.

## In plain words

Draw a circle for each program and a box for each kind of resource, for example printers or locks. Put a dot in a box for each copy of the resource. When a program holds a copy, draw an arrow from the box to the program. When a program waits for a copy, draw an arrow from the program to the box.

Now you can see the waiting. If each box has one dot, a loop of arrows means that each program in the loop waits for the next one, and none can move. If a box has several dots, a loop is not enough: a program outside the loop may give a copy back. To check, find a program that can get everything it asks for, pretend it finishes, give back its copies, and repeat. The programs that remain are stuck for good.

## The abstract type

The structure stores the allocation state of a system of reusable resources:

- $n$ processes $p, q, \ldots$, numbered $0$ to $n - 1$, and $m$ resource types, numbered $0$ to $m - 1$; type $r$ has $t(r) \ge 1$ units;
- $\mathit{held}[p][r]$, the units of $r$ that $p$ holds, and $\mathit{req}[p][r]$, the units of $r$ that $p$ has asked for and not yet got;
- for avoidance only, a set $\mathit{claim}[p]$ of the types that $p$ may ask for later.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes |
| $p, q$ | process names; $i, j$ are indices |
| $m$ | the number of resource types (the shared objects) |
| $t(r)$ | the number of units of type $r$ |
| $\mathit{avail}[r]$ | the free units of type $r$ |

The model is the usual one of deadlock theory. Processes are asynchronous. A process that asks for units it cannot get is *blocked*: it takes no step until the request is granted, so it releases nothing while it waits. A resource is reusable: a unit is never used up, and the holder gives it back when it releases it. Requests are AND requests: a process needs all the units it asked for. The graph does not model consumable resources such as messages. For those Holt uses a different rule, and the [wait-for graph](/wait-for-graph/) page covers the communication model.

The queries are: is a process blocked, which processes does it wait for, which processes are deadlocked, and (with claims) is it safe to grant a request.

## Representation

The graph is stored as two $n \times m$ matrices of edge counts, $\mathit{held}$ and $\mathit{req}$, a vector $\mathit{avail}$ of free units, and the claim sets. The request edges of $p$ are the entries $\mathit{req}[p][r] > 0$, each with multiplicity $\mathit{req}[p][r]$, and the assignment edges into $p$ are the entries $\mathit{held}[p][r] > 0$. A figure draws the units as dots inside the resource vertex and starts each assignment edge at a dot.

**Invariant.** For every type $r$:

$$\mathit{avail}[r] = t(r) - \sum_{p} \mathit{held}[p][r] \ge 0 \qquad\text{and}\qquad \mathit{held}[p][r] + \mathit{req}[p][r] \le t(r) \text{ for every } p.$$

The second part says that no process asks for more than the system has. Without it a process could be blocked forever with no other process involved.

The graph is bipartite by construction: each edge joins a process and a resource. A cycle therefore alternates between processes and resources, and it has even length.

## Operations

```pseudo id=main
NEW(n, t)
L1  avail ← t; held ← 0; req ← 0; claim[p] ← ∅ for each p

REQUEST(p, r, k)                ▷ requires held[p][r] + req[p][r] + k ≤ t(r)
L2  req[p][r] ← req[p][r] + k

GRANT(p)                        ▷ grant all pending requests of p, or none
L3  if req[p][r] > avail[r] for some r then
L6      return false            ▷ p stays blocked
L4  for each r: avail[r] ← avail[r] − req[p][r]; held[p][r] ← held[p][r] + req[p][r]; req[p][r] ← 0
L5  return true

RELEASE(p, r, k)                ▷ requires k ≤ held[p][r]
L7  held[p][r] ← held[p][r] − k; avail[r] ← avail[r] + k

WAITS-FOR(p)
L8  return the q ≠ p with held[q][r] > 0 for some r with req[p][r] > 0

REDUCE()                        ▷ returns the processes that no reduction removes
L9  work ← avail; left ← all processes
L10 while some p in left has req[p][r] ≤ work[r] for every r do
L11     work[r] ← work[r] + held[p][r] for every r; remove p from left
L12 return left

ADD-CLAIM(p, r)                 ▷ avoidance, one unit per type
L13 claim[p] ← claim[p] ∪ {r}

SAFE-GRANT(p, r)                ▷ requires t(r) = 1 for all r, r ∈ claim[p], r free, p asked for r
L14 move the request edge p → r to an assignment edge r → p
L15 if the graph of request, assignment and claim edges has a cycle then undo L14 and return false
L16 return true
```

**Request and grant** (lines L2 to L6). A request adds edges. GRANT turns all the request edges of $p$ into assignment edges at once, or leaves them all. A system that grants each request as soon as it fits is called *expedient* by Holt.

**Release** (line L7) removes assignment edges and frees the units.

**Waits-for** (line L8) projects the graph on the processes: $p$ waits for $q$ when $p$ requests a type of which $q$ holds a unit. When each type has one unit, this is exactly the [wait-for graph](/wait-for-graph/), and $p$ waits for the single holder of $r$. With several units, $p$ needs only one of the holders to release, so the projection loses information.

**Reduce** (lines L9 to L12) is Holt's graph reduction. A process whose requests all fit in the free units can, in the best case, get them, run to the end, and give back all it holds. The loop removes such processes one at a time and adds their units to the pool. The processes that remain are exactly the deadlocked ones, and the order of removal does not matter. The page on [deadlock detection](/deadlock-detection/) proves both facts and gives a faster version.

**Claim edges** (lines L13 to L16). For avoidance with one unit per type, each process declares in advance the types it may use, as dashed claim edges $p \to r$. A request turns a claim edge into a request edge, and a grant turns it into an assignment edge. SAFE-GRANT refuses a grant that would close a cycle when the claim edges count as edges. The proof file shows that "no cycle with claim edges" is exactly the condition that the processes can finish one after the other. With several units per type, the cycle test is too weak, and the [banker's algorithm](/banker-algorithm/) does the job.

## Example

Take three processes $p, q, s$ and two types: $A$ with one unit and $B$ with two units.

| step | operation | result | avail $(A, B)$ | state |
|---|---|---|---|---|
| 1 | REQUEST$(p, A, 1)$, GRANT$(p)$ | true | $(0, 2)$ | $p$ holds $A$ |
| 2 | REQUEST$(q, B, 1)$, GRANT$(q)$ | true | $(0, 1)$ | $q$ holds one $B$ |
| 3 | REQUEST$(s, B, 1)$, GRANT$(s)$ | true | $(0, 0)$ | $s$ holds one $B$ |
| 4 | REQUEST$(q, A, 1)$, GRANT$(q)$ | false | $(0, 0)$ | $q$ waits for $A$ |
| 5 | REQUEST$(p, B, 1)$, GRANT$(p)$ | false | $(0, 0)$ | $p$ waits for a $B$ |

The projection is $p \to \{q, s\}$, $q \to \{p\}$, and $s$ waits for nothing. So the graph has the cycle $p \to B \to q \to A \to p$. It is not a deadlock. REDUCE starts with $\mathit{work} = (0, 0)$ and removes $s$, which requests nothing, so $\mathit{work} = (0, 1)$. Now $p$ fits and is removed, giving $\mathit{work} = (1, 1)$, and then $q$ fits. REDUCE returns the empty set: if $s$ finishes, $p$ gets its unit of $B$, and $q$ gets $A$ after $p$.

If $s$ also asks for $A$ before it releases its unit, no process is removable, since $\mathit{work} = (0, 0)$ and each process requests a unit. REDUCE returns $\{p, q, s\}$, and all three are deadlocked.

**Claim edges.** Let $p$ and $q$ each claim both single unit types $A$ and $B$. $p$ asks for $A$, and SAFE-GRANT gives it, since the edges $q \to A \to p \to B$ and $q \to B$ form no cycle. Then $q$ asks for $B$. Giving $B$ to $q$ would close $p \to B \to q \to A \to p$, so SAFE-GRANT refuses, and $q$ waits although $B$ is free. Had the grant gone through, the next requests ($p$ for $B$, $q$ for $A$) would deadlock.

## Correctness

The structure keeps its invariant: GRANT moves units from $\mathit{avail}$ to $\mathit{held}$ only after line L3 checked that they fit, and RELEASE moves them back. The two theorems that make the graph useful are proved in [the proof file](proofs/correctness.md): every deadlock contains a cycle, for any number of units, and when each type has one unit, every cycle is a deadlock. So with single units, deadlock detection is [cycle detection](/cycle-detection/) on the wait-for graph. The proof file also shows that the claim edge test of SAFE-GRANT accepts a grant exactly when the new state is safe.

A cycle is necessary but not sufficient when a type has several units, as the example shows. Holt (1972) also gives a sufficient condition for that case: in an expedient state, a *knot* (a set $K$ of vertices from which exactly the vertices of $K$ are reachable) implies a deadlock. The reduction is the exact test in every case.

## Complexity

The space is $\Theta(nm)$ for the two matrices, plus the claim sets. Times are in the word RAM model.

| operation | time | notes |
|---|---|---|
| NEW | $\Theta(nm)$ | |
| REQUEST, RELEASE, ADD-CLAIM | $O(1)$ | |
| GRANT | $O(m)$ | |
| WAITS-FOR$(p)$ | $O(nm)$ | scan the column of each requested type |
| the whole wait-for graph | $O(n^2 m)$ | |
| REDUCE | $O(m n^2)$ | at most $n$ rounds, each scans $n$ rows of $m$ entries |
| SAFE-GRANT | $O(nm)$ | a depth-first search over $n + m$ vertices and at most $2nm$ edges |

A sparse representation, with lists of the nonzero entries, makes WAITS-FOR and the cycle test linear in the number of edges instead of $nm$.

## Variants

- **Single unit graphs.** When every type has one unit, the resource vertices carry no information beyond "held by whom", and the [wait-for graph](/wait-for-graph/) on processes replaces the graph. This is the form used by database lock managers.
- **Consumable resources.** Holt also treats resources such as messages and signals, which a producer creates and a consumer destroys. The reduction rule changes, because the number of units of such a type is not fixed.
- **Claim graphs.** Adding the claim edges gives the avoidance test above. With several units per type, the claims become a maximum need matrix, and the test becomes the safety check of the [banker's algorithm](/banker-algorithm/).
- **The general resource graph.** Holt's general form allows both reusable and consumable resource types in one graph.

## When to use it

Use the graph to reason about a deadlock, to explain it, and to build a detector. For a detector over locks, where each lock is one unit, keep only the wait-for graph. For pools of identical units, such as buffers or tape drives, keep the counts and use reduction, because the cycle test gives false alarms. Use claim edges only when each process can declare its needs in advance, which is rare outside batch systems.

## Pitfalls

- With several units of a type, a cycle is not a deadlock. A detector that reports every cycle aborts processes for nothing.
- A request edge must stay in the graph only while the process is blocked. A process that gave up a request (after a timeout, for example) must remove its edge, or the detector sees a phantom deadlock.
- The theory assumes that a blocked process releases nothing. A system that lets a waiting thread release a lock on a timeout, or that preempts resources, is outside the model, and a cycle can then dissolve by itself.
- The graph says nothing about future requests. A state with no deadlock can still be unsafe: every way forward may lead to a deadlock. Avoidance needs the claims.

## Implementations

## History

Coffman, Elphick and Shoshani (1971) stated circular wait in terms of a graph of processes and resources. Holt (1972) gave the general resource graph with units, the reduction, and the theorems on cycles and knots, for both reusable and consumable resources. The claim edge test for single unit avoidance appears in operating systems textbooks, for example Silberschatz, Galvin and Gagne, Chapter 8.

## References
