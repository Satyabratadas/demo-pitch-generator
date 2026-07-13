from pydantic import BaseModel, Field
from typing import List

class PitchSegment(BaseModel):
    """Represents a specific part of the demo timeline."""
    time_marker: str = Field(description="The timestamp range, e.g., '0:00 - 0:20'")
    action: str = Field(description="What the presenter should be doing on screen at this moment")
    talking_points: str = Field(description="What the presenter should actually say")

class DemoPitch(BaseModel):
    """The complete structure of the generated hackathon demo pitch."""
    project_name: str = Field(description="The name of the project extracted from the repository")
    hook: str = Field(description="A catchy 1-2 sentence opening that immediately grabs the judges' attention")
    problem_statement: str = Field(description="A clear, relatable explanation of the problem this project solves")
    tech_stack_highlight: str = Field(description="A brief summary of the technical choices and why they matter")
    
    # A step-by-step chronological timeline for the 2-minute pitch
    timeline: List[PitchSegment] = Field(description="Chronological breakdown of the 2-minute script")
    
    wow_moment: str = Field(description="The single most impressive feature or technical feat to highlight as the climax")
    demo_warnings: List[str] = Field(description="Common hackathon pitfalls to avoid specific to this project type")