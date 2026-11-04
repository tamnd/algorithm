---
tag: 7DMG83
kind: theorem
slug: matroid-greedy-theorem
name: Greedy optimality on matroids
aliases:
- matroid greedy theorem
- greedy works exactly on matroids
- Rado-Edmonds theorem
area: techniques/greedy
level: core
summary: The greedy algorithm returns a maximum-weight basis for every weighted matroid, and the matroid property characterizes this.
prereqs: [matroid, matroid-greedy-algorithm]
see_also: [matroid-greedy-algorithm, maximum-weight-matroid-basis, matroid, greedy-choice-property, exchange-argument, kruskal, matroid-intersection, submodular-function]
sources:
  - paper: doi:10.1112/plms/s3-7.1.300
    title: Richard Rado, Note on independence functions, Proceedings of the London Mathematical Society s3-7(1), 1957
    locator: pages 300 to 320
  - paper: doi:10.1007/BF01584082
    title: Jack Edmonds, Matroids and the greedy algorithm, Mathematical Programming 1(1), 1971
    locator: pages 127 to 136
  - paper: doi:10.1016/S0021-9800(68)80039-0
    title: David Gale, Optimal assignments in an ordered set, an application of matroid theory, Journal of Combinatorial Theory 4(2), 1968
    locator: pages 176 to 180
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 16.4, Matroids and greedy methods
  - book: isbn:9783662560389
    title: Bernhard Korte and Jens Vygen, Combinatorial Optimization, sixth edition
    locator: Chapter 13, Matroids (the greedy algorithm and its characterization of matroids)
  - book: isbn:9780199603398
    title: James Oxley, Matroid Theory, second edition
    locator: Section 1.8, The greedy algorithm
---

The matroid greedy theorem says that the greedy algorithm, which scans the elements by decreasing weight and keeps each one that preserves independence, finds a maximum-weight independent set for every nonnegative weight function if and only if the independence system is a [matroid](/matroid/). The "if" part shows that greedy is exact on spanning trees, linearly independent vectors, partition constraints and unit jobs with deadlines. The "only if" part shows that matroids are exactly the right setting: on any other independence system, some weights make greedy fail. The theorem is due to Rado (1957) and Edmonds (1971).

## Statement

Let $(E, \mathcal{I})$ be an *independence system*: $E$ is finite, $\emptyset \in \mathcal{I}$, and every subset of a set in $\mathcal{I}$ is in $\mathcal{I}$. For $w : E \to \mathbb{R}$, the *greedy algorithm* orders $E$ as $e_1, \ldots, e_n$ with $w(e_1) \ge \cdots \ge w(e_n)$, ties broken in any way, starts with $A = \emptyset$, and for $i = 1, \ldots, n$ replaces $A$ by $A \cup \{e_i\}$ when that set is in $\mathcal{I}$. The following are equivalent.

1. $(E, \mathcal{I})$ is a matroid, that is, it has the exchange property: if $X, Y \in \mathcal{I}$ and $|X| < |Y|$, then $X \cup \{y\} \in \mathcal{I}$ for some $y \in Y \setminus X$.
2. For every $w : E \to \mathbb{R}_{\ge 0}$ and every way to break ties, the greedy algorithm returns a set $A \in \mathcal{I}$ with $w(A) = \max\{w(X) : X \in \mathcal{I}\}$.

Moreover, if $(E, \mathcal{I})$ is a matroid, then for every $w : E \to \mathbb{R}$ the greedy algorithm returns a basis of maximum weight among all bases, and its $k$-th heaviest element weighs at least as much as the $k$-th heaviest element of any independent set, for every $k$.

## In plain words

Some choice problems have a special shape. A small allowed choice can always grow by one item taken from any larger allowed choice. Problems with this shape are called matroids.

The theorem says two things. First, on a matroid the simple rule "take the most valuable item that still fits, and never look back" gives the best answer, whatever the values are. Second, this works only on matroids. If the shape is missing, there are values for which the simple rule gives a worse answer than the best one.

So the shape is not just helpful for the rule; it is exactly what the rule needs. To know whether greedy is safe for every choice of values, check the shape.

## Proof

**(1) implies the moreover part, and so (2).** Let $(E, \mathcal{I})$ be a matroid, $w$ any real weights, and $A = \{g_1, \ldots, g_r\}$ the output, in the order of selection, so $w(g_1) \ge \cdots \ge w(g_r)$.

*$A$ is a basis.* $A$ is independent, since each addition is tested. If $x \notin A$, then $x$ was rejected when the current set was some $A' \subseteq A$, so $A' \cup \{x\} \notin \mathcal{I}$, and its superset $A \cup \{x\}$ is not in $\mathcal{I}$ either. So $A$ is maximal.

*Element-wise domination.* Let $X \in \mathcal{I}$ with elements $x_1, \ldots, x_s$ sorted by nonincreasing weight. First, $s \le r$: otherwise the exchange property gives $x \in X \setminus A$ with $A \cup \{x\}$ independent, against maximality. Suppose $w(g_k) < w(x_k)$ for some $k \le s$, and take the least such $k$. Apply the exchange property to $P = \{g_1, \ldots, g_{k-1}\}$ and $Q = \{x_1, \ldots, x_k\}$: some $x_j \in Q \setminus P$ has $P \cup \{x_j\} \in \mathcal{I}$. Then $w(x_j) \ge w(x_k) > w(g_k)$, so the greedy algorithm examined $x_j$ before $g_k$. At that moment its current set was contained in $P$, so adding $x_j$ gave a subset of $P \cup \{x_j\}$, which is independent, and $x_j$ was accepted. Then $x_j$ is an element of $A$ chosen before $g_k$, so $x_j \in P$, a contradiction. Hence $w(g_k) \ge w(x_k)$ for all $k \le s$.

