import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoProcessor, AutoModel
from fastapi import FastAPI, Body, Response
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse, JSONResponse
import scipy.io.wavfile as wavfile
import io


app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

class TextRequest(BaseModel):
    text: str

@app.post("/text")
async def process_text(request: TextRequest):
    try:
        # Получаем текст из запроса
        article_text = request.text
        
        # Обрабатываем текст
        WHITESPACE_HANDLER = lambda k: re.sub('\s+', ' ', re.sub('\n+', ' ', k.strip()))

        model_name = "csebuetnlp/mT5_multilingual_XLSum"
        tokenizer = AutoTokenizer.from_pretrained(model_name, legacy=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        input_ids = tokenizer(
            [WHITESPACE_HANDLER(article_text)],
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

        summary = tokenizer.decode(
            output_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )


        processor = AutoProcessor.from_pretrained("suno/bark-small", use_fast=False)
        model = AutoModel.from_pretrained("suno/bark-small")

        inputs = processor(
            text=summary,
            return_tensors="pt",
        )

        speech_values = model.generate(**inputs, do_sample=True)
        
        if speech_values is not None and len(speech_values) > 0:
            
            sampling_rate = model.generation_config.sample_rate

            buffer = io.BytesIO()
            wavfile.write(buffer, rate=sampling_rate, data=speech_values.cpu().numpy().squeeze())
            content = {"text": summary}


            response = StreamingResponse(io.BytesIO(buffer.getvalue()), media_type="audio/wav")

            response.headers["Content-Disposition"] = "attachment; filename=generated_audio.wav"

            response.body = content

            return response
        else:
            return JSONResponse(content={"detail": "No audio generated."}, status_code=400)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
