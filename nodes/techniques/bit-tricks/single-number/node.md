---
tag: D5KZK1
kind: problem
slug: single-number
name: Single number
aliases:
- find the element appearing once
- lonely number
area: techniques/bit-tricks
level: intro
summary: Finding the one element that occurs once when every other element occurs twice, by XOR of all values.
prereqs: [bitwise-operations]
see_also: [xor-swap, xor-linked-list, lowest-set-bit, majority-element-problem, boyer-moore-majority, streaming-model, parity-bit, nim]
sources:
  - url: https://leetcode.com/problems/single-number/
    title: LeetCode 136, Single Number
    locator: the problem statement (linear time and constant extra space)
  - url: https://leetcode.com/problems/single-number-ii/
    title: LeetCode 137, Single Number II
    locator: the problem statement (every other element appears three times)
  - url: https://leetcode.com/problems/single-number-iii/
    title: LeetCode 260, Single Number III
    locator: the problem statement (two elements appear once)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley (2011)
    locator: Section 7.1.3 (Bitwise tricks and techniques), the algebraic laws of the exclusive-or operation
---

The single number problem gives an array in which one value occurs once and every other value occurs exactly twice, and asks for the value that occurs once. The exclusive-or of all elements is the answer, because [XOR](/bitwise-operations/) is associative and commutative and $a \oplus a = 0$, so the pairs cancel. This takes one pass, $n - 1$ XORs and one word of extra space, while the obvious methods use a hash table, with $\Theta(n)$ extra space, or sorting, with $\Theta(n \log n)$ time. The problem is a common interview exercise (LeetCode 136), and its variants with triples and with two single values use the same bit-level counting.

## In plain words

Exclusive-or compares two numbers bit by bit and marks the places where they differ. A number combined with itself gives zero, and zero combined with a number gives the number back. The order of the combinations does not matter.

So if you combine all the numbers of the list, each pair of equal numbers cancels out, wherever its two copies stand. Only the number without a partner is left. You need one running value, and you look at each number once.

## Definition

**Input.** An array $A[1..n]$ of $w$-bit words, with $n = 2m + 1$ for some $m \ge 0$, such that one value $s$ occurs exactly once in $A$ and each other value that occurs in $A$ occurs exactly twice.

**Output.** The value $s$.

**Solution by XOR.** With $\oplus$ the bitwise exclusive-or of $w$-bit words,

$$s = A[1] \oplus A[2] \oplus \dots \oplus A[n].$$

*Proof.* The set of $w$-bit words with $\oplus$ is an abelian group in which $0$ is the identity and every element is its own inverse. Because the group is abelian, the XOR of the array does not depend on the order of the terms, so the terms can be rearranged into the pairs $v \oplus v$ and the single term $s$. Each pair is 0, and $s \oplus 0 \oplus \dots \oplus 0 = s$. $\square$

