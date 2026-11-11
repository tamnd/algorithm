---
tag: 4JH8SV
kind: algorithm
slug: asymmetric-numeral-systems
name: Asymmetric numeral systems
aliases:
- ANS
area: compression-and-coding/entropy-coding
level: research
summary: An entropy coder whose whole state is one natural number x; coding a symbol of probability p takes x to about x/p, and decoding runs in reverse order. This page gives the binary uABS form.
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {n: the number of symbols, m: the length of the output, w: the word length}
  time: {worst: Θ(n + n m / w), average: Θ(n + n m / w), best: Θ(n + n m / w)}
  space: {extra: Θ(1 + m / w)}
properties: {deterministic: true, online: false, recursive: false, comparison: false}
history:
  year: 2009
  people: [Jarek Duda]
  note: Duda put the first ANS paper on arXiv in 2009 and the paper with the rANS and tANS forms in 2013; Zstandard, LZFSE and JPEG XL use ANS coders.
prereqs: [shannon-entropy, arithmetic-coding]
see_also: [rans-coding, tabled-asymmetric-numeral-systems, range-coding, huffman-coding, zstandard, lossless-compression]
sources:
  - url: https://arxiv.org/abs/0902.0271
    title: Jarek Duda, Asymmetric numeral systems, arXiv 0902.0271, 2009
    locator: the whole paper (the state as a natural number, the coding and decoding functions, the binary uniform case)
  - url: https://arxiv.org/abs/1311.2540
    title: "Jarek Duda, Asymmetric numeral systems: entropy coding combining speed of Huffman coding with compression rate of arithmetic coding, arXiv 1311.2540, 2013"
    locator: the sections on uABS, on the range variant rANS, on the tabled variant tANS with streaming in the interval [L, 2L), and on the loss from quantized probabilities
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 5.4 (the expected length of a code built for the wrong distribution, H(p) plus the relative entropy D(p||q))
---

Asymmetric numeral systems (ANS) is a family of entropy coders for [lossless compression](/lossless-compression/) in which the whole state of the coder is one natural number $x$. Coding a symbol $s$ of probability $p_s$ maps $x$ to a number $C(s, x) \approx x / p_s$, so the state grows by about $\lg(1/p_s)$ bits, the [self-information](/self-information/) of $s$. Decoding applies the inverse map $D$ and gets the symbols back in the reverse order. Like [arithmetic coding](/arithmetic-coding/), ANS reaches a length within a small constant of the sum of $\lg(1/p_s)$. Unlike it, the decoder needs no interval with two ends, which makes a single table lookup or one multiplication per symbol enough. This page explains the idea with uABS, the uniform binary form, in exact arithmetic. The streaming forms have their own pages: [rANS](/rans-coding/) and [tANS](/tabled-asymmetric-numeral-systems/).

## In plain words

Writing a number in base two adds one binary digit for each step, and each digit has two equally likely values. ANS does the same with unequal values. It deals out all whole numbers to the symbols, in proportion to how likely each symbol is, as evenly as it can. To add a symbol to the state, the coder moves to the next number that belongs to that symbol, counted in the right place. A likely symbol owns many numbers, so the state grows a little. A rare symbol owns few, so the state grows a lot.

To read a symbol back, look at which symbol owns the current number, and count how many numbers of that symbol come before it. That count is the old state. The last symbol coded is the first one read back, like a stack.

## The problem

The input is a message $s_1 \ldots s_n$ over an alphabet $\Sigma$ with a probability $p_s > 0$ for each symbol. On this page $\Sigma = \{0, 1\}$, the probability of a 1 is $p$ with $0 < p < 1$, and $q = 1 - p$. The source model is memoryless (iid) with known $p$. The output is a natural number $X$, written in binary, from which the decoder, given $n$, $p$ and the start state $x_0$, gets the message back. The length is compared to the sum of $\lg(1/p_{s_i})$, whose expected value is $n$ times the [Shannon entropy](/shannon-entropy/) $h(p)$.

## The algorithm

General ANS fixes, for each symbol $s$, the set of states $y$ that hold $s$, with density close to $p_s$. $C(s, x)$ is the state of rank $x$ in the set of $s$, counted from 0, and $D(y)$ returns the symbol whose set holds $y$ and the rank of $y$ in that set. uABS takes the sets that are spread as evenly as possible: the state $y$ holds a 1 when the sequence $\lceil yp \rceil$ steps up at $y$.

