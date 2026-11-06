---
tag: R06GGM
kind: data-structure
slug: calkin-wilf-tree
name: Calkin-Wilf tree
area: number-theory/divisibility-and-gcd
level: advanced
summary: An infinite binary tree containing every positive rational exactly once in lowest terms, with children of a/b being a/(a+b) and (a+b)/b.
model: word-ram
complexity:
  vars: {d: the depth of the node, k: the number of terms of the continued fraction of the node}
  time: {children: O(1), parent: O(1), next: O(1), at: Θ(d), index_of: O(k)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, implicit: true}
history:
  year: 2000
  people: [Neil Calkin, Herbert Wilf]
  note: Recounting the rationals; the values in breadth-first order are Stern's diatomic sequence of 1858.
prereqs: [coprime-integers, euclidean-algorithm, continued-fraction, binary-tree]
see_also: [stern-brocot-tree, farey-sequence, continued-fraction-convergents, reducing-fractions, rational-approximation, binary-heap, fibonacci-numbers, euclidean-algorithm]
sources:
  - paper: "Neil Calkin and Herbert S. Wilf, Recounting the rationals, The American Mathematical Monthly 107(4), 2000"
    locator: pages 360 to 363 (the tree, the proof that each positive rational occurs once in lowest terms, and the breadth-first sequence b(n)/b(n+1))
  - paper: "Moritz A. Stern, Über eine zahlentheoretische Funktion, Journal für die reine und angewandte Mathematik 55, 1858"
    locator: pages 193 to 220 (the diatomic sequence)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition
    locator: Section 4.5, Relative primality (the Stern-Brocot tree and the L and R number system, the companion tree)
  - url: "https://oeis.org/A002487"
    locator: OEIS A002487, Stern's diatomic sequence (fusc), with the Calkin-Wilf and hyperbinary interpretations
  - url: "https://en.wikipedia.org/wiki/Calkin%E2%80%93Wilf_tree"
    locator: Wikipedia, Calkin-Wilf tree (breadth-first sequence, Newman's successor formula, continued fractions and run lengths)
---

The Calkin-Wilf tree is an infinite [binary tree](/binary-tree/) whose nodes are positive fractions: the root is $1/1$, and the node $a/b$ has left child $a/(a + b)$ and right child $(a + b)/b$. Every positive rational number appears in it exactly once, and always in lowest terms. The tree needs no storage, because each operation is a formula on the pair $(a, b)$: going up is one step of the subtractive [Euclidean algorithm](/euclidean-algorithm/), the path from the root spells out the [continued fraction](/continued-fraction/) of $a/b$ in run lengths, and numbering the nodes in breadth-first order, as in a [binary heap](/binary-heap/), gives the bijection $n \mapsto \mathrm{fusc}(n)/\mathrm{fusc}(n + 1)$ between positive integers and positive rationals, where fusc is Stern's diatomic sequence. Newman's formula $x \mapsto 1/(2\lfloor x \rfloor - x + 1)$ steps from each rational to the next one in that order.

## In plain words

Start with the fraction one over one. Every fraction has two children: for the left child, keep the top and replace the bottom by the sum of top and bottom; for the right child, keep the bottom and replace the top by the sum. Growing the tree this way, level by level, lists fractions without end.

Two things make it special. No fraction ever shows up twice, and every positive fraction shows up somewhere, already in lowest terms. To find a fraction's parent, subtract the smaller number from the larger; doing that again and again always ends at one over one, which is the reason every fraction is there. And reading the tree row by row gives a list of all fractions in which each one is a simple formula of the one before it.

## The abstract type

The structure represents the set $\mathbb{Q}_{>0}$ of positive rationals as a rooted binary tree, with these operations on a node $x = a/b$ ($a, b \ge 1$, $\gcd(a, b) = 1$):

- **children$(x)$**: the left child $a/(a + b)$ and the right child $(a + b)/b$.
- **parent$(x)$**: the parent, or none for the root $1/1$.
- **at$(n)$**: the node with breadth-first index $n \ge 1$, where the root is $1$ and the children of node $n$ are $2n$ and $2n + 1$.
- **index_of$(x)$**: the breadth-first index of $x$.
- **next$(x)$**: the node with index $\operatorname{index\_of}(x) + 1$.
- **depth$(x)$**: the level of $x$, with the root at depth $0$.

Every left child is less than $1$ and every right child is greater than $1$, at all levels, so the tree is **not** a search tree, unlike the [Stern-Brocot tree](/stern-brocot-tree/).

## Representation

The tree is **implicit**. A node is just its pair of integers $(a, b)$, and every operation computes its answer from the pair or from the index $n$; nothing is stored and the tree has no size limit. The index $n$ is the path from the root written in binary: the leading digit $1$ stands for the root, then each further digit is $0$ for a step to the left child and $1$ for a step to the right child.

The values along breadth-first order are ratios of consecutive terms of Stern's diatomic sequence, also called fusc after Dijkstra:

$$\mathrm{fusc}(0) = 0, \quad \mathrm{fusc}(1) = 1, \quad \mathrm{fusc}(2m) = \mathrm{fusc}(m), \quad \mathrm{fusc}(2m + 1) = \mathrm{fusc}(m) + \mathrm{fusc}(m + 1),$$

and node $n$ is $\mathrm{fusc}(n)/\mathrm{fusc}(n + 1)$. The sequence begins $0, 1, 1, 2, 1, 3, 2, 3, 1, 4, 3, 5, 2, 5, 3, 4, 1$; each denominator is the next numerator.

**Cost model.** On the [word RAM](/word-ram/) with $a$, $b$ and $n$ in words, each addition, subtraction, comparison, shift and division is one step. The numbers grow along a path: at depth $d$ they can be as large as the Fibonacci number $F_{d+2}$ and the index has $d + 1$ binary digits, so long paths need arbitrary precision, where each step costs time linear in the length of the numbers.

## Operations

```pseudo id=main
CW-CHILDREN(a, b)
L1  return (a, a + b), (a + b, b)            ▷ left, right
CW-PARENT(a, b)
L2  if a = b then return NIL                 ▷ only the root 1/1 has a = b
L3  if a < b then return (a, b − a)          ▷ a/b is a left child
L4  return (a − b, b)                        ▷ a/b is a right child
CW-AT(n)                                     ▷ n ≥ 1
L5  (a, b) ← (1, 1)
L6  for each binary digit c of n after the leading 1, from high to low
L7      if c = 0 then b ← a + b else a ← a + b
L8  return (a, b)
CW-INDEX(a, b)                               ▷ a, b ≥ 1
L9  n ← 0, len ← 0
L10 while a ≠ b
L11     if a > b then q ← ⌈a/b⌉ − 1, a ← a − qb, n ← n + (2^q − 1) · 2^len   ▷ q digits 1
L12     else q ← ⌈b/a⌉ − 1, b ← b − qa                                       ▷ q digits 0
L13     len ← len + q
L14 if a ≠ 1 then error "not in lowest terms"
L15 return n + 2^len                         ▷ prepend the leading 1 of the root
CW-NEXT(a, b)
L16 q ← ⌊a/b⌋
L17 return (b, (2q + 1)b − a)                ▷ Newman: 1/(2⌊x⌋ − x + 1)
```

CW-AT follows the path from the root, one digit at a time. CW-INDEX climbs from the node to the root in runs: while $a > b$ the node is a right child, and $q = \lceil a/b \rceil - 1$ parent steps in a row subtract $b$ each time and remove $q$ low digits $1$ from the index; the case $a < b$ is symmetric with digits $0$. Each run is one division of the [Euclidean algorithm](/euclidean-algorithm/), so the climb ends at $(1, 1)$ exactly when $\gcd(a, b) = 1$, and at $(g, g)$ with $g > 1$ otherwise. CW-NEXT is Newman's formula in integers: $1/(2q - a/b + 1) = b/((2q + 1)b - a)$.

**Continued fractions.** Write $a/b = [a_0; a_1, \ldots, a_k]$ with an odd number of terms, using $[\ldots, a_k] = [\ldots, a_k - 1, 1]$ if needed. Then the index of $a/b$, read from its lowest digit, is

$$\underbrace{1 \cdots 1}_{a_0} \; \underbrace{0 \cdots 0}_{a_1} \; \underbrace{1 \cdots 1}_{a_2} \; \cdots \; \underbrace{1 \cdots 1}_{a_k},$$

so the depth of $a/b$ is $a_0 + a_1 + \cdots + a_k - 1$. In the [Stern-Brocot tree](/stern-brocot-tree/) the same continued fraction is read from the highest digit instead, so the two trees hold the same fractions on each level, permuted by reversing the digits of the index below the leading $1$.

## Example

The first four levels, in breadth-first order with their indices:

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| node | 1/1 | 1/2 | 2/1 | 1/3 | 3/2 | 2/3 | 3/1 | 1/4 | 4/3 | 3/5 | 5/2 | 2/5 | 5/3 | 3/4 | 4/1 |

**CW-AT(10).** $10 = 1010_2$, and the digits after the leading $1$ are $0, 1, 0$: $1/1 \to 1/2 \to 3/2 \to 3/5$. Indeed $\mathrm{fusc}(10)/\mathrm{fusc}(11) = 3/5$.

**CW-INDEX(11, 7).** $11 > 7$: $q = 1$, one digit $1$, and the node becomes $4/7$. $4 < 7$: $q = 1$, one digit $0$, giving $4/3$. $4 > 3$: $q = 1$, one digit $1$, giving $1/3$. $1 < 3$: $q = 2$, two digits $0$, giving $1/1$. The digits from the lowest are $1, 0, 1, 0, 0$, and the leading $1$ gives $100101_2 = 37$. The depth is $5$, and $11/7 = [1; 1, 1, 3] = [1; 1, 1, 2, 1]$, whose terms sum to $6 = 5 + 1$.

**CW-NEXT.** From $3/5$: $q = 0$, so the next node is $5/(1 \cdot 5 - 3) = 5/2$. From the last node of a level, $4/1$: $q = 4$, and the next node is $1/(9 - 4) = 1/5$, the first node of the next level.

**Fibonacci path.** $F_{k+1}/F_k$ has continued fraction $[1; 1, \ldots, 1]$ with $k$ terms, so it lies at depth $k - 1$ and its index has alternating digits below the top: $34/21$ has index $11010101_2$. The path zigzags, and $F_{k+1}$ is the largest numerator at depth $k - 1$.

## Correctness

Node $n$ is $\mathrm{fusc}(n)/\mathrm{fusc}(n + 1)$, by induction on $n$: the root is $1/1$, the left child $2m$ of node $m$ is $\mathrm{fusc}(m)/(\mathrm{fusc}(m) + \mathrm{fusc}(m + 1)) = \mathrm{fusc}(2m)/\mathrm{fusc}(2m + 1)$, and the right child is handled the same way. Each node is in lowest terms, since $\gcd(a, a + b) = \gcd(a + b, b) = \gcd(a, b)$. Every positive reduced $a/b$ occurs: by induction on $a + b$, its parent candidate $(a, b - a)$ or $(a - b, b)$ is reduced with a smaller sum and occurs, and $a/b$ is its child. It occurs only once: a node other than the root has $a \ne b$, the side ($a < b$ for a left child, $a > b$ for a right child) and the parent are determined by $a/b$, and the parent occurs once by induction. CW-AT and CW-INDEX are the path to and from the root, and Newman's formula follows by induction on $n$, comparing the left child of the next parent with the right child of the current one. The full proofs are in the proofs.

## Complexity

| operation | word operations | note |
|---|---|---|
| children, parent | $O(1)$ | one addition or subtraction |
| next | $O(1)$ | one division, Newman's formula |
| at$(n)$ | $\Theta(d)$, $d = \lfloor \lg n \rfloor$ | one addition per digit |
| index_of$(a/b)$ | $O(k)$ | one division per continued fraction term |
| depth$(a/b)$ | $O(k)$ | sum of the terms minus $1$ |

Extra space is $\Theta(1)$ words beyond the numbers themselves. Since $k$ is at most the number of steps of the Euclidean algorithm on $(a, b)$, index_of costs $O(\log \max(a, b))$ divisions, although the index it returns can have up to $\max(a, b)$ binary digits, as for $n/1$ with index $2^n - 1$. With arbitrary precision and numbers of $\beta$ binary digits, at$(n)$ costs $O(d \beta)$ bit operations.

## Variants

- **Stern-Brocot tree.** The [Stern-Brocot tree](/stern-brocot-tree/) has the same levels in bit-reversed order and is a binary search tree for the rationals, so it supports [rational approximation](/rational-approximation/) by searching; the Calkin-Wilf tree supports none, but its breadth-first order is a simple sequence.
- **Including zero and negatives.** Prefixing $0$ and pairing each positive $x$ with $-x$ gives the sequence $0, 1, -1, 1/2, -1/2, 2, -2, \ldots$, a bijection between $\mathbb{N}$ and $\mathbb{Q}$.
- **Hyperbinary representations.** $\mathrm{fusc}(n + 1)$ is the number of ways to write $n$ as a sum of powers of $2$ with each power used at most twice; Calkin and Wilf showed this as well.
- **Stern's array.** Stern's original construction starts from the row $1, 1$ and inserts the sum of each adjacent pair between them, row by row: $1, 2, 1$, then $1, 3, 2, 3, 1$. The numerators of level $d$ of the Calkin-Wilf tree are row $d$ of this array without its last entry.
- **Other enumerations.** The [Farey sequence](/farey-sequence/) lists the fractions in $[0, 1]$ by bounded denominator, and the Cantor pairing lists pairs $(a, b)$ and skips the non-reduced ones; the Calkin-Wilf order needs no skipping and no gcd test.

## When to use it

Use it when a program needs to enumerate the positive rationals without repetition and without gcd computations, for instance to search over all fractions in an order that reaches each one, or to give each positive rational an integer code and decode it again with index_of and at. The index is also a compact bijective coding of rationals as integers. To find the fraction with small denominator nearest to a target, or to search the rationals in order, use the Stern-Brocot tree or [continued fraction convergents](/continued-fraction-convergents/) instead.

## Pitfalls

- **Not a search tree.** Comparing a target with a node does not tell which subtree contains it, because left children are below $1$ and right children above $1$ at every level.
- **Non-reduced input.** $6/4$ is not a node. Climbing with parent steps ends at $2/2$, not $1/1$; without the check of line L14 the code returns the index of $3/2$ for $6/4$ or loops on $2/2$, depending on the implementation.
- **Subtracting one step at a time.** Climbing from $n/1$ with single parent steps takes $n - 1$ steps; use the divisions of line L11 and L12.
- **Large indices.** Fractions with large continued fraction terms have huge indices: $10^6/1$ has an index of $10^6$ binary digits. Fixed-width integers overflow even for small fractions.
- **The last node of a level.** Newman's formula is uniform, but an implementation that computes next by going up to a common ancestor must handle the step from $k/1$ to $1/(k + 1)$, which changes the level.

## Implementations

## History

Moritz Stern studied the diatomic sequence in 1858, in the same paper that introduced what is now the Stern-Brocot tree. Dijkstra later studied it under the name fusc. Neil Calkin and Herbert Wilf published the tree in 2000 in the American Mathematical Monthly, under the title "Recounting the rationals", as a direct proof that the positive rationals are countable, with every rational listed once in lowest terms; they also related the sequence to hyperbinary representations. Moshe Newman found the formula $x \mapsto 1/(2\lfloor x \rfloor - x + 1)$ for the next term of the breadth-first sequence soon after.

## References
