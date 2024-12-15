import cv2
import numpy as np
import csv
import time
from sklearn import svm
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Konfigurasi Kamera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

# Membaca Database
FileDB = 'DatabaseWarna.txt'  # Pastikan file ini tersedia dan formatnya benar
Database = pd.read_csv(FileDB, sep=",", header=0)
print("Database:\n", Database)

# X = Data (B, G, R), y = Target
X = Database[['B', 'G', 'R']]
y = Database['Target']

# Normalisasi Data dan Pelatihan Model SVM
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Normalisasi data
clf = svm.SVC(kernel="linear")  # Gunakan kernel linear

clf.fit(X_scaled, y)

# Fungsi Prediksi Warna
def predict_color(B, G, R):
    color_scaled = scaler.transform([[B, G, R]])
    try:
        prediction = clf.predict(color_scaled)[0]  # Ambil hasil prediksi
        return prediction
    except Exception as e:
        return "Tidak Teridentifikasi"

# Loop Kamera untuk Prediksi
while True:
    ret, img = cap.read()
    if not ret:
        print("Gagal membaca frame dari kamera.")
        break

    img = cv2.flip(img, 1)  # Membalikkan kamera jika terbalik

    # Ambil warna rata-rata dari area tertentu
    region = img[220:260, 300:340]  # Area yang dianalisis
    colorB = int(np.mean(region[:, :, 0]))
    colorG = int(np.mean(region[:, :, 1]))
    colorR = int(np.mean(region[:, :, 2]))
    color = [colorB, colorG, colorR]

    # Prediksi warna
    prediction = predict_color(colorB, colorG, colorR)

    # Tampilkan hasil di jendela kamera
    cv2.putText(img, f"Prediksi: {prediction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.rectangle(img, (300, 220), (340, 260), (0, 255, 0), 2)  # Area analisis
    cv2.imshow("Color Tracking", img)

    # Tombol keluar (ESC)
    key = cv2.waitKey(30) & 0xff
    if key == 27:  # Tekan esc untuk keluar
        break

cap.release()
cv2.destroyAllWindows()
