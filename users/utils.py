import re


def subdomain_to_schema_name(subdomain: str) -> str:
    """Normalize subdomain string to a valid PostgreSQL schema name fragment."""
    s = subdomain.strip().lower().replace('-', '_')
    s = re.sub(r'[^a-z0-9_]', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return (s or 'tenant')[:63]
