import argparse

from prefect import flow, task

from backlog_automation.readers.excel_reader import read_excel
from backlog_automation.readers.word_reader import read_word
from backlog_automation.generators.story_generator import generate_backlog
from backlog_automation.publishers.jira_publisher import publish_backlog
from backlog_automation.publishers.confluence_publisher import publish_pages
from backlog_automation.publishers.figma_publisher import publish_frames


@task(name="Read Excel")
def task_read_excel(path: str):
    return read_excel(path)


@task(name="Read Word")
def task_read_word(path: str):
    return read_word(path)


@task(name="Generate Backlog via Claude")
def task_generate(excel_data: dict, word_text: str):
    return generate_backlog(excel_data, word_text)


@task(name="Publish to Jira")
def task_jira(epics: list):
    return publish_backlog(epics)


@task(name="Publish to Confluence")
def task_confluence(pages: list):
    return publish_pages(pages)


@task(name="Publish to Figma")
def task_figma(frames: list):
    return publish_frames(frames)


@flow(name="Backlog Automation")
def run(excel_path: str, word_path: str):
    excel_data = task_read_excel(excel_path)
    word_text = task_read_word(word_path)

    backlog = task_generate(excel_data, word_text)

    jira_result = task_jira(backlog["epics"])
    confluence_result = task_confluence(backlog["confluence_pages"])
    figma_result = task_figma(backlog["figma_frames"])

    print(f"\nJira:       {len(jira_result)} issues created")
    print(f"Confluence: {len(confluence_result)} pages created")
    print(f"Figma:      {len(figma_result)} frames created")


def app():
    parser = argparse.ArgumentParser(description="Automate backlog creation from Excel and Word")
    parser.add_argument("--excel", required=True, help="Path to Excel input file")
    parser.add_argument("--word", required=True, help="Path to Word input file")
    args = parser.parse_args()
    run(excel_path=args.excel, word_path=args.word)


if __name__ == "__main__":
    app()
