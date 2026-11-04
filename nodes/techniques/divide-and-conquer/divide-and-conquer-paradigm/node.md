---
tag: HKZG83
kind: technique
slug: divide-and-conquer-paradigm
name: Divide and conquer
aliases:
- Divide-and-conquer
area: techniques/divide-and-conquer
level: intro
summary: A design paradigm that splits a problem into smaller subproblems, solves them recursively, and combines their solutions into a solution of the whole.
prereqs: [recursion, induction]
see_also: [decrease-and-conquer, prune-and-search, divide-and-conquer-on-queries, master-theorem, recursion-tree-method, divide-and-conquer-recurrence, merge-sort, overlapping-subproblems]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.3.1 (The divide-and-conquer method), Chapter 4 introduction (recurrences of divide-and-conquer algorithms), Chapter 26 (work, span and parallel divide and conquer)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 5, Divide and Conquer (mergesort recurrence, counting inversions, closest pair, integer multiplication, FFT)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 2, Divide-and-conquer algorithms (multiplication, recurrences, mergesort, medians, matrix multiplication, FFT)
  - book: isbn:9780132316811
    title: Anany Levitin, Introduction to the Design and Analysis of Algorithms, third edition
    locator: Chapter 5, Divide-and-Conquer
---

Divide and conquer is a way to design an algorithm: split an instance into smaller instances of the same problem, solve each of them by [recursion](/recursion/), and combine their solutions into a solution of the whole. Its running time is a [divide-and-conquer recurrence](/divide-and-conquer-recurrence/) $T(n) = aT(n/b) + f(n)$, and its correctness is a proof by strong [induction](/induction/) on the size of the instance. [Merge sort](/merge-sort/), [quicksort](/quicksort/), [Karatsuba multiplication](/karatsuba-multiplication/) and the [fast Fourier transform](/fast-fourier-transform/) are all built this way.

## In plain words

Suppose a task is too big to do in one step, but a smaller copy of the same task is easier. Cut the task into a few smaller copies. Solve each copy in the same way, which cuts it again, until the pieces are so small that the answer is obvious. Then put the answers of the pieces back together.

The method has three parts. Divide: cut the input into pieces. Conquer: solve each piece by the same method. Combine: build the answer for the whole input from the answers for the pieces.

The method is fast when the pieces are much smaller than the input, when there are not too many of them, and when the cutting and the combining are cheap. It is slow when the same piece comes up again and again, because then the same work is done many times.

## When it applies

- **The problem is self-similar.** A part of the input (half of an array, a quarter of a matrix, the points left of a line) is a smaller instance of the same problem, or of a slightly stronger problem.
- **The answer for the whole follows from the answers for the parts** plus a small amount of extra work across the boundary: the inversions with one end in each half, the subarrays that cross the middle, the pairs of points near the dividing line.
- **The subproblems are independent.** They share no work. If they overlap, use [memoization](/memoization/) or a table instead (see the pitfall on [overlapping subproblems](/overlapping-subproblems/)).
- **A simple algorithm is quadratic or worse** and you look for $n \log n$ or for a smaller exponent. Splitting into halves with a linear combine step turns $\Theta(n^2)$ pair checks into $\Theta(n \log n)$.

## The template

```pseudo id=main
SOLVE(P)                                       ▷ P an instance of size n
L1  if size(P) ≤ n₀ then                       ▷ hole: the cut-off n₀
L2      return BASE(P)                         ▷ hole: a direct method for small instances
L3  (P₁, ..., P_a) ← DIVIDE(P)                 ▷ hole: the split; each size(P_i) < size(P)
L4  for i ← 1 to a do
L5      S_i ← SOLVE(P_i)
L6  return COMBINE(P, S₁, ..., S_a)            ▷ hole: the combine step
```

There are four holes. The cut-off $n_0$ and the method BASE of lines L1 and L2 handle the small instances; often $n_0 = 1$ and the answer is trivial. The split DIVIDE of line L3 makes $a$ subproblems, often each of size about $n/b$. The step COMBINE of line L6 builds the answer of $P$ from the answers $S_1, \dots, S_a$.

