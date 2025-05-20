import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

TEXT_KEYS = ("rich_text", "caption")  # don't include 'title'

def _block_text(block: dict) -> str:
    blk_type = block["type"]
    data = block.get(blk_type, {})
    out = []

    if blk_type == "child_page":
        out.append(data.get("title", ""))  # handle page title only
    else:
        for key in TEXT_KEYS:
            if key in data:
                value = data[key]
                if isinstance(value, list):
                    for rt in value:
                        out.append(rt.get("plain_text", ""))
                elif isinstance(value, str):
                    out.append(value)

    return "".join(out)

def extract_recursive(block_id: str, level: int = 0) -> str:
    out, cursor = [], None
    indent = "    " * level  # optional: indent for child blocks
    while True:
        resp = notion.blocks.children.list(block_id=block_id, start_cursor=cursor)
        for blk in resp["results"]:
            blk_type = blk["type"]

            # 1️⃣ Append this block’s text (if any)
            txt = _block_text(blk)
            if txt:
                out.append(f"{indent}{txt}")

            # 2️⃣ If it's a child_page, also recurse into that subpage
            if blk_type == "child_page":
                subpage_id = blk["id"]
                out.append(extract_recursive(subpage_id, level + 1))

            # 3️⃣ Also recurse into children of other blocks like toggles, callouts, etc.
            elif blk.get("has_children", False):
                out.append(extract_recursive(blk["id"], level + 1))

        if not resp.get("has_more"):
            break
        cursor = resp.get("next_cursor")

    return "\n".join(out)


if __name__ == "__main__":
    # 👉 share the private page with your integration and paste its 32-char ID here
    PAGE_ID = "d6d2e15e842b440fa7c098a3d899fa47"
    notes = extract_recursive(PAGE_ID)
    