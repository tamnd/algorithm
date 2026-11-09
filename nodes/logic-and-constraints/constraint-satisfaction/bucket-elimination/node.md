---
tag: GJ1MVJ
kind: algorithm
slug: bucket-elimination
name: Bucket elimination
aliases:
- Dechter bucket elimination
- variable elimination for CSP
- adaptive consistency
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Eliminates variables one at a time in a fixed order, joining and projecting the constraints in each bucket.
solves: [constraint-satisfaction-problem]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of constraints, d: the largest domain size, w: the induced width of the order}
  time: {worst: O((m + n) d^(w+1))}
  space: {extra: O(n d^w)}
properties: {deterministic: true, exact: true, in_place: false, online: false, recursive: false}
history:
  year: 1987
  people: [Rina Dechter, Judea Pearl]
  note: Dechter and Pearl (1987) gave adaptive consistency, which makes a network backtrack-free along an order in time exponential in its induced width. Dechter (1999) recast it as bucket elimination, one scheme for satisfaction, counting and optimization.
prereqs: [constraint-graph, treewidth, elimination-ordering]
see_also: [variable-elimination, tree-structured-csp, cutset-conditioning, k-consistency, freuder-theorem, tree-decomposition, counting-csp, belief-propagation]
sources:
  - paper: "Rina Dechter, Bucket elimination, a unifying framework for reasoning, Artificial Intelligence 113(1-2), 1999, pages 41 to 85"
    locator: the bucket elimination scheme for constraint satisfaction, counting and optimization, and its bound exponential in the induced width
  - paper: "Rina Dechter and Judea Pearl, Network-based heuristics for constraint-satisfaction problems, Artificial Intelligence 34(1), 1987, pages 1 to 38"
    locator: adaptive consistency, directional consistency and the induced width of an ordered graph
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 4, Directional consistency (adaptive consistency, bucket elimination, induced width and its bounds)
  - paper: doi:10.1145/322290.322292
    title: Eugene C. Freuder, A sufficient condition for backtrack-free search, Journal of the ACM 29(1), 1982
    locator: pages 24 to 32 (width of an ordered graph, the base of the induced width)
  - paper: "Dániel Marx, Can you beat treewidth?, Theory of Computing 6, 2010, pages 85 to 112"
    locator: under the exponential time hypothesis, binary CSP with primal treewidth k has no f(k) n^{o(k / log k)} algorithm
---

Bucket elimination solves a [constraint satisfaction problem](/constraint-satisfaction-problem/) with constraints of any arity by removing the variables one at a time along a fixed order. Each constraint goes into the *bucket* of its latest variable. Going from the last variable to the first, the algorithm joins the constraints in the bucket of a variable and projects that variable out, which gives a new constraint on the remaining variables of the bucket, and puts it into a lower bucket. If no new constraint is empty, a second pass assigns the variables from the first to the last without backtracking. The time is $O((m + n) d^{w^\ast + 1})$ and the space $O(n d^{w^\ast})$, where $w^\ast$ is the induced width of the order. It is Dechter and Pearl's adaptive consistency of 1987, in the form Dechter gave in 1999, and the CSP form of [variable elimination](/variable-elimination/).

## In plain words

Take the unknowns in a fixed order and get rid of them from the last to the first. To get rid of an unknown, collect all the rules that mention it, and write one new rule on its other unknowns: "these values are fine, because the removed unknown still has a value that fits". Then forget the removed unknown. The new rule goes to the latest of its unknowns, which is handled later.

If a new rule allows nothing, the problem has no answer. Otherwise, go forward from the first unknown and give each one a value that fits all the rules in its bucket. The new rules guarantee that a fitting value always exists. The cost depends on how many unknowns a new rule can mention, which is the induced width of the order.

## The problem

The input is a CSP with variables $x_1, \ldots, x_n$ in a given order, domains $D_i$ with $|D_i| \le d$, and $m$ constraints. A constraint is a scope, a tuple of distinct variables, with a relation on it, the set of allowed tuples. The output is a solution or the answer that none exists. The counting form returns the number of solutions.

The *primal graph* has an edge between two variables that share a scope. Along the order, the *induced graph* is built from the last variable to the first: when a variable is reached, its earlier neighbours are joined pairwise. The *induced width* $w^\ast$ of the order is the largest number of earlier neighbours of a variable in the induced graph. The smallest induced width over all orders is the [treewidth](/treewidth/) of the primal graph. Finding it is NP-hard, so orders come from heuristics such as min-degree and min-fill ([elimination ordering](/elimination-ordering/)).

Notation: $n$ variables, $m$ constraints, $d$ the largest domain size, $w = w^\ast$ the induced width of the order. Cost is counted in constraint checks, a test whether a tuple lies in a relation, on the word-RAM with hashing.

## The algorithm

