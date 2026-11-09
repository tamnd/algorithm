---
tag: X6QCE3
kind: algorithm
slug: ite-operator
name: If-then-else (ITE) operator
aliases:
- ITE algorithm
- ite
- if-then-else on BDDs
area: logic-and-constraints/binary-decision-diagrams
level: core
summary: Computes if f then g else h on BDDs and thereby implements all binary and unary operators.
solves: [boolean-equivalence-checking]
model: word-ram
complexity:
  vars: {f: the number of nodes of the BDD of f, g: the number of nodes of the BDD of g, h: the number of nodes of the BDD of h}
  time: {worst: O(f·g·h) expected}
  space: {extra: O(f·g·h)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1990
  people: [Karl S. Brace, Richard L. Rudell, Randal E. Bryant]
  note: Brace, Rudell and Bryant made ITE the one core operation of their BDD package, with a unique table, a computed table, standard triples and complemented edges.
prereqs: [reduced-ordered-bdd, shannon-expansion, cofactor, computed-table]
see_also: [bdd-apply, computed-table, complemented-edges, bdd-compose, reduced-ordered-bdd, bdd-quantification, memoization, hash-consing]
sources:
  - paper: doi:10.1109/DAC.1990.114826
    title: Karl S. Brace, Richard L. Rudell and Randal E. Bryant, Efficient implementation of a BDD package, Proceedings of the 27th ACM/IEEE Design Automation Conference, 1990, pages 40 to 45
    locator: Section 4.2 and Figure 1 (ITE and the two-variable operators as ITE calls), Sections 4.4 to 4.6 (the recursion, the computed table and the ITE algorithm with its bound), Section 5.2 (standard triples) and Section 5.3 (the ite_constant test)
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 4.3 (Apply) and Section 4.5 (Compose, computed with a three-argument form of Apply)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the ternary if-then-else operator on BDDs and its memo cache)
---

The ITE operator computes the [reduced ordered BDD](/reduced-ordered-bdd/) of $\mathrm{ite}(f, g, h) = (f \wedge g) \vee (\neg f \wedge h)$, "if $f$ then $g$ else $h$", from the BDDs of $f$, $g$ and $h$. Every unary and binary Boolean operator is one ITE call, for example $f \wedge g = \mathrm{ite}(f, g, 0)$ and $\neg f = \mathrm{ite}(f, 0, 1)$, so a BDD package can have ITE as its only core operation. It recurses on the [Shannon expansion](/shannon-expansion/) by the top variable of the three arguments, and with a [computed table](/computed-table/) it takes $O(|f| \cdot |g| \cdot |h|)$ expected time. It is the three-argument form of [BDD apply](/bdd-apply/): APPLY handles one operator on two arguments, and ITE handles all operators with one cache.

## In plain words

"If f then g else h" is a switch. Look at the first question. If its answer is yes, take the answer of the second question. If no, take the answer of the third. With yes or no questions, every way of mixing two questions can be written as such a switch: "both" means "if the first, then the second, else no". So one procedure for the switch is enough. The procedure picks the first input in the fixed order that any of the three questions asks about. It solves the problem twice, once with that input set to yes and once with it set to no, and joins the two answers into one box. A table of solved problems stops it from doing the same work twice.

## The problem

**Input:** a store of reduced ordered BDDs with the order $x_1 < \cdots < x_n$, and three nodes $f$, $g$, $h$ of the store.

**Output:** the node of the store for the function $\mathrm{ite}(f, g, h)$. Since the store is canonical, this node is unique, and the result can be compared with any other node by id.

The 16 binary operators, as ITE calls:

| operator | ITE | operator | ITE |
|---|---|---|---|
| $0$ | $0$ | $\neg(f \vee g)$ | $\mathrm{ite}(f, 0, \neg g)$ |
| $f \wedge g$ | $\mathrm{ite}(f, g, 0)$ | $f \leftrightarrow g$ | $\mathrm{ite}(f, g, \neg g)$ |
| $f \wedge \neg g$ | $\mathrm{ite}(f, \neg g, 0)$ | $\neg g$ | $\mathrm{ite}(g, 0, 1)$ |
| $f$ | $f$ | $f \vee \neg g$ | $\mathrm{ite}(f, 1, \neg g)$ |
| $\neg f \wedge g$ | $\mathrm{ite}(f, 0, g)$ | $\neg f$ | $\mathrm{ite}(f, 0, 1)$ |
| $g$ | $g$ | $f \to g$ | $\mathrm{ite}(f, g, 1)$ |
| $f \oplus g$ | $\mathrm{ite}(f, \neg g, g)$ | $\neg(f \wedge g)$ | $\mathrm{ite}(f, \neg g, 1)$ |
| $f \vee g$ | $\mathrm{ite}(f, 1, g)$ | $1$ | $1$ |

