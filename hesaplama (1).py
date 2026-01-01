import tkinter as tk
from tkinter import messagebox
from decimal import Decimal, InvalidOperation, getcontext

# Decimal hassasiyet ayarı (Finansal hesaplamalar için doğruluk sağlar)
getcontext().prec = 20

# --------------------------------------------------------
# I. VERİ DEPOLAMA VE GENEL FONKSİYONLAR
# --------------------------------------------------------

# --- Modül Veri Listeleri ---
entry_urun_isimleri_fiyat = []
entry_urun_fiyatlari_fiyat = []
entry_urun_adetleri_fiyat = []
urun_sayisi_fiyat = 0

entry_urun_isimleri_adet = []
entry_urun_fiyatlari_adet = []
entry_urun_satis_fiyatlari_adet = []
urun_sayisi_adet = 0

entry_urun_isimleri_hedef_para = []
entry_urun_fiyatlari_hedef_para = []
entry_urun_satis_fiyatlari_hedef_para = []
entry_urun_adetleri_hedef_para = []
urun_sayisi_hedef_para = 0

entry_urun_isimleri_ana_para = []
entry_urun_fiyatlari_ana_para = []
entry_urun_satis_fiyatlari_ana_para = []
entry_urun_adetleri_ana_para = []
urun_sayisi_ana_para = 0

# MODÜL 5 LİSTELERİ
entry_urun_isimleri_strateji_yeni = []
entry_urun_alis_fiyatlari_strateji_yeni = []
entry_urun_satis_fiyatlari_strateji_yeni = []
urun_sayisi_strateji_yeni = 0

def show_frame(frame):
    """Verilen Frame'i pencerede gösterir ve diğerlerini gizler."""
    frame.tkraise()

def clear_on_click(event):
    """Entry alanına tıklandığında, varsayılan değeri (0, 0.00 veya varsayılan isim) siler."""
    current_text = event.widget.get()
    # Varsayılan değerler ve örnek isimler için kontrol (Tüm fiyat ve isim varsayılanlarını kapsar)
    if current_text in ("0", "0.00", "1.00", "50.00", "10.00", "15.00", "1000.00", "1500.00", "2000.00", "5000.00", "50000.00", 
                        "Ürün Adı", "Ürün 1", "Ürün 2", "Ürün 3", "Ürün 4", "Ürün 5", "Ürün 6", "Ürün 7", "Ürün 8", "Ürün 9", "Ürün 10", "1"):
        event.widget.delete(0, tk.END)
    event.widget.focus_set()

def setup_entry(parent, default_value, width, row, column, entries_list=None):
    """Yeni bir Entry oluşturur, varsayılan değer ekler ve tıklama olayını bağlar."""
    entry = tk.Entry(parent, width=width)
    entry.grid(row=row, column=column, padx=5, pady=5, sticky="w")
    entry.insert(0, default_value)
    # Tıklama olayını bağla
    entry.bind("<Button-1>", clear_on_click) 
    
    if entries_list is not None:
        entries_list.append(entry)
    return entry

# --------------------------------------------------------
# II. HESAPLAMA MANTIKLARI (Tüm Modüller)
# --------------------------------------------------------

## Modül 1: Satış Fiyatı Hesaplama
def hesapla_satis_fiyati():
    try:
        ana_para = Decimal(entry_ana_para_fiyat.get() or "0.00")
        hedef_fiyat = Decimal(entry_hedef_fiyat_fiyat.get() or "0.00")
        urun_fiyatlari = [Decimal(entry.get() or "0.00") for entry in entry_urun_fiyatlari_fiyat]
        urun_adetleri = [Decimal(entry.get() or "0") for entry in entry_urun_adetleri_fiyat]
        
        if not urun_fiyatlari:
             messagebox.showerror("Hata", "Lütfen en az bir ürün bilgisi girin.")
             return
        
        toplam_maliyet = sum(fiyat * adet for fiyat, adet in zip(urun_fiyatlari, urun_adetleri))
        toplam_urun_adeti = sum(urun_adetleri)
        
        if toplam_urun_adeti <= 0:
            messagebox.showerror("Hata", "Toplam ürün adedi sıfır veya negatif olamaz.")
            return

        gerekli_toplam_satis = hedef_fiyat - ana_para
        birim_satis_fiyati = (gerekli_toplam_satis + toplam_maliyet) / toplam_urun_adeti
        
        sonuc_mesaji = (
            f"Toplam Harcama (Ürün Maliyeti): {toplam_maliyet:,.2f} TL\n"
            f"Toplam Ürün Adedi: {toplam_urun_adeti:,.0f}\n"
            f"Hedef Fiyata Ulaşmak İçin Gerekli Toplam Satış Hasılatı: {gerekli_toplam_satis + toplam_maliyet:,.2f} TL\n\n"
            f"**Bir Ürünün Satılması Gereken Minimum Fiyat:** {birim_satis_fiyati:,.2f} TL"
        )
        label_sonuc_fiyat.config(text=sonuc_mesaji)

    except InvalidOperation:
        messagebox.showerror("Hata", "Lütfen tüm alanlara geçerli sayısal değerler girin.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu: {e}")