The words may be read as unsigned or as signed in [two's complement](/twos-complement/): the XOR acts only on bit patterns, so there is no carry and no overflow. In Python, `^` on negative integers uses the infinite two's complement form, and the formula holds for every `int`.

**The general statement.** For every array, the XOR of all elements is the XOR of the values that occur an odd number of times. Seen bit by bit: bit $t$ of the result is the [parity](/bit-parity/) of the number of elements whose bit $t$ is 1.

## Variants

- **Every other value three times.** One value occurs once and each other value occurs three times (LeetCode 137). XOR no longer cancels the triples. For each bit position $t$, count the elements whose bit $t$ is 1; the count modulo 3 is bit $t$ of the single value. This takes $\Theta(nw)$ bit operations, or $\Theta(n)$ word operations with two words `ones` and `twos` that hold the count modulo 3 of every bit position at once: for each $x$, `ones = (ones ^ x) & ~twos`, then `twos = (twos ^ x) & ~ones`; at the end `ones` is the answer. The same idea works for any multiplicity $k$, with a counter modulo $k$ per bit.
- **Two single values.** Two values $a \ne b$ occur once and every other value occurs twice (LeetCode 260). The XOR of all elements is $d = a \oplus b \ne 0$. Its [lowest set bit](/lowest-set-bit/) $d \wedge (-d)$ marks a position where $a$ and $b$ differ. Split the array by this bit and XOR each part: each part holds one of the two values and complete pairs.
- **Missing number.** The array holds $n$ distinct values from $\{0, 1, \dots, n\}$, so one value is missing. The XOR of the array and of $0, 1, \dots, n$ is the missing value, by the same cancellation. The sum formula $n(n+1)/2$ minus the sum of the array also works but can overflow a fixed word.
- **Duplicate in a set.** The array holds $1, \dots, n - 1$ once each, plus one value twice. The XOR of the array and of $1, \dots, n - 1$ is the repeated value.
- **Odd occurrences.** In general the XOR finds the one value that occurs an odd number of times when all others occur an even number of times.
- **Streams.** In the [streaming model](/streaming-model/) the XOR solves the problem in one pass with $w$ bits of memory, independent of $n$.

## Examples

**Basic case.** $A = [4, 1, 2, 1, 2]$. The running XOR after each element is 4, 5, 7, 6, 4, and the answer is 4. In binary: $100 \oplus 001 = 101$, $\oplus\, 010 = 111$, $\oplus\, 001 = 110$, $\oplus\, 010 = 100$.

**Single element.** $A = [7]$; the answer is 7.

**Negative values.** $A = [-3, 5, -3]$. In 8-bit two's complement $-3 = 11111101_2$ and $5 = 00000101_2$; the XOR of all three is $00000101_2 = 5$.

**Triples.** For $A = [2, 2, 3, 2]$ the answer is 3, and for $A = [0, 1, 0, 1, 0, 1, 99]$ it is 99. For $A = [-4, -4, -4, -7]$ it is $-7$: per-bit counts modulo 3 over a 32-bit word give the pattern of $-7$, which must be read back as a signed value.

**Two singles.** For $A = [1, 2, 1, 3, 2, 5]$, the XOR of all is $3 \oplus 5 = 6 = 110_2$, whose lowest set bit is $2 = 010_2$. The elements with this bit set are $2, 3, 2$, with XOR 3; the others are $1, 1, 5$, with XOR 5. The answer is $\{3, 5\}$.

**Missing number.** For $A = [3, 0, 1]$ and $n = 3$, $(3 \oplus 0 \oplus 1) \oplus (0 \oplus 1 \oplus 2 \oplus 3) = 2$.

## Known algorithms

| method | time | extra space | notes |
|---|---|---|---|
| XOR of all elements | $\Theta(n)$ | $\Theta(1)$ words | needs the promise that all others occur twice |
| count with a [hash table](/hash-table/) | $\Theta(n)$ expected | $\Theta(n)$ | works for any multiplicities |
| sort, then scan for the unpaired value | $\Theta(n \log n)$ | depends on the sort | comparison-based |
| sum of distinct values times 2, minus the sum | $\Theta(n)$ expected | $\Theta(n)$ | needs the set of distinct values; can overflow |
| per-bit counting modulo $k$ | $\Theta(nw)$ bit operations | $\Theta(w)$ counters | the $k$-times variant |

## Bounds

Every algorithm must read all $n$ elements in the worst case: if one element is not read, an adversary can make it the single value or a member of a pair, and the answer changes. So the time is $\Omega(n)$ in any model where reading an element costs one step, and the XOR method matches it with $\Theta(n)$ time and $\Theta(1)$ extra words on the [word RAM](/word-ram/). In the [comparison model](/comparison-model/) XOR is not available, and the sorting solution takes $O(n \log n)$ comparisons.

## Reductions

- **To parity.** Bit $t$ of the answer is the parity of the bits at position $t$ of all elements, so the problem is $w$ parallel parity computations; see [bit parity](/bit-parity/).
- **From the swap.** The [XOR swap](/xor-swap/) and the [XOR linked list](/xor-linked-list/) use the same law $a \oplus a = 0$ to recover one value from an XOR of two.
- **Related counting problems.** The [majority element problem](/majority-element-problem/) asks for a value that occurs more than $n/2$ times; it has a different one-pass solution, the [Boyer-Moore majority vote](/boyer-moore-majority/), also in $\Theta(1)$ extra words.

## Applications

- **Recovery of lost data.** A parity block that stores the XOR of $k$ data blocks lets a system rebuild any one lost block as the XOR of the parity block and the $k - 1$ remaining blocks. This is the single-number argument applied to blocks, and it is the idea of [parity bits](/parity-bit/) at the scale of disks.
- **Checking a transfer.** The XOR of all words sent and all words received is 0 if every word arrived; a lost word shows up as the result when all others arrived.
- **Game theory.** In [Nim](/nim/) the XOR of the pile sizes decides the winner; the cancellation of equal piles is the same law.
- **Interview and teaching use.** The problem shows how an algebraic law of a bit operation replaces a data structure.

## References
