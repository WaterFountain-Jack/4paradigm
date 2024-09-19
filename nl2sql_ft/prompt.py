def get_system_prompt(db_type):
    return f'''You are a {db_type} expert. I will give you an input question and ask you to help me create a syntactically correct MySQL query to run
Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in backticks (`) to denote them as delimited identifiers.
Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
Pay attention to use CURDATE() function to get the current date, if the question involves "today". 

'''

def get_role_prompt(table_selected_info,user_query,example):
    prompt = f"""
Database schema information:
{table_selected_info}
The question is: {user_query}

/* Some SQL examples are provided based on similar problems: */

"""
    #random
    # for data in random.sample(example,num_example):
    #nomol
    for data in example:
        prompt = prompt + f"""Question: {data["query"]}
SQLQuery: {data["sql"]}

"""
    prompt =  prompt +'''Please use the following format for output:

Question: Question here
SQLQuery: SQL Query to run
Result: The results obtained from the query'''
    # logger.critical(f"选择的example条数为：{num_example}")
    return prompt