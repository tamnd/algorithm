---
tag: S6Y6MV
kind: data-structure
slug: e-graph
name: E-graph
aliases:
- equality graph
- egraph
area: logic-and-constraints/smt
level: advanced
summary: A union-find over e-classes of e-nodes with a hash-cons table. It stores a congruence over a growing set of terms and supports add, merge, rebuild and lookup.
model: word-ram
complexity:
  vars: {n: the number of e-nodes, k: the largest arity of a function symbol}
  time: {find: O(log(k n)), add: O(k log(k n)) expected, rebuild: O(k^2 n log(k n)^2) expected}
  space: {total: O(k n log(k n))}
history:
  year: 1980
  people: [Greg Nelson, Derek C. Oppen]
  note: Nelson and Oppen used the E-graph in their congruence closure procedure of 1980, and Kozen used the same idea in 1977. Willsey and others added deferred rebuilding in 2021.
prereqs: [disjoint-set, hash-consing, term-dag, congruence-closure]
see_also: [e-matching, euf-satisfiability, quantifier-instantiation, theory-conflict-explanation, cdcl-t, union-by-size, bellman-ford]
sources:
  - paper: doi:10.1145/3434304
    title: Max Willsey, Chandrakana Nandi, Yisu Remy Wang, Oliver Flatt, Zachary Tatlock and Pavel Panchekha, egg, fast and extensible equality saturation, Proceedings of the ACM on Programming Languages 5(POPL), 2021
    locator: Section 3, Rebuilding (the deferred restoration of the invariants), and Section 4, e-class analyses
  - paper: doi:10.1145/322186.322198
    title: Greg Nelson and Derek C. Oppen, Fast decision procedures based on congruence closure, Journal of the ACM 27(2), 1980, pages 356 to 364
    locator: the graph representation of terms and the merge procedure
  - paper: doi:10.1145/800105.803406
    title: Dexter Kozen, Complexity of finitely presented algebras, Proceedings of the Ninth Annual ACM Symposium on Theory of Computing, 1977, pages 164 to 177
    locator: the congruence closure of a finite presentation
  - paper: doi:10.1145/1066100.1066102
    title: David Detlefs, Greg Nelson and James B. Saxe, Simplify, a theorem prover for program checking, Journal of the ACM 52(3), 2005, pages 365 to 473
    locator: the E-graph and its use for matching
  - paper: doi:10.1145/1480881.1480915
    title: Ross Tate, Michael Stepp, Zachary Tatlock and Sorin Lerner, Equality saturation, a new approach to optimization, POPL 2009, pages 264 to 276
    locator: the E-PEG and the extraction of an optimized program
  - paper: doi:10.1145/322217.322228
    title: Peter J. Downey, Ravi Sethi and Robert E. Tarjan, Variations on the common subexpression problem, Journal of the ACM 27(4), 1980, pages 758 to 771
    locator: the relabelling of the smaller class and the signature table
---

An e-graph stores many terms and an equivalence relation on them in a compact form. Each e-class is a set of equal terms, and each e-node is a function symbol applied to e-classes, not to terms. So one e-node $f(c)$ stands for $f(t)$ for every term $t$ in the class $c$. A union-find joins classes, and a hash-cons table finds the class of an e-node. After a call to *rebuild*, the relation is closed under congruence: if the arguments of two e-nodes are in the same classes, the two e-nodes are in the same class. [Congruence closure](/congruence-closure/) is the algorithm that the e-graph runs. The e-graph is the data structure that keeps the result, and lets [E-matching](/e-matching/) and term extraction read it.

## In plain words

Think of a dictionary of words, where words that mean the same thing are put in one box. A long phrase is written with boxes in place of its words. So one phrase in the dictionary stands for all phrases that you get by picking any word from each box.

When you learn that two boxes hold words of the same meaning, you pour one box into the other. Some phrases now look the same, because their parts point to the same box. Those phrases then mean the same thing too, so their boxes must also be poured together.

An e-graph does this with terms of a program or a formula. It can wait and do all the pouring at once, which is faster when many facts arrive in a row.

## The abstract type

An e-graph holds a finite set $T$ of ground terms, closed under subterms, and an equivalence relation $\sim$ on $T$. In a clean state, $\sim$ is the [congruence closure](/congruence-closure/) of the equations merged so far. It supports these operations:

- ADD$(n)$: add an e-node, and so a term, and return its class.
- MERGE$(x, y)$: assert that two classes are equal. The classes are joined at once, but the congruence closure is restored only by REBUILD.
- REBUILD(): restore the congruence invariant.
- FIND$(x)$: the canonical id of the class of $x$.
- LOOKUP$(t)$: the class that represents the term $t$, or nil, in a clean state.
- Extraction: for each class, a term of least cost that it represents.

It is a [disjoint-set](/disjoint-set/) structure whose elements are terms with shared structure, as in a [term DAG](/term-dag/), with the extra rule of congruence.

## Representation

The e-graph has these fields:

- $\mathit{uf}$: a union-find array over class ids. A class id $x$ is canonical when $\mathit{uf}[x] = x$.
- $\mathit{nodes}[x]$: the list of e-nodes of the canonical class $x$. An e-node is $f(c_1, \ldots, c_k)$ for a symbol $f$ of arity $k$ and class ids $c_i$.
- $\mathit{parents}[x]$: a list of entries $(n, y)$, where $n$ is an e-node of class $y$ with an argument in class $x$.
- $\mathit{memo}$: a hash table from e-nodes to class ids, the hash-cons table.
- $\mathit{pending}$: a list of parent entries whose e-nodes may have changed their canonical form.

The *canonical form* of $f(c_1, \ldots, c_k)$ is $f(\mathrm{FIND}(c_1), \ldots, \mathrm{FIND}(c_k))$.

**Invariants.** These hold at all times.

- (E1) For each e-node $n$ of class $y$ and each argument $c_i$ of $n$, the entry $(n, y)$ is in $\mathit{parents}[\mathrm{FIND}(c_i)]$.
- (E2) For each e-node $n$ of class $y$, either $\mathrm{FIND}(\mathit{memo}[\mathrm{CANONICAL}(n)]) = \mathrm{FIND}(y)$, or an entry $(n, y)$ is on $\mathit{pending}$.
- (E3) Each pair of classes that is joined is equal in the congruence closure of the merged equations.

In a *clean* state, $\mathit{pending}$ is empty. Then (E2) gives the *congruence invariant*: two e-nodes with the same canonical form are in the same class, because both lead to the same entry of $\mathit{memo}$.

## Operations

```pseudo id=main
ADD(n = f(c1, …, ck))                       ▷ returns the class of n
L1  n ← f(FIND(c1), …, FIND(ck))
L2  if n is in memo then return FIND(memo[n])
L3  x ← a new class id with uf[x] = x, nodes[x] = [n], parents[x] = []
L4  for i = 1 … k: append (n, x) to parents[ci]
L5  memo[n] ← x
L6  return x

MERGE(x, y)
L7  x ← FIND(x), y ← FIND(y)
L8  if x = y then return false
L9  if |parents[x]| > |parents[y]| then swap x and y
L10 uf[x] ← y
L11 append nodes[x] to nodes[y]
L12 append parents[x] to pending
L13 append parents[x] to parents[y]
L14 return true

REBUILD()
L15 while pending is not empty do
L16     (n, y) ← remove an item of pending
L17     n ← CANONICAL(n)
L18     if n is in memo and FIND(memo[n]) ≠ FIND(y) then MERGE(memo[n], y)
L19     memo[n] ← FIND(y)

LOOKUP(t)                                   ▷ in a clean state
L20 if t = f(t1, …, tk) then ci ← LOOKUP(ti) for i = 1 … k
L21 if some ci is nil then return nil
L22 n ← f(c1, …, ck)
L23 if n is in memo then return FIND(memo[n]) else return nil
```

**ADD.** Line L1 puts the e-node in canonical form, and line L2 returns the existing class if the hash-cons table has it. This is [hash-consing](/hash-consing/): the same e-node is never stored twice in a clean state. A new e-node gets its own class, and line L4 registers it as a parent of each argument class. A term is added bottom up, one e-node per subterm.

**MERGE.** Lines L7 to L10 are a [union-find](/disjoint-set/) link. Line L9 links the class with the shorter parent list below the other, as in [union by size](/union-by-size/). Only the e-nodes with an argument in the class $x$ change their canonical form, since $x$ is no longer canonical. Line L12 puts exactly these on $\mathit{pending}$. MERGE does not look them up, so it costs $O(\log(kn))$ for the finds, plus the length of the moved list.

