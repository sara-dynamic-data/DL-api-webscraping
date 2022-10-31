from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


def get_rad_info(num):

    table_actuaciones = pd.DataFrame(columns=[
                                     'Fecha Actuación', 'Tipo', 'Anotación', 'Fecha Inicio', 'Fecha Finalizo', 'Fecha Registro'])

    for i in range(0, 2):

        try:

            chromedriver_autoinstaller.install()
            driver = webdriver.Chrome()
            driver.get(
                'https://consultaprocesos.ramajudicial.gov.co/Procesos/NumeroRadicacion')

            # ENVIAR KEY(RADICADO)

            WebDriverWait(driver, 2)\
                .until(EC.element_to_be_clickable((By.XPATH,
                                                  "//input[@id='input-72']")))\
                .send_keys(num)

            # CLICK BUSCAR

            button_search_info = driver.find_element(By.CLASS_NAME, 'mt-n2')
            button_search_info.find_element(
                By.CLASS_NAME, 'v-btn.v-btn--is-elevated.v-btn--has-bg.theme--light.v-size--default.success.mx-2.font-weight-bold') .click()

            try:
                time.sleep(2)
                driver.find_element(
                    By.XPATH, "/html/body/div/div[3]/div/div/div[2]/div/button")
                print('entro')
                alert = True

            except:
                alert = False
                print('siguio')
                pass

            if alert == True:
                break
                driver.close()
            else:

                # SELECCIONAR RADICADO
                time.sleep(1)

                WebDriverWait(driver, 2)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                      "/html/body/div/div[1]/div[3]/main/div/div/div/div[2]/div/div/div[2]/div/table/tbody/tr/td[2]/button")))\
                    .click()

                # CLICK BOTON ACTUACIONES
                time.sleep(2)

                WebDriverWait(driver, 2)\
                    .until(EC.element_to_be_clickable((By.XPATH,
                                                      "/html/body/div/div/div[3]/main/div/div/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/div[5]")))\
                    .click()

                # VERIFICAR NUMERO DE PAGINAS

                try:
                    number_pages = driver.find_element(
                        By.CLASS_NAME, 'v-pagination.theme--light')
                    time.sleep(2)
                    number_pages_container = number_pages.find_elements(
                        By.TAG_NAME, 'li')
                    time.sleep(2)
                    pages = [i.text for i in number_pages_container]
                    max_page = max(pages)
                except:
                    max_page = 1
                print(max_page)

                for i in range(1, int(max_page)+1):
                    print(i)

                    # IDENTIFICAR TABLA
                    table_container = driver.find_element(
                        By.CLASS_NAME, "v-data-table.elevation-1.caption.v-data-table--has-bottom.theme--light")

                    info_table = table_container.find_element(
                        By.TAG_NAME, "tbody")
                    time.sleep(2)
                    info_table_fecha_actuacion = info_table.find_elements(
                        By.XPATH, "/html/body/div/div/div[3]/main/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr/td[1]")
                    fecha_actuacion = [
                        i.text for i in info_table_fecha_actuacion]
                    time.sleep(2)
                    info_table_actuacion = info_table.find_elements(
                        By.XPATH, "/html/body/div/div/div[3]/main/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr/td[2]")
                    actuacion = [i.text for i in info_table_actuacion]
                    time.sleep(2)
                    info_table_anotacion = info_table.find_elements(
                        By.XPATH, "/html/body/div/div/div[3]/main/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr/td[3]")
                    anotacion = [i.text for i in info_table_anotacion]
                    time.sleep(2)
                    info_table_anotacion = info_table.find_elements(
                        By.XPATH, "/html/body/div/div/div[3]/main/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr/td[4]")
                    fecha_inicio = [i.text for i in info_table_anotacion]
                    time.sleep(2)
                    info_table_anotacion = info_table.find_elements(
                        By.XPATH, "/html/body/div/div/div[3]/main/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr/td[5]")
                    fecha_finalizo = [i.text for i in info_table_anotacion]
                    time.sleep(2)
                    info_table_anotacion = info_table.find_elements(
                        By.XPATH, "/html/body/div/div/div[3]/main/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/table/tbody/tr/td[6]")
                    fecha_registro = [i.text for i in info_table_anotacion]

                    tabla_temp = pd.DataFrame(list(zip(fecha_actuacion, actuacion, anotacion, fecha_inicio, fecha_finalizo, fecha_registro)), columns=[
                                              'Fecha Actuación', 'Tipo', 'Anotación', 'Fecha Inicio', 'Fecha Finalizo', 'Fecha Registro'])
                    table_actuaciones = pd.concat(
                        [table_actuaciones, tabla_temp], ignore_index=True)

                    if max_page != 1:
                        next_page = [
                            j for j in number_pages_container if j.text == str((i+1))]
                        if len(next_page) > 0:
                            next_page[0].click()
                            time.sleep(2)
                        else:
                            break

                print('acabo')
                driver.close()
                break

        except:
            driver.close()
            continue

    if len(table_actuaciones) > 0:
        df = table_actuaciones
    else:
        df = table_actuaciones
    return df


#table = get_rad_info("05001400300420190015200")
# table.to_csv('table.csv')
