---
tag: CAQC35
kind: problem
slug: check-digit-computation
name: Check digit computation
aliases:
- check digit
- check digit calculation
area: compression-and-coding/checksums
level: intro
summary: Choose one or two characters to append to an identifier so that every single wrong digit and most swapped digits make it invalid. ISBN, EAN, IBAN and ORCID each solve it with a weighted sum.
prereqs: [congruence]
see_also: [luhn-algorithm, verhoeff-algorithm, damm-algorithm, casting-out-nines, primitive-root, minimum-distance, error-detection, hamming-distance]
sources:
  - paper: doi:10.1145/243439.243457
    title: Joseph A. Gallian, Error detection methods, ACM Computing Surveys 28(3), 1996, pages 504 to 517
    locator: The sections on weighted check digits modulo 10 and modulo 11 (UPC, ISBN), on the error types and their frequencies, and on the dihedral group method
  - paper: "ISO/IEC 7064:2003, Information technology, Security techniques, Check character systems"
    title: ISO/IEC 7064:2003, Check character systems
    locator: The pure systems MOD 11-2 (one check character, possibly X) and MOD 97-10 (two check digits), and the error classes they detect
  - url: https://www.gs1.org/services/how-calculate-check-digit-manually
    title: GS1, How to calculate a check digit manually
    locator: The weights 3 and 1 from the right for GTIN-8, GTIN-12 (UPC-A), GTIN-13 (EAN-13) and GTIN-14, and the subtraction from the next multiple of ten
  - url: https://www.isbn-international.org/content/isbn-users-manual
    title: International ISBN Agency, ISBN Users' Manual
    locator: The structure of the ISBN and the check digit of ISBN-13, with the prefixes 978 and 979
  - url: https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
    title: ORCID, Structure of the ORCID identifier
    locator: The check digit by ISO/IEC 7064:2003 MOD 11-2, the sample code and the identifier 0000-0002-1825-0097
  - paper: "ISO 13616-1:2020, Financial services, International bank account number (IBAN), Part 1: Structure of the IBAN"
    title: ISO 13616-1:2020, Structure of the IBAN
    locator: The two check digits by ISO/IEC 7064 MOD 97-10, after the country code and check digits are moved to the end and letters are replaced by 10 to 35
---

The check digit problem asks for a short tail, usually one character, to append to an identifier such as a book number, a barcode or a bank account, so that the typical mistakes of a person who copies it make the result invalid. The two mistakes that matter most are one wrong digit and two adjacent digits swapped; together they are most of the errors that people make. Almost every scheme in use computes a weighted sum of the digits and picks the check so that the total is a fixed value modulo $m$. The choice of $m$ and of the weights decides which errors are caught. This page states the problem, explains the weighted schemes of ISBN, EAN, UPC, ISO/IEC 7064 and IBAN, and links to the three classic algorithms for decimal digits: [Luhn](/luhn-algorithm/), [Verhoeff](/verhoeff-algorithm/) and [Damm](/damm-algorithm/).

## In plain words

When you type a long number, you sometimes hit a wrong key, and sometimes you swap two keys. A check digit is one extra digit, computed from the others, that lets a machine notice such a slip at once, before the wrong book is shipped or the money goes to the wrong account.

The machine recomputes the check from the digits it got. If it does not match the last digit, something is wrong. A good check digit always notices a single wrong digit and a swap of two neighbors. One digit cannot catch everything: there are ten times more numbers than check digits, so some pairs of mistakes always slip through. The design question is which mistakes to catch and at what cost, such as the extra letter X of ISBN-10.

## Definition

**Input.** A payload $x_1 x_2 \ldots x_n$ of symbols from an alphabet of size $q$, usually the decimal digits.

**Output.** A check string $c$, usually one symbol, so that the code word $x_1 \ldots x_n c$ is valid. Validity is a test that the receiver can run on the code word alone.

**Error classes.** For decimal codes, Verhoeff (1969) and Gallian (1996) use these classes:

- *single error*: $a \to b$ in one place;
- *adjacent transposition*: $ab \to ba$;
- *twin error*: $aa \to bb$;
- *jump transposition*: $acb \to bca$;
- *jump twin error*: $aca \to bcb$;
- *phonetic error*: $50 \to 15$, from words such as "fifty" and "fifteen".

Single errors and adjacent transpositions are by far the most common, so the basic requirement is to detect all of them.

**Weighted schemes.** Most schemes fix weights $w_1, \ldots, w_{n+1}$ and a modulus $m$, and choose $c$ so that
$$\sum_{i=1}^{n} w_i x_i + w_{n+1} c \equiv r \pmod m$$
for a fixed $r$. An error that changes the digit in place $i$ by $\delta$ changes the sum by $w_i \delta$. A swap of $a$ in place $i$ and $b$ in place $j$ changes it by $(w_i - w_j)(b - a)$. The error is missed exactly when the change is $\equiv 0 \pmod m$.

## Variants

