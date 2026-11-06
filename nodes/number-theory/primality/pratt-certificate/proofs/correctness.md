---
title: Correctness of the Pratt certificate checker
proves: [correctness, termination, error]
status: full
---

We prove that VERIFY-PRATT accepts only primes (soundness), that every prime has a list it accepts (completeness), that it stops, and that it has no error. We also bound the size of the list.

**Lemma 1** (Lucas). Let $p > 1$ and $a$ be integers with $a^{p-1} \equiv 1 \pmod p$ and $a^{(p-1)/q} \not\equiv 1 \pmod p$ for every prime $q \mid p - 1$. Then $p$ is prime.

*Proof.* From $a^{p-1} \equiv 1$, $a$ is a unit modulo $p$. Let $d$ be its order in the group of units $\mathbb{Z}_p^*$; then $d \mid p - 1$. If $d < p - 1$, pick a prime $q$ dividing $(p-1)/d$; then $d \mid (p-1)/q$ and $a^{(p-1)/q} \equiv 1$, which is false. So $d = p - 1$, and the powers $a, a^2, \ldots, a^{p-1}$ are $p - 1$ distinct units. So all of $1, \ldots, p - 1$ are units, no $j$ with $1 < j < p$ divides $p$, and $p$ is prime. $\square$

**Lemma 2** (Crandall and Pomerance, Theorem 4.1.8). Let $p > 1$ be odd, and suppose $a^{(p-1)/2} \equiv -1 \pmod p$ and $a^{(p-1)/(2q)} \not\equiv -1 \pmod p$ for every odd prime $q \mid p - 1$. Then $p$ is prime. Conversely, every primitive root $a$ of an odd prime $p$ meets these conditions.

*Proof.* Squaring gives $a^{p-1} \equiv 1$. Since $p$ is odd and $p > 1$, $p \ge 3$ and $-1 \not\equiv 1$, so $a^{(p-1)/2} \not\equiv 1$; this is the condition of Lemma 1 for $q = 2$. Let $q$ be an odd prime factor of $p - 1$; then $2q \mid p - 1$, since $p - 1$ is even. Put $m = a^{(p-1)/(2q)}$ and suppose $a^{(p-1)/q} = m^2 \equiv 1$. As $q$ is odd, $m^q = (m^2)^{(q-1)/2} \, m \equiv m$. But $m^q = a^{(p-1)/2} \equiv -1$, so $m \equiv -1$, against the hypothesis. So $a^{(p-1)/q} \not\equiv 1$ for every prime $q \mid p - 1$, and Lemma 1 shows that $p$ is prime.

For the converse, let $a$ have order $p - 1$ modulo the odd prime $p$. Then $x = a^{(p-1)/2}$ satisfies $x^2 \equiv 1$ and $x \not\equiv 1$, and modulo a prime the only roots of $x^2 - 1$ are $\pm 1$, so $x \equiv -1$. If $a^{(p-1)/(2q)} \equiv -1$ for an odd prime $q$, then $a^{(p-1)/q} \equiv 1$, against the order of $a$. $\square$

**Soundness.** We show by induction on the number of entries processed that every element of the set *proven* is prime. At the start, *proven* $= \{2\}$. Suppose that before an entry $(p, a, \{q: e\})$ all elements of *proven* are prime, and that the entry passes lines L5 to L9. By line L6 every listed $q$ is prime. By line L5 the listed exponents are at least 1 and $\prod q^e = p - 1$, so by unique factorization the listed $q$ are exactly the prime factors of $p - 1$. Also $p$ is odd and $p \ge 3$. Lines L7 to L9 check the conditions of Lemma 2 for each odd prime factor of $p - 1$, since $a^{(p-1)/2} \bmod p = p - 1$ means $a^{(p-1)/2} \equiv -1$. So $p$ is prime by Lemma 2, and line L10 keeps the invariant. When the loop ends, line L11 returns true only if $n \in$ *proven*, so $n$ is prime. Lines L1 and L2 return true only for $n = 2$.

**Completeness.** Let $n$ be prime. If $n = 2$, line L1 accepts the empty list. Otherwise let $T$ be the set of odd primes in the Lucas tree of $n$: $n \in T$, and if $p \in T$ then every odd prime factor of $p - 1$ is in $T$. List the elements of $T$ in increasing order, each with a primitive root $a_p$ (which exists because $\mathbb{Z}_p^*$ is cyclic) and the factorization of $p - 1$. Every odd prime factor $q$ of $p - 1$ satisfies $q < p$, so its entry comes earlier and $q$ is in *proven* when the entry of $p$ is checked; the prime 2 is in *proven* from the start. Line L5 passes by construction, and lines L7 to L9 pass by the converse in Lemma 2. So every entry passes, $n$ is added at the end, and line L11 returns true.

**Termination.** The loop of line L4 runs once for each entry, and each entry does at most one product per listed prime, one membership test per listed prime and $1 + k$ modular powers, where $k$ is the number of listed primes. Each of these stops, so the checker stops on every finite list.

**Error.** The checker is deterministic, so for a fixed input its answer is fixed. By soundness it never accepts a composite, and by completeness every prime has an accepted list. There is no error probability.

**Size.** Let $N(p)$ be the number of odd primes, counted with repeats, in the Lucas tree of an odd prime $p$. We show $N(p) < \lg p$ by strong induction on $p$ (Crandall and Pomerance, proof of Theorem 4.1.9). For $p = 3$, $N(3) = 1 < \lg 3$. If $p - 1$ is a power of 2, then $N(p) = 1 < \lg p$. Otherwise let $q_1, \ldots, q_k$ be the distinct odd prime factors of $p - 1$. Their product divides $(p - 1)/2$, so
$$N(p) = 1 + \sum_{i=1}^{k} N(q_i) < 1 + \sum_{i=1}^{k} \lg q_i \le 1 + \lg \frac{p - 1}{2} < \lg p.$$
So the list built in the completeness proof has fewer than $\lg n$ entries. $\blacksquare$