## Modül 2: Ürün Adedi Hesaplama
def hesapla_adet():
    try:
        ana_para = Decimal(entry_ana_para_adet.get() or "0.00")
        hedef_fiyat = Decimal(entry_hedef_fiyat_adet.get() or "0.00")
        
        urun_isimleri = [entry.get() for entry in entry_urun_isimleri_adet]
        urun_fiyatlari = [Decimal(entry.get() or "0.00") for entry in entry_urun_fiyatlari_adet]
        urun_satis_fiyatlari = [Decimal(entry.get() or "0.00") for entry in entry_urun_satis_fiyatlari_adet]
        
        if len(urun_fiyatlari) == 0:
            messagebox.showerror("Hata", "Lütfen en az bir ürün ekleyin.")
            return

        gerekli_net_satis_miktari = hedef_fiyat - ana_para
        
        if gerekli_net_satis_miktari <= 0:
            messagebox.showwarning("Uyarı", "Hedef Fiyat Ana Paradan düşük veya eşit.")
            return

        profitable_products = []
        for isim, maliyet, satis in zip(urun_isimleri, urun_fiyatlari, urun_satis_fiyatlari):
            kar_marji = satis - maliyet
            if kar_marji > 0:
                profitable_products.append({'isim': isim, 'kar': kar_marji})
            
        if not profitable_products:
             messagebox.showerror("Hata", "Tüm ürünlerin satış fiyatı maliyetten yüksek olmalıdır.")
             return
             
        esit_pay = gerekli_net_satis_miktari / len(profitable_products)
        toplam_kontrol = Decimal('0')
        
        sonuc_mesaji = f"**Gerekli Toplam Net Kâr:** {gerekli_net_satis_miktari:,.2f} TL\n"
        sonuc_mesaji += f"**Kâr Dağılımı:** {len(profitable_products)} ürüne eşit pay ({esit_pay:,.2f} TL/ürün)\n\n"
        sonuc_mesaji += "**Hedefe Ulaşmak İçin Gereken Tahmini Ürün Adetleri:**\n"

        for product in profitable_products:
            urun_kar = product['kar']
            gerekli_adet = esit_pay / urun_kar
            gerekli_adet = gerekli_adet.to_integral_value(rounding='ROUND_CEILING')
            toplam_kontrol += gerekli_adet * urun_kar
            sonuc_mesaji += f"- {product['isim']}: {gerekli_adet:,.0f} adet\n"

        sonuc_mesaji += f"\n**Elde Edilecek Tahmini Net Satış (Kontrol):** {toplam_kontrol:,.2f} TL"

        label_sonuc_adet.config(text=sonuc_mesaji)

    except InvalidOperation:
        messagebox.showerror("Hata", "Lütfen tüm alanlara geçerli sayısal değerler girin.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu: {e}")

## Modül 3: Nihai Para Hesaplama
def hesapla_hedef_para():
    try:
        ana_para = Decimal(entry_ana_para_hedef_para.get() or "0.00")
        
        urun_fiyatlari = [Decimal(entry.get() or "0.00") for entry in entry_urun_fiyatlari_hedef_para]
        urun_satis_fiyatlari = [Decimal(entry.get() or "0.00") for entry in entry_urun_satis_fiyatlari_hedef_para]
        urun_adetleri = [Decimal(entry.get() or "0") for entry in entry_urun_adetleri_hedef_para]
        
        if not urun_fiyatlari:
             messagebox.showerror("Hata", "Lütfen en az bir ürün bilgisi girin.")
             return

        toplam_alis_maliyeti = sum(maliyet * adet for maliyet, adet in zip(urun_fiyatlari, urun_adetleri))
        toplam_satis_hasılatı = sum(satis * adet for satis, adet in zip(urun_satis_fiyatlari, urun_adetleri))
            
        nihai_bakiye = ana_para + toplam_satis_hasılatı - toplam_alis_maliyeti
        net_kar = toplam_satis_hasılatı - toplam_alis_maliyeti

        sonuc_mesaji = (
            f"Toplam Alış Maliyeti: {toplam_alis_maliyeti:,.2f} TL\n"
            f"Toplam Satış Hasılatı: {toplam_satis_hasılatı:,.2f} TL\n"
            f"Net Kâr (Hasılat - Maliyet): {net_kar:,.2f} TL\n\n"
            f"**Nihai Hesap Bakiyesi (Hedeflenen Toplam Para):** {nihai_bakiye:,.2f} TL"
        )
        label_sonuc_hedef_para.config(text=sonuc_mesaji)

    except InvalidOperation:
        messagebox.showerror("Hata", "Lütfen tüm alanlara geçerli sayısal değerler girin.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu: {e}")

