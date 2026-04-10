from flask import Flask, render_template, Response
import os
from fpdf import FPDF

app = Flask(__name__)

EVENTS = {
    "sparkathon": {
        "name": "Sparkathon",
        "short": "Build solutions for real-world problems in 24 hours.",
        "poster": "images/sparkathon_poster.jpg",
        "date": "April 20, 2026",
        "venue": "Seminar Hall, Block A – Navkis College of Engineering, Hassan",
        "prize_pool": "10,000",
        "theme": "AI for Social Good",
        "fee": "200 per team",
        "team_size": "3-5 members",
        "rules": [
            "All team members must be enrolled students of Navkis College.",
            "Teams must register before April 18, 2026.",
            "All code must be written during the hackathon window.",
            "Use of pre-built UI libraries is allowed; copy-pasted projects are not.",
            "Teams must present a working demo at the end.",
            "Decision of judges is final.",
        ],
        "google_form": "https://forms.gle/huQadNmQtjD4Xb5m8"
    },
    "escape-room": {
        "name": "Escape Room",
        "short": "Solve puzzles, crack codes, and escape before time runs out.",
        "poster": "images/escape_poster.jpg",
        "date": "April 21, 2026",
        "venue": "Conference Room, Block B – Navkis College of Engineering, Hassan",
        "prize_pool": "5,000",
        "theme": "Puzzle & Logic",
        "fee": "100 per team",
        "team_size": "2-4 members",
        "rules": [
            "No mobile phones allowed inside the room.",
            "Each team gets exactly 30 minutes.",
            "Hints can be requested twice per team.",
            "Physical damage to props leads to disqualification.",
            "Teams must wait outside until called.",
        ],
        "google_form": "https://forms.gle/SnMUzey9pE4KMHycA"
    },
    "big-bunty-hunt": {
        "name": "Big Bunty Hunt",
        "short": "Race across campus following clues in this epic treasure hunt.",
        "poster": "images/bunty_poster.jpg",
        "date": "April 22, 2026",
        "venue": "Navkis College Campus Grounds, Hassan",
        "prize_pool": "7,000",
        "theme": "Campus Treasure Hunt",
        "fee": "150 per team",
        "team_size": "3-5 members",
        "rules": [
            "Follow clues strictly in the given order.",
            "No searching outside the marked campus zones.",
            "Sharing clues with other teams leads to disqualification.",
            "The first team to complete all checkpoints wins.",
            "Coordinators decision is final in case of disputes.",
        ],
        "google_form": "https://forms.gle/amCMtMJJjRsVQgUMA"
    }
}

COMMON_RULES = [
    "All participants must carry their college ID cards at all times.",
    "Ragging, misbehaviour, or misconduct will lead to immediate disqualification.",
    "Participants must report 15 minutes before their event starts.",
    "Mobile phones must be on silent mode during all events.",
    "Decision of the organizing committee is final and binding.",
    "No refunds will be given after registration.",
    "Participants must follow all instructions given by coordinators.",
    "Any form of cheating will lead to disqualification of the entire team.",
]

EVENT_ORDER = ["sparkathon", "escape-room", "big-bunty-hunt"]

TEACHER_COORDINATORS = [
    {
        "name": "Prof. Teacher Name 1",
        "role": "Faculty Coordinator",
        "branch": "Computer Science Engineering",
        "phone": "+91 98765 43200",
        "email": "teacher1@navkis.edu.in",
        "photo": "images/teacher1.jpg"
    },
    {
        "name": "Prof. Teacher Name 2",
        "role": "Faculty Coordinator",
        "branch": "Electronics & Communication",
        "phone": "+91 98765 43201",
        "email": "teacher2@navkis.edu.in",
        "photo": "images/teacher2.jpg"
    },
]

PRESIDENT = [
    {
        "name": "President Name",
        "role": "President",
        "branch": "CSE",
        "sem": "6th Sem",
        "year": "3rd Year",
        "phone": "+91 98765 43210",
        "photo": "images/president.jpg"
    },
]

VICE_PRESIDENT = [
    {
        "name": "Vice President Name",
        "role": "Vice President",
        "branch": "ISE",
        "sem": "6th Sem",
        "year": "3rd Year",
        "phone": "+91 98765 43211",
        "photo": "images/vp.jpg"
    },
]

TECH_COORDINATORS = [
    {
        "name": "Tech Coord Name 1",
        "role": "Technical Coordinator",
        "branch": "CSE",
        "sem": "4th Sem",
        "year": "2nd Year",
        "phone": "+91 98765 43212",
        "photo": "images/tech1.jpg"
    },
    {
        "name": "Tech Coord Name 2",
        "role": "Technical Coordinator",
        "branch": "ISE",
        "sem": "4th Sem",
        "year": "2nd Year",
        "phone": "+91 98765 43213",
        "photo": "images/tech2.jpg"
    },
]

