---
tag: YXZZ39
kind: algorithm
slug: sliding-window-exponentiation
name: Sliding-window exponentiation
aliases:
- windowed exponentiation
- k-ary exponentiation
- sliding window method
- left-to-right sliding window
area: algebra/integer-arithmetic
level: advanced
summary: Exponentiation that precomputes odd powers and processes the exponent in windows to reduce multiplications.
solves: [integer-exponentiation, modular-exponentiation]
model: word-ram
complexity:
  vars: {t: the number of binary digits of the exponent, k: the window width, M: the cost of one multiplication in the monoid (M(n) plus a reduction for residues of n limbs)}
  time: {worst: O((t + 2^k) M), average: O((t + t/(k+1) + 2^k) M), best: O((t + 2^k) M)}
  space: {extra: O(2^k)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [binary-exponentiation, addition-chain]
see_also: [binary-exponentiation, modular-exponentiation, addition-chain-problem, non-adjacent-form, montgomery-multiplication, timing-attack, rsa-cryptosystem, matrix-exponentiation]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.6.3, Evaluation of powers (the 2^k-ary method, its variant with odd powers only, and the bound l(n) <= lg n + (1 + o(1)) lg n / lg lg n)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 14.6.1, Techniques for general exponentiation (Algorithm 14.82, left-to-right k-ary; Algorithm 14.85, sliding-window exponentiation; Table 14.16, the counts for window widths)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 2.6, Modular exponentiation (2.6.2, exponentiation with a larger base, and 2.6.3, sliding window and redundant representation)
  - paper: Ç. K. Koç, Analysis of sliding window techniques for exponentiation, Computers and Mathematics with Applications 30(10), 1995
    title: Çetin Kaya Koç, Analysis of sliding window techniques for exponentiation
    locator: pp. 17 to 24 (the average number of multiplications of fixed and variable windows)
  - url: https://eprint.iacr.org/2017/627
    title: Daniel J. Bernstein and others, Sliding right into disaster, left-to-right sliding windows leak, CHES 2017
    locator: the recovery of RSA keys from the square and multiply pattern of sliding windows in Libgcrypt
---

Sliding-window exponentiation computes $x^e$ in a monoid, such as integers, residues modulo $m$ or matrices, with fewer multiplications than the [binary method](/binary-exponentiation/). It first computes the odd powers $x, x^3, x^5, \ldots, x^{2^k - 1}$, a table of $2^{k-1}$ elements. Then it reads the binary digits of $e$ from the top. A zero digit costs one squaring. A one starts a window of at most $k$ digits that ends with a one; the window costs as many squarings as it has digits and a single multiplication by an entry of the table. For an exponent of $t$ binary digits, the method uses at most $t - 1$ squarings and $\lceil t/k \rceil - 1$ further multiplications after the table, against up to $t - 1$ of each for the binary method; for random exponents the number of windows is about $t/(k+1)$. With $k = \log_2 t - 2\log_2\log_2 t + O(1)$, the total is $t + O(t/\log t)$ multiplications. It is the standard method of big-number libraries for modular exponentiation with public exponents and in Diffie-Hellman and RSA verification.

## In plain words

The binary method reads the exponent one binary digit at a time: square for each digit, and multiply by $x$ for each 1. If the exponent has many 1s, that is many extra multiplications.

The sliding window reads several digits at once. First it makes a small table of odd powers: $x$, $x^3$, $x^5$, $x^7$. Take $x^{13}$, where 13 is 1101 in binary. The window "11" is 3, so start with $x^3$ from the table. The 0 is one squaring, giving $x^6$. The last 1 is a squaring and a product with $x$, giving $x^{13}$. For long exponents, each product with the table covers several digits, so there are far fewer products than 1s. The table costs work up front, so the best window length grows slowly with the length of the exponent.

## The problem

The input is an element $x$ of a monoid, with its product and identity 1, an exponent $e \ge 0$ with binary digits $e_{t-1} \ldots e_0$ and $e_{t-1} = 1$, and a window width $k \ge 1$. The output is $x^e$. For integers this is [integer exponentiation](/integer-exponentiation/), and for residues it is [modular exponentiation](/modular-exponentiation/).

**Cost model.** The cost is the number of products in the monoid, counting squarings separately, since a squaring is often cheaper. On the [word RAM](/word-ram/) with $w$-bit words, a product of residues modulo an $n$-limb number costs $M(n)$ limb operations plus a reduction, for example by [Montgomery multiplication](/montgomery-multiplication/). The worst-case counts are proved; the average counts for random exponents are proved in the cited analyses and also measured here.

## The algorithm

```pseudo id=main
SLIDING-WINDOW-POWER(x, e, k)              ▷ e ≥ 1 with digits e_(t−1) … e_0, e_(t−1) = 1
L1  x2 ← x·x;  T[1] ← x;  T[u] ← T[u − 2]·x2 for u = 3, 5, …, 2^k − 1   ▷ odd powers
L2  y ← 1;  i ← t − 1
L3  while i ≥ 0 do
L4      if e_i = 0 then y ← y·y;  i ← i − 1
        else
L5          j ← the least index ≥ i − k + 1 with e_j = 1;  u ← (e_i … e_j)_2   ▷ odd, < 2^k
            y ← y^(2^(i − j + 1)) by i − j + 1 squarings;  y ← y·T[u];  i ← j − 1
L6  return y
```

Squarings of $y = 1$ and the product $1 \cdot T[u]$ are skipped, so the first window costs nothing; this saves the $k$ or so squarings of the identity that a plain implementation performs. With $k = 1$ there is no table, and the method is the left-to-right binary method.

## Example

Take $e = 2989$, which is $101110101101$ in binary, $t = 12$, and $k = 3$. The table is $x, x^3, x^5, x^7$, at the cost of 1 squaring and 3 products. Reading from the top, the digits split as

$$\underbrace{101}_{5} \; \underbrace{11}_{3} \; 0 \; \underbrace{101}_{5} \; \underbrace{101}_{5} .$$

The window "110" after the first one would end with a 0, so it is cut to "11", and the 0 becomes a squaring of its own. The exponent of $y$ goes

| part | squarings | exponent of $y$ |
|---|---|---|
| 101 | 0, first window | $5$ |
| 11 | 2 | $5 \cdot 4 + 3 = 23$ |
| 0 | 1 | $46$ |
| 101 | 3 | $46 \cdot 8 + 5 = 373$ |
| 101 | 3 | $373 \cdot 8 + 5 = 2989$ |

The main loop makes 9 squarings and 3 products, and with the table the total is 10 squarings and 6 products, 16 in all. The binary method needs $11$ squarings and $7$ products, 18 in all, since $e$ has eight 1s; the $2^3$-ary method with a fixed window also needs 18. The counts were computed by script and are checked by the test of this page.

## Correctness

The invariant of the loop is $y = x^{\lfloor e / 2^{i+1} \rfloor}$, the power for the digits above position $i$. It holds at line L2, where $\lfloor e/2^t \rfloor = 0$ and $y = 1$. A zero digit gives $\lfloor e/2^i \rfloor = 2 \lfloor e/2^{i+1} \rfloor$, which line L4 computes by one squaring. A window from $i$ down to $j$ gives $\lfloor e/2^j \rfloor = \lfloor e/2^{i+1} \rfloor \cdot 2^{i-j+1} + u$, which line L5 computes by $i - j + 1$ squarings and one product with $T[u] = x^u$; the entry exists because $u$ is odd, since $e_j = 1$, and $u < 2^{i-j+1} \le 2^k$. Each step decreases $i$ by at least 1, so the loop ends, at $i = -1$, with $y = x^{\lfloor e/2^0 \rfloor} = x^e$. Line L1 is correct because $T[u-2] \cdot x^2 = x^u$. The full proof is below.

## Complexity

**Worst case, proved.** The table costs $2^{k-1}$ products for $k \ge 2$. The main loop squares once per digit, except for the digits of the first window, so it makes at most $t - 1$ squarings. Each window, together with the zero digits after it, covers at least $\min(k, \text{the digits left})$ digits, because a window is cut short only by zeros, which are then read as squarings. So there are at most $\lceil t/k \rceil$ windows and at most $\lceil t/k \rceil - 1$ products after the first. The total is at most

$$t - 2 + \lceil t/k \rceil + 2^{k-1}$$

products, against $2t - 2$ for the binary method in the worst case.

**Average.** For a random exponent, the digits after a window up to the next 1 are a run of expected length about 1, so the windows are spaced about $k + 1$ digits apart, and the count is about $t + t/(k+1) + 2^{k-1}$. Over 200 random exponents of $t = 1024$ digits, the measured number of windows was within 0.5% of $t/(k + 1)$ for every $k$ from 1 to 7, and the mean total was:

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| mean total | 1534 | 1365 | 1281 | 1233 | 1206 | 1197 | 1210 |
| $t - 1 + t/(k+1) + 2^{k-1}$ | 1536 | 1366 | 1283 | 1236 | 1210 | 1201 | 1215 |

So $k = 6$ is best at this length, saving 22% over the binary method. Minimizing $t/(k+1) + 2^{k-1}$ gives $k = 3$ for $t = 64$, $k = 5$ for $t = 256$ and $512$, $k = 6$ for $t = 1024$, and $k = 7$ for $2048$ and $4096$. With $k = \log_2 t - 2 \log_2 \log_2 t + O(1)$, the extra products are $O(t/\log t)$, which matches the upper bound $\log_2 e + (1 + o(1)) \log_2 e / \log_2\log_2 e$ of Brauer for the length of the shortest [addition chain](/addition-chain/), up to the $o(1)$.

**Space.** $2^{k-1}$ table entries, each the size of an element; for residues of $n$ limbs, $2^{k-1} n$ limbs.

## Properties

- **Generic.** Works in any monoid: integers, residues, polynomials, matrices, points of an elliptic curve.
- **Not recursive.** One pass over the exponent, from the top.
- **Builds an addition chain.** The exponents of the intermediate results form an addition chain for $e$, of length close to the optimum for large $e$.
- **Data-dependent pattern.** The sequence of squarings and products depends on the exponent, which matters for secret exponents.

## Variants and improvements

- **Fixed windows (the $2^k$-ary method).** Split $e$ into digits of exactly $k$ binary digits and use a table of all powers $x^0, \ldots, x^{2^k - 1}$. It is simpler and its pattern does not depend on $e$, but it needs twice the table and slightly more products; over the same 200 exponents of 1024 digits, its best mean was 1247, at $k = 5$, against 1197.
- **Signed windows.** In groups where inverses are free, such as elliptic curves, windows may use digits $\pm u$, as in the [non-adjacent form](/non-adjacent-form/) and its width-$w$ version, which halves the table again.
- **Right-to-left methods.** Yao's method reads the exponent from the low end, with $2^k$ accumulators instead of a table; it suits a fixed exponent and many bases.
- **Fixed base.** When $x$ is fixed and $e$ varies, as for a generator in Diffie-Hellman, precomputed powers $x^{2^{jk}}$ (comb methods, Brickell-Gordon-McCurley-Wilson) remove most squarings.
- **Several bases.** $x^a y^b$ is computed with one sequence of squarings and a joint table (Shamir's trick, Straus 1964).
- **Constant time.** For secret exponents, a fixed window with table lookups that touch every entry, or the Montgomery ladder, gives a pattern independent of $e$.

## When to use it

Use the sliding window for long exponents in any monoid when the exponent is public or timing does not matter: RSA signature verification, primality tests such as [Miller-Rabin](/miller-rabin/), and powers in computer algebra. Choose $k$ from the length of the exponent, as in the table above. For short exponents, below a few dozen digits, the binary method is as good. For secret exponents in cryptography, use a constant-time fixed-window method instead.

## Pitfalls

- **Windows that end with a zero.** A window must end with a 1, or its value is even and missing from the table of odd powers; cut the window and treat the zeros as squarings.
- **Wasted work on the identity.** Starting from $y = 1$ and squaring it costs up to $k$ useless products per call; start from the first window instead.
- **Too wide a window.** The table grows as $2^{k-1}$; a $k$ too large for the exponent loses more in the table than it saves, as the row $k = 7$ above shows.
- **Exponent zero.** $x^0 = 1$ must be handled before the main loop, which assumes $e_{t-1} = 1$.
- **Side channels.** The pattern of squarings and products reveals the windows. Bernstein and others (2017) recovered RSA-1024 keys from Libgcrypt's left-to-right sliding windows by a cache attack; see [timing attack](/timing-attack/).

## Implementations

## History

The $2^k$-ary method appears in Brauer's paper of 1939 on addition chains, where it gives the bound $\log_2 n + (1 + o(1)) \log_2 n / \log_2 \log_2 n$ on the length of a shortest chain. The refinement to windows of odd values that start at a 1 is due to Thurber, in his work on addition chains in 1973, according to Knuth's account in Section 4.6.3, and Knuth's Volume 2 presents both methods. With public-key cryptography, from the late 1970s, fast modular exponentiation became important in practice, and the sliding window method entered handbooks such as Menezes, van Oorschot and Vanstone (1996) and libraries such as GMP and OpenSSL; Koç (1995) analyzed the average counts of the variants. The cache attack of 2017 on Libgcrypt led libraries to use constant-time fixed windows for secret exponents.

## References
