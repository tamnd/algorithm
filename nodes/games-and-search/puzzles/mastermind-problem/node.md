---
tag: EHS84T
kind: problem
slug: mastermind-problem
name: Mastermind problem
aliases:
- Mastermind game
- Bulls and cows
area: games-and-search/puzzles
level: intro
summary: Find a hidden code of n pegs in k colors from scored guesses. For 4 pegs and 6 colors, 5 guesses are necessary and enough (Knuth 1976); deciding if any code fits given scores is NP-complete.
prereqs: [information-theoretic-bound]
see_also: [twenty-questions-problem, counterfeit-coin-problem, minimax, adversary-argument, decision-tree-model, constraint-satisfaction-problem, np-complete, brute-force-search]
sources:
  - paper: "Donald E. Knuth, The computer as master mind, Journal of Recreational Mathematics 9(1), 1976, 1 to 6"
    locator: the whole paper (the strategy that minimizes the largest answer class, its table of guesses, and the worst case of 5 guesses)
  - paper: "Kenji Koyama and Tony W. Lai, An optimal Mastermind strategy, Journal of Recreational Mathematics 25(4), 1993, 251 to 256"
    locator: the whole paper (the least expected number of guesses, 5625/1296, by exhaustive search)
  - paper: "Vašek Chvátal, Mastermind, Combinatorica 3(3-4), 1983, 325 to 329"
    locator: the whole paper (bounds for n pegs and k colors, and strategies with all guesses fixed in advance)
  - paper: doi:10.1145/2987372
    title: Benjamin Doerr, Carola Doerr, Reto Spöhel and Henning Thomas, Playing Mastermind with many colors, Journal of the ACM 63(5), 2016
    locator: the whole paper (O(n log log n) guesses for n pegs and n colors)
  - paper: "Jeff Stuckman and Guo-Qiang Zhang, Mastermind is NP-complete, INFOCOMP Journal of Computer Science 5(2), 2006, 25 to 28"
    locator: the whole paper (the NP-completeness of deciding whether some code fits a list of guesses and scores)
  - paper: "Michael T. Goodrich, On the algorithmic complexity of the Mastermind game with black-peg results, Information Processing Letters 109, 2009"
    locator: the whole paper (the version that reports black pegs only)
  - paper: "Giovanni Viglietta, Hardness of Mastermind, Fun with Algorithms (FUN 2012), Lecture Notes in Computer Science 7288, Springer, 2012"
    locator: the whole paper (counting the codes that fit the scores is #P-complete; hardness with few colors)
---

The Mastermind problem asks for a strategy that finds a hidden code, a word of $n$ pegs over $k$ colors, from guesses. Each guess gets a score of black and white pegs: black for a right color in the right place, white for a right color in the wrong place. For the board game, $n = 4$ and $k = 6$, so there are $6^4 = 1296$ codes. Knuth (1976) gave a strategy that always wins within 5 guesses, and 4 are not enough. The least expected number of guesses is $5625/1296 \approx 4.340$ (Koyama and Lai 1993). For general $n$ and $k$ the problem is a game of search with a rich answer, like the [twenty questions problem](/twenty-questions-problem/). Deciding whether any code fits a list of guesses and scores is [NP-complete](/np-complete/) (Stuckman and Zhang 2006).

## In plain words

One player hides a row of four colored pegs. The other player guesses rows, and after each guess is told how many pegs have the right color in the right place, and how many more have a right color that is in the wrong place. The goal is to find the hidden row with as few guesses as possible.

Each answer rules out all the rows that would have given a different answer. A good guess splits the rows that are still possible into many small groups, one for each answer, so that whatever the answer, few rows are left.

With six colors, a careful plan always finds the row in at most five guesses, and no plan can promise four.

## Definition

A *code* is a word $x = x_1 \cdots x_n$ over the colors $\{1, \ldots, k\}$. The *score* of a guess $g$ against the secret $s$ is the pair $(b, w)$ with

$$b = |\{i : g_i = s_i\}|, \qquad b + w = \sum_{c=1}^{k} \min(\#_c(g), \#_c(s)),$$

where $\#_c(x)$ is the number of places of $x$ with color $c$. The sum is the largest number of disjoint pairs of a place in $g$ and a place in $s$ with the same color, so $b + w$ counts all the matches and $w$ the ones in the wrong place.

A *strategy* is a decision tree: each node holds a guess, and has one child for each score. It *solves* the game when for every secret, the path of scores ends at a guess equal to the secret, with score $(n, 0)$. The cost counts the guesses, the last one included.

- **Worst case.** Minimize the largest number of guesses over all secrets.
- **Average case.** Minimize the average over all $k^n$ secrets.
- **Consistency.** Given guesses and their scores, is there a code that fits all of them? This is the *Mastermind satisfiability problem*.

For $n = 4$ there are 14 scores: all pairs with $b + w \le 4$, except $(3, 1)$, which cannot happen, since three right places and a fourth matching color would force the fourth place right too.

## Variants

- **Bulls and cows.** The older pencil game uses 4 different digits from 10, so $5040$ codes. The score is the same pair, bulls for black and cows for white. Only the set of codes changes.
- **Black pegs only.** The score is $b$ alone (Goodrich 2009). With two colors this is the problem of finding a 0-1 vector from the sizes of its intersections with chosen sets. This is coin weighing with a spring scale, which needs $\Theta(n / \log n)$ queries; Chvátal (1983) discusses this link.
- **Static Mastermind.** All guesses are fixed in advance, as in a non-adaptive strategy for the [counterfeit coin problem](/counterfeit-coin-problem/). Chvátal (1983) showed that for $k \le n^{1-\varepsilon}$, random guesses fixed in advance reach the information bound up to a constant factor.
- **Many colors.** For $k = n$, Doerr, Doerr, Spöhel and Thomas (2016) gave $O(n \log \log n)$ guesses, against a lower bound of order $n$.
- **Counting.** Count the codes that fit given scores. Viglietta (2012) showed this is #P-complete.

## Examples

**A score.** Write the colors as 1 to 6. Let the secret be 1123 and the guess 1312. Only the first place matches, so $b = 1$. Both codes have two 1s, one 2 and one 3, so the colors match in $2 + 1 + 1 = 4$ pairs and $w = 4 - 1 = 3$. The score is $(1, 3)$.

**The first guess.** Up to swapping colors and places, there are five kinds of first guess. The largest class of secrets that share one score is:

| first guess | 1111 | 1112 | 1122 | 1123 | 1234 |
|---|---|---|---|---|---|
| largest class | 625 | 317 | 256 | 276 | 312 |

For 1111, the score $(0, 0)$ leaves the $5^4 = 625$ codes with no 1. Knuth chose 1122, which has the smallest largest class.

**Four guesses are not enough.** Let $f(t)$ be the most codes that $t$ guesses can always tell apart. With one guess, only $f(1) = 1$. With $t$ guesses, the first one can be right for one code, and each of the other 13 scores must leave a set that $t - 1$ guesses can solve, so $f(t) \le 1 + 13 f(t - 1)$. This gives $f(2) \le 14$ and $f(3) \le 183$. Every first guess leaves a class of at least 256 secrets with a score other than $(4, 0)$, and $256 > 183$, so no strategy wins within 4 guesses for every secret. $\square$

**Knuth's strategy.** Guess 1122 first. After each answer, keep the set $S$ of codes that fit every score so far, and guess the code (from all 1296, not only from $S$) whose largest score class within $S$ is smallest. Break ties first in favor of a code in $S$, then by the least code in numeric order. On the 1296 secrets this strategy uses:

| guesses | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| secrets | 1 | 6 | 62 | 533 | 694 |

So it always wins within 5 guesses, with $5801$ guesses in total, an average of $5801 / 1296 \approx 4.476$. With the lower bound above, 5 is the exact worst case.

## Known algorithms

- **Minimax on partitions.** Knuth's strategy above: at each step a one-level [minimax](/minimax/) over all guesses and all scores. Each step tries all $k^n$ guesses against all live codes, so it costs $O(k^{2n} n)$ time per step, which is practical only for small boards.
- **Other one-step rules.** Choose the guess with the most score classes, or with the largest entropy of the class sizes, or with the least expected class size. Some of these give smaller averages than Knuth's rule.
- **Exhaustive search.** Koyama and Lai (1993) searched all strategies, with symmetry reductions, and found the least expected number of guesses, $5625/1296$. Their best strategy needs 6 guesses for some secrets, so the best average and the best worst case come from different strategies.
- **Consistent guessing.** Always guess some code that fits all scores so far. Finding one is a [constraint satisfaction problem](/constraint-satisfaction-problem/), solved for small boards by [brute force](/brute-force-search/) or backtracking. Strategies of this kind are simple, but their worst case can be worse.
- **Many pegs.** Chvátal's random static guesses, and the adaptive strategy of Doerr, Doerr, Spöhel and Thomas for $k = n$.

## Bounds

- **Information.** A score takes at most $\binom{n+2}{2}$ values, so a strategy needs at least $\log_{\binom{n+2}{2}} k^n = \Omega(n \log k / \log n)$ guesses. The count $f(t)$ above sharpens this for small boards.
- **4 pegs, 6 colors.** Worst case exactly 5 (Knuth 1976, with the argument above). Least average $5625/1296$ (Koyama and Lai 1993).
- **Static, few colors.** $O(n \log k / \log n)$ guesses fixed in advance for $k \le n^{1-\varepsilon}$ (Chvátal 1983), which matches the information bound up to a constant.
- **$k = n$.** $O(n \log \log n)$ adaptive guesses (Doerr, Doerr, Spöhel and Thomas 2016), and at least $\Omega(n)$ by the information bound.
- **Complexity.** Deciding whether a code fits given guesses and scores is NP-complete (Stuckman and Zhang 2006), also with black pegs only (Goodrich 2009). Counting such codes is #P-complete (Viglietta 2012).

## Reductions

- **From satisfiability.** Stuckman and Zhang reduce a satisfiability problem to Mastermind satisfiability: guesses and scores encode the clauses, and a code fits all scores exactly when it encodes a satisfying assignment.
- **To a decision tree.** A strategy is a decision tree with branching $\binom{n+2}{2} - 1$, so the lower bounds are leaf counts, as in the [decision tree model](/decision-tree-model/). The bound for 4 guesses above is such a count, made sharper by the first guess. The adversary that always gives the score with the largest class is an [adversary argument](/adversary-argument/).
- **To coin weighing.** Two colors and black pegs only is the spring-scale coin weighing problem, with a set of places as each query.

## Applications

- **Teaching search and lower bounds.** Mastermind is a standard small example of minimax search over partitions, and of a lower bound from counting the leaves of a decision tree.
- **Query learning.** Finding a hidden string from similarity scores models attacks that learn a secret from the number of matches it gives, and the learning of a hidden vector from inner-product queries.
- **Benchmarks.** The 1296 codes and the 5040 codes of bulls and cows are small enough for exhaustive search, so they serve as test cases for heuristic search and for genetic and other general-purpose methods.

## References
