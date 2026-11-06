---
tag: D262EM
kind: algorithm
slug: binary-exponentiation
name: Binary exponentiation
aliases:
- exponentiation by squaring
- fast exponentiation
- repeated squaring
- square-and-multiply
area: number-theory/modular-arithmetic
level: intro
summary: Computes x^n in O(log n) multiplications by squaring and multiplying by x per bit of n.
solves: [modular-exponentiation, integer-exponentiation]
model: word-ram
complexity:
  vars: {e: the exponent, k: the number of binary digits of the exponent, n: the number of binary digits of the modulus}
  time: {worst: Θ(log e), best: Θ(log e)}
  space: {extra: Θ(1)}
  multiplications: {worst: Θ(log e)}
  bit_operations: {worst: O(k n^2)}
properties: {deterministic: true, recursive: false}
history:
  note: Knuth traces the left-to-right binary method to Pingala's Chandah-sutra, an Indian work on prosody, and a right-to-left method to al-Kashi in 1427.
prereqs: [congruence, modular-multiplication, loop-invariant]
see_also: [sliding-window-exponentiation, addition-chain, matrix-exponentiation, montgomery-multiplication, barrett-reduction, fermat-little-theorem, miller-rabin, rsa-cryptosystem]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (Algorithm A, the right-to-left binary method; the left-to-right method; the count of multiplications; addition chains and the lower bound; history)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 31.6, Powers of an element (the procedure MODULAR-EXPONENTIATION by repeated squaring and its bit cost)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 2.4.4, Algorithm 2.143 (repeated square-and-multiply in Z_n), and Section 14.6.1, Algorithms 14.76 and 14.79 (right-to-left and left-to-right binary exponentiation) and Note 14.87 (comparison of the methods)
  - book: isbn:9780521516440
    title: Victor Shoup, A Computational Introduction to Number Theory and Algebra, second edition
    locator: Section 3.4, Computing in Z_n (the repeated-squaring algorithm and its cost)
---

