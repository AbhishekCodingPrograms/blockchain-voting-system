"""Menu-driven educational voting system backed by a simple hash-linked chain."""

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json


@dataclass
class Voter:
    voter_id: str
    name: str
    has_voted: bool = False


@dataclass
class Candidate:
    candidate_id: str
    name: str


class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [Block(0, [{"type": "GENESIS"}], "0" * 64)]

    def add_transaction(self, transaction):
        self.chain.append(Block(len(self.chain), [transaction], self.chain[-1].hash))

    def validate(self):
        if not self.chain:
            return False
        for index, block in enumerate(self.chain):
            expected_previous = "0" * 64 if index == 0 else self.chain[index - 1].hash
            if (block.index != index or block.previous_hash != expected_previous
                    or block.hash != block.calculate_hash()):
                return False
        return self.chain[0].transactions == [{"type": "GENESIS"}]

    def print_chain(self):
        for block in self.chain:
            print(f"\n--- Block {block.index} ---")
            print(f"Timestamp:     {block.timestamp}")
            print("Transactions:")
            print(json.dumps(block.transactions, indent=2, ensure_ascii=False))
            print(f"Previous hash: {block.previous_hash}")
            print(f"Block hash:    {block.hash}")


class VotingSystem:
    def __init__(self):
        self.voters = {}
        self.candidates = {}
        self.blockchain = Blockchain()

    @staticmethod
    def required(value, label):
        value = value.strip()
        if not value:
            raise ValueError(f"{label} cannot be empty.")
        return value

    def add_candidate(self, candidate_id, name):
        candidate_id = self.required(candidate_id, "Candidate ID")
        name = self.required(name, "Candidate name")
        if candidate_id in self.candidates:
            raise ValueError("Candidate ID already exists.")
        self.candidates[candidate_id] = Candidate(candidate_id, name)

    def add_voter(self, voter_id, name):
        voter_id = self.required(voter_id, "Voter ID")
        name = self.required(name, "Voter name")
        if voter_id in self.voters:
            raise ValueError("Voter ID already exists.")
        self.voters[voter_id] = Voter(voter_id, name)

    def cast_vote(self, voter_id, candidate_id):
        voter_id = self.required(voter_id, "Voter ID")
        candidate_id = self.required(candidate_id, "Candidate ID")
        if voter_id not in self.voters:
            raise ValueError("Voter is not registered.")
        if candidate_id not in self.candidates:
            raise ValueError("Candidate does not exist.")
        if self.voters[voter_id].has_voted:
            raise ValueError("This voter has already voted.")
        if not self.blockchain.validate():
            raise ValueError("Blockchain validation failed; vote was not recorded.")
        self.blockchain.add_transaction({
            "type": "VOTE",
            "voter_id": voter_id,
            "candidate_id": candidate_id,
        })
        self.voters[voter_id].has_voted = True


MENU = """
=== Voting Management System ===
1. Add Candidate (admin action)
2. Add Voter (admin action)
3. Cast Vote
4. Print Blockchain
5. Validate Chain
6. Exit
"""


def main():
    system = VotingSystem()
    print("Educational demo: all data is held in memory for this session.")
    while True:
        try:
            print(MENU)
            choice = input("Enter your choice (1-6): ").strip()
            if choice == "1":
                system.add_candidate(input("Candidate ID: "), input("Candidate name: "))
                print("Candidate added successfully.")
            elif choice == "2":
                system.add_voter(input("Voter ID: "), input("Voter name: "))
                print("Voter added successfully.")
            elif choice == "3":
                if not system.candidates or not system.voters:
                    print("Register at least one candidate and one voter first.")
                    continue
                print("\nAvailable candidates:")
                for candidate in system.candidates.values():
                    print(f"  {candidate.candidate_id}: {candidate.name}")
                system.cast_vote(input("Voter ID: "), input("Candidate ID: "))
                print("Vote recorded successfully.")
            elif choice == "4":
                system.blockchain.print_chain()
            elif choice == "5":
                print("Blockchain is valid." if system.blockchain.validate()
                      else "Blockchain is INVALID: tampering or corruption detected.")
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 6.")
        except ValueError as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
