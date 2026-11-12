---
tag: GXXKFF
kind: algorithm
slug: quartet-max-cut
name: Quartet MaxCut
aliases:
- QMC
area: biology/phylogenetics
level: research
summary: Builds a tree from quartets by divide and conquer. Each step cuts the taxa so that the quartet pairs fall on opposite sides, like a max cut.
solves: [maximum-quartet-consistency]
model: word-ram
complexity:
  vars: {n: the number of taxa, m: the number of quartets}
  time: {worst: "O(n m^2 2^n)"}
  space: {extra: "O(n + m)"}
properties: {deterministic: true, exact: false, online: false, recursive: true}
history:
  year: 2010
  people: [Sagi Snir, Satish Rao]
  note: Snir and Rao published Quartets MaxCut in 2010 and a faster version for large inputs in 2012. Later work added quartet weights and better graph construction.
prereqs: [maximum-quartet-consistency, maximum-cut, quartet]
see_also: [astral, supertree, species-tree-estimation, dinkelbach-algorithm, fractional-programming, local-search, maximum-rooted-triplet-consistency, splits-of-a-tree]
sources:
  - paper: doi:10.1109/TCBB.2008.133
    title: Sagi Snir and Satish Rao, Quartets MaxCut, a divide and conquer quartets algorithm, IEEE/ACM Transactions on Computational Biology and Bioinformatics 7(4), 2010, pages 704 to 718
    locator: the quartet graph with good and bad edges, the ratio objective, the artificial taxa and the recursion
  - paper: doi:10.1016/j.ympev.2011.06.021
    title: Sagi Snir and Satish Rao, Quartet MaxCut, a fast algorithm for amalgamating quartet trees, Molecular Phylogenetics and Evolution 62(1), 2012
    locator: the fast version of the method and its tests on large simulated inputs
  - paper: "W. Dinkelbach, On nonlinear fractional programming, Management Science 13(7), 1967"
    title: W. Dinkelbach, On nonlinear fractional programming
    locator: the parametric iteration used here to find the cut with the best ratio
  - book: isbn:9781107184718
    title: Tandy Warnow, Computational Phylogenetics, 2017
    locator: Chapter 7, Supertrees, the part on quartet amalgamation
---

Quartet MaxCut (QMC) is a heuristic for [maximum quartet consistency](/maximum-quartet-consistency/): it builds an unrooted [phylogenetic tree](/phylogenetic-tree/) that agrees with many of a given set of [quartets](/quartet/). It works top down. It splits the taxa into two sides so that, for most quartets $ab|cd$, the pairs $a, b$ and $c, d$ fall on opposite sides, and it treats this as a [maximum cut](/maximum-cut/) problem on a graph built from the quartets. Each side gets one new taxon that stands for the other side, the quartets that cross the cut in the wrong way go down to the side that holds most of their taxa, and the two trees are glued at the new taxa. Snir and Rao (2010) introduced the method. It is fast, it has no worst-case guarantee, and it is a common way to turn many small quartet trees into one large tree.

## In plain words

You have many statements of the form "a and b are on one side of the tree, and c and d are on the other side". You want one tree that agrees with most of them. QMC makes one decision at a time: which taxa go to the left of the first edge and which go to the right.

Each statement says "cut between the pairs, and do not cut inside a pair". Count the cuts of the first kind as good and the cuts of the second kind as bad, and choose the split with the best ratio of good to bad. Then solve each side in the same way. A statement with three taxa on one side goes down to that side, where one new taxon takes the place of the fourth one.

## The problem

The input is a finite set $S$ of $n$ taxa and a list $Q$ of $m$ quartets $ab|cd$, each on four distinct taxa of $S$. The output is an unrooted tree $T$ whose leaves are the taxa and whose internal vertices have degree at least 3, together with the number of quartets of $Q$ that $T$ displays. A tree displays $ab|cd$ if one edge has $a, b$ on one side and $c, d$ on the other. The goal is a tree that displays as many quartets as possible. Finding the best tree is NP-hard, so QMC only tries to come close.

**The quartet graph.** For a cut $(S_1, S_2)$ of the taxa, each quartet $ab|cd$ gives four *good* edges $ac, ad, bc, bd$ and two *bad* edges $ab, cd$. $G$ is the number of good edges and $B$ the number of bad edges, over all quartets, whose ends lie on different sides. If $q$ has $a, b$ on one side and $c, d$ on the other, it adds 4 to $G$ and 0 to $B$, and the cut satisfies $q$. If $q$ has its pairs mixed, two on each side, it adds 2 to $G$ and 2 to $B$, and the cut violates $q$. If $q$ has three taxa on one side, it adds 2 to $G$ and 1 to $B$, and the cut leaves $q$ open. QMC chooses a cut with two or more taxa on each side and a large ratio $G/B$.

## The algorithm

