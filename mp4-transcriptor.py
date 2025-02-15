import os
import sys
import subprocess
import wave
import numpy as np
import warnings
from transformers import pipeline
from rich.prompt import Prompt
from rich.console import Console
from rich.panel import Panel

# Uyarıları bastır (FutureWarning, DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Rich için konsol nesnesi oluşturuyoruz
console = Console()


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def extract_audio_from_mp4(mp4_filename, wav_filename, fs=16000):
    """
    ffmpeg kullanarak MP4 dosyasından ses çıkartır ve WAV formatında kaydeder.
    """
    command = [
        "ffmpeg",
        "-i", mp4_filename,
        "-vn",  # Video içeriğini yok say
        "-acodec", "pcm_s16le",  # 16-bit PCM codec
        "-ar", str(fs),  # Örnekleme frekansı
        "-ac", "1",  # Mono kanal
        wav_filename,
        "-y"  # Var olan dosyayı üzerine yaz
    ]
    console.print(
        f"[bold blue]'{mp4_filename}' dosyasından ses çıkartılıyor ve '{wav_filename}' olarak kaydediliyor...[/bold blue]")
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        console.print(f"[bold red]Ses çıkartma sırasında hata oluştu:\n{result.stderr.decode()}[/bold red]")
        sys.exit(1)
    else:
        console.print(f"[bold green]Ses başarıyla çıkartıldı![/bold green]")


def transcribe_audio(filename):
    console.print("[bold cyan]Ses dosyası transkribe ediliyor...[/bold cyan]")
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo", device=0)
    transcription = pipe(filename, return_timestamps=True)
    return transcription


def main():
    clear_console()
    console.print(Panel("MP4 Dosyası için Transkripsiyon Uygulamasına Hoşgeldiniz!", style="bold green"),
                  justify="center")

    # Kullanıcıdan MP4 dosyasının yolunu alıyoruz.
    mp4_filename = Prompt.ask("Lütfen transkripsiyon yapmak için MP4 dosyasının yolunu girin", default="input.mp4")

    if not os.path.exists(mp4_filename):
        console.print(f"[bold red]{mp4_filename} bulunamadı![/bold red]")
        sys.exit(1)

    # MP4 dosyasından ses çıkartıp WAV dosyası olarak kaydediyoruz.
    wav_filename = "extracted_audio.wav"
    extract_audio_from_mp4(mp4_filename, wav_filename)

    # Ses dosyasını transkribe ediyoruz.
    transcription = transcribe_audio(wav_filename)
    transcribed_text = transcription.get('text', '')

    console.print(Panel(f"[bold green]Transkripsiyon:[/bold green]\n{transcribed_text}", style="green"),
                  justify="center")

    # Transkripsiyon sonucunu "mp4_trsancription.txt" dosyasına kaydediyoruz.
    with open("mp4_trsancription.txt", "a", encoding="utf-8") as file:
        file.write(transcribed_text + "\n")
    console.print("[bold green]Transkripsiyon mp4_trsancription.txt dosyasına kaydedildi.[/bold green]\n")


if __name__ == "__main__":
    main()
