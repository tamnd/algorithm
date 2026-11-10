---
tag: 4P69AP
kind: theorem
slug: blumofe-leiserson-bound
name: Blumofe-Leiserson bound
aliases:
- randomized work-stealing bound
- work-stealing theorem
area: parallel/work-span-models
level: advanced
summary: Randomized work stealing runs a fully strict computation in expected time T_1/p + O(T_infinity), with O(p T_infinity) expected steal attempts and space at most p S_1.
prereqs: [work-stealing, work-span-model, greedy-scheduling, markov-inequality, balls-into-bins]
see_also: [brent-theorem, greedy-scheduling, work-law, span-law, parallel-slackness, arora-blumofe-plaxton-deque, chernoff-bound, fork-join-model]
sources:
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: Section 4, Lemma 4 (structural lemma) and Theorem 5 (space); Section 5, Lemma 6 (the recycling game); Section 6, Lemma 12 (steal attempts), Theorem 13 (time) and Theorem 14 (communication). Theorem numbers taken from the author preprint, to be checked against the journal pages
  - paper: doi:10.1145/277651.277678
    title: "Nimar S. Arora, Robert D. Blumofe and C. Greg Plaxton, Thread scheduling for multiprogrammed multiprocessors, SPAA 1998"
    locator: Section 3.4, Lemma 3 (structural lemma); Section 4.2, the potential function, Lemma 6 (top-heavy deques), Lemma 7 (balls and weighted bins) and Lemma 8; Section 4.3, Theorem 9 (dedicated environments)
  - paper: "Nimar S. Arora, Robert D. Blumofe and C. Greg Plaxton, Thread scheduling for multiprogrammed multiprocessors, Theory of Computing Systems 34(2), 2001"
    locator: the journal version of the SPAA 1998 paper, pp. 115-144
---

The Blumofe-Leiserson bound is the theorem that randomized [work stealing](/work-stealing/) runs a fully strict multithreaded computation with work $T_1$ and span $T_\infty$ on $P$ processors in expected time $T_1/P + O(T_\infty)$. The same paper bounds the steal attempts by $O(P\,T_\infty)$ in expectation, the space by $S_1 P$, and the communication by $O(P\,T_\infty(1 + n_d)S_{max})$ in expectation. Since every schedule needs time at least $\max(T_1/P, T_\infty)$, the bound shows that a simple distributed scheduler is within a constant factor of optimal in expectation.

## Statement

The notation is that of the [work-span model](/work-span-model/).

| Symbol | Meaning |
|---|---|
| $n$ | the input size of the program |
| $P$ (or $p$) | the number of processors |
| $W = T_1$ | the work: the number of unit-time instructions |
| $S = T_\infty$ | the span (critical-path length) |
| $T_P$ | the running time on $P$ processors |
| $W/S$ | the [parallelism](/parallelism/) |
| $S_1$ | the stack depth: the space of a serial run |

A multithreaded computation is *fully strict* when each join edge goes from a thread to its parent thread. Programs in the [fork-join model](/fork-join-model/), with spawn and sync, give fully strict computations. The scheduler is the Work-Stealing Algorithm of Blumofe and Leiserson: each processor works at the bottom of its own ready deque, puts the parent on the bottom of its deque when the running thread spawns a child, and, when its deque is empty, steals the top thread of the deque of a processor chosen uniformly at random. The machine is the *atomic-access model*: each steal attempt is one access to the victim's deque, and concurrent accesses to one deque are served one at a time in an order that an adversary chooses.

**Theorem (Blumofe and Leiserson 1999).** Consider any fully strict multithreaded computation with work $T_1$, critical-path length $T_\infty$ and stack depth $S_1$, run by the Work-Stealing Algorithm on $P$ processors in the atomic-access model.

