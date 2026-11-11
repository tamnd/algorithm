---
tag: GC5V3X
kind: algorithm
slug: arithmetic-coding
name: Arithmetic coding
aliases:
- arithmetic coder
- Witten-Neal-Cleary coder
area: compression-and-coding/entropy-coding
level: advanced
summary: Codes a whole message as one binary fraction inside a nested interval, so the length is within 2 bits of the sum of -lg p over the message, with no rounding per symbol.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of symbols, m: the length of the output, s: the alphabet size}
  time: {worst: Θ(n s + m), average: Θ(n s + m), best: Θ(n s + m)}
  space: {extra: Θ(s)}
properties: {deterministic: true, online: true, recursive: false, comparison: false}
history:
  year: 1976
  people: [Jorma Rissanen, Richard C. Pasco]
  note: Rissanen and Pasco found finite-precision arithmetic codes in 1976; Witten, Neal and Cleary published the integer coder that most programs copy in 1987.
prereqs: [shannon-entropy, lossless-compression]
see_also: [range-coding, asymmetric-numeral-systems, shannon-fano-elias-coding, huffman-coding, adaptive-modeling, context-modeling, cabac, prediction-by-partial-matching]
sources:
  - paper: doi:10.1147/rd.203.0198
    title: J. J. Rissanen, Generalized Kraft inequality and arithmetic coding, IBM Journal of Research and Development 20(3), 1976
    locator: pp. 198 to 203
  - paper: "Richard Clark Pasco, Source coding algorithms for fast data compression, PhD thesis, Stanford University, 1976"
    title: Source coding algorithms for fast data compression
    locator: the whole thesis (FIFO arithmetic codes with finite precision)
  - paper: doi:10.1109/TIT.1981.1056282
    title: Jorma Rissanen and Glen G. Langdon, Jr., Universal modeling and coding, IEEE Transactions on Information Theory 27(1), 1981
    locator: pp. 12 to 23 (the split of a compressor into a model and a coder)
  - paper: doi:10.1145/214762.214771
    title: Ian H. Witten, Radford M. Neal and John G. Cleary, Arithmetic coding for data compression, Communications of the ACM 30(6), 1987
    locator: pp. 520 to 540 (the C program with low, high and bits_to_follow, the adaptive model, and the section on compression efficiency)
  - paper: doi:10.1145/290159.290162
    title: Alistair Moffat, Radford M. Neal and Ian H. Witten, Arithmetic coding revisited, ACM Transactions on Information Systems 16(3), 1998
    locator: pp. 256 to 294 (the low and range form, carry handling, frequency limits and the cost of finite precision)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 5.9 (Shannon-Fano-Elias coding, the code length bound below lg(1/p) + 2) and Section 13.3 (arithmetic coding)
---

Arithmetic coding is a [lossless](/lossless-compression/) entropy coder that maps a whole message to one binary fraction inside an interval of width equal to the probability of the message. For each message and each probability model, the code has at most $\sum_i \lg(1/p_i) + 2$ bits with exact arithmetic, where $p_i$ is the probability that the model gave to the $i$-th symbol. So it loses less than one bit per message where a [Huffman code](/huffman-coding/) can lose up to one bit per symbol, and it separates the model from the coder: any [adaptive](/adaptive-modeling/) or [context](/context-modeling/) model can drive it. This page gives the integer coder of Witten, Neal and Cleary (1987), with $b$-bit registers and pending bits.

## In plain words

Start with the range from zero to one. Cut it into parts, one for each possible first symbol, with a size that matches how likely that symbol is. Keep the part of the symbol that actually comes. Cut that part again for the second symbol, and so on. At the end you have a small range, and its size is the probability of the whole message. Any number in it names the message, and a short binary fraction always fits in it.

A computer cannot keep an exact range that gets smaller and smaller. So the coder keeps the two ends in fixed-size registers. When both ends agree on the first binary digit, that digit can never change, so the coder writes it out and doubles the range. When the range sits around the middle and is small, the coder defers the digit and remembers how many it deferred.

## The problem

The input is a message $x_1 \ldots x_n$ over the alphabet $\Sigma = \{0, \ldots, \sigma - 1\}$ and a model that, before each symbol, gives integer counts: $c_{lo}(s)$, $c_{hi}(s) = c_{lo}(s) + f(s)$ and a total $T$, with $f(s) \ge 1$ for each symbol. The probability of $s$ is $p(s) = f(s)/T$. The output is a bit string from which the decoder, which runs the same model, gets the message back. This is [lossless compression](/lossless-compression/). The bound of this page is for each input, with no source model: it compares the output to the sum of $\lg(1/p_i)$, the [self-information](/self-information/) of the message under the model. For a memoryless source with the true model, its expected value is $n H(X) + 2$ at most, where $H$ is the [Shannon entropy](/shannon-entropy/).

## The algorithm

The registers have $b$ bits (here $b = 32$). Let $Q = 2^{b-2}$, $H = 2Q$, and let the totals satisfy $T \le T_{\max} \le Q$. The state $[low, high]$ holds integer ends, and $high$ stands for $high$ followed by an endless run of ones.

