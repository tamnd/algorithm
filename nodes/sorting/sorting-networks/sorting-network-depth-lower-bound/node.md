---
tag: Q4V748
kind: theorem
slug: sorting-network-depth-lower-bound
name: Sorting network depth lower bound
aliases:
- log n depth bound
area: sorting/sorting-networks
level: advanced
summary: Every sorting network on n inputs has depth at least log n, up to a constant.
prereqs: [network-depth, asymptotic-notation]
see_also: [minimum-depth-sorting-network, network-size, comparison-sort-lower-bound, aks-sorting-network, parallel-sorting-depth-lower-bound, odd-even-merge-sort]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (delay time of a network, and the bound from the number of comparators)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Section 27.1, Comparison networks (depth of a network, and the exercise on the depth of a sorting network)
  - paper: doi:10.1007/BF02579338
    title: M. Ajtai, J. Komlós and E. Szemerédi, Sorting in c log n parallel steps, Combinatorica 3(1) (1983)
    locator: pp. 1 to 19
  - paper: doi:10.1007/BF01840378
    title: M. S. Paterson, Improved sorting networks with O(log N) depth, Algorithmica 5 (1990)
    locator: pp. 75 to 92 (depth below 6100 lg n)
---

Each [sorting network](/sorting-network/) on $n$ wires has [depth](/network-depth/) at least $\lceil \lg n \rceil$, because after $t$ layers a wire depends on at most $2^t$ inputs. A second count, of [comparators](/comparator/), gives the stronger bound $\lceil \lg n! \rceil / \lfloor n/2 \rfloor$, which is $2 \lg n - O(1)$. So each sorting network has depth $\Omega(\log n)$, and the [AKS network](/aks-sorting-network/) shows that this is tight up to a constant factor.

## Statement

**Theorem.** Let $N$ be a sorting network on $n \ge 2$ wires, with depth $d$. Then

$$d \ge \lceil \lg n \rceil \qquad \text{and} \qquad d \ge \frac{\lceil \lg n! \rceil}{\lfloor n/2 \rfloor} \ge 2 \lg n - 2 \lg e.$$

In particular $d = \Omega(\log n)$, and $d(n) \ge (2 - o(1)) \lg n$ for the minimum depth $d(n)$.

## In plain words

A comparison brings together the information of two places. After one round, a place knows about at most 2 of the inputs; after two rounds, at most 4; after $t$ rounds, at most $2^t$. The place that ends with the smallest item must know about all $n$ inputs, because any of them can be the smallest. So the number of rounds is at least the number of times $n$ can be halved.

The second bound counts comparisons. Sorting needs many comparisons, but one round can do at most one comparison for each two items, so many rounds are needed.

## Proof

*The cone bound.* For a wire $w$ and $t \ge 0$, let $D_t(w)$ be the set of input wires $j$ such that the item on $w$ after $t$ layers can change when only input $j$ changes. Before any layer, $D_0(w) = \{w\}$. If layer $t$ has a comparator on wires $u$ and $v$, then the new items on $u$ and $v$ are the minimum and maximum of the old items on $u$ and $v$, so $D_t(u)$ and $D_t(v)$ are subsets of $D_{t-1}(u) \cup D_{t-1}(v)$. A wire without a comparator in layer $t$ keeps its item. By induction on $t$, $|D_t(w)| \le 2^t$.

Let $w_0$ be the first output wire, which holds the smallest item. For each input $j$, the input with a 0 at $j$ and 1 everywhere else gives 0 on $w_0$, and the input of all ones gives 1, so $j \in D_d(w_0)$. So $n \le |D_d(w_0)| \le 2^d$, and $d \ge \lceil \lg n \rceil$ because $d$ is an integer.

*The counting bound.* Let $N$ have size $s$. Run $N$ on an input that is a permutation $\pi$ of $0, 1, \ldots, n - 1$, and record for each comparator one bit: whether it exchanges its items. Given the $s$ bits, the network acts as a fixed permutation $\rho$ of the positions, so the output is $\rho$ applied to $\pi$. The output is $0, 1, \ldots, n - 1$, so $\pi$ is determined by $\rho$ and thus by the bits. Different inputs $\pi$ give different bit strings, so $n! \le 2^s$ and $s \ge \lceil \lg n! \rceil$. A layer is a set of comparators with disjoint wires, so it has at most $\lfloor n/2 \rfloor$ comparators, and $s \le d \lfloor n/2 \rfloor$. So $d \ge \lceil \lg n! \rceil / \lfloor n/2 \rfloor$.

*The asymptotic form.* From $n! \ge (n/e)^n$ we get $\lg n! \ge n \lg n - n \lg e$, and $\lfloor n/2 \rfloor \le n/2$, so

$$\frac{\lceil \lg n! \rceil}{\lfloor n/2 \rfloor} \ge \frac{n \lg n - n \lg e}{n/2} = 2 \lg n - 2 \lg e. \qquad \blacksquare$$

## Consequences

- **Depth $\Omega(\log n)$.** No sorting network, and no comparator network that finds only the minimum, is faster than $\lceil \lg n \rceil$ layers. The [minimum-depth](/minimum-depth-sorting-network/) values are larger: for example $d(16) = 9$ while the theorem gives $\max(4, \lceil 45/8 \rceil) = 6$.
- **Batcher's networks are within a factor $O(\log n)$.** [Odd-even merge sort](/odd-even-merge-sort/) and [bitonic sort](/bitonic-sort/) have depth $\tfrac12 \lg n (\lg n + 1)$ for $n = 2^k$, which is $\Theta(\log^2 n)$.
- **Size from depth.** Each sorting network of depth $d$ has size at most $d \lfloor n/2 \rfloor$. With the AKS network, this gives sorting networks of size $O(n \log n)$, which matches the [comparison sort lower bound](/comparison-sort-lower-bound/) up to a constant factor.
- **Selection and merging.** The cone bound also holds for each network whose output on one wire depends on all inputs, for example a network that computes the minimum, the median or a merge of two sequences of length $n/2$ (the middle output depends on all inputs).

## Tightness

- **Small $n$.** For $n = 2, 3, 4$ the bound $\max(\lceil \lg n \rceil, \lceil \lceil \lg n! \rceil / \lfloor n/2 \rfloor \rceil)$ is $1, 3, 3$, which equals $d(n)$. For $n = 5$ it gives 4, but $d(5) = 5$.
- **Up to a constant.** The AKS network has depth $O(\log n)$, so the bound $\Omega(\log n)$ is tight. The constant of the AKS construction is very large: Paterson's version has depth below $6100 \lg n$, far from the lower bound $2 \lg n - O(1)$.
- **The cone bound alone is weak.** The constant $1$ of the bound $\lceil \lg n \rceil$ is not tight for sorting: the counting bound gives $2 - o(1)$ for large $n$. The cone bound is tight for the minimum alone, because a tree of comparators finds the minimum in $\lceil \lg n \rceil$ layers.

## History

The cone argument and the count of comparators per layer are standard, and Knuth gives both in Section 5.3.4 of *The Art of Computer Programming*. For many years the best upper bound was the depth $\Theta(\log^2 n)$ of Batcher's networks of 1968. Ajtai, Komlós and Szemerédi closed the gap up to a constant factor in 1983 with a network of depth $O(\log n)$.

## References
