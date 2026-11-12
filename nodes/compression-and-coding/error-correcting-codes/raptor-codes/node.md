---
tag: GTWFNH
kind: definition
slug: raptor-codes
name: Raptor codes
area: compression-and-coding/error-correcting-codes
level: research
summary: "Fountain codes made of a high-rate precode followed by an LT code of constant mean degree. They encode and decode in linear time with a small constant overhead."
history:
  year: 2006
  people: [Amin Shokrollahi]
  note: Shokrollahi published Raptor codes in IEEE Transactions on Information Theory in 2006. RFC 5053 (2007) standardized the code R10, and RFC 6330 (2011) the code RaptorQ.
prereqs: [lt-codes, ldpc-code]
see_also: [fountain-codes, peeling-decoding, erasure-decoding, xor-gaussian-elimination, tanner-graph, binary-erasure-channel, erasure-codes, systematic-code]
sources:
  - paper: doi:10.1109/TIT.2006.874390
    title: Amin Shokrollahi, Raptor codes, IEEE Transactions on Information Theory 52(6), 2006, pages 2551 to 2567
    locator: Section III (Raptor codes as a precode with an output degree distribution), the lower bound on the degree of LT codes, Theorem 5 (the distribution with maximum degree D + 1 and overhead ε at cost O(log(1/ε))), and the section on systematic Raptor codes
  - url: https://www.rfc-editor.org/rfc/rfc5053
    title: Michael Luby, Amin Shokrollahi, Mark Watson and Thomas Stockhammer, RFC 5053, Raptor Forward Error Correction Scheme for Object Delivery, October 2007
    locator: Section 5.1.2 (Kmax = 8192), Section 5.4.2.3 (X, S, H, L and the LDPC and Half symbols), Section 5.4.4.2 Table 1 (degree generator), Section 5.4.4.3 (LTEnc), Section 5.4.4.4 (Trip), Section 5.5 (example decoder), Section 5.6 (tables V0 and V1), Section 5.7 (systematic indices J(K))
  - url: https://www.rfc-editor.org/rfc/rfc6330
    title: Michael Luby, Amin Shokrollahi, Mark Watson, Thomas Stockhammer and Lorenz Minder, RFC 6330, RaptorQ Forward Error Correction Scheme for Object Delivery, August 2011
    locator: Section 5.1.2 (K'max = 56403), Section 5.3.3.3 (LDPC and HDPC relations, P = L - W), Section 5.3.5.2 (degree table up to degree 30), Section 5.6 Table 2 (K', J, S, H, W), Section 5.8 (failure at most 1/100, 1/10^4 and 1/10^6 with K', K' + 1 and K' + 2 symbols)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 50 (digital fountain codes, and the short account of Raptor codes as a precode plus a weakened LT code)
---

A Raptor code is a [fountain code](/fountain-codes/) built in two stages. A high-rate erasure code, the *precode*, first extends the $k$ source symbols to $n$ slightly more *intermediate symbols*. An [LT code](/lt-codes/) whose mean degree is a constant then makes an endless stream of encoded symbols from the intermediate symbols. The LT stage alone would leave a few symbols unknown; the precode fills them in. Amin Shokrollahi introduced Raptor codes, for *rapid tornado*, and published them in 2006. They give fountain codes with linear-time encoding and decoding, and the standard codes R10 (RFC 5053) and RaptorQ (RFC 6330) are Raptor codes.

## Definition

**Notation.** The source has $k$ symbols, each a packet of bits, and $\oplus$ is bitwise XOR. A degree distribution is written as a polynomial $\Omega(x) = \sum_{d} \Omega_d x^d$, where $\Omega_d$ is the probability of degree $d$. The *overhead* of a decoder that succeeds from $K$ received symbols is $\varepsilon = K/k - 1$.

**Definition (Raptor code, Shokrollahi 2006).** A Raptor code with parameters $(k, \mathcal{C}, \Omega)$ is given by:

1. a linear *precode* $\mathcal{C}$ of dimension $k$ and length $n$ over $\mathrm{GF}(2)$;
2. an output degree distribution $\Omega(x)$ on $\{1, \ldots, n\}$.

Encoding has two steps. First encode the source with $\mathcal{C}$ to get $n$ intermediate symbols. Then make each encoded symbol as in an LT code over the $n$ intermediate symbols: draw a degree $d$ from $\Omega$, choose $d$ distinct intermediate symbols uniformly, and XOR them. As in every fountain code, the encoded symbol with index $j$ is made from a pseudorandom generator seeded with $j$.

**Decoding.** The receiver writes one linear equation for each received symbol and one for each check of the precode, with the $n$ intermediate symbols as unknowns. Shokrollahi's analysis uses the [peeling decoder](/peeling-decoding/) on this graph: peeling on the LT part recovers all but a small fraction of the intermediate symbols, and the precode, decoded by peeling too, recovers the rest. Practical decoders use *inactivation decoding*: they peel while they can, mark a symbol as inactive when peeling stops, and finish with Gaussian elimination on the small set of inactive symbols. This is maximum likelihood decoding, done fast.

**Why a precode helps.** An LT code must cover every source symbol, so by a coupon collector argument its mean degree is $\Omega(\ln k)$ (see [LT codes](/lt-codes/)). A Raptor code needs the LT stage to recover only a fraction $1 - \delta$ of the intermediate symbols, which a constant mean degree does. The precode, chosen to correct a $\delta$ fraction of erasures in linear time, does the rest. So the cost per symbol becomes a constant.

**Theorem (Shokrollahi 2006, Theorem 5).** Fix $\varepsilon > 0$. Let $D = \lceil 4(1+\varepsilon)/\varepsilon \rceil$, $\mu = \varepsilon/2 + (\varepsilon/2)^2$ and

$$\Omega_D(x) = \frac{1}{\mu + 1} \left( \mu x + \sum_{i=2}^{D} \frac{x^i}{(i-1)\,i} + \frac{x^{D+1}}{D} \right).$$

Take a precode of rate $(1 + \varepsilon/2)/(1 + \varepsilon)$ that the peeling decoder corrects up to a fixed small fraction of erasures (for example a suitable [LDPC code](/ldpc-code/)). Then the Raptor code decodes from $k(1 + \varepsilon)$ symbols with high probability, and it costs $O(\ln(1/\varepsilon))$ symbol operations per encoded symbol and per source symbol.

**Two extreme cases.**

- If the precode is the identity, the Raptor code is an LT code.
- If $\Omega(x) = x$, each encoded symbol is a copy of one intermediate symbol, and the code is the precode sent in random order. Shokrollahi calls this a *pre-code-only* Raptor code. It is not a good fountain, because collecting all $n$ intermediate symbols in random order needs about $n \ln n$ receptions.

**Systematic Raptor codes.** In a systematic code the first $k$ encoded symbols equal the source symbols. Shokrollahi's paper and RFC 5053 do this by running the encoder backwards: the sender first solves for intermediate symbols whose first $k$ encoded symbols are the source, then encodes them as usual. A receiver that loses nothing reads the source directly.

**The standard R10, RFC 5053 (2007).** The code works on source blocks of $K$ symbols, $4 \le K \le 8192$. Its precode adds $S$ LDPC symbols and $H$ Half symbols, $L = K + S + H$ intermediate symbols in all (Section 5.4.2.3):

- $X$ is the smallest positive integer with $X(X - 1) \ge 2K$;
- $S$ is the smallest prime with $S \ge \lceil 0.01 K \rceil + X$;
- $H$ is the smallest integer with $\binom{H}{\lceil H/2 \rceil} \ge K + S$.

Source symbol $i$ is XORed into three LDPC symbols: with $a = 1 + (\lfloor i/S \rfloor \bmod (S-1))$ and $b = i \bmod S$, it goes into LDPC symbols $b$, $b + a$ and $b + 2a$ modulo $S$. Half symbol $h$ is the XOR of those symbols $C[j]$, $0 \le j < K + S$, for which bit $h$ of the $j$-th Gray code of weight $\lceil H/2 \rceil$ is one. So each column of the Half part has weight $\lceil H/2 \rceil$, and the Half rows are dense.

The degree of an encoded symbol comes from a 20-bit random number $v$ and Table 1 of Section 5.4.4.2, copied here by hand:

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $f[j]$ | 0 | 10241 | 491582 | 712794 | 831695 | 948446 | 1032189 | 1048576 |
| $d[j]$ | | 1 | 2 | 3 | 4 | 10 | 11 | 40 |

Degree $d[j]$ is chosen when $f[j-1] \le v < f[j]$. The probabilities are about 0.0098, 0.459, 0.211, 0.113, 0.111, 0.080 and 0.016, and the mean degree is about 4.63, a constant. The generator LTEnc (Section 5.4.4.3) picks the $d$ intermediate symbols $b, b + a, b + 2a, \ldots$ modulo the smallest prime $L' \ge L$, and skips values at least $L$. The triple $(d, a, b)$ comes from the generator Trip (Section 5.4.4.4), which uses the random tables V0 and V1 of Section 5.6 and the systematic index $J(K)$ of Section 5.7. Section 5.5 gives an example decoder by Gaussian elimination in phases.

**The standard RaptorQ, RFC 6330 (2011).** RaptorQ allows up to $K'_{\max} = 56403$ source symbols per block, with $K$ padded up to a value $K'$ from Table 2. Its precode has $S$ LDPC symbols and $H$ HDPC symbols. The HDPC relations are over $\mathrm{GF}(256)$, which makes the code behave almost like a random code. $P = L - W$ intermediate symbols are *permanently inactivated*, so the decoder always puts them in the Gaussian elimination part. The degree table goes up to degree 30. Section 5.8 asks a decoder to fail at most once in 100 trials from $K'$ symbols, once in $10^4$ from $K' + 1$ and once in $10^6$ from $K' + 2$.

## Examples and non-examples

**The R10 precode for $K = 4$.** Here $X = 4$ (since $4 \cdot 3 = 12 \ge 8$ and $3 \cdot 2 = 6 < 8$), $S = 5$, $H = 5$ (since $\binom{4}{2} = 6 < 9 \le \binom{5}{3} = 10$) and $L = 14$. All four source symbols have $a = 1$, so source symbol $i$ enters LDPC symbols $i, i+1, i+2$ modulo 5:

| LDPC symbol | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| source symbols in it | 0, 3 | 0, 1 | 0, 1, 2 | 1, 2, 3 | 2, 3 |

The Half part uses the first $K + S = 9$ Gray codes with $\lceil 5/2 \rceil = 3$ ones: 7, 13, 14, 11, 25, 26, 28, 21, 22. For larger blocks the formulas give $(X, S, H, L) = (46, 59, 13, 1072)$ for $K = 1000$ and $(129, 211, 16, 8419)$ for $K = 8192$.

**A small Raptor code in the style of R10.** The implementation here uses the R10 precode, Table 1 and LTEnc. It is not RFC 5053: it draws $(d, a, b)$ from Python's random module in place of Trip and the tables V0 and V1, it is not systematic, and its decoder is peeling followed by plain Gaussian elimination. With $K = 200$ ($L = 233$), random lost symbols and 40 trials per row with fixed seeds, it decoded:

| extra symbols beyond $K$ | 0 | 2 | 5 | 10 |
|---|---|---|---|---|
| Raptor (precode plus LT) | 8/40 | 29/40 | 39/40 | 40/40 |
| same LT degrees, no precode | 0/40 | 0/40 | 1/40 | 4/40 |

Without the precode, the mean degree of 4.63 leaves some source symbols in no received symbol at all, and nothing can recover them. With 50 extra symbols, peeling alone (no elimination) finished in only 3 of 40 trials: the dense Half rows are made for the elimination phase.

**Non-example: an LT code.** An LT code is the Raptor code with the identity precode. To cover every source symbol it needs mean degree of order $\ln k$, so encoding and decoding cost $O(k \ln k)$, not $O(k)$.

**Non-example: an LDPC code alone.** An [LDPC code](/ldpc-code/) of rate $k/n$ decodes erasures in linear time, but it has a fixed length. It is a pre-code-only Raptor code at best, and a receiver that misses more than $n - k$ symbols cannot be helped.

**Non-example: the random linear fountain.** Each encoded symbol is a uniform random XOR of all source symbols. It needs only about 1.6 extra symbols on average, less than R10, but its mean degree is $k/2$ and decoding costs order $k^3$ bit operations. RaptorQ gets close to its overhead with constant degree by putting a small dense part over $\mathrm{GF}(256)$ in the precode.

## Related definitions

- [Fountain codes](/fountain-codes/): the class. Raptor codes are its members with linear time.
- [LT codes](/lt-codes/): the inner stage; a Raptor code weakens the LT code to constant degree.
- [LDPC codes](/ldpc-code/): the usual precode, decoded by the [peeling decoder](/peeling-decoding/).
- [Erasure decoding](/erasure-decoding/) and [Gaussian elimination over GF(2)](/xor-gaussian-elimination/): inactivation decoding is Gaussian elimination that peels first.
- [Systematic codes](/systematic-code/): R10 and RaptorQ are systematic Raptor codes.
- Online codes (Maymounkov 2002) use the same plan of an outer code plus a sparse fountain and were found at the same time.

## References

- Amin Shokrollahi, "Raptor codes", IEEE Transactions on Information Theory 52(6), 2006, pages 2551 to 2567.
- Michael Luby, Amin Shokrollahi, Mark Watson and Thomas Stockhammer, RFC 5053, "Raptor Forward Error Correction Scheme for Object Delivery", 2007.
- Michael Luby, Amin Shokrollahi, Mark Watson, Thomas Stockhammer and Lorenz Minder, RFC 6330, "RaptorQ Forward Error Correction Scheme for Object Delivery", 2011.
- David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003, Chapter 50.