```pseudo id=main
ENCODE(x[1..n], model)
L1  low ← 0, high ← 2^b − 1, pending ← 0
L2  for i ← 1 to n do
L3      (c_lo, c_hi, T) ← the counts of x[i] in model
L4      r ← high − low + 1
L5      high ← low + ⌊r · c_hi / T⌋ − 1
L6      low ← low + ⌊r · c_lo / T⌋
L7      loop
L8          if high < H then EMIT(0)                                  ▷ E1: lower half
L9          else if low ≥ H then EMIT(1), low ← low − H, high ← high − H    ▷ E2: upper half
L10         else if low ≥ Q and high < 3Q then pending ← pending + 1, low ← low − Q, high ← high − Q    ▷ E3: middle half
L11         else exit the loop
L12         low ← 2 · low, high ← 2 · high + 1
L13     update model with x[i]
L14 pending ← pending + 1
L15 if low < Q then EMIT(0) else EMIT(1)

EMIT(bit)
L16 output bit, then pending copies of 1 − bit, and set pending ← 0

DECODE(code, n, model)
L17 low ← 0, high ← 2^b − 1, value ← the first b bits of code (0 past the end)
L18 for i ← 1 to n do
L19     r ← high − low + 1
L20     t ← ⌊((value − low + 1) · T − 1) / r⌋
L21     s ← the symbol with c_lo(s) ≤ t < c_hi(s)
L22     high ← low + ⌊r · c_hi(s) / T⌋ − 1, low ← low + ⌊r · c_lo(s) / T⌋
L23     loop: the same tests as lines L8 to L11, and in E2 and E3 subtract H or Q from value too
L24         low ← 2 · low, high ← 2 · high + 1, value ← 2 · value + the next bit of code
L25     update model with s, output s
```

Lines L5 and L6 cut the current range in proportion to the counts. The loop of line L7 keeps the range wider than $Q$. E1 and E2 are the cases where the first bit is known. E3 is the underflow case: the range straddles the middle and fits in the middle half, so the next bit is still unknown, but it will be the opposite of the bit after it. The coder records this in `pending`, and EMIT writes the deferred bits after the next known bit. Lines L14 and L15 write two more bits (plus the pending ones) that pick a quarter of the scale inside the final range, so every continuation of the code stays in the range, and the decoder may read zeros past the end.

The decoder keeps $value$, a window of $b$ code bits that it moves in step with the encoder. Line L20 finds the count $t$ that $value$ points at. Line L21 searches the model for it, which takes $O(\sigma)$ with a plain array and $O(\log \sigma)$ with a [Fenwick tree](/fenwick-tree/).

The model in the implementation is adaptive: each count starts at 1, gets 1 after each coded symbol, and all counts are halved, rounding up, when $T$ reaches $T_{\max} = 2^{16} - 1$. Witten, Neal and Cleary end the message with an extra end-of-file symbol. The implementation passes the length $n$ instead. This changes the framing only.

## Example

Code "abaca" over $\Sigma = \{a, b, c\}$ with the adaptive model and $b = 32$. The table shows the probability of each symbol at its turn, the scaling steps, the registers after them, and the bits written so far.

| symbol | $p$ | steps | low | high | output | pending |
|---|---|---|---|---|---|---|
| a | 1/3 | E1 | 0x00000000 | 0xAAAAAAA9 | 0 | 0 |
| b | 1/4 | E1, E2 | 0x55555554 | 0xFFFFFFFB | 001 | 0 |
| a | 2/5 | E3 | 0x2AAAAAA8 | 0xB333332D | 001 | 1 |
| c | 1/6 | E2, E1 | 0x71C71C5C | 0xCCCCCCB7 | 001100 | 0 |
| a | 3/7 | E3, E3 | 0x471C7170 | 0xE326320B | 001100 | 2 |

The exact interval of the message is $[7/36, 62/315)$, of width $\frac13 \cdot \frac14 \cdot \frac25 \cdot \frac16 \cdot \frac37 = \frac{1}{420}$, so the ideal length is $\lg 420 \approx 8.71$ bits. At the end, line L14 makes pending 3, and $low \ge Q = \texttt{0x40000000}$, so line L15 writes 1 and three zeros. The code is the 10 bits 0011001000, the fraction $0.0011001_2 = 0.1953125$. Every number that starts with these bits lies in $[0.1953125, 0.1962890625)$, which is inside $[7/36, 62/315) \approx [0.19444, 0.19683)$.

## Correctness

The proof tracks the map from the original unit interval to the scaled registers. Each scaling step is a change of coordinates $y \mapsto 2y - a$ with $a \in \{0, \tfrac14, \tfrac12\}$. With $u$ the bits written and $m$ the pending count, the map is $\varphi(C) = 2^m(2^{|u|} C - u) - (2^m - 1)/2$, and this invariant shows that an E1 or E2 step writes exactly the bits that the pending E3 steps deferred. The intervals in original coordinates are nested, and the final two bits pick a dyadic interval inside the last one. The decoder's $value$ is $\lfloor 2^b \varphi(C) \rfloor$, so it lies in $[low, high]$, and line L20 finds the unique symbol whose subinterval holds it. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/) with words of at least $2b$ bits for the product $r \cdot c$.

