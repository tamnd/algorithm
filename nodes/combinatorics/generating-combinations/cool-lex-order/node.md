---
tag: T6JKA4
kind: algorithm
slug: cool-lex-order
name: Cool-lex order for combinations
aliases:
- cool-lex generation
- Williams cool-lex
- cool-lex
- suffix-rotated order of combinations
- prefix shift generation of combinations
area: combinatorics/generating-combinations
level: research
summary: Order of the k-subsets as bit strings in which each step rotates a short prefix by one place, with a loopless generator.
solves: [k-subset-enumeration]
model: word-ram
complexity:
  vars: {n: the length of the bit strings, k: the number of ones, N: the number of k-subsets}
  time: {worst: Θ(n+N), amortized: Θ(1)}
  space: {extra: Θ(1)}
properties: {in_place: true, deterministic: true, comparison: false, recursive: false}
history:
  year: 2005
  people: [Frank Ruskey, Aaron Williams]
  note: Ruskey and Williams presented the order at COCOON 2005 and gave the full treatment in Discrete Mathematics in 2009.
prereqs: [lexicographic-combinations, colexicographic-order, loopless-generation]
see_also: [colexicographic-order, fixed-weight-binary-strings, ehrlich-loopless-combinations, loopless-generation, gospers-hack, combinatorial-ranking-and-unranking, combination-gray-code-generation, lexicographic-combinations]
sources:
  - paper: doi:10.1016/j.disc.2007.11.048
    title: Frank Ruskey and Aaron Williams, The coolest way to generate combinations, Discrete Mathematics 309(17), 2009, 5305-5320
    locator: Section 2 (the iterative and recursive definitions and Theorem 1), Section 3 (the loopless and branchless algorithms) and Section 4 (Theorem 2, the rank)
  - paper: doi:10.1007/11533719_58
    title: Frank Ruskey and Aaron Williams, Generating combinations by prefix shifts, Computing and Combinatorics, COCOON 2005, Lecture Notes in Computer Science 3595, Springer, 2005
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (the suffix-rotated order and its loopless program, in an exercise with a solution by Aaron Williams)
---

Cool-lex order lists the bit strings of length $n$ with $k$ ones, that is, the $k$-subsets of $[n]$, by one simple rule: find the shortest prefix that ends in $010$ or $011$, or take the whole string if there is none, and rotate that prefix one place to the right. Starting from $1^k 0^{n-k}$, this rule visits each string once and comes back to the start. Each step changes two or four bits. A program with two indices and a fixed number of assignments makes each step, so the generator is [loopless](/loopless-generation/). Frank Ruskey and Aaron Williams found the order and named it for its likeness to [colexicographic order](/colexicographic-order/).

## In plain words

Write a choice of $k$ items from $n$ as a row of $n$ bits, with a $1$ for each chosen item. Start with all the ones on the left.

To get the next row, read from the left until you first see a $0$ followed by a $1$, and take one more bit. Now take the last bit of this piece and move it to the front. All the other bits of the piece move one place to the right. If the row has no $0$ followed by a $1$ and one more bit, use the whole row.

This rule visits every row once. Each step changes at most four bits, and a program can find these bits at once from two numbers that it keeps up to date. So the time between two rows is always small.

## The problem

Given $0 \le k \le n$, visit each bit string $b_1 b_2 \cdots b_n$ with exactly $k$ ones once. The string is the characteristic vector of a $k$-subset of $[n]$, so this is [k-subset enumeration](/k-subset-enumeration/) in the form of [fixed-weight binary strings](/fixed-weight-binary-strings/). The aim is $O(1)$ time between two visits in the worst case.

**The successor.** For a string $b$, let $p(b)$ be its shortest prefix that ends in $010$ or $011$, or all of $b$ if no such prefix exists. Let $\sigma(b)$ be $b$ with $p(b)$ rotated one place to the right: the last bit of $p(b)$ moves to the front. Cool-lex order is the list $1^k 0^{n-k}, \sigma(1^k 0^{n-k}), \sigma^2(1^k 0^{n-k}), \ldots$ of $N = C(n, k)$ strings.

**The recursion.** Let $L(s, t)$ be the cool-lex list with $s$ zeros and $t$ ones. Then $L(s, 0) = (0^s)$, $L(0, t) = (1^t)$, and for $s, t \ge 1$
$$L(s, t) = L(s - 1, t)\,0,\quad L(s, t - 1)\,1 \text{ without its first string},\quad 1^{t-1} 0^s 1.$$
Here $L\,0$ means each string of $L$ with a $0$ added at the end. Colex order has the recursion $L(s - 1, t)\,0, L(s, t - 1)\,1$. Ruskey and Williams write the same recursion as $W_{s,t} = W_{s-1,t}0, W_{s,t-1}1, 1^{t-1}0^s1$, with the list $1^t 0^s, W_{s,t}$.

## The algorithm