```pseudo id=main
QUARTET-MAX-CUT(S, Q)
L1  put the task (S, Q) on a stack, and repeat until the stack is empty:
L2      if |S| ≤ 3 or Q is empty, the tree of the task is a star on S
L3      else find a cut (S_1, S_2), with |S_1|, |S_2| ≥ 2, of large ratio G/B:
L4          α ← 0, and c ← a cut that maximizes G − α·B
L5          while B(c) > 0: α ← G(c)/B(c), c' ← a cut that maximizes G − α·B; stop if its value is ≤ 0, else c ← c'
L6      add a new taxon x_1 to S_1 and a new taxon x_2 to S_2
L7      for each quartet q = ab|cd in Q do
L8          if two taxa of q are on each side and {a, b} is one side, count q as satisfied
L9          if three or four taxa of q are in S_i, replace its taxon on the other side, if any, by x_i, and give q to S_i
L10     solve (S_1 ∪ {x_1}, Q_1) and (S_2 ∪ {x_2}, Q_2), then join the trees: remove x_1 and x_2 and connect their neighbors
L11 return the tree of the first task and the number of satisfied quartets
```

Lines L4 and L5 are Dinkelbach's method for [fractional programming](/fractional-programming/). They replace the ratio $G/B$ by the difference $G - \alpha B$, which is easier to maximize, and they raise $\alpha$ until no cut beats the current ratio. The search over cuts is exact when the set is small: the implementation tries every cut with two or more taxa on each side up to 12 taxa, and it uses a seeded [local search](/local-search/) that moves one taxon at a time on larger sets. The method of Snir and Rao uses a fast heuristic for this step, so the ratio cut is not always the best one.

Line L9 is the point where QMC defers a decision. A quartet with three taxa on one side, say $a, b, c$ in $S_1$ and $d \in S_2$, is satisfied by the final tree exactly when the tree of $S_1 \cup \{x_1\}$ displays $ab|cx_1$, because $x_1$ is where the rest of the tree is attached. A quartet with two taxa on each side is decided at once, and it does not go down. Line L10 connects the two trees by one new edge, which is the edge of the cut.

## Example

There are six quartets on the taxa a to f:
$$Q = \{ab|cd,\ ab|ce,\ ab|de,\ cd|ef,\ ac|df,\ bf|cd\}.$$

**The top cut, lines L3 to L5.** With $\alpha = 0$, the best cut maximizes $G$ alone. It is $cde \mid abf$ with $G = 20$ and $B = 3$, so the ratio is $20/3$. With $\alpha = 20/3$, the best value of $G - \alpha B$ is $8/3$, reached by $ab \mid cdef$ with $G = 16$ and $B = 2$, ratio 8. With $\alpha = 8$, the best value is 0, so the loop stops at $ab \mid cdef$. Each quartet gives:

| quartet | taxa on the side ab | good edges cut | bad edges cut | at this cut |
|---|---|---|---|---|
| ab\|cd | a, b | 4 | 0 | satisfied |
| ab\|ce | a, b | 4 | 0 | satisfied |
| ab\|de | a, b | 4 | 0 | satisfied |
| cd\|ef | none | 0 | 0 | goes to the side cdef |
| ac\|df | a | 2 | 1 | goes to the side cdef as yc\|df |
| bf\|cd | b | 2 | 1 | goes to the side cdef as yf\|cd |

Here $y$ is the new taxon on the side cdef, which stands for $\{a, b\}$. The cut $cde \mid abf$ has a larger $G$, but it cuts three bad edges, and it would violate two of the quartets.

**The two sides.** The side $\{a, b, x\}$ has three taxa, so it is a star. The side $\{c, d, e, f, y\}$ has the quartets $cd|ef$, $yc|df$ and $yf|cd$. With $\alpha = 0$, the best cut is $cd \mid efy$ with $G = 10$ and $B = 2$, and with $\alpha = 5$ no cut has a positive value. This cut satisfies $cd|ef$ and $yf|cd$, and it violates $yc|df$. Both of its sides then have no quartets, so they are stars.

**The join.** The final tree has the two nontrivial splits $ab \mid cdef$ and $cd \mid abef$. One internal vertex has degree 4, with the neighbors e, f, the part ab and the part cd, so the tree is not binary. It displays $ab|cd$, $ab|ce$, $ab|de$, $cd|ef$ and $bf|cd$, which is 5 of the 6 quartets. The only lost quartet is $ac|df$, which corresponds to $yc|df$ in the subproblem. A brute force over all 105 unrooted binary trees on six taxa shows that 5 is the optimum, and 6 of the trees reach it. A binary resolution of the QMC tree keeps both splits, so it also displays these 5 quartets, and it cannot display more.

## Correctness

