#!/usr/bin/env python3
"""Generate the public P5 Archive Manager evolution booklet and speaker sheet."""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, KeepTogether, Flowable, HRFlowable
)
from reportlab.pdfbase.pdfmetrics import stringWidth


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf"
OUTPUT.mkdir(parents=True, exist_ok=True)
BOOKLET = OUTPUT / "P5-Archive-Manager-Evolution.pdf"
TALKING = OUTPUT / "P5-Archive-Manager-Talking-Points.pdf"

NAVY = HexColor("#10253F")
BLUE = HexColor("#176B9B")
CYAN = HexColor("#39A6C8")
TEAL = HexColor("#1C8C84")
GREEN = HexColor("#2D936C")
ORANGE = HexColor("#E8872C")
RED = HexColor("#C64A46")
INK = HexColor("#17212B")
MUTED = HexColor("#586778")
PALE = HexColor("#F1F6F8")
PALE_BLUE = HexColor("#E8F3F8")
PALE_ORANGE = HexColor("#FFF3E5")
PALE_GREEN = HexColor("#EAF6F0")
LINE = HexColor("#C7D4DC")
WHITE = colors.white


def register_fonts():
    candidates = [
        ("Avenir", "/System/Library/Fonts/Avenir.ttc"),
        ("AvenirNext", "/System/Library/Fonts/Avenir Next.ttc"),
    ]
    for name, path in candidates:
        try:
            pdfmetrics.registerFont(TTFont(name, path, subfontIndex=0))
            return name
        except Exception:
            pass
    return "Helvetica"


FONT = register_fonts()
BOLD = "Helvetica-Bold"


def styles():
    s = getSampleStyleSheet()
    return {
        "title": ParagraphStyle("title", fontName=BOLD, fontSize=28, leading=31,
                                textColor=WHITE, spaceAfter=12),
        "subtitle": ParagraphStyle("subtitle", fontName=FONT, fontSize=12.5, leading=17,
                                   textColor=HexColor("#DCECF5")),
        "kicker": ParagraphStyle("kicker", fontName=BOLD, fontSize=8.5, leading=11,
                                 textColor=CYAN, tracking=1.1, spaceAfter=7),
        "h1": ParagraphStyle("h1", fontName=BOLD, fontSize=20, leading=24,
                             textColor=NAVY, spaceBefore=2, spaceAfter=10),
        "h2": ParagraphStyle("h2", fontName=BOLD, fontSize=13.5, leading=17,
                             textColor=BLUE, spaceBefore=9, spaceAfter=5),
        "body": ParagraphStyle("body", fontName=FONT, fontSize=9.5, leading=13.2,
                               textColor=INK, spaceAfter=7),
        "body_small": ParagraphStyle("body_small", fontName=FONT, fontSize=8.3,
                                     leading=11.1, textColor=INK, spaceAfter=5),
        "bullet": ParagraphStyle("bullet", fontName=FONT, fontSize=9.2, leading=12.5,
                                 textColor=INK, leftIndent=13, firstLineIndent=-8,
                                 bulletIndent=1, spaceAfter=4),
        "quote": ParagraphStyle("quote", fontName=BOLD, fontSize=13.5, leading=18,
                                textColor=NAVY, leftIndent=14, rightIndent=14,
                                spaceBefore=8, spaceAfter=10),
        "caption": ParagraphStyle("caption", fontName=FONT, fontSize=7.5, leading=9.5,
                                  textColor=MUTED, spaceBefore=4),
        "table": ParagraphStyle("table", fontName=FONT, fontSize=7.4, leading=9.5,
                                textColor=INK),
        "table_head": ParagraphStyle("table_head", fontName=BOLD, fontSize=7.4,
                                     leading=9, textColor=WHITE),
        "card_head": ParagraphStyle("card_head", fontName=BOLD, fontSize=11,
                                    leading=13, textColor=NAVY, spaceAfter=4),
        "card_num": ParagraphStyle("card_num", fontName=BOLD, fontSize=11,
                                   leading=13, textColor=WHITE, alignment=TA_CENTER),
        "card_body": ParagraphStyle("card_body", fontName=FONT, fontSize=8.5,
                                    leading=11, textColor=INK),
        "source": ParagraphStyle("source", fontName=FONT, fontSize=7.6, leading=10,
                                 textColor=MUTED, spaceAfter=4),
    }


ST = styles()


def P(text, style="body"):
    return Paragraph(text, ST[style])


def bullet(text):
    return Paragraph(text, ST["bullet"], bulletText="•")


