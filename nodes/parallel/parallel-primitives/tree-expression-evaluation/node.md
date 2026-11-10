---
tag: D1DXVT
kind: problem
slug: tree-expression-evaluation
name: Tree expression evaluation
aliases:
- arithmetic expression tree evaluation
area: parallel/parallel-primitives
level: advanced
summary: Compute the value of an arithmetic expression given as a tree. Tree contraction with a linear function on each edge does it in O(log n) time and O(n) work, for any shape of tree.
prereqs: [expression-tree, binary-tree, tree-contraction, work-span-model]
see_also: [tree-contraction, expression-tree, euler-tour-technique, list-ranking, list-contraction, brent-theorem, crew-pram, erew-pram]
sources:
  - paper: doi:10.1145/321812.321815
    title: Richard P. Brent, The parallel evaluation of general arithmetic expressions, Journal of the ACM 21(2), 1974
    locator: pp. 201 to 206 (an expression with n variables and constants and the operators +, x and / can be evaluated in time 4 log2 n + 10(n - 1)/p with p processors)
  - paper: doi:10.1109/SFCS.1985.43
    title: Gary L. Miller and John H. Reif, Parallel tree contraction and its application, 26th Annual Symposium on Foundations of Computer Science (FOCS), 1985
    locator: pp. 478 to 489 (expression evaluation by RAKE and COMPRESS in O(log n) time)
  - paper: "Karl Abrahamson, Norm Dadoun, David G. Kirkpatrick and Teresa Przytycka, A simple parallel tree contraction algorithm, Journal of Algorithms 10(2), 1989"
    title: A simple parallel tree contraction algorithm
    locator: pp. 287 to 302 (the shunt of odd-numbered leaves; O(log n) time with n / log n processors on the EREW PRAM)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 3, Section 3.3 (tree contraction and the evaluation of arithmetic expressions with linear functions on the edges)
  - paper: "Samuel R. Buss, The Boolean formula value problem is in ALOGTIME, 19th Annual ACM Symposium on Theory of Computing (STOC), 1987"
    title: The Boolean formula value problem is in ALOGTIME
    locator: pp. 123 to 131 (Boolean formulas are evaluated in logarithmic time on an alternating machine, so the problem is in NC1)
---

Tree expression evaluation asks for the value of an arithmetic expression that is given as an [expression tree](/expression-tree/): the leaves hold numbers and the internal nodes hold operators. A sequential postorder walk takes $\Theta(n)$ time. Evaluating the two subtrees of each node in parallel takes span equal to the height, which is $n/2$ for an expression such as $((x_1 + x_2) + x_3) + \cdots$. [Tree contraction](/tree-contraction/) removes the dependence on the shape: with a linear function $x \mapsto ax + b$ on each edge, it evaluates any expression with $+$, $-$ and $\times$ in $O(\log n)$ time and $O(n)$ work on the [EREW PRAM](/erew-pram/). Brent (1974) first showed that each expression can be evaluated in $O(\log n)$ parallel time.

Notation on this page: $n$ is the number of nodes, $\ell$ the number of leaves (so $n = 2\ell - 1$ for a full binary tree), $p$ the number of processors, $W$ the work and $S$ the span or parallel time. $\lg$ is $\log_2$.

## In plain words

A long sum is written as a tree: each operator sits above its two parts. To get the value, a part must wait for the values of its two smaller parts. If the tree is a long thin chain, the parts wait one after another, and many workers do not help.

The trick is to stop waiting for numbers. When one side of an operator is known and the other side is not, the worker writes down a rule such as "take the unknown value, triple it, and add six". Such a rule is small, and two rules in a row make one rule of the same kind. So the workers can cut many leaves out of the tree in each round and keep the rules on the links. Half the leaves go in each round.

## Definition

**Input.** A rooted full binary tree with nodes $0, \ldots, n - 1$. Each leaf $v$ holds a number $x_v$ from a commutative ring, for example the integers or the rationals. Each internal node $v$ holds an operator $op_v \in \{+, -, \times\}$ and has a left child and a right child. The tree is given by arrays $left$, $right$ and $op$, or by parent pointers and a side bit.

