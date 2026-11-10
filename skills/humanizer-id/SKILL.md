---
name: humanizer-id
description: Use when writing or finalizing Bahasa Indonesia article content (NEX-F, NEX-Fn, or /humanize). NEXUS wrapper (Layer 0 SQEG, register, brand voice, self-check) around the humanizer-indonesia pattern catalog, so output reads like a competent human writer, not AI, while preserving E-E-A-T signals.
---

# Humanizer Bahasa Indonesia (NEXUS)
Versi 3.0 | Katalog pola: adhiprib/humanizer-indonesia v1.7 (MIT), lihat `UPSTREAM.md`

## Tujuan

Filter humanizer untuk semua artikel Bahasa Indonesia. Terapkan ke setiap teks yang kamu tulis atau rewrite. Jangan umumkan proses ini ke user. Jalankan diam-diam sebelum output dikirim.

Tujuannya: tulisan yang terdengar seperti manusia yang kompeten, bukan AI, sambil memenuhi standar Google Page Quality (E-E-A-T, MC Quality, Needs Met).

NEXUS memegang Layer 0, register, dan self-check. Katalog pola AI (Layer 2) berasal dari upstream dan dibaca dari `references/`.

## Cara Menjalankan

1. **Layer 0 dulu**: lindungi elemen SQEG-critical sebelum menyentuh apapun
2. **Layer 1**: tentukan register (formal / semi-formal / kasual)
3. **Layer 2**: scan dan perbaiki pola AI dengan katalog upstream (lihat bagian Layer 2)
4. **Self-check**: jalankan checklist sebelum kirim output
5. **Output saja**: kirim teks hasil rewrite tanpa preamble, tanpa changelog

**Urutan prioritas bila bentrok:** fakta terverifikasi dan CTA dari `/convert` > Layer 0 SQEG > suara brand (jika ada) > Layer 2 pola AI. Suara brand mengalahkan pola Layer 2, tidak pernah Layer 0.

---
## LAYER 0: PROTEKSI SQEG (Non-Negotiable)

Enam aturan ini tidak bisa dilanggar oleh apapun di Layer 2.

---

### G1. Format Hyperlink Sesuai Medium Output

Format hyperlink HARUS disesuaikan dengan medium output konten.
Salah format menyebabkan URL muncul mentah di dalam tanda kurung — terlihat tidak profesional.

**Deteksi medium output sebelum menulis link:**

| Medium | Format yang benar | Contoh |
|---|---|---|
| Website / blog / CMS | Markdown anchor text | `[teks anchor](url)` |
| Caption Instagram / Facebook | Teks biasa + CTA terpisah | `Klik link di bio untuk konsultasi.` |
| WhatsApp / Telegram | URL langsung tanpa markdown | `Hubungi kami: example.com/kontak` |
| Email (plain text) | URL langsung | `example.com/kontak` |
| Email (HTML/rich text) | Anchor text hyperlink | `<a href="url">teks anchor</a>` |
| Dokumen Word / PDF | Teks anchor + URL dalam kurung | `Panduan ini (example.com/panduan)` |

**Aturan universal — berlaku di semua medium:**
- JANGAN gabungkan teks anchor dengan URL dalam satu kalimat kecuali format dokumen
- JANGAN tulis `teks anchor (url)` — ini format yang menyebabkan URL keliatan di luar
- JANGAN gunakan bare URL sebagai anchor text untuk konten website
- Kalau medium tidak jelas dari konteks, tanya user SEBELUM menulis link

❌ Salah (semua medium): "Klik di sini untuk mengobrol dengan kami (example.com/kontak)"
❌ Salah (semua medium): "Baca selengkapnya di https://example.com/panduan-relay"
✅ Benar (website): "[Jadwalkan konsultasi](example.com/kontak) untuk membahas kebutuhan Anda."
✅ Benar (Instagram caption): "Butuh rincian layanan? Klik link di bio."
✅ Benar (WhatsApp): "Hubungi tim kami di example.com/kontak"

---

### G2. Pertahankan Format List untuk Konten Prosedural dan Spesifikasi

JANGAN konversi ke prosa: how-to steps, spesifikasi teknis, checklist, FAQ, perbandingan produk.
Untuk format ini: hapus bold label AI-style, tapi pertahankan struktur list.
Konversi ke prosa HANYA bagian narasi dan argumen.

❌ Jangan konversi langkah prosedural:
"- **Langkah 1:** Matikan daya utama
- **Langkah 2:** Pasang MCB ke DIN rail"

✅ Benar — hapus bold, pertahankan list:
"1. Matikan daya utama sebelum menyentuh panel
2. Pasang MCB ke DIN rail dengan tekanan merata"

---

### G3. Pertahankan Caveat YMYL

Topik YMYL di konteks Indonesia: kesehatan/nutrisi, instalasi listrik, investasi/keuangan,
kepatuhan regulasi (OJK/BPOM/Kemenkeu), keselamatan kerja.

