---
title: The hygienic solution keeps exclusion and an acyclic precedence graph, and every hungry philosopher eats
proves: [correctness]
status: full
---

**Model.** The conflict graph $G$ is a finite simple undirected graph on the philosophers. Each edge $e = \{u, w\}$ has one fork and one request token. At any time the fork of $e$ is at $u$, at $w$, or on its way to one of them, and the same holds for the token. We say an object is *on $u$'s side* if it is at $u$ or on its way to $u$. A fork has a bit, clean or dirty. Each philosopher is thinking, hungry or eating, and takes one step at a time by the rules L2 to L7; the network delivers each message after a finite delay (L5). Initially (L1) the fork of $\{u, w\}$ with $u < w$ is at $u$ and dirty, the token is at $w$, and every philosopher is thinking. For fairness we assume weak fairness: a philosopher or a channel that has an enabled step forever eventually takes a step, and every meal ends.

**The precedence graph.** $H$ orients every edge of $G$: $u \to w$ ($u$ has precedence over $w$) if the fork of $\{u, w\}$ is on $u$'s side and clean, or on $w$'s side and dirty. A fork on its way is always clean (L4 cleans it), so a fork in transit gives precedence to its receiver.

**Lemma 1.** If the token and the fork of $e = \{u, w\}$ are both on $u$'s side, then $w$ is hungry.

*Proof.* Initially the two are on different sides. Consider the steps that can make the premise true. A token moves to $u$'s side only by L3 at $w$, which needs $w$ hungry and the fork not at $w$, that is, on $u$'s side; so after the step the premise holds and $w$ is hungry. A fork moves to $u$'s side only by L4 at $w$, which needs the token at $w$; after the step the token is on $w$'s side, so the premise is false. Deliveries (L5) do not change sides. While the premise holds, $w$ cannot stop being hungry: it leaves the hungry state only by eating (L6), which needs the fork at $w$. $\square$

**Lemma 2.** In every reachable state: (a) a clean fork is on the side of a hungry philosopher; (b) an eating philosopher holds all its forks, and all of them are dirty.

*Proof.* (a) A fork becomes clean only by L4 at some $u$, which sends it to $w$. Just before, the fork and the token were both at $u$, so $w$ is hungry by Lemma 1. A clean fork never moves again (L4 needs a dirty fork), and $w$ stays hungry until it eats, which makes the fork dirty (L6). (b) L6 needs all forks at $u$ and makes them dirty. While $u$ eats, it fires no L4 (which needs $u$ not eating), so no fork leaves, and nothing cleans a fork that is not sent. $\square$

**Theorem 1 (exclusion).** Two neighbours never eat at the same time.

*Proof.* Neighbours $u$ and $w$ share one fork. By Lemma 2(b) both would hold it. $\square$

**Theorem 2 (the precedence graph stays acyclic).** $H$ is acyclic in every reachable state.

*Proof.* Initially every fork is dirty and at the lower numbered end, so every edge of $H$ goes from the higher to the lower number, and $H$ is acyclic. We check each kind of step. L2, L3, L5 and L7 do not move a fork across sides and do not change a fork bit, so $H$ does not change. L4 at $u$ sends a dirty fork of $\{u, w\}$ from $u$ to $w$ and cleans it: before, the fork was dirty on $u$'s side, so $w \to u$; after, it is clean on $w$'s side, so again $w \to u$. Only L6 changes $H$: when $u$ eats, all its forks are on its side and become dirty, so every edge at $u$ now points to $u$, and $u$ is a sink. Edges not at $u$ do not change. Suppose the new $H$ had a cycle. If the cycle avoids $u$, it uses only unchanged edges, so it was a cycle before. If it passes through $u$, it must leave $u$ on an edge out of $u$, but $u$ is a sink. Both cases are impossible, so $H$ stays acyclic. $\square$

For a philosopher $u$, let $\mathit{anc}(u)$ be the set of philosophers with a path to $u$ in $H$ (not including $u$; $H$ is acyclic, so $u \notin \mathit{anc}(u)$).

**Lemma 3.** While $u$ does not eat, $\mathit{anc}(u)$ gains no member, and a member that eats leaves it.

*Proof.* $H$ changes only when some $x \ne u$ eats, which makes $x$ a sink and changes only edges at $x$. A path to $u$ in the new graph cannot pass through $x$, since it would have to leave the sink $x$; so it uses only edges that did not change, and was a path before. Hence the new $\mathit{anc}(u)$ is contained in the old one, without $x$. $\square$

**Theorem 3 (starvation freedom).** Under weak fairness, every hungry philosopher eventually eats.

*Proof.* By strong induction on $k$, we show: a philosopher that is hungry at a time when $|\mathit{anc}(u)| = k$ eventually eats. Fix such a $u$ and suppose it never eats. By Lemma 3, $\mathit{anc}(u)$ never grows, so from some time $t_1$ on it is a fixed set $A$, and no member of $A$ eats after $t_1$ (it would leave $A$).

Let $w$ be a neighbour of $u$ with $w \to u$ at some time after $t_1$, so $w \in A$. Every path to $w$ extends to $u$, and $w \notin \mathit{anc}(w)$, so $\mathit{anc}(w) \subsetneq A$ and $|\mathit{anc}(w)| < k$. Hence, by induction, $w$ is never hungry after $t_1$: a hungry $w$ would eventually eat, and it is in $A$. In particular $w$ never holds a clean fork after $t_1$ (Lemma 2(a)), so the edge $w \to u$ comes from the fork being dirty on $u$'s side, and $w$, which is not hungry, never sends the token to $u$ (L3 needs hunger). If the token were on $u$'s side together with the fork, $w$ would be hungry by Lemma 1; so the token stays at $w$.

Let $w$ be a neighbour with $u \to w$. If the fork is clean on $u$'s side, $u$ keeps it, since L4 needs a dirty fork. Otherwise the fork is dirty on $w$'s side. If $u$ holds the token, L3 is enabled at $u$ until it fires, so the token reaches $w$. At $w$, the fork is dirty and the token is there: $w$ cannot eat (L6 is blocked by that fork), an eating $w$ finishes, and then L4 at $w$ is enabled until it fires, so the fork comes to $u$ clean, and from then on $u$ keeps it. An edge at $u$ changes direction only when $u$ eats or a neighbour $w$ eats (Theorem 2); $u$ does not eat, and a neighbour that eats becomes a sink, which gives $u \to w$, this case again. So no new edge $w \to u$ appears after $t_1$, and the two cases cover every neighbour.

So eventually $u$ holds all its forks, and each one is either clean, or dirty with its token at the neighbour. Then L3 and L4 are disabled at $u$ (it holds every fork, and holds no token together with a dirty fork), and L6 is enabled and stays enabled, since nothing can take a clean fork from a hungry philosopher, and the neighbours in $A$ never send their tokens. By weak fairness $u$ eats, which is a contradiction. $\square$

Theorem 3 implies deadlock freedom: if some philosopher is hungry, some philosopher eventually eats. $\blacksquare$
