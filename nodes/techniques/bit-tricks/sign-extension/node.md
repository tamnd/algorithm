---
tag: 7D6VX1
kind: concept
slug: sign-extension
name: Sign extension
aliases:
- arithmetic shift right
area: techniques/bit-tricks
level: intro
summary: Widening a signed integer by replicating its sign bit into the new high bits.
prereqs: [twos-complement, bitwise-operations]
see_also: [bit-packing, integer-overflow, ones-complement, sign-magnitude-representation, branchless-programming, integer-division, bit-manipulation]
sources:
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition, Addison-Wesley (2013)
    locator: Chapter 2, Section 2-6 (Sign Extension) and Section 2-7 (Shift Right Signed from Unsigned)
  - book: isbn:9780134092669
    title: Randal E. Bryant and David R. O'Hallaron, Computer Systems, A Programmer's Perspective, third edition, Pearson (2016)
    locator: Section 2.2.6 (Expanding the bit representation of a number), Section 2.2.7 (Truncating numbers) and Section 2.1.9 (Shift operations in C)
  - book: isbn:9783642147630
    title: Jörg Arndt, Matters Computational, Ideas, Algorithms, Source Code, Springer (2011)
    locator: Chapter 1, Section 1.1 (Trivia)
  - url: https://graphics.stanford.edu/~seander/bithacks.html
    title: Sean Eron Anderson, Bit Twiddling Hacks
    locator: sections Sign extending from a constant bit-width, and Sign extending from a variable bit-width
  - url: https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf
    title: ISO/IEC 9899:2011 committee draft N1570 (the C11 standard)
    locator: Section 6.3.1.3 (Signed and unsigned integers) and Section 6.5.7 (Bitwise shift operators), paragraphs 4 and 5
---