**Cost.** Let $D(n)$ be the cost of line L3 and $C(n)$ the cost of line L6. If the split makes $a$ subproblems of size $n/b$, the running time satisfies

$$T(n) = \begin{cases} \Theta(1) & \text{if } n \le n_0, \\ a\,T(n/b) + D(n) + C(n) & \text{if } n > n_0, \end{cases}$$

with $f(n) = D(n) + C(n)$ in the form $aT(n/b) + f(n)$ (CLRS, Chapter 4 introduction). The sizes $n/b$ are rounded to integers in a real algorithm; the rounding does not change the order of the solution in the usual cases. To solve the recurrence, use the [master theorem](/master-theorem/), the [recursion-tree method](/recursion-tree-method/) or the [substitution method](/substitution-method/); for unequal parts, such as $T(n/5) + T(7n/10)$, use the recursion tree or the [Akra-Bazzi theorem](/akra-bazzi-theorem/). The three regimes of the master theorem tell where the work is: in the leaves (the $a^{\log_b n} = n^{\log_b a}$ base cases dominate), spread evenly over the $\log_b n$ levels, or at the root (the top combine step dominates).

**Correctness.** The proof is a strong induction on the size $n$ of the instance. Let $Q(n)$ say "SOLVE returns a correct answer for each instance of size $n$". Three facts give $Q(n)$ for every $n$:

1. *Base.* BASE is correct for each instance of size at most $n_0$.
2. *Progress.* DIVIDE returns instances of the same problem, each of size strictly less than $n$. Sizes are natural numbers, so each chain of calls is finite and the recursion stops.
3. *Combine.* If each $S_i$ is a correct answer for $P_i$, then COMBINE returns a correct answer for $P$.

For $n \le n_0$, fact 1 gives $Q(n)$. For $n > n_0$, assume $Q(m)$ for all $m < n$. By fact 2 each $P_i$ has size $m < n$, so each $S_i$ is correct by the hypothesis, and fact 3 gives $Q(n)$. The step often needs a stronger claim than the one you want: counting inversions also returns the sorted array, and the closest-pair algorithm also returns the points sorted by $y$. Put the extra output in $Q$, or the combine step has nothing to use.

## Classic examples

The list goes from simple to hard. Each line gives the recurrence and its solution.

