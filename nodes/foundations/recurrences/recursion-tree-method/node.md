---
tag: 7T161P
kind: technique
slug: recursion-tree-method
name: Recursion-tree method
aliases:
- recurrence tree
- tree method
area: foundations/recurrences
level: intro
summary: Expand a recurrence into a tree, sum the cost on each level, and add the levels to bound the total.
prereqs: [recurrence-relation, divide-and-conquer-recurrence, geometric-series, logarithms]
see_also: [substitution-method, iteration-method, master-theorem, watershed-function, akra-bazzi-theorem, harmonic-series]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 4.4, The recursion-tree method for solving recurrences
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 5.1, A First Recurrence, The Mergesort Algorithm (unrolling the recurrence); Section 5.2, Further Recurrence Relations
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 1, Recursion (the section on recursion trees)
---

The recursion-tree method solves a [recurrence relation](/recurrence-relation/) by drawing the tree of its recursive calls, writing the non-recursive cost of each call at its node, adding the costs of each level, and summing the levels. It turns a [divide-and-conquer recurrence](/divide-and-conquer-recurrence/) into a sum, usually a [geometric series](/geometric-series/), and shows at a glance whether the root, the leaves, or all levels together dominate the cost. The answer is a good guess; a fully rigorous solution either does the sum with exact bounds or checks the guess with the [substitution method](/substitution-method/).

## In plain words

A recursive program on a big input calls itself on smaller inputs, and those calls call themselves again. Draw each call as a box, with lines to the boxes of the calls it makes. You get a tree. In each box, write the work that the call does by itself, not counting its children.

The total work is the sum of all the numbers in the tree. To add them, go one row at a time. In a row, the calls are all of about the same size, so the row sum is easy: the number of boxes times the work per box. Then add up the rows. Often the row sums grow or shrink by a fixed factor, and then the biggest row decides the answer.

## When it applies

- Recurrences of the form $T(n) = \sum_i a_i T(n_i) + f(n)$, where the arguments $n_i$ are smaller than $n$ and the cost per node depends only on the size of the node.
- It is most useful when the costs of the levels form a simple series: geometric, constant, or a sum like $\sum 1/j$.
- It is a way to guess the answer for recurrences where no theorem applies directly, for example with unequal parts or unusual driving functions.
- It is less suited to full-history recurrences such as the average case of quicksort, where each call has a different number of children of random sizes.

## The template

For $T(n) = aT(n/b) + f(n)$ with $T(n) = \Theta(1)$ for $n < 1$:

1. **Draw the tree.** The root has size $n$ and cost $f(n)$. Each node of size $m \ge 1$ has $a$ children of size $m/b$.
2. **Describe level $j$.** It has $a^j$ nodes, each of size $n/b^j$, so the level costs $a^j f(n/b^j)$.
3. **Find the depth.** The nodes of level $j$ have size at least 1 for $j \le \lfloor \log_b n \rfloor$. The leaves are on level $\lfloor \log_b n \rfloor + 1$.
4. **Count the leaves.** There are $a^{\lfloor \log_b n \rfloor + 1} = \Theta(a^{\log_b n}) = \Theta(n^{\log_b a})$ leaves, each of cost $\Theta(1)$. This is the [watershed function](/watershed-function/).
5. **Sum.** $T(n) = \Theta(n^{\log_b a}) + \sum_{j=0}^{\lfloor \log_b n \rfloor} a^j f(n/b^j)$. Bound the sum with the formula for a geometric series, an [arithmetic series](/arithmetic-series/) or [integral bounds](/integral-bounds-for-sums/).
6. **Check.** Prove the result with the [substitution method](/substitution-method/), or note that step 5 is an exact identity for the real-valued recurrence (it is Lemma 1 in the proof of the [master theorem](/master-theorem/)) and that the sum bound is rigorous.

For unequal parts, step 2 changes: the nodes of one level have different sizes, and the levels are not all complete. Bound each level from above and below separately.

## Classic examples

### $T(n) = 3T(n/4) + cn^2$: the root dominates

Level $j$ has $3^j$ nodes of size $n/4^j$, so it costs $3^j c(n/4^j)^2 = (3/16)^j cn^2$. The level costs fall by the factor $3/16$. There are $n^{\log_4 3} \approx n^{0.792}$ leaves. So

$$T(n) \le \sum_{j \ge 0} \left(\tfrac{3}{16}\right)^j cn^2 + \Theta(n^{\log_4 3}) = \tfrac{16}{13} cn^2 + o(n^2),$$

and $T(n) \ge cn^2$ from the root alone. Hence $T(n) = \Theta(n^2)$. With $c = 1$, $T(1) = 1$ and $n = 4^k$, the exact sum is $T(n) = \frac{16}{13}n^2 - \frac{3}{13}n^{\log_4 3}$. For $n = 1024$ this is $1{,}290{,}499$, which is $1.2307 n^2$. The ratio $16/13 \approx 1.2308$ is the leading constant.

### $T(n) = 2T(n/2) + n$: all levels tie

Level $j$ has $2^j$ nodes of size $n/2^j$, so each level costs exactly $n$. There are $\lg n + 1$ levels down to size 1. With $T(1) = 1$ and $n = 2^k$: $T(n) = n\lg n + n$. This is [merge sort](/merge-sort/).

### $T(n) = 4T(n/2) + n$: the leaves dominate

Level $j$ costs $4^j(n/2^j) = 2^j n$, a series that grows by the factor 2. The last level dominates. There are $n^2$ leaves. With $T(1) = 1$ and $n = 2^k$, the sum is $n^2 + n(2^k - 1) = 2n^2 - n$, so $T(n) = \Theta(n^2)$.

### $T(n) = 2T(n/2) + n\lg n$: a slowly shrinking level cost

