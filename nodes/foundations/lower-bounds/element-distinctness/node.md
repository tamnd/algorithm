---
tag: 30GVXH
kind: problem
slug: element-distinctness
name: Element distinctness
aliases:
- Element distinctness problem
- collision finding
- distinctness problem
- element uniqueness
area: foundations/lower-bounds
level: core
summary: Decide whether n given elements are all distinct.
prereqs: [comparison-model, decision-tree-method, sorting-problem]
see_also: [element-distinctness-lower-bound, ben-or-theorem, decision-tree-method, closest-pair-lower-bound, hash-table, ambainis-element-distinctness, k-distinctness, collision-finding]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1, Lower bounds for sorting (the decision-tree model) and Chapter 11, Hash tables (expected constant time per operation with universal hashing)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.1, Minimum-comparison sorting (the values S(n) and the bound ceil(lg n!))
  - paper: doi:10.1145/800061.808735
    title: Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983)
    locator: pp. 80 to 86 (the bound Omega(n log n) for element distinctness in algebraic computation trees)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (element uniqueness and the reductions to closest pair)
  - paper: doi:10.1137/S0097539705447311
    title: Andris Ambainis, Quantum walk algorithm for element distinctness, SIAM Journal on Computing 37(1) (2007)
    locator: pp. 210 to 239 (the quantum algorithm with O(n^(2/3)) queries)
  - paper: doi:10.1145/1008731.1008735
    title: Scott Aaronson and Yaoyun Shi, Quantum lower bounds for the collision and the element distinctness problems, Journal of the ACM 51(4) (2004)
    locator: pp. 595 to 605 (the quantum lower bound Omega(n^(2/3)) for element distinctness)
---

Element distinctness is the problem of deciding whether $n$ given items are pairwise different. It has only two answers, but in the [comparison model](/comparison-model/) it is exactly as hard as sorting, $\lceil \lg(n!) \rceil$ comparisons or more, and in [algebraic computation trees](/algebraic-computation-tree/) it needs $\Omega(n \log n)$ steps by the [Ben-Or theorem](/ben-or-theorem/). With [hashing](/hash-table/) it takes $O(n)$ expected time, and a quantum algorithm needs only $\Theta(n^{2/3})$ queries. It is the standard source of $\Omega(n \log n)$ lower bounds by reduction, for example for the [closest pair](/closest-pair-lower-bound/) of points.

## In plain words

You have a list of items and you want to know whether any item appears twice. The answer is only yes or no, so it looks easy. But a method that may only compare items, and learn which is larger or whether they are equal, must in the worst case do as much work as putting the whole list in order. The reason is that two items that would be next to each other in order look almost the same to the method, and it must compare them to be sure they differ.

Other tools change the cost. If you can put each item into a bucket chosen by a random rule, you look only at items that land in the same bucket, and on average this is fast. A quantum computer can do better still. So the cost depends on what the method may do.

## Definition

**Input.** Items $x_1, \dots, x_n$ from a set $U$ with equality, and usually with a total order.

**Output.** "Yes" if $x_i \ne x_j$ for all $i \ne j$, and "no" otherwise.

**Search version.** If the answer is "no", also output a pair $i < j$ with $x_i = x_j$.

The cost depends on the model: comparisons with three answers ($<$, $=$, $>$) in the comparison model, tests of equality only, arithmetic and comparisons on real numbers in an algebraic computation tree, word operations and random bits on the [word RAM](/word-ram/), or queries to the input in the quantum query model.

## Variants

- **Counting distinct values.** Output the number of different values. Element distinctness asks whether this number is $n$.
- **[$k$-distinctness](/k-distinctness/).** Decide whether some value appears at least $k$ times.
- **Small universes.** If $U = \{1, \dots, m\}$ with $m < n$, the answer is "no" by the [pigeonhole principle](/pigeonhole-principle/). With $m = O(n)$, an array of $m$ flags solves the problem in $O(n + m)$ time.
- **The collision problem.** The input is promised to be either one-to-one or two-to-one, and the task is to tell which. This is easier than element distinctness, and it is the core of [collision finding](/collision-finding/) for hash functions.
- **Equality tests only.** The items can be tested for equality but not ordered, for example records with no key order.
- **Real numbers.** In algebraic models the inputs are real numbers, and arithmetic is allowed. The integer version is the same problem with inputs restricted to integers.

