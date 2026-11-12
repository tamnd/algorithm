---
tag: MHQMGE
kind: algorithm
slug: delta-encoding
name: Delta encoding
aliases:
- difference coding
- d-gap encoding
area: compression-and-coding/transforms-for-compression
level: intro
summary: Store the first value of a sequence and then the difference of each value from the one before it. Prefix sums undo it, and slowly changing data gives small numbers.
model: word-ram
complexity:
  vars: {n: the length of the sequence}
  time: {worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 2002
  people: [David G. Korn, Joshua P. MacDonald, Jeffrey C. Mogul, Kiem-Phong Vo]
  note: Differences of successive values were in use long before. RFC 3284 of 2002 (VCDIFF) gave a standard format for the delta of one file against another.
prereqs: [prefix-sums]
see_also: [difference-array, predictive-coding, variable-byte-encoding, elias-gamma-coding, pfor-delta, inverted-index, myers-diff, run-length-encoding]
sources:
  - paper: "RFC 3284, D. Korn, J. MacDonald, J. Mogul and K. Vo, The VCDIFF Generic Differencing and Compression Data Format, IETF, June 2002"
    title: RFC 3284, The VCDIFF Generic Differencing and Compression Data Format
    locator: Section 3, Delta Instructions (ADD, COPY and RUN, and the address space of the source followed by the target)
  - url: https://protobuf.dev/programming-guides/encoding/
    title: Protocol Buffers documentation, Encoding
    locator: the sections on base 128 varints and on signed integers (ZigZag encoding)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, 2nd edition, Morgan Kaufmann, 1999
    locator: Chapter 3, Indexing (the compression of inverted files by the gaps between document numbers; chapter number not checked)
---

Delta encoding stores a sequence of numbers as its first value followed by the difference of each value from the one before it. The sequence $1000, 1002, 1003, 1003, 1001$ becomes $1000, 2, 1, 0, -2$. The inverse is a running sum, a [prefix sum](/prefix-sums/), so both directions take one pass and $\Theta(n)$ time. Delta encoding does not make data smaller by itself. It turns values that change slowly, such as sensor readings, timestamps, sorted document numbers or audio samples, into small numbers, which a variable-length code such as [variable-byte encoding](/variable-byte-encoding/) or an [Elias gamma code](/elias-gamma-coding/) then stores in a few bits. The same name is also used for the difference of one file against another, which is a different method: it codes a new file as copies from an old file plus new bytes.

## In plain words

If a list of numbers changes only a little from one number to the next, write the first number, and after that only how much each number goes up or down. The changes are usually small numbers, and small numbers need fewer digits.

To get the list back, start from the first number and add each change in turn.

This works well for things like a temperature every minute, the time of each event in a log, or a sorted list of page numbers. It does not help when the numbers jump around without order: then the changes are as large as the numbers.

## The problem

**Input.** A sequence $X = X[0 \ldots n-1]$ of integers.

**Output.** The sequence $D$ with $D[0] = X[0]$ and $D[i] = X[i] - X[i-1]$ for $1 \le i < n$. The inverse returns $X[i] = D[0] + D[1] + \cdots + D[i]$.

## The algorithm

```pseudo id=main
DELTA-ENCODE(X[0 .. n − 1])
L1  prev ← 0
L2  for i ← 0 to n − 1 do
L3      D[i] ← X[i] − prev
L4      prev ← X[i]
L5  return D
```

```pseudo id=decode
DELTA-DECODE(D[0 .. n − 1])
D1  total ← 0
D2  for i ← 0 to n − 1 do
D3      total ← total + D[i]
D4      X[i] ← total
D5  return X
```

The start value $prev = 0$ makes $D[0] = X[0]$, so no special case is needed. Both loops can work in place.

**The codes that follow.** The differences can be negative. A common chain is delta, then *zigzag*, then *varint*:

- **Zigzag** maps the signed values $0, -1, 1, -2, 2, \ldots$ to $0, 1, 2, 3, 4, \ldots$: $v \mapsto 2v$ for $v \ge 0$ and $v \mapsto -2v - 1$ for $v < 0$. Small values of both signs become small unsigned values.
- **Varint** (LEB128) writes an unsigned value in groups of 7 bits, the low group first, and sets the high bit of each byte except the last. Values below 128 take one byte.

## Example

Readings of a sensor, once per minute: $1000, 1002, 1003, 1003, 1001, 998, 1000$. The deltas are $1000, 2, 1, 0, -2, -3, 2$. After zigzag, the six differences are $4, 2, 0, 3, 5, 4$, and each takes one varint byte, while each reading needs two bytes; the first value $1000$, zigzag $2000$, takes two.

**Document numbers.** In an [inverted index](/inverted-index/), the list of documents that hold a word is sorted, for example $3, 7, 11, 23, 29, 30$. Its d-gaps are $3, 4, 4, 12, 6, 1$. All gaps are positive, so no zigzag step is needed, and a common word has many small gaps.

**Varint.** The value 150 is `10010110` in binary. The low 7 bits are `0010110`, and the next group is `1`, so the bytes are `96 01` in hexadecimal, as in the Protocol Buffers documentation. Zigzag maps $-1$ to 1, $1$ to 2, $2147483647$ to $4294967294$, and $-2147483648$ to $4294967295$.

**Higher orders.** Delta encoding applied twice turns the ramp $5, 8, 11, 14, 17$ into $5, 3, 3, 3, 3$ and then $5, -2, 0, 0, 0$. Applied $k + 1$ times, it turns a polynomial of degree $k$ into zeros after the first $k + 1$ values.

## Correctness

The decoder inverts the encoder because the sum telescopes: $D[0] + \cdots + D[i] = X[0] + (X[1] - X[0]) + \cdots + (X[i] - X[i-1]) = X[i]$. The invariant of the loop of line L2 is $prev = X[i-1]$ (with $X[-1] = 0$), and the invariant of the decoder is $total = X[i-1]$ at the start of step $i$. The encoder also inverts the decoder, so the map is a bijection of integer sequences of length $n$. The full proof is below.

## Complexity

- **Time.** One subtraction for each value in the encoder and one addition for each value in the decoder: $\Theta(n)$.
- **Space.** $O(1)$ beyond the output, or none if the work is in place.
- **Range of the values.** If $0 \le X[i] < 2^b$, the differences lie in $(-2^b, 2^b)$, which needs $b + 1$ bits. To keep $b$ bits, compute the differences modulo $2^b$; the decoder then adds modulo $2^b$, and the result is still exact.

## Properties

- **Lossless and online.** Each difference needs only the previous value, and the decoder works value by value.
- **A special case of prediction.** Delta encoding predicts each value by the one before it and stores the error. [Predictive coding](/predictive-coding/) uses better predictors, such as a weighted sum of several earlier values.
- **The inverse of the prefix sum.** The [difference array](/difference-array/) of algorithm design is the same map, used to make range updates fast rather than to compress.
- **Errors spread.** A wrong difference changes every later value of the decoded sequence. Formats store a full value every so often to limit the damage and to allow random access.

## Variants and improvements

- **Modular deltas.** The Sub filter of PNG stores each byte minus the byte one pixel to the left, modulo 256, so the result stays one byte.
- **Delta of delta.** Time series stores code the difference of the differences, which is 0 when the samples arrive at a fixed rate. More generally, a delta of order $k$ is the fixed polynomial predictor of order $k$ used by lossless audio coders.
- **Frame of reference and patched coding.** [PFOR-delta](/pfor-delta/) codes blocks of d-gaps with a fixed bit width and handles the few large gaps as exceptions.
- **Delta of files.** VCDIFF (RFC 3284) codes a target file $T$ against a source file $S$ with three instructions: ADD, which gives new bytes; COPY, which gives a size and an address in the string $S$ followed by $T$; and RUN, which repeats one byte. A COPY that points into the part of $T$ made so far may overlap the bytes it produces, as in [LZ77](/lz77/). Line-based tools, such as diff with the [Myers algorithm](/myers-diff/), compute an edit script instead, and rsync finds the common blocks of two files on different machines with a rolling checksum.

## When to use it

Use delta encoding when neighboring values are close: sorted integer lists, timestamps, counters, slowly changing measurements, and the samples of smooth signals. Follow it by a code that is short for small values. Do not use it when the values are independent of each other, since the differences are then larger than the values; and do not use it on its own where random access is needed, unless you store a full value every so often.

## Pitfalls

- **Overflow.** In fixed-width integers, $X[i] - X[i-1]$ can overflow. Either use a wider type or compute modulo $2^b$ on both sides.
- **Negative differences with an unsigned code.** A varint of a negative number in two's complement takes the maximum length (10 bytes for 64 bits). Zigzag first.
- **The first value.** It is not a difference and is often much larger than the rest. Store it on its own, or let the code handle one large value.
- **Lossy coding of the differences.** If the differences are quantized, the errors add up in the decoder. A lossy coder must predict from the decoded values, not from the original ones; see [predictive coding](/predictive-coding/).
- **Unsorted lists.** d-gaps need a sorted list. A gap of zero or a negative gap means a duplicate or an error in the list.

## Implementations

## History

Differences of successive values are an old tool of numerical tables and of signal coding. Inverted file systems store the gaps between document numbers, and Witten, Moffat and Bell (Managing Gigabytes, 1994, second edition 1999) studied codes for these gaps. Version control systems such as SCCS and RCS store the versions of a file as deltas, and RFC 3284 (VCDIFF, 2002) by Korn, MacDonald, Mogul and Vo standardized a general format for the delta of one file against another. Protocol Buffers made the chain of zigzag and varint codes common in data formats.

## References
