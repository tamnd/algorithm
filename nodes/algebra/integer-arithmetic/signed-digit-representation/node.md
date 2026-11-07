---
tag: DNY74H
kind: definition
slug: signed-digit-representation
name: Signed-digit representation
aliases:
- balanced digit representation
- signed-digit number system
- SD representation
area: algebra/integer-arithmetic
level: advanced
summary: Positional representation whose digits may be negative, allowing redundant forms.
prereqs: [positional-number-system, radix]
see_also: [redundant-number-system, non-adjacent-form, balanced-ternary, booth-multiplication, non-restoring-division, carry-save-addition, twos-complement, carry-propagation]
sources:
  - paper: A. Avizienis, Signed-digit number representations for fast parallel arithmetic, IRE Transactions on Electronic Computers EC-10(3), 1961
    title: Algirdas Avizienis, Signed-digit number representations for fast parallel arithmetic
    locator: pp. 389 to 400 (the digit sets of radix r with r greater than 2 and the totally parallel addition)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 3, Redundant number systems (digit sets, generalized signed-digit numbers, carry-free addition and conversions)
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.1, Positional number systems (balanced ternary and negative digits)
---

A signed-digit representation writes an integer in a radix $\beta$ with digits that may be negative, such as $-1, 0, 1$ in radix 2 or $-6, \ldots, 6$ in radix 10. The value is the usual sum $\sum d_i \beta^i$. When the digit set has more than $\beta$ elements the representation is *redundant*: a number has several representations, for example $7 = 111_2 = 100\bar{1}_2$, where $\bar{1}$ is the digit $-1$. Redundancy is what makes the representation useful. Avizienis showed in 1961 that, with a suitable digit set in a radix $\beta \ge 3$, two numbers can be added with every sum digit depending only on two positions of the operands, so the time of an addition does not grow with the length. Signed digits also give negation by negating each digit, the sign from the leading nonzero digit, and sparse recodings such as the [non-adjacent form](/non-adjacent-form/) used to speed up multiplication and exponentiation.

## Definition

Fix a radix $\beta \ge 2$ and integers $a, b \ge 0$, and let the *digit set* be the set of consecutive integers

$$D = \{-a, -a + 1, \ldots, b - 1, b\}, \qquad a + b + 1 \ge \beta .$$

A **signed-digit representation** of an integer $x$ in radix $\beta$ with digit set $D$ is a finite string $d_{k-1} \cdots d_1 d_0$ with $d_i \in D$ and

$$x = \sum_{i=0}^{k-1} d_i \beta^i .$$

It is *signed* when $a \ge 1$. The usual [positional number system](/positional-number-system/) is the case $a = 0$, $b = \beta - 1$. The most studied case is the *symmetric* digit set $a = b$, written $D = [-a, a]$. A negative digit $-d$ is written $\bar{d}$.

**Facts.** Let $D = [-a, a]$ with $a \ge 1$ and $2a + 1 \ge \beta$.

1. **Completeness.** Every integer, positive or negative, has a representation. The digits $-a, \ldots, a$ contain a full set of residues modulo $\beta$, so the last digit can be chosen with $x \equiv d_0 \pmod \beta$, and the rest of the digits represent $(x - d_0)/\beta$, which is smaller in absolute value when $|x| > a$.
2. **Redundancy.** The representation is unique, up to leading zeros, exactly when $2a + 1 = \beta$, which requires $\beta$ odd; this is the *balanced* system, such as [balanced ternary](/balanced-ternary/). When $2a + 1 > \beta$ some integers have more than one representation, and the system is [redundant](/redundant-number-system/).
3. **Negation.** If $d_{k-1} \cdots d_0$ represents $x$, then $\overline{d_{k-1}} \cdots \overline{d_0}$, each digit negated, represents $-x$. No carries are involved.
4. **Sign.** If $a \le \beta - 1$, the sign of $x \ne 0$ is the sign of its leading nonzero digit. The reason is $\left| \sum_{i<j} d_i \beta^i \right| \le a(\beta^j - 1)/(\beta - 1) < \beta^j$.
5. **Carry-free addition** (Avizienis). If $\beta \ge 3$ and $\lceil (\beta + 1)/2 \rceil \le a \le \beta - 1$, two numbers can be added so that each sum digit depends only on the digits of the operands in its own position and the one below. For each position, write $p_i = x_i + y_i$ as $\beta t_{i+1} + w_i$ with a *transfer* $t_{i+1} \in \{-1, 0, 1\}$ and $|w_i| \le a - 1$. Then $s_i = w_i + t_i$ is a digit. In radix 2 this is impossible with digits $\{-1, 0, 1\}$, but a two-stage rule, which also looks at the position below, still gives addition in constant time.
6. **Conversion.** A signed-digit string converts to an ordinary one by one subtraction, $x = P - N$, where $P$ keeps the positive digits and $N$ the absolute values of the negative ones. This subtraction needs [carry propagation](/carry-propagation/), so the conversion costs what one ordinary addition costs; redundant arithmetic postpones it to the end.