The rule behind the table: with $f = 1$, the operator is a function of $g$ alone, one of $0$, $g$, $\neg g$, $1$; this is the second argument. With $f = 0$ it gives the third argument.

## The algorithm

```pseudo id=main
ITE(f, g, h)
L1  if f = 1 then return g
L2  if f = 0 then return h
L3  if g = h then return g
L4  if g = 1 and h = 0 then return f
L5  if g = f then g ← 1; if h = f then h ← 0          ▷ ite(f,f,h) = ite(f,1,h)
L6  if h = 0 and g < f then swap f and g               ▷ f ∧ g = g ∧ f
L7  if g = 1 and h < f then swap f and h               ▷ f ∨ h = h ∨ f
    (if the triple now meets a terminal case, return by lines L1 to L4)
L8  if the computed table holds (f, g, h) then return it
L9  x_i ← the top variable of f, g and h (the smallest index)
L10 t ← ITE(f|x_i=1, g|x_i=1, h|x_i=1)
L11 e ← ITE(f|x_i=0, g|x_i=0, h|x_i=0)
L12 r ← MK(i, e, t)                                    ▷ lo = e, hi = t
L13 store r in the computed table under (f, g, h)
L14 return r
```

The cofactor of an argument by its top variable $x_i$ is its low or high child. The cofactor of an argument whose top variable is below $x_i$ is the argument itself, since it does not depend on $x_i$. So line L10 and line L11 cost $O(1)$ each before the call. MK is the node constructor of the [reduced ordered BDD](/reduced-ordered-bdd/): it returns $e$ when $e = t$, and otherwise the unique node with the triple $(i, e, t)$.

Lines L5 to L7 put equal problems into one form, so they share one cache entry. Brace, Rudell and Bryant call such a fixed form a standard triple. The comparisons $g < f$ and $h < f$ compare node ids, which is one fixed rule; any fixed total order on nodes works.

## Example

Let $f = x_1 \oplus x_2$, $g = x_2 \wedge x_3$ and $h = x_3$, and compute $r = \mathrm{ite}(f, g, h)$. No terminal case applies, and the top variable is $x_1$, which only $f$ tests.

- $t = \mathrm{ite}(\neg x_2, \; x_2 \wedge x_3, \; x_3)$. The top variable is $x_2$. With $x_2 = 1$ the call is $\mathrm{ite}(0, x_3, x_3) = x_3$, and with $x_2 = 0$ it is $\mathrm{ite}(1, 0, x_3) = 0$. So $t = \mathrm{MK}(2, 0, x_3) = x_2 \wedge x_3$.
- $e = \mathrm{ite}(x_2, \; x_2 \wedge x_3, \; x_3)$. With $x_2 = 1$ the call is $\mathrm{ite}(1, x_3, x_3) = x_3$, and with $x_2 = 0$ it is $\mathrm{ite}(0, 0, x_3) = x_3$. MK$(2, x_3, x_3)$ applies the elimination rule and returns $x_3$, so $e = x_3$.
- $r = \mathrm{MK}(1, x_3, x_2 \wedge x_3)$: if $x_1 = 1$ then $x_2 \wedge x_3$, else $x_3$.

A direct check: for $x_1 = 1$ and $x_2 = 0$, $f = 1$ and $r = g = 0$; for $x_1 = 1$ and $x_2 = 1$, $f = 0$ and $r = h = x_3$. Both agree with $x_2 \wedge x_3$. The node $(x_2, 0, x_3)$ is shared with $g$ through the unique table, so the result adds only one node to the store.

## Correctness

The terminal cases are identities of $\mathrm{ite}$, and lines L5 to L7 replace the triple by one with the same value: $\mathrm{ite}(f, f, h) = f \vee h = \mathrm{ite}(f, 1, h)$, $\mathrm{ite}(f, g, f) = f \wedge g = \mathrm{ite}(f, g, 0)$, and AND and OR commute. A cofactor commutes with $\wedge$, $\vee$ and $\neg$, so the cofactor of $\mathrm{ite}(f, g, h)$ by $x_i = b$ is $\mathrm{ite}$ of the three cofactors, which lines L10 and L11 compute by induction. MK joins them by the Shannon expansion, and keeps the store reduced. The induction is on the sum of the levels of the arguments, which grows in each recursive call. The full proof is in [the proof file](proofs/correctness.md).

## Complexity