1. *(Time, Theorem 13.)* The expected running time, with the scheduling overhead included, is $T_1/P + O(T_\infty)$. For each $\varepsilon > 0$, with probability at least $1 - \varepsilon$, the running time is $T_1/P + O(T_\infty + \lg P + \lg(1/\varepsilon))$.
2. *(Steal attempts, Lemma 12.)* The expected number of steal attempts is $O(P\,T_\infty)$. For each $\varepsilon > 0$, with probability at least $1 - \varepsilon$, at most $O(P(T_\infty + \lg(1/\varepsilon)))$ steal attempts occur.
3. *(Space, Theorem 5.)* The space is at most $S_1 P$, in every run.
4. *(Communication, Theorem 14.)* If a join edge carries $O(1)$ bytes, the expected total communication is $O(P\,T_\infty(1 + n_d)S_{max})$ bytes, where $n_d$ is the largest number of join edges from a thread to its parent and $S_{max}$ is the size of the largest activation frame. With probability at least $1 - \varepsilon$ it is $O(P(T_\infty + \lg(1/\varepsilon))(1 + n_d)S_{max})$.

The constants in the $O$ terms do not depend on the computation or on $P$. Blumofe and Leiserson note that with a sharper bound of Plaxton for the contention, the high-probability time becomes $T_1/P + O(T_\infty)$ whenever $1/\varepsilon$ is at most polynomial in $P$ and in the number of steal attempts. Arora, Blumofe and Plaxton (Theorem 9) prove for their non-blocking work stealer in a dedicated machine an expected time of $O(T_1/P + T_\infty)$ and a time of $O(T_1/P + T_\infty + \lg(1/\varepsilon))$ with probability at least $1 - \varepsilon$, with no $\lg P$ term.

## In plain words

A program splits its work into many small tasks, and the scheduler hands them to the processors. Work stealing has no boss: a processor with nothing to do picks another processor at random and takes its oldest waiting task.

The theorem says that this is close to the best possible. The time is the total work divided among the processors, plus a cost for the steals. On average this extra cost is only a constant times the length of the longest chain of tasks that must run one after another. No scheduler can beat that chain or the even split of the work. So when the program has much more parallel work than processors, the time is close to a perfect split. The memory grows at most in proportion to the number of processors, and the communication is small too.

## Proof

We give a **sketch** of the time bound and the bound on steal attempts. It follows the potential-function argument of Arora, Blumofe and Plaxton, in the synchronous step model of the [work stealing](/work-stealing/) page: the DAG has unit-time nodes, each node has at most two successors, and in each step each processor either executes its assigned node or makes one steal attempt at a uniform random victim. In this model the $\lg P$ term of the atomic-access model does not appear. Blumofe and Leiserson prove their theorem with a different method, a delay-sequence argument together with a bound on the contention at the deques (their Lemmas 6, 9 and 12). The space bound has a short full proof, at the end.

**Step 1: accounting.** In each step, each processor executes a node or makes a steal attempt. So $P \cdot T_P = T_1 + A$, where $A$ is the number of steal attempts, and $T_P = T_1/P + A/P$. It remains to show $\mathrm{E}[A] = O(P\,T_\infty)$.

**Step 2: weights and potential.** When a node $v$ becomes enabled, the predecessor that was executed last is its *designated parent*. These edges form the *enabling tree*. Let $d(v)$ be the depth of $v$ in this tree and define the *weight* $w(v) = T_\infty - d(v)$. A path in the enabling tree is a path in the DAG, so $d(v) \le T_\infty - 1$ and $w(v) \ge 1$. Give each ready node $v$ the potential $3^{2w(v) - 1}$ if it is assigned to a processor, and $3^{2w(v)}$ if it is in a deque. Let $\Phi$ be the total. At the start, $\Phi = 3^{2T_\infty - 1}$. At the end, $\Phi = 0$, and while the run is not over, $\Phi \ge 3$.

**Step 3: the potential never increases.** Only three events change $\Phi$.

- An assigned node $u$ of weight $w$ is executed and enables two nodes. Both have weight $w - 1$: one is assigned, one goes to the deque. The potential goes from $3^{2w-1}$ to $3^{2w-3} + 3^{2w-2} = \tfrac{4}{9}\,3^{2w-1}$, a drop of $\tfrac59$ of the potential of $u$. With one enabled node or none, the drop is larger.
- A node moves from a deque to a processor (a pop or a steal). Its potential goes from $3^{2w}$ to $3^{2w-1}$, a drop of $\tfrac23$ of its potential.
- Nothing else changes a ready node.

