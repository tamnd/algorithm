---
tag: RV98XJ
kind: algorithm
slug: martelli-montanari-unification
name: Martelli-Montanari unification
aliases:
- Martelli-Montanari algorithm
- union-find unification
area: logic-and-constraints/unification-and-resolution
level: advanced
summary: Transformation-rule unification running in polynomial time with union-find.
solves: [unification-problem]
model: word-ram
complexity:
  vars: {N: the total size of the input equations, n: the number of variables}
  time: {worst: O(N α(N))}
  space: {extra: O(N)}
properties: {deterministic: true, exact: true, online: false, recursive: false, in_place: false}
history:
  year: 1982
  people: [Alberto Martelli, Ugo Montanari]
  note: Martelli and Montanari presented unification as the solving of a set of equations by transformation rules, and gave an efficient algorithm on multiequations, in ACM TOPLAS in 1982.
prereqs: [unification-problem, most-general-unifier, disjoint-set-forest, term-dag]
see_also: [robinson-unification, paterson-wegman-unification, mgu-existence-theorem, occurs-check, union-by-rank, inverse-ackermann-function, cycle-detection]
sources:
  - paper: doi:10.1145/357162.357169
    title: Alberto Martelli and Ugo Montanari, An efficient unification algorithm, ACM Transactions on Programming Languages and Systems 4(2), 1982, pages 258 to 282
    locator: the transformation rules on sets of equations, the multiequation algorithm with its counters and its built-in test for cycles, and the proofs of termination and correctness
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 4.6, Unification by transformation, and Section 4.8, Unification of term graphs
  - paper: "Kevin Knight, Unification: a multidisciplinary survey, ACM Computing Surveys 21(1), 1989, doi:10.1145/62029.62030"
    locator: the sections on Huet's union-find algorithm, the Paterson-Wegman algorithm and the Martelli-Montanari algorithm, and their complexity
  - book: isbn:9780444508133
    title: Franz Baader and Wayne Snyder, Unification Theory, in J. A. Robinson and A. Voronkov (editors), Handbook of Automated Reasoning, Elsevier and MIT Press, 2001
    locator: Volume I, Chapter 8, Section 2 (rule-based syntactic unification and its efficient implementation with term DAGs)
---

The Martelli-Montanari algorithm solves the [unification problem](/unification-problem/) by rewriting a set of equations with six rules (delete, decompose, clash, orient, occurs check and eliminate) until the set is in solved form or a rule reports failure. The solved form is an [idempotent](/idempotent-substitution/) [most general unifier](/most-general-unifier/). Alberto Martelli and Ugo Montanari published it in 1982, together with an efficient version on multiequations that finds cycles without a separate occurs check. On a [term DAG](/term-dag/) with a [disjoint-set forest](/disjoint-set-forest/), the same rules run in $O(N\,\alpha(N))$ time, almost linear in the input size $N$. The rule form is now the standard textbook presentation of unification.

## In plain words

Write the problem as a list of equations between patterns with blanks. Then apply simple moves until no move applies. If both sides of an equation are the same, drop it. If both sides start with the same symbol, replace the equation by equations between their parts. If they start with different symbols, there is no solution. If a blank equals a pattern, check that the pattern does not contain that blank, then put the pattern for the blank everywhere else and set the equation aside as solved.

Each move either removes a blank for good or makes the list smaller, so the process stops. The equations set aside are the answer. A fast version keeps every pattern once in a shared graph, and groups the parts that must be equal into classes, so that no pattern is ever copied.

## The problem

The input is a finite set of equations $E_0 = \{s_1 \doteq t_1, \ldots, s_m \doteq t_m\}$ between first-order terms. Notation: $N$ is the total number of symbol occurrences in $E_0$, $n$ is the number of distinct variables, $\sigma, \theta$ are substitutions, $t\sigma$ is the application of $\sigma$ to $t$, and $\sigma\theta$ means "first $\sigma$, then $\theta$". The output is an idempotent most general unifier of $E_0$, or FAIL when $E_0$ has no unifier.

A set of equations is in **solved form** when it is $\{x_1 \doteq t_1, \ldots, x_k \doteq t_k\}$ with distinct variables $x_i$, none of which occurs in any $t_j$. A solved form is the idempotent substitution $\{x_1 \mapsto t_1, \ldots, x_k \mapsto t_k\}$.

## The algorithm

The algorithm keeps a set $P$ of unsolved equations and a solved part $S$, an idempotent substitution. Each pass removes one equation from $P$ and applies the first rule that fits.

```pseudo id=main
MARTELLI-MONTANARI(E₀)                  ▷ an idempotent mgu of E₀, or FAIL
L1  S ← ε, P ← E₀
L2  while P ≠ ∅ do
L3      remove an equation s ≐ t from P
L4      if s = t then continue                                     ▷ delete
L5      if s, t are not variables and their roots or arities differ then return FAIL   ▷ clash
L6      if s = f(s₁,…,sₖ) and t = f(t₁,…,tₖ) then add s₁ ≐ t₁, …, sₖ ≐ tₖ to P; continue   ▷ decompose
L7      if s is not a variable then swap s and t                   ▷ orient
L8      if s occurs in t then return FAIL                          ▷ occurs check
L9      P ← P{s ↦ t}, S ← S{s ↦ t}                               ▷ eliminate
L10 return S
```