```pseudo id=main
BUCKET-ELIMINATION(D, C, x_1, ..., x_n)
L1  put each constraint into the bucket of the latest variable of its scope
L2  for x = x_n down to x_1 do
L3      U ← the variables of the constraints in bucket(x), other than x
L4      R_U ← {t ∈ ∏_{u ∈ U} D_u : some a ∈ D_x makes (t, x = a) satisfy all of bucket(x)}
L5      if R_U = ∅ then return NONE
L6      if U ≠ ∅ then put R_U into the bucket of the latest variable of U
L7  for x = x_1 to x_n do
L8      x ← the first a ∈ D_x such that the assignment so far with x = a satisfies all of bucket(x)
L9  return the assignment
```

Line L4 is a join of the constraints in the bucket followed by a projection that removes $x$. When $U$ is empty, $R_U$ is either the set with the empty tuple, meaning that $x$ has a value that fits its unary constraints, or empty. Lines L2 to L6 are the *elimination* pass; lines L7 to L9 are the *assignment* pass. Every constraint of the bucket of $x$ mentions only $x$ and earlier variables, and $R_U$ lies in an earlier bucket, so when line L8 reaches $x$ the assignment so far satisfies $R_U$, and some value of $x$ fits.

**Counting.** Replace each relation by a table of counts, 1 for an allowed tuple. Line L4 then sums, over $a \in D_x$, the product of the tables of the bucket, and the empty-scope tables multiply to the number of solutions. This is sum-product variable elimination, and the implementation's `bucket_count` does it.

## Example

Take $x_0, x_1, x_2, x_3$ with domains $\{0, 1, 2\}$, the order $x_0, x_1, x_2, x_3$, and the constraints $x_0 + x_1 = x_2$, $x_2 \ne x_3$ and $x_1 < x_3$. The primal graph has the edges $\{x_0, x_1\}$, $\{x_0, x_2\}$, $\{x_1, x_2\}$, $\{x_2, x_3\}$ and $\{x_1, x_3\}$.

| bucket | constraints in it | $U$ | new constraint $R_U$ | goes to |
|---|---|---|---|---|
| $x_3$ | $x_2 \ne x_3$, $x_1 < x_3$ | $\{x_1, x_2\}$ | $(x_1, x_2) \in \{(0,0), (0,1), (0,2), (1,0), (1,1)\}$ | $x_2$ |
| $x_2$ | $x_0 + x_1 = x_2$, $R(x_1, x_2)$ | $\{x_0, x_1\}$ | $(x_0, x_1) \in \{(0,0), (0,1), (1,0), (2,0)\}$ | $x_1$ |
| $x_1$ | $R(x_0, x_1)$ | $\{x_0\}$ | $x_0 \in \{0, 1, 2\}$ | $x_0$ |
| $x_0$ | $R(x_0)$ | $\emptyset$ | not empty | none |

The bucket of $x_3$ says: $x_3$ has a value greater than $x_1$ and different from $x_2$. That fails for $x_1 = 2$, and for $x_1 = 1$, $x_2 = 2$. In the bucket of $x_2$, a pair $(x_0, x_1)$ needs $x_2 = x_0 + x_1 \le 2$ with $(x_1, x_2)$ allowed by the new constraint. The three pairs with $x_0 + x_1 > 2$ fail, $(0, 2)$ fails because $(2, 2)$ is not allowed, and $(1, 1)$ fails because $(1, 2)$ is not allowed. Four of the nine pairs remain.

The assignment pass gives $x_0 = 0$; $x_1 = 0$, since $(0, 0)$ is allowed; $x_2 = 0 + 0 = 0$, and $(0, 0) \in R(x_1, x_2)$; $x_3 = 1$, the first value with $1 \ne 0$ and $1 > 0$. The solution is $(0, 0, 0, 1)$, found without backtracking. Each new constraint has at most 2 variables, and the induced width of the order is 2. The counting form returns 5, the number of solutions, which brute force confirms.

## Correctness

Let $C_i$ be the constraints in the buckets of $x_1, \ldots, x_i$ just after the bucket of $x_{i+1}$ has been processed, so that $C_n$ is the input. An assignment of $x_1, \ldots, x_{i-1}$ satisfies $C_{i-1}$ exactly when it extends to an assignment of $x_1, \ldots, x_i$ that satisfies $C_i$: the constraints of $C_i$ that do not mention $x_i$ are in $C_{i-1}$, and $R_U$ says exactly that a fitting value of $x_i$ exists. So the solutions of each $C_{i-1}$ are the projections of the solutions of $C_i$, and if line L5 finds an empty $R_U$, the input has no solution. If it never does, the assignment pass picks, for each variable, a value that fits its bucket, which exists because $R_U$ already holds; at the end, all constraints, the input ones included, are satisfied. The full proof is below.

## Complexity

**Scopes.** The variables in the bucket of $x$, other than $x$, are earlier neighbours of $x$ in the induced graph, so $|U| \le w^\ast$. By induction from the last variable: an input constraint in the bucket of $x$ has its other variables among the earlier neighbours of $x$ in the primal graph. A new constraint from the bucket of a later variable $y$ has as scope some earlier neighbours of $y$ in the induced graph, and the induced graph joins these pairwise, so its other variables are earlier neighbours of the latest of them, which is where it is put.

