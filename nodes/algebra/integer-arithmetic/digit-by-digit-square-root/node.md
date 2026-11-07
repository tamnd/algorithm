---
tag: SH6MP2
kind: algorithm
slug: digit-by-digit-square-root
name: Digit-by-digit square root
aliases:
- paper-and-pencil square root
- binary square root algorithm
- restoring square root
area: algebra/integer-arithmetic
level: core
summary: Computes square root one digit at a time in the manner of long division.
solves: [integer-square-root]
model: word-ram
complexity:
  vars: {n: the number of base β digits of the root (the input has 2n digits)}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  note: The method is ancient; the Chinese Nine Chapters on the Mathematical Art describe it, and it was taught in schools in the decimal form until calculators replaced it.
prereqs: [integer-square-root, long-division, positional-number-system]
see_also: [newton-integer-root, integer-nth-root, long-division, restoring-division, non-restoring-division, integer-division]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 21, Square-rooting methods (21.1, the pencil-and-paper algorithm; 21.2, restoring shift/subtract square-rooting; 21.3, binary non-restoring algorithm)
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley, 2012
    locator: Section 11-1, Integer square root (the shift-and-subtract method, one bit of the root per step)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.5.1, Square root (Algorithm 1.12 SqrtRem, the divide-and-conquer method that this algorithm is the base case of)
---

The digit-by-digit square root computes $\lfloor \sqrt A \rfloor$ and the remainder $A - \lfloor \sqrt A \rfloor^2$ of a natural number $A$ one digit of the root at a time, from the most significant digit down, in the same way as [long division](/long-division/). It brings down the digits of $A$ two at a time, and each new root digit $x$ is the largest one with $(2q\beta + x) \cdot x$ at most the current remainder, where $q$ is the root found so far and $\beta$ the base. In base 2 the test reduces to one comparison and one subtraction per bit, which is the restoring square root of hardware. For a root of $n$ digits it takes $\Theta(n^2)$ digit operations; Newton's method and the Karatsuba square root of Brent and Zimmermann are faster for long numbers.

## In plain words

To take the square root of 152399025 by hand, you split the digits into pairs from the right: 1, 52, 39, 90, 25. The first digit of the root is the largest digit whose square fits into the first pair. Then you subtract, bring down the next pair, and look for the next digit.

The rule for the next digit comes from squaring. If the root so far is $q$, and the next digit is $x$, then the new root is ten times $q$ plus $x$, and its square grows by twenty times $q$ times $x$, plus $x$ squared. So you look for the largest $x$ for which $x$ times twenty $q$ plus $x$ fits into what is left. It is the rhythm of long division.

In binary each digit is 0 or 1, so the guess is a single test: does the trial value fit, or not.

## The problem

The input is a natural number $A$ given by its digits in the base $\beta \ge 2$, padded with a leading zero to an even number $2n$ of digits: $A = \sum_{i=0}^{2n-1} a_i \beta^i$. The output is $Q = \lfloor \sqrt A \rfloor$, with $n$ digits, and the remainder $R = A - Q^2$, which satisfies $0 \le R \le 2Q$. This is the [integer square root](/integer-square-root/) problem. The bound $R \le 2Q$ is equivalent to $A < (Q + 1)^2$.

The cost model counts digit operations in the base $\beta$ on a word RAM: a product of an $m$-digit number by one digit, an addition or a subtraction of $m$-digit numbers, and a comparison each cost $\Theta(m)$.

## The algorithm

Write $P_j$ for the number formed by the top $2j$ digits of $A$, so that $P_0 = 0$, $P_{j+1} = P_j \beta^2 + (a_{2k+1} \beta + a_{2k})$ with $k = n - 1 - j$, and $P_n = A$.

