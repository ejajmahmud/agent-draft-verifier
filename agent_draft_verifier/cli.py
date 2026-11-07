"""CLI for agent-draft-verifier."""
import sys
import argparse
from .verifier import AgentDraftVerifier


def dummy_critic(context: str, token: str) -> bool:
    # Reject forbidden or hallucinated words
    return token.lower() not in ["hallucination", "crash", "buggy"]


def main():
    parser = argparse.ArgumentParser(description="Agent Draft Verifier")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        verifier = AgentDraftVerifier(dummy_critic)
        tokens = ["The", "database", "migration", "was", "hallucination", "completed"]
        summary = verifier.verify_tokens("Deploying service:", tokens)
        print(f"Verification summary: {summary.to_dict()}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
