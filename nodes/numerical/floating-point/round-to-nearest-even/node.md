---
tag: NM70WW
kind: definition
slug: round-to-nearest-even
name: Round to nearest, ties to even
aliases:
- banker's rounding
- round-half-to-even
- roundTiesToEven
- RN
area: numerical/floating-point
level: intro
summary: The default IEEE 754 rounding. It returns the float nearest to the exact result and breaks an exact tie toward the neighbour whose last significand digit is even.
prereqs: [floating-point-arithmetic, rounding-modes]
see_also: [rounding-modes, ulp, ieee-754, machine-epsilon, double-rounding, stochastic-rounding, floating-point-model, error-free-transformations]
sources:
  - url: https://doi.org/10.1109/IEEESTD.2019.8766229
    title: IEEE Std 754-2019, IEEE Standard for Floating-Point Arithmetic
    locator: Clause 4.3.1, Rounding-direction attributes to nearest (roundTiesToEven, the overflow rule); Clause 4.3.3 (roundTiesToEven is the default for binary formats)
  - book: isbn:9783319765259
    title: Jean-Michel Muller et al., Handbook of Floating-Point Arithmetic, second edition, Birkhauser, 2018
    locator: Section 2.2, Rounding (the definition of RN with ties to even and its properties); Chapters 7 and 8 on the implementation of rounding in the basic operations (guard, round and sticky bits)
  - paper: doi:10.1145/103162.103163
    title: David Goldberg, What every computer scientist should know about floating-point arithmetic, ACM Computing Surveys 23(1) (1991), 5-48
    locator: Section 1.5, Exactly Rounded Operations (Theorem 5 and the example of drift with round half up)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, Addison-Wesley, 1998
    locator: Section 4.2.1 (normalization and rounding, Algorithm N) and Section 4.2.2 (the result of Reiser and Knuth on (u ⊖ v) ⊕ v with rounding to even)
  - paper: "John F. Reiser and Donald E. Knuth, Evading the drift in floating-point addition, Information Processing Letters 3(3) (1975), 84-87"
    title: John F. Reiser and Donald E. Knuth, Evading the drift in floating-point addition, Information Processing Letters 3(3) (1975), 84-87
    locator: the proof that rounding to even stops the drift of repeated addition and subtraction
---

Round to nearest, ties to even, is the rounding rule that maps a real number to the nearest [floating-point](/floating-point-arithmetic/) number, and maps a number exactly halfway between two floats to the one whose last significand digit is even. It is roundTiesToEven of [IEEE 754](/ieee-754/), the default for binary formats, so it is the rounding of nearly all floating-point code, including each Python `float` operation and Python's `round`. Its error is at most half an [ulp](/ulp/), and the tie rule makes the errors of exact ties cancel on average instead of drifting in one direction.

## Definition

**Notation.** A floating-point system $\mathbb{F}$ has base $\beta$, precision $p$ and exponent range $[e_{\min}, e_{\max}]$; the default is binary64 ($\beta = 2$, $p = 53$, $e_{\min} = -1022$, $e_{\max} = 1023$). Each finite float is $x = M \beta^{q}$ with integers $M$ and $q$, $|M| < \beta^{p}$ and $q \ge e_{\min} - p + 1$. The unit roundoff is $u = \tfrac12\beta^{1-p}$ ($2^{-53}$ for binary64). $\Omega$ is the largest finite float.

**Definition.** Let $x$ be a real number with $|x| \le \Omega$. If $x \in \mathbb{F}$, then $\mathrm{RN}(x) = x$. Otherwise let $a < x < b$ be the two floats next to $x$ (see [rounding modes](/rounding-modes/)). Then

$$\mathrm{RN}(x) = \begin{cases} a & \text{if } x - a < b - x, \\ b & \text{if } b - x < x - a, \\ \text{the one of } a, b \text{ whose integral significand } M \text{ is even} & \text{if } x - a = b - x. \end{cases}$$

The significand $M$ of each float is taken with the exponent of the binade of $x$, $q = \max(e, e_{\min}) - p + 1$ where $\beta^{e} \le |x| < \beta^{e+1}$, so $a$ and $b$ are consecutive multiples $M\beta^{q}$ and $(M+1)\beta^{q}$, and exactly one of $M$ and $M + 1$ is even. (If $b = \beta^{e+1}$, its significand on this grid is $\beta^{p}$, which is even for an even $\beta$; the standard states the rule as "the one with an even least significant digit".)

**Overflow (Clause 4.3.1).** For $|x| > \Omega$, $\mathrm{RN}(x) = \pm\infty$ when $|x| \ge \beta^{e_{\max}}(\beta - \tfrac12 \beta^{1-p})$, and $\pm\Omega$ otherwise. So the rule treats the value $\beta^{e_{\max}+1}$ as if it existed, with an even significand, and then replaces it by $\infty$.

**The rule in binary, on integers.** To round a positive integer $n$ to the nearest multiple of $2^{k}$ (with $k \ge 1$), write $n = 2^{k} Q + R$ with $0 \le R < 2^{k}$. Then

