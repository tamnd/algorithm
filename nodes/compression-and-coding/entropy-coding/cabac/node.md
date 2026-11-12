---
tag: SYQ77C
kind: algorithm
slug: cabac
name: Context-adaptive binary arithmetic coding
aliases:
- CABAC
area: compression-and-coding/entropy-coding
level: advanced
summary: The entropy coder of H.264 and HEVC. It turns each syntax element into bins, picks a context per bin, and codes it with a table-driven binary arithmetic coder with 64 probability states.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of bins, c: the number of contexts}
  time: {worst: Θ(n + c), average: Θ(n + c), best: Θ(n + c)}
  space: {extra: Θ(c)}
properties: {deterministic: true, online: true, recursive: false, comparison: false}
history:
  year: 2003
  people: [Detlev Marpe, Heiko Schwarz, Thomas Wiegand]
  note: Marpe, Schwarz and Wiegand designed CABAC for H.264/AVC, approved in 2003. HEVC (2013) kept the same coding engine.
prereqs: [arithmetic-coding, context-modeling]
see_also: [adaptive-modeling, exp-golomb-coding, unary-coding, range-coding, jpeg-2000, huffman-coding]
sources:
  - paper: doi:10.1109/TCSVT.2003.815173
    title: Detlev Marpe, Heiko Schwarz and Thomas Wiegand, Context-based adaptive binary arithmetic coding in the H.264/AVC video compression standard, IEEE Transactions on Circuits and Systems for Video Technology 13(7), 620-636, 2003
    locator: the sections on binarization, context modeling, the probability estimation with 64 states, and the table-based arithmetic coder
  - url: https://www.itu.int/rec/T-REC-H.264
    title: ITU-T Recommendation H.264, Advanced video coding for generic audiovisual services
    locator: Section 9.3 (CABAC parsing process), 9.3.1.1 (initialization of the context variables), 9.3.2 (binarization), 9.3.3.2 (the arithmetic decoding engine), 9.3.4.2 (the arithmetic encoding engine), Tables 9-44 and 9-45
---

Context-adaptive binary arithmetic coding (CABAC) is the entropy coder of the H.264/AVC and HEVC video standards. It codes a stream of binary decisions, the *bins*, with a binary [arithmetic coder](/arithmetic-coding/) whose probabilities come from small adaptive models, the *contexts*. A syntax element such as a motion vector difference or a coefficient level is first turned into bins by a binarization. Each bin then gets a context chosen from the bins and elements already coded, as in [context modeling](/context-modeling/), and the coder codes it with the probability that the context holds. The coding engine works without multiplication: a 9-bit range, a table of 64 × 4 sub-ranges and a table of state changes do all the arithmetic. This page gives the engine of H.264, Section 9.3.

## In plain words

A video coder makes many yes-or-no decisions per block: is this coefficient zero, is this the last one, is the next level larger than one. CABAC writes each of these answers in less than one bit when the answer is easy to guess.

For each kind of question, in each situation, the coder keeps a small counter that says which answer is more likely and how sure it is. The counter moves up a step each time the guess is right and jumps down when it is wrong. The coder keeps a number range, gives the likely answer the larger part of it, and keeps only the part of the actual answer. When the range gets small, it doubles the range and sends out a bit. The decoder keeps the same counters and makes the same cuts, so it can follow the encoder.

## The problem

The input is a sequence of bins $b_1, b_2, \ldots$, each with a label that says how it is coded: with a context (a *decision* bin), with the fixed probability $\tfrac12$ (a *bypass* bin), or as the end-of-slice flag (a *terminate* bin). A context is a pair $(\sigma, v)$ of a probability state $\sigma \in \{0, \ldots, 62\}$ and the value $v$ of the most probable symbol (MPS); the other value is the least probable symbol (LPS). The output is a bit string from which a decoder that makes the same choices of context gets the bins back. The goal is a length close to $\sum_i \lg(1/p_i)$, the information of the bins under the probabilities of the contexts, at a low and fixed cost per bin.

## The algorithm

State $\sigma$ stands for the LPS probability $p_\sigma = \tfrac12 \alpha^\sigma$ with $\alpha = (0.01875/0.5)^{1/63} \approx 0.949$, so $p_0 = 0.5$ and $p_{62} \approx 0.02$. The table rangeTabLPS (Table 9-44) gives, for each state and each of the four quarters $q$ of the range, the width of the LPS part, close to $p_\sigma$ times the range. The table transIdxLPS (Table 9-45) gives the new state after an LPS. After an MPS the state goes up by one, to at most 62. State 63 is used only for the terminate bin.

