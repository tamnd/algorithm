---
tag: JT3CQS
kind: technique
slug: counting-argument
name: Counting argument
aliases:
- pigeonhole lower bound
- Shannon counting argument
area: foundations/lower-bounds
level: intro
summary: Shows a hard instance exists by comparing the number of inputs with the number of distinct algorithm behaviours.
prereqs: [lower-bound, pigeonhole-principle, logarithms]
see_also: [information-theoretic-bound, decision-tree-method, incompressibility-method, kraft-inequality, boolean-circuit, static-dictionary-lower-bound, comparison-sort-lower-bound, adversary-argument]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1 (the information-theoretic lower bound for sorting) and Section 5.3.2 (the bound lg C(m+n, m) for merging)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1, Lower bounds for sorting (Theorem 8.1, the leaves of the decision tree)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 6, Boolean circuits (Shannon's counting argument that most functions need large circuits)
  - paper: doi:10.1002/j.1538-7305.1949.tb03624.x
    title: Claude E. Shannon, The synthesis of two-terminal switching circuits, Bell System Technical Journal 28(1) (1949)
    locator: pp. 59 to 98 (the counting argument for the size of switching circuits)
---

A counting argument proves a lower bound by comparing two numbers: the number of different behaviours that an algorithm of cost at most $t$ can have, and the number of different behaviours that the problem needs. If the first number is smaller, no algorithm of cost $t$ solves the problem, so some input forces a higher cost. It is the [pigeonhole principle](/pigeonhole-principle/) applied to algorithms. Its main case is the [information-theoretic bound](/information-theoretic-bound/) for sorting, and the same idea gives Shannon's bound on circuit size, the [incompressibility method](/incompressibility-method/) and space bounds for data structures.

## In plain words

Suppose that a method may ask only a few yes or no questions. Then it can follow only a few different routes, and each route ends with one answer. If the problem has more possible answers than the method has routes, some answer is never given, and the method is wrong on some input.

So you count. Count the routes, the programs or the memory states that are possible within a budget. Count the answers, the functions or the inputs that the problem must tell apart. When the first count is the smaller one, the budget is too small. The argument says that a hard input exists. It usually does not say which input it is.

## When it applies

- The cost measure limits the number of distinct behaviours: queries with a fixed number of answers, circuits with a fixed number of gates, descriptions with a fixed number of bits, a memory with a fixed number of states.
- The problem forces many distinct behaviours: many different outputs, many functions to compute, or many inputs that must lead to different states.
- An existence result is enough. The method shows that a hard instance or a hard function exists, often that most instances are hard, and it rarely names one.

## The template

1. **Fix the budget.** Let $t$ be the cost: the number of queries, gates, bits of memory or bits of description.
2. **Bound the behaviours of cheap algorithms.** Show that the algorithms of cost at most $t$ have at most $N(t)$ distinct behaviours of the kind that matters. Typical values are $N(t) = k^t$ leaves for a tree with $k$ answers per query, $2^t$ states for $t$ bits of memory, and $2^t - 1$ strings shorter than $t$ bits.
3. **Count what the problem needs.** Show that a correct algorithm needs at least $R$ distinct behaviours. For example, inputs with different correct outputs must end at different leaves.
4. **Compare.** If $N(t) < R$, no algorithm of cost $t$ is correct. So the cost is at least the least $t$ with $N(t) \ge R$. For $N(t) = k^t$ this is $t \ge \lceil \log_k R \rceil$.
5. **Optional, most inputs are hard.** If the cheap behaviours cover at most $N(t)$ of $R$ equally likely cases, then a uniformly random case needs more than $t$ with probability at least $1 - N(t)/R$.

The count in step 2 must include all choices of the algorithm, including choices that depend on earlier answers. In a decision tree, count the leaves of the whole tree, not one path.

## Classic examples

**1. Sorting.** A comparison sort of $n$ distinct items is a binary tree, and inputs with different orders need different leaves. A tree of height $t$ has at most $2^t$ leaves, and $R = n!$. So $t \ge \lceil \lg(n!) \rceil$, which is $22$ for $n = 10$. See the [information-theoretic bound](/information-theoretic-bound/) and the [comparison sort lower bound](/comparison-sort-lower-bound/).

**2. Most orders are hard to sort.** In a binary tree the leaf depths $d(\ell)$ satisfy $\sum_\ell 2^{-d(\ell)} \le 1$, the [Kraft inequality](/kraft-inequality/). Each leaf of depth at most $t$ adds at least $2^{-t}$ to the sum, so at most $2^t$ leaves have depth at most $t$. Each order reaches its own leaf. So at most $2^t$ of the $n!$ orders are sorted with at most $t$ comparisons. For $n = 10$ and $t = 15$, that is a fraction of at most $2^{15}/10! = 0.0090$. Every comparison sort needs at least 16 comparisons on more than 99 percent of the orders of 10 items, while $\lg(10!) \approx 21.79$. In general, the fraction of orders sorted with at most $\lg(n!) - c$ comparisons is at most $2^{-c}$.

**3. Merging.** Merging two sorted lists of $n$ items each must produce one of $\binom{2n}{n}$ interleavings, so it needs at least $\lceil \lg \binom{2n}{n} \rceil$ comparisons (Knuth, Section 5.3.2). The usual merge makes $2n - 1$.

| $n$ | $\binom{2n}{n}$ | counting bound | $2n - 1$ |
|---|---|---|---|
| 3 | 20 | 5 | 5 |
| 4 | 70 | 7 | 7 |
| 5 | 252 | 8 | 9 |
| 8 | 12870 | 14 | 15 |
| 10 | 184756 | 18 | 19 |

For $n \ge 5$ the counting bound is below $2n - 1$, and an [adversary argument](/adversary-argument/) shows that $2n - 1$ is the true value ([merging lower bound](/merging-lower-bound/)). Counting is not always the strongest method.

**4. Most Boolean functions need large circuits (Shannon, 1949).** There are $2^{2^n}$ Boolean functions of $n$ inputs. A circuit with $s$ gates of fan-in 2 is fixed by choosing, for each gate $i$ in order, one of the 16 functions of two bits and two inputs among the $n$ variables and the earlier gates; the last gate is the output. So there are at most $(16 (n + s)^2)^s$ circuits with exactly $s$ gates, and at most $s \cdot (16 (n+s)^2)^s$ circuits with 1 to $s$ gates. A function with a circuit of 0 gates (a variable) also has a circuit with 1 gate (the AND of the variable with itself). Let $n \ge 5$ and $s = \lfloor 2^n/(4n) \rfloor$. Then $n + s \le 2^n$, so the base 2 logarithm of the number of circuits is at most

$$\lg s + s\,(4 + 2n) \le n + \frac{2^n}{4n}(2n + 4) = n + \frac{2^n}{2} + \frac{2^n}{n} < 2^n,$$

where the last step uses $n + 2^n/n < 2^n/2$ for $n \ge 5$. So fewer than $2^{2^n}$ functions have a circuit with at most $2^n/(4n)$ gates, and some function of $n$ inputs needs more gates. The same count shows that the fraction of such functions tends to 0 as $n$ grows. See [Boolean circuits](/boolean-circuit/). No explicit function is known that needs circuits of super-linear size.

**5. Incompressible strings.** There are $2^n$ strings of $n$ bits and only $2^n - 1$ binary strings of length less than $n$. So for each decoder, some string of $n$ bits has no shorter description. This is the base of [Kolmogorov complexity](/kolmogorov-complexity/) and of the [incompressibility method](/incompressibility-method/), which turns counting into proofs about one typical input.

**6. Memory of a one-pass algorithm.** A stream gives a set $S \subseteq \{1, \dots, m\}$ and then one query $q$, and the algorithm must answer "is $q \in S$?". After it reads $S$, its memory state must differ for any two different sets, because some $q$ is in one set and not in the other, and the rest of the run depends only on the state and $q$. There are $2^m$ sets and $2^b$ states of $b$ bits. So $b \ge m$.

**7. Space of a static set.** A data structure that stores any set of $n$ keys from a universe of $U$ keys must have a different memory image for each set. So it needs $\lceil \lg \binom{U}{n} \rceil$ bits. For $U = 2^{32}$ and $n = 10^6$ this is about $1.351 \times 10^7$ bits, or $13.5$ bits per key against 32 bits for a plain array. See the [static dictionary lower bound](/static-dictionary-lower-bound/).

## Variations

- **The information-theoretic bound.** The case where the behaviours are leaves of a decision tree and the requirement is the number of outputs. See the [information-theoretic bound](/information-theoretic-bound/).
- **Average-case counting.** Instead of counting leaves, bound the sum $\sum 2^{-d(\ell)} \le 1$ over the leaves $\ell$ (the Kraft inequality), which gives an average depth of at least $\lg R$ over $R$ equally likely cases. See the [decision tree method](/decision-tree-method/).
- **Most instances are hard.** Step 5 of the template. Shannon's argument and example 2 are of this kind.
- **Incompressibility.** Fix one incompressible input and argue about the run on it. The counting is done once, in the existence of the input. See the [incompressibility method](/incompressibility-method/).
- **Counting connected components.** In algebraic models, Ben-Or counts the connected components of the set of inputs with answer yes, and compares the count with the number of components that a tree of depth $t$ can separate. See the [Ben-Or theorem](/ben-or-theorem/).
- **Fooling sets in communication.** Pairs of inputs that must reach different transcripts are counted against the $2^c$ transcripts of $c$ bits.

### Pitfalls

- **Counting paths instead of trees.** An adaptive algorithm chooses each question from earlier answers. The behaviours to count are the leaves of the whole tree, or the whole programs, not the questions on one path.
- **Few outputs make a weak bound.** Finding the maximum has $n$ outputs, so counting gives only $\lceil \lg n \rceil$ comparisons, while the true value is $n - 1$. Element distinctness has 2 outputs, and counting gives 1. Use an [adversary argument](/adversary-argument/) or a path argument there.
- **The wrong branching factor.** A three-way comparison has 3 answers, and counting with $3^t$ gives only $\log_3(n!)$ for sorting. On distinct items the answer "equal" never occurs, so the tree is binary on these inputs. Say which answers can occur.
- **Existence is not construction.** Shannon's argument shows that hard functions exist, but it does not give one. A claim that "this function needs $2^n/(4n)$ gates" does not follow.
- **Ceilings and real logarithms.** The bound is the least integer $t$ with $N(t) \ge R$. Rounding $\lg R$ down gives a false bound.
- **The count must cover every algorithm.** In example 6, the claim needs the rest of the run to depend only on the state and $q$. If the algorithm may read the stream again, the argument fails.

## Exercises

1. Show that each comparison algorithm that finds both the maximum and the minimum of $n$ distinct items needs at least $\lceil \lg(n(n-1)) \rceil$ comparisons by counting. Compare with the true value $\lceil 3n/2 \rceil - 2$ for $n = 8$.
2. A tree with 3 answers per query must tell apart $3^{10}$ inputs. What is the least height? Show that a balanced tree reaches it.
3. Show that at most a fraction $2^{-c}$ of all strings of $n$ bits can be compressed by $c$ or more bits by a fixed decoder.
4. Prove that a comparison sort of $n$ distinct items makes at least $\lg(n!) - 1$ comparisons on at least half of the orders.
5. A stream gives $k$ distinct numbers from $\{1, \dots, m\}$ and then one query. Show that a one-pass algorithm that answers membership queries needs at least $\lceil \lg \binom{m}{k} \rceil$ bits of memory.
6. Redo Shannon's count with gates of fan-in 2 over the basis AND, OR and NOT only. How does the bound change?

## References