**Output.** The value $\mathrm{val}(\mathit{root})$, where $\mathrm{val}(v) = x_v$ at a leaf and $\mathrm{val}(v) = \mathrm{val}(left[v]) \; op_v \; \mathrm{val}(right[v])$ at an internal node.

The model is the PRAM or the [work-span model](/work-span-model/), and each arithmetic operation counts as one step. The sizes of the numbers are not counted; with integers they can grow to about $n$ times the size of the inputs.

## Variants

- **All subexpressions.** Compute $\mathrm{val}(v)$ for each node $v$, not only for the root. Tree contraction does it with one more pass that puts the removed nodes back in the reverse order.
- **Division.** With $/$ the functions on the edges become $x \mapsto (ax + b)/(cx + d)$. These are closed under composition too, so the same method works over a field (Brent 1974 allows division).
- **Semirings.** Over a commutative semiring, such as $(\max, +)$ or $(\vee, \wedge)$, the functions $x \mapsto a \otimes x \oplus b$ are closed under composition, because $\otimes$ distributes over $\oplus$. This gives the evaluation of Boolean formulas and of many dynamic programs on trees.
- **Boolean formula value problem.** The leaves are 0 or 1 and the operators are $\wedge$, $\vee$ and $\neg$. Buss (1987) showed that it is in ALOGTIME, so in $\mathrm{NC}^1$.
- **Arithmetic circuits.** If a node can feed several operators, the input is a directed acyclic graph, not a tree. The tree methods then do not apply directly, and the problem is harder.

## Examples

Take $((1 + 2) \times 3) + (4 \times (5 - 6)) = 9 + (-4) = 5$. The leaves from left to right are $1, 2, 3, 4, 5, 6$ with the numbers $0$ to $5$. Each round of the shunt (see below) rakes the leaves with odd numbers: first those that are left children, then those that are right children. A rake of a leaf $u$ with parent $p$ and sibling $s$ removes $u$ and $p$, puts $s$ in the place of $p$, and gives $s$ the function $g_p(c \; op_p \; g_s(\cdot))$, where $c$ is the value that $u$ sends up. The edge functions start as $x$.

| round | step | leaf raked | parent | new function on the sibling | the tree after the step |
|---|---|---|---|---|---|
| 1 | left children | 4 | $4 \times (\cdot)$ | $(5 - 6)$ part gets $4x$ | $((1 + 2) \times 3) + 4 \cdot (5 - 6)$ |
| 1 | right children | 2 | $(\cdot) + 2$ | leaf 1 gets $x + 2$ | $((1)_{x+2} \times 3) + 4 \cdot (5 - 6)$ |
| 1 | right children | 6 | $(\cdot) - 6$ | leaf 5 gets $4(x - 6) = 4x - 24$ | $((1)_{x+2} \times 3) + (5)_{4x - 24}$ |
| 2 | right children | 3 | $(\cdot) \times 3$ | leaf 1 gets $3(x + 2) = 3x + 6$ | $(1)_{3x+6} + (5)_{4x-24}$ |
| 3 | right children | 5 | $(\cdot) + c$, $c = 4 \cdot 5 - 24 = -4$ | leaf 1 gets $3x + 6 - 4 = 3x + 2$ | $(1)_{3x+2}$ |

In round 1 the leaves $1, 3, 5$ stay; in round 2 they have the numbers $0, 1, 2$, and only leaf 3 is odd; in round 3 only leaf 5 is odd. After $\lceil \lg 6 \rceil = 3$ rounds one leaf is left, and the value is $3 \cdot 1 + 2 = 5$. The two rakes of round 1 that are right children run at the same time, because they touch different nodes.

## Known algorithms

| algorithm | model | time | work | notes |
|---|---|---|---|---|
| postorder walk | RAM | $\Theta(n)$ | $\Theta(n)$ | with an explicit stack for deep trees |
| parallel recursion on the subtrees | work-span | span $\Theta(\text{height})$ | $\Theta(n)$ | span up to $\Theta(n)$ on a thin tree |
| Brent 1974, restructure the expression | PRAM | $4 \lg n + 10(n - 1)/p$ | $O(n)$ | the time is for the evaluation of the restructured expression |
| Miller and Reif 1985, randomized | PRAM | $O(\log n)$ expected | $O(n)$ | $n / \log n$ processors |
| Miller and Reif 1985, deterministic | PRAM | $O(\log n)$ | $O(n \log n)$ | $n$ processors |
| shunt, Abrahamson et al. 1989 | EREW PRAM | $O(\log n)$ | $O(n)$ | deterministic; needs the leaves numbered by the [Euler tour technique](/euler-tour-technique/) and [list ranking](/list-ranking/) |