## Modül 4: Gerekli Ana Para Hesaplama
def hesapla_ana_para():
    try:
        hedef_fiyat = Decimal(entry_hedef_fiyat_ana_para.get() or "0.00")
        
        urun_fiyatlari = [Decimal(entry.get() or "0.00") for entry in entry_urun_fiyatlari_ana_para]
        urun_satis_fiyatlari = [Decimal(entry.get() or "0.00") for entry in entry_urun_satis_fiyatlari_ana_para]
        urun_adetleri = [Decimal(entry.get() or "0") for entry in entry_urun_adetleri_ana_para]
        
        if not urun_fiyatlari:
             messagebox.showerror("Hata", "Lütfen en az bir ürün bilgisi girin.")
             return

        toplam_alis_maliyeti = sum(maliyet * adet for maliyet, adet in zip(urun_fiyatlari, urun_adetleri))
        toplam_satis_hasılatı = sum(satis * adet for satis, adet in zip(urun_satis_fiyatlari, urun_adetleri))
            
        net_kar = toplam_satis_hasılatı - toplam_alis_maliyeti
        gerekli_ana_para = hedef_fiyat - net_kar

        sonuc_mesaji = (
            f"Hedef Fiyat: {hedef_fiyat:,.2f} TL\n"
            f"Toplam Alış Maliyeti: {toplam_alis_maliyeti:,.2f} TL\n"
            f"Toplam Satış Hasılatı: {toplam_satis_hasılatı:,.2f} TL\n"
            f"Net Kâr (Hasılat - Maliyet): {net_kar:,.2f} TL\n\n"
            f"**Hedefe Ulaşmak İçin Gerekli Başlangıç Ana Parası:** {gerekli_ana_para:,.2f} TL"
        )
        label_sonuc_ana_para.config(text=sonuc_mesaji)

    except InvalidOperation:
        messagebox.showerror("Hata", "Lütfen tüm alanlara geçerli sayısal değerler girin.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu: {e}")

