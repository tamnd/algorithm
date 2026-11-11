---
title: The OR-proof designated verifier signature verifies, and the verifier can simulate it perfectly
proves: [correctness]
status: full
---

**Setting.** $G = \langle g \rangle$ has prime order $q$. The signer has $y_s = g^{x_s}$ and the designated verifier has $y_v = g^{x_v}$, with $y_s \ne y_v$. $H$ maps $(y_s, y_v, m, t_s, t_v)$ into $\mathbb{Z}_q$. A signature is $\sigma = (c_s, c_v, z_s, z_v) \in \mathbb{Z}_q^4$. Write $T_s(\sigma) = g^{z_s} y_s^{c_s}$ and $T_v(\sigma) = g^{z_v} y_v^{c_v}$; $\sigma$ is valid for $m$ if and only if $c_s + c_v \equiv H(y_s, y_v, m, T_s(\sigma), T_v(\sigma)) \pmod q$ (lines L6 and L7).

**Theorem 1 (correctness).** For every message and every choice of coins, verify accepts the output of sign.

*Proof.* Sign sets $t_s = g^k$ and $t_v = g^{z_v} y_v^{c_v}$ (line L2), so $T_v(\sigma) = t_v$. Line L4 sets $z_s = k - c_s x_s$, so $T_s(\sigma) = g^{k - c_s x_s} g^{x_s c_s} = g^k = t_s$. The verifier therefore hashes the same tuple as line L3 and gets $c$, and $c_s + c_v = (c - c_v) + c_v = c$. $\square$

**Theorem 2 (the verifier can make every signature).** For every valid $\sigma$ there is exactly one choice of signer coins $(k, c_v, z_v)$ with which sign outputs $\sigma$, and exactly one choice of simulator coins $(k', c_s, z_s)$ with which simulate (run with $x_v$) outputs $\sigma$. Hence, for uniform coins, the output of sign and the output of simulate are both uniform on the set of valid signatures for $m$, and they have the same distribution.

*Proof.* Signer side. If sign outputs $\sigma$, then its $c_v$ and $z_v$ are copied into $\sigma$, and $k$ is fixed by $z_s = k - c_s x_s$, so $k = z_s + c_s x_s$. Conversely, with these coins line L2 gives $t_s = g^{z_s + c_s x_s} = T_s(\sigma)$ and $t_v = T_v(\sigma)$, so line L3 gives $c = H(\ldots, T_s(\sigma), T_v(\sigma)) = c_s + c_v$ because $\sigma$ is valid, and lines L4 and L5 give back $c_s$ and $z_s$.

Simulator side. The roles of the two branches are swapped: $c_s$ and $z_s$ are copied, and $k' = z_v + c_v x_v$. With these coins line L8 gives $t_s = T_s(\sigma)$ and $t_v = g^{k'} = T_v(\sigma)$, and line L9 gives $c_v = (c_s + c_v) - c_s$ and $z_v = k' - c_v x_v$.

So each procedure is a bijection from $\mathbb{Z}_q^3$ onto the same set of valid signatures, and uniform coins give the uniform distribution on that set. $\square$

Theorem 2 is the reason a designated verifier signature does not transfer. A third party who sees $\sigma$ learns that it came from the holder of $x_s$ or from the holder of $x_v$, and both are equally likely: the distributions are identical, not only close. The verifier, who knows it did not run simulate, concludes that the signer signed. The tests check both bijections on 30 signatures and compare simple statistics of the two outputs.

**Unforgeability (note).** Correctness says nothing about a third party who knows neither key. In the random oracle model, two valid signatures with the same $(t_s, t_v)$ and different hash values $c \ne c'$ give $c_s \ne c_s'$ or $c_v \ne c_v'$; in the first case $x_s = (z_s - z_s')/(c_s' - c_s)$, and in the second case $x_v = (z_v - z_v')/(c_v' - c_v)$. By the forking lemma, a forger that knows neither key gives an algorithm for discrete logarithms in $G$. This is the soundness of the Cramer, Damgård and Schoenmakers OR proof.
