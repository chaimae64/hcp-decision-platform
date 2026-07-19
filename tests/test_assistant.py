from database.database_service import DatabaseService
from assistant.assistant_ai import AssistantAI

df = DatabaseService.load_table("chomage_v2")

question = "Pourquoi le chômage augmente ?"

response = AssistantAI.ask(
    question,
    df
)

print(response)