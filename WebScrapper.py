from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sqlite3

#First we need to create our data base
connection = sqlite3.connect("#####/Pizza.db") # - input the path were you want the database file
cur = connection.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS pizza
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE,
                  ranking TEXT,
                  opiniones TEXT,
                  address TEXT,
                  created_at DATETIME DEFAULT CURRENT_TIMESTAMP);''')

#Start the function, open the browser, maximmize the window and get the website.
def pedidos_ya(direccion, food):
  driver = webdriver.Chrome()
  driver.implicitly_wait(30)
  driver.maximize_window()
  #Website we want to scrappe   
  driver.get("https://www.pedidosya.com.uy")
  
  
  
  try:
    #We find all the elementes we need to do the search
    #First of all the address input
    input_nombre = driver.find_element_by_id("address")
    #We sent the string we want to use
    input_nombre.send_keys(direccion)
    #The kind of food we want to find
    input2_nombre = driver.find_element_by_id("optional")
    #Sent the food
    input2_nombre.send_keys(food)
    #The button we need to click to confirm
    boton = driver.find_element_by_id("search")
    boton.click()

    #In this case this website needs a confirmation of the address, for some reason the button only works if you click twice 
    confirm = driver.find_element_by_xpath("//*[@id='confirm']")
    confirm.click()
    confirm.click()
  
  
  except:
    #Mostramos este mensaje en caso de que se presente algún problema
    print ("El elemento no está presente")
  
  
  #Now we need to select all the elements that we want to scrape
  
  nombres = driver.find_elements_by_class_name("arrivalName") 
  ranking = driver.find_elements_by_class_name("rating-points")
  opiniones = driver.find_elements_by_xpath("//*[contains(text(),'opiniones')]")
  address = driver.find_elements_by_xpath("//span[@class='address']")
  
  # We iterate throught every one of the elements we want to save in the data base, in this case I used a zip function
  # So in that way we can iterate every element at the same time, also we need to encode to UTF-8, since some names uses latini and other codecs
  # And we save it to the database
  for a,b,c,d in zip(nombres, ranking, opiniones,  address):
    try:
      cur.execute('''INSERT INTO pizza(name, ranking, opiniones, address)
                VALUES(?, ?, ?, ?)''', (a.text.encode(), b.text.encode(), c.text.encode(), d.text.encode()))

      
      
    except:
      print("Elementos no encontrados")
      
  #We close the browser
  driver.close() 
  
  
  #Send a commit to the data base and close it.
  #We left the commit out of the for because we don't want to commit every time we find a result, that consumes much more resources
  connection.commit()
  connection.close()

  

#Calling the function with the parameters we want.
def main():
  print(pedidos_ya('Avenida General Rivera 4134','Pizza'))

main()

