---
title: Correctness of the Kerberos exchanges
proves: [correctness, replay rejection]
status: full
---

We use the notation and the line numbers of the page. Let $\delta$ be the allowed clock skew. We assume that the AEAD is correct, $\mathrm{Dec}(K, u, \mathrm{Enc}(K, u, m)) = m$ for each key $K$, key usage $u$ and message $m$, and that $\mathrm{Dec}$ fails when the key or the usage differs from the one used to encrypt, except with negligible probability (INT-CTXT for each key, with the usage bound to the ciphertext).

**Theorem 1 (honest runs succeed).** Suppose the KDC, the client $C$ and the service $S$ follow the protocol, all messages arrive unchanged, the password of $C$ gives the key $K_c$ that the KDC stores, each local clock differs from the KDC's clock by at most $\delta$ at each step, the whole run takes place before the TGT and the service ticket expire, and each authenticator is sent once. Then each check of lines L2, L5, L7, L10, L12 and L14 passes, and at the end $C$ and $S$ hold the same key $K_{c,s}$.

*Proof.* We go through the exchanges in order.

AS exchange. In line L1, $C$ seals its current time $t_C$ under $K_c$ with usage 1. In line L2 the KDC holds the same $K_c$, so decryption succeeds by correctness, and $|t_{KDC} - t_C| \le \delta$ by the clock assumption, so the pre-authentication check passes. In line L3 the KDC seals the TGT under $K_{tgs}$ with usage 2 and the reply part under $K_c$ with usage 3, and puts the nonce $n_1$ of the request and the name of the TGS into the reply part. In line L5, $C$ opens the reply part with $K_c$ and usage 3, which succeeds, and finds the nonce and the server name that it sent. So $C$ holds $K_{c,tgs}$ and the TGT, and the TGT holds the same $K_{c,tgs}$.

TGS exchange. In line L6, $C$ seals an authenticator $\{c, t, u\}$ under $K_{c,tgs}$ with usage 7, where $u$ is a counter that $C$ increases for each authenticator. In line L7 the TGS opens the TGT with $K_{tgs}$ and usage 2 and finds the name of the TGS. The TGT has not expired by assumption, and its start time is the KDC's time at issue, which is not later than now. The TGS opens the authenticator with the key $K_{c,tgs}$ from the TGT, which is the key that $C$ used, so decryption succeeds; the name in the authenticator is $c$, as is the name in the TGT; and $|t_{TGS} - t| \le \delta$ by the clock assumption. The replay cache holds no entry $(c, t, u, \text{krbtgt})$, because $u$ is new and each authenticator is sent once. So line L7 passes. Lines L8 and L9 seal the service ticket under $K_s$ and the reply under $K_{c,tgs}$ with usage 8, and line L10 succeeds by the same argument as line L5.

AP exchange. Line L11 seals a fresh authenticator under $K_{c,s}$ with usage 11. Line L12 repeats the argument of line L7 with $K_s$ in place of $K_{tgs}$, so $S$ accepts and stores the key $K_{c,s}$ from the ticket. Line L13 seals the time stamp $(t, u)$ of that authenticator under $K_{c,s}$ with usage 12, and in line L14, $C$ opens it with its own copy of $K_{c,s}$ and finds its own $(t, u)$. Both copies of $K_{c,s}$ come from the single value that the TGS chose in line L8: one through the service ticket, the other through the TGS reply. $\square$

**Lemma 2 (replay rejection).** Let a service accept an AP-REQ with authenticator time $t$ at its local time $\tau$. If the same AP-REQ is sent to that service again at local time $\tau' \ge \tau$, line L12 rejects it.

*Proof.* If $\tau' - t > \delta$, the skew check rejects it. Otherwise $\tau' \le t + \delta$. The cache keeps each entry while its time $t$ is at least $\tau'' - \delta$ for the current time $\tau''$, and $t \ge \tau' - \delta$, so the entry $(c, t, u, s)$ that the first acceptance added is still in the cache at time $\tau'$, and the cache check rejects the second copy. $\square$

**Lemma 3 (expiry).** A ticket with end time $e$ is rejected in line L7 or line L12 at each local time $\tau > e + \delta$.

*Proof.* The ticket is sealed under the long-term key of its service, so no one without that key can change $e$ without failing the decryption check. The check $\tau > e + \delta$ then rejects it. $\square$

Lemma 2 is why the replay cache only needs to keep entries for $\delta$ seconds, and Lemma 3 together with the cap on ticket life in lines L3 and L8 bounds how long a stolen ticket and its session key stay useful. Theorem 1 is a statement about honest runs. It does not show that the key is secret against an active attacker; for that, see the formal analyses cited on the page. $\blacksquare$
