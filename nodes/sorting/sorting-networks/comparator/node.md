---
tag: 9H7NX0
kind: definition
slug: comparator
name: Comparator
aliases:
- compare-exchange
- two-input comparator
area: sorting/sorting-networks
level: intro
summary: A gate on two wires that outputs the smaller value on one wire and the larger on the other.
prereqs: [comparison-model]
see_also: [sorting-network, zero-one-principle, network-size, network-depth, odd-even-transposition-sort, shell-sort, counting-network]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (the comparator module [i:j], the standard form and the untangling of general networks)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Section 27.1, Comparison networks (the comparator and its depth), and Section 27.2 (Lemma 27.1, monotone functions)
  - book: isbn:9780201314526
    title: Robert Sedgewick, Algorithms in C, Parts 1 to 4, third edition
    locator: Chapter 11, Special-purpose sorting methods (the compare-exchange operation in Batcher's networks)
---

A comparator is the operation on two positions $i < j$ that puts the smaller of the two items at position $i$ and the larger at position $j$. It is the only step of a [sorting network](/sorting-network/), and in code it is the compare-exchange `if a[i] > a[j]: swap a[i], a[j]`. In the [comparison model](/comparison-model/) a comparator costs one comparison and at most one exchange. Because it commutes with each non-decreasing function, the [zero-one principle](/zero-one-principle/) holds for all networks of comparators.

## Definition

Let $X$ be a set with a total order $\le$, and let $n \ge 2$. For wires $0 \le i < j \le n - 1$, the comparator $[i{:}j]$ is the map $X^n \to X^n$ given by $[i{:}j](x) = x'$ with

$$x'_i = \min(x_i, x_j), \qquad x'_j = \max(x_i, x_j), \qquad x'_k = x_k \text{ for } k \ne i, j.$$

The *size* of a comparator is 1, and its two wires are $i$ and $j$. A *general comparator* $[j{:}i]$ with $i < j$ is the same map with the minimum on the higher wire $j$. A *standard* comparator has its minimum on the lower wire, as above.

On items with keys, the comparator compares the keys. It exchanges the two items if the key at $i$ is larger than the key at $j$, and else does nothing. So two items with equal keys are never exchanged by one comparator.

Four properties follow from the definition. Let $c = [i{:}j]$.

1. **The output is a permutation of the input.** The multiset $\{x'_i, x'_j\}$ equals $\{x_i, x_j\}$.
2. **Idempotent.** $c(c(x)) = c(x)$, because after one application $x'_i \le x'_j$.
3. **Disjoint comparators commute.** If $c = [i{:}j]$ and $c' = [k{:}l]$ have four different wires, then $c \circ c' = c' \circ c$. Two comparators with a common wire do not commute in general.
4. **Monotone maps pass through.** Let $f : X \to Y$ be non-decreasing, where $Y$ is also totally ordered, and apply $f$ to each coordinate. Then $c(f(x)) = f(c(x))$.

*Proof of property 4.* Only coordinates $i$ and $j$ change. Assume $x_i \le x_j$. Then $f(x_i) \le f(x_j)$, so $\min(f(x_i), f(x_j)) = f(x_i) = f(\min(x_i, x_j))$ and $\max(f(x_i), f(x_j)) = f(x_j) = f(\max(x_i, x_j))$. The case $x_i > x_j$ is the same with $i$ and $j$ exchanged. $\square$

By induction on the number of comparators, property 4 holds for each comparator network: the network maps $f(x)$ to $f(y)$ when it maps $x$ to $y$. This is the lemma behind the zero-one principle (CLRS, Lemma 27.1).

## Examples and non-examples

**Examples.**

- $[0{:}2]$ on $(5, 8, 3)$ gives $(3, 8, 5)$. On $(3, 8, 5)$ it gives $(3, 8, 5)$, by property 2.
- $[1{:}2]$ on the bits $(1, 1, 0)$ gives $(1, 0, 1)$. On bits, the comparator writes $a \wedge b$ to wire $i$ and $a \vee b$ to wire $j$. So a network of $s$ comparators on bits is a monotone [Boolean circuit](/boolean-circuit/) of $2s$ gates.
- The general comparator $[2{:}0]$ on $(5, 8, 3)$ gives $(5, 8, 3)$: the minimum 3 stays on wire 2.
- The [sorting network](/sorting-network/) $[0{:}1], [1{:}2], [0{:}1]$ on 3 wires is the insertion of the third item into the sorted first two. [Odd-even transposition sort](/odd-even-transposition-sort/) uses only comparators $[i{:}i+1]$ on adjacent wires, and [Shellsort](/shell-sort/) with a fixed gap sequence is a sequence of compare-exchanges at distance $h$.
- In code without a branch, a comparator on numbers is `lo = min(a, b); hi = max(a, b)`. On SIMD hardware one instruction computes the minimum and one the maximum of many pairs at the same time, so a full layer of comparators costs two instructions.

**Stability fails in networks.** One comparator does not exchange equal keys, but a network of comparators is not stable in general. The network $[0{:}2], [0{:}1], [1{:}2]$ sorts each input of 3 items. On the input $(2_a, 2_b, 1)$, where $2_a$ and $2_b$ have the same key, $[0{:}2]$ gives $(1, 2_b, 2_a)$. The two other comparators make no exchange, so the output is $(1, 2_b, 2_a)$, and the equal items are in the wrong order. A comparator on a pair of distant wires can jump an item over an equal one.

**Non-examples.**

- **A fixed exchange.** The map that always exchanges wires $i$ and $j$ is a permutation of wires, not a comparator. It does not compare.
- **An exchange that depends on a third wire.** "Exchange $x_i$ and $x_j$ if $x_k > 0$" is not a comparator. Such a step does not commute with each non-decreasing map, because $f(x_k) > 0$ and $x_k > 0$ can differ, so the proof of the zero-one principle does not apply to networks of such steps.
- **A gate on three wires.** A gate that sorts the items of three wires is a 3-sorter, not a comparator. It does the work of 3 comparators in one step, and networks of such gates are a different model with other bounds.
- **A comparator with $i = j$.** It is not defined. A comparator always has two different wires.

## Related definitions

- [Sorting network](/sorting-network/): a sequence of comparators that sorts every input.
- [Network size](/network-size/): the number of comparators of a network.
- [Network depth](/network-depth/): the number of layers of comparators with disjoint wires.
- [Zero-one principle](/zero-one-principle/): a network of comparators sorts each input if it sorts each input of zeros and ones. Its proof uses property 4.
- [Merging network](/merging-network/): a network of comparators that merges two sorted sequences.
- [Counting network](/counting-network/): its *balancer* has the same shape as a comparator, but it routes tokens instead of comparing items.

## References
