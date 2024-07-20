# MasakinProjectBackend




## Tujuan Proyek
Proyek backend aplikasi Masakin ini bertujuan untuk menyediakan platform yang memudahkan pengguna dalam menemukan dan berbagi resep makanan dari berbagai negara. Aplikasi ini akan membantu pengguna mengeksplorasi berbagai masakan internasional, mempelajari teknik memasak baru, dan membagikan pengalaman mereka dengan komunitas global.

## Fitur Utama

| Fitur                | Deskripsi                                                                                                                                                 |
|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Database Resep**    | Menyediakan berbagai resep dari berbagai negara dengan informasi lengkap seperti bahan, langkah-langkah, waktu memasak, dan tingkat kesulitan.           |
| **Pengguna dan Otentikasi** | Menggunakan JWT untuk mengamankan akses pengguna, dengan fitur registrasi, login, dan pengelolaan profil. |
| **Pencarian dan Kategori** | Memungkinkan pengguna untuk mencari resep berdasarkan negara asal, jenis masakan, bahan utama, dan lain-lain. |
| **Favorit dan Ulasan** | Pengguna dapat menyimpan resep favorit dan memberikan ulasan serta rating untuk setiap resep.          |
| **Integrasi API**     | Menyediakan API yang memungkinkan pengembang lain untuk mengakses data resep untuk keperluan integrasi dengan aplikasi lain.                           |

## Teknologi yang Digunakan


| Teknologi           | Deskripsi                                                                                             |
|---------------------|-------------------------------------------------------------------------------------------------------|
| **Framework**       | Flask sebagai framework utama untuk pengembangan backend.                                              |
| **Manajemen Dependensi**       | Poetry sebagai aplikasi utama untuk instalasi dependensi yang akan dipakai backend.                                              |
| **Database**        | PostgreSQL untuk penyimpanan data resep dan pengguna pakai supabase dan dbeaver.                                                   |
| **ORM**             | SQLAlchemy untuk mengelola interaksi dengan database.                                                  |
| **Autentikasi**     | JSON Web Tokens (JWT) untuk mengamankan rute API.                                                      |
| **Penyimpanan Gambar** | Menggunakan layanan penyimpanan cloud dari Supabase untuk database gambar resep, bahan, alat masak, langkah masak. |
| **Docker**          | Untuk containerisasi aplikasi guna memudahkan deployment dan skala.                                    |


## Struktur Proyek
- **Models:** Definisi model database untuk resep, pengguna, dan ulasan.


<div align="center">
   <img width="500" src="/app/documentation/masakinrecipesupdatediagram.png" alt="temporary flow of database">

   <p>Overview of the flow of the database that will be created</p>
</div>
<p>
    <img src="https://img.shields.io/badge/Approved%20on:-%20July%2010,%20 2024-blue?&logo=visual%20studio%20code&logoColor=blue" />
</p>

- **Routes:** Pengaturan rute API untuk berbagai operasi seperti pengelolaan resep, otentikasi pengguna, dan fitur komunitas.
- **Services:** Layanan untuk logika bisnis seperti pencarian resep, pengelolaan favorit/ bookmark.

### Setup and Installation

Untuk menyiapkan proyek secara lokal, ikuti langkah-langkah berikut:

1. Clone repositori.
2. Install dependensi menggunakan Poetry.
3. Menghubungkan ke Supabase PostgreSQL. 
4. Tambahkan flask-migrate.
5. Konfigurasikan variabel lingkungan.
6. Jalankan aplikasi.

#### Konfigurasi Pengaturan Database di File .env:

1. Tambahkan pengaturan database PostgreSQL dari Supabase ke dalam file .env proyekmu:
   ```plaintext
    DB_NAME=your_database_name
    DB_USER=your_user
    DB_PASSWORD=your_password
    DB_HOST=your_host
    DB_PORT=your_port
    DATABASE_URI=postgresql://your_user:your_password@your_host:your_port/your_database_name
   ```
2. Update Konfigurasi Aplikasi
Pastikan aplikasi Flask kamu dikonfigurasi untuk menggunakan URI PostgreSQL yang telah ditentukan di .env. Di file konfigurasi utama aplikasi Flask, pastikan kamu memuat variabel lingkungan dari .env menggunakan python-dotenv:
   ```plaintext
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from dotenv import load_dotenv
    import os

    load_dotenv()  # Memuat variabel lingkungan dari .env

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    db = SQLAlchemy(app)

    # Import models setelah inisialisasi
    from your_application import models

   ```

#### Steps to Run:

1. Pastikan variabel lingkungan Anda dikonfigurasi dengan benar. Contoh `DATABASE_URI` untuk PostgreSql:
   ```plaintext
    DATABASE_URI = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

   ```

