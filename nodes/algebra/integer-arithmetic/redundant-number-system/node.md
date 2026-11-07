---
tag: 3X95VC
kind: concept
slug: redundant-number-system
name: Redundant number system
aliases:
- redundant representation
- redundant number representation
- redundant digit set
area: algebra/integer-arithmetic
level: advanced
summary: Number system with more digit values than the radix, allowing carry-free addition.
prereqs: [positional-number-system, carry-propagation]
see_also: [signed-digit-representation, carry-save-addition, non-adjacent-form, wallace-tree-multiplier, srt-division, skew-binary-random-access-list, brodal-queue, residue-number-system]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 3, Redundant number systems (the carry problem, digit sets and redundancy, generalized signed-digit numbers, carry-free and limited-carry addition, conversion)
  - paper: A. Avizienis, Signed-digit number representations for fast parallel arithmetic, IRE Transactions on Electronic Computers EC-10(3), 1961
    title: Algirdas Avizienis, Signed-digit number representations for fast parallel arithmetic
    locator: pp. 389 to 400 (redundant signed-digit systems and totally parallel addition)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press, 1998
    locator: Chapter 9, Numerical representations (redundant binary numbers with digits 0, 1 and 2, and skew binary numbers)
---

A redundant number system is a positional system in radix $\beta$ whose digit set has more than $\beta$ values, so that some numbers can be written in more than one way. With digits 0, 1 and 2 in radix 2, for example, the number 2 is both $10$ and $02$. This freedom is used to stop carries. In ordinary addition one carry can run through every position, which is why the [carry propagation](/carry-propagation/) of an $n$-digit adder takes time growing with $n$. In a redundant system an addition can leave a digit "too large" and absorb the extra later, so every digit of the sum depends only on a few nearby digits of the operands, and addition takes constant time whatever the length. The price is that comparison, sign detection and conversion to ordinary form still need a full carry-propagating step, so redundant forms are used *inside* long computations: fast multipliers and dividers in hardware, and counters in data structures with worst-case constant-time increments.

## In plain words

When you add two long numbers by hand, a single carry can ripple all the way from the right end to the left: $99999 + 1$ changes every digit. A machine must wait for that ripple before it knows the answer.

A redundant number system allows extra digits, such as a digit "2" in binary. Then a sum does not have to be tidied up at once. Each position can hold a little more than usual, and the tidying is done later, once, at the end. So many additions in a row can each be done in a fixed short time, however long the numbers are.

## The idea

**Digit sets.** In radix $\beta$ with digit set $D$, a string $d_{k-1} \cdots d_0$ has value $\sum d_i\beta^i$. With $|D| = \beta$ and $D = \{0, \ldots, \beta - 1\}$ every nonnegative integer has exactly one representation, the [positional number system](/positional-number-system/). With $|D| > \beta$ and $D$ a set of consecutive integers, representations exist but are no longer unique; $|D| - \beta$ measures the *redundancy*. The two main families are:

- **Carry-save digits**, $D = \{0, 1, 2\}$ in radix 2. A digit is the sum of two binary digits, so a carry-save number is just a pair of binary numbers whose sum is the value.
- **Signed digits**, $D = \{-a, \ldots, a\}$ with $2a + 1 > \beta$, such as $\{-1, 0, 1\}$ in radix 2; see [signed-digit representation](/signed-digit-representation/).

Parhami's *generalized signed-digit* systems, with $D = \{-a, \ldots, b\}$ and $a + b + 1 > \beta$, contain both.

**Why carries stop.** To add digit by digit, write each position sum $p_i = x_i + y_i$ as $\beta t_{i+1} + w_i$, with a transfer $t_{i+1}$ to the next position and an interim digit $w_i$, and set $s_i = w_i + t_i$. In an ordinary system, $s_i$ may overflow and need another transfer, and so on up the number. With enough redundancy, $t_{i+1}$ and $w_i$ can be chosen so that $w_i + t_i$ is always a digit, whatever $t_i$ is. Then the transfers move at most one place, and every sum digit depends on two positions of the operands only. Avizienis gave the condition for signed digits in radix $\beta \ge 3$: $\lceil (\beta + 1)/2 \rceil \le a \le \beta - 1$. In radix 2, and in carry-save form, the rule needs two stages, but the depth is still constant.

