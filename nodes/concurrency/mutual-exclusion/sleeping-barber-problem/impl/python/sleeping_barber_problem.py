# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sleeping-barber-problem/. The authors are listed in prov/PY293Y.jsonl.

"""The sleeping barber with N chairs, as procsim models.

  naive       the barber looks at the waiting count and sleeps if it is 0;
              a customer sits down and wakes the barber. The look and the
              sleep are two steps, so a wakeup can be lost.
  semaphores  the textbook solution: customers = 0, barbers = 0, mutex = 1,
              and the count waiting, protected by mutex.
  rendezvous  the same, plus a semaphore done, so that a customer leaves
              only after its haircut has ended.

The barber is a daemon that loops for ever; customers c0, c1, ... arrive once
each. A customer that finds all N chairs taken leaves at once.

Precondition: chairs >= 1. Cost: O(1) semaphore operations per customer;
the exhaustive tests visit at most a few thousand states.
"""

from typing import Iterator

from procsim import Sim


def _get(var: str):
    def f(s: Sim):
        return s.v[var]
    return f


def _add(var: str, d: int):
    def f(s: Sim) -> int:
        s.v[var] += d
        return s.v[var]
    return f


def _cut_start(s: Sim) -> None:
    s.v["cutting"] += 1


def _cut_end(s: Sim) -> None:
    s.v["cutting"] -= 1
    s.v["cuts"] += 1


def _arrive(chairs: int):
    """Under the mutex: sit down if a chair is free. Returns the ticket, or 0 to leave."""
    def f(s: Sim) -> int:
        if s.v["waiting"] < chairs:
            s.v["waiting"] += 1
            s.v["seated"] += 1
            return s.v["seated"]
        s.v["turned_away"] += 1
        return 0
    return f


def barber_naive(sim: Sim, me: str) -> Iterator[tuple]:
    while True:
        if (yield ("atomic", _get("waiting"))) == 0:
            yield ("sleep",)
        yield ("P", "mutex")
        yield ("atomic", _add("waiting", -1))
        yield ("V", "mutex")
        yield ("atomic", _cut_start)
        yield ("atomic", _cut_end)


def customer_naive(sim: Sim, me: str, chairs: int) -> Iterator[tuple]:
    yield ("P", "mutex")
    ticket = yield ("atomic", _arrive(chairs))
    yield ("V", "mutex")
    if ticket:
        yield ("wakeup", "barber")
        yield ("await", lambda s: s.v["cuts"] >= ticket)
        yield ("atomic", _add("left_served", 1))


def barber_sem(sim: Sim, me: str, rendezvous: bool) -> Iterator[tuple]:
    while True:
        yield ("P", "customers")  # sleep until a customer arrives
        yield ("P", "mutex")
        yield ("atomic", _add("waiting", -1))
        yield ("V", "barbers")  # call one customer to the chair
        yield ("V", "mutex")
        yield ("atomic", _cut_start)
        yield ("atomic", _cut_end)
        if rendezvous:
            yield ("V", "done")


def customer_sem(sim: Sim, me: str, chairs: int, rendezvous: bool) -> Iterator[tuple]:
    yield ("P", "mutex")
    ticket = yield ("atomic", _arrive(chairs))
    if ticket:
        yield ("V", "customers")  # wake the barber if he sleeps
        yield ("V", "mutex")
        yield ("P", "barbers")  # wait until the barber calls
        if rendezvous:
            yield ("P", "done")
        yield ("atomic", _add("left_served", 1))
    else:
        yield ("V", "mutex")  # the shop is full: leave


def build(kind: str, chairs: int, customers: int) -> Sim:
    s = Sim()
    for name in ("waiting", "seated", "turned_away", "cutting", "cuts", "left_served"):
        s.v[name] = 0
    s.semaphore("mutex", 1)
    if kind == "naive":
        s.spawn("barber", barber_naive, daemon=True)
        for i in range(customers):
            s.spawn(f"c{i}", customer_naive, chairs)
        return s
    rendezvous = kind == "rendezvous"
    assert kind in ("semaphores", "rendezvous"), kind
    s.semaphore("customers", 0)
    s.semaphore("barbers", 0)
    s.semaphore("done", 0)
    s.spawn("barber", barber_sem, rendezvous, daemon=True)
    for i in range(customers):
        s.spawn(f"c{i}", customer_sem, chairs, rendezvous)
    return s


def shop_rules(chairs: int):
    """Safety: at most `chairs` customers wait, and one haircut at a time."""
    def check(s: Sim):
        if not 0 <= s.v["waiting"] <= chairs:
            return f"waiting = {s.v['waiting']}"
        if s.v["cutting"] > 1:
            return "two haircuts at once"
        return None
    return check


def served_after_cut(s: Sim):
    """A served customer leaves only after a haircut has ended for it."""
    if s.v["left_served"] > s.v["cuts"]:
        return f"{s.v['left_served']} customers left after only {s.v['cuts']} haircuts"
    return None
