---
tag: 5DMN7F
kind: data-structure
slug: stern-brocot-tree
name: Stern-Brocot tree
aliases:
- Stern-Brocot sequence tree
- Brocot tree
area: number-theory/divisibility-and-gcd
level: advanced
summary: A binary tree enumerating every positive rational exactly once in lowest terms.
model: word-ram
complexity:
  vars: {p: the numerator of a fraction, q: its denominator, r: the number of runs in a path, N: the bound on denominators}
  time: {children: O(1), parent: O(1), encode: O(log(p + q)), decode: O(r), best_approximation: O(log N)}
  space: {per_node: O(1)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [continued-fraction, euclidean-algorithm, coprime-integers]
see_also: [calkin-wilf-tree, farey-sequence, continued-fraction-convergents, binary-search-tree, rational-approximation, reducing-fractions, lames-theorem, christoffel-word]
sources:
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 4.5, Relative Primality (the Stern-Brocot tree, the mediant, the property b c - a d = 1, the L and R number system and the matrices L and R)
  - book: isbn:9780199219865
    title: G. H. Hardy and E. M. Wright, An Introduction to the Theory of Numbers, sixth edition
    locator: Sections 3.1 to 3.4, Farey series (mediants and the property of consecutive fractions)
  - url: "https://cp-algorithms.com/others/stern_brocot_tree_farey_sequences.html"
    locator: sections Stern-Brocot tree, Tree structure, Finding the path to a fraction (the run-length search)
---

The Stern-Brocot tree is an infinite binary search tree whose nodes are the positive rational numbers, each exactly once and in lowest terms. Every node is the **mediant** $(a + c)/(b + d)$ of two fractions $a/b < c/d$, its nearest ancestors on the left and on the right, starting from the bounds $0/1$ and $1/0$ around the root $1/1$. The in-order traversal lists the fractions in increasing order, the path from the root to $p/q$ is spelled by the [continued fraction](/continued-fraction/) of $p/q$, and the nodes in $(0, 1)$ with denominator at most $N$ are the inner terms of the [Farey sequence](/farey-sequence/) of order $N$. The tree is never stored: a node is the pair of its bounds, and a path is a short list of runs, so navigation and the search for the best rational approximation with bounded denominator take a logarithmic number of arithmetic operations.

## In plain words

Start with the two fractions zero over one and one over zero, which stands for infinity. Between two neighbors, put the fraction whose top is the sum of their tops and whose bottom is the sum of their bottoms. Between zero and infinity this gives one over one, the root. Repeat between every pair of neighbors, again and again. Every positive fraction appears exactly once, already in lowest terms, and the fractions stay in increasing order from left to right. To find a fraction, walk down from the root, going left when the target is smaller and right when it is larger. Long walks in one direction can be taken in a single jump.

## The abstract type

The tree is an implicit, read-only binary search tree on the positive rationals $\mathbb{Q}_{>0}$, ordered by value.

- **root**: the node $1/1$.
- **left(x)**, **right(x)**: the two children of $x$; every node has both.
- **parent(x)**: the parent of $x$, or none for the root.
- **value(x)**: the fraction at $x$, in lowest terms.
- **encode(p, q)**: the path from the root to the node with value $p/q$, as a word in $L$ and $R$; $p/q$ need not be in lowest terms.
- **decode(path)**: the node at the end of a path.
- **best_approximation(x, N)**: the fraction with denominator at most $N$ that is closest to a given real $x \ge 0$; here $x = u/v$ is a rational given exactly.

Zero, negative numbers and $1/0$ are not nodes: encode rejects $p \le 0$ or $q \le 0$, and best_approximation rejects $x < 0$. For $x \le 0$ one uses the symmetry $x \mapsto -x$, and the fraction $0/1$ is a valid answer of best_approximation.

## Representation

A node is stored as its **bounds**, four integers $(a, b, c, d)$ with $a/b < c/d$ and $bc - ad = 1$, and its value is the mediant $(a + c)/(b + d)$. The bounds are the nearest ancestor on the left and on the right, or the sentinels $0/1$ and $1/0$, so the root is $(0, 1, 1, 0)$. Then

- the left child is $(a, b, a + c, b + d)$, and the right child is $(a + c, b + d, c, d)$;
- the parent is obtained by undoing the last step, from the bound that was created last, which is the one with the larger sum of numerator and denominator.

A path is stored **run-length encoded**, as a list of runs $(R, k_0), (L, k_1), (R, k_2), \ldots$ of alternating directions with $k_i \ge 1$ (the first run may be an $L$ run). This matters because the depth can be huge: $n/1$ is at depth $n - 1$, on the path $R^{n-1}$. Going down $k$ times in the same direction is one update, $(a, b) \leftarrow (a + kc, b + kd)$ for $R^k$ and $(c, d) \leftarrow (c + ka, d + kb)$ for $L^k$. In matrix form, following Concrete Mathematics, the bounds are the columns of $S = \begin{pmatrix} b & d \\ a & c \end{pmatrix}$, denominators on top, which is the identity at the root. A move $L$ multiplies $S$ on the right by $\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$, which replaces the right column by the sum of the columns, and a move $R$ multiplies by $\begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$, which replaces the left column. The tree has no storage of its own.

## Operations

```pseudo id=main
ENCODE(p, q)                                        ▷ p, q ≥ 1; returns runs of L and R
L1  runs ← empty list;  dir ← R
L2  while q ≠ 0 do
L3      k ← ⌊p / q⌋;  (p, q) ← (q, p − k q)          ▷ one step of Euclid
L4      if q = 0 then k ← k − 1                      ▷ the last run stops at the node itself
L5      if k > 0 then append (dir, k) to runs
L6      dir ← the other direction
L7  return runs

DECODE(runs)                                        ▷ returns the bounds of the node
L8  (a, b, c, d) ← (0, 1, 1, 0)
L9  for each (dir, k) in runs do
L10     if dir = R then (a, b) ← (a + k c, b + k d) else (c, d) ← (c + k a, d + k b)
L11 return (a, b, c, d)                             ▷ the node is (a + c)/(b + d)

PARENT(a, b, c, d)
L12 if (a, b, c, d) = (0, 1, 1, 0) then return none            ▷ the root
L13 if a + b > c + d then return (a − c, b − d, c, d) else return (a, b, c − a, d − b)

BEST-APPROXIMATION(u, v, N)                          ▷ x = u/v ≥ 0, v ≥ 1, N ≥ 1
L14 (a, b, c, d) ← (0, 1, 1, 0)
L15 while b + d ≤ N do                               ▷ the node (a + c)/(b + d) is allowed
L16     if u (b + d) = v (a + c) then return (a + c)/(b + d)
L17     if u (b + d) > v (a + c) then k ← largest k with (a + kc)/(b + kd) < x and b + kd ≤ N;  (a, b) ← (a + kc, b + kd)
L18     else k ← largest k with (c + ka)/(d + kb) > x and d + kb ≤ N;  (c, d) ← (c + ka, d + kb)
L19 return the nearer of a/b and c/d to x, and a/b on a tie or if d = 0
```

In line L17 the largest $k$ is $\lfloor (ub - av - 1)/(cv - ud) \rfloor$, capped by $\lfloor (N - b)/d \rfloor$ when $d > 0$; it is at least 1, because the node itself is below $x$ and allowed. Line L18 is symmetric, with $\lfloor (cv - ud - 1)/(ub - av) \rfloor$ capped by $\lfloor (N - d)/b \rfloor$; the first quotient is dropped when $ub = av$, which happens only for $x = 0$. Both are exact integer computations, with no floating point.

ENCODE runs [Euclid's algorithm](/euclidean-algorithm/) on $(p, q)$: the run lengths are the partial quotients $[k_0; k_1, \ldots, k_m]$ of $p/q$, starting with $R$, with the last one decreased by 1, and runs of length 0 are dropped. So the path to $p/q$ is $R^{k_0} L^{k_1} R^{k_2} \cdots$ with $k_m - 1$ in the last place, and the depth of $p/q$ is $k_0 + \cdots + k_m - 1$.

## Example

**The first levels.** The bounds $0/1$ and $1/0$ give the root $1/1$; the next levels are $1/2, 2/1$; then $1/3, 2/3, 3/2, 3/1$; then $1/4, 2/5, 3/5, 3/4, 4/3, 5/3, 5/2, 4/1$. Listing all fractions of the levels up to 3 in order, $1/4, 1/3, 2/5, 1/2, 3/5, 2/3, 3/4, 1/1, \ldots$, any two neighbors $a/b < c/d$ satisfy $bc - ad = 1$; for example $5 \cdot 1 - 2 \cdot 2 = 1$ for $2/5 < 1/2$.

**Encode and decode $5/7$.** Euclid gives $5 = 0 \cdot 7 + 5$, $7 = 1 \cdot 5 + 2$, $5 = 2 \cdot 2 + 1$, $2 = 2 \cdot 1$, so $5/7 = [0; 1, 2, 2]$ and the path is $R^0 L^1 R^2 L^1 = L R R L$.

| move | bounds $(a/b, c/d)$ | node |
| --- | --- | --- |
| start | $(0/1, 1/0)$ | $1/1$ |
| $L$ | $(0/1, 1/1)$ | $1/2$ |
| $R^2$ | $(2/3, 1/1)$ | $3/4$ |
| $L$ | $(2/3, 3/4)$ | $5/7$ |

The $R^2$ row is one update, $(a, b) \leftarrow (0 + 2 \cdot 1, 1 + 2 \cdot 1)$, passing through $1/2 \to 2/3 \to 3/4$ as nodes. The bounds of $5/7$ satisfy $3 \cdot 3 - 2 \cdot 4 = 1$. Its parent is $3/4$: the bound $3/4$ has the larger sum, $7 > 5$, so line L13 returns the bounds $(2, 3, 3 - 2, 4 - 3)$, that is $(2/3, 1/1)$, with value $3/4$. Its children are $7/10$ and $8/11$.

**Best approximation of $\pi$ with denominator at most 100.** With $x = \pi$ given to 30 decimal places:

| node | compare with $x$ | jump | new bounds |
| --- | --- | --- | --- |
| $1/1$ | below | $R^3$ | $(3/1, 1/0)$ |
| $4/1$ | above | $L^7$ | $(3/1, 22/7)$ |
| $25/8$ | below | $R^{14}$, capped by $1 + 14 \cdot 7 = 99 \le 100$ | $(311/99, 22/7)$ |

The next node, $333/106$, has a denominator above 100, so the search stops with $311/99 < \pi < 22/7$. Since $\pi - 311/99 \approx 0.000178$ and $22/7 - \pi \approx 0.00126$, the answer is $311/99$. Without the cap, the third run would have length 15, the third partial quotient of $\pi = [3; 7, 15, 1, 292, \ldots]$. With $N = 1000$ the answer is $355/113$, and with $N = 7$ it is $22/7$.

## Correctness

The full proof is in `proofs/correctness.md`; the main facts are these.

- **Invariant $bc - ad = 1$.** It holds for $(0, 1, 1, 0)$, and each child replaces one bound by the mediant $(a + c, b + d)$, which keeps it: $b(a + c) - a(b + d) = bc - ad$. So $a/b < (a + c)/(b + d) < c/d$, and the value $(a + c)/(b + d)$ is in lowest terms, since $b(a + c) - a(b + d) = 1$ is a Bézout relation for it.
- **Search order.** Every node of the left subtree of a node lies strictly between its left bound and the node, and every node of the right subtree between the node and its right bound. So the tree is a binary search tree, and no value appears twice.
- **Every positive rational appears.** Searching for $p/q$ in lowest terms, the bounds satisfy $bp - aq \ge 1$ and $cq - dp \ge 1$ while $p/q$ is strictly inside. Then $p + q = (c + d)(bp - aq) + (a + b)(cq - dp) \ge a + b + c + d$, using $bc - ad = 1$. Each step increases $a + b + c + d$, so the search reaches $p/q$ after at most $p + q - 2$ steps.
- **ENCODE.** At the root the walk to $x = p/q$ goes right while the value $j + 1$ is below $x$, that is $\lfloor x \rfloor$ times, or $x - 1$ times if $x$ is an integer, where it stops. After that, the rest of the walk is the walk to $1/(x - \lfloor x \rfloor)$ with $L$ and $R$ exchanged. This is Euclid's recursion on $(p, q)$, with the last quotient decreased by 1 because the walk stops at the node.
- **BEST-APPROXIMATION.** The loop keeps $a/b < x < c/d$ (with $x = 0$ allowed on the left), and every jump moves to the farthest node on the same side of $x$ whose denominator is allowed. At the end, $a/b$ and $c/d$ are neighbors in the [Farey sequence](/farey-sequence/) of order $N$: any fraction between them has denominator at least $b + d > N$. So no fraction with denominator at most $N$ lies strictly between them, and the nearest one to $x$ is one of the two.

## Complexity

**Cost model.** With word-sized integers, each arithmetic operation costs one unit, provided the products such as $u(b + d)$ fit in double words. With arbitrary precision, every operation counted below acts on numbers with $O(n)$ bits, where $n$ is the bit length of the inputs, and costs $O(n^2)$ bit operations with schoolbook arithmetic.

| operation | arithmetic operations |
| --- | --- |
| value, left, right, parent | $O(1)$ |
| encode$(p, q)$ | $O(1 + \log \min(p, q))$ divisions, by [Lamé's theorem](/lames-theorem/) |
| decode of $r$ runs | $O(r)$ |
| best_approximation$(u/v, N)$ | $O(\log N)$ iterations, each $O(1)$ |

In best_approximation, the directions of consecutive iterations alternate, because each jump is as long as $x$ allows, and a jump cut short by $N$ is the last one. An $R$ jump adds at least $d$ to $b$, and an $L$ jump adds at least $b$ to $d$, so the denominators grow at least like the Fibonacci numbers, and the loop makes at most $\log_\varphi N + O(1)$ iterations. In our tests the count never exceeded $\log_\varphi N + 2$. The number of runs of a path is at most the number of partial quotients, which is $O(\log \min(p, q) + 1)$, even though the depth can be as large as $p + q - 2$. Each node takes $O(1)$ integers of space.

## Variants

- **Calkin-Wilf tree.** The [Calkin-Wilf tree](/calkin-wilf-tree/) also contains every positive rational once, with children $a/(a + b)$ and $(a + b)/b$. Each level holds the same fractions as the same level of the Stern-Brocot tree, in bit-reversed order, but it is not a search tree.
- **Restriction to $(0, 1)$.** The left subtree of the root has the bounds $0/1$ and $1/1$ and holds exactly the rationals in $(0, 1)$; it is often called the Farey tree, and its nodes with denominator at most $N$ are the inner terms of the Farey sequence of order $N$.
- **Matrix form and the number system.** The path is a word in $L$ and $R$, and the node is the product of the matrices $L$ and $R$ along it. This is the Stern-Brocot number system of Concrete Mathematics, in which an irrational number has an infinite path, for example $e = R^2 L R^2 L R L^4 R L R^6 \cdots$, read from $e = [2; 1, 2, 1, 1, 4, 1, 1, 6, \ldots]$.
- **Lowest common ancestor and ranges.** The lowest common ancestor of two fractions is the end of the longest common prefix of their paths, found run by run. The fraction with the smallest denominator in an open interval $(x, y)$ is the first node of the search that lies strictly between $x$ and $y$, found by walking down, by whole runs, while $x$ and $y$ are on the same side.
- **Stern's diatomic sequence.** Writing all fractions of the levels up to $k$ in order, between $0/1$ and $1/0$, the numerators are the first $2^{k+1} + 1$ terms of Stern's diatomic sequence $0, 1, 1, 2, 1, 3, 2, 3, 1, 4, 3, 5, \ldots$, defined by $s(2n) = s(n)$ and $s(2n + 1) = s(n) + s(n + 1)$.

## When to use it

- **Best rational approximation** with a bound on the denominator, exactly and without floating point, for example to print a measured value as a simple fraction or to choose gear ratios.
- **The simplest fraction in an interval**, the one with the smallest denominator, as in contest problems and in the reconstruction of a fraction from a rounded decimal.
- **Enumerating** all reduced fractions in a range, in order, by an in-order walk with a cutoff on the denominator.
- **Exact walks related to continued fractions**: the path is a readable form of the continued fraction, and the bounds are its convergents and intermediate fractions, as in [continued fraction convergents](/continued-fraction-convergents/).

## Pitfalls

- **Stepping one node at a time.** The depth of $p/q$ is the sum of its partial quotients minus 1, which is $n - 1$ for $n/1$. A search that moves one level per step takes linear time in the value; jump by whole runs.
- **The last run.** The path to $p/q = [k_0; \ldots, k_m]$ ends with $k_m - 1$, not $k_m$. Forgetting the decrement gives a child of the right node. The continued fraction must be in the form with $k_m \ge 2$ (or $p/q$ an integer), which Euclid's algorithm produces.
- **Off-by-one in the jumps.** In line L17 the jump must stop strictly below $x$; the node equal to $x$ is caught by line L16. Using $\lfloor (ub - av)/(cv - ud) \rfloor$ without the $-1$ steps onto $x$ when $x$ is a node, and past it in the next iteration.
- **Floating point.** Comparing $x$ with a mediant in floating point fails for large denominators; compare $u(b + d)$ with $v(a + c)$ exactly.
- **Sentinel $1/0$.** The right bound starts as $1/0$, so $d = 0$ until the first $L$ move: guard the cap $\lfloor (N - b)/d \rfloor$, and never return $1/0$ as an approximation.

## Implementations

## History

Moritz Stern described the tree in 1858 in a paper on a number-theoretic function, now called Stern's diatomic sequence, and Achille Brocot, a French clockmaker, described it independently in 1861 as a method to design gear trains that approximate a given ratio. The mediant construction is older: it underlies the Farey sequence, whose neighbor property Cauchy proved in 1816. Graham, Knuth and Patashnik made the tree and its $L$, $R$ number system widely known in Section 4.5 of Concrete Mathematics.

## References
