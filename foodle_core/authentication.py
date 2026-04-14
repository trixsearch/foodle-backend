"""
DRF token auth using the Authorization: Bearer <token> header (frontend convention).
Default DRF uses the "Token" keyword; this matches typical SPA / OAuth-style headers.
"""

from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'