QMC is a heuristic, so the claim is not that the tree is optimal. The proof file shows four facts. The procedure stops, because both sides of each cut have two or more taxa and each child is smaller than its parent. It returns a tree whose leaves are exactly the input taxa, because the join of two trees at a pair of leaves is again a tree. The count of satisfied quartets equals the number of quartets that the tree displays: a quartet decided at line L8 is displayed if and only if it was counted, because the new edge of line L10 separates exactly the two sides, and a quartet passed down at line L9 is displayed by the final tree exactly when its replacement is displayed by the tree of the child. Last, when the cut search is exact, Dinkelbach's iteration stops after at most $2m + 1$ steps with a cut of the largest ratio $G/B$, because $B$ strictly decreases from step to step.

## Complexity

The model is the word RAM, and the costs are for the implementation with the exact cut search.

| part | cost | reason |
|---|---|---|
| one evaluation of $G - \alpha B$ | $O(m)$ | six edges per quartet |
| one exact cut search on $s$ taxa | $O(2^s m)$ | all cuts with two or more taxa on each side |
| Dinkelbach steps per subproblem | at most $2m + 1$ | $B$ decreases at each step |
| number of cuts | at most $n - 3$ | each cut is a different internal edge of the result |

Each quartet is in at most one subproblem at each depth, and the subproblems have at most $n$ taxa, so the total time is $O(n m^2 2^n)$. In practice, Dinkelbach stops after a few steps, as in the example. The fast versions replace the exact search by a heuristic that runs in time polynomial in $n$ and $m$, which is what makes QMC useful for thousands of taxa. The task stack, the plans for the joins and the quartets waiting in their subproblems take $O(n + m)$ extra space, because each quartet waits in at most one subproblem.

## Properties

- **Heuristic.** No approximation ratio is known. The tree can display fewer quartets than the optimum. In one run of 300 random inputs on 5 or 6 taxa with 4 to 12 quartets, the implementation was below the brute-force optimum 13 times.
- **Not always binary.** A subproblem without quartets becomes a star, so the output can have vertices of high degree where the input says nothing.
- **Consistent input.** For a complete set of quartets that all come from one binary tree, the tests always recover that tree. This is an observation from the tests on up to 8 taxa, not a theorem of this page.
- **Order does not matter.** The cut depends on the quartets only through $G$ and $B$, so the order of the input does not change the tree, except where ties in the cut search are broken by the order of the taxa.
- **Deterministic.** The exact search is deterministic, and the local search uses a fixed seed.

## Variants and improvements

- **Weighted quartets (wQMC).** Avni, Cohen and Snir (2015) give each quartet a weight, for example its support from the data, and weigh its good and bad edges by it.
- **Quartets from gene trees.** For [species tree estimation](/species-tree-estimation/), the quartets come from gene trees. TREE-QMC (Han and Molloy) builds the quartet graph directly from the gene trees, without listing all quartets, and normalizes the weights. This makes the method practical for large data sets.
- **Exact alternatives.** [ASTRAL](/astral/) solves the weighted problem exactly over a restricted set of splits by dynamic programming. It is slower, and it is usually more accurate.
- **Rooted analog.** For rooted triplets, a cut that keeps the pair of each triplet together is the idea of the min-cut supertree method of Semple and Steel. It is a heuristic for the rooted problem, [maximum rooted triplet consistency](/maximum-rooted-triplet-consistency/).

## When to use it

Use QMC to combine a large number of quartet trees, for example from a [supertree](/supertree/) analysis or from four-taxon subsets of a large alignment, when an exact method is too slow. Use its weighted versions to combine gene trees into a species tree. Do not use it when you need a guarantee on the number of displayed quartets: for small inputs, an exact search is possible, and for complete inputs the PTAS of Jiang, Kearney and Li has a guarantee.

## Pitfalls

- **Ratio, not difference.** Maximizing $G - B$ alone, or $G$ alone, picks cuts that cut many bad edges, as the cut $cde \mid abf$ in the example shows. The ratio, or a well chosen $\alpha$, is necessary.
- **Small sides.** A side with one taxon has no edge to resolve, and the recursion would not shrink. Both sides need two or more taxa.
- **Wrong replacement.** A quartet with three taxa in $S_1$ must get the new taxon of $S_1$, which stands for $S_2$, not the new taxon of $S_2$. With the wrong taxon, the deferred quartet refers to a taxon that the child does not have.
- **Counting at the wrong time.** A quartet with two taxa on each side is decided at the cut. It must not go down to a child, or it is counted twice.
- **Deep recursion.** On a caterpillar-like result the recursion depth is about $n$. The implementation uses an explicit stack of tasks for this reason.

## Implementations

## History

Quartet methods for building trees go back to the 1990s, with quartet puzzling and the PTAS of Jiang, Kearney and Li for complete inputs. Snir and Rao (2010) proposed Quartets MaxCut, which reduces each step of a top-down construction to a cut problem with good and bad edges, and in 2012 they described a fast version for large inputs. Avni, Cohen and Snir (2015) extended it to weighted quartets. Later, Han and Molloy built the quartet graph directly from gene trees in TREE-QMC, which made it a competitor to ASTRAL for large species tree problems.

## References
