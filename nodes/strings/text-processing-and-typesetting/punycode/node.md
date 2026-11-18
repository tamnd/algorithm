---
tag: S9VM2F
kind: algorithm
slug: punycode
name: Punycode
aliases:
- Bootstring encoding
area: strings/text-processing-and-typesetting
level: core
summary: "Encode a Unicode string as ASCII letters, digits and hyphens. The basic characters are copied, and the others are written as sorted insertions with deltas in a variable-length base 36 code."
model: word-ram
complexity:
  vars: {N: the number of code points of the string}
  time: {worst: Θ(N^2), best: Θ(N)}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [unicode-code-point, variable-length-code]
see_also: [utf-8, variable-byte-encoding, variable-length-code, unicode-normalization-forms, unicode-case-folding, unicode-confusable-detection, unicode-code-point]
sources:
  - url: https://www.rfc-editor.org/rfc/rfc3492
    title: "A. Costello, Punycode: A Bootstring encoding of Unicode for Internationalized Domain Names in Applications (IDNA), RFC 3492, March 2003"
    locator: "Section 3 (Bootstring description: 3.1 basic code point segregation, 3.2 insertion unsort coding, 3.3 generalized variable-length integers, 3.4 bias adaptation), Section 5 (parameter values), Section 6 (6.1 bias adaptation function, 6.2 decoding procedure, 6.3 encoding procedure, 6.4 overflow handling) and Section 7.1 (sample strings)"
  - url: https://docs.python.org/3/library/codecs.html#text-encodings
    title: Python documentation, codecs
    locator: Text Encodings (the punycode codec) and encodings.idna
---

Punycode writes a string of Unicode [code points](/unicode-code-point/) as a string of ASCII letters, digits and hyphens, so that a domain name such as bücher.example can travel through the DNS, which only allows those characters in host names. It copies the ASCII characters first and then describes where each other character goes and what its value is, as a sequence of insertions sorted by value. Each insertion is one number, a delta from the one before, and the numbers are written in a [variable-length](/variable-length-code/) base 36 code whose thresholds adapt to the size of the recent deltas. Adam Costello defined it in RFC 3492 (2003) as an instance of a general method called Bootstring.

## In plain words

Think of the name "bücher". The plain letters b, c, h, e and r can go into the result as they are. Only ü needs a description, and that description must use plain letters too.

Punycode writes "bcher", a hyphen, and then a short code for the instruction "put the character ü at place 1". It joins the value of ü and its place into one number, so that the description is a single number.

When a name has many special characters, Punycode puts them in order of their value and writes each one as the difference from the one before. These differences are usually small, so they take few letters. The letters work like digits in base 36, with a rule that tells where each number ends. So "bücher" becomes "bcher-kva", and with the prefix "xn--" it is the host name label "xn--bcher-kva".

## The problem

The input is a string $s$ of $N$ scalar values. A code point below 80 is *basic*. The output is a string of basic code points from which $s$ can be recovered, and the decoder does that recovery. It must reject inputs that no string encodes to.

The parameters of section 5 of RFC 3492 are: base 36, $t_{\min} = 1$, $t_{\max} = 26$, skew 38, damp 700, initial bias 72 and initial $n$ 128. The digit values 0 to 25 are the letters a to z, in either case, and 26 to 35 are the digits 0 to 9. The delimiter is "-".

The threshold for the digit at position $k = 36, 72, 108, \ldots$ of a number is

$$T(k, bias) = \begin{cases} 1 & \text{if } k \le bias, \\ 26 & \text{if } k \ge bias + 26, \\ k - bias & \text{otherwise.} \end{cases}$$

