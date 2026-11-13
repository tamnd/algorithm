---
tag: JY9MWF
kind: concept
slug: combinatorial-game-theory
name: Combinatorial game theory
aliases:
- CGT
- partisan game theory
area: games-and-search/game-tree-search
level: advanced
summary: "The theory of two-player games with perfect information and no chance under normal play, where each game gets a value {L | R} and a sum of games is decided by adding values."
prereqs: [winning-losing-states, sprague-grundy-theorem, grundy-number]
see_also: [nim, boutons-theorem, mex-function, games-on-graphs, zermelo-theorem, perfect-information-game, zero-sum-game, minimax]
sources:
  - book: isbn:9781568811277
    title: John H. Conway, On Numbers and Games, 2nd edition, A K Peters (2001); 1st edition Academic Press (1976)
    locator: Part One (numbers as games, and the simplicity rule) and Part Two (games, sums, order, canonical forms, infinitesimals); general locator
  - book: isbn:9781568811307
    title: Elwyn R. Berlekamp, John H. Conway and Richard K. Guy, Winning Ways for Your Mathematical Plays, volume 1, 2nd edition, A K Peters (2001)
    locator: Chapter 2, Finding the Correct Number is Simplicity Itself; Chapter 5, Numbers, Nimbers and Numberless Wonders; Chapter 6, The Heat of Battle (general locators)
  - book: isbn:9780821851906
    title: Aaron N. Siegel, Combinatorial Game Theory, Graduate Studies in Mathematics 146, American Mathematical Society (2013)
    locator: Chapter I, Combinatorial Games, from p. 1; Chapter II, Short Games, from p. 53 (II.1 The Group G, p. 53; II.2 Canonical Form, p. 64; II.3 Numbers, p. 68; II.4 Infinitesimals, p. 82; II.5 Temperature, p. 101); Chapter V, Misère Play, from p. 223; Chapter VI, Loopy Games, from p. 279
  - book: isbn:9781568812779
    title: Michael H. Albert, Richard J. Nowakowski and David Wolfe, Lessons in Play, A K Peters (2007)
    locator: Chapter 2, Outcome Classes, from p. 35; Chapter 5, Values of Games, from p. 87; Chapter 8, Hot Games, from p. 159; Chapter 9, All-Small Games, from p. 185
  - book: isbn:9781568810324
    title: Elwyn Berlekamp and David Wolfe, Mathematical Go, Chilling Gets the Last Point, A K Peters (1994)
    locator: the whole book (Go endgames analyzed as sums of games, with chilling); general locator
---

Combinatorial game theory (CGT) studies two-player games of [perfect information](/perfect-information-game/) without chance, played under the normal rule that the player who cannot move loses, and it gives each such game a *value* in an ordered abelian group. The two players, Left and Right, may have different moves (partisan games), and the central operation is the disjunctive sum, where a game falls apart into independent components and each move is made in one of them. The value of a sum is the sum of the values, so the theory decides a sum without searching it. Numbers, the nimbers of the [Sprague-Grundy theorem](/sprague-grundy-theorem/), infinitesimals such as $\uparrow$ and hot games such as $\pm 1$ are all values of this kind.

## In plain words

Many board games break into separate regions near the end. In the board game Go, for example, the last fights happen in small corners that no longer touch. Each turn, a player picks one region and moves there.

Searching the whole board at once is slow, because the number of ways to combine moves in all regions is huge. Combinatorial game theory gives each region a value instead, the way a number describes an amount. Then you add the values. The total tells who wins with best play.

Some values are ordinary numbers: they say how many free moves one side has in hand. Others are not numbers at all. Some are smaller than every positive number but still more than nothing. Others are hot, which means both players want to move there first. The theory sorts these out and says which region to play in.

## The idea

### Games and outcomes

A *short game* is written $G = \{G^L \mid G^R\}$, where $G^L$ ranges over the *left options* (positions Left can move to) and $G^R$ over the *right options*. Each option is again a short game. Short means: finitely many positions and no infinite play. The base game is $0 = \{\,\mid\,\}$, with no options.

