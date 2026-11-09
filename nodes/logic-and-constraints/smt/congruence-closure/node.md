---
tag: QSSXKY
kind: algorithm
slug: congruence-closure
name: Congruence closure
aliases:
- congruence closure algorithm
- Downey-Sethi-Tarjan algorithm
area: logic-and-constraints/smt
level: advanced
summary: Computes the least congruence on a finite set of ground terms that contains given equations. It decides conjunctions of EUF equalities and disequalities in O(n log n) time.
solves: [euf-satisfiability]
model: word-ram
complexity:
  vars: {n: "the number of nodes of the term DAG plus the number of input equations, with the arity bounded by a constant"}
  time: {worst: "O(n log^2 n)", expected: "O(n log n)"}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1980
  people: [Greg Nelson, Derek C. Oppen, Peter J. Downey, Ravi Sethi, Robert E. Tarjan]
  note: Nelson and Oppen (1980) gave a congruence closure algorithm with an O(n^2) worst case, and Downey, Sethi and Tarjan (1980) gave the O(n log n) method with a signature table.
prereqs: [euf-satisfiability, disjoint-set, term-dag]
see_also: [e-graph, theory-conflict-explanation, ackermannization, nelson-oppen, dpll-t, union-by-size, hash-consing, knuth-bendix-completion]
sources:
  - paper: doi:10.1145/322217.322228
    title: Peter J. Downey, Ravi Sethi and Robert E. Tarjan, Variations on the common subexpression problem, Journal of the ACM 27(4), 1980, pages 758 to 771
    locator: the congruence closure problem on a labelled graph and the O(n log n) algorithm with a signature table
  - paper: doi:10.1145/322186.322198
    title: Greg Nelson and Derek C. Oppen, Fast decision procedures based on congruence closure, Journal of the ACM 27(2), 1980, pages 356 to 364
    locator: the congruence closure algorithm and its use to decide the quantifier-free theory of equality with uninterpreted functions
  - paper: doi:10.1016/j.ic.2006.08.009
    title: Robert Nieuwenhuis and Albert Oliveras, Fast congruence closure and extensions, Information and Computation 205(4), 2007, pages 557 to 580
    locator: the incremental algorithm with use lists and a lookup table, the proof forest and the Explain operation
  - paper: doi:10.1145/359545.359570
    title: Robert E. Shostak, An algorithm for reasoning about equality, Communications of the ACM 21(7), 1978, pages 583 to 585
    locator: the decision procedure for ground equalities with uninterpreted functions
  - paper: doi:10.1007/s10703-017-0283-x
    title: Andreas Fellner, Pascal Fontaine and Bruno Woltzenlogel Paleo, NP-completeness of small conflict set generation for congruence closure, Formal Methods in System Design 51(3), 2017, pages 533 to 544
    locator: the NP-completeness of the smallest explanation and smallest conflict set problems
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, An Algorithmic Point of View, second edition, Springer, 2016
    locator: Chapter 4, Equality Logic and Uninterpreted Functions
  - book: isbn:9783540741121
    title: Aaron R. Bradley and Zohar Manna, The Calculus of Computation, Springer, 2007
    locator: Chapter 9, Quantifier-Free Equality and Data Structures (the congruence closure algorithm and its correctness)
---

Congruence closure computes, for a finite set of ground terms and a set of equations between them, the least equivalence relation that contains the equations and is closed under congruence: if the arguments of two applications of the same function symbol are equivalent, the two applications are equivalent. It decides [EUF satisfiability](/euf-satisfiability/) for a conjunction of literals: the conjunction is satisfiable if and only if no disequality joins two equivalent terms. The method of Downey, Sethi and Tarjan relabels the smaller class at each merge and looks up the parents of that class in a signature table, so it runs in $O(n \log n)$ time with a hash table. It is the core of the [e-graph](/e-graph/) and of the EUF solver in each [DPLL(T)](/dpll-t/) solver.

## In plain words

You have a set of expressions such as "f of a" and "f of f of a", and a list of facts that say two expressions are equal. You want all the other equalities that follow. Two rules give them. Equality is an equivalence, so equal things chain together. And a function gives equal results on equal inputs, so if "a" equals "b", then "f of a" equals "f of b".

The algorithm keeps the expressions in groups of known-equal items. When a fact joins two groups, it moves the members of the smaller group into the larger one. Then it looks again at each expression that uses a moved member as an input, and checks in a table whether another expression with the same function and the same input groups already exists. If so, those two expressions are equal too, and the algorithm joins their groups next.

## The problem