**Step 4: structural lemma and top-heavy deques.** Let $v_0$ be the node assigned to a processor and $v_1, \ldots, v_k$ its deque from bottom to top. By induction on the steps, $w(v_0) \le w(v_1) < w(v_2) < \cdots < w(v_k)$ (ABP, Lemma 3). So $w(v_j) \le w(v_k) - (k - j)$ for $1 \le j \le k$, and $w(v_0) \le w(v_k) - (k - 1)$. The potential of the processor other than its top node is therefore

$$3^{2w(v_0) - 1} + \sum_{j=1}^{k-1} 3^{2w(v_j)} \le 3^{2w(v_k)}\Big(\frac{1}{3 \cdot 9^{k-1}} + \sum_{i=1}^{k-1} 9^{-i}\Big).$$

For $k = 1$ the bracket is $\tfrac13$. For $k \ge 2$ it is at most $\tfrac{1}{27} + \tfrac18 < \tfrac13$. So the top node holds at least $\tfrac34$ of the potential of its processor (ABP, Lemma 6).

**Step 5: balls into weighted bins.** Throw $P$ balls independently into $P$ bins, where each ball lands in each bin $q$ with probability at least $1/P$. Let bin $q$ have weight $W_q \ge 0$, let $W = \sum_q W_q$, and let $X$ be the total weight of the bins that get at least one ball. Then $\mathrm{E}[W - X] \le \sum_q W_q (1 - 1/P)^P < W/e$. By [Markov's inequality](/markov-inequality/) applied to $W - X \ge 0$, for each $0 < \beta < 1$,

$$\Pr[X < \beta W] = \Pr[W - X > (1 - \beta) W] < \frac{1}{(1 - \beta)e}.$$

With $\beta = \tfrac12$, $\Pr[X \ge W/2] > 1 - 2/e > \tfrac14$ (ABP, Lemma 7). In our model a thief picks among the other $P - 1$ processors, and the thief's own bin has weight 0, so each ball hits each bin of positive weight with probability $1/(P-1) \ge 1/P$.

**Step 6: one phase.** Split the run into *phases*: a phase starts at a step and ends at the first step at which at least $P$ steal attempts have occurred since its start. Each step has at most $P$ attempts, so a phase has fewer than $2P$ attempts. Look at the start of a phase, and let $\Phi(q)$ be the potential of the nodes of processor $q$ (its assigned node and its deque). Split the processors into the set $\mathcal{A}$ of those with an assigned node and an empty deque, and the set $\mathcal{D}$ of those with a nonempty deque; the others have no potential. For $q \in \mathcal{A}$, the assigned node is executed in the first step of the phase, so $q$'s potential drops by at least $\tfrac59 \Phi(q)$. For $q \in \mathcal{D}$, let $u_q$ be its top node. If any attempt in the phase targets $q$, then $u_q$ has left the deque by the end of that attempt, because pushes go to the bottom and only a pop or a steal removes $u_q$. So the potential of $u_q$ drops by at least $\tfrac23 \Phi(u_q) \ge \tfrac23 \cdot \tfrac34 \Phi(q) = \tfrac12 \Phi(q)$. These drops belong to different nodes, and the potential of a node together with the nodes that it later enables never grows (Step 3), so the drops add up. Step 5 with the bin weights $\Phi(q)$ for $q \in \mathcal{D}$ shows that with probability more than $\tfrac14$, the hit processors of $\mathcal{D}$ hold at least half of $\Phi(\mathcal{D})$. Then the phase cuts the potential by at least $\tfrac59 \Phi(\mathcal{A}) + \tfrac14 \Phi(\mathcal{D}) \ge \tfrac14 \Phi$. The probability bound holds for each history before the phase.

**Step 7: counting phases.** After $k$ phases that each cut $\Phi$ by a quarter, $\Phi \le (3/4)^k\, 3^{2T_\infty - 1}$. This is below 3, so the run is over, once $k \ge K = \lceil (2T_\infty - 2)\log_{4/3} 3 \rceil + 1 = O(T_\infty)$. Each phase succeeds with probability more than $\tfrac14$ given the past, so the expected number of phases before $K$ successes is less than $4K$. Each phase has fewer than $2P$ attempts, so $\mathrm{E}[A] < 8PK = O(P\,T_\infty)$. With Step 1, $\mathrm{E}[T_P] = T_1/P + O(T_\infty)$. A [Chernoff bound](/chernoff-bound/) on the number of successes in $O(T_\infty + \lg(1/\varepsilon))$ phases gives $A = O(P(T_\infty + \lg(1/\varepsilon)))$ and $T_P = T_1/P + O(T_\infty + \lg(1/\varepsilon))$ with probability at least $1 - \varepsilon$. $\square$ (end of the sketch)

**The space bound (full proof).** By the structural lemma of Blumofe and Leiserson (their Lemma 4), the threads in a processor's deque, from top to bottom, and then the thread that the processor runs, form a chain in which each thread is the parent of the next. So at each step, the live activation frames form a tree whose leaves are the threads that the processors run, and each leaf has a processor that works on it (the *busy-leaves* property). The frames on the path from the root to one leaf are one stack of the serial program, so they take at most $S_1$ space. There are at most $P$ leaves, so the frames take at most $S_1 P$ space. $\blacksquare$

## Consequences

- **Linear speedup with slackness.** If $T_1/T_\infty \ge cP$ for a large constant $c$, the expected time is $(T_1/P)(1 + O(1/c))$, so the expected [speedup](/speedup/) is close to $P$. This is the reason for the rule that a program needs [parallel slackness](/parallel-slackness/).
- **The work-first principle.** The bound charges the steal overhead to the $O(T_\infty)$ term, and the work term has no overhead. Frigo, Leiserson and Randall used this to design Cilk-5: make each spawn cheap, and move the cost of the scheduling onto the steals.
- **A practical form of Brent's theorem.** A [greedy scheduler](/greedy-scheduling/) gives $T_P \le T_1/P + T_\infty$ by [Brent's theorem](/brent-theorem/), but it needs a central view of all ready nodes. Work stealing gets the same bound in expectation, up to the constant in front of $T_\infty$, without a central queue.
- **Example.** For [P-FIB](/parallel-fibonacci/)(30), $T_1 = 5385073$ strands and $T_\infty = 60$. On $P = 64$ processors, $T_1/P \approx 84142$. The bound says the expected overhead term is a constant times 60, which is below one percent of the work term for any constant up to 14.

