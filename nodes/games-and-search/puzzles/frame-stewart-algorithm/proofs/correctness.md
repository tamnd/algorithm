---
title: The Frame-Stewart algorithm makes S(n, p) legal moves and moves the tower, and it runs in O(n^2 p + m) time
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode of the page. A call FRAME-STEWART$(n, s, d, P)$ has $n \ge 0$, a set $P$ of at least 3 pegs, and $s, d \in P$ with $s \ne d$. The table holds $S(n', p')$ and the split $K(n', p')$ for all $n' \le n$ and $3 \le p' \le p$, where $K(n', p')$ is a value of $k$ in $1, \dots, n' - 1$ that reaches the minimum in

$$S(n', p') = \min_{1 \le k \le n' - 1} \bigl(2\,S(k, p') + S(n' - k, p' - 1)\bigr).$$

**Precondition (Pre).** The $n$ discs to move are the $n$ smallest discs that lie on the pegs of $P$. They form a tower on top of peg $s$. Every other disc on a peg of $P$ is larger than each of the $n$ discs.

**Postcondition (Post).** The $n$ discs form a tower on top of peg $d$, every other disc is where it was before the call, and the call made exactly $S(n, |P|)$ moves, each of them legal and each between two pegs of $P$.

**Lemma 1 (larger discs act as the floor).** Assume Pre. A move of one of the $n$ discs between two pegs of $P$ is legal in the whole puzzle if and only if it is legal in the puzzle that has only the $n$ discs on the pegs of $P$.

*Proof.* A move takes the top disc $x$ of a peg $q$ to a peg $q'$. Under Pre, while the $n$ discs are the only discs that move, every other disc on a peg of $P$ lies below all of them and is larger than $x$. So $x$ is on top of $q$ in the whole puzzle exactly when it is on top among the $n$ discs, and the top disc of $q'$ in the whole puzzle is smaller than $x$ exactly when the top one among the $n$ discs is smaller than $x$: a larger disc below them never is. $\square$

**Theorem 1 (correctness).** Every call that starts under Pre ends with Post.

*Proof.* Induction on $n$.

$n = 0$: line L1 returns with no move, and $S(0, \cdot) = 0$.

$n = 1$: line L2 moves the only disc, which is on top of $s$ by Pre. Every other disc on $d$ is larger, so the move is legal, and it is 1 = $S(1, \cdot)$ move.

$n \ge 2$ and $|P| = 3$: line L5 runs the three-peg recursion. The first call moves discs $1, \dots, n - 1$ (the smallest $n - 1$) from $s$ to $a$; Pre holds for it, because disc $n$ and all other discs on $P$ are larger. By the induction hypothesis it ends with them on $a$ after $S(n - 1, 3)$ legal moves. Then disc $n$ is on top of $s$ and every disc on $d$ is larger than it, so its move is legal. The last call moves the $n - 1$ discs from $a$ to $d$, where they now lie on disc $n$; Pre holds again, and the induction hypothesis applies. The total is $2(2^{n-1} - 1) + 1 = 2^n - 1 = S(n, 3)$.

$n \ge 2$ and $|P| \ge 4$: let $k = K(n, |P|)$, so $1 \le k \le n - 1$.

- L7: the $k$ smallest of the $n$ discs are the $k$ smallest discs on $P$, they lie on top of $s$, and all other discs on $P$ are larger. Pre holds, so by the induction hypothesis ($k < n$) the call ends with them as a tower on $a$ after $S(k, |P|)$ legal moves, and nothing else moved.
- L8: now the discs $k + 1, \dots, n$ of the group form a tower on top of $s$. On the pegs of $P \setminus \{a\}$ they are the smallest discs, because the $k$ smaller ones are on $a$, and every other disc on these pegs is larger. The set $P \setminus \{a\}$ has at least 3 pegs and contains $s$ and $d$. So Pre holds, and by the induction hypothesis ($n - k < n$) the call ends with these discs as a tower on $d$, after $S(n - k, |P| - 1)$ legal moves between pegs of $P \setminus \{a\}$. No move touches peg $a$, so the $k$ small discs stay there.
- L9: the $k$ small discs form a tower on $a$; they are the smallest discs on $P$, and the other discs on $P$, including the $n - k$ discs now on $d$, are larger. Pre holds, and the call ends with the $k$ discs on top of $d$, above the $n - k$ discs, after $S(k, |P|)$ legal moves.

The legality of each move in the whole puzzle follows from Lemma 1. At the end the $n$ discs form a tower on $d$, every other disc is untouched, and the number of moves is $2S(k, |P|) + S(n - k, |P| - 1) = S(n, |P|)$ by the choice of $k$. $\square$

The top call FRAME-STEWART$(n, \text{source}, \text{target}, \{0, \dots, p - 1\})$ meets Pre, because all discs form a tower on the source. So the algorithm solves the puzzle with $S(n, p)$ moves.

**Theorem 2 (termination).** Every call returns.

*Proof.* A call with $n \le 1$ returns at L1 or L2 without a recursive call. A call with $n \ge 2$ makes at most three recursive calls, each with $n - 1$, $k$ or $n - k$ discs, and $1 \le k \le n - 1$, so each has at most $n - 1$ discs: the number of discs drops by at least 1 at each level. So the depth of the recursion is at most $n$, every call makes at most three calls, and the tree of calls is finite. $\square$

**Theorem 3 (cost).** Let $m = S(n, p)$. Filling the table costs $O(n^2 p)$ time and $O(np)$ space, and the recursion costs $O(m)$ time and $O(np)$ space besides the output.

*Proof.* The table has at most $(n + 1)(p - 2)$ entries. The entries with $n' \le 1$ or $p' = 3$ cost $O(1)$ each. Each other entry takes the minimum of $n' - 1 \le n$ sums of two earlier entries, so it costs $O(n)$. All values are at most $2^n$, so they fit in $O(n)$ bits, which the word RAM model of the page counts as a constant number of words for the sizes where the moves can be listed. This gives $O(n^2 p)$ time and $O(np)$ space.

For the recursion, every call other than the top call has at least one disc: L5 passes $n - 1 \ge 1$, L7 and L9 pass $k \ge 1$, and L8 passes $n - k \ge 1$. A call with one disc is a leaf of the call tree and makes exactly one move. A call with $n \ge 2$ makes two or three recursive calls (and L5 also makes one move). Let the call tree have $\ell$ leaves and $i$ inner nodes; since each inner node has at least 2 children, $i \le \ell - 1$. Each leaf makes one move, so $\ell \le m$, and the tree has at most $2m - 1$ nodes. Keep $P$ as a bit mask of $p$ bits, with $p$ at most the word size. Then each call does $O(1)$ work besides its children: it reads one table entry, finds $a$ as the lowest set bit of $P$ with the bits of $s$ and $d$ cleared, and forms $P \setminus \{a\}$ by clearing one bit. So the recursion takes $O(m)$ time. The stack has depth at most $n$ by Theorem 2 and $O(1)$ words per frame, so $O(n)$ space, within the $O(np)$ of the table. If $P$ is kept as a list of pegs instead, each call costs $O(p)$ and the bounds become $O(mp)$ time and $O(np)$ stack space. $\square$
