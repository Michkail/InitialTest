from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import pyotp


class TwoFactorSetupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not user.otp_secret:
            user.otp_secret = pyotp.random_base32()
            user.save()

        otp_uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(user.username, issuer_name="Karpous")

        return Response({"otp_uri": otp_uri})

class TwoFactorVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        totp = pyotp.TOTP(request.user.otp_secret)

        if totp.verify(code):
            request.user.two_factor_enabled = True
            request.user.save()

            return Response({"status": "2FA verified"})
        
        return Response({"status": "Invalid code"}, status=400)
