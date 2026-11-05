---
tag: PDA2C6
kind: problem
slug: maximum-product-subarray
name: Maximum product subarray
aliases:
- maximum subarray product
area: sequences/subarray-problems
level: core
summary: Contiguous run with the largest product; negative values can flip the sign, so both extremes must be tracked.
prereqs: [maximum-subarray-problem, subarray]
see_also: [kadane-max-product, kadane-algorithm, maximum-circular-subarray-sum, sliding-window-positive-sum, prefix-sums, adversary-argument, optimal-substructure, maximum-density-segment]
sources:
  - url: https://leetcode.com/problems/maximum-product-subarray/
    title: LeetCode, problem 152, Maximum Product Subarray
    locator: problem statement (integer items, a non-empty subarray, the answer fits in 32 bits)
  - url: https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/
    title: LeetCode, problem 1567, Maximum Length of Subarray With Positive Product
    locator: problem statement
  - url: https://leetcode.com/problems/subarray-product-less-than-k/
    title: LeetCode, problem 713, Subarray Product Less Than K
    locator: problem statement (positive integer items)
  - paper: doi:10.1145/358234.381162
    title: "Jon Bentley, Programming pearls: algorithm design techniques, Communications of the ACM 27(9) (1984), 865-873"
    locator: the sum version of the problem and its linear scan
---

The maximum product subarray problem asks, for an array of numbers, for the [subarray](/subarray/) of consecutive items whose product is largest. It looks like the [maximum subarray problem](/maximum-subarray-problem/) with multiplication in place of addition, but signs make it different. A negative item turns the largest product into the smallest and the smallest into the largest, and a zero resets everything. So the best product that ends at a position does not follow from the best product that ends one step before alone. It also needs the smallest one. With both, one scan solves the problem in $\Theta(n)$ time and $O(1)$ extra space, the [max-product scan with minimum tracking](/kadane-max-product/).

## In plain words

You have a list of numbers, some negative and maybe some zero. You want one stretch of neighbors whose numbers, multiplied together, give the largest result.

With sums, a bad stretch so far is just thrown away. With products, a very negative result so far is not useless: one more negative number turns it into a very large positive result. So you must remember both the largest and the smallest product of a stretch that ends where you are. A zero kills every stretch that contains it, so the list falls apart into pieces between the zeros. Numbers between $-1$ and $1$ make products smaller, so the longest stretch is not always the best.

## Definition

**Input.** An array $A[0..n-1]$ of real numbers, with $n \ge 1$.

**Output.** Indices $0 \le i \le j \le n - 1$ that maximize
$$\Pi(i, j) = A[i] \cdot A[i+1] \cdots A[j],$$
and the value $\Pi^* = \max_{i \le j} \Pi(i, j)$. The subarray must be non-empty. If the empty subarray is allowed, its product is $1$.

**Why the sum methods fail.** Let $E^{+}(j)$ and $E^{-}(j)$ be the largest and the smallest product of a subarray that ends at $j$. For sums, the best sum that ends at $j$ depends only on the best one at $j - 1$. For products,
$$E^{+}(j) = \max\bigl(A[j],\ A[j] E^{+}(j-1),\ A[j] E^{-}(j-1)\bigr),$$
and the symmetric rule holds for $E^{-}(j)$. When $A[j] < 0$, the largest new product comes from the *smallest* old one. Products also have no inverse when an item is $0$, so the prefix-sum trick, which divides a large prefix product by a small one, breaks at zeros.

## Variants

