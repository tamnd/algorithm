---
tag: SD1VWV
kind: concept
slug: undetected-error-probability
name: Undetected error probability
aliases:
- residual error probability
area: compression-and-coding/checksums
level: core
summary: Probability that a corrupted message still matches its check value. It is about 2^-r for an r-bit check under random errors, but some codes do worse at low error rates.
prereqs: [binary-symmetric-channel, macwilliams-identity, cyclic-redundancy-check]
see_also: [crc-error-detection-guarantees, crc-generator-polynomial, dual-code, minimum-distance, hamming-code, error-detection, checksum, hamming-weight]
sources:
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Section 3.6 (probability of an undetected error for linear codes over a BSC, the formula from the weight distribution and from the dual code, and the example of the (7, 4) Hamming code)
  - paper: doi:10.1109/TCOM.1982.1095473
    title: Jack K. Wolf, Arnold M. Michelson and Allen H. Levesque, On the probability of undetected error for linear block codes, IEEE Transactions on Communications 30(2), 1982
    locator: The computation of the undetected error probability from the weight distribution of the dual code, and the codes for which it exceeds 2^-(n-k)
  - paper: "S. K. Leung-Yan-Cheong and M. E. Hellman, Concerning a bound on undetected error probability, IEEE Transactions on Information Theory 22(2), 1976"
    title: Concerning a bound on undetected error probability
    locator: The examples of codes that do not meet the bound 2^-(n-k) at every bit error rate
  - paper: doi:10.1109/DSN.2004.1311885
    title: Philip Koopman and Tridib Chakravarty, Cyclic redundancy code (CRC) polynomial selection for embedded networks, International Conference on Dependable Systems and Networks (DSN), 2004
    locator: Section 2 (the undetected error probability at low bit error rates is set by the Hamming distance and the number of codewords of that weight)
---

The undetected error probability $P_{ud}$ of an error-detecting code is the probability that the channel changes a codeword into another codeword, so the receiver accepts wrong data. On a [binary symmetric channel](/binary-symmetric-channel/) it is a polynomial in the bit error rate $p$, fixed by the weight distribution of the code. For an $r$-bit [cyclic redundancy check](/cyclic-redundancy-check/) it is close to $2^{-r}$ when the errors are very noisy, and much smaller at low error rates. But for some codes and lengths it goes above $2^{-r}$; these codes are called improper.

## In plain words

A check catches most damage, but not all. Some damaged messages happen to have a valid check value, and the receiver accepts them. The undetected error probability is the chance of this.

It depends on how the damage happens. If every possible damage is equally likely, a check of r bits misses about one in two to the power of r. If the damage is usually small, only a few flipped bits, a good check misses much less often, because it catches all small damage.

A bad check can be worse than one in two to the power of r for small damage. So a designer computes this chance for the real message length and the real error rate, and does not trust a rule of thumb.

## The idea

### The formula

Let $C$ be a binary linear code of length $n$ and dimension $k$, with $r = n - k$ check bits. Let $A_i$ be the number of codewords of [Hamming weight](/hamming-weight/) $i$. On a binary symmetric channel each bit flips independently with probability $p$. The error pattern is the XOR of the sent and received words. For a linear code the receiver misses an error exactly when the error is a nonzero codeword, so

$$P_{ud}(p) = \sum_{i=1}^{n} A_i\, p^i (1 - p)^{n - i}.$$

This does not depend on which codeword was sent. For a CRC with generator $G$, the codewords of length $n$ are the multiples of $G$ of degree less than $n$, and $k = n - r$.

### The dual formula

Enumerating $2^k$ codewords is impossible for long messages. The [dual code](/dual-code/) has only $2^r$ words. Its weight distribution $B_i$ comes from the rows of the [parity-check matrix](/parity-check-matrix/): for a CRC, column $i$ is the syndrome $x^i \bmod G$. The [MacWilliams identity](/macwilliams-identity/) $W_C(x, y) = 2^{-r} W_{C^\perp}(x + y, x - y)$, at $x = 1 - p$ and $y = p$, gives

$$P_{ud}(p) = 2^{-r} \sum_{i=0}^{n} B_i (1 - 2p)^i - (1 - p)^n.$$

For a 16-bit CRC this is a sum over 65536 dual words at any length $n$, so the cost is $O(2^r n)$ instead of $O(2^k n)$.

### Two regimes

