import time
import logging
import threading
import schedule  
import gps     
import json     
import requests 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
KONFIGURASI_UMUM = {
    'id_rangkaian': 'ID-Rangkaian-Saat-Ini'
}

KONFIGURASI_JADWAL = {
    'sumber': 'lokal',
    'lokasi_file': 'jadwal.json',
    'url_api': 'alamat_api_jadwal'
}

KONFIGURASI_LOKASI = {
    'sumber': 'gps',
    'url_api': 'alamat_api_lokasi'
}

KONFIGURASI_COUPLER = {
    'status': 'terputus',
    'id_rangkaian_terhubung': None
}

KONFIGURASI_ELEKTRIFIKASI = {
    'status': 'mati',
    'tegangan': None,
    'arus': None
}

KONFIGURASI_TIMS = {
    'alamat_ip': 'alamat_ip_tims',
    'port': 12345
}
PERUBAHAN_LOKASI = {
    'ip_perubahan': 'alamat_ip_perubahan',
    'port':67890
}

def dapatkan_jadwal():

    try:
        if KONFIGURASI_JADWAL['sumber'] == 'lokal':
            with open(KONFIGURASI_JADWAL['lokasi_file'], 'r') as f:
                jadwal = json.load(f)
                return jadwal
        elif KONFIGURASI_JADWAL['sumber'] == 'server':
            response = requests.get(KONFIGURASI_JADWAL['api']) #isi kata api dengan api yang sudah ditentukan oleh DJKA
            response.raise_for_status()
            return response.json()
        else:
            logging.error("resource not available")
            return None
    except Exception as e:
        logging.error(f"failed to get Schedule: {e}")
        return None

def dapatkan_lokasi():
    try:
        if KONFIGURASI_LOKASI['sumber'] == 'gps':
            logging.warning("GPS reading not started.")
            return None
        elif KONFIGURASI_LOKASI['sumber'] == 'server':
            response = requests.get(KONFIGURASI_LOKASI['url_api'])
            response.raise_for_status()
            return response.json()
        else:   
            logging.error("location resource not available")
            return None
    except Exception as e:
        logging.error(f"Gagal mendapatkan lokasi: {e}")
        return None
    
def perubahan_lokasi():
    try:
        if PERUBAHAN_LOKASI['perubahan'] == 'server':
            response = requests.get(PERUBAHAN_LOKASI['url_api_perubahan'])
            response.raise_for_status()
            return response.json()
        elif PERUBAHAN_LOKASI['sumber'] == 'informasi_perubahan':
            response = requests.get(PERUBAHAN_LOKASI['url_api_perubahan'])
            response.raise_for_status()
            return response.json()
        else:
            logging.error("failed to change location")
            return None
    except Exception as e:
        logging.error(f"Failed to Changes location: {e}")
        return None
        
def hitung_jarak(lokasi1, lokasi2):
    if lokasi1 and lokasi2 and 'latitude' in lokasi1 and 'longitude' in lokasi1 and 'latitude' in lokasi2 and 'longitude' in lokasi2:
        from math import radians, cos, sin, asin, sqrt
        lon1 = radians(lokasi1['longitude'])
        lat1 = radians(lokasi1['latitude'])
        lon2 = radians(lokasi2['longitude'])
        lat2 = radians(lokasi2['latitude'])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 6371
        return c * r
    return float('inf')

def inisiasi_penyambungan_terjadwal(id_rangkaian_target, lokasi_target):
    logging.info(f"Initialization: {id_rangkaian_target} at: {lokasi_target}")
    KONFIGURASI_COUPLER['status'] = 'Coupling_processing'
    KONFIGURASI_COUPLER['id_rangkaian_terhubung'] = id_rangkaian_target

def deteksi_kedekatan(lokasi_saat_ini, lokasi_target, threshold_jarak=1.0):
    if lokasi_saat_ini and lokasi_target:
        jarak = hitung_jarak(lokasi_saat_ini, lokasi_target)
        logging.info(f"target for coupling lenght: {jarak:.2f} km")
        return jarak <= threshold_jarak
    return False

def verifikasi_penyambungan_lokal():
    time.sleep(3)
    status_hardware = 'Succesfully Connected!'
    if status_hardware == 'Succesfully Connected!':
        KONFIGURASI_COUPLER['status'] = 'Succesfully Connected!'
        logging.info(f"Penyambungan fisik dengan rangkaian ID {KONFIGURASI_COUPLER['id_rangkaian_terhubung']} berhasil.")
        return True
    else:
        KONFIGURASI_COUPLER['status'] = 'gagal Succesfully Connected!'
        KONFIGURASI_COUPLER['id_rangkaian_terhubung'] = None
        logging.warning("Penyambungan Coupler gagal.")
        return False

