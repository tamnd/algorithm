---
tag: 8WWSGW
kind: model
slug: nondeterministic-turing-machine
name: Nondeterministic Turing machine
aliases:
- NTM
area: foundations/models-of-computation
level: core
summary: Turing machine with multiple allowed transitions; accepts if some computation path accepts.
prereqs: [turing-machine, multitape-turing-machine]
see_also: [np, p, np-complete, cook-levin-theorem, multitape-simulation-theorem, savitch-theorem, pspace, exptime]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 3.2 (nondeterministic Turing machines) and Section 7.3 (the class NP)
  - book: isbn:9780521424264
    title: "Sanjeev Arora and Boaz Barak, Computational Complexity: A Modern Approach"
    locator: Chapter 2, Section 2.1 (the class NP), including Section 2.1.2 (nondeterministic Turing machines)
  - book: isbn:9780201530827
    title: Christos H. Papadimitriou, Computational Complexity, Addison-Wesley, 1994
    locator: Section 2.7 (nondeterministic machines)
---

A nondeterministic Turing machine is a [Turing machine](/turing-machine/) whose transition function gives a set of possible moves, so a configuration can have several successors. It accepts an input when at least one of its computation paths reaches the accept state. Its running time is the length of its longest path. The class [NP](/np/) is the set of languages that such a machine decides in polynomial time, and the best known deterministic simulation takes time exponential in the running time. Whether this loss can be avoided is open, and it is the P versus NP question.

## The machine

A nondeterministic machine $N$ has the same parts as the one-tape machine of the [Turing machine](/turing-machine/) page, except for the transition function. Its states $Q$ include a start state $q_0$, *accept* and *reject*. Its tape alphabet is $\Gamma \ni \sqcup$, its input alphabet is $\Sigma$, and

$$
\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma \to \mathcal{P}(Q \times \Gamma \times \{L, R\}),
$$

where $\mathcal{P}$ is the power set. The set $\delta(q, a)$ is finite and can be empty. Let $b = \max_{q,a} |\delta(q,a)|$, and assume $b \ge 1$. Configurations are as for the deterministic machine. We write $C \vdash C'$ when $C'$ follows from $C$ by one move in $\delta(q, a)$. A configuration can have zero, one or up to $b$ successors.

A **computation path** on an input $w$ is a sequence $C_0 \vdash C_1 \vdash \cdots$ with $C_0 = q_0\,w$ that stops at a halting configuration (state accept or reject) or at a configuration with no successor, or else goes on without end. The paths form a tree, the **computation tree**, whose root is $C_0$ and whose nodes have at most $b$ children.

**Acceptance.** $N$ *accepts* $w$ if some computation path on $w$ ends in a configuration with state accept. The language of $N$ is $L(N) = \{ w \in \Sigma^* : N \text{ accepts } w\}$. The word $w$ is not in $L(N)$ when no path accepts: every path then rejects, stops without a successor, or runs forever. $N$ *decides* $L$ if $L(N) = L$ and every path on every input is finite. The rule is one-sided. A single accepting path is enough to accept, but all paths must fail to reject. The machine does not guess "correctly" in any physical sense. The definition says only that a good sequence of choices exists.

**Example.** Let $L_3$ be the set of words over $\{0,1\}$ whose third symbol from the right is $1$. The machine $N_3$ below guesses the position of that $1$. In state $q_0$ it scans right, and when it reads a $1$ it may either go on in $q_0$ or commit to this $1$ by entering $q_1$. After the commit it reads two more symbols, then needs a blank. A pair that the table does not list has $\delta(q, a) = \emptyset$.

| State | Reads | Choices $(\text{next state}, \text{write}, \text{move})$ |
|---|---|---|
| $q_0$ | $0$ | $(q_0, 0, R)$ |
| $q_0$ | $1$ | $(q_0, 1, R)$ or $(q_1, 1, R)$ |
| $q_1$ | $0$ or $1$ | $(q_2, \text{the same symbol}, R)$ |
| $q_2$ | $0$ or $1$ | $(q_3, \text{the same symbol}, R)$ |
| $q_3$ | $\sqcup$ | (accept, $\sqcup$, $R$) |

On $0110$ the computation tree has three paths. The path that commits at the second symbol accepts after 5 steps. The two paths that stay in $q_0$ at the second symbol both stop without a successor after 4 steps. So $N_3$ accepts $0110$, and indeed the third symbol from the right is $1$. On $0000$ the only path stops after 4 steps, so $N_3$ rejects. Every path on a word of length $n$ has at most $n + 1$ steps. So $N_3$ decides $L_3$ in time $n + 1$.

## What it counts

The **time** of a path is its number of steps. $N$ runs in time $t(n)$ if, for every input of length $n$, every computation path has at most $t(n)$ steps. In particular $N$ halts on every path. This is the measure of Sipser: the longest path of the tree, not the shortest accepting path. It is the measure of this page. For a function $t$, $\mathrm{NTIME}(t(n))$ is the set of languages that some nondeterministic multitape machine decides in time $O(t(n))$. The class $\mathrm{NP}$ is

