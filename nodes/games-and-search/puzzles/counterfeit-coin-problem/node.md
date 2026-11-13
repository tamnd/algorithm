---
tag: ASZJ2T
kind: problem
slug: counterfeit-coin-problem
name: Counterfeit coin problem
aliases:
- Coin weighing problem
- Twelve coins puzzle
area: games-and-search/puzzles
level: intro
summary: Find the one fake coin, heavier or lighter, among N coins with a balance scale. In w weighings at most (3^w - 3)/2 coins can be done, so 12 coins need 3 weighings (Dyson 1946).
prereqs: [information-theoretic-bound, decision-tree-method]
see_also: [adversary-argument, decision-tree-model, lower-bound, ternary-search, twenty-questions-problem]
sources:
  - paper: doi:10.2307/3611225
    title: Freeman J. Dyson, Note 1931, The problem of the pennies, The Mathematical Gazette 30(291), 1946, 231 to 234
    locator: the whole note (the bound 2N <= 3^w - 3, the matching non-adaptive scheme from ternary labels, and the case with one extra genuine coin)
  - paper: "Richard K. Guy and Richard J. Nowakowski, Coin-weighing problems, The American Mathematical Monthly 102(2), 1995, 164 to 167"
    locator: the whole article (a survey of the variants and their literature)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, 2nd edition, Addison-Wesley, 1998
    locator: Section 5.3.1 (decision trees and the information-theoretic lower bound for comparison problems)
---

The counterfeit coin problem gives $N$ coins that look the same, one of which is fake and is either heavier or lighter than the others, and a balance scale with two pans. Find the fake coin, and say whether it is heavy or light, with as few weighings as possible. Each weighing has three outcomes, so $w$ weighings tell apart at most $3^w$ cases, which is the [information-theoretic bound](/information-theoretic-bound/); a sharper count gives $N \le (3^w - 3)/2$, and Dyson (1946) showed that every $N$ from 3 to $(3^w - 3)/2$ can be done, even with all weighings fixed in advance. So 12 coins need exactly 3 weighings, and 13 coins can be done in 3 only with one extra coin known to be genuine. The name "coin weighing problem" is also used for a different problem, in which an accurate scale weighs sets of coins to find all fake coins.

## In plain words

You have a pile of coins. One of them is a fake, and you do not know whether it is too heavy or too light. You have a scale with two pans that only tells you which side is heavier, or that the sides are equal.

Each use of the scale gives one of three answers. So a few weighings can only tell apart a limited number of possibilities, and each coin gives two possibilities, heavy or light. With three weighings, twelve coins is the most you can handle, and only if every weighing splits the possibilities as evenly as possible.

The trick is to put some coins on the left, some on the right, and leave some off, so that every answer leaves about a third of the possibilities. With a good plan you can even write down all three weighings before you start.

## Definition

Coins are $1, \ldots, N$. A *case* is a pair $(i, t)$ with $i$ the fake coin and $t \in \{\text{heavy}, \text{light}\}$, so there are $2N$ cases. A *weighing* is a pair of disjoint sets $(A, B)$ of coins with $|A| = |B|$. In case $(i, \text{heavy})$ the result is "left" if $i \in A$, "right" if $i \in B$ and "equal" otherwise; in case $(i, \text{light})$ left and right swap.

An *adaptive strategy* with $w$ weighings is a ternary [decision tree](/decision-tree-model/) of depth at most $w$: each inner node holds a weighing and has one child for each result. It *solves* the problem when the cases that reach each leaf all name the same coin and type. A *non-adaptive strategy* is a list of $w$ weighings fixed in advance, so that the $2N$ cases give $2N$ different result words.

- **Decision.** Given $N$ and $w$, is there a strategy?
- **Optimization.** Given $N$, the least $w$.
- **With a reference.** The same, with one extra coin known to be genuine.

## Variants

- **The fake is known to be heavy.** Then $N$ cases, and $N \le 3^w$ is necessary and enough: split the coins into three groups as equal as possible, weigh two of them, and recurse on the group that holds the fake. This is [ternary search](/ternary-search/) on a balance.
- **One extra genuine coin.** The bound becomes $N \le (3^w - 1)/2$, so 13 coins in 3 weighings and 40 coins in 4.
- **Non-adaptive schemes.** Dyson's labeling below; all weighings are written down at the start.
- **Several fake coins, or a fake coin that may not exist.** These add cases and change the counts; Guy and Nowakowski (1995) survey them.
- **The spring-scale problem.** A scale that shows the total weight of a set of coins, used to find all the light coins. This is a different problem, about the number of subset weighings needed, and is not covered here.

## Examples

**The 12 coins in 3 weighings, adaptive.** Weigh $\{1, 2, 3, 4\}$ against $\{5, 6, 7, 8\}$.

- *Equal.* The fake is among 9 to 12, and coins 1 to 8 are genuine. Weigh $\{9, 10, 11\}$ against $\{1, 2, 3\}$. If equal, weigh 12 against 1 to get its type. If the left pan is heavy, the fake is a heavy one of 9, 10, 11; weigh 9 against 10, and the heavier one is the fake, or 11 if they balance. A light left pan works the same way.
- *Left heavy.* Either one of 1 to 4 is heavy or one of 5 to 8 is light: 8 cases. Weigh $\{1, 2, 5\}$ against $\{3, 6, 9\}$, where 9 is genuine. Left heavy leaves 1 or 2 heavy or 6 light; weigh 1 against 2. Right heavy leaves 3 heavy or 5 light; weigh 3 against 9. Equal leaves 4 heavy or 7, 8 light; weigh 7 against 8.
- *Right heavy.* The same with the two groups swapped.