## Modül 5: Bileşik Kâr Stratejisi (Çoklu Ürün)
def hesapla_strateji_yeni():
    try:
        baslangic_ana_para = Decimal(entry_baslangic_ana_para_strateji_yeni.get() or "0.00")
        hedef_toplam_para = Decimal(entry_hedef_toplam_para_strateji_yeni.get() or "0.00")
        
        # --- 1. Geçerli ve Kârlı Ürünleri Filtreleme ---
        gecerli_urunler = []
        toplam_alis_fiyati_gecerli = Decimal('0')
        
        num_entries = len(entry_urun_alis_fiyatlari_strateji_yeni)
        
        for i in range(num_entries):
            
            alis_entry = entry_urun_alis_fiyatlari_strateji_yeni[i]
            satis_entry = entry_urun_satis_fiyatlari_strateji_yeni[i]
            isim_entry = entry_urun_isimleri_strateji_yeni[i]
            
            try:
                alis = Decimal(alis_entry.get() or "0.00") 
                satis = Decimal(satis_entry.get() or "0.00")
            except InvalidOperation:
                continue 

            if alis <= 0:
                continue 
            
            kar_marji = satis - alis
            if kar_marji <= 0:
                continue
            
            urun_bilgisi = {
                'isim': isim_entry.get() or f"Ürün {i+1}",
                'alis': alis,
                'kar': kar_marji,
                'oran': kar_marji / alis
            }
            gecerli_urunler.append(urun_bilgisi)
            toplam_alis_fiyati_gecerli += alis

        if not gecerli_urunler:
            messagebox.showerror("Hata", "Lütfen geçerli (Alış > 0 ve Satış > Alış) fiyatlara sahip en az bir ürün girin.")
            return

        # --- 2. Hedef Kontrolü ve Başlangıç Ayarları ---
        gerekli_net_kar = hedef_toplam_para - baslangic_ana_para
        if gerekli_net_kar <= 0:
            messagebox.showwarning("Uyarı", "Hedeflenen Toplam Para, Ana Paradan yüksek olmalıdır!")
            return

        guncel_bakiye = baslangic_ana_para
        sefer_sayisi = 0
        max_sefer_limit = 100
        
        sonuc_listesi = f"🚀 Başlangıç Ana Para: **{baslangic_ana_para:,.2f} TL**\n"
        sonuc_listesi += f"🎯 Hedef Toplam Para: **{hedef_toplam_para:,.2f} TL** (Gerekli Kâr: {gerekli_net_kar:,.2f} TL)\n"
        sonuc_listesi += f"💡 Strateji: Mevcut bakiye, **tüm kârlı ürünlerin alış fiyatlarına orantılı olarak** dağıtılacaktır.\n"
        
        # --- 3. Iteratif Hesaplama Döngüsü (Çoklu Ürün) ---
        while guncel_bakiye < hedef_toplam_para and sefer_sayisi < max_sefer_limit:
            sefer_sayisi += 1
            
            toplam_sefer_alis_maliyeti = Decimal('0')
            toplam_sefer_net_kar = Decimal('0')
            
            sefer_detayi = f"\n📈 {sefer_sayisi}. SEFER BİLGİLERİ \n"
            sefer_detayi += f"  - Başlangıç Bakiye: {guncel_bakiye:,.2f} TL\n"
            
            # Her ürüne ayrılan sermaye payını hesapla
            for urun in gecerli_urunler:
                # Sermaye Payı = (Ürün Alış Fiyatı / Tüm Ürünlerin Toplam Alış Fiyatı) * Mevcut Bakiye
                pay_oran = urun['alis'] / toplam_alis_fiyati_gecerli
                ayrilan_sermaye = guncel_bakiye * pay_oran
                
                # Bu sermaye ile kaç adet alınır?
                alinabilecek_adet = ayrilan_sermaye / urun['alis']
                alinacak_adet = alinabilecek_adet.to_integral_value(rounding='ROUND_FLOOR')
                
                if alinacak_adet > 0:
                    alis_maliyeti = alinacak_adet * urun['alis']
                    net_kar = alinacak_adet * urun['kar']
                    
                    toplam_sefer_alis_maliyeti += alis_maliyeti
                    toplam_sefer_net_kar += net_kar
                    
                    sefer_detayi += f"  - {urun['isim']} Adet: **{alinacak_adet:,.0f}** (Kâr: {net_kar:,.2f} TL)\n"
            
            # Genel Kontrol ve Bakiye Güncelleme
            if toplam_sefer_alis_maliyeti == 0:
                 sonuc_listesi += f"\n[DURDURULDU] {sefer_sayisi}. Seferde hiçbir üründen alım yapılamadı (Sermaye yetersiz)."
                 break

            guncel_bakiye += toplam_sefer_net_kar
            
            sefer_detayi += f"  - Toplam Alış Maliyeti: {toplam_sefer_alis_maliyeti:,.2f} TL\n"
            sefer_detayi += f"  - Toplam Net Kazanç: {toplam_sefer_net_kar:,.2f} TL\n"
            sefer_detayi += f"  - **Nihai Bakiye:** {guncel_bakiye:,.2f} TL\n"
            
            sonuc_listesi += sefer_detayi
            
        # --- 4. Final Sonuçlandırma ---
        if guncel_bakiye >= hedef_toplam_para:
            sonuc_listesi += f"\n🎉 **TEBRİKLER!** Hedeflenen {hedef_toplam_para:,.2f} TL'ye **{sefer_sayisi}** seferde ulaşıldı."
        elif sefer_sayisi == max_sefer_limit:
             sonuc_listesi += f"\n[UYARI] {max_sefer_limit} Sefer Sınırına ulaşıldı. Hedef tamamlanamadı."

        label_sonuc_strateji_yeni.config(text=sonuc_listesi, justify=tk.LEFT, fg="darkgreen")
        
        frame_scrolled_content_strateji_yeni.update_idletasks()
        canvas_strateji_yeni.config(scrollregion=canvas_strateji_yeni.bbox("all"))

    except InvalidOperation:
        messagebox.showerror("Hata", "Lütfen tüm alanlara geçerli sayısal değerler girin.")
    except Exception as e:
        messagebox.showerror("Hata", f"Beklenmedik bir hata oluştu: {e}")

# --------------------------------------------------------
# III. ARAYÜZ OLUŞTURMA FONKSİYONLARI (ÜRÜN EKLEME)
# --------------------------------------------------------

