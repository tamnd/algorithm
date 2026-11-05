---
tag: 19BYG6
kind: problem
slug: post-office-problem
name: Post office problem
aliases:
- k-median on a line
- placing k post offices on a line
area: searching/search-on-answers
level: advanced
summary: Choose k facility positions on a line to minimize total distance from houses to their nearest facility.
model: algebraic-decision-tree
complexity:
  vars: {n: the number of houses, k: the number of post offices, U: "the range of the integer coordinates"}
  time: {worst: "O(n log n + n log(n U))"}
prereqs: [median, divide-and-conquer-optimization, aliens-trick, monge-property]
see_also: [k-median-problem, aliens-trick, monge-property, knuth-optimization, divide-and-conquer-optimization, smawk-algorithm, maximin-placement, minimax-partition]
sources:
  - url: https://ioinformatics.org/files/ioi2000problem5.pdf
    title: IOI 2000, Post Office
    note: the competition version, with V villages and P post offices
  - paper: doi:10.1007/BF02574380
    title: "Alok Aggarwal, Baruch Schieber and Takeshi Tokuyama, Finding a minimum-weight k-link path in graphs with the concave Monge property and applications, Discrete and Computational Geometry 12 (1994), 263-280"
    note: convexity in k of minimum-weight k-link paths under the concave Monge property, and the parametric search on the penalty
  - paper: doi:10.1016/0167-6377(91)90041-M
    title: "Refael Hassin and Arie Tamir, Improved complexity bounds for location problems on the real line, Operations Research Letters 10(7) (1991), 395-402"
    note: the k-median on a line in O(kn) time
---

The post office problem places $k$ post offices on a line with $n$ houses so that the total distance from each house to its nearest post office is as small as possible. It is the [k-median problem](/k-median-problem/) restricted to one dimension, where it becomes easy: the houses served by one office form a contiguous block in sorted order, the best office for a block is at its [median](/median/) house, and the problem becomes the partition of a sorted list into $k$ blocks with the smallest total cost. A dynamic program solves it in $O(kn^2)$ time; the [Monge property](/monge-property/) of the block cost brings this down to $O(kn \log n)$, $O(n^2)$ or $O(kn)$; and since the optimum is convex in $k$, a binary search on a penalty per office, the [Aliens trick](/aliens-trick/), removes the dependence on $k$. That last step is a search on the answer of a new kind: the search is over a price, and the predicate is the number of offices the price buys.

## In plain words

Houses stand along a straight road, and the town can build a few post offices. Everyone walks to the nearest one, and the town wants the total walking to be as small as possible.

Two facts make this easy. The houses that use the same office sit next to each other along the road, so the town only has to cut the row of houses into groups. And for one group the best spot is the middle house, because moving away from it brings the office closer to fewer people than it takes it away from.

So the task is to cut the row into the right groups. Trying the cuts one office at a time works. A faster idea charges a fee for each office, finds the best plan for that fee, and adjusts the fee until the plan builds exactly the wanted number of offices.

## Definition

**Input.** Real numbers $x_1 \le x_2 \le \cdots \le x_n$, the positions of the houses (sorted; sorting costs $O(n \log n)$ otherwise), and an integer $k$ with $1 \le k \le n$.

**Output.** Positions $p_1, \ldots, p_k$ that minimize
$$\mathrm{OPT}(k) = \min_{p_1, \ldots, p_k} \sum_{i=1}^{n} \min_{1 \le j \le k} |x_i - p_j|.$$

**Lemma 1 (one office).** For houses $x_a \le \cdots \le x_b$, the sum $\sum_{i=a}^{b} |x_i - p|$ is minimized at $p = x_m$ with $m = \lfloor (a + b)/2 \rfloor$, a median.

*Proof.* The function $\phi(p) = \sum |x_i - p|$ is convex and piecewise linear. Moving $p$ right by $\delta$, while no house lies strictly between $p$ and $p + \delta$, changes $\phi$ by $\delta (L - R)$, where $L$ is the number of houses at or left of $p$ and $R$ the number strictly right of $p$. At $p = x_m$, moving right gives $L \ge m - a + 1 \ge b - m \ge R$, because $2m \ge a + b - 1$; moving left by $\delta$ changes $\phi$ by $\delta (R' - L')$, where $R' \ge b - m + 1$ houses lie at or right of $x_m$ and $L' \le m - a$ lie strictly left, and $b - m + 1 \ge m - a$ because $2m \le a + b$. So neither direction decreases $\phi$, and a convex function with no descent direction is at its minimum. $\square$

Write $w(a, b)$ for this minimum. With prefix sums $S_j = x_1 + \cdots + x_j$ ([prefix sums](/prefix-sums/)),
$$w(a, b) = x_m (m - a + 1) - (S_m - S_{a-1}) + (S_b - S_m) - x_m (b - m),$$
so each block cost takes $O(1)$ time after $O(n)$ preprocessing.

