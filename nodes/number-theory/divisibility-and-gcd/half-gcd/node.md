---
tag: NZPF3Q
kind: algorithm
slug: half-gcd
name: Half-GCD
aliases:
- Half-GCD algorithm
- Knuth-Schonhage half-gcd
- Schonhage half-gcd
- Schönhage's half-GCD
- subquadratic GCD
area: number-theory/divisibility-and-gcd
level: advanced
summary: A divide-and-conquer gcd for big integers and polynomials that runs in quasi-linear time.
solves: [gcd-of-two-integers]
model: word-ram
complexity:
  vars: {n: the bit length of the larger absolute value of the inputs, M: the cost of multiplying two numbers of bit length n}
  time: {worst: O(M(n) log n), best: O(n)}
  space: {extra: O(n)}
  bit_operations: {worst: O(M(n) log n)}
properties: {deterministic: true, recursive: true}
history:
  year: 1971
  people: [Donald E. Knuth, Arnold Schönhage]
  note: Knuth gave the first subquadratic gcd in 1970 and Schönhage improved it to O(n (log n)^2 log log n) in 1971.
prereqs: [euclidean-algorithm, gcd-recursion-theorem, lehmers-gcd]
see_also: [gcd-of-two-integers, extended-euclidean-algorithm, continued-fraction, polynomial-gcd, karatsuba-multiplication, schonhage-strassen-multiplication, harvey-van-der-hoeven-multiplication, binary-gcd]
sources:
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic
    locator: Section 1.6.3, Half binary GCD, divide and conquer GCD (the divide and conquer idea, its O(M(n) log n) cost, and Algorithm 1.22 HalfBinaryGcd)
  - paper: "N. Möller, On Schönhage's algorithm and subquadratic integer gcd computation, Mathematics of Computation 77 (2008)"
    locator: pages 589 to 607 (the reduction on the high half, the fixup steps and the O(n (log n)^2 log log n) bound)
  - paper: "A. Schönhage, Schnelle Berechnung von Kettenbruchentwicklungen, Acta Informatica 1 (1971)"
    locator: pages 139 to 144
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.5.2, The Greatest Common Divisor (the remarks on asymptotically fast gcd methods after Algorithm L)
---

