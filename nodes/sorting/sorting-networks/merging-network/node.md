---
tag: RHH058
kind: definition
slug: merging-network
name: Merging network
aliases:
- Batcher merging network
area: sorting/sorting-networks
level: core
summary: A comparator network that merges two sorted input sequences into one sorted output.
prereqs: [sorting-network, zero-one-principle]
see_also: [odd-even-merge-sort, bitonic-merger, merging-sorted-lists, merging-lower-bound, bitonic-sort, network-depth]
sources:
  - paper: doi:10.1145/1468075.1468121
    title: K. E. Batcher, Sorting networks and their applications, AFIPS Spring Joint Computer Conference 32 (1968)
    locator: pp. 307 to 314 (the odd-even merge and the bitonic merge)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (merging networks, Batcher's merge and Floyd's lower bound)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Section 27.4, A merging network
  - paper: doi:10.1145/227595.227693
    title: Peter Bro Miltersen, Mike Paterson and Jun Tarui, The asymptotic complexity of merging networks, Journal of the ACM 43(1) (1996)
    locator: pp. 147 to 165 (the lower bound M(n, n) ≥ n lg n − O(n))
---

A merging network is a comparator network on $p + q$ wires that outputs a sorted sequence whenever the first $p$ inputs are sorted and the last $q$ inputs are sorted. It is the network form of [merging two sorted lists](/merging-sorted-lists/), and it is the step that Batcher's sorting networks repeat: [odd-even merge sort](/odd-even-merge-sort/) and [bitonic sort](/bitonic-sort/) are merge sorts whose merge is a merging network. Batcher's odd-even merge of two lists of $n$ items each has $n \lg n + O(n)$ [comparators](/comparator/) and depth $\lg(2n)$, and both numbers are optimal up to lower-order terms.

## Definition

Let $p, q \ge 1$. A comparator network $N$ on the wires $0, \ldots, p + q - 1$ is a *$(p, q)$-merging network* when, for each input $x$ over a totally ordered set with

$$x_0 \le x_1 \le \cdots \le x_{p-1} \quad \text{and} \quad x_p \le x_{p+1} \le \cdots \le x_{p+q-1},$$

the output $N(x)$ is sorted. On inputs that do not satisfy this condition, nothing is required. Write $M(p, q)$ for the smallest size of a $(p, q)$-merging network.

**The zero-one principle for merging.** A network is a $(p, q)$-merging network if and only if it merges each 0-1 input of this form. The proof of the [zero-one principle](/zero-one-principle/) works without change, because a non-decreasing map sends sorted sequences to sorted sequences. There are only $(p + 1)(q + 1)$ such 0-1 inputs, $0^a 1^{p-a} 0^b 1^{q-b}$ for $0 \le a \le p$ and $0 \le b \le q$. So a merging network on $n$ wires can be checked with $O(n^2)$ inputs, while a sorting network needs $2^n$.

**Two kinds of merger.**

- *Batcher's odd-even merge* merges the items at even places of both lists, merges the items at odd places of both lists, and then compares places $2t + 1$ and $2t + 2$. For two lists of $2^{k-1}$ items it has $2^{k-1}(k - 1) + 1$ comparators and depth $k$.
- The *[bitonic merger](/bitonic-merger/)* sorts each bitonic sequence. A sorted list followed by the reverse of a sorted list is bitonic. So with its first layer changed to compare $t$ with $n - 1 - t$, it merges two sorted lists. For $n = 2^k$ wires it has $2^{k-1} k$ comparators and depth $k$.

**Lower bounds.** Let $n = p + q$.

- *Depth.* For $p = q$, each merging network has depth at least $\lceil \lg n \rceil$. The item on a wire after $d$ layers is one of at most $2^d$ inputs. The output at place $p$ can be any input: $x_i$ with $i < p$ is there when exactly $p - i$ items of the second list are below it, and in the same way for the second list. So $2^d \ge n$.
- *Size.* Floyd proved a lower bound of the form $M(n, n) \ge \tfrac12 n \lg n - O(n)$ (Knuth, Section 5.3.4). Miltersen, Paterson and Tarui raised it to $M(n, n) \ge n \lg n - O(n)$ in 1996. Batcher's odd-even merge gives $M(n, n) \le n \lg n + O(n)$, so it is optimal up to the $O(n)$ term.
- *Against comparisons.* An adaptive algorithm in the [comparison model](/comparison-model/) merges two lists of $n$ items with $2n - 1$ comparisons. A merging network needs $\Theta(n \log n)$ comparators, because it can not choose its comparisons. See the [merging lower bound](/merging-lower-bound/) for the adaptive case.

## Examples and non-examples

**Examples.**

- $M(1, 1) = 1$: the single comparator $[0{:}1]$.
- The $(2, 2)$-merging network $[0{:}2], [1{:}3], [1{:}2]$ is Batcher's odd-even merge for four wires. On $(2, 7, 1, 5)$ it gives $(1, 7, 2, 5)$, then $(1, 5, 2, 7)$, then $(1, 2, 5, 7)$. It has 3 comparators and depth 2.
- A $(1, q)$-merging network is the insertion of one item into a sorted list: $[0{:}1], [1{:}2], \ldots, [q - 1{:}q]$, with the single item on wire 0. It has $q$ comparators, and $M(1, q) = q$: if the single item is the largest, every wire must change its item, so the comparators must connect all $q + 1$ wires.
- In [odd-even merge sort](/odd-even-merge-sort/) on $2^k$ wires, the last merge has $2^{k-1}(k - 1) + 1$ comparators. For $n = 8$ it has 9 of the 19 comparators.

**Non-examples.**

- The layer $[0{:}2], [1{:}3]$ alone is not a $(2, 2)$-merging network. On the 0-1 input $(0, 1, 0, 1)$ it gives $(0, 1, 0, 1)$, which is not sorted. The last comparator $[1{:}2]$ is needed.
- The bitonic merger with its usual first layer $[t : t + n/2]$ is not a merging network for two lists in the same direction. On $(1, 3, 2, 4)$ it outputs $(1, 3, 2, 4)$. It merges only when the second list is reversed.
- A merging network is not a sorting network in general. The $(2, 2)$-merging network above does not sort $(2, 1, 4, 3)$: it outputs $(2, 1, 4, 3)$ unchanged.

## Related definitions

- [Sorting network](/sorting-network/): a network that sorts each input. A sort of $2^k$ items can be built from $k$ levels of merging networks.
- [Bitonic merger](/bitonic-merger/) and [bitonic sequence](/bitonic-sequence/): sorting a bitonic sequence is the same as merging two sorted lists, one of them reversed.
- [Odd-even merge sort](/odd-even-merge-sort/): Batcher's sort built from his odd-even merge.
- [Merging sorted lists](/merging-sorted-lists/): the same problem for algorithms that may choose their comparisons.
- [Network depth](/network-depth/) and [network size](/network-size/): the two costs of a merging network.

## References