- **[Binary search](/binary-search/).** Compare with the middle item and keep one half. $T(n) = T(n/2) + \Theta(1) = \Theta(\log n)$. There is one subproblem and no combine step, so many books call this [decrease and conquer](/decrease-and-conquer/).
- **[Merge sort](/merge-sort/).** Sort the two halves, then merge them in linear time. $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$ comparisons, which is optimal in the [comparison model](/comparison-model/) by the [comparison sort lower bound](/comparison-sort-lower-bound/).
- **[Quicksort](/quicksort/).** The work is in the divide step (the partition) and the combine step is empty. A balanced split gives $2T(n/2) + \Theta(n) = \Theta(n \log n)$; the worst split gives $T(n-1) + \Theta(n) = \Theta(n^2)$. With a random pivot the expected number of comparisons is $\Theta(n \log n)$ for every input ([randomized quicksort](/randomized-quicksort/)).
- **[Counting inversions](/counting-inversions/).** Count the inversions in each half, then count the pairs with one item in each half during the merge. $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$. For $A = [5, 2, 8, 1, 9, 3, 7, 4]$, the halves $[5, 2, 8, 1]$ and $[9, 3, 7, 4]$ have 4 inversions each. The merge of $[1, 2, 5, 8]$ and $[3, 4, 7, 9]$ finds 5 more: $(5, 3)$, $(5, 4)$, $(8, 3)$, $(8, 4)$ and $(8, 7)$. The total is 13.
- **[Maximum subarray](/maximum-subarray-divide-and-conquer/).** The best subarray is in the left half, in the right half, or crosses the middle; the crossing case takes a linear scan from the middle in each direction. $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$. [Kadane's algorithm](/kadane-algorithm/) solves the [problem](/maximum-subarray-problem/) in $\Theta(n)$, so here divide and conquer is not the best method.
- **[Karatsuba multiplication](/karatsuba-multiplication/).** Multiply two $n$-digit numbers with three products of half size instead of four. $T(n) = 3T(n/2) + \Theta(n) = \Theta(n^{\log_2 3})$, and $\log_2 3 \approx 1.585$.
- **[Strassen's algorithm](/strassen-algorithm/).** Multiply two $n \times n$ matrices with seven products of $n/2 \times n/2$ blocks instead of eight. $T(n) = 7T(n/2) + \Theta(n^2) = \Theta(n^{\log_2 7})$, and $\log_2 7 \approx 2.807$ (CLRS, Section 4.2).
- **[Closest pair of points](/closest-pair-divide-and-conquer/).** Split the points by a vertical line, solve each side, and check only the points in a strip of width $2\delta$ around the line, where $\delta$ is the best distance found so far; each point in the strip is compared with a constant number of neighbours in $y$ order. With presorting, $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$. This matches the $\Omega(n \log n)$ bound for the [closest pair problem](/closest-pair-of-points/) in the [algebraic decision tree](/algebraic-decision-tree/) model, which follows from the [element distinctness lower bound](/element-distinctness-lower-bound/).
- **[Fast Fourier transform](/fast-fourier-transform/).** Evaluate a polynomial of degree less than $n$ at the $n$-th roots of unity from its even and odd coefficients, for $n$ a power of 2. $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$ arithmetic operations. It gives [polynomial multiplication](/polynomial-multiplication/) in $\Theta(n \log n)$ operations.
- **[Median of medians](/median-of-medians/).** To select the $k$-th smallest item, find a pivot as the median of the medians of groups of 5, then recurse on one side. Up to rounding terms, $T(n) \le T(n/5) + T(7n/10) + O(n)$. Because $1/5 + 7/10 = 9/10 < 1$, the work drops by a constant factor per level of the recursion tree and $T(n) = \Theta(n)$ in the worst case.
- **Skyline.** For the [skyline problem](/skyline-problem/), compute the skyline of each half of the buildings, then merge the two skylines with one left-to-right pass over their breakpoints, as in merging sorted lists. $T(n) = 2T(n/2) + \Theta(n) = \Theta(n \log n)$. The [skyline sweep](/skyline-sweep/) reaches the same bound with a priority queue.

## Variations

- **[Decrease and conquer](/decrease-and-conquer/).** Only one subproblem is solved ($a = 1$): binary search, [exponentiation by squaring](/binary-exponentiation/), [Euclid's algorithm](/euclidean-algorithm/).
- **[Prune and search](/prune-and-search/).** Each round discards a constant fraction of the input that cannot hold the answer, and recurses on the rest. If a round costs $O(n)$, the total is $O(n)(1 + c + c^2 + \cdots) = O(n)$ for a fraction $c < 1$ that stays. [Median of medians](/median-of-medians/) and [quickselect](/quickselect/) are of this kind.
- **[Divide and conquer on queries](/divide-and-conquer-on-queries/).** Recurse over the time line of an offline sequence of updates and queries, rather than over the input items.
- **Parallel divide and conquer.** The $a$ recursive calls of line L4 are independent, so they can run at the same time in the [fork-join model](/fork-join-parallelism/). In the [work-span model](/work-span-model/) the work $T_1(n)$ follows the usual recurrence and the span follows $T_\infty(n) = T_\infty(n/b) + (\text{span of divide and combine})$. Merge sort with a serial merge has work $\Theta(n \log n)$ and span $T_\infty(n) = T_\infty(n/2) + \Theta(n) = \Theta(n)$, so its parallelism is only $\Theta(\log n)$; a [parallel merge](/parallel-merge/) shortens the combine step and gives [parallel merge sort](/parallel-merge-sort/) (CLRS, Chapter 26).
- **Unequal or many parts.** The split need not be in halves. Median of medians uses parts of sizes $n/5$ and $7n/10$; a $\sqrt{n}$-way split gives recurrences such as $T(n) = \sqrt{n}\,T(\sqrt{n}) + O(n)$.
- **Divide and conquer in a DP.** The [divide and conquer optimization](/divide-and-conquer-optimization/) computes one row of a dynamic program by recursion on the row, when the optimal split points are monotone.

## Pitfalls

- **Overlapping subproblems.** The recursion $F(n) = F(n-1) + F(n-2)$ for the [Fibonacci numbers](/fibonacci-numbers/) splits $n$ into $n-1$ and $n-2$, and these parts share almost all their subproblems. The number of calls is $C(n) = 1 + C(n-1) + C(n-2)$ with $C(0) = C(1) = 1$, whose solution is $C(n) = 2F(n+1) - 1$ (induction: $1 + (2F(n) - 1) + (2F(n-1) - 1) = 2F(n+1) - 1$). For $n = 40$ that is 331,160,281 calls to compute $F(40) = 102{,}334{,}155$. The count grows as $\phi^n$ with $\phi = (1 + \sqrt5)/2$. A table or [memoization](/memoization/) computes each $F(k)$ once, in $\Theta(n)$ additions. When the subproblems overlap, the method is dynamic programming, not divide and conquer.
- **Unbalanced splits.** The recurrence $T(n) = T(n-1) + \Theta(n)$ is $\Theta(n^2)$, not $\Theta(n \log n)$. Quicksort with the first item as the pivot hits this case on sorted input. A split into fixed fractions, even $n/10$ and $9n/10$, still gives $\Theta(n \log n)$; a split that removes only a constant number of items does not.
- **A combine step that is too costly.** With $T(n) = 2T(n/2) + \Theta(n^2)$ the root dominates and $T(n) = \Theta(n^2)$: the recursion gains nothing over a direct quadratic method. Typical causes are a merge that compares all pairs, and a closest-pair step that sorts the strip again at each level, which gives $\Theta(n \log^2 n)$ instead of $\Theta(n \log n)$.
- **Too small a base case.** Recursion down to size 1 pays the cost of a call for each tiny piece. Real code stops at a cut-off $n_0$ (often a few dozen items) and uses a simple method such as [insertion sort](/insertion-sort/) below it. The cut-off changes the constant, not the order: the $n/n_0$ base cases cost $O(n_0^2)$ each, $O(n\,n_0)$ in all.
- **Recursion depth.** The depth is the number of nested calls, about $\log_b n$ for an even split but up to $n$ for an unbalanced one. A deep recursion can overflow the call stack (Python stops at about 1000 frames by default). For quicksort, recurse on the smaller part and loop on the larger part; then the depth is at most $\log_2 n$ ([quicksort stack depth](/quicksort-stack-depth/)).
- **Subproblems that are not of the same problem.** The halves must be valid instances, with all the conditions that the algorithm needs. If the problem asks for a sorted input or for distinct keys, check that each part keeps that property, or strengthen the problem as in the correctness proof above.

## Exercises

1. Give a divide-and-conquer algorithm that finds both the minimum and the maximum of $n$ numbers, $n$ a power of 2, with $3n/2 - 2$ comparisons. Write its recurrence for the number of comparisons and solve it. (For $n = 2, 4, 8, 16$ the counts are $1, 4, 10, 22$.)
2. An item is a majority element of an array if it occurs in more than half of the positions. Show that a majority element of the whole array is a majority element of at least one half. Use this to find a majority element, or report that there is none, in $O(n \log n)$ time with equality tests only.
3. Solve $T(n) = T(n/10) + T(9n/10) + n$ with $T(1) = 1$ by a recursion tree, and show that $T(n) = \Theta(n \log n)$. Explain why the depth of the tree is $\log_{10/9} n$ on one side and $\log_{10} n$ on the other.
4. Prove that the naive recursive Fibonacci procedure makes $2F(n+1) - 1$ calls on input $n$, and that $F(n+1) \ge \phi^{n-1}$ for $n \ge 1$. Conclude that the number of calls is exponential in $n$.
5. A local minimum of an $n \times n$ grid of distinct numbers is a cell that is smaller than its (up to four) neighbours. Design a divide-and-conquer algorithm that finds a local minimum with $O(n)$ probes of the grid. (Hint: look at the middle row, the middle column and the border of the current square, and recurse into one quadrant.)

## References
