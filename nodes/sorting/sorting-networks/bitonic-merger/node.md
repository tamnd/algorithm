---
tag: F6D32Z
kind: concept
slug: bitonic-merger
name: Bitonic merger
aliases:
- bitonic merging network
- bitonic split
area: sorting/sorting-networks
level: core
summary: A network that sorts a bitonic sequence of length n using log n layers of comparators.
prereqs: [bitonic-sequence, zero-one-principle]
see_also: [bitonic-sort, bitonic-sequence, merging-network, odd-even-merge-sort, network-depth, bitonic-counting-network]
sources:
  - paper: doi:10.1145/1468075.1468121
    title: K. E. Batcher, Sorting networks and their applications, AFIPS Spring Joint Computer Conference 32 (1968)
    locator: pp. 307 to 314 (the bitonic sorter)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Section 27.3 (the half-cleaner and BITONIC-SORTER) and Section 27.4 (MERGER)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (Batcher's bitonic sorter)
---

The bitonic merger is the comparator network that sorts each [bitonic sequence](/bitonic-sequence/) of length $n = 2^k$. It has $k$ layers, and layer $j$ is a row of *half-cleaners* that compare each wire $i$ with wire $i + n/2^j$ inside blocks of $n/2^{j-1}$ wires. It has $\tfrac12 n \lg n$ [comparators](/comparator/) and depth $\lg n$. Two sorted lists, the second one reversed, form a bitonic sequence, so the bitonic merger is also a [merging network](/merging-network/), and it is the merge step of [bitonic sort](/bitonic-sort/).

## In plain words

Take a list that goes up and then down, with an even number of items. Compare the first item with the middle item, the second with the one after the middle, and so on, and put the smaller of each pair in the first half. After this one round, every item in the first half is at most every item in the second half. Also, each half again goes up and then down, after a turn of the circle.

So the two halves can be sorted on their own, with the same round on each half, then on each quarter, and so on. After as many rounds as you can halve the list, it is sorted.

## The idea

**The half-cleaner.** For $m = 2h$ wires, the half-cleaner is the layer of comparators $[t : t + h]$ for $t = 0, \ldots, h - 1$. Let its input $x$ be bitonic, and let $u_t = \min(x_t, x_{t+h})$ and $v_t = \max(x_t, x_{t+h})$ be the two halves of its output. Then:

1. $u$ and $v$ are bitonic;
2. $u_s \le v_t$ for all $s$ and $t$.

For 0-1 inputs, this is a short argument. The ones of $x$ fill one cyclic interval. If there are at most $h$ ones, no pair $t, t + h$ holds two ones, so $u$ is all zeros and the ones of $v$ fill one cyclic interval of $h$ positions. If there are at least $h$ ones, the same argument with zeros shows that $v$ is all ones. In both cases $u_s \le v_t$. The general case follows, because a non-decreasing map $f$ commutes with min and max, and $x$ is bitonic exactly when each threshold image $t \mapsto [x_t \ge \theta]$ is bitonic.

**The merger.** BITONIC-MERGER on $m$ wires applies the half-cleaner and then BITONIC-MERGER on each half. By induction on $m$ and the two properties, it sorts each bitonic input: after the first layer the first half holds the $h$ smallest items, each half is bitonic, and the two recursive calls sort them. Unrolled, layer $j$ for $j = 1, \ldots, k$ compares wire $i$ with wire $i \oplus 2^{k-j}$ for each $i$ whose bit $k - j$ is 0.

**Cost.** The merger on $n = 2^k$ wires has $k$ layers of $n/2$ comparators each, so its size is $\tfrac12 n \lg n$ and its depth is $\lg n$. The depth is the smallest possible for a merging network of two lists of $n/2$ items. The item on a wire after $d$ layers is one of at most $2^d$ inputs, and the output at position $n/2$ can be any of the $n$ inputs: $a_i$ is there when exactly $n/2 - i$ items of $b$ are smaller than it, and in the same way for $b_j$. So $2^d \ge n$.

**Merging with the merger.** To merge two sorted lists $a$ and $b$ of $n/2$ items each, feed the merger with $a$ followed by $b$ in reverse order. This sequence goes up and then down. Instead of reversing $b$, one can change the first layer to compare $t$ with $n - 1 - t$, as CLRS does in its MERGER. The two halves of the result are then bitonic, and the rest of the merger sorts them.

**Comparison with Batcher's odd-even merge.** The odd-even merge of [odd-even merge sort](/odd-even-merge-sort/) also has depth $\lg n$, but only $\tfrac12 n (\lg n - 1) + 1$ comparators. The bitonic merger uses more comparators, but its layers are all of the same simple form $i$ and $i \oplus h$, and it sorts any bitonic input, not only two sorted halves.

## Examples

The merger on the bitonic input $(3, 4, 7, 8, 6, 5, 2, 1)$, with $n = 8$:

| layer | comparators | output |
|---|---|---|
| 1 | [0:4] [1:5] [2:6] [3:7] | 3 4 2 1 6 5 7 8 |
| 2 | [0:2] [1:3] [4:6] [5:7] | 2 1 3 4 6 5 7 8 |
| 3 | [0:1] [2:3] [4:5] [6:7] | 1 2 3 4 5 6 7 8 |

After layer 1 the first half $(3, 4, 2, 1)$ holds the four smallest items, and both halves are bitonic. The network has $3 \cdot 4 = 12$ comparators.

The merger does not sort an input that is not bitonic. On $(1, 3, 2, 4)$, the layer $[0:2], [1:3]$ changes nothing, and the layer $[0:1], [2:3]$ changes nothing either, so the output $(1, 3, 2, 4)$ is not sorted.

A sketch of the network as code, for $n$ a power of 2:

```
def bitonic_merger(n):
    net, h = [], n // 2
    while h >= 1:
        for i in range(n):
            if i & h == 0:
                net.append((i, i | h))
        h //= 2
    return net
```

## Where it is used

- **Bitonic sort.** Bitonic sort sorts the two halves and merges them with a bitonic merger. Its depth is $\sum_{j=1}^{k} j = \tfrac12 k (k + 1)$.
- **Parallel machines.** Each layer pairs the wires that differ in one bit. So the merger maps onto a hypercube, one dimension per layer, and onto SIMD units, where a layer is a fixed shuffle followed by a minimum and a maximum.
- **Merging on GPUs.** Merges of sorted blocks in GPU sorts and in SIMD merge kernels often use a bitonic merger on a block of 8, 16 or 32 items.
- **Counting networks.** The [bitonic counting network](/bitonic-counting-network/) uses the same wiring with balancers, and its proof follows the same steps.

## References
