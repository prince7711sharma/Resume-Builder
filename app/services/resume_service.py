from app.schemas.resume_schema import ResumeInput, ResumeOutput
from app.agents.resume_agent import ResumeAgent
from app.utils.formatter import serialize_input, clean_output


class ResumeService:
    """
    Service layer that orchestrates the resume generation pipeline:
      1. Serialize validated input into a structured prompt string.
      2. Delegate to the ResumeAgent for LLM-based generation.
      3. Clean and normalize the raw LLM output.
      4. Return a validated ResumeOutput model.
    """

    def __init__(self):
        self._agent = ResumeAgent()

    def generate_resume(self, data: ResumeInput) -> ResumeOutput:
        # Step 1 — Convert Pydantic model → structured plain-text prompt block
        user_data_str: str = serialize_input(data)

        # Step 2 — Run LangChain agent (Groq LLM call)
        raw_resume: str = self._agent.generate(user_data_str)

        # Step 3 — Post-process and clean the output
        final_resume: str = clean_output(raw_resume)

        # Step 4 — Return validated output model
        return ResumeOutput(resume=final_resume)
