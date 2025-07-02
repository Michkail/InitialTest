import logging

logger = logging.getLogger("audit")

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else None
        response = self.get_response(request)

        logger.info(f"[AUDIT] user={user} method={request.method} path={request.path} status={response.status_code}")
        return response
