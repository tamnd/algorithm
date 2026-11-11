---
tag: SXWWDF
kind: algorithm
slug: casting-out-nines
name: Casting out nines
aliases:
- check digit by mod 9
- digit sums mod 9
- digital root check
- mod 9 check
area: compression-and-coding/checksums
level: intro
summary: Checks a sum or product by the digit sums mod 9 of the operands and the result. A mismatch proves an error; a match misses every error that is a multiple of 9, such as swapped digits.
model: word-ram
complexity:
  vars: {n: the total number of digits of the operands and the claimed result}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1202
  people: [Ibn Sina, Leonardo of Pisa (Fibonacci)]
  note: The dates are uncertain. Secondary sources credit Aryabhata II (about 950) and Ibn Sina (about 1020, a "Hindu method") with the check on arithmetic; Fibonacci taught it in Liber Abaci in 1202.
prereqs: [congruence]
see_also: [check-digit-computation, luhn-algorithm, additive-checksum, ones-complement-arithmetic, chinese-remainder-theorem, residue-number-system, error-detection]
sources:
  - url: https://en.wikipedia.org/wiki/Casting_out_nines
    title: Casting out nines, Wikipedia
    locator: The sections on the method, on the errors it misses, and on its history (Hippolytus, Iamblichus, Aryabhata II, Ibn Sina, Fibonacci)
  - paper: "Laurence E. Sigler, Fibonacci's Liber Abaci, a translation into modern English of Leonardo Pisano's Book of Calculation, Springer, 2002"
    title: L. E. Sigler, Fibonacci's Liber Abaci, Springer, 2002
    locator: The early chapters on multiplication and addition of whole numbers, where the proof by casting out nines is taught (exact chapter not checked)
  - paper: "Bibhutibhushan Datta and Avadhesh Narayan Singh, History of Hindu Mathematics, A Source Book, Asia Publishing House, 1962"
    title: B. Datta and A. N. Singh, History of Hindu Mathematics, 1962
    locator: The part on checks of the fundamental operations (Aryabhata II and the account of Ibn Sina), as cited by Wikipedia
  - paper: doi:10.1145/243439.243457
    title: Joseph A. Gallian, Error detection methods, ACM Computing Surveys 28(3), 1996, pages 504 to 517
    locator: The section on check digits computed modulo 9 and the errors they miss
---