The half-GCD computes the [greatest common divisor](/gcd-of-two-integers/) of two integers of $n$ bits with $O(M(n) \log n)$ bit operations, where $M(n)$ is the cost of one multiplication. Plain [Euclid](/euclidean-algorithm/) and [Lehmer's GCD](/lehmers-gcd/) need $\Theta(n^2)$. The core is a procedure $\mathrm{HGCD}(a, b)$ that runs Euclid's algorithm only until the remainders fall below $2^{n/2}$, and returns the pair reached together with the $2 \times 2$ matrix of the quotients used. It finds those quotients from the leading halves of the numbers, by two recursive calls of about half the length, and then applies the matrices to the long numbers with fast multiplication. Repeating HGCD halves the length each time, so the gcd costs about as much as one HGCD. The same scheme works for [polynomials](/polynomial-gcd/), and the matrix also gives Bézout coefficients and the [continued fraction](/continued-fraction/) of $a/b$.

## In plain words

Euclid's method on two long numbers makes many small steps, and each step touches the whole numbers. But the first half of the steps depends only on the first half of the digits. So cut both numbers in half, solve the problem for the leading halves, and write down how the steps mix the two numbers as a small table of four numbers. Apply that table to the full numbers in one go with fast multiplication. Now the numbers are shorter, and the same trick on their leading parts gives the next batch of steps. Each piece of work is done on numbers half as long, so the total grows only a little faster than one multiplication.

## The problem

**Input.** Integers $a$ and $b$, of any sign, possibly 0.

**Output.** $\gcd(a, b) \ge 0$, with $\gcd(0, 0) = 0$. Signs are dropped first, and the larger absolute value is put first, so the core works on $a \ge b \ge 0$.

**The half problem.** For $a \ge b \ge 0$ with $n$ bits in $a$, let $m = \lceil n/2 \rceil$. Euclid's algorithm produces the remainders $r_0 = a$, $r_1 = b$, $r_{i+1} = r_{i-1} \bmod r_i$, which decrease, so there is exactly one $j$ with $r_j \ge 2^m > r_{j+1}$ (if $b < 2^m$, then $j = 0$). $\mathrm{HGCD}(a, b)$ returns $(\alpha, \beta) = (r_j, r_{j+1})$, the quotients $q_1, \ldots, q_j$, and the matrix

$$M = \begin{pmatrix} q_1 & 1 \\ 1 & 0 \end{pmatrix} \cdots \begin{pmatrix} q_j & 1 \\ 1 & 0 \end{pmatrix}, \qquad \begin{pmatrix} a \\ b \end{pmatrix} = M \begin{pmatrix} \alpha \\ \beta \end{pmatrix},$$

with $\det M = (-1)^j$. So $\beta$ has at most about half the bits of $a$, and $\gcd(a, b) = \gcd(\alpha, \beta)$.

**Cost model.** Arbitrary precision on the [word RAM](/word-ram/): numbers are arrays of $w$-bit words, $n$ is the bit length of $\max(|a|, |b|)$, and costs are counted in bit operations. $M(n)$ is the cost of multiplying two $n$-bit numbers, and division with remainder costs $O(M(n))$; with [Karatsuba](/karatsuba-multiplication/) $M(n) = O(n^{1.59})$, with [Schönhage and Strassen](/schonhage-strassen-multiplication/) $O(n \log n \log \log n)$, and with [Harvey and van der Hoeven](/harvey-van-der-hoeven-multiplication/) $O(n \log n)$. Below a threshold of $T$ bits the algorithm switches to plain Euclid; $T$ is a tuning constant.

## The algorithm

```pseudo id=main
HGCD(a, b)                                         ▷ a ≥ b ≥ 0; returns (M, Q, α, β)
L1  n ← bitlength(a);  m ← ⌈n / 2⌉;  M ← I;  Q ← empty list
L2  if b < 2^m then return (M, Q, a, b)
L3  if n ≤ T then do Euclid steps while b ≥ 2^m, recording each q in M and Q; return (M, Q, a, b)
L4  (R, P) ← HGCD(⌊a / 2^m⌋, ⌊b / 2^m⌋)                ▷ quotients of the leading halves
L5  (M, Q, a, b) ← FIXUP(R, P, a, b, 2^m)
L6  if b ≥ 2^m then one Euclid step (a, b) ← (b, a mod b), recorded in M and Q
L7      if b ≥ 2^m and 2(bitlength(a) − m) < n then k ← 2m − bitlength(a);  (S, P) ← HGCD(⌊a / 2^k⌋, ⌊b / 2^k⌋)
L8          (S, P, a, b) ← FIXUP(S, P, a, b, 2^m);  M ← M S;  append P to Q
L9  while b ≥ 2^m do one Euclid step, recorded in M and Q
L10 return (M, Q, a, b)

FIXUP(R, P, a, b, L)                                ▷ R = product of the quotient matrices of P
L11 (α, β) ← R⁻¹ (a, b)
L12 while P is not empty and not (α > β > 0 and α ≥ L) do
        q ← remove the last element of P;  R ← R · [q 1; 1 0]⁻¹;  (α, β) ← (q α + β, α)
L13 return (R, P, α, β)

GCD(a, b)
L14 (a, b) ← (max(|a|, |b|), min(|a|, |b|))
L15 while b ≥ 2^T do (_, _, a, b) ← HGCD(a, b);  if b ≠ 0 then (a, b) ← (b, a mod b)
L16 while b ≠ 0 do (a, b) ← (b, a mod b)
L17 return a
```

Recording a quotient $q$ means $M \leftarrow M \begin{pmatrix} q & 1 \\ 1 & 0 \end{pmatrix}$ and appending $q$ to $Q$. The inverse of a quotient matrix is $\begin{pmatrix} 0 & 1 \\ 1 & -q \end{pmatrix}$, and $R^{-1}$ is the adjugate of $R$ times $\det R = \pm 1$, so line L11 costs four multiplications.

The call of line L4 runs Euclid on the leading $n - m$ bits. Its quotients are usually the true quotients of $(a, b)$, but the last one or two can be wrong, because the low bits were cut off. FIXUP applies the matrix to the full numbers and checks the result; if it is not a valid pair of remainders, it takes back the last quotients one at a time. After line L5 the smaller number $b$ has about $3n/4$ bits, and after the step of line L6 the call of line L7 is on the leading $2(\ell - m)$ bits of numbers with $\ell$ bits, about $n/2$ of them, which brings $b$ below $2^m$ up to a few more steps.

## Example

HGCD on $a = 3141592653$ and $b = 2718281828$, with threshold $T = 16$. Here $n = 32$, $m = 16$ and $2^m = 65536$. Full Euclid on $(a, b)$ has 21 quotients: $1, 6, 2, 2, 1, 2, 6, 8, 2, 1, 1, 1, 3, 6, 1, 2, 1, 10, 1, 20, 2$.

| line | action | $(a, b)$ after the line | quotients added |
| --- | --- | --- | --- |
| L1 | $n = 32$, $m = 16$ | $(3141592653, 2718281828)$ | |
| L4 | call on the leading halves $(47936, 41477)$: 16 bits, so line L3 runs Euclid until below $2^8$ and stops at $(316, 65)$ | | |
| L5 | $R = \begin{pmatrix} 141 & 52 \\ 122 & 45 \end{pmatrix}$, $R^{-1}(a, b)$ is valid, no quotient taken back | $(21014329, 3434082)$ | $1, 6, 2, 2, 1, 2$ |
| L6 | one long division, $q = 6$ | $(3434082, 409837)$ | $6$ |
| L7 | $\ell = 22$, $k = 2 \cdot 16 - 22 = 10$; call on $(3353, 400)$, which stops at $(94, 59)$ below $2^6$ | | |
| L8 | $S = \begin{pmatrix} 25 & 17 \\ 3 & 2 \end{pmatrix}$, $S^{-1}(a, b)$ is valid | $(99065, 56321)$ | $8, 2, 1$ |
| L9 | $56321 < 65536$, no step | $(99065, 56321)$ | |
| L10 | return $M = \begin{pmatrix} 22873 & 15548 \\ 19791 & 13453 \end{pmatrix}$ | | |

The ten quotients found are the first ten of Euclid's, and $(99065, 56321)$ are Euclid's remainders $r_{10}$ and $r_{11}$, the first remainder below $2^{16}$ and the one before it. Only three operations touched the 32-bit numbers: two matrix applications and one division. Check: $22873 \cdot 99065 + 15548 \cdot 56321 = 3141592653$. GCD then does one division, $(56321, 42744)$, and the rest is short; the result is 1.

## Correctness

Three facts give correctness; the full proof is in `proofs/correctness.md`.

1. **Valid pairs are Euclid states.** If $R$ is a product of quotient matrices with quotients $q_1, \ldots, q_j \ge 1$, $j \ge 1$, and $(\alpha, \beta) = R^{-1}(a, b)$ satisfies $\alpha > \beta > 0$, then Euclid on $(a, b)$ starts with exactly the quotients $q_1, \ldots, q_j$ and reaches $(\alpha, \beta)$. Proof: going back up from $(\alpha, \beta)$, each pair $(x, y)$ with $x > y > 0$ comes from $(qx + y, x)$, whose first entry is again larger than its second, and $\lfloor (qx + y)/x \rfloor = q$ with remainder $y$. So the condition of line L12 certifies the quotients, and FIXUP stops at the latest when all quotients are taken back.
2. **Invariant.** In HGCD, the current pair is always the state of Euclid on the original input after the quotients in $Q$, $M$ is their product, and $a \ge 2^m$. Lines L5 and L8 keep this by fact 1 and the test $\alpha \ge 2^m$; lines L6 and L9 do true Euclid steps only while $b \ge 2^m$.
3. **Exit.** Line L10 is reached with $b < 2^m \le a$, so the pair is the unique Euclid state that straddles $2^m$. Every matrix has determinant $\pm 1$, so $\gcd$ is kept, and GCD ends with plain Euclid.

The recursion terminates because the call of line L4 has $n - m < n$ bits, and line L7 calls only when the input has $2(\ell - m) < n$ bits.

## Complexity

- **Recurrence.** Apart from the two recursive calls, HGCD on $n$ bits does $O(1)$ multiplications and divisions of numbers with $O(n)$ bits, plus the steps taken back in FIXUP and the steps of line L9. The analyses of Schönhage, Thull and Yap, and Möller show that both are $O(1)$, and that the calls are on $n/2 + O(1)$ bits. In our tests with $T = 64$ on random and Fibonacci inputs of up to 20000 bits, FIXUP never took back more than two quotients, line L9 never did more than two steps, and the call of line L7 never had more than $\lceil n/2 \rceil + 15$ bits, and the guard of line L7 never skipped a call. So $H(n) \le 2 H(n/2 + O(1)) + O(M(n))$, which gives $H(n) = O(M(n) \log n)$ for $M(n)/n$ nondecreasing.
- **The GCD loop.** Each pass of line L15 does one HGCD and one division, and halves the bit length, so the total is $O(M(n) \log n)$ as well.
- **Bounds.** With [Harvey and van der Hoeven's multiplication](/harvey-van-der-hoeven-multiplication/), the gcd of $n$-bit integers takes $O(n (\log n)^2)$ bit operations; with Schönhage and Strassen, $O(n (\log n)^2 \log \log n)$, the bound of Schönhage's paper; with Karatsuba, $O(n^{1.59})$, since the $\log n$ is absorbed by a polynomial recurrence. The best case is $b < 2^T$, which costs one division, $O(n)$ bit operations when $b$ is that small.
- **Space.** The matrix entries at a level of $n$ bits have at most about $n/2$ bits, the quotients in $Q$ have at most $n + |Q|$ bits in total, and the stack holds levels of geometrically decreasing size, so the extra space is $O(n)$ bits. The recursion depth is $\log_2(n/T) + O(1)$.

## Properties

- **Same quotients as Euclid.** HGCD returns exactly Euclid's quotients and remainders, in order. So it computes the [continued fraction](/continued-fraction/) of $a/b$, and the product of all matrices gives the Bézout coefficients of the [extended Euclidean algorithm](/extended-euclidean-algorithm/): if $(a, b) = M (g, 0)$, with $M = \begin{pmatrix} m_{00} & m_{01} \\ m_{10} & m_{11} \end{pmatrix}$, the first row of $M^{-1} = \det M \cdot \begin{pmatrix} m_{11} & -m_{01} \\ -m_{10} & m_{00} \end{pmatrix}$ gives $s, t$ with $as + bt = g$.
- **Recursive.** Depth $O(\log n)$; the Python implementation below uses recursion, which is safe at this depth.
- **Deterministic.**

## Variants and improvements

- **Polynomials.** For polynomials over a field, the degree plays the role of the bit length, and there are no carries, so the high half gives exact quotients and no fixup is needed. This is the HGCD of Aho, Hopcroft and Ullman, and the basis of the fast [polynomial GCD](/polynomial-gcd/) and fast [extended Euclidean algorithm for polynomials](/polynomial-extended-euclidean-algorithm/).
- **Möller's variant.** Möller's algorithm uses a different reduction condition and fixup, which makes the analysis simpler and the code shorter; it is the one used in GMP.
- **Half binary GCD.** Stehlé and Zimmermann's algorithm works from the low bits, like the [binary GCD](/binary-gcd/), which avoids the carry problem; Brent and Zimmermann give it as Algorithm 1.22.
- **Lehmer at the leaves.** Real implementations replace plain Euclid below the threshold by [Lehmer's GCD](/lehmers-gcd/) with a word-sized matrix.
- **Extended GCD and continued fractions.** Keep the matrices, as above; the same recursion gives fast rational reconstruction and fast [continued fraction convergents](/continued-fraction-convergents/).

## When to use it

Use the half-GCD for integers of many thousands of bits and more, where fast multiplication pays off; in GMP the crossover from Lehmer's method is a tuned threshold of some hundreds of words, which depends on the machine. Below that, use Lehmer's GCD or the binary GCD; for word-sized inputs, use plain Euclid or the binary GCD. In the Python implementation below, which multiplies with Karatsuba's method, the half-GCD was about 5 times faster than a Python loop of plain Euclid at $10^5$ bits and about 10 times faster at $4 \cdot 10^5$ bits, but the built-in `math.gcd`, written in C, was faster still at these sizes.

## Pitfalls

- **Trusting the high half.** The quotients of the leading halves are not always the true quotients. With $a = 2723649695$ and $b = 1569894979$, the leading 16 bits give the quotients $1, 1, 2, 1, 3, 2, 2$, but Euclid on $(a, b)$ has $1, 1, 2, 1, 3, 2, 1, 1$. Applying the seven matrices gives the pair $(19714131, -1952291)$, which has a negative entry. FIXUP takes back the last quotient and gets $(37475971, 19714131)$, the true state after six steps.
- **Overshooting.** The call of line L7 can also return a pair whose larger entry is already below $2^m$. Without the test $\alpha \ge 2^m$ in line L12, HGCD would return the wrong pair, which harms nothing for the gcd but breaks the specification, and with it the size bounds of the analysis.
- **Equal leading halves.** If $\lfloor a/2^m \rfloor = \lfloor b/2^m \rfloor$, the recursive result can make $\alpha = \beta$; the identity matrix must then be accepted, as line L12 does.
- **No progress.** If HGCD returns at once because $b < 2^m$, the division of line L15 is what shortens the numbers; leaving it out makes the loop run forever.
- **Slow multiplication.** With schoolbook multiplication, $M(n) = \Theta(n^2)$ and the method costs $\Theta(n^2 \log n)$, worse than Euclid. The gain needs subquadratic multiplication and division.

## Implementations

## History

Lehmer's 1938 method found many Euclid steps from the leading word. Knuth, in his 1970 address to the International Congress of Mathematicians, applied the idea recursively to leading halves and obtained the first subquadratic gcd, with $O(n (\log n)^5 \log \log n)$ bit operations. Schönhage improved it in 1971 to $O(n (\log n)^2 \log \log n)$ in a paper on the fast computation of continued fractions. For polynomials, Moenck and then Aho, Hopcroft and Ullman gave the half-GCD under that name. The details for integers are delicate, and published versions contained errors; Thull and Yap gave a careful version in 1990, and Möller in 2008 a simpler one, which GMP adopted.

## References
