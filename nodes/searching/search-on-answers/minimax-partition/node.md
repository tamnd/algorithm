---
tag: PJXEQV
kind: problem
slug: minimax-partition
name: Linear partition (minimize the maximum block sum)
aliases:
- painter's partition problem
- book allocation problem
- minimum largest-sum split
- split array largest sum
area: searching/search-on-answers
level: core
summary: Split an array into k contiguous blocks so that the largest block sum is as small as possible.
model: word-ram
complexity:
  vars: {n: the number of items, S: the sum of the items}
  time: {worst: O(n log n)}
prereqs: [binary-search-on-answer, greedy-algorithm, prefix-sums]
see_also: [binary-search-on-answer, maximin-placement, optimization-to-decision-reduction, sorted-matrix-selection, makespan-minimization, load-balancing-problem, partition-problem, optimal-substructure]
sources:
  - url: https://leetcode.com/problems/split-array-largest-sum/
    title: LeetCode 410, Split Array Largest Sum
  - book: isbn:9781848000698
    title: Steven S. Skiena, The Algorithm Design Manual, second edition, Springer, 2008
    locator: Section 8.5, The Partition Problem (the dynamic program for linear partition)
  - paper: doi:10.1016/j.jpdc.2004.05.003
    title: "Ali Pinar and Cevdet Aykanat, Fast optimal load balancing algorithms for 1D partitioning, Journal of Parallel and Distributed Computing 64(8) (2004), 974-996"
    note: the chains-on-chains partitioning problem and its exact algorithms
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 4.3.2, Finding Optimal Solutions
---

Linear partition splits a sequence of $n$ non-negative numbers into at most $k$ contiguous blocks so that the largest block sum is as small as possible. The decision question "is there a split with all block sums at most $t$?" is answered by a greedy pass in $O(n)$ time, and its answers are false then true in $t$, so [binary search on the answer](/binary-search-on-answer/) solves the problem in $O(n \log S)$ time for integer items with sum $S$. A dynamic program solves it in $O(kn^2)$ time, and a search over the $O(n^2)$ possible block sums by [sorted-matrix selection](/sorted-matrix-selection/) gives $O(n \log n)$ for any real items. In parallel computing it is the chains-on-chains partitioning problem, the balance of a chain of tasks over a chain of processors.

## In plain words

A row of books must go to $k$ readers. Each reader gets a run of books that stand next to each other, and the order cannot change. You want the reader with the most pages to have as few pages as possible.

Guess a limit on the pages. Give books to the first reader from the left until the next book would pass the limit, then start the next reader. If this uses at most $k$ readers, the limit works. A higher limit also works, and a lower one may not. So the best limit is the place where "does not work" turns into "works", and you find it by halving the range of limits again and again.

## Definition

**Input.** Non-negative numbers $a_1, \ldots, a_n$ and an integer $k \ge 1$.

**Output.** Indices $0 = i_0 < i_1 < \cdots < i_j = n$ with $j \le k$, which define the blocks $a_{i_{r-1}+1}, \ldots, a_{i_r}$, that minimize the largest block sum

$$\max_{1 \le r \le j} \sum_{i = i_{r-1}+1}^{i_r} a_i,$$

and the optimal value $\mathrm{OPT}$. With prefix sums $P_0 = 0$ and $P_i = a_1 + \cdots + a_i$, the block sums are the differences $P_{i_r} - P_{i_{r-1}}$.

**At most $k$ or exactly $k$.** For $n \ge k$, the two versions have the same optimum: a split into fewer than $k$ blocks can be refined by cutting a block with at least two items, which does not increase any block sum because the items are non-negative.

**Decision version.** $\mathrm{FEASIBLE}(t)$: is there a split into at most $k$ blocks with all block sums at most $t$? A split that works for $t$ works for each $t' \ge t$, so this is a [monotone predicate](/monotone-predicate/), and $\mathrm{FEASIBLE}(t)$ holds if and only if $t \ge \mathrm{OPT}$.

**Simple bounds.** $\max_i a_i \le \mathrm{OPT} \le S$, and also $\mathrm{OPT} \ge S/k$ and $\mathrm{OPT} \le S/k + \max_i a_i$. The last bound comes from the greedy split at the limit $S/k + \max_i a_i$: each block except the last has a sum above $S/k$, so there are at most $k$ blocks.

## Variants

- **The painter's partition.** Boards of lengths $a_i$ are painted by $k$ painters, each painting a contiguous run, at one unit of time per unit of length; the time is the largest block sum.
- **Book allocation.** Each of $k$ students must get at least one book, so exactly $k$ non-empty blocks are required; this is the same problem when $n \ge k$.
- **Maximize the minimum block.** Split into exactly $k$ blocks so that the smallest block sum is as large as possible. The greedy test closes a block as soon as its sum reaches $t$, and the answer is the largest feasible $t$.
- **Other costs per block.** If the cost of a block is any non-decreasing function of the block, such as the sum of squares or the time of a processor with a setup cost, the same greedy test and search apply. If the objective is the sum of the block costs instead of the maximum, the problem needs a dynamic program, sped up by the [Knuth optimization](/knuth-optimization/) or the [divide and conquer optimization](/divide-and-conquer-optimization/) when the cost is Monge.
- **Without the order.** If the items may be assigned to blocks in any order, the problem becomes [makespan minimization](/makespan-minimization/) on identical machines, which is NP-hard; for $k = 2$ its decision form contains the [partition problem](/partition-problem/).

## Examples

**Split array largest sum.** For $a = (7, 2, 5, 10, 8)$ and $k = 2$, the best split is $(7, 2, 5 \mid 10, 8)$, with sums $14$ and $18$, so $\mathrm{OPT} = 18$. The smallest-feasible search on $[\max a, S] = [10, 32]$ runs:

