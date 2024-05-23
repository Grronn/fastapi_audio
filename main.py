import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoProcessor, AutoModel
from fastapi import FastAPI, Body, Response, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, JSONResponse
import scipy.io.wavfile as wavfile
import io

app = FastAPI()

class TextRequest(BaseModel):
    text: str

def preprocess_text(text):
    WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))
    return WHITESPACE_HANDLER(text)

def generate_summary(text, model, tokenizer):
    input_ids = tokenizer(
        [text],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    )["input_ids"]

    output_ids = model.generate(
        input_ids=input_ids,
        max_length=84,
        no_repeat_ngram_size=2,
        num_beams=4
    )[0]

    return tokenizer.decode(
        output_ids,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )

def generate_speech(text, model, processor):
    inputs = processor(
        text=text,
        return_tensors="pt",
    )

    return model.generate(**inputs, do_sample=True)

def generate_audio_response(speech_values, summary, model):
    sampling_rate = model.generation_config.sample_rate

    buffer = io.BytesIO()
    wavfile.write(buffer, rate=sampling_rate, data=speech_values.cpu().numpy().squeeze())
    content = {"text": summary}

    response = StreamingResponse(io.BytesIO(buffer.getvalue()), media_type="audio/wav")
    response.headers["Content-Disposition"] = "attachment; filename=generated_audio.wav"
    response.body = content

    return response


@app.get("/health")
async def health_check():
    """
    Проверка состояния сервиса.
    Возвращает HTTP 200, если сервис функционирует нормально.
    """
    return Response(status_code=200)


@app.post("/text")
async def process_text(request: TextRequest):
    try:
        article_text = request.text
        model_name = "csebuetnlp/mT5_multilingual_XLSum"
        tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        summary = generate_summary(preprocess_text(article_text), model, tokenizer)

        processor = AutoProcessor.from_pretrained("suno/bark-small", use_fast=False)
        model = AutoModel.from_pretrained("suno/bark-small")

        speech_values = generate_speech(summary, model, processor)

        if speech_values is not None and len(speech_values) > 0:
            return generate_audio_response(speech_values, summary, model)
        else:
            return JSONResponse(content={"detail": "No audio generated."}, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/taras")
async def process_text(request: TextRequest):
    try:
        article_text = request.text
        model_name = "csebuetnlp/mT5_multilingual_XLSum"
        tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        summary = generate_summary(preprocess_text(article_text), model, tokenizer)

        processor = AutoProcessor.from_pretrained("suno/bark-small", use_fast=False)
        model = AutoModel.from_pretrained("suno/bark-small")

        speech_values = generate_speech(summary, model, processor)

        if speech_values is not None and len(speech_values) > 0:
            return generate_audio_response(speech_values, summary, model)
        else:
            return JSONResponse(content={"detail": "No audio generated."}, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/olegtext")
async def process_text(request: TextRequest):
    try:
        article_text = request.text
        model_name = "csebuetnlp/mT5_multilingual_XLSum"
        tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        summary = generate_summary(preprocess_text(article_text), model, tokenizer)

        processor = AutoProcessor.from_pretrained("suno/bark-small", use_fast=False)
        model = AutoModel.from_pretrained("suno/bark-small")

        speech_values = generate_speech(summary, model, processor)

        if speech_values is not None and len(speech_values) > 0:
            return generate_audio_response(speech_values, summary, model)
        else:
            return JSONResponse(content={"detail": "No audio generated."}, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))