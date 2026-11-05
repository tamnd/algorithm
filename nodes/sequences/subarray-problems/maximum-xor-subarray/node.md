---
tag: 6FRQ23
kind: problem
slug: maximum-xor-subarray
name: Maximum XOR subarray
aliases:
- maximum subarray XOR
area: sequences/subarray-problems
level: advanced
summary: Find the subarray whose XOR of elements is largest; reduces to prefix XOR pairs queried with a binary trie.
prereqs: [subarray, prefix-sums, trie, bitwise-operations]
see_also: [persistent-trie, xor-gaussian-elimination, subarray-sum-equals-k, prefix-sum-hash-counting, maximum-subarray-problem, bit-manipulation, hash-table, sliding-window]
sources:
  - url: https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/
    title: LeetCode, problem 421, Maximum XOR of Two Numbers in an Array
    locator: problem statement (the pair problem that the prefix XOR reduction gives)
  - url: https://cses.fi/problemset/task/1655
    title: CSES Problem Set, Maximum Xor Subarray
    locator: problem statement
  - url: https://leetcode.com/problems/maximum-xor-with-an-element-from-array/
    title: LeetCode, problem 1707, Maximum XOR With an Element From Array
    locator: problem statement (queries of the largest XOR with a value, answered with a trie)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Section 6.3, Digital Searching (tries over the bits of the keys)
---

The maximum XOR subarray problem gives an array of $w$-bit non-negative integers and asks for the non-empty [subarray](/subarray/) whose bitwise exclusive or (XOR) of items is largest. XOR is its own inverse, so with prefix XORs $X[t] = A[0] \oplus \dots \oplus A[t-1]$ the subarray $A[i..j)$ has XOR $X[i] \oplus X[j]$, in the same way that a subarray sum is a difference of [prefix sums](/prefix-sums/). The problem is then the largest XOR of a pair among $n + 1$ numbers. A binary [trie](/trie/) of the prefix XORs read so far answers, for each $j$, the best partner of $X[j]$ in $O(w)$ steps, by choosing at each bit the child that differs, for $O(nw)$ time in total.

## In plain words

XOR compares two numbers bit by bit and gives a $1$ where they differ. XOR of a run of numbers is like a sum where carries are dropped. Like a sum, it can be undone: XOR the same number in again and it goes away.

So keep running XORs from the start of the list. The XOR of a run is the running XOR at its end, XORed with the running XOR before its start. The question becomes: which two running XORs differ the most?

To differ the most, two numbers must differ in the highest bit possible, then in the next one, and so on. Put the running XORs seen so far into a tree that branches on each bit, from the top bit down. For a new number, walk down the tree and, at each bit, take the branch with the opposite bit if it exists.

## Definition

**Input.** An array $A[0..n-1]$ of integers with $0 \le A[t] < 2^w$ and $n \ge 1$.

**Output.** The largest value of $A[i] \oplus A[i+1] \oplus \dots \oplus A[j-1]$ over $0 \le i < j \le n$, and one such pair $(i, j)$.

**Prefix form.** With $X[0] = 0$ and $X[t] = X[t-1] \oplus A[t-1]$, the XOR of $A[i..j)$ is $X[i] \oplus X[j]$, since the items before $i$ appear in both and cancel. So the output is $\max_{0 \le i < j \le n} X[i] \oplus X[j]$, the largest XOR of two of the $n + 1$ prefix values.

**Greedy on bits.** For a fixed $x$ and a set $S$, the $y \in S$ that maximizes $x \oplus y$ is found by fixing the bits of $y$ from the highest down: at each bit, choose the value opposite to the bit of $x$ if some element of $S$ with the bits chosen so far has it. A $1$ in a higher bit is worth more than all lower bits together, so this choice is optimal.

## Variants

- **Count the subarrays with XOR equal to $k$.** Count the pairs $i < j$ with $X[i] = X[j] \oplus k$, with a [hash table](/hash-table/) of counts, as in [prefix sum hash counting](/prefix-sum-hash-counting/) for [subarray sum equals k](/subarray-sum-equals-k/).
- **Count the subarrays with XOR less than $k$.** Store a count in each trie node, and walk the trie with the bits of $k$, adding the counts of the subtrees that give a smaller XOR. This takes $O(nw)$ time.
- **Range queries.** The largest XOR of a subarray that ends at $r$ and starts in $[l, r]$, or the largest XOR of a value with an item in a range, with a [persistent trie](/persistent-trie/) over the prefix values, in $O(w)$ time per query.
- **Length bounds.** Subarrays of length at most $U$: keep only the prefix values $X[j - U..j-1]$ in the trie, adding one and removing one per step as in a [sliding window](/sliding-window/), with counts in the nodes.
- **Not contiguous.** The largest XOR of any subset of the items is a different problem, solved by a linear basis over $\mathrm{GF}(2)$, that is [Gaussian elimination on bits](/xor-gaussian-elimination/), in $O(nw)$ time.
- **Smallest XOR.** The smallest XOR of a pair is reached by two values that are adjacent in sorted order, so sorting the prefix values solves the smallest XOR subarray in $O(n \log n)$ time; a trie also works.

