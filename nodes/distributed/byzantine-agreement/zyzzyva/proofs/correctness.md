---
title: Zyzzyva is safe within a view, and its view change is not
proves: [correctness]
status: full
---

**Claim.** Let $n = 3f + 1$ replicas run Zyzzyva with at most $f$ Byzantine replicas and unforgeable signatures. (1) Within one view, any two histories that clients complete, on the fast path or on the two-phase path, are prefixes of each other. (2) The view change of the SOSP 2007 and TOCS 2009 papers does not keep this property across views: there are runs with $n = 4$ and $f = 1$ in which two clients complete histories that differ at position 1. Part (2) is the result of Abraham, Gueta, Malkhi, Alvisi, Kotla and Martin (arXiv 1712.01367); the tests of the implementation replay both of their runs.

**Setup.** A *spec response* of replica $i$ is a signed $(v, H)$: replica $i$ in view $v$ has executed the history $H$. A client completes $H$ in view $v$ on the *fast path* with $3f + 1$ matching spec responses for $(v, H)$, and on the *two-phase path* with a *commit certificate*, $2f + 1$ matching spec responses for $(v, H)$, and then $2f + 1$ LOCAL-COMMIT replies to it. The rules of an honest replica that the proof uses:

- (Z1) In view $v$ it executes a request only if the ORDER-REQ extends its current history by one request (line L2). So its histories in view $v$ form a chain $H_0 \subset H_1 \subset \dots$, each a prefix of the next.
- (Z2) It sends a spec response for $(v, H)$ only when $H$ is its current history in view $v$.
- (Z3) It sends LOCAL-COMMIT for a commit certificate only if the history of the certificate is a prefix of its own history, and it keeps the certificate (line L5).

## Part 1: safety within a view

**Lemma 1.** Any two sets of $2f + 1$ replicas share an honest replica.

*Proof.* Two such sets share at least $2(2f + 1) - (3f + 1) = f + 1$ replicas, and at most $f$ of them are faulty. $\square$

**Theorem 1.** If clients complete $H_1$ and $H_2$ in the same view $v$, then one of them is a prefix of the other.

*Proof.* Each completion rests on $2f + 1$ or more spec responses for its history in view $v$: the fast path has $3f + 1$, and the two-phase path has a commit certificate with $2f + 1$. Signatures cannot be forged, so the replicas named in each set really signed. By Lemma 1 an honest replica $i$ signed both $(v, H_1)$ and $(v, H_2)$. By (Z2) both were its current history at some time in view $v$, and by (Z1) its histories in view $v$ form a chain. So one of $H_1$ and $H_2$ is a prefix of the other. $\blacksquare$

Theorem 1 holds whatever the primary does: a faulty primary can send different requests to different replicas, but it cannot get $2f + 1$ signatures for two histories that fork. The tests check this with 200 seeded runs of a faulty primary that gives each request a random prefix and random receivers, and that signs spec responses for any history.

**What the view change must do.** After a completion in view $v$, every later view must start from a history that extends the completed one. The evidence that the new primary sees, in $2f + 1$ VIEW-CHANGE messages, is:

- after a fast-path completion of $H$, all $3f + 1$ replicas signed $H$, so the $2f + 1$ messages contain at least $f + 1$ honest replicas whose histories extend $H$;
- after a two-phase completion of $H$, $2f + 1$ replicas sent LOCAL-COMMIT, so by Lemma 1 the messages contain an honest replica that holds a commit certificate for $H$ (Z3).

The rule of the papers uses both kinds of evidence: the new primary starts from the commit certificate with the longest history, and then appends every request that $f + 1$ VIEW-CHANGE histories hold at the next position (lines L8 and L9). Each kind of evidence is correct alone. The rule fails because the two kinds can point to different histories, and the rule does not compare them by view.

## Part 2: two runs that break safety

Take $n = 4$, $f = 1$, replicas $i_1, i_2, i_3, i_4$, and $i_1$ Byzantine. The primary of view $v$ is $i_v$. The network is asynchronous until after the last step, so every delay below is allowed.

**Run 1 (Section 2.3 of the paper).**

1. View 1, primary $i_1$. It sends request $a$ at position 1 to $i_1$, $i_2$, $i_3$ and request $b$ at position 1 to $i_4$. Client $c_1$ gets 3 matching spec responses for $(1, a)$, a commit certificate $C_a$. Its COMMIT reaches only $i_1$, and $c_1$ does not complete.
2. View 2, primary $i_2$. It gets VIEW-CHANGE from $i_2$ (history $a$), $i_4$ (history $b$) and $i_1$, which hides $C_a$ and claims history $b$. No message has a certificate, and $b$ has $f + 1 = 2$ votes at position 1, so the new history is $b$. All four replicas execute it and client $c_2$ gets 4 matching spec responses for $(2, b)$: $b$ completes at position 1 on the fast path.
3. View 3, primary $i_3$. It gets VIEW-CHANGE from $i_1$ (with $C_a$), $i_3$ and $i_4$ (history $b$). The rule starts from the certificate, so the new history is $a$, and a client completes $a$ at position 1.

The fast-path evidence for $b$ (two honest histories) loses to an older commit certificate for $a$.

**Run 2 (Section 2.4 of the paper).**

1. View 1, primary $i_1$. It orders $a_1, a_2$ at $i_1$, $i_2$, $i_3$. A client forms a commit certificate $C_1$ for $(a_1, a_2)$, and its COMMIT reaches only $i_1$.
2. View 2, primary $i_2$. It gets VIEW-CHANGE from $i_1$ (claims the empty history), $i_2$ ($a_1, a_2$) and $i_4$ (empty). No request has $f + 1$ votes, so the new history is empty. $i_3$ is slow and stays in view 1. The primary orders $b_1$ at $i_1$, $i_2$, $i_4$; a client forms a commit certificate $C_2$ for $(b_1)$ and gets LOCAL-COMMIT from all three: $b_1$ completes at position 1.
3. View 3, primary $i_3$. It gets VIEW-CHANGE from $i_1$ (with $C_1$), $i_3$ ($a_1, a_2$) and $i_4$ (with $C_2$). $C_1$ is longer, so the new history is $(a_1, a_2)$, and a client completes it: position 1 holds $a_1$ for one client and $b_1$ for another.

Here a newer commit certificate loses to a longer, older one. Choosing the certificate of the highest view fixes Run 2 but not Run 1, where the fast-path completion leaves no certificate at all.

**Conclusion.** Within a view the quorums of Theorem 1 make Zyzzyva safe. Across views, safety needs a rule that ranks all evidence by the view in which it was formed, as the view change of [PBFT](/pbft/) does with its prepared certificates; the rule of the original papers does not, and the two runs above violate safety. $\blacksquare$
