---
tag: 72GMWX
kind: theorem
slug: consensus-round-lower-bound
name: Round lower bound for synchronous consensus
aliases:
- f+1 rounds lower bound
area: distributed/consensus
level: advanced
summary: Synchronous crash-tolerant consensus with f faults needs f+1 rounds in the worst case.
prereqs: [floodset, consensus-properties]
see_also: [flp-impossibility, byzantine-round-lower-bound, dolev-strong-algorithm, interactive-consistency, synchronous-model, crash-failure, round-complexity, adversary-argument]
sources:
  - paper: doi:10.1016/0020-0190(82)90033-3
    title: Michael J. Fischer and Nancy A. Lynch, A lower bound for the time to assure interactive consistency, Information Processing Letters 14(4), 1982
    locator: pages 183 to 186 (t + 1 rounds are necessary for interactive consistency with t faulty processes)
  - paper: doi:10.1137/0212045
    title: Danny Dolev and H. Raymond Strong, Authenticated algorithms for Byzantine agreement, SIAM Journal on Computing 12(4), 1983
    locator: pages 656 to 666 (the t + 1 round lower bound, which holds also with signatures)
  - paper: doi:10.1016/S0020-0190(99)00100-3
    title: Marcos K. Aguilera and Sam Toueg, A simple bivalency proof that t-resilient consensus requires t + 1 rounds, Information Processing Letters 71(3-4), 1999
    locator: pages 155 to 158 (the bivalence proof for crash failures that this page follows)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 6, Section 6.7 (the number of rounds for agreement with stopping failures, proved with a chain of executions)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 5, Section 5.1 (the lower bound of f + 1 rounds for consensus with crash failures)
---

In the [synchronous model](/synchronous-model/) with [crash failures](/crash-failure/), each deterministic [consensus](/consensus-problem/) algorithm that tolerates $f$ crashes has a run in which some correct process is still undecided after $f$ rounds, when $f \le n - 2$. So $f + 1$ rounds are necessary in the worst case, and [FloodSet](/floodset/) shows that they are enough. Fischer and Lynch proved the bound in 1982 for Byzantine faults, Dolev and Strong also for signed messages, and the simple bivalence proof for crashes on this page is by Aguilera and Toueg (1999).

## Statement

**Model.** There are $n$ processes on a complete network of reliable links. Computation runs in lock-step rounds: in each round each live process sends messages, receives all messages sent to it in the round, and changes its state. At most $f$ processes crash. A process that crashes in round $r$ sends its round $r$ messages to a subset of the others that the adversary chooses, and takes no step after that. A process is *correct* if it never crashes.

**Theorem.** Let $1 \le f \le n - 2$. Let $A$ be a deterministic algorithm for binary consensus in this model that satisfies, in each run with at most $f$ crashes:

- **agreement:** no two correct processes decide different values;
- **validity:** if all inputs are $v$, then each decision is $v$;
- **termination:** each correct process decides.

Then $A$ has a run with at most $f$ crashes, and with at most one crash in each round, in which some correct process has not decided at the end of round $f$. So $A$ needs at least $f + 1$ rounds in its worst case.

The [properties](/consensus-properties/) used are the weakest common forms. Agreement is not uniform, and validity is only unanimity. So the bound holds for each stronger form too, and for each larger value set, because an algorithm for a larger set also solves the binary case. For $f = 0$ one round is needed and enough, so the bound $f + 1$ holds for $0 \le f \le n - 2$.

## In plain words

Computers work in rounds, and some of them may stop during a round after they have sent a message to only some of the others. Can they always agree within as many rounds as there are possible stops? No. The adversary can stop one computer in each round, each time just as it tells one other computer something new. Then, in the last round, one computer knows something that another computer does not, and they cannot tell each other in time. One more round fixes this, because at most as many computers stop as there are possible stops, so some round has no stop. A simple flooding algorithm uses exactly this one extra round, so the bound is the best possible.

