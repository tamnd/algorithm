---
title: Cuckoo hashing keeps its invariant and implements a dictionary
proves: [correctness, termination]
status: full
---

We write $P(T)$ for the set of pairs in the cells of $T_1$ and $T_2$. The invariant is (C1) each pair $(k, v) \in P(T)$ is in $T_1[h_1(k)]$ or $T_2[h_2(k)]$; (C2) no key occurs in two cells; (C3) $n = |P(T)|$; (C4) $r \ge (1 + \varepsilon) n$.

**Theorem.** Start from empty tables with $r \ge 1$ and $0 < \varepsilon \le 1$ and apply any sequence of CUCKOO-INSERT, CUCKOO-SEARCH and CUCKOO-DELETE. Each operation that ends leaves (C1) to (C4) true, and $P(T)$ equal to the map that the same sequence gives on an abstract dictionary. Each search returns the value of its key in that map, or NIL. If the hash functions of line L16 are drawn independently from a distribution under which a fixed set of at most $r / (1 + \varepsilon)$ keys can be placed with probability at least $q > 0$, then each insert ends with probability 1.

*Proof.* Empty tables satisfy (C1) to (C4) with $n = 0$, and they hold the empty map.

**Step 1 (the two cells are enough).** Assume (C1). A pair with key $k$ is in $T_1[h_1(k)]$ or $T_2[h_2(k)]$. So a test of these two cells finds every pair with key $k$, and if both tests fail, $k$ is not a key.

**Step 2 (search).** By Step 1 and (C2), lines L1 and L2 return the value of the only pair with key $k$, if there is one, and line L3 returns NIL otherwise. Search changes nothing.

**Step 3 (delete).** By Step 1 and (C2), lines L13 and L14 clear the only cell with key $k$, if there is one, and lower $n$ by 1. The other pairs do not move, so (C1) and (C2) hold, (C3) holds, and (C4) holds because $n$ decreased. The map loses exactly $k$.

**Step 4 (the eviction walk).** Consider lines L6 to L11 started with a pair $x_0$ whose key is not a key of $P(T)$, on tables that satisfy (C1) and (C2). Let $Q = P(T) \cup \{x_0\}$. We claim that before each of lines L8 and L10:

> **(W)** $x$ is a pair of $Q$, and $P(T) = Q \setminus \{x\}$. Each pair of $P(T)$ is in one of its two cells, and the keys of $Q$ are distinct.

At line L6, $x = x_0$ and $P(T) = Q \setminus \{x_0\}$, so (W) holds. Line L8 swaps $x$ with the content $c$ of $T_1[h_1(\text{key}(x))]$. After the swap, the old $x$ is in its own first cell, and the new $x$ is $c$. If $c$ is NIL, then $P(T) = Q$, each pair is in one of its cells, and line L9 adds 1 to $n$. If $c$ is a pair, it was in $P(T)$, it is now out of the tables, and $P(T) = Q \setminus \{c\}$, so (W) holds again before line L10. Line L10 is the same with $T_2$ and $h_2$. The keys of $Q$ do not change in a swap, so they stay distinct. Hence if the walk returns at line L9 or L11, then $P(T) = Q$, (C1) and (C2) hold, and $n$ has grown by 1. If it does not return after MaxLoop rounds, then by (W) the tables hold $Q \setminus \{x\}$, each pair in one of its cells.

**Step 5 (rehash).** Line L15 sets $S = P(T) \cup X$. Line L16 empties the tables and sets $n = 0$. Line L17 runs the walk for each pair of $S$ in turn. The keys of $S$ are distinct, so each walk starts with a key that is not yet in the tables, and Step 4 applies. If all walks return, then $P(T) = S$, with (C1) and (C2), and $n = |S|$ by (C3). If one walk fails, line L17 goes back to line L16 and starts again from the same $S$. So when REHASH returns, $P(T) = S$ and (C1) to (C3) hold.

**Step 6 (insert).** If line L4 finds key $k$, it replaces the value in place. No pair moves and the map is the old map with $k$ mapped to $v$. Else $k$ is not a key, by Step 1. Line L5 keeps $P(T)$ by Step 5, and after it $r \ge (1 + \varepsilon)(n + 1)$: either the test failed, or $r$ was doubled from a value $r_0 \ge (1 + \varepsilon) n$. If $n \ge 1$, then $2 r_0 \ge 2(1 + \varepsilon) n \ge (1 + \varepsilon)(n + 1)$. If $n = 0$, then $2 r_0 \ge 2 \ge 1 + \varepsilon$, because $r_0 \ge 1$ and $\varepsilon \le 1$. By Step 4 with $x_0 = (k, v)$, either the walk places all of $Q = P(T) \cup \{(k, v)\}$, or it leaves one pair $x$ outside with $P(T) = Q \setminus \{x\}$. In the second case, line L12 calls REHASH with $X = \{x\}$, and by Step 5 the result is $P(T) = Q$. In both cases $n = |Q|$ and $r \ge (1 + \varepsilon) n$, so (C1) to (C4) hold and the map is the old map plus $(k, v)$.

**Step 7 (termination).** Each walk has at most MaxLoop rounds, so it ends. REHASH repeats line L16 until one draw of $h_1, h_2$ places all of $S$. The set $S$ has at most $r / (1 + \varepsilon)$ keys by (C4), so each draw succeeds with probability at least $q$, independently of the earlier draws. The probability that the first $t$ draws all fail is at most $(1 - q)^t$, which tends to 0. So REHASH ends with probability 1, after an expected number of at most $1/q$ draws.

By induction on the number of operations, using Steps 2, 3 and 6, the theorem holds. $\blacksquare$
