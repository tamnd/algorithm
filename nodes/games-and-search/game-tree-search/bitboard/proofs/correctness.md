---
title: The bitboard operations of tic-tac-toe and Connect Four match the rules of the games
proves: [correctness]
status: full
---

We use the pseudocode of the page, lines L1 to L13. Integers are in two's complement, and $x \mathbin{\&} y$, $x \mid y$, $x \oplus y$ and $\lnot x$ are the bitwise operations. A bitboard $b$ stands for the set $\{i : \text{bit } i \text{ of } b \text{ is } 1\}$, so $\&$ is intersection, $\mid$ is union, $\oplus$ is symmetric difference, and $\lnot b \mathbin{\&} F$ is the complement within a set $F$.

**Claim 1 (lowest bit, lines L4 to L6).** For $b > 0$, $b \mathbin{\&} (-b)$ is $2^j$, where $j$ is the index of the lowest set bit of $b$. So BITS outputs the members of $b$ in increasing order and stops after $|b|$ passes.

*Proof.* Write $b = u \cdot 2^{j+1} + 2^j$ with $u \ge 0$, so bits $0$ to $j-1$ are 0. In two's complement, $-b = \lnot b + 1$. The low $j$ bits of $\lnot b$ are 1, bit $j$ is 0, and the higher bits are those of $\lnot u$. Adding 1 carries through the low $j$ bits, clears them, and sets bit $j$, and the higher bits stay those of $\lnot u$. So $b$ and $-b$ share bit $j$ and no other bit. Line L6 removes bit $j$ from $b$, so each pass outputs the smallest remaining member, and the loop ends when $b = 0$. $\square$

**Claim 2 (tic-tac-toe, lines L1 to L3).** Bit $i$ stands for square $i$, $F = 2^9 - 1$, and the 8 line masks $w$ are the sets of three squares of a row, a column or a diagonal. Then HAS-LINE$(b)$ is true if and only if the squares of $b$ contain a line. EMPTY$(x, o)$ is the set of empty squares. PLAY$(x, i)$ adds square $i$ to $x$.

*Proof.* $b \mathbin{\&} w = w$ says that $w \subseteq b$, so line L1 tests each line for containment. $\lnot(x \mid o) \mathbin{\&} F$ is the complement of $x \cup o$ within the 9 squares. $x \mid 2^i$ is $x \cup \{i\}$. $\square$

**Connect Four layout.** The board has $w$ columns and $h$ rows. Cell $(c, r)$, column $c$ and row $r$ from the bottom, is bit $c(h+1) + r$. The bits $c(h+1) + h$ are *guard bits* and are never set. Let $B$ be the set of the $w h$ cell bits. A position is a pair (cur, mask), where mask is the set of all stones and cur is the set of the stones of the side to move. In each column the stones fill the rows $0, \ldots, j-1$ for some $j \le h$, by the rules of the game.

**Claim 3 (moves, lines L7 to L9).** CAN-PLAY$(\text{mask}, c)$ is true if and only if column $c$ has an empty cell. PLAY$(\text{cur}, \text{mask}, c)$ puts a stone of the side to move on the lowest empty cell of column $c$, changes no other cell, and returns the position with the other side to move.

*Proof.* Column $c$ is full exactly when its top cell $(c, h-1)$ holds a stone, since stones fill a column from the bottom. That is the test of line L7. For line L9, let column $c$ hold $j < h$ stones, so its bits are $2^{c(h+1)}, \ldots, 2^{c(h+1)+j-1}$. Adding $2^{c(h+1)}$ to mask adds 1 to the block of $j$ ones that starts at bit $c(h+1)$. The carry clears these $j$ bits and sets bit $c(h+1) + j$, which is 0 in mask, so the carry stops there and the other bits do not change. The OR with mask restores the cleared bits. So the new mask is mask plus the cell $(c, j)$, the lowest empty cell. Before the move, cur holds the stones of the mover, and $\text{cur} \oplus \text{mask}$ holds the stones of the opponent. Line L8 makes this the new cur, which is right, since the opponent moves next and the new stone belongs to the mover. $\square$

**Claim 4 (four in a row, lines L10 to L13).** Let $b \subseteq B$. Then WON$(b)$ is true if and only if $b$ contains four cells in a row, in a column, or on a diagonal.

*Proof.* After line L11, bit $i$ of $m$ is set if and only if bits $i$ and $i + s$ of $b$ are set. So bit $i$ of $m \mathbin{\&} (m \gg 2s)$ is set if and only if bits $i$, $i + s$, $i + 2s$ and $i + 3s$ of $b$ are set. It remains to show that, for the four shifts, these four bits are in $B$ exactly when they are four cells in a line.

If four cells are in a line, they are $(c + k\,\delta_c, r + k\,\delta_r)$ for $k = 0, 1, 2, 3$, with $(\delta_c, \delta_r)$ one of $(0, 1)$, $(1, 0)$, $(1, -1)$ and $(1, 1)$, after we take the end with the smaller column as the start. Their bits are $i + k s$ with $i = c(h+1) + r$ and $s = \delta_c (h+1) + \delta_r$, which is $1$, $h + 1$, $h$ and $h + 2$.

Conversely, let $i = c(h+1) + r$ with $0 \le r < h$, and let $i + ks \in b \subseteq B$ for $k = 1, 2, 3$.
- $s = 1$. If $r + k = h$ for some $k \le 3$, then bit $i + k$ is the guard bit of column $c$, which is not in $B$. So $r + 3 < h$, and the cells are $(c, r + k)$, a vertical line.
- $s = h + 1$. Then $i + ks = (c + k)(h+1) + r$, the cell $(c + k, r)$. These bits are in $B$ only if $c + 3 < w$, and they form a horizontal line.
- $s = h$. Then $i + ks = (c + k)(h+1) + (r - k)$. If $r - k = -1$ for some $k \le 3$, that bit is $(c + k - 1)(h+1) + h$, a guard bit. So $r - 3 \ge 0$, and the cells $(c + k, r - k)$ form a diagonal.
- $s = h + 2$. Then $i + ks = (c + k)(h+1) + (r + k)$. If $r + k = h$ for some $k \le 3$, that bit is a guard bit. So $r + 3 < h$, and the cells $(c + k, r + k)$ form a diagonal.

Line L13 is reached only when no shift finds such an $i$. $\square$

The guard bits do the work in Claim 4: a run of four bits that would wrap from the top of one column to the bottom of the next must pass through a guard bit, which is 0. Without them, a layout with $h$ bits per column gives false lines. For example, with $h = 4$ and the shift $h + 1 = 5$ of the up diagonal in that layout, the cells $(0, 3)$, $(2, 0)$, $(3, 1)$ and $(4, 2)$ have the bits $3, 8, 13, 18$, which differ by 5, but they are not on a line.
