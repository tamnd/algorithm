---
tag: 0Z565M
kind: problem
slug: radix-conversion
name: Radix conversion
aliases:
- base conversion
- binary to decimal conversion
- decimal to binary conversion
- number base conversion
area: algebra/integer-arithmetic
level: core
summary: Convert the digit representation of an integer from one radix to another.
model: word-ram
complexity:
  vars: {n: the number of limbs of N, M: the cost M(k) of multiplying two integers of k limbs}
  time: {worst: O(M(n) log n)}
prereqs: [positional-number-system, division-with-remainder, horner-rule]
see_also: [scaled-remainder-tree, radix, multiprecision-integer, long-division, subproduct-tree, floating-point-to-decimal, decimal-to-floating-point, polynomial-evaluation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.4, Radix conversion (Methods 1a, 1b, 2a and 2b, conversion of fractions, and fast conversion of large numbers in the exercises)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.7, Base conversion (1.7.1, Quadratic algorithms, and 1.7.2, Subquadratic algorithms)
  - url: https://docs.python.org/3/library/stdtypes.html#int-max-str-digits
    title: Python documentation, Built-in Types, Integer string conversion length limitation
    locator: the default limit of 4300 decimal digits and the reason for it
---

Radix conversion is the problem of rewriting the digits of an integer $N$ given in one radix $\alpha$ as the digits of $N$ in another radix $\beta$. Its everyday case is between binary and decimal: a program reads decimal input into binary words, and prints binary words as decimal text. For numbers of one or two words it is a few machine divisions. For an $n$-limb [multiprecision integer](/multiprecision-integer/) the school methods, repeated division by the new radix or Horner's rule in the new radix, take $\Theta(n^2)$ limb operations, while a divide-and-conquer method with precomputed powers of the radix takes $O(M(n) \log n)$, where $M(n)$ is the cost of an $n$-limb product. When one radix is a power of the other, as with binary and hexadecimal, conversion is a regrouping of digits in linear time.

## In plain words

The number eight hundred fourteen thousand five hundred seven is written 814507 in decimal and C6DAB in hexadecimal. It is the same number; only the way of writing it differs. Radix conversion turns one way of writing into the other.

To get the hexadecimal digits, divide by 16 again and again: the remainders 11, 10, 13, 6, 12 are the digits B, A, D, 6, C, from the right. To go back, read the hexadecimal digits from the left and keep a running value, multiplying by 16 and adding each new digit. For numbers with millions of digits both ways are slow, and faster methods split the number in halves.

## Definition

**Input.** Radices $\alpha, \beta \ge 2$ and the digits $u_0, \ldots, u_{m-1}$, $0 \le u_i < \alpha$, of an integer $N = \sum_{i} u_i \alpha^i \ge 0$.

**Output.** The digits $v_0, \ldots, v_{m'-1}$, $0 \le v_j < \beta$, with $N = \sum_j v_j \beta^j$ and $v_{m'-1} \ne 0$ (or the single digit 0 if $N = 0$). By the uniqueness of [positional representation](/positional-number-system/) the output is determined by $N$, and $m' = \lfloor \log_\beta N \rfloor + 1$ for $N \ge 1$.

**The two directions.** The arithmetic is done in some working radix, usually the machine radix $2^w$. *Output conversion* turns the machine representation into digits of another radix, for printing; *input conversion* turns digits of another radix into the machine representation, for reading. On a computer with base $\beta = 2^w$ limbs, an $n$-limb number has about $n w \log_{10} 2$ decimal digits.

**Cost model.** Word RAM with $w$-bit words; costs in limb operations, with $M(n)$ the cost of an $n$-limb product. The bounds below are proved; the sizes at which one method beats another are observed.

## Variants

- **Integers and fractions.** For a fraction $0 \le x < 1$ the roles change: the digits in radix $\beta$ come from repeated multiplication by $\beta$, taking the integer parts. A fraction with finitely many digits in one radix may have infinitely many in another: $0.1$ in decimal is $0.000110011\ldots$ in binary, repeating $0011$.
- **Floating-point numbers.** Converting a binary float to the shortest decimal string that reads back to the same float, or a decimal string to the nearest float, needs care with rounding; see [floating-point to decimal](/floating-point-to-decimal/) and [decimal to floating-point](/decimal-to-floating-point/).
- **Power-related radices.** If $\alpha = \gamma^a$ and $\beta = \gamma^b$, convert by regrouping: each radix $\alpha$ digit is $a$ digits in radix $\gamma$, and groups of $b$ of these form the radix $\beta$ digits. Binary, octal and hexadecimal convert this way in $O(m)$ time.
- **Mixed radix.** The output digits have different radices, as in hours, minutes and seconds, or the [factorial number system](/factorial-number-system/); repeated division works with each divisor in turn.
- **Fixed length.** Print exactly $k$ digits with leading zeros, as when a limb of $\lfloor 64 \log_{10} 2 \rfloor = 19$ decimal digits is printed inside a longer number.

## Examples

All values were checked by script.

- **Output by division.** $814507 = 16 \cdot 50906 + 11$, $50906 = 16 \cdot 3181 + 10$, and so on: the remainders are $11, 10, 13, 6, 12$, so $814507 = \texttt{C6DAB}_{16}$.
- **Input by Horner's rule.** Reading the decimal digits $8, 1, 4, 5, 0, 7$ into a hexadecimal accumulator with $x \leftarrow 10x + u$ gives $\texttt{8}, \texttt{51}, \texttt{32E}, \texttt{1FD1}, \texttt{13E2A}, \texttt{C6DAB}$.
- **Divide and conquer.** $814507 = 814 \cdot 10^3 + 507$, so the decimal digits of $814507$ are those of $814$ followed by those of $507$ padded to three places. In the general method the split is by $10^{2^i}$ with precomputed powers.
- **Regrouping.** $\texttt{C6DAB}_{16} = 1100\,0110\,1101\,1010\,1011_2$, one group of four binary digits per hexadecimal digit, and $3066653_8$ by groups of three.
- **A non-terminating fraction.** The first twelve binary digits of $0.1$ are $000110011001$.

## Known algorithms

| method | direction | cost in limb operations | notes |
|---|---|---|---|
| Repeated division by $\beta$ | output | $\Theta(n^2)$ | Knuth's Method 1a; a [short division](/long-division/) by one word per digit |
| Division by $\beta^k$ per word | output | $\Theta(n^2)$ | divide by the largest power $\beta^k$ that fits in a word, then split each remainder into $k$ digits; fewer long divisions |
| Horner's rule in radix $\beta$ | input | $\Theta(n^2)$ | Knuth's Method 1b, $x \leftarrow \alpha x + u_i$; see [Horner's rule](/horner-rule/) |
| Repeated multiplication of a fraction | output | $\Theta(n^2)$ | Knuth's Method 2a, the integer part of $\beta x$ is the next digit |
| Divide and conquer with powers $\beta^{2^i}$ | both | $O(M(n) \log n)$ | split $N = q\beta^{k} + r$ with $k$ a power of two near half the length, recurse on $q$ and $r$ |
| [Scaled remainder tree](/scaled-remainder-tree/) | output | $O(M(n) \log n)$ | replaces the divisions by multiplications of fixed-point fractions |
| Regrouping | both | $\Theta(n)$ | only when $\alpha$ and $\beta$ are powers of a common radix |

The divide-and-conquer output method precomputes $\beta^{k}, \beta^{2k}, \beta^{4k}, \ldots$ up to about half the length of $N$, divides $N$ by the largest of them with a fast division, and converts the quotient and the remainder recursively, padding the remainder with leading zeros. The input method is the same tree read upward: convert the two halves of the digit string, then combine them as $q\beta^{k} + r$ with one multiplication.

## Bounds

- **Upper bound.** $O(M(n) \log n)$ in both directions. The recursion has $O(\log n)$ levels; level $i$ performs $2^i$ divisions or multiplications of size $n/2^i$, costing $O(M(n))$ in total since $M$ grows at least linearly, and the powers cost $O(M(n))$ in total because their sizes double. With $M(n) = O(n \log n)$ in the bit complexity model (Harvey and van der Hoeven, 2019, published 2021), conversion of an $N_b$-digit binary number to decimal takes $O(N_b \log^2 N_b)$ bit operations.
- **Lower bound.** $\Omega(n)$, to read the input and write the output. For radices that are not powers of a common radix, no algorithm with cost $O(M(n))$ is known; the $\log n$ factor is the gap.
- **Regrouping is optimal.** For power-related radices the $\Theta(n)$ bound is tight.

## Reductions

- **To division with remainder**, for output: $N = q\beta + v_0$, and the digits of $q$ are the remaining ones. See [division with remainder](/division-with-remainder/).
- **To polynomial evaluation**, for input: $N = u(\alpha)$ for the polynomial $u(x) = \sum_i u_i x^i$, evaluated in radix $\beta$ arithmetic. Horner's rule and the divide-and-conquer method are the two ways of [evaluating a polynomial](/polynomial-evaluation/) at one point.
- **To a remainder tree**, for output: the digits in radix $\beta$ are remainders of $N$ by the powers $\beta^{k}$ arranged as a tree, the integer analogue of the [subproduct tree](/subproduct-tree/) used for multipoint evaluation of polynomials.
- **Between two bases of the same family**, to regrouping, as above.

## Applications

- **Input and output of numbers.** Every printed integer passes through output conversion, and every parsed one through input conversion; for one-word numbers compilers replace the division by 10 by a multiplication with a precomputed reciprocal.
- **Large computations.** Programs that compute $\pi$ or $e$ to billions of decimal digits work in binary and convert at the end; the subquadratic methods make the conversion a small part of the total time.
- **Security.** Quadratic conversion of very long strings is a denial of service risk: since Python 3.11, and in security releases of older versions, conversion between `int` and decimal `str` is limited by default to 4300 digits, for this reason.
- **Number formats.** Hexadecimal and octal dumps and base 64 encodings use regrouping, and decimal arithmetic in finance uses radix $10^k$ limbs to avoid conversion.

## References