By backward induction ([Zermelo's theorem](/zermelo-theorem/)) every short game is in exactly one of four outcome classes:

| class | who wins with best play | order relation to 0 |
|---|---|---|
| $\mathcal{L}$ | Left, whoever moves first | $G > 0$ |
| $\mathcal{R}$ | Right, whoever moves first | $G < 0$ |
| $\mathcal{N}$ | the player who moves first (the Next player) | $G \parallel 0$ (fuzzy, incomparable) |
| $\mathcal{P}$ | the player who moves second (the Previous player) | $G = 0$ |

### Sums, negatives and order

- **Sum.** $G + H = \{G^L + H, G + H^L \mid G^R + H, G + H^R\}$: the mover picks one component and moves there.
- **Negative.** $-G = \{-G^R \mid -G^L\}$: the roles of Left and Right swap.
- **Order.** $G \ge H$ when Left wins $G - H$ whenever Right moves first, that is, $G - H \in \mathcal{L} \cup \mathcal{P}$. Then $G = H$ means $G - H \in \mathcal{P}$, and $G \parallel H$ means $G - H \in \mathcal{N}$.

Equal games are interchangeable in every sum: if $G = H$, then $G + X$ and $H + X$ have the same outcome for every $X$. With this equality, the values of short games form an abelian group $\mathbb{G}$ with a partial order compatible with addition. $G - G = 0$ for every $G$ (the mirror strategy), so the sum of a game and its negative is a second-player win.

### Canonical form

The same value has many game trees. Two simplifications keep the value: deleting *dominated* options (a left option $G^{L_1} \le G^{L_2}$ is never better for Left), and bypassing *reversible* options (a left option whose right reply $G^{L R} \le G$ can be replaced by the left options of that reply). Conway proved that applying both until neither applies gives a unique *canonical form* for each value, so equality of values becomes equality of reduced trees. Counting canonical forms by *birthday* (the depth of the tree): 1 game is born on day 0 ($0$), 4 by day 1 ($0$, $*$, $1$, $-1$) and 22 by day 2.

### Kinds of values

- **Numbers.** $1 = \{0 \mid\}$, $-1 = \{\mid 0\}$, $n + 1 = \{n \mid\}$, and $\tfrac{1}{2} = \{0 \mid 1\}$, with $\tfrac12 + \tfrac12 = 1$. The numbers among short games are the dyadic rationals $m/2^k$. A number $x$ means that Left is $x$ moves ahead. The *simplicity rule* evaluates many games: if some number $x$ lies strictly between every $G^L$ and every $G^R$ (in the sense $G^L \triangleleft x \triangleleft G^R$, where $\triangleleft$ means "less than or fuzzy"), then $G$ equals the simplest such number, the one born earliest. For example $\{-1 \mid 1\} = 0$ and $\{1 \mid 2\} = \tfrac32$. In a sum of a number and a game that is not a number, a player who has a winning move has one outside the number (the number avoidance theorem), so numbers are *cold*: nobody wants to move in them.
- **Nimbers.** $* = \{0 \mid 0\}$ and $*n = \{0, *, \dots, *(n-1) \mid 0, *, \dots, *(n-1)\}$, the values of impartial games. $*n + *m = *(n \oplus m)$, as in [Nim](/nim/). $*$ is fuzzy with 0: whoever moves first wins.
- **Infinitesimals.** $\uparrow = \{0 \mid *\}$ ("up") is positive, but smaller than every positive number: $0 < \uparrow < 2^{-k}$ for every $k$. $\uparrow + *$ is fuzzy with 0, while $\uparrow + \uparrow + *$ is positive. Such values decide close endgames where the numbers cancel.
- **Hot games.** $\pm 1 = \{1 \mid -1\}$ is a *switch*: the first player to move there gains one point. Hot games are fuzzy with a range of numbers. *Temperature* measures how much a move there is worth, and *thermographs* give a game's mean value and temperature; the rule "move in the hottest component" is a good, though not always optimal, strategy for sums of hot games. *Cooling* by $t$ subtracts a tax of $t$ from every move, and *chilling* is cooling by 1, the tool of Berlekamp and Wolfe for Go endgames.

### Relation to other parts of game theory

- **Impartial games** are the case where both players always have the same options; their values are nimbers, and the theory reduces to [Grundy numbers](/grundy-number/) and the [mex](/mex-function/) rule.
- **Minimax search** ([minimax](/minimax/)) treats a game as one tree. CGT applies when the tree is a sum of small trees, where it replaces a search of the product with addition of values.
- **Misère play** (the last player to move loses) breaks the group structure; misère theory works with quotients over restricted families of games (Siegel, Chapter V).
- **Loopy games**, where positions can repeat, get values such as $\mathrm{on} = \{\mathrm{on} \mid\}$ and need [games on graphs](/games-on-graphs/) for their outcomes (Siegel, Chapter VI).

## Examples

All values below were found by comparing sums against brute-force outcome classes, as in the Order rule: $G = H$ holds when the search finds $G - H$ to be a second-player win.

**Basic values.**

| game | value | outcome class | reason |
|---|---|---|---|
| $\{\,\mid\,\}$ | $0$ | $\mathcal{P}$ | no move for anyone |
| $\{0 \mid 0\}$ | $*$ | $\mathcal{N}$ | the first player moves to 0 and wins |
| $\{0 \mid\}$ | $1$ | $\mathcal{L}$ | only Left can move |
| $\{0 \mid 1\}$ | $\tfrac12$ | $\mathcal{L}$ | $\tfrac12 + \tfrac12 - 1$ is in $\mathcal{P}$ |
| $\{0 \mid *\}$ | $\uparrow$ | $\mathcal{L}$ | positive, and $\uparrow < \tfrac14$ |
| $\{1 \mid -1\}$ | $\pm 1$ | $\mathcal{N}$ | $\pm 1 + \pm 1$ is in $\mathcal{P}$ |
| $\{-1 \mid 1\}$ | $0$ | $\mathcal{P}$ | simplicity rule |
| $\{* \mid *\}$ | $0$ | $\mathcal{P}$ | every move gives $*$, which the opponent wins |
| $\{0, * \mid 0\}$ | $\uparrow *$ | $\mathcal{N}$ | equals $\uparrow + *$ |

**Sums.** $* + * = 0$ and $\uparrow + \downarrow = 0$ (second-player wins). $1 + *$ is in $\mathcal{L}$: the number dominates the nimber. $\pm 1 + 1 = \{2 \mid 0\}$ is in $\mathcal{N}$, but $\pm 1 + 2$ is in $\mathcal{L}$. $\uparrow$ and $*$ are fuzzy with each other.

**Domineering.** On a grid, Left places vertical dominoes and Right horizontal ones, and the player who cannot place loses. A vertical strip of 2 cells is $1$ (Left has one move, Right none), a vertical strip of 4 cells is $2$, a horizontal strip of 2 or 3 cells is $-1$, and the $2 \times 2$ square is $\{1 \mid -1\} = \pm 1$: whoever plays first leaves the other with no move and keeps one move. A $2 \times 2$ square beside a vertical strip of 4 cells is a sum, $\pm 1 + 2$, and Left wins it whoever starts; the search of the combined board gives the same class.

## Where it is used

- **Go endgames.** Berlekamp and Wolfe analyzed late Go endgames as sums of small regions, and with chilling found exact winning plays in positions that strong players misjudged.
- **Hackenbush, Domineering, Amazons, Konane, Toads and Frogs.** These games are the standard test cases of the theory; their regions are evaluated separately, then added.
- **Endgame play in programs.** A program can split a late position into independent regions, compute each value (often in canonical form), and decide the sum by arithmetic; the software CGSuite does this for many games.
- **Impartial games.** Every result on [Nim](/nim/), [Bouton's theorem](/boutons-theorem/) and the Sprague-Grundy theorem is the impartial corner of the theory.
- **Complexity.** Single games such as [generalized geography](/generalized-geography/) and [Hex](/hex-game/) are hard to solve; CGT does not make them easy, but it shows that their difficulty does not come from sums of easy parts.

## References
