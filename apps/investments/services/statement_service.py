import io
from reportlab.pdfgen import canvas
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model


class StatementService:
    def generate_pdf(self, user):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, f"Investment Summary for {user.username}")
        p.drawString(100, 780, f"Total Investments: {user.investments.count()}")
        p.showPage()
        p.save()
        buffer.seek(0)

        return buffer

    def send_email(self, user, pdf_buffer):
        email = EmailMessage(
            subject="Your Investment Statement",
            body="Attached is your latest portfolio summary.",
            to=[user.email]
        )
        email.attach("statement.pdf", pdf_buffer.read(), "application/pdf")
        email.send()

    def generate_and_send_all(self):
        User = get_user_model()

        for user in User.objects.all():
            pdf = self.generate_pdf(user)
            self.send_email(user, pdf)