Every branch ends with one case after the third weighing, for all 24 cases.

**The 12 coins in 3 weighings, fixed in advance.** Give each coin a word of three digits from $\{0, 1, 2\}$:

| coin | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| word | 001 | 010 | 011 | 012 | 100 | 202 | 102 | 220 | 221 | 210 | 121 | 122 |

In weighing $j$, the coins with digit 1 in place $j$ go on the left pan and those with digit 2 go on the right pan:

- weighing 1: $\{5, 7, 11, 12\}$ against $\{6, 8, 9, 10\}$;
- weighing 2: $\{2, 3, 4, 10\}$ against $\{8, 9, 11, 12\}$;
- weighing 3: $\{1, 3, 9, 11\}$ against $\{4, 6, 7, 12\}$.

Write the results as a word with left $= 1$, right $= 2$ and equal $= 0$. A heavy coin gives its own word; a light coin gives its word with 1 and 2 swapped. The 12 words and their 12 swaps are the 24 words with not all digits equal, so every case gives a different word. For example, the results right, equal, left give $201$, the swap of $102$, so coin 7 is light. Each pan holds 4 coins because, in each place, as many words have a 1 as a 2. Dyson (1946) built such a set of words for every $N$ from 3 to $(3^w - 3)/2$.

**The bound.** For $w \ge 1$ weighings and no reference coin, a strategy exists only if $2N \le 3^w - 3$; with one extra genuine coin, only if $2N \le 3^w - 1$. *Proof.* First a lemma: if no weighing so far has been unbalanced, the remaining $u \ge 1$ suspects give $2u$ cases, and $w'$ more weighings can solve them only if $2u \le 3^{w'} - 1$. Follow the branch where all remaining results are "equal". A fake coin that is put on a pan in one of these weighings unbalances it, so only the cases of coins never weighed on this branch reach its leaf. A coin never weighed gives two cases, heavy and light, at the same leaf, so no coin can be left unweighed, and this leaf receives no case. The $2u$ cases then go to the other $3^{w'} - 1$ leaves, at most one each. This proves the bound with a reference coin, with $u = N$ and $w' = w$. Without a reference, the first weighing puts $k \ge 1$ coins against $k$ coins. If the left pan is heavy, $2k$ cases remain ($k$ heavy and $k$ light), so $2k \le 3^{w-1}$, and since $3^{w-1}$ is odd, $2k \le 3^{w-1} - 1$. The same holds for "right". If the pans balance, $N - 2k$ suspects remain, and by the lemma $2(N - 2k) \le 3^{w-1} - 1$. Adding the three bounds gives $2N \le 3(3^{w-1} - 1) = 3^w - 3$. $\square$

An exhaustive search over all adaptive strategies, which only needs to track how many coins are unknown, possibly heavy, possibly light or genuine, gives the exact sets: for $w = 2, 3, 4$ the solvable $N$ are 3 to 3, 3 to 12 and 3 to 39, and with a reference coin 1 to 4, 1 to 13 and 1 to 40. One or two coins can never be solved without a reference, since a weighing of coin 1 against coin 2 cannot tell "1 heavy" from "2 light".

## Known algorithms

- **Balanced splitting.** At each node choose the weighing so that each of the three results leaves at most $3^{w'-1}$ cases and the "equal" branch keeps a usable form. Dyson's constructions do this for every feasible $N$ in time polynomial in $N$.
- **Ternary labels.** For the non-adaptive scheme, choose $N$ ternary words of length $w$, no two equal or swaps of each other and none all 0s, with as many 1s as 2s in each place. Decoding is a table lookup of the result word.
- **Exhaustive search.** For small $N$ and $w$, a search over weighings by the counts of the four kinds of coins decides feasibility exactly; this is the [decision tree method](/decision-tree-method/) run by computer.

## Bounds

- **Information.** $2N$ cases and 3 results per weighing give $w \ge \lceil \log_3 (2N) \rceil$, the [information-theoretic bound](/information-theoretic-bound/) for ternary decision trees.
- **Exact.** $w = \lceil \log_3 (2N + 3) \rceil$ for $N \ge 3$ without a reference coin, and $w = \lceil \log_3 (2N + 1) \rceil$ with one, by the bound above and Dyson's constructions.
- **Known heavy.** $w = \lceil \log_3 N \rceil$.

## Reductions

- **To ternary decision trees.** A strategy is a ternary decision tree whose leaves are the cases; the bounds above are leaf counts, and the "equal" branch argument is an [adversary argument](/adversary-argument/) that always answers "equal".
- **To a code.** A non-adaptive scheme is a set of ternary words, one per coin, such that the words and their swaps are all different: a small code design problem.

## Applications

- **Teaching lower bounds.** The puzzle is a standard first example of an information-theoretic lower bound and of why a bound by counting leaves need not be tight: $3^3 = 27$ leaves would allow 13 coins, and the sharper argument gives 12.
- **Testing with a three-way comparison.** Any test that answers less, equal or greater, applied to sets of items, has the same structure, and the same bounds hold.

## References
