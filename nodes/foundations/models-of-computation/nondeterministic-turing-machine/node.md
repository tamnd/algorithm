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
  - paper: doi:10.1145/800157.805047
    title: Stephen A. Cook, The complexity of theorem-proving procedures, Proceedings of the 3rd Annual ACM Symposium on Theory of Computing (STOC 1971)
    locator: pp. 151 to 158
  - paper: "Leonid A. Levin, Universal sequential search problems, Problemy Peredachi Informatsii 9(3) (1973)"
    locator: pp. 115 to 116
  - paper: doi:10.1016/S0022-0000(70)80006-X
    title: Walter J. Savitch, Relationships between nondeterministic and deterministic tape complexities, Journal of Computer and System Sciences 4(2), 1970
    locator: pp. 177 to 192
  - paper: doi:10.1137/0217058
    title: Neil Immerman, Nondeterministic space is closed under complementation, SIAM Journal on Computing 17(5), 1988
    locator: pp. 935 to 938
  - paper: doi:10.1007/BF00299636
    title: Róbert Szelepcsényi, The method of forced enumeration for nondeterministic automata, Acta Informatica 26(3), 1988
    locator: pp. 279 to 284
  - paper: "Ronald V. Book, Sheila A. Greibach and Ben Wegbreit, Time- and tape-bounded Turing acceptors and AFLs, Journal of Computer and System Sciences 4(6) (1970)"
    locator: pp. 606 to 621 (two storage tapes are enough for a time-bounded nondeterministic acceptor)
  - paper: "Stephen A. Cook, A hierarchy for nondeterministic time complexity, Journal of Computer and System Sciences 7(4) (1973)"
    locator: pp. 343 to 353
  - paper: doi:10.1145/322047.322061
    title: Joel I. Seiferas, Michael J. Fischer and Albert R. Meyer, Separating nondeterministic time complexity classes, Journal of the ACM 25(1), 1978
    locator: pp. 146 to 167
  - paper: doi:10.1016/0304-3975(83)90015-4
    title: Stanislav Žák, A Turing machine time hierarchy, Theoretical Computer Science 26(3), 1983
    locator: pp. 327 to 333
  - paper: doi:10.1109/SFCS.1983.39
    title: Wolfgang J. Paul, Nicholas Pippenger, Endre Szemerédi and William T. Trotter, On determinism versus non-determinism and related problems, 24th Annual Symposium on Foundations of Computer Science (FOCS 1983)
    locator: pp. 429 to 438
---

A nondeterministic Turing machine is a [Turing machine](/turing-machine/) whose transition function gives a set of possible moves, so a configuration can have several successors. It accepts an input when at least one of its computation paths reaches the accept state. Its running time is the length of its longest path. The class [NP](/np/) is the set of languages that such a machine decides in polynomial time, and the best known deterministic simulation takes time exponential in the running time. Whether a polynomial loss is enough is the open [P](/p/) versus NP question.

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

On $0110$ the computation tree has three paths. The path that commits at the second symbol accepts after 5 steps. The path that commits at the third symbol reaches $q_2$ on the blank and stops after 4 steps. The path that never commits reaches the blank in $q_0$ and stops after 4 steps. So $N_3$ accepts $0110$, and indeed the third symbol from the right is $1$. On $0000$ the only path stops after 4 steps, so $N_3$ rejects. In general, $N_3$ accepts $w$ if and only if $|w| \ge 3$ and $w_{|w|-2} = 1$: an accepting path must commit on a $1$ and then read exactly two more symbols before the blank. Every move goes right, so every path on a word of length $n$ has at most $n + 1$ steps, and $N_3$ decides $L_3$ in time $n + 1$. A deterministic finite automaton for $L_3$ needs $8$ states, one for each possible content of the last three symbols, while $N_3$ has $4$ states that are not halting. The same guess-then-check pattern gives $L_k$ (the $k$-th symbol from the right is $1$) with $k + 1$ such states against $2^k$ deterministic ones. See [nondeterministic finite automaton](/nondeterministic-finite-automaton/).