### The linear-function trick

For a node $v$ that is not the current root, let $g_v$ be the function on the edge from $v$ to its parent; at the start each $g_v$ is the identity. Define the value of the current tree by $\mathrm{val}'(v) = x_v$ at a leaf and $\mathrm{val}'(v) = g_{left[v]}(\mathrm{val}'(left[v])) \; op_v \; g_{right[v]}(\mathrm{val}'(right[v]))$ at an internal node.

**Lemma 1 (closure).** If $g(x) = ax + b$ and $c$ is a constant, then $c + g(x)$, $g(x) + c$, $c - g(x)$, $g(x) - c$, $c \cdot g(x)$ and $g(x) \cdot c$ are linear in $x$, and so is the composition of two linear functions.

*Proof.* $c \pm (ax + b) = (\pm a)x + (c \pm b)$, $(ax + b) - c = ax + (b - c)$, and $c(ax + b) = (ca)x + cb$, using that the ring is commutative. For the composition, $a_1(a_2 x + b_2) + b_1 = (a_1 a_2)x + (a_1 b_2 + b_1)$. $\square$

**Lemma 2 (a rake keeps the value).** Let $r$ be the current root and assume that the value of the input is $g_r(\mathrm{val}'(r))$. Rake a leaf $u$ with parent $p$ and sibling $s$: remove $u$ and $p$, put $s$ in the place of $p$, and set $g_s \leftarrow g_p(c \; op_p \; g_s(\cdot))$ with $c = g_u(x_u)$, the operands kept in their order. Then the value of the input is still $g_{r'}(\mathrm{val}'(r'))$ for the new root $r'$.