## Modül 1 Ürün Ekleme
def urun_ekle_fiyat():
    global urun_sayisi_fiyat
    urun_sayisi_fiyat += 1
    row_num = urun_sayisi_fiyat + 1
    setup_entry(frame_urunler_fiyat, "Ürün Adı", 15, row_num, 0, entry_urun_isimleri_fiyat)
    setup_entry(frame_urunler_fiyat, "0.00", 10, row_num, 2, entry_urun_fiyatlari_fiyat)
    setup_entry(frame_urunler_fiyat, "1", 5, row_num, 4, entry_urun_adetleri_fiyat)
    tk.Label(frame_urunler_fiyat, text="TL").grid(row=row_num, column=3, padx=0)
    tk.Label(frame_urunler_fiyat, text="adet").grid(row=row_num, column=5, padx=0)

## Modül 2 Ürün Ekleme
def urun_ekle_adet():
    global urun_sayisi_adet
    urun_sayisi_adet += 1
    row_num = urun_sayisi_adet + 1
    setup_entry(frame_urunler_adet, f"Ürün {urun_sayisi_adet}", 15, row_num, 0, entry_urun_isimleri_adet)
    setup_entry(frame_urunler_adet, "10.00", 10, row_num, 2, entry_urun_fiyatlari_adet)
    setup_entry(frame_urunler_adet, "15.00", 10, row_num, 4, entry_urun_satis_fiyatlari_adet)
    tk.Label(frame_urunler_adet, text="Alış (TL)").grid(row=row_num, column=1, padx=0)
    tk.Label(frame_urunler_adet, text="Satış (TL)").grid(row=row_num, column=3, padx=0)

## Modül 3 Ürün Ekleme
def urun_ekle_hedef_para():
    global urun_sayisi_hedef_para
    urun_sayisi_hedef_para += 1
    row_num = urun_sayisi_hedef_para + 1
    setup_entry(frame_urunler_hedef_para, f"Ürün {urun_sayisi_hedef_para}", 15, row_num, 0, entry_urun_isimleri_hedef_para)
    setup_entry(frame_urunler_hedef_para, "10.00", 10, row_num, 2, entry_urun_fiyatlari_hedef_para)
    setup_entry(frame_urunler_hedef_para, "15.00", 10, row_num, 4, entry_urun_satis_fiyatlari_hedef_para)
    setup_entry(frame_urunler_hedef_para, "1", 5, row_num, 6, entry_urun_adetleri_hedef_para)
    tk.Label(frame_urunler_hedef_para, text="Alış (TL)").grid(row=row_num, column=1, padx=0)
    tk.Label(frame_urunler_hedef_para, text="Satış (TL)").grid(row=row_num, column=3, padx=0)
    tk.Label(frame_urunler_hedef_para, text="Adet").grid(row=row_num, column=5, padx=0)

## Modül 4 Ürün Ekleme
def urun_ekle_ana_para():
    global urun_sayisi_ana_para
    urun_sayisi_ana_para += 1
    row_num = urun_sayisi_ana_para + 1
    setup_entry(frame_urunler_ana_para, f"Ürün {urun_sayisi_ana_para}", 15, row_num, 0, entry_urun_isimleri_ana_para)
    setup_entry(frame_urunler_ana_para, "10.00", 10, row_num, 2, entry_urun_fiyatlari_ana_para)
    setup_entry(frame_urunler_ana_para, "15.00", 10, row_num, 4, entry_urun_satis_fiyatlari_ana_para)
    setup_entry(frame_urunler_ana_para, "1", 5, row_num, 6, entry_urun_adetleri_ana_para)
    tk.Label(frame_urunler_ana_para, text="Alış (TL)").grid(row=row_num, column=1, padx=0)
    tk.Label(frame_urunler_ana_para, text="Satış (TL)").grid(row=row_num, column=3, padx=0)
    tk.Label(frame_urunler_ana_para, text="Adet").grid(row=row_num, column=5, padx=0)

## Modül 5 Ürün Ekleme 
def urun_ekle_strateji_yeni():
    global urun_sayisi_strateji_yeni
    urun_sayisi_strateji_yeni += 1
    row_num = urun_sayisi_strateji_yeni + 1
    
    tk.Label(frame_urunler_strateji_yeni, text=f"Ürün {urun_sayisi_strateji_yeni} Adı:").grid(row=row_num, column=0, padx=5, sticky="e")
    
    # İsim alanı, setup_entry kullanmadığı için manuel bağlamayı koruyoruz.
    urun_isim_entry = tk.Entry(frame_urunler_strateji_yeni, width=15)
    urun_isim_entry.grid(row=row_num, column=1, padx=2) 
    urun_isim_entry.insert(0, f"Ürün {urun_sayisi_strateji_yeni}")
    urun_isim_entry.bind("<Button-1>", clear_on_click) 
    entry_urun_isimleri_strateji_yeni.append(urun_isim_entry) 

    # Fiyat alanları setup_entry kullandığı için otomatik olarak bind edilir.
    setup_entry(frame_urunler_strateji_yeni, "10.00", 10, row_num, 3, entry_urun_alis_fiyatlari_strateji_yeni)
    setup_entry(frame_urunler_strateji_yeni, "15.00", 10, row_num, 5, entry_urun_satis_fiyatlari_strateji_yeni)

    tk.Label(frame_urunler_strateji_yeni, text="Alış Fiyatı (TL):").grid(row=row_num, column=2, padx=5, sticky="e")
    tk.Label(frame_urunler_strateji_yeni, text="Satış Fiyatı (TL):").grid(row=row_num, column=4, padx=5, sticky="e")
    root.update_idletasks()

