---
tag: VSM51F
kind: problem
slug: cryptarithmetic-puzzle
name: Cryptarithmetic puzzle
aliases:
- cryptarithm
- SEND + MORE = MONEY
area: techniques/backtracking
level: intro
summary: Assign distinct digits to letters so that a written arithmetic equation holds.
prereqs: [generic-backtracking-algorithm, constraint-satisfaction-problem]
see_also: [chronological-backtracking, partial-solution, search-tree-pruning, variable-ordering-heuristics, forward-checking, brute-force-search, np-complete]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1
    locator: Section 7.2.1.2, Generating all permutations (alphametics)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 6, Constraint Satisfaction Problems (the cryptarithmetic example TWO + TWO = FOUR)
  - paper: doi:10.1145/24658.24662
    title: David Eppstein, On the NP-completeness of cryptarithms, ACM SIGACT News 18(3), 1987
    locator: pp. 38 to 40
---

A cryptarithmetic puzzle is an arithmetic equation, usually a sum, in which each digit is replaced by a letter. The task is to find an assignment of digits to letters such that different letters get different digits, no number starts with 0, and the equation holds. The standard example is SEND + MORE = MONEY, which has exactly one solution. The puzzle is a small [constraint satisfaction problem](/constraint-satisfaction-problem/) and a standard exercise for [backtracking](/generic-backtracking-algorithm/), where the column-by-column search with carries is much faster than a test of all digit assignments.

## In plain words

In the puzzle SEND + MORE = MONEY, each letter stands for one digit. Two different letters stand for two different digits. The first letter of a word is never zero. You must find the digits that make the sum correct.

You can try every way to give digits to the 8 letters, but there are almost two million ways. A better method works like a sum on paper. Start at the right column. Choose digits for the letters on top of that column. The sum then gives the digit at the bottom and the carry into the next column. If the bottom letter already has a different digit, or the digit is already in use, go back and change the last choice. Most bad choices fail after one or two columns, so the search is short.

## Definition

**Input.** A base $b \ge 2$, usually $b = 10$, and words $w_1, \ldots, w_k$ and $r$ over an alphabet of letters. The equation is $w_1 + \cdots + w_k = r$. Let $\Lambda$ be the set of letters that occur in the words, and let $\Lambda_0 \subseteq \Lambda$ be the set of first letters of words with two or more letters.

**Solution.** An injective map $\sigma : \Lambda \to \{0, 1, \ldots, b - 1\}$ such that $\sigma(x) \ne 0$ for each $x \in \Lambda_0$ and
$$\sum_{i=1}^{k} \operatorname{val}_\sigma(w_i) = \operatorname{val}_\sigma(r),$$
where for a word $a_1 a_2 \ldots a_\ell$ the value is $\operatorname{val}_\sigma(a_1 \ldots a_\ell) = \sum_{j=1}^{\ell} \sigma(a_j)\, b^{\ell - j}$.

**Output.** The decision version asks whether a solution exists. The search version asks for one solution, and the enumeration version for all of them. A well-made puzzle has exactly one solution.

Injectivity needs $|\Lambda| \le b$. In base 10 there are at most 10 letters, so a puzzle has at most $10! = 3\,628\,800$ candidate maps.

## Variants

- **Other operations.** Subtraction, multiplication and long division, in which some or all digits are replaced by letters or by stars. A puzzle that uses words with a meaning, as SEND + MORE = MONEY does, is often called an *alphametic*.
- **Leading zeros allowed.** Drop the condition on $\Lambda_0$. Then a puzzle can have many more solutions: SEND + MORE = MONEY has 25, and TWO + TWO = FOUR has 19.
- **Other bases.** The definition does not change. When $b$ is part of the input, the number of letters is not bounded.
- **Doubly true puzzles.** The words are number names, so the equation is true in words and in digits.

## Examples

**SEND + MORE = MONEY.** The letters are S, E, N, D, M, O, R and Y, so $|\Lambda| = 8$ and $\Lambda_0 = \{S, M\}$. The only solution is
$$9567 + 1085 = 10652,$$
with $S = 9$, $E = 5$, $N = 6$, $D = 7$, $M = 1$, $O = 0$, $R = 8$ and $Y = 2$.

A part of the solution follows from the columns alone. The column on the left holds only M and the carry out of the column of S and M, so $M$ is a carry and $M = 1$. The next column gives $S + 1 + c = 10 \cdot 1 + O$ with carry $c \in \{0, 1\}$, so $S \ge 8$ and $O \in \{0, 1\}$; as $M = 1$, $O = 0$.

