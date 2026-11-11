---
tag: 5N3GKG
kind: data-structure
slug: lfsr
name: Linear feedback shift register
aliases:
- LFSR
area: cryptography/symmetric-ciphers
level: core
summary: A shift register whose new bit is a fixed XOR of its state bits. In cryptography it is a fast building block, but 2L output bits reveal it by Berlekamp-Massey, so ciphers add nonlinearity.
model: word-ram
complexity:
  vars: {n: the number of output bits, L: the length of the register}
  time: {worst: Θ(n L), best: Θ(n L)}
  space: {extra: Θ(L)}
properties: {deterministic: true}
history:
  year: 1969
  people: [Solomon W. Golomb, James L. Massey, Thomas Siegenthaler]
  note: Golomb developed the theory of shift register sequences in the 1950s and 1960s. Massey (1969) showed how to find the shortest LFSR for a sequence, and Siegenthaler (1985) gave the correlation attack on LFSR combiners.
prereqs: [linear-feedback-shift-register, primitive-polynomial, stream-cipher]
see_also: [linear-feedback-shift-register, berlekamp-massey, a5-1, grain, trivium, snow-3g, gf2-polynomial-arithmetic, walsh-hadamard-transform]
sources:
  - paper: "James L. Massey, Shift-register synthesis and BCH decoding, IEEE Transactions on Information Theory 15(1), 1969, pages 122 to 127"
    locator: the synthesis algorithm (Berlekamp-Massey), Theorem 1 (the length bound N + 1 - L) and the uniqueness of the shortest LFSR from 2L bits
  - paper: "Thomas Siegenthaler, Decrypting a class of stream ciphers using ciphertext only, IEEE Transactions on Computers C-34(1), 1985, pages 81 to 85"
    locator: the correlation attack on a nonlinear combination of LFSRs, one register at a time
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Section 6.2 (LFSRs, linear complexity, the Berlekamp-Massey algorithm) and Section 6.3 (nonlinear combination and filter generators, the Geffe generator, correlation attacks)
  - book: isbn:9780521392310
    title: Rudolf Lidl and Harald Niederreiter, Finite Fields, second edition, Cambridge University Press, 1997
    locator: Chapter 8 (linear recurring sequences, minimal polynomials, periods and the order of a polynomial)
---

A linear feedback shift register (LFSR) of length $L$ is a register of $L$ bits that, at each step, outputs one bit, shifts, and feeds back a fixed XOR of its bits. With a primitive feedback polynomial it runs through all $2^L - 1$ nonzero states. This page treats the LFSR as a building block of [stream ciphers](/stream-cipher/): its linear complexity, the [Berlekamp-Massey](/berlekamp-massey/) algorithm that recovers it from $2L$ output bits, and the nonlinear combiners and filters that ciphers add, with the correlation attack on them. The general [LFSR page](/linear-feedback-shift-register/) covers its use as a non-cryptographic random number generator.

## In plain words

Think of a row of light bulbs, each on or off. At each tick, the bulb at the left end is the output. All bulbs move one place to the left, and a new bulb enters at the right. Its state is the XOR of a fixed set of bulbs. This is very cheap in hardware. With a good choice of the set, the row passes through every pattern except all off before it repeats. But the rule is linear. If an attacker sees twice as many output bits as there are bulbs, a short algorithm finds the rule and the starting pattern, and then predicts all later bits. So a cipher never outputs the bits of a single LFSR directly. It mixes several of them, or bits of one, through a nonlinear function.

## The abstract type

An LFSR of length $L$ over $\mathbb{F}_2$ is given by a *connection polynomial* $C(x) = 1 + c_1 x + \cdots + c_L x^L$ with $c_i \in \{0, 1\}$. Its output sequence $s_0, s_1, \ldots$ satisfies the linear recurrence
$$s_t = c_1 s_{t-1} \oplus c_2 s_{t-2} \oplus \cdots \oplus c_L s_{t-L} \qquad (t \ge L),$$
and the first $L$ bits are the initial state. The *characteristic polynomial* is $f(x) = x^L C(1/x) = x^L + c_1 x^{L-1} + \cdots + c_L$. If $c_L = 1$ the step is invertible. The register supports two operations: load a state, and step (output one bit).

