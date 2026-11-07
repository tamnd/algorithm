---
tag: CRTBFS
kind: algorithm
slug: goldschmidt-division
name: Goldschmidt division
aliases:
- Goldschmidt algorithm
- Goldschmidt's division by convergence
- division by convergence
area: numerical/floating-point
level: advanced
summary: Iteratively scales numerator and denominator by correction factors until the denominator reaches one.
solves: [floating-point-division]
model: word-ram
complexity:
  vars: {k: "the number of iterations (3 for binary64 with a 7-bit seed table)", W: the width of the fixed-point datapath}
  time: {worst: Θ(k), average: Θ(k), best: Θ(k)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, in_place: false}
history:
  year: 1964
  people: [Robert E. Goldschmidt]
  note: Goldschmidt described division by convergence in his 1964 MIT master's thesis, and the method was used in the floating-point unit of the IBM System/360 Model 91 (1967).
prereqs: [floating-point-division, newton-raphson-division, floating-point-arithmetic]
see_also: [srt-division, newton-raphson-division, fused-multiply-add, floating-point-product-error, fast-inverse-square-root, long-division, integer-division, correctly-rounded-functions]
sources:
  - paper: "Robert E. Goldschmidt, Applications of division by convergence, M.Sc. thesis, Massachusetts Institute of Technology, 1964"
    title: Robert E. Goldschmidt, Applications of division by convergence (1964)
    locator: the iteration that multiplies dividend and divisor by the same factors until the divisor converges to one
  - paper: "S. F. Anderson, J. G. Earle, R. E. Goldschmidt and D. M. Powers, The IBM System/360 Model 91, floating-point execution unit, IBM Journal of Research and Development 11(1) (1967), 34-53"
    title: Anderson, Earle, Goldschmidt and Powers, The IBM System/360 Model 91, floating-point execution unit (1967)
    locator: the hardware divider based on division by convergence
  - paper: "Stuart F. Oberman and Michael J. Flynn, Division algorithms and implementations, IEEE Transactions on Computers 46(8) (1997), 833-854"
    title: Stuart F. Oberman and Michael J. Flynn, Division algorithms and implementations (1997)
    locator: the section on functional iteration, comparing Newton-Raphson and series expansion (Goldschmidt) and their latencies
  - paper: "Guy Even, Peter-Michael Seidel and Warren E. Ferguson, A parametric error analysis of Goldschmidt's division algorithm, Journal of Computer and System Sciences 70(1) (2005), 118-139"
    title: Guy Even, Peter-Michael Seidel and Warren E. Ferguson, A parametric error analysis of Goldschmidt's division algorithm (2005)
    locator: the error analysis of the iteration with truncated multiplications and the choice of the datapath width
  - paper: "Stuart F. Oberman, Floating point division and square root algorithms and implementation in the AMD-K7 microprocessor, Proceedings of the 14th IEEE Symposium on Computer Arithmetic (ARITH 14), 1999, 106-115"
    title: Stuart F. Oberman, Floating point division and square root algorithms and implementation in the AMD-K7 microprocessor (1999)
    locator: a Goldschmidt-type divider in a commercial x86 processor and its final rounding by remainder
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 4.7, Newton-Raphson-based division with an FMA (iterative division and the final correction by an exact residual); Section 4.5, residuals of division
---

Goldschmidt division computes $a/b$ by multiplying the dividend and the divisor by the same sequence of factors $f_0, f_1, \ldots$ chosen so that the divisor $d_i = b f_0 f_1 \cdots f_{i}$ converges to $1$; the dividend then converges to $a/b$. With $d_i = 1 - \eta$, the factor $f = 2 - d_i = 1 + \eta$ gives $d_{i+1} = 1 - \eta^2$, so the number of correct bits doubles at each step, as in [Newton-Raphson division](/newton-raphson-division/), but the two multiplications of a step are independent, which suits pipelined multipliers. A table gives a first factor with about $7$ correct bits, three iterations reach $56$, and a final comparison of an exact remainder fixes the last bit, so the result is the correctly rounded quotient required for [floating-point division](/floating-point-division/). Goldschmidt proposed it in 1964; it was used in the IBM System/360 Model 91, the AMD K7 and other processors.

## In plain words

To divide one number by another, it is enough to multiply both by the same amount: the answer does not change. Goldschmidt's method keeps multiplying both until the bottom number becomes one. Then the top number is the answer.

At each step the bottom number is a little off from one, say short by a small amount. Multiplying both numbers by one plus that amount makes the bottom number short only by the square of it, which is far smaller. So the error shrinks very fast: a rough start that is right to two digits becomes right to four, then eight, then sixteen. A last check of the remainder makes sure the final digit is the correctly rounded one.

## The problem

**Notation.** Binary64 with round to nearest, ties to even, $p = 53$; $\mathrm{RN}$ is rounding to nearest, and $\mathrm{ulp}$ is as in Muller et al., Section 2.3.2; see [floating-point arithmetic](/floating-point-arithmetic/). The datapath holds nonnegative fixed-point numbers with $W = 64$ fractional bits, and $\mathrm{tr}$ truncates a product to $W$ fractional bits.

