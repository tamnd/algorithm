---
tag: BH03QV
kind: technique
slug: information-theoretic-bound
name: Information-theoretic lower bound
aliases:
- information-theory lower bound
- entropy lower bound
area: foundations/lower-bounds
level: intro
summary: Counts the possible outputs; a tree of depth d has at most 2^d leaves, so depth is at least log of the output count.
prereqs: [decision-tree-model, counting-argument, logarithms]
see_also: [counting-argument, decision-tree-method, adversary-argument, comparison-sort-lower-bound, shannon-entropy, kraft-inequality, huffman-coding, merging-lower-bound]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (the information-theoretic lower bound S(n) >= ceil(lg n!) and the table of S(n)) and Section 5.3.2 (the bound for merging)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1, Lower bounds for sorting (the decision-tree model, Theorem 8.1)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.2, Mergesort (Proposition I, no compare-based algorithm sorts with fewer than lg(N!) compares)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: Chapter 5, Data Compression (the Kraft inequality and the bound of the expected length of a prefix code by the entropy)
  - paper: "Jeff Kahn and Michael Saks, Balancing poset extensions, Order 1(2) (1984)"
    locator: pp. 113 to 126 (a comparison that splits the linear extensions in a ratio between 3/11 and 8/11)
---

The information-theoretic lower bound says that an algorithm that asks questions with at most $k$ answers each, and that must be able to give $R$ different outputs, asks at least $\lceil \log_k R \rceil$ questions on some input. The reason is that a [decision tree](/decision-tree-model/) of height $h$ has at most $k^h$ leaves. With a probability distribution on the inputs, the average number of questions is at least the [entropy](/shannon-entropy/) of the output. It is the [counting argument](/counting-argument/) applied to the leaves of a tree, and it gives the bound $\lceil \lg(n!) \rceil$ for comparison sorting.

## In plain words

Each yes or no question splits the possible answers into two groups, and the reply tells you which group holds the right answer. In the worst case the reply keeps the larger group. So one question can at best cut the number of possible answers in half. To get from many possible answers down to one, you need at least as many questions as the number of times you can halve the count before it reaches one.

For sorting, the possible answers are all the orders of the items. Ten items have more than three million orders, and you must halve that number about 22 times. So every method that sorts ten items by comparing pairs needs 22 comparisons on some input. The same idea gives a bound on the average, from the entropy of the answer.

## When it applies

- The algorithm learns about the input only through queries with a bounded number $k$ of answers: comparisons, weighings on a balance, bit probes, yes or no tests.
- The problem has many outputs, or many inputs that must end at different leaves. The bound is good when $\log_k R$ is close to the cost of the best algorithm.
- The cost to bound is the number of queries, in the worst case or on average. Other work is free.

## The template

1. **Name the queries and their answers.** Fix $k$, the number of answers that **can occur** on the inputs that you use. Comparisons of distinct items have $k = 2$, even if the algorithm uses three-way comparisons.
2. **Count the outputs.** Let $R$ be the number of different correct outputs on these inputs. More generally, let $R$ be the size of a set of inputs of which no two may end at the same leaf.
3. **Worst case.** A tree of height $h$ has at most $k^h$ leaves, and each of the $R$ outputs needs its own leaf. So $k^h \ge R$ and
$$h \ge \lceil \log_k R \rceil.$$
4. **Average case.** If the input has a distribution under which output $y$ occurs with probability $p_y$, the expected number of queries is at least
$$H_k = \sum_y p_y \log_k \frac{1}{p_y}.$$
With $R$ equally likely outputs, $H_k = \log_k R$.
5. **Check tightness.** Find an algorithm and compare. If the bound is far from the algorithm, try an [adversary argument](/adversary-argument/) or a path argument of the [decision tree method](/decision-tree-method/).

**Proof of step 3.** By induction on $h$, a tree of height $h$ in which each node has at most $k$ children has at most $k^h$ leaves: a single leaf has $1 = k^0$, and a root with at most $k$ subtrees of height at most $h - 1$ has at most $k \cdot k^{h-1}$ leaves. Each output $y$ is the output of some input, whose run ends at a leaf labelled $y$. So the number of leaves is at least $R$. Then $k^h \ge R$, and $h$ is an integer. ∎