## What it counts

The **time** of a path is its number of steps. $N$ runs in time $t(n)$ if, for every input of length $n$, every computation path has at most $t(n)$ steps. In particular $N$ halts on every path. This is the measure of Sipser: the longest path of the tree, not the shortest accepting path. It is the measure of this page. Some texts measure instead the shortest accepting path on each accepted input. For a time-constructible $t$ the two measures define the same class $\mathrm{NTIME}(t)$, because a machine can count its steps on a clock and reject at time $t(n)$. For a function $t$, $\mathrm{NTIME}(t(n))$ is the set of languages that some nondeterministic multitape machine decides in time $O(t(n))$. The class $\mathrm{NP}$ is

$$
\mathrm{NP} = \bigcup_{k \ge 1} \mathrm{NTIME}(n^k).
$$

The **space** of a path is the number of distinct cells that the head visits, and the space of $N$ is the largest over all paths. With a read-only input tape, $\mathrm{NSPACE}(s(n))$ is the set of languages that a nondeterministic machine decides with space $O(s(n))$ on its work tapes, and $\mathrm{NL} = \mathrm{NSPACE}(\log n)$. The cost of a run does not add the costs of the branches: the paths are alternative runs, not parallel work that you pay for.

A nondeterministic machine is not a probabilistic machine. It assigns no probability to its paths, and it has no error. It also does not model a real parallel computer, because the number of branches can be exponential in the time.

## Relation to other models

Every deterministic machine is a nondeterministic machine with $|\delta(q,a)| = 1$ for all $q, a$, so $\mathrm{DTIME}(t) \subseteq \mathrm{NTIME}(t)$. The multitape version has the transition function $\delta : (Q \setminus \{\text{accept}, \text{reject}\}) \times \Gamma^k \to \mathcal{P}(Q \times \Gamma^k \times \{L,R,S\}^k)$. The one-tape simulation of the [multitape Turing machine](/multitape-turing-machine/) page carries over to the nondeterministic case: the machine makes its choice at the step where the deterministic simulation applies $\delta$. So the polynomial-time classes do not depend on the number of tapes. For nondeterministic machines the loss is much smaller than a square: Book, Greibach and Wegbreit (1970) showed that a nondeterministic machine with any number of tapes that runs in time $t(n)$ has an equivalent nondeterministic machine with two tapes that runs in time $O(t(n))$. The machine guesses the whole sequence of moves and of scanned symbols, and then checks each tape against the guess, one tape at a time. The deterministic analogue, by Hennie and Stearns, loses a factor $\log t(n)$.

**Theorem (deterministic simulation).** Let $N$ be a nondeterministic machine that runs in time $t(n)$, where $t(n) \ge n$ for all $n$, and let $L = L(N)$. Then a deterministic multitape machine $D$ decides $L$ in time $2^{O(t(n))}$. A deterministic one-tape machine decides $L$ in time $2^{O(t(n))}$ too. Hence $\mathrm{NTIME}(t(n)) \subseteq \bigcup_{c \ge 1} \mathrm{DTIME}(2^{c\,t(n)})$.

*Proof.* Take $N$ with one tape and $b$ as above. Number the elements of each set $\delta(q,a)$ as $1, \ldots, |\delta(q,a)|$. A string $c = c_1 \cdots c_\ell \in \{1, \ldots, b\}^\ell$ is a list of choices. The **run along $c$** starts in $C_0$ and does this for $i = 1, \ldots, \ell$. If the configuration is halting or has $|\delta(q,a)| < c_i$ (this includes $\delta(q,a) = \emptyset$), the run stops. Else it makes move number $c_i$ of $\delta(q,a)$. The **status** of the run is *accept* if it stops in, or ends in, a configuration with state accept. It is *alive* if it makes all $\ell$ moves and the last configuration is not halting. Else it is *dead*.