**Notation.** A term is a constant $a$ or an application $f(t_1, \ldots, t_k)$ of a function symbol of arity $k \ge 1$ to terms. Let $T$ be a finite set of ground terms that is closed under subterms, stored as a [term DAG](/term-dag/) with one node for each distinct term. Let $E$ be a finite set of equations $s = t$ with $s, t \in T$. Here $n$ is the number of nodes of $T$ plus $|E|$, and the arity of each symbol is at most a constant. (In the area notation, $n$ counts variables. On this page it counts terms, because the terms are the variables of the problem.)

**Congruence closure.** An equivalence relation $\sim$ on $T$ is a *congruence* on $T$ when, for each pair of applications $f(s_1, \ldots, s_k)$ and $f(t_1, \ldots, t_k)$ in $T$ with the same symbol and $s_i \sim t_i$ for all $i$, also $f(s_1, \ldots, s_k) \sim f(t_1, \ldots, t_k)$. The intersection of congruences on $T$ is a congruence, and the relation $T \times T$ is one, so there is a least congruence on $T$ that contains $E$. This is the *congruence closure* $\mathrm{CC}(E)$.

**Output.** A partition of $T$ into the classes of $\mathrm{CC}(E)$, with a query "are $s$ and $t$ in the same class". For a conjunction of the equations $E$ and a set $D$ of disequations, the answer to [EUF satisfiability](/euf-satisfiability/) is "satisfiable" exactly when no $s \ne t$ in $D$ has $s$ and $t$ in the same class.

## The algorithm

Each node $u$ has a representative $\mathit{rep}[u]$. Each representative $r$ holds the list $\mathit{members}[r]$ of its class and the list $\mathit{uses}[r]$ of the applications that have an argument in the class. The signature of an application $p = f(c_1, \ldots, c_k)$ is $\mathrm{SIG}(p) = (f, \mathit{rep}[c_1], \ldots, \mathit{rep}[c_k])$. The table maps a signature to one node that had it when it was stored.

```pseudo id=main
CONGRUENCE-CLOSURE(T, E)                       ▷ T closed under subterms, children first
L1  for each node u of T: rep[u] ← u, members[u] ← [u], uses[u] ← []
L2  pending ← the equations of E
L3  for each application p = f(c1, …, ck) of T, in order:
L4      append p to uses[rep[ci]] for i = 1 … k
L5      if SIG(p) is in table then append (p, table[SIG(p)]) to pending
L6      else table[SIG(p)] ← p
L7  while pending is not empty do
L8      (a, b) ← remove an item of pending
L9      if rep[a] = rep[b] then continue
L10     if |members[rep[a]]| > |members[rep[b]]| then swap a and b
L11     ra ← rep[a], rb ← rep[b]
L12     for each x in members[ra]: rep[x] ← rb
L13     append members[ra] to members[rb]
L14     for each p in uses[ra]:
L15         if SIG(p) is not in table then table[SIG(p)] ← p
L16         else if rep[table[SIG(p)]] ≠ rep[p] then append (p, table[SIG(p)]) to pending
L17     append uses[ra] to uses[rb]
L18 return rep                                  ▷ s ~ t if and only if rep[s] = rep[t]
```

Lines L1 to L6 build the start state. Line L5 already finds terms that are equal by congruence alone, such as two copies of $f(a)$ in the input before [hash-consing](/hash-consing/). The loop of line L7 handles one merge at a time. Line L10 makes $ra$ the smaller class, by [union by size](/union-by-size/), and line L12 relabels it, so a find is one array read. A merge changes the signature only of the applications that have an argument in the class $ra$. Line L14 visits exactly these, because $\mathit{uses}[ra]$ lists them. For each, line L15 or L16 looks up the new signature. If a node with the same signature is in another class, the two nodes are congruent and line L16 queues their merge.

Old signatures stay in the table. They contain a representative that is no longer one, so a later lookup never matches them.

**Explanations.** To use congruence closure inside a [lazy SMT solver](/lazy-smt/), each merge also adds an edge to a *proof forest*. Before line L12, reverse the path from $a$ to the root of its proof tree, then add the edge $a \to b$ with its reason: the label of an input equation, or "congruence of $p$ and $q$". The proof trees then have the same node sets as the classes. EXPLAIN$(s, t)$ finds the nearest common ancestor of $s$ and $t$, collects the labels of input edges on the two paths, and for each congruence edge between $f(s_1, \ldots, s_k)$ and $f(t_1, \ldots, t_k)$ explains each pair $s_i, t_i$ in the same way. This is the method of Nieuwenhuis and Oliveras. The result is a [theory conflict explanation](/theory-conflict-explanation/) when $s \ne t$ is asserted.

## Example

