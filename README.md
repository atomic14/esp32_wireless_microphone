# Intro

You can watch a video of this working here: https://youtu.be/0jR-QNTfydA at around 4:23

[![Demo Video](https://img.youtube.com/vi/0jR-QNTfydA/0.jpg)](https://www.youtube.com/watch?v=0jR-QNTfydA)

The `firmware` folder contains the ESP32 code that will stream audio over websockets or TCP sockets.

The `player` folder contains a simple Python program that will receive audio from the ESP32 and either play it or record it to a WAV file.
