---
tag: 09SJJW
kind: definition
slug: maximal-length-sequence
name: Maximal-length sequence
aliases:
- m-sequence
- PN sequence
- pseudonoise sequence
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "The output of a linear feedback shift register with a primitive polynomial of degree n. It has period 2^n - 1, is nearly balanced, and its periodic autocorrelation takes only two values."
model: word-ram
prereqs: [linear-feedback-shift-register, primitive-polynomial]
see_also: [gold-sequences, kasami-sequences, de-bruijn-sequence, autocorrelation, hamming-code, direct-sequence-spread-spectrum, barker-code, welch-bound]
sources:
  - book: isbn:9789814632003
    title: Solomon W. Golomb, Shift Register Sequences, third revised edition, World Scientific, 2017 (first edition Holden-Day, 1967)
    locator: The chapters on linear shift register sequences (the period of the recurrence of a primitive polynomial) and on the randomness postulates (balance, the run property and the two-level autocorrelation)
  - paper: doi:10.1109/PROC.1980.11697
    title: Dilip V. Sarwate and Michael B. Pursley, Crosscorrelation properties of pseudorandom and related sequences, Proceedings of the IEEE 68(5), 1980
    locator: pp. 593 to 619 (the sections on m-sequences, their periodic autocorrelation and the shift-and-add property)
  - paper: doi:10.1109/TCOM.1982.1095533
    title: Raymond L. Pickholtz, Donald L. Schilling and Laurence B. Milstein, Theory of spread-spectrum communications, a tutorial, IEEE Transactions on Communications 30(5), 1982
    locator: pp. 855 to 884 (the section on pseudonoise generators and the properties of maximal-length sequences)
---

A maximal-length sequence, or m-sequence, is the output of a binary [linear feedback shift register](/linear-feedback-shift-register/) whose feedback polynomial is [primitive](/primitive-polynomial/). A register of $n$ cells can hold $2^n - 1$ nonzero states, and with a primitive polynomial it goes through all of them before it repeats, so the output has the longest possible period $N = 2^n - 1$. Three properties make m-sequences the standard spreading code of [direct-sequence spread spectrum](/direct-sequence-spread-spectrum/) and the building block of [Gold](/gold-sequences/) and [Kasami](/kasami-sequences/) sequences: the numbers of ones and zeros in a period differ by one, the runs have a fixed distribution, and the periodic [autocorrelation](/autocorrelation/) in $\pm 1$ form is $N$ at shift $0$ and $-1$ at every other shift. These are exact results for every primitive polynomial, not statistics of a random model. The sequence is easy to predict from $2n$ consecutive bits, so it is pseudorandom in the sense of correlation, not in the sense of cryptography.

## Definition

Let $f(x) = x^n + f_{n-1} x^{n-1} + \cdots + f_1 x + 1$ be a polynomial over GF(2), with $f_i \in \{0, 1\}$. A binary sequence $s_0, s_1, s_2, \ldots$ satisfies the **linear recurrence of $f$** if

$$s_{k+n} = \sum_{i=0}^{n-1} f_i \, s_{k+i} \pmod 2 \qquad \text{for all } k \ge 0, \quad f_0 = 1.$$

The start state $(s_0, \ldots, s_{n-1})$ fixes the whole sequence. The sequence is periodic, because the state $(s_k, \ldots, s_{k+n-1})$ can take at most $2^n$ values and the map from one state to the next is invertible (the constant term $f_0 = 1$ lets us recover $s_k$ from the next state). The zero state gives the zero sequence, so a nonzero start gives a period of at most $2^n - 1$.

A **maximal-length sequence** of degree $n$ is a nonzero sequence that satisfies the recurrence of some $f$ of degree $n$ and has period exactly $N = 2^n - 1$. This happens if and only if $f$ is a primitive polynomial: $f$ is irreducible and its roots have multiplicative order $2^n - 1$ in GF($2^n$) (Golomb, the chapter on linear shift register sequences). Then every nonzero start state gives an m-sequence, and the $2^n - 1$ nonzero start states give the $N$ cyclic shifts of one sequence.

The **$\pm 1$ form** maps bit $0$ to $+1$ and bit $1$ to $-1$: $a_k = (-1)^{s_k} = 1 - 2 s_k$. The **periodic correlation** of two $\pm 1$ sequences $a$ and $b$ of period $N$ at shift $t$ is