## Tightness

- **The time bound is optimal up to a constant factor.** Every schedule has $T_P \ge T_1/P$ by the [work law](/work-law/) and $T_P \ge T_\infty$ by the [span law](/span-law/), so $T_P \ge \max(T_1/P, T_\infty) \ge \tfrac12(T_1/P + T_\infty)$.
- **The $T_\infty$ term cannot go.** A chain of $T_\infty$ nodes takes $T_\infty$ steps on any number of processors, which is $T_1/P + (1 - 1/P)T_\infty$.
- **The coefficient of $T_1/P$ is exactly 1.** No hidden constant multiplies the work term in the bound of Blumofe and Leiserson. The bound of Arora, Blumofe and Plaxton is stated as $O(T_1/P + T_\infty)$ because their rounds have a constant number of instructions each.
- **Expectation, not every run.** Work stealing is not greedy, so a single unlucky run can be slow; the theorem bounds the mean and gives tail bounds. The term $\lg P$ in the high-probability bound of Blumofe and Leiserson comes from the contention at the deques in the atomic-access model.
- **Space and communication.** Blumofe and Leiserson state that the time, space and communication bounds are all existentially optimal within a constant factor. For the communication, some fully strict computations need $\Omega(P\,T_\infty(1 + n_d)S_{max})$ bytes under every schedule that achieves linear speedup; this follows from a lower bound of Wu and Kung for divide-and-conquer computations.

## History

Blumofe and Leiserson presented the randomized work-stealing algorithm and its bounds at FOCS 1994, and the journal version appeared in the Journal of the ACM in 1999. Their analysis uses a delay-sequence argument and a "recycling game" that models the contention of thieves at the deques. Arora, Blumofe and Plaxton (SPAA 1998, journal version 2001) gave a non-blocking work stealer for multiprogrammed systems, where the kernel can take processors away, and analysed it with the potential function used in the sketch above. Their analysis is now the common textbook route to the bound.

## References
