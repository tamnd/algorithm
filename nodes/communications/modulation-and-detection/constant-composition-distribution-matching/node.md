---
tag: EKQBW6
kind: algorithm
slug: constant-composition-distribution-matching
name: Constant composition distribution matching
aliases:
- CCDM
area: communications/modulation-and-detection
level: research
summary: Maps uniform bits to amplitude sequences of a fixed type by arithmetic coding, giving the target distribution for probabilistic shaping.
model: word-ram
complexity:
  vars: {n: the output length in symbols, M: the number of output symbols (amplitudes), w: the word size in bits}
  time: {worst: O(M n² log M / w)}
  space: {extra: O(n log M / w)}
properties: {deterministic: true, invertible: true, fixed_length: true, constant_composition: true}
history:
  year: 2016
  people: [Patrick Schulte, Georg Böcherer]
  note: Schulte and Böcherer used a constant composition code with arithmetic coding as a fixed-length distribution matcher, and showed that its rate approaches the entropy of the target distribution.
prereqs: [arithmetic-coding, multinomial-coefficient, kullback-leibler-divergence, shannon-entropy]
see_also: [probabilistic-constellation-shaping, arithmetic-coding, enumerative-coding, multiset-permutations, combinatorial-ranking-and-unranking, pulse-amplitude-modulation, ldpc-code, arbitrary-precision-arithmetic]
sources:
  - paper: doi:10.1109/TIT.2015.2499181
    title: Patrick Schulte and Georg Böcherer, Constant composition distribution matching, IEEE Transactions on Information Theory 62(1), 430-434, 2016
    locator: the choice of the output type, the arithmetic coding encoder and decoder, and the rate and divergence results
  - paper: doi:10.1109/TCOMM.2015.2494016
    title: Georg Böcherer, Fabian Steiner and Patrick Schulte, Bandwidth efficient and rate-matched low-density parity-check coded modulation, IEEE Transactions on Communications 63(12), 4651-4665, 2015
    locator: probabilistic amplitude shaping, where a distribution matcher produces the amplitudes
---

Constant composition distribution matching (CCDM) turns a block of $k$ uniform bits into a block of $n$ symbols, each word with the same number of copies of each symbol. The fixed counts, the composition, are chosen so that the word's symbol frequencies match a target distribution. In [probabilistic constellation shaping](/probabilistic-constellation-shaping/), the symbols are the amplitudes of an ASK constellation, and the target gives small amplitudes more often than large ones. The map is one-to-one, so the receiver gets the bits back with the inverse map. The encoder is an [arithmetic coder](/arithmetic-coding/) run backwards, in which each output symbol has the probability "copies left divided by symbols left". With exact integers this is the same as picking the word of a given rank among all words of the composition, which is what this page does.

## In plain words

Think of a bag with 4 tiles marked "1", 3 marked "3", 2 marked "5" and 1 marked "7". Every way of drawing all 10 tiles in a row is a possible output, and all outputs contain each mark the same number of times. There are 12600 such rows. The matcher numbers the rows in dictionary order and uses the incoming bits to pick one, spread evenly over the list. The receiver finds the number of the row it received and turns it back into the bits. Because every row has many 1s and few 7s, the signal uses little energy. The cost is that 13 bits pick among only 12600 rows, fewer bits than the symbols could carry with no rule.

## The problem

The input is $k$ independent uniform bits. The output alphabet is $a_1 < a_2 < \cdots < a_M$ and the target distribution is $P$ on it. Choose counts $c = (c_1, \ldots, c_M)$ with $\sum_s c_s = n$, and let $\mathcal{T}_c$ be the set of words of length $n$ in which $a_s$ appears exactly $c_s$ times. It has

$$T = |\mathcal{T}_c| = \frac{n!}{c_1!\, c_2! \cdots c_M!}$$

words (a [multinomial coefficient](/multinomial-coefficient/)). With $k = \lfloor \log_2 T \rfloor$, find an injective map $f : \{0, 1\}^k \to \mathcal{T}_c$ and its inverse on the image, both fast. The rate is $k/n$ bits per symbol. Schulte and Böcherer choose $c/n$ as the type of length $n$ with the smallest [divergence](/kullback-leibler-divergence/) $D(c/n \,\|\, P)$; the rate can then come close to the entropy $H(P)$ for large $n$.

## The algorithm

Order the words of $\mathcal{T}_c$ by dictionary order of the symbol indices. The number of words that start with $a_s$ is $T c_s/n$, since fixing the first symbol leaves a word of length $n - 1$ with one copy of $a_s$ less. The encoder turns the bits into an integer $v$, spreads it over the $T$ ranks, and unranks. The decoder ranks and divides back.

