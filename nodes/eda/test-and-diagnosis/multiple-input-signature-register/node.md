---
tag: CM81DK
kind: data-structure
slug: multiple-input-signature-register
name: Multiple-input signature register
aliases:
- MISR
- signature register
area: eda/test-and-diagnosis
level: core
summary: An LFSR that XORs several circuit outputs into its stages every clock, compressing a long response stream into one signature compared at the end of BIST.
model: word-ram
complexity:
  vars: {m: the number of input words, k: the number of stages, w: the word size in bits}
  time: {worst: "O(m (k / w + 1))", average: "O(m (k / w + 1))", best: "O(m (k / w + 1))"}
  space: {extra: "O(k / w + 1)"}
properties: {deterministic: true, recursive: false}
history:
  year: 1979
  people: [B. Könemann, J. Mucha, G. Zwiehoff]
  note: The BILBO register of Könemann, Mucha and Zwiehoff (1979) has a mode in which it compacts many circuit outputs into one signature, the multiple-input signature register.
prereqs: [linear-feedback-shift-register, gf2-polynomial-arithmetic, built-in-self-test]
see_also: [signature-aliasing-probability, cyclic-redundancy-check, x-compact, lfsr-reseeding, embedded-deterministic-test, fault-dictionary, scan-design, irreducible-polynomial]
sources:
  - paper: "B. Könemann, J. Mucha and G. Zwiehoff, Built-in logic block observation techniques, Digest of Papers, 1979 Test Conference, 37 to 41, 1979"
    title: B. Könemann, J. Mucha and G. Zwiehoff, Built-in logic block observation techniques, Digest of Papers, 1979 Test Conference, 37 to 41, 1979
    locator: the BILBO register and its signature mode with one input per stage
  - book: isbn:9780471624639
    title: Paul H. Bardell, William H. McAnney and Jacob Savir, Built-In Test for VLSI, Pseudorandom Techniques, Wiley-Interscience, 1987
    locator: the chapters Test Response Compression Techniques and Shift-Register Polynomial Division (the multiple-input register as polynomial division)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter Compression Techniques (signature analysis and parallel signature analysis)
  - paper: doi:10.1109/TC.1980.1675610
    title: J. E. Smith, Measures of the effectiveness of fault signature analysis, IEEE Transactions on Computers C-29(6), 510 to 514, 1980
    locator: the count of aliasing error streams when all of them are equally likely
---

A multiple-input signature register, or MISR, is a [linear feedback shift register](/linear-feedback-shift-register/) with $k$ stages and one extra XOR at the input of every stage, so that it takes a $k$-bit word from the circuit under test at each clock. Read as a polynomial over GF(2), one clock computes $r \leftarrow (x\,r + w) \bmod q$ for a feedback polynomial $q$ of degree $k$, so after a whole test the register holds the remainder of one long polynomial, built from all $k$ input streams, divided by $q$. It is the usual response compactor of [built-in self-test](/built-in-self-test/) and of scan compression. This page is about the register as a data structure: its state, its operations, why the signature is a remainder, and which errors it can and cannot lose. How often a random error is lost is on the page [signature aliasing probability](/signature-aliasing-probability/).

## In plain words

A test produces millions of output bits. Storing all of them and the right answers is costly. A signature register keeps only a short summary.

It is a row of a few flip-flops. At every clock, each flip-flop takes the bit from its neighbor, mixes in one output bit of the circuit, and, when the last flip-flop holds a 1, also mixes in a fixed feedback pattern. After the test, the row holds a short code, the signature, and the chip compares it with the code of a good chip.

The code works like the remainder of a long division. A single wrong bit always changes it. But some patterns of several wrong bits leave it unchanged, and then a bad chip passes.

## The abstract type

The type has two fixed parameters and one value.

- The number of stages $k \ge 1$, and the feedback polynomial $q(x) = x^k + q_{k-1} x^{k-1} + \cdots + q_1 x + q_0$ over GF(2), of degree exactly $k$.
- The value is a register $r = (r_0, \ldots, r_{k-1})$ of $k$ bits, read as the polynomial $r(x) = r_0 + r_1 x + \cdots + r_{k-1} x^{k-1}$ of degree less than $k$. An input word $w = (w_0, \ldots, w_{k-1})$ is read the same way.

The operations are:

- `RESET(s)`: set $r$ to the seed $s$, usually 0.
- `CLOCK(w)`: one clock with the input word $w$.
- `SIGNATURE()`: return $r$.

The specification is the formula of the signature. After `RESET(s)` and the clocks `CLOCK(w_0)`, ..., `CLOCK(w_{m-1})`,

$$\mathrm{SIGNATURE}() = \Big( x^m s(x) + \sum_{t=0}^{m-1} x^{m-1-t}\, w_t(x) \Big) \bmod q(x).$$