**Lemma 2 (contiguous blocks).** There is an optimal solution in which the houses served by each office form a contiguous block $x_a, \ldots, x_b$, and each office is at a median of its block.

*Proof.* Take any optimal offices, sorted as $p_1 \le \cdots \le p_k$, and send each house to its nearest office, breaking ties toward the left one. The set of points whose nearest office is $p_j$ is an interval, so each office serves a contiguous block of the sorted houses. Moving each office to a median of its block does not increase the cost, by Lemma 1. $\square$

So
$$\mathrm{OPT}(k) = \min_{0 = i_0 < i_1 < \cdots < i_k = n} \sum_{j=1}^{k} w(i_{j-1} + 1, i_j),$$
a partition of a sorted sequence into $k$ blocks, the same shape as [minimax partition](/minimax-partition/) with a sum in place of a maximum.

## Variants

- **Weighted houses.** House $i$ has $c_i$ letters, and the cost is $\sum c_i |x_i - p|$. The office of a block is at its [weighted median](/weighted-median/), and everything else carries over.
- **Opening costs instead of a count.** Each office costs $f$ to build, and the goal is to minimize the walking plus $f$ times the number of offices. This is the uncapacitated [facility location problem](/facility-location-problem/) on a line, and it is exactly the penalized problem of the Aliens trick below.
- **Squared distances.** The cost $\sum (x_i - p)^2$ puts the office at the mean of its block, and the problem is [k-means](/k-means/) in one dimension. The block cost again has the Monge property, and the same algorithms apply.
- **The largest distance.** Minimizing the largest walk instead of the sum is the [k-center problem](/k-center-problem/) on a line, which a greedy check plus [binary search on the answer](/binary-search-on-answer/) solves; the dual question, keeping offices far apart, is [maximin placement](/maximin-placement/).
- **Offices at given sites.** If the offices must stand at candidate sites other than the houses, the blocks are still contiguous, but the best site of a block is the candidate nearest its median on one side or the other.

## Examples

Houses at $1, 2, 6, 7, 8, 15$.

| $k$ | best blocks | offices | $\mathrm{OPT}(k)$ | $\mathrm{OPT}(k-1) - \mathrm{OPT}(k)$ |
|---|---|---|---|---|
| 1 | $\{1,2,6,7,8,15\}$ | 6 | 21 | |
| 2 | $\{1,2\}, \{6,7,8,15\}$ | 1, 7 | 1 + 10 = 11 | 10 |
| 3 | $\{1,2\}, \{6,7,8\}, \{15\}$ | 1, 7, 15 | 1 + 2 + 0 = 3 | 8 |
| 4 | | | 2 | 1 |
| 5 | | | 1 | 1 |
| 6 | every house its own block | | 0 | 1 |

The savings $10, 8, 1, 1, 1$ do not increase, so $\mathrm{OPT}(k)$ is convex in $k$. For $k = 2$, a block with an even number of houses has two medians: $\{6, 7, 8, 15\}$ costs $10$ with the office anywhere in $[7, 8]$.

**The penalized search for $k = 2$.** For a price $\lambda$ per office, let $g(\lambda) = \min_{k'} (\mathrm{OPT}(k') + \lambda k')$, the cheapest plan when offices cost $\lambda$ each, and let $c(\lambda)$ be the number of offices it uses. The plan with $k'$ offices is cheapest exactly when $\lambda$ lies between the savings on either side of $k'$, so a plan with $2$ offices is cheapest exactly when $8 \le \lambda \le 10$. At $\lambda = 9$: $21 + 9 = 30$, $11 + 18 = 29$, $3 + 27 = 30$, so $g(9) = 29$ with $c = 2$, and $\mathrm{OPT}(2) = g(9) - 2 \cdot 9 = 11$. At $\lambda = 5$ the cheapest plan has $3$ offices ($3 + 15 = 18$), so the price must go up; at $\lambda = 20$ it has $1$ ($21 + 20 = 41$), so the price must go down.

## Known algorithms

**Dynamic programming, $O(kn^2)$.** Let $D[j][i]$ be the least cost of serving $x_1, \ldots, x_i$ with $j$ offices. Then $D[0][0] = 0$, $D[0][i] = \infty$ for $i > 0$, and
$$D[j][i] = \min_{j - 1 \le t < i} \big( D[j-1][t] + w(t + 1, i) \big).$$
There are $kn$ entries and each takes $O(n)$ time. This is fast enough for the IOI 2000 task, which has $n \le 300$ and $k \le 30$.

**The Monge property.** For $a \le b \le c \le d$, the block cost satisfies the quadrangle inequality
$$w(a, c) + w(b, d) \le w(a, d) + w(b, c).$$
Let $\mathrm{opt}(j, i)$ be the smallest $t$ that attains the minimum in $D[j][i]$. The inequality makes $\mathrm{opt}(j, i)$ nondecreasing in $i$, and with it:

- [divide-and-conquer optimization](/divide-and-conquer-optimization/) computes each row $D[j][\cdot]$ in $O(n \log n)$, for $O(kn \log n)$ in total;
- [Knuth's optimization](/knuth-optimization/), using $\mathrm{opt}(j-1, i) \le \mathrm{opt}(j, i) \le \mathrm{opt}(j, i+1)$, computes the whole table in $O(n^2)$, independent of $k$;
- the [SMAWK algorithm](/smawk-algorithm/) computes each row in $O(n)$, for $O(kn)$ in total, the bound of Hassin and Tamir.

**The Aliens trick, independent of $k$.** Penalize each office by $\lambda$ and solve the one-dimensional recurrence
$$E[i] = \min_{0 \le t < i} \big( E[t] + w(t + 1, i) + \lambda \big),$$
which has no index $j$ and takes $O(n)$ time with SMAWK or $O(n \log n)$ with a simpler monotone queue, recording the number of blocks $c(\lambda)$ of a minimizer. Then binary search on $\lambda$ for a price with $c(\lambda) = k$, or the boundary price if no price gives exactly $k$, and return $E[n] - \lambda k$. For integer coordinates every saving $\mathrm{OPT}(k-1) - \mathrm{OPT}(k)$ is an integer in $[0, nU]$, so integer values of $\lambda$ suffice and the search takes $O(\log(nU))$ rounds. The total is $O(n \log(nU))$ after sorting. Two facts make this a valid search on the answer:

*The predicate is monotone.* If $\lambda_1 < \lambda_2$ and $c_1, c_2$ are the counts of any optimal plans at the two prices, then $c_2 \le c_1$. *Proof.* Optimality at each price gives $\mathrm{OPT}(c_1) + \lambda_1 c_1 \le \mathrm{OPT}(c_2) + \lambda_1 c_2$ and $\mathrm{OPT}(c_2) + \lambda_2 c_2 \le \mathrm{OPT}(c_1) + \lambda_2 c_1$. Adding them gives $(\lambda_2 - \lambda_1)(c_2 - c_1) \le 0$, and $\lambda_2 > \lambda_1$ forces $c_2 \le c_1$. $\square$ So "the plan at price $\lambda$ uses at most $k$ offices" is a [monotone predicate](/monotone-predicate/) in $\lambda$, as the trace above shows.

*Every $k$ is reached.* Monotonicity alone does not make every count appear; that needs $\mathrm{OPT}(k)$ to be convex in $k$, so that each $k$ is optimal for the prices between its two neighbouring savings. Convexity of the minimum weight of a $k$-link path under the concave Monge property is a theorem of Aggarwal, Schieber and Tokuyama, and it applies here because $w$ satisfies the quadrangle inequality. When several counts tie at the boundary price, take the smallest count among the minimizers, search for the smallest price whose count is at most $k$, and the formula $E[n] - \lambda k$ is still exact because all tied plans have the same penalized cost.

## Bounds

- **Upper.** $O(n \log n)$ to sort, then $O(n \log(nU))$ by the Aliens trick with SMAWK for integer coordinates, or $O(kn)$ by SMAWK row by row, or $O(n^2)$ by Knuth's optimization.
- **Lower.** When $k$ is part of the input and the houses are not sorted, $\Omega(n \log n)$ comparisons are needed in the algebraic decision tree model. With $k = n - 1$, exactly two houses share an office, and the best choice is the closest pair, so $\mathrm{OPT}(n - 1)$ is the smallest gap between consecutive sorted houses. Then $\mathrm{OPT}(n-1) = 0$ if and only if two houses coincide, which decides [element distinctness](/element-distinctness/), and element distinctness needs $\Omega(n \log n)$.
- **One office.** For $k = 1$ the answer is the median, found in $O(n)$ time without sorting by [median of medians](/median-of-medians/) or in expected $O(n)$ by [quickselect](/quickselect/).

## Reductions

- **To a shortest $k$-link path.** Make a graph on $0, 1, \ldots, n$ with an edge $t \to i$ of weight $w(t + 1, i)$ for every $t < i$. A partition into $k$ blocks is a path from $0$ to $n$ with exactly $k$ edges, and the weights form a Monge matrix. This is the setting of Aggarwal, Schieber and Tokuyama.
- **From the count to a price.** The constraint "exactly $k$ offices" is moved into the objective with a multiplier $\lambda$, a one-dimensional [Lagrangian relaxation](/lagrangian-relaxation/). Convexity of $\mathrm{OPT}$ in $k$ means there is no duality gap, and the monotone count turns the choice of $\lambda$ into a search on the answer.
- **From element distinctness**, as in the lower bound above.

## Applications

- **Facility placement along a line**: shops, stops or depots along a road, a river or a railway, where demand is spread over the line.
- **Optimal one-dimensional clustering and quantization.** Splitting sorted values into $k$ groups with the least total absolute deviation is the same problem, used for histograms with $k$ bins and for choosing $k$ representative values.
- **A teaching problem.** It is the classic exercise for the Monge-based speedups of dynamic programs and for the Aliens trick, since both apply cleanly.

## References
