import pydicom
from pydicom.dataset import FileDataset
from PIL import Image
import numpy as np
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os

# Lista de arquivos selecionados
image_paths = []

# Inicializa a janela principal primeiro
root = tk.Tk()
root.title("Conversor PNG/JPG para DICOM")
root.geometry("700x680")
root.resizable(False, False)

# Variáveis Tkinter
image_path = tk.StringVar()
save_path = tk.StringVar()
patient_name = tk.StringVar()
color_mode = tk.StringVar(value="Preto e Branco")

# Função para converter imagem para DICOM
def convert_to_dicom(input_image_path, output_dicom_path, patient_name, mode):
    img = Image.open(input_image_path)

    if mode == 'Preto e Branco':
        img = img.convert('L')
        np_image = np.array(img)
        samples_per_pixel = 1
        photometric = "MONOCHROME2"
    else:
        img = img.convert('RGB')
        np_image = np.array(img)
        samples_per_pixel = 3
        photometric = "RGB"

    file_meta = pydicom.Dataset()
    file_meta.MediaStorageSOPClassUID = pydicom.uid.SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.ImplementationClassUID = pydicom.uid.PYDICOM_IMPLEMENTATION_UID
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    ds = FileDataset(output_dicom_path, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.PatientName = patient_name or "Anon"
    ds.PatientID = "123456"
    ds.Modality = "OT"
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    ds.SOPClassUID = file_meta.MediaStorageSOPClassUID

    dt = datetime.datetime.now()
    ds.StudyDate = dt.strftime('%Y%m%d')
    ds.StudyTime = dt.strftime('%H%M%S')

    ds.SamplesPerPixel = samples_per_pixel
    ds.PhotometricInterpretation = photometric
    ds.Rows, ds.Columns = np_image.shape[:2]
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0

    if samples_per_pixel == 3:
        ds.PlanarConfiguration = 0

    ds.PixelData = np_image.tobytes()
    ds.save_as(output_dicom_path)

# Visualiza imagem PNG/JPG
def visualizar_imagem_original(canvas_frame, imagem_path):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    try:
        img = Image.open(imagem_path)
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(img)
        ax.axis('off')
        ax.set_title("Imagem Original")

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exibir imagem: {e}")

# Visualiza DICOM
def visualizar_dicom_integrado(canvas_frame, dicom_path):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    try:
        ds = pydicom.dcmread(dicom_path)
        pixel_data = ds.pixel_array

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.imshow(pixel_data, cmap='gray' if ds.SamplesPerPixel == 1 else None)
        ax.axis('off')
        ax.set_title("DICOM Convertido")

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exibir DICOM: {e}")

# Seleciona imagens
def browse_image():
    files = filedialog.askopenfilenames(filetypes=[("Imagens", "*.jpg *.jpeg *.png")])
    if files:
        image_paths.clear()
        image_paths.extend(files)
        nomes = "; ".join(os.path.basename(f) for f in files)
        image_path.set(nomes)
        visualizar_imagem_original(original_frame, image_paths[0])

# Converte para DICOM
def convert():
    if not image_paths:
        messagebox.showerror("Erro", "Selecione uma ou mais imagens.")
        return

    patient = patient_name.get()
    mode = color_mode.get()
    output_dir = filedialog.askdirectory(title="Escolha a pasta de saída")

    if not output_dir:
        return

    try:
        last_output = ""
        for file in image_paths:
            base = os.path.splitext(os.path.basename(file))[0]
            output_path = os.path.join(output_dir, f"{base}_convertido.dcm")
            convert_to_dicom(file, output_path, patient, mode)
            last_output = output_path

        messagebox.showinfo("Sucesso", f"{len(image_paths)} imagens convertidas com sucesso.")
        if last_output:
            visualizar_dicom_integrado(preview_frame, last_output)

    except Exception as e:
        messagebox.showerror("Erro na conversão", str(e))

# Interface
style = ttk.Style(root)
style.theme_use("clam")

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

ttk.Label(main_frame, text="Imagens PNG/JPG selecionadas:").pack(anchor="w")
ttk.Entry(main_frame, textvariable=image_path, width=85).pack()
ttk.Button(main_frame, text="Selecionar Imagens", command=browse_image).pack(pady=5)

ttk.Label(main_frame, text="Nome do Paciente:").pack(anchor="w", pady=(10, 0))
ttk.Entry(main_frame, textvariable=patient_name, width=30).pack()

ttk.Label(main_frame, text="Modo de Cor:").pack(anchor="w", pady=(10, 0))
ttk.Combobox(main_frame, textvariable=color_mode, values=["Preto e Branco", "Colorido"], state="readonly").pack()

ttk.Button(main_frame, text="Converter para DICOM", command=convert).pack(pady=15)

# Visualização lado a lado
preview_container = ttk.Frame(main_frame)
preview_container.pack(fill="both", expand=True)

ttk.Label(preview_container, text="Imagem Original:").grid(row=0, column=0, sticky="w")
ttk.Label(preview_container, text="DICOM Convertido:").grid(row=0, column=1, sticky="w")

original_frame = ttk.Frame(preview_container, width=300, height=300, relief="sunken")
original_frame.grid(row=1, column=0, padx=5, pady=5)

preview_frame = ttk.Frame(preview_container, width=300, height=300, relief="sunken")
preview_frame.grid(row=1, column=1, padx=5, pady=5)

root.mainloop()
