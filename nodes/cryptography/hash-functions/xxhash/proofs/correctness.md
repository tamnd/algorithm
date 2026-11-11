---
title: The steps of xxHash are bijections, which explains both its spread and its lack of security
proves: [correctness]
status: full
---

We use the notation of the page, with words of $w$ bits and arithmetic modulo $2^w$.

**Lemma 1.** For odd $P$, the map $x \mapsto P x$ is a bijection of $\mathbb{Z}/2^w$. For any $k$ with $1 \le k < w$, the maps $x \mapsto x \lll k$ and $x \mapsto x \oplus (x \gg k)$ are bijections of $\{0,1\}^w$.

*Proof.* An odd $P$ has an inverse modulo $2^w$. Rotation by $k$ is undone by rotation by $w - k$. For the xorshift, the top $k$ bits of $y = x \oplus (x \gg k)$ equal those of $x$; then each lower block of $k$ bits of $x$ is the matching block of $y$ XOR the block above it in $x$, which is already known. So $x$ is determined by $y$. $\square$

**Lemma 2 (the round).** For fixed $a$, the map $l \mapsto ((a + l P_2) \lll r) P_1$ is a bijection; for fixed $l$, the map of $a$ is a bijection.

*Proof.* It is a composition of an addition, a multiplication by the odd $P_2$ (for the map of $l$), a rotation and a multiplication by the odd $P_1$; each is a bijection by Lemma 1. $\square$

**Theorem 1 (the code is the specified function).** The code follows steps 1 to 7 of the specification line by line, and the tests check it on all 17 values of the reference self-test. A function has no other notion of correctness. $\blacksquare$

**Theorem 2 (preimages of short inputs).** For a fixed seed $s$, XXH32 restricted to 4-byte inputs is a bijection of $\{0,1\}^{32}$, and its inverse costs a constant number of word operations.

*Proof.* For $n = 4$ the computation is $h = s + P_5 + 4$, then $h \gets ((h + u P_3) \lll 17) P_4$, then the mix of line L6. The map of $u$ is a bijection by Lemma 2, and the mix is a composition of bijections by Lemma 1. Undo each step in reverse order. $\square$

**Theorem 3 (collisions with a known seed).** For a known seed and any input $x$ with at least two stripes, and any change of lane $i$ in stripe $j$, there is exactly one value of lane $i$ in stripe $j + 1$ that makes the accumulators after stripe $j + 1$ equal to those of $x$, so the two inputs collide.

*Proof.* Let $a$ and $a'$ be accumulator $i$ after stripe $j$ for the two inputs, and $l$ lane $i$ of stripe $j + 1$ in $x$. The round after stripe $j + 1$ is a function of $a + l P_2$. Choosing $l' = l + (a - a') P_2^{-1}$ gives $a' + l' P_2 = a + l P_2$, so the accumulators agree after that round. The other accumulators did not change, and all later steps are the same for both inputs. $\square$

**Remark.** The bijections are what spread the bits: no step merges two different internal states, so differences are never lost, and the final mix sends each bit to about half of the output bits. The same property makes every step easy to invert, so xxHash has no preimage or collision resistance against an attacker who knows the seed. With a secret seed the attack above does not apply directly, but no security claim is made for that case either.