Binary exponentiation computes a power $x^e$ with about $2 \lg e$ multiplications instead of the $e - 1$ of the naive loop: it reads the exponent in binary, squares once for each binary digit and multiplies once for each digit $1$. It solves [modular exponentiation](/modular-exponentiation/) $x^e \bmod m$ in $\Theta(\log e)$ time on the [word RAM](/word-ram/) when the modulus fits in a word, and in $O(k n^2)$ bit operations for a $k$-digit exponent and an $n$-digit modulus. It works in each monoid, so the same loop computes powers of matrices, of polynomials and of permutations. It is a building block of [Fermat's](/fermat-primality-test/) and the [Miller-Rabin](/miller-rabin/) primality tests, of [RSA](/rsa-cryptosystem/) and of [Diffie-Hellman](/diffie-hellman/) key exchange.

## In plain words

To raise a number to a large power, the naive way multiplies by the number again and again, once for each unit of the power. This is far too slow for a power with hundreds of digits.

Squaring is the key. Square the number, and you get its second power. Square that, and you get the fourth power, then the eighth, and so on. A few squarings reach very high powers.

Any power is a sum of such doubling powers: thirteen is eight plus four plus one. So write the power in binary. Walk through its digits from the lowest one. At each step, square the running square. When the digit is one, also multiply the result by the running square. The work grows with the number of digits of the power, not with the power itself. With remainders, the numbers also stay small.

## The problem

**Input.** An integer $x$, an integer exponent $e \ge 0$, and a modulus $m \ge 1$.

**Output.** $x^e \bmod m$, the integer $r$ with $0 \le r < m$ and $r \equiv x^e \pmod m$. The convention $x^0 = 1$ holds for each $x$, including $x = 0$, so the output for $e = 0$ is $1 \bmod m$, which is $0$ when $m = 1$.

This is [modular exponentiation](/modular-exponentiation/). Without the modulus, the same loop computes the exact power, which is [integer exponentiation](/integer-exponentiation/).

**Representation and range.** Residues are represented by their least non-negative representatives, integers in $0$ to $m - 1$. The modulus can be any $m \ge 1$: prime, composite, even or a power of two. The base need not be coprime to $m$.

**Cost model.** Two models are used. On the [word RAM](/word-ram/) with words of $w$ binary digits, the modulus satisfies $m < 2^w$, and a modular product $ab \bmod m$ of two residues costs $O(1)$ (a double-word product and a division, as on 64-bit hardware). The cost is then the number of loop passes. For [arbitrary-precision](/arbitrary-precision-arithmetic/) integers, the modulus has $n$ binary digits, the exponent has $k$ binary digits, and the cost is counted in bit operations. Without a modulus the numbers grow, and the bound becomes the cost of the last squaring.

## The algorithm

```pseudo id=main
BINARY-EXP(x, e, m)                        ▷ e ≥ 0, m ≥ 1; returns x^e mod m
L1  r ← 1 mod m                            ▷ 0 when m = 1
L2  b ← x mod m
L3  while e > 0 do
L4      if e is odd then r ← r · b mod m
L5      e ← ⌊e / 2⌋
L6      if e > 0 then b ← b · b mod m
L7  return r
```

The variable $b$ runs through $x, x^2, x^4, x^8, \ldots$ modulo $m$: line L6 squares it once for each binary digit of the exponent. The variable $r$ collects the product of the squares that belong to digits $1$: line L4 multiplies them in when the lowest digit of $e$ is $1$. Line L5 drops this digit. Line L6 skips the squaring after the last digit, which would be wasted.

This order reads the exponent from its lowest digit, so it is the *right-to-left* binary method. The *left-to-right* method reads it from the highest digit:

```pseudo id=left-to-right
BINARY-EXP-LR(x, e, m)                     ▷ e = (d_{k−1} … d_1 d_0) in binary, d_{k−1} = 1
L1  r ← 1 mod m
L2  for i ← k − 1 downto 0 do
L3      r ← r · r mod m
L4      if d_i = 1 then r ← r · x mod m
L5  return r
```

Its invariant is $r \equiv x^{\lfloor e / 2^i \rfloor}$ after the pass for digit $i$: squaring appends a digit $0$ to the exponent read so far, and the multiplication by $x$ turns it into $1$. It multiplies always by the fixed base $x$, which is useful when $x$ is small or has a fast multiplication, and it is the base of the [sliding-window](/sliding-window-exponentiation/) methods.

## Example

Compute $3^{200} \bmod 1009$. In binary, $200 = 11001000_2 = 128 + 64 + 8$, so the loop runs 8 times. The table shows the state after each pass.

| pass | digit $e \bmod 2$ | $r$ after L4 | $e$ after L5 | $b$ after L6 |
|---|---|---|---|---|
| start | | 1 | 200 | 3 |
| 1 | 0 | 1 | 100 | 9 |
| 2 | 0 | 1 | 50 | 81 |
| 3 | 0 | 1 | 25 | 507 |
| 4 | 1 | 507 | 12 | 763 |
| 5 | 0 | 507 | 6 | 985 |
| 6 | 0 | 507 | 3 | 576 |
| 7 | 1 | 431 | 1 | 824 |
| 8 | 1 | 985 | 0 | 824 |

So $3^{200} \equiv 985 \pmod{1009}$. In pass 3, $b = 81^2 = 6561 = 6 \cdot 1009 + 507$, so $b \equiv 3^8$. The result is $3^8 \cdot 3^{64} \cdot 3^{128} \bmod 1009$. The run uses 7 squarings and 3 multiplications into $r$, 10 multiplications in total, against 199 for the naive loop.

## Correctness

The loop keeps the [loop invariant](/loop-invariant/)

$$r \cdot b^{e} \equiv x_0^{e_0} \pmod m, \qquad 0 \le r, b < m,$$

where $x_0$ and $e_0$ are the inputs. Lines L1 and L2 make it true, since $r \equiv 1$ and $b \equiv x_0$. If $e$ is even, $b^e = (b^2)^{e/2}$. If $e$ is odd, $b^e = b \cdot (b^2)^{(e-1)/2}$, and line L4 moves the factor $b$ into $r$. In both cases the new $e$ is $\lfloor e/2 \rfloor$ and the new $b$ is $b^2$, so the invariant holds after the pass. Each reduction modulo $m$ keeps the [congruence](/congruence/) because congruences respect products. The value $e$ at least halves in each pass, so the loop stops; at exit $e = 0$ and $r \equiv x_0^{e_0}$, with $0 \le r < m$. The full proof, including the skipped squaring of line L6 and the case $m = 1$, is in the proofs.

## Complexity

**Loop passes.** For $e \ge 1$, the loop runs $\lfloor \lg e \rfloor + 1$ times, once for each binary digit of $e$, because line L5 removes one digit in each pass. For $e = 0$ it does not run.

**Multiplications.** Let $\nu(e)$ be the number of digits $1$ in the binary form of $e$. Line L6 runs in each pass except the last, so it makes $\lfloor \lg e \rfloor$ squarings. Line L4 makes $\nu(e)$ multiplications, and the first one multiplies by $r = 1$, so a program can replace it by a copy. The total is

$$\lfloor \lg e \rfloor + \nu(e) \le 2 \lfloor \lg e \rfloor + 1,$$

with equality when $e = 2^j - 1$. The smallest count, $\lfloor \lg e \rfloor + 1$, occurs when $e$ is a power of two. So the number of multiplications is $\Theta(\log e)$ in both the worst and the best case. Left-to-right with the first squaring of $1$ skipped makes $\lfloor \lg e \rfloor$ squarings and $\nu(e) - 1$ real multiplications.

**A lower bound.** Each method that forms $x^e$ from $x$ with multiplications of already computed powers is an [addition chain](/addition-chain/) for $e$: the exponents start at $1$, and each new one is the sum of two earlier ones. A sum of two numbers at most $s$ is at most $2s$, so after $j$ multiplications all exponents are at most $2^j$. Hence $x^e$ needs at least $\lceil \lg e \rceil$ multiplications. Binary exponentiation is within a factor of $2$ of this bound. Knuth (Section 4.6.3) shows that the shortest chain for $e$ has length $\lg e + O(\lg e / \lg \lg e)$, so the factor $2$ can be brought close to $1$, but no fast method is known that finds a shortest chain.

**Time on the word RAM.** With $m < 2^w$, each pass costs $O(1)$, so the time is $\Theta(\log e)$ in each case. The extra space is $\Theta(1)$ words.

**Bit operations.** If $m$ has $n$ binary digits, each product of two residues and its reduction cost $O(n^2)$ bit operations with schoolbook multiplication and division. With at most $2k$ products, the total is $O(k n^2)$ bit operations; with a multiplication of cost $M(n)$ and division by [Newton's method](/newton-raphson-method/), it is $O(k M(n))$. When $e < m$, which is the usual case in cryptography, this is $O(n^3)$ for schoolbook arithmetic. The extra space is $O(n)$ bits.

**Exact powers.** Without a modulus, $x^e$ has about $e$ times as many digits as $x$, so the cost of the method is dominated by the last squaring or multiplication. If $x$ has $n$ binary digits, the operands at the step for digit $i$ have $O(n e / 2^i)$ digits, and with schoolbook multiplication the costs form a geometric series with a total of $O((n e)^2)$ bit operations. The naive loop costs $\Theta(n^2 e^2)$ as well, so for exact powers the gain comes only with a fast multiplication.

| measure | bound |
|---|---|
| loop passes for $e \ge 1$ | $\lfloor \lg e \rfloor + 1$ |
| multiplications | $\lfloor \lg e \rfloor + \nu(e) \le 2 \lfloor \lg e \rfloor + 1$ |
| lower bound for any chain of products | $\lceil \lg e \rceil$ |
| time on the word RAM, $m < 2^w$ | $\Theta(\log e)$ worst and best |
| bit operations, $n$-digit modulus, $k$-digit exponent | $O(k n^2)$ schoolbook, $O(k M(n))$ in general |
| extra space | $\Theta(1)$ words |

## Properties

- **Generic.** The loop uses only an associative product and its identity, so it works in each monoid: residues, matrices ([matrix exponentiation](/matrix-exponentiation/) and [Fibonacci numbers](/fibonacci-numbers/)), polynomials modulo a polynomial, permutations ([permutation power](/permutation-power/)), and points of an elliptic curve, where the product is a point addition and the method is called double-and-add.
- **Deterministic and iterative.** No random choices and no recursion. A recursive form $x^e = (x^{\lfloor e/2 \rfloor})^2 \cdot x^{e \bmod 2}$ has depth $\lfloor \lg e \rfloor + 1$, which is small, but the loop needs no stack.
- **Not constant time.** The sequence of operations depends on the digits of $e$. This leaks a secret exponent through timing or power traces.

## Variants and improvements

- **Left-to-right binary method.** The block `left-to-right` above. Same count, and it multiplies by the fixed base $x$.
- **$2^t$-ary and [sliding-window exponentiation](/sliding-window-exponentiation/).** Precompute $x^j$ for small odd $j$ and process $t$ digits of $e$ at a time. This lowers the number of multiplications to about $\lg e + \lg e/(t + 1)$ plus the table of $2^{t-1}$ entries, against about $1.5 \lg e$ for the binary method on a random exponent. For an exponent of 2048 binary digits and $t = 6$, this is about 2370 multiplications against about 3070.
- **[Addition chains](/addition-chain/).** A short chain for a fixed exponent saves multiplications when the same exponent is used many times. For $e = 15$, the binary method uses 6 multiplications, and the chain $1, 2, 3, 6, 12, 15$ uses 5.
- **Montgomery ladder.** Keep the pair $(x^j, x^{j+1})$ and make one squaring and one multiplication for each digit, whatever its value. The uniform sequence of operations resists timing attacks.
- **Fast reduction.** In a long exponentiation with one modulus, replace the division in each product by [Montgomery multiplication](/montgomery-multiplication/) or [Barrett reduction](/barrett-reduction/).
- **Reduce the exponent.** If $\gcd(x, m) = 1$, then $x^e \equiv x^{e \bmod \varphi(m)} \pmod m$ by [Euler's theorem](/euler-theorem/), and for a prime $m$, $x^e \equiv x^{e \bmod (m-1)}$ by [Fermat's little theorem](/fermat-little-theorem/). For RSA with a known factorization, the [Chinese remainder theorem](/chinese-remainder-theorem/) splits one exponentiation into two of half the size.
- **Several bases.** Shamir's trick computes $x^a y^b$ with one shared sequence of squarings, which is used to verify signatures.

## When to use it

Use binary exponentiation for each power with a large exponent: it is short, needs no table and is within a factor of 2 of the optimum. For exponents of hundreds or thousands of digits, as in RSA, a sliding window saves about a fifth of the multiplications. For a secret exponent, use a constant-time ladder instead. For a small fixed exponent such as $e = 3$ or $e = 65537$, the binary method is already optimal or close to it. For powers in an exact (non-modular) setting, the cost is the size of the result, and a fast multiplication matters more than the order of the products.

## Pitfalls

- **Overflow of the product.** With a 64-bit modulus, `b * b % m` overflows a 64-bit integer when $m > 2^{32}$. Use a 128-bit product, or a [modular multiplication](/modular-multiplication/) routine, in lines L4 and L6.
- **The result for $m = 1$.** Starting with `r = 1` instead of `r = 1 % m` (line L1) returns $1$ for $e = 0$ and $m = 1$, but the residue modulo $1$ is $0$. The test with $m = 1$ catches it.
- **Negative bases.** In C, Java and Go, `x % m` is negative for a negative $x$, and line L2 then gives a wrong representative. Write `b = ((x % m) + m) % m`.
- **A signed exponent.** A loop on a signed $e$ with an arithmetic shift does not end for a negative $e$. Reject $e < 0$, or compute the [modular inverse](/modular-inverse/) of $x^{-e}$.
- **Floating-point powers.** `pow(x, e)` in floating point loses digits long before the reduction modulo $m$. Never reduce the result of a float power.
- **Reducing the exponent without the hypothesis.** $x^e \equiv x^{e \bmod \varphi(m)}$ needs $\gcd(x, m) = 1$. For $x = 2$, $m = 8$ and $e = 4$, it gives $2^0 = 1$, but $2^4 \bmod 8 = 0$.

## Implementations

The Python version follows the main block. It accepts any integer $x$ and arbitrary-precision $e$ and $m$, and it never calls the built-in three-argument `pow`, which the tests use as the reference.

## History

The method is old. Knuth (Section 4.6.3) traces the left-to-right binary method to Pingala's Chandah-sutra, an Indian work on prosody that computes powers of 2 by squaring and doubling, and he reports a right-to-left method in a work of al-Kashi from 1427. Knuth's section also gives the history of addition chains, which began with the question of the shortest way to compute a power. In modern computing the method became central with public-key cryptography, where each RSA operation is one modular exponentiation with a large exponent.

## References
