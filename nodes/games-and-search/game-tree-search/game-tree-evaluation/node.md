---
tag: 1ZVZRX
kind: problem
slug: game-tree-evaluation
name: Game tree evaluation
aliases:
- minimax value computation
- game value
area: games-and-search/game-tree-search
level: intro
summary: Given a finite game tree with values at its leaves, compute the minimax value of the root. Deterministic methods need all n leaves, randomized ones about n^0.7537 on uniform binary NAND trees.
prereqs: [game-tree, zero-sum-game]
see_also: [minimax, negamax, alpha-beta-pruning, knuth-moore-theorem, best-move-selection, yao-minimax-principle, proof-number-search, randomized-query-complexity]
sources:
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326 (the minimax value of a game tree, its negamax form, and the leaves that any method must read to prove it)
  - paper: doi:10.1016/0304-3975(85)90210-5
    title: Marc Snir, Lower bounds on probabilistic linear decision trees, Theoretical Computer Science 38 (1985)
    locator: pp. 69 to 82 (the randomized evaluation of NAND trees; general locator, the section was not checked)
  - paper: doi:10.1109/SFCS.1986.44
    title: Michael Saks and Avi Wigderson, Probabilistic Boolean decision trees and the complexity of evaluating game trees, 27th Annual Symposium on Foundations of Computer Science (1986)
    locator: pp. 29 to 38 (the randomized evaluation of uniform NAND trees is optimal, with exponent log2((1 + sqrt 33) / 4))
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press (1995)
    locator: Chapter 2, Section 2.1, Game Tree Evaluation, from p. 28 (the randomized algorithm on AND-OR trees and the deterministic lower bound), and Section 2.2, The Minimax Principle, from p. 31
---

Game tree evaluation is the problem of computing the minimax value of the root of a finite [game tree](/game-tree/): the outcome that both players can secure if both play as well as possible. The input is the tree, with a number at each leaf, the outcome for the player MAX. The output is one number. The usual cost measure is the number of leaves that a method reads, because in a game program the score of a leaf is the expensive step. Read all leaves and the problem is easy; the question is how many leaves a method can skip and still be sure of the answer. For a tree with $n$ leaves, every deterministic method must read all $n$ on some inputs, and a randomized method can do with an expected $\Theta(n^{0.7537})$ on uniform binary trees with values 0 and 1. To get a move and not only the value, see [best move selection](/best-move-selection/).

## In plain words

Two players take turns, and you have the whole tree of possible games written out, with the final score at the end of each branch. You want to know the score that results from best play by both sides.

The answer follows from the bottom up: at each branch point, the player whose turn it is takes the best branch for them. That reads every score in the tree.

Often you can skip parts. If one move already wins for you, you need not look at your other moves. But an opponent who knows your order of reading can arrange the scores so that you never get to skip. Reading in a random order defeats that opponent, and on average you then read a lot less.

## Definition

**Input.** A finite rooted tree $T$. Each inner node $v$ is a MAX node or a MIN node, and each leaf $\ell$ has a value $u(\ell)$ from an ordered set, usually the integers or $\{0, 1\}$. In a game, MAX and MIN alternate, but the problem does not need that.

**Output.** The minimax value $V(\mathrm{root})$, where
$$ V(\ell) = u(\ell), \qquad V(v) = \max_{c} V(c) \text{ at a MAX node}, \qquad V(v) = \min_{c} V(c) \text{ at a MIN node}, $$
over the children $c$ of $v$. In the [negamax](/negamax/) form, each leaf holds the value for the player to move there, and $V(v) = \max_c \bigl(-V(c)\bigr)$ at every inner node.

**Boolean trees.** With values 0 and 1, a MAX node is an OR and a MIN node is an AND, so $T$ is an AND-OR tree. In the negamax form with values 0 and 1 (1 for a win of the player to move), every inner node is a NAND: a position is won exactly when some move leads to a position that is lost for the opponent. Two NAND levels make an OR of ANDs, since NAND(NAND(a, b), NAND(c, d)) = (a AND b) OR (c AND d). So a tree of alternate AND and OR levels is a NAND tree, after the leaves are complemented when the height is odd, and the two forms have the same cost.

**Cost model.** The tree shape is known, and a method gets a leaf value only by reading it. The cost is the number of leaves read, in the worst case over the leaf values for a deterministic method, and as the worst case over the leaf values of the expected number for a randomized method that is always right. Time on a word RAM is the number of nodes visited; for a depth-first method this is at most the number of leaves read times the height plus one.

## Variants

