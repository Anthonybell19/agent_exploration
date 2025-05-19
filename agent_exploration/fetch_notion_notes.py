from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

def get_page_text(block_id):
    blocks = notion.blocks.children.list(block_id=block_id)
    text = []
    for block in blocks['results']:
        block_type = block['type']
        if 'text' in block.get(block_type, {}):
            texts = block[block_type]['text']
            for t in texts:
                text.append(t['plain_text'])
    return '\n'.join(text)

def get_all_notes_from_database(database_id):
    pages = notion.databases.query(database_id=database_id)['results']
    notes = []
    for page in pages:
        page_id = page['id']
        content = get_page_text(page_id)
        notes.append(content)
    return notes