There is a second way to read the same sum. Write the stream of input $i$ as the polynomial $W_i(x) = \sum_t w_{t,i}\, x^{m-1-t}$, where $w_{t,i}$ is bit $i$ of word $t$, so the first bit has the highest power, as in long division. Then $\sum_t x^{m-1-t} w_t(x) = \sum_i x^i W_i(x)$. A MISR is a single-input signature register fed with the XOR of the $k$ input streams, stream $i$ shifted up by $i$ places. This one line explains both the strength and the weakness of the register, below.

## Representation

The register is one $k$-bit word, with bit $i$ for stage $r_i$, and the low part $q - x^k$ of the polynomial is a second $k$-bit constant. This is the internal-XOR form, also called the Galois form, of an LFSR: stage 0 takes $q_0 r_{k-1} \oplus w_0$, and stage $i \ge 1$ takes $r_{i-1} \oplus q_i r_{k-1} \oplus w_i$. In hardware it is $k$ flip-flops, one XOR per input, and one XOR per nonzero coefficient $q_i$ with $1 \le i \le k-1$. All stages change on the same clock, so the register takes one word per clock at the full clock rate.

## Operations

```pseudo id=main
CLOCK(r, w)
L1  msb ← bit k − 1 of r
L2  r ← r shifted one place toward stage k − 1, bit k − 1 dropped and stage 0 set to 0
L3  if msb = 1 then r ← r XOR (q − x^k)
L4  r ← r XOR w
```

`RESET(s)` stores $s$ in $r$ and `SIGNATURE()` returns $r$, each in one word operation.

Lines L1 to L3 compute $x\,r(x) \bmod q(x)$. The shift multiplies by $x$. If the top stage was 0, then $x\,r$ has degree less than $k$ and is already reduced. If it was 1, then $x\,r = x^k + (\text{the shifted bits})$, and $x^k \equiv q(x) - x^k \pmod q$, since over GF(2) minus is plus, so line L3 adds the low part of $q$. Line L4 adds the input word. So one clock is

$$r \leftarrow (x\,r + w) \bmod q.$$

This is one step of long division of a polynomial by $q$, in the same way as the single-input register on the [built-in self-test](/built-in-self-test/) page and the [cyclic redundancy check](/cyclic-redundancy-check/), except that $k$ new bits enter at once.

## Example

Take $k = 3$ and $q = x^3 + x + 1$, so $q - x^3 = x + 1$, the word 011. Start from $r = 000$ and clock five words. Words and registers are written $r_2 r_1 r_0$, high stage first.

| clock $t$ | $r$ before | msb | after L2 | after L3 | $w_t$ | after L4 |
|---|---|---|---|---|---|---|
| 0 | 000 | 0 | 000 | 000 | 101 | 101 |
| 1 | 101 | 1 | 010 | 001 | 011 | 010 |
| 2 | 010 | 0 | 100 | 100 | 110 | 010 |
| 3 | 010 | 0 | 100 | 100 | 001 | 101 |
| 4 | 101 | 1 | 010 | 001 | 100 | 101 |

The signature is 101, the polynomial $x^2 + 1$. The formula gives the same value. The words are $w_0 = x^2 + 1$, $w_1 = x + 1$, $w_2 = x^2 + x$, $w_3 = 1$ and $w_4 = x^2$, so

$$x^4 w_0 + x^3 w_1 + x^2 w_2 + x\,w_3 + w_4 = x^6 + x^4 + x^2 + x.$$

Modulo $q$, $x^3 = x + 1$, $x^4 = x^2 + x$ and $x^6 = (x + 1)^2 = x^2 + 1$, and the sum reduces to $x^2 + 1$.

Now put errors on the stream. An error on input 0 at clock 3, so that $w_3 = 000$, adds $x^{4-3} \cdot x^0 = x$ to the polynomial, and the signature becomes $101 \oplus 010 = 111$. The error is caught. Two errors, one on input 0 at clock 1 and one on input 1 at clock 2, add $x^{3} \cdot x^0$ and $x^{2} \cdot x^1$, the same monomial $x^3$ twice. They cancel, and the signature stays 101, although two bits of the stream are wrong. The second error reaches stage 1 at the clock when the first error, shifted up from stage 0, is also there.

## Correctness

Facts 1 and 2 hold for every $q$ of degree $k$, and fact 3 needs $q_0 = 1$. They are proved on the [proof page](proofs/correctness.md).

1. **The signature is a remainder.** After $m$ clocks from the seed $s$, the register holds $\big(x^m s + \sum_t x^{m-1-t} w_t\big) \bmod q$. The proof is by induction on the clocks, with the step $r \leftarrow (x\,r + w) \bmod q$.
2. **Linearity, and the error polynomial.** If the good circuit gives the words $w_t$ and a faulty one gives $w_t \oplus e_t$, then the two signatures differ by $E \bmod q$, where $E(x) = \sum_t x^{m-1-t} e_t(x) = \sum_t \sum_i e_{t,i}\, x^{m-1-t+i}$. The faulty chip passes exactly when $q$ divides $E$. The seed drops out.
3. **A single wrong bit never aliases.** A single wrong bit gives $E = x^j$. Since $q_0 = 1$, $q$ is not a power of $x$, and the only irreducible factor of $x^j$ is $x$, so $q$ does not divide $x^j$.

