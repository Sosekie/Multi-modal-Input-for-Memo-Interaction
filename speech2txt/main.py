from .record import *
from .totxt import *
import time
from datetime import datetime

def audio_trigger_merge(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 1)
    print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('text: ', text)
    if "m" in text.lower() or "g" in text.lower():
        result_queue.put(True)
        print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()

<<<<<<< Updated upstream
def audio_trigger_create(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 1)
    print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('text: ', text)
    if "c" in text.lower():
        result_queue.put(True)
        print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()
=======
    # model_id = "openai/whisper-large-v3"
    model_id = "openai/whisper-base"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, 
        low_cpu_mem_usage=True, 
        use_safetensors=True,
        # if GPU allowed
        # use_flash_attention_2=True
    )
    # if GPU not allowed
    # model = model.to_bettertransformer()

    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    return pipe

def speech2txt(pipe, sample):

    result = pipe(sample,
                # optional:
                generate_kwargs={
                    "language": "english",
                    #   "task": "translate"
                    },
                )
    print(result["text"])


if __name__ == "__main__":

    start_time = datetime.now()
    pipe = model_initialize()
    end_time = datetime.now()
    print(f"load time: {(end_time - start_time).total_seconds()} seconds")

    for i in range(5):
        start_time = datetime.now()
        speech2txt(pipe, sample = './speech2txt/Recording/Recording_1.mp3')
        end_time = datetime.now()
        print(f"excute time: {(end_time - start_time).total_seconds()} seconds")
>>>>>>> Stashed changes
