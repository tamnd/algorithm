---
tag: V8CF6R
kind: technique
slug: digit-dynamic-programming
name: Digit dynamic programming
aliases:
- digit DP
area: techniques/dynamic-programming
level: advanced
summary: Count integers in a range with a digit-based property by DP over digit positions.
prereqs: [memoization, tabulation]
see_also: [bitmask-dp, memoization, transfer-matrix-method, prefix-sums]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage, 2013
    locator: Chapter 1, Regular Languages, Section 1.1, Finite Automata (deterministic automata and the product construction)
  - book: isbn:9783030393564
    title: Antti Laaksonen, Guide to Competitive Programming, second edition, Springer, 2020
    locator: Chapter 6, Dynamic Programming (counting solutions with a recursive state)
---

Digit dynamic programming counts the integers $x$ in a range $[0, N]$ whose decimal digits have some property, such as a given digit sum, or no two equal adjacent digits, by a recursion over the digit positions of $N$ from the most significant to the least. The state is the position, a small summary of the digits chosen so far, and one bit that tells whether the prefix still equals the prefix of $N$. The number of states is the number of digits times the size of the summary times 2, so the time does not depend on $N$ itself but only on its length. A range $[a, b]$ is handled as $g(b) - g(a - 1)$.

## In plain words

Suppose you must count the numbers up to some large limit whose digits add up to 10. The limit can have 18 digits, so you cannot check each number.

Write the numbers with the same length as the limit, with zeros in front. Choose the digits from left to right. As long as your digits copy the limit exactly, the next digit cannot be larger than the next digit of the limit. Once you choose a smaller digit at some place, the rest of the digits are free. For the free part, the answer depends only on how many places are left and how much digit sum is still needed. So the same small questions come up again and again, and you answer each one once.

## When it applies

- The question is "how many integers in $[a, b]$ have property $P$", or "what is the sum of some function over them", with $b$ up to $10^{18}$ or much more.
- $P$ can be checked by reading the digits from left to right while keeping a small amount of memory: a running sum, a remainder modulo $m$, the last digit, a set of digits seen, or a state of a finite automaton.
- In other words, $P$ restricted to strings of a fixed length is a regular language, and the summary is the state of a deterministic automaton that accepts it.

## The template

Let $d_0 d_1 \cdots d_{L-1}$ be the digits of $N$, most significant first, and let $\delta$ be the step of the automaton for $P$. The holes are the start state, $\delta$ and the test of acceptance.

```pseudo id=main
COUNT(p, q, tight)                                 ▷ positions p..L−1 remain, automaton in state q
L1  if p = L then return [accept(q)]               ▷ hole: the test at the end
L2  if memo[p, q, tight] is set then return it
L3  hi ← d_p if tight else 9
L4  total ← 0
L5  for x ← 0 to hi do
L6      total ← total + COUNT(p + 1, δ(q, x), tight and x = hi)   ▷ hole: the step δ
L7  memo[p, q, tight] ← total
L8  return total

DIGIT-DP(N)
L9  return COUNT(0, q₀, true)                      ▷ hole: the start state q₀
```

**Why it counts each $x \le N$ once.** Write each $x$ in $[0, N]$ with exactly $L$ digits, with zeros in front. The recursion walks a tree in which a path from the root to a leaf is a string of $L$ digits. With $tight$ true, line L3 allows only digits up to $d_p$, and the flag stays true only when $x = d_p$. So the strings reached are exactly those that are at most $N$ in the lexicographic order, which for strings of the same length is the numeric order. Each string reaches line L1 once, with the automaton in the state after reading it.

**Why the memo is valid.** The count of line L5 depends only on $p$, $q$ and $tight$: the digits that remain and their limits are fixed by these three values, and the automaton forgets everything else.

**Cost.** There are at most $2 L |Q|$ states, each with at most 10 steps, so the time is $O(10 \cdot L \cdot |Q|)$ and the space is $O(L \cdot |Q|)$. Only $L$ of the states have $tight$ true, so the table with $tight$ false can be shared between calls for different $N$.

