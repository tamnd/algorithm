---
title: Oscillating sort sorts in ceil(log_P S) merge levels
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. Let $P = T - 2 \ge 2$. The work tapes are read backward, so each work tape is a stack of runs: line L4 and line L8 append a run at the end, and line L7 removes the last run. Reading a run backward gives its items in the reverse order. Write $\overline{\mathrm{dir}}$ for the opposite direction of $\mathrm{dir}$.

Let $F_1, F_2, \ldots, F_S$ be the consecutive parts of $M$ items of $F$ (the last may be shorter), so that the $j$-th execution of line L4 reads $F_j$.

**Lemma.** Let $n \ge 1$. Suppose that BUILD$(n, x, \mathrm{dir})$ starts when line L4 has read $F_1, \ldots, F_{j}$. Then it returns when line L4 has read $F_1, \ldots, F_{j+n}$, and at that time:

1. tape $x$ holds its old runs and, after them, one new run, which holds the items of $F_{j+1}, \ldots, F_{j+n}$ sorted in the direction $\mathrm{dir}$;
2. every other work tape holds exactly its old runs;
3. the recursion below this call has $\lceil \log_P n \rceil$ levels of merges.

*Proof.* By strong induction on $n$.

For $n = 1$, lines L3 and L4 read $F_{j+1}$, sort it in the direction $\mathrm{dir}$, and append it to $x$. No other tape changes and there is no merge, and $\lceil \log_P 1 \rceil = 0$.

For $n \ge 2$, line L5 gives parts $n_1 \ge \cdots \ge n_P$ with $n_1 = \lceil n/P \rceil < n$ and sum $n$, and $P$ distinct tapes $y_1, \ldots, y_P$, all different from $x$. Line L6 calls BUILD$(n_i, y_i, \overline{\mathrm{dir}})$ for each $i$ with $n_i > 0$, in the order of $i$. By induction, the call for $i$ reads the next $n_i$ parts of $F$, appends to $y_i$ one run $Q_i$ with these items sorted in the direction $\overline{\mathrm{dir}}$, and leaves every other work tape as it was. In particular, the later calls for $i' > i$ do not change $y_i$, and no call changes $x$. So when line L6 ends, the parts $F_{j+1}, \ldots, F_{j+n}$ have been read, each $y_i$ holds its old runs followed by $Q_i$, and every other tape is as before.

Line L7 removes $Q_i$ from each $y_i$, which restores $y_i$, and reads $Q_i$ backward, which gives its items sorted in the direction $\mathrm{dir}$. Line L8 merges these sequences in the direction $\mathrm{dir}$, so the result is sorted in that direction and holds exactly the items of $F_{j+1}, \ldots, F_{j+n}$. It appends the result to $x$. This proves 1 and 2.

For 3, the deepest sub-call is for $n_1 = \lceil n/P \rceil$, and it has $\lceil \log_P \lceil n/P \rceil \rceil$ levels by induction. The calls with smaller $n_i$ have at most as many levels, because $\lceil \log_P \cdot \rceil$ is non-decreasing. Line L8 adds one level, and $\lceil \log_P \lceil n/P \rceil \rceil + 1 = \lceil \log_P n \rceil$ for integers $n \ge 2$, because $\lceil n/P \rceil \le P^q$ exactly when $n \le P^{q+1}$. $\blacksquare$

**Theorem.** OSCILLATING-SORT returns the items of $F$ in non-decreasing order, reads $F$ once, never rewinds a tape, and makes $\lceil \log_P S \rceil$ levels of merges.

*Proof.* Line L2 calls BUILD$(S, W_1, \text{ascending})$ with all work tapes empty and nothing read. By the lemma with $j = 0$ and $n = S$, it reads $F_1, \ldots, F_S$, which is all of $F$, once and in order, and it leaves one run on $W_1$, which holds all items in non-decreasing order, and all other work tapes empty. All reads of a work tape are backward reads of its last run, and all writes are at its end, so no rewind is needed. Part 3 of the lemma gives the number of levels. $\blacksquare$
