---
tag: NM29E3
kind: technique
slug: generate-and-test
name: Generate-and-test
aliases:
- enumerate-and-check
- generate and test
- British Museum algorithm
area: combinatorics/exhaustive-search
level: intro
summary: Generate candidates one at a time and test each against the constraints.
prereqs: [search-space, brute-force-search]
see_also: [brute-force-search, generic-backtracking-algorithm, cryptarithmetic-puzzle, search-space, search-tree-pruning, n-queens-problem, combinatorial-generation, constraint-satisfaction-problem]
sources:
  - book: isbn:9780201533774
    title: Patrick Henry Winston, Artificial Intelligence, third edition, Addison-Wesley, 1992
    locator: Chapter 3, Generate and test, means-ends analysis, and problem reduction
  - paper: doi:10.1145/360018.360022
    title: Allen Newell and Herbert A. Simon, Computer science as empirical inquiry, symbols and search, Communications of the ACM 19(3), 1976
    locator: Part II, heuristic search (generate-and-test as the basic form of search by a symbol system)
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2, Backtrack programming (the move from testing complete candidates to testing partial ones)
---

Generate-and-test is a method that splits a search into two independent parts: a *generator* that produces candidate solutions one at a time, and a *tester* that accepts or rejects each candidate. With a generator that lists a complete [search space](/search-space/) without repeats, it is [brute-force search](/brute-force-search/), and it finds every solution. The two parts can be improved apart from each other, and the main way to make the method fast is to move tests from the tester into the generator, so that bad candidates are never produced. Taken to the end, this move turns generate-and-test into [backtracking](/generic-backtracking-algorithm/).

## In plain words

One person makes guesses and another person checks them. The guesser does not need to know the rules of the puzzle, and the checker does not need to know how the guesses are made. This split makes the program simple: you can write and test each half alone.

The checker is usually easy to write. The hard question is how good the guesser is. A careless guesser repeats guesses or misses some, and then the method is slow or wrong. A smart guesser uses some of the rules itself, so that it never makes a guess that it already knows is bad. The more rules the guesser uses, the fewer guesses the checker has to look at.

## When it applies

The method applies when the candidates can be listed by a generator and a single candidate can be checked. It fits best when the test is a black box, for example a simulation or an external program, or when the test only makes sense on a complete candidate. It finds all solutions, and stops at the first one if asked.

A good generator has three properties.

- **Complete.** It produces every candidate in the space, so no solution is missed.
- **Non-redundant.** It produces each candidate once, so no time is spent on repeats and no solution is reported twice.
- **Informed.** It does not produce candidates that some cheap rule already excludes.

Winston lists the same three properties for generators in Chapter 3 of his *Artificial Intelligence*. A generator that is complete and non-redundant gives a correct method; an informed generator gives a fast one. If the constraints can be checked on partial candidates, backtracking is better, because one failed check removes all the candidates that share a prefix.

## The template

```pseudo id=main
GENERATE-AND-TEST(I)                 ▷ outputs each candidate that passes the test
L1  g ← START(I)                         ▷ the state of the generator
L2  while g has a next candidate do
L3      x ← NEXT(g)
L4      if TEST(I, x) then
L5          OUTPUT(x)                    ▷ or return x to stop at the first solution
```

**Correctness.** If the generator lists a set $S$ that contains all solutions, each one exactly once, and TEST is true exactly on the solutions in $S$, then the output is the set of all solutions, each once. The proof is the invariant "after $j$ steps, the output is the set of solutions among the first $j$ candidates", which line L4 keeps.

**Cost.** The time is $\sum_{x \in S} (t_{\text{gen}}(x) + t_{\text{test}}(x))$, where $t_{\text{gen}}(x)$ is the time to produce $x$. If both are bounded by $t$, the time is $O(|S| \, t)$. The space is that of the generator state and one candidate.

