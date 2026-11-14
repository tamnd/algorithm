---
tag: Q7GZTS
kind: algorithm
slug: offline-variable-substitution
name: Offline variable substitution
aliases:
- pointer equivalence detection
area: compilers-and-program-analysis/pointer-and-alias-analysis
level: advanced
summary: Finds variables with surely equal points-to sets before solving and merges them, which shrinks the constraint graph.
solves: [points-to-analysis]
model: word-ram
complexity:
  vars: {n: the number of variables (each variable is also a location), m: the number of pointer statements}
  time: {worst: O(n^3 + m)}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, recursive: false, online: false, flow_sensitive: false, context_sensitive: false}
history:
  year: 2000
  people: [Atanas Rountev, Satish Chandra]
  note: Rountev and Chandra found, with a linear pass over the copy graph, many variables whose sets must be equal, and solved Andersen's constraints for one variable of each group.
prereqs: [strongly-connected-components, tarjan-scc, andersen-analysis]
see_also: [online-cycle-elimination, hybrid-cycle-detection, steensgaard-analysis, topological-sort, points-to-analysis, three-address-code]
sources:
  - paper: doi:10.1145/349299.349310
    title: Atanas Rountev and Satish Chandra, Off-line variable substitution for scaling points-to analysis, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2000), 47 to 56, 2000
    locator: whole paper (the copy graph, the variables that receive values only through copies, the substitution and its measurements on C programs)
  - paper: doi:10.1145/1250734.1250767
    title: Ben Hardekopf and Calvin Lin, The ant and the grasshopper, fast and accurate pointer analysis for millions of lines of code, Proceedings of the ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI '07), 290 to 299, 2007
    locator: the section on offline variable substitution as a step before the solver
  - paper: "Lars Ole Andersen, Program Analysis and Specialization for the C Programming Language, PhD thesis, DIKU, University of Copenhagen, 1994 (DIKU report 94/19)"
    locator: the chapter on pointer analysis (the inclusion constraints that the substitution rewrites)
---

