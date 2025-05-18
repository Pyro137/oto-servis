import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QFrame,
    QDialog, QLineEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('İŞLEM SEÇİNİZ ...')
        self.setGeometry(200, 100, 900, 500)
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # TANIMLAMALAR
        tanimlamalar_label = QLabel('TANIMLAMALAR')
        tanimlamalar_label.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        main_layout.addWidget(tanimlamalar_label)
        tanimlamalar_layout = QHBoxLayout()
        self.add_button(tanimlamalar_layout, 'ARAÇ KARTI EKLE')
        self.add_button(tanimlamalar_layout, 'ARAÇ LİSTESİ')
        self.add_button(tanimlamalar_layout, 'CARİ EKLE')
        self.add_button(tanimlamalar_layout, 'CARİ LİSTESİ')
        self.add_button(tanimlamalar_layout, 'ÖDEME HAREKETLERİ')
        main_layout.addLayout(tanimlamalar_layout)

        # Separator
        main_layout.addWidget(self.get_separator())

        # İŞ TANIM VE SORGULAMA
        is_tanim_label = QLabel('İŞ TANIM VE SORGULAMA')
        is_tanim_label.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        main_layout.addWidget(is_tanim_label)
        is_tanim_layout = QHBoxLayout()
        self.add_button(is_tanim_layout, 'SERVİS GİRİŞİ EKLE')
        self.add_button(is_tanim_layout, 'KAYIT KABUL')
        self.add_button(is_tanim_layout, 'ONAYLI KAYITLAR')
        self.add_button(is_tanim_layout, 'RANDEVU')
        self.add_button(is_tanim_layout, 'ARAÇ GEÇMİŞİ')
        main_layout.addLayout(is_tanim_layout)

        # Separator
        main_layout.addWidget(self.get_separator())

        # FİNANS - DİĞER
        finans_label = QLabel('FİNANS - DİĞER')
        finans_label.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        main_layout.addWidget(finans_label)
        finans_layout = QHBoxLayout()
        self.add_button(finans_layout, 'KASA')
        self.add_button(finans_layout, 'EXCELİ GÖSTER')
        self.add_button(finans_layout, 'VERİTABANI YOLU DEĞİŞTİR')
        self.add_button(finans_layout, 'SİSTEMİ KAPAT')
        main_layout.addLayout(finans_layout)

        # Bottom bar
        bottom_layout = QHBoxLayout()
        tarih_label = QLabel(QDate.currentDate().toString('dd.MM.yyyy'))
        bottom_layout.addWidget(tarih_label)
        bottom_layout.addStretch()
        hosgeldiniz_label = QLabel('OTO SERVİS PROGRAMINA HOŞGELDİNİZ')
        bottom_layout.addWidget(hosgeldiniz_label)
        main_layout.addLayout(bottom_layout)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def add_button(self, layout, text):
        btn = QPushButton(text)
        btn.setMinimumHeight(50)
        btn.setStyleSheet('font-size: 14px;')
        btn.clicked.connect(lambda: self.button_clicked(text))
        layout.addWidget(btn)

    def button_clicked(self, text):
        if text == 'SİSTEMİ KAPAT':
            self.close()
        elif text == 'ARAÇ KARTI EKLE':
            dialog = AracKartiFormu(self)
            dialog.exec_()
        elif text == 'CARİ EKLE':
            dialog = CariFormu(self)
            dialog.exec_()
        elif text == 'CARİ LİSTESİ':
            dialog = CariListesiDialog(self)
            dialog.exec_()
        elif text == 'ARAÇ LİSTESİ':
            dialog = AracListesiDialog(self)
            dialog.exec_()
        elif text == 'ÖDEME HAREKETLERİ':
            dialog = OdemeHareketleriDialog(self)
            dialog.exec_()
        elif text == 'SERVİS GİRİŞİ EKLE':
            dialog = ServisGirisiEkleDialog(self)
            dialog.exec_()
        elif text == 'KAYIT KABUL':
            dialog = KayitKabulDialog(self)
            dialog.exec_()
        elif text == 'ONAYLI KAYITLAR':
            dialog = OnayliKayitlarDialog(self)
            dialog.exec_()
        elif text == 'ARAÇ GEÇMİŞİ':
            dialog = CariListesiDialog(self)
            dialog.exec_()
        else:
            QMessageBox.information(self, 'Bilgi', f'{text} tıklandı!')

    def get_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet('color: #888;')
        return line

class AracKartiFormu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Araç Kartı Formu')
        self.setFixedSize(450, 350)
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Cari Seçimi
        cari_secim_label = QLabel('Cari Seçimi Yapınız')
        cari_secim_label.setStyleSheet('font-weight: bold;')
        ana_layout.addWidget(cari_secim_label)

        cari_layout = QGridLayout()
        cari_kodu_label = QLabel('Cari Kodu *')
        self.cari_kodu_edit = QLineEdit()
        self.cari_kodu_edit.setReadOnly(True)
        cari_unvani_label = QLabel('Cari Ünvanı *')
        self.cari_unvani_edit = QLineEdit()
        self.cari_unvani_edit.setReadOnly(True)
        sec_btn = QPushButton('Seç')
        sec_btn.setFixedWidth(60)
        sec_btn.clicked.connect(self.cari_sec)
        cari_layout.addWidget(cari_kodu_label, 0, 0)
        cari_layout.addWidget(self.cari_kodu_edit, 0, 1)
        cari_layout.addWidget(sec_btn, 0, 2)
        cari_layout.addWidget(cari_unvani_label, 1, 0)
        cari_layout.addWidget(self.cari_unvani_edit, 1, 1, 1, 2)
        ana_layout.addLayout(cari_layout)

        # Araç Bilgileri
        arac_bilgi_label = QLabel('Araç Bilgilerini Giriniz')
        arac_bilgi_label.setStyleSheet('font-weight: bold;')
        ana_layout.addWidget(arac_bilgi_label)

        arac_layout = QGridLayout()
        plaka_label = QLabel('Plaka *')
        self.plaka_edit = QLineEdit()
        arac_tipi_label = QLabel('Araç Tipi *')
        self.arac_tipi_combo = QComboBox()
        self.arac_tipi_combo.addItems(['Otomobil', 'Kamyonet', 'Minibüs', 'Motosiklet', 'Diğer'])
        model_yili_label = QLabel('Model Yılı')
        self.model_yili_edit = QLineEdit()
        marka_label = QLabel('Marka')
        self.marka_edit = QLineEdit()
        model_label = QLabel('Model')
        self.model_edit = QLineEdit()
        arac_layout.addWidget(plaka_label, 0, 0)
        arac_layout.addWidget(self.plaka_edit, 0, 1)
        arac_layout.addWidget(arac_tipi_label, 1, 0)
        arac_layout.addWidget(self.arac_tipi_combo, 1, 1)
        arac_layout.addWidget(model_yili_label, 2, 0)
        arac_layout.addWidget(self.model_yili_edit, 2, 1)
        arac_layout.addWidget(marka_label, 3, 0)
        arac_layout.addWidget(self.marka_edit, 3, 1)
        arac_layout.addWidget(model_label, 4, 0)
        arac_layout.addWidget(self.model_edit, 4, 1)
        ana_layout.addLayout(arac_layout)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        kaydet_btn = QPushButton('Kaydet')
        iptal_btn = QPushButton('İptal')
        kaydet_btn.setStyleSheet('background-color: #e0e0e0;')
        iptal_btn.setStyleSheet('background-color: #f8d7da;')
        kaydet_btn.clicked.connect(self.kaydet)
        iptal_btn.clicked.connect(self.reject)
        btn_layout.addWidget(kaydet_btn)
        btn_layout.addWidget(iptal_btn)
        ana_layout.addLayout(btn_layout)

        self.setLayout(ana_layout)

    def cari_sec(self):
        """Cari seçme dialogunu açar"""
        def on_cari_select(kod, ad):
            self.cari_kodu_edit.setText(kod)
            self.cari_unvani_edit.setText(ad)
        
        dialog = CariSecDialog(self, on_select=on_cari_select)
        dialog.exec_()

    def kaydet(self):
        """Araç kartını kaydeder"""
        # Zorunlu alanları kontrol et
        if not self.cari_kodu_edit.text():
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir cari seçin!')
            return
        if not self.plaka_edit.text():
            QMessageBox.warning(self, 'Uyarı', 'Lütfen plaka girin!')
            return

        try:
            # Araç bilgilerini al
            cari_kodu = self.cari_kodu_edit.text()
            plaka = self.plaka_edit.text()
            arac_tipi = self.arac_tipi_combo.currentText()
            model_yili = self.model_yili_edit.text()
            marka = self.marka_edit.text()
            model = self.model_edit.text()

            # Veritabanına kaydet
            if self.db.add_arac(cari_kodu, plaka, arac_tipi, model_yili, marka, model):
                QMessageBox.information(self, 'Başarılı', 'Araç kaydı başarıyla eklendi!')
                self.accept()
            else:
                QMessageBox.warning(self, 'Hata', 'Araç kaydedilirken bir hata oluştu!')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Bir hata oluştu: {str(e)}')

