from argparse import ArgumentParser
from email.message import EmailMessage
from itertools import combinations
from random import sample
import ssl
import smtplib
import yaml


def is_valid(chosen_edges, fam):
    assert len(chosen_edges) == len(fam)

    givers = {x[0] for x in chosen_edges}
    receivers = {x[1] for x in chosen_edges}

    assert givers == fam
    assert receivers == fam
    return True


def draw(fam, couples):
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

        chosen_edge = (giver, receiver)
        chosen_edges.append(chosen_edge)

        already_giving.add(giver)
        already_receiving.add(receiver)

    if not is_valid(chosen_edges, fam):
        return None
    else:
        return tuple(sorted(chosen_edges))


def get_valid_draw(fam, couples):
    out_draw = None
    while out_draw is None:
        out_draw = draw(fam, couples)
    return out_draw


def get_message(santa, elf, santa_email, sender_address):
    msg = EmailMessage()
    msg.set_content(
        f"Hey {santa}, get a gift for {elf} this year! 🤫🤐😉\n\nMerry Christmas! 🎅🤶🎄🦌🎁"
    )
    msg["Subject"] = "TOP SECRET"
    msg["From"] = sender_address
    msg["To"] = santa_email
    return msg


def main(test=True):
    with open("config.yml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    pwd = config["pwd"]
    user = config["user"]
    emails = config["email"]
    couples = [set(couple) for couple in config["couples"]]
    fam = set(emails.keys())

    secret_santas = get_valid_draw(fam, couples)

    if test:
        server = smtplib.SMTP("localhost", 1025)

        for santa, elf in secret_santas:
            print(f"From: {emails[santa]}; To: {elf}")

    else:
        port = 465  # For SSL
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
        server.login(user, pwd)

    for santa, elf in secret_santas:
        santa_email = emails[santa]
        message = get_message(santa, elf, santa_email, user)
        server.send_message(message)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    main(test=args.test)