## Examples

- $(3, 1, 4, 1, 5)$: the answer is "no", with the pair $(2, 4)$, since $x_2 = x_4 = 1$.
- $(2, 7, 1, 8)$: the answer is "yes". In sorted order $1 < 2 < 7 < 8$ each pair of neighbours differs.
- $n$ random values from $\{1, \dots, m\}$: by the [birthday paradox](/birthday-paradox/), a repeat has probability about $1/2$ when $n$ is about $1.18\sqrt{m}$, so for $m = 365$ already $n = 23$ items give a repeat more often than not.

## Known algorithms

| method | model | cost |
|---|---|---|
| compare all pairs | equality tests | $n(n-1)/2$ tests |
| sort, then compare neighbours | comparisons | $O(n \log n)$; the minimum is $S(n)$ comparisons |
| hash table | word RAM with random bits | $O(n)$ expected time |
| array of flags | integers in $\{1, \dots, m\}$ | $O(n + m)$ time |
| [radix sort](/radix-sort/), then compare neighbours | word RAM, integers of $O(\log n)$ bits | $O(n)$ time |
| [Ambainis's quantum walk](/ambainis-element-distinctness/) | quantum queries | $O(n^{2/3})$ queries |

**Sort and scan.** Sort the items, then compare each item with the next. Two equal items are next to each other after sorting, so a repeat exists if and only if some neighbours are equal. With a sort by three-way comparisons, stop as soon as some comparison answers "equal".

**Hashing.** Insert the items one by one into a [hash table](/hash-table/) with [universal hashing](/universal-hashing/), and stop when an item is already present. Each operation takes $O(1)$ expected time, so the whole run takes $O(n)$ expected time.

## Bounds

**Comparisons with three answers: exactly $S(n)$.** Let $S(n)$ be the least worst-case number of comparisons of a sort of $n$ distinct keys, so $S(n) \ge \lceil \lg(n!) \rceil$.

*Lower bound.* Let $T$ be a comparison tree that decides element distinctness, and let $x$ be an input of distinct keys. Its path must compare each two keys that are neighbours in sorted order. If it does not compare $x_a$ and $x_b$, where $x_b$ is the next larger key after $x_a$, set $x_b$ equal to $x_a$. Each other comparison on the path keeps its answer, since no key lies strictly between $x_a$ and $x_b$. So the changed input reaches the same leaf "yes", but it has a repeat. So the path of each input of distinct keys fixes its sorted order, and inputs with different orders reach different leaves along answers "$<$" and "$>$" only. So $T$, restricted to inputs of distinct keys, is a sorting tree, and its height is at least $S(n) \ge \lceil \lg(n!) \rceil$. This is the path argument of the [decision tree method](/decision-tree-method/).

*Upper bound.* Run an optimal sorting tree for distinct keys, and answer "no" as soon as a comparison answers "equal". If the run ends with no answer "equal", it ends at a leaf of some order $\sigma$. Some input of distinct keys in order $\sigma$ reaches this leaf, and by the argument above its path compares each two neighbours in $\sigma$. The run on $x$ follows the same path with the same strict answers, so the keys of $x$ are strictly increasing in the order $\sigma$, and they are distinct. This takes at most $S(n)$ comparisons.

So, in this model, element distinctness costs exactly $S(n)$ comparisons, the same as sorting. For $n = 8$ that is 16, and for $n = 10^6$ it is at least $\lceil \lg(10^6!) \rceil = 18488885$.

**Equality tests only: exactly $n(n-1)/2$.** An adversary answers "not equal" to every test. If a pair $(i, j)$ is never tested, take distinct values and then set $x_j = x_i$: every test answer stays true, since a test of $j$ against $k \ne i$ compares $x_i$ with $x_k$. So an algorithm that stops before testing all pairs is wrong on one of the two inputs. Testing all pairs meets the bound. For $n = 10^6$ this is $499999500000$ tests.

**Algebraic computation trees: $\Theta(n \log n)$.** The set of inputs in $\mathbb{R}^n$ with answer "yes" has $n!$ connected components, one for each order. Ben-Or (1983) proved that if an algebraic computation tree of height $h$ decides a set with $N$ connected components, then $h = \Omega(\log N - n)$. With $N = n!$ this gives height $\Omega(n \log n)$, even when the tree may add, multiply, divide and compare real numbers. Sorting gives the matching upper bound. See the [element distinctness lower bound](/element-distinctness-lower-bound/) and the [Ben-Or theorem](/ben-or-theorem/).

**Word RAM with random bits: $\Theta(n)$ expected.** Hashing reads each item once, and every algorithm must read all items, since changing any one item to equal another changes the answer. The lower bound of the algebraic model does not apply, because a hash function uses the bits of a key and not only comparisons and arithmetic.

**Quantum queries: $\Theta(n^{2/3})$.** Ambainis gave a quantum walk that uses $O(n^{2/3})$ queries, and Aaronson and Shi proved that $\Omega(n^{2/3})$ queries are necessary when the range of values is large enough.

| model | bound | $n = 10^6$ |
|---|---|---|
| equality tests | $n(n-1)/2$ | $499999500000$ |
| three-way comparisons | $S(n) \ge \lceil \lg(n!) \rceil$ | $\ge 18488885$ |
| algebraic computation tree | $\Theta(n \log n)$ | about $2 \cdot 10^7$ up to a constant |
| word RAM, hashing | $\Theta(n)$ expected | about $10^6$ up to a constant |
| quantum queries | $\Theta(n^{2/3})$ | $10^4$ up to a constant |

## Reductions

- **To sorting.** Sort, then compare neighbours. So any sorting algorithm gives an algorithm for element distinctness with $n - 1$ more comparisons, and a lower bound for element distinctness is a lower bound for sorting.
- **To closest pair.** The items are distinct if and only if the closest pair of the points $x_1, \dots, x_n$ on the real line has distance greater than 0. So the $\Omega(n \log n)$ bound carries over to the [closest pair](/closest-pair-lower-bound/) problem in algebraic computation trees. The same idea gives bounds for the Euclidean minimum spanning tree and for other proximity problems (Preparata and Shamos, Chapter 5).
- **To counting distinct values.** The items are distinct if and only if the number of distinct values is $n$.
- **From set disjointness.** Two sets $A$ and $B$, each without repeats, are disjoint if and only if the list $A$ followed by $B$ has no repeat. So a lower bound for disjointness, for example from communication complexity, is also a lower bound for element distinctness.

### Pitfalls

- **Two answers do not mean a small bound.** Leaf counting gives only 1 comparison, because there are two outputs. The true bound needs the path argument above.
- **The model decides the answer.** $\Omega(n \log n)$ holds for comparisons and algebraic trees, not for hashing on the word RAM. A claim that "element distinctness needs $n \log n$ time" must name the model.
- **Expected versus worst case.** Hashing gives $O(n)$ expected time. Its worst case on a bad input for a fixed hash function is $\Theta(n^2)$.
- **The integer version.** The count of connected components is for real inputs. For integer inputs the argument needs more care, and with the floor function or bit operations the bound does not hold, since radix sort then runs in linear time on small integers. See the [element distinctness lower bound](/element-distinctness-lower-bound/) for the integer case.

## Applications

- **Data checks.** Testing that a key column of a table has no repeats, that a list of identifiers is unique, or that a file system has no two files with the same name in a folder.
- **Duplicate removal.** Databases implement DISTINCT by sorting or by hashing, the two algorithms above. On a sorted array the repeats are removed in one pass ([remove duplicates from a sorted array](/remove-duplicates-from-sorted-array/)).
- **Lower bounds.** It is the base problem for $\Omega(n \log n)$ bounds in computational geometry, through reductions to closest pair, convex hull and related problems ([convex hull lower bound](/convex-hull-lower-bound/)).
- **Cryptography.** Finding a collision of a hash function is the search version on the values $h(1), h(2), \dots$, and the birthday bound $\Theta(\sqrt{m})$ for $m$ output values is the reason that hash outputs need $2b$ bits for $b$ bits of security.

## References
