---
title: MurmurHash3_x86_32 is built from bijections of the state
proves: [correctness, termination]
status: full
---

**Notation.** All values are 32-bit words, that is elements of $\{0, \ldots, 2^{32} - 1\}$, with arithmetic modulo $2^{32}$. For a word $k$, let $\mathrm{MIX}(k)$ and $\mathrm{FMIX}(k)$ be the values returned by lines L12 to L13 and L14 to L18. For a block $k$, let $B_k(h) = \mathrm{ROTL}(h \oplus \mathrm{MIX}(k), 13) \cdot 5 + \mathtt{0xe6546b64}$ be the effect of lines L4 and L5 on the state.

**Lemma 1 (termination and the computed value).** MURMUR3-32 stops on every input. If the input has the full blocks $k_0, \ldots, k_{q-1}$ with $q = \lfloor n/4 \rfloor$ and the tail word $k_q$ of line L7, it returns $\mathrm{FMIX}(T(B_{k_{q-1}}(\cdots B_{k_0}(s) \cdots)) \oplus n)$, where $s$ is the seed, $T(h) = h \oplus \mathrm{MIX}(k_q)$ if $n > 4q$ and $T(h) = h$ otherwise.

*Proof.* The loop of line L2 makes $q$ passes and every other line runs once, so the procedure stops. Line L3 forms $k_j$ from bytes $4j$ to $4j + 3$, and lines L4 and L5 replace $h$ by $B_{k_j}(h)$; by induction on $j$, after $j$ passes $h = B_{k_{j-1}}(\cdots B_{k_0}(s) \cdots)$. Lines L6 to L9 apply $T$, line L10 XORs $n$, and line L11 applies FMIX. $\square$

**Lemma 2 (the basic bijections).** Each of the following maps of 32-bit words is a bijection: (a) $x \mapsto x \oplus c$ for a constant $c$; (b) $x \mapsto \mathrm{ROTL}(x, r)$; (c) $x \mapsto c x$ for an odd constant $c$; (d) $x \mapsto x + c$; (e) $x \mapsto x \oplus (x \gg r)$ for $1 \le r \le 31$.

*Proof.* (a) is its own inverse. (b) has the inverse $\mathrm{ROTL}(\cdot, 32 - r)$. (c): an odd $c$ is coprime to $2^{32}$, so it has an inverse $c^{-1}$ modulo $2^{32}$, and $y \mapsto c^{-1} y$ inverts the map. (d) has the inverse $y \mapsto y - c$. (e): the set is finite, so it suffices to show injectivity. Let $y = x \oplus (x \gg r)$. Bits $31$ down to $32 - r$ of $x \gg r$ are 0, so these bits of $y$ equal those of $x$. For a bit $i < 32 - r$, bit $i$ of $y$ is bit $i$ of $x$ XOR bit $i + r$ of $x$. Going from bit 31 down to bit 0, each bit of $x$ is determined by $y$ and the higher bits of $x$, which are already known. So $y$ determines $x$. $\square$

**Lemma 3.** MIX and FMIX are bijections, and for every block $k$, $B_k$ is a bijection.

*Proof.* MIX is (c) with $c_1$, then (b), then (c) with $c_2$; $c_1$ and $c_2$ are odd. FMIX is (e) with $r = 16$, (c) with $f_1$, (e) with $r = 13$, (c) with $f_2$ and (e) with $r = 16$; $f_1$ and $f_2$ are odd. $B_k$ is (a) with $c = \mathrm{MIX}(k)$, (b), (c) with $c = 5$ and (d). Compositions of bijections are bijections (Lemma 2). $\square$

**Lemma 4 (seeds).** For a fixed input, the map from the seed to the hash is a bijection. So distinct seeds give distinct hashes of one input.

*Proof.* By Lemma 1, the hash is $\mathrm{FMIX}(T(B_{k_{q-1}} \circ \cdots \circ B_{k_0}(s)) \oplus n)$. For a fixed input, $T$ is the identity or (a), and $\oplus n$ is (a). By Lemma 3, the map $s \mapsto$ hash is a composition of bijections. $\square$

**Lemma 5 (one changed block).** Let $x \ne y$ be inputs of the same length $n$ that differ only within one full block, or only within the tail. Then they have different hashes for every seed.

*Proof.* The two inputs have the same blocks except one, with words $k \ne k'$. If it is the full block $j$, the states before it are equal, say $h$. MIX is injective (Lemma 3), so $h \oplus \mathrm{MIX}(k) \ne h \oplus \mathrm{MIX}(k')$, and the rest of $B$ is injective, so the states after the block differ. The remaining steps are the same bijections for both inputs, since they have the same later blocks, the same tail and the same $n$; so the hashes differ. If it is the tail, the tail words differ, the states before line L9 are equal, and the same argument applies to line L9 followed by lines L10 and L11. $\square$

**Lemma 6 (collisions for every seed).** Let $x_1, x_2, y_1, y_2$ be blocks with $\mathrm{MIX}(y_1) = \mathrm{MIX}(x_1) \oplus 2^{18}$ and $\mathrm{MIX}(y_2) = \mathrm{MIX}(x_2) \oplus 2^{31}$, and let $z$ be any byte string. Then $x_1 x_2 z$ and $y_1 y_2 z$ have equal hashes for every seed.

*Proof.* Such $y_1, y_2$ exist because MIX is a bijection (Lemma 3). Let $h$ be the state before the first block; it is the seed. After line L4, the states are $u = h \oplus \mathrm{MIX}(x_1)$ and $u \oplus 2^{18}$. ROTL by 13 gives $v$ and $v \oplus 2^{31}$. XOR with $2^{31}$ is the same as adding $2^{31}$ modulo $2^{32}$, since it changes only the top bit. So the states after line L5 are $5v + a$ and $5(v + 2^{31}) + a = 5v + a + 5 \cdot 2^{31} = 5v + a + 2^{31}$, where $a = \mathtt{0xe6546b64}$, because $4 \cdot 2^{31} \equiv 0$. Writing $w = 5v + a$, they are $w$ and $w \oplus 2^{31}$. After line L4 on the second block, they are $w \oplus \mathrm{MIX}(x_2)$ and $w \oplus 2^{31} \oplus \mathrm{MIX}(x_2) \oplus 2^{31} = w \oplus \mathrm{MIX}(x_2)$, which are equal. From here the two inputs have the same bytes $z$ and the same length, so by Lemma 1 they reach the same hash. $\square$

**Theorem.** MURMUR3-32 stops on every input and returns the value of Lemma 1. Its block mix and finalizer are bijections; for a fixed input, distinct seeds give distinct hashes; equal-length inputs that differ in one block never collide; and the pairs of Lemma 6 collide for every seed.

*Proof.* Lemmas 1, 3, 4, 5 and 6. $\blacksquare$

**Remark (what is not proved).** The avalanche behaviour and the spread of hash values over ordinary inputs are measured properties, not theorems. Lemma 6 shows that no bound on the probability of a collision over a random seed can hold for all fixed pairs of inputs.
