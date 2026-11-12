---
tag: 8V9YWA
kind: problem
slug: optimal-prefix-code
name: Optimal prefix code problem
aliases:
- minimum-redundancy code
- minimum-length prefix code
- minimum weighted external path length
area: compression-and-coding/entropy-coding
level: core
summary: Given symbol weights, choose a prefix code that minimizes the weighted sum of codeword lengths. Huffman's algorithm solves it in O(n log n) time.
prereqs: [prefix-code, kraft-inequality, shannon-entropy]
see_also: [huffman-coding, length-limited-prefix-code, optimal-alphabetic-code, unequal-letter-cost-coding, source-coding-theorem, uniquely-decodable-code, optimal-merge-pattern, shannon-fano-coding]
sources:
  - paper: doi:10.1109/jrproc.1952.273898
    title: David A. Huffman, A method for the construction of minimum-redundancy codes, Proceedings of the IRE 40(9), 1952
    locator: pages 1098 to 1101
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: Sections 5.2 (Kraft inequality), 5.3 (optimal codes), 5.4 (bounds on the optimal code length), 5.5 (Kraft inequality for uniquely decodable codes) and 5.8 (optimality of Huffman codes)
  - paper: doi:10.1109/tc.1976.1674574
    title: Martin C. Golumbic, Combinatorial merging, IEEE Transactions on Computers C-25(11), 1976
    locator: pages 1164 to 1167 (the minimax version)
  - paper: doi:10.1137/0137015
    title: T. C. Hu, D. J. Kleitman and J. K. Tamaki, Binary trees optimum under various criteria, SIAM Journal on Applied Mathematics 37(2), 1979
    locator: pages 246 to 256
  - paper: doi:10.1109/tit.1978.1055959
    title: Robert G. Gallager, Variations on a theme by Huffman, IEEE Transactions on Information Theory 24(6), 1978
    locator: pages 668 to 674 (the redundancy bound)
  - paper: doi:10.1145/3342555
    title: Alistair Moffat, Huffman coding, ACM Computing Surveys 52(4), 2019
    locator: Sections 2.1 to 2.4 (algorithms), 2.6 and 2.7 (optimality and effectiveness) and 4.1 (length-limited codes)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.3, Huffman codes
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.5, Path length
---

The optimal prefix code problem asks for a [prefix code](/prefix-code/) for $n$ symbols with given weights that minimizes the weighted sum of the codeword lengths. With probabilities as weights, this is the expected number of bits per symbol. By the [Kraft inequality](/kraft-inequality/) it is a problem about lengths only: choose positive integers $l_i$ with $\sum_i 2^{-l_i} \le 1$ to minimize $\sum_i w_i l_i$. [Huffman coding](/huffman-coding/) solves it exactly in $O(n \log n)$ time, and the optimal cost $L$ satisfies $H \le L < H + 1$, where $H$ is the [Shannon entropy](/shannon-entropy/). Changes to the constraints give harder problems: a length limit, a fixed order of the symbols, or code letters of different costs.

## In plain words

You want to give each letter of an alphabet a string of bits, so that a long text written with these strings is as short as possible. Common letters should get short strings and rare letters long ones. But the strings must not get in each other's way: no string may be the start of another, so that a reader always knows where one letter ends.

There is only so much room for short strings. Only two strings have one bit, and if you use one of them you lose all the longer strings that start with it. The problem is to share this room among the letters in the best way. Huffman found a simple method that always gives the best answer.

## Definition

**Input.** Weights $w_1, \ldots, w_n \ge 0$ for $n \ge 2$ symbols. The weights are the probabilities $p_i$ of a memoryless source, or the counts of the symbols in a known message. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area.

**Output.** A binary prefix code: codewords $c_1, \ldots, c_n$ in $\{0, 1\}^*$ such that no $c_i$ is a prefix of another $c_j$.

**Goal.** Minimize the cost $\sum_i w_i l_i$, where $l_i$ is the length of $c_i$. For probabilities this is the expected length $L$; for counts it is the length of the coded message, without the description of the code.

**Equivalent forms.**

- *Lengths.* A prefix code with lengths $l_1, \ldots, l_n$ exists if and only if $\sum_i 2^{-l_i} \le 1$ (Kraft). So the problem is an integer program over the lengths, and a [canonical code](/canonical-huffman-code/) turns the lengths into codewords.
- *Trees.* A prefix code is a binary tree with the symbols at its leaves; the length of a codeword is the depth of its leaf. The cost is the weighted external path length of the tree. An optimal tree is full: each inner node has two children, so $\sum_i 2^{-l_i} = 1$.
- *Uniquely decodable codes.* By McMillan's theorem, the lengths of each [uniquely decodable code](/uniquely-decodable-code/) also satisfy the Kraft inequality. So an optimal prefix code is optimal among all uniquely decodable codes too.

## Variants

