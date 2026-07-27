import os, glob, json, soundfile as sf

base_path = "dev-clean/LibriSpeech/dev-clean"
usable_data = []
transcript_files = glob.glob(os.path.join(base_path, "**/*.txt"), recursive=True)
transcript_map = {}
for tfile in transcript_files:
    with open(tfile, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(" ", 1)
            if len(parts) == 2:
                audio_id, text = parts
                transcript_map[audio_id + ".flac"] = text


flac_files = glob.glob(os.path.join(base_path, "**/*.flac"), recursive=True)
for i, file_path in enumerate(flac_files):
    try:
        waveform, sr = sf.read(file_path)
        duration = len(waveform) / sr
        file_name = os.path.basename(file_path)
        transcript = transcript_map.get(file_name, None)

        usable_data.append({
            "id": f"sample_{i}",
            "file": file_name,
            "original_path": file_path,
            "audio_duration": round(duration, 2),
            "begin_time": 0.0,
            "end_time": round(duration, 2),
            "transcript": transcript,
            "speaker_id": file_path.split(os.sep)[-3],
            "chapter_id": file_path.split(os.sep)[-2],
            "audio_path": file_path,
            "sampling_rate": sr
        })
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


with open("librispeech_devclean_full.json", "w", encoding="utf-8") as f:
    json.dump(usable_data, f, ensure_ascii=False, indent=2)
    
with open("librispeech_devclean_full.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total samples loaded: {len(data)}")
print("Keys in first sample:", data[0].keys())
print("Transcript of first sample:", data[0]["transcript"])