Let $E = \{f^3(a) = a,\ f^5(a) = a\}$, where $f^k(a)$ means $f$ applied $k$ times to $a$. The set $T$ has the six terms $a, f(a), \ldots, f^5(a)$, and $D = \{f(a) \ne a\}$. The table starts with the signatures $(f, a)$ for $f(a)$, $(f, f(a))$ for $f^2(a)$, and so on.

| step | pop from pending | reason | relabelled class | parent looked up | new pending | classes after the step |
|---|---|---|---|---|---|---|
| 1 | $f^3(a), a$ | input | $\{f^3(a)\}$ | $f^4(a)$ has $(f, a)$, held by $f(a)$ | $f^4(a), f(a)$ | $\{a, f^3a\}$, $\{fa\}$, $\{f^2a\}$, $\{f^4a\}$, $\{f^5a\}$ |
| 2 | $f^4(a), f(a)$ | congruence | $\{f^4(a)\}$ | $f^5(a)$ has $(f, f(a))$, held by $f^2(a)$ | $f^5(a), f^2(a)$ | $\{a, f^3a\}$, $\{fa, f^4a\}$, $\{f^2a\}$, $\{f^5a\}$ |
| 3 | $f^5(a), f^2(a)$ | congruence | $\{f^5(a)\}$ | none | none | $\{a, f^3a\}$, $\{fa, f^4a\}$, $\{f^2a, f^5a\}$ |
| 4 | $f^5(a), a$ | input | $\{f^2a, f^5a\}$ | $f^3(a)$ has $(f, a)$, held by $f(a)$ | $f^3(a), f(a)$ | $\{a, f^3a, f^2a, f^5a\}$, $\{fa, f^4a\}$ |
| 5 | $f^3(a), f(a)$ | congruence | $\{fa, f^4a\}$ | $f^2(a)$ and $f^5(a)$ match their own class | none | one class |

After the first equation alone there are three classes, so $f^3(a) = a \wedge f(a) \ne a$ is satisfiable. After both equations, $f(a)$ and $a$ are in the same class, so $f^3(a) = a \wedge f^5(a) = a \wedge f(a) \ne a$ is unsatisfiable. In step 4 both classes have two members, and the tie keeps the class of $a$ as the representative. EXPLAIN$(f(a), a)$ walks the proof forest and returns both input equations, which is the conflict $\{f^3(a) = a, f^5(a) = a, f(a) \ne a\}$.

## Correctness

At the end, $\mathit{rep}[s] = \mathit{rep}[t]$ if and only if $s$ and $t$ are in the same class of $\mathrm{CC}(E)$. Soundness holds because each queued pair is an input equation or a pair of applications whose arguments are already in the same class, so by induction each merge joins two terms of the same class of $\mathrm{CC}(E)$. Completeness rests on this invariant of the table: for each application $p$, the entry $\mathit{table}[\mathrm{SIG}(p)]$ exists and is in the class of $p$ or in a pair with $p$ on pending. When the loop stops, two congruent applications have the same signature, so they share a table entry and are in one class. The decision procedure is correct because the classes of $\mathrm{CC}(E)$ give a model of $E$ and the disequations (the term model), and each model of $E$ makes congruent terms equal. The full proofs, with the proof that $\mathrm{CC}(E)$ is the set of equations between terms of $T$ that $E$ entails, are in the [proof page](proofs/correctness.md).

## Complexity

Let $n$ be the number of nodes plus $|E|$, and let the arity be at most a constant $a$.

- **Relabelling.** A node is relabelled at line L12 only when its class is the smaller one, and after the merge its class is at least twice as large. A class has at most $n$ nodes, so each node is relabelled at most $\lg n$ times: $O(n \log n)$ in total.
- **Use lists.** Line L4 makes one entry for each argument position, so there are at most $a n$ entries. An entry moves with the class of its argument and is visited at line L14 only when that class is the smaller one, so at most $\lg n$ times. Each visit computes a signature in $O(a)$ steps and does one table operation: $O(a^2 n \log n)$ steps and $O(a n \log n)$ table operations.
- **Pending.** Each item comes from an equation of $E$, from line L5 or from a visit at line L16, so there are $O(a n \log n)$ items, and at most $n - 1$ of them cause a merge.
- **The table.** With a hash table each operation takes expected $O(1)$ time, so the total is expected $O(n \log n)$ for a constant arity. With a balanced search tree each operation takes $O(\log n)$ time in the worst case, so the total is $O(n \log^2 n)$ in the worst case.
- **Space.** The arrays, lists and table take $\Theta(n)$ words.
- **Explain.** Each proof forest edge is expanded at most once in one call, so at most $1 + a(n - 1)$ pairs are explained, and each walks paths of length at most $n$. One call takes $O(a n^2)$ time in this simple form. Nieuwenhuis and Oliveras give a faster version with a second union-find.

