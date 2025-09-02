from __future__ import annotations
from pathlib import Path

def retrieve(query: str, top_k: int = 2) -> list[str]:
    # TODO: real embeddings; for now, return any markdown snippet
    snippets = []
    for p in Path("knowledge").glob("**/*.md"):
        snippets.append(p.read_text(encoding="utf-8")[:300])
        if len(snippets) >= top_k:
            break
    return snippets
