from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.llm import get_llm


RESUME_SYSTEM_PROMPT = """Senior Professional Resume Architect AI.
Task: Generate a premium, classically structured resume in MARKDOWN that follows a SPECIFIC layout.

STRICT LAYOUT RULES:
1. HEADER (Centered style): 
   # FULL NAME (ALL CAPS)
   (phone) | email | location
   LinkedIn: link | GitHub: link | Portfolio: link

2. SECTION HEADERS: Use `## SECTION NAME` in ALL CAPS.

3. PROFESSIONAL SUMMARY: 1-2 paragraph block.

4. EXPERTISE SECTION: 
   Use a single line (or two) of skills separated by pipes `|`. 
   Format: Skill 1 | Skill 2 | Skill 3

5. TECHNICAL SKILLS SECTION:
   - Use the following labels exactly: Languages:, Web Dev:, ML & AI:, Libraries:, Tools & DBs:
   - Format: **Label:** Valve 1, Value 2...

6. FEATURED PROJECTS:
   - Header style: `### ROLE | PROJECT NAME`
   - Use 2-3 impact-driven bullets per project.

7. EDUCATION & CERTS: Standard professional blocks.

8. DIVIDERS: Ensure sections are separated logically.

USER DATA:
{user_data}

GENERATE STYLISH MARKDOWN RESUME NOW:
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