**Moving tests into the generator.** Suppose that TEST is a conjunction $C_1 \wedge C_2$, and that one can generate the set $S' = \{x \in S : C_1(x)\}$ directly. Then GENERATE-AND-TEST over $S'$ with the test $C_2$ gives the same output in time $O(|S'| \, t)$. The step is safe when $C_1$ is a *necessary* condition for a solution. Repeated, this gives the hierarchy

$$\text{all candidates} \supseteq S' \supseteq S'' \supseteq \cdots \supseteq \text{solutions},$$

and the art is to find a large $C_1$ for which $S'$ still has a simple generator.

## Classic examples

**The cryptarithm SEND + MORE = MONEY.** Assign distinct digits to the eight letters S, E, N, D, M, O, R, Y so that the sum is correct and no number starts with 0. See the [cryptarithmetic puzzle](/cryptarithmetic-puzzle/) page. Four generators, from naive to informed:

| generator | candidates tested |
|---|---|
| any digit for each letter | $10^8 = 100{,}000{,}000$ |
| distinct digits for the letters | $10 \cdot 9 \cdots 3 = 1{,}814{,}400$ |
| distinct digits, with $S \ne 0$ and $M \ne 0$ | $1{,}451{,}520$ |
| distinct digits, $S \ne 0$, $M = 1$ | $161{,}280$ |

The last generator uses one fact: the sum of two numbers below 10,000 is below 20,000, so the leading digit $M$ of the five-digit sum is 1. Each generator gives the same unique solution $9567 + 1085 = 10652$. A column-by-column backtracking search, which checks each column of the sum as soon as its digits are set, tests far fewer partial assignments.

**The eight queens.** A generator of all sets of 8 squares produces $\binom{64}{8} = 4{,}426{,}165{,}368$ candidates. A generator of permutations, one queen per row and per column, produces $8! = 40{,}320$, and the tester only checks the diagonals. The [n-queens problem](/n-queens-problem/) page continues the example with backtracking.

**Random generators.** A generator may also draw candidates at random. Then the method is a Las Vegas search: each output is correct, but the time is random and a solution can be missed in a bounded run. For a space of $N$ candidates with $s$ solutions, independent uniform draws need $N/s$ draws on average to find one, since the number of draws is geometric with success probability $s/N$.

**The British Museum algorithm.** The name, used in early work on artificial intelligence, is a joke about the most naive generator of all: produce every possible text, as in the story of monkeys typing all the books in the British Museum, and test each one. It stands for generate-and-test with an uninformed generator.

## Variations

- **Hierarchical generate-and-test.** Generate a partial candidate, test what can be tested, and extend only the ones that pass. This is [backtracking](/generic-backtracking-algorithm/), with the test as a [pruning](/search-tree-pruning/) rule.
- **Plausible generators.** Order the candidates so that likely solutions come first. The worst case does not change, but the first solution comes sooner.
- **Generate, test and repair.** When a candidate fails, change it a little instead of making a new one. This leads to [local search](/local-search/).
- **Counting.** Replace OUTPUT by a counter to count the solutions. A [counting problem](/counting-problem/) often has faster methods than listing.

## Pitfalls

- **A generator that repeats.** Symmetric encodings, such as a tour and its reverse, make the generator produce the same solution several times. Then the output has repeats and the count of solutions is wrong.
- **A test in the generator that is too strong.** A condition moved into the generator must hold for every solution. If it is only a heuristic, solutions are lost and nothing signals it.
- **Expensive tests on cheap candidates.** If most candidates fail a cheap condition, test it first, or move it into the generator, before the expensive test.
- **Sharing the candidate.** If the generator changes one array in place, OUTPUT must copy it.

## Exercises

1. Show that the four counts in the table for SEND + MORE = MONEY are correct, and explain why the last generator still finds every solution.
2. In SEND + MORE = MONEY, the second column from the left gives $S + M + c = O + 10$, where $c$ is a carry. Use it with $M = 1$ to find the possible values of $S$ and $O$, and count the candidates that remain.
3. Write a generator of the permutations of $[n]$ in which no item is in its own place (derangements), so that a tester does not need to check that condition. Compare the number of candidates with $n!$.
4. Give an example of a test $C_1$ that is cheap to check but for which no simple generator of $\{x : C_1(x)\}$ is known.

## References