**REBUILD.** Each pending entry is put in canonical form again. If the table already has an e-node with the same canonical form in another class, the two e-nodes are congruent, and line L18 joins the classes. This MERGE can add more entries to $\mathit{pending}$, and the loop goes on until it is empty. This is deferred rebuilding, as in egg. Many merges can come before one REBUILD, and the work for the parents is shared between them.

**LOOKUP.** A term $t$ is *represented* by the class $x$ when $t = f(t_1, \ldots, t_k)$ and $x$ has an e-node $f(c_1, \ldots, c_k)$ with each $t_i$ represented by $c_i$. LOOKUP finds this class without adding anything. A class can represent infinitely many terms. After a merge of $f(a)$ with $a$, the class of $a$ represents $a$, $f(a)$, $f(f(a))$ and so on.

**Extraction.** For a cost of each e-node, a best term of a class is one of least total cost that the class represents. The best costs are the least fixpoint of $\mathrm{cost}(x) = \min_{f(c_1, \ldots, c_k) \in x} \bigl(\mathrm{cost}(f) + \sum_i \mathrm{cost}(c_i)\bigr)$. A loop of rounds in the style of [Bellman-Ford](/bellman-ford/) finds it: a best term never has the same class twice on a path from its root, so its depth is at most the number of classes, and that many rounds are enough.

## Example

Add the terms $g(f(a))$, $g(f(b))$ and $f(c)$. This makes 8 classes, one for each distinct subterm: $a, f(a), g(f(a)), b, f(b), g(f(b)), c, f(c)$. Then MERGE$(a, b)$ and MERGE$(b, c)$ come before one REBUILD.

| step | action | pending after the step | classes |
|---|---|---|---|
| 1 | MERGE$(a, b)$: the parent lists both have length 1, so $a$ goes below $b$ | the entry of $f(a)$ | 7 |
| 2 | MERGE$(b, c)$: $c$ has the shorter parent list, so $c$ goes below $b$ | the entries of $f(a)$ and $f(c)$ | 6 |
| 3 | REBUILD takes $f(c)$: its canonical form is $f(b)$, which is in $\mathit{memo}$ with the class of $f(b)$, so join | the entry of $f(a)$ | 5 |
| 4 | REBUILD takes $f(a)$: its canonical form is also $f(b)$, so join with the class of $f(b)$. Both parent lists have length 1, and the class of $f(b)$ goes below | the entry of $g(f(b))$ | 4 |
| 5 | REBUILD takes $g(f(b))$: its canonical form is now equal to that of $g(f(a))$, so join | empty | 3 |

The final classes are $\{a, b, c\}$, $\{f(a), f(b), f(c)\}$ and $\{g(f(a)), g(f(b))\}$. LOOKUP$(g(f(c)))$ now returns the third class, though this term was never added, and LOOKUP$(g(c))$ returns nil. With cost 1 for each e-node, extraction gives the terms $b$, $f(b)$ and $g(f(b))$ of size 1, 2 and 3, or other terms of the same size, depending on the order of the e-nodes.

## Correctness

Each operation keeps (E1), (E2) and (E3). ADD adds the entries of (E1) and the table entry of (E2). MERGE moves the parent list of $x$ to $y$, which keeps (E1), and puts each e-node whose canonical form changed on $\mathit{pending}$, which keeps (E2). REBUILD joins only congruent e-nodes, which keeps (E3), and it removes an entry only after it has set the table entry of (E2). REBUILD stops, because each join lowers the number of classes and each other step removes one entry. So in a clean state the relation is closed under congruence by (E2), it contains the merged equations, and by (E3) it is not larger than the congruence closure. LOOKUP is correct in a clean state by induction on the term, using the congruence invariant. The full proof is in the [proof page](proofs/correctness.md).

## Complexity

Let $n$ be the number of e-nodes, $k$ the largest arity, and $W = n + kn$, a bound on the total length of the parent lists.

| operation | cost |
|---|---|
| FIND | $O(\log W)$ worst case |
| ADD | $O(k \log W)$ worst case, plus one table operation, $O(k)$ expected time with hashing |
| MERGE | $O(\log W)$ plus the length of the moved parent list |
| REBUILD, total over a whole run | at most $kn \log_2 W$ pending entries, each $O(k \log W)$ plus one table operation |
| LOOKUP$(t)$ | $O(\lvert t \rvert \, k \log W)$, plus $\lvert t \rvert$ table operations |
| extraction | at most $c$ rounds over all e-nodes, for $c$ classes |

