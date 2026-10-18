# {{CLIENT_NAME}}: fakta dan klaim

Dibaca oleh setiap tahap NEXUS. Kalau isinya bertentangan dengan context profile, file ini yang menang. Yang tidak tertulis di sini, di context profile, atau di kolom "Penawaran & klaim yang boleh" pada sheet tidak diklaim di artikel.

Terakhir diperbarui: {{DATE}}

<!-- Isi setiap baris bertanda TODO. Baris yang dibiarkan kosong dilewati: tahap NEXUS memakai default-nya sendiri atau bertanya. Jangan tulis kata sandi atau token di file ini. -->

## Defaults

Dipakai untuk input yang tidak diberikan user atau baris sheet.

- Domain: {{DOMAIN}}
- Inisial brand: {{INITIALS}}
- Bahasa utama: {{LANG}}
- Voice: brand ("kami" di ID, "we" di EN). Ganti ke third-party kalau artikel terbit di situs pihak lain.
- FAQ delivery: {{FAQ_DELIVERY}}
- Context profile: {{CONTEXT_PROFILE}}
- CTA artikel ID: {{CTA_ID}}
- CTA artikel EN: {{CTA_EN}}
- Label tombol: {{CTA_LABEL}}
- Penulis: {{AUTHOR}}
- Kategori blog: {{BLOG_CATEGORY}}
- Artikel ID menautkan halaman bahasa Indonesia, artikel EN menautkan halaman bahasa Inggris.

### Google Drive (diisi /setup atau saat ekspor pertama)

- Folder Drive: {{DRIVE_FOLDER}}
- Folder Drive outline: {{DRIVE_FOLDER_OUTLINE}}
- Folder Drive article: {{DRIVE_FOLDER_ARTICLE}}
- Queue sheet: {{QUEUE_SHEET}}

<!-- ID folder Google Drive. Folder utama bernama brand klien, berisi subfolder Outline dan Article. Nama Doc: INISIAL-OL-KODE (outline) dan INISIAL-AR-KODE (artikel), -v2 dan seterusnya untuk revisi. Queue sheet: ID Google Sheet antrean brand ini (INISIAL-QUEUE Brand), di folder utama. -->

### WordPress (opsional, untuk status `approved` di queue)

- WordPress: {{WP_SITE}}
- WordPress auth env: {{WP_AUTH_ENV}}
- FAQ ACF field: {{FAQ_ACF}}

<!-- WordPress: URL situs WordPress (bisa berbeda dari Domain, misalnya https://example.com/blog).
WordPress auth env: nama environment variable yang berisi base64 dari "username:application password". Satu variabel per situs, misalnya WP_ACME_AUTH. Isinya diset sendiri oleh user, tidak pernah ditulis di sini.
FAQ ACF field: isi hanya kalau FAQ metabox situs adalah ACF repeater yang "Show in REST API"-nya aktif, dengan format: nama_field (sub_field_pertanyaan, sub_field_jawaban). Kosong = FAQ di-paste manual. -->

## Layanan dan prioritas CTA

Link komersial dan CTA diarahkan ke layanan ini, urut dari prioritas tertinggi. Hanya halaman yang benar-benar ada di situs.

| Layanan | URL EN | URL ID | Catatan |
|---|---|---|---|
| TODO | | | |

## Tim (untuk byline, reviewer, dan schema)

- TODO: nama, jabatan, link profil publik. Tulis siapa yang boleh disebut dan siapa yang tidak.

## Tidak boleh

- TODO: misalnya harga, janji hasil, nama klien tanpa izin, menjelekkan kompetitor tertentu, data internal.

## Studi kasus dan bukti yang boleh dipakai

- TODO: hanya yang sudah disetujui klien. Tulis apa yang boleh disebut (nama, angka, periode) dan apa yang tidak.
