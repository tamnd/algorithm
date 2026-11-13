---
tag: 02YCWR
kind: problem
slug: nim
name: Nim
aliases:
- Nim game
area: games-and-search/game-tree-search
level: intro
summary: "Two players take turns removing tokens from one heap; who takes the last token wins. The problem: given the heap sizes, decide who wins and find a winning move."
prereqs: [winning-losing-states, bitwise-operations]
see_also: [boutons-theorem, mex-function, grundy-number, sprague-grundy-theorem, combinatorial-game-theory, games-on-graphs, solved-game, generalized-geography]
sources:
  - paper: doi:10.2307/1967631
    title: Charles L. Bouton, Nim, a game with a complete mathematical theory, Annals of Mathematics, Second Series, 3(1/4) (1901 to 1902)
    locator: pp. 35 to 39 (the rules, the safe combinations as the positions whose binary digits sum to an even number in each column, and the variant where the player who takes the last token loses)
  - paper: "\"A generalization of the game called nim\""
    title: Eliakim Hastings Moore, A generalization of the game called nim, Annals of Mathematics, Second Series, 11(3) (1910), JSTOR 1967321
    locator: pp. 93 to 94 (the game where a move takes from at most k heaps, and its rule with digit sums modulo k + 1)
  - book: isbn:9780821851906
    title: Aaron N. Siegel, Combinatorial Game Theory, Graduate Studies in Mathematics 146, American Mathematical Society (2013)
    locator: Chapter IV, Impartial Games, from p. 179 (Nim, nim-sums and Nim variants), and Section V.1, Misère Nim, from p. 224
  - book: isbn:9781568812779
    title: Michael H. Albert, Richard J. Nowakowski and David Wolfe, Lessons in Play, A K Peters (2007)
    locator: Chapter 7, Impartial Games, from p. 135 (Nim and the nim-sum; general locator)
---