**Union-find depth.** Give each class the weight $|\mathit{parents}[x]| + 1$. Weights only grow, and line L9 links the lighter class below the heavier one. So the depth of an id grows by one only when the weight of its tree at least doubles, and the depth is at most $\log_2 W$. Path halving makes the finds faster in practice, but the bound above does not use it.

**Pending entries.** An entry moves to $\mathit{pending}$ only at line L12, when its list is the shorter one, and then its new list is at least twice as long. A list has at most $kn$ entries, so each entry moves at most $\log_2(kn)$ times. There are at most $kn$ entries in total, one for each argument position of each e-node. This is the counting of Downey, Sethi and Tarjan, so for a fixed arity the whole run does $O(n \log n)$ table operations, the same as eager [congruence closure](/congruence-closure/).

**Space.** The lists use $O(kn)$ space. The table keeps old keys: each pending entry can leave one key that is no longer canonical, so the table can hold $O(kn \log(kn))$ keys.

## Variants

- **Eager e-graphs in SMT solvers.** An SMT solver such as Z3 restores congruence after each merge, as in the [congruence closure](/congruence-closure/) page. It also keeps a trail to undo merges when the [CDCL(T)](/cdcl-t/) search backtracks, and a proof forest to [explain](/theory-conflict-explanation/) each equality. Deferred rebuilding fits better when there is no backtracking and many merges come in a batch.
- **E-class analysis.** egg attaches a value from a semilattice to each class, such as a constant or a type, and joins the values at each merge. A rewrite can then read the value of a class.
- **E-matching.** [E-matching](/e-matching/) finds the substitutions that make a pattern with variables equal to a term of a class. SMT solvers use it for [quantifier instantiation](/quantifier-instantiation/), and equality saturation uses it to apply rewrites.
- **Equality saturation.** Tate, Stepp, Tatlock and Lerner apply all rewrite rules to an e-graph again and again, so that it holds many equivalent programs at once, and then extract the best program. When shared subterms are counted once, the simple fixpoint of extraction is not exact any more, and they used a pseudo-Boolean solver for it.
- **Removing old keys.** egg removes the old key of a parent entry from the table before it inserts the new one. This keeps the table at $O(kn)$ keys.

## When to use it

Use an e-graph when a program needs to keep many terms and equalities between them, and to ask which terms are equal or which terms a class represents. Examples are the EUF solver of an SMT solver, E-matching for quantifiers, and optimizers that rewrite programs by equality saturation. To decide only one conjunction of [EUF](/euf-satisfiability/) literals, the [congruence closure](/congruence-closure/) algorithm is enough, and an e-graph adds nothing. Use deferred rebuilding when many merges come before each query. Use eager congruence with a trail when the solver must backtrack.

## Pitfalls

- **Queries in a dirty state.** Between MERGE and REBUILD the congruence invariant does not hold. LOOKUP, E-matching and extraction can then miss equal terms. FIND is always correct for the merges made so far.
- **Keys that are not canonical.** The table must be read with the canonical form of an e-node. An e-node built with old class ids misses its entry.
- **Unbounded growth by rewrites.** A rewrite such as $x \to x + 0$ adds new e-nodes each time it is applied. Equality saturation needs a limit on the number of e-nodes or rounds.
- **Recursion on deep terms.** Terms with long chains, such as $f$ applied a thousand times, overflow a recursive ADD or LOOKUP. The implementation uses an explicit stack.
- **Counting shared nodes in extraction.** The fixpoint gives the least tree cost. If an e-node that is used twice should be paid for once, this is a different problem.

## Implementations

## History

Kozen gave congruence closure for finitely presented algebras in 1977. Nelson and Oppen used a graph of terms with merged classes in their congruence closure procedure of 1980, and Downey, Sethi and Tarjan gave the $O(n \log n)$ method in the same year. Nelson's E-graph became the core of the Simplify prover, which used it for matching of quantified formulas, as Detlefs, Nelson and Saxe describe in 2005. Joshi, Nelson and Randall used it in the Denali superoptimizer in 2002. Tate and others introduced equality saturation in 2009. Willsey and others gave deferred rebuilding and e-class analyses in the egg library in 2021.

## References
