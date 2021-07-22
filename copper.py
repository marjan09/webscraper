from typing import Text
import httpx
import json
from lxml import html
from bs4 import BeautifulSoup
from numpy import mat
import re
import pandas as pd
from pandas import DataFrame


class CopperKey:
    def __init__(self, language='english'):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://standalone.kupferschluessel.de',
            'Connection': 'keep-alive',
            'Referer': 'https://standalone.kupferschluessel.de/suche.php?lang=german',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }

        self.cookies = {
            'PHPSESSID': 'k85a5p1dgvvo0oc2bfoeqroj34',
        }

        self.language = language

    def get_search_results(self, material_name):
        search_results = []

        try:
            data = {
                'werkstoff': material_name,
                'lang': [
                    self.language,
                    self.language
                ]
            }

            response = httpx.post('https://standalone.kupferschluessel.de/ergebnisse.php', headers=self.headers, cookies=self.cookies, data=data)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, features="html.parser")
                results = soup.find('select', {'class': 'selecter'}).find_all('option')
                search_results = list(map(lambda result: result['value'], results))

        except Exception as e:
            print(f"Error: {e}")

        return search_results

    def get_comparsion_materials(self, material_id):
        search_results = []

        try:
            data = {
                'werkstoff2': material_id,
                'lang': self.language
            }

            response = httpx.post('https://standalone.kupferschluessel.de/vergleichswerkstoffe.php', headers=self.headers, cookies=self.cookies, data=data)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, features="html.parser")
                results = soup.find('select', {'class': 'selecter'}).find_all('option')
                search_results = list(map(lambda result: result['value'], results))

        except Exception as e:
            print(f"Error: {e}")

        return search_results

    def get_material_data(self, material_id):
        material_data = {}

        try:
            data = {
                'werkstoff': material_id,
                'lang': self.language
            }

            response = httpx.post('https://standalone.kupferschluessel.de/content.php', headers=self.headers, cookies=self.cookies, data=data)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, features="html.parser")

                # content_table = soup.find('table', {'class': 'contenttab'}).findNext("tr")
                # b = content_table.findNext("table").find("td", {"class": "kategorie"})

                # text = b.string.extract()
                
                table = soup.find("table", class_="atabelle")

                # rows = table.find_all('tr')

                # for row in rows:
                #     print(row)
                # print(table)
                # with open('test556.html', 'w', encoding='utf-8') as file:
                #     file.write(str(table))

                dfs = pd.read_html(str(table), thousands=".", decimal=",")

                for i in dfs:
                    df = pd.DataFrame(i)
                    
                    df.fillna('',inplace=True)
                    df.loc[0, 0] = "Element"
                    df.loc[0, 1] = "Min"
                    df.loc[0, 2] = "Max"
                
                
                
                
                
                
                    
                
                b = df.iloc[0:16, [0,1,2]]
                # print(b)
                e = df.iloc[1:16, [5,6,7]].rename(columns = { 5: 0, 6: 1, 7: 2}, inplace=False)

                

                # asd = e.set_index(keys="Element")
                # # print(asd)
                # print(e)

                data_frame_1 = b.to_json(orient='records').replace(']', ',')
                
                data_frame_2 = e.to_json(orient='records')[1:]

                both_data = data_frame_1 + data_frame_2
                dict_data = {}
                kl  = soup.find("table", {"class":'contenttab'}).find_all('td', {'class': 'kategorie'})
                


                for origin in kl[1]:
                    
                    orig = origin.text
                #     dictionary[f"{orig.replace('[', '')}"] = f"{o}"

                # print(dictionary)
                    
                dict_data[orig.replace(u'\xa0', u' ').strip()] = str(both_data)
                dict_data = str(dict_data)
                dictionary_to_string = dict_data.replace("'[{", "[{").replace("]'}", "]}").replace("'", '"').replace("}]},", "}],").strip()
                # dictionary_to_string = str(dict_data).replace("'[", '[').replace("]'", "]").replace("'", '"').replace("]}", "],")
                # print(dictionary_to_string)

                
                
                with open("tralala456.json", "a", encoding="utf-8") as file:
                    file.write()

                   

                
                # with open("tralala.txt", "r", encoding="utf-8") as file:
                #     content = file.read()
                #     print(content)
  
                # for origin in kl[1]:
                #     orig = origin
                for material in kl[0]:
                    mat = material.replace(":", "")
                    
                
                
                div  = soup.find("table", {"class":'contenttab'}).find_all('tr')
                # for element in div[5:10]:
                #     find_other_td = element.find_all("td")
                    
                #     for some_element in find_other_td:
                #         # print(some_element)
                #         print(some_element)
                        
                        
                        # if len(some_element) == 13:
                        #     find_data = some_element.find_all('td', {'class': 'dspalte1'})
                        #     print(find_data)
                            
                    # if find_other_td[-1].value().lower() != "standarts":

                 
                
                # for j in find_other_td:
                #     # prin
                #     pass
                for child in div[4:]:
                    string = child.find_all('td', {"class": 'kleins'})
                    find_data = child.find_all('td', {'class': 'dspalte1'})
                    for j in find_data:
                        pass
                    for property in string:
                        material_data[f'{mat}'] = orig.text.replace(u'\u00a0', '')
                        material_data[f'{property.text}'] = f'{j.text}'

                header_row = soup.select('table >  tr > td.kategorie')[-1]
                if header_row.text.lower() != "remark":
                    pass
                else:
                    header = header_row.findNext('td', class_='dspalte1')
                    text = header.text
                    material_data["Remark"] = text.replace(u'\u00a0', '')


        except Exception as e:
            print(f"Error: {e}",f"{material_id}")
        

        return material_data
    
        

    def crawl(self):
        copper_data = {}
        with open('copper_materials.json', 'r', encoding='utf-8', errors="ignore") as file:
            material_designations = json.loads(file.read())


        for material_designation in material_designations[1600:1604]:
            copper_data[material_designation] = {}
            materials = self.get_search_results(material_designation)

            for material_id in materials:
                print(f"Crawling {material_designation}:{material_id}")
                copper_data[material_designation][material_id] = {}

                comparsion_materials = self.get_comparsion_materials(material_id)
                copper_data[material_designation][material_id]['comparsion_materials'] = comparsion_materials

                material_data = self.get_material_data(material_id)
                copper_data[material_designation][material_id]['data'] = material_data
        # with open('copper_data_witsshout_tablewww.json', 'w', encoding='utf-8', errors="ignore") as file:
        #     file.write(json.dumps(copper_data))


coperkey = CopperKey()
coperkey.crawl()

