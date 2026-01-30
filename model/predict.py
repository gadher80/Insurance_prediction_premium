import pickle
import pandas as pd

model_version = "1.0.0"

# Load model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

def predict_output(user_input:dict):
    input_df = pd.DataFrame(user_input)
    prediction = model.predict(input_df)[0]

    # model classes probabilities for confidence score (per-class)
    probabilities = model.predict_proba(input_df)[0]
    classes = getattr(model, "classes_", None)

    # Build a mapping from class label -> probability
    if classes is not None:
        class_confidences = {str(c): float(p) for c, p in zip(classes, probabilities)}
    else:
        # fallback: return list of probabilities if classes_ not available
        class_confidences = {str(i): float(p) for i, p in enumerate(probabilities)}

    confidence = float(max(probabilities))
    return {"prediction": str(prediction), "confidence": confidence, "class_confidences": class_confidences}



