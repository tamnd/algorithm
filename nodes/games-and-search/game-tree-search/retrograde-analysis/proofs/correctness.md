---
title: Retrograde analysis by layers gives the exact value and the exact distance to mate of every position
proves: [correctness, termination, complexity]
status: full
---

We use the pseudocode RETROGRADE of the page. $S$ is a finite set of positions. Each $p \in S$ has a finite list $\text{MOVES}(p)$ of moves; a move leads to a position of $S$ or out of $S$, and a move out of $S$ leads to a draw. A *mate* is a position of $S$ that is lost for the side to move by the rules. We assume that UNMOVES is the inverse of MOVES on $S$: $p \in \text{UNMOVES}(q)$ exactly when $p, q \in S$ and some move of $p$ leads to $q$. A move listed $k$ times counts $k$ times in both. The tests check this for the 4 by 4 toy.

**Definitions.** Let $L_0$ be the set of mates and $W_0 = \emptyset$. For $n \ge 1$ let
$$ W_n = W_{n-1} \cup \{ p : \text{some move of } p \text{ leads to } L_{n-1} \}, \qquad L_n = L_{n-1} \cup \{ p : p \text{ has a move, and every move of } p \text{ leads to } W_{n-1} \}. $$
A move out of $S$ is in neither set. The sets grow with $n$.

**Lemma 1 (meaning).** $p \in W_n$ exactly when the side to move at $p$ can force a mate of the opponent within $n$ plies. $p \in L_n$ exactly when the opponent can force a mate of the side to move within $n$ plies, whatever the side to move does.

*Proof.* By induction on $n$. For $n = 0$: no mate of the opponent happens in 0 plies, and a mate within 0 plies is a mate now. For $n \ge 1$: the side to move forces a mate within $n$ plies exactly when it has a move to a position in which the opponent, now to move, is forced to be mated within $n - 1$ plies, which is $L_{n-1}$ by induction. The side to move is forced to be mated within $n$ plies exactly when it is mated now, or it has moves and every move leads to a position from which the opponent forces a mate within $n - 1$ plies, which is $W_{n-1}$. A move out of $S$ ends in a draw, so it gives no forced mate. $\square$

Since the sets grow and $S$ is finite, they stop growing. If $W_n = W_{n-1}$ and $L_n = L_{n-1}$, then $W_{n+1} = W_n$ and $L_{n+1} = L_n$, because each set depends only on the sets of the round before. So there is a first $N$ with $W_N = W_{N+1}$ and $L_N = L_{N+1}$, and the sets do not change after it. Write $W = W_N$ and $L = L_N$.

**Lemma 2 (draws).** If $p \notin W \cup L$, then neither side can force a mate from $p$.

*Proof.* Suppose the side to move can force a mate. Fix a strategy that does so. Every play that follows it ends in a mate, so the tree of these plays has no infinite path. Each position has finitely many moves, so by König's lemma the tree is finite, and it has a depth $n$. Then $p \in W_n \subseteq W$. The same argument for the opponent gives $p \in L$. $\square$

So the positions outside $W \cup L$ are draws: each side can avoid a mate for ever, or the play leaves $S$ by a move that is a draw. A draw by repetition, an infinite play, is one of these cases.

**Theorem 3 (the layers).** After line L7 has run $n$ times, the labeled positions are exactly $W_n \cup L_n$. A position $p$ gets the label WIN with distance $n$ when $n$ is the least index with $p \in W_n$, and LOSS with distance $n$ when $n$ is the least index with $p \in L_n$. The layer $F$ holds exactly the positions first labeled in the last round.

*Proof.* By induction on $n$. For $n = 0$, line L1 labels exactly $L_0$ with distance 0, and $F = L_0$.

Assume the claim for $n$, and let $F$ be the positions first labeled in round $n$, so $F = (W_n \cup L_n) \setminus (W_{n-1} \cup L_{n-1})$ for $n \ge 1$ and $F = L_0$ for $n = 0$.

*WIN in round $n + 1$.* Line L5 labels $p$ WIN when $p$ is not labeled and some move of $p$ leads to a LOSS position $q \in F$. By induction $q \in L_n$, so $p \in W_{n+1}$. Conversely, let $p \in W_{n+1} \setminus (W_n \cup L_n)$. Some move leads to $q \in L_n$. The least index of $q$ is not more than $n$; if it were less than $n$, then $p$ would be in $W_n$. So $q \in F$, and line L5 labels $p$ when $q$ is processed, unless $p$ was labeled earlier in the same round, which is also in round $n + 1$.

*LOSS in round $n + 1$.* The counter of $p$ starts at the number of moves of $p$ and goes down by 1 for each move of $p$ to a position that was labeled WIN, when that position is processed. Each WIN position is processed once, in the round after it is labeled, and UNMOVES lists $p$ once per move into it. Round $n + 1$ processes the positions labeled in round $n$. So when round $n + 1$ has processed its whole layer, the counter of a position that is still unlabeled is the number of its moves that do not lead to $W_n$. The counter reaches 0 in round $n + 1$ exactly when every move of $p$ leads to $W_n$ and $p$ was not labeled before, that is when $p \in L_{n+1} \setminus (W_n \cup L_n)$. A move out of $S$ never lowers the counter.

*No position in both.* $W_n \cap L_n = \emptyset$ for all $n$, by induction: a position in $W_n$ has a move into $L_{n-1}$, and a position in $L_n$ has every move into $W_{n-1}$, and these are disjoint. Also, a position that is labeled is never labeled again, because lines L5 and L6 skip labeled positions. So the labels and the layer are as claimed. $\square$

**Corollary 4.** RETROGRADE stops after at most $|S| + 1$ rounds, because each round before the last labels at least one new position. When it stops, $W \cup L$ is labeled, and line L8 labels the rest DRAW, which is right by Lemma 2.

**Corollary 5 (exact distances).** The distance of a WIN position $p$ is $1 + \min$ of the distances of its moves to LOSS positions: the winner mates as fast as possible. The distance of a LOSS position that is not a mate is $1 + \max$ of the distances of its moves, all of which go to WIN positions: the loser holds out as long as possible. So the distance is the *distance to mate* (DTM) under optimal play by both sides. This follows from Lemma 1 and the least indexes in Theorem 3. The tests check these two equations at every position of the toy, and compare all values and distances with a direct computation of the sets $W_n$ and $L_n$.

**Cost.** Each position is in a layer at most once. When $q$ is processed, line L4 looks at each move into $q$ once, so all rounds together look at each move once. A counter is set the first time it is needed, from one call of MOVES. So the time is $O(V + E)$ for $V = |S|$ positions and $E$ moves, plus the time of the move generators, and the space is $O(V)$ for the labels, the distances and the counters, with no stored graph. $\blacksquare$
