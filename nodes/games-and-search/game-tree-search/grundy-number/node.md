---
tag: VC5H7C
kind: concept
slug: grundy-number
name: Grundy number
aliases:
- Grundy value
- nim-value
- mex value
- Sprague-Grundy value
area: games-and-search/game-tree-search
level: advanced
summary: The Grundy number of a position in a finite impartial game is the mex of the Grundy numbers of its options. It is 0 exactly at losses, and it adds by XOR over sums of games.
prereqs: [mex-function, nim, winning-losing-states]
see_also: [sprague-grundy-theorem, boutons-theorem, combinatorial-game-theory, games-on-graphs, generalized-geography, memoization, topological-sort]
sources:
  - paper: "\"Über mathematische Kampfspiele\""
    title: Roland P. Sprague, Über mathematische Kampfspiele, Tohoku Mathematical Journal, First Series, 41 (1935 to 1936)
    locator: pp. 438 to 444 (every finite impartial game is equivalent to a Nim heap, whose size is the value of the position)
  - paper: "\"Mathematics and games\""
    title: Patrick M. Grundy, Mathematics and games, Eureka 2 (1939), reprinted in Eureka 27 (1964)
    locator: pp. 6 to 8 of the 1939 issue (the function now called the Grundy function, defined by the mex rule, and its XOR rule for sums)
  - paper: doi:10.1017/S0305004100031509
    title: Richard K. Guy and Cedric A. B. Smith, The G-values of various games, Proceedings of the Cambridge Philosophical Society 52(3) (1956)
    locator: pp. 514 to 526 (octal games, their code, the periodicity theorem, and the values of Kayles and other games)
  - book: isbn:9780821851906
    title: Aaron N. Siegel, Combinatorial Game Theory, Graduate Studies in Mathematics 146, American Mathematical Society (2013)
    locator: Chapter IV, Impartial Games, from p. 179 (nim values, subtraction and octal games, the periodicity theorem), Chapter V, Misère Play, from p. 223, and Chapter VI, Loopy Games, from p. 279
  - book: isbn:9781568811307
    title: Elwyn R. Berlekamp, John H. Conway and Richard K. Guy, Winning Ways for Your Mathematical Plays, volume 1, 2nd edition, A K Peters (2001)
    locator: Chapter 4, Taking and Breaking (octal games, Kayles, Dawson's Kayles and Grundy's game; general locator)
---

The Grundy number (or nim-value) of a position $p$ in a finite impartial game is the number $g(p)$ defined by the [mex](/mex-function/) rule: a position with no move has value 0, and otherwise $g(p)$ is the smallest nonnegative integer that is not the value of any position one move away. It refines the win/loss labeling of [winning and losing states](/winning-losing-states/): $g(p) = 0$ exactly when the player to move loses. By the [Sprague-Grundy theorem](/sprague-grundy-theorem/), the position behaves like a [Nim](/nim/) heap of size $g(p)$, and the value of a sum of games is the XOR of the values of its parts. This is what makes games that split into independent parts solvable part by part.

## In plain words

In some games both players have exactly the same moves; only whose turn it is differs. For such a game, the Grundy number gives each position a score that is a whole number.

You compute it from the end of the game backward. A position with no move scores zero. For any other position, look at the scores of the positions you can move to, and take the smallest whole number that is missing from that list.

Zero means the player to move loses with good play. Any other score means that player wins. The score carries more than win or lose: when a game falls apart into separate smaller games, played side by side, you combine their scores with the binary operation exclusive or. The combined score tells you who wins the whole thing, without searching the combined game.

## The idea

### Definition

An *impartial game* here is a finite directed acyclic graph of positions, where an edge $p \to q$ means a move from $p$ to $q$ (an *option* of $p$), the same for both players. Finite and acyclic means every play ends. Under normal play, the player with no move loses. The Grundy number is defined by recursion on the length of the longest play from $p$:
$$ g(p) = \operatorname{mex}\{\, g(q) : q \text{ an option of } p \,\}. $$
The recursion is well founded because every option has a shorter longest play.

### What the number says