| lo | hi | t | greedy blocks | feasible |
|---|---|---|---|---|
| 10 | 32 | 21 | (7, 2, 5), (10, 8) | yes |
| 10 | 21 | 15 | (7, 2, 5), (10), (8) | no |
| 16 | 21 | 18 | (7, 2, 5), (10, 8) | yes |
| 16 | 18 | 17 | (7, 2, 5), (10), (8) | no |

It returns $18$ after 4 tests, within $\lceil \lg 23 \rceil = 5$.

**Equal items.** For $n$ items of size $1$, $\mathrm{OPT} = \lceil n/k \rceil$.

**One large item.** For $a = (1, 1, 20, 1, 1)$ and $k = 3$, $\mathrm{OPT} = 20$, the largest item; the lower bound $\max_i a_i$ is tight.

## Known algorithms

**The greedy test.** Scan from the left, add each item to the current block while the sum stays at most $t$, and start a new block otherwise. Answer yes if $t \ge \max_i a_i$ and at most $k$ blocks are used. It runs in $O(n)$ time.

*Proof that the greedy test is exact.* If it answers yes, its split is a witness. Conversely, suppose some split into $j \le k$ blocks has all sums at most $t$, with ends $e_1 < \cdots < e_j = n$, and let the greedy blocks end at $g_1 < g_2 < \cdots$. We show by induction that $g_r \ge e_r$ while both exist, so the greedy uses at most $j$ blocks. For $r = 1$, the items $a_1, \ldots, a_{e_1}$ have sum at most $t$, and the greedy keeps adding while the sum is at most $t$, so $g_1 \ge e_1$. If $g_r \ge e_r$, then the greedy's block $r + 1$ starts at $g_r + 1 \ge e_r + 1$, and the items from there to $e_{r+1}$ are a part of the solution's block $r + 1$, so their sum is at most $t$ because the items are non-negative. So $g_{r+1} \ge e_{r+1}$, or the greedy has already reached $n$. $\square$ Without the check $t \ge \max_i a_i$ the test is wrong; the page on [binary search on the answer](/binary-search-on-answer/) gives an example.

**Binary search on the answer.** For integer items, a smallest-feasible search over $[\max_i a_i, S]$ makes $\lceil \lg(S - \max_i a_i + 1) \rceil$ tests, so the total is $O(n \log S)$. With the bounds $S/k \le \mathrm{OPT} \le S/k + \max_i a_i$, the range has length at most $\max_i a_i + 1$, and the search makes $O(\log \max_i a_i)$ tests.

**Dynamic programming.** Let $M[j][i]$ be the optimum for the first $i$ items in at most $j$ blocks. Then $M[1][i] = P_i$ and

$$M[j][i] = \min_{0 \le l \le i} \max\big(M[j-1][l],\ P_i - P_l\big).$$

This takes $O(kn^2)$ time and is the method of Skiena's book. It has [optimal substructure](/optimal-substructure/) because the last block and the best split of the rest are independent. Since $M[j-1][l]$ is non-decreasing in $l$ and $P_i - P_l$ is non-increasing in $l$, the best $l$ for each $i$ can be found by a binary search, which gives $O(kn \log n)$.

**Search over the candidates.** $\mathrm{OPT}$ is a block sum, so it is one of the differences $P_j - P_i$ with $i < j$. In the matrix $M[i][j] = P_j - P_i$ the rows are non-decreasing and the columns non-increasing. A binary search on the rank of the candidate, with each candidate found by [sorted-matrix selection](/sorted-matrix-selection/) in $O(n)$ time and tested by the greedy in $O(n)$ time, takes $O(n \log n)$ time for real items, with no dependence on $S$.

**Faster tests.** With prefix sums, the greedy can find the end of each block by a binary search on $P$, in $O(k \log n)$ time per test instead of $O(n)$. Pinar and Aykanat survey and compare the exact algorithms built from such probes for the chains-on-chains problem.

## Bounds

- **Upper bound.** $O(n \log n)$ for real items by the candidate search, and $O(n \log S)$ for integer items by the simple search.
- **Lower bound.** $\Omega(n)$ in any model: an algorithm that does not read some item cannot tell whether it is huge. Algorithms that get close to linear time are known for this problem; their exact bounds are not given here.
- **Number of tests.** For integer answers in a range of size $R$, any method that only uses the decision test needs $\lceil \lg R \rceil$ tests in the worst case, since each test has two outcomes.

## Reductions

- **To a monotone decision.** The problem reduces to $O(\log S)$ or $O(\log n)$ greedy tests, as above. This is the [optimization-to-decision reduction](/optimization-to-decision-reduction/) for a minimization.
- **From the unordered version.** Makespan minimization with $k$ machines is linear partition over the best order of the items, so the order is what makes linear partition easy.
- **A special case of tree partitioning.** A sequence is a path, and splitting a tree into $k$ connected parts with the smallest largest weight generalizes the problem; on trees the decision test is again a greedy, which works from the leaves upward and cuts off the heaviest child parts first.

## Applications

- **Load balancing on a chain.** In parallel computing, a sequence of tasks with costs is split among $k$ processors that each take a contiguous part, to keep data local; the time of the step is the largest part. This is the chains-on-chains problem of Pinar and Aykanat, and a form of the [load balancing problem](/load-balancing-problem/).
- **Dividing work among people.** Books among readers, boards among painters, or a long text among translators, when each gets a contiguous run.
- **Batch processing.** A stream of jobs in a fixed order is cut into $k$ batches with a limit on the largest batch.

## References
