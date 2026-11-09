---
title: Pre-star and post-star saturation compute exactly the predecessors and successors
proves: [correctness, termination]
status: full
---

**Setting.** $\mathcal{P} = (P, \Gamma, \Delta)$ is a pushdown system whose rules $\langle p, \gamma \rangle \hookrightarrow \langle p', w \rangle$ have $|w| \le 2$. The input $\mathcal{P}$-automaton is $\mathcal{A} = (Q, \Gamma, \to_0, P, F)$, with no transition into a state of $P$. Let $C = L(\mathcal{A})$. For a set $R$ of transitions, $s \xrightarrow{w}_R s'$ means that $R$ has a path labelled $w$ from $s$ to $s'$; for post*, the path may use empty moves, which do not add to the label. A step $\langle p, \gamma u \rangle \Rightarrow \langle p', w u \rangle$ by a rule only depends on the top letter, so

$$(\ast) \qquad \langle p, v \rangle \Rightarrow^* \langle p', v' \rangle \text{ implies } \langle p, v u \rangle \Rightarrow^* \langle p', v' u \rangle \text{ for each } u \in \Gamma^*.$$

## Part 1: PRE-STAR

Let $R$ be the final value of rel.

**Lemma 1 (termination).** Every transition that enters trans has the form $(s, \gamma, s')$ with $s, s' \in Q$. So rel only grows, inside the finite set $Q \times \Gamma \times Q$; each iteration of line L4 removes one element of trans and adds new elements only in an iteration where line L7 makes rel larger. Such iterations happen at most $|Q|^2 |\Gamma|$ times, each adds finitely many elements to trans, and every other iteration makes trans smaller. So the loop stops.

*Proof.* Lines L2, L8 and L10 add $(p, \gamma, p')$, $(p_1, \gamma_1, q')$ and $(p_1, \gamma_1, q'')$, whose targets are targets of transitions already in rel, or control locations; all are in $Q$. Derived rules have targets $q' \in Q$ too. The counting is as stated. $\square$

**Reasons.** Each transition $t = (p, \gamma, s) \in R \setminus {\to_0}$ was put into trans at line L2, L8 or L10, and we fix one such moment. At that moment the following holds: there is a rule step $\langle p, \gamma \rangle \Rightarrow \langle p', w \rangle$ with $|w| \le 2$ and a path $p' \xrightarrow{w} s$ that uses transitions already in rel, so inserted into rel before $t$. Indeed:

- line L2: the rule $\langle p, \gamma \rangle \hookrightarrow \langle s, \varepsilon \rangle$ and the empty path from $s$ to $s$;
- line L8 with a rule of $\Delta$: the rule $\langle p, \gamma \rangle \hookrightarrow \langle q, \gamma' \rangle$ and the transition $(q, \gamma', s) \in$ rel being processed;
- line L8 with a derived rule $\langle p, \gamma \rangle \hookrightarrow \langle q', \gamma_2 \rangle$, which line L9 made from a rule $\langle p, \gamma \rangle \hookrightarrow \langle q, \gamma' \gamma_2 \rangle$ and a transition $(q, \gamma', q') \in$ rel, and the transition $(q', \gamma_2, s)$ being processed: the path $q \xrightarrow{\gamma'} q' \xrightarrow{\gamma_2} s$;
- line L10: the same rule $\langle p, \gamma \rangle \hookrightarrow \langle q, \gamma' \gamma_2 \rangle$, the transition $(q, \gamma', q')$ being processed and $(q', \gamma_2, s) \in$ rel.

In all cases the path has at most two transitions, each inserted into rel before $t$.

**Lemma 2 (shape).** Every transition of $R \setminus {\to_0}$ starts in a state of $P$. A path in $R$ that starts in a state of $Q \setminus P$ uses only transitions of $\to_0$.

*Proof.* Lines L2, L8 and L10 add transitions whose source is the left side of a rule, which is in $P$. A transition of $\to_0$ never enters $P$, so a path that starts outside $P$ stays outside $P$, and from there only transitions of $\to_0$ leave. $\square$

**Lemma 3 (soundness).** If $p \in P$ and $p \xrightarrow{w}_R s$, then there is a configuration $\langle p', w' \rangle$ with $\langle p, w \rangle \Rightarrow^* \langle p', w' \rangle$ and $p' \xrightarrow{w'}_{\to_0} s$.

