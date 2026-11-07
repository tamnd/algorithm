---
tag: NK7PPZ
kind: problem
slug: integer-exponentiation
name: Integer exponentiation
aliases:
- computing x^n
- powering
area: algebra/integer-arithmetic
level: intro
summary: Compute x^n for integers x and exponents n using few multiplications.
model: multitape-turing-machine
complexity:
  vars: {N: the number of binary digits of x, e: the exponent, M: the cost of multiplying two numbers of the given length}
  time: {worst: O(M(e N))}
prereqs: [integer-multiplication, positional-number-system]
see_also: [binary-exponentiation, sliding-window-exponentiation, addition-chain, addition-chain-problem, modular-exponentiation, matrix-exponentiation, integer-nth-root, fibonacci-numbers]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (the binary methods, the m-ary method, addition chains, the bounds on l(n), and the cost of powering when the numbers grow)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.3, Multiplication (the cost of products of unequal sizes, 1.3.5, and of squaring, 1.3.6)
  - paper: doi:10.1090/S0002-9904-1939-07068-7
    title: Alfred Brauer, On addition chains, Bulletin of the American Mathematical Society 45(10), 1939
    locator: pp. 736 to 739 (the 2^k-ary method and the upper bound log2 n + (1 + o(1)) log2 n / log2 log2 n)
  - paper: doi:10.1016/0304-3975(75)90008-0
    title: Arnold Schönhage, A lower bound for the length of addition chains, Theoretical Computer Science 1(1), 1975
    locator: pp. 1 to 12 (l(n) >= log2 n + log2 v(n) - 2.13)
---

Integer exponentiation is the problem of computing $x^e$ for an integer $x$ and a nonnegative integer exponent $e$. The result has about $e$ times as many digits as $x$, so the problem is less about the number of multiplications than about their sizes. The [binary method](/binary-exponentiation/) uses about $\log_2 e$ multiplications instead of $e - 1$. In bit operations, the whole computation costs $O(M(eN))$ for $x$ of $N$ binary digits, where $M$ is the cost of a [multiplication](/integer-multiplication/): about the cost of one product of the size of the answer. With schoolbook products the binary method saves only a constant factor over repeated multiplication, as Knuth discusses in Section 4.6.3.

## In plain words

To get 3 to the power 10, you could multiply 3 by itself nine times. A faster way squares: 3 times 3 is 9, 9 times 9 is 81, one more 3 gives 243, and 243 squared is 59049. That took four multiplications instead of nine. In general the number of steps grows with the number of digits of the exponent, not with the exponent itself.

But the numbers get long fast. Each squaring doubles the length, and the last step works on numbers half as long as the answer. That last step alone costs about as much as all the steps before it together. So the real work is a few big multiplications, and a fast way to multiply large numbers is what makes powering fast.

## Definition

**Input.** An integer $x$ with $N$ binary digits ($N = \lfloor \log_2 |x| \rfloor + 1$ for $x \ne 0$), and an integer $e \ge 0$.

**Output.** The integer $x^e$, with $x^0 = 1$ (also for $x = 0$, by convention).

**Size of the output.** For $|x| \ge 2$, $x^e$ has $\lfloor e \log_2 |x| \rfloor + 1$ binary digits, between $e(N - 1) + 1$ and $eN$. So the output is about $e$ times longer than $x$, and any algorithm writes $\Theta(eN)$ digits.

**Two cost measures.** The *multiplication count* is the number of products in a computation that starts from $x$ and only multiplies earlier results; its minimum is the length $l(e)$ of a shortest [addition chain](/addition-chain/) for $e$, since the exponents of the results form such a chain. The *bit cost* counts the operations on digits, so a product of an $a$-digit and a $b$-digit number costs about $ab$ with schoolbook multiplication and $M(\max(a, b))$ in general.

## Variants

- **Modular exponentiation.** Compute $x^e \bmod m$. The results stay below $m$, so each product has the same size and the multiplication count is the cost measure that matters ([modular exponentiation](/modular-exponentiation/)).
- **Powers in other structures.** The same methods compute $A^e$ for a matrix ([matrix exponentiation](/matrix-exponentiation/)), $e P$ for a point of an elliptic curve, and powers of polynomials. Only associativity is needed.
- **Fixed exponent.** For one $e$ used many times, such as $x^{65537}$ in RSA, a precomputed shortest addition chain saves multiplications ([addition chain problem](/addition-chain-problem/)).
- **Several powers.** Compute $x^{e_1}, \ldots, x^{e_k}$ together (an *addition sequence*), or a product $x_1^{e_1} \cdots x_k^{e_k}$ (a vectorial chain).
- **Inverse problems.** Given $y$ and $e$, find $\lfloor y^{1/e} \rfloor$ ([integer $n$th root](/integer-nth-root/)); given $y$, decide whether $y$ is a perfect power. Given $x$, $y$ and a modulus, find $e$: the discrete logarithm, believed hard.

## Examples

**$3^{10}$ by the left-to-right binary method.** $10 = 1010_2$. Start with $3$. Bit 0: square, $9$. Bit 1: square, $81$, and multiply by 3, $243$. Bit 0: square, $59049$. That is 4 multiplications, $\lfloor \log_2 10 \rfloor + \nu(10) - 1 = 3 + 2 - 1$, where $\nu$ is the number of 1s in binary. The exponents $1, 2, 4, 5, 10$ form an addition chain of length 4, and 4 is optimal for 10.