Casting out nines checks a sum or a product done by hand. Add the decimal digits of each operand and reduce mod 9; this "excess of nines" is the number mod 9, because $10 \equiv 1 \pmod 9$. Do the same operation on the excesses of the operands and compare with the excess of the claimed result. If they differ, the result is wrong. If they agree, the result is right mod 9 only: the check misses every error that changes the result by a multiple of 9, and that includes any transposition of its digits, a 0 written as 9, and a partial product shifted by one column. It is the decimal form of the end-around-carry sum of the [Internet checksum](/internet-checksum/), which reduces mod $2^{16} - 1$ in the same way (see [ones' complement arithmetic](/ones-complement-arithmetic/)). Casting out elevens, with the alternating digit sum, catches the swaps of adjacent digits, and the two checks together miss exactly the errors that are multiples of 99. The history is old and partly uncertain; Fibonacci taught the check in 1202.

## In plain words

Add up the digits of a number. If the total has more than one digit, add those digits too, until one digit is left, and count 9 as 0. What is left is the remainder of the number when divided by 9.

To check $3248 \times 1765 = 5732720$, reduce each number: 3248 gives 8, 1765 gives 1, and 5732720 gives 8. Now do the same multiplication on the small numbers: $8 \times 1 = 8$. It matches, so the check passes. If it had not matched, the product would surely be wrong.

A match is weaker. If you swap two digits of the answer, or write a 0 for a 9, the digit sum stays the same and the check still passes. Casting out elevens, with digits added and subtracted in turn, catches most of those slips.

## The problem

The input is two non-negative integers $a$ and $b$ in decimal and a claimed result $c$ of $a + b$ or $a \times b$. The output is "error" or "no error found". The answer "error" must be correct whenever it is given; the answer "no error found" is allowed to be wrong. The check must use only digit operations on small numbers, so that it is much cheaper than doing the arithmetic again. We count digit operations in the [word RAM](/word-ram/).

The key fact is that $10 \equiv 1 \pmod 9$, so $10^i \equiv 1$ for every $i$, and a number $\sum_i d_i 10^i$ is congruent to its digit sum $\sum_i d_i$ (see [congruence](/congruence/)).

## The algorithm

```pseudo id=main
EXCESS9(x)                                   ▷ the digit sum of x with nines cast out
L1  r ← 0
L2  for each decimal digit d of x do
L3      r ← r + d
L4      if r ≥ 9 then r ← r − 9
L5  return r

CHECK-ADDITION(a, b, c)
L6  return EXCESS9(EXCESS9(a) + EXCESS9(b)) = EXCESS9(c)

CHECK-MULTIPLICATION(a, b, c)
L7  return EXCESS9(EXCESS9(a) · EXCESS9(b)) = EXCESS9(c)
```

Line L4 keeps $r$ in $0..8$: before it $r \le 8 + 9 = 17$. So 9 counts as 0, which is what "casting out" a nine means. The implementation never computes $x \bmod 9$ on the number itself; it works on the digits only, as a person does.

## Example

Check $3248 \times 1765$, with the claimed result 5732720.

- $3 + 2 + 4 + 8 = 17$, and $1 + 7 = 8$, so EXCESS9(3248) $= 8$.
- $1 + 7 + 6 + 5 = 19$, so EXCESS9(1765) $= 1$.
- $8 \times 1 = 8$.
- $5 + 7 + 3 + 2 + 7 + 2 + 0 = 26$, so EXCESS9(5732720) $= 8$.

The two sides agree, so line L7 finds no error. A clerk who copies the product as 5723720, with two digits swapped, also passes the check. Casting out elevens catches it: the alternating digit sums from the right give $8 - 4 + 2 - 3 = 3$ for 3248, $5 - 6 + 7 - 1 = 5$ for 1765, and $3 \times 5 = 15 \equiv 4 \pmod{11}$, while 5723720 gives $0 - 2 + 7 - 3 + 2 - 7 + 5 = 2$. A clerk who writes 5732820, with one digit off by 1, fails the nines check. The tests check all these values.

## Correctness

Each digit $d_i$ stands for $d_i 10^i$, and $10^i \equiv 1 \pmod 9$, so a number is congruent to its digit sum, and line L4 keeps the running sum reduced. So EXCESS9$(x) = x \bmod 9$. Addition and multiplication respect congruences, so a correct result always passes. The check passes exactly when $c \equiv a + b$ (or $a b$) mod 9, so the errors it misses are exactly those with $c - (a \text{ op } b)$ a multiple of 9. The tests confirm this rule on every wrong product $c < 1000$ of every $x, y < 30$. The full proof, with casting out elevens, is in the correctness file below.

## Complexity

EXCESS9 does one addition and one comparison per digit, so it takes $\Theta(k)$ time for $k$ digits and $O(1)$ extra space. The checks call it on $a$, $b$, $c$ and on a number below 81, so they take $\Theta(n)$ time in total. Schoolbook multiplication of the operands takes $\Theta(n^2)$ digit operations, so the check is much cheaper than doing the work again, which is its purpose.

## Properties

Which errors are missed follows from the rule above:

| error in the result | change | nines | elevens |
|---|---|---|---|
| one digit wrong, not 0 for 9 | $\pm k 10^i$, $1 \le k \le 8$ | caught | caught |
| a 0 written as 9 or back | $\pm 9 \cdot 10^i$ | missed | caught |
| adjacent digits swapped | $9(a - b) 10^i$ | missed | caught |
| digits two places apart swapped | $99(a - b) 10^i$ | missed | missed |
| any permutation of the digits | multiple of 9 | missed | depends |
| a 0 added at the end | $9t$ for the true result $t$ | missed | caught unless 11 divides $t$ |
| a partial product shifted one column | $9 p 10^i$ | missed | caught unless $11$ divides $p$ |

- **Rate.** For a wrong answer that is close to random, the nines check misses about 1 in 9. In the tests, of the 899,100 wrong products $c < 1000$ of $x, y < 30$, it misses 99,260, and nines and elevens together miss 8,258, which are exactly the multiples of 99.
- **Errors in the check.** The check itself is arithmetic and can be done wrong. A slip there gives a false alarm or a false pass.
- **A check digit mod 9.** Used as a check digit, the number mod 9 misses every 0 to 9 change and every transposition, as the table shows. This is why stronger schemes such as [Luhn](/luhn-algorithm/) weight or permute the digits (see [check digit computation](/check-digit-computation/)).

## Variants and improvements

- **Casting out elevens.** Since $10 \equiv -1 \pmod{11}$, the alternating sum of the digits, from the right, gives $x \bmod 11$. It catches every swap of two different adjacent digits, because the change $9(a - b)10^i$ is not a multiple of 11. The implementation includes it.
- **Both together.** By the [Chinese remainder theorem](/chinese-remainder-theorem/), passing both checks means $c \equiv a \text{ op } b \pmod{99}$. This is a small [residue number system](/residue-number-system/) used as a check.
- **Division and subtraction.** Check $a = q b + r$ for a division by casting out nines from $q$, $b$, $r$ and $a$; check a subtraction $a - b = c$ as the addition $c + b = a$.
- **Other bases.** In base $B$ the digit sum gives the number mod $B - 1$, and the alternating sum gives it mod $B + 1$. In base $2^{16}$ the first one is the [Internet checksum](/internet-checksum/); see also the [additive checksum](/additive-checksum/).

## When to use it

Use casting out nines as a quick check of hand arithmetic or of a mental calculation, and as a classroom example of [congruence](/congruence/). Add casting out elevens when digit swaps are likely, as in copying. Do not use either as a check digit for identifiers; use [Luhn](/luhn-algorithm/), [Verhoeff](/verhoeff-algorithm/) or [Damm](/damm-algorithm/). In software, compare the result with a second method or use a modular check with a large or random modulus.

## Pitfalls

- **A pass is not a proof.** The check proves only $c \equiv a \text{ op } b \pmod 9$. A transposed answer passes.
- **Reduce the result of the small operation.** For a product, reduce $\mathrm{EXCESS9}(a) \cdot \mathrm{EXCESS9}(b)$ again, as line L7 does: $8 \times 7 = 56$ must become 2 before the comparison.
- **9 is 0.** A digit sum of 9 or 18 reduces to 0. Comparing a digital root of 9 with an excess of 0 gives a false alarm.
- **Elevens from the right.** The alternating sum must start with a plus at the units digit. Starting from the left gives $-x \bmod 11$ for a number with an even count of digits, so the three numbers can get different signs.
- **Negative numbers.** The implementation accepts non-negative integers only and raises an error otherwise.

## Implementations

## History

The history is old and the sources are secondary, so the details below are uncertain. Hippolytus of Rome (early third century) and Iamblichus describe repeated digit sums of Greek numerals, but not as a check of arithmetic. The earliest known work that uses the digit sum mod 9 to check calculations is usually given as the Mahasiddhanta of Aryabhata II, about 950. Ibn Sina (Avicenna), about 1020, described it in detail and called it the "Hindu method". Leonardo of Pisa (Fibonacci) taught it in Liber Abaci in 1202, and from there it entered the arithmetic books of Europe, where it was taught in schools for centuries. The sources cited here do not date casting out elevens.

## References