**Zero exactly at losses.** For every position $p$, the player to move loses if and only if $g(p) = 0$. Proof by induction on the longest play from $p$. A position with no move has $g = 0$ and is a loss. If $g(p) = 0$, then 0 is missing from the values of the options, so every option has a nonzero value and is a win for the player to move there, by induction; so every move from $p$ loses. If $g(p) = k > 0$, then by the definition of mex the value 0 belongs to some option, which is a loss for the opponent by induction; moving there wins.

**A value $k$ acts like a Nim heap of size $k$.** From a position of value $k$ there is a move to a position of each value $0, 1, \dots, k - 1$, as from a heap of $k$, and there is no move to a position of value $k$. There may be moves to larger values, which a heap does not have; the [Sprague-Grundy theorem](/sprague-grundy-theorem/) shows that they never help, because the opponent can move back down to value $k$.

**Sums.** In the sum $G_1 + \dots + G_m$, a move is a move in one component of the mover's choice, and the player with no move in any component loses. The Sprague-Grundy theorem gives
$$ g(p_1, \dots, p_m) = g(p_1) \oplus \dots \oplus g(p_m), $$
with $\oplus$ the bitwise XOR. A winning move in a sum with total $x \ne 0$ changes one component of value $v$ with $v \oplus x < v$ to an option of value $v \oplus x$, which exists by the mex rule.

### Computing it

With the game graph written out, compute the values in reverse [topological order](/topological-sort/), or by recursion with [memoization](/memoization/). The mex of $d$ values takes $O(d)$ time, so the total is $O(|V| + |E|)$. Two bounds follow from the mex: $g(p)$ is at most the number of options of $p$, and $g(p)$ is at most the length of the longest play from $p$, because $\operatorname{mex}(S) \le \max(S) + 1$ for a nonempty set $S$.

The point of the value is that one never builds the graph of a sum. A sum of $m$ components with $N$ positions each has $N^m$ positions, but its value needs only the $m$ component values.

### Periodicity

**Subtraction games.** In the game $S(s_1, \dots, s_r)$ a move takes $s_i$ tokens from a heap. The value $g(n)$ depends only on $g(n - s_1), \dots, g(n - s_r)$, so only on the last $s = \max_i s_i$ values, and every value is at most $r$. There are at most $(r + 1)^s$ windows of $s$ consecutive values, so two windows repeat by the pigeonhole principle, and from the first repeat on the sequence is periodic. So every finite subtraction game has an eventually periodic Grundy sequence, and the period is found by computing values until a window repeats.

**Octal games.** An octal game has a code $0.d_1 d_2 d_3 \dots$ with octal digits $d_k$. A move removes $k$ tokens from one heap, and the digit says what may remain of that heap: bit 1 of $d_k$ allows nothing (the heap had exactly $k$ tokens), bit 2 allows one nonempty heap, bit 4 allows two nonempty heaps. Nim is $0.333\dots$, the subtraction game $S(1, 2)$ is $0.33$, and Kayles, where a move knocks down one pin or two adjacent pins from a row and may split the row, is $0.77$. Guy and Smith proved the periodicity theorem: if the code has finitely many nonzero digits and the last is $d_t$, and if $g(n + p) = g(n)$ for all $n$ with $n_0 \le n < 2 n_0 + p + t$, then $g(n + p) = g(n)$ for all $n \ge n_0$. So a finite computation can prove that a sequence is periodic forever.

### Where the theory stops

