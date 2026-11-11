---
title: ECIES decryption inverts ECIES encryption
proves: [correctness]
status: full
---

**Setting.** $E$ is an elliptic curve over $\mathbb{F}_p$, and $E(\mathbb{F}_p)$ is its group of points with identity $O$. $G \in E(\mathbb{F}_p)$ has prime order $n$, and the cofactor $h$ is not divisible by $n$. The private key is $d \in \{1, \ldots, n-1\}$ and the public key is $Q = dG$ (lines L1 and L2). The KDF and the MAC are deterministic functions, and decode is the inverse of the point encoding on points of $E$.

**Claim.** For every message $m$ and every $k \in \{1, \ldots, n-1\}$, ECIES-DECRYPT$(d, \cdot)$ applied to the output $(\bar{R}, c, t)$ of ECIES-ENCRYPT$(Q, m)$ with scalar $k$ returns $m$, with the same choice of the option bind on both sides.

*Proof.* We use two facts about scalar multiplication, where $aP$ means $P$ added to itself $a$ times.

**Fact 1.** For integers $a, b \ge 0$ and a point $P$, $a(bP) = (ab)P$. *Proof of the fact.* $a(bP)$ is the sum of $a$ copies of the sum of $b$ copies of $P$. The group is associative, so this is the sum of $ab$ copies of $P$. $\square$

**Fact 2.** For an integer $a$, $aG = O$ if and only if $n$ divides $a$. *Proof of the fact.* This is the definition of the order $n$ of $G$ together with division with remainder: write $a = sn + r$ with $0 \le r < n$; then $aG = s(nG) + rG = rG$, and $rG = O$ with $0 < r < n$ would contradict the minimality of $n$. $\square$

*Step 1: line L11 accepts.* $R = kG$ is a point of $E$, because $E(\mathbb{F}_p)$ is closed under addition. The encoding of line L5 and decode are inverse to each other, so line L11 recovers $R$ and the curve test passes.

*Step 2: both sides compute the same $Z$.* The sender computes $Z_s = (hk)Q = (hk)(dG)$, and the receiver computes $Z_r = (hd)R = (hd)(kG)$. By Fact 1 both equal $(hkd)G$, so $Z_s = Z_r$.

*Step 3: $Z \ne O$.* $n$ is prime and divides none of $h$, $k$ and $d$ ($k$ and $d$ lie strictly between 0 and $n$). A prime that divides a product divides one of its factors, so $n$ does not divide $hkd$, and by Fact 2 $Z = (hkd)G \ne O$. So line L12 does not reject, and $x(Z)$ is defined.

*Step 4: the keys agree.* The input of the KDF at line L13 is $x(Z_r)$, followed by $\bar{R}$ if bind is set. By Step 2 and since the receiver uses the $\bar{R}$ it received, this is exactly the input of line L7. The requested length is $|c| + 32 = |m| + 32$ on both sides, because XOR keeps the length. The KDF is deterministic, so both sides get the same $k_E$ and $k_M$.

*Step 5: the tag check passes.* Line L14 computes $\mathrm{MAC}(k_M, c)$ with the same key and the same $c$ as line L9. The MAC is deterministic, so the result equals $t$, and line L14 does not reject.

*Step 6: line L15 returns $m$.* $c \oplus k_E = (m \oplus k_E) \oplus k_E = m \oplus (k_E \oplus k_E) = m$, because XOR is associative and every byte string XOR itself is zero.

So ECIES-DECRYPT returns $m$. $\blacksquare$