Fact 2 also says which pairs of errors alias. The error bit $(t, i)$, at clock $t$ on input $i$, gives the monomial $x^{m-1-t+i}$, so the two error bits $(t, i)$ and $(t + 1, i + 1)$ give the same monomial and always cancel, whatever $q$ is. Two error bits with different exponents $a > b$ alias exactly when $q$ divides $x^b (x^{a-b} + 1)$, that is when $q$ divides $x^{a-b} + 1$. For a primitive $q$ this happens exactly when $2^k - 1$ divides $a - b$, since $2^k - 1$ is then the least $n \ge 1$ for which $q$ divides $x^n + 1$.

## Complexity

For $k \le w$, the word size, each operation is $O(1)$ word operations, so a stream of $m$ words costs $O(m)$ time. For larger $k$, a clock touches $\lceil k / w \rceil$ words. The extra space is the register itself. In hardware, one clock is one word, so the register keeps up with the circuit at full speed, and the area is $k$ flip-flops and $O(k)$ XOR gates. The signature is $k$ bits however long the test is.

## Variants

- **Single-input register.** With $k$ circuit outputs and a one-bit input, first XOR the outputs into one bit, then divide. A MISR saves this XOR tree and keeps more information, since the outputs enter at different stages.
- **External-XOR form.** The feedback can also be taken as one XOR of tapped stages into stage 0, the Fibonacci form of the LFSR, with the input words still XORed into every stage. The map from streams to signatures is again linear and onto, so the count of aliasing streams is the same, but the set of aliasing streams is a different one, and the signature is not the plain remainder of fact 1.
- **Space compactor first.** With hundreds of scan chains and a 32-bit or 64-bit MISR, an XOR network first reduces the chain outputs to the width of the register. The [X-compact](/x-compact/) network is one with proved properties when some outputs are unknown.
- **Masking.** A mask register forces chosen chain outputs to 0 on chosen clocks, so that unknown values do not enter the register.
- **Several signatures.** Reading the signature after every pattern or every block, instead of once at the end, shortens the stream that one aliasing event can hide and gives data for diagnosis.
- **BILBO.** The register of Könemann, Mucha and Zwiehoff works as a normal register, a scan register, a pattern generator with the inputs held at 0, or a MISR.

## When to use it

Use a MISR whenever a long response must be checked on the chip or carried out through few pins: the output side of [built-in self-test](/built-in-self-test/), the output side of scan compression such as [embedded deterministic test](/embedded-deterministic-test/), and checks of memory contents. The pattern side of these schemes uses the same register with the inputs off, as in [LFSR reseeding](/lfsr-reseeding/). Do not use it when every response bit is needed, for example for diagnosis with a [fault dictionary](/fault-dictionary/), unless the signature is read often or the test is run again with the register bypassed.

## Pitfalls

- **Unknown values.** One unknown bit $X$ on an input makes every later state of the register unknown, since the next state depends on it linearly and nothing removes it. Block or mask every source of $X$ before the register.
- **Errors in neighbor stages.** Fact 2 shows that an error on input $i$ at clock $t$ and one on input $i + 1$ at clock $t + 1$ cancel. A fault that drives two neighbor scan chains in this pattern aliases for every polynomial. Do not connect outputs that share logic to neighbor stages, or use a space compactor that mixes them first.
- **A polynomial without the term 1.** If $q_0 = 0$, then $x$ divides $q$, the step $r \mapsto x\,r \bmod q$ is not one to one, and the register forgets part of its past. For $q = x^3$ it is a plain shift register, and an error on input 2 at clock 0 is gone after one more clock. For $q = x^3 + x^2 = x^2 (x + 1)$, two wrong bits on input 2 at any two neighbor clocks give $E = x^b (x + 1)$ with $b \ge 2$, a multiple of $q$, and alias.
- **The good signature depends on everything.** The seed, the number of clocks, the order of the inputs and every bit of the good response enter the signature. A change in any of them needs a new good signature from simulation.
- **One signature hides where the error was.** Pass or fail is all that a final signature tells. Diagnosis needs the failing clocks, which means reading the register more often or running the test again in a mode that bypasses it.

## Implementations

## History

The BILBO register of Könemann, Mucha and Zwiehoff (1979) put a signature mode with one input per stage into the registers of the circuit itself, and this is the multiple-input signature register of logic BIST. The description as polynomial division over GF(2), and the count of aliasing error streams under the model in which all of them are equally likely, are in Smith (1980) and in the book of Bardell, McAnney and Savir (1987).

## References