*Proof.* Order the transitions of $R$ by their insertion time, with the transitions of $\to_0$ counted as time 0. To a path, assign the multiset of the insertion times of its transitions. We use induction on this multiset in the multiset order, which is well founded. If all transitions of the path are in $\to_0$, take $\langle p', w' \rangle = \langle p, w \rangle$. Otherwise, by Lemma 2 the first transition $t = (p, \gamma, s_1)$ of the path is not in $\to_0$: if it were, the rest of the path would start outside $P$ and would use only $\to_0$ too. Write $w = \gamma v$ and $s_1 \xrightarrow{v}_R s$. The reason of $t$ gives $\langle p, \gamma \rangle \Rightarrow \langle p'', u \rangle$ and a path $p'' \xrightarrow{u}_R s_1$ of at most two transitions, each older than $t$. The path $p'' \xrightarrow{u} s_1 \xrightarrow{v} s$ has the multiset of the old path with the time of $t$ replaced by at most two smaller times, so it is smaller in the multiset order. By induction, $\langle p'', u v \rangle \Rightarrow^* \langle p', w' \rangle$ with $p' \xrightarrow{w'}_{\to_0} s$. With $(\ast)$, $\langle p, \gamma v \rangle \Rightarrow \langle p'', u v \rangle \Rightarrow^* \langle p', w' \rangle$. $\square$

**Lemma 4 (saturation).** $R \supseteq {\to_0}$, and for each rule $\langle p, \gamma \rangle \hookrightarrow \langle p', w \rangle$ and each path $p' \xrightarrow{w}_R s$, the transition $(p, \gamma, s)$ is in $R$.

*Proof.* Every element of trans is eventually removed at line L5 and is then in rel, so every transition that is ever put into trans is in $R$; this includes $\to_0$. Take a rule and a path.

- $w = \varepsilon$: then $s = p'$, and line L2 put $(p, \gamma, p')$ into trans.
- $w = \gamma'$: the transition $(p', \gamma', s)$ was processed at some time, and then line L8 scanned the rule and put $(p, \gamma, s)$ into trans.
- $w = \gamma' \gamma_2$, with $(p', \gamma', q') \in R$ and $(q', \gamma_2, s) \in R$. If $(q', \gamma_2, s)$ entered rel before $(p', \gamma', q')$ was processed, then while processing $(p', \gamma', q')$, line L10 found it and put $(p, \gamma, s)$ into trans. Otherwise line L9 had already added the derived rule $\langle p, \gamma \rangle \hookrightarrow \langle q', \gamma_2 \rangle$ when $(q', \gamma_2, s)$ was processed, and line L8 put $(p, \gamma, s)$ into trans. $\square$

**Lemma 5 (completeness).** If $\langle p, w \rangle \Rightarrow^* \langle p', w' \rangle$ and $p' \xrightarrow{w'}_R s$, then $p \xrightarrow{w}_R s$.

*Proof.* By induction on the length of the run. For length 0 there is nothing to show. Otherwise the run starts with a step $\langle p, \gamma v \rangle \Rightarrow \langle p'', u v \rangle$ by a rule $\langle p, \gamma \rangle \hookrightarrow \langle p'', u \rangle$, with $w = \gamma v$. By induction, $p'' \xrightarrow{u v}_R s$, so there is a state $s_1$ with $p'' \xrightarrow{u}_R s_1 \xrightarrow{v}_R s$. By Lemma 4, $(p, \gamma, s_1) \in R$, so $p \xrightarrow{\gamma v}_R s$. $\square$

**Theorem 1.** The automaton $(Q, \Gamma, R, P, F)$ accepts exactly $\mathrm{pre}^*(C)$.

*Proof.* If it accepts $\langle p, w \rangle$, then $p \xrightarrow{w}_R f$ with $f \in F$, and Lemma 3 gives $\langle p, w \rangle \Rightarrow^* \langle p', w' \rangle$ with $p' \xrightarrow{w'}_{\to_0} f$, so $\langle p', w' \rangle \in C$. Conversely, if $\langle p, w \rangle \Rightarrow^* \langle p', w' \rangle \in C$, then $p' \xrightarrow{w'}_{\to_0} f$ for some $f \in F$; this path is in $R$ by Lemma 4, and Lemma 5 gives $p \xrightarrow{w}_R f$. $\square$

## Part 2: POST-STAR

