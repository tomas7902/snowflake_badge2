
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My name is Tom")

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.dataframe(my_fruit_list)


#Pick a fruitlist
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(my_fruit_list)

try:
  fruit_choice = streamlit.text_input("What fruit would you like to add?")
  if not fruit_choice:
    streamlit.error("Please sewlect a fruit to get information")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)

except URLerror as e:
  streamlit.error()
  
streamlit.stop()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("Select Current_user(),current_account(),current_region()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cur.execute("Select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.dataframe(my_data_row)

streamlit.text_input("What fruit would you like to add?")

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
