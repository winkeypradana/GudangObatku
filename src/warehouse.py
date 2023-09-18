import csv
import time
import os
import getpass
from tabulate import tabulate
from datetime import datetime


def clear_screen():
    os.system('clear')

def initialize_db():
    """
    Fungsi untuk menginisialisasi database
    """
    # Membaca data dari file CSV
    with open("data/database-warehouse.csv", "r") as file:
        reader = csv.reader(file)
        db = list(reader)
    return db

def save_db(db):
    """
    Fungsi untuk menyimpan database ke dalam file CSV
    """
    with open("data/database-warehouse.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(db)

def lihat_stock_obat(db):
    """
    Fungsi untuk menampilkan stock obat dari database
    """
    clear_screen()
    headers = ["Nama", "Kode Obat", "Bentuk Obat", "Klasifikasi Obat", "Tanggal Kadaluarsa", "Stock", "Harga"]
    data = db[1:]

    print("\n{:^40}".format("=== Selamat Datang di Menu Lihat Stock Obat Gudang Obatku ==="))
    print("\n{:^60}".format("=== Silahkan Pilih Pilihan Yang Tersedia ==="))
    
    while True:
        print("\nMenu Utama Lihat Stock:")
        print("1. Tampilkan Semua Obat")
        print("2. Urutan Obat Mendekati Kadaluarsa")
        print("3. Urutan Obat Berdasarkan Stock Terendah")
        print("4. Urutan Obat Berdasarkan Klasifikasi Obat")
        print("5. Cari Obat Berdasarkan Kode Obat")
        print("0. Kembali ke Menu Utama")
        
        choice = input("Pilih menu (0-5): ")
        
        if choice == "0":
            clear_screen()
            return
        
        elif choice == "1":
            clear_screen()
            print("\n=== Stock Semua Obat ===")
            if len(data) == 0:
                print("\nMaaf, database Anda tidak tersedia!")
            else:
                print(tabulate(data, headers=headers, tablefmt="grid"))
        
        elif choice == "2":
            clear_screen()
            print("\n=== Urutan Obat Mendekati Kadaluarsa ===")
            if len(data) == 0:
                print("\nMaaf, database Anda tidak tersedia!")
            else:
            # Mengubah string tanggal menjadi objek datetime untuk pengurutan
                for row in db[1:]:
                    row[5] = datetime.strptime(row[5], "%d-%m-%Y")
                
                db_sorted_by_expiry = sorted(db[1:], key=lambda x: x[5])  # Sort by expiry date in ascending order
            
                # Mengubah kembali objek datetime menjadi string untuk ditampilkan dalam tabel
                for row in db_sorted_by_expiry:
                    row[5] = row[5].strftime("%d-%m-%Y")
                
                expiry_table = [[row[1], row[2], row[5]] for row in db_sorted_by_expiry]
            
                print(tabulate(expiry_table, headers=["Nama Obat","Kode Obat", "Tanggal Kadaluarsa"], tablefmt="grid"))
        
        elif choice == "3":
            clear_screen()
            print("\n=== Urutan Obat Berdasarkan Stock Terendah ===")
            if len(data) == 0:
                print("\nMaaf, database Anda tidak tersedia!")
            else:
                db_sorted_by_stock = sorted(db[1:], key=lambda x: int(x[6]))
                stock_table = [[row[1], row[2], row[6]] for row in db_sorted_by_stock]
                print(tabulate(stock_table, headers=["Nama Obat","Kode Obat", "Stock"], tablefmt="grid"))
        
        elif choice == "4":
            clear_screen()
            print("\n=== Urutan Obat Berdasarkan Klasifikasi Obat ===")
            if len(data) == 0:
                print("\nMaaf, database Anda tidak tersedia!")
            else:
                db_sorted_by_class = sorted(db[1:], key=lambda x: x[4])
                class_table = [[row[1], row[2], row[4]] for row in db_sorted_by_class]
                print(tabulate(class_table, headers=["Nama Obat","Kode Obat", "Klasifikasi Obat"], tablefmt="grid"))

        elif choice == "5":
            clear_screen()
            print("\n=== Cari Obat Berdasarkan Kode Obat ===")
            kode_obat = input("Masukkan kode obat yang ingin dicari: ")
            
            obat_ditemukan = False
            obat_data = []
            for row in db[1:]:
                if row[2] == kode_obat:
                    obat_ditemukan = True
                    obat_data.append(row)
            
            if obat_ditemukan:
                print("\n=== Obat Ditemukan ===")
                print(tabulate(obat_data, headers=["Nama Obat","Kode Obat", "Bentuk Obat", "Klasifikasi Obat", "Tanggal Kadaluarsa", "Stock", "Harga"], tablefmt="grid"))
            else:
                print("\n=== Obat Tidak Ditemukan ===")

        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")
            time.sleep(3)
            clear_screen()

def tambah_obat_baru(db):
    """
    Fungsi untuk menambahkan obat baru ke database
    """
    clear_screen()
    data_input = []

    while True:
        print("\n=== Tambah Obat Baru ===")
        print("\n1.Tambah Obat Baru")
        print("0.Kembali ke Menu Utama")

        choice = input("\nPilih menu (0-1): ")
        if choice == "0":
            clear_screen()
            return
        
        elif choice == "1":
            clear_screen()
            while True:
                nama_obat = input("Masukkan nama obat: ").capitalize()

                while True:
                    bentuk_obat = input("Masukkan bentuk obat: ").capitalize()
                    if not bentuk_obat.isalpha():
                        print("Hanya karakter alfabet yang diizinkan. Silakan coba lagi.")
                        continue
                    if any(obat[1].capitalize() == nama_obat.capitalize() and obat[3].capitalize() == bentuk_obat.capitalize() for obat in db):
                        print("Maaf, obat tersebut sudah ada. Silahkan input obat lainnya.")
                        return
                    else:
                        break

                while True:
                    klasifikasi_obat = input("Masukkan klasifikasi obat: ").title()
                    if not klasifikasi_obat.replace(" ", "").isalpha():
                        print("Hanya karakter alfabet yang diizinkan. Silakan coba lagi.")
                        continue
                    else:
                        break

                #Kode_obat otomatis
                kode_obat = nama_obat[:2].capitalize() + nama_obat [-1] + bentuk_obat[-0] + bentuk_obat[-1] + klasifikasi_obat[-1]
    
                while True:
                    tanggal_kadaluarsa_input = input("Masukkan tanggal kadaluarsa (DDMMYYYY): ")
                    if len(tanggal_kadaluarsa_input) != 8 or not tanggal_kadaluarsa_input.isdigit():
                        print("Tanggal tidak valid. Silakan input dalam format DDMMYYYY dan diatas tahun 2023.")
                        continue

                    # Ubah ke format DD-MM-YYYY
                    tanggal_kadaluarsa = '-'.join([tanggal_kadaluarsa_input[:2], tanggal_kadaluarsa_input[2:4], tanggal_kadaluarsa_input[4:]])

                    day, month, year= [int(part) for part in tanggal_kadaluarsa.split('-')]
                    if not (1 <= day <= 31) or not (1 <= month <= 12) or year <= 2023:
                        print("Tanggal tidak valid. Silakan input dalam format DDMMYYYY dan diatas tahun 2023.")
                        continue
                    try:
                        datetime.strptime(tanggal_kadaluarsa, "%d-%m-%Y")
                        break  # Jika berhasil, keluar dari loop
                    except ValueError:
                        print("Tanggal tidak valid. Silakan input dalam format DDMMYYYY dan diatas tahun 2023.")

                while True:
                    stock_obat = input("Masukkan stock obat: ")
                    if not stock_obat.isdigit():
                        print("Stock harus berupa angka. Silakan coba lagi.")
                        continue
                    else:
                        break

                while True:
                    harga_obat = input("Masukkan harga obat: ")
                    if not harga_obat.isdigit():
                        print("Stock harus berupa angka. Silakan coba lagi.")
                        continue
                    else:
                        break
            
                # Untuk menampilkan data yang sudah di input
                data_input.append([nama_obat, kode_obat, bentuk_obat, klasifikasi_obat, tanggal_kadaluarsa, stock_obat, harga_obat])
                print("Data Input:")
                print(tabulate(data_input, headers=["Nama Obat", "Kode Obat", "Bentuk Obat", "Klasifikasi Obat", "Tanggal Kadaluarsa", "Stock Obat", "Harga Obat"], tablefmt="grid"))
            
                confirm = ""
                while confirm.lower() != "ya" and confirm.lower() != "tidak":
                    confirm = input("Apakah anda ingin menambahkan obat lainnya? (ya/tidak): ")
                    if confirm.lower() == "ya":
                        break
                    elif confirm.lower() != "tidak":
                        print("Input tidak valid. Silakan masukkan 'ya' atau 'tidak'.")

                if confirm.lower() != "ya":
                    break

            confirm = input("Apakah anda yakin ingin menambahkan obat yang sudah anda input? (ya/tidak): ")

            while confirm not in ["ya", "tidak"]:
                print("Input tidak valid. Silakan masukkan 'ya' atau 'tidak'.")
                confirm = input("Apakah anda yakin ingin menambahkan obat yang sudah anda input? (ya/tidak): ").lower()

            if confirm.lower() == "ya":
                print("\n=== Validasi ===")
                for attempt in range(3):
                    input_username = input("Masukkan username: ").upper()
                    input_password = getpass.getpass("Masukkan password: ")

                    if input_username == "WINKEY" and input_password == "123":
                        for obat in data_input:
                            obat_baru = [str(len(db))] + obat[0:]
                            db.append(obat_baru)
                            # Memperbarui indeks setelah menambahkan obat baru
                            for i in range (1, len(db)):
                                db[i][0] = str(i)
                        print("Obat berhasil ditambahkan!")
                        save_db(db)
                        break
                    else:
                        print("Username atau password salah. Silakan coba lagi.")
                else:
                    print("Maaf kami tidak bisa memvalidasi anda, tidak ada obat baru yang ditambahkan!")
                    break
            
            elif confirm.lower() == "tidak":
                print("Tidak ada obat baru yang ditambahkan!")
                break
        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")
            time.sleep(3)
            clear_screen()

def update_obat(db):
    """
    Fungsi untuk mengupdate stock obat di dalam database
    """
    clear_screen()
    while True:
        print("\n=== Update Obat ===")
        print("\n1. Update Stock Obat")
        print("2. Update Harga Obat ")
        print("0. Kembali ke Menu Utama")

        choice = input("\nPilih menu (0-1): ")
        if choice == "0":
            clear_screen()
            return
        
        elif choice == "1":
            clear_screen()
            print("\n=== Update Stock Obat ===")
            nama_obat = input("Masukkan nama obat yang akan diupdate stocknya: ").capitalize()
            kode_obat = input("Masukkan kode obat yang akan diupdate stocknya (Case Sensitive): ")

            # Memeriksa apakah nama obat dan kode obat terdaftar dalam database
            obat_terdaftar = False
            obat_data = []
            for row in db[1:]:
                if row[1] == nama_obat and row[2] == kode_obat:
                    obat_terdaftar = True
                    obat_data = row
                    break
            
            if not obat_terdaftar:
                print("Obat tidak terdaftar!")
                continue

            # Menampilkan tabel obat hanya untuk entri yang diinput oleh pengguna
            headers = ["No", "Nama Obat", "Kode Obat", "Stock"]
            table_data = []
            for i, row in enumerate(db[1:]):
                if row[1] == nama_obat and row[2] == kode_obat:
                    table_data.append([i+1, row[1], row[2], row[6]])
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            for row in db[1:]:
                if row[1] == nama_obat:
                    while True:
                        stock_baru = input(f"Masukkan stock obat {row[1]} ({row[2]}) yang baru: ")
                        if stock_baru.isdigit():
                            confirm = ""
                            while confirm.lower() != "ya" and confirm.lower() != "tidak":
                                confirm = input("Apakah anda yakin ingin mengubah stock obat? (ya/tidak): ")
                                if confirm.lower() == "ya":
                                    print("\n=== Validasi ===")
                                    for attempt in range(3):
                                        input_username = input("Masukkan username: ").upper()
                                        input_password = getpass.getpass("Masukkan password: ")

                                        if input_username == "WINKEY" and input_password == "123":
                                            row[6] = stock_baru
                                            print("\nStock obat berhasil diupdate!")
                                            print(f"Stock obat {row[1]} sekarang adalah {stock_baru}")
                                            save_db(db)
                                            return
                                        else:
                                            print("Username atau password salah. Silakan coba lagi.")

                                    print("Maaf kami tidak bisa memvalidasi anda!")
                                    print("Stock obat tidak berhasil diupdate!")
                                    clear_screen()
                                    return
                                elif confirm.lower() == "tidak":
                                    print("Stock obat tidak ada yang terupdate!")
                                    clear_screen
                                    return
                                else:
                                    print("Input tidak valid. Silahkan masukkan 'ya' atau 'tidak'.")
                        else:
                            print("Maaf anda harus menginput angka!")

            print("Obat tidak ditemukan!")
            

        elif choice == "2":
            clear_screen()
            print("\n=== Update Harga Obat ===")
            nama_obat = input("Masukkan nama obat yang akan diupdate harganya: ").capitalize()
            kode_obat = input("Masukkan kode obat yang akan diupdate harganyanya (Case Sensitive): ")

            # Memeriksa apakah nama obat dan kode obat terdaftar dalam database
            obat_terdaftar = False
            obat_data = []
            for row in db[1:]:
                if row[1] == nama_obat and row[2] == kode_obat:
                    obat_terdaftar = True
                    obat_data = row
                    break
            
            if not obat_terdaftar:
                print("Obat tidak terdaftar!")
                continue

            # Menampilkan tabel obat hanya untuk entri yang diinput oleh pengguna
            headers = ["No", "Nama Obat", "Kode Obat", "Harga"]
            table_data = []
            for i, row in enumerate(db[1:]):
                if row[1] == nama_obat and row[2] == kode_obat:
                    table_data.append([i+1, row[1], row[2], row[7]])
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            
            for row in db[1:]:
                if row[1] == nama_obat:
                    while True:
                        harga_baru = input(f"Masukkan harga obat {row[1]} ({row[2]}) yang baru: ")
                        if harga_baru.isdigit():
                            confirm = ""
                            while confirm.lower() != "ya" and confirm.lower() != "tidak":
                                confirm = input("Apakah anda yakin ingin mengubah harga obat? (ya/tidak): ")
                                if confirm.lower() == "ya":
                                    print("\n=== Validasi ===")
                                    for attempt in range(3):
                                        input_username = input("Masukkan username: ").upper()
                                        input_password = getpass.getpass("Masukkan password: ")

                                        if input_username == "WINKEY" and input_password == "123":
                                            row[7] = harga_baru
                                            print("\nHarga obat berhasil diupdate!")
                                            print(f"Harga obat {row[1]} sekarang adalah {harga_baru}")
                                            save_db(db)
                                            return
                                        else:
                                            print("Username atau password salah. Silakan coba lagi.")

                                    print("Maaf kami tidak bisa memvalidasi anda!")
                                    print("Harga obat tidak berhasil diupdate!")
                                    return
                                elif confirm.lower() == "tidak":
                                    print("Harga obat tidak ada yang terupdate!")
                                    return
                                else:
                                    print("Input tidak valid. Silahkan masukkan 'ya' atau 'tidak'.")
                        else:
                            print("Maaf anda harus menginput angka!")

            print("Obat tidak ditemukan!")

        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")
            time.sleep(3)
            clear_screen()

def hapus_obat(db):
    """
    Fungsi untuk menghapus obat dari database
    """
    clear_screen()
    while True:
        print("\n=== Hapus Obat ===")
        print("\n1. Hapus Obat")
        print("0. Kembali ke Menu Utama")

        choice = input("\nPilih menu (0-1): ")
        if choice == "0":
            clear_screen()
            return
        
        elif choice == "1":
            clear_screen
            tabel_obat = []
            while True:
                nama_obat = input("Masukkan nama obat yang akan dihapus: ").capitalize()
                kode_obat = input("Masukkan kode obat yang akan dihapus (Case Sensitive): ")

                obat_ditemukan = False
                for i in range(1, len(db)):
                    if db[i][1] == nama_obat and db[i][2] == kode_obat:
                        obat_ditemukan = True
                        tabel_obat.append(db[i])
                
                if not obat_ditemukan:
                    print("Obat tidak terdaftar!")
                    break
                
                confirm = input("Apakah anda ingin menghapus obat lainnya? (ya/tidak): ")
                while confirm.lower() != "ya" and confirm.lower() != "tidak":
                    print("Input tidak valid. Silakan masukkan 'ya' atau 'tidak'.")
                    confirm = input ("Apakah anda ingin menghapus obat lainnya? (ya/tidak): ")
                
                if confirm.lower() == "tidak":
                    break

            if len(tabel_obat) > 0:
                print("\n=== Obat yang akan dihapus ===")
                print(tabulate(tabel_obat, headers=["Nomor", "Nama", "Kode Obat", "Bentuk Obat", "Klasifikasi Obat", "Tanggal Kadaluarsa", "Stock", "Harga"], tablefmt="grid"))

                confirm = input("Apakah anda yakin ingin menghapus obat yang sudah anda input? (ya/tidak): ")
                while confirm.lower() not in ["ya", "tidak"]:
                    print("Input tidak valid. Silakan masukkan 'ya' atau 'tidak'.")
                    confirm = input("Apakah anda yakin ingin menghapus obat yang sudah anda input? (ya/tidak): ").lower()

                if confirm.lower() == "tidak":
                    print("Obat tidak ada yang terhapus!")
                else:
                    print("\n=== Validasi ===")
                    for attempt in range(3):
                        input_username = input("Masukkan username: ").upper()
                        input_password = getpass.getpass("Masukkan password: ")

                        if input_username == "WINKEY" and input_password == "123":
                            for obat in tabel_obat:
                                db.remove(obat)
                            print("Obat berhasil dihapus!")
                            save_db(db)
                            break
                        else:
                            print("Username atau password salah. Silakan coba lagi.")
                    else:
                        print("Maaf kami tidak bisa memvalidasi anda, obat tidak ada yang terhapus!")
            else:
                print("Tidak ada obat yang akan dihapus!")
        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")
            time.sleep(3)
            clear_screen()

        # Memperbarui indeks setelah menghapus obat
        for i in range(1, len(db)):
            db[i][0] = str(i)

def pembelian_obat(db):
    """
    Fungsi untuk menampilkan urutan obat yang mendekati kadaluarsa
    dan urutan obat dari stock yang paling sedikit hingga terbanyak
    """
    clear_screen()
    while True:
        print("\n===Pembelian Obat===")
        print("\n1. Pembelian Obat")
        print("0. Kembali ke Menu Utama")
        
        choice = input("\nPilih menu (0-1): ")
        if choice == "0":
            clear_screen()
            return
        
        elif choice == "1":
            clear_screen()
            cart = []
            print("\nObat yang tersedia:")
            table = []
            for i, item in enumerate(db[1:]):
                    table.append([i+1, item[1], item[2], item[3], item[4], item[5], item[6], item[7]])
            print(tabulate(table, headers=["No.", "Nama Obat", "Kode Obat", "Bentuk Obat", "Klasifikasi Obat", "Tanggal Kadaluarsa", "Stock", "Harga"], tablefmt="grid"))

            while True: 
                nama_obat = input("Masukkan nama obat yang ingin dibeli: ").capitalize()
                kode_obat = input("Masukkan kode obat yang ingin dibeli: ")
                
                obat_terdaftar = False
                obat_data = []
                for row in db[1:]:
                    if row[1] == nama_obat and row[2] == kode_obat:
                        obat_terdaftar = True
                        obat_data = row
                        break
                
                if not obat_terdaftar:
                    print("Obat tidak terdaftar!")
                    continue
                
                stock = int(obat_data[6])
                while True:
                    try:
                        qty = int(input(f"Masukkan jumlah obat {nama_obat} ({kode_obat}) yang ingin dibeli: "))
                        if qty > stock:
                            print(f"Stock {nama_obat} ({kode_obat}) tinggal {stock}")
                            continue
                        break
                    except ValueError:
                        print("Mohon masukkan angka yang valid.")
              
                total_harga = qty * int(obat_data[7])
                cart.append([nama_obat, kode_obat, qty, total_harga])
                
                # Update stock di database
                obat_data[6] = str(stock - qty)
                
                print("\nIsi Keranjang:")
                print(tabulate(cart, headers=["Nama Obat", "Kode Obat", "Qty", "Total Harga"], tablefmt="grid"))
                
                while True:
                    ans = input("\nIngin membeli obat lain? (ya/tidak): ")
                    if ans.lower() in ["ya", "tidak"]:
                        break
                    else:
                        print("Input tidak valid. Silakan masukkan 'ya' atau 'tidak'.")
                
                if ans.lower() == "tidak":
                    break
            
            total_biaya = sum(item[3] for item in cart)
            print("\nDaftar Pembelian:")
            print(tabulate(cart, headers=["Nama Obat", "Kode Obat", "Qty", "Total Harga"], tablefmt="grid"))
        
            # Tampilkan total yang harus dibayar
            print(f"\nTotal Yang Harus Dibayar: Rp.{total_biaya}")
            while True:
                try:
                    pembayaran = int(input('\nSilakan masukkan jumlah uang pembayaran: Rp.'))
                    if pembayaran < total_biaya:
                        print(f'Maaf, jumlah uang yang Anda bayarkan kurang. Total yang harus dibayar adalah Rp.{total_biaya}')
                    elif pembayaran > total_biaya:
                        kembalian = pembayaran - total_biaya
                        print(f'Terima kasih, berikut ini kembaliannya: Rp.{kembalian}')
                        save_db(db)
                        break
                    else:
                        print('Uang Anda pas, Terima kasih')
                        save_db(db)
                        break
                except ValueError:
                    print("Mohon masukkan angka yang valid.")
        else:
            print("Pilihan tidak valid. Silakan pilih menu yang tersedia.")
            time.sleep(3)
            clear_screen()