Nim is a game for two players on a row of heaps of tokens: a move takes one or more tokens from a single heap, the players alternate, and in the normal rule the player who takes the last token wins. As a problem, Nim asks: given the heap sizes, does the player to move have a strategy that wins against every defense, and if so, which move starts it? [Bouton's theorem](/boutons-theorem/) answers both questions with the bitwise XOR of the heap sizes, in time linear in the length of the input. Nim matters far beyond itself, because the [Sprague-Grundy theorem](/sprague-grundy-theorem/) shows that every finite impartial game behaves like a single Nim heap.

## In plain words

There are some piles of coins on a table. On your turn you pick one pile and take as many coins from it as you like, at least one. Then your opponent does the same. Whoever takes the last coin wins.

The game always ends, because coins only go away. So for any setup of piles, one of the two players can force a win. The question is which one, and how.

You could try every possible line of play, but the number of setups grows very fast with the pile sizes. A short rule exists instead. Write each pile size in binary, add up each column of digits without carrying, and look at the result. If every column is even, the player to move loses against good play. If not, there is a move that makes every column even, and that move wins.

## Definition

**Positions and moves.** A position is a finite tuple $(a_1, \dots, a_k)$ of nonnegative integers, the heap sizes. A move picks an index $i$ with $a_i > 0$ and a number $b$ with $0 \le b < a_i$, and replaces $a_i$ by $b$. The order of the heaps does not matter, and empty heaps can be dropped. Every move lowers $a_1 + \dots + a_k$ by at least 1, so every play ends after at most $a_1 + \dots + a_k$ moves.

**Winner.** Two players move in turn. Under the *normal play* convention, a player with no move (all heaps empty) loses, so the player who takes the last token wins. Under the *misère* convention, the player who takes the last token loses.

**The problem.** Given a position, decide whether it is an N-position (the player to move, the Next player, can force a win) or a P-position (the Previous player can), and in an N-position return a move to a P-position. By [Zermelo's theorem](/zermelo-theorem/) every position is one of the two, since Nim is finite, has [perfect information](/perfect-information-game/), and has no draws. These are the labels W and L of [winning and losing states](/winning-losing-states/).

**Input size.** The heap sizes are given in binary, so the input has $n = \sum_i \lceil \log_2(a_i + 1) \rceil$ bits, up to separators. The positions reachable from $(a_1, \dots, a_k)$ number $\prod_i (a_i + 1)$, which is exponential in $n$. A search over the [game graph](/games-on-graphs/) is therefore not a polynomial-time algorithm for Nim.

## Variants

- **Misère Nim.** The player who takes the last token loses. Bouton's paper treats this rule too. If some heap has 2 or more tokens, the outcome equals that of normal play. If every heap has at most 1 token, the player to move wins exactly when the number of nonempty heaps is even. The best move differs from normal play only near the end: when a normal-play winning move would leave only heaps of size 0 and 1, leave an odd number of 1-heaps instead.
- **Moore's Nim$_k$.** A move takes tokens from at least 1 and at most $k$ heaps, any amount from each. The player to move loses exactly when, in each binary digit position, the number of heaps with a 1 there is a multiple of $k + 1$. Nim is the case $k = 1$, where "a multiple of 2" means the XOR is 0.
- **Subtraction games.** One heap, and a move removes $m$ tokens for some $m$ in a fixed set $S$. With $S = \{1, 2, \dots, r\}$ the P-positions are the multiples of $r + 1$. With $S = \{1, 3, 4\}$ they are the heaps $n$ with $n \bmod 7 \in \{0, 2\}$. A sum of such heaps is solved by [Grundy numbers](/grundy-number/), not by the plain XOR of sizes.
- **Lasker's Nim.** A move either takes tokens from one heap or splits one heap into two nonempty heaps. The Grundy value of a heap of size $h \ge 1$ is $h$ when $h \bmod 4 \in \{1, 2\}$, $h + 1$ when $h \bmod 4 = 3$, and $h - 1$ when $h \bmod 4 = 0$; a position is a P-position when the XOR of these values is 0.
- **Wythoff's game.** Two heaps; a move takes any number from one heap, or the same number from both. The P-positions are the pairs $(\lfloor j\varphi \rfloor, \lfloor j\varphi^2 \rfloor)$ and their mirror images, for $j = 0, 1, 2, \dots$, with $\varphi = (1 + \sqrt 5)/2$: $(0, 0), (1, 2), (3, 5), (4, 7), (6, 10), (8, 13), \dots$ This game is not a sum of two one-heap games, and its rule is not an XOR rule.
- **Nim on a graph, and partisan versions.** Changing the move rule (tokens on vertices, edges, or moves only one player may make) gives the games of [generalized geography](/generalized-geography/) and of [combinatorial game theory](/combinatorial-game-theory/) in general. Some of these are PSPACE-complete, so Nim's closed rule is the exception.

## Examples

**One position, played out.** Take $(3, 4, 5)$. In binary, $011 \oplus 100 \oplus 101 = 010$, so the nim-sum is $2$ and the player to move, A, wins. A move must lower one heap $a$ to $a \oplus 2$. Only $3 \oplus 2 = 1 < 3$ works; $4 \oplus 2 = 6$ and $5 \oplus 2 = 7$ are larger than the heaps. So A's only winning move is $3 \to 1$. One possible play:

| move | by | position | nim-sum |
|---|---|---|---|
| start | | $(3, 4, 5)$ | 2 |
| heap 1: $3 \to 1$ | A | $(1, 4, 5)$ | 0 |
| heap 2: $4 \to 2$ | B | $(1, 2, 5)$ | 6 |
| heap 3: $5 \to 3$ | A | $(1, 2, 3)$ | 0 |
| heap 3: $3 \to 0$ | B | $(1, 2, 0)$ | 3 |
| heap 2: $2 \to 1$ | A | $(1, 1, 0)$ | 0 |
| heap 1: $1 \to 0$ | B | $(0, 1, 0)$ | 1 |
| heap 2: $1 \to 0$ | A | $(0, 0, 0)$ | 0 |

A moves to nim-sum 0 every time, B always leaves a nonzero nim-sum, and A takes the last token.

**More positions.**

- $(1, 2, 3)$: $01 \oplus 10 \oplus 11 = 0$, a P-position. Every move loses.
- $(3, 5, 7)$: the nim-sum is $1$, and all three heaps have bit 0 set, so there are three winning moves: $3 \to 2$, $5 \to 4$ and $7 \to 6$.
- $(7, 5, 3, 1)$: the nim-sum is $0$, a P-position.
- One heap $(a)$ with $a > 0$ is an N-position: take everything. Two heaps $(a, b)$ form a P-position exactly when $a = b$, and the winning strategy from $a \ne b$ is to equalize and then copy the opponent.

**All small positions.** Among the $8 + 8^2 + 8^3 + 8^4 = 4{,}680$ ordered tuples of 1 to 4 heaps with sizes 0 to 7, exactly $585$ have nim-sum 0. These are the P-positions, and a full search of the game graph labels the same 585.

**Misère.** In $(1, 1, 2)$ under normal play the winning move is $2 \to 0$, which leaves $(1, 1)$. Under misère play that move loses, since the opponent takes one token and leaves the last for you. The misère winning move is $2 \to 1$, which leaves three heaps of size 1.

## Known algorithms

- **The XOR rule** ([Bouton's theorem](/boutons-theorem/)). Compute $x = a_1 \oplus \dots \oplus a_k$. The position is a P-position exactly when $x = 0$. If $x \ne 0$, let $t$ be the highest set bit of $x$; every heap $a_i$ with bit $t$ set satisfies $a_i \oplus x < a_i$, and lowering it to $a_i \oplus x$ gives nim-sum 0. The number of winning moves is the number of heaps with bit $t$ set, which is odd. The cost is $O(n)$ bit operations for an input of $n$ bits, or $O(k)$ word operations when the sizes fit in a machine word.
- **Search of the game graph.** Label all $\prod_i (a_i + 1)$ positions by the backward rule of [winning and losing states](/winning-losing-states/), or by [retrograde analysis](/retrograde-analysis/). This is exponential in the input size, and it is the reference that the XOR rule is compared with on small inputs.
- **Grundy values.** Compute the [Grundy number](/grundy-number/) of each heap with the [mex function](/mex-function/); in Nim it is the heap size itself. This generalization is what solves the variants above.

## Bounds

- **Upper bound.** $O(n)$ bit operations for $n$ input bits, by the XOR rule, in the bit model; $O(k)$ in the word RAM with $k$ heaps.
- **Lower bound.** Every algorithm must read every bit of a P-position: if $x = 0$ and one bit of one heap flips, the nim-sum becomes nonzero and the answer changes. So $\Omega(n)$ bits must be read in the worst case, and the XOR rule is optimal up to a constant factor.
- **Game length.** A play lasts at most $a_1 + \dots + a_k$ moves, reached when each move takes one token. The winner of an N-position can win in a number of moves that depends on the opponent; the XOR rule does not minimize it.

## Reductions

- **Every impartial game to Nim.** By the [Sprague-Grundy theorem](/sprague-grundy-theorem/), a position of any finite impartial game under normal play is equivalent to the Nim heap of size $g(p)$, its Grundy number. A sum of impartial games is then equivalent to the Nim position $(g(p_1), \dots, g(p_k))$. This is a reduction in the sense of outcome, not of cost: computing $g(p)$ may be hard.
- **Nim as a game on a graph.** A Nim position is a vertex of a directed acyclic graph with $\prod_i (a_i + 1)$ vertices, an instance of [games on graphs](/games-on-graphs/). The reduction is exponential, because the graph is given by a rule and not written out.
- **Hard relatives.** Changing the rules slightly gives PSPACE-complete games. Node Kayles, where a move claims a vertex of a graph that is not next to a claimed vertex, and [generalized geography](/generalized-geography/) are both PSPACE-complete; the geography page gives the proofs and their sources.

## Applications

- **Analysis of impartial games.** Kayles, Dawson's Kayles, Grundy's game and Green Hackenbush are solved by computing Grundy values of their parts and taking the XOR, as if each part were a Nim heap.
- **Testing game solvers.** Nim has a closed answer for every position, so it serves as a test input for solvers such as [proof-number search](/proof-number-search/), [df-pn](/df-pn/) and retrograde analysis: the solver's answer must match the XOR rule.
- **Teaching.** Nim is the standard first example of a game where an exhaustive search is exponential but the answer has a short proof and a linear-time rule.

## References
