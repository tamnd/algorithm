---
tag: SH4TH9
kind: algorithm
slug: bdd-satisfy-count
name: Counting satisfying assignments on BDDs
aliases:
- BDD model counting
- satcount
- Satisfy-count
- BDD solution counting
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: Counts satisfying assignments in time linear in the BDD size by dynamic programming over nodes.
solves: [model-counting]
model: word-ram
complexity:
  vars: {f: the number of nodes of the BDD of f}
  time: {worst: O(f)}
  space: {extra: O(f)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1986
  people: [Randal E. Bryant]
  note: Bryant listed Satisfy-count among the basic BDD operations, with cost linear in the graph size. His printed formula lacked a -1 in the exponents, an error that Adnan Darwiche reported in 2001.
prereqs: [reduced-ordered-bdd, shannon-expansion]
see_also: [model-counting, reduced-ordered-bdd, ordered-binary-decision-diagram, bdd-apply, zero-suppressed-bdd, sat, boolean-function, memoization]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 4.6 (Satisfy-one with Lemma 3, Satisfy-all, and the Satisfy-count formula), with footnote 10 of the annotated version on the author's web page (the correction by Adnan Darwiche, 2001)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Algorithm C (count solutions of a BDD)
---

Counting the satisfying assignments of a Boolean function $f$ of $n$ variables is #P-complete for formulas, but on an [ordered BDD](/ordered-binary-decision-diagram/) it takes one pass over the nodes. Each node gets the number of models of its function over the variables from its own level down, and a parent combines the numbers of its two children with a factor $2^k$ for the $k$ levels that each edge skips. The cost is $O(|f|)$ arithmetic operations, as Bryant (1986) stated, and the result can have up to $n + 1$ bits.

## In plain words

A diagram asks questions about the inputs, one at a time, and ends at yes or no. We want to know how many of all the possible inputs end at yes. Work from the bottom up. The yes end counts as one way and the no end counts as zero ways. Each question node adds the ways of its two answers. When an arrow jumps over some questions, the diagram does not care about those inputs, so each of them doubles the number of ways. Each node is done once, so the work grows with the size of the diagram, not with the number of possible inputs.

## The problem

**Input:** an ordered BDD with the variable order $x_1 < \cdots < x_n$ and a root node $f$. Node $0$ and node $1$ are the terminals, and an inner node is a triple $(i, l, h)$ that tests $x_i$, with low child $l$ and high child $h$. The level $\mathrm{var}(u)$ of an inner node is $i$, and a terminal has level $n + 1$.

**Output:** $|S_f|$, where $S_f = \{a \in \{0,1\}^n : f(a) = 1\}$ is the set of models of $f$. The count is over all $n$ variables, also the ones that $f$ does not depend on. For counting on formulas and the general problem, see [model counting](/model-counting/).

## The algorithm

```pseudo id=main
SATCOUNT(f)
L1  return COUNT(f) · 2^(var(f) − 1)

COUNT(u)        ▷ with a memo table for one top-level call
L2  if u = 0 then return 0
L3  if u = 1 then return 1
L4  if the memo holds u then return its value
L5  let (i, l, h) be the triple of u
L6  c ← COUNT(l) · 2^(var(l) − i − 1) + COUNT(h) · 2^(var(h) − i − 1)
L7  store c in the memo, and return c
```

COUNT$(u)$ is the number of models of $f_u$ over the variables $x_{\mathrm{var}(u)}, \ldots, x_n$. An edge from level $i$ to level $j$ skips the $j - i - 1$ variables in between, and each of them can take both values, so the count of the child is multiplied by $2^{j-i-1}$. Line L1 does the same for the $\mathrm{var}(f) - 1$ variables above the root. The Python code numbers the variables from $0$, so there the root factor is $2^{\mathrm{var}(f)}$ and a terminal has level $n$.

## Example

Take $n = 3$ and $f = (x_1 \wedge x_2) \vee x_3$. Its reduced BDD has three inner nodes: $c = (3, 0, 1)$, $b = (2, c, 1)$ and $a = (1, c, b)$.

| node | triple | COUNT |
|---|---|---|
| $c$ | $(3, 0, 1)$ | $0 \cdot 2^{0} + 1 \cdot 2^{0} = 1$ |
| $b$ | $(2, c, 1)$ | $1 \cdot 2^{0} + 1 \cdot 2^{1} = 3$ |
| $a$ | $(1, c, b)$ | $1 \cdot 2^{1} + 3 \cdot 2^{0} = 5$ |

The edge from $b$ to the terminal $1$ skips $x_3$, so it counts $2$, and the edge from $a$ to $c$ skips $x_2$, so it counts $2$. The root is at level $1$, so $|S_f| = 5 \cdot 2^0 = 5$. The models are $001, 011, 101, 111$ and $110$ for $x_1 x_2 x_3$.

**Skipped levels at the top.** With $n = 10$, the BDD of $x_{10}$ is one node at level $10$ with COUNT $= 1$, and line L1 multiplies by $2^9$: $512$ models. For $x_1 \wedge x_{10}$, the root $(1, 0, v)$ has COUNT $= 1 \cdot 2^{10 - 1 - 1} = 256$. For $x_4 \vee x_7$ the count is $3 \cdot 2^8 = 768$. The tests check these numbers.

## Correctness

Each node $u$ represents a function $f_u$ that depends only on $x_{\mathrm{var}(u)}, \ldots, x_n$. Split the models of $f_u$ by the value of $x_i$. With $x_i = 0$ the function is $f_l$, which depends only on the variables from level $\mathrm{var}(l)$ on. The variables $x_{i+1}, \ldots, x_{\mathrm{var}(l)-1}$ are free, so this half has $\mathrm{COUNT}(l) \cdot 2^{\mathrm{var}(l) - i - 1}$ models. The case $x_i = 1$ is the same with $h$. Induction from the terminals gives line L6, and the free variables above the root give line L1. The proof uses no reduction rule, so the algorithm is also correct on ordered BDDs that are not reduced. The full proof is in [the proof file](proofs/correctness.md).

## Complexity

**Theorem (Bryant 1986).** SATCOUNT does $O(|f|)$ arithmetic operations, and it uses $O(|f|)$ extra words for the memo and the stack.

*Proof.* Line L7 stores the value of each inner node, so each node passes line L4 without a hit at most once. Each such pass makes two calls, so there are at most $2|f| + 1$ calls, and each does $O(1)$ steps with at most two shifts and one addition. The levels strictly grow along a path, so the recursion depth is at most $n + 1$. $\square$

The counts can reach $2^n$, so the numbers need $n + 1$ bits. If an arithmetic operation on $n$-bit numbers costs $O(n / w)$ word steps, the time is $O(|f| \cdot n / w)$. Bryant states the cost as $O(|G|)$ with the assumption that integer operations take constant time.

## Properties

- **Exact.** The result is an exact integer. The code uses Python integers, which have no fixed size.
- **Linear in the BDD, not in the models.** The number of models can be $2^n$ while the BDD has $O(n)$ nodes. For the parity of $n$ variables the BDD has $2n + 1$ nodes and the count is $2^{n-1}$.
- **No reduction needed.** The algorithm works on any ordered BDD. On a general [binary decision diagram](/binary-decision-diagram/) a path can test a variable twice, so the skip factor has no meaning. There, counting is #P-hard, because every CNF formula has a branching program of linear size.
- **One pass also gives all subcounts.** After the pass, COUNT of each node is known. A sampler or an enumerator can use these values.

## Variants and improvements

- **Bottom-up loop.** The nodes are made children first, so a loop over the node numbers in increasing order fills an array of counts with no recursion. The code has this form as `satcount_bottom_up`.
- **Probability and weighted counting.** Replace the factor $2$ for each variable by the weights $1 - p_i$ and $p_i$. Then COUNT$(u) = (1 - p_i) \cdot \mathrm{COUNT}(l) + p_i \cdot \mathrm{COUNT}(h)$, where a skipped variable contributes the factor $(1 - p_j) + p_j = 1$. The result is the probability that $f = 1$ when each $x_i$ is $1$ with probability $p_i$. The code has this form as `probability`.
- **Satisfy-one.** Bryant (1986) finds one model in $O(n)$ steps: go down from the root, and at each node take a child that is not the terminal $0$. In a reduced BDD every inner node has the terminal $1$ below it (his Lemma 3), so the walk never backtracks more than one step.
- **Satisfy-all.** Bryant (1986) lists all models in $O(n \cdot |S_f|)$ steps by a full search that branches on both values of each skipped variable.
- **Uniform sampling.** With the counts of the children, go down from the root and take the high child with probability equal to its share of the count. Each model then has the same probability.
- **Complemented edges.** In a store with [complemented edges](/complemented-edges/), a complemented edge to a node $u$ at level $k$ counts $2^{n - k + 1} - \mathrm{COUNT}(u)$ over the variables from level $k$ on.
- **ZDDs.** In a [zero-suppressed BDD](/zero-suppressed-bdd/) a skipped variable is $0$ and not free, so the count of a node is just the sum of the counts of its children, with no factor.

## When to use it

Use it to count the models of a function that already has a small BDD, for example the reachable states of a model checker, the solutions of a puzzle that was compiled into a BDD, or the inputs that make a circuit output true. Use the weighted form for probabilities, such as the reliability of a network or the probability of a fault. If the function is a CNF formula and no BDD exists yet, building the BDD can take exponential time and memory, so a model counter that works on the formula can be better; see [model counting](/model-counting/).

## Pitfalls

- **The formula as printed in 1986.** The exponents in Bryant's paper are $\mathrm{var}(l) - i$ and $\mathrm{var}(h) - i$, without the $-1$. With them, each path counts twice for each inner node on it. For $x_n$ the formula gives $2^n$ in place of $2^{n-1}$. The tests compare the two formulas.
- **Forgetting the skipped levels.** A count that just adds the counts of the children, as in a ZDD, is wrong for a BDD whenever an edge skips a level. The factor at the root, for the variables above it, is also easy to forget.
- **Counting over the support only.** The count depends on $n$. The same node has $2^{n - m}$ times more models in a store with $n$ variables than over its own $m$ support variables. State which $n$ the count is for.
- **Integer overflow.** With $n \geq 64$ the counts do not fit in a 64-bit word. Use big integers, or use floating point and accept rounding.
- **A shared memo.** The memo holds counts for one value of $n$. If the store can grow new variables, a memo that is kept between calls must be cleared.

## Implementations

## History

Bryant (1986) listed Satisfy-count among the basic operations on reduced function graphs, next to Satisfy-one and Satisfy-all, with time $O(|G|)$. The formula in the paper omits the $-1$ in the two exponents. In the annotated version on his web page, footnote 10 states that Adnan Darwiche of UCLA observed the error in a private message in 2001, and it gives the corrected formula. Knuth presents the count as Algorithm C in Section 7.1.4 of Volume 4A (2011).

## References
