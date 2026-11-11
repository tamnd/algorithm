---
title: A DC-net delivers the message and hides the sender when the honest key graph is connected
proves: [correctness, sender anonymity]
status: full
---

We use the notation and the line numbers of the page. The key graph is $\Gamma = (V, E)$ with $V = \{1, \ldots, n\}$. For each edge $e = \{i, j\}$, line L1 gives a key $k_e$, uniform in $\{0, 1\}^\ell$ and independent of the other keys. We write $\oplus$ for the XOR of $\ell$-bit strings, which makes $\{0, 1\}^\ell$ a vector space over the field with two elements. Party $i$ sends $m_i$, where $m_i = 0^\ell$ if $i$ does not send, so lines L2 and L3 give
$$A_i = m_i \oplus \bigoplus_{e \ni i} k_e.$$

**Lemma 1 (each key is in two announcements).** $\bigoplus_{i \in V} A_i = \bigoplus_{i \in V} m_i$.

*Proof.* Expand the XOR of all $A_i$. Each $m_i$ appears once. Each key $k_e$ with $e = \{i, j\}$ appears in $A_i$ and in $A_j$ and in no other announcement, since line L2 takes only the edges at a party. So it appears exactly twice, and $k_e \oplus k_e = 0^\ell$. What is left is $\bigoplus_i m_i$. $\square$

**Theorem 2 (correctness).** If exactly one party $s$ sends $m$ in a round and all parties follow lines L1 to L5, every party computes $M = m$ in line L5. If no party sends, $M = 0^\ell$. If parties $s_1, \ldots, s_r$ send, $M = m_{s_1} \oplus \cdots \oplus m_{s_r}$.

*Proof.* This is Lemma 1 with the given $m_i$. All parties see the same broadcast announcements, so they compute the same $M$. $\square$

**Lemma 3 (the honest key sums are uniform on a hyperplane).** Let $H \subseteq V$ be a set of parties such that the subgraph $\Gamma_H$ of edges with both ends in $H$ is connected, and let $h = |H|$. For $i \in H$ let $K_i = \bigoplus_{e \ni i,\, e \subseteq H} k_e$. Then the vector $(K_i)_{i \in H}$ is uniform on the set $Z = \{(v_i)_{i \in H} : \bigoplus_{i \in H} v_i = 0^\ell\}$, and independent of the keys on edges that are not inside $H$.

*Proof.* Independence is clear, because $(K_i)$ is a function of the keys inside $H$ only, and keys are independent. The map $\phi$ from the keys inside $H$ to $(K_i)_{i \in H}$ is linear over the two-element field, in each of the $\ell$ bit positions separately. Its image lies in $Z$, by the argument of Lemma 1 applied to $\Gamma_H$. We show that the image is all of $Z$. Take a spanning tree $\tau$ of $\Gamma_H$, which exists since $\Gamma_H$ is connected, and set the keys on edges outside $\tau$ to $0$. Given $v \in Z$, we choose the keys on $\tau$ from the leaves up: pick a leaf $i$ of $\tau$ with its tree edge $e$, set $k_e = v_i$, so $K_i = v_i$, and replace $v_j$ by $v_j \oplus v_i$ for the other end $j$ of $e$; remove $i$ and repeat. Each step keeps the XOR of the remaining entries at $0$, so when one vertex is left its entry is $0$, which matches its key sum, the XOR of no remaining edges. So $\phi$ maps onto $Z$. A linear map from a uniform input gives an output that is uniform on its image, since every point of the image has the same number of preimages (a coset of the kernel). $\square$

**Theorem 4 (Chaum's theorem: sender anonymity).** Let $C \subseteq V$ be a coalition of dishonest parties, and $H = V \setminus C$ the honest parties, and assume that $\Gamma_H$ is connected. The view of $C$ is the set of keys on edges that touch $C$, the messages of $C$, and all announcements. Then for any two honest parties $s, s' \in H$ and any message $m$, the view of $C$ when $s$ sends $m$ has the same distribution as when $s'$ sends $m$. This holds against an adversary of unlimited computing power.

*Proof.* Condition on the keys on edges that touch $C$; they are part of the view and are independent of the keys inside $H$. For honest $i$, let $c_i$ be the XOR of the keys on edges from $i$ to $C$, which $C$ knows. Then $A_i = K_i \oplus c_i \oplus m_i$ for $i \in H$, where $m_i = m$ if $i$ is the sender and $0^\ell$ otherwise. The announcements of $C$ are functions of its keys and its own messages, so they do not depend on who in $H$ sends. By Lemma 3, $(K_i)_{i \in H}$ is uniform on $Z$. Adding the fixed vector $(c_i \oplus m_i)_{i \in H}$ is a bijection from $Z$ to the coset $Z \oplus (c_i \oplus m_i)_i$, which is the set of vectors whose XOR is $\bigoplus_{i \in H} c_i \oplus m$. This set is the same for $s$ and for $s'$, because it depends on the sender only through the XOR of the $m_i$, which is $m$ in both cases. So the honest announcements are uniform on the same set in both cases, and the full view has the same distribution. No step uses a computational assumption, so the statement holds for any adversary. $\square$

**Proposition 5 (the condition is needed).** If $\Gamma_H$ is not connected, let $H_1$ be a connected component of $\Gamma_H$. Then $C$ learns whether the sender is in $H_1$.

*Proof.* $C$ computes $\bigoplus_{i \in H_1} (A_i \oplus c_i)$. Each key inside $H_1$ cancels by the argument of Lemma 1, and there are no honest edges from $H_1$ to the rest of $H$, since $H_1$ is a component. So the value is $\bigoplus_{i \in H_1} m_i$, which is $m$ if the sender is in $H_1$ and $0^\ell$ otherwise. For $m \ne 0^\ell$ this tells the two cases apart. $\square$

The proof of Theorem 4 shows more: for any vector of messages $(m_i)_{i \in H}$, the honest announcements are uniform on the vectors whose XOR is $\bigoplus_{i \in H} c_i \oplus \bigoplus_{i \in H} m_i$. So the view of $C$ depends on the honest messages only through their XOR.

**Proposition 6 (jamming is not detected).** Let $C$ be a set of observing parties, which may include the sender, and let $H = V \setminus C$ with $\Gamma_H$ connected. Suppose that one party $j \in H$ adds a nonzero string $z$ to its announcement. Then every party computes $M = m \oplus z \neq m$, and the view of $C$ has the same distribution for every choice of $j \in H$.

*Proof.* The first claim is Lemma 1 with $m_j$ replaced by $m_j \oplus z$. For the second, treat $z$ as a message of $j$. The XOR of the messages of $H$ is $z$ if the sender is in $C$, and $m \oplus z$ if the sender is in $H$; in both cases it does not depend on $j$. By the remark after Theorem 4, the view of $C$ then has the same distribution for every $j \in H$. So the observers, the sender among them, see that the round is broken but cannot tell from the round who broke it. $\blacksquare$
