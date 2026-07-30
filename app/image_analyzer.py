from io import BytesIO

import torch
from PIL import Image
from transformers import (
    CLIPImageProcessor,
    CLIPModel,
    CLIPTokenizer,
)


MODEL_NAME = "openai/clip-vit-base-patch32"

tokenizer = CLIPTokenizer.from_pretrained(MODEL_NAME)
image_processor = CLIPImageProcessor.from_pretrained(MODEL_NAME)
model = CLIPModel.from_pretrained(MODEL_NAME)

model.eval()


VIBES = {
    "summer": "a happy summer photo with sunshine and warm colors",
    "romantic": "a soft romantic photo with love and tenderness",
    "night": "a cinematic photo taken in a city at night",
    "mysterious": "a dark mysterious atmospheric photo",
    "cozy": "a cozy warm peaceful photo",
    "party": "an energetic party photo with celebration",
    "dreamy": "a dreamy ethereal aesthetic photo",
    "confident": "a stylish confident powerful photo",
    "sad": "a melancholic emotional sad photo",
    "luxury": "an elegant luxurious expensive looking photo",
}


def analyze_image(image_bytes: bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    vibe_names = list(VIBES.keys())
    vibe_descriptions = list(VIBES.values())

    text_inputs = tokenizer(
        vibe_descriptions,
        padding=True,
        truncation=True,
        max_length=77,
        return_tensors="pt",
    )

    image_inputs = image_processor(
        images=[image],
        return_tensors="pt",
    )

    with torch.no_grad():
        outputs = model(
            input_ids=text_inputs["input_ids"],
            attention_mask=text_inputs["attention_mask"],
            pixel_values=image_inputs["pixel_values"],
        )

    probabilities = torch.softmax(
        outputs.logits_per_image,
        dim=1,
    )[0]

    results = []

    for vibe_name, probability in zip(vibe_names, probabilities):
        results.append(
            {
                "vibe": vibe_name,
                "score": round(probability.item() * 100, 2),
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:3]