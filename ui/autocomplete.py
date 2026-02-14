OPKEYS = ["DELTA", "ASSERT", "QUERY", "EMIT"]
OPTYPES = {
    "DELTA": ["set", "add", "slide"],
    "QUERY": ["get", "overall"],
    "EMIT": ["signal"],
}

COMMON_KEYS = [
    "mood.happy",
    "mood.anxious",
    "mood.calm",
    "focus.depth",
    "memory.short_term.load",
    "thought",
]
