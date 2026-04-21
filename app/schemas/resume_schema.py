from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class ProfileLink(BaseModel):
    platform: str = Field(..., examples=["LinkedIn", "GitHub", "Portfolio", "LeetCode"])
    link: str = Field(..., examples=["https://linkedin.com/in/yourname"])


class ProjectItem(BaseModel):
    role: str = Field(..., examples=["Developer", "ML Engineer", "Full Stack Developer"])
    name: str = Field(..., examples=["AI Chatbot"])
    description: str = Field(..., examples=["Built a chatbot using LangChain and OpenAI API"])
    tech_stack: str = Field(..., examples=["Python, LangChain, FastAPI, React"])
    impact: Optional[str] = Field(default=None, examples=["Reduced support tickets by 40%"])


class EducationItem(BaseModel):
    degree: str = Field(..., examples=["B.Tech Computer Science"])
    institution: str = Field(..., examples=["IIT Bombay"])
    year: str = Field(..., examples=["2025"])
    score: Optional[str] = Field(default=None, examples=["8.7 CGPA"])


class TechnicalSkills(BaseModel):
    languages: Optional[str] = Field(default=None, examples=["Python, JavaScript, Java, C++"])
    web_dev: Optional[str] = Field(default=None, examples=["React, Node.js, FastAPI, HTML, CSS"])
    ml_ai: Optional[str] = Field(default=None, examples=["TensorFlow, PyTorch, Scikit-learn, LangChain"])
    libraries: Optional[str] = Field(default=None, examples=["Pandas, NumPy, Matplotlib, Requests"])
    tools_dbs: Optional[str] = Field(default=None, examples=["Git, Docker, MongoDB, PostgreSQL, Redis"])


class ResumeInput(BaseModel):
    name: str = Field(..., min_length=2, examples=["Priya Sharma"])
    phone: str = Field(..., examples=["+91 9876543210"])
    email: EmailStr = Field(..., examples=["priya@email.com"])
    location: str = Field(..., examples=["Mumbai, Maharashtra"])
    profiles: list[ProfileLink] = Field(default_factory=list)
    summary: Optional[str] = Field(
        default=None,
        description="Optional brief summary; AI will generate one if not provided",
    )
    skills: TechnicalSkills = Field(...)
    projects: list[ProjectItem] = Field(..., min_length=1)
    education: list[EducationItem] = Field(..., min_length=1)
    certifications: list[str] = Field(
        default_factory=list,
        examples=[["AWS Cloud Practitioner 2024", "ML Internship at TechCorp – built data pipeline"]],
    )


class ResumeOutput(BaseModel):
    resume: str = Field(..., description="Fully formatted ATS-friendly resume in plain text")