Let $M$ be the set of new states $m_{p', \gamma_1}$ and $R$ the final rel. Write $Q_0 = Q \setminus P$.

**Lemma 6 (shape and termination).** Every transition of $R$ has its source in $P \cup M \cup Q_0$ and its target in $Q_0 \cup M$. Empty moves start in $P$. Transitions that start in $Q_0$ are those of $\to_0$. Transitions that start in $M$ have a letter of $\Gamma$. The algorithm stops.

*Proof.* Line P1 puts the transitions of $\to_0$ that leave $Q_0$ into rel; they end in $Q_0$, because $\to_0$ has no transition into $P$. The other transitions are added at lines P7 to P11 with sources $p' \in P$, $p \in P$, $p'' \in P$ or $m \in M$, and targets that are targets of transitions already in rel, or new states. By induction on the insertion order, no target is in $P$. Empty moves are added only at line P7, with a source in $P$. The sets of states and letters are finite, rel only grows, and trans grows only when rel does, so the loop stops as in Lemma 1. $\square$

By Lemma 6, empty moves never follow each other: an empty move ends outside $P$, and empty moves start in $P$.

**Invariants.** We show that each transition of $R$ has the following property, by induction on the insertion order.

- (A) A transition $(p, a, s)$ with $p \in P$, $a \in \Gamma \cup \{\varepsilon\}$ and $s \in Q_0$: there is $\langle p', w' \rangle$ with $p' \xrightarrow{w'}_{\to_0} s$ and $\langle p', w' \rangle \Rightarrow^* \langle p, a \rangle$, where $\langle p, \varepsilon \rangle$ is the configuration with an empty stack.
- (B) A transition $(p, a, m_{p^\circ, \gamma^\circ})$ with $p \in P$: $\langle p^\circ, \gamma^\circ \rangle \Rightarrow^* \langle p, a \rangle$.
- (C) A transition $(m_{p^\circ, \gamma^\circ}, \gamma_2, s)$: there is a rule $\langle p_1, \gamma_1 \rangle \hookrightarrow \langle p^\circ, \gamma^\circ \gamma_2 \rangle$ and a transition $(p_1, \gamma_1, s) \in R$ that was inserted before it.

It is convenient to merge (A) and (B) into one statement about a transition $(p, a, s)$ with $p \in P$: there is an *origin* of $s$ that reaches $\langle p, a \rangle$, where an origin of $s \in Q_0$ is a configuration $\langle p', w' \rangle$ with $p' \xrightarrow{w'}_{\to_0} s$, and the origin of $m_{p^\circ, \gamma^\circ}$ is $\langle p^\circ, \gamma^\circ \rangle$.

*Proof of the invariants.* Transitions of $\to_0$ from $P$ satisfy (A) with $\langle p', w' \rangle = \langle p, a \rangle$, and those from $Q_0$ need no property. For a transition put into trans while processing $(p, a, s)$ with $a \in \Gamma$, which by induction has an origin $o$ of $s$ with $o \Rightarrow^* \langle p, a \rangle$:

- line P7, $(p', \varepsilon, s)$: $o \Rightarrow^* \langle p, a \rangle \Rightarrow \langle p', \varepsilon \rangle$, so $o$ is an origin that works.
- line P8, $(p', \gamma_1, s)$: $o \Rightarrow^* \langle p, a \rangle \Rightarrow \langle p', \gamma_1 \rangle$.
- line P9, $(p', \gamma_1, m_{p', \gamma_1})$: (B) holds with the empty run. The transition $(m_{p', \gamma_1}, \gamma_2, s)$ has (C) with the rule $\langle p, a \rangle \hookrightarrow \langle p', \gamma_1 \gamma_2 \rangle$ and the transition $(p, a, s)$.
- line P10 and line P11 add $(p'', b, s')$ from an empty move $(p'', \varepsilon, x)$ and a transition $(x, b, s')$, both in rel. If $x \in Q_0$, then $(x, b, s')$ is in $\to_0$ and $s' \in Q_0$; by (A) there is $\langle p', w' \rangle$ with $p' \xrightarrow{w'}_{\to_0} x$ and $\langle p', w' \rangle \Rightarrow^* \langle p'', \varepsilon \rangle$. Then $p' \xrightarrow{w' b}_{\to_0} s'$, and by $(\ast)$, $\langle p', w' b \rangle \Rightarrow^* \langle p'', b \rangle$. If $x = m_{p^\circ, \gamma^\circ}$, then by (B), $\langle p^\circ, \gamma^\circ \rangle \Rightarrow^* \langle p'', \varepsilon \rangle$, and by (C) there is a rule $\langle p_1, \gamma_1 \rangle \hookrightarrow \langle p^\circ, \gamma^\circ b \rangle$ with $(p_1, \gamma_1, s') \in R$ older, which has an origin $o$ of $s'$ with $o \Rightarrow^* \langle p_1, \gamma_1 \rangle$. Then $o \Rightarrow^* \langle p_1, \gamma_1 \rangle \Rightarrow \langle p^\circ, \gamma^\circ b \rangle \Rightarrow^* \langle p'', b \rangle$, using $(\ast)$ in the last part. $\square$

**Lemma 7 (soundness).** If $p \in P$ and $p \xrightarrow{w}_R s$ with $s \in Q_0 \cup M$, then some origin $o$ of $s$ has $o \Rightarrow^* \langle p, w \rangle$. If $s = p$ and $w = \varepsilon$, then $\langle p, \varepsilon \rangle$ is its own origin in the sense that $p \xrightarrow{\varepsilon}_{\to_0} p$.

*Proof.* By induction on the number of transitions of the path. A path of length 0 is the second case. Let the first transition be $(p, a, s_1)$, with $w = a v$ and $s_1 \xrightarrow{v}_R s$. If $s_1 \in Q_0$, then by Lemma 6 the rest of the path is in $\to_0$; by the invariant there is $\langle p', w' \rangle$ with $p' \xrightarrow{w'}_{\to_0} s_1$ and $\langle p', w' \rangle \Rightarrow^* \langle p, a \rangle$, so $\langle p', w' v \rangle$ is an origin of $s$ that reaches $\langle p, a v \rangle$ by $(\ast)$. If $s_1 = m_{p^\circ, \gamma^\circ}$ and $v = \varepsilon$, the claim is (B). Otherwise the next transition is $(s_1, \gamma_2, s_2)$ with $v = \gamma_2 v'$, and (C) gives a rule $\langle p_1, \gamma_1 \rangle \hookrightarrow \langle p^\circ, \gamma^\circ \gamma_2 \rangle$ with $(p_1, \gamma_1, s_2) \in R$. The path $p_1 \xrightarrow{\gamma_1} s_2 \xrightarrow{v'}_R s$ is one transition shorter, so by induction some origin $o$ of $s$ has $o \Rightarrow^* \langle p_1, \gamma_1 v' \rangle$. Then $o \Rightarrow^* \langle p_1, \gamma_1 v' \rangle \Rightarrow \langle p^\circ, \gamma^\circ \gamma_2 v' \rangle \Rightarrow^* \langle p, a \gamma_2 v' \rangle$ by (B) and $(\ast)$. $\square$

