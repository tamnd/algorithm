---
tag: 0H0WG2
kind: definition
slug: mex-function
name: Mex function
aliases:
- minimum excludant
- mex
area: games-and-search/game-tree-search
level: intro
summary: The mex of a set of nonnegative integers is the smallest nonnegative integer that is not in the set. It is the rule that gives Grundy values of game positions.
see_also: [grundy-number, sprague-grundy-theorem, nim, boutons-theorem, greedy-coloring, winning-losing-states]
sources:
  - book: isbn:9781568811307
    title: Elwyn R. Berlekamp, John H. Conway and Richard K. Guy, Winning Ways for Your Mathematical Plays, volume 1, 2nd edition, A K Peters (2001)
    locator: Chapter 3, Some Harder Games and How to Make Them Easier (the mex rule for nim-values; general locator)
  - book: isbn:9780821851906
    title: Aaron N. Siegel, Combinatorial Game Theory, Graduate Studies in Mathematics 146, American Mathematical Society (2013)
    locator: Chapter IV, Impartial Games, from p. 179 (the mex rule and nim values), and Chapter VIII, Transfinite Games, from p. 397 (the mex of a set of ordinals)
  - book: isbn:9781568812779
    title: Michael H. Albert, Richard J. Nowakowski and David Wolfe, Lessons in Play, A K Peters (2007)
    locator: Chapter 7, Impartial Games, from p. 135 (the minimum excluded value and the Grundy value of a position)
---

The mex (minimum excludant) of a set of nonnegative integers is the smallest nonnegative integer that is not in the set: $\operatorname{mex}\{0, 1, 3\} = 2$ and $\operatorname{mex}\{1, 2\} = 0$. It is the one operation in the theory of impartial games: the [Grundy number](/grundy-number/) of a position is the mex of the Grundy numbers of the positions that one move reaches, and the [Sprague-Grundy theorem](/sprague-grundy-theorem/) turns this into a solution of sums of games. The mex of a finite set of size $k$ is at most $k$, and so a table of $k + 1$ flags computes it in $O(k)$ time.

## Definition

Let $\mathbb{N} = \{0, 1, 2, \dots\}$. For a set $S \subseteq \mathbb{N}$ with $S \neq \mathbb{N}$,
$$ \operatorname{mex}(S) = \min(\mathbb{N} \setminus S). $$
The minimum exists because $\mathbb{N} \setminus S$ is a nonempty set of nonnegative integers. An equivalent form: $m = \operatorname{mex}(S)$ exactly when
$$ m \notin S \quad\text{and}\quad \{0, 1, \dots, m - 1\} \subseteq S. $$
The first condition says that $m$ is missing, the second that no smaller number is missing. For a list with repeats, the mex is the mex of the set of its entries.

**Bound.** If $S$ is finite, then $\operatorname{mex}(S) \le |S|$, with equality exactly when $S = \{0, 1, \dots, |S| - 1\}$. Proof: the $|S| + 1$ numbers $0, 1, \dots, |S|$ cannot all be in a set of $|S|$ elements, so one of them is missing, and the mex is at most that number. If the mex is $|S|$, then $\{0, \dots, |S| - 1\} \subseteq S$, and these $|S|$ numbers fill $S$. The converse is the equivalent form with $m = |S|$.

**Monotone.** If $S \subseteq T$, then $\operatorname{mex}(S) \le \operatorname{mex}(T)$. Proof: $\operatorname{mex}(T) \notin T$, so $\operatorname{mex}(T) \notin S$, and the least number missing from $S$ is at most $\operatorname{mex}(T)$. Adding a value larger than the mex leaves the mex unchanged, and adding the value equal to the mex raises it.

**Computation.** Given $k$ numbers (repeats allowed), make an array of $k + 1$ flags, set the flag of each number $v \le k$, and return the first index whose flag is clear. A number $v > k$ cannot be the mex or block it, because the mex is at most the number of distinct values, which is at most $k$. The time is $O(k)$ and the extra space is $O(k)$, with no sort and no hash table. Sorting first costs $O(k \log k)$ in the comparison model and gives nothing more. When the set changes by inserts and deletes over values in $\{0, \dots, U\}$, a count per value and a segment tree over $0$ to $U$ that stores whether each range has a zero count answer each query in $O(\log U)$ time.