Sign extension widens a signed integer from $k$ bits to $w > k$ bits without changing its value. In [two's complement](/twos-complement/), a $k$-bit word $v$ with top bit $v_{k-1}$ has the value $-v_{k-1} 2^{k-1} + \sum_{i<k-1} v_i 2^i$, and the $w$-bit word with the same value is $v$ with $w - k$ copies of $v_{k-1}$ placed above it. Processors do this in one instruction when they load a narrow signed value into a wide register; in software, the field $v$ is extended by the formula $(v \oplus m) - m$ with $m = 2^{k-1}$, or by a left shift followed by an arithmetic right shift. The arithmetic right shift is itself sign extension: it fills the vacated high bits with copies of the sign bit.

## In plain words

A negative number in two's complement starts with a 1, and a nonnegative number starts with a 0. If you copy a short signed number into a wider box, the empty places at the left must be filled. Fill them with zeros, and a negative number turns into a large positive one. Fill them with copies of the first bit, and the number keeps its value.

For example, the 4-bit pattern 1011 means minus five. Written with 8 bits, minus five is 11111011: the leading 1 is copied four times. The pattern 0101 means five, and with 8 bits it is 00000101.

## The idea

Fix $1 \le k \le w$. A $k$-bit word $v = (v_{k-1} \dots v_0)_2$, read as a signed two's complement number, has the value

$$\mathrm{val}_k(v) = -v_{k-1} 2^{k-1} + \sum_{i=0}^{k-2} v_i 2^i.$$

**Theorem.** Let $u$ be the $w$-bit word whose low $k$ bits are those of $v$ and whose high $w - k$ bits all equal $v_{k-1}$. Then $\mathrm{val}_w(u) = \mathrm{val}_k(v)$.

*Proof.* If $v_{k-1} = 0$, then $u$ has zeros above bit $k - 2$, and both values are $\sum_{i<k-1} v_i 2^i$. If $v_{k-1} = 1$, then $\mathrm{val}_w(u) = -2^{w-1} + (2^{w-2} + \dots + 2^{k-1}) + \sum_{i<k-1} v_i 2^i$, and $-2^{w-1} + 2^{w-2} + \dots + 2^{k-1} = -2^{k-1}$, a telescoping sum. This is $\mathrm{val}_k(v)$. $\square$

Because $\mathrm{val}_w$ is one-to-one on $w$-bit words, $u$ is the only $w$-bit word with this value, so copying the sign bit is the only way to widen without changing the value.

**Zero extension.** For unsigned numbers the new bits are zeros, and the value does not change either. The two rules differ exactly when $v_{k-1} = 1$: then zero extension gives $\mathrm{val}_k(v) + 2^k$, which is the unsigned reading of $v$.

**The XOR-subtract formula.** Suppose $v$ holds the field in its low $k$ bits and zeros above. With $m = 2^{k-1}$ and arithmetic on $w$-bit words modulo $2^w$,

$$u = (v \oplus m) - m.$$

If $v_{k-1} = 0$, the XOR sets bit $k - 1$, and subtracting $m$ clears it again: $u = v$. If $v_{k-1} = 1$, the XOR clears bit $k - 1$, giving $v - m$, and subtracting $m$ gives $v - 2^k$, which modulo $2^w$ is $v$ with ones in bits $k$ to $w - 1$. Two equivalent forms are $(v \wedge (m - 1)) - (v \wedge m)$ and $v \vee -(v \wedge m)$. Each of them uses unsigned arithmetic only, so none has undefined behaviour in C when done on an unsigned type.

**The shift formula.** Shift $v$ left by $w - k$, so that its sign bit lands in bit $w - 1$, then shift right arithmetically by $w - k$, which copies bit $w - 1$ into the vacated places. This needs a signed type in C, and two rules of C11 then matter. A left shift of a signed value whose result is not representable is undefined (Section 6.5.7, paragraph 4). A right shift of a negative signed value is implementation-defined (Section 6.5.7, paragraph 5); common compilers use an arithmetic shift, but the standard does not require it. A portable version shifts left on an unsigned type, converts to the signed type, which is implementation-defined for out-of-range values before C23 (Section 6.3.1.3, paragraph 3), and then shifts right.

**Arithmetic shift from a logical shift.** With $t = 2^{w-1} \gg n$ computed as a logical shift, $((x \gg_{\text{logical}} n) \oplus t) - t$ equals the arithmetic shift $x \gg_{\text{arith}} n$ for every $w$-bit word $x$ and $0 \le n < w$ (Warren, Section 2-7). It is the XOR-subtract formula applied to the field of $w - n$ bits that the logical shift leaves.

**Narrowing.** The reverse direction, truncating a $w$-bit word to its low $k$ bits, keeps the value exactly when the high $w - k + 1$ bits are all equal, that is, when the value lies in $[-2^{k-1}, 2^{k-1})$. Then sign-extending the truncated word gives the original word back. This is the test for whether a signed value fits in $k$ bits.

## Examples

**Four bits to eight.** The 4-bit field $v = 1011_2 = 11$ has signed value $-8 + 3 = -5$. With $m = 8$: $v \oplus m = 0011_2 = 3$ and $3 - 8 = -5$, which as an 8-bit word is $11111011_2 = 251$. The field $0101_2$ (value 5) gives $00000101_2$.

**A byte to a 16-bit word.** The byte `0x9C` $= 10011100_2$ is 156 unsigned and $-100$ signed. Sign extension gives `0xFF9C` $= 1111111110011100_2$, which is $-100$ as a signed 16-bit word. Zero extension gives `0x009C`, which is 156. The byte `0x7C` has top bit 0, and both extensions give `0x007C` $= 124$.

**A 12-bit field.** A device returns a 12-bit two's complement reading `0xF38`. With $m = 2^{11} = $ `0x800`, $(\texttt{0xF38} \oplus \texttt{0x800}) - \texttt{0x800} = \texttt{0x738} - \texttt{0x800} = -200$, which is `0xFF38` as a 16-bit word.

**Shift and division.** On 8-bit words, the arithmetic shift of $-7 = 11111001_2$ right by 1 is $11111100_2 = -4$, which is $\lfloor -7/2 \rfloor$. C integer division rounds toward zero, so `-7 / 2` is $-3$. An arithmetic right shift is a [division](/integer-division/) by $2^n$ only when the rounding toward $-\infty$ is what the program wants.

**Machine instructions.** On x86, `MOVSX` loads a byte or 16-bit word and sign-extends it, and `MOVZX` zero-extends it. In C, converting a value of type `int8_t` to `int32_t` keeps the value (C11 Section 6.3.1.3, paragraph 1), so the compiler emits a sign extension.

## Where it is used

- Reading signed fields out of packed records, network headers, sensor data and audio samples of 12 or 24 bits; see [bit packing](/bit-packing/).
- Decoding the immediate operands of machine instructions, which are stored as short signed fields and widened to the register size.
- Converting between C integer types of different widths; the rules of the usual arithmetic conversions widen signed values by sign extension and unsigned values by zero extension.
- Building masks without branches: $x \gg_{\text{arith}} (w - 1)$ is 0 for $x \ge 0$ and all ones for $x < 0$, a sign mask used in [branchless programming](/branchless-programming/), for example $|x| = (x \oplus s) - s$ with that mask $s$.
- Checking for [integer overflow](/integer-overflow/) when a wide result is narrowed: the narrowing is safe exactly when sign-extending the narrow result gives back the wide one.
- The other signed codes behave differently: in [ones' complement](/ones-complement/) widening also copies the sign bit, while in [sign-magnitude](/sign-magnitude-representation/) the sign bit stays on top and the new bits are zeros.

## References
