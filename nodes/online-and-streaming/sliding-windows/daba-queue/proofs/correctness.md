---
title: DABA keeps its invariants and returns the aggregate of the window
proves: [correctness]
status: full
---

The proof follows the structure of Lemma 8 and Theorem 9 of Tangwongsan, Hirzel and Schneider, with every case written out. Let $(M, \otimes, 1)$ be a monoid. Slot $i$ of the deque holds $\mathit{val}(i) = v_i$, and the values never change while a slot is in the window. For positions $i \le j$ write $\Pi(i..j) = v_i \otimes \cdots \otimes v_{j-1}$, with $\Pi(i..i) = 1$. By associativity, $\Pi(i..k) = \Pi(i..j) \otimes \Pi(j..k)$ for $i \le j \le k$.

**The invariants.** A state with positions $F, L, R, A, B, E$ satisfies

- (O) $F \le L \le R \le A \le B \le E$, and the window is $v_F, \ldots, v_{E-1}$;
- (G) $\mathit{agg}(i) = \Pi(i..B)$ for $i \in [F, L)$; $\mathit{agg}(i) = \Pi(i..R)$ for $i \in [L, R)$; $\mathit{agg}(i) = \Pi(R..i+1)$ for $i \in [R, A)$; $\mathit{agg}(i) = \Pi(i..B)$ for $i \in [A, B)$; $\mathit{agg}(i) = \Pi(B..i+1)$ for $i \in [B, E)$;
- (S) either $F = B = E$, or $L - F = E - B + 1$ and $R - L = A - R$.

The empty structure has all six positions equal, so it satisfies (O), (G) with every range empty, and (S).

**Lemma 1 (helpers).** Under (O) and (G), each helper returns the aggregate of its sublist: $\Pi_L = \Pi(L..R)$, $\Pi_R = \Pi(R..A)$, $\Pi_A = \Pi(A..B)$, $\Pi_B = \Pi(B..E)$, and $\Pi_F = \Pi(F..B)$ whenever $F < L$ or $F = B$.

*Proof.* Each helper returns $1$ for an empty sublist, which is the empty product. If $L < R$, $\Pi_L = \mathit{agg}(L) = \Pi(L..R)$ by (G). If $R < A$, $\Pi_R = \mathit{agg}(A-1) = \Pi(R..A)$. If $A < B$, $\Pi_A = \mathit{agg}(A) = \Pi(A..B)$. If $B < E$, $\Pi_B = \mathit{agg}(E-1) = \Pi(B..E)$. If $F < L$ then $F < B$ and $\Pi_F = \mathit{agg}(F) = \Pi(F..B)$. If $F = B$ then $\Pi_F = 1 = \Pi(F..B)$. $\square$

**The precondition of FIXUP.** Call a state *ready* when (O) and (G) hold, and either (P1) $F = B$ and $E - B \le 1$, or (P2) $F < B$, $L - F = E - B$ and $R - L = A - R$.

**Lemma 2.** If a state satisfies (O), (G) and (S), then the state after line L2 of INSERT, or after line L4 of EVICT on a non-empty window, is ready.

*Proof.* INSERT$(v)$. Line L2 writes slot $E$ with $\mathit{val} = v_E = v$ and $\mathit{agg} = \Pi_B \otimes v = \Pi(B..E) \otimes v_E = \Pi(B..E+1)$ by Lemma 1, then sets $E' = E + 1$. This is the (G) condition for slot $E$ in $[B, E')$, and no other slot changes, so (O) and (G) hold. If the old state had $F = B = E$, then now $F = B$ and $E' - B = 1$, which is (P1). Otherwise $L - F = E - B + 1 = E' - B$ and $R - L = A - R$, and $F < L \le B$ gives $F < B$, which is (P2).

