# Voting Management System on a Simple Blockchain

A menu-driven Python console application for registering candidates and voters,
casting votes, printing blocks and transactions, and validating a simple blockchain.

## Requirements and execution

Python 3.10 or newer. No third-party packages are required.

```console
python main.py
```

On Windows, `py main.py` also works if the Python launcher is installed.

## Menu

1. Add Candidate - register a unique candidate ID and a name.
2. Add Voter - register a unique voter ID and a name.
3. Cast Vote - select a registered candidate using a registered voter ID.
4. Print Blockchain - display each block, its transactions, timestamp, previous hash, and hash.
5. Validate Chain - verify block indices, recomputed hashes, links, and genesis contents.
6. Exit.

The menu repeats after each action until Exit is selected. Invalid input produces
an explanatory message and returns to the menu.

## Example demonstration

1. Choose 1; enter candidate ID `C1` and name `Alice`.
2. Choose 2; enter voter ID `V1` and name `Bob`.
3. Choose 3; enter voter ID `V1` and candidate ID `C1`.
4. Choose 4 to inspect the genesis block and the vote block.
5. Choose 5; the application reports `Blockchain is valid.`
6. Try voting again as `V1`; the application rejects double-voting.
7. Choose 6 to exit.

## Design

- `Voter` stores `voter_id`, `name`, and `has_voted`.
- `Candidate` stores `candidate_id` and `name`.
- `VotingSystem` keeps voters and candidates in dictionaries keyed by unique IDs.
- `Block` contains an index, UTC timestamp, transaction list, previous hash, and SHA-256 hash.
- `Blockchain` begins with a genesis block. Each accepted vote creates one new block.
- Hashes are calculated from deterministic JSON containing all block data except the hash itself.
- Chain validation recomputes each hash and checks its link to the preceding block.

Blank IDs/names, duplicate IDs, unknown voters/candidates, and repeat votes are
rejected before a vote is recorded. Leading/trailing whitespace is removed;
IDs are case-sensitive. A failed vote does not mark the voter as having voted.

## Tests

```console
python -m unittest -v
```

Tests cover successful voting, duplicate IDs, double-voting, unknown IDs, blank
fields, transaction tampering, broken hash links, genesis/index validation, and
the complete menu flow.

## Scope

This is a simple, single-process educational blockchain. Data is kept in memory
and resets when the application exits. Registration options are designated admin
actions in the menu; authentication is outside this assignment's minimum features.
There is no distributed consensus, proof of work, encryption, or secret ballot.
Votes contain voter IDs and are visible when printing the chain. Hash linking
detects edits that leave hashes or links inconsistent; someone controlling the
entire program can rewrite and rehash the chain. This demo is not intended for
real elections.

## GitHub submission

1. Create a GitHub repository named `blockchain-voting-system`.
2. Upload `main.py`, `test_voting.py`, `README.md`, and `.gitignore`.
3. Confirm the README and source files are visible in the repository.
4. Copy the repository URL from your browser and paste it into the assignment submission box.

Alternatively, from this folder, after creating an empty repository:

```console
git init
git add .
git commit -m "Complete blockchain voting assignment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/blockchain-voting-system.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username before running the remote command.
