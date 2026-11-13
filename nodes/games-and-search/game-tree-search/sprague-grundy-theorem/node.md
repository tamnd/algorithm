---
tag: AMWPCY
kind: theorem
slug: sprague-grundy-theorem
name: Sprague-Grundy theorem
aliases:
- Sprague-Grundy theorem for impartial games
area: games-and-search/game-tree-search
level: advanced
summary: Under normal play, every finite impartial game is equivalent to the Nim heap whose size is its Grundy number, and the Grundy number of a sum is the XOR of the parts.
prereqs: [grundy-number, mex-function, nim, boutons-theorem]
see_also: [combinatorial-game-theory, games-on-graphs, generalized-geography, winning-losing-states, zermelo-theorem]
sources:
  - paper: "\"Über mathematische Kampfspiele\""
    title: Roland P. Sprague, Über mathematische Kampfspiele, Tohoku Mathematical Journal, First Series, 41 (1935 to 1936)
    locator: pp. 438 to 444 (every finite impartial game under normal play is equivalent to a Nim heap)
  - paper: "\"Mathematics and games\""
    title: Patrick M. Grundy, Mathematics and games, Eureka 2 (1939), reprinted in Eureka 27 (1964)
    locator: pp. 6 to 8 of the 1939 issue (the same result found independently, with the function g defined by the mex rule and the XOR rule for sums)
  - paper: doi:10.1017/S0305004100031510
    title: Patrick M. Grundy and Cedric A. B. Smith, Disjunctive games with the last player losing, Proceedings of the Cambridge Philosophical Society 52(3) (1956)
    locator: pp. 527 to 533 (sums of impartial games under misère play, where the Grundy values of the parts do not decide the sum)
  - book: isbn:9780821851906
    title: Aaron N. Siegel, Combinatorial Game Theory, Graduate Studies in Mathematics 146, American Mathematical Society (2013)
    locator: Chapter IV, Impartial Games, from p. 179 (the theorem and its proof), Chapter V, Misère Play, from p. 223, and Chapter VIII, Transfinite Games, from p. 397 (ordinal values)
  - book: isbn:9781568812779
    title: Michael H. Albert, Richard J. Nowakowski and David Wolfe, Lessons in Play, A K Peters (2007)
    locator: Chapter 7, Impartial Games, from p. 135 (the theorem in the language of game values; general locator)
---

