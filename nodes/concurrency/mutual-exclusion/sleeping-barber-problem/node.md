---
tag: PY293Y
kind: problem
slug: sleeping-barber-problem
name: Sleeping barber problem
aliases:
- sleeping barber
- barbershop problem
area: concurrency/mutual-exclusion
level: core
summary: A barber sleeps when no customer waits, and a shop has N chairs. Coordinate barber and customers with no lost wakeup, no deadlock and no overfull room. Dijkstra, 1965.
history:
  year: 1965
  people: [Edsger W. Dijkstra]
  note: Dijkstra told the barber story in Cooperating Sequential Processes (EWD 123) to show a counting semaphore built from binary ones. The version with N chairs is the textbook form.
prereqs: [semaphore, bounded-buffer-problem]
see_also: [bounded-buffer-problem, semaphore, condition-variable, monitor, deadlock, race-condition, readers-writers-problem, cigarette-smokers-problem]
sources:
  - url: "https://www.cs.utexas.edu/~EWD/transcriptions/EWD01xx/EWD123.html"
    title: Edsger W. Dijkstra, Cooperating Sequential Processes, EWD 123, 1965
    locator: the end of Section 4.2, The Superfluity of the General Semaphore, where the barber story illustrates a general semaphore built from the binary semaphores buffer manipulation and consumer delay and the integer numqueupor
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition (2015)
    locator: Chapter 2, the section on classical IPC problems, the sleeping barber problem with CHAIRS, the semaphores customers, barbers and mutex, and the count waiting
  - url: "https://greenteapress.com/wp/semaphores/"
    title: Allen B. Downey, The Little Book of Semaphores, version 2.2
    locator: Chapter 5, the section The barbershop problem, with n chairs, the rendezvous between barber and customer, and the FIFO barbershop
---

In the sleeping barber problem, a barber shop has one barber, one barber chair, and a waiting room with $N$ chairs. When there are no customers, the barber sleeps in his chair. A customer who arrives wakes the barber if he sleeps, sits in a free waiting chair if he is busy, and leaves at once if all $N$ chairs are taken. Dijkstra told the story in 1965, and the problem is now the standard example of how [semaphores](/semaphore/) avoid the lost wakeup: the [race condition](/race-condition/) in which the barber decides to sleep, a customer arrives and tries to wake him before he is asleep, and both then wait for ever.

## In plain words

A barber cuts hair. When the shop is empty he takes a nap. A new customer must wake him up. If he is busy, the customer sits down to wait, but there are only a few chairs, and when they are all taken the customer goes home.

The trap is timing. The barber looks at the room, sees nobody, and is about to lie down. Just then a customer comes in, sees the barber awake, and sits down without waking him. The barber lies down. Now the barber sleeps and the customer waits, and nothing will ever change.

The fix is a counter that remembers each arrival, so the barber never sleeps while someone is waiting for him.

## Definition

The model has $n$ asynchronous processes in a sequentially consistent memory: one barber and $n - 1$ customers. A process may crash between steps, but the problem asks for nothing when one crashes inside the protocol. The shared objects are the count of waiting customers and the synchronization objects: counting [semaphores](/semaphore/) with P and V, or a [mutex](/mutex/) with [condition variables](/condition-variable/), or sleep and wakeup.

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes: the barber and $n - 1$ customers |
| $p, q$ | process names; $i, j$ index customers |
| $N$ | the number of chairs in the waiting room |
| $k$ | the contention: the number of customers in the shop |
| $m$ | the number of shared objects: the count and the semaphores |

The barber loops: wait for a customer, call him to the chair, cut his hair. A customer arrives once: if a waiting chair is free, he sits, waits to be called and gets his haircut; otherwise he leaves. A solution must have these properties.

- **Room bound** (safety): at most $N$ customers wait.
- **One haircut at a time** (safety): the barber cuts one customer's hair at a time.
- **No lost wakeup** (progress): if a customer waits, the barber does not sleep for ever; equivalently, the system has no state in which the barber sleeps and a customer waits for ever. This is [deadlock freedom](/deadlock-freedom/) for the shop.
- **Every seated customer is served**: a customer who sits down eventually gets a haircut. With a FIFO order of service this is [starvation freedom](/starvation-freedom/).

