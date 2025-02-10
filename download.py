from ultralytics import YOLO

# Definir o caminho para salvar o modelo
model_path = "models/yolov8n.pt"

# Carregar e salvar o modelo
model = YOLO("yolov8n.pt")
model.export(format="torchscript")  # Apenas para garantir compatibilidade

# Mover para a pasta correta, caso tenha sido salvo no cache
import shutil
import os

cached_model_path = os.path.expanduser("~/.cache/ultralytics/yolov8n.pt")
if os.path.exists(cached_model_path):
    shutil.move(cached_model_path, model_path)

print(f"Modelo baixado e salvo em: {model_path}")
