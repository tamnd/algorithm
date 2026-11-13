---
title: The opening book keys transpositions together, has no cycle, backs up the negamax value of its moves, and draws moves by weight
proves: [correctness, complexity]
status: full
---

We use the operations BOOK-PROBE, BOOK-ADD, BOOK-CHOOSE, BOOK-LEARN and BOOK-BACKUP of the page, on tic-tac-toe. A position $p$ is a set of pairs (cell, piece). The key is $Z(p) = \bigoplus_{(i, x) \in p} Z[i, x]$, where $\oplus$ is the XOR of 64-bit words and $Z[i, x]$ is a fixed random word, as in [Zobrist hashing](/zobrist-hashing/).

**Lemma 1 (transpositions share a key).** If two move sequences from the empty board reach the same position $p$, then line L6 gives both the key $Z(p)$.

*Proof.* Line L2 starts with the key 0 of the empty board. A move puts the piece $x$ on the empty cell $i$, so the new position is $p \cup \{(i, x)\}$, and line L6 sets the key to $Z(p) \oplus Z[i, x] = Z(p \cup \{(i, x)\})$. By induction on the number of moves, the key after a sequence is $Z$ of the position it reaches. This depends only on the position, not on the order of the moves, because $\oplus$ is associative and commutative. $\square$

So a book stores one entry per position, not per move sequence, as long as no two positions in it have the same key. With 64-bit random words that is very unlikely for a small book, and the tests check it for all 5,478 positions that can arise in tic-tac-toe with the seed of the tests. A real book cannot check it and accepts a small risk.

**Lemma 2 (the book is a DAG).** Let the book graph have an arc from $p$ to the position after each book move of $p$. The graph has no cycle, and the order by decreasing number of pieces is a reverse topological order.

*Proof.* A move adds one piece, so every arc goes from a position with $j$ pieces to one with $j + 1$. A cycle would need the number of pieces to return to its start, which is impossible. If positions are sorted by decreasing number of pieces, every arc goes from a later position to an earlier one. $\square$

**Theorem 3 (backup).** Let $\text{leaf}(c)$ be a value for the side to move at each position $c$ that is not in the book. Define the *book value* $W(p)$ of a book position $p$ by $W(p) = \max_x -W'(c_x)$ over the book moves $x$ of $p$, where $c_x$ is the position after $x$, and $W'(c) = W(c)$ if $c$ is in the book and $\text{leaf}(c)$ otherwise. Then BOOK-BACKUP returns $W(p)$ for every book position. This is also the value of the negamax recursion that follows the book moves as a tree, with no sharing.

*Proof.* By Lemma 2, line L12 handles each position after all its children in the book. At line L13, the value of each child is either already computed, by induction equal to $W(c)$, or given by leaf. So line L13 computes the maximum in the definition. The definition of $W$ is the negamax recursion over the book moves; a position reached by two paths gets the same value on both, so computing it once does not change the result. $\square$

If $\text{leaf}$ is the exact game value, $W(p)$ is the value of $p$ when both sides must play book moves while they are in the book and play perfectly after. With all moves of the first four plies in the book and the exact leaf values, the tests find $W(\text{empty}) = 0$, a draw, the known value of tic-tac-toe.

**Theorem 4 (choice by weight).** Let $E$ be the moves of $p$ with positive weight, $w_x$ their weights and $W = \sum_{x \in E} w_x$. If $u$ is uniform in $[0, 1)$, BOOK-CHOOSE returns the move $x$ with probability $w_x / W$, and it returns NIL when $E$ is empty.

*Proof.* Line L8 handles the empty case. Line L9 walks through $E$ in a fixed order $x_1, \ldots, x_k$ and returns the first $x_j$ with $u W < w_{x_1} + \cdots + w_{x_j}$. This is the event $u \in [S_{j-1} / W, S_j / W)$ with $S_j$ the partial sums, an interval of length $w_{x_j} / W$. $\square$

The implementation computes $uW$ exactly with rational numbers, so the only error is that `random.random` returns a multiple of $2^{-53}$.

**Theorem 5 (learning).** After $a$ wins and $l$ losses of the program on lines through a book move $x$ of its own, in any order, BOOK-LEARN leaves the weight $w_0 (3/2)^a (1/2)^l$ if this product never fell below $1/4$ after a step, and 0 otherwise. A move of weight 0 is never chosen again, by Theorem 4.

*Proof.* Line L10 does nothing for a draw. Line L11 multiplies the weight by $3/2$ for a win and by $1/2$ for a loss, and sets it to 0 when it falls below the floor $1/4$. A weight of 0 stays 0 under multiplication. $\square$

**Cost.** BOOK-PROBE and one step of BOOK-ADD cost $O(1)$ expected time for the [hash table](/hash-table/) plus the XOR; the implementation also computes the key from scratch in BOOK-PROBE, which costs one step per cell. BOOK-ADD and BOOK-LEARN cost $O(h)$ for a line of $h$ book plies. BOOK-CHOOSE costs $O(k)$ for $k$ book moves. BOOK-BACKUP costs $O(V \log V + E)$ with the sort, or $O(V + E)$ with a bucket per number of pieces or any [topological sort](/topological-sort/), for $V$ positions and $E$ book moves, plus the calls of leaf. $\blacksquare$
