import os
import sys
import termios  # Unix tabanlı sistemlerde çalışır.
import wave
import numpy as np
import sounddevice as sd
import warnings
from pynput import keyboard
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

def flush_stdin():
    """
    sys.stdin'de bekleyen (kalan) karakterleri temizler.
    Unix tabanlı sistemlerde termios.tcflush() kullanarak giriş tamponunu temizler.
    """
    try:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        pass

def record_audio(filename, fs=16000):
    clear_console()
    console.print(Panel("Ses Transkripsiyon Uygulamasına Hoşgeldiniz!", style="bold green"), justify="center")
    console.print("[bold blue]Kayda başlamak için 'Enter'a basın. Kayıt sırasında durdurmak için 'q' tuşuna basın.[/bold blue]\n")
    input()  # Kullanıcı Enter'a bastığında devam eder

    console.print("[bold yellow]Recording... (Press 'q' to stop)[/bold yellow]")
    audio_frames = []
    stop_flag = [False]  # Kayıt durdurulması için mutable bayrak

    def callback(indata, frames, time, status):
        if status:
            console.log(f"[red]{status}[/red]")
        audio_frames.append(indata.copy())

    def on_press(key):
        try:
            if key.char == 'q':
                console.print("[bold red]Recording stopped.[/bold red]")
                stop_flag[0] = True
                return False  # Dinleyiciyi durdur
        except AttributeError:
            pass

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    with sd.InputStream(samplerate=fs, channels=1, dtype='int16', callback=callback):
        while not stop_flag[0]:
            sd.sleep(100)

    listener.join()
    audio_data = np.concatenate(audio_frames, axis=0)

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit (2 byte)
        wf.setframerate(fs)
        wf.writeframes(audio_data.tobytes())
    console.print(f"[green]Audio saved to {filename} ({len(audio_data)} samples)[/green]")

def transcribe_audio(filename):
    console.print("[bold cyan]Transcribing audio...[/bold cyan]")
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo", device=0)
    transcription = pipe(filename, return_timestamps=True)
    return transcription

def main():
    while True:
        clear_console()
        console.print(Panel("Yeni Kayıt için Hazır", style="bold magenta"), justify="center")
        filename = "recorded_audio.wav"
        record_audio(filename)

        console.print("\n[bold blue]Lütfen kaydedilen dosyayı kontrol edin (örneğin, bir medya oynatıcı ile).[/bold blue]\n")
        transcription = transcribe_audio(filename)
        transcribed_text = transcription.get('text', '')
        console.print(Panel(f"[bold green]Transcription:[/bold green]\n{transcribed_text}", style="green"), justify="center")

        with open("transcription.txt", "a") as file:
            file.write(transcribed_text + "\n")
        console.print("[bold green]Transcription saved to transcription.txt[/bold green]\n")

        # Önceki kayıttan kalan karakterleri temizliyoruz.
        flush_stdin()

        # Kullanıcıya yeni kayıt yapıp yapmayacağını soruyoruz.
        try:
            response = Prompt.ask("Yeni bir kayıt yapmak ister misiniz? (y/n)", default="y")
        except Exception:
            response = ""
        # Girdiyi temizle ve varsayılan değeri kullan.
        choice = response.strip().lower() or "y"
        # Eğer ilk karakter "q" ise, onu temizliyoruz.
        if choice.startswith("q"):
            choice = choice[1:].strip() or "y"
        if choice != 'y':
            console.print("[bold yellow]Çıkılıyor...[/bold yellow]")
            break

if __name__ == "__main__":
    main()