## Examples and non-examples

All examples were checked by script.

- **Radix 2, digits $\{-1, 0, 1\}$.** With four digits, $7$ has exactly four representations: $0111$, $1\bar{1}11$, $10\bar{1}1$ and $100\bar{1}$. Four digits give $3^4 = 81$ strings but only the 31 values $-15, \ldots, 15$.
- **Balanced ternary**, radix 3 with digits $\{-1, 0, 1\}$: $5 = 1\bar{1}\bar{1}$, since $9 - 3 - 1 = 5$, and $100 = 11\bar{1}01$. Negation gives $-100 = \bar{1}\bar{1}10\bar{1}$.
- **Carry-free addition in radix 10** with digits $[-6, 6]$. Add $3\bar{4}62 = 2662$ and $56\bar{6}4 = 5544$. The position sums are $8, 2, 0, 6$ from the top. The 8 and the 6 are at least 6, so each sends a transfer of 1 upward and leaves $-2$ and $-4$. The sum digits are $1, \bar{2}, 2, 1, \bar{4}$, that is $10000 - 2000 + 200 + 10 - 4 = 8206 = 2662 + 5544$. No digit waited for a carry from more than one position away.
- **Conversion.** $10\bar{1}1\bar{1}_2 = 10010_2 - 00101_2 = 18 - 5 = 13$.
- **Two's complement** is a signed-digit representation in which only the top position may be negative: the word $x_{w-1} \cdots x_0$ has value $-x_{w-1}2^{w-1} + \sum_{i<w-1} x_i 2^i$, so its top digit is taken from $\{-1, 0\}$; see [two's complement](/twos-complement/).

**Non-examples.**

- **Digits too large for the sign rule.** In radix 2 with digits $[-2, 2]$, the string $1\bar{2}$ has value $2 - 2 = 0$ although its leading digit is positive: fact 4 needs $a \le \beta - 1$.
- **Digit sets without zero.** Radix 2 with digits $\{-1, 1\}$ only, as in the quotient digits of [non-restoring division](/non-restoring-division/), represents only odd numbers, because the last digit is odd. The definition asks for consecutive digits including 0, and the divider needs a final correction.
- **Carry-save form** is redundant, with digits $\{0, 1, 2\}$ in radix 2, but it is not signed; see [carry-save addition](/carry-save-addition/).

## Related definitions

- **Redundant number system.** Any positional system with more than $\beta$ digit values; signed-digit systems are the main family. See [redundant number system](/redundant-number-system/).
- **Non-adjacent form.** The canonical binary signed-digit representation with no two adjacent nonzero digits; it has the fewest nonzero digits. See [non-adjacent form](/non-adjacent-form/).
- **Booth recoding.** Rewriting a multiplier in radix 2 or 4 with signed digits, so that a run of ones becomes two nonzero digits. See [Booth multiplication](/booth-multiplication/).
- **Balanced ternary.** The nonredundant symmetric system in radix 3. See [balanced ternary](/balanced-ternary/).
- **Generalized signed-digit numbers.** Parhami's family of digit sets $[-a, b]$ with $a + b + 1 \ge \beta$, which contains the signed-digit, carry-save and ordinary systems as special cases.

### History

Negative digits were proposed for decimal arithmetic long before computers: Colson in 1726 and Cauchy in 1840 noted that digits from $-5$ to $5$ make hand multiplication easier, and balanced ternary was studied as a curiosity and built into the Setun computer at Moscow State University in 1958. For computer arithmetic, Avizienis in 1961 defined signed-digit systems for fast parallel addition and gave the conditions on the digit set. Booth's multiplier recoding of 1951 and the non-restoring and SRT dividers use the same idea of digits $\pm 1$.

## References