class SectionBand(Flowable):
    def __init__(self, label, title, color=BLUE, height=54):
        super().__init__()
        self.label, self.title, self.color, self.height = label, title, color, height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.width, self.height, 7, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(BOLD, 8)
        c.drawString(14, self.height - 17, self.label.upper())
        c.setFont(BOLD, 17)
        c.drawString(14, 15, self.title)


class StageRail(Flowable):
    def __init__(self, stages, height=132):
        super().__init__()
        self.stages = stages
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def draw(self):
        c = self.canv
        n = len(self.stages)
        margin = 24
        step = (self.width - 2 * margin) / (n - 1)
        y = self.height - 36
        c.setStrokeColor(LINE)
        c.setLineWidth(3)
        c.line(margin, y, self.width - margin, y)
        colors_ = [ORANGE, CYAN, BLUE, TEAL, GREEN]
        for i, (year, title, note) in enumerate(self.stages):
            x = margin + i * step
            c.setFillColor(colors_[i % len(colors_)])
            c.circle(x, y, 8, fill=1, stroke=0)
            c.setFillColor(NAVY)
            c.setFont(BOLD, 8)
            c.drawCentredString(x, y + 18, year)
            c.setFont(BOLD, 7.6)
            for j, line in enumerate(title.split("|")):
                c.drawCentredString(x, y - 24 - j * 10, line)
            c.setFillColor(MUTED)
            c.setFont(FONT, 6.5)
            for j, line in enumerate(note.split("|")):
                c.drawCentredString(x, y - 51 - j * 8, line)


class WorkflowDiagram(Flowable):
    def __init__(self, height=410):
        super().__init__()
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def box(self, x, y, w, h, title, fill, fs=7.2):
        c = self.canv
        c.setFillColor(fill)
        c.setStrokeColor(colors.white)
        c.roundRect(x, y, w, h, 6, fill=1, stroke=0)
        c.setFillColor(NAVY if fill != NAVY else WHITE)
        c.setFont(BOLD, fs)
        lines = title.split("|")
        start = y + h / 2 + (len(lines) - 1) * 4
        for i, line in enumerate(lines):
            c.drawCentredString(x + w / 2, start - i * 9, line)

    def arrow(self, x1, y1, x2, y2):
        c = self.canv
        c.setStrokeColor(MUTED)
        c.setFillColor(MUTED)
        c.setLineWidth(1.2)
        c.line(x1, y1, x2, y2)
        import math
        ang = math.atan2(y2-y1, x2-x1)
        size = 4
        for off in (2.55, -2.55):
            c.line(x2, y2, x2 + size*math.cos(ang+off), y2 + size*math.sin(ang+off))

    def draw(self):
        c = self.canv
        w = self.width
        bw, bh = 126, 36
        center = (w - bw) / 2
        self.box(center, 362, bw, bh, "Choose server|and operator intent", NAVY)
        self.box(16, 300, bw, bh, "Folder check|enumerate local files", PALE_BLUE)
        self.box(center, 300, bw, bh, "Project file|or path list", PALE_ORANGE)
        self.box(w-bw-16, 300, bw, bh, "P5 stub|project original name", PALE_GREEN)
        self.arrow(center+bw/2, 362, 16+bw/2, 336)
        self.arrow(center+bw/2, 362, center+bw/2, 336)
        self.arrow(center+bw/2, 362, w-16-bw/2, 336)

        self.box(16, 234, bw, bh, "Mapped P5 path|then historical roots", PALE_BLUE)
        self.box(center, 234, bw, bh, "Resolve media|across indexes", PALE_ORANGE)
        self.box(w-bw-16, 234, bw, bh, "Confirm matching|archive entry", PALE_GREEN)
        self.arrow(16+bw/2, 300, 16+bw/2, 270)
        self.arrow(center+bw/2, 300, center+bw/2, 270)
        self.arrow(w-16-bw/2, 300, w-16-bw/2, 270)

        self.box(16, 168, bw, bh, "Restore-engine fallback|if path lookup fails", PALE_BLUE)
        self.box(center, 168, bw, bh, "Prepare versions, tapes|and destination", PALE_ORANGE)
        self.arrow(16+bw/2, 234, 16+bw/2, 204)
        self.arrow(center+bw/2, 234, center+bw/2, 204)
        self.arrow(w-16-bw/2, 234, center+bw, 186)

        self.box(16, 102, bw, bh, "Per-file verdict|and provenance", HexColor("#DDEEF6"))
        self.box(center, 102, bw, bh, "Submit and monitor|one restore job", HexColor("#FCE5CE"))
        self.arrow(16+bw/2, 168, 16+bw/2, 138)
        self.arrow(center+bw/2, 168, center+bw/2, 138)

        self.box(16, 34, 112, bh, "Verified|write proof", PALE_GREEN)
        self.box(center-56, 34, 112, bh, "Not archived|offer archive", PALE_ORANGE)
        self.box(w-128, 34, 112, bh, "Mismatch/uncertain|hold for review", HexColor("#F7E3E2"))
        self.arrow(16+bw/2, 102, 72, 70)
        self.arrow(16+bw/2, 102, center, 70)
        self.arrow(16+bw/2, 102, w-72, 70)
        c.setFillColor(MUTED)
        c.setFont(FONT, 7)
        c.drawCentredString(w/2, 4, "Failures remain undetermined; they are never converted into proof that a file is absent.")