In an incremental use, these bounds hold for the whole sequence of merges, not for each merge.

## Properties

- **Incremental.** The algorithm accepts new terms and new equations at any time. The state after each merge is the closure of the equations so far. This is what a theory solver in [CDCL(T)](/cdcl-t/) needs.
- **Not backtrackable as written.** To undo merges, keep a trail of the changes and undo them in reverse order, as in [union-find with rollback](/union-find-with-rollback/). With relabelling, one merge changes only the entries of the moved class, so the trail stays short.
- **Deterministic and non-recursive.** The implementation uses an explicit stack to add deep terms.
- **Explanations are not minimal.** The explanation of an equality need not be a smallest set of inputs, and it need not even be irredundant. For the inputs $b = f(b)$, $f(a) = a$, $f(b) = a$, in this order, EXPLAIN$(b, f(a))$ returns all three, but the first and the third already give $b = a$ and then $f(a) = f(b) = b$. To find a smallest explanation is NP-hard (Fellner, Fontaine and Woltzenlogel Paleo, 2017; see [theory conflict explanation](/theory-conflict-explanation/)).

## Variants and improvements

- **The quadratic method.** Nelson and Oppen (1980) merge two classes and then compare the predecessors of the two classes pair by pair. This is simpler, and it takes $O(n^2)$ time in the worst case.
- **Curried terms.** Downey, Sethi and Tarjan, and also Nieuwenhuis and Oliveras, first rewrite each term into binary applications of one symbol $\cdot$, so $f(a, b)$ becomes $\cdot(\cdot(f, a), b)$. This bounds the arity by 2 for any input, at the cost of a constant factor in size.
- **The e-graph.** An [e-graph](/e-graph/) keeps the classes and the nodes of each class, so it can list all terms equal to a given term, and it is the data structure of [e-matching](/e-matching/) and of equality saturation.
- **Interpreted extensions.** Nieuwenhuis and Oliveras extend the method to integer offsets ($s = t + k$). Combined with other theories, the method gives the EUF part of [Nelson-Oppen](/nelson-oppen/) and of [Shostak's method](/shostak-combination/).
- **Completion view.** Congruence closure can be seen as [Knuth-Bendix completion](/knuth-bendix-completion/) of a set of ground equations, with new constants as names of the classes. Bachmair, Tiwari and Vigneron (abstract congruence closure, 2003) describe it in this way.

## When to use it

Use congruence closure for a conjunction of equalities and disequalities over uninterpreted function symbols, and as the EUF solver inside an SMT solver. For a formula with Boolean structure, use it in a [lazy SMT](/lazy-smt/) loop, or remove the functions by [Ackermannization](/ackermannization/) and use an [eager encoding](/eager-smt-encoding/). If the input has no function symbols at all, a plain [disjoint-set](/disjoint-set/) structure is enough. Congruence closure is not [unification](/unification-problem/): unification treats variables as unknowns to solve for, while congruence closure treats all terms as fixed ground terms.

## Pitfalls

- **Losing the use list of the smaller class.** Only the parents of the smaller class need a new lookup, because only their signatures change. But line L17 must still append $\mathit{uses}[ra]$ to $\mathit{uses}[rb]$. If the entries are dropped, a later merge of the class $rb$ does not look at these parents again, and a congruence is missed.
- **Signatures with stale representatives.** A signature must be computed with the representatives at the time of the lookup. A key built when the node was created is wrong after a merge.
- **Arity in the key.** The key must include the symbol and all argument classes. A symbol used with two arities, such as $h(a)$ and $h(a, a)$, gives different keys.
- **Recursion on deep terms.** A term such as $f^{3000}(a)$ breaks a recursive traversal in Python. Add terms with an explicit stack.
- **Path compression with backtracking.** A theory solver must undo merges when the SAT search backtracks. Path compression changes many pointers in one find, so a trail of changes is long. Relabelling with union by size changes only the moved class.

## Implementations

## History

Shostak (1978) and Nelson and Oppen (1980) gave the first congruence closure algorithms used to decide equality with uninterpreted functions, and Nelson and Oppen proved the $O(n^2)$ bound of their method. Downey, Sethi and Tarjan (1980) studied the problem as a variation of the common subexpression problem on labelled graphs and gave the $O(n \log n)$ method with a signature table. Nieuwenhuis and Oliveras (2005 and 2007) added the proof forest and the explain operation for use inside DPLL(T). Fellner, Fontaine and Woltzenlogel Paleo (2017) proved that a smallest explanation is NP-hard to find.

## References