Level $j$ costs $2^j \cdot \frac{n}{2^j}\lg\frac{n}{2^j} = n(\lg n - j)$. The levels are not equal, but they shrink only linearly. With $n = 2^k$ and $T(1) = 1$,

$$T(n) = n + n\sum_{j=0}^{k-1}(k - j) = n + n\frac{k(k+1)}{2} = \tfrac12 n\lg^2 n + \tfrac12 n\lg n + n.$$

So $T(n) = \Theta(n\log^2 n)$. Half of the levels cost at least $n\lg n/2$ each, which is why the extra factor $\lg n$ appears.

### $T(n) = 2T(n/2) + n/\lg n$: a harmonic sum

This recurrence falls in the gap between two cases of the [master theorem](/master-theorem/), but the tree solves it. With $n = 2^m$, level $j$ for $0 \le j \le m - 1$ costs $2^j \cdot \frac{n/2^j}{\lg(n/2^j)} = \frac{n}{m - j}$. With $T(1) = 1$,

$$T(n) = n + n\sum_{j=0}^{m-1}\frac{1}{m-j} = n(1 + H_m),$$

where $H_m$ is the $m$-th [harmonic number](/harmonic-series/). Since $H_m = \ln m + O(1)$, $T(n) = \Theta(n\log\log n)$. For $n = 2^{20}$, $T(n)/n = 1 + H_{20} \approx 4.598$.

### $T(n) = T(n/3) + T(2n/3) + cn$: an unbalanced tree

The root costs $cn$. Its children have sizes $n/3$ and $2n/3$ and cost $cn$ together. Each level that is complete costs exactly $cn$, because the sizes of its nodes add up to $n$. The shortest path from the root to a leaf follows the $1/3$ branch and has length $\log_3 n$. The longest path follows the $2/3$ branch and has length $\log_{3/2} n$.

- *Lower bound.* The first $\lfloor\log_3 n\rfloor$ levels are complete, so $T(n) \ge cn\lfloor\log_3 n\rfloor = \Omega(n\log n)$.
- *Upper bound.* Each level costs at most $cn$, and there are at most $\log_{3/2} n + 1$ levels, so the internal nodes cost at most $cn(\log_{3/2} n + 1)$. The leaves need care: the tree is not complete, and its number of leaves is not $2^{\log_{3/2} n} = n^{\log_{3/2} 2} \approx n^{1.71}$. It is $\Theta(n)$. The number of leaves $L$ satisfies $L(n) = L(n/3) + L(2n/3)$, and since $\frac13 + \frac23 = 1$, the [Akra-Bazzi theorem](/akra-bazzi-theorem/) gives $L(n) = \Theta(n)$.

Hence $T(n) = \Theta(n\log n)$. The [substitution method](/substitution-method/) confirms the upper bound with the constant $c/(\lg 3 - \frac23) \approx 1.089c$ in front of $n\lg n$.

## Variations

- **Exact sums.** For the real-valued recurrence, the level sum is exact, not only a guess. The proof of the [master theorem](/master-theorem/) is a recursion tree with the three kinds of series bounded carefully.
- **Iteration.** Writing the levels as successive substitutions is the [iteration method](/iteration-method/). The tree is the same computation drawn as a picture.
- **Weighted trees.** For $T(n) = \sum a_i T(b_i n) + g(n)$, weight the node of size $m$ by $m^p$ where $\sum a_i b_i^p = 1$. Then the weights of each complete level add up to $n^p$, and the sum becomes the integral of the [Akra-Bazzi theorem](/akra-bazzi-theorem/).
- **Cost other than time.** The same tree counts stack depth (the height), the number of calls (the number of nodes), and cache misses (stop the tree when a node fits in cache).

## Pitfalls

- **Treating an unbalanced tree as complete.** In the $T(n/3) + T(2n/3)$ example, the levels below depth $\log_3 n$ are missing nodes. Their costs are at most $cn$, not exactly $cn$, and the number of leaves is $\Theta(n)$, not $n^{1.71}$.
- **Forgetting the leaves.** In $4T(n/2) + n$ the leaves are the whole answer. Always add the leaf term $\Theta(n^{\log_b a})$ before deciding which term dominates.
- **Summing to infinity when the series grows.** The bound $\sum_{j \ge 0} r^j = 1/(1 - r)$ holds only for $0 \le r < 1$. For $r > 1$ sum to the last level, where the largest term is.
- **Hiding a growing number of terms in $O$.** "Each level costs $O(n)$ and there are $\lg n$ levels" is correct, but "each level costs $O(n)$, so the total is $O(n)$" is not.
- **Calling the tree a proof without bounds.** The picture with "$\cdots$" in the middle is a guess. A proof gives an exact formula for each level, or an upper and a lower bound for each level, and a correct sum.

## Exercises

1. Use a recursion tree to solve $T(n) = T(n/2) + n^2$. (Root dominates: $\Theta(n^2)$.)
2. Solve $T(n) = 7T(n/2) + n^2$ and compare with the [Strassen algorithm](/strassen-algorithm/). (Leaves dominate: $\Theta(n^{\lg 7})$.)
3. Solve $T(n) = T(n/4) + T(3n/4) + n$, and give the shortest and the longest root-to-leaf path. (Both $\Theta(\log n)$; the answer is $\Theta(n\log n)$.)
4. Solve $T(n) = T(n - 1) + T(1) + n$ with a tree. Why is it not a divide-and-conquer recurrence? (The tree is a path; $\Theta(n^2)$.)
5. Solve $T(n) = 2T(n/2) + n\lg^2 n$ and give the exact value on powers of 2 with $T(1) = 1$. (The level sum is $n\sum_{i=1}^{k} i^2$.)

## References