def aktifkan_elektrifikasi_lokal():
    logging.info("Mengaktifkan elektrifikasi rangkaian yang Succesfully Connected! secara lokal.")
    KONFIGURASI_ELEKTRIFIKASI['status'] = 'proses_menghidupkan'
    time.sleep(2)
    KONFIGURASI_ELEKTRIFIKASI['status'] = 'hidup'
    KONFIGURASI_ELEKTRIFIKASI['tegangan'] = 'Tegangan Terukur'
    KONFIGURASI_ELEKTRIFIKASI['arus'] = 'Arus Terukur'
    logging.info("Elektrifikasi rangkaian lokal aktif.")

def nonaktifkan_elektrifikasi_lokal():
    logging.info("Menonaktifkan elektrifikasi rangkaian lokal.")
    KONFIGURASI_ELEKTRIFIKASI['status'] = 'proses_mematikan'
    KONFIGURASI_ELEKTRIFIKASI['tegangan'] = None
    KONFIGURASI_ELEKTRIFIKASI['arus'] = None
    time.sleep(2)
    KONFIGURASI_ELEKTRIFIKASI['status'] = 'mati'
    logging.info("Elektrifikasi rangkaian lokal nonaktif.")

def proses_penjadwalan():
    jadwal = dapatkan_jadwal()
    lokasi_saat_ini = dapatkan_lokasi()
    if jadwal and lokasi_saat_ini:
        for item in jadwal:
            if item['rangkaian_target'] != KONFIGURASI_UMUM['id_rangkaian'] and 'lokasi_bertemu' in item and 'waktu_bertemu' in item:
                lokasi_target = item['lokasi_bertemu']
                waktu_bertemu_str = item['waktu_bertemu']
                from datetime import datetime
                try:
                    waktu_bertemu = datetime.strptime(waktu_bertemu_str, '%Y-%m-%d %H:%M:%S')
                    waktu_sekarang = datetime.now()
                    selisih_waktu = (waktu_bertemu - waktu_sekarang).total_seconds()
                    if 0 < selisih_waktu <= 300:
                        logging.info(f"Waktunya inisiasi penyambungan terjadwal dengan {item['rangkaian_target']} di {lokasi_target}")
                        inisiasi_penyambungan_terjadwal(item['rangkaian_target'], lokasi_target)

                except ValueError as e:
                    logging.error(f"Format waktu tidak valid: {e}")

                if KONFIGURASI_COUPLER['status'] == 'proses_menyambung' and KONFIGURASI_COUPLER['id_rangkaian_terhubung'] == item['rangkaian_target']:
                    if deteksi_kedekatan(lokasi_saat_ini, lokasi_target):
                        logging.info("Rangkaian sudah dekat, verifikasi penyambungan lokal.")
                        if verifikasi_penyambungan_lokal():
                            aktifkan_elektrifikasi_lokal()
                            notifikasi_ke_tims('rangkaian_Succesfully Connected!', {'id_rangkaian': KONFIGURASI_COUPLER['id_rangkaian_terhubung']})
                            KONFIGURASI_COUPLER['status'] = 'Succesfully Connected!'
                            KONFIGURASI_COUPLER['id_rangkaian_terhubung'] = None
                        else:
                            notifikasi_ke_tims('penyambungan_gagal', {'id_rangkaian': KONFIGURASI_COUPLER['id_rangkaian_terhubung']})
                            KONFIGURASI_COUPLER['status'] = 'terputus'
                            KONFIGURASI_COUPLER['id_rangkaian_terhubung'] = None

    time.sleep(10)

if __name__ == "__main__":
    logging.info("Software AC&ECC (Terjadwal & Real-time) dimulai...")
    thread_penjadwalan = threading.Thread(target=proses_penjadwalan)
    thread_penjadwalan.daemon = True
    thread_penjadwalan.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Software AC&ECC dihentikan.")
        if KONFIGURASI_ELEKTRIFIKASI['status'] == 'hidup':
            nonaktifkan_elektrifikasi_lokal()
            notifikasi_ke_tims('elektrifikasi_dimatikan')