---
tag: 2TJFYV
kind: technique
slug: rule-of-product
name: Rule of product
aliases:
- multiplication principle
- product rule
area: combinatorics/counting-algorithms
level: intro
summary: A counting principle stating that when a choice is made in successive independent steps, the total number of outcomes is the product of the counts at each step.
prereqs: [rule-of-sum]
see_also: [rule-of-sum, binomial-coefficient, factorial, permutation, divisor-function, counting-argument, double-counting]
sources:
  - book: isbn:9780073383095
    title: Kenneth H. Rosen, Discrete Mathematics and Its Applications, seventh edition
    locator: Section 6.1, The Basics of Counting (the product rule and the division rule)
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Section 2.1, Four Basic Counting Principles (the multiplication principle and the division principle)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C.1, Counting (rules of sum and product, strings, permutations)
---

The rule of product says that if an object is built by a sequence of $k$ choices, and the $i$-th choice always has $n_i$ options whatever the earlier choices were, then there are $n_1 n_2 \cdots n_k$ objects. In terms of sets, the Cartesian product $A_1 \times \cdots \times A_k$ has $|A_1| \cdots |A_k|$ elements. It counts strings, functions, subsets, [permutations](/permutation/) and the cost of nested loops, and it is the second basic tool of counting after the [rule of sum](/rule-of-sum/).

## In plain words

A lunch has one soup out of three and one salad out of four. For each soup there are four salads to go with it, so there are twelve lunches. That is the rule: when you make one choice after another, and each step always offers the same number of options, you multiply the numbers.

The options at a later step may depend on the earlier choices, but their number may not. When you pick a first and a second winner from ten runners, the second pick has nine options whatever the first pick was. Also, each sequence of choices must give a different object. If two different sequences give the same object, you count that object more than once.

## When it applies

- Each object is described by a fixed number of choices, made in a fixed order: the characters of a string, the values of a function, the rows of a table, the digits of a number.
- The number of options at each step is the same for all earlier choices. The set of options may change.
- The description is a bijection: each object has exactly one sequence of choices, and each sequence gives a valid object.

## The template

Notation: $|S|$ is the size of a finite set $S$, and $[n] = \{1, \ldots, n\}$.

**Rule of product.** Let $T$ be a finite set of sequences $(x_1, \ldots, x_k)$. Assume that for each $i$ from 1 to $k$, and for each prefix $(x_1, \ldots, x_{i-1})$ of a sequence in $T$, exactly $n_i$ values $x_i$ extend the prefix to a prefix of a sequence in $T$. Then $|T| = n_1 n_2 \cdots n_k$. In particular, $|A_1 \times \cdots \times A_k| = |A_1| \cdots |A_k|$ for finite sets $A_i$.

*Proof.* By induction on $k$. For $k = 0$, $T$ holds only the empty sequence and the empty product is 1. For $k \ge 1$, let $P$ be the set of prefixes $(x_1, \ldots, x_{k-1})$ of the sequences in $T$. By the hypothesis for $i \le k - 1$ and the induction hypothesis, $|P| = n_1 \cdots n_{k-1}$. Split $T$ by the prefix: the sequences with prefix $p$ form a set $T_p$, and each sequence has exactly one prefix, so the sets $T_p$ are disjoint and cover $T$. By the hypothesis for $i = k$, each $T_p$ has $n_k$ elements. The [rule of sum](/rule-of-sum/) gives $|T| = \sum_{p \in P} n_k = |P| \cdot n_k$. For the Cartesian product, the options for $x_i$ are always $A_i$, so $n_i = |A_i|$. $\square$

```pseudo id=main
COUNT-BY-STAGES(S)
L1  encode each object of S as a sequence (x_1, ..., x_k)           ▷ hole: the encoding
L2  check: the encoding is one to one and onto S                     ▷ no object twice, none missing
L3  for i ← 1 to k do
L4      n_i ← the number of options for x_i, given x_1, ..., x_(i−1)   ▷ hole: must not depend on them
L5  return n_1 · n_2 · ... · n_k
```

Line L2 makes $|S| = |T|$, where $T$ is the set of codes. Line L4 is the hypothesis of the rule: the number $n_i$ is the same for every prefix. When the number does depend on the prefix, split by the prefix with the rule of sum, or choose another order of the choices (see the pitfalls).

## Classic examples

**1. Strings.** There are $q^n$ strings of length $n$ over an alphabet of $q$ symbols. A license plate of three letters and three digits has $26^3 \cdot 10^3 = 17{,}576{,}000$ forms.

