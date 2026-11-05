---
title: KR-SET outputs exactly the occurrences of the patterns
proves: [correctness, termination]
status: full
---

**Claim.** For every text $T[0 \ldots n-1]$, every list of patterns $P_0, \ldots, P_{k-1}$ and every value of $r$ drawn at line L1, KR-SET stops and outputs each pair $(s, j)$ with $0 \le s \le n - |P_j|$ and $T[s \ldots s + |P_j| - 1] = P_j$ exactly once, and outputs no other pair.

**Notation.** For a string $x$ of length $\ell$, $h(x) = \sum_{i=0}^{\ell-1} c(x_i)\, r^{\ell-1-i} \bmod p$, with values in $\{0, \ldots, p-1\}$. In the pass for a length $\ell \ge 1$ with $\ell \le n$, write $W_s = T[s \ldots s + \ell - 1]$ and $t_s = h(W_s)$ for $0 \le s \le n - \ell$. For a distinct pattern $Q$, $J(Q) = \{j : P_j = Q\}$; the sets $J(Q)$ partition $\{0, \ldots, k-1\}$.

**Lemma 1 (the table).** After line L4 in the pass for $\ell$, the lists of $H$ together contain each distinct pattern of length $\ell$ exactly once, and $Q$ is in the list $H[v]$ if and only if $|Q| = \ell$ and $v = h(Q)$.

*Proof.* Line L4 visits each distinct pattern of length $\ell$ once and appends it to the list at its own hash value, and $H$ is empty before, by line L3. $\square$

**Lemma 2 (rolling).** For $0 \le s < n - \ell$, $\big((t_s - c(T[s])\, r^{\ell-1})\, r + c(T[s+\ell])\big) \bmod p = t_{s+1}$.

*Proof.* Modulo $p$,
$$\Big(t_s - c(T[s])\, r^{\ell-1}\Big) r + c(T[s+\ell]) \equiv \sum_{i=1}^{\ell-1} c(T[s+i])\, r^{\ell-i} + c(T[s+\ell]) = \sum_{i=0}^{\ell-1} c(T[s+1+i])\, r^{\ell-1-i},$$
which is $h(W_{s+1})$ before reduction. The final reduction gives the representative in $\{0, \ldots, p-1\}$, which is $t_{s+1}$. $\square$

**Lemma 3 (invariant).** In the pass for $\ell$ with $1 \le \ell \le n$, each time line L9 runs for the shift $s$, $ht = t_s$.

*Proof.* By induction on $s$. For $s = 0$, line L7 sets $ht = h(T[0 \ldots \ell-1]) = t_0$. If $ht = t_s$ at line L9 and $s < n - \ell$, then lines L9 and L10 do not change $ht$, and line L11 sets $ht$ to the left side of Lemma 2 with $R = r^{\ell-1} \bmod p$, so $ht = t_{s+1}$ when line L9 runs for $s + 1$. $\square$

**Lemma 4 (the pass for one length).** The pass for a length $\ell$ outputs each pair $(s, j)$ with $|P_j| = \ell$ and $P_j$ occurring at $s$ exactly once, and no other pair.

*Proof.* *Case $\ell = 0$.* Line L5 outputs $(s, j)$ for every $s$ in $0 \ldots n$ and every $j$ with $P_j = \varepsilon$, once each, and the pass ends. The empty pattern occurs at exactly these $s$.

*Case $\ell > n$.* No pattern of length $\ell$ fits in the text, so it has no occurrence, and line L6 ends the pass with no output.

*Case $1 \le \ell \le n$.* Each $s$ in $0 \ldots n - \ell$ is visited once by line L8. Fix $s$. By Lemma 3, line L9 goes through the list $H[t_s]$, which by Lemma 1 holds each distinct pattern $Q$ of length $\ell$ with $h(Q) = t_s$ once. Line L10 outputs $(s, j)$ for $j \in J(Q)$ exactly when $W_s = Q$.

- *Every occurrence is output.* If $P_j$ occurs at $s$, let $Q = P_j$. Then $W_s = Q$, so $h(Q) = t_s$, so $Q$ is in $H[t_s]$, the test of line L10 succeeds, and $(s, j)$ is output since $j \in J(Q)$.
- *Only occurrences are output.* A pair $(s, j)$ is output only with some $Q$ in $H[t_s]$ such that $W_s = Q$ and $j \in J(Q)$, so $P_j = Q = W_s$.
- *No pair twice.* For fixed $s$, the pair $(s, j)$ can come only from $Q = P_j$, which is in the list once, and $j$ appears once in $J(Q)$. $\square$

**Theorem.** The claim holds.

*Proof.* *Termination.* Line L2 runs over finitely many lengths. In each pass, line L4 visits finitely many patterns, line L5 outputs a finite set, and lines L8 to L11 run $n - \ell + 1$ times with finite lists at line L9. So the algorithm stops.

*Output.* Each pattern index $j$ belongs to the pass for $\ell = |P_j|$, and only that pass outputs pairs with index $j$, because line L5 and line L10 output only indices of patterns of the current length. By Lemma 4, that pass outputs each occurrence $(s, j)$ once and no non-occurrence. The value of $r$ is not used in this argument, so the output is the same for every base. $\blacksquare$

**Remark (the error of the Monte Carlo variant).** Without the comparison at line L10, the pass outputs $(s, j)$ for every $Q \in H[t_s]$. A false pair needs a distinct pattern $Q \ne W_s$ of length $\ell$ with $h(Q) = h(W_s)$. If $T$ and the patterns do not depend on $r$ and $p$ is prime, the difference $h(Q) - h(W_s)$ is a nonzero polynomial in $r$ of degree at most $\ell - 1$ over $\mathbb{F}_p$, because the codes are below $p$. It has at most $\ell - 1$ roots, so this event has probability at most $(\ell - 1)/p$. The union bound over the at most $n$ windows and the distinct patterns of each length gives a total probability of at most $n \sum_j (|P_j| - 1)^+ / p \le n m / p$.
