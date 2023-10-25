import pygame as pe
from pydub import AudioSegment
from pydub.playback import play
import os


sound_file_path = "./sound/start.wav" # 再生する音声ファイルのパス

# 速度調節がされていなかった場合にする
adjusted_sound_file_path = "./sound/start_up.wav"
if not os.path.exists(adjusted_sound_file_path):
    # -------- pydubによる再生速度調節 --------
    audio = AudioSegment.from_file(sound_file_path)
    speed_adjustment = 1.3
    ajusted_audio = audio.speedup(playback_speed=speed_adjustment)
    ajusted_audio.export(adjusted_sound_file_path, format="wav")
sound_file_path = adjusted_sound_file_path

# -------- pygameによるサウンド再生 --------
pe.init() # pygameを初期化
sound_object = pe.mixer.Sound(sound_file_path) # サウンドオブジェクトを作成
# playback_speed = 1.2 # 再生速度の倍率（1.0がデフォルト）
# sound_object.set_playback_speed(playback_speed)
sound_object.play() # サウンドを再生
pe.time.wait(int(sound_object.get_length() * 1000)) # 音声再生終了まで待つ
pe.quit() # pygameを終了