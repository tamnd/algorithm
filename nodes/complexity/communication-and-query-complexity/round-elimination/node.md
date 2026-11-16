---
tag: 5D44FG
kind: technique
slug: round-elimination
name: Round elimination
area: complexity/communication-and-query-complexity
level: research
summary: "A lower bound method for protocols with few rounds. When the first message must serve k independent sub-problems, it can be removed at a small cost in error, and induction ends in a contradiction."
prereqs: [one-way-communication-complexity, randomized-communication-complexity]
see_also: [predecessor-lower-bound, index-problem, pointer-chasing-problem, gap-hamming-distance, cell-probe-lower-bound, one-way-communication-complexity, information-complexity, direct-sum-communication]
sources:
  - paper: doi:10.1006/jcss.1998.1577
    title: "Peter Bro Miltersen, Noam Nisan, Shmuel Safra and Avi Wigderson, On Data Structures and Asymmetric Communication Complexity, Journal of Computer and System Sciences 57(1) (1998), 37-49"
    locator: the round elimination lemma and its use for data structure lower bounds
  - paper: doi:10.1016/j.jcss.2007.06.016
    title: "Pranab Sen and S. Venkatesh, Lower bounds for predecessor searching in the cell probe model, Journal of Computer and System Sciences 74(3) (2008), 364-385"
    locator: Result 2, the round elimination lemma with error increase (1/2) sqrt(2 m ln 2 / k)
  - paper: doi:10.1006/jcss.2002.1822
    title: "Paul Beame and Faith E. Fich, Optimal Bounds for the Predecessor Problem and Related Problems, Journal of Computer and System Sciences 65(1) (2002), 38-72"
    locator: the round elimination argument for the predecessor problem
  - paper: "Noam Nisan and Avi Wigderson, Rounds in communication complexity revisited, SIAM Journal on Computing 22(1) (1993)"
    locator: the round lower bound for pointer chasing, proved by removing one round at a time
  - paper: "Joshua Brody, Amit Chakrabarti, Oded Regev, Thomas Vidick and Ronald de Wolf, Better gap-Hamming lower bounds via better round elimination, Proceedings of APPROX-RANDOM 2010"
    locator: a round elimination lemma for distributional protocols and its use for gap Hamming distance
---

Round elimination proves lower bounds for communication protocols with a fixed number of rounds. Its main lemma says: if a problem is made of $k$ independent copies of a smaller problem, and the player who speaks first does not know which copy matters, then the first message can be removed at a small cost in error, as long as it is much shorter than $k$. Repeating the step removes all rounds and leaves a protocol with no messages, which cannot have error below $1/2$. The method was isolated by Miltersen, Nisan, Safra and Wigderson (1998) for data structure lower bounds, and its sharpest classical form is due to Sen and Venkatesh (2008).

## In plain words

Alice must speak first, but the question has many parts and only Bob knows which part counts. If her first message is short, it can say only a little about each part. So for the part that counts, the message tells Bob almost nothing, and the players could skip it and lose very little.

After the skip, Bob speaks first, and he is now the one who does not know which part counts. The same reasoning removes his message too. After all messages are gone, nobody has said anything, and then nobody can answer better than a coin toss. If the losses along the way were small, this is a contradiction, so the messages could not have been short.

## When it applies

- The protocol has a bounded number $r$ of rounds, and each round has a known bound on the length of its message. The method gives trade-offs between the number of rounds and the message lengths, and it says nothing about protocols with many rounds.
- The problem is self-reducible: an instance of the problem on large inputs contains an instance of the form $f^{(k),A}$ below, where $f$ is the same kind of problem with the roles of the players swapped and smaller parameters.
- Typical uses are asymmetric problems from data structures, where Alice (the query) sends short messages and Bob (the table) sends long ones, and one-way or few-round bounds for problems like [index](/index-problem/) and [gap Hamming distance](/gap-hamming-distance/).

## The template