```pseudo id=main
DIGIT-SQRT(A, β)                        ▷ A has digits a[2n − 1] … a[0] in base β
L1  q ← 0, r ← 0
L2  for k ← n − 1 downto 0 do
L3      r ← r · β² + a[2k + 1] · β + a[2k]          ▷ bring down the next pair
L4      x ← the largest digit in 0 .. β − 1 with (2qβ + x) · x ≤ r
L5      r ← r − (2qβ + x) · x
L6      q ← q · β + x                                ▷ append the digit x to the root
L7  return (q, r)
```

The term $(2q\beta + x) \cdot x$ is the growth of the square: $(q\beta + x)^2 = q^2 \beta^2 + (2q\beta + x)\, x$. By hand, the number $2q\beta + x$ is written as "twice the root so far, with the digit $x$ appended". Line L4 can search the $\beta$ candidates by binary search, with $\lceil \log_2 \beta \rceil$ trial products, or estimate $x$ from the top digits of $r$ divided by $2q$ and correct it, as in long division. In base 2, line L4 is the single test $4q + 1 \le r$: if it holds, $x = 1$ and line L5 subtracts $4q + 1$; otherwise $x = 0$.

## Example

The square root of $A = 152399025$ in base 10. The pairs are 1, 52, 39, 90, 25, so $n = 5$.

| step | pair | $r$ after L3 | digit $x$ | $(2 \cdot 10 q + x) \cdot x$ | $r$ after L5 | $q$ after L6 |
|---|---|---|---|---|---|---|
| 1 | 01 | 1 | 1 | $1 \cdot 1 = 1$ | 0 | 1 |
| 2 | 52 | 52 | 2 | $22 \cdot 2 = 44$ | 8 | 12 |
| 3 | 39 | 839 | 3 | $243 \cdot 3 = 729$ | 110 | 123 |
| 4 | 90 | 11090 | 4 | $2464 \cdot 4 = 9856$ | 1234 | 1234 |
| 5 | 25 | 123425 | 5 | $24685 \cdot 5 = 123425$ | 0 | 12345 |

So $\sqrt{152399025} = 12345$ exactly. In step 4 the digit 5 would need $2465 \cdot 5 = 12325 > 11090$, so $x = 4$.

**In base 2.** $A = 200 = 11\,00\,10\,00_2$, with the pairs 3, 0, 2, 0. The steps give $r = 3$, test $1 \le 3$, $x = 1$, $r = 2$, $q = 1$; then $r = 8$, test $5 \le 8$, $x = 1$, $r = 3$, $q = 3$; then $r = 14$, test $13 \le 14$, $x = 1$, $r = 1$, $q = 7$; then $r = 4$, test $29 \le 4$ fails, $x = 0$, $q = 14$. So $\lfloor \sqrt{200} \rfloor = 14$ with remainder $200 - 196 = 4$.

## Correctness

The invariant of the loop of line L2, after $j$ passes, is

$$q = \lfloor \sqrt{P_j} \rfloor, \qquad r = P_j - q^2, \qquad 0 \le r \le 2q .$$

The key fact is that the root of $P_{j+1} = P_j \beta^2 + g$, with $0 \le g < \beta^2$, lies between $q\beta$ and $q\beta + \beta - 1$, because $(q\beta)^2 \le P_{j+1} < ((q + 1)\beta)^2$. So the new root is $q\beta + x$ for one digit $x$, and the largest $x$ with $(q\beta + x)^2 \le P_{j+1}$ is the largest $x$ with $(2q\beta + x)\, x \le r\beta^2 + g$, which is line L4. The full proof is below.

## Complexity

- **Steps.** The loop of line L2 runs $n$ times, once per root digit.
- **One step.** At pass $j$, $q$ has $j$ digits and $r \le 2q$ has at most $j + 1$ digits. Line L3 is a shift by two digits and an addition, line L5 a product by one digit and a subtraction, and line L6 a shift: $\Theta(j)$ digit operations. Line L4 costs $\Theta(j)$ per trial; it uses $O(\log \beta)$ trials by binary search, one trial in base 2, and $O(1)$ trials with the estimate from the leading digits.
- **Total.** $\sum_{j=1}^{n} \Theta(j) = \Theta(n^2)$ digit operations for a fixed base, in every case. In base 2 this is $\Theta(N^2)$ bit operations for an $N$-bit input, the same as the [restoring division](/restoring-division/) of numbers of that size.
- **Space.** $q$ and $r$ have $O(n)$ digits.

