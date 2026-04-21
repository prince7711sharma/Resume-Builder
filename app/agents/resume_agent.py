from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm


RESUME_SYSTEM_PROMPT = """Senior Resume Writer AI for RS Education Solution.
Task: Generate premium, ATS-optimized resume in PLAIN TEXT.

STRICT RULES:
- Output ONLY the resume. No commentary.
- NO markdown formatting (no **, ##, *, `).
- Use blank lines between sections.
- Use strong action verbs (Developed, Engineered, etc.).
- Bullets: Use plain dash (-).
- Resume order: Header, Summary, Expertise, Tech Skills, Projects, Education, Certs.

STRUCTURE:
1. HEADER: FULL NAME (ALL CAPS) | (phone) | email | city, state | Profiles: link1 | link2
2. SUMMARY: 3-4 line paragraph. Cover current role, tech specialization, and impact.
3. EXPERTISE: Single line: Skill1 | Skill2 | Skill3
4. TECHNICAL SKILLS: (Labels: Languages:, Web Dev:, ML & AI:, Libraries:, Tools & DBs:)
5. FEATURED PROJECTS: (3 minimum) Role | Project Name. 3 bullets each: Action, Tech, Quantified Impact.
6. EDUCATION: DEGREE | INSTITUTION | YEAR. Score/GPA: [x] (if available).
7. CERTS & ACHIEVEMENTS: Professional bullets.

USER DATA:
{user_data}

GENERATE PLAIN TEXT RESUME NOW:
"""


class ResumeAgent:
    """
    LangChain-based agent responsible for resume generation.
    Composes the prompt, calls the Groq LLM, and returns raw text output.
    """

    def __init__(self):
        self._llm = get_llm()
        self._prompt = PromptTemplate(
            input_variables=["user_data"],
            template=RESUME_SYSTEM_PROMPT,
        )
        self._chain = self._prompt | self._llm | StrOutputParser()

    def generate(self, user_data: str) -> str:
        """
        Accepts user data, runs resilient chain call with fallback.
        """
        from app.core.llm import resilient_call
        from app.core.config import settings
        
        try:
            # First attempt with primary model
            return resilient_call(self._chain, {"user_data": user_data}).strip()
        except Exception:
            # Hard fallback to 8B model if primary fails all retries
            from app.core.llm import get_llm
            fallback_llm = get_llm(model_name=settings.GROQ_FALLBACK_MODEL)
            fallback_chain = self._prompt | fallback_llm | StrOutputParser()
            return resilient_call(fallback_chain, {"user_data": user_data}).strip()