**2. Subsets.** Encode a subset $A \subseteq [n]$ by the bits $x_i = [i \in A]$. This is a bijection with $\{0, 1\}^n$, so $[n]$ has $2^n$ subsets. See [power set enumeration](/power-set-enumeration/).

**3. Functions, injections, permutations.** A function from $[k]$ to $[n]$ is a sequence of $k$ values, so there are $n^k$ functions. For a one-to-one function, the $i$-th value has $n - i + 1$ options (the values not used yet), so there are $n(n-1)\cdots(n-k+1) = n!/(n-k)!$ of them for $k \le n$. With $k = n$ this is $n!$, the number of [permutations](/permutation/) (see [factorial](/factorial/)). Dividing by the $k!$ orders of each $k$-subset gives the [binomial coefficient](/binomial-coefficient/).

**4. Divisors.** If $N = p_1^{a_1} \cdots p_r^{a_r}$ with distinct primes $p_i$, a divisor of $N$ is $p_1^{b_1} \cdots p_r^{b_r}$ with $0 \le b_i \le a_i$, and by unique factorization each divisor has one such form. So $N$ has $(a_1 + 1) \cdots (a_r + 1)$ divisors. For $720 = 2^4 \cdot 3^2 \cdot 5$ this is $5 \cdot 3 \cdot 2 = 30$. See the [divisor function](/divisor-function/).

**5. Boolean functions.** A function from $\{0, 1\}^n$ to $\{0, 1\}$ chooses one of 2 values for each of the $2^n$ inputs, so there are $2^{2^n}$ of them: 256 for $n = 3$ and 65,536 for $n = 4$. Shannon's [counting argument](/counting-argument/) compares this number with the number of small circuits.

**6. Nested loops.** A loop over $i \in [n]$ with an inner loop over $j \in [m]$ runs its body once for each pair $(i, j)$, so $nm$ times. A loop over the pairs $i < j$ of $[n]$ runs $\binom{n}{2}$ times, which needs the division rule below.

## Variations

- **Division rule.** If a map from a set $T$ onto a set $S$ sends exactly $d$ elements of $T$ to each element of $S$, then $|S| = |T| / d$. Example: there are $5 \cdot 4 = 20$ ordered pairs of distinct people from 5, each committee of two comes from $d = 2$ of them, so there are 10 committees. Seating $n$ people at a round table, where rotations give the same seating, gives $n!/n = (n-1)!$ seatings. This is a case of [double counting](/double-counting/).
- **Sets of functions.** $|B^A| = |B|^{|A|}$, where $B^A$ is the set of functions from $A$ to $B$. This is the source of the notation $2^S$ for the power set.
- **Generating functions.** The Cartesian product of two combinatorial classes, with sizes that add, has the generating function $A(z) B(z)$. See [generating functions](/generating-functions/).
- **Probability.** For independent random choices, the probability of a joint outcome is the product of the probabilities. With uniform choices, this is the rule of product divided by the total count.

## Pitfalls

- **The number of options depends on the earlier choices.** Count the two-digit numbers with two different digits. If you choose the first digit first, it has 9 options (not 0) and the second has 9 (not the first), so $9 \cdot 9 = 81$. If you choose the second digit first, it has 10 options, and the first digit then has 9 options when the second digit is 0 but 8 options otherwise. The rule does not apply in that order. A split by the rule of sum gives $9 + 9 \cdot 8 = 81$.
- **Order that does not matter.** Choosing a team of 2 from 5 people as "5 options, then 4 options" counts each team twice, once in each order. The answer is $20 / 2 = 10$, not 20.
- **A choice that is not part of the object.** The number of 4-digit PINs with no two equal adjacent digits is $10 \cdot 9 \cdot 9 \cdot 9 = 7290$, because each digit only has to differ from the one before it. If you also ask it to differ from all earlier digits, you count a different set.
- **Overlapping options across steps.** In "choose a president and then a treasurer", the same person may not hold both roles. If the second step still offers all $n$ people, you count $n^2$ pairs, not $n(n-1)$.

## Exercises

1. Show that a set of $n$ elements has $2^{n^2}$ binary relations.
2. Show that $10! = 2^8 \cdot 3^4 \cdot 5^2 \cdot 7$ has 270 divisors.
3. Count the strings of length $n$ over $\{a, b, c\}$ in which no two adjacent letters are equal, and show that the answer is $3 \cdot 2^{n-1}$ for $n \ge 1$.

## References