Every call that misses the cache has as arguments the cofactors $f_\alpha$, $g_\alpha$, $h_\alpha$ of the three inputs by one partial assignment $\alpha$ of a prefix of the variables, up to the swaps and constants of lines L5 to L7. Each $f_\alpha$ is a node of the BDD of $f$, and the same holds for $g$ and $h$. So there are $O(|f| \cdot |g| \cdot |h|)$ calls that miss, each with $O(1)$ expected work besides its two recursive calls, and each call that hits returns in $O(1)$ expected time. The total is $O(|f| \cdot |g| \cdot |h|)$ expected time, and the cache and the new nodes take as much space.

For a binary operator, one argument is a terminal or $\neg g$, whose BDD has the size of $g$. In a package with [complemented edges](/complemented-edges/) $\neg g$ is the node of $g$, and $\mathrm{ite}(f, g, \neg g)$ has only $O(|f| \cdot |g|)$ distinct triples. So ITE gives the bound $O(|f| \cdot |g|)$ of [APPLY](/bdd-apply/) for the binary operators. Without the computed table, the number of calls can grow as $2^n$, since a node can be reached by exponentially many paths.

## Properties

- **Exact and canonical.** The result is the unique node of the function, so it can be compared with any other node in $O(1)$ time.
- **Recursive, with depth at most $n + 1$**, since the top variable moves down one level or more in each call.
- **Persistent.** ITE only adds nodes and never changes existing ones, so all earlier results stay valid.
- **One cache for all operators.** Since all operators are ITE calls, a result computed for $f \wedge g$ can serve a later $\neg f \vee \neg g$ call in a package with complemented edges, after normalization.

## Variants and improvements

- **Standard triples with complemented edges.** With [complemented edges](/complemented-edges/), Brace, Rudell and Bryant also use $\mathrm{ite}(f, g, h) = \mathrm{ite}(\neg f, h, g) = \neg \mathrm{ite}(f, \neg g, \neg h)$, and pick the form in which the first two arguments are regular (not complemented). Then $\mathrm{ite}(f, g, \neg f)$ becomes $\mathrm{ite}(f, g, 1)$, and the equivalent forms of a triple share one cache entry.
- **APPLY.** [Bryant's APPLY](/bdd-apply/) has one operator and two arguments. It has a smaller cache key and gives the $O(|f| \cdot |g|)$ bound directly.
- **Constrain and restrict.** The [generalized cofactors](/generalized-cofactor/) use the same recursion with a care set as the first argument.
- **Composition.** [BDD compose](/bdd-compose/) is $f|_{x_i = g} = \mathrm{ite}(g, f|_{x_i=1}, f|_{x_i=0})$, one ITE after two restrictions.
- **ITE with a constant result test.** A variant, ite_constant in Brace, Rudell and Bryant (1990), only asks whether $\mathrm{ite}(f, g, h)$ is a constant, and stops as soon as two different terminal values appear. It answers implication tests $f \to g$ without building the result.

## When to use it

Use ITE as the core of a BDD package: it gives all 16 binary operators, negation, multiplexers and composition with one recursion and one cache, so the cache is shared between operators. Use a specialized APPLY, or a specialized AND, when one operator dominates, for example the AND of many constraints in model checking, because its cache key is shorter and its terminal cases are stronger, for example $f \wedge 0 = 0$ at once.

## Pitfalls

- **No cache.** Without the computed table the recursion follows paths, not nodes, and can take exponential time on a BDD with few nodes.
- **Normalization that loops.** A swap rule must use a strict order, such as the node id, so that the normalized triple is a fixed point. Two rules that undo each other make ITE call itself forever.
- **Wrong top variable.** The split must use the smallest index among all three arguments. If it splits on the top variable of $f$ only, the cofactor of $g$ by a variable below its top is not a child of $g$.
- **Stale cache entries.** After garbage collection, entries that name freed nodes must be removed, or a later call can return a freed node.
- **The order of $e$ and $t$ in MK.** MK takes the low child first. Swapping $e$ and $t$ gives $\mathrm{ite}(f, h, g)$ in place of $\mathrm{ite}(f, g, h)$ at that node, and the error is easy to miss when $g$ and $h$ are symmetric in a test.

## Implementations

## History

Bryant (1986) gave APPLY for binary operators, and in Section 4.5 he computed composition with a three-argument form of it. Brace, Rudell and Bryant (1990) made the ternary ITE the one core operation of their package. They gave the table of the 16 binary operators as ITE calls, the terminal cases, the standard triples that make equivalent calls share a cache entry, a computed table that is a hash-based cache, and complemented edges. Later packages, such as CUDD, keep ITE but add specialized AND and XOR operations. Knuth (2011, Section 7.1.4) describes the ternary operator on BDDs and its memo cache as a basic tool of BDD synthesis.

## References
