"""Core Agent Draft Verifier implementation."""
from typing import List, Dict, Any, Callable


class VerificationSummary:
    def __init__(self, accepted_tokens: List[str], rejected_tokens: List[str], acceptance_rate: float):
        self.accepted_tokens = accepted_tokens
        self.rejected_tokens = rejected_tokens
        self.acceptance_rate = acceptance_rate

    def to_dict(self) -> Dict[str, Any]:
        return {
            "accepted_count": len(self.accepted_tokens),
            "rejected_count": len(self.rejected_tokens),
            "acceptance_rate": round(self.acceptance_rate, 3),
            "final_text": " ".join(self.accepted_tokens)
        }


class AgentDraftVerifier:
    def __init__(self, critic_validator: Callable[[str, str], bool]):
        self.critic_validator = critic_validator
        self.history: List[VerificationSummary] = []

    def verify_tokens(self, context: str, draft_tokens: List[str]) -> VerificationSummary:
        accepted = []
        rejected = []
        diverged = False

        for token in draft_tokens:
            if diverged:
                rejected.append(token)
                continue

            # Verify with critic
            if self.critic_validator(context, token):
                accepted.append(token)
                context = context + " " + token
            else:
                diverged = True
                rejected.append(token)

        total = len(draft_tokens)
        rate = (len(accepted) / total) if total > 0 else 0.0
        summary = VerificationSummary(accepted, rejected, rate)
        self.history.append(summary)
        return summary
