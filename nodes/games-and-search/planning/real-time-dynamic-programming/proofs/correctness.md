---
title: With a monotone admissible start, RTDP trials end and the values converge to the optimal costs on the relevant states
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page and these assumptions.

- **(S1)** The state set is finite, each state has a finite set of actions, and each action has a cost $c(s, a) \ge c_{\min} > 0$.
- **(S2)** From every state that some policy can reach from $s_0$, there is a proper policy, so the optimal cost $V^*$ is finite there. By the [stochastic shortest path](/stochastic-shortest-path/) theorem, $V^* = T V^*$ on these states, where $(TV)(s) = \min_a Q_V(s, a)$ and $Q_V(s, a) = c(s, a) + \sum_{s'} P(s' \mid s, a) V(s')$, with $V = 0$ on $G$.
- **(S3)** The start values are admissible, $h \le V^*$, and monotone, $h \le T h$, with $h = 0$ on $G$. The function $h = 0$ has both properties, and so has the function $h_{\min}$ of the implementation.

Write $V_t$ for the table after $t$ backups, with $V_t(s) = h(s)$ for a state that has no entry yet. Line L1 gives a state its value $h(s)$ when it is first seen, so this convention describes the table exactly.

**Lemma 1 (the values stay admissible and monotone, and only rise).** For every $t$: $V_t \le V^*$, $V_t \le T V_t$, and $V_{t+1} \ge V_t$.

*Proof.* By induction on $t$. For $t = 0$ this is (S3). Suppose that it holds for $V_t$, and that the backup $t + 1$ is at the state $s$. Line L6 sets $V_{t+1}(s) = (T V_t)(s)$, and $V_{t+1} = V_t$ elsewhere. Because $V_t(s) \le (T V_t)(s)$, the value at $s$ does not go down, so $V_{t+1} \ge V_t$. The operator $T$ is monotone: if $V \le W$ then $TV \le TW$, since each $Q_V(s, a)$ is a sum of $c(s, a)$ and of the values $V(s')$ with nonnegative weights. Hence $T V_{t+1} \ge T V_t$. At a state $u \ne s$ this gives $V_{t+1}(u) = V_t(u) \le (T V_t)(u) \le (T V_{t+1})(u)$. At $s$ it gives $V_{t+1}(s) = (T V_t)(s) \le (T V_{t+1})(s)$. Finally $V_{t+1}(s) = (T V_t)(s) \le (T V^*)(s) = V^*(s)$ by monotonicity and (S2). $\square$

So each value $V_t(s)$ is a non-decreasing sequence bounded by $V^*(s)$, and it has a limit $V_\infty(s) \le V^*(s)$.

**Lemma 2 (closed sets cost something).** Let $C$ be a nonempty set of non-goal states, and let $\mu$ pick at each $s \in C$ an action all of whose outcomes are in $C$. Then no function $W$ on $C$ satisfies $W(s) = c(s, \mu(s)) + \sum_{s'} P(s' \mid s, \mu(s)) W(s')$ for all $s \in C$.

*Proof.* The policy $\mu$ defines a [Markov chain](/markov-chain/) on the finite set $C$. It has a [stationary distribution](/stationary-distribution/) $\pi$ on $C$. Multiply the equation at $s$ by $\pi(s)$ and add over $s \in C$. The terms with $W$ are equal on both sides, because $\pi$ is stationary, and what remains is $0 = \sum_{s \in C} \pi(s) c(s, \mu(s)) \ge c_{\min} > 0$, a contradiction. $\square$

We use one fact from probability. If, during one run, a state $s$ is visited infinitely often and the action $a$ is taken at infinitely many of these visits, then with probability 1 each outcome $s'$ with $P(s' \mid s, a) > 0$ follows infinitely many of them. This holds because the outcomes of the visits are independent draws from $P(\cdot \mid s, a)$, so the second Borel-Cantelli lemma applies, in the form for conditionally independent events.

**Lemma 3 (each trial ends).** With probability 1, the loop of line L4 stops.

*Proof.* Suppose that a trial runs forever. Let $C$ be the set of states that it visits infinitely often, and for $s \in C$ let $B(s)$ be the set of actions that it takes at $s$ infinitely often. Both sets are nonempty, because the state and action sets are finite. By the fact above, with probability 1, every outcome of every action in $B(s)$ is in $C$; it is not in $G$, because the trial would stop there. Take $a \in B(s)$ and a sequence of times at which line L5 picks $a$ at $s$. At these times $V_{t+1}(s) = Q_{V_t}(s, a)$, and as $t \to \infty$ both sides converge, to $V_\infty(s)$ and to $Q_{V_\infty}(s, a)$. So $V_\infty(s) = Q_{V_\infty}(s, a)$ for every $s \in C$ and $a \in B(s)$. Choose one $\mu(s) \in B(s)$ for each $s \in C$. Then $V_\infty$ restricted to $C$ solves the equation of Lemma 2 for $\mu$, which is not possible. So an infinite trial has probability 0. $\square$

**Theorem.** With probability 1, let $C$ be the set of states that infinitely many trials visit. Then $s_0 \in C$, $V_t(s) \to V^*(s)$ for every $s \in C$, every action that infinitely many trials take at a state of $C$ is optimal there, and after some trial every trial follows an optimal proper policy from $s_0$.

*Proof.* By Lemma 3 every trial ends, so the run consists of infinitely many trials. Every trial starts at $s_0$, so $s_0 \in C$. For $s \in C$ let $B(s)$ be the set of actions taken at $s$ in infinitely many trials; it is not empty, because the action set is finite. Take $a \in B(s)$. It is taken at $s$ infinitely often, so by the fact above each of its outcomes follows infinitely often. Each trial is finite, so these occurrences fall in infinitely many trials, and every outcome of $a$ is in $C \cup G$. As in Lemma 3, $V_\infty(s) = Q_{V_\infty}(s, a)$ for all $a \in B(s)$.

Each action in $B(s)$ is also greedy in the limit. At the times when $a$ is picked, $Q_{V_t}(s, a) \le Q_{V_t}(s, b)$ for every action $b$, and both sides converge, so $Q_{V_\infty}(s, a) \le Q_{V_\infty}(s, b)$. Hence $V_\infty(s) = \min_b Q_{V_\infty}(s, b) = (T V_\infty)(s)$ on $C$.

Choose $\mu(s) \in B(s)$ for each $s \in C$. The policy $\mu$ keeps the process in $C \cup G$. It reaches $G$ with probability 1 from every state of $C$: otherwise the chain of $\mu$ on $C$ would have a closed set $C' \subseteq C$ that does not meet $G$, and $V_\infty$ on $C'$ would solve the equation of Lemma 2. So $\mu$ is proper on $C$, and its cost $V_\mu$ is the unique solution on $C$ of $W(s) = Q_W(s, \mu(s))$. The function $V_\infty$ solves the same system, so $V_\infty = V_\mu$ on $C$. Then $V^* \le V_\mu = V_\infty \le V^*$ on $C$, so $V_\infty = V^*$ on $C$. This holds for every choice of $\mu$, so each action in $B(s)$ is optimal at $s$, and every such $\mu$ is an optimal proper policy from each state of $C$.

Each state outside $C$ is visited in only finitely many trials, and each action outside $B(s)$ is taken at $s$ in only finitely many trials. There are finitely many such states and actions, so there is a trial $K$ after which no trial visits a state outside $C$ or takes an action outside $B(s)$. From trial $K$ on, every trial moves by actions of an optimal proper policy. $\square$

The theorem says nothing about states outside $C$. Their values are lower bounds that need not be close to $V^*$, and the greedy policy there need not be optimal.

**Remarks.** Barto, Bradtke and Singh (1995) prove convergence on the relevant states for any admissible start, without the monotone condition (S3), and under the general assumptions of Bertsekas and Tsitsiklis in place of positive costs. Monotonicity is used above only to make the values rise, which gives the limits $V_\infty$ at once. Without (S3), a backup can lower a value, and the proof needs the argument of asynchronous value iteration instead. The theorem does not give a bound on the number of trials. Labeled RTDP adds a test that marks a state as solved, and so gives a stopping rule.
