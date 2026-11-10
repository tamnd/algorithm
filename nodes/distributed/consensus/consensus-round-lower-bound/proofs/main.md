---
title: Synchronous consensus with f crashes needs f + 1 rounds
proves: [statement]
status: full
---

This is the bivalence proof of Aguilera and Toueg (1999), written out in full.

**Statement.** Consider the synchronous model with $n$ processes, a complete network of reliable links, and crash failures, with $1 \le f \le n - 2$. Let $A$ be a deterministic algorithm that, in each run with at most $f$ crashes, satisfies agreement (no two processes that do not crash decide different values), unanimity validity (if all inputs are $v$, a decision is $v$) and termination (each process that does not crash decides). Then $A$ has a run with at most $f$ crashes in which some process that does not crash has not decided at the end of round $f$.

**Setup.**

1. A process that crashes in round $r$ sends its round $r$ message to a subset of the others of the adversary's choice, and takes no step after round $r$. A process is *correct* in a run if it never crashes. A decision is final once made.
2. A run is *serial* if at most one process crashes in each round. We use only serial runs with at most $f$ crashes. They are runs of the model, so $A$ satisfies the three properties on them.
3. A *$k$-configuration* is the global state after round $k$ of a serial run: the state of each process and the set of crashed processes. After round $k$ of a serial run, at most $k$ processes have crashed.
4. For a $k$-configuration $C$, $\mathrm{Val}(C)$ is the set of values that correct processes decide in the serial runs with at most $f$ crashes that extend $C$. In such a run at least $n - f \ge 2$ processes are correct, they all decide (termination), and they decide the same value (agreement). So each run has exactly one decision value, and $\mathrm{Val}(C) \ne \emptyset$. $C$ is *$v$-valent* if $\mathrm{Val}(C) = \{v\}$ and *bivalent* if $\mathrm{Val}(C) = \{0, 1\}$. A univalent $C$ has the property that every serial extension of it decides its one value, so to learn the valence of a univalent configuration it is enough to look at one extension.
5. Let $C$ be a $k$-configuration. Its *one-round extensions* are the $(k+1)$-configurations of serial runs through $C$. Since at most one process crashes in round $k + 1$, each one-round extension is either $C^{\varnothing}$, where no process crashes in round $k+1$, or $C^{p,S}$, where a process $p$ that is live in $C$ crashes in round $k+1$ and its round $k+1$ message reaches exactly the set $S$ of live processes other than $p$. Each serial run through $C$ passes through exactly one of them, so $\mathrm{Val}(C)$ is the union of the sets $\mathrm{Val}$ of the one-round extensions.
6. *Indistinguishability.* If two runs give a process the same state at the end of some round, and from then on the same messages in each round, the process makes the same steps and the same decisions in both, because $A$ is deterministic.

**Lemma 1 (a bivalent start).** Some $0$-configuration is bivalent.

1. For $0 \le j \le n$, let $I_j$ be the $0$-configuration in which $p_1, \ldots, p_j$ have input 1 and the others input 0. By validity, $\mathrm{Val}(I_0) = \{0\}$ and $\mathrm{Val}(I_n) = \{1\}$.
2. Assume that no $I_j$ is bivalent. Then each is univalent, and there is a $j$ with $I_{j-1}$ 0-valent and $I_j$ 1-valent. These two differ only in the input of $p_j$.
3. Let $\rho$ be the serial run from $I_{j-1}$ in which $p_j$ crashes in round 1 and sends nothing, and no other process crashes. Let $\rho'$ be the same from $I_j$. This is one crash, and $f \ge 1$.
4. In both runs $p_j$ sends nothing, and every other process has the same input. By step 6 of the setup and induction on the rounds, every process other than $p_j$ has the same state in each round of $\rho$ and $\rho'$. So the correct processes decide the same value in both.
5. But $\rho$ decides 0 and $\rho'$ decides 1, by step 2. This is a contradiction. $\square$

**Lemma 2 (one more round, still bivalent).** Let $0 \le k \le f - 2$, and let $C$ be a bivalent $k$-configuration. Then some one-round extension of $C$ is bivalent.