After line L7, $s$ is a variable $x$ and $t \ne x$. Line L9 applies $\{x \mapsto t\}$ to all of $P$ and composes it onto $S$, so $x$ disappears from $P$ for good. The correctness proof does not depend on which equation line L3 picks.

**The efficient form.** Applying a binding to all of $P$ copies terms, and on trees this can cost exponential time, as in [Robinson's algorithm](/robinson-unification/). The efficient form never copies. It keeps all terms once in a [term DAG](/term-dag/), and it keeps the equations as an equivalence relation on DAG nodes:

1. Build one DAG for all terms, with each variable as one node. Put each node in its own class of a disjoint-set forest. A class keeps at most one function node as its **schema**.
2. Keep a list of node pairs to merge, initially the pairs $(s_i, t_i)$.
3. For each pair, find the two class roots. If they are the same, skip it (delete). If both classes have schemas with different symbols or arities, return FAIL (clash). If both have schemas $f(a_1, \ldots, a_k)$ and $f(b_1, \ldots, b_k)$, add the pairs $(a_i, b_i)$ (decompose), and keep one schema. Then union the two classes (eliminate, with orient implicit).
4. When the list is empty, make the graph of classes: an edge from a class to the class of each child of its schema. If this graph has a cycle, return FAIL (occurs check). Else return the classes: each variable is bound to its class, which stands for the schema of the class or a chosen variable.

This is Huet's union-find algorithm of 1976, and it is the rule system run on shared terms. Martelli and Montanari's own algorithm keeps **multiequations** $\{x_1, \ldots, x_j\} = (t_1, \ldots, t_l)$, a set of variables that are equal to a multiset of terms. It keeps a counter of how often the variables of each multiequation occur in other multiequations. It always solves a multiequation whose counter is zero, so it finds a cycle exactly when no such multiequation is left, and it needs no separate occurs check.

## Example

Solve $E_0 = \{g(x_2) \doteq x_1,\ f(x_1, h(x_1), x_2) \doteq f(g(x_3), x_4, x_3)\}$ with the rules, taking the equations of $P$ in order.

| pass | equation taken | rule | $S$ after the pass |
|---|---|---|---|
| 1 | $g(x_2) \doteq x_1$ | orient, eliminate $x_1 \mapsto g(x_2)$ | $\{x_1 \mapsto g(x_2)\}$ |
| 2 | $f(g(x_2), h(g(x_2)), x_2) \doteq f(g(x_3), x_4, x_3)$ | decompose | same |
| 3 | $g(x_2) \doteq g(x_3)$ | decompose | same |
| 4 | $x_2 \doteq x_3$ | eliminate $x_2 \mapsto x_3$ | $\{x_1 \mapsto g(x_3),\ x_2 \mapsto x_3\}$ |
| 5 | $h(g(x_3)) \doteq x_4$ | orient, eliminate $x_4 \mapsto h(g(x_3))$ | $\{x_1 \mapsto g(x_3),\ x_2 \mapsto x_3,\ x_4 \mapsto h(g(x_3))\}$ |
| 6 | $x_3 \doteq x_3$ | delete | same |

The result is $\{x_1 \mapsto g(x_3),\ x_2 \mapsto x_3,\ x_4 \mapsto h(g(x_3))\}$. In pass 4, the binding $x_2 \mapsto x_3$ also changes the earlier binding of $x_1$ from $g(x_2)$ to $g(x_3)$.

**The same problem with union-find.** The classes end as $\{x_1, g(x_2), g(x_3)\}$, $\{x_2, x_3\}$, $\{x_4, h(x_1)\}$, one class for the two $f$ nodes, and the classes of the pair. No class has two schemas with different symbols, and the graph of classes has no cycle. Naming the class $\{x_2, x_3\}$ by $x_2$ gives $\{x_1 \mapsto g(x_2),\ x_3 \mapsto x_2,\ x_4 \mapsto h(g(x_2))\}$, the same mgu up to the renaming that swaps $x_2$ and $x_3$.

**A cycle.** For $f(x, y) \doteq f(g(y), g(x))$, decomposition merges $x$ with $g(y)$ and $y$ with $g(x)$. No clash occurs, but the class of $x$ has the schema $g(y)$ with a child in the class of $y$, and the class of $y$ has the schema $g(x)$ with a child in the class of $x$. The graph of classes has a cycle, so the result is FAIL.

## Correctness

The proof keeps two invariants at the start of each pass. (J1) A substitution $\theta$ unifies $E_0$ if and only if $\theta = S\theta$ and $\theta$ unifies $P$. (J2) $S$ is idempotent and no variable of its domain occurs in $P$. Delete, decompose and orient do not change the unifiers of $P$. Clash and the occurs check fail only when $P$, and so $E_0$, has no unifier. Eliminate keeps (J1), because a unifier of $x \doteq t$ satisfies $\{x \mapsto t\}\theta = \theta$. The measure (number of variables of $P$, size of $P$) drops in each pass, so the loop ends. At the end $P = \emptyset$, so the unifiers of $E_0$ are exactly the $\theta$ with $\theta = S\theta$, and $S$ is the least of them. The full proof is below.

For the union-find form, the final classes are the least equivalence on DAG nodes that contains the input pairs and is closed under decomposition. A unifier must identify every pair in one class, so a clash or a cycle means that no unifier exists. Otherwise the classes, read as a substitution, form a solved form.

## Complexity

- **Rules on trees.** Line L9 copies $t$ into every occurrence of $x$. On the input $f(x_1, \ldots, x_n) \doteq f(g(x_0, x_0), \ldots, g(x_{n-1}, x_{n-1}))$ the solved form has size $2^{n+2} - n - 4$, so the time is exponential, as for Robinson's algorithm.
- **Union-find form.** The DAG has at most $N$ nodes. There are at most $N$ unions, since each union joins two classes. Each schema is dropped at most once, so the decompositions add at most $N$ pairs in total. Each pair costs two finds. With [union by rank](/union-by-rank/) and path compression, $O(N)$ operations take $O(N\,\alpha(N))$ time, where $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). The cycle test is one depth-first search over the classes, in $O(N)$ time. Building the DAG with a hash table takes $O(N)$ expected time. The total is $O(N\,\alpha(N))$, and the space is $O(N)$.
- **Output.** The mgu is returned as the classes on the DAG. Writing it out as trees can cost exponential space, which the implementation below does only at the end.
- **The multiequation algorithm.** Martelli and Montanari's own version is also close to linear. It avoids copying through multiequations and finds cycles with counters.

