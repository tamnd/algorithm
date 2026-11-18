---
tag: 6SS0HB
kind: algorithm
slug: simd-utf-8-validation
name: Keiser-Lemire UTF-8 validation
aliases:
- SIMD UTF-8 validation
area: strings/text-processing-and-typesetting
level: research
summary: "Validate UTF-8 with vector table lookups on the nibbles of each byte and of the byte before it. The authors measured under 0.4 instructions per byte on AVX2 hardware."
model: word-ram
complexity:
  vars: {n: the number of input bytes, W: the number of bytes in a vector register}
  time: {worst: Θ(n / W), best: Θ(n / W)}
  space: {extra: Θ(W)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [utf-8, bit-parallelism]
see_also: [utf-8, utf-16, deterministic-finite-automaton, vectorization, bitwise-operations, unicode-code-point]
sources:
  - url: https://arxiv.org/abs/2010.03090
    title: John Keiser and Daniel Lemire, Validating UTF-8 In Less Than One Instruction Per Byte, arXiv:2010.03090
    locator: "Section 3 (the rules), Section 6 (the lookup algorithm: 6.1 the 2-byte tables, 6.2 the 3 and 4 byte check, 6.3 incomplete input, 6.4 the ASCII path), Tables 8 and 9, Section 7.2 and Figure 2"
  - url: https://doi.org/10.1002/spe.2920
    title: John Keiser and Daniel Lemire, Validating UTF-8 In Less Than One Instruction Per Byte, Software, Practice and Experience 51(5), 950-964, 2021
    locator: Sections 6 and 7
  - book: isbn:9781936213344
    title: The Unicode Consortium, The Unicode Standard, Version 16.0.0, 2024
    locator: Chapter 3, Section 3.9, D92 and Table 3-7 (well-formed UTF-8 byte sequences)
---

The Keiser-Lemire validator decides whether a byte string is well-formed [UTF-8](/utf-8/) with a few vector instructions per block of 16, 32 or 64 bytes and no branch per byte. Every error in a UTF-8 string shows up in some pair of a byte and the byte before it, or as a continuation byte that the byte two or three places back requires or forbids. The validator looks up the high nibble and the low nibble of the previous byte and the high nibble of the current byte in three 16-entry tables, ANDs the three results, and so gets a set of error bits for every byte in parallel. John Keiser and Daniel Lemire published it in 2021, and on AVX2 processors it ran at over 10 GiB/s in their tests.

## In plain words

A UTF-8 checker usually reads one byte at a time and asks: is this byte allowed here, given the bytes before it? That costs a few decisions per byte, and modern processors are slow when they cannot predict a decision.

This method asks the same question for 16 or 32 bytes at once, with no decisions. The trick is that almost every mistake can be seen by looking at just two neighbouring bytes, and in fact at only three of their four-bit halves. For each half there is a small table of 16 entries that says which mistakes are possible. If all three tables agree on a mistake, the pair is wrong.

One more check looks two and three bytes back, to catch the bytes that a long character needs. The results of all blocks are ORed together, and the text is valid if the final result is zero.

## The problem

The input is a byte string $B$ of length $n$. The output is true if $B$ is a concatenation of the sequences of Table 3-7 of the core specification, and false otherwise. The validator does not say where the first error is, and it does not decode.

Section 3 of the paper lists the kinds of error. With a *continuation* byte meaning one in 80..BF and a *lead* byte one in C0..FF, they are:

- **5+ byte.** A byte F8..FF. It is caught as "too large" below.
- **Too short.** A lead byte followed by a byte that is not a continuation.
- **Too long.** A continuation byte with nothing to continue: after an ASCII byte, or after a complete sequence.
- **Overlong.** C0 or C1 followed by a continuation, E0 followed by 80..9F, F0 followed by 80..8F.
- **Too large.** F4 followed by 90..BF, or F5..FF followed by a continuation.
- **Surrogate.** ED followed by A0..BF.

## The algorithm

The vectors have $W$ bytes ($W = 16$ in the implementation, 32 with AVX2). The operations are lane-wise: AND, OR, XOR, a saturating subtraction SATSUB that stops at 0, a nibble extraction, a 16-entry table lookup (the instruction `pshufb` on x86 and `vqtbl1q_u8` on ARM), and SHIFT$(prev, x, k)$, which builds the vector whose lane $i$ is the byte $k$ places before $x[i]$, taking the first $k$ lanes from the end of $prev$.

```pseudo id=main
VALIDATE(B[0..n-1])
L1  error <- 0; prev <- 0; prev_incomplete <- 0
L2  for each block x of W bytes of B, the last one padded with zero bytes do
L3      if every byte of x is below 0x80 then
L4          error <- error OR prev_incomplete
L5      else
L6          error <- error OR CHECK-BLOCK(x, prev)
L7          prev_incomplete <- SATSUB(x, MAX_TAIL)
L8      prev <- x
L9  error <- error OR prev_incomplete
L10 return every byte of error is 0

CHECK-BLOCK(x, prev)
L11 p1 <- SHIFT(prev, x, 1)
L12 sc <- T1[HIGH(p1)] AND T2[LOW(p1)] AND T3[HIGH(x)]
L13 p2 <- SHIFT(prev, x, 2); p3 <- SHIFT(prev, x, 3)
L14 must23 <- (SATSUB(p2, 0x60) OR SATSUB(p3, 0x70)) AND 0x80
L15 return must23 XOR sc
```

**The tables (line L12).** Each error kind gets one bit. A bit is set in the AND exactly when all three tables have it, so each table entry lists the error kinds that its nibble allows. With the bit values of the paper's Table 9:

| bit | name | previous byte | current byte |
|---|---|---|---|
| 01 | TOO_SHORT | C0..FF | 00..7F or C0..FF |
| 02 | TOO_LONG | 00..7F | 80..BF |
| 04 | OVERLONG_3 | E0 | 80..9F |
| 08 | TOO_LARGE | F4..FF | 90..BF |
| 10 | SURROGATE | ED | A0..BF |
| 20 | OVERLONG_2 | C0, C1 | 80..BF |
| 40 | OVERLONG_4 or TOO_LARGE_1000 | F0 or F5..FF | 80..8F |
| 80 | TWO_CONTS | 80..BF | 80..BF |

For example, T1, indexed by the high nibble of the previous byte, has 02 at the nibbles 0 to 7, 80 at 8 to B, 21 at C, 01 at D, 15 at E and 49 at F. The nibble E allows TOO_SHORT, OVERLONG_3 and SURROGATE, and T2 and T3 then narrow OVERLONG_3 to the low nibble 0 and the current bytes 80..9F. Bit 40 serves two kinds that never meet: both need a current byte in 80..8F, and the previous byte is F0 for one and F5..FF for the other.

**Two continuations (line L14).** TWO_CONTS is not always an error. The third and fourth bytes of a sequence are continuations after a continuation. They are expected exactly when the byte two places back is at least E0 or the byte three places back is at least F0. SATSUB$(y, \mathtt{60})$ has bit 7 set exactly when $y \ge \mathtt{E0}$, and SATSUB$(y, \mathtt{70})$ exactly when $y \ge \mathtt{F0}$. The XOR of line L15 clears TWO_CONTS where it is expected and sets bit 7 where a continuation is expected but missing.

**The end of the input (lines L7 and L9).** A sequence can start in the last 3 bytes of a block. The next block checks it, but if the input ends, or the next block is all ASCII and skipped, nothing would. MAX_TAIL is FF in every lane except the last three, which hold EF, DF and BF. SATSUB$(x, \mathtt{MAX\_TAIL})$ is nonzero exactly when the third last byte is at least F0, the second last at least E0 or the last at least C0.

**The ASCII path (lines L3 and L4).** A block of ASCII bytes has no error of its own. It only needs the check of the end of the block before it. The paper does this test on blocks of 64 bytes.

## Example

The bytes of "9", ç, 鏡 and 😀, followed by a zero byte, as in Table 9 of the paper. The previous vector is zero.

| lane | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| input | 39 | C3 | A7 | E9 | 8F | A1 | F0 | 9F | 98 | 80 | 00 |
| previous byte | 00 | 39 | C3 | A7 | E9 | 8F | A1 | F0 | 9F | 98 | 80 |
| T1 | 02 | 02 | 21 | 80 | 15 | 80 | 80 | 49 | 80 | 80 | 80 |
| T2 | E7 | CB | 83 | CB | CB | CB | A3 | E7 | CB | CB | E7 |
| T3 | 01 | 01 | BA | 01 | E6 | BA | 01 | AE | AE | E6 | 01 |
| sc | 00 | 00 | 00 | 00 | 00 | 80 | 00 | 00 | 80 | 80 | 00 |
| must23 | 00 | 00 | 00 | 00 | 00 | 80 | 00 | 00 | 80 | 80 | 00 |
| error | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 | 00 |

The three 80 values of sc are the third byte A1 of 鏡 and the third and fourth bytes 98 and 80 of 😀. The bytes E9 two places before lane 5 and F0 two and three places before lanes 8 and 9 make must23 equal there, so the XOR clears them. The test `test_table_9_worked_example` checks every row.

Now change the last byte of 😀 from 80 to 41. In lane 9, T1 at 9 is 80, T2 at 8 is CB and T3 at 4 is 01, so sc is 00. But F0 is three places back, so must23 is 80, and the error is 80: the sequence is too short. For the overlong pair C0 AF, the lane of AF has 21 AND E7 AND BA = 20, which is OVERLONG_2.

## Correctness

The paper derives the tables from the error list. The proof in proofs/correctness.md goes the other way. First, the bits of $sc$ have exactly the meanings in the table above, which `test_meaning_of_each_error_bit` checks on all 65,536 byte pairs. Second, with the input padded by zero bytes on both sides, the validator reports an error exactly when some position $j$ has $sc(j) \ne must23(j)$, because the block checks see every position of the input, and the end check covers the positions of the skipped ASCII blocks and of the padding. Third, a string is well-formed exactly when no position has such an error. In one direction, in a well-formed string, $sc$ is TWO_CONTS exactly at the third and fourth bytes of sequences, and $must23$ is 80 at exactly the same places. In the other, the first place where a decoder would fail has a bad pair, or a missing or extra continuation that $must23$ exposes.

## Complexity

Count each vector instruction as one step. This is an assumption of the analysis: a real instruction has a latency and a throughput that depend on the processor. Then each block of $W$ bytes costs a constant number of steps: two nibble extractions and three lookups, three shifts, two saturating subtractions, and five AND, OR and XOR operations. The whole input costs $\Theta(n / W)$ steps and $\Theta(W)$ bytes of state. The ASCII path makes blocks of pure ASCII cost only a test and an OR.

The speed is a measurement, not a consequence of the model. On an Intel i7-6700 (Skylake) and an AMD EPYC 7262 (Zen 2), with GCC 9.3 and AVX2, the lookup validator retires slightly under 0.4 instructions per byte on the files twitter.json and hongkong.html (section 7.2), and it validates random UTF-8 at about 12 to 13 GB/s (Figure 2). Section 2 states: "We consistently exceed 10 GiB/s".

| claim | value |
|---|---|
| steps per block | a constant number of vector instructions |
| total | $\Theta(n / W)$ steps |
| measured, AVX2 | under 0.4 instructions per byte |

## Properties

- **No data-dependent branch inside a block.** The only branch is the ASCII test, which is well predicted on most real text.
- **Same language as Table 3-7.** It accepts exactly the well-formed UTF-8 strings, including the noncharacters, which are scalar values.
- **Verdict only.** The errors are ORed across blocks, so the result says only that the input is bad. Finding the position needs a second, scalar pass.
- **Streaming.** The state between blocks is the previous block, the end check value and the error vector, so the input can arrive in pieces.

## Variants and improvements

- **Branchy and finite-state validators.** A scalar validator reads one byte at a time with branches, or runs a [finite automaton](/deterministic-finite-automaton/) with a transition table. The paper uses such validators as baselines.
- **Wider vectors.** With AVX2, $W = 32$, and the shifts must cross the two 128-bit halves of a register with a permute. With AVX-512, $W = 64$.
- **Transcoding.** The same checks run inside SIMD converters from UTF-8 to [UTF-16](/utf-16/), which must validate anyway.
- **Error position.** After a failed block, run a scalar decoder from a few bytes before that block to find the first bad byte.

## When to use it

Use it when large inputs must be validated before they are parsed: JSON documents, files read from disk, and network messages. Most such input is valid and mostly ASCII, and the validator then costs a small part of the parsing time. For short strings, a scalar validator is as fast, because the vector setup dominates. When the program also needs the code points, decoding validates as a side effect, so a separate validator is only worth it when the decoder itself is slow or when the data stays in UTF-8.

## Pitfalls

- **Missing end check.** If the input ends exactly at a block boundary, an incomplete sequence in the last 3 bytes leaves no trace in the block checks. Lines L7 and L9 catch it, and the test `test_sequence_cut_at_the_end_of_a_full_vector` checks it.
- **Skipped ASCII blocks.** An ASCII block after a block that ends inside a sequence must still raise the error. Line L4 does that, and the same test covers it.
- **Padding.** The last block must be padded with zero bytes, which are ASCII. Other padding can hide a truncated sequence or create a false error.
- **Lost context.** The previous block must be kept even when the current one is ASCII, or the shifts of the next block see the wrong bytes.
- **Copying the tables by hand.** One wrong bit in one of the 48 table entries accepts some bad pair or rejects some good one, and random tests rarely find it. Build the entries from the named bit constants, as the implementation does, and check all 65,536 pairs.
- **Reading the speed as a bound.** "Less than one instruction per byte" is a measurement on specific processors and inputs. On other hardware the number differs.

## Implementations

## History

UTF-8 validation was long done with byte-at-a-time decoders or with table-driven automata. Keiser and Lemire posted their lookup method on arXiv in October 2020 and published it in Software: Practice and Experience in 2021. The method is used in the simdjson parser, which must validate its UTF-8 input, and the paper compares it with scalar validators on the same hardware.

## References
