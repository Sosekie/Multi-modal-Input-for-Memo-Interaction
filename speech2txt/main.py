import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
from datetime import datetime

def model_initialize():
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

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

    pipe = model_initialize()

    for i in range(5):
        start_time = datetime.now()
        speech2txt(pipe, sample = './speech2txt/Recording/Recording_1.mp3')
        end_time = datetime.now()
        print(f"excute time：{(end_time - start_time).total_seconds()} seconds")