**What is lost.** The value of a redundant number is not visible from its leading digits alone: $10$ and $02$ are equal, and in signed digits $1\bar{1}\bar{1} = 1$ has a positive leading digit in the same place as $011 = 3$ but is smaller. Comparison, sign detection, overflow detection and conversion to the ordinary form need a carry-propagate addition, once. The design rule is therefore to stay redundant for as many operations as possible and convert at the end.

**Counting with redundant digits.** The same idea gives counters whose increment touches $O(1)$ digits in the worst case. A plain binary counter has amortized $O(1)$ increments but a worst case of $\Theta(k)$, when $0111\cdots1$ becomes $1000\cdots0$; see [binary counter increment](/binary-counter-increment/). With digits 0, 1 and 2 and a regularity condition on where the 2s may stand, an increment can be done by changing a constant number of digits: turn a 2 into 0 and add 1 to the digit above it, then add 1 at the bottom. Skew binary numbers, with weights $2^{i+1} - 1$, digits 0, 1 and 2, and only the lowest nonzero digit allowed to be 2, have the same property with a very simple rule.

## Examples

All examples were checked by script.

- **Redundancy.** In radix 2 with digits 0, 1 and 2, three digits give the values $0$ to $14$. The value 4 has three representations, $100$, $020$ and $012$, while $7 = 111$ has only one.
- **Carry-save addition of three numbers.** $13 + 11 + 7$: the bitwise sum is $1101 \oplus 1011 \oplus 0111 = 0001$, and the carries, the majority of each column shifted left, are $11110$. So $13 + 11 + 7$ is held as the pair $(1, 30)$, found in one step of full adders with no carry chain. One ordinary addition gives $31$ at the end. See [carry-save addition](/carry-save-addition/).
- **Signed-digit addition in radix 10** with digits $-6$ to $6$: $3\bar{4}62 + 56\bar{6}4 = 1\bar{2}21\bar{4}$, that is $2662 + 5544 = 8206$, with every transfer moving one place; the details are on the [signed-digit](/signed-digit-representation/) page.
- **Skew binary counting.** $0, 1, 2, 10, 11, 12, 20, 100, 101, 102, 110, 111, 112, 120, 200, 1000$ are the numbers 0 to 15. Each step either adds 1 to the last digit or turns the lowest 2 into 0 and adds 1 to the digit above it: never more than two digits change. Here $1000 = 15$, since the weights are $1, 3, 7, 15$.
- **A non-example.** Decimal with digits 0 to 9 is not redundant: $99999 + 1$ changes all six digits, and no rule can avoid it.

## Where it is used

- **Multipliers.** A [Wallace tree multiplier](/wallace-tree-multiplier/) adds the partial products in carry-save form, reducing them three to two in constant depth per level, and converts once with a fast adder.
- **Dividers and square roots.** [SRT division](/srt-division/) keeps the partial remainder in carry-save or signed-digit form and chooses quotient digits from $\{-1, 0, 1\}$ or a larger set by looking at a few leading digits. The quotient itself is redundant and is converted on the fly.
- **Online arithmetic.** Ercegovac's online arithmetic computes digits most significant first, which is possible only with a redundant output.
- **Recoding.** The [non-adjacent form](/non-adjacent-form/) and Booth recoding pick a sparse representation among many, to save additions in multiplication and exponentiation.
- **Data structures.** Okasaki's numerical representations build lists, heaps and random access lists from redundant counters. The [skew binary random access list](/skew-binary-random-access-list/) uses skew binary numbers for $O(1)$ worst-case cons and tail, and the [Brodal queue](/brodal-queue/) uses redundant counters to keep its worst-case bounds.
- **Not redundant in this sense.** A [residue number system](/residue-number-system/) also has carry-free addition, but each number has one representation; it removes carries by working modulo several coprime numbers, not by extra digits.

## References