**Search effort.** A [brute-force search](/brute-force-search/) that tests every injective map from the 8 letters to the 10 digits tests $10!/2! = 1\,814\,400$ maps. The column search of the section below, run on the same puzzle, gives digits to the letters of the top rows one at a time, from the right column to the left, and gets the digit of the bottom letter from the sum. It makes 7236 digit choices and 6248 column checks in total to list all solutions, and it finds only the one above.

**TWO + TWO = FOUR.** This puzzle has 7 solutions with nonzero first letters, for example $734 + 734 = 1468$ and $765 + 765 = 1530$. The column search makes 350 digit choices to list all 7.

**A puzzle with many solutions.** In A + A = BC, the letter $B$ is the carry out of a sum of two digits, and $B \ne 0$ as it is a first letter, so $B = 1$. Then $2A = 10 + C$, so $A \in \{5, 6, 7, 8, 9\}$ with $C = 0, 2, 4, 6, 8$. All five maps are injective, so the puzzle has 5 solutions and is not well made.

## Known algorithms

- **Brute force over permutations.** Test each injective map, which is $\frac{b!}{(b - |\Lambda|)!}$ maps with $O(L)$ work each, where $L$ is the total length of the words. Knuth uses the alphametic SEND + MORE = MONEY as a motivating example for algorithms that generate all permutations.
- **Column-wise backtracking.** Process the columns from right to left with the carry $c$ into the current column. In the column, give a digit to each top-row letter that has none yet, using only unused digits and no 0 for a letter in $\Lambda_0$. When the top-row letters of the column all have digits, let $s = c + \sum \sigma(\text{top letters})$. The bottom letter must get $s \bmod b$: if it has a digit, the digits must agree, and if it has none, the digit $s \bmod b$ must be unused. Continue with the next column and carry $\lfloor s / b \rfloor$. At the end, the carry must be 0. This is the [generic backtracking algorithm](/generic-backtracking-algorithm/) where the [partial solution](/partial-solution/) is the set of letters with digits, and each column gives a test of the prefix. Each digit choice is undone when the search returns, as in [chronological backtracking](/chronological-backtracking/).
- **Constraint propagation.** As a CSP, the puzzle has one variable for each letter and one carry variable for each column, an all-different constraint on the letters, and one linear constraint for each column, $c_{\text{in}} + \sum \text{top} = \text{bottom} + b \cdot c_{\text{out}}$. Backtracking with [forward checking](/forward-checking/) or bounds consistency on the column constraints, and with the [minimum remaining values](/minimum-remaining-values/) order, removes most of the search; on SEND + MORE = MONEY, propagation alone fixes $M = 1$ and $O = 0$, as above.
- **One linear equation.** Write the sum as $\sum_{x \in \Lambda} a_x \sigma(x) = 0$, where $a_x$ is the sum of the place values $b^{j}$ at which $x$ occurs in a top word, less those at which it occurs in $r$. For SEND + MORE = MONEY, this is $1000S + 91E - 90N + D - 9000M - 900O + 10R - Y = 0$. A backtracking search over this one equation can prune with the bounds of the remaining terms.

## Bounds

- **Fixed base.** In base 10 there are at most $10!$ maps, so every puzzle is solved in time linear in its length. The interest of the problem is in the constant: the column search is many times faster than the brute force on typical puzzles.
- **Base in the input.** Eppstein (1987) proved that deciding whether a cryptarithm has a solution is NP-complete. The hardness needs the base and the number of letters to grow with the input, as the fixed-base problem is solved in linear time. The problem is in NP because a map $\sigma$ is a certificate that is checked in polynomial time.

## Reductions

- **To a CSP.** The model above, with letter variables, carry variables, column constraints and one all-different constraint.
- **To integer programming.** The single linear equation, with binary variables $y_{x,d}$ for "letter $x$ gets digit $d$", gives a 0-1 integer program with one row for each letter, one row for each digit and the equation.
- **From an NP-complete problem.** Eppstein's NP-completeness proof is a reduction to the decision version with a base that grows with the input. The page does not restate it.

## Applications

- **Teaching.** It is a standard first example of a CSP and of backtracking with column constraints and carries, and of the large gain from pruning on partial solutions over [generate and test](/generate-and-test/).
- **Recreational mathematics.** A puzzle setter can use the enumeration version to check that a new puzzle has exactly one solution.

## References
