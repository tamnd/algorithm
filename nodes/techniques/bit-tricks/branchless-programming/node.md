---
tag: 0WBFSM
kind: technique
slug: branchless-programming
name: Branchless programming
aliases:
- branch-free code
- conditional masks
area: techniques/bit-tricks
level: core
summary: Computing min, max, absolute value and conditionals with masks and arithmetic instead of branches.
prereqs: [twos-complement, bitwise-operations, bitmask]
see_also: [branchless-binary-search, simd-within-a-register, bit-slicing, timing-attack, sample-sort, lomuto-partition, sorting-network, table-lookup]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 2-4, Absolute Value Function; Section 2-12, Comparison Predicates; Section 2-19, Doz, Max, Min; Section 2-20, Exchanging Registers
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
  - paper: doi:10.1007/978-3-540-30140-0_69
    title: Peter Sanders and Sebastian Winkel, Super scalar sample sort, Algorithms, ESA 2004, Lecture Notes in Computer Science 3221
    locator: pp. 784 to 796
---

Branchless programming replaces a conditional jump by straight-line code that computes both outcomes, or a mask, and combines them with arithmetic and Boolean operations. The basic tool is the mask $-[c]$, which is all ones when the condition $c$ holds and all zeros otherwise, so that `(a AND m) OR (b AND NOT m)` selects $a$ or $b$ without a jump. Warren collects the standard forms for absolute value, minimum, maximum, comparison predicates and the difference or zero in Chapter 2 of Hacker's Delight. The method pays when a branch is hard to predict, as in the inner loops of sorting and searching, and it is required in cryptographic code, where the time must not depend on secret data.

## In plain words

A modern processor guesses which way each "if" will go and starts working on that path before it knows. When it guesses wrong it throws the work away, which costs about as much as a dozen or more simple instructions. If the condition is random, it guesses wrong half of the time.

Branchless code avoids the guess. It computes the condition as a number, 0 or 1, turns it into a mask of all zeros or all ones, and uses the mask to pick the answer. The code always runs the same instructions, so there is nothing to guess and nothing to throw away.

## When it applies

- The condition depends on data in a way the branch predictor cannot learn, such as comparisons of random keys in a sort or a search.
- Both outcomes are cheap to compute, so computing both costs less than a misprediction.
- The code must take the same time for all inputs, as in cryptography, where a branch on a secret value leaks it through a [timing attack](/timing-attack/).
- The code runs on many lanes at once, as in [SIMD within a register](/simd-within-a-register/), vector units or [bit slicing](/bit-slicing/), where different lanes would need different branches.

## The template

All values are $w$-bit two's complement words. Write $[c]$ for 1 if $c$ holds and 0 otherwise, and $x \gg_s k$ for the arithmetic right shift, which copies the sign bit.

1. **Compute the condition as 0 or 1.** Use a comparison that the machine evaluates without a jump (SETcc on x86, a compare into a register on others), or a formula from Warren, Section 2-12.
2. **Make a mask.** $m = -[c]$ is all ones or all zeros. For the sign of $x$, $m = x \gg_s (w - 1)$ directly.
3. **Combine.** Select with $(a \mathbin{\&} m) \mathbin{|} (b \mathbin{\&} \lnot m)$, or with $b \oplus ((a \oplus b) \mathbin{\&} m)$, which uses one register less. Add a conditional amount with $x + (d \mathbin{\&} m)$.
4. **Check the machine code.** Compilers turn some branches into conditional moves by themselves, and turn some branchless code back into branches.

**Standard forms.** With $s = x \gg_s (w - 1)$:

| task | branchless form | note |
| --- | --- | --- |
| $\lvert x \rvert$ | $(x \oplus s) - s$ | for $x = -2^{w-1}$ the result is $-2^{w-1}$ |
| $\min(x, y)$ | $y \oplus ((x \oplus y) \mathbin{\&} -[x < y])$ | |
| $\max(x, y)$ | $x \oplus ((x \oplus y) \mathbin{\&} -[x < y])$ | |
| $\operatorname{sign}(x)$ | $(x \gg_s (w - 1)) \mathbin{\vert} ((-x) \gg_u (w - 1))$ | $\gg_u$ is the logical shift |
| doz, $\max(x - y, 0)$ unsigned | $(x - y) \mathbin{\&} -[x \ge y]$ | |

