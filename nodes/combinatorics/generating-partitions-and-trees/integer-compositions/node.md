---
tag: FABZ4B
kind: problem
slug: integer-compositions
name: Integer compositions
aliases:
- Ordered partitions
- Weak compositions
- Compositions of an integer
area: combinatorics/generating-partitions-and-trees
level: intro
summary: Enumerate all ways to write n as an ordered sum of positive integers; there are 2^(n-1) compositions of n for n at least 1.
complexity:
  vars: {n: the integer that is split, N: "the number of compositions, 2^(n-1)"}
  time: {worst: Ω(N)}
prereqs: [combinatorial-generation]
see_also: [composition-generation, counting-integer-compositions, integer-partitions, stars-and-bars, power-set-enumeration, lexicographic-combinations, binary-reflected-gray-code, binomial-coefficient]
sources:
  - book: isbn:9781107602625
    title: Richard P. Stanley, Enumerative Combinatorics, Volume 1, second edition, Cambridge University Press, 2012
    locator: Section 1.2, How to count (compositions, compositions with k parts and weak compositions)
  - book: isbn:9780521637664
    title: George E. Andrews, The Theory of Partitions, Cambridge University Press, 1998 (first published 1976)
    locator: Chapter 4, Compositions and Simon Newcomb's problem, pages 54 to 67
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 5, Next composition of n into k parts (NEXCOM), and Chapter 6, Random composition of n into k parts (RANCOM)
---

The composition problem asks for a list of all compositions of $n$: the ways to write $n$ as a sum of positive integers when the order of the terms matters. Each composition of $n \ge 1$ is fixed by the set of places where the sum is cut, so there are $2^{n-1}$ of them, and $\binom{n-1}{k-1}$ with exactly $k$ parts. The problem is the ordered twin of the [integer partition problem](/integer-partitions/), and it reduces to listing subsets, so [composition generation](/composition-generation/) runs in constant amortized time.

## In plain words

Put a row of identical coins on a table and cut the row into groups. Keep the groups in their order from left to right. Each way to cut gives a list of group sizes, and two lists are different when they differ in any place, even if they hold the same numbers. The task is to list every such cut once.

There is a gap between each two neighbor coins, and each gap is either cut or not. So the cuts are just a choice of gaps, and listing them is the same as listing all subsets of the gaps. The count doubles each time you add a coin.

## Definition

**Notation.** $n \ge 0$ is the integer to split, $[m] = \{1, \ldots, m\}$, and $C(m, j) = \binom{m}{j}$.

**Composition.** A composition of $n$ is a sequence $c = (c_1, \ldots, c_m)$ of integers $c_i \ge 1$ with $c_1 + \cdots + c_m = n$. The $c_i$ are its parts and $m$ is its length. The empty sequence is the one composition of $0$.

**Problem.** Given $n$, output each composition of $n$ exactly once.

**The cut set.** For $n \ge 1$, map $c$ to its set of partial sums

$$S(c) = \{c_1,\ c_1 + c_2,\ \ldots,\ c_1 + \cdots + c_{m-1}\} \subseteq [n-1].$$

The map is a bijection from the compositions of $n$ onto the subsets of $[n-1]$. *Proof.* The partial sums strictly increase, because each part is at least $1$, and they lie between $1$ and $n - 1$, so $S(c)$ is a subset of $[n - 1]$ with $m - 1$ elements. Conversely, a subset $\{s_1 < \cdots < s_{m-1}\}$ gives the composition with parts $s_1 - s_0, s_2 - s_1, \ldots, s_m - s_{m-1}$, where $s_0 = 0$ and $s_m = n$; these parts are positive and add up to $n$. The two maps are inverse. $\square$

**Counts.** By the bijection, for $n \ge 1$:

- the number of compositions of $n$ is $2^{n-1}$;
- the number with exactly $k$ parts is $C(n-1, k-1)$, for $1 \le k \le n$;
- the total number of parts over all compositions is $\sum_{S \subseteq [n-1]} (|S| + 1) = 2^{n-1} + (n-1)\, 2^{n-2} = (n+1)\, 2^{n-2}$.

The generating function is $\sum_{n \ge 0} c(n)\, x^n = \frac{1}{1 - x/(1-x)} = \frac{1 - x}{1 - 2x}$, because a composition is a sequence of parts and one part has the series $x + x^2 + \cdots = \frac{x}{1-x}$.

## Variants

- **Exactly $k$ parts.** List the $C(n-1, k-1)$ compositions of length $k$. These are the $(k-1)$-subsets of $[n-1]$.
- **Weak compositions.** Parts may be $0$. A weak composition of $n$ into exactly $k$ parts is a sequence $(c_1, \ldots, c_k)$ of non-negative integers with sum $n$. Adding $1$ to each part gives a composition of $n + k$ into $k$ parts, so there are $C(n + k - 1, k - 1)$ of them; this is [stars and bars](/stars-and-bars/). Without a fixed $k$ the number of weak compositions is infinite, so $k$ is always given.
- **Restricted parts.** Parts lie in a set $A$. The count $c_A(n)$ satisfies $c_A(0) = 1$ and $c_A(n) = \sum_{a \in A,\ a \le n} c_A(n - a)$, by the value of the last part. For $A = \{1, 2\}$ this is the Fibonacci number $F_{n+1}$, for odd parts it is $F_n$, and for parts at least $2$ it is $F_{n-1}$ (with $F_1 = F_2 = 1$ and $n \ge 1$, and $n \ge 2$ in the last case).
- **Bounded parts.** Parts at most $b$. The count follows the same recurrence with $A = [b]$, a $b$-step Fibonacci sequence.
- **Order.** Lexicographic order of the part sequences, or a Gray code in which one step merges two neighbor parts or splits one part in two.
- **Counting, ranking and sampling.** Count, rank or sample one composition without the list. The cut set makes all three easy: the rank is a binary number of $n - 1$ digits, and a uniform random composition is a uniform random subset of $[n - 1]$.

