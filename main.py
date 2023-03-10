import os
from commu.preprocessor.utils import constants
from commu.midi_generator.generate_pipeline import MidiGenerationPipeline
from typing import Dict, List
import argparse
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
import uuid
from key import secrete_key
from pydantic import BaseModel
from fastapi import FastAPI, Header, HTTPException
import shutil

app = FastAPI()
api_key_header = APIKeyHeader(name="Token")

"""
table name : metagenerator
key : unique 한 key
song : 노래 경로
mood : list 형태로 저장
"""


try:

    import mido

except ImportError as error:

    raise ImportError(

        """



`pip install mido`를 수행해서 패키지를 설치하세요.

Package Github: https://github.com/mido/mido

Package Document: https://mido.readthedocs.io/en/latest/

"""

    ) from error


def merge_midi(files: "List[str]") -> mido.MidiFile:

    # 모든 미디 파일 읽기

    midis = [mido.MidiFile(path) for path in files]

    if not midis:

        raise ValueError("파일 목록이 비었습니다.")

    # 빈 미디 파일 생성

    mergedMidi = mido.MidiFile()

    mergedMidi.ticks_per_beat = midis[0].ticks_per_beat

    mergedMidi.tracks = sum((midi.tracks for midi in midis), start=[])

    return mergedMidi


def save_midi(path: str, midi: "mido.MidiFile", exist_ok=False) -> None:

    if (not exist_ok) and os.path.exists(path):

        raise FileExistsError(

            f"{path} 은 이미 존재하는 파일입니다. 파일명을 변경하거나, exist_ok 옵션을 True로 설정해 덮어쓰세요."

        )

    midi.save(path)


def main(model_arg: Dict, input_arg: Dict):
    pipeline = MidiGenerationPipeline(model_arg)

    inference_cfg = pipeline.model_initialize_task.inference_cfg
    model = pipeline.model_initialize_task.execute()

    encoded_meta = pipeline.preprocess_task.execute(input_arg)
    input_data = pipeline.preprocess_task.input_data

    pipeline.inference_task(
        model=model,
        input_data=input_data,
        inference_cfg=inference_cfg
    )
    sequences = pipeline.inference_task.execute(encoded_meta)

    pipeline.postprocess_task(input_data=input_data)
    pipeline.postprocess_task.execute(
        sequences=sequences
    )


class Item(BaseModel):
    control: str


class responseItem(BaseModel):
    out_list: List[str]


@app.post("/auto_music", response_model=responseItem)
async def auto_music(item: Item, token: str = Depends(api_key_header)):
    # control must be : 00000000 (1/0, length : 8)
    print(item.control)
    uid = str(uuid.uuid4())

    NUM_GEN = 2
    main({'checkpoint_dir': '/home/dani/workspace/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': 70, 'audio_key': 'aminor', 'time_signature': '4/4', 'pitch_range': 'mid_high', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'main_melody', 'rhythm': 'standard',
                                                                         'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    main({'checkpoint_dir': '/home/dani/workspace/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': 70, 'audio_key': 'bminor', 'time_signature': '4/4', 'pitch_range': 'mid_low', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'main_melody', 'rhythm': 'standard',
                                                                         'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    main({'checkpoint_dir': '/home/dani/workspace/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': 70, 'audio_key': 'aminor', 'time_signature': '4/4', 'pitch_range': 'mid_high', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'pad', 'rhythm': 'standard',
                                                                         'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    main({'checkpoint_dir': '/home/dani/workspace/checkpoint_best.pt'}, {'output_dir': uid, 'bpm': 70, 'audio_key': 'aminor', 'time_signature': '4/4', 'pitch_range': 'mid_high', 'num_measures': 8.0, 'inst': 'acoustic_piano', 'genre': 'newage', 'track_role': 'riff', 'rhythm': 'standard',
                                                                         'min_velocity': 60, 'max_velocity': 80, 'chord_progression': 'Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E-Am-Am-Am-Am-Am-Am-Am-Am-G-G-G-G-G-G-G-G-F-F-F-F-F-F-F-F-E-E-E-E-E-E-E-E', 'num_generate': NUM_GEN, 'top_k': 32, 'temperature': 0.95})
    midi_path_list = []
    out_midi_list = []

    uid_directory = os.listdir(uid)

    for sub_d in uid_directory:
        sub_d = uid + "/" + sub_d
        sublist = []

        for sub_f in os.listdir(sub_d):
            sublist.append(sub_d + "/" + sub_f)
        midi_path_list.append(sublist)

    for midx in range(NUM_GEN):
        output_list = []
        out_file_name = "generated/"+"{}_{}.mid".format(uid, midx)

        for m in midi_path_list:
            output_list.append(m[midx])
        save_midi(
            out_file_name,
            merge_midi(output_list),
            exist_ok=True,
        )
        out_midi_list.append(out_file_name)

    if os.path.exists(uid):
        shutil.rmtree(uid)

    if token != secrete_key["SECRETE-KEY"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return {"out_list": out_midi_list}
