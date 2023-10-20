import pygame as pe
from pydub import AudioSegment
from pydub.playback import play

sound_file_path = "./sound/start.wav" # 再生する音声ファイルのパス
if not "./wav_test_1.2.py"
# -------- pydubによる再生速度調節 --------
audio = AudioSegment.from_file(sound_file_path)
speed_adjustment = 1.3
ajusted_audio = audio.speedup(playback_speed=speed_adjustment)

# -------- pygameによるサウンド再生 --------
pe.init() # pygameを初期化
sound_object = pe.mixer.Sound(sound_file_path) # サウンドオブジェクトを作成
# playback_speed = 1.2 # 再生速度の倍率（1.0がデフォルト）
# sound_object.set_playback_speed(playback_speed)
sound_object.play() # サウンドを再生
pe.time.wait(int(sound_object.get_length() * 1000)) # 音声再生終了まで待つ
pe.quit() # pygameを終了