**Time.** Line L4 runs through at most $d^{|U|} \le d^{w^\ast}$ tuples $t$, and for each through at most $d$ values of $x$, and tests each constraint of the bucket. Each bucket gets its input constraints and at most one new constraint from each later bucket. So the total number of constraint tests is $O((m + n) d^{w^\ast + 1})$. The assignment pass makes $O(d)$ tests per constraint. The time is $O((m + n) d^{w^\ast + 1})$, exponential in the induced width and not in $n$.

**Space.** Each new relation has at most $d^{w^\ast}$ tuples, and there are at most $n$ of them, so the extra space is $O(n d^{w^\ast})$. This is the main practical limit: with $d = 10$ and $w^\ast = 8$, one table has $10^8$ tuples.

**Lower bound.** The exponential dependence on the width cannot be removed in general. Marx (2010) showed that, under the exponential time hypothesis, binary CSP with a primal graph of treewidth $k$ has no algorithm with time $f(k) \cdot N^{o(k / \log k)}$ for any function $f$, where $N$ is the input size. So, up to the $\log k$ factor, the exponent of bucket elimination is the right one.

## Properties

- **Exact and complete.** It decides the CSP, and finds a solution when one exists.
- **Backtrack-free.** After the elimination pass, the CSP formed by all the buckets is backtrack-free along the order; this is why Dechter and Pearl called it adaptive consistency. It is strong directional $(w^\ast + 1)$-consistency, adapted to each variable.
- **Order dependent.** The cost depends on the order through $w^\ast$. The answer does not.
- **Not in place.** It adds new constraints and keeps them for the assignment pass.
- **Exponential space.** Unlike search or [cutset conditioning](/cutset-conditioning/), it stores tables of size $d^{w^\ast}$.

## Variants and improvements

- **Counting and optimization.** Replacing "exists" by a sum gives the number of solutions, a step towards [counting CSPs](/counting-csp/). Replacing it by a minimum of summed costs solves weighted CSPs and MAX-CSP. With probabilities, it is [variable elimination](/variable-elimination/) for Bayesian networks.
- **Directional arc and path consistency.** Bounding the scope of new constraints to 1 or 2 variables, and projecting each constraint separately, gives directional arc and path consistency, which are cheap but do not always decide the problem.
- **Trees.** On a forest with a parent-first order, $w^\ast = 1$, each bucket has binary constraints only, and bucket elimination is the [tree-structured CSP algorithm](/tree-structured-csp/).
- **Mini-buckets.** Split a large bucket into parts with at most $i$ variables each and process them separately. This gives a bound or a relaxation in $O(n d^i)$ time and space, not an exact answer.
- **Tree decompositions.** Grouping the buckets gives a [tree decomposition](/tree-decomposition/) of width $w^\ast$, and cluster-tree methods run two passes over it to get, for example, the values of every variable that occur in some solution, all at once.
- **Hybrid with search.** Condition on a set of variables until the rest has small induced width, then eliminate. This is the $w$-cutset scheme between search and elimination.

## When to use it

Use bucket elimination when an order of small induced width exists, say $w^\ast$ up to 10 to 20 for small domains, and the tables fit in memory. It is a natural choice for counting and optimization, where search must visit many solutions. For large or unknown width, use search with propagation, such as [maintaining arc consistency](/maintaining-arc-consistency/), or [cutset conditioning](/cutset-conditioning/), which uses linear space. Compute the induced width of a candidate order before running: it takes polynomial time, with no tables, and predicts the table sizes.

## Pitfalls

- **A bad order.** The induced width depends on the order, and a poor order on a grid can give $w^\ast$ near $n$. Use min-fill or min-degree, and compute $w^\ast$ first.
- **Forgetting unary constraints.** A constraint with one variable goes into that variable's bucket. Treat the domain as a constraint there, or the projection is too large.
- **Putting the new constraint in the wrong bucket.** It must go to the latest variable of its scope; putting it into an earlier bucket breaks the assignment pass.
- **Throwing the buckets away.** The assignment pass needs all the new constraints. If only the answer yes or no is needed, they can be dropped after use.
- **Big counts.** In the counting form, the numbers reach $d^n$. Use big integers or modular counts.

## Implementations

## History

Nonserial dynamic programming, from Bertelè and Brioschi in the early 1970s, eliminated variables in the same way for optimization problems, and Seidel applied it to constraint problems in 1981. Freuder (1982) defined the width of an ordered graph. Dechter and Pearl (1987) introduced adaptive consistency and the induced width, and showed that a CSP can be solved in time exponential in the induced width. Dechter (1999) presented bucket elimination as one framework for constraint satisfaction, propositional satisfiability (where it is directional resolution, a form of the Davis-Putnam procedure), counting, belief updating and optimization.

## References