## Proof

The full proof, with every step, is below. This section gives its structure.

**Setup.** A run is *serial* if at most one process crashes in each round. Only serial runs with at most $f$ crashes are used. For the global state $C$ after round $k$ of a serial run, $\mathrm{Val}(C)$ is the set of values that correct processes decide in serial extensions of $C$ with at most $f$ crashes. In each such extension at least $n - f \ge 2$ processes are correct, and they all decide one value, so $\mathrm{Val}(C)$ is $\{0\}$, $\{1\}$ or $\{0, 1\}$. $C$ is *univalent* in the first two cases and *bivalent* in the last. The proof is an [adversary argument](/adversary-argument/). A deterministic process that has the same state and gets the same messages in two runs behaves the same in both. This *indistinguishability* is the only tool.

The one-round extensions of $C$ are $C^{\varnothing}$, in which nobody crashes in round $k + 1$, and $C^{p,S}$, in which a live process $p$ crashes in round $k + 1$ and its message reaches exactly the set $S$. $\mathrm{Val}(C)$ is the union of their $\mathrm{Val}$ sets.

**Lemma 1 (a bivalent start).** Some initial configuration is bivalent.

*Proof.* Let $I_j$ give input 1 to $p_1, \ldots, p_j$ and input 0 to the others. By validity, $I_0$ is 0-valent and $I_n$ is 1-valent. If no $I_j$ is bivalent, some $I_{j-1}$ is 0-valent and $I_j$ is 1-valent, and they differ only in the input of $p_j$. Crash $p_j$ in round 1 before it sends anything, in both. Then no other process can tell the two runs apart, and the correct processes decide the same value in both. This is a contradiction. $\square$

**Lemma 2 (one more bivalent round).** If $k \le f - 2$ and $C$ is a bivalent configuration after round $k$, then some one-round extension of $C$ is bivalent.

*Proof.* Assume that all one-round extensions are univalent, and let $C^{\varnothing}$ be $v$-valent. Some extension is then $(1-v)$-valent. Fix a live process $p$ and remove the receivers of its round $k+1$ message one at a time, from $C^{\varnothing}$ down to $C^{p,\emptyset}$.

- $C^{\varnothing}$ and $C^{p,S_{\mathrm{all}}}$, where all other live processes get the message, have the same valence. All processes other than $p$ have the same state in both. Crash $p$ in round $k+2$ before it sends anything in the first, and let nobody crash later in the second. No process other than $p$ can tell these runs apart.
- $C^{p,S}$ and $C^{p,S \setminus \{q\}}$ have the same valence. Only $q$ can tell them apart. Crash $q$ in round $k + 2$ before it sends anything, in both. This is a crash in round $k + 2 \le f$, so the run has at most $f$ crashes and is still serial. No process other than $q$ can tell the two runs apart, and at least two processes are correct.

So each $C^{p,S}$ is $v$-valent, for each $p$ and $S$, and all one-round extensions are $v$-valent. This is a contradiction. $\square$

**Lemma 3 (the last round).** If $C$ is a bivalent configuration after round $f - 1$, then some serial run through $C$ with at most $f$ crashes has a correct process that is undecided at the end of round $f$.

*Proof.* Assume that each correct process has decided by the end of round $f$ in each such run. Then the valence of each one-round extension $C'$ is fixed by the decisions already made in $C'$, so $C'$ is univalent. The chain of Lemma 2 now needs no crash in round $f + 1$: in $C^{p,S}$ and $C^{p,S \setminus \{q\}}$ there are at least $n - f \ge 2$ live processes, and $p$ is not one of them, so a live process $r \ne q$ has the same state, and the same decision, in both. This is the step that uses $f \le n - 2$. Then all one-round extensions have one valence, a contradiction. $\square$

**The theorem.** Lemma 1 gives a bivalent initial configuration. Lemma 2, used $f - 1$ times, gives a bivalent configuration after round $f - 1$ of a serial run with at most $f - 1$ crashes. Lemma 3 gives the run in which a correct process is undecided after round $f$. $\blacksquare$