**Lemma 8 (saturation).** (a) If $(p, \gamma, s) \in R$ with $p \in P$ and $\langle p, \gamma \rangle \hookrightarrow \langle p', u \rangle$, then $p' \xrightarrow{u}_R s$. (b) If $(p, \varepsilon, x) \in R$ and $(x, b, s) \in R$, then $(p, b, s) \in R$.

*Proof.* (a) When $(p, \gamma, s)$ was processed, line P7, P8 or P9 put $(p', \varepsilon, s)$, $(p', \gamma_1, s)$, or $(p', \gamma_1, m_{p', \gamma_1})$ and $(m_{p', \gamma_1}, \gamma_2, s)$ into trans or rel, and everything put into trans ends in $R$. (b) If $(x, b, s)$ was in rel when $(p, \varepsilon, x)$ was processed, line P11 added $(p, b, s)$. Otherwise $(x, b, s)$ entered rel later. It does not start in $P$, so by Lemma 6 and line P1 it was added at line P9 with $x \in M$, and then line P10 found $(p, \varepsilon, x)$ and added $(p, b, s)$. $\square$

**Lemma 9 (completeness).** If $c \in C$ and $c \Rightarrow^* \langle p, w \rangle$, then the result accepts $\langle p, w \rangle$.

*Proof.* By induction on the length of the run. A configuration of $C$ is accepted by $\to_0 \subseteq R$. For a step $\langle p, \gamma v \rangle \Rightarrow \langle p'', u v \rangle$ by a rule $\langle p, \gamma \rangle \hookrightarrow \langle p'', u \rangle$: by induction, $p \xrightarrow{\gamma v}_R f$ with $f \in F$. If the path starts with an empty move $(p, \varepsilon, x)$, then $x \notin P$ and the next transition $(x, \gamma, s_1)$ is not empty, so by Lemma 8 (b) the two can be replaced by $(p, \gamma, s_1)$. So we may assume the path is $p \xrightarrow{\gamma} s_1 \xrightarrow{v}_R f$. Lemma 8 (a) gives $p'' \xrightarrow{u}_R s_1$, so $p'' \xrightarrow{u v}_R f$. $\square$

**Theorem 2.** The result of POST-STAR accepts exactly $\mathrm{post}^*(C)$.

*Proof.* If it accepts $\langle p, w \rangle$, then $p \xrightarrow{w}_R f$ with $f \in F \subseteq Q$; the new states are not final. If the path is empty, $\langle p, \varepsilon \rangle \in C$ because $p \in F$. Otherwise $f \in Q_0$, and Lemma 7 gives $\langle p', w' \rangle$ with $p' \xrightarrow{w'}_{\to_0} f$, which is in $C$, and $\langle p', w' \rangle \Rightarrow^* \langle p, w \rangle$. The converse is Lemma 9. $\blacksquare$