Two measures matter in cryptography:
- **Period.** The least $T > 0$ with $s_{t+T} = s_t$ for all $t$. If $C$ (equivalently $f$) is [primitive](/primitive-polynomial/) of degree $L$, each nonzero state gives period $2^L - 1$, the maximum. Such an output is an *m-sequence*.
- **Linear complexity.** For a finite or infinite sequence $s$, $\Lambda(s)$ is the length of the shortest LFSR that generates it. An m-sequence of length $L$ has $\Lambda = L$. A random sequence of $N$ bits has $\Lambda$ close to $N/2$ (HAC, Section 6.2.2).

## Representation

**Fibonacci form.** Store $(s_t, s_{t+1}, \ldots, s_{t+L-1})$. Output $s_t$, and append $s_{t+L} = \bigoplus_i c_i s_{t+L-i}$. The XOR taps sit outside the register.

**Galois form.** Store a polynomial $a(x)$ of degree below $L$ in $\mathbb{F}_2[x]/(f)$, as an $L$-bit word. Output the coefficient of $x^{L-1}$, then set $a \leftarrow x \cdot a \bmod f$: shift left, and if the bit that falls out is 1, XOR in $f(x) - x^L$. The XOR taps sit between the cells, so one step is one shift and at most one XOR of a word.

The two forms give the same set of sequences. Each output of either form satisfies the recurrence of $f$, and when $f$ is primitive all nonzero solutions of that recurrence are shifts of one m-sequence. So, for a primitive $f$, each Galois output is a shift of each Fibonacci output. The proof is in [proofs/correctness.md](proofs/correctness.md).

## Operations

```pseudo id=main
FIBONACCI-STEP(s, C)                       ▷ s = (s[0], ..., s[L−1]); s[0] is the oldest bit
L1  out ← s[0]
L2  new ← c1·s[L−1] ⊕ c2·s[L−2] ⊕ ... ⊕ cL·s[0]
L3  s ← (s[1], ..., s[L−1], new)
L4  return out

GALOIS-STEP(a, f)                          ▷ a is an L-bit word, a polynomial mod f
L5  out ← bit L−1 of a
L6  a ← (a shifted left by 1) with bit L dropped
L7  if out = 1 then a ← a ⊕ (f − x^L)
L8  return out

BERLEKAMP-MASSEY(s0, ..., s(N−1))          ▷ Massey (1969)
L9  C ← 1, B ← 1, L ← 0, m ← 1
L10 for n ← 0 to N − 1 do
L11     d ← s_n ⊕ c1·s(n−1) ⊕ ... ⊕ cL·s(n−L)          ▷ the discrepancy
L12     if d = 0 then m ← m + 1
L13     else if 2L ≤ n then T ← C; C ← C + x^m·B; L ← n + 1 − L; B ← T; m ← 1
L14     else C ← C + x^m·B; m ← m + 1
L15 return (L, C)
```

BERLEKAMP-MASSEY keeps $C$, the shortest LFSR that generates the bits seen so far, and $B$, the value of $C$ before the last length change. When $C$ predicts the next bit wrongly ($d = 1$), adding $x^m B$ fixes the prediction at $n$ without breaking it at earlier positions. Line L13 raises the length only when the bound of Massey's Theorem 1 forces it.

The code on this page is for study only. It is not constant time, an LFSR alone is not a cipher, and the code must not protect real data. Use a vetted cipher from libsodium or a FIPS 140 validated module.

### Nonlinear combiners and filters

- **Combination generator.** Run $k$ LFSRs in parallel and output $z_t = F(x^{(1)}_t, \ldots, x^{(k)}_t)$ for a Boolean function $F$.
- **Filter generator.** Run one LFSR and output $z_t = F$ of several of its state bits.
- **Clock control.** Let one register decide when the others step, as in [A5/1](/a5-1/).
- **Nonlinear feedback.** Add an NFSR whose feedback is nonlinear, as in [Grain](/grain/) and [Trivium](/trivium/).