## Classic examples

### Digit sum equal to 10, up to 345

Let $P$ be "the digit sum is 10", and let the automaton state be the sum still needed, so $q_0 = 10$, $\delta(q, x) = q - x$ (dead below 0), and the end test is $q = 0$. Let $free(k, s)$ be the number of strings of $k$ digits with sum $s$, which is the memo entry with $tight$ false. For two digits, $free(2, s) = s + 1$ for $s \le 9$ and $free(2, 10) = 9$.

For $N = 345$:

- First digit 0, 1 or 2 (below 3, so free): $free(2, 10) + free(2, 9) + free(2, 8) = 9 + 10 + 9 = 28$.
- First digit 3 (tight), sum 7 still needed. Second digit 0 to 3 (below 4, so free): $free(1, 7) + free(1, 6) + free(1, 5) + free(1, 4) = 4$.
- First digits 3, 4 (tight), sum 3 still needed. Third digit at most 5: only 3 works, which gives 1.

The total is $28 + 4 + 1 = 33$, and a direct check of the 346 numbers $0, \ldots, 345$ gives 33. For the range $[1000, 2024]$ the answer is $g(2024) - g(999) = 57$.

### Other properties

- **Divisible by $m$.** The state is the remainder of the prefix modulo $m$, with $\delta(r, x) = (10 r + x) \bmod m$.
- **No two adjacent equal digits.** The state is the last digit, plus a flag for "no nonzero digit yet", since the zeros in front are not real digits.
- **Contains the string 13.** The state is a state of the string matching automaton of the pattern, as in [Aho-Corasick](/aho-corasick/) for several patterns.
- **Sum of digit sums.** Store in each state a pair (count, sum) and combine the pairs in line L6.
- **Other bases.** Replace 9 by $b - 1$. In base 2, the method counts the integers up to $N$ with a given number of 1 bits.

## Variations

- **Leading zeros.** When $P$ depends on the real first digit (for example "no two adjacent digits equal", or "the digits are distinct"), add a flag $started$ to the state. While it is false, a zero is a filler and does not update $q$.
- **Lower and upper limits together.** Instead of $g(b) - g(a - 1)$, keep two flags, one for the lower limit and one for the upper. This is needed when $a - 1$ is hard to form, as with strings, or when the answer is not a count but a minimum or a witness.
- **The $k$-th number with the property.** Use the counts to choose the digits from left to right: at each position, skip the digits whose subtree has fewer than the remaining $k$ numbers.
- **Large ranges and fixed $|Q|$.** For $L$ in the millions with a small automaton, the free counts are powers of the transition matrix of the automaton, as in the [transfer matrix method](/transfer-matrix-method/).

## Pitfalls

- **Memoizing the tight states as free ones.** If the memo key leaves out $tight$, a state reached with $tight$ true reuses a count made with all digits free, which overcounts.
- **The number 0.** The method counts $x = 0$ as the string of $L$ zeros. Decide whether 0 belongs to the answer and correct for it, for example when the range starts at 1.
- **Leading zeros that change the property.** For "every digit is odd", the string 007 has zeros, but the number 7 does not. Use the $started$ flag.
- **Computing $g(a - 1)$ for $a = 0$.** Treat $g(-1) = 0$.
- **Clearing the memo between calls.** Entries with $tight$ true depend on $N$ and must not be reused for another limit.

## Exercises

1. Count the integers in $[1, 10^{18}]$ that are divisible by the sum of their digits.
   <details><summary>Hint</summary>Fix the target digit sum $s$ for $s = 1, \ldots, 162$, and run a digit DP with the state (sum so far, remainder modulo $s$).</details>
2. Count the integers in $[0, N]$ whose decimal digits are all distinct. What is the state, and how many states are there?
3. Using the free counts, find the 100th positive integer whose digit sum is 10.
4. Show that the property "the digit sum is a prime" can be handled by the template with an automaton of 163 states for numbers below $10^{18}$.

## References