## Examples

**$n = 4$.** The $2^3 = 8$ compositions in lexicographic order, with their cut sets:

| composition | cut set | parts |
| --- | --- | --- |
| $1, 1, 1, 1$ | $\{1, 2, 3\}$ | $4$ |
| $1, 1, 2$ | $\{1, 2\}$ | $3$ |
| $1, 2, 1$ | $\{1, 3\}$ | $3$ |
| $1, 3$ | $\{1\}$ | $2$ |
| $2, 1, 1$ | $\{2, 3\}$ | $3$ |
| $2, 2$ | $\{2\}$ | $2$ |
| $3, 1$ | $\{3\}$ | $2$ |
| $4$ | $\{\}$ | $1$ |

By length there are $1, 3, 3, 1$ compositions with $1, 2, 3, 4$ parts, which are $C(3, 0), \ldots, C(3, 3)$. The total number of parts is $20 = 5 \cdot 2^{2}$. Only $5$ of these $8$ are [partitions](/integer-partitions/) once sorted, since $p(4) = 5$: $(1, 1, 2)$, $(1, 2, 1)$ and $(2, 1, 1)$ sort to the same partition, and so do $(1, 3)$ and $(3, 1)$.

**Parts $1$ and $2$.** The compositions of $4$ with parts in $\{1, 2\}$ are $1111$, $112$, $121$, $211$ and $22$, which is $F_5 = 5$. They are the ways to climb $4$ stairs with steps of size $1$ or $2$.

**Weak compositions.** The weak compositions of $2$ into $3$ parts are $(2, 0, 0)$, $(1, 1, 0)$, $(1, 0, 1)$, $(0, 2, 0)$, $(0, 1, 1)$ and $(0, 0, 2)$, which is $C(4, 2) = 6$.

**Non-examples.** $(2, 0, 2)$ is not a composition of $4$, because a part is $0$; it is a weak composition into $3$ parts. $(1, 2)$ is not a composition of $4$, because its sum is $3$.

## Known algorithms

| method | order | time for each composition | notes |
| --- | --- | --- | --- |
| [Lexicographic successor](/composition-generation/) | lexicographic | $O(1)$ amortized, CAT | $2^{n-1} - n$ extra writes in all |
| Binary counter on the cut set | lexicographic or reverse | $O(1)$ amortized | the [binary counter](/binary-counter-increment/) |
| [Gray code](/binary-reflected-gray-code/) on the cut set | one merge or split | $O(1)$ worst case | loopless with a linked list of parts |
| [Combinations](/lexicographic-combinations/) of $[n-1]$ | lexicographic | $O(1)$ amortized | exactly $k$ parts |
| NEXCOM (Nijenhuis and Wilf) | their order | $O(1)$ amortized | weak compositions into $k$ parts |
| Recursion on the first part | lexicographic | $O(1)$ amortized | simple, depth up to $n$ |

All of these output each composition as a change to the previous one. Copying each composition out costs its length, so a full list of copies costs $\Theta((n+1)\, 2^{n-2})$.

## Bounds

- **Output.** Each method visits $N = 2^{n-1}$ compositions, so it needs $\Omega(N)$ time. The CAT and loopless methods meet this bound.
- **Copies.** Writing each composition in full costs $\Omega(n\, 2^{n-1})$ in total, since the average length is $(n + 1)/2$.
- **Counting.** The count $2^{n-1}$ is an exact integer of $n - 1$ bits, so counting takes $O(1)$ word operations as a shift, or $O(n)$ bit operations. For restricted parts, the recurrence takes $O(n\, |A|)$ big integer additions, on numbers of $O(n)$ bits.

## Reductions

- **To subsets.** The cut set is a bijection with the subsets of $[n - 1]$, so each [subset enumeration](/power-set-enumeration/) method lists compositions, and each Gray code for subsets gives a Gray code for compositions.
- **Exactly $k$ parts to combinations.** The compositions with $k$ parts match the $(k-1)$-subsets of $[n-1]$, which [combination generation](/lexicographic-combinations/) lists.
- **Weak compositions to compositions.** Add $1$ to each part, as in [stars and bars](/stars-and-bars/). Weak compositions of $n$ into $k$ parts also match the multisets of size $n$ from $[k]$.
- **Partitions as sorted compositions.** A [partition](/integer-partitions/) is a composition with non-increasing parts. Filtering compositions gives partitions, but it wastes most of the work, since $p(n)/2^{n-1} \to 0$.
- **Conjugate composition.** The complement of the cut set in $[n-1]$ gives another composition of $n$, the conjugate, and this is an involution on compositions.

## Applications

- **Ordered sums and tilings.** The compositions of $n$ with parts in $A$ are the tilings of a $1 \times n$ strip with tiles of lengths in $A$, and the ways to climb $n$ stairs with step sizes in $A$.
- **Splitting a sequence.** The ways to cut a sequence of $n$ items into consecutive non-empty blocks are the compositions of $n$. A brute force check of a segmentation method, such as optimal line breaking, runs over them.
- **Distribution of identical items.** Weak compositions into $k$ parts are the ways to put $n$ identical items into $k$ labeled boxes.
- **Descent sets.** The descent set of a [permutation](/permutation/) of $[n]$ is a subset of $[n - 1]$, so it is a composition of $n$. This links compositions with the counting of permutations by their descents.
- **Number theory.** Andrews (Chapter 4) counts compositions by their parts and treats Simon Newcomb's problem with them.

## References