The **Geffe generator** combines three LFSRs with $z = x_1 x_2 \oplus \bar{x}_1 x_3$: it outputs $x_2$ when $x_1 = 1$ and $x_3$ when $x_1 = 0$. For independent uniform bits, $\Pr[z = x_2] = \Pr[x_1 = 1] + \Pr[x_1 = 0]\Pr[x_3 = x_2] = 1/2 + 1/4 = 3/4$, and likewise $\Pr[z = x_3] = 3/4$. **Siegenthaler's correlation attack** (1985) uses this: try each of the $2^{L_2} - 1$ initial states of register 2, generate its output, and keep the state whose output agrees with $z$ in about 75 percent of positions; a wrong state agrees in about 50 percent. Do the same for register 3, then search register 1. The cost is about $2^{L_1} + 2^{L_2} + 2^{L_3}$ trials instead of $2^{L_1 + L_2 + L_3}$.

## Example

Take $C(x) = 1 + x + x^4$ (primitive), so $s_t = s_{t-1} \oplus s_{t-4}$, and the state $1, 0, 0, 0$. The Fibonacci form outputs one full period of 15 bits:

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $s_t$ | 1 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 1 | 0 | 1 | 1 | 0 | 0 |

For example $s_4 = s_3 \oplus s_0 = 0 \oplus 1 = 1$ and $s_8 = s_7 \oplus s_4 = 1 \oplus 1 = 0$. The Galois form with $f = x^4 + x^3 + 1$, started at $a(x) = 1$, outputs 0 0 0 1 1 1 1 0 1 0 1 1 0 0, which is the same sequence from $t = 1$.

BERLEKAMP-MASSEY on the first 8 bits, 1 0 0 0 1 1 1 1:

| $n$ | $s_n$ | $d$ | $L$ after | $C(x)$ after |
|---|---|---|---|---|
| 0 | 1 | 1 | 1 | $1 + x$ |
| 1 | 0 | 1 | 1 | $1$ |
| 2 | 0 | 0 | 1 | $1$ |
| 3 | 0 | 0 | 1 | $1$ |
| 4 | 1 | 1 | 4 | $1 + x^4$ |
| 5 | 1 | 1 | 4 | $1 + x + x^4$ |
| 6 | 1 | 0 | 4 | $1 + x + x^4$ |
| 7 | 1 | 0 | 4 | $1 + x + x^4$ |

It finds $L = 4$ and $C = 1 + x + x^4$ from $2L = 8$ bits.

A toy Geffe attack: registers of lengths 7, 8 and 9 with primitive polynomials $1 + x + x^7$, $1 + x^2 + x^3 + x^4 + x^8$ and $1 + x^4 + x^9$, a 24-bit key, and 200 output bits. For register 2 the right state agrees with $z$ in 148 of 200 positions, and the best wrong state in 119. For register 3 the counts are 151 and 119. The right state of register 1 agrees in exactly 100 positions, so the attack cannot find it by correlation; with registers 2 and 3 known, a search of its 127 states finds it. The attack takes $127 + 255 + 511$ trials instead of about $2^{24}$.

## Correctness

The Fibonacci step appends the bit that the recurrence demands, so its output satisfies the recurrence by construction. The Galois output is $\ell(x^t a_0 \bmod f)$ for a fixed linear map $\ell$, and $f(x) \equiv 0$ in $\mathbb{F}_2[x]/(f)$ gives the same recurrence. If $f$ is primitive, $\mathbb{F}_2[x]/(f)$ is the field $\mathbb{F}_{2^L}$ and $x$ has order $2^L - 1$, so the period of each nonzero sequence is $2^L - 1$. For Berlekamp-Massey, Massey's Theorem 1 says that if an LFSR of length $L$ generates $s_0 \ldots s_{N-1}$ but not $s_0 \ldots s_N$, then each LFSR that generates $s_0 \ldots s_N$ has length at least $N + 1 - L$. It follows that $2L$ bits of an LFSR sequence of length $L$ fix the rest of the sequence. The proofs are in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- FIBONACCI-STEP costs $\Theta(L)$ bit operations as written, or $\Theta(1)$ word operations when the state is a machine word and the taps are a mask (a parity of a masked word). GALOIS-STEP costs one shift and at most one XOR of an $L$-bit word.
- $n$ output bits cost $\Theta(n L)$ bit operations, or $\Theta(n)$ word operations when $L$ fits in a word.
- BERLEKAMP-MASSEY on $N$ bits costs $\Theta(N^2)$ bit operations: line L11 sums up to $L \le N$ terms, and lines L13 and L14 add polynomials of degree at most $N$.
- The correlation attack on $k$ registers with $N$ output bits costs $\Theta\bigl(N \sum_i 2^{L_i}\bigr)$ steps, against $\Theta(2^{\sum_i L_i})$ for a key search.

