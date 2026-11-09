---
tag: R0CA6Z
kind: algorithm
slug: genetic-programming
name: Genetic programming
aliases:
- GP
- tree-based genetic programming
area: optimization/metaheuristics
level: advanced
summary: A genetic algorithm whose individuals are programs, most often expression trees, changed by subtree crossover and subtree mutation. Its main use is symbolic regression.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {G: the number of generations, N: the population size, S: the largest tree size, m: the number of fitness cases, k: the tournament size}
  time: {worst: O(G N (S m + k))}
  space: {extra: O(N S)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 1992
  people: [John R. Koza, Nichael L. Cramer]
  note: Cramer evolved tree-structured programs in 1985. Koza developed the method with subtree crossover and ramped half-and-half and set it out in his 1992 book Genetic Programming.
prereqs: [genetic-algorithm, expression-tree]
see_also: [tournament-selection, crossover, mutation, elitism, schema-theorem, abstract-syntax-tree, overfitting, premature-convergence]
sources:
  - book: isbn:9780262111706
    title: John R. Koza, Genetic Programming, On the Programming of Computers by Means of Natural Selection, MIT Press, 1992
    locator: Chapter 6 (the function and terminal sets, closure, ramped half-and-half, crossover and the depth limit) and Chapter 10 (symbolic regression)
  - book: isbn:9781409200734
    title: Riccardo Poli, William B. Langdon and Nicholas F. McPhee, A Field Guide to Genetic Programming, lulu.com, 2008
    locator: Chapters 2 to 5 (representation, initialization, selection, subtree crossover and mutation) and Chapter 11 (bloat)
  - paper: Nichael Lynn Cramer, A representation for the adaptive generation of simple sequential programs, Proceedings of the First International Conference on Genetic Algorithms and Their Applications, 1985
    title: A representation for the adaptive generation of simple sequential programs
    locator: pages 183 to 187 (tree-structured programs changed by genetic operators)
  - book: doi:10.1007/978-3-662-04726-2
    title: William B. Langdon and Riccardo Poli, Foundations of Genetic Programming, Springer, 2002
    locator: Chapters 4 and 5 (schema theorems for GP) and Chapter 8 (the size and depth of trees)
  - paper: doi:10.1162/evco.2006.14.3.309
    title: Sean Luke and Liviu Panait, A comparison of bloat control methods for genetic programming, Evolutionary Computation 14(3), 2006
    locator: pages 309 to 344 (depth limits, parsimony pressure and their effect on tree size)
  - paper: doi:10.1126/science.1165893
    title: Michael Schmidt and Hod Lipson, Distilling free-form natural laws from experimental data, Science 324(5923), 2009
    locator: pages 81 to 85 (symbolic regression by GP that finds conserved quantities of physical systems)
---

Genetic programming (GP) is a [genetic algorithm](/genetic-algorithm/) in which each individual is a program. In the usual form a program is an [expression tree](/expression-tree/) built from a set of functions, such as $+$, $-$ and $\times$, and a set of terminals, such as the input $x$ and constants. The fitness of a tree is its error on a list of test inputs, and new trees come from subtree crossover, which swaps a subtree of one parent for a subtree of another, and from subtree mutation, which replaces a subtree by a random one. The main use is symbolic regression: find a formula that fits data, with no fixed form given in advance. GP has no useful time bound in general, but with elitism and mutation it finds a zero-error tree with probability 1 when one exists within the depth limit.

## In plain words

Write each candidate formula as a tree: the leaves are the input and small constants, and the inner nodes are operations such as add and multiply. Start with many random trees. Score each tree by how far its values are from the wanted values on some test inputs.

To make the next round, pick good trees by small contests. Most new trees come from two parents: cut a branch out of the first tree and put a branch of the second tree in its place. Some new trees come from one parent with a branch replaced by a new random branch. Keep the best tree as it is, and throw away any child that is too deep. Repeat until a tree fits the data or the time runs out.

## The problem

The input is a list of $m$ fitness cases $(x_1, y_1), \ldots, (x_m, y_m)$, a function set $F$ and a terminal set $T$. A tree is a terminal, or a function from $F$ with one subtree for each argument. The error of a tree $t$ is $E(t) = \sum_{i=1}^m |t(x_i) - y_i|$, and the goal is a tree with $E(t) = 0$, or with $E$ as small as possible. The depth of a terminal is 0, and the depth of any other tree is one more than the largest depth of its subtrees. Trees deeper than $D_{\max}$ are not allowed.

The function set must have **closure**: every function must accept every value that any tree can return. With $F = \{+, -, \times\}$ on integers this holds. With division it holds only if division by 0 returns a fixed value, which Koza called protected division.

## The algorithm

The parameters are the population size $N$, the number of generations $G$, the tournament size $k$, the probabilities $p_c$ and $p_m$ of crossover and mutation with $p_c + p_m \le 1$, the number of elites $e$, the initial depth $D_{\text{init}}$, the depth limit $D_{\max}$ and the depth $D_{\text{mut}}$ of new subtrees in mutation.

```pseudo id=main
GP(cases, N, G, k, p_c, p_m, e, D_init, D_max, D_mut)
L1  P ← N trees by ramped half-and-half with depths 2 to D_init
L2  compute the error E(t) of each tree t in P
L3  for g ← 1 to G, while the smallest error is above 0 do
L4      Q ← the e trees of P with the smallest errors       ▷ elitism
L5      while |Q| < N do
L6          with probability p_c: a, b ← two tournament winners; child ← a with a random subtree replaced by a random subtree of b
L7          with probability p_m: a ← a tournament winner; child ← a with a random subtree replaced by grow(D_mut)
L8          otherwise: a ← a tournament winner; child ← a      ▷ reproduction
L9          if depth(child) > D_max then child ← a
L10         add child to Q
L11     P ← Q, and compute the error of each tree in P
L12 return a tree of P with the smallest error
```

**Full and grow.** The full method builds a tree in which every leaf has depth exactly $d$: it takes a random function at each node above depth $d$ and a random terminal at depth $d$. The grow method takes a uniform random element of $F \cup T$ at each node above depth $d$ and a random terminal at depth $d$, so its trees have depth at most $d$ and many shapes.

**Ramped half-and-half.** Line L1 spreads the population over the depth limits $2, 3, \ldots, D_{\text{init}}$ in equal parts, and builds half of each part with full and half with grow. This gives trees of many sizes and shapes at the start.

**Tournament.** A [tournament](/tournament-selection/) draws $k$ trees uniformly with replacement and returns the one with the smallest error.

**Random subtree.** In lines L6 and L7, a random subtree is the subtree at a node chosen uniformly among all nodes of the tree. Koza chose an inner node with probability 0.9 and a leaf with probability 0.1. The uniform choice is simpler and is the one the implementation uses.

## Example

The fitness cases are $x = -5, -4, \ldots, 5$ with $y = x^2 + x + 1$, so $m = 11$, and the sets are $F = \{+, -, \times\}$ and $T = \{x, 1\}$. Take two parents.

| tree | formula | error |
|---|---|---|
| $a = (+\ (\times\ x\ x)\ 1)$ | $x^2 + 1$ | $\sum \lvert x \rvert = 30$ |
| $b = (+\ x\ 1)$ | $x + 1$ | $\sum x^2 = 110$ |

In preorder, the nodes of $a$ are $+$, $\times$, $x$, $x$, $1$, and the nodes of $b$ are $+$, $x$, $1$. Subtree crossover chooses one of the 5 nodes of $a$ and one of the 3 nodes of $b$, so there are 15 children with probability $1/15$ each.

- Replace the leaf $1$ of $a$ by all of $b$: the child is $(+\ (\times\ x\ x)\ (+\ x\ 1)) = x^2 + x + 1$, with error 0.
- Replace the first $x$ of $a$ by all of $b$: the child is $(+\ (\times\ (+\ x\ 1)\ x)\ 1) = (x + 1)x + 1$, also with error 0. The same holds for the second $x$.
- Replace the $\times$ node of $a$ by all of $b$: the child is $(+\ (+\ x\ 1)\ 1) = x + 2$, with error $\sum |x^2 - 1| = 101$.

Exactly 3 of the 15 children have error 0, so one crossover of these parents gives an exact formula with probability $1/5$. Neither parent was close: one lacked the term $x$ and the other the term $x^2$, and crossover joined the two parts. The test file checks this count.

## Correctness

GP gives no certificate that a tree is the best possible, unless its error is 0. Its correctness consists of these invariants and one convergence statement. The proofs are below.

- **Closure.** Every tree in every population is a well-formed tree over $F \cup T$, so every tree has a defined value on every input.
- **Depth.** Every tree has depth at most $D_{\max}$: the initial trees have depth at most $D_{\text{init}} \le D_{\max}$, and line L9 replaces any deeper child by its parent.
- **Elitism.** With $e \ge 1$, the smallest error in the population never increases, and line L12 returns a tree with the smallest error seen in any generation.
- **Convergence.** If a tree $t^*$ with $E(t^*) = 0$ and depth at most $D_{\text{mut}} \le D_{\max}$ exists, and $p_m > 0$ and $N > e$, then each generation creates $t^*$ with probability at least $p_m \, 5^{-\text{size}(t^*)} / S$ for the sets above, where $S = 2^{D_{\max}+1} - 1$. So the probability that no tree of error 0 exists after $g$ generations tends to 0 as $g$ grows.

The convergence bound is useless as a time bound, since it is exponential in the size of $t^*$. Runtime analyses of simple GP exist only for small model problems.

## Complexity

The error of one tree with at most $S$ nodes on $m$ cases costs $O(S m)$. A tournament costs $O(k)$, and crossover, mutation and the depth check each cost $O(S)$. So one generation costs $O(N (S m + k))$, and $G$ generations cost $O(G N (S m + k))$, plus $O(N \log N)$ per generation to find the elites by sorting. The population takes $O(N S)$ space. A binary tree of depth at most $D_{\max}$ has at most $S = 2^{D_{\max}+1} - 1$ nodes, so $S$ can be large, and in practice the cost depends on the actual sizes of the trees, which tend to grow during a run.

## Properties

- **Variable size.** Trees change size and shape during the run, unlike the fixed-length strings of a genetic algorithm.
- **Interpretable output.** The result is a formula or program that a person can read, check and simplify.
- **Bloat.** The average tree size tends to grow over the generations with little gain in fitness. Much of the growth is in parts of the tree that do not change its value, such as $(-\ x\ x)$.
- **Anytime.** With elitism, the best tree found so far is always available and never gets worse.

## Variants and improvements

- **Linear GP.** A program is a sequence of register instructions instead of a tree.
- **Cartesian GP.** A program is a directed acyclic graph on a grid of nodes, coded by a fixed-length list of integers.
- **Grammatical evolution.** An integer string selects the rules of a grammar, so the programs always respect the grammar.
- **Strongly typed GP.** Each function has argument and result types, and the operators keep the trees well typed. This replaces the closure requirement.
- **Bloat control.** Depth or size limits, parsimony pressure (a penalty on size), and lexicographic selection that prefers smaller trees on a tie in error.
- **Lexicase selection.** A parent is chosen by filtering the population one fitness case at a time in random order, instead of by total error.
- **Semantic operators.** Geometric semantic crossover combines the outputs of the parents directly, for example $r \cdot a + (1 - r) \cdot b$ for a random $r$, with known effects on the error but fast growth of the trees.
- **Constant optimization.** Fit the numeric constants of each tree by a local method, such as least squares, inside the GP loop.

## When to use it

Use GP when the form of the answer is unknown and a readable formula or small program is the goal, as in symbolic regression on scientific data, the design of heuristics and some problems of automatic program repair. If the form of the model is known, fit its parameters directly, for example by [linear regression](/linear-regression/), which is much faster and gives exact answers. If only predictions matter, standard machine learning models are usually faster to train and easier to tune than GP. A formula found by GP can fit the training cases exactly and still fail on new inputs, so test it on data held back, as with any model that can [overfit](/overfitting/).

## Pitfalls

- **No closure.** Without protected operations, a tree such as $x / (x - x)$ fails at run time. Define the value of each function on all inputs, or use typed GP.
- **Bloat.** Without a depth or size limit, trees can grow until the evaluation is very slow. Line L9 is one guard. Return the simplified form of the result.
- **Large constants by chance.** With only small constants in $T$, a tree needs many nodes to build a constant such as 37. Add ephemeral random constants, which are new random numbers created when a leaf is made, or a local fit of the constants.
- **Overfitting.** A formula with zero error on few cases can be wrong elsewhere. Keep a test set apart from the fitness cases.
- **Floating point.** With real values, exact zero error is rare. Stop at a small error threshold, and watch for overflow in deep products.

## Implementations

## History

Cramer (1985) evolved tree-structured programs with genetic operators. Koza developed tree-based GP in the late 1980s, with subtree crossover, the closure requirement, ramped half-and-half and many applications, and published his first GP book in 1992, followed by three more volumes up to 2003. Poli and Langdon proved schema theorems for GP in the late 1990s, and Langdon and Poli collected the theory in 2002. Schmidt and Lipson (2009) used GP to find conserved quantities from measured motion data, which drew wide attention to symbolic regression.

## References