**Proof of step 4.** Let the run on input $x$ end at leaf $\ell(x)$ of depth $d(\ell)$, and let $q_\ell$ be the probability that the run ends at $\ell$. By the [Kraft inequality](/kraft-inequality/), $\sum_\ell k^{-d(\ell)} \le 1$, summed over the leaves. Over the leaves with $q_\ell > 0$, the concavity of $\log_k$ (Jensen's inequality) gives

$$\sum_\ell q_\ell\, d(\ell) - \sum_\ell q_\ell \log_k \frac{1}{q_\ell} = -\sum_\ell q_\ell \log_k \frac{k^{-d(\ell)}}{q_\ell} \ge -\log_k \sum_\ell k^{-d(\ell)} \ge 0.$$

So the expected depth is at least the entropy of the leaf. The output is a function of the leaf, and a function of a random variable has entropy at most that of the variable: each output probability $p_y$ is a sum of leaf probabilities $q_\ell$, and $\log_k(1/p_y) \le \log_k(1/q_\ell)$ for each such leaf. So the expected depth is at least $H_k$. ∎

**The adversary view.** The same bound comes from an adversary. It keeps the set $S$ of outputs that are still possible, and answers each query with the answer that keeps the largest part of $S$. Each answer keeps at least $|S|/k$ outputs. After $h$ queries at least $R/k^h$ outputs remain, and the algorithm can stop only when one remains.

## Classic examples

The table gives the bound and the true worst-case value for some problems. All bounds count queries in the worst case.

| problem | queries | $R$ | bound | true value |
|---|---|---|---|---|
| sort 10 distinct items | comparisons, $k = 2$ | $10! = 3628800$ | 22 | 22 |
| sort 12 distinct items | comparisons, $k = 2$ | $12! = 479001600$ | 29 | 30 |
| merge two sorted lists of 5 | comparisons, $k = 2$ | $\binom{10}{5} = 252$ | 8 | 9 |
| maximum of 8 items | comparisons, $k = 2$ | 8 | 3 | 7 |
| find the odd coin of 12, and if it is heavy or light | balance, $k = 3$ | 24 | 3 | 3 |
| the same for 13 coins | balance, $k = 3$ | 26 | 3 | 4 |

**Sorting.** Each order of $n$ distinct items needs its own output, so $R = n!$ and $h \ge \lceil \lg(n!) \rceil$. With [Stirling's approximation](/stirling-approximation/), $\lg(n!) = n \lg n - n \lg e + O(\log n)$. The average over the $n!$ equally likely orders is at least $\lg(n!)$ too. The bound is exact for $n \le 11$, and for $n = 12$ the true value is 30 (Knuth, Section 5.3.1). See the [comparison sort lower bound](/comparison-sort-lower-bound/) and [merge sort optimality](/merge-sort-optimality/).

**Merging.** The outputs are the $\binom{m+n}{m}$ ways to interleave two sorted lists of lengths $m$ and $n$. For $m = n$ the bound is $\lceil \lg \binom{2n}{n} \rceil = 2n - \frac12 \lg n + O(1)$, below the true value $2n - 1$ for $n \ge 5$. For $m = 1$ the bound is $\lceil \lg(n+1) \rceil$, and binary insertion meets it. See the [merging lower bound](/merging-lower-bound/).

**Search in a sorted array.** The $n + 1$ gaps where an absent key can fall must end at different leaves, and only the answers "less" and "greater" occur for absent keys, so $k = 2$ and the bound is $\lceil \lg(n+1) \rceil$. [Binary search](/binary-search/) meets it. The proof that the gaps need different leaves is on the [sorted search lower bound](/sorted-search-lower-bound/) page. A naive count with three answers and $2n + 1$ outputs gives only $\lceil \log_3(2n+1) \rceil$, which is 3 instead of 4 for $n = 8$.

**The twelve coins.** One of 12 coins is heavier or lighter than the others, and a balance compares two groups of coins with three answers. The $24$ cases need $\lceil \log_3 24 \rceil = 3$ weighings, and a known scheme of 3 weighings exists. For 13 coins the bound is still $\lceil \log_3 26 \rceil = 3$, but 3 weighings are not enough. Suppose that the first weighing puts $j$ coins on each pan. If it tips, $2j$ cases remain for two weighings, which can separate at most $9$, so $j \le 4$. If it balances, the $13 - 2j$ coins that were not weighed give $2(13 - 2j)$ cases, so $13 - 2j \le 4$ and $j \ge 5$. Both cannot hold. So the bound is not always reached, even when $k^h$ is larger than $R$.

**Average search with unequal probabilities.** If the keys of a search have probabilities $\frac12, \frac14, \frac18, \frac1{16}, \frac1{16}$, the entropy is $1.875$ bits, so each strategy of yes or no questions needs at least $1.875$ questions on average. A [Huffman code](/huffman-coding/) of the keys gives a strategy with exactly $1.875$ when the questions may be arbitrary subsets. With comparisons only, the bound still holds, and an optimal search tree comes close.

## Variations

- **$k$-way queries.** A balance or a three-way comparison with equal keys gives $\log_3$. Bit probes of a word of $w$ bits read as one query give $k = 2^w$ and $\log_{2^w} R = \lg R / w$.
- **Inputs instead of outputs.** For decision problems, $R = 2$ and the bound is useless. Sometimes one can still find many inputs that must end at different leaves, as for [element distinctness](/element-distinctness/): each order of distinct items needs its own leaf. This is the [decision tree method](/decision-tree-method/).
- **Entropy of partial information.** When some order is already known, the outputs are the linear extensions of a partial order $P$, and the bound is $\lceil \lg e(P) \rceil$. Kahn and Saks (1984) proved that a comparison is always available that splits the linear extensions in a ratio of at most about $8/11$, so sorting with partial information takes $O(\log e(P))$ comparisons.
- **Lower bounds for data structures.** A structure that must distinguish $R$ sets needs $\lceil \lg R \rceil$ bits. See the [static dictionary lower bound](/static-dictionary-lower-bound/).

### Pitfalls

- **Counting answers that cannot occur.** Three-way comparisons on distinct keys never answer "equal". Using $k = 3$ gives a weaker bound than the true one.
- **Few outputs.** The maximum of $n$ items has $n$ outputs and needs $n - 1$ comparisons, not $\lceil \lg n \rceil$. A decision problem has 2 outputs. The information bound is then far too weak, and the work is in an adversary or path argument.
- **Reading the bound as an algorithm.** $\lceil \log_k R \rceil$ is a lower bound. A tree that reaches it may not exist, as the 13 coins and the 12 items show.
- **Rounding.** Take the ceiling of the real logarithm. $\lfloor \lg(12!) \rfloor = 28$ is not a valid bound statement for a worst case of 29.
- **Model.** The bound is on the number of queries of the named kind. [Radix sort](/radix-sort/) reads digits, not comparisons, and is not bound by $\lg(n!)$.

## Exercises

1. Prove that each comparison algorithm that finds the maximum and the minimum of $n$ distinct items needs at least $\lceil \lg(n(n-1)) \rceil$ comparisons. For which $n$ is this the true value $\lceil 3n/2 \rceil - 2$?
2. Show that $\lceil \lg \binom{2n}{n} \rceil \ge 2n - \lceil \frac12 \lg n \rceil - 1$ for $n \ge 1$, from $\binom{2n}{n} \ge 4^n/(2\sqrt{n})$.
3. Find a scheme of 3 weighings for the twelve coins.
4. With one extra coin that is known to be genuine, show that 13 coins can be done in 3 weighings, and that the count $26 \le 27$ allows it.
5. Prove that the expected number of comparisons of every comparison sort on a uniformly random order of $n$ distinct items is at least $\lg(n!)$.
6. A sorted array of $n$ items is searched for a key that is in the array with probability $p_i$ at position $i$ and never absent. Give the information-theoretic lower bound on the expected number of three-way comparisons.

## References
