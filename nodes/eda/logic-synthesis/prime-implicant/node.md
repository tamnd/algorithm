---
tag: 76W0F8
kind: definition
slug: prime-implicant
name: Prime implicant
aliases:
- prime cube
area: eda/logic-synthesis
level: intro
summary: An implicant that no longer implies the function if any literal is removed. Some minimum sum of products uses only prime implicants.
prereqs: [implicant]
see_also: [sum-of-products, dont-care-condition, quine-mccluskey, petricks-method, karnaugh-map, two-level-logic-minimization, espresso, set-cover]
sources:
  - paper: doi:10.1080/00029890.1952.11988183
    title: W. V. Quine, The problem of simplifying truth functions, American Mathematical Monthly 59(8), 521 to 531, 1952
    locator: prime implicants, and the theorem that a shortest normal formula is a sum of prime implicants
  - paper: doi:10.1080/00029890.1955.11988710
    title: W. V. Quine, A way to simplify truth functions, American Mathematical Monthly 62(9), 627 to 631, 1955
    locator: the consensus method for finding the prime implicants
  - paper: "Ashok K. Chandra and George Markowsky, On the number of prime implicants, Discrete Mathematics 24(1), 7 to 11, 1978"
    title: On the number of prime implicants
    locator: the lower bound of order 3^n/n and the upper bound of order 3^n/√n on the largest number of prime implicants of an n-variable function
  - book: isbn:9780898381641
    title: Robert K. Brayton, Gary D. Hachtel, Curtis T. McMullen and Alberto L. Sangiovanni-Vincentelli, Logic Minimization Algorithms for VLSI Synthesis, Kluwer, 1984
    locator: Chapter 2, Basic Definitions (prime and essential cubes, covers)
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 4, Synthesis of Two-Level Circuits (Quine's theorem and essential primes)
---

A prime implicant of a Boolean function $f$ is an [implicant](/implicant/) that no other implicant contains. Put another way, it is a product term that implies $f$, but stops implying $f$ when any one of its literals is removed. Quine (1952) showed why primes matter: each cube of a cover can grow to a prime that contains it, and this never adds a cube or a literal. So some minimum [sum of products](/sum-of-products/) uses only primes, and exact minimizers first list the primes and then choose some of them. A prime is essential when it alone covers some 1 point of $f$; every cover by primes must use it. The number of primes can be very large: Chandra and Markowsky (1978) showed that the largest number for $n$ variables is between orders $3^n/n$ and $3^n/\sqrt{n}$.

## Definition

Let $f$ have on-set $F$, don't-care set $D$ and off-set $R$, and let $\mathrm{Imp}(f)$ be its set of implicants, the cubes $c$ with $c \subseteq F \cup D$.

**Prime implicant.** An implicant $p$ is prime if no implicant $c$ has $p \subsetneq c$.

**Literal form.** An implicant $p$ is prime exactly when, for each literal $\ell$ of $p$, the cube $p \setminus \ell$ (the cube $p$ with $\ell$ removed) is not an implicant. Proof: if some $p \setminus \ell$ is an implicant, it contains $p$ strictly, so $p$ is not prime. Conversely, if an implicant $c$ has $p \subsetneq c$, then $c$ lacks some literal $\ell$ of $p$, and $p \subsetneq p \setminus \ell \subseteq c$, so $p \setminus \ell$ is an implicant.

**Essential prime.** A prime $p$ is essential if some minterm $m \in F$ lies in $p$ and in no other prime. Each implicant that contains $m$ lies in some prime, and that prime contains $m$, so it is $p$. Hence every cover made of primes contains every essential prime.

**Redundant primes.** The other primes are of two kinds. A non-essential prime is totally redundant if it lies inside the union of the essential primes and $D$, and partially redundant otherwise. A totally redundant prime is in no minimum cover. Partially redundant primes are where the hard choices are.

**Quine's theorem.** Let the cost of a cover be (number of cubes, number of literals), compared in this order. Then every minimum cover of $f$ consists of primes. Proof: replace each cube $c$ of a minimum cover by a prime $p \supseteq c$. The result is still a cover, since it contains the old union and stays in $F \cup D$. It has at most as many cubes, and if some $c$ was not prime, then $p$ has fewer literals than $c$, so the cost drops. That contradicts minimality. If the cost is only the number of cubes, the same step shows that some minimum cover is prime.

**Number of primes.** Each of the $3^n$ cubes can be prime for some function, but not all at once. Chandra and Markowsky (1978) proved that the largest number of primes of an $n$-variable function is $\Omega(3^n / n)$ and $O(3^n / \sqrt{n})$. The lower bound uses the function that is 1 when the number of ones in the input is between $n/3$ and $2n/3$. For $n = 1, 2, 3, 4$ the largest numbers are 1, 2, 6 and 13.

## Examples and non-examples

- **$f = x_1 x_2 + \bar{x}_1 x_3$.** The primes are $x_1 x_2$, $\bar{x}_1 x_3$ and $x_2 x_3$. The first two are essential: minterm 6 ($110$) is only in $x_1 x_2$ and minterm 1 ($001$) is only in $\bar{x}_1 x_3$. The prime $x_2 x_3$ lies inside the union of the two essential primes, so it is totally redundant. It is the consensus of the two other terms. The minimum SOP is $x_1 x_2 + \bar{x}_1 x_3$.
- **Non-example.** The minterm $x_1 x_2 x_3$ is an implicant of the same $f$, but not prime: it lies in $x_1 x_2$, and removing $x_3$ keeps an implicant.
- **A table with a choice.** Take $f = \sum m(4, 8, 10, 11, 12, 15)$ with don't-cares $d(9, 14)$ over $x_1 x_2 x_3 x_4$. Its primes are ${-}100$, $10{-}{-}$, $1{-}{-}0$ and $1{-}1{-}$. The prime ${-}100$ is essential for minterm 4, and $1{-}1{-}$ is essential for minterm 15. Minterm 8 is then left, and it lies in two primes, $10{-}{-}$ and $1{-}{-}0$. Each choice gives a minimum cover with 3 cubes and 7 literals.
- **No essential prime.** The function that is 1 unless all three inputs are equal, $\sum m(1, 2, 3, 4, 5, 6)$, has the six primes $0{-}1$, $01{-}$, ${-}01$, ${-}10$, $1{-}0$ and $10{-}$. Each minterm lies in exactly two of them, so no prime is essential. This is a cyclic table. The minimum covers have 3 primes, for example $\{0{-}1, {-}10, 10{-}\}$, while the cover $\{0{-}1, 1{-}0, {-}01, {-}10\}$ is prime and irredundant but has 4 cubes. This is the largest number of primes for 3 variables.
- **Don't-cares change the primes.** For $\sum m(1, 3, 6, 7)$ with minterm 5 as a don't-care, the primes are $x_3$ and $x_1 x_2$. The cube $\bar{x}_1 x_3$ is no longer prime because $x_3$ is now an implicant.
- **Unate functions.** For $x_1 + x_2$ the primes are $x_1$ and $x_2$, and both are essential. In a completely specified [unate function](/unate-function/) every prime is essential, so the sum of all primes is the unique minimum SOP.

The sum of all primes of $f$ is a canonical SOP of $f$. It is often called the Blake canonical form.

## Related definitions

- **[Implicant](/implicant/).** A cube inside the on-set plus the don't-care set.
- **[Quine-McCluskey](/quine-mccluskey/).** Lists all primes by merging cubes that differ in one variable, then solves the prime implicant table.
- **[Petrick's method](/petricks-method/).** Lists every irredundant choice of primes for the table, by multiplying out a product of sums.
- **[Karnaugh map](/karnaugh-map/).** Shows the primes as the largest rectangles of 1s, for up to four or five variables.
- **[Set cover](/set-cover/).** Choosing primes to cover the on-set minterms is a set cover problem, with one set for each prime.
- **[Espresso](/espresso/).** Makes each cube of a cover prime, one at a time, without listing all primes.
- **[Two-level logic minimization](/two-level-logic-minimization/).** The problem that the primes and the covering step solve.

## References