The machine $D$ has three tapes: the input, a work tape on which it simulates $N$, and a tape that holds the string $c$. For $\ell = 0, 1, 2, \ldots$ in turn, and for each $c \in \{1,\ldots,b\}^\ell$ in lexicographic order, $D$ performs the run along $c$. It copies the input to the work tape, then simulates the moves with the help of $c$. Then it erases the work tape. If a run has status accept, $D$ accepts. After all strings of length $\ell$, if no run was alive, $D$ rejects. Else it goes on with $\ell + 1$.

*Correctness.* Suppose $N$ accepts $w$. Some accepting path has $s$ steps and a list of choices $c \in \{1,\ldots,b\}^s$, and the run along $c$ has status accept. $D$ reaches level $s$ unless it accepts earlier. At each level it can reject only if no run is alive. A reject at level $\ell < s$ would mean that no run along a string of length $\ell$ is alive. But the first $\ell$ choices of the accepting path give a run of that length that makes all $\ell$ moves and is not halting, because $\ell < s$. So that run is alive. Hence $D$ does not reject before level $s$, and it accepts at level $s$ at the latest. Conversely, $D$ accepts only after a run of status accept, and that run is a real accepting path of $N$. So $D$ accepts $w$ if and only if $N$ accepts $w$, as long as $D$ halts.

Suppose $N$ does not accept $w$. At level $\ell = t(n) + 1$ no run is alive: an alive run is a path of $N$ with $t(n) + 1$ steps whose last configuration is not halting, and no path has more than $t(n)$ steps. So $D$ halts at level $t(n)+1$ at the latest. It does not accept, because no run has status accept. It rejects.

*Time.* $D$ stops by level $t(n) + 1$. The number of strings it tries is at most $\sum_{\ell=0}^{t(n)+1} b^\ell \le (t(n)+2)\, b^{t(n)+1}$. For each string, $D$ spends $O(n)$ steps to copy the input, $O(\ell)$ steps to simulate the moves (each move is a constant number of steps), $O(n + \ell)$ steps to erase the work tape, and $O(\ell)$ steps to produce the next string. This is $O(t(n))$ steps in all, since $n \le t(n)$ and $\ell \le t(n)+1$. The total is $O(t(n)^2\, b^{t(n)+1}) = 2^{O(t(n))}$, because $b$ is a constant and $t(n)^2 \le 2^{2 t(n)}$ for $t(n) \ge 1$. A one-tape machine simulates $D$ with a square of this time (the claim of the multitape page), and $(2^{O(t)})^2 = 2^{O(t)}$. A machine with more tapes is simulated in the same way, with $O(1)$ steps for each of its moves. $\blacksquare$

**Theorem (recognizers).** For every nondeterministic machine $N$ there is a deterministic machine $D$ with $L(D) = L(N)$. If every path of $N$ is finite on every input, $D$ can be made a decider.

*Proof.* Let $D$ be the machine of the proof above, with this change: it stops with accept when a run has status accept, and otherwise it goes on to level $\ell + 1$ while some run is alive, and it rejects when a level has no alive run. If $N$ accepts $w$, the argument above shows that $D$ accepts $w$ at level $s$ at the latest, even when other paths of $N$ run forever, because the search is by level and so is breadth first. If $N$ does not accept $w$, then $D$ never accepts, and it either rejects or runs forever, so $L(D) = L(N)$. Now suppose that every path of $N$ on $w$ is finite. The computation tree is finitely branching with no infinite path, so by König's lemma it is finite. Then it has some depth $h$, and no run is alive at level $h + 1$, so $D$ halts. Hence $D$ decides $L(N)$. $\blacksquare$