- **Explicit or implicit tree.** If the tree is given as a data structure, its size $n$ is part of the input and $O(n)$ time is easy. In a game, the tree is given by the rules, with a move generator and a score for terminal positions, and it has exponential size in the depth. Then the problem is hard in general: a quantified Boolean formula $\exists x_1 \forall x_2 \ldots$ is a game tree of depth $n$ with $2^n$ leaves, so the implicit form is [PSPACE](/pspace/)-hard, as on the [QBF](/qbf/) and [generalized geography](/generalized-geography/) pages.
- **Depth-limited evaluation.** Cut the tree at depth $d$ and score the cut positions with an [evaluation function](/evaluation-function/). The result is the value of a smaller tree, not of the game.
- **Threshold question.** Decide whether $V(\mathrm{root}) \ge t$. This is a Boolean evaluation, by the reduction below.
- **Game graphs.** If positions repeat, the tree becomes a directed graph. Without cycles, memoization evaluates each position once. With cycles, the values are the labels of [winning and losing states](/winning-losing-states/), found by [retrograde analysis](/retrograde-analysis/).
- **Chance nodes.** Nodes that take an average are the [expectiminimax](/expectiminimax/) variant. Most cutoff arguments of this page then fail, because an average depends on every child.

## Examples

**A small NAND tree.** Take the tree ((1, 0), (1, 1)) in negamax form with values 0 and 1. The left child is NAND(1, 0) = 1 and the right child is NAND(1, 1) = 0, so the root is NAND(1, 0) = 1: the player to move wins by going right.

- Reading from left to right, a method reads 1 and 0 under the left child (value 1, which does not decide the root), then 1 and 1 under the right child: 4 leaves.
- Reading from right to left, it reads the two leaves of the right child, finds 0, and stops: 2 leaves.
- The randomized method picks the order of the children at random at each node. With probability $1/2$ it starts at the right child and reads 2 leaves. Otherwise it reads the left child, at an expected cost of $\frac12 \cdot 1 + \frac12 \cdot 2 = \frac32$, and then the right child, 2 more. The expected cost is $\frac12 \cdot 2 + \frac12 \cdot \frac72 = \frac{11}{4}$.

**The worst case of the randomized method.** For the uniform binary NAND tree of height $h$ with $n = 2^h$ leaves, let $C_0(h)$ and $C_1(h)$ be the largest expected cost over inputs with root value 0 and 1. The tests compute the exact expectation, with fractions, for each of the 65,536 inputs of height 4 and every smaller height, and find:

| $h$ | $n$ | $C_0(h)$ | $C_1(h)$ | worst / $n$ |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | 1 |
| 1 | 2 | 2 | 3/2 | 1 |
| 2 | 4 | 3 | 11/4 | 0.75 |
| 3 | 8 | 11/2 | 35/8 | 0.688 |
| 4 | 16 | 35/4 | 123/16 | 0.547 |
| 5 | 32 | 123/8 | 403/32 | 0.480 |
| 6 | 64 | 403/16 | 1387/64 | 0.394 |
| 10 | 1024 | 52595/256 | 178251/1024 | 0.201 |

The rows for $h \ge 5$ come from the recurrence in the Bounds section.

## Known algorithms

- **[Minimax](/minimax/) and [negamax](/negamax/).** A depth-first walk that reads every leaf: $\Theta(n)$ leaves and time, and space for one path. Correct for any values and any tree shape.
- **[Alpha-beta pruning](/alpha-beta-pruning/).** The same walk with two bounds that skip subtrees which cannot change the value. The answer is the same. On a uniform tree of branching factor $b$ and depth $d$ with the best move first everywhere, it reads $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, and no method that proves the value reads fewer ([Knuth-Moore theorem](/knuth-moore-theorem/)). With a bad order it reads all $b^d$. See [pruning in game trees](/pruning/) for the general idea.
- **Other exact searches.** [SSS*](/sss-star/), [Scout](/scout-search/), [principal variation search](/principal-variation-search/) and [MTD(f)](/mtdf/) return the same value with other orders of work, often on many threshold questions.
- **Boolean trees.** [Proof-number search](/proof-number-search/) is a best-first method for AND-OR trees that grows the part of the tree that is cheapest to prove or disprove.
- **Randomized evaluation (Snir 1985).** On a Boolean tree in NAND form: at each inner node, evaluate the children in a random order, and stop at the first child of value 0, since that fixes the node to 1. The method is always right; only its cost is random. Motwani and Raghavan (Section 2.1) give the same idea on AND-OR trees.

## Bounds