## Variants

- **Word-oriented LFSRs.** The registers of [SNOW 3G](/snow-3g/) hold 32-bit words over $\mathbb{F}_{2^{32}}$, and the register of [ZUC](/zuc/) holds 31-bit words over the prime field of $2^{31} - 1$. One step makes a whole word.
- **NFSRs.** A nonlinear feedback shift register resists Berlekamp-Massey. [Grain](/grain/) pairs an LFSR (which guarantees the period) with an NFSR, and [Trivium](/trivium/) uses three short registers with quadratic feedback.
- **Correlation immune functions.** Siegenthaler (1984) defined $m$th-order correlation immunity: $F$ is uncorrelated with each set of $m$ inputs. He also showed a trade-off with the algebraic degree. The [Walsh-Hadamard transform](/walsh-hadamard-transform/) measures the correlations.
- **Fast correlation attacks.** Meier and Staffelbach (1988, 1989) used the low-weight multiples of the feedback polynomial to correct the noisy output without trying all states.
- **Algebraic attacks.** Courtois and Meier (2003) wrote the output as low-degree equations in the initial state and solved them by linearization.

## When to use it

Use an LFSR when you need a long, balanced, cheap bit sequence: scrambling, spread spectrum, built-in self test of hardware, CRCs, and as the linear part of a stream cipher. Do not use an LFSR, or a linear combination of LFSRs, as a keystream generator on its own: $2\Lambda$ bits reveal it. In a cipher, combine it with a nonlinear part and check the design against correlation, fast correlation and algebraic attacks.

## Pitfalls

- **The all-zero state.** Line L2 maps the zero state to itself, so the output is all zeros. A cipher must never load it; the key and IV loading of real designs puts fixed ones into the state for this reason.
- **A non-primitive polynomial.** With $C = 1 + x^2 + x^4 = (1 + x + x^2)^2$, the state 1 0 0 0 has period 6, not 15. The period then depends on the start state.
- **Mixing the two polynomial conventions.** The taps of line L2 come from $C(x)$, and the reduction of line L7 uses $f(x) = x^L C(1/x)$, the reciprocal. Using $C$ in line L7 gives the reversed recurrence; for a primitive $C$ it still has the maximum period, but the output does not match a reference.
- **Too few bits for Berlekamp-Massey.** With fewer than $2\Lambda$ bits, line L15 returns a shorter LFSR that fits the bits seen but predicts wrong bits later.
- **A combiner with correlation.** A Geffe-style function that agrees with one input more often than half the time lets the correlation attack split the key search into one search per register.

## Implementations

## History

Golomb developed the theory of maximal-length shift register sequences in the 1950s and 1960s, for radar and communications. Berlekamp gave an algorithm for decoding BCH codes in 1968, and Massey showed in 1969 that it finds the shortest LFSR that generates a given sequence; the algorithm now has both names. Through the 1970s and 1980s many stream ciphers combined LFSRs with nonlinear functions. Siegenthaler defined correlation immunity in 1984 and gave the divide and conquer correlation attack in 1985. Later designs such as A5/1, E0, SNOW 3G, Grain and Trivium keep the LFSR for its speed and period and add clock control, nonlinear registers or a finite state machine.

## References
