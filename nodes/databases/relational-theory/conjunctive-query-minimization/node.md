---
tag: PG64E9
kind: algorithm
slug: conjunctive-query-minimization
name: Conjunctive query minimization
aliases:
- tableau minimization
- query core computation
area: databases/relational-theory
level: advanced
summary: Find the smallest equivalent conjunctive query by deleting atoms while the query still maps homomorphically into the smaller one.
model: word-ram
complexity:
  vars: {k: the number of atoms of the query, a: the largest arity of a relation}
  time: {worst: O(a k^(k+1))}
  space: {extra: O(a k^2)}
prereqs: [conjunctive-query, query-containment-problem, chandra-merlin-theorem]
see_also: [sagiv-yannakakis-theorem, query-optimization, data-exchange-core-computation, chase-algorithm, three-coloring, constraint-satisfaction-problem, acyclic-hypergraph, treewidth]
sources:
  - paper: doi:10.1145/800105.803397
    title: Ashok K. Chandra and Philip M. Merlin, Optimal implementation of conjunctive queries in relational data bases, Proceedings of the 9th Annual ACM Symposium on Theory of Computing (STOC), 77 to 90 (1977)
    locator: the minimization of conjunctive queries by homomorphisms and the uniqueness of the minimal query up to renaming
  - paper: doi:10.1145/320107.320112
    title: Alfred V. Aho, Yehoshua Sagiv and Jeffrey D. Ullman, Efficient optimization of a class of relational expressions, ACM Transactions on Database Systems 4(4), 435 to 454 (1979)
    locator: tableau minimization, and the polynomial-time method for simple tableaux
  - paper: doi:10.1137/0208017
    title: Alfred V. Aho, Yehoshua Sagiv and Jeffrey D. Ullman, Equivalences among relational expressions, SIAM Journal on Computing 8(2), 218 to 246 (1979)
    locator: tableaux for select-project-join expressions and the NP-completeness of their equivalence
  - paper: doi:10.1016/S0304-3975(99)00220-0
    title: Chandra Chekuri and Anand Rajaraman, Conjunctive query containment revisited, Theoretical Computer Science 239(2), 211 to 229 (2000)
    locator: polynomial-time containment and minimization for acyclic queries and for queries of bounded query width
  - paper: doi:10.1145/153850.153856
    title: Surajit Chaudhuri and Moshe Y. Vardi, Optimization of real conjunctive queries, Proceedings of the 12th ACM Symposium on Principles of Database Systems (PODS), 59 to 70 (1993)
    locator: containment and equivalence of conjunctive queries under bag semantics
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 6 (static analysis and optimization), the section on query minimization and tableaux
---

Conjunctive query minimization takes a [conjunctive query](/conjunctive-query/) and returns an equivalent conjunctive query with the smallest number of atoms. It tries each atom once: if the query has a homomorphism into the query without that atom, the atom is redundant, and it goes. Chandra and Merlin (1977) showed that the result is the *core* of the query, which is unique up to a renaming of the variables, and that no equivalent conjunctive query has fewer atoms. A query with fewer atoms needs fewer joins, so this is the classic step of semantic [query optimization](/query-optimization/). Each test is an [NP-complete](/np-complete/) homomorphism problem, and the whole task is NP-hard.

## In plain words

A query asks for rows that match a pattern of conditions. Sometimes one condition says nothing new: every row that matches the other conditions also matches it, after you rename some helper variables. You can then delete that condition and the answers stay the same.

The algorithm goes through the conditions one at a time. For each one, it asks: can I send the whole query into the query without this condition, so that each condition lands on a condition that is still there and the output columns stay fixed? If yes, the condition goes. At the end, no condition can go, and no smaller query gives the same answers.

## The problem

We use set semantics: a relation is a set of tuples, and a query returns a set of tuples. A conjunctive query is a rule

$$Q(\bar x) \mathbin{:\!-} R_1(\bar u_1), \ldots, R_k(\bar u_k),$$

where each $\bar u_i$ is a tuple of variables and constants and each variable of the head $\bar x$ occurs in the body. Two queries are *equivalent*, $Q \equiv Q'$, if $Q(D) = Q'(D)$ for every database $D$. A *homomorphism* from $Q$ to $Q'$ is a map $h$ from the variables of $Q$ to the terms of $Q'$, the identity on constants, with $h(\bar x) = \bar x'$ and $h(R_i(\bar u_i))$ an atom of the body of $Q'$ for each $i$. By the [Chandra-Merlin theorem](/chandra-merlin-theorem/), $Q' \subseteq Q$ if and only if there is a homomorphism from $Q$ to $Q'$.

**Input.** A conjunctive query $Q$ with $k$ atoms. **Output.** A conjunctive query $Q' \equiv Q$ with the smallest number of atoms among all conjunctive queries equivalent to $Q$.