The program keeps two indices. Before each step except the first, $y$ is the position of the first $0$, and $x$ is the position of the first $1$ after it. So the first $01$ in $b$ is at positions $x - 1$ and $x$, and $p(b) = b_1 \cdots b_{x+1}$.

```pseudo id=main
COOL-LEX(n, k)                         ▷ 1 ≤ k ≤ n; visit the strings b[1 .. n] with k ones
L1  b[i] ← 1 for 1 ≤ i ≤ k;  b[i] ← 0 for k < i ≤ n
L2  x ← k;  y ← k
L3  visit b
L4  while x < n
L5      b[x] ← 0;  b[y] ← 1;  x ← x + 1;  y ← y + 1
L6      if b[x] = 0 then
L7          b[x] ← 1;  b[1] ← 0
L8          if y > 2 then x ← 2
L9          y ← 1
L10     visit b
```

Line L5 moves the first $1$ after the first block of zeros to the front of that block. If the next bit is $1$, the prefix ended in $011$, and this is the whole rotation. If the next bit is $0$, the prefix ended in $010$, and line L7 moves that $0$ to the front of the string. Lines L8 and L9 then find the new first $0$ and the new first $01$ with no search: the string now starts with $0$, and the next $1$ is at position $2$ unless the old string started with $0$. The loop stops at the last string, $1^{k-1} 0^{n-k} 1$, where the first $01$ ends at position $n$.

For $k = 0$ there is one string, $0^n$. For $k = n$ the loop does not run.

## Example

Take $n = 5$ and $k = 3$. The table shows each string, the indices at the visit, and the bits that the next step changes.

| visit | $b$ | set | $x$ | $y$ | $p(b)$ | next step |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | $11100$ | $\{1, 2, 3\}$ | 3 | 3 | $11100$ | L7, y > 2, so 2 bits |
| 1 | $01110$ | $\{2, 3, 4\}$ | 2 | 1 | $011$ | L5 only, 2 bits |
| 2 | $10110$ | $\{1, 3, 4\}$ | 3 | 2 | $1011$ | L5 only, 2 bits |
| 3 | $11010$ | $\{1, 2, 4\}$ | 4 | 3 | $11010$ | L7, 4 bits |
| 4 | $01101$ | $\{2, 3, 5\}$ | 2 | 1 | $011$ | L5 only, 2 bits |
| 5 | $10101$ | $\{1, 3, 5\}$ | 3 | 2 | $1010$ | L7, 4 bits |
| 6 | $01011$ | $\{2, 4, 5\}$ | 2 | 1 | $010$ | L7 with $y = 2$, 2 bits |
| 7 | $00111$ | $\{3, 4, 5\}$ | 3 | 1 | $0011$ | L5 only, 2 bits |
| 8 | $10011$ | $\{1, 4, 5\}$ | 4 | 2 | $10011$ | L5 only, 2 bits |
| 9 | $11001$ | $\{1, 2, 5\}$ | 5 | 3 | $11001$ | stop |

At visit $3$, the prefix $11010$ ends in $010$. Its rotation is $01101$: line L5 makes $11100$, and line L7 sets $b_5 = 1$ and $b_1 = 0$. The rotation of the last string $11001$ would give $11100$ again, so the list is a cycle.

For $k = 2$ the list is $11000, 01100, 10100, 01010, 00110, 10010, 01001, 00101, 00011, 10001$.

## Correctness

The proof file has the full argument. It has two parts.

1. **The program computes $\sigma$.** Write the string as $1^a 0^m 1 c \cdots$, with $y = a + 1$ and $x = a + m + 1$. If $c = 1$, the rotation of $1^a 0^m 1 1$ is $1^{a+1} 0^m 1$, which changes only $b_y$ and $b_x$, and both indices go up by one. If $c = 0$, the rotation of $1^a 0^m 1 0$ is $0 1^a 0^m 1$, which line L7 completes. The new first $0$ is at $1$, and the new first $1$ after it is at $2$ if $a \ge 1$, or at $m + 2$ if $a = 0$. Line L8 tests $a \ge 1$ as $y > 2$.
2. **The orbit of $\sigma$ is the recursive list.** By induction on $s + t$, consecutive strings of $L(s, t)$ satisfy $v = \sigma(u)$. Inside the first block, adding a $0$ at the end does not change the shortest prefix, except at the last string of $L(s-1, t)$. Inside the second block, adding a $1$ does not change it either. At the two joins, a direct check shows that $\sigma$ gives the next string. The blocks hold the strings that end in $0$, and then those that end in $1$, so each string appears once.

## Complexity

**Each step.** Lines L4 to L9 make at most eight assignments to the string and the indices and three tests, and no line has a loop. So the time between two visits is $O(1)$ in the worst case.

**Total.** Line L1 takes $\Theta(n)$ time, and the $N - 1$ steps take $\Theta(N)$. So the total is $\Theta(n + N)$.

