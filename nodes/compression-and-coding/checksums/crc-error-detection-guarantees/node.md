---
tag: Y8VC6W
kind: theorem
slug: crc-error-detection-guarantees
name: CRC error-detection guarantees
aliases:
- CRC burst detection property
area: compression-and-coding/checksums
level: core
summary: An r-bit CRC detects every burst of length at most r, and every odd number of bit errors when the generator has factor x+1.
prereqs: [cyclic-redundancy-check, crc-generator-polynomial, burst-errors]
see_also: [crc32c, undetected-error-probability, hamming-distance, minimum-distance, cyclic-code, multiplicative-order, table-driven-crc, error-detection]
sources:
  - paper: doi:10.1109/JRPROC.1961.287814
    title: W. W. Peterson and D. T. Brown, Cyclic codes for error detection, Proceedings of the IRE 49(1), 1961
    locator: pp. 228 to 235 (detection of all bursts of length at most the number of check bits, the fraction of longer bursts that are missed, and the errors detected by the factors of the generator)
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 5 (error detection with cyclic codes, the burst-detection result and the fractions of undetected long bursts)
  - paper: doi:10.1109/DSN.2004.1311885
    title: Philip Koopman and Tridib Chakravarty, Cyclic redundancy code (CRC) polynomial selection for embedded networks, International Conference on Dependable Systems and Networks (DSN), 2004
    locator: Sections 2 and 3 (Hamming distance as a function of data word length, and the role of the factor x + 1)
  - url: https://users.ece.cmu.edu/~koopman/crc/crc8.html
    title: Philip Koopman, CRC polynomial zoo, 8-bit polynomials
    locator: Entries 0x83 and 0xa6 (the data lengths for Hamming distance 3 and 4, which follow from the period of the generator)
---

The error-detection guarantees of a [cyclic redundancy check](/cyclic-redundancy-check/) are the classes of errors that it detects with certainty, whatever the message. An $r$-bit CRC with a [generator polynomial](/crc-generator-polynomial/) $G$ detects every single-bit error and every [burst](/burst-errors/) of length at most $r$. If $x + 1$ divides $G$, it also detects every error of odd weight, and it detects every pair of errors closer than the period of $G$. All these facts follow from one rule: an error is missed exactly when $G$ divides it.

## Statement

Let $G(x)$ be a polynomial over GF(2) of degree $r \ge 1$ with $G(0) = 1$, and let codewords have $N$ bits. An error pattern is a nonzero polynomial $E(x)$ of degree less than $N$: the coefficient of $x^i$ is 1 when bit $i$ is wrong. The weight of $E$ is its number of nonzero terms. A burst of length $b$ is an error $x^i B(x)$ with $\deg B = b - 1$ and $B(0) = 1$, so the first and the last wrong bits are $b - 1$ apart. The period of $G$ is the least $e \ge 1$ with $G \mid x^e + 1$, the [multiplicative order](/multiplicative-order/) of $x$ modulo $G$.

**Theorem.** The receiver of the CRC with generator $G$, for any init, xorout and reflection, misses an error $E$ if and only if $G \mid E$. Hence:

1. Every error of weight 1 is detected.
2. If $(x + 1) \mid G$, every error of odd weight is detected.
3. An error $x^i + x^{i+j}$ with $j \ge 1$ is missed if and only if $e \mid j$. So if $N \le e$, every error of weight 2 is detected.
4. Every burst of length $b \le r$ is detected.
5. At a fixed position there are $2^{b-2}$ bursts of length $b \ge 2$. Of them, 1 is missed if $b = r + 1$, and $2^{b-r-2}$ are missed if $b \ge r + 2$. The missed fractions are $2^{-(r-1)}$ and $2^{-r}$.
6. For $N \ge r$, exactly $2^{N-r} - 1$ of the $2^N - 1$ nonzero error patterns are missed.

With reflection, the positions are permuted, which keeps weights; the statement about bursts holds for the order in which the register reads the bits.

## In plain words

A CRC treats the message as a long polynomial and keeps its remainder after division by a fixed polynomial. An error changes the message by adding an error polynomial. The check fails to see the error only when the fixed polynomial divides the error polynomial exactly.

A short error, one that fits inside a window no wider than the check, is too small to be a multiple of the fixed polynomial, so the CRC always catches it. If the fixed polynomial has an even number of terms, every multiple of it has an even number of 1 bits, so the CRC catches every odd number of flipped bits. Two flipped bits are caught unless they are a whole number of periods apart. Longer bursts are missed only rarely, about once in two to the power of the check width.

## Proof

The rule. By the invariant of the CRC register, the receiver accepts a word exactly when its polynomial, with the fixed contribution of init and xorout removed, is a multiple of $G$. The sent word is accepted, and the effect of an error is to add $E$ by linearity over GF(2). So the received word is accepted if and only if $G \mid E$. The full argument is on the page of the [cyclic redundancy check](/cyclic-redundancy-check/).

Lemma. Since $G(0) = 1$, $x$ does not divide $G$, and $x$ is irreducible, so $\gcd(x, G) = 1$. Hence $G \mid x^i A$ if and only if $G \mid A$.