- **Integer items.** If every non-zero item has $|A[k]| \ge 1$, then in each block between zeros the best product uses the whole block if it has an even number of negative items, and otherwise the block without its prefix up to the first negative item, or without its suffix from the last negative item. This gives a simple linear algorithm with no minimum to track.
- **Positive items.** If every item is positive, then $\log \Pi(i, j) = \sum_{k=i}^{j} \log A[k]$, and the problem is the maximum subarray problem on the logarithms.
- **Longest subarray with a positive product.** The length, not the size, of the product matters; this is LeetCode problem 1567. Track the first index of an even and an odd count of negative items since the last zero.
- **Product below a bound.** Count or find the subarrays with product less than $k$, for positive items. A [sliding window](/sliding-window-positive-sum/) does it in linear time, as in LeetCode problem 713.
- **Circular.** On a ring the complement trick of the [maximum circular subarray sum](/maximum-circular-subarray-sum/) does not work, because a total product cannot be divided by a zero product. Double the array and bound the length by $n$.
- **Largest absolute value.** The largest $|\Pi(i, j)|$ is the largest product of the absolute values, a positive-item problem when there is no zero.

## Examples

**A sign flip.** For $A = [2, 3, -2, 4]$ the answer is $6$, from $[2, 3]$. The whole array has product $-48$.

**Two negatives.** For $A = [-2, 3, -4]$ the answer is $24$, the whole array. After $[-2, 3]$ the largest product that ends at $3$ is $3$, but the smallest is $-6$, and $-6 \cdot (-4) = 24$.

**Zeros.** For $A = [-2, 0, -1]$ the answer is $0$, from $[0]$. Each block between the zeros has only one negative item.

**Small items.** For $A = [0.5, 4, 0.5]$ the answer is $4$, from $[4]$. The whole array has product $1$, so the integer rule of taking the whole block fails for items between $-1$ and $1$.

**One item.** For $A = [-3]$ the answer is $-3$.

## Known algorithms

| method | time | extra space | items |
|---|---|---|---|
| all pairs with running products | $\Theta(n^2)$ | $O(1)$ | any |
| [max-product scan with minimum tracking](/kadane-max-product/) | $\Theta(n)$ | $O(1)$ | any |
| split at zeros, count negatives | $\Theta(n)$ | $O(1)$ | $\lvert x \rvert \ge 1$ or $x = 0$ |
| best prefix and suffix products, reset at zeros | $\Theta(n)$ | $O(1)$ | $\lvert x \rvert \ge 1$ or $x = 0$ |
| logarithms and [Kadane's algorithm](/kadane-algorithm/) | $\Theta(n)$ | $O(1)$ | positive |

**Prefix and suffix products.** For integer items, the best product of a block between zeros is a prefix or a suffix of the block, by the rule of the even and odd counts above. So the largest of all running products from the left and from the right, each restarted after a zero, together with $0$ if there is a zero, is the answer. This works only with $|x| \ge 1$: for $[0.5, 4, 0.5]$ every prefix and suffix product is at most $2$.

## Bounds

**Linear time is optimal.** If an algorithm does not read $A[k]$, an adversary chooses $A[k]$ large enough, or $0$, to change the answer, so every item must be read and $\Omega(n)$ time is needed. This is an [adversary argument](/adversary-argument/). The scan with minimum tracking reaches it.

**Size of the numbers.** With integer items of $b$ bits, the answer can have up to $n b$ bits, so the word-RAM bound of $\Theta(n)$ holds only if the products fit in a word, as in LeetCode 152. With exact big integers, the cost of the multiplications dominates. Working with logarithms and signs avoids the growth but brings rounding.

## Reductions

- **Positive items to sums.** For positive items, taking logarithms turns the problem into the maximum subarray problem, and exponentials turn it back. So the two problems are the same for positive items, up to rounding.
- **Zeros split the problem.** A subarray with a zero has product $0$. So the answer is the best over the blocks between zeros, or $0$ if there is a zero and every block has a negative best.
- **Integer items to counting.** For integer items, the question in each block is only about the parity of the number of negative items, which a prefix count answers.

## Applications

- **Growth rates.** For a series of growth factors, such as returns of an investment in successive periods, the product over a run is the total growth, so the best run is a maximum product subarray. With positive factors this is the maximum subarray of the log returns.
- **Teaching.** It is the standard example of a dynamic program whose state must keep two values, the largest and the smallest, because the operation is not monotone.

## References