**Use in games.** In a finite [impartial game](/combinatorial-game-theory/), where both players have the same moves, the Grundy number of a position $p$ is
$$ g(p) = \operatorname{mex}\{\, g(q) : q \text{ is an option of } p \,\}, $$
the mex of the values one move away. A position with no move gets $\operatorname{mex}(\emptyset) = 0$. The two halves of the equivalent form are the two facts that the theory needs: no option has the value $g(p)$, and every smaller value is the value of some option.

**Ordinals.** The same definition works for a set $S$ of ordinals: $\operatorname{mex}(S)$ is the least ordinal not in $S$. It always exists, because $S$ is a set and the ordinals are not. This form gives Grundy values of games where a position can have infinitely many options.

## Examples and non-examples

**Small sets.**

| $S$ | $\operatorname{mex}(S)$ | reason |
|---|---|---|
| $\emptyset$ | 0 | 0 is missing |
| $\{1, 2\}$ | 0 | 0 is missing |
| $\{0, 2\}$ | 1 | 0 is present, 1 is missing |
| $\{0, 1, 3\}$ | 2 | 0 and 1 present, 2 missing |
| $\{0, 1, 2\}$ | 3 | equality case of the bound, $\lvert S \rvert = 3$ |
| $\{0, 1, 2, 5, 100\}$ | 3 | large entries do not matter |
| list $0, 0, 0, 1$ | 2 | repeats count once |
| $\{1, 3, 5, 7, \dots\}$ (odd numbers) | 0 | an infinite set can have a mex |

**A game.** In the subtraction game where a move takes 1, 3 or 4 tokens from a heap, the values start $g(0), \dots, g(6) = 0, 1, 0, 1, 2, 3, 2$. Then $g(7)$ is the mex of $g(6), g(4), g(3) = 2, 2, 1$, so it is the mex of $\{1, 2\}$, which is 0. A heap of 7 is a loss for the player to move. From there the values repeat with period 7.

**Graph coloring.** [Greedy coloring](/greedy-coloring/) visits vertices in a fixed order and gives each vertex the mex of the colors of its colored neighbors, with colors $0, 1, 2, \dots$. A vertex of degree $d$ then gets a color at most $d$, by the bound.

**Non-examples.**

- $\operatorname{mex}(\mathbb{N})$ is not defined: no nonnegative integer is missing. Over ordinals, it is $\omega$.
- The mex is not "the maximum plus one". For $S = \{0, 2\}$ the maximum plus one is 3, and the mex is 1. The two agree only when $S$ is $\{0, \dots, k - 1\}$.
- The mex is not defined on sets with negative numbers or on arbitrary sets of integers. The smallest integer missing from a subset of $\mathbb{Z}$ need not exist.
- The mex of a union is not a function of the mexes of the parts: $\operatorname{mex}\{0\} = 1$ and $\operatorname{mex}\{1\} = 0$, but $\operatorname{mex}\{0, 1\} = 2$. Only the weaker rule of the Definition holds: a larger set has a mex at least as large.

## Related definitions

- [Grundy number](/grundy-number/): the value $g(p)$ defined by the mex rule above, and the reason the mex exists as a named operation.
- [Sprague-Grundy theorem](/sprague-grundy-theorem/): every finite impartial game is equivalent to a [Nim](/nim/) heap of size equal to its Grundy number.
- [Bouton's theorem](/boutons-theorem/): in Nim the Grundy number of a heap of size $n$ is $n$, since its options have values $0, \dots, n - 1$, and a sum of heaps has the XOR of the sizes.
- Nim-sum: the bitwise XOR ([bitwise operations](/bitwise-operations/)), the operation that combines Grundy numbers of the parts of a sum.
- Grundy number of a graph: the largest number of colors that greedy coloring with the mex rule can use over all vertex orders. It shares the name, and it is a different invariant from the Grundy number of a game position.
- [Winning and losing states](/winning-losing-states/): the coarser labeling that keeps only whether a value is 0 (a loss for the player to move) or not.

## References
