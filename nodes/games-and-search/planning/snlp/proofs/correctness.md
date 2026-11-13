---
title: SNLP is sound, terminates, is complete within its bound, returns a plan with the fewest steps, and is systematic
proves: [correctness]
status: full
---

We use the pseudocode of the page. The task is a ground STRIPS task $(F, A, I, G)$, and a plan is a sequence of actions that applies from $I$ and ends in a state that contains $G$. A partial plan $P$ has steps $0$ (START, with $\mathit{add} = I$), $1$ (FINISH, with $\mathit{pre} = G$) and other steps, each a copy of an action; an ordering $\prec$, the transitive closure of its constraints; and causal links $i \xrightarrow{p} j$ with $p \in \mathit{add}(i) \cap \mathit{pre}(j)$ and $i \prec j$. A step $k$ *touches* $p$ if $p \in \mathit{add}(k) \cup \mathit{del}(k)$. A threat is a pair $(k, i \xrightarrow{p} j)$ with $k \ne i, j$, $k$ touching $p$, and neither $k \prec i$ nor $j \prec k$. A linearization $L$ is a total order of the steps that extends $\prec$, and $\mathrm{seq}(L)$ is its list of actions without START and FINISH.

Two facts about the search tree are used below. Every step other than START is created by line L13 together with a link from it, so every step other than START and FINISH is the producer of a link, and following links forward from any step reaches FINISH. And a link is added only for an open condition, which it closes, so each pair $(p, j)$ is the consumer end of at most one link.

**Lemma 1 (soundness).** If $P$ has acyclic orderings, no open condition and no threat, then $\mathrm{seq}(L)$ is a plan for every linearization $L$.

*Proof.* Let $L = (0, s_1, \ldots, s_m, 1)$ and let $x_t$ be the state after $t$ actions, with $x_0 = I$. We show that every precondition $p$ of $s_{t+1}$ is in $x_t$; the same argument for FINISH gives $G \subseteq x_m$. There is a link $i \xrightarrow{p} s_{t+1}$, and $i$ comes earlier in $L$. If $i = s_r$, then $p \in x_r$ since $p \in \mathit{add}(s_r)$; if $i$ is START, then $p \in x_0$. A step $k$ strictly between $i$ and $s_{t+1}$ in $L$ satisfies neither $k \prec i$ nor $s_{t+1} \prec k$, because $L$ extends $\prec$. If $p \in \mathit{del}(k)$, then $k$ touches $p$ and $(k, i \xrightarrow{p} s_{t+1})$ is a threat, which $P$ does not have. So no action between them deletes $p$, and $p \in x_t$. $\square$

**Lemma 2 (termination).** For a fixed $n$, REFINE visits finitely many partial plans.

*Proof.* Each refinement adds a new step with a link (at most $n$ times on a branch, by line L13), or a link that closes an open condition (at most $(n + 1) q$ times, for the largest precondition size $q$, since links are never removed), or an ordering $k \prec i$ or $j \prec k$ for a threat. A threat exists only if neither pair is in $\prec$, so the closure gains a pair, and it has at most $(n + 2)^2$ pairs. So every branch is finite, every node has finitely many children, and by König's lemma the tree is finite. $\square$

**Lemma 3 (the step bound).** If a plan exists, a plan with at most $2^{|F|} - 1$ actions exists. A shortest plan contains no action $a$ with $\mathit{add}(a) \subseteq \mathit{pre}(a)$, and every precondition of its actions is reachable when delete lists are ignored.

*Proof.* A shortest plan visits no state twice, and there are $2^{|F|}$ states. If $a$ applies in $x$ and $\mathit{add}(a) \subseteq \mathit{pre}(a) \subseteq x$, the next state is a subset of $x$; STRIPS is monotone (if $x \subseteq y$ and $a$ applies in $x$, it applies in $y$ and gives a superset), so the plan without $a$ still works and is shorter. Every state that a plan visits lies inside the facts reachable with delete lists ignored. $\square$

So the filter of the implementation keeps every action of a shortest plan.

**Lemma 4 (completeness).** Let $\sigma = (a_1, \ldots, a_m)$ be a plan over the actions given to REFINE, with $m \le n$. Then REFINE with the bound $n$ returns a complete plan.

*Proof.* Give START position $0$, FINISH position $m + 1$ and $a_t$ position $t$, and say that position $0$ adds $I$. Call $P$ *faithful* if there is a one-to-one map $\phi$ from the steps of $P$ to positions with $\phi(\text{START}) = 0$, $\phi(\text{FINISH}) = m + 1$, every other step $s$ a copy of $a_{\phi(s)}$, $i \prec j$ only if $\phi(i) < \phi(j)$, and, for every link $i \xrightarrow{p} j$, $\phi(i)$ the last position before $\phi(j)$ that adds $p$. The first plan is faithful. We show that each flaw of a faithful plan has a resolver that gives a faithful child. Then, whichever flaw line L8 picks, a faithful child exists; following such children gives a finite path (Lemma 2) that ends at a faithful plan with no flaw, which line L7 returns, unless the depth-first search returns another complete plan first.

*Open condition $(p, j)$.* Since $\sigma$ is a plan, $p$ holds before position $\phi(j)$, so some earlier position adds $p$; let $q$ be the last. If $q = \phi(i)$ for a step $i$, then $j \prec i$ is false, so line L12 offers $i \xrightarrow{p} j$, and its ordering $i \prec j$ agrees with $\phi$. Otherwise $q \ne 0$ and $q$ is unused, so $P$ has fewer than $m \le n$ action steps, and line L13 offers a new copy of $a_q$ linked to $j$; extend $\phi$ by $q$. Orderings that agree with $\phi$ have a closure that agrees with $\phi$.

