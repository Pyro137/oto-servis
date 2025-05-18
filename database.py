import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="oto_servis.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        try:
            # Cari (Customer) table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS cari (
                    cari_kodu TEXT PRIMARY KEY,
                    cari_adi TEXT NOT NULL,
                    telefon TEXT,
                    cari_tipi TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Araç (Vehicle) table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS arac (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cari_kodu TEXT,
                    plaka TEXT NOT NULL,
                    arac_tipi TEXT NOT NULL,
                    model_yili TEXT,
                    marka TEXT,
                    model TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cari_kodu) REFERENCES cari (cari_kodu)
                )
            ''')

            # Servis Kayıtları (Service Records) table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS servis_kayitlari (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    arac_id INTEGER,
                    tarih DATE NOT NULL,
                    tutar DECIMAL(10,2) NOT NULL,
                    durum TEXT NOT NULL,
                    onay_durumu TEXT DEFAULT 'BEKLEMEDE',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (arac_id) REFERENCES arac (id)
                )
            ''')

            # İşlem Detayları (Transaction Details) table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS islem_detaylari (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    servis_kayit_id INTEGER,
                    islem_aciklamasi TEXT NOT NULL,
                    tutar DECIMAL(10,2) NOT NULL,
                    aciklama TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (servis_kayit_id) REFERENCES servis_kayitlari (id)
                )
            ''')

            # Ödeme Hareketleri (Payment Transactions) table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS odeme_hareketleri (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cari_kodu TEXT,
                    tarih DATE NOT NULL,
                    tutar DECIMAL(10,2) NOT NULL,
                    odeme_tipi TEXT NOT NULL,
                    aciklama TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cari_kodu) REFERENCES cari (cari_kodu)
                )
            ''')

            # Kasa (Cash Register) table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS kasa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tarih DATE NOT NULL,
                    tutar DECIMAL(10,2) NOT NULL,
                    islem_tipi TEXT NOT NULL,
                    aciklama TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()

    # Cari (Customer) operations
    def add_cari(self, cari_kodu, cari_adi, telefon, cari_tipi):
        try:
            self.cursor.execute('''
                INSERT INTO cari (cari_kodu, cari_adi, telefon, cari_tipi)
                VALUES (?, ?, ?, ?)
            ''', (cari_kodu, cari_adi, telefon, cari_tipi))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding cari: {e}")
            return False

    def get_cari(self, cari_kodu):
        try:
            self.cursor.execute('SELECT * FROM cari WHERE cari_kodu = ?', (cari_kodu,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting cari: {e}")
            return None

    def get_all_cari(self):
        try:
            self.cursor.execute('SELECT * FROM cari')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all cari: {e}")
            return []

    # Araç (Vehicle) operations
    def add_arac(self, cari_kodu, plaka, arac_tipi, model_yili, marka, model):
        try:
            self.cursor.execute('''
                INSERT INTO arac (cari_kodu, plaka, arac_tipi, model_yili, marka, model)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (cari_kodu, plaka, arac_tipi, model_yili, marka, model))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding arac: {e}")
            return False

    def get_arac(self, plaka):
        try:
            self.cursor.execute('SELECT * FROM arac WHERE plaka = ?', (plaka,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting arac: {e}")
            return None

    def get_arac_by_cari(self, cari_kodu):
        """Seçili cariye ait araçları getirir"""
        try:
            self.cursor.execute('''
                SELECT plaka, arac_tipi, model_yili, marka, model
                FROM arac
                WHERE cari_kodu = ?
            ''', (cari_kodu,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting vehicles by customer: {e}")
            return []

    # Servis Kayıtları (Service Records) operations
    def add_servis_kayit(self, arac_id, tarih, tutar, durum):
        try:
            self.cursor.execute('''
                INSERT INTO servis_kayitlari (arac_id, tarih, tutar, durum)
                VALUES (?, ?, ?, ?)
            ''', (arac_id, tarih, tutar, durum))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding servis kayit: {e}")
            return None

    def get_servis_kayitlari(self, arac_id):
        try:
            self.cursor.execute('SELECT * FROM servis_kayitlari WHERE arac_id = ?', (arac_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting servis kayitlari: {e}")
            return []

    def get_servis_kayitlari_by_arac_and_status(self, arac_id, status):
        try:
            self.cursor.execute('''
                SELECT * FROM servis_kayitlari 
                WHERE arac_id = ? AND durum = ?
                ORDER BY created_at DESC
            ''', (arac_id, status))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting servis kayitlari: {e}")
            return []

    # İşlem Detayları (Transaction Details) operations
    def add_islem_detay(self, servis_kayit_id, islem_aciklamasi, tutar, aciklama):
        try:
            self.cursor.execute('''
                INSERT INTO islem_detaylari (servis_kayit_id, islem_aciklamasi, tutar, aciklama)
                VALUES (?, ?, ?, ?)
            ''', (servis_kayit_id, islem_aciklamasi, tutar, aciklama))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding islem detay: {e}")
            return False

    def get_islem_detaylari(self, servis_kayit_id):
        try:
            self.cursor.execute('SELECT * FROM islem_detaylari WHERE servis_kayit_id = ?', (servis_kayit_id,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting islem detaylari: {e}")
            return []

    # Ödeme Hareketleri (Payment Transactions) operations
    def add_odeme_hareket(self, cari_kodu, tarih, tutar, odeme_tipi, aciklama):
        try:
            self.cursor.execute('''
                INSERT INTO odeme_hareketleri (cari_kodu, tarih, tutar, odeme_tipi, aciklama)
                VALUES (?, ?, ?, ?, ?)
            ''', (cari_kodu, tarih, tutar, odeme_tipi, aciklama))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding odeme hareket: {e}")
            return False

    def get_odeme_hareketleri(self, cari_kodu):
        try:
            self.cursor.execute('SELECT * FROM odeme_hareketleri WHERE cari_kodu = ?', (cari_kodu,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting odeme hareketleri: {e}")
            return []

    def update_servis_kayit_status_and_total(self, servis_kayit_id, status, total_amount):
        try:
            self.cursor.execute('''
                UPDATE servis_kayitlari 
                SET durum = ?, tutar = ?
                WHERE id = ?
            ''', (status, total_amount, servis_kayit_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating servis kayit: {e}")
            return False

    def get_servis_kayitlari_by_status(self, status):
        """Fetches service records based on their status."""
        try:
            self.cursor.execute('''
                SELECT
                    sk.id,
                    a.plaka,
                    a.arac_tipi,
                    c.cari_kodu,
                    c.cari_adi,
                    c.telefon,
                    sk.tarih,
                    sk.tutar  -- Assuming 'tutar' is the column with the total amount in servis_kayitlari
                FROM servis_kayitlari sk
                JOIN arac a ON sk.arac_id = a.id
                JOIN cari c ON a.cari_kodu = c.cari_kodu
                WHERE sk.durum = ?
            ''', (status,))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching service records by status: {e}")
            return []

    def get_cari_bakiye(self, cari_kodu):
        """Hesaplar cari bakiyesini (borç - alacak)"""
        try:
            # Servis kayıtlarından borç hesapla
            self.cursor.execute('''
                SELECT COALESCE(SUM(sk.tutar), 0)
                FROM servis_kayitlari sk
                JOIN arac a ON sk.arac_id = a.id
                WHERE a.cari_kodu = ? AND sk.onay_durumu = 'ONAYLANDI'
            ''', (cari_kodu,))
            borc = self.cursor.fetchone()[0] or 0

            # Ödeme hareketlerinden alacak hesapla
            self.cursor.execute('''
                SELECT COALESCE(SUM(tutar), 0)
                FROM odeme_hareketleri
                WHERE cari_kodu = ?
            ''', (cari_kodu,))
            alacak = self.cursor.fetchone()[0] or 0

            return borc - alacak
        except sqlite3.Error as e:
            print(f"Error calculating cari balance: {e}")
            return 0

    def update_servis_kayit_onay(self, servis_kayit_id, onay_durumu):
        """Servis kaydının onay durumunu günceller"""
        try:
            self.cursor.execute('''
                UPDATE servis_kayitlari 
                SET onay_durumu = ?
                WHERE id = ?
            ''', (onay_durumu, servis_kayit_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating service record approval: {e}")
            return False

    def add_kasa_hareketi(self, tarih, tutar, islem_tipi, aciklama):
        """Kasa hareketi ekler"""
        try:
            self.cursor.execute('''
                INSERT INTO kasa (tarih, tutar, islem_tipi, aciklama)
                VALUES (?, ?, ?, ?)
            ''', (tarih, tutar, islem_tipi, aciklama))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding cash register transaction: {e}")
            return False

    def get_kasa_bakiye(self):
        """Kasa bakiyesini hesaplar"""
        try:
            self.cursor.execute('''
                SELECT COALESCE(SUM(CASE 
                    WHEN islem_tipi = 'GIRIS' THEN tutar 
                    WHEN islem_tipi = 'CIKIS' THEN -tutar 
                    ELSE 0 
                END), 0)
                FROM kasa
            ''')
            return self.cursor.fetchone()[0] or 0
        except sqlite3.Error as e:
            print(f"Error calculating cash register balance: {e}")
            return 0

    def get_onayli_servis_kayitlari(self):
        """Onaylı servis kayıtlarını getirir"""
        try:
            self.cursor.execute('''
                SELECT
                    sk.id,
                    a.plaka,
                    a.arac_tipi,
                    c.cari_kodu,
                    c.cari_adi,
                    c.telefon,
                    sk.tarih,
                    sk.tutar
                FROM servis_kayitlari sk
                JOIN arac a ON sk.arac_id = a.id
                JOIN cari c ON a.cari_kodu = c.cari_kodu
                WHERE sk.onay_durumu = 'ONAYLANDI'
                ORDER BY sk.tarih DESC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching approved service records: {e}")
            return []

    def get_bekleyen_servis_kayitlari(self):
        """Bekleyen servis kayıtlarını getirir"""
        try:
            self.cursor.execute('''
                SELECT
                    sk.id,
                    a.plaka,
                    a.arac_tipi,
                    c.cari_kodu,
                    c.cari_adi,
                    c.telefon,
                    sk.tarih,
                    sk.tutar
                FROM servis_kayitlari sk
                JOIN arac a ON sk.arac_id = a.id
                JOIN cari c ON a.cari_kodu = c.cari_kodu
                WHERE sk.onay_durumu = 'BEKLEMEDE'
                ORDER BY sk.tarih DESC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching pending service records: {e}")
            return []

    def get_all_araclar(self):
        """Tüm araçları getirir"""
        try:
            self.cursor.execute('''
                SELECT 
                    c.cari_kodu,
                    c.cari_adi,
                    a.plaka,
                    a.arac_tipi,
                    a.model_yili,
                    a.marka,
                    a.model
                FROM arac a
                JOIN cari c ON a.cari_kodu = c.cari_kodu
                ORDER BY c.cari_adi, a.plaka
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting all vehicles: {e}")
            return []

    def get_odeme_hareketleri_by_date_range(self, start_date, end_date):
        """Belirli tarih aralığındaki ödeme hareketlerini getirir"""
        try:
            self.cursor.execute('''
                SELECT 
                    a.plaka,
                    a.arac_tipi,
                    c.cari_kodu,
                    c.cari_adi,
                    c.telefon,
                    oh.tarih,
                    oh.tutar
                FROM odeme_hareketleri oh
                JOIN cari c ON oh.cari_kodu = c.cari_kodu
                JOIN arac a ON c.cari_kodu = a.cari_kodu
                WHERE oh.tarih BETWEEN ? AND ?
                ORDER BY oh.tarih DESC
            ''', (start_date, end_date))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting payment transactions by date range: {e}")
            return []

    def get_arac_gecmisi(self):
        """Araç geçmişini getirir"""
        try:
            self.cursor.execute('''
                SELECT 
                    a.plaka,
                    a.marka,
                    a.model,
                    c.cari_adi,
                    MAX(sk.tarih) as son_servis_tarihi,
                    COUNT(sk.id) as toplam_servis_sayisi
                FROM arac a
                JOIN cari c ON a.cari_kodu = c.cari_kodu
                LEFT JOIN servis_kayitlari sk ON a.id = sk.arac_id
                GROUP BY a.plaka, a.marka, a.model, c.cari_adi
                ORDER BY son_servis_tarihi DESC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting vehicle history: {e}")
            return [] 