import cv2
import pandas as pd
import os
from ultralytics import YOLO
import time

#YOLO
MODEL_PATH = "models/yolov8n.pt" 
TARGET_CLASSES = {"cell phone", "radio", "smartphone"}

model = YOLO(MODEL_PATH)

#Analisar video(checar)
def analyze_video(video_url):
    inicio = time.time()
    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        return "Erro"

    found = False
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_count > 300:
            break

        results = model(frame)
        for r in results:
            for box in r.boxes:
                cls = model.names[int(box.cls[0])]
                if cls in TARGET_CLASSES:
                    found = True
                    break
            if found:
                break

        frame_count += 1

    cap.release()
    fim = time.time()
    print(f"Tempo de execução: {fim - inicio:.4f} segundos")
    return "Verdadeiro" if found else "Falso"

#Ler planilha
def process_videos(input_file, output_file):
    
    df = pd.read_excel(input_file)

    for index, row in df.iterrows():
        video_url = row["Links"]
        evidency = analyze_video(video_url)
        
        df.at[index, "Evidencia"] = evidency
        df.at[index, "Status"] = "Validado" if evidency in ["Verdadeiro", "Falso"] else "Erro"

    df.to_excel(output_file, index=False)
    print("Processo concluído! Resultados salvos em:", output_file)

if __name__ == "__main__":
    input_excel = "data/saida.xlsx"
    output_excel = "data/resultado.xlsx"
    
    os.makedirs("models", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    inicio = time.time()
    process_videos(input_excel, output_excel)
    fim = time.time()