2. Install paket yang diperlukan menggunakan "poetry add":
   ```bash
    poetry add flask sqlalchemy psycopg2-binary
   ```

3. Jalankan aplikasi `Flask` Anda:
   ```bash
   poetry run flask --app app run
   ```

Dengan mengikuti langkah-langkah ini, Anda seharusnya dapat terhubung dengan sukses ke database PostgreSQL Anda menggunakan SQLAlchemy dalam aplikasi Flask Anda.

#### Konfigurasi Flask-Migrate dengan Poetry:
1. Install Flask-Migrate
Pertama, pastikan Flask-Migrate terinstal sebagai dependensi proyek. Kamu bisa menambahkannya ke proyek menggunakan Poetry:
   ```bash
    poetry add flask-migrate
   ```
2. Konfigurasi Aplikasi Flask
Pastikan aplikasi Flask kamu dikonfigurasi dengan Flask-Migrate. Di file konfigurasi utama aplikasi Flask kamu, tambahkan kode berikut:
   ```bash
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from dotenv import load_dotenv

    load_dotenv()  # Memuat variabel lingkungan dari .env

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # Import models setelah inisialisasi
    from your_application import models

    #Gantilah postgresql://user:password@localhost/dbname dengan URI database PostgreSQL kamu yang sesuai.
   ```

3. Inisialisasi Flask-Migrate
Untuk memulai menggunakan Flask-Migrate, inisialisasi folder migrasi dengan perintah berikut:
   ```bash
    poetry run flask db init

    #Ini akan membuat folder migrations di direktori proyek kamu
   ```
4. Membuat Migrasi, Mengaplikasikan Migrasi dan Rollback Migrasi(Opsional)
Setelah kamu membuat atau memodifikasi model database, buatlah skrip migrasi dengan perintah berikut:
   ```bash
    poetry run flask db migrate -m "Deskripsi migrasi"

    #Gantilah "Deskripsi migrasi" dengan deskripsi yang relevan tentang perubahan yang dilakukan.
   ```
    Terapkan migrasi yang telah dibuat ke database dengan perintah berikut:
   ```bash
    poetry run flask db upgrade
   ```
   Jika kamu perlu membatalkan migrasi, kamu bisa menggunakan:
    ```bash
    poetry run flask db downgrade
    ```
Dengan mengikuti langkah-langkah ini, kamu dapat mengkonfigurasi dan menggunakan Flask-Migrate dengan Poetry dalam proyek Flask kamu. Ini memungkinkan kamu untuk mengelola perubahan skema database secara efisien.
## URL Deployment

Aplikasi backend ini telah dideploy menggunakan layanan [Vercel](https://vercel.com) dan dapat diakses melalui URL berikut: [https://masakinprojectbe.vercel.app/](https://masakinprojectbe.vercel.app/). URL ini dapat digunakan oleh aplikasi frontend untuk mengakses berbagai endpoint yang disediakan oleh backend, seperti manajemen resep, otentikasi pengguna, dan lain-lain.

## Dokumentasi API
Untuk mempermudah akses dan penggunaan API, dokumentasi API aplikasi Masakin tersedia di Postman. Kamu dapat mengimpor koleksi Postman menggunakan [tautan ini](https://documenter.getpostman.com/view/32137902/2sA3e1DAgX#intro). Dokumentasi ini mencakup:

- **Endpoint API:** Deskripsi lengkap setiap endpoint, metode HTTP, parameter, dan contoh permintaan serta respons.
- **Autentikasi:** Panduan penggunaan JWT untuk autentikasi API (Bearer Token).
- **Contoh Permintaan:** Contoh permintaan GET, POST, PUT, DELETE untuk berbagai endpoint.


## Kontributor

| Nama                | Peran                        | Kontak                           |
|---------------------|------------------------------|----------------------------------|
| **Iman Maris**        | Pengembang Backend (Setup Database, Relasi antar models, dll)           | [marisiman99@gmail.com](marisiman99@gmail.com) |
| **Jane Smith**      | Pengembang Backend (CRUD API , tester/ debuger)          | [yosaphatharwindra@gmail.com](yosaphatharwindra@gmail.com) |


## Penutup

Semoga proyek ini dapat berjalan dengan lancar dan memberikan manfaat pembelajaran bagi kami sebagai pengembang. Terima kasih semua.

---

<div align="center">
    <sub>Made by the Masakin Project Team. Powered by Vercel and Supabase.</sub>
</div>

<div align="center">
    <a href="https://vercel.com"><img src="https://img.shields.io/badge/Powered%20by-Vercel-blue?logo=vercel&logoColor=white"></a>
    <a href="https://supabase.com"><img src="https://img.shields.io/badge/Powered%20by-Supabase-green?logo=supabase&logoColor=white"></a>
</div>