## Examples

**A first array.** $A = [8, 1, 2, 12, 7, 6]$, so $X = [0, 8, 9, 11, 7, 0, 6]$. In four bits, $X[1] = 1000$ and $X[4] = 0111$ differ in every bit, so $X[1] \oplus X[4] = 1111 = 15$, the largest possible value. It comes from $A[1..4) = [1, 2, 12]$, and indeed $1 \oplus 2 \oplus 12 = 15$. The pair $X[2] \oplus X[6] = 9 \oplus 6 = 15$ gives a second answer, $[2, 12, 7, 6]$.

**The trie walk.** For $j = 6$, $X[6] = 0110$, and the trie holds $\{0, 8, 9, 11, 7\}$. At bit $3$ the walk wants a $1$ and finds $8, 9, 11$. At bit $2$ it wants a $0$ and keeps all three. At bit $1$ it wants a $0$ and keeps $8, 9$. At bit $0$ it wants a $1$ and ends at $9$. So the best partner of $6$ is $9$, with XOR $15$.

**A cancellation.** $A = [1, 2, 3, 4]$, so $X = [0, 1, 3, 0, 4]$. The prefix $[1, 2, 3]$ has XOR $0$. The answer is $7 = X[2] \oplus X[4] = 3 \oplus 4$, from $[3, 4]$.

**The whole array.** $A = [3, 10, 5, 25, 2, 8]$ has $X[6] = 31 = 11111$, the largest value with five bits, so the whole array is an answer.

## Known algorithms

| method | time | extra space | notes |
|---|---|---|---|
| all pairs | $\Theta(n^2)$ | $O(1)$ | running XOR for each start |
| binary trie of prefix XORs | $O(nw)$ | $O(nw)$ | insert $X[j]$ after querying it; the standard solution |
| bit by bit with a hash set | $O(nw)$ expected | $O(n)$ | fix the answer from the top bit, test each bit with the set of prefixes of the values |
| sort and divide on the top bit | $O(nw)$ | $O(n)$ | split the values by the highest bit where they differ and recurse on pairs of groups |

The hash set method builds the answer $r$ from the top bit down. At bit $b$ it tries $r' = r$ with bit $b$ set, and asks whether two values $x, y$ have $(x \gg b) \oplus (y \gg b) = r' \gg b$, which is a lookup of $(x \gg b) \oplus (r' \gg b)$ in the set of the values $x \gg b$.

## Bounds

**Linear for fixed width.** Each item must be read, so $\Omega(n)$ time is needed. For $w = O(1)$, or $w = O(\log n)$ counted as words, the trie method takes $O(nw)$ bit steps, which is $O(n)$ for a fixed width.

**Space.** The trie has at most $(n + 1)w + 1$ nodes. A compressed trie, or the hash set method, uses $O(n)$ words.

## Reductions

- **To the largest XOR pair.** By the prefix form, the problem on $n$ items is the largest XOR of a pair among $n + 1$ values.
- **From the largest XOR pair.** Given values $v_0, \dots, v_{m-1}$ with $m \ge 2$, set $A[t] = v_t \oplus v_{t+1}$ for $0 \le t \le m - 2$. Then $X[t] = v_0 \oplus v_t$ for every $t$, and $X[i] \oplus X[j] = v_i \oplus v_j$. So the largest XOR subarray of $A$ is the largest XOR pair of the values, and the two problems are equivalent up to $O(n)$ extra work.
- **Analogy with sums.** It is the XOR form of the [maximum subarray problem](/maximum-subarray-problem/). Kadane's method does not apply, because the best XOR ending at $j$ does not follow from the best XOR ending at $j - 1$.

## Applications

- **Contest problems.** A standard use of a binary trie and of the prefix trick for an operation with inverses.
- **Hashing and checksums.** Locating a stretch of a stream of words whose XOR checksum has a given property, such as being $0$, which is the counting variant.
- **Bit tricks.** It is the model for answering "largest XOR with a value in a set" queries, used in many problems on trees and arrays with a persistent trie.

## References