**Notation.** For a problem $f(x, y)$ and an integer $k \ge 1$, let $f^{(k),A}$ be the problem in which Alice holds $x_1, \ldots, x_k$, Bob holds $i \in \{1, \ldots, k\}$, $y$, and the prefix $x_1, \ldots, x_{i-1}$, and the answer is $f(x_i, y)$. Define $f^{(k),B}$ in the same way with the roles exchanged.

**Round elimination lemma (Sen and Venkatesh, Result 2).** Suppose $f^{(k),A}$ has a public-coin protocol with error less than $\varepsilon$ in which Alice sends the first message, of $m_1$ bits, followed by messages of $m_2, \ldots, m_r$ bits. Then $f$ has a public-coin protocol with error less than

$$\varepsilon + \tfrac12 \sqrt{2 m_1 \ln 2 / k}$$

in which Bob sends the first message, followed by messages of $m_2, \ldots, m_r$ bits, so with one round fewer. The same holds with the roles exchanged.

The idea of the proof: a message of $m_1$ bits carries at most $m_1$ bits of information about $x_1, \ldots, x_k$. By the chain rule, for a random $i$ it carries at most $m_1/k$ bits about $x_i$ given the prefix, and Pinsker's inequality turns this into a statistical distance of at most $\sqrt{(m_1/k) \ln 2 / 2}$. So the players can replace the first message by one drawn with public coins, without looking at $x_i$, at this cost in error. The full proof, the self-reductions and a complete application are on the [predecessor lower bound](/predecessor-lower-bound/) page.

```pseudo id=main
ROUND-ELIMINATION(g, r, m_1, ..., m_r)
L1  assume g has a public-coin r-round protocol with message lengths m_1, ..., m_r and error ε_0
L2  show that g contains ⟨f^{(k),A}⟩ for a problem f of the same family      ▷ ⟨self-reduction⟩
L3  apply the lemma: f has an (r - 1)-round protocol, Bob first, with error ε_0 + (1/2) sqrt(2 m_1 ln 2 / k)
L4  swap the roles of Alice and Bob and repeat L2 and L3 for each remaining round
L5  after r steps: a 0-round protocol for ⟨the base problem⟩ with error ε_0 + sum of the added terms
L6  a 0-round protocol for the base problem has error at least 1/2; so the sum is at least 1/2 - ε_0
L7  return the condition on m_1, ..., m_r and k that this forces
```

The holes are the $\langle$self-reduction$\rangle$ that finds $f^{(k),A}$ inside the current problem, the size $k$ it gives, and $\langle$the base problem$\rangle$, which must be hard with no messages at all, for example a uniform bit that Bob must guess.

**The error budget.** Start with error $\varepsilon_0 = 1/3$ and suppose every step uses the same $m$ and $k$. Then the sum of $r$ added terms is $r \cdot \tfrac12 \sqrt{2 m \ln 2 / k}$, and it stays below $1/6$ exactly when

$$m < \frac{k}{18\, r^2 \ln 2}.$$

So with $r$ rounds, each sub-problem split must make $k$ at least about $18\, r^2 \ln 2 \cdot m \approx 12.5\, r^2 m$. The factor $r^2$ is the price of the method, and it is the reason the bounds weaken as the number of rounds grows.

## Classic examples

**Index in one round.** Let $f(x, y) = x$ for a single bit $x$, with no input for Bob. Then $f^{(n),A}$ is the augmented [index problem](/index-problem/) on $n$ bits: Alice holds $x_1, \ldots, x_n$, Bob holds $i$ and the prefix, and he must output $x_i$. Suppose a one-way protocol with $m$ bits has error $1/3$. The lemma gives a protocol for $f$ with no messages and error less than $1/3 + \tfrac12 \sqrt{2 m \ln 2 / n}$. With no messages, Bob guesses a uniform bit and errs with probability $1/2$. So $\tfrac12 \sqrt{2 m \ln 2 / n} \ge 1/6$, which gives

$$m \ge \frac{n}{18 \ln 2} \approx 0.0801\, n.$$

The direct information bound gives $(1 - H_2(1/3))\, n \approx 0.0817\, n$, so for one round the lemma loses only a little. The bound holds for index without the prefix too, since the prefix only helps Bob.

