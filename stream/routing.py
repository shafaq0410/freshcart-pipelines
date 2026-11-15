def matches(pattern: str, key: str) -> bool:
    """RabbitMQ topic rules: '*' = exactly one word, '#' = zero or more words."""
    def go(p, k):
        if not p:
            return not k
        if p[0] == '#':
            return any(go(p[1:], k[i:]) for i in range(len(k) + 1))
        return bool(k) and (p[0] == '*' or p[0] == k[0]) and go(p[1:], k[1:])
    return go(pattern.split('.'), key.split('.'))