ADAPT$(\delta, count, first)$, from section 6.1, divides $\delta$ by 700 if $first$ and by 2 otherwise, adds $\delta \operatorname{div} count$, and then returns $36 k' + \lfloor 36 \delta' / (\delta' + 38) \rfloor$, where $k'$ counts how many times $\delta$ had to be divided by 35 to get a value $\delta'$ of at most 455.

## The algorithm

```pseudo id=main
PUNYCODE-ENCODE(s)
L1  out <- the basic code points of s, in order
L2  b <- |out|; h <- b; if b > 0 then append "-" to out
L3  n <- 128; delta <- 0; bias <- 72
L4  while h < |s| do
L5      m <- the least code point of s that is at least n
L6      delta <- delta + (m - n) * (h + 1); n <- m
L7      for each code point c of s, in order do
L8          if c < n then delta <- delta + 1
L9          if c = n then
L10             q <- delta; k <- 36; t <- T(k, bias)
L11             while q >= t do append DIGIT(t + (q - t) mod (36 - t)); q <- (q - t) div (36 - t); k <- k + 36; t <- T(k, bias)
L12             append DIGIT(q)
L13             bias <- ADAPT(delta, h + 1, h = b); delta <- 0; h <- h + 1
L14     delta <- delta + 1; n <- n + 1

PUNYCODE-DECODE(p)
L15 out <- the code points of p before its last "-", or nothing if that "-" is not after position 0; pos <- the index of the first code point after them and the "-"
L16 n <- 128; i <- 0; bias <- 72
L17 while pos < |p| do
L18     oldi <- i; w <- 1; k <- 36
L19     loop: fail if pos = |p|; d <- VALUE(p[pos]); pos <- pos + 1
L20         i <- i + d * w; t <- T(k, bias)
L21         if d < t then exit the loop; w <- w * (36 - t); k <- k + 36
L22     bias <- ADAPT(i - oldi, |out| + 1, oldi = 0)
L23     n <- n + i div (|out| + 1); i <- i mod (|out| + 1)
L24     insert n into out at index i; i <- i + 1
```

The encoder returns $out$ when the loop of line L4 ends, and the decoder returns $out$ when the loop of line L17 ends.

**Insertion unsort coding (section 3.2).** The decoder keeps a state $(n, i)$: the value of the next code point to insert and the index where it goes. One delta moves the state forward. The index runs fastest and the value slowest, so a delta of $\delta$ from $(n, i)$ in a string of $h$ code points means "skip $\delta$ places in the list of all pairs (value, index), where each value has $h + 1$ indexes". Line L23 turns the skipped count back into a value and an index. The encoder produces the same count by scanning $s$ once per value (lines L7 to L9) and counting the code points that are already in the decoder's string.

**Generalized variable-length integers (section 3.3).** A delta is written least significant digit first. A digit below its threshold $t$ is the last digit, so the code needs no separator. The weight of each digit is the product of $36 - t$ over the earlier digits.

**Bias adaptation (section 3.4).** After each delta, ADAPT sets the bias so that the thresholds fit the size of the next delta. The first delta is usually large, since it carries the distance from 128 to the first value, so it is damped by 700 instead of 2.

**Checks.** The decoder fails on a non-basic code point before the delimiter, on a character that is not a digit, on input that ends inside a number (line L19), and on an overflow of 32-bit unsigned integers (section 6.4). The implementation also rejects a decoded value that is basic, a surrogate or above 10FFFF.

## Example

Encode "bücher". Line L1 gives "bcher", so $b = h = 5$, and line L2 appends "-". Line L5 finds $m = \mathtt{FC}$ (ü), and line L6 sets $\delta = (252 - 128) \cdot 6 = 744$. The scan meets b, which is below FC, so $\delta = 745$, and then ü.

| digit position $k$ | threshold $t$ | $q$ | digit value | character |
|---|---|---|---|---|
| 36 | 1 | 745 | $1 + 744 \bmod 35 = 10$ | k |
| 72 | 1 | $744 \operatorname{div} 35 = 21$ | $1 + 20 \bmod 35 = 21$ | v |
| 108 | 26 | $20 \operatorname{div} 35 = 0$ | 0 | a |

The bias is 72 for the first delta, so the thresholds are 1, 1 and 26. The output is "bcher-kva".

Decode it. Line L15 gives "bcher". The digits k, v and a have the values 10, 21 and 0 and the weights 1, 35 and $35^2$, so $i = 10 + 21 \cdot 35 = 745$, and a stops the number because $0 < 26$. Line L23 sets $n = 128 + 745 \operatorname{div} 6 = 252$ and $i = 745 \bmod 6 = 1$, and line L24 inserts U+00FC at index 1. The result is "bücher". The tests also check "münchen" (mnchen-3ya), "mañana" (maana-pta) and the 12 samples of section 7.1 that have no mixed-case annotation.

## Correctness

The proof in proofs/correctness.md has three steps. First, if the decoder inserts the non-basic code points in the order of (value, position), each at the index equal to the number of code points already placed before it, it rebuilds $s$. Second, the delta that line L10 writes is exactly the one that moves the decoder state from one insertion to the next: line L6 counts the values skipped, times the number of indexes per value, and the scan counts the placed code points before each position. Third, the variable-length code of lines L10 to L12 and lines L18 to L21 is a bijection, as long as both sides use the same thresholds, and they do, because they call ADAPT with the same arguments. Digits are never "-", so the last "-" of the output separates the basic code points from the digits.

## Complexity

In the [word-RAM model](/word-ram/), with $N$ code points of which $N - b$ are not basic, the encoder does one scan of $s$ for each distinct non-basic value, plus a scan in line L5 to find it, so it takes $O(N (N - b + 1))$ time. Each delta fits in 32 bits, and line L11 divides it by at least 10 for each digit, so it has at most 11 digits. The decoder inserts into an array, which costs $O(N)$ per insertion. Both are $\Theta(N^2)$ in the worst case and $\Theta(N)$ when all code points are basic.

| claim | value |
|---|---|
| encoding time | $O(N (N - b + 1))$ |
| decoding time | $O(N (N - b + 1))$ with an array |
| digits per delta | at most 11 for 32-bit deltas |

A DNS label has at most 63 octets, so $N$ is small in practice, and the quadratic bound does not matter there.

## Properties

- **Injective.** Different strings give different outputs, and the decoder inverts the encoder.
- **Basic code points first.** The ASCII part of the label stays readable, as in "bcher-kva".
- **Not unique on input to the decoder.** The decoder accepts digits in either case, so "maana-PTA" also decodes to "mañana". A label must be compared after a round trip through the decoder and the encoder, or in lowercase.
- **Compact.** Sorted insertions with adaptive thresholds give short outputs for text in one script, because the values of such text lie close together.

## Variants and improvements

- **Bootstring.** Section 3 defines the method for any set of parameters: the base, the thresholds, the damping and the initial values. Punycode is one choice of them, tuned for domain names.
- **Mixed-case annotation.** Appendix A of RFC 3492 lets the case of each final digit carry a hint about the case of the code point. IDNA does not use it, and the implementation writes lowercase digits.
- **Faster decoding.** A balanced tree or a [rope](/rope/) for $out$ makes each insertion $O(\log N)$, which makes decoding $O(N \log N)$ besides the digit reading.

## When to use it

Use Punycode to turn an internationalized domain name label into the "xn--" form that DNS, TLS certificates and mail headers carry. Punycode is only the last step of that process. IDNA2008 (RFC 5891) or UTS 46 first map and check the label, with [normalization](/unicode-normalization-forms/) to NFC and, in UTS 46, [case folding](/unicode-case-folding/), and then each label is encoded. For general text in ASCII channels, use UTF-8 with a transfer encoding instead. Punycode is not designed for long strings.

## Pitfalls

- **Overflow.** A crafted label can make $i$ or $w$ exceed 32 bits. The decoder must check before each multiplication and addition, as section 6.4 shows. The test `test_overflow_is_detected` checks this.
- **Truncated numbers.** A label that ends with a digit at or above its threshold is invalid. The test `test_bad_input` checks this and other bad inputs.
- **A delimiter at the start.** If the only "-" is at position 0, there are no basic code points, and the "-" is read as a digit, which fails. "-" itself is not a valid label.
- **Case.** Uppercase and lowercase digits have the same value, but basic code points keep their case. The test `test_decoder_accepts_uppercase_digits` checks this.
- **Skipping the IDNA checks.** Encoding a label without the mapping and validity checks of IDNA allows labels that look like other labels. See [confusable detection](/unicode-confusable-detection/). Python's "idna" codec implements the older IDNA2003, not IDNA2008, so the tests use the "punycode" codec as the oracle.

## Implementations

## History

The IETF worked on internationalized domain names in the early 2000s, and several ASCII-compatible encodings were proposed. Adam Costello's Punycode was chosen, and it was published in March 2003 as RFC 3492, together with RFC 3490 (IDNA) and RFC 3491 (Nameprep). The revised protocol of 2010, IDNA2008 (RFC 5890 to RFC 5894), replaced Nameprep with new rules but kept Punycode and the "xn--" prefix.

## References