*Proof.* Before the rake, $g_p(\mathrm{val}'(p)) = g_p(c \; op_p \; g_s(\mathrm{val}'(s)))$, which is the new $g_s(\mathrm{val}'(s))$; the subtree of $s$ does not change, so $\mathrm{val}'(s)$ does not change. So the value that reaches the parent of $p$, or the value of the whole tree if $p$ was the root, is the same, and each node above keeps its $\mathrm{val}'$. By Lemma 1 the new $g_s$ is again of the form $ax + b$, so it takes $O(1)$ space and $O(1)$ time to compute. $\square$

When one leaf is left, it is the root $r$ and the value is $g_r(x_r)$. The trick fails for $x \cdot y$ with two unknowns, which is why a rake only removes a leaf, whose value is known.

### The shunt schedule

Number the leaves $0, \ldots, \ell - 1$ from left to right. In each round, rake the leaves with odd numbers, first those that are left children and then those that are right children; then the even leaves keep their order, and the leaf numbered $2j$ gets the number $j$.

```pseudo id=main
SHUNT-EVALUATE(T)                              ▷ T: a full binary expression tree
L1  for each node v in parallel: g_v ← (a = 1, b = 0)         ▷ the identity x ↦ x
L2  number the leaves 0, 1, …, ℓ − 1 from left to right       ▷ Euler tour and list ranking
L3  while more than one leaf is left do
L4      for each leaf u with an odd number that is a left child, in parallel: RAKE(u)
L5      for each leaf u with an odd number that is a right child, in parallel: RAKE(u)
L6      keep the even leaves in order; the leaf numbered 2j gets the number j
L7  return g_r(x_r) for the last leaf r, which is now the root

RAKE(u)                                        ▷ u: a leaf with parent p and sibling s
L8  c ← g_u(x_u)                               ▷ the value that u sends up
L9  g_s ← g_p(c op_p g_s(·)), with the operands in their order   ▷ linear again, by Lemma 1
L10 put s in the place of p below the parent of p, or make s the root
```

**Lemma 3 (no conflicts).** In one substep, two rakes touch disjoint nodes and disjoint fields.

*Proof.* Let $u$ and $u'$ be raked in the same substep, with parents $p$ and $p'$. Between two odd leaves there is an even leaf, so $u$ and $u'$ are not next to each other in the leaf order. If $p = p'$, then $u$ and $u'$ are the two children of $p$ and are next to each other, which is false. If $p'$ is the parent of $p$, then $u'$ and $p$ are the two children of $p'$; both rakes are of the same side, so if $u'$ is a left child then $p$ is a right child and $u$ is a left child of $p$, and $u$ is the first leaf after $u'$. If $u'$ is a right child, then $p$ is a left child and $u$ is the right child of $p$, and $u'$ is the first leaf after $u$. Both cases contradict the first sentence. The same holds with $p$ and $p'$ swapped, and the sibling of $u$ is not $p'$ or $u'$ for the same reason. So the nodes $u, p$ and the child slot of the parent of $p$ that a rake writes are not touched by another rake of the substep. $\square$

**Lemma 4 (rounds).** After a round, the leaves are exactly the even leaves, in the same order, and the tree is again a full binary tree. So $\ell$ leaves need exactly $\lceil \lg \ell \rceil$ rounds, and the total number of rakes is $\ell - 1$.

*Proof.* A rake removes one leaf and its parent, and the sibling takes the parent's place, so the tree stays full and binary and keeps the other leaves in order. In a round the odd leaves go, which leaves $\lceil \ell / 2 \rceil$ leaves. Starting from $\ell$ and taking $\lceil \cdot / 2 \rceil$ reaches 1 after exactly $\lceil \lg \ell \rceil$ steps. Each rake removes one leaf, and one leaf is left. $\square$

With the leaf array packed in each round, round $r$ costs $O(\lceil \ell / 2^{r} \rceil)$ work, so the work is $O(\ell) = O(n)$. Each round is two substeps of $O(1)$ time, so the time after the leaf numbering is $O(\log n)$. The leaf numbering by the Euler tour and list ranking costs $O(\log n)$ time and $O(n)$ work with the work-efficient list ranking algorithms. In the work-span model with binary forking, each substep is a parallel loop with span $O(\log n)$, and the span is $O(\log^2 n)$.

## Bounds

- **Work.** Each leaf must be read, so $W = \Omega(n)$.
- **Time on the CREW PRAM.** A tree of $+$ nodes over the bits $x_1, \ldots, x_n$ has value greater than 0 exactly when the OR of the bits is 1. The OR of $n$ bits needs $\Omega(\log n)$ time on a CREW PRAM with any number of processors (Cook, Dwork and Reischuk 1986), so expression evaluation needs $\Omega(\log n)$ time there, and the $O(\log n)$ algorithms are optimal in time and work.
- **Depth of an equivalent expression.** Brent (1974) showed that each expression of size $n$ over $+$, $-$, $\times$ and $/$ has an equivalent expression of depth $O(\log n)$. With fan-in 2, depth $\Omega(\log n)$ is needed for an expression that depends on $n$ inputs.

## Reductions

- **To tree contraction.** The method above is [tree contraction](/tree-contraction/) with the RAKE fold of Lemma 2 and the composition of linear functions as the COMPRESS fold.
- **From a list sum.** A sum $x_1 + \cdots + x_n$ stored as a linked list is the expression tree of a left comb. So the evaluation of an expression is at least as hard as one list sum, and the shunt uses [list ranking](/list-ranking/) to number the leaves.
- **Boolean formulas.** The Boolean formula value problem is the special case over the Boolean semiring with negation, which maps the functions $x$, $\neg x$, $0$ and $1$ to each other under composition.

## Applications

- Parallel evaluation of formulas and of expressions in compilers, which motivated Brent (1974).
- Placing problems in $\mathrm{NC}^1$: Boolean formulas, and through tree contraction many problems on trees.
- Dynamic programs on trees, such as the maximum weight [independent set](/independent-set/) of a tree, by the semiring variant.
- [Brent's theorem](/brent-theorem/) on scheduling a computation with work $W$ and depth $D$ on $p$ processors in time $W/p + D$ comes from the same 1974 paper.

## References
