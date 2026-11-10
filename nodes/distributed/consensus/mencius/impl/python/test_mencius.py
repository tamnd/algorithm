# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mencius/. The authors are listed in prov/H2QGRY.jsonl.

from mencius import Mencius

CMDS = [f"c{i}" for i in range(12)]


def test_no_failures_uses_skips_and_no_revocation() -> None:
    for n in (3, 5):
        for seed in range(40):
            sim = Mencius(n, seed, CMDS, dup=0.1).run()
            assert not sim.violation
            assert sim.revocations == 0
            assert all(s.executed == sim.servers[0].executed for s in sim.servers)
            assert sorted(sim.servers[0].executed) == sorted(CMDS)


def test_one_busy_server_and_idle_servers_that_only_skip() -> None:
    for seed in range(30):
        sim = Mencius(3, seed, CMDS, clients_at=[0]).run()
        assert sim.servers[0].executed == CMDS
        assert all(s.executed == CMDS for s in sim.servers)
        assert sim.skips >= 2 * (len(CMDS) - 1)
        # Server 0 coordinates every instance that holds a command.
        assert all(v == "no-op" for j, v in sim.servers[1].learned.items() if j % 3)


def test_safety_with_crashes_false_suspicions_and_duplicates() -> None:
    for n, f in ((3, 1), (5, 2)):
        for seed in range(60):
            sim = Mencius(n, seed, CMDS, dup=0.1, crashes=f, crash_prob=0.01,
                          suspect_prob=0.02).run()
            assert not sim.violation, (n, seed)
            assert sim.logs_agree(), (n, seed)
            assert sim.no_duplicates(), (n, seed)


def test_crashed_coordinators_are_revoked() -> None:
    for n, f in ((3, 1), (5, 2)):
        for seed in range(60):
            sim = Mencius(n, seed, CMDS, crashes=f, crash_prob=0.02).run()
            assert not sim.violation and sim.logs_agree() and sim.no_duplicates()
            safe = [c for c, p in sim.sent_to.items() if p not in sim.crashed]
            assert sim.all_executed(safe), (n, seed)
            logs = [s.executed for s in sim.live()]
            assert all(lg == logs[0] for lg in logs), (n, seed)


def test_rule_4_resuggests_after_a_false_revocation() -> None:
    lost = 0
    for seed in range(40):
        sim = Mencius(3, seed, CMDS, suspect_prob=0.05).run()
        assert not sim.violation and sim.logs_agree() and sim.all_executed(), seed
        bad = Mencius(3, seed, CMDS, suspect_prob=0.05, no_rule4=True).run()
        lost += not bad.all_executed()
    assert lost > 0


def test_without_skips_an_idle_server_blocks_execution() -> None:
    stalled = 0
    for seed in range(20):
        sim = Mencius(3, seed, CMDS, clients_at=[0], no_skip=True, ticks=False).run()
        stalled += len(sim.servers[0].executed) < len(CMDS)
    assert stalled == 20


def test_revoking_without_reading_the_accepted_values_is_unsafe() -> None:
    bad = sum(Mencius(3, seed, CMDS, dup=0.1, suspect_prob=0.05, unsafe_revoke=True).run().violation
              for seed in range(60))
    assert bad > 0
