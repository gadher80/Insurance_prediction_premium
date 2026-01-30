from pydantic import BaseModel, Field, computed_field, field_validator

class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="The predicted class label")
    confidence: float = Field(ge=0, le=1)
    class_probabilities: dict[str, float] = Field(..., description="Probabilities for each class label")

    
    