*Optimality.* All bases have size $r$, so for a basis $B$ the domination gives $w(B) \le w(A)$. If all weights are nonnegative, then for every $X \in \mathcal{I}$, $w(X) = \sum_{k \le s} w(x_k) \le \sum_{k \le s} w(g_k) \le w(A)$. This proves (2).

**(2) implies (1).** Suppose the exchange property fails: there are $X, Y \in \mathcal{I}$ with $|X| < |Y|$ such that $X \cup \{y\} \notin \mathcal{I}$ for every $y \in Y \setminus X$. Let $a = |X|$, so $|Y| \ge a + 1$. Define nonnegative integer weights
$$ w(e) = \begin{cases} a + 2 & e \in X, \\ a + 1 & e \in Y \setminus X, \\ 0 & \text{otherwise.} \end{cases} $$
The greedy algorithm first examines the elements of $X$, which are heavier than all others. Each set it forms from them is a subset of $X$, so it is independent, and all of $X$ is taken. Next it examines the elements $y \in Y \setminus X$. Its current set $A$ contains $X$, so $A \cup \{y\} \supseteq X \cup \{y\}$, which is not independent; by the hereditary property, $A \cup \{y\}$ is not independent, and $y$ is rejected. The remaining elements weigh 0. So the output has weight $a(a + 2)$. But $Y \in \mathcal{I}$ and
$$ w(Y) \ge (a + 1)\,|Y| \ge (a + 1)^2 = a(a + 2) + 1 > a(a + 2). $$
So the greedy algorithm is not optimal for this $w$, and (2) fails. $\square$

## Consequences

- **Spanning trees.** Forests of a graph form the [graphic matroid](/graphic-matroid/), so greedy by weight gives a maximum or, with the order reversed, a minimum spanning tree. This is [Kruskal's algorithm](/kruskal/).
- **Unit jobs with deadlines.** The sets of jobs that can meet their deadlines form a matroid, so greedy by profit is optimal for [job sequencing with deadlines](/job-sequencing-with-deadlines/).
- **Vectors.** A heaviest set of linearly independent vectors is found greedily in a [linear matroid](/linear-matroid/).
- **Any increasing objective.** By the element-wise domination, the greedy basis is optimal not only for the sum of weights but for every objective that is nondecreasing in each element weight, such as the bottleneck (the smallest weight in the basis). This is Gale's form of the theorem.
- **Only the order matters.** The output depends on $w$ only through the order of the weights, so one greedy run answers the problem for all weight functions with the same order.
- **Polyhedral form.** Edmonds (1971) showed that the greedy solution also solves the linear program $\max \{ w^\top x : x \ge 0,\ x(S) \le r(S) \text{ for all } S \subseteq E \}$, where $r$ is the rank function. So this polytope, the matroid polytope, has integral vertices, which are the characteristic vectors of the independent sets.
- **Test for the greedy method.** To show that greedy is exact for a selection problem with additive weights, it suffices to prove the exchange property of its feasible sets. This is the matroid route to the [greedy choice property](/greedy-choice-property/).

## Tightness

- **Every non-matroid fails for some weights.** The second half of the proof is constructive: whenever the exchange property fails for $X$ and $Y$, the weights $a + 2$, $a + 1$, 0 defeat greedy. For matchings in the path $a - b - c - d$, with $X = \{bc\}$ and $Y = \{ab, cd\}$, greedy returns weight 3 against 4.
- **Unit weights are not enough.** If all weights are 1, greedy returns a maximal independent set, and it is optimal whenever all maximal sets have the same size. That does not make a matroid. On $E = \{1, 2, 3, 4\}$ with the maximal independent sets $\{1, 2\}$ and $\{3, 4\}$, all maximal sets have size 2, but $\{1\}$ cannot be enlarged from $\{3, 4\}$. With $w(1) = 3$, $w(3) = w(4) = 2$, $w(2) = 0$, greedy returns $\{1, 2\}$ of weight 3, while $\{3, 4\}$ has weight 4.
- **Nonnegative weights in (2).** For the maximum-weight independent set, negative weights must be excluded: the greedy algorithm as stated takes a whole basis even when its last elements have negative weight. Stopping at the first nonpositive weight repairs this.
- **Independence systems.** On an independence system that is not a matroid, greedy is not exact, but its weight is at least the rank quotient of the system times the optimum, and this factor is the best possible for greedy (Jenkyns; Korte and Hausmann; see Korte and Vygen).
- **Two matroids.** The common independent sets of two matroids, such as bipartite matchings, are an independence system that is not a matroid in general, so greedy fails there, and [matroid intersection](/matroid-intersection/) algorithms are used instead.

## History

The greedy rule for spanning trees is older than matroids: Borůvka (1926) and Kruskal (1956) used it. Rado proved in 1957 that the greedy rule is optimal for every weight function exactly on matroids, in the language of independence functions. Gale (1968) proved the element-wise optimality of the greedy basis, in a paper on optimal assignments. Edmonds (1971), in "Matroids and the greedy algorithm", gave the characterization together with its linear programming form and made it widely known in combinatorial optimization. CLRS presents the "if" direction as the justification of the procedure GREEDY.

## References
