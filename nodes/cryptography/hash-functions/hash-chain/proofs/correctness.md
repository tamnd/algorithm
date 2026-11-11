---
title: A hash chain verifier accepts each honest value once, and a forgery inverts the step function
proves: [correctness]
status: full
---

We use the notation of the page: $x_i = f^i(s)$ for $0 \le i \le n$, the verifier holds $v$, and the prover stores checkpoints $x_c$ for the multiples $c$ of $t$ with $c \le n$.

**Lemma 1 (checkpoints).** For $0 \le i \le n$ and $c = t \lfloor i / t \rfloor$, $f^{i-c}(x_c) = x_i$, and the computation takes $i - c = i \bmod t \le t - 1$ calls.

*Proof.* $c \le i$ and $c$ is a multiple of $t$ with $c \le n$, so $x_c$ is stored. Then $f^{i-c}(x_c) = f^{i-c}(f^c(s)) = f^i(s) = x_i$. $\square$

**Lemma 2 (verifier invariant).** If the verifier starts with $v = x_n$ and accepts exactly the honest values in order, then after $u$ acceptances $v = x_{n-u}$.

*Proof.* Induction on $u$. For $u = 0$ it holds by line L3. Before the $(u+1)$-th login $v = x_{n-u}$, and by Lemma 1 the prover sends $x_{n-u-1}$. Since $f(x_{n-u-1}) = x_{n-u} = v$, line L5 accepts and sets $v = x_{n-u-1}$. $\square$

**Theorem 1 (completeness).** The honest prover is accepted $n$ times, once for each of $x_{n-1}, \ldots, x_0$. $\blacksquare$

**Lemma 3 (no replay).** A value accepted once is rejected later, unless $f$ has a fixed point or a short cycle on the chain.

*Proof.* After $x_j$ is accepted, $v = x_j$. Sending $x_j$ again is accepted only if $f(x_j) = x_j$. Sending an older value $x_k$ with $k > j$ is accepted only if $f(x_k) = x_j$, that is $x_{k+1} = x_j$ with $k + 1 > j$, so the chain has a cycle of length $k + 1 - j$. For a random function with $m$-bit outputs, the chance that a chain of length $n$ meets a value twice is at most about $n^2 / 2^{m+1}$ by the birthday bound. $\square$

**Theorem 2 (soundness by reduction).** Let $A$ be an adversary that sees the anchor and the values $x_{n-1}, \ldots, x_j$ and then makes the verifier accept a value at state $v = x_j$ with probability $\varepsilon$. Then there is an algorithm $B$ that, given $x_j$, finds a preimage of $x_j$ under $f$ with probability $\varepsilon$ and about the same running time plus $n$ calls to $f$.

*Proof.* $B$ gets $x_j$. It computes $x_{j+1}, \ldots, x_n$ by applying $f$, gives them to $A$ as the anchor and the used values, and runs $A$. If the verifier accepts $y$, then $f(y) = x_j$, so $y$ is a preimage. The view of $A$ is exactly the real one, because all values it sees are functions of $x_j$. $\blacksquare$

**The distribution of $x_j$.** Theorem 2 needs $f$ to be hard to invert at $x_j = f^j(s)$, which is not a uniform image of $f$.

- If $f$ is a permutation and $s$ is uniform, $x_j$ is uniform, and it equals $f(x_{j-1})$ with $x_{j-1}$ uniform. So preimage resistance of $f$ in the usual sense applies. If the adversary may choose which login to attack, $B$ guesses $j$ and loses a factor $n$.
- If $f$ is a random function with $m$-bit outputs, the preimages of $x_j$ are fixed only by the oracle. An adversary with $q$ oracle queries that are not on the chain finds a new preimage with probability at most $q / 2^m$, and the honest preimage $x_{j-1}$ is hidden because $A$ never sees it. Iterating a random function shrinks its image, so $x_j$ is in a set of about $2^{m+1} / j$ values for large $j$, but this does not help to find a preimage of a given value. The bound is tight up to constants.
- For a general one-way function the iterate $f^j$ need not be one way, so no standard model statement follows without more assumptions.

**Small count attack.** An adversary who learns $x_k$ for any $k$ gets $x_i$ for all $i \ge k$ by applying $f$. So it is accepted at every state $v = x_j$ with $j > k$. This is why a client must never answer a challenge with a count lower than it expects.