$$C_{a,b}(t) = \sum_{k=0}^{N-1} a_k \, b_{(k+t) \bmod N},$$

and the periodic autocorrelation is $C_{a,a}(t)$. The mapping turns XOR into a product: $(-1)^{s \oplus s'} = (-1)^{s} (-1)^{s'}$.

The procedure below generates one period and its autocorrelation. It uses $O(n)$ word operations per output bit, or $O(1)$ if the taps are packed into one machine word, so one period costs $O(N n)$ in the [word RAM](/word-ram/) model in this plain form, and the full autocorrelation costs $O(N^2)$ by direct sums.

```pseudo id=main
M-SEQUENCE(f, state)        ▷ f primitive of degree n, state ≠ 0, N = 2^n - 1
L1  s[0 .. n-1] ← state
    for k ← 0 to N - n - 1 do
L2      b ← XOR of s[k + i] over the exponents i < n of f
L3      s[k + n] ← b
L4  a[k] ← 1 - 2 s[k] for k = 0, ..., N - 1        ▷ the ±1 form
L5  C(t) ← Σ_k a[k] a[(k + t) mod N] for t = 0, ..., N - 1
    return s, C
```

**Properties.** Let $s$ be an m-sequence of degree $n$ and period $N = 2^n - 1$. Golomb lists the first three as his randomness postulates, and m-sequences satisfy all of them:

1. **Balance.** One period holds $2^{n-1}$ ones and $2^{n-1} - 1$ zeros. In $\pm 1$ form, $\sum_k a_k = -1$.
2. **Runs.** A run is a maximal block of equal bits, read cyclically. One period has $2^{n-1}$ runs. For $1 \le \ell \le n - 2$ there are $2^{n-\ell-2}$ runs of ones and $2^{n-\ell-2}$ runs of zeros of length $\ell$. There is one run of $n - 1$ zeros and one run of $n$ ones.
3. **Two-level autocorrelation.** $C_{a,a}(0) = N$ and $C_{a,a}(t) = -1$ for $t = 1, \ldots, N - 1$.
4. **Window property.** Each nonzero $n$-tuple appears exactly once as a window $(s_k, \ldots, s_{k+n-1})$ in one period. The zero $n$-tuple never appears.
5. **Shift and add.** For $t \not\equiv 0 \pmod N$, the sum $s_k \oplus s_{k+t}$ is again a shift $s_{k+d}$ of the same sequence, for some $d$ that depends on $t$.

Property 3 follows from properties 5 and 1. For $t \ne 0$, $a_k a_{k+t} = (-1)^{s_k \oplus s_{k+t}} = (-1)^{s_{k+d}}$, so $C_{a,a}(t) = \sum_k (-1)^{s_{k+d}}$, which is the number of zeros minus the number of ones in a period: $(2^{n-1} - 1) - 2^{n-1} = -1$. Property 5 holds because the sum of two solutions of a linear recurrence is a solution, its start state is nonzero when $t \ne 0$ (by property 4), and every nonzero solution is a shift of $s$.

Two consequences follow. The DFT of one period of $a$ has $|A[0]|^2 = 1$ and $|A[k]|^2 = N + 1$ for $k \ne 0$, since the DFT of the autocorrelation $(N + 1)\delta_t - 1$ is the squared magnitude spectrum. So the periodic sequence has a flat line spectrum except at zero frequency, which is why it looks like white noise to a correlator. Second, the $N$ shifts of one period together with the zero word are the codewords of the simplex code of length $N$ and dimension $n$, the dual of the [Hamming code](/hamming-code/); every nonzero codeword has weight $2^{n-1}$. The number of distinct m-sequences of degree $n$, up to shifts, equals the number of primitive polynomials of degree $n$, which is $\varphi(2^n - 1)/n$ with Euler's function $\varphi$.

## Examples and non-examples

**Degree 3.** Take $f(x) = x^3 + x + 1$, so the recurrence is $s_{k+3} = s_{k+1} \oplus s_k$. From the state $100$:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $s_k$ | 1 | 0 | 0 | 1 | 0 | 1 | 1 |
| window $s_k s_{k+1} s_{k+2}$ | 100 | 001 | 010 | 101 | 011 | 111 | 110 |
| $a_k$ | -1 | +1 | +1 | -1 | +1 | -1 | -1 |