The Sprague-Grundy theorem says that, under normal play, every finite impartial game is equivalent to a single [Nim](/nim/) heap: the position $G$ can be replaced by a heap of $g(G)$ tokens inside any sum of games without changing who wins, where $g$ is the [Grundy number](/grundy-number/). The companion rule is that the Grundy number of a sum is the bitwise XOR of the Grundy numbers of its parts. Together they reduce a game that splits into independent parts to a Nim position, which [Bouton's theorem](/boutons-theorem/) solves. Sprague proved the theorem in 1935 and Grundy independently in 1939.

## Statement

**Setting.** An *impartial game* is given by a set of positions and, for each position $G$, a set of *options*, the positions one move away; both players have the same options. Write $G'$ for an option of $G$. The hypotheses are:

1. **Finite.** Every position has finitely many options, and every play ends after finitely many moves. With finitely many options per position, König's lemma then bounds the length of every play from $G$ by a number $h(G)$, the *height* of $G$.
2. **Normal play.** The player who has no move loses.
3. **Disjunctive sum.** In the sum $G + H$, a position is a pair of positions, and a move is a move in exactly one of the two components, chosen by the mover. The sum has no move exactly when neither component has one. The sum of several games is defined the same way.

The *Nim heap* $*n$ is the game whose options are $*0, *1, \dots, *(n - 1)$. The *Grundy number* is $g(G) = \operatorname{mex}\{g(G') : G' \text{ an option of } G\}$ ([mex](/mex-function/)). Two games are *equivalent*, $G \equiv K$, if for every impartial game $H$ the sums $G + H$ and $K + H$ have the same outcome (a win or a loss for the player to move).

**Theorem.** Under hypotheses 1 to 3:

- (a) $G$ is a loss for the player to move if and only if $g(G) = 0$.
- (b) $g(G + H) = g(G) \oplus g(H)$, where $\oplus$ is bitwise XOR.
- (c) $G \equiv *g(G)$. More generally, $G \equiv K$ if and only if $g(G) = g(K)$.

## In plain words

Some games give both players the same moves, always end, and are lost by the player who cannot move. Pick any position of such a game. The theorem says that, as far as winning goes, the position is the same as one pile of coins in the coin-taking game Nim. The size of that pile is the position's Grundy number, which you can compute from the end of the game backward.

This matters when several games are played side by side and each turn you move in one of them. Replace each game by its pile. You now have a Nim game with several piles, and Nim is solved: combine the pile sizes with the binary operation exclusive or, and the player to move loses exactly when the result is zero. So you never need to search the combined game.

## Proof

All three parts are proved by induction on height. Every option $G'$ satisfies $h(G') < h(G)$, and the options of $G + H$ are the games $G' + H$ and $G + H'$, of smaller height than $G + H$ since $h(G + H) = h(G) + h(H)$.

**Two facts about the mex.** Let $m = \operatorname{mex}(S)$. Then (i) $m \notin S$, and (ii) every $y < m$ is in $S$. Both are the definition of the smallest missing number. Applied to $g(G)$: no option of $G$ has the value $g(G)$, and for every $y < g(G)$ some option of $G$ has the value $y$.

**Part (a).** By induction on $h(G)$. If $G$ has no option, then $g(G) = \operatorname{mex}(\emptyset) = 0$, and the player to move loses by normal play. Otherwise, suppose $g(G) = 0$. By fact (i), no option has value 0, so by induction every option is a win for the player to move there, the opponent; hence every move loses, and $G$ is a loss. Suppose $g(G) > 0$. By fact (ii) with $y = 0$, some option $G'$ has value 0, which is a loss for the opponent by induction; moving to $G'$ wins.

**Part (b).** By induction on $h(G) + h(H)$. Let $a = g(G)$, $b = g(H)$ and $x = a \oplus b$. By the definition of $g$, it is enough to show two things: no option of $G + H$ has value $x$, and every $y < x$ is the value of an option of $G + H$.

*No option has value $x$.* An option is $G' + H$ or $G + H'$. By induction, $g(G' + H) = g(G') \oplus b$. If this were $x = a \oplus b$, XOR with $b$ on both sides would give $g(G') = a$, which fact (i) forbids. The case $G + H'$ is the same with the roles of $G$ and $H$ swapped.

*Every $y < x$ is the value of an option.* Let $z = x \oplus y$, which is nonzero, and let $t$ be its highest set bit. Then $x$ and $y$ agree above bit $t$ and differ at bit $t$; since $y < x$, bit $t$ of $x$ is 1 and bit $t$ of $y$ is 0. Bit $t$ of $x = a \oplus b$ is 1, so exactly one of $a$ and $b$ has bit $t$ set; say $a$ (the other case is symmetric). Then $a \oplus z$ agrees with $a$ above bit $t$ and has bit $t$ equal to 0, so $a \oplus z < a$. By fact (ii), $G$ has an option $G'$ with $g(G') = a \oplus z$. By induction,
$$ g(G' + H) = (a \oplus z) \oplus b = x \oplus z = y. $$

So $g(G + H) = \operatorname{mex}\{\text{values of the options}\} = x$.

**Part (c).** First, $g(*n) = n$, by induction on $n$: the options of $*n$ are $*0, \dots, *(n - 1)$, with values $0, \dots, n - 1$ by induction, and their mex is $n$. Now let $H$ be any impartial game satisfying hypothesis 1. By part (b) twice,
$$ g(G + H) = g(G) \oplus g(H) = g(*g(G)) \oplus g(H) = g(*g(G) + H). $$
By part (a), $G + H$ and $*g(G) + H$ are both losses or both wins for the player to move. So $G \equiv *g(G)$.

For the general form: if $g(G) = g(K)$, then $G \equiv *g(G) = *g(K) \equiv K$, since $\equiv$ is transitive. Conversely, if $G \equiv K$, take $H = K$. By parts (b) and (a), $K + K$ has value $g(K) \oplus g(K) = 0$ and is a loss, so $G + K$ is a loss too, and $g(G) \oplus g(K) = 0$, which means $g(G) = g(K)$. $\blacksquare$

## Consequences

- **Bouton's theorem.** A Nim position $(a_1, \dots, a_k)$ is the sum $*a_1 + \dots + *a_k$. By part (b) and $g(*a) = a$, its value is $a_1 \oplus \dots \oplus a_k$, and by part (a) it is a loss exactly when this is 0. The direct proof is on the [Bouton's theorem](/boutons-theorem/) page.
- **Solving sums part by part.** The outcome of $G_1 + \dots + G_m$ needs only $g(G_1), \dots, g(G_m)$, each computed on its own game graph. A sum of $m$ parts with $N$ positions each has $N^m$ positions, but the values cost about $m$ times the work for one part.
- **The winning move.** In a sum with $x = g(G_1) \oplus \dots \oplus g(G_m) \ne 0$, take a part with $g(G_i) \oplus x < g(G_i)$ (one exists: a part whose value has the top bit of $x$ set) and move it to an option of value $g(G_i) \oplus x$, which exists by fact (ii).
- **The group of impartial games.** Up to equivalence, finite impartial games form a group under $+$ that is isomorphic to $(\mathbb{N}, \oplus)$. Every game is its own negative: $G + G \equiv *0$, the mirror strategy.
- **Splitting moves.** In games where a move may split a heap into two heaps, such as Kayles, a position after the split is a sum, so its value is the XOR of two values. This is why the [Grundy number](/grundy-number/) recursion for octal games runs over XORs.
- **Grundy numbers carry more than outcome.** Two winning positions with values 1 and 2 are not equivalent: added to $*1$, the first gives a loss and the second a win. Win/loss labels of the parts do not determine the outcome of a sum; the values do.

## Tightness

Each hypothesis is needed for the statement as given.

- **Normal play.** Under misère play (the player who cannot move wins), $*0$ and $*2 + *2$ both have Grundy number 0, but the player to move wins $*0$, having no move, and loses $*2 + *2$ by the misère rule for Nim. So the Grundy number does not decide the outcome, and part (a) fails. Grundy and Smith studied misère sums in 1956; their theory is far less complete.
- **Every play ends.** If positions may repeat, the recursion for $g$ is not well founded and plays may be infinite, with draws. A position with a move to itself has no value in $\mathbb{N}$. Loopy impartial games need a generalized Grundy function with an extra symbol for positions from which play can be made to go on forever; see [games on graphs](/games-on-graphs/).
- **Finitely many options.** A position whose options are $*0, *1, *2, \dots$ has no finite Grundy number: every natural number is the value of an option. The theorem holds with ordinal values and the ordinal nim-sum, outside the setting here.
- **Impartial.** If the players have different moves, no Nim heap is equivalent to the game where the first player (Left) has one move, to the empty game, and the other player (Right) has none. Left wins it whoever starts, while $*0$ is a loss for the player to move and $*n$ with $n > 0$ is a win for the player to move. Partisan games need the values of [combinatorial game theory](/combinatorial-game-theory/).
- **Disjunctive sum.** For other ways of combining games, such as a move in every component at once, the XOR rule fails and other theories apply.

## History

Bouton solved Nim in 1901 with the XOR rule. Roland Sprague, in a paper in the Tohoku Mathematical Journal dated 1935 to 1936, showed that every finite impartial game under normal play is equivalent to a Nim heap. Patrick Grundy found the same result independently in a short paper in Eureka in 1939, where he introduced the function now named after him. Grundy and Smith turned to misère sums in 1956. The use of the theorem on octal games such as Kayles is on the [Grundy number](/grundy-number/) page. In the partisan theory of [combinatorial game theory](/combinatorial-game-theory/), the Nim heaps are the nimbers $*n$, one family among all game values.

## References