```pseudo id=main
CCDM-ENCODE(u_1..u_k, c_1..c_M, a_1..a_M)
L1   n ← Σ_s c_s ;  T ← n! / (c_1! ··· c_M!) ;  k ← ⌊log₂ T⌋
L2   v ← Σ_t u_t · 2^(k-t)                      ▷ the bits as an integer, first bit most significant
L3   r ← ⌈v · T / 2^k⌉                          ▷ 0 ≤ r < T
L4   N ← T                                      ▷ the number of words that are still possible
L5   for ℓ ← n down to 1                        ▷ ℓ symbols are still to place
L6       for s ← 1 to M with c_s > 0
L7           N_s ← N · c_s / ℓ                  ▷ an exact integer
L8           if r < N_s then  x_{n-ℓ+1} ← a_s ;  c_s ← c_s - 1 ;  N ← N_s ;  go to the next ℓ
L9           r ← r - N_s
L10  return x_1..x_n

CCDM-DECODE(x_1..x_n, c_1..c_M)                  ▷ T and k as in L1
L11  r ← 0 ;  N ← T ;  ℓ ← n
L12  for t ← 1 to n, with x_t = a_q
L13      for s ← 1 to q - 1:  r ← r + N · c_s / ℓ
L14      N ← N · c_q / ℓ ;  c_q ← c_q - 1 ;  ℓ ← ℓ - 1
L15  v ← ⌊r · 2^k / T⌋ ;  return the k bits of v
```

Line L3 picks the smallest rank $r$ with $r \ge v T/2^k$. In the arithmetic coder of the paper, this is the lowest output interval whose lower end lies in the input interval of $v$. Since $T \ge 2^k$, the ranks of different $v$ differ by at least one, and line L15 recovers $v$.

## Example

**A short block.** Take $n = 5$, the amplitudes $1, 3, 5$ and $c = (2, 2, 1)$. Then $T = 5!/(2!\,2!\,1!) = 30$ and $k = 4$, so 16 of the 30 words are used. The input 1011 gives $v = 11$ and $r = \lceil 11 \cdot 30/16 \rceil = \lceil 20.625 \rceil = 21$. Unranking:

| $\ell$ | $N$ | $c$ before | counts $N c_s/\ell$ tried | $r$ after | symbol |
|---|---|---|---|---|---|
| 5 | 30 | (2, 2, 1) | 12 (skip), 12 (take) | 9 | 3 |
| 4 | 12 | (2, 1, 1) | 6 (skip), 3 (skip), 3 (take) | 0 | 5 |
| 3 | 3 | (2, 1, 0) | 2 (take) | 0 | 1 |
| 2 | 2 | (1, 1, 0) | 1 (take) | 0 | 1 |
| 1 | 1 | (0, 1, 0) | 1 (take) | 0 | 3 |

The output is $3, 5, 1, 1, 3$. The decoder ranks it back to $21$ and computes $\lfloor 21 \cdot 16/30 \rfloor = \lfloor 11.2 \rfloor = 11$, that is 1011. The 16 inputs $v = 0, \ldots, 15$ go to the ranks $0, 2, 4, 6, 8, 10, 12, 14, 15, 17, 19, 21, 23, 25, 27, 29$, from $1, 1, 3, 3, 5$ for $v = 0$ to $5, 3, 3, 1, 1$ for $v = 15$. Every word has the energy $2 \cdot 1 + 2 \cdot 9 + 25 = 45$, or $9$ per symbol, against $35/3 = 11.7$ for uniform amplitudes; the rate is $0.8$ bits per symbol, against an entropy of $1.52$ for the type.

**The binary example of the paper.** With $n = 4$ and two 0s and two 1s, $T = 6$ and $k = 2$. The inputs 00, 01, 10, 11 go to the ranks $0, 2, 3, 5$, that is to 0011, 0110, 1001, 1100.

**Rate against block length.** For the target $P = (0.4, 0.3, 0.2, 0.1)$ on the amplitudes $1, 3, 5, 7$, with entropy $H(P) = 1.8464$ bits and energy $13$ against $21$ for uniform amplitudes, the best type is $P$ itself at these lengths:

| $n$ | $k$ | $k/n$ | rate loss $H(P) - k/n$ | bound $(3\log_2(n + 1) + 1)/n$ |
|---|---|---|---|---|
| 10 | 13 | 1.300 | 0.546 | 1.138 |
| 20 | 30 | 1.500 | 0.346 | 0.709 |
| 100 | 175 | 1.750 | 0.0964 | 0.210 |
| 1000 | 1831 | 1.831 | 0.0154 | 0.0309 |
| 10000 | 18444 | 1.8444 | 0.0020 | 0.0041 |

## Correctness

The count of words that start with a given symbol is $T c_s/n$, by the multinomial formula. Lines L5 to L9 keep two invariants: $N$ is the number of words of the remaining composition, and $r$ is the rank of the wanted word among them. At each step the words are grouped by their first symbol in the order $a_1, \ldots, a_M$, the group of $a_s$ has $N_s$ words, and line L8 enters the group that contains rank $r$. So the output is the word of rank $r$, and it has the composition $c$. The decoder adds the sizes of the groups before the actual symbol, which gives back $r$. Line L3 gives $r - 1 < vT/2^k \le r$, and since $T \ge 2^k$ this implies $v \le r\,2^k/T < v + 1$, so line L15 returns $v$. So the map is one-to-one, and every output has the composition $c$. For the rate, the type class of a type $Q$ of length $n$ on $M$ symbols has at least $2^{nH(Q)}/\binom{n + M - 1}{M - 1}$ words, which gives $k/n > H(c/n) - \big((M - 1)\log_2(n + 1) + 1\big)/n$. The full proof is below.

