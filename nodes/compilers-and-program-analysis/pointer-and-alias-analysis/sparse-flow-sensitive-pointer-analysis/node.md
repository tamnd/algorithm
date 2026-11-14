---
tag: 9J9RX5
kind: algorithm
slug: sparse-flow-sensitive-pointer-analysis
name: Sparse flow-sensitive pointer analysis
aliases:
- staged flow-sensitive pointer analysis
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: research
summary: Makes flow-sensitive points-to analysis scale by propagating facts only along def-use chains found by a cheaper pre-analysis.
solves: [points-to-analysis]
model: word-ram
complexity:
  vars: {n: the number of nodes and edges of the control flow graph, m: the number of names}
  time: {worst: O(n^3 m^4)}
  space: {extra: O(n^2 m + n m^2)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: true, context_sensitive: false}
history:
  year: 2011
  people: [Ben Hardekopf, Calvin Lin]
  note: Hardekopf and Lin used Andersen's analysis to find def-use chains for memory and then ran the flow-sensitive analysis only along them.
prereqs: [andersen-analysis, def-use-chains, flow-sensitivity]
see_also: [static-single-assignment-form, reaching-definitions, points-to-analysis, steensgaard-analysis, demand-driven-points-to, field-sensitivity, alias-analysis]
sources:
  - paper: doi:10.1109/CGO.2011.5764696
    title: Ben Hardekopf and Calvin Lin, Flow-sensitive pointer analysis for millions of lines of code, Proceedings of CGO 2011
    locator: the staged analysis with an auxiliary flow-insensitive analysis, def-use chains for address-taken variables and strong updates on singleton targets
---

