from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.cities import tier_1, tier_2



class UserInput(BaseModel):
    age: Annotated[int, Field(gt=0, lt=120)]
    weight: Annotated[float, Field(gt=0)]
    height: Annotated[float, Field(gt=0)]
    income_lpa: Annotated[float, Field(gt=0)]
    smoker: Annotated[Literal["Yes", "No"], Field()]
    city: Annotated[str, Field()]
    occupation: Annotated[
        Literal[
            "business_owner",
            "freelancer",
            "government_job",
            "private_job",
            "retired",
            "student",
            "unemployed"
        ],
        Field()
    ]

    #convert city into title case and validate
    @field_validator("city")
    def validate_city(cls, v:str) -> str:
        v= v.strip().title()
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        h_m = self.height / 100
        return round(self.weight / (h_m ** 2), 2)

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1:
            return 1
        elif self.city in tier_2:
            return 2
        else:
            return 3

    @computed_field
    @property
    def lifestyle_risk_score(self) -> int:
        score = 0
        if self.bmi < 18.5:
            score += 1
        elif self.bmi < 25:
            score += 2
        elif self.bmi < 30:
            score += 3
        else:
            score += 4

        if self.smoker == "Yes":
            score += 3
        else:
            score += 1

        return score

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.lifestyle_risk_score <= 3:
            return "low"
        elif self.lifestyle_risk_score <= 6:
            return "medium"
        else:
            return "high"


    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"
