---
title: The reversible binary GCD circuit outputs gcd(u, v) and clears its history
proves: [correctness]
status: full
---

We use the pseudocode of the page. The inputs are an odd $u$ with $0 < u < 2^n$ and $v$ with $0 \le v < 2^n$. Write $\ell(x)$ for the bit length of $x$, with $\ell(0) = 0$. The circuit permutes basis states, so it is enough to prove the claims on basis states.

**Lemma 1 (one round).** Let one round, lines L2 to L6, start with $u$ odd, $0 \le v < 2^n$ and $e_i = h_i = d = 0$, $\mathit{tmp} = 0$. Then it ends with $d = 0$, $\mathit{tmp} = 0$, $e_i = v_0$, $h_i = [v \text{ odd and } v < u]$, and new values

- $u' = u$ and $v' = v/2$ if $v$ is even;
- $u' = \min(u, v)$ and $v' = (\max(u, v) - \min(u, v))/2$ if $v$ is odd.

In both cases $u'$ is odd, $0 \le v' < 2^n$ and $\gcd(u', v') = \gcd(u, v)$.

*Proof.* Line L2 sets $e_i = v_0$. In line L3, the comparator of the adder toggles $d$ exactly when $v < u$, the Toffoli gate sets $h_i = e_i \wedge [v < u]$, and the second comparator, which sees the same $u$ and $v$, toggles $d$ back to 0. If $v$ is even, $e_i = h_i = 0$, lines L4 and L5 do nothing, and $v$ is even, so the wire rotation of line L6 gives $v/2$. If $v$ is odd, line L4 swaps exactly when $v < u$, so after it $u = \min$ and $v = \max$ of the old values. Line L5 copies $u$ into $\mathit{tmp}$ under $e_i = 1$, subtracts it from $v$, which gives $\max - \min \ge 0$, and copies again, so $\mathit{tmp} = 0$. Both values are odd, so the difference is even and line L6 halves it.

Now $u'$ is odd: it is $u$, or it is $v$ when $v$ is odd. The value $v'$ is at most $\max(u, v)/2 < 2^n$. For the GCD, $\gcd(u, v/2) = \gcd(u, v)$ when $v$ is even and $u$ is odd, because 2 does not divide $u$, and $\gcd(\min, (\max - \min)/2) = \gcd(\min, \max - \min) = \gcd(u, v)$ for the same reason. $\square$

**Lemma 2 (the round bound).** For all such inputs, $v = 0$ after at most $2n - 1$ rounds, and a round that starts with $v = 0$ changes no register except the wire labels of $v$.

*Proof.* Let $S = \ell(u) + \ell(v)$. At the start $S \le 2n$, and always $\ell(u) \ge 1$ because $u$ is odd. Take a round with $v > 0$. If $v$ is even, $\ell(v/2) = \ell(v) - 1$, so $S$ drops by 1. If $v$ is odd, $v' = (\max - \min)/2 < \max/2$, so $\ell(v') \le \ell(\max) - 1$, and $\ell(u') = \ell(\min)$, so $S' \le \ell(\min) + \ell(\max) - 1 = S - 1$. So $S$ drops by at least 1 in every round with $v > 0$. Suppose that $v > 0$ before each of the rounds $1, \dots, 2n - 1$. Then before round $2n - 1$ we have $S \le 2n - (2n - 2) = 2$, and $\ell(u) \ge 1$, $\ell(v) \ge 1$, so $u = v = 1$, and round $2n - 1$ gives $v' = 0$. Hence $v = 0$ after round $2n - 1$ at the latest.

If $v = 0$, then $v_0 = 0$, so $e_i = 0$ and $h_i = 0$, lines L4 and L5 do nothing, and the rotation of the all-zero register $v$ keeps the value 0. $\square$

**Theorem.** QGCD maps $|u\rangle|v\rangle|0\rangle$ to $|u\rangle|v\rangle|\gcd(u, v)\rangle$ and returns $\mathit{tmp}$, $d$, the carry qubit and all history qubits to 0.

*Proof.* By Lemma 1, after lines L1 to L6 the register $u$ holds a value whose GCD with the final $v$ equals $\gcd(u, v)$, and by Lemma 2 the final $v$ is 0, so $u$ holds $\gcd(u_0, v_0)$; also $\mathit{tmp} = d = 0$ and the carry qubit is 0 by the adder's specification. Line L7 XORs this value into $g = 0$ with CNOT gates that do not change $u$. Line L8 is the inverse of the forward circuit, which touches no qubit of $g$; so applying it to the state after line L7 gives back the input values of $u$, $v$ and all ancillas, which were $u_0$, $v_0$ and 0, while $g$ keeps $\gcd(u_0, v_0)$. $\blacksquare$

**Corollary.** For any amplitudes $\alpha_{u,v}$, the circuit maps $\sum \alpha_{u,v} |u\rangle|v\rangle|0\rangle|0\rangle$ to $\sum \alpha_{u,v} |u\rangle|v\rangle|\gcd(u, v)\rangle|0\rangle$, with the ancillas in $|0\rangle$ and not entangled with the inputs.

**Tightness of the bound.** For $n \ge 2$, $u = 2^{n-1} + 1$ and $v = 2^{n-1}$ need $2n - 1$ rounds: $n - 1$ halvings bring $v$ to 1, one round gives $u = 1$ and $v = 2^{n-2}$, and $n - 2$ halvings and one last subtraction bring $v$ to 0.