Pertahankan kalimat ini (jangan dihapus sebagai filler):
- "Konsultasikan dengan teknisi listrik bersertifikat sebelum instalasi."
- "Matikan MCB utama sebelum melanjutkan."
- "Hasil dapat berbeda tergantung kondisi jaringan lokal."

Tetap hapus: "per pengetahuan penulis", "data dapat berubah sewaktu-waktu",
"berdasarkan informasi yang tersedia saat ini".

---

### G4. Heading Harus Spesifik dan Deskriptif

Semua H2/H3 harus cukup spesifik untuk berdiri sendiri sebagai pernyataan informatif.

❌ Generik: "Manfaat Relay Phoenix Contact"
✅ Spesifik: "Relay Phoenix Contact vs Omron: perbandingan waktu respons dan umur pakai"

Gunakan huruf kapital hanya di kata pertama dan nama diri. Tidak ada Title Case Semua Kata.

---

### G5. Pertahankan Pengalaman Langsung dan Observasi Lapangan

Jangan hapus anekdot atau bukti berbasis pengalaman. Ini adalah sinyal E-E-A-T Experience.

❌ Hapus (samar): "Banyak perusahaan besar berhasil menerapkan strategi ini."
✅ Pertahankan (pengalaman spesifik): "Dari pengalaman instalasi di tiga pabrik Bekasi,
konfigurasi ini konsisten lebih stabil dibanding setup default pabrikan."

---

### G6. Ganti Transisi yang Dihapus — Jangan Hapus Begitu Saja

Saat kamu menghapus frasa transisi AI (Pola 29), ganti dengan koneksi logis yang spesifik.
Artikel tanpa jembatan logis terasa choppy dan menurunkan persepsi kualitas di mata Google rater.

❌ Hapus phrasing generik: "Setelah memahami cara kerja relay, kini saatnya membahas spesifikasi."
✅ Ganti dengan koneksi spesifik: "Pemilihan spesifikasi langsung bergantung pada karakteristik
beban tadi — terutama nilai arus puncak saat motor pertama dinyalakan."

---

## LAYER 1: TENTUKAN REGISTER

Tentukan sebelum menjalankan pola apapun, dan konsisten sampai akhir.

- **Formal**: pakai "Anda", kalimat baku → artikel berita, B2B, dokumen teknis
- **Semi-formal**: "Anda" atau "kamu" (pilih satu, konsisten) → blog profesional, LinkedIn
- **Kasual**: "kamu" atau "lo/gue" sesuai konteks → blog lifestyle, media sosial

---

---

## LAYER 2: POLA AI (katalog upstream)

Baca `references/id-ai-tells.md` (katalog pola, false positive, dan register yang dikecualikan) lalu `references/upstream-skill.md` (alur kerja dan aturan upstream). Terapkan keduanya dengan penyesuaian NEXUS berikut:

- **Abaikan** di upstream: instruksi memuat `voice-prib-id.md` (preset suara penulis lain, tidak disertakan), pertanyaan interaktif ke user, dan keluaran laporan atau changelog. Pipeline NEXUS tidak boleh berhenti bertanya dan hanya mengirim teks hasil.
- Suara: pakai brand voice klien bila ada di konteks. Tanpa itu, ikuti register dari Layer 1.
- **Metrik (opsional, `/finaldraft`):** `python scripts/metrik.py <file.md> --preset semiformal` (preset: `akademik`, `ajar`, `semiformal`) hanya sebagai sinyal. Jangan mengubah teks demi angka.
- Jangan terapkan pola ke kode, JSON, tabel data, atau blok CTA hasil `/convert`.

---

## SELF-CHECK (Jalankan sebelum setiap output)

**Layer 0 — SQEG:**
1. Semua internal link punya anchor text deskriptif? Tidak ada naked URL?
2. List prosedural/spesifikasi/checklist sudah dipertahankan strukturnya?
3. Konten YMYL masih punya appropriate caveats?
4. Semua heading spesifik dan deskriptif? Bukan Title Case?
5. Transisi yang dihapus sudah diganti dengan koneksi spesifik?

**Layer 2 (pola AI):**
6. Semua pola di `references/id-ai-tells.md` sudah dipindai, dengan false positive dikecualikan?
7. Setiap pembuka paragraf berbeda dan panjang paragraf bervariasi?
8. Ada penutup generik atau atribusi samar yang tersisa?
9. Ada konteks lokal Indonesia yang relevan tapi belum masuk?
10. Ada em dash atau en dash yang bukan untuk rentang angka?
11. Dibaca keras, terasa seperti tulisan orang Indonesia sungguhan?

---

## Saat User Bilang "Humanize" atau "Biar Ga Kelihatan AI"

1. Tentukan register yang sesuai konteks konten
2. Jalankan Layer 0, tandai semua elemen yang dilindungi SQEG
3. Scan Layer 2 dengan katalog upstream
4. Pertahankan makna asli: ubah CARA penyampaiannya, bukan ISI-nya
5. Jalankan self-check 11 poin
6. Output hanya teks hasil rewrite, tanpa preamble dan tanpa penjelasan perubahan
