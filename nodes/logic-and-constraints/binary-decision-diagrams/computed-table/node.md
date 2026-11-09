---
tag: P4ZDFG
kind: concept
slug: computed-table
name: Computed table
aliases:
- operation cache
- apply cache
- computed cache
- memo cache
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: A cache of previous operation results that keeps apply and ITE from recomputing subproblems.
prereqs: [memoization, hash-table, reduced-ordered-bdd]
see_also: [bdd-apply, ite-operator, bdd-quantification, bdd-compose, hash-consing, memoization, dag-dynamic-programming, complemented-edges]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 4.3 (the table of pairs of vertices already computed in Apply, and the bound on the number of calls that it gives)
  - paper: doi:10.1109/DAC.1990.114826
    title: Karl S. Brace, Richard L. Rudell and Randal E. Bryant, Efficient implementation of a BDD package, Proceedings of the 27th ACM/IEEE Design Automation Conference, 1990, pages 40 to 45
    locator: Section 4.5 (the memory function for ITE), Section 5.2 (standard triples), Section 5.4 (garbage collection removes the entries that name dead nodes) and Section 5.5 (the caching computed table and its measured cost)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the memo cache of the recursive synthesis operations)
---

The computed table of a BDD package is a cache that maps an operation and its argument nodes, such as $(\wedge, f, g)$, to the node of the result. The recursive operations [APPLY](/bdd-apply/) and [ITE](/ite-operator/) look in it before they split on the top variable, so each tuple of nodes is solved at most once, even when the recursion reaches it along exponentially many paths. This is what turns APPLY from a walk over paths into a walk over pairs of nodes, with Bryant's bound of $O(|f| \cdot |g|)$. It is [memoization](/memoization/) of the Shannon recursion, and it is a different table from the unique table, which keeps the store canonical.

## In plain words

A BDD is a diagram in which many routes lead to the same box. An operation on two diagrams works box by box, and without help it would treat the same pair of boxes again for every route that reaches it. The computed table is a notebook. Before the operation works on a pair of boxes, it looks in the notebook. If the answer is there, it takes it and stops. If not, it does the work and writes the answer down. So each pair is done once. The notebook can also forget answers to save space. Then the result is still right, and only some work is done again.

## The idea

**The table.** The computed table maps a key to a node of the store. The key is the operator and the ids of the argument nodes, for example $(\mathrm{op}, f, g)$ for APPLY or $(f, g, h)$ for ITE. A recursive operation looks up its key after the terminal cases and before the split, and stores its result before it returns:

1. if the arguments give a terminal case, return the result;
2. if the computed table holds the key, return the stored node;
3. split on the top variable, recurse on the cofactors, and join the results with MK;
4. store the result under the key, and return it.

**Why it gives the product bound.** The arguments of every call of APPLY$(\circ, f, g)$ are a node reachable from $f$ and a node reachable from $g$. With the table, each such pair does the work of step 3 at most once, so there are at most $|f| \cdot |g|$ such calls and at most $2|f| \cdot |g| + 1$ calls in all. Without it, the calls follow the paths of the two BDDs, and a BDD with $O(n)$ nodes can have $2^n$ paths.

**Correctness does not depend on it.** A stored entry is a correct result, and the store never changes a node, so a hit returns the same node that the recursion would build. A miss only costs time. So the table can be lossy. Brace, Rudell and Bryant (1990) use a hash-based cache: an array of entries indexed by a hash of the key, with no collision chains, where a new entry overwrites the old entry in its slot. This bounds the memory, but the product bound is lost: in the worst case, when all keys hash to one slot, ITE takes exponential time. On their 12 test circuits the cache needed 16% more recursive calls than a full hash table, but the run time grew by only 6%.

**The two tables.** A BDD package has two hash tables with different jobs:

