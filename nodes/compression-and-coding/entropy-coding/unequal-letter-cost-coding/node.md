---
tag: QF16XK
kind: problem
slug: unequal-letter-cost-coding
name: Prefix coding with unequal letter costs
aliases:
- unequal letter cost code
- lopsided tree problem
area: compression-and-coding/entropy-coding
level: research
summary: Find a prefix code of least expected cost when the letters of the code alphabet have different costs, as dots and dashes do. Polynomial for fixed integer costs; not known to be NP-hard.
prereqs: [optimal-prefix-code, kraft-inequality]
see_also: [huffman-coding, length-limited-prefix-code, optimal-alphabetic-code, source-coding-theorem, arithmetic-coding, shannon-entropy]
sources:
  - paper: doi:10.1109/tit.1961.1057615
    title: Richard M. Karp, Minimum-redundancy coding for the discrete noiseless channel, IRE Transactions on Information Theory 7(1), 1961
    locator: pages 27 to 38 (the integer programming formulation)
  - paper: doi:10.1109/18.705558
    title: Mordecai J. Golin and Günter Rote, A dynamic programming algorithm for constructing optimal prefix-free codes with unequal letter costs, IEEE Transactions on Information Theory 44(5), 1998
    locator: pages 1770 to 1781
  - paper: doi:10.1145/509907.510020
    title: Mordecai J. Golin, Claire Kenyon and Neal E. Young, Huffman coding with unequal letter costs, Proceedings of the 34th ACM Symposium on Theory of Computing, 2002
    locator: pages 785 to 791 (the polynomial-time approximation scheme)
  - paper: doi:10.1002/j.1538-7305.1948.tb01338.x
    title: Claude E. Shannon, A mathematical theory of communication, Bell System Technical Journal 27(3), 1948
    locator: Part I, Section 1, Discrete noiseless systems (the capacity of a channel whose symbols have different durations)
---

Prefix coding with unequal letter costs asks for an optimal [prefix code](/prefix-code/) when the letters of the code alphabet do not all cost the same. In Morse code a dash takes three times as long as a dot; on some channels a 1 costs more energy than a 0. The cost of a codeword is the sum of the costs of its letters, and the aim is the least expected cost. With equal costs this is the [optimal prefix code problem](/optimal-prefix-code/), solved by Huffman's algorithm. With unequal costs no greedy method is known to be exact. Karp (1961) solved it by integer programming; Golin and Rote (1998) gave a dynamic program that is polynomial when the costs are fixed integers; Golin, Kenyon and Young (2002) gave a polynomial-time approximation scheme. Whether the general problem is NP-hard is open.

## In plain words

In a normal code every bit costs the same, so the best code makes common words short. Now suppose a 0 is cheap and a 1 is dear, as a short beep is cheaper than a long one. A codeword's price is the total price of its letters. You want the code with the lowest average price.

Huffman's trick no longer works. It builds the tree from the bottom, joining the two rarest symbols, and only at the end would you know which branches are cheap. The cheap branches should hold the common symbols, but the shape of the tree and the choice of branches depend on each other. So the best known exact methods build the tree from the top, one price level at a time, and try many shapes.

## Definition

**Input.** Weights $w_1, \ldots, w_n > 0$ for $n$ symbols, and the costs $c_1, \ldots, c_r > 0$ of the $r$ letters of the code alphabet. Here $n$ is the alphabet size of the source, written $\sigma$ in the notation of this area. The binary case $r = 2$, with costs $a$ for 0 and $b$ for 1, is the most studied.

**Output.** A prefix code: one word over the code alphabet for each symbol, no word a prefix of another.

**Objective.** Minimize $\sum_i w_i \operatorname{cost}(x_i)$, where the cost of a word is the sum of the costs of its letters.

In the tree of the code, an edge for letter $j$ has length $c_j$, and the cost of a codeword is the length of the path to its leaf. Such trees are called *lopsided trees*. An optimal tree has no unused branch when the costs are positive: an inner node with a single used child can be replaced by that child, which lowers the cost. So, in the binary case, an optimal tree is a full binary tree whose left edges cost $a$ and right edges cost $b$, and the heavier symbols sit at the cheaper leaves.

## Variants

- **Equal weights.** All $w_i$ equal: the task is to choose the $n$ cheapest leaves of some tree. This special case is easier and has polynomial algorithms for any letter costs.
- **More letters.** $r > 2$ letters with different costs, such as the dot, the dash and the gaps of telegraphy.
- **Alphabetic codes with letter costs.** The codewords must also keep the order of the symbols, as in the [optimal alphabetic code problem](/optimal-alphabetic-code/).
- **Length or cost limits.** A limit on the cost of the longest codeword, as for [length-limited codes](/length-limited-prefix-code/).
- **Searching with unequal outcomes.** A comparison tree in which one answer of a test takes longer to act on than the other is the same tree with weighted edges.

## Examples

