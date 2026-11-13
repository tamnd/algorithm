---
title: The reversible extended binary GCD outputs x^-1 mod N and clears its ancillas
proves: [correctness]
status: full
---

We use the pseudocode of the page. $N \ge 3$ is odd with bit length $n$, and $0 \le x < N$. All congruences are modulo $N$. The circuit permutes basis states, so it is enough to prove the claims on basis states.

**Lemma 1 (the parts).** On registers of $n + 1$ qubits:

1. For $0 \le a, b < N$, the modular adder maps $b$ to $(b + a) \bmod N$, keeps $a$ and returns its flag $f$ to 0. Its inverse maps $b$ to $(b - a) \bmod N$.
2. For $0 \le b < N$, line L7 maps $b$ to $b \cdot 2^{-1} \bmod N$ and returns $p$, the constant register and the carry qubit to 0.

*Proof.* Part 1 is Lemma 1 of the proof on the [quantum modular exponentiation](/quantum-modular-exponentiation/) page with the constant replaced by the register $a$; the argument uses only $0 \le a < N$. Since the map $b \mapsto (b + a) \bmod N$ is a bijection of $\{0, \dots, N - 1\}$, the inverse circuit computes its inverse on that range.

For part 2, let $q = b \bmod 2$. The first CNOT sets $p = q$. Adding $qN$ gives $b + qN$, which is even (as $N$ is odd) and at most $2N - 2 < 2^{n+1}$. Relabeling the wires divides by 2 because the low bit is 0, so $b' = (b + qN)/2$. Then $2 b' \equiv b$, so $b' \equiv b \cdot 2^{-1}$, and $0 \le b' < N$. If $q = 0$, then $b' = b/2 \le (N - 1)/2$; if $q = 1$, then $b' = (b + N)/2 \ge (N + 1)/2$. So $q = [b' \ge (N + 1)/2]$. The last step negates $p$ and toggles it when $b' < (N + 1)/2$, which gives $p = 1 \oplus q \oplus (1 \oplus q) = 0$. $\square$

**Lemma 2 (invariants).** Before and after every round, $A x \equiv u$, $B x \equiv v$, $0 \le A, B < N$, $u$ is odd, $0 \le v < 2^n$, and $\gcd(u, v) = \gcd(N, x)$. The work registers, the constant register, the carry qubit and the flags $d$, $f$, $p$ are 0 between rounds.

*Proof.* At the start $(u, v, A, B) = (N, x, 0, 1)$, so $A x = 0 \equiv N$ and $B x = x$; $N$ is odd and $x < N < 2^n$. For the registers $u$ and $v$ and the bits $e_i$, $h_i$, a round acts exactly as a round of the [quantum GCD](/quantum-gcd/) circuit, so the facts on $u$ and $v$ hold by Lemma 1 of that proof. Line L4 swaps $(u, A)$ with $(v, B)$, which swaps the two congruences. Line L5, when $e_i = 1$, gives $v - u$ and $(B - A) \bmod N$ by Lemma 1, and $(B - A)x \equiv v - u$; the copy of $A$ is made and removed with the same Toffoli gates, so the work register returns to 0. Lines L6 and L7 halve $v$ (which is even) and replace $B$ by $B \cdot 2^{-1}$, and $(B \cdot 2^{-1}) x \equiv v \cdot 2^{-1} \equiv v/2$, since $2 \cdot (v/2) = v$. $\square$

**Theorem.** For $0 \le x < N$, QINV maps $|x\rangle|0\rangle$ with all ancillas 0 to $|x\rangle|A\rangle$ with all ancillas 0, where $0 \le A < N$ and $A x \equiv \gcd(x, N)$. In particular $A = x^{-1} \bmod N$ when $\gcd(x, N) = 1$.

*Proof.* By Lemma 2 of the quantum GCD proof, $v = 0$ after the $2n - 1$ rounds, so by Lemma 2 here $u = \gcd(u, 0) = \gcd(N, x)$ and $A x \equiv u$. If $\gcd(x, N) = 1$, then $A x \equiv 1$ with $0 \le A < N$, so $A$ is the inverse. Line L8 XORs the low $n$ bits of $A$ into the output register, which holds 0; the top bit of $A$ is 0 since $A < N < 2^n$. Line L9 applies the inverse of lines L2 to L7, which touch no qubit of the output register, so it restores $(u, v, A, B) = (N, x, 0, 1)$ with all history qubits 0. Undoing line L1 then clears $u$ and $B$. $\blacksquare$

**Corollary.** For any amplitudes $\alpha_x$ over units $x$, the circuit maps $\sum_x \alpha_x |x\rangle|0\rangle$ to $\sum_x \alpha_x |x\rangle|x^{-1} \bmod N\rangle$, with every ancilla in $|0\rangle$ and not entangled with $x$.