## Variants

- **Dijkstra's original.** In EWD 123 the waiting room has no stated number of chairs, so no customer is turned away. The story illustrates how two binary semaphores and a count can do the work of a counting semaphore, and the sliding door of the waiting room is the binary semaphore that protects the count.
- **$N$ chairs.** The version with a waiting room of $N$ chairs, in which a customer who finds them all taken leaves, is the textbook form (for example in Tanenbaum's book). It is a [bounded buffer](/bounded-buffer-problem/) of customers in which producers do not wait when the buffer is full.
- **The rendezvous.** In the textbook solution the customer and the barber only meet at the call; Downey's version adds semaphores so that the customer leaves only after the haircut has ended.
- **FIFO service.** Customers are served in order of arrival, with a queue of private semaphores.
- **Several barbers.** The barbershop with several barbers and a sofa (Hilzer's barbershop, in Downey's book) adds a cash register and more steps.

## Examples

**The lost wakeup.** In a naive solution the barber tests the count and then sleeps, in two steps, and a customer raises the count and then sends a wakeup; a wakeup sent to a process that is not asleep is lost.

```text
BARBER                                   CUSTOMER
loop                                     P(mutex)
  if waiting = 0 then sleep              if waiting < N then
  P(mutex); waiting := waiting - 1         waiting := waiting + 1; V(mutex)
  V(mutex)                                 wakeup(barber)
  cut hair                                 wait for the haircut
                                         else V(mutex) and leave
```

The search over all interleavings with one chair and one customer finds the deadlock: the barber reads waiting = 0; the customer sits down, sets waiting to 1 and sends a wakeup, which is lost because the barber is not yet asleep; the barber then sleeps. Now the barber sleeps with a customer in the room, and the customer waits for a haircut that never comes. Testing the count under the mutex does not help by itself, since the barber cannot sleep while he holds the mutex.

**The semaphore solution.** The textbook solution uses three semaphores: customers counts the waiting customers and starts at 0, barbers counts the barbers ready to cut and starts at 0, and mutex protects the count waiting and starts at 1.

```text
BARBER                                   CUSTOMER
loop                                     P(mutex)
  P(customers)    { sleep if none }      if waiting < N then
  P(mutex)                                 waiting := waiting + 1
  waiting := waiting - 1                   V(customers)   { wake the barber }
  V(barbers)      { call a customer }      V(mutex)
  V(mutex)                                 P(barbers)     { wait to be called }
  cut hair                                 get haircut
                                         else
                                           V(mutex)       { the shop is full }
```

The fix for the lost wakeup is that V(customers) is never lost: if the barber is not yet waiting, the semaphore keeps the count, and his next P(customers) goes straight through. The barber's "test and sleep" is one atomic P. The search finds no state with more than $N$ waiting, no two haircuts at once, and no deadlock, for one, two and three customers with one or two chairs, and with three customers and one chair it finds runs where a customer is turned away. Seeded random runs with three chairs and eight customers end with every customer served or turned away.

**The haircut is not a rendezvous.** In the textbook solution the customer may run "get haircut" and leave before the barber has started to cut, since nothing ties the two together; the search finds this with one customer. Downey's fix adds a semaphore that the barber signals when the haircut ends, and the customer waits on it before it leaves. With it, the search finds no customer that leaves before its haircut has ended.

## Known algorithms

| solution | primitives | lost wakeup | notes |
|---|---|---|---|
| naive sleep and wakeup | count, sleep, wakeup | yes | deadlocks |
| textbook semaphores | customers, barbers, mutex | no | customer and barber only meet at the call |
| semaphores with a rendezvous | adds a semaphore for the end of the haircut | no | customer leaves after the haircut |
| monitor | a mutex and conditions | no | the barber waits in a while loop on "a customer waits" |
| FIFO barbershop | a queue of private semaphores | no | serves in order of arrival |

With a [monitor](/monitor/), the barber does "while waiting = 0: wait(customerArrived)", and a [condition variable](/condition-variable/) wait releases the mutex and blocks in one atomic step, so the test and the sleep cannot be separated by a customer's signal. Each customer costs a constant number of semaphore operations: 2 P and 2 V in the textbook solution, or one P and one V if it leaves.

## Bounds

**Theorem.** In the semaphore solution, in every reachable state, $0 \le$ waiting $\le N$, and the barber never sleeps in P(customers) while waiting $> 0$.

*Proof.* waiting changes only under mutex: a customer raises it only after checking waiting $< N$, so it never exceeds $N$; the barber lowers it only after a P(customers), and each V(customers) follows one raise, so the number of completed P(customers) never exceeds the number of raises, and waiting never goes below 0. For the second part, let $r$ be the number of raises and $c$ the number of V(customers) done. Each raise is followed, still under mutex, by its V(customers), so $c = r$ whenever nobody holds mutex in between. The count of the semaphore customers is $c$ minus the number of completed P(customers), and waiting is $r$ minus the number of decrements. The barber decrements right after each completed P(customers), in the same critical section, so outside the critical sections the semaphore count equals waiting. If waiting $> 0$, the semaphore is positive, and P(customers) does not block. $\square$

A deadlock needs a state where no process can step. The barber can always step unless he waits in P(customers), which by the theorem means nobody waits; a waiting customer waits in P(barbers), and the barber does V(barbers) once for each customer he takes. So every seated customer is called, and with a FIFO semaphore for barbers, in the order in which they wait on it.

## Reductions

- The waiting room is a [bounded buffer](/bounded-buffer-problem/) of customers, with the barber as the only consumer and customers as producers who leave instead of waiting when the buffer is full. customers plays the role of full; there is no semaphore empty, since a full room makes the customer leave.
- The lost wakeup here is the same race as in the sleep and wakeup version of the bounded buffer. Both are fixed by making "test and sleep" atomic: a semaphore P, or a condition variable wait that releases the mutex as it blocks.
- The call (V(barbers) and P(barbers)) and the end of the haircut together are a rendezvous, which Downey builds from two semaphores.

## Applications

- **Server threads.** A worker thread that sleeps when its request queue is empty and is woken by each new request, with a bound on the queue and requests rejected when it is full, is a sleeping barber.
- **Device drivers.** A driver thread that sleeps until an interrupt handler signals new work has the same structure, and the same race if the check and the sleep are not atomic.
- **Teaching.** The problem is the standard example of the lost wakeup.

### History

Dijkstra told the story of the sleeping barber in "Cooperating Sequential Processes" (EWD 123, 1965), at the end of Section 4.2, The Superfluity of the General Semaphore. There he builds the effect of a general (counting) semaphore from two binary semaphores, buffer manipulation and consumer delay, and an integer numqueupor, whose value $-1$ means that the barber sleeps. His shop has a waiting room with one sliding door that closes either the entry or the exit, so only one person passes at a time; a barber who finds the room empty sleeps in one of its chairs, and a customer who finds him asleep wakes him. The room has no fixed number of chairs. Later textbooks, Tanenbaum's among them, gave the version with $N$ chairs and the semaphores customers, barbers and mutex. Downey's Little Book of Semaphores adds a rendezvous for the haircut, a FIFO version, and Hilzer's barbershop with several barbers.

### Exercises

1. In the naive solution, move "wakeup(barber)" before "waiting := waiting + 1". Is the wakeup still lost in some schedule?
2. Show that in the textbook solution two customers can both be called before either one sits in the barber chair. Does that break the rule "one haircut at a time"?
3. Make the service FIFO: a customer who sits down before another gets its haircut first.
4. Write the solution as a [monitor](/monitor/) with Mesa semantics. Where must the waits be in while loops?
5. Extend the semaphore solution to $B$ barbers. Which semaphores change?

## References
