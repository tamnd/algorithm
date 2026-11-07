---
tag: 8H3YQ9
kind: algorithm
slug: double-dabble
name: Double dabble
aliases:
- shift-and-add-3
- binary to BCD conversion
area: algebra/integer-arithmetic
level: intro
summary: Converts binary to packed BCD by shifting left and adding 3 to digits of 5 or more.
solves: [radix-conversion]
model: word-ram
complexity:
  vars: {n: the number of binary digits of the input}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [positional-number-system, integer-addition]
see_also: [radix-conversion, positional-number-system, carry-propagation, integer-division]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.4, Radix conversion (Method 1b, multiplication by the old radix in the arithmetic of the new radix, which double dabble is for the radices 2 and 10)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.7, Base conversion (quadratic and subquadratic conversion, for comparison)
---

Double dabble converts an $n$-bit binary number to binary-coded decimal (BCD), with four bits per decimal digit. It shifts the bits of the input one at a time into a register of decimal digits, and before each shift it adds 3 to each digit that is 5 or more. That correction makes the binary shift act as a doubling in decimal, so after $n$ shifts the register holds the decimal digits of the input. It needs only shifts, comparisons and the addition of a constant, which is why it is common in hardware without a divider, such as FPGA and microcontroller code that drives decimal displays. It takes $\Theta(n^2)$ digit operations; divide-and-conquer [radix conversion](/radix-conversion/) is faster for long numbers.

## In plain words

Reading a binary number from its first bit, you can find its value by a simple rule: start with zero, and for each bit, double what you have and add the bit. Double dabble does this doubling in decimal, digit by digit, while it reads the bits.

Doubling a decimal digit is easy except when the digit is 5 or more, because then the result is 10 or more and must carry into the next digit. Each digit is stored in four bits, and shifting four bits left doubles them in binary, where a carry happens only at 16. Adding 3 first fixes this: a digit of 5 or more becomes 8 or more, and its double becomes 16 or more, so the carry comes out at the right moment, and what stays behind is the correct decimal digit.

## The problem

The input is a natural number $x < 2^n$ given by its bits $x_{n-1}, \ldots, x_0$, most significant first. The output is its decimal digits $D[0], \ldots, D[d-1] \in \{0, \ldots, 9\}$, least significant first, with $x = \sum_i D[i]\, 10^i$, where $d = \lceil n \log_{10} 2 \rceil$ is the number of decimal digits of $2^n - 1$ (and $d = 1$ for $n = 0$). In packed BCD, $D[i]$ occupies bits $4i$ to $4i + 3$ of the output. This is a case of [radix conversion](/radix-conversion/), from base 2 to base 10.

The cost model counts digit operations: comparing a 4-bit digit with 5, adding 3 to it, and shifting it left by one bit with a carry in and out each cost $O(1)$. On a word RAM with $w$-bit words, $w/4$ digits can be handled in parallel by masks, which divides the cost by $\Theta(w)$.

## The algorithm

```pseudo id=main
DOUBLE-DABBLE(x_{n−1} … x_0)               ▷ returns D[0 .. d − 1], low digit first
L1  D[0 .. d − 1] ← 0
L2  for each bit b of x, from x_{n−1} down to x_0 do
L3      for i ← 0 to d − 1 do
L4          if D[i] ≥ 5 then D[i] ← D[i] + 3        ▷ the dabble
L5      carry ← b
L6      for i ← 0 to d − 1 do                        ▷ shift the register left by one bit
L7          t ← 2 · D[i] + carry
L8          D[i] ← t mod 16, carry ← ⌊t / 16⌋
L9  return D
```

Lines L5 to L8 are a left shift of the whole register by one bit, with the next input bit shifted in at the bottom; each digit is a 4-bit field, and bit 3 of a digit moves into bit 0 of the next one. In hardware, the input register sits to the right of the BCD register, and one shift of the joined register does lines L5 to L8. The adjustments of line L4 are independent of each other and are done in parallel.

## Example

Convert $x = 243 = 1111\,0011_2$, with $n = 8$ and $d = 3$. The BCD register is shown with the hundreds digit first, followed by the input bits not yet shifted in.

| step | hundreds | tens | ones | bits left | value of $D$ |
|---|---|---|---|---|---|
| start | 0000 | 0000 | 0000 | 11110011 | 0 |
| shift 1 | 0000 | 0000 | 0001 | 1110011 | 1 |
| shift 2 | 0000 | 0000 | 0011 | 110011 | 3 |
| shift 3 | 0000 | 0000 | 0111 | 10011 | 7 |
| add 3 to ones | 0000 | 0000 | 1010 | 10011 | |
| shift 4 | 0000 | 0001 | 0101 | 0011 | 15 |
| add 3 to ones | 0000 | 0001 | 1000 | 0011 | |
| shift 5 | 0000 | 0011 | 0000 | 011 | 30 |
| shift 6 | 0000 | 0110 | 0000 | 11 | 60 |
| add 3 to tens | 0000 | 1001 | 0000 | 11 | |
| shift 7 | 0001 | 0010 | 0001 | 1 | 121 |
| shift 8 | 0010 | 0100 | 0011 | | 243 |

