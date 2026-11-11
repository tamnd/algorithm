---
title: Trivium decrypts correctly, and its state update is a bijection
proves: [correctness]
status: full
---

Write $s = (s_1, \ldots, s_{288}) \in \mathrm{GF}(2)^{288}$ for the state and $F$ for the map of lines L7 to L12 of the page: $F(s) = s'$ with

$$s'_1 = s_{243} + s_{288} + s_{286} s_{287} + s_{69}, \qquad s'_i = s_{i-1} \ (2 \le i \le 93),$$

$$s'_{94} = s_{66} + s_{93} + s_{91} s_{92} + s_{171}, \qquad s'_i = s_{i-1} \ (95 \le i \le 177),$$

$$s'_{178} = s_{162} + s_{177} + s_{175} s_{176} + s_{264}, \qquad s'_i = s_{i-1} \ (179 \le i \le 288).$$

Let $g(s) = s_{66} + s_{93} + s_{162} + s_{177} + s_{243} + s_{288}$ be the output of lines L5 and L6.

**Lemma 1 (determinism).** The keystream $z_1, \ldots, z_n$ is a function of $(K, IV, n)$ only.

*Proof.* Lines L1 to L3 set $s^{(0)}$ from $K$ and $IV$ and fixed constants. Line L4 sets $s^{(i)} = F(s^{(i-1)})$, and line L6 outputs $z_{i-1152} = g(s^{(i-1)})$ for $i > 1152$. Both $F$ and $g$ are fixed Boolean maps. By induction on $i$, each $s^{(i)}$ and each $z_j$ is a function of $s^{(0)}$, so of $(K, IV)$. $\square$

**Theorem 1 (correctness).** For every key $K$, IV and message $m$ of $n$ bits, decryption of $c = m \oplus z$ under $(K, IV)$ returns $m$.

*Proof.* By Lemma 1 the receiver computes the same $z$. For each bit, $(m_j + z_j) + z_j = m_j + (z_j + z_j) = m_j$, because $z_j + z_j = 0$ in GF(2). $\blacksquare$

**Theorem 2 ($F$ is a bijection).** $F$ is a permutation of $\mathrm{GF}(2)^{288}$.

*Proof.* $F$ maps a finite set to itself, so it suffices to show that $s$ is a function of $s' = F(s)$. The shifts give $s_{i-1} = s'_i$ for $2 \le i \le 93$, $95 \le i \le 177$ and $179 \le i \le 288$. This recovers every cell of $s$ except the three last cells $s_{93}$, $s_{177}$ and $s_{288}$, which leave the registers. Each of them appears linearly, once, in one feedback equation, and the other terms of that equation are cells already recovered:

- From $s'_{94}$: $s_{93} = s'_{94} + s_{66} + s_{91} s_{92} + s_{171} = s'_{94} + s'_{67} + s'_{92} s'_{93} + s'_{172}$.
- From $s'_{178}$: $s_{177} = s'_{178} + s_{162} + s_{175} s_{176} + s_{264} = s'_{178} + s'_{163} + s'_{176} s'_{177} + s'_{265}$.
- From $s'_1$: $s_{288} = s'_1 + s_{243} + s_{286} s_{287} + s_{69} = s'_1 + s'_{244} + s'_{287} s'_{288} + s'_{70}$.

So $F$ has an inverse and is a bijection. $\blacksquare$

**Corollary.** For a fixed key, the map from the 1152-step state to the initial state is one-to-one, so two different IVs give different states after line L4 finishes the warm-up. Also, the sequence $s^{(0)}, s^{(1)}, \ldots$ is purely periodic: it returns to $s^{(0)}$ and has no pre-period, because a bijection on a finite set splits it into disjoint cycles. The length of the cycle is not known, and the proof gives no lower bound on it.

These results are functional properties only. The security of Trivium (no attack on the full 1152 rounds faster than exhaustive search over the 80-bit key) is a claim of the designers that rests on public analysis, not on a proof.