**Deterministic lower bound: all $n$ leaves.** On the uniform binary NAND tree, every deterministic method reads all $n$ leaves on some input. An adversary answers the reads. It keeps a rule: the first child of a node whose leaves have all been read gets the value 1. A 1 does not decide a NAND, so the node stays open until its second child has been read in full. When the last leaf under the second child is read, the nodes that become complete at that moment form a path upward, each with a sibling of value 1, so each is the complement of the one below. The adversary picks the leaf so that the top node of this path gets the value that its own rule needs. So no node, and in particular not the root, is known before all its leaves are read. The tests run this adversary against deterministic methods that read the leaves in many different fixed orders, not only depth first, for heights 1 to 4, and every one reads all $n$ leaves. Because Boolean trees are a special case, the bound holds for general values too.

**Randomized upper bound: $O(n^{0.7537})$.** For the randomized method on the uniform binary NAND tree of height $h$:
$$ C_0(h) = 2\, C_1(h-1), \qquad C_1(h) = C_0(h-1) + \tfrac12 C_1(h-1), \qquad C_0(0) = C_1(0) = 1. $$
A node of value 0 has two children of value 1, and both must be read. A node of value 1 has a child of value 0. If the other child is 1, the method reads the 0 child first with probability $\frac12$ and stops, and otherwise reads both, so the expected cost is $C_0 + \frac12 C_1$ in the worst case; if both children are 0, the cost is only $C_0$. Costs of children add, and the worst case for each child can be picked on its own, so these are the exact worst cases; the tests confirm them on all inputs up to height 4. The matrix $\begin{pmatrix} 0 & 2 \\ 1 & 1/2 \end{pmatrix}$ has the largest eigenvalue $\lambda = (1 + \sqrt{33})/4 \approx 1.68614$, so the cost grows like $\lambda^h = n^{\log_2 \lambda}$ with
$$ \log_2 \frac{1 + \sqrt{33}}{4} \approx 0.753725. $$

**Randomized lower bound: the same exponent.** Saks and Wigderson (1986) proved that no randomized method that is always right reads fewer leaves on uniform binary NAND trees, up to a constant factor, so the bound is $\Theta(n^{0.7537})$. The proof gives a hard distribution of inputs and bounds every deterministic method on it, by [Yao's minimax principle](/yao-minimax-principle/). The query model behind these bounds is the one of [decision tree complexity](/decision-tree-complexity/) and [randomized query complexity](/randomized-query-complexity/).

**With good order.** Upper bounds below $n$ for deterministic methods need luck in the input or a good guess at the order: alpha-beta reads $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves on a uniform tree of branching factor $b$ and depth $d$, with $n = b^d$, when the best move is first everywhere (this is $2\sqrt{n} - 1$ when $d$ is even), and $n$ when it is last.

## Reductions

**General values to Boolean values.** For a threshold $t$, replace each leaf value $u$ by 1 if $u \ge t$ and by 0 otherwise. Then the Boolean tree, with MAX as OR and MIN as AND, has the value 1 exactly when $V(\mathrm{root}) \ge t$. The proof is by induction from the leaves: $\max_c V(c) \ge t$ holds if and only if some $V(c) \ge t$, and $\min_c V(c) \ge t$ if and only if every $V(c) \ge t$. With $k$ distinct leaf values, a binary search over the thresholds finds the value with about $\log_2 k$ Boolean evaluations. This is the idea behind MTD(f) and Scout.

**Boolean values to best move selection.** Deciding the value of a Boolean tree reduces to choosing the best move in a tree with one more leaf, as on the [best move selection](/best-move-selection/) page.

**QBF to Boolean evaluation.** A formula $Q_1 x_1 \ldots Q_n x_n\, \varphi$ is true exactly when the Boolean tree of depth $n$, with an OR for each $\exists$, an AND for each $\forall$, and the truth of $\varphi$ at the leaves, has value 1. So the implicit problem is PSPACE-hard, and a depth-first evaluation in polynomial space shows that it is in PSPACE.

## Applications

- **Game programs.** Every search in a chess or checkers program evaluates a depth-limited game tree, usually with alpha-beta and its refinements.
- **Solving games.** A [solved game](/solved-game/) is one where the value of the start position has been computed, by evaluation of the full tree or graph.
- **AND-OR trees elsewhere.** Planning with nondeterministic actions, as in [contingent planning](/contingent-planning/), and proofs in logic programming search AND-OR trees.
- **Lower bounds.** NAND trees are a standard example in query complexity, where they separate deterministic, randomized and quantum query costs.

## References
