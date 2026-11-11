---
tag: BC0D59
kind: algorithm
slug: luhn-algorithm
name: Luhn algorithm
aliases:
- Luhn formula
- mod 10 check
- modulus 10 check
area: compression-and-coding/checksums
level: intro
summary: Mod-10 check digit of payment card and IMEI numbers. Double every second digit from the right, add the digits, total 0 mod 10. It misses no single error and of adjacent swaps only 09 and 90.
model: word-ram
complexity:
  vars: {n: the number of digits}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1960
  people: [Hans Peter Luhn]
  note: Luhn of IBM filed the patent for a hand-held device that verifies numbers by this rule in 1954, and US patent 2,950,048 was granted in 1960. ISO/IEC 7812-1 later made it the check of payment card numbers.
prereqs: [check-digit-computation]
see_also: [verhoeff-algorithm, damm-algorithm, casting-out-nines, permutation, error-detection, hamming-distance]
sources:
  - url: https://patents.google.com/patent/US2950048A/en
    title: H. P. Luhn, Computer for Verifying Numbers, US patent 2,950,048, filed January 6, 1954, granted August 23, 1960
    locator: The description of the doubling of alternate digits, the addition of the digits of each product, and the test for a total that ends in 0
  - paper: "ISO/IEC 7812-1:2017, Identification cards, Identification of issuers, Part 1: Numbering system"
    title: ISO/IEC 7812-1:2017, Numbering system
    locator: The annex on the Luhn formula for computing modulus 10 double-add-double check digits
  - paper: doi:10.1145/243439.243457
    title: Joseph A. Gallian, Error detection methods, ACM Computing Surveys 28(3), 1996, pages 504 to 517
    locator: The section on the IBM scheme (Luhn) and the errors it misses
---

The Luhn algorithm computes the check digit of payment card numbers, IMEI numbers of mobile phones, and many other identifiers. Count the digits from the right, with the check digit first. Double every second digit, and when the double is 10 or more, add its two digits (the same as subtracting 9). The number is valid when the total of all the digits is a multiple of 10. Hans Peter Luhn of IBM patented a device for it in 1954 to 1960. The doubling map is a [permutation](/permutation/) of the digits, so every single wrong digit is caught; and the map $x \mapsto D(x) - x$, where $D$ is the doubling, almost separates the digits, so every swap of two neighbors is caught except 09 and 90. It is cheaper to explain than the [Verhoeff](/verhoeff-algorithm/) and [Damm](/damm-algorithm/) algorithms, which catch all adjacent swaps, and it is stronger than the weights 3 and 1 of EAN barcodes, which miss five pairs of digits (see [check digit computation](/check-digit-computation/)).

## In plain words

Start at the right end of the number. Leave the last digit as it is, double the one before it, leave the next one, double the next, and so on to the left. When a doubled digit gives a two-digit number, such as 16, add the two digits, so 16 counts as 7. Add everything. If the total ends in 0, the number is valid.

To make the last digit for a new number, do the same with the doubling starting at the rightmost digit you have, and pick the digit that brings the total to a multiple of 10. A clerk can do all of this in his head, which was the point in 1954. The check catches every single wrong digit and almost every swap of two neighbors.

## The problem

The input is a payload of $n$ decimal digits. The output is one check digit $c$ such that the $(n+1)$-digit number passes the test. Write the code word as $x_1 \ldots x_{n+1}$ from the right, so $x_1 = c$. With the doubling map $D(x) = 2x$ for $x \le 4$ and $D(x) = 2x - 9$ for $x \ge 5$, the test is

$$\sum_{i \text{ odd}} x_i + \sum_{i \text{ even}} D(x_i) \equiv 0 \pmod{10}.$$

The table of $D$ is 0, 2, 4, 6, 8, 1, 3, 5, 7, 9. We count digit operations in the [word RAM](/word-ram/).

## The algorithm

One loop reads the digits from the right and switches the doubling on and off. Validation starts with no doubling, at the check digit. Generation runs the same loop over the payload with the doubling on at its rightmost digit, which will sit in place 2.

```pseudo id=main
LUHN-SUM(x, double)                         ▷ x read from the right
L1  t ← 0
L2  d ← double                              ▷ true if the rightmost digit is doubled
L3  for each digit v of x, from right to left do
L4      t ← t + (D[v] if d else v)          ▷ D = 0 2 4 6 8 1 3 5 7 9
L5      d ← not d
L6  return t mod 10

CHECK-DIGIT(p)
L7  return (10 − LUHN-SUM(p, true)) mod 10

IS-VALID(w)
L8  return LUHN-SUM(w, false) = 0
```

Line L7 works because in the code word the payload digits keep their parity of place, shifted by one: the rightmost payload digit sits in place 2 and is doubled. The check digit sits in place 1 with weight 1, so the check that makes the total 0 is $(10 - t) \bmod 10$.

## Example

The payload 7992739871. From the right, the digits 1, 8, 3, 2 and 9 sit in even places of the code word and are doubled: they give 2, 7 (from 16), 6, 4 and 9 (from 18). The others, 7, 9, 7, 9 and 7, stay. The total is

$$2 + 7 + 7 + 9 + 6 + 7 + 4 + 9 + 9 + 7 = 67,$$