Offline variable substitution makes [Andersen's analysis](/andersen-analysis/) faster without a change to its result. Before the solver starts, it looks only at the statements and finds groups of variables whose least points-to sets must be equal. It then rewrites the statements so that each group is one variable, solves the smaller system, and gives each variable the set of its group. The test is simple: a variable that gets values only by copies from other variables, and from nothing else, has the union of their sets. Rountev and Chandra (2000) gave the method and found that many variables of C programs, most of them temporaries, are of this kind.

## In plain words

Many pointer variables in a program only receive copies of other pointers. A temporary that holds a copy of one pointer and nothing else will always hold the same addresses as that pointer. Pointers that copy each other in a circle also hold the same addresses. The method finds these groups before the real analysis starts, with one pass over the copy statements. It must be careful with any pointer that can get a value in another way: from an address, from a read through a pointer, or by a write through a pointer to it. Such a pointer starts a group of its own. The analysis then treats each group as one pointer, so it has less to do, and each pointer gets the result of its group.

## The problem

The input is a set of statements in the four basic forms `p = &a`, `p = q`, `p = *q` and `*p = q` over $n$ variables, and the output is the least solution $L$ of the subset constraints of Andersen's analysis, as on the page of the [points-to analysis](/points-to-analysis/) problem. The order is the subset order on each set, with the empty sets at the bottom, in the direction of Cousot. The analysis is flow-insensitive: it ignores the order of the statements, but not the statements that the control flow gives.

The *copy graph* has an edge $q \to p$ for each copy `p = q`. A variable is *indirect* if it can get a value other than by a copy: it is the left side of `p = &a` or of `p = *q`, or its address is taken in some `x = &p`, so that a store `*x = q` can write into it. All other variables are *direct*. The key fact: a direct variable gets values only through the edges of the copy graph, so its least set is the union of the sets of its sources.

## The algorithm

Each strongly connected component of the copy graph gets a label, and components with one label must have one least set. The labels go out in [topological order](/topological-sort/), so the sources of a component have their labels first.

```pseudo id=main
OVS(S)
L1  G <- the graph with an edge q -> p for each p = q in S
L2  X <- the variables p with p = &a or p = *q in S, and the a with p = &a in S
L3  for each strongly connected component C of G, in topological order do
L4      if C has a variable in X then label[C] <- a fresh label
L5      else P <- the labels of the components with an edge into C, without EMPTY
L6          if P is empty then label[C] <- EMPTY
L7          else if P has one label l then label[C] <- l
L8          else label[C] <- a fresh label
L9  rep[v] <- the first variable with the label of v, for each variable v
L10 S' <- S with each variable v replaced by rep[v], except the a of p = &a; drop the copies r = r and repeats
L11 M <- the result of Andersen's solver on S', with the set of a location a kept at rep[a]
L12 return M[rep[v]] for each variable v
```

The label EMPTY marks the direct components that nothing flows into: their sets are surely empty. The addresses in the sets stay the original locations (line L10): if $q$ and $r$ are in one group, a pointer to $q$ does not point to $r$. The implementation finds the components with an iterative form of [Tarjan's algorithm](/tarjan-scc/), which gives them in reverse topological order.

## Example

The program, in the toy IR:

```
entry:
  p = &a
  a = &b
  q = p
  r = q
  s = r
  r = s
  u = q
  u = s
  t = *u
  ret 0
```

The copy graph has the edges $p \to q$, $q \to r$, $r \to s$, $s \to r$, $q \to u$ and $s \to u$. The set $X$ is $\{p, a, b, t\}$: $p$ and $a$ are the left sides of `p = &a` and `a = &b`, $a$ and $b$ have their addresses taken, and $t$ is the left side of a load.

| component | in $X$ | labels of the sources | label |
|---|---|---|---|
| $\{p\}$ | yes | | 1 (fresh) |
| $\{a\}$, $\{b\}$, $\{t\}$ | yes | | a fresh label each |
| $\{q\}$ | no | $\{1\}$ from $p$ | 1 |
| $\{r, s\}$ | no | $\{1\}$ from $q$ | 1 |
| $\{u\}$ | no | $\{1\}$ from $q$ and $s$ | 1 |

So $p$, $q$, $r$, $s$ and $u$ form one group with the representative $p$. The variable $u$ has two sources, but both carry the label 1, so it joins too. The nine statements become three:

```
p = &a
a = &b
t = *p
```

The solver gives $M(p) = \{a\}$, $M(a) = \{b\}$ and $M(t) = \{b\}$ on four nodes instead of eight variables. Line L12 gives $pts(q) = pts(r) = pts(s) = pts(u) = \{a\}$, which is the result of Andersen's analysis on the original program.

If the program also had `w = &q` and `*w = c` with `c = &d`, then $q$ would have its address taken. It would be in $X$ and get a fresh label, since the store writes $d$ into its set but not into the set of $p$.

## Correctness

The full proof is in the proof file. Its steps:

1. **A direct component gets only what its sources give.** If no variable of a component is in $X$, its least set is the union of the least sets of the variables with an edge into it. The proof makes the set of the component equal to that union, checks that the result is still a solution, and uses the fact that $L$ is the least one. A store cannot write into a direct variable, since every address in a least set is the address of a variable in $X$.
2. **Equal labels mean equal sets.** By induction in topological order: a fresh label belongs to one component, whose members share a set because they copy each other in a cycle; EMPTY components get a union of empty sets; a component that takes the label of all its sources gets their common set.
3. **The rewritten system has the same least solution.** The original least solution, read on the representatives, solves the rewritten system, so the rewritten least solution is no larger. The rewritten least solution, read back on all variables, solves the original system, so it is no smaller.

So any correct solver for the rewritten system gives Andersen's result after the map back.

## Complexity

**Proved.** Lines L1 to L10 take $O(n + m)$ time and space: Tarjan's algorithm is linear, and each edge into a component is looked at once for its label. The solver then runs on $n' \le n$ nodes, with sets of at most $n$ locations, in $O(n'^2 n)$ time with difference propagation. The total is within Andersen's bound of $O(n^3 + m)$ time and $O(n^2 + m)$ space. The substitution does not lower the worst case.

**Stated in the paper, not proved here.** Rountev and Chandra report that on C programs the substitution removes a large part of the variables before solving and makes the analysis much faster. Hardekopf and Lin (2007) use it as a first step before their solvers for programs of millions of lines.

**Measured, not proved.** On the 400 seeded random programs of the test file, of up to 12 variables and 30 statements, the 2460 variables become 1853 nodes and the 5630 distinct statements become 4154. On 200 random programs of 20 variables and 30 statements with mostly copies, the 3823 variables become 1611 nodes and the 5895 statements become 3113. The result equals Andersen's least solution in every case.

## Properties

- **Same result as Andersen's analysis.** The substitution changes the system, not its least solution.
- **Offline.** It looks only at the statements, before any solving, and costs linear time.
- **Weaker than the truth.** It finds only some of the variables with equal least sets. Variables that become equal through loads and stores, or through cycles that loads and stores close, are left to the solver or to [online cycle elimination](/online-cycle-elimination/).
- **Works with any solver.** The rewritten system is an ordinary system of the four forms, plus the map from locations to nodes.
- **Locations stay apart.** Only the pointers are merged; the addresses in the sets are the original ones.

## Variants and improvements

- **Hash-based value numbering.** Hardekopf and Lin (SAS 2007) gave each variable a set of labels and merged variables with equal label sets, with ideas from value numbering. This finds more equal variables, including some that receive values from loads, and also finds locations that are equal.
- **Cycles in the solver.** Online and [lazy or hybrid cycle detection](/hybrid-cycle-detection/) merge the cycles that only appear while the solver runs. The hybrid method uses an offline pass over the same graph, with extra nodes for the loads and stores.
- **Unification.** [Steensgaard's analysis](/steensgaard-analysis/) merges every pair of variables joined by a copy, which is much more than this method and loses precision.

## When to use it

Use it as a cheap first step before any inclusion-based solver for large programs, especially for code produced by a compiler front end, such as [three-address code](/three-address-code/), which has many temporaries that only copy another value. It costs linear time and never changes the answer. It helps less when most pointers are written through other pointers, as in code with many heap structures.

## Pitfalls

- **Forgetting the stores.** A variable whose address is taken can be written by a store `*x = q`. If it is merged with its copy source, the facts from the store spread to the source, or are lost. Treat every variable whose address is taken as indirect.
- **Merging the locations.** The rewritten `p = &a` must keep $a$ as it is, and the solver must read the set of $a$ at $rep(a)$. Replacing $a$ by $rep(a)$ in the sets makes a pointer to $a$ seem to point to its whole group.
- **Two sources with different labels.** The union of two different sets is not equal to either one. Such a component needs a fresh label, unless one of the sources is surely empty.
- **The wrong order.** Labels must go out in topological order; a component whose sources have no labels yet cannot take one.

## Implementations

## History

Andersen's analysis (1994) was too slow for large C programs, and much of its work went into variables that were only copies of others. Rountev and Chandra (2000) found these variables with a linear pass over the copy graph, before solving, and reported large savings on C programs. Fähndrich, Foster, Su and Aiken (1998) had merged cycles during solving; the two methods work together. Hardekopf and Lin (2007) used offline substitution with their lazy and hybrid cycle detection, and in a second paper the same year extended it with hash-based value numbering, which finds more equal pointers and also equal locations.

## References
