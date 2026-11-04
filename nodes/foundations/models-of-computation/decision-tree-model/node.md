---
tag: F3DC2S
kind: model
slug: decision-tree-model
name: Decision tree model
aliases:
- decision tree
- decision tree complexity
area: foundations/models-of-computation
level: core
summary: Algorithms as trees of queries whose cost is the depth; gives lower bounds such as the sorting bound.
prereqs: [comparison-model, asymptotic-notation, logarithms]
see_also: [information-theoretic-bound, decision-tree-method, adversary-argument, comparison-sort-lower-bound, query-complexity, sensitivity-theorem, algebraic-decision-tree, yao-minimax-principle]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1 (the decision-tree model and Theorem 8.1)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (minimum-comparison sorting, the table of values of S(n))
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 12, Decision trees (certificate complexity, randomized decision trees and Yao's principle)
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43 (sensitivity, block sensitivity, certificate complexity, degree and their relations)
  - paper: doi:10.4007/annals.2019.190.3.6
    title: Hao Huang, Induced subgraphs of hypercubes and a proof of the sensitivity conjecture, Annals of Mathematics 190(3) (2019)
    locator: pp. 949 to 955
  - paper: doi:10.1016/0304-3975(76)90053-0
    title: Ronald L. Rivest and Jean Vuillemin, On recognizing graph properties from adjacency matrices, Theoretical Computer Science 3(3) (1976)
    locator: pp. 371 to 384
  - paper: doi:10.1007/BF02579140
    title: Jeff Kahn, Michael Saks and Dean Sturtevant, A topological approach to evasiveness, Combinatorica 4(4) (1984)
    locator: pp. 297 to 306
  - paper: doi:10.1109/SFCS.1986.44
    title: Michael Saks and Avi Wigderson, Probabilistic Boolean decision trees and the complexity of evaluating game trees, 27th IEEE Symposium on Foundations of Computer Science (FOCS 1986)
    locator: pp. 29 to 38
  - paper: doi:10.1109/SFCS.1977.24
    title: Andrew Chi-Chih Yao, Probabilistic computations, toward a unified measure of complexity, 18th IEEE Symposium on Foundations of Computer Science (FOCS 1977)
    locator: pp. 222 to 227 (the minimax principle)
---

The decision tree model describes an algorithm as a rooted tree. Each inner node asks one query about the input, each branch is one answer, and each leaf gives the output. The cost of the algorithm on an input is the number of queries on the path that the input follows, and the cost of the algorithm is the height of the tree, the largest number of queries on any path. Only queries cost: all other work is free, so a lower bound in this model holds for every algorithm that learns about its input through these queries, however fast its other steps are.

## The machine

Fix a set $X$ of inputs, a set $Y$ of outputs and a function $f : X \to Y$ to compute. Fix a set $Q$ of allowed queries. A **query** is a function $q : X \to A_q$ where $A_q$ is a finite set of answers. In a binary tree, $|A_q| = 2$.

A **decision tree** over $Q$ is a rooted tree with these parts.

- Each inner node $v$ has a query $q_v \in Q$ and, for each answer $a \in A_{q_v}$, at most one child $v_a$.
- Each leaf has a label in $Y$.

The tree **runs** on an input $x \in X$ as follows. It starts at the root. At an inner node $v$ it computes $a = q_v(x)$ and moves to the child $v_a$. At a leaf it outputs the label of the leaf. The tree **computes** $f$ when, for each $x \in X$, the run on $x$ reaches a child that exists and ends with the output $f(x)$.

The tree is a fixed object, not a program with a loop. It is built for one problem size. So the model is non-uniform: an algorithm for all sizes is a family of trees, one for each size.

Three common choices of $Q$:

- **Comparison trees.** The input is a sequence $x_1, \dots, x_n$ of keys, and a query is "$x_i < x_j$?" with two answers, or a three-way comparison of $x_i$ and $x_j$ with answers less, equal and greater. This is the [comparison model](/comparison-model/).
- **Boolean decision trees.** The input is a bit string $x \in \{0,1\}^n$, and a query reads one bit $x_i$.
- **Algebraic trees.** A query asks for the sign of a polynomial of the inputs. See [algebraic decision trees](/algebraic-decision-tree/), [linear decision trees](/linear-decision-tree/) and [algebraic computation trees](/algebraic-computation-tree/).

## What it counts

The **depth** of a leaf is the number of edges from the root to the leaf. The **height** of a tree is the largest depth of a leaf. Let $\mathrm{D}(f)$ be the least height of a decision tree over $Q$ that computes $f$. This is the **worst-case cost** of $f$ in the model: some input needs $\mathrm{D}(f)$ queries, and no algorithm of the model does better on its worst input.

For a probability distribution $\mu$ on $X$, the **average cost** of a tree is $\sum_{x \in X} \mu(x) \cdot \mathrm{depth}(\text{leaf reached by } x)$. A **randomized** algorithm is a probability distribution over trees. Its expected cost on an input is the average over this distribution. The randomized cost of the algorithm is the largest expected cost over all inputs $x \in X$. See the [Yao minimax principle](/yao-minimax-principle/).

For Boolean functions there are two standard randomized costs. $R_0(f)$ is the least randomized cost of an algorithm that is always correct (zero error). $R_2(f)$ is the least randomized cost of an algorithm that is correct with probability at least $2/3$ on each input (bounded error). Then $R_2(f) \le R_0(f) \le \mathrm{D}(f)$. The name *query complexity* is also used for these costs; see [query complexity](/query-complexity/).

The model does not count the size of the tree, the memory, or any work between queries.

## Relation to other models

- The [comparison model](/comparison-model/) is the decision tree model with $Q$ equal to the comparisons of two input keys. A deterministic comparison-based algorithm, such as [merge sort](/merge-sort/), gives one tree for each input size (a randomized one gives a distribution over such trees), and the number of comparisons that it makes on an input is the length of the path of that input.
- A [branching program](/branching-program/) is a decision tree in which different paths can meet again, so it is a directed acyclic graph. A decision tree is a branching program of which the graph is a tree. The graph form can be much smaller.
- The [cell-probe model](/cell-probe-model/) and the [bit-probe model](/bit-probe-model/) are decision trees in which a query reads one cell or one bit of a data structure.
- The model gives only lower bounds that hold for algorithms that use the queries of $Q$. An algorithm with other operations, such as the arithmetic of [counting sort](/counting-sort/) or [radix sort](/radix-sort/), is not a tree over comparisons and can be faster.

## Known results in the model

### The counting lemma

**Lemma 1.** A tree in which each inner node has at most $k$ children and every leaf has depth at most $h$ has at most $k^h$ leaves.

*Proof.* By induction on $h$. If $h = 0$, the tree is a single leaf, and $k^0 = 1$. Let $h \ge 1$ and suppose the claim holds for $h - 1$. The root is an inner node or a leaf. If it is a leaf, the tree has 1 leaf, and $1 \le k^h$ when $k \ge 1$. Otherwise the root has at most $k$ subtrees, and each is a tree of which every leaf has depth at most $h - 1$ in the subtree. By the induction hypothesis each subtree has at most $k^{h-1}$ leaves. So the tree has at most $k \cdot k^{h-1} = k^h$ leaves. ∎

**Corollary 2 (counting bound).** This is the [information-theoretic bound](/information-theoretic-bound/), a [counting argument](/counting-argument/) on the leaves, and it is the base of the [decision tree method](/decision-tree-method/) for lower bounds. Let a decision tree with at most $k$ answers for each query compute $f : X \to Y$. Let $h$ be its height. Then $k^h \ge |f(X)|$, so

$$h \ge \lceil \log_k |f(X)| \rceil.$$

*Proof.* For each $y \in f(X)$ there is an input $x$ with $f(x) = y$. The run on $x$ ends at a leaf with label $y$. So the labels of the leaves cover $f(X)$, and the tree has at least $|f(X)|$ leaves. By Lemma 1 the tree has at most $k^h$ leaves. So $k^h \ge |f(X)|$. Take $\log_k$ on both sides. The height $h$ is an integer, so $h \ge \lceil \log_k |f(X)| \rceil$. ∎

### Sorting

The [sorting problem](/sorting-problem/) asks for the keys in order. Take the inputs to be the $n!$ sequences of $n$ distinct keys, written as permutations of $\{1, \dots, n\}$. The output is the permutation that sorts the input, so the outputs of two different inputs are different. Comparisons of distinct keys have two answers, "less" and "greater", so $k = 2$.

**Theorem 3.** Each comparison tree that sorts $n$ distinct keys has height at least $\lceil \lg(n!) \rceil$. Also $\lg(n!) \ge n \lg n - n \lg e$, so the height is $\Omega(n \log n)$.

*Proof.* The function $f$ maps each input to its sorting permutation, so $|f(X)| = n!$. Corollary 2 with $k = 2$ gives $h \ge \lceil \lg(n!) \rceil$. For the second claim, $e^n = \sum_{j \ge 0} n^j / j! \ge n^n / n!$, because the term $j = n$ is one term of a sum of positive terms. So $n! \ge (n/e)^n$, and $\lg(n!) \ge n \lg n - n \lg e$ with $\lg e \approx 1.4427$. For $n \ge 8$ this is at least $n \lg n - 1.45 n \ge (n \lg n)/2$, because $\lg n \ge 3$ gives $0.5 \lg n \ge 1.5 > 1.45$. ∎

A three-way comparison tree has three children for each node, and the "equal" child is never reached on distinct keys. So removing it leaves a tree with two children, and the same bound holds.

The table shows the bound for small $n$. The last column is the least worst-case number of comparisons of any comparison sort, as Knuth tabulates it in Section 5.3.1.

| $n$ | $n!$ | $\lg(n!)$ | $\lceil \lg(n!) \rceil$ | least worst case |
|---|---|---|---|---|
| 3 | 6 | 2.585 | 3 | 3 |
| 4 | 24 | 4.585 | 5 | 5 |
| 5 | 120 | 6.907 | 7 | 7 |
| 6 | 720 | 9.492 | 10 | 10 |
| 10 | 3628800 | 21.791 | 22 | 22 |
| 12 | 479001600 | 28.835 | 29 | 30 |

The bound is tight for $n \le 11$, and it is not tight for $n = 12$: the count argument only counts leaves and does not say that a tree with $n!$ leaves of nearly equal depth exists. The [Ford and Johnson algorithm](/ford-johnson-algorithm/) reaches the values of the last column. For large $n$ the bound is tight up to the linear term: [merge sort](/merge-sort/) uses at most $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$ comparisons, which is $n \lg n + O(n)$. See the [comparison sort lower bound](/comparison-sort-lower-bound/).

**Example, $n = 3$.** Call the keys $a, b, c$. The tree below sorts them with at most 3 comparisons. Each line is a node. Indentation shows the depth.

```text
a < b ?
  yes: b < c ?
         yes: output a b c
         no:  a < c ?
                yes: output a c b
                no:  output c a b
  no:  b < c ?
         yes: a < c ?
                yes: output b a c
                no:  output b c a
         no:  output c b a
```

The tree has 6 leaves, two at depth 2 and four at depth 3. The height is 3, which is $\lceil \lg 6 \rceil$. No tree of height 2 exists, because a binary tree of height 2 has at most 4 leaves.

### The average depth

**Lemma 4.** A binary tree in which each inner node has exactly two children and that has $L \ge 1$ leaves has leaf depths that add up to at least $L \lg L$.

*Proof.* By strong induction on $L$. For $L = 1$ the tree is one leaf of depth 0, and $1 \cdot \lg 1 = 0$. Let $L \ge 2$. The root has two subtrees with $L_1$ and $L_2$ leaves, where $L_1, L_2 \ge 1$ and $L_1 + L_2 = L$. Each leaf is one level deeper in the whole tree than in its subtree. Let $E(\cdot)$ be the sum of the leaf depths. Then $E = L + E_1 + E_2$. By the induction hypothesis $E \ge L + L_1 \lg L_1 + L_2 \lg L_2$. The function $g(x) = x \lg x$ is convex for $x > 0$, because $g''(x) = 1/(x \ln 2) > 0$. So $g(L_1) + g(L_2) \ge 2 g(L/2) = L \lg(L/2) = L \lg L - L$. Hence $E \ge L + L \lg L - L = L \lg L$. ∎

**Theorem 5.** Let a comparison tree sort $n$ distinct keys. If the input is a uniformly random permutation, the expected number of comparisons is at least $\lg(n!)$.

*Proof.* Each input reaches one leaf. Two different inputs have different sorted outputs, so they reach different leaves. So exactly $n!$ leaves are reached, and each is reached by one input. The average depth is $\frac{1}{n!}$ times the sum of the depths of these leaves. Delete all nodes that no input reaches. Some inner nodes now have one child. Remove each such node and join its parent to its child. This step does not increase the depth of a leaf. The result is a tree with $n!$ leaves in which each inner node has two children. By Lemma 4 its leaf depths add up to at least $n! \lg(n!)$. The depths in the original tree are at least as large. So the average is at least $\lg(n!)$. ∎

Two consequences follow. First, the bound of Theorem 3 holds for the average case too: an average of at least $\lg(n!)$ gives a worst case of at least $\lg(n!)$. Second, it holds for randomized algorithms. A randomized comparison sort is a distribution over trees, each of which sorts. By Theorem 5, on a uniformly random input each tree has an average of at least $\lg(n!)$. So the average over the distribution is at least $\lg(n!)$, and some input has expected cost at least $\lg(n!)$.

### Search in a sorted array

The array $A[1] < A[2] < \dots < A[n]$ is known to be sorted. The order of the array is known, so a comparison of two array entries gives no information. A query compares $x$ with one entry $A[i]$, with the answers less, equal and greater. The algorithm must output an index $i$ with $A[i] = x$, or the word "absent".

**Theorem 6.** Each comparison tree that solves this problem on all inputs has height at least $\lceil \lg(n+1) \rceil$.

*Proof.* Use the array $A[i] = 2i$ and consider the $n$ inputs $x = 2i$. For each $i$, the run on $x = 2i$ passes through a node that compares $x$ with $A[i]$. Suppose not, for some $i$. The run on $x = 2i$ ends at a leaf. This leaf must say "found at $i$". Now take $x' = 2i + 1$. Each comparison on the path is with some $A[j]$ with $j \ne i$, and $x$ and $x'$ give the same answer: both are greater than $A[j]$ for $j < i$, and both are less than $A[j]$ for $j > i$. So the run on $x'$ ends at the same leaf. But $x'$ is not in the array, so the answer is wrong. This is a contradiction.

So there are at least $n$ nodes in the tree, one for each index, and they are different nodes. Let the node for $i$ be the first node on the run for $x = 2i$ that compares $x$ with $A[i]$. Every earlier answer on this run is "less" or "greater", because "equal" can occur only when $x$ is compared with $A[i]$. The nodes that are reached by "less" and "greater" answers only are at most $2^d$ at depth $d$. The $n$ nodes are inner nodes, so their depths are in $0, \dots, h - 1$. Hence $n \le 1 + 2 + \dots + 2^{h-1} = 2^h - 1$ and $h \ge \lg(n+1)$. The height is an integer. ∎

[Binary search](/binary-search/) makes at most $\lfloor \lg n \rfloor + 1 = \lceil \lg(n+1) \rceil$ probes. For $n = 7$ both numbers are 3, and for $n = 8$ both are 4. So the bound is tight for each $n$. See [sorted search lower bound](/sorted-search-lower-bound/) and [search in a sorted array](/search-in-sorted-array/).

### A bound that counting does not give

Counting needs many outputs. The function $f : \{0,1\}^n \to \{0,1\}$ has two outputs, so Corollary 2 gives only $h \ge 1$. For the parity function, a different argument gives a much better bound.

**Theorem 7.** Every Boolean decision tree that computes the parity $x_1 \oplus \dots \oplus x_n$ has height at least $n$, and some tree has height $n$. So $\mathrm{D}(\text{parity}) = n$.

*Proof.* The tree that reads $x_1, \dots, x_n$ in order has height $n$. Now take any tree of height less than $n$. Take a leaf and an input $x$ that reaches it. The path has fewer than $n$ queries, so some index $i$ is not queried on it. Let $x'$ be $x$ with bit $i$ changed. The run on $x'$ gives the same answers to the same queries, so it reaches the same leaf. The two inputs have different parity but the same output. So the tree is wrong. ∎

This is an [adversary argument](/adversary-argument/): the adversary answers each query and keeps one free bit until the end. The same argument shows $\mathrm{D}(\mathrm{OR}_n) = n$: the adversary answers 0 to each query, and while one bit is unread, the output can still be 0 or 1.

### Sensitivity, certificates and degree

Let $f : \{0,1\}^n \to \{0,1\}$. For $x \in \{0,1\}^n$ and a set $S$ of indices, let $x^S$ be $x$ with the bits in $S$ flipped. Four measures bound $\mathrm{D}(f)$ from below.

- The **sensitivity** $s(f)$ is the largest, over $x$, number of indices $i$ with $f(x^{\{i\}}) \ne f(x)$.
- The **block sensitivity** $bs(f)$ is the largest, over $x$, number of pairwise disjoint sets $S_1, \dots, S_k$ with $f(x^{S_j}) \ne f(x)$ for each $j$.
- The **certificate complexity** $C(f)$ is the least $c$ such that each $x$ has a set of at most $c$ indices whose values in $x$ fix $f$: every $y$ that agrees with $x$ on the set has $f(y) = f(x)$. See [certificate complexity](/certificate-complexity/).
- The **degree** $\deg(f)$ is the degree of the unique multilinear real polynomial that equals $f$ on $\{0,1\}^n$. See [polynomial degree](/polynomial-degree/).

**Theorem 8.** For every $f$, $s(f) \le bs(f) \le C(f) \le \mathrm{D}(f)$ and $\deg(f) \le \mathrm{D}(f)$.

*Proof.* A sensitive index $i$ is a block $\{i\}$, so $s(f) \le bs(f)$. Let $S_1, \dots, S_k$ be disjoint sensitive blocks at $x$, and let $T$ be a certificate for $x$. If $T$ misses a block $S_j$, then $x^{S_j}$ agrees with $x$ on $T$, so $f(x^{S_j}) = f(x)$, which is false. So $T$ meets each of the $k$ disjoint blocks, and $|T| \ge k$. This gives $bs(f) \le C(f)$. In a tree of height $\mathrm{D}(f)$, the queries on the path of $x$ form a certificate for $x$, because each $y$ that agrees with $x$ on them follows the same path. This gives $C(f) \le \mathrm{D}(f)$. For the degree, each leaf $\ell$ defines the product $p_\ell(x)$ of the factors $x_i$ (for the answer 1) and $1 - x_i$ (for the answer 0) over the queries on its path. Then $p_\ell(x) = 1$ when $x$ reaches $\ell$ and $0$ otherwise, and $f = \sum_\ell (\text{label of } \ell)\, p_\ell$ is a polynomial of degree at most the height. Replace each $x_i^2$ by $x_i$, which changes no value on $\{0,1\}^n$, to make it multilinear. The multilinear representation is unique, so $\deg(f) \le \mathrm{D}(f)$. $\square$

For the majority of 3 bits, $s = bs = C = 2$ and $\mathrm{D} = \deg = 3$, since $\mathrm{MAJ}_3 = x_1x_2 + x_1x_3 + x_2x_3 - 2x_1x_2x_3$.

The measures are also bounded in the other direction. $\mathrm{D}(f) \le C(f)^2$, $\mathrm{D}(f) \le bs(f)^3$, $bs(f) \le 2\deg(f)^2$, and $\mathrm{D}(f) = O(R_2(f)^3)$ (Buhrman and de Wolf, 2002, give these with their sources). The question whether $s(f)$ is also polynomially related to them was the *sensitivity conjecture*. Huang (2019) proved $s(f) \ge \sqrt{\deg(f)}$, which settles it: $s$, $bs$, $C$, $\deg$, $\mathrm{D}$ and $R_2$ are all polynomially related. See the [sensitivity theorem](/sensitivity-theorem/), [sensitivity](/sensitivity/) and [block sensitivity](/block-sensitivity/).

### Graph properties and evasiveness

A function is *evasive* if $\mathrm{D}(f) = n$, so that some input forces the tree to read every bit. A graph property on $v$ vertices is a function of the $\binom{v}{2}$ bits of the adjacency matrix that does not change when the vertices are renamed. It is *monotone* if adding an edge never changes the answer from 1 to 0, and *nontrivial* if it is not constant.

- Rivest and Vuillemin (1976) proved that every nontrivial monotone graph property has $\mathrm{D} = \Omega(v^2)$. So for such properties, such as "the graph is connected" or "the graph has a triangle", no algorithm that reads the adjacency matrix is much faster than reading all of it.
- Kahn, Saks and Sturtevant (1984) proved that every nontrivial monotone graph property is evasive when $v$ is a prime power, and improved the general bound to about $v^2/4$.
- The conjecture that every nontrivial monotone graph property is evasive for all $v$ (the Aanderaa, Karp and Rosenberg conjecture) is open.

Monotonicity is needed. Some graph properties that are not monotone are decided with $O(v)$ queries; the standard example is the property of being a *scorpion graph*.

### Randomized trees

A randomized tree can be much cheaper than a deterministic one. Let $f$ be the complete binary tree of NAND gates of height $h$, a function of $n = 2^h$ bits that evaluates a game tree. Every deterministic tree reads all $n$ bits on some input, so $\mathrm{D}(f) = n$. The randomized algorithm of Snir evaluates a random child first and skips the other child when the first one decides the gate. Saks and Wigderson (1986) proved that its expected cost is $\Theta(n^{\alpha})$ with $\alpha = \lg\big((1 + \sqrt{33})/4\big) \approx 0.7537$, and that no zero-error randomized algorithm does better. See [game tree evaluation](/game-tree-evaluation/).

Lower bounds for randomized trees use the [Yao minimax principle](/yao-minimax-principle/) (Yao, 1977). For every distribution $\mu$ on inputs, the expected cost of the best zero-error randomized algorithm on its worst input is at least the least average cost under $\mu$ of a deterministic tree that computes $f$. The randomized sorting bound after Theorem 5 is this principle with the uniform distribution on the $n!$ orders.

### Pitfalls

- **A lower bound holds only for the queries in $Q$.** The sorting bound is for comparisons. Integer keys allow other operations, and [radix sort](/radix-sort/) uses them to beat it. Name the query set with every bound.
- **The counting bound is only a lower bound.** It needs no tree to exist. For $n = 12$ the least height is 30, not $\lceil \lg(12!) \rceil = 29$.
- **The counting bound is weak for few outputs.** For a function with two outputs it gives one query. Use an adversary, certificates or degree instead, as for parity and OR above.
- **Height is not running time.** The model counts queries only. A tree of height $O(n \log n)$ can need exponential time to compute the next query, and a tree of small height can have exponentially many nodes.
- **The model is non-uniform.** A bound for each $n$ separately does not give one algorithm for all $n$. An upper bound in the model is not an algorithm until someone gives a uniform way to build the trees.
- **Randomized and deterministic costs differ.** A deterministic lower bound, such as $\mathrm{D}(f) = n$ for the NAND tree, does not hold for randomized algorithms. A randomized lower bound needs its own argument, usually Yao's principle.

## References