**A chain of executions.** The proof of Lynch, Section 6.7, uses a direct chain in place of valence. It lists runs of $R$ rounds, from all inputs 0 with no crash to all inputs 1 with no crash. Each run has at most one crash in each round, so at most $R$ crashes. In each pair of neighbours, some process is correct in both and has the same final state in both, so it decides the same value in both. Validity fixes 0 at one end and 1 at the other, so if $R \le f$, some run of the chain breaks agreement. The chain changes one input at a time, and to change the input of $p$ it first silences $p$. To remove a message of round $r < R$ from $p$ to $q$, it first silences $q$ from round $r + 1$ on, so the change is hidden, and then brings $q$ back. For $n = 3$ and $R = 1$ the chain has 22 runs. For $n = 4$ and $R = 2$ it has 261 runs.

On the chain for $n = 3$ and $R = 1$, FloodSet with the minimum rule breaks agreement here: the inputs are $v_1 = 1$, $v_2 = 1$, $v_3 = 0$, and $p_3$ crashes in round 1 with its message reaching only $p_2$. Then $p_1$ decides 1 and $p_2$ decides 0. A program can build such chains and find such runs for small $n$ and $f$, but it cannot prove the bound for all $n$, $f$ and algorithms. The proof above does that.

**The case $f = n - 1$.** The bound needs $f \le n - 2$. With $f = n - 1$, a run with crashes in each of the first $f$ rounds can leave a single correct process, which cannot disagree with anyone. So FloodSet with only $f$ rounds is correct when $f = n - 1$: either one of the $f$ rounds has no crash, or all $n - 1$ crashes happen in the first $f$ rounds and one process is left.

## Consequences

- **FloodSet is optimal.** No deterministic algorithm beats the $f + 1$ rounds of [FloodSet](/floodset/) in the worst case, when $f \le n - 2$.
- **Stronger failures.** A crash is a special case of a [Byzantine](/byzantine-failure-model/) fault, so each algorithm for Byzantine faults also needs $f + 1$ rounds. This is the [Byzantine round lower bound](/byzantine-round-lower-bound/), and the [Dolev-Strong algorithm](/dolev-strong-algorithm/) meets it with signatures.
- **Worst case only.** The bound is about one bad run. Algorithms that *stop early* decide sooner in runs with few actual crashes, and still use $f + 1$ rounds when the adversary uses all its crashes.
- **Deterministic only.** The proof uses the fact that the same state and the same messages give the same behavior. Randomized algorithms are outside the theorem.
- **A template.** The bivalence method, with a chain of configurations that differ in one step, is the method of the [FLP impossibility](/flp-impossibility/) proof. In the synchronous model each round of delay costs the adversary one crash, so the result is a bound and not an impossibility.

## Tightness

The bound is exact. [FloodSet](/floodset/) solves consensus with any $f < n$ crashes in exactly $f + 1$ rounds, with uniform agreement, so $f + 1$ rounds are necessary and enough when $f \le n - 2$. The condition $f \le n - 2$ is needed: with $f = n - 1$, $f$ rounds are enough, because Lemma 3 fails when only one live process can be left after round $f$. The adversary in the proof uses only one crash per round, so the bound holds already for these restricted adversaries.

## History

Pease, Shostak and Lamport stated the agreement problem in 1980, and their algorithms for Byzantine faults used $f + 1$ rounds. Fischer and Lynch proved in 1982 that $f + 1$ rounds are necessary for interactive consistency with $f$ faulty processes. Dolev and Strong showed in 1983 that the bound holds also for authenticated algorithms, in which messages are signed. The textbooks of Lynch (1996) and of Attiya and Welch (2004) prove the bound for crash failures with chains of executions. Aguilera and Toueg gave the short bivalence proof in 1999, with the method of the FLP proof.

## References
