---
tag: 0TS6SH
kind: problem
slug: power-set-enumeration
name: Enumerating the power set
aliases:
- generating all subsets
- subset generation
- listing all subsets
area: combinatorics/generating-combinations
level: intro
summary: List all 2^n subsets of an n-element set, each exactly once.
complexity:
  vars: {n: the size of the ground set}
  time: {worst: Ω(2^n)}
prereqs: [combinatorial-generation]
see_also: [power-set-by-recursion, binary-reflected-gray-code, loopless-gray-code-generation, submask-enumeration, k-subset-enumeration, binary-counter-increment, hypercube-hamiltonian-cycle, generic-backtracking-algorithm]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (Algorithm M for mixed-radix counting, Gray binary code, Algorithm G and the loopless Algorithm L)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 1, Next subset of an n-set
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2, Section 2.2, Subsets (lexicographic order and Gray codes, with rank and unrank)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition, Springer, 2020
    locator: Section 17.5, Generating subsets
---

Power set enumeration asks for a list of all $2^n$ subsets of an $n$-element set, with each subset exactly once. A subset is the same as an $n$-bit string, so the problem is also the listing of all $n$-bit strings. Any method needs $\Omega(2^n)$ time, and the [binary reflected Gray code](/binary-reflected-gray-code/) reaches $O(1)$ time for each subset in the worst case. It is the first step of each [brute-force search](/brute-force-search/) over subsets.

## In plain words

You have a few items, for example the toppings for a pizza. You want to see every possible choice of toppings: no topping, each single topping, each pair, and so on, up to all of them. Each item is either in or out, so each new item doubles the number of choices.

A simple way is to count in binary. Each digit of the number belongs to one item. A one means "in" and a zero means "out". Counting from zero up to the largest number with that many digits gives every choice once. A better way changes only one item at each step, so a program can update its work with one small change.

## Definition

Let $n \ge 0$ and let $[n] = \{1, \ldots, n\}$ be the ground set. The power set is $2^{[n]} = \{S : S \subseteq [n]\}$, and $|2^{[n]}| = 2^n$.

**Input.** The integer $n$. A set $U = \{u_1, \ldots, u_n\}$ of other items reduces to $[n]$ by the index map $j \mapsto u_j$.

**Output.** A sequence $S_0, S_1, \ldots, S_{2^n - 1}$ of subsets of $[n]$ in which each subset of $[n]$ appears exactly once.

**Representation.** A subset $S$ is stored as its characteristic vector $x \in \{0, 1\}^n$, with $x_j = 1$ if and only if $j \in S$. When $n$ is at most the word size $w$, the vector fits in one machine word, and the subset is the integer $\sum_{j \in S} 2^{j-1}$. A subset can also be stored as the sorted list of its elements.

**Cost model.** In the usual model the generator keeps one current vector and changes it in place. The visit of each subset is free. If each subset is copied to the output, each copy costs $\Theta(n)$ more.

## Variants

- **A fixed order.** Binary counting order (the integers $0$ to $2^n - 1$), Gray code order (neighbors differ in one element), lexicographic order of the sorted lists, or the order by size (all subsets of size $0$, then of size $1$, and so on).
- **Submasks.** List all subsets of a given set $M$, not of all of $[n]$. The trick $s \leftarrow (s - 1) \wedge M$ does this in $O(1)$ word operations for each subset. See [submask enumeration](/submask-enumeration/).
- **Subsets of one size.** List only the subsets of size $k$. This is [k-subset enumeration](/k-subset-enumeration/).
- **Subsets with a side condition.** List only the subsets with a sum at most $W$, or only the independent sets of a graph. Here the number of outputs is not known in advance, and [backtracking](/generic-backtracking-algorithm/) cuts the branches that cannot lead to an output.
- **Rank and unrank.** In binary counting order the rank of $S$ is $\sum_{j \in S} 2^{j-1}$, and unrank reads the bits. In Gray code order rank and unrank are the conversions [from Gray to binary](/gray-to-binary-conversion/) and [from binary to Gray](/binary-to-gray-conversion/).
- **One random subset.** Choose each element with probability $1/2$, independently. See [uniform random subset](/uniform-random-subset/).

## Examples

**$n = 4$ in Gray code order.** The 16 bit strings $x_4 x_3 x_2 x_1$ are