For example, with $w = 8$ and $x = -6$ = 0xFA: $s$ = 0xFF $= -1$, $x \oplus s = 5$, and $5 - (-1) = 6$.

## Classic examples

- **Minimum, maximum and absolute value.** The forms above, from Warren, Sections 2-4 and 2-19.
- **Branchless binary search.** Keep a base pointer and a length; at each step, `base += (a[base + half] < key) * half`, so the loop has a fixed number of steps and no data-dependent branch. See [branchless binary search](/branchless-binary-search/).
- **Partitioning in quicksort.** Write each element to the output and advance the output index by $[a_i < p]$, as in a branch-free [Lomuto partition](/lomuto-partition/). The loop does the same work for every element.
- **Sample sort.** Sanders and Winkel classify each element into one of $k$ buckets by walking an implicit search tree of splitters with $j \leftarrow 2j + [a > s_j]$, with no branches, and report that this makes their [sample sort](/sample-sort/) faster than quicksort-based library sorts on the machines they tested.
- **Sorting networks.** A compare-exchange is `lo = min(a, b); hi = max(a, b)`, which is branch-free with the forms above, so a [sorting network](/sorting-network/) is a branch-free sort for small arrays.
- **Constant-time comparison.** To compare two secret byte strings, OR together the XORs of all byte pairs and test the result once at the end, instead of returning at the first difference.

## Variations

- **Conditional move instructions.** CMOV on x86 and CSEL on ARM select between two registers without a jump. They do the work of step 3 in one instruction.
- **Predication.** Some instruction sets attach a condition to each instruction, which turns a short "if" into straight-line code.
- **Arithmetic selection.** $a + [c] (b - a)$ selects with a multiplication, which is convenient in high-level languages, and also works for floating-point values.
- **Table selection.** Store the two outcomes in a two-entry array and index it by $[c]$. This turns a control dependence into a data dependence, but the memory access can leak the index through the cache.
- **Vector masks.** Vector compare instructions produce lane masks directly, and blend instructions select by them.

## Pitfalls

- **Overflow.** The tempting form $\min(x, y) = y + ((x - y) \mathbin{\&} ((x - y) \gg_s (w - 1)))$ is wrong when $x - y$ overflows: with $w = 8$ it gives a wrong result for 16384 of the 65536 pairs. Use the comparison form.
- **Arithmetic shift of signed values.** In C before C23 the right shift of a negative signed value is implementation-defined, and $\lvert -2^{w-1} \rvert$ overflows. Use unsigned types and an explicit mask where it matters.
- **Slower when the branch is predictable.** A well-predicted branch costs almost nothing, while branchless code always computes both outcomes and adds a data dependence. Measure on real data.
- **Longer dependency chains.** A conditional move makes the next step wait for the comparison; a predicted branch lets the processor run ahead. In a binary search over a large array this can matter more than mispredictions, and prefetching both candidates helps.
- **The compiler may undo it.** An optimizer can turn branchless source code into a branch, or a branch into a conditional move. For constant-time code, check the generated machine code.

## Exercises

1. Prove that $(x \oplus s) - s$ with $s = x \gg_s (w - 1)$ equals $\lvert x \rvert$ for $-2^{w-1} < x < 2^{w-1}$, and find its value for $x = -2^{w-1}$.
2. Find the pairs $(x, y)$ of 8-bit signed values for which the overflow form of $\min$ in the pitfalls is wrong, and count them.
3. Write a branch-free routine that clamps $x$ to the interval $[lo, hi]$, and prove it correct when $lo \le hi$.
4. Write a branch-free merge step that takes the smaller head of two sorted arrays and advances the right index, and count its instructions.
5. Give a branch-free test, from Boolean operations only, that returns all ones when two $w$-bit words are equal and 0 otherwise. Hint: with $d = x \oplus y$, the word $(d \mathbin{|} -d) \gg_s (w - 1)$ is all ones exactly when $d \ne 0$.

## References