```pseudo id=main
C(s, x)                                     ▷ the coding function
L1  if s = 1 then return ⌊x / p⌋
L2  else return ⌈(x + 1) / q⌉ − 1

D(y)                                        ▷ the decoding function
L3  s ← ⌈(y + 1) p⌉ − ⌈y p⌉
L4  if s = 1 then return (1, ⌈y p⌉)
L5  else return (0, y − ⌈y p⌉)

ENCODE(s[1..n], x0)
L6  x ← x0
L7  for i ← n down to 1 do x ← C(s[i], x)
L8  return x

DECODE(x, n, x0)
L9  for i ← 1 to n do (s[i], x) ← D(x)
L10 check that x = x0, then return s[1..n]
```

Line L3 tells which symbol the state $y$ holds. There are $\lceil yp \rceil$ states below $y$ that hold a 1 and $y - \lceil yp \rceil$ that hold a 0, so lines L4 and L5 return the rank of $y$ among the states of its symbol. Lines L1 and L2 solve this for $y$: they find the state of rank $x$ among the states of $s$.

The coder is last in, first out. ENCODE codes the message from the end, so that DECODE, which reads from the top of the state, returns it in the original order. The start state $x_0$ is a fixed number known to both sides, and the decoder must also know $n$. The final check at line L10 detects some damaged inputs.

**Streaming.** The exact state grows without bound. Practical coders keep $x$ in an interval $I = [L, bL)$, for example with $b = 2$ or $b = 256$. Before coding $s$, the encoder writes the low base-$b$ digits of $x$ and divides $x$ by $b$ until $C(s, x)$ falls in $I$. After $D$, the decoder reads digits back while $x < L$. This works when the set of $x$ with $C(s, x) \in I$ has the form $[k, bk)$ for each $s$, so that exactly one number of divisions by $b$ reaches it. The two common designs choose $C$ to make this true:

- **rANS** uses the range layout $C(s, x) = \lfloor x / f_s \rfloor M + c_s + (x \bmod f_s)$, with integer frequencies $f_s$ summing to $M$ and $c_s$ their prefix sums. It needs one multiplication and one division to encode, and one multiplication to decode. See [rANS](/rans-coding/).
- **tANS** fixes $L$ states, spreads the symbols over them by a rule, and stores $C$ and $D$ for the whole interval in tables. Coding a symbol is a table lookup and a shift. See [tANS](/tabled-asymmetric-numeral-systems/).

## Example

Take $p = 3/10$. Line L3 gives the symbols of the states 0 to 20:

| $y$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $s(y)$ | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |

Three in each ten states hold a 1. Code the message 0 1 0 0 1 0 from $x_0 = 1$. ENCODE takes the symbols from the end: $C(0, 1) = 2$, $C(1, 2) = 6$, $C(0, 6) = 9$, $C(0, 9) = 14$, $C(1, 14) = 46$, $C(0, 46) = 67$. The output is $X = 67$, which is 7 bits in binary. DECODE starts at 67: $D(67) = (0, 46)$, $D(46) = (1, 14)$, $D(14) = (0, 9)$, $D(9) = (0, 6)$, $D(6) = (1, 2)$, $D(2) = (0, 1)$. It returns 0 1 0 0 1 0 and ends at the start state 1.

The ideal length is $2 \lg(10/3) + 4 \lg(10/7) \approx 5.53$ bits, and $\lg 68 \approx 6.09$. The difference includes $\lg 2 = 1$ bit for the start state, which a streaming coder pays once per stream.

## Correctness