class RelationshipDiagram(Flowable):
    def __init__(self, height=250):
        super().__init__()
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return availWidth, self.height

    def node(self, x, y, w, h, title, fill):
        c = self.canv
        c.setFillColor(fill)
        c.roundRect(x, y, w, h, 7, fill=1, stroke=0)
        c.setFillColor(WHITE if fill in (NAVY, BLUE, TEAL) else NAVY)
        c.setFont(BOLD, 7.5)
        lines = title.split("|")
        start = y+h/2+(len(lines)-1)*4
        for i, line in enumerate(lines):
            c.drawCentredString(x+w/2, start-i*9, line)

    def line(self, x1, y1, x2, y2, dash=None):
        c = self.canv
        c.setStrokeColor(MUTED)
        c.setLineWidth(1.3)
        c.setDash(dash or [])
        c.line(x1, y1, x2, y2)
        c.setDash([])

    def draw(self):
        w = self.width
        nw, nh, gap = 91, 44, 12
        total = 5*nw+4*gap
        x0 = (w-total)/2
        y = 170
        nodes = [
            ("Shell scripts|local nsdchat", ORANGE),
            ("Platypus app|+ swiftDialog", CYAN),
            ("SwiftUI app|bundled shell", BLUE),
            ("CLI 3.x|remote nsdchat", TEAL),
            ("API 4.x|REST + P5Kit", NAVY),
        ]
        for i, (title, fill) in enumerate(nodes):
            x = x0+i*(nw+gap)
            self.node(x, y, nw, nh, title, fill)
            if i:
                self.line(x-gap, y+nh/2, x, y+nh/2, [3,2] if i == 4 else None)
        api_x = x0+4*(nw+gap)
        cli_x = x0+3*(nw+gap)
        self.node(cli_x-4, 74, 99, 42, "nsdchat|port 9001", PALE_GREEN)
        self.node(api_x-10, 74, 111, 42, "P5 REST API v8|/rest/v1", PALE_BLUE)
        self.line(cli_x+nw/2, y, cli_x+nw/2, 116)
        self.line(api_x+nw/2, y, api_x+nw/2, 116)
        self.node((w-105)/2, 8, 105, 42, "Archiware P5|archive system", NAVY)
        self.line(cli_x+nw/2, 74, w/2-24, 50)
        self.line(api_x+nw/2, 74, w/2+24, 50)
        c = self.canv
        c.setFillColor(MUTED)
        c.setFont(FONT, 7)
        c.drawString(api_x-8, 141, "Separate successor, not an in-place upgrade")


class BookletDoc(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=LETTER, leftMargin=0.68*inch,
                         rightMargin=0.68*inch, topMargin=0.65*inch,
                         bottomMargin=0.58*inch, **kw)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="normal", frames=[frame], onPage=self.decorate)])

    def decorate(self, c, doc):
        if doc.page == 1:
            return
        c.saveState()
        c.setStrokeColor(LINE)
        c.line(doc.leftMargin, 0.42*inch, LETTER[0]-doc.rightMargin, 0.42*inch)
        c.setFont(FONT, 7.2)
        c.setFillColor(MUTED)
        c.drawString(doc.leftMargin, 0.25*inch, "P5 Archive Manager - Evolution of methodology and architecture")
        c.drawRightString(LETTER[0]-doc.rightMargin, 0.25*inch, str(doc.page))
        c.restoreState()


def cover_canvas(c, doc):
    pass


def table(data, widths, header=True, font=7.4, padding=5):
    converted = []
    for r, row in enumerate(data):
        converted.append([Paragraph(str(cell), ST["table_head"] if r == 0 and header else ST["table"]) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), padding),
        ("RIGHTPADDING", (0,0), (-1,-1), padding),
        ("TOPPADDING", (0,0), (-1,-1), padding),
        ("BOTTOMPADDING", (0,0), (-1,-1), padding),
        ("GRID", (0,0), (-1,-1), 0.4, LINE),
    ]
    if header:
        commands += [("BACKGROUND", (0,0), (-1,0), NAVY)]
        start = 1
    else:
        start = 0
    for r in range(start, len(data)):
        if r % 2 == 0:
            commands.append(("BACKGROUND", (0,r), (-1,r), PALE))
    t.setStyle(TableStyle(commands))
    return t