**Input.** Positive normal binary64 numbers $a = A \cdot 2^{e_a}$ and $b = B \cdot 2^{e_b}$, $A, B \in [1, 2)$, with a normal quotient (signs, zeros, infinities and NaNs are handled before the iteration, as in any divider).

**Output.** $\mathrm{RN}(a/b)$.

## The algorithm

```pseudo id=main
GOLDSCHMIDT-DIVIDE(a, b, k)          ▷ k ≥ 3 iterations; all values in W-bit fixed point
L1  (A, e_a) ← SPLIT(a);  (B, e_b) ← SPLIT(b)      ▷ A, B in [1, 2)
L2  f ← TABLE(B)                                   ▷ |1 − B·f| < 2^(-7)
L3  n ← tr(A·f);  d ← tr(B·f)
L4  repeat k times
L5      f ← 2 − d                                  ▷ exact
L6      n ← tr(n·f);  d ← tr(d·f)                   ▷ independent products
L7  q ← NEAREST-INTEGER(n / v)                      ▷ v = 2^(-52) if A ≥ B, else 2^(-53)
L8  if A < (q − 1/2)·v·B then q ← q − 1             ▷ exact integer comparison
L9  if A > (q + 1/2)·v·B then q ← q + 1
L10 return q·v·2^(e_a − e_b)
```

The invariant is that $n/d$ stays close to $A/B$ while $d$ approaches $1$. The table in line L2 has $128$ entries indexed by the $7$ leading fraction bits of $B$; entry $i$ is $1/(1 + (i + \tfrac12)/128)$ rounded to $10$ fractional bits. Lines L7 to L9 round $n$ to the binary64 grid of the quotient and correct it by one unit if the exact remainder says so; $v$ is the spacing of binary64 numbers near $A/B$, which lies in $(\tfrac12, 2)$.

## Example

The implementation was run with $k = 3$; the values are the fixed-point numbers divided by $2^{64}$, and $1 - d$ shows the convergence.

**$a = 1$, $b = 3$**, so $A = 1$, $B = 1.5$, table index $64$:

| step | $f$ | $n$ | $d$ | $1 - d$ |
|---|---|---|---|---|
| L3 | 0.665039062500 | 0.66503906250000000 | 0.99755859375000000 | $2.441 \times 10^{-3}$ |
| 1 | 1.002441406250 | 0.66666269302368164 | 0.99999403953552246 | $5.960 \times 10^{-6}$ |
| 2 | 1.000005960464 | 0.66666666664298191 | 0.99999999996447286 | $3.553 \times 10^{-11}$ |
| 3 | 1.000000000036 | 0.66666666666666663 | 1.00000000000000000 | $5.421 \times 10^{-20}$ |

The error $1 - d$ is squared at each step until it reaches $2^{-64} \approx 5.4 \times 10^{-20}$, the truncation of the datapath. Since $A < B$, $v = 2^{-53}$, line L7 gives $q = 6004799503160661$, lines L8 and L9 leave it unchanged, and the result is $q \cdot 2^{-53} \cdot 2^{-1} = 0.3333333333333333$ = 0x1.5555555555555p-2, which is $\mathrm{RN}(1/3)$.

**The Pentium input** $a = 4195835$, $b = 3145727$: $A = 1.0003650188446045$, $B = 1.4999995231628418$, and the first factor $0.66796875$ gives $1 - d_0 = -1.953 \times 10^{-3}$; then $1 - d$ is $3.813 \times 10^{-6}$, $1.454 \times 10^{-11}$ and $2^{-64}$, and the result is $1.333820449136241$, equal to Python's `a / b`.

## Correctness

**Theorem.** For positive normal $a$, $b$ with a normal quotient and $3 \le k \le 64$, the algorithm returns $\mathrm{RN}(a/b)$.

*Proof sketch.* (1) The table entry satisfies $|1 - Bf_0| \le 2^{-8} + 2^{-10} < 2^{-7}$: $B$ is within $2^{-8}$ of the interval midpoint $c_i$, and $f_0$ is within $2^{-11}$ of $1/c_i$. (2) Write $d_j = 1 - \eta_j$ and $n_j = (A/B) d_j + \tau_j$. Since $f_j = 1 + \eta_j$ exactly, line L6 gives $\eta_{j+1} = \eta_j^2 + \beta$ with $0 \le \beta < 2^{-64}$, and $\tau_{j+1} = \tau_j f_j + (A/B)\beta - \alpha$ with $0 \le \alpha < 2^{-64}$: the ratio is perturbed only by truncations, and the perturbations add up linearly. (3) After three steps $\eta_3 < 2^{-55.3}$ and $|\tau_3| < 2^{-60.9}$, so $|n_k - A/B| < 2^{-54} \le v/2$. (4) Then the integer $q$ of line L7 is within $1$ of the correctly rounded $q^{*}$, and lines L8 and L9, which compare $A$ with the midpoints $(q \pm \tfrac12)vB$ exactly, move it to $q^{*}$. A binary quotient is never exactly a midpoint, so no tie arises. The full proof is in `proofs/correctness.md`.