```pseudo id=main
INIT-ENCODER
L1  low ← 0, range ← 510, first ← true, outstanding ← 0

ENCODE-DECISION(ctx, bin)
L2  rLPS ← rangeTabLPS[ctx.state][(range >> 6) & 3]
L3  range ← range − rLPS
L4  if bin ≠ ctx.mps then
L5      low ← low + range, range ← rLPS
L6      if ctx.state = 0 then ctx.mps ← 1 − ctx.mps
L7      ctx.state ← transIdxLPS[ctx.state]
L8  else ctx.state ← min(ctx.state + 1, 62)
L9  RENORM-E

RENORM-E
L10 while range < 256 do
L11     if low < 256 then PUT-BIT(0)
L12     else if low ≥ 512 then low ← low − 512, PUT-BIT(1)
L13     else low ← low − 256, outstanding ← outstanding + 1
L14     range ← 2 · range, low ← 2 · low

PUT-BIT(b)
L15 if first then first ← false else write b
L16 write outstanding copies of 1 − b, outstanding ← 0

ENCODE-BYPASS(bin)
L17 low ← 2 · low + bin · range
L18 if low ≥ 1024 then low ← low − 1024, PUT-BIT(1)
L19 else if low < 512 then PUT-BIT(0)
L20 else low ← low − 512, outstanding ← outstanding + 1

ENCODE-TERMINATE(bin)
L21 range ← range − 2
L22 if bin = 1 then low ← low + range, range ← 2, RENORM-E, PUT-BIT((low >> 9) & 1), write ((low >> 7) & 3) | 1 in 2 bits
L23 else RENORM-E

INIT-DECODER
L24 range ← 510, offset ← the first 9 bits

DECODE-DECISION(ctx)
L25 rLPS ← rangeTabLPS[ctx.state][(range >> 6) & 3], range ← range − rLPS
L26 if offset ≥ range then bin ← 1 − ctx.mps, offset ← offset − range, range ← rLPS, update ctx as in L6 and L7
L27 else bin ← ctx.mps, update ctx as in L8
L28 while range < 256 do range ← 2 · range, offset ← 2 · offset + the next bit
L29 return bin

DECODE-BYPASS
L30 offset ← 2 · offset + the next bit
L31 if offset ≥ range then offset ← offset − range, return 1 else return 0

DECODE-TERMINATE
L32 range ← range − 2
L33 if offset ≥ range then return 1 else renormalize as in L28 and return 0
```

**The engine.** The range stays in $[256, 510]$. Line L2 uses two bits of the range to pick one of four columns, so the LPS width is a table lookup in place of a product. The MPS part is the lower part of the interval and the LPS part the upper one. The renormalization at L10 to L14 is the carry handling of [Witten, Neal and Cleary](/arithmetic-coding/) on a 10-bit register: when the interval straddles the middle, the coder counts an *outstanding* bit and writes it as soon as the next bit is known. The first bit is always 0, and line L15 drops it.

**Bypass bins.** A bypass bin halves the interval. Lines L17 to L20 shift first and then compare with doubled bounds, which saves a renormalization loop. Signs and the suffixes of Exp-Golomb codes are bypass bins, because their values are close to uniform.

**Terminate.** The end-of-slice flag is coded with an LPS width of 2. When it is 1, the encoder flushes: it renormalizes, writes the bit that settles the outstanding bits and two more bits. The last bit written is always 1, and H.264 uses it as the stop bit of the slice data.

**Binarization.** H.264 turns each syntax element into bins with a few codes: [unary](/unary-coding/) and truncated unary codes, fixed-length codes, [Exp-Golomb](/exp-golomb-coding/) codes of order $k$, and code tables for the macroblock and sub-macroblock types. The UEG$k$ code of a coefficient level or of a motion vector difference has a truncated unary prefix in decision bins and an Exp-Golomb suffix in bypass bins.

**Context selection.** Each bin of a binarization has a context index from a fixed rule. For example, the first bin of a motion vector difference picks one of three contexts from the sum of the differences of the left and upper blocks, and a coefficient bin picks a context from its position in the block. H.264 has several hundred context variables. At the start of each slice every context is set from two constants $(m, n)$ and the slice QP: $pre = \mathrm{clip}(1, 126, ((m \cdot QP) \gg 4) + n)$, then $\sigma = 63 - pre$ and MPS 0 if $pre \le 63$, else $\sigma = pre - 64$ and MPS 1.

## Example

Take one context with state 10 and MPS 0, and code the decision bins 0, 0, 1, 0, then a bypass 1 and a terminate 1.

| bin | state | range | $q$ | rLPS | then low | then range | new state | outstanding |
|---|---|---|---|---|---|---|---|---|
| 0 (MPS) | 10 | 510 | 3 | 142 | 0 | 368 | 11 | 0 |
| 0 (MPS) | 11 | 368 | 1 | 99 | 0 | 269 | 12 | 0 |
| 1 (LPS) | 12 | 269 | 0 | 77 | 256 | 308 | 9 | 1 |
| 0 (MPS) | 9 | 308 | 0 | 90 | 0 | 436 | 10 | 2 |