## Properties

- **Exact.** It returns the exact floor of the root and the exact remainder, with no rounding and no floating point.
- **Most significant digit first.** The root digits come out from the top, and each one is final. So the method can stop after any number of digits, which gives a truncated root; appending pairs of zeros to $A$ gives digits after the point.
- **A remainder for free.** $R = A - Q^2$ tells at once whether $A$ is a perfect square ($R = 0$).
- **Like division.** The structure is the same as long division with a divisor $2q\beta + x$ that grows by one digit at each step, and the hardware forms (restoring and non-restoring) share the datapath of a divider.

## Variants and improvements

- **Restoring binary square root.** In base 2, compute $r - (4q + 1)$; if it is negative, restore $r$ and set the bit to 0. Hacker's Delight gives the version that keeps $4q$ shifted in a word, with one subtraction per bit.
- **Non-restoring square root.** Keep a possibly negative remainder and choose between adding and subtracting at each step, which saves the restore, as in [non-restoring division](/non-restoring-division/).
- **Higher radix and SRT square root.** Several bits per step with a redundant digit set, as in floating-point units that share the square root with the divider.
- **Karatsuba square root.** Brent and Zimmermann's SqrtRem computes the root of the top half recursively, then the next quarter of the digits by one division, which costs $O(M(n))$ for Karatsuba multiplication. The digit-by-digit method is its base case.
- **Newton's method.** [Newton's iteration](/newton-integer-root/) $x \leftarrow \lfloor (x + \lfloor A/x \rfloor)/2 \rfloor$ converges quadratically, and with a reciprocal square root iteration it costs $O(M(n))$.
- **Other roots.** For $k$th roots the growth term becomes $(q\beta + x)^k - (q\beta)^k$, and the digit search works the same way ([integer nth root](/integer-nth-root/)).

## When to use it

Use the digit-by-digit method for roots of a few words, in hardware without a fast multiplier, and when you need exact results digit by digit, such as a root to a fixed number of decimal places. In base 2 it is the simplest correct integer square root for a machine word: 32 iterations of a shift, a compare and a subtract for a 64-bit input. For numbers of hundreds of digits or more, the $O(M(n))$ methods win, and libraries switch to them above a threshold that is measured, not proved.

## Pitfalls

- **Pairs from the wrong end.** Line L3 brings down the digits in pairs that are aligned with the units digit. For an odd number of digits, pad with a leading zero, not a trailing one: $152399025$ starts with the pair 01, not 15.
- **The wrong trial term.** Line L4 tests $(2q\beta + x) \cdot x$, not $(q\beta + x)^2$ against $r$, because $r$ is already $P - q^2\beta^2$. Testing $(q\beta + x)^2 \le r$ gives digits that are too large.
- **Forgetting that $r$ grows.** After line L5, $r$ can be as large as $2q$, which has one digit more than $q$. A fixed-width register for $r$ of the same width as $q$ overflows; in base 2 for a $2m$-bit input, $r$ needs $m + 1$ bits.
- **Floating point instead.** `int(math.sqrt(A))` in double precision is wrong for large $A$; for example for $A = (2^{27} + 1)^2 - 1 = 2^{54} + 2^{28}$, the float rounds up and the result is $2^{27} + 1$, one too large. The integer method avoids this.

## Implementations

## History

Square roots by a digit-by-digit procedure are among the oldest algorithms. The Chinese Nine Chapters on the Mathematical Art give a procedure for extracting square roots digit by digit, and Indian mathematicians, such as Aryabhata around 500, described the decimal method. It was a standard part of school arithmetic for centuries. The binary restoring and non-restoring forms were developed for the arithmetic units of electronic computers, and the radix-2 method is still the base of software integer square roots for one word.

## References