What is proved and what is observed:

- **Proved**: correct rounding to nearest for positive normal inputs with a normal quotient and $3 \le k \le 64$, with the truncated $64$-bit datapath, no FMA, and no floating-point rounding inside the iteration (the iteration uses exact integer products followed by truncation).
- **Observed**: the tests compare the result with the exactly rounded quotient from `fractions.Fraction` for $20000$ random pairs over exponents in $[-400, 400]$, $5000$ pairs of nearby significands and $5000$ quotients of integers, and with Python's hardware division; all agree. With $k = 2$ the result was wrong for about $95\%$ of random pairs in $[1, 2)$, since the error is then near $2^{-28}$.

## Complexity

Each iteration is two multiplications of $(W + 2)$-bit numbers and one subtraction; the multiplications are independent, so with a pipelined multiplier an iteration costs about one multiplier latency plus one cycle. The total is $\Theta(k)$ steps, with $k = \lceil \log_2(p'/t) \rceil$ iterations for $t$ correct bits from the table and $p'$ target bits; for binary64 with $t = 7$ that is $3$. The correction needs one multiplication and comparison (in hardware, the remainder $a - qb$). Space: the table of $2^{t}$ entries and $O(1)$ registers.

## Properties

- **Quadratic convergence.** $1 - d_{j+1} = (1 - d_j)^2$ in exact arithmetic, so $1 - d_k = (1 - d_0)^{2^{k}}$.
- **Independent multiplications.** In each step $n \cdot f$ and $d \cdot f$ do not depend on each other; Newton-Raphson's $y(2 - by)$ has two dependent products.
- **Not self-correcting.** Errors made in $n$ are not removed by later steps; they accumulate (Lemma 2 of the proof). Newton-Raphson, by contrast, corrects errors in its iterate. This is why Goldschmidt needs a wider datapath or a final correction.
- **Same hardware for square root.** Multiplying by factors that drive $b \cdot y^2$ to $1$ gives $\sqrt{b}$ and $1/\sqrt{b}$ the same way.
- **Deterministic and branch-free** apart from the final correction.

## Variants and improvements

- **Series form.** $a/b = a(1 + \eta)(1 + \eta^2)(1 + \eta^4)\cdots$ for $b = 1 - \eta$; this is the same algorithm, written as a product.
- **With an FMA in software.** The steps can be run in binary64 floating point with FMAs; the final correction then uses the exact residual $r = \mathrm{fma}(-q, b, a)$ and the update $q + ry$, as in Markstein's method (Muller et al., Section 4.7).
- **Mixed Goldschmidt and Newton.** Many implementations run Goldschmidt steps first, for parallelism, and finish with a Newton-Raphson step, which corrects accumulated errors.
- **Larger tables.** A $t$-bit seed table reduces $k$; tables of $10$ to $14$ bits and a polynomial seed are common trade-offs between area and latency.
- **Digit recurrence instead.** [SRT division](/srt-division/) needs no multiplier and gives the remainder directly, at the cost of more steps.

## When to use it

Use Goldschmidt division where a fast pipelined multiplier already exists and division latency matters: in floating-point units that share the multiplier, in GPUs and DSPs, and in software on machines without a divider. Use SRT when area and power matter more than latency, and Newton-Raphson with an FMA in software when the FMA is the fastest operation available.

## Pitfalls

- **Too few iterations or too narrow a datapath.** The approximation must be within half a unit of the quotient before the one-step correction; with $k = 2$ the result is often wrong, and with $W$ too close to $p$ the truncation errors reach the last bit.
- **Skipping the correction.** Without lines L8 and L9 the result is only faithful in general; correct rounding needs the remainder.
- **Truncation direction.** The analysis uses truncation toward zero of nonnegative values; rounding the products changes the error terms, and a sign error in the factor $2 - d$ makes the iteration diverge.
- **Special cases.** Zeros, infinities, NaNs, subnormal inputs and results that underflow or overflow must be handled outside the iteration, as in the [floating-point division](/floating-point-division/) problem.
- **Table errors.** A wrong seed entry still converges with enough iterations but can break the fixed iteration count; the Pentium bug was a table error in an SRT divider.

## Implementations

## History

Robert Goldschmidt described division by convergence in his 1964 master's thesis at MIT. The floating-point unit of the IBM System/360 Model 91 (Anderson, Earle, Goldschmidt and Powers, 1967) used it with a fast multiplier. Oberman and Flynn (1997) compared it with digit recurrence and Newton-Raphson in their survey, and Oberman (1999) described a Goldschmidt-type divider in the AMD K7. Even, Seidel and Ferguson (2005) gave a parametric error analysis of the iteration with truncated multiplications.

## References
