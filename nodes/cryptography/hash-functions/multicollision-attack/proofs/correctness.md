---
title: The 2^t messages of a Joux multicollision are distinct and have the same digest
proves: [correctness]
status: full
---

Let $f : \{0,1\}^n \times \{0,1\}^b \to \{0,1\}^n$ be a compression function, and let $H$ be the Merkle-Damgård hash with initial value $IV$: for a message $M = M_1 \cdots M_\ell$ of $\ell$ blocks, $H(M) = f(f^\ast(IV, M), \mathrm{len}(\ell))$, where $f^\ast(h, \varepsilon) = h$ and $f^\ast(h, M_1 \cdots M_i) = f(f^\ast(h, M_1 \cdots M_{i-1}), M_i)$, and $\mathrm{len}(\ell)$ is the length block. Padding inside the last block is folded into $\mathrm{len}$ here, since all messages below have the same length.

Let $P = [(B_1, B'_1), \ldots, (B_t, B'_t)]$ be the output of JOUX-MULTICOLLISION, and let $h_0 = IV$ and $h_i$ be the value of $h$ after round $i$ of line L2.

**Lemma 1 (each round).** For $i = 1, \ldots, t$: $B_i \ne B'_i$, and $f(h_{i-1}, B_i) = f(h_{i-1}, B'_i) = h_i$.

*Proof.* At the start of round $i$, $h = h_{i-1}$. Line L3 finds $B \ne B'$ with $f(h_{i-1}, B) = f(h_{i-1}, B')$, and sets $h_i = f(h_{i-1}, B)$. A birthday attack on the map $B \mapsto f(h_{i-1}, B)$ returns such a pair, as shown on the page of the [birthday attack](/birthday-attack/), whenever the block space has more than $2^n$ elements, or in general with the probability given there. $\square$

**Lemma 2 (all paths meet).** For $0 \le i \le t$ and each choice $C_j \in \{B_j, B'_j\}$ for $j \le i$, $f^\ast(IV, C_1 \cdots C_i) = h_i$.

*Proof.* By induction on $i$. For $i = 0$, the message is empty and $f^\ast(IV, \varepsilon) = IV = h_0$. For $i \ge 1$, by the induction hypothesis $f^\ast(IV, C_1 \cdots C_{i-1}) = h_{i-1}$, so $f^\ast(IV, C_1 \cdots C_i) = f(h_{i-1}, C_i) = h_i$ by Lemma 1, for either choice of $C_i$. $\square$

**Theorem.** The $2^t$ messages $C_1 \cdots C_t$ with $C_i \in \{B_i, B'_i\}$ are pairwise distinct, and all have the digest $f(h_t, \mathrm{len}(t))$. The attack makes $t$ birthday searches on $n$-bit values, so about $t \cdot 1.25 \cdot 2^{n/2}$ calls of $f$ on average when each map $B \mapsto f(h, B)$ acts as a random function.

*Proof.* Two different choice vectors differ at some position $i$, where one message has $B_i$ and the other $B'_i \ne B_i$, so the messages differ. By Lemma 2 with $i = t$, each message reaches the chaining value $h_t$ after $t$ blocks. All have $t$ blocks, so the length block is $\mathrm{len}(t)$ for each, and the digest is $f(h_t, \mathrm{len}(t))$. The cost follows from the cost of each birthday search. $\blacksquare$

**Corollary (concatenation).** Let $H_1$ be as above with an $n_1$-bit chaining value, and $H_2$ any function. Among the $2^t$ messages of a multicollision of $H_1$, any two $M \ne M'$ with $H_2(M) = H_2(M')$ satisfy $H_1(M) \| H_2(M) = H_1(M') \| H_2(M')$. If the values $H_2(M)$ of the $2^t$ messages behave as independent and uniform $n_2$-bit values, such a pair exists with probability at least $1 - e^{-2^t(2^t - 1)/2^{n_2 + 1}}$, which is at least $1 - e^{-7.9}$ for $t = n_2/2 + 2$ and $n_2 \ge 16$.

*Proof.* The first claim follows from the theorem, since $H_1(M) = H_1(M')$. The probability is the birthday lower bound with $q = 2^t$ values in $N = 2^{n_2}$. With $t = n_2/2 + 2$, $q(q - 1)/2N \ge (16 \cdot 2^{n_2} - 4 \cdot 2^{n_2/2})/2^{n_2+1} \ge 8 - 2^{1 - n_2/2}$, which is at least 7.9 for $n_2 \ge 16$. $\blacksquare$
