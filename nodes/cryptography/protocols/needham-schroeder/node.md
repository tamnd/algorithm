---
tag: 0T48C0
kind: algorithm
slug: needham-schroeder
name: Needham-Schroeder lineage and protocol analysis
aliases:
- Needham-Schroeder lineage
area: cryptography/protocols
level: advanced
summary: How the 1978 Needham-Schroeder protocols led to the 1987 nonce fix, BAN logic, Kerberos and Lowe's attack, with a bounded Dolev-Yao model checker that finds that attack.
solves: [reachability-problem]
model: word-ram
complexity:
  vars: {k: the number of sessions in the scenario, c: the number of typed inputs tried for one receive, m: the total size of the terms in a state}
  time: {worst: O((3c)^k k c m), average: O((3c)^k k c m), best: O(k^2 c m)}
  space: {extra: O((3c)^k m)}
properties: {deterministic: true, randomized: false}
history:
  year: 1995
  people: [Roger Needham, Michael Schroeder, Danny Dolev, Andrew Yao, Michael Burrows, Martin Abadi, Gavin Lowe]
  note: The protocols are from 1978 and the intruder model from 1983; Lowe found the attack on the public-key protocol in 1995 by model checking a small system with FDR.
prereqs: [needham-schroeder-protocol, explicit-state-model-checking]
see_also: [key-distribution-center, kerberos, denning-sacco-protocol, otway-rees-protocol, yahalom-protocol, entity-authentication, bounded-model-checking, depth-first-search]
sources:
  - paper: doi:10.1145/359657.359659
    title: Roger M. Needham and Michael D. Schroeder, Using encryption for authentication in large networks of computers, Communications of the ACM 21(12), 1978, pages 993 to 999
    locator: the authentication server with shared keys, the public-key protocol with a key directory, and the warning that such protocols are prone to subtle errors
  - paper: "Roger M. Needham and Michael D. Schroeder, Authentication revisited, ACM SIGOPS Operating Systems Review 21(1), January 1987"
    locator: the fix of the shared-key protocol in which the responder's nonce is placed inside the ticket (page number to check)
  - paper: "Dorothy E. Denning and Giovanni Maria Sacco, Timestamps in key distribution protocols, Communications of the ACM 24(8), August 1981, pages 533 to 536"
    locator: the replay of an old ticket after the compromise of its session key, and timestamps as the fix
  - paper: "Michael Burrows, Martin Abadi and Roger Needham, A logic of authentication, Proceedings of the Royal Society of London A 426, 1989, pages 233 to 271"
    locator: the BAN logic of belief, its rules, and the analyses of the Needham-Schroeder, Kerberos, Otway-Rees and Yahalom protocols
  - paper: doi:10.1145/77648.77649
    title: Michael Burrows, Martin Abadi and Roger Needham, A logic of authentication, ACM Transactions on Computer Systems 8(1), 1990, pages 18 to 36
    locator: the shorter journal version of the BAN logic
  - paper: doi:10.1109/TIT.1983.1056650
    title: Danny Dolev and Andrew C. Yao, On the security of public key protocols, IEEE Transactions on Information Theory 29(2), 1983, pages 198 to 208
    locator: the intruder who controls the network and can apply only the cryptographic operations whose keys it holds
  - paper: "Gavin Lowe, An attack on the Needham-Schroeder public-key authentication protocol, Information Processing Letters 56(3), 1995, pages 131 to 133"
    locator: the attack in which the intruder uses a run that the initiator starts with it to pose as the initiator to a third party (pages to check)
  - paper: "Gavin Lowe, Breaking and fixing the Needham-Schroeder public-key protocol using FDR, TACAS 1996, LNCS 1055, Springer, pages 147 to 166"
    locator: the CSP model, the attack found by FDR on a small system, the fixed protocol with the responder's name in message 2, and the argument that the small system suffices
  - paper: "Michael Rusinowitch and Mathieu Turuani, Protocol insecurity with a finite number of sessions, composed keys is NP-complete, Theoretical Computer Science 299, 2003, pages 451 to 475"
    locator: the decision procedure for a bounded number of sessions and its complexity
---

In 1978 Needham and Schroeder published two key distribution protocols, one with shared keys and an authentication server, and one with public keys. The [Needham-Schroeder protocol](/needham-schroeder-protocol/) page gives their steps and the two classic attacks. This page follows what came after: the trusted server model that became the [key distribution center](/key-distribution-center/), the fixes with nonces and timestamps that led to [Kerberos](/kerberos/), the BAN logic that tried to reason about such protocols, the Dolev-Yao intruder model, and Lowe's discovery in 1995, by model checking, of an attack on the public-key protocol that had gone unseen for 17 years. The algorithm on this page is a small bounded model checker in the Dolev-Yao model. It searches all interleavings of a few sessions, finds Lowe's attack on the public-key protocol (NSPK), and finds no attack on Lowe's fixed version (NSL) within the same bound.

