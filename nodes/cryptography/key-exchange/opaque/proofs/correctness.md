---
title: Correctness of OPAQUE
proves: [correctness]
status: full
---

We prove that a client who registered with a password and logs in with the same password recovers its key pair, that both sides compute the same session key, and that all checks pass. We also show that a wrong password makes the envelope check fail unless the MAC is forged. Notation is that of the page: $G$ has prime order $q$ and generator $g$, and every received element is checked to lie in $G \setminus \{1\}$.

**Lemma 1 (OPRF unblinding).** For any $h \in G$, $k \in [1, q)$ and $r \in [1, q)$, if $M = h^r$ and $Z = M^k$, then $Z^{r^{-1} \bmod q} = h^k$.

*Proof.* $Z = h^{rk}$, so $Z^{r^{-1}} = h^{r k r^{-1}}$. As $h$ has order dividing $q$, exponents are taken modulo $q$, and $r r^{-1} \equiv 1 \pmod q$, so the result is $h^k$. The inverse exists because $q$ is prime and $r \ne 0$. $\square$

**Lemma 2 (same randomized password).** If the server uses the same OPRF key $k_C$ at registration and at login, and the client uses the same password, the client computes the same $y$ and the same rwd in lines L3 and L8.

*Proof.* The server derives $k_C$ deterministically from its seed and the credential identifier, so it is the same in lines L2 and L7. By Lemma 1, the client gets $H'(pw)^{k_C}$ in both lines, whatever the two blinding factors were. Then $y = H(pw, H'(pw)^{k_C})$ and $\mathrm{rwd} = \mathrm{Extract}(\texttt{""}, y \| \mathrm{KSF}(y))$ are fixed functions of equal inputs. $\square$

**Lemma 3 (unmasking).** With the same rwd, the client recovers $pk_S$ and the envelope exactly from the masked response.

*Proof.* masking_key $= \mathrm{Expand}(\mathrm{rwd}, \texttt{"MaskingKey"})$ is the value the server stored at registration. The server computes $\mathrm{masked} = \mathrm{pad} \oplus (pk_S \| \mathrm{envelope})$ with $\mathrm{pad} = \mathrm{Expand}(\text{masking\_key}, \text{masking\_nonce} \| \texttt{"CredentialResponsePad"})$, and sends masking_nonce in clear. The client computes the same pad and XORs it again; since $a \oplus b \oplus b = a$, it obtains $pk_S \| \mathrm{envelope}$. $\square$

**Lemma 4 (envelope recovery).** With the same rwd, the same nonce, the same $pk_S$ and the same identities, the client re-derives the registered $(sk_U, pk_U)$ and the tag check of line L8 passes.

*Proof.* At registration, line L4 derived $(sk_U, pk_U)$ from $\mathrm{Expand}(\mathrm{rwd}, \text{nonce} \| \texttt{"PrivateKey"})$ by a deterministic function, and line L5 computed the tag with auth_key $= \mathrm{Expand}(\mathrm{rwd}, \text{nonce} \| \texttt{"AuthKey"})$ over nonce, $pk_S$ and the identities. At login, the client reads the nonce from the envelope (Lemma 3) and computes the same Expand outputs from the same rwd (Lemma 2), so it gets the same key pair and the same tag. $\square$

**Lemma 5 (3DH agreement).** If the client holds $sk_U$ with $pk_U = g^{sk_U}$ (the stored value) and the server holds $sk_S$ with $pk_S = g^{sk_S}$, both compute the same $(dh_1, dh_2, dh_3)$.

*Proof.* The client computes $dh_1 = epk_S^{esk_U} = g^{esk_S esk_U}$, $dh_2 = pk_S^{esk_U} = g^{sk_S esk_U}$ and $dh_3 = epk_S^{sk_U} = g^{esk_S sk_U}$. The server computes $dh_1 = epk_U^{esk_S} = g^{esk_U esk_S}$, $dh_2 = epk_U^{sk_S} = g^{esk_U sk_S}$ and $dh_3 = pk_U^{esk_S} = g^{sk_U esk_S}$. Exponent products commute, so each pair is equal. $\square$

**Lemma 6 (keys and MACs).** If both sides hold the same $dh_1, dh_2, dh_3$ and the same preamble, they derive the same Km2, Km3 and session_key, and both MAC checks pass.

*Proof.* The preamble is a fixed encoding of the identities, KE1 and KE2 without its MAC, and both sides hold the same values of these, since messages arrive unchanged. The key schedule applies Extract and Expand to equal inputs. The client recomputes the server MAC with the same Km2 over the same hash, and the server recomputes KE3 with the same Km3 over the same preamble and server MAC. $\square$

**Theorem.** If the client registered with $pw$ and logs in with $pw$, the login completes without abort, both sides output the same session_key, and the client obtains the export key of registration. If the client logs in with $pw' \ne pw$, line L8 aborts unless $H$ or $H'$ collides on $pw, pw'$, or the MAC is forged.

*Proof.* Lemmas 2 to 6 give the first part; the export key is $\mathrm{Expand}(\mathrm{rwd}, \text{nonce} \| \texttt{"ExportKey"})$, equal by Lemma 2. For $pw' \ne pw$, the value $y' = H(pw', H'(pw')^{k_C})$ differs from $y$ unless $H$ collides, because the first input differs. Then $\mathrm{rwd}' \ne \mathrm{rwd}$ unless Extract collides, so masking_key and auth_key differ. The unmasked envelope is then a string the client cannot relate to rwd', and the tag check passes only if the stored tag equals a MAC under an independent key, that is, only by a forgery. $\blacksquare$