$$
\mathrm{NP} = \bigcup_{k \ge 1} \mathrm{NTIME}(n^k).
$$

The **space** of a path is the number of distinct cells that the head visits, and the space of $N$ is the largest over all paths. The cost of a run does not add the costs of the branches: the paths are alternative runs, not parallel work that you pay for.

A nondeterministic machine is not a probabilistic machine. It assigns no probability to its paths, and it has no error. It also does not model a real parallel computer, because the number of branches can be exponential in the time.

## Relation to other models

Every deterministic machine is a nondeterministic machine with $|\delta(q,a)| = 1$ for all $q, a$, so $\mathrm{DTIME}(t) \subseteq \mathrm{NTIME}(t)$. The multitape version has the transition function $\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma^k \to \mathcal{P}(Q \times \Gamma^k \times \{L,R,S\}^k)$. The one-tape simulation of the [multitape Turing machine](/multitape-turing-machine/) page carries over to the nondeterministic case: the machine makes its choice at the step where the deterministic simulation applies $\delta$. So the polynomial-time classes do not depend on the number of tapes.

**Theorem (deterministic simulation).** Let $N$ be a nondeterministic machine that runs in time $t(n)$, where $t(n) \ge n$ for all $n$, and let $L = L(N)$. Then a deterministic multitape machine $D$ decides $L$ in time $2^{O(t(n))}$. A deterministic one-tape machine decides $L$ in time $2^{O(t(n))}$ too. Hence $\mathrm{NTIME}(t(n)) \subseteq \bigcup_{c \ge 1} \mathrm{DTIME}(2^{c\,t(n)})$.

*Proof.* Take $N$ with one tape and $b$ as above. Number the elements of each set $\delta(q,a)$ as $1, \ldots, |\delta(q,a)|$. A string $c = c_1 \cdots c_\ell \in \{1, \ldots, b\}^\ell$ is a list of choices. The **run along $c$** starts in $C_0$ and does this for $i = 1, \ldots, \ell$. If the configuration is halting or has $|\delta(q,a)| < c_i$ (this includes $\delta(q,a) = \emptyset$), the run stops. Else it makes move number $c_i$ of $\delta(q,a)$. The **status** of the run is *accept* if it stops in, or ends in, a configuration with state accept. It is *alive* if it makes all $\ell$ moves and the last configuration is not halting. Else it is *dead*.

The machine $D$ has three tapes: the input, a work tape on which it simulates $N$, and a tape that holds the string $c$. For $\ell = 0, 1, 2, \ldots$ in turn, and for each $c \in \{1,\ldots,b\}^\ell$ in lexicographic order, $D$ performs the run along $c$. It copies the input to the work tape, then simulates the moves with the help of $c$. Then it erases the work tape. If a run has status accept, $D$ accepts. After all strings of length $\ell$, if no run was alive, $D$ rejects. Else it goes on with $\ell + 1$.

*Correctness.* Suppose $N$ accepts $w$. Some accepting path has $s$ steps and a list of choices $c \in \{1,\ldots,b\}^s$, and the run along $c$ has status accept. $D$ reaches level $s$ unless it accepts earlier. At each level it can reject only if no run is alive. A reject at level $\ell < s$ would mean that no run along a string of length $\ell$ is alive. But the first $\ell$ choices of the accepting path give a run of that length that makes all $\ell$ moves and is not halting, because $\ell < s$. So that run is alive. Hence $D$ does not reject before level $s$, and it accepts at level $s$ at the latest. Conversely, $D$ accepts only after a run of status accept, and that run is a real accepting path of $N$. So $D$ accepts $w$ if and only if $N$ accepts $w$, as long as $D$ halts.

Suppose $N$ does not accept $w$. At level $\ell = t(n) + 1$ no run is alive: an alive run is a path of $N$ with $t(n) + 1$ steps whose last configuration is not halting, and no path has more than $t(n)$ steps. So $D$ halts at level $t(n)+1$ at the latest. It does not accept, because no run has status accept. It rejects.

*Time.* $D$ stops by level $t(n) + 1$. The number of strings it tries is at most $\sum_{\ell=0}^{t(n)+1} b^\ell \le (t(n)+2)\, b^{t(n)+1}$. For each string, $D$ spends $O(n)$ steps to copy the input, $O(\ell)$ steps to simulate the moves (each move is a constant number of steps), $O(n + \ell)$ steps to erase the work tape, and $O(\ell)$ steps to produce the next string. This is $O(t(n))$ steps in all, since $n \le t(n)$ and $\ell \le t(n)+1$. The total is $O(t(n)^2\, b^{t(n)+1}) = 2^{O(t(n))}$, because $b$ is a constant and $t(n)^2 \le 2^{2 t(n)}$ for $t(n) \ge 1$. A one-tape machine simulates $D$ with a square of this time (the claim of the multitape page), and $(2^{O(t)})^2 = 2^{O(t)}$. A machine with more tapes is simulated in the same way, with $O(1)$ steps for each of its moves. $\blacksquare$