1. Assume that all one-round extensions of $C$ are univalent. Since $\mathrm{Val}(C) = \{0, 1\}$ is their union (setup step 5), some are 0-valent and some are 1-valent. Let $C^{\varnothing}$ be $v$-valent.
2. *Claim A: $C^{p, S_{\mathrm{all}}}$ is $v$-valent, where $S_{\mathrm{all}}$ is the set of all live processes other than $p$.* In $C^{p,S_{\mathrm{all}}}$ every process has the same state as in $C^{\varnothing}$, and only the label "crashed" of $p$ differs. Take the extension of $C^{p,S_{\mathrm{all}}}$ with no more crashes, and the extension of $C^{\varnothing}$ in which $p$ crashes in round $k+2$ and sends nothing, with no other crash. The second run is serial and has at most $k + 1 \le f$ crashes. In both runs, $p$ sends nothing after round $k + 1$, so every other process has the same states in both (setup step 6). The correct processes are the same in both and decide the same value. Both configurations are univalent, so they have the same valence (setup step 4).
3. *Claim B: for each $S$ and each $q \in S$, $C^{p,S}$ and $C^{p,S \setminus \{q\}}$ have the same valence.* The two configurations differ only in the state of $q$. Take, from each of them, the extension in which $q$ crashes in round $k + 2$ and sends nothing, with no other crash. This adds one crash in round $k+2$, so the runs are serial with at most $k + 2 \le f$ crashes. Here we use $k \le f - 2$. In both runs, no process other than $q$ ever gets a message that depends on the state of $q$ after round $k+1$, so all processes other than $p$ and $q$ have the same states in both runs. At least $n - f \ge 2$ processes are correct in these runs, and none of them is $p$ or $q$, so some correct process decides the same value in both. Both configurations are univalent, so they have the same valence.
4. Fix a live process $p$. Starting from $C^{p,S_{\mathrm{all}}}$, remove the members of $S_{\mathrm{all}}$ one at a time. By Claim B, every $C^{p,S}$ with $S \subseteq S_{\mathrm{all}}$ has the valence of $C^{p,S_{\mathrm{all}}}$, which is $v$ by Claim A.
5. So every one-round extension of $C$ is $v$-valent. This contradicts step 1. $\square$

**Lemma 3 (the last round).** Let $C$ be a bivalent $(f-1)$-configuration. Then in some serial run through $C$ with at most $f$ crashes, a correct process has not decided at the end of round $f$.

1. Assume the opposite: in every serial run through $C$ with at most $f$ crashes, each correct process has decided by the end of round $f$.
2. Then each one-round extension $C'$ of $C$ is univalent. In the extension of $C'$ with no more crashes, each process live in $C'$ is correct, so it has decided by the end of round $f$, and by agreement all of them have decided one value $w$. In any other extension of $C'$, the correct processes are among these processes, and their decisions are already made. So $\mathrm{Val}(C') = \{w\}$.
3. As in Lemma 2, step 1, some one-round extension is 0-valent and some is 1-valent. Let $C^{\varnothing}$ be $v$-valent.
4. $C^{p,S_{\mathrm{all}}}$ is $v$-valent. All processes other than $p$ have the same state in it as in $C^{\varnothing}$. At least $n - f \ge 2$ processes are live in it, and each has decided the same value in both.
5. $C^{p,S}$ and $C^{p,S \setminus \{q\}}$ have the same valence. They differ only in the state of $q$. At least $n - f \ge 2$ processes are live in them, and $p$ is not one of them, so there is a live process $r \ne q$. Process $r$ has the same state in both, and it has already decided, so it decided the same value in both.
6. Steps 4 and 5 give, as in Lemma 2, step 4, that all one-round extensions are $v$-valent. This contradicts step 3. $\square$

**Proof of the theorem.** By Lemma 1 there is a bivalent $0$-configuration. Apply Lemma 2 for $k = 0, 1, \ldots, f - 2$ (no application when $f = 1$). This gives a bivalent $(f-1)$-configuration of a serial run. By Lemma 3, some serial run through it with at most $f$ crashes has a correct process that is undecided at the end of round $f$. So $A$ needs at least $f + 1$ rounds in its worst case. $\blacksquare$

**The case $f = 0$.** With $n \ge 2$ and no rounds, the decision of $p_1$ is a function of its input alone, and the same holds for $p_2$. Validity on the unanimous inputs forces $p_1$ to decide $v_1$ and $p_2$ to decide $v_2$. The inputs $v_1 = 0$ and $v_2 = 1$ then break agreement. So at least $1 = f + 1$ round is necessary.
