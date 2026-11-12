---
tag: PD1H78
kind: algorithm
slug: majority-logic-decoding
name: Majority-logic decoding
aliases:
- Reed decoding algorithm
- Reed majority-logic decoder
- one-step majority-logic decoding
- threshold decoding of block codes
area: compression-and-coding/error-correcting-codes
level: advanced
summary: "Decode each symbol, or each coefficient of a Reed-Muller code, by a majority vote over parity checks that share only that symbol. It corrects up to half the number of checks."
model: word-ram
complexity:
  vars: {n: "the code length, 2^m for RM(r, m)", k: "the dimension of RM(r, m)", m: the number of variables, r: the order of the code}
  time: {worst: Θ(n k)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1954
  people: [Irving S. Reed, James L. Massey]
  note: Reed decoded the Reed-Muller codes by majority votes in 1954. Massey named one-step and multi-step majority-logic decoding, and the threshold decoding of convolutional codes, in his 1963 book.
prereqs: [reed-muller-code, parity-check-matrix]
see_also: [syndrome-decoding, hadamard-code, bit-flipping-decoding, ldpc-code, convolutional-code, bch-code, cyclic-code, maximum-likelihood-decoding]
sources:
  - paper: doi:10.1109/TIT.1954.1057465
    title: I. S. Reed, A class of multiple-error-correcting codes and the decoding scheme, Transactions of the IRE Professional Group on Information Theory 4(4), 1954
    locator: pp. 38 to 49 (the decoder that finds the coefficients of the highest degree first by majority votes)
  - paper: "J. L. Massey, Threshold Decoding, MIT Press, Cambridge, Massachusetts, 1963"
    title: Threshold Decoding
    locator: Chapters 1 and 2 (orthogonal parity checks, one-step and L-step majority decoding, and the bound of floor(J/2) errors)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 4.3 (Reed's decoding of RM codes) and Chapter 8 (one-step and multi-step majority-logic decoding of cyclic codes, with the (15, 7) example)
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 13, Section 7 (majority-logic decoding of Reed-Muller codes)
---

Majority-logic decoding decides each unknown, a code symbol or a coefficient of the message, by a vote among parity checks that all contain that unknown and share nothing else. If there are $J$ such checks, $t \le \lfloor J/2 \rfloor$ errors spoil at most $t$ of them, and the majority is still right. Reed used this idea in 1954 to decode the [Reed-Muller code](/reed-muller-code/) $\mathrm{RM}(r, m)$ up to half its minimum distance. He found the coefficients of the top degree first, then removed them and repeated. Massey (1963) named one-step and multi-step majority-logic decoding and applied them to [cyclic codes](/cyclic-code/) and convolutional codes. The decoder needs only XOR gates and majority gates, so it is fast and simple in hardware.

## In plain words

Suppose you want to know one hidden bit. You have several independent ways to compute it from the received word, and no two of these ways read the same received symbol, except the hidden one itself. One wrong symbol can spoil at most one of these ways. So if fewer than half of the symbols they read are wrong, most of the ways still give the right answer, and a vote finds it.

For a Reed-Muller code, the hidden bits are the coefficients of a polynomial. The decoder votes on the coefficients of the most complex terms first. Then it removes those terms from the received word, so that the next votes see a simpler polynomial with the same errors. It goes down level by level until it has every coefficient.

## The problem

**Code.** $\mathrm{RM}(r, m)$ is the set of value tables of Boolean polynomials $f = \sum_{|S| \le r} a_S x_S$ in $x_1, \dots, x_m$, where $x_S = \prod_{i \in S} x_i$. The table lists $f(p)$ at all $n = 2^m$ points $p \in \mathrm{GF}(2)^m$. The code has dimension $k = \sum_{i \le r} \binom{m}{i}$ and minimum distance $2^{m - r}$.

**Channel.** A codeword is sent over a binary channel with hard decisions, for example the [binary symmetric channel](/binary-symmetric-channel/). The receiver gets $y = f + e$.

**Task.** Given $y$, return the coefficients $a_S$, correctly whenever $\mathrm{wt}(e) \le t = 2^{m - r - 1} - 1$, which is $\lfloor (d - 1)/2 \rfloor$ for $d = 2^{m - r}$.

**Check sums.** For $S$ with $|S| = \ell$, let $V_S$ be the subspace spanned by the unit vectors $e_i$ with $i \in S$. Its $2^{m - \ell}$ cosets $b + V_S$ are disjoint and cover all points. The check sum of $y$ on a coset $P$ is $y(P) = \sum_{p \in P} y_p$. If $y$ is the table of a polynomial of degree at most $\ell$, every one of these sums equals the coefficient $a_S$.

## The algorithm

```pseudo id=main
REED-DECODE(y, r, m)              ▷ y is a received word of RM(r, m), n = 2^m
L1  f ← ∅                          ▷ the monomials found so far
L2  for ℓ ← r down to 0 do
L3      for each S ⊆ {1, …, m} with |S| = ℓ do
L4          ones ← 0
L5          for each coset P of V_S do                ▷ 2^(m − ℓ) disjoint cosets
L6              ones ← ones + y(P)                    ▷ the check sum, 0 or 1
L7          if ones > 2^(m − ℓ − 1) then a_S ← 1 else a_S ← 0
L8      y ← y + Σ_{|S| = ℓ, a_S = 1} table(x_S)        ▷ remove the degree ℓ part
L9      f ← f ∪ {S : |S| = ℓ, a_S = 1}
L10 return f
```

Line L7 takes the majority of the $2^{m - \ell}$ check sums for $a_S$, with a tie read as 0. Line L8 removes the decoded part of degree $\ell$ after all votes of that degree. Then the rest of $y$ is a polynomial of degree at most $\ell - 1$ plus the same error. For $\ell = 0$ the cosets are single points, and line L7 is a majority vote over all $n$ received bits for the constant term.

The implementation stores a point $p$ as an integer whose bit $i$ is $x_{i+1}$. The coset of $V_S$ with base $b$ is the set $b \mid \mathit{sub}$ for every submask $\mathit{sub}$ of the mask of $S$, and the bases are the points with all bits of $S$ equal to 0.

## Example

Take $\mathrm{RM}(1, 3)$, the $[8, 4, 4]$ code, with $t = 2^{3 - 1 - 1} - 1 = 1$. Points are $p = 0, \dots, 7$, with $x_1, x_2, x_3$ the bits 0, 1, 2 of $p$. Send $f = 1 + x_1 + x_2$, whose table is $10011001$. An error at position 6 gives

$$y = 10011011 \quad (y_0, \dots, y_7).$$

**Degree 1 (line L2 with $\ell = 1$).** For each variable there are 4 cosets of size 2.

| $S$ | cosets | check sums | ones | $a_S$ |
|---|---|---|---|---|
| $\{1\}$ | $\{0,1\}, \{2,3\}, \{4,5\}, \{6,7\}$ | 1, 1, 1, 0 | 3 | 1 |
| $\{2\}$ | $\{0,2\}, \{1,3\}, \{4,6\}, \{5,7\}$ | 1, 1, 0, 1 | 3 | 1 |
| $\{3\}$ | $\{0,4\}, \{1,5\}, \{2,6\}, \{3,7\}$ | 0, 0, 1, 0 | 1 | 0 |

In each row the error at position 6 spoils exactly the one check sum whose coset contains 6, and the other three agree. Line L8 adds the tables of $x_1$ and $x_2$: $10011011 + 01010101 + 00110011 = 11111101$.

**Degree 0.** The cosets are the 8 single points. Seven of the bits are 1, so $a_\emptyset = 1$. Line L10 returns $\{\emptyset, \{1\}, \{2\}\}$, which is $f = 1 + x_1 + x_2$.

**One-step decoding of a cyclic code.** The $(15, 7, 5)$ BCH code with $g(x) = 1 + x^4 + x^6 + x^7 + x^8$ has $J = 4$ dual codewords that contain position 14 and share no other position. The implementation finds them by search from the dual code:

$$\{0, 2, 6, 14\}, \quad \{7, 8, 10, 14\}, \quad \{3, 11, 12, 14\}, \quad \{1, 5, 13, 14\}.$$

The decoder flips bit 14 when 3 or 4 of these checks fail, and does the same for each other position with the checks shifted cyclically. It corrects $\lfloor 4/2 \rfloor = 2$ errors, the full power of a code with $d = 5$. The tests check all 121 patterns of at most 2 errors on 4 codewords.

## Correctness

The full proof is in the proofs file. The key facts:

- **Each check sum reads the coefficient.** If $g$ has degree at most $\ell$ and $|S| = \ell$, then $g(b + V_S) = a_S$ for every coset. A monomial $x_T$ with $T \ne S$ and $|T| \le \ell$ sums to an even number over the coset, and $x_S$ sums to 1.
- **The check sums are orthogonal.** The cosets of $V_S$ are disjoint, so one error changes exactly one of the $2^{m - \ell}$ sums. With at most $t = 2^{m - r - 1} - 1 \le 2^{m - \ell - 1} - 1$ errors, fewer than half of the sums are wrong, and line L7 decides $a_S$ correctly.
- **The peeling keeps the error the same.** After line L8, $y$ is the table of the part of $f$ of degree less than $\ell$ plus the same error $e$. So the next level sees the same situation with $\ell - 1$.
- **The radius is tight.** A word equal to 1 on half of the support of $x_1 \cdots x_r$ is at distance $2^{m - r - 1}$ from both $0$ and that minimum weight codeword. No decoder can correct both of these patterns of $t + 1$ errors.

The tests check every pattern of at most $t$ errors for $\mathrm{RM}(r, m)$ with $(r, m)$ in $(0, 2)$, $(0, 3)$, $(1, 3)$, $(0, 4)$, $(1, 4)$, $(2, 4)$, $(2, 5)$, $(3, 5)$ and $(4, 6)$, and random patterns of exactly $t$ errors for lengths up to 128.

## Complexity

**Time.** For one monomial $x_S$, lines L5 and L6 read each of the $n$ positions once, in $2^{m - \ell}$ check sums of $2^\ell$ bits. There are $k$ monomials in total, so the votes cost $\Theta(n k)$ bit operations. Line L8 adds at most one table of length $n$ per monomial, also $O(n k)$. So the decoder runs in $\Theta(n k)$ time. For the first order code $\mathrm{RM}(1, m)$ this is $\Theta(n \log n)$, the same order as the fast Walsh-Hadamard transform decoder.

**Space.** One working copy of $y$ and the list of found monomials: $\Theta(n)$ bits.

**Hardware.** All votes of one degree are independent, so a circuit decodes in $r + 1$ levels of XOR trees and majority gates. This short, fixed depth is the main reason to use majority logic.

## Properties

- **Bounded distance.** The decoder corrects every pattern of up to $2^{m - r - 1} - 1$ errors. Beyond that it may return a wrong codeword, and it gives no warning.
- **Not maximum likelihood.** It often corrects many patterns of more than $t$ errors, but it is not a nearest codeword decoder in general, and it ignores soft information unless the votes are weighted.
- **Deterministic and parallel.** The votes of one degree do not depend on each other.
- **Multi-step.** In Massey's terms, Reed's decoder is an $(r + 1)$-step decoder: each step uses the results of the steps before it.

## Variants and improvements

- **One-step majority-logic decoding.** For a [cyclic code](/cyclic-code/), find $J$ checks orthogonal on the last position, that is, dual codewords that contain it and share no other position. A vote of these checks decides that position, and cyclic shifts give all other positions. It corrects $\lfloor J/2 \rfloor$ errors. Difference-set codes and some [BCH codes](/bch-code/), such as the $(15, 7, 5)$ code above, reach their full error correcting power this way.
- **L-step decoding.** When no $J$ checks are orthogonal on one position, checks orthogonal on a set of positions give the sum of that set by a vote. Further votes reduce the sets until one position remains. Reed's decoder is a case of this method.
- **Finite geometry codes.** Euclidean and projective geometry codes are built so that their duals contain many orthogonal checks. They are the main family of codes designed for majority-logic decoding.
- **Weighted votes.** With soft inputs, each check gets a weight from the reliability of its symbols, as in Massey's a posteriori probability threshold decoding.
- **Iterative bit flipping.** Gallager's decoder for [LDPC codes](/ldpc-code/) repeats votes of sparse checks and flips the bits that most checks blame. See [bit-flipping decoding](/bit-flipping-decoding/).
- **Threshold decoding of convolutional codes.** Massey used the same orthogonal checks on the syndrome of a [convolutional code](/convolutional-code/), decoding one information bit per time step.

## When to use it

Use majority-logic decoding when the code has many orthogonal checks and the decoder must be very fast, small or simple: Reed-Muller codes, difference-set and finite geometry codes, and some memory and storage systems. Use it also as a short reference decoder for Reed-Muller codes in tests. Do not use it when soft information is available and every fraction of a decibel matters. Then soft decoders such as the Walsh-Hadamard transform decoder for $\mathrm{RM}(1, m)$, recursive list decoders for longer RM codes, or belief propagation for LDPC codes do better. For codes with few orthogonal checks, such as most long BCH codes, one-step majority logic corrects far fewer errors than the code allows, and an algebraic decoder is better.

## Pitfalls

- **Bottom up order.** Voting on the constant term first does not work. The check sums for $x_S$ read $a_S$ only when the remaining polynomial has degree at most $|S|$, so line L2 must go from degree $r$ down.
- **The wrong subspace.** The check sums for $x_S$ are sums over the cosets of $V_S$, the subspace in the directions of $S$. The complementary subspace has $2^{|S|}$ cosets of size $2^{m - |S|}$, and sums over them do not give $a_S$.
- **Ties.** With an even number of checks, $t + 1$ errors can make a tie. The rule at line L7 must be fixed, and a tie must not be counted as a correct decision in error rate estimates.
- **Checks that are not orthogonal.** If two checks share a second position besides the one being decided, a single error at that position spoils both, and $\lfloor J/2 \rfloor$ errors are no longer guaranteed. The tests verify orthogonality of the checks that the search returns.
- **Output not a codeword.** A one-step decoder decides each position separately. With more than $\lfloor J/2 \rfloor$ errors its output need not be a codeword, so a final syndrome check is needed to detect such failures.

## Implementations

## History

Reed's 1954 paper gave the polynomial view of the codes that Muller had found the same year, and with it the decoder that votes on the highest degree coefficients first. It was among the first practical decoders for codes that correct more than one error. Massey's 1963 book Threshold Decoding defined orthogonal parity checks, one-step and L-step majority-logic decoding, and their use for convolutional codes. In the following years Rudolph, Weldon, Kasami, Lin and others built finite geometry and difference-set codes for these decoders, and Lin and Costello give a full chapter to them.

## References
