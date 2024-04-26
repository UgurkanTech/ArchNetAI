import os
import sys
from typing import List
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from NetNode import *

model = NetModelFactory.createModel(NetModelType.INSTRUCTOR, model="phi3")

from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    email: str = Field(..., description="Email address")
    social: str


class Meeting(BaseModel):
    users: List[User]
    date: str = Field(..., description="dd/mm/yyyy")
    location: str = Field(..., description="Short address")
    budget: int
    deadline: str = Field(..., description="dd/mm/yyyy")


text_block = """
In a recent web meeting, we planned an upcoming tech conference. Participant details:

- Alice Smith, alices@email.com, social @TechGuruAlice
- Bob Johnson, bobj@email.com, social @InnovatorBob
- Charlie Williams, charliew@email.com, social @CharlieTheCoder

The conference is on May 10th, 2024, at 1234 Tech Street. Keynote speaker: Elon Musk. Budget: $80,000. 
Proposals due by April 1st. Next meeting: March 15th, 3 PM GMT.
"""

model.setJSONBaseModel(Meeting)

stream = model.getModelResponse(f"Get the information about the meeting and the users {text_block}")

model.printStream(stream)

#print(model.getResponseResult(stream=stream))
