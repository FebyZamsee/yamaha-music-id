from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import os
import time
import random
from  traceback import format_exc as erlog

os.system('cls')
with open("daerah.txt",encoding="utf-8") as cvs:
	fileD = cvs.read().strip().splitlines()
daerahlist = fileD

from tkinter import Tk, Label, Button, Toplevel
from tkinter import ttk

def buttonOK(title, message):
    top = Toplevel()
    top.title(title)

    label = Label(top, text=message, font=('Helvetica', 14, 'bold'))
    label.pack(padx=10, pady=10)

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 16, 'bold'),
                    foreground='#ffffff', background='#4CAF50', padding=(20, 10))

    ok_button = ttk.Button(
        top, text="OK", command=top.destroy, style='TButton')
    ok_button.pack(pady=20)

    screen_height = top.winfo_screenheight()
    x_position = 0
    y_position = screen_height - top.winfo_reqheight()
    top.geometry("+{}+{}".format(x_position, y_position))

    top.wait_window()


filename = input('[?] Nama File : ')
with open(filename, 'r+') as file:
	akunlist = file.read().strip().splitlines()

	for ke,akun in enumerate(akunlist):
		adres2 = random.choice(daerahlist).lower().capitalize()
		print(f"\n----[{ke+1}]----")
		empas = akun.split(' ')
		email = empas[0]
		pw = empas[1]
		no = empas[2]
		try:
			web = webdriver.Chrome()
			web.set_window_size(200, 420)
			web.set_window_position(0, 0)
			web.get("https://id.yamaha.com/index.html#")

			login_button = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.ID, "login-button")))
			login_button.click()

			email_input = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.ID, "gigya-loginID-67897267002611440")))
			email_input.send_keys(email)
			print("[] Email :", email)

			password_input = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.ID, "gigya-password-125149165024586620")))
			password_input.send_keys(pw)
			print("[] Password :", pw)

			actions = ActionChains(web)
			# time.sleep(5)
			submit_button = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME, "gigya-input-submit")))
			actions.send_keys(Keys.RETURN)
			actions.perform()
			print("[] Login")
			# input()
			# time.sleep(10)
			# buka menu edit
			time.sleep(6)
			login_button = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.ID, "login-button"))
			)
			login_button.click()
			time.sleep(3)

			# Cari dan klik tombol "Data Saya"
			data_saya_button = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-pagekey='mydetails'] a")))
			data_saya_button.click()
			time.sleep(0.8)

			edit_button = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.CLASS_NAME, "btn-edit")))
			edit_button.click()


			print("[] Edit Page")
			time.sleep(1)

			# isi form
			nomor = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.ID, "mypage-mydetails-edit-phonenumber")))
			posCode = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.ID, "mypage-mydetails-edit-postalcode")))
			select_element = WebDriverWait(web, 10).until(
				EC.presence_of_element_located(
					(By.ID, "mypage-mydetails-edit-postaladdress1"))
			)

			select = Select(select_element)
			options = select.options
			random_option = random.choice(options)
			selected_option = random_option.get_attribute("value")
			daerah = WebDriverWait(web, 10).until(
				EC.presence_of_element_located((By.ID, "mypage-mydetails-edit-postaladdress2")))

			nomor.send_keys(no)
			print("[] Phone Number :", no)
			# time.sleep(0.8)

			kodepos = str(random.randint(22564,69872))
			posCode.send_keys(kodepos)
			print("[] Postal Code :", kodepos)

			# time.sleep(0.8)

			select.select_by_value(selected_option)

			print("[] Address 1 :", selected_option)

			# time.sleep(0.8)

			daerah.send_keys(adres2)
			print('[] Address 2 :', adres2)
			web.set_window_position(0, 400)

			# time.sleep(0.8)
			buttonOK("Continue","Tekan Enter Untuk Melanjutkan")
			file.seek(0)
			lines = file.readlines()
			file.seek(0)
			file.writelines(line for line in lines if akun not in line)
			file.truncate()
			print("Menghapus List")
			web.quit()
		except:
			print("Error ...")
			web.quit()
			# print(erlog())
			continue