$$0000, 0001, 0011, 0010, 0110, 0111, 0101, 0100, 1100, 1101, 1111, 1110, 1010, 1011, 1001, 1000.$$

Each step flips exactly one bit, so each step adds or removes one element. The last string differs from the first in one bit, so the list is a cycle.

**The cost of counting.** To go from $0$ to $2^n - 1$, a binary counter flips $2^{n+1} - n - 2$ bits in total. For $n = 4$ this is $26$ flips for $15$ steps, against $15$ flips for the Gray code. The value $2^{n+1} - n - 2$ is less than twice the number of steps, so binary counting is constant amortized time, but one step (from $0111$ to $1000$) flips $4$ bits.

**Submasks.** For $M = 1011$ the rule $s \leftarrow (s - 1) \wedge M$, from $s = M$, gives $1011, 1010, 1001, 1000, 0011, 0010, 0001, 0000$: the $2^3 = 8$ subsets of $M$, in decreasing order.

**The size of the output.** The subsets of $[n]$ have $n 2^{n-1}$ elements in total, because each element is in half of the subsets. For $n = 4$ this is $32$.

## Known algorithms

| algorithm | order | time for each subset | page |
| --- | --- | --- | --- |
| binary counter | binary counting | $O(1)$ amortized, $O(n)$ worst case | [power set by recursion](/power-set-by-recursion/) |
| include or exclude recursion | binary counting | $O(1)$ amortized | [power set by recursion](/power-set-by-recursion/) |
| Gray code by the parity rule | Gray code | $O(1)$ amortized | [Gray code generation](/gray-code-generation/) |
| focus pointers (Bitner, Ehrlich and Reingold) | Gray code | $O(1)$ worst case | [loopless Gray code generation](/loopless-gray-code-generation/) |
| $(s - 1) \wedge M$ | decreasing integers | $O(1)$ word operations | [submask enumeration](/submask-enumeration/) |
| $k$-subsets for $k = 0, 1, \ldots, n$ | by size | $O(1)$ amortized for $k \le n/2$ | [lexicographic combinations](/lexicographic-combinations/) |

## Bounds

- **Lower bound.** There are $2^n$ outputs, so each algorithm takes $\Omega(2^n)$ time. In the in-place model, two consecutive subsets differ in at least one element, so the total number of changes is at least $2^n - 1$. A Gray code meets this bound exactly.
- **Upper bound.** Loopless Gray code generation takes $O(1)$ time in the worst case between two visits, after $O(n)$ initialization. So the total time is $\Theta(2^n)$.
- **Written output.** If each subset is written out in full as a bit string, the output has $n 2^n$ bits, so the time is $\Theta(n 2^n)$. As sorted lists, the output has $n 2^{n-1}$ elements in total.

## Reductions

- **To and from bit strings.** A subset of $[n]$ and its characteristic vector are the same object. So a listing of $\{0, 1\}^n$ is a listing of the power set, with no extra cost.
- **To counting.** The binary counting order is a bijection to the integers $0$ to $2^n - 1$. So listing the power set is the same as running a [binary counter](/binary-counter-increment/).
- **To Hamiltonian paths.** A Gray code for $\{0, 1\}^n$ is a Hamiltonian path in the $n$-dimensional hypercube graph, and a cyclic Gray code is a Hamiltonian cycle. See [hypercube Hamiltonian cycle](/hypercube-hamiltonian-cycle/).
- **From k-subsets.** The power set is the disjoint union of the $k$-subsets for $k = 0, \ldots, n$. So a [k-subset enumeration](/k-subset-enumeration/) for each $k$ lists the power set by size.

## Applications

- **Brute force over subsets.** Exact algorithms for [subset sum](/subset-sum-problem/), small [knapsack](/knapsack-problem/) instances and set cover try each subset. A Gray code order updates the sum with one addition or subtraction for each step.
- **Meet in the middle.** The [Horowitz and Sahni algorithm](/horowitz-sahni-algorithm/) lists the $2^{n/2}$ subset sums of each half of the input, sorts them and matches them.
- **Dynamic programming over subsets.** [Bitmask DP](/bitmask-dp/) and the [sum over subsets](/sum-over-subsets/) transform run over all subsets of $[n]$ as integers in binary counting order.
- **Testing.** A test of a function with $n$ Boolean flags tries all $2^n$ settings when $n$ is small.

## References