**Bits changed.** A step changes $2$ bits when the prefix ends in $011$, or when it ends in $010$ and the string starts with $0$. It changes $4$ bits otherwise. Ruskey and Williams count the lines of their loopless program. In the terms of this page, line L7 runs $C(n - 1, k)$ times, and for $k \ge 2$ line L8 sets $x \leftarrow 2$ in $C(n - 2, k - 1)$ steps. Apart from the first step, which changes only $2$ bits, these are exactly the steps that change $4$ bits, so there are $C(n - 2, k - 1) - 1$ of them. For $n = 10$ and $k = 5$ this is $69$ of the $251$ steps.

**Space.** The string and two indices.

## Properties

- **Loopless.** The worst-case time between two visits is $O(1)$, and the program needs only $O(1)$ extra space. See [loopless generation](/loopless-generation/).
- **Prefix shifts.** Each step is a rotation of a prefix by one place. Ruskey and Williams state that no other algorithm for combinations has this property.
- **One or two transpositions.** Each step swaps one or two pairs of a $0$ and a $1$. So the order is a Gray code on bit strings, but not a [revolving door](/revolving-door-ordering/) order: some steps change two elements of the set.
- **Cyclic.** The last string $1^{k-1} 0^{n-k} 1$ rotates to the first.
- **Like colex.** The list for $s$ zeros and $t$ ones starts with the list for $s - 1$ zeros and $t$ ones, with a $0$ added, as in [colexicographic order](/colexicographic-order/). The rank formula is also like the colex formula.
- **Rank.** Let $c_1 < \cdots < c_k$ be the positions of the ones, and let $r$ be the least index with $c_r > r$. Ruskey and Williams show that the rank is $\binom{c_r}{r} - 1 + \sum_{j = r + 1}^{k} \left( \binom{c_j - 1}{j} - 1 \right)$, and $0$ if there is no such $r$. For $\{2, 4, 5\}$ this is $(2 - 1) + (3 - 1) + (4 - 1) = 6$. See [ranking and unranking combinations](/combinatorial-ranking-and-unranking/).
- **Not loopless on index lists.** As a list $c_1 < \cdots < c_k$, many entries can change in one step. Ruskey and Williams note that the order cannot be loopless in that form. It is genlex in that form: the sets with the same largest elements are next to each other.

## Variants and improvements

- **Branchless.** Ruskey and Williams give a form with no test: each step swaps $b_x$ with $b_y$ and $b_1$ with $b_{x+1}$, and updates $x$ and $y$ with arithmetic on the bits.
- **Machine words.** When the string fits in one word, a fixed number of word operations makes each step. Knuth gives such a program for MMIX. Compare [Gosper's hack](/gospers-hack/), which gives colex order with word operations.
- **Linked lists.** If the bits are in a singly linked list, the rotation is four pointer changes, so the step is again loopless.
- **Recursion.** The recursive definition gives a CAT program that makes the swaps at the two joins of each level.
- **Multisets.** Ruskey and Williams suggest a similar prefix rotation rule for permutations of a multiset, see [multiset permutations](/multiset-permutations/). They report only tests for it in this paper.
- **Multisets of a fixed size.** Through the stars and bars string, cool-lex order lists [combinations with repetition](/combinations-with-repetition/).

## When to use it

Use it when combinations are bit strings or machine words, and you want a short loopless program, for example in hardware or in a tight inner loop. Use it when you need a rank function for a Gray code of combinations. If the work for each subset must change by one element in and one element out, use a revolving door order, such as [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/). If you need sorted index lists, use the [lexicographic successor](/lexicographic-combinations/).

## Pitfalls

- **The first step.** The first string $1^k 0^{n-k}$ has no $01$, so $x$ and $y$ do not have their usual meaning. The start $x = y = k$ is chosen so that the first pass of the loop gives $0 1^k 0^{n-k-1}$. Do not start with other values.
- **$k = 0$.** The program needs $k \ge 1$. With $k = 0$, line L5 writes $b[0]$. Handle the case apart.
- **The order of the writes.** In line L5, the write $b[x] \leftarrow 0$ must come before $b[y] \leftarrow 1$. At the first step $x = y = k$, and the other order leaves a $0$ there.
- **Reading past the end.** Line L6 reads $b[x]$ after $x$ grows. This is safe because the loop runs only while $x < n$.
- **Index lists.** Do not keep the subset as a sorted array of elements if you need $O(1)$ time for each step. One step can shift many elements of that array.

## Implementations

## History

Frank Ruskey and Aaron Williams presented the order at COCOON 2005, in a paper on generating combinations by prefix shifts. The journal version, "The coolest way to generate combinations", appeared in Discrete Mathematics in 2009. It gives the iterative and recursive definitions, the loopless and branchless programs and the rank. They named the order cool-lex because it is so close to colex order. Knuth includes the order in Section 7.2.1.3, in the form that rotates suffixes because he writes bits from $b_{n-1}$ down to $b_0$, with a loopless program in an exercise whose solution he credits to Williams.

## References