**Example.** For the machine $N_3$ above, $b = 2$. On $0110$ the accepting path has the list of choices $1\,2\,1\,1\,1$, and $D$ tries $1 + 2 + 4 + 8 + 16 = 31$ strings at the levels $0$ to $4$ and then $9$ strings at level $5$, so it accepts after $40$ runs. On $0000$ no run of length $5$ is alive, so $D$ rejects after all $1 + 2 + 4 + 8 + 16 + 32 = 63$ strings of length at most $5$. The bound $(t(n) + 2)\,b^{t(n)+1}$ of the proof, with $t(n) = 5$, is $7 \cdot 64 = 448$.

The same simulation shows $\mathrm{NTIME}(t(n)) \subseteq \mathrm{DSPACE}(t(n))$ for $t(n) \ge n$, when the space counts the cells of all tapes. The work tape and the string $c$ have $O(t(n))$ cells, and $D$ reuses them for each run. For nondeterministic space the loss is much smaller than for time (see Savitch's theorem below).

## Known results in the model

- **NP.** $\mathrm{NP} = \bigcup_k \mathrm{NTIME}(n^k)$. A language $L$ is in NP if and only if there are polynomials $p, q$ (with natural-number coefficients) and a deterministic machine $V$ such that $V$ runs in time $q(|x| + |y|)$ and $L = \{ x : \exists y,\ |y| \le p(|x|) \text{ and } V \text{ accepts } (x, y) \}$. The string $y$ is a [certificate](/certificate/), and $V$ is a *verifier*. The proof is below.
- **Place of NP.** $\mathrm{P} \subseteq \mathrm{NP}$, because a deterministic machine is a nondeterministic machine. By the theorem above, $\mathrm{NP} \subseteq \mathrm{EXP}$ and $\mathrm{NP} \subseteq \mathrm{PSPACE}$. See [P](/p/), [PSPACE](/pspace/) and [EXPTIME](/exptime/). Whether $\mathrm{P} = \mathrm{NP}$ is open.
- **Complete problems.** The [Cook-Levin theorem](/cook-levin-theorem/) (Cook 1971, Levin 1973) shows that [SAT](/sat/) is [NP-complete](/np-complete/). The proof writes the accepting computation of a nondeterministic machine with time bound $t(n)$ as a $t(n) \times t(n)$ table of tape contents, and expresses the rules of the machine by clauses on the cells of the table. SAT is in NP because a machine can guess an assignment of the variables and check it in polynomial time.
- **Nondeterministic time hierarchy.** Cook (1973) proved $\mathrm{NTIME}(n^r) \subsetneq \mathrm{NTIME}(n^s)$ for $1 \le r < s$. Seiferas, Fischer and Meyer (1978) proved the general form: if $g$ is time-constructible and $f(n+1) = o(g(n))$, then $\mathrm{NTIME}(f(n)) \subsetneq \mathrm{NTIME}(g(n))$, for multitape machines. Žák (1983) gave a short proof of the same result. There is no factor $\log f$ as in the deterministic hierarchy, because the two-tape simulation of Book, Greibach and Wegbreit loses only a constant factor. The shift $n + 1$ comes from the diagonal argument, which cannot complement a nondeterministic machine directly.
- **Linear time.** Paul, Pippenger, Szemerédi and Trotter (1983) proved $\mathrm{DTIME}(n) \subsetneq \mathrm{NTIME}(n)$ for multitape machines. For polynomial time the question is the open P versus NP question.
- **Space: Savitch.** Savitch (1970) proved $\mathrm{NSPACE}(s(n)) \subseteq \mathrm{DSPACE}(s(n)^2)$ for space-constructible $s(n) \ge \log n$. So nondeterminism costs at most a square in space, and $\mathrm{NPSPACE} = \mathrm{PSPACE}$. See [Savitch's theorem](/savitch-theorem/).
- **Space: complements.** Immerman (1988) and Szelepcsényi (1988), each on their own, proved $\mathrm{NSPACE}(s(n)) = \mathrm{coNSPACE}(s(n))$ for $s(n) \ge \log n$. In particular $\mathrm{NL} = \mathrm{coNL}$. See the [Immerman-Szelepcsényi theorem](/immerman-szelepcsenyi-theorem/). The analogous question for time, $\mathrm{NP} = \mathrm{coNP}$, is open.
- **Acceptance is not symmetric.** [coNP](/co-np/) is the class of complements of languages in NP. The definition gives no machine for it, because "no path accepts" is a universal statement. Whether $\mathrm{NP} = \mathrm{coNP}$ is open.

*Proof of the certificate characterization.* Here $p$ is a polynomial with natural-number coefficients, and $q$ is a polynomial. Assume that $L \in \mathrm{NP}$. Let $N$ decide $L$ with every path of at most $r(n)$ steps, where $r$ is a polynomial. Let $V$ be the machine that, on $(x, y)$ with $y \in \{1, \ldots, b\}^*$ coded in binary, runs $N$ on $x$ and uses $y_i$ as the choice at step $i$. $V$ rejects if a choice is out of range, if $y$ ends before $N$ halts, or if $N$ halts in reject. $V$ accepts if $N$ reaches accept. The run takes $O(r(|x|))$ steps on a multitape machine. If $x \in L$, an accepting path has at most $r(|x|)$ steps, and its list of choices, with $\lceil \lg (b+1) \rceil$ bits for each choice, is a certificate of length at most $\lceil \lg (b+1) \rceil\, r(|x|)$. This is at most $p(|x|)$ for a polynomial $p$ with natural-number coefficients, and $V$ runs in time $O(r(|x|)) \le q(|x| + |y|)$ for a suitable polynomial $q$, because $V$ stops after at most $r(|x|)$ choices. If $V$ accepts $(x, y)$, the run is an accepting path of $N$, so $x \in L$.

Conversely, assume that $V$, $p$ and $q$ are as stated. Let $(x, y)$ be coded as $x$, a separator symbol, then $y$, and measure the time of $V$ in $|x| + |y|$. Let $N$ work in three stages on an input $x$ of length $n$. First it writes $p(n)$ ones on a work tape. This is deterministic and takes time polynomial in $n$, because $p$ is a fixed polynomial with natural-number coefficients. Second it writes a string $y$ on another tape, symbol by symbol. At each step it chooses among writing $0$, writing $1$ and stopping, and it counts its symbols against the ones so that it stops after $p(n)$ symbols at the latest. Third it simulates $V$ on the coded pair $(x, y)$, which has length at most $n + p(n) + 1$, and accepts if and only if $V$ accepts. Each path has polynomially many steps, because $|y| \le p(n)$ and the third stage takes at most $q(n + p(n) + 1)$ simulated steps. A path accepts if and only if its string $y$ makes $V$ accept. So $N$ accepts $x$ if and only if some $y$ with $|y| \le p(n)$ makes $V$ accept, that is, if and only if $x \in L$. Hence $L \in \mathrm{NP}$. $\blacksquare$

### Pitfalls

- **Time is the longest path, not the sum of all paths.** A machine that branches into $2^n$ paths of length $n$ runs in time $n$. Adding the branches gives the cost of a deterministic search, not the time of $N$.
- **Nondeterminism is not randomness.** One accepting path is enough, however few there are. A probabilistic machine needs many accepting paths. See [probabilistic Turing machine](/probabilistic-turing-machine/).
- **The definition is one-sided.** Swapping accept and reject in $N$ does not give a machine for the complement. The new machine accepts $w$ when some path rejects, which is not the same as "no path accepts". This is why coNP is not known to equal NP.
- **Deciding needs every path to halt.** A machine that accepts the right words but has an infinite path on some other word only recognizes its language. The time bound $t(n)$ makes every path finite.
- **A guess must be checked.** A machine that guesses a certificate must verify all of it. A guess that is used without a check makes the machine accept words that are not in the language.
- **Exponential simulation is the best known, not a proven lower bound.** No superpolynomial lower bound is known for the deterministic simulation of polynomial-time nondeterministic machines in general. For linear time on multitape machines, only the separation of Paul, Pippenger, Szemerédi and Trotter is known.

## References
