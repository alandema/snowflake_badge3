
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(
    col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)

pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()

incredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=6,
)

if incredients_list:
    # st.write(incredients_list)
    # st.text(incredients_list)

    # incredients_string = ' '.join(incredients_list)
    incredients_string = ''

    for fruit_chosen in incredients_list:
        incredients_string += fruit_chosen + ' '   # had to do this for the hashes in the grader function  # noqa

    # st.text(incredients_string)

    time_to_insert = st.button("Submit Order")

    if incredients_string and time_to_insert:
        session.sql(
            "INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (?, ?)",
            params=[incredients_string, name_on_order]
        ).collect()

        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

    for fruit_chosen in incredients_list:
        url = f"https://fruityvice.com/api/fruit/{fruit_chosen}"
        fruityvice_response = requests.get(url)

        if fruityvice_response.status_code != 200:
            url = f"https://fruityvice.com/api/fruit/{fruit_chosen[:-1]}"
            fruityvice_response = requests.get(url)

        if fruityvice_response.status_code != 200:
            url = f"https://fruityvice.com/api/fruit/{fruit_chosen[:-3]}y"
            fruityvice_response = requests.get(url)

        if fruityvice_response.status_code != 200:
            search_on = pd_df.loc[pd_df['FRUIT_NAME']
                                  == fruit_chosen, 'SEARCH_ON'].iloc[0]
            url = f"https://fruityvice.com/api/fruit/{search_on}"
            fruityvice_response = requests.get(url)

        if fruityvice_response.status_code == 200:
            fv_df = st.dataframe(
                data=fruityvice_response.json(), use_container_width=True)


# # new section to display nutrition info
# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
# # st.text(fruityvice_response.json())
# fv_dt = st.dataframe(data=fruityvice_response.json(), use_container_width=True)


# # requirements.txt
# snowflake-connector-python
# snowflake-snowpark-python
# streamlit==1.31.1
# requests
