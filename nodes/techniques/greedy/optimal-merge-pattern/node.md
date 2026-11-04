---
tag: 2JQ4FM
kind: problem
slug: optimal-merge-pattern
name: Optimal merge pattern
aliases:
- merge pattern problem
- merge sequence cost
- optimal file merge order
- optimal two-way merge order
area: techniques/greedy
level: intro
summary: Merge sorted files pairwise in an order that minimizes total cost, by always merging the two smallest.
prereqs: [greedy-algorithm, merge-sort]
see_also: [huffman-coding, k-way-merge, binary-heap, hu-tucker-algorithm, garsia-wachs-algorithm, optimal-tape-storage, exchange-argument, greedy-choice-property]
sources:
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 4, The Greedy Method (optimal merge patterns)
  - paper: doi:10.1109/JRPROC.1952.273898
    title: David A. Huffman, A method for the construction of minimum-redundancy codes, Proceedings of the IRE 40(9), 1952
    locator: pages 1098 to 1101
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.3, Huffman codes
---

The optimal merge pattern problem asks for the cheapest way to merge $n$ sorted files into one by repeated two-way merges, when merging files of sizes $x$ and $y$ costs $x + y$. The cost of a merge pattern is the weighted external path length of its merge tree, so the problem is the same as building a [Huffman code](/huffman-coding/) with the file sizes as frequencies. The greedy rule "always merge the two smallest files" is optimal and runs in $O(n \log n)$ time with a [binary heap](/binary-heap/).

## In plain words

You have several sorted lists of different lengths, and you want one sorted list. A merge takes two lists and makes one, and its cost is the total length of the two lists, because every item is moved once. You repeat merges until one list is left.

The order of the merges matters a lot. An item that takes part in many merges is moved many times. So the long lists should take part in few merges, and the short lists can take part in many.

The best plan is simple. Always merge the two shortest lists you have now. This is the same rule that builds Huffman codes, and it is optimal for the same reason.

## Definition

**Input.** Sizes $q_1, \ldots, q_n \ge 0$ of $n$ sorted files, $n \ge 1$.

**Merge patterns.** A step replaces two files of sizes $x$ and $y$ by one file of size $x + y$, at cost $x + y$. A merge pattern is a sequence of $n - 1$ steps that ends with one file. Its cost is the sum of the step costs.

**Merge trees.** Each merge pattern gives a binary tree in which every internal node has two children. The leaves are the input files, and each internal node is a merge. Let $\ell_i$ be the depth of file $i$, the number of merges that move its records. Then
$$ \text{cost} = \sum_{i=1}^{n} q_i\, \ell_i, $$
the weighted external path length of the tree, because each record of file $i$ is moved once at each of the $\ell_i$ merges above it. Every such tree comes from some merge pattern, so the problem is to find a binary tree with the given leaf weights and the least weighted external path length.

**Theorem.** Merging the two smallest files at each step gives a pattern of least cost.

*Proof.* Induction on $n$; for $n = 1$ there is nothing to do. Let $x$ and $y$ be two smallest sizes. *First, some optimal tree has $x$ and $y$ as siblings at the largest depth.* Take an optimal tree and two sibling leaves $a$, $b$ at the largest depth $D$; they exist because every internal node has two children. Swapping leaf $x$ with $a$ changes the cost by $(q_a - q_x)(\ell_x - D) \le 0$, because $q_x \le q_a$ and $\ell_x \le D$. The same holds for $y$ and $b$. *Second, reduce.* In a tree $T$ where $x$ and $y$ are siblings, replacing them and their parent by one leaf of size $x + y$ gives a tree $T'$ for $n - 1$ files, with $\text{cost}(T) = \text{cost}(T') + x + y$. This is a one-to-one correspondence between such trees and trees for the $n - 1$ files. So an optimal tree for the $n$ files is an optimal tree for the $n - 1$ files with the leaf $x + y$ expanded. The greedy algorithm merges $x$ and $y$ first and then, by induction, builds an optimal tree for the $n - 1$ files. $\square$

This is the proof of Huffman's algorithm. The page [Huffman coding](/huffman-coding/) treats it from the side of codes.

## Variants