class CariSecDialog(QDialog):
    def __init__(self, parent=None, on_select=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Listesi')
        self.setMinimumSize(500, 400)
        self.on_select = on_select
        self.selected_cari_kodu = None
        self.selected_cari_adi = None
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_aktar = QPushButton('Bilgileri Aktar')
        btn_iptal = QPushButton('İptal')
        btn_yeni = QPushButton('Yeni Ekle')
        btn_layout.addWidget(btn_aktar)
        btn_layout.addWidget(btn_iptal)
        btn_layout.addWidget(btn_yeni)
        ana_layout.addLayout(btn_layout)

        # Arama kutusu
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText('Cari Adı / Ünvanı')
        self.search_edit.textChanged.connect(self.filter_cari)
        ana_layout.addWidget(self.search_edit)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Cari Kodu', 'Cari Adı / Ünvanı', 'Telefon', 'Cari Tipi'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        ana_layout.addWidget(self.table)

        # Connect buttons
        btn_iptal.clicked.connect(self.reject)
        btn_aktar.clicked.connect(self.aktar)
        btn_yeni.clicked.connect(self.yeni_cari_ekle)  # Connect the Yeni Ekle button

        self.setLayout(ana_layout)
        self.load_cari_data()

    def yeni_cari_ekle(self):
        """Yeni cari ekleme dialogunu açar"""
        dialog = CariFormu(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_cari_data()  # Refresh the list after adding new customer

    def load_cari_data(self):
        """Carileri veritabanından yükler"""
        cariler = self.db.get_all_cari()
        self.table.setRowCount(len(cariler))
        
        for row, cari in enumerate(cariler):
            # cari_kodu, cari_adi, telefon, cari_tipi
            self.table.setItem(row, 0, QTableWidgetItem(str(cari[0])))  # cari_kodu
            self.table.setItem(row, 1, QTableWidgetItem(str(cari[1])))  # cari_adi
            self.table.setItem(row, 2, QTableWidgetItem(str(cari[2])))  # telefon
            self.table.setItem(row, 3, QTableWidgetItem(str(cari[3])))  # cari_tipi

    def filter_cari(self):
        """Cari listesini filtreler"""
        search_text = self.search_edit.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def aktar(self):
        """Seçili cariyi döndürür"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir cari seçin!')
            return
        
        # Seçili satırdaki cari bilgilerini al
        self.selected_cari_kodu = self.table.item(row, 0).text()
        self.selected_cari_adi = self.table.item(row, 1).text()
        
        # Eğer callback fonksiyonu varsa çağır
        if self.on_select:
            self.on_select(self.selected_cari_kodu, self.selected_cari_adi)
        
        # Dialog'u kapat
        self.accept()

class CariFormu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Formu')
        self.setFixedSize(400, 250)
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Başlık
        baslik_label = QLabel('Cari Bilgilerini Giriniz')
        baslik_label.setStyleSheet('font-weight: bold;')
        ana_layout.addWidget(baslik_label)

        form_layout = QGridLayout()
        cari_kodu_label = QLabel('Cari Kodu *')
        self.cari_kodu_edit = QLineEdit()
        cari_adi_label = QLabel('Cari Adı / Ünvanı *')
        self.cari_adi_edit = QLineEdit()
        telefon_label = QLabel('Telefon')
        self.telefon_edit = QLineEdit()
        cari_tipi_label = QLabel('Cari Tipi *')
        self.cari_tipi_combo = QComboBox()
        self.cari_tipi_combo.addItems(['Bireysel', 'Kurumsal'])
        form_layout.addWidget(cari_kodu_label, 0, 0)
        form_layout.addWidget(self.cari_kodu_edit, 0, 1)
        form_layout.addWidget(cari_adi_label, 1, 0)
        form_layout.addWidget(self.cari_adi_edit, 1, 1)
        form_layout.addWidget(telefon_label, 2, 0)
        form_layout.addWidget(self.telefon_edit, 2, 1)
        form_layout.addWidget(cari_tipi_label, 3, 0)
        form_layout.addWidget(self.cari_tipi_combo, 3, 1)
        ana_layout.addLayout(form_layout)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        kaydet_btn = QPushButton('Kaydet')
        iptal_btn = QPushButton('İptal')
        kaydet_btn.setStyleSheet('background-color: #e0e0e0;')
        iptal_btn.setStyleSheet('background-color: #f8d7da;')
        kaydet_btn.clicked.connect(self.kaydet)
        iptal_btn.clicked.connect(self.reject)
        btn_layout.addWidget(kaydet_btn)
        btn_layout.addWidget(iptal_btn)
        ana_layout.addLayout(btn_layout)

        self.setLayout(ana_layout)

    def kaydet(self):
        """Cari kaydını kaydeder"""
        # Zorunlu alanları kontrol et
        if not self.cari_kodu_edit.text():
            QMessageBox.warning(self, 'Uyarı', 'Lütfen cari kodu girin!')
            return
        if not self.cari_adi_edit.text():
            QMessageBox.warning(self, 'Uyarı', 'Lütfen cari adı girin!')
            return

        try:
            # Form verilerini al
            cari_kodu = self.cari_kodu_edit.text()
            cari_adi = self.cari_adi_edit.text()
            telefon = self.telefon_edit.text()
            cari_tipi = self.cari_tipi_combo.currentText()

            # Veritabanına kaydet
            if self.db.add_cari(cari_kodu, cari_adi, telefon, cari_tipi):
                QMessageBox.information(self, 'Başarılı', 'Cari kaydı başarıyla eklendi!')
                self.accept()
            else:
                QMessageBox.warning(self, 'Hata', 'Cari kaydedilirken bir hata oluştu!')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Bir hata oluştu: {str(e)}')

class CariListesiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Listesi')
        self.setMinimumSize(900, 500)
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_yeni = QPushButton('YENİ CARİ EKLE')
        btn_duzenle = QPushButton('KAYDI DÜZENLE')
        btn_sil = QPushButton('KAYDI SİL')
        btn_servis = QPushButton('SERVİS HAREKETLERİ')
        btn_odeme_al = QPushButton('ÖDEME AL')
        btn_odeme_yap = QPushButton('ÖDEME YAP')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_yeni, btn_duzenle, btn_sil, btn_servis, btn_odeme_al, btn_odeme_yap, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı')
        self.filtre_combo = QComboBox()
        self.filtre_combo.addItems(['', 'Tedarikçi', 'Müşteri'])
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(self.filtre_combo)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(3, 7)
        self.table.setHorizontalHeaderLabels([
            'Cari Kodu', 'Cari Adı / Ünvanı', 'Telefon No', 'Cari Tipi', 'Borç', 'Alacak', 'Bakiye'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # Örnek veriler
        self.data = [
            ['TD002', 'AHMET CANDAN', '05323323232', 'Tedarikçi', '6.550,00', '3.911,00', '2.639,00'],
            ['CR001', 'FATİH ÖZ', '05552221122', 'Müşteri', '13.969,57', '1.800,00', '12.169,57'],
            ['CR002', 'MUSTAFA CAN', '05332332636', 'Müşteri', '15.750,68', '13.000,00', '2.750,68'],
        ]
        for row, row_data in enumerate(self.data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                if col == 6 and value.replace('.', '').replace(',', '').startswith('-'):
                    item.setForeground(Qt.red)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        alt_label = QLabel('3 adet kayıt listeleniyor | Toplam Borç: 36.270,25 TL | Toplam Alacak: 18.711,00 TL | Genel Bakiye: 17.559,25 TL')
        ana_layout.addWidget(alt_label)

        # Kapat butonu işlevi
        btn_kapat.clicked.connect(self.reject)

        # Servis Hareketleri butonu işlevi
        btn_servis.clicked.connect(self.show_servis_hareketleri)

        # Cari tablosuna çift tıklama işlevi
        self.table.doubleClicked.connect(self.show_cari_arac_listesi)

        self.setLayout(ana_layout)

    def show_servis_hareketleri(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir cari seçin!')
            return
        cari = self.data[row]
        # Örnek: Sadece AHMET CANDAN için servis kaydı gösterelim
        if cari[1] == 'AHMET CANDAN':
            cari_bilgi = {'cari_adi': cari[1]}
            servisler = [
                ['1.02.2025', '6.300,00', 'Kayıt Kapalı'],
            ]
        else:
            cari_bilgi = {'cari_adi': cari[1]}
            servisler = []
        dialog = CariServisKayitlariDialog(self, cari_bilgi, servisler)
        dialog.exec_()

    def show_cari_arac_listesi(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir cari seçin!')
            return
        cari_kodu = self.table.item(row, 0).text()
        cari_adi = self.table.item(row, 1).text()
        # Burada CariAracListesiDialog'u çağıracağız
        dialog = CariAracListesiDialog(self, cari_kodu, cari_adi)
        dialog.exec_()

class CariAracListesiDialog(QDialog):
    def __init__(self, parent=None, cari_kodu=None, cari_adi=None):
        super().__init__(parent)
        self.setWindowTitle(f'{cari_adi} ({cari_kodu}) - Araç Listesi')
        self.setMinimumSize(950, 500)
        self.cari_kodu = cari_kodu
        self.cari_adi = cari_adi
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar (AracListesiDialog'a benzer butonlar eklenebilir)
        btn_layout = QHBoxLayout()
        btn_servis = QPushButton('SERVİS KAYITLARI')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_servis, btn_pdf, btn_kapat]:
             btn.setMinimumHeight(40)
             btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanı (isteğe bağlı)
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Plaka, Marka veya Model')
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(0, 5) # Başlangıçta boş
        self.table.setHorizontalHeaderLabels([
            'Araç Plakası', 'Araç Tipi', 'Model Yılı', 'Marka', 'Model'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        self.alt_label = QLabel('0 adet araç listeleniyor')
        ana_layout.addWidget(self.alt_label)

        # Kapat butonu işlevi
        btn_kapat.clicked.connect(self.reject)

        # Servis Kayıtları butonu işlevi (ileride eklenecek)
        # btn_servis.clicked.connect(self.show_servis_kayitlari)

        self.setLayout(ana_layout)

        # Örnek veri yükleme (gerçek uygulamada veritabanından gelecek)
        self.load_arac_data()

        # Tabloya çift tıklama işlevi
        self.table.doubleClicked.connect(self.show_servis_kayitlari)

    def load_arac_data(self):
        # Burada seçilen cariye ait araç verileri veritabanından alınacak
        # Şimdilik örnek veri kullanıyoruz
        self.data = []
        if self.cari_kodu == 'CR001':
            self.data = [['CR001', 'FATİH ÖZ', '06 AA 001', 'Otomobil', '2023', 'MERCEDES', 'C 180 d']]
        elif self.cari_kodu == 'TD002':
            self.data = [['TD002', 'AHMET CANDAN', '02 BB 002', 'Otomobil', '2022', 'OPEL', ''], ['TD002', 'AHMET CANDAN', '01 AA 003', 'Otomobil', '2020', '', '']]
        elif self.cari_kodu == 'CR002':
            self.data = [['CR002', 'MUSTAFA CAN', '34 AA 001', 'Arazi, SUV & Pickup', '2014', 'AUDI', 'A7']]

        self.table.setRowCount(len(self.data))
        for row, row_data in enumerate(self.data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        self.alt_label.setText(f'{len(self.data)} adet araç listeleniyor')

    def show_servis_kayitlari(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir araç seçin!')
            return
        # Seçili araç bilgisini al
        arac = self.data[row]
        if arac[1] == 'FATİH ÖZ':
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = [
                ['7.03.2025', '1.750,36', 'Kayıt Kapalı'],
                ['8.03.2025', '12.210,21', 'Kayıt Kapalı'],
            ]
        elif arac[1] == 'AHMET CANDAN':
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = [
                ['15.03.2025', '3500,00', 'Kayıt Kapalı'],
            ]
        else:
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = []
        dialog = ServisKayitlariDialog(self, arac_bilgi, servisler)
        dialog.exec_()

class CariServisKayitlariDialog(QDialog):
    def __init__(self, parent=None, cari_bilgi=None, servisler=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Servis Kayıtları')
        self.setMinimumSize(700, 450)
        self.cari_bilgi = cari_bilgi or {}
        self.servisler = servisler or []
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        btn_detay.setMinimumHeight(40)
        btn_kapat.setMinimumHeight(40)
        btn_layout.addWidget(btn_detay)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_kapat)
        ana_layout.addLayout(btn_layout)

        # Cari Bilgileri
        grid = QGridLayout()
        grid.addWidget(QLabel('Cari Adı / Ünvanı'), 0, 0)
        grid.addWidget(QLabel(self.cari_bilgi.get('cari_adi', '')), 0, 1)
        ana_layout.addLayout(grid)

        # Servis Kayıtları Tablosu
        servis_label = QLabel('Servis Kayıtları')
        servis_label.setStyleSheet('font-weight: bold;')
        ana_layout.addWidget(servis_label)
        self.table = QTableWidget(len(self.servisler), 3)
        self.table.setHorizontalHeaderLabels(['Tarih', 'Tutar', 'Durum'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        for row, row_data in enumerate(self.servisler):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        toplam_tutar = sum(float(s[1].replace('.', '').replace(',', '.')) for s in self.servisler)
        alt_label = QLabel(f'{len(self.servisler)} adet kayıt listeleniyor | Toplam Tutar: {toplam_tutar:,.2f} TL'.replace(',', 'X').replace('.', ',').replace('X', '.'))
        ana_layout.addWidget(alt_label)

        btn_kapat.clicked.connect(self.reject)

        # DETAY GÖRÜNTÜLE butonu işlevi
        btn_detay.clicked.connect(self.show_detay)

        self.setLayout(ana_layout)

    def show_detay(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir servis kaydı seçin!')
            return
        # Seçili servis kaydı verilerini al
        servis_kaydi_data = self.servisler[row]
        
        # KayitDetayDialog için gerekli bilgileri hazırla
        # Arac ve Cari bilgileri self.arac_bilgi den geliyor
        # İşlem ve geçmiş servis bilgileri şimdilik örnek olarak kalacak
        kayit_detay = self.arac_bilgi.copy()
        # Seçilen servis kaydının tarih, tutar ve durumu eklenebilir veya KayitDetayDialog'un iç mantığına göre ayarlanabilir
        # Şimdilik sadece temel araç ve cari bilgisi aktarılıyor.
        
        # KayitDetayDialog'u aç
        dialog = KayitDetayDialog(self, kayit=kayit_detay)
        dialog.exec_()

class KayitDetayDialog(QDialog):
    def __init__(self, parent=None, kayit=None):
        super().__init__(parent)
        self.setWindowTitle('İş Emri Formu')
        self.setMinimumSize(900, 600)
        self.kayit = kayit or {}
        self.initUI()

    def initUI(self):
        ana_layout = QHBoxLayout()

        # Sol Panel: Araç ve Cari Bilgileri
        sol_widget = QWidget()
        sol_layout = QVBoxLayout()
        sol_widget.setLayout(sol_layout)

        baslik1 = QLabel('Araç - Cari Bilgileri')
        baslik1.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        sol_layout.addWidget(baslik1)

        form_grid = QGridLayout()
        form_grid.addWidget(QLabel('Cari Kodu'), 0, 0)
        form_grid.addWidget(QLabel(self.kayit.get('cari_kodu', '')), 0, 1)
        form_grid.addWidget(QLabel('Cari Adı / Ünvanı'), 1, 0)
        form_grid.addWidget(QLabel(self.kayit.get('cari_adi', '')), 1, 1)
        form_grid.addWidget(QLabel('Telefon'), 2, 0)
        form_grid.addWidget(QLabel(self.kayit.get('telefon', '')), 2, 1)
        form_grid.addWidget(QLabel('Cari Tipi *'), 3, 0)
        form_grid.addWidget(QLabel(self.kayit.get('cari_tipi', '')), 3, 1)
        form_grid.addWidget(QLabel('Plaka *'), 4, 0)
        form_grid.addWidget(QLabel(self.kayit.get('plaka', '')), 4, 1)
        form_grid.addWidget(QLabel('Araç Tipi *'), 5, 0)
        form_grid.addWidget(QLabel(self.kayit.get('arac_tipi', '')), 5, 1)
        form_grid.addWidget(QLabel('Model Yılı'), 6, 0)
        form_grid.addWidget(QLabel(self.kayit.get('model_yili', '')), 6, 1)
        form_grid.addWidget(QLabel('Marka'), 7, 0)
        form_grid.addWidget(QLabel(self.kayit.get('marka', '')), 7, 1)
        form_grid.addWidget(QLabel('Model'), 8, 0)
        form_grid.addWidget(QLabel(self.kayit.get('model', '')), 8, 1)
        sol_layout.addLayout(form_grid)

        # Geçmiş Servis Kayıtları
        gecmis_label = QLabel('Geçmiş Servis Kayıtları')
        gecmis_label.setStyleSheet('font-weight: bold;')
        sol_layout.addWidget(gecmis_label)
        self.gecmis_table = QTableWidget(3, 3)
        self.gecmis_table.setHorizontalHeaderLabels(['Tarih', 'Tutar', 'Durum'])
        self.gecmis_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.gecmis_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.gecmis_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.gecmis_table.setSelectionMode(QTableWidget.SingleSelection)
        gecmis_data = [
            ['7.03.2025', '13.750,68', 'Kayıt Kapalı'],
            ['8.03.2025', '2.000,00', 'Kayıt Kapalı'],
            ['10.03.2025', '5.750,00', 'Kayıt Açık'],
        ]
        for row, row_data in enumerate(gecmis_data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.gecmis_table.setItem(row, col, item)
        sol_layout.addWidget(self.gecmis_table)

        ana_layout.addWidget(sol_widget, 2)

        # Sağ Panel: İşlem ve Özet Bilgileri
        sag_widget = QWidget()
        sag_layout = QVBoxLayout()
        sag_widget.setLayout(sag_layout)

        baslik2 = QLabel('İşlem ve Özet Bilgileri')
        baslik2.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        sag_layout.addWidget(baslik2)

        # İşlem Bilgileri Girişi
        islem_giris_group = QWidget()
        islem_giris_layout = QGridLayout()
        islem_giris_group.setLayout(islem_giris_layout)
        islem_giris_layout.addWidget(QLabel('İşlem Açıklaması'), 0, 0)
        islem_giris_layout.addWidget(QLineEdit(), 0, 1)
        islem_giris_layout.addWidget(QLabel('İşlem Tutarı'), 0, 2)
        islem_giris_layout.addWidget(QLineEdit(), 0, 3)
        islem_giris_layout.addWidget(QLabel('Açıklama'), 0, 4)
        islem_giris_layout.addWidget(QLineEdit(), 0, 5)
        btn_ekle = QPushButton('Ekle')
        islem_giris_layout.addWidget(btn_ekle, 0, 6)
        sag_layout.addWidget(islem_giris_group)

        # İşlem Listesi
        islem_listesi_label = QLabel('İşlem Listesi')
        islem_listesi_label.setStyleSheet('font-weight: bold;')
        sag_layout.addWidget(islem_listesi_label)
        self.islem_table = QTableWidget(3, 3)
        self.islem_table.setHorizontalHeaderLabels(['İşlem Açıklaması', 'Tutar', 'Açıklama'])
        self.islem_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.islem_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.islem_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.islem_table.setSelectionMode(QTableWidget.SingleSelection)
        islem_data = [
            ['DENEME', '500', ''],
            ['DİĞER', '250', ''],
            ['MALZEME', '5000', 'MALZEMELER ALINDI'],
        ]
        for row, row_data in enumerate(islem_data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.islem_table.setItem(row, col, item)
        sag_layout.addWidget(self.islem_table)

        # İşlem Özeti
        ozet_group = QWidget()
        ozet_layout = QGridLayout()
        ozet_group.setLayout(ozet_layout)
        ozet_layout.addWidget(QLabel('İşlem Özeti'), 0, 0, 1, 2)
        ozet_layout.addWidget(QLabel('Toplam İşlem Sayısı'), 1, 0)
        toplam_islem = QLabel('3')
        toplam_islem.setStyleSheet('background: #ffffcc;')
        ozet_layout.addWidget(toplam_islem, 1, 1)
        ozet_layout.addWidget(QLabel('Toplam İşlem Tutarı'), 2, 0)
        toplam_tutar = QLabel('5.750,00')
        toplam_tutar.setStyleSheet('background: #ccffcc;')
        ozet_layout.addWidget(toplam_tutar, 2, 1)
        sag_layout.addWidget(ozet_group)

        # Alt butonlar
        alt_btn_layout = QHBoxLayout()
        alt_btn_layout.addStretch()
        btn_guncelle = QPushButton('GÜNCELLE')
        btn_temizle = QPushButton('İŞLEMLERİ TEMİZLE')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        alt_btn_layout.addWidget(btn_guncelle)
        alt_btn_layout.addWidget(btn_temizle)
        alt_btn_layout.addWidget(btn_pdf)
        alt_btn_layout.addWidget(btn_kapat)
        sag_layout.addLayout(alt_btn_layout)

        ana_layout.addWidget(sag_widget, 3)

        self.setLayout(ana_layout)
        btn_kapat.clicked.connect(self.reject)

class ServisGirisiEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('İş Emri Formu')
        self.setMinimumSize(1100, 650)
        self.initUI()

    def initUI(self):
        ana_layout = QHBoxLayout()

        # Sol Panel: Araç ve Cari Bilgileri
        sol_widget = QWidget()
        sol_layout = QVBoxLayout()
        sol_widget.setLayout(sol_layout)

        baslik1 = QLabel('Araç - Cari Bilgileri')
        baslik1.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        sol_layout.addWidget(baslik1)

        form_grid = QGridLayout()
        self.cari_kodu_edit = QLineEdit()
        self.cari_adi_edit = QLineEdit()
        form_grid.addWidget(QLabel('Cari Kodu'), 0, 0)
        form_grid.addWidget(self.cari_kodu_edit, 0, 1)
        form_grid.addWidget(QLabel('Cari Adı / Ünvanı'), 1, 0)
        form_grid.addWidget(self.cari_adi_edit, 1, 1)
        form_grid.addWidget(QLabel('Telefon'), 2, 0)
        form_grid.addWidget(QLineEdit(), 2, 1)
        form_grid.addWidget(QLabel('Cari Tipi *'), 3, 0)
        form_grid.addWidget(QComboBox(), 3, 1)
        sec_btn1 = QPushButton('Seç')
        form_grid.addWidget(sec_btn1, 3, 2)
        self.plaka_edit = QLineEdit()
        self.arac_tipi_combo = QComboBox()
        self.model_yili_edit = QLineEdit()
        self.marka_edit = QLineEdit()
        self.model_edit = QLineEdit()
        form_grid.addWidget(QLabel('Plaka *'), 4, 0)
        form_grid.addWidget(self.plaka_edit, 4, 1)
        form_grid.addWidget(QLabel('Araç Tipi *'), 5, 0)
        form_grid.addWidget(self.arac_tipi_combo, 5, 1)
        form_grid.addWidget(QLabel('Model Yılı'), 6, 0)
        form_grid.addWidget(self.model_yili_edit, 6, 1)
        form_grid.addWidget(QLabel('Marka'), 7, 0)
        form_grid.addWidget(self.marka_edit, 7, 1)
        form_grid.addWidget(QLabel('Model'), 8, 0)
        form_grid.addWidget(self.model_edit, 8, 1)
        sec_btn2 = QPushButton('Seç')
        form_grid.addWidget(sec_btn2, 8, 2)
        sol_layout.addLayout(form_grid)

        # Geçmiş Servis Kayıtları
        gecmis_label = QLabel('Geçmiş Servis Kayıtları')
        gecmis_label.setStyleSheet('font-weight: bold;')
        sol_layout.addWidget(gecmis_label)
        self.gecmis_table = QTableWidget(0, 3)
        self.gecmis_table.setHorizontalHeaderLabels(['Tarih', 'Tutar', 'Durum'])
        self.gecmis_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.gecmis_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.gecmis_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.gecmis_table.setSelectionMode(QTableWidget.SingleSelection)
        sol_layout.addWidget(self.gecmis_table)

        ana_layout.addWidget(sol_widget, 2)

        # Sağ Panel: İşlem ve Özet Bilgileri
        sag_widget = QWidget()
        sag_layout = QVBoxLayout()
        sag_widget.setLayout(sag_layout)

        baslik2 = QLabel('İşlem ve Özet Bilgileri')
        baslik2.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        sag_layout.addWidget(baslik2)

        # İşlem Bilgileri Girişi
        islem_giris_group = QWidget()
        islem_giris_layout = QGridLayout()
        islem_giris_group.setLayout(islem_giris_layout)
        islem_giris_layout.addWidget(QLabel('İşlem Açıklaması'), 0, 0)
        islem_giris_layout.addWidget(QLineEdit(), 0, 1)
        islem_giris_layout.addWidget(QLabel('İşlem Tutarı'), 0, 2)
        islem_giris_layout.addWidget(QLineEdit(), 0, 3)
        islem_giris_layout.addWidget(QLabel('Açıklama'), 0, 4)
        islem_giris_layout.addWidget(QLineEdit(), 0, 5)
        btn_ekle = QPushButton('Ekle')
        islem_giris_layout.addWidget(btn_ekle, 0, 6)
        sag_layout.addWidget(islem_giris_group)

        # İşlem Listesi
        islem_listesi_label = QLabel('İşlem Listesi')
        islem_listesi_label.setStyleSheet('font-weight: bold;')
        sag_layout.addWidget(islem_listesi_label)
        self.islem_table = QTableWidget(0, 3)
        self.islem_table.setHorizontalHeaderLabels(['İşlem Açıklaması', 'Tutar', 'Açıklama'])
        self.islem_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.islem_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.islem_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.islem_table.setSelectionMode(QTableWidget.SingleSelection)
        sag_layout.addWidget(self.islem_table)

        # İşlem Özeti
        ozet_group = QWidget()
        ozet_layout = QGridLayout()
        ozet_group.setLayout(ozet_layout)
        ozet_layout.addWidget(QLabel('İşlem Özeti'), 0, 0, 1, 2)
        ozet_layout.addWidget(QLabel('Toplam İşlem Sayısı'), 1, 0)
        toplam_islem = QLabel('0')
        toplam_islem.setStyleSheet('background: #ffffcc;')
        ozet_layout.addWidget(toplam_islem, 1, 1)
        ozet_layout.addWidget(QLabel('Toplam İşlem Tutarı'), 2, 0)
        toplam_tutar = QLabel('0,00')
        toplam_tutar.setStyleSheet('background: #ccffcc;')
        ozet_layout.addWidget(toplam_tutar, 2, 1)
        sag_layout.addWidget(ozet_group)

        # Alt butonlar
        alt_btn_layout = QHBoxLayout()
        alt_btn_layout.addStretch()
        btn_olustur = QPushButton('EMRİ OLUŞTUR')
        btn_temizle = QPushButton('İŞLEMLERİ TEMİZLE')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        alt_btn_layout.addWidget(btn_olustur)
        alt_btn_layout.addWidget(btn_temizle)
        alt_btn_layout.addWidget(btn_pdf)
        alt_btn_layout.addWidget(btn_kapat)
        sag_layout.addLayout(alt_btn_layout)

        ana_layout.addWidget(sag_widget, 3)

        self.setLayout(ana_layout)
        btn_kapat.clicked.connect(self.reject)
        sec_btn1.clicked.connect(self.cari_sec)
        sec_btn2.clicked.connect(self.arac_sec)

    def cari_sec(self):
        def on_cari_select(kod, ad):
            self.cari_kodu_edit.setText(kod)
            self.cari_adi_edit.setText(ad)
        
        dialog = CariSecDialog(self, on_select=on_cari_select)
        dialog.exec_()

    def arac_sec(self):
        def aktar_callback(plaka, tip, yil, marka, model):
            self.plaka_edit.setText(plaka)
            self.arac_tipi_combo.setCurrentText(tip)
            self.model_yili_edit.setText(yil)
            self.marka_edit.setText(marka)
            self.model_edit.setText(model)
        dialog = AracSecDialog(self, on_select=aktar_callback)
        dialog.exec_()

class AracListesiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Araç Listesi')
        self.setMinimumSize(950, 500)
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_yeni = QPushButton('YENİ ARAÇ EKLE')
        btn_duzenle = QPushButton('KAYDI DÜZENLE')
        btn_sil = QPushButton('KAYDI SİL')
        btn_servis = QPushButton('SERVİS KAYITLARI')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_yeni, btn_duzenle, btn_sil, btn_servis, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanı
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı veya Plaka')
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(4, 7)
        self.table.setHorizontalHeaderLabels([
            'Cari Kodu', 'Cari Adı / Ünvanı', 'Araç Plakası', 'Araç Tipi', 'Model Yılı', 'Marka', 'Model'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # Örnek veriler
        self.data = [
            ['TD002', 'AHMET CANDAN', '02 BB 002', 'Otomobil', '2022', 'OPEL', ''],
            ['TD002', 'AHMET CANDAN', '01 AA 003', 'Otomobil', '2020', '', ''],
            ['CR001', 'FATİH ÖZ', '06 AA 001', 'Otomobil', '2023', 'MERCEDES', 'C 180 d'],
            ['CR002', 'MUSTAFA CAN', '34 AA 001', 'Arazi, SUV & Pickup', '2014', 'AUDI', 'A7'],
        ]
        for row, row_data in enumerate(self.data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        alt_label = QLabel('4 adet kayıt listeleniyor')
        ana_layout.addWidget(alt_label)

        # Kapat butonu işlevi
        btn_kapat.clicked.connect(self.reject)

        # Servis Kayıtları butonu işlevi
        btn_servis.clicked.connect(self.show_servis_kayitlari)

        self.setLayout(ana_layout)

    def show_servis_kayitlari(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir araç seçin!')
            return
        # Örnek: Sadece FATİH ÖZ için servis kaydı gösterelim
        arac = self.data[row]
        if arac[1] == 'FATİH ÖZ':
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = [
                ['7.03.2025', '1.750,36', 'Kayıt Kapalı'],
                ['8.03.2025', '12.210,21', 'Kayıt Kapalı'],
            ]
        elif arac[1] == 'AHMET CANDAN':
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = [
                ['15.03.2025', '3500,00', 'Kayıt Kapalı'],
            ]
        else:
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = []
        dialog = ServisKayitlariDialog(self, arac_bilgi, servisler)
        dialog.exec_()

class ServisKayitlariDialog(QDialog):
    def __init__(self, parent=None, arac_bilgi=None, servisler=None):
        super().__init__(parent)
        self.setWindowTitle('Servis Kayıtları')
        self.setMinimumSize(700, 450)
        self.arac_bilgi = arac_bilgi or {}
        self.servisler = servisler or []
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        btn_detay.setMinimumHeight(40)
        btn_kapat.setMinimumHeight(40)
        btn_layout.addWidget(btn_detay)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_kapat)
        ana_layout.addLayout(btn_layout)

        # Araç Bilgileri
        grid = QGridLayout()
        grid.addWidget(QLabel('Cari Adı'), 0, 0)
        grid.addWidget(QLabel(self.arac_bilgi.get('cari_adi', '')), 0, 1)
        grid.addWidget(QLabel('Araç Tipi'), 0, 2)
        grid.addWidget(QLabel(self.arac_bilgi.get('arac_tipi', '')), 0, 3)
        grid.addWidget(QLabel('Marka'), 0, 4)
        grid.addWidget(QLabel(self.arac_bilgi.get('marka', '')), 0, 5)
        grid.addWidget(QLabel('Plaka'), 1, 0)
        grid.addWidget(QLabel(self.arac_bilgi.get('plaka', '')), 1, 1)
        grid.addWidget(QLabel('Model Yılı'), 1, 2)
        grid.addWidget(QLabel(self.arac_bilgi.get('model_yili', '')), 1, 3)
        grid.addWidget(QLabel('Model'), 1, 4)
        grid.addWidget(QLabel(self.arac_bilgi.get('model', '')), 1, 5)
        ana_layout.addLayout(grid)

        # Servis Kayıtları Tablosu
        servis_label = QLabel('Servis Kayıtları')
        servis_label.setStyleSheet('font-weight: bold;')
        ana_layout.addWidget(servis_label)
        self.table = QTableWidget(len(self.servisler), 3)
        self.table.setHorizontalHeaderLabels(['Tarih', 'Tutar', 'Durum'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        for row, row_data in enumerate(self.servisler):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        toplam_tutar = sum(float(s[1].replace('.', '').replace(',', '.')) for s in self.servisler)
        alt_label = QLabel(f'{len(self.servisler)} adet kayıt listeleniyor | Toplam Tutar: {toplam_tutar:,.2f} TL'.replace(',', 'X').replace('.', ',').replace('X', '.'))
        ana_layout.addWidget(alt_label)

        btn_kapat.clicked.connect(self.reject)

        # DETAY GÖRÜNTÜLE butonu işlevi
        btn_detay.clicked.connect(self.show_detay)

        self.setLayout(ana_layout)

    def show_detay(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir servis kaydı seçin!')
            return
        # Seçili servis kaydı verilerini al
        servis_kaydi_data = self.servisler[row]
        
        # KayitDetayDialog için gerekli bilgileri hazırla
        # Arac ve Cari bilgileri self.arac_bilgi den geliyor
        # İşlem ve geçmiş servis bilgileri şimdilik örnek olarak kalacak
        kayit_detay = self.arac_bilgi.copy()
        # Seçilen servis kaydının tarih, tutar ve durumu eklenebilir veya KayitDetayDialog'un iç mantığına göre ayarlanabilir
        # Şimdilik sadece temel araç ve cari bilgisi aktarılıyor.
        
        # KayitDetayDialog'u aç
        dialog = KayitDetayDialog(self, kayit=kayit_detay)
        dialog.exec_()

class OdemeHareketleriDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Ödeme Hareketleri')
        self.setMinimumSize(1100, 550)
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_onay_iptal = QPushButton('ONAYI İPTAL ET')
        btn_sil = QPushButton('KAYDI SİL')
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_odeme_al = QPushButton('ÖDEME AL')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_onay_iptal, btn_sil, btn_detay, btn_odeme_al, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı, Plaka veya Telefon')
        self.tarih1 = QDateEdit()
        self.tarih1.setDisplayFormat('d.MM.yyyy')
        self.tarih1.setDate(QDate(2025, 3, 3))
        self.tarih1.setCalendarPopup(True)
        self.tarih2 = QDateEdit()
        self.tarih2.setDisplayFormat('d.MM.yyyy')
        self.tarih2.setDate(QDate(2025, 3, 10))
        self.tarih2.setCalendarPopup(True)
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(self.tarih1)
        filtre_layout.addWidget(self.tarih2)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(5, 7)
        self.table.setHorizontalHeaderLabels([
            'Araç Plakası', 'Araç Tipi', 'Cari Kodu', 'Cari Ünvanı', 'Telefon', 'Tarih', 'Tutar'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # Örnek veriler
        data = [
            ['34 AA 001', 'Arazi, SUV & Pickup', 'CR002', 'MUSTAFA CAN', '05332332636', '10.03.2025', '5.750,00'],
            ['34 AA 001', 'Arazi, SUV & Pickup', 'CR002', 'MUSTAFA CAN', '05332332636', '8.03.2025', '2.000,00'],
            ['06 AA 001', 'Otomobil', 'CR001', 'FATİH ÖZ', '05552221122', '8.03.2025', '12.219,21'],
            ['34 AA 001', 'Arazi, SUV & Pickup', 'CR002', 'MUSTAFA CAN', '05332332636', '7.03.2025', '13.750,68'],
            ['06 AA 001', 'Otomobil', 'CR001', 'FATİH ÖZ', '05552221122', '7.03.2025', '1.750,36'],
        ]
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                if col == 6 and float(value.replace('.', '').replace(',', '.')) > 0:
                    item.setForeground(Qt.red)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        alt_label = QLabel('5 adet kayıt listeleniyor | Toplam Tutar: 35.470,25 TL | 3.03.2025 - 10.03.2025 Tarihleri arasında 7 günlük kayıt sonuçları.')
        ana_layout.addWidget(alt_label)

        # Kapat butonu işlevi
        btn_kapat.clicked.connect(self.reject)

        # ÖDEME AL butonu işlevi
        btn_odeme_al.clicked.connect(self.show_odeme_al_form)

        self.setLayout(ana_layout)

    def show_odeme_al_form(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        # Seçili satırdan cari bilgisi al (örnek olarak bazı sütunları kullanıyorum)
        cari_bilgi = {
            'cari_kodu': self.table.item(row, 2).text(),
            'cari_adi': self.table.item(row, 3).text(),
            'telefon': self.table.item(row, 4).text(),
            'bakiye': '8.500,68 TL - BORÇLU', # Örnek bakiye
        }
        dialog = OdemeAlmaFormuDialog(self, cari_bilgi)
        dialog.exec_()

class OnayliKayitlarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Onaylı Kayıtlar')
        self.setMinimumSize(1100, 550)
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_onay_iptal = QPushButton('ONAYI İPTAL ET')
        btn_sil = QPushButton('KAYDI SİL')
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_odeme_al = QPushButton('ÖDEME AL')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_onay_iptal, btn_sil, btn_detay, btn_odeme_al, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı, Plaka veya Telefon')
        self.tarih1 = QDateEdit()
        self.tarih1.setDisplayFormat('d.MM.yyyy')
        self.tarih1.setDate(QDate.currentDate())
        self.tarih1.setCalendarPopup(True)
        self.tarih2 = QDateEdit()
        self.tarih2.setDisplayFormat('d.MM.yyyy')
        self.tarih2.setDate(QDate.currentDate())
        self.tarih2.setCalendarPopup(True)
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(self.tarih1)
        filtre_layout.addWidget(self.tarih2)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Araç Plakası', 'Araç Tipi', 'Cari Kodu', 'Cari Ünvanı', 'Telefon', 'Tarih', 'Tutar'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        self.alt_label = QLabel()
        ana_layout.addWidget(self.alt_label)

        # Buton işlevleri
        btn_kapat.clicked.connect(self.reject)
        btn_onay_iptal.clicked.connect(self.onay_iptal)
        btn_sil.clicked.connect(self.kayit_sil)
        btn_detay.clicked.connect(self.show_detay)
        btn_odeme_al.clicked.connect(self.show_odeme_al_form)
        btn_filtrele.clicked.connect(self.filtrele)
        btn_temizle.clicked.connect(self.temizle)

        self.setLayout(ana_layout)
        self.load_data()

    def load_data(self):
        """Onaylı servis kayıtlarını yükler"""
        kayitlar = self.db.get_onayli_servis_kayitlari()
        self.table.setRowCount(len(kayitlar))
        
        toplam_tutar = 0
        for row, kayit in enumerate(kayitlar):
            for col, value in enumerate(kayit):
                item = QTableWidgetItem(str(value))
                if col == 7:  # Tutar sütunu
                    tutar = float(value)
                    toplam_tutar += tutar
                    item.setText(f"{tutar:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                self.table.setItem(row, col, item)
        
        self.alt_label.setText(f"{len(kayitlar)} adet kayıt listeleniyor | Toplam Tutar: {toplam_tutar:,.2f} TL".replace(',', 'X').replace('.', ',').replace('X', '.'))

    def onay_iptal(self):
        """Seçili kaydın onayını iptal eder"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        kayit_id = int(self.table.item(row, 0).text())
        if self.db.update_servis_kayit_onay(kayit_id, 'BEKLEMEDE'):
            QMessageBox.information(self, 'Başarılı', 'Kayıt onayı başarıyla iptal edildi!')
            self.load_data()
        else:
            QMessageBox.warning(self, 'Hata', 'Kayıt onayı iptal edilirken bir hata oluştu!')

    def kayit_sil(self):
        """Seçili kaydı siler"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        cevap = QMessageBox.question(self, 'Onay', 'Seçili kaydı silmek istediğinizden emin misiniz?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if cevap == QMessageBox.Yes:
            kayit_id = int(self.table.item(row, 0).text())
            # Silme işlemi eklenecek
            QMessageBox.information(self, 'Başarılı', 'Kayıt başarıyla silindi!')
            self.load_data()

    def show_detay(self):
        """Seçili kaydın detaylarını gösterir"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        kayit_id = int(self.table.item(row, 0).text())
        # KayitDetayDialog'u aç
        dialog = KayitDetayDialog(self, kayit_id=kayit_id)
        dialog.exec_()

    def show_odeme_al_form(self):
        """Ödeme alma formunu gösterir"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        cari_kodu = self.table.item(row, 3).text()
        cari_adi = self.table.item(row, 4).text()
        telefon = self.table.item(row, 5).text()
        bakiye = self.db.get_cari_bakiye(cari_kodu)
        
        cari_bilgi = {
            'cari_kodu': cari_kodu,
            'cari_adi': cari_adi,
            'telefon': telefon,
            'bakiye': f"{bakiye:,.2f} TL - {'BORÇLU' if bakiye > 0 else 'ALACAKLI'}".replace(',', 'X').replace('.', ',').replace('X', '.')
        }
        
        dialog = OdemeAlmaFormuDialog(self, cari_bilgi)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def filtrele(self):
        """Kayıtları filtreler"""
        # Filtreleme işlevi eklenecek
        pass

    def temizle(self):
        """Filtreleri temizler"""
        self.filtre_edit.clear()
        self.tarih1.setDate(QDate.currentDate())
        self.tarih2.setDate(QDate.currentDate())
        self.load_data()

class OdemeAlmaFormuDialog(QDialog):
    def __init__(self, parent=None, cari_bilgi=None):
        super().__init__(parent)
        self.setWindowTitle('Ödeme Alma Formu')
        self.setFixedSize(450, 450)
        self.cari_bilgi = cari_bilgi or {}
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Cari Bilgileri
        cari_bilgi_group = QWidget()
        cari_bilgi_layout = QGridLayout()
        cari_bilgi_group.setLayout(cari_bilgi_layout)
        cari_bilgi_layout.addWidget(QLabel('Cari Bilgileri'), 0, 0)
        cari_bilgi_layout.addWidget(QLabel('Cari Kodu'), 1, 0)
        cari_kodu_label = QLabel(self.cari_bilgi.get('cari_kodu', ''))
        cari_bilgi_layout.addWidget(cari_kodu_label, 1, 1)
        cari_bilgi_layout.addWidget(QLabel('Cari Adı / Ünvanı'), 2, 0)
        cari_adi_label = QLabel(self.cari_bilgi.get('cari_adi', ''))
        cari_bilgi_layout.addWidget(cari_adi_label, 2, 1)
        cari_bilgi_layout.addWidget(QLabel('Telefon'), 3, 0)
        telefon_label = QLabel(self.cari_bilgi.get('telefon', ''))
        cari_bilgi_layout.addWidget(telefon_label, 3, 1)
        cari_bilgi_layout.addWidget(QLabel('Bakiye'), 4, 0)
        bakiye_label = QLabel(self.cari_bilgi.get('bakiye', ''))
        cari_bilgi_layout.addWidget(bakiye_label, 4, 1)
        ana_layout.addWidget(cari_bilgi_group)

        # Ödeme Bilgileri Giriş
        odeme_giris_group = QWidget()
        odeme_giris_layout = QGridLayout()
        odeme_giris_group.setLayout(odeme_giris_layout)
        odeme_giris_layout.addWidget(QLabel('Ödeme Bilgilerini Giriniz'), 0, 0)
        odeme_giris_layout.addWidget(QLabel('Ödeme Tarihi'), 1, 0)
        self.odeme_tarihi_edit = QDateEdit()
        self.odeme_tarihi_edit.setDisplayFormat('d.MM.yyyy')
        self.odeme_tarihi_edit.setDate(QDate.currentDate())
        self.odeme_tarihi_edit.setCalendarPopup(True)
        odeme_giris_layout.addWidget(self.odeme_tarihi_edit, 1, 1)
        odeme_giris_layout.addWidget(QLabel('Ödeme Tipi'), 2, 0)
        self.odeme_tipi_combo = QComboBox()
        self.odeme_tipi_combo.addItems(['Nakit', 'Kredi Kartı', 'Banka Havalesi'])
        odeme_giris_layout.addWidget(self.odeme_tipi_combo, 2, 1)
        odeme_giris_layout.addWidget(QLabel('Tutar'), 3, 0)
        self.tutar_edit = QLineEdit()
        odeme_giris_layout.addWidget(self.tutar_edit, 3, 1)
        odeme_giris_layout.addWidget(QLabel('Açıklama'), 4, 0)
        self.aciklama_edit = QLineEdit()
        odeme_giris_layout.addWidget(self.aciklama_edit, 4, 1)
        ana_layout.addWidget(odeme_giris_group)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        kaydet_btn = QPushButton('Kaydet')
        iptal_btn = QPushButton('İptal')
        kaydet_btn.setStyleSheet('background-color: #e0e0e0;')
        iptal_btn.setStyleSheet('background-color: #f8d7da;')
        kaydet_btn.clicked.connect(self.kaydet)
        iptal_btn.clicked.connect(self.reject)
        btn_layout.addWidget(kaydet_btn)
        btn_layout.addWidget(iptal_btn)
        ana_layout.addLayout(btn_layout)

        self.setLayout(ana_layout)

    def kaydet(self):
        """Ödeme kaydını kaydeder"""
        try:
            # Form verilerini al
            tarih = self.odeme_tarihi_edit.date().toString('yyyy-MM-dd')
            odeme_tipi = self.odeme_tipi_combo.currentText()
            tutar_str = self.tutar_edit.text().replace('.', '').replace(',', '.')
            aciklama = self.aciklama_edit.text()
            cari_kodu = self.cari_bilgi.get('cari_kodu')

            # Tutarı sayıya çevir
            try:
                tutar = float(tutar_str)
            except ValueError:
                QMessageBox.warning(self, 'Hata', 'Lütfen geçerli bir tutar giriniz!')
                return

            # Veritabanına kaydet
            if self.db.add_odeme_hareketi(cari_kodu, tarih, tutar, odeme_tipi, aciklama):
                # Kasa hareketi ekle
                self.db.add_kasa_hareketi(tarih, tutar, 'GIRIS', f'Cari: {cari_kodu} - {aciklama}')
                QMessageBox.information(self, 'Başarılı', 'Ödeme başarıyla kaydedildi!')
                self.accept()
            else:
                QMessageBox.warning(self, 'Hata', 'Ödeme kaydedilirken bir hata oluştu!')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Bir hata oluştu: {str(e)}')

class AracGecmisiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Araç Geçmişi')
        self.setMinimumSize(950, 550)
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Plaka, Cari Kodu veya Cari Adı')
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(3, 6)
        self.table.setHorizontalHeaderLabels([
            'Plaka', 'Marka', 'Model', 'Cari Adı / Ünvanı', 'Son Servis Tarihi', 'Toplam Servis Sayısı'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # Örnek veriler
        data = [
            ['34 AA 001', 'AUDI', 'A7', 'MUSTAFA CAN', '10.03.2025', '3'],
            ['06 AA 001', 'MERCEDES', 'C 180 d', 'FATİH ÖZ', '8.03.2025', '2'],
            ['02 BB 002', 'OPEL', '', 'AHMET CANDAN', '7.03.2025', '1'],
        ]
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        alt_label = QLabel('3 adet araç geçmişi listeleniyor')
        ana_layout.addWidget(alt_label)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE') # Servis Kayıtları Detayı için
        btn_kapat = QPushButton('SAYFAYI Kapat')
        btn_layout.addWidget(btn_detay)
        btn_layout.addWidget(btn_kapat)
        ana_layout.addLayout(btn_layout)

        btn_kapat.clicked.connect(self.reject)
        # btn_detay.clicked.connect(self.show_detay) # Detay görüntüleme işlevi sonra eklenebilir

        self.setLayout(ana_layout)

class CariSecDialog(QDialog):
    def __init__(self, parent=None, on_select=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Listesi')
        self.setMinimumSize(500, 400)
        self.on_select = on_select
        self.selected_cari_kodu = None
        self.selected_cari_adi = None
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_aktar = QPushButton('Bilgileri Aktar')
        btn_iptal = QPushButton('İptal')
        btn_yeni = QPushButton('Yeni Ekle')
        btn_layout.addWidget(btn_aktar)
        btn_layout.addWidget(btn_iptal)
        btn_layout.addWidget(btn_yeni)
        ana_layout.addLayout(btn_layout)

        # Arama kutusu
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText('Cari Adı / Ünvanı')
        self.search_edit.textChanged.connect(self.filter_cari)
        ana_layout.addWidget(self.search_edit)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Cari Kodu', 'Cari Adı / Ünvanı', 'Telefon', 'Cari Tipi'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        ana_layout.addWidget(self.table)

        # Connect buttons
        btn_iptal.clicked.connect(self.reject)
        btn_aktar.clicked.connect(self.aktar)
        btn_yeni.clicked.connect(self.yeni_cari_ekle)  # Connect the Yeni Ekle button

        self.setLayout(ana_layout)
        self.load_cari_data()

    def yeni_cari_ekle(self):
        """Yeni cari ekleme dialogunu açar"""
        dialog = CariFormu(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_cari_data()  # Refresh the list after adding new customer

    def load_cari_data(self):
        """Carileri veritabanından yükler"""
        cariler = self.db.get_all_cari()
        self.table.setRowCount(len(cariler))
        
        for row, cari in enumerate(cariler):
            # cari_kodu, cari_adi, telefon, cari_tipi
            self.table.setItem(row, 0, QTableWidgetItem(str(cari[0])))  # cari_kodu
            self.table.setItem(row, 1, QTableWidgetItem(str(cari[1])))  # cari_adi
            self.table.setItem(row, 2, QTableWidgetItem(str(cari[2])))  # telefon
            self.table.setItem(row, 3, QTableWidgetItem(str(cari[3])))  # cari_tipi

    def filter_cari(self):
        """Cari listesini filtreler"""
        search_text = self.search_edit.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def aktar(self):
        """Seçili cariyi döndürür"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir cari seçin!')
            return
        
        # Seçili satırdaki cari bilgilerini al
        self.selected_cari_kodu = self.table.item(row, 0).text()
        self.selected_cari_adi = self.table.item(row, 1).text()
        
        # Eğer callback fonksiyonu varsa çağır
        if self.on_select:
            self.on_select(self.selected_cari_kodu, self.selected_cari_adi)
        
        # Dialog'u kapat
        self.accept()

class CariFormu(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Formu')
        self.setFixedSize(400, 250)
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Başlık
        baslik_label = QLabel('Cari Bilgilerini Giriniz')
        baslik_label.setStyleSheet('font-weight: bold;')
        ana_layout.addWidget(baslik_label)

        form_layout = QGridLayout()
        cari_kodu_label = QLabel('Cari Kodu *')
        self.cari_kodu_edit = QLineEdit()
        cari_adi_label = QLabel('Cari Adı / Ünvanı *')
        self.cari_adi_edit = QLineEdit()
        telefon_label = QLabel('Telefon')
        self.telefon_edit = QLineEdit()
        cari_tipi_label = QLabel('Cari Tipi *')
        self.cari_tipi_combo = QComboBox()
        self.cari_tipi_combo.addItems(['Bireysel', 'Kurumsal'])
        form_layout.addWidget(cari_kodu_label, 0, 0)
        form_layout.addWidget(self.cari_kodu_edit, 0, 1)
        form_layout.addWidget(cari_adi_label, 1, 0)
        form_layout.addWidget(self.cari_adi_edit, 1, 1)
        form_layout.addWidget(telefon_label, 2, 0)
        form_layout.addWidget(self.telefon_edit, 2, 1)
        form_layout.addWidget(cari_tipi_label, 3, 0)
        form_layout.addWidget(self.cari_tipi_combo, 3, 1)
        ana_layout.addLayout(form_layout)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        kaydet_btn = QPushButton('Kaydet')
        iptal_btn = QPushButton('İptal')
        kaydet_btn.setStyleSheet('background-color: #e0e0e0;')
        iptal_btn.setStyleSheet('background-color: #f8d7da;')
        kaydet_btn.clicked.connect(self.kaydet)
        iptal_btn.clicked.connect(self.reject)
        btn_layout.addWidget(kaydet_btn)
        btn_layout.addWidget(iptal_btn)
        ana_layout.addLayout(btn_layout)

        self.setLayout(ana_layout)

    def kaydet(self):
        """Cari kaydını kaydeder"""
        # Zorunlu alanları kontrol et
        if not self.cari_kodu_edit.text():
            QMessageBox.warning(self, 'Uyarı', 'Lütfen cari kodu girin!')
            return
        if not self.cari_adi_edit.text():
            QMessageBox.warning(self, 'Uyarı', 'Lütfen cari adı girin!')
            return

        try:
            # Form verilerini al
            cari_kodu = self.cari_kodu_edit.text()
            cari_adi = self.cari_adi_edit.text()
            telefon = self.telefon_edit.text()
            cari_tipi = self.cari_tipi_combo.currentText()

            # Veritabanına kaydet
            if self.db.add_cari(cari_kodu, cari_adi, telefon, cari_tipi):
                QMessageBox.information(self, 'Başarılı', 'Cari kaydı başarıyla eklendi!')
                self.accept()
            else:
                QMessageBox.warning(self, 'Hata', 'Cari kaydedilirken bir hata oluştu!')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Bir hata oluştu: {str(e)}')

class CariListesiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Listesi')
        self.setMinimumSize(900, 500)
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_yeni = QPushButton('YENİ CARİ EKLE')
        btn_duzenle = QPushButton('KAYDI DÜZENLE')
        btn_sil = QPushButton('KAYDI SİL')
        btn_servis = QPushButton('SERVİS HAREKETLERİ')
        btn_odeme_al = QPushButton('ÖDEME AL')
        btn_odeme_yap = QPushButton('ÖDEME YAP')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_yeni, btn_duzenle, btn_sil, btn_servis, btn_odeme_al, btn_odeme_yap, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı')
        self.filtre_combo = QComboBox()
        self.filtre_combo.addItems(['', 'Tedarikçi', 'Müşteri'])
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(self.filtre_combo)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(3, 7)
        self.table.setHorizontalHeaderLabels([
            'Cari Kodu', 'Cari Adı / Ünvanı', 'Telefon No', 'Cari Tipi', 'Borç', 'Alacak', 'Bakiye'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # Örnek veriler
        self.data = [
            ['TD002', 'AHMET CANDAN', '05323323232', 'Tedarikçi', '6.550,00', '3.911,00', '2.639,00'],
            ['CR001', 'FATİH ÖZ', '05552221122', 'Müşteri', '13.969,57', '1.800,00', '12.169,57'],
            ['CR002', 'MUSTAFA CAN', '05332332636', 'Müşteri', '15.750,68', '13.000,00', '2.750,68'],
        ]
        for row, row_data in enumerate(self.data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                if col == 6 and value.replace('.', '').replace(',', '').startswith('-'):
                    item.setForeground(Qt.red)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        alt_label = QLabel('3 adet kayıt listeleniyor | Toplam Borç: 36.270,25 TL | Toplam Alacak: 18.711,00 TL | Genel Bakiye: 17.559,25 TL')
        ana_layout.addWidget(alt_label)

        # Kapat butonu işlevi
        btn_kapat.clicked.connect(self.reject)

        # Servis Hareketleri butonu işlevi
        btn_servis.clicked.connect(self.show_servis_hareketleri)

        # Cari tablosuna çift tıklama işlevi
        self.table.doubleClicked.connect(self.show_cari_arac_listesi)

        self.setLayout(ana_layout)

    def show_servis_hareketleri(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir cari seçin!')
            return
        cari = self.data[row]
        # Örnek: Sadece AHMET CANDAN için servis kaydı gösterelim
        if cari[1] == 'AHMET CANDAN':
            cari_bilgi = {'cari_adi': cari[1]}
            servisler = [
                ['1.02.2025', '6.300,00', 'Kayıt Kapalı'],
            ]
        else:
            cari_bilgi = {'cari_adi': cari[1]}
            servisler = []
        dialog = CariServisKayitlariDialog(self, cari_bilgi, servisler)
        dialog.exec_()

    def show_cari_arac_listesi(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir cari seçin!')
            return
        cari_kodu = self.table.item(row, 0).text()
        cari_adi = self.table.item(row, 1).text()
        # Burada CariAracListesiDialog'u çağıracağız
        dialog = CariAracListesiDialog(self, cari_kodu, cari_adi)
        dialog.exec_()

class CariAracListesiDialog(QDialog):
    def __init__(self, parent=None, cari_kodu=None, cari_adi=None):
        super().__init__(parent)
        self.setWindowTitle(f'{cari_adi} ({cari_kodu}) - Araç Listesi')
        self.setMinimumSize(950, 500)
        self.cari_kodu = cari_kodu
        self.cari_adi = cari_adi
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar (AracListesiDialog'a benzer butonlar eklenebilir)
        btn_layout = QHBoxLayout()
        btn_servis = QPushButton('SERVİS KAYITLARI')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_servis, btn_pdf, btn_kapat]:
             btn.setMinimumHeight(40)
             btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanı (isteğe bağlı)
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Plaka, Marka veya Model')
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(0, 5) # Başlangıçta boş
        self.table.setHorizontalHeaderLabels([
            'Araç Plakası', 'Araç Tipi', 'Model Yılı', 'Marka', 'Model'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        self.alt_label = QLabel('0 adet araç listeleniyor')
        ana_layout.addWidget(self.alt_label)

        # Kapat butonu işlevi
        btn_kapat.clicked.connect(self.reject)

        # Servis Kayıtları butonu işlevi (ileride eklenecek)
        # btn_servis.clicked.connect(self.show_servis_kayitlari)

        self.setLayout(ana_layout)

        # Örnek veri yükleme (gerçek uygulamada veritabanından gelecek)
        self.load_arac_data()

        # Tabloya çift tıklama işlevi
        self.table.doubleClicked.connect(self.show_servis_kayitlari)

    def load_arac_data(self):
        # Burada seçilen cariye ait araç verileri veritabanından alınacak
        # Şimdilik örnek veri kullanıyoruz
        self.data = []
        if self.cari_kodu == 'CR001':
            self.data = [['CR001', 'FATİH ÖZ', '06 AA 001', 'Otomobil', '2023', 'MERCEDES', 'C 180 d']]
        elif self.cari_kodu == 'TD002':
            self.data = [['TD002', 'AHMET CANDAN', '02 BB 002', 'Otomobil', '2022', 'OPEL', ''], ['TD002', 'AHMET CANDAN', '01 AA 003', 'Otomobil', '2020', '', '']]
        elif self.cari_kodu == 'CR002':
            self.data = [['CR002', 'MUSTAFA CAN', '34 AA 001', 'Arazi, SUV & Pickup', '2014', 'AUDI', 'A7']]

        self.table.setRowCount(len(self.data))
        for row, row_data in enumerate(self.data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        self.alt_label.setText(f'{len(self.data)} adet araç listeleniyor')

    def show_servis_kayitlari(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir araç seçin!')
            return
        # Seçili araç bilgisini al
        arac = self.data[row]
        if arac[1] == 'FATİH ÖZ':
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = [
                ['7.03.2025', '1.750,36', 'Kayıt Kapalı'],
                ['8.03.2025', '12.210,21', 'Kayıt Kapalı'],
            ]
        elif arac[1] == 'AHMET CANDAN':
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = [
                ['15.03.2025', '3500,00', 'Kayıt Kapalı'],
            ]
        else:
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = []
        dialog = ServisKayitlariDialog(self, arac_bilgi, servisler)
        dialog.exec_()

class CariServisKayitlariDialog(QDialog):
    def __init__(self, parent=None, cari_bilgi=None, servisler=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Servis Kayıtları')
        self.setMinimumSize(700, 450)
        self.cari_bilgi = cari_bilgi or {}
        self.servisler = servisler or []
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        btn_detay.setMinimumHeight(40)
        btn_kapat.setMinimumHeight(40)
        btn_layout.addWidget(btn_detay)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_kapat)
        ana_layout.addLayout(btn_layout)

        # Cari Bilgileri
        grid = QGridLayout()
        grid.addWidget(QLabel('Cari Adı / Ünvanı'), 0, 0)
        grid.addWidget(QLabel(self.cari_bilgi.get('cari_adi', '')), 0, 1)
        ana_layout.addLayout(grid)

        # Servis Kayıtları Tablosu
        servis_label = QLabel('Servis Kayıtları')
        servis_label.setStyleSheet('font-weight: bold;')
        ana_layout.addWidget(servis_label)
        self.table = QTableWidget(len(self.servisler), 3)
        self.table.setHorizontalHeaderLabels(['Tarih', 'Tutar', 'Durum'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        for row, row_data in enumerate(self.servisler):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        toplam_tutar = sum(float(s[1].replace('.', '').replace(',', '.')) for s in self.servisler)
        alt_label = QLabel(f'{len(self.servisler)} adet kayıt listeleniyor | Toplam Tutar: {toplam_tutar:,.2f} TL'.replace(',', 'X').replace('.', ',').replace('X', '.'))
        ana_layout.addWidget(alt_label)

        btn_kapat.clicked.connect(self.reject)

        # DETAY GÖRÜNTÜLE butonu işlevi
        btn_detay.clicked.connect(self.show_detay)

        self.setLayout(ana_layout)

    def show_detay(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir servis kaydı seçin!')
            return
        # Seçili servis kaydı verilerini al
        servis_kaydi_data = self.servisler[row]
        
        # KayitDetayDialog için gerekli bilgileri hazırla
        # Arac ve Cari bilgileri self.arac_bilgi den geliyor
        # İşlem ve geçmiş servis bilgileri şimdilik örnek olarak kalacak
        kayit_detay = self.arac_bilgi.copy()
        # Seçilen servis kaydının tarih, tutar ve durumu eklenebilir veya KayitDetayDialog'un iç mantığına göre ayarlanabilir
        # Şimdilik sadece temel araç ve cari bilgisi aktarılıyor.
        
        # KayitDetayDialog'u aç
        dialog = KayitDetayDialog(self, kayit=kayit_detay)
        dialog.exec_()

class KayitDetayDialog(QDialog):
    def __init__(self, parent=None, kayit=None):
        super().__init__(parent)
        self.setWindowTitle('İş Emri Formu')
        self.setMinimumSize(900, 600)
        self.kayit = kayit or {}
        self.initUI()

    def initUI(self):
        ana_layout = QHBoxLayout()

        # Sol Panel: Araç ve Cari Bilgileri
        sol_widget = QWidget()
        sol_layout = QVBoxLayout()
        sol_widget.setLayout(sol_layout)

        baslik1 = QLabel('Araç - Cari Bilgileri')
        baslik1.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        sol_layout.addWidget(baslik1)

        form_grid = QGridLayout()
        form_grid.addWidget(QLabel('Cari Kodu'), 0, 0)
        form_grid.addWidget(QLabel(self.kayit.get('cari_kodu', '')), 0, 1)
        form_grid.addWidget(QLabel('Cari Adı / Ünvanı'), 1, 0)
        form_grid.addWidget(QLabel(self.kayit.get('cari_adi', '')), 1, 1)
        form_grid.addWidget(QLabel('Telefon'), 2, 0)
        form_grid.addWidget(QLabel(self.kayit.get('telefon', '')), 2, 1)
        form_grid.addWidget(QLabel('Cari Tipi *'), 3, 0)
        form_grid.addWidget(QLabel(self.kayit.get('cari_tipi', '')), 3, 1)
        form_grid.addWidget(QLabel('Plaka *'), 4, 0)
        form_grid.addWidget(QLabel(self.kayit.get('plaka', '')), 4, 1)
        form_grid.addWidget(QLabel('Araç Tipi *'), 5, 0)
        form_grid.addWidget(QLabel(self.kayit.get('arac_tipi', '')), 5, 1)
        form_grid.addWidget(QLabel('Model Yılı'), 6, 0)
        form_grid.addWidget(QLabel(self.kayit.get('model_yili', '')), 6, 1)
        form_grid.addWidget(QLabel('Marka'), 7, 0)
        form_grid.addWidget(QLabel(self.kayit.get('marka', '')), 7, 1)
        form_grid.addWidget(QLabel('Model'), 8, 0)
        form_grid.addWidget(QLabel(self.kayit.get('model', '')), 8, 1)
        sol_layout.addLayout(form_grid)

        # Geçmiş Servis Kayıtları
        gecmis_label = QLabel('Geçmiş Servis Kayıtları')
        gecmis_label.setStyleSheet('font-weight: bold;')
        sol_layout.addWidget(gecmis_label)
        self.gecmis_table = QTableWidget(3, 3)
        self.gecmis_table.setHorizontalHeaderLabels(['Tarih', 'Tutar', 'Durum'])
        self.gecmis_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.gecmis_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.gecmis_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.gecmis_table.setSelectionMode(QTableWidget.SingleSelection)
        gecmis_data = [
            ['7.03.2025', '13.750,68', 'Kayıt Kapalı'],
            ['8.03.2025', '2.000,00', 'Kayıt Kapalı'],
            ['10.03.2025', '5.750,00', 'Kayıt Açık'],
        ]
        for row, row_data in enumerate(gecmis_data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.gecmis_table.setItem(row, col, item)
        sol_layout.addWidget(self.gecmis_table)

        ana_layout.addWidget(sol_widget, 2)

        # Sağ Panel: İşlem ve Özet Bilgileri
        sag_widget = QWidget()
        sag_layout = QVBoxLayout()
        sag_widget.setLayout(sag_layout)

        baslik2 = QLabel('İşlem ve Özet Bilgileri')
        baslik2.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        sag_layout.addWidget(baslik2)

        # İşlem Bilgileri Girişi
        islem_giris_group = QWidget()
        islem_giris_layout = QGridLayout()
        islem_giris_group.setLayout(islem_giris_layout)
        islem_giris_layout.addWidget(QLabel('İşlem Açıklaması'), 0, 0)
        islem_giris_layout.addWidget(QLineEdit(), 0, 1)
        islem_giris_layout.addWidget(QLabel('İşlem Tutarı'), 0, 2)
        islem_giris_layout.addWidget(QLineEdit(), 0, 3)
        islem_giris_layout.addWidget(QLabel('Açıklama'), 0, 4)
        islem_giris_layout.addWidget(QLineEdit(), 0, 5)
        btn_ekle = QPushButton('Ekle')
        islem_giris_layout.addWidget(btn_ekle, 0, 6)
        sag_layout.addWidget(islem_giris_group)

        # İşlem Listesi
        islem_listesi_label = QLabel('İşlem Listesi')
        islem_listesi_label.setStyleSheet('font-weight: bold;')
        sag_layout.addWidget(islem_listesi_label)
        self.islem_table = QTableWidget(3, 3)
        self.islem_table.setHorizontalHeaderLabels(['İşlem Açıklaması', 'Tutar', 'Açıklama'])
        self.islem_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.islem_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.islem_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.islem_table.setSelectionMode(QTableWidget.SingleSelection)
        islem_data = [
            ['DENEME', '500', ''],
            ['DİĞER', '250', ''],
            ['MALZEME', '5000', 'MALZEMELER ALINDI'],
        ]
        for row, row_data in enumerate(islem_data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.islem_table.setItem(row, col, item)
        sag_layout.addWidget(self.islem_table)

        # İşlem Özeti
        ozet_group = QWidget()
        ozet_layout = QGridLayout()
        ozet_group.setLayout(ozet_layout)
        ozet_layout.addWidget(QLabel('İşlem Özeti'), 0, 0, 1, 2)
        ozet_layout.addWidget(QLabel('Toplam İşlem Sayısı'), 1, 0)
        toplam_islem = QLabel('3')
        toplam_islem.setStyleSheet('background: #ffffcc;')
        ozet_layout.addWidget(toplam_islem, 1, 1)
        ozet_layout.addWidget(QLabel('Toplam İşlem Tutarı'), 2, 0)
        toplam_tutar = QLabel('5.750,00')
        toplam_tutar.setStyleSheet('background: #ccffcc;')
        ozet_layout.addWidget(toplam_tutar, 2, 1)
        sag_layout.addWidget(ozet_group)

        # Alt butonlar
        alt_btn_layout = QHBoxLayout()
        alt_btn_layout.addStretch()
        btn_guncelle = QPushButton('GÜNCELLE')
        btn_temizle = QPushButton('İŞLEMLERİ TEMİZLE')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        alt_btn_layout.addWidget(btn_guncelle)
        alt_btn_layout.addWidget(btn_temizle)
        alt_btn_layout.addWidget(btn_pdf)
        alt_btn_layout.addWidget(btn_kapat)
        sag_layout.addLayout(alt_btn_layout)

        ana_layout.addWidget(sag_widget, 3)

        self.setLayout(ana_layout)
        btn_kapat.clicked.connect(self.reject)

class ServisGirisiEkleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('İş Emri Formu')
        self.setMinimumSize(1100, 650)
        self.initUI()

    def initUI(self):
        ana_layout = QHBoxLayout()

        # Sol Panel: Araç ve Cari Bilgileri
        sol_widget = QWidget()
        sol_layout = QVBoxLayout()
        sol_widget.setLayout(sol_layout)

        baslik1 = QLabel('Araç - Cari Bilgileri')
        baslik1.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        sol_layout.addWidget(baslik1)

        form_grid = QGridLayout()
        self.cari_kodu_edit = QLineEdit()
        self.cari_adi_edit = QLineEdit()
        form_grid.addWidget(QLabel('Cari Kodu'), 0, 0)
        form_grid.addWidget(self.cari_kodu_edit, 0, 1)
        form_grid.addWidget(QLabel('Cari Adı / Ünvanı'), 1, 0)
        form_grid.addWidget(self.cari_adi_edit, 1, 1)
        form_grid.addWidget(QLabel('Telefon'), 2, 0)
        form_grid.addWidget(QLineEdit(), 2, 1)
        form_grid.addWidget(QLabel('Cari Tipi *'), 3, 0)
        form_grid.addWidget(QComboBox(), 3, 1)
        sec_btn1 = QPushButton('Seç')
        form_grid.addWidget(sec_btn1, 3, 2)
        self.plaka_edit = QLineEdit()
        self.arac_tipi_combo = QComboBox()
        self.model_yili_edit = QLineEdit()
        self.marka_edit = QLineEdit()
        self.model_edit = QLineEdit()
        form_grid.addWidget(QLabel('Plaka *'), 4, 0)
        form_grid.addWidget(self.plaka_edit, 4, 1)
        form_grid.addWidget(QLabel('Araç Tipi *'), 5, 0)
        form_grid.addWidget(self.arac_tipi_combo, 5, 1)
        form_grid.addWidget(QLabel('Model Yılı'), 6, 0)
        form_grid.addWidget(self.model_yili_edit, 6, 1)
        form_grid.addWidget(QLabel('Marka'), 7, 0)
        form_grid.addWidget(self.marka_edit, 7, 1)
        form_grid.addWidget(QLabel('Model'), 8, 0)
        form_grid.addWidget(self.model_edit, 8, 1)
        sec_btn2 = QPushButton('Seç')
        form_grid.addWidget(sec_btn2, 8, 2)
        sol_layout.addLayout(form_grid)

        # Geçmiş Servis Kayıtları
        gecmis_label = QLabel('Geçmiş Servis Kayıtları')
        gecmis_label.setStyleSheet('font-weight: bold;')
        sol_layout.addWidget(gecmis_label)
        self.gecmis_table = QTableWidget(0, 3)
        self.gecmis_table.setHorizontalHeaderLabels(['Tarih', 'Tutar', 'Durum'])
        self.gecmis_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.gecmis_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.gecmis_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.gecmis_table.setSelectionMode(QTableWidget.SingleSelection)
        sol_layout.addWidget(self.gecmis_table)

        ana_layout.addWidget(sol_widget, 2)

        # Sağ Panel: İşlem ve Özet Bilgileri
        sag_widget = QWidget()
        sag_layout = QVBoxLayout()
        sag_widget.setLayout(sag_layout)

        baslik2 = QLabel('İşlem ve Özet Bilgileri')
        baslik2.setStyleSheet('font-weight: bold; font-size: 16px; background: #444; color: #fff; padding: 4px;')
        sag_layout.addWidget(baslik2)

        # İşlem Bilgileri Girişi
        islem_giris_group = QWidget()
        islem_giris_layout = QGridLayout()
        islem_giris_group.setLayout(islem_giris_layout)
        islem_giris_layout.addWidget(QLabel('İşlem Açıklaması'), 0, 0)
        islem_giris_layout.addWidget(QLineEdit(), 0, 1)
        islem_giris_layout.addWidget(QLabel('İşlem Tutarı'), 0, 2)
        islem_giris_layout.addWidget(QLineEdit(), 0, 3)
        islem_giris_layout.addWidget(QLabel('Açıklama'), 0, 4)
        islem_giris_layout.addWidget(QLineEdit(), 0, 5)
        btn_ekle = QPushButton('Ekle')
        islem_giris_layout.addWidget(btn_ekle, 0, 6)
        sag_layout.addWidget(islem_giris_group)

        # İşlem Listesi
        islem_listesi_label = QLabel('İşlem Listesi')
        islem_listesi_label.setStyleSheet('font-weight: bold;')
        sag_layout.addWidget(islem_listesi_label)
        self.islem_table = QTableWidget(0, 3)
        self.islem_table.setHorizontalHeaderLabels(['İşlem Açıklaması', 'Tutar', 'Açıklama'])
        self.islem_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.islem_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.islem_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.islem_table.setSelectionMode(QTableWidget.SingleSelection)
        sag_layout.addWidget(self.islem_table)

        # İşlem Özeti
        ozet_group = QWidget()
        ozet_layout = QGridLayout()
        ozet_group.setLayout(ozet_layout)
        ozet_layout.addWidget(QLabel('İşlem Özeti'), 0, 0, 1, 2)
        ozet_layout.addWidget(QLabel('Toplam İşlem Sayısı'), 1, 0)
        toplam_islem = QLabel('0')
        toplam_islem.setStyleSheet('background: #ffffcc;')
        ozet_layout.addWidget(toplam_islem, 1, 1)
        ozet_layout.addWidget(QLabel('Toplam İşlem Tutarı'), 2, 0)
        toplam_tutar = QLabel('0,00')
        toplam_tutar.setStyleSheet('background: #ccffcc;')
        ozet_layout.addWidget(toplam_tutar, 2, 1)
        sag_layout.addWidget(ozet_group)

        # Alt butonlar
        alt_btn_layout = QHBoxLayout()
        alt_btn_layout.addStretch()
        btn_olustur = QPushButton('EMRİ OLUŞTUR')
        btn_temizle = QPushButton('İŞLEMLERİ TEMİZLE')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        alt_btn_layout.addWidget(btn_olustur)
        alt_btn_layout.addWidget(btn_temizle)
        alt_btn_layout.addWidget(btn_pdf)
        alt_btn_layout.addWidget(btn_kapat)
        sag_layout.addLayout(alt_btn_layout)

        ana_layout.addWidget(sag_widget, 3)

        self.setLayout(ana_layout)
        btn_kapat.clicked.connect(self.reject)
        sec_btn1.clicked.connect(self.cari_sec)
        sec_btn2.clicked.connect(self.arac_sec)

    def cari_sec(self):
        def on_cari_select(kod, ad):
            self.cari_kodu_edit.setText(kod)
            self.cari_adi_edit.setText(ad)
        
        dialog = CariSecDialog(self, on_select=on_cari_select)
        dialog.exec_()

    def arac_sec(self):
        def aktar_callback(plaka, tip, yil, marka, model):
            self.plaka_edit.setText(plaka)
            self.arac_tipi_combo.setCurrentText(tip)
            self.model_yili_edit.setText(yil)
            self.marka_edit.setText(marka)
            self.model_edit.setText(model)
        dialog = AracSecDialog(self, on_select=aktar_callback)
        dialog.exec_()

class AracListesiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Araç Listesi')
        self.setMinimumSize(950, 500)
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_yeni = QPushButton('YENİ ARAÇ EKLE')
        btn_duzenle = QPushButton('KAYDI DÜZENLE')
        btn_sil = QPushButton('KAYDI SİL')
        btn_servis = QPushButton('SERVİS KAYITLARI')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_yeni, btn_duzenle, btn_sil, btn_servis, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanı
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı veya Plaka')
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(4, 7)
        self.table.setHorizontalHeaderLabels([
            'Cari Kodu', 'Cari Adı / Ünvanı', 'Araç Plakası', 'Araç Tipi', 'Model Yılı', 'Marka', 'Model'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # Örnek veriler
        self.data = [
            ['TD002', 'AHMET CANDAN', '02 BB 002', 'Otomobil', '2022', 'OPEL', ''],
            ['TD002', 'AHMET CANDAN', '01 AA 003', 'Otomobil', '2020', '', ''],
            ['CR001', 'FATİH ÖZ', '06 AA 001', 'Otomobil', '2023', 'MERCEDES', 'C 180 d'],
            ['CR002', 'MUSTAFA CAN', '34 AA 001', 'Arazi, SUV & Pickup', '2014', 'AUDI', 'A7'],
        ]
        for row, row_data in enumerate(self.data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        alt_label = QLabel('4 adet kayıt listeleniyor')
        ana_layout.addWidget(alt_label)

        # Kapat butonu işlevi
        btn_kapat.clicked.connect(self.reject)

        # Servis Kayıtları butonu işlevi
        btn_servis.clicked.connect(self.show_servis_kayitlari)

        self.setLayout(ana_layout)

    def show_servis_kayitlari(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir araç seçin!')
            return
        # Örnek: Sadece FATİH ÖZ için servis kaydı gösterelim
        arac = self.data[row]
        if arac[1] == 'FATİH ÖZ':
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = [
                ['7.03.2025', '1.750,36', 'Kayıt Kapalı'],
                ['8.03.2025', '12.210,21', 'Kayıt Kapalı'],
            ]
        elif arac[1] == 'AHMET CANDAN':
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = [
                ['15.03.2025', '3500,00', 'Kayıt Kapalı'],
            ]
        else:
            arac_bilgi = {
                'cari_adi': arac[1],
                'plaka': arac[2],
                'arac_tipi': arac[3],
                'model_yili': arac[4],
                'marka': arac[5],
                'model': arac[6],
            }
            servisler = []
        dialog = ServisKayitlariDialog(self, arac_bilgi, servisler)
        dialog.exec_()

class ServisKayitlariDialog(QDialog):
    def __init__(self, parent=None, arac_bilgi=None, servisler=None):
        super().__init__(parent)
        self.setWindowTitle('Servis Kayıtları')
        self.setMinimumSize(700, 450)
        self.arac_bilgi = arac_bilgi or {}
        self.servisler = servisler or []
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        btn_detay.setMinimumHeight(40)
        btn_kapat.setMinimumHeight(40)
        btn_layout.addWidget(btn_detay)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_kapat)
        ana_layout.addLayout(btn_layout)

        # Araç Bilgileri
        grid = QGridLayout()
        grid.addWidget(QLabel('Cari Adı'), 0, 0)
        grid.addWidget(QLabel(self.arac_bilgi.get('cari_adi', '')), 0, 1)
        grid.addWidget(QLabel('Araç Tipi'), 0, 2)
        grid.addWidget(QLabel(self.arac_bilgi.get('arac_tipi', '')), 0, 3)
        grid.addWidget(QLabel('Marka'), 0, 4)
        grid.addWidget(QLabel(self.arac_bilgi.get('marka', '')), 0, 5)
        grid.addWidget(QLabel('Plaka'), 1, 0)
        grid.addWidget(QLabel(self.arac_bilgi.get('plaka', '')), 1, 1)
        grid.addWidget(QLabel('Model Yılı'), 1, 2)
        grid.addWidget(QLabel(self.arac_bilgi.get('model_yili', '')), 1, 3)
        grid.addWidget(QLabel('Model'), 1, 4)
        grid.addWidget(QLabel(self.arac_bilgi.get('model', '')), 1, 5)
        ana_layout.addLayout(grid)

        # Servis Kayıtları Tablosu
        servis_label = QLabel('Servis Kayıtları')
        servis_label.setStyleSheet('font-weight: bold;')
        ana_layout.addWidget(servis_label)
        self.table = QTableWidget(len(self.servisler), 3)
        self.table.setHorizontalHeaderLabels(['Tarih', 'Tutar', 'Durum'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        for row, row_data in enumerate(self.servisler):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        toplam_tutar = sum(float(s[1].replace('.', '').replace(',', '.')) for s in self.servisler)
        alt_label = QLabel(f'{len(self.servisler)} adet kayıt listeleniyor | Toplam Tutar: {toplam_tutar:,.2f} TL'.replace(',', 'X').replace('.', ',').replace('X', '.'))
        ana_layout.addWidget(alt_label)

        btn_kapat.clicked.connect(self.reject)

        # DETAY GÖRÜNTÜLE butonu işlevi
        btn_detay.clicked.connect(self.show_detay)

        self.setLayout(ana_layout)

    def show_detay(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir servis kaydı seçin!')
            return
        # Seçili servis kaydı verilerini al
        servis_kaydi_data = self.servisler[row]
        
        # KayitDetayDialog için gerekli bilgileri hazırla
        # Arac ve Cari bilgileri self.arac_bilgi den geliyor
        # İşlem ve geçmiş servis bilgileri şimdilik örnek olarak kalacak
        kayit_detay = self.arac_bilgi.copy()
        # Seçilen servis kaydının tarih, tutar ve durumu eklenebilir veya KayitDetayDialog'un iç mantığına göre ayarlanabilir
        # Şimdilik sadece temel araç ve cari bilgisi aktarılıyor.
        
        # KayitDetayDialog'u aç
        dialog = KayitDetayDialog(self, kayit=kayit_detay)
        dialog.exec_()

class OdemeHareketleriDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Ödeme Hareketleri')
        self.setMinimumSize(1100, 550)
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_onay_iptal = QPushButton('ONAYI İPTAL ET')
        btn_sil = QPushButton('KAYDI SİL')
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_odeme_al = QPushButton('ÖDEME AL')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_onay_iptal, btn_sil, btn_detay, btn_odeme_al, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı, Plaka veya Telefon')
        self.tarih1 = QDateEdit()
        self.tarih1.setDisplayFormat('d.MM.yyyy')
        self.tarih1.setDate(QDate(2025, 3, 3))
        self.tarih1.setCalendarPopup(True)
        self.tarih2 = QDateEdit()
        self.tarih2.setDisplayFormat('d.MM.yyyy')
        self.tarih2.setDate(QDate(2025, 3, 10))
        self.tarih2.setCalendarPopup(True)
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(self.tarih1)
        filtre_layout.addWidget(self.tarih2)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(5, 7)
        self.table.setHorizontalHeaderLabels([
            'Araç Plakası', 'Araç Tipi', 'Cari Kodu', 'Cari Ünvanı', 'Telefon', 'Tarih', 'Tutar'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # Örnek veriler
        data = [
            ['34 AA 001', 'Arazi, SUV & Pickup', 'CR002', 'MUSTAFA CAN', '05332332636', '10.03.2025', '5.750,00'],
            ['34 AA 001', 'Arazi, SUV & Pickup', 'CR002', 'MUSTAFA CAN', '05332332636', '8.03.2025', '2.000,00'],
            ['06 AA 001', 'Otomobil', 'CR001', 'FATİH ÖZ', '05552221122', '8.03.2025', '12.219,21'],
            ['34 AA 001', 'Arazi, SUV & Pickup', 'CR002', 'MUSTAFA CAN', '05332332636', '7.03.2025', '13.750,68'],
            ['06 AA 001', 'Otomobil', 'CR001', 'FATİH ÖZ', '05552221122', '7.03.2025', '1.750,36'],
        ]
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                if col == 6 and float(value.replace('.', '').replace(',', '.')) > 0:
                    item.setForeground(Qt.red)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        alt_label = QLabel('5 adet kayıt listeleniyor | Toplam Tutar: 35.470,25 TL | 3.03.2025 - 10.03.2025 Tarihleri arasında 7 günlük kayıt sonuçları.')
        ana_layout.addWidget(alt_label)

        # Kapat butonu işlevi
        btn_kapat.clicked.connect(self.reject)

        # ÖDEME AL butonu işlevi
        btn_odeme_al.clicked.connect(self.show_odeme_al_form)

        self.setLayout(ana_layout)

    def show_odeme_al_form(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        # Seçili satırdan cari bilgisi al (örnek olarak bazı sütunları kullanıyorum)
        cari_bilgi = {
            'cari_kodu': self.table.item(row, 2).text(),
            'cari_adi': self.table.item(row, 3).text(),
            'telefon': self.table.item(row, 4).text(),
            'bakiye': '8.500,68 TL - BORÇLU', # Örnek bakiye
        }
        dialog = OdemeAlmaFormuDialog(self, cari_bilgi)
        dialog.exec_()

class OnayliKayitlarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Onaylı Kayıtlar')
        self.setMinimumSize(1100, 550)
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_onay_iptal = QPushButton('ONAYI İPTAL ET')
        btn_sil = QPushButton('KAYDI SİL')
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_odeme_al = QPushButton('ÖDEME AL')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_onay_iptal, btn_sil, btn_detay, btn_odeme_al, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı, Plaka veya Telefon')
        self.tarih1 = QDateEdit()
        self.tarih1.setDisplayFormat('d.MM.yyyy')
        self.tarih1.setDate(QDate.currentDate())
        self.tarih1.setCalendarPopup(True)
        self.tarih2 = QDateEdit()
        self.tarih2.setDisplayFormat('d.MM.yyyy')
        self.tarih2.setDate(QDate.currentDate())
        self.tarih2.setCalendarPopup(True)
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(self.tarih1)
        filtre_layout.addWidget(self.tarih2)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Araç Plakası', 'Araç Tipi', 'Cari Kodu', 'Cari Ünvanı', 'Telefon', 'Tarih', 'Tutar'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        self.alt_label = QLabel()
        ana_layout.addWidget(self.alt_label)

        # Buton işlevleri
        btn_kapat.clicked.connect(self.reject)
        btn_onay_iptal.clicked.connect(self.onay_iptal)
        btn_sil.clicked.connect(self.kayit_sil)
        btn_detay.clicked.connect(self.show_detay)
        btn_odeme_al.clicked.connect(self.show_odeme_al_form)
        btn_filtrele.clicked.connect(self.filtrele)
        btn_temizle.clicked.connect(self.temizle)

        self.setLayout(ana_layout)
        self.load_data()

    def load_data(self):
        """Onaylı servis kayıtlarını yükler"""
        kayitlar = self.db.get_onayli_servis_kayitlari()
        self.table.setRowCount(len(kayitlar))
        
        toplam_tutar = 0
        for row, kayit in enumerate(kayitlar):
            for col, value in enumerate(kayit):
                item = QTableWidgetItem(str(value))
                if col == 7:  # Tutar sütunu
                    tutar = float(value)
                    toplam_tutar += tutar
                    item.setText(f"{tutar:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                self.table.setItem(row, col, item)
        
        self.alt_label.setText(f"{len(kayitlar)} adet kayıt listeleniyor | Toplam Tutar: {toplam_tutar:,.2f} TL".replace(',', 'X').replace('.', ',').replace('X', '.'))

    def onay_iptal(self):
        """Seçili kaydın onayını iptal eder"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        kayit_id = int(self.table.item(row, 0).text())
        if self.db.update_servis_kayit_onay(kayit_id, 'BEKLEMEDE'):
            QMessageBox.information(self, 'Başarılı', 'Kayıt onayı başarıyla iptal edildi!')
            self.load_data()
        else:
            QMessageBox.warning(self, 'Hata', 'Kayıt onayı iptal edilirken bir hata oluştu!')

    def kayit_sil(self):
        """Seçili kaydı siler"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        cevap = QMessageBox.question(self, 'Onay', 'Seçili kaydı silmek istediğinizden emin misiniz?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if cevap == QMessageBox.Yes:
            kayit_id = int(self.table.item(row, 0).text())
            # Silme işlemi eklenecek
            QMessageBox.information(self, 'Başarılı', 'Kayıt başarıyla silindi!')
            self.load_data()

    def show_detay(self):
        """Seçili kaydın detaylarını gösterir"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        kayit_id = int(self.table.item(row, 0).text())
        # KayitDetayDialog'u aç
        dialog = KayitDetayDialog(self, kayit_id=kayit_id)
        dialog.exec_()

    def show_odeme_al_form(self):
        """Ödeme alma formunu gösterir"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        cari_kodu = self.table.item(row, 3).text()
        cari_adi = self.table.item(row, 4).text()
        telefon = self.table.item(row, 5).text()
        bakiye = self.db.get_cari_bakiye(cari_kodu)
        
        cari_bilgi = {
            'cari_kodu': cari_kodu,
            'cari_adi': cari_adi,
            'telefon': telefon,
            'bakiye': f"{bakiye:,.2f} TL - {'BORÇLU' if bakiye > 0 else 'ALACAKLI'}".replace(',', 'X').replace('.', ',').replace('X', '.')
        }
        
        dialog = OdemeAlmaFormuDialog(self, cari_bilgi)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()

    def filtrele(self):
        """Kayıtları filtreler"""
        # Filtreleme işlevi eklenecek
        pass

    def temizle(self):
        """Filtreleri temizler"""
        self.filtre_edit.clear()
        self.tarih1.setDate(QDate.currentDate())
        self.tarih2.setDate(QDate.currentDate())
        self.load_data()

class OdemeAlmaFormuDialog(QDialog):
    def __init__(self, parent=None, cari_bilgi=None):
        super().__init__(parent)
        self.setWindowTitle('Ödeme Alma Formu')
        self.setFixedSize(450, 450)
        self.cari_bilgi = cari_bilgi or {}
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Cari Bilgileri
        cari_bilgi_group = QWidget()
        cari_bilgi_layout = QGridLayout()
        cari_bilgi_group.setLayout(cari_bilgi_layout)
        cari_bilgi_layout.addWidget(QLabel('Cari Bilgileri'), 0, 0)
        cari_bilgi_layout.addWidget(QLabel('Cari Kodu'), 1, 0)
        cari_kodu_label = QLabel(self.cari_bilgi.get('cari_kodu', ''))
        cari_bilgi_layout.addWidget(cari_kodu_label, 1, 1)
        cari_bilgi_layout.addWidget(QLabel('Cari Adı / Ünvanı'), 2, 0)
        cari_adi_label = QLabel(self.cari_bilgi.get('cari_adi', ''))
        cari_bilgi_layout.addWidget(cari_adi_label, 2, 1)
        cari_bilgi_layout.addWidget(QLabel('Telefon'), 3, 0)
        telefon_label = QLabel(self.cari_bilgi.get('telefon', ''))
        cari_bilgi_layout.addWidget(telefon_label, 3, 1)
        cari_bilgi_layout.addWidget(QLabel('Bakiye'), 4, 0)
        bakiye_label = QLabel(self.cari_bilgi.get('bakiye', ''))
        cari_bilgi_layout.addWidget(bakiye_label, 4, 1)
        ana_layout.addWidget(cari_bilgi_group)

        # Ödeme Bilgileri Giriş
        odeme_giris_group = QWidget()
        odeme_giris_layout = QGridLayout()
        odeme_giris_group.setLayout(odeme_giris_layout)
        odeme_giris_layout.addWidget(QLabel('Ödeme Bilgilerini Giriniz'), 0, 0)
        odeme_giris_layout.addWidget(QLabel('Ödeme Tarihi'), 1, 0)
        self.odeme_tarihi_edit = QDateEdit()
        self.odeme_tarihi_edit.setDisplayFormat('d.MM.yyyy')
        self.odeme_tarihi_edit.setDate(QDate.currentDate())
        self.odeme_tarihi_edit.setCalendarPopup(True)
        odeme_giris_layout.addWidget(self.odeme_tarihi_edit, 1, 1)
        odeme_giris_layout.addWidget(QLabel('Ödeme Tipi'), 2, 0)
        self.odeme_tipi_combo = QComboBox()
        self.odeme_tipi_combo.addItems(['Nakit', 'Kredi Kartı', 'Banka Havalesi'])
        odeme_giris_layout.addWidget(self.odeme_tipi_combo, 2, 1)
        odeme_giris_layout.addWidget(QLabel('Tutar'), 3, 0)
        self.tutar_edit = QLineEdit()
        odeme_giris_layout.addWidget(self.tutar_edit, 3, 1)
        odeme_giris_layout.addWidget(QLabel('Açıklama'), 4, 0)
        self.aciklama_edit = QLineEdit()
        odeme_giris_layout.addWidget(self.aciklama_edit, 4, 1)
        ana_layout.addWidget(odeme_giris_group)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        kaydet_btn = QPushButton('Kaydet')
        iptal_btn = QPushButton('İptal')
        kaydet_btn.setStyleSheet('background-color: #e0e0e0;')
        iptal_btn.setStyleSheet('background-color: #f8d7da;')
        kaydet_btn.clicked.connect(self.kaydet)
        iptal_btn.clicked.connect(self.reject)
        btn_layout.addWidget(kaydet_btn)
        btn_layout.addWidget(iptal_btn)
        ana_layout.addLayout(btn_layout)

        self.setLayout(ana_layout)

    def kaydet(self):
        """Ödeme kaydını kaydeder"""
        try:
            # Form verilerini al
            tarih = self.odeme_tarihi_edit.date().toString('yyyy-MM-dd')
            odeme_tipi = self.odeme_tipi_combo.currentText()
            tutar_str = self.tutar_edit.text().replace('.', '').replace(',', '.')
            aciklama = self.aciklama_edit.text()
            cari_kodu = self.cari_bilgi.get('cari_kodu')

            # Tutarı sayıya çevir
            try:
                tutar = float(tutar_str)
            except ValueError:
                QMessageBox.warning(self, 'Hata', 'Lütfen geçerli bir tutar giriniz!')
                return

            # Veritabanına kaydet
            if self.db.add_odeme_hareketi(cari_kodu, tarih, tutar, odeme_tipi, aciklama):
                # Kasa hareketi ekle
                self.db.add_kasa_hareketi(tarih, tutar, 'GIRIS', f'Cari: {cari_kodu} - {aciklama}')
                QMessageBox.information(self, 'Başarılı', 'Ödeme başarıyla kaydedildi!')
                self.accept()
            else:
                QMessageBox.warning(self, 'Hata', 'Ödeme kaydedilirken bir hata oluştu!')
        except Exception as e:
            QMessageBox.warning(self, 'Hata', f'Bir hata oluştu: {str(e)}')

class AracGecmisiDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Araç Geçmişi')
        self.setMinimumSize(950, 550)
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Plaka, Cari Kodu veya Cari Adı')
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget(3, 6)
        self.table.setHorizontalHeaderLabels([
            'Plaka', 'Marka', 'Model', 'Cari Adı / Ünvanı', 'Son Servis Tarihi', 'Toplam Servis Sayısı'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        # Örnek veriler
        data = [
            ['34 AA 001', 'AUDI', 'A7', 'MUSTAFA CAN', '10.03.2025', '3'],
            ['06 AA 001', 'MERCEDES', 'C 180 d', 'FATİH ÖZ', '8.03.2025', '2'],
            ['02 BB 002', 'OPEL', '', 'AHMET CANDAN', '7.03.2025', '1'],
        ]
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        alt_label = QLabel('3 adet araç geçmişi listeleniyor')
        ana_layout.addWidget(alt_label)

        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE') # Servis Kayıtları Detayı için
        btn_kapat = QPushButton('SAYFAYI Kapat')
        btn_layout.addWidget(btn_detay)
        btn_layout.addWidget(btn_kapat)
        ana_layout.addLayout(btn_layout)

        btn_kapat.clicked.connect(self.reject)
        # btn_detay.clicked.connect(self.show_detay) # Detay görüntüleme işlevi sonra eklenebilir

        self.setLayout(ana_layout)

class CariSecDialog(QDialog):
    def __init__(self, parent=None, on_select=None):
        super().__init__(parent)
        self.setWindowTitle('Cari Listesi')
        self.setMinimumSize(500, 400)
        self.on_select = on_select
        self.selected_cari_kodu = None
        self.selected_cari_adi = None
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_aktar = QPushButton('Bilgileri Aktar')
        btn_iptal = QPushButton('İptal')
        btn_yeni = QPushButton('Yeni Ekle')
        btn_layout.addWidget(btn_aktar)
        btn_layout.addWidget(btn_iptal)
        btn_layout.addWidget(btn_yeni)
        ana_layout.addLayout(btn_layout)

        # Arama kutusu
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText('Cari Adı / Ünvanı')
        self.search_edit.textChanged.connect(self.filter_cari)
        ana_layout.addWidget(self.search_edit)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Cari Kodu', 'Cari Adı / Ünvanı', 'Telefon', 'Cari Tipi'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        ana_layout.addWidget(self.table)

        # Connect buttons
        btn_iptal.clicked.connect(self.reject)
        btn_aktar.clicked.connect(self.aktar)
        btn_yeni.clicked.connect(self.yeni_cari_ekle)  # Connect the Yeni Ekle button

        self.setLayout(ana_layout)
        self.load_cari_data()

    def yeni_cari_ekle(self):
        """Yeni cari ekleme dialogunu açar"""
        dialog = CariFormu(self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_cari_data()  # Refresh the list after adding new customer

    def load_cari_data(self):
        """Carileri veritabanından yükler"""
        cariler = self.db.get_all_cari()
        self.table.setRowCount(len(cariler))
        
        for row, cari in enumerate(cariler):
            # cari_kodu, cari_adi, telefon, cari_tipi
            self.table.setItem(row, 0, QTableWidgetItem(str(cari[0])))  # cari_kodu
            self.table.setItem(row, 1, QTableWidgetItem(str(cari[1])))  # cari_adi
            self.table.setItem(row, 2, QTableWidgetItem(str(cari[2])))  # telefon
            self.table.setItem(row, 3, QTableWidgetItem(str(cari[3])))  # cari_tipi

    def filter_cari(self):
        """Cari listesini filtreler"""
        search_text = self.search_edit.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)

    def aktar(self):
        """Seçili cariyi döndürür"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir cari seçin!')
            return
        
        # Seçili satırdaki cari bilgilerini al
        self.selected_cari_kodu = self.table.item(row, 0).text()
        self.selected_cari_adi = self.table.item(row, 1).text()
        
        # Eğer callback fonksiyonu varsa çağır
        if self.on_select:
            self.on_select(self.selected_cari_kodu, self.selected_cari_adi)
        
        # Dialog'u kapat
        self.accept()

class AracSecDialog(QDialog):
    def __init__(self, parent=None, on_select=None):
        super().__init__(parent)
        self.setWindowTitle('Araç Listesi')
        self.setMinimumSize(600, 400)
        self.on_select = on_select
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_aktar = QPushButton('Bilgileri Aktar')
        btn_iptal = QPushButton('İptal')
        btn_yeni = QPushButton('Yeni Ekle')
        btn_layout.addWidget(btn_aktar)
        btn_layout.addWidget(btn_iptal)
        btn_layout.addWidget(btn_yeni)
        ana_layout.addLayout(btn_layout)

        # Arama kutusu
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText('Araç Plakası, Marka, Model')
        ana_layout.addWidget(self.search_edit)

        # Tablo
        self.table = QTableWidget(2, 5)
        self.table.setHorizontalHeaderLabels([
            'Araç Plakası', 'Araç Tipi', 'Model Yılı', 'Marka', 'Model'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        data = [
            ['06 AA 001', 'Otomobil', '2023', 'MERCEDES', 'C 180 d'],
            ['34 AA 001', 'Arazi, SUV & Pickup', '2014', 'AUDI', 'A7'],
        ]
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                self.table.setItem(row, col, item)
        ana_layout.addWidget(self.table)

        btn_iptal.clicked.connect(self.reject)
        btn_aktar.clicked.connect(self.aktar)

        self.setLayout(ana_layout)

    def aktar(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir araç seçin!')
            return
        plaka = self.table.item(row, 0).text()
        tip = self.table.item(row, 1).text()
        yil = self.table.item(row, 2).text()
        marka = self.table.item(row, 3).text()
        model = self.table.item(row, 4).text()
        if self.on_select:
            self.on_select(plaka, tip, yil, marka, model)
        self.accept()

class KayitKabulDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Kayıt Kabul')
        self.setMinimumSize(1100, 550)
        self.db = Database()
        self.initUI()

    def initUI(self):
        ana_layout = QVBoxLayout()

        # Üst butonlar
        btn_layout = QHBoxLayout()
        btn_onayla = QPushButton('KAYDI ONAYLA')
        btn_reddet = QPushButton('KAYDI REDDET')
        btn_detay = QPushButton('DETAY GÖRÜNTÜLE')
        btn_pdf = QPushButton('PDF AKTAR')
        btn_kapat = QPushButton('SAYFAYI KAPAT')
        for btn in [btn_onayla, btn_reddet, btn_detay, btn_pdf, btn_kapat]:
            btn.setMinimumHeight(40)
            btn_layout.addWidget(btn)
        ana_layout.addLayout(btn_layout)

        # Filtre alanları
        filtre_layout = QHBoxLayout()
        self.filtre_edit = QLineEdit()
        self.filtre_edit.setPlaceholderText('Cari Kodu, Cari Adı, Plaka veya Telefon')
        self.tarih1 = QDateEdit()
        self.tarih1.setDisplayFormat('d.MM.yyyy')
        self.tarih1.setDate(QDate.currentDate())
        self.tarih1.setCalendarPopup(True)
        self.tarih2 = QDateEdit()
        self.tarih2.setDisplayFormat('d.MM.yyyy')
        self.tarih2.setDate(QDate.currentDate())
        self.tarih2.setCalendarPopup(True)
        btn_filtrele = QPushButton('Filtrele')
        btn_temizle = QPushButton('Temizle')
        filtre_layout.addWidget(self.filtre_edit)
        filtre_layout.addWidget(self.tarih1)
        filtre_layout.addWidget(self.tarih2)
        filtre_layout.addWidget(btn_filtrele)
        filtre_layout.addWidget(btn_temizle)
        ana_layout.addLayout(filtre_layout)

        # Tablo
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            'ID', 'Araç Plakası', 'Araç Tipi', 'Cari Kodu', 'Cari Ünvanı', 'Telefon', 'Tarih', 'Tutar'
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        ana_layout.addWidget(self.table)

        # Alt bilgi
        self.alt_label = QLabel()
        ana_layout.addWidget(self.alt_label)

        # Buton işlevleri
        btn_kapat.clicked.connect(self.reject)
        btn_onayla.clicked.connect(self.kayit_onayla)
        btn_reddet.clicked.connect(self.kayit_reddet)
        btn_detay.clicked.connect(self.show_detay)
        btn_filtrele.clicked.connect(self.filtrele)
        btn_temizle.clicked.connect(self.temizle)

        self.setLayout(ana_layout)
        self.load_data()

    def load_data(self):
        """Bekleyen servis kayıtlarını yükler"""
        kayitlar = self.db.get_bekleyen_servis_kayitlari()
        self.table.setRowCount(len(kayitlar))
        
        for row, kayit in enumerate(kayitlar):
            for col, value in enumerate(kayit):
                item = QTableWidgetItem(str(value))
                if col == 7:  # Tutar sütunu
                    item.setText(f"{float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                self.table.setItem(row, col, item)
        
        self.alt_label.setText(f"{len(kayitlar)} adet kayıt listeleniyor")

    def kayit_onayla(self):
        """Seçili kaydı onaylar"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        kayit_id = int(self.table.item(row, 0).text())
        if self.db.update_servis_kayit_onay(kayit_id, 'ONAYLANDI'):
            QMessageBox.information(self, 'Başarılı', 'Kayıt başarıyla onaylandı!')
            self.load_data()
        else:
            QMessageBox.warning(self, 'Hata', 'Kayıt onaylanırken bir hata oluştu!')

    def kayit_reddet(self):
        """Seçili kaydı reddeder"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        kayit_id = int(self.table.item(row, 0).text())
        if self.db.update_servis_kayit_onay(kayit_id, 'REDDEDILDI'):
            QMessageBox.information(self, 'Başarılı', 'Kayıt başarıyla reddedildi!')
            self.load_data()
        else:
            QMessageBox.warning(self, 'Hata', 'Kayıt reddedilirken bir hata oluştu!')

    def show_detay(self):
        """Seçili kaydın detaylarını gösterir"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Uyarı', 'Lütfen bir kayıt seçin!')
            return
        
        kayit_id = int(self.table.item(row, 0).text())
        # KayitDetayDialog'u aç
        dialog = KayitDetayDialog(self, kayit_id=kayit_id)
        dialog.exec_()

    def filtrele(self):
        """Kayıtları filtreler"""
        # Filtreleme işlevi eklenecek
        pass

    def temizle(self):
        """Filtreleri temizler"""
        self.filtre_edit.clear()
        self.tarih1.setDate(QDate.currentDate())
        self.tarih2.setDate(QDate.currentDate())
        self.load_data()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 