## Properties

- **Order-independent.** Any order of the rules gives a correct answer. Different orders give mgus that differ by a renaming.
- **Idempotent output.** The solved form is idempotent, and it uses only variables of the input.
- **Systems of equations.** The input is a set of equations, so no pairing under a new symbol is needed.
- **Late occurs check.** The union-find form runs the occurs check once, at the end, as a cycle test. Without that last step, it solves unification over rational trees.

## Variants and improvements

- **Huet's union-find algorithm (1976).** The union-find form above, from Huet's thesis. It is almost linear, and it was the first algorithm of that speed for unification over rational trees.
- **Paterson and Wegman (1978).** The [Paterson-Wegman algorithm](/paterson-wegman-unification/) processes the classes in an order that detects cycles during the search, and it runs in $O(N)$ time.
- **Rational trees.** Drop the cycle test of step 4, as in Prolog II. The answer is then a system of equations that can be cyclic.
- **Equational unification.** Rule-based algorithms for [equational unification](/equational-unification/) add rules for the theory. For example, [Stickel's algorithm](/stickel-ac-unification/) replaces decomposition for an associative-commutative symbol by the solution of a linear Diophantine system.
- **Higher-order and nominal unification.** [Huet's pre-unification](/huet-pre-unification/) and [Urban's nominal unification](/urban-nominal-unification/) are also stated as transformation rules in this style.

## When to use it

Use the rule form to explain or prove unification, and to extend it to a new theory. Use the union-find form when terms are large or shared, when the input may be adversarial, or when the problem is a big system of equations, as in type inference for large programs. For small terms, as in most clause heads, a recursive Robinson-style algorithm with lazy bindings is simpler and often just as fast.

## Pitfalls

- **Orient without eliminate.** Rule systems that state orient as a separate rule must not swap two variables back and forth; orient applies only when the left side is not a variable.
- **Forgetting to apply the binding to $S$.** In line L9, earlier bindings in $S$ must also get $\{x \mapsto t\}$. Otherwise $S$ is not idempotent and need not unify.
- **Forgetting the cycle test.** The union-find form without step 4 accepts $x \doteq f(x)$. The result is unsound for finite terms. See [occurs check](/occurs-check/).
- **Keeping two schemas.** When two classes with schemas merge, only one schema is kept, but their arguments must be paired first. Dropping the decomposition gives wrong answers.
- **Union without rank or compression.** Plain unions can make finds take linear time, and the total quadratic.

## Implementations

## History

Alberto Martelli and Ugo Montanari published "An efficient unification algorithm" in ACM TOPLAS in 1982. They described unification as solving a set of equations by transformations, proved that the transformations terminate and give a most general unifier, and gave an efficient algorithm on multiequations. Similar rules appear in Herbrand's thesis of 1930. Huet's thesis of 1976 gave the almost linear union-find algorithm, and Paterson and Wegman gave a linear algorithm in 1978.

## References
