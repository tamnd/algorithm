---
title: The greedy longest copy at each position builds the target with the fewest moves
proves: [correctness]
status: full
---

We use the pseudocode of the page. The source is $S$ with $|S| = m$ and the target is $T$ with $|T| = n$, indexed from 0. A *move* is a copy $(p, \ell)$ with $\ell \ge 1$, which appends $S[p \ldots p + \ell - 1]$, or an add of one symbol. A *cover* of $T$ is a list of moves whose outputs, joined in order, give $T$. Each move of a cover produces a segment $T[q \ldots r - 1]$ of $T$; we say that it goes *from $q$ to $r$*. The cost of a cover is its number of moves.

For a position $q < n$, let $L(q)$ be the length of the longest prefix of $T[q \ldots n - 1]$ that occurs in $S$ as a substring, and let $G(q) = q + \max(1, L(q))$.

**Lemma 1 (closure).** If $T[q \ldots r - 1]$ occurs in $S$, then every substring $T[q' \ldots r' - 1]$ with $q \le q' < r' \le r$ occurs in $S$.

*Proof.* If $T[q \ldots r - 1] = S[p \ldots p + r - q - 1]$, then $T[q' \ldots r' - 1] = S[p + q' - q \ldots p + r' - q - 1]$. $\square$

**Lemma 2 (the greedy step).** Lines L3 to L6, run at position $q$, append one move from $q$ to $G(q)$. Every move of any cover that starts at $q$ ends at most at $G(q)$.

*Proof.* Line L3 computes, for each start $p$ in $S$, the length of the longest common prefix of $S[p \ldots m - 1]$ and $T[q \ldots n - 1]$, and line L4 keeps the largest. A prefix of $T[q \ldots]$ occurs in $S$ exactly when it is a common prefix of $T[q \ldots]$ and some $S[p \ldots]$, so the largest value is $L(q)$. If $L(q) = 0$, the symbol $T[q]$ does not occur in $S$, and line L5 appends an add from $q$ to $q + 1 = G(q)$. Otherwise line L6 appends the copy $(p, L(q))$ with $S[p \ldots p + L(q) - 1] = T[q \ldots q + L(q) - 1]$, from $q$ to $G(q)$. For the second claim: an add from $q$ ends at $q + 1 \le G(q)$, and a copy from $q$ to $r$ produces $T[q \ldots r - 1]$ as a substring of $S$, so $r - q \le L(q)$ and $r \le G(q)$. $\square$

**Lemma 3 (monotone).** If $q \le q' < n$, then $G(q) \le G(q')$.

*Proof.* If $q' \ge G(q)$, then $G(q') > q' \ge G(q)$. Otherwise $q \le q' < G(q)$. If $L(q) = 0$, then $G(q) = q + 1$ and $q' = q$. If $L(q) \ge 1$, then $T[q \ldots G(q) - 1]$ occurs in $S$, so by Lemma 1 the prefix $T[q' \ldots G(q) - 1]$ of $T[q' \ldots]$ occurs in $S$, and $q' + L(q') \ge G(q)$. $\square$

**Theorem 1 (valid).** The moves returned at line L7 build $T$ from $S$.

*Proof.* The loop of line L2 keeps the invariant that the moves so far build $T[0 \ldots q - 1]$. It holds at $q = 0$ by line L1. By Lemma 2, one round appends a move that produces $T[q \ldots G(q) - 1]$ and sets $q$ to $G(q)$, so the invariant holds again. Since $G(q) > q$, the loop ends, at $q = n$, and the moves build $T$. $\square$

**Theorem 2 (fewest moves).** No cover of $T$ has fewer moves than the greedy cover.

*Proof.* The method of [greedy stays ahead](/greedy-stays-ahead/). Let a cover have $k$ moves, ending at $r_1 < r_2 < \ldots < r_k = n$, and let the greedy moves end at $g_1 < g_2 < \ldots$. We show $g_i \ge r_i$ for each $i \le k$ for which the greedy cover still has an $i$-th move, by induction on $i$. For $i = 1$, both first moves start at 0, so $r_1 \le G(0) = g_1$ by Lemma 2. Assume $g_i \ge r_i$ and $g_i < n$. The $(i + 1)$-th move of the cover goes from $r_i$ to $r_{i + 1}$, so by Lemmas 2 and 3, $r_{i + 1} \le G(r_i) \le G(g_i) = g_{i + 1}$. So the greedy cover reaches $n$ no later than its $k$-th move: it has at most $k$ moves. $\square$

**Adds are forced.** By Lemma 2, line L5 adds a symbol only when it does not occur in $S$. Every cover must produce such a symbol with an add, so the greedy cover has the least possible number of adds, and by Theorem 2 also the least number of moves in total, which is the least number of copies plus the forced adds.

**The linear version.** The [suffix automaton](/suffix-automaton/) of $S$ accepts exactly the substrings of $S$ when every state is accepting, so walking it along $T[q \ldots]$ until a transition is missing reads exactly $L(q)$ symbols. All the strings that reach one state have the same set of end positions in $S$, and the first end position of the state where the walk stops gives the start of the first occurrence of $T[q \ldots q + L(q) - 1]$. So the linear version appends the same moves as lines L3 to L6, and the theorems apply to it.

**Cost.** In the direct version, line L3 at position $q$ compares at most $L(q) + 1$ pairs for each of the $m$ starts, so one round costs $O(m (L(q) + 1))$. The rounds advance $q$ by $\max(1, L(q))$, which sums to $n$, so the total is $O(m n)$. In the linear version, the automaton has $O(m)$ states and is built in $O(m)$ expected time with hash tables for the transitions, and each round reads $L(q)$ symbols plus one failed lookup, $O(n)$ in total.