# --------------------------------------------------------
# IV. ANA PENCERE VE ÇERÇEVELERİ OLUŞTURMA
# --------------------------------------------------------

root = tk.Tk()
root.title("Kâr Hesaplama Uygulaması")

container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)

# Uygulamayı Kapatma Fonksiyonu
def kapat_uygulama():
    root.destroy()
    
def add_close_button(parent_frame):
    """Verilen Frame'e sağ üst köşede kapatma butonu ekler."""
    close_btn = tk.Button(parent_frame, text="❌ Kapat", command=kapat_uygulama, bg="red", fg="white", font=("Arial", 8, "bold"))
    
    # Frame içindeki konumlandırma (Bu sayede her modülde sağ üstte görünür)
    close_btn.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne") 

# --- A. Ana Menü Frame'i ---
frame_menu = tk.Frame(container)
frame_menu.grid(row=0, column=0, sticky="nsew")
add_close_button(frame_menu) # Butonu ekle

tk.Label(frame_menu, text="Hoş Geldiniz! Lütfen Bir Hesaplama Tipi Seçin.", font=("Arial", 12, "bold")).pack(pady=30, padx=20)

tk.Button(frame_menu, text="1. Satış Fiyatı Hesapla", width=30, height=2, command=lambda: show_frame(frame_fiyat)).pack(pady=5)
tk.Button(frame_menu, text="2. Ürün Adedi Hesapla", width=30, height=2, command=lambda: show_frame(frame_adet)).pack(pady=5)
tk.Button(frame_menu, text="3. Nihai Para Hesapla (Toplam Bakiye)", width=30, height=2, command=lambda: show_frame(frame_hedef_para)).pack(pady=5)
tk.Button(frame_menu, text="4. Gerekli Ana Para Hesapla", width=30, height=2, command=lambda: show_frame(frame_ana_para)).pack(pady=5)
tk.Button(frame_menu, text="5. Bileşik Kâr Stratejisi (Çoklu Ürün)", width=30, height=2, command=lambda: show_frame(frame_strateji_yeni)).pack(pady=5)

# --------------------------------------------------------------------------------------------------------------------------------

# --- B. Modül 1: Satış Fiyatı Hesaplama Frame'i ---
frame_fiyat = tk.Frame(container)
frame_fiyat.grid(row=0, column=0, sticky="nsew")
add_close_button(frame_fiyat) # Butonu ekle
tk.Label(frame_fiyat, text="1. Satış Fiyatı Hesaplama Modülü", font=("Arial", 12, "bold")).pack(pady=10)