- **Misère play.** Under the rule that the last player to move loses, Grundy numbers of the parts do not determine the outcome of a sum. [Bouton's theorem](/boutons-theorem/) has the misère rule for Nim, and the general misère theory (genus, misère quotients) is much harder; see Siegel, Chapter V.
- **Loopy games.** If positions can repeat, plays can be infinite and draws appear ([games on graphs](/games-on-graphs/)). A generalized Grundy function, with an extra value for positions from which play can go on forever, takes over; see Siegel, Chapter VI.
- **Partisan games.** When the players have different moves, a single number per position is not enough, and the values of [combinatorial game theory](/combinatorial-game-theory/) replace nimbers.
- **Hardness.** The recursion is linear in the size of the game graph, but that graph can be exponential in the size of the position. Deciding whether $g(p) = 0$ is PSPACE-complete for Node Kayles and for [generalized geography](/generalized-geography/), so no general shortcut exists.
- **A name clash.** In graph theory, the Grundy number of a graph is the largest number of colors that [greedy coloring](/greedy-coloring/) can use. It applies the mex rule to colors of neighbors, and it is a different invariant.

## Examples

**Subtraction games.** Computed by the mex rule up to $n = 200$:

| moves | $g(0), g(1), \dots$ | pattern | losses ($g = 0$) |
|---|---|---|---|
| $\{1, 2\}$ | 0, 1, 2, 0, 1, 2, 0, ... | $n \bmod 3$ | multiples of 3 |
| $\{1, 2, 3\}$ | 0, 1, 2, 3, 0, 1, 2, 3, ... | $n \bmod 4$ | multiples of 4 |
| $\{1, 3, 4\}$ | 0, 1, 0, 1, 2, 3, 2, 0, 1, ... | period 7 from $n = 0$ | $n \bmod 7 \in \{0, 2\}$ |
| $\{2, 3\}$ | 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, ... | period 5 from $n = 0$ | $n \bmod 5 \in \{0, 1\}$ |
| any heap size (Nim) | 0, 1, 2, 3, ... | $g(n) = n$ | only $n = 0$ |

For $\{1, 3, 4\}$, the value $g(5) = 3$ is the mex of $g(4), g(2), g(1) = 2, 0, 1$. The value 3 is larger than any move would suggest in plain win/loss terms: a heap of 5 is just a win, but in a sum it counts as a Nim heap of 3.

**A sum.** Play three games at once: a heap of 5 in $S(1, 2)$ (value 2), a heap of 6 in $S(1, 3, 4)$ (value 2), and a Nim heap of 3 (value 3). The total is $2 \oplus 2 \oplus 3 = 3 \ne 0$, so the player to move wins. Each component of value $v$ needs an option of value $v \oplus 3$, and there are three winning moves:

- Nim heap $3 \to 0$, value $3 \to 0$; total $2 \oplus 2 \oplus 0 = 0$.
- $S(1, 2)$ heap $5 \to 4$, value $2 \to 1$; total $1 \oplus 2 \oplus 3 = 0$.
- $S(1, 3, 4)$ heap $6 \to 3$, value $2 \to 1$; total $2 \oplus 1 \oplus 3 = 0$.

**Kayles.** The values for rows of $0$ to $12$ pins are $0, 1, 2, 3, 1, 4, 3, 2, 1, 4, 2, 6, 4$. A row of $n$ pins with one pin taken from the middle splits into two rows with value $g(a) \oplus g(b)$, which is why the mex runs over XORs. The last $n$ with $g(n) \ne g(n + 12)$ is $n = 70$ ($g(70) = 6$, $g(82) = 2$), and the values for $n = 71$ to $82$ are $7, 4, 1, 2, 8, 1, 4, 7, 2, 1, 8, 2$. With $n_0 = 71$, $p = 12$ and $t = 2$ the Guy-Smith test needs agreement for $71 \le n < 156$, which holds; so Kayles has period 12 from $n = 71$ on. The same test fails for $n_0 = 70$.

**Dawson's Kayles** ($0.07$: a move removes two adjacent pins) has period 34; in the indexing by number of pins used here, its last exception is at $n = 52$, and the Guy-Smith test with $n_0 = 53$ holds.

**Grundy's game**, where a move splits one heap into two heaps of different sizes, has values $0, 0, 0, 1, 0, 2, 1, 0, 2, 1, 0, 2, 1, 3, 2$ for heaps of $0$ to $14$. It is not an octal game, and no period is known for it.

## Where it is used

- **Solving sums.** Any impartial game that splits into independent parts (rows of pins, separate regions of a board, separate heaps) is solved by computing the value of each part once and taking the XOR. This is how octal games, Kayles-like games and many puzzles with a "split" move are analyzed.
- **Tables and periods.** For a one-parameter family such as heaps or rows, the values are tabulated, and a proved period turns the table into a closed rule, as for Kayles.
- **Competitive programming.** Problems that ask for the winner of several simultaneous games reduce to Grundy numbers and XOR, with the values computed by memoized recursion.
- **Partisan theory.** In [combinatorial game theory](/combinatorial-game-theory/), the impartial values are the nimbers $*k$, a subgroup of all game values, and the Grundy number $k$ is the index of that nimber.

## References