$$\mathrm{RN}_k(n) = \begin{cases} 2^{k} Q & \text{if } R < 2^{k-1}, \\ 2^{k} (Q + 1) & \text{if } R > 2^{k-1}, \\ 2^{k} (Q + (Q \bmod 2)) & \text{if } R = 2^{k-1}. \end{cases}$$

Hardware computes the same thing with three bits after the kept ones: the *guard* bit $G$ (the first dropped bit), the *round* bit, and the *sticky* bit, the OR of all later bits. With $L$ the last kept bit and $S'$ the OR of the round and sticky bits, the result rounds up exactly when $G \wedge (L \vee S')$.

**Properties (proved).**

1. *Error.* $|\mathrm{RN}(x) - x| \le \tfrac12\mathrm{ulp}(x)$, and $\mathrm{RN}(x) = x(1 + \delta)$ with $|\delta| \le u/(1 + u)$ in the normal range (proof on the [machine epsilon](/machine-epsilon/) page). The tie rule has no effect on these bounds.
2. *Monotone and odd.* $x \le y$ implies $\mathrm{RN}(x) \le \mathrm{RN}(y)$, and $\mathrm{RN}(-x) = -\mathrm{RN}(x)$. Both follow from the definition, because the tie rule depends on $|x|$ only.
3. *No drift (Reiser and Knuth 1975; Goldberg, Theorem 5).* For floats $x$ and $y$, let $x_0 = x$ and $x_{n} = \mathrm{RN}(\mathrm{RN}(x_{n-1} - y) + y)$. With ties to even, either $x_n = x$ for all $n$, or $x_n = x_1$ for all $n \ge 1$. With ties away from zero the sequence can move by one ulp at each step.
4. *Unbiased on ties.* If the last kept digit is even or odd with equal frequency, half of the ties round up and half round down, so the mean error over ties is zero. Ties away from zero, in contrast, rounds every positive tie up.

## Examples and non-examples

**Ties in binary64.** The real $1 + 2^{-53}$ is halfway between $1 = 2^{52} \cdot 2^{-52}$ (even $M$) and $1 + 2^{-52}$ (odd $M$), so it rounds to 1, and `1.0 + 2**-53 == 1.0` is true. For integers above $2^{53}$, where the floats are the even integers: $2^{53} + 1 \mapsto 2^{53}$, $2^{53} + 3 \mapsto 2^{53} + 4$, $2^{54} + 2 \mapsto 2^{54}$ (the floats there are multiples of 4) and $2^{54} + 6 \mapsto 2^{54} + 8$. In each case the result's significand $M$ is even.

**The integer rule agrees with the hardware.** For 100000 random 60-bit integers $n$ with the top bit set, $\mathrm{RN}_7(n)$ from the formula above equals `int(float(n))`, which is the binary64 rounding of $n$ to 53 significant bits.

**Python's `round`.** `round(0.5) == 0`, `round(1.5) == 2`, `round(2.5) == 2`, `round(3.5) == 4` and `round(-2.5) == -2`. A call such as `round(2.675, 2) == 2.67` is not a tie: the stored value of `2.675` is below 2.675.

**Drift with round half up.** Goldberg's example is decimal with $p = 3$, $x = 1.00$ and $y = -0.555$. With round half up, $x_1 = 1.01$, $x_2 = 1.02$, $x_3 = 1.03$, and so on: $1.00 + 0.555 = 1.555$ rounds up to $1.56$, and $1.56 - 0.555 = 1.005$ rounds up to $1.01$. With round half even, $1.555 \mapsto 1.56$ and $1.005 \mapsto 1.00$, so $x_n = 1.00$ for each $n$. Python's `decimal` module with a precision of 3 gives exactly these sequences under `ROUND_HALF_UP` and `ROUND_HALF_EVEN`.

**Non-examples.**

- *Round half up* (the school rule) and *round half away from zero* (C's `round` function, and roundTiesToAway of IEEE 754) give the same result as ties to even except on exact ties.
- *Round half to odd*, and the different *round to odd* (a sticky rounding that returns the neighbour with an odd last bit whenever $x \notin \mathbb{F}$), are not IEEE 754 modes. Round to odd at a higher precision followed by round to nearest at the target precision avoids [double rounding](/double-rounding/) errors.
- Rounding to nearest *twice*, first to a wider format and then to the target, is not the same as rounding once. The tie rule is the reason: the first rounding can create a tie that did not exist.
- Truncation, used by C to convert a `double` to an `int`, is round toward zero, not to nearest.

## Related definitions

- [Rounding modes](/rounding-modes/): the four other IEEE 754 roundings.
- [Unit in the last place](/ulp/) and [machine epsilon](/machine-epsilon/): the size of the error that $\mathrm{RN}$ makes.
- [Standard model of floating-point arithmetic](/floating-point-model/): the relative error bound $u$ that $\mathrm{RN}$ gives.
- [Error-free transformations](/error-free-transformations/): algorithms such as [TwoSum](/two-sum/) whose proofs need $\mathrm{RN}$, not only the bound $u$.
- [Double rounding](/double-rounding/): the error of two successive roundings to nearest.
- [Stochastic rounding](/stochastic-rounding/): a random tie-free alternative used in low precision.

## References