- **At $p = 1/2$** every pattern is equally likely, and $P_{ud}(1/2) = (2^k - 1)/2^n < 2^{-r}$. This is the value behind the rule of thumb "an $r$-bit check misses one error in $2^r$".
- **At small $p$** the first nonzero term dominates: $P_{ud}(p) \approx A_d\, p^d$, where $d$ is the [minimum distance](/minimum-distance/). So a code with a large Hamming distance at the message length, and few codewords of that weight, is far better than $2^{-r}$. This is why generators are chosen by their Hamming distance profile; see [CRC generator polynomial](/crc-generator-polynomial/).

### Proper and improper codes

A code is *proper* if $P_{ud}(p)$ does not decrease on $[0, 1/2]$. Then $P_{ud}(p) \le P_{ud}(1/2) < 2^{-r}$ for every $p$, and the rule of thumb is a true bound. A code is *improper* if $P_{ud}$ goes above its value at $1/2$ for some $p < 1/2$. This happens when the code has many codewords of low weight: they dominate at moderate $p$ before the high-weight terms take over. Leung-Yan-Cheong and Hellman (1976) gave codes that do not meet the bound $2^{-r}$, and Wolf, Michelson and Levesque (1982) computed $P_{ud}$ for linear block codes from the dual distribution and found more such cases. Whether a code is proper depends on its length, so a CRC that is proper at one length can be improper at another.

## Examples

**The [7, 4] [Hamming code](/hamming-code/)**, generated by $x^3 + x + 1$, has $A(z) = 1 + 7z^3 + 7z^4 + z^7$, and its dual, the simplex code, has $B(z) = 1 + 7z^4$. Both formulas give

$$P_{ud}(p) = 7p^3(1 - p)^4 + 7p^4(1 - p)^3 + p^7 = \tfrac{1}{8}\bigl(1 + 7(1 - 2p)^4\bigr) - (1 - p)^7,$$

which is the example in Lin and Costello. At $p = 1/2$ it is $15/128$. This code is proper.

**CRC-8/SMBUS at 64 bits.** The generator 0x107 $= (x + 1)(\ldots)$ at $n = 64$ has $A_4 = 5049$ codewords of weight 4 and none of weight 1, 2 or 3. The dual formula gives $P_{ud} \approx 4.76 \times 10^{-9}$ at $p = 10^{-3}$, close to $A_4 p^4 \approx 5.05 \times 10^{-9}$, and $2.80 \times 10^{-5}$ at $p = 10^{-2}$. Both are far below $2^{-8} \approx 3.9 \times 10^{-3}$. The code is proper at lengths 64, 128 and 256 on a grid of 2000 values of $p$.

**An improper code.** The generator $x^8 + 1$ at $n = 64$ has 224 codewords of weight 2, the pairs of positions a multiple of 8 apart. Its $P_{ud}$ reaches about 0.0345 near $p = 0.036$, almost 9 times $2^{-8}$.

**CRC-16 at 128 bits.** The generator 0x18005 of CRC-16/ARC, at $n = 128$, has $P_{ud}(0.035) \approx 5.12 \times 10^{-5}$, which is about 3.35 times $2^{-16}$, computed exactly with fractions. The generator 0x11021 of ITU-T V.41 at the same length and $p$ gives about 1.05 times $2^{-16}$. Both are improper at this length, although both have Hamming distance 4.

**Check by simulation.** The implementation also runs 100000 trials of a binary symmetric channel with the fixed seed 1982, draws the flipped positions by geometric gaps, and counts the nonzero error patterns with syndrome 0. For $x^8 + 1$ at $n = 64$ with $p = 1/32$, for CRC-8/SMBUS at $n = 64$ with $p = 0.2$, and for the [7, 4] Hamming code with $p = 0.1$, the counts agree with the dual formula within five standard deviations. Other tests check that the dual formula equals the direct sum exactly for several codes, and that the MacWilliams transform of $B$ gives back $A$.

## Where it is used

When a system needs a known limit on the rate of wrong data that is accepted, as in safety-critical networks, designers compute $P_{ud}$ for the chosen [checksum](/checksum/) or CRC at the real message lengths and bit error rates. Koopman and Chakravarty use the low-$p$ form $A_d p^d$ to compare CRC generators. The [CRC error-detection guarantees](/crc-error-detection-guarantees/) give the error classes that are never missed; $P_{ud}$ gives the probability for all the rest. For [error detection](/error-detection/) against an adversary, the error is not random, and $P_{ud}$ does not apply; a [message authentication code](/message-authentication-code/) is needed.

## References