The first two bins leave the range above 256, so nothing is written. The LPS takes the upper 77 of the range 269: low becomes 192 and range 77. Two shifts follow: the first writes the dropped 0 bit, and the second finds the interval in the middle and counts an outstanding bit. The state goes from 12 to transIdxLPS[12] = 9. The last MPS needs one shift, again in the middle. The bypass 1 gives $low = 0 + 436 < 512$, so it writes 0 and the two outstanding 1 bits. The terminate bin and the flush add 10 more bits, and the stream is `0111101100111`, the bytes `7B 38` with the padding. There were 4 shifts before the terminate bin, and the stream has $4 + 9 = 13$ bits. The decoder reads 9 bits, follows the same splits, and after the terminate bin it has read the 13 bits exactly.

## Correctness

The proof follows the coder with an exact integer $A$, the lower end of the interval with no bits taken out. Two invariants hold: the range stays in $[256, 510]$ with $low + range \le 1024$, and $A$ equals the bits written so far, followed by the outstanding bits, plus the register $low$. So the written bits are a prefix of every point in the interval. The flush writes the value of a point inside the final interval, and the decoder's $offset$ is that point minus $A$, so the comparisons at L26, L31 and L33 pick the same part as the encoder. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/).

- **Time.** A bin costs a table lookup, a few additions and at most 7 shifts of the renormalization, so $n$ bins cost $\Theta(n)$. Setting up the contexts costs $\Theta(c)$ per slice.
- **Space.** One byte per context: 6 bits of state and 1 bit of MPS. The tables have $64 \cdot 4 + 64$ entries.
- **Code length.** The proof shows that the stream has at most $\sum_i \lg(1/p_i) + 9$ bits, where $p_i$ is the probability the coder gave bin $i$. On 50000 bins with an LPS probability of 0.1 in one context, the implementation was about 4% above the entropy of the source, because the state machine keeps adapting.

## Properties

- **No multiplication.** The table gives the LPS width from 6 bits of state and 2 bits of range.
- **Adaptive.** Each context follows its bins with a memory of about $1/(1 - \alpha) \approx 20$ bins.
- **Sequential.** Each decision bin depends on the range left by the one before, so a decoder cannot code bins of one slice in parallel. This is the main cost of CABAC in hardware.
- **Slice by slice.** The contexts and the engine start over at each slice, so slices can be decoded on their own.

## Variants and improvements

- **CAVLC.** The Baseline profile of H.264 uses context-adaptive variable-length codes in place of CABAC. Marpe et al. (2003) report bit-rate savings of 9 to 14 percent for CABAC over CAVLC.
- **HEVC.** H.265 uses the same engine and state tables with fewer contexts, more bypass bins grouped together, and wavefront parallel processing, which starts each row of blocks from contexts saved in the row above.
- **VVC.** H.266 replaces the 64-state machine with two probability estimates that adapt at different rates and are averaged, and computes the LPS width with a small product.
- **The Q-coder and MQ-coder.** Earlier table-driven binary arithmetic coders with a state machine for the probability. The MQ-coder is used in [JPEG 2000](/jpeg-2000/) and JBIG2.

## When to use it

Use CABAC when the standard asks for it: in H.264 Main and High profiles and in HEVC. Its design suits any coder of binary decisions with a small fixed alphabet of contexts and a need for a fixed cost per bin without multiplication. When decisions are not binary, or when a counter with more precision is affordable, a multi-symbol [range coder](/range-coding/) with [adaptive models](/adaptive-modeling/) is simpler.

## Pitfalls

- **Range is 9 bits, low is 10 bits.** The encoder's register holds one more bit than the decoder's offset. Using the same width on both sides breaks the outstanding-bit logic.
- **The first bit.** The encoder must drop the first bit it puts; the decoder starts by reading 9 bits, not 10.
- **The bypass shift.** Lines L17 to L20 compare with 1024 and 512 because the shift happens first. Using the bounds of the decision path gives a wrong stream.
- **State 63.** It is reserved for the terminate bin. The MPS step stops at 62, and the context initialization never gives 63.
- **The flush.** The two final bits are $((low \gg 7) \bmod 4)$ with the low bit set. Writing them unchanged loses the stop bit.

## Implementations

## History

Binary arithmetic coding with a state machine for the probability goes back to the Q-coder of IBM in 1988 and to its successors, the QM-coder of JBIG and JPEG and the MQ-coder of JBIG2 and JPEG 2000. Marpe, Schwarz and Wiegand developed CABAC for the H.264/AVC standard of the ITU-T and ISO/IEC, which was approved in 2003, and described it the same year. They kept the idea of a table-driven engine and added a systematic design of binarization and context selection for video syntax. HEVC, approved in 2013, uses CABAC as its only entropy coder, and VVC (2020) keeps the scheme with a new probability estimate.

## References
