---
tag: 06ZXXT
kind: algorithm
slug: huffman-coding
name: Huffman coding
aliases:
- Huffman's algorithm
- Huffman code
area: compression-and-coding/entropy-coding
level: intro
summary: Build an optimal prefix code by merging the two lightest subtrees again and again. The expected length is within one bit of the entropy.
solves: [optimal-prefix-code]
model: word-ram
complexity:
  vars: {n: the number of symbols}
  time: {worst: Θ(n log n), average: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: true}
history:
  year: 1952
  people: [David A. Huffman]
  note: Huffman published the method in the Proceedings of the IRE in September 1952, as a construction of minimum-redundancy codes.
prereqs: [prefix-code, priority-queue, greedy-algorithm]
see_also: [optimal-prefix-code, canonical-huffman-code, adaptive-huffman-coding, length-limited-prefix-code, shannon-fano-coding, arithmetic-coding, optimal-merge-pattern, deflate]
sources:
  - paper: doi:10.1109/jrproc.1952.273898
    title: David A. Huffman, A method for the construction of minimum-redundancy codes, Proceedings of the IRE 40(9), 1952
    locator: pages 1098 to 1101 (the merge of the two least probable messages, and the D-ary case)
  - paper: "Jan van Leeuwen, On the construction of Huffman trees, Proceedings of the 3rd International Colloquium on Automata, Languages and Programming (ICALP), Edinburgh University Press, 1976"
    locator: pages 382 to 410 (the linear-time method for sorted weights)
  - paper: doi:10.1109/tit.1978.1055959
    title: Robert G. Gallager, Variations on a theme by Huffman, IEEE Transactions on Information Theory 24(6), 1978
    locator: pages 668 to 674 (the sibling property and the redundancy bound p_1 + 0.086)
  - paper: doi:10.1016/s0019-9958(64)90241-4
    title: Eugene S. Schwartz, An optimum encoding with minimum longest code and total number of digits, Information and Control 7(1), 1964
    locator: pages 37 to 44 (the tie rule that gives the smallest longest codeword among optimal codes)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.3, Huffman codes
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition
    locator: Sections 5.4 (bounds on the optimal code length), 5.6 (Huffman codes) and 5.8 (optimality of Huffman codes)
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.5, Path length (Huffman's method for minimum weighted path length)
---

Huffman coding builds an optimal [prefix code](/prefix-code/) for a list of symbol weights: it merges the two lightest subtrees, again and again, until one tree is left. It solves the [optimal prefix code problem](/optimal-prefix-code/) in $O(n \log n)$ time with a [priority queue](/priority-queue/), and in $O(n)$ time when the weights are already sorted. Its expected codeword length $L$ satisfies $H \le L < H + 1$, where $H$ is the [Shannon entropy](/shannon-entropy/) of the source. It is the entropy coder of DEFLATE, JPEG and many other formats.

## In plain words

Each symbol starts as a small tree with one node, marked with how often the symbol occurs. Take the two trees with the smallest marks and join them under a new root. The mark of the new tree is the sum of the two marks. Do this again until one tree is left.

Now read the code from the tree. Going to the left child writes a 0, and going to the right child writes a 1. The codeword of a symbol is the path from the root to its leaf. Rare symbols were joined early, so they are deep in the tree and get long codewords. Common symbols were joined late and get short ones. No codeword is the start of another, so a decoder reads the bits one at a time and walks down the tree.

## The problem

The input is $n \ge 1$ symbols with weights $w_1, \ldots, w_n \ge 0$. The weights are probabilities $p_i$ of a memoryless source, or counts of the symbols in a known message. The output is a prefix code, that is a binary code tree with the symbols at its leaves, that minimizes the cost $\sum_i w_i l_i$, where $l_i$ is the length of the codeword of symbol $i$. With probabilities, the cost is the expected length $L$ in bits per symbol. With counts, it is the length of the encoded message in bits, not counting the description of the code. Here $n$ is the alphabet size, written $\sigma$ in the notation of this area. This is the [optimal prefix code problem](/optimal-prefix-code/).

## The algorithm

```pseudo id=main
HUFFMAN(w[1 .. n])                         ▷ n ≥ 1 weights; returns the root of a code tree
L1  Q ← an empty min-priority queue
L2  for i ← 1 to n do INSERT(Q, leaf i, w[i])
L3  for k ← 1 to n − 1 do
L4      x ← EXTRACT-MIN(Q)
L5      y ← EXTRACT-MIN(Q)
L6      z ← a new inner node with left child x and right child y
L7      w(z) ← w(x) + w(y)
L8      INSERT(Q, z, w(z))
L9  return EXTRACT-MIN(Q)
```

Each pass of the loop removes two items and adds one, so after $n - 1$ passes the queue holds one tree, with all $n$ leaves. The codeword of a symbol is the sequence of edge labels from the root to its leaf, with 0 for a left edge and 1 for a right edge. The encoder looks each symbol up in a table of codewords. The decoder starts at the root, follows one edge for each bit, and outputs a symbol and goes back to the root when it reaches a leaf.

**Sorted weights: two queues.** If $w_1 \le \cdots \le w_n$, a heap is not necessary (van Leeuwen 1976). The leaves wait in queue $A$ in sorted order. Each new inner node goes to the back of a second queue $B$. The weights of the new nodes never decrease, because each one is the sum of the two smallest items that are left. So $B$ is sorted too, and the smallest item is always at the front of $A$ or of $B$.

```pseudo id=two-queue
HUFFMAN-SORTED(w[1 .. n])                  ▷ w[1] ≤ w[2] ≤ … ≤ w[n]
T1  A ← the leaves 1 .. n in order; B ← an empty queue
T2  for k ← 1 to n − 1 do
T3      x ← the smaller front of A and B   ▷ on a tie, take the front of A
T4      y ← the smaller front of A and B   ▷ on a tie, take the front of A
T5      append the node (x, y) with weight w(x) + w(y) to B
T6  return the only item left
```

## Example

Take eight symbols with these counts in a message of 50 symbols: E 12, T 9, A 8, O 7, N 6, S 4, H 3, R 1. A heap breaks a tie by age, so an older item leaves first.

| step | the two items taken | new weight | queue after the step |
|---|---|---|---|
| 1 | R 1, H 3 | 4 | 4, S 4, N 6, O 7, A 8, T 9, E 12 |
| 2 | S 4, (R H) 4 | 8 | N 6, O 7, A 8, 8, T 9, E 12 |
| 3 | N 6, O 7 | 13 | A 8, 8, T 9, E 12, 13 |
| 4 | A 8, (S R H) 8 | 16 | T 9, E 12, 13, 16 |
| 5 | T 9, E 12 | 21 | 13, 16, 21 |
| 6 | (N O) 13, (A S R H) 16 | 29 | 21, 29 |
| 7 | (T E) 21, 29 | 50 | the root |

With 0 for the first item taken (the left child) and 1 for the second, the codewords are:

| symbol | E | T | A | O | N | S | H | R |
|---|---|---|---|---|---|---|---|---|
| count | 12 | 9 | 8 | 7 | 6 | 4 | 3 | 1 |
| codeword | 01 | 00 | 110 | 101 | 100 | 1110 | 11111 | 11110 |
| length | 2 | 2 | 3 | 3 | 3 | 4 | 5 | 5 |

The message takes $\sum w_i l_i = 141$ bits, against 150 bits for a fixed code of 3 bits for each symbol. Per symbol this is $L = 2.82$ bits, and the entropy of the counts is $H \approx 2.7746$ bits, so the redundancy $L - H$ is about $0.045$ bits. The word TEA encodes as 00 01 110, and the decoder reads 0001110 back as T, E, A. The sum of the inner weights $4 + 8 + 13 + 16 + 21 + 29 + 50$ is also 141: each inner node adds its weight once for each level of the leaves below it.

## Correctness

Two facts give the proof, by induction on $n$. The *greedy choice*: some optimal tree has the two lightest symbols as sibling leaves at the largest depth, because a swap that moves a lighter symbol deeper never increases the cost. The *merge*: if two siblings $x$ and $y$ are replaced by one leaf of weight $w_x + w_y$, the cost drops by exactly $w_x + w_y$, for every tree. So after the first merge, an optimal tree for the $n - 1$ remaining items gives an optimal tree for the $n$ symbols. This is an [exchange argument](/exchange-argument/), and the same proof shows that each rule for ties gives an optimal tree. The full proof, with the bounds $H \le L < H + 1$, is below.

## Complexity

The input size is the number of symbols $n$. The time does not depend on the length of the message, which only enters through the counting pass and the encoding.

- **Heap method.** With a [binary heap](/binary-heap/), line L2 costs $O(n)$ with bottom-up heap construction, and the loop does $2(n - 1)$ EXTRACT-MIN and $n - 1$ INSERT calls of $O(\log n)$ time each. The total is $O(n \log n)$ time.
- **Two queues.** Each pass of HUFFMAN-SORTED does $O(1)$ work, so it takes $\Theta(n)$ time after the sort. The sort costs $O(n \log n)$ comparisons in general, or $O(n + m)$ time with a counting sort when the counts are integers below $m$.
- **Space.** The tree has $2n - 1$ nodes, so the extra space is $\Theta(n)$.
- **Coding.** Encoding with a table and decoding with a walk of the tree take $O(1)$ time per output bit, so $\Theta(n_{\text{bits}})$ for a message of $n_{\text{bits}}$ encoded bits. Table-driven decoding of a [canonical Huffman code](/canonical-huffman-code/) reads several bits at a time.

## Properties

- **Optimal.** No prefix code has a smaller cost. By the Kraft and McMillan inequalities, no [uniquely decodable code](/uniquely-decodable-code/) does either.
- **Within one bit of the entropy.** For a memoryless source with all $p_i > 0$, $H \le L < H + 1$. Gallager (1978) proved the sharper bound $L - H \le p_1 + \sigma_G$, where $p_1$ is the largest probability and $\sigma_G = 1 - \log_2 e + \log_2 \log_2 e \approx 0.0861$.
- **Full tree.** Each inner node has two children, so for $n \ge 2$ the lengths satisfy the [Kraft inequality](/kraft-inequality/) with equality: $\sum 2^{-l_i} = 1$.
- **Monotone lengths.** If $w_i > w_j$ then $l_i \le l_j$ in each optimal code, by the swap of Lemma 1 in the proof.
- **Not unique.** Ties, and the choice of which child gets the 0, give different trees. Different trees can even have different length lists with the same cost: weights 1, 1, 2, 2 give lengths 2, 2, 2, 2 or 3, 3, 2, 1, both of cost 12.
- **Deep trees.** The longest codeword can have $n - 1$ bits. Weights that grow like the Fibonacci numbers 1, 1, 2, 3, 5, 8, ... give a tree that is a chain, with lengths $n - 1, n - 1, n - 2, \ldots, 1$.

## Variants and improvements

- **Minimum longest codeword.** In HUFFMAN-SORTED, line T3 and line T4 take a leaf before a merged node of the same weight. This is the tie rule of Schwartz (1964): among all optimal codes it gives one with the smallest longest codeword and the smallest sum of lengths. Textbooks call it the minimum variance Huffman code.
- **D-ary codes.** For a code alphabet of $D$ letters, add symbols of weight 0 until $n \equiv 1 \pmod{D - 1}$, then merge the $D$ lightest items at each step. Huffman's paper treats this case.
- **Canonical codes.** Keep only the lengths $l_i$ and assign the codewords in a fixed order. The decoder then needs only the lengths. See [canonical Huffman code](/canonical-huffman-code/).
- **A length limit.** Formats cap the codeword length, for example at 15 bits in DEFLATE. See [length-limited prefix code](/length-limited-prefix-code/) and the exact [package-merge](/package-merge/) algorithm.
- **One pass.** [Adaptive Huffman coding](/adaptive-huffman-coding/) updates the tree after each symbol, so no table is sent.
- **Blocks.** Coding blocks of $k$ symbols of a memoryless source as one symbol gives a redundancy below $1/k$ bits per symbol, at the cost of an alphabet of size $n^k$.

## When to use it

Use Huffman coding when the symbol statistics are known or can be counted in a first pass, and decoding speed matters: a canonical code decodes with a few table lookups per symbol. It is the right choice when no symbol has a very large probability, because the loss against the entropy is then small. When one symbol has a probability near 1, each codeword still costs at least one bit, and [arithmetic coding](/arithmetic-coding/) or [asymmetric numeral systems](/asymmetric-numeral-systems/) come much closer to the entropy. When the statistics change along the message, an adaptive coder or a context model does better than one static code.

## Pitfalls

- **One symbol.** HUFFMAN returns a single leaf, with a codeword of length 0, so the encoded message is empty and the decoder cannot know how many symbols to output. Give the single symbol a 1-bit codeword, as the implementation below does, or send the message length.
- **Different trees at the two ends.** Ties can be broken in many ways. If the encoder sends the counts and the decoder rebuilds the tree, both must use the same queue and the same tie rule. It is safer to send the code lengths and use a canonical code.
- **Floating-point weights.** With probabilities as floats, two sums that are equal in exact arithmetic can compare as different, and the two ends can build different trees. Use integer counts.
- **Forgetting the table.** The cost $\sum w_i l_i$ does not count the description of the code. For a short message the table can cost more than the saving.
- **No length limit.** A code built from real counts can have codewords longer than the format allows, or longer than a machine word. Check the longest length and use a length-limited method when it is too long.

## Implementations

## History

Huffman published the method in 1952 in the Proceedings of the IRE, for codes over an alphabet of $D$ letters. The top-down method of [Shannon-Fano coding](/shannon-fano-coding/), from Shannon (1948) and Fano (1949), came before it and is not always optimal. Schwartz (1964) studied the tie rule that gives the shortest longest codeword. Van Leeuwen (1976) gave the linear-time method for sorted weights. Gallager (1978) proved the redundancy bound $p_1 + 0.086$ and the sibling property that adaptive Huffman coding is based on.

## References