Then $s_7 = s_5 \oplus s_4 = 1 = s_0$, $s_8 = s_6 \oplus s_5 = 0 = s_1$, and the sequence $1001011$ repeats with period $7 = 2^3 - 1$. The windows list all seven nonzero triples once. There are four ones and three zeros. The periodic autocorrelation at shifts $0$ to $6$ is $(7, -1, -1, -1, -1, -1, -1)$. At shift $1$, for example, the products $a_k a_{k+1}$ are $-1, +1, -1, -1, -1, +1, +1$, with sum $-1$. Shift and add: $s_k \oplus s_{k+1}$ for $k = 0, \ldots, 6$ is $1011100$, which is $s_{k+3}$, the sequence shifted by $3$.

**Degree 4.** $f(x) = x^4 + x + 1$ from the state $1000$ gives $100010011010111$, of period $15$, with eight ones and seven zeros. Its $8$ runs are two runs of length $1$ of each bit, one run of length $2$ of each bit, one run of three zeros and one run of four ones, as property 2 says. The autocorrelation is $15$ at shift $0$ and $-1$ at the other $14$ shifts.

**Degree 5.** $f(x) = x^5 + x^2 + 1$ from $10000$ gives the period $1000010010110011111000110111010$ of length $31$. Degree 5 has $\varphi(31)/5 = 6$ primitive polynomials, so there are six different m-sequences of period 31. Two of them, from $x^5 + x^2 + 1$ and $x^5 + x^4 + x^3 + x^2 + 1$, form the preferred pair behind the [Gold sequences](/gold-sequences/) of period 31.

**Non-example: a reducible polynomial.** $x^4 + x^2 + 1 = (x^2 + x + 1)^2$ gives period $6$ from the state $1000$, not $15$. The register splits its nonzero states into several shorter cycles.

**Non-example: irreducible but not primitive.** $x^4 + x^3 + x^2 + x + 1$ is irreducible over GF(2), but its roots are fifth roots of unity, so the period is $5$ from every nonzero state. Irreducibility is not enough.

**Non-example: a random sequence.** A sequence of $15$ fair coin flips has a periodic autocorrelation whose off-peak values spread around $0$ with a standard deviation near $\sqrt{15}$. Small values like $-1$ at every shift are what make the m-sequence useful for code acquisition: a correlator sees a peak of $N$ against a floor of exactly $-1$.

**Non-example: Barker codes.** A [Barker code](/barker-code/) has small aperiodic autocorrelation, which matters for a single radar pulse. An m-sequence is designed for the periodic case. The aperiodic autocorrelation of $1001011$ at shifts $1$ to $6$ is $(-2, -1, 2, -3, 0, 1)$, with a peak sidelobe of $3$, while the Barker code of length 7 has sidelobes of magnitude at most $1$.

## Related definitions

- [Linear feedback shift register](/linear-feedback-shift-register/) is the circuit that runs the recurrence, and [primitive polynomial](/primitive-polynomial/) is the condition for the maximal period. Those pages give the algebra; this page gives the correlation properties used in communications.
- A [de Bruijn sequence](/de-bruijn-sequence/) of order $n$ holds every $n$-tuple once, including the zero tuple. Inserting one extra zero into the run of $n - 1$ zeros of an m-sequence gives a de Bruijn sequence of length $2^n$.
- [Gold sequences](/gold-sequences/) add two m-sequences of a preferred pair, and [Kasami sequences](/kasami-sequences/) add an m-sequence and a decimation of it. Both give many sequences with low cross-correlation. One m-sequence alone has a perfect two-level autocorrelation, but different m-sequences of the same degree can have large cross-correlation.
- The [Welch bound](/welch-bound/) limits how low the correlations of a family of many sequences can be. For one $\pm 1$ sequence of odd length $N$, every correlation value is odd, so $-1$ is the smallest possible off-peak magnitude, and an m-sequence reaches it at every shift.
- [Zadoff-Chu sequences](/zadoff-chu-sequence/) are complex sequences with an off-peak periodic autocorrelation of exactly $0$, which no binary sequence of odd length can have.
- The [Hamming code](/hamming-code/) is the dual of the simplex code formed by the shifts of an m-sequence.

## References