For a set $S$ of atoms of $Q$, write $Q_S$ for the query with the head of $Q$ and the body $S$.

## The algorithm

MINIMIZE tries each atom once, in the order of the body. HOM is a backtracking search for a homomorphism, one source atom at a time.

```pseudo id=main
MINIMIZE(Q)
L1  S ← the body of Q
L2  for each atom α of the body of Q, in order
L3      if HOM(Q_S, Q_{S − {α}}) succeeds then
L4          S ← S − {α}                          ▷ α is redundant
L5  return Q_S

HOM(P, P')
L6  h ← the map that sends the head of P to the head of P' (fail on a clash)
    SEARCH(1, h), with α_1, ..., α_n the atoms of P:
L7      if i > n then return h
L8      for each atom β of P' with the relation name of α_i
L9          g ← h extended so that h(α_i) = β (skip β on a clash)
L10         if SEARCH(i + 1, g) succeeds then return its map
L11     fail
```

Line L4 is safe for any α found at line L3. The identity map is a homomorphism from $Q_{S - \{\alpha\}}$ to $Q_S$, so $Q_S \subseteq Q_{S - \{\alpha\}}$, and the map found at line L3 gives the other direction. A head variable is mapped to itself, so it still occurs in $S - \{\alpha\}$, and the query stays safe. If the body has two equal atoms, line L4 deletes one copy.

The code sorts the atoms of $P$ so that atoms with fewer candidates in $P'$ come first, which cuts the search but does not change the answer.

## Example

Take $Q(x, z) \mathbin{:\!-} E(x, y), E(y, z), E(x, w), E(w, z), E(x, u)$. It asks for pairs joined by a path of length two, twice, and for an edge out of $x$.

| atom tried | homomorphism into the rest | result | body after the step |
|---|---|---|---|
| $E(x, y)$ | $y \mapsto w$, $u \mapsto w$ | removed | $E(y, z), E(x, w), E(w, z), E(x, u)$ |
| $E(y, z)$ | $y \mapsto w$ | removed | $E(x, w), E(w, z), E(x, u)$ |
| $E(x, w)$ | $E(x, w)$ must go to $E(x, u)$, then $E(u, z)$ is missing | kept | the same |
| $E(w, z)$ | no atom left of the form $E(\cdot, z)$ | kept | the same |
| $E(x, u)$ | $u \mapsto w$ | removed | $E(x, w), E(w, z)$ |

The result is $Q'(x, z) \mathbin{:\!-} E(x, w), E(w, z)$. It has two atoms, and no conjunctive query with one atom is equivalent, because none of the three atoms can go. Here a different order of the body would keep $E(x, y), E(y, z)$ instead, which is the same query up to the renaming $y \leftrightarrow w$.

The head matters. For $Q(x, y) \mathbin{:\!-} E(x, z), E(y, z)$ nothing can go, since $x$ and $y$ are fixed. The Boolean query $Q() \mathbin{:\!-} E(x, z), E(y, z)$ folds $y$ onto $x$ and keeps one atom.

## Correctness

The proofs are in [the correctness proof](proofs/correctness.md). There are three steps.

- **Each step keeps equivalence.** This is the argument under the pseudocode. So $Q_S \equiv Q$ at each point.
- **At the end, no single atom can be deleted.** Let $\alpha$ be kept when the set was $S_\alpha$, and let $S$ be the final set, so $S \subseteq S_\alpha$. Suppose $g$ is a homomorphism from $Q_S$ to $Q_{S - \{\alpha\}}$. Since $Q_S \equiv Q_{S_\alpha}$, there is a homomorphism $f$ from $Q_{S_\alpha}$ to $Q_S$. Then $g \circ f$ maps $Q_{S_\alpha}$ into $Q_{S - \{\alpha\}}$, whose atoms are all in $S_\alpha - \{\alpha\}$. So the test at line L3 would have succeeded for $\alpha$, a contradiction. One pass is enough.
- **If no single atom can be deleted, the query has the fewest atoms.** Let $Q' \equiv Q_S$ have fewer atoms than $S$. Homomorphisms $f$ from $Q_S$ to $Q'$ and $g$ from $Q'$ to $Q_S$ give the map $g \circ f$ from $Q_S$ to itself, whose image has at most as many atoms as $Q'$. So some atom $\alpha \in S$ is not in the image, and $g \circ f$ is a homomorphism from $Q_S$ to $Q_{S - \{\alpha\}}$.

Chandra and Merlin also showed that two minimal equivalent queries are the same up to a renaming of the variables. This minimal query is the *core* of $Q$.

## Complexity

Let $k$ be the number of atoms of $Q$ and $a$ the largest arity. The bounds are in the [word RAM](/word-ram/) model and are combined complexity: the query is the input, and there is no database.