**Notation.** $A$ and $B$ are honest agents and $I$ is the intruder, which is also a registered agent with its own key pair. $\{m\}_{pk(X)}$ is $m$ encrypted with the public key of $X$, which only $X$ can open. $N_a$, $N_b$ are nonces, written $N1, N2, \ldots$ in the code, and $N_i$ is the intruder's nonce. $K$ is the set of terms that the intruder knows. A *session* is one run of one role by one agent; a *scenario* is a finite list of sessions; $k$ is their number.

## In plain words

In 1978 two researchers wrote down how computers could use a trusted server, or public keys, to set up secret conversations. Their short protocols looked right. Over the next twenty years, people found that they were not.

First, someone showed that an old stolen key could be replayed. The authors added a fresh random number, and others used clocks instead, which became Kerberos. Then a logic was invented to prove such protocols correct, but it missed a problem. In 1995, a researcher let a computer try every way in which a cheating party could mix and forward messages between honest parties. It found that a dishonest party could make Bob believe he was talking to Alice.

This page builds a small version of that computer search, and shows that the fixed protocol passes it.

## The problem

Given a protocol, a finite scenario of sessions, and security goals, decide whether an intruder who controls the network can reach a state in which a goal fails. The intruder can read, block and replay every message, and can build new messages from what it knows, but it can open $\{m\}_{pk(X)}$ only if it holds the private key of $X$ (the Dolev-Yao model, 1983). The goals checked here are *agreement*, that when an honest agent finishes a run with an honest partner, the partner ran the protocol with it on the same nonces, and *secrecy* of the nonces of such runs. With a bounded number of sessions this is a reachability question on a finite graph; Rusinowitch and Turuani (2003) showed that it is NP-complete for a bounded number of sessions in a broader model. With an unbounded number of sessions it is undecidable in general.

## The algorithm

```pseudo id=main
search(protocol, scenario)
L1  stack ← [(the start state of each session, close(the intruder's initial knowledge), empty trace)];  seen ← ∅
L2  while stack is not empty:
L3      (S, K, tr) ← pop(stack)
L4      if (S, K) ∈ seen: continue;  add (S, K) to seen
L5      if a goal fails in (S, K): return the attack tr
L6      for each session whose next step is a send of m (the initiator's first message):
L7          push (S with the session advanced, close(K ∪ {m}), tr + [send m])
L8      for each session whose next step is a receive of a pattern p, then a reply r:
L9          for each typed choice σ of the variables of p (nonces of the scenario or Ni; agent names):
L10             if derive(K, pσ): push (S advanced with σ, close(K ∪ {rσ}), tr + [receive pσ, send rσ])
L11 return "no attack within this scenario"
close(K)
L12 repeat: add the parts of each tuple in K, and the body of each {m}pk(I) in K, until nothing is new
derive(K, t)
L13 true if t ∈ K, or t is a tuple whose parts all derive, or t = {m}pk(X) and m derives
```

**States.** A state holds, for each session, its step and the values it has received, together with the intruder knowledge $K$. All messages go through the intruder, so each sent message is added to $K$ (lines L7 and L10). The search is an [explicit-state](/explicit-state-model-checking/) [depth-first search](/depth-first-search/) with a stack and a set of visited states (lines L1 to L4), so it covers every interleaving of the sessions.

**The intruder.** The knowledge $K$ is kept closed under analysis (line L12): the intruder splits tuples and opens what is encrypted for $I$. Whether the intruder can send a message $t$ is then a check of synthesis (line L13): it can send any term in $K$, and it can pair and encrypt what it can derive, with any public key. Analysis before synthesis is enough, because taking apart a term that the intruder has just built gives nothing new.

**Typed inputs.** An honest agent accepts only messages of its expected form, so the candidates in line L9 are the pattern with each nonce variable set to one of the scenario's nonces or $N_i$, and each name variable set to $A$, $B$ or $I$. All nonces that the intruder could invent behave alike, so one, $N_i$, is enough.

**Goals.** Line L5 checks every finished session whose partner is honest. For a responder that finished believing its partner is $A$, there must be an initiator session of $A$ with that responder as partner, with the same two nonces. Neither nonce of such a run may be in $K$.