The output is $0010\,0100\,0011$, which is $\text{0x243}$ read as packed BCD. After each shift the register holds the decimal value of the bits read so far: 1, 3, 7, 15, 30, 60, 121, 243. In the same way, $65535$ with $n = 16$ gives $\text{0x65535}$.

## Correctness

The invariant of the loop of line L2 is: after the first $k$ bits have been shifted in, every $D[i]$ is in $\{0, \ldots, 9\}$ and $\sum_i D[i]\, 10^i = \lfloor x / 2^{n-k} \rfloor$, the number formed by those $k$ bits. One step doubles this value and adds the bit. If $D[i] \le 4$, then $2D[i] + c \le 9$ and the digit produces no carry. If $D[i] \ge 5$, line L4 makes it $D[i] + 3 \le 12$, and $2(D[i] + 3) + c = 16 + (2D[i] + c - 10)$, so line L8 leaves $2D[i] + c - 10 \in \{0, \ldots, 9\}$ and carries 1, worth 10 at this position. So each digit does exactly a decimal doubling with carry. Since $x < 10^d$, the top digit never carries out. The full proof is below.

## Complexity

- **Time.** The loop of line L2 runs $n$ times, and each pass does $2d$ digit steps in lines L3 to L8. With $d = \lceil n \log_{10} 2 \rceil \approx 0.30103\, n$, the total is $2nd = \Theta(n^2)$ digit operations, in every case, since no step depends on the values.
- **Space.** The register holds $d$ digits, $4d \approx 1.204\, n$ bits, so $\Theta(n)$.
- **Saving the first steps.** A digit can reach 5 only after three bits have entered it, so the first three passes of line L3 never adjust, and the passes for digit $i$ can start only when bits have reached it. Hardware versions use this to drop about half of the add-3 cells; the order $\Theta(n^2)$ does not change.
- **As a circuit.** Unrolling the loop gives a triangular array of add-3 cells with $n$ levels, each of constant depth, so the depth is $O(n)$ and the size is $O(n^2)$.

## Properties

- **No division.** The usual conversion divides by 10 repeatedly. Double dabble uses only shifts, comparisons and additions of the constant 3, and so suits hardware and small processors without a fast divider.
- **Bit serial.** It reads the input one bit at a time, most significant first, so it can convert a number while the bits arrive.
- **Not adaptive.** It does the same work for each input of $n$ bits.
- **In place.** In hardware, the input and the BCD digits share one shift register of $n + 4d$ bits.

## Variants and improvements

- **Add 6 after the shift.** Double each digit with the carry from below, and if $2D[i] + c \ge 10$, subtract 10 and carry 1. On 4-bit fields this is the add-6 correction of BCD addition, as done by the DAA instruction of the x86 family after a binary addition of $D + D$; it gives the same digits as adding 3 before the shift.
- **Reverse double dabble.** To convert BCD to binary, shift the register right by one bit at a time, and after each shift subtract 3 from each digit that is 8 or more. A digit receives 8 exactly when the digit above it was odd, while a decimal halving should give it 5.
- **Several bits per step.** Shift in $k$ bits at a time and correct each digit with a table of $2^{k+4}$ entries, which trades area for fewer steps.
- **Other target bases.** For a target base $B$ that is even and at most 16, stored in 4-bit fields, the correction is to add $8 - B/2$ to each digit that is at least $B/2$.
- **Fast conversion.** For numbers of thousands of bits, divide-and-conquer [radix conversion](/radix-conversion/) splits $x$ by a power of 10 and converts the halves, in $O(M(n) \log n)$ time.

## When to use it

Use double dabble when you need decimal digits from a binary number in hardware, or on a processor with no divide instruction, and the numbers are short, such as a 16-bit counter shown on a seven-segment display. On a processor with fast division, repeated division by 10 (or by $10^k$ for blocks of digits) uses fewer steps. For long numbers, use divide-and-conquer radix conversion.

## Pitfalls

- **Adjusting after the last shift.** Line L4 comes before the shift of each pass, and there is no adjustment after the last shift. An extra adjustment at the end changes digits 5 to 9 into 8 to 12, which are not decimal digits.
- **The wrong threshold.** Line L4 tests $D[i] \ge 5$. Testing $D[i] > 5$ or $D[i] \ge 8$ breaks the doubling of the digit 5: $2 \cdot 5 = 10$ must carry, and only $5 + 3 = 8$ makes the 4-bit shift carry.
- **A register that is too short.** The register needs $d = \lceil n \log_{10} 2 \rceil$ digits. With fewer, the top carry of line L8 is lost; for $n = 8$, the value 255 needs 3 digits, not 2.
- **Shifting digits one by one without the carry.** Lines L7 and L8 move bit 3 of each digit into bit 0 of the next digit. Shifting each 4-bit field on its own, as $D[i] \leftarrow 2D[i] \bmod 16$ with no carry, drops the carries that make the decimal doubling work.

## Implementations

## History

Double dabble is Horner's rule $x = (\cdots((x_{n-1}) \cdot 2 + x_{n-2}) \cdot 2 + \cdots) \cdot 2 + x_0$ evaluated in decimal arithmetic, which is Knuth's Method 1b of radix conversion. The add-3 correction is the decimal adjustment of BCD adders moved to before the shift. The name and the shift-and-add-3 form are folklore of digital design, and the method appears in textbooks and FPGA application notes for driving decimal displays.

## References
