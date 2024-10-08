from dash import Dash, dcc, html, callback, Output, Input, no_update
import dash_bootstrap_components as dbc
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import TavilySearchResults
from dotenv import find_dotenv, load_dotenv
import os
import logging


logging.basicConfig(level=logging.DEBUG)

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

search_tool = TavilySearchResults()

def get_bank_logo(bank_name):
    logos = {
        "Industrial and Commercial Bank of China (ICBC)": "/assets/logos/ICBC-logo-500x281.png",
        "China Construction Bank Corporation": "/assets/logos/China-Construction-Bank-Corporation-Logo-500x315.png",
        "Agricultural Bank of China": "/assets/logos/Agricultural-Bank-of-China-logo-500x281.png",
        "Bank of China ltd": "/assets/logos/Bank-of-China-logo-500x300.png",
        "JPMorgan Chase":" /assets/logos/JPMorgan-Logo-500x281.png",
        "Bank of America": "/assets/logos/Bank-of-America-Logo-500x281.png",
        "Mitsubishi UFJ Financial Group": "/assets/logos/mizuho-financial-group9895.jpg",
        "HSBC Holdings plc": "/assets/logos/HSBC-Logo-500x281.png",
        "BNP Paribas": "/assets/logos/BNP-Paribas-Logo-500x281.png",
        "Crédit Agricole": "/assets/logos/Credit-Agricole-logo-500x281.png"
    }
    return logos.get(bank_name, "/assets/logos/default_logo.png")

# Defining agents:
researcher = Agent(
    role='Senior Research Analyst',
    goal="""Uncover the latest news and trends about the bank selected by the user in the task section. Provide the analysis in separate paragraphs for readability.""",
    backstory="""You work at a leading banking think tank. 
    Your expertise lies in identifying emerging trends.
    You have a knack for dissecting complex data and presenting actionable insights.""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool]
)
writer = Agent(
    role='Banking Content Strategist',
    goal='Craft compelling content from news on the selected bank. Organize the content into paragraphs.',
    backstory="""You are a famous Content Strategist, known for your insightful and engaging articles.
    You transform complex concepts into compelling narratives. You avoid complex words so it doesn't sound like you're an AI.""",
    verbose=True,
    allow_delegation=True,
)

critic_agent = Agent(
    role='Content Critique Specialist',
    goal="""Review the content provided by the Writer Agent and provide constructive feedback to enhance clarity, coherence, and engagement.
    If improvements are needed, indicate areas for revision.""",
    backstory="""You have an eye for detail and a knack for improving written content. 
    You review articles for quality, structure, and engagement, providing insightful feedback to refine the narrative.""",
    verbose=True,
    allow_delegation=False
)

# Создаем приложение Dash с использованием Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Multi AI Agent System - Bank Analysis", className='text-center text-primary, mb-4'))
    ]),
    dbc.Row([
        dbc.Col(html.P(
            "Select a bank for which you want to analyze the latest news and trends. Our AI agents will provide you with a detailed analysis and summary.",
            className='text-center'), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                ["Industrial and Commercial Bank of China (ICBC)",
                 "China Construction Bank Corporation",
                 "Agricultural Bank of China",
                 "Bank of China ltd",
                 "JPMorgan Chase",
                 "Bank of America",
                 "Mitsubishi UFJ Financial Group",
                 "HSBC Holdings plc",
                 "BNP Paribas",
                 "Crédit Agricole"],
                id="topic",
                placeholder="Select a bank...",
                className='mb-3'
            ),
        ], width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col(dbc.Checkbox(
            id='use-critic',
            label='Include Critic Agent for Improved Quality (May increase processing time)',
            className='mb-3',
            value=True  # По умолчанию критик включен
        ), width=6)
    ], justify='center'),
    dbc.Row([
        dbc.Col(
            dcc.Loading(  # Используем dcc.Loading для отображения индикатора загрузки
                id="loading",
                type="default",
                children=html.Div(id="loading-placeholder", className='text-center text-muted')
            )
        )
    ]),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody(id="answer-placeholder"), className="mt-3"))
    ])
], fluid=True)

@callback(
    Output("answer-placeholder", "children"),
    Output("loading-placeholder", "children"),
    Input("topic", "value"),
    Input("use-critic", "value"),
)
def activate_agent(bank_chosen, use_critic):
    if bank_chosen is None:
        return no_update, ""

    # Loading indicator
    loading_text = f"Analyzing {bank_chosen}... Please wait."
    logging.debug(f"Bank chosen: {bank_chosen}, Use critic: {use_critic}")

    try:

        paragraphs = []  # Инициализируем пустой список для хранения результата

        for _ in range(3):
            task1 = Task(
                description=f"""Conduct a comprehensive analysis of the latest news about {bank_chosen}.
                Identify key trends, investments, loans, acquisitions, or holdings. Research how macroeconomic 
                factors, such as interest rates, might impact the bank's performance. Ensure the analysis is well-structured with separate paragraphs.""",
                expected_output="Full analysis report in bullet points",
                agent=researcher
            )
            task2 = Task(
                description=f"""Using the insights provided, develop an engaging blog
                post that highlights the latest concerns and projections of {bank_chosen}.
                Support your arguments with key financial metrics and organize the content into clear paragraphs.""",
                expected_output="Full blog post in the form of 4 paragraphs",
                agent=writer
            )

            # If user chooses not to use critic
            agents = [researcher, writer]
            tasks = [task1, task2]

            # If users chooses to use critic
            if use_critic:
                logging.debug("Including critic agent in the process.")
                critique_task = Task(
                    description=f"""Review the blog post about {bank_chosen} and provide feedback on areas that need improvement.
                                Focus on clarity, coherence, and engagement. If revisions are needed, provide specific suggestions.""",
                    expected_output="Feedback on the blog post with suggestions for improvement.",
                    agent=critic_agent
                )
                agents.append(critic_agent)
                tasks.append(critique_task)
            else:
                logging.debug("Critic agent not included in the process.")

            crew = Crew(
                agents=agents,
                tasks=tasks,
                verbose=True,
                process=Process.sequential
            )

            result = crew.kickoff()
            logging.debug("Result received from crew kickoff.")

            if use_critic and "no further improvements needed" in result.raw.lower():
                break  # Если нет замечаний, выходим из цикла

        # Loading bank's logo
        bank_logo = get_bank_logo(bank_chosen)
        logo_img = html.Img(src=bank_logo, style={'width': '200px', 'margin': '20px auto'})

        # Editing results
        paragraphs = result.raw.split("\n\n")
        formatted_output = [dcc.Markdown(paragraph) for paragraph in paragraphs if paragraph.strip() != ""]

        return [logo_img] + formatted_output, ""

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message)
        return error_message, ""

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8080)