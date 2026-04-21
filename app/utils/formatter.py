from app.schemas.resume_schema import ResumeInput


def serialize_input(data: ResumeInput) -> str:
    """
    Converts a validated ResumeInput Pydantic model into a structured
    plain-text block that is injected into the LangChain prompt template.
    """
    lines: list[str] = []

    # ── Personal Info ──────────────────────────────────────────────────────────
    lines.append("PERSONAL INFORMATION")
    lines.append(f"Name        : {data.name}")
    lines.append(f"Phone       : {data.phone}")
    lines.append(f"Email       : {data.email}")
    lines.append(f"Location    : {data.location}")

    # ── Profiles ───────────────────────────────────────────────────────────────
    if data.profiles:
        profile_str = " | ".join(
            f"{p.platform}: {p.link}" for p in data.profiles
        )
        lines.append(f"Profiles    : {profile_str}")
    else:
        lines.append("Profiles    : None")

    lines.append("")

    # ── Summary (optional hint) ────────────────────────────────────────────────
    if data.summary:
        lines.append("SUMMARY HINT (improve and expand this):")
        lines.append(data.summary)
        lines.append("")

    # ── Technical Skills ───────────────────────────────────────────────────────
    lines.append("TECHNICAL SKILLS")
    skills = data.skills
    if skills.languages:
        lines.append(f"Languages     : {skills.languages}")
    if skills.web_dev:
        lines.append(f"Web Dev       : {skills.web_dev}")
    if skills.ml_ai:
        lines.append(f"ML & AI       : {skills.ml_ai}")
    if skills.libraries:
        lines.append(f"Libraries     : {skills.libraries}")
    if skills.tools_dbs:
        lines.append(f"Tools & DBs   : {skills.tools_dbs}")

    lines.append("")

    # ── Projects ───────────────────────────────────────────────────────────────
    lines.append("PROJECTS")
    for idx, proj in enumerate(data.projects, start=1):
        lines.append(f"Project {idx}:")
        lines.append(f"  Role        : {proj.role}")
        lines.append(f"  Name        : {proj.name}")
        lines.append(f"  Description : {proj.description}")
        lines.append(f"  Tech Stack  : {proj.tech_stack}")
        if proj.impact:
            lines.append(f"  Impact      : {proj.impact}")
        lines.append("")

    # ── Education ──────────────────────────────────────────────────────────────
    lines.append("EDUCATION")
    for edu in data.education:
        lines.append(f"  Degree      : {edu.degree}")
        lines.append(f"  Institution : {edu.institution}")
        lines.append(f"  Year        : {edu.year}")
        if edu.score:
            lines.append(f"  Score       : {edu.score}")
        lines.append("")

    # ── Certifications ─────────────────────────────────────────────────────────
    if data.certifications:
        lines.append("CERTIFICATIONS & ACHIEVEMENTS")
        for cert in data.certifications:
            lines.append(f"  - {cert}")

    return "\n".join(lines)


def clean_output(raw: str) -> str:
    """
    Post-processes the LLM output to ensure consistent formatting.
    Normalizes spacing and trims whitespace, while preserving Markdown structure.
    """
    import re
    
    # Remove common AI-generated preamble/postamble if any (though prompt forbids it)
    # Just in case, trim everything before the first '#' and after the last content
    
    # Normalize multiple consecutive blank lines to a single blank line
    raw = re.sub(r"\n{3,}", "\n\n", raw)

    # Strip trailing whitespace per line
    cleaned_lines = [line.rstrip() for line in raw.splitlines()]

    return "\n".join(cleaned_lines).strip()