so the check digit is $10 - 7 = 3$, and 79927398713 is valid. Changing the last digit to 0 makes it invalid. The card test number 4111111111111111 is valid as well. The tests check these values and compare the implementation on 1,000 random payloads and 1,000 random strings with an independent form that writes out each product and adds its digits.

## Correctness

The check digit makes the total 0 by construction, and the validation loop computes the same total. Since $D$ is a permutation of $\{0, \ldots, 9\}$, a change of one digit changes the total by a nonzero amount mod 10, so every single error is detected. A swap of adjacent digits $a, b$ changes the total by $\pm\big((D(a) - a) - (D(b) - b)\big)$, and the values $D(x) - x \bmod 10$ for $x = 0, \ldots, 9$ are 0, 1, 2, 3, 4, 6, 7, 8, 9, 0. They are distinct except that 0 and 9 both give 0. So the only missed adjacent swaps are 09 and 90. The full proof is in the correctness file below.

## Complexity

Each digit costs one table lookup and one addition, so validation and generation take $\Theta(n)$ time and $\Theta(1)$ extra space. The loop reads from the right; to read from the left, find the parity of $n$ first.

## Properties

Over all 10,000 payloads of 4 digits (5-digit code words), the tests count the missed errors of each class exactly:

| error | example | missed | of |
|---|---|---|---|
| single error | $a \to b$ | 0 | 450,000 |
| adjacent transposition | $ab \to ba$ | 800 | 36,000 |
| twin error | $aa \to bb$ | 2,400 | 36,000 |
| jump transposition | $abc \to cba$ | 27,000 | 27,000 |

- **Adjacent transpositions.** The 800 misses are all swaps of 0 and 9 (the tests check each one). That is 2 of the 90 ordered pairs of different digits.
- **Twin errors.** Since $D(x) + x \bmod 10$ takes the values 0, 3, 6, 9, 2, 6, 9, 2, 5, 8, the twins $22 \leftrightarrow 55$, $33 \leftrightarrow 66$ and $44 \leftrightarrow 77$ are missed, and the tests find exactly these three pairs.
- **Jump transpositions.** Digits two places apart get the same treatment, so a swap of them never changes the total. All are missed.
- **Phonetic errors.** Of the errors $a0 \leftrightarrow 1a$ for $a = 2, \ldots, 9$, such as "fifty" for "fifteen", Luhn misses $20 \leftrightarrow 12$ when the left digit is doubled and $80 \leftrightarrow 18$ when the right digit is doubled, and catches the rest.
- **Leading zeros.** Adding zeros on the left does not change the total, so 0 and 00 are both valid, and the check digit of a payload does not depend on leading zeros.

## Variants and improvements

- **Weighted mod 10 (GS1).** EAN and UPC use weights 3 and 1. A weighted sum is linear, and the [check digit computation](/check-digit-computation/) page shows that no weighted scheme mod 10 catches all single errors and all adjacent swaps; GS1 misses five pairs. Luhn is not linear in the digits, because $D$ is not multiplication by a constant mod 10, and it misses only one pair.
- **[Verhoeff algorithm](/verhoeff-algorithm/).** Replaces the addition mod 10 by the dihedral group of order 10 and the doubling by a permutation of order 8. It catches all single errors and all adjacent transpositions, and most twin and jump errors.
- **[Damm algorithm](/damm-algorithm/).** Uses one table of a quasigroup. Same guarantees as Verhoeff with a single table.
- **Luhn mod N.** The same doubling idea over an alphabet of $N$ symbols, for codes with letters.

## When to use it

Use Luhn when a standard requires it: payment cards (ISO/IEC 7812), IMEI, and the many national schemes that copied it. For a new decimal code, prefer [Damm](/damm-algorithm/) or [Verhoeff](/verhoeff-algorithm/), which cost a table of 100 entries and catch all adjacent swaps. None of these guards against fraud: anyone can compute a valid check digit.

## Pitfalls

- **Which digits to double.** Double every second digit counting from the right, with the check digit not doubled. Doubling the first digit from the left gives the same result only when the full number, check digit included, has an even length.
- **Generation versus validation.** When generating, the rightmost payload digit is doubled, because it will sit in place 2. Running the validation loop on the payload and appending $(10 - t) \bmod 10$ gives a wrong digit.
- **The 9 subtraction.** Use $2x - 9$ for $x \ge 5$, or add the digits of the product. Reducing $2x$ mod 10 is a different and much weaker check: it maps 0 and 5 both to 0, so it misses some single errors.
- **Non-ASCII digits.** Some languages treat other Unicode digits as decimal digits. The implementation rejects them.
- **Not a security check.** A passing number is only well formed. Card issuers check the account itself.

## Implementations

## History

Hans Peter Luhn, a researcher at IBM, filed a patent on January 6, 1954 for a hand-held "Computer for Verifying Numbers", a mechanical device that applies this rule; it was granted as US patent 2,950,048 on August 23, 1960. The rule spread to credit card numbers, and the ISO/IEC 7812 standard for issuer identification numbers made it the check digit of card numbers. Later it was adopted for IMEI numbers and many national identifiers. Verhoeff (1969) and later authors studied which errors such schemes miss, which led to the [Verhoeff](/verhoeff-algorithm/) and [Damm](/damm-algorithm/) algorithms.

## References
