---
title: Lamport signatures verify, and one key is unforgeable for one message
proves: [correctness]
status: full
---

**Setting.** $f : \{0,1\}^\ell \to \{0,1\}^\ell$ is the function that line L2 applies to the secret values, and $D$ maps a message to $n$ digest bits $D(m)_1 \ldots D(m)_n$ (lines L4 and L7). The secret key is $x_{i,b}$ for $i \in [n]$ and $b \in \{0,1\}$, and the public key is $y_{i,b} = f(x_{i,b})$.

**Lemma 1 (an honest signature verifies).** For every key pair made by lines L1 to L3 and every message $m$, VERIFY$(pk, m, \text{SIGN}(sk, m))$ returns true.

*Proof.* Let $d = D(m)$. Line L5 returns $\sigma = (x_{1,d_1}, \ldots, x_{n,d_n})$, so $\sigma$ has $n$ entries of $\ell$ bits each and line L6 does not reject. Line L7 computes the same $d$, because $D$ is a function of $m$ only. For each $i$, line L9 compares $f(\sigma_i) = f(x_{i,d_i})$ with $y_{i,d_i}$, and these are equal by line L2. So no iteration of the loop of line L8 returns false, and line L10 returns true. $\square$

**The one-time game (EUF-1-CMA).** The challenger makes a key pair and gives $pk$ to the adversary $A$. $A$ may ask for one signature, on a message $m$ of its choice, and gets $\sigma = $ SIGN$(sk, m)$. $A$ wins if it outputs $(m^*, \sigma^*)$ with $m^* \ne m$ (or any $m^*$ if it asked nothing) and VERIFY$(pk, m^*, \sigma^*)$ is true. Write $\varepsilon$ for the chance that $A$ wins.

**Theorem 2 (one-time unforgeability, standard model).** Let $A$ run in time $t$ and win with chance $\varepsilon$. Then there is an inverter $B$ for $f$ that runs in time about $t + 2n$ evaluations of $f$, and a collision finder $C$ for $D$ that runs in time about $t$, such that

$$\varepsilon \le 2n \cdot \Pr[B \text{ inverts } f] + \Pr[C \text{ finds a collision of } D].$$

*Proof.* Split the winning runs of $A$ into two events. Event $W_1$: $A$ wins and asked for a signature on some $m$ with $D(m^*) = D(m)$. Event $W_2$: $A$ wins and $D(m^*) \ne D(m)$, or $A$ asked nothing. Then $\varepsilon = \Pr[W_1] + \Pr[W_2]$.

*The collision finder.* $C$ makes a key pair itself, runs $A$, answers the one query with SIGN, and outputs $(m, m^*)$. On $W_1$, $m \ne m^*$ and $D(m) = D(m^*)$, so $C$ finds a collision with chance at least $\Pr[W_1]$.

*The inverter.* $B$ gets $Y = f(X)$ for a uniform $X \in \{0,1\}^\ell$ and must output some $X'$ with $f(X') = Y$.

1. $B$ picks a position $(i^*, b^*)$ uniformly among the $2n$ positions. It picks the other $2n - 1$ secret values uniformly and sets $y_{i,b} = f(x_{i,b})$ for them, and $y_{i^*,b^*} = Y$. Each $y_{i,b}$ is then $f$ of a uniform value, as in a real key, and $(i^*, b^*)$ is independent of $pk$.
2. When $A$ asks for a signature on $m$, $B$ needs $x_{i,D(m)_i}$ for each $i$. If $D(m)_{i^*} = b^*$, $B$ does not know the value and stops with failure. Otherwise it answers correctly.
3. When $A$ outputs $(m^*, \sigma^*)$, $B$ outputs $\sigma^*_{i^*}$.

Compare $B$ with a run $B'$ that knows all $2n$ secret values, answers every query, and also picks $(i^*, b^*)$ uniformly, independent of everything else. The view of $A$ in $B'$ is exactly the real game. Let $S$ be the set of positions $(j, D(m^*)_j)$ that were *not* revealed by the answer to the query. On $W_2$, $S$ is not empty: if $A$ asked nothing, every position of $D(m^*)$ is in $S$; if $A$ asked for $m$, there is a $j$ with $D(m^*)_j \ne D(m)_j$, and the value $x_{j, D(m^*)_j}$ was not revealed. Because $(i^*, b^*)$ is independent of the view of $A$ in $B'$, $\Pr[W_2 \text{ and } (i^*, b^*) \in S] \ge \Pr[W_2] / (2n)$.

On this event, the query (if any) did not reveal position $(i^*, b^*)$, so $B$ does not stop in step 2, and its run is the same as the run of $B'$. The verification of $\sigma^*$ succeeds, so in line L9 for $i = i^*$ we have $f(\sigma^*_{i^*}) = y_{i^*, D(m^*)_{i^*}} = y_{i^*, b^*} = Y$. So $B$ outputs a preimage of $Y$, and $\Pr[B \text{ inverts } f] \ge \Pr[W_2]/(2n)$.

Adding the two bounds gives $\varepsilon = \Pr[W_1] + \Pr[W_2] \le \Pr[C \text{ finds a collision}] + 2n \Pr[B \text{ inverts } f]$. $\blacksquare$

**Remarks.**

- The factor $2n$ is the loss of the reduction. It does not depend on the running time of $A$.
- The proof uses the one query only in step 2. With two queries on $m_1$ and $m_2$, every position where $D(m_1)$ and $D(m_2)$ differ is revealed in both halves, and the set $S$ can be empty for many $m^*$. This is the key reuse attack of the page: a random $m^*$ is covered with chance $2^{-e}$, where $e$ is the number of positions where the two digests agree.
- If $D$ is randomized by the signer (a fresh random prefix in each signature), the adversary must commit to $m$ before it sees the prefix, so the event $W_1$ needs a weaker property of the hash than full collision resistance. This is the reason why modern schemes such as LMS, XMSS and SPHINCS+ randomize the message hash.