A sparse flow-sensitive pointer analysis computes a points-to set for each variable at each program point, like the dense [flow-sensitive](/flow-sensitivity/) analysis, but it moves a set only from the node that defines it to the nodes that use it. For top-level variables these [def-use chains](/def-use-chains/) are easy to find. For memory reached through pointers they depend on the result being computed. The staged analysis of Hardekopf and Lin (2011) breaks this cycle with a cheap first stage: [Andersen's analysis](/andersen-analysis/) gives a sound over-approximation of what each store may write and each load may read, and that gives def-use chains that are safe to use. The second stage then runs the flow-sensitive transfer functions, with strong updates, along those chains only. The result is exactly the dense result at every place where a variable is used.

## In plain words

A flow-sensitive analysis knows that a pointer pointed to one thing before a line and to another thing after it. The plain way to do this keeps a full table of every pointer at every line and copies the table from line to line. Most entries never change on the way, so most of that copying is wasted. The sparse way sends each new fact straight from the line that makes it to the lines that read it. The hard part is knowing which lines read a fact written through a pointer. A fast first pass that ignores the order of statements answers that safely, because it can only say "maybe" too often, never too rarely. The second pass then follows those links and gets the same answers as the full table.

## The problem

The input is a control flow graph whose nodes hold statements of four forms: $x = \&a$, $x = y$, $x = {*}y$ and ${*}x = y$, with node $0$ as the entry. A name of the form $h_1, h_2, \ldots$ is a heap location that stands for every object made at one allocation site. The output is, for each reachable node $u$ and each name $w$ that $u$ may read, the set $IN_u(w)$ of names that $w$ may point to just before $u$, and the set $OUT_d(v)$ just after each node $d$ for each name $v$ that $d$ may define. Here $A$ is Andersen's result, and $DEF(n)$ and $USE(n)$ are the names that $n$ may define and read according to $A$.

| item | value |
|---|---|
| direction | forward |
| may or must | may |
| domain | maps from pairs (node, name) on def-use edges to subsets of the names, each inside the Andersen set of the name |
| order | pointwise inclusion (bottom is precise) |
| join | union over the def-use edges into a node |
| bottom and top | every set empty, and every name mapped to its Andersen set |
| boundary value | at the entry no name points to anything |
| initial value | every $out(d, v)$ is empty |
| transfer | $x = \&a$ gives $\{a\}$, a copy and a load give the usual sets, and a store gives a strong update to a single target that is not a heap name and a weak update otherwise |

## The algorithm

```pseudo id=main
SPARSE-FS(S, G)
L1  A = ANDERSEN(S)
L2  for each node n reachable from the entry, compute DEF(n) and USE(n) with A
L3  for each reachable node d and each v in DEF(d) do
L4      add an edge d -v-> u for each node u with v in USE(u) that some path reaches from d with no node strictly between them that may define v
L5  set every out(d, v) to the empty set and put every reachable node on the worklist W
L6  while W is not empty do
L7      take a node n from W
L8      for each w in USE(n), in(w) = the union of out(d, w) over the edges d -w-> n
L9      for each v in DEF(n), new = TRANSFER(n, v, in)
L10         if new differs from out(n, v) then out(n, v) = new and put every u with an edge n -v-> u on W
L11 return out, and in(w) at each node for each w in USE of the node

TRANSFER(n, v, in)
L12 x = &a gives {a}; x = y gives in(y); x = *y gives the union of in(b) for b in in(y)
    for a store *x = y:
L13 if in(x) is empty then return the empty set
L14 if in(x) = {v} and v is not a heap name then return in(y)
L15 if v is in in(x) then return in(v) ∪ in(y) else return in(v)
```

For a node $n$, $DEF(n)$ is $\{x\}$ for the first three forms and $A(x)$ for a store ${*}x = y$. $USE(n)$ is empty for $x = \&a$, $\{y\}$ for a copy, $\{y\} \cup A(y)$ for a load and $\{x, y\} \cup A(x)$ for a store. The search of line L4 is a depth-first search from the successors of $d$ that records each node using $v$ and stops at each node that may define $v$. A store defines every name that its pointer may point to by Andersen's result, so a weak update at a store passes the old value on through line L15.

Line L14 is the strong update. When the pointer points to exactly one name, and that name is one concrete location, the store overwrites it, so the old value is dropped. Line L13 handles a store whose pointer points to nothing yet. Such a store cannot run, so its output is empty. This keeps TRANSFER monotone: if line L13 kept the old value, a later strong update could make the output smaller, and the result would depend on the order of the worklist.

## Example

```
0: p = &a
1: x = &p
2: t = *x
3: q = &b
4: *x = q
5: r = *x
6: s = p
```

The nodes form one straight path. Andersen's analysis gives $A(x) = \{p\}$, $A(p) = A(t) = A(r) = A(s) = \{a, b\}$ and $A(q) = \{b\}$. So the store at node 4 may define only $p$, and the loads at nodes 2 and 5 may read $x$ and $p$.

| def-use edge | why |
|---|---|
| $0 \xrightarrow{p} 2$, $0 \xrightarrow{p} 4$ | node 4 may define $p$, so the search stops there |
| $1 \xrightarrow{x} 2$, $1 \xrightarrow{x} 4$, $1 \xrightarrow{x} 5$ | no other node defines $x$ |
| $3 \xrightarrow{q} 4$ | the store reads $q$ |
| $4 \xrightarrow{p} 5$, $4 \xrightarrow{p} 6$ | the store gives the new value of $p$ |

The worklist gives $out(0, p) = \{a\}$ and $out(1, x) = \{p\}$, so node 2 gets $t = \{a\}$. At node 4, $in(x) = \{p\}$ is one name and not a heap name, so line L14 gives $out(4, p) = in(q) = \{b\}$. Node 5 reads $p$ through the edge from node 4 and gets $r = \{b\}$, and node 6 gets $s = \{b\}$. Andersen's analysis alone gives $\{a, b\}$ for $t$, $r$ and $s$. If $x$ pointed to a heap name $h_1$ instead, line L15 would keep the old value, and a later load would see both the old and the new value.

## Correctness

The proof file shows four facts. First, TRANSFER keeps every set inside the Andersen set of its name and is monotone, because a store with an empty pointer set gives the empty set. Second, a node changes only names in its DEF set and reads only names in its USE set, both computed from the sound Andersen result. Third, the least solution of the sparse equations is equal to the dense flow-sensitive least solution on every def-use pair. One direction restricts the dense solution to the def-use pairs and shows that it satisfies the sparse equations. The other direction extends the sparse solution to every node by the reaching definitions and shows that it satisfies the dense equations. Fourth, every concrete run is covered: a strong update is applied only when the pointer can hold one location, and a heap name, which stands for many objects, gets only weak updates.

## Complexity

**Proved.** Let $n$ be the number of nodes and edges and $m$ the number of names. After Andersen's analysis, building the def-use edges takes $O(n^2 m)$ time, with at most $n^2 m$ edges. Each value $out(d, v)$ only grows inside $A(v)$, so it changes at most $m$ times, and the worklist makes at most $n + n^2 m^2$ visits of $O(n m^2)$ each. That gives $O(n^3 m^4)$ time and $O(n^2 m + n m^2)$ space. This bound is loose. The point of the method is that real programs have far fewer def-use edges than the worst case.

**Stated in the literature.** Hardekopf and Lin report that the staged analysis handles C programs of up to millions of lines of code, as the title of their paper says, and that it is much faster and uses much less memory than their earlier semi-sparse analysis.

**Measured, not proved.** On 400 random programs with up to 25 nodes and 8 names (seed 2011), the sparse result equals the dense result at every def-use pair. The sparse analysis stored 7936 points-to facts where the dense tables stored 33568, which is 24%. Of the 525 reachable stores, 81 got a strong update. On 300 programs (seed 2004), every dense set is inside the Andersen set, and some are strictly smaller. On 300 programs (seed 2003), every fact of a random concrete run is in the result.

## Properties

- **Exact with respect to the dense analysis.** The sparse result is not an approximation of the dense flow-sensitive result: at each use the sets are the same.
- **As precise as its strong updates allow.** It is more precise than Andersen's analysis only because of the order of statements and the strong updates of line L14.
- **The first stage limits the cost, not the result.** A less precise first stage gives larger DEF and USE sets and more def-use edges, so more work, but the answers stay the same as long as the first stage is sound.
- **Flow-sensitive, not context-sensitive.** Calls are handled through the call graph, with one set per variable and node for all contexts.

## Variants and improvements

- **Semi-sparse analysis.** Hardekopf and Lin's earlier analysis (2009) puts only the top-level variables, whose address is never taken, in [SSA form](/static-single-assignment-form/) and still propagates the address-taken variables densely.
- **Memory SSA.** The def-use edges of line L4 for address-taken variables are usually built by putting the program in SSA form for memory, with a may-definition at each store and a may-use at each load for the names that Andersen's result gives. This gives fewer edges than one edge from each definition to each use.
- **Access equivalence.** Names whose def-use chains are the same can share one set of edges, which saves memory on large programs.
- **A cheaper first stage.** [Steensgaard's analysis](/steensgaard-analysis/) can replace Andersen's analysis as the first stage. It is faster but gives more def-use edges.
- **Fields and contexts.** The same staging works with [field-sensitive](/field-sensitivity/) names and with a context-sensitive first stage.

## When to use it

Use it when a client needs flow-sensitive precision, for example strong updates for a bug checker or for proving that a pointer is not null at a point, on a program that is too large for the dense analysis. When flow-insensitive precision is enough, Andersen's analysis alone is cheaper. When only a few variables matter, a [demand-driven analysis](/demand-driven-points-to/) may be cheaper still.

## Pitfalls

- **Strong updates on heap names.** A version of line L14 without the test "v is not a heap name" overwrites a heap location that stands for many objects. For $q_0 = \&a$, $x = \&h_1$, ${*}x = q_0$, $q = \&b$, ${*}x = q$, $r = {*}x$ it gives $r = \{b\}$ instead of $\{a, b\}$, which misses a real value. The right line L14 updates strongly only a name for one concrete location.
- **Keeping the old value at a store that cannot run.** A version of line L13 that returns $in(v)$ when $in(x)$ is empty makes TRANSFER non-monotone, because a later strong update gives a smaller set. The result then depends on the order of the worklist. The right line L13 returns the empty set.
- **Stopping the search at a use.** A version of line L4 that stops at the first node that uses $v$ misses later uses on the same path. The right search records a node that uses $v$ and goes on past it, and stops only at a node that may define $v$.
- **An unsound first stage.** If the first stage misses a target of a store, the store does not appear in DEF for that name and the def-use edges skip it. The first stage must be sound for every statement of the program.
- **Calling it sound with reflection or native code.** Like every whole-program pointer analysis, it covers only the statements it sees. Code loaded, generated or called through native interfaces needs a model.

## Implementations

## History

Sparse evaluation of dataflow problems along def-use chains is older than pointer analysis on SSA form. For pointer analysis the difficulty was that the def-use chains of memory depend on the points-to result itself. Hardekopf and Lin (2009) first made the top-level variables sparse in a semi-sparse analysis. In 2011 they added the staging: a flow-insensitive analysis first gives safe def-use chains for memory, and the flow-sensitive analysis then runs only along them. Later frameworks for LLVM build a sparse value-flow graph in the same way.

## References