CLUB_MEMBERS = [
    {
        "name": "Member Name 1",
        "role": "Club Member",
        "branch": "CSE",
        "sem": "2nd Sem",
        "year": "1st Year",
        "phone": "+91 98765 43220",
        "photo": "images/member1.jpg"
    },
    {
        "name": "Member Name 2",
        "role": "Club Member",
        "branch": "ISE",
        "sem": "2nd Sem",
        "year": "1st Year",
        "phone": "+91 98765 43221",
        "photo": "images/member2.jpg"
    },
]


def generate_pdf(title, subtitle, details, rules, poster_path=None):
    def clean(text):
        return text.encode('latin-1', errors='replace').decode('latin-1')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    # ── HEADER ──
    pdf.set_fill_color(10, 10, 30)
    pdf.rect(0, 0, 210, 45, 'F')
    pdf.set_xy(0, 8)
    pdf.set_text_color(0, 220, 220)
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(210, 14, "TECHSPARK CLUB", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(210, 9, "Navkis College of Engineering, Hassan", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_y(52)
    # ── POSTER IMAGE ──
    if poster_path and os.path.exists(poster_path):
        img_x = 55
        img_w = 100
        pdf.image(poster_path, x=img_x, y=pdf.get_y(), w=img_w)
        pdf.ln(img_w * 1.45)
        pdf.set_draw_color(0, 180, 180)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(8)

    # ── TITLE ──
    pdf.set_text_color(0, 180, 180)
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, clean(title), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    if subtitle:
        pdf.set_font("Helvetica", "I", 11)
        pdf.set_text_color(100, 100, 160)
        pdf.cell(0, 8, clean(subtitle), align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    pdf.set_draw_color(0, 180, 180)
    pdf.set_line_width(0.5)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(8)

    # ── EVENT DETAILS ──
    if details:
        pdf.set_fill_color(230, 245, 255)
        pdf.set_font("Helvetica", "B", 13)
        pdf.set_text_color(0, 120, 140)
        pdf.cell(0, 9, "  Event Details", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.ln(4)

        for key, value in details.items():
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 50, 80)
            pdf.cell(42, 8, clean(key) + ":", new_x="RIGHT", new_y="TMARGIN")
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 8, clean(value), new_x="LMARGIN", new_y="NEXT")

        pdf.ln(4)
        pdf.set_draw_color(0, 180, 180)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(8)

    # ── RULES ──
    pdf.set_fill_color(230, 245, 255)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(0, 120, 140)
    pdf.cell(0, 9, "  Rules & Regulations", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(30, 30, 30)
    for i, rule in enumerate(rules, 1):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 140, 140)
        pdf.cell(8, 8, str(i) + ".", new_x="RIGHT", new_y="TMARGIN")
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(30, 30, 30)
        pdf.multi_cell(0, 8, clean(rule), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # ── FOOTER ──
    pdf.ln(4)
    pdf.set_draw_color(0, 180, 180)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, "TechSpark Club - Inspire, Innovate, Integrate", align="C")

    return bytes(pdf.output())
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/events")
def events():
    return render_template("events.html")
@app.route("/blackout")
def blackout():
    event_list = [(k, EVENTS[k]) for k in EVENT_ORDER]
    return render_template("blackout.html", event_list=event_list)

@app.route("/events/<event_id>")
def event_detail(event_id):
    event = EVENTS.get(event_id)
    if not event:
        return "Event not found", 404
    return render_template("event_detail.html", event=event, event_id=event_id)

@app.route("/events/<event_id>/download")
def download_event_rules(event_id):
    event = EVENTS.get(event_id)
    if not event:
        return "Event not found", 404
    details = {
        "Date": event["date"],
        "Venue": event["venue"],
        "Theme": event["theme"],
        "Prize Pool": "Rs. " + event["prize_pool"],
        "Entry Fee": "Rs. " + event["fee"],
        "Team Size": event["team_size"],
    }
    poster_path = os.path.join(
        app.static_folder, "images",
        os.path.basename(event["poster"])
    )
    pdf_bytes = generate_pdf(
        title=event["name"] + " - Rule Book",
        subtitle=event["short"],
        details=details,
        rules=event["rules"],
        poster_path=poster_path
    )
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={event_id}-rulebook.pdf"}
    )


@app.route("/rulebook")
def rulebook():
    return render_template("rulebook.html", common_rules=COMMON_RULES)

@app.route("/rulebook/download")
def download_rulebook():
    pdf_bytes = generate_pdf(
        title="TechSpark - Common Rule Book",
        subtitle="Rules applicable to all events",
        details=None,
        rules=COMMON_RULES
    )
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": "attachment; filename=techspark-common-rulebook.pdf"}
    )

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/coordinators")
def coordinators():
    return render_template("coordinators.html",
        teachers=TEACHER_COORDINATORS,
        president=PRESIDENT,
        vice_president=VICE_PRESIDENT,
        tech_coords=TECH_COORDINATORS,
        members=CLUB_MEMBERS)

if __name__ == "__main__":
    app.run(debug=True)