**Predecessor search.** Miltersen, Nisan, Safra and Wigderson, and then Beame and Fich, turned a cell probe scheme with $t$ probes into a protocol with $2t$ rounds, Alice sending $\lceil \log_2 s \rceil$ bits per round and Bob sending a cell of $w$ bits. Self-reductions of the predecessor problem split the query into $k$ blocks for Alice's rounds and the key set into $k$ parts for Bob's rounds. Round elimination then gives the Beame and Fich bound $\Omega(\log \ell / \log\log \ell)$. The full argument with Sen and Venkatesh's lemma is on the [predecessor lower bound](/predecessor-lower-bound/) page.

**Pointer chasing.** In the [pointer chasing problem](/pointer-chasing-problem/), a protocol with $k$ rounds in which the wrong player starts needs many bits. Nisan and Wigderson (1993) proved this by removing one round at a time: a short first message says little about the next pointer, which is chosen by the unknown current position. Their argument is a direct information proof in the spirit of round elimination.

**Gap Hamming distance.** Brody and Chakrabarti (2009) used round elimination to prove $\Omega(n)$ bounds for protocols with a constant number of rounds for [gap Hamming distance](/gap-hamming-distance/). Brody, Chakrabarti, Regev, Vidick and de Wolf (2010) proved a stronger lemma for distributional protocols and improved the dependence on the number of rounds, before the two-way bound of Chakrabarti and Regev settled the problem for any number of rounds.

## Variations

- **The original lemma.** Miltersen, Nisan, Safra and Wigderson proved a version with a weaker error term. Its parameters were enough for their bounds, but the bounds of Beame and Fich and the randomized bounds need sharper forms.
- **Quantum protocols.** Sen and Venkatesh proved their lemma also for quantum protocols, which gives predecessor bounds for quantum queries.
- **Distributional form.** The lemma can be stated for protocols with small error under a product distribution, which is the form used for gap Hamming distance.
- **Cell probe elimination.** Patrascu and Thorup replaced rounds by cell probes and proved an elimination lemma directly for data structures, which gave the exact time-space trade-off for predecessor search. See [cell probe lower bounds](/cell-probe-lower-bound/).
- **Message compression.** A related family of results compresses the first message instead of removing it, and then uses a [direct sum](/direct-sum-communication/) argument; these are proved with [information complexity](/information-complexity/).

## Pitfalls

- The first speaker must not know which sub-problem matters. If Bob could send $i$ first, the problem would become easy, and the lemma does not apply to that order.
- The other player's extra knowledge is part of the problem. In $f^{(k),A}$ Bob also holds the prefix $x_1, \ldots, x_{i-1}$. A self-reduction that does not give Bob this prefix is fine, since the prefix only helps Bob, but a reduction that needs to give Alice information about $i$ breaks the lemma.
- The error terms add up over the rounds. With $r$ rounds, $k$ must be about $r^2$ times larger than the message length, not $r$ times. Forgetting this gives bounds that are too strong.
- The lemma needs public coins in the new protocol: the removed message is replaced by one drawn with shared randomness. Bounds for private coins follow, since private-coin protocols are at least as costly.
- The same name is used in distributed computing for a different method, which turns a $t$-round algorithm in the [LOCAL model](/local-model/) into a $(t-1)$-round algorithm for a derived problem. It has the same shape of argument but no communication lemma.

## Exercises

1. Derive $m \ge n/(18 \ln 2)$ for one-way index from the lemma, and compare it with $(1 - H_2(1/3))\, n$.
2. Show that the condition $m < k/(18 r^2 \ln 2)$ keeps the total error below $1/2$ when the starting error is $1/3$.
3. Show that a lower bound for augmented index implies the same lower bound for index.
4. Explain why the lemma gives nothing when $m_1 \ge k$, and give a protocol for $f^{(k),A}$ in which Alice's first message has $k$ bits and the rest of the protocol is trivial, when $f$ is a single bit.
5. For two-way index, show that a protocol in which Bob speaks first costs $\lceil \log_2 n \rceil + 1$ bits, and explain which hypothesis of the lemma fails.

## References