- **Unrestricted (the classic problem).** Solved by Huffman's algorithm.
- **Code alphabet of $D$ letters.** Replace 2 by $D$ in the Kraft inequality. Huffman's method merges the $D$ lightest items after padding with zero weights.
- **Length-limited.** Add the constraint $l_i \le L_{\max}$. Formats such as DEFLATE need it. See [length-limited prefix code](/length-limited-prefix-code/); the [package-merge](/package-merge/) algorithm solves it in $O(n L_{\max})$ time.
- **Alphabetic.** The codewords must be in the same lexicographic order as the symbols. See [optimal alphabetic code](/optimal-alphabetic-code/).
- **Unequal letter costs.** The bits 0 and 1 have different costs, as the dot and the dash of Morse code. See [unequal letter cost coding](/unequal-letter-cost-coding/). The problem is polynomial for fixed integer costs, but no polynomial-time algorithm is known for general costs, and it is not known to be NP-hard.
- **Minimax.** Minimize $\max_i (w_i + l_i)$ instead of the sum. This is the cost of a merge or a circuit in which a node of depth $l$ is ready at time $w_i + l_i$. Golumbic (1976) showed that Huffman's method with $\max(a, b) + 1$ in place of $a + b$ solves it. Hu, Kleitman and Tamaki (1979) studied a wider class of cost functions of this kind.
- **Minimum variance.** Among all optimal codes, choose one with the smallest longest codeword or the smallest variance of the lengths. A tie rule in Huffman's method gives it.

## Examples

**A small case.** Weights 5, 2, 1, 1. The lengths 1, 2, 3, 3 satisfy $2^{-1} + 2^{-2} + 2^{-3} + 2^{-3} = 1$ and cost $5 + 4 + 3 + 3 = 15$. The fixed code with 2 bits for each symbol costs 18. No length list does better than 15.

| lengths for 5, 2, 1, 1 | Kraft sum | cost |
|---|---|---|
| 2, 2, 2, 2 | 1 | 18 |
| 1, 2, 3, 3 | 1 | 15 |
| 1, 3, 3, 3 | 7/8 | 17 |
| 1, 1, 2, 2 | 3/2, not a code | 11 |

**Several optima.** Weights 1, 1, 2, 2 have the optimal length lists 2, 2, 2, 2 and 3, 3, 2, 1, both of cost 12. The first has the shorter longest codeword.

**A skewed source.** Probabilities 0.9 and 0.1 need one bit each, so $L = 1$, while $H \approx 0.469$ bits. A prefix code cannot spend less than one bit on a symbol. Coding pairs of symbols, or [arithmetic coding](/arithmetic-coding/), comes closer to $H$.

## Known algorithms

- **[Huffman coding](/huffman-coding/).** Merge the two lightest items until one tree is left. $O(n \log n)$ time with a heap.
- **Two queues.** For sorted weights, van Leeuwen (1976) gave an $O(n)$ method with two queues. Moffat and Katajainen (1995) compute the lengths in place in the array of sorted weights, with $O(1)$ extra space.
- **Brute force.** Try all non-decreasing length lists that satisfy the Kraft inequality, with lengths at most $n - 1$, assigned to the weights in non-increasing order. This is exponential and only useful as a check, as in the code below.
- **[Shannon-Fano coding](/shannon-fano-coding/).** Fast top-down splits, not always optimal, but within one bit of the entropy in Shannon's form.

## Bounds

- **Entropy bounds.** For probabilities with entropy $H$, the optimal cost satisfies $H \le L < H + 1$. The lower bound holds for each prefix code, by Kraft and Gibbs' inequality; the upper bound comes from the lengths $\lceil \log_2 (1/p_i) \rceil$, which satisfy the Kraft inequality. This is the one-symbol case of the [source coding theorem](/source-coding-theorem/).
- **Gallager's bound.** $L - H \le p_1 + 0.086$ for the largest probability $p_1 < 1/2$ (Gallager 1978).
- **Lengths.** An optimal code for $n \ge 2$ symbols has lengths between 1 and $n - 1$. A heavier symbol never has a longer codeword.
- **Time.** Huffman's algorithm takes $O(n \log n)$ time, and $O(n)$ time after sorting.

## Reductions

- **Optimal merge pattern.** Merging $n$ sorted files two at a time, where a merge costs the sum of the two sizes, has the same cost function as a code tree. An optimal code tree is an optimal merge order. See [optimal merge pattern](/optimal-merge-pattern/).
- **Sorted weights and alphabetic codes.** If the symbols are in order of non-increasing weight, the lengths of an optimal code are non-decreasing, and a canonical code with these lengths keeps the symbol order. So for sorted weights the optimal alphabetic code and the optimal prefix code have the same cost.
- **Search trees.** A code tree is a decision tree that identifies a symbol with yes or no questions. The minimum expected number of questions, with any questions allowed, is the optimal prefix code cost.

## Applications

The problem is the core of static entropy coding. [DEFLATE](/deflate/), JPEG, Brotli and many other formats build Huffman codes for their symbol counts, usually with a length limit, and send them as canonical codes. It also appears in the design of decision trees for identification, in optimal merge orders, and in the analysis of comparison-based search when each question can split the set in any way.

## References