EVICT. The window is not empty, so by (S) the old state has $L - F = E - B + 1 \ge 1$, so slot $F$ is in $[F, L)$. Line L4 removes it and sets $F' = F + 1 \le L$. (O) holds, and (G) holds because each remaining slot keeps its value and its range. If $F' = B$, then $L = B$ (from $F' \le L \le B$), so $E - B = L - F - 1 = 0$, which is (P1). Otherwise $F' < B$, $L - F' = E - B$ and $R - L = A - R$, which is (P2). $\square$

**Lemma 3.** FIXUP maps a ready state to a state that satisfies (O), (G) and (S), and does not change the window.

*Proof.* FIXUP moves positions and writes $\mathit{agg}$ fields; it never adds or removes a slot, so the window does not change. Cases follow the code.

*Singleton, lines L6 and L7, so $F = B$.* By readiness this is (P1), so $E - B \le 1$. If $E = B$ the window is empty and line L7 makes all six positions equal to $E = F$, so (S) holds by its first case, and (G) holds with all ranges empty. If $E = B + 1$, the window is the single slot $F = B$, which was in $[B, E)$ with $\mathit{agg}(F) = \Pi(B..B+1) = v_F$. Line L7 sets $L = R = A = B = E = F + 1$. Now slot $F$ is in $[F, L)$ and needs $\mathit{agg}(F) = \Pi(F..B) = \Pi(F..F+1) = v_F$, which holds. All other ranges are empty. (S): $L - F = 1 = E - B + 1$ and $R - L = 0 = A - R$.

From here on $F \ne B$, so the state is (P2): $F < B$, $L - F = E - B$, $R - L = A - R$.

*Flip, lines L8 and L9, so $L = B$.* By (O), $L = R = A = B$; call this position $b$. Then $b - F = L - F = E - b$, and $b - F \ge 1$ since $F < B$. Line L9 sets $L' = F$, $A' = E$, $B' = E$, and $R$ stays $b$. Check (G) for the new ranges. $[F, L')$ is empty. $[L', R) = [F, b)$ was $[F, L)$, where $\mathit{agg}(i) = \Pi(i..B) = \Pi(i..b) = \Pi(i..R)$, as $l_L$ requires. $[R, A') = [b, E)$ was $[B, E)$, where $\mathit{agg}(i) = \Pi(B..i+1) = \Pi(R..i+1)$, as $l_R$ requires. $[A', B')$ and $[B', E)$ are empty. (O) holds: $F \le F \le b \le E \le E \le E$. And $L' - F = 0 = E - B'$ and $R - L' = b - F = E - b = A' - R$. So the state is again (P2), now with $L' < R$ since $b - F \ge 1$. Then the test of line L10 fails and the shrink case runs. So it is enough to prove the shift and shrink cases for a (P2) state where (O) and (G) hold.

*Shift, lines L10 and L11, so $L = R$.* Then $A - R = R - L = 0$, so $L = R = A$. Also $L < B$: if line L8 found $L = B$, the flip left $L < R$ and this case does not run; if not, $L \ne B$ and $L \le B$. So slot $A$ exists in $[A, B)$ with $\mathit{agg}(A) = \Pi(A..B)$. Line L11 sets $L' = R' = A' = A + 1 \le B$. Slot $A$ is now in $[F, L')$, where it needs $\Pi(A..B)$, which it has. $[L', R')$ and $[R', A')$ are empty, and $[A', B)$ lost its first slot, keeping the same condition on the rest. (S): $L' - F = L - F + 1 = E - B + 1$, and $R' - L' = 0 = A' - R'$.

*Shrink, lines L12 to L15, so $L < R$.* Then $A - R = R - L \ge 1$, so $L < R < A$. By Lemma 1, line L12 computes $\Pi(L..R) \otimes \Pi(R..A) \otimes \Pi(A..B) = \Pi(L..B)$ and stores it in slot $L$; the value $\Pi_A$ used here is $\mathit{agg}(A)$ or $1$, and slot $A$ is not slot $L$. Line L13 sets $L' = L + 1 \le R$. Slot $L$ is now in $[F, L')$ and needs $\Pi(L..B)$, which it has. The slots of $[L', R)$ keep $\Pi(i..R)$. Line L14 reads $\Pi_A = \Pi(A..B)$ again, which line L12 did not change because slot $L \ne A$, and stores $v_{A-1} \otimes \Pi(A..B) = \Pi(A-1..B)$ in slot $A - 1$. Slot $A - 1 \ge R$ is not slot $L$. Line L15 sets $A' = A - 1 \ge R$. Slot $A - 1$ is now in $[A', B)$ and needs $\Pi(A-1..B)$, which it has. The slots of $[R, A')$ keep $\Pi(R..i+1)$, and $[A, B)$ and $[B, E)$ do not change. (O): $F \le L' \le R \le A' \le B$. (S): $L' - F = L - F + 1 = E - B + 1$, and $R - L' = R - L - 1 = A - R - 1 = A' - R$. $\square$

**Theorem.** In every reachable state, (O), (G) and (S) hold, EVICT returns the oldest item, and QUERY returns $v_F \otimes \cdots \otimes v_{E-1}$, the aggregate of the window from the oldest to the newest item.

*Proof.* The empty structure satisfies the invariants. QUERY changes nothing. By Lemmas 2 and 3, INSERT and EVICT map a state with the invariants to a state with the invariants for the new window, so by induction on the number of operations all reachable states have them. EVICT removes slot $F$, which by (O) holds the oldest item. For QUERY: if the window is empty, $F = B = E$ and line L1 returns $1 \otimes 1 = 1$. If not, (S) gives $L - F \ge 1$, so by Lemma 1 $\Pi_F = \Pi(F..B)$ and $\Pi_B = \Pi(B..E)$, and line L1 returns $\Pi(F..B) \otimes \Pi(B..E) = \Pi(F..E)$. The proof uses only associativity and the identity law. $\blacksquare$
