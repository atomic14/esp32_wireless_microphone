import pyaudio
import socket
import threading
import wave
from PyInquirer import prompt
from time import sleep


# ask the user if they want to record or play
def main_menu():
    questions = [
        {
            "type": "list",
            "name": "mode",
            "message": "What do you want to do?",
            "choices": ["Record", "Play"],
        }
    ]
    answers = prompt(questions)
    return answers["mode"]


# select the output audio device using pyinquirer
def get_output_audio_device_idx(p: pyaudio.PyAudio):
    audio_device_list = []
    for i in range(p.get_device_count()):
        device = p.get_device_info_by_index(i)
        if device["maxOutputChannels"] > 0:
            audio_device_list.append({"name": device["name"], "checked": True})
    questions = [
        {
            "type": "list",
            "name": "audio_device",
            "message": "Select the audio device to use (I recommend you use a virtual audio device!)",
            "choices": audio_device_list,
        }
    ]
    answers = prompt(questions)
    # select the user's preffered audio device
    output_device_idx = [
        i
        for i in range(p.get_device_count())
        if answers["audio_device"] == p.get_device_info_by_index(i)["name"]
    ][0]
    return output_device_idx


# this will run in a thread reading audio from the tcp socket and buffering it
buffer = []
buffering = False
buffer_audio = True


def read_audio_from_socket():
    global buffering, buffer, buffer_audio
    # connect to the esp32 socket
    sock = socket.socket()
    sock.connect(("microphone.local", 9090))
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    while buffer_audio:
        data = sock.recv(4096)
        if data == b"":
            raise RuntimeError("Lost connection")
        buffer.append(data)
        if len(buffer) > 50 and buffering:
            print("Finished buffering")
            buffering = False


def main():
    global buffer, buffering, buffer_audio
    # initiaslise pyaudio
    p = pyaudio.PyAudio()
    mode = main_menu()
    # kick off the audio buffering thread
    thread = threading.Thread(target=read_audio_from_socket)
    thread.daemon = True
    thread.start()
    if mode == "Record":
        input("Recording to output.wav - hit any key to stop")
        buffer_audio = False
        # write the buffered audio to a wave file
        with wave.open("output.wav", "wb") as wave_file:
            wave_file.setnchannels(1)
            wave_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wave_file.setframerate(44100)
            wave_file.writeframes(b"".join(buffer))
    else:
        output_device_idx = get_output_audio_device_idx(p)
        # set up the audio stream
        stream = pyaudio.Stream(
            p,
            output=True,
            rate=44100,
            channels=1,
            format=pyaudio.paInt16,
            output_device_index=output_device_idx,
            frames_per_buffer=1024,
        )
        # this will write the buffered audio to the audio stream
        while True:
            if not buffering and len(buffer) > 0:
                data = buffer.pop(0)
                stream.write(data)
                if len(buffer) == 0:
                    print("Buffering...")
                    buffering = True
            else:
                sleep(0.001)


if __name__ == "__main__":
    main()