- **ISBN-10.** Nine digits, weights $10, 9, \ldots, 2$, and weight 1 on the check. The total must be $0 \bmod 11$. The check value 10 is written X.
- **EAN-13, ISBN-13 and UPC-A (GS1).** From the right, the check has weight 1, the digit before it 3, then 1, 3, and so on. The total must be $0 \bmod 10$. ISBN-13 is EAN-13 with the prefix 978 or 979. UPC-A is EAN-13 with a leading 0 left out.
- **ISO/IEC 7064 MOD 11-2.** The character in place $i$ from the right (the check is $i = 1$) has weight $2^{i-1} \bmod 11$, and the total must be $1 \bmod 11$. The check value 10 is written X. ORCID identifiers and the 18-character resident identity numbers of China (GB 11643-1999) use it. In Horner form: $p \leftarrow 0$; for each digit $x$, $p \leftarrow 2(p + x) \bmod 11$; then $c = (12 - p) \bmod 11$.
- **ISO/IEC 7064 MOD 97-10.** Two check digits, chosen so that the whole string read as a decimal number is $1 \bmod 97$; that is, the check is $98 - (\text{payload} \cdot 100 \bmod 97)$. IBAN uses it, after it moves the country code and the check digits to the end and replaces each letter by a number from 10 (A) to 35 (Z).
- **Luhn (mod 10).** Double every second digit from the right, subtract 9 when the result exceeds 9, and make the sum $0 \bmod 10$. Payment card numbers use it. See [Luhn algorithm](/luhn-algorithm/).
- **Group-based schemes.** [Verhoeff](/verhoeff-algorithm/) uses the dihedral group of order 10 and a permutation, and [Damm](/damm-algorithm/) uses a table of a quasigroup of order 10. Both catch all single errors and all adjacent transpositions with one decimal digit.
- **Casting out nines.** The digit sum mod 9 is the oldest check of this kind. It catches no swaps at all. See [casting out nines](/casting-out-nines/).

## Examples

**ISBN-10 0-306-40615-2.** The weighted sum of the payload is $10 \cdot 0 + 9 \cdot 3 + 8 \cdot 0 + 7 \cdot 6 + 6 \cdot 4 + 5 \cdot 0 + 4 \cdot 6 + 3 \cdot 1 + 2 \cdot 5 = 130$, and $130 \equiv 9 \pmod{11}$. The check is $11 - 9 = 2$, so the total is $132 \equiv 0$.

**ISBN-13 978-0-306-40615-7.** The weights 1, 3, 1, 3, ... from the left on the twelve digits give 93, so the check is $10 - 3 = 7$.

**EAN-13 4006381333931.** The twelve digits give $4 + 0 + 0 + 18 + 3 + 24 + 1 + 9 + 3 + 9 + 9 + 9 = 89$, so the check is $10 - 9 = 1$. The UPC-A code 036000291452 has the check 2.

**ORCID 0000-0002-1825-0097.** The Horner form gives $p = 0$ for the seven leading zeros, then 4, 10, 3, 10, 8, 5, 10 and 5 after the digits 2, 1, 8, 2, 5, 0, 0, 9. The check is $(12 - 5) \bmod 11 = 7$.

**Chinese identity number.** For the payload 63280119790817003 the weights $2^{17}, \ldots, 2^1 \bmod 11$ are 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2. The weighted sum is 336, which is $6 \bmod 11$, so the check is $(12 - 6) \bmod 11 = 6$. The payload 34262219840209049 gets the check X.

**IBAN GB82 WEST 1234 5698 7654 32.** Moving the first four characters to the end gives WEST12345698765432GB82. Replacing W, E, S, T, G and B by 32, 14, 28, 29, 16 and 11 gives 3214282912345698765432161182, which is $1 \bmod 97$. With 00 in place of 82 the remainder is 16, and $98 - 16 = 82$.

**Exhaustive counts.** For all 10,000 payloads of 4 digits, the tests count the errors that each scheme misses on the 5-character code word. A single error replaces one character by one of the other decimal digits, and a transposition swaps two different characters.

| scheme | missed single errors | missed adjacent swaps | missed swaps at any distance |
|---|---|---|---|
| mod 11, weights 5, 4, 3, 2, 1 (ISBN rule) | 0 | 0 of 36,091 | 0 of 90,364 |
| ISO/IEC 7064 MOD 11-2 | 0 | 0 of 36,091 | 0 of 90,364 |
| GS1, weights 3 and 1 mod 10 | 0 | 4,000 of 36,000 | 42,000 of 90,000 |
| ISO/IEC 7064 MOD 97-10 (3 digits and 2 check digits) | 0 | 0 of 3,618 | 0 of 9,016 |

The mod 11 totals are a little larger than 36,000 and 90,000 because 909 of the code words end in X. The GS1 scheme misses exactly the adjacent swaps of two digits that differ by 5 (10 percent of the digit pairs, hence 4,000), and every swap of two places with the same weight. For the [Luhn](/luhn-algorithm/), [Verhoeff](/verhoeff-algorithm/) and [Damm](/damm-algorithm/) codes, the same counts are on the Damm page.

## Known algorithms

