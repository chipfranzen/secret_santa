from collections import Counter
from enum import Enum, unique
from itertools import combinations
from random import sample


@unique
class fam(Enum):
    ANDREW = "andrew"
    CHIP = "chip"
    SARAH = "sarah"
    SCOTT = "scott"
    TERYN = "teryn"
    THAO = "thao"


fam_values = {x.value for x in fam}


couples = [{fam.CHIP, fam.THAO}, {fam.SCOTT, fam.TERYN}, {fam.SARAH, fam.ANDREW}]


def is_valid(chosen_edges):
    assert len(chosen_edges) == len(fam)

    givers = {x[0] for x in chosen_edges}
    receivers = {x[1] for x in chosen_edges}

    assert givers == fam_values
    assert receivers == fam_values
    return True


def draw():
    all_edges = combinations(fam, 2)

    valid_edges = [edge for edge in all_edges if set(edge) not in couples]

    chosen_edges = []
    n_edges = len(fam)
    already_giving = set()
    already_receiving = set()

    for _ in range(n_edges):
        left_to_pick = set(fam) - already_giving
        giver = sample(left_to_pick, 1)[0]
        invalid_receivers = already_receiving - {giver}
        edges_in_hat = [
            edge
            for edge in valid_edges
            if ((giver in edge) and (not any([p in invalid_receivers for p in edge])))
        ]

        try:
            chosen_edge = sample(edges_in_hat, 1)[0]
        except ValueError:
            return None
        valid_edges.remove(chosen_edge)
        receiver = next(filter(lambda x: x != giver, chosen_edge))

        chosen_edge = (giver.value, receiver.value)
        chosen_edges.append(chosen_edge)

        already_giving.add(giver)
        already_receiving.add(receiver)

    if not is_valid(chosen_edges):
        return None
    else:
        return tuple(sorted(chosen_edges))


def main():
    draws = [draw() for _ in range(100000)]

    valid_draws = [x for x in draws if x is not None]
    print(valid_draws[1])
    draw_counts = Counter(valid_draws)
    print(len(draw_counts.keys()))
    print(sorted(draw_counts.values()))


if __name__ == "__main__":
    main()