1. For $E = x^i$, the lemma gives $G \mid 1$, which is false because $\deg G \ge 1$.
2. $E(1)$ is the weight of $E$ modulo 2, which is 1. If $G \mid E$ and $(x + 1) \mid G$, then $(x + 1) \mid E$, so $E(1) = 0$. Contradiction.
3. $x^i + x^{i+j} = x^i (x^j + 1)$. By the lemma it is missed if and only if $x^j \equiv 1 \pmod G$. The period $e$ exists because $x$ is a unit in the finite ring $\mathrm{GF}(2)[x]/(G)$, and the $j$ with $x^j \equiv 1$ are exactly the multiples of $e$. If $N \le e$, then $j \le N - 1 < e$.
4. By the lemma, $x^i B$ is missed if and only if $G \mid B$. But $B \ne 0$ and $\deg B = b - 1 < r$, so $G \nmid B$.
5. A burst is fixed by its $b - 2$ inner bits, so there are $2^{b-2}$. It is missed if and only if $B = GQ$. Then $\deg Q = b - 1 - r$, the top coefficient of $Q$ is 1, and $Q(0) = 1$ because $B(0) = G(0) = 1$. For $b = r + 1$ the only choice is $Q = 1$. For $b \ge r + 2$ the $b - r - 2$ inner coefficients of $Q$ are free, and distinct $Q$ give distinct $B$. Dividing by $2^{b-2}$ gives the fractions.
6. The missed patterns are the products $GQ$ with $Q \ne 0$ and $\deg Q < N - r$, and there are $2^{N-r} - 1$ of them.

The implementation checks each claim exhaustively for the CRC-8 generators 0x107 and 0x14D and the CRC-16 generators 0x18005 and 0x11021: all single errors up to 300 bits, all $2^{20} - 1$ patterns of 20 bits, all double errors up to beyond the period, all bursts up to length 16 for width 8 and 20 for width 16, and a real CRC-16/IBM-3740 with init 0xFFFF on random messages.

## Consequences

- **Hamming distance 4 for the classic design.** If $G = (x + 1) p(x)$ with $p$ primitive of degree $r - 1$, then by the Chinese remainder theorem the period is $2^{r-1} - 1$. Claims 1 to 3 then give [Hamming distance](/hamming-distance/) at least 4 for codewords of up to $2^{r-1} - 1$ bits. For CRC-16/ARC, $G = (x + 1)(x^{15} + x + 1)$ with period 32767. For [CRC-32C](/crc32c/) the period is $2^{31} - 1$.
- **Hamming distance 3 for a primitive generator.** If $G$ is primitive of degree $r$, its period is $2^r - 1$, so all errors of weight 1 and 2 are detected in codewords of up to $2^r - 1$ bits. The IEEE CRC-32 is of this form.
- **Bursts.** CRC-32 detects every burst of 32 bits or fewer, at any position in a message of any length, and misses only 1 in $2^{31}$ bursts of 33 bits and 1 in $2^{32}$ longer bursts. A [table-driven CRC](/table-driven-crc/) computes the same remainder, so it has the same guarantees.
- **Random errors.** If all nonzero patterns are equally likely, the miss probability is $(2^{N-r} - 1)/(2^N - 1) < 2^{-r}$. For errors on a channel with independent bit flips the miss probability depends on the weight distribution of the code instead; see [undetected error probability](/undetected-error-probability/).
- **Cyclic codes.** The same proof applies to every [cyclic code](/cyclic-code/) of length $n$ and $n - k = r$ check bits, which detects every burst of length at most $n - k$, including end-around bursts.

## Tightness

Each bound is reached.

- **Bursts of length $r + 1$.** $E = G$ itself is a burst of length $r + 1$, and it is missed. So the bound $b \le r$ in claim 4 cannot be raised for any generator.
- **Odd weight without $x + 1$.** The primitive generator 0x14D $= x^8 + x^6 + x^3 + x^2 + 1$ has 5 terms, so $E = G$ is a missed error of weight 5. The exhaustive test finds missed odd-weight patterns of 20 bits for this generator.
- **Double errors.** $x^e + 1$ is a missed error of weight 2 for every generator, so the length bound $N \le e$ in claim 3 cannot be raised. For 0x101 $= x^8 + 1$ the period is 8, so two flips 8 bits apart are missed in any message.
- **The condition $G(0) = 1$.** For $G = x^2 + x$, the error $E = G$ is a burst of length 2 that is missed, although $r = 2$. Every standard CRC generator has a constant term.
- **Weight 3 and more.** The theorem says nothing about errors of weight 3, 4 or more at practical lengths. These depend on the whole generator and are found by search; see the [minimum distance](/minimum-distance/) profiles on the [generator polynomial](/crc-generator-polynomial/) page.

## History

Peterson and Brown (1961) introduced cyclic codes for error detection and proved the main statements: detection of all bursts of length at most the number of check bits, the fractions $2^{-(r-1)}$ and $2^{-r}$ of longer bursts that are missed, and the role of the factors of the generator, such as $x + 1$ for odd numbers of errors. Textbooks such as Lin and Costello give the same results for all cyclic codes. Castagnoli, Bräuer and Herrmann (1993) and Koopman and Chakravarty (2004) moved the focus from these classes to the Hamming distance at each data length, because the classes do not decide which generator is best for errors of weight 3 to 6.

## References