## Complexity

In the [word RAM](/word-ram/) with words of $w \ge \log_2 n$ bits, every count is at most $T \le M^n$, a number of at most $n\log_2 M$ bits, or $O(n\log M/w)$ words. Line L7 multiplies such a number by a small integer and divides it exactly by $\ell$, in $O(n\log M/w)$ steps. It runs at most $M$ times per symbol, so unranking and ranking cost $O(M n^2\log M/w)$, and computing $T$ costs $O(n^2\log M/w)$. Line L3 multiplies two numbers of $O(n\log M)$ bits, in $O((n\log M/w)^2)$ steps with schoolbook multiplication, which is not larger. The extra space is the few big numbers, $O(n\log M/w)$ words. A binary search over the cumulative counts in line L6 cuts the factor $M$ to $\log M$ multiplications per symbol. The arithmetic coder of the paper works with finite precision and rescaling, in $O(1)$ word operations per symbol for fixed precision, at the cost of a small change in the codebook.

## Properties

- **Fixed length and one-to-one.** Every block of $k$ bits gives a block of $n$ symbols, and the decoder is exact. A fixed length suits a channel code with a fixed block size, and an error in one block does not spread to the next.
- **Constant composition.** Every output has the same counts, so every word has the same energy, the same number of each amplitude, and the same per-word frequencies. In a long stream, the frequencies of the amplitudes are exactly $c/n$.
- **Rate loss.** The rate $k/n$ is below the entropy $H(c/n)$ of the type, and the loss is at most $((M - 1)\log_2(n + 1) + 1)/n$, which goes to zero as $n$ grows. The normalized divergence of the output from i.i.d. $P$ also goes to zero.
- **Unequal use.** Only $2^k$ of the $T$ words are used, and each used word has probability $2^{-k}$. The symbols at one position are not exactly i.i.d. with distribution $P$.
- **Serial.** Each output symbol depends on all earlier decisions, which limits the speed in hardware.

## Variants and improvements

- **Finite precision arithmetic coding.** The original encoder is an arithmetic coder with registers of fixed width and rescaling, which avoids big numbers.
- **Binary decomposition.** Write each amplitude as a few bits and match each bit level with a binary CCDM. Binary CCDM indexes the words of a fixed weight, as [enumerative coding](/enumerative-coding/) does.
- **Shorter blocks with less loss.** Multiset-partition matching and sphere shaping allow words of more than one type, for example all words with energy below a bound. They lose less rate at short $n$, which CCDM needs for low latency.
- **Parallel matchers.** Several short CCDMs in parallel raise the throughput, at the cost of a larger rate loss.
- **Other targets.** The same encoder matches any distribution on a finite alphabet, not only amplitudes, for example the bits of a rate-adapted code.

## When to use it

Use CCDM for the amplitudes of [probabilistic amplitude shaping](/probabilistic-constellation-shaping/) when the block can be long (hundreds to thousands of symbols), so that the rate loss is small, and when a fixed length and an exact inverse matter more than the lowest latency. For short blocks, a matcher that allows several types loses less.

## Pitfalls

- **Short blocks.** At $n = 10$ the rate loss is $0.55$ bits per symbol, more than the shaping gain is worth. Check the rate table before choosing $n$.
- **The type.** Rounding $nP$ independently for each symbol need not give counts that sum to $n$, and may not give the type with the smallest divergence. Choose $c$ as a whole.
- **Exact arithmetic.** $T$ grows like $2^{nH}$, so $n = 1000$ needs integers of about $1850$ bits. Floating point loses the exact ranks and breaks the inverse.
- **The rounding direction.** Line L3 rounds up and line L15 rounds down. Rounding both the same way can map two inputs to one rank, or give a rank that the decoder sends back to a different $v$.
- **Errors in the decoder input.** The decoder assumes a word of composition $c$. After a channel error, the received word may not be in $\mathcal{T}_c$, or may be a word that the encoder never produces. In probabilistic amplitude shaping the channel decoder corrects the errors first, so the matcher sees error-free amplitudes most of the time; the receiver must still handle the other case.

## Implementations

## History

Fixed-to-fixed distribution matching came up with probabilistic shaping for higher-order modulation. Böcherer, Steiner and Schulte in 2015 proposed probabilistic amplitude shaping, in which a distribution matcher produces the amplitudes and a systematic LDPC code adds the signs. Schulte and Böcherer in 2016 gave the constant composition matcher: choose the type with the smallest divergence from the target, use all words of that type as the codebook, and index them by arithmetic coding with the probabilities "copies left divided by symbols left". They showed that the rate approaches the entropy of the target as the block length grows. The idea of indexing all words of a fixed composition is older: it is the enumerative source coding of Cover in 1973 for fixed weights.

## References
