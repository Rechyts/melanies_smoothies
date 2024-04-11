# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothier :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothier.
    """
)

name_of_smoothier = st.text_input('Name of Smoothier: ')
st.write('The name of your Smoothier will be:', name_of_smoothier)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: '
    , my_dataframe
    ,max_selections=5
)
if ingredients_list:

    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        st.subheader(each_fruit+ " Nutrition Information")
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string +  """', '""" + name_of_smoothier + """')"""

    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()        
            st.success('Your Smoothie is ordered, '+ name_of_smoothier + '!', icon="✅")

    #st.write(my_insert_stmt)