**About the code.** The Python code models NSPK and NSL with the three messages $\{N_a, A\}_{pk(B)}$, $\{N_a, N_b\}_{pk(A)}$ (NSL: $\{N_a, N_b, B\}_{pk(A)}$) and $\{N_b\}_{pk(B)}$. Encryption is symbolic and perfect; there is no real cryptography. It is a teaching tool, not a verifier: use Tamarin, ProVerif or Scyther to analyse a real protocol. There are no official test vectors for such a checker; the test compares the trace with the attack in Lowe's papers.

## Example

The scenario has two sessions: $A$ as initiator with partner $I$, and $B$ as responder. The search returns this trace for NSPK, which is Lowe's attack.

| Step | Event | Intruder learns | Note |
|---|---|---|---|
| 1 | A sends $\{N1, A\}_{pk(I)}$ | $N1$ | $A$ wants to talk to $I$ |
| 2 | B receives $\{N1, A\}_{pk(B)}$ | | built by $I$ from $N1$ and $A$ |
| 3 | B sends $\{N1, N2\}_{pk(A)}$ | nothing | $I$ cannot open it |
| 4 | A receives $\{N1, N2\}_{pk(A)}$ | | forwarded; $A$ thinks it is from $I$ |
| 5 | A sends $\{N2\}_{pk(I)}$ | $N2$ | $A$ answers $I$, as the protocol says |
| 6 | B receives $\{N2\}_{pk(B)}$ | | built by $I$; $B$ finishes with partner $A$ |

In the last state, $B$ believes that it ran the protocol with $A$, but $A$ ran it with $I$: agreement fails. And $N2$, which $B$ takes as a secret shared with $A$, is in $K$: secrecy fails. The search reaches this state after visiting 28 states.

With NSL, step 3 sends $\{N1, N2, B\}_{pk(A)}$. In her run with $I$, $A$ expects $\{N1, z, I\}_{pk(A)}$, so she rejects the forwarded message, and the intruder cannot make the expected one because it cannot learn $N2$. The search visits all 29 reachable states and finds no attack.

Over all 83 scenarios with one to three sessions of $A$ and $B$ in either role, the search finds an attack on NSPK in 14 scenarios and in none for NSL. Each attacked scenario has an initiator who talks to $I$ and an honest responder, as Lowe's attack needs. The 3-session runs take less than a second in Python.

## Correctness

**Claim.** For a given scenario in the typed model, the search returns a trace exactly when an attack exists, and each trace it returns is an attack. *Soundness*: each transition pushed in lines L7 and L10 is a step that the model allows, because by the analysis-then-synthesis lemma, derive on the closed knowledge says exactly what the intruder can deduce; the trace is returned only when a goal fails. *Completeness*: every intruder nonce can be renamed to $N_i$ without changing which messages honest agents accept, so line L9 tries every value that an attack could use, and a depth-first search with a visited set reaches every reachable state, because the moves from a state depend only on the state. *Termination*: each session has finitely many local states, and $K$ is a function of the session states. The proof page gives the details.

**What the bound means.** A result of no attack covers only the scenarios searched. Lowe argued in 1996 that for NSL an attack on any system gives an attack on the small system he checked. Tools that handle an unbounded number of sessions, such as ProVerif and Tamarin, prove NSL secure in the symbolic model. Warinschi (2003) showed that NSL is secure in a computational model when the encryption is IND-CCA2, and not with every IND-CPA scheme.

## Complexity

Each session has at most three local states and binds at most $c$ value choices, so it has $O(c)$ local states, and the knowledge is a function of the session states. The number of reachable states is therefore at most $(3c)^k$. Each state tries $O(k c)$ inputs, and each derive or closure costs $O(m)$ set operations, so the worst-case time is $O((3c)^k k c m)$ and the visited set takes $O((3c)^k m)$ space. When an attack lies on the first path that the depth-first search takes, it stops after $O(k)$ states, for $O(k^2 c m)$ time. The exponential growth in $k$ is the state explosion of explicit-state model checking; tools such as OFMC and Tamarin reduce it with symbolic (lazy) intruders and constraint solving.

## Properties

- **Exact within the model.** The result is exact for the given scenario and the typed Dolev-Yao model.
- **Only a bounded search.** It does not prove security for more sessions.
- **Typed.** It assumes that agents can tell nonces, names and keys apart. Untyped models allow type-flaw attacks; tagging each field with its type, as Heather, Lowe and Schneider showed in 2000, makes the typed analysis valid.
- **Perfect cryptography.** It ignores the algebra of real encryption, so attacks that need malleability, such as those in Warinschi's analysis, are out of its reach.
- **Deterministic.** The search order is fixed, so the same input gives the same trace.