Five symbols A to E with weights 9, 8, 8, 6, 6, and binary letters with costs $a = 1$ for 0 and $b = 2$ for 1. A Huffman code gives the lengths 2, 2, 2, 3, 3.

| code | A (9) | B (8) | C (8) | D (6) | E (6) | total cost |
|---|---|---|---|---|---|---|
| Huffman lengths, words 00, 01, 10, 110, 111 | 00: 2 | 01: 3 | 10: 3 | 110: 5 | 111: 6 | 132 |
| Huffman lengths, best choice of words | 01: 3 | 10: 3 | 11: 4 | 000: 3 | 001: 4 | 125 |
| optimal | 01: 3 | 10: 3 | 000: 3 | 11: 4 | 001: 4 | 123 |

Each cell gives the word and its cost. No code that keeps the Huffman lengths costs less than 125, but the optimal code costs 123: it gives C a three-letter word, 000, which costs only 3 because it uses only the cheap letter, and gives the two-letter word 11, of cost 4, to the lighter D. Lengths are the wrong measure here; only the letter costs count. The dynamic program below and a search over all tree shapes both give 123.

For five symbols of equal weight with the same costs, the optimal word costs are 3, 3, 3, 4, 4, for a total of 17: for example the words 000, 001, 01, 10, 11, with costs 3, 4, 3, 3, 4.

## Known algorithms

| method | time | note |
|---|---|---|
| Integer programming (Karp 1961) | exponential in the worst case | Exact, for any letter costs. |
| Level-by-level dynamic program (Golin and Rote 1998) | $O(n^{C+2})$ | Exact, for integer letter costs; $C$ is the largest letter cost. |
| Approximation scheme (Golin, Kenyon and Young 2002) | polynomial for each fixed $\varepsilon > 0$ | Cost at most $(1 + \varepsilon)$ times the optimum. |
| [Huffman coding](/huffman-coding/) | $O(n \log n)$ | Exact only when all letter costs are equal. |

**The dynamic program, for two letters.** Sort the weights so that $w_1 \ge w_2 \ge \cdots \ge w_n$; an optimal code gives the cheaper words to the heavier symbols. Build the tree from the top, one cost level at a time. The state after a level is $(m, v_1, \ldots, v_C)$: the first $m$ symbols already have their leaves, and $v_k$ nodes wait at $k$ levels below. Moving down one level adds the total weight $w_{m+1} + \cdots + w_n$ of the symbols still without a leaf, since each of them will end at least one level lower. At the new level, choose how many of the $v_1$ waiting nodes become leaves, $q$ of them for the next $q$ symbols; the others become inner nodes, each adding one node $a$ levels down and one $b$ levels down. There are $O(n^{C+1})$ states and $O(n)$ choices of $q$, which gives $O(n^{C+2})$ time. For costs 1 and 2, this is $O(n^4)$.

## Bounds

- **Capacity.** For binary letters of costs $a$ and $b$, let $c > 1$ be the root of $c^{-a} + c^{-b} = 1$. Every prefix code satisfies $\sum_i c^{-\operatorname{cost}(x_i)} \le 1$, a [Kraft inequality](/kraft-inequality/) for letter costs, with equality for a full tree. By Gibbs' inequality, the mean cost per symbol is at least $H / \log_2 c$, where $H$ is the [entropy](/shannon-entropy/). The number $\log_2 c$ is the capacity of the channel in bits per unit of cost, as in Shannon (1948). For costs 1 and 2, $c$ is the golden ratio, $\log_2 c \approx 0.694$, and the bound is about $1.44 H$.
- **Upper bound.** Codes built from the capacity, in the manner of Shannon's code, come within an additive constant of $H / \log_2 c$ that depends only on the letter costs.
- **Complexity.** The problem is in P for any fixed set of integer letter costs, by the dynamic program, but the degree grows with the largest cost. No polynomial algorithm is known for general costs, and the problem is not known to be NP-hard.

## Reductions

- **Equal letter costs.** With $a = b$, the cost is $a$ times the length, and the problem is the optimal prefix code problem. Huffman's algorithm solves it, and the dynamic program then gives the Huffman cost.
- **Rational costs.** Rational letter costs can be scaled to integers, so the dynamic program applies; the degree grows with the scaled largest cost.
- **Lopsided trees.** The problem is the search for a minimum weighted path length tree whose edges have two lengths, with the heaviest weights at the shortest paths.

## Applications

- **Telegraphy.** Morse code, whose dots and dashes and gaps have different durations, is the classic case, and Shannon's capacity for channels with symbols of different durations was the first theory of it.
- **Channels with unequal symbol costs.** Transmission in which one signal takes more time, energy or bandwidth than another, such as some optical or low-power links.
- **Constrained recording codes.** Channels on which some letters or runs of letters are costly, where the cost of each letter is part of the design.
- **Search with unequal answer costs.** Comparison trees in which the outcomes of a test lead to steps of different cost.

## References