*Threat $(k, i \xrightarrow{p} j)$.* Since $\phi$ is one to one, $\phi(k) \notin \{\phi(i), \phi(j)\}$. Suppose $\phi(i) < \phi(k) < \phi(j)$. If $p \in \mathit{add}(k)$, then $\phi(k)$ is a later position before $\phi(j)$ that adds $p$, against the choice of $\phi(i)$. Otherwise $p \in \mathit{del}(k)$, $p$ is false after position $\phi(k)$, and no position between $\phi(k)$ and $\phi(j)$ adds $p$ (that would again contradict the choice of $\phi(i)$), so $p$ is false before $\phi(j)$, against $\sigma$ being a plan. So $\phi(k) < \phi(i)$ and demotion agrees with $\phi$, or $\phi(k) > \phi(j)$ and promotion agrees with $\phi$. That ordering keeps $\prec$ acyclic, so line L10 offers it. $\square$

**Lemma 5 (the cut test).** If a round with bound $n$ ends with $\mathit{cut} = \mathit{false}$, then every round with a bound $n' > n$ visits the same partial plans and also fails.

*Proof.* The bound appears only in line L13. Since line L14 never ran, at each open condition the round met, either $P$ had fewer than $n$ steps or no action adds $p$, and in both cases the set $R$ is the same under $n'$. By induction from the root the two rounds make the same choices. $\square$

**Lemma 6 (the last adder).** Let $P$ be complete and $L$ a linearization. For every link $i \xrightarrow{p} j$, $i$ is the last step before $j$ in $L$ that adds $p$.

*Proof.* $i$ adds $p$ and comes before $j$. A step $k \ne i, j$ that adds $p$ and lies between them in $L$ touches $p$ and satisfies neither $k \prec i$ nor $j \prec k$, so it would form a threat. $\square$

**Lemma 7 (systematicity).** Let $P_1 \ne P_2$ be two complete plans returned at different leaves of one bounded search. Then no linearization $L_1$ of $P_1$ and $L_2$ of $P_2$ have $\mathrm{seq}(L_1) = \mathrm{seq}(L_2)$.

*Proof.* Suppose $\mathrm{seq}(L_1) = \mathrm{seq}(L_2) = \tau = (b_1, \ldots, b_m)$, with START at position $0$, adding $I$, and FINISH at $m + 1$. Let $N$ be the deepest common ancestor of the two leaves; it has a flaw $f$, and the leaves lie below two different resolvers $r_1 \ne r_2$ of $f$. The steps and links of $N$ belong to both $P_1$ and $P_2$.

For a complete plan $P$ that contains $N$ and a linearization $L$ of $P$ with $\mathrm{seq}(L) = \tau$, write $\pi_L(s)$ for the position of step $s$ in $L$. By Lemma 6, if $s \xrightarrow{p} w$ is a link, then $\pi_L(s)$ is the last position before $\pi_L(w)$ in $\tau$ that adds $p$. So $\pi_L(s)$ is a function of $\tau$, $p$ and $\pi_L(w)$ alone. Every step of $N$ other than START and FINISH is the producer of a link of $N$ whose consumer was created earlier, so by induction on the creation order, starting from $\pi_L(\text{FINISH}) = m + 1$, the position of each step of $N$ is the same in $L_1$ and $L_2$. Call it $\psi(s)$. It is one to one, since $L_1$ puts distinct steps at distinct positions.

*If $f$ is a threat $(k, i \xrightarrow{p} j)$* with $r_1 = (k \prec i)$ and $r_2 = (j \prec k)$, then $\psi(k) < \psi(i)$ from $L_1$ and $\psi(k) > \psi(j) > \psi(i)$ from $L_2$, a contradiction.

*If $f$ is an open condition $(p, j)$*, let $q$ be the last position before $\psi(j)$ in $\tau$ that adds $p$. In $P_1$ the unique link into $(p, j)$ is the one made by $r_1$; by Lemma 6 its producer sits at position $q$ in $L_1$. The same holds for $r_2$ in $L_2$. If $r_1$ and $r_2$ both link from existing steps $i_1 \ne i_2$ of $N$, then $\psi(i_1) = q = \psi(i_2)$, against $\psi$ being one to one. If $r_1$ links from an existing step $i_1$ and $r_2$ from a new step $s_2$, then in $L_2$ both $i_1$ (at $\psi(i_1) = q$, using $L_1$) and $s_2$ sit at position $q$, which is impossible. If both make new steps, of actions $c_1 \ne c_2$, then the action at position $q$ of $\tau$ is both $c_1$ and $c_2$. Every case is a contradiction. $\square$

**Theorem.** SNLP returns a complete plan whose every linearization is a plan, with the fewest steps of any plan, if a plan exists, and it returns failure otherwise. The complete plans that one bounded search can return have pairwise disjoint sets of action sequences.

*Proof.* Lemma 1 gives soundness. If a plan exists, let $L^*$ be the length of a shortest one; by Lemma 3 it uses only filtered actions and $L^* \le 2^{|F|} - 1$. A round $n < L^*$ cannot succeed, since its plan would give a plan with fewer than $L^*$ actions; it does not stop the loop at line L5, since by Lemma 5 that would make the round $L^*$ fail, against Lemma 4. So line L1 reaches the round $L^*$, which succeeds by Lemma 4 and returns a plan of exactly $L^*$ steps. If no plan exists, no round returns a plan, and the loop ends at line L5 or L6 after finitely many rounds by Lemma 2. The last claim is Lemma 7. $\square$

Lemma 7 fails for POP. There a step that adds $p$ may sit between the ends of a link on $p$, Lemma 6 fails, and the sequence no longer fixes the producer of each link. The example of the page shows it: the sequence AARS is a linearization of three different complete POP plans.