**Theorem (recognizers).** For every nondeterministic machine $N$ there is a deterministic machine $D$ with $L(D) = L(N)$. If every path of $N$ is finite on every input, $D$ can be made a decider.

*Proof.* Let $D$ be the machine of the proof above, with this change: it stops with accept when a run has status accept, and otherwise it goes on to level $\ell + 1$ while some run is alive, and it rejects when a level has no alive run. If $N$ accepts $w$, the argument above shows that $D$ accepts $w$ at level $s$ at the latest, even when other paths of $N$ run forever, because the search is by level and so is breadth first. If $N$ does not accept $w$, then $D$ never accepts, and it either rejects or runs forever, so $L(D) = L(N)$. Now suppose that every path of $N$ on $w$ is finite. The computation tree is finitely branching with no infinite path, so by König's lemma it is finite. Then it has some depth $h$, and no run is alive at level $h + 1$, so $D$ halts. Hence $D$ decides $L(N)$. $\blacksquare$

The same simulation shows $\mathrm{NTIME}(t(n)) \subseteq \mathrm{DSPACE}(t(n))$ for $t(n) \ge n$, when the space counts the cells of all tapes. The work tape and the string $c$ have $O(t(n))$ cells, and $D$ reuses them for each run. The [Savitch theorem](/savitch-theorem/) is a separate result about nondeterministic space.

## Known results in the model

- **NP.** $\mathrm{NP} = \bigcup_k \mathrm{NTIME}(n^k)$. A language $L$ is in NP if and only if there are polynomials $p, q$ (with natural-number coefficients) and a deterministic machine $V$ such that $V$ runs in time $q(|x| + |y|)$ and $L = \{ x : \exists y,\ |y| \le p(|x|) \text{ and } V \text{ accepts } (x, y) \}$. The string $y$ is a [certificate](/certificate/), and $V$ is a *verifier*. The proof is below.
- **Place of NP.** $\mathrm{P} \subseteq \mathrm{NP}$, because a deterministic machine is a nondeterministic machine. By the theorem above, $\mathrm{NP} \subseteq \mathrm{EXP}$ and $\mathrm{NP} \subseteq \mathrm{PSPACE}$. See [P](/p/), [PSPACE](/pspace/) and [EXPTIME](/exptime/). Whether $\mathrm{P} = \mathrm{NP}$ is open.
- **Complete problems.** The [Cook-Levin theorem](/cook-levin-theorem/) shows that [SAT](/sat/) is [NP-complete](/np-complete/). SAT is in NP because a machine can guess an assignment of the variables and check it in polynomial time.
- **Acceptance is not symmetric.** [coNP](/co-np/) is the class of complements of languages in NP. The definition gives no machine for it, because "no path accepts" is a universal statement. Whether $\mathrm{NP} = \mathrm{coNP}$ is open.

*Proof of the certificate characterization.* Here $p$ is a polynomial with natural-number coefficients, and $q$ is a polynomial. Assume that $L \in \mathrm{NP}$. Let $N$ decide $L$ with every path of at most $r(n)$ steps, where $r$ is a polynomial. Let $V$ be the machine that, on $(x, y)$ with $y \in \{1, \ldots, b\}^*$ coded in binary, runs $N$ on $x$ and uses $y_i$ as the choice at step $i$. $V$ rejects if a choice is out of range, if $y$ ends before $N$ halts, or if $N$ halts in reject. $V$ accepts if $N$ reaches accept. The run takes $O(r(|x|))$ steps on a multitape machine. If $x \in L$, an accepting path has at most $r(|x|)$ steps, and its list of choices is a certificate of length $O(r(|x|))$. If $V$ accepts $(x, y)$, the run is an accepting path of $N$, so $x \in L$.

Conversely, assume that $V$, $p$ and $q$ are as stated. Let $(x, y)$ be coded as $x$, a separator symbol, then $y$, and measure the time of $V$ in $|x| + |y|$. Let $N$ work in three stages on an input $x$ of length $n$. First it writes $p(n)$ ones on a work tape. This is deterministic and takes time polynomial in $n$, because $p$ is a fixed polynomial with natural-number coefficients. Second it writes a string $y$ on another tape, symbol by symbol. At each step it chooses among writing $0$, writing $1$ and stopping, and it counts its symbols against the ones so that it stops after $p(n)$ symbols at the latest. Third it simulates $V$ on the coded pair $(x, y)$, which has length at most $n + p(n) + 1$, and accepts if and only if $V$ accepts. Each path has polynomially many steps, because $|y| \le p(n)$ and the third stage takes at most $q(n + p(n) + 1)$ simulated steps. A path accepts if and only if its string $y$ makes $V$ accept. So $N$ accepts $x$ if and only if some $y$ with $|y| \le p(n)$ makes $V$ accept, that is, if and only if $x \in L$. Hence $L \in \mathrm{NP}$. $\blacksquare$

## References