## Variants and improvements

**The lineage of the shared-key protocol.**

- **1978.** Needham and Schroeder introduce the authentication server that shares a key with each principal, which is the model of every later [key distribution center](/key-distribution-center/), and a public-key version in which the server holds a directory of public keys. They warn that such protocols are prone to subtle errors.
- **1981.** Denning and Sacco show that in the shared-key protocol the responder cannot tell a fresh ticket from an old one, so an attacker who learns an old session key can replay its ticket. They propose timestamps in place of the responder's nonce check ([Denning-Sacco protocol](/denning-sacco-protocol/)).
- **1987.** In "Authentication revisited", Needham and Schroeder fix the protocol without clocks: the responder first sends a nonce, sealed under its key with the server, and the server puts that nonce inside the ticket, so the responder knows that the ticket is fresh.
- **1988.** Kerberos takes the timestamp route: each ticket has an expiry time and each authenticator a timestamp, checked against a clock skew window and a replay cache.
- **Otway-Rees (1987), Yahalom, and the wide-mouthed frog.** Other designs from this time move the work between the parties and the server; see [Otway-Rees](/otway-rees-protocol/), [Yahalom](/yahalom-protocol/) and the [wide-mouthed frog protocol](/wide-mouthed-frog-protocol/).

**The lineage of the analysis.**

- **Dolev and Yao (1983)** define the intruder that this page uses: it controls the network and can use only the keys it holds.
- **BAN logic (1989, 1990).** Burrows, Abadi and Needham reason about what each principal *believes*, with rules such as "if $P$ sees a message encrypted under a key it shares with $Q$, $P$ believes that $Q$ once said it" and "if $P$ believes a message is fresh and that $Q$ once said it, $P$ believes $Q$ believes it". Applied to the shared-key protocol, the logic makes the Denning-Sacco problem visible: the proof needs the assumption that $B$ believes the session key is fresh. BAN found redundancies and flaws in several protocols. But it has no model of an honest agent who runs a session with a dishonest one, and its analysis of the public-key protocol did not show Lowe's attack. Its idealization step, which turns messages into formulas, was also criticized as a source of error.
- **Lowe (1995, 1996).** Lowe wrote the protocol in CSP and searched a small system with the FDR model checker, which found the attack in the example above. The fix adds the responder's name to message 2. This made model checking a standard method for protocols.
- **Later tools.** Paulson's inductive method in Isabelle (1998), ProVerif (Blanchet 2001), Scyther (Cremers 2008) and Tamarin (2012) handle unbounded sessions with symbolic reasoning, and the same models were later used for TLS 1.3 and Signal.

## When to use it

Use a small search like this to learn how symbolic analysis works, or to test a toy protocol design before a real analysis. For a real protocol, use a maintained tool such as Tamarin or ProVerif, which handle unbounded sessions, Diffie-Hellman algebra and equational theories. Use the lineage above as a list of the classic mistakes: missing freshness for one party, missing names in messages, and trust in clocks.

## Pitfalls

- **Concluding security from a bounded search.** Line L11 says "no attack within this scenario", not "secure". An attack may need more sessions.
- **Too strong a typing assumption.** If the implementation does not check types, line L9 misses type-flaw attacks.
- **Goals that are too weak.** Secrecy of $N_b$ alone would also find Lowe's attack, but other attacks break only agreement, and some only injective agreement, which line L5 does not check: a replayed run that matches an old run passes non-injective agreement.
- **Forgetting the intruder as an agent.** Lowe's attack needs $A$ to start an honest session with $I$. A model in which only honest agents run sessions misses it; the scenarios must include sessions with dishonest partners.
- **Analysis after synthesis.** The closure in line L12 must run each time new terms enter $K$; checking derive on a set that is not closed misses messages that the intruder can open.

## Implementations

## History

Needham and Schroeder published both protocols in 1978. Denning and Sacco found the replay on the shared-key protocol in 1981, and Needham and Schroeder fixed it with an extra nonce in 1987, while Kerberos (1988) used timestamps. Dolev and Yao defined the intruder model in 1983. Burrows, Abadi and Needham published the BAN logic in 1989 and 1990. In 1995 Gavin Lowe published the attack on the public-key protocol, 17 years after the protocol appeared, and in 1996 described how FDR found it and proved the fixed protocol, now called Needham-Schroeder-Lowe. The attack became the standard first example for every protocol analysis tool.

## References
