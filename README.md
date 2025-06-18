# 🩻 Conversor de Imagens PNG/JPG para DICOM

Uma aplicação Python com interface gráfica que converte imagens comuns (JPG/PNG) em arquivos médicos no formato **DICOM** — padrão utilizado em hospitais, clínicas e sistemas PACS.

---

## 💡 Funcionalidades

✅ Conversão de uma ou **múltiplas imagens** JPG/PNG para DICOM  
✅ Suporte a imagens em **preto e branco** ou **coloridas**  
✅ Interface gráfica amigável usando **Tkinter**  
✅ Visualização integrada da imagem original e do DICOM convertido  
✅ Campo para inserção do **nome do paciente**  
✅ Geração de arquivos compatíveis com sistemas PACS  
✅ Criação de **.EXE** para uso offline em Windows  
✅ Compatível com Windows 10 ou superior

---

## 📷 Demonstração

| Imagem Original  | DICOM Convertido |
|------------------|------------------|
| ![original](https://i.imgur.com/Obf67Wb.png) | ![dicom](https://i.imgur.com/PNB2d3T.png) |

---

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [pydicom](https://pydicom.github.io/)
- [Pillow (PIL)](https://pillow.readthedocs.io/)
- [NumPy](https://numpy.org/)
- [Tkinter (GUI)](https://wiki.python.org/moin/TkInter)
- [Matplotlib](https://matplotlib.org/)
- [PyInstaller](https://pyinstaller.org/) – para gerar o `.exe`
- [Inno Setup](https://jrsoftware.org/isinfo.php) – para criar o instalador `.exe`

---

## 🖥️ Como Executar Localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/conversor-dicom.git
cd conversor-dicom
