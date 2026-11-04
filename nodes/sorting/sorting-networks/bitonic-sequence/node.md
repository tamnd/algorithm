---
tag: 67C5ZP
kind: definition
slug: bitonic-sequence
name: Bitonic sequence
aliases:
- bitonic
area: sorting/sorting-networks
level: core
summary: A sequence that first increases then decreases, or can be cyclically shifted to do so.
prereqs: [sorting-network]
see_also: [bitonic-merger, bitonic-sort, zero-one-principle, merging-network, bitonic-counting-network, bitonic-tsp]
sources:
  - paper: doi:10.1145/1468075.1468121
    title: K. E. Batcher, Sorting networks and their applications, AFIPS Spring Joint Computer Conference 32 (1968)
    locator: pp. 307 to 314 (bitonic sequences and the bitonic sorter)
  - book: isbn:9780262032933
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, second edition
    locator: Section 27.3, A bitonic sorting network (the definition, and the half-cleaner lemma for 0-1 sequences)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.4, Networks for sorting (Batcher's bitonic sorter)
---

A bitonic sequence is a sequence that first goes up and then goes down, or that becomes such a sequence after a cyclic shift. Batcher introduced the notion for his [bitonic sorter](/bitonic-sort/): a sorted list followed by a list sorted in the other direction is bitonic, and a bitonic sequence of length $n = 2^k$ can be sorted by a [bitonic merger](/bitonic-merger/) of depth $k$. For sequences of zeros and ones the definition is simple: the ones fill one cyclic interval of positions.

## Definition

Let $x = (x_0, x_1, \ldots, x_{n-1})$ be a sequence over a totally ordered set.

The sequence $x$ is *unimodal* (increasing, then decreasing) when there is an index $k$ with

$$x_0 \le x_1 \le \cdots \le x_k \ge x_{k+1} \ge \cdots \ge x_{n-1}.$$

Either part can be empty, so each sorted sequence and each reverse sorted sequence is unimodal.

The sequence $x$ is *bitonic* when some cyclic shift $(x_r, x_{r+1}, \ldots, x_{n-1}, x_0, \ldots, x_{r-1})$ of it is unimodal.

Some texts also count a sequence that first decreases and then increases. This adds nothing: such a sequence is a cyclic shift of an increasing-then-decreasing sequence, because one can start the cycle at its largest item.

**Zero-one sequences.** A sequence $x \in \{0, 1\}^n$ is bitonic if and only if it has the form $0^a 1^b 0^c$ or $1^a 0^b 1^c$ with $a, b, c \ge 0$. Equivalently, the positions of its ones are empty or one cyclic interval $\{r, r+1, \ldots, r + \ell - 1\}$, read modulo $n$. There are $n(n-1) + 2$ bitonic 0-1 sequences of length $n$.

**Threshold form.** A sequence $x$ is bitonic if and only if, for each value $\theta$, the positions $\{t : x_t \ge \theta\}$ are empty, all positions, or one cyclic interval. *Proof.* If $x$ is unimodal, the positions with $x_t \ge \theta$ are an interval around the peak, and a cyclic shift keeps cyclic intervals. For the converse, shift $x$ so that it starts at a position $r$ of a smallest item. For $\theta$ above this item, the set $\{t : x_t \ge \theta\}$ is a cyclic interval that does not hold $r$, so it is an ordinary interval of the shifted sequence. These intervals shrink as $\theta$ grows, so the shifted sequence goes up and then down. $\square$

So a non-decreasing map $f$ sends bitonic sequences to bitonic sequences, and $x$ is bitonic exactly when each of its 0-1 images $t \mapsto [x_t \ge \theta]$ is bitonic. This is what lets the [zero-one principle](/zero-one-principle/) prove the bitonic networks correct.

**Closure.** If $x$ is bitonic, so are its reverse, each cyclic shift of it, and $f(x)$ for each non-decreasing $f$.

**The half-cleaner property.** Let $x$ be bitonic of length $2h$, and let $u_t = \min(x_t, x_{t+h})$ and $v_t = \max(x_t, x_{t+h})$ for $t < h$. Then $u$ and $v$ are bitonic, and $u_s \le v_t$ for all $s$ and $t$. For 0-1 sequences, one of $u$ and $v$ is constant. The 0-1 case is Lemma 27.3 of CLRS (second edition), and the general case follows from it by the threshold form. This property is the base of the bitonic merger.

## Examples and non-examples

**Examples.**

- $(1, 4, 6, 8, 3, 2)$ goes up to 8 and then down. It is unimodal, so it is bitonic.
- $(6, 9, 4, 2, 3, 5)$ is bitonic: the cyclic shift that starts at 2 is $(2, 3, 5, 6, 9, 4)$, which is unimodal.
- A sorted list followed by a reverse sorted list, such as $(1, 3, 5, 7, 8, 6, 4, 2)$, is bitonic. So is a reverse sorted list followed by a sorted list, such as $(8, 5, 2, 1, 3, 4)$.
- Each sequence with at most 3 items is bitonic, and so is each constant sequence.
- Of the 16 sequences in $\{0, 1\}^4$, all except $(0, 1, 0, 1)$ and $(1, 0, 1, 0)$ are bitonic, which gives $4 \cdot 3 + 2 = 14$.
- The half-cleaner on $(3, 4, 7, 8, 6, 5, 2, 1)$ gives $u = (3, 4, 2, 1)$ and $v = (6, 5, 7, 8)$. Both are bitonic, and $\max u = 4 \le 5 = \min v$.

**Non-examples.**

- $(1, 3, 2, 4)$ is not bitonic. Its four cyclic shifts $(1, 3, 2, 4)$, $(3, 2, 4, 1)$, $(2, 4, 1, 3)$ and $(4, 1, 3, 2)$ each go up, down and up again. The threshold $\theta = 3$ gives the positions $\{1, 3\}$, which are not a cyclic interval.
- Two sorted lists in the same direction, such as $(1, 5, 2, 6)$, are not bitonic in general. This is why [bitonic sort](/bitonic-sort/) reverses one of the two halves, or sorts it in the other direction, before it merges.
- The concatenation of two bitonic sequences need not be bitonic: $(1, 2, 1)$ followed by $(1, 2, 1)$ is $(1, 2, 1, 1, 2, 1)$, which has two peaks.
- A *bitonic tour* in the [bitonic travelling salesman problem](/bitonic-tsp/) is a different notion: a tour that goes from left to right and back. It shares only the name.

## Related definitions

- [Bitonic merger](/bitonic-merger/): a network of depth $\lg n$ that sorts each bitonic sequence of length $n = 2^k$, made of half-cleaners.
- [Bitonic sort](/bitonic-sort/): the sorting network that sorts the two halves and merges the bitonic result.
- [Merging network](/merging-network/): a network that merges two sorted lists. Reversing the second list turns merging into sorting a bitonic sequence.
- [Zero-one principle](/zero-one-principle/): by the threshold form, it is enough to check the bitonic 0-1 inputs.
- [Bitonic counting network](/bitonic-counting-network/): the same wiring with balancers instead of comparators.

## References
