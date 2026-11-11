---
title: Correctness of CPace
proves: [correctness]
status: full
---

We prove that two honest parties with the same PRS, CI, sid and transcript compute the same ISK, and that line L7 aborts only with negligible probability in an honest run. Notation is that of the page. Curve25519 has order $8\ell$ with $\ell$ a prime close to $2^{252}$, and its twist has order $4\ell'$ with $\ell'$ prime. For a 32-byte string $y$, let $c(y)$ be the clamped scalar of RFC 7748: the three low bits cleared, bit 255 cleared and bit 254 set, so $c(y) = 8 c'(y)$ with $2^{251} \le c'(y) < 2^{252}$.

**Lemma 1 (same generator).** If both parties use the same PRS, CI and sid, they compute the same $g$ in lines L1 to L4.

*Proof.* Line L1 is a fixed encoding of (DSI, PRS, CI, sid), line L2 a hash, line L3 a fixed decoding and line L4 a fixed function. A composition of functions gives equal outputs on equal inputs. $\square$

**Lemma 2 (X25519 commutes).** For any u-coordinate $g$ and scalars $y_a$, $y_b$, $\mathrm{X25519}(y_a, \mathrm{X25519}(y_b, g)) = \mathrm{X25519}(y_b, \mathrm{X25519}(y_a, g))$.

*Proof.* RFC 7748 defines $\mathrm{X25519}(y, u)$ as the u-coordinate of $c(y) \cdot Q$, where $Q$ is a point with u-coordinate $u$ on Curve25519 or on its quadratic twist; the Montgomery ladder computes this value without knowing which one, and the u-coordinate of $c \cdot Q$ is the same for $Q$ and $-Q$, so the result does not depend on the choice of the point. Let $G$ be a point with u-coordinate $g$. Then $\mathrm{X25519}(y_b, g)$ is the u-coordinate of $c(y_b) G$, and applying $y_a$ gives the u-coordinate of $c(y_a)(c(y_b) G) = (c(y_a) c(y_b)) G$. By symmetry the other side gets the u-coordinate of $(c(y_b) c(y_a)) G$, the same point. $\square$

**Lemma 3 (no false abort).** If $g$ is the u-coordinate of a point $G$ of order $8\ell$, $4\ell$, $2\ell$ or $\ell$ (on the curve), or of a point of order divisible by $\ell'$ (on the twist), then $K \ne I$ for every pair of scalars.

*Proof.* Take the curve case. We have $c(y_a) c(y_b) = 64\, c'(y_a)\, c'(y_b)$ with $0 < c'(y) < 2^{252}$. The prime $\ell$ equals $2^{252} + 27742317777372353535851937790883648493$, so $\ell > 2^{252} > c'(y)$, and $\ell$ divides neither $c'(y_a)$, nor $c'(y_b)$, nor 64. As $\ell$ is prime, $\ell \nmid c(y_a) c(y_b)$. The order of $G$ is a multiple of $\ell$, so the order of $(c(y_a) c(y_b)) G$ is still a multiple of $\ell$. Hence this point is neither the neutral element nor the point of order 2, which are the two points whose u-coordinate encodes as 32 zero bytes. In the twist case the same argument works with $\ell' = 2^{253} - 55484635554744707071703875581767296995 > 2^{252}$. $\square$

The Elligator 2 map of line L4 outputs the u-coordinate of a point on the curve, of order in $\{1, 2, 4, 8, \ell, 2\ell, 4\ell, 8\ell\}$. Only the 8 points of order dividing 8 fall outside Lemma 3, and each point has at most two preimages $\pm u$ under the map. In the random oracle model the hash of line L2 makes $u$ uniform over about $2^{255}$ values, so the probability of a low-order $g$ is at most $16 \cdot 2^{-254}$, which is negligible.

**Lemma 4 (same ISK).** If both parties hold the same $K$, sid and transcript, they compute the same ISK in line L8.

*Proof.* Line L8 is a hash of a fixed encoding of (DSI, sid, $K$) followed by the transcript. In the initiator-responder setting both parties build $\mathrm{lv\_cat}(Y_a, AD_a) \| \mathrm{lv\_cat}(Y_b, AD_b)$ from the same received and sent values. In the symmetric setting the ordered concatenation puts the larger of the two strings first, which does not depend on which party computes it. So the hash inputs are equal. $\square$

**Theorem.** If $A$ and $B$ hold the same PRS, CI, sid and transcript form, and the messages $(Y_a, AD_a)$ and $(Y_b, AD_b)$ arrive unchanged, both output the same ISK, and line L7 aborts only with negligible probability.

*Proof.* By Lemma 1 both use the same $g$. $A$ computes $K = \mathrm{X25519}(y_a, Y_b) = \mathrm{X25519}(y_a, \mathrm{X25519}(y_b, g))$ and $B$ computes $\mathrm{X25519}(y_b, \mathrm{X25519}(y_a, g))$; Lemma 2 shows that they are equal. Lemma 3 and the remark after it show that $K \ne I$ except with negligible probability. Lemma 4 then gives equal ISK. $\blacksquare$

If PRS differs, the generators are two outputs of a random oracle followed by Elligator 2, so they are unrelated points, and equal ISK values would need $K_A = K_B$ or a hash collision. This happens only with negligible probability, which the test with a wrong password checks.