- **One test (theorem).** HOM visits at most $k$ levels and tries at most $k$ target atoms per level, so its search tree has $O(k^k)$ nodes. Each extension costs $O(a)$ time with a dictionary. That is $O(a k^k)$ time per test.
- **The whole algorithm (theorem).** $k$ tests, so $O(a k^{k+1})$ time in the worst case. The search keeps one map of at most $a k$ variables per level, which is $O(a k^2)$ extra space.
- **Hardness (theorem).** For a graph $G$, let $Q_G$ be the Boolean query with the atoms $E(u, v)$ and $E(v, u)$ for each edge $uv$. Take the Boolean query $Q_{K_3} \wedge Q_G$ on disjoint variables, where $G$ has no loops. If $G$ is [3-colorable](/three-coloring/), the $G$ part maps into the triangle and the core has 6 atoms. If the core has 6 atoms, it is the image of the triangle, so $G$ maps into a triangle and is 3-colorable. So computing the size of the core is NP-hard, and no polynomial algorithm is expected.
- **Polynomial cases (theorem).** For acyclic queries and for queries of bounded query width, containment and minimization take polynomial time (Chekuri and Rajaraman 2000). The homomorphism test is then a [constraint satisfaction problem](/constraint-satisfaction-problem/) with an [acyclic](/acyclic-hypergraph/) or bounded [treewidth](/treewidth/) structure.

Real queries have few atoms, so the exponential bound is rarely a problem in practice. This is a common observation, not a theorem.

## Properties

- **The result is unique up to renaming.** Every order of the atoms gives a query with the same number of atoms, and all of them are isomorphic. The atoms that stay can differ.
- **The result is a subquery.** Its body is a subset of the body of $Q$. No new variables or atoms come in.
- **The result is minimum, not only minimal.** No conjunctive query equivalent to $Q$ has fewer atoms, even one with atoms that are not in $Q$.
- **Constants and head variables are fixed.** A homomorphism can rename only the existential variables.

## Variants and improvements

- **Tableau minimization.** Aho, Sagiv and Ullman (1979) write a select-project-join expression as a tableau, one row per atom, and minimize the tableau by deleting rows. This is the same algorithm. For their class of *simple* tableaux, they gave a polynomial-time method.
- **Minimization under dependencies.** With [functional](/functional-dependency/) or [tuple-generating](/tuple-generating-dependency/) dependencies, first apply the [chase](/chase-algorithm/) to the query, then minimize. Atoms that the dependencies make redundant then also go.
- **Unions of conjunctive queries.** Delete each member that is contained in another member, then minimize each member. The [Sagiv-Yannakakis theorem](/sagiv-yannakakis-theorem/) shows that this gives a smallest equivalent union.
- **Cores in data exchange.** The same retraction step computes the core of a universal solution, an instance with labeled nulls instead of variables. See [data exchange core computation](/data-exchange-core-computation/).
- **Acyclic queries.** Chekuri and Rajaraman replace the backtracking search by a polynomial test when the query is acyclic or has bounded query width.

## When to use it

Use it in an optimizer for queries with set semantics, such as SQL queries with `SELECT DISTINCT`, Datalog rule bodies, and queries over views that a user or a tool has built by combining smaller queries. Generated queries often have redundant joins, and each atom that goes saves one join. Use it also before a containment or equivalence test that you run many times, since the core is a small canonical form.

## Pitfalls

- **Bag semantics.** Under bag semantics, which plain SQL uses, the number of copies of each answer counts. Chaudhuri and Vardi (1993) showed that two conjunctive queries are then equivalent if and only if they are isomorphic, so no atom is redundant, and containment is much harder, with cases that are still open. Do not minimize a query without `DISTINCT` this way.
- **Deleting by a subset test.** An atom is not redundant because its variables occur in other atoms. In $Q(x) \mathbin{:\!-} E(x, y), E(y, x)$ both atoms share all variables, but neither can go. Only a homomorphism into the smaller query is a correct test.
- **Renaming a head variable.** The map must send the head to itself. A search that lets $x \mapsto y$ for a head variable $x$ deletes atoms that are needed.
- **Built-in predicates.** With $\neq$ or $<$ in the body the homomorphism test is no longer correct. Containment of such queries needs other methods.

## Implementations

## History

Chandra and Merlin (1977) defined conjunctive queries, proved the homomorphism criterion for containment, and showed that every conjunctive query has a unique minimal equivalent query, found by deleting atoms. Aho, Sagiv and Ullman (1979) stated the method for tableaux of select-project-join expressions, proved NP-completeness for the general case, and gave polynomial methods for simple tableaux. Chaudhuri and Vardi (1993) showed that the picture changes under bag semantics. Chekuri and Rajaraman (1997, journal version 2000) gave polynomial containment and minimization for acyclic queries and for bounded query width.

## References