| | unique table | computed table |
|---|---|---|
| key | $(i, l, h)$, a node triple | an operator and argument nodes |
| value | the node with this triple | the result node of the operation |
| needed for | canonicity: one node per function | speed: each subproblem solved once |
| may forget entries | no, only entries of dead nodes | yes, at any time |

The unique table is [hash-consing](/hash-consing/): it must be lossless, because a missing entry makes a second node for the same triple and breaks the [canonicity](/bdd-canonicity/) of the store.

**Raising the hit rate.** Two calls that give the same result should use the same key. ITE puts its arguments into one standard form, for example $\mathrm{ite}(f, f, h) \to \mathrm{ite}(f, 1, h)$ and $f \wedge g \to g \wedge f$ when $g$ has the smaller id. With [complemented edges](/complemented-edges/) the forms $\mathrm{ite}(f, g, h)$, $\mathrm{ite}(\neg f, h, g)$ and $\neg\mathrm{ite}(f, \neg g, \neg h)$ also share one entry. For a commutative operator in APPLY, the arguments can be sorted by id.

**Lifetime.** Entries can stay between top-level calls, so a later operation can reuse earlier results. Brace, Rudell and Bryant measured 17% more recursive steps and 22% more run time when they cleared the table at each top-level call. When the package frees dead nodes, it must also remove every entry that names a freed node, as a key or as a value. Otherwise a later lookup can return a node whose id now belongs to a different function.

## Examples

**AND of two parities.** Let $p$ be the parity of $x_1, \ldots, x_n$, with $2n + 1$ nodes, and $q$ the parity of the odd-indexed variables, with $n + 1$ nodes. In the BDD of $p$, the two nodes at a level $k \geq 2$ are reached by $2^{k-1}$ paths together. These are the numbers of calls of APPLY$(\wedge, p, q)$ without the early stop on controlling values, counted by the tests of [BDD apply](/bdd-apply/):

| $n$ | $\lvert p \rvert$ | $\lvert q \rvert$ | calls with the table | calls without the table |
|---|---|---|---|---|
| 4 | 9 | 5 | 23 | 31 |
| 10 | 21 | 11 | 71 | 2047 |
| 16 | 33 | 17 | 119 | 131071 |

Without the table, the recursion visits every node of the full decision tree, $2^{n+1} - 1$ calls. With it, the count grows linearly in $n$, well below the bound $2|p| \cdot |q| + 1$.

**Normalized keys.** Computing $f \wedge g$ and later $g \wedge f$ with ITE gives the keys $(f, g, 0)$ and $(g, f, 0)$. After the swap rule, both become the key with the smaller id first, so the second call is one lookup. The tests of the [ITE operator](/ite-operator/) check that the second call adds no new calls.

**Keys with more parts.** An operation with more inputs needs them all in the key. For the existential quantification $\exists X\, f$, the key holds $f$ and the set $X$, or an id of the set. For the relational product $\exists X\,(f \wedge g)$ it holds $f$, $g$ and $X$. If the key omits $X$, a result for one set of variables can be returned for another.

## Where it is used

- **[APPLY](/bdd-apply/) and [ITE](/ite-operator/).** The table is the reason for their bounds $O(|f| \cdot |g|)$ and $O(|f| \cdot |g| \cdot |h|)$.
- **[Quantification](/bdd-quantification/), [composition](/bdd-compose/) and restriction.** Each recursive operation keeps entries with its own operator tag, often in one shared cache.
- **Counting and other one-pass computations.** [Satisfy-count](/bdd-satisfy-count/) keeps one value per node. This is the same idea with a key of one node, often in a field of the node or in an array for one pass.
- **Other decision diagrams.** The operations of [zero-suppressed BDDs](/zero-suppressed-bdd/), [algebraic decision diagrams](/algebraic-decision-diagram/) and other [decision diagrams](/decision-diagram/) use the same kind of cache.
- **[Symbolic model checking](/symbolic-model-checking/).** Image computations repeat many subproblems across iterations, and a cache that persists between calls saves this work.

## References