- **Code length.** Let $L$ be the number of output bits. Each scaling step adds exactly one output bit, and lines L14 and L15 add 2, so $L = S + 2$ for $S$ steps. Lemma 1 of the proof gives $r > Q$ before each symbol. The new width is then more than $r p_i - 1 \ge r p_i (1 - T_{\max}/Q)$, so
$$L \le \sum_{i=1}^{n} \lg \frac{1}{p_i} + 2 + n \lg \frac{1}{1 - T_{\max}/Q}.$$
With $b = 32$ and $T_{\max} = 2^{16} - 1$, the last term is less than $8.81 \times 10^{-5}$ bits per symbol. With exact arithmetic the last term is 0, and the bound is the one of [Shannon-Fano-Elias coding](/shannon-fano-elias-coding/).
- **Time.** Each symbol costs a constant number of word operations for lines L4 to L6 plus the model. Each step of the loop writes one bit, so the steps cost $\Theta(m)$ in total, where $m$ is the output length. With the linear search of the implementation, the model costs $\Theta(\sigma)$ per symbol. So the time is $\Theta(n \sigma + m)$ in each case. A Fenwick tree makes the model cost $O(\log \sigma)$.
- **Space.** $\Theta(\sigma)$ for the counts, and $O(1)$ words for the coder.

## Properties

- **Deterministic and online.** The encoder writes each bit as soon as it is known, and the decoder needs only the next $b$ bits.
- **Separates model and coder.** The coder accepts any counts with $f(s) \ge 1$ and $T \le T_{\max}$ at each step, so the model may change after every symbol.
- **Not a prefix code per symbol.** The output bits do not split into codewords. A single bit error spoils the rest of the message.

## Variants and improvements

- **Range coding.** [Range coding](/range-coding/) is the same interval method with byte output and a renormalization that works on bytes. It handles the underflow case with a carry instead of pending bits.
- **Low and range form.** Moffat, Neal and Witten (1998) keep $low$ and the width $r$ instead of $high$, replace the two divisions by one, and handle a carry into the written bits. Their coder allows larger totals for the same register size.
- **Binary coders.** The Q-coder, the MQ-coder of JPEG 2000 and the M coder of [CABAC](/cabac/) code only two symbols and replace the multiplication by a table.
- **Asymmetric numeral systems.** [ANS](/asymmetric-numeral-systems/) reaches a similar compression with one integer state and no multiplication by the range in the decoder, but it decodes in the reverse order of encoding.

## When to use it

Use arithmetic coding when the model gives probabilities far from powers of $\tfrac12$, for example a skewed binary source, or when the model changes after each symbol, as in [PPM](/prediction-by-partial-matching/), [context mixing](/context-mixing/) and [context tree weighting](/context-tree-weighting/). A [Huffman code](/huffman-coding/) with table lookups is faster for a fixed model with a large alphabet and moderate skew. rANS and tANS are faster for a static model.

## Pitfalls

- **Overflow of the product.** Line L5 computes $r \cdot c_{hi}$, which needs up to $b + \lg T_{\max}$ bits. With $b = 32$ in C, the product needs a 64-bit type.
- **A total too large.** If $T > Q$, the width $\lfloor r c_{hi}/T \rfloor - \lfloor r c_{lo}/T \rfloor$ can be 0 for a rare symbol, and the coder fails. Halve the counts before $T$ reaches $T_{\max} \le Q$.
- **Dropping the final bits.** Line L15 must write one bit and all pending bits. A coder that only flushes `pending` and forgets the deciding bit decodes wrongly at the end.
- **A model that is not mirrored.** The decoder must update its model at line L25 in exactly the same way and at the same time as line L13. An update before the coding step in one and after it in the other gives garbage.
- **The order of operations in line L20.** The formula is $\lfloor ((value - low + 1) T - 1)/r \rfloor$. The form $\lfloor (value - low) T / r \rfloor$ can point one count too low, because the encoder rounds the boundaries down. For example, with $r = 3$, $T = 2$ and $value - low = 1$, the second symbol starts at offset $\lfloor 3 \cdot 1 / 2 \rfloor = 1$, so the right count is $t = 1$, but the wrong form gives 0.

## Implementations

## History

The [Shannon-Fano-Elias code](/shannon-fano-elias-coding/) already uses the cumulative probability of a message as its code word, but to compute it for a long message one symbol at a time needs a precision that grows with the message. In 1976 Rissanen, in the IBM Journal, and Pasco, in his Stanford thesis, independently showed coders with finite precision. Rissanen and Langdon (1979, 1981) developed the method at IBM and separated modeling from coding. The paper of Witten, Neal and Cleary in Communications of the ACM (1987) gave a complete C program with the underflow handling by pending bits, and it made the method widely known. Moffat, Neal and Witten (1998) revised the design for speed and for larger alphabets.

## References