- **Merge cost with comparisons.** Merging lists of sizes $x$ and $y$ takes at most $x + y - 1$ comparisons. With this cost, every pattern pays $n - 1$ less than with $x + y$, so the same pattern is optimal.
- **$k$-way merges.** Each step merges up to $k$ files at the cost of their total size, as in [k-way merging](/k-way-merge/). The greedy rule merges the $k$ smallest files, after adding files of size 0 until $(n - 1)$ is a multiple of $k - 1$. Without the padding, the rule can fail.
- **Order-preserving merges.** If only files that are adjacent in a fixed order may be merged, the tree must keep the leaves in order. This is the optimal alphabetic tree problem, solved by the [Hu-Tucker algorithm](/hu-tucker-algorithm/) and the [Garsia-Wachs algorithm](/garsia-wachs-algorithm/) in $O(n \log n)$ time. The greedy rule above does not keep the order.
- **Prefix codes.** With symbol frequencies as sizes, a merge tree is a binary prefix code, and the cost is the total encoded length. This is [Huffman coding](/huffman-coding/).

## Examples

**Five files.** Sizes $20, 30, 10, 5, 30$.

| step | two smallest | merged size | cost so far | files after the step |
| --- | --- | --- | --- | --- |
| 1 | 5, 10 | 15 | 15 | 15, 20, 30, 30 |
| 2 | 15, 20 | 35 | 50 | 30, 30, 35 |
| 3 | 30, 30 | 60 | 110 | 35, 60 |
| 4 | 35, 60 | 95 | 205 | 95 |

The cost is 205, the least over all merge patterns. Merging from left to right in the input order costs $50 + 60 + 65 + 95 = 270$, and the worst pattern costs 325. In the merge tree, the files of size 5 and 10 have depth 3, the file of size 20 has depth 2, the two files of size 30 have depth 2, and $5 \cdot 3 + 10 \cdot 3 + 20 \cdot 2 + 30 \cdot 2 + 30 \cdot 2 = 205$.

**Three-way merges and padding.** Sizes $40, 10, 35, 15, 25, 5$ with $k = 3$. Here $n - 1 = 5$ is odd, so add one file of size 0. The rule merges $0, 5, 10$ (cost 15), then $15, 15, 25$ (cost 55), then $35, 40, 55$ (cost 130), for a total of 200, which is optimal. Without the padding, the rule merges $5, 10, 15$ (cost 30), then $25, 30, 35$ (cost 90), then $40, 90$ (cost 130), for a total of 250. The padding makes the last merge a full three-way merge, so that no merge with fewer than $k$ files happens at the top of the tree, where it is most expensive.

## Known algorithms

- **Greedy with a min-heap.** Put the sizes in a [binary heap](/binary-heap/), and $n - 1$ times remove the two smallest and insert their sum. $O(n \log n)$ time and $O(n)$ space.
- **Two queues on sorted input.** If the sizes are given sorted, keep the input in one queue and the merged files, which are produced in nondecreasing order, in a second queue. The two smallest are at the fronts of the queues, so the algorithm runs in $O(n)$ time.
- **Brute force.** Try all pairs at each step. Exponential, useful only as a test oracle.

## Bounds

- **Upper bound.** $O(n \log n)$ time in general and $O(n)$ for sorted sizes.
- **Lower bound.** $\Omega(n)$ time, because every size can change the answer.
- **Value.** For $n$ equal sizes $q$, the optimum is $q$ times the external path length of a binary tree with all leaves on two adjacent levels, about $q\, n \log_2 n$.

## Reductions

- **Equal to Huffman coding.** A merge tree with leaf sizes $q_i$ is a binary prefix code with frequencies $q_i$, and the two costs are the same sum $\sum_i q_i \ell_i$. Each problem is the other under a change of names.
- **Unit sizes give the balanced tree.** With all $q_i = 1$ the cost is the external path length, and the greedy rule builds a tree with all leaves on two adjacent levels, the shape of a balanced [merge sort](/merge-sort/).

## Applications

- **External sorting.** After the runs of a file are sorted, they are merged on disk. Merging small runs first reduces the total data moved.
- **Combining sorted lists of different sizes.** Search engines and databases merge posting lists and sorted runs of very different lengths.
- **Teaching.** The problem gives the Huffman construction a concrete cost that is easy to see: records moved.

## References
