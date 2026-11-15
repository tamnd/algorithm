---
title: The queue method returns the grounded labelling and stops after linear work
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The input is a finite framework $(A, R)$ with $n = |A|$ arguments and $m = |R|$ attacks. $R$ is a set, so each attack is listed once. For a set $S$, $S^+$ is the set of the arguments that some member of $S$ attacks, and $F(S)$ is the set of the arguments that $S$ defends: $a \in F(S)$ when each attacker of $a$ is in $S^+$. A set $E$ is a complete extension when it is conflict-free and $E = F(E)$ (Dung 1995, Lemma 24). The grounded extension is the least complete extension (Dung 1995, Theorem 25).

Write $IN$, $OUT$ and $UND$ for the sets of the arguments with the label in, out and undec. "Pushed" means put in $Q$ by line L3 or line L12.

**Invariants.** Each time the test of line L4 runs:

> **(I1)** For each argument $c$, $count[c]$ is the number of attackers of $c$ that are not in $OUT$.
>
> **(I2)** Each argument in $IN$ or in $Q$ has all its attackers in $OUT$.
>
> **(I3)** Each argument in $OUT$ has an attacker in $IN$.
>
> **(I4)** $IN$, $OUT$ and the arguments in $Q$ are pairwise disjoint, and the arguments in $Q$ have the label undec.
>
> **(I5)** Each argument has been pushed at most once, and the arguments pushed so far are exactly the members of $IN$ and $Q$.

*Initialization.* Line L1 sets each count to the number of attackers, and $OUT$ is empty, so (I1) holds. Line L2 makes every label undec, and line L3 pushes exactly the arguments with no attacker, once each. These have no attacker at all, so (I2) holds, and (I3), (I4) and (I5) hold because $IN$ and $OUT$ are empty.

*Maintenance.* Line L5 takes $a$ out of $Q$. By (I4), $a$ has the label undec, and line L6 labels it in. So $a$ moves from $Q$ to $IN$, and (I2) still holds for $a$.

Lines L7 to L9 look at each $b$ that $a$ attacks. First, $b$ is not in $IN$: if it were, then by (I2) its attacker $a$ would be in $OUT$, but $a$ was in $Q$, which (I4) keeps apart from $OUT$. Second, $b$ is not in $Q$, for the same reason. So line L8 finds $b$ either already out, and does nothing, or undec and not in $Q$. In the second case line L9 labels $b$ out. Then $b$ has the attacker $a \in IN$, so (I3) holds for $b$. No argument of $IN$ or $Q$ changes its label, so (I4) holds.

When $b$ enters $OUT$, exactly the attacks $(b, c)$ change from "attacker not out" to "attacker out". Lines L10 and L11 decrease $count[c]$ once for each such attack, so (I1) holds again. If $count[c]$ reaches 0, then by (I1) every attacker of $c$ is in $OUT$, and line L12 pushes $c$, which keeps (I2). This $c$ is not in $OUT$: by (I3) it would have an attacker in $IN$, and that attacker would be in $OUT$ too, against (I4). It is not in $IN$ or $Q$: a count only goes down and never below 0 by (I1), so it reaches 0 at most once, and an argument pushed by line L3 has no attacker, so its count never changes. So $c$ has the label undec and was never pushed before, and (I4) and (I5) hold.

**Termination and work.** By (I5), each argument is pushed at most once, so the loop of line L4 runs at most $n$ times. Line L7 scans the attacks that leave an argument when it enters $IN$, and line L10 scans the attacks that leave an argument when it enters $OUT$. Each argument enters $IN$ at most once and $OUT$ at most once, and never both by (I4). So each attack $(x, y)$ is scanned at most once over the whole run, and lines L7 and L10 together run at most $m$ times. With the $\Theta(n + m)$ work of lines L1 to L3, the run takes $\Theta(n + m)$ steps.

**Lemma 1 (soundness).** Let $E$ be any complete extension of $(A, R)$. At each moment, $IN \subseteq E$ and $OUT \subseteq E^+$.

*Proof.* By induction on the steps of the run. At the start both sets are empty. When line L6 labels $a$ in, each attacker of $a$ is in $OUT$ by (I2), so it is in $E^+$ by the hypothesis. So $E$ defends $a$, and $a \in F(E) = E$. When line L9 labels $b$ out, $b$ is attacked by $a$, and $a \in E$, so $b \in E^+$. $\square$

**Lemma 2.** When the loop stops, $IN$ is a complete extension.

*Proof.* Now $Q$ is empty.

- $OUT = IN^+$. By (I3), $OUT \subseteq IN^+$. Each $a \in IN$ went through lines L7 to L9, which leave every argument that $a$ attacks in $OUT$. So $IN^+ \subseteq OUT$.
- $IN$ is conflict-free. If $a, b \in IN$ and $a$ attacks $b$, then $b \in IN^+ = OUT$, against (I4).
- $IN \subseteq F(IN)$. By (I2), each attacker of a member of $IN$ is in $OUT = IN^+$.
- $F(IN) \subseteq IN$. Let $IN$ defend $c$. Then each attacker of $c$ is in $IN^+ = OUT$, so $count[c] = 0$ by (I1). If $c$ has no attacker, line L3 pushed it. Else its count went from a positive value to 0 at line L11, and line L12 pushed it. By (I5), $c$ is in $IN$ or in $Q$, and $Q$ is empty. $\square$

**Theorem.** GROUNDED$(A, R)$ stops after $\Theta(n + m)$ steps. The arguments labelled in form the grounded extension $G$, the arguments labelled out form $G^+$, and the other arguments are labelled undec.

*Proof.* Termination and the bound are shown above. By Lemma 2, $IN$ is a complete extension. By Lemma 1, $IN$ is a subset of every complete extension. So $IN$ is the least complete extension, which is the grounded extension $G$ (Dung 1995, Theorem 25). By the proof of Lemma 2, $OUT = G^+$, and the remaining arguments keep the label undec from line L2. $\square$

The order in which $Q$ hands out the arguments is not used anywhere in the proof, so a stack or any other bag gives the same result.
