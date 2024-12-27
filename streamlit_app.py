# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize your smoothie:cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie
    """
)

cnx = st.connection('snowflake')
session = cnx.session()

name_on_order = st.text_input("Name on Smoothie : ")
st.write("The Name on your smoothie will be:", name_on_order)
# option = st.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone"),
# )

# st.write("You selected:", option)

# option = st.selectbox("what is your favourite fruit?",("Banana","Strawbeery","Peaches"))
# st.write("your favourite fruit is :", option)

# session = get_active_session()
dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data= dataframe, use_container_width=False, )


#multi select widget
INGREDIENTS_LIST = st.multiselect('Choose upto 5 ingredients:',dataframe,max_selections = 5)

#to print or write the select values only whne a option is selected
if INGREDIENTS_LIST:
    ingredients_string = ''
    for fruit_chosen in INGREDIENTS_LIST:
        ingredients_string+=fruit_chosen + '   '
    # st.write(ingredients_string)
#inserting the orders in orders table    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    # so only once every fruit is selected and ordered , then only we need to insert in a single order row
    time_to_insert = st.button('Submit Order')
    # st.write(my_insert_stmt)
    if time_to_insert:
        # ----inserting the values to table and printing the success message
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!' + ','+ name_on_order, icon="✅")
