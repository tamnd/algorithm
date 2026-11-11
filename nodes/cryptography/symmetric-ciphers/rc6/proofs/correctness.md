---
title: RC6 decryption inverts RC6 encryption
proves: [correctness]
status: full
---

Fix $w$, $r$ and a table $S[0 \ldots 2r+3]$ of $w$-bit words. The proof holds for any table, so it does not depend on the key schedule. All arithmetic is modulo $2^w$. Write $g(x) = (x \times (2x + 1)) \lll \lg w$, so line L4 is $t \leftarrow g(B)$ and line L5 is $u \leftarrow g(D)$.

**Facts.** For fixed $k$ and $s$: $x \mapsto x + k$ has the inverse $y \mapsto y - k$; $x \mapsto x \lll s$ has the inverse $y \mapsto y \ggg s$; and $x \mapsto x \oplus k$ is its own inverse. The proof does not need $g$ to be invertible.

**One round.** Let $(A, B, C, D)$ be the state at the start of round $i$, and let $t = g(B)$ and $u = g(D)$. Lines L6 and L7 give

$$A' = ((A \oplus t) \lll u) + S[2i], \qquad C' = ((C \oplus u) \lll t) + S[2i+1],$$

and $B$ and $D$ do not change. Line L8 outputs $(B, C', D, A')$.

Given this output $(P, Q, R, T)$, the inverse step first sets $(A, B, C, D) \leftarrow (T, P, Q, R) = (A', B, C', D)$, which undoes line L8. Now $B$ and $D$ hold their values from the start of the round, so $g(B) = t$ and $g(D) = u$ are the same values that lines L6 and L7 used. Then

$$((A' - S[2i]) \ggg u) \oplus t = ((A \oplus t) \lll u) \ggg u \oplus t = A,$$

$$((C' - S[2i+1]) \ggg t) \oplus u = ((C \oplus u) \lll t) \ggg t \oplus u = C.$$

So the round is a bijection on states, and the inverse step of the page undoes it. The order of the two lines in the inverse step does not matter, because each uses only $t$ and $u$, which do not change.

**The whole cipher.** Encryption is: line L1, line L2, rounds $1, \ldots, r$, line L9, line L10. Each step is a bijection, so encryption is a bijection, and its inverse applies the inverse steps in reverse order: $C \leftarrow C - S[2r+3]$, $A \leftarrow A - S[2r+2]$, the inverse of rounds $r, \ldots, 1$, then $D \leftarrow D - S[1]$ and $B \leftarrow B - S[0]$. This is the decryption of the page. $\square$

**Termination.** The loop of line L3 runs $r$ times and the loop of line L14 runs $3 \max(c, 2r + 4)$ times, each with a fixed amount of work.

**A remark on $f(x) = x(2x + 1)$.** The paper notes that $f$ is one to one modulo $2^w$. This is not needed for correctness. It holds because $f(x) - f(y) = (x - y)(2x + 2y + 1)$, and the second factor is odd, so it is a unit modulo $2^w$; hence $f(x) = f(y)$ implies $x = y$.
