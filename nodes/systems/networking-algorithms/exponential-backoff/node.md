---
tag: SRY509
kind: algorithm
slug: exponential-backoff
name: Exponential backoff
aliases:
- capped exponential backoff
- exponential backoff with jitter
area: systems/networking-algorithms
level: intro
summary: A retry policy that waits base·2^n after the n-th failure, up to a cap, and randomizes the wait (jitter) so that clients that failed together do not retry together.
model: asynchronous-model
complexity:
  vars: {n: the number of attempts}
  time: {best: Θ(n), worst: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1976
  people: [Robert M. Metcalfe, David R. Boggs]
  note: Ethernet doubled the range of its random retransmission delay after each collision. The same rule later became the standard retry policy for clients of network services.
prereqs: [geometric-series]
see_also: [binary-exponential-backoff, karn-algorithm, jacobson-rto-estimation, token-bucket, rate-limiter, load-shedding, polite-contention-manager, spin-lock]
sources:
  - url: https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
    title: Marc Brooker, Exponential Backoff And Jitter, AWS Architecture Blog, 2015 (a blog post)
    locator: the definitions of full jitter, equal jitter and decorrelated jitter, and the simulation of contending clients
  - url: https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
    title: Marc Brooker, Timeouts, retries, and backoff with jitter, Amazon Builders' Library
    locator: the sections on retries and backoff, and on jitter
  - paper: doi:10.1145/360248.360253
    title: Robert M. Metcalfe and David R. Boggs, Ethernet, Distributed packet switching for local computer networks, Communications of the ACM 19(7), 1976, 395-404
    locator: the section on collision control and the retransmission interval
  - url: https://www.rfc-editor.org/rfc/rfc6298
    title: RFC 6298, Computing TCP's Retransmission Timer, 2011
    locator: Section 5, rule 5.5 (back off the timer) and rule 2.5 (an upper bound)
  - url: https://sre.google/sre-book/addressing-cascading-failures/
    title: Betsy Beyer, Chris Jones, Jennifer Petoff and Niall Richard Murphy (eds.), Site Reliability Engineering, Chapter 22, Addressing Cascading Failures
    locator: the section on retries (randomized exponential backoff and limits on retries)
---

Exponential backoff is a retry policy: after the $n$-th failure in a row, a client waits about $\mathit{base} \cdot 2^n$ before it tries again, up to a maximum wait $\mathit{cap}$, and up to a maximum number of attempts. Modern versions add *jitter*, a random part of the wait, so that many clients that failed at the same moment do not retry at the same moment. Marc Brooker's 2015 blog post on the AWS Architecture Blog compares three kinds of jitter: full, equal and decorrelated. The same rule backs off the TCP retransmission timer and, as [binary exponential backoff](/binary-exponential-backoff/), resolves collisions in Ethernet.

## In plain words

A call to a service fails. Maybe the service is overloaded. If you try again at once, you add to the load. So you wait 1 second. If it fails again, you wait 2 seconds, then 4, then 8, but never more than, say, a minute. After a fixed number of tries you give up.

If a thousand clients failed at the same moment and all wait exactly 1, 2, 4 seconds, they all come back at the same moments, and they fail together again. So each client picks a random wait between zero and the current limit. The clients then spread out, and most of them get through.

## The problem

A client calls a remote operation that fails for a while because of overload, contention or a short outage. The client must retry often enough to finish soon after the cause goes away, but its retries must not keep the overload alive. Many clients act at the same time and cannot talk to each other.

## The algorithm

The policy has a base delay, a cap, a maximum number of attempts, and a jitter mode.

```pseudo id=main
RETRY(operation, base, cap, attempts)
L1  for n ← 0 to attempts − 1 do
L2      if operation succeeds then return success
L3      if n = attempts − 1 then return failure
L4      v ← min(cap, base · 2^n)
L5      no jitter:     d ← v
L6      full jitter:   d ← uniform(0, v)
L7      equal jitter:  d ← v/2 + uniform(0, v/2)
L8      decorrelated:  d ← min(cap, uniform(base, 3 · previous d))   ▷ previous d starts at base
L9      wait d
```

The formulas in lines L6 to L8 are those of Brooker's post. Decorrelated jitter does not use $n$: each wait is drawn from a range that grows with the previous wait.

## Example

With $\mathit{base} = 1$, $\mathit{cap} = 100$ and no jitter, the waits are 1, 2, 4, 8, 16, 32, 64, 100, 100, ... . Before the cap, the total wait before attempt $n$ is $2^n - 1$. A call that fails four times and then succeeds waits $1 + 2 + 4 + 8 = 15$ in total. With a budget of 6 attempts and $\mathit{cap} = 8$, a call that always fails gives up after waiting $1 + 2 + 4 + 8 + 8 = 23$.

The value of jitter shows when many clients start together. In a slotted model, 20 clients try in slot 0, an attempt succeeds only if it is alone in its slot, a client that waits $d$ tries again in slot $\lfloor \mathit{now} + d \rfloor + 1$, $\mathit{base} = 1$, $\mathit{cap} = 1000$, and each client has 30 attempts. Averages over 30 seeds:

| jitter | clients that finish | attempts in total | slot of the last success |
|---|---|---|---|
| none | 0 | 600 | none |
| full | 20 | about 145 | about 141 |
| equal | 20 | about 147 | about 192 |
| decorrelated | 20 | about 147 | about 108 |

Without jitter, all 20 clients collide at every attempt and none finishes. With any jitter, all finish with about 7 attempts per client. In this model equal jitter takes the longest, which agrees with Brooker's simulation; his simulation found that full jitter uses slightly less work and decorrelated jitter slightly less time, and these differences depend on the model.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). Without jitter, the total wait before attempt $n$ is $\mathit{base}(2^n - 1)$ until the cap, so a client makes only $O(\log T)$ attempts in time $T$, and then one attempt per $\mathit{cap}$. Without jitter, clients that collide once collide forever, since they all compute the same waits; an induction on the attempts shows it. With full jitter, two clients that collide after a wait range of $v$ slots meet again with probability at most $1/v$, so the chance of $n$ more collisions in a row falls faster than any exponential.

## Complexity

Each attempt costs $O(1)$ work to compute the delay, and the policy keeps $O(1)$ state: the attempt number and, for decorrelated jitter, the previous delay. The total time to give up after $a$ attempts without jitter is $\mathit{base}(2^{a-1} - 1)$ until the cap is reached.

## Properties

- **Load falls fast.** A failing client sends fewer and fewer attempts, until the cap.
- **Cap.** Bounds the wait, so a client notices soon when the service is back.
- **Budget.** A maximum number of attempts or a deadline bounds the total time.
- **Jitter.** Breaks the synchrony of clients that failed together. Full jitter has mean $v/2$; equal jitter has mean $3v/4$ and never waits less than $v/2$.
- **Randomized.** With jitter, the policy is not deterministic; tests use a seeded generator.

## Variants and improvements

- **Other factors.** Any factor larger than 1 works; gRPC's connection backoff uses 1.6 with a jitter of 20 percent and a maximum of 120 s.
- **Binary exponential backoff.** Ethernet draws a whole number of slot times uniformly from $0$ to $2^{\min(n,10)} - 1$ and gives up after 16 attempts: see [binary exponential backoff](/binary-exponential-backoff/).
- **Timer backoff.** TCP doubles its retransmission timeout at each timeout (RFC 6298, rule 5.5) and keeps the doubled value until a valid sample: see [Karn's algorithm](/karn-algorithm/).
- **Retry budgets and token buckets.** Allow retries only while they are a small fraction of the requests, with a [token bucket](/token-bucket/), so that retries cannot multiply the load.
- **Server hints.** A server may say when to retry, for example with the HTTP header Retry-After.
- **Backoff in locks.** A [spin lock](/spin-lock/) may back off exponentially after a failed test-and-set, to reduce the traffic on the lock.

## When to use it

Use it for every retry of a call over a network: requests to an overloaded service, reconnects after a connection drops, polling for a resource that is not ready. Use jitter whenever more than one client can fail at the same time. Retry only operations that are safe to repeat.

## Pitfalls

- **No jitter.** Clients that failed together come back together, and each retry wave is as large as the first.
- **No cap or no budget.** The waits grow without limit, or a client retries forever.
- **Retries at every layer.** If each of three layers retries three times, one request can become 27 calls at the bottom. Retry at one layer.
- **Retrying operations that are not safe to repeat.** A retried payment may run twice. Use an idempotency key, or do not retry.
- **Waiting for the wrong errors.** Retry on overload and on timeouts, not on errors that will not go away, such as a bad request.

## Implementations

## History

Random retransmission delays came with the ALOHA network around 1970. Metcalfe and Boggs's Ethernet paper (1976) let each station adjust its mean retransmission interval to the load, by doubling it after each collision. TCP gained an exponential backoff of its retransmission timer in the work of Karn and Partridge (1987) and Jacobson (1988). For service clients, Marc Brooker's 2015 post on the AWS Architecture Blog showed by simulation why jitter matters, and the AWS SDKs use capped exponential backoff with jitter.

## References