Count the states below $y$ that hold each symbol: the sum of the symbols from 0 to $y - 1$ telescopes to $\lceil yp \rceil$. So $D(y)$ gives the symbol of $y$ and its rank among the states of that symbol. Each symbol owns infinitely many states, so $D$ is a bijection from the natural numbers onto pairs of a symbol and a rank. A short computation with floors and ceilings shows that $C(s, x)$ of lines L1 and L2 is the state of rank $x$ that holds $s$, so $D(C(s, x)) = (s, x)$. DECODE then undoes the steps of ENCODE one by one, from the last to the first. The full proof is in [the correctness proof](#proof-correctness).

## Complexity

Model: [word RAM](/word-ram/) with $w$-bit words, and exact integers of many words for the state.

- **Code length.** Let $X$ be the output. The proof shows that a step with a 1 multiplies $x + 1$ by at most $1/p$, and a step with a 0 multiplies it by at most $(1/q)(1 + q/(x+1))$. The extra factors form a geometric series, so
$$\lg(X + 1) \le \lg(x_0 + 1) + \sum_{i=1}^{n} \lg \frac{1}{p_{s_i}} + \frac{q}{p\,(x_0 + 1) \ln 2}.$$
The excess is a constant that does not depend on $n$. On 16000 bits with $p = 0.3$ from a fixed seed, the implementation measured 1.68 bits above the ideal length.
- **Time.** The exact form makes $n$ steps on a state of up to $m$ bits, and each step multiplies or divides by a fixed fraction, which costs $O(m / w)$ word operations. So the time is $\Theta(n + n m / w)$. The streaming forms keep $x$ in one word and cost $O(1)$ per symbol.
- **Space.** $\Theta(1 + m/w)$ words for the state.

The streaming forms quantize the probabilities to $f_s / M$ or to counts out of $L$ states. If the coder uses $q_s$ in place of the true $p_s$, the expected cost per symbol is $H(p) + D(p \| q)$, the entropy plus the relative entropy of the true and the coded distribution. Duda (2013) also analyses the loss of the tabled form from a spread that is not perfectly even, which falls as the number of states grows.

## Properties

- **Last in, first out.** The decoder returns the symbols in the reverse order of encoding. An adaptive model must therefore run forward in a first pass, store its probabilities, and the encoder then codes backward. This is why ANS is used mostly with static or block-wise models.
- **One number of state.** The state is one integer. Several independent states can work on interleaved symbols, which suits SIMD and GPU code (see [rANS](/rans-coding/)).
- **Not online in the exact form.** ENCODE must see the whole message before it outputs anything. Streaming coders output in blocks.

## Variants and improvements

- **uABS.** The binary form of this page, with even spreading. Its streaming form is a binary coder with one multiplication per bit.
- **rABS and rANS.** The range form, binary or for any alphabet, is the most used form in software. See [rANS](/rans-coding/).
- **tANS.** The tabled form, as in Zstandard. See [tANS](/tabled-asymmetric-numeral-systems/).

## When to use it

Use ANS when a static or block-wise model drives an entropy coder and decoding speed matters: tANS or rANS decode as fast as a table-driven [Huffman](/huffman-coding/) decoder and reach the compression of arithmetic coding. Use [arithmetic coding](/arithmetic-coding/) or [range coding](/range-coding/) when the model adapts after each symbol, because then the reverse order of ANS forces a second pass.

## Pitfalls

- **The order.** Encoding the message front to back and decoding it front to back returns the reverse. Code backward, or reverse the output.
- **The end of the message.** $X$ alone does not tell where the message ends: $D(0) = (1, 0)$, and from a small state the decoder can go on returning symbols. Send $n$, or code an end symbol. Streaming coders start at $L$ and stop when the input and the state are both used up.
- **Probabilities of 0 or 1.** A symbol with probability 0 owns no state and cannot be coded. Every symbol that occurs must keep a frequency of at least 1 after quantization.
- **Streaming without the right interval.** If the set of $x$ with $C(s, x) \in [L, bL)$ is not of the form $[k, bk)$, the decoder can read a wrong number of digits. rANS gets it from $L$ a multiple of $M$, and tANS from tables built for the interval.

## Implementations

## History

Duda put the first paper on asymmetric numeral systems on arXiv in 2009. It described the natural number state, the coding and decoding functions and the uniform binary case. His 2013 paper added the range variant and the tabled variant with the interval $[L, 2L)$, and compared them to Huffman and arithmetic coding. Yann Collet wrote the Finite State Entropy library, a fast tANS coder, in 2013, and it became the entropy coder of Zstandard. Fabian Giesen published a byte-wise and interleaved rANS coder in 2014. Apple's LZFSE uses tANS, and JPEG XL uses rANS.

## References