- **Weighted sum mod 11 (ISBN-10, MOD 11-2).** One pass over the digits, $\Theta(n)$ time. Catches all single errors and all transpositions while the weights are distinct, at the cost of an eleventh symbol.
- **Weighted sum mod 10 (GS1).** One pass, digits only. Catches all single errors and 8/9 of the adjacent transpositions.
- **[Luhn algorithm](/luhn-algorithm/).** One pass with a doubling table. Catches all single errors and all adjacent transpositions except 09 and 90.
- **[Verhoeff algorithm](/verhoeff-algorithm/)** and **[Damm algorithm](/damm-algorithm/).** One pass with a table of 100 entries. Both catch all single errors and all adjacent transpositions with one decimal digit.
- **MOD 97-10.** Two digits; reduces the long number modulo 97 a few digits at a time. Catches all single errors and all transpositions at distance below 96, and leaves about 1 in 97 of the other errors.

The implementation computes ISBN-10, GS1 (EAN-13, ISBN-13, UPC-A), MOD 11-2 (with the Chinese identity number as a special case), MOD 97-10 and IBAN. Its tests check the published examples above, compare each scheme with a brute-force search for the check on 1,000 random payloads, run the exhaustive counts, and check every single error and every transposition of 300 random full ISBN-10 code words.

## Bounds

**Why mod 11 with distinct weights catches all transpositions.** A single error changes the sum by $w_i \delta$ with $\delta \ne 0$, and a swap of $a \ne b$ in places $i$ and $j$ changes it by $(w_i - w_j)(b - a)$. Since 11 is prime, $\mathbb{Z}_{11}$ has no zero divisors: a product is $0 \bmod 11$ only if a factor is. With weights that are nonzero and distinct mod 11, $w_i \not\equiv 0$ and $w_i - w_j \not\equiv 0$. The differences of symbols lie in $[-10, 10]$ and are not 0, so they are not multiples of 11. Hence both changes are nonzero mod 11, and the errors are detected. ISBN-10 has weights $10, \ldots, 1$, all distinct. MOD 11-2 has weights $2^{i-1} \bmod 11$, which are distinct for $i = 1, \ldots, 10$ because 2 is a [primitive root](/primitive-root/) modulo 11; places 10 apart get the same weight, so on code words longer than 10 characters, such as the 18-character identity number and the 16-character ORCID, a swap of two characters exactly 10 places apart is missed.

**Why weights 1 and 3 mod 10 miss digits that differ by 5.** A swap of adjacent digits $a$ and $b$ changes the GS1 sum by $(3 - 1)(b - a) = 2(b - a)$, and $2(b - a) \equiv 0 \pmod{10}$ exactly when $b - a \equiv 0 \pmod 5$, that is, $|a - b| = 5$. So 05, 16, 27, 38 and 49 and their reverses are missed.

**No weighted sum mod 10 catches both classes.** For all single errors in place $i$ to be detected, $w_i \delta \not\equiv 0 \pmod{10}$ for every $\delta \in \{1, \ldots, 9\}$, so $w_i$ must be a unit mod 10, which means odd and not 5. Then two adjacent weights are both odd, so $w_i - w_{i+1}$ is even, and the swap of two digits that differ by 5 changes the sum by $(w_i - w_{i+1}) \cdot 5 \equiv 0 \pmod{10}$. So every weighted decimal scheme with one check digit misses some adjacent transposition, or some single error. Luhn escapes the linear form with its doubling map and still misses 09 and 90. Verhoeff and Damm escape it fully, with a non-commutative group and a quasigroup.

**One check symbol cannot do more than distance 2.** A single check symbol over an alphabet of size $q$ gives $q^n$ code words of length $n + 1$. Take two payloads that differ in the first place only. Their code words differ in that place and at most in the check, so in at most two places. So the [minimum distance](/minimum-distance/) is at most 2, and some error in two places is always missed. In the same way, among all errors that turn a code word into a random string, about $1/q$ pass. Two check symbols, as in MOD 97-10, lower that to about $1/97$.

## Reductions

- **To modular arithmetic.** Every weighted scheme is one [congruence](/congruence/) $\sum w_i x_i \equiv r \pmod m$, and computing the check means solving it for the last unknown, which needs the [modular inverse](/modular-inverse/) of its weight. The common schemes give the check weight 1, so the check is a subtraction.
- **To error detection codes.** A check digit scheme is an [error detection](/error-detection/) code of length $n + 1$ with one redundant symbol. Its detection rules are statements about the [Hamming distance](/hamming-distance/) and about the structure of the errors it misses.

## Applications

- **Book trade.** ISBN-10 until 2006 and ISBN-13 since 2007, ISSN for serials (mod 11).
- **Retail.** EAN-13, UPC-A, GTIN-14 and other GS1 keys on barcodes.
- **Payments.** Payment card numbers (Luhn), IBAN (MOD 97-10), and many national account numbers.
- **Identity.** National identity numbers (MOD 11-2 in China, other mod 11 rules elsewhere), ORCID for researchers.
- **Data entry everywhere.** Order numbers, serial numbers and other codes that people type.

## References