def page_heading(label, title, color=BLUE):
    return [SectionBand(label, title, color), Spacer(1, 14)]


def build_booklet():
    doc = BookletDoc(str(BOOKLET), title="From P5 Archive Check to P5 Archive Manager API",
                     author="macvfx", subject="Product evolution, methodology, security, and tools")
    story = []

    # Cover - implemented as a full-width dark panel inside the printable frame.
    story += [Spacer(1, 0.45*inch)]
    cover = Table([[
        Paragraph("P5 ARCHIVE TOOLS / PRODUCT HISTORY", ST["kicker"]),
    ], [
        Paragraph("From P5 Archive Check<br/>to P5 Archive Manager API", ST["title"]),
    ], [
        Paragraph("How a local shell check became a multi-server, evidence-driven archive, delete, and restore application.", ST["subtitle"]),
    ]], colWidths=[doc.width-0.7*inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), NAVY),
        ("LEFTPADDING", (0,0), (-1,-1), 26),
        ("RIGHTPADDING", (0,0), (-1,-1), 26),
        ("TOPPADDING", (0,0), (-1,0), 24),
        ("BOTTOMPADDING", (0,2), (-1,2), 30),
    ]))
    story += [cover, Spacer(1, 24), StageRail([
        ("2025", "Shell|script", "local|nsdchat"),
        ("2025", "Platypus|+ dialog", "drag and drop|app wrapper"),
        ("2025-26", "SwiftUI|+ CLI", "remote server|manager"),
        ("Jun 2026", "REST API|prototype", "proof, delete|and archive"),
        ("Nov 2026", "API 4.5", "restore and|site config"),
    ]), Spacer(1, 12), P("Public source and Git-history review through P5 Archive Manager API 4.5.0 (build 67), released 2026-11-10.", "caption"), PageBreak()]

    story += page_heading("01 / Executive overview", "The real evolution was methodological", BLUE)
    story += [P("The app did not begin as a conventional product. It began as one operational question:"),
              P("For every file under this folder, can Archiware P5 return an ArchiveEntry handle?", "quote"),
              P("That question stayed at the centre of the product, but the standard of evidence changed. The first tools classified files by handle presence. The current API app models local files, archived paths, verification verdicts, server trust, mutation jobs, receipts, and restoration intent."),
              Spacer(1, 5)]
    cards = [
        [P("THEN", "kicker"), P("NOW", "kicker")],
        [P("Handle or no handle", "card_head"), P("Per-file proof and verdict", "card_head")],
        [P("One local server and default index", "card_body"), P("Multiple servers, indexes, mappings, historical roots, and imported volumes", "card_body")],
        [P("Reports after a check", "card_body"), P("Proof before delete, immediate re-verification, receipt after action", "card_body")],
        [P("Manual restore elsewhere", "card_body"), P("Project-file restore, path-list restore, and direct stub restore", "card_body")],
    ]
    ct = Table(cards, colWidths=[doc.width/2-4, doc.width/2-4], hAlign="LEFT")
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), PALE_ORANGE), ("BACKGROUND", (1,0), (1,-1), PALE_BLUE),
        ("BOX", (0,0), (0,-1), 0.6, ORANGE), ("BOX", (1,0), (1,-1), 0.6, CYAN),
        ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    story += [ct, Spacer(1, 14), P("The UI changed several times, but the deeper transition was from a script that answered a question to an application that can justify, perform, and record consequential actions."), PageBreak()]

    story += page_heading("02 / Timeline", "Five generations, one continuous problem", TEAL)
    timeline = [
        ["Date", "Generation", "Method and capability change"],
        ["2025-11-13", "P5 Check shell script", "Published the local-server find -> handle -> metadata workflow. Added swiftDialog progress, reports in /Users/Shared, and a tarball of intermediate evidence."],
        ["Nov 2025", "Platypus app", "Turned the drag-and-drop script into a Mac app bundle. Better access and feedback; the execution engine remained shell plus local nsdchat."],
        ["Nov 2025", "Basic SwiftUI app", "Made folder drop, progress, and output presentation native app state. The Swift interface still launched a bundled checker script."],
        ["2025-11-20 to 11-23", "Remote nsdchat manager", "Added named servers, ports, users, custom indexes, Keychain passwords, and remote awsock connections."],
        ["Feb-Apr 2026", "CLI 3.x product", "Added guarded deletion, proof links, typed confirmation, audit logs, partial delete, cancellation, and shared server configuration."],
        ["2026-06-14", "REST prototype", "Started a separate no-nsdchat app. The first day established local-driven checks, size verification, provenance, deep verify, receipts, and archive submission."],
        ["Jun-Jul 2026", "REST beta 0.x", "Added job evidence, multi-index/server support, logs, source-path metadata, path mappings, and historical roots."],
        ["Aug 2026", "CLI/API split formalised", "CLI stayed on stable 3.x. The separately installed REST successor became API 4.x, with distinct behaviour and update channels."],
        ["Sep 2026", "Native transport and TLS", "Moved REST transport to P5Kit/URLSession and Keychain access to Security APIs; added per-server certificate review and no-downgrade rules."],
        ["Sep-Nov 2026", "Restore and deployment", "Added project-file restore, imported-volume search, stub restore, Restore-engine fallback, and centrally deployable site settings."],
    ]
    story += [table(timeline, [0.86*inch, 1.25*inch, doc.width-2.11*inch]), PageBreak()]

    story += page_heading("03 / Early method", "The script was a transparent evidence pipeline", ORANGE)
    story += [P("The original method was easy to explain and inspect. It used ordinary shell tools to build a sequence of evidence files:"),
              bullet("Use <b>find</b> to enumerate local files, excluding metadata and P5 stub sidecars."),
              bullet("Call <b>nsdchat ArchiveEntry handle</b> for each path."),
              bullet("Separate paths with handles from paths without handles."),
              bullet("For each handle, request status, size, archive time, volume, and barcode."),
              bullet("Assemble a CSV with <b>paste</b>, write a not-archived list, preserve a log, and bundle intermediate files."),
              Spacer(1, 7), P("What Platypus and swiftDialog changed", "h2"),
              P("Platypus supplied the app shape: a drag target, an icon, and a distributable bundle. swiftDialog supplied visible progress. Neither changed how P5 was queried. This distinction matters because a native-looking interface did not yet mean a native archive engine."),
              Spacer(1, 7)]
    early = [
        ["Strength", "Limit"],
        ["Direct, understandable command sequence", "Per-file and per-field command count grows quickly"],
        ["Human-readable intermediate evidence", "Predictable shared temp files can collide or retain stale data"],
        ["Local P5 access needs no remote credential", "Newline-delimited shell and CSV assembly are fragile around unusual names"],
        ["Easy to wrap as drag and drop", "Wrapper dependencies do not remove shell trust boundaries"],
    ]
    story += [table(early, [doc.width/2, doc.width/2]), PageBreak()]

    story += page_heading("04 / Native interface, CLI engine", "Swift changed the interface before the engine", CYAN)
    story += [P("The first Swift app made the workflow feel like a product: selected folder, progress state, server picker, output list, and settings. But its engine contract was still a bundled shell script."),
              P("Remote operation was the next major step. The app stored a password in Keychain, built an awsock connection, passed it to the child process, and called remote nsdchat on port 9001. This preserved the proven handle-by-path method while separating the operator Mac from the P5 server."),
              Spacer(1, 8)]
    cli_changes = [
        ["CLI-era addition", "Methodological effect"],
        ["Named servers and selectable indexes", "Made the target explicit and reusable"],
        ["Proof links and typed DELETE confirmation", "Placed a human review gate before destructive action"],
        ["Archived-file list", "Separated deletion candidates from the general report"],
        ["Partial delete", "Allowed proven files to be removed while retaining unarchived files"],
        ["Cancellation and progress parsing", "Made long checks operable rather than opaque"],
        ["Broken-link reporting and run-folder diagnostics", "Reduced ambiguous failures and stale-output mistakes"],
        ["Reviewed server discovery", "Stopped configuration files from silently changing the server list"],
    ]
    story += [table(cli_changes, [1.7*inch, doc.width-1.7*inch]), Spacer(1, 10),
              P("Security boundary", "h2"),
              P("Keychain protected the password at rest, but the secret still crossed into a subprocess environment and an awsock connection string. The app also depended on a fixed nsdchat installation and on files as the interface between engine and UI."), PageBreak()]

    story += page_heading("05 / REST foundation", "The API app became an evidence and action system", BLUE)
    story += [P("The REST implementation was created as a separate application, not as an in-place transport patch. It kept the product goal while changing the data model, query strategy, and safety architecture."),
              Spacer(1, 5)]
    rest = [
        ["Change", "Why it matters"],
        ["Local-driven directory inventory", "Enumerates disk first and queries only P5 directories that can hold those files"],
        ["Per-file exact / close / mismatch / absent verdict", "Makes delete eligibility explicit instead of equating handle presence with proof"],
        ["Proof report before delete", "Evidence exists even if a later mutation fails"],
        ["Immediate candidate re-verification", "Catches local changes between check and delete"],
        ["Archive job ID, manifest, and report", "Turns a submission into a traceable operation"],
        ["Path mappings and historical roots", "Separates where a project lives now from where P5 indexed it"],
        ["Multi-index and alternate-source search", "Finds media under imported volumes or after relocation"],
        ["Project and stub restore", "Connects archive evidence to editorial recovery intent"],
    ]
    story += [table(rest, [1.82*inch, doc.width-1.82*inch]), Spacer(1, 10),
              P("The conceptual jump", "h2"),
              P("The old question was: <b>Does P5 know this path?</b> The new question is: <b>What evidence supports the action we are about to take?</b>"), PageBreak()]

    story += page_heading("06 / Current workflow", "One entry point, three operator intents", TEAL)
    story += [WorkflowDiagram(), Spacer(1, 7), P("The current application keeps the fast path fast. Broader searches are fallbacks, not the default. A transport or authentication failure remains undetermined and cannot become evidence for archive or delete.", "caption"), PageBreak()]

    story += page_heading("07 / Product relationships", "Successor lineage without forced migration", NAVY)
    story += [RelationshipDiagram(), Spacer(1, 12),
              P("P5 Archive Manager CLI 3.x and P5 Archive Manager API 4.x can coexist. They have different bundle identities, settings, transports, workflows, and update channels. The REST app inherits the operational lessons of the CLI line, but it is not the same executable with a protocol switch."),
              P("The architecture also became more modular. The API app owns local comparison, mappings, verdicts, UI, receipts, and job orchestration; P5Kit supplies shared transport and REST contracts; Archiware P5 remains the system of record."),
              Spacer(1, 8)]
    rel = [
        ["Component", "Responsibility"],
        ["Main Check", "Fast local-versus-P5 comparison and per-file provenance"],
        ["Restore search engine", "Broader name, imported-volume, catalogue, TSV, and relocated-media resolution"],
        ["Receipt store", "Proof, deletion outcomes, archive reports, and optional external mirror"],
        ["Server and site settings", "Connections, trust, mappings, historical roots, and repeatable deployment"],
        ["P5Kit / URLSession", "Request transport, shared REST models, cancellation, and server-file contracts"],
    ]
    story += [table(rel, [1.65*inch, doc.width-1.65*inch]), PageBreak()]

    story += page_heading("08 / Security", "The trust model became visible and enforceable", RED)
    security = [
        ["Generation", "Security gain", "Residual concern"],
        ["Shell / Platypus", "Local operation and transparent evidence files", "Shared predictable temp names; shell and filename parsing; sensitive reports"],
        ["Remote nsdchat Swift", "Per-server Keychain storage; explicit server/index; destructive-action gates", "Credential expanded into subprocess environment and awsock string; external binary dependency"],
        ["REST API current", "Security APIs; in-memory Authorization header; TLS pin or system trust; no downgrade; no redirects; reviewed imports; proof and receipts", "HTTP remains possible; fingerprints require independent verification; mutations can have uncertain timeout outcomes"],
    ]
    story += [table(security, [1.16*inch, 2.43*inch, doc.width-3.59*inch]), Spacer(1, 12),
              P("Current safety controls", "h2"),
              bullet("Passwords and certificate pins are excluded from server and site exports."),
              bullet("An imported HTTPS server arrives unpinned and must be reviewed locally."),
              bullet("HTTPS failures do not fall back to HTTP, and redirects are refused."),
              bullet("Authentication and connectivity failures stop classification instead of becoming 'not archived'."),
              bullet("Delete is limited to eligible verdicts, writes proof first, re-verifies, and records every outcome."),
              bullet("Archive plans that delete files or folders at source are detected and blocked by default."),
              Spacer(1, 5), P("Operational cautions", "h2"),
              P("Archive, delete, and restore remain real mutations. A timeout can mean the server accepted a job even when the client missed the response. Do not blindly repeat a submission; reconcile against P5 jobs and the saved evidence. Stopping local monitoring does not necessarily stop a server-side job."), PageBreak()]

    story += page_heading("09 / Tool history", "Each tool change removed a specific constraint", CYAN)
    tools = [
        ["Layer", "Early", "Current API", "Reason"],
        ["UI", "Terminal; Platypus + swiftDialog", "Native SwiftUI workflows", "Explicit state, choices, and mutation review"],
        ["Discovery", "find -> text files", "FileManager + typed models", "Avoid file-protocol and silent subtree loss"],
        ["P5 access", "local/remote nsdchat", "REST v8 via P5Kit/URLSession", "Portability and richer workflows"],
        ["Query", "one handle per path", "directory inventory + layered fallback", "Fewer calls and relocated-media recovery"],
        ["Credentials", "local or awsock subprocess", "Security APIs + in-memory header", "Remove password-bearing process transport"],
        ["Trust", "CLI/network assumption", "HTTP/HTTPS + system trust or pin", "Per-server, visible transport policy"],
        ["Evidence", "CSV, text, log, tar", "Typed state plus proof, receipts, reports", "Human evidence without temp files as protocol"],
        ["Restore", "manual/external", "Project, path-list, and stub restore", "Editorially informed recovery"],
        ["Testing", "manual inspection", "Contract, filename, mapping, TLS, and live probes", "Separate source confidence from live acceptance"],
    ]
    story += [table(tools, [0.72*inch, 1.33*inch, 1.61*inch, doc.width-3.66*inch], padding=4), PageBreak()]

    story += page_heading("10 / What stayed constant", "The first script contained the product's durable ideas", GREEN)
    story += [P("The modern application is not a rejection of the shell tool. It is the original method made explicit, testable, and safe enough to support consequential actions."), Spacer(1, 8)]
    constants = [
        [P("01", "card_num"), P("Start with the files the operator actually has", "card_head")],
        [P("02", "card_num"), P("Ask P5 for evidence rather than infer archive state locally", "card_head")],
        [P("03", "card_num"), P("Keep archived and not-archived results separately inspectable", "card_head")],
        [P("04", "card_num"), P("Preserve logs and evidence for troubleshooting", "card_head")],
        [P("05", "card_num"), P("Make long-running operations visible", "card_head")],
    ]
    ct = Table(constants, colWidths=[0.55*inch, doc.width-0.55*inch])
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), NAVY), ("TEXTCOLOR", (0,0), (0,-1), WHITE),
        ("BACKGROUND", (1,0), (1,-1), PALE), ("GRID", (0,0), (-1,-1), 0.5, LINE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("TOPPADDING", (0,0), (-1,-1), 12), ("BOTTOMPADDING", (0,0), (-1,-1), 12),
    ]))
    story += [ct, Spacer(1, 17), P("The shortest accurate summary", "h2"),
              P("P5 Archive Manager evolved from a local path checker into a multi-server decision and recovery system. The core question remained the same; the quality of proof, the range of paths, and the responsibility of the actions changed."), PageBreak()]

    story += page_heading("11 / Evidence and boundaries", "Source-backed history, bounded claims", MUTED)
    story += [P("Primary evidence", "h2"),
              P("macvfx/p5ArchiveCheck - original shell scripts, README, and public Git history", "source"),
              P("https://github.com/macvfx/p5ArchiveCheck", "source"),
              P("macvfx/p5ArchiveManager - public README, API guide, lineage document, and release notes", "source"),
              P("https://github.com/macvfx/p5ArchiveManager", "source"),
              P("Local CLI and API source histories - changelogs, request/job trace, credential and TLS assessments, tests, Keychain helper, request client, restore service, and receipt store", "source"),
              P("macvfx.blog - Platypus, swiftDialog, signing/notarization, and move-to-native-Swift context", "source"),
              P("https://macvfx.blog/", "source"),
              Spacer(1, 12), P("Evidence boundary", "h2"),
              P("Repository history proves when public files and implementations were recorded. It does not necessarily prove the first private experiment or first production use. Build and automated-test success do not prove every P5 plan, network, certificate, delete, archive, or restore workflow in production."),
              P("Current scope: P5 Archive Manager API 4.5.0 (build 67), released 2026-11-10. The 4.x line remains beta in the reviewed public documentation."),
              Spacer(1, 16), HRFlowable(width="100%", color=LINE), Spacer(1, 10),
              P("Canonical source document", "h2"),
              P("docs/P5-ARCHIVE-MANAGER-EVOLUTION.md in the public P5 Archive Manager repository.", "source")]

    doc.build(story)


