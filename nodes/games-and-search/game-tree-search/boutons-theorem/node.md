---
tag: 9301CP
kind: theorem
slug: boutons-theorem
name: Bouton's theorem
aliases:
- Bouton's theorem on Nim
- Nim-sum theorem
area: games-and-search/game-tree-search
level: core
summary: In Nim under normal play, the player to move loses exactly when the XOR of the heap sizes is 0. From any other position a move to XOR 0 exists and wins.
prereqs: [nim, bitwise-operations, winning-losing-states]
see_also: [sprague-grundy-theorem, grundy-number, mex-function, combinatorial-game-theory, zermelo-theorem, solved-game]
sources:
  - paper: doi:10.2307/1967631
    title: Charles L. Bouton, Nim, a game with a complete mathematical theory, Annals of Mathematics, Second Series, 3(1/4) (1901 to 1902)
    locator: pp. 35 to 39 (the theorem for three heaps, its extension to any number of heaps, and the rule for the game where the player who takes the last token loses)
  - paper: "\"A generalization of the game called nim\""
    title: Eliakim Hastings Moore, A generalization of the game called nim, Annals of Mathematics, Second Series, 11(3) (1910), JSTOR 1967321
    locator: pp. 93 to 94 (the theorem for moves on at most k heaps, with digit sums modulo k + 1)
  - book: isbn:9780821851906
    title: Aaron N. Siegel, Combinatorial Game Theory, Graduate Studies in Mathematics 146, American Mathematical Society (2013)
    locator: Chapter IV, Impartial Games, from p. 179 (Bouton's theorem and nim-sums), and Section V.1, Misère Nim, from p. 224
  - book: isbn:9781568812779
    title: Michael H. Albert, Richard J. Nowakowski and David Wolfe, Lessons in Play, A K Peters (2007)
    locator: Chapter 7, Impartial Games, from p. 135 (the nim-sum and the solution of Nim; general locator)
---

Bouton's theorem solves [Nim](/nim/): under normal play, the player to move loses exactly when the bitwise XOR of the heap sizes, the *nim-sum*, is 0. From a position with a nonzero nim-sum, lowering a suitable heap makes the nim-sum 0, and repeating this wins. Charles Bouton proved it in 1901, with the rule for the misère game, where the player who takes the last token loses. The theorem is the first full solution of a nontrivial game, and the [Sprague-Grundy theorem](/sprague-grundy-theorem/) extends it to every finite impartial game.

## Statement

**Setting.** A Nim position is a tuple $(a_1, \dots, a_k)$ of nonnegative integers, with $k \ge 1$ finite. A move replaces one $a_i > 0$ by some $b$ with $0 \le b < a_i$. Two players alternate. Write $\oplus$ for bitwise XOR ([bitwise operations](/bitwise-operations/)) and
$$ x(a_1, \dots, a_k) = a_1 \oplus a_2 \oplus \dots \oplus a_k. $$

**Theorem (normal play).** Assume normal play: a player with no move loses. Then the player to move loses with best play (a P-position) if and only if $x = 0$. If $x \ne 0$ and $t$ is the index of the highest set bit of $x$, the moves to a position with nim-sum 0 are exactly the moves $a_i \to a_i \oplus x$ for the heaps $a_i$ whose bit $t$ is 1. There is an odd number of such heaps, and so at least one.

**Theorem (misère play).** Assume misère play: a player with no move wins, so the player who takes the last token loses. Then the player to move loses with best play if and only if

- some heap has 2 or more tokens and $x = 0$, or
- every heap has at most 1 token and the number of heaps with 1 token is odd.

Both statements need the game to be finite (finitely many heaps of finite size, so every play ends) and need each move to change exactly one heap. Nim has no draws, so "loses with best play" and "is not a win" mean the same thing here.

## In plain words

Write each heap size in binary and stack the numbers. Look at each column of digits. Call the position balanced when every column has an even number of ones.

From a balanced position, any move breaks the balance: a move changes one heap, so it changes at least one of its digits, and that column turns odd. From an unbalanced position, you can always restore the balance with one move: find the leftmost odd column, pick a heap with a one there, and change that heap's digits so that every column turns even. The new number is smaller, so the move is legal.

The empty table is balanced. So whoever always leaves a balanced position gets the last move. In the variant where the last move loses, the same plan works until only heaps of size one remain.

## Proof

**Normal play.** Let $P$ be the set of positions with $x = 0$. The proof shows three facts and then puts them together.

*Fact 1: the position with no move is in $P$.* The only position with no move is $(0, \dots, 0)$, and its nim-sum is 0.

*Fact 2: every move from a position in $P$ leads out of $P$.* A move changes one heap from $a_i$ to $b \ne a_i$. XOR is associative and commutative, and $y \oplus y = 0$, so the new nim-sum is
$$ x' = x \oplus a_i \oplus b. $$
If $x = 0$, then $x' = a_i \oplus b$, and this is nonzero because $a_i \ne b$.

*Fact 3: from a position with $x \ne 0$, the moves into $P$ are exactly the moves $a_i \to a_i \oplus x$ for the heaps with bit $t$ set, and there is an odd number of them.* Bit $t$ of $x$ is the XOR of the bits $t$ of all heaps, so it is 1 exactly when an odd number of heaps have bit $t$ set. Since bit $t$ of $x$ is 1, that number is odd, so at least one. Take a heap $a_i$ and set $b = a_i \oplus x$. The number $x$ has no set bit above $t$, so $b$ and $a_i$ agree in every bit above $t$, and they differ in bit $t$.

- If bit $t$ of $a_i$ is 1, then bit $t$ of $b$ is 0, and $b < a_i$, since the two numbers first differ at bit $t$. So $a_i \to b$ is a legal move, and its nim-sum is $x \oplus a_i \oplus b = x \oplus x = 0$.
- If bit $t$ of $a_i$ is 0, then $b > a_i$, so this heap has no move to nim-sum 0: by the formula for $x'$, the only new size with $x' = 0$ is $b = a_i \oplus x$, and it is too large.

*Putting it together.* Let $s = a_1 + \dots + a_k$. Every move lowers $s$ by at least 1. The claim is: for every position, the player to move loses if the position is in $P$ and wins if it is not. The proof is by strong induction on $s$.

- $s = 0$: the position is $(0, \dots, 0)$, in $P$ by Fact 1, and the player to move has no move, so loses under normal play.
- $s > 0$ and the position is in $P$: there is a move, since some heap is nonempty. By Fact 2, every move leads to a position outside $P$ with a smaller total, where by induction the player to move, the opponent, wins. So every move loses.
- $s > 0$ and the position is not in $P$: by Fact 3, some move leads to a position in $P$ with a smaller total, where by induction the player to move, the opponent, loses. So that move wins.

This proves the first sentence of the theorem. The second sentence is Fact 3, together with Fact 2 for the converse: a move to a nonzero nim-sum leads to a position where the opponent wins, so the winning moves are exactly the moves into $P$.

**Misère play.** Let $M$ be the set of positions described in the misère theorem. Call a heap *big* if it has 2 or more tokens.

*Fact 4: if exactly one heap is big, then $x \ne 0$.* The other heaps are 0 or 1, so they have no set bit above bit 0. The big heap has a set bit at position 1 or higher, and nothing cancels it. So $x \ge 2$. Hence a position in $M$ with a big heap has at least two big heaps.

*Fact 5: the position $(0, \dots, 0)$ is not in $M$.* It has no big heap and zero heaps of size 1, an even number.

*Fact 6: every move from a position in $M$ leads out of $M$.*

- No big heap, odd number of 1-heaps: a move empties one 1-heap, so the new position has no big heap and an even number of 1-heaps.
- Some big heap and $x = 0$: by Fact 4 there are at least two big heaps, and a move changes only one, so the new position still has a big heap. By Fact 2 its nim-sum is not 0.

*Fact 7: from a position outside $M$ other than $(0, \dots, 0)$, some move leads into $M$.*

- No big heap, an even and nonzero number of 1-heaps: empty one of them. The count becomes odd.
- Exactly one big heap $a_j$: let $c$ be the number of 1-heaps among the others. If $c$ is even, lower $a_j$ to 1, and if $c$ is odd, lower it to 0. Both are legal since $a_j \ge 2$. The new position has no big heap and an odd number of 1-heaps.
- Two or more big heaps and $x \ne 0$: make the normal-play move of Fact 3. It changes one heap, so a big heap remains, and the nim-sum becomes 0.

*Putting it together.* The induction on $s$ is the same as before. For $s = 0$ the player to move has no move and wins under misère play, and the position is not in $M$ by Fact 5. A position in $M$ has $s > 0$ (it has a big heap or an odd number of 1-heaps), so it has a move, and every move leads out of $M$ by Fact 6, to a smaller total where the opponent wins by induction. A position outside $M$ with $s > 0$ has a move into $M$ by Fact 7, where the opponent loses by induction. $\blacksquare$

## Consequences

- **A linear-time solution.** Deciding the outcome and finding a winning move takes $O(n)$ bit operations for $n$ input bits. The lower bound and the input-size discussion are on the [Nim](/nim/) page.
- **Two heaps.** $(a, b)$ is a P-position exactly when $a = b$, since $a \oplus b = 0$ means $a = b$. The second player wins by copying, the mirror strategy.
- **Grundy values of Nim.** The value of a single heap $a$ under the [mex](/mex-function/) rule is $a$, because its options are the heaps $0, \dots, a - 1$. The [Sprague-Grundy theorem](/sprague-grundy-theorem/) then gives that the [Grundy number](/grundy-number/) of $(a_1, \dots, a_k)$ is $x$, not only whether it is 0. Bouton's theorem is the special case "value 0 if and only if P-position".
- **The group of nim-sums.** $(\mathbb{N}, \oplus)$ is an abelian group in which every element is its own inverse. This is why a sum of a game with itself is always a second-player win: $G + G$ has value $g \oplus g = 0$.
- **Moore's generalization.** If a move may change from 1 to $k$ heaps, the player to move loses exactly when, in each bit position, the number of heaps with a 1 there is a multiple of $k + 1$ (Moore, 1910). The proof has the same three facts, with arithmetic modulo $k + 1$ in each column in place of XOR.

## Tightness

Each hypothesis is needed.

- **Normal play.** Under misère play the XOR rule fails at the end of the game: $(1, 1)$ has $x = 0$, but the player to move wins by taking one token, and $(1)$ has $x = 1$, but the player to move must take the last token and loses. The misère statement shows that the rule fails only on positions with no big heap.
- **One heap per move.** In Moore's game with $k = 2$, the position $(1, 1)$ has $x = 0$, but the player to move takes both tokens and wins.
- **Moves to any smaller size.** In the subtraction game where a move removes 1 or 2 tokens, a single heap of 3 has $x = 3$, but it is a loss for the player to move: both moves leave a heap of 1 or 2, which the opponent empties. The Nim proof breaks at Fact 3, because the move $a_i \to a_i \oplus x$ may be forbidden. [Grundy numbers](/grundy-number/) repair this.
- **Finiteness.** With infinitely many nonempty heaps the nim-sum is not defined and a play need not end. Heaps of infinite ordinal size need the ordinal form of the nim-sum, which is outside this theorem.

## History

Bouton's paper appeared in the Annals of Mathematics in its volume for 1901 to 1902, under the title "Nim, a game with a complete mathematical theory". It proves the theorem for three heaps, then states the extension to any number of heaps, and treats the misère rule. Moore's 1910 paper in the same journal solved the game where a move takes from at most $k$ heaps. The later step, that every finite impartial game under normal play is equivalent to a Nim heap, made Bouton's nim-sum the general rule for sums of impartial games; its history is on the [Sprague-Grundy theorem](/sprague-grundy-theorem/) page.

## References