frame_hedefler_fiyat = tk.LabelFrame(frame_fiyat, text="Hedefler ve Başlangıç"); frame_hedefler_fiyat.pack(padx=10, pady=5, fill="x")
tk.Label(frame_hedefler_fiyat, text="Başlangıç Ana Para (TL):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_ana_para_fiyat = setup_entry(frame_hedefler_fiyat, "1000.00", 15, 0, 1)
tk.Label(frame_hedefler_fiyat, text="Hedef Fiyat (TL):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_hedef_fiyat_fiyat = setup_entry(frame_hedefler_fiyat, "1500.00", 15, 1, 1)

frame_urunler_fiyat = tk.LabelFrame(frame_fiyat, text="Ürün Maliyet ve Adet Bilgileri"); frame_urunler_fiyat.pack(padx=10, pady=5, fill="x")
tk.Button(frame_urunler_fiyat, text="Ürün Ekle", command=urun_ekle_fiyat).grid(row=0, column=0, columnspan=6, pady=5)
urun_ekle_fiyat() 

tk.Button(frame_fiyat, text="HESAPLA", font=("Arial", 10, "bold"), command=hesapla_satis_fiyati).pack(pady=10)

label_sonuc_fiyat = tk.Label(frame_fiyat, text="", justify=tk.LEFT, fg="darkgreen"); label_sonuc_fiyat.pack(padx=10, pady=5)
tk.Button(frame_fiyat, text="Ana Menüye Dön", command=lambda: show_frame(frame_menu)).pack(pady=10)

# --------------------------------------------------------------------------------------------------------------------------------

# --- C. Modül 2: Ürün Adedi Hesaplama Frame'i ---
frame_adet = tk.Frame(container)
frame_adet.grid(row=0, column=0, sticky="nsew")
add_close_button(frame_adet) # Butonu ekle
tk.Label(frame_adet, text="2. Ürün Adedi Hesaplama Modülü", font=("Arial", 12, "bold")).pack(pady=10)

frame_hedefler_adet = tk.LabelFrame(frame_adet, text="Hedefler ve Başlangıç"); frame_hedefler_adet.pack(padx=10, pady=5, fill="x")
tk.Label(frame_hedefler_adet, text="Başlangıç Ana Para (TL):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_ana_para_adet = setup_entry(frame_hedefler_adet, "1000.00", 15, 0, 1)
tk.Label(frame_hedefler_adet, text="Hedef Fiyat (TL):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_hedef_fiyat_adet = setup_entry(frame_hedefler_adet, "2000.00", 15, 1, 1)

frame_urunler_adet = tk.LabelFrame(frame_adet, text="Ürün Fiyat Bilgileri"); frame_urunler_adet.pack(padx=10, pady=5, fill="x")
tk.Button(frame_urunler_adet, text="Ürün Ekle", command=urun_ekle_adet).grid(row=0, column=0, columnspan=4, pady=5)
urun_ekle_adet() 

tk.Button(frame_adet, text="HESAPLA", font=("Arial", 10, "bold"), command=hesapla_adet).pack(pady=10)

label_sonuc_adet = tk.Label(frame_adet, text="", justify=tk.LEFT, fg="darkgreen"); label_sonuc_adet.pack(padx=10, pady=5)
tk.Button(frame_adet, text="Ana Menüye Dön", command=lambda: show_frame(frame_menu)).pack(pady=10)

# --------------------------------------------------------------------------------------------------------------------------------

# --- D. Modül 3: Nihai Para Hesaplama Frame'i ---
frame_hedef_para = tk.Frame(container)
frame_hedef_para.grid(row=0, column=0, sticky="nsew")
add_close_button(frame_hedef_para) # Butonu ekle
tk.Label(frame_hedef_para, text="3. Nihai Para Hesaplama Modülü", font=("Arial", 12, "bold")).pack(pady=10)

frame_hedefler_hedef_para = tk.LabelFrame(frame_hedef_para, text="Başlangıç"); frame_hedefler_hedef_para.pack(padx=10, pady=5, fill="x")
tk.Label(frame_hedefler_hedef_para, text="Başlangıç Ana Para (TL):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_ana_para_hedef_para = setup_entry(frame_hedefler_hedef_para, "1000.00", 15, 0, 1)

frame_urunler_hedef_para = tk.LabelFrame(frame_hedef_para, text="Ürün İşlem Bilgileri"); frame_urunler_hedef_para.pack(padx=10, pady=5, fill="x")
tk.Button(frame_urunler_hedef_para, text="Ürün Ekle", command=urun_ekle_hedef_para).grid(row=0, column=0, columnspan=7, pady=5)
urun_ekle_hedef_para() 

tk.Button(frame_hedef_para, text="HESAPLA", font=("Arial", 10, "bold"), command=hesapla_hedef_para).pack(pady=10)

label_sonuc_hedef_para = tk.Label(frame_hedef_para, text="", justify=tk.LEFT, fg="darkgreen"); label_sonuc_hedef_para.pack(padx=10, pady=5)
tk.Button(frame_hedef_para, text="Ana Menüye Dön", command=lambda: show_frame(frame_menu)).pack(pady=10)

# --------------------------------------------------------------------------------------------------------------------------------

# --- E. Modül 4: Gerekli Ana Para Hesaplama Frame'i ---
frame_ana_para = tk.Frame(container)
frame_ana_para.grid(row=0, column=0, sticky="nsew")
add_close_button(frame_ana_para) # Butonu ekle
tk.Label(frame_ana_para, text="4. Gerekli Ana Para Hesaplama Modülü", font=("Arial", 12, "bold")).pack(pady=10)

frame_hedefler_ana_para = tk.LabelFrame(frame_ana_para, text="Hedef"); frame_hedefler_ana_para.pack(padx=10, pady=5, fill="x")
tk.Label(frame_hedefler_ana_para, text="Hedef Fiyat (TL):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_hedef_fiyat_ana_para = setup_entry(frame_hedefler_ana_para, "2000.00", 15, 0, 1)

frame_urunler_ana_para = tk.LabelFrame(frame_ana_para, text="Ürün İşlem Bilgileri"); frame_urunler_ana_para.pack(padx=10, pady=5, fill="x")
tk.Button(frame_urunler_ana_para, text="Ürün Ekle", command=urun_ekle_ana_para).grid(row=0, column=0, columnspan=7, pady=5)
urun_ekle_ana_para() 

tk.Button(frame_ana_para, text="HESAPLA", font=("Arial", 10, "bold"), command=hesapla_ana_para).pack(pady=10)

label_sonuc_ana_para = tk.Label(frame_ana_para, text="", justify=tk.LEFT, fg="darkgreen"); label_sonuc_ana_para.pack(padx=10, pady=5)
tk.Button(frame_ana_para, text="Ana Menüye Dön", command=lambda: show_frame(frame_menu)).pack(pady=10)

# --------------------------------------------------------------------------------------------------------------------------------

# --- F. Modül 5: Bileşik Kâr Stratejisi (Çoklu Ürün) Frame'i ---
frame_strateji_yeni = tk.Frame(container)
frame_strateji_yeni.grid(row=0, column=0, sticky="nsew")
add_close_button(frame_strateji_yeni) # Butonu ekle
tk.Label(frame_strateji_yeni, text="5. Bileşik Kâr Stratejisi Modülü (Çoklu Ürün Adımlı Büyüme)", font=("Arial", 12, "bold")).pack(pady=10)

frame_hedefler_strateji_yeni = tk.LabelFrame(frame_strateji_yeni, text="Hedefler ve Başlangıç"); frame_hedefler_strateji_yeni.pack(padx=10, pady=5, fill="x")
tk.Label(frame_hedefler_strateji_yeni, text="Başlangıç Ana Para (TL):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_baslangic_ana_para_strateji_yeni = setup_entry(frame_hedefler_strateji_yeni, "5000.00", 15, 0, 1)
tk.Label(frame_hedefler_strateji_yeni, text="Hedef Toplam Para (TL):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_hedef_toplam_para_strateji_yeni = setup_entry(frame_hedefler_strateji_yeni, "50000.00", 15, 1, 1)

frame_urunler_strateji_yeni = tk.LabelFrame(frame_strateji_yeni, text="Ürün Bilgileri (Alış ve Satış Fiyatı)"); frame_urunler_strateji_yeni.pack(padx=10, pady=5, fill="x")
tk.Button(frame_urunler_strateji_yeni, text="Ürün Ekle", command=urun_ekle_strateji_yeni).grid(row=0, column=0, columnspan=6, pady=5)
urun_ekle_strateji_yeni() 

tk.Button(frame_strateji_yeni, text="STRATEJİYİ HESAPLA", font=("Arial", 10, "bold"), command=hesapla_strateji_yeni).pack(pady=10)

# Scrollbar ve Canvas Konteyneri oluşturma
frame_sonuc_container_strateji_yeni = tk.Frame(frame_strateji_yeni)
frame_sonuc_container_strateji_yeni.pack(padx=10, pady=5, fill="both", expand=True)

canvas_strateji_yeni = tk.Canvas(frame_sonuc_container_strateji_yeni, height=200) 
scrollbar_strateji_yeni = tk.Scrollbar(frame_sonuc_container_strateji_yeni, orient="vertical", command=canvas_strateji_yeni.yview)
scrollbar_strateji_yeni.pack(side="right", fill="y")

canvas_strateji_yeni.pack(side="left", fill="both", expand=True)
canvas_strateji_yeni.configure(yscrollcommand=scrollbar_strateji_yeni.set)

frame_scrolled_content_strateji_yeni = tk.Frame(canvas_strateji_yeni)
canvas_strateji_yeni.create_window((0, 0), window=frame_scrolled_content_strateji_yeni, anchor="nw")

label_sonuc_strateji_yeni = tk.Label(frame_scrolled_content_strateji_yeni, text="Adım adım çoklu ürün bileşik kâr stratejisi burada görünecektir.", justify=tk.LEFT, fg="blue", wraplength=450)
label_sonuc_strateji_yeni.pack(padx=5, pady=5, fill="x")

frame_scrolled_content_strateji_yeni.bind(
    "<Configure>",
    lambda e: canvas_strateji_yeni.configure(
        scrollregion=canvas_strateji_yeni.bbox("all")
    )
)

tk.Button(frame_strateji_yeni, text="Ana Menüye Dön", command=lambda: show_frame(frame_menu)).pack(pady=10)

# --------------------------------------------------------------------------------------------------------------------------------

# --- Başlangıçta Ana Menüyü Göster ---
show_frame(frame_menu)

# --- Uygulamayı Çalıştırma ---
root.mainloop()