**$x^{15}$.** The binary method uses 6 multiplications ($x^2, x^3, x^6, x^7, x^{14}, x^{15}$), but 5 suffice: $x^2, x^4, x^5, x^{10}, x^{15}$, with $x^{15} = x^{10} x^5$. So the binary method is not always optimal.

**Multiplication counts of the binary method.** It uses $\lfloor \log_2 e \rfloor + \nu(e) - 1$ products: 6 for $e = 64$ (squarings only), 8 for $e = 100$, 14 for $e = 1000$, and 38 for $e = 2^{20} - 1$.

**The size of the answer.** $3^{100000}$ has 158497 binary digits and 47713 decimal digits. CPython refuses by default to convert integers of more than 4300 decimal digits to a string, because its conversion takes quadratic time; the power itself is computed in a fraction of a second.

**Bit cost with schoolbook products.** Let $x$ have $N = 64$ binary digits and $e = 1000$, and charge $ab$ for a product of an $a$-digit and a $b$-digit number. Repeated multiplication costs $\sum_{k=1}^{e-1} kN \cdot N \approx \frac12 (eN)^2$, computed exactly as $0.4995 (eN)^2$. The left-to-right binary method costs $0.3334 (eN)^2$: the squarings have sizes $eN/2, eN/4, \ldots$, which sum to $\frac{1}{4} + \frac{1}{16} + \cdots = \frac13$ of $(eN)^2$. The factor between the two is only $1.5$, although the multiplication counts are 999 and 14.

## Known algorithms

| algorithm | multiplications | bit cost with schoolbook / fast products |
|---|---|---|
| repeated multiplication | $e - 1$ | $\Theta((eN)^2)$ / $\Omega(e^2 N)$, from $e - 1$ unbalanced products |
| [binary exponentiation](/binary-exponentiation/), left-to-right or right-to-left | $\lfloor \log_2 e \rfloor + \nu(e) - 1$ | $\Theta((eN)^2)$ / $O(M(eN))$ |
| $2^k$-ary and [sliding-window exponentiation](/sliding-window-exponentiation/) | $\log_2 e + (1 + o(1)) \frac{\log_2 e}{\log_2 \log_2 e}$ | as above, the extra savings are in the count |
| shortest [addition chain](/addition-chain/) | $l(e)$, optimal | as above |
| $x = 2^k$: shift | 0 | $O(ek)$ to write the result |

For the fast-product column: the squarings in the binary method have sizes $eN/2^j$, and $\sum_j M(eN/2^j) \le 2M(eN)$ when $M(n)/n$ does not decrease, so the total is $O(M(eN))$. Repeated multiplication instead does $e - 1$ products of a long number by an $N$-digit one, each of which costs at least linear time in the long number, so it needs $\Omega(e^2 N)$ bit operations, much more than $M(eN) = O(eN \log(eN))$.

## Bounds

**Multiplication count, lower bound.** Each product at most doubles the largest exponent reached, so $k$ products reach at most $x^{2^k}$, and at least $\lceil \log_2 e \rceil$ products are needed. Schönhage (1975) proved the sharper $l(e) \ge \log_2 e + \log_2 \nu(e) - 2.13$.

**Multiplication count, upper bound.** Brauer (1939) proved $l(e) \le \log_2 e + (1 + o(1)) \frac{\log_2 e}{\log_2 \log_2 e}$ by the $2^k$-ary method, and Erdős (1960) proved that this is tight for almost all $e$. So the optimal count is $\log_2 e$ plus a lower-order term.

**Bit cost.** The output has $\Theta(eN)$ digits, which gives a lower bound $\Omega(eN)$. Squaring is the case $e = 2$, and squaring is as hard as multiplication up to a constant, since $ab = \frac{(a+b)^2 - (a-b)^2}{4}$. The upper bound $O(M(eN))$ of the binary method is within a constant factor of one multiplication of numbers of the size of the result, and with the bound $M(n) = O(n \log n)$ of [integer multiplication](/integer-multiplication/) this is $O(eN \log(eN))$.

## Reductions

- **From multiplication.** Squaring is powering with $e = 2$, and a product is two squarings and a few additions, so powering is at least as hard as multiplication of numbers of the size of the result.
- **To multiplication.** The binary method computes $x^e$ with cost $O(M(eN))$, so the two problems have the same cost up to a constant, measured in the size of the output.
- **Fibonacci numbers and linear recurrences.** $F_n$ is an entry of the matrix power $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n$, so [Fibonacci numbers](/fibonacci-numbers/) reduce to powering in a ring of matrices.
- **Shortest chains.** Minimizing the multiplication count is the [addition chain problem](/addition-chain-problem/).

## Applications

- Modular exponentiation in RSA, Diffie-Hellman key exchange and primality tests.
- The powers $10^k$ and $\beta^k$ used by divide-and-conquer [radix conversion](/radix-conversion/).
- Exact combinatorics and number theory, for example in the evaluation of binomial coefficients from prime factorizations, $\binom{n}{k} = \prod p^{e_p}$.
- Computing large terms of linear recurrences through matrix powers.

## References