def draw_wrapped(c, text, x, y, width, font, size, leading, color=INK, max_lines=None):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if stringWidth(trial, font, size) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if max_lines:
        lines = lines[:max_lines]
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def build_talking_points():
    c = canvas.Canvas(str(TALKING), pagesize=LETTER)
    W, H = LETTER
    c.setTitle("P5 Archive Manager - Talking Points and Fun Facts")
    c.setAuthor("macvfx")
    c.setFillColor(NAVY)
    c.rect(0, H-108, W, 108, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont(BOLD, 8.5)
    c.drawString(42, H-35, "ONE-PAGE SPEAKER SHEET")
    c.setFillColor(WHITE)
    c.setFont(BOLD, 22)
    c.drawString(42, H-64, "P5 Archive Manager: talking points")
    c.setFont(FONT, 9.5)
    c.setFillColor(HexColor("#DCECF5"))
    c.drawString(42, H-84, "A shell script grew into an evidence-driven archive, delete, and restore system.")

    # 30-second story
    x, y, fullw = 42, H-132, W-84
    c.setFillColor(PALE_BLUE)
    c.roundRect(x, y-72, fullw, 72, 7, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.setFont(BOLD, 8)
    c.drawString(x+13, y-17, "THE 30-SECOND STORY")
    draw_wrapped(c,
        "It started with one practical question: can P5 return an archive handle for every file in this folder? The interface moved from shell to Platypus to SwiftUI, but the bigger change was from handle presence to defensible proof. Today the REST app can verify, archive, delete with receipts, and restore from project files or P5 stubs across multiple servers and historical storage paths.",
        x+13, y-33, fullw-26, FONT, 8.5, 10.8, INK)

    # Two columns of points
    col_gap = 16
    colw = (fullw-col_gap)/2
    left = x
    right = x+colw+col_gap
    top = y-91
    facts = [
        ("1", "The first algorithm is still recognizable", "Enumerate local files, ask P5 for evidence, separate archived from not archived, and preserve a report."),
        ("2", "A native-looking app was not yet a native engine", "Platypus and the first SwiftUI app improved access and feedback while the real work still ran in shell and nsdchat."),
        ("3", "The REST rewrite changed the unit of trust", "A handle became one input to a per-file verdict with size, date, volume, location, and provenance."),
        ("4", "The app writes proof before it deletes", "It then re-verifies each candidate and records every outcome in a receipt and audit log."),
        ("5", "Not found is not the same as not archived", "The app tries mapped paths, historical roots, imported volumes, catalogues, TSVs, and a bounded relocated-media search."),
        ("6", "A network failure cannot become a verdict", "Authentication or transport problems stop classification; they never turn into evidence that a file is absent."),
        ("7", "Project files became restoration maps", "XML, FCPXML, FCPXMLD, Resolve DRT, and path lists can drive one prepared restore job."),
        ("8", "RED media changes the restore unit", "A timeline may name one RED segment, but the app can restore the whole .RDC folder."),
        ("9", "CLI and API can live side by side", "CLI 3.x and API 4.x are separate apps and update channels, which makes migration a comparison rather than a forced replacement."),
        ("10", "The security story has its own evolution", "Keychain-at-rest became Security APIs, in-memory auth headers, explicit TLS trust, no downgrade, and no redirect replay."),
    ]

    def fact_card(fx, fy, num, head, body):
        h = 64
        c.setFillColor(PALE)
        c.roundRect(fx, fy-h, colw, h-4, 6, fill=1, stroke=0)
        c.setFillColor(CYAN if int(num)%2 else ORANGE)
        c.circle(fx+16, fy-18, 10, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont(BOLD, 8)
        c.drawCentredString(fx+16, fy-21, num)
        c.setFillColor(NAVY)
        c.setFont(BOLD, 8.2)
        c.drawString(fx+31, fy-14, head)
        draw_wrapped(c, body, fx+31, fy-27, colw-40, FONT, 7.1, 8.4, INK, 4)
        return fy-h

    ly = ry = top
    for i, fact in enumerate(facts):
        if i < 5:
            ly = fact_card(left, ly, *fact)
        else:
            ry = fact_card(right, ry, *fact)

    # Closing prompts
    base = 94
    c.setFillColor(PALE_ORANGE)
    c.roundRect(x, base, fullw, 66, 7, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.setFont(BOLD, 8)
    c.drawString(x+13, base+48, "GOOD QUESTIONS TO THROW INTO THE ROOM")
    c.setFillColor(INK)
    c.setFont(FONT, 7.8)
    c.drawString(x+13, base+32, "- What counts as enough proof to delete the local copy?")
    c.drawString(x+13, base+19, "- How many historical storage identities can one project accumulate?")
    c.drawString(x+265, base+32, "- What should happen after an uncertain submission timeout?")
    c.drawString(x+265, base+19, "- When is a native UI only a wrapper, and when is it a new architecture?")

    c.setStrokeColor(LINE)
    c.line(42, 70, W-42, 70)
    c.setFillColor(MUTED)
    c.setFont(FONT, 6.8)
    c.drawString(42, 54, "Source: public p5ArchiveCheck and p5ArchiveManager histories; reviewed through API 4.5.0 build 67 (2026-11-10).")
    c.drawRightString(W-42, 54, "Speaker sheet - public-safe")
    c.showPage()
    c.save()


if __name__ == "__main__":
    build_booklet()
    build_talking_points()
    print(BOOKLET)
    print(TALKING)
