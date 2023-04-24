import re
import time
from selenium import webdriver
# from selenium.common import ElementNotVisibleException, ElementNotSelectableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
import csv
from multiprocessing import Pool
option = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
option.add_experimental_option("prefs",prefs)
option.add_argument("--window-size=1920,1080")
# option.add_argument("--headless=new")

def MainParcer(urls_category):
    try:
        driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=option)



        def GetLinksCategories():
            block_category = driver.find_element(By.XPATH, '//div[@class="wR"]')
            categories_elemets = block_category.find_elements(By.XPATH, '//a[@class="JU wS"]')

            return categories_elemets



        def ParsingBlocksProducts(product_category):
            # FilterStore()
            driver.implicitly_wait(10)



            def ParsingUrlsProducts():
                product_urls = []
                time.sleep(10)
                block = driver.find_element(By.XPATH, "//div[@class='El Eo']")
                link_elements = block.find_elements(By.XPATH, "//section[@class='Il Ip En']/a")

                # button = block.find_elements(By.XPATH, "//button[@class='fw zu fB fH']")
                # for i in button:
                #     i.click()
                #     time.sleep(1)

                for element in link_elements:
                    product_urls.append(element.get_attribute('href'))

                return product_urls


            def Main():
                product_urls = []
                time.sleep(10)
                try:
                    product_urls += ParsingUrlsProducts()
                except Exception as e:
                    print("Ошибка:", e)
                    print("Товары не найдены")
                    pass
                try:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='eg ek ez eq eG eK et']")))
                    print("Кнопка загрузки обнаружена")
                except:
                    print("Кнопка загрузки не найдена")

                isNextDisabled = False
                driver.implicitly_wait(10)
                while not isNextDisabled:
                            try:
                                next = driver.find_elements(By.XPATH, "//nav[@aria-label='pagination']/ol/li")
                                next[-1].click()
                                print("Перехожу на следущую стараницу категории")
                            except Exception as e:
                                print('Кнопка далее не работает!')
                            try:
                                    WebDriverWait(driver, 2).until( EC.element_to_be_clickable((By.XPATH, "//button[@class='eg ek ez eq eG eK et']")))
                                    product_urls += ParsingUrlsProducts()
                            except:
                                    print("Выход из цикла!!!")
                                    product_urls += ParsingUrlsProducts()
                                    isNextDisabled = True
                                    return product_urls
                return product_urls

            return  Main()


        def ChoiceAktobe():
            driver.find_element(By.XPATH, "//li[@class='nM n_3 nU nX nN cV cW nS']/div[@class='nQ']").click()
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, "//span[contains(text(),'Актобе')]").click()


        def CheckWindowMail():

            # Переменая для
            try:
                # try:
                #     driver.implicitly_wait(5)
                #     driver.switch_to.frame("fl-642215")
                #     driver.implicitly_wait(5)
                #     driver.find_element(By.XPATH, "//div[@class='screen screen--login']/button[@class='close']").click()
                # except:
                #     driver.switch_to.default_content()
                try:
                    driver.switch_to.frame("fl-350315")
                    driver.find_element(By.XPATH, "//a[@class='Notification-button Notification-buttonBlock']").click()
                    driver.switch_to.default_content()
                    driver.find_element(By.XPATH, "//div[@class='v w']/button[@class='eg A ek ez eq eG eL']").click()
                except:
                    driver.switch_to.default_content()
                    driver.find_element(By.XPATH, "//div[@class='v w']/button[@class='eg A ek ez eq eG eL']").click()

            except Exception as e:
                driver.switch_to.default_content()
                print("Ошибка:", e)
                print("Окна с рассылкой нет!")


        def ParsingProductPage(product_urls, winHandleBefore, product_category):
            CheckWindowMail()
            driver.switch_to.new_window('tab')
            for href in product_urls:
                print("Перехожу по ссылке:", href)
                if href:
                    driver.get(href)
                else:
                   return print("Ссылки нет")
                try:
                    try:
                        try:
                            driver.implicitly_wait(2)
                            price = driver.find_element(By.XPATH, '//div[@class="XG"]/div[@class="bbn"]/div[@class="bbo"]').text
                            sale_price = price
                        except:
                            driver.implicitly_wait(2)
                            price = driver.find_element(By.XPATH, '//div[@class="XG"]/div[@class="ba_7 bbc"]/div[@class="ba_9"]/div[@class="bba"]/span').text
                            sale_price = driver.find_element(By.XPATH, '//div[@class="XG"]/div[@class="ba_7 bbc"]/div[@class="ba_8"]').text
                    except:
                        try:
                            try:
                                price = driver.find_element(By.XPATH, "//div[@class='bb_']").text
                                sale_price = driver.find_element(By.XPATH, "//div[@class='bb_3 bb_5']").text
                            except:
                                price = driver.find_element(By.XPATH, "//div[@class='bb_3'] || //p[@class='bb_3']").text
                                sale_price = price
                        except:
                            try:
                                price = driver.find_element(By.XPATH, "//div[@class='ba_7']/div[@class='ba_8']").text
                                sale_price = price
                            except:
                                try:
                                    price = driver.find_element(By.XPATH, "//div[@class='bbZ']/p[@class='bb_']").text
                                    sale_price = driver.find_element(By.XPATH, "//div[@class='bb_0']/p[@class='bb_3 bb_5']").text
                                except:
                                    price = driver.find_element(By.XPATH, "//div[@class='bb_0']/p[@class='bb_3']").text
                                    sale_price = price
                except Exception as e:
                    print("НЕ НАШЛИ ЦЕНУ!")
                    break



                try:
                    try:
                        name = driver.find_element(By.XPATH, '//header[@class="Hz ix"]/h1').text
                    except:
                        name = driver.find_element(By.XPATH, '//h1[@class="YL"]').text
                except:
                    print("Название нет")
                try:
                    try:
                        picture = driver.find_element(By.XPATH, '//picture[@class="Hg Hh"]/img').get_attribute('src')
                    except:
                        picture = driver.find_element(By.XPATH, '//picture[@class="Et"]/img').get_attribute('src')
                except:
                        print("Картинки нет")
                try:
                    sku = href.split("/")[-2]
                except:
                    print("sku нет")

                category = ">".join(map(str, product_category))
                with open('31_03_2023_DM_MALL_new.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=";", lineterminator="\r")
                    writer.writerow(
                        [name, price, sale_price, picture, category, sku]
                    )
                print(name, price, sale_price, picture, category, sku)
            driver.close()
            driver.switch_to.window(winHandleBefore)






        driver.get("https://kz.detmir.com")
        CheckWindowMail();
        driver.implicitly_wait(10)
        ChoiceAktobe()

        i = 0


        print("Перехожу на категорию:", urls_category + "?filter=stores:3107%2C3396")
        driver.get(urls_category +"?filter=stores:3107%2C3396")
        CheckWindowMail();
        winHandleBefore = driver.window_handles[0]
        driver.implicitly_wait(10)
        CheckWindowMail()
        driver.implicitly_wait(10)
        product_category = []
        try:
           block_header = driver.find_element(By.XPATH, '//header[@class="Hz ix"]/nav[@aria-label="breadcrumb"]')
           for element in block_header.find_elements(By.XPATH, '//nav[@aria-label="breadcrumb"]/ul[@class="Ln Lw"]/li[@class="Lp"]'):
                 product_category.append(element.text)
        except:
              print("Нет категорий")
        try:
            product_urls = ParsingBlocksProducts(product_category)
        except Exception as e:
               print("ОШИБКА! В ПАРСИНГЕ БЛОКОВ ПРОДУКТОВ", e)
        try:
            ParsingProductPage(product_urls, winHandleBefore, product_category)
        except Exception as e:
                print("ОШИБКА В ПАРСИНГЕ СТРАНИЦ ПРОДУКТОВ", e)


    except Exception as ex:
                        print(ex)
    finally:
            driver.close()
            driver.quit()

if __name__ == '__main__':
    urls_category = []
    # Открыть файл с ссылками на продукты гигиены и ухода за детьми
    with open('DM_LINKS/Гигиена и уход/Гигиенические средства детские+ Бытовая химия детская.txt', 'r', encoding='utf-8') as file:
        # Прочитать все строки из файла
        lines = file.readlines()
        lines2 = []
        # Обработать каждую строку, удалив символы переноса строки и пробелы
        for line in lines:
            line = re.sub("^\s+|\n|\r|\s+$", '', line)
            lines2.append(line)
        # Добавить обработанные ссылки в список urls_category
        urls_category += lines2
    # Открыть файл с ссылками на продукты для питания и кормления детей
    with open('DM_LINKS/Товары для питания и кормления/Детское питание + Молочные продукты для детей+Сладости.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines2 = []
        for line in lines:
            line = re.sub("^\s+|\n|\r|\s+$", '', line)
            lines2.append(line)
        urls_category += lines2
    # Открыть файл с ссылками на продукты для купания и ванны детей
    with open('DM_LINKS/Гигиена и уход/Аксессуары для купания и ванны.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines2 = []
        for line in lines:
            line = re.sub("^\s+|\n|\r|\s+$", '', line)
            lines2.append(line)
        urls_category += lines2
    # Открыть файл с ссылками на пустышки и прорезыватели
    with open('DM_LINKS/Гигиена и уход/Пустышки и прорезыватели.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines2 = []
        for line in lines:
            line = re.sub("^\s+|\n|\r|\s+$", '', line)
            lines2.append(line)
        urls_category += lines2
    # Открыть файл с ссылками на аксессуары и средства для кормления
    with open('DM_LINKS/Товары для питания и кормления/Аксессуары и средства для кормления.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        lines2 = []
        for line in lines:
            line = re.sub("^\s+|\n|\r|\s+$", '', line)
            lines2.append(line)
        urls_category += lines2

    with open('31_03_2023_DM_MALL_new.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\r")
        writer.writerow(['name', 'priceDM', 'sale_price', 'picture', 'product_category', 'sku'])
    p = Pool(processes=3)
    p.map(MainParcer, urls_category)

